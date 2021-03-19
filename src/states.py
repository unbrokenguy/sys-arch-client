import json
import mimetypes
from pathlib import Path
import os
from file_manager import State
from utils import Tools


class ExitState(State):
    def action(self):
        exit()


class PreviousState(State):
    def action(self):
        self.context.next(self.context.prev_state)


base_actions = {"Выход": ExitState, "Назад": PreviousState}


class UploadState(State):
    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update({"Начать ввод": EntryState})

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        Tools.print_choose_dict(choices)
        user_input = input()
        if user_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        elif choices[user_input] == "Начать ввод":
            raw_data = input()
            if os.path.isfile(raw_data):
                files = {"data": open(raw_data, "rb")}
                self.context.api.create_file(files)
            else:
                self.context.api.create_user_input(raw_data)
            self.context.next(self.actions[choices[user_input]]())
        else:
            self.context.next(self.actions[choices[user_input]]())


def get_choices(choices):
    choices["choose"].extend(list(base_actions.keys()))
    choices = Tools.get_choose_dict(choices)
    Tools.print_choose_dict(choices)
    return choices


class DownloadState(State):

    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update({"Выбрать категорию": EntryState})

    def download_file(self, category, file):
        response = self.context.api.get_data(file["id"])
        if response.status_code == 200:
            path = Path(f"{self.context.storage_path}/{category['name']}/")
            path.mkdir(parents=True, exist_ok=True)
            file_name = f"{path}/{Tools.random_string()}{mimetypes.guess_extension(response.headers['content-type'])}"
            if not os.path.isfile(file_name):
                print(path)
                with open(file_name, "wb+") as destination:
                    for chunk in response:
                        destination.write(chunk)
            Tools.print_ok_message(f"Файл успешно загружен в {file_name}")

    def download_choices(self, category, unpack_value):
        response = self.context.api.get_category_data(category["id"])
        values = json.loads(response.text)
        choices = self.format_to_choose(values, unpack_value)
        return values, choices

    def handle_user_input_download(self, category):
        values, choices = self.download_choices(category, "name")
        choice = input()
        if choices[choice] in base_actions.keys():
            return base_actions[values[choice]]
        if choice not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        else:
            user_input = {}
            for d in values:
                if d["name"] == choices[choice]:
                    user_input = d
            response = self.context.api.get_data(user_input["id"])
            if response.status_code == 200:
                Tools.print_ok_message("Данные успешно получены.")
                print(response.text)

    def handle_file_download(self, category):
        files, choices = self.download_choices(category, "name")
        file_name_input = input()
        if choices[file_name_input] in base_actions.keys():
            return base_actions[files[file_name_input]]
        if file_name_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        else:
            file = 0
            for d in files:
                if d["name"] == choices[file_name_input]:
                    file = d
            self.download_file(category, file)
        return None

    def format_to_choose(self, categories, unpack_value):
        temp = {"choose": [d[unpack_value] for d in categories]}
        return get_choices(temp)

    def handle_download(self):
        categories = json.loads(self.context.api.get_categories().text)
        choices = self.format_to_choose(categories, "name")
        category_input = input()
        if category_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        elif choices[category_input] in base_actions.keys():
            return base_actions[choices[category_input]]
        else:
            category = {}
            is_file = True
            for d in categories:
                if d["name"] == choices[category_input]:
                    category = d
                    if d["name"] == "Строки" or d["name"] == "Числа":
                        is_file = False
            if is_file:
                return self.handle_file_download(category)
            else:
                return self.handle_user_input_download(category)
        return None

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        Tools.print_choose_dict(choices)
        user_input = input()
        if user_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        elif choices[user_input] == "Выбрать категорию":
            go_to = self.handle_download()
            self.context.next(
                go_to() if go_to is not None else self.actions[choices[user_input]]()
            )
        else:
            self.context.next(self.actions[choices[user_input]]())


class LoginState(State):
    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update(
            {
                "Ввести логин и пароль": EntryState
            })

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        Tools.print_choose_dict(choices)
        user_input = input()
        if user_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        elif choices[user_input] == "Ввести логин и пароль":
            print("Введите логин")
            username = input()
            print("Введите пароль")
            password = input()
            self.context.api.login(username, password)
            self.context.next(self.actions[choices[user_input]]())


class EntryState(State):
    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update(
            {
                "Загрузить данные на сервер": UploadState,
                "Скачать файл с сервера": DownloadState,
            }
        )

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        Tools.print_choose_dict(choices)
        user_input = input()
        if user_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        else:
            self.context.next(self.actions[choices[user_input]]())

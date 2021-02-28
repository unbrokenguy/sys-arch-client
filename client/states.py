import json
from pathlib import Path
import requests
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
        self.actions.update({"Начать ввод": StartState})

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        Tools.print_choose_dict(choices)
        user_input = input()
        if user_input not in choices.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        elif choices[user_input] == "Начать ввод":
            raw_data = input()
            if os.path.isfile(raw_data):
                files = {"file": open(raw_data, "rb")}
                response = requests.post(
                    url=f"{self.context.server_url}/upload/",
                    headers={},
                    data={},
                    files=files,
                )
            else:
                data = {"user_input": raw_data}
                response = requests.post(
                    url=f"{self.context.server_url}/upload/", headers={}, data=data
                )
            Tools.handle_response(response)
            self.context.next(self.actions[choices[user_input]]())
        else:
            self.context.next(self.actions[choices[user_input]]())


class DownloadState(State):
    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update({"Выбрать категорию": StartState})

    def file_response(self, response):
        if "status" in response.text:
            Tools.handle_response(response)
            return False
        elif "data" in response.text:
            data = json.loads(response.text)
            Tools.print_ok_message("Данные успешно получены.")
            print(data["data"])
            return False
        return True

    def download(self, category, file_name):
        response = requests.get(
            url=f"{self.context.server_url}/download?file_type={category}&file_name={file_name}",
            stream=True,
        )
        if self.file_response(response):
            if response.status_code == 200:
                path = Path(f"{self.context.storage_path}/{category}/")
                path.mkdir(parents=True, exist_ok=True)
                if not os.path.isfile(f"{path}/{file_name}"):
                    with open(f"{path}/{file_name}", "wb+") as destination:
                        for chunk in response:
                            destination.write(chunk)
                Tools.print_ok_message(f"Файл успешно загружен в {path}/{file_name}")

    def get_choises(self, choices):
        choices["choose"].extend(list(base_actions.keys()))
        choices = Tools.get_choose_dict(choices)
        Tools.print_choose_dict(choices)
        return choices

    def handle_file_download(self, file_category):
        response = requests.get(
            url=f"{self.context.server_url}/download?file_type={file_category}"
        )
        files = json.loads(response.text)
        files = self.get_choises(files)
        file_name_input = input()
        if files[str(file_name_input)] in base_actions.keys():
            return base_actions[files[file_name_input]]
        if file_name_input not in files.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        else:
            self.download(file_category, files[file_name_input])
        return None

    def handle_download(self):
        categories = json.loads(
            requests.get(url=f"{self.context.server_url}/download").text
        )
        categories = self.get_choises(categories)
        category_input = input()
        if category_input not in categories.keys():
            Tools.print_error("Пожалуйста введите корректные данные.")
        elif categories[category_input] in base_actions.keys():
            return base_actions[categories[category_input]]
        else:
            return self.handle_file_download(categories[category_input])
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


class StartState(State):
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

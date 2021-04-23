import json
import mimetypes
import os
from getpass import getpass
from pathlib import Path
from file_manager import StateStrategy
from utils import Tools


def get_choices(choices):
    from states import ExitState, PreviousState

    base_actions = {"Выход": ExitState, "Назад": PreviousState}
    choices["choose"].extend(list(base_actions.keys()))
    choices = Tools.get_choose_dict(choices)
    Tools.print_choose_dict(choices)
    return choices


def try_except_decorator(func):
    """Wraps the function in a try ... except ... block so that no need to handle KeyError manually

    Args:
        func: function to wrap
    """

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except KeyError:
            Tools.print_error("Пожалуйста введите корректные данные.")

    return wrapper


class LoginStateStrategy(StateStrategy):

    # Оборачивает нашу функцию в try except чтобы дальше мы не обрабатывали сами каждую KeyError ошибку
    @try_except_decorator
    def action(self, **kwargs):
        choices = kwargs["choices"]
        # Печатаем меню, которое нам передали
        Tools.print_choose_dict(choices)
        user_input = input()
        # Добавляем ввод пользователя в именнованные аргументы
        kwargs.update({"user_input": user_input})
        if choices[user_input] == "Ввести логин и пароль":
            email = input("Введите почту:")
            password = getpass("Введите пароль:")
            self.context.api.login(email, password)
        # Получаем следущее состояние
        next_state = self.basic_action(**kwargs)
        return next_state


class DownloadStateStrategy(StateStrategy):
    def handle_user_input_download(self, category, **kwargs):
        # Получаем данные и меню
        values, choices = self.download_choices(category, "name")
        choice = input()
        user_input = {}
        for d in values:
            if d["name"] == choices[choice]:
                user_input = d
        if len(user_input.keys()) == 0:
            # Выбрали не данные
            return self.basic_action(**kwargs)()
        # Получаем данные с сервера
        response = self.context.api.get_data(user_input["id"])
        if response.status_code == 200:
            Tools.print_ok_message("Данные успешно получены.")
            print(response.text)

    def download_file(self, category, file, **kwargs):
        # Запрашивем данные по id с сервера
        response = self.context.api.get_data(file["id"])
        if response.status_code == 200:
            # Составляем путь куда мы хотим сохранить данные
            path = Path(f"{self.context.storage_path}/{category['name']}/")
            # Если не существует, создаем директории по всему пути.
            path.mkdir(parents=True, exist_ok=True)
            # Создаем случайное.                         Расширение файла
            file_name = f"{path}/{Tools.random_string()}{mimetypes.guess_extension(response.headers['content-type'])}"
            if not os.path.isfile(file_name):
                print(path)
                with open(file_name, "wb+") as destination:
                    for chunk in response:
                        destination.write(chunk)
            Tools.print_ok_message(f"Файл успешно загружен в {file_name}")

    def download_choices(self, category, unpack_value):
        # Получаем с сервера все данные в конкретной категории
        response = self.context.api.get_category_data(category["id"])
        values = json.loads(response.text)
        # Распаковываем данные в знакомы формат словаря choose
        choices = self.format_to_choose(values, unpack_value)
        return values, choices

    def handle_file_download(self, category, **kwargs):
        # Получаем данные и меню
        files, choices = self.download_choices(category, "name")
        user_input = input()
        file = None
        for d in files:
            if d["name"] == choices[user_input]:
                file = d
        if not file:
            # Данные выбраны не были
            return self.basic_action(**kwargs)()
        # Данные выбраны
        return self.download_file(category, file, **kwargs)

    def format_to_choose(self, categories, unpack_value):
        temp = {"choose": [d[unpack_value] for d in categories]}
        return get_choices(temp)

    def handle_download(self):
        # Запрашиваем список категорий с сервера
        categories = json.loads(self.context.api.get_categories().text)
        # Распаковываем данные в знакомы формат словаря choose
        choices = self.format_to_choose(categories, "name")
        category_input = input()
        category = {}
        # Проверка категории
        is_file = True
        for d in categories:
            if d["name"] == choices[category_input]:
                category = d
                if d["name"] == "Строки" or d["name"] == "Числа":
                    is_file = False
                break
        if is_file:
            # Загрузка файла
            return self.handle_file_download(category)
        else:
            # Загрузка Строк и Чисел
            return self.handle_user_input_download(category)

    # Оборачивает нашу функцию в try except чтобы дальше мы не обрабатывали сами каждую KeyError ошибку
    @try_except_decorator
    def action(self, **kwargs):
        choices = kwargs["choices"]
        # Печатаем меню, которое нам передали
        Tools.print_choose_dict(choices)
        user_input = input()
        # Добавляем ввод пользователя в именнованные аргументы
        kwargs.update({"user_input": user_input})
        next_state = None
        if choices[user_input] == "Выбрать категорию":
            # Возвращает следущее состояние или None
            next_state = self.handle_download()
        # next_state = next_state if bool(next_state) else self.basic_action(**kwargs)
        # next_state важнее self.basic_action(**kwargs)
        next_state = next_state or self.basic_action(**kwargs)
        if not next_state:
            # Если next_state None, то пользователь точно ошибся
            raise KeyError
        return next_state


class UploadStateStrategy(StateStrategy):

    # Оборачивает нашу функцию в try except чтобы дальше мы не обрабатывали сами каждую KeyError ошибку
    @try_except_decorator
    def action(self, **kwargs):
        choices = kwargs["choices"]
        # Печатаем меню, которое нам передали
        Tools.print_choose_dict(choices)
        user_input = input()
        # Добавляем ввод пользователя в именнованные аргументы
        kwargs.update({"user_input": user_input})
        if choices[user_input] == "Начать ввод":
            raw_data = input()
            if os.path.isfile(raw_data):
                files = {"data": open(raw_data, "rb")}
                # Отправляем запрос на сервер
                self.context.api.create_data({"data": files})
            else:
                # Отправляем запрос на сервер
                self.context.api.create_data({"data": raw_data})
        # Получаем следущее состояние
        return self.basic_action(**kwargs)

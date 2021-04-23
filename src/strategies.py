import json
import os
from getpass import getpass
from pathlib import Path
from file_manager import StateStrategy
from utils import Tools


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
    """
    Sign in strategy.
    If Server sign in method changed, only need to change Login Strategy, not Login State.
    """

    @try_except_decorator  # Оборачивает нашу функцию в try чтобы не обрабатывать каждый раз KeyError ошибку
    def action(self, **kwargs):
        choices = kwargs["choices"]
        user_input = Tools.handle_menu_options(choices)  # Печатаем меню, которое нам передали

        kwargs.update({"user_input": user_input})  # Добавляем ввод пользователя в именнованные аргументы

        if choices[user_input] == "Ввести логин и пароль":
            email = input("Введите почту:")
            password = getpass("Введите пароль:")
            self.context.api.login(email, password)

        next_state = StateStrategy.basic_action(**kwargs)  # Получаем следущее состояние
        return next_state


def format_to_choose(categories, unpack_value):
    """Unpack categories (response from Server) with given unpack value. And formatting it to choose dict.
    Args:
        categories: List of Dict[categories]
        unpack_value: String with value to get from Dict[categories]
    Returns:
        Choices Dict.
    """
    return Tools.get_choices([d[unpack_value] for d in categories])


class DownloadStateStrategy(StateStrategy):
    """
    Define how to download data from Server.
    """

    def handle_user_input_download(self, category, **kwargs):
        values, choices = self.download_choices(category, "name")  # Получаем данные и меню
        choices = Tools.get_choose_dict(choices)
        choice = Tools.handle_menu_options(choices)
        user_input = {}
        for d in values:
            if d["name"] == choices[choice]:
                user_input = d
        if len(user_input.keys()) == 0:
            return StateStrategy.basic_action(**kwargs)()  # Выбрали не данные
        response = self.context.api.get_data(user_input["id"])  # Получаем данные с сервера
        if response.status_code == 200:
            Tools.print_ok_message("Данные успешно получены.")
            print(response.text)

    def download_file(self, category, file):
        response = self.context.api.get_data(file["id"])  # Запрашивем данные по id с сервера
        if response.status_code == 200:
            path = Path(f"{self.context.storage_path}/{category['name']}/")  # Составляем путь куда сохранить данные
            path.mkdir(parents=True, exist_ok=True)  # Если не существует, создаем директории по всему пути.

            file_name = Tools.generate_file_name(path, response.headers["content-type"])  # random_file_name.extension

            if not os.path.isfile(file_name):
                print(path)
                with open(file_name, "wb+") as destination:
                    for chunk in response:
                        destination.write(chunk)
            Tools.print_ok_message(f"Файл успешно загружен в {file_name}")

    def download_choices(self, category, unpack_value):
        response = self.context.api.get_category_data(category["id"])  # Получаем с сервера все данные в категории
        values = json.loads(response.text)
        choices = format_to_choose(values, unpack_value)  # Распаковываем данные в знакомы формат словаря choose
        return values, choices

    def handle_file_download(self, category, **kwargs):
        files, choices = self.download_choices(category, "name")  # Получаем данные и меню
        choices = Tools.get_choose_dict(choices)
        user_input = Tools.handle_menu_options(choices)
        file = None

        for d in files:
            if d["name"] == choices[user_input]:
                file = d

        if not file:
            return StateStrategy.basic_action(**kwargs)()  # Данные выбраны не были

        return self.download_file(category, file)  # Данные выбраны

    def handle_download(self):
        categories = json.loads(self.context.api.get_categories().text)  # Запрашиваем список категорий с сервера
        choices = format_to_choose(categories, "name")  # Распаковываем данные в знакомы формат словаря choose
        choices = Tools.get_choose_dict(choices)
        category_input = Tools.handle_menu_options(choices)
        category = {}

        is_file = True  # Проверка категории
        for d in categories:
            if d["name"] == choices[category_input]:
                category = d
                if d["name"] == "Строки" or d["name"] == "Числа":
                    is_file = False
                break
        if is_file:
            return self.handle_file_download(category)  # Загрузка файла
        else:
            return self.handle_user_input_download(category)  # Загрузка Строк и Чисел

    @try_except_decorator  # Оборачивает нашу функцию в try чтобы не обрабатывать каждый раз KeyError ошибку
    def action(self, **kwargs):
        choices = kwargs["choices"]
        user_input = Tools.handle_menu_options(choices)  # Печатаем меню, которое нам передали

        kwargs.update({"user_input": user_input})  # Добавляем ввод пользователя в именнованные аргументы

        next_state = None

        if choices[user_input] == "Выбрать категорию":
            next_state = self.handle_download()  # Возвращает следущее состояние или None

        next_state = next_state or StateStrategy.basic_action(**kwargs)
        # next_state = next_state if bool(next_state) else self.basic_action(**kwargs)
        # next_state важнее self.basic_action(**kwargs)

        if not next_state:
            raise KeyError  # Если next_state None, то пользователь точно ошибся

        return next_state


class UploadStateStrategy(StateStrategy):
    """
    Define how to upload data to Server.
    """

    @try_except_decorator  # Оборачивает нашу функцию в try чтобы не обрабатывать каждый раз KeyError ошибку
    def action(self, **kwargs):
        choices = kwargs["choices"]
        user_input = Tools.handle_menu_options(choices)  # Печатаем меню, которое нам передали

        kwargs.update({"user_input": user_input})  # Добавляем ввод пользователя в именнованные аргументы

        if choices[user_input] == "Начать ввод":
            raw_data = input()
            if os.path.isfile(raw_data):
                files = {"data": open(raw_data, "rb")}
                self.context.api.create_data({"data": files})  # Отправляем запрос на сервер
            else:
                self.context.api.create_data({"data": raw_data})  # Отправляем запрос на сервер

        return StateStrategy.basic_action(**kwargs)  # Получаем следущее состояние

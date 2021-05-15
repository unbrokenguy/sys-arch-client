import json
import os
from pathlib import Path

from file_manager import StateStrategy
from utils import Tools, format_to_choose


class DownloadStrategy(StateStrategy):
    """
    Define how to download data from Server.
    """

    def download_user_input(self, category):
        response = self.context.api.get_data(category["id"])  # Получаем данные с сервера
        if response.status_code == 200:
            Tools.print_ok_message("Данные успешно получены:")
            print(response.text)

    def download_file(self, category):
        response = self.context.api.get_data(category["id"])  # Запрашивем данные по id с сервера
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

    def handle_download(self):
        categories = json.loads(self.context.api.get_categories().text)  # Запрашиваем список категорий с сервера
        choices = format_to_choose(categories, "name")  # Распаковываем данные в знакомы формат словаря choose
        menu = Tools.get_choose_dict(choices)
        category_input = Tools.handle_menu_options(menu)
        category = {}
        is_file = True  # Проверка категории
        for d in categories:
            if d["name"] == menu[category_input]:
                category = d
                if d["name"] == "Строки" or d["name"] == "Числа":
                    is_file = False
                break
        if is_file:
            self.download_file(category)  # Загрузка файла
        else:
            self.download_user_input(category)  # Загрузка Строк и Чисел
        return

    def action(self, **kwargs):
        choices = kwargs["choices"]
        user_input = Tools.handle_menu_options(choices)  # Печатаем меню, которое нам передали

        kwargs.update({"user_input": user_input})  # Добавляем ввод пользователя в именнованные аргументы

        if choices[user_input] == "Выбрать категорию":
            self.handle_download()

        return StateStrategy.basic_action(**kwargs)

import os

from file_manager import StateStrategy
from utils import try_except_decorator, Tools


class UploadStrategy(StateStrategy):
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

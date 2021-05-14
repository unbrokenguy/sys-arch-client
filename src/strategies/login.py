from getpass import getpass

from file_manager import StateStrategy
from utils import try_except_decorator
from utils import Tools


class LoginStrategy(StateStrategy):
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

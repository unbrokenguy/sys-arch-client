from file_manager import State
from strategies import LoginStateStrategy, DownloadStateStrategy, UploadStateStrategy
from utils import Tools


class ExitState(State):
    """
    State handle exit from our Application.
    """

    def action(self):
        """Exit from program."""
        exit()


class PreviousState(State):
    """
    State handle go to previous State in our Application.
    """

    def action(self):
        """
        Set FileManager state to previous State.
        """
        self.context.next(self.context.prev_state)


base_actions = {"Выход": ExitState, "Назад": PreviousState}


class LoginState(State):
    """
    Login State for FileManager Application.
    """

    def __init__(self):
        """
        self.actions это словарь действий и состояний, которые может совершить пользователь,
        после выполнения переходит на слудущее состояние
        """
        super().__init__()

        self.actions = dict.copy(base_actions)
        self.actions.update({"Ввести логин и пароль": MainState})

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})  # Составляем меню действий

        strategy = LoginStateStrategy()  # Выбираем стратегию
        strategy.context = self.context

        # Переходим на следущее состояние, которое нам вернет стратегия по меню.
        self.context.next(self.actions[strategy.action(choices=choices)]())


class MainState(State):
    """
    Main State for FileManager application
    Uploads or Download File by Strategy.
    """

    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update(
            {
                "Загрузить данные на сервер": MainState,
                "Скачать файл с сервера": MainState,
            }
        )
        self.strategies = dict(zip(self.actions.keys(), [None, None, UploadStateStrategy, DownloadStateStrategy]))
        self.strategies_actions = dict(
            zip(self.actions.keys(), [None, None, {"Начать ввод": MainState}, {"Выбрать категорию": MainState}])
        )

    def action(self):
        # Составляем меню действий
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        # Сами печатаем меню, не в стратегии
        Tools.print_choose_dict(choices)
        user_input = input()
        # Выбираем стратегию
        try:
            strategy = self.strategies[choices[user_input]]
            # Не у всех действий есть стратегия
            if not strategy:
                # Переходим на следущее состояние у действия
                self.context.next(self.actions[user_input]())
            else:
                # Если стратегия есть
                strategy = strategy()
                strategy.context = self.context
                # Составляем словарь действий и состояний для стратегии
                _strategy_actions = dict.copy(base_actions)
                _strategy_actions.update(self.strategies_actions[choices[user_input]])
                # Составляем меню для стратегии
                _choices = Tools.get_choose_dict(data={"choose": list(_strategy_actions.keys())})
                # Переходим на следущее состояние, которое нам вернет стратегия по меню.
                self.context.next(self.actions[strategy.action(choices=_choices)]())
        except KeyError:
            pass

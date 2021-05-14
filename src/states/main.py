from file_manager import State
from states import ExitState, PreviousState
from strategies import UploadStrategy, DownloadStrategy
from utils import Tools


class MainState(State):
    """
    Main State for FileManager application
    Uploads or Download File by Strategy.
    """

    def __init__(self):
        super().__init__()
        self.base_actions = {"Выход": ExitState, "Назад": PreviousState}
        self.actions = dict.copy(self.base_actions)
        self.actions.update(
            {
                "Загрузить данные на сервер": MainState,
                "Скачать файл с сервера": MainState,
            }
        )
        self.strategies = dict(zip(self.actions.keys(), [None, None, UploadStrategy, DownloadStrategy]))
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
                _strategy_actions = dict.copy(self.base_actions)
                _strategy_actions.update(self.strategies_actions[choices[user_input]])
                # Составляем меню для стратегии
                _choices = Tools.get_choose_dict(data={"choose": list(_strategy_actions.keys())})
                # Переходим на следущее состояние, которое нам вернет стратегия по меню.
                self.context.next(self.actions[strategy.action(choices=_choices)]())
        except KeyError:
            pass

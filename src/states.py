from file_manager import State
from strategies import LoginStateStrategy, DownloadStateStrategy, UploadStateStrategy
from utils import Tools


class ExitState(State):
    def action(self):
        exit()


class PreviousState(State):
    def action(self):
        self.context.next(self.context.prev_state)


base_actions = {"Выход": ExitState, "Назад": PreviousState}


def get_choices(choices):
    choices["choose"].extend(list(base_actions.keys()))
    choices = Tools.get_choose_dict(choices)
    Tools.print_choose_dict(choices)
    return choices


class LoginState(State):
    def __init__(self):
        super().__init__()
        self.actions = dict.copy(base_actions)
        self.actions.update({"Ввести логин и пароль": MainState})

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        strategy = LoginStateStrategy()
        strategy.context = self.context
        self.context.next(self.actions[strategy.action(choices=choices)]())


class MainState(State):
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
        self.strategies_actions = dict(zip(self.actions.keys(), [None, None, {"Начать ввод": MainState}, {"Выбрать категорию": MainState}]))

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})
        Tools.print_choose_dict(choices)
        user_input = input()
        try:
            strategy = self.strategies[choices[user_input]]
            if not strategy:
                self.context.next(self.actions[user_input]())
            else:
                strategy = strategy()
                strategy.context = self.context
                _strategy_actions = dict.copy(base_actions)
                _strategy_actions.update(self.strategies_actions[choices[user_input]])
                _choices = Tools.get_choose_dict(data={"choose": list(_strategy_actions.keys())})
                self.context.next(self.actions[strategy.action(choices=_choices)]())
        except KeyError:
            pass





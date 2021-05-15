from file_manager import State
from states import MainState, ExitState
from strategies import LoginStrategy
from utils import Tools


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
        base_actions = {"Выход": ExitState}
        self.actions = dict.copy(base_actions)
        self.actions.update({"Ввести логин и пароль": MainState})

    def action(self):
        choices = Tools.get_choose_dict(data={"choose": list(self.actions.keys())})  # Составляем меню действий

        strategy = LoginStrategy()  # Выбираем стратегию
        strategy.context = self.context

        # Переходим на следущее состояние, которое нам вернет стратегия по меню.
        self.context.next(self.actions[strategy.action(choices=choices)]())

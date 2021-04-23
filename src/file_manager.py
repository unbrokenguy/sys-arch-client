from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from server_api import ServerApi


class State(ABC):
    """
    Abstract State Class
    """

    def __init__(self):
        self._context = None

    # Позволяет обращаться к вычисляемым полям (функиям) как к аттрибутам
    # не obj.getContext(), а просто ogj.context
    @property
    def context(self) -> FileManager:
        return self._context

    # не obj.setContext(context), а просто ogj.context = context
    @context.setter
    def context(self, context: FileManager) -> None:
        self._context = context

    @abstractmethod
    def action(self):
        pass

    def previous(self):
        self._context.previous()


class StateStrategy(ABC):
    """
    Abstract StrategyState Class
    """

    def __init__(self):
        self._context = None

    # Позволяет обращаться к вычисляемым полям (функиям) как к аттрибутам
    # не obj.getContext(), а просто ogj.context
    @property
    def context(self) -> FileManager:
        return self._context

    # не obj.setContext(context), а просто ogj.context = context
    @context.setter
    def context(self, context: FileManager) -> None:
        self._context = context

    @staticmethod
    def basic_action(**kwargs):
        """Returns State depends on user input"""
        choices = kwargs["choices"]
        user_input = kwargs["user_input"]
        try:
            return choices[user_input]
        except KeyError:
            return None

    @abstractmethod
    def action(self, **kwargs):
        """This is a request from StatePattern"""
        pass

    def previous(self):
        self._context.previous()


class FileManager:
    """
    Client application.
    Application has multiple states:
        LoginState, MainState, EntryState, PreviousState.
    """

    prev_state = None
    curr_state = None

    def __init__(self, state: State, url):
        self.storage_path = Path("files/")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.api = ServerApi(url)
        self.next(state)

    def next(self, state: State):
        """Set current state to a state
        Args:
            state: next State
        """
        state.context = self
        if self.prev_state.__class__.__name__ == "LoginState":
            self.prev_state = self.curr_state
        if state.__class__.__name__ != "PreviousState":
            self.prev_state = self.curr_state
        self.curr_state = state

    def previous(self):
        """
        Swaps previous state and current state
        """
        self.prev_state, self.curr_state = (
            self.curr_state,
            self.prev_state,
        )

    def execute(self):
        """This is a handle from StatePattern, handles the request"""
        self.curr_state.action()

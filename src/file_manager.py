from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from server_api import ServerApi


class State(ABC):
    def __init__(self):
        self._context = None

    @property
    def context(self) -> FileManager:
        return self._context

    @context.setter
    def context(self, context: FileManager) -> None:
        self._context = context

    @abstractmethod
    def action(self):
        pass

    def previous(self):
        self._context.previous()


class StateStrategy(ABC):
    def __init__(self):
        self._context = None

    @property
    def context(self) -> FileManager:
        return self._context

    @context.setter
    def context(self, context: FileManager) -> None:
        self._context = context

    @staticmethod
    def basic_action(**kwargs):
        choices = kwargs['choices']
        user_input = kwargs['user_input']
        try:
            return choices[user_input]
        except KeyError:
            return None

    @abstractmethod
    def action(self, **kwargs):
        pass

    def previous(self):
        self._context.previous()


class FileManager:
    prev_state = None
    curr_state = None

    def __init__(self, state: State, url, auth_url):
        self.storage_path = Path("files/")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.api = ServerApi(url, auth_url)
        self.next(state)

    def next(self, state: State):
        state.context = self
        if state.__class__.__name__ != "PreviousState":
            self.prev_state = self.curr_state
        self.curr_state = state

    def previous(self):
        self.prev_state, self.curr_state = (
            self.curr_state,
            self.prev_state,
        )

    def execute(self):
        self.curr_state.action()

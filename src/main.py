import os
from file_manager import FileManager
from states import LoginState, ExitState

if __name__ == "__main__":
    manager = FileManager(
        url=os.getenv("SERVER_URL"),
        state=LoginState(),
    )
    while type(manager.curr_state) != ExitState:
        manager.execute()
    manager.execute()

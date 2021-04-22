from file_manager import FileManager
from states import LoginState, ExitState

if __name__ == "__main__":
    manager = FileManager(
        url="http://127.0.0.1:8003/api",
        state=LoginState(),
    )
    while type(manager.curr_state) != ExitState:
        manager.execute()
    manager.execute()

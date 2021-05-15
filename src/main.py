import os
from file_manager import FileManager
from states import LoginState, ExitState


if __name__ == "__main__":
    manager = FileManager(  # Initialize FileManager application.
        url=os.getenv("SERVER_URL", "https://sadmadsoul.dev/api"),
        state=LoginState(),
    )
    #  Loop through FileManager states while current state is not ExitState.
    while not isinstance(manager.curr_state, ExitState):
        manager.execute()
    manager.execute()

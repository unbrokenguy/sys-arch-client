from file_manager import State


class ExitState(State):
    """
    State handle exit from our Application.
    """

    def action(self):
        """Exit from program."""
        exit()

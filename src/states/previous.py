from file_manager import State


class PreviousState(State):
    """
    State handle go to previous State in our Application.
    """

    def action(self):
        """
        Set FileManager state to previous State.
        """
        self.context.next(self.context.prev_state)

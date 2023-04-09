from consts.states import States

class StateMachine():
    def __init__(self) -> None:
        self._state = States.PLAYING

    @property
    def state(self):
        return self._state
    
    def pause(self):
        self._state = States.PAUSED


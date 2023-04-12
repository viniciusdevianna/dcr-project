from .consts.states import States

class StateMachine():
    def __init__(self) -> None:
        self._state = States.LOADING

    @property
    def state(self):
        return self._state
    
    def draw_phase(self):
        self._state = States.DRAWING

    def summon_phase(self):
        self._state = States.SUMMONING

    def battle_phase(self):
        self._state = States.BATTLING
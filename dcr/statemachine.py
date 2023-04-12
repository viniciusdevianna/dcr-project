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

    def prepare_battle_phase(self):
        self._state = States.PREPARING_BATTLE

    def resume_battle_phase(self):
        self._state = States.BATTLING

    def end_battle_phase(self):
        self._state = States.ENDING_BATTLE

    def declare_win(self):
        self._state = States.WINNING

    def declare_loss(self):
        self._state = States.LOSING
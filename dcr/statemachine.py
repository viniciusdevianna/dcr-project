from .consts.states import States

class StateMachine():
    def __init__(self) -> None:
        self._state = States.LOADING
        self._battle_cycle = (
            States.DRAWING,
            States.SUMMONING,
            States.PREPARING_BATTLE,
            States.BATTLING,
            States.ENDING_BATTLE,
            States.IDLE,
            States.AFTER_BATTLE,
        )
        self._actual_stage = -1

    @property
    def state(self):
        return self._state
    
    def pause(self):
        self._state = States.IDLE
    
    def next_battle_stage(self):
        if self._actual_stage < len(self._battle_cycle) - 1:
            self._actual_stage += 1            
        else:
            self._actual_stage = 0

        self._state = self._battle_cycle[self._actual_stage]

    def declare_win(self):
        self._state = States.WINNING

    def declare_loss(self):
        self._state = States.LOSING

    def declare_draw(self):
        self._state = States.NO_WINNERS
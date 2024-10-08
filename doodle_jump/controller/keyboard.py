from datetime import timedelta
from doodle_jump.controller import Controller

class Keyboard(Controller):
    def update(self, delta: timedelta) -> None:
        raise NotImplementedError

    def horizontal(self) -> float:
        raise NotImplementedError

    def shoot(self) -> bool:
        raise NotImplementedError

from doodle_jump.controller import Controller
from doodle_jump.game import FrameInfo, Game


class Gpio(Controller):
    """
    Gpio controller class.
    """

    def update(self, info: FrameInfo, game: Game) -> None:
        raise NotImplementedError()

    def horizontal(self) -> float:
        raise NotImplementedError()

    def shoot(self) -> bool:
        raise NotImplementedError()

from pygame import K_LEFT, K_RIGHT, K_SPACE, KEYDOWN, KEYUP
from doodle_jump.controller import Controller

from doodle_jump.game import FrameInfo, Game


class Keyboard(Controller):
    """
    The controller that uses the keyboard as input

    The left and right keys are used to move the horizontal position
    The space key is used to shoot
    """

    __shoot: bool

    __left_pressed: bool
    __right_pressed: bool

    HORIZONTAL_SPEED = 150

    def __init__(self):
        self.__horizontal = 0

        self.__shoot = False

        self.__left_pressed = False
        self.__right_pressed = False

    def update(self, info: FrameInfo, game: Game) -> None:
        self.__shoot = False

        for event in info.events:
            if not event.type == KEYDOWN and not event.type == KEYUP:
                continue

            if event.key == K_LEFT:
                self.__left_pressed = event.type == KEYDOWN
            elif event.key == K_RIGHT:
                self.__right_pressed = event.type == KEYDOWN

            if event.key == K_SPACE:
                self.__shoot = event.type == KEYDOWN

        match self.__left_pressed, self.__right_pressed:
            case (True, False):
                self.__horizontal = (
                    -Keyboard.HORIZONTAL_SPEED * info.time.total_seconds()
                )
            case (False, True):
                self.__horizontal = (
                    Keyboard.HORIZONTAL_SPEED * info.time.total_seconds()
                )
            case _:
                self.__horizontal = 0

    def horizontal(self) -> float:
        return self.__horizontal

    def shoot(self) -> bool:
        return self.__shoot

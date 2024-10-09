from pygame import Surface
from doodle_jump.game import Actor, FrameInfo, Game
from doodle_jump.math.rectangle import Rectangle
from doodle_jump.render_target import RenderTarget
from doodle_jump.math.vector2 import Vector2


class Platform(Actor):
    __position: Vector2
    __image: Surface

    def __init__(self, image: Surface, position: Vector2) -> None:
        super().__init__()

        self.__position = position
        self.__image = image

    def update(self, info: FrameInfo, game: Game) -> None:

        pass

    def render(
        self, info: FrameInfo, render_target: RenderTarget, game: Game
    ) -> None:
        render_target.blit(
            self.__image,
            self.__position,
        )

    @property
    def hitbox(self) -> Rectangle:
        return Rectangle(
            self.__position.x,
            self.__position.y,
            self.__image.get_width(),
            self.__image.get_height(),
        )

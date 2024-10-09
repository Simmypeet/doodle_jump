from doodle_jump.actor.platform import Platform
from doodle_jump.controller import Controller
from doodle_jump.controller.keyboard import Keyboard
from doodle_jump.game import Actor, FrameInfo, Game, RenderTarget

from pygame import Surface, Vector2


from doodle_jump.math.rectangle import Rectangle


class Player(Actor):
    __controller: Controller
    __position: Vector2
    __image: Surface
    __speed_y: float

    SPEED_Y = 250
    GRAVITY = 100

    def __init__(self, image: Surface):
        super().__init__()

        self.__controller = Keyboard()
        self.__position = Vector2(0, 0)
        self.__image = image
        self.__speed_y = Player.SPEED_Y

    def update(self, info: FrameInfo, game: Game) -> None:
        self.__controller.update(info, game)

        self.__position.x += self.__controller.horizontal()
        self.__position.y -= self.__speed_y * info.time.total_seconds()

        self.__speed_y -= Player.GRAVITY * info.time.total_seconds()

        # wrap around the screen
        display_half_width = game.surface.get_width() / 2
        if self.__position.x > display_half_width:
            self.__position.x = -display_half_width - self.__image.get_width()
        elif (
            self.__position.x + self.__image.get_width() < -display_half_width
        ):
            self.__position.x = display_half_width

        # detect hit with platform
        if self.__speed_y < 0:
            for platform in game.scene.get_actors_of_instance(Platform):
                if self.hitbox.collides(platform.hitbox):
                    self.__speed_y = Player.SPEED_Y

    def render(
        self, info: FrameInfo, render_target: RenderTarget, game: Game
    ) -> None:
        render_target.blit(
            self.__image,
            Vector2(
                self.__position.x,
                self.__position.y,
            ),
        )

    @property
    def position(self) -> Vector2:
        return self.__position

    @property
    def hitbox(self) -> Rectangle:
        return Rectangle(
            self.__position.x,
            self.__position.y,
            self.__image.get_width(),
            self.__image.get_height(),
        )

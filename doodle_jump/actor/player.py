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

    # __image_list_right: list[Surface]
    # __image_list_left: list[Surface]
    # __is_moving_right: bool
    # __is_moving_left: bool

    # __fame_index: int
    # __fame_timer: float


    SPEED_Y = 500
    GRAVITY = 800

    def __init__(self, image: Surface):
    # def __init__(self, image_list_right: list[Surface], image_list_left: list[Surface]):
        super().__init__()

        self.__controller = Keyboard()
        self.__position = Vector2(0, 0)
        self.__image = image
        self.__speed_y = Player.SPEED_Y

        # self.__image_list_right = image_list_right
        # self.__image_list_left = image_list_left
        # self.__is_moving_right = False;
        # self.__is_moving_left = False;
        # self.__fame_index = 0
        # self.__fame_timer = 0



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
                    platform.notify_collision()

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

    # @property
    # def current_image_list(self)-> list[Surface]:
    #     if self.__is_moving_right:
    #         return self.__image_list_right
    #     return self.__image_list_left
    #     # raise NotImplementedError()
    
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
    
    # @property
    # def shotting(self) -> bool:
    #     return self.__controller.shotting()


    # hit the ground

    # hit the enemy

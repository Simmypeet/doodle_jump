from pygame import Surface, Vector2
import pygame
from doodle_jump.actor.platform import Platform
from doodle_jump.actor.player import Player
from doodle_jump.camera import Camera
from doodle_jump.game import FrameInfo, Game, Scene
from doodle_jump.render_target import RenderTarget


class Main(Scene):
    """The main scene of the game."""

    __playform_image: Surface
    __player_image: Surface

    __player: Player

    __camera: Camera
    __y_camera: float

    def __init__(self, game: Game) -> None:
        super().__init__()

        self.__player_image = pygame.transform.scale_by(
            pygame.image.load("resource/Players/bunny1_jump.png"), 0.5
        )
        self.__platform_image = pygame.transform.scale_by(
            pygame.image.load("resource/Environment/ground_grass.png"), 0.5
        )

        self.__player = Player(self.__player_image)

        platform = Platform(self.__platform_image, Vector2(0, 0))
        self.add_actor(platform)

        platform = Platform(self.__platform_image, Vector2(-100, -100))
        self.add_actor(platform)

        self.add_actor(self.__player)

        self.__camera = Camera(Vector2(0, 0), 0, 0)
        self.__y_camera = (
            -game.surface.get_height() / 2 + self.__platform_image.get_height()
        )

    def update(self, info: FrameInfo, game: Game) -> None:
        super().update(info, game)

        player_hitbox = self.__player.hitbox
        self.__y_camera = min(
            self.__y_camera,
            player_hitbox.top
            + player_hitbox.height / 2
            + game.surface.get_height() / 3,
        )

    def render(self, info: FrameInfo, game: Game) -> None:
        self.__camera.position = Vector2(0, self.__y_camera)

        self.__camera.width = game.surface.get_width()
        self.__camera.height = game.surface.get_height()

        self.render_actors(
            info, RenderTarget(game.surface, self.__camera), game
        )

import random
from pygame import Surface, Vector2
import pygame
from doodle_jump.actor.platform import Platform
from doodle_jump.actor.player import Player
from doodle_jump.camera import Camera
from doodle_jump.game import FrameInfo, Game, Scene
from doodle_jump.render_target import RenderTarget

from doodle_jump.actor.enemy import Enemy, gen_enemies


class Main(Scene):
    """The main scene of the game."""

    __platform_image: Surface
    __player_image: Surface

    __player: Player

    __camera: Camera
    __y_camera: float
    __current_level: float

    STEP = 150
    ENEMY_RATE = 0.3

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

        self.add_actor(self.__player)

        self.__current_level = -Main.STEP
        self.__camera = Camera(Vector2(0, 0), 0, 0)
        self.__y_camera = (
            -game.surface.get_height() / 2 + self.__platform_image.get_height()
        )

    def update(self, info: FrameInfo, game: Game) -> None:
        player_hitbox = self.__player.hitbox
        self.__y_camera = min(
            self.__y_camera,
            player_hitbox.top
            + player_hitbox.height / 2
            - (game.surface.get_height() / 6),
        )

        self.__camera.position = Vector2(0, self.__y_camera)

        camera_world_bounds = self.__camera.world_bounds()

        # generate platforms until it reaches the camera's top
        while (
            self.__current_level + self.__platform_image.get_height()
            > camera_world_bounds.top
        ):
            x_position = random.randint(
                int(camera_world_bounds.left),
                int(camera_world_bounds.width + camera_world_bounds.left),
            ) - (self.__platform_image.get_width() / 2)

            platform = Platform(
                self.__platform_image,
                Vector2(
                    x_position,
                    self.__current_level,
                ),
            )
            self.add_actor(platform)

            if random.uniform(0, 1) < Main.ENEMY_RATE:
                enemy = gen_enemies(
                    x_position,
                    self.__current_level - 50,
                )
                self.add_actor(enemy)

            self.__current_level -= Main.STEP

        # delete platforms that are not visible
        for platform in self.get_actors_of_instance(Platform):
            if (
                platform.hitbox.top
                > camera_world_bounds.top + camera_world_bounds.height
            ):
                self.remove_actor(platform)

        # delete enemies that are not visible
        for enemy in self.get_actors_of_instance(Enemy):
            if (
                enemy.position.y
                > camera_world_bounds.top + camera_world_bounds.height
            ):
                self.remove_actor(enemy)

        super().update(info, game)

    def render(self, info: FrameInfo, game: Game) -> None:
        self.__camera.position = Vector2(0, self.__y_camera)

        self.__camera.width = game.surface.get_width()
        self.__camera.height = game.surface.get_height()

        self.render_actors(
            info, RenderTarget(game.surface, self.__camera), game
        )

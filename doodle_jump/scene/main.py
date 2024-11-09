from pygame import Surface, Vector2
from pygame.font import Font

from doodle_jump.actor.platform import Platform
from doodle_jump.actor.player import Player
from doodle_jump.camera import Camera
from doodle_jump.controller import Controller
from doodle_jump.controller.keyboard import Keyboard
from doodle_jump.game import FrameInfo, Game, Scene
from doodle_jump.render_target import RenderTarget

from doodle_jump.actor.enemy import Enemy, gen_enemies

import pygame
import random


class Main(Scene):
    """The main scene of the game."""

    __platform_image: Surface
    __player_image: Surface
    __font: Font
    __score_text: Surface
    __controller: Controller

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

        # FIXME: change the controller here
        self.__controller = Keyboard()

        self.__font = Font("resource/Font/Habbo.ttf", 30)
        self.__player = Player(self.__player_image, self.__controller)

        platform = Platform(self.__platform_image, Vector2(0, 0))

        self.add_actor(platform)
        self.add_actor(self.__player)

        self.__current_level = -Main.STEP
        self.__camera = Camera(Vector2(0, 0), 0, 0)
        self.__y_camera = (
            -game.surface.get_height() / 2 + self.__platform_image.get_height()
        )

    def update(self, info: FrameInfo, game: Game) -> None:
        self.__controller.update(info, game)

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
            self.__score_text = self.__font.render(
                f"Score: {int(-self.__current_level)}",
                False,
                (255, 255, 255),
            )

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

        # check if the player out of the screen / game over
        if self.__player.position.y > (
            camera_world_bounds.top + camera_world_bounds.height + 1000
        ):
            game.change_scene(
                GameOver(
                    self.__font, int(-self.__current_level), self.__controller
                )
            )

        super().update(info, game)

    def render(self, info: FrameInfo, game: Game) -> None:
        self.__camera.position = Vector2(0, self.__y_camera)

        self.__camera.width = game.surface.get_width()
        self.__camera.height = game.surface.get_height()

        self.render_actors(
            info, RenderTarget(game.surface, self.__camera), game
        )

        game.surface.blit(self.__score_text, (10, 10))


class GameOver(Scene):
    __score_text: Surface
    __restart_text: Surface
    __controller: Controller

    def __init__(self, font: Font, score: int, controller: Controller) -> None:
        super().__init__()

        self.__score_text = font.render(
            f"Score: {score}",
            False,
            (255, 255, 255),
        )

        self.__restart_text = font.render(
            "Shoot to Restart",
            False,
            (255, 255, 255),
        )

        self.__controller = controller

    def update(self, info: FrameInfo, game: Game) -> None:
        super().update(info, game)

        self.__controller.update(info, game)

        if self.__controller.shoot():
            game.change_scene(Main(game))

    def render(self, info: FrameInfo, game: Game) -> None:
        half_x = game.surface.get_width() / 2
        half_y = game.surface.get_height() / 2

        game.surface.blit(
            self.__score_text,
            (
                half_x - self.__score_text.get_width() / 2,
                half_y - self.__score_text.get_height(),
            ),
        )

        game.surface.blit(
            self.__restart_text,
            (
                half_x - self.__restart_text.get_width() / 2,
                half_y,
            ),
        )

from doodle_jump.actor.platform import Platform
from doodle_jump.controller import Controller
from doodle_jump.controller.keyboard import Keyboard
from doodle_jump.game import Actor, FrameInfo, Game, RenderTarget
from doodle_jump.actor.enemy import Enemy

import pygame
from pygame import Surface, Vector2


from doodle_jump.math.rectangle import Rectangle


class Player(Actor):
    __controller: Controller
    __position: Vector2
    __image: Surface
    __speed_y: float

    __last_direction: int

    SPEED_Y = 500
    GRAVITY = 800

    def __init__(self, image: Surface):
        super().__init__()

        self.__controller = Keyboard()
        self.__position = Vector2(0, 0)
        self.__image = image
        self.__speed_y = Player.SPEED_Y

        self.__last_direction = -1

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
        player_hitbox = self.hitbox
        for platform in game.scene.get_actors_of_instance(Platform):
            platform_hitbox = platform.hitbox

            if (
                player_hitbox.collides(platform_hitbox)
                and self.__speed_y < 0
                and platform.player_was_on_top
            ):
                self.__speed_y = Player.SPEED_Y
                platform.notify_collision()

            platform.player_was_on_top = (
                player_hitbox.top + player_hitbox.height < platform_hitbox.top
            )

        # bullet
        horizontal_input = self.__controller.horizontal()
        if horizontal_input > 0:
            self.__last_direction = 1
        elif horizontal_input < 0:
            self.__last_direction = -1
        else:
            self.__last_direction = self.__last_direction

        self.__position.x += horizontal_input
        self.__position.y -= self.__speed_y * info.time.total_seconds()

        if self.__controller.shoot():
            bullet = Bullet(
                Vector2(
                    self.__position.x + (self.__image.get_width() // 2),
                    self.__position.y,
                ),
                "resource/Particles/portal_yellowParticle.png",
                self.__last_direction,
            )
            game.scene.add_actor(bullet)

        # die
        for enemy in game.scene.get_actors_of_instance(Enemy):
            if self.hitbox.collides(enemy.hitbox):
                # game.stop()
                pass

        if self.__position.y > game.surface.get_height() / 2 + 200:
            game.stop()

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


class Bullet(Actor):
    def __init__(self, position: Vector2, image_path: str, direction: int):
        super().__init__()
        self.__position = position
        self.__speed = 400
        self.__direction = direction
        self.__image = pygame.image.load(image_path)
        self.__image = pygame.transform.scale(self.__image, (10, 5))

    def update(self, info: FrameInfo, game: Game) -> None:
        self.__position.x += (
            self.__speed * self.__direction * info.time.total_seconds()
        )

        screen_width = game.surface.get_width()

        if self.__position.x + self.__image.get_width() > screen_width - 230:
            game.scene.remove_actor(self)
        if self.__position.x < -280:
            game.scene.remove_actor(self)

        for enemy in game.scene.get_actors_of_instance(Enemy):
            if self.hitbox.collides(enemy.hitbox):
                game.scene.remove_actor(self)
                game.scene.remove_actor(enemy)

    def render(
        self, info: FrameInfo, render_target: RenderTarget, game: Game
    ) -> None:
        render_target.blit(self.__image, self.__position)

    @property
    def hitbox(self) -> Rectangle:
        return Rectangle(
            self.__position.x,
            self.__position.y,
            self.__image.get_width(),
            self.__image.get_height(),
        )

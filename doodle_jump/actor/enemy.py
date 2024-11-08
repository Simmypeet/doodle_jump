from doodle_jump.game import Actor, FrameInfo, Game, RenderTarget
from pygame import Surface, Vector2
from doodle_jump.math.rectangle import Rectangle

import pygame
import random


class Enemy(Actor):
    __speed_x: float
    __position: Vector2
    __image: Surface
    __direction: int

    SPEED_X = 150

    def __init__(self, image: Surface, position: Vector2) -> None:
        super().__init__()

        self.__position = position
        self.__image = image
        self.__speed_x = Enemy.SPEED_X
        self.__direction = 1

    def update(self, info: FrameInfo, game: Game) -> None:

        self.__position.x += (
            self.__speed_x * self.__direction * info.time.total_seconds()
        )

        display_half_width = game.surface.get_width() / 2
        if self.__position.x > display_half_width and self.__direction == 1:
            self.__direction = -1
        elif (
            self.__position.x + self.__image.get_width() < -display_half_width
            and self.__direction == -1
        ):
            self.__direction = 1

    def render(
        self, info: FrameInfo, render_target: RenderTarget, game: Game
    ) -> None:
        render_target.blit(self.__image, self.__position)

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
def gen_enemies(number: int)->list[Enemy]:
    notoverlap = -100
    enemies = ["resource/Enemies/flyMan_fly.png", "resource/Enemies/spikeBall_2.png"
               ,"resource/Enemies/spikeMan_stand.png","resource/Enemies/cloud.png",
               "resource/Enemies/springMan_stand.png","resource/Enemies/sun1.png",
               "resource/Enemies/wingMan1.png"]
    generated_enemies = []  

    for _ in range(number):
        rand_idx = random.randint(0, len(enemies) - 1)
        image = pygame.transform.scale(
            pygame.image.load(enemies[rand_idx]), (50, 50) 
        )
        position = random.randrange(80, 200)
        notoverlap += position 
        start_position = Vector2(-400, -350 - notoverlap)#use for resize x and y

        enemy = Enemy(image, start_position) 
        generated_enemies.append(enemy) 

    return generated_enemies 



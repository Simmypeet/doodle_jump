from doodle_jump.game import Actor, FrameInfo, Game, RenderTarget
from pygame import Surface, Vector2
import pygame
import random  
from doodle_jump.math.rectangle import Rectangle
from time import sleep

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
    
        self.__position.x += self.__speed_x * self.__direction * info.time.total_seconds()


        screen_width = game.surface.get_width()

        if self.__position.x + self.__image.get_width() > screen_width - 230:
            self.__direction = -1  
        elif self.__position.x < -280:
            self.__direction = 1  

    def render(self, info: FrameInfo, render_target: RenderTarget, game: Game) -> None:
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
def gen_enemies(number: int):
    notoverlap = -100
    enemies = ["resource/Enemies/flyMan_fly.png", "resource/Enemies/spikeBall_2.png"]
    generated_enemies = []  

    for _ in range(number):
        rand_idx = random.randint(0, len(enemies) - 1)
        image = pygame.transform.scale(
            pygame.image.load(enemies[rand_idx]), (50, 50) 
        )
        position = random.randrange(80, 200)
        notoverlap += position  # Increase the Y offset to prevent overlap
        start_position = Vector2(0, -100 - notoverlap)

        enemy = Enemy(image, start_position)  # Create the enemy instance
        generated_enemies.append(enemy)  # Add to the list of enemies

    return generated_enemies  # Return the list of generated enemies



def generate_enemies(image: Surface, num_enemies: int, screen_width: int) -> list[Enemy]:
    enemies = []
    min_distance_x = 100  # Minimum distance between enemies on the x-axis
    current_x = 0  # Starting x position

    for _ in range(num_enemies):
        y_position = random.randint(50, 300)

        current_x += random.randint(min_distance_x, min_distance_x + 150)

        if current_x > screen_width - 230:
            current_x = current_x % screen_width

        enemy = Enemy(image, Vector2(current_x, y_position))
        enemies.append(enemy)

    return enemies


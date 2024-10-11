# from doodle_jump.game import Actor, FrameInfo, Game, RenderTarget
# from pygame import Surface, Vector2
# import random  # For random y position generation
# from doodle_jump.math.rectangle import Rectangle

# class Enemy(Actor):
#     __speed_x: float
#     __position: Vector2
#     __image: Surface
#     __direction: int  # 1 for moving right, -1 for moving left

#     SPEED_X = 150  # Horizontal speed

#     def __init__(self, image: Surface, position: Vector2) -> None:
#         super().__init__()

#         self.__position = position  # Enemy's position
#         self.__image = image
#         self.__speed_x = Enemy.SPEED_X  # Speed in the x direction
#         self.__direction = 1  # Start by moving to the right

#     def update(self, info: FrameInfo, game: Game) -> None:
#         # Horizontal movement
#         self.__position.x += self.__speed_x * self.__direction * info.time.total_seconds()

#         # Bounce off screen edges
#         screen_width = game.surface.get_width()

#         if self.__position.x + self.__image.get_width() > screen_width -230:
#             self.__direction = -1  # Move left
#         elif self.__position.x < -280:
#             self.__direction = 1  # Move right

#     def render(self, info: FrameInfo, render_target: RenderTarget, game: Game) -> None:
#         render_target.blit(self.__image, self.__position)

#     @property
#     def position(self) -> Vector2:
#         return self.__position

#     @property
#     def hitbox(self) -> Rectangle:
#         return Rectangle(
#             self.__position.x,
#             self.__position.y,
#             self.__image.get_width(),
#             self.__image.get_height(),
#         )

# # # Function to generate enemies at random y-positions
# # def generate_enemies(image: Surface, num_enemies: int, screen_width: int) -> list[Enemy]:
# #     enemies = []
# #     for _ in range(num_enemies):
# #         x_position = random.randint(0, screen_width - image.get_width())
# #         y_position = random.randint(50, 400)  # Random y between 50 and 400
# #         enemy = Enemy(image, Vector2(x_position, y_position))
# #         enemies.append(enemy)
# #     return enemies
# # Function to generate enemies with different x and y positions
# def generate_enemies(image: Surface, num_enemies: int, screen_width: int) -> list[Enemy]:
#     enemies = []
#     min_distance_x = 100  # Minimum distance between enemies on the x-axis
#     current_x = 0  # Starting x position

#     for _ in range(num_enemies):
#         # Generate random y position between a range, e.g., 50 to 400
#         y_position = random.randint(50, 400)

#         # Ensure enemies are spaced out along the x-axis
#         current_x += random.randint(min_distance_x, min_distance_x + 150)

#         # Wrap around if the x position exceeds the screen width
#         if current_x > screen_width - 230:
#             current_x = current_x % screen_width

#         # Create a new enemy at the given x and y position
#         enemy = Enemy(image, Vector2(current_x, y_position))
#         enemies.append(enemy)

#     return enemies

from doodle_jump.game import Actor, FrameInfo, Game, RenderTarget
from pygame import Surface, Vector2
import random  # For random y position generation
from doodle_jump.math.rectangle import Rectangle

class Enemy(Actor):
    __speed_x: float
    __position: Vector2
    __image: Surface
    __direction: int  # 1 for moving right, -1 for moving left

    SPEED_X = 150  # Horizontal speed

    def __init__(self, image: Surface, position: Vector2) -> None:
        super().__init__()

        self.__position = position  # Enemy's position
        self.__image = image
        self.__speed_x = Enemy.SPEED_X  # Speed in the x direction
        self.__direction = 1  # Start by moving to the right

    def update(self, info: FrameInfo, game: Game) -> None:
        # Horizontal movement
        self.__position.x += self.__speed_x * self.__direction * info.time.total_seconds()

        # Bounce off screen edges
        screen_width = game.surface.get_width()

        if self.__position.x + self.__image.get_width() > screen_width - 230:
            self.__direction = -1  # Move left
        elif self.__position.x < -280:
            self.__direction = 1  # Move right

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

def generate_enemies(image: Surface, num_enemies: int, screen_width: int) -> list[Enemy]:
    enemies = []
    min_distance_x = 100  # Minimum distance between enemies on the x-axis
    current_x = 0  # Starting x position

    for _ in range(num_enemies):
        # Generate random y position between a range, e.g., 50 to 400
        y_position = random.randint(50, 400)

        # Ensure enemies are spaced out along the x-axis
        current_x += random.randint(min_distance_x, min_distance_x + 150)

        # Wrap around if the x position exceeds the screen width
        if current_x > screen_width - 230:
            current_x = current_x % screen_width

        # Create a new enemy at the given x and y position
        enemy = Enemy(image, Vector2(current_x, y_position))
        enemies.append(enemy)

    return enemies

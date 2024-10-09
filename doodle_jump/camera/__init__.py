from dataclasses import dataclass

from pygame import Vector2

from doodle_jump.math.rectangle import Rectangle


@dataclass
class Camera:
    position: Vector2
    """The center position of the camera."""

    width: int
    """The width of the camera."""

    height: int
    """The height of the camera."""

    def to_view(self, position: Vector2) -> Vector2:
        """Change the world position to the view position."""

        return Vector2(
            self.to_view_x(position.x),
            self.to_view_y(position.y),
        )

    def world_bounds(self) -> Rectangle:
        """Get the world bounds of the camera."""

        return Rectangle(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width,
            self.height,
        )

    def to_view_x(self, x: float) -> float:
        """Change the world x position to the view x position."""

        return x - self.position.x + self.width / 2

    def to_view_y(self, y: float) -> float:
        """Change the world y position to the view y position."""

        return y - self.position.y + self.height / 2

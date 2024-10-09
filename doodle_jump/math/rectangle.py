from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rectangle:
    left: float
    top: float
    width: float
    height: float

    def collides(self, rect2: Rectangle) -> bool:
        """Check if this rectangle collides with another rectangle."""

        return (
            self.left < rect2.left + rect2.width
            and self.left + self.width > rect2.left
            and self.top < rect2.top + rect2.height
            and self.top + self.height > rect2.top
        )

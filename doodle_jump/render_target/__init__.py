from dataclasses import dataclass

from pygame import Rect, Surface
import pygame


from doodle_jump.camera import Camera
from doodle_jump.math.rectangle import Rectangle
from doodle_jump.math.vector2 import Vector2


@dataclass
class RenderTarget:
    surface: Surface
    camera: Camera | None

    def blit(
        self,
        source: Surface,
        dest: Vector2 | Rectangle,
        source_rect: Rectangle | None = None,
        special_flags: int = 0,
    ) -> None:
        """Blit the source surface to the destination."""

        match dest:
            case Vector2():
                dest_x = dest.x
                dest_y = dest.y

                dest_width = source.get_width()
                dest_height = source.get_height()

            case Rectangle():
                dest_x = dest.left
                dest_y = dest.top

                dest_width = dest.width
                dest_height = dest.height

        scale_x = dest_width / source.get_width()
        scale_y = dest_height / source.get_height()

        if self.camera is not None:
            dest_x = self.camera.to_view_x(dest_x)
            dest_y = self.camera.to_view_y(dest_y)

        if source_rect is not None:
            final_source_rect = Rect(
                source_rect.left * scale_x,
                source_rect.top * scale_y,
                source_rect.width * scale_x,
                source_rect.height * scale_y,
            )
        else:
            final_source_rect = None

        if (
            dest_width != source.get_width()
            or dest_height != source.get_height()
        ):
            source = pygame.transform.scale(
                source,
                (dest_width, dest_height),
            )

        self.surface.blit(
            source,
            (dest_x, dest_y),
            final_source_rect,
            special_flags,
        )

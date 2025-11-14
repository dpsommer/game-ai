import pygame

from gameai import config

from .collision import CollidableObject2D


class Surface2D(CollidableObject2D):
    """Game surface such as platform or walls

    Args:
        settings (SurfaceOptions): configuration options for the surface
    """

    def __init__(self, settings: config.SurfaceSettings):
        super().__init__(settings)

    def update(self, *, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

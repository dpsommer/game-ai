import abc
from typing import List, Protocol, Tuple, TypeVar

import pygame

from gameai import config
from gameai.sprites import Character2D
from gameai.types import SpriteSupportsGroup


class Camera(metaclass=abc.ABCMeta):

    pos: pygame.Vector2

    @abc.abstractmethod
    def update(self):
        pass


class Camera2D(Camera):

    def __init__(self, opts: config.Camera2DOptions, follow: Character2D):
        self.follow = follow
        x, y = self._follow_centered()
        self.pos = pygame.Vector2(x, y)

    def _follow_centered(self) -> Tuple[float, float]:
        w, h = pygame.display.get_window_size()
        x = -self.follow.rect.centerx + (w / 2)
        y = -self.follow.rect.centery + (h / 2)
        return x, y

    def update(self):
        # rect.center is the draw point relative to the screen;
        # we need to follow, ie. self.x should trend towards
        # follow.rect.centerx + window_width / 2
        x, y = self._follow_centered()
        self.pos += (pygame.Vector2((x, y)) - self.pos) * 0.05
        # TODO: clamp x/y values to background bounds


class SpriteSupportsCamera(SpriteSupportsGroup, Protocol):
    source_rect: pygame.Rect


T = TypeVar("T", bound=SpriteSupportsCamera)


class CameraGroup(pygame.sprite.AbstractGroup[T]):

    def __init__(
        self, *sprites: T, camera: Camera, background: pygame.Surface | None = None
    ):
        super().__init__(*sprites)
        self.camera = camera
        self.background = background

    def draw(
        self,
        surface: pygame.Surface,
        bgsurf: pygame.Surface | None = None,
        special_flags: int = 0,
    ) -> List[pygame.Rect]:
        sprites: List[T] = self.sprites()
        bgsurf = self.background or bgsurf
        if bgsurf is not None:
            surface.blit(bgsurf, (0, 0))

        sprite_blits = []
        for spr in sprites:
            with_camera_offset = spr.rect.move(self.camera.pos)
            sprite_blits.append(
                (spr.image, with_camera_offset, spr.source_rect, special_flags)
            )

        blits = surface.blits(sprite_blits)
        if blits is not None:
            self.spritedict.update(zip(sprites, blits, strict=False))
            return blits
        return []

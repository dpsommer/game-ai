import dataclasses
from typing import List, Protocol

import pygame

from gameai import config
from gameai.types import Coordinate


class SupportsCollision(Protocol):
    image: pygame.Surface
    rect: pygame.Rect
    collision_box: config.CollisionBox
    # last_pos is the topleft coord of the previous position of the object
    last_pos: Coordinate


@dataclasses.dataclass
class Collision2D:
    # x and y represent translation coordinates for the colliding
    # object to move so that it is in bounds
    x: int = 0
    y: int = 0

    top: SupportsCollision | None = None
    left: SupportsCollision | None = None
    right: SupportsCollision | None = None
    bottom: SupportsCollision | None = None

    @staticmethod
    def between(
        target: SupportsCollision, objects: List[SupportsCollision]
    ) -> "Collision2D":
        coll = Collision2D()
        last_x, last_y = target.last_pos
        collisions = target.rect.collideobjectsall(objects, key=lambda o: o.rect)

        for collision in collisions:
            # check that both objects collide in the direction of collision
            # AND the object is passing through the collision box
            # AND the direction of movement is towards the collision point
            if (
                target.collision_box.top
                and collision.collision_box.bottom
                and target.rect.top <= collision.rect.bottom
                and target.rect.bottom > collision.rect.bottom
                and last_y >= collision.rect.bottom
            ):
                coll.y = collision.rect.bottom - target.rect.top
                coll.top = collision
            if (
                target.collision_box.left
                and collision.collision_box.right
                and target.rect.left <= collision.rect.right
                and target.rect.right > collision.rect.right
                and last_x >= collision.rect.right
            ):
                coll.x = collision.rect.right - target.rect.left
                coll.left = collision
            if (
                target.collision_box.right
                and collision.collision_box.left
                and target.rect.right >= collision.rect.left
                and target.rect.left < collision.rect.left
                and last_x + target.rect.width <= collision.rect.left
            ):
                coll.x = collision.rect.left - target.rect.right
                coll.right = collision
            if (
                target.collision_box.bottom
                and collision.collision_box.top
                and target.rect.bottom >= collision.rect.top
                and target.rect.top < collision.rect.top
                and last_y + target.rect.height <= collision.rect.top
            ):
                coll.y = collision.rect.top - target.rect.bottom
                coll.bottom = collision

        return coll


class CollidableObject2D(config.Loadable, pygame.sprite.DirtySprite):

    def __init__(self, settings: config.CollidableSettings):
        super().__init__()
        self.settings = settings

        self._layer = settings.layer
        image_size = (settings.width, settings.height)
        self.image = settings.image if settings.image else pygame.Surface(image_size)

        self.collision_box = settings.collision_box

        self.rect = self.image.get_rect()
        self.last_pos: Coordinate = self.rect.topleft
        self._reset()

    def _reset(self):
        x, y = self.settings.topleft
        self.source_rect = self.image.get_bounding_rect()
        self.rect.update((x, y), self.source_rect.size)
        self.last_pos: Coordinate = self.rect.topleft

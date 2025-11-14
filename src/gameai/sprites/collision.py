import abc
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

    @staticmethod
    def between(
        target: SupportsCollision, objects: List[SupportsCollision]
    ) -> "Collision2D":
        coll = Collision2D()
        last_x, last_y = target.last_pos
        target_box = target.collision_box.rect
        collisions = target_box.collideobjectsall(
            objects, key=lambda o: o.collision_box.rect
        )

        for collision in collisions:
            box = collision.collision_box.rect
            # check that both objects collide in the direction of collision
            # AND the object is passing through the collision box
            # AND the direction of movement is towards the collision point
            if (
                target.collision_box.top
                and collision.collision_box.bottom
                and target_box.top <= box.bottom
                and target_box.bottom > box.bottom
                and last_y >= box.bottom
            ):
                coll.y = box.bottom - target_box.top
            if (
                target.collision_box.left
                and collision.collision_box.right
                and target_box.left <= box.right
                and target_box.right > box.right
                and last_x >= box.right
            ):
                coll.x = box.right - target_box.left
            if (
                target.collision_box.right
                and collision.collision_box.left
                and target_box.right >= box.left
                and target_box.left < box.left
                and last_x + target_box.width <= box.left
            ):
                coll.x = box.left - target_box.right
            if (
                target.collision_box.bottom
                and collision.collision_box.top
                and target_box.bottom >= box.top
                and target_box.top < box.top
                and last_y + target_box.height <= box.top
            ):
                coll.y = box.top - target_box.bottom

        return coll


class CollidableObject2D(
    config.Loadable, pygame.sprite.DirtySprite, metaclass=abc.ABCMeta
):
    def __init__(self, settings: config.CollidableSettings):
        super().__init__()
        self.settings = settings

        self.layer = settings.layer
        image_size = (settings.width, settings.height)
        self.image = settings.image if settings.image else pygame.Surface(image_size)

        self.collision_box = settings.collision_box

        self.rect = self.image.get_rect()
        self.rect.move_ip(settings.topleft)
        self._set_collision_rect(self.image.get_bounding_rect())
        self.last_pos: Coordinate = self.collision_box.rect.topleft

    def _set_collision_rect(self, bounding_rect: pygame.Rect):
        coll_left = self.rect.left + bounding_rect.left
        coll_top = self.rect.top + bounding_rect.top
        self.collision_box.rect.update((coll_left, coll_top), bounding_rect.size)

    def _reset(self):
        (
            x,
            y,
        ) = self.settings.topleft
        self.rect.topleft = (int(x), int(y))
        self._set_collision_rect(self.image.get_bounding_rect())
        self.last_pos: Coordinate = self.collision_box.rect.topleft

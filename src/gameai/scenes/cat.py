from typing import List, Type

import pygame

from gameai import config
from gameai.sprites import CollidableObject2D, Collision2D, Platform2D, cat

from .camera import Camera2D, CameraGroup
from .scene import Scene, end_current_scene


class CatGame(config.Loadable, Scene):

    settings_file: str = config.CAT_GAME_SETTINGS_FILE
    settings_type: Type[config.CatGameSettings] = config.CatGameSettings

    def __init__(self, settings: config.CatGameSettings, screen: pygame.Surface):
        super().__init__(screen)
        self.player = cat.Player.load()
        self.camera = Camera2D(settings.camera, self.player)
        self.sprites: CameraGroup[CollidableObject2D] = CameraGroup(  # type: ignore
            camera=self.camera,
            background=self.background,
        )
        self.sprites.add(self.player)
        self.sprites.add(cat.Floor.load())
        # TODO: use a background image
        self.background.fill("white")
        # set group background surface
        self.sprites.background = self.background
        self.score = 0

    def draw(self) -> List[pygame.Rect]:
        self.sprites.update()
        return self.sprites.draw(self.screen)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: show game menu
                end_current_scene()

    def tick(self, dt: float):
        self.player.move(pygame.key.get_pressed())
        visible_surfaces = [
            s for s in self.sprites if s.visible and isinstance(s, Platform2D)
        ]
        # detect collisions between the player and visible objects
        # XXX: it's expensive to handle collisions on every frame
        coll = Collision2D.between(self.player, visible_surfaces)  # type: ignore
        self.player.handle_collision(coll)
        self.camera.update()

    def dirty_all_sprites(self):
        for sprite in self.sprites:
            sprite.dirty = 1

    def _reset(self):
        super()._reset()
        self.player._reset()

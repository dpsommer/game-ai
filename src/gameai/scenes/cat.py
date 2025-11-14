from typing import List, Type

import pygame

from gameai import config
from gameai.sprites import Collision2D, cat

from .scene import Scene, end_current_scene


class CatGame(config.Loadable, Scene):

    settings_file: str = config.CAT_GAME_SETTINGS_FILE
    settings_type: Type[config.CatGameSettings] = config.CatGameSettings

    def __init__(self, settings: config.CatGameSettings, screen: pygame.Surface):
        super().__init__(screen)
        self.surfaces = pygame.sprite.LayeredDirty()
        self.characters = pygame.sprite.LayeredDirty()
        self.player = cat.Player.load()
        self.characters.add(self.player)
        self.surfaces.add(cat.Floor.load())
        self.score = 0

    def draw(self) -> List[pygame.Rect]:
        # TODO: use a background surface instead
        self.screen.fill("white")
        self.surfaces.update(screen=self.screen)
        self.characters.update(screen=self.screen)
        return self.characters.draw(self.screen) + self.surfaces.draw(self.screen)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: show game menu
                self._wipe()
                end_current_scene()

    def tick(self, dt: float):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        visible_surfaces = [s for s in self.surfaces if s.visible]
        # detect collisions between the player and visible objects
        # XXX: it's expensive to handle collisions on every frame
        coll = Collision2D.between(self.player, visible_surfaces)  # type: ignore
        self.player.handle_collision(coll)

    def dirty_all_sprites(self):
        self.player.dirty = 1

    def _wipe(self):
        super()._wipe()
        self.player._reset()

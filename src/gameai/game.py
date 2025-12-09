import dataclasses
from typing import List, Type

import pygame
import pygame.extensions.dps.core as pgcore
import pygame.extensions.dps.pg2d as pg2d

from . import const
from . import diagnostics as diags
from . import level, player


@dataclasses.dataclass
class CatGameSettings(pgcore.Configurable):
    camera: pg2d.CameraOptions
    platforms: List[level.PlatformSettings]


class CatGame(pgcore.Scene):

    settings_file: str = const.CAT_GAME_SETTINGS_FILE
    settings_type: Type[CatGameSettings] = CatGameSettings

    def __init__(self, settings: CatGameSettings, screen: pygame.Surface):
        super().__init__(screen)
        # load character and level sprites
        self.player = player.Player.load()
        self.platforms = [level.Platform(settings=s) for s in settings.platforms]

        # setup physics controller + load phys objects
        self.physics = pg2d.PhysicsController.load(
            settings_file=const.PHYS_CONTROLLER_SETTINGS_FILE
        )
        self.physics.add_physics_objects(self.player, *self.platforms)

        # setup camera to follow the player. uses a pygame.sprite.AbstractGroup
        # subclass to redraw sprites in the group with camera offset
        self.camera = pg2d.Camera(settings.camera, self.player)
        self.sprites: pg2d.CameraGroup[pg2d.GameSprite] = pg2d.CameraGroup(  # type: ignore
            camera=self.camera,
            background=self.background,
        )
        self.sprites.add(self.player.sprite, *[p.sprite for p in self.platforms])
        # TODO: use a background image
        self.background.fill("white")
        # set group background surface
        self.sprites.background = self.background
        self.score = 0

        # create diagnostics overlay for troubleshooting/debugging purposes
        self.diagnostics_overlay = diags.Diagnostics(self, screen=self.screen)
        self._setup_diagnostics()

    def draw(self) -> List[pygame.Rect]:
        self.sprites.update()
        return self.sprites.draw(self.screen)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                pgcore.new_scene(self.diagnostics_overlay)
            if event.key == pygame.K_ESCAPE:
                # TODO: show game menu
                pgcore.end_current_scene()

    def update(self, dt: float):
        self.physics.update(dt)
        self.camera.update(dt)

    def _setup_diagnostics(self):
        self.diagnostics_overlay.add("Player position", self.player.rect)
        self.diagnostics_overlay.add("Player velocity", self.player.velocity)
        self.diagnostics_overlay.add("Camera position", self.camera.pos)

    def dirty_all_sprites(self):
        for sprite in self.sprites:
            sprite.dirty = 1

    def _reset(self):
        super()._reset()
        self.player.reset()
        self.camera.reset()

import dataclasses

import pygame.extensions.dps.pg2d as pg2d


@dataclasses.dataclass
class PlatformSettings(pg2d.SpriteOptions, pg2d.PhysicsSurfaceSettings):
    pass


class Platform(pg2d.PhysicsSurface):

    settings_type = PlatformSettings

    def __init__(self, settings: PlatformSettings):
        self.sprite = pg2d.GameSprite(settings)
        super().__init__(settings, rect=self.sprite.rect)

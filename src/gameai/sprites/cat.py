from typing import Type

from gameai import config

from .character import Character2D
from .surface import Surface2D


class Cat(Character2D):
    pass


class Player(Cat):

    settings_file: str = "cat_game_player.yml"
    settings_type: Type[config.CatSettings] = config.CatSettings

    def __init__(self, settings: config.CatSettings):
        super().__init__(settings)


class Floor(Surface2D):

    settings_file: str = "cat_game_floor.yml"
    settings_type: Type[config.SurfaceSettings] = config.SurfaceSettings

    def __init__(self, settings: config.SurfaceSettings):
        super().__init__(settings)

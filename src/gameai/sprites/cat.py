from typing import Type

from gameai import config

from .character import Character2D
from .platform import Platform2D


class Player(Character2D):

    settings_file: str = "cat_game_player.yml"
    settings_type: Type[config.CatSettings] = config.CatSettings

    def __init__(self, settings: config.CatSettings):
        super().__init__(settings)


class Floor(Platform2D):

    settings_file: str = "cat_game_floor.yml"
    settings_type: Type[config.PlatformSettings] = config.PlatformSettings

    def __init__(self, settings: config.PlatformSettings):
        super().__init__(settings)

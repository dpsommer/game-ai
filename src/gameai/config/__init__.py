from .io import Configurable, Loadable
from .settings import (
    ButtonOptions,
    GameSettings,
    MainMenuSettings,
    OptionsMenuSettings,
    SpriteOptions,
    TextOptions,
)

# settings file names; keep these in one place so it's easier to
# update them all if we change the config language, for example
GAME_SETTINGS_FILE = "game.yml"
MAIN_MENU_SETTINGS_FILE = "main_menu.yml"
OPTIONS_MENU_SETTINGS_FILE = "options_menu.yml"

__all__ = [
    "Configurable",
    "Loadable",
    "GameSettings",
    "TextOptions",
    "SpriteOptions",
    "ButtonOptions",
    "MainMenuSettings",
    "OptionsMenuSettings",
    "GAME_SETTINGS_FILE",
    "MAIN_MENU_SETTINGS_FILE",
    "OPTIONS_MENU_SETTINGS_FILE",
]

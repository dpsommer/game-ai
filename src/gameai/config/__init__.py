from .io import Configurable, Loadable
from .settings import (
    ButtonOptions,
    CatGameSettings,
    CatSettings,
    CharacterSettings,
    CollidableSettings,
    CollisionBox,
    GameSettings,
    MainMenuSettings,
    OptionsMenuSettings,
    SpriteOptions,
    SurfaceSettings,
    TextOptions,
)

# settings file names; keep these in one place so it's easier to
# update them all if we change the config language, for example
CAT_GAME_SETTINGS_FILE = "cat_game.yml"
GAME_SETTINGS_FILE = "game.yml"
MAIN_MENU_SETTINGS_FILE = "main_menu.yml"
OPTIONS_MENU_SETTINGS_FILE = "options_menu.yml"

__all__ = [
    "Configurable",
    "Loadable",
    "CharacterSettings",
    "CollidableSettings",
    "CollisionBox",
    "GameSettings",
    "TextOptions",
    "SpriteOptions",
    "ButtonOptions",
    "SurfaceSettings",
    "MainMenuSettings",
    "OptionsMenuSettings",
    "CatGameSettings",
    "CatSettings",
    "CAT_GAME_SETTINGS_FILE",
    "GAME_SETTINGS_FILE",
    "MAIN_MENU_SETTINGS_FILE",
    "OPTIONS_MENU_SETTINGS_FILE",
]

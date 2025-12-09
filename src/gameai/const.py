import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parent

DEFAULT_ACCELERATION_FRAMES = 5

# settings file names
GAME_SETTINGS_FILE = "settings/game.yml"
CAT_GAME_SETTINGS_FILE = "settings/cat_game.yml"
MAIN_MENU_SETTINGS_FILE = "settings/main_menu.yml"
OPTIONS_MENU_SETTINGS_FILE = "settings/options_menu.yml"
PHYS_CONTROLLER_SETTINGS_FILE = "settings/physics_controller.yml"
PLAYER_SETTINGS_FILE = "settings/player.yml"

# game actions
MOVE_LEFT_ACTION = "move_left"
MOVE_RIGHT_ACTION = "move_right"
JUMP_ACTION = "jump"

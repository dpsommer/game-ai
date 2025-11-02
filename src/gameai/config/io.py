import pathlib
from typing import Any

import yaml

CONF_DIR = pathlib.Path(__file__).parent / "settings"

__settings = {}


# TODO:
# * create local config file on first run, load from local on subsequent runs
# * save configuration changes
def load_settings(filename: str) -> Any:
    if filename in __settings:
        return __settings[filename]

    try:
        with open(CONF_DIR / filename) as f:
            settings = yaml.safe_load(f)
            __settings[filename] = settings
            return settings

    except yaml.YAMLError as e:
        # TODO: log yaml load error
        print(f"Failed to read YAML from {filename}: {e}")
    except IOError as e:
        print(f"IO error reading {filename}: {e}")


def save_settings():
    pass

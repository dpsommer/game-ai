import pathlib
from typing import Any

import yaml

CONF_DIR = pathlib.Path(__file__).parent / "conf_files"


# TODO:
# * create local config file on first run, load from local on subsequent runs
# * save configuration changes
def load_config(filename: str) -> Any:
    try:
        with open(CONF_DIR / filename) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        # TODO: log yaml load error
        print(f"Failed to read YAML from {filename}: {e}")
    except IOError as e:
        print(f"IO error reading {filename}: {e}")

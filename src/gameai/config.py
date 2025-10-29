import dataclasses

DEFAULT_FRAMERATE = 60

DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720


@dataclasses.dataclass
class Config:
    framerate: int
    screen_width: int
    screen_height: int


def load_config() -> Config:
    # TODO: load values from ini file
    return Config(
        framerate=DEFAULT_FRAMERATE,
        screen_width=DEFAULT_SCREEN_WIDTH,
        screen_height=DEFAULT_SCREEN_HEIGHT,
    )

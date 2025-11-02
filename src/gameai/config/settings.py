import dataclasses

from . import io


@dataclasses.dataclass
class GameSettings:
    framerate: int
    screen_width: int
    screen_height: int
    fullscreen: bool

    @staticmethod
    def load() -> "GameSettings":
        conf = io.load_settings("game.yml")
        return GameSettings(**conf)

    def save(self):
        # TODO: store settings when updated
        pass

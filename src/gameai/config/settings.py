import dataclasses

import pygame

from gameai.types import Align, ColorValue, Coordinate, VerticalAlign

from . import io

DEFAULT_ACCELERATION_FRAMES = 5


@dataclasses.dataclass
class TextOptions(io.Configurable):
    font: pygame.font.Font
    antialias: bool
    color: ColorValue
    hover_color: ColorValue
    align: Align
    v_align: VerticalAlign


# TODO: animatable sprites
@dataclasses.dataclass
class SpriteOptions(io.Configurable):
    topleft: Coordinate = (0, 0)
    image: pygame.Surface | None = None
    layer: int = 0


@dataclasses.dataclass
class ButtonOptions(SpriteOptions):
    text: str = ""
    color: ColorValue = ""
    text_opts: TextOptions | None = None
    width: float = 0
    height: float = 0


@dataclasses.dataclass
class GameSettings(io.Configurable):
    framerate: int
    screen_width: int
    screen_height: int
    fullscreen: bool


@dataclasses.dataclass
class CameraSettings(io.Configurable):
    viewport: pygame.Rect


@dataclasses.dataclass
class MainMenuSettings(io.Configurable):
    play_button: ButtonOptions
    options_button: ButtonOptions
    exit_button: ButtonOptions


@dataclasses.dataclass
class OptionsMenuSettings(io.Configurable):
    margin: int
    fullscreen_button: ButtonOptions
    close_button: ButtonOptions


@dataclasses.dataclass
class CollisionBox(io.Configurable):
    top: bool = False
    left: bool = False
    right: bool = False
    bottom: bool = False
    rect: pygame.Rect = dataclasses.field(
        default_factory=lambda: pygame.Rect(0, 0, 0, 0)
    )


@dataclasses.dataclass
class CollidableSettings(SpriteOptions):
    collision_box: CollisionBox = dataclasses.field(default_factory=CollisionBox)
    width: float = 0
    height: float = 0


@dataclasses.dataclass
class SurfaceSettings(CollidableSettings):
    friction_coefficient: float = 0


@dataclasses.dataclass
class CharacterSettings(CollidableSettings):
    speed: int = 0
    jump_speed: int = 0
    acceleration_frames = DEFAULT_ACCELERATION_FRAMES


@dataclasses.dataclass
class CatGameSettings(io.Configurable):
    pass


@dataclasses.dataclass
class CatSettings(CharacterSettings):
    pass

import dataclasses

import pygame

from gameai.types import Align, ColorValue, Coordinate, VerticalAlign

from . import io


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
class MainMenuSettings(io.Configurable):
    play_button: ButtonOptions
    options_button: ButtonOptions
    exit_button: ButtonOptions


@dataclasses.dataclass
class OptionsMenuSettings(io.Configurable):
    margin: int
    fullscreen_button: ButtonOptions
    close_button: ButtonOptions

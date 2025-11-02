import dataclasses
import enum
from typing import Sequence, Tuple, Callable

import pygame

# use type definitions from pygame._common

RGBOutput = Tuple[int, int, int]
RGBAOutput = Tuple[int, int, int, int]
ColorValue = pygame.Color | int | str | RGBOutput | RGBAOutput | Sequence[int]

Coordinate = Tuple[float, float] | Sequence[float] | pygame.Vector2

WINDOW_SIZE_CHANGED = [
    pygame.WINDOWRESIZED,
    pygame.WINDOWSIZECHANGED,
    pygame.WINDOWMAXIMIZED,
]


class Align(enum.Enum):
    LEFT = 0
    CENTRE = 1
    RIGHT = 2


class VerticalAlign(enum.Enum):
    TOP = 0
    CENTRE = 1
    BOTTOM = 2


@dataclasses.dataclass
class GameOptions:
    framerate: int
    screen_width: int
    screen_height: int


@dataclasses.dataclass
class TextOptions:
    font: pygame.font.Font
    antialias: bool
    color: ColorValue
    align: Align
    v_align: VerticalAlign


@dataclasses.dataclass
class SpriteOptions:
    topleft: Coordinate = (0, 0)
    image: pygame.Surface | None = None


@dataclasses.dataclass
class ButtonOptions(SpriteOptions):
    on_click: Callable = lambda: None
    text: str = ""
    color: ColorValue = ""
    text_opts: TextOptions | None = None
    width: float = 0
    height: float = 0

import enum
from typing import Sequence, Tuple

import pygame

# use type definitions from pygame._common

RGBOutput = Tuple[int, int, int]
RGBAOutput = Tuple[int, int, int, int]
ColorValue = pygame.Color | int | str | RGBOutput | RGBAOutput | Sequence[int]

Coordinate = Tuple[float, float] | Sequence[float] | pygame.Vector2


class Align(enum.Enum):
    LEFT = 0
    CENTRE = 1
    RIGHT = 2


class VerticalAlign(enum.Enum):
    TOP = 0
    CENTRE = 1
    BOTTOM = 2

from typing import Sequence, Tuple, Union

import pygame

# use the same type definitions as font._common
RGBOutput = Tuple[int, int, int]
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.Color, int, str, RGBOutput, RGBAOutput, Sequence[int]]


def draw_text(
        screen: pygame.Surface, text: str, font: pygame.font.Font,
        colour: ColorValue, x: int, y: int):
    antialias = True  # TODO: config option
    img = font.render(text, antialias, colour)
    return screen.blit(img, (x, y))

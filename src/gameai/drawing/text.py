import pygame

from gameai.config import TextOptions
from gameai.types import Align, VerticalAlign


def draw_text(text: str, screen: pygame.Surface, opts: TextOptions):
    img = opts.font.render(text, opts.antialias, opts.color)
    rect = screen.get_rect()
    x = y = 0

    if opts.v_align == VerticalAlign.CENTRE:
        y = rect.height / 2 - (img.get_height() / 2)
    if opts.v_align == VerticalAlign.BOTTOM:
        y = rect.height - img.get_height()

    if opts.align == Align.CENTRE:
        x = rect.width / 2 - (img.get_width() / 2)
    elif opts.align == Align.RIGHT:
        x = rect.width - img.get_width()

    screen.blit(img, (x, y))


__all__ = [
    "draw_text",
]

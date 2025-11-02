import pygame

from gameai import types


def draw_text(text: str, screen: pygame.Surface, opts: types.TextOptions):
    img = opts.font.render(text, opts.antialias, opts.color)
    rect = screen.get_rect()
    x = y = 0

    if opts.v_align == types.VerticalAlign.CENTRE.value:
        y = rect.height / 2 - (img.get_height() / 2)
    if opts.v_align == types.VerticalAlign.BOTTOM.value:
        y = rect.height - img.get_height()

    if opts.align == types.Align.CENTRE.value:
        x = rect.width / 2 - (img.get_width() / 2)
    elif opts.align == types.Align.RIGHT.value:
        x = rect.width - img.get_width()

    screen.blit(img, (x, y))


__all__ = [
    "draw_text",
]

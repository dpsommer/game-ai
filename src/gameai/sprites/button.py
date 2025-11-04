from typing import Callable

import pygame

from gameai.config import ButtonOptions
from gameai.drawing import draw_text


class Button(pygame.sprite.DirtySprite):
    """Clickable image or text button

    Args:
        opts (ButtonOptions): configuration options for the button
        on_click (Callable): on-click callback
    """

    _hovered: bool = False

    def __init__(self, opts: ButtonOptions, on_click: Callable):
        super().__init__()

        image_size = (opts.width, opts.height)
        self.image = opts.image if opts.image else pygame.Surface(image_size)

        self.opts = opts
        self.on_click = on_click

        self.rect = self.image.get_rect()
        self.rect.update(opts.topleft, image_size)

    def update(self, *, screen: pygame.Surface):
        if self.opts.text and self.opts.text_opts is not None:
            self.image.fill(self.opts.color)
            draw_text(self.opts.text, self.image, self.opts.text_opts, self.hovered)
        # just blit here, we make the actual update call in the Scene
        screen.blit(self.image, self.rect)

    @property
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, hovered):
        # only dirty the sprite if we're changing state
        if self._hovered is not hovered:
            self.dirty = 1
        self._hovered = hovered


__all__ = [
    "Button",
]

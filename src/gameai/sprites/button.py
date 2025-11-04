from typing import Callable

import pygame

from gameai.config import ButtonOptions
from gameai.drawing import draw_text


class Button(pygame.sprite.Sprite):

    def __init__(self, opts: ButtonOptions, on_click: Callable):
        super().__init__()

        image_size = (opts.width, opts.height)
        self.image = opts.image if opts.image else pygame.Surface(image_size)

        self.opts = opts
        self.on_click = on_click

        # set sprite position by updating the rect
        self.rect = self.image.get_rect()
        self.rect.update(opts.topleft, image_size)

    def update(self, *, screen: pygame.Surface):
        if self.opts.text and self.opts.text_opts is not None:
            self.image.fill(self.opts.color)
            draw_text(self.opts.text, self.image, self.opts.text_opts)
        # just blit here, we make the actual update call in the Scene
        screen.blit(self.image, self.rect)


__all__ = [
    "Button",
]

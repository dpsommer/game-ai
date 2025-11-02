import pygame

from gameai import types
from gameai.drawing import draw_text


class Button(pygame.sprite.Sprite):

    def __init__(self, opts: types.ButtonOptions):
        super().__init__()

        image_size = (opts.width, opts.height)
        self.image = opts.image if opts.image else pygame.Surface(image_size)

        self.opts = opts
        self.on_click = opts.on_click
        # set sprite position by updating the rect
        self.rect = self.image.get_rect()
        self.rect.update(opts.topleft, image_size)

    def update(self, *, screen: pygame.Surface):
        if self.opts.text and self.opts.text_opts is not None:
            self.image.fill(self.opts.color)
            draw_text(self.opts.text, self.image, self.opts.text_opts)
        # just blit here, we make the actual update call in the Scene
        screen.blit(self.image, self.rect)

    @staticmethod
    def from_config(conf: dict) -> "Button":
        # XXX: this approach is pretty janky. it would be good to have more
        # generic handling of yml -> dataclass loading in the config module
        text_opts = conf.get("text_opts", {})
        font = text_opts.get("font", {})
        # if multiple buttons use the same YAML block definition, they will
        # also share the same python dict - if the value has already been
        # changed to a Font object, we don't need to do anything
        if type(font) is not pygame.font.Font:
            text_opts["font"] = pygame.font.SysFont(**text_opts.get("font", {}))
        conf["text_opts"] = types.TextOptions(**text_opts)
        return Button(types.ButtonOptions(**conf))


__all__ = [
    "Button",
]

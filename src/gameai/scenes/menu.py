from typing import List

import pygame

from gameai.config import load_settings
from gameai.sprites import Button

from .scene import Scene


class Menu(Scene):

    settings_file: str

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        # need https://github.com/pygame/pygame/pull/4635 to be merged
        # to get rid of the pylance type assignment error here
        self.buttons: pygame.sprite.Group[Button] = pygame.sprite.Group()

    def draw(self) -> List[pygame.Rect]:
        self.buttons.update(screen=self.screen)
        return [button.rect for button in self.buttons]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.on_click()

    def tick(self, dt: float):
        pass  # noop

    @classmethod
    def load(cls, screen: pygame.Surface) -> "Menu":
        menu = cls(screen)
        conf = load_settings(cls.settings_file)

        for name, btn_conf in conf["buttons"].items():
            # XXX: cute but janky and may lead to confusing errors
            button = Button.from_config(btn_conf)
            button.on_click = getattr(menu, f"_{name}")
            menu.buttons.add(button)
            setattr(menu, f"{name}_button", button)

        return menu


class MainMenu(Menu):

    settings_file = "main_menu.yml"
    play_button: Button
    options_button: Button
    exit_button: Button

    def draw(self) -> List[pygame.Rect]:
        button_height = self.play_button.rect.height
        # line up buttons in the centre of the screen with 1/4 height spacing
        x = int(self.screen.get_width() / 2)
        mid_y = self.screen.get_height() / 2

        self.play_button.rect.center = (x, int(mid_y - (button_height * 1.25)))
        self.options_button.rect.center = (x, int(mid_y))
        self.exit_button.rect.center = (x, int(mid_y + (button_height * 1.25)))

        return super().draw()

    def _play(self):
        # TODO: start the game
        print("Clicked Play")

    def _options(self):
        # TODO: display options menu
        print("Clicked Options")

    def _exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

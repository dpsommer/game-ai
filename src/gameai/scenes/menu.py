from typing import List

import pygame

from gameai.config import load_config
from gameai.sprites import Button

from .scene import Scene


class Menu(Scene):

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


class MainMenu(Menu):

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        conf = load_config("main_menu.yml")

        self.play_button = self._play_button(conf["buttons"]["play"])
        self.options_button = self._options_button(conf["buttons"]["options"])
        self.exit_button = self._exit_button(conf["buttons"]["exit"])
        self.conf = conf

        self.buttons.add(self.play_button, self.options_button, self.exit_button)

    def draw(self) -> List[pygame.Rect]:
        button_width = self.conf["button_width"]
        button_height = self.conf["button_height"]
        button_size = (button_width, button_height)

        # line up buttons in the centre of the screen with 1/4 height spacing
        x = self.screen.get_width() / 2 - (button_width / 2)
        mid_y = self.screen.get_height() / 2 - (button_height / 2)

        self.play_button.rect.update((x, mid_y - (button_height * 1.25)), button_size)
        self.options_button.rect.update((x, mid_y), button_size)
        self.exit_button.rect.update((x, mid_y + (button_height * 1.25)), button_size)

        return super().draw()

    def _play_button(self, conf: dict) -> Button:
        def play():
            # TODO: start the game
            print("Clicked Play")

        conf["on_click"] = play
        return Button.from_config(conf)

    def _options_button(self, conf: dict) -> Button:
        def show_options():
            # TODO: start the game
            print("Clicked Options")

        conf["on_click"] = show_options
        return Button.from_config(conf)

    def _exit_button(self, conf: dict) -> Button:
        on_click = lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
        conf["on_click"] = on_click
        return Button.from_config(conf)

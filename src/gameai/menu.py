import dataclasses
from typing import List, Type

import pygame
import pygame.extensions.dps.core as pgcore
import pygame.extensions.dps.pg2d as pg2d

from . import const, game


@dataclasses.dataclass
class MainMenuSettings(pgcore.Configurable):
    play_button: pg2d.ButtonOptions
    options_button: pg2d.ButtonOptions
    exit_button: pg2d.ButtonOptions


@dataclasses.dataclass
class OptionsMenuSettings(pgcore.Configurable):
    margin: int
    fullscreen_button: pg2d.ButtonOptions
    close_button: pg2d.ButtonOptions


class MainMenu(pg2d.Menu):
    """Main menu displayed when the game is first run

    Args:
        settings (MainMenuSettings): menu display and button configuration
        screen (pygame.Surface): draw surface for rendering the menu
    """

    settings_file: str = const.MAIN_MENU_SETTINGS_FILE
    settings_type: Type[MainMenuSettings] = MainMenuSettings

    def __init__(self, settings: MainMenuSettings, screen: pygame.Surface):
        super().__init__(screen)
        self.play_button = pg2d.Button(settings.play_button, self._play)
        self.options_button = pg2d.Button(settings.options_button, self._options)
        self.exit_button = pg2d.Button(settings.exit_button, self._exit)
        self.buttons.add(self.play_button, self.options_button, self.exit_button)

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
        pgcore.new_scene(game.CatGame.load(screen=self.screen))

    def _options(self):
        pgcore.new_scene(OptionsMenu.load(screen=self.screen))

    def _exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))


class OptionsMenu(pg2d.Menu):
    """Options submenu for the player to modify game settings

    Args:
        settings (OptionsMenuSettings): menu display and button configuration
        screen (pygame.Surface): draw surface for rendering the menu
    """

    settings_file: str = const.OPTIONS_MENU_SETTINGS_FILE
    settings_type: Type[OptionsMenuSettings] = OptionsMenuSettings

    def __init__(self, settings: OptionsMenuSettings, screen: pygame.Surface):
        super().__init__(screen)
        self.margin = settings.margin
        self.close_button = pg2d.Button(settings.close_button, self._close)
        self.fullscreen_button = pg2d.Button(
            settings.fullscreen_button, self._fullscreen
        )
        self.buttons.add(self.close_button, self.fullscreen_button)

    def draw(self) -> List[pygame.Rect]:
        # TODO: add panes for different option types (general, video, etc.) and
        # flesh out available options; add a toggle button type?
        self._draw_left_panel()
        return super().draw()

    def _draw_left_panel(self):
        for i, button in enumerate(self.buttons):
            y = i * (button.rect.height + self.margin) + self.margin
            button.rect.topleft = (self.margin, y)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._close()
        super().handle_event(event)

    def _close(self):
        pgcore.end_current_scene()

    def _fullscreen(self):
        pygame.display.toggle_fullscreen()

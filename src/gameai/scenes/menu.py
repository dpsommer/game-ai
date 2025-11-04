from typing import List, Type

import pygame

from gameai import config
from gameai.sprites import Button

from .scene import Scene, end_current_scene, new_scene


class Menu(Scene):
    """Base class for in-game menus

    Args:
        screen (pygame.Surface): draw surface for rendering the menu
    """

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        # need https://github.com/pygame/pygame/pull/4635 to be merged
        # to get rid of the pylance type assignment error here
        self.buttons: pygame.sprite.LayeredDirty[Button] = pygame.sprite.LayeredDirty()  # type: ignore

    def draw(self) -> List[pygame.Rect]:
        self.buttons.update(screen=self.screen)
        return [button.rect for button in self.buttons]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.on_click()
                    return
        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.hovered = button.rect.collidepoint(event.pos)

    def tick(self, dt: float):
        pass  # noop

    def dirty_all_sprites(self):
        for button in self.buttons:
            if button.visible:
                button.dirty = 1


class MainMenu(config.Loadable, Menu):
    """Main menu displayed when the game is first run

    Args:
        settings (MainMenuSettings): menu display and button configuration
        screen (pygame.Surface): draw surface for rendering the menu
    """

    settings_file: str = config.MAIN_MENU_SETTINGS_FILE
    settings_type: Type[config.MainMenuSettings] = config.MainMenuSettings

    def __init__(self, settings: config.MainMenuSettings, screen: pygame.Surface):
        super().__init__(screen)
        self.play_button = Button(settings.play_button, self._play)
        self.options_button = Button(settings.options_button, self._options)
        self.exit_button = Button(settings.exit_button, self._exit)
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
        # TODO: start the game
        print("Clicked Play")

    def _options(self):
        options_menu = OptionsMenu.load(screen=self.screen)
        new_scene(options_menu)

    def _exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))


class OptionsMenu(config.Loadable, Menu):
    """Options submenu for the player to modify game settings

    Args:
        settings (OptionsMenuSettings): menu display and button configuration
        screen (pygame.Surface): draw surface for rendering the menu
    """

    settings_file: str = config.OPTIONS_MENU_SETTINGS_FILE
    settings_type: Type[config.OptionsMenuSettings] = config.OptionsMenuSettings

    def __init__(self, settings: config.OptionsMenuSettings, screen: pygame.Surface):
        super().__init__(screen)
        self.margin = settings.margin
        self.close_button = Button(settings.close_button, self._close)
        self.fullscreen_button = Button(settings.fullscreen_button, self._fullscreen)
        self.buttons.add(self.close_button, self.fullscreen_button)

    def draw(self) -> List[pygame.Rect]:
        # TODO: add panes for different option types (general, video, etc.) and
        # flesh out available options; add a toggle button type?
        self.screen.fill("white")
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
        self.screen.fill("black")
        end_current_scene()

    def _fullscreen(self):
        pygame.display.toggle_fullscreen()

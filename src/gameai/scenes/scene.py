import abc
from collections import deque
from typing import List

import pygame


class Scene(abc.ABC):
    """Defines methods for game scenes

    Args:
        screen (pygame.Surface): draw surface for rendering the scene
    """

    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen

    @abc.abstractmethod
    def draw(self) -> List[pygame.Rect]:
        pass

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abc.abstractmethod
    def tick(self, dt: float):
        pass

    @abc.abstractmethod
    def dirty_all_sprites(self):
        pass

    def _wipe(self):
        self.screen.fill("black")
        pygame.display.update()


# track the scene stack so we can overlay scenes
__scenes: deque[Scene] = deque()


def get_active_scene() -> Scene:
    """Returns the currently active scene"""
    return __scenes[0]


def new_scene(scene: Scene):
    """Starts a new scene as the active scene"""
    __scenes.appendleft(scene)


def end_current_scene() -> Scene:
    """Ends the currently active scene and returns the next in the stack"""
    __scenes.popleft()
    active_scene = get_active_scene()
    if active_scene is None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    return active_scene

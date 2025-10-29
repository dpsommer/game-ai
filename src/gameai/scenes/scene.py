import abc
from typing import List

import pygame


class Scene(abc.ABC):

    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__()
        self.screen = screen

    @abc.abstractmethod
    def draw(self) -> List[pygame.Rect]:
        pass

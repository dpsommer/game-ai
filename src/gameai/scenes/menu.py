from typing import List

import pygame

from .scene import Scene


class MainMenu(Scene):

    def draw(self) -> List[pygame.Rect]:
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("purple")
        return []  # whole screen?

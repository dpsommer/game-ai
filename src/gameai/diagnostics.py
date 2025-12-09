from typing import Any, Dict, List

import pygame
import pygame.extensions.dps.core as pgcore
from pygame.extensions.dps.core.types import Coordinate


class Diagnostics(pgcore.Scene):

    def __init__(self, scene: pgcore.Scene, screen: pygame.Surface):
        super().__init__(screen)
        self._diagnostics: Dict[str, Any] = {}
        self.active_scene = scene

    def add(self, name: str, value: Any):
        self._diagnostics[name] = value

    def draw(self) -> List[pygame.Rect]:
        rects = self.active_scene.draw()
        for i, diag in enumerate(self._diagnostics.items()):
            name, val = diag
            if type(val) is pygame.Rect:
                val = val.center
            y_pos = i * 14 + 2
            self.draw_value(name, val, (2, y_pos))
        return rects

    def draw_value(self, name: str, value: Any, pos: Coordinate):
        font = pygame.font.SysFont("arial", 12)
        img = font.render(f"{name}: {value}", True, "black")
        self.screen.blit(img, pos)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_F12, pygame.K_ESCAPE):
                pgcore.end_current_scene()
                return
        self.active_scene.handle_event(event)

    def update(self, dt: float):
        self.active_scene.update(dt)

    def dirty_all_sprites(self):
        self.active_scene.dirty_all_sprites()

    def _reset(self):
        pass  # no-op

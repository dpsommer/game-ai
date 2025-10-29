import pygame

from . import scenes


class Game:
    def __init__(self, framerate=60, width=1280, height=720):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.scene = scenes.MainMenu(self.screen)
        self._running = True
        self._dt = 0

    def run(self):
        while self._running:
            self._handle_events()
            self._render()
            self._tick()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _render(self):
        rects = self.scene.draw()
        pygame.display.update(rects)

    def _tick(self):
        # TODO: tick behaviour trees
        self._dt = self.clock.tick(self.framerate) / 1000

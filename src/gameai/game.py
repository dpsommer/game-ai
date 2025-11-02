import pygame

from . import scenes, types


class Game:

    def __init__(self, opts: types.GameOptions):
        pygame.init()

        screen_size = (opts.screen_width, opts.screen_height)
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.framerate = opts.framerate
        self._running = False

    def run(self):
        self._running = True
        main_menu = scenes.MainMenu(self.screen)
        scenes.new_scene(main_menu)

        while self._running:
            self._handle_events()
            self._tick()
            self._render()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            # handle system-level events here and everything else in the scene
            match event.type:
                case pygame.QUIT:
                    self._running = False
                case pygame.WINDOWRESIZED | pygame.WINDOWSIZECHANGED:
                    self.screen.fill("black")
                    pygame.display.update()
                case pygame.WINDOWMAXIMIZED:
                    self.screen.fill("black")
                    pygame.display.toggle_fullscreen()
                    pygame.display.update()
                case _:
                    scene = scenes.get_active_scene()
                    scene.handle_event(event)

    def _render(self):
        # XXX: should we be drawing all/some scenes, not just the active one?
        active_scene = scenes.get_active_scene()
        rects = active_scene.draw()
        pygame.display.update(rects)

    def _tick(self):
        dt = self.clock.tick(self.framerate) / 1000
        scene = scenes.get_active_scene()
        scene.tick(dt)

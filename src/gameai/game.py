import pygame

from . import scenes, types

GAME_WIDTH = 640
GAME_HEIGHT = 360


class Game:

    def __init__(self, opts: types.GameOptions):
        pygame.init()

        screen_size = (opts.screen_width, opts.screen_height)
        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode(screen_size, flags=flags)
        # create two surfaces to use for scaling purposes. the draw surface is
        # a fixed size, and all scenes draw to it. the aspect surface maintains
        # the same aspect ratio as the draw surface, but scales with the screen
        self._draw_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self._aspect_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self._rescale()

        self.clock = pygame.time.Clock()
        self.framerate = opts.framerate
        self._running = False

    def run(self):
        self._running = True
        main_menu = scenes.MainMenu(self._draw_surface)
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
                    # self.screen.fill("black")
                    self._rescale()
                case pygame.WINDOWMAXIMIZED:
                    # self.screen.fill("black")
                    pygame.display.toggle_fullscreen()
                    self._rescale()
                case _:
                    scene = scenes.get_active_scene()
                    scene.handle_event(event)

    def _render(self):
        # XXX: should we be drawing all/some scenes, not just the active one?
        scene = scenes.get_active_scene()
        scene.draw()

        size = self._aspect_surface.get_size()
        pygame.transform.scale(self._draw_surface, size, self._aspect_surface)

        aspect_rect = self._aspect_surface.get_rect()
        aspect_rect.center = self.screen.get_rect().center
        self.screen.blit(self._aspect_surface, aspect_rect)
        # XXX: is it possible to still limit the redraw surface despite scaling?
        pygame.display.update(aspect_rect)

    def _tick(self):
        dt = self.clock.tick(self.framerate) / 1000
        scene = scenes.get_active_scene()
        scene.tick(dt)

    def _rescale(self):
        aspect_width = self.screen.get_width() / GAME_WIDTH
        aspect_height = self.screen.get_height() / GAME_HEIGHT
        ratio = min(aspect_width, aspect_height)
        size = (GAME_WIDTH * ratio, GAME_HEIGHT * ratio)

        self._aspect_surface = pygame.transform.scale(self._aspect_surface, size)
        pygame.display.update()

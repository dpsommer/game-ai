import pygame

from . import config, scenes, types

GAME_WIDTH = 640
GAME_HEIGHT = 360


class Game(config.Loadable):

    settings_file = "game.yml"
    settings_type = config.GameSettings

    def __init__(self, settings: config.GameSettings):
        pygame.init()

        screen_size = (settings.screen_width, settings.screen_height)
        flags = pygame.RESIZABLE | (settings.fullscreen and pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(screen_size, flags=flags)
        # create two surfaces to use for scaling purposes. the draw surface is
        # a fixed size, and all scenes draw to it. the aspect surface maintains
        # the same aspect ratio as the draw surface, but scales with the screen
        self._draw_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self._aspect_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self._rescale()

        self.clock = pygame.time.Clock()
        self.framerate = settings.framerate
        self._running = False

    def run(self):
        self._running = True
        main_menu = scenes.MainMenu.load(self._draw_surface)
        scenes.new_scene(main_menu)

        while self._running:
            self._handle_events()
            self._tick()
            self._render()

        pygame.quit()

    def _handle_events(self):
        scene = scenes.get_active_scene()

        for event in pygame.event.get():
            # handle system-level events here and everything else in the scene
            match event.type:
                case pygame.QUIT:
                    self._running = False
                case pygame.WINDOWRESIZED | pygame.WINDOWSIZECHANGED:
                    self._rescale()
                case pygame.WINDOWMAXIMIZED:
                    pygame.display.toggle_fullscreen()
                    self._rescale()
                case pygame.MOUSEBUTTONDOWN | pygame.MOUSEBUTTONUP | pygame.MOUSEMOTION:
                    # adjust the position of mouse events by the window scale factor
                    event.pos = self._scale_pos(event.pos)
                    scene.handle_event(event)
                case _:
                    scene.handle_event(event)

    def _render(self):
        # XXX: should we be drawing all/some scenes, not just the active one?
        scene = scenes.get_active_scene()
        scene.draw()

        size = self._aspect_surface.get_size()
        pygame.transform.smoothscale(self._draw_surface, size, self._aspect_surface)

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
        scale_factor = self.get_scale_factor()
        size = (GAME_WIDTH * scale_factor, GAME_HEIGHT * scale_factor)
        self._aspect_surface = pygame.transform.smoothscale(self._aspect_surface, size)
        pygame.display.update()

    def _scale_pos(self, pos: types.Coordinate) -> types.Coordinate:
        x, y = pos
        aspect_w, aspect_h = self._aspect_surface.get_size()
        x_offset = (self.screen.get_width() - aspect_w) / 2
        y_offset = (self.screen.get_height() - aspect_h) / 2
        scale_factor = self.get_scale_factor()
        return ((x - x_offset) / scale_factor, (y - y_offset) / scale_factor)

    def get_scale_factor(self) -> float:
        width_scale = self.screen.get_width() / GAME_WIDTH
        height_scale = self.screen.get_height() / GAME_HEIGHT
        return min(width_scale, height_scale)

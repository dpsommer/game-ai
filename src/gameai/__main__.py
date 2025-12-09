import pygame
import pygame.extensions.dps.core as pgcore

from . import const, menu


def run():
    pygame.init()
    pgcore.init(resource_dir=const.ROOT_DIR, game_name="Cat Game")
    game = pgcore.Game.load(settings_file=const.GAME_SETTINGS_FILE)
    game.run(menu.MainMenu.load(screen=game._draw_surface))


if __name__ == "__main__":
    run()

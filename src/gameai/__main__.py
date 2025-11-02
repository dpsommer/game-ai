from . import config, game


def run():
    conf = config.GameSettings.load()
    game.Game(conf).run()


if __name__ == "__main__":
    run()

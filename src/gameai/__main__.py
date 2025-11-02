from . import config, game, types


def run():
    conf = config.load_config("game.yml")
    game.Game(types.GameOptions(**conf)).run()


if __name__ == "__main__":
    run()

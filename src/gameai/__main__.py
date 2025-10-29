from . import config, game


def run():
    conf = config.load_config()
    game.Game(
        framerate=conf.framerate,
        width=conf.screen_width,
        height=conf.screen_height
    ).run()

if __name__ == "__main__":
    run()

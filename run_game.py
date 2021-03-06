from gametitle.bootstrap import bootstrap_game
from zkit import config


if __name__ == "__main__":
    if config.getboolean('general', 'profile'):
        import cProfile
        import pstats

        game = bootstrap_game()
        cProfile.run('game.loop()', "results.prof")
        p = pstats.Stats("results.prof")
        p.strip_dirs()
        p.sort_stats('cumulative').print_stats(50)

    else:
        try:
            game = bootstrap_game()
            game.loop()
        except:
            import pygame
            pygame.quit()
            raise

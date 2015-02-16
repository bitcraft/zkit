import logging

import pygame
from pygame.display import set_mode

from zkit import config
from zkit import gui
from zkit import resources
from zkit.scenes import Game
from zkit.level import LevelScene

from gametitle.title import TitleScene

logger = logging.getLogger('zkit.bootstrap')


def bootstrap_game():
    pygame.display.init()
    pygame.mixer.init(frequency=config.getint('sound', 'frequency'),
                      buffer=config.getint('sound', 'buffer'))
    pygame.font.init()
    pygame.init()

    main_surface = set_mode((config.getint('display', 'width'),
                             config.getint('display', 'height')))

    main_surface.fill((0, 0, 0))
    gui.draw_text(main_surface, "loading, please wait...", (255, 255, 255),
                  main_surface.get_rect())
    pygame.display.flip()

    for path, thing in resources.load():
        logger.info('loaded %s', path)
        pygame.event.pump()

    game = Game(config.getint('display', 'target-fps'), main_surface)
    game.register_scene(TitleScene(game))
    level_scene = LevelScene(game)
    game.register_scene(level_scene)
    level_scene.init()
    game.push_scene('level')
    return game

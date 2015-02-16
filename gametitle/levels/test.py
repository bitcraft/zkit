"""
This is a demo level
"""

# import your game entities here
# implement any level specific enemies here

from zkit.entity import *
from gametitle.enemies import *


def setup_level(level_scene):
    """
    Initialize your entities
    """
    level_scene.move_hero((1, 1))

    level_scene.build_entity(Saucer, 'shipPink_manned.png', (4, 4))
    level_scene.build_entity(Enemy, "alienGreen.png", (4, 4))

    level_scene.build_button("testDoor", "tileMagic_tile.png", (2, 4))
    level_scene.build_door("testDoor", (0, 0))

    e = ShipPart('smallRockStone.png', level_scene.load_level)
    level_scene.add_entity(e, (2, 2))

    # # start the silly timer to drop powerups
    # #timer = Task(self.new_powerup, 5000, -1)
    # #self.timers.add(timer)


def handle_internal_events(level_scene):
    """
    Handle non-entity specific events here
    (or entity specific events if that means getting the game done on time)
    """
    pass

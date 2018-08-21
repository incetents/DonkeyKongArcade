# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Shows a timer with remaining bonus time on it

from Engine.Entity import *
from Game.GameHud import *
from Game.GameData import *


class BonusTime(Entity):
    def __init__(self, ent_name: str):
        # Base
        Entity.__init__(self, ent_name)
        # Hud Piece
        self.gui: Hud = Hud('hud_bonus_counter', 'spr_bonus_counter', Vector3(171, 197, 0))
        self.time: Numbers = Numbers(0, Vector3(176, 200, 0), Vector4(0, 1, 1, 1), 4)

    def update(self, delta_time):
        self.gui.update(delta_time)
        self.time.update_number(GameData.get_singleton().get_bonus_time())

    def draw(self):
        self.gui.draw()
        self.time.draw()
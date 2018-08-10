
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Hud System for game
from Engine.Sprite import *
import Engine.Storage
from Engine.Transform import *
from Engine.Entity import *
from Engine.SpriteBatch import *
from Game.GameData import *
from Engine.Text import *

_instance = None

class Hud(Entity):
    def __init__(self, entity_name: str, sprite_name: str, position: Vector3):
        # Base Constructor
        Entity.__init__(self, entity_name)
        # Sprite
        self.sprite = self.add_component(Engine.Storage.get(Engine.Storage.Type.SPRITE, sprite_name))
        # Transform
        self.transform.set_position(position)

    def draw(self):
        self.sprite.draw(self.transform)

class GameHud:
    def __init__(self):
        # self._mario_lives: List[Hud] = []
        self._mario_lives_1: Hud = None
        self._mario_lives_2: SpriteBatch = None
        self._mario_lives_3: SpriteBatch = None
        self._mario_lives_4: SpriteBatch = None
        self._mario_lives_5: SpriteBatch = None
        self._bonus_counter: Hud = None

        self._player1_score: Text = None

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = GameHud()
        return _instance

    def setup(self):
        _m1 = Hud('hud_mario_life1', 'spr_mini_mario', Vector3(8, 224, 0))
        _m2 = Hud('hud_mario_life2', 'spr_mini_mario', Vector3(16, 224, 0))
        _m3 = Hud('hud_mario_life3', 'spr_mini_mario', Vector3(24, 224, 0))
        _m4 = Hud('hud_mario_life4', 'spr_mini_mario', Vector3(32, 224, 0))
        _m5 = Hud('hud_mario_life5', 'spr_mini_mario', Vector3(40, 224, 0))

        self._mario_lives_2 = SpriteBatch('batch_mario_lives2', 'mini_mario')
        self._mario_lives_3 = SpriteBatch('batch_mario_lives3', 'mini_mario')
        self._mario_lives_4 = SpriteBatch('batch_mario_lives4', 'mini_mario')
        self._mario_lives_5 = SpriteBatch('batch_mario_lives5', 'mini_mario')

        self._mario_lives_2.add_entities([_m1, _m2])
        self._mario_lives_3.add_entities([_m1, _m2, _m3])
        self._mario_lives_4.add_entities([_m1, _m2, _m3, _m4])
        self._mario_lives_5.add_entities([_m1, _m2, _m3, _m4, _m5])

        self._mario_lives_1 = _m1
        self._bonus_counter = Hud('hud_bonus_counter', 'spr_bonus_counter', Vector3(171, 198, 0))

    def draw(self):
        _data = GameData.get_singleton()

        # Draw Lives
        if _data.lives >= 6:
            self._mario_lives_5.draw()
        elif _data.lives is 5:
            self._mario_lives_4.draw()
        elif _data.lives is 4:
            self._mario_lives_3.draw()
        elif _data.lives is 3:
            self._mario_lives_2.draw()
        elif _data.lives is 2:
            self._mario_lives_1.draw()
        else:
            # Draw Nothing
            pass

        # self._mario_life.draw()

        self._bonus_counter.draw()
        pass
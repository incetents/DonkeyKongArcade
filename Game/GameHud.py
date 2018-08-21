
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Hud System for game
from Engine.Text import *
import Engine.Text
from Engine.Sprite import *
import Engine.Storage
from Engine.Transform import *
from Engine.Entity import *
from Engine.SpriteBatch import *
from Game.GameData import *
from Game.Numbers import *


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
        self._mario_icons: List[Hud] = []
        self._mario_icon_batch: SpriteBatch = None
        self._mario_icon_draw: bool = True
        self._bonus_counter: Hud = None
        self._highscore_text1: Hud = None
        self._highscore_text2: Hud = None
        self._highscore_text3: Hud = None
        self._life_icon: Hud = None
        self._highscore_text1: Hud = None
        self._highscore_text2: Hud = None
        self._highscore_text3: Hud = None

        self._life_amount: Numbers = Numbers(0, Vector3(186, 224, 0), Vector4(0, 0, 170.0/255.0, 1), 2)
        self._player1_score: Numbers = Numbers(0, Vector3(8, 240, 0))
        self._player2_score: Numbers = Numbers(0, Vector3(160, 240, 0))
        self._highscore: Numbers = Numbers(0, Vector3(88, 240, 0))
        self._bonus_timer: Numbers = Numbers(0, Vector3(176, 200, 0), Vector4(0, 1, 1, 1), 4)

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = GameHud()
        return _instance

    def setup(self):
        # Mario Lives
        self._mario_icons.append(Hud('hud_mario_life1', 'spr_mini_mario', Vector3(8, 224, 0)))
        self._mario_icons.append(Hud('hud_mario_life2', 'spr_mini_mario', Vector3(16, 224, 0)))
        self._mario_icons.append(Hud('hud_mario_life3', 'spr_mini_mario', Vector3(24, 224, 0)))
        self._mario_icons.append(Hud('hud_mario_life4', 'spr_mini_mario', Vector3(32, 224, 0)))
        self._mario_icons.append(Hud('hud_mario_life5', 'spr_mini_mario', Vector3(40, 224, 0)))
        ic = self._mario_icons

        self._mario_icon_batch = SpriteBatch('batch_mario_lives', 'mini_mario')
        self._mario_icon_batch.add_entities([ic[0], ic[1], ic[2], ic[3], ic[4]])

        self._bonus_counter = Hud('hud_bonus_counter', 'spr_bonus_counter', Vector3(171, 197, 0))
        self._life_icon = Hud('life_icon', 'spr_life_icon', Vector3(170, 224, 0))

        self._highscore_text1 = Hud('highscore_text1', 'spr_highscore1', Vector3(0, 248, 0))
        self._highscore_text2 = Hud('highscore_text2', 'spr_highscore2', Vector3(0, 248, 0))
        self._highscore_text3 = Hud('highscore_text3', 'spr_highscore3', Vector3(0, 248, 0))

    def update_lives(self):
        _lives = GameData.get_singleton().get_lives()
        # Update Lives
        if _lives >= 6:
            self._mario_icons[0].enabled = True
            self._mario_icons[1].enabled = True
            self._mario_icons[2].enabled = True
            self._mario_icons[3].enabled = True
            self._mario_icons[4].enabled = True
        elif _lives is 5:
            self._mario_icons[0].enabled = True
            self._mario_icons[1].enabled = True
            self._mario_icons[2].enabled = True
            self._mario_icons[3].enabled = True
            self._mario_icons[4].enabled = False
        elif _lives is 4:
            self._mario_icons[0].enabled = True
            self._mario_icons[1].enabled = True
            self._mario_icons[2].enabled = True
            self._mario_icons[3].enabled = False
            self._mario_icons[4].enabled = False
        elif _lives is 3:
            self._mario_icons[0].enabled = True
            self._mario_icons[1].enabled = True
            self._mario_icons[2].enabled = False
            self._mario_icons[3].enabled = False
            self._mario_icons[4].enabled = False
        elif _lives is 2:
            self._mario_icons[0].enabled = True
            self._mario_icons[1].enabled = False
            self._mario_icons[2].enabled = False
            self._mario_icons[3].enabled = False
            self._mario_icons[4].enabled = False

        self._mario_icon_draw = _lives > 1

    def draw(self):
        # _data = GameData.get_singleton()

        # Lives
        if self._mario_icon_draw:
            self._mario_icon_batch.draw()
        # Bonus
        # self._bonus_counter.draw()

        # Highscore text
        if pygame.time.get_ticks() % 1000 > 500:
            self._highscore_text1.draw()
        else:
            if GameData.get_singleton().check_player1_turn():
                self._highscore_text2.draw()
            else:
                self._highscore_text3.draw()

        # Highscore
        self._highscore.update_number(GameData.get_singleton().get_highscore())
        self._highscore.draw()

        # Bonus timer
        # self._bonus_timer.update_number(GameData.get_singleton().get_bonus_time())
        # self._bonus_timer.draw()

        # Life Icon + amount
        self._life_icon.draw()
        self._life_amount.update_number(GameData.get_singleton().get_level())
        self._life_amount.draw()

        # Score
        if GameData.get_singleton().check_player1_turn():
            self._player1_score.update_number(GameData.get_singleton().get_player1_score())
        else:
            self._player2_score.update_number(GameData.get_singleton().get_player2_score())

        self._player1_score.draw()
        self._player2_score.draw()


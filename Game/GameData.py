
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Global Game Data
from Game.Mario import *
from Game.DonkeyKong import *
from Game.Oilbarrel import *

_instance = None


class GameData:
    def __init__(self):
        # objects
        self.global_mario: Mario = None
        self.global_dk: DonkeyKong = None
        self.global_oil: Oilbarrel = None
        # Data
        self._lives_player1: int = 6
        self._lives_player2: int = 6
        self._score_player1: int = 0
        self._score_player2: int = 0
        self._highscore: int = 0
        self._player1_turn: bool = True
        self._bonus_time: int = 0
        self._level: int = 1
        self._level_start_time: int = 0
        self._level_seconds_passed: int = 0

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = GameData()
        return _instance

    def init_level_time(self):
        self._level_start_time = pygame.time.get_ticks()

    def update_level_time(self):
        self._level_seconds_passed = math.floor((pygame.time.get_ticks() - self._level_start_time) / 1000)
        self._bonus_time = max(0, 5000 + 1000 * (self._level - 1) - (100 * self._level_seconds_passed))

    def add_score(self, _score: int):
        if self._player1_turn:
            self._score_player1 += _score
            self._highscore = max(self._highscore, self._score_player1)
        else:
            self._score_player2 += _score
            self._highscore = max(self._highscore, self._score_player2)

    def get_player1_score(self) -> int:
        return self._score_player1

    def get_player2_score(self) -> int:
        return self._score_player2

    def check_player1_turn(self) -> bool:
        return self._player1_turn

    def get_current_player_score(self) -> int:
        if self._player1_turn:
            return self._score_player1
        else:
            return self._score_player2

    def get_lives(self) -> int:
        if self._player1_turn:
            return self._lives_player1
        else:
            return self._lives_player2

    def increase_lives(self, amount: int):
        if self._player1_turn:
            self._lives_player1 += amount
        else:
            self._lives_player2 += amount

    def get_highscore(self) -> int:
        return self._highscore

    def get_bonus_time(self) -> int:
        return self._bonus_time
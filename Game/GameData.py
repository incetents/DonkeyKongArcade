
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Global Game Data

_instance = None

class GameData:
    def __init__(self):
        self.lives: int = 6
        self._score_player1: int = 0
        self._score_player2: int = 0
        self._player1_turn: bool = True
        pass

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = GameData()
        return _instance

    def add_score(self, _score: int):
        if self._player1_turn:
            self._score_player1 += _score
        else:
            self._score_player2 += _score

    def get_player1_score(self) -> int:
        return self._score_player1

    def get_player2_score(self) -> int:
        return self._score_player2

    def get_current_player_score(self) -> int:
        if self._player1_turn:
            return self._score_player1
        else:
            return self._score_player2
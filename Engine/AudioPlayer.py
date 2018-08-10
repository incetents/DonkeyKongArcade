
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Simple Audio Manager

from __future__ import annotations
import pygame
from typing import *
from pathlib import Path
import Engine.Storage

_instance = None


class AudioPlayer:
    def __init__(self):
        self._active_song: Song = None
        self._repeat_count: int = 0
        self._sfx: Dict[str, SFX] = {}

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = AudioPlayer()
        return _instance

    @staticmethod
    def stop_all_audio():
        pygame.mixer.stop()

    def set_song(self, song: str, repeat_count: int=0):
        self._active_song = Engine.Storage.get(Engine.Storage.Type.SONG, song)
        self.set_repeat_count(repeat_count)
        return self

    def set_repeat_count(self, _count: int):
        self._repeat_count = _count
        return self

    def play_song(self):
        if self._active_song is not None:
            pygame.mixer.music.load(self._active_song.get_file_path())
            pygame.mixer.music.play(self._repeat_count)
        return self

    def stop_song(self):
        if self._active_song is not None:
            pygame.mixer.music.stop()
        return self

    def set_song_pause(self, _state: bool):
        if self._active_song is not None:
            if _state:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        return self

class Song:
    def __init__(self, song_name: str, file_path: str):
        super().__init__()
        my_file = Path(file_path)
        self._file_path = ''
        if my_file.is_file():
            self._file_path = file_path
            # Add to storage
            Engine.Storage.add(Engine.Storage.Type.SONG, song_name, self)
        else:
            print('File does not exist', file_path)

    def get_file_path(self) -> str:
        return self._file_path

class SFX:
    def __init__(self, song_name: str, file_path: str):
        super().__init__()
        # Check if file exists
        my_file = Path(file_path)
        if my_file.is_file():
            try:
                self._audio_file = pygame.mixer.Sound(file_path)
                Engine.Storage.add(Engine.Storage.Type.SFX, song_name, self)
            except:
                print('Unable to load file due to bitrate issue', file_path)
        else:
            print('File does not exist', file_path)

    def play(self):
        self._audio_file.play()

    def stop(self):
        self._audio_file.stop()


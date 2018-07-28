
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Keep Track of Time]

import pygame

class Clock:
    def __init__(self, seconds: float=0):
        self._seconds = seconds
        self._time_start = pygame.time.get_ticks()
        self._time_end = self._time_start + seconds * 1000.0

    def get_seconds(self) -> float:
        return self._seconds

    def get_remaining_time(self) -> float:
        return max(0, self._time_end - pygame.time.get_ticks())

    def add_time(self, seconds):
        self._seconds += seconds
        self._time_end += seconds * 1000.0

    def reset(self):
        self._time_start = pygame.time.get_ticks()
        self._time_end = self._time_start + self._seconds * 1000.0

    def reset_with_new_time(self, seconds):
        self._seconds = seconds
        self._time_start = pygame.time.get_ticks()
        self._time_end = self._time_start + seconds * 1000.0

    def is_finished(self) -> bool:
        return self._time_end < pygame.time.get_ticks()
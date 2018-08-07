
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Base Engine Starting Location

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Engine.Collision import *
import Engine.Collision
import Engine.CollisionManager
from Engine.Vector import *

import Engine.Storage
import Engine.Input
from Game.Game import *
import Engine.Config
import Engine.Graphics

_instance = None

class engine:
    def __init__(self):
        self.running: bool = True
        self.clock = pygame.time.Clock()
        self.game = Game.get_singleton()
        self.dela_time: float = 0.0

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = engine()
        return _instance

    def start(self):
        # Graphics/Input Process
        pygame.init()
        pygame.display.set_caption('Donkey Kong Arcade [Python]')
        gameDisplay = pygame.display.set_mode((Engine.Config.SCREEN_WIDTH, Engine.Config.SCREEN_HEIGHT),
                                              DOUBLEBUF | OPENGLBLIT)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        Engine.Input.setup()

        self.game.setup()


    def exit(self):
        pygame.quit()
        quit()

    def _update(self):
        self.delta_time: float = 0
        if self.clock.get_fps() > 0.0:
            # set and Cap delta time for safety
            self.delta_time = min(0.1, 1.0 / self.clock.get_fps())

        # Update Game
        self.game.update(self.delta_time)

        # FPS Clock Update
        self.clock.tick(60)

    def m_loop(self):
        while self.running:
            # Special Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            # Update
            if Engine.Input.get_key(pygame.K_ESCAPE):
                self.running = False
                return

            # Clear Screen
            Engine.Graphics.clear_screen()

            # Update Game
            self._update()

            # Draw Game
            self.game.draw()
            self.game.draw_UI(self.delta_time)

            # Update Buffer
            pygame.display.flip()

            # Updates Input
            Engine.Input.update()



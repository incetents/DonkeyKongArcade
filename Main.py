
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Engine.Collision import Collider_AABB_2D, Collider_Circle_2D
import Engine.Collision
from Engine.Vector import Vector2, Vector3

import Engine.Storage
import Engine.Input
# import Game.Game
from Game.Game import Game
import Engine.Config
import Engine.Graphics


# Vertices
vertices = (
    (+1, -1, -1),
    (+1, +1, -1),
    (-1, +1, -1),
    (-1, -1, -1),
    (+1, -1, +1),
    (+1, +1, +1),
    (-1, -1, +1),
    (-1, +1, +1)
)
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

rotation = 0

def Spr():

    _size = 50.0
    glPushMatrix()

    glBegin(GL_QUADS)

    # glTexCoord2f(0, 0)
    glColor3fv((1, 1, 0))
    glVertex3fv((0, 0, -5))

    # glTexCoord2f(1, 0)
    glColor3fv((1, 1, 0))
    glVertex3fv((_size, 0, -5))

    # glTexCoord2f(1, 1)
    glColor3fv((1, 1, 1))
    glVertex3fv((_size, _size, -5))

    # glTexCoord2f(0, 1)
    glColor3fv((1, 0, 1))
    glVertex3fv((0, _size, -5))

    glEnd()

    glPopMatrix()

    glFlush()


def Cube():
    global rotation

    glPushMatrix()
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(rotation, 0, 1, 0)
    rotation += 5.0
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    glPopMatrix()


def text_objects(text, font):
    textSurface = font.render(text, True, (1,0,0))
    return textSurface, textSurface.get_rect()


def main():
    # Engine Setup
    pygame.init()
    pygame.display.set_caption('Donkey Kong Arcade [Python]')
    gameDisplay = pygame.display.set_mode((Engine.Config.SCREEN_WIDTH, Engine.Config.SCREEN_HEIGHT), DOUBLEBUF | OPENGLBLIT)
    clock = pygame.time.Clock()

    # gluPerspective(45, gameDisplay[0]/gameDisplay[1], 0.1, 50.0)
    # glOrtho(-SCREEN_WIDTH/2, +SCREEN_WIDTH/2, -SCREEN_HEIGHT/2, +SCREEN_HEIGHT/2, -500, 500.0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    running = True

    # Game
    _game = Game.get_singleton()

    # Misc Setup
    Engine.Input.setup()

    while running:
        # Special Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        if Engine.Input.get_key(pygame.K_ESCAPE):
            running = False

        # Clear Screen
        Engine.Graphics.clear_screen()

        # Update Game
        _delta_time: float = 0
        if clock.get_fps() > 0.0:
            _delta_time = 1.0 / clock.get_fps()

        # Update with Delta time (0 safety check)
        _game.update(_delta_time)
        # Draw Game
        _game.draw()
        _game.draw_UI(_delta_time)

        # Update Buffer
        pygame.display.flip()

        # Updates Input
        Engine.Input.update()

        # FPS Clock Update
        clock.tick(60)

    pygame.quit()
    quit()


# Run Main
if __name__ == "__main__":
    main()
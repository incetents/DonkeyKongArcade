
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Main Camera Controls Only

from OpenGL.GL import *
from Engine.Transform import Transform
from Engine.Vector import Vector3
import Engine.Config

position: Vector3 = Vector3(114, 90, 0)
zoom: float = 3

move_speed: float = 3
scale_speed: float = 0.1

def push():
    # Camera Perspective
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(
        -Engine.Config.SCREEN_WIDTH / 2,
        +Engine.Config.SCREEN_WIDTH / 2,
        -Engine.Config.SCREEN_HEIGHT / 2,
        +Engine.Config.SCREEN_HEIGHT / 2,
        -500, 500.0
    )
    # Apply Camera Transformation
    global model
    # Zoom Effect
    if zoom is not 1:
        glPushMatrix()
        if zoom != 0:
            glScalef(zoom, zoom, zoom)
    # Movement
    glPushMatrix()
    glTranslatef(-position.x, -position.y, -position.z)


def pop():
    glPopMatrix()
    if zoom is not 1:
        glPopMatrix()


def move_up():
    global position
    position += Vector3(0, +move_speed, 0)

def move_down():
    global position
    position += Vector3(0, -move_speed, 0)

def move_left():
    global position
    position += Vector3(-move_speed, 0, 0)

def move_right():
    global position
    position += Vector3(+move_speed, 0, 0)

def zoom_out():
    global zoom
    zoom = max(0.1, zoom - scale_speed)

def zoom_in():
    global zoom
    zoom += scale_speed
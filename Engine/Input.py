
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Mouse / Keyboard / Joystick Data
import pygame

KeyboardState_Current = None
KeyboardState_Previous = None


def setup():
    global KeyboardState_Previous
    global KeyboardState_Current

    KeyboardState_Previous = pygame.key.get_pressed()
    KeyboardState_Current = pygame.key.get_pressed()


def update():
    global KeyboardState_Previous
    global KeyboardState_Current

    KeyboardState_Previous = KeyboardState_Current
    KeyboardState_Current = pygame.key.get_pressed()


def get_key(_key_code: pygame.key) -> bool:
    return KeyboardState_Current[_key_code]


def get_key_pressed(_key_code: pygame.key) -> bool:
    return KeyboardState_Current[_key_code] and not KeyboardState_Previous[_key_code]


def get_key_release(_key_code: pygame.key) -> bool:
    return not KeyboardState_Current[_key_code] and KeyboardState_Previous[_key_code]



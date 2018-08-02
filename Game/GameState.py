
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Controls states of Game Class

# Math
import math
import Engine.Camera
import Engine.Collision
import Engine.Storage
from Engine.Storage import *
from Engine.Collision import *
from Engine.CollisionManager import *
from Engine.Raycast import *
from Engine.Vector import *
# Entities / Sprites
from Engine.Sprite import *
from Engine.Entity import *
# Misc
from typing import List
import Engine.Graphics
import Engine.Config
# Game
import pygame
from Game.MarioState import *
from Game.Mario import *
from Game.Tile import *
from Game.Enemy_Fire import *
from Game.Barrel import *
from Game.Oilbarrel import *
from Game.InvisBlock import *
import Engine.Input
from Engine.Text import *
import Engine.Config

ray: Raycast_2D = None

class GameState:
    def __init__(self):
        # Reset Collision System
        ColliderManager_2D.get_singleton().clear()
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass

    def draw(self):
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.test = Tile('dk', 'spr_dk1', Vector3())

        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass

    def draw(self):
        self.test.draw()
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Load(GameState):
    def __init__(self):
        GameState.__init__(self)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        pass

    def draw(self):
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Game(GameState):
    def __init__(self):
        GameState.__init__(self)

        self._mario: Mario = Mario('mario')
        self._mario.transform.set_position(Vector3(50, 20, 0))
        self._mario.transform.set_flip_x(True)

        self._gametiles = GameTiles('spr_floor1', 'spr_ladder1')

        self._enemy1 = Enemy_Fire('enemy1')
        self._enemy1.transform.set_position(Vector3(50, 20, 0))

        self._barrel_1 = Barrel('barrel1', Vector3(50, 176, 0))

        self._invis_box1 = InvisBlock('invis1', Vector3(-4, 92, 0), Vector3(8, 216, 1))
        self._invis_box2 = InvisBlock('invis1', Vector3(228, 92, 0), Vector3(8, 216, 1))

        self._oil1 = Oilbarrel('oil1', Vector3(24, 8, 0))

        pass

    def enter(self):
        # FLOORS
        ################
        # First Line
        for i in range(14):
            self._gametiles.add_tile_floor(Vector3(8 * i, 0, 0))

        for i in range(14):
            self._gametiles.add_tile_floor(Vector3(8 * (i + 14), math.floor(i / 2), 0))

        # Backslash line 1
        for i in range(26):
            self._gametiles.add_tile_floor(Vector3(8 * i, 40 - math.floor(i / 2), 0))

        # Forwardslash line 1
        for i in range(26):
            self._gametiles.add_tile_floor(Vector3(8 * i + 16, 60 + math.floor(i / 2), 0))

        # Backslash line 2
        for i in range(26):
            self._gametiles.add_tile_floor(Vector3(8 * i, 106 - math.floor(i / 2), 0))

        # Forwardslash line 2
        for i in range(26):
            self._gametiles.add_tile_floor(Vector3(8 * i + 16, 126 + math.floor(i / 2), 0))

        # Last Line
        for i in range(18):
            self._gametiles.add_tile_floor(Vector3(8 * i, 164, 0))
        for i in range(8):
            self._gametiles.add_tile_floor(Vector3(8 * (i + 18), 163 - math.floor(i / 2), 0))

        # Pauline Line
        for i in range(6):
            self._gametiles.add_tile_floor(Vector3(8 * i + (8 * 11), 192, 0))

        # LADDERS
        ################
        self._gametiles.add_tile_ladder(Vector3(8 * 11, Engine.Config.TILE_SIZE * 1, 0))
        self._gametiles.add_tile_ladder(Vector3(8 * 11, Engine.Config.TILE_SIZE * 2, 0))
        self._gametiles.add_tile_ladder(Vector3(8 * 11, Engine.Config.TILE_SIZE * 3, 0))

        # Extra Blocks
        ColliderManager_2D.get_singleton().add_static_collider(self._invis_box1)
        ColliderManager_2D.get_singleton().add_static_collider(self._invis_box2)
        # ColliderManager_2D.get_singleton().add_static_collider(self._oil1)

        pass

    def exit(self):
        pass

    def update(self, delta_time: float):

        self._gametiles.update(delta_time)

        if self._mario.enabled is True:
            self._mario.update(delta_time)

        if self._enemy1.enabled is True:
            self._enemy1.update(delta_time)

        if self._barrel_1.enabled is True:
            self._barrel_1.update(delta_time)

        if self._oil1.enabled is True:
            self._oil1.update(delta_time)

        # COLLISION
        # -------------------------------------

        # Mario
        ColliderManager_2D.get_singleton().process_collision_aabb(self._mario,
        self._enemy1, self._barrel_1
        )

        # Others
        ColliderManager_2D.get_singleton().process_collision_aabb(self._enemy1)
        ColliderManager_2D.get_singleton().process_collision_aabb(self._barrel_1,
        )
#
        # Test
        if Engine.Input.get_key(pygame.K_q):
            self._mario.set_state(MarioState_Enum.DEAD)


        # ------------------------------------------

    def draw(self):
        self._gametiles.draw()

        if self._mario.enabled is True:
            self._mario.draw()

        if self._enemy1.enabled is True:
            self._enemy1.draw()

        if self._barrel_1.enabled is True:
            self._barrel_1.draw()

        if self._oil1.enabled is True:
            self._oil1.draw()

        self._invis_box1.draw()
        self._invis_box2.draw()


        _c = ColliderManager_2D.get_singleton()
        _c.draw_chunks()
        pass

    def draw_ui(self, delta_time: float):
        # Data
        _fps: str = '0'
        if delta_time > 0.0:
            _fps = str(round(100.0 / delta_time) / 100.0)

        _camerapos = str(Engine.Camera.position)
        _camerazoom = str(round(Engine.Camera.zoom * 100.0) / 100.0)
        _playerpos = str(round(self._mario.transform.get_position() * 10.0) / 10.0)

        _text = Text(
            'FPS: ' + _fps + '\nCamera Pos: ' + _camerapos + '\nCameraZoom: ' + _camerazoom +
            '\nMario Pos: ' + _playerpos,
            Vector2(-Engine.Config.SCREEN_WIDTH / 2 + 5, +Engine.Config.SCREEN_HEIGHT / 2 - 30),
            38,
            Vector4(0.9, 0.8, 0.88, 1),
            TextAlignment.LEFT,
            48,
            0.5
        )

        _text.draw()
        pass

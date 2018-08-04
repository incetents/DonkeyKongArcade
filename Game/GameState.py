
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# Controls states of Game Class

# Math
import math
import Engine.Camera
import Engine.Collision
import Engine.Storage
import Engine.Input
import Engine.Config
from Engine.Storage import *
from Engine.Collision import *
from Engine.CollisionManager import *
from Engine.Raycast import *
from Engine.Vector import *
# Entities / Sprites
from Engine.Sprite import *
from Engine.Entity import *
from Engine.EntityManager import *
# Misc
from typing import List
import Engine.Graphics
import Engine.Config
# Game
import pygame
from Game.MarioState import *
from Game.Mario import *
from Game.Tile import *
from Game.Ladder import *
from Game.Enemy_Fire import *
from Game.Barrel import *
from Game.Oilbarrel import *
from Game.InvisBlock import *
from Game.DonkeyKong import *
# Text
from Engine.Text import *


ray: Raycast_2D = None

class GameState:
    def __init__(self):
        # Reset Collision System
        ColliderManager_2D.get_singleton().clear()
        # Reset Current List of Entities
        EntityManager_2D.get_singleton().clear()
        # Mario is global#
        self._mario: Mario = None
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # Update Entities
        EntityManager_2D.get_singleton().update(delta_time)
        pass

    def draw(self):
        # Draw Entities
        EntityManager_2D.get_singleton().draw()
        pass

    def draw_ui(self, delta_time: float):
        pass


class GameState_Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.test = Tile('dk', 'spr_dk_center', Vector3())
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        super().update(delta_time)
        pass

    def draw(self):
        super().draw()
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

        # Special Entities
        self._floor_tiles = TileBatch('batch_tiles1', 'spr_floor1', Collision_Type.PLATFORM)
        # Ladders
        # self._ladders: List[Entity_2D] = []

        # Entities
        self._mario: Mario = Mario('mario')
        self._mario.transform.set_position(Vector3(50, 20, 0))
        self._mario.transform.set_flip_x(True)

        self._enemy1 = Enemy_Fire('enemy1', Vector3(120, 20, 0))

        self._barrel_1 = Barrel('barrel1', Vector3(50, 172 + 5, 0))

        self._invis_box1 = InvisBlock('invis1', Vector3(-12, 92, 0), Vector3(8, 216, 1))
        self._invis_box2 = InvisBlock('invis2', Vector3(236, 92, 0), Vector3(8, 216, 1))

        self._oil1 = Oilbarrel('oil1', Vector3(24, 8, 0))

        self._stack_barrels = Tile('stack_o_barrels', 'spr_barrel_stack1', Vector3(0, 172, 0))
        self._stack_barrels.collision.offset = Vector2(10, 16)
        self._stack_barrels.collision.type = Collision_Type.TRIGGER
        self._stack_barrels.collision.id = Engine.Config.TRIGGER_ID_DEATH

        self._dk = DonkeyKong('dk', Vector3(42, 172, 0))

        # FLOORS
        ################
        # First Line
        for i in range(14):
            self._floor_tiles.add_tile(Vector3(8 * i, 0, 0))

        for i in range(14):
            self._floor_tiles.add_tile(Vector3(8 * (i + 14), math.floor(i / 2), 0))

        # Backslash line 1
        for i in range(26):
            self._floor_tiles.add_tile(Vector3(8 * i, 40 - math.floor(i / 2), 0))

        # Forwardslash line 1
        for i in range(26):
            self._floor_tiles.add_tile(Vector3(8 * i + 16, 60 + math.floor(i / 2), 0))

        # Backslash line 2
        for i in range(26):
            self._floor_tiles.add_tile(Vector3(8 * i, 106 - math.floor(i / 2), 0))

        # Forwardslash line 2
        for i in range(26):
            self._floor_tiles.add_tile(Vector3(8 * i + 16, 126 + math.floor(i / 2), 0))

        # Last Line
        for i in range(18):
            self._floor_tiles.add_tile(Vector3(8 * i, 164, 0))
        for i in range(8):
            self._floor_tiles.add_tile(Vector3(8 * (i + 18), 163 - math.floor(i / 2), 0))

        # Pauline Line
        for i in range(6):
            self._floor_tiles.add_tile(Vector3(8 * i + (8 * 11), 192, 0))

        # LADDERS
        ################
        self._ladders: List[Ladder] = []
        self._ladders.append(Ladder('ladder' + str(1), 'spr_ladder_52', Vector3(64, 172, 0)))
        self._ladders.append(Ladder('ladder' + str(2), 'spr_ladder_52', Vector3(80, 172, 0)))

        # Extra Blocks#

        EntityManager_2D.get_singleton().add_entity(self._enemy1)
        EntityManager_2D.get_singleton().add_entity(self._barrel_1)
        EntityManager_2D.get_singleton().add_entity(self._invis_box1)
        EntityManager_2D.get_singleton().add_entity(self._invis_box2)
        EntityManager_2D.get_singleton().add_entity(self._oil1)
        EntityManager_2D.get_singleton().add_entity(self._stack_barrels)
        EntityManager_2D.get_singleton().add_entity(self._dk)

        EntityManager_2D.get_singleton().add_entity_list(self._ladders)

        EntityManager_2D.get_singleton().add_batch(self._floor_tiles)

        EntityManager_2D.get_singleton().add_entity(self._mario)
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # Base
        super().update(delta_time)

        # Debug Mode
        if Engine.Input.get_key(pygame.K_n):
            self._mario.debug = True
        if Engine.Input.get_key(pygame.K_m):
            self._mario.debug = False

        # TEST
        if Engine.Input.get_key(pygame.K_z):
            self._oil1.spawn_fire()

        # Test
        if Engine.Input.get_key(pygame.K_q):
            self._mario.set_state(MarioState_Enum.DEAD)


        # ------------------------------------------

    def draw(self):

        # Base
        super().draw()

        # Chunk outlines
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

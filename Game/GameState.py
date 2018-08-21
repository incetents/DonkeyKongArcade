
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
from Game.Enemy_Fire import *
from Game.Barrel import *
from Game.Oilbarrel import *
from Game.InvisBlock import *
from Game.DonkeyKong import *
import Game.Barrel
from Game.GameHud import *
from Game.BonusTimer import *
# Text
from Engine.Text import *


ray: Raycast_2D = None

class GameState:
    def __init__(self):
        # Reset Collision System
        ColliderManager_2D.get_singleton().clear()
        # Reset Current List of Entities
        EntityManager.get_singleton().clear()
        # Mario is global#
        self._mario: Mario = None
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time: float):
        # Update Entities
        EntityManager.get_singleton().update(delta_time)
        pass

    def draw(self):
        # Draw Entities
        EntityManager.get_singleton().draw()
        pass

    def draw_debug(self, delta_time: float):
        pass


class GameState_Menu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.test = Tile('test', 'spr_barrel_stack1', Vector3())
        EntityManager.get_singleton().add_entity(self.test)
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

    def draw_debug(self, delta_time: float):
        pass


class GameState_Intro(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.test = Tile('test', 'spr_ladder_52', Vector3())
        EntityManager.get_singleton().add_entity(self.test)
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

    def draw_debug(self, delta_time: float):
        pass


class GameState_Ready(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.test = Tile('test', 'spr_ladder_52', Vector3())
        EntityManager.get_singleton().add_entity(self.test)
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

    def draw_debug(self, delta_time: float):
        pass


class GameState_Game(GameState):
    def __init__(self):
        GameState.__init__(self)

        # Audio
        self._level_music: Song = Engine.Storage.get(Engine.Storage.Type.SONG, 'music_25m')

        # Special Entities
        self._floor_tiles = TileBatch(
            'batch_tiles1', 'floor1', Collision_Type.PLATFORM, Engine.Config.TRIGGER_ID_FLOOR)

        self._ladder_tiles = TileBatch(
            'batch_tiles2', 'ladder1', Collision_Type.TRIGGER, Engine.Config.TRIGGER_ID_LADDER)

        # Entities
        self._mario: Mario = Mario('mario')
        self._mario.transform.set_position(Vector3(50, 20, 0))
        self._mario.set_layer(2)
        self._mario.transform.set_flip_x(True)

        # Bonus timer
        self._bonus_time: BonusTime = BonusTime('bonus_timer')

        # self._enemy1 = Enemy_Fire('enemy1', Vector3(120, 20, 0))
        # self._barrel_1 = Barrel('barrel1', Vector3(80, 16, -2), Direction.LEFT)


        self._invis_box1 = InvisBlock('invis1', Vector3(-12, 92, 0), Vector3(8, 216, 1))
        self._invis_box2 = InvisBlock('invis2', Vector3(236, 92, 0), Vector3(8, 216, 1))

        self._oil = Oilbarrel('oil1', Vector3(24, 8, 0))

        self._destroy_barrel_trig = InvisBlock('trig_destroy_barrel',
                                               self._oil.transform.get_position() + Vector3(-12, -8, 0),
                                               Vector3(16, 16, 1)
                                               )
        self._destroy_barrel_trig.collision.type = Collision_Type.TRIGGER
        self._destroy_barrel_trig.collision.id = Engine.Config.TRIGGER_ID_BARREL_DESTROY

        self._stack_barrels = Tile('stack_o_barrels', 'spr_barrel_stack1', Vector3(0, 172, 0))
        self._stack_barrels.collision.offset = Vector2(10, 16)
        self._stack_barrels.collision.type = Collision_Type.TRIGGER
        self._stack_barrels.collision.id = Engine.Config.TRIGGER_ID_DEATH

        self._dk = DonkeyKong('dk', Vector3(42, 172, 0))
        self._dk.set_layer(-2)

        # SPECIAL
        GameData.get_singleton().global_mario = self._mario
        GameData.get_singleton().global_dk = self._dk
        GameData.get_singleton().global_oil = self._oil

        Game.Barrel.oil_barrel_ref = self._oil
        Game.Barrel.mario_ref = self._mario

        # FLOORS
        ################
        # First Line
        self._floor_tiles.add_tile(Vector3(0, 0, 0), 'spr_floor_red_14')

        for i in range(7):
            self._floor_tiles.add_tile(Vector3(112 + (i * 16), i + 1, 0), 'spr_floor_red_2')

        # Backslash line 1
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i, 40 - i, 0), 'spr_floor_red_2')

        # Forwardslash line 1
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i + 16, 61 + i, 0), 'spr_floor_red_2')

        # Backslash line 2
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i, 106 - i, 0), 'spr_floor_red_2')

        # Forwardslash line 2
        for i in range(13):
            self._floor_tiles.add_tile(Vector3(16 * i + 16, 127 + i, 0), 'spr_floor_red_2')

        # Last Line
        self._floor_tiles.add_tile(Vector3(0, 164, 0), 'spr_floor_red_18')

        for i in range(4):
            self._floor_tiles.add_tile(Vector3(16 * i + 144, 163 - i, 0), 'spr_floor_red_2')

        # Pauline Line
        self._floor_tiles.add_tile(Vector3(88, 192, 0), 'spr_floor_red_6')

        # LADDERS
        ################

        # DEBUG
        self._ladder_tiles.add_tile(Vector3(112, 9, 0), 'spr_ladder_24')

        # Ladder 1
        self._ladder_tiles.add_tile(Vector3(80, 8, 0), 'spr_ladder_8')
        self._ladder_tiles.add_tile(Vector3(80, 32, 0), 'spr_ladder_3')
        # Ladder 2
        self._ladder_tiles.add_tile(Vector3(184, 13, 0), 'spr_ladder_16')
        # Ladder 3
        self._ladder_tiles.add_tile(Vector3(96, 42, 0), 'spr_ladder_24')
        # Ladder 4
        self._ladder_tiles.add_tile(Vector3(32, 46, 0), 'spr_ladder_16')
        # Ladder 5
        self._ladder_tiles.add_tile(Vector3(64, 72, 0), 'spr_ladder_8')
        self._ladder_tiles.add_tile(Vector3(64, 96, 0), 'spr_ladder_6')
        # Ladder 6
        self._ladder_tiles.add_tile(Vector3(112, 75, 0), 'spr_ladder_24')
        # Ladder 7
        self._ladder_tiles.add_tile(Vector3(184, 79, 0), 'spr_ladder_16')
        # Ladder 8
        self._ladder_tiles.add_tile(Vector3(168, 104, 0), 'spr_ladder_8')
        self._ladder_tiles.add_tile(Vector3(168, 128, 0), 'spr_ladder_8')
        # Ladder 9
        self._ladder_tiles.add_tile(Vector3(72, 110, 0), 'spr_ladder_20')
        # Ladder 10
        self._ladder_tiles.add_tile(Vector3(32, 112, 0), 'spr_ladder_16')
        # Ladder 11
        self._ladder_tiles.add_tile(Vector3(88, 139, 0), 'spr_ladder_13')
        self._ladder_tiles.add_tile(Vector3(88, 160, 0), 'spr_ladder_4')
        # Ladder 12
        self._ladder_tiles.add_tile(Vector3(184, 145, 0), 'spr_ladder_16')
        # Ladder 13
        self._ladder_tiles.add_tile(Vector3(128, 172, 0), 'spr_ladder_20')
        # Ladder DK
        self._ladder_tiles.add_tile(Vector3(64, 172, 0), 'spr_ladder_52')
        self._ladder_tiles.add_tile(Vector3(80, 172, 0), 'spr_ladder_52')

        pass

    def enter(self):
        # Game Audio
        AudioPlayer.stop_all_audio()
        AudioPlayer.get_singleton().set_song('music_25m', -1).play_song()
        # Game Hud
        GameHud.get_singleton().update_lives()
        # Add entities
        EntityManager.get_singleton().add_entity(self._invis_box1)
        EntityManager.get_singleton().add_entity(self._invis_box2)
        EntityManager.get_singleton().add_entity(self._oil)
        EntityManager.get_singleton().add_entity(self._destroy_barrel_trig)
        EntityManager.get_singleton().add_entity(self._stack_barrels)
        EntityManager.get_singleton().add_entity(self._dk)
        EntityManager.get_singleton().add_entity(self._bonus_time)

        EntityManager.get_singleton().add_batch(self._floor_tiles)
        EntityManager.get_singleton().add_batch(self._ladder_tiles)

        EntityManager.get_singleton().add_entity(self._mario)

        # Game Data
        GameData.get_singleton().init_level_time()
        pass

    def exit(self):
        AudioPlayer.stop_all_audio()
        pass

    def update(self, delta_time: float):
        # Game Data
        GameData.get_singleton().update_level_time()

        # Base
        #print('~~~')
        #_t = pygame.time.get_ticks()
        super().update(delta_time)
        #print('update time:', pygame.time.get_ticks() - _t)

        # Debug Mode
        if Engine.Input.get_key(pygame.K_n):
            self._mario.set_debug(True)
        if Engine.Input.get_key(pygame.K_m):
            self._mario.set_debug(False)

        # TEST
        if Engine.Input.get_key_pressed(pygame.K_z):
            self._dk.spawn_barrel()
            # self._oil.spawn_fire()

        # Test
        if Engine.Input.get_key_pressed(pygame.K_q):
            self._mario.set_state(MarioState_Enum.DEAD)

        if Engine.Input.get_key_pressed(pygame.K_x):
            self._mario.set_state(MarioState_Enum.CLIMB)

        # ------------------------------------------

    def draw(self):
        # Base
        # print('~~~')
        # _t = pygame.time.get_ticks()
        super().draw()
        # print('draw time:', pygame.time.get_ticks() - _t)

        # Chunk outlines
        _c = ColliderManager_2D.get_singleton()
        _c.draw_chunks()

        # Debug Art from Entities
        EntityManager.get_singleton().draw_debug()

        # ------------------------------------------

    # Non-camera space debug graphics
    def draw_debug(self, delta_time: float):

        # Data
        _fps: str = '0'
        if delta_time > 0.0:
            _fps = str(round(100.0 / delta_time) / 100.0)

        _camerapos = str(Engine.Camera.position)
        _camerazoom = str(round(Engine.Camera.zoom * 100.0) / 100.0)
        _playerpos = str(round(self._mario.transform.get_position() * 10.0) / 10.0)

        _text = GameText(
            'FPS: ' + _fps + '\nCamera Pos: ' + _camerapos + '\nCameraZoom: ' + _camerazoom +
            '\nMario Pos: ' + _playerpos,
            Vector2(-Engine.Config.SCREEN_WIDTH / 2 + 5, +Engine.Config.SCREEN_HEIGHT / 2 - 30),
            38,
            Vector4(0.2, 0.9, 0.22, 1),
            TextAlignment.LEFT,
            48,
            0.5
        )

        _text.draw()
        # ------------------------------------------

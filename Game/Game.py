
# Emmanuel Lajeunesse ©2018 - Using PyGame and PyOpenGL

# [Main Game Functionality Goes Here]

# from __future__ import annotations
import pygame

# Textures
from Engine.Texture import *
# Sprites
from Engine.Sprite import *
# Math
import math
import Engine.Camera
import Engine.Sprite
from Engine.Anchor import *
from Engine.Vector import *
from Engine.Collision import *
from Engine.Transform import *
import Engine.Collision
from Engine.CollisionManager import *
from Engine.Rigidbody import *
# Data
import Engine.Input
import Engine.Storage
from Engine.Text import *
from Engine.Graphics import *

# Entities
from Engine.Entity import *
from Game.Mario import *
from Game.Tile import *
from Game.GameHud import *

# Misc
from typing import List
from OpenGL.GL import *
import Engine.Config
from Engine.AudioPlayer import *

from Game.GameState import *

_instance = None


class Game:
    def __init__(self):
        # State
        self._state = None
        self.is_setup: bool = False

    def setup(self):
        # State
        self._state = GameState()
        # Setup Functions
        self.setup_audio()
        self.setup_textures()
        self.setup_sprites()
        self.setup_animations()
        self.setup_meshes()
        # Setup Hud
        GameHud.get_singleton().setup()
        # Initial State
        self.set_state(GameState_Game())
        self.is_setup = True

    @staticmethod
    def get_singleton():
        global _instance
        if _instance is None:
            _instance = Game()
        return _instance

    def set_state(self, _new_state: GameState):
        self._state.exit()
        self._state = _new_state
        self._state.enter()

    def get_state(self) -> GameState:
        return self._state

    def setup_audio(self):
        # Load Audio (music)
        Song('music_25m', 'audio/music_25m.wav')
        Song('music_50m', 'audio/music_50m.mp3')
        Song('music_75m', 'audio/music_75m.mp3')
        Song('music_100m', 'audio/music_100m.mp3')
        # Load Audio (sound effects)
        SFX('sfx_jump', 'audio/sfx_jump.wav')
        SFX('sfx_walk1', 'audio/sfx_walk1.wav')
        SFX('sfx_walk2', 'audio/sfx_walk2.wav')
        SFX('sfx_walk3', 'audio/sfx_walk3.wav')
        SFX('sfx_walk4', 'audio/sfx_walk4.wav')
        SFX('sfx_walk5', 'audio/sfx_walk5.wav')
        SFX('sfx_barrel_score', 'audio/sfx_barrel_score.wav')
        SFX('sfx_death', 'audio/sfx_death.wav')

    def setup_textures(self):
        # Font Texture
        Texture('font', 'assets/text/tilesheet.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('numbers', 'assets/numbers/numbers.png', FilterMode.POINT, WrapMode.CLAMP)

        # Special Stuff
        Texture('pixel_black', 'assets/pixels/pixel_black.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_white', 'assets/pixels/pixel_white.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_red', 'assets/pixels/pixel_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_green', 'assets/pixels/pixel_green.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('pixel_blue', 'assets/pixels/pixel_blue.png', FilterMode.POINT, WrapMode.CLAMP)

        # Hud Stuff
        Texture('mini_mario', 'assets/hud/mini_mario.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('bonus_counter', 'assets/hud/bonus_counter.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('highscore1', 'assets/hud/highscore1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('highscore2', 'assets/hud/highscore2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('highscore3', 'assets/hud/highscore3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('life_icon', 'assets/hud/life_icon.png', FilterMode.POINT, WrapMode.CLAMP)

        # Game Stuff
        Texture('score_100', 'assets/effects/score_100.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('score_200', 'assets/effects/score_200.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('score_300', 'assets/effects/score_300.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('score_500', 'assets/effects/score_500.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('score_800', 'assets/effects/score_800.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('dk_center', 'assets/dk/dk1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_left', 'assets/dk/dk2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_drop', 'assets/dk/dk3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_pound', 'assets/dk/dk4.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_climb1', 'assets/dk/dk5.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_climb2', 'assets/dk/dk6.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_hold1', 'assets/dk/dk7.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('dk_hold2', 'assets/dk/dk8.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('mario1',     'assets/mario/mario1.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario2',     'assets/mario/mario2.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario3',     'assets/mario/mario3.png',     FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_jump', 'assets/mario/mario_jump.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_death1', 'assets/mario/mario_death1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_death2', 'assets/mario/mario_death2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_dead', 'assets/mario/mario_dead.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_climb1', 'assets/mario/mario_climb1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_climb2', 'assets/mario/mario_climb2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_climb3', 'assets/mario/mario_climb3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_climb4', 'assets/mario/mario_climb4.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('mario_climb5', 'assets/mario/mario_climb5.png', FilterMode.POINT, WrapMode.CLAMP)

        # Idle hammer
        Texture('hammer_idle1_red', 'assets/mario_hammer/idle1_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_idle2_red', 'assets/mario_hammer/idle2_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_idle1_yellow', 'assets/mario_hammer/idle1_yellow.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_idle2_yellow', 'assets/mario_hammer/idle2_yellow.png', FilterMode.POINT, WrapMode.CLAMP)
        # Walk with hammer
        Texture('hammer_walk1_red', 'assets/mario_hammer/walk1_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk2_red', 'assets/mario_hammer/walk2_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk3_red', 'assets/mario_hammer/walk3_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk4_red', 'assets/mario_hammer/walk4_red.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk1_yellow', 'assets/mario_hammer/walk1_yellow.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk2_yellow', 'assets/mario_hammer/walk2_yellow.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk3_yellow', 'assets/mario_hammer/walk3_yellow.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('hammer_walk4_yellow', 'assets/mario_hammer/walk4_yellow.png', FilterMode.POINT, WrapMode.CLAMP)


        Texture('floor1', 'assets/tiles/floor1.png', FilterMode.POINT, WrapMode.REPEAT)
        Texture('ladder1', 'assets/tiles/ladder1.png', FilterMode.POINT, WrapMode.REPEAT)

        Texture('hammer', 'assets/objects/hammer.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('barrel_side1', 'assets/objects/barrel_side1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_side2', 'assets/objects/barrel_side2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel', 'assets/objects/barrel.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_side1_blue', 'assets/objects/barrel_side1_blue.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_side2_blue', 'assets/objects/barrel_side2_blue.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_blue', 'assets/objects/barrel_blue.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_vertical', 'assets/objects/barrel_vertical.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('barrel_stack', 'assets/objects/stacked_barrels.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('fire_barrel1', 'assets/enemies/fire_barrel1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel2', 'assets/enemies/fire_barrel2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel3', 'assets/enemies/fire_barrel3.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel4', 'assets/enemies/fire_barrel4.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_barrel5', 'assets/enemies/fire_barrel5.png', FilterMode.POINT, WrapMode.CLAMP)

        Texture('fire1', 'assets/enemies/fire1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire2', 'assets/enemies/fire2.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_blue1', 'assets/enemies/fire_blue1.png', FilterMode.POINT, WrapMode.CLAMP)
        Texture('fire_blue2', 'assets/enemies/fire_blue2.png', FilterMode.POINT, WrapMode.CLAMP)

    def setup_sprites(self):
        # Load Sprites
        Sprite('spr_pixel_black', 'pixel_black')
        Sprite('spr_pixel_white', 'pixel_white')
        Sprite('spr_pixel_red', 'pixel_red')
        Sprite('spr_pixel_green', 'pixel_green')
        Sprite('spr_pixel_blue', 'pixel_blue')

        # Hud
        Sprite('spr_mini_mario', 'mini_mario', Anchor.BOTLEFT)
        Sprite('spr_bonus_counter', 'bonus_counter', Anchor.BOTLEFT)
        Sprite('spr_highscore1', 'highscore1', Anchor.BOTLEFT)
        Sprite('spr_highscore2', 'highscore2', Anchor.BOTLEFT)
        Sprite('spr_highscore3', 'highscore3', Anchor.BOTLEFT)
        Sprite('spr_life_icon', 'life_icon', Anchor.BOTLEFT)

        # Game
        Sprite('spr_score_100', 'score_100', Anchor.BOT)
        Sprite('spr_score_200', 'score_200', Anchor.BOT)
        Sprite('spr_score_300', 'score_300', Anchor.BOT)
        Sprite('spr_score_500', 'score_500', Anchor.BOT)
        Sprite('spr_score_800', 'score_800', Anchor.BOT)

        Sprite('spr_dk_center', 'dk_center', Anchor.BOT)
        Sprite('spr_dk_left', 'dk_left', Anchor.BOT)
        Sprite('spr_dk_right', 'dk_left', Anchor.BOT).set_flip_x(True)
        Sprite('spr_dk_drop', 'dk_drop', Anchor.BOT)
        Sprite('spr_dk_hold_barrel1', 'dk_hold1', Anchor.BOT)
        Sprite('spr_dk_hold_barrel2', 'dk_hold2', Anchor.BOT)

        # Mario
        Sprite('spr_mario1', 'mario1', Anchor.BOT)
        Sprite('spr_mario2', 'mario2', Anchor.BOT)
        Sprite('spr_mario3', 'mario3', Anchor.BOT)
        Sprite('spr_mario_jump', 'mario_jump', Anchor.BOT)
        Sprite('spr_mario_death1', 'mario_death1', Anchor.BOT)
        Sprite('spr_mario_death2', 'mario_death2', Anchor.BOT).set_flip_x(True)
        Sprite('spr_mario_death3', 'mario_death1', Anchor.BOT).set_flip_y(True)
        Sprite('spr_mario_death4', 'mario_death2', Anchor.BOT)
        Sprite('spr_mario_dead', 'mario_dead', Anchor.BOT)
        Sprite('spr_mario_climb1', 'mario_climb1', Anchor.BOT)
        Sprite('spr_mario_climb2', 'mario_climb2', Anchor.BOT)
        Sprite('spr_mario_climb3', 'mario_climb3', Anchor.BOT)
        Sprite('spr_mario_climb4', 'mario_climb4', Anchor.BOT)
        Sprite('spr_mario_climb5', 'mario_climb5', Anchor.BOT)
        # Mario Hammer
        Sprite('spr_hammer_idle1_red', 'hammer_idle1_red', Anchor.BOT)
        Sprite('spr_hammer_idle2_red', 'hammer_idle2_red', Anchor.BOT)
        Sprite('spr_hammer_idle1_yellow', 'hammer_idle1_yellow', Anchor.BOT)
        Sprite('spr_hammer_idle2_yellow', 'hammer_idle2_yellow', Anchor.BOT)
        Sprite('spr_hammer_walk1_red', 'hammer_walk1_red', Anchor.BOT)
        Sprite('spr_hammer_walk2_red', 'hammer_walk2_red', Anchor.BOT)
        Sprite('spr_hammer_walk3_red', 'hammer_walk3_red', Anchor.BOT)
        Sprite('spr_hammer_walk4_red', 'hammer_walk4_red', Anchor.BOT)
        Sprite('spr_hammer_walk1_yellow', 'hammer_walk1_yellow', Anchor.BOT)
        Sprite('spr_hammer_walk2_yellow', 'hammer_walk2_yellow', Anchor.BOT)
        Sprite('spr_hammer_walk3_yellow', 'hammer_walk3_yellow', Anchor.BOT)
        Sprite('spr_hammer_walk4_yellow', 'hammer_walk4_yellow', Anchor.BOT)

        Sprite('spr_floor_red_1', 'floor1', Anchor.BOTLEFT)
        Sprite('spr_floor_red_2', 'floor1', Anchor.BOTLEFT).set_scale_x(2.0).set_uv_right(2.0)
        Sprite('spr_floor_red_6', 'floor1', Anchor.BOTLEFT).set_scale_x(6.0).set_uv_right(6.0)
        Sprite('spr_floor_red_14', 'floor1', Anchor.BOTLEFT).set_scale_x(14.0).set_uv_right(14.0)
        Sprite('spr_floor_red_18', 'floor1', Anchor.BOTLEFT).set_scale_x(18.0).set_uv_right(18.0)

        Sprite('spr_ladder_52', 'ladder1', Anchor.BOTLEFT).set_scale_y(52.0 / 8.0).set_uv_top(52.0 / 8.0)
        Sprite('spr_ladder_24', 'ladder1', Anchor.BOTLEFT).set_scale_y(24.0 / 8.0).set_uv_top(24.0 / 8.0)
        Sprite('spr_ladder_20', 'ladder1', Anchor.BOTLEFT).set_scale_y(20.0 / 8.0).set_uv_top(20.0 / 8.0)
        Sprite('spr_ladder_16', 'ladder1', Anchor.BOTLEFT).set_scale_y(16.0 / 8.0).set_uv_top(16.0 / 8.0)
        Sprite('spr_ladder_13', 'ladder1', Anchor.BOTLEFT).set_scale_y(13.0 / 8.0).set_uv_top(13.0 / 8.0)
        Sprite('spr_ladder_8', 'ladder1', Anchor.BOTLEFT)
        Sprite('spr_ladder_6', 'ladder1', Anchor.BOTLEFT).set_scale_y(6.0 / 8.0).set_uv_top(6.0 / 8.0)
        Sprite('spr_ladder_4', 'ladder1', Anchor.BOTLEFT).set_scale_y(4.0 / 8.0).set_uv_top(4.0 / 8.0)
        Sprite('spr_ladder_3', 'ladder1', Anchor.BOTLEFT).set_scale_y(3.0 / 8.0).set_uv_top(3.0 / 8.0)

        Sprite('spr_fire_barrel1', 'fire_barrel1', Anchor.BOT)
        Sprite('spr_fire_barrel2', 'fire_barrel2', Anchor.BOT)
        Sprite('spr_fire_barrel3', 'fire_barrel3', Anchor.BOT)
        Sprite('spr_fire_barrel4', 'fire_barrel4', Anchor.BOT)
        Sprite('spr_fire_barrel5', 'fire_barrel5', Anchor.BOT)

        Sprite('spr_barrel_side1', 'barrel_side1', Anchor.BOT)
        Sprite('spr_barrel_side2', 'barrel_side2', Anchor.BOT)
        Sprite('spr_barrel_1', 'barrel', Anchor.BOT)
        Sprite('spr_barrel_2', 'barrel', Anchor.BOT).set_flip_x(True)
        Sprite('spr_barrel_3', 'barrel', Anchor.BOT).set_flip_x(True).set_flip_y(True)
        Sprite('spr_barrel_4', 'barrel', Anchor.BOT).set_flip_y(True)

        Sprite('spr_barrel_side1_blue', 'barrel_side1_blue', Anchor.BOT)
        Sprite('spr_barrel_side2_blue', 'barrel_side2_blue', Anchor.BOT)
        Sprite('spr_barrel_1_blue', 'barrel_blue', Anchor.BOT)
        Sprite('spr_barrel_2_blue', 'barrel_blue', Anchor.BOT).set_flip_x(True)
        Sprite('spr_barrel_3_blue', 'barrel_blue', Anchor.BOT).set_flip_x(True).set_flip_y(True)
        Sprite('spr_barrel_4_blue', 'barrel_blue', Anchor.BOT).set_flip_y(True)

        Sprite('spr_barrel_vertical', 'barrel_vertical')
        Sprite('spr_barrel_stack1', 'barrel_stack', Anchor.BOTLEFT)

        Sprite('spr_enemy_fire1', 'fire1')
        Sprite('spr_enemy_fire2', 'fire2')

    def setup_animations(self):
        # Load Animations
        SpriteSequence('anim_mario_idle',
                        'spr_mario1'
                        )
        SpriteSequence('anim_mario_walk',
                        'spr_mario1',
                        'spr_mario2',
                        'spr_mario2',
                        'spr_mario1',
                        'spr_mario3',
                        'spr_mario3'
                        )
        SpriteSequence('anim_mario_jump',
                        'spr_mario_jump'
                        )
        SpriteSequence('anim_mario_dying',
                        'spr_mario_death1',
                        'spr_mario_death2',
                        'spr_mario_death3',
                        'spr_mario_death4'
                        )
        SpriteSequence('anim_mario_dead',
                        'spr_mario_dead'
                        )
        SpriteSequence('anim_mario_climb',
                       'spr_mario_climb1',
                       'spr_mario_climb2',
                       'spr_mario_climb3',
                       'spr_mario_climb4',
                       'spr_mario_climb5'
                       )

        SpriteSequence('anim_mario_hammer_idle_red',
                       'spr_hammer_idle1_red',
                       'spr_hammer_idle2_red'
                       )
        SpriteSequence('anim_mario_hammer_idle_yellow',
                       'spr_hammer_idle1_yellow',
                       'spr_hammer_idle2_yellow'
                       )

        # Sprite('spr_hammer_idle1_red', 'hammer_idle1_red', Anchor.BOT)
        # Sprite('spr_hammer_idle2_red', 'hammer_idle2_red', Anchor.BOT)
        # Sprite('spr_hammer_idle1_yellow', 'hammer_idle1_yellow', Anchor.BOT)
        # Sprite('spr_hammer_idle2_yellow', 'hammer_idle2_yellow', Anchor.BOT)
        # Sprite('spr_hammer_walk1_red', 'hammer_walk1_red', Anchor.BOT)
        # Sprite('spr_hammer_walk2_red', 'hammer_walk2_red', Anchor.BOT)
        # Sprite('spr_hammer_walk3_red', 'hammer_walk3_red', Anchor.BOT)
        # Sprite('spr_hammer_walk4_red', 'hammer_walk4_red', Anchor.BOT)
        # Sprite('spr_hammer_walk1_yellow', 'hammer_walk1_yellow', Anchor.BOT)
        # Sprite('spr_hammer_walk2_yellow', 'hammer_walk2_yellow', Anchor.BOT)
        # Sprite('spr_hammer_walk3_yellow', 'hammer_walk3_yellow', Anchor.BOT)
        # Sprite('spr_hammer_walk4_yellow', 'hammer_walk4_yellow', Anchor.BOT)


        SpriteSequence('anim_dk_frames',
                       'spr_dk_center',
                       'spr_dk_left',
                       'spr_dk_right',
                       'spr_dk_hold_barrel1',
                       'spr_dk_hold_barrel2',
                       'spr_dk_drop'
                       )

        SpriteSequence('anim_oil_barrel_empty',
                       'spr_fire_barrel5',
                       )
        SpriteSequence('anim_oil_barrel_normal',
                       'spr_fire_barrel1',
                       'spr_fire_barrel2'
                       )
        SpriteSequence('anim_oil_barrel_burn',
                       'spr_fire_barrel3',
                       'spr_fire_barrel4',
                       )

        SpriteSequence('anim_barrel_roll',
                       'spr_barrel_1',
                       'spr_barrel_2',
                       'spr_barrel_3',
                       'spr_barrel_4'
                       )
        SpriteSequence('anim_barrel_fall',
                       'spr_barrel_side1',
                       'spr_barrel_side2'
                       )
        SpriteSequence('anim_barrel_roll_blue',
                       'spr_barrel_1_blue',
                       'spr_barrel_2_blue',
                       'spr_barrel_3_blue',
                       'spr_barrel_4_blue'
                       )
        SpriteSequence('anim_barrel_fall_blue',
                       'spr_barrel_side1_blue',
                       'spr_barrel_side2_blue'
                       )

        SpriteSequence('anim_enemy1',
                       'spr_enemy_fire1',
                       'spr_enemy_fire2'
                       )

    def setup_meshes(self):
        # Load Meshes
        # _m1 = Mesh('quad_2d')
        # _v = (
        #     Vector3(-0.5, -0.5, 0),
        #     Vector3(+0.5, -0.5, 0),
        #     Vector3(+0.5, +0.5, 0),
        #     Vector3(-0.5, +0.5, 0)
        # )
        # _uv = (
        #     Vector2(0, 0),
        #     Vector2(1, 0),
        #     Vector2(1, 1),
        #     Vector2(0, 1)
        # )
        # _m1.set_vertices(_v)
        # _m1.set_uvs(_uv)
        pass

    def update(self, delta_time: float):

        # State Update
        self._state.update(delta_time)

        # Move Camera
        if Engine.Input.get_key(pygame.K_w):
            Engine.Camera.move_up()
        elif Engine.Input.get_key(pygame.K_s):
            Engine.Camera.move_down()
        if Engine.Input.get_key(pygame.K_a):
            Engine.Camera.move_left()
        elif Engine.Input.get_key(pygame.K_d):
            Engine.Camera.move_right()

        # Mode Switcher
        if Engine.Input.get_key(pygame.K_1):
            self.set_state(GameState_Menu())
        elif Engine.Input.get_key(pygame.K_2):
            self.set_state(GameState_Intro())
        elif Engine.Input.get_key(pygame.K_3):
            self.set_state(GameState_Ready())
        elif Engine.Input.get_key(pygame.K_4):
            self.set_state(GameState_Game())

        # Check if mario dead for level reset
        if type(self._state) is GameState_Game:
            _mario: Mario = self._state._mario
            if not _mario.alive:
                self.set_state(GameState_Game())


    def draw(self):
        Engine.Camera.push()

        # State Draw
        self._state.draw()

        # Draw Hud
        GameHud.get_singleton().draw()

        Engine.Camera.pop()

        # Flush it
        glFlush()

    def draw_debug(self, delta_time):

        # Draw UI
        self._state.draw_debug(delta_time)

    def get_Mario(self) -> Mario:
        return self._state._mario
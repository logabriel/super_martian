"""
ISPPJ1 2024
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Camera import Camera
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player
from src.GameItem import GameItem
from src.Tile import Tile
from src.definitions import tiles


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        (self.spanw_player_x , self.spawn_player_y) = settings.SPAWN_PLAYER[self.level]

        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            pygame.mixer.music.load(
                settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
            )
            pygame.mixer.music.play(loops=-1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            self.player = Player(self.spanw_player_x, self.spawn_player_y, self.game_level)
            self.player.change_state("idle")
        else:
            self.player.game_level = self.game_level
            self.player.tilemap = self.tilemap

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(0, 0, settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.set_collision_boundaries(self.game_level.get_rect())
            self.camera.attach_to(self.player)

        self.clock = enter_params.get("clock")

        if self.clock is None:
            self.clock = Clock(30)

            def countdown_timer():
                self.clock.count_down()

                if 0 < self.clock.time <= 5:
                    settings.SOUNDS["timer"].play()

                if self.clock.time == 0:
                    self.player.change_state("dead")

            Timer.every(1, countdown_timer)
        else:
            Timer.resume()
        
        #Set the golden key and golden block as inactive.
        for item in self.game_level.items:
            if item.texture_id == "key-gold":
                if item.frame_index == 0:
                    self.itemKey = item
                    self.itemKey.active = False
                elif item.frame_index == 8:
                    self.itemBLock = item
                    self.itemBLock.active = False

        self.score_next_level = 200 + self.level*28

    def update(self, dt: float) -> None:
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            Timer.clear()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)

        if self.player.y >= self.player.tilemap.height:
            self.player.change_state("dead")

        self.camera.update()
        self.game_level.set_render_boundaries(self.camera.get_rect())
        self.game_level.update(dt)

        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        for item in self.game_level.items:
            if not item.active or not item.collidable:
                continue

            if self.player.collides(item):
                item.on_collide(self.player)
                item.on_consume(self.player)
        
        if self.player.score >= self.score_next_level:
            self.game_level.winNextLevel = True
            
            self.player.score = 0
            
            pygame.mixer.music.stop()
            settings.SOUNDS["win"].stop()
            settings.SOUNDS["win"].play()

            Timer.clear()
            
            for item in self.game_level.items:
                if not item.frame_index == "Key-gold":
                    item.active = False
            
            self.itemBLock.active = True
            self.itemKey.active = True
            self.generate_item_block()
        
        if self.game_level.winNextLevel:
            if self.itemBLock.collides_on(self.player, GameItem.BOTTOM) and self.player.collision_on_top():
                if not self.itemKey.consumable:
                    def arrive():
                        self.itemKey.consumable = True
                    Timer.tween(
                        1,
                        [ (self.itemKey, {"y": self.itemKey.y - 16})],
                        on_finish=arrive,
                    )

        if self.player.key: #change next level
            self.state_machine.change("transition", player=self.player,level=self.level)

    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)
    
    #Generate a solid block in the first layer
    def generate_item_block(self) -> None:
        item_i = self.tilemap.to_i(self.itemBLock.y)
        item_j = self.tilemap.to_j(self.itemBLock.x)          
        self.tilemap.layers[0][item_i][item_j] = Tile(item_i, item_j, 16, 16, 41, dict(top=True, right=True, bottom=True, left=True))

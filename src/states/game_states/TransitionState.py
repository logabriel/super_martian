from typing import Dict, Any

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Player import Player
from src.GameLevel import GameLevel

class TransitionState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level")
        self.player = enter_params.get("player")

        if self.level == 2:
            self.level = 1
            self.player = None
        else:
            self.level = 2
            self.player.key = False
            self.player.x = settings.SPAWN_PLAYER[self.level][0]
            self.player.y = settings.SPAWN_PLAYER[self.level][1]
            self.player.vx = 0
            self.player.vy = 0
            self.player.change_state("idle")

        pygame.mixer.music.stop()
        pygame.mixer.music.load(
            settings.BASE_DIR / "assets" / "sounds" / "music_intro.ogg"
        )
        pygame.mixer.music.play()
    
    def exit(self) -> None:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 130, 196))

        render_text(
            surface,
            f"Next level {self.level}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            20,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "press enter to continue",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT // 2,
            (197, 195, 198),
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change(
                "play",
                level=self.level,
                player=self.player,
            )
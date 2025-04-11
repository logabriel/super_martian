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
        self.radius = max(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)  # Radio inicial del círculo
        self.transitioning = True  # Indica si la transición está activa

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
    
    def update(self, dt: float) -> None:
        if self.transitioning:
            self.radius -= 500 * dt  # Reducir el radio gradualmente
            if self.radius <= 0:
                self.transitioning = False  # Finalizar la transición

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))  # Fondo negro

        # Dibujar el círculo de transición
        if self.transitioning:
            pygame.draw.circle(
                surface,
                (255, 255, 255),  # Color del círculo
                (settings.VIRTUAL_WIDTH // 2, settings.VIRTUAL_HEIGHT // 2),
                max(0, int(self.radius)),
            )
        else:
            # Mostrar texto cuando la transición termine

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
        if not self.transitioning and input_id == "enter" and input_data.pressed:
            self.state_machine.change(
                "play",
                level=self.level,
                player=self.player,
            )

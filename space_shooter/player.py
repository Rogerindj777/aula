# =============================================================
# player.py — Classe da nave do jogador
# =============================================================

import pygame
from settings import (
    PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    SHOOT_COOLDOWN, CYAN, WHITE, ORANGE
)
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    """Nave controlada pelo jogador.

    Move-se para esquerda/direita com as setas do teclado.
    Atira projéteis pressionando a barra de espaço.
    """

    WIDTH = 48
    HEIGHT = 52

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self._draw_ship()

        self.rect = self.image.get_rect(
            centerx=SCREEN_WIDTH // 2,
            bottom=SCREEN_HEIGHT - 30
        )

        self.last_shot_time = 0

    def _draw_ship(self):
        """Desenha a nave com estética retro."""
        w, h = self.WIDTH, self.HEIGHT

        # Corpo principal — triângulo
        body_points = [
            (w // 2, 4),       # ponta superior
            (4, h - 8),        # base esquerda
            (w - 4, h - 8),    # base direita
        ]
        pygame.draw.polygon(self.image, (20, 60, 120), body_points)
        pygame.draw.polygon(self.image, CYAN, body_points, 2)

        # Cabine — pequeno triângulo interno
        cabin_points = [
            (w // 2, 14),
            (w // 2 - 6, 30),
            (w // 2 + 6, 30),
        ]
        pygame.draw.polygon(self.image, (60, 180, 255), cabin_points)

        # Asas laterais
        left_wing = [(4, h - 8), (0, h), (16, h - 8)]
        right_wing = [(w - 4, h - 8), (w, h), (w - 16, h - 8)]
        pygame.draw.polygon(self.image, (15, 50, 100), left_wing)
        pygame.draw.polygon(self.image, CYAN, left_wing, 2)
        pygame.draw.polygon(self.image, (15, 50, 100), right_wing)
        pygame.draw.polygon(self.image, CYAN, right_wing, 2)

        # Propulsor — brilho na base
        thruster_rect = pygame.Rect(w // 2 - 4, h - 6, 8, 6)
        pygame.draw.rect(self.image, ORANGE, thruster_rect, border_radius=2)

    def update(self):
        """Movimenta a nave com base nas teclas pressionadas."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Impede que a nave saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, bullet_group: pygame.sprite.Group) -> bool:
        """Dispara um projétil se o cooldown permitir.

        Returns:
            True se o tiro foi disparado, False caso contrário.
        """
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= SHOOT_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot_time = now
            return True
        return False

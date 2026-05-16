# =============================================================
# bullet.py — Classe dos projéteis disparados pela nave
# =============================================================

import pygame
from settings import BULLET_SPEED, CYAN, SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):
    """Projétil disparado pela nave do jogador.

    Move-se para cima a cada frame e se auto-destrói
    ao sair da tela.
    """

    WIDTH = 4
    HEIGHT = 14

    def __init__(self, x: int, y: int):
        super().__init__()

        # Cria a superfície do projétil com brilho
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # Núcleo brilhante
        pygame.draw.rect(self.image, CYAN, (0, 0, self.WIDTH, self.HEIGHT),
                         border_radius=2)

        # Brilho central mais claro
        core_color = (180, 255, 255)
        pygame.draw.rect(self.image, core_color, (1, 2, 2, self.HEIGHT - 4),
                         border_radius=1)

        self.rect = self.image.get_rect(centerx=x, bottom=y)

    def update(self):
        """Move o projétil para cima e remove se sair da tela."""
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

# =============================================================
# asteroid.py — Classe dos asteroides
# =============================================================

import math
import random
import pygame
from settings import (
    ASTEROID_SPEED_INITIAL, SCREEN_WIDTH, SCREEN_HEIGHT,
    ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS,
    DARK_GRAY, RED, ORANGE
)


class Asteroid(pygame.sprite.Sprite):
    """Asteroide que surge no topo da tela e desce.

    Cada asteroide tem formato irregular gerado aleatoriamente,
    simulando rochas espaciais no estilo Atari.
    """

    def __init__(self, speed: float = ASTEROID_SPEED_INITIAL):
        super().__init__()

        self.speed = speed
        self.radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        size = self.radius * 2 + 4  # margem para o contorno

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self._draw_asteroid(size)

        self.rect = self.image.get_rect(
            centerx=random.randint(self.radius, SCREEN_WIDTH - self.radius),
            bottom=0
        )

    def _draw_asteroid(self, size: int):
        """Desenha um asteroide com formato rochoso irregular."""
        center = size // 2
        num_vertices = random.randint(8, 12)
        points = []

        for i in range(num_vertices):
            angle = (2 * math.pi / num_vertices) * i
            # Variação aleatória no raio para criar irregularidade
            variation = random.uniform(0.7, 1.0)
            r = self.radius * variation
            x = center + r * math.cos(angle)
            y = center + r * math.sin(angle)
            points.append((x, y))

        # Corpo do asteroide
        pygame.draw.polygon(self.image, DARK_GRAY, points)

        # Contorno
        border_color = (100, 90, 110)
        pygame.draw.polygon(self.image, border_color, points, 2)

        # Crateras decorativas (2-3 pequenos círculos escuros)
        num_craters = random.randint(2, 3)
        for _ in range(num_craters):
            crater_r = random.randint(2, max(3, self.radius // 6))
            cx = center + random.randint(-self.radius // 3, self.radius // 3)
            cy = center + random.randint(-self.radius // 3, self.radius // 3)
            crater_color = (40, 40, 55)
            pygame.draw.circle(self.image, crater_color, (cx, cy), crater_r)

    def update(self):
        """Move o asteroide para baixo."""
        self.rect.y += self.speed

    def is_off_screen(self) -> bool:
        """Verifica se o asteroide passou do fundo da tela."""
        return self.rect.top > SCREEN_HEIGHT

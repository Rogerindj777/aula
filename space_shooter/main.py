# =============================================================
# main.py — Loop principal do jogo Space Shooter
# =============================================================

import sys
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, CYAN,
    RED, YELLOW, ORANGE, STAR_COLOR, SCORE_PER_HIT,
    ASTEROID_SPEED_INITIAL, ASTEROID_SPEED_MAX,
    ASTEROID_SPAWN_INITIAL, ASTEROID_SPAWN_MIN,
    DIFFICULTY_STEP
)
from player import Player
from asteroid import Asteroid


# ----- Estrelas de fundo -----

def create_stars(count: int = 120) -> list:
    """Gera posições e brilhos aleatórios para estrelas de fundo."""
    stars = []
    for _ in range(count):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        brightness = random.randint(80, 255)
        size = random.choice([1, 1, 1, 2])
        stars.append((x, y, brightness, size))
    return stars


def draw_stars(surface: pygame.Surface, stars: list):
    """Desenha o campo de estrelas no fundo."""
    for x, y, brightness, size in stars:
        color = (brightness, brightness, min(255, brightness + 30))
        if size == 1:
            surface.set_at((x, y), color)
        else:
            pygame.draw.circle(surface, color, (x, y), size)


# ----- HUD (Heads-Up Display) -----

def get_difficulty(score: int) -> dict:
    """Calcula dificuldade baseada na pontuação.

    Retorna dict com spawn_rate e asteroid_speed atuais.
    """
    level = score // DIFFICULTY_STEP  # sobe nível a cada DIFFICULTY_STEP pontos

    # Spawn rate diminui (mais rápido) a cada nível
    spawn_rate = max(ASTEROID_SPAWN_MIN,
                     ASTEROID_SPAWN_INITIAL - level * 100)

    # Velocidade dos asteroides aumenta a cada nível
    asteroid_speed = min(ASTEROID_SPEED_MAX,
                         ASTEROID_SPEED_INITIAL + level * 0.5)

    return {
        "level": level + 1,
        "spawn_rate": int(spawn_rate),
        "asteroid_speed": asteroid_speed,
    }


def draw_hud(surface: pygame.Surface, font: pygame.font.Font,
             score: int, level: int):
    """Desenha a pontuação e o nível no canto superior."""
    # Pontuação
    shadow = font.render(f"PONTOS: {score}", True, (0, 0, 0))
    surface.blit(shadow, (17, 17))
    text = font.render(f"PONTOS: {score}", True, CYAN)
    surface.blit(text, (15, 15))

    # Nível
    level_shadow = font.render(f"NÍVEL: {level}", True, (0, 0, 0))
    surface.blit(level_shadow, (17, 47))
    level_text = font.render(f"NÍVEL: {level}", True, YELLOW)
    surface.blit(level_text, (15, 45))


# ----- Tela de Game Over -----

def draw_game_over(surface: pygame.Surface, score: int):
    """Desenha a tela de Game Over com a pontuação final."""
    # Overlay escuro semi-transparente
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    # Fontes
    font_big = pygame.font.Font(None, 72)
    font_med = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)

    # "GAME OVER"
    go_text = font_big.render("GAME OVER", True, RED)
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    surface.blit(go_text, go_rect)

    # Linha decorativa
    line_y = SCREEN_HEIGHT // 2 - 20
    pygame.draw.line(surface, RED, (SCREEN_WIDTH // 2 - 120, line_y),
                     (SCREEN_WIDTH // 2 + 120, line_y), 2)

    # Pontuação final
    score_text = font_med.render(f"Pontuação: {score}", True, YELLOW)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(score_text, score_rect)

    # Instruções
    restart_text = font_small.render("Pressione  R  para reiniciar", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    surface.blit(restart_text, restart_rect)

    quit_text = font_small.render("Pressione  ESC  para sair", True, (160, 160, 180))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 105))
    surface.blit(quit_text, quit_rect)


# ----- Efeito de explosão simples -----

class Explosion:
    """Partículas simples de explosão ao destruir um asteroide."""

    def __init__(self, x: int, y: int):
        self.particles = []
        for _ in range(12):
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            lifetime = random.randint(8, 20)
            size = random.randint(2, 5)
            color = random.choice([YELLOW, ORANGE, RED, CYAN])
            self.particles.append([x, y, dx, dy, lifetime, size, color])

    def update(self) -> bool:
        """Atualiza partículas. Retorna False quando todas sumiram."""
        alive = []
        for p in self.particles:
            p[0] += p[2]  # x += dx
            p[1] += p[3]  # y += dy
            p[4] -= 1     # lifetime -= 1
            if p[4] > 0:
                alive.append(p)
        self.particles = alive
        return len(self.particles) > 0

    def draw(self, surface: pygame.Surface):
        """Desenha as partículas na tela."""
        for p in self.particles:
            alpha = int(255 * (p[4] / 20))
            color = (*p[6][:3],)
            pygame.draw.circle(surface, color, (int(p[0]), int(p[1])), p[5])


# =============================================================
# LOOP PRINCIPAL
# =============================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🚀 Space Shooter — Estilo Atari")
    clock = pygame.time.Clock()

    # Fonte para o HUD
    hud_font = pygame.font.Font(None, 36)

    # Estado do jogo
    running = True
    game_over = False
    score = 0

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Jogador
    player = Player()
    all_sprites.add(player)

    # Estrelas de fundo
    stars = create_stars()

    # Explosões ativas
    explosions: list[Explosion] = []

    # Timer de spawn de asteroides (começa lento)
    SPAWN_EVENT = pygame.USEREVENT + 1
    current_difficulty = get_difficulty(score)
    pygame.time.set_timer(SPAWN_EVENT, current_difficulty["spawn_rate"])

    # ---- Game Loop ----
    while running:
        clock.tick(FPS)

        # ---- EVENTOS ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        # Reiniciar jogo
                        score = 0
                        game_over = False
                        all_sprites.empty()
                        bullets.empty()
                        asteroids.empty()
                        explosions.clear()
                        player = Player()
                        all_sprites.add(player)
                        current_difficulty = get_difficulty(score)
                        pygame.time.set_timer(SPAWN_EVENT,
                                              current_difficulty["spawn_rate"])
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Spawn de asteroides
            if event.type == SPAWN_EVENT and not game_over:
                asteroid = Asteroid(speed=current_difficulty["asteroid_speed"])
                asteroids.add(asteroid)
                all_sprites.add(asteroid)

        if not game_over:
            # Tiro contínuo ao segurar espaço
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if player.shoot(bullets):
                    # Adiciona o último bullet ao grupo geral
                    for b in bullets:
                        if b not in all_sprites:
                            all_sprites.add(b)

            # ---- ATUALIZAÇÃO ----
            all_sprites.update()

            # Colisão: projétil ↔ asteroide
            hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
            for asteroid_hit in hits:
                score += SCORE_PER_HIT
                explosions.append(
                    Explosion(asteroid_hit.rect.centerx, asteroid_hit.rect.centery)
                )

            # Atualizar dificuldade com base na pontuação
            new_difficulty = get_difficulty(score)
            if new_difficulty["spawn_rate"] != current_difficulty["spawn_rate"]:
                current_difficulty = new_difficulty
                pygame.time.set_timer(SPAWN_EVENT,
                                      current_difficulty["spawn_rate"])

            # Colisão: asteroide ↔ nave
            if pygame.sprite.spritecollide(player, asteroids, False,
                                           pygame.sprite.collide_rect_ratio(0.75)):
                game_over = True

            # Asteroide passou do fundo da tela
            for asteroid in asteroids:
                if asteroid.is_off_screen():
                    game_over = True
                    break

        # Atualizar explosões
        explosions = [e for e in explosions if e.update()]

        # ---- RENDERIZAÇÃO ----
        screen.fill(BLACK)
        draw_stars(screen, stars)

        all_sprites.draw(screen)

        # Desenhar explosões
        for explosion in explosions:
            explosion.draw(screen)

        # HUD
        draw_hud(screen, hud_font, score, current_difficulty["level"])

        # Game Over
        if game_over:
            draw_game_over(screen, score)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

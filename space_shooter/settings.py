# =============================================================
# settings.py — Configurações e constantes do jogo
# =============================================================

# Dimensões da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Taxa de quadros
FPS = 60

# Velocidades
PLAYER_SPEED = 6
BULLET_SPEED = 8

# Dificuldade progressiva dos asteroides
ASTEROID_SPEED_INITIAL = 2       # velocidade no início
ASTEROID_SPEED_MAX = 7           # velocidade máxima
ASTEROID_SPAWN_INITIAL = 1500   # spawn lento no início (ms)
ASTEROID_SPAWN_MIN = 350        # spawn mais rápido possível (ms)
DIFFICULTY_STEP = 50             # pontos necessários para subir de nível

# Cooldown de tiro do jogador (milissegundos)
SHOOT_COOLDOWN = 250

# Tamanho dos asteroides (raio min/max)
ASTEROID_MIN_RADIUS = 18
ASTEROID_MAX_RADIUS = 40

# Pontuação por asteroide destruído
SCORE_PER_HIT = 10

# ---- Paleta de cores (RGB) ----
BLACK = (10, 10, 30)
WHITE = (240, 240, 255)
CYAN = (0, 230, 255)
RED = (255, 50, 80)
YELLOW = (255, 220, 50)
ORANGE = (255, 140, 30)
DARK_GRAY = (60, 60, 80)
STAR_COLOR = (180, 180, 220)

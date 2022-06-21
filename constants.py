import pygame

pygame.init()

# colors
BLACK: tuple = (0, 0, 0)
WHITE: tuple = (255, 255, 255)
RED: tuple = (255, 0, 0)
PURPLE: tuple = (240, 0, 255)
YELLOW: tuple = (255, 255, 30)
PANEL: tuple = (153, 217, 234)

# font
FONT_SMALL = pygame.font.SysFont('Lucida Sans', 20)
FONT_PANEL = pygame.font.SysFont('Lucida Sans', 15)
FONT_HIGH = pygame.font.SysFont('Lucida Sans', 10)
FONT_BIG = pygame.font.SysFont('Lucida Sans', 24)

# window dimensions
WINDOW_WIDTH: int = 400
WINDOW_HEIGHT: int = 600

# game constants
SCROLL_THRESH: int = 150
GRAVITY: int = 1
MAX_ENEMIES: int = 10
ENEMY_SCALE: tuple = (60, 50)
BONUS_SCALE: tuple = (50, 40)
FLOOR_SCALE: tuple = (400, 40)
WUALUIGI_SCALE: tuple = (40, 70)


CLOCK = pygame.time.Clock()
FPS: int = 60

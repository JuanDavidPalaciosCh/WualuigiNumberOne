import pygame

# colors
BLACK: tuple = (0, 0, 0)
WHITE: tuple = (255, 255, 255)
PURPLE: tuple = (240, 0, 255)

# window dimensions
WINDOW_WIDTH: int = 400
WINDOW_HEIGHT: int = 600

# game constants
SCROLL_THRESH: int = 200
GRAVITY: int = 1
MAX_ENEMIES: int = 10
ENEMY_SCALE: tuple = (50, 40)
FLOOR_SCALE: tuple = (400, 40)


CLOCK = pygame.time.Clock()
FPS: int = 60

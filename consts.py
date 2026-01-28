import pygame
from math_custom import Vector2D

# SETUP
SCREEN_W:int = 0
SCREEN_H:int = 0
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_W), pygame.FULLSCREEN) # For borderless, use pygame.NOFRAME
# If setted to fullscreen then pass the real sizes 
if SCREEN_W == 0:
    SCREEN_W = SCREEN.width
if SCREEN_H == 0:
    SCREEN_H = SCREEN.height

FPS:int = 60

# COLORS
CLR_WHITE:tuple[int,int,int] = (255,255,255)
CLR_GREEN:tuple[int,int,int] = (0,255,0)


# PHYSICAL CONSTANTS
GRAVITY:Vector2D = Vector2D(0, 980)
BOUNCE_STOP:float = 60
SLIDE_STOP:float = 10
USER_PULL_STRENGTH:float = 1000.0
USER_PULL_DAMPING:float = 2.0

# SCENE
WALL_FRICTION:float = 0.3   # how much does the velocity get reduced
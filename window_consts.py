import pygame

# SETUP
SCREEN_W:int = 0
SCREEN_H:int = 0
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_W), pygame.FULLSCREEN) # For borderless, use pygame.NOFRAME
# If setted to fullscreen then pass the real sizes 
if SCREEN_W == 0:
    SCREEN_W = SCREEN.width
if SCREEN_H == 0:
    SCREEN_H = SCREEN.height

SCREEN_CENTER: tuple[float, float] = (SCREEN_W*0.5, SCREEN_H*0.5)

FPS:int = 60

# COLORS
CLR_WHITE:tuple[int,int,int] = (255,255,255)
CLR_GREEN:tuple[int,int,int] = (0,255,0)


import pygame
from math_custom import Vector2D
import datetime

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


# PHYSICAL CONSTANTS
GRAVITY:Vector2D = Vector2D(0, 980)
BOUNCE_STOP:float = 60
SLIDE_STOP:float = 10
USER_PULL_STRENGTH:float = 1000.0
USER_PULL_DAMPING:float = 2.0

# SCENE
WALL_FRICTION:float = 0.3   # how much does the velocity get reduced

# CHARACTER
SPLAT_VELOCITY:Vector2D = Vector2D(200, 400)   # the speed where it splats hitting the floor


# CHARACTER CONSTS
JUMP_FORCE: Vector2D = Vector2D(4000, -15000)
WAIT_TIME:  float = 5
TARGET_STOP:float = 100

# Phrases for Pachu
pachus_bd = datetime.date(datetime.datetime.now().year, 3, 6)
CUCHU_PHRASES = [
        'Te amo <3',
        'Estas ocupada amor?',
        'Me encantas jsjsjs',
        'Mandame un mensaje a whatsapp',
        'Te puedo ayudar?',
        'Soy tu principe jeje',
        f'Faltan {(pachus_bd - datetime.date.today()).days} dias para tu cumple!',
        'aiiiiiiiiiii',
        ':V',
        'OMG',
        'XD',
        'ñam ñam',
        'Vemos Javier Ledesma?',
        'Quiero refrescos...',
        'Te quiero mucho mucho <3',
        'Mi loquitaaAaAa',
        'Sos perfecta <3',
        'Mi bombonita <3',
        'Its showtime',
        'PaachUUuU PaAchUuuUu',
        'Te morfo <3',
        'Tirameee',
        'Quiero tiramisu'
]

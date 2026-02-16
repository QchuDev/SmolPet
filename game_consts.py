import pygame
import datetime

from basics import CharacterData, SpriteSheet
from math_custom import Vector2D

# PHYSICAL CONSTANTS
GRAVITY:Vector2D = Vector2D(0, 100)
BOUNCE_STOP:float = 60
SLIDE_STOP:float = 10
WALL_FRICTION:float = 0.3   # how much does the velocity get reduced
SPLAT_VELOCITY:Vector2D = Vector2D(200, 200)   # the speed where it splats hitting the floor

# MOUSE DRAG
USER_PULL_STRENGTH:float = 1000.0
USER_PULL_DAMPING:float = 2.0


# AICONTROLLER
JUMP_FORCE: Vector2D = Vector2D(4000, -15000)
WAIT_TIME:  float = 10
SLEEP_TIME: float = 120
TARGET_STOP:float = 100

# WEIGHTS
SLEEP_WEIGHT    :tuple[str,int] = ('sleep',2)
MOVE_WEIGHT     :tuple[str,int] = ('move', 30)
WAIT_WEIGHT     :tuple[str,int] = ('wait', 40)
TALK_WEIGHT     :tuple[str,int] = ('talk', 20)
OPEN_IMG_WEIGHT :tuple[str,int] = ('open_image', 8)

ACTION_WEIGHTS  :list[tuple[str,int]] = [SLEEP_WEIGHT, MOVE_WEIGHT, WAIT_WEIGHT, TALK_WEIGHT, OPEN_IMG_WEIGHT]  # Randomize weights for actions



# ===================================================================================================================================
#                                           ALL CHARACTER DATAS
# ===================================================================================================================================

# Spritesheets
bobby_ss = SpriteSheet('resources/images/bobby_16.png', (16,16), scale_factor=4)
cuchu_ss = SpriteSheet('resources/images/cuchu_16.png', (16,16), scale_factor=4)
pol_ss = SpriteSheet('resources/images/pol_16.png', (16,16), scale_factor=4)

# Phrases 
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
BOBBY_PHRASES = [
    'Im a little piece of art', 
    'I cant feel a thing', 
    'My flesh is pixels'
]
POL_PHRASES = [
    'Guau', 
    'Guau Guau', 
    'GUAU', 
    'grr'
]

# Character DATA
CHARACTERS: list[CharacterData] = [
    CharacterData(bobby_ss, 'Bobby', BOBBY_PHRASES),
    CharacterData(cuchu_ss, 'Cuchu', CUCHU_PHRASES),
    CharacterData(pol_ss, 'Pol', POL_PHRASES)
]
import pygame
import datetime

from essentials.basics import CharacterData, SpriteSheet, State, Transition
from essentials.math_custom import Vector2D

# PHYSICAL CONSTANTS
GRAVITY:Vector2D = Vector2D(0, 980)
BOUNCE_STOP:float = 60
SLIDE_STOP:float = 10
SPLAT_VELOCITY:Vector2D = Vector2D(200, 200)   # the speed where it splats hitting the floor

# MOUSE DRAG
USER_PULL_STRENGTH:float = 250.0
USER_PULL_DAMPING:float = 2.0

# AICONTROLLER
JUMP_FORCE: Vector2D = Vector2D(4000, -15000)
WAIT_TIME:  float = 10
SIT_TIME:  float = 30
SLEEP_TIME: float = 120
TARGET_STOP:float = 100

# WEIGHTS for AIController actions
ACTION_WEIGHTS  :list[tuple[str,int]] = [
    ('sleep', 2), 
    ('move', 40), 
    ('wait', 60), 
    ('talk', 8), 
    ('open_image', 1),
    ('sit', 15)
]

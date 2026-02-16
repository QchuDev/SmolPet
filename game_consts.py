import pygame
import datetime

from basics import CharacterData, SpriteSheet, State, Transition
from math_custom import Vector2D

# PHYSICAL CONSTANTS
GRAVITY:Vector2D = Vector2D(0, 980)
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
SLEEP_WEIGHT    :tuple[str,int] = ('sleep', 2)
MOVE_WEIGHT     :tuple[str,int] = ('move', 40)
WAIT_WEIGHT     :tuple[str,int] = ('wait', 60)
TALK_WEIGHT     :tuple[str,int] = ('talk', 10)
OPEN_IMG_WEIGHT :tuple[str,int] = ('open_image', 8)

ACTION_WEIGHTS  :list[tuple[str,int]] = [SLEEP_WEIGHT, MOVE_WEIGHT, WAIT_WEIGHT, TALK_WEIGHT, OPEN_IMG_WEIGHT]  # Randomize weights for actions

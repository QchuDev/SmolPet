import pygame
from essentials.basics import Entity, SpriteSheet
from essentials.components import Entity

# PARTICLE PREFABS
# name =        [texture, lifetime,ammount, force, accy]
POPCORN_PRTS =  ['popcorn', 0.6,    6,      3,      0.2     ]
SPARK_PRTS =    ['spark',   0.8,    8,      3,      0       ]
HEART_PRTS =    ['heart',   0.8,    8,      3,      -0.08   ]
SMOKE_PRTS =    ['smoke',   0.6,    8,      2,      -0.02   ]

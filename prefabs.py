import pygame
from essentials.basics import Entity, SpriteSheet
from essentials.components import Entity

# PARTICLE PREFABS
# name =        [texture, lifetime,ammount, force, accy]
POPCORN_PRTS =  ['popcorn', 0.8,    8,      3,      0.2     ]
SPARK_PRTS =    ['spark',   0.8,    8,      3,      0       ]
HEART_PRTS =    ['heart',   0.8,    8,      3,      -0.05   ]


# ENTITIES
#popcorn_bucket_img = SpriteSheet('resources/images/popcorn_bucket.png', (16,16), scale_factor=4)
#POPCORN_BUCKET = Entity(popcorn_bucket_img.get_sprite(0), 'Popcorn Bucket')
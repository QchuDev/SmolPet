import random
import pygame
from pygame._sdl2 import Texture

from essentials.basics import Entity, Animation, ParticlesManager, SpriteSheet, World
from essentials.math_custom import Vector2D
from essentials.components import ParticlesEmitter, PhysicalBall, MouseDrag, Animator, AIController, StatesManager, TextBubble, CharactersHandler, EntityEraser
from characters_setup import CHARACTERS
from essentials.window_setup import RENDERER
from states_graph import STATES

# Initialize the font
pygame.font.init()

prts_manager = ParticlesManager()
def initial_entities():
    # entities array
    ents = []

    # animations
    idle:       Animation = Animation('idle',       [0, 1, 2],      frame_duration=0.2)
    hit_floor:  Animation = Animation('hit_floor',  [3, 4, 5],      frame_duration=0.08,    loop=False)
    hit_wall:   Animation = Animation('hit_wall',   [12, 13, 14],   frame_duration=0.08,    loop=False)
    air:        Animation = Animation('air',        [6, 7, 8],      frame_duration=0.2)
    talk:       Animation = Animation('talk',       [9, 10, 11],    frame_duration=0.2)
    go_sleep:   Animation = Animation('go_sleep',   [15, 16, 17],   frame_duration=0.2,     loop=False)
    sleeping:   Animation = Animation('sleeping',   [18, 19, 20],   frame_duration=0.3)
    # entity and components
    for i in range(1):
        npc = Entity(
                name=f'Entity{i}',
                components= [
                PhysicalBall(radius=30, air_resist=0.0005, mass=1, retention_y=0.45),
                MouseDrag(),
                Animator(anims = [idle, hit_floor, hit_wall, air, talk, go_sleep, sleeping]),  # sleeping WIP
                AIController(timer_range=(0.5, 2)),
                StatesManager(STATES),
                TextBubble(),
                CharactersHandler(CHARACTERS)
                ]
            )
        
        # Random start-push
        phys = npc.get_component(PhysicalBall)
        rand_push = Vector2D(random.random()*2-1, random.random()*2-1)*50000
        if phys: phys.applyForce(rand_push)
        
        ents.append(npc)

    # POPCORN BUCKET ========================================================================
    popcorn_bucket_ss = SpriteSheet('resources/images/props_16.png', (16,16), scale_factor=4)
    popcorn_bucket = Entity(
        popcorn_bucket_ss.get_texture(0), 
        name='Popcorn Bucket',
        components= [
            PhysicalBall(radius=30, air_resist=0.001, mass=1, retention_y=0.3, directed=False, show_hitboxes=True),
            MouseDrag(),
            ParticlesEmitter(prts_manager, 'popcorn', frequency=1, offset= (0, -4))
        ]
    )
    ents.append(popcorn_bucket)

    return ents

def setup_entities(ents: list[Entity]):
    for e in ents:
        e.start()

World.entities = initial_entities()
setup_entities(World.entities)
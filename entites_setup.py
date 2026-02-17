import random
import pygame
from basics import Entity, Animation, World
from components import PhysicalBall, MouseDrag, Animator, AIController, StatesManager, TextBubble, CharactersHandler, EntityEraser
from characters_setup import CHARACTERS
from states_graph import STATES

# Initialize the font
pygame.font.init()

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
    sleeping:   Animation = Animation('sleeping',   [18, 19, 20],   frame_duration=0.2)

    # entity and components
    for i in range(100):
        npc = Entity(name=f'Entity{i}',
            components= [
            PhysicalBall(radius=30, air_resist=0.0005, mass=1, retention_y=0.45),
            MouseDrag(),
            Animator(anims = [idle, hit_floor, hit_wall, air, talk, go_sleep, sleeping]),  # sleeping WIP
            AIController(timer_range=(0.5, 2)),
            StatesManager(STATES),
            TextBubble('resources/images/text_bubble.png', corner_size=16),
            CharactersHandler(CHARACTERS)
            ]
        )
        
        ents.append(npc)

    return ents

def setup_entities(ents: list[Entity]):
    for e in ents:
        e.start()

World.entities = initial_entities()
setup_entities(World.entities)
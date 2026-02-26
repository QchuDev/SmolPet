import random
import pygame
from pygame import Rect
from pygame._sdl2 import Texture
from achievements import ALL_ACHIEVEMENTS
from essentials.basics import PersistenceManager, UIElement, Entity, Animation, ParticlesManager, SpriteSheet, UIManager, World
from essentials.math_custom import Vector2D
from essentials.components import Button, ParticlesEmitter, PhysicalBall, MouseDrag, Animator, AIController, QuitOnClick, StatesManager, TextBubble, CharactersHandler, EntityEraser
from characters_setup import CHARACTERS
from essentials.window_setup import RENDERER, SCREEN_CENTER, SCREEN_W, SCREEN_H
from states_graph import NPC_STATES, PROP_STATES

# Initialize the font
pygame.font.init()

# NPC ANIMATIONS
NPC_ANIMATIONS = [
    Animation('idle',       [0, 1, 2],      frame_duration=0.2),
    Animation('hit_floor',  [3, 4, 5],      frame_duration=0.08,    loop=False),
    Animation('air',        [6, 7, 8],      frame_duration=0.2),
    Animation('talk',       [9, 10, 11],    frame_duration=0.2),
    Animation('hit_wall',   [12, 13, 14],   frame_duration=0.08,    loop=False),
    Animation('go_sleep',   [15, 16, 17],   frame_duration=0.2,     loop=False),
    Animation('sleeping',   [18, 19, 20],   frame_duration=0.3),
    Animation('go_sit',     [21,22,23],     frame_duration=0.2,     loop=False),
    Animation('sit',        [24,25,26],     frame_duration=0.3)
]

PROP_ANIMATIONS = [
    Animation('still',      [0, 1, 2],      frame_duration=0.2),
    Animation('bounce',     [3, 4, 5],      frame_duration=0.08,    loop=False),
]

# Main particles manager
prts_manager = ParticlesManager()

# Main persistence manager
persist_manager = PersistenceManager()
# Entities
def initial_entities():
    # entities array
    ents = []

    save_data = persist_manager.load()
    if save_data:
        # Load achievements
        from achievements import load_save_data
        load_save_data(save_data['achievements'])

        # Spawn entities
        for ent_info in save_data['entities']:
            # For now we save only the name
            
            
            
            pass


    else:
        ALL_ACHIEVEMENTS['UN VIRUS?!?'][0] = True
    
    # entity and components
    for i in range(10):
        npc = Entity(
                name=f'Entity{i}',
                components= [
                PhysicalBall(radius=30, air_resist=0.0005, mass=1, retention_y=0.45),
                MouseDrag(),
                Animator(anims = NPC_ANIMATIONS),  # sleeping WIP
                AIController(timer_range=(0.5, 2)),
                StatesManager(NPC_STATES),
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
    popcorn_bucket_ss = SpriteSheet('resources/images/popcorn_bucket_16.png', (16,16), scale_factor=4)
    popcorn_bucket = Entity( 
        name='Popcorn Bucket',
        components= [
            PhysicalBall(radius=30, air_resist=0.001, mass=1, retention_y=0.3, directed=False),
            MouseDrag(),
            ParticlesEmitter(prts_manager, 'popcorn', frequency=3, offset= (0, -2)),
            Animator(popcorn_bucket_ss, anims=PROP_ANIMATIONS),
            StatesManager(PROP_STATES)
        ]
    )
    ents.append(popcorn_bucket)

    # TIRAMISU ========================================================================
    tiramisu_ss = SpriteSheet('resources/images/tiramisu_16.png', (16,16), scale_factor=4)
    tiramisu = Entity( 
        name='Tiramisu',
        components= [
            PhysicalBall(pos=SCREEN_CENTER+Vector2D(32,0), radius=30, air_resist=0.001, mass=1, retention_y=0.2, directed=False),
            MouseDrag(),
            Animator(tiramisu_ss, anims=PROP_ANIMATIONS),
            StatesManager(PROP_STATES)
        ]
    )
    ents.append(tiramisu)

    # BALLOONS ========================================================================
    balloon_sss=[]
    for i in range(4):
        balloon_sss.append(SpriteSheet(f'resources/images/balloons/balloon{i}_16.png', (16,16), scale_factor=4))
    
    for i in range(1):
        balloon = Entity( 
            name='Balloon',
            components= [
                PhysicalBall(pos=SCREEN_CENTER+Vector2D(-32,0), radius=15, air_resist=0.005, mass=1, retention_y=0.6, grav_scale=0.1, directed=False),
                MouseDrag(),
                Animator(balloon_sss[random.randint(0, len(balloon_sss)-1)], anims=PROP_ANIMATIONS),
                StatesManager(PROP_STATES)
            ]
        )
        ents.append(balloon)

    # Sets up all entities
    for e in ents:
        e.start()

    return ents

# UI Elements
def initial_ui():
    # entities array
    ui_elems = []

    # quit button
    qbutton_surface = pygame.image.load('resources/images/ui/buttons_16.png')
    quit_button = UIElement(
        texture=Texture.from_surface(RENDERER, qbutton_surface),
        rect=Rect(0,0,32,32),
        ui_components=[
            Button(click_radius=38),
            QuitOnClick()
        ]
    )
    quit_button.pos.x, quit_button.pos.y  = SCREEN_W - 42, 16

    ui_elems.append(quit_button)

    # Sets up all entities
    for u in ui_elems:
        u.start()

    return ui_elems

# hand them to World and UIManager
World.entities = initial_entities()
UIManager.ui_elements = initial_ui()
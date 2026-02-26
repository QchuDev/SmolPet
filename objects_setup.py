import random
import pygame
from pygame import Rect
from pygame._sdl2 import Texture
from essentials.basics import GameManager, PersistenceManager, UIElement, ParticlesManager, UIManager, World
from essentials.components import Button, QuitOnClick
from essentials.math_custom import Vector2D
from essentials.window_setup import RENDERER,SCREEN_W
from prefabs import ALL_PREFABS

# Initialize the font
pygame.font.init()

# Main particles manager
prts_manager = ParticlesManager()

# Main persistence manager
persist_manager = PersistenceManager()
# Entities
def initial_entities() -> None:
    save_data = persist_manager.load()
    if save_data:
        # Load achievements
        from achievements import load_save_data
        load_save_data(save_data['achievements'])

        # Spawn entities
        for i, ent_info in enumerate(save_data['entities']):
            # For now we save only the name
            prefab_name = ent_info['name'].lower()

            # Call the necessary prefab to spawn 
            if prefab_name != 'balloon':
                new_ent = ALL_PREFABS[prefab_name].clone()
            else:
                random_ballon = ['red balloon', 'blue balloon', 'yellow ballon', 'green balloon'][random.randrange(0,4)]
                new_ent = ALL_PREFABS[random_ballon].clone()

            # Change its starting position
            padding = 40
            new_ent.pos = Vector2D(padding + (SCREEN_W-2*padding)*i/len(save_data['entities']),-40)

            # Insert it to the main loop
            World.entities.append(new_ent)

    else:
        # Because we dont have save data is our first time
        # We spawn Pachu and set first_time equals True
        World.entities.append(ALL_PREFABS['pachu'])
        GameManager.first_time = False
    
    # Calling the start method of entities so components prepare
    for e in World.entities:
        e.start()

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
initial_entities()
UIManager.ui_elements = initial_ui()
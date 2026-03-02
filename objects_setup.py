import random
import pygame
from pygame import Rect
from pygame._sdl2 import Texture
from essentials.basics import PersistenceManager, UIElement, ParticlesManager, UIManager, World
from essentials.components import AchievementCycle, Animator, Button, QuitOnClick, StatesManager
from essentials.gm import GameManager
from essentials.math_custom import Vector2D
from essentials.window_setup import RENDERER,SCREEN_W,SCREEN_H
from prefabs import ALL_PREFABS
import prefabs

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

            # Create an entity from prefabs
            new_ent = prefabs.create_entity(prefab_name, x=SCREEN_W*random.uniform(0,1), y=SCREEN_H*0.8)

            # Insert it to the main loop
            World.entities.append(new_ent)
            GameManager.unlocked_entites.append(prefab_name)

    else:
        # Because we dont have save data is our first time
        GameManager.first_time = True
        
    
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
        name='quit button',
        texture=Texture.from_surface(RENDERER, qbutton_surface),
        rect=Rect(0,0,32,32),
        ui_components=[
            Button(click_radius=20),
            QuitOnClick()
        ]
    )
    quit_button.pos.x, quit_button.pos.y  = SCREEN_W - 42, 42
    ui_elems.append(quit_button)



    # The UIElement in charge of showing the achievements
    achievements_displayer = AchievementCycle(scale=3)
    displayer_uielement = UIElement(
        name='achievement pop-up',
        ui_components=[
            achievements_displayer
        ]
    )
    ui_elems.append(displayer_uielement)
    GameManager.achievements_displayer = achievements_displayer


    # Sets up all entities
    for u in ui_elems:
        u.start()

    return ui_elems

# hand them to World and UIManager
initial_entities()
UIManager.ui_elements = initial_ui()
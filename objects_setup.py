import random
import pygame
from pygame import Rect
from pygame._sdl2 import Texture
from essentials.basics import PersistenceManager, UIElement, ParticlesManager, UIManager, World
from essentials.components import AchievementCycle, Animator, Button, HoverDetect, ProgressGrid, QuitOnClick, SlideOut, SlideWith, StatesManager, ToggleAchievementsOnClick, ToggleMuteOnClick
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
        GameManager.t_played = save_data['time_played']

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

    buttons_surface = pygame.image.load('resources/images/ui/buttons_16.png')
    button_texture  = Texture.from_surface(RENDERER, buttons_surface)
    # quit button
    quit_button = UIElement(
        name='quit button',
        texture=button_texture,
        source_area=Rect(0,0,16,16),
        rect=Rect(0,0,32,32),
        ui_components=[
            Button(click_radius=20),
            QuitOnClick()
        ]
    )
    
    # mute button
    mute_button = UIElement(
        name='mute button',
        texture=button_texture,
        source_area=Rect(0, 32, 16, 16),
        rect=Rect(0,0,32,32),
        ui_components=[
            Button(click_radius=20, pressed_rect=Rect(16,32,16,16), not_pressed_rect=Rect(0,32,16,16)),
            ToggleMuteOnClick()
        ]
    )

    progress_panel = UIElement(
        name='progress panel',
        ui_components=[
            ProgressGrid()
        ]
    )
    # progress button toggles -> ON and OFF the progress panel
    progress_button = UIElement(
        name='progress button',
        texture=button_texture,
        source_area=Rect(0, 16, 16, 16),
        rect=Rect(0,0,32,32),
        ui_components=[
            Button(click_radius=20, pressed_rect=Rect(16,16,16,16), not_pressed_rect=Rect(0,16,16,16)),
            ToggleAchievementsOnClick(progress_panel)
        ]
    )

    mx,my = 0.98, 0.1
    
    slider_surface = pygame.image.load('resources/images/ui/slide_panel.png')
    slider_texture  = Texture.from_surface(RENDERER, slider_surface)
    # the UIElement which is in charge of showing the buttons inside it
    buttons_slider = UIElement(
        name='buttons slider',
        texture=slider_texture,
        rect=Rect(0,0,slider_texture.width*2,slider_texture.height*2),
        source_area=Rect(0,0,slider_texture.width,slider_texture.height),
        ui_components=[
            SlideWith([quit_button, mute_button, progress_button]),
            HoverDetect(),
            SlideOut(pos_a=Vector2D(SCREEN_W*(mx+0.01), SCREEN_H*my), pos_b=Vector2D(SCREEN_W*(mx-0.05), SCREEN_H*my))
        ]
    )
    
    quit_button.pos =Vector2D(SCREEN_W*mx, SCREEN_H*my)
    mute_button.pos =Vector2D(SCREEN_W*(mx-0.02), SCREEN_H*my)
    progress_button.pos =Vector2D(SCREEN_W*(mx-0.04), SCREEN_H*my)
    buttons_slider.pos = Vector2D(SCREEN_W*(mx-0.05), SCREEN_H*my)

    # order of draw, remember
    ui_elems.append(progress_panel)
    ui_elems.append(buttons_slider)
    ui_elems.append(quit_button)
    ui_elems.append(mute_button)
    ui_elems.append(progress_button)

    



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
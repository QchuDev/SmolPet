import pygame
import win32api
import win32con
import win32gui
import datetime

# Custom packages
from math_custom import Vector2D
# Essentials
from basics import Entity, Animation
# Components
from components import Animator, PhysicalBall, MouseDrag, AIController, StatesManager, TextBubble, CharactersHandler
# Import Setup constants
from window_consts import SCREEN, FPS, SCREEN_CENTER, CLR_GREEN, CLR_WHITE
from game_consts import CHARACTERS

pygame.init()
pygame.display.set_caption('For my love')

## TRANSPARENT WINDOW =================================================================================== 
TRANSPARENT_COLOR = (255, 0, 128)  # Transparency color
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]

win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)

# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT_COLOR), 0, win32con.LWA_COLORKEY)

# Keep window to the front
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

## ==========================================================================================================

# Function to create all wanted entities at start
def create_entities() -> list[Entity]:
    ents = []

    # CREATE BOBBY =====================================================
    # animations and character
    

    idle:       Animation = Animation('idle', [0, 1, 2], frame_duration=0.2)
    hit_floor:  Animation = Animation('hit_floor', [3, 4, 5], frame_duration=0.08, loop=False)
    hit_wall:   Animation = Animation('hit_wall', [12, 13, 14], frame_duration=0.08, loop=False)
    air:        Animation = Animation('air', [6, 7, 8], frame_duration=0.2)
    talk:       Animation = Animation('talk', [9, 10, 11], frame_duration=0.2)
    go_sleep:   Animation = Animation('go_sleep', [15, 16, 17], frame_duration=0.2, loop=False)
    sleeping:   Animation = Animation('sleeping', [18, 19, 20], frame_duration=0.2)

    # entity and components
    for i in range(100):
        bobby = Entity(name='Entity00',
            components= [
            PhysicalBall(pos = SCREEN_CENTER, radius=30, air_resist=0.0005, mass=1),
            MouseDrag(),
            Animator(anims = [idle, hit_floor, hit_wall, air, talk, go_sleep, sleeping]),  # sleeping WIP
            AIController(timer_range=(0.5, 2)),
            StatesManager(),
            TextBubble('resources/images/text_bubble.png', corner_size=16),
            CharactersHandler(CHARACTERS)
            ]
        )
        ents.append(bobby)

    return ents

# Calls the start funcion on the entity so it can setup all its components
def setup_entities(ents: list[Entity]):
    for e in ents:
        e.start()

# Time Variables
clock = pygame.time.Clock()
dt = 0.01
dt_phys = 1/60  # once per 60FPS
accumulator = 0.0

entities: list[Entity] = create_entities()
setup_entities(entities)
charHandler = entities[0].get_component(CharactersHandler)
## MAIN LOOP ======================================================
running:bool = True
while running:
    # Update delta_time
    dt = clock.tick(FPS) / 1000
    accumulator += dt
    dt = max(0.001, min(0.1, dt))

    SCREEN.fill(TRANSPARENT_COLOR)  # Transparent background

    # Update the entities on a constant way, when the accumulator exceeds the dt_phys (delta time for physics)
    while accumulator >= dt_phys:
        # Update entities
        for entity in entities:
           entity.update(dt_phys)
        accumulator -= dt_phys
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:        # Check for key events
            if event.key == pygame.K_ESCAPE:    
                running = False                 # Close with the ESC button
            elif event.key == pygame.K_SPACE:
                if charHandler: 
                    charHandler.switch_character('Cuchu' if charHandler.curr_char == 'Bobby' else 'Bobby')
    
    # DRAWS.
    for entity in entities:
        entity.draw()       # Draw entities

    pygame.display.flip()   # Update draws
import pygame
import win32api
import win32con
import win32gui

# Custom packages
from math_custom import Vector2D

# Essentials
from basics import Entity, SpriteSheet, Animation

# Components
from basics import Animator, PhysicalBall, MouseDrag, AIController, StatesManager

# Import Setup constants
from consts import SCREEN, FPS



pygame.init()
pygame.display.set_caption('Smol Pet')

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

# Time Variables
clock = pygame.time.Clock()
global delta_time
delta_time = 0.01


# Character creation ==============================================
# Creating the components for the character

idle: Animation = Animation('idle', [0, 1, 2], frame_duration=0.15)
hit_floor: Animation = Animation('hit_floor', [3, 4, 5], frame_duration=0.10, loop=False)
air: Animation = Animation('air', [6,7,8], frame_duration=0.15)

ss = SpriteSheet('resources/images/placeholder_spritesheet.png', (64,64))
character = ss.get_sprite(0)

population = 100
entities: list[Entity] = []
for i in range(population):
    ent = Entity(character, 
        [
        PhysicalBall(pos = (SCREEN.get_width()*i/population, SCREEN.get_height()*0.5),radius=30, air_resist=0.0005, mass=1),
        MouseDrag(),
        Animator(ss, [idle, hit_floor, air]),
        AIController(timer_range=(0.5, 2)),
        StatesManager()
        ]
    )
    entities.append(ent)


## MAIN LOOP ======================================================
now = pygame.time.get_ticks()
cont = 0
running:bool = True

while running:
    # Filling the background with the previously color setted to be transparent.
    SCREEN.fill(TRANSPARENT_COLOR)  # Transparent background

    # Close with the ESC button
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    for entity in entities:
        entity.update(delta_time)
        entity.draw()
    
    # Update delta_time
    delta_time = clock.tick(FPS) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    
    pygame.display.flip()
    now = pygame.time.get_ticks()
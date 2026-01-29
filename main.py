import pygame
import win32api
import win32con
import win32gui
import math

# Custom packages
from math_custom import Vector2D
from basics import Entity, SpriteSheet, Animator, PhysicalBall, MouseDrag

# Import Setup constants
from consts import SCREEN, FPS




pygame.init()

pygame.display.set_caption('Smol Pet')
## TRANSPARENT WINDOW =================================================================================== 
TRANSPARENT_COLOR = (255, 0, 128)  # Transparency color
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]

win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT_COLOR), 0, win32con.LWA_COLORKEY)
# Keep window to the front
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
## ==========================================================================================================

# Time Variables
clock = pygame.time.Clock()
global delta_time
delta_time = 0.01


# Character creation ==============================================

# Creating the components for the character

cuchu_character = pygame.image.load('resources/images/ball.png').convert_alpha()
cuchu_character = pygame.transform.scale(cuchu_character, (60,60))

cuchu = Entity(cuchu_character, [
    PhysicalBall(radius=30, air_resist=0.0005, mass=2),
    MouseDrag()
    ])

# =================================================================

## MAIN LOOP ======================================================
running:bool = True
while running:
    # Filling the background with the previously color setted to be transparent.
    SCREEN.fill(TRANSPARENT_COLOR)  # Transparent background
    # Close with the ESC button
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update Entity
    cuchu.update(delta_time)

    # Draw entities
    cuchu.draw()

    # Update delta_time
    delta_time = clock.tick(FPS) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    
    pygame.display.flip()
import math

import pygame
import win32api

# Import Setup constants
from essentials.math_custom import Vector2D
from essentials.window_setup import RENDERER, TRANSPARENT_COLOR, WINDOW, FPS, SCREEN_CENTER, WINDOW
from prefabs import POPCORN_PRTS, SPARK_PRTS, HEART_PRTS
# Setup scripts
from essentials.debug_tools import monitor
import user_activity

# Execute the entities_setup before reading World
from entites_setup import prts_manager
from essentials.basics import Entity, MouseInput, World


# Time Variables
clock = pygame.time.Clock()
dt = 0.01
dt_phys = 1/60  # once per 60FPS
accumulator = 0.0

# testing 
## MAIN LOOP ======================================================
running:bool = True
while running:
    # Update delta_time
    dt = clock.tick(FPS) / 1000
    accumulator += dt
    dt = max(0.001, min(0.1, dt))

    # Draw the background
    RENDERER.draw_color = TRANSPARENT_COLOR
    RENDERER.clear()

    # Update mouse inputs
    m_x, m_y = win32api.GetCursorPos()
    MouseInput.pos.x, MouseInput.pos.y = m_x, m_y
    MouseInput.left_clicked = bool(win32api.GetAsyncKeyState(0x01) & 0x8000)

    # To clean the request queue
    for event in pygame.event.get():
        pass
    
    # Update the entities on a constant way, when the accumulator exceeds the dt_phys (delta time for physics)
    while accumulator >= dt_phys:
        # Update entities
        for entity in World.entities:
            entity.update(dt_phys)
        accumulator -= dt_phys
         
    # DRAWS
    for entity in World.entities:
        entity.draw()       # Draw entities
    
    # Particles manager
    prts_manager.update(dt)
    prts_manager.draw()

    # Debug tools
    monitor.clock.tick()
    monitor.update(dt)
    monitor.render()

    RENDERER.present()


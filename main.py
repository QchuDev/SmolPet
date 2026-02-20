import pygame
import win32api
import win32con
import win32gui

# Import Setup constants
from essentials.window_consts import SCREEN, FPS, SCREEN_CENTER
from prefabs import POPCORN_PRTS, SPARK_PRTS, HEART_PRTS
# Setup scripts
from essentials.debug_tools import monitor
import user_activity

# Execute the entities_setup before reading World
import entites_setup
from essentials.basics import World, ParticlesManager

pygame.init()
pygame.display.set_caption('A small detail')

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
dt = 0.01
dt_phys = 1/60  # once per 60FPS
accumulator = 0.0

# testing 

prts_manager = ParticlesManager()
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
        for entity in World.entities:
           entity.update(dt_phys)
        accumulator -= dt_phys    

    m_x, m_y = win32api.GetCursorPos()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:        # Check for key events
            if event.key == pygame.K_ESCAPE:    
                running = False                 # Close with the ESC button
            elif event.key == pygame.K_1:
                prts_manager.emit(m_x-15, m_y-15, *SPARK_PRTS)
            elif event.key == pygame.K_2:
                prts_manager.emit(m_x-15, m_y-15, *POPCORN_PRTS)
            elif event.key == pygame.K_3:
                prts_manager.emit(m_x-15, m_y-15, *HEART_PRTS)
                
    # DRAWS.
    for entity in World.entities:
        entity.draw()       # Draw entities

    # Particles manager
    prts_manager.update(dt)
    prts_manager.draw()

    # Debug tools
    monitor.render(SCREEN, clock)

    pygame.display.flip()   # Update draws
import pygame
import win32api
import win32con
import win32gui

# Import Setup constants
from window_consts import SCREEN, FPS

# Execute the entities_setup before reading World
import entites_setup
from basics import World

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

# DEVELOPMENT DEBUG
class PerformanceMonitor:
    def __init__(self, font_size=18):
        self.font = pygame.font.SysFont("Arial", font_size)
        self.clock = pygame.time.Clock()
        self.fps_list = []
        
    def render(self, screen, clock):
        # 1. Obtener FPS actuales
        fps = clock.get_fps()
        
        # 2. Calcular "Frame Time" (ms que tarda tu código en ejecutarse)
        # clock.get_rawtime() devuelve el tiempo transcurrido entre los dos últimos ticks
        # sin contar el tiempo que Pygame estuvo esperando para limitar los FPS.
        frame_time = clock.get_rawtime()
        
        # 3. Formatear textos
        # FPS: Frames por segundo reales
        # MS: Tiempo real de procesamiento (si es > 16ms, no llegarás a 60 FPS)
        fps_text = self.font.render(f"FPS: {int(fps)}", True, (0, 255, 0))
        ms_text = self.font.render(f"Proc: {frame_time}ms", True, (0, 255, 255))
        
        # 4. Dibujar fondo negro pequeño para legibilidad
        pygame.draw.rect(screen, (0, 0, 0, 150), (5, 5, 100, 45))
        screen.blit(fps_text, (10, 10))
        screen.blit(ms_text, (10, 28))
monitor = PerformanceMonitor()

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

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:        # Check for key events
            if event.key == pygame.K_ESCAPE:    
                running = False                 # Close with the ESC button
                
    # DRAWS.
    for entity in World.entities:
        entity.draw()       # Draw entities

    monitor.render(SCREEN, clock)

    pygame.display.flip()   # Update draws
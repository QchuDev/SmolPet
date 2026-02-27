import pygame
import win32api
import win32con
import win32gui
from pygame._sdl2 import Window, Renderer

from essentials.math_custom import Vector2D
pygame.init()

proyect_name = 'smol pet'
# SETUP
# If setted to fullscreen then pass the real sizes 
WINDOW = Window(title=proyect_name, borderless=False, size=(1920,1080))
SCREEN_W, SCREEN_H = WINDOW.size

# Renderer (we use the GPU for better performance)
global RENDERER
RENDERER = Renderer(WINDOW, accelerated=1)


SCREEN_CENTER: Vector2D = Vector2D(SCREEN_W*0.5, SCREEN_H*0.5)

FPS:int = 60

# COLORS
CLR_WHITE:tuple[int,int,int] = (255,255,255)
CLR_GREEN:tuple[int,int,int] = (0,255,0)
TRANSPARENT_COLOR = (255, 0, 128)  # Transparency color

## TRANSPARENT WINDOW =========================================================
import time

# 1. Esperar un instante para que Windows registre la creación de la ventana
time.sleep(0.2) 
# 2. Buscar la ventana por su título exacto
# IMPORTANTE: El título debe ser exactamente el mismo que pusiste en Window(title=proyect_name)
hwnd = win32gui.FindWindow(None, proyect_name)
if hwnd != 0:
    # 3. Aplicar estilos de capa (Layered) y ToolWindow (para que no salga en la barra de tareas)
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(
        hwnd, 
        win32con.GWL_EXSTYLE, 
        ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW
    )

    # 4. Establecer el color de transparencia
    win32gui.SetLayeredWindowAttributes(
        hwnd, 
        win32api.RGB(*TRANSPARENT_COLOR), 
        0, 
        win32con.LWA_COLORKEY
    )

    # 5. Mantener siempre al frente
    win32gui.SetWindowPos(
        hwnd, 
        win32con.HWND_TOPMOST, 
        0, 0, 0, 0, 
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )
    print(f"¡Éxito! SmolPet ahora es transparente. Handle: {hwnd}")
else:
    print("Error: No se encontró la ventana proyect_name. Asegúrate de que el título coincida.")

## ============================================================================
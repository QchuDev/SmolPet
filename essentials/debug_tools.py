import pygame
from pygame._sdl2 import Window, Renderer, Texture, Image
from essentials.window_setup import RENDERER


pygame.font.init()

class PerformanceMonitor:
    def __init__(self, font_size=18):
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.clock = pygame.time.Clock()
        self.fps_timer = 0
        self.fps_tex = None
        self.ms_tex = None

    def update(self, dt):
        self.fps_timer += dt
        
        # Actualizamos solo 2 veces por segundo para ahorrar CPU/GPU
        if self.fps_timer > 0.5 or self.fps_tex is None:
            self.fps_timer = 0
            
            # 1. Obtener datos
            current_fps = int(self.clock.get_fps())
            current_ms = self.clock.get_time() # Tiempo del último frame en ms
            
            # 2. Renderizar a Surfaces (CPU)
            fps_surf = self.font.render(f"FPS: {current_fps}", True, (0, 255, 0))
            ms_surf = self.font.render(f"Proc: {current_ms}ms", True, (0, 255, 0))

            # 3. Convertir a Texturas (GPU)
            # Nota: Al reasignar self.fps_tex, la textura anterior se marca para recolección
            self.fps_tex = Texture.from_surface(RENDERER, fps_surf)
            self.ms_tex = Texture.from_surface(RENDERER, ms_surf)

    def render(self):
        if self.fps_tex and self.ms_tex:
            # Fondo semi-transparente para legibilidad
            RENDERER.draw_color = (0, 0, 0, 180)
            RENDERER.fill_rect((5, 5, 110, 50))
            
            # Dibujar textos
            RENDERER.blit(self.fps_tex, dest=pygame.Rect(10, 10, self.fps_tex.width, self.fps_tex.height))
            RENDERER.blit(self.ms_tex, dest=pygame.Rect(10, 30, self.ms_tex.width, self.ms_tex.height))

# Uso:
monitor = PerformanceMonitor()
# ... en el bucle principal ...

import pygame
from pygame._sdl2 import Window, Renderer, Texture, Image
from essentials.window_setup import RENDERER


pygame.font.init()
class PerformanceMonitor:
    def __init__(self, font_size=18):
        self.font = pygame.font.SysFont("Arial", font_size)
        self.clock = pygame.time.Clock()
        self.fps_list = []
        
    def render(self, clock):
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
        
        # Convertimos el texto (Surface) a Textura (GPU)
        fps_tex = Texture.from_surface(RENDERER, fps_text)
        ms_tex = Texture.from_surface(RENDERER, ms_text)

        # --- 2. Dibujar el fondo (En GPU) ---
        # Creamos el rectángulo de fondo
        bg_rect = pygame.Rect(5, 5, 100, 45)

        # Dibujamos un rectángulo con color sólido en el Renderer
        # Nota: draw_color controla el color de las operaciones de dibujo del renderer
        RENDERER.draw_color = (0, 0, 0, 150)
        RENDERER.fill_rect(bg_rect)

        # --- 3. Dibujar los textos (En GPU) ---
        # Definimos rectángulos de destino para cada texto para que no se solapen
        fps_dest = pygame.Rect(10, 10, fps_tex.width, fps_tex.height)
        ms_dest = pygame.Rect(10, 28, ms_tex.width, ms_tex.height)

        RENDERER.blit(fps_tex, dest=fps_dest)
        RENDERER.blit(ms_tex, dest=ms_dest)

monitor = PerformanceMonitor()
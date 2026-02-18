import pygame
pygame.font.init()
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
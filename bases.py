from consts import SCREEN_W, SCREEN_H, SCREEN
import pygame
from physics import PhysicalBall

class Entity():
    def __init__(self, surface:pygame.Surface, physical:PhysicalBall=PhysicalBall()):
        self.surface = surface
        pass
    
    def draw(self):
        SCREEN.blit(self.surface)

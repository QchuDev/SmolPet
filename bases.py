from consts import SCREEN_W, SCREEN_H, SCREEN
import pygame
from physics import PhysicalBall
from math_custom import Vector2D
class Entity():
    def __init__(self, surface:pygame.Surface, phys:PhysicalBall | None = None):
        self.surface = surface
        self.phys = phys
    
    def draw(self, pos:Vector2D = Vector2D(0,0)):
        if self.phys is not None:
            SCREEN.blit(self.surface, (self.phys.pos.x, self.phys.pos.y))
        else:
            SCREEN.blit(self.surface, (pos.x,pos.y))
        


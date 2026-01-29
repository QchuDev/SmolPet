from consts import SCREEN_W, SCREEN_H, SCREEN
import pygame
from pygame import Surface
from physics import PhysicalBall
from math_custom import Vector2D

class Entity():
    def __init__(self, surface:pygame.Surface, phys:PhysicalBall | None = None):
        self.surface = surface
        self.phys = phys
    
    def draw(self, pos:Vector2D = Vector2D(0,0)):
        if self.phys is not None:
            SCREEN.blit(self.surface, (self.phys.pos.x - self.surface.width*0.5, self.phys.pos.y - self.surface.height*0.5))
        else:
            SCREEN.blit(self.surface, (pos.x,pos.y))
    
    def update_surface(self, new_surface:Surface):
        self.surface = new_surface

# Spritesheet: extracts the images of a spritesheet and saves the parts
class SpriteSheet():
    def __init__(self, file_path:str, cell_size=(64,64)) -> None:
        sheet:Surface = pygame.image.load(file_path).convert_alpha()
        w, h = cell_size[0], cell_size[1]
        self.sprites: list[Surface] = []
        i,j = 0,0
        self.size = 0
        while(j < sheet.get_height()):

            rect = pygame.Rect(i, j, w, h)

            sprite:Surface = sheet.subsurface(rect).copy()
            print(f'pos {i,j}\tsize {w,h}\t->{sprite}')

            self.sprites.append(sprite)

            if i + w >= sheet.get_width():
                i = 0
                j += h
            else:
                i += w
        self.size = len(self.sprites)


    def get_sprite(self, index:int) -> Surface:
        return self.sprites[index]

class Animator():
    def __init__(self, ss:SpriteSheet, anims:dict[str, list[int]]) -> None:
        self.ss:SpriteSheet = ss
        self.anims = anims

        self.current_anim:str = ''
        self.current_frame:int = 0

    def play(self, anim_name:str):
        for name in self.anims.keys():
            if name != anim_name:
                continue
            ## WIP
import pygame
import win32api
from abc import ABC, abstractmethod


# Custom
from consts import SCREEN_W, SCREEN_H, SCREEN
from consts import SCREEN_W, SCREEN_H
from consts import GRAVITY, BOUNCE_STOP, SLIDE_STOP, USER_PULL_DAMPING, USER_PULL_STRENGTH
from pygame import Surface
from math_custom import Vector2D

# =====================================================================================
#                               ESSENTIALS
# =====================================================================================

class Entity():
    def __init__(self, image:pygame.Surface, components:list[Component] = []):
        self.components = components 

        self.pos = Vector2D(0,0)
        self.image = image

    # Draws the entity image 
    def draw(self):
        SCREEN.blit(self.image, (self.pos.x - self.image.width*0.5 , self.pos.y - self.image.height*0.5))
    
    # Updates everycomponent
    def update(self, delta_time:float):
        for comp in self.components:
            comp.update(self, delta_time)

    # Adds a new component
    def add_component(self, new_comp):
        self.components.append(new_comp)

    def get_component(self, component_type):

        for c in self.components:
            if isinstance(c, component_type):
                return c
        
        return None

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
            # print(f'pos {i,j}\tsize {w,h}\t->{sprite}')

            self.sprites.append(sprite)

            if i + w >= sheet.get_width():
                i = 0
                j += h
            else:
                i += w
        self.size = len(self.sprites)


    def get_sprite(self, index:int) -> Surface:
        return self.sprites[index]

    def update(self, entity:Entity):
        pass

# Interface of the Components ("what should they have")
class Component(ABC):
    def __init__(self) -> None:
        self.name = ''
    @abstractmethod
    def update(self, entity:Entity, delta_time:float):
        pass
    


# =====================================================================================
#                               COMPONENTS
# =====================================================================================


# Animator: decides which is the next frame from a group of animations
class Animator(Component):
    def __init__(self, ss:SpriteSheet, anims:dict[str, list[int]], entity:Entity) -> None:
        self.name = 'Animator'

    def update(self, entity:Entity):
        SCREEN.blit(entity.image, (entity.pos.x, entity.pos.y))
        pass

    def play(self):
        pass

# PhysicalBall: the one in charge of following the rules of physics updating itself
class PhysicalBall(Component):

    def __init__(self, pos=(SCREEN_W * 0.5, SCREEN_H * 0.5), vel = (0,0), mass=1, radius=1, air_resist=0.5, retention_x=0.8, retention_y=0.4):
        self.name = 'PhysicalBall'
        
        self.pos:Vector2D = Vector2D(pos[0], pos[1])
        self.vel:Vector2D = Vector2D(vel[0], vel[1])
        self.acc:Vector2D = Vector2D(0,0)
        self.mass:float = max(0.001, mass)
        self.radius:float = max(0.001, radius)
        self.air_resist:float = air_resist
        self.retention_x = retention_x
        self.retention_y = retention_y

    # Applying gravity and normal floor force
    def gravityEffect(self) -> None:
        self.acc.x += GRAVITY.x
        self.acc.y += GRAVITY.y

        if self.pos.y >= SCREEN_H - self.radius:
            self.pos.y = SCREEN_H - self.radius
            
            if abs(self.vel.x) > SLIDE_STOP:
                self.vel.x *= self.retention_x
            else:
                self.vel.x = 0
            
            if abs(self.vel.y) > BOUNCE_STOP:
                self.vel.y *= -self.retention_y
            else:
                self.vel.y = 0
                self.applyForce(-GRAVITY)

    # Apply a force to the entity
    def applyForce(self, force:Vector2D, show_info=False) -> None:
        mass = self.mass
        #Update Acceleration
        self.acc.x += force.x/mass
        self.acc.y += force.y/mass

        # Show the applied force and the current acceleration
        if show_info:
            print(f'Force applied: ({force.x}, {force.y})')
            print(f'Mass: {mass} || Added Acc: ({force.x/mass}, {force.y/mass})')
            print()
            print(f'New Acceleration = {self.acc}')
            print()
    
    # Checks for walls and pushes the entity
    def wallsPush(self):
        # Right wall
        if self.pos.x >= SCREEN_W-self.radius and self.vel.x > 10:
            self.pos.x = SCREEN_W - self.radius
            self.vel.x = -self.vel.x * self.retention_x
                
        # Left wall
        if self.pos.x <= self.radius and self.vel.x < -10:
            self.pos.x = self.radius
            self.vel.x = -self.vel.x * self.retention_x
    
    # Drag of the entity
    def airForce(self):
        # Air resistance
        drag_dir = -self.vel.normalized()
        self.applyForce(drag_dir*self.air_resist*(self.vel.dot(self.vel)))


    # Update call from the entity
    def update(self, entity:Entity, delta_time:float):

        # Acceleration downwards by gravity 
        self.gravityEffect()
        self.wallsPush()
        self.airForce()

        # Update physical state
        self.vel += self.acc*delta_time
        self.pos += self.vel*delta_time
        self.acc.x = 0
        self.acc.y = 0

        entity.pos = self.pos

class MouseDrag(Component):
    def __init__(self) -> None:
        self.name = 'MouseDrag'
        # Mouse variables
        self.mouse_pos:Vector2D = Vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        self.is_pulling = False
        self.phys_ball:PhysicalBall | None = None



    def update(self, entity: Entity, delta_time: float):
        if self.phys_ball is None:
            comp = entity.get_component(PhysicalBall)
            if isinstance(comp, PhysicalBall):
                self.phys_ball = comp 
            
            if not self.phys_ball:
                print(f"{entity}: Has not a PhysicsBall Component. It's required if using MouseDrag")
                return
        
        left_click_state = win32api.GetAsyncKeyState(0x01)

        if left_click_state & 0x8000:
            m_x, m_y = win32api.GetCursorPos()
            self.mouse_pos.x  = m_x
            self.mouse_pos.y  = m_y
            
            self.pos_diff = self.mouse_pos - self.phys_ball.pos
            self.diff_mag = self.pos_diff.magnitude()
            
            if self.diff_mag <= self.phys_ball.radius + 5:
                self.is_pulling = True
        else:
            self.is_pulling = False

        if self.is_pulling:
            self.phys_ball.applyForce((self.pos_diff*USER_PULL_STRENGTH) - self.phys_ball.vel*USER_PULL_DAMPING)

        
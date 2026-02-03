import pygame
import win32api
from abc import ABC, abstractmethod
import random
from typing import TypeVar, Type, Optional
import math
# Custom
from consts import SCREEN_W, SCREEN_H, SCREEN
from consts import SCREEN_W, SCREEN_H
from consts import GRAVITY, BOUNCE_STOP, SLIDE_STOP, USER_PULL_DAMPING, USER_PULL_STRENGTH
from consts import SPLAT_SPEED
from pygame import Surface
from math_custom import Vector2D

# =====================================================================================
#                               ESSENTIALS
# =====================================================================================
T = TypeVar('T', bound='Component')
class Entity():
    def __init__(self, image:pygame.Surface, components:list[Component] = []):
        self.components = components 
        self.pos = Vector2D(0,0)
        self.rotation:float = 0 # counterclockwise angle
        self.image = image

    # Draws the entity image 
    def draw(self):
        SCREEN.blit(self.image, (self.pos.x - self.image.width*0.5 , self.pos.y - self.image.height*0.5))
    
    # Updates everycomponent
    def update(self, dt:float):
        for comp in self.components:
            comp.update(self, dt)

    # Adds a new component
    def add_component(self, new_comp):
        self.components.append(new_comp)

    def get_component(self, component_type: Type[T]) -> Optional[T]:
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
            
            self.sprites.append(sprite)

            if i + w >= sheet.get_width():
                i = 0
                j += h
            else:
                i += w
        self.size = len(self.sprites)

    def get_sprite(self, index:int) -> Surface:
        return self.sprites[index]

# Interface of the Components ("what should they have")
class Component(ABC):
    
    @abstractmethod
    def update(self, entity:Entity, dt:float):
        pass
    
class Animation():
    def __init__(self, name:str, seq:list[int], loop:bool = True, frame_duration:float = 0.1) -> None:
        self.name = name
        self.seq = seq
        self.loop = loop
        self.frame_duration = frame_duration

# =====================================================================================
#                               COMPONENTS
# =====================================================================================

# Animator: decides which is the next frame from a group of animations
class Animator(Component):
    def __init__(self, ss:SpriteSheet, anims:list[Animation]) -> None:
        
        self.frame_idx:int = 0
        
        self.ss = ss
        self.anims: dict[str, Animation] = {a.name: a for a in anims}

        self.timer:float = 0
        
        self.current_anim: Animation | None = list(self.anims.values())[0] if self.anims else None        

    def update(self, entity:Entity, dt:float):
        if not self.current_anim:
            return
        
        self.timer += dt

        if self.timer >= self.current_anim.frame_duration:
            self.timer = 0.0
            sprite_id=0
            if self.current_anim.loop or self.frame_idx < len(self.current_anim.seq)-1:
                self.frame_idx = (self.frame_idx + 1) % len(self.current_anim.seq)
                sprite_id = self.current_anim.seq[self.frame_idx]

            entity.image = self.ss.get_sprite(sprite_id)

    def play(self, name:str, entity:Entity):
        if self.current_anim and self.current_anim.name == name:
            return
        
        if name in self.anims:
            self.current_anim = self.anims[name]
            self.frame_idx = 0
            self.timer = 0

            sprite_id = self.current_anim.seq[self.frame_idx]
            entity.image = self.ss.get_sprite(sprite_id)

    def is_finished(self) -> bool:
        if self.current_anim: 
            if self.current_anim.loop: return False
            
            return self.frame_idx == len(self.current_anim.seq) - 1
        
        
        print(f'Error: there is no animation playing')
        return False
    
# PhysicalBall: the one in charge of following the rules of physics updating itself
class PhysicalBall(Component):

    def __init__(self, pos=(SCREEN_W * 0.5, SCREEN_H * 0.5), vel = (0,0), mass=1, radius=1, air_resist=0.5, retention_x=0.8, retention_y=0.4):
        self.update_priority: int = 10
        
        self.pos:Vector2D = Vector2D(pos[0], pos[1])
        self.vel:Vector2D = Vector2D(vel[0], vel[1])
        self.acc:Vector2D = Vector2D(0,0)
        self.mass:float = max(0.001, mass)
        self.radius:float = max(0.001, radius)
        self.air_resist:float = air_resist
        self.retention_x = retention_x
        self.retention_y = retention_y

        self.is_hitting_floor: bool = False

    # Applying gravity and normal floor force
    def gravityEffect(self) -> None:
        self.acc.x += GRAVITY.x
        self.acc.y += GRAVITY.y

        if self.pos.y >= SCREEN_H - self.radius:
            if abs(self.vel.y) > SPLAT_SPEED:
                self.is_hitting_floor = True

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
    def update(self, entity:Entity, dt:float):

        # Acceleration downwards by gravity 
        self.gravityEffect()
        self.wallsPush()
        self.airForce()
        
        # Update physical state
        self.vel += self.acc*dt
        self.pos += self.vel*dt
        self.acc.x = 0
        self.acc.y = 0

        entity.pos = self.pos
        
# MouseDrag lets the entity get dragged with physics by the mouse
class MouseDrag(Component):
    def __init__(self) -> None:
        # Mouse variables
        self.mouse_pos:Vector2D = Vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        self.is_pulling = False
        self.phys_ball:PhysicalBall | None = None
        self.animator: Animator | None = None


    def update(self, entity: Entity, dt: float):
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


# =====================================================================================
#                                   W.I.P                                
# =====================================================================================
# Script to take the desicions of the NPC

# ...
class AIController(Component):
    
    def __init__(self, timer_range:tuple[float,float] = (1,3)) -> None:
        self.phys_ball: PhysicalBall | None = None
        self.timer_range:tuple[float, float] = timer_range

        self.max_time: float = 1.0
        self.timer: float = 0.0

        self.desicions: list[str] = ['move', 'talk', 'wait'] 

    def decide(self, entity:Entity):
        # Update max_time
        self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])
        
        if not self.phys_ball: self.phys_ball = entity.get_component(PhysicalBall)
        if not self.phys_ball: return
        
        if entity.pos.y > SCREEN_H*0.95: 
            self.phys_ball.applyForce(Vector2D(random.randint(-1,1)*4000, -10000))

    def update(self, entity:Entity, delta_tine:float):
        if self.phys_ball is None:
            comp = entity.get_component(PhysicalBall)
            if isinstance(comp, PhysicalBall):
                self.phys_ball = comp
        
        self.timer += delta_tine

        if self.timer > self.max_time:
            self.timer = 0
            self.decide(entity)

# Component who decides the current animation to be played
class StatesManager(Component):
    def __init__(self) -> None:
        self.current_state = 'idle'
        self.animator: Animator | None = None
        self.phys: PhysicalBall | None = None


    def update(self, entity:Entity, dt:float):
        if not self.animator: self.animator = entity.get_component(Animator)
        if not self.phys: self.phys = entity.get_component(PhysicalBall)

        self.handle_logic(entity)


    def handle_logic(self, entity:Entity):
        if not self.animator or not self.phys: return

        match self.current_state:

            case 'idle':
                if self.phys.pos.y < SCREEN_H - self.phys.radius:
                    self.change_state('air', entity)
                elif self.phys.is_hitting_floor:
                    self.change_state('hit_floor', entity)
            case 'air':
                if self.phys.pos.y >= SCREEN_H - self.phys.radius:
                    self.change_state('idle', entity)
                elif self.phys.is_hitting_floor:
                    self.change_state('hit_floor', entity)
            case 'hit_floor':
                if self.animator.is_finished():
                    self.phys.is_hitting_floor = False

                    if self.phys.pos.y >= SCREEN_H - self.phys.radius:
                        self.change_state('idle', entity)
                    elif self.phys.is_hitting_floor:
                        self.change_state('hit_floor', entity)

    def change_state(self, new_state:str, entity:Entity):
        if self.current_state != new_state:
            self.current_state = new_state
            if self.animator:
                self.animator.play(new_state, entity)
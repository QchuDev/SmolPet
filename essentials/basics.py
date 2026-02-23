import pygame
from pygame import Rect, Surface
import random
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional
from pygame._sdl2 import Texture

# Custom
from .math_custom import Vector2D
from .window_setup import RENDERER, WINDOW




# =====================================================================================
#                               BASIC MANAGERS AND CLASSES
# =====================================================================================

class Input:
    mouse_pos = Vector2D(0,0)
    left_clicked = False

# This objects is in charged of presenting all entities needed as fast as possible
class World:
    entities: list[Entity] = []
    def spawn_entity(self, new_entity:Entity):
        self.entities.append(new_entity)

# The one in charge of all Particles
class ParticlesManager:
    def __init__(self):
        # The states of each particle is represented by: [x,y, vx,vy, lifetime, id, state, accy]
        self.particles = []
        self.textures = Texture.from_surface(RENDERER, pygame.image.load('resources/images/particles_8.png'))
        ss = SpriteSheet('resources/images/particles_8.png', cell_size=(8,8), scale_factor=4)
        temp_texture: list[Texture] = ss.right_textures
        self.w, self.h = ss.sprite_w, ss.sprite_h
        self.uvs = {
            'spark': temp_texture[0:4],
            'popcorn': temp_texture[4:8],
            'heart': temp_texture[8:12],
        }

    # add to the particles array the new particles to be rendered by the draw()
    def emit(self, x,y, particle_type:str, mid_lifetime=1.0, ammount:int=1, force=2.0, accy=0):
        for _ in range(ammount):
            vx=random.uniform(-force, force)
            vy=random.uniform(-force, force)

            # Some randomness for variation
            lifetime = mid_lifetime*random.uniform(0.8, 1.2)

            self.particles.append([x,y ,vx,vy, lifetime, particle_type, 0, mid_lifetime, accy])

    # update the state of each particle
    def update(self, dt):
        for i in range(len(self.particles)-1, -1, -1):
            p = self.particles[i]
            p[0]+= p[2] # x += vx
            p[1]+= p[3] # y += vy

            # Acceleration in y axis
            p[3] += p[8]
            
            p[4] -= dt  # lifetime -= dt
            if p[4]<0:
                self.particles.pop(i)   # remove particle if its time is over

            # Update state 
            if      p[4]>0.8*p[7]:   p[6] = 0
            elif    p[4]>0.6*p[7]:   p[6] = 1
            elif    p[4]>0.4*p[7]:   p[6] = 2
            else:                    p[6] = 3
    
    # draws all the particles at once 
    def draw(self):
        for p in self.particles:
            texture = self.uvs[p[5]][p[6]]
            rect = Rect(p[0]-self.w*0.5, p[1]-self.h*0.5, self.w, self.h)
            RENDERER.blit(texture, rect)

T = TypeVar('T', bound='Component')
class Entity():
    __slots__ = ['components', 'pos', 'scale', 'texture', 'name', 'facing', 'active']

    def __init__(self, texture:Texture | None = None, name:str = 'no_name', components:list[Component] = []):
        self.components = components 
        self.pos:   Vector2D = Vector2D(0,0)
        self.scale: Vector2D = Vector2D(1,1)

        self.texture: Texture | None  = texture

        self.name:  str = name
        self.facing:int = 1
        self.active:bool = True

    # Called once at the very beggining
    def start(self):
        for comp in self.components:
            comp.start(self)

    # Draws the entity image 
    def draw(self):
        # Dont do a thing if inactive
        if not self.active or not self.texture: return

        # Dont draw if not visible
        if self.pos.y < -20: return
        
        s_x = self.scale.x*self.texture.width
        s_y = self.scale.y*self.texture.height
        draw_x = self.pos.x - s_x * 0.5
        draw_y = self.pos.y - s_y * 0.5
        dest_rect = Rect(draw_x, draw_y, s_x, s_y)

        
        # WIP CHANGING THE WAY OF DRAWING ON SCREEN
        RENDERER.blit(
            source = self.texture, 
            dest = dest_rect
        )

        for c in self.components:
            c.draw()

        
    # Updates everycomponent
    def update(self, dt:float):
        # Dont do a thing if inactive
        if not self.active: return
        for comp in self.components:
            comp.update(dt)

    # Adds a new component
    def add_component(self, new_comp):
        self.components.append(new_comp)

    def get_component(self, component_type: Type[T]) -> Optional[T]:
        for c in self.components:
            if isinstance(c, component_type):
                return c
        
        return None

# Interface of the Components ("what should they have")
class Component(ABC):
    __slots__ = ['parent']

    # A component only has to know its parent
    def __init__(self) -> None:
        self.parent: Entity = Entity()
    
    # Ref the parent of the component
    def start(self, entity:Entity):
        self.parent = entity
        if not self.parent: 
            raise Exception(f"No parent detected for {self.__class__.__name__}")

    def update(self, dt:float):
        pass

    def draw(self):
        pass

# Spritesheet: extracts the images of a spritesheet and saves the parts
class SpriteSheet():
    __slots__ = ['texture', 'sprite_w', 'sprite_h', 'surfaces', 'right_textures', 'left_textures']
    def __init__(self, file_path:str, cell_size=(64,64), scale_factor=1) -> None:
        self.surfaces: list[Surface] = []
        self.right_textures: list[Texture] = []
        self.left_textures: list[Texture] = []
        
        if file_path == '': return
        sheet:Surface = pygame.image.load(file_path)

        # Scaling sheet and also width and height
        if scale_factor != 1:
            new_size = (sheet.get_width() * scale_factor, sheet.get_height() * scale_factor)
            sheet = pygame.transform.scale(sheet, new_size)
            w, h = cell_size[0] * scale_factor, cell_size[1] * scale_factor
        else:
            w, h = cell_size[0], cell_size[1]

        # CREATING THE TEXTURE AT VRAM
        self.texture = Texture.from_surface(RENDERER, sheet)
        
        
        sheet_w, sheet_h = sheet.get_size()
        step_w = int(w)
        step_h = int(h)
        # Cutting the sheet to sprites
        for j in range(0, sheet_h, step_h):
            for i in range(0, sheet_w, step_w):
                rect = pygame.Rect(i, j, w, h)
                sprite_surf = sheet.subsurface(rect)
                self.surfaces.append(sprite_surf)
                self.right_textures.append(Texture.from_surface(RENDERER, sprite_surf))
                self.left_textures.append(Texture.from_surface(RENDERER, pygame.transform.flip(sprite_surf, True, False)))
                
                print(f"DEBUG: Sheet size: {sheet_w}x{sheet_h} | Step: {step_w}x{step_h}")

        self.sprite_w, self.sprite_h = w, h
        
    def get_sprite(self, index:int) -> Surface: 
        return self.surfaces[index]
    
    def get_texture(self, index:int, flipped:bool=False) -> Texture: 
        return self.right_textures[index] if not flipped else self.left_textures[index]

# Animation: has name, a sequence of indexes, frame duration and if its a loop
class Animation():
    __slots__ = ['name', 'seq', 'loop', 'frame_duration']
    def __init__(self, name:str, seq:list[int], loop:bool = True, frame_duration:float = 0.1) -> None:
        self.name = name
        self.seq = seq
        self.loop = loop
        self.frame_duration = frame_duration

# CharacterData: has name, phrases and a SpriteSheet
class CharacterData():
    __slots__ = ['name', 'phrases', 'ss']
    def __init__(self, ss: SpriteSheet, name:str, phrases:list[str] = []):
        self.name:      str = name
        self.phrases:   list[str] = phrases
        self.ss:        SpriteSheet = ss

# State:
class State():
    __slots__ = ['name', 'transitions']
    def __init__(self, name:str = '', trans: list[Transition] = []):
        self.name:  str = name
        self.transitions:  list[Transition] = trans
    
    # Returns the next states name
    def transition(self, entity:Entity) -> str:
        next_state: str = self.name
        for t in self.transitions:
            if t.check(entity):
                next_state = t.to_state
                break
        return next_state

# Transition: 
class Transition():
    __slots__ = ['to_state', 'condition']
    def __init__(self, to_state: str, condition):
        self.to_state = to_state
        self.condition = condition
    
    def check(self, entity:Entity) -> bool:
        return self.condition(entity)

# WIP
# This class is in charge of checking for possible events, such as achievements or special moments.
class EventsManager:
    pass

class Event():
    def __init__(self, condition , spawns=[]) -> None:
        pass
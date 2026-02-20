import pygame
import random
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Optional

# Custom
from pygame import Surface
from .math_custom import Vector2D
from .window_consts import SCREEN




# =====================================================================================
#                               BASIC MANAGERS AND CLASSES
# =====================================================================================


# This objects is in charged of presenting all entities needed as fast as possible
class World:
    entities: list[Entity] = []

# The one in charge of all Particles
class ParticlesManager:
    def __init__(self):
        # The states of each particle is represented by: [x,y, vx,vy, lifetime, id, state, accy]
        self.particles = []

        temp_sprites = SpriteSheet('resources/images/particles_8.png', cell_size=(8,8), scale_factor=4).sprites
        self.textures = {
            'spark': temp_sprites[0:4],
            'popcorn': temp_sprites[4:8],
            'heart': temp_sprites[8:12],
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
            img = self.textures[p[5]]
            SCREEN.blit(img[p[6]], (int(p[0]), int(p[1])))

T = TypeVar('T', bound='Component')
class Entity():
    __slots__ = ['components', 'pos', 'image', 'name', 'facing', 'active']

    def __init__(self, image:pygame.Surface = Surface((0,0)), name:str = 'no_name', components:list[Component] = []):
        self.components = components 
        self.pos:   Vector2D = Vector2D(0,0)
        self.image: Surface = image
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
        if not self.active: return

        # Dont draw if not visible
        if self.pos.y < -20: return

        for c in self.components:
            c.draw()

        # Flip if necessary
        if self.facing == -1:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        else:
            image_to_draw = self.image

        SCREEN.blit(image_to_draw, (int(self.pos.x - self.image.width*0.5) , int(self.pos.y - self.image.height*0.5)))

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
    __slots__ = ['sprites', 'size']
    def __init__(self, file_path:str, cell_size=(64,64), scale_factor=1) -> None:
        if file_path == '': return
        sheet:Surface = pygame.image.load(file_path).convert_alpha()
        w, h = cell_size[0], cell_size[1]
        
        self.sprites: list[Surface] = []

        i,j = 0,0
        self.size = 0
        while(j < sheet.get_height()):

            rect = pygame.Rect(i, j, w, h)

            sprite:Surface = sheet.subsurface(rect).copy()
            
            # Scale de sprites
            new_size = (sprite.get_width()*scale_factor, sprite.get_height()*scale_factor)
            sprite = pygame.transform.scale(sprite, new_size)

            self.sprites.append(sprite)

            if i + w >= sheet.get_width():
                i = 0
                j += h
            else:
                i += w
        self.size = len(self.sprites)

    def get_sprite(self, index:int) -> Surface:
        return self.sprites[index]

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

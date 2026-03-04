import copy
import json
import os

import win32api

import pygame
from pygame import Rect, Surface
import random
from abc import ABC
from typing import TypeVar, Type, Optional
from pygame._sdl2 import Texture



# Custom
from .math_custom import Vector2D
from .window_setup import RENDERER, SCREEN_W, WINDOW

def smart_copy(target, memo=None):
    if memo is None: memo = {}
    
    # 1. Si es un tipo básico o None, devolver tal cual
    if target is None or isinstance(target, (int, float, str, bool)):
        return target
    
    # 2. Si es un objeto de Pygame/SDL2, NO clonar, solo pasar la referencia
    t_name = type(target).__name__
    if t_name in ('Texture', 'Font', 'Surface', 'Renderer', 'Context'):
        return target
        
    # 3. Para todo lo demás, dejar que Python haga su magia
    # Esto ahora funcionará perfecto porque hay __dict__
    return copy.deepcopy(target, memo)
def _bypass_pickle(obj, memo):
    return obj

# 2. Registramos la regla para Texturas y Fuentes de SDL2
# Esto afecta a TODO el programa, incluyendo deepcopy dentro de listas/dicts
copy._deepcopy_dispatch[pygame._sdl2.video.Texture] = _bypass_pickle # type: ignore
try:
    copy._deepcopy_dispatch[pygame.font.Font] = _bypass_pickle # type: ignore
except:
    pass

# =====================================================================================
#                               BASIC MANAGERS AND CLASSES
# =====================================================================================
  
    
# This objects is in charged of presenting all entities needed as fast as possible
class World:
    entities: list[Entity] = []
    def spawn_entity(self, new_entity:Entity):
        self.entities.append(new_entity)

# Gets both clicks and the position of the mouse at the screen
class MouseInput:
    pos = Vector2D(0,0)
    left_clicked: bool = False
    right_clicked: bool = False

    @classmethod
    def update(cls) -> None:
        cls.pos.x, cls.pos.y = win32api.GetCursorPos()
        cls.left_clicked = bool(win32api.GetAsyncKeyState(0x01) & 0x8000)
        cls.right_clicked = bool(win32api.GetAsyncKeyState(0x02) & 0x8000)
    
    @classmethod
    def mouse_pos(cls) -> Vector2D:
        return cls.pos

# An entity has name, position, texture, scale and a set of compoenents to create new behavior
T = TypeVar('T', bound='Component')
class Entity():

    def __init__(self,  pos:Vector2D = Vector2D(0,0), texture:Texture | None = None, name:str = 'no_name', components:list[Component] = []):
        self.components = components 
        self.pos:   Vector2D = pos
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

    # Gives the component asked for and if not found -> None
    def get_component(self, component_type: Type[T]) -> Optional[T]:
        if not self.active: return None
        for c in self.components:
            if isinstance(c, component_type):
                return c
        
        return None

    # Returns a copy itself, copying components and everything
    def clone(self):
        # Con el parche global y sin slots, esto es ahora 100% seguro
        new_ent = copy.deepcopy(self)
        
        # Re-vinculamos los componentes al nuevo clon
        for comp in new_ent.components:
            comp.parent = new_ent
            
        return new_ent
    
    def __deepcopy__(self, memo):
        # Creamos la instancia nueva
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        
        # Copiamos el diccionario de atributos (__dict__)
        for k, v in self.__dict__.items():
            if k == 'parent':
                # Evitamos copiar al padre para no entrar en bucle infinito
                setattr(result, k, None)
            else:
                # El parche global de arriba se encargará de las texturas
                # aquí, incluso si están dentro de listas o diccionarios.
                setattr(result, k, copy.deepcopy(v, memo))
                
        return result

# Father of all Components ("what should they have")
class Component(ABC):

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

    def __deepcopy__(self, memo):
        # Creamos la instancia nueva
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        
        # Copiamos el diccionario de atributos (__dict__)
        for k, v in self.__dict__.items():
            if k == 'parent':
                # Evitamos copiar al padre para no entrar en bucle infinito
                setattr(result, k, None)
            else:
                # El parche global de arriba se encargará de las texturas
                # aquí, incluso si están dentro de listas o diccionarios.
                setattr(result, k, copy.deepcopy(v, memo))
                
        return result

# Spritesheet: extracts the images of a spritesheet and saves the parts
class SpriteSheet():
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

        self.sprite_w, self.sprite_h = w, h
        
    def get_sprite(self, index:int) -> Surface: 
        return self.surfaces[index]
    
    def get_texture(self, index:int, flipped:bool=False) -> Texture: 
        return self.right_textures[index] if not flipped else self.left_textures[index]


# Animation: has name, a sequence of indexes, frame duration and if its a loop
class Animation():
    def __init__(self, name:str, seq:list[int], loop:bool = True, frame_duration:float = 0.1) -> None:
        self.name = name
        self.seq = seq
        self.loop = loop
        self.frame_duration = frame_duration

# CharacterData: has name, phrases and a SpriteSheet
class CharacterData():
    def __init__(self, ss: SpriteSheet, name:str, phrases:list[str] = []):
        self.name:      str = name
        self.phrases:   list[str] = phrases
        self.ss:        SpriteSheet = ss

class EntityContext:
    def __init__(self, entity):
        from .components import PhysicalBall, Animator, AIController
        # Cacheamos los componentes una sola vez al inicio del estado
        self.phys = entity.get_component(PhysicalBall)
        self.anim = entity.get_component(Animator)
        self.aic = entity.get_component(AIController)
        self.entity = entity # Por si acaso
 
# State: a name and has a set of transitions
class State():
    def __init__(self, name:str = '', trans: list[Transition] = []):
        self.name:  str = name
        self.transitions:  list[Transition] = trans
    
    # Returns the next states name
    def transition(self, ctx:EntityContext) -> str:
        next_state: str = self.name
        for t in self.transitions:
            if t.check(ctx):
                next_state = t.to_state
                break
        return next_state

# Transition: has a conditions and the state that it goes to 
class Transition():
    def __init__(self, to_state: str, condition):
        self.to_state = to_state
        self.condition = condition
    
    def check(self, ctx:EntityContext) -> bool:
        return self.condition(ctx)

# The one in chraged of storing all the UI elements and calling their update methods
class UIManager:
    ui_elements: list[UIElement] = []

# This class is in charge of checking for possible events, such as achievements or special moments.
U = TypeVar('U', bound='UIComponent')
class UIElement():
    def __init__(self, name:str='', rect:Rect=Rect(0,0, 8,8), texture:Texture|None = None, source_area:Rect=Rect(0,0, 16,16), ui_components:list[UIComponent]=[]) -> None:
        self.name: str = name
        
        self.pos: Vector2D = Vector2D(rect[0], rect[1])
        self.size: Vector2D = Vector2D(rect[2], rect[3])

        self.texture : Texture|None = texture
        self.source_area: Rect = source_area

        self.components: list[UIComponent] = ui_components
        self.show: bool = True
    
    def start(self):
        for ui_c in self.components:
            ui_c.start(self)

    def update(self, dt:float):
        for ui_c in self.components:
            ui_c.update(dt)

    def draw(self):
        if self.texture: 
            dest_rect = Rect(*self.pos, *self.size)
            RENDERER.blit(self.texture, dest_rect, self.source_area)
        
        for ui_c in self.components:
            ui_c.draw()
    
    def get_component(self, component_type: Type[U]) -> Optional[U]:
        for c in self.components:
            if isinstance(c, component_type):
                return c
        
        return None

# Father of all Components ("what should they have")
class UIComponent(ABC):

    # A component only has to know its parent
    def __init__(self) -> None:
        self.parent: UIElement = UIElement()
    
    # Ref the parent of the component
    def start(self, ui_element:UIElement):
        self.parent = ui_element
        if not self.parent: 
            raise Exception(f"No parent detected for {self.__class__.__name__}")

    def update(self, dt:float):
        pass

    def draw(self):
        pass

# A listener can hear the input of a button when happens, then acts according 
class Listener(ABC):
    def hear(self):
        pass

# Class in charge of saving and loading the data from and to the json file save_data
class PersistenceManager:
    SAVE_FILE = 'saves/save_data.json'

    @classmethod
    def save(cls, entities: list[Entity]):
        entity_data=[]
        skipped_ents = [
            'popcorn bucket', 
            'tiramisu', 
            'red balloon',
            'blue balloon',
            'yellow balloon',
            'green balloon',
            'poop',
            'coke'
        ]
        
        for ent in entities:
            if ent.name in skipped_ents: continue

            # We only save the name of the entity for now
            entity_data.append(
                {
                    'name':ent.name
                }
            )
        
        from achievements import get_save_data
        achievement_data = get_save_data()

        full_data = {
            'entities': entity_data,
            'achievements': achievement_data
        }

        with open(cls.SAVE_FILE, 'w') as f:
            json.dump(full_data, f, indent=4)
        print(full_data)
        print()
        print('Changes saved')

    @classmethod
    def load(cls):
        if not os.path.exists(cls.SAVE_FILE):
            return None
        try:
            with open(cls.SAVE_FILE,'r') as f:
                return json.load(f)
        except:
            return None

# Class in charge of the sound effects
class SFXManager:
    
    sounds: dict[str, pygame.mixer.Sound] = {
        'unlock':           pygame.mixer.Sound('resources/sounds/achievement_unlock.wav'),
        'unlock2':          pygame.mixer.Sound('resources/sounds/achievement_unlock_2.wav'),
        'sparks':          pygame.mixer.Sound('resources/sounds/sparks.wav'),
        'hit':          pygame.mixer.Sound('resources/sounds/hit.wav'),
        'break':          pygame.mixer.Sound('resources/sounds/break.wav'),
    }

    @classmethod
    def play(cls, sound:str, volume_mult:float = 1):
        if sound in cls.sounds:
            from game_consts import SFX_VOLUME
            s = cls.sounds[sound]
            s.set_volume(SFX_VOLUME*volume_mult)
            s.play()

# The one in charge of all Particles
class ParticlesManager:
    # The states of each particle is represented by: [x,y, vx,vy, lifetime, id, state, accy]
    particles = []
    textures = Texture.from_surface(RENDERER, pygame.image.load('resources/images/particles_8.png'))
    ss = SpriteSheet('resources/images/particles_8.png', cell_size=(8,8), scale_factor=4)
    temp_texture: list[Texture] = ss.right_textures
    w, h = ss.sprite_w, ss.sprite_h
    uvs = {
        'spark': temp_texture[0:4],
        'popcorn': temp_texture[4:8],
        'heart': temp_texture[8:12],
        'chocolate': temp_texture[12:16],
        'popcorn_break': temp_texture[16:20],
        'tiramisu_break': temp_texture[20:24]
    }

    # add to the particles array the new particles to be rendered by the draw()
    @classmethod
    def emit(cls, x,y, particle_type:str, mid_lifetime=1.0, ammount:int=1, force=2.0, accy=0, dir:int = 0):
        for _ in range(ammount):
            vx=random.uniform(-force, force)
            vy=random.uniform(-force, force)

            if dir != 0:
                vx = abs(vx) * dir

            # Some randomness for variation
            lifetime = mid_lifetime*random.uniform(0.8, 1.2)

            cls.particles.append([x,y ,vx,vy, lifetime, particle_type, 0, mid_lifetime, accy])

    # update the state of each particle
    @classmethod
    def update(cls, dt):
        for i in range(len(cls.particles)-1, -1, -1):
            p = cls.particles[i]
            p[0]+= p[2] # x += vx
            p[1]+= p[3] # y += vy

            # Acceleration in y axis
            p[3] += p[8]
            
            # Update state 
            if      p[4]>0.8*p[7]:   p[6] = 0
            elif    p[4]>0.6*p[7]:   p[6] = 1
            elif    p[4]>0.4*p[7]:   p[6] = 2
            else:                    p[6] = 3

            p[4] -= dt  # lifetime -= dt
            if p[4]<0:
                cls.particles.pop(i)   # remove particle if its time is over

    
    # draws all the particles at once 
    @classmethod
    def draw(cls):
        for p in cls.particles:
            texture = cls.uvs[p[5]][p[6]]
            rect = Rect(p[0]-cls.w*0.5, p[1]-cls.h*0.5, cls.w, cls.h)
            RENDERER.blit(texture, rect)

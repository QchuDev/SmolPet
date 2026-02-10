import pygame
import win32api
from abc import ABC, abstractmethod
import random
from typing import TypeVar, Type, Optional

# Custom
from consts import SCREEN_W, SCREEN_H, SCREEN
from consts import SCREEN_W, SCREEN_H
from consts import GRAVITY, BOUNCE_STOP, SLIDE_STOP, USER_PULL_DAMPING, USER_PULL_STRENGTH, SPLAT_VELOCITY
from consts import CUCHU_PHRASES, WAIT_TIME, JUMP_FORCE, TARGET_STOP
from pygame import Surface
from math_custom import Vector2D

# =====================================================================================
#                               ESSENTIALS
# =====================================================================================
T = TypeVar('T', bound='Component')
class Entity():
    def __init__(self, image:pygame.Surface, components:list[Component] = []):
        self.components = components 
        self.pos:   Vector2D = Vector2D(0,0)
        self.image: Surface = image

    # Draws the entity image 
    def draw(self):
        SCREEN.blit(self.image, (int(self.pos.x - self.image.width*0.5) , int(self.pos.y - self.image.height*0.5)))


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
    
    def __init__(self, file_path:str, cell_size=(64,64), scale_factor=1) -> None:
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

# Problem: sometimes the npc jumps too much, there is dependecy with the frames
class PhysicalBall(Component):

    def __init__(self, pos=(SCREEN_W * 0.5, SCREEN_H * 0.5), vel = (0,0), mass=1, radius=1, air_resist=0.5, retention_x=0.8, retention_y=0.4):
        # State of the object
        self.pos:Vector2D = Vector2D(pos[0], pos[1])
        self.vel:Vector2D = Vector2D(vel[0], vel[1])
        self.acc:Vector2D = Vector2D(0,0)
        
        # Properties of body
        self.mass:float = max(0.001, mass)
        self.radius:float = max(0.001, radius)
        self.air_resist:float = air_resist
        
        # How much of the speed is retained on collision
        self.retention_x = retention_x
        self.retention_y = retention_y

        # hits info
        self.is_hitting_floor:      bool = False
        self.is_hitting_wall:       bool = False
        
        # extra info
        self.og_image:              Surface | None = None
        self.is_grounded:           bool = False

    # Applying gravity and normal floor force
    def gravityEffect(self) -> None:
        self.acc.x += GRAVITY.x
        self.acc.y += GRAVITY.y

        if self.pos.y >= SCREEN_H - self.radius:
            self.is_grounded = True
            if abs(self.vel.y) > SPLAT_VELOCITY.y:
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
        else:
            self.is_grounded = False

    # Apply a force to the entity
    def applyForce(self, force:Vector2D, show_info=False) -> None:
        mass = self.mass
        #Update Acceleration
        self.acc.x += force.x/mass
        self.acc.y += force.y/mass
    
    # Checks for walls and pushes the entity
    def wallsPush(self):
        # Right wall
        if self.pos.x >= SCREEN_W-self.radius*0.5:
            self.pos.x = SCREEN_W - self.radius
            self.vel.x = -self.vel.x * self.retention_x
            
            if abs(self.vel.x) > SPLAT_VELOCITY.x: self.is_hitting_wall = True      
        # Left wall
        elif self.pos.x <= self.radius*0.5:
            self.pos.x = self.radius
            self.vel.x = -self.vel.x * self.retention_x
            self.is_hitting_wall = True

            if abs(self.vel.x) > SPLAT_VELOCITY.x: self.is_hitting_wall = True      
    
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

# Component who decides the current animation to be played
class StatesManager(Component):
    def __init__(self) -> None:
        self.current_state = 'idle'
        self.animator: Animator | None = None
        self.phys: PhysicalBall | None = None
        self.ai_controller: AIController | None = None

        self.og_image: Surface | None = None

    # Calls the handle logic and picks the needed components
    def update(self, entity:Entity, dt:float):
        if not self.animator: self.animator = entity.get_component(Animator)
        if not self.phys: self.phys = entity.get_component(PhysicalBall)
        if not self.ai_controller: self.ai_controller = entity.get_component(AIController)
        
        self.handle_logic(entity)

    # Switches to each state when the conditions are met
    def handle_logic(self, entity:Entity):
        if not (self.animator and self.phys and self.ai_controller): return
        match self.current_state:

            case 'idle':
                if not self.phys.is_grounded:
                    self.change_state('air', entity)
                elif self.phys.is_hitting_floor:
                    self.change_state('hit_floor', entity)
                elif self.phys.is_hitting_wall:
                    self.change_state('hit_wall', entity)
                elif self.ai_controller.curr_action == 'talk':
                        self.change_state('talk', entity)
            case 'air':
                # IDLE IF THE CHARACTER STOPPED
                if self.phys.is_grounded and abs(self.phys.vel.x) < SLIDE_STOP:
                    self.change_state('idle', entity)
                elif self.phys.is_hitting_floor:
                    self.change_state('hit_floor', entity)
                elif self.phys.is_hitting_wall:
                    self.change_state('hit_wall', entity)
            case 'hit_floor':
                if self.animator.is_finished():
                    self.phys.is_hitting_floor = False
                    if self.phys.is_grounded:
                        self.change_state('idle', entity)

                    elif self.ai_controller.curr_action == 'talk':
                        self.change_state('talk', entity)

                    elif self.phys.is_hitting_wall:
                        self.change_state('hit_wall', entity)
                    else:
                        self.change_state('air', entity)
                        
            case 'hit_wall':
                if self.animator.is_finished():
                    self.phys.is_hitting_wall = False
                    if self.phys.is_grounded:
                        self.change_state('idle', entity)
                    elif self.ai_controller.curr_action == 'talk':
                        self.change_state('talk', entity)
                    elif self.phys.is_hitting_floor:
                        self.change_state('hit_floor', entity)
                    else:
                        self.change_state('air', entity)
            case 'talk':
                if self.ai_controller.curr_action != 'talk' or not self.phys.is_grounded:
                    self.change_state('air', entity)
                
    # Changes the state and plays the corresponding animation        
    def change_state(self, new_state:str, entity:Entity):
        if self.current_state != new_state:
            self.current_state = new_state
            if self.animator:
                self.animator.play(new_state, entity)

# =====================================================================================
#                                   W.I.P                                
# =====================================================================================

# Component to decide the next action of the NPC
# This class changes the state of the StateManager to play certain animations
class AIController(Component):
    
    def __init__(self, timer_range:tuple[float,float] = (1,3)) -> None:
        # Needed components
        self.phys: PhysicalBall | None = None
        self.bubb: TextBubble | None = None

        # Timer for taking action
        self.timer_range:tuple[float, float] = timer_range
        self.max_time: float = 1.0
        self.timer: float = 0.0

        # All the possible actions and the current one 
        self.actions: list[str] = ['move', 'talk', 'wait']
        self.curr_action: str = 'move'

        # Target zone (for 'intelligent' movement)
        self.target_x:      float = 0
        self.target_setted: bool = False

        

    def update(self, entity:Entity, delta_tine:float):
        if self.phys is None:
            comp = entity.get_component(PhysicalBall)
            if isinstance(comp, PhysicalBall):
                self.phys = comp

        # Handle the timer     
        self.timer += delta_tine
        if self.timer > self.max_time:
            self.timer = 0
            self.decide(entity)

    def decide(self, entity:Entity):
        # Choose next action
        # currently random

        if not self.bubb: self.bubb = entity.get_component(TextBubble)
        if not self.phys: self.phys = entity.get_component(PhysicalBall)
        if not (self.phys and self.bubb): return
                
        # Dont show the text bubble
        self.bubb.show = False
        
        if self.curr_action != 'move':
            self.curr_action = self.actions[random.randrange(0, len(self.actions))]
        
        print(f'Now bobby will: {self.curr_action}')
        match self.curr_action:

            case 'move':
                # Push the entity
                if self.phys.is_grounded:
                    dir = 1 if (self.target_x > entity.pos.x) else -1
                    self.phys.applyForce(Vector2D(dir*JUMP_FORCE.x, JUMP_FORCE.y))

                # Timer reset
                dist_from_target = abs(self.target_x - entity.pos.x)
                if not self.target_setted: 
                    self.target_x = random.randrange(0, SCREEN_W)
                    self.target_setted = True

                # Change action if target reached
                if dist_from_target < TARGET_STOP :
                    self.curr_action = self.actions[random.randrange(0, len(self.actions))]
                    self.target_setted = False

                self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])
                
                print(f'Distance: {int(dist_from_target)}\tTargetted: {self.target_setted}')

            case 'wait':
                # Timer reset
                if self.phys.is_grounded: self.max_time = WAIT_TIME + 2*random.random()*random.randrange(-1, 2)    # wait for (5 - 7) seconds
                else: self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])

            case 'talk':

                # Change the phrase of the TextBubble and show it
                rand_phrase = CUCHU_PHRASES[random.randrange(0, len(CUCHU_PHRASES))]
                self.bubb.changephrase(rand_phrase)
                self.bubb.show = True

                # Timer reset
                self.max_time = len(rand_phrase)*0.4 if len(rand_phrase) > 4 else 2.0
        
        print()

# The component to show a TextBubble (with a certain phrase) above the entity 
class TextBubble(Component):
    def __init__(self, sheet_path: str, corner_size: int = 8):
        self.raw_sheet: SpriteSheet = SpriteSheet(sheet_path, (4,4), 4)
        self.c = corner_size # Tamaño en píxeles de las esquinas
        self.font = pygame.font.SysFont('Pixeloid', 20)
        
        self.phrase:str = ''
        self.show:bool  = True
    
    def changephrase(self, new_phrase:str):
        self.phrase = new_phrase

    def generate_bubble(self, padding: int = 10) -> Surface:
        # 1. Preparar el texto
        text_surf = self.font.render(self.phrase, True, (0, 0, 0))
        tw, th = text_surf.get_size()
        
        # 2. Dimensiones finales    
        s = self.c # Tamaño de la celda del sprite (esquina)
        bw = max(tw + (padding * 2), s * 2)
        bh = max(th + (padding * 2), s * 2)
        
        bubble_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
        
        # --- DIBUJAR ESQUINAS ---
        bubble_surf.blit(self.raw_sheet.get_sprite(0), (0, 0))              # TL
        bubble_surf.blit(self.raw_sheet.get_sprite(2), (bw - s, 0))         # TR
        bubble_surf.blit(self.raw_sheet.get_sprite(6), (0, bh - s))         # BL
        bubble_surf.blit(self.raw_sheet.get_sprite(8), (bw - s, bh - s))    # BR
        
        # --- DIBUJAR BORDES (Escalados) ---
        # Horizontal (Arriba y Abajo)
        horiz_size = (bw - s * 2, s)
        bubble_surf.blit(pygame.transform.scale(self.raw_sheet.get_sprite(1), horiz_size), (s, 0))
        bubble_surf.blit(pygame.transform.scale(self.raw_sheet.get_sprite(7), horiz_size), (s, bh - s))
        # Vertical (Izquierda y Derecha)
        vert_size = (s, bh - s * 2)
        bubble_surf.blit(pygame.transform.scale(self.raw_sheet.get_sprite(3), vert_size), (0, s))
        bubble_surf.blit(pygame.transform.scale(self.raw_sheet.get_sprite(5), vert_size), (bw - s, s))
        
        # --- CENTRO ---
        bubble_surf.blit(pygame.transform.scale(self.raw_sheet.get_sprite(4), (bw - s*2, bh - s*2)), (s, s))
        
        # 3. Superponer el texto (Centrado matemáticamente en la burbuja)
        # Esto asegura que si la burbuja es más grande que el texto, quede en el medio
        text_x = (bw - tw) // 2
        text_y = (bh - th) // 2
        bubble_surf.blit(text_surf, (text_x, text_y))
        
        return bubble_surf


    def update(self, entity: Entity, dt: float):
        if self.show:
            bubble = self.generate_bubble()
            SCREEN.blit(bubble, (entity.pos.x + entity.image.get_width()*0.25, entity.pos.y - entity.image.get_height()*0.8))

# Components which gets a set of CharactersData (Object)
class CharactersHandler(Component):
    def __init__(self, characters: list[CharacterData]) -> None:
        self.curr_char: str = characters[0].name
        self.characters: dict[str, CharacterData] = {c.name: c for c in characters}
        
        # For the CharacterHandler to work we need:
        # - Animator (to change the sprite sheet thats being used)
        # - AI_Controller to change the phrases for the talking
        #  (...)

        self.animator:  Animator | None = None 
        self.ai_controller:  AIController | None = None 

        pass

    def update(self, entity: Entity, dt: float):
        if not self.animator: self.animator = entity.get_component(Animator)
        if not self.ai_controller: self.ai_controller = entity.get_component(AIController)

    def switch_character(self, new_char: str):
        pass

class CharacterData():
    def __init__(self, ss: SpriteSheet, name:str, phrases:list[str] = []):
        self.name:      str = name
        self.phrases:   list[str] = phrases


import pygame
import win32api
import random
from typing import Type
from pygame._sdl2 import Window, Renderer, Texture, Image

# Custom
from .basics import Component, SpriteSheet, CharacterData, Animation, Entity, State, World, ParticlesManager
from .window_setup import RENDERER, SCREEN_W, SCREEN_H, WINDOW, SCREEN_CENTER

from game_consts import GRAVITY, BOUNCE_STOP, SLIDE_STOP, USER_PULL_DAMPING, USER_PULL_STRENGTH, SPLAT_VELOCITY
from game_consts import WAIT_TIME, SLEEP_TIME, JUMP_FORCE, TARGET_STOP, ACTION_WEIGHTS
from prefabs import POPCORN_PRTS

from .math_custom import Vector2D

# BROKEN VERSION: WIP CHANGING THE WAY OF DRAWING
# BROKEN VERSION: WIP CHANGING THE WAY OF DRAWING
# BROKEN VERSION: WIP CHANGING THE WAY OF DRAWING
# BROKEN VERSION: WIP CHANGING THE WAY OF DRAWING
# BROKEN VERSION: WIP CHANGING THE WAY OF DRAWING

# =====================================================================================
#                               COMPONENTS
# =====================================================================================

# Animator: decides which is the next frame from a group of animations
class Animator(Component):
    __slots__ = ['frame_idx', 'ss', 'anims', 'timer', 'current_anim']
    def __init__(self, ss:SpriteSheet=SpriteSheet(''), anims:list[Animation] = []) -> None:
        self.frame_idx:int = 0
        
        self.ss = ss
        self.anims: dict[str, Animation] = {a.name: a for a in anims}
 
        self.timer:float = 0
        
        self.current_anim: Animation = list(self.anims.values())[0] if self.anims else Animation('',[])        

    def update(self, dt:float):
        if not self.current_anim:
            return
        
        self.timer += dt

        if self.timer >= self.current_anim.frame_duration:
            self.timer = 0.0
            sprite_id=0
            if self.current_anim.loop or self.frame_idx < len(self.current_anim.seq)-1:
                self.frame_idx = (self.frame_idx + 1) % len(self.current_anim.seq)
                sprite_id = self.current_anim.seq[self.frame_idx]
                self.parent.texture = self.ss.get_texture(sprite_id)

    def play(self, name:str):
        
        if self.current_anim and self.current_anim.name == name:
            return
        
        if name in self.anims:
            self.current_anim = self.anims[name]
            self.frame_idx = 0
            self.timer = 0

            sprite_id = self.current_anim.seq[self.frame_idx]
            self.parent.texture = self.ss.get_texture(sprite_id)

    def is_finished(self) -> bool:
        if self.current_anim: 
            if self.current_anim.loop: return False
            
            return self.frame_idx == len(self.current_anim.seq) - 1
        
        
        print(f'Error: there is no animation playing')
        return False
    
# PhysicalBall: the one in charge of following the rules of physics updating itself
# Problem: sometimes the npc jumps too much, there is dependecy with the frames
class PhysicalBall(Component):
    __slots__ = ['pos', 'vel', 'acc', 'mass', 'radius', 'air_resist', 'retention_x', 'retention_y', 'is_hitting_floor', 'is_hitting_wall', 'is_grounded', 'directed']
    def __init__(self, pos=(SCREEN_CENTER[0], SCREEN_CENTER[1]), vel = (0,0), mass:float=1, radius:float=1, air_resist:float=0.05, retention_x:float=0.8, retention_y:float=0.4, directed:bool = True):
        # State of the object
        self.pos:Vector2D = Vector2D(pos[0], pos[1])
        self.vel:Vector2D = Vector2D(vel[0], vel[1])
        self.acc:Vector2D = Vector2D(0,0)
        
        # Properties of body
        self.mass:float = max(0.01, mass)
        self.radius:float = max(0.01, radius)
        self.air_resist:float = air_resist
        
        # How much of the speed is retained on collision
        self.retention_x = retention_x
        self.retention_y = retention_y

        # hits info
        self.is_hitting_floor:      bool = False
        self.is_hitting_wall:       bool = False
        # extra info
        self.is_grounded:           bool = False

        self.directed = directed

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
    def update(self, dt:float):

        # Reset hitting variables
        self.is_hitting_floor = False
        self.is_hitting_wall = False

        # Acceleration downwards by gravity 
        self.gravityEffect()
        self.airForce()
        self.wallsPush()
        
        # Update physical state
        self.vel += self.acc*dt
        self.pos += self.vel*dt
        self.acc.x = 0
        self.acc.y = 0

        if self.directed:
            if abs(self.vel.x) > 50:
                if self.vel.x < 0:
                    self.parent.facing = -1
                elif self.vel.x > 0:
                    self.parent.facing = 1
            
        self.parent.pos = self.pos

# MouseDrag lets the entity get dragged with physics by the mouse
class MouseDrag(Component):
    __slots__ = ['mouse_pos', 'is_pulling', 'phys', 'animator', 'pos_diff', 'diff_mag']
    def __init__(self) -> None:
        # Mouse variables
        self.mouse_pos:Vector2D = Vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        self.is_pulling = False
        self.phys:PhysicalBall = PhysicalBall()
        self.animator: Animator | None = None
        self.pos_diff: Vector2D = Vector2D(0,0)
        self.diff_mag: float = 0
    
    # The entity needs a PhysicalBall to work.
    def start(self, entity:Entity):
        super().start(entity)
        comp = self.parent.get_component(PhysicalBall)
        if comp: 
            self.phys = comp
        else:
            raise Exception(f"{self.parent.name}: Has not a PhysicsBall Component. It's required if using {self.__class__.__name__}")
            

    def update(self, dt: float):
        if self.phys is None:
            comp = self.parent.get_component(PhysicalBall)
            if isinstance(comp, PhysicalBall):
                self.phys = comp 
            
        
        left_click_state = win32api.GetAsyncKeyState(0x01)

        if left_click_state & 0x8000:
            m_x, m_y = win32api.GetCursorPos()
            self.mouse_pos.x  = m_x
            self.mouse_pos.y  = m_y
            
            self.pos_diff = self.mouse_pos - self.phys.pos
            self.diff_mag = self.pos_diff.magnitude()
            
            if self.diff_mag <= self.phys.radius + 5:
                self.is_pulling = True
        else:
            self.is_pulling = False

        if self.is_pulling:
            self.phys.applyForce((self.pos_diff*USER_PULL_STRENGTH) - self.phys.vel*USER_PULL_DAMPING)

# Component who decides the current animation to be played
class StatesManager(Component):
    __slots__ = ['current_state', 'states', 'animator']
    def __init__(self, states:list[State]) :
        self.current_state:     State = states[0]
        self.states:            dict[str,State] = {s.name : s for s in states}

        # Animator to change animations
        self.animator: Animator = Animator(SpriteSheet(''), [])

    # Needs an animator, physicalball and aicontroller to work. (yeah thats not good)
    def start(self, entity:Entity):
        super().start(entity)
        e_anim = self.parent.get_component(Animator)
        missing_comps: list[Type] = []

        if e_anim: self.animator = e_anim
        else: missing_comps.append(Animator)

        if len(missing_comps) > 0:
            raise Exception(f"{self.parent.name}: Has not a {[c.__name__ for c in missing_comps]} Component. It's required if using {self.__class__.__name__}")
    
    # Updating to the next state (can also stay the same)
    def update(self, dt:float):
        self.change_state(self.current_state.transition(self.parent))

    # Changes the state and plays the corresponding animation        
    def change_state(self, new_state:str):
        if self.current_state != new_state:
            s = self.states.get(new_state)
            if s:
                self.current_state = s
                if self.animator:
                    self.animator.play(new_state)
                #print(f'Playing: {new_state}')

# Components which gets a set of CharactersData (Object)
class CharactersHandler(Component):
    __slots__ =['curr_char', 'characters', 'animator', 'ai_controller']

    def __init__(self, characters: list[CharacterData]) -> None:
        self.curr_char: str = characters[random.randrange(0,len(characters))].name
        self.characters: dict[str, CharacterData] = {c.name: c for c in characters}
        
        # For the CharacterHandler to work we need:
        # - Animator (to change the sprite sheet thats being used)
        # - AI_Controller to change the phrases for the talking
        #  (...)

        self.animator:  Animator = Animator(SpriteSheet(''), []) 
        self.ai_controller:  AIController = AIController() 
    
    def start(self, entity:Entity):
        super().start(entity)

        e_anim = self.parent.get_component(Animator)
        e_aic = self.parent.get_component(AIController)
        missing_comps: list[Type] = []

        if e_anim: self.animator = e_anim
        else: missing_comps.append(Animator)

        if e_aic: self.ai_controller = e_aic
        else: missing_comps.append(AIController)

        if len(missing_comps) > 0:
            raise Exception(f"{self.parent.name}: Has not a {[c.__name__ for c in missing_comps]} Component. It's required if using {self.__class__.__name__}")

        # Setting the dafaults for Animator and AI Controller
        self.update_character()

    def switch_character(self, new_char: str):
        if new_char in self.characters:
            self.curr_char = new_char
            self.update_character()

    def update_character(self):
        character = self.characters.get(self.curr_char)
        if character:
            self.animator.ss = character.ss
            self.ai_controller.phrases = character.phrases           

global bubble_sheet
bubble_sheet: SpriteSheet = SpriteSheet('resources/images/text_bubble.png', (4,4), 4)
class TextBubble(Component):
    __slots__ = ['raw_sheet', 'c', 'font', 'phrase', 'show', 'texture']
    def __init__(self):
        self.c = 8
        self.font = pygame.font.SysFont('ocraextended', 16)
        self.phrase: str = '(I need some phrases mate...)'
        self.show: bool = False
        self.texture: Texture | None = None
        self.update_texture()
    
    def changephrase(self, new_phrase: str):
        if self.phrase != new_phrase:
            self.phrase = new_phrase
            self.update_texture()

    def update_texture(self):
        surf = self.generate_bubble_surf()
        self.texture = Texture.from_surface(RENDERER, surf)

    def draw(self):
        if self.show and self.texture and self.parent.texture:
            x = self.parent.pos.x + self.parent.texture.width * 0.25
            y = self.parent.pos.y - self.parent.texture.height * 1.2
            dest_rect = pygame.Rect(x, y, self.texture.width, self.texture.height)
            RENDERER.blit(self.texture, dest=dest_rect)
    
    def generate_bubble_surf(self, padding: int = 5) -> pygame.Surface:
        lines, _ = self.text_info(self.phrase)
        if not lines: return pygame.Surface((0, 0), pygame.SRCALPHA)

        line_surfs = [self.font.render(l, True, (0, 0, 0)) for l in lines]
        max_w = max(s.get_width() for s in line_surfs)
        line_h = self.font.get_linesize()
        total_h = line_h * len(lines)

        s = self.c 
        bw = max_w + (padding * 2) + (s * 2)
        bh = total_h + (padding * 2) + (s * 2)
        bw, bh = max(bw, s * 2), max(bh, s * 2)
        
        bubble_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
        mid_w = bw - (s * 2)
        mid_h = bh - (s * 2)

        bubble_surf.blit(bubble_sheet.surfaces[0], (0, 0))
        bubble_surf.blit(bubble_sheet.surfaces[2], (bw - s, 0))
        bubble_surf.blit(bubble_sheet.surfaces[6], (0, bh - s))
        bubble_surf.blit(bubble_sheet.surfaces[8], (bw - s, bh - s))

        if mid_w > 0:
            top = pygame.transform.scale(bubble_sheet.surfaces[1], (mid_w, s))
            bottom = pygame.transform.scale(bubble_sheet.surfaces[7], (mid_w, s))
            bubble_surf.blit(top, (s, 0))
            bubble_surf.blit(bottom, (s, bh - s))

        if mid_h > 0:
            left = pygame.transform.scale(bubble_sheet.surfaces[3], (s, mid_h))
            right = pygame.transform.scale(bubble_sheet.surfaces[5], (s, mid_h))
            bubble_surf.blit(left, (0, s))
            bubble_surf.blit(right, (bw - s, s))

        if mid_w > 0 and mid_h > 0:
            center = pygame.transform.scale(bubble_sheet.surfaces[4], (mid_w, mid_h))
            bubble_surf.blit(center, (s, s))

        current_y = (bh - total_h) // 2
        for surf in line_surfs:
            text_x = (bw - surf.get_width()) // 2
            bubble_surf.blit(surf, (text_x, current_y))
            current_y += line_h

        return bubble_surf
    
    def text_info(self, text: str) -> tuple[list[str], str]:
        max_chars = 16
        words = text.split(' ')
        lines = []
        current_line_words = []
        current_count = 0
        largest_verse = ""

        for word in words:
            word_len = len(word)
            space = 1 if current_line_words else 0
            if current_count + space + word_len <= max_chars:
                current_line_words.append(word)
                current_count += space + word_len
            else:
                full_line = " ".join(current_line_words)
                lines.append(full_line)
                if len(full_line) > len(largest_verse):
                    largest_verse = full_line
                current_line_words = [word]
                current_count = word_len

        if current_line_words:
            full_line = " ".join(current_line_words)
            lines.append(full_line)
            if len(full_line) > len(largest_verse):
                largest_verse = full_line

        return lines, largest_verse

# Component to decide the next action of the NPC
# This class changes the state of the StateManager to play certain animations
class AIController(Component):
    __slots__ = ['phys', 'bubb', 'timer_range', 'max_time', 'timer', 'actions', 'curr_action', 'target_x', 'target_setted', 'going_to_open', 'phrases', 'weights', 'total_weight']
    def __init__(self, timer_range:tuple[float,float] = (1,3)) -> None:
        # Needed components
        self.phys: PhysicalBall = PhysicalBall()
        self.bubb: TextBubble = TextBubble()

        # Timer for taking action
        self.timer_range:tuple[float, float] = timer_range
        self.max_time: float = 1.0
        self.timer: float = 0.0

        # All the possible actions and the current one 
        self.actions: list[str] = ['move', 'talk', 'wait', 'sleep']
        self.curr_action: str = 'wait'

        # Target zone (for 'intelligent' movement)
        self.target_x:      float = 0
        self.target_setted: bool = False
        self.going_to_open: bool = False
        self.phrases:   list[str] = [' ']

        # Random action and weights system
        self.weights = ACTION_WEIGHTS

        temp: int = 0
        for w in self.weights:
            temp += w[1]
        
        self.total_weight: int = temp

    # Getting all needed componets
    def start(self, entity:Entity):
        super().start(entity)
        e_phys = self.parent.get_component(PhysicalBall)
        e_textb = self.parent.get_component(TextBubble)
        missing_comps: list[Type] = []

        if e_phys: self.phys = e_phys
        else: missing_comps.append(PhysicalBall)

        if e_textb: self.bubb = e_textb
        else: missing_comps.append(TextBubble)

        if len(missing_comps) > 0:
            raise Exception(f"{self.parent.name}: Has not a {[c.__name__ for c in missing_comps]} Component. It's required if using {self.__class__.__name__}")
    
    # Timer to handle the decision making
    def update(self, dt:float):
        # Handle the timer     
        self.interruptAction()

        self.timer += dt
        if self.timer > self.max_time:
            self.timer = 0
            self.decide()
        
    # A function to interrupt actions when meeting certain conditions
    def interruptAction(self):
        if self.curr_action == 'sleep' and not self.phys.is_grounded: 
            self.curr_action = 'wait'

    def decide(self):

        # Dont show
        if self.curr_action != 'talk': self.bubb.show = False

        if self.curr_action != 'move': self.randomize_action()
        
        #print(f'Now bobby will: {self.curr_action}')
        match self.curr_action:

            case 'move':
                # Push the entity
                if self.phys.is_grounded:
                    dir = 1 if (self.target_x > self.parent.pos.x) else -1
                    self.phys.applyForce(Vector2D(dir*JUMP_FORCE.x, JUMP_FORCE.y))

                # Timer reset
                dist_from_target = abs(self.target_x - self.parent.pos.x)
                if not self.target_setted: 
                    self.target_x = random.randrange(0, SCREEN_W)
                    self.target_setted = True

                # Change action if target reached
                if dist_from_target < TARGET_STOP :
                    self.randomize_action()
                    self.target_setted = False

                self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])
                
                #print(f'Distance: {int(dist_from_target)}\tTargetted: {self.target_setted}')

            case 'wait':
                # Timer reset
                if self.phys.is_grounded: self.max_time = WAIT_TIME + 2*random.random()*random.randrange(-1, 2)    # wait for (3 - 7) seconds
                else: self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])

            case 'talk':
                # Change the phrase of the TextBubble and show it
                rand_phrase = self.phrases[random.randrange(0, len(self.phrases))]
                self.bubb.changephrase(rand_phrase)
                self.bubb.show = True
                #print(f'{'Saying' if self.bubb.show else 'Not Saying'}: {rand_phrase}')

                # Timer reset
                self.max_time = len(rand_phrase)*0.4 if len(rand_phrase) > 4 else 2.0

            case 'sleep':
                if self.phys.is_grounded: 
                    self.max_time = SLEEP_TIME # wait SLEEP_TIME ammount
                    self.parent.facing = 1
                else: 
                    self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])

            case 'open_img':
                if not self.target_setted:
                    self.target_x = SCREEN_W-10
                    self.target_setted = True
                    self.going_to_open = True

                if self.target_x < self.parent.pos.x:
                    # Logic to open the image at the corner of the screen 
                    # 1. Choose an image from the prev list, load it and show it on screen as an Entity
                    # 2. Activate animation
                    # 3. Apply a knockback force to the entity
                    print(f'Right corner reached')
                    pass

    def randomize_action(self):
        rand = random.randrange(0, self.total_weight+1)
        #print(f'Random number: {rand}/{self.total_weight}')
        action = ''
        accum = 0
        for w in self.weights:
            if accum > rand: break
            action = w[0]
            accum += w[1]
        
        self.curr_action = action


# =====================================================================================
#                                   W.I.P                                
# =====================================================================================

class EntityEraser(Component):
    __slots__ = ['phys']
    def __init__(self) -> None:
        self.phys: PhysicalBall = PhysicalBall()        

    def start(self, entity: Entity):
        super().start(entity)
        e_phys = self.parent.get_component(PhysicalBall)
        missing_comps: list[Type] = []

        if e_phys: self.phys = e_phys
        else: missing_comps.append(PhysicalBall)

        if len(missing_comps) > 0:
            raise Exception(f"{self.parent.name}: Has not a {[c.__name__ for c in missing_comps]} Component. It's required if using {self.__class__.__name__}")
    
    def update(self, dt: float):
        for e in World.entities:
            if e == self.parent: continue
            d = self.parent.pos.distance(e.pos)
            if d < self.phys.radius:
                e.active = False        # Inactives the entity it touches

class ParticlesEmitter(Component):
    __slots__ = ['manager', 'particle', 'frecuency', 'timer']
    def __init__(self, manager, particle:str ='spark', frecuency=1.0):
        self.manager: ParticlesManager = manager
        self.particle = particle
        self.frecuency = frecuency
        self.timer = 0
        
    def update(self, dt:float):
        self.timer += dt
        if self.timer > self.frecuency:
            x= self.parent.pos.x
            y= self.parent.pos.y
            self.manager.emit(x,y,*POPCORN_PRTS)
            self.timer = 0
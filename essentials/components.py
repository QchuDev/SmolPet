import datetime

import pygame
from pygame import Color, Rect
import random
from typing import Type
from pygame._sdl2 import Texture

from essentials.basics import UIElement

# Custom
from .basics import EntityContext, SFXManager, UIComponent, Listener, Component, MouseInput, SpriteSheet, CharacterData, Animation, Entity, State, World, ParticlesManager
from .window_setup import RENDERER, SCREEN_W, SCREEN_H, SCREEN_CENTER

from game_consts import GRAVITY, BOUNCE_STOP, JUMP_ACC, SIT_TIME, SLIDE_STOP, USER_PULL_DAMPING, USER_PULL_STRENGTH, SPLAT_VELOCITY
from game_consts import WAIT_TIME, SLEEP_TIME, TARGET_STOP, ACTION_WEIGHTS

from .math_custom import Vector2D

# =====================================================================================
#                               ENTITY COMPONENTS
# =====================================================================================

# Animator: decides which is the next frame from a group of animations
class Animator(Component):
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
                self.parent.texture = self.ss.get_texture(sprite_id, flipped = self.parent.facing<0)

    def play(self, name:str):
        
        if self.current_anim and self.current_anim.name == name:
            return
        
        if name in self.anims:
            self.current_anim = self.anims[name]
            self.frame_idx = 0
            self.timer = 0
            sprite_id = self.current_anim.seq[self.frame_idx]
            self.parent.texture = self.ss.get_texture(sprite_id, flipped = self.parent.facing<0)

    def is_finished(self) -> bool:
        if self.current_anim: 
            if self.current_anim.loop: return False
            
            return self.frame_idx == len(self.current_anim.seq) - 1
        
        
        print(f'Error: there is no animation playing')
        return False
    
# PhysicalBall: the one in charge of following the rules of physics updating itself
# Problem: sometimes the npc jumps too much, there is dependecy with the frames
class PhysicalBall(Component):
    def __init__(self, vel = (0,0), mass:float=1, radius:float=1, air_resist:float=0.05, retention_x:float=0.8, retention_y:float=0.4, directed:bool = True, grav_scale:float = 1,show_hitboxes:bool = False):
        # State of the object
        self.vel:Vector2D = Vector2D(vel[0], vel[1])
        self.acc:Vector2D = Vector2D(0,0)
        
        # Properties of body
        self.mass:float = max(0.01, mass)
        self.grav_scale = max(0, grav_scale)
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
        self.show_hitboxes= show_hitboxes

    # Applying gravity and normal floor force
    def gravityEffect(self) -> None:
        self.acc.x += GRAVITY.x * self.grav_scale
        self.acc.y += GRAVITY.y * self.grav_scale

        if self.parent.pos.y >= SCREEN_H - self.radius:
            self.is_grounded = True
            
            if abs(self.vel.y) > SPLAT_VELOCITY.y:
                self.is_hitting_floor = True
            self.parent.pos.y = SCREEN_H - self.radius
            
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
        if self.parent.pos.x >= SCREEN_W-self.radius*0.5:
            self.parent.pos.x = SCREEN_W - self.radius
            self.vel.x = -self.vel.x * self.retention_x
            
            if abs(self.vel.x) > SPLAT_VELOCITY.x: self.is_hitting_wall = True      
        # Left wall
        elif self.parent.pos.x <= self.radius*0.5:
            self.parent.pos.x = self.radius
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
        self.vel.x += self.acc.x*dt
        self.vel.y += self.acc.y*dt
        self.parent.pos.x += self.vel.x*dt
        self.parent.pos.y += self.vel.y*dt
        self.acc.x = 0
        self.acc.y = 0

        if self.directed:
            if abs(self.vel.x) > 50:
                if self.vel.x < 0:
                    self.parent.facing = -1
                elif self.vel.x > 0:
                    self.parent.facing = 1

    # hitboxes draw
    def draw(self):
        if self.show_hitboxes:
            if not self.parent.texture: return

            RENDERER.draw_color = (0,255,0,255)
            diameter = self.radius * 2
            draw_x = self.parent.pos.x - self.radius*0.5
            draw_y = self.parent.pos.y - self.radius

            rect_border= (draw_x, draw_y, diameter*0.5, diameter)
            RENDERER.draw_rect(rect_border)

# MouseDrag lets the entity get dragged with physics by the mouse
class MouseDrag(Component):
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
        if MouseInput.left_clicked:
            self.pos_diff = MouseInput.pos - self.parent.pos
            dist_sq = self.pos_diff.magnitude_squared()
            
            if self.is_pulling or dist_sq <= (self.phys.radius + 10)**2:
                self.is_pulling = True
        else:
            self.is_pulling = False

        if self.is_pulling:
            pull = (self.pos_diff * USER_PULL_STRENGTH)
            damp = (self.phys.vel * USER_PULL_DAMPING)
            self.phys.applyForce(pull - damp)

    def draw(self):
        if self.is_pulling:
            RENDERER.draw_color = Color(255,255,255)
            RENDERER.draw_line(tuple(self.parent.pos), tuple(MouseInput.pos))
       
# Component who decides the current animation to be played
class StatesManager(Component):

    def __init__(self, states:list[State]) :
        self.current_state:     State = states[0]
        self.states:            dict[str,State] = {s.name : s for s in states}
        self.ctx = EntityContext(Entity())
        
        # Animator to change animations
        self.animator: Animator = Animator(SpriteSheet(''), [])

    # Needs an animator, physicalball and aicontroller to work. (yeah thats not good)
    def start(self, entity:Entity):
        super().start(entity)
        e_anim = self.parent.get_component(Animator)
        missing_comps: list[Type] = []
        self.ctx = EntityContext(self.parent)

        if e_anim: self.animator = e_anim
        else: missing_comps.append(Animator)

        if len(missing_comps) > 0:
            raise Exception(f"{self.parent.name}: Has not a {[c.__name__ for c in missing_comps]} Component. It's required if using {self.__class__.__name__}")
    
    # Updating to the next state (can also stay the same)
    def update(self, dt:float):
        self.change_state(self.current_state.transition(self.ctx))

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

global pixel_font
pixel_font = pygame.font.Font("resources/fonts/Minecraft.ttf", 16)

global bubble_sheet
bubble_sheet: SpriteSheet = SpriteSheet('resources/images/text_bubble.png', (4,4), 4)

    
def text_info(text: str) -> tuple[list[str], str]:
    max_chars = 18 # Aumentado un poco para mejor lectura
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
def create_paragraph_texture(text, color=(255, 255, 255)):
    font = pixel_font
    lines, _ = text_info(text)
    line_surfaces = [font.render(l, False, color) for l in lines]
    
    if not line_surfaces: return None

    # Calculamos el tamaño total del párrafo
    w = max(s.get_width() for s in line_surfaces)
    line_height = font.get_linesize()
    h = line_height * len(line_surfaces)

    # Creamos una superficie transparente para "pegar" las líneas
    paragraph_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    for i, s in enumerate(line_surfaces):
        paragraph_surf.blit(s, (0, i * line_height))
    
    # Convertimos a textura de SDL2 para el RENDERER
    return Texture.from_surface(RENDERER, paragraph_surf)

class TextBubble(Component):
    
    def __init__(self):
        # self.c define el grosor de las esquinas en el resultado final
        self.c = 8 
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
            # Posicionamiento sobre la cabeza del NPC
            x = self.parent.pos.x + (self.parent.texture.width * 0.5)
            y = self.parent.pos.y - self.texture.height - 5
            
            dest_rect = pygame.Rect(int(x), int(y), self.texture.width, self.texture.height)
            RENDERER.blit(self.texture, dest=dest_rect)
    
    def generate_bubble_surf(self, padding: int = 6) -> pygame.Surface:
        lines, _ = text_info(self.phrase)
        if not lines: return pygame.Surface((0, 0), pygame.SRCALPHA)

        # 1. Render nitido (Sin suavizado para estilo Minecraft)
        line_surfs = [pixel_font.render(l, False, (0, 0, 0)) for l in lines]
        max_w = max(s.get_width() for s in line_surfs)
        line_h = pixel_font.get_linesize()
        total_h = line_h * len(lines)

        s = self.c 
        # Forzamos enteros para evitar el "bleeding" de píxeles
        bw = int(max_w + (padding * 2) + (s * 2))
        bh = int(total_h + (padding * 2) + (s * 2))
        
        bubble_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
        
        # PRE-ESCALADO DE PIEZAS: 
        # Escalamos las piezas de 4x4 originales a piezas de SxS (8x8)
        # Esto evita que el 9-slice intente estirar y mover al mismo tiempo
        p = [pygame.transform.scale(surf, (s, s)) for surf in bubble_sheet.surfaces]

        mid_w = bw - (s * 2)
        mid_h = bh - (s * 2)

        # --- ESQUINAS ---
        bubble_surf.blit(p[0], (0, 0))          # TL
        bubble_surf.blit(p[2], (bw - s, 0))     # TR
        bubble_surf.blit(p[6], (0, bh - s))     # BL
        bubble_surf.blit(p[8], (bw - s, bh - s))# BR

        # --- BORDES ---
        if mid_w > 0:
            top = pygame.transform.scale(p[1], (mid_w, s))
            bottom = pygame.transform.scale(p[7], (mid_w, s))
            bubble_surf.blit(top, (s, 0))
            bubble_surf.blit(bottom, (s, bh - s))

        if mid_h > 0:
            left = pygame.transform.scale(p[3], (s, mid_h))
            right = pygame.transform.scale(p[5], (s, mid_h))
            bubble_surf.blit(left, (0, s))
            bubble_surf.blit(right, (bw - s, s))

        # --- CENTRO ---
        if mid_w > 0 and mid_h > 0:
            center = pygame.transform.scale(p[4], (mid_w, mid_h))
            bubble_surf.blit(center, (s, s))

        # --- TEXTO (Centrado con corrección visual) ---
        current_y = (bh - total_h) // 2
        for surf in line_surfs:
            text_x = (bw - surf.get_width()) // 2
            bubble_surf.blit(surf, (text_x, current_y))
            current_y += line_h

        return bubble_surf
    
# Component to decide the next action of the NPC
# This class changes the state of the StateManager to play certain animations
class AIController(Component):
    def __init__(self, timer_range:tuple[float,float] = (1,3)) -> None:
        # Needed components
        self.phys: PhysicalBall = PhysicalBall()
        self.bubb: TextBubble = TextBubble()

        # Timer for taking action
        self.timer_range:tuple[float, float] = timer_range
        self.max_time: float = 1.0
        self.timer: float = 0.0

        # All the possible actions and the current one 
        self.plan: list[str] = ['wait']

        # Target zone (for 'intelligent' movement)
        self.target_x:      float = 0
        self.target_setted: bool = False
        self.going_to_open: bool = False
        self.phrases:   list[str] = [' ']

        # Random action and weights system
        self.weights = ACTION_WEIGHTS
        self.is_night: bool = False

        # Night behavior

        temp: int = 0
        for w in self.weights.values():
            temp += w

        
        
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
        if self.plan[0] != 'talk': self.bubb.show = False

        self.timer += dt
        if self.timer > self.max_time:
            self.timer = 0
            self.decide()
            if not self.is_night:
                if datetime.datetime.now().hour > 21:
                    self.weights['sleep'] = ACTION_WEIGHTS['sleep']*10 # At night we boost the sleeping stat to be more common.
                    self.is_night = True
        
    # A function to interrupt actions when meeting certain conditions
    def interruptAction(self):
        interrputed_from_lifting: list[str] = ['sleep', 'sit']
        if self.plan[0] in interrputed_from_lifting and not self.phys.is_grounded: 
            self.plan[0] = 'wait'

    # its a hard-coded method for the decision of NPCS
    def decide(self):
        
        self.next_action()
        match self.plan[0]:
            case 'move':
                
                # Push the entity
                if self.phys.is_grounded:
                    dir = 1 if (self.target_x > self.parent.pos.x) else -1
                    self.phys.applyForce(Vector2D(dir*JUMP_ACC.x, JUMP_ACC.y)*self.phys.mass)

                # Setting the 
                dist_from_target = abs(self.target_x - self.parent.pos.x)
                if not self.target_setted: 
                    self.target_x = random.randrange(0, SCREEN_W)
                    self.target_setted = True

                # Change action if target reached
                if dist_from_target < TARGET_STOP :
                    self.randomize_action()
                    self.target_setted = False
                else:
                    # if not reached, then append a new move action
                    self.plan.insert(0, 'move')

                self.max_time = self.timer_range[0] + random.random()*(self.timer_range[1] - self.timer_range[0])
                
            case 'wait':
                # Timer reset
                if self.phys.is_grounded: self.max_time = random.uniform(0.8, 1.2)*WAIT_TIME
                else: self.max_time = random.uniform(*self.timer_range)

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
                    self.max_time = random.uniform(*self.timer_range)

            case 'open_img':
                
                if not self.target_setted:
                    print('LETS OPEN AN IMAGE!!!')
                    self.target_x = SCREEN_W-10
                    self.target_setted = True
                    self.going_to_open = True

                if self.target_x < self.parent.pos.x:
                    # Logic to open the image at the corner of the screen 
                    # 1. Choose an image from the prev list, load it and show it on screen as an Entity
                    # 2. Activate animation
                    # 3. Apply a knockback force to the entity
                    print(f'OPENING IMAGE!!!')
                    pass

            case 'sit':
                # Timer reset
                if self.phys.is_grounded: self.max_time = random.uniform(0.8, 1.2)*SIT_TIME   # wait for (28 - 32) seconds
                else: self.max_time = random.uniform(*self.timer_range)
        
    def next_action(self):
        ## When there is no other aciton than de current one , then randomize
        if len(self.plan) == 1:
            self.randomize_action()
        if len(self.plan) > 1: 
            self.plan.pop(0)

    def randomize_action(self):
        rand = random.randrange(0, self.total_weight+1)
        #print(f'Random number: {rand}/{self.total_weight}')
        chosen_action = ''
        accum = 0
        for a, w in self.weights.items():
            if accum > rand: break
            chosen_action = a
            accum += w
        
        self.plan.append(chosen_action)


# Component to give an fixed ammount of health to props
class PropDuration(Component):
    def __init__(self, durability:int, breaking_particle:list) -> None:
        self.durability = durability
        self.breaking_particle = breaking_particle
        self.phys: PhysicalBall = PhysicalBall()    # to start with something

    def start(self, entity: Entity):
        super().start(entity)
        e_phys = self.parent.get_component(PhysicalBall)

        if e_phys: self.phys = e_phys
        else: raise Exception(f"{self.parent.name}: Has not a PhysicalBall Component. It's required if using {self.__class__.__name__}")

    def update(self, dt:float):
        if self.phys.is_hitting_floor or self.phys.is_hitting_wall:
            self.durability -= 1

        if self.durability < 1:
            self.parent.active = False
            ParticlesManager.emit(self.parent.pos.x, self.parent.pos.y,*self.breaking_particle)
            SFXManager.play('break', self.phys.vel.magnitude()/1000)

class PlayOnHit(Component):
    def __init__(self) -> None:
        self.phys = PhysicalBall()

    def start(self, entity: Entity):
        super().start(entity)
        e_phys = self.parent.get_component(PhysicalBall)

        if e_phys: self.phys = e_phys
        else: raise Exception(f"{self.parent.name}: Has not a PhysicalBall Component. It's required if using {self.__class__.__name__}")

    def update(self, dt:float):
        if self.phys.is_hitting_floor or self.phys.is_hitting_wall:
            SFXManager.play('hit', self.phys.vel.magnitude()/1000)

# =====================================================================================
#                               UI COMPONENTS
# =====================================================================================
class Button(UIComponent):
    
    def __init__(self, pressed_rect:Rect = Rect(16,0,16,16), not_pressed_rect:Rect = Rect(0,0,16,16), click_radius:float=16) -> None:
        self.pressed_rect:Rect = pressed_rect
        self.not_pressed_rect:Rect = not_pressed_rect
        self.click_radius:float = max(1, click_radius)
        self.click_down: bool = False
        self.click_up: bool = False
        self.listeners: list[Listener] = []

    def update(self, dt:float):
        is_click_held = MouseInput.left_clicked
        center:Vector2D = self.parent.pos + Vector2D(16,16)
        is_close = center.distance(MouseInput.pos) < self.click_radius

        # If close and held... change texture
        if is_close and is_click_held:
            self.parent.source_area = self.pressed_rect
        else:
            self.parent.source_area = self.not_pressed_rect

        # If pressed while inside
        if is_close and is_click_held and not self.click_down:
            self.click_down = True
            self.click_up = False
        
        # If the button is up
        elif not is_click_held and self.click_down:
            self.click_down = False
            
            # Only sent an event when its close enough
            if is_close:
                self.click_up = True
                for l in self.listeners:
                    l.hear()
            else:
                # If its lifted up but outside, then no event is sent
                self.click_up = False
            

        # Safety reset, if not clicking then the click_down should be false
        if not is_click_held:
            self.click_down = False

global achievements_icons
achievements_icons: Texture = Texture.from_surface(RENDERER, pygame.image.load('resources/images/ui/achievement_icons.png'))
global base_achievement
base_achievement: Texture = Texture.from_surface(RENDERER, pygame.image.load('resources/images/ui/achievements_popup.png'))

class AchievementCycle(UIComponent):
    def __init__(self, scale:int = 3) -> None:
        # [time_left, x, y, target_x, target_y, source_pos(16x16 icon), name_text, desc_text, first_time]
        self.showed_img = []
        self.n = len(self.showed_img)
        self.popups_offet = 120
        self.scale = scale

    def update(self, dt:float):
        # Move the animations
        for i, im in enumerate(self.showed_img):
            im[0] -= dt
            if im[0] < 0 :
                self.showed_img.pop(i)

            # The notification will last 10 senconds: 1 to enter, 8 to show and 1 to leave
            delta_x = 0
            delta_y = 0
            
            if im[0] > 9:   # startin or leaving
                delta_x = (im[3]-im[1])*pow(im[0]-9, 2)*0.2
            elif im[0] < 1:   # startin or leaving
                delta_x = (im[3]+400-im[1])*pow(im[0], 2)*0.2
            
            # delta y
            target_y = im[4]-self.popups_offet*i
            delta_y = (target_y-im[2])*pow((im[0]-1)/8, 2)

            if im[8]: 
                ParticlesManager.emit(SCREEN_W, target_y+32, 'spark', 3, 10, 3, 0, -1)
            
            im[8] = False

            im[1] += delta_x
            im[2] += delta_y

    def draw(self):
        # draws using the data in self.showed_img and achievement_icons
        for im in self.showed_img:
            RENDERER.blit(base_achievement, dest=Rect(int(im[1]), int(im[2]), base_achievement.width*self.scale, base_achievement.height*self.scale))
            icon_offset = 12
            RENDERER.blit(
                achievements_icons, 
                dest=Rect(int(im[1]+icon_offset), int(im[2]+icon_offset+6), 16*self.scale, 16*self.scale), 
                area=Rect(int(im[5][0]), int(im[5][1]), 16, 16)
            )

            name_text: Texture = im[6]
            desc_text: Texture = im[7]
            progress_text: Texture = im[9]
            # Here goes the logic for text showing
            offset_x = 70
            RENDERER.blit(name_text, dest=Rect(im[1]+offset_x, im[2]+18, name_text.width, name_text.height))
            RENDERER.blit(desc_text, dest=Rect(im[1]+offset_x, im[2]+36, desc_text.width, desc_text.height))

            RENDERER.blit(progress_text, dest=Rect(im[1]+offset_x, im[2]+100, progress_text.width, progress_text.height))

# =====================================================================================
#                                 LISTENERS
# =====================================================================================

# On click it will close the game
class QuitOnClick(UIComponent, Listener):
    def __init__(self) -> None:
        self.button:Button|None = None

    def start(self, ui_element: UIElement):
        super().start(ui_element)
        e_button = self.parent.get_component(Button)
        if not e_button:
            raise Exception(f"{self.parent.name}: Has not a Button Component. It's required if using {self.__class__.__name__}")
        self.button = e_button

        self.button.listeners.append(self)

    def hear(self):
        from essentials.gm import GameManager
        GameManager.running = False

class ToggleMuteOnClick(UIComponent, Listener):
    def __init__(self) -> None:
        self.button:Button|None = None

    def start(self, ui_element: UIElement):
        super().start(ui_element)
        e_button = self.parent.get_component(Button)
        if not e_button:
            raise Exception(f"{self.parent.name}: Has not a Button Component. It's required if using {self.__class__.__name__}")
        self.button = e_button

        self.button.listeners.append(self)

    def hear(self):
        import game_consts
        game_consts.SFX_VOLUME = 1 if game_consts.SFX_VOLUME == 0 else 0
        if self.button:
            if game_consts.SFX_VOLUME == 1:
                self.button.pressed_rect = Rect(16,32,16,16)
                self.button.not_pressed_rect = Rect(0,32,16,16)
            else:
                self.button.pressed_rect = Rect(16,48,16,16)
                self.button.not_pressed_rect = Rect(0,48,16,16)

class ToggleAchievementsOnClick(UIComponent, Listener):
    def __init__(self, progress_panel) -> None:
        self.button:Button|None = None
        self.progress_panel = UIElement()

    def start(self, ui_element: UIElement):
        super().start(ui_element)
        e_button = self.parent.get_component(Button)
        if not e_button:
            raise Exception(f"{self.parent.name}: Has not a Button Component. It's required if using {self.__class__.__name__}")
        self.button = e_button

        self.button.listeners.append(self)

    def hear(self):
        from game_consts import SFX_VOLUME
        SFX_VOLUME = 1 if SFX_VOLUME == 0 else 0

# =====================================================================================
#                                   W.I.P                                
# =====================================================================================

class EntityEraser(Component):
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
    def __init__(self, particle_prefab, condition_name:str, offset: tuple[float,float] = (0,0)):
        self.particle_prefab = particle_prefab
        self.offset = offset
        self.condition_name = condition_name
        self.condition = lambda: False
        
    # setting up the condition to be met for spawning particles
    def start(self, entity: Entity):
        super().start(entity)
        match self.condition_name:
            case 'in_hit':
                phys = self.parent.get_component(PhysicalBall)
                if phys:
                    self.condition = lambda: phys.is_hitting_floor or phys.is_hitting_wall
    
    # Check for the condition and spawn particles if met
    def update(self, dt:float):
        if self.condition():
            x= self.parent.pos.x + self.offset[0]
            y= self.parent.pos.y + self.offset[1]
            ParticlesManager.emit(x,y,*self.particle_prefab)
            self.timer = 0
            
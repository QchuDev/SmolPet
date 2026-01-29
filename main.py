import pygame
import win32api
import win32con
import win32gui
import math
# Custom packages
import physics
from math_custom import Vector2D
from bases import Entity, SpriteSheet
# Import Setup constants
from consts import SCREEN, SCREEN_W, SCREEN_H, FPS
# Import Scene constants
from consts import WALL_FRICTION
# Import Physic's constants
from consts import GRAVITY, USER_PULL_DAMPING, USER_PULL_STRENGTH
# Import colors
from consts import CLR_WHITE, CLR_GREEN

pygame.init()

pygame.display.set_caption('Smol Pet')
## TRANSPARENT WINDOW =================================================================================== 
TRANSPARENT_COLOR = (255, 0, 128)  # Transparency color
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]

win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT_COLOR), 0, win32con.LWA_COLORKEY)
# Keep window to the front
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
## ==========================================================================================================

# Time Variables
clock = pygame.time.Clock()
global delta_time
delta_time = 0.01

# Mouse variables
mouse_pos:Vector2D = Vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
isPulling = False
pos_diff:Vector2D = Vector2D(0,0)
diff_mag:float = 0

# Character creation ===========================================
# Creating the physics component for character
phys_ball = physics.PhysicalBall(radius=30, air_resist=0.0005, mass=2)

# Working the character image
cuchu_ss = SpriteSheet('resources/images/placeholder_spritesheet.png', (64,64)) 

sprite_index:int = 0
cuchu_character = cuchu_ss.get_sprite(sprite_index)
cuchu_character = pygame.transform.scale(cuchu_character, (60,60))

cuchu = Entity(cuchu_character, phys_ball)
## ============================================================


# TESTING =====================================================

cont = 0
## ============================================================

entities:list[Entity] = [cuchu]

## FUNCTIONS    ===============================================

# All logic of the dragging of the character 
def mouse_drag():
    global isPulling, pos_diff, diff_mag

    left_click_state = win32api.GetAsyncKeyState(0x01)

    if left_click_state & 0x8000:
        m_x, m_y = win32api.GetCursorPos()
        mouse_pos.x  = m_x
        mouse_pos.y  = m_y
        
        pos_diff = mouse_pos - phys_ball.pos
        diff_mag = pos_diff.magnitude()
        
        if diff_mag <= phys_ball.radius + 5:
            isPulling = True
    else:
        isPulling = False

    if isPulling:
        phys_ball.applyForce((pos_diff*USER_PULL_STRENGTH) - phys_ball.vel*USER_PULL_DAMPING)

# All Physics logic updating
def physics_update():

    for entity in entities:
        if entity.phys is None:
            continue

        phys_comp = entity.phys
        
        # Acceleration downwards by gravity 
        phys_comp.gravityEffect()
        
        # Right wall
        if phys_comp.pos.x >= SCREEN_W-phys_comp.radius and phys_comp.vel.x > 10:
            phys_comp.pos.x = SCREEN_W - phys_comp.radius
            phys_comp.vel.x = -phys_comp.vel.x * WALL_FRICTION
                
        # Left wall
        if phys_comp.pos.x <= phys_comp.radius and phys_comp.vel.x < -10:
            phys_comp.pos.x = phys_comp.radius
            phys_comp.vel.x = -phys_comp.vel.x * WALL_FRICTION
            
        # Air resistance
        drag_dir = -phys_comp.vel.normalized()
        phys_comp.applyForce(drag_dir*phys_comp.air_resist*(phys_comp.vel.dot(phys_comp.vel)))

        # Update physics of the phys_comp
        phys_comp.updateState(delta_time)


def animations():
    
    
    
    
    pass

## MAIN LOOP ======================================================
running:bool = True
while running:
    # Filling the background with the previously color setted to be transparent.
    SCREEN.fill(TRANSPARENT_COLOR)  # Transparent background

    mouse_drag()
    physics_update()

    animations()
    
    # Close with the ESC button
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                cuchu.update_surface(cuchu_ss.get_sprite(cont % 4))
                cont += 1
    # Draw entities
    for entity in entities:
        entity.draw()

    # Testing =============================================



    # ==================================================================

    # Update delta_time
    delta_time = clock.tick(FPS) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    
    pygame.display.flip()
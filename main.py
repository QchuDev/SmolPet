import pygame
import win32api
import win32con
import win32gui
import math
# Custom packages
import physics
from math_custom import Vector2D

# Import Setup constants
from consts import SCREEN, SCREEN_W, SCREEN_H, FPS
# Import Scene constants
from consts import WALL_FRICTION, FLOOR_FRICTION
# Import Physic's constants
from consts import GRAVITY, USER_PULL_DAMPING, USER_PULL_STRENGTH
# Import colors
from consts import CLR_WHITE 

pygame.init()
done = False
TRANSPARENT_COLOR = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)

## =============================== TRANSPARENT WINDOW ====================================================
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
mouse_pos:Vector2D = Vector2D(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

# TESTING =====================================================

ball = physics.PhysicalBall(radius=20, air_resist=0.0005, mass=2)
isPulling = False
pos_diff:Vector2D = Vector2D(0,0)
diff_mag:float = 0

## ============================================================
while not done:
    # Acceleration downwards by gravity 
    ball.gravityEffect()

    # Filling the background with the previously color setted to be transparent.
    SCREEN.fill(TRANSPARENT_COLOR)  # Transparent background


    # Close with the ESC button
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        
    # Mouse drag
    if pygame.mouse.get_pressed()[0]:
        mouse_pos.x  = pygame.mouse.get_pos()[0]
        mouse_pos.y  = pygame.mouse.get_pos()[1]
        pos_diff:Vector2D = mouse_pos - ball.pos
        diff_mag = pos_diff.magnitude()
        if diff_mag <= ball.radius:
            isPulling = True
    else:
        isPulling = False

    if isPulling:
        
        ball.applyForce((pos_diff*USER_PULL_STRENGTH) - ball.vel*USER_PULL_DAMPING)


    pygame.draw.circle(SCREEN, CLR_WHITE, (ball.pos.x, ball.pos.y), ball.radius)
    
    # Testing with physics =============================================

    # Right wall
    if ball.pos.x >= SCREEN_W-ball.radius and ball.vel.x > 10:
        ball.pos.x = SCREEN_W - ball.radius
        ball.vel.x = -ball.vel.x * WALL_FRICTION
            
    # Left wall
    if ball.pos.x <= ball.radius and ball.vel.x < -10:
        ball.pos.x = ball.radius
        ball.vel.x = -ball.vel.x * WALL_FRICTION
        
    # Air resistance
    drag_dir = -ball.vel.normalized()
    ball.applyForce(drag_dir*ball.air_resist*(ball.vel.dot(ball.vel)))

    # ==================================================================

    # Update physics of the ball
    ball.updateState(delta_time)
    
    # Update SCREEN and delta_time
    pygame.display.flip()
    delta_time = clock.tick(FPS) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    

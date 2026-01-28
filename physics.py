from consts import SCREEN_W, SCREEN_H
from consts import GRAVITY, BOUNCE_STOP, SLIDE_STOP
from math_custom import Vector2D

class PhysicalBall():

    def __init__(self, pos=(SCREEN_W * 0.5, SCREEN_H * 0.5), vel = (0,0), mass=1, radius=1, air_resist=0.5, retention_x=0.8, retention_y=0.4):
        self.pos:Vector2D = Vector2D(pos[0], pos[1])
        self.vel:Vector2D = Vector2D(vel[0], vel[1])
        self.acc:Vector2D = Vector2D(0,0)
        self.mass:float = max(0.001, mass)
        self.radius:float = max(0.001, radius)
        self.air_resist:float = air_resist
        self.retention_x = retention_x
        self.retention_y = retention_y

    # All checks and effects of gravity
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

    # Updates the acceleration when applying a force to an object.
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
    
    def updateState(self, delta_time , show_info=False) -> None:        
        self.vel += self.acc*delta_time
        self.pos += self.vel*delta_time
        self.acc.x = 0
        self.acc.y = 0

        # Show the current physical state of the object
        if show_info:
            print(f'Position =\t{self.pos}')
            print(f'Velocity =\t{self.vel}')
            print(f'Acceleration =\t{self.acc}')
            print('=======================================')
            
    

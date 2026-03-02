import math
class Vector2D():
    __slots__ = ['x', 'y']
    def __init__(self, x,y) -> None:
        self.x:float = x
        self.y:float = y

    # Dot product between this and other vector
    def dot(self, other:Vector2D) -> float:
        return self.x*other.x + self.y*other.y    
    
    # Returns the normalized version of the vector 
    def normalized(self):
        sq_mag = self.x**2 + self.y**2
        if sq_mag < 0.0001: return Vector2D(0,0) # Avoid calculation if near zero
        inv_mag = 1.0 / math.sqrt(sq_mag)
        return Vector2D(self.x * inv_mag, self.y * inv_mag)
    
    def distance(self, other:Vector2D) -> float:
        diff_x = self.x - other.x
        diff_y = self.y - other.y
        distance = math.sqrt(diff_x**2 + diff_y**2)
        return distance
    
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def magnitude_squared(self) -> float:
        return self.x**2 + self.y**2
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __add__(self, other) -> Vector2D:
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, k:float) -> Vector2D:
        return Vector2D(self.x*k, self.y*k)

    def __neg__(self) -> Vector2D:
        return Vector2D(-self.x, -self.y)

    def __iter__(self):
        yield self.x
        yield self.y

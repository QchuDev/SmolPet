import math
class Vector2D():
    def __init__(self, x,y) -> None:
        self.x:float = x
        self.y:float = y
        

    # Dot product between this and other vector
    def dot(self, other:Vector2D) -> float:
        return self.x*other.x + self.y*other.y    
    
    # Returns the normalized version of the vector 
    def normalized(self) -> Vector2D:
        if abs(self.x+self.y) < 0.0001:
            return Vector2D(0,0)
        
        s = 1/math.sqrt(self.x**2 + self.y**2)
        n_x = self.x * s
        n_y = self.y * s 
        return Vector2D(n_x, n_y)
    
    def distance(self, other:Vector2D) -> float:
        diff_x = self.x - other.x
        diff_y = self.y - other.y
        distance = math.sqrt(diff_x**2 + diff_y**2)
        return distance
    
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

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
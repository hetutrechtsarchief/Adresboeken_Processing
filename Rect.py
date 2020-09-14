class Rect:
    
    def __init__(self, x, y, w, h):  # Object constructor
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def intersects(self, other):
        return not (
        (other.x           > self.x + self.w) or 
        (other.x + other.w < self.x         ) or
        (other.y           > self.y + self.h) or
        (other.y + other.h < self.y         ))
    

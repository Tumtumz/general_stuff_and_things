import math

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point: ({self.x}, {self.y})"
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def simple_distance(p1, p2):
    dx = max(p1.x, p2.x) - min(p1.x, p2.x)
    dy = max(p1.y, p2.y) - min(p1.y, p2.y)
    return dx + dy

def complex_distance(p1, p2):
    dx = max(p1.x, p2.x) - min(p1.x, p2.x)
    dy = max(p1.y, p2.y) - min(p1.y, p2.y)
    return round(math.sqrt(dx * dx + dy * dy))

def true_distance(p1, p2):
    dx = max(p1.x, p2.x) - min(p1.x, p2.x)
    dy = max(p1.y, p2.y) - min(p1.y, p2.y)
    return math.sqrt(dx * dx + dy * dy)

if __name__=="__main__":
    origin = Point(12, 12)
    for x in range(25):
        line = []
        for y in range(25):
            line.append(str(complex_distance(origin, Point(x, y))).rjust(2))
        print(line)
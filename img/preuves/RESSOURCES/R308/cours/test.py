class Point:
    """Un point 2D avec coordonnées (x, y)."""
    def __init__(self, x:float = 0.0, y:float = 0.0):
        self.x = x # attribut d'instance
        self.y = y
        
    def norme(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
if __name__ == "__main__" :
    p = Point(3, 4)
    print(p.x, p.y, p.norme()) # 3 4 5.0
    p1 = Point(0, 0)
    print(p1.x, p1.y, p1.norme())
    a = Point(1, 2)
    b = a
    b.x = 99
    print(a.x)
    print(a is b)
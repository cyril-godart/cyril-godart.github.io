class Maths:
    @staticmethod
    def clamp(x: float, lo: float, hi: float) -> float:
        return max(lo, min(x, hi))
    
print(Maths.clamp(42, 0, 10))

class Date:
    def __init__(self, j: int, m: int, a: int):
        self.j, self.m, self.a = j, m, a

    def __str__(self) -> str:
        return f"({self.j:02d},{self.m:02d},{self.a})"
    
    def __eq__(self, other: object) -> bool:
        return self.j == other.j and self.m == other.m and self.a == other.a
    
    def __gt__(self, other: object) -> bool:
        return self.a > other.a or (self.a > other.a and self.m > other.m) or (self.a > other.a and self.m > other.m and self.j > other.j)
        
        #self.j > other.j or self.m > other.m or self.a > other.a 
    
    @classmethod
    def from_iso(cls, s: str) -> "Date":
        a, m, j = map(int, s.split("-"))
        return cls(j, m, a)
    
date1 = Date.from_iso("2025-09-02") 
date2 = Date.from_iso("2026-09-01")
date3 = Date.from_iso("2025-09-02")
print(Date.from_iso("2025-09-02"))
print(Date.__eq__(date1,date3))
print(Date.__eq__(date1,date2))
print(date1 > date2)
print(date1 > date3)
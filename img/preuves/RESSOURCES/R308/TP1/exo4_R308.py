class Heure:
    """Représente une heure de la journée (h, m, s)."""
    
    def __init__(self, h: int, m: int, s: int):
        # TODO: Initialiser et valider les attributs
        self.h = h
        self.m = m
        self.s = s
        assert 0 <= h <= 23, "heures non valide"
        assert 0 <= m <= 59, "minutes non valide"
        assert 0 <= s <= 59, "secondes non valide"

    @classmethod
    def from_secondes(cls, total_secondes: int) -> "Heure":
        # TODO: Calculer h, m, s et retourner une nouvelle instance `cls(...)`
        """Constructeur alternatif : crée une instance d'Heure depuis un total de secondes."""
        if total_secondes < 0:
            raise ValueError("Le nombre total de secondes ne peut pas être négatif.")
        
        # S'assure que le nombre de secondes est dans une journée de 24h
        total_secondes %= (24 * 3600)
        
        # divmod(a, b) retourne le tuple (a // b, a % b)
        minutes, s = divmod(total_secondes, 60)
        h, m = divmod(minutes, 60)
        
        # Appelle le constructeur __init__ de la classe (`cls`)
        return cls(h, m, s)
    
    def __repr__(self) -> str:
        # TODO
        return f"Heure({self.h}, {self.m}, {self.s})"

    def __str__(self) -> str:
        # TODO
        return f"{self.h:02d}:{self.m:02d}:{self.s:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Heure):
            return NotImplemented
        # TODO: Comparer self et other
        return self.h == other.h and self.m == other.m and self.s == other.s

# --- Tests à valider ---
h1 = Heure(1, 1, 1)
print(f"repr(h1): {repr(h1)}")
print(f"str(h1): {str(h1)}")

# Test du classmethod
total_secs = 3661 # 1 heure, 1 minute, 1 seconde
h2 = Heure.from_secondes(total_secs)
assert h2.h == 1 and h2.m == 1 and h2.s == 1

# Test de l'égalité
h3 = Heure(1, 1, 1)
assert h1 == h2
assert h1 == h3
assert h2 != Heure(1, 1, 2)

print("Tests de l'exercice 4 passés avec succès !")
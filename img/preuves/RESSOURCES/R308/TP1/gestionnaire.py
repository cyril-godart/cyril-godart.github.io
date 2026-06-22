# On importe la classe EquipementReseau pour pouvoir vérifier son type
from equipement import EquipementReseau

class GestionnaireParc:
    """Gère une collection d'équipements réseau."""

    def __init__(self, nom_parc: str):
        self.nom_parc = nom_parc
        self.equipements = [] # Initialise une liste vide pour stocker les objets

    def ajouter_equipement(self, equipement: EquipementReseau):
        """Ajoute un équipement au parc après avoir vérifié son type."""
        if not isinstance(equipement, EquipementReseau):
            print(f"ERREUR: Tentative d'ajout d'un objet qui n'est pas un EquipementReseau.")
            return
        
        self.equipements.append(equipement)
        print(f"INFO: L'équipement {equipement.hostname} a été ajouté au parc {self.nom_parc}.")

    def lister_equipements(self):
        """Affiche la liste de tous les équipements du parc."""
        if not self.equipements:
            print(f"Le parc '{self.nom_parc}' est vide.")
            return
        
        print(f"--- Équipements dans le parc '{self.nom_parc}' ---")
        for eq in self.equipements:
            print(f"  - {eq}") # __repr__ de l'équipement est appelé ici

    def rechercher_par_hostname(self, hostname: str) -> EquipementReseau | None:
        """Recherche un équipement par son hostname et le retourne s'il est trouvé."""
        for eq in self.equipements:
            if eq.hostname == hostname:
                return eq
        return None # Retourne None si aucun équipement n'est trouvé

    def statistiques(self):
        """Affiche des statistiques sur les équipements du parc."""
        total = len(self.equipements)
        actifs = sum(1 for eq in self.equipements if eq.est_actif)
        inactifs = total - actifs
        
        print(f"--- Statistiques pour le parc '{self.nom_parc}' ---")
        print(f"  Nombre total d'équipements : {total}")
        print(f"  Équipements actifs        : {actifs}")
        print(f"  Équipements inactifs      : {inactifs}")
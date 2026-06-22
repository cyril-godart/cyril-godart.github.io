class EquipementReseau:
    """Représente un équipement réseau (routeur, switch...)."""
    
    compteur_id = 0

    def __init__(self, hostname: str, ip_address: str):
        self.hostname = hostname
        self.ip_address = ip_address
        self.statut = 'inactif'
        
        # Assigner un ID unique et l'incrémenter
        self.id = EquipementReseau.compteur_id
        EquipementReseau.compteur_id += 1

    def __repr__(self) -> str:
        """Représentation textuelle complète de l'équipement."""
        return f"Equipement(id={self.id}, hostname='{self.hostname}', ip='{self.ip_address}', statut='{self.statut}')"

    def activer(self):
        """Change le statut de l'équipement à 'actif'."""
        self.statut = 'actif'
        print(f"INFO: {self.hostname} est maintenant actif.")

    def desactiver(self):
        """Change le statut de l'équipement à 'inactif'."""
        self.statut = 'inactif'
        print(f"INFO: {self.hostname} est maintenant inactif.")

    @property
    def est_actif(self) -> bool:
        """Propriété en lecture seule qui vérifie si l'équipement est actif."""
        return self.statut == 'actif'
from equipement import EquipementReseau
from gestionnaire import GestionnaireParc

# --- Tests à valider ---

# 1. Création des équipements
r1 = EquipementReseau(hostname="R1-Paris", ip_address="192.168.1.1")
s1 = EquipementReseau(hostname="S1-Lille", ip_address="192.168.1.10")
r2 = EquipementReseau(hostname="R2-Lyon", ip_address="10.0.0.1")

assert r1.id == 0 and s1.id == 1, "Les IDs doivent être uniques et séquentiels."
assert r1.statut == 'inactif', "Le statut initial doit être 'inactif'."

# 2. Activation et test de la propriété
r1.activer()
assert r1.est_actif is True, "La propriété est_actif doit refléter le statut."
print(r1)

# 3. Création du gestionnaire et ajout d'équipements
parc_nord = GestionnaireParc("Parc-Nord-France")
parc_nord.ajouter_equipement(r1)
parc_nord.ajouter_equipement(s1)

# 4. Lister et rechercher
print("\n--- Liste des équipements du parc ---")
parc_nord.lister_equipements()

print("\n--- Recherche de 'S1-Lille' ---")
equipement_trouve = parc_nord.rechercher_par_hostname("S1-Lille")
assert equipement_trouve is s1
print(f"Trouvé : {equipement_trouve}")

# 5. Statistiques
print("\n--- Statistiques du parc ---")
# Active s1 pour les stats
s1.activer()
parc_nord.statistiques() # Devrait afficher : Total: 2, Actifs: 2, Inactifs: 0

s1.desactiver()
print("\n--- Statistiques après désactivation ---")
parc_nord.statistiques() # Devrait afficher : Total: 2, Actifs: 1, Inactifs: 1

print("\nTests du mini-projet passés avec succès !")
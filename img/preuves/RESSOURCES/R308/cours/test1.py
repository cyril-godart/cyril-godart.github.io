class CompteBancaire:
    def __init__(self, titulaire:str, solde: float = 0.0):
        self.titulaire = titulaire
        self.solde = solde

    def depot(self, montant: float) -> None:
        self.solde += montant

    def retrait(self, montant: float) -> None:
        if montant > self.solde:
            raise ValueError("Solde insuffisant")
        self.solde -= montant

if __name__ == "__main__" :
    compte = CompteBancaire("Cyril", 1000.0)
    compte.depot(500.0)
    print(compte.solde)
    compte.retrait(1500)
    compte.retrait(1)
"""
AlgoInvest&Trade - version force brute.

Le programme lit un fichier CSV d'actions, teste toutes les combinaisons
possibles et garde celle qui rapporte le plus sans dépasser 500 €.
Avec 20 actions, ça fait 2^20 = 1 048 576 combinaisons à vérifier.

Utilisation : python3 bruteforce.py
"""

import csv
import sys
import time
from itertools import combinations

BUDGET = 500
FICHIER_PAR_DEFAUT = "Liste_d_actions_-_P7_Python_-_Feuille_1.csv"


class Action:

    def __init__(self, nom, prix, pourcentage):
        self.nom = nom
        self.prix = prix
        self.pourcentage = pourcentage

    def gain(self):
        # Le bénéfice est donné en pourcentage du prix, on le convertit en euros
        return self.prix * self.pourcentage / 100

    def __str__(self):
        return f"{self.nom} | prix : {self.prix:.2f} € | gain : {self.gain():.2f} €"


# Dans le fichier, le bénéfice est écrit avec un "%",
# il faut l'enlever avant de convertir en nombre
def lire_fichier(chemin):
    actions = []
    with open(chemin, newline="", encoding="utf-8") as fichier:
        lecteur = csv.reader(fichier)
        next(lecteur)
        for ligne in lecteur:
            prix = float(ligne[1])
            pourcentage = float(ligne[2].replace("%", ""))
            actions.append(Action(ligne[0], prix, pourcentage))
    return actions


def cout_total(actions):
    total = 0
    for action in actions:
        total += action.prix
    return total


def gain_total(actions):
    total = 0
    for action in actions:
        total += action.gain()
    return total


def force_brute(actions, budget):
    meilleure_combinaison = []
    meilleur_gain = 0

    # combinations(actions, taille) donne tous les groupes possibles de "taille"
    # actions, sans répétition et sans tenir compte de l'ordre
    for taille in range(1, len(actions) + 1):
        for combinaison in combinations(actions, taille):
            if cout_total(combinaison) <= budget:
                gain = gain_total(combinaison)
                if gain > meilleur_gain:
                    meilleur_gain = gain
                    meilleure_combinaison = list(combinaison)

    return meilleure_combinaison


def afficher_resultat(actions, duree):
    print(f"\nActions à acheter ({len(actions)}) :")
    for action in actions:
        print(f"  {action}")
    print(f"\nCoût total : {cout_total(actions):.2f} €")
    print(f"Bénéfice après 2 ans : {gain_total(actions):.2f} €")
    print(f"Temps d'exécution : {duree:.3f} secondes")


def main():
    if len(sys.argv) > 1:
        chemin = sys.argv[1]
    else:
        chemin = FICHIER_PAR_DEFAUT

    actions = lire_fichier(chemin)
    print(f"{len(actions)} actions lues dans {chemin}")
    print("Recherche de la meilleure combinaison, ça peut prendre un moment...")

    debut = time.perf_counter()
    meilleures_actions = force_brute(actions, BUDGET)
    duree = time.perf_counter() - debut

    afficher_resultat(meilleures_actions, duree)


if __name__ == "__main__":
    main()
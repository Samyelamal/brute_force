"""
AlgoInvest&Trade - version optimisée (programmation dynamique).

Le problème ressemble au "problème du sac à dos" : le budget de 500 € est
la taille du sac, chaque action a un poids (son prix) et une valeur (son gain).
Au lieu de tester toutes les combinaisons, on remplit un tableau qui garde,
pour chaque budget possible, le meilleur gain qu'on peut obtenir.

Avant de lancer le calcul, le programme fait un petit rapport sur les données,
car les fichiers historiques peuvent contenir des valeurs fausses.

Utilisation : python3 optimized.py 
"""

import csv
import math
import sys
import time

BUDGET = 500
FICHIER_PAR_DEFAUT = "dataset1_Python+P7.csv"

# Le tableau a besoin de prix entiers, donc on compte en dixièmes d'euro.
# 500 € deviennent 5000 dixièmes.
PRECISION = 10


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


# Les fichiers n'ont pas tous le même format : dans certains le bénéfice
# est écrit avec un "%", dans d'autres non. On enlève le "%" s'il y en a un.
def lire_fichier(chemin):
    actions = []
    with open(chemin, newline="", encoding="utf-8") as fichier:
        lecteur = csv.reader(fichier)
        next(lecteur)
        for ligne in lecteur:
            if len(ligne) < 3:
                continue
            try:
                prix = float(ligne[1])
                pourcentage = float(ligne[2].replace("%", ""))
            except ValueError:
                print(f"Ligne ignorée (valeur illisible) : {ligne}")
                continue
            actions.append(Action(ligne[0], prix, pourcentage))
    return actions


def trouver_doublons(actions):
    compteur = {}
    for action in actions:
        if action.nom in compteur:
            compteur[action.nom] += 1
        else:
            compteur[action.nom] = 1

    doublons = []
    for nom in compteur:
        if compteur[nom] > 1:
            doublons.append(nom)
    return doublons


def afficher_rapport(actions):
    prix_nuls = 0
    prix_negatifs = 0
    benefices_incorrects = 0
    for action in actions:
        if action.prix == 0:
            prix_nuls += 1
        elif action.prix < 0:
            prix_negatifs += 1
        if action.pourcentage <= 0:
            benefices_incorrects += 1

    print("Rapport sur les données :")
    print(f"  Actions dans le fichier : {len(actions)}")
    print(f"  Prix égal à 0 : {prix_nuls}")
    print(f"  Prix négatif : {prix_negatifs}")
    print(f"  Bénéfice nul ou négatif : {benefices_incorrects}")

    doublons = trouver_doublons(actions)
    print(f"  Noms en double : {len(doublons)}")
    for nom in doublons:
        for action in actions:
            if action.nom == nom:
                print(f"    {action}")


# On garde seulement les actions exploitables :
# - un prix négatif ou nul n'a pas de sens
# - un bénéfice nul ou négatif ne rapporte rien, inutile de l'acheter
# - quand un nom apparaît deux fois avec des valeurs différentes, on ne sait
#   pas laquelle est la bonne, donc on retire les deux par prudence
def nettoyer(actions):
    doublons = trouver_doublons(actions)
    actions_valides = []
    for action in actions:
        if action.prix <= 0 or action.pourcentage <= 0:
            continue
        if action.nom in doublons:
            continue
        actions_valides.append(action)
    return actions_valides


# On arrondit toujours au-dessus pour ne jamais sous-estimer un prix,
# comme ça le vrai total dépensé ne peut pas dépasser le budget.
def prix_en_unites(action):
    return math.ceil(round(action.prix * PRECISION, 2))


def sac_a_dos(actions, budget):
    capacite = budget * PRECISION

    tableau = [[0] * (capacite + 1)]

    for action in actions:
        poids = prix_en_unites(action)
        gain = action.gain()
        precedente = tableau[-1]

        ligne = precedente.copy()

        for c in range(poids, capacite + 1):
            avec_action = precedente[c - poids] + gain
            if avec_action > ligne[c]:
                ligne[c] = avec_action

        tableau.append(ligne)

    actions_choisies = []
    c = capacite
    for i in range(len(actions), 0, -1):
        if tableau[i][c] != tableau[i - 1][c]:
            action = actions[i - 1]
            actions_choisies.append(action)
            c -= prix_en_unites(action)

    actions_choisies.reverse()
    return actions_choisies


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

    debut = time.perf_counter()

    actions = lire_fichier(chemin)
    afficher_rapport(actions)
    actions_valides = nettoyer(actions)
    print(f"  Actions conservées : {len(actions_valides)}")

    meilleures_actions = sac_a_dos(actions_valides, BUDGET)
    duree = time.perf_counter() - debut

    afficher_resultat(meilleures_actions, duree)


if __name__ == "__main__":
    main()
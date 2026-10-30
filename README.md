# AlgoInvest&Trade : optimisation d'investissements

Ce projet cherche la meilleure liste d'actions à acheter pour un client, avec
un budget de 500 €, afin de maximiser son bénéfice au bout de deux ans.

Contraintes :
- chaque action ne peut être achetée qu'une seule fois ;
- on ne peut pas acheter une fraction d'action ;
- on dépense au maximum 500 € par client.

## Prérequis

Python 3.8 ou plus récent. Le projet utilise seulement la bibliothèque
standard de Python, il n'y a donc rien à installer.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `bruteforce.py` | Teste toutes les combinaisons possibles (force brute) |
| `optimized.py` | Version optimisée par programmation dynamique |
| `Liste_d_actions_-_P7_Python_-_Feuille_1.csv` | Liste des 20 actions de départ |
| `dataset1_Python+P7.csv` | Premier fichier historique de Sienna |
| `dataset2_Python+P7.csv` | Second fichier historique de Sienna |

## Lancer les programmes

Ouvrir un terminal dans le dossier du projet, puis :

```
python3 bruteforce.py
python3 optimized.py
python3 optimized.py "dataset2_Python+P7.csv"
```

Sous Windows, remplacer `python3` par `python`.

Sans argument, `bruteforce.py` lit la liste des 20 actions et `optimized.py`
lit le dataset1. On peut donner un autre fichier CSV en argument, à condition
qu'il ait trois colonnes dans cet ordre : nom, prix, bénéfice en pourcentage.

## Fonctionnement

**bruteforce.py** teste les 2^20 = 1 048 576 combinaisons possibles des
20 actions et garde la plus rentable qui respecte le budget. Cette méthode
devient inutilisable quand le nombre d'actions augmente.

**optimized.py** affiche d'abord un rapport sur les données (prix nuls ou
négatifs, bénéfices incorrects, doublons), écarte les lignes inutilisables,
puis résout le problème comme un problème du sac à dos avec la
programmation dynamique. Les prix sont comptés en dixièmes d'euro et
arrondis au-dessus, ce qui garantit de ne jamais dépasser le budget.

## Résultats obtenus

| Fichier | Programme | Coût | Bénéfice | Temps |
|---|---|---|---|---|
| Liste de 20 actions | bruteforce.py | 498,00 € | 99,08 € | environ 1 s |
| Liste de 20 actions | optimized.py | 498,00 € | 99,08 € | moins de 0,01 s |
| dataset1 | optimized.py | 499,23 € | 198,22 € | environ 0,4 s |
| dataset2 | optimized.py | 499,24 € | 197,69 € | environ 0,2 s |

Les temps varient selon l'ordinateur utilisé.
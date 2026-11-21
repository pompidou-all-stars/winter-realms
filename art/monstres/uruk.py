"""Grand-orc des forges (palier 1, sol) — kit 2.40 : orc noir, grand et droit, heaume, épaulières, couperet, bouclier à main blanche."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Grand-orc des forges"}

def pieces(K):
    return (casque(K, 'heaume', col='#2f3238') + epaulieres(K, col='#2f3238', taille=.95, pointes=2, col_pointe=FER, bord=None) +
            arme(K, 'epee', taille=1.3, col='#9aa2ac') + bouclier(K, col='#2f3238', bord=FER, embleme='#e8e0d0') +
            ceinture(K, pagne='#2a2a2a', boucle=FER) + genouilleres(K) + brassards(K, col='#2f3238', pointes=FER))

def construire(ctx):
    bipede('grand_orc', dict(z=1.0, peau=('#3d4a3a', '#56634e', '#2c3729'), bas='#3a3530', botte='#2a2622', tete='orc', voute=.25,
                             carrure=1.15, jambes=.42, muscle=1.2, oeil='#ffcf3a', lourd=1.1, pieces=pieces))

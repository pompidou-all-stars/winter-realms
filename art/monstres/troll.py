"""Troll des glaces (palier 1, sol) — kit 2.40 : grand troll bleu-vert voûté, bras immenses, défenses, crête rousse, gourdin."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Troll des glaces"}

def pieces(K):
    t = K.j('tete')
    return (defenses(K, taille=1.4) + arme(K, 'gourdin', taille=1.2, manche='#5a4a3a') + ceinture(K, pagne='#cfd8e2', boucle=None) +
            collier_crocs(K) + [corne(f'Crete{k}', '#d8642a', 'Tete', (0, t.y + .02 + .03 * k, t.z + .15 - .02 * k), .025, .1, .8,
                                      rot=(-.4, 0, 0), seg=5, n=3) for k in range(4)])

def construire(ctx):
    bipede('troll', dict(z=1.1, peau=('#57aeb0', '#74c4c4', '#3f8a8c'), bas='#7a6a5a', botte='#3f8a8c', tete='orc', tete_r=.9,
                         carrure=1.1, bras=1.35, voute=.85, jambes=.4, muscle=.7, oeil='#ffd23a', pieces=pieces))

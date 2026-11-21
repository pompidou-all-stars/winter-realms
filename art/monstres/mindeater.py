"""Cérébrophage (palier 2, spécial, étourdit) — kit 2.40 : être à peau mauve et tête en dôme, visage de tentacules, longue robe
noire et violette à haut col, mains griffues, aura psychique (création originale à la manière des horreurs psioniques)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Cérébrophage"}

def pieces(K):
    t, p = K.j('tete'), K.j('poitrine')
    K.lueurs.append(tore('Aura', '#c87aff', 'Tete', (0, t.y + .02, t.z + .12), .13, .008, rot=(.3, 0, 0), seg=16, seg2=3))
    return ([corne(f'Tentacule{k}', '#a86a98', 'Tete', (x, t.y - .1, t.z + .02), .018, .16, -1.2 + .3 * (k % 2), rot=(math.pi - .2, x * 2, 0), seg=5, n=4)
             for k, x in enumerate((-.045, -.015, .015, .045))] +
            [profil('Col', '#2a1a3a', 'Torse', [(-.2, 0), (.2, 0), (.24, .22), (0, .14), (-.24, .22)], .012, pos=(0, .08, p.z + .06), rot=(.3, 0, 0))])

def construire(ctx):
    bipede('cerebrophage', dict(z=1.05, peau=('#a86a98', '#c88ab8', '#7a4a6e'), bas='#3a1a4a', tete='tentacules', tete_r=1.05,
                                bas_du_corps='robe', carrure=.85, bras=1.1, muscle=0, voute=.2, jambes=.4, relief=RELIEF_PEAU,
                                oeil='#e8b0ff', pieces=pieces))

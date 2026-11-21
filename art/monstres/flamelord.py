"""Seigneur des brasiers (palier 3, sol) — kit 2.40 : démon colossal de roche volcanique fissurée de lave, grandes ailes noires
déchirées, cornes de bélier, crinière et épaulettes de flammes, fouet de feu et épée ardente (création originale à la manière des
grands démons de feu)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Seigneur des brasiers"}
FEU, BRAISE = '#ff7a1a', '#ffb347'

def pieces(K):
    t, p, e = K.j('tete'), K.j('poitrine'), K.j('epaule.L')
    K.lueurs += [cone(f'Criniere{k}', FEU, 'Tete', (x, t.y + .06, t.z + .1), .055, .002, .26 - .04 * abs(k - 2), rot=(-.9, x * 3, 0), seg=5)
                 for k, x in enumerate((-.1, -.05, 0, .05, .1))]
    K.lueurs += [cone(f'FlammeE{k}.{n}', FEU, f'Bras.{n}', (s * e.x + s * .03 * k, e.y + .02, e.z + .07), .04, .002, .16 - .03 * k, rot=(0, s * .3, 0), seg=5)
                 for s, n in ((1, 'L'), (-1, 'R')) for k in range(2)]
    K.lueurs += [plaque(f'Lave{k}', BRAISE, 'Torse', (x, -.18, p.z + z), .08, .01, .012, rot=(0, 0, a))
                 for k, (x, z, a) in enumerate(((-.08, .05, .6), (.07, -.02, -.5), (0, -.1, .2), (-.04, -.15, -.9), (.1, .07, 1.1)))]
    return (cornes(K, col='#1a1416', taille=1.4, forme='belier') + ailes_dos(K, '#1a1416', '#3a1a14', envergure=1.5) +
            arme(K, 'epee', taille=1.6, col=BRAISE) + arme(K, 'fouet', cote='L', taille=1.4, col=FEU))

def construire(ctx):
    bipede('seigneur_brasiers', dict(z=1.75, peau=('#2a2024', '#4a3a3a', '#140e10'), bas='#2a2024', botte='#140e10', tete='demon', tete_r=1.1,
                                     carrure=1.5, jambes=.42, muscle=1.3, voute=.45, queue=('#2a2024', 1.3), relief=RELIEF_ROC, ecailles=5,
                                     oeil='#ffcf3a', lourd=1.3, pieces=pieces))

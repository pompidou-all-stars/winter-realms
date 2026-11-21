"""Tambour de guerre ogre (palier 2, spécial, hâte) — kit 2.40 : ogre peint de guerre portant un énorme tambour sur le ventre,
deux mailloches, plumes et os."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Tambour de guerre ogre"}

def pieces(K):
    v = K.j('ventre'); out = [boule('Tambour', '#8a5a2a', 'Colonne', (0, -.25, v.z), .17, ech=(1, .55, 1), seg=14),
                              tore('Cercle', OR, 'Colonne', (0, -.3, v.z), .165, .012, rot=(math.pi / 2, 0, 0), seg=14, seg2=4),
                              boule('Peau_tambour', '#e8dcc0', 'Colonne', (0, -.33, v.z), .15, ech=(1, .08, 1), seg=12)]
    for s, n in ((1, 'L'), (-1, 'R')):
        w = K.j('poignet.L')
        out += [cone(f'Mailloche.{n}', BOIS, f'Main.{n}', (s * w.x, w.y - .02, w.z - .08), .012, .012, .22, rot=(1.0, 0, 0), seg=5),
                boule(f'Tete_mailloche.{n}', '#e8dcc0', f'Main.{n}', (s * w.x, w.y - .2, w.z + .04), .03, seg=6)]
    return out + collier_crocs(K) + [corne(f'Plume{k}', ROUGE if k % 2 else '#e8b23a', 'Tete', (x, K.j('tete').y + .02, K.j('tete').z + .15), .02, .12, .5,
                                           rot=(-.4, x * 3, 0), seg=4, n=2) for k, x in enumerate((-.05, 0, .05))]

def construire(ctx):
    bipede('tambour_ogre', dict(z=1.1, peau=('#b89a6a', '#d0b485', '#8a7048'), bas='#6a4a2a', botte='#4a3420', tete='orc', tete_r=.8,
                                ventre=1.5, carrure=1.35, muscle=.5, voute=.5, jambes=.34, oeil='#ffe45e', lourd=1.3, pieces=pieces))

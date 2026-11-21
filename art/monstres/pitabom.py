"""Abomination des fosses (palier 3, sol) — kit 2.40 : rat géant mutant monstrueux, chair rose et fourrure en lambeaux, plusieurs
têtes de rat, bras mécaniques, cristaux verts, chaînes (création originale à partir des hommes-rats)."""
from communs.creatures import *
from communs.creatures import _tete
INFOS = {'categorie': 'monstre', 'titre': "Abomination des fosses"}
P = ('#b88a8a', '#d0a8a4', '#8a5a5a')

def vols(K):
    t, p = K.j('tete'), K.j('poitrine')
    v = [V('Colonne', P[0], c=(0, -.04, .45), r=(.3, .28, .22))]
    for x, dz in ((.15, -.08), (-.16, -.05)):
        v += [seul(q) for q in _tete(K, (x, t.y + .03, t.z + dz), 'rat', ('#6a5a4a', '#8a7a68', '#4a3e32'))]
    return v

def pieces(K):
    p = K.j('poitrine'); w = K.j('poignet.L')
    K.lueurs += [cone(f'Cristal{k}', '#7aff5a', 'Torse', (x, .16, p.z + .12), .04, .002, .18, rot=(-.5, x * 3, 0), seg=5) for k, x in enumerate((-.1, 0, .1))]
    return ([tore('Chaine', FER, 'Torse', (0, 0, p.z - .05), .25, .014, rot=(0, .7, 0), seg=14, seg2=4)] +
            [cone('BrasMeca', FER2, 'Main.R', (-w.x, w.y, w.z), .05, .03, .25, rot=(math.pi, 0, 0), seg=8),
             profil('Lame_meca', LAME, 'Main.R', [(0, 0), (.06, .02), (.04, -.28)], .015, pos=(-w.x, w.y - .02, w.z - .25), rot=(0, 0, math.pi))])

def construire(ctx):
    bipede('abomination_fosses', dict(z=1.6, peau=P, bas='#6a5a4a', botte=P[2], tete='rat', tete_r=1.1, voute=.85, jambes=.32,
                                      carrure=1.5, bras=1.3, ventre=1.4, muscle=1.0, queue=('#d8a59a', 1.0), taches=.3, oeil='#7aff5a',
                                      lourd=1.6, volumes=vols, pieces=pieces))

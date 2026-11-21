"""Dévoreur de mana (palier 3, spécial, anti-magie) — kit 2.40 : spectre de néant flottant, sans jambes (longue traîne violette),
gueule béante à défenses, couronne et dos hérissés de cristaux de mana, très longs bras griffus, orbe de mana aspiré dans la poitrine."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Dévoreur de mana"}

def pieces(K):
    p, e, w, t = K.j('poitrine'), K.j('epaule.L'), K.j('poignet.L'), K.j('tete')
    K.lueurs += [cone(f'Cristal{k}', '#c87aff', 'Torse', (x, .14, p.z + .1), .05, .002, .24 + .06 * (k % 2), rot=(-.6, x * 3, 0), seg=5)
                 for k, x in enumerate((-.14, -.07, 0, .07, .14))]
    K.lueurs += [cone(f'CristalE.{n}', '#c87aff', f'Bras.{n}', (s * e.x, e.y, e.z + .06), .04, .002, .18, rot=(0, s * .5, 0), seg=5) for s, n in ((1, 'L'), (-1, 'R'))]
    K.lueurs += [cone(f'Couronne{k}', '#e8b0ff', 'Tete', (x, t.y + .03, t.z + .12), .02, .001, .12, rot=(0, x * 5, 0), seg=4) for k, x in enumerate((-.07, -.025, .025, .07))]
    K.lueurs.append(boule('Orbe', '#e8b0ff', 'Torse', (0, -.2, p.z - .04), .05, seg=10))
    return [corne(f'Griffe{k}.{n}', '#2a1a3a', f'Main.{n}', (s * w.x + s * .022 * (k - 1), w.y - .04, w.z - .09), .014, .14, .6, rot=(math.pi - .3, 0, 0), seg=4, n=3)
            for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)] + defenses(K, taille=1.4)

def construire(ctx):
    bipede('devoreur_mana', dict(z=1.4, peau=('#3a1a54', '#5a2a7a', '#24103a'), bas='#24103a', tete='demon', tete_r=1.05, bas_du_corps='traine',
                                 carrure=1.15, bras=1.55, muscle=.5, voute=.9, relief=RELIEF_LISSE, taches=.25, oeil='#e8b0ff', pieces=pieces))

"""Grand Ancien des abysses (palier 3, sol) — kit 2.40 : colosse ventru à tête de pieuvre, longue barbe de tentacules, tentacules
dorsaux, ailes membraneuses, peau vert-noir luisante marbrée, robe de lambeaux d'algues, griffes (création originale inspirée des
Grands Anciens de Lovecraft)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Grand Ancien des abysses"}
TENT = '#4a7a5a'

def pieces(K):
    t, w, p = K.j('tete'), K.j('poignet.L'), K.j('poitrine')
    return ([corne(f'Tentacule{k}', TENT, 'Tete', (x, t.y - .1, t.z + .02), .03, .36, -1.6 + .5 * (k % 3), rot=(math.pi - .15, x * 2, 0), seg=6, n=6)
             for k, x in enumerate((-.08, -.05, -.02, .02, .05, .08))] +
            [corne(f'TentDos{k}', TENT, 'Torse', (x, .15, p.z + .05), .04, .4, 1.6, rot=(-1.0, x * 4, 0), seg=6, n=6)
             for k, x in enumerate((-.12, 0, .12))] +
            ailes_dos(K, '#1a2a24', '#2a4a3a', envergure=1.2) +
            [corne(f'Griffe{k}.{n}', '#1a1a1a', f'Main.{n}', (s * w.x + s * .022 * (k - 1), w.y - .04, w.z - .09), .013, .1, .5, rot=(math.pi - .3, 0, 0), seg=4, n=2)
             for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)])

def construire(ctx):
    bipede('grand_ancien', dict(z=1.75, peau=('#2a4a3a', '#3a6a54', '#1a2a24'), bas='#1a3a2e', botte='#1a2a24', tete='tentacules',
                                tete_r=1.45, bas_du_corps='robe', carrure=1.35, bras=1.15, jambes=.38, muscle=.3, ventre=1.6, voute=.5,
                                relief=RELIEF_PEAU, taches=.35, taille_taches=6, oeil='#e8ff5a', lourd=1.6, pieces=pieces))

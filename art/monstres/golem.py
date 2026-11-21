"""Golem runique (palier 2, sol) — kit 2.40 : colosse de roche taillée en blocs fissurés, runes bleues lumineuses, éclats de roche sur
les épaules et le dos, poings énormes, tête-bloc à fente lumineuse."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Golem runique"}
ROC = '#7a7f88'

def pieces(K):
    p, t = K.j('poitrine'), K.j('tete')
    K.lueurs += [plaque(f'Rune{k}', '#5ab8ff', 'Torse', (x, -.19, p.z + z), .035, .01, .06, rot=(0, 0, .6 * k))
                 for k, (x, z) in enumerate(((-.08, .04), (.07, .02), (0, -.08)))]
    K.lueurs += [plaque('Fente', '#5ab8ff', 'Tete', (0, t.y - .1, t.z + .07), .09, .01, .018)]
    eclats = [cone(f'Eclat{k}', ROC, 'Torse', (x, .12, p.z + .1 + z), .05, .004, .16 + .04 * (k % 2), rot=(-.5, x * 2.5, 0), seg=4)
              for k, (x, z) in enumerate(((-.12, 0), (-.04, .04), (.05, .03), (.13, -.01)))]
    return eclats + epaulieres(K, col=ROC, taille=1.2, pointes=0, bord=None) + [
        cone(f'Pointe.{n}', ROC, f'Bras.{n}', (s * K.j('epaule.L').x, .02, K.j('epaule.L').z + .1), .045, .003, .14, rot=(0, s * .4, 0), seg=4)
        for s, n in ((1, 'L'), (-1, 'R'))]

def construire(ctx):
    bipede('golem_runique', dict(z=1.2, peau=('#8e929c', '#b0b4bc', '#6a6e78'), bas='#7e828c', botte='#6a6e78', tete='aucune',
                                 carrure=1.45, bras=1.2, jambes=.36, muscle=.3, voute=.35, relief=RELIEF_ROC, oeil='#5ab8ff', lourd=1.5,
                                 volumes=lambda K: [V('Tete', '#8e929c', c=(0, K.j('tete').y, K.j('tete').z + .07), r=(.1, .09, .085))],
                                 pieces=pieces))

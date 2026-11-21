"""Mère des couvées (palier 3, spécial, invocation — capacité à venir) — kit 2.40 : grande démone à l'abdomen gonflé d'œufs
lumineux, ailes membraneuses, cornes, griffes ; elle fait éclore des diablotins."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Mère des couvées"}

def vols(K):
    return [V('Hanches', '#6a2a3a', c=(0, .2, .32), r=(.24, .3, .22))]   # abdomen

def pieces(K):
    for k, (x, y, z) in enumerate(((.12, .1, .4), (-.1, .18, .35), (.05, .32, .3), (-.04, .05, .45), (.15, .28, .25))):
        K.oeil(f'Oeuf{k}', 'Hanches', (x, y, z), .045, col='#ffb347')
    return cornes(K, col='#2a1a1a', taille=1.1, forme='droites') + ailes_dos(K, '#3a1a24', '#5a2a34', envergure=1.0)

def construire(ctx):
    bipede('mere_couvees', dict(z=1.3, peau=('#8a3a4a', '#a85a68', '#6a2a3a'), bas='#6a2a3a', tete='demon', bas_du_corps='robe',
                                carrure=1.0, bras=1.25, muscle=.4, voute=.55, queue=('#6a2a3a', 1.0), relief=RELIEF_PEAU, taches=.2,
                                oeil='#ffb347', volumes=vols, pieces=pieces))

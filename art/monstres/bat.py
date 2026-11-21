"""Chauve-souris géante (palier 1, volant) — kit 2.40 : grande chauve-souris violette, ailes membraneuses, grandes oreilles, crocs."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chauve-souris géante"}

def pieces(K):
    m = K.j('museau')
    return [corne(f'Croc.{n}', OS_, 'Machoire', (s * .02, m.y + .1, m.z - .04), .008, .03, .3, seg=4, n=2) for s, n in ((1, 'L'), (-1, 'R'))]

def construire(ctx):
    volant('chauve_souris', dict(z=.75, corps=('#5a4a6a', '#7a6a8a', '#9a8aa8'), aile=('#6a5a7a', '#4a3a5a'), tete='chauve',
                                 envergure=1.1, queue=.2, oeil='#ff4a4a', relief=RELIEF_POIL, pieces=pieces))

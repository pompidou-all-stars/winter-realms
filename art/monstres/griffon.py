"""Griffon sauvage (palier 1, volant) — kit 2.40 : corps de lion fauve, tête d'aigle blanche à bec doré, ailes de plumes."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Griffon sauvage"}

def vols(K):
    t = K.j('nuque')
    return [V('Tete', '#f0ece2', c=(0, t.y - .05, t.z + .02), r=(.08, .085, .075), prio=1)]

def construire(ctx):
    volant('griffon', dict(z=.85, corps=('#b8863a', '#d8a85a', '#e8d0a0'), aile=('#efe8da', '#a87a3a'), forme='plumes', tete='bec',
                           bec=OR, envergure=1.0, queue=.9, oeil='#ffcf3a', relief=RELIEF_POIL, volumes=vols))

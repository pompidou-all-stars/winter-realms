"""Béhémoth (palier 3, sol) — kit 2.40 : bête colossale et trapue à cuir violet sombre, cornes en arc, plaques osseuses, défenses."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Béhémoth"}

def pieces(K):
    nu, m = K.j('nuque'), K.j('museau')
    return (plaques_dos(K, '#c8b8a0', n=6, taille=1.1) + griffes(K) +
            [corne(f'Corne.{n}', '#e8dcc0', 'Tete', (s * .1, nu.y - .05, nu.z + .1), .045, .28, 1.6, rot=(-.5, s * 1.2, 0), n=5) for s, n in ((1, 'L'), (-1, 'R'))] +
            [corne(f'Defense.{n}', '#e8dcc0', 'Tete', (s * .06, m.y + .12, m.z - .05), .03, .14, 1.0, rot=(-.6, s * .3, 0)) for s, n in ((1, 'L'), (-1, 'R'))])

def construire(ctx):
    bete('behemoth', dict(z=1.7, poil=('#4a3a5a', '#6a5a7a', '#8a7a98'), patte='#2a2034', crete='#2a2034', tete='taureau', tete_r=1.4,
                          longueur=1.0, pattes=.9, epaisseur=1.6, cou=.85, queue=.6, relief=RELIEF_ECAILLE, ecailles=6, oeil='#ff5a2a', ech=.9,
                          duree=.7, foulee=.35, pieces=pieces))

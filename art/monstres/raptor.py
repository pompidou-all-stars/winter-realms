"""Chevaucheur de raptor (palier 1, sol) — kit 2.40 : homme-lézard à la lance sur un raptor vert à crête rouge et longue queue."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Chevaucheur de raptor"}
cv = {}

def lance(s, b): return lance_cavalier(s, b, col='#e8d8a0', bouclier='#3a6a8a')

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#3f8a5a', '#5aa874', '#2c6a42'), tissu='#3a6a8a', taille=.72, pieces=lance)
    return v

def pieces(K):
    return cv['p'] + meches_dos(K, '#c8322a', n=5, taille=.7, rangs=False) + griffes(K)

def construire(ctx):
    bete('chevaucheur_raptor', dict(z=.95, poil=('#4f8a3a', '#7aa84a', '#d8c890'), patte='#3a5a2a', crete='#c8322a', tete='lezard',
                                    longueur=1.05, pattes=1.05, epaisseur=.85, cou=1.0, queue=1.5, relief=RELIEF_ECAILLE,
                                    oeil='#ffd23a', ech=1.2, volumes=vols, pieces=pieces))

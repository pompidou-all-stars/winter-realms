"""Archiliche (palier 3, spécial, résurrection — capacité à venir) — kit 2.40 : sorcier squelette flottant en robe violette et or,
couronne de fer, bâton à crâne et orbe vert, phylactère lumineux ; il relève les morts."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Archiliche"}

def pieces(K):
    p = K.j('poitrine')
    K.lueurs.append(boule('Phylactere', '#7aff8a', 'Torse', (0, -.19, p.z), .035, ech=(1, 1, 1.4), seg=8))
    return (casque(K, 'couronne', col='#3a3a40') + arme(K, 'baton', taille=1.35, col=OR) + cape(K, col='#3a1a5a', longueur=1.1) +
            epaulieres(K, col='#3a1a5a', taille=.9, pointes=3, col_pointe=OS_, bord=OR))

def construire(ctx):
    bipede('archiliche', dict(z=1.3, peau=('#e6e2d2', '#d0ccbc', '#b8b4a4'), bas='#3a1a5a', tete='crane', bas_du_corps='traine',
                              carrure=.95, bras=1.1, muscle=0, ventre=.7, voute=.3, relief=RELIEF_PIERRE, magie='#7aff8a', oeil='#7aff8a',
                              pieces=pieces))

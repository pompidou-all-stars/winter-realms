"""Char des tombes (palier 2, spécial, résurrection — capacité à venir) — kit 2.40 : carrosse funèbre noir et violet à lanternes
spectrales, tiré par un destrier squelettique fantôme (inspiré des chars des comtes vampires)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Char des tombes"}

def pieces(K):
    b = K.j('bassin'); y = b.y + .4; z = .32; out = []
    out += [plaque('Carrosse', '#1e1a24', 'Hanches', (0, y, z + .2), .42, .46, .36), plaque('Toit', '#4a2a5a', 'Hanches', (0, y, z + .41), .48, .52, .05),
            plaque('Porte', '#4a2a5a', 'Hanches', (.215, y, z + .2), .01, .18, .26)]
    for s, n in ((1, 'L'), (-1, 'R')):
        for k, dy in enumerate((-.16, .16)):
            out += [tore(f'Roue{k}.{n}', '#2a2430', 'Hanches', (s * .26, y + dy, .14), .13, .018, rot=(0, math.pi / 2, 0), seg=12, seg2=4)]
        K.lueurs.append(boule(f'Lanterne.{n}', '#b07aff', 'Hanches', (s * .25, y - .25, z + .42), .035, seg=8))
    for k in range(4):
        out.append(cone(f'Pic{k}', '#4a2a5a', 'Hanches', ((k % 2 - .5) * .36, y + (k // 2 - .5) * .4, z + .43), .02, .002, .08, seg=4))
    out.append(plaque('Timon', '#2a2430', 'Hanches', (0, b.y + .05, .3), .03, .5, .03))
    return out + meches_dos(K, '#b07aff', n=4, taille=.6, rangs=False)

def construire(ctx):
    bete('char_tombes', dict(z=1.1, poil=('#d0ccbc', '#e6e2d2', '#8a8678'), patte='#b8b4a4', crete='#b07aff', tete='cheval', tete_r=.9,
                             longueur=.95, pattes=1.15, epaisseur=.65, cou=1.0, queue=.5, relief=RELIEF_PIERRE, oeil='#b07aff',
                             ech=1.0, duree=.45, foulee=.55, pieces=pieces))

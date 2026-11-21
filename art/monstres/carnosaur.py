"""Carnosaure monté (palier 3, sol) — kit 2.40 : énorme saurien carnivore à grande gueule, crête rouge, monté par un chef homme-lézard
à lance d'or et coiffe de plumes."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Carnosaure monté"}
cv = {}

def armes(s, b):
    return lance_cavalier(s, b, col=OR, manche='#5a3a22', longueur=.75, bouclier='#c8a040') + [
        corne(f'Plume{k}', ('#c8322a', '#e8b23a', '#3ac8c0')[k], 'Dos', ((k - 1) * .03, b.y + .02, b.z + .42 * s), .02, .12, .6, rot=(-.5, (k - 1) * .4, 0), seg=4, n=2)
        for k in range(3)]

def vols(K):
    v, cv['p'] = cavalier(K, peau=('#3f8a5a', '#5aa874', '#2c6a42'), tissu='#c8a040', taille=.75, pieces=armes)
    return v

def pieces(K):
    m = K.j('museau')
    return cv['p'] + meches_dos(K, '#c8322a', n=6, taille=.9, rangs=False) + griffes(K) + [
        corne(f'Dent{k}.{n}', OS_, 'Tete', (s * .05, m.y + .05 + .04 * k, m.z - .03), .012, .045, .3, rot=(math.pi, 0, 0), seg=4, n=2)
        for s, n in ((1, 'L'), (-1, 'R')) for k in range(3)]

def construire(ctx):
    bete('carnosaure', dict(z=1.45, poil=('#6a5a3a', '#8a7a52', '#d8c8a0'), patte='#4a3e28', crete='#c8322a', tete='lezard', tete_r=1.4,
                            longueur=1.1, pattes=1.15, epaisseur=1.25, cou=1.0, queue=1.5, relief=RELIEF_ECAILLE, oeil='#ffcf3a',
                            ech=1.0, duree=.55, volumes=vols, pieces=pieces))

"""Élu des Ruines (palier 3, sol) — kit 2.40 : champion en armure noire et cuivre, heaume à grandes cornes, monté sur une bête
cuirassée à cornes (notre version des élus du Chaos sur leur monture démoniaque)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Élu des Ruines"}
ARM, CUIV = '#2a2630', '#b8743a'
cv = {}

def armes(s, b):
    out = lance_cavalier(s, b, col='#8a8f99', manche=ARM, longueur=.7, bouclier=ARM)
    for sg in (1, -1):
        out.append(corne(f'CorneC{sg}', CUIV, 'Dos', (sg * .05 * s, b.y - .02, b.z + .4 * s), .02, .14, .9, rot=(-.4, sg * 1.1, 0), seg=5, n=3))
    return out

def vols(K):
    v, cv['p'] = cavalier(K, peau=(ARM, '#3a3640', '#1a181e'), tissu=ARM, taille=.8, pieces=armes)
    return v

def pieces(K):
    nu = K.j('nuque')
    return cv['p'] + plaques_dos(K, CUIV, n=4, taille=.7) + griffes(K, col=CUIV) + [
        corne(f'CorneM.{n}', CUIV, 'Tete', (s * .09, nu.y - .05, nu.z + .08), .035, .2, 1.0, rot=(-.3, s * 1.3, 0)) for s, n in ((1, 'L'), (-1, 'R'))]

def construire(ctx):
    bete('elu_ruines', dict(z=1.35, poil=('#5a2a2a', '#7a3a34', '#3a1a1a'), patte='#2a1414', crete=CUIV, tete='taureau', tete_r=1.3,
                            longueur=1.0, pattes=1.0, epaisseur=1.4, cou=.95, queue=.6, relief=RELIEF_ECAILLE, ecailles=7, oeil='#ff3a2a', ech=1.0,
                            duree=.5, volumes=vols, pieces=pieces))

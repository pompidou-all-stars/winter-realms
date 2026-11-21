"""Prêtre-crapaud (palier 2, spécial, soin) — kit 2.40 : énorme crapaud sacré en robe d'or et de turquoise, couronne, bâton à orbe vert,
glyphes lumineux (inspiré des prêtres-crapauds des hommes-lézards)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Prêtre-crapaud"}

def pieces(K):
    p = K.j('poitrine')
    K.lueurs += [plaque(f'Glyphe{k}', '#6fcf97', 'Torse', (x, -.19, p.z), .03, .01, .04) for k, x in enumerate((-.06, .06))]
    return casque(K, 'couronne', col=OR) + arme(K, 'baton', taille=1.1, col=OR) + collier_crocs(K, col='#3ac8c0', cordon=OR, n=5)

def construire(ctx):
    bipede('pretre_crapaud', dict(z=1.05, peau=('#5a8a3a', '#8ab85a', '#3a6a2a'), bas='#3ac8c0', tete='crapaud', tete_r=1.25, tete_h=.2,
                                  bas_du_corps='robe', ventre=1.7, carrure=1.3, muscle=0, voute=.2, jambes=.3, relief=RELIEF_PEAU, taches=.25,
                                  magie='#6fcf97', oeil='#ffe43a', lourd=1.5, pieces=pieces))

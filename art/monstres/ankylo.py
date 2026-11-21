"""Ankylosaure de guerre (palier 1, spécial, blindé) — kit 2.40 : saurien bas et large, cuir brun à grandes écailles, écussons et plaques osseuses, massue au bout de la queue."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Ankylosaure de guerre"}

def pieces(K):
    q2, re, b = K.j('queue2'), K.j('reins'), K.j('bassin')
    return plaques_dos(K, '#c8b890', n=7, taille=.9) + [
        boule('Massue', '#c8b890', 'Queue2', tuple(q2), .08, ech=(1.3, 1, .8), seg=10)] + [
        cone(f'Epine{k}.{n}', '#e0d4b0', 'Dos' if k < 2 else 'Hanches', (s * .2, re.y - .15 + .17 * k, re.z), .025, .002, .09, rot=(0, s * 1.5, 0), seg=5)
        for s, n in ((1, 'L'), (-1, 'R')) for k in range(4)] + griffes(K) + [
        boule(f'Ecusson{k}', '#a89870', 'Dos' if k < 6 else 'Hanches', (((k % 3) - 1) * .12, re.y - .2 + .1 * (k // 3), re.z + .17 - .03 * abs((k % 3) - 1)), .065, ech=(1, 1, .6), seg=7)
        for k in range(9)]   # 2.40 : rangées d'écussons osseux (cuirasse d'écailles)

def construire(ctx):
    bete('ankylosaure', dict(z=1.0, poil=('#7a6a4a', '#968660', '#c8b890'), patte='#4a3e2a', crete='#968660', tete='lezard', tete_r=.9,
                             longueur=1.1, pattes=.7, epaisseur=1.45, cou=.55, queue=1.2, relief=RELIEF_ECAILLE, oeil='#ffcf3a',
                             ech=1.05, duree=.6, foulee=.4, pieces=pieces))

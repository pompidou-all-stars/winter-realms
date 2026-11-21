"""Manticore (palier 2, volant) — kit 2.40 : lion rouge-orangé à crinière sombre, ailes de chauve-souris, queue de scorpion à dard."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Manticore"}

def vols(K):
    nu = K.j('nuque')
    return [V('Cou', '#4a2a1a', c=(0, nu.y + .04, nu.z - .01), r=(.12, .1, .11), prio=1)]   # crinière

def pieces(K):
    q2 = K.j('queue2')
    return [corne('Dard', '#2a1a1a', 'Queue2', tuple(q2), .04, .14, 1.5, rot=(-.3, 0, 0), seg=6, n=4)] + [
        boule(f'Anneau{k}', '#8a3a1a', 'Queue2' if k else 'Queue1', tuple(K.j('queue1').lerp(q2, k / 2)), .04, seg=8) for k in range(3)]

def construire(ctx):
    volant('manticore', dict(z=1.2, corps=('#c8743a', '#d8945a', '#e8c090'), aile=('#6a2a1a', '#8a3a24'), tete='felin', tete_r=1.2,
                             envergure=.95, queue=1.1, epaisseur=1.2, relief=RELIEF_POIL, oeil='#ffcf3a', volumes=vols, pieces=pieces))

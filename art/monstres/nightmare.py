"""Destrier de cauchemar (palier 3, spécial, accéléré) — kit 2.40 : cheval noir démoniaque, crinière et queue de flammes violettes,
sabots enflammés, cornes, yeux ardents."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Destrier de cauchemar"}

def pieces(K):
    nu = K.j('nuque'); q2 = K.j('queue2')
    K.lueurs += [cone(f'Criniere{k}', '#c87aff', 'Cou' if k < 3 else 'Dos', (0, nu.y + .08 + .08 * k, nu.z + .05 - .03 * k), .04, .002, .14,
                      rot=(-.9, 0, 0), seg=5) for k in range(5)]
    K.lueurs += [cone(f'QueueFeu{k}', '#c87aff', 'Queue2', (0, q2.y - .04 * k, q2.z + .03 * k), .04, .002, .14, rot=(-2.2, 0, (k - 1) * .3), seg=5) for k in range(3)]
    for s, n in ((1, 'L'), (-1, 'R')):
        for pat, j in (('PatteAvant', 'poignet.L'), ('PatteArriere', 'cheville.L')):
            w = K.j(j); K.lueurs.append(boule(f'Sabot{pat}.{n}', '#c87aff', f'{pat}.{n}', (s * w.x, w.y - .05, .03), .045, ech=(1, 1, .5), seg=8))
    return [corne(f'Corne.{n}', '#1a1a1a', 'Tete', (s * .05, nu.y - .05, nu.z + .1), .02, .12, .9, rot=(-.6, s * .3, 0), seg=5, n=3) for s, n in ((1, 'L'), (-1, 'R'))]

def construire(ctx):
    bete('destrier_cauchemar', dict(z=1.3, poil=('#1e1a24', '#2e2834', '#3a3044'), patte='#141018', crete='#c87aff', tete='cheval',
                                    longueur=1.05, pattes=1.25, epaisseur=1.0, cou=1.1, queue=.8, relief=RELIEF_POIL, oeil='#e8b0ff',
                                    ech=1.0, duree=.4, foulee=.6, pieces=pieces))

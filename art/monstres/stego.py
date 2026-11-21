"""Stégosaure de guerre (palier 2, spécial, blindé) — kit 2.40 : grand saurien à petite tête, rangée de grandes plaques dorsales
rouge et crème, queue à quatre piques, harnais de bronze."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Stégosaure de guerre"}

def pieces(K):
    q2 = K.j('queue2'); re = K.j('reins')
    return (plaques_dos(K, '#c84a2a', n=8, taille=1.4) +
            [cone(f'Pique{k}', '#e8dcc0', 'Queue2', (sg * .04, q2.y - .05 * (k // 2), q2.z + .02), .03, .002, .16, rot=(-.5, sg * 1.2, 0), seg=5)
             for k, sg in enumerate((1, -1, 1, -1))] +
            [tore('Harnais', '#b07a3a', 'Dos', (0, re.y - .05, re.z), .26, .014, rot=(math.pi / 2, 0, 0), ech=(1, 1, 1.15), seg=14, seg2=4)] + griffes(K))

def construire(ctx):
    bete('stegosaure', dict(z=1.1, poil=('#6a7a5a', '#8a9a72', '#d8c8a0'), patte='#4a5a3e', crete='#c84a2a', tete='lezard', tete_r=.75,
                            longueur=1.2, pattes=.95, epaisseur=1.35, cou=.8, queue=1.3, tete_z=-.12, relief=RELIEF_ECAILLE, oeil='#ffcf3a',
                            ech=1.1, duree=.65, foulee=.4, pieces=pieces))

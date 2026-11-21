"""Roue foudroyante (palier 2, sol) — kit 2.40 : grande roue de guerre des hommes-rats, cerclée de fer, moyeu à cristal vert
crépitant, pointes sur la jante (engin sans pattes)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Roue foudroyante"}

def pieces(K):
    re = K.j('reins'); c = (0, re.y - .1, .42); out = []
    for s in (1, -1):
        out.append(tore(f'Jante{s}', '#5a4a3a', 'Dos', (s * .14, c[1], c[2]), .4, .035, rot=(0, math.pi / 2, 0), seg=16, seg2=5))
        out.append(tore(f'Cercle{s}', FER, 'Dos', (s * .16, c[1], c[2]), .4, .018, rot=(0, math.pi / 2, 0), seg=16, seg2=4))
    for k in range(6):
        a = k * math.pi / 3
        out.append(cone(f'Rayon{k}', BOIS, 'Dos', (0, c[1], c[2]), .02, .02, .38, rot=(a, 0, 0), seg=5))
        out.append(cone(f'Pic{k}', FER, 'Dos', (0, c[1] - math.sin(a) * .42, c[2] + math.cos(a) * .42), .025, .002, .08, rot=(a, 0, 0), seg=5))
    K.lueurs.append(boule('Coeur', '#7aff5a', 'Dos', c, .1, seg=10))
    K.lueurs += [cone(f'Arc{k}', '#bfffaa', 'Dos', c, .008, .002, .36, rot=(k * math.pi / 3 + math.pi / 6, 0, 0), seg=3) for k in range(6)]   # arcs électriques
    out += [tore(f'Cage{k}', '#c8a040', 'Dos', c, .14, .012, rot=(0, math.pi / 2, k * math.pi / 2), seg=12, seg2=3) for k in range(2)]
    return out

def construire(ctx):
    bete('roue_foudroyante', dict(z=1.3, poil=('#5a4a3a', '#7a6a58', '#4a3a2e'), tete='aucune', queue=0, sans_pattes=True, epaisseur=.12, longueur=.4,
                                  relief=RELIEF_LISSE, oeil='#7aff5a', ech=1.0, duree=.35, foulee=.1, pieces=pieces))

"""Ver des neiges (palier 3, sol) — kit 2.40 : ver géant d'un seul tenant, chair blanc bleuté marbrée, anneaux de chitine, gueule
ronde béante garnie de crocs, piquants de glace sur le dos (corps sans pattes qui ondule)."""
from communs.creatures import *
INFOS = {'categorie': 'monstre', 'titre': "Ver des neiges"}
CHAIR, ANNEAU = '#dde5ee', '#9fb0c4'

def _points(K):
    b, re, ga, nu = K.j('bassin'), K.j('reins'), K.j('garrot'), K.j('nuque')
    return [('Queue2', K.j('queue2'), .07), ('Queue1', K.j('queue1'), .12), ('Hanches', b, .17), ('Dos', re, .2), ('Dos', ga, .21), ('Cou', nu, .2)]

def vols(K):
    pts = _points(K); v = []
    for (o1, p1, r1), (o2, p2, r2) in zip(pts, pts[1:]):   # un seul corps continu : capsules qui se chevauchent
        v.append(V(o2, CHAIR, a=(0, p1.y, max(r1, p1.z - .3)), b=(0, p2.y, max(r2, p2.z - .3)), ra=r1, rb=r2))
    nu = K.j('nuque')
    v.append(V('Tete', CHAIR, a=(0, nu.y, max(.2, nu.z - .3)), b=(0, nu.y - .2, nu.z - .14), ra=.2, rb=.19))
    v.append(V('Tete', '#5a1a2a', c=(0, nu.y - .33, nu.z - .14), r=(.14, .04, .14), prio=3, rel=0))
    v.append(V('Tete', '#c85a6a', c=(0, nu.y - .31, nu.z - .14), r=(.1, .03, .1), prio=4, rel=0))
    return v

def pieces(K):
    nu = K.j('nuque'); out = []
    for k, (o, p, r) in enumerate(_points(K)[1:]):   # anneaux de chitine
        out.append(tore(f'Anneau{k}', ANNEAU, o, (0, p.y, max(r, p.z - .3)), r * 1.0, .03 * r / .2 + .008, rot=(math.pi / 2, 0, 0), seg=14, seg2=4))
    out.append(tore('Levre', ANNEAU, 'Tete', (0, nu.y - .31, nu.z - .14), .17, .035, rot=(math.pi / 2, 0, 0), seg=14, seg2=5))
    for k in range(10):
        a = k * math.pi / 5
        out.append(cone(f'Croc{k}', OS_, 'Tete', (math.cos(a) * .13, nu.y - .31, nu.z - .14 + math.sin(a) * .13), .022, .001, .08,
                        rot=(math.pi / 2, 0, -a * 0), seg=4))
    out += [cone(f'Glace{k}', '#bfe6ff', 'Dos' if k < 4 else 'Hanches', (0, K.j('garrot').y + .12 * k, .44 - .03 * k), .04, .002, .16, seg=5) for k in range(6)]
    return out

def construire(ctx):
    bete('ver_neiges', dict(z=1.5, poil=(CHAIR, '#eef2f5', '#c8d0d8'), tete='aucune', queue=1.0, sans_pattes=True, epaisseur=.4,
                            longueur=1.2, relief=RELIEF_PEAU, taches=.3, taille_taches=5, oeil='#7fd8ff', ech=.9, duree=.8, foulee=.1,
                            volumes=vols, pieces=pieces))

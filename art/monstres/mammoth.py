"""Mammouth de guerre (palier 3, sol) : mammouth laineux aux longues défenses recourbées, trompe,
nacelle de bois et étendard sur le dos. Très lent, énorme. Proposé pour la PR B (clé CR « mammoth »)."""
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 1.45
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Mammouth de guerre"}

def fabriquer():
    c = collection('mammouth_guerre'); dans(c)
    r = pivot('mammouth_guerre'); H = hauteur()
    corps = quadrupede(r, dict(poil='#6e4a30', poil2='#80583a', ventre='#5a3a24', patte='#4a3426', yeux='#ffffff',
                               museau='tortue', tete=.3, queue='#4a3426', largeur=.3, pattes=.48, epaisseur=.32,
                               lqueue=.12), H * .82, H * 1.1)
    T = piece(r, 'Tete'); rt = H * .82 * .3
    sphere('Bosse', '#80583a', rt * .7, (0, rt * .3, rt * .65), (1, 1, .9), 10, 6, T)
    for s in (-1, 1): sphere(f'Oreille{s}', '#5a3a24', rt * .5, (s * rt * .85, rt * .1, 0), (.35, 1, 1.1), 8, 5, T)
    # trompe : trois segments qui descendent en se recourbant vers l'avant
    p, bout = T, (0, -rt * .95, -rt * .2)
    for k, (lg, rx) in enumerate(((rt * .7, .05), (rt * .6, -.45), (rt * .5, -.7))):
        p = pivot(f'Trompe{k}', bout, p); p.rotation_euler = (rx, 0, 0)
        cylindre(f'TrompeSeg{k}', '#7a5236', rt * (.24 - k * .05), rt * (.3 - k * .06), lg, 8, (0, 0, -lg), p)
        bout = (0, 0, -lg)
    for s in (-1, 1):
        d = pivot(f'Defense{s}', (s * rt * .45, -rt * .8, -rt * .45), T); d.rotation_euler = (1.6, s * .3, 0)
        cone(f'DefenseA{s}', '#fff3d6', rt * .14, rt * 1.0, 8, (0, 0, 0), d)
        cone(f'DefenseB{s}', '#fff3d6', rt * .09, rt * .55, 6, (0, 0, rt * .95), d, (-1.4, 0, 0))
    # nacelle et étendard
    boite('Tapis', '#9b2f2f', H * .62, H * .55, H * .03, (0, H * .08, H * .3), 0, corps)
    boite('Nacelle', '#8a6040', H * .4, H * .36, H * .14, (0, H * .08, H * .38), H * .02, corps)
    for sx in (-1, 1):
        for sy in (-1, 1): cylindre(f'Montant{sx}{sy}', '#5a3a22', H * .012, H * .012, H * .16, 5, (sx * H * .17, H * .08 + sy * H * .15, H * .44), corps)
    cylindre('Hampe', '#5a3a22', H * .012, H * .012, H * .4, 5, (H * .15, H * .22, H * .44), corps)
    prisme('Etendard', '#c0392b', [(0, 0), (H * .16, -H * .02), (H * .12, -H * .07), (H * .16, -H * .12), (0, -H * .12)], H * .01,
           (H * .15, H * .22, H * .84), corps)
    peindre(r)
    trot(r, duree=1.3, ampl=.3, rebond=H * .015, queue=.15)
    return r

def construire(ctx):
    preparer(fabriquer())

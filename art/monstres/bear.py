"""Ours de guerre (palier 2, sol) : grand ours brun en armure, chanfrein et plaques d'acier sur le dos,
oreilles rondes, griffes claires. Proposé pour la PR B (clé CR « bear »)."""
from communs.outils import collection, dans, pivot, peindre, sphere, boite, cone, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 1.15
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Ours de guerre"}

def fabriquer():
    c = collection('ours_guerre'); dans(c)
    r = pivot('ours_guerre'); H = hauteur()
    corps = quadrupede(r, dict(poil='#6a4630', poil2='#7f5639', ventre='#9a6c4a', patte='#4a3020', yeux='#ffffff',
                               museau='tortue', tete=.24, queue='#4a3020', largeur=.24, pattes=.42, epaisseur=.27,
                               lqueue=.1), H * .85, H * 1.3)
    T = piece(r, 'Tete'); rt = H * .85 * .24
    sphere('Truffe', '#1b1b1b', rt * .18, (0, -rt * 1.25, -rt * .05), (1.2, .8, .8), 6, 4, T)
    for s in (-1, 1): sphere(f'OreilleRonde{s}', '#5a3a26', rt * .28, (s * rt * .65, rt * .1, rt * .75), (1, .5, 1), 8, 5, T)
    boite('Chanfrein', '#7d8590', rt * .55, rt * .9, rt * .1, (0, -rt * .55, rt * .72), rt * .04, T, (-.35, 0, 0), metal=.2, rough=.5)
    for k in range(3):
        boite(f'Plaque{k}', '#7d8590', H * .36, H * .2, H * .06, (0, -H * .12 + k * H * .2, H * .3 - k * H * .02), H * .02, corps,
              (.1, 0, 0), metal=.2, rough=.5)
    for o in list(c.objects):
        if o.name.startswith('PatteJambeA'):
            for k in (-1, 0, 1): cone(f'Griffe{o.name}{k}', '#f4efe0', H * .015, H * .05, 4, (k * H * .03, -H * .07, -H * .01), o, (1.6, 0, 0))
    peindre(r)
    trot(r, duree=.7, ampl=.45, rebond=H * .03, queue=.1)
    return r

def construire(ctx):
    preparer(fabriquer())

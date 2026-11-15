"""Destrier de cauchemar (palier 3, magique : accéléré) : cheval noir à crinière et queue de flammes
violettes, yeux rouges, sabots ardents ; galope de plus en plus vite. Clé CR « nightmare »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.betes import quadrupede, yeux_bete
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.3
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Destrier de cauchemar"}

def fabriquer():
    c = collection('destrier_cauchemar'); dans(c)
    r = pivot('destrier_cauchemar'); H = hauteur()
    quadrupede(r, dict(poil='#1f1c24', poil2='#2a2630', ventre='#2a2630', patte='#14121a', yeux='#ff3a3a', oreilles=1,
                       museau='loup', tete=.2, queue='#a04aff', largeur=.18, pattes=.58, epaisseur=.2, lqueue=.5), H * .7, H * 1.25)
    T = piece(r, 'Tete'); rt = H * .7 * .2
    for k in range(5): cone(f'Criniere{k}', '#a04aff', rt * .2, rt * .8, 4, (0, rt * (.4 + k * .35), rt * (.6 - k * .15)), T, (-.9, 0, 0), emis=2.5)
    for o in list(c.objects):
        if o.name.startswith('Patte'): sphere(f'Flamme{o.name}', '#c77dff', H * .05, (0, 0, -H * .02), (1, 1, .6), 6, 4, o, emis=2)
    for o in list(c.objects):
        if o.name.startswith('QueueCone'): o.data.materials[0] = __import__('communs.outils', fromlist=['mat']).mat('#a04aff', emis=2.5)
    piece(r, 'Queue').rotation_euler = (-.25, 0, 0)  # queue de flammes qui flotte derrière
    peindre(r)
    trot(r, duree=.4, ampl=.8, rebond=H * .04, queue=.6)
    return r

def construire(ctx):
    preparer(fabriquer())

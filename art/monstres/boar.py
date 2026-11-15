"""Sanglier de guerre (palier 1, sol) : gros sanglier brun-roux à crête noire, défenses d'ivoire recourbées,
selle de cuir rivetée sur le dos. Charge au trot. Proposé pour la PR B (clé CR « boar »)."""
from communs.outils import collection, dans, pivot, peindre, cone, boite, sphere, descendants
from communs.betes import quadrupede
from communs.animations import trot
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 0.9
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Sanglier de guerre"}

def fabriquer():
    c = collection('sanglier_guerre'); dans(c)
    r = pivot('sanglier_guerre'); H = hauteur()
    corps = quadrupede(r, dict(poil='#7a4a2e', poil2='#93603c', ventre='#b98a5e', patte='#3a2a20', crete='#2b211c',
                               yeux='#ff7a3a', oreilles=1, museau='tortue', tete=.27, queue='#3a2a20', largeur=.21,
                               pattes=.4, epaisseur=.24, lqueue=.2), H * .8, H * 1.35)
    T = piece(r, 'Tete'); rt = H * .8 * .27
    sphere('Groin', '#c98a7a', rt * .32, (0, -rt * 1.22, -rt * .15), (1.1, .5, .85), 8, 5, T)
    for s in (-1, 1):
        cone(f'Defense{s}', '#fff6dc', rt * .09, rt * .6, 6, (s * rt * .4, -rt * 1.0, -rt * .35), T, (-.6, s * .5, 0))
    boite('Selle', '#5a3a22', H * .3, H * .45, H * .05, (0, H * .1, H * .25), H * .02, corps)
    for s in (-1, 1):
        for k in (-1, 1): sphere(f'Rivet{s}{k}', '#c9ced6', H * .025, (s * H * .13, H * .1 + k * H * .16, H * .28), (1, 1, .6), 6, 4, corps, metal=.6)
    peindre(r)
    trot(r, duree=.45, ampl=.65, rebond=H * .05, queue=.6)
    return r

def construire(ctx):
    preparer(fabriquer())

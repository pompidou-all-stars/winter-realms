"""Lutin des glaces (magique : accéléré) : petit lutin bleu glacier aux grandes oreilles, long nez pointu,
bonnet à pompon, écharpe rouge qui flotte, cristaux brillants aux poings. Il court de plus en plus vite.
Proposé pour la PR B (clé CR « imp »)."""
from communs.outils import collection, dans, pivot, peindre, sphere, prisme, descendants
from communs.personnages import humanoide
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 0.7
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Lutin des glaces"}

def fabriquer():
    c = collection('lutin_glaces'); dans(c)
    r = pivot('lutin_glaces'); H = hauteur()
    humanoide(r, dict(peau='#6fc6e8', peau2='#8fd8f2', tissu='#2f5f9a', torse='#3a76b8', cuir='#e8f4fb', botte='#1f3f6a',
                      carrure=.8, tete=.17, jambes=.32, voute=.35, nez=('long', .35), oreilles=.7, sourcils=1,
                      yeux='#ffe45e', bonnet='#e8f4fb'), H)
    Cr = piece(r, 'Crane'); rh = H * .17
    sphere('Pompon', '#ffffff', rh * .3, (0, rh * 1.3, rh * 1.4), (1, 1, 1), 8, 5, Cr)
    B = piece(r, 'Buste')
    prisme('Echarpe', '#e04a5a', [(-H * .05, 0), (H * .05, 0), (H * .03, -H * .2), (-H * .03, -H * .17)], H * .015, (0, H * .1, H * .3), B, (-1.0, 0, 0))
    for o in list(c.objects):
        if o.name.startswith('Poing'): sphere(f'Cristal{o.name}', '#9ff3ff', H * .03, (0, 0, H * .05), (.7, .7, 1.4), 6, 4, o, emis=3)
    peindre(r)
    marche(r, duree=.4, ampl_jambe=.8, ampl_bras=.7, rebond=H * .07, roulis=.15)
    return r

def construire(ctx):
    preparer(fabriquer())

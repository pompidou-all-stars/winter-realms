"""Yéti (palier 2, sol) : colosse à fourrure blanche, visage gris-bleu, cornes courtes, gros poings,
bracelets de glace. Proposé pour la PR B (clé CR « yeti »)."""
from communs.outils import collection, dans, pivot, peindre, sphere, cone, descendants
from communs.personnages import humanoide
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 1.15
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Yéti"}

def fabriquer():
    c = collection('yeti'); dans(c)
    r = pivot('yeti'); H = hauteur()
    humanoide(r, dict(peau='#f1f5f8', peau2='#8ea4b8', tissu='#e2eaf0', torse='#f7fafc', cuir='#9fe6ff', botte='#dfe7ee',
                      carrure=1.4, tete=.11, jambes=.3, voute=.3, nez=('rond', .2), machoire=1, sourcils=1, defenses=1,
                      yeux='#4ad2ff', epaulieres='cuir'), H)
    Cr = piece(r, 'Crane'); rh = H * .11
    sphere('Face', '#8ea4b8', rh * .75, (0, -rh * .45, -rh * .15), (1, .7, .9), 10, 6, Cr)
    for s in (-1, 1): cone(f'CorneY{s}', '#5a6a7a', rh * .18, rh * .55, 6, (s * rh * .7, 0, rh * .7), Cr, (0, s * .7, 0))
    for o in list(c.objects):
        if o.name.startswith('Epauliere'):  # touffes de fourrure sur les épaules
            for k in range(3): cone(f'Touffe{o.name}{k}', '#ffffff', H * .03, H * .08, 4, (0, (k - 1) * H * .04, H * .05), o)
    peindre(r, cime=1.15)
    marche(r, duree=1.0, ampl_jambe=.45, ampl_bras=.55, rebond=H * .04, roulis=.1)
    return r

def construire(ctx):
    preparer(fabriquer())

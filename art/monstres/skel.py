"""Squelette du givre (palier 1, sol) : guerrier squelette maigre, os blanchis par le gel, casque rouillé,
haillons bleu nuit, yeux cyan et vieille épée. Proposé pour la PR B (clé CR « skel »)."""
from communs.outils import collection, dans, pivot, peindre, sphere, descendants
from communs.personnages import humanoide, epee
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py, qui sera complété avec la PR B)
Z = 0.85
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Squelette du givre"}

def fabriquer():
    c = collection('squelette_givre'); dans(c)
    r = pivot('squelette_givre'); H = hauteur()
    humanoide(r, dict(peau='#e6e2d2', peau2='#cfc9b4', tissu='#2f3d5c', torse='#e6e2d2', cuir='#5a4a3a', botte='#cfc9b4',
                      metal='#8a7a6a', carrure=.72, tete=.13, jambes=.4, voute=.12, nez=('rond', .12), machoire=1,
                      sourcils=1, yeux='#7ff3ff', casque='#8a6a4a', epaulieres='or',
                      arme=lambda p, HH: epee(p, HH, '#9aa3ad', '#8a6a4a')), H)
    # côtes visibles sur le torse
    B = piece(r, 'Buste')
    for k in range(3): sphere(f'Cote{k}', '#f4f1e6', H * .1, (0, -H * .1, H * (.13 + k * .055)), (1, .25, .18), 8, 4, B)
    peindre(r)
    marche(r, duree=.7, ampl_jambe=.55, ampl_bras=.45, rebond=H * .04, roulis=.12)
    return r

def construire(ctx):
    preparer(fabriquer())

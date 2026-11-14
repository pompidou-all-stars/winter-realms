"""Prêtresse (CR healer, aura de soin) : gobeline en robe verte, couronne de feuilles, baguette à feuille lumineuse."""
from communs.outils import collection, dans, pivot, peindre
from communs.personnages import humanoide, baguette
from communs.animations import marche
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Prêtresse"}

def fabriquer():
    c = collection('pretresse'); dans(c)
    r = pivot('pretresse'); H = hauteur('pretresse')
    humanoide(r, dict(peau='#7cc04a', peau2='#9ad66a', tissu='#2e9e6b', torse='#2e9e6b', robe='#23805a', accent='#f4e27a',
                      cuir='#5a3d26', botte='#3a2a1c', carrure=.85, tete=.16, jambes=.32, nez=('rond', .3), oreilles=.6,
                      couronne='#6fcf97', arme=lambda p, HH: baguette(p, HH, '#9ff0b8')), H)
    peindre(r)
    marche(r, duree=.75, ampl_jambe=.35, ampl_bras=.25, rebond=H * .04, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())

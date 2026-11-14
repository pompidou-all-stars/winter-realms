"""Chaman de guerre (CR chaman, aura de hâte) : gobelin en robe rouge, coiffe de plumes, bâton à orbe doré."""
from communs.outils import collection, dans, pivot, peindre
from communs.personnages import humanoide, baton
from communs.animations import marche
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Chaman de guerre"}

def fabriquer():
    c = collection('chaman_guerre'); dans(c)
    r = pivot('chaman_guerre'); H = hauteur('chaman')
    humanoide(r, dict(peau='#7cc04a', peau2='#9ad66a', tissu='#a8322a', torse='#a8322a', robe='#8a2a22', accent='#e8b23a',
                      cuir='#4a321f', botte='#3a2a1c', carrure=.9, tete=.16, jambes=.32, voute=.15, nez=('long', .3),
                      oreilles=.7, sourcils=1, plumes=['#e8b23a', '#ffffff', '#a8322a'],
                      arme=lambda p, HH: baton(p, HH, '#ffe45e', '#6b4423')), H)
    peindre(r)
    marche(r, duree=.7, ampl_jambe=.4, ampl_bras=.3, rebond=H * .05, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())

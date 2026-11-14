"""Azh'Khar, seigneur des lames (CR hero, boss) : seigneur elfe déchu, armure violette, longues oreilles,
yeux cyan, couronne d'épines, cape, deux lames courbes lumineuses et aura violette au sol.
Personnage original (voir le commentaire « Héros original » dans index.html)."""
from communs.outils import collection, dans, pivot, peindre, anneau
from communs.personnages import humanoide, lame_courbe
from communs.animations import marche
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Azh’Khar, seigneur des lames"}

def fabriquer():
    c = collection('azhkhar'); dans(c)
    r = pivot('azhkhar'); H = hauteur('heros')
    humanoide(r, dict(peau='#c8b5d9', peau2='#d7c6e8', tissu='#33264f', torse='#49335f', accent='#7a5ab0', cuir='#251b38',
                      botte='#251b38', metal='#5b4380', carrure=1.0, tete=.11, jambes=.4, nez=('crochu', .2), oreilles=.9,
                      yeux='#9ffcff', couronne='#b9a0e0', epaulieres='pointes', cape='#33264f',
                      arme=lambda p, HH: lame_courbe(p, HH, '#b9faff'), arme_g=lambda p, HH: lame_courbe(p, HH, '#b9faff')), H)
    anneau('Aura', '#bc8cff', H * .45, H * .02, 20, 3, (0, 0, H * .02), r, emis=2.5)
    for o in c.objects:
        if o.name.startswith('BrasG'): o.rotation_euler = (-.4, -.5, 0)
        if o.name.startswith('BrasD'): o.rotation_euler = (-.4, .5, 0)
    peindre(r)
    marche(r, duree=1.0, ampl_jambe=.4, ampl_bras=.2, rebond=H * .02, roulis=.05)
    return r

def construire(ctx):
    preparer(fabriquer())

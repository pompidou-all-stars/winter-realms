"""Sapeur gobelin (CR gob) : petit gobelin malingre, grandes oreilles, long nez, lunettes de mineur,
bonnet et bombe à la main. Le plus petit des monstres (z 0,75). Animation « marche » sautillante."""
from communs.outils import collection, dans, pivot, peindre
from communs.personnages import humanoide, bombe
from communs.animations import marche
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Sapeur gobelin"}

def fabriquer():
    c = collection('sapeur_gobelin'); dans(c)
    r = pivot('sapeur_gobelin')
    H = hauteur('sapeur_gobelin')
    o = dict(peau='#7cc04a', peau2='#9ad66a', tissu='#6b5a3e', torse='#8a6a44', cuir='#4a321f', botte='#3a2a1c',
             carrure=.85, tete=.17, jambes=.32, voute=.25, sourcils=1, nez=('long', .38), oreilles=.9,
             lunettes=1, bonnet='#a33b2a', arme=bombe)
    humanoide(r, o, H)
    peindre(r)
    marche(r, duree=.55, ampl_jambe=.6, ampl_bras=.5, rebond=H * .08, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())

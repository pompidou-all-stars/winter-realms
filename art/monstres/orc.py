"""Brute orc (CR orc) : guerrier orc trapu et voûté, épaulières à pointes, casque à cornes, hache.
Taille moyenne (z 0,95). Animation « marche » lourde."""
from communs.outils import collection, dans, pivot, peindre
from communs.personnages import humanoide, hache
from communs.animations import marche
from communs.echelles import hauteur
from communs.export_jeu import preparer

INFOS = {'categorie': 'monstre', 'titre': "Brute orc"}

def fabriquer():
    c = collection('brute_orc'); dans(c)
    r = pivot('brute_orc')
    H = hauteur('brute_orc')
    o = dict(peau='#4f9a3a', peau2='#63b04a', tissu='#7a4f2c', torse='#4f9a3a', cuir='#4a321f', botte='#3a2a1c',
             metal='#7d8794', carrure=1.2, tete=.13, jambes=.33, voute=.18,
             machoire=1, sourcils=1, yeux='#ff5a3c', nez=('rond', .26), defenses=1, oreilles=.35,
             cheveux='chignon', epaulieres='pointes', harnais=1, arme=hache)
    humanoide(r, o, H)
    peindre(r)
    marche(r, duree=1.0, ampl_jambe=.5, ampl_bras=.35, rebond=H * .05, roulis=.09)
    return r

def construire(ctx):
    preparer(fabriquer())

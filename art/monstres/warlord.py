"""Seigneur de guerre orc (palier 3, sol) : orc colossal en armure noire et rouge, heaume à cornes,
épaulières à pointes, cape de fourrure, énorme hache. Clé CR « warlord »."""
import math
from communs.outils import collection, dans, pivot, peindre, sphere, cone, cylindre, boite, prisme, anneau, descendants
from communs.personnages import humanoide, epee, hache, marteau, gourdin, baton, bouclier, lame_courbe
from communs.animations import marche
from communs.export_jeu import preparer

# taille selon le facteur z proposé pour CR (même formule que communs/echelles.py) ; voir PALIERS.md
Z = 1.35
def hauteur(): return .40 * Z ** 1.8
def piece(r, nom): return next(o for o in descendants(r) if o.name.split('.')[0] == nom)

INFOS = {'categorie': 'monstre', 'titre': "Seigneur de guerre orc"}

def fabriquer():
    c = collection('seigneur_guerre'); dans(c)
    r = pivot('seigneur_guerre'); H = hauteur()
    humanoide(r, dict(peau='#4f9a3a', peau2='#63b04a', tissu='#2a2c34', torse='#3a2c2c', cuir='#5a1f1f', botte='#2a2c34',
                      metal='#3a3d48', accent='#a8262a', cape='#5a4a3a', carrure=1.4, tete=.11, jambes=.34, voute=.08,
                      machoire=1, sourcils=1, defenses=1, nez=('rond', .24), yeux='#ff5a3c', casque='#3a3d48', cornes=1,
                      epaulieres='pointes', arme=hache), H)
    peindre(r)
    marche(r, duree=.95, ampl_jambe=.4, ampl_bras=.3, rebond=H * .03, roulis=.06)
    return r

def construire(ctx):
    preparer(fabriquer())

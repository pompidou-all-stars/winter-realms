"""Cyclope des cendres (CR cyc) : géant ventru à un seul œil, corne frontale, défenses, énorme massue.
Le plus grand des monstres au sol."""
from outils import collection, dans, pivot, peindre
from personnages import humanoide, gourdin
from animations import marche
from echelles import hauteur

def fabriquer():
    c = collection('cyclope_cendres'); dans(c)
    r = pivot('cyclope_cendres'); H = hauteur('cyclope')
    humanoide(r, dict(peau='#d49a68', peau2='#e9bf95', tissu='#6b4a2f', torse='#d49a68', cuir='#4a321f', botte='#8a5a33',
                      carrure=1.45, tete=.12, jambes=.33, voute=.15, machoire=1, nez=('rond', .22), defenses=1,
                      un_oeil=1, yeux='#ff6a2a', corne='#3a3330', harnais=1,
                      arme=lambda p, HH: gourdin(p, HH, '#5a3d26')), H)
    peindre(r)
    marche(r, duree=1.2, ampl_jambe=.45, ampl_bras=.35, rebond=H * .03, roulis=.08)
    return r

if __name__ == '__main__': fabriquer()

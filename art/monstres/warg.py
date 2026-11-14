"""Warg (CR wolf) : grand loup gris aux yeux rouges, crête de poils noirs, crocs. Rapide. Animation « marche » au trot."""
from outils import collection, dans, pivot, peindre
from betes import quadrupede
from animations import trot
from echelles import hauteur

def fabriquer():
    c = collection('warg'); dans(c)
    r = pivot('warg'); H = hauteur('warg')
    quadrupede(r, dict(poil='#6f747c', poil2='#8a9099', ventre='#b5bcc4', patte='#4a4f57', crete='#2b2f36',
                       yeux='#ff4a3a', oreilles=1, museau='loup', tete=.24, queue='#4a4f57', largeur=.2, pattes=.55,
                       epaisseur=.2), H * .85, H * 1.6)
    peindre(r)
    trot(r, duree=.42, ampl=.7, rebond=H * .05)
    return r

if __name__ == '__main__': fabriquer()

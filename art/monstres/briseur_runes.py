"""Briseur de runes (CR breaker, anti-magie) : orc en armure d'acier, casque, grand bouclier gravé
d'une rune barrée, marteau. Insensible au Givre et au Mage."""
from outils import collection, dans, pivot, peindre, boite
from personnages import humanoide, bouclier, marteau
from animations import marche
from echelles import hauteur

def bouclier_anti_magie(p, H):
    bouclier(p, H, '#b9c0c9', '#6c6e76', '#9ff3ff')
    boite('Barre', '#c0392b', H * .2, H * .03, H * .03, (0, -H * .08, H * .02), 0, p, (0, .8, 0), emis=1)

def fabriquer():
    c = collection('briseur_runes'); dans(c)
    r = pivot('briseur_runes'); H = hauteur('briseur')
    humanoide(r, dict(peau='#4f9a3a', peau2='#63b04a', tissu='#6c6e76', torse='#b9c0c9', cuir='#4a321f', botte='#6c6e76',
                      metal='#b9c0c9', carrure=1.15, tete=.12, jambes=.33, voute=.12, machoire=1, sourcils=1, yeux='#ff5a3c',
                      nez=('rond', .24), defenses=1, oreilles=.3, casque='#b9c0c9', epaulieres='or',
                      arme=lambda p, HH: marteau(p, HH, '#8a8f99'), arme_g=bouclier_anti_magie), H)
    for o in c.objects:
        if o.name.startswith('BrasG'): o.rotation_euler = (-.9, -.2, 0)
    peindre(r)
    marche(r, duree=.8, ampl_jambe=.45, ampl_bras=.2, rebond=H * .04, roulis=.07)
    return r

if __name__ == '__main__': fabriquer()

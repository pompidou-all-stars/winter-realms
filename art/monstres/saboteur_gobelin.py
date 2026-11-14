"""Saboteur gobelin (CR sapper, étourdit les tours) : gobelin en tenue sombre, lunettes, baril de poudre
sur le dos et grosse bombe allumée à la main."""
from outils import collection, dans, pivot, peindre
from personnages import humanoide, bombe
from animations import marche
from echelles import hauteur

def fabriquer():
    c = collection('saboteur_gobelin'); dans(c)
    r = pivot('saboteur_gobelin'); H = hauteur('saboteur')
    humanoide(r, dict(peau='#7cc04a', peau2='#9ad66a', tissu='#4a4a52', torse='#3a3a42', cuir='#2b2b30', botte='#2b2b30',
                      carrure=.95, tete=.17, jambes=.32, voute=.25, sourcils=1, nez=('long', .36), oreilles=.85,
                      lunettes=1, bonnet='#2b2b30', sac='#7a5234', arme=bombe), H)
    peindre(r)
    marche(r, duree=.55, ampl_jambe=.55, ampl_bras=.45, rebond=H * .07, roulis=.06)
    return r

if __name__ == '__main__': fabriquer()

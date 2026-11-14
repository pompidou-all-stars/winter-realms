"""Golem runique (CR golem) : colosse de pierre trapu, petite tête, yeux et runes orange lumineux,
épaules couvertes de mousse. Lent."""
from outils import collection, dans, pivot, peindre
from personnages import humanoide
from animations import marche
from echelles import hauteur

def fabriquer():
    c = collection('golem_runique'); dans(c)
    r = pivot('golem_runique'); H = hauteur('golem')
    humanoide(r, dict(peau='#9a9ca6', peau2='#b4b6bf', tissu='#7d808a', torse='#8a8d97', cuir='#4a7a3a', botte='#6c6e76',
                      carrure=1.5, tete=.09, jambes=.3, voute=.1, nez=('rond', .12), sourcils=1, yeux='#ff9f2e',
                      epaulieres='cuir', runes='#ff9f2e'), H)
    peindre(r)
    marche(r, duree=1.3, ampl_jambe=.35, ampl_bras=.3, rebond=H * .02, roulis=.05)
    return r

if __name__ == '__main__': fabriquer()

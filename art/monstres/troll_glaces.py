"""Troll des glaces (CR troll) : grand troll bleu dégingandé et voûté, long nez, iroquoise, défenses,
pagne de fourrure et gourdin hérissé de glace."""
from outils import collection, dans, pivot, peindre
from personnages import humanoide, gourdin
from animations import marche
from echelles import hauteur

def fabriquer():
    c = collection('troll_glaces'); dans(c)
    r = pivot('troll_glaces'); H = hauteur('troll')
    humanoide(r, dict(peau='#4fa3b0', peau2='#74c4cf', tissu='#e8f0f2', torse='#4fa3b0', cuir='#6b4a2f', botte='#3f7f81',
                      carrure=.95, tete=.12, jambes=.4, voute=.35, nez=('long', .42), defenses=1, oreilles=.6, sourcils=1,
                      yeux='#ffe45e', cheveux='iroquoise', epaulieres='cuir',
                      arme=lambda p, HH: gourdin(p, HH, '#8a6a4a')), H)
    peindre(r)
    marche(r, duree=.85, ampl_jambe=.5, ampl_bras=.5, rebond=H * .04, roulis=.1)
    return r

if __name__ == '__main__': fabriquer()

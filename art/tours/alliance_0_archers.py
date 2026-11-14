"""Alliance, emplacement 0 : Tour des archers (Archer, tir rapide).
Tour de pierre taillée à base talutée, mâchicoulis, chemin de ronde crénelé, toit en flèche bleu
et or porté par quatre poteaux, écusson au soleil d'or, bannière. Un archer en tabard bleu se tient
sous le toit ; la pièce « Tourelle » pivote vers la cible en jeu."""
import math
import outils
from outils import collection, dans, pivot, cylindre, boite, sphere, cone, prisme, anneau, peindre
from factions import PAL, socle_alliance
from personnages import humanoide

def arc(p, H):
    pts = []
    for i in range(9):
        a = -1.15 + 2.3 * i / 8; pts.append((-math.cos(a) * H * .42 + H * .3, math.sin(a) * H * .42))
    for i in range(8, -1, -1):
        a = -1.15 + 2.3 * i / 8; pts.append((-math.cos(a) * H * .37 + H * .3, math.sin(a) * H * .38))
    prisme('Bois', '#6b4423', pts, H * .04, (0, -H * .05, 0), p, (0, 0, math.pi / 2))
    boite('Corde', '#f4efe0', H * .01, H * .01, H * .76, (0, -H * .03, 0), 0, p)

def fabriquer():
    c = collection('alliance_0'); dans(c)
    p = PAL['alliance']
    r = pivot('alliance_0')
    z = socle_alliance(r)
    # fût : base talutée en blocs, corps légèrement effilé, bandeau sculpté
    cylindre('Talus', p['moyen'], .27, .22, .14, 10, (0, 0, z), r, biseau=.02)
    for q in range(8):
        a = q * 2 * math.pi / 8
        boite(f'Bloc{q}', p['pierre'], .1, .07, .07, (math.cos(a) * .245, math.sin(a) * .245, z + .04), 0, r, (0, 0, a + math.pi / 2))
    cylindre('Fut', p['pierre'], .21, .18, .34, 10, (0, 0, z + .12), r, biseau=.01)
    anneau('Bandeau', p['moyen'], .195, .018, 16, 4, (0, 0, z + .26), r)
    # fenêtre en arc (renfoncement sombre, encadrement doré), porte cloutée
    boite('Fenetre', '#1d2333', .06, .03, .1, (0, -.185, z + .34), .02, r)
    anneau('CadreFen', p['or_'], .036, .007, 12, 4, (0, -.19, z + .37), r, (math.pi / 2, 0, 0), metal=.7, rough=.3)
    boite('Porte', '#5a3a1c', .13, .04, .17, (0, -.215, z + .085), .03, r)
    for s in (-1, 1): sphere(f'Gond{s}', '#2b2b30', .012, (s * .04, -.237, z + .1), (1, .6, 1), 6, 4, r, metal=.6)
    # écusson : soleil d'or sur fond bleu
    prisme('Ecu', p['accent'], [(-.07, .06), (.07, .06), (.07, -.02), (0, -.09), (-.07, -.02)], .02, (0, -.2, z + .22), r)
    prisme('BordEcu', p['or_'], [(-.08, .07), (.08, .07), (.08, -.025), (0, -.105), (-.08, -.025)], .012, (0, -.19, z + .22), r, metal=.6)
    sphere('Soleil', p['or_'], .028, (0, -.212, z + .235), (1, .5, 1), 8, 4, r, metal=.6, rough=.3)
    # mâchicoulis (consoles) et chemin de ronde crénelé
    zt = z + .46
    for q in range(8):
        a = q * 2 * math.pi / 8
        boite(f'Console{q}', p['moyen'], .06, .07, .07, (math.cos(a) * .2, math.sin(a) * .2, zt - .05), 0, r, (0, 0, a + math.pi / 2))
    cylindre('Ronde', p['pierre'], .25, .25, .05, 10, (0, 0, zt), r, biseau=.012)
    for q in range(8):
        a = q * 2 * math.pi / 8 + math.pi / 8
        boite(f'Merlon{q}', p['pierre'], .075, .05, .07, (math.cos(a) * .225, math.sin(a) * .225, zt + .085), 0, r, (0, 0, a + math.pi / 2))
    # toit en flèche sur quatre poteaux
    for q in range(4):
        a = q * math.pi / 2 + math.pi / 4
        cylindre(f'Poteau{q}', '#6b4423', .016, .016, .24, 6, (math.cos(a) * .17, math.sin(a) * .17, zt + .05), r)
    zr = zt + .28
    cylindre('Avancee', p['toit'], .29, .25, .04, 10, (0, 0, zr), r, biseau=.008)
    cone('Fleche', p['toit'], .25, .32, 10, (0, 0, zr + .04), r)
    anneau('LisereToit', p['or_'], .27, .014, 16, 4, (0, 0, zr + .02), r, metal=.7, rough=.3)
    sphere('Pommeau', p['or_'], .035, (0, 0, zr + .38), (1, 1, 1.2), 8, 6, r, metal=.7, rough=.3)
    cylindre('Hampe', p['or_'], .008, .008, .14, 6, (0, 0, zr + .4), r, metal=.7)
    prisme('Banniere', p['accent'], [(0, 0), (.15, -.015), (.12, -.045), (.15, -.075), (0, -.08)], .01, (0, 0, zr + .53), r)
    # archer (pivote vers la cible)
    tour = pivot('Tourelle', (0, 0, zt + .05), r)
    H = .26
    outils.SIMPLE = True
    humanoide(tour, dict(peau='#f0c9a0', peau2='#e5a988', tissu='#5a4a3a', torse='#2f5fa8', accent='#2f5fa8', cuir='#6b4423',
                          botte='#4a321f', metal='#c9ced6', carrure=.9, tete=.14, jambes=.36, nez=('rond', .3),
                          sourcils=0, casque='#c9ced6', epaulieres='or', arme_g=arc), H)
    outils.SIMPLE = False
    # pose : bras gauche tendu vers l'avant avec l'arc, bras droit tirant la corde
    for o in c.objects:
        if o.name.startswith('BrasG'): o.rotation_euler = (-1.45, 0, .2)
        if o.name.startswith('BrasD'): o.rotation_euler = (-1.2, 0, -.6)
    peindre(r, sol=.7)
    return r

if __name__ == '__main__': fabriquer()

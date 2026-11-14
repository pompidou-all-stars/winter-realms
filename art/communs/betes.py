"""Bêtes : quadrupèdes (warg, tortue), volants (chauve-souris, griffon, dragon) et gelées.

Pièces nommées utilisées par les animations :
  Corps, Tete, Queue, JambeAG / JambeAD / JambePG / JambePD (avant/arrière, gauche/droite),
  AileG / AileD (battent autour de l'axe Y). Les bêtes regardent vers -Y, pieds en z = 0."""
import math
from outils import pivot, cylindre, boite, sphere, cone, prisme, anneau

def yeux_bete(T, r, y, z, ecart, col, pupille=True):
    for s in (-1, 1):
        sphere(f'Oeil{"GD"[s > 0]}', col, r, (s * ecart, y, z), (1, .6, 1), 8, 6, T, emis=.8 if col != '#ffffff' else 0)
        if pupille: sphere(f'Pupille{"GD"[s > 0]}', '#1b1b1b', r * .5, (s * ecart, y - r * .5, z), (.6, .5, 1), 6, 4, T)

def quadrupede(racine, o, H, L):
    """H : hauteur au garrot ; L : longueur du corps."""
    hz = H * o.get('pattes', .5)
    corps = pivot('Corps', (0, 0, hz), racine)
    w = L * o.get('largeur', .32)
    sphere('Tronc', o['poil'], 1, (0, L * .08, H * .1), (w, L * .52, H * o.get('epaisseur', .24)), 12, 8, corps)
    sphere('Poitrail', o.get('poil2', o['poil']), 1, (0, -L * .28, H * .16), (w * 1.1, L * .28, H * o.get('epaisseur', .24) * 1.15), 12, 8, corps)
    if o.get('ventre'): sphere('Ventre', o['ventre'], 1, (0, -L * .05, -H * .02), (w * .75, L * .4, H * .18), 10, 6, corps)
    if o.get('crete'):
        for k in range(5):
            cone(f'Crete{k}', o['crete'], H * .05, H * .14, 4, (0, -L * .3 + k * L * .15, H * .4 - k * H * .03), corps, (.4, 0, 0))
    # pattes
    for nom, x, y in (('JambeAG', -1, -1), ('JambeAD', 1, -1), ('JambePG', -1, 1), ('JambePD', 1, 1)):
        j = pivot(nom, (x * w * .6, y * L * .3, hz), racine)
        cylindre(f'Cuisse{nom}', o['poil'], H * .09, H * .065, hz * .75, 8, (0, 0, -hz * .8), j, lisse=True)
        sphere(f'Patte{nom}', o.get('patte', o['poil']), H * .075, (0, -H * .03, -hz + H * .05), (1, 1.3, .7), 8, 4, j)
    # tête
    T = pivot('Tete', (0, -L * .58, hz + H * .3), racine)
    rt = H * o.get('tete', .22)
    sphere('Crane', o.get('poil2', o['poil']), rt, (0, 0, 0), (1, 1.05, .95), 12, 8, T)
    m = o.get('museau', 'loup')
    if m == 'loup':
        cone('Museau', o.get('poil2', o['poil']), rt * .5, rt * 1.4, 8, (0, -rt * .6, -rt * .3), T, (1.5, 0, 0))
        sphere('Truffe', '#1b1b1b', rt * .14, (0, -rt * 1.98, -rt * .3), (1, 1, .8), 6, 4, T)
        for s in (-1, 1): cone(f'Croc{s}', '#fffbe8', rt * .06, rt * .25, 4, (s * rt * .2, -rt * 1.2, -rt * .5), T, (math.pi, 0, 0))
    elif m == 'tortue':
        sphere('Museau', o.get('poil2', o['poil']), rt * .7, (0, -rt * .6, -rt * .1), (1, 1, .8), 10, 6, T)
    if o.get('oreilles'):
        for s in (-1, 1): cone(f'Oreille{"GD"[s > 0]}', o['poil'], rt * .3, rt * .8, 4, (s * rt * .5, rt * .1, rt * .7), T, (0, s * .3, 0))
    yeux_bete(T, rt * .17, -rt * .82, rt * .25, rt * .38, o.get('yeux', '#ffffff'), o.get('yeux', '#ffffff') == '#ffffff')
    # queue
    q = pivot('Queue', (0, L * .55, hz + H * .15), racine); q.rotation_euler = (.25, 0, 0)
    cone('QueueCone', o.get('queue', o['poil']), H * .07, L * o.get('lqueue', .45), 6, (0, 0, 0), q, (-math.pi / 2 + .15, 0, 0))
    return corps

def aile(parent, nom, cote, envergure, col, forme='membrane', bord=None):
    """Aile dans le plan horizontal, attachée au pivot (0,0,0) ; cote = -1 (gauche) ou 1 (droite)."""
    e = envergure
    if forme == 'membrane':
        pts = [(0, .16 * e), (cote * .55 * e, .22 * e), (cote * .5 * e, -.04 * e), (cote * .38 * e, .06 * e),
               (cote * .3 * e, -.14 * e), (cote * .18 * e, -.02 * e), (cote * .08 * e, -.16 * e), (0, -.1 * e)]
    else:  # plumes
        pts = [(0, .1 * e), (cote * .3 * e, .14 * e), (cote * .58 * e, .06 * e), (cote * .55 * e, -.02 * e), (cote * .45 * e, -.06 * e),
               (cote * .4 * e, -.02 * e), (cote * .3 * e, -.1 * e), (cote * .25 * e, -.05 * e), (cote * .15 * e, -.12 * e), (0, -.06 * e)]
    if cote > 0: pts = list(reversed(pts))
    prisme(f'Voile{nom}', col, pts, e * .015, (0, 0, 0), parent, (math.pi / 2, 0, 0))
    cylindre(f'Os{nom}', bord or col, e * .012, e * .006, e * .55, 5, (0, -.12 * e, 0), parent, rot=(0, cote * math.pi / 2, -cote * .15))

def volant(racine, o, taille, envergure):
    """Corps volant à VOL au-dessus du sol (la hauteur de vol est ajoutée par le jeu : modèle centré à z = 0)."""
    corps = pivot('Corps', (0, 0, 0), racine)
    for s, n in ((-1, 'AileG'), (1, 'AileD')):
        a = pivot(n, (s * taille * .2, 0, taille * .1), corps)
        aile(a, n, s, envergure, o['aile'], o.get('forme', 'membrane'), o.get('os'))
    return corps

def gelee(racine, H, col='#b5e04a', col2='#d6f27a'):
    corps = pivot('Corps', (0, 0, 0), racine)
    sphere('Gelee', col, H * .55, (0, 0, H * .42), (1.15, 1.1, .85), 14, 9, corps, rough=.2)
    sphere('Dessus', col2, H * .35, (-H * .1, -H * .05, H * .7), (1, 1, .55), 10, 6, corps, rough=.2)
    sphere('Reflet', '#ffffff', H * .08, (-H * .2, -H * .38, H * .65), (1, .4, 1.4), 6, 4, corps, emis=1)
    for k, (x, z) in enumerate(((.18, .3), (-.2, .2), (.05, .15))):
        sphere(f'Bulle{k}', col2, H * .06, (x * H, -H * .35, z * H), (1, .5, 1), 6, 4, corps)
    yeux_bete(corps, H * .09, -H * .55, H * .5, H * .17, '#ffffff')
    boite('Bouche', '#3a5a1a', H * .2, H * .03, H * .04, (0, -H * .6, H * .3), H * .015, corps)
    return corps

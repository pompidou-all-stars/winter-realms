"""Portail d'apparition, château de sortie et plateau-diorama de référence.

Le portail et le château sont exportés en GLB. Le plateau est reconstruit en code dans le jeu
(aux couleurs de chaque faction) ; la version Blender sert de référence de style pour les rendus."""
import math
from outils import collection, dans, pivot, cylindre, boite, sphere, cone, prisme, peindre, anneau
from factions import SOL, BIOME

def portail():
    c = collection('portail'); dans(c)
    r = pivot('portail')
    cylindre('Fosse', '#2a1440', .44, .44, .03, 24, (0, 0, 0), r)
    for i, (col, rr) in enumerate((('#5b2a86', .38), ('#9b59d0', .27), ('#e0b3ff', .16))):
        a = pivot(f'Anneau{i + 1}', (0, 0, .035 + i * .01), r)
        # arc de cercle ouvert (≈ 250°), comme dans la 2D
        pts = []
        for k in range(15):
            t = k / 14 * 4.4; pts.append((math.cos(t) * rr, math.sin(t) * rr))
        for k in range(14, -1, -1):
            t = k / 14 * 4.4; pts.append((math.cos(t) * (rr - .06), math.sin(t) * (rr - .06)))
        o = prisme(f'Arc{i + 1}', col, pts, .02, (0, 0, 0), a, (math.pi / 2, 0, 0), emis=1.5)
    # arche de pierre sombre au-dessus de la fosse
    for s in (-1, 1):
        cylindre(f'Pilier{"GD"[s > 0]}', '#4a3b5e', .07, .06, .5, 8, (s * .4, .05, 0), r)
        sphere(f'Cristal{"GD"[s > 0]}', '#c79bff', .06, (s * .4, .05, .54), (1, 1, 1.6), 6, 4, r, emis=2)
    peindre(r, sol=.8)
    return r

def chateau():
    c = collection('chateau'); dans(c)
    r = pivot('chateau')
    pierre, sombre, toit, or_ = '#ece4cf', '#a9b4c2', '#2b56a0', '#e3b44a'
    boite('Base', sombre, .74, .56, .08, (0, .02, .04), .02, r)
    boite('Donjon', pierre, .62, .46, .4, (0, .02, .28), .025, r)
    boite('Corniche', sombre, .68, .52, .04, (0, .02, .49), .012, r)
    for q, x in enumerate((-.25, -.08, .08, .25)):
        boite(f'Merlon{q}', pierre, .1, .06, .08, (x, -.21, .55), .012, r)
    # tour maîtresse au centre, toit en flèche
    cylindre('Maitresse', pierre, .15, .14, .42, 10, (0, .1, .48), r, biseau=.01)
    cylindre('AvanceeM', toit, .19, .17, .03, 10, (0, .1, .9), r)
    cone('FlecheM', toit, .17, .34, 10, (0, .1, .93), r)
    anneau('LisereM', or_, .18, .012, 14, 3, (0, .1, .91), r, metal=.7, rough=.3)
    for s in (-1, 1):
        n = "GD"[s > 0]
        cylindre(f'Tourelle{n}', pierre, .12, .11, .56, 10, (s * .33, -.12, 0), r, biseau=.01)
        cylindre(f'Avancee{n}', toit, .15, .14, .03, 10, (s * .33, -.12, .56), r)
        cone(f'Toit{n}', toit, .14, .26, 10, (s * .33, -.12, .59), r)
        anneau(f'Lisere{n}', or_, .145, .01, 12, 3, (s * .33, -.12, .575), r, metal=.7, rough=.3)
        sphere(f'Pommeau{n}', or_, .022, (s * .33, -.12, .86), (1, 1, 1.2), 6, 4, r, metal=.7)
        boite(f'Etendard{n}', '#2f5fa8', .09, .012, .16, (s * .17, -.215, .36), .004, r)
        boite(f'BordEt{n}', or_, .1, .008, .02, (s * .17, -.222, .44), 0, r, metal=.6)
    # porte en arc, herse dorée
    boite('Porte', '#4a2f17', .17, .04, .22, (0, -.215, .19), .03, r)
    anneau('Arche', sombre, .09, .02, 10, 3, (0, -.225, .27), r, (math.pi / 2, 0, 0))
    for q in (-1, 0, 1): boite(f'Barreau{q}', or_, .012, .01, .18, (q * .05, -.24, .18), 0, r, metal=.6)
    cylindre('Mat', '#3c2a1a', .01, .01, .26, 6, (0, .1, 1.25), r)
    # le drapeau prend la couleur du joueur en jeu (matériau « Drapeau »)
    d = prisme('Drapeau', '#ffd166', [(0, 0), (.2, -.035), (0, -.1)], .012, (0, .1, 1.5), r)
    d.data.materials[0].name = 'Drapeau'
    peindre(r, sol=.7)
    return r

def plateau(cols, rows, faction='alliance', x0=0, y0=0):
    """Plateau-diorama : socle arrondi et dalles surélevées en damier (référence pour three.js).
    La case (x, y) du jeu est centrée en (x + .5, -(y + .5)) dans Blender."""
    c = collection('plateau'); dans(c)
    r = pivot('plateau')
    sol, bio = SOL[faction], BIOME[faction]
    boite('Terre', bio['terre'], cols + .1, rows + .1, .3, (cols / 2, -rows / 2, -.2), .06, r)
    boite('Falaise', bio['bord'], cols + .3, rows + .3, .35, (cols / 2, -rows / 2, -.45), .1, r)
    for y in range(rows):
        for x in range(cols):
            boite(f'Dalle{x}_{y}', sol[(x + y + x0 + y0) % 2], .97, .97, .08, (x + .5, -(y + .5), -.04), .03, r)
            seed = ((x + x0) * 92821 + (y + y0) * 68917) % 997
            fx, fy = x + .25 + (seed % 50) / 100, -(y + .25 + ((seed * 7) % 50) / 100)
            if seed % 11 == 0:
                sphere(f'Caillou{x}_{y}', '#b8b2a2', .07, (fx, fy, .0), (1.2, 1, .6), 6, 4, r)
            elif seed % 7 == 0:
                for q in (-1, 0, 1):
                    cone(f'Herbe{x}_{y}{q}', bio['detail'], .02, .1, 4, (fx + q * .04, fy, 0), r, (0, q * .4, 0))
            elif seed % 5 == 0:
                for q in range(3):
                    sphere(f'Fleur{x}_{y}{q}', bio['fleur'] if q else '#ffffff', .018, (fx + q * .05, fy + (q % 2) * .04, .02), (1, 1, .7), 6, 4, r)
    peindre(r, sol=.75, local=.05, bruit=.1)
    return r

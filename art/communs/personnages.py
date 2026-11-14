"""Personnage réutilisable, style heroic fantasy cartoon : silhouette trapue et lisible, épaulières,
brassards, pagne, détails sculptés ; tête un peu grosse et nez marqué, sans excès.

Hiérarchie produite (noms utilisés par les animations et par le jeu) :
  <racine> ─ Corps (pivot aux hanches) ─ Tete, BrasG, BrasD (→ Arme)
           ├ JambeG, JambeD
Le personnage regarde vers -Y, pieds en z = 0. H = hauteur totale (cases).

Options (dict o) : peau, peau2 (nez, mâchoire), tissu, cuir, metal, botte, accent,
  carrure (largeur), tete (rayon / H), jambes (hauteur des hanches / H), voute (dos voûté, rad),
  oreilles (longueur), nez ('rond' | 'long' | 'crochu', taille), defenses, sourcils, yeux (couleur),
  cheveux ('chignon' | 'iroquoise' | None), casque, cornes, epaulieres ('pointes' | 'or' | 'cuir' | None),
  lunettes, bonnet, arme (fonction).
"""
import math
from outils import cylindre, boite, sphere, cone, prisme, pivot, anneau

def humanoide(racine, o, H):
    cr = o.get('carrure', 1.0)
    hz = H * o.get('jambes', .36)
    rh = H * o.get('tete', .12)
    # ---------- jambes ----------
    for s, n in ((-1, 'G'), (1, 'D')):
        j = pivot(f'Jambe{n}', (s * H * .075 * cr, 0, hz), racine)
        cylindre(f'Cuisse{n}', o['tissu'], H * .055 * cr, H * .05, hz * .55, 8, (0, 0, -hz * .55), j, lisse=True)
        cylindre(f'Tibia{n}', o['botte'], H * .05, H * .06, hz * .4, 8, (0, 0, -hz * .92), j, biseau=H * .008)
        boite(f'Pied{n}', o['botte'], H * .1, H * .15, H * .07, (0, -H * .03, -hz + H * .035), H * .022, j)
        cylindre(f'Revers{n}', o.get('cuir', o['botte']), H * .066, H * .066, H * .03, 8, (0, 0, -hz * .55), j, biseau=H * .006)
    corps = pivot('Corps', (0, 0, hz), racine)
    buste = pivot('Buste', (0, 0, 0), corps); buste.rotation_euler = (o.get('voute', 0), 0, 0)
    # ---------- bassin, pagne, ceinture ----------
    tw, cw = H * .13 * cr, H * .19 * cr
    cylindre('Pagne', o['tissu'], tw * 1.25, tw * .95, H * .16, 10, (0, 0, -H * .12), buste, biseau=H * .01)
    if o.get('accent'):
        boite('Tabard', o['accent'], tw * .9, H * .02, H * .2, (0, -tw * .95, -H * .1), H * .006, buste)
    anneau('Ceinture', o.get('cuir', '#4a321f'), tw * 1.0, H * .018, 14, 5, (0, 0, H * .03), buste, echelle=(1, .82, 1.2))
    boite('Boucle', '#f2c14e', H * .05, H * .02, H * .04, (0, -tw * .85, H * .03), H * .006, buste, metal=.7, rough=.3)
    # ---------- torse ----------
    cylindre('Ventre', o['tissu'], tw, cw * .95, H * .2, 12, (0, 0, H * .03), buste, lisse=True).scale = (1, .8, 1)
    sphere('Poitrine', o.get('torse', o['tissu']), cw, (0, 0, H * .22), (.92, .66, .5), 14, 8, buste)
    if o.get('harnais'):
        boite('Harnais', o.get('cuir', '#4a321f'), H * .05, cw * 1.5, H * .36, (0, 0, H * .17), H * .005, buste, (.0, .62, 0)).scale = (1, 1, 1)
        sphere('Rivet', '#c9ced6', H * .02, (0, -cw * .68, H * .2), (1, .6, 1), 6, 4, buste, metal=.6)
    zs = H * .29
    # ---------- tête ----------
    tete = pivot('Tete', (0, -H * .02, zs + H * .03), buste); tete.rotation_euler = (-o.get('voute', 0) * .8, 0, 0)
    cylindre('Cou', o['peau'], rh * .45, rh * .5, rh * .5, 8, (0, 0, -rh * .1), tete)
    T = pivot('Crane', (0, 0, rh * .95), tete)
    sphere('Visage', o['peau'], rh, (0, 0, 0), (.95, .95, 1), 16, 10, T)
    p2 = o.get('peau2', o['peau'])
    if o.get('machoire'):
        sphere('Machoire', p2, rh * .8, (0, -rh * .3, -rh * .45), (1.05, .85, .6), 12, 8, T)
    if o.get('sourcils'):
        boite('Arcade', p2, rh * 1.25, rh * .35, rh * .22, (0, -rh * .78, rh * .2), rh * .08, T, (-.25, 0, 0))
    yc = o.get('yeux', '#ffffff')
    for s, n in ((-1, 'G'), (1, 'D')):
        sphere(f'Oeil{n}', yc, rh * .16, (s * rh * .34, -rh * .86, rh * .02), (1, .55, .8), 8, 6, T, emis=.4 if yc != '#ffffff' else 0)
        if yc == '#ffffff': sphere(f'Pupille{n}', '#1b1b1b', rh * .08, (s * rh * .34, -rh * .95, rh * .0), (1, .5, 1), 6, 4, T)
    nz = o.get('nez', ('rond', .3))
    if nz[0] == 'long': cone('Nez', p2, rh * nz[1] * .55, rh * nz[1] * 2.6, 8, (0, -rh * .9, -rh * .12), T, (-1.35, 0, 0))
    elif nz[0] == 'crochu':
        sphere('Nez', p2, rh * nz[1], (0, -rh * 1.0, -rh * .1), (.8, 1.1, 1.05), 10, 6, T)
    else: sphere('Nez', p2, rh * nz[1], (0, -rh * .98, -rh * .12), (1.05, .9, .85), 10, 6, T)
    if o.get('defenses'):
        for s in (-1, 1): cone(f'Defense{"GD"[s > 0]}', '#fff6dc', rh * .1, rh * .45, 6, (s * rh * .42, -rh * .85, -rh * .55), T, (.25, -s * .15, 0))
    if o.get('oreilles'):
        e = o['oreilles']
        for s in (-1, 1):
            prisme(f'Oreille{"GD"[s > 0]}', o['peau'], [(0, -rh * .25), (s * rh * (.4 + e), rh * (.25 + e * .25)), (0, rh * .3)], rh * .1,
                   (s * rh * .85, rh * .05, rh * .05), T, (0, 0, -s * .25))
    ch = o.get('cheveux')
    if ch == 'chignon':
        sphere('Chignon', '#1d1a17', rh * .32, (0, rh * .35, rh * .95), (1, 1, 1.2), 8, 6, T)
        anneau('Lien', '#c9a24a', rh * .17, rh * .05, 10, 4, (0, rh * .35, rh * .75), T)
    elif ch == 'iroquoise':
        for i in range(4): cone(f'Meche{i}', '#1d1a17', rh * .16, rh * .5, 4, (0, -rh * .3 + i * rh * .3, rh * .82), T, (.3 - i * .25, 0, 0))
    if o.get('casque'):
        c = o['casque']
        sphere('Casque', c, rh * 1.04, (0, rh * .05, rh * .28), (1, 1.02, .78), 16, 7, T, metal=.6, rough=.35)
        anneau('BordCasque', c, rh * 1.0, rh * .07, 16, 4, (0, rh * .05, rh * .1), T, metal=.6, rough=.35)
        boite('Nasal', c, rh * .12, rh * .1, rh * .55, (0, -rh * 1.0, rh * .08), rh * .03, T, metal=.6, rough=.35)
        if o.get('cornes'):
            for s in (-1, 1): cone(f'Corne{"GD"[s > 0]}', '#efe6cc', rh * .16, rh * .75, 6, (s * rh * .9, 0, rh * .55), T, (0, s * 1.0, 0))
    if o.get('bonnet'):
        cone('Bonnet', o['bonnet'], rh * .9, rh * 1.4, 10, (0, rh * .15, rh * .45), T, (.5, 0, 0))
        anneau('BordBonnet', o.get('cuir', '#4a321f'), rh * .88, rh * .08, 12, 4, (0, rh * .05, rh * .48), T, rot=(.45, 0, 0))
    if o.get('lunettes'):
        for s in (-1, 1): anneau(f'Lunette{"GD"[s > 0]}', '#b98a3a', rh * .2, rh * .06, 10, 4, (s * rh * .3, -rh * .88, rh * .42), T, (1.35, 0, 0), metal=.6)
        boite('Sangle', '#3c2a1a', rh * 2.0, rh * .2, rh * .1, (0, 0, rh * .42), 0, T)
    # ---------- épaules et bras ----------
    ep = o.get('epaulieres')
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * cw * .95, 0, zs - H * .01), buste); b.rotation_euler = (0, s * .18, 0)
        if ep:
            col = o.get('metal', '#8a929c') if ep != 'cuir' else o.get('cuir', '#6b4a2f')
            sphere(f'Epauliere{n}', col, H * .085 * cr, (s * H * .015, 0, H * .02), (1.1, 1, .75), 10, 6, b, metal=.5 if ep != 'cuir' else 0, rough=.4)
            if ep == 'pointes':
                for k in (-1, 0, 1): cone(f'Pointe{n}{k}', '#e8e2cf', H * .016, H * .07, 5, (s * H * .05, k * H * .04, H * .07), b, (k * .3, s * .5, 0))
            elif ep == 'or':
                anneau(f'LisereEp{n}', '#e0b44e', H * .08 * cr, H * .01, 12, 4, (s * H * .015, 0, -H * .005), b, metal=.7, rough=.3)
        cylindre(f'BrasHaut{n}', o['peau'], H * .045 * cr, H * .04 * cr, H * .14, 8, (0, 0, -H * .14), b, lisse=True)
        cylindre(f'Brassard{n}', o.get('cuir', '#6b4a2f'), H * .045 * cr, H * .052 * cr, H * .1, 8, (0, 0, -H * .25), b, biseau=H * .006)
        sphere(f'Poing{n}', o['peau'], H * .05 * cr, (0, 0, -H * .27), (1, 1, 1), 8, 6, b)
        if n == 'D' and o.get('arme'):
            a = pivot('Arme', (0, -H * .01, -H * .27), b); o['arme'](a, H)
        if n == 'G' and o.get('arme_g'):
            a = pivot('ArmeG', (0, -H * .01, -H * .27), b); o['arme_g'](a, H)
    return corps

# ---------- armes ----------
def hache(p, H):
    cylindre('Manche', '#6b4423', H * .018, H * .018, H * .52, 6, (0, 0, -H * .14), p)
    anneau('Bague', '#c9a24a', H * .02, H * .008, 8, 4, (0, 0, H * .22), p, metal=.7)
    lame = [(0, 0)]
    for i in range(9):
        a = -1.0 + 2.0 * i / 8; lame.append((H * (.1 + .12 * math.cos(a)), H * .1 * math.sin(a) * 1.5))
    lame.append((0, H * .06))
    prisme('Lame', '#cfd6df', [(x, z + H * .27) for x, z in lame], H * .03, (0, 0, 0), p, metal=.35, rough=.45)
    prisme('Talon', '#8a929c', [(0, H * .25), (-H * .07, H * .29), (0, H * .33)], H * .02, (0, 0, 0), p, metal=.6)

def bombe(p, H):
    sphere('Bombe', '#2b2b30', H * .09, (0, -H * .05, H * .05), (1, 1, 1), 10, 8, p, rough=.4)
    cylindre('Meche', '#c9a24a', H * .012, H * .012, H * .05, 6, (0, -H * .05, H * .13), p)
    sphere('Etincelle', '#ffd34d', H * .022, (0, -H * .05, H * .19), (1, 1, 1), 6, 4, p, emis=4)

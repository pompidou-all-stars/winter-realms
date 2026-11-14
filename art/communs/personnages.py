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
from .outils import cylindre, boite, sphere, cone, prisme, pivot, anneau

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
    if o.get('robe'):
        # longue robe jusqu'aux pieds (mages, prêtresses) : les jambes restent dessous
        cylindre('Robe', o['robe'], tw * 1.9, tw * 1.0, hz + H * .02, 12, (0, 0, -hz + H * .01), buste, biseau=H * .01)
        if o.get('accent'): boite('Bande', o['accent'], tw * .5, H * .02, hz * .95, (0, -tw * 1.38, -hz * .45), 0, buste, (-.2, 0, 0))
    cylindre('Pagne', o['tissu'], tw * 1.25, tw * .95, H * .16, 10, (0, 0, -H * .12), buste, biseau=H * .01)
    if o.get('cape'):
        prisme('Cape', o['cape'], [(-cw * .9, H * .28), (cw * .9, H * .28), (cw * 1.3, -hz * .85), (0, -hz * .75), (-cw * 1.3, -hz * .85)],
               H * .02, (0, cw * .72, 0), buste, (.12, 0, 0))
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
    if o.get('runes'):
        for k, (x, z) in enumerate(((-.35, .2), (.35, .2), (0, .05))):
            sphere(f'RuneCorps{k}', o['runes'], H * .025, (x * cw, -cw * .62, H * z + H * .05), (1, .4, 1), 6, 4, buste, emis=3)
    if o.get('sac'):
        cylindre('Sac', o['sac'], H * .09, H * .09, H * .2, 8, (0, cw * .85, H * .02), buste, biseau=H * .01)
        anneau('CercleSac', '#3a3330', H * .092, H * .008, 8, 3, (0, cw * .85, H * .12), buste)
        cylindre('MecheSac', '#c9a24a', H * .01, H * .01, H * .06, 5, (0, cw * .85, H * .22), buste)
    # ---------- tête ----------
    tete = pivot('Tete', (0, -H * .02, zs + H * .03), buste); tete.rotation_euler = (-o.get('voute', 0) * .8, 0, 0)
    cylindre('Cou', o['peau'], rh * .45, rh * .5, rh * .5, 8, (0, 0, -rh * .1), tete)
    T = pivot('Crane', (0, 0, rh * .95), tete)
    sphere('Visage', o['peau'], rh, (0, 0, 0), (.95, .95, 1), 14, 8, T)
    p2 = o.get('peau2', o['peau'])
    if o.get('machoire'):
        sphere('Machoire', p2, rh * .8, (0, -rh * .3, -rh * .45), (1.05, .85, .6), 12, 8, T)
    if o.get('sourcils'):
        boite('Arcade', p2, rh * 1.25, rh * .35, rh * .22, (0, -rh * .78, rh * .2), rh * .08, T, (-.25, 0, 0))
    yc = o.get('yeux', '#ffffff')
    if o.get('un_oeil'):
        sphere('Oeil', '#ffffff', rh * .34, (0, -rh * .78, rh * .12), (1, .55, .9), 12, 8, T)
        sphere('Iris', yc if yc != '#ffffff' else '#5a3a1c', rh * .17, (0, -rh * .97, rh * .1), (1, .5, 1), 10, 6, T)
        boite('ArcadeUnique', p2, rh * 1.0, rh * .3, rh * .2, (0, -rh * .8, rh * .5), rh * .08, T, (-.3, 0, 0))
    for s, n in (() if o.get('un_oeil') else ((-1, 'G'), (1, 'D'))):
        sphere(f'Oeil{n}', yc, rh * .16, (s * rh * .34, -rh * .86, rh * .02), (1, .55, .8), 8, 6, T, emis=.4 if yc != '#ffffff' else 0)
        if yc == '#ffffff': sphere(f'Pupille{n}', '#1b1b1b', rh * .08, (s * rh * .34, -rh * .95, rh * .0), (1, .5, 1), 6, 4, T)
    nz = o.get('nez', ('rond', .3))
    if nz[0] == 'long': cone('Nez', p2, rh * nz[1] * .55, rh * nz[1] * 2.6, 8, (0, -rh * .9, -rh * .12), T, (1.75, 0, 0))
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
        sphere('Casque', c, rh * 1.04, (0, rh * .05, rh * .28), (1, 1.02, .78), 14, 6, T, metal=.6, rough=.35)
        anneau('BordCasque', c, rh * 1.0, rh * .07, 12, 3, (0, rh * .05, rh * .1), T, metal=.6, rough=.35)
        boite('Nasal', c, rh * .12, rh * .1, rh * .55, (0, -rh * 1.0, rh * .08), rh * .03, T, metal=.6, rough=.35)
        if o.get('cornes'):
            for s in (-1, 1): cone(f'Corne{"GD"[s > 0]}', '#efe6cc', rh * .16, rh * .75, 6, (s * rh * .9, 0, rh * .55), T, (0, s * 1.0, 0))
    if o.get('corne'):
        cone('CorneFront', o['corne'], rh * .2, rh * .6, 6, (0, -rh * .2, rh * .85), T, (-.4, 0, 0))
    if o.get('plumes'):
        for k, col in enumerate(o['plumes']):
            prisme(f'Plume{k}', col, [(-rh * .1, 0), (0, rh * 1.0), (rh * .1, 0)], rh * .04, ((k - 1) * rh * .3, rh * .3, rh * .7), T, (-.4, (k - 1) * .4, 0))
    if o.get('barbe'):
        b = o['barbe']
        cone('Barbe', b, rh * .75, rh * 1.3, 8, (0, -rh * .45, -rh * .25), T, (math.pi - .35, 0, 0))
        sphere('Moustache', b, rh * .35, (0, -rh * .92, -rh * .22), (1.6, .6, .5), 8, 4, T)
    if o.get('capuche'):
        # capuche ouverte devant : posée en arrière du crâne, le visage reste visible
        sphere('Capuche', o['capuche'], rh * 1.1, (0, rh * .38, rh * .22), (1.05, .9, 1.02), 12, 7, T)
        cone('PointeCapuche', o['capuche'], rh * .45, rh * .8, 6, (0, rh * .95, rh * .55), T, (-1.1, 0, 0))
    if o.get('couronne'):
        c = o['couronne']; anneau('Couronne', c, rh * .78, rh * .08, 12, 3, (0, 0, rh * .78), T, metal=.7, rough=.3)
        for k in range(5):
            a = k * 2 * math.pi / 5 - math.pi / 2
            cone(f'Fleuron{k}', c, rh * .1, rh * .35, 4, (math.cos(a) * rh * .78, math.sin(a) * rh * .78, rh * .8), T, metal=.7, rough=.3)
    if o.get('chapeau'):
        c = o['chapeau']; cylindre('Bord', c, rh * 1.5, rh * 1.5, rh * .08, 12, (0, 0, rh * .6), T)
        cone('Pointe', c, rh * .85, rh * 1.6, 10, (0, 0, rh * .66), T, (-.25, 0, 0))
    if o.get('bonnet'):
        cone('Bonnet', o['bonnet'], rh * .9, rh * 1.4, 10, (0, rh * .15, rh * .45), T, (-.5, 0, 0))
        anneau('BordBonnet', o.get('cuir', '#4a321f'), rh * .88, rh * .08, 12, 4, (0, rh * .05, rh * .48), T, rot=(-.45, 0, 0))
    if o.get('lunettes'):
        for s in (-1, 1): anneau(f'Lunette{"GD"[s > 0]}', '#b98a3a', rh * .2, rh * .06, 10, 4, (s * rh * .3, -rh * .88, rh * .42), T, (1.35, 0, 0), metal=.6)
        boite('Sangle', '#3c2a1a', rh * 2.0, rh * .2, rh * .1, (0, 0, rh * .42), 0, T)
    # ---------- épaules et bras ----------
    ep = o.get('epaulieres')
    for s, n in ((-1, 'G'), (1, 'D')):
        b = pivot(f'Bras{n}', (s * cw * .95, 0, zs - H * .01), buste); b.rotation_euler = (0, s * .18, 0)
        if ep:
            col = o.get('metal', '#8a929c') if ep != 'cuir' else o.get('cuir', '#6b4a2f')
            sphere(f'Epauliere{n}', col, H * .085 * cr ** .5, (s * H * .015, 0, H * .02), (1.1, 1, .75), 10, 6, b, metal=.5 if ep != 'cuir' else 0, rough=.4)
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

def epee(p, H, lame='#dfe5ec', garde='#e3b44a'):
    cylindre('Poignee', '#4a321f', H * .015, H * .015, H * .1, 6, (0, 0, -H * .04), p)
    boite('Garde', garde, H * .14, H * .03, H * .025, (0, 0, H * .065), H * .005, p, metal=.7, rough=.3)
    prisme('Lame', lame, [(-H * .025, 0), (H * .025, 0), (H * .02, H * .36), (0, H * .42), (-H * .02, H * .36)], H * .014,
           (0, 0, H * .075), p, metal=.5, rough=.35)

def marteau(p, H, tete='#8a8f99'):
    cylindre('Manche', '#6b4423', H * .018, H * .018, H * .45, 6, (0, 0, -H * .1), p)
    boite('Masse', tete, H * .18, H * .11, H * .11, (0, 0, H * .36), H * .02, p, metal=.6, rough=.4)
    anneau('Bague', '#e0a34d', H * .025, H * .01, 8, 3, (0, 0, H * .3), p, metal=.7)

def gourdin(p, H, bois='#7a5234'):
    cylindre('Gourdin', bois, H * .025, H * .06, H * .5, 8, (0, 0, -H * .05), p, biseau=H * .01)
    for k in range(3): cone(f'Clou{k}', '#c9ced6', H * .015, H * .05, 4, (0, 0, H * (.25 + k * .07)), p, (0, 1.57, k * 2.1))

def baton(p, H, orbe='#9ff3ff', bois='#5a3a1c'):
    cylindre('Baton', bois, H * .016, H * .02, H * .75, 6, (0, 0, -H * .25), p)
    anneau('Crochet', bois, H * .05, H * .014, 8, 3, (0, 0, H * .53), p, (1.57, 0, 0))
    sphere('OrbeBaton', orbe, H * .045, (0, 0, H * .53), (1, 1, 1), 10, 6, p, emis=3)

def bouclier(p, H, col='#8a929c', bord='#e3b44a', embleme=None):
    prisme('Bouclier', col, [(-H * .14, H * .12), (H * .14, H * .12), (H * .14, -H * .05), (0, -H * .18), (-H * .14, -H * .05)], H * .03,
           (0, -H * .05, 0), p, (0, 0, 0), metal=.4, rough=.45)
    prisme('BordBouclier', bord, [(-H * .155, H * .135), (H * .155, H * .135), (H * .155, -H * .055), (0, -H * .2), (-H * .155, -H * .055)], H * .02,
           (0, -H * .03, 0), p, metal=.7, rough=.3)
    if embleme: sphere('Embleme', embleme, H * .05, (0, -H * .075, H * .02), (1, .5, 1), 8, 4, p, metal=.6, emis=.5)

def lame_courbe(p, H, col='#b9faff'):
    pts = [(0, 0)]
    for i in range(7): a = i / 6; pts.append((H * (.05 + .12 * math.sin(a * 2.4)), H * .45 * a))
    for i in range(6, -1, -1): a = i / 6; pts.append((H * (.0 + .1 * math.sin(a * 2.4)), H * .45 * a))
    prisme('LameCourbe', col, pts, H * .015, (0, 0, H * .02), p, emis=1.2, rough=.3)
    cylindre('Poignee', '#2a1d3a', H * .015, H * .015, H * .1, 6, (0, 0, -H * .08), p)

def baguette(p, H, col='#7ee0a0'):
    cylindre('Baguette', '#6b4423', H * .012, H * .01, H * .25, 6, (0, 0, -H * .02), p)
    sphere('Feuille', col, H * .04, (0, 0, H * .25), (1, .5, 1.5), 8, 4, p, emis=1.5)

def arc_court(p, H):
    pts = []
    for i in range(9):
        a = -1.15 + 2.3 * i / 8; pts.append((-math.cos(a) * H * .42 + H * .3, math.sin(a) * H * .42))
    for i in range(8, -1, -1):
        a = -1.15 + 2.3 * i / 8; pts.append((-math.cos(a) * H * .37 + H * .3, math.sin(a) * H * .38))
    prisme('Arc', '#6b4423', pts, H * .04, (0, -H * .05, 0), p, (0, 0, math.pi / 2))
    boite('Corde', '#f4efe0', H * .01, H * .01, H * .76, (0, -H * .03, 0), 0, p)

def bombe(p, H):
    sphere('Bombe', '#2b2b30', H * .09, (0, -H * .05, H * .05), (1, 1, 1), 10, 8, p, rough=.4)
    cylindre('Meche', '#c9a24a', H * .012, H * .012, H * .05, 6, (0, -H * .05, H * .13), p)
    sphere('Etincelle', '#ffd34d', H * .022, (0, -H * .05, H * .19), (1, 1, 1), 6, 4, p, emis=4)

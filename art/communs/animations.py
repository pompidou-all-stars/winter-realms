"""Animations simples par pièces (pas de squelette) : chaque pièce nommée reçoit des clés de rotation
ou de position. Un clip = une Action Blender, exportée comme animation glTF du même nom."""
import bpy, math

FPS = 24

def _trouver(racine, nom):
    pile = [racine]
    while pile:
        o = pile.pop()
        if o.name.split('.')[0] == nom: return o
        pile += list(o.children)
    return None

def _cles(o, chemin, idx, valeurs, n):
    """valeurs : fonction phase(0..1) → valeur ; n clés réparties sur la boucle, la dernière = la première."""
    base = getattr(o, chemin)[idx]
    for i in range(n + 1):
        ph = i / n
        getattr(o, chemin)[idx] = base + valeurs(ph)
        o.keyframe_insert(chemin, index=idx, frame=1 + ph * n * (FPS / n) * _cles.duree)
    getattr(o, chemin)[idx] = base

def _debut(racine, nom, duree):
    bpy.context.scene.render.fps = FPS
    _cles.duree = duree
    for o in [racine] + list(racine.children_recursive):
        if o.animation_data and o.animation_data.action: o.animation_data_clear()

def _nommer(racine, nom):
    for o in [racine] + list(racine.children_recursive):
        if o.animation_data and o.animation_data.action:
            o.animation_data.action.name = f'{nom}_{o.name}'
            # le nom du clip glTF est celui de la piste NLA
            tr = o.animation_data.nla_tracks.new(); tr.name = nom
            st = tr.strips.new(nom, int(o.animation_data.action.frame_range[0]), o.animation_data.action)
            o.animation_data.action = None

def marche(racine, duree=1.0, ampl_jambe=.5, ampl_bras=.4, rebond=.03, roulis=.06, n=8):
    _debut(racine, 'marche', duree)
    s = lambda ph: math.sin(ph * 2 * math.pi)
    for nom, sg in (('JambeG', 1), ('JambeD', -1)):
        o = _trouver(racine, nom)
        if o: _cles(o, 'rotation_euler', 0, lambda ph, sg=sg: sg * ampl_jambe * s(ph), n)
    for nom, sg in (('BrasG', -1), ('BrasD', 1)):
        o = _trouver(racine, nom)
        if o: _cles(o, 'rotation_euler', 0, lambda ph, sg=sg: sg * ampl_bras * s(ph), n)
    c = _trouver(racine, 'Corps')
    if c:
        _cles(c, 'location', 2, lambda ph: rebond * abs(math.sin(ph * 2 * math.pi)), n)
        _cles(c, 'rotation_euler', 1, lambda ph: roulis * s(ph), n)
    _nommer(racine, 'marche')

def battement(racine, duree=.35, ampl=.9, flottement=.05, n=8):
    _debut(racine, 'vol', duree)
    s = lambda ph: math.sin(ph * 2 * math.pi)
    for nom, sg in (('AileG', -1), ('AileD', 1)):
        o = _trouver(racine, nom)
        if o: _cles(o, 'rotation_euler', 1, lambda ph, sg=sg: sg * ampl * s(ph), n)
    c = _trouver(racine, 'Corps')
    if c: _cles(c, 'location', 2, lambda ph: flottement * math.sin(ph * 2 * math.pi + 1.5), n)
    _nommer(racine, 'vol')

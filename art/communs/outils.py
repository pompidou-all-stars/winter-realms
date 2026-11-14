"""Outils communs aux scripts de modèles 3D de Winter Realms.

Convention : 1 unité Blender = 1 case du terrain. Z vers le haut, le modèle regarde vers -Y
(vers le bas de l'écran en jeu, qui est la direction de la sortie). Origine au pied du modèle.
Les couleurs sont données en hexadécimal sRGB, comme dans index.html, et converties ici.
Chaque pièce animable est un objet nommé (Tete, BrasG, BrasD, JambeG, JambeD, Arme, AileG…).
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix

# ---------- scène ----------
def vider_scene():
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.actions, bpy.data.cameras, bpy.data.lights):
        for d in list(coll):
            if d.users == 0: coll.remove(d)

def collection(nom):
    c = bpy.data.collections.get(nom)
    if c:
        for o in list(c.objects): bpy.data.objects.remove(o, do_unlink=True)
    else:
        c = bpy.data.collections.new(nom); bpy.context.scene.collection.children.link(c)
    return c

# ---------- couleurs et matériaux ----------
def lin(h):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b), 1.0)

def mat(h, rough=0.7, metal=0.0, emis=0.0):
    """Matériau simple, partagé par couleur (aucune texture). La couleur est multipliée par la
    « peinture » des sommets (attribut Col) : c'est elle qui donne le dégradé façon peint à la main."""
    nom = f"c{h.lstrip('#')}" + (f"_e{emis:g}" if emis else "") + (f"_m{metal:g}" if metal else "") + (f"_r{rough:g}" if rough != .7 else "")
    m = bpy.data.materials.get(nom)
    if m: return m
    m = bpy.data.materials.new(nom); m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
    mx.inputs[0].default_value = 1.0
    mx.inputs[6].default_value = lin(h)
    nt.links.new(ca.outputs[0], mx.inputs[7]); nt.links.new(mx.outputs[2], p.inputs['Base Color'])
    p.inputs['Base Color'].default_value = lin(h)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    if emis:
        p.inputs['Emission Color'].default_value = lin(h)
        p.inputs['Emission Strength'].default_value = emis
    m.diffuse_color = lin(h)
    return m

# ---------- création de pièces ----------
_coll = None
def dans(c):
    global _coll; _coll = c

def _obj(nom, me, h, parent=None, **kw):
    o = bpy.data.objects.new(nom, me)
    (_coll or bpy.context.scene.collection).objects.link(o)
    if h: me.materials.append(mat(h, **kw))
    if parent: o.parent = parent
    for p in me.polygons: p.use_smooth = False
    return o

def _bm_to(nom, bm, h, parent=None, **kw):
    me = bpy.data.meshes.new(nom); bm.to_mesh(me); bm.free()
    return _obj(nom, me, h, parent, **kw)

def cylindre(nom, h, r1, r2, haut, seg=12, pos=(0, 0, 0), parent=None, lisse=False, biseau=0.0, rot=(0, 0, 0), **kw):
    if SIMPLE: seg, biseau = min(seg, 6), 0
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=haut)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, haut / 2))
    if biseau:
        ar = [e for e in bm.edges if any(len(f.verts) > 4 for f in e.link_faces)]
        bmesh.ops.bevel(bm, geom=ar, offset=biseau, segments=1, affect='EDGES')
    o = _bm_to(nom, bm, h, parent, **kw); o.location = pos; o.rotation_euler = rot
    if lisse or biseau: lisser(o, 40)
    return o

def anneau(nom, h, r, epais, seg=16, seg2=6, pos=(0, 0, 0), parent=None, rot=(0, 0, 0), echelle=(1, 1, 1), **kw):
    """Tore (liserés, anneaux, bracelets)."""
    seg2 = min(seg2, 3 if epais < .02 else seg2)
    if r < .06 or SIMPLE: seg = min(seg, 8 if SIMPLE else 10)
    if SIMPLE: seg2 = 3
    bm = bmesh.new(); vs = []
    for i in range(seg):
        a = i / seg * 2 * math.pi; ligne = []
        for j in range(seg2):
            b = j / seg2 * 2 * math.pi; rr = r + math.cos(b) * epais
            ligne.append(bm.verts.new((math.cos(a) * rr * echelle[0], math.sin(a) * rr * echelle[1], math.sin(b) * epais * echelle[2])))
        vs.append(ligne)
    for i in range(seg):
        for j in range(seg2):
            a, b = vs[i], vs[(i + 1) % seg]
            bm.faces.new((a[j], b[j], b[(j + 1) % seg2], a[(j + 1) % seg2]))
    o = _bm_to(nom, bm, h, parent, **kw); o.location = pos; o.rotation_euler = rot; lisser(o, 70); return o

def boite(nom, h, sx, sy, sz, pos=(0, 0, 0), biseau=0.0, parent=None, rot=(0, 0, 0), **kw):
    if SIMPLE: biseau = 0
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    if biseau:
        bmesh.ops.bevel(bm, geom=bm.edges[:] + bm.verts[:], offset=biseau, segments=1, affect='EDGES')
    o = _bm_to(nom, bm, h, parent, **kw); o.location = pos; o.rotation_euler = rot
    return o

SIMPLE = False  # vrai pendant la construction d'un petit personnage (archer sur une tour…)

def _lod(taille, seg, anneaux):
    """Moins de facettes pour les petites pièces (budget de triangles des modèles)."""
    if SIMPLE: return min(seg, 8), min(anneaux, 5)
    if taille < .02: return min(seg, 6), min(anneaux, 4)
    if taille < .045: return min(seg, 10), min(anneaux, 6)
    return seg, anneaux

def sphere(nom, h, r, pos=(0, 0, 0), echelle=(1, 1, 1), seg=12, anneaux=8, parent=None, rot=(0, 0, 0), **kw):
    seg, anneaux = _lod(r * max(echelle), seg, anneaux)
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=anneaux, radius=r)
    bmesh.ops.scale(bm, vec=echelle, verts=bm.verts)
    o = _bm_to(nom, bm, h, parent, **kw); o.location = pos; o.rotation_euler = rot
    lisser(o); return o

def cone(nom, h, r, haut, seg=8, pos=(0, 0, 0), parent=None, rot=(0, 0, 0), **kw):
    o = cylindre(nom, h, r, 0, haut, seg, pos, parent, **kw); o.rotation_euler = rot; return o

def prisme(nom, h, pts, epaisseur, pos=(0, 0, 0), parent=None, rot=(0, 0, 0), **kw):
    """Polygone 2D (x, z) extrudé sur Y : drapeaux, lames, oreilles."""
    bm = bmesh.new(); vs = [bm.verts.new((x, -epaisseur / 2, z)) for x, z in pts]
    f = bm.faces.new(vs); r = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, verts=[v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)], vec=(0, epaisseur, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _bm_to(nom, bm, h, parent, **kw); o.location = pos; o.rotation_euler = rot; return o

def lisser(o, angle=50):
    for p in o.data.polygons: p.use_smooth = True
    try: o.data.set_sharp_from_angle(angle=math.radians(angle))
    except Exception: pass

def pivot(nom, pos=(0, 0, 0), parent=None):
    """Objet vide servant d'articulation (la pièce animée tourne autour)."""
    e = bpy.data.objects.new(nom, None); e.empty_display_size = 0.05
    (_coll or bpy.context.scene.collection).objects.link(e); e.location = pos
    if parent: e.parent = parent
    return e

# ---------- yeux et nez caricaturaux ----------
def yeux(parent, x, y, z, ecart, r, blanc='#ffffff', pupille='#1b1b1b'):
    for s, n in ((-1, 'G'), (1, 'D')):
        sphere(f'Oeil{n}', blanc, r, (x + s * ecart, y, z), (1, .7, 1.25), 10, 6, parent)
        sphere(f'Pupille{n}', pupille, r * .5, (x + s * ecart, y - r * .55, z - r * .15), (1, .6, 1), 8, 6, parent, rough=.3)

def copier(racine, pos, nom=None):
    """Copie d'une hiérarchie (maillages partagés), pour placer plusieurs exemplaires dans un rendu."""
    m = {}
    for o in descendants(racine):
        c = o.copy(); m[o] = c
        for col in o.users_collection: col.objects.link(c)
        if o.animation_data:
            c.animation_data_clear(); ad = c.animation_data_create()
            for tr in o.animation_data.nla_tracks:
                t2 = ad.nla_tracks.new(); t2.name = tr.name
                for st in tr.strips: t2.strips.new(st.name, int(st.frame_start), st.action)
    for o, c in m.items():
        if o.parent in m: c.parent = m[o.parent]
    m[racine].location = pos
    if nom: m[racine].name = nom
    return m[racine]

# ---------- peinture des sommets (dégradé façon peint à la main) ----------
def _hash(x, y, z):
    v = math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453
    return v - math.floor(v)

def peindre(racine, sol=.62, cime=1.1, bruit=.07, hauteur=None, local=.18):
    """Assombrit le bas (occlusion au sol), éclaircit le haut, et ajoute un léger grain déterministe.
    Le résultat est stocké dans l'attribut de couleur « Col » (exporté en COLOR_0)."""
    bpy.context.view_layer.update()
    objs = [o for o in descendants(racine) if o.type == 'MESH']
    zs = [(o.matrix_world @ v.co).z for o in objs for v in o.data.vertices]
    z0 = min(zs); H = hauteur or (max(zs) - z0) or 1
    for o in objs:
        me = o.data
        if 'Col' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Col'])
        ca = me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
        lz = [v.co.z for v in me.vertices]; l0, l1 = min(lz), max(lz)
        for poly in me.polygons:
            for li in poly.loop_indices:
                v = me.vertices[me.loops[li].vertex_index]; w = o.matrix_world @ v.co
                g = min(1, max(0, (w.z - z0) / H)); g = sol + (cime - sol) * (g ** .7)
                if l1 - l0 > 1e-4: g *= 1 - local + 2 * local * (v.co.z - l0) / (l1 - l0) * .5 + local * .5
                g *= 1 + (_hash(round(w.x, 2), round(w.y, 2), round(w.z, 2)) - .5) * 2 * bruit
                g = max(0, min(1, g))
                ca.data[li].color = (g, g * .985, g * .96, 1)
    return racine

# ---------- comptes ----------
def triangles(objs):
    n = 0
    for o in objs:
        if o.type == 'MESH':
            n += sum(len(p.vertices) - 2 for p in o.data.polygons)
    return n

def descendants(racine):
    out = [racine]
    for c in racine.children: out += descendants(c)
    return out

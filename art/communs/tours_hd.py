"""Tours « haute définition » (2.40, pilote Cour des Ossements) : le procédé des monstres organiques (Brute orc, Warg)
appliqué aux tours.

1. statue() : une créature de tour (squelette, gargouille, colosse…) est une union de volumes fondue d'un seul tenant
   (remaillage en voxels), dont une SCULPTURE détaillée (relief : os piqués, pierre rongée) est cuite en texture peinte
   et en carte de relief sur un modèle léger. Les tours ne s'animent que par pivots (Tourelle…) : la créature est donc
   modelée directement dans sa pose, sans squelette d'animation.
2. peindre_architecture() : les pièces fixes de la tour (pierre, fer, bois, neige) sont réunies en un seul maillage et
   reçoivent la même peinture cuite (occlusion dans les creux, arêtes éclaircies, dégradé, grain), au lieu d'une simple
   couleur par sommet.
Les pièces lumineuses gardent leur matériau « Lueur_… » ; les pièces animées (sous Tourelle, Orbe, Cristal, Anneaux…)
gardent la peinture par sommets.
Dépend de communs/organique.py (procédé des monstres, branche visuel/bestiaire-epique)."""
import bpy, math
from mathutils import Vector
from . import outils
from .organique import (Volume as V, symetrique, corps, corps_haut, ajouter_pieces, colorier_et_lier, peindre_texture,
                        lueur, _ctx, boule, cone, corne, tore, plaque, profil)
from .export_jeu import _couleur_base, _materiau_peint, _materiau_lueur

RELIEF_OS = [('CLOUDS', .006, .03, None), ('VORONOI', .004, .008, None)]       # os piqués et rongés
RELIEF_PIERRE = [('VORONOI', .016, .05, None), ('CLOUDS', .006, .012, None)]  # pierre taillée, éclats
ANIMES = ('Tourelle', 'Orbe', 'Cristal', 'Eclats', 'Anneaux', 'AnneauFlottant', 'Arme', 'Flamme')

def _joindre(objs, nom):
    objs = [o for o in objs if o]
    if len(objs) > 1:
        with _ctx(objs, objs[0]): bpy.ops.object.join()
    o = objs[0]; o.name = nom; o.data.name = nom
    return o

def _plus_proche(vols, P):
    """Indice du volume le plus proche de chaque point (tableau numpy N × 3), comme Volume.distance mais vectorisé."""
    import numpy as np
    D = np.empty((len(vols), len(P)), dtype=np.float32)
    for i, v in enumerate(vols):
        if v.kind == 'membre':
            a, b = np.array(v.a), np.array(v.b); ab = b - a; L2 = float(ab @ ab)
            t = np.clip(((P - a) @ ab) / L2, 0, 1) if L2 else np.zeros(len(P))
            d = np.linalg.norm(P - (a + np.outer(t, ab)), axis=1) - (v.ra + (v.rb - v.ra) * t)
        else:
            Mi = np.array(v.Mi); q = P @ Mi[:3, :3].T + Mi[:3, 3]
            d = (np.linalg.norm(q, axis=1) - 1.0) * min(v.r)
        D[i] = d - v.prio * 1e-3
    return D.argmin(axis=0)

def _couleurs_rapides(o, vols, idx):
    """Attribut « Col » (par coin) depuis l'indice de volume de chaque sommet."""
    import numpy as np
    from .outils import lin
    me = o.data
    pal = np.array([lin(v.col) for v in vols], dtype=np.float32)
    lv = np.empty(len(me.loops), dtype=np.int32); me.loops.foreach_get('vertex_index', lv)
    ca = me.color_attributes.get('Col') or me.color_attributes.new('Col', 'FLOAT_COLOR', 'CORNER')
    ca.data.foreach_set('color', pal[idx[lv]].ravel())

_GABARIT = {}
def _sphere_gabarit(u=14, v=9):
    """Sphère unité (sommets, faces) créée une seule fois."""
    import bmesh, numpy as np
    if (u, v) not in _GABARIT:
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=1.0)
        V_ = np.array([x.co[:] for x in bm.verts], dtype=np.float32)
        F_ = [[x.index for x in f.verts] for f in bm.faces]; bm.free()
        _GABARIT[(u, v)] = (V_, F_)
    return _GABARIT[(u, v)]

def maillage_rapide(nom, vols):
    """Même géométrie que Volume.maillage (ellipsoïdes, chapelets de sphères pour les membres), construite d'un bloc
    avec numpy : bmesh.ops.create_uvsphere devient très lent quand le maillage grossit (une centaine de volumes fins)."""
    import numpy as np
    V0, F0 = _sphere_gabarit(); nv = len(V0); pts, faces = [], []
    def ajouter(Pv):
        base = sum(len(p) for p in pts); pts.append(Pv); faces.extend([[i + base for i in f] for f in F0])
    for v in vols:
        if v.kind == 'ellipse':
            M = np.array(v.M); ajouter(V0 @ M[:3, :3].T + M[:3, 3])
        else:
            # membre : tronc de cône fermé et lisse + une sphère à chaque bout (le chapelet de sphères laissait des
            # bourrelets réguliers, visibles une fois cuits dans la carte de relief des grandes formes : robes, troncs)
            a, b = np.array(v.a), np.array(v.b)
            ajouter(V0 * v.ra + a); ajouter(V0 * v.rb + b)
            ax = b - a; L = np.linalg.norm(ax)
            if L < 1e-6: continue
            ax = ax / L; tmp = np.array((1.0, 0, 0)) if abs(ax[0]) < .9 else np.array((0, 1.0, 0))
            u = np.cross(ax, tmp); u /= np.linalg.norm(u); w = np.cross(ax, u)
            S, N = 16, max(2, min(24, int(L / max(.004, min(v.ra, v.rb))) + 1))
            ang = np.linspace(0, 2 * np.pi, S, endpoint=False)
            anneaux = []
            for i in range(N + 1):
                t = i / N; rr = v.ra + (v.rb - v.ra) * t; ctr = a + (b - a) * t
                anneaux.append(ctr + rr * (np.outer(np.cos(ang), u) + np.outer(np.sin(ang), w)))
            Pv = np.concatenate(anneaux + [a[None], b[None]]); base = sum(len(p) for p in pts); pts.append(Pv)
            for i in range(N):
                for k in range(S):
                    k2 = (k + 1) % S
                    faces.append([base + i * S + k, base + i * S + k2, base + (i + 1) * S + k2, base + (i + 1) * S + k])
            ca, cb = base + (N + 1) * S, base + (N + 1) * S + 1
            for k in range(S):
                k2 = (k + 1) % S
                faces.append([ca, base + k2, base + k]); faces.append([cb, base + N * S + k, base + N * S + k2])
    me = bpy.data.meshes.new(nom); me.from_pydata(np.concatenate(pts).tolist(), [], faces); me.update()
    o = bpy.data.objects.new(nom, me); bpy.context.collection.objects.link(o)
    return o

def corps_rapide(nom, vols, voxel=.011, lissage=6, triangles=2000):
    """organique.corps avec maillage_rapide."""
    o = maillage_rapide(nom + '_brut', vols); me = o.data
    m = o.modifiers.new('fondre', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = voxel; m.use_smooth_shade = True
    s = o.modifiers.new('lisser', 'SMOOTH'); s.factor = .5; s.iterations = lissage
    dg = bpy.context.evaluated_depsgraph_get()
    n = len(o.evaluated_get(dg).data.polygons)
    d = o.modifiers.new('alleger', 'DECIMATE'); d.ratio = min(1.0, triangles / max(1, 2 * n))
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
    me2.name = nom
    for p in me2.polygons: p.use_smooth = True
    o2 = bpy.data.objects.new(nom, me2); bpy.context.collection.objects.link(o2)
    return o2

def corps_haut_rapide(nom, vols, voxel=.0045, lissage=4, reliefs=()):
    """organique.corps_haut, avec la recherche du volume le plus proche vectorisée (numpy) : une créature de tour
    compte jusqu'à une centaine de volumes fins (os), et la boucle Python prenait plusieurs minutes."""
    import numpy as np
    o = maillage_rapide(nom + '_brut_haut', vols); me = o.data
    m = o.modifiers.new('fondre', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = voxel; m.use_smooth_shade = True
    s = o.modifiers.new('lisser', 'SMOOTH'); s.factor = .5; s.iterations = lissage
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
    h = bpy.data.objects.new(nom + '_haut', me2); bpy.context.collection.objects.link(h)
    P = np.empty(len(me2.vertices) * 3, dtype=np.float32); me2.vertices.foreach_get('co', P); P = P.reshape(-1, 3)
    idx = _plus_proche(vols, P)
    g = h.vertex_groups.new(name='relief')
    rels = np.array([v.rel for v in vols])[idx]
    for r in set(rels.tolist()):
        if r > 0: g.add(np.nonzero(rels == r)[0].tolist(), float(r), 'REPLACE')
    _couleurs_rapides(h, vols, idx)
    jetables = []
    for k, (typ, force, taille, etire) in enumerate(reliefs):
        tex = bpy.data.textures.new(f'{nom}_relief{k}', typ); tex.noise_scale = taille
        if hasattr(tex, 'noise_depth'): tex.noise_depth = 2
        d = h.modifiers.new(f'relief{k}', 'DISPLACE'); d.texture = tex; d.strength = force; d.mid_level = .5; d.vertex_group = 'relief'
        d.texture_coords = 'LOCAL'; jetables.append(tex)
    if reliefs:
        dg = bpy.context.evaluated_depsgraph_get()
        me3 = bpy.data.meshes.new_from_object(h.evaluated_get(dg))
        h.modifiers.clear(); vieux = h.data; h.data = me3; bpy.data.meshes.remove(vieux)
    for x in jetables: bpy.data.textures.remove(x)
    for p in h.data.polygons: p.use_smooth = True
    return h

def statue(nom, vols, pieces=(), lueurs=(), couleur_lueur='#6fd2c0', relief=RELIEF_OS, tri=1400, voxel=.007, H=1.0,
           taches=.15, taille=512):
    """Créature construite à la hauteur 1 (regard vers -Y), fondue, sculptée, peinte ; mise à la taille H.
    Renvoie (maillage peint, maillage des lueurs ou None)."""
    import time; t0 = time.time()
    trace = lambda m: print(f'[statue {nom}] {m} {time.time() - t0:.1f} s', flush=True)
    vols = symetrique(vols)
    c = corps_rapide(nom, vols, voxel=voxel, lissage=4, triangles=tri); trace(f'corps ({len(vols)} volumes)')
    colorier_et_lier(c, vols); trace('couleurs')
    haut = corps_haut_rapide(nom, vols, voxel=max(.0028, voxel * .6), reliefs=relief); trace(f'sculpture ({len(haut.data.vertices)} sommets)')
    # 2.40 : seul le corps est cuit depuis sa sculpture ; les accessoires (armure, armes) collés aux os faussaient la cuisson
    # (taches noires) : ils gardent leur peinture par sommets, avec l'occlusion cuite dans les sommets
    for g in list(c.vertex_groups): c.vertex_groups.remove(g)
    peindre_texture(c, taille=taille, occl=.05, H=1.0, source=haut, relief=1.0, taille_relief=max(128, taille * 3 // 4), taches=taches, taille_taches=10,
                    sol=.6, cime=1.08, aretes=.3, grain=.08)
    trace('peinture cuite')
    acc = None
    if pieces:
        acc = _joindre(list(pieces), nom + '_accessoires')
        for g in list(acc.vertex_groups): acc.vertex_groups.remove(g)
        acc.data.materials.clear(); acc.data.materials.append(_materiau_peint())
        occlusion_sommets(acc, autres=[c]); trace('accessoires')
    lu = None
    if lueurs:
        lu = _joindre(list(lueurs), nom + '_lueur')
        for g in list(lu.vertex_groups): lu.vertex_groups.remove(g)
        lueur(lu, couleur_lueur)
    for o in (c, acc, lu):
        if o is None: continue
        o.scale = (H, H, H)
        with _ctx([o]): bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return c, acc, lu

def poser(objs, parent, pos=(0, 0, 0), rot=(0, 0, 0)):
    for o in objs:
        if o is None: continue
        o.parent = parent; o.location = pos; o.rotation_euler = rot; o['statue'] = 1

def peindre_sauf_statues(racine, **kw):
    """outils.peindre (dégradé et grain par sommets) sans toucher aux créatures déjà peintes (marquées par poser())."""
    import numpy as np
    gardes = []
    for o in outils.descendants(racine):
        if o.type == 'MESH' and o.get('statue') and 'Col' in o.data.color_attributes:
            a = o.data.color_attributes['Col']; v = np.empty(len(a.data) * 4, dtype=np.float32); a.data.foreach_get('color', v)
            gardes.append((o, a.data_type, v))
    outils.peindre(racine, **kw)
    for o, typ, v in gardes:
        me = o.data
        if 'Col' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Col'])
        a = me.color_attributes.new('Col', typ, 'CORNER'); a.data.foreach_set('color', v)
    for o in outils.descendants(racine):
        if o.type == 'MESH' and o.get('statue') and o.data.materials and o.data.materials[0].name.startswith(('Peau', 'Lueur_')):
            if 'Col' in o.data.color_attributes: o.data.color_attributes.remove(o.data.color_attributes['Col'])

def _anime(o, racine):
    p = o.parent
    while p is not None and p is not racine:
        if p.name.split('.')[0].startswith(ANIMES): return True
        p = p.parent
    return False

def _cuire_sommets(racine):
    """Comme export_jeu.cuire, mais laisse intactes les créatures déjà peintes (matériau « Peau »)."""
    peint = _materiau_peint()
    for o in outils.descendants(racine):
        if o.type != 'MESH' or not o.data.materials: continue
        m0 = o.data.materials[0]
        if m0.name.startswith(('Peau', 'Lueur_', 'Peint', 'Drapeau')): continue
        me = o.data
        if me.users > 1: o.data = me = me.copy()
        rgb, e = _couleur_base(m0)
        if e > 0:
            me.materials.clear(); me.materials.append(_materiau_lueur(rgb))
            if 'Col' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Col'])
            continue
        if 'Col' not in me.color_attributes:
            ca = me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
            for d in ca.data: d.color = (1, 1, 1, 1)
        for d in me.color_attributes['Col'].data:
            c = d.color; d.color = (c[0] * rgb[0], c[1] * rgb[1], c[2] * rgb[2], 1)
        me.materials.clear(); me.materials.append(peint)

def occlusion_sommets(o, autres=(), distance=.06, force=.62, subdiviser=0):
    """Cuit l'occlusion ambiante (Cycles) dans un attribut de sommets et l'applique à « Col » : creux et pieds de murs
    assombris, sans dépliage ni texture (robuste avec des pièces qui se chevauchent). autres : objets qui font de l'ombre."""
    import numpy as np
    sc = bpy.context.scene
    try: sc.render.engine = 'CYCLES'
    except TypeError: pass
    sc.cycles.samples = 64; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False
    sc.world = sc.world or bpy.data.worlds.new('Monde')
    sc.world.light_settings.distance = distance
    me = o.data
    if 'Col' not in me.color_attributes: return
    if me.color_attributes['Col'].data_type != 'FLOAT_COLOR' or me.color_attributes['Col'].domain != 'CORNER':
        # même type que l'attribut de cuisson, pour que la cuisson n'écrive pas dans « Col »
        pass
    ao = me.color_attributes.new('AO', 'FLOAT_COLOR', 'CORNER')
    noms = [a.name for a in me.color_attributes]
    me.color_attributes.active_color = ao; me.color_attributes.render_color_index = noms.index('AO')
    b = sc.render.bake; b.target = 'VERTEX_COLORS'; b.use_selected_to_active = False
    for x in bpy.context.view_layer.objects: x.select_set(x == o)
    bpy.context.view_layer.objects.active = o
    with _ctx([o]): bpy.ops.object.bake(type='AO')
    b.target = 'IMAGE_TEXTURES'
    n = len(me.loops)
    a = np.empty(n * 4, dtype=np.float32); ao.data.foreach_get('color', a)
    col = me.color_attributes['Col']; cc = np.empty(n * 4, dtype=np.float32); col.data.foreach_get('color', cc)
    f = (1 - force) + force * a.reshape(-1, 4)[:, :1]
    cc = cc.reshape(-1, 4); cc[:, :3] *= f; col.data.foreach_set('color', cc.ravel())
    me.color_attributes.remove(me.color_attributes['AO'])
    me.color_attributes.active_color = me.color_attributes['Col']
    me.color_attributes.render_color_index = [a.name for a in me.color_attributes].index('Col')

def peindre_architecture(racine, taille=1024, sol=.45, cime=1.0, aretes=.32, grain=.1):
    """Réunit les pièces fixes peintes par sommets en un maillage « Architecture », avec l'occlusion cuite dans les sommets.
    (Une première version cuisait une texture peinte : trop sombre, et le dépliage de pièces qui se chevauchent créait des
    artefacts ; l'occlusion par sommets garde le matériau « Peint » du jeu.)"""
    bpy.context.view_layer.update()
    _cuire_sommets(racine)
    fixes = [o for o in outils.descendants(racine) if o.type == 'MESH' and o.data.materials and o.data.materials[0].name == 'Peint'
             and not _anime(o, racine)]
    if not fixes: return None
    mw = racine.matrix_world.copy()
    for o in fixes:
        w = o.matrix_world.copy(); o.parent = racine; o.matrix_world = w
    a = _joindre(fixes, racine.name + '_architecture')
    # densifier un peu les grandes faces pour que l'occlusion par sommets ait des points où se poser
    import bmesh
    bm = bmesh.new(); bm.from_mesh(a.data)
    longues = [e for e in bm.edges if e.calc_length() > .12]
    if longues: bmesh.ops.subdivide_edges(bm, edges=longues, cuts=2, use_grid_fill=True)
    bm.to_mesh(a.data); bm.free()
    occlusion_sommets(a, distance=.08, force=.55)
    return a

# ------------------------------------------------------------------ squelette « haute définition »
OS, OS2, OS3, NOIR = '#c2b393', '#a3946f', '#6f6248', '#141116'

def squelette_vols(J, os_=OS, os2=OS2, ombre=NOIR, cotes=4, epaisseur=1.0):
    """Volumes d'un squelette humain réaliste (crâne aux orbites creuses, cage thoracique, bassin, os longs à épiphyses)
    selon les articulations J (posées, côté .L = +X). Les .R sont recopiés par symétrie : pour un bras posé différemment
    à droite, donner aussi les articulations .R (alors seuls les volumes .L listés ici sont recopiés… sauf si J a les .R)."""
    e = epaisseur; v = []
    def os_long(nom, a, b, r):
        a, b = Vector(a), Vector(b)
        v.append(V(nom, os2, a=a, b=b, ra=r * e, rb=r * .85 * e))
        v.append(V(nom, os_, c=a, r=(r * 1.5 * e,) * 3)); v.append(V(nom, os_, c=b, r=(r * 1.4 * e,) * 3))
    g = lambda n: Vector(J[n])
    t = g('tete')
    # crâne : boîte crânienne, maxillaire, pommettes, mâchoire, orbites et fosse nasale creusées (couleur sombre, sans relief)
    v += [V('Tete', os_, c=t + Vector((0, .012, .062)), r=(.05, .066, .058)),
          V('Tete', os2, c=t + Vector((0, -.045, .065)), r=(.045, .02, .022), rot=(.3, 0, 0), prio=1),   # front et arcades
          V('Tete', os_, c=t + Vector((0, -.045, .02)), r=(.042, .03, .032), prio=1),
          V('Tete', os2, c=t + Vector((.032, -.04, .022)), r=(.016, .022, .014), prio=1),
          V('Tete', os2, c=t + Vector((0, -.04, -.025)), r=(.038, .03, .012), rot=(.3, 0, 0), prio=1),
          V('Tete', ombre, c=t + Vector((.022, -.06, .04)), r=(.016, .012, .015), prio=3, rel=0),
          V('Tete', ombre, c=t + Vector((0, -.072, .018)), r=(.007, .008, .011), prio=3, rel=0)]
    v.append(V('Tete', ombre, c=t + Vector((0, -.066, -.003)), r=(.022, .006, .003), prio=3, rel=0))   # fente des dents
    # colonne et vertèbres
    os_long('Colonne', g('bassin') + Vector((0, .03, .03)), g('cou') + Vector((0, .02, 0)), .011)
    for k in range(4):
        z = g('bassin').lerp(g('cou'), k / 3.0)
        v.append(V('Colonne', os_, c=z + Vector((0, .045, .02)), r=(.013, .012, .01)))
    # bassin : ailes iliaques et sacrum
    b = g('bassin')
    v += [V('Hanches', os_, c=b + Vector((.045, .01, .02)), r=(.04, .018, .036), rot=(0, .3, -.4)),
          V('Hanches', os2, c=b + Vector((0, .03, 0)), r=(.025, .015, .035))]
    # cage thoracique : côtes en arc (3 segments par côte), sternum, clavicules
    p, c = g('poitrine'), g('cou')
    for k in range(cotes):
        z = p.z + .055 - k * .038; w = .072 - abs(k - 1.2) * .008
        a0 = Vector((.008, .04, z + .01)); a1 = Vector((w, .02, z)); a2 = Vector((w * 1.02, -.035, z - .02)); a3 = Vector((.016, -.06, z - .04))
        for q, (x, y) in enumerate(((a0, a1), (a1, a2), (a2, a3))):
            v.append(V('Torse', os_ if q != 1 else os2, a=x, b=y, ra=.0085 * e, rb=.008 * e))
    v.append(V('Torse', os2, a=Vector((0, -.062, p.z + .05)), b=Vector((0, -.06, p.z - .07)), ra=.009 * e, rb=.007 * e))
    os_long('Epaule.L', Vector((.012, -.03, c.z - .02)), g('epaule.L') + Vector((0, -.01, .01)), .0085)
    v.append(V('Epaule.L', os2, c=g('epaule.L') + Vector((-.03, .05, -.04)), r=(.035, .008, .045), rot=(0, 0, -.3)))  # omoplate
    # membres
    os_long('Bras.L', g('epaule.L'), g('coude.L'), .012)
    av = g('poignet.L') - g('coude.L'); n = av.cross(Vector((0, 0, 1))); n = n.normalized() * .008 if n.length > 1e-4 else Vector((.008, 0, 0))
    v.append(V('AvantBras.L', os2, a=g('coude.L') + n, b=g('poignet.L') + n, ra=.009 * e, rb=.008 * e))   # radius
    v.append(V('AvantBras.L', os2, a=g('coude.L') - n, b=g('poignet.L') - n, ra=.008 * e, rb=.007 * e))   # cubitus
    v.append(V('Main.L', os_, c=g('poignet.L').lerp(g('doigts.L'), .3), r=(.016, .012, .02)))
    for k in range(2):
        d = g('doigts.L') - g('poignet.L')
        base = g('poignet.L').lerp(g('doigts.L'), .45) + Vector(((k - .5) * .01, 0, 0))
        v.append(V('Main.L', os2, a=base, b=base + d * .65, ra=.0055, rb=.0045))
    os_long('Cuisse.L', g('hanche.L'), g('genou.L'), .015)
    v.append(V('Cuisse.L', os_, c=g('genou.L') + Vector((0, -.018, .005)), r=(.012, .008, .014)))        # rotule
    gn, ch = g('genou.L'), g('cheville.L')
    v.append(V('Tibia.L', os2, a=gn, b=ch, ra=.011 * e, rb=.008 * e))
    v.append(V('Tibia.L', os2, a=gn + Vector((.012, .01, 0)), b=ch + Vector((.01, .008, 0)), ra=.0065, rb=.0055))  # péroné
    v.append(V('Pied.L', os_, c=ch + Vector((0, -.035, -.025)), r=(.022, .05, .014)))
    # cou : vertèbres cervicales entre la colonne et le crâne
    os_long('Cou', g('cou') + Vector((0, .02, 0)), t + Vector((0, .015, .03)), .009)
    # pièces centrales hors de l'axe (côtes, orbite, pommette, aile du bassin…) : recopiées de l'autre côté
    from .organique import miroir
    hors = lambda x: (abs(x.c.x) > 1e-3) if x.kind == 'ellipse' else (abs(x.a.x) > 1e-3 or abs(x.b.x) > 1e-3)
    v += [miroir(x) for x in v if '.L' not in x.os and hors(x)]
    return v

def joints_debout(bras_l=None, bras_r=None, z0=0.0):
    """Articulations d'un squelette debout (hauteur 1), bras le long du corps sauf si bras_l / bras_r donnent
    (épaule, coude, poignet, doigts) ; côté droit fourni → il n'est pas recopié par symétrie."""
    J = {'bassin': (0, .02, .5), 'ventre': (0, .03, .6), 'poitrine': (0, .02, .7), 'cou': (0, 0, .82), 'tete': (0, -.01, .87),
         'sommet': (0, -.02, 1.0), 'clavicule.L': (.03, 0, .8),
         'epaule.L': (.105, .01, .79), 'coude.L': (.135, .03, .6), 'poignet.L': (.14, 0, .44), 'doigts.L': (.14, -.02, .38),
         'hanche.L': (.065, .02, .49), 'genou.L': (.075, -.01, .27), 'cheville.L': (.08, .02, .06), 'orteils.L': (.08, -.08, .015)}
    if bras_l: J.update(zip(('epaule.L', 'coude.L', 'poignet.L', 'doigts.L'), bras_l))
    return {k: (x, y, z + z0) for k, (x, y, z) in J.items()}, bras_r

def squelette_statue(nom, J, bras_r=None, pieces=(), lueurs=(), H=.35, tri=1500, voxel=.0045, taille=512, **kw):
    """Squelette complet : les volumes .L sont recopiés à droite ; avec bras_r (épaule, coude, poignet, doigts du côté
    droit, x négatifs), le bras droit est posé à part."""
    vols = squelette_vols(J, **kw)
    if bras_r:
        Jr = dict(J); Jr.update(zip(('epaule.L', 'coude.L', 'poignet.L', 'doigts.L'), [(-x, y, z) for x, y, z in bras_r]))
        bras = [x for x in squelette_vols(Jr, **kw) if x.os in ('Bras.L', 'AvantBras.L', 'Main.L')]
        vols = [x for x in vols if x.os not in ('Bras.L', 'AvantBras.L', 'Main.L')] + [x for x in squelette_vols(J, **kw) if x.os in ('Bras.L', 'AvantBras.L', 'Main.L')]
        from .organique import miroir
        vols += [miroir(x) for x in bras]
        # miroir() renomme .L → .R ; on retire la recopie automatique du bras gauche en marquant les volumes
        for x in vols:
            if x.os in ('Bras.L', 'AvantBras.L', 'Main.L'): x.os = x.os.replace('.L', '.G')
    return statue(nom, vols, pieces, lueurs, H=H, tri=tri, voxel=voxel, taille=taille)

def copier_statue(objs, collection):
    """Copie indépendante d'une créature (corps, accessoires, lueurs) : même texture, maillages copiés."""
    copie = []
    for o in objs:
        if o is None: copie.append(None); continue
        n = o.copy(); n.data = o.data.copy(); collection.objects.link(n); copie.append(n)
    return copie

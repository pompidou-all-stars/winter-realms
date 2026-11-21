"""Créatures « organiques » (pilote de la montée en gamme des monstres, 2.30).

Différences avec personnages.py / betes.py (formes simples posées côte à côte, pièces rigides) :
1. Le CORPS est d'un seul tenant : une union de volumes (ellipsoïdes, membres effilés) est fondue par un
   remaillage en voxels, lissée puis allégée. Plus de jointures visibles aux épaules ou aux hanches.
2. Un SQUELETTE (armature) déforme le corps. Les poids viennent des volumes eux-mêmes : chaque volume est
   attaché à un os, et un sommet suit les os des volumes les plus proches (fondu doux aux articulations).
   Les accessoires durs (armure, arme, casque) suivent un seul os.
3. Une TEXTURE PEINTE est cuite (Cycles) : couleur de chaque volume, ombre dans les creux (occlusion),
   arêtes éclaircies, dégradé du bas vers le haut, léger grain. Un seul matériau « Peau » lit cette image.
4. Les animations sont des clés d'os : elles servent à tous les monstres d'une même famille de squelette.

Convention : on construit à l'échelle 1 (H = 1, pieds en z = 0, le monstre regarde vers -Y), puis
`finir()` met à la taille du jeu. Côté .L = +X (gauche du monstre), .R = -X.
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix, Euler
from .outils import lin

# ------------------------------------------------------------------ volumes
class Volume:
    """Ellipsoïde (centre c, demi-axes r, rotation rot) ou membre effilé (a → b, rayons ra → rb)."""
    def __init__(self, os_, col, c=None, r=None, rot=(0, 0, 0), a=None, b=None, ra=None, rb=None, prio=0, rel=1.0):
        self.os, self.col, self.prio, self.rel = os_, col, prio, rel   # rel : part du relief sculpté (0 = lisse : truffe, yeux…)
        if a is not None:
            self.a, self.b, self.ra, self.rb = Vector(a), Vector(b), ra, rb if rb is not None else ra
            self.kind = 'membre'
        else:
            self.c, self.r, self.kind = Vector(c), Vector(r), 'ellipse'
            self.M = Matrix.Translation(self.c) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((*self.r, 1))
            self.Mi = self.M.inverted()

    def distance(self, p):
        if self.kind == 'membre':
            ab = self.b - self.a; L2 = ab.length_squared
            t = max(0.0, min(1.0, (p - self.a).dot(ab) / L2)) if L2 else 0.0
            return (p - (self.a + ab * t)).length - (self.ra + (self.rb - self.ra) * t)
        q = self.Mi @ p
        return (q.length - 1.0) * min(self.r)

    def maillage(self, bm):
        """Ajoute le volume au bmesh (sphère déformée, ou chapelet de sphères pour un membre)."""
        if self.kind == 'ellipse':
            res = bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=1.0)
            bmesh.ops.transform(bm, matrix=self.M, verts=res['verts'])
            return
        n = max(2, int((self.b - self.a).length / (min(self.ra, self.rb) * .5)) + 1)
        for i in range(n + 1):
            t = i / n; r = self.ra + (self.rb - self.ra) * t
            res = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=r)
            bmesh.ops.translate(bm, vec=self.a.lerp(self.b, t), verts=res['verts'])

def _ctx(objs, actif=None):
    """Contexte explicite pour les opérateurs (fonctionne en ligne de commande comme dans Blender ouvert)."""
    objs = list(objs); actif = actif or objs[0]
    return bpy.context.temp_override(object=actif, active_object=actif, selected_objects=objs, selected_editable_objects=objs)

def miroir(v):
    """Copie d'un volume du côté .L vers le côté .R (x → -x)."""
    s = lambda p: Vector((-p[0], p[1], p[2]))
    os_ = v.os.replace('.L', '.R')
    if v.kind == 'membre':
        return Volume(os_, v.col, a=s(v.a), b=s(v.b), ra=v.ra, rb=v.rb, prio=v.prio, rel=v.rel)
    rot = v.M.to_3x3().normalized().to_euler()
    return Volume(os_, v.col, c=s(v.c), r=v.r, rot=(rot.x, -rot.y, -rot.z), prio=v.prio, rel=v.rel)

def symetrique(vols):
    return vols + [miroir(v) for v in vols if '.L' in v.os]

# ------------------------------------------------------------------ squelette
def squelette(nom, joints, os_):
    """joints : {'nom': (x, y, z)} (les .L sont recopiés en .R) ; os_ : [(nom, tête, queue, parent)]."""
    J = dict(joints)
    for k, p in joints.items():
        if k.endswith('.L'): J[k[:-2] + '.R'] = (-p[0], p[1], p[2])
    liste = []
    for (n, t, q, par) in os_:
        liste.append((n, t, q, par))
        if n.endswith('.L'):
            liste.append((n[:-2] + '.R', t.replace('.L', '.R'), q.replace('.L', '.R'), par.replace('.L', '.R') if par else par))
    arm = bpy.data.armatures.new(nom + '_squelette')
    o = bpy.data.objects.new(nom, arm); bpy.context.collection.objects.link(o)
    bpy.context.view_layer.objects.active = o
    with _ctx([o]): bpy.ops.object.mode_set(mode='EDIT')
    for (n, t, q, par) in liste:
        b = arm.edit_bones.new(n); b.head = J[t]; b.tail = J[q]
        b.roll = 0
        if par: b.parent = arm.edit_bones[par]; b.use_connect = False
    with _ctx([o]): bpy.ops.object.mode_set(mode='OBJECT')
    for pb in o.pose.bones: pb.rotation_mode = 'XYZ'
    return o

# ------------------------------------------------------------------ corps fondu
def _nouvel_objet(nom, me):
    o = bpy.data.objects.new(nom, me); bpy.context.collection.objects.link(o); return o

def corps(nom, vols, voxel=.011, lissage=6, triangles=2000):
    """Union des volumes → remaillage voxel → lissage → allègement. Renvoie l'objet maillage."""
    bm = bmesh.new()
    for v in vols: v.maillage(bm)
    me = bpy.data.meshes.new(nom + '_brut'); bm.to_mesh(me); bm.free()
    o = _nouvel_objet(nom + '_brut', me)
    m = o.modifiers.new('fondre', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = voxel; m.use_smooth_shade = True
    s = o.modifiers.new('lisser', 'SMOOTH'); s.factor = .5; s.iterations = lissage
    dg = bpy.context.evaluated_depsgraph_get()
    n = len(o.evaluated_get(dg).data.polygons)
    d = o.modifiers.new('alleger', 'DECIMATE'); d.ratio = min(1.0, triangles / max(1, 2 * n))   # remaillage en quadrilatères → 2 triangles chacun
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
    me2.name = nom
    for p in me2.polygons: p.use_smooth = True
    return _nouvel_objet(nom, me2)

def corps_haut(nom, vols, voxel=.0045, lissage=4, reliefs=()):
    """Version très détaillée du corps (2.31), qui n'est jamais exportée : elle sert de « sculpture » dont on cuit
    le relief (normal map) et les ombres fines (texture) sur le corps léger.
    reliefs : [(type, force, taille, etirement)] ; type de texture Blender ('CLOUDS', 'VORONOI', 'STUCCI') ;
    etirement (sx, sy, sz) allonge le motif (poils couchés le long du corps) ou None.
    Le relief est dosé par Volume.rel (groupe de sommets « relief »)."""
    bm = bmesh.new()
    for v in vols: v.maillage(bm)
    me = bpy.data.meshes.new(nom + '_brut_haut'); bm.to_mesh(me); bm.free()
    o = _nouvel_objet(nom + '_brut_haut', me)
    m = o.modifiers.new('fondre', 'REMESH'); m.mode = 'VOXEL'; m.voxel_size = voxel; m.use_smooth_shade = True
    s = o.modifiers.new('lisser', 'SMOOTH'); s.factor = .5; s.iterations = lissage
    dg = bpy.context.evaluated_depsgraph_get()
    me2 = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
    bpy.data.objects.remove(o, do_unlink=True); bpy.data.meshes.remove(me)
    h = _nouvel_objet(nom + '_haut', me2)
    # couleur et dose de relief du volume le plus proche
    cols, g = [None] * len(me2.vertices), h.vertex_groups.new(name='relief')
    par_rel = {}
    for v in me2.vertices:
        d, vol = min(((vol.distance(v.co) - vol.prio * 1e-3, vol) for vol in vols), key=lambda x: x[0])
        cols[v.index] = vol.col; par_rel.setdefault(vol.rel, []).append(v.index)
    for r, idx in par_rel.items():
        if r > 0: g.add(idx, r, 'REPLACE')
    _remplir_couleurs(h, lambda vi: cols[vi])
    jetables = []
    for k, (typ, force, taille, etire) in enumerate(reliefs):
        tex = bpy.data.textures.new(f'{nom}_relief{k}', typ); tex.noise_scale = taille
        if hasattr(tex, 'noise_depth'): tex.noise_depth = 2
        d = h.modifiers.new(f'relief{k}', 'DISPLACE'); d.texture = tex; d.strength = force; d.mid_level = .5; d.vertex_group = 'relief'
        if etire:
            e = bpy.data.objects.new(f'{nom}_axes{k}', None); bpy.context.collection.objects.link(e); e.scale = etire
            d.texture_coords = 'OBJECT'; d.texture_coords_object = e; jetables.append(e)
        else:
            d.texture_coords = 'LOCAL'
        jetables.append(tex)
    if reliefs:
        dg = bpy.context.evaluated_depsgraph_get()
        me3 = bpy.data.meshes.new_from_object(h.evaluated_get(dg))
        h.modifiers.clear(); vieux = h.data; h.data = me3; bpy.data.meshes.remove(vieux)
    for x in jetables:
        (bpy.data.objects if isinstance(x, bpy.types.Object) else bpy.data.textures).remove(x)
    for p in h.data.polygons: p.use_smooth = True
    return h

def ajouter_pieces(haut, pieces):
    """Copie les accessoires dans la sculpture, pour que leur cuisson se fasse aussi depuis la version détaillée."""
    copies = []
    for p in pieces:
        c = p.copy(); c.data = p.data.copy(); bpy.context.collection.objects.link(c); copies.append(c)
    with _ctx([haut] + copies, haut): bpy.ops.object.join()
    return haut

def colorier_et_lier(o, vols, adoucir=.025):
    """Couleur du volume le plus proche, et poids d'os en fondu doux (4 os au plus par sommet)."""
    me = o.data
    cols = [None] * len(me.vertices)
    poids = []
    for v in me.vertices:
        p = v.co
        ds = [(vol.distance(p) - vol.prio * 1e-3, vol) for vol in vols]
        dmin, vmin = min(ds, key=lambda x: x[0])
        cols[v.index] = vmin.col
        par_os = {}
        for d, vol in ds:
            par_os[vol.os] = min(par_os.get(vol.os, 9), d)
        w = {k: math.exp(-(d - dmin) / adoucir) for k, d in par_os.items() if d - dmin < adoucir * 4}
        w = sorted(w.items(), key=lambda x: -x[1])[:4]
        tot = sum(x[1] for x in w)
        poids.append([(k, x / tot) for k, x in w if x / tot > .03])
    groupes = {}
    for i, lst in enumerate(poids):
        for k, x in lst:
            g = groupes.get(k) or o.vertex_groups.get(k) or o.vertex_groups.new(name=k); groupes[k] = g
            g.add([i], x, 'REPLACE')
    _remplir_couleurs(o, lambda vi: cols[vi])

def _remplir_couleurs(o, f):
    me = o.data
    ca = me.color_attributes.get('Col') or me.color_attributes.new('Col', 'FLOAT_COLOR', 'CORNER')
    cache = {}
    for l in me.loops:
        h = f(l.vertex_index)
        if h not in cache: cache[h] = lin(h)
        ca.data[l.index].color = cache[h]

# ------------------------------------------------------------------ accessoires durs
def _objet_bm(nom, bm, col, os_, lisse_angle=40):
    me = bpy.data.meshes.new(nom); bm.to_mesh(me); bm.free()
    o = _nouvel_objet(nom, me)
    for p in me.polygons: p.use_smooth = True
    me.set_sharp_from_angle(angle=math.radians(lisse_angle))
    g = o.vertex_groups.new(name=os_); g.add(list(range(len(me.vertices))), 1.0, 'REPLACE')
    _remplir_couleurs(o, lambda vi: col)
    return o

def _placer(bm, verts, pos, rot, ech=(1, 1, 1)):
    M = Matrix.Translation(Vector(pos)) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((*ech, 1))
    bmesh.ops.transform(bm, matrix=M, verts=verts)

def _biseauter(bm, largeur):
    if largeur > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=largeur, segments=1, affect='EDGES', profile=.5)

def boule(nom, col, os_, pos, r, ech=(1, 1, 1), rot=(0, 0, 0), demi=False, seg=12):
    bm = bmesh.new(); res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(6, seg // 2), radius=r)
    if demi:
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-5], context='VERTS')
        bmesh.ops.contextual_create(bm, geom=[e for e in bm.edges if e.is_boundary])
    _placer(bm, bm.verts, pos, rot, ech)
    return _objet_bm(nom, bm, col, os_, 60)

def cone(nom, col, os_, pos, r1, r2, h, rot=(0, 0, 0), seg=8, biseau=0.0, ech=(1, 1, 1)):
    """Cône ou cylindre dont la base est en pos, dirigé selon +Z local (puis rot)."""
    bm = bmesh.new()
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r1, radius2=r2, depth=h)
    bmesh.ops.translate(bm, vec=(0, 0, h / 2), verts=bm.verts)
    _biseauter(bm, biseau)
    _placer(bm, bm.verts, pos, rot, ech)
    return _objet_bm(nom, bm, col, os_)

def corne(nom, col, os_, pos, r, longueur, courbe, rot=(0, 0, 0), seg=6, n=4):
    """Corne / défense / pointe recourbée : anneaux qui s'affinent le long d'un arc."""
    bm = bmesh.new(); anneaux = []
    for i in range(n + 1):
        t = i / n; ang = courbe * t
        # arc dans le plan YZ : centre de courbure en (0, -R, 0)
        R = longueur / max(abs(courbe), 1e-3)
        cy, cz = (R - R * math.cos(ang)) * (1 if courbe > 0 else -1), R * math.sin(abs(ang))
        rr = r * (1 - t) ** .85 + r * .04
        ring = []
        for k in range(seg):
            a = 2 * math.pi * k / seg
            ring.append(bm.verts.new((rr * math.cos(a), cy + rr * math.sin(a) * math.cos(ang), cz - rr * math.sin(a) * math.sin(ang))))
        anneaux.append(ring)
    for i in range(n):
        for k in range(seg):
            a, b = anneaux[i][k], anneaux[i][(k + 1) % seg]
            c, d = anneaux[i + 1][(k + 1) % seg], anneaux[i + 1][k]
            bm.faces.new((a, b, c, d))
    bm.faces.new(list(reversed(anneaux[0])))
    bm.faces.new(anneaux[-1])
    _placer(bm, bm.verts, pos, rot)
    return _objet_bm(nom, bm, col, os_, 70)

def tore(nom, col, os_, pos, R, r, rot=(0, 0, 0), ech=(1, 1, 1), seg=14, seg2=5):
    bm = bmesh.new(); anneaux = []
    for i in range(seg):
        a = 2 * math.pi * i / seg; ring = []
        for k in range(seg2):
            b = 2 * math.pi * k / seg2
            rr = R + r * math.cos(b)
            ring.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), r * math.sin(b))))
        anneaux.append(ring)
    for i in range(seg):
        for k in range(seg2):
            a1, a2 = anneaux[i], anneaux[(i + 1) % seg]
            bm.faces.new((a1[k], a2[k], a2[(k + 1) % seg2], a1[(k + 1) % seg2]))
    _placer(bm, bm.verts, pos, rot, ech)
    return _objet_bm(nom, bm, col, os_, 60)

def plaque(nom, col, os_, pos, sx, sy, sz, rot=(0, 0, 0), biseau=.006, ech=(1, 1, 1)):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    _biseauter(bm, biseau)
    _placer(bm, bm.verts, pos, rot, ech)
    return _objet_bm(nom, bm, col, os_, 35)

def profil(nom, col, os_, pts, epaisseur, pos=(0, 0, 0), rot=(0, 0, 0), biseau=.004):
    """Plaque découpée : contour pts [(x, z)] dans le plan XZ, épaisseur selon Y (lame de hache, pagne…)."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, -epaisseur / 2, z)) for x, z in pts]
    f = bm.faces.new(vs)
    res = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=(0, epaisseur, 0), verts=[v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    _biseauter(bm, biseau)
    _placer(bm, bm.verts, pos, rot)
    return _objet_bm(nom, bm, col, os_, 35)

# ------------------------------------------------------------------ assemblage, texture peinte
def assembler(nom, arm, corps_o, pieces, lueurs=()):
    """Joint corps + accessoires en un seul maillage skinné (« nom »), les lueurs (yeux) en un second."""
    def joindre(objs, n):
        if len(objs) > 1:
            with _ctx(objs): bpy.ops.object.join()
        o = objs[0]; o.name = n; o.data.name = n
        o.parent = arm
        m = o.modifiers.new('squelette', 'ARMATURE'); m.object = arm
        return o
    peau = joindre([corps_o] + list(pieces), nom + '_peau')
    yeux = joindre(list(lueurs), nom + '_lueur') if lueurs else None
    return peau, yeux

def _deplier(o):
    bpy.context.view_layer.objects.active = o
    for p in o.data.polygons: p.select = True
    for v in o.data.vertices: v.select = True
    for e in o.data.edges: e.select = True
    with _ctx([o]): bpy.ops.object.mode_set(mode='EDIT')
    with bpy.context.temp_override(object=o, active_object=o, edit_object=o, selected_objects=[o], selected_editable_objects=[o]):
        bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=.012, area_weight=0.0, scale_to_bounds=False)
        bpy.ops.object.mode_set(mode='OBJECT')

def peindre_texture(o, taille=512, occl=.10, H=1.0, echantillons=48, sol=.62, cime=1.08, grain=.06, aretes=.22, nom_img=None,
                    source=None, relief=1.0, taille_relief=None, cage=.03, taches=0.0, taille_taches=8.0, ecailles=0.0):
    """Cuit la « peinture » du maillage dans une image (couleur × occlusion × dégradé + arêtes claires).
    2.31 : avec source (la sculpture de corps_haut), la peinture est lue sur la version détaillée (ombres fines des
    rides, des poils, des muscles) et une carte de relief (normal map) est cuite en plus ; le modèle exporté garde
    le même nombre de triangles. taches : marbrures de couleur (peau tachetée, pelage moucheté)."""
    _deplier(o)
    if source is not None:
        return _peindre_depuis(o, source, taille, occl, H, echantillons, sol, cime, grain, aretes, nom_img, relief,
                               taille_relief or taille, cage, taches, taille_taches, ecailles)
    sc = bpy.context.scene
    try: sc.render.engine = 'CYCLES'
    except TypeError: pass
    sc.cycles.samples = echantillons; sc.cycles.device = 'CPU'
    sc.cycles.use_denoising = False
    img = bpy.data.images.new(nom_img or (o.name + '_peinture'), taille, taille, alpha=False)
    img.colorspace_settings.name = 'sRGB'
    mat = bpy.data.materials.new('cuisson'); mat.use_nodes = True
    nt = mat.node_tree; N = nt.nodes; Lk = nt.links
    for n in list(N): N.remove(n)
    out = N.new('ShaderNodeOutputMaterial')
    em = N.new('ShaderNodeEmission')
    col = N.new('ShaderNodeVertexColor'); col.layer_name = 'Col'
    ao = N.new('ShaderNodeAmbientOcclusion'); ao.samples = 16; ao.inputs['Distance'].default_value = occl
    geo = N.new('ShaderNodeNewGeometry')
    tc = N.new('ShaderNodeTexCoord')
    sep = N.new('ShaderNodeSeparateXYZ')
    Lk.new(tc.outputs['Object'], sep.inputs[0])
    # dégradé vertical : sol → cime
    grad = N.new('ShaderNodeMapRange'); grad.inputs['From Min'].default_value = 0; grad.inputs['From Max'].default_value = H
    grad.inputs['To Min'].default_value = sol; grad.inputs['To Max'].default_value = cime
    Lk.new(sep.outputs['Z'], grad.inputs['Value'])
    # occlusion adoucie : .35 → 1
    aom = N.new('ShaderNodeMapRange'); aom.inputs['To Min'].default_value = .25; aom.inputs['To Max'].default_value = 1.05
    Lk.new(ao.outputs['AO'], aom.inputs['Value'])
    # arêtes (pointiness) : éclaircissement des bords saillants, assombrissement des creux
    ar = N.new('ShaderNodeMapRange'); ar.inputs['From Min'].default_value = .47; ar.inputs['From Max'].default_value = .58
    ar.inputs['To Min'].default_value = 1 - aretes * .6; ar.inputs['To Max'].default_value = 1 + aretes
    Lk.new(geo.outputs['Pointiness'], ar.inputs['Value'])
    # grain
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 60 / H; nz.inputs['Detail'].default_value = 4
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    gm = N.new('ShaderNodeMapRange'); gm.inputs['To Min'].default_value = 1 - grain; gm.inputs['To Max'].default_value = 1 + grain
    Lk.new(nz.outputs['Fac'], gm.inputs['Value'])
    def mul(a, b):
        m = N.new('ShaderNodeMix'); m.data_type = 'RGBA'; m.blend_type = 'MULTIPLY'; m.inputs['Factor'].default_value = 1
        Lk.new(a, m.inputs[6]); Lk.new(b, m.inputs[7]); return m.outputs[2]
    c = mul(col.outputs['Color'], aom.outputs['Result'])
    c = mul(c, grad.outputs['Result'])
    c = mul(c, ar.outputs['Result'])
    c = mul(c, gm.outputs['Result'])
    # lumière peinte venant du haut (faces tournées vers le ciel plus claires), comme les textures peintes à la main
    sepn = N.new('ShaderNodeSeparateXYZ'); Lk.new(geo.outputs['Normal'], sepn.inputs[0])
    hl = N.new('ShaderNodeMapRange'); hl.inputs['From Min'].default_value = -1; hl.inputs['From Max'].default_value = 1
    hl.inputs['To Min'].default_value = .72; hl.inputs['To Max'].default_value = 1.18
    Lk.new(sepn.outputs['Z'], hl.inputs['Value'])
    c = mul(c, hl.outputs['Result'])
    Lk.new(c, em.inputs['Color'])
    Lk.new(em.outputs[0], out.inputs['Surface'])
    tex = N.new('ShaderNodeTexImage'); tex.image = img; N.active = tex
    o.data.materials.clear(); o.data.materials.append(mat)
    # le squelette ne doit pas déformer la cuisson
    mods = [m for m in o.modifiers if m.type == 'ARMATURE']
    for m in mods: m.show_render = m.show_viewport = False
    for x in bpy.context.view_layer.objects: x.select_set(x == o)
    bpy.context.view_layer.objects.active = o
    with _ctx([o]): bpy.ops.object.bake(type='EMIT', margin=6, margin_type='EXTEND')
    for m in mods: m.show_render = m.show_viewport = True
    img.pack()
    # matériau final : l'image peinte, mate
    fin = bpy.data.materials.new('Peau'); fin.use_nodes = True
    p = next(n for n in fin.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    t2 = fin.node_tree.nodes.new('ShaderNodeTexImage'); t2.image = img
    fin.node_tree.links.new(t2.outputs['Color'], p.inputs['Base Color'])
    p.inputs['Roughness'].default_value = .8
    if 'Specular IOR Level' in p.inputs: p.inputs['Specular IOR Level'].default_value = .25
    o.data.materials.clear(); o.data.materials.append(fin)
    bpy.data.materials.remove(mat)
    if 'Col' in o.data.color_attributes: o.data.color_attributes.remove(o.data.color_attributes['Col'])
    return img

def _reseau_peinture(mat, occl, H, sol, cime, grain, aretes, taches, taille_taches, ecailles=0.0):
    """Réseau « émission » de la peinture (couleur des sommets × occlusion × dégradé × arêtes × grain × lumière du haut)."""
    nt = mat.node_tree; N = nt.nodes; Lk = nt.links
    for n in list(N): N.remove(n)
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    col = N.new('ShaderNodeVertexColor'); col.layer_name = 'Col'
    ao = N.new('ShaderNodeAmbientOcclusion'); ao.samples = 16; ao.inputs['Distance'].default_value = occl
    geo = N.new('ShaderNodeNewGeometry'); tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ')
    Lk.new(tc.outputs['Object'], sep.inputs[0])
    def rng(src, a, b, c, d):
        m = N.new('ShaderNodeMapRange'); m.inputs['From Min'].default_value = a; m.inputs['From Max'].default_value = b
        m.inputs['To Min'].default_value = c; m.inputs['To Max'].default_value = d; Lk.new(src, m.inputs['Value']); return m.outputs['Result']
    def mul(a, b):
        m = N.new('ShaderNodeMix'); m.data_type = 'RGBA'; m.blend_type = 'MULTIPLY'; m.inputs['Factor'].default_value = 1
        Lk.new(a, m.inputs[6]); Lk.new(b, m.inputs[7]); return m.outputs[2]
    c = col.outputs['Color']
    if taches:
        nt2 = N.new('ShaderNodeTexNoise'); nt2.inputs['Scale'].default_value = taille_taches / H; nt2.inputs['Detail'].default_value = 3
        Lk.new(tc.outputs['Object'], nt2.inputs['Vector'])
        c = mul(c, rng(nt2.outputs['Fac'], .35, .65, 1 - taches, 1 + taches * .6))
    if ecailles:   # 2.40 : motif d'écailles peint (cellules de Voronoï aux bords sombres) pour les reptiles
        vo = N.new('ShaderNodeTexVoronoi'); vo.feature = 'DISTANCE_TO_EDGE'; vo.inputs['Scale'].default_value = ecailles / H
        Lk.new(tc.outputs['Object'], vo.inputs['Vector'])
        c = mul(c, rng(vo.outputs['Distance'], .0, .09, .55, 1.06))
    c = mul(c, rng(ao.outputs['AO'], 0, 1, .22, 1.05))
    c = mul(c, rng(sep.outputs['Z'], 0, H, sol, cime))
    c = mul(c, rng(geo.outputs['Pointiness'], .47, .58, 1 - aretes * .6, 1 + aretes))
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 60 / H; nz.inputs['Detail'].default_value = 4
    Lk.new(tc.outputs['Object'], nz.inputs['Vector'])
    c = mul(c, rng(nz.outputs['Fac'], 0, 1, 1 - grain, 1 + grain))
    sepn = N.new('ShaderNodeSeparateXYZ'); Lk.new(geo.outputs['Normal'], sepn.inputs[0])
    c = mul(c, rng(sepn.outputs['Z'], -1, 1, .72, 1.18))
    Lk.new(c, em.inputs['Color']); Lk.new(em.outputs[0], out.inputs['Surface'])

def _peindre_depuis(o, src, taille, occl, H, echantillons, sol, cime, grain, aretes, nom_img, relief, taille_relief, cage,
                    taches, taille_taches, ecailles=0.0):
    sc = bpy.context.scene
    try: sc.render.engine = 'CYCLES'
    except TypeError: pass
    sc.cycles.samples = echantillons; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = False
    img = bpy.data.images.new(nom_img or (o.name + '_peinture'), taille, taille, alpha=False)
    img.colorspace_settings.name = 'sRGB'
    nimg = bpy.data.images.new(o.name + '_relief', taille_relief, taille_relief, alpha=False)
    nimg.colorspace_settings.name = 'Non-Color'
    # la sculpture porte le réseau de peinture ; le modèle léger porte l'image cible (nœud actif)
    mat = bpy.data.materials.new('cuisson'); mat.use_nodes = True
    _reseau_peinture(mat, occl, H, sol, cime, grain, aretes, taches, taille_taches, ecailles)
    src.data.materials.clear(); src.data.materials.append(mat)
    cible = bpy.data.materials.new('cible'); cible.use_nodes = True
    tex = cible.node_tree.nodes.new('ShaderNodeTexImage')
    o.data.materials.clear(); o.data.materials.append(cible)
    mods = [m for m in o.modifiers if m.type == 'ARMATURE']
    for m in mods: m.show_render = m.show_viewport = False
    b = sc.render.bake
    b.use_selected_to_active = True; b.cage_extrusion = cage; b.max_ray_distance = cage * 2.5; b.margin = 6
    for x in bpy.context.view_layer.objects: x.select_set(x in (o, src))
    bpy.context.view_layer.objects.active = o
    with _ctx([src, o], o):
        tex.image = img; cible.node_tree.nodes.active = tex
        bpy.ops.object.bake(type='EMIT', margin=6, margin_type='EXTEND')
        if relief:
            tex.image = nimg; cible.node_tree.nodes.active = tex
            bpy.ops.object.bake(type='NORMAL', normal_space='TANGENT', margin=6, margin_type='EXTEND')
    b.use_selected_to_active = False
    for m in mods: m.show_render = m.show_viewport = True
    img.pack()
    fin = bpy.data.materials.new('Peau'); fin.use_nodes = True
    nt = fin.node_tree; p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    t2 = nt.nodes.new('ShaderNodeTexImage'); t2.image = img; nt.links.new(t2.outputs['Color'], p.inputs['Base Color'])
    p.inputs['Roughness'].default_value = .8
    if 'Specular IOR Level' in p.inputs: p.inputs['Specular IOR Level'].default_value = .25
    if relief:
        nimg.pack()
        tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = nimg
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = relief
        nt.links.new(tn.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    else:
        bpy.data.images.remove(nimg)
    o.data.materials.clear(); o.data.materials.append(fin)
    bpy.data.materials.remove(mat); bpy.data.materials.remove(cible)
    if 'Col' in o.data.color_attributes: o.data.color_attributes.remove(o.data.color_attributes['Col'])
    me = src.data; bpy.data.objects.remove(src, do_unlink=True); bpy.data.meshes.remove(me)
    return img

def lueur(o, hexa):
    """Matériau émissif « Lueur_… » (yeux, runes) : le jeu le fait briller."""
    from .export_jeu import _materiau_lueur
    o.data.materials.clear(); o.data.materials.append(_materiau_lueur(lin(hexa)[:3]))
    if 'Col' in o.data.color_attributes: o.data.color_attributes.remove(o.data.color_attributes['Col'])

def finir(arm, H):
    """Met le modèle à la taille du jeu (H cases) : échelle appliquée au squelette et aux maillages."""
    arm.scale = (H, H, H)
    objs = [arm] + list(arm.children)
    with _ctx(objs, arm): bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# ------------------------------------------------------------------ animations sur os
FPS = 24

def clip(arm, nom, duree, pistes, boucle=True, n=None):
    """Une Action → une piste NLA « nom ». pistes :
      {(os, 'rot'|'loc', axe): f(phase 0..1) → valeur}      axes LOCAUX de l'os ;
      {(os, 'monde'): f(phase) → ((rx, ry, rz), (dx, dy, dz))}  rotation (radians) et déplacement dans les axes
      du MONDE (X à droite, Y vers l'arrière, Z vers le haut), autour de la tête de l'os : plus simple à écrire
      quand l'os est couché (dos d'un quadrupède) ou en biais."""
    bpy.context.scene.render.fps = FPS
    arm.animation_data_create()
    act = bpy.data.actions.new(f'{nom}_{arm.name}')
    arm.animation_data.action = act
    n = n or max(4, int(round(duree * FPS / 2)))
    for pb in arm.pose.bones:
        pb.rotation_euler = (0, 0, 0); pb.location = (0, 0, 0)
    ph_de = lambda i: 0.0 if (boucle and i == n) else i / n
    for cle, f in pistes.items():
        pb = arm.pose.bones.get(cle[0])
        if not pb: continue
        if cle[1] == 'monde':
            B = pb.bone.matrix_local.to_3x3(); Bi = B.inverted()
            for i in range(n + 1):
                r, d = f(ph_de(i))
                pb.rotation_euler = (Bi @ Euler(r, 'XYZ').to_matrix() @ B).to_euler('XYZ')
                pb.location = Bi @ Vector(d)
                fr = 1 + i / n * duree * FPS
                pb.keyframe_insert('rotation_euler', frame=fr); pb.keyframe_insert('location', frame=fr)
            pb.rotation_euler = (0, 0, 0); pb.location = (0, 0, 0)
            continue
        os_, ch, ax = cle
        chemin = 'rotation_euler' if ch == 'rot' else 'location'
        for i in range(n + 1):
            getattr(pb, chemin)[ax] = f(ph_de(i))
            pb.keyframe_insert(chemin, index=ax, frame=1 + i / n * duree * FPS)
        getattr(pb, chemin)[ax] = 0
    tr = arm.animation_data.nla_tracks.new(); tr.name = nom
    tr.strips.new(nom, 1, act)
    arm.animation_data.action = None
    return act

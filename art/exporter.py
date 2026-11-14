"""Export des modèles en GLB pour le jeu (assets/3d/).

Pour chaque modèle :
1. on le construit seul dans la scène ;
2. on « cuit » la couleur de chaque pièce dans ses sommets (couleur du matériau × peinture), puis
   toutes les pièces non lumineuses prennent un matériau unique « Peint » (un seul dessin par pièce fusionnée) ;
   les pièces lumineuses gardent un matériau « Lueur_<couleur> » (émissif) ;
3. on fusionne les pièces qui bougent ensemble (enfants directs d'un même pivot, par matériau) ;
4. on exporte en GLB avec les animations (une animation par piste NLA : « marche », « vol »).
L'optimisation (meshopt) est faite ensuite par tests/outils/optimiser-3d.js (glTF-Transform)."""
import bpy, os, math
import outils, tours_communes

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in dir() else None

def _couleur_base(m):
    p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    mx = next((n for n in m.node_tree.nodes if n.type == 'MIX'), None)
    c = mx.inputs[6].default_value if mx else p.inputs['Base Color'].default_value
    e = p.inputs['Emission Strength'].default_value if p else 0
    return tuple(c[:3]), e

def _materiau_peint():
    m = bpy.data.materials.get('Peint')
    if m: return m
    m = bpy.data.materials.new('Peint'); m.use_nodes = True
    nt = m.node_tree; p = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    ca = nt.nodes.new('ShaderNodeVertexColor'); ca.layer_name = 'Col'
    nt.links.new(ca.outputs[0], p.inputs['Base Color'])
    p.inputs['Roughness'].default_value = .75
    return m

def _materiau_lueur(rgb):
    nom = 'Lueur_%02x%02x%02x' % tuple(int(min(1, c) ** (1 / 2.2) * 255) for c in rgb)
    m = bpy.data.materials.get(nom)
    if m: return m
    m = bpy.data.materials.new(nom); m.use_nodes = True
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*rgb, 1)
    p.inputs['Emission Color'].default_value = (*rgb, 1)
    p.inputs['Emission Strength'].default_value = 1.0
    return m

def cuire(racine):
    """Couleur du matériau multipliée dans l'attribut Col ; matériau unique Peint ou Lueur."""
    peint = _materiau_peint()
    for o in outils.descendants(racine):
        if o.type != 'MESH' or not o.data.materials: continue
        me = o.data
        if o.data.users > 1: o.data = me = me.copy()
        if me.materials[0].name == 'Drapeau':  # recoloré par le jeu (couleur du joueur)
            if 'Col' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Col'])
            continue
        rgb, e = _couleur_base(me.materials[0])
        if e > 0:
            me.materials.clear(); me.materials.append(_materiau_lueur(rgb))
            if 'Col' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Col'])
            continue
        if 'Col' not in me.color_attributes:
            ca = me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
            for d in ca.data: d.color = (1, 1, 1, 1)
        ca = me.color_attributes['Col']
        for d in ca.data:
            c = d.color; d.color = (c[0] * rgb[0], c[1] * rgb[1], c[2] * rgb[2], 1)
        me.materials.clear(); me.materials.append(peint)

def fusionner(racine):
    """Fusionne, sous chaque pivot, les pièces maillées qui partagent un matériau."""
    groupes = {}
    for o in outils.descendants(racine):
        if o.type == 'MESH' and o.parent is not None and not o.children:
            groupes.setdefault((o.parent.name, o.data.materials[0].name), []).append(o)
    for (pnom, mnom), objs in groupes.items():
        if len(objs) < 2: continue
        bpy.ops.object.select_all(action='DESELECT')
        for o in objs: o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        objs[0].name = f'{pnom}_{"lueur" if mnom.startswith("Lueur") else "peint"}'

def exporter(racine, chemin):
    bpy.context.view_layer.update()
    cuire(racine); fusionner(racine)
    bpy.ops.object.select_all(action='DESELECT')
    for o in outils.descendants(racine): o.select_set(True)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    anim = any(o.animation_data and o.animation_data.nla_tracks for o in outils.descendants(racine))
    bpy.ops.export_scene.gltf(filepath=chemin, export_format='GLB', use_selection=True, export_yup=True, export_apply=True,
                              export_animations=anim, export_animation_mode='NLA_TRACKS', export_force_sampling=True,
                              export_vertex_color='NAME', export_vertex_color_name='Col', export_all_vertex_colors=False,
                              export_materials='EXPORT', export_image_format='NONE', export_extras=False)
    return outils.triangles(outils.descendants(racine))

# ---------------------------------------------------------------- liste complète
MONSTRES = ['sapeur_gobelin', 'warg', 'brute_orc', 'troll_glaces', 'golem_runique', 'cyclope_cendres', 'chauve_souris',
            'griffon_corrompu', 'dragon_ancien', 'chaman_guerre', 'pretresse', 'gelee_mutante', 'tortue', 'briseur_runes',
            'spectre', 'saboteur_gobelin', 'azhkhar', 'petit_limon']  # même ordre que CR dans sim.js

def tout(racine_depot, seulement=None):
    import importlib, sys
    sortie = os.path.join(racine_depot, 'art', '_brut')  # GLB bruts, optimisés ensuite vers assets/3d par art/optimiser.mjs
    res = []
    travaux = [(f'tours/{f}_{j}.glb', (lambda f=f, j=j: tours_communes.tour(f, j))) for f in tours_communes.FACTIONS for j in range(10)]
    travaux += [(f'monstres/{m}.glb', (lambda m=m: sys.modules[m].fabriquer())) for m in MONSTRES]
    import portail_chateau
    travaux += [('decor/portail.glb', portail_chateau.portail), ('decor/chateau.glb', portail_chateau.chateau)]
    for rel, fab in travaux:
        if seulement and not any(s in rel for s in seulement): continue
        outils.vider_scene()
        for m in list(bpy.data.materials):
            if m.users == 0: bpy.data.materials.remove(m)
        r = fab(); r.location = (0, 0, 0)
        n = exporter(r, os.path.join(sortie, rel))
        res.append((rel, n))
    return res

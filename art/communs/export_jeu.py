"""Préparation d'un modèle pour le jeu, appelée à la fin de chaque construire(ctx) (avant l'export par generer.py).

1. « Cuisson » : la couleur du matériau de chaque pièce est multipliée dans ses sommets (attribut Col, qui porte
   déjà la peinture : dégradé et grain) ; toutes les pièces non lumineuses prennent un matériau unique « Peint »
   qui lit cet attribut. Les pièces lumineuses gardent un matériau « Lueur_<couleur> » (émissif). Le matériau
   « Drapeau » est gardé tel quel (le jeu le recolore à la couleur du joueur).
2. Fusion : sous chaque pivot, les pièces qui partagent un matériau deviennent un seul maillage
   (une dizaine de pièces par modèle au lieu d'une centaine : beaucoup moins de dessins par image sur téléphone).
Les pivots (objets vides : Tourelle, Tete, BrasG…) et les animations (pistes NLA) sont conservés."""
import bpy
from . import outils

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
    peint = _materiau_peint()
    for o in outils.descendants(racine):
        if o.type != 'MESH' or not o.data.materials: continue
        me = o.data
        if me.users > 1: o.data = me = me.copy()
        # 2.40 : créatures « haute définition » (texture peinte « Peau ») et pièces déjà cuites (« Peint ») : rien à refaire
        if me.materials[0].name.startswith(('Peau', 'Peint')): continue
        if me.materials[0].name == 'Drapeau':
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
        for d in me.color_attributes['Col'].data:
            c = d.color; d.color = (c[0] * rgb[0], c[1] * rgb[1], c[2] * rgb[2], 1)
        me.materials.clear(); me.materials.append(peint)

def fusionner(racine):
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

def preparer(racine):
    """À appeler à la fin de construire(ctx), une fois le modèle complet (pièces, peinture, animations)."""
    bpy.context.view_layer.update()
    cuire(racine); fusionner(racine)
    racine.location = (0, 0, 0)
    return racine

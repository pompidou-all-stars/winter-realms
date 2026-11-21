"""Neige sur les modèles (thème « Winter Realms », depuis la 2.8).

enneiger(racine) pose une couche de neige sur les faces tournées vers le ciel (toits, créneaux, socles, plates-formes,
dômes, chapiteaux) : chaque face retenue est recopiée un peu au-dessus, légèrement rétrécie, en blanc bleuté. La neige
est une pièce à part (matériau « Neige »), rattachée au même pivot que la pièce enneigée : elle bouge avec elle et
export_jeu.preparer la fusionne avec ses voisines.

Ne reçoivent pas de neige : les personnages et les pièces animées (descendants de Tourelle, Corps, Tete, Bras…, Jambe…),
les pièces lumineuses (flammes, cristaux, runes) et les toutes petites faces. Le nombre de triangles ajoutés est plafonné
pour rester sous le budget du modèle (art/budgets.json) : les plus grandes faces passent en premier."""
import bpy, bmesh
from mathutils import Vector
from . import outils

COULEUR = '#eef4fb'
SEUIL_PENTE = .55       # composante verticale minimale de la normale (≈ 57° de pente au plus)
AIRE_MIN = .0012        # aire minimale d'une face enneigée (en cases²)
EPAISSEUR = .014        # hauteur de la couche au-dessus de la face
RETRAIT = .93           # la couche est un peu plus petite que la face (bord visible de la pièce)
PLAT = .85              # au-dessous, la face est une pente (toit, dôme)
RETRAIT_PENTE = .55     # sur une pente, la neige couvre la partie haute (55 % depuis le sommet)
EXCLUS = ('Tourelle', 'Corps', 'Tete', 'Bras', 'Jambe', 'Cristal', 'Eclats', 'Flamme', 'Orbe', 'Anneaux', 'Anneau', 'Servant', 'Arme', 'Dallage', 'SansNeige')  # Dallage (2.40) : sol de pierre laissé visible ; SansNeige (2.40) : eau, braises, intérieurs

def _exclu(o):
    p = o.parent
    while p is not None:
        if p.type == 'EMPTY' and p.name.split('.')[0].startswith(EXCLUS): return True
        p = p.parent
    return False

def _lumineux(o):
    for m in o.data.materials:
        n = next((x for x in m.node_tree.nodes if x.type == 'BSDF_PRINCIPLED'), None) if m and m.use_nodes else None
        if n and n.inputs['Emission Strength'].default_value > 0: return True
    return False

def enneiger(racine, budget=2990):
    """Ajoute la neige ; budget = nombre total de triangles à ne pas dépasser pour le modèle."""
    bpy.context.view_layer.update()
    objs = [o for o in outils.descendants(racine) if o.type == 'MESH' and o.data.materials and not _exclu(o) and not _lumineux(o)]
    reste = budget - outils.triangles(outils.descendants(racine))
    if reste <= 0: return 0
    faces = []  # (aire, objet, sommets du monde, normale du monde)
    for o in objs:
        mw = o.matrix_world; nmat = mw.to_3x3().inverted_safe().transposed()
        for p in o.data.polygons:
            n = (nmat @ p.normal).normalized()
            if n.z < SEUIL_PENTE: continue
            pts = [mw @ o.data.vertices[i].co for i in p.vertices]
            # aire dans le monde (somme des triangles en éventail)
            aire = sum(((pts[i] - pts[0]).cross(pts[i + 1] - pts[0])).length / 2 for i in range(1, len(pts) - 1))
            if aire < AIRE_MIN: continue
            faces.append((aire, o, pts, n))
    faces.sort(key=lambda f: -f[0])
    par_parent, ajout = {}, 0
    for aire, o, pts, n in faces:
        t = len(pts) - 2
        if ajout + t > reste: continue
        ajout += t; par_parent.setdefault(o.parent, []).append((pts, n))
    mat = outils.mat(COULEUR, rough=.9)
    for parent, liste in par_parent.items():
        bm = bmesh.new()
        for pts, n in liste:
            if n.z < PLAT:
                # pente (toit, dôme) : la neige part du sommet et n'en couvre que le haut, l'avant-toit garde sa couleur
                c = max(pts, key=lambda q: q.z); k = RETRAIT_PENTE
            else:
                c = sum(pts, Vector()) / len(pts); k = RETRAIT
            vs = [bm.verts.new(c + (q - c) * k + n * EPAISSEUR + Vector((0, 0, EPAISSEUR * .5))) for q in pts]
            try: bm.faces.new(vs)
            except ValueError: pass
        me = bpy.data.meshes.new('Neige'); bm.to_mesh(me); bm.free()
        me.materials.append(mat)
        # peinture des sommets (attribut Col lu par le matériau) : blanc, à peine ombré sur les bords
        ca = me.color_attributes.new('Col', 'BYTE_COLOR', 'CORNER')
        for i, d in enumerate(ca.data): v = 1 - .04 * (i % 3 == 0); d.color = (v, v, v, 1)
        ob = bpy.data.objects.new('Neige', me)
        (racine.users_collection[0] if racine.users_collection else bpy.context.scene.collection).objects.link(ob)
        # sommets calculés dans le monde : on rattache au pivot en gardant la place
        ob.parent = parent
        if parent is not None: ob.matrix_parent_inverse = parent.matrix_world.inverted()
        for poly in me.polygons: poly.use_smooth = False
    return ajout

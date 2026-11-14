"""Rendus de validation (EEVEE) : éclairage doux de maquette, caméra orthographique."""
import bpy, math
from mathutils import Vector
from .outils import lin

def studio(fond='#3b4a52'):
    sc = bpy.context.scene
    for o in list(bpy.data.objects):
        if o.type in ('LIGHT', 'CAMERA'): bpy.data.objects.remove(o, do_unlink=True)
    w = sc.world or bpy.data.worlds.new('Monde'); sc.world = w; w.use_nodes = True
    bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs[0].default_value = lin(fond); bg.inputs[1].default_value = 1.0
    soleil = bpy.data.lights.new('Soleil', 'SUN'); soleil.energy = 4.2; soleil.angle = math.radians(12); soleil.color = (1, .95, .86)
    so = bpy.data.objects.new('Soleil', soleil); sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(42), math.radians(-18), math.radians(-35))
    ciel = bpy.data.lights.new('Ciel', 'SUN'); ciel.energy = .9; ciel.use_shadow = False; ciel.color = (.7, .82, 1)
    co = bpy.data.objects.new('Ciel', ciel); sc.collection.objects.link(co); co.rotation_euler = (math.radians(-50), 0, math.radians(150))
    # lumière de contour (arrière), pour détacher les silhouettes du sol
    rim = bpy.data.lights.new('Contour', 'SUN'); rim.energy = 2.2; rim.use_shadow = False; rim.color = (1, .9, .75)
    ro = bpy.data.objects.new('Contour', rim); sc.collection.objects.link(ro); ro.rotation_euler = (math.radians(-65), 0, math.radians(10))
    try: sc.eevee.use_shadows = True
    except Exception: pass
    sc.view_settings.view_transform = 'Standard' if 'Standard' in [i.identifier for i in type(sc.view_settings).bl_rna.properties['view_transform'].enum_items] else sc.view_settings.view_transform
    sc.render.film_transparent = False

def camera(cible, direction, echelle, nom='Cam'):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new(nom); cd.type = 'ORTHO'; cd.ortho_scale = echelle; cd.clip_end = 200
    c = bpy.data.objects.new(nom, cd); sc.collection.objects.link(c)
    d = Vector(direction).normalized(); c.location = Vector(cible) + d * 30
    c.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = c; return c

def rendre(chemin, l=1024, h=1024, echantillons=32):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = l, h, 100
    try: sc.eevee.taa_render_samples = echantillons
    except Exception: pass
    sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = chemin
    bpy.ops.render.render(write_still=True)

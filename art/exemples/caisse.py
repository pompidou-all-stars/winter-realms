"""Exemple minimal d'asset (non utilisé par le jeu) : une caisse en bois aux couleurs de l'Alliance.
Sert de modèle pour écrire un nouveau script et de témoin pour vérifier la chaîne de génération."""
INFOS = {'categorie': 'exemple', 'titre': 'Caisse de démonstration'}

def construire(ctx):
    bpy = ctx.bpy
    or_alliance = ctx.jeu['FACTIONS'][0]['color'] if ctx.jeu else '#d8b45c'
    bois = ctx.materiau('bois', '#8a5a2c')
    ferrure = ctx.materiau('ferrure', or_alliance, rugosite=0.35, metal=0.6)
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 0, 0.3))
    ctx.habiller(ctx.biseau(bpy.context.object, 0.04), bois)
    for z in (0.08, 0.52):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z))
        cercle = bpy.context.object; cercle.scale = (0.62, 0.62, 0.05)
        ctx.habiller(ctx.biseau(cercle, 0.01, 2), ferrure)

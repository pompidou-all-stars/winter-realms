"""Planches de validation : toutes les tours d'une faction, ou tous les monstres, côte à côte.
Usage dans Blender (après atelier.py) : planches.tours('horde', chemin_png) ; planches.monstres(chemin_png)."""
import bpy
import outils, rendu, tours_communes

def tours(faction, chemin, l=2000, h=620):
    outils.vider_scene()
    for j in range(10):
        t = tours_communes.tour(faction, j); t.location = (j * 1.05, 0, 0)
    rendu.studio()
    rendu.camera((4.72, 0, .6), (.35, -1.6, .75), 10.6)
    rendu.rendre(chemin, l, h, 32)

def monstres(liste, chemin, l=2000, h=700, ecart=.75):
    outils.vider_scene()
    x = 0
    for mod in liste:
        m = mod.fabriquer(); m.location = (x, 0, 0); x += ecart
    bpy.context.scene.frame_set(4)
    rendu.studio()
    rendu.camera(((x - ecart) / 2, 0, .3), (.3, -1.6, .6), x * .98)
    rendu.rendre(chemin, l, h, 48)

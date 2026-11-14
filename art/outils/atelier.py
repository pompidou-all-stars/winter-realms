"""Atelier de conception dans un Blender OUVERT (MCP) : recharge les pièces communes après chaque retouche
et construit un asset dans la scène, sans exporter (l'export définitif passe par generer.py).

Dans Blender (onglet Script, ou via le MCP) :
    exec(open(r'<dépôt>\\art\\outils\\atelier.py', encoding='utf-8').read())
    atelier_asset('tours/alliance-0')          # construit la tour dans la scène (sans préparation pour le jeu)
    atelier_asset('monstres/orc', jeu=True)    # … avec la préparation pour le jeu (couleurs cuites, pièces fusionnées)
    planches.tours('horde', r'C:\\…\\horde.png')  # planche de validation (voir planches.py)
"""
import sys, os, importlib, importlib.util, types
try: ART
except NameError: ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') if '__file__' in dir() else None
ART = os.path.abspath(ART if not ART.endswith('outils') else os.path.join(ART, '..'))
for _p in (ART, os.path.join(ART, 'outils')):
    if _p not in sys.path: sys.path.insert(0, _p)
import bpy
# ordre de rechargement : les modules de base d'abord (les autres importent leurs fonctions)
for _n in ['outils', 'echelles', 'animations', 'factions', 'personnages', 'betes', 'tours_communes', 'decor', 'export_jeu', 'rendu']:
    _m = sys.modules.get('communs.' + _n)
    _m = importlib.reload(_m) if _m else importlib.import_module('communs.' + _n)
    globals()[_n] = _m
planches = importlib.reload(sys.modules['planches']) if 'planches' in sys.modules else importlib.import_module('planches')

def charger_asset(id_):
    """Module Python du script d'asset art/<id_>.py (rechargé à chaque appel)."""
    spec = importlib.util.spec_from_file_location('asset_' + id_.replace('/', '_').replace('-', '_'), os.path.join(ART, id_ + '.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def atelier_asset(id_, jeu=False):
    """Construit l'asset dans la scène ouverte. jeu=False : sans la préparation pour le jeu (pratique pour retoucher)."""
    mod = charger_asset(id_)
    ctx = types.SimpleNamespace(bpy=bpy, jeu={})
    if jeu or not hasattr(mod, 'fabriquer'):
        avant = set(bpy.data.objects)
        if not jeu:
            ancien = export_jeu.preparer; export_jeu.preparer = lambda r: r
            try: mod.construire(ctx)
            finally: export_jeu.preparer = ancien
        else: mod.construire(ctx)
        neufs = [o for o in bpy.data.objects if o not in avant and o.parent is None]
        return neufs[0] if neufs else None
    return mod.fabriquer()

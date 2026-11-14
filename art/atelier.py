"""Point d'entrée commun : rend tous les modules de art/ importables et les recharge (pratique pendant
qu'on retouche un modèle dans un Blender ouvert). Usage dans Blender :
    exec(open(r'<dépôt>/art/atelier.py', encoding='utf-8').read())
puis les modules sont disponibles sous leur nom (outils, factions, alliance_0_archers…)."""
import sys, os, importlib
ART = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else ART
for _d in ('communs', 'tours', 'monstres', 'decor'):
    _p = os.path.join(ART, _d)
    if _p not in sys.path: sys.path.insert(0, _p)
_noms = []
for _d in ('communs', 'decor', 'tours', 'monstres'):
    for _f in sorted(os.listdir(os.path.join(ART, _d))):
        if _f.endswith('.py'): _noms.append(_f[:-3])
# ordre de rechargement : les modules de base d'abord (les autres importent leurs fonctions)
_base = ['outils', 'echelles', 'animations', 'factions', 'personnages', 'betes', 'tours_communes', 'rendu']
_noms = [n for n in _base if n in _noms] + [n for n in _noms if n not in _base]
if ART not in sys.path: sys.path.insert(0, ART)
_noms += [_f[:-3] for _f in sorted(os.listdir(ART)) if _f.endswith('.py') and _f != 'atelier.py']
for _n in _noms:
    _m = sys.modules.get(_n)
    globals()[_n] = importlib.reload(_m) if _m else importlib.import_module(_n)

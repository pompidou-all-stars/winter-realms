"""Winter Realms — génération des assets 3D à partir des scripts de art/.

Chaque asset est un script Python de art/ (hors art/outils/ et art/communs/) qui définit :
    INFOS = {'categorie': 'tour' | 'monstre' | 'decor' | 'exemple', 'titre': '…'}
    def construire(ctx): …   # crée ses objets dans une scène vide

Ce programme vide la scène, appelle construire(ctx), exporte le résultat en GLB dans assets/3d/<id>.glb
et tient à jour assets/3d/manifeste.json (taille, triangles, empreinte du script source).

Utilisation (mêmes résultats sur le PC et dans le cloud, avec Blender 5.3) :
  - module Python bpy (cloud, GitHub) :  python art/outils/generer.py [ids…] [options]
  - Blender installé (PC) :               blender --background --python art/outils/generer.py -- [ids…] [options]
Options :
  --tout            régénère tous les assets (par défaut si aucun id n'est donné)
  --verifier        régénère dans un dossier temporaire et vérifie : scripts qui s'exécutent, budgets,
                    manifeste à jour (aucun fichier n'est modifié) ; code de sortie 1 en cas de problème
  --apercus DOSSIER rend aussi une image d'aperçu PNG par asset dans DOSSIER
Ne pas lancer depuis la scène Blender ouverte (MCP) : le programme vide la scène.
"""
import sys, os, json, hashlib, importlib.util, tempfile, subprocess, math

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ART = os.path.join(RACINE, 'art')
SORTIE = os.path.join(RACINE, 'assets', '3d')
MANIFESTE = os.path.join(SORTIE, 'manifeste.json')
BUDGETS = os.path.join(ART, 'budgets.json')
VERSION_BLENDER = '5.3'

def lire(chemin):
    with open(chemin, 'rb') as f:
        return f.read().decode('utf-8').replace('\r\n', '\n')

def scripts_assets():
    """ids des assets : chemins relatifs à art/, sans .py (ex. « tours/alliance-0 »)."""
    ids = []
    for dossier, sous, fichiers in os.walk(ART):
        rel = os.path.relpath(dossier, ART).replace('\\', '/')
        if rel.split('/')[0] in ('outils', 'communs', '__pycache__'):
            continue
        for f in fichiers:
            if f.endswith('.py') and not f.startswith('_'):
                ids.append(((rel + '/') if rel != '.' else '') + f[:-3])
    return sorted(ids)

def empreinte(id_):
    """Empreinte de la « recette » d'un asset : son script + tous les fichiers de art/communs/.
    Même calcul que tests/simulation/assets3d.test.js : ne pas changer l'un sans l'autre."""
    h = hashlib.sha256()
    h.update(('script:' + lire(os.path.join(ART, id_ + '.py'))).encode('utf-8'))
    communs = os.path.join(ART, 'communs')
    if os.path.isdir(communs):
        for f in sorted(x for x in os.listdir(communs) if x.endswith('.py')):
            h.update(('\n--communs/' + f + '\n' + lire(os.path.join(communs, f))).encode('utf-8'))
    return h.hexdigest()

def tables_du_jeu():
    """Les tables de sim.js (couleurs des factions, tours, monstres), pour paramétrer les modèles."""
    try:
        sortie = subprocess.run(['node', '-e',
            "const S=require('./sim.js');console.log(JSON.stringify({FACTIONS:S.FACTIONS,TW:S.TW,CR:S.CR}))"],
            cwd=RACINE, capture_output=True, text=True, check=True).stdout
        return json.loads(sortie)
    except Exception as e:
        print('⚠️ Tables du jeu indisponibles (Node.js manquant ?) :', e)
        return {}

class Contexte:
    """Outils mis à disposition des scripts d'assets."""
    def __init__(self, bpy, jeu):
        self.bpy, self.jeu = bpy, jeu
    def couleur(self, hexa):
        """'#d8b45c' → (r, g, b) linéaire, comme Blender l'attend."""
        hexa = hexa.lstrip('#')
        srgb = [int(hexa[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb)
    def materiau(self, nom, couleur, rugosite=0.7, metal=0.0):
        m = self.bpy.data.materials.get(nom) or self.bpy.data.materials.new(nom)
        m.use_nodes = True
        b = m.node_tree.nodes['Principled BSDF']
        rgb = self.couleur(couleur) if isinstance(couleur, str) else couleur
        b.inputs['Base Color'].default_value = (*rgb, 1)
        b.inputs['Roughness'].default_value = rugosite
        b.inputs['Metallic'].default_value = metal
        return m
    def biseau(self, obj, largeur=0.03, segments=3):
        mod = obj.modifiers.new('biseau', 'BEVEL'); mod.width = largeur; mod.segments = segments
        return obj
    def habiller(self, obj, materiau, lisse=True):
        obj.data.materials.append(materiau)
        if lisse:
            for p in obj.data.polygons:
                p.use_smooth = True
        return obj

def charger_bpy():
    try:
        import bpy
        return bpy
    except ImportError:
        print('Blender introuvable. Dans le cloud : pip install bpy==5.3.0 ; sur le PC : '
              'blender --background --python art/outils/generer.py -- …')
        sys.exit(2)

def generer(bpy, id_, dossier, jeu, apercus=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    spec = importlib.util.spec_from_file_location('asset_' + id_.replace('/', '_').replace('-', '_'), os.path.join(ART, id_ + '.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, ART)
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    infos = getattr(mod, 'INFOS', {})
    mod.construire(Contexte(bpy, jeu))
    maillages = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not maillages:
        raise RuntimeError('le script n\'a créé aucun objet')
    dg = bpy.context.evaluated_depsgraph_get()
    triangles = 0
    for o in maillages:
        ev = o.evaluated_get(dg); me = ev.to_mesh(); me.calc_loop_triangles(); triangles += len(me.loop_triangles); ev.to_mesh_clear()
    fichier = os.path.join(dossier, id_ + '.glb')
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    for o in bpy.context.scene.objects:
        o.select_set(o.type == 'MESH')
    bpy.ops.export_scene.gltf(filepath=fichier, export_format='GLB', use_selection=True, export_apply=True,
                              export_cameras=False, export_lights=False)
    if apercus:
        rendre_apercu(bpy, maillages, os.path.join(apercus, id_.replace('/', '-') + '.png'))
    return {'id': id_, 'categorie': infos.get('categorie', 'exemple'), 'titre': infos.get('titre', id_),
            'fichier': 'assets/3d/' + id_ + '.glb', 'triangles': triangles, 'octets': os.path.getsize(fichier),
            'empreinte_source': empreinte(id_), 'blender': VERSION_BLENDER}

def rendre_apercu(bpy, maillages, chemin):
    sc = bpy.context.scene
    pts = [o.matrix_world @ v.co for o in maillages for v in o.data.vertices]  # coordonnées dans la scène
    mini = [min(p[i] for p in pts) for i in range(3)]
    maxi = [max(p[i] for p in pts) for i in range(3)]
    centre = [(a + b) / 2 for a, b in zip(mini, maxi)]; taille = max(b - a for a, b in zip(mini, maxi)) or 1
    bpy.ops.object.light_add(type='SUN'); soleil = bpy.context.object; soleil.data.energy = 3
    soleil.rotation_euler = (math.radians(50), 0, math.radians(35))
    monde = bpy.data.worlds.new('apercu'); sc.world = monde; monde.use_nodes = True
    monde.node_tree.nodes['Background'].inputs[0].default_value = (0.55, 0.62, 0.7, 1)
    bpy.ops.object.empty_add(location=centre); cible = bpy.context.object
    d = taille * 2.2
    bpy.ops.object.camera_add(location=(centre[0] + d * 0.6, centre[1] - d * 0.75, centre[2] + d * 0.65)); cam = bpy.context.object
    c = cam.constraints.new('TRACK_TO'); c.target = cible; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    sc.camera = cam; sc.render.engine = 'CYCLES'; sc.cycles.samples = 24; sc.cycles.device = 'CPU'
    sc.render.resolution_x = sc.render.resolution_y = 400; sc.render.filepath = chemin
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    bpy.ops.render.render(write_still=True)

def budgets():
    with open(BUDGETS, encoding='utf-8') as f:
        return json.load(f)

def controler(entree, b):
    lim = b.get(entree['categorie'])
    if not lim:
        return ['catégorie inconnue « %s » (voir art/budgets.json)' % entree['categorie']]
    p = []
    if entree['triangles'] > lim['triangles']:
        p.append('%d triangles (budget %d)' % (entree['triangles'], lim['triangles']))
    if entree['octets'] > lim['octets']:
        p.append('%d octets (budget %d)' % (entree['octets'], lim['octets']))
    return p

def main(args):
    verifier = '--verifier' in args
    apercus = args[args.index('--apercus') + 1] if '--apercus' in args else None
    demandes = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--apercus')]
    tous = scripts_assets()
    ids = tous if (not demandes or '--tout' in args or verifier) else demandes
    for i in ids:
        if i not in tous:
            print('❌ Asset inconnu : %s (scripts disponibles : %s)' % (i, ', '.join(tous))); return 1
    bpy = charger_bpy(); jeu = tables_du_jeu(); b = budgets()
    manifeste = {'blender': VERSION_BLENDER, 'assets': {}}
    if os.path.exists(MANIFESTE):
        with open(MANIFESTE, encoding='utf-8') as f:
            manifeste = json.load(f)
    dossier = tempfile.mkdtemp(prefix='wr-assets-') if verifier else SORTIE
    problemes = []
    for i in ids:
        try:
            e = generer(bpy, i, dossier, jeu, apercus)
        except Exception as err:
            problemes.append('%s : le script échoue (%s)' % (i, err)); continue
        for p in controler(e, b):
            problemes.append('%s : hors budget, %s' % (i, p))
        print('✅ %s : %d triangles, %.1f Ko' % (i, e['triangles'], e['octets'] / 1024))
        if verifier:
            ref = manifeste['assets'].get(i)
            if not ref:
                problemes.append('%s : absent du manifeste (lancer la génération puis commiter assets/3d/)' % i)
            elif ref['empreinte_source'] != e['empreinte_source']:
                problemes.append('%s : le script a changé mais le fichier 3D n\'a pas été régénéré' % i)
            elif not os.path.exists(os.path.join(RACINE, ref['fichier'])):
                problemes.append('%s : fichier %s manquant' % (i, ref['fichier']))
        else:
            manifeste['assets'][i] = e
    if verifier:
        for i in manifeste['assets']:
            if i not in tous:
                problemes.append('%s : présent dans le manifeste mais son script n\'existe plus' % i)
    else:
        manifeste['assets'] = {k: v for k, v in sorted(manifeste['assets'].items()) if k in tous}
        manifeste['blender'] = VERSION_BLENDER
        total = sum(v['octets'] for v in manifeste['assets'].values())
        if total > b['total_octets']:
            problemes.append('total %d octets (budget %d)' % (total, b['total_octets']))
        os.makedirs(SORTIE, exist_ok=True)
        with open(MANIFESTE, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(manifeste, f, ensure_ascii=False, indent=1); f.write('\n')
    for p in problemes:
        print('❌ ' + p)
    print(('❌ %d problème(s)' % len(problemes)) if problemes else '✅ Assets 3D : tout est en ordre')
    return 1 if problemes else 0

if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    sys.exit(main(argv))

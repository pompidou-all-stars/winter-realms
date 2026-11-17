"""Répliques des 5 factions de Winter Realms, générées en local avec Chatterbox Multilingual (Resemble AI, licence MIT).

Les textes viennent de assets/audio/catalogue.json (« repliques »). Le timbre de chaque faction vient :
  - d'un enregistrement de référence art/sons/voix/<faction>.wav (10 à 20 s de voix claire), s'il existe ;
  - sinon de la voix par défaut du modèle, transformée (hauteur, écho) selon le profil ci-dessous.
Chaque réplique a une graine fixe : relancer le script redonne la même prise.

Usage (environnement Python « voix-env », voir art/sons/LISEZMOI.md) :
  python art/sons/voix.py [motif ...] [--sortie DOSSIER] [--remplacer]
    motif : « nains », « horde-sel », « legion-impossible »…
"""
import argparse, hashlib, json, random, sys, time
from pathlib import Path

try:  # certificats du système (proxys, antivirus qui inspectent HTTPS) pour le téléchargement des modèles
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass

import numpy as np
import soundfile as sf
import torch
import torchaudio.functional as AF

RAC = Path(__file__).resolve().parents[2]
CAT = RAC / "assets" / "audio" / "catalogue.json"
REF = Path(__file__).resolve().parent / "voix"

# exaggeration : intensité de l'émotion ; cfg : fidélité au texte et rythme (bas = plus lent, plus posé)
# demi_tons : hauteur appliquée après génération ; echo : (retard s, gain) pour une voix d'outre-tombe
PROFILS = {
    "alliance":   dict(exaggeration=0.6, cfg=0.5, demi_tons=-2, echo=None),
    "horde":      dict(exaggeration=0.9, cfg=0.4, demi_tons=-5, echo=None),
    "sylvestres": dict(exaggeration=0.4, cfg=0.5, demi_tons=+1, echo=(0.09, 0.25)),
    "nains":      dict(exaggeration=0.8, cfg=0.45, demi_tons=-4, echo=None),
    "legion":     dict(exaggeration=0.5, cfg=0.3, demi_tons=-6, echo=(0.13, 0.4)),
}


def graine(i, n):
    return int(hashlib.sha1(f"{i}#{n}".encode()).hexdigest()[:8], 16)


def fixer_graine(g):
    random.seed(g); np.random.seed(g % 2**32); torch.manual_seed(g); torch.cuda.manual_seed_all(g)


def transformer(w, sr, p):
    if p["demi_tons"]:
        w = AF.pitch_shift(w, sr, p["demi_tons"])
    a = w.squeeze(0).cpu().numpy().astype(np.float32)
    if p["echo"]:
        d, g = p["echo"]; k = int(sr * d)
        b = np.concatenate([a, np.zeros(k * 3, np.float32)])
        for i in (1, 2, 3): b[k * i:k * i + len(a)] += a * g ** i
        a = b
    seuil = 10 ** (-45 / 20) * np.abs(a).max()
    idx = np.nonzero(np.abs(a) > seuil)[0]
    if len(idx): a = a[max(0, idx[0] - int(sr * .03)): idx[-1] + int(sr * .08)]
    return a * (10 ** (-3 / 20) / max(1e-9, np.abs(a).max()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("motifs", nargs="*")
    ap.add_argument("--sortie", default=str(RAC / "assets" / "audio"))
    ap.add_argument("--remplacer", action="store_true")
    o = ap.parse_args()
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    taches = [(f, c, n, t) for f, ctx in cat["repliques"].items() for c, l in ctx.items() for n, t in enumerate(l, 1)
              if not o.motifs or any(m in f"{f}-{c}" for m in o.motifs)]
    if not taches: sys.exit("Aucune réplique ne correspond.")
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m = ChatterboxMultilingualTTS.from_pretrained(device=torch.device("cuda"))
    total = 0
    for f, c, n, texte in taches:
        i = f"voix-{f}-{c}"
        dest = Path(o.sortie) / "voix" / f / f"{i}-{n}.mp3"
        if dest.exists() and not o.remplacer: continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        p, ref = PROFILS[f], REF / f"{f}.wav"
        t = time.time(); fixer_graine(graine(i, n))
        w = m.generate(texte, language_id="fr", audio_prompt_path=str(ref) if ref.exists() else None,
                       exaggeration=p["exaggeration"], cfg_weight=p["cfg"])
        sf.write(dest, transformer(w, m.sr, p), m.sr, format="MP3")
        total += 1
        print(f"✓ voix/{f}/{dest.name}  « {texte} »  ({time.time() - t:.1f} s)", flush=True)
    print(f"{total} répliques générées.")


if __name__ == "__main__":
    main()

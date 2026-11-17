"""Bruitages et ambiances de Winter Realms, générés en local avec Stable Audio Open 1.0 (Stability AI).

La consigne, la durée et le nombre de variantes de chaque son viennent de assets/audio/catalogue.json.
Chaque variante a une graine fixe (dérivée de l'identifiant et du numéro) : relancer le script redonne le même son.

Usage (environnement Python « sons-env », voir art/sons/LISEZMOI.md) :
  python art/sons/bruitages.py [motif ...] [--sortie DOSSIER] [--remplacer] [--pas 100]
    motif       : ne génère que les sons dont l'identifiant contient ce texte (ex. « tir-arrow », « boom »)
    --sortie    : dossier de sortie (par défaut assets/audio) ; un essai peut aller ailleurs
    --remplacer : régénère aussi les variantes déjà présentes
    --pas       : nombre de pas de diffusion (qualité / vitesse), 100 par défaut

Licence du modèle : Stability AI Community License (usage commercial gratuit sous 1 M$ de chiffre d'affaires annuel).
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

try:  # certificats du système (proxys, antivirus qui inspectent HTTPS) pour le téléchargement des modèles
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass

import numpy as np
import soundfile as sf
import torch
from diffusers import StableAudioPipeline

RAC = Path(__file__).resolve().parents[2]
CAT = RAC / "assets" / "audio" / "catalogue.json"
NEGATIF = "music, melody, speech, voice, talking, low quality, distorted, clipping, noise, hum"


def dossier(i):
    if i.startswith("tir-"): return "tours"
    if i.split("-")[0] in ("chantier", "fini", "up"): return "construction"
    if i.split("-")[0] in ("mort", "arrivee"): return "monstres"
    if i.startswith("amb-"): return "ambiances"
    return "interface"


def graine(i, n):
    return int(hashlib.sha1(f"{i}#{n}".encode()).hexdigest()[:8], 16)


def finir(audio, sr, boucle):
    """Mono, silence final coupé (sauf boucles), crête ramenée à -3 dB, fondu de sortie de 30 ms."""
    a = audio.mean(axis=0) if audio.ndim == 2 else audio
    if not boucle:
        seuil = 10 ** (-50 / 20) * max(1e-9, np.abs(a).max())
        idx = np.nonzero(np.abs(a) > seuil)[0]
        if len(idx): a = a[: min(len(a), idx[-1] + int(sr * 0.05))]
        f = min(len(a), int(sr * 0.03))
        a[-f:] *= np.linspace(1, 0, f)
    pk = np.abs(a).max()
    if pk > 0: a = a * (10 ** (-3 / 20) / pk)
    return a.astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("motifs", nargs="*")
    ap.add_argument("--sortie", default=str(RAC / "assets" / "audio"))
    ap.add_argument("--remplacer", action="store_true")
    ap.add_argument("--pas", type=int, default=100)
    o = ap.parse_args()
    cat = json.loads(CAT.read_text(encoding="utf-8"))
    sons = [s for s in cat["sons"] if not o.motifs or any(m in s["id"] for m in o.motifs)]
    if not sons: sys.exit("Aucun son ne correspond.")
    pipe = StableAudioPipeline.from_pretrained("stabilityai/stable-audio-open-1.0", torch_dtype=torch.float16).to("cuda")
    sr = pipe.vae.sampling_rate
    total = 0
    for s in sons:
        for n in range(1, s["n"] + 1):
            dest = Path(o.sortie) / dossier(s["id"]) / f"{s['id']}-{n}.mp3"
            if dest.exists() and not o.remplacer: continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            t = time.time()
            g = torch.Generator("cuda").manual_seed(graine(s["id"], n))
            # le modèle produit mal les sons très courts : on génère au moins 2 s puis on coupe le silence
            out = pipe(s["p"], negative_prompt=NEGATIF, num_inference_steps=o.pas,
                       audio_end_in_s=max(2.0, s["dur"]), num_waveforms_per_prompt=1, generator=g).audios[0]
            a = out.float().cpu().numpy()
            if not s.get("loop"): a = a[:, : int(sr * max(s["dur"], 0.4) * 1.5)]
            sf.write(dest, finir(a, sr, s.get("loop")), sr, format="MP3")
            total += 1
            print(f"✓ {dest.relative_to(Path(o.sortie)).as_posix()}  ({time.time() - t:.1f} s)", flush=True)
    print(f"{total} fichiers générés.")


if __name__ == "__main__":
    main()

"""Répliques des 5 factions de Winter Realms, générées en local avec Chatterbox Multilingual (Resemble AI, licence MIT).

Les textes viennent de assets/audio/catalogue.json (« repliques »). Le timbre de chaque faction vient :
  - d'un enregistrement de référence art/sons/voix/<faction>.wav (10 à 20 s de voix claire), s'il existe ;
  - sinon de la voix par défaut du modèle, transformée (hauteur, écho) selon le profil ci-dessous.
Chaque réplique a une graine fixe : relancer le script redonne la même prise.

Usage (environnement Python « voix-env », voir art/sons/LISEZMOI.md) :
  python art/sons/voix.py [motif ...] [--sortie DOSSIER] [--remplacer]
    motif : « nains », « horde-sel », « legion-impossible »…
"""
import argparse, difflib, hashlib, json, random, re, sys, time, unicodedata
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
# Esprit validé par le concepteur (« Grrr… On cogne qui ? ») : jeu caricatural et drôle, émotion forte.
# Pas de transformation après coup (hauteur, écho) : elle rendait les voix robotiques ; le timbre viendra
# d'un enregistrement de référence par faction (art/sons/voix/<faction>.wav).
PROFILS = {
    "alliance":   dict(exaggeration=0.85, cfg=0.4, demi_tons=0, echo=None),
    "horde":      dict(exaggeration=1.0, cfg=0.35, demi_tons=0, echo=None),
    "sylvestres": dict(exaggeration=0.75, cfg=0.4, demi_tons=0, echo=None),
    "nains":      dict(exaggeration=0.95, cfg=0.35, demi_tons=0, echo=None),
    "legion":     dict(exaggeration=0.9, cfg=0.3, demi_tons=0, echo=None),
}
# onomatopées : le modèle les joue librement, on ne les exige pas dans la vérification
ONOMATOPEES = r"\b(g+r+|bwa+ha+(ha)*|mouah+a+(ha)*|h[ée]( h[ée])*|ho( ho)*|hum( hum)*|hmpf|m+h+|ha)\b"


def reference(f):
    """Enregistrement de référence de la faction (wav, m4a, mp3…), converti en wav mono 24 kHz, ou None."""
    src = next((p for p in sorted(REF.glob(f"{f}.*")) if p.suffix.lower() in (".wav", ".m4a", ".mp3", ".ogg", ".flac", ".aac", ".opus")), None)
    if not src: return None
    wav = REF / f".{f}-ref.wav"
    if not wav.exists() or wav.stat().st_mtime < src.stat().st_mtime:
        import av
        with av.open(str(src)) as c:
            rs = av.AudioResampler(format="flt", layout="mono", rate=24000)
            a = np.concatenate([r.to_ndarray().reshape(-1) for fr in c.decode(audio=0) for r in rs.resample(fr)])
        a = a[: 24000 * 25]  # 25 s au plus
        sf.write(wav, a * (10 ** (-3 / 20) / max(1e-9, np.abs(a).max())), 24000)
    return str(wav)


def graine(i, n, essai=0):
    cle = f"{i}#{n}" + (f"#{essai}" if essai else "")  # 1re prise : même graine qu'avant la vérification
    return int(hashlib.sha1(cle.encode()).hexdigest()[:8], 16)


ESSAIS = 5        # prises au plus par réplique
SEUIL = 0.8       # ressemblance minimale entre le texte demandé et ce que Whisper entend


def lettres(t):
    """Texte réduit à ses lettres, sans accents ni ponctuation, pour comparer."""
    t = re.sub(ONOMATOPEES, " ", t.lower())
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if c.isalnum())


def verifier(whisper, w, sr, texte):
    """Transcrit la prise (Whisper, français), coupe ce qui suit le dernier mot attendu
    (le modèle ajoute parfois des marmonnements) et rend (prise coupée, ressemblance, transcription)."""
    a = w.squeeze(0).cpu().numpy().astype(np.float32)
    a16 = AF.resample(torch.from_numpy(a), sr, 16000).numpy()
    segs, _ = whisper.transcribe(a16, language="fr", word_timestamps=True, beam_size=5, vad_filter=False)
    mots = [m for s in segs for m in (s.words or [])]
    cible = lettres(texte)
    meilleur, fin, entendu = 0.0, None, ""
    for k in range(1, len(mots) + 1):  # plus court début de transcription qui ressemble le mieux au texte
        e = "".join(m.word for m in mots[:k])
        r = difflib.SequenceMatcher(None, cible, lettres(e)).ratio()
        if r > meilleur + 1e-6: meilleur, fin, entendu = r, mots[k - 1].end, e.strip()
    if fin is not None:
        a = a[: min(len(a), int((fin + 0.25) * sr))]
    return torch.from_numpy(a).unsqueeze(0), meilleur, entendu


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
    from faster_whisper import WhisperModel
    whisper = WhisperModel("small", device="cpu", compute_type="int8")
    total, rates = 0, []
    for f, c, n, texte in taches:
        i = f"voix-{f}-{c}"
        dest = Path(o.sortie) / "voix" / f / f"{i}-{n}.mp3"
        if dest.exists() and not o.remplacer: continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        p, ref = PROFILS[f], reference(f)
        t = time.time(); garde = None
        for essai in range(ESSAIS):  # les essais suivent un ordre fixe : relancer redonne le même résultat
            fixer_graine(graine(i, n, essai))
            w = m.generate(texte, language_id="fr", audio_prompt_path=ref,
                           exaggeration=p["exaggeration"], cfg_weight=p["cfg"])
            w, r, entendu = verifier(whisper, w, m.sr, texte)
            if garde is None or r > garde[1]: garde = (w, r, entendu, essai)
            if r >= SEUIL: break
        w, r, entendu, essai = garde
        sf.write(dest, transformer(w, m.sr, p), m.sr, format="MP3")
        total += 1
        ok = r >= SEUIL
        if not ok: rates.append(dest.name)
        print(f"{'✓' if ok else '⚠'} voix/{f}/{dest.name}  « {texte} » → entendu « {entendu} »  "
              f"({r:.0%}, prise {essai + 1}, {time.time() - t:.1f} s)", flush=True)
    print(f"{total} répliques générées" + (f", à réécouter : {', '.join(rates)}" if rates else ", toutes vérifiées") + ".")


if __name__ == "__main__":
    main()

"""Tiempos por palabra de cada clip de voz (faster-whisper), para sincronizar lo que se ve con lo que se dice."""
import sys, json, subprocess, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
carpeta = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
for wav in sorted(carpeta.glob("*.wav")):
    dst = out / (wav.stem + ".json")
    if dst.exists(): continue
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    segs, _ = m.transcribe(a, language="es", word_timestamps=True)
    w = [(round(x.start, 2), round(x.end, 2), x.word.strip()) for s in segs for x in s.words]
    dst.write_text(json.dumps(w, ensure_ascii=False))
    print(wav.stem, len(w), flush=True)

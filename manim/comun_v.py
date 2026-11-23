"""
Estilo compartido para videos VERTICALES virales (1080x1920, 30 fps).
- Encabezado fijo de 2 líneas (blanco + neón), tipografía monoespaciada gruesa.
- Fondo azul noche con estrellas, brillo neón, números de 7 segmentos.
- Voz neuronal (sherpa-onnx, es_MX-claude-high) con caché por texto.
- Zonas seguras de TikTok: contenido importante entre y=+5.6 y y=-4.6, x < 3.4.
"""
import hashlib
import subprocess
import wave
from pathlib import Path

import numpy as np
from manim import *

config.frame_height, config.frame_width = 16, 9
import os as _os
if _os.environ.get("PREVIEW"):
    config.pixel_height, config.pixel_width, config.frame_rate = 960, 540, 10
else:
    config.pixel_height, config.pixel_width = 1920, 1080
    config.frame_rate = 30

FONDO_A, FONDO_B = "#070A1F", "#141B4A"
PANEL = "#111640"
CIAN = "#38E8FF"
VERDE = "#2EF2A2"
MAGENTA = "#E04BFF"
ROSA = "#FF3E9A"
AMARILLO = "#FFC93C"
NARANJA = "#FF8A3D"
GRIS = "#8E97C8"
BLANCO = "#F2F4FF"
MONO = "JetBrains Mono"
SEG = "DSEG7 Classic"
config.background_color = FONDO_A

DIR = Path(__file__).resolve().parent
VOCES = Path("/home/claude/voces")
MODELO_VOZ = "vits-piper-es_MX-claude-high"
FILTRO_VOZ = ("highpass=f=60,equalizer=f=180:t=q:w=1:g=2,equalizer=f=3200:t=q:w=1.5:g=2,"
              "acompressor=threshold=-22dB:ratio=3:attack=10:release=120,loudnorm=I=-15:TP=-1.5")
_tts = None


def _motor():
    global _tts
    if _tts is None:
        import sherpa_onnx
        d = VOCES / MODELO_VOZ
        cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=str(next(d.glob("*.onnx"))), tokens=str(d / "tokens.txt"),
                data_dir=str(d / "espeak-ng-data"), noise_scale=0.667, noise_scale_w=0.8, length_scale=1.0),
            num_threads=2))
        _tts = sherpa_onnx.OfflineTts(cfg)
    return _tts


# Voz elegida por variable de entorno VOZ: alex | dora | santa (Kokoro) o piper (es_MX-claude-high)
import os
VOZ = os.environ.get("VOZ", "eleven")
KOKORO = {"alex": 29, "dora": 28, "santa": 53}
VEL = float(os.environ.get("VOZ_VEL", "1.1"))
RECORTE = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.03,areverse,"
           "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.06,areverse,")
_motores = {}


def _kokoro():
    if "kokoro" not in _motores:
        import sherpa_onnx
        d = VOCES / "kokoro-multi-lang-v1_0"
        mc = sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=str(d / "model.onnx"), voices=str(d / "voices.bin"), tokens=str(d / "tokens.txt"),
            data_dir=str(d / "espeak-ng-data"), dict_dir=str(d / "dict"),
            lexicon=f"{d}/lexicon-us-en.txt,{d}/lexicon-zh.txt", lang="es"), num_threads=2)
        _motores["kokoro"] = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=mc, silence_scale=0.15))
    return _motores["kokoro"]


MODELO_ELEVEN = os.environ.get("ELEVEN_MODELO", "eleven_v4")
# ritmo viral: pausas internas máx ~0.25 s y 5 % más ágil, sin cambiar el tono
FILTRO_ELEVEN = ("silenceremove=stop_periods=-1:stop_duration=0.28:stop_threshold=-40dB:stop_silence=0.22,"
                 "atempo=1.05,highpass=f=50,loudnorm=I=-15:TP=-1.5")


def _eleven(texto, destino):
    import json
    import urllib.request
    env = dict(l.strip().split("=", 1) for l in open(Path.home() / ".config/eleven/env") if "=" in l)
    env["ELEVEN_VOZ"] = os.environ.get("ELEVEN_VOZ_ID", env["ELEVEN_VOZ"])
    cuerpo = {"text": texto, "model_id": MODELO_ELEVEN, "language_code": "es"}
    for intento in (cuerpo, {k: v for k, v in cuerpo.items() if k != "language_code"}):
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{env['ELEVEN_VOZ']}?output_format=mp3_44100_128",
            data=json.dumps(intento).encode(), headers={"xi-api-key": env["ELEVEN_KEY"], "Content-Type": "application/json"})
        try:
            Path(destino).write_bytes(urllib.request.urlopen(req, timeout=120).read())
            return
        except urllib.error.HTTPError as e:
            error = e.read().decode()[:300]
    raise RuntimeError(f"ElevenLabs: {error}")


def audio(carpeta, clave, texto, velocidad=None):
    velocidad = velocidad or VEL
    carpeta = Path(f"{carpeta}_{VOZ}")
    carpeta.mkdir(parents=True, exist_ok=True)
    wav, firma = carpeta / f"{clave}.wav", carpeta / f"{clave}.txt"
    h = hashlib.md5(f"{texto}|{velocidad}|{VOZ}|{FILTRO_VOZ}|{RECORTE}|{FILTRO_ELEVEN if VOZ == 'eleven' else ''}".encode()).hexdigest()
    if not (wav.exists() and firma.exists() and firma.read_text() == h):
        import soundfile as sf
        if VOZ == "miguel":  # voz grabada por el usuario: grabaciones/<carpeta>/<clave>.(wav|mp3|m4a|ogg)
            fuente = next((DIR / "grabaciones" / Path(carpeta).name.rsplit("_", 1)[0]).glob(f"{clave}.*"), None)
            if fuente is None:
                raise FileNotFoundError(f"Falta la grabación de '{clave}'")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(fuente), "-ac", "1", "-af",
                            "afftdn=nf=-25," + RECORTE + FILTRO_VOZ, "-ar", "48000", str(wav)], check=True)
            firma.write_text(h)
            with wave.open(str(wav)) as w:
                return wav, w.getnframes() / w.getframerate()
        if VOZ == "mudo":  # solo para vistas previas de diseño: silencio con la duración estimada del texto
            import numpy as _np
            dur = max(1.0, len(texto) / 15.5)
            sf.write(str(wav), _np.zeros(int(48000 * dur), dtype="float32"), 48000)
            firma.write_text(h)
            return wav, dur
        if VOZ == "eleven":  # ElevenLabs por API (clave y voz en ~/.config/eleven/env)
            fuente, sello = carpeta / f"{clave}_eleven.src", carpeta / f"{clave}_eleven.txt"
            h2 = hashlib.md5(f"{texto}|{MODELO_ELEVEN}|{os.environ.get('ELEVEN_VOZ_ID', '')}".encode()).hexdigest()
            if not (fuente.exists() and sello.exists() and sello.read_text() == h2):
                _eleven(texto, fuente)  # solo gasta créditos si cambia el texto o el modelo
                sello.write_text(h2)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(fuente), "-ac", "1", "-af",
                            RECORTE + FILTRO_ELEVEN, "-ar", "48000", str(wav)], check=True)
            firma.write_text(h)
            with wave.open(str(wav)) as w:
                return wav, w.getnframes() / w.getframerate()
        if VOZ in KOKORO:
            a = _kokoro().generate(texto, sid=KOKORO[VOZ], speed=velocidad)
        else:
            a = _motor().generate(texto, sid=0, speed=velocidad)
        crudo = carpeta / f"{clave}_crudo.wav"
        sf.write(str(crudo), np.array(a.samples), a.sample_rate)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(crudo), "-af", RECORTE + FILTRO_VOZ,
                        "-ar", "48000", str(wav)], check=True)
        crudo.unlink()
        firma.write_text(h)
    with wave.open(str(wav)) as w:
        return wav, w.getnframes() / w.getframerate()


def efectos(carpeta):
    sr = 48000
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    def guardar(nombre, x):
        x = (np.clip(x, -1, 1) * 32767 * 0.45).astype(np.int16)
        with wave.open(str(carpeta / f"{nombre}.wav"), "w") as w:
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr), w.writeframes(x.tobytes())

    t = np.linspace(0, 0.1, int(sr * 0.1), endpoint=False)
    guardar("pop", np.sin(2 * np.pi * (900 - 3500 * t) * t) * np.exp(-t * 40))
    t = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
    ruido = np.convolve(np.random.default_rng(1).normal(size=t.size), np.ones(40) / 40, "same")
    guardar("whoosh", ruido * np.sin(np.pi * t / 0.5) ** 2 * 3)
    t = np.linspace(0, 0.9, int(sr * 0.9), endpoint=False)
    guardar("ding", (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t * 5))
    t = np.linspace(0, 0.06, int(sr * 0.06), endpoint=False)
    guardar("tic", np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 90))


def musica(destino, segundos, sr=48000):
    """Fondo ambiental suave (acordes lentos sintetizados), libre de derechos."""
    t = np.arange(int(sr * segundos)) / sr
    acordes = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (196.0, 246.9, 293.7), (164.8, 207.7, 246.9)]
    x = np.zeros_like(t)
    dur = 4.0
    for i, a in enumerate(acordes * int(np.ceil(segundos / (dur * 4)) + 1)):
        t0 = i * dur
        m = (t >= t0) & (t < t0 + dur + 1.5)
        if not m.any():
            break
        tt = t[m] - t0
        env = np.minimum(tt / 1.2, 1) * np.exp(-np.maximum(tt - dur, 0) * 2)
        for f in a:
            x[m] += env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) / 6
    pulso = 0.5 + 0.5 * np.sin(2 * np.pi * t / 0.5) ** 8
    x += 0.04 * np.sin(2 * np.pi * 55 * t) * pulso
    x *= np.minimum(t / 2, 1) * np.minimum((segundos - t) / 2, 1)
    x = (x / np.abs(x).max() * 0.6 * 32767).astype(np.int16)
    with wave.open(str(destino), "w") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr), w.writeframes(x.tobytes())


def musica_motiva(destino, segundos, sr=48000, bpm=104):
    """Fondo MOTIVADOR libre de derechos (H01 v3, pedido 23-nov): progresión I-V-vi-IV en Do, pad suave, arpegio
    pulsado en corcheas, bombo blando en cada tiempo y charles en contratiempo. Se mezcla bajo (la voz manda)."""
    n = int(sr * segundos)
    t = np.arange(n) / sr
    x = np.zeros(n)
    beat = 60.0 / bpm
    compas = 4 * beat
    acordes = [(261.6, 329.6, 392.0), (196.0, 246.9, 293.7), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6)]
    bajos = [65.4, 49.0, 55.0, 43.7]
    rng = np.random.default_rng(7)
    k = 0
    while k * compas < segundos:
        a, b = acordes[k % 4], bajos[k % 4]
        t0 = k * compas
        i0, i1 = int(t0 * sr), min(n, int((t0 + compas + 0.6) * sr))
        tt = t[i0:i1] - t0
        env = np.minimum(tt / 0.4, 1) * np.exp(-np.maximum(tt - compas, 0) * 5)
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2.003 * f * tt) for f in a) / 9
        x[i0:i1] += env * pad
        x[i0:i1] += 0.30 * env * np.sin(2 * np.pi * b * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / beat) ** 2)
        notas = [a[0] * 2, a[1] * 2, a[2] * 2, a[1] * 2]
        for e in range(8):            # arpegio en corcheas
            ts = t0 + e * beat / 2
            j0, j1 = int(ts * sr), min(n, int((ts + 0.35) * sr))
            if j0 >= n:
                break
            u = t[j0:j1] - ts
            f = notas[e % 4]
            x[j0:j1] += 0.16 * np.exp(-u * 11) * (np.sin(2 * np.pi * f * u) + 0.3 * np.sin(2 * np.pi * 2 * f * u))
        for e in range(4):            # bombo blando + charles
            ts = t0 + e * beat
            j0, j1 = int(ts * sr), min(n, int((ts + 0.25) * sr))
            if j0 >= n:
                break
            u = t[j0:j1] - ts
            x[j0:j1] += 0.35 * np.sin(2 * np.pi * (55 + 90 * np.exp(-u * 30)) * u) * np.exp(-u * 14)
            th = ts + beat / 2
            h0, h1 = int(th * sr), min(n, int((th + 0.06) * sr))
            if h0 < n:
                u = t[h0:h1] - th
                ruido = rng.normal(size=u.size)
                ruido = ruido - np.convolve(ruido, np.ones(6) / 6, "same")
                x[h0:h1] += 0.05 * ruido * np.exp(-u * 70)
        k += 1
    x *= np.minimum(t / 3, 1) * np.minimum((segundos - t) / 3, 1)
    x = (x / np.abs(x).max() * 0.6 * 32767).astype(np.int16)
    with wave.open(str(destino), "w") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr), w.writeframes(x.tobytes())


# ------------------------------------------------------------------ visuales
def T(texto, size=40, color=BLANCO, peso="ULTRABOLD", fuente=MONO):
    return Text(texto, font=fuente, font_size=size, color=color, weight=peso)


def glow(m, color=None, capas=5, ancho=14, opacidad=0.07):
    color = color or m.get_color()
    g = VGroup()
    for i in range(capas, 0, -1):
        c = m.copy()
        c.set_fill(opacity=0)
        c.set_stroke(color, width=ancho * i / capas + 1, opacity=opacidad)
        g.add(c)
    return g


def neon(m, color=None, **kw):
    return VGroup(glow(m, color, **kw), m)


def fondo(a=FONDO_A, b=FONDO_B, pantallas=8):
    w, h = config.frame_width, config.frame_height
    base = Rectangle(width=w * 3, height=h * pantallas, stroke_width=0).set_fill(color=[b, a], opacity=1)
    base.set_sheen_direction(UP).move_to(UP * h * (pantallas - 1) / 2 * 0.95)
    rng = np.random.default_rng(7)
    n = 520
    estrellas = VGroup(*[Dot([x, y, 0], radius=r, color=BLANCO).set_opacity(o) for x, y, r, o in zip(
        rng.uniform(-w / 2, w / 2, n), rng.uniform(-h / 2, h * 7, n), rng.uniform(0.01, 0.03, n),
        rng.uniform(0.15, 0.65, n))])
    return VGroup(base, estrellas)


def encabezado(l1, l2, c2=VERDE, s1=58, s2=96):
    a = T(l1, s1, BLANCO)
    b = T(l2, s2, c2)
    g = VGroup(a, b).arrange(DOWN, buff=0.18)
    for m in (a, b):
        if m.width > 7.3:
            m.scale_to_fit_width(7.3)
    g.move_to([0, 5.55, 0])
    return VGroup(glow(b, c2, capas=4, ancho=12, opacidad=0.06), g)


def display(valor, unidad="", color=CIAN, size=80):
    num = T(valor, size, color, "NORMAL", SEG)
    sombra = T("".join("8" if ch.isdigit() else ch for ch in valor), size, color, "NORMAL", SEG).set_opacity(0.08)
    sombra.move_to(num, aligned_edge=RIGHT)
    g = VGroup(sombra, glow(num, color, capas=4, ancho=10, opacidad=0.08), num)
    if unidad:
        g.add(T(unidad, int(size * 0.5), color).next_to(num, RIGHT, buff=0.18, aligned_edge=DOWN))
    return g


def etiqueta(texto, color=GRIS, size=30):
    return T(texto, size, color, "NORMAL")


class EscenaVertical(MovingCameraScene):
    GUION: dict = {}
    CARPETA_VOZ = "voz"
    COLORES = (FONDO_A, FONDO_B)
    PANTALLAS = 8

    def setup(self):
        super().setup()
        efectos(DIR / "sfx")
        self.camera.background_color = self.COLORES[0]
        self.fondo = fondo(*self.COLORES, self.PANTALLAS)
        self.add(self.fondo)
        self.srt = []

    def voz(self, clave):
        wav, dur = audio(DIR / self.CARPETA_VOZ, clave, self.GUION[clave])
        inicio = self.renderer.time
        self.add_sound(str(wav))
        self.fin_voz = inicio + dur
        pal = self.GUION[clave].split()
        bloques = [" ".join(pal[i:i + 6]) for i in range(0, len(pal), 6)]
        pesos = np.array([len(b) + 4 for b in bloques], float)
        lim = inicio + np.concatenate([[0], np.cumsum(pesos) / pesos.sum() * dur])
        self.srt += [(a, z, b) for b, a, z in zip(bloques, lim[:-1], lim[1:])]
        return dur

    def cerrar_voz(self, extra=-0.3):
        w = self.fin_voz - self.renderer.time + extra
        if w > 0.02:
            self.wait(w)

    def sfx(self, nombre, gain=-8):
        self.add_sound(str(DIR / "sfx" / f"{nombre}.wav"), gain=gain)

    def fijo(self, m, offset=None):
        """Mantiene un objeto fijo en pantalla aunque la cámara se mueva."""
        off = m.get_center() - self.camera.frame.get_center() if offset is None else offset
        m.add_updater(lambda x: x.move_to(self.camera.frame.get_center() + off))
        return m

    def tear_down(self):
        import json
        (DIR / f"{type(self).__name__}.srt.json").write_text(json.dumps(self.srt, ensure_ascii=False))


def pastilla(texto, color=CIAN, size=30, relleno=0.18):
    """Cápsula redondeada con texto (etiquetas bajo los dibujos)."""
    t = T(texto, size, color)
    caja = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.32, corner_radius=(t.height + 0.32) / 2,
                            stroke_color=color, stroke_width=3).set_fill(color, relleno)
    return VGroup(caja, t.move_to(caja))


def fuente(texto, y=-4.45):
    return T("fuente: " + texto, 20, GRIS, "NORMAL").set_opacity(0.85).move_to([0, y, 0])


def chispa(a, b, color=AMARILLO, n=7, amp=0.18, semilla=0):
    """Rayo en zigzag entre dos puntos."""
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    nrm = np.array([-d[1], d[0], 0]) / (np.linalg.norm(d) + 1e-9)
    rng = np.random.default_rng(semilla)
    pts = [a] + [a + d * k / n + nrm * amp * rng.uniform(-1, 1) for k in range(1, n)] + [b]
    m = VMobject(stroke_color=color, stroke_width=7).set_points_as_corners(pts)
    return VGroup(glow(m, color, capas=4, ancho=16, opacidad=0.12), m, m.copy().set_stroke(BLANCO, 2.5))

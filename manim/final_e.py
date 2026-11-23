"""Video final: cuerpo Manim + música suave + marca de agua (logo + @miguelesquit) + portada en los 2 primeros cuadros.
Uso: python3 final_e.py entrada.mp4 v|h salida.mp4 portada.png   (la portada va SIEMPRE, en verticales y horizontales)"""
import subprocess, sys, os
from comun_v import musica, musica_motiva
from pathlib import Path
ent, fmt, sal = sys.argv[1], sys.argv[2], sys.argv[3]
portada = sys.argv[4] if len(sys.argv) > 4 else None
if not portada:
    print("AVISO: falta la portada; el video no la tendrá al inicio", file=sys.stderr)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ent],
                         capture_output=True, text=True).stdout)
m = Path(sal).with_suffix(".musica.wav")
(musica_motiva if os.environ.get("MUSICA") == "motiva" else musica)(m, d + 1)
import os
marca = Path(__file__).parent / f"marca_{fmt}{os.environ.get('MARCA', '2')}.png"  # MARCA="" usa la versión anterior
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ent, "-i", str(m), "-i", str(marca), "-filter_complex",
                "[0:v][2:v]overlay=0:0,format=yuv420p[v];[0:a]aresample=48000,asplit=2[voz][sc];"
                f"[1:a]volume={os.environ.get('VOL_MUSICA', '0.10')}[mu0];"
                "[mu0][sc]sidechaincompress=threshold=0.02:ratio=4:attack=20:release=400[mu];"   # la música baja cuando hablas
                "[voz][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac",
                "-b:a", "192k", "-movflags", "+faststart", sal], check=True)
m.unlink()
if portada:  # 2 cuadros de portada al inicio (para elegirla como miniatura en Reels/Shorts)
    tmp = Path(sal).with_suffix(".tmp.mp4")
    Path(sal).rename(tmp)
    w, h = (1080, 1920) if fmt == "v" else (1920, 1080)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-t", str(2 / 30), "-i", portada,
                    "-f", "lavfi", "-t", str(2 / 30), "-i", "anullsrc=r=48000:cl=mono", "-i", str(tmp), "-filter_complex",
                    f"[0:v]scale={w}:{h},format=yuv420p,setsar=1[p];[2:v]setsar=1[b];[1:a]aresample=48000[pa];[2:a]aresample=48000[ba];"
                    "[p][pa][b][ba]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", sal], check=True)
    tmp.unlink()
print(sal, round(d, 1), "s")

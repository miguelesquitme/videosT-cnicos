# Videos técnicos · @miguelesquit

Código de los videos de electricidad y automatización (YouTube y Facebook).

| Carpeta | Contenido |
|---|---|
| `manim/` | Escenas Manim 0.21: bases (`comun_e.py`, `taller.py`, `shorts_c.py`, `reel_base.py`), librerías de piezas (`piezas_*.py`), guiones (`guion_*.py`, `guiones_*.py`), `final_e.py` (música, marca de agua y portada) |
| `remotion/` | Reels hechos en Remotion 4 (React + SVG): `src/R3.jsx`, `R4.jsx`, `R5.jsx`, `lib.jsx`, scripts `prep.py`, `render.mjs`, `stills.mjs` |
| `sfx/` | Efectos de sonido (tic, pop, ding, whoosh) |
| `marca/` | Logo oficial y marcas de agua |
| `referencias/` | Enlaces y notas de los manuales usados para recrear cada equipo (sin PDFs con copyright) |

La clave de ElevenLabs **nunca** va en este repo: vive en `~/.config/eleven/env` (`ELEVEN_KEY`).

Render típico: `FORMATO=v VOZ=eleven manim -qh --disable_caching -o salida archivo.py Clase` y luego `MARCA=3 python3 final_e.py salida.mp4 v final.mp4 portada.png`.

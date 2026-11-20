# Kit · Videos de electricidad (@miguelesquit)

Estilo: fondo blanco, rejilla suave, líneas finas, tipografía Inter, colores NEC (neutro blanco, fase negra,
retorno rojo, tierra verde) y turquesa del logo como color de marca.

- `comun_e.py`   estilo, paleta, cables/tubos "físicos", escena base con voz (usa comun_v.py para voz/música).
                  FORMATO=v → 1080x1920 · FORMATO=h → 1920x1080.
- `dibujos_aves.py` pajarito, águila, poste, persona, tanque, pila, iconos.
- `nema.py`      centro de carga, breaker, caja octagonal 4", caja 2x4, interruptor, portalámparas, foco,
                  conectores EMT, abrazaderas, wire nuts y rutas de cables del circuito.
- `e01_pajaros.py`  video vertical.   `e02_guion.py` + `e02_lampara.py`  video horizontal.
- `logo.py`      recrea el logo ME. y genera marca_v.png / marca_h.png.  `final_e.py` agrega música y marca.
- `voz_e01_eleven/`, `voz_e02_eleven/`  voces ya generadas: re-renderizar no gasta créditos.

Producir:
  VOZ=eleven python3 e01_pajaros.py                       # voces (solo cambia lo editado)
  VOZ=eleven manim -o final e01_pajaros.py Pajaros
  python3 final_e.py media/videos/e01_pajaros/1920p30/final.mp4 v salida.mp4
  FORMATO=h VOZ=eleven manim -o final e02_lampara.py Lampara
  python3 final_e.py media/videos/e02_lampara/1080p30/final.mp4 h salida.mp4
Vista previa rápida: anteponer PREVIEW=1.
La clave de ElevenLabs va en ~/.config/eleven/env (nunca en el código).

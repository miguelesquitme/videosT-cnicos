# Librería de componentes (canal @miguelesquit)

Equipos dibujados en SVG con medidas reales (mm), rasterizados a PNG con Chromium y usados en Manim.

| Archivo | Contenido |
|---|---|
| `svgref.py` | Equipos del tablero calcados de las referencias del usuario: contactor, disyuntores, guardamotor, relé térmico, relés y temporizador de 8 pines, operadores 22 mm (frente + bloque trasero), sensores, flotador, motor Nidec con placa real, caja de bornes, borneras, LOGO!, LOGO!Power, CPU 1212C, pinza, multímetro, puntas. Cada uno con sus estados (on/off, presionado, disparado). |
| `svgfoto.py` | Fotocontrol de alumbrado ANSI C136.10 pieza por pieza: frente, corte, prueba con cinta, base de giro vista de abajo, receptáculo con hilos, tarjeta (sensor, fuente, relé, MOV), CdS, fototransistor, relé en corte, luminaria en poste. Fuentes en el docstring. |
| `simsvg.py` | Símbolos IEC de referencia (CONGELADOS). |
| `render_svg.py` | `render_lote(lote, carpeta, px_mm)` → PNG transparente + JSON (`W`, `H`, `margen`, `bornes` en mm). |
| `svgeq.py`, `svghd.py` | Versiones anteriores (se conservan por compatibilidad). |

Cada función devuelve `(svg, puntos_mm, (W, H))`. En Manim: `Pieza(nombre, ancho).p("punto")` (ver `manim/f01_fotocelda.py`) o `Eq3` (`manim/h01v3_lay.py`).

Diagramas: `manim/diag_lit.py` recrea literal los diagramas que entrega el usuario (potrace, un color, textos reescritos).
Sincronía voz-imagen: `manim/alinear.py <carpeta_voz> <alin_xx>` (faster-whisper) + `self.en("palabra")`.

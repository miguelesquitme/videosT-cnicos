# Notas de publicaciones (imágenes RRSS) — se trabajan en OTRO chat; no cargar en sesiones de video

## Publicaciones (FB · IG · comunidad YT), 24-nov — `manim/posts/gen_posts2.py`
- 1080 × 1350, FONDO BLANCO (se ven los detalles), estilo de las referencias del usuario: banda superior con la pregunta, título en dos líneas (texto de color + cinta inclinada), párrafo explicativo, equipo del catálogo grande con FLECHAS punteadas que señalan y nombran sus partes, fuente al pie, logo ME. abajo a la izquierda y sello "¿Sabías esto?…" abajo a la derecha. Letra de títulos Oswald (`posts/fonts`, OFL).
- Siempre con la referencia (norma, hoja de datos o placa) de donde sale el dato.

## Publicaciones v3 (25-nov) — `manim/posts3/gen.py` (reemplaza a posts/ v1-v2)
- NO usar el banco de equipos propio: fotos REALES de Wikimedia Commons (crédito y licencia CC impresos al pie). Se traen con el navegador integrado (JS → canvas → base64) porque el contenedor no llega a Commons.
- 4 estilos: Partes de componentes (foto real + rectángulos numerados + leyenda técnica concisa) · ¿Sabías qué? · Datos interesantes · Comparaciones (dos fotos, VS, columnas, barra de conclusión). Marco metálico con remaches, panel blanco, chip de categoría de color.
- ≥ 3 fuentes por tema (norma, fabricante, organismo). Sin preguntas tipo trivia (aún no hay audiencia).

## Publicaciones v4 (25-nov, VIGENTE) — `manim/posts4/gen.py` (fotos en posts3/fotos)
- Estilo de las referencias Suiler: SIN cuadrícula, fondo claro con ondas/cuadros suaves, título Montserrat 900 en dos líneas (navy + texto blanco con contorno azul y relieve 3D) que dice lo que enseña, caja blanca con la explicación.
- Partes: "PARTES DE UN X" = vista FRONTAL real; "ASÍ ES UN X POR DENTRO" = corte/desarmado. Rótulos SEÑALADOS (recuadro blanco con borde rojo/azul alternado + línea en codo + punto), NO leyenda numerada aparte. Sin saturar: 6–8 rótulos cortos.

## Publicaciones v5 (25-nov, VIGENTE) — `manim/posts5/gen.py` (reusa Foto/rotulos de posts4; fotos en posts3/fotos)
- Aprobado por el usuario: SOLO el formato "ASÍ ES UN X POR DENTRO" (foto real en corte/abierta + rótulos señalados). Las de partes frontales, ¿sabías?, placa y comparaciones v4 NO le gustaron (confusas).
- FONDO BLANCO liso. Título: "ASÍ ES UN" pequeño azul marino + nombre en Anton NARANJA #FF6A00 con sombra azul marino + cinta azul marino "POR DENTRO". Caja de explicación gris claro con borde naranja.

## Publicaciones v6 (25-nov) — `manim/posts6/gen.py`: 10 ESTILOS para que el usuario escoja
- v5 le pareció plana y repetitiva; el título Anton se veía anticuado. Quiere impacto tipo miniatura, "Así es… por dentro" SOLO cuando aplique, y SOLO electricidad industrial (nada automotriz ni de otros temas: sin alternador, foco LED ni motor DC de servo).
- Estilos: 01 miniatura oscura+amarillo · 02 partes numeradas (Barlow itálica) · 03 VS diagonal azul/naranja · 04 dato número gigante · 05 tip de tablerista amarillo · 06 cómo se lee (acero) · 07 ¿sabías que? naranja · 08 paso a paso · 09 ficha técnica oscura · 10 editorial foto a sangre. Pendiente: que elija y luego crear la skill de imágenes.

## Publicaciones v7 (25-nov, VIGENTE) — `manim/posts7/gen.py`
- Estilos ELEGIDOS por el usuario (de v6/v5): E01 miniatura oscura+amarillo · E02 partes numeradas CON línea punteada del número al punto de la foto · E04 dato número gigante · E09 ficha técnica CON líneas de cada tarjeta a la pieza · "por dentro" blanco con título resaltado (marcador amarillo + chip azul).
- Le gustan las fotos tipo catálogo (producto recortado, fondo blanco) y los esquemas didácticos tipo Energy Matic (estados normal/activado, componentes internos). Esas referencias son de un libro: usarlas solo como información/estilo, nunca copiar sus imágenes.
- Datos verificados para corregir referencias: curva D = 10–20 × In (IEC 60898-1); clase 30 = 9–30 s a 7,2 Ie (IEC 60947-4-1).

## Lote B didácticas (25-nov) — `manim/posts8/gen.py`
- 20 esquemas propios en SVG estilo libro técnico ordenado (estados normal/activado, partes internas, simbología IEC desde simsvg, curvas, colores IEC 60204-1, PNP/NPN, M12). Entrega por carpetas `Imágenes/<fecha>_<lote>_<tema>` en la PC del usuario (C:\Users\Esquit\Documents\Personal\Videos RRSS\miguel esquit\Imágenes). Skill propuesta: `imagenes-miguelesquit`.

## Lote C normas (25-nov) — `manim/posts9/gen.py`, fuentes en `referencias/loteC_fuentes.md`
- El usuario RECHAZÓ el lote B por símbolos IEC incorrectos/incompletos dibujados a mano (ej. térmico sin recuadro, 95-96/97-98 mal); solo le gustaron los colores de pilotos y pulsadores. Le gustó el diseño.
- Regla nueva: un tema MUY específico por imagen y CADA dato cruzado con 2 PDF + 2 páginas web (norma o fabricante). Discrepancias anotadas (p. ej. Rapid llama "German" a un código de punteras que no es DIN 46228-4).
- En publicaciones NO dibujar símbolos IEC a mano: usar gráficos simples (barras, escalas, perfiles acotados), tablas, tarjetas de color y fotos reales.
- Entregado en `Imágenes/2026-11-25_loteC_normas` (PC ce1-labele3-155; ahí también se copiaron lote A y lote B).

## Lote D componentes (25-nov) — `manim/posts10/gen.py`, fuentes en `referencias/loteD_fuentes.md`
- Al usuario le gustó el lote C. Pidió mezclar fotos reales (Commons) con ilustraciones detalladas del catálogo (`posts10/img`) y títulos MÁS VISTOSOS: kicker de color + línea 1 navy + palabra clave en CINTA INCLINADA de color con sombra (`T()` en gen.py).
- Discrepancia: la placa/`items.json` del motor del catálogo dibuja 9 puntas baja tensión en TRIÁNGULO (T1-T6-T7); el caso base es estrella. En publicaciones usar foto real + tabla en estrella hasta corregirlo.
- Datos de hoja de datos por encima de la ilustración (3RV2021-4EA10 = 400 A, no 13 × 32). D20 resalta la placa con rectángulos de color, no líneas sobre el texto.
- Entregado en `Imágenes/2026-11-25_loteD_componentes`.

## 3D (25-nov) — `manim/posts3d/` (three.js `modelo.html` + `render3d.js` con servidor local 127.0.0.1:8765, luego `gen.py`)
- Relé térmico CHINT NR2-25 2,5–4 A modelado en 3D (cuerpo negro, placa blanca, dial azul con escala, STOP rojo, RESET azul H/A, TEST, indicador, 98 NO 97 · 96 NC 95, 2/T1 4/T2 6/T3, pines de cobre, gancho, placa lateral). Datos de la ficha LARSSYSTEM/CHINT (Clase 10A, Ue 690 V, 1NA+1NC, falta de fase). Señalado estilo E02 con líneas punteadas y vista lateral. Entregado en `Imágenes/2026-11-25_loteE_3d`.

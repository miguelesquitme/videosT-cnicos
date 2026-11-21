# Reglas del canal @miguelesquit (se cargan en cada sesión conectada a este repo)

Este archivo es la "memoria" del proyecto: cada corrección del usuario se agrega aquí y no se repite.

## Calidad técnica (lo más importante)
- Todo es técnico y a detalle. Cada borne, cable, etiqueta y símbolo se verifica contra la hoja de datos y la norma. Un punto mal conectado invalida el video.
- Nada se inventa: medidas, bornes y datos se sacan de documentación oficial (ver `referencias/`). Si falta un dato, se investiga o se pregunta al usuario.
- Todo lleva capacidad: las protecciones, el contactor, el relé térmico y el cable salen de la corriente del motor y de la tensión. Se usa la placa real del motor y NEC 2020 art. 430 (T430.250, 430.22, T430.52, 430.32) o IEC.
- Tres revisiones antes de renderizar (diseño, ingeniería borne por borne, docente) + hojas de contacto; quedan por escrito en `revision_<clave>.md`.

## Librería de componentes (`lib/`)
- Corrección 21-nov (v2): los equipos son BLANCOS como el esquema de referencia del usuario (cuerpo blanco con degradado suave, franjas oscuras en los auxiliares, tornillos "+" con relieve, línea azul, etiqueta con la referencia). SOLO los PLC (LOGO!, S7-1200) van en gris, con el detalle del CPU 1212C (borneras negras con tornillo de ranura, grupos rotulados, LEDs).
- Corrección 21-nov (v4): estilo PLANO calcado de las referencias, esquinas RECTAS (nada redondeado), sombras cortas y definidas bajo franjas y piezas elevadas. `svgref.py` dibuja cada equipo en los píxeles de su imagen de referencia y lo escala a mm (contactor, breaker 2P, CPU 1212C). Es la base para el resto del catálogo. `a_inkscape()` exporta SVG con capas para editar en Inkscape (archivos en `lib/inkscape/`). Catálogo v3 completo en `svgref.py`.
- Corrección 21-nov: en la franja de marca de los equipos genéricos va el LOGO ME. (no el texto MIGUEL ESQUIT).
- Pulsadores: I = marcha (verde), O = paro (rojo) según IEC 60417, aunque una referencia muestre lo contrario. CPU 1212C: 6 LED de salidas (no 8). LOGO!Power: todos los bornes arriba (L N + + − −).
- `svgeq.py` + `render_svg.py`: los equipos se dibujan en SVG (mm reales, degradados y sombras) y se rasterizan con Chromium a PNG de alta resolución; cada equipo trae sus bornes en mm (JSON) para cablear encima en Manim. Es la herramienta principal para equipos.
- `simbolos.py`: símbolos dibujados como en el Manual electrotécnico Telesquemario, cap. 7 (marca de función en el contacto fijo: gancho = contactor, × con tope = disyuntor, aro con tope = seccionador; mando manual ⊞; disparadores térmico (escalón) e I> en cajas por polo; pulsador "E" + círculo de función Ⓘ/Ⓞ; números de bornes girados 90° a la izquierda; bornes de campo con círculo). Potencia trazo grueso, mando trazo fino.
- `equipos.py`, `plcs.py`, `estilo.py`: versión 1 en Manim puro (reemplazada por SVG; se conserva por compatibilidad).
- `catalogo.py` + `catalogo_docx.js`: generan el catálogo en Word (equipo | símbolo | datos) para que el usuario lo revise.
- Equipos genéricos (disyuntor, guardamotor, contactor, relés, operadores, sensores, flotador): SIN marca del fabricante; llevan el logo del canal. LOGO!, S7-1200 y variadores: se CONSERVA la marca y el modelo.
- Pulsadores, selectores y pilotos: frente en 2D + vista trasera con el bloque de contacto (punto de conexión real). No se dibujan los cables conectados en los tornillos de las piezas de catálogo.

## Designaciones (pedido del usuario)
-F disyuntor / relé térmico · -Q disyuntor general · -QM guardamotor · -KM contactor · -KA relé · -KT temporizador · -S pulsador, selector, flotador · -H piloto · -B sensor · -M motor · -X borneras · -A PLC · -T fuente/transformador.
Borneras por paquetes: -X0 alimentación · -X1 motores · -X2 puerta/mando · -X3 campo (sensores).

## Numeración de bornes
Potencia 1/L1 3/L2 5/L3 → 2/T1 4/T2 6/T3 · NA x3-x4 · NC x1-x2 · bobina A1-A2 · térmico 95-96 NC / 97-98 NA · piloto X1-X2.
Relé/temporizador de 8 pines: bobina 2-7; común 1 (NA 3, NC 4); común 8 (NA 6, NC 5). Base: arriba 3 4 5 6, abajo 2 1 8 7.
Bloques de pulsador: NA 3-4, NC 1-2 (en el esquema 13-14 / 11-12 o 21-22). Sensores de 3 hilos: BN +, BU −, BK salida.

## Conductores (IEC 60204-1)
Potencia negro · mando AC rojo · mando DC azul · neutro azul claro · PE verde/amarillo. Calibre según la corriente (la potencia se ve más gruesa que el mando). Cada punta con puntera (DIN 46228-4) y marcador con su número de hilo.

## Video HORIZONTAL (estructura fija)
1 Gancho · 2 Justificar: causar duda / responder una pregunta técnica · 3 Planteamiento del problema real (capacidad del motor y tensión → protecciones) · 4 Lista de materiales (cantidad, nombre, características, observación) · 5 Diagrama de mando IEC · 6 Diagrama de potencia IEC · 7 Esquema de conexión del mando (a la par del diagrama, tramo por tramo) · 8 Esquema de conexión de potencia (igual) · 9 Pasarlo al cuadro eléctrico · 10 Puesta en marcha · 11 Invitación a suscribirse y a ver el siguiente video y los shorts.
- Cada sección abre con la frase de lo que toca ver y sonido de escritura. Sonidos donde apliquen (breaker que se conecta, disparo, motor, movimientos) + música de fondo a 0,10.
- Zoom siempre que se conecte un borne o se ajuste algo. Medición con multímetro como en las referencias.
- Por cada video horizontal: 3 shorts verticales de la misma calidad, relacionados, que lleven al horizontal.

## Videos VERTICALES
Fondo negro con cuadrícula (el de R2). 1:30 a 3:30. Un solo concepto por reel. Título "Así funciona…". Cierre: "Si te sirvió, suscríbete y sígueme."

## Caso base del canal
Trituradora de piedrín: motor 10 hp, 230/460 V, 24,3/12,2 A, 1760 rpm, F.S. 1,25 (catálogo real), red 240 V 3~; mando 240 VAC.

## Seguridad
La clave de ElevenLabs vive solo en `~/.config/eleven/env` (ELEVEN_KEY). Nunca en el repo.

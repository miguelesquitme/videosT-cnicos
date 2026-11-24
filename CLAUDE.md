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
- Corrección 21-nov (catálogo v4): SÍMBOLOS IEC = solo REFERENCIA (`simsvg.py`); los diagramas definitivos los entrega el usuario. Disyuntor: el símbolo es el que viene impreso en el equipo (× en el contacto, sin cajas). Guardamotor/térmico: cajas de disparo PEGADAS entre polos. Térmico: 95-96/97-98 accionados por el elemento térmico (sin símbolo de reset). Piloto: símbolo sin color. LOGO! y fuente: símbolos separados.
- Equipos: MÁS sombra en todo (filtros sDura/sCuerpo/sMando); bornes y borneras SIN contorno, se separan por sombra; marcadores de borneras en blanco (se rotulan al conectar). Pines del térmico de COBRE. Dial del guardamotor con aro oscuro (no blanco sobre blanco) y maneta negra con lengüeta clara. Piloto: apagado tenue / encendido verde pleno. Relé y temporizador llevan a la par el diagrama interno del zócalo. Sensor óptico en 3 modos con el haz recto sobre el eje. Cable del flotador con holgura. Motor visto de lado con placa PLATEADA de datos reales en el costado (no textos abajo). Caja de bornes estilo real (ver v5: placa gris, cobre, tuercas hexagonales). Pinza/multímetro estilo Fluke sin marca + puntas de prueba.
- Corrección 21-nov (v5): ETIQUETA de designación en los EQUIPOS FÍSICOS = placa AMARILLA cuadrada, sin borde, letras negras, con guion (-F1, -QM1…), y del MISMO tamaño real en todos (13 × 4,8 mm, `svgref.PL` + `ETQ_MM`). En pulsadores, selector, emergencia y pilotos va AFUERA (debajo), nunca sobre el botón o la luz. En guardamotor y relé térmico va dentro del rectángulo de la carátula. En borneras va en el separador. En los SÍMBOLOS la designación queda en texto negro.
- Pulsadores: I = marcha (verde), O = paro (rojo) según IEC 60417, aunque una referencia muestre lo contrario. CPU 1212C: 6 LED de salidas (no 8). LOGO!Power: todos los bornes arriba (L N + + − −).
- `svgeq.py` + `render_svg.py`: los equipos se dibujan en SVG (mm reales, degradados y sombras) y se rasterizan con Chromium a PNG de alta resolución; cada equipo trae sus bornes en mm (JSON) para cablear encima en Manim. Es la herramienta principal para equipos.
- `simbolos.py`: símbolos dibujados como en el Manual electrotécnico Telesquemario, cap. 7 (marca de función en el contacto fijo: gancho = contactor, × con tope = disyuntor, aro con tope = seccionador; mando manual ⊞; disparadores térmico (escalón) e I> en cajas por polo; pulsador "E" + círculo de función Ⓘ/Ⓞ; números de bornes girados 90° a la izquierda; bornes de campo con círculo). Potencia trazo grueso, mando trazo fino.
- `equipos.py`, `plcs.py`, `estilo.py`: versión 1 en Manim puro (reemplazada por SVG; se conserva por compatibilidad).
- `catalogo.py` + `catalogo_docx.js`: generan el catálogo en Word (equipo | símbolo | datos) para que el usuario lo revise.
- Equipos genéricos (disyuntor, guardamotor, contactor, relés, operadores, sensores, flotador): SIN marca del fabricante; llevan el logo del canal. LOGO!, S7-1200 y variadores: se CONSERVA la marca y el modelo.
- Pulsadores, selectores y pilotos: frente en 2D + vista trasera con el bloque de contacto (punto de conexión real). No se dibujan los cables conectados en los tornillos de las piezas de catálogo.

## Cómo se trabaja (reglas de oro del usuario)
- TODO lo que el usuario corrige en el catálogo se refiere a los COMPONENTES FÍSICOS, salvo que diga "símbolo".
- La SIMBOLOGÍA IEC NO se toca (`simsvg.py` y los PNG `*_simbolo.png` quedan congelados). El usuario entrega los diagramas hechos.
- Lo que el usuario NO menciona NO se modifica. Antes de entregar se verifica que solo cambiaron los equipos pedidos.
- Cada corrección se anota aquí el mismo día, con el componente y el porqué.

## Correcciones de equipos (v5, 21-nov)
- Breakers: datos impresos como el ejemplo del usuario (Ue, norma, Icn, Uimp), ventana indicadora verde y "O-OFF" en cada manija.
- Guardamotor: bloque de contactos auxiliares arriba (13-14 NO, 21-22 NC); carátula ordenada como el WEG MPW40 de referencia (CLASS 10, dial con escala sin encimarse, rectángulo de etiqueta con rango, TRIP con barra curva sin curva de disparo, I> con valor, TEST, ON con "I", mando negro con lengüeta, OFF con "O", símbolo lateral).
- Relé térmico: sencillo como la referencia (dial azul, TEST, STOP rojo, RESET azul, 98 NO 97 · 96 NC 95 bajo los tornillos, sin dibujos de contactos).
- Relé y temporizador: números impresos en el plástico de la base.
- Operadores 22 mm y bloques traseros: base cuadrada GRIS con sombra (contraste). Flecha del paro de emergencia con punta tangente.
- Motor: carcasa del mismo alto que tapa y ventilador (sin partes delgadas).
- Caja de bornes: placa aislante GRIS, puntos de conexión de COBRE, tuercas HEXAGONALES, numeración impresa en la placa (no en marcadores).
- Borneras: sin bordes ni líneas dobles, con sombras, tornillos como el S7-1200, paquete con tierra (verde/amarillo), neutro (azul) y grises, separadores al inicio y final con la etiqueta.
- LOGO! y LOGO!Power: bornes iguales a los del S7-1200 (regleta negra + tornillo de ranura); ningún tornillo puede tocar a otro en ningún equipo.
- Pinza amperimétrica calcada del original del usuario (sin marca).
- Pulsadores, selector, emergencia y pilotos: se QUEDA el frente 2D + el bloque trasero por separado (como v5). Lo único que cambió (captura del usuario, 21-nov) es el DIBUJO DEL BLOQUE DE CONTACTO: tornillos EN CRUZ (iguales a los auxiliares del contactor) n1 arriba / n2 abajo con número, ventana NC roja / NO verde / LED blanca, leva semicircular, pestaña con punto y tornillo de fijación a la izquierda; cuerpo gris. (`svgref.bloque`). NO usar la lámina operador-de-lado.

## Correcciones de equipos (v8, 22-nov)
- Cada equipo con DOS estados, sin borrar el apagado: breakers `on=` (ventana verde encendida + manija arriba "I-ON"; apagado = ventana oscura), guardamotor `on=`, contactor `on=`, relé térmico `disparado=` (bandera TRIP), relé 8p y temporizador `on=` (LED), selector pos 0/1, pulsadores/emergencia `presionado=`, piloto `encendido=`.
- Guardamotor: frente más corto, mando más arriba (boceto del usuario, WEG MPW40).
- Relé térmico estilo CHNT NR2: escala de amperios IMPRESA en el dial (números correctos del rango), RESET azul con H (manual) y A (automático).
- Temporizador: en el video se pone el tiempo correcto que se use (`tiempo=`).
- Operadores 22 mm: caja de plástico NEGRO con sombra + portaetiquetas negro ARRIBA con espacio AMARILLO (designación y función, p. ej. -S1 ARRANQUE). Reemplaza la etiqueta abajo de v5. Bloque trasero: cuadrado NEGRO con el contacto GRIS (tornillos en cruz).
- Sensores: etiqueta en la base junto a la salida del cable; datos técnicos impresos en la base.
- Motor: etiqueta sobre la caja de conexiones. Borneras: topes más bajos que los bornes. LOGO!/LOGO!Power: etiqueta en el rectángulo de arriba.

## Correcciones de equipos (v9, 22-nov noche)
- Operadores (pulsadores, selector, emergencia, pilotos): el frente y el portaetiquetas son UNA SOLA pieza de plástico negro (arriba el espacio amarillo con designación y función, abajo el operador). `_operador_svg`.
- Bloque trasero: SIN cuadro negro alrededor; se ve la parte trasera del pulsador: base/adaptador NEGRO y el contacto en GRIS CLARO bien distinto (tornillos en cruz, ventana de color, leva).

## Diagramas (regla 22-nov)
- (Correcciones_V7) Se recrean PIXEL POR PIXEL desde la imagen del usuario (`manim/diag_lit.py`: se borran solo los textos, el dibujo se pasa a UN SOLO COLOR negro y se vectoriza con potrace; los textos se reescriben en su lugar). Solo cambian etiquetas, numeraciones, nombres y capacidades según el caso. Originales en `referencias/diagramas_h01/`.
- Los diagramas de mando y potencia los ENTREGA el usuario. Se recrean literal (mismos símbolos); solo puede cambiar el color de los textos; mando con trazo un poco más fino que potencia.
- En cada video nuevo, ANTES de empezar, se le PIDEN los diagramas al usuario.

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

## H01 Arranque directo — v2 (decisiones 22-nov, reemplazan las del 21-nov)
- Diagramas: los del usuario (Correcciones_V6: potencia image5, mando image6), literal. Se adaptan solo los VALORES al motor de 10 hp y -X1 pasa de U1 V1 W1 a T1 T2 T3 (motor NEMA, autorizado por el usuario).
- Red 208Y/120 V 3~ 60 Hz · mando 120 VAC L-N (L tomada en el borne 1 de ENTRADA de -F2, mismo punto que -X0:1; decisión del usuario).
- Motor REAL: Nidec US Motors U10P2D · 10 hp · 208-230/460 V · 26,5/23,9/12 A · 1760 rpm · F.S. 1,25 · Ef. 91,7 % · NEMA B · 215T · TEFC · Aisl. F. FP y letra de código NO publicados (no se ponen). 9 puntas; "apto para arranque de devanado parcial en baja tensión" ⇒ estrella (Y) 9 puntas: baja tensión L1-T1·T7, L2-T2·T8, L3-T3·T9, T4-T5-T6 unidos (confirmar con la placa de conexiones).
- Cálculo NEC 2020 a 208 V: T430.250 = 30,8 A · conductor 125 % = 38,5 A → 8 AWG THHN 75 °C · breaker -F2 3P curva C 80 A (250 % = 77 A → siguiente estándar, 430.52(C)(1) Exc. 1) · relé térmico -F3 23–32 A ajustado a 26,5 A (máx 125 % = 33,1 A, 430.32(A)(1)) · contactor -KM1 38 A AC-3 (UL: 10 hp a 200/208 V; el de 32 A solo da 7,5 hp a 208 V) bobina 120 VAC 1NA+1NC · -F1 1P C2 · mando 14 AWG rojo, neutro azul claro, PE verde/amarillo.
- Mando: -X0 L → -F1 1-2 → -F3 95-96 → -S0 PARO 11-12 → -S1 ARRANQUE 13-14 ∥ -KM1 13-14 → -KM1 A1-A2 ∥ -H1 (verde, M1 ON) → N. Desde -F1:2 → -KM1 21-22 → -H2 (rojo, M1 OFF) → N. Sin -X2 (no está en el diagrama).
- Hilos (número IEC por potencial): 1 L→F1:1 · 2 F1:2/95/21 · 3 96-11 · 4 12-13-13 · 5 14-14-A1-X1(H1) · 6 22-X1(H2) · N.
- Correcciones V6 del video: gancho con dato curioso o pregunta (NUNCA insinuar que otros lo hacen mal) · eje del motor girando (sin arcos) · datos de placa encerrados en rectángulos · nunca decir "menos" por el guion · lista de materiales en tabla Cantidad | Nombre | Características | Observación (tensión del sistema, riel DIN 35 mm, contactor separando mando/potencia, térmico compatible con el contactor, borneras contadas del diagrama por color + separadores por paquete, cable aproximado por ítem color/calibre, riel DIN, canaleta ranurada, gabinete con medida) · diagramas dibujados tramo por tramo (línea, símbolo, línea) explicando · equipos más pequeños, cables CURVOS, cada cable con puntera + marcador IEC entrando bajo el tornillo, marcado simultáneo en el diagrama · tablero real por etapas (gabinete, plancha, canaletas, riel, tornillos, equipos, puerta), más pequeño con el motor y las mediciones a la vista · cierre: "subiré más contenido, suscríbete, sígueme y mira mi siguiente video" (sin decir cuántos shorts ni el tema del siguiente) · sin tarjeta de shorts.

## H01 v3 (Correcciones_V7, 22-nov noche)
- Fondo GRIS CLARO con cuadrícula gris suave (`TEMA=gris`); títulos, cuadros y textos con contraste (texto oscuro, cinta azul marino).
- Lo que se ve coincide EXACTO con lo que se dice: cada evento se ancla a su palabra (alineación faster-whisper de cada clip en `manim/alin_h01v2/`; `self.en("palabra")`).
- Conexión = DIDÁCTICA (no como plancha): arriba protecciones y contactor (térmico debajo, como el diagrama), abajo borneras en su riel DIN, puerta en vista trasera a la derecha, sin espacios grandes.
- Punto de conexión REAL: el cable llega al borde del equipo frente al tornillo y entra por DEBAJO del plástico; solo se ve el collar de la puntera (forma real) y el marcador blanco con el número. Cables SIN borde (solo el blanco lo lleva).
- Puesta en marcha en el esquema de conexión, ANTES del tablero (sección 9); el tablero es la 10.
- Tablero: plancha 400 × 300 mm (gabinete 400 × 300 × 200), canaleta ranurada 40 × 60 mm, riel DIN 35 mm dorado con tornillos naranja, estilo de la referencia del usuario; el cableado final va de cada borne a la canaleta.
- Miniatura: "Mi primer arranque de motor | Análisis de un caso, lista de materiales, diseño de diagramas y conexión" (`manim/miniatura_h01v3.png`).

## H01 v4 (Revisión V8, 23-nov)
- La VOZ siempre es la clonada del usuario (ELEVEN_VOZ_ID = VOCES[FORMATO] de comun_e). Al regenerar un clip, importar comun_e primero; nunca llamar comun_v.audio solo (usa otra voz).
- Diagramas SIN hoja blanca: directo sobre el fondo gris.
- En conexión del mando y de potencia NO se hace zoom.
- Borneras de caballete a escala real respecto de los demás equipos (KB = 0,72 K); equipos más cerca y más grandes para ver las conexiones.
- 95 y 96 del relé térmico se conectan POR ABAJO.
- Puerta (pulsadores y pilotos) a la derecha del contactor, a su altura, para enseñar a conectar.
- Medición de tensión: selector en V~ y la pantalla en voltios (208 / 120 V AC); resistencia: selector en Ω.
- Pinza: UN solo cable (T1 separado de los demás), con acercamiento y resaltado.
- Sin sección de tablero (se elimina). El cierre NO lleva portadilla de sección.
- Música de fondo MOTIVADORA (`comun_v.musica_motiva`, MUSICA=motiva) a 0,09 y con ducking bajo la voz (sidechaincompress en final_e.py).

## Videos VERTICALES
Fondo negro con cuadrícula (el de R2). 1:30 a 3:30. Un solo concepto por reel. Título "Así funciona…". Cierre: "Si te sirvió, suscríbete y sígueme."

## Caso base del canal
Trituradora de piedrín: motor Nidec U10P2D 10 hp, 208-230/460 V, 26,5/23,9/12 A, 1760 rpm, F.S. 1,25; red 208Y/120 V 3~; mando 120 VAC (desde H01 v2).

## Seguridad
La clave de ElevenLabs vive solo en `~/.config/eleven/env` (ELEVEN_KEY). Nunca en el repo.

## Shorts v2 (pedido 23-nov): recrear los reels con dibujo REAL
- Nada de dibujitos didácticos: cada aparato se dibuja pieza por pieza desde PDFs/hojas de datos (SVG en mm, `lib/svgfoto.py` como modelo) y cada evento se ancla a su palabra (faster-whisper). Primera prueba: F01 fotocelda (`manim/f01_fotocelda.py`, guion nuevo `guion_f01.py`). Los demás shorts, después de que el usuario apruebe esta prueba.
- (23-nov, pedido del usuario) Investigación de CADA componente: mínimo 4 fuentes = 2 manuales/hojas de datos PDF + 2 páginas web, de fabricantes distintos; ficha en `referencias/<clave>_fuentes.md`. Modelar por fuera y por dentro desde esas fuentes.
- Reels v2 hechos (23-nov): V22 toques, V23 giro al revés, V24 corona, V25 fusible, V26 factor de potencia, V28 120→240 V, V29 luces que bajan, V30 kWh, V32 estrella/triángulo, V33 IP65. Se saltaron V27 (lo cubre R1 inductivo) y V31 (lo cubre V31b variador). Base común `manim/reel_v2.py`, piezas `lib/svgv2*.py`/`svgv3*.py`.

## Canva (23-nov): cuadros editables para que el usuario corrija
- `manim/canva_dump.py` vuelca un cuadro de Manim a SVG/PDF editable (texto real, paths, imágenes) + inventario `*_base.json`. `manim/canva_h01_c8.py` = H01v4 sección 8 (inicio de p5).
- `manim/canva_diag.py`: el diagrama de potencia se dibuja SÍMBOLO POR SÍMBOLO (trazos con id: sim_X0_barras, sim_F2_disyuntor, sim_KM1_contactor, sim_F3_rele_termico, sim_X1_bornes, sim_M1_motor, sim_tierras, conductores_*), medido píxel a píxel de `potencia_original.png` (x·1,25+44,75 / y·1,25+95,75). La cuadrícula va en un solo path.
- (23-nov noche) El usuario dio acceso completo a Canva. Diseño del cuadro 8: DAHby9XlvlY ("Cuadro 8 · Conexión de potencia"). OJO: create-design genera con IA e INVENTA (puso Schneider GV2ME14, rangos falsos): solo sirve para obtener un diseño 1920×1080 vacío; se borra todo y se arma con edit-design.
- Armado (`manim/canva_capas.py` → `canva/capas/`): fondo PNG, cada equipo PNG suelto (insert_fill con el mediaId que devuelve la subida), cables en 2 capas PNG transparentes, diagrama como formas (insert_shape), marcas naranjas como formas, textos con add_text + format_text.
- Reglas de Canva aprendidas: un trazo de UN solo segmento (M…L…) NO se dibuja → las líneas rectas van como rectángulos RELLENOS (1,9 px); formas de alto < 12 px se estiran → viewBox de 12 px; replace_shape solo acepta trazos cerrados y ≤ 2048 bytes; cada edit-design devuelve todo el documento (caro): agrupar operaciones.
- Detección de cambios: `canva/h01_c8_canva_base.json` (locator → nombre de símbolo/equipo/texto). Se lee el diseño con read-design y se compara; o el usuario deja comentarios.

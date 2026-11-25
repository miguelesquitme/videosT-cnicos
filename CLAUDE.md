# Canal @miguelesquit · memoria del proyecto (versión compacta 24-nov)

Reglas vigentes. Cada corrección nueva del usuario se agrega aquí el mismo día (componente + porqué) y no se repite.

## Reglas de oro
- Todo técnico y a detalle; NADA se inventa (hoja de datos, norma o se pregunta). Un borne mal conectado invalida el video.
- Lo que el usuario NO menciona NO se modifica. Sus correcciones del catálogo son de COMPONENTES FÍSICOS salvo que diga "símbolo".
- Simbología IEC congelada (`lib/simsvg.py`, `*_simbolo.png`). Los DIAGRAMAS los entrega el usuario: pedirlos ANTES de cada video nuevo y seguirlos literal.
- Voz SIEMPRE la clonada: `import comun_e` antes que nada (`ELEVEN_VOZ_ID = VOCES[FORMATO]`); nunca `comun_v.audio` suelto. Clave solo en `~/.config/eleven/env`. Claves de clip NUEVAS cuando cambia un texto (la caché y `alinear.py` saltan las existentes).
- Lo que se ve = lo que se dice: cada evento anclado a su palabra (`alinear.py carpeta_voz alin_x/`, `self.en("palabra")`).
- Tres revisiones antes de renderizar (diseño, ingeniería borne por borne, docente) + hoja de contacto, en `revision_<clave>.md`.
- Commit y push al terminar cada entrega (hay un hook que lo exige).

## Datos del caso base (trituradora de piedrín)
- Red 208Y/120 V 3~ 60 Hz · mando 120 VAC L-N.
- Motor Nidec US Motors U10P2D: 10 hp · 208-230/460 V · 26,5/23,9/12 A · 1760 rpm · F.S. 1,25 · Ef. 91,7 % · NEMA B · 215T · TEFC · Aisl. F. FP y letra de código NO publicados (no se dicen). 9 puntas, estrella baja tensión: L1-T1·T7, L2-T2·T8, L3-T3·T9, T4-T5-T6 unidos.
- NEC 2020 a 208 V: T430.250 = 30,8 A · conductor 125 % = 38,5 A → 8 AWG THHN 75 °C · -F2 3P curva C 80 A (250 % = 77 A → siguiente estándar, 430.52(C)(1) Exc. 1) · -F3 23–32 A ajustado a 26,5 A (máx 125 % = 33,1 A, 430.32(A)(1)) · -KM1 38 A AC-3 (el de 32 A solo da 7,5 hp a 208 V) bobina 120 VAC 1NA+1NC · -F1 1P C2 · mando 14 AWG.
- Salida al motor: manguera TSJ 4 × 8 AWG (3 negros + verde/amarillo).

## Normas de dibujo y numeración
- Designaciones: -F disyuntor/relé térmico · -Q general · -QM guardamotor · -KM contactor · -KA relé · -KT temporizador · -S pulsador/selector/flotador · -H piloto · -B sensor · -M motor · -X borneras (-X0 alimentación, -X1 motores, -X2 puerta, -X3 campo) · -A PLC · -T fuente.
- Bornes: potencia 1/L1 3/L2 5/L3 → 2/T1 4/T2 6/T3 · NA x3-x4 · NC x1-x2 · bobina A1-A2 · térmico 95-96 NC / 97-98 NA · piloto X1-X2 · relé 8 pines: bobina 2-7, común 1 (NA 3, NC 4), común 8 (NA 6, NC 5) · bloque de pulsador NA 3-4, NC 1-2 · sensor 3 hilos BN +, BU −, BK salida.
- Conductores IEC 60204-1: potencia negro · mando AC rojo · mando DC azul · neutro azul claro · PE verde/amarillo; potencia más gruesa que mando. Cada punta con puntera (DIN 46228-4) + marcador blanco con su número de hilo.
- Pulsadores: verde I = marcha, rojo O = paro (IEC 60417). Decir "autoenclavamiento"; nunca decir "menos" por el guion.

## Librería de equipos (`lib/svgref.py` → PNG + JSON de bornes en mm con `render_svg.render_lote`)
- Estilo plano calcado de las referencias, esquinas rectas, cuerpo BLANCO con degradado suave, franjas oscuras en auxiliares, tornillos "+" con relieve, mucha sombra corta; bornes sin contorno. Solo los PLC (LOGO!, S7-1200) en gris.
- Genéricos SIN marca, con el logo ME. del canal; LOGO!, S7-1200 y variadores conservan marca y modelo.
- Etiqueta de designación = placa AMARILLA 13 × 4,8 mm, letras negras, con guion. En guardamotor y térmico dentro de la carátula; en borneras en el separador; en motor sobre la caja de conexiones; en LOGO! en el rectángulo de arriba; en sensores en la base.
- Cada equipo con sus dos estados (on/off, disparado, presionado, encendido, selector 0/1, temporizador con su `tiempo=`).
- Breakers: Ue, norma, Icn, Uimp impresos; ventana verde (encendido) y "I-ON"/"O-OFF" en cada manija.
- Guardamotor como WEG MPW40 (auxiliares 13-14/21-22 arriba, CLASS 10, dial con aro oscuro, TRIP, I>, TEST, mando negro con lengüeta). Relé térmico estilo CHNT NR2: escala de amperios real en el dial azul, TEST, STOP rojo, RESET azul H/A, 98 NO 97 · 96 NC 95; pines de COBRE.
- Operadores 22 mm: frente + portaetiquetas = UNA pieza de plástico negro (arriba espacio amarillo con designación y función, abajo el operador). Vista trasera (`svgref.bloque`): adaptador NEGRO cuadrado sin franjas y el CONTACTO en GRIS (tornillos en cruz n1 arriba / n2 abajo, ventana NC roja / NO verde / LED blanca, leva, pestaña). El cuadro del frente = mismo tamaño que el trasero.
- Borneras (`svgref.bornera`): labios arriba/abajo, tornillo redondo de ranura, cuadro central con número, topes oscuros (más bajos) con tornillo, SIN bordes; ancho según calibre; PE verde/amarillo, N azul. Riel DIN metálico con ranuras, sin bordes.
- Caja de bornes del motor: placa gris, puntos de cobre, tuercas hexagonales, numeración impresa. Motor de lado con placa plateada de datos reales. Pinza y multímetro estilo Fluke sin marca, con puntas.
- Relé y temporizador con números impresos en la base y su diagrama interno a la par. Sensores con datos impresos en la base. Ningún tornillo toca a otro.

## Video HORIZONTAL (modelo: H01 v5, `manim/h01v5*.py`)
- Estructura: 1 Gancho (dato curioso o pregunta, nunca insinuar que otros lo hacen mal) · 2 Pregunta técnica · 3 Problema real (placa del motor y tensión → protecciones) · 4 Materiales en tabla Cantidad | Nombre | Características | Observación · 5 Diagrama de mando · 6 Diagrama de potencia · 7 Conexión del mando · 8 Conexión de potencia · 9 Puesta en marcha · cierre "subiré más contenido, suscríbete, sígueme y mira mi siguiente video" (sin portadilla, sin tarjeta de shorts).
- Fondo `TEMA=gris` con cuadrícula; cinta azul marino; textos oscuros. Diagramas recreados píxel a píxel (`diag_lit.py`), sin hoja blanca, dibujados tramo por tramo.
- Conexión didáctica (sin zoom en 7 y 8): diagrama a la izquierda; arriba -F2 y -F1, debajo -KM1 con -F3 pegado, borneras bajo el térmico en su riel; puerta a la derecha en vista TRASERA (el frente solo al inicio, diciendo que por temas didácticos se ve por detrás). Equipos separados, escala real (KB = 0,72 K).
- Cables: entran a cada borne SOLO por ARRIBA o por ABAJO (contactor 13/21/A1 arriba, 14/22/A2 abajo; 95/96 por abajo); curvas ABIERTAS con tramo recto donde quepa el marcador; el cable entra bajo el plástico frente al tornillo (solo se ven collar y marcador); sin borde.
- UN hilo a la vez siguiendo el diagrama (marca naranja simultánea), lento (≈ 2,8 s), aros en origen y destino, opacando los ya conectados.
- Puesta en marcha: sin energía y con -F2 cerrado, continuidad 2-4, 4-6, 2-6 y cada fase contra PE (sin continuidad) · mando en Ω desde el hilo 3 · energía: 208 V entre fases y 120 V L-N en -X0 · marcha · corriente en la CAJA DEL MOTOR con zoom, pinza en UN solo conductor · disparo del térmico y RESET.
- Audio: `MUSICA=motiva VOL_MUSICA=0.09 MARCA=4 python3 final_e.py cuerpo.mp4 h salida.mp4 portada.png` (ducking bajo la voz). Sonidos donde apliquen (breaker, contactor, disparo, motor, tornillo).
- Render: `FORMATO=h TEMA=gris VOZ=eleven manim -qh --disable_caching -o <n> <archivo> <Clase>`; `SOLO=sec1,sec2 PREVIEW=1 -ql` para revisar.
- Por cada horizontal: 5 a 10 reels relacionados que lleven a él.
- H01: el diagrama de potencia del usuario lleva L1 (X0:1) → entrada 5 de -F2, L2 → 3, L3 → 1 (seguido literal); la L del mando se toma en la entrada 5 (= X0:1). Pendiente de confirmar por el usuario.

## Reels verticales (modelo: F01 fotocelda, `manim/f01_fotocelda.py` + `reel_v2.py`)
- 1:30 a 3:30, UN solo concepto. Fondo negro con cuadrícula (`TEMA=negro`), título "ASÍ FUNCIONA…" o pregunta, chip numerado por sección, zona útil y +3,6 a −7,2.
- Cada aparato dibujado pieza por pieza desde 4 fuentes (2 PDF de fabricante + 2 páginas web, fabricantes distintos), ficha en `referencias/<clave>_fuentes.md`; por fuera y por dentro.
- Cierre: "Si te sirvió, suscríbete y sígueme." Portada `Portada<clave>` en los 2 primeros cuadros (`final_e.py ... v ...`).
- Hechos: F01, V22–V26, V28–V30, V32, V33, R1–R5, v03–v18. No repetir temas.

## Miniaturas (`manim/miniaturas_pro/gen.py`, HTML + Playwright 1920×1080)
- Componentes (disyuntor, térmico, contactor): fondo AZUL con rayos suaves, etiqueta "GUÍA PRÁCTICA", título "SELECCIONA EL [APARATO] CORRECTO", tarjetas "N CRITERIOS / 2 EJEMPLOS", el equipo grande del catálogo actual, logo arriba a la derecha.
- Procesos (arranques: directo, cambio de giro, estrella-delta…): mismo diseño con fondo MORADO (`CSS_MORADO`), etiqueta "¡POR FIN!" u otra, equipos del proceso y tarjetas de datos del caso.

## Canva (cuadros editables para corregir)
- Diseño del cuadro 8 de H01: DAHby9XlvlY. `create-design` inventa contenido: solo para obtener un lienzo vacío; se arma con `edit-design` (`manim/canva_capas.py`, `canva_diag.py`, base de cambios `canva/h01_c8_canva_base.json`).
- Límites: línea de un solo segmento no se dibuja (usar rectángulo relleno), formas < 12 px se estiran, `replace_shape` solo trazos cerrados ≤ 2048 bytes, agrupar operaciones.

## Publicaciones (FB · IG · comunidad YT), 24-nov — `manim/posts/gen_posts2.py`
- 1080 × 1350, FONDO BLANCO (se ven los detalles), estilo de las referencias del usuario: banda superior con la pregunta, título en dos líneas (texto de color + cinta inclinada), párrafo explicativo, equipo del catálogo grande con FLECHAS punteadas que señalan y nombran sus partes, fuente al pie, logo ME. abajo a la izquierda y sello "¿Sabías esto?…" abajo a la derecha. Letra de títulos Oswald (`posts/fonts`, OFL).
- Siempre con la referencia (norma, hoja de datos o placa) de donde sale el dato.

## Serie de arranques (reels A01–A15 = V39–V53), 24-nov — `manim/reels_arr.py`, `guiones_arr.py`, `gen_arr_eq.py`, `lib/svgarr.py`
- Cortes nuevos en `svgarr`: relé térmico (bimetal, calefactor, regleta, 95-96/97-98), bobina del contactor (núcleo E, armadura, espira de sombra), puntera DIN 46228-4.

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

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

## Video HORIZONTAL (modelo: H01 v5 = el entregado como "mi primer arranque de motor", `manim/h01v5*.py`; es la referencia vigente)
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
- REFERENCIA VIGENTE: lote V22–V33 v2 (`manim/vNNv2.py` + `guion_vNNv2.py`, de "¿Estática o una fuga que mata?" V22 a "¿Qué significa IP65?" V33) y la serie de arranques A01–A15 ligada a H01 (`reels_arr.py`, `guiones_arr.py`, `guion_aNN.py`).
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

## Lote F · serie de UN dispositivo (25-nov) — `manim/posts11/gen.py`, fuentes en `referencias/loteE_fuentes.md`
- Nuevo formato pedido por el usuario: el usuario pasa un producto (link de tienda) y se hacen 6 infografías: 1 partes señaladas · 2 funcionamiento · 3 criterios de selección · 4 aplicación real · 5 versus con un equivalente de otra marca · 6 símbolo IEC con sus partes marcadas en el equipo (cajas de color con letra en ambos, no líneas largas: se ven sucias).
- Primero: relé térmico CHINT NR2-25 9–13 A (larssystemgt.com/1347). `svgref.rele_termico` ahora acepta `n_pasos` (escala 9-10-11-12-13).
- Las fotos de tiendas no se bajan desde el contenedor; si la PC no está conectada, pedir que adjunte la foto.
- Pendiente copiar a `Imágenes/2026-11-25_loteF_rele_termico_NR2` (PC desconectada al entregar).

## Lote G · 3D y foto real (25-nov) — `manim/posts12/gen.py`, fuentes en `referencias/loteG_fuentes.md`
- Fotos de tiendas: con el navegador integrado se bajan por `fetch` → base64 (salen en webp). Archivos grandes: en trozos de ≤ 600 000 caracteres (más grande se trunca a ~262 k).
- Siemens CAx sin cuenta: `www.automation.siemens.com/bilddb/cax_de.aspx?mlfb=<MLFB>` → cada motivo tiene `download.aspx?reqInsID=…` (STEP, DXF, SVG, PNG, render). Uso gratuito con crédito "Siemens AG".
- Render 3D de calidad: `posts12/modelos/hq.html` (PBR, sombra, luz de relleno desde la cámara, `mat` por nombre de malla, `hide`, devuelve posición de cada pieza). Etiquetas libres con `marc()` (posición manual) — más limpias que `lados()` cuando la pieza es ancha.
- Al usuario le importa usar SU foto cuando la da (NR2) y que las explicaciones no sean "básicas".

## Lote H · 5 equipos × 6 (25-nov) — `manim/posts13/gen.py`, fuentes en `referencias/loteH_fuentes.md`
- Al usuario le gustó G07 (foto real nítida de tienda). ESTILO VIGENTE: título kicker + cinta inclinada (sin la palabra "real"); rótulos con LÍNEA CONTINUA y RECUADRO de color semitransparente sobre la pieza (`cajas()`), `marcas()` solo recuadro con número, `letras()` para símbolo↔foto.
- Serie por equipo: 1 partes · 2 funcionamiento · 3 criterios · 4 aplicación real · 5 versus (rival en tarjeta oscura, sin foto ajena) · 6 símbolo con letras en símbolo y foto.
- Relpol R2N: bornes 11-12-14 / 41-42-44 / A1-A2 (impresos), no octal. Entregado en `Imágenes/2026-11-25_loteH_5equipos`.
- v2 (correcciones): fotos OFICIALES del fabricante, nítidas y sin marca de agua (relpol.pl, chintglobal.com, ifm.com, download.se.com `rendition_1500_jpg`, bilddb Siemens); nunca borrar marcas de agua de fotos ajenas. Recuadros de color SIN borde (relleno ~22 %), etiquetas sin borde. NO escribir marca, serie ni código del equipo en títulos/textos/pie ("imagen oficial del fabricante"). Versus = entre TIPOS de equipo (guardamotor vs breaker, breaker vs fusible, relé vs contactor, inductivo vs capacitivo); si no hay par lógico, no se hace. Estilos en `posts13/base.py`.

## Catálogo de 50 equipos 2D/3D (26-nov) — `referencias/equipos_2d3d/` (Word `Equipos_2D_3D_50.docx`, `build.js`)
- Referencias aprobadas por el usuario: G01 (LAY37 FreeCAD en 3D) y G06 (render + dibujo acotado Siemens). G05 (sensor genérico FreeCAD) = MALO, no usar modelos genéricos.
- Fuentes verificadas: Siemens Industry Bilddatenbank (42; búsqueda por MLFB con `multiobjecttypes` 60 = 3D-Modell, 70 = 3D-Rendering, 12 = Maßzeichnung, 4 = Produktfoto; POST a `search.aspx`), ifm (7; `restservices/us/en/productdetail/cadZips/<código>` da STEP/DXF), FreeCAD LAY37.
- Sin 3D en Bilddatenbank: motores SIMOTICS, SINAMICS V20/G120C (solo 2D), transformadores 4AM.
- Lote 2 (26-nov, `referencias/equipos_2d3d_lote2/`): el usuario pidió 50 de TIPOS DISTINTOS (el lote 1 repetía contactores, temporizadores, relés). Ningún tipo se repite con el lote 1.
- Vistas propias desde el STEP oficial: `step2glb.py` (OCP/cadquery-ocp → GLB) + `hq.html`/`batch.js` (three.js 0.160, Playwright). Así se ve el equipo desde cualquier ángulo.
- Bilddatenbank: `search.aspx?mlfb=X&multipleObjectTypes=T` (GET directo) · `download_csv.aspx` da títulos de motivos · descarga: POST `WSWebControls.asmx/RenderMotivDetail` → `download.aspx?reqInsID` (P.png 1000 px, .stp). Pasar STEP grandes con gzip (CompressionStream) en trozos de 600 000 caracteres.
- Verificar cada código en SiePortal (iframe en sieportal.siemens.com): 5ST3010 es contacto auxiliar, 3RF2320 descontinuado → 3RF3320.
- Schneider: imágenes multi-vista `download.se.com/files?p_Doc_Ref=…&p_File_Type=rendition_1500_jpg` (pedir desde una pestaña en download.se.com por CORS). WEG: biblioteca CAD libre `ecatalog.weg.net/drawings_2d_3d` (motores NEMA W22 215T, CFW500, CPTW, capacitores, tomas).

## Marca del canal (26-nov)
- Logo ME. turquesa SIEMPRE (`manim/logo_oficial.png`: M #94D3DF, E. #0095B0). El usuario ya NO aparece en foto en perfil/portadas. Banners modernos, gráficos limpios (nada que parezca IA), que muestren lo que hace: tableros, arranque de motores, PLC, normas. Generador: `manim/marca/gen.py`.
- Publicaciones de imágenes: se hacen en OTRO chat (skill `imagenes-miguelesquit`); notas en `referencias/publicaciones_notas.md`. No leerlas aquí.

## Shorts 3.0 (26-nov) — ganchos y títulos en el doc "Shorts 3.0 · nuevos ganchos y títulos"
- Facebook castigó el formato: todos de 1:33 y arrancando con definición técnica. REGLA: segundo 0 = acción visible (nada de título estático), frase 0–3 s de ≤ 8 palabras que contradice o intriga, definición después. Duración VARIABLE desde 1:00 según el tema (quitar/dejar p6, acortar el párrafo largo); nunca dos seguidos iguales ni 1:33.
- Carpetas en la PC (`miguel esquit/02. Verticales/`): `05 Instalaciones generales 2.0` = F01 + V22–V26, V28–V30, V32, V33 (11) → `05 Instalaciones generales 3.0`; `06 Refedencias de arranques con contactor - Mejora 2.0` = A01–A15 (V39–V53) → `06 Refedencias de arranques con contactor - Mejora 3.0`. Ambas 3.0 creadas el 26-nov con un LEEME_3.0.md. Ganchos de V19–V21, V27, V31, V34–V38 listos pero esos videos no están en esas carpetas.
- Medir a 48 h: vistas de 3 s en FB (> 20) y "vistos vs deslizados" en YouTube.

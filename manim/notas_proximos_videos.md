# Notas para los próximos videos (pedidas por Miguel)

## Efecto de corriente preferido (29-oct-2026)
Referencia: `referencias/efecto_corriente_punteada.png`.
- En lugar de "cometas" sueltos, el propio conductor lleva una **línea punteada que avanza** ("hormigas marchando") por su centro.
- Fase: conductor negro con trazos cian claro (#7FF3F5 aprox.) que se desplazan.
- Neutro: conductor blanco con trazos cian; tierra: verde/amarillo con trazos.
- Los trazos son cortos, rectangulares y redondeados, separados de forma regular, y se mueven a velocidad constante y suave en el sentido de la corriente.
- Implementación sugerida en `taller.py`: `DashedVMobject` sobre la ruta del cable con updater que desplace la fase de los guiones (o redibujar segmentos con offset `s0 += dt*vel`).
- El fondo de la referencia es azul oscuro con puntos; las cajas son grises con borde café/beige.

## Fondo del canal (29-oct-2026): azul marino
- `TEMA=oscuro` es ahora el valor por defecto en comun_e.py: degradado fijo #08142E → #12305A (opción "B · azul marino" elegida por Miguel), rejilla #16294F, textos blancos, tarjetas #1B2156, cable negro con borde claro.
- Marca de agua para fondo oscuro: `MARCA=3 python3 final_e.py ...` (logo turquesa 14 % + @miguelesquit claro).
- Corriente: `corriente()` ahora dibuja guiones cian (#6FF2FF) que avanzan sobre el conductor; la versión anterior quedó como `corriente_cometa()`. Durante "encender" y "repaso" los tubos se ponen translúcidos para ver los conductores.
- Ojo: nunca usar `.set_opacity()` en tubos (rellena el polígono); usar `set_stroke(opacity=...)`.

## Regla para videos LARGOS (29-oct-2026, pedido de Miguel)
- Una sola pregunta central al inicio; cada sección es un paso hacia la respuesta y el final llega al objetivo.
- Nada de temas sueltos para rellenar los 8 min: profundizar en la idea central (demostraciones, errores con su consecuencia animada, ejercicio). Lo que se desvía va a un Short.
- Título = la pregunta o el objetivo (no dos temas distintos en el mismo título).

## Comentarios del 30-oct-2026 (para los próximos videos; los ya hechos se quedan así)
- **Tarjetas con más contraste** sobre el fondo azul: relleno más claro (p. ej. #24306B → #2B3A7A) y borde #4A5AA0, para que se distingan del fondo.
- **Cables con curvas reales**: nada de quiebres en ángulo recto ni diagonales rectas; doblar con radio (set_points_smoothly / esquinas redondeadas), como un cable de verdad.
- **Empalmes** (Miguel les dice "empalmes", no "colas"): los conductores salen de la caja, se ven los 15 cm libres (NEC 2020 300.14: 150 mm libres y, si la abertura es < 200 mm, 75 mm fuera de la caja), se unen con el conector de empalme y luego se doblan hacia adentro. NEC 110.14(B) solo exige empalmar con un dispositivo identificado para ese uso (o soldadura) y aislarlo; no exige un tipo "derivación" en lugar de "cola de ratón", así que no decir que uno es obligatorio.
- **Conexión en tornillos**: el aislamiento llega hasta el tornillo, sin cobre expuesto fuera del terminal; el cable entra con curva natural y abraza el tornillo.
- **Continuidad visible**: el cable se ve entrar al tubo y salir del tubo (por el conector), nunca aparece "de la nada".
- Referencia de buenas conexiones: `referencias/conexiones_buenas_tecney.png`.
- **Procedimientos con PASOS**: cuando el video tenga procedimiento, barra lateral de pasos (PASO 1, 2, 3...) con el paso actual resaltado y su título arriba, diseño moderno con la paleta del canal (no como `referencias/pasos_barra_lateral_antigua.png`, que se ve antiguo). Solo cuando hay pasos.

## Cuidar los detalles (30-oct-2026, para actualizar la skill la próxima vez)
- Cuando un aparato se conecta, dibujar su **clavija real** (cuerpo, patas de fase/neutro/tierra) entrando en el **tomacorriente o la regleta**, no una línea que termina en el agujero. Referencia de lo que NO hacer: `referencias/detalle_clavija_regleta_mal.png`.
- Regla general: cada conexión debe verse físicamente (clavija en tomacorriente, cable en tornillo, cable entrando/saliendo del tubo, empalme con su conector).

## Cierre sin nombrar plataformas (31-oct-2026) — CONFIGURACIÓN FIJA
- Al final NO mencionar YouTube ni Facebook (ni en voz ni en pantalla), para evitar penalizaciones. Solo "Suscríbete" y "Sígueme".
- Voz de cierre: "Si te sirvió, suscríbete y sígueme. Nos vemos en el próximo video."
- Pantalla final (`resumen_y_final` en taller.py): botones "SUSCRÍBETE" (rojo) y "SÍGUEME" (turquesa), logo oficial y @miguelesquit. Ya cambiado en el código.
- Los videos ya entregados se quedan como están.

## Videos verticales (31-oct-2026)
- Usar el logo oficial y la MISMA paleta de los horizontales: fondo azul marino (degradado #08142E → #12305A), textos blancos, turquesa #0E9BB5, corriente punteada cian, marca de agua `marca_v3.png` (logo turquesa suave + @miguelesquit claro). Cierre: "SUSCRÍBETE" / "SÍGUEME", sin nombrar plataformas.

## Shorts verticales — corrección importante (1-nov-2026)
- Los 16 shorts V03–V18 quedaron superficiales: muy cortos (50–60 s), poco técnicos, diseño simple. Para los próximos:
  - Duración 1:30–3:00 (YouTube Shorts permite hasta 3 min; Facebook paga por tiempo de visualización).
  - Lenguaje técnico correcto: "lámpara incandescente", "interruptor termomagnético", "conductor", etc. Nunca "los focos de antes".
  - Explicar el fundamento y el origen del dato (física, norma, fabricante), no solo afirmarlo.
  - Diseño más rico y variado en cada short: escenas, diagramas, cortes, zoom, comparaciones animadas.

## Retroalimentación de los Shorts V03–V18 (1-nov-2026)
- Se sintieron superficiales y poco profesionales: deben enganchar PERO dejar enseñanza técnica real (fundamento y origen del dato).
- Terminología técnica correcta: "lámpara incandescente", no "focos de antes".
- Diseños más variados, visuales y didácticos (no la misma plantilla de pastillas).
- Duración de Shorts: 1:30 a 3:00 (no menos de 1 min).
- Se creó la skill `videos-electricidad-miguelesquit` (exclusiva de este canal).

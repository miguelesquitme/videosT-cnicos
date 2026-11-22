---
title: "H01 · Arranque directo de un motor trifásico · Trituradora de piedrín"
subtitle: "Guion para revisión · @miguelesquit · 21-nov-2026"
---

# Datos de diseño (decididos contigo)

| Dato | Valor | Fuente |
|---|---|---|
| Motor | 10 hp (7,5 kW), IEC 6 bornes, conexión **triángulo (Δ)** a 230 V | Placa del caso base |
| Corriente de placa | 24,3 A · F.S. 1,25 · 1760 rpm | Placa |
| Red | 240 V trifásica, 60 Hz | Caso base |
| Corriente de tabla | 28 A | NEC T430.250 |
| Conductor de potencia | 125 % × 28 A = 35 A → **10 AWG THHN 75 °C** | NEC 430.22 / T310.16 |
| Breaker del motor -Q1 | 250 % × 28 A = 70 A → **3P 70 A** | NEC T430.52 (tiempo inverso) |
| Relé térmico -F2 | máx. 125 % × 24,3 A = 30,4 A → **23–32 A ajustado a 24,3 A**, clase 10 | NEC 430.32(A)(1) |
| Contactor -KM1 | **32 A AC-3**, bobina 240 VAC, 1 NA + 1 NC | IEC 60947-4-1 |
| Protección del mando -F1 | **2P 6 A curva C**, conductor 14 AWG | NEC 430.72 |
| Mando | 240 VAC entre L1 y L2 | Caso base |

> **Referencia del usuario (21-nov):** lámina "Arranque directo de un motor trifásico" (Contec). Se usa SOLO como referencia de estructura y estilo: a la izquierda el esquema de conexión con los equipos físicos, a la derecha los diagramas IEC de potencia y mando con cada equipo resaltado en un recuadro de color. **Todos los equipos se dibujan con nuestra biblioteca.**
>
> Adaptaciones al caso del canal: en lugar del guardamotor va **breaker -Q1 + contactor -KM1 + relé térmico -F2**; el mando es a **240 VAC entre L1 y L2** con breaker **2P -F1** (la red del caso base no tiene neutro); el contacto **95-96 del térmico** va en serie antes del paro; sin pilotos, igual que la referencia.

Circuito de mando: L1 → -F1 (1-2) → -F2 (95-96) → -S1 paro (11-12) → -S2 marcha (13-14) en paralelo con -KM1 (13-14) → bobina -KM1 (A1-A2) → -F1 (4-3) → L2.

Circuito de potencia: -X0 (L1 L2 L3 PE) → -Q1 (1-2, 3-4, 5-6) → -KM1 (1/L1-2/T1, 3/L2-4/T2, 5/L3-6/T3) → -F2 (2/T1, 4/T2, 6/T3) → -X1 (U V W PE) → -M1 (U1 V1 W1, PE a la carcasa; puentes Δ U1-W2, V1-U2, W1-V2).

# Guion (voz) por sección

## 1. Gancho (0:00 – 0:20)
**Pantalla:** la trituradora arranca, el motor gira, se oye el breaker y luego el motor; zoom al breaker de 70 A.

**Voz:** "Este motor de diez caballos mueve una trituradora de piedrín… y la protección que casi todos ponen aquí está mal. Hoy te enseño a escogerla con números, a armar el mando y la potencia, y a conectarlo borne por borne, hasta ponerlo en marcha."

## 2. Justificar: la pregunta técnica (0:20 – 1:00)
**Pantalla:** pregunta en grande: "¿Si el motor consume 24,3 A, por qué el breaker es de 70 A?"

**Voz:** "Si el motor consume veinticuatro amperios, ¿por qué el breaker es de setenta? ¿No se quema el motor? La respuesta es no… porque el breaker no protege al motor de la sobrecarga: protege al cable del cortocircuito. Del motor se encarga otro equipo: el relé térmico. Y entender esa diferencia es lo que separa un tablero que dura años de uno que se dispara cada vez que arranca la trituradora."

## 3. Planteamiento del problema real (1:00 – 3:00)
**Pantalla:** placa del motor con zoom a HP, V, A, F.S.; tablas NEC apareciendo; cada resultado se escribe con sonido de escritura.

**Voz:**
"Todo empieza en la placa. Diez caballos, doscientos treinta voltios en triángulo, veinticuatro punto tres amperios, factor de servicio uno punto veinticinco.

Para el cable y el breaker la norma no usa la placa: usa la tabla cuatro treinta punto doscientos cincuenta. Para diez caballos a doscientos treinta voltios, veintiocho amperios.

El cable: ciento veinticinco por ciento de veintiocho… treinta y cinco amperios. Calibre diez AWG, THHN a setenta y cinco grados.

El breaker: la tabla cuatro treinta punto cincuenta y dos permite hasta doscientos cincuenta por ciento para un breaker de tiempo inverso. Setenta amperios, tripolar. Así aguanta la corriente de arranque, que en este motor llega a ciento sesenta y dos amperios, sin dispararse.

El térmico sí usa la placa: como el factor de servicio es uno punto veinticinco, el ajuste máximo es ciento veinticinco por ciento de veinticuatro punto tres: treinta punto cuatro amperios. Escogemos uno de veintitrés a treinta y dos y lo ajustamos a la corriente de placa: veinticuatro punto tres.

El contactor: categoría AC-tres, treinta y dos amperios, bobina a doscientos cuarenta voltios.

Y el mando lo protegemos aparte, con un breaker bipolar de seis amperios y cable catorce."

## 4. Lista de materiales (3:00 – 3:45)
**Pantalla:** tabla que se llena fila por fila; a la par aparece cada equipo del catálogo con su etiqueta amarilla.

| Cant. | Equipo | Características | Observación |
|---|---|---|---|
| 1 | Breaker -Q1 | 3P, 70 A, curva C | Protege el cable contra cortocircuito |
| 1 | Breaker -F1 | 2P, 6 A, curva C | Protege el mando |
| 1 | Contactor -KM1 | 32 A AC-3, bobina 240 VAC, 1NA+1NC | Maniobra el motor |
| 1 | Relé térmico -F2 | 23–32 A, clase 10 | Ajuste 24,3 A, reset manual |
| 1 | Pulsador -S1 | Rojo, bloque NC 11-12 | Paro |
| 1 | Pulsador -S2 | Verde, bloque NA 13-14 | Marcha |
| 1 | Borneras -X0, -X1, -X2 | Alimentación, motor y puerta | Con PE verde/amarillo |
| — | Cable | 10 AWG potencia (negro) · 14 AWG mando (rojo) · PE verde/amarillo | Con puntera y marcador |
| 1 | Motor -M1 | 10 hp, 230 V Δ, 24,3 A | Trituradora |

**Voz:** lectura breve de cada fila (solo nombre, capacidad y para qué sirve).

## 5. Diagrama de mando IEC (3:45 – 5:00)
**Pantalla:** diagrama de mando IEC al estilo de la referencia (vertical, cada equipo en un recuadro de color, nodos marcados), trazado línea por línea con sonido de escritura.

**Voz:** "Empezamos por el mando, que es el cerebro. La fase L1 entra por el breaker de seis amperios, pasa por el contacto cerrado del térmico, noventa y cinco–noventa y seis… si hay sobrecarga, este contacto se abre y todo se detiene. Luego el paro, normalmente cerrado. Luego la marcha, normalmente abierta… y en paralelo, el contacto trece–catorce del contactor: la retención. Al soltar la marcha, ese contacto mantiene la bobina energizada. La bobina, A1–A2, cierra el circuito hacia L2, por el segundo polo del breaker de mando."

## 6. Diagrama de potencia IEC (5:00 – 5:50)
**Pantalla:** diagrama de potencia IEC al estilo de la referencia, a la izquierda del de mando, trazo grueso.

**Voz:** "La potencia es más sencilla: las tres fases pasan por el breaker de setenta, por los contactos principales del contactor, por el térmico… y llegan al motor en U1, V1 y W1, con la tierra a la carcasa. En la caja de bornes, los puentes en triángulo: U1 con W2, V1 con U2 y W1 con V2."

## 7. Esquema de conexión del mando (5:50 – 8:00)
**Pantalla:** a la izquierda el diagrama de mando con el tramo resaltado; a la derecha los equipos del catálogo. Cada cable rojo se tiende de borne a borne con zoom, puntera y marcador con su número.

**Voz:** tramo por tramo, nombrando origen y destino ("del dos de -F1 al noventa y cinco de -F2…"), siguiendo exactamente tu diagrama.

## 8. Esquema de conexión de potencia (8:00 – 9:20)
**Pantalla:** igual que el 7, con cable negro 10 AWG y PE verde/amarillo; zoom en cada borne; al final el ajuste del dial del térmico a 24,3 A (zoom + sonido).

## 9. Pasarlo al cuadro eléctrico (9:20 – 10:30)
**Pantalla:** placa de montaje con riel DIN y canaleta; los equipos se montan en orden (-Q1, -F1, -KM1 con -F2 acoplado, borneras -X0/-X1/-X2); el cableado entra a la canaleta; los pulsadores y pilotos en la puerta.

**Voz:** criterios de armado: potencia arriba-abajo en el mismo sentido que el diagrama, mando separado, todo marcado.

## 10. Puesta en marcha (10:30 – 11:40)
**Pantalla:** verificaciones con multímetro como en las referencias: continuidad del mando con -Q1 abierto, aislamiento entre fases, tensión de llegada 240 V entre fases. Luego: -Q1 ON (sonido breaker), -F1 ON, marcha -S2 → contactor (sonido) → motor (sonido); medición con pinza ≈ corriente de trabajo; paro -S1. Simulación de sobrecarga con TEST del térmico (sonido de disparo): el contactor cae aunque se pulse marcha → RESET y vuelve a arrancar.

## 11. Cierre (11:40 – 12:00)
**Voz:** "Si te sirvió, suscríbete. En el siguiente video arrancamos este mismo motor con un variador de frecuencia. Y si quieres repasar rápido, te dejo los shorts de este tema."

> Sí conviene mencionar los shorts, pero en una sola frase y con las tarjetas en pantalla: ayudan a que el espectador siga en el canal sin alargar el cierre.

# Shorts propuestos (verticales, 1:30 – 3:30)
1. **Así funciona la retención de un contactor** (el 13–14 en paralelo con la marcha).
2. **Así se calcula la protección de un motor** (por qué 70 A en el breaker y 24,3 A en el térmico).
3. **Así funciona el relé térmico** (95–96 / 97–98, ajuste, TEST y RESET).

Cada short termina invitando a ver el video completo.

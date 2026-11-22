# Revisión H01 · Arranque directo · Trituradora de piedrín

## 1. Diseño
- Fondo negro con cuadrícula; cinta de sección fija que sigue a la cámara en los zooms.
- Todos los equipos salen de la biblioteca (`svgref.py` → `h01_eq/*.png` + bornes en JSON). Etiquetas amarillas de tamaño fijo.
- Diagramas IEC con recuadro de color por equipo (estilo de `referencias/H01_referencia_arranque_directo.jpg`).
- Rutas por "canaletas": cada hilo sale del borne hacia un carril y entra al borne destino; ningún hilo cruza la cara de un equipo salvo la entrada lateral al 95 de -F2 y las bajadas a la canaleta inferior (como en un tablero real).

## 2. Ingeniería, borne por borne
| Hilo | Desde | Hasta | Diagrama |
|---|---|---|---|
| 1 | -Q1:2 (L1) | -F1:1 | L1 → -F1 1 |
| 2 | -Q1:4 (L2) | -F1:3 | L2 → -F1 3 |
| 3 | -F1:2 | -F2:95 | -F1 2 → 95 |
| 4 | -F2:96 | -X2:1 → -S1 bloque NC 1 (11) | 96 → 11 |
| 5 | -S1 bloque 2 (12) | -X2:2 → -S2 bloque NA 3 (13) y -KM1:13 | 12 → 13 ∥ 13 |
| 6 | -S2 bloque 4 (14) | -X2:3 → -KM1:14 y -KM1:A1 | 14 ∥ 14 → A1 |
| 7 | -KM1:A2 | -F1:4 | A2 → -F1 4 → L2 |
| Pot. | -X0 L1 L2 L3 | -Q1 1 3 5 | ✔ |
| Pot. | -Q1 2 4 6 | -KM1 1/L1 3/L2 5/L3 | ✔ |
| Pot. | -F2 (pines) | -KM1 2/T1 4/T2 6/T3 | montaje directo ✔ |
| Pot. | -F2 2/T1 4/T2 6/T3 | -X1 U V W | ✔ |
| PE | -X0 PE | -X1 PE | verde/amarillo ✔ |

Capacidades (NEC 2020): T430.250 28 A · 430.22 → 35 A → 10 AWG THHN 75 °C · T430.52 → 70 A · 430.32(A)(1) → máx 30,4 A, ajuste 24,3 A · AC-3 32 A · mando 2P 6 A, 14 AWG (430.72(B), tomas dentro del tablero).
Motor IEC Δ: U1-W2, V1-U2, W1-V2.

Nota: el bloque de contacto físico rotula 1-2 (NC) y 3-4 (NA); en el esquema IEC del pulsador son 11-12 y 13-14 (regla del canal).

## 3. Docente
- Cada sección abre con su portadilla y tecleo; la voz lleva el orden: placa → norma → resultado.
- La pregunta del gancho (24 A vs 70 A) se responde en la sección 2 y se demuestra en la 3.
- La retención se anima con flujo de corriente; la prueba del térmico muestra que el paro por sobrecarga exige RESET.
- La lectura de la pinza se rotula "lectura de ejemplo" (no es un dato de placa).

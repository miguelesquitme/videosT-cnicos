# Revisión H23 · Mi primer arranque con contactores

## 1. Revisión de ingeniería eléctrica: tabla borne por borne

| Hilo | Origen | Destino | Conductor | Esquema |
|---|---|---|---|---|
| L1 L2 L3 | acometida (canaleta superior) | -Q1 1, 3, 5 | negro 14 AWG | t1 |
| — | -Q1 2, 4, 6 | -KM1 1/L1, 3/L2, 5/L3 (mismo orden de fases) | negro 14 AWG | t2 |
| — | -KM1 2/T1 4/T2 6/T3 + 14 + A2 | pines del -F2 (montaje directo, 5 pines) | — | t3 |
| U V W | -F2 2/T1 4/T2 6/T3 | -X1 U, V, W → motor U1, V1, W1 | negro 14 AWG | t4 |
| — | motor 230 V Δ | puentes U1-W2, V1-U2, W1-V2 | — | placa de bornes |
| PE | acometida → barra PE → -X1 PE → carcasa del motor | verde/amarillo | pe |
| — | L1/L2 acometida | -F1 1, 3 → -F1 2, 4 → -T1 L, N; -T1 PE a la barra | negro / verde-amarillo | alimentación del mando |
| 1 | -T1 + | -F2 95 (y puente 95 → 97) | azul | a0 / b0 |
| 2 | -F2 96 | -X1:1 → -S0 11 | azul | a1 |
| 3 | -S0 12 | -X1:2 → -S1 13 y -KM1 13 | azul | a2, a3, l1 |
| 4 | -S1 14 | -X1:3 → -KM1 A1; -F2 14/22 (repite el 14 del contactor) → A1 | azul | a4, l2, a5 |
| 0V | -F2 A2 (repite el A2 del contactor) | -T1 − | azul | a6 |
| 5 | -F2 98 | -X1:4 → -H1 X1 | azul | b1 |
| 0V | -H1 X2 | -X1:5 → -T1 − | azul | b2 |

Comprobaciones:
- La disposición de bornes del contactor coincide con la hoja de datos oficial: arriba 1/L1 3/L2 5/L3 13NO A1+; abajo 2/T1 4/T2 6/T3 14NO A2−.
- El relé S00 entra en 2/T1 4/T2 6/T3 14 A2 y repite A2 y 14/22, según el esquema del catálogo (3RU21 16: 95-96 NC, 97-98 NA, A2, 14/22).
- Mando: + → 95-96 → S0 (NC 11-12) → S1 (NA 13-14) ∥ KM1 13-14 → A1; A2 → 0 V. El autoenclavamiento queda en paralelo SOLO con S1, nunca con S0.
- Paro con contacto NC: al cortarse un cable, la máquina se detiene (IEC 60204-1).
- Q1: 4,2 A × 250 % = 10,5 A → 15 A (NEC Tabla 430.52 y 430.52(C)(1) Exc. 1). Conductores: 4,2 × 1,25 = 5,25 A → 14 AWG (430.22).
- F2: ajuste 3,9 A = corriente de placa; F.S. 1,15 permite hasta 125 % (430.32(A)(1)). Rango del relé 3,5–5 A: correcto.
- Contactor de 7 A AC-3 para un motor de 4,2 A: correcto.
- Motor 230 Δ / 400 Y con red de 230 V → triángulo: correcto. 3,9 A / √3 = 2,25 A: correcto.
- Bobina de 24 V DC a 4 W → R ≈ 144 Ω.
- Prueba en frío: se suelta el + de la fuente para no medir a través de ella (corregido antes de grabar la voz).
- Se cablea con Q1 y F1 en OFF (palancas abajo); se suben solo en "energizar".
- Designación: el contactor se deja como KM1 (Telesquemario) con nota en pantalla de que la IEC 81346-2 actual usa Q.

## 2. Revisión de diseño
- Fondo negro con cuadrícula. El tablero va sobre una placa gris claro para dar contraste a los equipos gris pizarra.
- El tablero quedó a la derecha (x 0,3 a 7,6) y el diagrama en una tarjeta a la izquierda; nada se corta.
- Corrección: los cables quedaban detrás de la placa (z-index) y desaparecían al salir del zoom. Ahora tienen z = 3 y el zoom es una transformación inversa exacta.
- Corrección: canaletas más separadas de los equipos para que se vea cada tramo de cable; marcador con número en cada punta.
- Corrección: al resaltar el diagrama, los números de bornes se volvían manchas; ahora solo se resaltan las líneas.
- Corrección: "+24 V" se encimaba con el título del esquema.
- Tarjetas y portadillas en negro; cinta de sección siempre arriba (z = 45).

## 3. Revisión docente
- El orden sigue el diagrama: leer → potencia (4 tramos) → mando (rama por rama) → prueba en frío → energizar.
- Cada tramo que se nombra en la voz se ilumina en el esquema y, al mismo tiempo, se cablea en el tablero con zoom.
- Léxico: autoenclavamiento, contacto normalmente cerrado, corriente de placa, conductor de protección, prueba en frío, orden de fases.
- Los 3 errores son los que se ven en campo: enclavamiento en paralelo con el paro, paro con contacto NA, térmico al máximo.

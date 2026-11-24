# Revisión H01 v5 (Correcciones_V, 23-nov)

## 1 · Diseño (punto por punto del Word)
| Punto | Qué pidió | Cómo quedó |
|---|---|---|
| 1-A | La parte negra le quita forma | `svgref.bloque`: adaptador negro cuadrado sin franjas laterales |
| 1-B | Contacto GRIS, tornillos originales | Columna de contacto gris claro, tornillos en cruz, ventana NC/NO/LED, leva, pestaña |
| 1-C | Cuadro del frente = cuadro trasero | KF = KD = 0,030; el cuadro del frente se coloca exactamente sobre el del bloque |
| 1-D | Frente solo al inicio | `c_intro_5`: se ve el frente, se dice que por temas didácticos se verá por detrás y la puerta "gira" |
| 2 | Borneras y riel nuevos, sin bordes, calibres | `svgref.bornera` (10 mm² potencia, N 2,5 mm²), riel metálico con ranuras sin bordes |
| 3 | Entrar por arriba/abajo | ENTRADAS v5: todas "u"/"d"; 13/21/A1 por arriba, 14/22/A2 por abajo, 95/96 por abajo |
| 4 | Curvas abiertas, espacio para el marcador | radio 0,2 y tramo recto ≥ puntera + marcador; en las J inferiores el marcador va en el tramo horizontal |
| 5 | Más espacio | Diagrama más pequeño, puerta a la derecha con pasillos, borneras bajo el térmico |
| 6 | Un hilo a la vez | 13 clips de mando + 10 de potencia, un cable por clip |
| 7 | Opacar lo ya conectado | `opacar()` antes de cada hilo (cable, punteras, marca en el diagrama) |
| 8 | Más lento | 2,8 s por cable + aros en origen y destino |
| 9 | Manguera TSJ y medición de corriente con zoom | TSJ 4 × 8 AWG; zoom a la caja del motor; pinza en T1 y forma incorrecta tachada |
| 10 | Continuidad bajo -F2 sin energía, fases y contra tierra | `frio_5`: 2-4, 4-6, 2-6, cada fase–PE: OL |

## 2 · Ingeniería borne por borne
- Mando (120 VAC): L en -F2:5 (= X0:1, L1) → F1:1 · F1:2 → KM1:21 y → F3:95 · F3:96 → S0:1(11) · S0:2(12) → S1:3(13) y → KM1:13 · S1:4(14) → KM1:14, → H1:X1 · KM1:14 → A1 · KM1:22 → H2:X1 · N: X0:4 → A2 → H1:X2 → H2:X2.
- Potencia literal del diagrama del usuario: X0:1 (L1) → F2:5, X0:2 → F2:3, X0:3 → F2:1; F2 2/4/6 → KM1 1/3/5; F3 2/4/6 → X1 1/2/3; PE X0:5 → X1:4; TSJ X1 → M1 T1 T2 T3 + PE.
- Prueba en frío: con KM1 abierto, entre salidas de F2 no hay carga → OL; fases–PE → OL. La L del mando se toma en la ENTRADA de F2, no afecta la prueba.
- Prueba del mando en ohmios desde el hilo 3 (no desde el 2: por el 21-22 NC siempre hay camino por H2).
- Corriente: pinza en un solo conductor; en la manguera completa la suma vectorial ≈ 0.

## 3 · Docente
- Cada clip nombra origen, destino y si entra por arriba o por abajo; los aros marcan ambos extremos.
- Duda abierta para el usuario: el diagrama original lleva L3 a la entrada 1 y L1 a la entrada 5 de -F2 (se siguió literal).

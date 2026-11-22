# Revisión H01 v2 · Arranque directo · Trituradora de piedrín (22-nov)

Archivos: `h01v2.py` (escena), `h01v2_diag.py` (diagramas literales del usuario), `h01v2_lay.py` (equipos y cables), `h01_guion.py`, equipos en `h01v2_eq/`.

## 1. Diseño
- Fondo negro con cuadrícula; cinta de sección. Diagramas sobre HOJA BLANCA, recreados literal del usuario (mando image6, potencia image5): líneas de mando granate, neutro azul, PE verde punteado, símbolos negros, rótulos turquesa. Mando con trazo más fino (2,2) que potencia (3,0).
- Diagramas dibujados TRAMO POR TRAMO (línea → símbolo → línea), con la voz explicando cada tramo y una nota a la derecha.
- Conexión: equipos más pequeños (0,026 u/mm) sobre plancha naranja; puerta gris con los bloques de contacto (punto de conexión real) y el frente de cada operador. Cables con esquinas redondeadas, puntera (pin + collar DIN 46228-4) que entra DEBAJO del tornillo (la cabeza del tornillo se dibuja encima), marcador blanco con el número IEC. Mientras se tiende cada cable, el mismo tramo se marca en el diagrama.
- Tablero real por etapas: gabinete 500×400×200 → plancha → canaletas ranuradas 40×40 → rieles DIN + tornillos → equipos → puerta → cableado a canaleta. En la puesta en marcha el tablero se reduce y se ven el motor, el multímetro y la pinza.

## 2. Ingeniería, borne por borne
| Hilo | Desde | Hasta | Diagrama |
|---|---|---|---|
| 1 | -F2:1 (entrada L1, decisión del usuario) | -F1:1 | -X0 L → -F1 1 |
| 2 | -F1:2 | -F3:95 (acceso por abajo) y puente 95 → -KM1:21 | -F1 2 → 95 · nodo → 21 |
| 3 | -F3:96 (baja entre 4/T2 y 6/T3) | -S0 bloque 1 (11) | 96 → 11 |
| 4 | -S0 bloque 2 (12) | puente a -S1 bloque 3 (13) y regreso a -KM1:13 | 12 → 13 ∥ 13 |
| 5 | -S1 bloque 4 (14) | -KM1:14 → puente a A1 · puente a -H1:X1 | 14 ∥ 14 → A1 ∥ X1 |
| 6 | -KM1:22 | -H2:X1 | 22 → X1 |
| N | -X0:4 | -KM1:A2 → -H1:X2 → -H2:X2 | A2, X2, X2 → N |
| L1 L2 L3 | -X0:1 2 3 | -F2:1 3 5 | ✔ |
| L1 L2 L3 | -F2:2 4 6 | -KM1 1/L1 3/L2 5/L3 | ✔ |
| — | -F3 pines | -KM1 2/T1 4/T2 6/T3 | montaje directo ✔ |
| T1 T2 T3 | -F3 2/T1 4/T2 6/T3 | -X1:1 2 3 | ✔ |
| PE | -X0:5 | -X1:4 | ✔ |
| Motor | -X1:1 2 3 → T1 T2 T3 | T1-T7 · T2-T8 · T3-T9 · T4-T5-T6 (Y 9 puntas, baja) | confirmar con la placa |

Capacidades (NEC 2020, 208 V): T430.250 30,8 A · 430.22 38,5 A → 8 AWG THHN 75 °C · T430.52 77 A → C80 · 430.32(A)(1) máx 33,1 A, ajuste 26,5 A (rango 23–32) · contactor 38 A AC-3 (10 hp a 200/208 V UL; el de 32 A solo 7,5 hp) bobina 120 VAC · -F1 1P C2 · mando 14 AWG · PE 8 AWG (T250.122 para 80 A) · rotor bloqueado T430.251(B) 178 A.
Bloques de pulsador: físico 1-2 (NC) y 3-4 (NA); en el diagrama 11-12 y 13-14.

## 3. Docente
- Gancho con dato curioso (×7 al arrancar) y pregunta; sin insinuar que otros lo hacen mal. Eje del motor girando, sin arcos.
- Datos de placa encerrados en rectángulos mientras la voz los nombra.
- Lista de materiales en tabla Cantidad | Nombre | Características | Observación; borneras contadas del diagrama (6 grises, 1 azul, 2 PE, 4 separadores); cable aproximado por ítem; riel, canaleta y gabinete.
- La voz nunca dice "menos" por el guion de la designación.
- Cierre sin tarjeta de shorts ni tema del siguiente video.

# Lote H · 5 dispositivos × 6 infografías (25-nov-2026) — `manim/posts13/gen.py`
Fotos: larssystemgt.com (usadas a pedido del autor, con crédito): NS2-25X /6160, NXB-63 2P C40 /10146, Relpol R2N /50900, Autonics PR12-2DP /37750, NOARK Ex9C50 /4060. Bajadas con el navegador integrado (fetch → base64). Las de 510 px se ampliaron ×2 con enfoque.

| Equipo | Datos | Fuente |
|---|---|---|
| CHINT NS2-25X 9–14 A | In 14 A, Ii 170 A, Icu 15 kA/400 V, 3 kA/690 V, Ics 7,5 kA/400 V, 5,5 kW/400 V, Ui 690 V, Uimp 8 kV; clase 10A: 1,05× no dispara 2 h, 1,2× < 2 h, 1,5× < 2 min, 7,2× 2–10 s; falta de fase 2 fases 1,15× → < 2 h; auxiliares NS2-AE11/AE20, AU11/AU20 | CHINT NS2 catálogo (lemona.lt/NS2.pdf), TÜV, placa lateral (Icu 100 kA a 230/240 V, 3 kW a 230 V) |
| Schneider GV2ME16 | 9–14 A, 170 A, Icu 100/15/3 kA (230/400/690 V), Uimp 6 kV, pulsadores, 5,5 kW/400 V, 3 kW/230 V | hojas de datos Schneider (se.com, RS, Mouser) |
| CHINT NXB-63 | Icn 6000/10000 A, Ui 500 V, Uimp 4 kV, vida 10 000 eléctrica / 20 000 mecánica, curvas B/C/D | catálogo CHINT NXB-63; IEC 60898-1 (C 5–10 In; 1,13/1,45 In en 1 h; 2,55 In 1–120 s para In > 32 A) |
| ABB S202-C40 | 40 A C 6 kA, Uimp 4 kV, IEC 60898-1 + IEC 60947-2 + UL 1077, 440 V máx., vida 10 000/20 000 | hojas ABB (RS, Farnell, materielelectrique) |
| Relpol R2N 2CO 230 VAC | 12 A/250 VAC AC1, 3000 VA, AC15 3 A/120 V · 1,5 A/240 V (B300), DC1 12 A/24 V, mín. 10 V/5 mA, bobina 184–253 V 1,6 VA (50 Hz), vida 10^5 AC1, 2×10^7 mecánica, 2,5 kV / 4 kV, 27,4 × 21 × 35,5 mm, −40…+55 °C (AC), zócalos GZT2/GZM2, WTL, botón naranja = AC | Relpol e_R2N.pdf, RS, Onninen; numeración impresa en el relé (11=9, 12=1, 14=5, 41=12, 42=4, 44=8, A1=13, A2=14) |
| Finder 56.32.8.230.0040 | 12 A, 3000 VA, 1,5 VA, 184–253 V, 10^5 ciclos, 4 kV, 0040 = botón bloqueable + indicador, zócalos serie 96 | Finder S56 / T5632, RS, Conrad |
| Autonics PR12-2DP | 2 mm, M12, enrasado, 12–24 VDC (10–30), 10 mA, 1,5 kHz, 200 mA, residual 1,5 V, LED rojo, IP67, hierro 12×12×1, ajuste 0–1,4 mm | catálogo Autonics PR (manualmachine, tequipment, chipdip) |
| Omron E2B-M12KS02-WP-B1 | 2 mm PNP NA, 10–30 VDC, 1,5 kHz, 200 mA, residual 2 V, LED amarillo, 10 mA | ia.omron.com especificaciones E2B, RS |
| NOARK Ex9C50 | placa: AC-3 50 A (230/400 V), 15/22 kW, Ui 1000 V, Uimp 8 kV, Ith 80 A, 15 hp 208 V · 20 hp 240 V (3~), 14–4 AWG, 6 N·m, UL 5 kA con fusibles; hoja: cierre 0,85–1,1 Uc, apertura 0,20–0,75 Uc, 10×10^6 mecánica, 1NA+1NC = 13-14/21-22 | NOARK Ex9C datasheet (wolfautomation), placa del equipo |
| Schneider LC1D50AM7 | 50 A AC-3, 80 A AC-1, 15 kW/230 V, 22 kW/400 V, 15 hp 208 V, 1NA+1NC, apertura 0,3–0,6 Uc, 6 Mciclos mecánica | hojas Schneider (se.com, w11stop, RS) |
| NEC 2020 | T430.250 (3 hp 208 V = 10,6 A; 15 hp = 46,2 A), 430.22, 430.32, 430.52, 240.4(D), 210.19/20, T310.16 | NFPA 70 |

## Discrepancias / notas
- El R2N NO es relé octal: bornes 11-12-14 / 41-42-44 / A1-A2 (impreso; EN 50005). El símbolo de 8 pines del catálogo (bobina 2-7) no aplica: se armó con `simsvg.bobina` + `conmutado`.
- El NS2-25X no indica en la hoja si está listado como "Tipo E" (NEC): se advierte.
- Datos de bobina VA y vida eléctrica del Ex9C50 no se usaron: la tabla del PDF tiene columnas ambiguas.
- Las curvas de H02/H08 y la amplitud de H20 son FORMA ILUSTRATIVA; los puntos marcados son los de la norma/fabricante.

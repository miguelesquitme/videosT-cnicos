# Lote E · Relé térmico CHINT NR2-25 9–13 A (25-nov-2026) — `manim/posts11/gen.py`
Producto de referencia del usuario: larssystemgt.com/1347 (RELE TERMICO NR2-25-9-13A CHINT).

## Fuentes
- PDF CHINT NR2 Thermal Overload Relay (mantech.co.za/Datasheets/Products/nr2_chint.pdf): clase 10A, tabla 4.1 (1,05/1,2/1,5/7,2 Ir), aux 1NA+1NC, AC-15 2,73 A 220 V / 1,58 A 380 V, DC-13 0,2 A, fusible 9–13 A aM 16 / gG 25.
- PDF CHINT NR2 (lemona.lt/Files/Instrukcijos/Pdf/NR2.pdf): mismas tablas, rangos 4–6 · 5,5–8 · 7–10 · 9–13 · 12–18 · 17–25, contactores NC1-09…32 / NC7, base MB-2.
- CHINT NR2 User Instruction 2020.04 (manuals.online): −5…+40 °C, Ui 690 V, Uimp 6 kV, bornes 95-96 NC / 97-98 NA, ajuste con leva.
- Web: chintglobal.com NR2 (pérdida de fase, H/A, enchufable o MB) · larssystemgt.com/1347.
- Schneider LRD16: ficha PDF (clase 10A, 9–13 A, 690 V/6 kV, AC-15 1,5 A 240 V, −20…+60 °C, LC1D12–D38, 130 % Ir pérdida de fase) · se.com LRD16 · FAQ FA28091 (H/A) · RS 394-9346.
- Funcionamiento: Schneider FAQ FA364937 (bimetal, diferencial de pérdida de fase) · viox.com · IEC 60947-4-1.
- Aplicación: Baldor VM3661T-9 info packet (3 hp, 208-230/460 V, 9,6-8,8/4,4 A, SF 1,15) · NEC 430.32(A)(1).
- Símbolo: lib/simsvg (congelado) · IEC 60617 · IEC 81346-2 · EN 50005.

## Discrepancias
- gG para 9–13 A: el PDF de lemona da 16 A en una tabla y 25 A en otra; mantech y Larssystem dan aM 16 / gG 25 → se usó 16/25.
- Foto del producto: la página de Larssystem no se pudo descargar (contenedor sin acceso, PC desconectada) → ilustración del catálogo con dial 9–13 A.

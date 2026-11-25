# Lote C (25-nov) · 10 imágenes · fuentes cruzadas (2 PDF + 2 páginas web por tema)

Regla del lote: SIN símbolos IEC dibujados a mano (fue el error del lote B). Solo datos de norma, gráficos simples, tablas, tarjetas de color y fotos reales de Commons.

## C01 · IP65 (IEC 60529)
- PDF 1: Rolec, "Info IP65 EN" (EN 60529): IP6X vacío ≤ 2 kPa, 8 h, talco · IPX5 12,5 L/min ± 5 %, ≥ 3 min, 2,5–3 m.
- PDF 2: HellermannTyton, brochure helaguard p.143 (DIN EN IEC 60529): 6 = hermético al polvo, 5 = chorro de agua desde cualquier dirección.
- Web 1: bopla.de, "IP 65 to DIN EN 60529": primer dígito protege personas y equipo; segundo solo agua.
- Web 2: newark.com, IP ratings: 5 = boquilla 6,3 mm; 6 = boquilla 12,5 mm.
- Coinciden. (La presión 30 kPa solo aparece en 2 webs; no se usó.)

## C02 · Clase de aislamiento F = 155 °C
- PDF 1: NEMA, "NEMA motor standards vs IEC motor standards": A 105, E 120, B 130, F 155, H 180 °C; elevación por resistencia (40 °C amb.) B 80, F 105, H 125 K (SF 1,0); con SF ≥ 1,15: B 90, F 115.
- PDF 2: Toshiba, Tech Notes "Temperature Rise": 105 + 40 = 145 °C; 10 °C de margen de punto caliente hasta 155 °C.
- Web 1: ABB, "How to read a NEMA motor nameplate": B 80, F 105, H 125 K; común: aislamiento F con elevación B.
- Web 2: Engineering ToolBox, NEMA insulation classes: 40 + 105 + 10 = 155 °C.
- Coinciden.

## C03 · Factor de servicio 1,15 (NEMA MG 1)
- PDF 1: Baldor/ABB 9AKK108388 (placa NEMA): sobrecarga continua hasta hp × FS; a gran altitud el FS efectivo baja a 1,0.
- PDF 2: NEMA vs IEC (PDF): IEC no reconoce el FS; el motor trabaja más caliente.
- PDF extra: Baldor 9AKK106886: motores Inverter/Vector Duty con FS 1,0.
- Web 1: ABB (artículo placa NEMA): 10 hp × 1,15 = 11,5 hp; MG 1 9.15.1 menor vida; sobre 3300 ft FS efectivo 1,0.
- Web 2: PetroWiki "Motor specifications": 30 hp × 1,15 = 34,5 hp.
- Coinciden. Nota: 3300 ft ≈ 1000 m (conversión nuestra); Ciudad de Guatemala ≈ 1500 m.

## C04 · Riel DIN TH35 (IEC 60715)
- PDF 1: Phoenix Contact NS 35/7,5 PERF (0843103): ancho 35, interior 27, fondo 7,5, ranura 15 × 6,2, paso 25 mm, espesor 1.
- PDF 2: Phoenix Contact NS 35/15 (1207655 / 1207695): ancho 35, interior 27, fondo 15, "similar a EN 60715".
- PDF extra: IEC 60715:2017 (índice): TH 35-7,5 y TH 35-15. Weidmüller TS35x7.5 (fondo 7,5).
- Web 1: Wikipedia "DIN rail": IEC/EN 60715 35 × 7,5 y 35 × 15; antes DIN 46277-3 / EN 50022.
- Web 2: Rittal "Support rails to EN 60715": TH 35/7,5 y TH 35/15. Electropedia: TH35-15 = altura 15 mm sobre el plano.
- Coinciden. Espesor del 35 × 15 no se dio (los dibujos no son claros).

## C05 · Bobina del contactor 85–110 % Us (IEC 60947-4-1)
- PDF 1: ENEC, guía de ensayos IEC/EN 60947-4-1: cierra bien a 85 % Us y a 110 % Us.
- PDF 2: Schneider, ficha TeSys D (RS): 0,85…1,1 Uc funcionamiento; suelta 0,3…0,6 Uc.
- Web 1: ABB, catálogo Motor Protection & Control (contactor relay): 0,85…1,1 × Uc; drop-out 20…75 %.
- Web 2: CR4 GlobalSpec (cita 60947-4-1): suelta AC entre 75 % y 20 %, DC entre 75 % y 10 %.
- Coinciden. Schneider suelta entre 30 y 60 % (dentro del rango de la norma).

## C06 · Sensor inductivo sa ≤ 0,81 sn (IEC 60947-5-2)
- PDF 1: Pepperl+Fuchs, catálogo Sensors and Systems p.32: 0 < sa ≤ 0,81 sn; H ≤ 0,2 sr; apagado seguro a 3 sn.
- PDF 2: Bernstein/Altech "A1 Inductive General": sr 90–110 %; sa 0–81 % sn.
- PDF extra: SICK IHM06-02BPSVT0S: sn 2 mm, sa 1,62 mm (= 0,81 × 2).
- Web 1: Pepperl+Fuchs gp28808: 0,9 sn ≤ sr ≤ 1,1 sn; placa estándar.
- Web 2: Baumer, Know-how inductivos: sa entre 0 y 81 % de sn; placa = diámetro o 3 sn.
- Coinciden. 0,81 = 0,9 × 0,9 (sr mín. × su mín.), deducción de las definiciones.

## C07 · Colores de conductores IEC 60204-1
- PDF 1: Siemens, "Control Panels compliant with IEC" 6.8.1: negro potencia CA/CC, rojo mando CA, azul mando CC, naranja circuitos exceptuados; N azul claro; PE verde-amarillo.
- PDF 2: PPMA/IET "Cable colours in machines": negro, rojo, azul, naranja (enclavamientos con fuente externa), azul claro N, verde-amarillo PE.
- Web 1: industrialmonitordirect (13.2.4): negro, rojo, azul, naranja = exceptuados 5.3.5.
- Web 2: wevolver/Rowse: naranja = enclavamientos alimentados desde fuente externa; N azul claro; PE verde-amarillo.
- Coinciden (naranja: la edición vieja dice "enclavamiento externo", la nueva "circuitos exceptuados": ambos siguen con tensión con el seccionador abierto).

## C08 · Punteras DIN 46228-4 código de colores
- PDF 1: Phoenix Contact, tabla DIN 46228-4 vs NF C 63-023: 0,5 blanco, 0,75 gris, 1 rojo, 1,5 negro, 2,5 azul, 4 gris, 6 amarillo, 10 rojo, 16 azul.
- PDF 2: Rapid 06-3117 (surtido "DIN color code"): 0,5 blanco, 0,75 gris, 1 rojo, 1,5 negro, 2,5 azul, 4 gris, 6 amarillo, 10 rojo.
- Web 1: industrialmonitordirect, "DIN ferrule color coding": misma tabla.
- Web 2: Bossard, surtido código DIN: 0,5 blanco, 0,75 gris, 1 rojo, 1,5 negro, 2,5 azul.
- DISCREPANCIA: Rapid 33-1285 llama "German type" a otra tabla (0,5 naranja, 0,75 blanco, 1 amarillo, 1,5 rojo…), que en Phoenix es un "código especial", NO DIN 46228-4. Se usa la de Phoenix (fabricante + 3 fuentes).
- 0,25 y 0,34 mm² NO están en la norma DIN (Phoenix los marca con *): no se ponen.

## C09 · NEC 240.4(D) conductores pequeños
- PDF 1: Mike Holt, NEC 2023 cap. 240 (12 AWG Cu 20 A, 10 AWG Cu 30 A).
- PDF 2: Mike Holt, "Conductor sizing and protection": 15 A n.º 14, 20 A n.º 12, 30 A n.º 10.
- Web 1: EC&M "Conductor sizing part 1": lista (1)–(7), 14 Cu 15 A, 12 Cu 20 A, 10 Cu 30 A.
- Web 2: Encore Wire, Wire ampacity table (nota *): misma regla.
- Tabla 310.16 columna 90 °C: 14 = 25 A, 12 = 30 A, 10 = 40 A (open-exam-prep, buyawg, Scribd). Coinciden.
- No se usó la columna 60 °C del 14 AWG: hay fuentes viejas con 20 A y nuevas con 15 A.

## C10 · NEC 110.14(C) temperatura de terminales
- PDF 1: Eaton/Bussmann, "Conductor ampacities": ≤ 100 A usar 60 °C; motores diseño B, C, D: 75 °C.
- PDF 2: Mike Holt (muestra): 50 A en terminal 60 °C → 6 AWG (55 A); terminal 75 °C → 8 AWG (50 A).
- Web 1: Schneider 0110DB9901: ≤ 100 A o 14–1 AWG / > 100 A tabla de combinaciones.
- Web 2: EC&M "Codes standards: widen pipe": ≤ 100 A o 14–1 AWG → 60 °C; > 100 A o > 1 AWG → 75 °C.
- Coinciden.

# Lote G · equipos en 3D y foto real (25-nov-2026) — `manim/posts12/gen.py`
Render: STEP → GLB (`lib/visor3d/step2glb.py`, cascadio) → three.js (`manim/posts12/modelos/hq.html` + `hq.js`, devuelve la posición en pantalla de cada pieza).

| Imagen | Modelo / foto | Autor y licencia | Datos |
|---|---|---|---|
| G01 paro de emergencia | FreeCAD Parts Library, EmergencyButton-Disk_LAY37 | AngelLM, CC BY 3.0 | IEC 60204-1, ISO 13850, IEC 60947-5-5; LAY37-11ZS 1NA+1NC 10 A 660 V, montaje 22 mm |
| G02 pulsador verde | FreeCAD, Green Push-button 22 mm | Henrique Enzweiler, CC BY 3.0 | Ø22,3 mm (EAO, Omron A22NN, Eaton RMQ-Titan), IEC 60204-1 colores, IEC 60947-5-1 |
| G03 hongo rojo | FreeCAD, Red mushroom head push button 22 mm | Henrique Enzweiler, CC BY 3.0 | IEC 60204-1 (rojo permitido para paro), ISO 13850 / IEC 60947-5-5 (emergencia enclava) |
| G04 fuente conmutada | FreeCAD, Switching power supply (genérico) | Henrique Enzweiler, CC BY 3.0 | Ejemplo Mean Well LRS-350-24: 24 V 14,6 A 350 W, ADJ 21,6–28,8 V, 115/230 VAC por selector, protecciones |
| G05 sensor inductivo | FreeCAD, Inductive-Proximity-Sensor (genérico) | fran6t, CC BY 3.0 | IEC 60947-5-2 (BN/BU/BK), Sn M12 2/4 mm (P+F, Omron, lote D) |
| G06 contactor Siemens | Siemens Industry Bilddatenbank: render G_NSA0_XX_00822, dibujo G_NSA0_XX_00821/00823, STEP G_NSA0_XX_00834 | Siemens AG (descarga gratuita) | SiePortal 3RT2015-1AP01: AC-3e/AC-3 7 A, 3 kW/400 V, 230 VAC, 1NA, S00; 45 × 57,5 × 73 mm |
| G07 NR2-25 | Fotos larssystemgt.com/1347 (1 frente, 2 lateral) | LARSSYSTEM Guatemala, usadas a pedido del usuario | CHINT NR2 PDF y manual (ver loteE_fuentes.md) |

## Notas
- El breaker Schneider EZ9F16110 de FreeCAD es un solo sólido muy simple: se descartó por baja calidad.
- Autoría de FreeCAD sacada del historial git (LICENSE-Assets lo indica); la propiedad "License" de los FCStd dice "All rights reserved" por defecto, pero el repositorio la cubre con CC BY 3.0.
- La foto de Larssystem es de baja resolución (510 × 480) y lleva marca de agua; no se puede convertir en 3D fiel.

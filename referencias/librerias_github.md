# Librerías de componentes eléctricos en GitHub (25-nov-2026)
Clonadas en el contenedor en `/home/claude/libs` (no se suben al repo por tamaño). Muestra: `muestra_librerias_github.png`.

| # | Repo | Licencia | Contenido | Utilidad |
|---|---|---|---|---|
| 1 | qelectrotech/qelectrotech-elements | uso libre sin condiciones | 9 028 símbolos IEC (.elmt XML) + artículos de 120 marcas | ★★★★★ diagramas; `lib/elmt2svg.py` los pasa a SVG |
| 2 | FreeCAD/FreeCAD-library (Electrical Parts) | CC BY 3.0 | 3D STEP/STL: breaker Schneider EZ9F16110, pulsadores 22 mm, LAY37, fuentes | ★★★★ 3D (sin color) |
| 3 | davillenah/291_E_IEC60617_Symbols_Generator | MIT | 226 SVG/DXF unifilar/multifilar BT | ★★★★ tableros |
| 4 | chille/electricalsymbols | CC BY-SA 3.0 | 33 SVG de mando IEC | ★★★ |
| 5 | cdelker/schemdraw · circuitikz/circuitikz | MIT · LPPL | circuitos por código (estilo IEC/europeo) | ★★★ |
| 6 | KarelT1/KiCad-IEC-60617 · rjardina/Jardina (GPL-2) · bzarek/draw.io-electrical · Mr-FuzzyPenguin/manim-circuit (MIT) | varias | KiCad, draw.io, Manim (electrónica) | ★★ |
Ojo: la simbología del canal sigue congelada en `lib/simsvg.py`; estas librerías son consulta/opción, no reemplazo sin aprobación del usuario.

## Equipos 2D/3D (contactores, térmicos, guardamotores, PLC) — 25-nov
- 3D libres: FreeCAD-library (CC BY 3.0: breaker EZ9F16110, LAY37, pulsadores 22 mm, fuentes) · KiCad packages3D (CC BY-SA 4.0: relés Finder/Omron de placa, borneras Phoenix).
- 3D SIN licencia (solo referencia): MrCong1/contactor-3d-viewer (contactor GLB con texturas), shinelu308/switchgear-3d-viewer (celda). Samadsia/Synthetic-Data-Generation = fotos Siemens (no usar). etn-ccis/blui-icons = Eaton propietario (no usar).
- 2D libres: QElectroTech `98_graphics/99_assembly_plan` = vistas frontales (LC1D09, LRD, CAD32, ATV12, M221, ABB S20x, Siemens, Eaton, Omron, Finder, pulsadores) → `lib/elmt2svg.py`.
- Mejores modelos reales: portales de fabricante (Schneider se.com CAD, Siemens SiePortal/CAx, ABB, WEG, Eaton, Rockwell, CHINT), TraceParts/3Dfindit, GrabCAD, Sketchfab (CC BY). El contenedor no llega a esos sitios: el usuario baja el .stp y se convierte con `lib/visor3d/step2glb.py` + `visor_glb.html`/`render_glb.js` (servidor local en la carpeta del modelo).

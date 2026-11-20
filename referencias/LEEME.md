# Referencias de equipos

Cada equipo se recrea con la forma y los bornes de su documentación oficial, sin logo ni nombre comercial.
No se suben los PDF (tienen copyright): solo el enlace y lo que se tomó de cada uno.

| Pieza (`manim/piezas_siemens.py`) | Documento | Datos usados |
|---|---|---|
| `contactor_s00` | Hoja de datos del contactor S00, 7 A AC-3, 24 V DC, 1 NA ([PDF](https://www.mouser.lt/datasheet/3/5917/5/3RT20151BB41_datasheet_en.pdf)), págs. 1, 7 y 8 | 45 × 58 × 73 mm. Arriba: 1/L1 3/L2 5/L3 13NO A1+. Abajo: 2/T1 4/T2 6/T3 14NO A2−. Bobina de 4 W. Conductor de 0,5–4 mm². Designación IEC 81346-2: Q |
| `termico_s00` | Catálogo del relé térmico clase 10 ([PDF](https://cdn.shopify.com/s/files/1/0276/0700/7329/files/siemens-3RU21-catalog.pdf)), págs. 3/15 y 3/16 | 45 × 61,7 mm. 5 pines (2/T1 4/T2 6/T3 14 A2). 95-96 NC, 97-98 NA. Repite A2 y 14/22. TEST, STOP y RESET M/A. Rangos 3,5–5 / 4,5–6,3 / 5,5–8 / 7–10 A |
| (próximo) módulo lógico | Hoja de datos 12/24 RCE ([PDF](https://www.mouser.com/datasheet/2/1412/6ED10521MD080BA1_datasheet_en-3271159.pdf)) | 71,5 × 90 × 60 mm. 8 entradas (4 analógicas de 0–10 V). 4 salidas a relé de 10 A resistiva / 3 A inductiva |
| (próximo) variador compacto | Instrucciones de servicio del variador compacto ([PDF](https://cache.industry.siemens.com/dl/files/317/109751317/att_931919/v1/G120C_op_instr_0917_en-US.pdf)) | Tamaño AA de 73 × 181 mm. Bornes de potencia abajo. Panel -X21, USB -X22. Ajuste de fábrica 12 (E/S estándar con consigna analógica) |

Estilo visual: equipos planos en gris pizarra, etiquetas turquesa y diagramas limpios (Word de referencia del usuario, 19-nov-2026). Fondo negro con cuadrícula en verticales y horizontales.

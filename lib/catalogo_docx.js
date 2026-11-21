// Catálogo de componentes @miguelesquit en Word: equipo | símbolo IEC | datos técnicos.
// Uso: node catalogo_docx.js items.json carpeta_imagenes salida.docx
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  PageOrientation, HeadingLevel, LevelFormat, BorderStyle, VerticalAlign, PageBreak, Footer, PageNumber } = require("docx");

const [, , itemsPath, imgDir, salida] = process.argv;
const items = JSON.parse(fs.readFileSync(itemsPath, "utf8"));
const TURQ = "1BA8C4", OSC = "1D2939", GRIS = "F2F4F7", BORDE = "D0D5DD";

const borde = { style: BorderStyle.SINGLE, size: 4, color: BORDE };
const bordes = { top: borde, bottom: borde, left: borde, right: borde };
const W_TABLA = 13680;            // carta horizontal con márgenes de 0,75"
const COLS = [3900, 3900, 5880];

function img(file, wMax, hMax = 230) {
  const p = path.join(imgDir, file);
  if (!fs.existsSync(p)) return null;
  const data = fs.readFileSync(p);
  const w = data.readUInt32BE(16), h = data.readUInt32BE(20);
  if (w < 60 && h < 60) return null;
  const f = Math.min(wMax / w, hMax / h);
  return new ImageRun({ type: "png", data, transformation: { width: Math.round(w * f), height: Math.round(h * f) } });
}
const P = (runs, opts = {}) => new Paragraph({ children: Array.isArray(runs) ? runs : [runs], spacing: { after: 60 }, ...opts });
const T = (t, o = {}) => new TextRun({ text: t, font: "Arial", size: 19, color: OSC, ...o });

function filaEncabezado() {
  const cel = (t, w) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: bordes, shading: { fill: OSC, type: ShadingType.CLEAR, color: "auto" },
    margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: [P(T(t, { bold: true, color: "FFFFFF", size: 20 }), { alignment: AlignmentType.CENTER })] });
  return new TableRow({ tableHeader: true, children: [cel("Equipo (dibujo del canal)", COLS[0]), cel("Símbolo IEC", COLS[1]), cel("Datos técnicos", COLS[2])] });
}

function filaItem(it, n) {
  const imE = img(`${it.id}_equipo.png`, 250), imS = img(`${it.id}_simbolo.png`, 250);
  const celImg = (im, w) => new TableCell({ width: { size: w, type: WidthType.DXA }, borders: bordes, verticalAlign: VerticalAlign.CENTER,
    margins: { top: 80, bottom: 80, left: 80, right: 80 },
    children: [im ? P(im, { alignment: AlignmentType.CENTER }) : P(T("— (no aplica)", { italics: true, color: "667085" }), { alignment: AlignmentType.CENTER })] });
  const datos = [
    P([T(`${n}. ${it.nombre}`, { bold: true, size: 24, color: OSC })], { spacing: { after: 80 } }),
    P([T("Se identifica con: ", { bold: true }), T(it.desig, { bold: true, color: TURQ })]),
    P([T("Bornes: ", { bold: true }), T(it.bornes)]),
    ...it.datos.map(d => new Paragraph({ numbering: { reference: "vinetas", level: 0 }, spacing: { after: 40 }, children: [T(d)] })),
  ];
  if (it.notas) datos.push(P([T("Notas: ", { bold: true }), T(it.notas)], { spacing: { before: 60, after: 60 } }));
  if (it.fuente) datos.push(P([T("Fuente: ", { bold: true, color: "667085", size: 16 }), T(it.fuente, { color: "667085", size: 16 })]));
  datos.push(P([T("Tus correcciones: ", { bold: true, color: "B42318" }), T("______________________________________________", { color: "98A2B3" })], { spacing: { before: 80 } }));
  return new TableRow({ cantSplit: true, children: [celImg(imE, COLS[0]), celImg(imS, COLS[1]),
    new TableCell({ width: { size: COLS[2], type: WidthType.DXA }, borders: bordes, margins: { top: 100, bottom: 100, left: 160, right: 160 }, children: datos })] });
}

const intro = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun({ text: "Catálogo de componentes y símbolos IEC", font: "Arial", size: 44, bold: true, color: OSC })] }),
  P([T("Canal @miguelesquit · versión 3 para revisión · 21-nov-2026", { color: TURQ, bold: true, size: 22 })], { spacing: { after: 200 } }),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "Cómo leer este documento", font: "Arial", size: 28, bold: true, color: OSC })] }),
  ...[
    "Cada fila: el equipo calcado de tus referencias en estilo plano, esquinas rectas y sombras definidas (equipos blancos; solo los PLC en gris), su símbolo IEC dibujado como en el Manual electrotécnico Telesquemario (marcas de función, mando ⊞, disparadores en cajas, números de bornes girados) y sus datos técnicos.",
    "Equipos genéricos (disyuntor, guardamotor, contactor, relés, operadores, sensores): sin la marca del fabricante, con tu logo ME. en la franja de marca. PLC LOGO! y S7-1200: se conserva la marca porque se trabaja sobre ese modelo.",
    "Formas y bornes tomados de hojas de datos oficiales; las medidas son reales (mm). Las capacidades se dan para el CASO BASE del canal.",
    "Escribe tus correcciones en la línea roja de cada componente y devuélveme el documento: cada corrección se guarda en las reglas del repo.",
  ].map(t => new Paragraph({ numbering: { reference: "vinetas", level: 0 }, spacing: { after: 60 }, children: [T(t, { size: 21 })] })),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "Caso base: trituradora de piedrín", font: "Arial", size: 28, bold: true, color: OSC })] }),
  ...[
    "Motor 10 hp, 230/460 V, 24,3/12,2 A de placa, 1760 rpm, F.S. 1,25, η 91,7 %, f.p. 0,84, 9 puntas (motor de catálogo). Red: 240 V trifásica.",
    "Corriente de tabla NEC 430.250: 28 A → conductor 125 % = 35 A → 10 AWG THHN 75 °C (NEC 430.22).",
    "Protección: guardamotor 22–32 A ajustado a 24,3 A (o breaker 70 A por NEC Tabla 430.52 + relé térmico 23–32 A).",
    "Contactor 32 A AC-3 con bobina 240 VAC. Mando a 240 VAC entre L1-L2 protegido con disyuntor 2P de 6 A, conductor 14 AWG.",
    "Borneras por paquetes: -X0 alimentación · -X1 motores · -X2 puerta/mando · -X3 campo.",
    "Colores de conductores: potencia negro · mando AC rojo · mando DC azul · neutro azul claro · PE verde/amarillo (IEC 60204-1).",
  ].map(t => new Paragraph({ numbering: { reference: "vinetas", level: 0 }, spacing: { after: 60 }, children: [T(t, { size: 21 })] })),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: "Preguntas para ti", font: "Arial", size: 28, bold: true, color: OSC })] }),
  ...[
    "Motor: el de catálogo es NEMA de 9 puntas (T1…T9). ¿Prefieres mostrar uno IEC de 6 bornes (U1 V1 W1 / W2 U2 V2) para que coincida con tu referencia?",
    "Protección del motor: ¿guardamotor + contactor (más común en IEC) o breaker 3P + contactor + relé térmico? Dejé ambos dimensionados.",
    "Flotador: ¿qué marca/modelo usas? Los colores de los 3 hilos cambian entre fabricantes.",
    "Imágenes 28–30 de tu Word (HMI, S7-300, SCALANCE): las dejo para una segunda entrega como 'solo esquema'. ¿Correcto?",
  ].map(t => new Paragraph({ numbering: { reference: "numeros", level: 0 }, spacing: { after: 60 }, children: [T(t, { size: 21 })] })),
  new Paragraph({ children: [new PageBreak()] }),
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { font: "Arial", size: 44, bold: true }, paragraph: { spacing: { before: 0, after: 80 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: "Arial", size: 28, bold: true }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true, outlineLevel: 0 } },
    ],
  },
  numbering: { config: [
    { reference: "vinetas", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
    { reference: "numeros", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 420, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [T("@miguelesquit · Catálogo de componentes · pág. ", { size: 16, color: "667085" }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "667085", font: "Arial" })] })] }) },
    children: [...intro, new Table({ width: { size: W_TABLA, type: WidthType.DXA }, columnWidths: COLS, rows: [filaEncabezado(), ...items.map((it, i) => filaItem(it, i + 1))] })],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(salida, b); console.log("ok", salida); });

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, BorderStyle, LevelFormat, PageBreak, Footer, PageNumber, ExternalHyperlink,
} = require('docx');

const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'datos.json'), 'utf8'));
const DISP = JSON.parse(fs.readFileSync(path.join(__dirname, 'disp.json'), 'utf8'));
const NAV = '0B1F4D';
const CAT = {
  A: ['Mando y señalización', '0057FF'],
  B: ['Maniobra y protección de motores', '22A559'],
  C: ['Relés de control y vigilancia', '7C3AED'],
  D: ['Protección y distribución', 'FF8A00'],
  E: ['Automatización', '0FA3A3'],
  F: ['Sensores', 'E5383B'],
};
const W = 10080; // ancho útil (Letter, márgenes 0,8")
const border = { style: BorderStyle.SINGLE, size: 4, color: 'D0D5DD' };
const borders = { top: border, bottom: border, left: border, right: border };

const P = (text, opt = {}) => new Paragraph({ spacing: { after: 80 }, keepNext: !!opt.kn, ...opt.p, children: [].concat(text).map(t => typeof t === 'string' ? new TextRun({ text: t, ...opt.r }) : t) });
const B = (t) => new TextRun({ text: t, bold: true });

function link(m, fab) {
  let url;
  if (fab === 'Siemens') url = `https://www.automation.siemens.com/bilddb/cax_de.aspx?mlfb=${m}`;
  else if (fab === 'ifm') url = `https://www.ifm.com/us/en/product/${m}`;
  else url = 'https://github.com/FreeCAD/FreeCAD-library/tree/master/Electrical%20Parts/Electrical%20Switches';
  return new ExternalHyperlink({ link: url, children: [new TextRun({ text: url, style: 'Hyperlink', size: 16 })] });
}

function disponible(m, fab) {
  if (fab === 'ifm') return 'Modelo 3D STEP y SAT · dibujo 2D DXF y DWG · dibujo acotado en la ficha · foto oficial 1600 px';
  if (fab.startsWith('FreeCAD')) return 'Modelo 3D STEP y FCStd (CC BY 3.0) · render propio ya hecho (G01) · 2D: se proyecta del STEP';
  const key = m.split(' ')[0];
  const [m3, r, d, f] = DISP[key] || [0, 0, 0, 0];
  const s = [];
  if (m3) s.push('Modelo 3D STEP');
  if (r) s.push('render 3D oficial');
  if (d) s.push('dibujo acotado 2D (DXF/PNG)');
  if (f) s.push('foto de producto');
  return s.join(' · ');
}

function cell(children, w, shade) {
  return new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [].concat(children),
  });
}

function ficha(i, r) {
  const [cat, nombre, modelo, fab, datos, partes, idea] = r;
  const key = modelo.split(' ')[0];
  const th = fab.startsWith('FreeCAD') ? 'LAY37' : key;
  const img = fs.readFileSync(path.join(__dirname, 'th', `${th}.jpg`));
  const col = CAT[cat][1];
  const rows = [
    ['Modelo', `${modelo}  ·  ${fab}`],
    ['Datos', datos],
    ['Disponible', disponible(modelo, fab)],
    ['Partes para señalar', partes],
    ['Idea de imagen', idea],
  ].map(([k, v]) => new TableRow({ cantSplit: true, children: [cell(P(k, { kn: true, r: { bold: true, size: 18, color: NAV } }), 2100, 'F2F6FC'), cell(P(v, { kn: true, r: { size: 18 } }), W - 2100)] }));
  rows.push(new TableRow({ cantSplit: true, children: [cell(P('Descarga', { r: { bold: true, size: 18, color: NAV } }), 2100, 'F2F6FC'), cell(new Paragraph({ children: [link(key, fab)] }), W - 2100)] }));
  return [
    new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, keepLines: true,
      children: [new TextRun({ text: `${i}. `, color: col }), new TextRun({ text: nombre })] }),
    new Paragraph({ keepNext: true, spacing: { after: 60 }, alignment: AlignmentType.CENTER,
      children: [new ImageRun({ type: 'jpg', data: img, transformation: { width: 432, height: 216 },
        altText: { title: nombre, description: `${nombre}: render o foto oficial y dibujo acotado`, name: th } })] }),
    new Paragraph({ keepNext: true, alignment: AlignmentType.CENTER, spacing: { after: 80 },
      children: [new TextRun({ text: fab.startsWith('FreeCAD') ? 'render propio del modelo FreeCAD (G01)' : 'izquierda: render o foto oficial · derecha: dibujo acotado', italics: true, size: 16, color: '667085' })] }),
    new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [2100, W - 2100], rows }),
    new Paragraph({ spacing: { after: 200 }, children: [] }),
  ];
}

// ---------- portada y criterios
const intro = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('50 equipos con modelo 2D y 3D de calidad')] }),
  P('Catálogo verificado para infografías y videos del canal @miguelesquit · 26 de noviembre de 2026', { r: { color: '475467', size: 22 } }),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('Cómo se eligieron')] }),
  P([B('Referencia aprobada: '), 'G01 (paro de emergencia en 3D) y G06 (contactor con render y dibujo acotado del fabricante). ', B('Rechazado: '), 'G05, el sensor inductivo genérico sin detalle.']),
  P([B('Regla: '), 'solo entra un equipo real que tenga modelo 3D oficial (STEP) y dibujo 2D acotado del fabricante. Los 50 se revisaron uno por uno el 26 de noviembre en la base del fabricante; las miniaturas de cada ficha son las imágenes oficiales.']),
  P([B('Fuentes: '), 'Siemens Industry Bilddatenbank (42 equipos), ifm electronic (7 sensores) y FreeCAD Parts Library (1, el LAY37 ya aprobado).']),
  P([B('Uso: '), 'Siemens: descarga gratuita citando “Siemens AG”. ifm: STEP y DXF de descarga libre en la página del producto, citar “ifm electronic”. FreeCAD: CC BY 3.0 citando al autor. En las imágenes no se escribe marca ni código (solo en el pie de fuentes).']),
  P([B('Buscados y descartados: '), 'motor trifásico, variador de frecuencia (V20 y G120C solo tienen dibujo 2D, sin 3D), transformador de mando y los modelos genéricos de FreeCAD (sensor, fuente, breaker de un solo sólido). Para el motor y el variador habría que bajar el STEP de otro portal (SiePortal CAx, WEG o ABB).']),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('Resumen por categoría')] }),
];
const cnt = {};
D.forEach(r => { cnt[r[0]] = (cnt[r[0]] || 0) + 1; });
const resumen = new Table({
  width: { size: W, type: WidthType.DXA }, columnWidths: [6080, 2000, 2000],
  rows: [new TableRow({ children: ['Categoría', 'Equipos', 'Números'].map((t, k) => cell(P(t, { r: { bold: true, color: 'FFFFFF', size: 20 } }), [6080, 2000, 2000][k], NAV)) })]
    .concat(Object.keys(CAT).map(c => {
      const idx = D.map((r, i) => r[0] === c ? i + 1 : 0).filter(Boolean);
      return new TableRow({ children: [cell(P(CAT[c][0], { r: { size: 20, bold: true, color: CAT[c][1] } }), 6080), cell(P(String(cnt[c]), { r: { size: 20 } }), 2000), cell(P(`${idx[0]}–${idx[idx.length - 1]}`, { r: { size: 20 } }), 2000)] });
    })),
});

const body = [...intro, resumen, new Paragraph({ children: [new PageBreak()] })];
let last = '';
D.forEach((r, i) => {
  if (r[0] !== last) {
    if (last) body.push(new Paragraph({ children: [new PageBreak()] }));
    body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: CAT[r[0]][0], color: CAT[r[0]][1] })] }));
    last = r[0];
  }
  body.push(...ficha(i + 1, r));
});

const doc = new Document({
  creator: 'Claude para @miguelesquit',
  title: '50 equipos con modelo 2D y 3D',
  styles: {
    default: { document: { run: { font: 'Arial', size: 21 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { font: 'Arial', size: 44, bold: true, color: NAV }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Arial', size: 32, bold: true, color: NAV }, paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Arial', size: 26, bold: true, color: NAV }, paragraph: { spacing: { before: 160, after: 80 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1152, bottom: 1152, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: '@miguelesquit · 50 equipos 2D/3D · pág. ', size: 16, color: '667085' }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '667085' })] })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(path.join(__dirname, 'Equipos_2D_3D_50.docx'), b); console.log('ok'); });

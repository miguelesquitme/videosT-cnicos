const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  HeadingLevel, AlignmentType, BorderStyle, LevelFormat, PageBreak, Footer, PageNumber, ExternalHyperlink,
} = require('docx');

const D = JSON.parse(fs.readFileSync(path.join(__dirname, 'datos.json'), 'utf8'));
const sizeOf = (b) => ({ w: b.readUInt16BE(b.indexOf(Buffer.from([0xff,0xc0]))+7), h: b.readUInt16BE(b.indexOf(Buffer.from([0xff,0xc0]))+5) });
const NAV = '0B1F4D';
const CAT = {
  A: ['Seguridad de máquina y mando', '0057FF'],
  B: ['Motores, accionamientos y maniobra', '22A559'],
  C: ['Protección, medición y energía', 'FF8A00'],
  D: ['Tablero, clima y bornes', '7C3AED'],
  E: ['Automatización y comunicación', '0FA3A3'],
  F: ['Sensores', 'E5383B'],
};
const W = 10080; // ancho útil (Letter, márgenes 0,8")
const border = { style: BorderStyle.SINGLE, size: 4, color: 'D0D5DD' };
const borders = { top: border, bottom: border, left: border, right: border };

const P = (text, opt = {}) => new Paragraph({ spacing: { after: 80 }, keepNext: !!opt.kn, ...opt.p, children: [].concat(text).map(t => typeof t === 'string' ? new TextRun({ text: t, ...opt.r }) : t) });
const B = (t) => new TextRun({ text: t, bold: true });

const SE_REG = { ATV320U15M2C: 'us/en', NSYS3D4320: 'us/en', ABL6TS10U: 'uk/en', BLRCH104A125B48: 'uk/en', VPL12N: 'us/en', PKF16M434: 'uk/en', BMH0701T06A2A: 'us/en', LV847123: 'us/en' };
function urlDe(m, fab) {
  if (fab === 'Siemens') return `https://www.automation.siemens.com/bilddb/cax_de.aspx?mlfb=${m}`;
  if (fab === 'ifm') return `https://www.ifm.com/us/en/product/${m}`;
  if (fab === 'WEG') return 'https://ecatalog.weg.net/drawings_2d_3d/index.asp?empresa=WMO&language=ING';
  return `https://www.se.com/${SE_REG[m]}/product/${m}/`;
}
function link(m, fab) {
  const url = urlDe(m, fab);
  return new ExternalHyperlink({ link: url, children: [new TextRun({ text: url, style: 'Hyperlink', size: 16 })] });
}
const SIN_PLANO = ['8MR6423-6LV30', '8MR2132-5AB', '8MR2200-0B'];
const SE_PLANO = ['ATV320U15M2C', 'NSYS3D4320'];
function disponible(m, fab) {
  if (fab === 'Siemens') return 'Modelo 3D STEP oficial (descargado, convertido y renderizado en 2 vistas)' + (SIN_PLANO.includes(m) ? ' · foto oficial · la base no trae plano acotado' : ' · plano acotado 2D · render o foto oficial');
  if (fab === 'ifm') return 'Modelo 3D STEP y SAT (descargado y renderizado en 2 vistas) · 2D DXF y DWG · foto oficial' + (m === 'DTI410' ? '' : ' · plano acotado en la ficha');
  if (fab === 'WEG') return 'STEP, IGES, SAT, Parasolid y DXF gratis en la biblioteca CAD de WEG (ruta NEMA / W22_GENERAL_PURPOSE / 11_FRAME_215T) · 3 vistas renderizadas desde el STEP';
  return 'Imágenes oficiales en 1500 px' + (m === 'ATV320U15M2C' ? ' (6 vistas: frente, lados, atrás, arriba y abajo)' : m === 'ABL6TS10U' ? ' (6 vistas)' : m === 'PKF16M434' ? ' + vista explotada' : '') + (SE_PLANO.includes(m) ? ' · plano acotado' : '') + ' · archivos CAD en la página del producto (Documentos → CAD)';
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
  const key = fab === 'WEG' ? 'W22-215T' : modelo.split(' ')[0];
  const ths = key === '5SE2316' ? ['5SE2316', '5SG1301'] : [key];
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
    ...ths.map(th => { const img = fs.readFileSync(path.join(__dirname, 'th', `${th}.jpg`)); const { w, h } = sizeOf(img); let H = 165, Wd = Math.round(w * H / h); if (Wd > 640) { Wd = 640; H = Math.round(h * Wd / w); }
      return new Paragraph({ keepNext: true, spacing: { after: 40 }, alignment: AlignmentType.CENTER,
      children: [new ImageRun({ type: 'jpg', data: img, transformation: { width: Wd, height: H },
        altText: { title: nombre, description: `${nombre}: vistas del modelo 3D, imagen oficial y plano`, name: th } })] }); }),
    new Paragraph({ keepNext: true, alignment: AlignmentType.CENTER, spacing: { after: 80 },
      children: [new TextRun({ text: fab === 'WEG' ? 'Vistas renderizadas desde el STEP oficial de WEG (se pueden girar a cualquier ángulo)' : (fab === 'Siemens' || fab === 'ifm') ? 'Vistas 3D renderizadas desde el STEP oficial del fabricante (se pueden girar a cualquier ángulo); foto y plano oficiales' : 'Imágenes oficiales del fabricante', italics: true, size: 16, color: '667085' })] }),
    new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [2100, W - 2100], rows }),
    new Paragraph({ spacing: { after: 200 }, children: [] }),
  ];
}

// ---------- portada y criterios
const intro = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun('50 equipos más con modelo 2D y 3D · lote 2')] }),
  P('Catálogo verificado para infografías y videos del canal @miguelesquit · 26 de noviembre de 2026 · todos los equipos son de tipo distinto', { r: { color: '475467', size: 22 } }),
  new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun('Cómo se eligieron')] }),
  P([B('Qué cambió respecto al primer lote: '), 'los 50 son de tipo distinto entre sí y ninguno repite un tipo del primer Word (no hay otro contactor, temporizador, relé de vigilancia, breaker, PLC ni sensor inductivo/capacitivo/fotoeléctrico difuso). Entran motor, variador, servomotor, transformador de mando, capacitores, ACB, gabinete y clima del tablero, que en el lote 1 faltaban.']),
  P([B('Calidad: '), 'para 42 equipos bajé el modelo 3D STEP oficial (Siemens, ifm y WEG), lo convertí y lo rendericé yo desde dos ángulos para comprobar que el modelo está completo y se ve bien. Como es un modelo 3D real, se puede girar a cualquier vista, cortar, explotar o animar. Los 8 de Schneider Electric traen vistas oficiales en 1500 px (el variador y el transformador, 6 vistas cada uno) y su CAD está en la página del producto.']),
  P([B('Verificación: '), 'cada descripción técnica se tomó el 26 de noviembre de la página oficial del producto (SiePortal de Siemens, ficha técnica de ifm, página de Schneider Electric y biblioteca CAD de WEG). Al revisar se corrigieron dos códigos: 5ST3010 resultó ser un contacto auxiliar (se cambió por la barra de pines 5ST3610) y 3RF2320 está descontinuado (se usa su sucesor 3RF3320).']),
  P([B('Uso de las imágenes: '), 'Siemens permite el uso citando “Siemens AG”. Para ifm, Schneider Electric y WEG los archivos son de descarga pública, pero no revisé sus condiciones de uso: hay que leerlas antes de publicar. En las publicaciones no se escribe marca ni código (solo en el pie de fuentes).']),
  P([B('Buscados y descartados: '), 'cortina de luz de seguridad (no encontré una con 3D descargable en las fuentes revisadas), el interruptor horario crepuscular y la transferencia automática de Siemens (sin resultados con ese código en la base) y el variador de WEG (su archivo 3D pesa 32 MB; se prefirió el de Schneider, que trae 6 vistas oficiales).']),
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
  title: '50 equipos más con modelo 2D y 3D (lote 2)',
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
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: '@miguelesquit · 50 equipos 2D/3D, lote 2 · pág. ', size: 16, color: '667085' }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '667085' })] })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(path.join(__dirname, 'Equipos_2D_3D_lote2.docx'), b); console.log('ok'); });

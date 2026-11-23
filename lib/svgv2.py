"""Base común de las piezas de los reels v2 (dibujo real pieza por pieza, medidas en mm).
Cada módulo svgvXX.py dibuja en píxeles con una escala s (mm/px) y llama a `pieza()`, que devuelve
(svg, puntos_mm, (W, H)) como svgref. `lote(catalogo, carpeta, grupos)` renderiza a PNG + JSON."""
from svgref import svg_mm, T, R, logo  # noqa: F401
from svgfoto import DEFS_F

DEFS_2 = """<defs>
 <linearGradient id="gAcero" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6E757D"/><stop offset="0.3" stop-color="#D9DEE3"/><stop offset="0.6" stop-color="#AEB5BC"/><stop offset="1" stop-color="#5E646B"/></linearGradient>
 <linearGradient id="gAceroV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9DEE3"/><stop offset="0.5" stop-color="#AEB5BC"/><stop offset="1" stop-color="#6E757D"/></linearGradient>
 <linearGradient id="gEsmalte" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#EEF1F4"/><stop offset="1" stop-color="#D3D8DE"/></linearGradient>
 <linearGradient id="gNegro" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A3D42"/><stop offset="1" stop-color="#121315"/></linearGradient>
 <linearGradient id="gBlancoP" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FBFBF8"/><stop offset="1" stop-color="#DCDDD6"/></linearGradient>
 <linearGradient id="gLaton" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A6A1E"/><stop offset="0.3" stop-color="#F1D27A"/><stop offset="0.55" stop-color="#D2A944"/><stop offset="1" stop-color="#7C5C16"/></linearGradient>
 <linearGradient id="gLatonV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F1D27A"/><stop offset="0.6" stop-color="#C99B36"/><stop offset="1" stop-color="#7C5C16"/></linearGradient>
 <linearGradient id="gCobre" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3B183"/><stop offset="0.5" stop-color="#C8743E"/><stop offset="1" stop-color="#8C4A1E"/></linearGradient>
 <linearGradient id="gCobreH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8C4A1E"/><stop offset="0.4" stop-color="#F3B183"/><stop offset="1" stop-color="#8C4A1E"/></linearGradient>
 <linearGradient id="gAlu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F4F6"/><stop offset="0.5" stop-color="#C3C9CF"/><stop offset="1" stop-color="#8D949B"/></linearGradient>
 <radialGradient id="gAluR" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#F4F6F8"/><stop offset="0.7" stop-color="#B4BBC2"/><stop offset="1" stop-color="#7F868D"/></radialGradient>
 <radialGradient id="gAceroR" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#CBD1D7"/><stop offset="0.7" stop-color="#7D848B"/><stop offset="1" stop-color="#4E545B"/></radialGradient>
 <linearGradient id="gPiel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9B48F"/><stop offset="0.55" stop-color="#D49A72"/><stop offset="1" stop-color="#B57B55"/></linearGradient>
 <linearGradient id="gCeram" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#EDEAE2"/><stop offset="1" stop-color="#C9C4B8"/></linearGradient>
 <linearGradient id="gVidrio" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9FC3DA" stop-opacity="0.55"/><stop offset="1" stop-color="#3E6A88" stop-opacity="0.75"/></linearGradient>
 <linearGradient id="gGalv" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#80878E"/><stop offset="0.35" stop-color="#C9CFD5"/><stop offset="0.6" stop-color="#9DA4AB"/><stop offset="1" stop-color="#6A7077"/></linearGradient>
 <linearGradient id="gGris" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9AA1A8"/><stop offset="1" stop-color="#5D636A"/></linearGradient>
 <linearGradient id="gAzulM" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1E3F7A"/><stop offset="0.4" stop-color="#3D6BB3"/><stop offset="1" stop-color="#173264"/></linearGradient>
 <pattern id="pArena" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#E8DFC8"/>
  <circle cx="3" cy="4" r="1.8" fill="#C9BC9A"/><circle cx="10" cy="9" r="1.6" fill="#D6CBAE"/><circle cx="7" cy="12" r="1.2" fill="#BFB18C"/><circle cx="12" cy="2" r="1.1" fill="#CFC3A2"/></pattern>
 <pattern id="pLam" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#7D848B"/><rect width="12" height="2" fill="#5B6168"/></pattern>
</defs>"""


def sombra(cont, f="sDura"):
    return f'<g filter="url(#{f})">{cont}</g>'


def pieza(Wp, Hp, s, cuerpo, puntos=None, margen=4):
    svg, WH = svg_mm(Wp, Hp, s, DEFS_F + DEFS_2 + cuerpo, margen=margen)
    return svg, {k: (x * s, y * s) for k, (x, y) in (puntos or {}).items()}, WH


def tornillo(x, y, r, ranura="cruz", rot=20):
    """Tornillo de cabeza redonda: acero con relieve y ranura."""
    g = f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#gAceroR)"/>'
    if ranura == "cruz":
        g += (f'<g transform="rotate({rot} {x} {y})"><rect x="{x - r * 0.7}" y="{y - r * 0.12}" width="{r * 1.4}" height="{r * 0.24}" fill="#3A3F45"/>'
              f'<rect x="{x - r * 0.12}" y="{y - r * 0.7}" width="{r * 0.24}" height="{r * 1.4}" fill="#3A3F45"/></g>')
    else:
        g += f'<g transform="rotate({rot} {x} {y})"><rect x="{x - r * 0.75}" y="{y - r * 0.13}" width="{r * 1.5}" height="{r * 0.26}" fill="#3A3F45"/></g>'
    return sombra(g, "sTorn")


def lote(catalogo, carpeta, grupos):
    """grupos = {px_mm: [nombres]}"""
    from render_svg import render_lote, margen_de
    for px, ns in grupos.items():
        render_lote([(n, catalogo[n](), margen_de(catalogo[n]()[0])) for n in ns], carpeta, px_mm=px)


def hoja(carpeta, salida, alto=420):
    """Hoja de piezas para revisar en imagen fija."""
    import glob
    from PIL import Image
    fs = sorted(glob.glob(f"{carpeta}/*.png"))
    ims = []
    for f in fs:
        im = Image.open(f).convert("RGBA")
        ims.append(im.resize((max(1, int(im.width * alto / im.height)), alto)))
    filas, fila, w = [], [], 0
    for im in ims:
        if w + im.width > 2400 and fila:
            filas.append(fila); fila, w = [], 0
        fila.append(im); w += im.width + 10
    if fila:
        filas.append(fila)
    W = max(sum(i.width + 10 for i in f) for f in filas) + 10
    out = Image.new("RGB", (W, len(filas) * (alto + 10) + 10), "#2A2D33")
    for r, f in enumerate(filas):
        x = 10
        for im in f:
            out.paste(im, (x, 10 + r * (alto + 10)), im); x += im.width + 10
    out.save(salida)
    return [f.split("/")[-1] for f in fs]

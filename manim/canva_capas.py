"""Arma las CAPAS del cuadro para reconstruirlo en Canva elemento por elemento (sin IA de Canva):
fondo (cuadrícula + puerta + título) · cada equipo como PNG suelto · cables en 2 capas PNG transparentes ·
diagrama de potencia como FORMAS vectoriales de Canva (una por símbolo/polo/tramo) · marcas naranjas como formas ·
textos del diagrama como texto de Canva. Escribe canva/capas/*.png y canva/capas/ops.json (operaciones de edit-design).

Uso: python3 canva_capas.py canva/h01_c8_v2.svg canva/capas
"""
import base64
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import canva_diag as CD  # noqa: E402

EQUIPOS = ["F2", "F1", "X0", "X1", "S0", "S0b", "S1", "S1b", "H1", "H1b", "H2", "H2b", "KM1", "F3"]
CABLES_A = ["cables_mando"] + [f"Group_0{n}" for n in (23, 24, 25, 30, 31, 32, 42, 43, 44, 47)]
CABLES_B = [f"VGroup_0{n}" for n in range(51, 61)]
MARCAS = [f"VMobject_0{n}" for n in (20, 21, 22, 27, 28, 29, 34, 35, 36, 39, 40, 41, 46)]
QUITAR_FONDO = EQUIPOS + CABLES_A + CABLES_B + MARCAS + ["diagrama_potencia", "diagrama_potencia_textos"]
JS = "/tmp/claude-0/svg2.js"

K, OX, OY = 1.25, 44.75, 95.75          # original → página


def grupos(svg):
    """{id: (inicio, fin)} de los <g id=…> de nivel superior."""
    out, i = {}, 0
    for m in re.finditer(r'<g id="([^"]+)"', svg):
        out.setdefault(m.group(1), m.start())
    return out


def bloque(svg, gid):
    i = svg.index(f'<g id="{gid}"')
    prof, j = 0, i
    for m in re.finditer(r"<g[ >]|</g>", svg[i:]):
        prof += 1 if m.group(0) != "</g>" else -1
        if prof == 0:
            j = i + m.end()
            break
    return i, j


def sin(svg, ids):
    for g in ids:
        if f'<g id="{g}"' in svg:
            a, b = bloque(svg, g)
            svg = svg[:a] + svg[b:]
    return svg


def solo(svg, ids):
    cab = svg[:svg.index(">", svg.index("<svg")) + 1]
    partes = [svg[slice(*bloque(svg, g))] for g in ids if f'<g id="{g}"' in svg]
    return cab + "".join(partes) + "</svg>"


def render(svg_txt, png, transparente=False):
    tmp = png.replace(".png", ".svg")
    open(tmp, "w").write(svg_txt)
    subprocess.run(["node", JS, os.path.abspath(tmp), os.path.abspath(png)], check=True)
    if transparente:   # Chromium pinta blanco detrás: se rasteriza con fondo transparente vía omitBackground
        subprocess.run(["node", "-e", f"""
const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1920,height:1080}}}});
await p.goto('file://{os.path.abspath(tmp)}');
await p.waitForTimeout(500);await p.screenshot({{path:'{os.path.abspath(png)}',omitBackground:true}});await b.close();}})();"""], check=True)
    os.remove(tmp)


# ---------------------------------------------------------------- formas del diagrama (coords de página)
def P(x, y):
    return (K * x + OX, K * y + OY)


def linea_pts(*pts):
    return [P(x, y) for x, y in pts]


def guiones(p0, p1, on=3.75, off=3.75):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    segs, t = [], 0.0
    while t < L:
        e = min(t + on, L)
        segs.append([(x0 + ux * t, y0 + uy * t), (x0 + ux * e, y0 + uy * e)])
        t += on + off
    return segs


def forma(nombre, subpaths, sw=1.9, relleno=None, color="#000000", opac=None, arcos=None):
    """subpaths: listas de puntos (página). arcos: lista de (cx, cy, r) círculos."""
    xs, ys = [], []
    for sp in subpaths:
        for x, y in sp:
            xs.append(x), ys.append(y)
    for cx, cy, r in arcos or []:
        xs += [cx - r, cx + r]
        ys += [cy - r, cy + r]
    m = sw / 2 + 1
    x0, y0, x1, y1 = min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m
    w, h = max(x1 - x0, 2), max(y1 - y0, 2)
    d = []
    for sp in subpaths:
        d.append("M" + " L".join(f"{x - x0:.2f},{y - y0:.2f}" for x, y in sp) + (" Z" if relleno and len(sp) > 2 else ""))
    for cx, cy, r in arcos or []:
        a, b = cx - x0, cy - y0
        d.append(f"M{a - r:.2f},{b:.2f} A{r:.2f},{r:.2f} 0 1,0 {a + r:.2f},{b:.2f} A{r:.2f},{r:.2f} 0 1,0 {a - r:.2f},{b:.2f} Z")
    op = {"type": "insert_shape", "page_id": "PAGE", "top": round(y0, 2), "left": round(x0, 2), "width": round(w, 2),
          "height": round(h, 2), "path": " ".join(d), "view_box_width": round(w, 2), "view_box_height": round(h, 2)}
    if relleno:
        op["color"] = relleno
    else:
        op["stroke_color"], op["stroke_weight"] = color, sw
    if opac is not None:
        op["opacity"] = opac
    op["_nombre"] = nombre
    return op


def formas_diagrama():
    F = []
    FA = CD.FASES
    # -X0 barras
    for nom, y in (("PE", 21), ("N", 51), ("L3", 81), ("L2", 111), ("L1", 141)):
        F.append(forma(f"X0_{nom}_bornes", [], arcos=[(*P(35, y), 4 * K), (*P(95, y), 4 * K)]))
        if nom == "PE":
            segs = [linea_pts((39, y), (52, y)), linea_pts((56, y), (91, y))] + guiones(P(99, y), P(514, y))
        else:
            segs = [linea_pts((39, y), (91, y)), linea_pts((99, y), (514, y))]
        F.append(forma(f"barra_{nom}", segs))
    # derivaciones
    for nom, x, y in (("L3", 245, 81), ("L2", 275, 111), ("L1", 305, 141)):
        F.append(forma(f"cond_{nom}_X0-F2", [linea_pts((x, y), (x, 246))]))
        F.append(forma(f"punto_{nom}", [], relleno="#000000", arcos=[(*P(x, y), 2.6 * K)]))
    # -F2
    for k, x in enumerate(FA):
        dx = x - 245
        t = ((237, 247), (258, 272), (287, 297))[k]
        F.append(forma(f"F2_polo{k + 1}", [linea_pts((230 + dx, 246), (245 + dx, 275)), linea_pts((t[0], 261), (t[1], 261))]))
        cx, cy, a = 231.5 + dx, 258, math.radians(-25)
        cuad = [(-4.5, -4.5), (4.5, -4.5), (4.5, 4.5), (-4.5, 4.5)]
        F.append(forma(f"F2_polo{k + 1}_disparo", [[P(cx + u * math.cos(a) - v * math.sin(a), cy + u * math.sin(a) + v * math.cos(a)) for u, v in cuad]],
                       relleno="#000000"))
    F.append(forma("cond_F2-KM1", [linea_pts((x, 275), (x, 366)) for x in FA]))
    # -KM1
    for k, x in enumerate(FA):
        dx = x - 245
        t = ((237, 247), (263, 272), (287, 297))[k]
        F.append(forma(f"KM1_polo{k + 1}", [linea_pts((230 + dx, 366), (245 + dx, 395)), linea_pts((t[0], 381), (t[1], 381))]))
    F.append(forma("cond_KM1-F3", [linea_pts((x, 395), (x, 471.5)) for x in FA]))
    # -F3
    F.append(forma("F3_caja", [linea_pts((238, 471.5), (327, 471.5), (327, 501.5), (238, 501.5), (238, 471.5))]))
    for k, x in enumerate(FA):
        F.append(forma(f"F3_polo{k + 1}", [linea_pts((x, 471.5), (x, 478.5), (x + 15, 478.5), (x + 15, 494.5), (x, 494.5), (x, 501.5))]))
    F.append(forma("cond_F3-X1", [linea_pts((x, 501.5), (x, 557)) for x in FA]))
    # -X1
    F.append(forma("X1_bornes", [], arcos=[(*P(x, 561), 4 * K) for x in FA + (335,)]))
    # -M1
    F.append(forma("cond_X1-M1", [linea_pts((245, 565), (245, 632)), linea_pts((275, 565), (275, 621.5)), linea_pts((305, 565), (305, 633))]))
    F.append(forma("M1_motor", [], arcos=[(*P(275, 666), 44.5 * K)]))
    til = [P(291 + 18 * i / 24, 673 - 3.5 * math.sin(2 * math.pi * i / 24)) for i in range(25)]
    F.append(forma("M1_tilde", [til]))
    F.append(forma("M1_masa", [linea_pts((323.5, 657.5), (323.5, 675)), linea_pts((326.5, 657.5), (326.5, 675))]))
    # PE y tierras
    pe = guiones(P(335, 21), P(335, 557)) + guiones(P(335, 565), P(335, 606)) + guiones(P(335, 576), P(395, 576)) + \
        guiones(P(395, 576), P(395, 588)) + guiones(P(440, 21), P(440, 183))
    F.append(forma("cond_PE_punteado", pe))
    F.append(forma("cond_PE_solido", [linea_pts((335, 606), (335, 666), (327, 666)), linea_pts((395, 588), (395, 606)), linea_pts((440, 183), (440, 201))]))
    F.append(forma("puntos_PE", [], relleno="#000000", arcos=[(*P(335, 21), 2.6 * K), (*P(440, 21), 2.6 * K), (*P(335, 576), 2.6 * K)]))
    for n, (x, y) in (("tierra_1", (440, 201)), ("tierra_2", (395, 606))):
        F.append(forma(n, [linea_pts((x - 14.5, y), (x + 14.5, y)), linea_pts((x - 9.5, y + 7), (x + 9.5, y + 7)), linea_pts((x - 4.5, y + 14), (x + 4.5, y + 14))]))
    return F


def bezier_pts(d):
    """Puntos de un path 'M… C…' (muestrea cada cúbica)."""
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
    pts = [(nums[0], nums[1])]
    i = 2
    while i + 5 < len(nums):
        p0 = pts[-1]
        c1, c2, p3 = (nums[i], nums[i + 1]), (nums[i + 2], nums[i + 3]), (nums[i + 4], nums[i + 5])
        for t in (0.5, 1.0):
            u = 1 - t
            pts.append((u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p3[0],
                        u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p3[1]))
        i += 6
    # quita puntos repetidos / colineales seguidos
    lim = [pts[0]]
    for p in pts[1:]:
        if math.hypot(p[0] - lim[-1][0], p[1] - lim[-1][1]) > 0.5:
            lim.append(p)
    return lim


def formas_marcas(svg):
    F = []
    for g in MARCAS:
        a, b = bloque(svg, g)
        m = re.search(r' d="([^"]+)"[^>]*stroke="(#[0-9A-Fa-f]{6})" stroke-opacity="([\d.]+)" stroke-width="([\d.]+)"', svg[a:b])
        F.append(forma(f"marca_{g}", [bezier_pts(m.group(1))], sw=float(m.group(4)), color=m.group(2), opac=float(m.group(3))))
    return F


def textos_diagrama(svg):
    a, b = bloque(svg, "diagrama_potencia_textos")
    T = []
    for m in re.finditer(r"<text ([^>]*)>([^<]*)</text>", svg[a:b]):
        at, txt = m.group(1), m.group(2)
        fs = float(re.search(r'font-size="([\d.]+)"', at).group(1))
        tl = float(re.search(r'textLength="([\d.]+)"', at).group(1))
        tr = re.search(r"translate\(([\d.]+),([\d.]+)\) rotate\(-90\)", at)
        if tr:   # girado: x base, y abajo; ancho del texto = tl en vertical
            xb, yb = float(tr.group(1)), float(tr.group(2))
            cx, cy = xb - 0.36 * fs, yb - tl / 2
            T.append({"texto": txt, "fs": fs, "cx": cx, "cy": cy, "rot": -90, "w": tl})
        else:
            x, y = float(re.search(r' x="([\d.]+)"', at).group(1)), float(re.search(r' y="([\d.]+)"', at).group(1))
            T.append({"texto": txt, "fs": fs, "cx": x + tl / 2, "cy": y - 0.36 * fs, "rot": 0, "w": tl})
    return T


def main(entrada, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    svg = open(entrada).read()
    render(sin(svg, QUITAR_FONDO), f"{carpeta}/fondo.png")
    render(solo(svg, CABLES_A), f"{carpeta}/cables_mando.png", True)
    render(solo(svg, CABLES_B), f"{carpeta}/cables_potencia.png", True)
    eq = {}
    for g in EQUIPOS:
        a, b = bloque(svg, g)
        m = re.search(r'x="([\d.\-]+)" y="([\d.\-]+)" width="([\d.]+)" height="([\d.]+)"[^>]*href="data:image/png;base64,([^"]+)"', svg[a:b])
        open(f"{carpeta}/eq_{g}.png", "wb").write(base64.b64decode(m.group(5)))
        eq[g] = [float(m.group(i)) for i in range(1, 5)]
    ops = {"equipos": eq, "formas": formas_diagrama() + formas_marcas(svg), "textos": textos_diagrama(svg)}
    json.dump(ops, open(f"{carpeta}/ops.json", "w"), ensure_ascii=False, indent=0)
    print(len(ops["formas"]), "formas,", len(ops["textos"]), "textos,", len(eq), "equipos")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Base de estilos del lote H (v2: recuadros sin borde). Lote H (25-nov): 5 dispositivos × 6 infografías con fotos reales de larssystemgt.com (a pedido del autor).
Estilo nuevo: título de G07 (cinta inclinada, SIN la palabra "real"); rótulos con LÍNEA CONTINUA y RECUADRO de color
semitransparente sobre la pieza. Estructura por equipo: 1 partes · 2 funcionamiento · 3 criterios · 4 aplicación · 5 versus · 6 símbolo.
Fuentes en referencias/loteH_fuentes.md."""
import importlib.util
import math
import subprocess
import sys
from pathlib import Path
from PIL import Image

AQ = Path(__file__).parent
sys.path.insert(0, str(AQ.parent.parent / "lib"))
import simsvg as S  # noqa: E402


def _load(n, p):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


g12 = _load("g12", AQ.parent / "posts12" / "gen.py")
g = g12.g
page, kick, T, svg, tabla = g.page, g.kick, g.T, g.svg, g.tabla
DID = g.DID + """
.lb{position:absolute;display:flex;gap:10px;align-items:center;background:#fff;border-radius:14px;padding:5px 10px 5px 6px;
 box-shadow:0 6px 16px rgba(11,31,77,.16)}
.lb .n{flex:none;width:40px;height:40px;border-radius:50%;color:#fff;font:800 20px Montserrat;display:flex;align-items:center;justify-content:center}
.lb b{display:block;font:800 19px/1.1 Montserrat;color:#0B1F4D}.lb span{display:block;font:500 15px/1.2 Montserrat;color:#475467;margin-top:2px}
.ph{position:absolute;background:#fff;border-radius:22px;box-shadow:0 10px 30px rgba(11,31,77,.12)}
.cap{position:absolute;font:700 15px Montserrat;color:#667085;text-align:center}
.crit{position:absolute;left:40px;right:40px;display:flex;gap:16px;align-items:stretch;background:#F6FAFF;border-radius:16px;overflow:hidden}
.crit .k{flex:none;width:64px;display:flex;align-items:center;justify-content:center;color:#fff;font:900 40px 'Barlow C'}
.crit .c{flex:1;padding:9px 14px 10px 4px;font:500 17px/1.3 Montserrat;color:#1d2939}.crit .c b{display:block;font:800 21px/1.15 Montserrat;color:#0B1F4D;margin-bottom:2px}
.crit .v{flex:none;padding:5px 12px;border-radius:9px;color:#fff;font:900 24px/1 'Barlow C';white-space:nowrap}
.vs{position:absolute;left:40px;right:40px;border-radius:18px;overflow:hidden;box-shadow:0 8px 22px rgba(11,31,77,.12);font:600 19px Montserrat;background:#fff}
.vs div{display:grid;grid-template-columns:1.05fr 1fr 1fr;align-items:center;border-top:2px solid #E4E7EC}.vs div:first-child{border-top:0}
.vs span{padding:8px 14px}.vs span+span{text-align:center;font:800 24px 'Barlow C';color:#0B1F4D;border-left:2px solid #E4E7EC}
.vs div.h span{background:#0B1F4D;color:#fff;font:800 18px Montserrat}.vs div.d{background:#FFF4E5}
.blk{position:absolute;border-radius:16px;padding:10px 14px;font:500 16px/1.28 Montserrat;color:#1d2939;background:#F6FAFF;text-align:center;box-shadow:0 6px 16px rgba(11,31,77,.10)}
.blk b{display:block;font:900 26px/1.05 'Barlow C';color:#0B1F4D;margin-bottom:3px}
.leg{position:absolute;left:40px;right:40px;display:grid;gap:10px}
.leg div{display:flex;gap:10px;align-items:center;background:#F6FAFF;border-radius:12px;padding:6px 10px;font:500 15px/1.25 Montserrat;color:#1d2939}
.leg i{flex:none;font-style:normal;width:36px;height:36px;border-radius:9px;color:#fff;font:900 24px 'Barlow C';display:flex;align-items:center;justify-content:center}
.leg b{font-weight:800;color:#0B1F4D}"""
NAV, AZ, TEAL, NAR, RJ, VER = g.NAV, g.AZ, g.TEAL, g.NAR, g.RJ, g.VER
MOR = "#7C3AED"
CL = ["#0057FF", "#E5383B", "#FF8A00", "#22A559", "#7C3AED", "#0FA3A3", "#D6336C", "#B45309"]
chips, nota = g12.chips, g12.nota


def hexa(c, a):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return f"rgba({int(c[0:2], 16)},{int(c[2:4], 16)},{int(c[4:6], 16)},{a})"


class Img:
    def __init__(self, src, x, y, w=None, h=None):
        W, H = Image.open(AQ / "img" / f"{src}.png").size
        if w and not h:
            h = w * H / W
        if h and not w:
            w = h * W / H
        self.src = f"../img/{src}.png"
        self.x, self.y, self.w, self.h = x, y, w, h

    def p(self, fx, fy):
        return self.x + fx * self.w, self.y + fy * self.h

    def r(self, b):
        x0, y0 = self.p(b[0], b[1])
        x1, y1 = self.p(b[2], b[3])
        return x0, y0, x1, y1

    def html(self, sombra=True):
        sh = "filter:drop-shadow(0 12px 20px rgba(11,31,77,.20));" if sombra else ""
        return (f"<img src='{self.src}' style='position:absolute;left:{self.x:.0f}px;top:{self.y:.0f}px;"
                f"width:{self.w:.0f}px;height:{self.h:.0f}px;{sh}'>")


def rect(x0, y0, x1, y1, c, a=.22):
    """Recuadro de color SIN borde, semitransparente (no tapa la pieza)."""
    return f"<rect x='{x0:.0f}' y='{y0:.0f}' width='{x1 - x0:.0f}' height='{y1 - y0:.0f}' rx='8' fill='{hexa(c, a)}'/>"


def cajas(f, items, wl=290):
    """items: (n, (fx0,fy0,fx1,fy1), título, sub, lx, ly[, color]). Recuadro semitransparente + línea CONTINUA al rótulo."""
    sv, out = [], []
    for it in items:
        n, b, t, sub, lx, ly = it[:6]
        c = it[6] if len(it) > 6 else CL[(n - 1) % len(CL)]
        x0, y0, x1, y1 = f.r(b)
        cx = (x0 + x1) / 2
        if cx > lx + wl:
            ax, ay = lx + wl, ly
        elif cx < lx:
            ax, ay = lx, ly
        else:
            ax, ay = cx, (ly + 30 if (y0 + y1) / 2 > ly else ly - 30)
        tx, ty = min(max(ax, x0), x1), min(max(ay, y0), y1)
        sv.append(rect(x0, y0, x1, y1, c))
        sv.append(f"<line x1='{ax:.0f}' y1='{ay:.0f}' x2='{tx:.0f}' y2='{ty:.0f}' stroke='#fff' stroke-width='8' stroke-linecap='round'/>"
                  f"<line x1='{ax:.0f}' y1='{ay:.0f}' x2='{tx:.0f}' y2='{ty:.0f}' stroke='{c}' stroke-width='3.5' stroke-linecap='round'/>"
                  f"<circle cx='{tx:.0f}' cy='{ty:.0f}' r='6' fill='{c}' stroke='#fff' stroke-width='2.5'/>")
        out.append(f"<div class='lb' style='left:{lx}px;top:{ly - 30}px;width:{wl}px;box-sizing:border-box'>"
                   f"<div class='n' style='background:{c}'>{n}</div><div><b>{t}</b><span>{sub}</span></div></div>")
    return svg(0, 0, 1080, 1350, "".join(sv)) + "".join(out)


def marcas(f, items):
    """Solo recuadros con su número (sin línea): items (n, caja, …)."""
    sv, out = [], []
    for it in items:
        n, b = it[0], it[1]
        c = CL[(n - 1) % len(CL)]
        x0, y0, x1, y1 = f.r(b)
        sv.append(rect(x0, y0, x1, y1, c))
        out.append(f"<div style='position:absolute;left:{x0 - 14:.0f}px;top:{y0 - 16:.0f}px;width:32px;height:32px;border-radius:50%;background:{c};"
                   f"color:#fff;font:800 17px/32px Montserrat;text-align:center;border:2px solid #fff;box-shadow:0 3px 8px rgba(0,0,0,.3)'>{n}</div>")
    return svg(0, 0, 1080, 1350, "".join(sv)) + "".join(out)


def letras(f, items):
    """items: (letra, (fx0,fy0,fx1,fy1), color[, 'tl'|'tr'|'bl'|'br'])  · recuadro + chip con la letra."""
    sv, out = [], []
    for it in items:
        L, b, c = it[:3]
        pos = it[3] if len(it) > 3 else "tl"
        x0, y0, x1, y1 = f.r(b)
        sv.append(rect(x0, y0, x1, y1, c, .22))
        cx = x0 - 16 if pos[1] == "l" else x1 - 18
        cy = y0 - 18 if pos[0] == "t" else y1 - 16
        out.append(f"<div style='position:absolute;left:{cx:.0f}px;top:{cy:.0f}px;width:34px;height:34px;border-radius:9px;background:{c};"
                   f"color:#fff;font:900 24px \"Barlow C\";display:flex;align-items:center;justify-content:center;border:2px solid #fff;"
                   f"box-shadow:0 3px 8px rgba(0,0,0,.3)'>{L}</div>")
    return svg(0, 0, 1080, 1350, "".join(sv)) + "".join(out)


def ph(x, y, w, h):
    return f"<div class='ph' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px'></div>"


def cap(x, y, w, t):
    return f"<div class='cap' style='left:{x}px;top:{y}px;width:{w}px'>{t}</div>"


def crit(top, items, x=40, w=1000, gap=10):
    """items: (título, texto, valor, color) · altura automática."""
    out = [f"<div style='position:absolute;left:{x}px;width:{w}px;top:{top}px;display:grid;gap:{gap}px'>"]
    for i, (t, d, v, c) in enumerate(items):
        out.append(f"<div class='crit' style='position:relative;left:0;right:0'><div class='k' style='background:{c}'>{i + 1}</div>"
                   f"<div class='c'><div style='display:flex;justify-content:space-between;align-items:center;gap:8px'><b>{t}</b>"
                   f"<span class='v' style='background:{c};margin:0'>{v}</span></div>{d}</div></div>")
    return "".join(out) + "</div>"


def versus(top, a, b, filas, dif=()):
    h = f"<div class='h'><span>Dato</span><span>{a}</span><span>{b}</span></div>"
    return (f"<div class='vs' style='top:{top}px'>{h}"
            + "".join(f"<div class='{'d' if i in dif else ''}'><span>{t}</span><span>{x}</span><span>{y}</span></div>" for i, (t, x, y) in enumerate(filas))
            + "</div>")


def rival(x, y, w, h, marca, linea, modelo, datos, col=NAV):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:22px;background:{col};color:#fff;"
            f"display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0 10px 26px rgba(11,31,77,.25)'>"
            f"<div style='font:800 20px Montserrat;letter-spacing:3px;color:#AFC3E8'>{marca}</div>"
            f"<div style='font:600 22px Montserrat;margin-top:6px'>{linea}</div>"
            f"<div style='font:900 64px/1 \"Barlow C\";margin:14px 0;color:#FFD400'>{modelo}</div>"
            f"<div style='font:500 18px/1.35 Montserrat;color:#DCE6F5;padding:0 24px'>{datos}</div></div>")


def vsbadge(cx, cy):
    return (f"<div style='position:absolute;left:{cx - 46}px;top:{cy - 46}px;width:92px;height:92px;border-radius:50%;background:#FF6A00;"
            f"border:6px solid #fff;box-shadow:0 8px 20px rgba(0,0,0,.3);color:#fff;font:900 44px/80px \"Barlow C\";text-align:center;font-style:italic'>VS</div>")


def leyenda(top, items, cols=2, x=40, w=1000):
    return (f"<div class='leg' style='top:{top}px;left:{x}px;right:auto;width:{w}px;grid-template-columns:repeat({cols},1fr)'>"
            + "".join(f"<div><i style='background:{c}'>{L}</i><span><b>{t}</b> {d}</span></div>" for L, t, d, c in items) + "</div>")


def blk(x, y, w, t, d, c=NAV, h=None, bg="#fff"):
    hh = f"height:{h}px;box-sizing:border-box;" if h else ""
    return (f"<div class='blk' style='left:{x}px;top:{y}px;width:{w}px;{hh}background:{hexa(c, .10) if bg == '#fff' else bg}'>"
            f"<b style='color:{c}'>{t}</b>{d}</div>")


def flecha(x1, y1, x2, y2, c=NAV, w=5, t=""):
    ang = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = ang + 2.6, ang - 2.6
    p = f"{x2},{y2} {x2 + 16 * math.cos(a1):.0f},{y2 + 16 * math.sin(a1):.0f} {x2 + 16 * math.cos(a2):.0f},{y2 + 16 * math.sin(a2):.0f}"
    s = f"<line x1='{x1}' y1='{y1}' x2='{x2 - 10 * math.cos(ang):.0f}' y2='{y2 - 10 * math.sin(ang):.0f}' stroke='{c}' stroke-width='{w}'/><polygon points='{p}' fill='{c}'/>"
    if t:
        s += (f"<text x='{(x1 + x2) / 2 + 10}' y='{(y1 + y2) / 2}' font-family='Montserrat' font-size='16' font-weight='700' fill='{c}' "
              f"dominant-baseline='central'>{t}</text>")
    return s


def tx(x, y, s, size=16, w=700, c=NAV, a="middle"):
    return (f"<text x='{x:.0f}' y='{y:.0f}' font-family='Montserrat' font-size='{size}' font-weight='{w}' fill='{c}' "
            f"text-anchor='{a}' dominant-baseline='central'>{s}</text>")


# ------------------------------------------------------------------ gráfica tiempo-corriente log-log
def curva(x, y, w, h, xr, yr, cuerpo_fn, xt, yt, xlab, ylab="tiempo"):
    lx0, lx1 = math.log10(xr[0]), math.log10(xr[1])
    ly0, ly1 = math.log10(yr[0]), math.log10(yr[1])

    def P(a, b):
        return x + (math.log10(a) - lx0) / (lx1 - lx0) * w, y + h - (math.log10(b) - ly0) / (ly1 - ly0) * h
    s = [f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='#F6FAFF' stroke='#CFE0F5' stroke-width='2' rx='6'/>"]
    for v, lab in xt:
        px, _ = P(v, yr[0])
        s.append(f"<line x1='{px:.0f}' y1='{y}' x2='{px:.0f}' y2='{y + h}' stroke='#DCE6F5' stroke-width='1.5'/>" + tx(px, y + h + 16, lab, 15, 700, "#475467"))
    for v, lab in yt:
        _, py = P(xr[0], v)
        s.append(f"<line x1='{x}' y1='{py:.0f}' x2='{x + w}' y2='{py:.0f}' stroke='#DCE6F5' stroke-width='1.5'/>" + tx(x - 8, py, lab, 15, 700, "#475467", "end"))
    s.append(tx(x + w / 2, y + h + 40, xlab, 16, 800, NAV))
    s.append(f"<text x='{x - 62}' y='{y + h / 2}' font-family='Montserrat' font-size='16' font-weight='800' fill='{NAV}' text-anchor='middle' "
             f"transform='rotate(-90 {x - 62} {y + h / 2})'>{ylab}</text>")
    s.append(cuerpo_fn(P))
    return svg(0, 0, 1080, 1350, "".join(s))


def pts(P, lst):
    return " ".join(f"{P(a, b)[0]:.0f},{P(a, b)[1]:.0f}" for a, b in lst)


YT = [(.01, "0,01 s"), (.1, "0,1 s"), (1, "1 s"), (10, "10 s"), (120, "2 min"), (3600, "1 h"), (7200, "")]

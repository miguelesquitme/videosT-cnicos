"""Lote H (25-nov): 5 dispositivos × 6 infografías con fotos reales de larssystemgt.com (a pedido del autor).
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
.ph{position:absolute;background:#fff;border-radius:22px;border:3px solid #E4E7EC;box-shadow:0 10px 26px rgba(11,31,77,.10)}
.cap{position:absolute;font:700 15px Montserrat;color:#667085;text-align:center}
.crit{position:absolute;left:40px;right:40px;display:flex;gap:16px;align-items:stretch;background:#F6FAFF;border-radius:16px;overflow:hidden}
.crit .k{flex:none;width:64px;display:flex;align-items:center;justify-content:center;color:#fff;font:900 40px 'Barlow C'}
.crit .c{flex:1;padding:9px 14px 10px 4px;font:500 17px/1.3 Montserrat;color:#1d2939}.crit .c b{display:block;font:800 21px/1.15 Montserrat;color:#0B1F4D;margin-bottom:2px}
.crit .v{flex:none;padding:5px 12px;border-radius:9px;color:#fff;font:900 24px/1 'Barlow C';white-space:nowrap}
.vs{position:absolute;left:40px;right:40px;border-radius:18px;overflow:hidden;border:3px solid #0B1F4D;font:600 19px Montserrat;background:#fff}
.vs div{display:grid;grid-template-columns:1.15fr 1fr 1fr;align-items:center;border-top:2px solid #E4E7EC}.vs div:first-child{border-top:0}
.vs span{padding:8px 14px}.vs span+span{text-align:center;font:800 24px 'Barlow C';color:#0B1F4D;border-left:2px solid #E4E7EC}
.vs div.h span{background:#0B1F4D;color:#fff;font:800 18px Montserrat}.vs div.d{background:#FFF4E5}
.blk{position:absolute;border-radius:16px;padding:10px 14px;font:500 16px/1.28 Montserrat;color:#1d2939;background:#fff;border:3px solid #0B1F4D;text-align:center}
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


def rect(x0, y0, x1, y1, c, a=.17):
    return (f"<rect x='{x0:.0f}' y='{y0:.0f}' width='{x1 - x0:.0f}' height='{y1 - y0:.0f}' rx='8' fill='none' stroke='#fff' stroke-width='7' opacity='.85'/>"
            f"<rect x='{x0:.0f}' y='{y0:.0f}' width='{x1 - x0:.0f}' height='{y1 - y0:.0f}' rx='8' fill='{hexa(c, a)}' stroke='{c}' stroke-width='3.5'/>")


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
        out.append(f"<div class='lb' style='left:{lx}px;top:{ly - 30}px;width:{wl}px;border:3px solid {c};box-sizing:border-box'>"
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
        sv.append(rect(x0, y0, x1, y1, c, .15))
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
    return (f"<div class='blk' style='left:{x}px;top:{y}px;width:{w}px;{hh}border-color:{c};background:{bg}'>"
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

# ===================================================================== FUENTES
LS = "LARSSYSTEM Guatemala (larssystemgt.com/{}), usadas a pedido del autor"
F_GM = "CHINT, catálogo NS2 (manual motor starter) · placa del NS2-25X · IEC 60947-2 / IEC 60947-4-1"
F_BR = "CHINT, catálogo NXB-63 · IEC 60898-1 · marcado del equipo"
F_RE = "Relpol, hoja de datos R2N (2CO) · marcado del relé"
F_SE = "Autonics, catálogo serie PR · IEC 60947-5-2"
F_KM = "NOARK, hoja de datos Ex9C · placa del Ex9C50 · IEC 60947-4-1"

P = {}

# =====================================================================================================================
# GUARDAMOTOR CHINT NS2-25X 9–14 A
# =====================================================================================================================
C1 = AZ
f = Img("gm1", 200, 285, w=690)
P["H01_guardamotor_partes"] = page(DID,
    kick("GUARDAMOTOR · CHINT NS2-25X", C1) + T("Las partes del", "guardamotor", C1, sub="NS2-25X · 9–14 A · mando giratorio · térmico + magnético", size=60)
    + f.html() + cajas(f, [
        (1, (.33, .07, .70, .19), "Entrada 1/L1 3/L2 5/L3", "llega la red", 30, 345),
        (2, (.27, .29, .42, .47), "Dial 9–14 A", "ajuste del térmico", 30, 520),
        (3, (.27, .60, .46, .68), "TEST", "dispara el mecanismo", 30, 690),
        (4, (.33, .80, .70, .93), "Salida 2/T1 4/T2 6/T3", "va al contactor/motor", 30, 860),
        (5, (.53, .25, .72, .31), "Portaetiqueta", "designación -QM1", 760, 420),
        (6, (.44, .41, .71, .71), "Mando giratorio", "I-ON · O-OFF", 760, 590),
        (7, (.52, .69, .73, .75), "IEC 60947-2 / -4-1", "normas que cumple", 760, 760)], wl=280)
    + chips(985, [("9–14 A", "Rango del térmico: el dial va a la corriente de placa.", C1),
                  ("170 A", "Disparo magnético instantáneo (cortocircuito).", RJ),
                  ("CLASE 10A", "A 7,2 × Ir dispara entre 2 y 10 s.", NAR)])
    + nota(1125, "Un solo aparato: <b>seccionador + sobrecarga + cortocircuito + falta de fase</b>. Se monta en riel DIN de 35 mm."),
    F_GM, LS.format(6160))

# ---- H02 funcionamiento
f = Img("gm1", 20, 270, w=380)


def _gm_curva(P):
    s = []
    up = [(1.2, 7200), (1.5, 120), (3, 30), (7.2, 10), (12.1, 6), (12.1, .01)]
    s.append(f"<polyline points='{pts(P, up)}' fill='none' stroke='{AZ}' stroke-width='4' stroke-dasharray='10 6'/>")
    x7, y10 = P(7.2, 10)
    _, y2 = P(7.2, 2)
    s.append(f"<line x1='{x7:.0f}' y1='{y10:.0f}' x2='{x7:.0f}' y2='{y2:.0f}' stroke='{NAR}' stroke-width='12' stroke-linecap='round'/>")
    s.append(tx(x7 - 12, (y10 + y2) / 2, "7,2×: 2–10 s", 17, 800, NAR, "end"))
    for a, b, t, c, al in ((1.05, 7200, "1,05×: NO dispara en 2 h", VER, "start"), (1.2, 7200, "1,2×: dispara &lt; 2 h", AZ, "start"),
                           (1.5, 120, "1,5×: &lt; 2 min", AZ, "start")):
        px, py = P(a, b)
        s.append(f"<circle cx='{px:.0f}' cy='{py:.0f}' r='8' fill='{c}' stroke='#fff' stroke-width='3'/>")
        s.append(tx(px + 14, py + (-16 if a == 1.05 else 16 if a == 1.2 else 0), t, 16, 800, c, al))
    xm, _ = P(12.1, 1)
    s.append(f"<rect x='{xm - 4:.0f}' y='{P(12.1, 1)[1]:.0f}' width='8' height='{P(12.1, .01)[1] - P(12.1, 1)[1]:.0f}' fill='{RJ}' rx='4'/>")
    s.append(tx(xm - 10, P(12.1, .03)[1], "170 A = 12 × 14 A", 17, 800, RJ, "end"))
    s.append(tx(P(1.3, .02)[0], P(1.3, .02)[1], "curva: forma ilustrativa", 14, 600, "#98A2B3", "start"))
    return "".join(s)


P["H02_guardamotor_funcionamiento"] = page(DID,
    kick("GUARDAMOTOR · CÓMO DISPARA", C1) + T("Tres disparos en", "un aparato", C1, sub="Térmico, magnético y falta de fase actúan sobre el mismo mecanismo", size=58)
    + ph(20, 265, 390, 400) + f.html(False) + marcas(f, [(1, (.27, .29, .42, .47), "", "", 0, 0), (2, (.44, .41, .71, .71), "", "", 0, 0)])
    + "<div style='position:absolute;left:430px;right:40px;top:265px;display:grid;gap:10px'>"
    + "".join(f"<div style='border-radius:16px;background:#F6FAFF;border-left:10px solid {c};padding:10px 16px;font:500 17px/1.3 Montserrat;color:#1d2939'>"
              f"<b style='display:block;font:900 29px/1.05 \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for t, d, c in (
                  ("TÉRMICO · SOBRECARGA", "Un <b>bimetal por fase</b> se calienta con la corriente. Al pasar de 1,2 × Ir se dobla, empuja la regleta y abre los 3 polos.", AZ),
                  ("MAGNÉTICO · CORTOCIRCUITO", "Una <b>bobina por fase</b> atrae su núcleo al llegar a <b>170 A</b> y golpea el mecanismo: abre al instante, sin fusibles.", RJ),
                  ("FALTA DE FASE", "La regleta <b>diferencial</b> compara las 3 fases: una en cero y las otras a 1,15 × Ir → dispara en menos de 2 h.", NAR)))
    + "</div>"
    + curva(130, 715, 900, 360, (1, 20), (.01, 7200), _gm_curva,
            [(1, "1"), (1.2, "1,2"), (1.5, "1,5"), (2, "2"), (3, "3"), (5, "5"), (7.2, "7,2"), (10, "10"), (12.1, "12"), (20, "20")], YT,
            "múltiplos de la corriente ajustada Ir (con Ir = 14 A)")
    + nota(1150, "1 = dial (ajuste del térmico) · 2 = mando: tras un disparo se <b>rearma</b> girándolo a O y luego a I."),
    F_GM + " (tabla de disparo clase 10A, falta de fase)", LS.format(6160))

# ---- H03 criterios
f = Img("gm4r", 30, 290, w=500)
P["H03_guardamotor_criterios"] = page(DID,
    kick("GUARDAMOTOR · SELECCIÓN", C1) + T("Cómo escoger el", "guardamotor", C1, sub="Todo sale de la placa del motor y de la placa del NS2-25X", size=60)
    + ph(20, 280, 520, 560) + f.html(False) + letras(f, [
        ("A", (.61, .39, .86, .49), AZ, "tr"), ("B", (.61, .49, .86, .67), RJ, "br"), ("C", (.46, .58, .63, .65), VER, "bl")])
    + cap(20, 850, 520, "placa lateral del NS2-25X (foto girada)")
    + leyenda(890, [("A", "Ie 9–14 A", "AC-3, Ue 690 V, Uimp 8 kV", AZ), ("B", "Icu / Ics", "100 kA a 230/240 V · 15 kA a 400 V", RJ),
                    ("C", "Potencia", "3 kW a 230 V · 5,5 kW a 400 V", VER)], cols=1, x=30, w=490)
    + crit(285, [("Corriente del motor", "La de placa debe caer dentro del rango; el dial se pone en ella.", "9–14 A", AZ),
                 ("Tensión de la red", "Ue del aparato ≥ tensión entre fases (208/240 V).", "690 V", NAV),
                 ("Poder de corte", "Icu ≥ corriente de cortocircuito donde se instala.", "100 kA", RJ),
                 ("Clase de disparo", "10A = arranque normal. Arranques largos piden clase 20 o 30.", "10A", NAR),
                 ("Potencia de referencia", "Placa del NS2-25X: 3 kW a 230 V.", "3 kW", VER),
                 ("Accesorios", "Auxiliares frontales NS2-AE11/AE20 o laterales AU11/AU20.", "1NA+1NC", MOR)], x=560, w=480)
    + nota(1065, "Si el motor marca más de 14 A, ya no es este: sube al rango siguiente (13–18 A). Nunca ajustes el dial <b>por encima</b> de la placa.").replace("top:1065px", "top:1065px"),
    F_GM, LS.format(6160))

# ---- H04 aplicación
fq = Img("gm1", 120, 380, w=330)
fk = Img("km1", 120, 690, w=330)
P["H04_guardamotor_aplicacion"] = page(DID,
    kick("GUARDAMOTOR · CASO REAL", C1) + T("Bomba de 3 hp con", "guardamotor", C1, sub="Red 208 V trifásica · arranque directo · sin fusibles", size=58)
    + blk(150, 285, 270, "RED 208 V 3~", "L1 · L2 · L3 · PE", NAV)
    + fq.html() + marcas(fq, [(1, (.27, .29, .42, .47))])
    + fk.html()
    + blk(150, 1005, 270, "MOTOR 3 hp", "208 V · jaula de ardilla", NAV)
    + svg(0, 0, 1080, 1350, flecha(285, 360, 285, 395) + flecha(285, 668, 285, 712) + flecha(285, 975, 285, 1005))
    + "<div style='position:absolute;left:40px;top:500px;font:900 32px \"Barlow C\";color:#0057FF'>-QM1</div>"
    + "<div style='position:absolute;left:40px;top:810px;font:900 32px \"Barlow C\";color:#0B1F4D'>-KM1</div>"
    + "<div style='position:absolute;left:480px;top:520px;width:120px;font:600 14px/1.25 Montserrat;color:#475467'>1 = dial a la corriente de placa</div>"
    + "<div style='position:absolute;left:620px;right:40px;top:285px;display:grid;gap:12px'>"
    + "".join(f"<div style='border-radius:16px;background:#F6FAFF;border-left:10px solid {c};padding:10px 16px;font:500 17px/1.3 Montserrat;color:#1d2939'>"
              f"<b style='display:block;font:900 30px/1.05 \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for t, d, c in (
                  ("10,6 A", "Corriente de tabla NEC 430.250 para 3 hp a 208 V → entra en 9–14 A.", AZ),
                  ("DIAL = PLACA", "Se ajusta a la corriente de placa del motor, no a la de tabla.", NAR),
                  ("14 AWG", "Conductor al 125 %: 13,3 A → 14 AWG THHN (75 °C).", VER),
                  ("170 A", "Si hay cortocircuito, el magnético abre en milisegundos.", RJ),
                  ("100 kA", "Icu a 230/240 V: aguanta la falla del tablero sin fusibles.", MOR)))
    + "</div>"
    + nota(1110, "En instalaciones NEC, para que proteja <b>solo</b> el cortocircuito debe estar listado como <b>Tipo E</b>; si no, se pone breaker o fusibles antes."),
    F_GM + " · NEC 2020 T430.250, 430.22, 430.32, 430.52", LS.format(6160) + " · contactor: larssystemgt.com/4060")

# ---- H05 versus
f = Img("gm1", 60, 290, w=420)
P["H05_guardamotor_versus"] = page(DID,
    kick("GUARDAMOTOR · COMPARACIÓN", C1) + T("NS2-25X contra", "GV2ME16", C1, sub="CHINT vs Schneider Electric TeSys Deca · mismo rango 9–14 A", size=60)
    + ph(40, 280, 460, 420) + f.html(False) + cap(40, 710, 460, "CHINT NS2-25X")
    + rival(580, 280, 460, 420, "SCHNEIDER ELECTRIC", "TeSys Deca · GV2ME", "GV2ME16", "Guardamotor 3P, 9–14 A, magnetotérmico, mando por pulsadores")
    + vsbadge(540, 490)
    + versus(750, "NS2-25X", "GV2ME16", [
        ("Rango térmico", "9–14 A", "9–14 A"), ("Disparo magnético", "170 A", "170 A"),
        ("Icu a 230/240 V", "100 kA", "100 kA"), ("Icu a 400/415 V", "15 kA", "15 kA"), ("Icu a 690 V", "3 kA", "3 kA"),
        ("Uimp", "8 kV", "6 kV"), ("Mando", "giratorio", "pulsadores"), ("Motor a 400 V", "5,5 kW", "5,5 kW")], dif=(5, 6))
    + nota(1180, "Eléctricamente <b>equivalentes</b>: cambia el mando (giratorio vs pulsadores I/O) y la Uimp. Escoge por precio y repuesto local."),
    F_GM + " · Schneider Electric, hoja de datos GV2ME16 (se.com, RS)", LS.format(6160))

# ---- H06 símbolo
s = Img("04_guardamotor_simbolo", 40, 300, w=470)
f = Img("gm1", 530, 270, w=530)
f2 = Img("gm4r", 640, 790, w=330)
P["H06_guardamotor_simbolo"] = page(DID,
    kick("GUARDAMOTOR · SÍMBOLO IEC 60617", C1) + T("Símbolo del", "guardamotor", C1, sub="Cada parte del símbolo está en el equipo", size=60)
    + ph(30, 280, 490, 450) + s.html(False)
    + letras(s, [("A", (.10, .22, .22, .36), AZ), ("B", (.30, .02, .82, .38), RJ, "tr"), ("C", (.28, .53, .88, .65), NAR, "tr"),
                 ("D", (.28, .65, .88, .77), MOR, "br"), ("E", (.30, .78, .82, .94), VER, "bl")])
    + f.html() + letras(f, [("A", (.44, .41, .71, .71), AZ, "tr"), ("B", (.33, .07, .70, .19), RJ, "tr"), ("C", (.27, .29, .42, .47), NAR),
                            ("E", (.33, .80, .70, .93), VER, "bl")])
    + f2.html() + letras(f2, [("F", (.46, .43, .57, .59), TEAL, "tr")])
    + cap(560, 1150, 480, "F: el mismo símbolo impreso en la placa lateral")
    + leyenda(750, [("A", "Mando manual", "→ mando giratorio I/O", AZ), ("B", "Polos 1/L1 3/L2 5/L3 (×)", "→ bornes de entrada", RJ),
                    ("C", "Disparador térmico", "→ dial 9–14 A", NAR), ("D", "Disparador magnético I&gt;", "→ adentro, 170 A (no se ve)", MOR),
                    ("E", "Salidas 2/T1 4/T2 6/T3", "→ bornes de abajo", VER), ("F", "Símbolo en placa", "→ costado del equipo", TEAL)], cols=1, x=30, w=490)
    ,
    "IEC 60617 (símbolos) · IEC 81346 (designación -QM) · " + F_GM, LS.format(6160) + " · símbolo: catálogo @miguelesquit")

# =====================================================================================================================
# BREAKER CHINT NXB-63 2P C40
# =====================================================================================================================
C2 = NAR
f = Img("br1", 170, 285, w=700)
P["H07_breaker_partes"] = page(DID,
    kick("BREAKER · CHINT NXB-63 2P C40", C2) + T("Las partes del", "breaker", C2, sub="Interruptor termomagnético de 2 polos, 40 A, curva C", size=62)
    + f.html() + cajas(f, [
        (1, (.30, .08, .68, .21), "Entrada 1 · 3", "bornes de arriba", 30, 360),
        (2, (.31, .34, .40, .41), "C40", "curva C · In = 40 A", 30, 500),
        (3, (.31, .41, .39, .48), "400 V~ · 6000", "Ue y Icn = 6000 A", 30, 610),
        (4, (.31, .48, .47, .54), "IEC/EN 60898-1", "norma del breaker", 30, 720),
        (8, (.30, .79, .68, .91), "Salida 2 · 4", "bornes de abajo", 30, 880),
        (5, (.38, .40, .45, .46), "Ventanilla", "posición del contacto", 770, 420),
        (6, (.53, .45, .61, .53), "Símbolo impreso", "1-3 arriba, 2-4 abajo", 770, 560),
        (7, (.31, .54, .67, .78), "Palanca unida", "los 2 polos abren juntos", 770, 700)], wl=270)
    + chips(985, [("40 A", "Corriente nominal In a 30 °C.", C2), ("CURVA C", "Magnético entre 5 y 10 × In: 200–400 A.", RJ),
                  ("6 kA", "Icn: máxima falla que interrumpe.", AZ)])
    + nota(1125, "Arriba entra la línea y abajo sale la carga; la palanca <b>única</b> evita que quede una fase energizada."),
    F_BR, LS.format(10146))

# ---- H08 funcionamiento


def _br_curva(P):
    s = []
    x5, ytop = P(5, 7200)
    x10, ybot = P(10, .01)
    _, y01 = P(5, .1)
    s.append(f"<rect x='{x5:.0f}' y='{y01:.0f}' width='{x10 - x5:.0f}' height='{ybot - y01:.0f}' fill='{hexa(RJ, .22)}' stroke='{RJ}' stroke-width='2.5'/>")
    s.append(tx((x5 + x10) / 2, y01 - 16, "magnético C", 16, 800, RJ))
    s.append(tx((x5 + x10) / 2, (y01 + ybot) / 2, "5–10 × In", 16, 800, RJ))
    xa, ya = P(2.55, 120)
    _, yb = P(2.55, 1)
    s.append(f"<line x1='{xa:.0f}' y1='{ya:.0f}' x2='{xa:.0f}' y2='{yb:.0f}' stroke='{NAR}' stroke-width='12' stroke-linecap='round'/>")
    s.append(tx(xa + 14, (ya + yb) / 2, "2,55×: 1–120 s", 16, 800, NAR, "start"))
    for a, b, t, c in ((1.13, 3600, "1,13×: NO dispara en 1 h", VER), (1.45, 3600, "1,45×: dispara &lt; 1 h", AZ)):
        px, py = P(a, b)
        s.append(f"<circle cx='{px:.0f}' cy='{py:.0f}' r='8' fill='{c}' stroke='#fff' stroke-width='3'/>")
        s.append(tx(px + 14, py + (-18 if a == 1.13 else 18), t, 16, 800, c, "start"))
    up = [(1.45, 3600), (2.55, 120), (5, 25), (10, 8), (10, .01)]
    s.append(f"<polyline points='{pts(P, up)}' fill='none' stroke='{AZ}' stroke-width='4' stroke-dasharray='10 6'/>")
    s.append(tx(P(1.2, .02)[0], P(1.2, .02)[1], "curva: forma ilustrativa", 14, 600, "#98A2B3", "start"))
    return "".join(s)


f = Img("br1", 0, 270, w=420)
P["H08_breaker_funcionamiento"] = page(DID,
    kick("BREAKER · CÓMO DISPARA", C2) + T("Así dispara un", "breaker C40", C2, sub="Dos disparadores por polo y una cámara que apaga el arco", size=60)
    + ph(20, 265, 390, 400) + f.html(False)
    + "<div style='position:absolute;left:430px;right:40px;top:265px;display:grid;gap:10px'>"
    + "".join(f"<div style='border-radius:16px;background:#F6FAFF;border-left:10px solid {c};padding:10px 16px;font:500 17px/1.3 Montserrat;color:#1d2939'>"
              f"<b style='display:block;font:900 29px/1.05 \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for t, d, c in (
                  ("BIMETAL · SOBRECARGA", "Con 40 A: <b>45 A</b> (1,13 ×) no dispara en 1 h; <b>58 A</b> (1,45 ×) dispara en menos de 1 h; <b>102 A</b> (2,55 ×) entre 1 y 120 s.", AZ),
                  ("BOBINA · CORTOCIRCUITO", "Curva C: a <b>200 A</b> (5 ×) no debe disparar en 0,1 s; a <b>400 A</b> (10 ×) dispara en menos de 0,1 s.", RJ),
                  ("CÁMARA DE ARCO", "Las placas metálicas dividen y enfrían el arco al abrir; corta hasta <b>6000 A</b> (Icn).", NAR)))
    + "</div>"
    + curva(130, 715, 900, 360, (1, 20), (.01, 7200), _br_curva,
            [(1, "1"), (1.13, ""), (1.45, "1,45"), (2, "2"), (2.55, "2,55"), (5, "5"), (10, "10"), (20, "20")], YT,
            "múltiplos de In  (In = 40 A → 5 × = 200 A, 10 × = 400 A)")
    + nota(1150, "La zona roja es la <b>curva C</b>: tolera el arranque de motores pequeños y transformadores sin disparar."),
    F_BR + " · tiempos convencionales para In ≤ 63 A", LS.format(10146))

# ---- H09 criterios
f = Img("br1", 0, 300, w=560)
P["H09_breaker_criterios"] = page(DID,
    kick("BREAKER · SELECCIÓN", C2) + T("Cómo escoger el", "breaker", C2, sub="Lo que dice el frente del NXB-63 y lo que debes comprobar", size=60)
    + ph(20, 280, 520, 560) + f.html(False)
    + letras(f, [("A", (.31, .34, .40, .41), AZ), ("B", (.31, .41, .39, .48), RJ, "bl"), ("C", (.31, .48, .47, .54), VER, "br"),
                 ("D", (.31, .54, .67, .78), NAR, "tr")])
    + leyenda(860, [("A", "C40", "curva C y 40 A", AZ), ("B", "400 V~ · 6000", "tensión y Icn en A", RJ), ("C", "IEC/EN 60898-1", "norma", VER),
                    ("D", "2 polos", "una palanca", NAR)], cols=2, x=30, w=490)
    + crit(285, [("Corriente In", "Protege al CONDUCTOR: 40 A pide mínimo 8 AWG THHN (10 AWG llega a 30 A).", "40 A", AZ),
                 ("Curva", "B: resistivas · C: motores pequeños, transformadores · D: arranques fuertes.", "C", RJ),
                 ("Poder de corte", "Icn ≥ corriente de cortocircuito en el tablero (hay versión de 10 kA).", "6 kA", NAR),
                 ("Polos", "A 208/240 V entre fases las dos líneas tienen tensión: 2 polos.", "2P", VER),
                 ("Tensión", "230/400 V: sirve en redes de 120/208 V y 120/240 V.", "400 V", NAV),
                 ("Vida útil", "Eléctrica 10 000 maniobras · mecánica 20 000.", "10 000", MOR)], x=560, w=480)
    + nota(1065, "Primero el <b>conductor</b>, luego el breaker: el breaker nunca debe ser mayor que lo que aguanta el cable."),
    F_BR + " · NEC 2020 240.4(D), T310.16", LS.format(10146))

# ---- H10 aplicación
fb = Img("br1", 290, 410, w=330)
P["H10_breaker_aplicacion"] = page(DID,
    kick("BREAKER · CASO REAL", C2) + T("Calentador de 6 kW a", "208 V", C2, sub="Carga resistiva continua entre dos fases", size=60)
    + blk(320, 280, 270, "BARRAS L1 · L2", "208 V entre fases", NAV)
    + fb.html()
    + "<div style='position:absolute;left:80px;top:560px;font:900 34px \"Barlow C\";color:#FF8A00'>-F1</div>"
    + blk(320, 760, 270, "8 AWG THHN", "2 líneas + tierra", NAV)
    + blk(320, 900, 270, "CALENTADOR", "6 kW · 208 V · 1~", NAR)
    + svg(0, 0, 1080, 1350, flecha(455, 360, 455, 430) + flecha(455, 728, 455, 760) + flecha(455, 840, 455, 900))
    + "<div style='position:absolute;left:640px;right:40px;top:280px;display:grid;gap:12px'>"
    + "".join(f"<div style='border-radius:16px;background:#F6FAFF;border-left:10px solid {c};padding:10px 16px;font:500 17px/1.3 Montserrat;color:#1d2939'>"
              f"<b style='display:block;font:900 30px/1.05 \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for t, d, c in (
                  ("28,8 A", "I = 6000 W ÷ 208 V.", AZ),
                  ("× 1,25 = 36 A", "Carga continua (3 h o más): breaker al 125 %.", NAR),
                  ("40 A · 2P", "Siguiente valor estándar; 2 polos porque L1 y L2 tienen tensión.", RJ),
                  ("8 AWG", "50 A a 75 °C; el 10 AWG solo se protege hasta 30 A.", VER),
                  ("CURVA C", "Aquí bastaría B; la C también sirve (no hay arranque).", MOR)))
    + "</div>"
    + nota(1060, "Con breaker de 1 polo, al disparar quedaría <b>L2 energizada</b> dentro del calentador: por eso 2P con palanca unida."),
    F_BR + " · NEC 2020 210.19(A), 210.20(A), 240.4(D), T310.16", LS.format(10146))

# ---- H11 versus
f = Img("br1", 60, 280, w=420)
P["H11_breaker_versus"] = page(DID,
    kick("BREAKER · COMPARACIÓN", C2) + T("NXB-63 contra", "S202-C40", C2, sub="CHINT vs ABB System pro M compact S200 · 2P · C · 40 A", size=60)
    + ph(40, 280, 460, 420) + f.html(False) + cap(40, 710, 460, "CHINT NXB-63 2P C40")
    + rival(580, 280, 460, 420, "ABB", "System pro M compact · S200", "S202-C40", "Breaker 2P, 40 A, curva C, 6 kA")
    + vsbadge(540, 490)
    + versus(750, "NXB-63 C40", "S202-C40", [
        ("Corriente In", "40 A", "40 A"), ("Curva", "C", "C"), ("Icn (IEC 60898-1)", "6 kA", "6 kA"),
        ("Uimp", "4 kV", "4 kV"), ("Vida eléctrica", "10 000", "10 000"), ("Vida mecánica", "20 000", "20 000"),
        ("Otras normas", "—", "IEC 60947-2 · UL 1077"), ("Tensión máx.", "400 V", "440 V")], dif=(6, 7))
    + nota(1180, "Para el mismo circuito son <b>intercambiables</b>; el ABB trae doble norma y listado UL 1077 (suplementario, no sustituye a un UL 489)."),
    F_BR + " · ABB, hojas de datos S200 (S202-C40, RS / Farnell)", LS.format(10146))

# ---- H12 símbolo
s = Img("02_disyuntor_2p_simbolo", 70, 300, w=420)
f = Img("br1", 470, 270, w=640)
P["H12_breaker_simbolo"] = page(DID,
    kick("BREAKER · SÍMBOLO IEC 60617", C2) + T("Símbolo del", "breaker 2P", C2, sub="El símbolo viene impreso en el propio frente", size=60)
    + ph(30, 280, 480, 420) + s.html(False)
    + letras(s, [("A", (.30, .08, .80, .30), AZ, "tr"), ("B", (.36, .32, .80, .48), RJ, "tr"), ("C", (.38, .45, .64, .53), NAR, "bl"),
                 ("D", (.30, .60, .80, .95), VER, "br")])
    + f.html() + letras(f, [("A", (.30, .08, .68, .21), AZ, "tr"), ("C", (.31, .54, .67, .78), NAR, "tr"), ("D", (.30, .79, .68, .91), VER, "br"),
                            ("E", (.53, .45, .61, .53), TEAL, "tr")])
    + leyenda(740, [("A", "Bornes 1 y 3", "→ entradas de arriba", AZ), ("B", "× función de disyuntor", "→ disparo térmico y magnético dentro", RJ),
                    ("C", "Línea de acción", "→ palanca unida de los 2 polos", NAR), ("D", "Bornes 2 y 4", "→ salidas de abajo", VER),
                    ("E", "Símbolo impreso", "→ al lado de la palanca", TEAL)], cols=1, x=30, w=490)
    + nota(1180, "La <b>×</b> en el contacto distingue al disyuntor del simple interruptor; la línea punteada dice que los polos se mueven juntos."),
    "IEC 60617 · IEC 81346 (-F) · " + F_BR, LS.format(10146) + " · símbolo: catálogo @miguelesquit")

# =====================================================================================================================
# RELÉ RELPOL R2N 2CO 230 VAC
# =====================================================================================================================
C3 = RJ
f = Img("re2", 190, 280, w=700)
P["H13_rele_partes"] = page(DID,
    kick("RELÉ · RELPOL R2N-2012-23-5230-WTL", C3) + T("Las partes del", "relé", C3, sub="Relé enchufable de 2 contactos conmutados, bobina 230 VAC", size=62)
    + f.html() + cajas(f, [
        (1, (.07, .26, .20, .43), "Botón de prueba", "bloqueable · naranja = AC", 20, 340),
        (2, (.28, .33, .52, .46), "Armadura", "la atrae la bobina", 20, 500),
        (3, (.14, .66, .21, .80), "LED", "bobina energizada", 20, 700),
        (4, (.53, .30, .64, .45), "Indicador mecánico", "se mueve con el contacto", 780, 330),
        (5, (.64, .27, .80, .42), "Contactos 2 CO", "AgNi · 12 A 250 VAC", 780, 460),
        (6, (.37, .46, .70, .72), "Bobina 230 VAC", "1,6 VA a 50 Hz", 780, 620),
        (7, (.80, .25, .91, .65), "Pines faston", "al zócalo GZT2/GZM2", 780, 780)], wl=280)
    + chips(985, [("2 CO", "Dos conmutados: 11-12-14 y 41-42-44.", C3), ("12 A · 250 VAC", "Carga resistiva AC1 (3000 VA).", AZ),
                  ("WTL", "W indicador · T botón de prueba · L LED.", NAR)])
    + nota(1125, "Mide <b>27,4 × 21 × 35,5 mm</b> y se enchufa en zócalo de riel DIN 35 mm; se cambia sin desconectar cables."),
    F_RE, LS.format(50900))

# ---- H14 funcionamiento
f = Img("re2", 20, 270, w=560)
P["H14_rele_funcionamiento"] = page(DID,
    kick("RELÉ · CÓMO FUNCIONA", C3) + T("Así conmuta un", "relé", C3, sub="Se ve a través de la tapa transparente del R2N", size=62)
    + f.html() + marcas(f, [(1, (.37, .46, .70, .72), "", "", 0, 0), (2, (.28, .33, .52, .46), "", "", 0, 0), (3, (.64, .27, .80, .42), "", "", 0, 0),
                           (4, (.14, .66, .21, .80), "", "", 0, 0)])
    + "<div style='position:absolute;left:600px;right:40px;top:270px;display:grid;gap:10px'>"
    + "".join(f"<div style='display:flex;gap:12px;align-items:center;border-radius:14px;background:#F6FAFF;padding:8px 12px;font:500 16px/1.28 Montserrat;color:#1d2939'>"
              f"<div style='flex:none;width:38px;height:38px;border-radius:50%;background:{c};color:#fff;font:800 19px/38px Montserrat;text-align:center'>{n}</div>"
              f"<div><b style='color:#0B1F4D'>{t}</b> {d}</div></div>" for n, t, d, c in (
                  (1, "Bobina:", "llegan 230 VAC a A1-A2 y circulan ≈ 7 mA (1,6 VA).", CL[0]),
                  (2, "Armadura:", "el campo la atrae y empuja la carta de contactos.", CL[1]),
                  (3, "Contactos:", "los comunes 11 y 41 dejan el NC y tocan el NA.", CL[2]),
                  (4, "LED:", "se enciende mientras haya tensión en la bobina.", CL[3])))
    + "</div>"
    + tabla(830, [("Bobina A1-A2", "0 V  →  230 V"), ("11-12 · 41-42 (NC)", "cerrado → ABIERTO"), ("11-14 · 41-44 (NA)", "abierto → CERRADO"),
                  ("LED / indicador", "apagado → ENCENDIDO")], cab="<span>ESTADO</span><span style='flex:none'>REPOSO → ENERGIZADO</span>", extra="font-size:20px")
    + nota(1135, "Cierra con <b>184 a 253 V</b> en la bobina. El botón naranja mueve los contactos a mano para <b>probar sin tensión</b> en la bobina."),
    F_RE, LS.format(50900))

# ---- H15 criterios
f = Img("re1", 20, 300, w=500)
P["H15_rele_criterios"] = page(DID,
    kick("RELÉ · SELECCIÓN", C3) + T("Cómo escoger el", "relé", C3, sub="La tensión de la bobina y el tipo de carga deciden", size=62)
    + ph(20, 280, 520, 500) + f.html(False)
    + letras(f, [("A", (.36, .63, .78, .72), AZ, "tr"), ("B", (.44, .72, .78, .81), RJ, "br"), ("C", (.25, .03, .82, .18), NAR, "tr")])
    + leyenda(800, [("A", "R2N-2012-23-5230-WTL", "modelo completo", AZ), ("B", "230 V AC", "tensión de bobina", RJ),
                    ("C", "Botón naranja", "bobina de AC (verde = DC)", NAR)], cols=1, x=30, w=490)
    + crit(285, [("Tensión de bobina", "Cierra entre 184 y 253 V: sirve a 208 o 240 V entre fases; a 120 V NO.", "230 VAC", AZ),
                 ("Carga resistiva", "AC1 12 A a 250 V (3000 VA). DC1: 12 A a 24 V.", "12 A", RJ),
                 ("Carga inductiva", "Bobinas y pilotos (AC15): 1,5 A a 240 V, 3 A a 120 V.", "1,5 A", NAR),
                 ("Carga mínima", "10 V / 5 mA. Para señales de PLC usa contactos dorados (AgNi/Au).", "5 mA", VER),
                 ("Zócalo", "GZT2 o GZM2: 12 A, 300 V, riel 35 mm, tornillo.", "GZT2", NAV),
                 ("Temperatura", "Con bobina AC: −40 a +55 °C.", "55 °C", MOR)], x=560, w=480)
    + nota(1065, "Los 12 A son para carga <b>resistiva</b>. Para una bobina de contactor o un motor, mira la categoría AC15, que es mucho menor."),
    F_RE, LS.format(50900))

# ---- H16 aplicación
fr = Img("re1", 395, 470, w=290)
P["H16_rele_aplicacion"] = page(DID,
    kick("RELÉ · CASO REAL", C3) + T("El PLC sabe que el", "motor arrancó", C3, sub="Mando a 240 V separado de las entradas de 24 VDC", size=56)
    + blk(360, 290, 360, "MANDO 240 VAC", "A1-A2 en paralelo con la bobina de -KM1", NAV)
    + fr.html()
    + "<div style='position:absolute;left:700px;top:620px;font:900 34px \"Barlow C\";color:#E5383B'>-KA1</div>"
    + blk(40, 910, 470, "11-14 → PLC  I0.0", "24 VDC; aislamiento 4 kV entre bobina y contactos", AZ)
    + blk(570, 910, 470, "41-44 → PILOTO -H1", "verde 240 V: «motor en marcha»", VER)
    + svg(0, 0, 1080, 1350, flecha(540, 395, 540, 470) + flecha(470, 775, 275, 905, AZ) + flecha(610, 775, 805, 905, VER))
    + chips(1050, [("CARGA MÍNIMA", "Una entrada de PLC toma ≈ 4 mA: menos que 5 mA → pide contactos dorados.", RJ),
                   ("NC LIBRES", "11-12 y 41-42 quedan para alarmas o enclavamientos.", NAR)], cols=2)
    + nota(1185, "El relé <b>separa</b> dos tensiones: 240 VAC del mando y 24 VDC del PLC nunca se tocan."),
    F_RE + " · Siemens, S7-1200 (entrada 24 VDC ≈ 4 mA)", LS.format(50900))

# ---- H17 versus
f = Img("re1", 70, 290, w=400)
P["H17_rele_versus"] = page(DID,
    kick("RELÉ · COMPARACIÓN", C3) + T("R2N contra", "Finder 56.32", C3, sub="Relpol vs Finder · 2 CO · 12 A · bobina 230 VAC", size=60)
    + ph(40, 280, 460, 420) + f.html(False) + cap(40, 710, 460, "Relpol R2N-2012-23-5230-WTL")
    + rival(580, 280, 460, 420, "FINDER", "Serie 56 · relé de potencia", "56.32", "56.32.8.230.0040 · 2 CO, 12 A, bobina 230 VAC")
    + vsbadge(540, 490)
    + versus(750, "R2N", "56.32", [
        ("Contactos", "2 CO · 12 A", "2 CO · 12 A"), ("AC1", "3000 VA", "3000 VA"), ("Bobina 230 VAC", "1,6 VA", "1,5 VA"),
        ("Rango de bobina", "184–253 V", "184–253 V"), ("Vida eléctrica AC1", "100 000", "100 000"),
        ("Aislamiento bobina-contacto", "4 kV", "4 kV"), ("Extras", "botón + indicador + LED", "botón + indicador"),
        ("Zócalo", "GZT2 / GZM2", "serie 96")], dif=(6, 7))
    + nota(1180, "Hacen lo mismo; el R2N agrega LED. Usa el <b>zócalo de su propia marca</b> para asegurar contacto y retención."),
    F_RE + " · Finder, hoja serie 56 (56.32) · RS, Conrad", LS.format(50900))

# ---- H18 símbolo (compuesto con simsvg)
sym = (AQ / "img" / "rele_r2n_simbolo.svg").read_text().replace("<svg ", "<svg style='position:absolute;left:30px;top:300px;width:500px;height:198px' ", 1)


class _Box:
    def __init__(s, x, y, w, h):
        s.x, s.y, s.w, s.h = x, y, w, h

    def r(s, b):
        return s.x + b[0] * s.w, s.y + b[1] * s.h, s.x + b[2] * s.w, s.y + b[3] * s.h


sb = _Box(30, 300, 500, 198)
f4 = Img("re4", 560, 270, w=490)
f5 = Img("re5", 40, 560, w=440)
P["H18_rele_simbolo"] = page(DID,
    kick("RELÉ · SÍMBOLO IEC 60617", C3) + T("Símbolo del", "relé 2 CO", C3, sub="Numeración nueva (EN 50005) y antigua del zócalo", size=60)
    + ph(20, 285, 520, 230) + sym
    + letras(sb, [("A", (.15, .12, .27, .88), AZ), ("B", (.42, .12, .62, .88), RJ, "tr"), ("C", (.70, .12, .90, .88), VER, "tr")])
    + f4.html() + letras(f4, [("B", (.36, .37, .47, .62), RJ), ("C", (.50, .37, .61, .62), VER, "tr"), ("A", (.61, .37, .71, .62), AZ, "br")])
    + cap(560, 745, 490, "costado del relé: diagrama impreso")
    + f5.html() + letras(f5, [("B", (.19, .05, .37, .57), RJ), ("C", (.57, .05, .75, .57), VER, "tr"), ("A", (.19, .60, .75, .78), AZ, "bl")])
    + cap(40, 1010, 440, "base: pines 1 · 4 · 5 · 8 · 9 · 12 · 13 · 14")
    + tabla(790, [("A · bobina", "A1 = 13 · A2 = 14"), ("B · contacto 1", "11 = 9 · 12 = 1 · 14 = 5"), ("C · contacto 2", "41 = 12 · 42 = 4 · 44 = 8")],
            cab="<span>NUEVA = ANTIGUA</span>", extra="left:520px;font-size:18px")
    + nota(1060, "<b>11/41</b> = común · <b>12/42</b> = NC · <b>14/44</b> = NA. No es el relé octal de 8 pines (bobina 2-7): sus bornes son distintos."),
    "IEC 60617 · EN 50005 (numeración de bornes) · " + F_RE, LS.format(50900) + " · símbolo armado con la librería IEC @miguelesquit")

# =====================================================================================================================
# SENSOR INDUCTIVO AUTONICS PR12-2DP
# =====================================================================================================================
C4 = TEAL
f = Img("se2", 160, 280, w=720)
f1 = Img("se1", 760, 830, w=300)
P["H19_sensor_partes"] = page(DID,
    kick("SENSOR INDUCTIVO · AUTONICS PR12-2DP", C4) + T("Las partes del", "sensor inductivo", C4, sub="M12 · 2 mm · PNP normalmente abierto · 3 hilos", size=58)
    + f.html() + cajas(f, [
        (1, (.05, .00, .25, .34), "Cable 3 hilos", "BN + · BU − · BK salida", 20, 330),
        (2, (.16, .29, .33, .52), "Cabeza trasera", "LED rojo de operación", 20, 520),
        (3, (.38, .38, .67, .72), "Cuerpo M12 × 1", "rosca metálica, enrasado", 770, 420),
        (4, (.55, .62, .74, .84), "Cara activa", "aquí sale el campo", 770, 640)], wl=280)
    + f1.html() + cajas(f1, [(5, (.62, .26, .93, .48), "Puntas", "café, azul y negro", 470, 925)], wl=270)
    + chips(1020, [("2 mm", "Distancia nominal Sn (hierro 12×12×1 mm).", C4), ("1,5 kHz", "Hasta 1500 detecciones por segundo.", AZ),
                   ("10–30 VDC", "Consumo máx. 10 mA · carga máx. 200 mA.", NAR), ("IP67", "Polvo y agua.", VER)], cols=4)
    + nota(1165, "No necesita tocar la pieza: detecta <b>metal</b> por campo magnético; no se desgasta."),
    F_SE, LS.format(37750))

# ---- H20 funcionamiento
blocks = [("OSCILADOR", "LC a alta frecuencia", AZ), ("BOBINA", "ferrita abierta: campo en la cara", TEAL),
          ("METAL", "corrientes de Foucault roban energía", NAR), ("COMPARADOR", "umbral con histéresis", MOR), ("SALIDA PNP", "BK pasa a +V", RJ)]


def _amp():
    x, y, w, h = 560, 640, 460, 290
    s = [f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='#F6FAFF' stroke='#CFE0F5' stroke-width='2' rx='6'/>"]
    pts_ = []
    for i in range(61):
        d = 4 * i / 60
        a = 1 - math.exp(-1.2 * d)
        pts_.append(f"{x + d / 4 * w:.0f},{y + h - 20 - a * (h - 50):.0f}")
    s.append(f"<polyline points='{' '.join(pts_)}' fill='none' stroke='{AZ}' stroke-width='4'/>")
    a2 = 1 - math.exp(-1.2 * 2)
    yu = y + h - 20 - a2 * (h - 50)
    xs = x + 2 / 4 * w
    s.append(f"<line x1='{x}' y1='{yu:.0f}' x2='{x + w}' y2='{yu:.0f}' stroke='{RJ}' stroke-width='2.5' stroke-dasharray='8 6'/>")
    s.append(f"<line x1='{xs:.0f}' y1='{y}' x2='{xs:.0f}' y2='{y + h}' stroke='{NAV}' stroke-width='2'/>")
    s.append(tx(xs, y + h + 18, "Sn = 2 mm", 16, 800, NAV) + tx(x, y + h + 18, "0", 15, 700, "#475467") + tx(x + w, y + h + 18, "4 mm", 15, 700, "#475467"))
    s.append(tx(x + w - 8, yu - 14, "umbral", 15, 800, RJ, "end"))
    s.append(f"<rect x='{x}' y='{y}' width='{xs - x:.0f}' height='{h}' fill='{hexa(RJ, .10)}'/>")
    s.append(tx(x + (xs - x) / 2, y + 26, "DETECTA", 17, 900, RJ) + tx(xs + 60, y + 26, "no detecta", 15, 700, "#475467", "start"))
    s.append(tx(x + w / 2, y + h + 44, "distancia del metal a la cara (forma ilustrativa)", 15, 800, NAV))
    s.append(f"<text x='{x - 16}' y='{y + h / 2}' font-family='Montserrat' font-size='15' font-weight='800' fill='{NAV}' text-anchor='middle' "
             f"transform='rotate(-90 {x - 16} {y + h / 2})'>amplitud</text>")
    return "".join(s)


f = Img("se3", 20, 610, w=500)
P["H20_sensor_funcionamiento"] = page(DID,
    kick("SENSOR INDUCTIVO · CÓMO FUNCIONA", C4) + T("Así detecta el", "metal", C4, sub="Un oscilador que se «frena» cuando llega una pieza metálica", size=62)
    + "".join(blk(20 + i * 210, 300, 196, t, d, c, h=150) for i, (t, d, c) in enumerate(blocks))
    + svg(0, 0, 1080, 1350, "".join(flecha(216 + i * 210, 375, 230 + i * 210, 375, NAV, 4) for i in range(4)))
    + f.html() + cajas(f, [(1, (.70, .30, .92, .67), "Cara activa", "campo ≈ 2 mm", 40, 1000)], wl=250)
    + svg(0, 0, 1080, 1350, _amp())
    + "<div style='position:absolute;left:40px;right:40px;top:480px;font:500 19px/1.4 Montserrat;color:#1d2939;background:#F6FAFF;border-radius:16px;padding:14px 20px'>"
      "Sin metal, el oscilador trabaja a <b>amplitud máxima</b>. Al acercarse el metal, las corrientes de Foucault le quitan energía y la amplitud cae; "
      "cuando pasa el <b>umbral</b>, el comparador activa la salida PNP y enciende el LED rojo. La histéresis (máx. 10 % de Sn) evita parpadeos.</div>"
    + tabla(1080, [("Metal presente", "BK ≈ +V − 1,5 V · LED ON"), ("Sin metal", "BK abierto · LED OFF")], extra="font-size:20px;left:560px"),
    F_SE + " · Omron, guía técnica de sensores de proximidad", LS.format(37750))

# ---- H21 criterios
P["H21_sensor_criterios"] = page(DID,
    kick("SENSOR INDUCTIVO · SELECCIÓN", C4) + T("Cómo escoger el", "sensor inductivo", C4, sub="PR12-2DP: lo que significa cada letra y número", size=58)
    + "<div style='position:absolute;left:40px;right:40px;top:280px;display:flex;justify-content:center;gap:8px;font:900 64px/1 \"Barlow C\"'>"
    + "".join(f"<div style='text-align:center'><div style='background:{c};color:#fff;padding:8px 18px;border-radius:12px'>{t}</div>"
              f"<div style='font:700 15px/1.2 Montserrat;color:#475467;margin-top:6px;width:150px'>{d}</div></div>" for t, d, c in (
                  ("P", "proximidad", NAV), ("R", "cilíndrico", NAV), ("12", "rosca M12", AZ), ("-2", "Sn = 2 mm", TEAL), ("D", "DC 3 hilos", NAR), ("P", "salida PNP", RJ)))
    + "</div>"
    + crit(440, [("Material y tamaño de la pieza", "2 mm con hierro de 12 × 12 × 1 mm; otros metales se detectan más cerca.", "hierro", NAV),
                 ("Distancia de trabajo", "Instálalo entre 0 y 1,4 mm de la pieza para que detecte siempre.", "0–1,4 mm", TEAL),
                 ("Montaje", "Enrasado: puede ir embutido en metal. El no enrasado (PR12-4) ve 4 mm pero necesita espacio libre.", "enrasado", AZ),
                 ("PNP o NPN", "PNP entrega +V en BK → entrada de PLC tipo sumidero (común a 0 V).", "PNP", RJ),
                 ("Alimentación y carga", "12–24 VDC (10–30 VDC); salida máx. 200 mA; caída máx. 1,5 V.", "200 mA", NAR),
                 ("Velocidad", "Frecuencia de respuesta máx. 1,5 kHz.", "1,5 kHz", VER)])
    + chips(900, [("PNP · fuente", "BK entrega +V a la carga; la carga regresa a 0 V (BU).", RJ),
                  ("NPN · sumidero", "BK conecta la carga a 0 V; la carga va a +V (BN).", AZ)], cols=2)
    + nota(1040, "Un sensor <b>PNP en una entrada para NPN</b> no funciona: revisa el común del PLC antes de comprar."),
    F_SE + " · IEC 60947-5-2", LS.format(37750))

# ---- H22 aplicación
f = Img("se4", 40, 300, w=440)


def _engr():
    cx, cy, R, r = 770, 570, 140, 110
    s, pp = [], []
    n = 12
    for i in range(n * 4):
        a = 2 * math.pi * i / (n * 4)
        rr = R if (i % 4) in (1, 2) else r
        pp.append(f"{cx + rr * math.cos(a):.0f},{cy + rr * math.sin(a):.0f}")
    s.append(f"<polygon points='{' '.join(pp)}' fill='#98A2B3' stroke='#475467' stroke-width='3'/>"
             f"<circle cx='{cx}' cy='{cy}' r='34' fill='#fff' stroke='#475467' stroke-width='3'/>")
    s.append(f"<rect x='{cx - 30}' y='{cy - R - 108}' width='60' height='88' rx='8' fill='#C9CED6' stroke='#475467' stroke-width='3'/>"
             f"<rect x='{cx - 30}' y='{cy - R - 28}' width='60' height='14' fill='#E8602C'/>")
    s.append(tx(cx + 50, cy - R - 76, "PR12-2DP", 18, 800, NAV, "start") + tx(cx + 50, cy - R - 50, "≤ 1,4 mm del diente", 16, 700, RJ, "start"))
    s.append(tx(cx, cy + R + 28, "engranaje de 12 dientes", 16, 800, NAV))
    return "".join(s)


P["H22_sensor_aplicacion"] = page(DID,
    kick("SENSOR INDUCTIVO · CASO REAL", C4) + T("Vigilar la velocidad de", "un eje", C4, sub="El sensor cuenta dientes y el PLC calcula las rpm", size=56)
    + ph(20, 280, 480, 440) + f.html(False) + svg(0, 0, 1080, 1350, _engr())
    + "<div style='position:absolute;left:40px;right:40px;top:760px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px'>"
    + "".join(f"<div style='border-radius:14px;padding:10px 14px;background:{bg};color:#fff;font:600 17px/1.3 Montserrat'>"
              f"<b style='display:block;font:900 32px/1 \"Barlow C\"'>{t}</b>{d}</div>" for t, d, bg in (
                  ("BN → L+", "24 VDC de la fuente", "#7B4A2A"), ("BU → M", "0 V de la fuente", "#1D4ED8"), ("BK → I0.0", "entrada del PLC (sumidero)", "#111")))
    + "</div>"
    + "<div style='position:absolute;left:40px;right:40px;top:890px;border-radius:18px;background:#F6FAFF;padding:16px 22px;font:500 21px/1.4 Montserrat;color:#1d2939'>"
      "<b style='font:900 34px \"Barlow C\";color:#0FA3A3'>f = dientes × rpm ÷ 60</b><br>"
      "A 3000 rpm con 12 dientes: 12 × 3000 ÷ 60 = <b>600 pulsos por segundo</b> → menor que 1,5 kHz ✓. "
      "Si la frecuencia cae (correa rota o eje trabado), el PLC detiene el motor y da alarma.</div>"
    + nota(1150, "La entrada del PLC también debe ser rápida: una entrada normal filtra pulsos; para 600 Hz usa un <b>contador rápido</b>."),
    F_SE, LS.format(37750))

# ---- H23 versus
f = Img("se2", 70, 280, w=420)
P["H23_sensor_versus"] = page(DID,
    kick("SENSOR INDUCTIVO · COMPARACIÓN", C4) + T("PR12-2DP contra", "Omron E2B", C4, sub="Autonics vs Omron E2B-M12KS02-WP-B1 · M12 · 2 mm · PNP NA", size=58)
    + ph(40, 280, 460, 420) + f.html(False) + cap(40, 710, 460, "Autonics PR12-2DP")
    + rival(580, 280, 460, 420, "OMRON", "Serie E2B · M12 enrasado", "E2B-M12KS02", "-WP-B1 · PNP NA, 2 mm, cable 2 m")
    + vsbadge(540, 490)
    + versus(750, "PR12-2DP", "E2B-M12KS02-WP-B1", [
        ("Distancia Sn", "2 mm", "2 mm"), ("Montaje", "enrasado", "enrasado"), ("Salida", "PNP NA", "PNP NA"),
        ("Alimentación", "10–30 VDC", "10–30 VDC"), ("Frecuencia", "1,5 kHz", "1,5 kHz"), ("Carga máx.", "200 mA", "200 mA"),
        ("Caída residual", "1,5 V", "2 V"), ("LED", "rojo", "amarillo")], dif=(6, 7))
    + nota(1180, "Se reemplazan uno por otro <b>sin cambiar el cableado</b>: misma rosca, mismos colores BN/BU/BK y misma salida."),
    F_SE + " · Omron, especificaciones E2B (ia.omron.com, RS)", LS.format(37750))

# ---- H24 símbolo
s = Img("14_sensor_inductivo_simbolo", 40, 300, w=470)
f = Img("se2", 540, 270, w=500)
f1 = Img("se1", 560, 760, w=460)
P["H24_sensor_simbolo"] = page(DID,
    kick("SENSOR INDUCTIVO · SÍMBOLO IEC 60617", C4) + T("Símbolo del", "sensor inductivo", C4, sub="Detector de proximidad de 3 hilos con salida NA", size=58)
    + ph(30, 280, 490, 380) + s.html(False)
    + letras(s, [("A", (.28, .25, .58, .68), AZ), ("B", (.40, .03, .62, .25), "#7B4A2A", "tr"), ("C", (.40, .68, .62, .96), "#1D4ED8", "br"),
                 ("D", (.58, .30, .80, .96), "#111", "tr")])
    + f.html() + letras(f, [("A", (.55, .62, .74, .84), AZ, "br"), ("E", (.16, .29, .67, .72), TEAL, "tl")])
    + f1.html() + letras(f1, [("B", (.62, .26, .93, .48), "#111", "tr")])
    + leyenda(700, [("A", "Rombo + cuadro lleno", "= detector inductivo → cara activa", AZ), ("B", "BN +", "→ café, al +24 V", "#7B4A2A"),
                    ("C", "BU −", "→ azul, al 0 V", "#1D4ED8"), ("D", "BK salida NA", "→ negro, a la entrada", "#111"),
                    ("E", "Recuadro", "= el cuerpo del sensor", TEAL)], cols=1, x=30, w=490)
    + nota(1170, "Las puntas B-C-D salen en el mismo cable; los colores los fija la <b>IEC 60947-5-2</b> para todas las marcas."),
    "IEC 60617 · IEC 60947-5-2 · IEC 81346 (-B) · " + F_SE, LS.format(37750) + " · símbolo: catálogo @miguelesquit")

# =====================================================================================================================
# CONTACTOR NOARK Ex9C50 50 A 220 VAC
# =====================================================================================================================
C5 = VER
f = Img("km1", 170, 280, w=700)
P["H25_contactor_partes"] = page(DID,
    kick("CONTACTOR · NOARK Ex9C50", C5) + T("Las partes del", "contactor", C5, sub="50 A AC-3 · bobina 220 VAC · 1NA + 1NC", size=62)
    + f.html() + cajas(f, [
        (1, (.42, .04, .62, .17), "Bobina A1 · A2", "220 VAC · arriba al centro", 20, 330),
        (2, (.30, .20, .69, .32), "Entrada 1/L1 3/L2 5/L3", "de la protección", 20, 480),
        (3, (.31, .34, .69, .79), "Tapa transparente", "protege el frente", 20, 660),
        (4, (.30, .78, .69, .92), "Salida 2/T1 4/T2 6/T3", "al relé térmico/motor", 20, 860),
        (5, (.64, .05, .74, .16), "Oreja de fijación", "tornillo o riel DIN", 780, 330),
        (6, (.45, .51, .57, .61), "Portacontactos", "verde: se mueve al cerrar", 780, 560),
        (7, (.69, .29, .78, .76), "Auxiliares", "13-14 NA · 21-22 NC", 780, 720)], wl=280)
    + chips(985, [("50 A AC-3", "Motores: 15 kW a 230 V · 22 kW a 400 V.", C5), ("80 A AC-1", "Cargas resistivas (Ith).", AZ),
                  ("1NA + 1NC", "Autoenclavamiento y enclavamiento.", NAR)])
    + nota(1125, "Arriba entra la red, abajo sale al motor; la <b>bobina</b> va arriba al centro y los auxiliares al costado."),
    F_KM, LS.format(4060))

# ---- H26 funcionamiento
f = Img("km1", 0, 270, w=520)
P["H26_contactor_funcionamiento"] = page(DID,
    kick("CONTACTOR · CÓMO FUNCIONA", C5) + T("Así cierra un", "contactor", C5, sub="Un electroimán que mueve todos los contactos a la vez", size=62)
    + f.html() + marcas(f, [(1, (.42, .04, .62, .17), "", "", 0, 0), (2, (.45, .51, .57, .61), "", "", 0, 0), (3, (.30, .20, .69, .32), "", "", 0, 0),
                           (4, (.69, .29, .78, .76), "", "", 0, 0)])
    + "<div style='position:absolute;left:540px;right:40px;top:270px;display:grid;gap:10px'>"
    + "".join(f"<div style='display:flex;gap:12px;align-items:center;border-radius:14px;background:#F6FAFF;padding:8px 12px;font:500 16px/1.28 Montserrat;color:#1d2939'>"
              f"<div style='flex:none;width:38px;height:38px;border-radius:50%;background:{c};color:#fff;font:800 19px/38px Montserrat;text-align:center'>{n}</div>"
              f"<div><b style='color:#0B1F4D'>{t}</b> {d}</div></div>" for n, t, d, c in (
                  (1, "Bobina A1-A2:", "con 220 VAC el núcleo en E se magnetiza.", CL[0]),
                  (2, "Armadura:", "es atraída y arrastra el portacontactos verde.", CL[1]),
                  (3, "Polos 1-2, 3-4, 5-6:", "cierran y el motor recibe tensión.", CL[2]),
                  (4, "Auxiliares:", "13-14 cierra y 21-22 abre, junto con los polos.", CL[3]),
                  (5, "Sin tensión:", "un resorte regresa todo a reposo.", RJ)))
    + "</div>"
    + tabla(830, [("Cierra (0,85–1,1 Uc)", "187 – 242 V"), ("Abre (0,20–0,75 Uc)", "44 – 165 V"), ("Espira de sombra", "evita vibración en AC")],
            cab="<span>BOBINA 220 VAC</span>", extra="font-size:20px")
    + nota(1075, "Por eso un contactor de 220 V <b>no cierra</b> con 120 V, y si la tensión baja mucho puede soltar: protege al motor de arrancar solo al volver la energía si usas autoenclavamiento."),
    F_KM, LS.format(4060))

# ---- H27 criterios
f = Img("km5c", 70, 290, w=400)
P["H27_contactor_criterios"] = page(DID,
    kick("CONTACTOR · SELECCIÓN", C5) + T("Cómo escoger el", "contactor", C5, sub="La placa lateral del Ex9C50 trae los datos clave", size=62)
    + ph(20, 280, 520, 540) + f.html(False)
    + letras(f, [("A", (.0, .04, .88, .15), AZ, "tr"), ("B", (.0, .15, .92, .31), RJ, "tr"), ("C", (.0, .40, .92, .55), VER, "tr"),
                 ("D", (.0, .67, .92, .84), NAR, "br")])
    + leyenda(840, [("A", "Ui 1000 V · Uimp 8 kV", "Ith (AC-1) 80 A", AZ), ("B", "AC-3", "50 A · 15 kW a 230 V", RJ),
                    ("C", "HP a 208 V", "15 hp trifásico", VER), ("D", "Cable y par", "2,5–25 mm² · 6 N·m", NAR)], cols=2, x=30, w=490)
    + crit(285, [("Categoría AC-3", "Motor jaula: corriente del motor ≤ corriente AC-3.", "50 A", C5),
                 ("Potencia a tu tensión", "Placa: 15 hp a 208 V, 20 hp a 240 V (trifásico).", "15 hp", AZ),
                 ("Tensión de bobina", "220 VAC: cierra de 187 a 242 V. A 120 V no sirve.", "220 V", RJ),
                 ("Auxiliares", "13-14 para autoenclavamiento · 21-22 para enclavamiento.", "1NA+1NC", NAR),
                 ("Cargas resistivas", "Hornos y resistencias: AC-1 hasta 80 A.", "80 A", NAV),
                 ("Cable", "Bornes de 14 a 4 AWG; apriete 6 N·m.", "4 AWG", MOR)], x=560, w=480)
    + nota(990, "No escojas solo por los amperios del <b>modelo</b>: compara con la corriente del motor en <b>AC-3</b> a la tensión de tu red."),
    F_KM, LS.format(4060))

# ---- H28 aplicación
fk = Img("km1", 300, 420, w=310)
P["H28_contactor_aplicacion"] = page(DID,
    kick("CONTACTOR · CASO REAL", C5) + T("Motor de 15 hp a", "208 V", C5, sub="Arranque directo con autoenclavamiento", size=60)
    + blk(320, 280, 270, "PROTECCIÓN", "breaker o fusibles (NEC 430.52)", NAV)
    + fk.html()
    + "<div style='position:absolute;left:220px;top:560px;font:900 34px \"Barlow C\";color:#22A559'>-KM1</div>"
    + blk(320, 760, 270, "RELÉ TÉRMICO", "ajustado a la placa del motor", NAV)
    + blk(320, 900, 270, "MOTOR 15 hp", "208 V · 3~", C5)
    + svg(0, 0, 1080, 1350, flecha(455, 365, 455, 425) + flecha(455, 720, 455, 760) + flecha(455, 845, 455, 900))
    + "<div style='position:absolute;left:640px;right:40px;top:280px;display:grid;gap:12px'>"
    + "".join(f"<div style='border-radius:16px;background:#F6FAFF;border-left:10px solid {c};padding:10px 16px;font:500 17px/1.3 Montserrat;color:#1d2939'>"
              f"<b style='display:block;font:900 30px/1.05 \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for t, d, c in (
                  ("46,2 A", "Corriente de tabla NEC 430.250, 15 hp a 208 V → menor que 50 A AC-3 ✓.", C5),
                  ("6 AWG", "Conductor al 125 %: 57,8 A → 6 AWG THHN (65 A a 75 °C).", AZ),
                  ("BOBINA ENTRE FASES", "220 V entre L1 y L2: 208 V está dentro de 187–242 V.", RJ),
                  ("13-14", "En paralelo con el pulsador de marcha: autoenclavamiento.", NAR),
                  ("5 kA", "La placa (UL) pide protección con fusibles para 5 kA a 600 V.", MOR)))
    + "</div>"
    + nota(1060, "El contactor <b>maniobra</b>; no protege. La sobrecarga la cuida el relé térmico y el cortocircuito el breaker o los fusibles."),
    F_KM + " · NEC 2020 T430.250, 430.22, T310.16", LS.format(4060))

# ---- H29 versus
f = Img("km1", 70, 280, w=420)
P["H29_contactor_versus"] = page(DID,
    kick("CONTACTOR · COMPARACIÓN", C5) + T("Ex9C50 contra", "LC1D50AM7", C5, sub="NOARK vs Schneider Electric TeSys Deca · 50 A · bobina 220 VAC", size=58)
    + ph(40, 280, 460, 420) + f.html(False) + cap(40, 710, 460, "NOARK Ex9C50")
    + rival(580, 280, 460, 420, "SCHNEIDER ELECTRIC", "TeSys Deca · LC1D", "LC1D50AM7", "Contactor 3P, 50 A AC-3, bobina 220 VAC, 1NA+1NC")
    + vsbadge(540, 490)
    + versus(750, "Ex9C50", "LC1D50AM7", [
        ("AC-3 (≤ 440 V)", "50 A", "50 A"), ("AC-1", "80 A", "80 A"), ("kW a 230 V", "15 kW", "15 kW"), ("kW a 400 V", "22 kW", "22 kW"),
        ("hp a 208 V (3~)", "15 hp", "15 hp"), ("Auxiliares", "1NA + 1NC", "1NA + 1NC"),
        ("Bobina abre a", "0,20–0,75 Uc", "0,3–0,6 Uc"), ("Vida mecánica", "10 millones", "6 millones")], dif=(6, 7))
    + nota(1180, "Mismos valores de maniobra; revisa el <b>montaje</b> (riel/tornillos) y la posición de los bornes de bobina al reemplazar."),
    F_KM + " · Schneider Electric, hoja de datos LC1D50AM7", LS.format(4060))

# ---- H30 símbolo
s = Img("05_contactor_simbolo", 30, 310, w=500)
f = Img("km1", 520, 270, w=560)
P["H30_contactor_simbolo"] = page(DID,
    kick("CONTACTOR · SÍMBOLO IEC 60617", C5) + T("Símbolo del", "contactor", C5, sub="Polos, auxiliares y bobina: cada uno en su lugar del equipo", size=60)
    + ph(20, 280, 520, 380) + s.html(False)
    + letras(s, [("A", (.14, .02, .30, .49), AZ), ("B", (.33, .02, .47, .49), RJ, "tr"), ("C", (.54, .02, .82, .49), NAR, "tr"),
                 ("D", (.28, .50, .50, .98), VER, "bl")])
    + f.html() + letras(f, [("A", (.30, .20, .69, .32), AZ), ("B", (.30, .78, .69, .92), RJ, "bl"), ("C", (.69, .30, .79, .76), NAR, "tr"),
                            ("D", (.42, .04, .62, .17), VER, "tr"), ("E", (.45, .51, .57, .61), TEAL, "tl")])
    + leyenda(700, [("A", "Polos 1-3-5", "→ bornes de entrada", AZ), ("B", "Polos 2-4-6", "→ bornes de salida", RJ),
                    ("C", "13-14 NA · 21-22 NC", "→ bloque del costado: 13 y 21 arriba, 14 y 22 abajo", NAR),
                    ("D", "Bobina A1-A2", "→ bornes arriba al centro", VER), ("E", "Línea punteada", "→ portacontactos verde", TEAL)], cols=1, x=30, w=490)
    
    + nota(1180, "El <b>semicírculo</b> en el contacto marca la función de contactor; la línea punteada une todo lo que mueve la bobina."),
    "IEC 60617 · IEC 81346 (-KM) · " + F_KM, LS.format(4060) + " · símbolo: catálogo @miguelesquit")

if __name__ == "__main__":
    sel = sys.argv[1:] or list(P)
    for k in sel:
        (AQ / "html" / f"{k}.html").write_text(P[k], encoding="utf-8")
    subprocess.run(["node", "shot.js", *sel], cwd=AQ, check=True)
    print("ok", len(sel))

"""Lote B (25-nov): 20 publicaciones DIDÁCTICAS de electricidad industrial, inspiradas en el orden y la claridad
de las referencias del usuario (esquemas de estado normal/activado, partes internas, simbología), dibujadas por
nosotros en SVG. Fondo blanco, título con marcador amarillo. Símbolos IEC desde lib/simsvg.py (congelados)."""
import importlib.util
import math
import subprocess
import sys
from pathlib import Path

AQ = Path(__file__).parent
RAIZ = AQ.parent.parent
sys.path.insert(0, str(RAIZ / "lib"))
import simsvg as S  # noqa: E402


def _load(n, p):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


p4 = _load("p4", AQ.parent / "posts4" / "gen.py")
p6 = _load("p6", AQ.parent / "posts6" / "gen.py")
page, CC = p6.page, p4.CC
NAV, AZ, TEAL, NAR, RJ, VER, AM, CU, GR = "#0B1F4D", "#0057FF", "#0FA3A3", "#FF8A00", "#E5383B", "#22A559", "#FFD400", "#E08A2E", "#8A94A6"

CSS = """body{background:#fff!important}
.kk{position:absolute;left:50px;top:40px;font:800 22px Montserrat;letter-spacing:3px;color:#fff;padding:6px 16px;border-radius:8px}
.tt{position:absolute;left:46px;right:40px;top:86px;font:900 66px/1.02 Montserrat;color:#0B1F4D;letter-spacing:-1.8px}
.tt em{font-style:normal;background:linear-gradient(transparent 56%,#FFD400 56%);padding:0 6px}
.pn{position:absolute;left:40px;right:40px;border-radius:26px;border:3px solid #CFE0F5;background:#F6FAFF}
.ch{position:absolute;font:800 22px Montserrat;color:#fff;border-radius:12px;padding:8px 16px;line-height:1.15;text-align:center}
.ch small{display:block;font-weight:500;font-size:17px}
.tx{position:absolute;left:50px;right:50px;font:500 24px/1.38 Montserrat;color:#1d2939}.tx b{font-weight:800;color:#0B1F4D}
.cd{position:absolute;border-radius:20px;padding:16px 20px;color:#fff;font:500 20px/1.3 Montserrat}.cd b{display:block;font:900 34px 'Barlow C'}
svg{position:absolute;overflow:visible}"""


def head(kick, col, t):
    return f"<div class='kk' style='background:{col}'>{kick}</div><div class='tt'>{t}</div>"


def svg(x, y, w, h, body, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return f"<svg style='left:{x}px;top:{y}px' width='{w}' height='{h}' viewBox='{vb}'>{body}</svg>"


def sim(t, x, y, w):
    s = t[0].replace('width="', 'data-w="').replace('height="', 'data-h="', 1)
    return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px'>{s.replace('<svg ', '<svg style=\"position:static;width:100%;height:auto\" ', 1)}</div>"


def L(x1, y1, x2, y2, c=NAV, w=4, dash=None, cap="round"):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{c}' stroke-width='{w}' stroke-linecap='{cap}'{d}/>"


def P(d, c=NAV, w=4, f="none", dash=None):
    dd = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<path d='{d}' stroke='{c}' stroke-width='{w}' fill='{f}' stroke-linejoin='round' stroke-linecap='round'{dd}/>"


def R(x, y, w, h, f="#fff", c=NAV, sw=3, r=6):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{f}' stroke='{c}' stroke-width='{sw}'/>"


def C(x, y, r, f="#fff", c=NAV, sw=3):
    return f"<circle cx='{x}' cy='{y}' r='{r}' fill='{f}' stroke='{c}' stroke-width='{sw}'/>"


def Tx(x, y, s, size=24, w=700, c=NAV, a="middle", fam="Montserrat"):
    return f"<text x='{x}' y='{y}' font-family='{fam}' font-size='{size}' font-weight='{w}' fill='{c}' text-anchor='{a}' dominant-baseline='central'>{s}</text>"


def borne(x, y, n, up=True):
    return C(x, y, 11, "#fff", NAV, 3) + Tx(x, y - 30 if up else y + 30, n, 24, 800)


def flecha(x1, y1, x2, y2, c=VER, w=6):
    a = math.atan2(y2 - y1, x2 - x1)
    h = [(x2 - 18 * math.cos(a - .45), y2 - 18 * math.sin(a - .45)), (x2 - 18 * math.cos(a + .45), y2 - 18 * math.sin(a + .45))]
    return L(x1, y1, x2, y2, c, w) + f"<polygon points='{x2},{y2} {h[0][0]:.0f},{h[0][1]:.0f} {h[1][0]:.0f},{h[1][1]:.0f}' fill='{c}'/>"


def chip(x, y, t, col, s=None, w=None):
    ww = f"width:{w}px;" if w else ""
    return f"<div class='ch' style='left:{x}px;top:{y}px;{ww}background:{col}'>{t}{f'<small>{s}</small>' if s else ''}</div>"


def contacto_h(x, y, cerrado, nc_tipo=True, c=NAV):
    """Contacto vertical didáctico (puente): fijo arriba y abajo, puente móvil."""
    s = L(x, y - 60, x, y - 14, c, 5) + L(x, y + 14, x, y + 60, c, 5)
    if cerrado:
        s += L(x - 18, y - 14, x + 18, y - 14, c, 5) + L(x - 18, y + 14, x + 18, y + 14, c, 5) + R(x - 22, y - 12, 44, 24, "#C9D3E3", c, 3, 4)
    else:
        s += L(x - 18, y - 14, x + 18, y - 14, c, 5) + L(x - 18, y + 14, x + 18, y + 14, c, 5) + R(x + 6, y - 40, 44, 24, "#C9D3E3", c, 3, 4)
    return s


P_ = {}


# ===================================================================== B01 relé térmico: normal vs sobrecarga
def bimetal_panel(ox, oy, activo):
    s = []
    for i, n in enumerate(("1", "3", "5")):
        x = ox + 90 + i * 120
        s.append(borne(x, oy + 40, n))
        col = "#FF6B1A" if activo else CU
        s.append(P(f"M{x},{oy + 52} C{x},{oy + 80} {x - 40},{oy + 90} {x},{oy + 110}", col, 5))
        if activo:
            s.append(P(f"M{x},{oy + 110} C{x},{oy + 180} {x + 6},{oy + 240} {x + 34},{oy + 280}", "#9AA3B5", 18))
        else:
            s.append(L(x, oy + 110, x, oy + 280, "#9AA3B5", 18, cap="butt"))
        for k in range(4):
            yy = oy + 130 + k * 36
            s.append(P(f"M{x - 16 + (k * 2 if activo else 0)},{yy} q16,-14 32,0", col, 5))
        s.append(P(f"M{x + (34 if activo else 0)},{oy + 280} L{x + (34 if activo else 0)},{oy + 330}", col, 5) + borne(x + (34 if activo else 0), oy + 342, str(int(n) + 1), False))
    rx = ox + 40 + (34 if activo else 0)
    s.append(R(rx, oy + 285, 360, 26, "#2F7DE1", "#1F5FB5", 2, 4))
    s.append(L(rx + 360, oy + 298, ox + 560, oy + 298, TEAL, 4))
    if activo:
        s.append(flecha(ox + 450, oy + 270, ox + 530, oy + 270, VER, 6))
    # contactos 95-96 (NC) y 97-98 (NA)
    for j, (a, b, nc) in enumerate((("95", "96", True), ("97", "98", False))):
        x = ox + 620 + j * 130
        cerr = (nc and not activo) or (not nc and activo)
        s.append(borne(x, oy + 150, a) + borne(x, oy + 446 - 0, b, False))
        s.append(L(x, oy + 161, x, oy + 268, NAV, 5) + L(x, oy + 328, x, oy + 435, NAV, 5))
        s.append(R(x - 30 + (0 if cerr else 26), oy + 284 + (0 if cerr else -40), 60, 28, "#FFD9A8" if not cerr else "#E6EAF2", NAV, 3, 4))
        s.append(L(x - 22, oy + 268, x + 22, oy + 268, NAV, 5) + L(x - 22, oy + 328, x + 22, oy + 328, NAV, 5))
        s.append(Tx(x, oy + 495, "NC" if nc else "NA", 22, 800, RJ if nc else VER))
    return "".join(s)


P_["B01_rele_termico_estados"] = (head("RELÉ TÉRMICO · CÓMO FUNCIONA", NAR, "¿Qué pasa dentro del<br>térmico en una <em>sobrecarga</em>?") +
    "<div class='pn' style='top:280px;height:450px'></div>" + chip(840, 296, "NORMAL", TEAL, "sin sobrecarga") +
    svg(40, 290, 1000, 430, bimetal_panel(40, 0, False), "0 -20 1000 520") +
    "<div class='pn' style='top:745px;height:450px;border-color:#F6C6C6;background:#FFF7F7'></div>" + chip(840, 761, "SOBRECARGA", RJ, "bimetal curvado") +
    svg(40, 755, 1000, 430, bimetal_panel(40, 0, True), "0 -20 1000 520") +
    "<div class='tx' style='top:1205px;font-size:20px;text-align:center'>El bimetal se curva por el calor, empuja la <b>regleta</b>: abre <b>95-96</b> y cierra <b>97-98</b>.</div>",
    "IEC 60947-4-1 · Schneider Electric, TeSys LRD (principio) · Siemens, manual SIRIUS 3RU2", "ilustración propia")

# ===================================================================== B02 relé térmico simbología
P_["B02_rele_termico_simbolo"] = (head("RELÉ TÉRMICO · SIMBOLOGÍA", NAR, "Cómo se dibuja el<br><em>relé térmico</em>") +
    "<div class='pn' style='top:290px;height:560px'></div>" + sim(S.termico("F3"), 70, 330, 940) +
    chip(80, 720, "POTENCIA", AZ, "1-2 · 3-4 · 5-6 en serie con el motor", 300) +
    chip(560, 720, "MANDO", RJ, "95-96 NC en serie con la bobina", 210) + chip(800, 720, "SEÑAL", VER, "97-98 NA para piloto de falla", 210) +
    "<div class='pn' style='top:880px;height:300px;background:#fff'></div>"
    "<div class='tx' style='top:905px'><b>Los dos símbolos son el mismo aparato.</b> La parte de potencia (escalón dentro del cuadro) va entre el contactor y el motor; "
    "la de mando abre <b>95-96</b> y apaga la bobina del contactor cuando hay sobrecarga. Se identifica con <b>-F</b>.</div>",
    "IEC 60617 (símbolos) · IEC 81346-2 (designación -F) · IEC 60947-4-1", "símbolos propios IEC")


# ===================================================================== B03 diferencial esquema interno
def rcd_interno():
    s = []
    xf, xn = 560, 700
    s.append(Tx(xf, 20, "F", 34, 900, "#8B4513") + Tx(xn, 20, "N", 34, 900, AZ))
    for x, c in ((xf, "#8B4513"), (xn, AZ)):
        s.append(L(x, 40, x, 120, c, 6) + L(x, 170, x, 760, c, 6))
        s.append(P(f"M{x},{120} L{x + 26},{165}", c, 6))
    s.append(L(xf + 12, 145, xn + 12, 145, GR, 3, "8 7") + L(xf - 60, 145, xf + 12, 145, GR, 3, "8 7"))
    s.append(f"<ellipse cx='630' cy='470' rx='170' ry='60' fill='none' stroke='#9AA3B5' stroke-width='28'/>")
    s.append(f"<ellipse cx='630' cy='470' rx='170' ry='60' fill='none' stroke='#5D6779' stroke-width='3'/>")
    for k in range(5):
        s.append(P(f"M{470 + k * 12},{440} q-20,30 0,60", RJ, 4))
    s.append(P("M470,445 C380,430 360,330 330,300", RJ, 4) + P("M500,500 C400,520 330,420 300,330", RJ, 4))
    s.append(R(250, 260, 90, 90, "#fff", NAV, 4) + L(262, 340, 328, 270, NAV, 4))
    s.append(L(295, 260, 295, 145, GR, 3, "8 7") + L(295, 145, xf - 60, 145, GR, 3, "8 7"))
    s.append(P(f"M{xn},{250} H860 V640 H{xf}", NAR, 4) + R(840, 330, 40, 20, AM, NAV, 3, 3) + P("M848,420 l8,-10 l8,20 l8,-20 l8,20 l8,-10", NAR, 4))
    s.append(L(820, 330, 900, 330, NAV, 4) + L(860, 300, 860, 330, NAV, 4))
    s.append(Tx(xf - 100, 700, "Carga", 26, 800) + R(xf - 40, 760, 220, 50, "#C9D3E3", NAV, 3) + Tx(630, 785, "CARGA", 24, 800))
    return "".join(s)


P_["B03_diferencial_interno"] = (head("DIFERENCIAL · CÓMO FUNCIONA", AZ, "Lo que hay dentro<br>de un <em>diferencial</em>") +
    "<div class='pn' style='top:280px;height:870px;background:#fff'></div>" + svg(0, 300, 1080, 840, rcd_interno()) +
    chip(70, 330, "Contactos", NAV, "F y N, abren juntos") + chip(70, 520, "Relé de disparo", RJ, "electroimán") +
    chip(70, 760, "Toroide + bobina", "#5D6779", "de detección") + chip(860, 600, "Prueba T", NAR, "con resistencia") +
    chip(720, 360, "IF = IN → Φ = 0", TEAL) +
    "<div class='tx' style='top:1160px;font-size:21px'>Si hay fuga a tierra, <b>IF ≠ IN</b>: el toroide induce corriente en su bobina y el relé abre los contactos. "
    "El botón <b>T</b> desvía corriente por fuera del toroide para simular la fuga.</div>",
    "IEC 61008-1 · Schneider Electric, guía de protección diferencial · ABB, manual de baja tensión", "ilustración propia")


# ===================================================================== B04 diferencial simbología 2P y 4P
def rcd_sim(n, x0, labels):
    s, dx = [], 90
    xs = [x0 + i * dx for i in range(n)]
    for x, (a, b) in zip(xs, labels):
        s.append(L(x, 40, x, 120) + L(x, 120, x - 28, 190) + L(x, 200, x, 330))
        s.append(P(f"M{x - 10},{110} l20,20 m0,-20 l-20,20", NAV, 3))
        s.append(Tx(x - 24, 70, a, 24, 800) + Tx(x - 24, 310, b, 24, 800))
    s.append(f"<ellipse cx='{(xs[0] + xs[-1]) / 2}' cy='262' rx='{(xs[-1] - xs[0]) / 2 + 40}' ry='22' fill='none' stroke='{NAV}' stroke-width='4'/>")
    s.append(L(xs[0] - 14, 155, xs[-1] + 20, 155, GR, 3, "8 7"))
    s.append(L(xs[0] - 14, 155, xs[0] - 90, 155, GR, 3, "8 7") + R(xs[0] - 160, 120, 70, 70, "#fff", NAV, 4) + Tx(xs[0] - 125, 155, "IΔ", 26, 800))
    s.append(L(xs[0] - 125, 190, xs[0] - 125, 262, GR, 3, "8 7") + L(xs[0] - 125, 262, xs[0] - (xs[-1] - xs[0]) / 2 - 40 + (xs[0] + xs[-1]) / 2 - xs[0], 262, GR, 3, "8 7"))
    s.append(Tx(xs[0] - 125, 92, "-F1", 26, 800))
    return "".join(s)


P_["B04_diferencial_simbolo"] = (head("DIFERENCIAL · SIMBOLOGÍA", AZ, "Cómo se dibuja el<br><em>diferencial</em>") +
    "<div class='pn' style='top:280px;height:470px;left:40px;right:560px'></div>" + chip(60, 296, "2 POLOS", AZ, "monofásico") +
    svg(60, 360, 460, 380, rcd_sim(2, 240, [("1", "2"), ("N", "N")])) +
    "<div class='pn' style='top:280px;height:470px;left:540px'></div>" + chip(560, 296, "4 POLOS", NAV, "trifásico + neutro") +
    svg(560, 360, 480, 380, rcd_sim(4, 190, [("1", "2"), ("3", "4"), ("5", "6"), ("N", "N")])) +
    "<div class='pn' style='top:780px;height:400px;background:#fff'></div>" +
    "".join(chip(70 + i * 330, 805, t, c, s, 290) for i, (t, c, s) in enumerate([("Óvalo", "#5D6779", "el toroide abraza TODOS los conductores"), ("IΔ", RJ, "relé que dispara por corriente diferencial"), ("Línea punteada", GR, "une el disparo con todos los polos")])) +
    "<div class='tx' style='top:960px'>El <b>neutro pasa por el toroide</b> igual que las fases. Si el neutro no pasa, el diferencial ve una “fuga” falsa y dispara siempre. "
    "Se identifica con <b>-F</b> (IEC 81346-2).</div>",
    "IEC 60617 (símbolos) · IEC 61008-1 · IEC 81346-2", "símbolos propios IEC")


# ===================================================================== B05 contactor partes internas (esquema)
def contactor_esq(activo=False, campo=False):
    s = []
    dxa = -30 if activo else 0
    s.append(P("M60,90 H220 V130 H100 V250 H220 V290 H60 Z", "#5D6779", 3, "#C9D3E3"))     # culata en E (fija)
    s.append(R(108, 140, 70, 100, "#F7B733", "#B7791F", 3) + Tx(143, 190, "", 20))
    for k in range(6):
        s.append(L(112, 150 + k * 16, 174, 150 + k * 16, "#B7791F", 2))
    s.append(P("M30,150 C60,150 80,170 108,170", "#8B4513", 4) + P("M30,215 C60,215 80,210 108,210", AZ, 4))
    s.append(C(30, 150, 11) + Tx(30, 122, "A1", 22, 800) + C(30, 215, 11) + Tx(30, 245, "A2", 22, 800))
    ax = 260 + dxa
    s.append(R(ax, 80, 34, 220, "#C9D3E3", "#5D6779", 3, 3))                                                         # armadura (martillo)
    s.append(P(f"M{ax + 34},100 l12,-8 l12,16 l12,-16 l12,16 l12,-16 l12,8", "#5D6779", 3) + P(f"M{ax + 34},280 l12,-8 l12,16 l12,-16 l12,16 l12,-16 l12,8", "#5D6779", 3))
    if campo:
        for r in (30, 52, 74):
            s.append(f"<ellipse cx='160' cy='190' rx='{110 + r}' ry='{90 + r * .6}' fill='none' stroke='#FF8A00' stroke-width='3' opacity='.75'/>")
    s.append(L(ax + 34, 190, 1000, 190, GR, 4, "12 9"))
    for i, (a, b) in enumerate((("1/L1", "2/T1"), ("3/L2", "4/T2"), ("5/L3", "6/T3"))):
        x = 460 + i * 120
        s.append(contacto_h(x, 190, activo) + Tx(x, 100, a, 22, 800) + Tx(x, 282, b, 22, 800))
    for i, (a, b, nc) in enumerate((("13", "14", False), ("21", "22", True))):
        x = 840 + i * 110
        s.append(contacto_h(x, 190, activo != nc) + Tx(x, 100, a, 22, 800) + Tx(x, 282, b, 22, 800) + Tx(x, 320, "NC" if nc else "NA", 20, 800, RJ if nc else VER))
    return "".join(s)


P_["B05_contactor_partes"] = (head("CONTACTOR · PARTES INTERNAS", TEAL, "Las partes internas<br>de un <em>contactor</em>") +
    "<div class='pn' style='top:280px;height:520px'></div>" + svg(40, 380, 1000, 340, contactor_esq()) +
    "".join(chip(x, y, t, c, s) for x, y, t, c, s in [
        (70, 300, "Bobina", "#B7791F", "A1-A2"), (250, 300, "Martillo", "#5D6779", "armadura móvil"), (70, 720, "Culata", "#5D6779", "núcleo fijo en E"),
        (300, 720, "Resortes", GR, "abren al quitar tensión"), (520, 300, "Principales", AZ, "potencia al motor"), (820, 300, "Auxiliares", VER, "mando y señal")]) +
    "<div class='pn' style='top:830px;height:340px;background:#fff'></div>"
    "<div class='tx' style='top:860px'>La <b>línea punteada</b> es la unión mecánica: el martillo arrastra a la vez los contactos <b>principales</b> y los <b>auxiliares</b>. "
    "Los principales son más robustos porque llevan la corriente del motor; los auxiliares solo la del mando.</div>",
    "IEC 60947-4-1 · Schneider Electric, guía TeSys D · Siemens, manual SIRIUS 3RT2", "ilustración propia")

# ===================================================================== B06 contactor estados
P_["B06_contactor_estados"] = (head("CONTACTOR · CÓMO FUNCIONA", TEAL, "Contactor en <em>reposo</em><br>y <em>energizado</em>") +
    "<div class='pn' style='top:280px;height:430px'></div>" + chip(60, 296, "REPOSO", TEAL, "bobina sin tensión") + svg(40, 380, 1000, 340, contactor_esq()) +
    "<div class='pn' style='top:730px;height:430px;border-color:#FFD9A8;background:#FFF9F1'></div>" + chip(60, 746, "ENERGIZADO", NAR, "bobina con tensión") +
    svg(40, 830, 1000, 340, contactor_esq(True, True)) +
    "<div class='tx' style='top:1170px;font-size:20px;text-align:center'>Con tensión en A1-A2: principales y <b>13-14</b> cierran, <b>21-22</b> abre. Sin tensión, los resortes lo regresan.</div>",
    "IEC 60947-4-1 · Schneider Electric, guía TeSys D · Siemens, manual SIRIUS 3RT2", "ilustración propia")

# ===================================================================== B07 categorías de empleo
cats = [("AC-1", VER, "Cargas no inductivas o poco inductivas", "hornos de resistencias, calefacción"),
        ("AC-2", AZ, "Motores de anillos rozantes", "arranque y desconexión"),
        ("AC-3", NAR, "Motores de jaula de ardilla", "arranque y desconexión con el motor en marcha"),
        ("AC-4", RJ, "Motores de jaula: servicio duro", "frenado a contracorriente, marcha a impulsos")]
P_["B07_contactor_categorias"] = (head("CONTACTOR · CATEGORÍAS", TEAL, "¿Qué significa <em>AC-3</em><br>en un contactor?") +
    "<div style='position:absolute;left:640px;top:280px;width:400px;height:420px;border-radius:26px;overflow:hidden;border:3px solid #CFE0F5'>"
    "<img src='../../posts3/fotos/p10_iek.jpg' style='width:100%;height:100%;object-fit:cover'></div>" +
    "<div class='tx' style='top:300px;width:560px'>La <b>categoría de empleo</b> dice para qué carga está probado el contactor. La misma pieza tiene una corriente distinta en cada categoría.</div>"
    "<div class='tx' style='top:520px;width:560px;font-size:21px;color:#475467'>Ejemplo real: un contactor modular de 24 A en AC-1 solo da 9 A en AC-3.</div>" +
    "".join(f"<div class='cd' style='left:40px;right:40px;top:{730 + i * 112}px;height:100px;background:{c};display:flex;align-items:center;gap:24px'>"
            f"<b style='width:130px'>{a}</b><div><div style='font-weight:800;font-size:24px'>{t}</div>{s}</div></div>" for i, (a, c, t, s) in enumerate(cats)),
    "IEC 60947-4-1, categorías de empleo · ABB, ficha ESB24-40 · Schneider Electric, catálogo TeSys", f"“Contactor DIN IEK”, Kae, CC BY-SA 3.0, {CC}")

# ===================================================================== B08 numeración de bornes
P_["B08_contactor_numeracion"] = (head("CONTACTOR · BORNES", TEAL, "Cómo se <em>numeran</em> los<br>bornes del contactor") +
    "<div class='pn' style='top:280px;height:460px'></div>" + sim(S.contactor("KM1"), 90, 300, 900) +
    "".join(f"<div class='cd' style='left:{40 + (i % 2) * 510}px;top:{770 + (i // 2) * 150}px;width:490px;height:135px;background:{c}'><b>{a}</b>{s}</div>"
            for i, (a, c, s) in enumerate([("1/L1 → 2/T1", AZ, "principales: impar entra, par sale"), ("A1 · A2", "#B7791F", "bobina"),
                                           ("…1 – …2", RJ, "unidad 1-2: contacto NC (21-22)"), ("…3 – …4", VER, "unidad 3-4: contacto NA (13-14)")])) +
    "<div class='tx' style='top:1080px;font-size:21px'>La <b>decena</b> es el número de orden (1.º, 2.º…); la <b>unidad</b> dice la función. 5-6 y 7-8 se usan en contactos especiales (temporizados, del térmico).</div>",
    "IEC 60947-1, anexo L (marcado de bornes) · EN 50012 · IEC 60617", "símbolos propios IEC")


# ===================================================================== B09 sensor inductivo por dentro
def sensor_corte(cap=False):
    s = []
    s.append(R(360, 90, 300, 640, "#E6EAF2", "#8A94A6", 4, 18))
    for k in range(26):
        s.append(L(360, 130 + k * 22, 352, 140 + k * 22, "#8A94A6", 3) + L(660, 130 + k * 22, 668, 140 + k * 22, "#8A94A6", 3))
    s.append(R(330, 300, 360, 40, "#C9D3E3", "#8A94A6", 3, 4) + R(330, 350, 360, 40, "#C9D3E3", "#8A94A6", 3, 4))
    s.append(R(380, 60, 260, 60, "#2F7DE1" if not cap else NAR, NAV, 3, 10))
    if cap:
        s.append(R(420, 70, 70, 30, "#22A559", NAV, 2, 4) + R(530, 70, 70, 30, "#1E7B44", NAV, 2, 4))
    else:
        s.append(R(430, 70, 160, 46, "#4A4F59", NAV, 2, 6) + R(452, 78, 116, 30, CU, "#8B5A1F", 2, 4))
    for r in (40, 70, 100):
        s.append(f"<path d='M{510 - r * 1.6},60 A{r * 1.6},{r} 0 0 1 {510 + r * 1.6},60' fill='none' stroke='{'#FF8A00' if not cap else '#22A559'}' stroke-width='3' opacity='.8'/>")
    s.append(R(395, 420, 70, 230, "#7FD6D6", NAV, 2, 6) + R(480, 420, 70, 230, "#F2E86D", NAV, 2, 6) + R(565, 420, 60, 230, "#B9C8F5", NAV, 2, 6))
    s.append(C(600, 745, 16, RJ, NAV, 2))
    s.append(R(495, 730, 30, 90, "#222", "#222", 2, 4))
    for i, c in enumerate(("#8B4513", "#111", AZ)):
        s.append(P(f"M{502 + i * 8},820 q{(i - 1) * 20},40 {(i - 1) * 30},70", c, 5))
    return "".join(s)


P_["B09_sensor_inductivo"] = (head("SENSORES · INDUCTIVO", NAR, "Así funciona un<br>sensor <em>inductivo</em>") +
    "<div class='pn' style='top:270px;height:900px;background:#fff'></div>" + svg(0, 280, 1080, 900, sensor_corte()) +
    "".join(chip(x, y, t, c, s, 270) for x, y, t, c, s in [
        (60, 300, "Campo magnético", NAR, "alterno, frente a la cara"), (60, 450, "Bobina + ferrita", CU, "en la cara activa"),
        (60, 700, "Oscilador", TEAL, "genera el campo"), (760, 700, "Evaluador + salida", AZ, "PNP o NPN"),
        (760, 960, "LED", RJ, "indica conmutación"), (60, 960, "Cable 3 hilos", NAV, "BN +  BK salida  BU −")]) +
    "<div class='tx' style='top:1180px;font-size:20px'>El metal cercano absorbe energía por <b>corrientes de Foucault</b>, la oscilación cae y la salida conmuta. Solo detecta <b>metales</b>.</div>",
    "IEC 60947-5-2 (detectores de proximidad) · Pepperl+Fuchs, sensores inductivos · Omron, guía técnica de sensores de proximidad", "ilustración propia")

# ===================================================================== B10 sensor capacitivo
P_["B10_sensor_capacitivo"] = (head("SENSORES · CAPACITIVO", VER, "Así funciona un<br>sensor <em>capacitivo</em>") +
    "<div class='pn' style='top:270px;height:900px;background:#fff'></div>" + svg(0, 280, 1080, 900, sensor_corte(True)) +
    "".join(chip(x, y, t, c, s, 270) for x, y, t, c, s in [
        (60, 300, "Campo eléctrico", VER, "frente a la cara"), (60, 450, "Electrodos", "#1E7B44", "activo y de compensación"),
        (60, 700, "Oscilador", TEAL, "RC"), (760, 700, "Ajuste de sensibilidad", AZ, "potenciómetro"),
        (760, 960, "LED", RJ, "indica conmutación"), (60, 960, "Cable 3 hilos", NAV, "BN +  BK salida  BU −")]) +
    "<div class='tx' style='top:1180px;font-size:20px'>Detecta <b>metales y no metales</b> (agua, grano, plástico) porque cambian la capacidad del campo. Ideal para niveles en tolvas y tanques.</div>",
    "IEC 60947-5-2 · Pepperl+Fuchs, sensores capacitivos · Omron, guía técnica de sensores de proximidad", "ilustración propia")


# ===================================================================== B11 fotoeléctricos 3 tipos
def foto_tipo(y, tipo):
    s = [R(40, y, 120, 90, "#2F3540", NAV, 3, 10) + C(150, y + 45, 14, RJ, NAV, 2)]
    if tipo == "barrera":
        s.append(L(165, y + 45, 760, y + 45, "#FF4D4D", 10) + R(770, y, 120, 90, "#2F3540", NAV, 3, 10) + C(780, y + 45, 14, "#333", NAV, 2))
        s.append(Tx(100, y + 120, "Emisor", 20, 700) + Tx(830, y + 120, "Receptor", 20, 700))
    elif tipo == "reflex":
        s.append(L(165, y + 35, 820, y + 35, "#FF4D4D", 8) + L(820, y + 55, 165, y + 55, "#FF9999", 8) + R(830, y + 5, 40, 80, "#B0B7C3", NAV, 3, 4))
        s.append(Tx(100, y + 120, "Emisor-receptor", 20, 700) + Tx(850, y + 120, "Reflector", 20, 700))
    else:
        s.append(L(165, y + 35, 560, y + 35, "#FF4D4D", 8) + L(560, y + 55, 165, y + 55, "#FF9999", 8) + R(570, y - 5, 110, 100, "#F2B544", NAV, 3, 8))
        s.append(Tx(100, y + 120, "Emisor-receptor", 20, 700) + Tx(625, y + 120, "Objeto", 20, 700))
    return "".join(s)


P_["B11_fotoelectricos"] = (head("SENSORES · FOTOELÉCTRICOS", AZ, "Los 3 tipos de sensor<br><em>fotoeléctrico</em>") +
    "".join(f"<div class='pn' style='top:{290 + i * 290}px;height:270px'></div>" + chip(60, 304 + i * 290, t, c, s) + svg(60, 380 + i * 290, 960, 160, foto_tipo(0, k))
            for i, (k, t, c, s) in enumerate([("barrera", "BARRERA", AZ, "mayor alcance"), ("reflex", "RÉFLEX", TEAL, "con reflector"), ("difuso", "DIFUSO", NAR, "el objeto refleja")])) +
    "<div class='tx' style='top:1170px;font-size:20px'>Barrera: el objeto <b>corta</b> el haz. Réflex: corta el haz que regresa del reflector. Difuso: el <b>objeto mismo</b> devuelve la luz.</div>",
    "IEC 60947-5-2 · Omron, E3Z (guía de selección) · SICK, sensores fotoeléctricos", "ilustración propia")


# ===================================================================== B12 PNP vs NPN
def pnp_npn(pnp):
    s = [R(40, 60, 200, 220, "#fff", NAV, 4, 10), P("M140,110 L180,170 L140,230 L100,170 Z", NAV, 3)]
    s.append(L(240, 90, 360, 90, "#8B4513", 6) + L(240, 170, 300, 170, "#111", 6) + L(240, 250, 360, 250, AZ, 6))
    s.append(Tx(270, 70, "BN", 20, 800, "#8B4513") + Tx(270, 150, "BK", 20, 800) + Tx(270, 230, "BU", 20, 800, AZ))
    s.append(Tx(372, 90, "+24 V", 22, 800, RJ, "start") + Tx(372, 250, "0 V", 22, 800, AZ, "start"))
    if pnp:
        s.append(L(300, 170, 300, 190) + R(270, 190, 60, 40, "#F2E86D", NAV, 3, 4) + L(300, 230, 300, 250, NAV, 4) + C(300, 250, 6, NAV, NAV, 1))
        s.append(flecha(320, 150, 320, 182, RJ, 4))
    else:
        s.append(L(300, 170, 300, 150) + R(270, 110, 60, 40, "#F2E86D", NAV, 3, 4) + L(300, 110, 300, 90, NAV, 4) + C(300, 90, 6, NAV, NAV, 1))
        s.append(flecha(320, 120, 320, 160, AZ, 4))
    s.append(Tx(360, 210 if pnp else 130, "carga", 20, 700, NAV, "start"))
    return "".join(s)


P_["B12_pnp_npn"] = (head("SENSORES · CONEXIÓN", AZ, "<em>PNP</em> o <em>NPN</em>:<br>cómo se conecta la carga") +
    "<div class='pn' style='top:280px;height:520px;right:560px'></div>" + chip(60, 296, "PNP", RJ, "entrega +24 V") + svg(60, 380, 460, 320, pnp_npn(True)) +
    "<div class='pn' style='top:280px;height:520px;left:540px'></div>" + chip(560, 296, "NPN", AZ, "entrega 0 V") + svg(560, 380, 460, 320, pnp_npn(False)) +
    "<div class='tx' style='top:720px;left:60px;right:560px;font-size:21px'>Carga entre <b>BK y BU</b>.</div>"
    "<div class='tx' style='top:720px;left:560px;font-size:21px'>Carga entre <b>BK y BN</b>.</div>"
    "<div class='pn' style='top:830px;height:330px;background:#fff'></div>"
    "<div class='tx' style='top:860px'>En un <b>PLC</b>: con sensor <b>PNP</b> el común de las entradas va a <b>0 V</b>; con sensor <b>NPN</b> va a <b>+24 V</b>. "
    "Si el sensor no coincide con la entrada, el LED del sensor enciende pero el PLC <b>no ve la señal</b>.</div>",
    "IEC 60947-5-2 · IEC 61131-2 (entradas digitales) · Siemens, S7-1200 manual (entradas sink/source)", "ilustración propia")

# ===================================================================== B13 colores y pines M12
m12 = (C(200, 200, 150, "#2F3540", NAV, 4) + C(200, 200, 112, "#4A4F59", "#222", 3) + R(188, 40, 24, 30, "#2F3540", "#2F3540", 0, 3) +
       "".join(C(200 + 70 * math.cos(a), 200 + 70 * math.sin(a), 18, "#E0B04A", "#8B6A1F", 3) + Tx(200 + 70 * math.cos(a), 200 + 70 * math.sin(a), n, 20, 900, NAV)
               for n, a in (("1", -math.pi / 4), ("2", -3 * math.pi / 4), ("3", 3 * math.pi / 4), ("4", math.pi / 4))) + C(200, 200, 10, "#E0B04A", "#8B6A1F", 3))
hilos = [("BN", "#8B4513", "#fff", "1", "+ alimentación"), ("WH", "#F5F5F5", NAV, "2", "2.ª salida (4 hilos)"), ("BU", AZ, "#fff", "3", "− alimentación (0 V)"), ("BK", "#111", "#fff", "4", "salida (NA en 3 hilos)")]
P_["B13_colores_sensor"] = (head("SENSORES · CABLEADO", NAV, "Qué significa cada<br><em>color</em> del sensor") +
    "<div class='pn' style='top:280px;height:450px;right:560px'></div>" + svg(80, 300, 400, 400, m12) +
    "<div class='tx' style='top:690px;left:60px;right:560px;text-align:center;font-size:19px'>Conector M12 macho, vista de frente</div>" +
    "".join(f"<div class='cd' style='left:560px;right:40px;top:{280 + i * 113}px;height:100px;background:{bg};color:{fg};border:3px solid #CFE0F5;display:flex;align-items:center;gap:20px'>"
            f"<b style='width:70px'>{a}</b><div><div style='font-weight:800;font-size:22px'>Pin {p}</div>{t}</div></div>" for i, (a, bg, fg, p, t) in enumerate(hilos)) +
    "<div class='pn' style='top:760px;height:400px;background:#fff'></div>"
    "<div class='tx' style='top:790px'>Es el código de <b>IEC 60947-5-2</b> para sensores de 3 y 4 hilos: <b>marrón +, azul −, negro salida</b>. "
    "En el diagrama se escribe <b>BN, BU, BK, WH</b>. Revisa siempre la hoja del sensor: algunos de 2 hilos o de tipo NAMUR usan otro esquema.</div>",
    "IEC 60947-5-2 · IEC 61076-2-101 (conector M12) · Pepperl+Fuchs y SICK, hojas de datos", "ilustración propia")


# ===================================================================== B14 curvas B C D (gráfico)
def curvas():
    s, x0, y0, W, H = [], 120, 40, 820, 560
    s.append(L(x0, y0, x0, y0 + H, NAV, 4) + L(x0, y0 + H, x0 + W, y0 + H, NAV, 4))
    lx = lambda m: x0 + W * math.log10(m) / math.log10(30)
    for m in (1, 2, 3, 5, 10, 20, 30):
        s.append(L(lx(m), y0 + H, lx(m), y0 + H + 10, NAV, 3) + Tx(lx(m), y0 + H + 34, f"{m}", 22, 700))
    s.append(Tx(x0 + W / 2, y0 + H + 75, "múltiplos de In", 22, 700))
    s.append(Tx(60, y0 + H / 2, "tiempo", 22, 700))
    for a, b, c, t in ((3, 5, AZ, "B"), (5, 10, VER, "C"), (10, 20, RJ, "D")):
        s.append(f"<rect x='{lx(a):.0f}' y='{y0 + H - 130}' width='{lx(b) - lx(a):.0f}' height='120' fill='{c}' opacity='.22'/>")
        s.append(P(f"M{lx(1.13):.0f},{y0 + 20} C{lx(1.6):.0f},{y0 + 260} {lx(a) - 30:.0f},{y0 + H - 200} {lx(a):.0f},{y0 + H - 130} L{lx(b):.0f},{y0 + H - 10}", c, 6))
        s.append(Tx((lx(a) + lx(b)) / 2, y0 + H - 160, t, 44, 900, c, fam="Barlow C"))
    s.append(Tx(lx(1.6) + 30, y0 + 120, "zona térmica (bimetal)", 22, 700, NAV, "start"))
    s.append(Tx(lx(4), y0 + H - 250, "zona magnética", 22, 700, NAV, "start"))
    return "".join(s)


P_["B14_curvas_bcd"] = (head("TERMOMAGNÉTICO · CURVAS", RJ, "Curvas <em>B, C y D</em>:<br>¿cuándo dispara?") +
    "<div class='pn' style='top:270px;height:720px;background:#fff'></div>" + svg(40, 290, 1000, 700, curvas()) +
    "".join(f"<div class='cd' style='left:{40 + i * 340}px;top:1010px;width:320px;height:150px;background:{c}'><b>{a}</b>{t}</div>"
            for i, (a, c, t) in enumerate([("B · 3–5 In", AZ, "resistivas, cables largos"), ("C · 5–10 In", VER, "uso general"), ("D · 10–20 In", RJ, "motores, transformadores")])) +
    "<div class='tx' style='top:1170px;font-size:19px;text-align:center'>Todas: <b>1,13 In</b> no dispara en 1 h · <b>1,45 In</b> dispara en menos de 1 h (In ≤ 63 A).</div>",
    "IEC 60898-1 · ABB, What you need to know about MCB trip curves · Siemens, MCB primer", "gráfico esquemático propio")

# ===================================================================== B15 guardamotor símbolo + foto
P_["B15_guardamotor_simbolo"] = (head("GUARDAMOTOR · SIMBOLOGÍA", NAV, "El <em>guardamotor</em>:<br>dos protecciones en uno") +
    "<div style='position:absolute;left:40px;top:280px;width:420px;height:620px;border-radius:26px;overflow:hidden;border:3px solid #CFE0F5'>"
    "<img src='../../posts3/fotos/p09_mpcb.jpg' style='width:100%;height:100%;object-fit:cover'></div>" +
    "<div class='pn' style='top:280px;height:620px;left:490px'></div>" + sim(S.guardamotor("QM1"), 510, 330, 510) +
    chip(510, 760, "Escalón", NAR, "térmico: sobrecarga (ajustable)", 240) + chip(770, 760, "I&gt;", RJ, "magnético: cortocircuito", 240) +
    "<div class='pn' style='top:930px;height:240px;background:#fff'></div>"
    "<div class='tx' style='top:955px'>Une un <b>interruptor</b> con disparo <b>térmico</b> y <b>magnético</b>. Se ajusta a la corriente de placa del motor y además sirve para <b>seccionar</b> (ON/OFF). Se identifica con <b>-QM</b>.</div>",
    "IEC 60947-2 · IEC 60947-4-1 · Siemens, ficha 3RV2011-0HA10", f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0, {CC}")


# ===================================================================== B16 clases de disparo (gráfico)
def clases():
    s, x0, y0, W, H = [], 120, 40, 820, 520
    s.append(L(x0, y0, x0, y0 + H, NAV, 4) + L(x0, y0 + H, x0 + W, y0 + H, NAV, 4))
    lx = lambda m: x0 + W * (m - 1) / 7.5
    ly = lambda t: y0 + H - H * math.log10(t) / math.log10(200)
    for m in (1, 2, 4, 6, 7.2, 8):
        s.append(L(lx(m), y0 + H, lx(m), y0 + H + 10, NAV, 3) + Tx(lx(m), y0 + H + 34, f"{m}".replace(".", ","), 22, 800 if m == 7.2 else 600, RJ if m == 7.2 else NAV))
    for t in (1, 10, 100):
        s.append(Tx(x0 - 30, ly(t), f"{t} s", 20, 700))
    s.append(L(lx(7.2), y0, lx(7.2), y0 + H, RJ, 3, "10 8"))
    for c, tmax, col in ((10, 10, AZ), (20, 20, VER), (30, 30, NAR)):
        s.append(P(f"M{lx(1.25):.0f},{y0} C{lx(2):.0f},{max(y0, ly(tmax * 9)):.0f} {lx(5):.0f},{ly(tmax * 1.6):.0f} {lx(7.2):.0f},{ly(tmax):.0f} L{lx(8.4):.0f},{ly(tmax * .78):.0f}", col, 6))
        s.append(Tx(lx(8.4) + 10, ly(tmax * .78), f"Clase {c}", 24, 900, col, "start", "Barlow C"))
    s.append(Tx(x0 + W / 2, y0 + H + 75, "múltiplos de Ir (corriente ajustada)", 22, 700))
    return "".join(s)


P_["B16_clases_disparo"] = (head("RELÉ TÉRMICO · CLASES", NAR, "Clase <em>10, 20 y 30</em>:<br>¿qué tan rápido dispara?") +
    "<div class='pn' style='top:270px;height:700px;background:#fff'></div>" + svg(40, 290, 1000, 680, clases()) +
    "".join(f"<div class='cd' style='left:{40 + i * 340}px;top:990px;width:320px;height:150px;background:{c}'><b>Clase {a}</b>a 7,2 Ir: {t}</div>"
            for i, (a, c, t) in enumerate([("10", AZ, "de 4 a 10 s · arranque normal"), ("20", VER, "de 6 a 20 s · arranque pesado"), ("30", NAR, "de 9 a 30 s · muy pesado")])) +
    "<div class='tx' style='top:1150px;font-size:19px;text-align:center'>Además: <b>1,05 Ir</b> no dispara en 2 h · <b>1,2 Ir</b> dispara en menos de 2 h.</div>",
    "IEC 60947-4-1 (límites de funcionamiento y clases) · Schneider Electric, Trip class designation · Siemens, SIRIUS 3RU2/3RV2", "gráfico esquemático propio")


# ===================================================================== B17 final de carrera secuencia
def fc(paso):
    s = [R(40, 160, 280, 170, "#E6EAF2", NAV, 3, 12)]
    ang = {1: -20, 2: 12, 3: -20}[paso]
    px, py = 90, 160
    ex, ey = px + 230 * math.cos(math.radians(ang)), py + 230 * math.sin(math.radians(ang))
    s.append(L(px, py, ex, ey, "#5D6779", 12) + C(ex, ey, 24, RJ, "#8B1E1E", 3) + C(px, py, 12, "#5D6779", NAV, 2))
    s.append(R(150, 120 if paso != 2 else 140, 34, 50, RJ, "#8B1E1E", 2, 3))
    cerr_na = paso == 2
    s.append(Tx(110, 365, "13-14", 20, 800, VER if cerr_na else GR) + Tx(250, 365, "21-22", 20, 800, RJ if not cerr_na else GR))
    s.append(Tx(110, 395, "cerrado" if cerr_na else "abierto", 18, 600) + Tx(250, 395, "abierto" if cerr_na else "cerrado", 18, 600))
    s.append(R(10, 40 if paso != 2 else 60, 170, 50, "#2F7DE1", NAV, 3, 10) + L(180, 65 if paso != 2 else 85, 280 if paso == 2 else 200, 65 if paso != 2 else 85, "#9AA3B5", 10))
    if paso == 2:
        s.append(flecha(190, 30, 270, 30, AZ, 5))
    if paso == 3:
        s.append(flecha(270, 30, 190, 30, AZ, 5))
    return "".join(s)


P_["B17_final_de_carrera"] = (head("MANDO · FINAL DE CARRERA", VER, "Cómo trabaja un<br><em>final de carrera</em>") +
    "".join(f"<div class='pn' style='top:280px;height:470px;left:{40 + i * 340}px;right:auto;width:320px'></div>" + chip(60 + i * 340, 296, f"PASO {i + 1}", c, s) +
            svg(40 + i * 340, 330, 330, 420, fc(i + 1)) for i, (c, s) in enumerate([(TEAL, "reposo"), (NAR, "el actuador lo empuja"), (AZ, "el resorte lo regresa")])) +
    "<div class='pn' style='top:780px;height:390px;background:#fff'></div>"
    "<div class='tx' style='top:805px'>Detecta la <b>posición</b> de una pieza por contacto físico. Al empujar la palanca, el NA <b>13-14</b> cierra y el NC <b>21-22</b> abre; al soltarla, el resorte lo regresa. "
    "Para seguridad se usa el NC con <b>apertura positiva</b> (⊖): se abre a la fuerza aunque los contactos estén soldados.</div>",
    "IEC 60947-5-1 (interruptores de posición) · IEC 60204-1 · Schneider Electric, XC Standard", "ilustración propia")

# ===================================================================== B18 colores de pulsadores
puls = [("MARCHA", "#F4F4F4", NAV, "blanco (preferido), gris, negro o verde", "nunca rojo"), ("PARO", "#1B1B1B", "#fff", "negro (preferido), gris o blanco", "rojo permitido; nunca verde"),
        ("EMERGENCIA", RJ, "#fff", "rojo sobre fondo amarillo", "hongo, enclavamiento"), ("REARME", AZ, "#fff", "azul, blanco, gris o negro", "reset")]
P_["B18_colores_pulsadores"] = (head("MANDO · PULSADORES", RJ, "¿De qué color va<br>cada <em>pulsador</em>?") +
    "".join(f"<div class='pn' style='top:{280 + i * 215}px;height:195px'></div>"
            f"<div style='position:absolute;left:80px;top:{305 + i * 215}px;width:145px;height:145px;border-radius:50%;background:{"#FFD400" if t == "EMERGENCIA" else "#2B2F36"};display:flex;align-items:center;justify-content:center'>"
            f"<div style='width:{120 if t == "EMERGENCIA" else 100}px;height:{120 if t == "EMERGENCIA" else 100}px;border-radius:50%;background:{bg};box-shadow:inset 0 -8px 0 rgba(0,0,0,.25);border:3px solid #111'></div></div>"
            f"<div class='tx' style='top:{318 + i * 215}px;left:270px'><b style='font:900 44px \"Barlow C\"'>{t}</b><br>{d}<br><span style='color:{RJ};font-weight:700'>{n}</span></div>"
            for i, (t, bg, fg, d, n) in enumerate(puls)) +
    "<div class='tx' style='top:1150px;font-size:19px'>Verde para marcha y rojo para paro <b>también cumplen</b>; lo prohibido es rojo en marcha y verde en paro.</div>",
    "IEC 60204-1:2016 (10.2.1) · Schneider Electric, FAQ FA28043 · IEC 60073", "ilustración propia")

# ===================================================================== B19 colores de pilotos
pil = [("ROJO", RJ, "Emergencia", "condición peligrosa: actuar ya"), ("AMARILLO", AM, "Anormal", "condición crítica inminente"),
       ("AZUL", AZ, "Obligatorio", "el operador debe actuar"), ("VERDE", VER, "Normal", "funcionamiento correcto"), ("BLANCO", "#F4F4F4", "Neutro", "información general")]
P_["B19_colores_pilotos"] = (head("MANDO · PILOTOS", AM, "¿Qué dice el <em>color</em><br>de cada piloto?") +
    "".join(f"<div class='pn' style='top:{280 + i * 172}px;height:155px'></div>"
            f"<div style='position:absolute;left:80px;top:{292 + i * 172}px;width:130px;height:130px;border-radius:50%;background:#2B2F36;display:flex;align-items:center;justify-content:center'>"
            f"<div style='width:96px;height:96px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0%,{c} 45%,{c} 100%);box-shadow:0 0 30px {c}'></div></div>"
            f"<div class='tx' style='top:{308 + i * 172}px;left:260px'><b style='font:900 42px \"Barlow C\"'>{t} · {s}</b><br>{d}</div>"
            for i, (t, c, s, d) in enumerate(pil)) +
    "<div class='tx' style='top:1150px;font-size:19px'>Ejemplo: motor en marcha = verde · disparo del térmico = amarillo · paro de emergencia activado = rojo.</div>",
    "IEC 60204-1:2016 (10.3.2) · IEC 60073 · Schneider Electric, Harmony XB4", "ilustración propia")


# ===================================================================== B20 relé 8 pines
def zocalo():
    s = [C(220, 220, 190, "#2F3540", NAV, 4) + C(220, 220, 58, "#1B1F24", "#111", 3) + R(208, 150, 24, 30, "#4A4F59", "#4A4F59", 0, 3)]
    fun = {"1": TEAL, "3": VER, "4": RJ, "2": "#B7791F", "7": "#B7791F", "8": TEAL, "6": VER, "5": RJ}
    for i in range(8):
        a = math.radians(-90 - 22.5 - i * 45)
        x, y = 220 + 125 * math.cos(a), 220 + 125 * math.sin(a)
        n = str(i + 1)
        s.append(C(x, y, 26, fun[n], "#fff", 3) + Tx(x, y, n, 26, 900, "#fff"))
    return "".join(s)


P_["B20_rele_8_pines"] = (head("MANDO · RELÉ DE 8 PINES", TEAL, "Los pines del<br><em>relé de 8 pines</em>") +
    "<div class='pn' style='top:280px;height:500px;right:560px'></div>" + svg(60, 300, 440, 440, zocalo()) +
    "<div class='tx' style='top:745px;left:60px;right:560px;text-align:center;font-size:18px'>Base octal vista desde abajo</div>" +
    "<div class='pn' style='top:280px;height:500px;left:540px'></div>" + sim(S.rele8("KA1"), 560, 380, 460) +
    "".join(f"<div class='cd' style='left:{40 + (i % 2) * 510}px;top:{810 + (i // 2) * 125}px;width:490px;height:110px;background:{c}'><b>{a}</b>{t}</div>"
            for i, (a, c, t) in enumerate([("2 – 7", "#B7791F", "bobina"), ("1 · 8", TEAL, "comunes"), ("1-3 · 8-6", VER, "NA (cierran al energizar)"), ("1-4 · 8-5", RJ, "NC (abren al energizar)")])) +
    "<div class='tx' style='top:1070px;font-size:19px'>Es la distribución más común (tipo Finder 60.12 / Omron MK2P). Confírmala siempre en el <b>diagrama impreso</b> del relé.</div>",
    "Finder, ficha serie 60 · Omron, MK-S · IEC 61810-1", "ilustración propia")

P = {k: page(CSS, v[0], v[1], v[2]) for k, v in P_.items()}

if __name__ == "__main__":
    import shutil
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    shutil.copytree(AQ.parent / "posts6" / "fonts", AQ / "fonts", dirs_exist_ok=True)
    ks = [k for k in P if not sys.argv[1:] or any(a in k for a in sys.argv[1:])]
    for k in ks:
        (AQ / "html" / f"{k}.html").write_text(P[k])
    (AQ / "shot.js").write_text(p4.JS)
    subprocess.run(["node", "shot.js", *ks], cwd=AQ, check=True)
    print(len(ks))

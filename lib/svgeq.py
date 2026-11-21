"""Equipos en SVG (alta calidad: degradados, sombras suaves, tornillos con relieve).
Estilo: equipos BLANCOS como la referencia del usuario (esquema 'circuito de potencia'); SOLO los PLC en gris.
Todas las coordenadas en mm reales. Cada función devuelve (svg, bornes) con bornes = {nombre: (x_mm, y_mm)} medido
desde la esquina superior izquierda del equipo, y (W, H) del equipo.
Se rasteriza con render_svg.py (Chromium) y se usa en Manim como imagen (equipo_img.py)."""
import math

LOGO_POLIS = [
    ([(0, 3), (114.5, 3), (170, 176), (224.5, 3), (224.5, 215), (199, 303.5), (141, 303.5), (103.5, 177), (103.5, 390.5), (0, 390.5)], "#91D4DF"),
    ([(245, 3), (345.5, 3), (345.5, 390.5), (245, 390.5)], "#0094B0"),
    ([(366, 3), (524.5, 3), (524.5, 88.5), (366, 88.5)], "#0094B0"),
    ([(366, 154), (481.5, 154), (481.5, 239.5), (366, 239.5)], "#0094B0"),
    ([(366, 305), (524.5, 305), (524.5, 390.5), (366, 390.5)], "#0094B0"),
    ([(562, 304), (639.5, 304), (639.5, 390.5), (562, 390.5)], "#0094B0"),
]
FUENTE = "Montserrat, Inter, Arial, sans-serif"
OSC = "#3D4350"        # franja oscura (bornes auxiliares)
AZUL = "#1F6FC5"       # línea azul de acento
TXT = "#1D2939"

DEFS = """
<defs>
 <linearGradient id="gBlanco" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBFCFD"/><stop offset="1" stop-color="#E6E9EE"/></linearGradient>
 <linearGradient id="gBlancoH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F7F8FA"/><stop offset="0.5" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9ECF0"/></linearGradient>
 <linearGradient id="gGrisCl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F1F3F6"/><stop offset="1" stop-color="#D9DDE3"/></linearGradient>
 <linearGradient id="gOsc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A5160"/><stop offset="1" stop-color="#363C48"/></linearGradient>
 <linearGradient id="gPLC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7C8797"/><stop offset="1" stop-color="#6A7585"/></linearGradient>
 <linearGradient id="gPLCcl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8994A4"/><stop offset="1" stop-color="#7A8595"/></linearGradient>
 <radialGradient id="gTorn" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.65" stop-color="#EEF2F5"/><stop offset="1" stop-color="#C6CED6"/></radialGradient>
 <radialGradient id="gTornAro" cx="0.5" cy="0.5" r="0.5"><stop offset="0.72" stop-color="#9FB0BE" stop-opacity="0"/><stop offset="0.86" stop-color="#9FB0BE" stop-opacity="0.55"/><stop offset="1" stop-color="#9FB0BE" stop-opacity="0"/></radialGradient>
 <radialGradient id="gRojo" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FF8A80"/><stop offset="0.55" stop-color="#E53935"/><stop offset="1" stop-color="#B71C1C"/></radialGradient>
 <radialGradient id="gVerde" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#8CF5A9"/><stop offset="0.55" stop-color="#22C55E"/><stop offset="1" stop-color="#15803D"/></radialGradient>
 <radialGradient id="gAmbar" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFE08A"/><stop offset="0.55" stop-color="#F5B500"/><stop offset="1" stop-color="#C98A00"/></radialGradient>
 <radialGradient id="gAzul" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#7FB8FF"/><stop offset="0.55" stop-color="#2E7BE0"/><stop offset="1" stop-color="#1A4FA0"/></radialGradient>
 <radialGradient id="gBlancoB" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#F1F3F6"/><stop offset="1" stop-color="#C9CFD7"/></radialGradient>
 <radialGradient id="gNegro" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#5A6270"/><stop offset="0.6" stop-color="#2A2F38"/><stop offset="1" stop-color="#15181D"/></radialGradient>
 <linearGradient id="gMetal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF1F4"/><stop offset="0.45" stop-color="#B9C2CC"/><stop offset="0.55" stop-color="#A9B3BE"/><stop offset="1" stop-color="#DDE2E8"/></linearGradient>
 <linearGradient id="gMotor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4F8DE0"/><stop offset="0.5" stop-color="#2F6FC4"/><stop offset="1" stop-color="#1F4F96"/></linearGradient>
 <filter id="fSombra" x="-10%" y="-10%" width="130%" height="130%"><feDropShadow dx="0.6" dy="0.9" stdDeviation="0.7" flood-color="#000" flood-opacity="0.28"/></filter>
 <filter id="fSuave" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0.2" dy="0.35" stdDeviation="0.35" flood-color="#000" flood-opacity="0.35"/></filter>
</defs>"""


def t(x, y, s, size, color=TXT, peso=700, ancla="middle", rot=0, ls=0):
    r = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FUENTE}" font-size="{size}" font-weight="{peso}" fill="{color}" text-anchor="{ancla}" dominant-baseline="central" letter-spacing="{ls}"{r}>{s}</text>'


def rect(x, y, w, h, fill, r=0, stroke=None, sw=0.25, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}"{st} {extra}/>'


def tornillo(x, y, r=3.4):
    """Tornillo de borne estilo referencia: disco blanco con relieve y cruz azul-pizarra gruesa."""
    c = "#2F4A5C"
    a = r * 0.62
    w = r * 0.36
    return (f'<g filter="url(#fSuave)"><circle cx="{x}" cy="{y}" r="{r * 1.25:.2f}" fill="url(#gTornAro)"/>'
            f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="url(#gTorn)" stroke="#AEB9C4" stroke-width="0.25"/></g>'
            f'<rect x="{x - a:.2f}" y="{y - w / 2:.2f}" width="{2 * a:.2f}" height="{w:.2f}" rx="{w / 2:.2f}" fill="{c}"/>'
            f'<rect x="{x - w / 2:.2f}" y="{y - a:.2f}" width="{w:.2f}" height="{2 * a:.2f}" rx="{w / 2:.2f}" fill="{c}"/>')


def tornillo_ranura(x, y, r=2.0, fondo="#1B1E23"):
    """Tornillo de PLC/bornera: cabeza gris con ranura diagonal (como el CPU 1212C de la referencia)."""
    return (f'<circle cx="{x}" cy="{y}" r="{r * 1.18:.2f}" fill="{fondo}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="url(#gMetal)" stroke="#5C6470" stroke-width="0.2"/>'
            f'<line x1="{x - r * 0.7:.2f}" y1="{y + r * 0.7:.2f}" x2="{x + r * 0.7:.2f}" y2="{y - r * 0.7:.2f}" stroke="#2A2F36" stroke-width="{r * 0.32:.2f}" stroke-linecap="round"/>')


def logo(x, y, h):
    s = h / 394
    pol = "".join(f'<polygon points="{" ".join(f"{px * s + x:.2f},{py * s + y:.2f}" for px, py in pts)}" fill="{c}"/>' for pts, c in LOGO_POLIS)
    return f"<g>{pol}</g>"


def franja_marca(x, y, w):
    """Franja de marca: logo del canal + línea azul (reemplaza la marca del fabricante)."""
    return logo(x, y - 1.4, 2.8) + rect(x + 6, y - 0.5, w - 6, 1.0, AZUL, 0.5)


def envolver(W, H, cuerpo, margen=3):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-margen} {-margen} {W + 2 * margen} {H + 2 * margen}" '
            f'width="{W + 2 * margen}mm" height="{H + 2 * margen}mm">{DEFS}{cuerpo}</svg>')


# ============================================================ DISYUNTOR MODULAR
def disyuntor(polos=1, In=6, curva="C", ref="F1", on=False):
    W, H = 18.0 * polos, 90.0
    b = {}
    s = [f'<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gBlanco)", 1.2, "#B8C0CA", 0.3), "</g>"]
    s.append(rect(0.4, 0.4, W - 0.8, 21, "url(#gGrisCl)", 0.8))
    s.append(rect(0.4, H - 21.4, W - 0.8, 21, "url(#gGrisCl)", 0.8))
    for i in range(1, polos):
        s.append(f'<line x1="{18 * i}" y1="0.5" x2="{18 * i}" y2="{H - 0.5}" stroke="#C3CAD3" stroke-width="0.35"/>')
    for i in range(polos):
        xc = 9 + 18 * i
        s.append(tornillo(xc, 10.5))
        s.append(tornillo(xc, H - 10.5))
        s.append(t(xc + 5.6, 4.0, str(2 * i + 1), 2.2, "#475467"))
        s.append(t(xc + 5.6, H - 4.0, str(2 * i + 2), 2.2, "#475467"))
        b[str(2 * i + 1)] = (xc, 10.5)
        b[str(2 * i + 2)] = (xc, H - 10.5)
    s.append(franja_marca(1.8, 25.2, W - 3.6))
    s.append(t(1.8, 31.5, f"{curva}{In}", 6.2 if polos > 1 else 5.0, "#4A5361", 800, "start"))
    s.append(t(1.8, 36.3, "230/400 V~", 1.5, "#667085", 600, "start"))
    # símbolo impreso por polo
    for i in range(polos):
        xs = W - 3.2 - (polos - 1 - i) * 3.2 if polos > 1 else W - 3.2
        s.append(f'<path d="M{xs},28 v2.2 M{xs - 0.9},31.2 l1.8,1.8 M{xs + 0.9},31.2 l-1.8,1.8 M{xs},34.4 l-1.3,-1.8 M{xs},34.4 v2.2" stroke="#475467" stroke-width="0.28" fill="none"/>')
    # palanca (accionamiento unido)
    s.append(rect(1.2, 41, W - 2.4, 3.2, "#2B2F36", 0.4))
    s.append(rect(1.2, 41.6, W - 2.4, 0.8, "#6B7380", 0.3))
    py = 45.5 if on else 49.5
    s.append(rect(2.2, 44.2, W - 4.4, 11.8, "#1F2329", 0.6))
    for i in range(polos):
        s.append(rect(18 * i + 3.0, py, 12.0, 5.6, "#2B2F36", 0.6, "#111", 0.2))
        s.append(rect(18 * i + 3.0, py + 0.8, 12.0, 0.9, "#6B7380", 0.3))
    s.append(rect(W / 2 - 4.5, 58.0, 9, 1.0, "#F2F4F7", 0.3) if False else "")
    s.append(t(W / 2, 61.8, f"-{ref}", 5.2 if polos > 1 else 4.2, TXT, 700))
    s.append(rect(1.8, 66.4, W - 3.6, 1.3, AZUL, 0.6))
    s.append(rect(W - 4.6, 38.0, 3.2, 1.6, "#D92D20" if on else "#12B76A", 0.3))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ CONTACTOR
def contactor(ref="KM1", bobina="240 V~", ie="32 A · AC-3"):
    W, H = 45.0, 85.0
    b = {}
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gBlanco)", 1.2, "#B8C0CA", 0.3), "</g>"]
    s.append(rect(0.5, 0.5, W - 1, 15.5, "url(#gGrisCl)", 0.8))
    s.append(rect(0.5, H - 16, W - 1, 15.5, "url(#gGrisCl)", 0.8))
    for x, n in zip((8.5, 22.5, 36.5), ("1/L1", "3/L2", "5/L3")):
        s.append(t(x, 3.4, n, 2.6, "#344054"))
        s.append(tornillo(x, 9.6, 3.6))
        b[n] = (x, 9.6)
    for x, n in zip((8.5, 22.5, 36.5), ("2/T1", "4/T2", "6/T3")):
        s.append(tornillo(x, H - 9.6, 3.6))
        s.append(t(x, H - 3.2, n, 2.6, "#344054"))
        b[n] = (x, H - 9.6)
    # franjas oscuras de auxiliares
    s.append(rect(0, 16.5, W, 14.5, "url(#gOsc)", 0))
    s.append(rect(0, H - 31, W, 14.5, "url(#gOsc)", 0))
    for x, n, et in zip((16.5, 28.5, 39.5), ("13", "21", "A1"), ("13 NO", "21 NC", "A1")):
        s.append(tornillo(x, 21.6, 3.0))
        s.append(t(x, 28.0, et, 2.3, "#FFFFFF", 700))
        b[n] = (x, 21.6)
    for x, n, et in zip((16.5, 28.5, 39.5), ("14", "22", "A2"), ("14 NO", "22 NC", "A2")):
        s.append(t(x, H - 28.0, et, 2.3, "#FFFFFF", 700))
        s.append(tornillo(x, H - 21.6, 3.0))
        b[n] = (x, H - 21.6)
    # frente central
    s.append(franja_marca(2.2, 34.2, W - 4.4))
    s.append(rect(3, 36.6, W - 6, 0.4, "#D5DAE0"))
    s.append(rect(13.5, 38.0, 18, 7.4, "#4A4F58", 0.4))
    for i, x in enumerate((14.3, 18.6, 22.9, 27.2)):
        s.append(rect(x, 38.7, 3.6, 6.0, "#6E7580" if i % 2 else "#5A606B", 0.2))
    s.append(f'<path d="M3,46.6 H13 V51.0 M32,51.0 V46.6 H42" stroke="#C9CFD7" stroke-width="0.35" fill="none"/>')
    s.append(t(W / 2, 49.6, f"-{ref}", 4.6, TXT, 700))
    s.append(rect(3, 52.2, W - 6, 1.0, AZUL, 0.5))
    s.append(t(4.0, 42.0, bobina, 1.6, "#667085", 700, "start"))
    s.append(t(W - 4.0, 42.0, ie, 1.6, "#667085", 700, "end"))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ RELÉ TÉRMICO (montaje directo)
def rele_termico(ref="F2", rango=(23, 32), ajuste=24.3):
    W, H = 45.0, 66.0
    b = {}
    s = []
    for x in (8.5, 22.5, 36.5):   # pines que entran al contactor
        s.append(rect(x - 1.2, -4.0, 2.4, 6.0, "#E08A1E", 0.4))
    s += ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gBlanco)", 1.2, "#B8C0CA", 0.3), "</g>"]
    s.append(franja_marca(2.0, 3.4, W - 4))
    # frente elevado
    s.append('<g filter="url(#fSuave)">' + rect(1.6, 6.2, W - 3.2, 21.5, "url(#gBlancoH)", 1.0, "#C3CAD3", 0.3) + "</g>")
    s.append(rect(3.0, 7.8, 19.5, 16.5, "#ECEFF3", 0.6, "#C9CFD7", 0.25))
    cx, cy, r = 11.5, 15.4, 6.0
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gAzul)" stroke="#164A8C" stroke-width="0.3"/>')
    a0, a1 = 210, -30
    for v in (rango[0], (rango[0] + rango[1]) / 2, rango[1]):
        ang = math.radians(a0 + (a1 - a0) * (v - rango[0]) / (rango[1] - rango[0]))
        s.append(t(cx + (r + 1.9) * math.cos(ang), cy - (r + 1.9) * math.sin(ang), f"{v:g}", 1.5, "#344054"))
        s.append(f'<line x1="{cx + (r - 1.2) * math.cos(ang):.2f}" y1="{cy - (r - 1.2) * math.sin(ang):.2f}" x2="{cx + (r - 0.2) * math.cos(ang):.2f}" y2="{cy - (r - 0.2) * math.sin(ang):.2f}" stroke="#FFFFFF" stroke-width="0.35"/>')
    ang = math.radians(a0 + (a1 - a0) * (ajuste - rango[0]) / (rango[1] - rango[0]))
    s.append(f'<g transform="rotate({-math.degrees(ang):.1f} {cx} {cy})"><rect x="{cx - 3.8}" y="{cy - 0.7}" width="7.6" height="1.4" rx="0.7" fill="#163E73"/>'
             f'<rect x="{cx - 0.7}" y="{cy - 3.8}" width="1.4" height="7.6" rx="0.7" fill="#163E73"/><polygon points="{cx + 4.6},{cy} {cx + 3.4},{cy - 0.9} {cx + 3.4},{cy + 0.9}" fill="#FFFFFF"/></g>')
    s.append(f'<polygon points="4.2,11.2 6.0,8.6 7.8,11.2" fill="#3D4350"/>')
    s.append(t(19.0, 22.6, "A", 1.8, "#344054"))
    s.append(rect(13.0, 22.0, 4.6, 1.5, "#3D4350", 0.3))
    s.append(t(17.6, 9.6, "TEST", 1.6, "#475467", 700))
    s.append(t(W - 3.5, 10.6, f"-{ref}", 4.4, TXT, 700, "end"))
    s.append(t(29.5, 14.6, "STOP", 1.7, "#475467", 700))
    s.append(t(38.5, 14.6, "RESET", 1.7, "#475467", 700))
    s.append(rect(24.5, 16.4, 19, 8.6, "#3D4350", 4.3))
    s.append(f'<circle cx="29.0" cy="20.7" r="3.3" fill="url(#gRojo)"/><circle cx="29.0" cy="20.7" r="1.5" fill="#FF7043"/>')
    s.append(f'<circle cx="39.0" cy="20.7" r="3.3" fill="url(#gAzul)"/>' + t(37.8, 20.7, "M", 1.6, "#FFFFFF") + t(40.2, 20.7, "A", 1.6, "#FFFFFF"))
    s.append(t(W - 3.5, 26.0, "CLASS 10", 1.4, "#667085", 700, "end"))
    # fila de auxiliares 98 NO 97 · 96 NC 95
    for x, n in zip((6.5, 16.5, 28.5, 38.5), ("98", "97", "96", "95")):
        s.append(t(x, 31.4, n, 2.6, "#344054"))
        s.append(tornillo(x, 37.0, 3.0))
        b[n] = (x, 37.0)
    s.append(t(11.5, 32.6, "NO", 2.0, "#475467"))
    s.append(t(33.5, 32.6, "NC", 2.0, "#475467"))
    s.append(rect(0.5, 42.2, W - 1, 23.3, "url(#gGrisCl)", 0.8))
    for x, n in zip((8.5, 22.5, 36.5), ("2/T1", "4/T2", "6/T3")):
        s.append(tornillo(x, 51.5, 3.6))
        s.append(t(x, 60.6, n, 2.6, "#344054"))
        b[n] = (x, 51.5)
    return envolver(W, H, "".join(s), 5), b, (W, H)


# ============================================================ GUARDAMOTOR
def guardamotor(ref="QM1", rango=(22, 32), ajuste=24.3, on=False):
    W, H = 45.0, 97.0
    b = {}
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gBlanco)", 1.2, "#B8C0CA", 0.3), "</g>"]
    s.append(rect(0.5, 0.5, W - 1, 17, "url(#gGrisCl)", 0.8))
    s.append(rect(0.5, H - 17.5, W - 1, 17, "url(#gGrisCl)", 0.8))
    for x, n in zip((8.5, 22.5, 36.5), ("1/L1", "3/L2", "5/L3")):
        s.append(t(x, 3.4, n, 2.5, "#344054"))
        s.append(tornillo(x, 10.0, 3.6))
        b[n] = (x, 10.0)
    for x, n in zip((8.5, 22.5, 36.5), ("2/T1", "4/T2", "6/T3")):
        s.append(tornillo(x, H - 10.0, 3.6))
        s.append(t(x, H - 3.4, n, 2.5, "#344054"))
        b[n] = (x, H - 10.0)
    s.append(franja_marca(2.2, 21.0, W - 4.4))
    s.append('<g filter="url(#fSuave)">' + rect(2, 24, W - 4, 52, "url(#gBlancoH)", 1.2, "#C3CAD3", 0.3) + "</g>")
    cx, cy, r = 11.5, 33.0, 5.2
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 1.2}" fill="#E4E8ED" stroke="#B8C0CA" stroke-width="0.3"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gBlancoB)" stroke="#8A94A0" stroke-width="0.3"/>')
    a0, a1 = 225, -45
    for v in (rango[0], (rango[0] + rango[1]) / 2, rango[1]):
        ang = math.radians(a0 + (a1 - a0) * (v - rango[0]) / (rango[1] - rango[0]))
        s.append(t(cx + (r + 3.0) * math.cos(ang), cy - (r + 3.0) * math.sin(ang), f"{v:g}", 1.6, "#344054"))
    ang = math.radians(a0 + (a1 - a0) * (ajuste - rango[0]) / (rango[1] - rango[0]))
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + (r - 0.8) * math.cos(ang):.2f}" y2="{cy - (r - 0.8) * math.sin(ang):.2f}" stroke="#D92D20" stroke-width="0.8" stroke-linecap="round"/>')
    s.append(f'<line x1="{cx - 2.6}" y1="{cy}" x2="{cx + 2.6}" y2="{cy}" stroke="#667085" stroke-width="0.6" transform="rotate({-math.degrees(ang):.1f} {cx} {cy})"/>')
    s.append(t(cx, cy + r + 3.6, "A", 1.8, "#344054"))
    s.append(rect(27, 28, 12, 6, "#ECEFF3", 0.6, "#C9CFD7", 0.25) + t(33, 31, "CLASS 10", 1.5, "#475467"))
    s.append(rect(27, 37, 5.0, 2.4, "#3D4350", 0.4) + t(34.8, 38.2, "TEST", 1.6, "#475467", 700, "start"))
    # mando giratorio
    mx, my = 26.0, 59.0
    s.append(f'<circle cx="{mx}" cy="{my}" r="11.5" fill="#E4E8ED" stroke="#B8C0CA" stroke-width="0.3"/>')
    rot = 0 if on else -90
    s.append(f'<g transform="rotate({rot} {mx} {my})" filter="url(#fSuave)"><rect x="{mx - 3.4}" y="{my - 10.5}" width="6.8" height="21" rx="3" fill="url(#gNegro)"/>'
             f'<rect x="{mx - 0.6}" y="{my - 9}" width="1.2" height="6" rx="0.6" fill="#FFFFFF"/></g>')
    s.append(t(mx, my - 14.0, "I  ON", 1.9, "#344054") + t(mx - 15.5, my, "O", 2.2, "#344054") + t(mx - 15.5, my + 3, "OFF", 1.4, "#344054"))
    s.append(t(10.5, 50.0, f"{rango[0]}–{rango[1]} A", 1.8, "#475467"))
    s.append(t(10.5, 72.0, f"-{ref}", 4.6, TXT, 700))
    s.append(rect(3, 77.2, W - 6, 1.2, AZUL, 0.6))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ BASE 8 PINES + RELÉ / TEMPORIZADOR
def rele_8p(ref="KA1", bobina="240 V~", tipo="rele"):
    W, H = 38.0, 76.0
    b = {}
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gBlanco)", 1.4, "#B8C0CA", 0.3), "</g>"]
    s.append(rect(0.5, 0.5, W - 1, 15, "url(#gGrisCl)", 0.8))
    s.append(rect(0.5, H - 15.5, W - 1, 15, "url(#gGrisCl)", 0.8))
    for x, n in zip((5.6, 14.5, 23.5, 32.4), ("3", "4", "5", "6")):
        s.append(t(x, 3.2, n, 3.0, "#344054"))
        s.append(tornillo(x, 9.6, 3.2))
        b[n] = (x, 9.6)
    for x, n in zip((5.6, 14.5, 23.5, 32.4), ("2", "1", "8", "7")):
        s.append(tornillo(x, H - 9.6, 3.2))
        s.append(t(x, H - 3.0, n, 3.0, "#344054"))
        b[n] = (x, H - 9.6)
    if tipo == "rele":
        s.append('<g filter="url(#fSuave)">' + rect(3, 17.5, W - 6, 41, "#DDE6EF", 1.6, "#AEB9C6", 0.35) + "</g>")
        s.append(rect(4.2, 18.7, W - 8.4, 38.6, "#E9EFF5", 1.2))
        s.append(franja_marca(5.5, 21.6, W - 11))
        s.append(t(W / 2, 26.8, f"-{ref}", 4.0, TXT))
        s.append(t(W / 2, 31.4, bobina + " · 10 A 250 V~", 1.5, "#667085"))
        for i, (c, na, nc) in enumerate((("1", "3", "4"), ("8", "6", "5"))):
            x = 12.5 + 13 * i
            s.append(f'<path d="M{x},50 v-3.6 l-2.4,-4.6 M{x - 3},40.8 h1.4 v-2.6 M{x + 3},41.6 v-3.4" stroke="#344054" stroke-width="0.35" fill="none"/>')
            s.append(t(x, 51.6, c, 1.8, "#344054") + t(x - 3, 36.8, nc, 1.8, "#344054") + t(x + 3, 36.8, na, 1.8, "#344054"))
        s.append(rect(16.0, 52.6, 6, 2.6, "none", 0, "#344054", 0.35) + t(14.4, 53.9, "2", 1.6, "#344054") + t(23.6, 53.9, "7", 1.6, "#344054"))
        s.append(f'<circle cx="{W - 6.5}" cy="54" r="1.1" fill="#86D99A" stroke="#2E7D32" stroke-width="0.3"/>')
    else:
        s.append('<g filter="url(#fSuave)">' + rect(2.5, 17.2, W - 5, 41.6, "url(#gBlancoH)", 1.4, "#B8C0CA", 0.3) + "</g>")
        s.append(t(5.2, 20.6, "POWER", 1.5, "#475467", 700, "start") + t(W - 5.2, 20.6, "UP", 1.5, "#475467", 700, "end"))
        s.append(f'<circle cx="6.6" cy="23.0" r="0.9" fill="#4ADE80"/><circle cx="{W - 6.6}" cy="23.0" r="0.9" fill="#FDBA74"/>')
        cx, cy = W / 2, 37.5
        s.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#F4F6F8" stroke="#98A2B3" stroke-width="0.3"/>')
        for i in range(31):
            a = math.radians(225 - 270 * i / 30)
            r1 = 10.4 if i % 5 else 9.4
            s.append(f'<line x1="{cx + r1 * math.cos(a):.2f}" y1="{cy - r1 * math.sin(a):.2f}" x2="{cx + 11.4 * math.cos(a):.2f}" y2="{cy - 11.4 * math.sin(a):.2f}" stroke="#344054" stroke-width="0.25"/>')
        for i, v in enumerate(("0", "1", "2", "3", "4", "5", "6")):
            a = math.radians(225 - 270 * i / 6)
            s.append(t(cx + 7.6 * math.cos(a), cy - 7.6 * math.sin(a), v, 1.6, "#344054"))
        s.append(f'<circle cx="{cx}" cy="{cy}" r="4.6" fill="url(#gNegro)"/><line x1="{cx}" y1="{cy}" x2="{cx - 6.6}" y2="{cy - 6.6}" stroke="#D92D20" stroke-width="0.6" stroke-linecap="round"/>')
        s.append(t(cx, cy + 9.4, "s · min · h", 1.4, "#475467"))
        s.append(t(5.2, 54.6, "MODE", 1.4, "#475467", 700, "start") + t(W - 4.0, 54.6, f"-{ref}", 3.4, TXT, 700, "end"))
        s.append(logo(4.8, 50.6, 2.4))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ OPERADORES DE PUERTA (frente 2D) Y BLOQUES (vista trasera)
def operador(tipo="pulsador", color="verde", ref="S1", simbolo="I", pos=0):
    grad = {"verde": "gVerde", "rojo": "gRojo", "amarillo": "gAmbar", "azul": "gAzul", "blanco": "gBlancoB", "negro": "gNegro"}[color]
    if tipo == "emergencia":
        W = H = 60.0
        cx = cy = 30.0
        s = [f'<circle cx="{cx}" cy="{cy}" r="29.5" fill="#F5C400" stroke="#B48A00" stroke-width="0.4"/>',
             t(cx, 54.5, "PARO DE EMERGENCIA", 2.6, "#3B2F00", 800),
             f'<circle cx="{cx}" cy="{cy}" r="16" fill="#D0D5DD" stroke="#98A2B3" stroke-width="0.4"/>',
             f'<g filter="url(#fSombra)"><circle cx="{cx}" cy="{cy - 1}" r="19.5" fill="url(#gRojo)"/></g>',
             f'<path d="M{cx - 6},{cy + 7} q6,3 12,0" stroke="#FFFFFF" stroke-width="0.8" fill="none" opacity="0.8"/><polygon points="{cx + 6},{cy + 5.6} {cx + 8},{cy + 7.2} {cx + 5.6},{cy + 8.4}" fill="#FFFFFF" opacity="0.8"/>']
        Ht = H + 11
    else:
        W, H = 30.0, 30.0
        cx = cy = 15.0
        s = [f'<g filter="url(#fSombra)"><circle cx="{cx}" cy="{cy}" r="14.6" fill="url(#gBlancoB)" stroke="#AEB9C4" stroke-width="0.3"/></g>',
             f'<circle cx="{cx}" cy="{cy}" r="12.0" fill="#E3E7EC" stroke="#B8C0CA" stroke-width="0.3"/>']
        if tipo == "pulsador":
            s.append(f'<circle cx="{cx}" cy="{cy}" r="10.4" fill="url(#{grad})"/>')
            s.append(f'<circle cx="{cx}" cy="{cy}" r="7.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="0.4"/>')
            if simbolo:
                s.append(t(cx, cy, simbolo, 8.5, "#FFFFFF" if color not in ("blanco", "amarillo") else TXT, 800))
        elif tipo == "piloto":
            s.append(f'<circle cx="{cx}" cy="{cy}" r="10.4" fill="url(#{grad})" opacity="0.95"/>')
            for r_ in (7.5, 5.0, 2.6):
                s.append(f'<circle cx="{cx}" cy="{cy}" r="{r_}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="0.35"/>')
        elif tipo == "selector":
            s.append(f'<circle cx="{cx}" cy="{cy}" r="10.4" fill="url(#gNegro)"/>')
            rot = 45 if pos else -45
            s.append(f'<g transform="rotate({rot} {cx} {cy})" filter="url(#fSuave)"><rect x="{cx - 2.6}" y="{cy - 9.5}" width="5.2" height="19" rx="2.2" fill="#1B1E23"/><rect x="{cx - 0.5}" y="{cy - 8.4}" width="1.0" height="6" rx="0.5" fill="#FFFFFF"/></g>')
            s.append(t(cx - 10.5, 2.0, "0", 2.6, TXT) + t(cx + 10.5, 2.0, "1", 2.6, TXT))
        Ht = H + 11
    s.append(rect(W / 2 - 12, Ht - 8.5, 24, 7.5, "#FFFFFF", 0.8, "#98A2B3", 0.3) + t(W / 2, Ht - 4.75, f"-{ref}", 3.8, TXT))
    return envolver(W, Ht, "".join(s)), {}, (W, Ht)


def bloque(n1, n2, nc=False, piloto=False):
    """Bloque de contacto (vista trasera, 2D): cuerpo negro, dos tornillos y su número impreso; etiqueta NO/NC o LED."""
    W, H = 14.0, 34.0
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "#23272E", 1.4, "#101215", 0.3), "</g>",
         rect(-8, -5.5, W + 16, 5, "#3D4350", 1.0, "#22262D", 0.3)]
    b = {}
    for y, n in ((9.0, n1), (H - 9.0, n2)):
        s.append(f'<circle cx="{W / 2}" cy="{y}" r="4.0" fill="#3A3F48"/>' + tornillo(W / 2, y, 2.9))
        s.append(t(-1.6, y, n, 3.2, TXT, 800, "end"))
        b[n] = (W / 2, y)
    if piloto:
        s.append(rect(2.4, H / 2 - 2.4, W - 4.8, 4.8, "#98A2B3", 0.8) + t(W / 2, H / 2, "LED", 2.0, TXT))
    else:
        s.append(rect(2.4, H / 2 - 2.4, W - 4.8, 4.8, "#D92D20" if nc else "#12B76A", 0.8) + t(W / 2, H / 2, "NC" if nc else "NO", 2.2, "#FFFFFF"))
    return envolver(W, H, "".join(s), 9), b, (W, H)


# ============================================================ BORNERA DE CABALLETE
def bornera(nombres, tipos=None, ref="X1", ancho=6.2):
    tipos = tipos or {}
    n = len(nombres)
    W, H = n * ancho + 2.0, 48.0
    b = {}
    s = [rect(-4.5, -2.0, 4.5, H + 4, "#7C8594", 0.6), t(-2.25, -5.5, f"-{ref}", 3.6, TXT, 800)]
    for i, nm in enumerate(nombres):
        x = i * ancho
        tp = tipos.get(nm, "paso")
        if tp == "PE":
            body = rect(x, 0, ancho - 0.25, H, "#2E9E44", 0.4, "#1E6B2E", 0.25)
            body += "".join(f'<line x1="{x}" y1="{yy}" x2="{x + ancho - 0.25}" y2="{yy - 3}" stroke="#F2C200" stroke-width="1.4"/>' for yy in range(4, int(H), 5))
        elif tp == "N":
            body = rect(x, 0, ancho - 0.25, H, "#2F6FD0", 0.4, "#1A4FA0", 0.25)
        else:
            body = rect(x, 0, ancho - 0.25, H, "#B3BAC4", 0.4, "#7C8594", 0.25) + rect(x + 0.6, 0.6, 1.0, H - 1.2, "#CDD2D9", 0.3)
        s.append(body)
        xc = x + (ancho - 0.25) / 2
        s.append(rect(x + 0.5, 17.5, ancho - 1.25, 13, "#FFFFFF", 0.4, "#98A2B3", 0.2) + t(xc, 24, nm, 2.4 if len(nm) < 3 else 1.9, TXT, 800, rot=-90 if len(nm) > 1 else 0))
        s.append(tornillo_ranura(xc, 8.0, 2.1, "#5B6472"))
        s.append(tornillo_ranura(xc, H - 8.0, 2.1, "#5B6472"))
        b[nm + "^"] = (xc, 8.0)
        b[nm + "v"] = (xc, H - 8.0)
    s.append(rect(n * ancho - 0.25, -1.0, 2.0, H + 2, "#7C8594", 0.4))
    return envolver(W, H, "".join(s), 7), b, (W, H)


# ============================================================ MOTOR (vista lateral, plano)
def motor(ref="M1"):
    W, H = 300.0, 200.0
    s = ['<g filter="url(#fSombra)">']
    s.append(rect(48, 30, 200, 140, "url(#gMotor)", 18, "#163E73", 1.2))
    for i in range(10):
        y = 40 + i * 13.2
        s.append(rect(56, y, 184, 5, "#1F4F96", 2.5, None) + rect(56, y, 184, 1.6, "#5C98E6", 0.8, None))
    s.append(rect(14, 44, 40, 112, "url(#gMotor)", 16, "#163E73", 1.2))
    for i in range(7):
        s.append(rect(18, 54 + i * 14, 32, 3.4, "#1F4F96", 1.7))
    s.append(rect(118, 6, 92, 30, "url(#gMotor)", 6, "#163E73", 1.2))
    s.append(f'<circle cx="112" cy="21" r="8" fill="#1B1E23"/>')
    s.append(rect(248, 82, 46, 36, "url(#gMetal)", 3, "#7C8594", 0.8) + rect(262, 88, 26, 7, "#5B6472", 1))
    for x in (70, 226):
        s.append(f'<polygon points="{x - 26},192 {x + 26},192 {x + 16},166 {x - 16},166" fill="#1F4F96" stroke="#163E73" stroke-width="1"/>')
    s.append("</g>")
    s.append(rect(118, 80, 72, 42, "#DDE2E8", 3, "#98A2B3", 0.8) + t(154, 92, "3~ MOTOR", 7, TXT) + t(154, 110, f"-{ref}", 10, TXT, 800))
    return envolver(W, H, "".join(s), 4), {"caja": (164, 21)}, (W, H)


# ============================================================ PLC (GRIS, con marca)
def cpu1212(ref="A1"):
    """S7-1200 CPU 1212C AC/DC/RLY (90 × 100 mm), según la imagen de referencia: borneras negras con tornillos de ranura,
    grupos rotulados (120-240VAC, 24VDC, 24VDC INPUTS, ANALOG INPUTS, RELAY OUTPUTS), LEDs de estado y de E/S, tapa central."""
    W, H = 90.0, 100.0
    b = {}
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gPLC)", 2.0, "#4E5866", 0.4), "</g>"]
    # bornera superior (3 conectores: alimentación 5, entradas 9, analógicas 3)
    arriba = ["L1", "N", "PE", "L+", "M", "1M", ".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", "2M", "0", "1"]
    grupos = [(0, 5), (5, 14), (14, 17)]
    paso = 5.0
    x0 = 4.5
    for g0, g1 in grupos:
        xa = x0 + g0 * paso - 2.4
        s.append(rect(xa, 2.0, (g1 - g0) * paso + 0.8, 8.6, "#22262D", 3.8))
    for i, n in enumerate(arriba):
        x = x0 + i * paso + (0.0 if i < 5 else 0.0)
        s.append(tornillo_ranura(x, 6.3, 1.85, "#22262D"))
        s.append(t(x, 13.4, n if n != "PE" else "⏚", 1.7, "#F2F4F7", 700))
        clave = {".0": "I0.0", ".1": "I0.1", ".2": "I0.2", ".3": "I0.3", ".4": "I0.4", ".5": "I0.5", ".6": "I0.6", ".7": "I0.7", "0": "AI0", "1": "AI1"}.get(n, n)
        b[clave] = (x, 6.3)
    s.append(f'<path d="M3,16 h24 M30,16 h41 M74,16 h13" stroke="#E4E7EC" stroke-width="0.25"/>')
    s.append(t(10, 18.2, "120-240VAC", 1.4, "#E4E7EC", 600) + t(21.5, 18.2, "24VDC", 1.4, "#E4E7EC", 600) + t(50, 18.2, "24VDC INPUTS", 1.4, "#E4E7EC", 600) + t(80, 18.2, "ANALOG INPUTS", 1.3, "#E4E7EC", 600))
    # LEDs de estado y de E/S
    for i, n in enumerate(("RUN / STOP", "ERROR", "MAINT")):
        s.append(rect(3.0, 24.5 + i * 4.2, 3.2, 1.8, "#C9CFD7", 0.3) + t(7.5, 25.4 + i * 4.2, n, 1.3, "#E4E7EC", 600, "start"))
    for i in range(8):
        s.append(rect(57 + i * 3.6, 24.5, 2.6, 1.8, "#C9CFD7", 0.3))
    s.append(f'<path d="M56,29 v-1 h29 v1" stroke="#E4E7EC" stroke-width="0.25" fill="none"/>' + "".join(t(58.3 + i * 3.6, 30.4, f".{i}", 1.2, "#E4E7EC", 600) for i in range(8)))
    s.append(t(56, 32.4, "DI a", 1.2, "#E4E7EC", 600, "start"))
    for i in range(6):
        s.append(rect(57 + i * 3.6, 58.5, 2.6, 1.8, "#C9CFD7", 0.3))
    s.append(f'<path d="M56,57 v1 h21.6 v-1" stroke="#E4E7EC" stroke-width="0.25" fill="none"/>' + "".join(t(58.3 + i * 3.6, 55.6, f".{i}", 1.2, "#E4E7EC", 600) for i in range(6)))
    s.append(t(56, 53.2, "DQ a", 1.2, "#E4E7EC", 600, "start"))
    s.append(rect(23, 23, 26, 49, "url(#gPLCcl)", 1.0, "#5E6877", 0.35))
    s.append(rect(23, 27.5, 26, 3.4, "#6E7988", 0) + t(36, 29.2, "SIEMENS", 2.2, "#E4E7EC", 800))
    s.append(t(72, 41.0, "CPU 1212C", 2.6, "#F2F4F7", 600) + t(72, 44.8, "AC/DC/RLY", 2.2, "#F2F4F7", 600))
    s.append(t(72, 48.8, f"-{ref}", 3.0, "#F2F4F7", 800))
    for i, n in enumerate(("LINK", "Rx/Tx")):
        s.append(rect(3.0, 74 + i * 4, 2.4, 1.8, "#C9CFD7", 0.3) + t(7.0, 74.9 + i * 4, n, 1.3, "#E4E7EC", 600, "start"))
    s.append(rect(30, 74, 13, 21, "url(#gPLCcl)", 0.8, "#5E6877", 0.35))
    s.append(t(64, 74.5, "RELAY OUTPUTS", 1.4, "#E4E7EC", 600))
    abajo = ["1L", ".0", ".1", ".2", ".3", "2L", ".4", ".5"]
    s.append(rect(45.6, 88.6, 42.2, 8.6, "#22262D", 3.8))
    for i, n in enumerate(abajo):
        x = 49.5 + i * 5.0
        s.append(t(x, 84.6, n, 1.6, "#F2F4F7", 700))
        s.append(tornillo_ranura(x, 92.9, 1.85, "#22262D"))
        clave = {".0": "Q0.0", ".1": "Q0.1", ".2": "Q0.2", ".3": "Q0.3", ".4": "Q0.4", ".5": "Q0.5"}.get(n, n)
        b[clave] = (x, 92.9)
    s.append(f'<path d="M46,81 v1 h20 v-1 M70,81 v1 h17 v-1" stroke="#E4E7EC" stroke-width="0.25" fill="none"/>' + t(48, 79.2, "DQ a", 1.2, "#E4E7EC", 600, "start"))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ LOGO! 8 Y LOGO!Power (GRIS, con marca)
def _fila_bornes(s, b, nombres, x0, paso, y, y_txt, claves=None, r=1.9):
    for i, n in enumerate(nombres):
        x = x0 + i * paso
        s.append(tornillo_ranura(x, y, r, "#22262D"))
        if n:
            s.append(t(x, y_txt, n, 1.8, "#F2F4F7", 700))
        b[(claves[i] if claves else n)] = (x, y)


def logo8(ref="A1"):
    """LOGO! 8 12/24RCE: 71,5 × 90 mm (4 módulos). Arriba L+ M I1…I8; abajo Q1 (1 2) … Q4 (1 2).
    Frente: display, teclas de cursor, ESC y OK, Ethernet. Se conserva la marca."""
    W, H = 71.5, 90.0
    b = {}
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gPLC)", 2.0, "#4E5866", 0.4), "</g>"]
    s.append(rect(2.2, 2.0, W - 4.4, 8.4, "#22262D", 3.6))
    _fila_bornes(s, b, ["L+", "M", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"], 6.0, 6.6, 6.2, 13.2)
    s.append(f'<path d="M3,15.6 h12 M18,15.6 h50" stroke="#E4E7EC" stroke-width="0.25"/>' + t(9, 17.4, "12/24V", 1.3, "#E4E7EC", 600) + t(43, 17.4, "I1…I8 (I1 I2 I7 I8: 0–10 V)", 1.3, "#E4E7EC", 600))
    s.append(rect(2.2, H - 10.4, W - 4.4, 8.4, "#22262D", 3.6))
    nombres, claves = [], []
    for q in range(1, 5):
        nombres += ["1", "2"]
        claves += [f"Q{q}.1", f"Q{q}.2"]
    _fila_bornes(s, b, nombres, 6.0, 8.5, H - 6.2, H - 13.2, claves)
    for q in range(4):
        s.append(t(6.0 + (2 * q + 0.5) * 8.5, H - 16.6, f"Q{q + 1}", 1.6, "#F2F4F7", 700))
        s.append(f'<path d="M{6.0 + 2 * q * 8.5 - 1.5},{H - 15.2} h{8.5 + 3}" stroke="#E4E7EC" stroke-width="0.25"/>')
    s.append(rect(3.0, 21.0, W - 6, 46, "url(#gPLCcl)", 1.2, "#5E6877", 0.35))
    s.append(t(13.0, 24.6, "SIEMENS", 2.6, "#F2F4F7", 800) + t(W - 12.0, 24.6, "LOGO!", 3.4, "#F2F4F7", 800))
    s.append(rect(6.0, 28.5, 33, 19, "#A9C5B0", 1.0, "#3F4A56", 0.5) + rect(7.4, 29.9, 30.2, 16.2, "#BFD9C4", 0.6))
    s.append(t(22.5, 34.0, "I1 I2 I3 I4", 2.0, "#2F3B33", 700) + t(22.5, 38.6, "Q1 Q2 Q3 Q4", 2.0, "#2F3B33", 700) + t(22.5, 43.2, "Mo 12:00", 2.0, "#2F3B33", 700))
    cx, cy = 54.0, 37.5
    for dx, dy, ang in ((0, -5.2, 0), (0, 5.2, 180), (-5.2, 0, 270), (5.2, 0, 90)):
        s.append(f'<g transform="rotate({ang} {cx + dx} {cy + dy})">{rect(cx + dx - 2.2, cy + dy - 2.2, 4.4, 4.4, "#5A6474", 0.6, "#3F4A56", 0.3)}<polygon points="{cx + dx},{cy + dy - 1.2} {cx + dx - 1},{cy + dy + 0.7} {cx + dx + 1},{cy + dy + 0.7}" fill="#E4E7EC"/></g>')
    s.append(rect(44.5, 47.5, 7.4, 4.0, "#5A6474", 0.6, "#3F4A56", 0.3) + t(48.2, 49.5, "ESC", 1.5, "#F2F4F7"))
    s.append(rect(56.5, 47.5, 7.4, 4.0, "#3F9E5C", 0.6, "#2E7D45", 0.3) + t(60.2, 49.5, "OK", 1.6, "#FFFFFF"))
    s.append(rect(6.0, 52.5, 11, 9, "#1B1E23", 0.8) + rect(8.0, 54.5, 7, 5, "#3A3F48", 0.4) + t(11.5, 64.0, "LAN", 1.4, "#E4E7EC", 600))
    s.append(t(30.0, 56.0, "12/24RCE", 2.0, "#F2F4F7", 700) + t(30.0, 60.0, "6ED1052-1MD08-0BA1", 1.3, "#D0D5DD", 600) + t(W - 8.0, 62.0, f"-{ref}", 3.2, "#F2F4F7", 800))
    return envolver(W, H, "".join(s)), b, (W, H)


def logo_power(ref="T1"):
    """LOGO!Power 24 V / 1,3 A: 36 × 90 mm. Arriba L N; abajo + + − −. LED DC OK y potenciómetro."""
    W, H = 36.0, 90.0
    b = {}
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "url(#gPLC)", 2.0, "#4E5866", 0.4), "</g>"]
    s.append(rect(2.2, 2.0, W - 4.4, 8.4, "#22262D", 3.6))
    _fila_bornes(s, b, ["L", "N"], 11.0, 14.0, 6.2, 13.2)
    s.append(rect(2.2, H - 10.4, W - 4.4, 8.4, "#22262D", 3.6))
    _fila_bornes(s, b, ["+", "+", "−", "−"], 6.0, 8.0, H - 6.2, H - 13.2, ["+1", "+2", "-1", "-2"])
    s.append(rect(3.0, 21.0, W - 6, 46, "url(#gPLCcl)", 1.2, "#5E6877", 0.35))
    s.append(t(W / 2, 26.0, "SIEMENS", 2.4, "#F2F4F7", 800) + t(W / 2, 31.0, "LOGO!Power", 2.6, "#F2F4F7", 800))
    s.append(t(W / 2, 36.0, "100–240 V~ → 24 V⎓ 1,3 A", 1.4, "#E4E7EC", 600))
    s.append(f'<circle cx="11" cy="47" r="1.3" fill="#3B6E47" stroke="#1F3D27" stroke-width="0.3"/>' + t(11, 50.6, "DC OK", 1.4, "#E4E7EC", 600))
    s.append(f'<circle cx="25" cy="47" r="2.6" fill="url(#gMetal)" stroke="#4E5866" stroke-width="0.3"/><line x1="23.3" y1="47" x2="26.7" y2="47" stroke="#2A2F36" stroke-width="0.5"/>' + t(25, 51.6, "22,2–26,4 V", 1.3, "#E4E7EC", 600))
    s.append(t(W / 2, 60.5, f"-{ref}", 3.2, "#F2F4F7", 800))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ SENSORES M18 Y FLOTADOR
def sensor(tipo="inductivo", ref="B1"):
    """Sensor M18 de 3 hilos PNP (lateral, cara a la derecha), con cable y punteras: BN +, BK salida, BU −."""
    W, H = 130.0, 30.0
    cy = 15.0
    cara = {"inductivo": "#2E7BE0", "capacitivo": "#F59E0B", "optico": "#2A2F38"}[tipo]
    s = ['<g filter="url(#fSombra)">']
    s.append(rect(46, cy - 9, 70, 18, "url(#gMetal)", 1.0, "#7C8594", 0.3))
    s.append("".join(f'<line x1="{x}" y1="{cy - 9}" x2="{x + 1.2}" y2="{cy + 9}" stroke="#8A94A0" stroke-width="0.35"/>' for x in range(48, 114, 2)))
    for x in (60, 92):
        s.append(rect(x, cy - 13, 5.5, 26, "url(#gMetal)", 0.8, "#5C6470", 0.35))
    s.append(rect(116, cy - 8.6, 6, 17.2, cara, 2.2, "#1F2937", 0.3))
    if tipo == "optico":
        s.append(f'<circle cx="119" cy="{cy - 3.6}" r="2.2" fill="#E5484D"/><circle cx="119" cy="{cy + 3.6}" r="2.2" fill="#6B7280"/>')
    s.append(rect(32, cy - 7.5, 14, 15, "#2A2F38", 1.6))
    s.append(f'<circle cx="39" cy="{cy - 3.4}" r="1.8" fill="#F79009"/>')
    if tipo == "capacitivo":
        s.append(f'<circle cx="39" cy="{cy + 3.4}" r="2.0" fill="url(#gMetal)"/><line x1="37.8" y1="{cy + 3.4}" x2="40.2" y2="{cy + 3.4}" stroke="#2A2F38" stroke-width="0.4"/>')
    s.append(rect(20, cy - 6, 12, 12, "url(#gMetal)", 1.0, "#5C6470", 0.3) + t(26, cy, "M12", 2.2, TXT, 800))
    s.append("</g>")
    s.append(t(80, cy - 17.5, f"-{ref}", 4.0, TXT, 800))
    b = {}
    for i, (col, nom) in enumerate((("#8B5A2B", "BN"), ("#1B1E23", "BK"), ("#2E7BE0", "BU"))):
        y = cy - 5 + 5 * i
        s.append(f'<path d="M20,{cy} C12,{cy} 10,{y} 4,{y}" stroke="{col}" stroke-width="2.2" fill="none"/>')
        s.append(rect(0, y - 1.3, 4.2, 2.6, "#E08A1E", 0.6))
        s.append(t(-1.5, y, {"BN": "BN +", "BK": "BK salida", "BU": "BU −"}[nom], 2.4, TXT, 800, "end"))
        b[nom] = (0, y)
    return envolver(W, H, "".join(s), 22), b, (W, H)


def flotador(ref="S5"):
    W, H = 60.0, 80.0
    s = ['<g filter="url(#fSombra)">', f'<rect x="10" y="0" width="40" height="62" rx="18" fill="url(#gAzul)" stroke="#164A8C" stroke-width="0.6"/>',
         f'<rect x="16" y="6" width="28" height="44" rx="12" fill="#5B9CF0" opacity="0.6"/>', rect(25, 58, 10, 9, "#C62828", 2), "</g>"]
    s.append(logo(23.5, 18, 6) + t(30, 36, f"-{ref}", 4.4, "#FFFFFF", 800))
    s.append(f'<path d="M30,67 C30,80 10,78 4,72" stroke="#1B1E23" stroke-width="4" fill="none" stroke-linecap="round"/>')
    b = {}
    for i, (col, nom) in enumerate((("#1B1E23", "C"), ("#8B5A2B", "NA"), ("#2E7BE0", "NC"))):
        y = 66 + 5 * i
        s.append(f'<path d="M4,72 C0,72 -2,{y} -8,{y}" stroke="{col}" stroke-width="2" fill="none"/>' + rect(-12, y - 1.2, 4, 2.4, "#E08A1E", 0.5))
        s.append(t(-13.5, y, nom, 2.8, TXT, 800, "end"))
        b[nom] = (-12, y)
    return envolver(W, H, "".join(s), 22), b, (W, H)


# ============================================================ CAJA DE BORNES DEL MOTOR
def caja_bornes(tipo="9", conexion="bajo"):
    """tipo '9': NEMA 9 puntas (230 V: T1-T6-T7, T2-T4-T8, T3-T5-T9). tipo '6': IEC U1 V1 W1 / W2 U2 V2 (Δ o Y)."""
    W, H = 100.0, 74.0
    s = [rect(0, 0, W, H, "url(#gMotor)", 8, "#163E73", 1.0), rect(6, 6, W - 12, H - 12, "#2A4F80", 5),
         rect(10, 10, W - 20, H - 20, "#C0392B" if tipo == "6" else "#E8E2D0", 4, "#7A271A" if tipo == "6" else "#B8A98A", 0.6)]
    b = {}
    if tipo == "6":
        pos = {"U1": (28, 26), "V1": (50, 26), "W1": (72, 26), "W2": (28, 50), "U2": (50, 50), "V2": (72, 50)}
        if conexion == "delta":
            for a, c in (("U1", "W2"), ("V1", "U2"), ("W1", "V2")):
                s.append(rect(pos[a][0] - 3, pos[a][1], 6, 24, "#D9A441", 1.5, "#8A6514", 0.4))
        else:
            s.append(rect(25, 47, 50, 6, "#D9A441", 1.5, "#8A6514", 0.4))
    else:
        if conexion == "bajo":
            pos = {"T1": (26, 22), "T6": (26, 37), "T7": (26, 52), "T2": (50, 22), "T4": (50, 37), "T8": (50, 52), "T3": (74, 22), "T5": (74, 37), "T9": (74, 52)}
            grupos = (("T1", "T7"), ("T2", "T8"), ("T3", "T9"))
        else:
            pos = {"T1": (26, 20), "T2": (50, 20), "T3": (74, 20), "T4": (26, 38), "T7": (26, 54), "T5": (50, 38), "T8": (50, 54), "T6": (74, 38), "T9": (74, 54)}
            grupos = (("T4", "T7"), ("T5", "T8"), ("T6", "T9"))
        for a, c in grupos:
            s.append(f'<line x1="{pos[a][0]}" y1="{pos[a][1]}" x2="{pos[c][0]}" y2="{pos[c][1]}" stroke="#B54708" stroke-width="3.2" stroke-linecap="round" opacity="0.85"/>')
    for n, (x, y) in pos.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="4.6" fill="url(#gMetal)" stroke="#5C6470" stroke-width="0.4"/><polygon points="{" ".join(f"{x + 2.8 * math.cos(math.radians(60 * k)):.2f},{y + 2.8 * math.sin(math.radians(60 * k)):.2f}" for k in range(6))}" fill="#9AA4B2" stroke="#5C6470" stroke-width="0.3"/>')
        s.append(rect(x + 5, y - 2.6, 9.5, 5.2, "#FFFFFF", 1, "#98A2B3", 0.3) + t(x + 9.75, y, n, 2.8, TXT, 800))
        b[n] = (x, y)
    s.append(t(W / 2, H - 4.6, "9 puntas · tensión baja (230 V)" if tipo == "9" and conexion == "bajo" else ("9 puntas · tensión alta (460 V)" if tipo == "9" else ("IEC 6 bornes · Δ" if conexion == "delta" else "IEC 6 bornes · Y")), 3.0, "#FFFFFF", 700))
    return envolver(W, H, "".join(s)), b, (W, H)


# ============================================================ INSTRUMENTOS
def multimetro(lectura="0.000", unidad="Ω"):
    W, H = 90.0, 180.0
    s = ['<g filter="url(#fSombra)">', rect(0, 0, W, H, "#F5B800", 12, "#9A7300", 0.8), "</g>", rect(6, 6, W - 12, H - 12, "#2B2F36", 8)]
    s.append(rect(12, 16, 66, 36, "#C9D8C5", 3, "#7E8C7A", 0.6) + t(64, 34, lectura, 15, TXT, 700, "end") + t(72, 44, unidad, 6, TXT, 800, "end") + t(16, 21.5, "AUTO", 3, TXT, 700, "start"))
    cx, cy = 45, 96
    s.append(f'<circle cx="{cx}" cy="{cy}" r="21" fill="url(#gNegro)" stroke="#101215" stroke-width="1"/>')
    for lab, ang in (("OFF", 160), ("V~", 120), ("V⎓", 90), ("Ω", 55), ("A", 20)):
        a = math.radians(ang)
        s.append(t(cx + 30 * math.cos(a), cy - 30 * math.sin(a), lab, 4.4, "#FFFFFF", 800))
    s.append(f'<g transform="rotate(35 {cx} {cy})"><rect x="{cx - 4}" y="{cy - 19}" width="8" height="38" rx="3" fill="#15181D"/><rect x="{cx - 1}" y="{cy - 17}" width="2" height="10" rx="1" fill="#F5B800"/></g>')
    s.append(f'<circle cx="25" cy="150" r="7" fill="#101215" stroke="#3A3F48" stroke-width="1"/><circle cx="65" cy="150" r="7" fill="#B42318" stroke="#7A271A" stroke-width="1"/>')
    s.append(t(25, 139, "COM", 4, "#FFFFFF", 800) + t(65, 139, "VΩ", 4, "#FFFFFF", 800) + t(45, 168, "CAT III 600 V", 3.4, "#F5B800", 800))
    return envolver(W, H, "".join(s)), {"COM": (25, 150), "V": (65, 150)}, (W, H)


def pinza(lectura="24.3", unidad="A~"):
    W, H = 80.0, 190.0
    s = ['<g filter="url(#fSombra)">', f'<path d="M14,70 C2,40 18,4 40,4 C62,4 78,40 66,70" stroke="#C62828" stroke-width="13" fill="none" stroke-linecap="round"/>',
         rect(6, 62, 68, 126, "#C62828", 10, "#7A271A", 0.8), "</g>", rect(12, 70, 56, 110, "#2B2F36", 6)]
    s.append(rect(17, 78, 46, 26, "#C9D8C5", 2.4, "#7E8C7A", 0.5) + t(55, 91, lectura, 10, TXT, 700, "end") + t(60, 99, unidad, 4, TXT, 800, "end"))
    s.append(f'<circle cx="40" cy="135" r="14" fill="url(#gNegro)"/>' + t(40, 160, "CAT III 600 V", 3.4, "#F5B800", 800))
    return envolver(W, H, "".join(s)), {}, (W, H)


def riel_canaleta(largo=160.0):
    W, H = largo, 90.0
    s = [rect(0, 0, W, 40, "#B7BDC6", 1, "#7C8594", 0.5)]
    for i in range(int(W // 8)):
        x = 4 + i * 8
        s.append(rect(x - 1.5, 0, 3, 6, "#8A929E", 0.3) + rect(x - 1.5, 34, 3, 6, "#8A929E", 0.3))
    s.append(rect(4, 6, W - 8, 28, "#C9CED6", 1))
    s.append(rect(0, 50, W, 35, "#A9B0BA", 0) + rect(0, 55, W, 25, "#D3D8DE", 0))
    for x in range(12, int(W), 25):
        s.append(rect(x - 5.5, 64.8, 11, 5.4, "#7C8594", 2.7))
    s.append(t(W / 2, 20, "Canaleta ranurada 40 × 40 mm", 4, TXT, 700) + t(W / 2, 88.5, "Riel DIN 35 × 7,5 mm (EN 60715)", 3.6, TXT, 700))
    return envolver(W, H, "".join(s)), {}, (W, H)


def conductores():
    """Muestra de conductores con puntera (ferrule) y marcador: colores IEC 60204-1."""
    W, H = 110.0, 80.0
    s = []
    for i, (col, lab, sec) in enumerate((("#15171B", "L1", "10 AWG"), ("#15171B", "U", "10 AWG"), ("#D92D20", "3", "14 AWG"), ("#53B1FD", "N", "14 AWG"), ("#2E9E44", "PE", "10 AWG"))):
        x = 10 + i * 22
        w = 3.2 if sec == "10 AWG" else 2.2
        s.append(f'<line x1="{x}" y1="16" x2="{x}" y2="74" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
        if lab == "PE":
            s.append(f'<line x1="{x}" y1="16" x2="{x}" y2="74" stroke="#F2C200" stroke-width="{w * 0.45}" stroke-dasharray="4 4"/>')
        s.append(rect(x - 1.4, 2, 2.8, 8, "url(#gMetal)", 0.4, "#7C8594", 0.2) + rect(x - 2.3, 9, 4.6, 7, "#2F6FD0" if sec == "14 AWG" else "#F5C400", 1.0))
        s.append(rect(x - 4.5, 22, 9, 6, "#FFFFFF", 0.8, "#98A2B3", 0.3) + t(x, 25, lab, 3.2, TXT, 800) + t(x, 78.5, sec, 2.6, TXT, 700))
    return envolver(W, H, "".join(s)), {}, (W, H)

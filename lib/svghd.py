"""Equipos en alta definición (v3): volumen, bisel, cavidades hundidas, tornillos con relieve, sombras en capas.
Luz desde arriba-izquierda. Medidas en mm. Devuelve (svg, bornes, (W, H)) igual que svgeq."""
import math
from svgeq import LOGO_POLIS, envolver as _env, FUENTE

TXT = "#1E2733"

DEFS_HD = """
<defs>
 <linearGradient id="hBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#F6F7F9"/><stop offset="1" stop-color="#E7EAEE"/></linearGradient>
 <linearGradient id="hBodyX" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0.06"/><stop offset="0.06" stop-color="#000" stop-opacity="0"/><stop offset="0.94" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.10"/></linearGradient>
 <linearGradient id="hCamara" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9ECF0"/><stop offset="1" stop-color="#D3D8DF"/></linearGradient>
 <linearGradient id="hCamaraSombra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.16"/><stop offset="0.25" stop-color="#000" stop-opacity="0"/></linearGradient>
 <linearGradient id="hOsc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#555B69"/><stop offset="0.12" stop-color="#4A505D"/><stop offset="1" stop-color="#3A3F4B"/></linearGradient>
 <linearGradient id="hPaso" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF0F3"/></linearGradient>
 <linearGradient id="hVentana" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3E46"/><stop offset="1" stop-color="#4E535C"/></linearGradient>
 <linearGradient id="hPalanca" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A5F68"/><stop offset="0.18" stop-color="#2E3238"/><stop offset="1" stop-color="#1E2126"/></linearGradient>
 <radialGradient id="hCavidad" cx="0.5" cy="0.38" r="0.62"><stop offset="0.55" stop-color="#9AA6B3"/><stop offset="0.85" stop-color="#C4CCD5"/><stop offset="1" stop-color="#E4E8ED"/></radialGradient>
 <radialGradient id="hHalo" cx="0.5" cy="0.5" r="0.5"><stop offset="0.7" stop-color="#7F92A6" stop-opacity="0.0"/><stop offset="0.86" stop-color="#7F92A6" stop-opacity="0.45"/><stop offset="1" stop-color="#7F92A6" stop-opacity="0"/></radialGradient>
 <radialGradient id="hCabeza" cx="0.36" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#F1F4F7"/><stop offset="0.85" stop-color="#D2D9E0"/><stop offset="1" stop-color="#B4BFCA"/></radialGradient>
 <linearGradient id="hArandela" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7F9FB"/><stop offset="0.5" stop-color="#C9D1DA"/><stop offset="1" stop-color="#9AA6B3"/></linearGradient>
 <linearGradient id="pBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#76818F"/><stop offset="1" stop-color="#66717F"/></linearGradient>
 <linearGradient id="pTapa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#808B99"/><stop offset="1" stop-color="#727D8B"/></linearGradient>
 <linearGradient id="pConector" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3F47"/><stop offset="0.2" stop-color="#25282E"/><stop offset="1" stop-color="#1A1C20"/></linearGradient>
 <radialGradient id="pTorn" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#E9EDF1"/><stop offset="0.6" stop-color="#AEB7C1"/><stop offset="1" stop-color="#6F7883"/></radialGradient>
 <linearGradient id="pLed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9EDF1"/><stop offset="1" stop-color="#C3CAD3"/></linearGradient>
 <filter id="hSombra" x="-15%" y="-10%" width="135%" height="130%"><feGaussianBlur in="SourceAlpha" stdDeviation="1.1"/><feOffset dx="0.7" dy="1.3" result="o"/><feComponentTransfer><feFuncA type="linear" slope="0.32"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="hSombraC" x="-20%" y="-30%" width="140%" height="180%"><feGaussianBlur in="SourceAlpha" stdDeviation="0.45"/><feOffset dx="0" dy="0.55" result="o"/><feComponentTransfer><feFuncA type="linear" slope="0.45"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="hSombraT" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="0.3"/><feOffset dx="0.15" dy="0.35" result="o"/><feComponentTransfer><feFuncA type="linear" slope="0.5"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


def envolver(W, H, cuerpo, margen=4):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-margen} {-margen} {W + 2 * margen} {H + 2 * margen}" '
            f'width="{W + 2 * margen}mm" height="{H + 2 * margen}mm">{DEFS_HD}{cuerpo}</svg>')


def T(x, y, s, size, color=TXT, peso=700, ancla="middle", rot=0, ls=0, fam=FUENTE):
    r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-size="{size}" font-weight="{peso}" fill="{color}" text-anchor="{ancla}" dominant-baseline="central" letter-spacing="{ls}"{r}>{s}</text>'


def R(x, y, w, h, fill, r=0, stroke=None, sw=0.25, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}"{st} {extra}/>'


def L(x1, y1, x2, y2, color, sw=0.25, op=1):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{sw}" stroke-opacity="{op}"/>'


def logo(x, y, h):
    s = h / 394
    return "<g>" + "".join(f'<polygon points="{" ".join(f"{px * s + x:.2f},{py * s + y:.2f}" for px, py in pts)}" fill="{c}"/>' for pts, c in LOGO_POLIS) + "</g>"


def tornillo(x, y, r=3.3, cruz="#23465C"):
    """Tornillo combinado con arandela: cavidad hundida, halo, arandela metálica, cabeza convexa y cruz grabada."""
    a, w = r * 0.6, r * 0.34
    out = [f'<circle cx="{x}" cy="{y}" r="{r * 1.32:.2f}" fill="url(#hHalo)"/>',
           f'<circle cx="{x}" cy="{y}" r="{r * 1.16:.2f}" fill="url(#hCavidad)"/>',
           f'<g filter="url(#hSombraT)"><circle cx="{x}" cy="{y}" r="{r * 1.02:.2f}" fill="url(#hArandela)"/>',
           f'<circle cx="{x}" cy="{y}" r="{r * 0.86:.2f}" fill="url(#hCabeza)" stroke="#A9B4C0" stroke-width="0.12"/></g>']
    # cruz grabada: borde claro abajo-derecha (luz), cuerpo oscuro
    for dx, dy, col, op in ((0.12, 0.14, "#FFFFFF", 0.9), (0, 0, cruz, 1)):
        out.append(f'<g opacity="{op}"><rect x="{x - a + dx:.2f}" y="{y - w / 2 + dy:.2f}" width="{2 * a:.2f}" height="{w:.2f}" rx="{w / 2:.2f}" fill="{col}"/>'
                   f'<rect x="{x - w / 2 + dx:.2f}" y="{y - a + dy:.2f}" width="{w:.2f}" height="{2 * a:.2f}" rx="{w / 2:.2f}" fill="{col}"/></g>')
    return "".join(out)


def bisel(x, y, w, h, r=1.0, luz=0.85, sombra=0.14):
    """Borde con luz arriba/izquierda y sombra abajo/derecha para dar volumen a un bloque."""
    return (L(x + r, y + 0.25, x + w - r, y + 0.25, "#FFFFFF", 0.45, luz) + L(x + 0.25, y + r, x + 0.25, y + h - r, "#FFFFFF", 0.35, luz * 0.7) +
            L(x + r, y + h - 0.25, x + w - r, y + h - 0.25, "#000000", 0.4, sombra) + L(x + w - 0.25, y + r, x + w - 0.25, y + h - r, "#000000", 0.35, sombra))


def etiqueta_borne(x, y, num, func=None, color=TXT, size=2.4):
    """'13 NO': número en negrita y la función en peso normal, centrado como bloque (no se encima con nada)."""
    if not func:
        return T(x, y, num, size, color, 800)
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FUENTE}" font-size="{size}" fill="{color}" text-anchor="middle" dominant-baseline="central">'
            f'<tspan font-weight="800">{num}</tspan><tspan font-weight="500" dx="0.6">{func}</tspan></text>')


# ====================================================================== CONTACTOR HD
def contactor(ref="KM1", bobina="240 V~ 60 Hz", ie="AC-3 · 32 A"):
    W, H = 45.0, 85.0
    b = {}
    s = []
    # cuerpo con sombra proyectada
    s.append(f'<g filter="url(#hSombra)">{R(0, 0, W, H, "url(#hBody)", 1.6, "#AEB7C2", 0.3)}</g>')
    s.append(R(0, 0, W, H, "url(#hBodyX)", 1.6))
    # cámara superior (bornes de potencia), hundida
    s.append(R(0.6, 0.6, W - 1.2, 14.2, "url(#hCamara)", 1.2) + R(0.6, 0.6, W - 1.2, 14.2, "url(#hCamaraSombra)", 1.2))
    for x in (15.0, 30.0):
        s.append(L(x, 1.2, x, 14.2, "#C2C9D2", 0.35) + L(x + 0.35, 1.2, x + 0.35, 14.2, "#FFFFFF", 0.3, 0.8))
    for x, n in zip((7.5, 22.5, 37.5), ("1/L1", "3/L2", "5/L3")):
        s.append(T(x, 2.9, n, 2.35, "#2D3748", 700))
        s.append(tornillo(x, 9.0, 3.1))
        b[n] = (x, 9.0)
    # franja oscura superior (sobresale del cuerpo: profundidad)
    s.append(f'<g filter="url(#hSombraC)">{R(-0.7, 15.4, W + 1.4, 12.8, "url(#hOsc)", 0.6)}</g>')
    s.append(L(-0.4, 15.7, W + 0.4, 15.7, "#7A8190", 0.35))
    for x, n, f_ in ((17.5, "13", "NO"), (29.0, "21", "NC"), (40.0, "A1", None)):
        s.append(tornillo(x, 19.6, 2.55))
        s.append(etiqueta_borne(x, 25.3, n, f_, "#FFFFFF", 2.15))
        b[n] = (x, 19.6)
    # frente blanco: marca, ventana, escalón con el rótulo, línea azul
    s.append(logo(2.2, 30.6, 2.6) + R(8.0, 31.25, 3.0, 1.3, "#0094B0", 0.3) if False else logo(2.2, 30.4, 2.6))
    s.append(R(13.5, 31.4, W - 15.5, 1.1, "#1F6FC5", 0.55))
    s.append(f'<g filter="url(#hSombraT)">{R(12.0, 34.6, 21.0, 7.6, "url(#hVentana)", 0.5, "#2A2E35", 0.25)}</g>')
    for i in range(5):
        s.append(R(12.7 + i * 4.0, 35.3, 3.6, 6.2, "#575C66" if i % 2 == 0 else "#7B818B", 0.2))
    s.append(L(12.2, 34.85, 32.8, 34.85, "#FFFFFF", 0.25, 0.25))
    s.append(T(6.4, 37.2, bobina.split(" ")[0] + " " + bobina.split(" ")[1], 1.55, "#667085", 700) + T(6.4, 39.4, " ".join(bobina.split(" ")[2:]) or "", 1.4, "#8A94A3", 600))
    s.append(T(39.0, 37.2, ie.split(" · ")[0], 1.55, "#667085", 700) + T(39.0, 39.4, ie.split(" · ")[1], 1.4, "#8A94A3", 600))
    # escalón: líneas del perfil y placa elevada central
    s.append(f'<path d="M1.2,43.6 H10.8 V45.2 M34.2,45.2 V43.6 H43.8" stroke="#CBD1D9" stroke-width="0.35" fill="none"/>')
    s.append(f'<path d="M1.2,43.85 H10.6" stroke="#FFFFFF" stroke-width="0.3"/>')
    s.append(f'<g filter="url(#hSombraT)">{R(10.8, 44.4, 23.4, 7.4, "url(#hPaso)", 0.4, "#D2D8DF", 0.25)}</g>')
    s.append(T(W / 2, 48.2, f"-{ref}", 4.4, TXT, 700))
    s.append(f'<g filter="url(#hSombraT)">{R(3.2, 53.2, W - 6.4, 1.25, "#1F6FC5", 0.6)}</g>')
    # franja oscura inferior
    s.append(f'<g filter="url(#hSombraC)">{R(-0.7, 56.2, W + 1.4, 12.8, "url(#hOsc)", 0.6)}</g>')
    s.append(L(-0.4, 56.5, W + 0.4, 56.5, "#7A8190", 0.35))
    for x, n, f_ in ((17.5, "14", "NO"), (29.0, "22", "NC"), (40.0, "A2", None)):
        s.append(etiqueta_borne(x, 59.5, n, f_, "#FFFFFF", 2.15))
        s.append(tornillo(x, 64.9, 2.55))
        b[n] = (x, 64.9)
    # cámara inferior
    s.append(R(0.6, 70.2, W - 1.2, 14.2, "url(#hCamara)", 1.2) + R(0.6, 70.2, W - 1.2, 14.2, "url(#hCamaraSombra)", 1.2))
    for x in (15.0, 30.0):
        s.append(L(x, 70.8, x, 83.8, "#C2C9D2", 0.35) + L(x + 0.35, 70.8, x + 0.35, 83.8, "#FFFFFF", 0.3, 0.8))
    for x, n in zip((7.5, 22.5, 37.5), ("2/T1", "4/T2", "6/T3")):
        s.append(tornillo(x, 76.0, 3.1))
        s.append(T(x, 82.2, n, 2.35, "#2D3748", 700))
        b[n] = (x, 76.0)
    s.append(bisel(0, 0, W, H, 1.6, 0.7, 0.12))
    return envolver(W, H, "".join(s)), b, (W, H)


# ====================================================================== DISYUNTOR HD
def disyuntor(polos=2, In=6, curva="C", ref="F1", on=False):
    W, H = 18.0 * polos, 90.0
    b = {}
    s = [f'<g filter="url(#hSombra)">{R(0, 0, W, H, "url(#hBody)", 1.4, "#AEB7C2", 0.3)}</g>', R(0, 0, W, H, "url(#hBodyX)", 1.4)]
    # cámaras de bornes (perfil más bajo que el frente: más oscuras y con sombra del frente)
    for y0 in (0.6, H - 20.6):
        s.append(R(0.6, y0, W - 1.2, 20.0, "url(#hCamara)", 1.0) + R(0.6, y0, W - 1.2, 20.0, "url(#hCamaraSombra)", 1.0))
    s.append(R(0.6, 20.6, W - 1.2, 1.2, "#000000", 0.2, extra='opacity="0.10"') + R(0.6, H - 21.8, W - 1.2, 1.2, "#000000", 0.2, extra='opacity="0.06"'))
    for i in range(1, polos):
        x = 18.0 * i
        s.append(L(x, 0.8, x, H - 0.8, "#BCC4CE", 0.4) + L(x + 0.4, 0.8, x + 0.4, H - 0.8, "#FFFFFF", 0.3, 0.8))
    for i in range(polos):
        xc = 9.0 + 18.0 * i
        s.append(tornillo(xc, 10.6, 3.5))
        s.append(tornillo(xc, H - 10.6, 3.5))
        s.append(T(xc + 6.3, 3.0, str(2 * i + 1), 2.0, "#556070", 700))
        s.append(T(xc + 6.3, H - 3.0, str(2 * i + 2), 2.0, "#556070", 700))
        b[str(2 * i + 1)] = (xc, 10.6)
        b[str(2 * i + 2)] = (xc, H - 10.6)
    # frente elevado
    s.append(R(0.5, 21.6, W - 1.0, 47.0, "url(#hPaso)", 0.6) + bisel(0.5, 21.6, W - 1.0, 47.0, 0.6, 0.9, 0.12))
    s.append(logo(2.0, 23.4, 2.4))
    s.append(R(W - 5.5, 24.2, 3.6, 1.2, "#1F6FC5", 0.4))
    s.append(T(1.8, 31.0, f"{curva}{In}", 7.6 if polos > 1 else 6.0, "#8C95A2", 600, "start"))
    s.append(T(1.9, 36.0, "230/400 V~", 1.55, "#8C95A2", 600, "start"))
    s.append(T(1.9, 38.2, "6 kA · IEC 60898-1", 1.3, "#A0A8B4", 600, "start"))
    # símbolo impreso (por polo): borne, ×, cuchilla, borne
    for i in range(polos):
        xs = W - 3.0 - (polos - 1 - i) * 3.4
        s.append(f'<g stroke="#5B6472" stroke-width="0.26" fill="none"><path d="M{xs},27.6 v2.6"/><path d="M{xs - 0.8},29.4 l1.6,1.6 M{xs + 0.8},29.4 l-1.6,1.6"/><path d="M{xs},35.6 l-1.3,-2.6"/><path d="M{xs},35.6 v2.0"/></g>')
        s.append(T(xs - 1.2, 27.8, str(2 * i + 1), 1.1, "#5B6472", 600) + T(xs - 1.2, 37.8, str(2 * i + 2), 1.1, "#5B6472", 600))
    # palanca: puente común + manijas por polo (profundidad con degradado y brillo)
    s.append(f'<g filter="url(#hSombraC)">{R(1.4, 40.6, W - 2.8, 4.4, "url(#hPalanca)", 0.4)}</g>')
    s.append(R(1.6, 41.3, W - 3.2, 0.7, "#8A9099", 0.3) + R(1.6, 43.0, W - 3.2, 0.5, "#5E636C", 0.2))
    y_m = 45.0 if not on else 44.2
    for i in range(polos):
        x0 = 18.0 * i + 2.4
        s.append(f'<g filter="url(#hSombraC)">{R(x0, y_m, 13.2, 9.6, "url(#hPalanca)", 0.5)}</g>')
        s.append(R(x0 + 0.4, y_m + 0.7, 12.4, 0.7, "#8A9099", 0.3) + R(x0 + 0.4, y_m + 2.6, 12.4, 0.45, "#666B74", 0.2))
    s.append(R(W - 4.8, 56.6, 3.0, 1.6, "#D92D20" if on else "#12B76A", 0.4))
    s.append(T(W / 2 - (2.0 if polos == 1 else 0), 60.6, f"-{ref}", 6.0 if polos > 1 else 4.6, TXT, 600))
    s.append(f'<g filter="url(#hSombraT)">{R(2.2, 65.4, W - 4.4, 1.5, "#1F6FC5", 0.7)}</g>')
    s.append(bisel(0, 0, W, H, 1.4, 0.6, 0.12))
    return envolver(W, H, "".join(s)), b, (W, H)


# ====================================================================== CPU 1212C AC/DC/RLY HD (con marca)
def torn_plc(x, y, r=1.75):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r * 1.25:.2f}" fill="#0E1013"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="url(#pTorn)"/>'
            f'<line x1="{x - r * 0.72:.2f}" y1="{y + r * 0.42:.2f}" x2="{x + r * 0.72:.2f}" y2="{y - r * 0.42:.2f}" stroke="#2B3036" stroke-width="{r * 0.34:.2f}" stroke-linecap="round"/>'
            f'<line x1="{x - r * 0.62:.2f}" y1="{y + r * 0.58:.2f}" x2="{x + r * 0.62:.2f}" y2="{y - r * 0.26:.2f}" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="0.12"/>')


def conector(x0, y0, n, paso, alto=8.6):
    w = n * paso + 1.0
    s = [f'<g filter="url(#hSombraC)">{R(x0, y0, w, alto, "url(#pConector)", alto / 2.2)}</g>', L(x0 + 2, y0 + 0.4, x0 + w - 2, y0 + 0.4, "#5A616B", 0.3)]
    for i in range(1, n):
        x = x0 + 0.5 + i * paso
        s.append(L(x, y0 + 1.2, x, y0 + alto - 1.2, "#0B0C0E", 0.25))
    return "".join(s), [x0 + 0.5 + paso * (i + 0.5) for i in range(n)]


def led(x, y, w=2.6, h=1.9):
    return R(x, y, w, h, "url(#pLed)", 0.25, "#5C6675", 0.15) + L(x + 0.2, y + 0.2, x + w - 0.2, y + 0.2, "#FFFFFF", 0.15, 0.9)


def cpu1212(ref="A1"):
    W, H = 90.0, 100.0
    b = {}
    C, C2 = "#EEF1F5", "#D7DCE3"
    s = [f'<g filter="url(#hSombra)">{R(0, 0, W, H, "url(#pBody)", 2.4, "#4B5563", 0.4)}</g>']
    # conectores superiores: [L1 N PE L+ M] [1M .0 … .7] [2M 0 1]
    paso = 4.75
    grupos = [(["L1", "N", "PE", "L+", "M"], 1.6), (["1M", ".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7"], 26.6), (["2M", "0", "1"], 72.6)]
    claves = {".0": "I0.0", ".1": "I0.1", ".2": "I0.2", ".3": "I0.3", ".4": "I0.4", ".5": "I0.5", ".6": "I0.6", ".7": "I0.7", "0": "AI0", "1": "AI1"}
    for nombres, x0 in grupos:
        cs, xs = conector(x0, 1.4, len(nombres), paso)
        s.append(cs)
        for x, n in zip(xs, nombres):
            s.append(torn_plc(x, 5.7))
            b[claves.get(n, n)] = (x, 5.7)
            s.append(T(x, 12.5, n if n != "PE" else "⏚", 1.75, C, 600))
    xs_all = {n: x for (nombres, x0) in grupos for n, x in zip(nombres, conector(x0, 1.4, len(nombres), paso)[1])}
    # flechas: alimentación de entrada (↓) y salida de sensores (↑)
    for n in ("L1", "N"):
        pass
    x_l1, x_n, x_pe, x_lp, x_m = (xs_all[k] for k in ("L1", "N", "PE", "L+", "M"))
    s.append(f'<path d="M{x_l1},14.3 V15.6 H{x_n} V14.3 M{(x_l1 + x_n) / 2},15.6 V17.8" stroke="{C}" stroke-width="0.28" fill="none"/>'
             f'<polygon points="{(x_l1 + x_n) / 2 - 0.8},17.0 {(x_l1 + x_n) / 2 + 0.8},17.0 {(x_l1 + x_n) / 2},18.3" fill="{C}"/>')
    s.append(f'<path d="M{x_lp},14.3 V15.6 H{x_m} V14.3 M{(x_lp + x_m) / 2},15.6 V18.0" stroke="{C}" stroke-width="0.28" fill="none"/>'
             f'<polygon points="{(x_lp + x_m) / 2 - 0.8},16.1 {(x_lp + x_m) / 2 + 0.8},16.1 {(x_lp + x_m) / 2},14.9" fill="{C}" transform="translate(0,1.2)"/>')
    s.append(f'<path d="M{x_pe - 1.0},15.0 h2.0 M{x_pe - 0.65},15.6 h1.3 M{x_pe - 0.3},16.2 h0.6 M{x_pe},14.2 v0.8" stroke="{C}" stroke-width="0.28"/>')
    s.append(T((x_l1 + x_n) / 2 + 1.5, 20.2, "120-240VAC", 1.45, C, 600) + T((x_lp + x_m) / 2, 20.2, "24VDC", 1.45, C, 600))
    x10, x17 = xs_all["1M"], xs_all[".7"]
    s.append(f'<path d="M{xs_all[".0"]},14.3 V15.3 H{x17} V14.3" stroke="{C}" stroke-width="0.28" fill="none"/>' + T((xs_all[".0"] + x17) / 2, 16.6, "DI a", 1.2, C2, 600))
    s.append(T((x10 + x17) / 2, 20.2, "24VDC INPUTS", 1.45, C, 600))
    s.append(f'<path d="M{xs_all["0"]},14.3 V15.3 H{xs_all["1"]} V14.3" stroke="{C}" stroke-width="0.28" fill="none"/>' + T((xs_all["0"] + xs_all["1"]) / 2, 16.6, "AI", 1.2, C2, 600))
    s.append(T((xs_all["2M"] + xs_all["1"]) / 2, 19.6, "ANALOG", 1.45, C, 600) + T((xs_all["2M"] + xs_all["1"]) / 2, 21.6, "INPUTS", 1.45, C, 600))
    # líneas del panel (profundidad del frente)
    for y in (26.2, 63.6):
        s.append(L(1.0, y, W - 1.0, y, "#5B6573", 0.35) + L(1.0, y + 0.35, W - 1.0, y + 0.35, "#8D98A6", 0.25))
    # tapa central (elevada) y tapa inferior (puerto PROFINET)
    s.append(f'<g filter="url(#hSombraC)">{R(14.2, 22.4, 31.6, 56.0, "url(#pTapa)", 0.8, "#5B6573", 0.35)}</g>' + bisel(14.2, 22.4, 31.6, 56.0, 0.8, 0.35, 0.2))
    s.append(f'<g filter="url(#hSombraC)">{R(21.2, 78.4, 21.6, 21.0, "url(#pTapa)", 0.6, "#5B6573", 0.35)}</g>' + bisel(21.2, 78.4, 21.6, 21.0, 0.6, 0.3, 0.2))
    s.append(R(15.4, 27.6, 17.6, 4.0, "#5F8597", 0.3) + T(24.2, 29.6, "SIEMENS", 2.45, "#EAF2F6", 800, ls=0.12))
    s.append(R(30.6, 21.4, 4.0, 1.6, "#2B3038", 0.3))
    # LEDs de estado + textos verticales
    for i, n in enumerate(("RUN / STOP", "ERROR", "MAINT")):
        x = 3.0 + i * 3.6
        s.append(led(x, 28.2, 2.6, 1.9))
        s.append(T(x + 1.3, 36.6, n, 1.35, C, 600, "middle", rot=-90))
    # LEDs DI (8) y DQ (6) con corchetes
    for i in range(8):
        s.append(led(56.2 + i * 3.75, 28.2))
    s.append(f'<path d="M56.0,35.2 V34.2 H85.3 V35.2" stroke="{C}" stroke-width="0.26" fill="none"/>' + "".join(T(57.5 + i * 3.75, 33.0, f".{i}", 1.3, C, 600) for i in range(8)) + T(57.4, 36.6, "DI a", 1.15, C2, 600, "start"))
    s.append(T(76.0, 44.0, "CPU 1212C", 2.55, C, 500) + T(76.0, 47.6, "AC/DC/RLY", 2.55, C, 500))
    s.append(T(57.4, 52.6, "DQ a", 1.15, C2, 600, "start") + f'<path d="M56.0,55.4 V56.4 H77.0 V55.4" stroke="{C}" stroke-width="0.26" fill="none"/>' + "".join(T(57.5 + i * 3.75, 54.3, f".{i}", 1.3, C, 600) for i in range(6)))
    for i in range(6):
        s.append(led(56.2 + i * 3.75, 58.6))
    s.append(T(84.6, 60.0, f"-{ref}", 2.6, C, 800, "end") if False else "")
    for i, n in enumerate(("LINK", "Rx/Tx")):
        s.append(led(3.0, 67.0 + i * 3.6, 2.2, 1.7) + T(6.4, 67.85 + i * 3.6, n, 1.4, C, 600, "start"))
    # salidas a relé: [1L .0 .1 .2 .3] [2L .4 .5]
    s.append(T(69.0, 79.6, "RELAY OUTPUTS", 1.45, C, 600) + T(49.6, 81.6, "DQ a", 1.15, C2, 600, "start"))
    abajo = [(["1L", ".0", ".1", ".2", ".3"], 49.4), (["2L", ".4", ".5"], 74.6)]
    clv = {".0": "Q0.0", ".1": "Q0.1", ".2": "Q0.2", ".3": "Q0.3", ".4": "Q0.4", ".5": "Q0.5"}
    for nombres, x0 in abajo:
        cs, xs = conector(x0, 90.0, len(nombres), 4.6)
        s.append(cs)
        s.append(f'<path d="M{xs[0] - 0.8},83.8 V82.8 H{xs[-1] + 0.8} V83.8" stroke="{C}" stroke-width="0.26" fill="none"/>')
        for x, n in zip(xs, nombres):
            s.append(T(x, 86.6, n, 1.6, C, 600))
            s.append(torn_plc(x, 94.3))
            b[clv.get(n, n)] = (x, 94.3)
    s.append(T(33.0, 74.0, f"-{ref}", 3.0, C, 800) if False else "")
    s.append(bisel(0, 0, W, H, 2.4, 0.35, 0.2))
    return envolver(W, H, "".join(s)), b, (W, H)

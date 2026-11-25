"""Piezas nuevas de la serie ARRANQUES (reels A03, A11, A13), 24-nov. Estilo plano de svgref, vistas en CORTE.
Fuentes de forma y funcionamiento:
- Relé térmico en corte (bimetal por fase con calefactor enrollado, regleta de disparo, mecanismo con resorte, 95-96 NC y 97-98 NA):
  IEC 60947-4-1 (relés de sobrecarga); Schneider "TeSys LRD thermal overload relays" (catálogo); Siemens 3RU2 manual de
  instrucciones (esquema interno); CHINT NR2 hoja de datos (95-96 / 97-98, TEST, STOP, RESET H/A).
- Puntera DIN 46228-4: tubo de cobre estañado + collar de plástico de color por sección (0,5 blanco · 0,75 gris · 1 rojo ·
  1,5 negro · 2,5 azul · 4 gris · 6 amarillo · 10 rojo); Phoenix Contact, guía de punteras AI; Weidmüller, punteras H.
- Electroimán del contactor en corte (núcleo E laminado fijo, bobina en el brazo central con A1-A2, armadura E móvil,
  resortes de retorno, espiras de sombra de cobre en las caras polares, puente de contactos móvil con pastillas de plata):
  Schneider FAQ FA129583 (VA de llamada y mantenimiento); Siemens SIRIUS 3RT2 manual; ABB AF "contactor technology".
Cada función devuelve (svg, puntos_mm, (W, H)) como svgref."""
from svgref import svg_mm, R, T

COBRE, COBRE_O, PLATA = "#C87533", "#8C4A1E", "#D7DCE1"


def _resorte(x, y0, y1, w=22, n=7, color="#6E7680", grosor=6):
    paso = (y1 - y0) / (2 * n)
    pts = [f"{x},{y0}"]
    for i in range(1, 2 * n):
        pts.append(f"{x + (w if i % 2 else -w)},{y0 + i * paso:.1f}")
    pts.append(f"{x},{y1}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{grosor}" stroke-linejoin="round"/>'


def rele_corte(disparado=False, ancho_mm=60.0):
    W, H = 640, 560
    s = ancho_mm / W
    dx = 46 if disparado else 0
    c = ['<defs><linearGradient id="gCav" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D5DAE0"/><stop offset="1" stop-color="#C3C9D0"/></linearGradient></defs>']
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, W, H, "#EEF0F2")}</g>' + R(18, 18, W - 36, H - 36, "url(#gCav)"))
    pts = {}
    for k, x in enumerate((110, 230, 350)):
        # pin de entrada (del contactor) y terminal de salida
        c.append(R(x - 12, 0, 24, 70, "url(#rCobre)") + R(x - 30, 440, 60, 50, "#2B2F36") + R(x - 12, 490, 24, 52, "url(#rCobre)"))
        # lámina bimetálica: dos capas (acero / latón) empotradas abajo; se curva a la derecha con la sobrecarga
        for off, col in ((-6, "#8E98A3"), (6, "#C9A227")):
            c.append(f'<path d="M{x + off},440 Q{x + off},260 {x + off + dx},120" fill="none" stroke="{col}" stroke-width="12"/>')
        # calefactor de cobre enrollado sobre la lámina (vueltas en diagonal)
        for i in range(9):
            y = 180 + i * 28
            t = (440 - y) / 320
            xc = x + dx * (1 - t) ** 2
            c.append(f'<line x1="{xc - 26}" y1="{y + 8}" x2="{xc + 26}" y2="{y - 8}" stroke="{COBRE}" stroke-width="9" stroke-linecap="round"/>')
        c.append(f'<line x1="{x}" y1="70" x2="{x - 22}" y2="176" stroke="{COBRE}" stroke-width="8"/>')
        pts[f"bimetal{k + 1}"] = (x * s, 300 * s)
    pts["calefactor"] = (230 * s, 260 * s)
    pts["bimetal"] = (110 * s, 330 * s)
    # regleta de disparo (plástico oscuro) con las muescas que tocan cada lámina
    c.append(f'<g filter="url(#sTorn)">{R(70 + dx, 98, 420, 30, "#3A3F47")}</g>')
    for x in (110, 230, 350):
        c.append(R(x + dx + 8, 96, 10, 34, "#20242A"))
    pts["regleta"] = ((300 + dx) * s, 113 * s)
    # mecanismo: palanca, resorte y contactos auxiliares
    c.append(f'<line x1="{490 + dx}" y1="113" x2="{560}" y2="{200}" stroke="#20242A" stroke-width="12" stroke-linecap="round"/>')
    c.append('<circle cx="560" cy="200" r="12" fill="#5A626C"/>')
    yb = 300 if disparado else 262          # puente móvil
    c.append(f'<line x1="560" y1="200" x2="560" y2="{yb}" stroke="#20242A" stroke-width="10"/>')
    c.append(_resorte(560, yb + 14, 470, 20, 6))
    c.append(R(504, yb - 7, 112, 14, "#6E747B") + f'<circle cx="512" cy="{yb - 9}" r="8" fill="{PLATA}"/><circle cx="608" cy="{yb - 9}" r="8" fill="{PLATA}"/>'
             + f'<circle cx="512" cy="{yb + 9}" r="8" fill="{PLATA}"/><circle cx="608" cy="{yb + 9}" r="8" fill="{PLATA}"/>')
    for y, n1, n2 in ((236, "95", "96"), (326, "97", "98")):
        c.append(R(486, y - 8, 36, 16, "url(#rCobre)") + R(598, y - 8, 36, 16, "url(#rCobre)")
                 + f'<circle cx="512" cy="{y + (8 if y < 300 else -8)}" r="8" fill="{PLATA}"/><circle cx="608" cy="{y + (8 if y < 300 else -8)}" r="8" fill="{PLATA}"/>'
                 + T(470, y, n1, 26, "#101828", 800, "end") + T(630, y - 26, n2, 26, "#101828", 800, "end"))
    pts["nc"] = (560 * s, 236 * s)
    pts["no"] = (560 * s, 326 * s)
    pts["resorte"] = (560 * s, 420 * s)
    pts["pin1"] = (110 * s, 30 * s)
    svg, WH = svg_mm(W, H, s, "".join(c))
    return svg, pts, WH


def puntera(tipo="puntera", collar="#1E4FD8", aislamiento="#D92D20", largo_mm=90.0):
    """Vista lateral de la punta del cable. tipo: 'hilos' (pelado, hilos sueltos y abiertos) o 'puntera' (crimpada)."""
    W, H = 900, 220
    s = largo_mm / W
    cy = 110
    c = [f'<g filter="url(#sTorn)">{R(0, cy - 38, 380, 76, aislamiento)}</g>' + R(0, cy - 38, 380, 10, "#ffffff40")]
    pts = {"aislamiento": (190 * s, cy * s)}
    if tipo == "hilos":
        import math
        for i in range(19):
            a = (i - 9) * 0.045
            x1, y1 = 380 + 300 * math.cos(a), cy + (i - 9) * 3 + 300 * math.sin(a) * 1.3
            c.append(f'<path d="M380,{cy + (i - 9) * 3.2} Q500,{cy + (i - 9) * 3.6} {x1:.0f},{y1:.0f}" fill="none" stroke="url(#rCobre)" stroke-width="7" stroke-linecap="round"/>')
        pts["hilos"] = (640 * s, (cy - 40) * s)
    else:
        # collar de plástico (cono + cilindro) y tubo de cobre estañado crimpado
        c.append(f'<g filter="url(#sTorn)"><path d="M360,{cy - 52} L470,{cy - 46} L470,{cy + 46} L360,{cy + 52} Z" fill="{collar}"/></g>'
                 + f'<path d="M360,{cy - 52} L470,{cy - 46} L470,{cy - 34} L360,{cy - 38} Z" fill="#ffffff40"/>')
        c.append(f'<g filter="url(#sTorn)">{R(470, cy - 24, 400, 48, "url(#rAcero)")}</g>')
        for x in range(520, 860, 40):
            c.append(R(x, cy - 24, 6, 48, "#9AA1A9"))
        c.append(R(866, cy - 24, 8, 48, "#C87533"))
        pts["collar"] = (415 * s, cy * s)
        pts["tubo"] = (680 * s, cy * s)
        pts["punta"] = (870 * s, cy * s)
    svg, WH = svg_mm(W, H, s, "".join(c))
    return svg, pts, WH


def bobina_corte(cerrado=False, ancho_mm=60.0):
    W, H = 600, 720
    s = ancho_mm / W
    gap = 0 if cerrado else 70
    c = []
    lam = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="720" stroke="#5E6670" stroke-width="2" opacity="0.55"/>' for x in range(80, 521, 12))
    # núcleo fijo en E (laminado) con la ventana de la bobina
    nuc = "M80,400 H170 V560 H265 V400 H335 V560 H430 V400 H520 V650 H80 Z"
    c.append(f'<defs><clipPath id="cN"><path d="{nuc}"/></clipPath><clipPath id="cA"><path d="M80,{180 - gap} H520 V{395 - gap} H430 V{260 - gap} H335 V{395 - gap} H265 V{260 - gap} H170 V{395 - gap} H80 Z"/></clipPath></defs>')
    c.append(f'<g filter="url(#sCuerpo)"><path d="{nuc}" fill="#9AA3AD"/></g><g clip-path="url(#cN)">{lam}</g>')
    # bobina: carrete negro + sección del bobinado de cobre a cada lado del brazo central
    for x0 in (175, 340):
        c.append(R(x0, 402, 85, 156, "#1E2125"))
        for yy in range(416, 548, 16):
            for xx in range(x0 + 12, x0 + 80, 16):
                c.append(f'<circle cx="{xx}" cy="{yy}" r="6.5" fill="{COBRE}" stroke="{COBRE_O}" stroke-width="1.5"/>')
    # espiras de sombra (cobre) en las caras polares de los brazos exteriores
    for x in (80, 470):
        c.append(R(x + 6, 404, 40, 16, COBRE))
    # armadura E móvil (laminada)
    arm = f"M80,{180 - gap} H520 V{395 - gap} H430 V{260 - gap} H335 V{395 - gap} H265 V{260 - gap} H170 V{395 - gap} H80 Z"
    c.append(f'<g filter="url(#sCuerpo)"><path d="{arm}" fill="#AEB6BF"/></g><g clip-path="url(#cA)">{lam}</g>')
    # resortes de retorno a los lados
    for x in (40, 560):
        c.append(R(x - 24, 640, 48, 14, "#5A626C") + _resorte(x, 230 - gap, 640, 16, 8))
        c.append(R(x - 24, 206 - gap, 48 + (0 if x == 40 else 0), 14, "#5A626C") + f'<line x1="{x}" y1="{213 - gap}" x2="{80 if x == 40 else 520}" y2="{213 - gap}" stroke="#5A626C" stroke-width="8"/>')
    # porta-contactos y puente móvil; contactos fijos arriba
    # puente móvil sobre la armadura; los contactos fijos están DEBAJO del puente: al bajar la armadura, el puente los toca
    c.append(R(250, 110 - gap, 100, 72, "#2B2F36") + R(26, 74 - gap, 548, 18, "url(#rCobre)")
             + f'<circle cx="44" cy="{100 - gap}" r="9" fill="#D7DCE1"/><circle cx="556" cy="{100 - gap}" r="9" fill="#D7DCE1"/>')
    for x in (-30, 530):
        c.append(R(x, 118, 100, 20, "url(#rCobre)"))
    c.append('<circle cx="44" cy="110" r="9" fill="#D7DCE1"/><circle cx="556" cy="110" r="9" fill="#D7DCE1"/>')
    # terminales A1 / A2 y sus hilos
    for x, n in ((40, "A1"), (560, "A2")):
        xb = 190 if n == "A1" else 410
        c.append(f'<path d="M{xb},560 Q{xb},690 {x},690" fill="none" stroke="{COBRE}" stroke-width="6"/>'
                 + R(x - 26, 676, 52, 30, "#5A626C") + T(x, 660, n, 28, "#101828", 800))
    pts = {"nucleo": (300 * s, 610 * s), "armadura": (300 * s, (215 - gap) * s), "bobina": (217 * s, 480 * s),
           "espira": (100 * s, 412 * s), "resorte": (560 * s, 420 * s), "entrehierro": (300 * s, (397 - gap / 2) * s),
           "contacto": (44 * s, 110 * s), "A1": (40 * s, 690 * s), "A2": (560 * s, 690 * s)}
    svg, WH = svg_mm(W, H, s, "".join(c))
    return svg, pts, WH

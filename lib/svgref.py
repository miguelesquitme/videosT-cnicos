"""Equipos v4 calcados de las referencias del usuario (estilo plano, esquinas rectas, sombras definidas).
Cada equipo se dibuja en las coordenadas en píxeles de su imagen de referencia y se escala a mm reales.
Devuelve (svg, bornes_mm, (W, H)) igual que svgeq/svghd.
Equipos genéricos: la franja de marca lleva el nombre del canal (MIGUEL | ESQUIT) en lugar del fabricante.
"""
F = "Inter, Arial, sans-serif"

DEFS = """<defs>
 <linearGradient id="rClaro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F1F3F2"/><stop offset="1" stop-color="#E3E6E5"/></linearGradient>
 <linearGradient id="rFrente" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E4E5E3"/><stop offset="0.06" stop-color="#F0F1EF"/><stop offset="0.94" stop-color="#F0F1EF"/><stop offset="1" stop-color="#DADCDA"/></linearGradient>
 <linearGradient id="rOsc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#525664"/><stop offset="0.08" stop-color="#4A4E5B"/><stop offset="1" stop-color="#444855"/></linearGradient>
 <linearGradient id="rAnillo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5F8FA"/><stop offset="1" stop-color="#CBD5DC"/></linearGradient>
 <radialGradient id="rDisco" cx="0.45" cy="0.4" r="0.65"><stop offset="0" stop-color="#F4F8FB"/><stop offset="0.8" stop-color="#E2EAF0"/><stop offset="1" stop-color="#C9D3DB"/></radialGradient>
 <linearGradient id="rPalanca" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3D4240"/><stop offset="1" stop-color="#2E3230"/></linearGradient>
 <linearGradient id="rTeal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#127779"/><stop offset="1" stop-color="#0F6E70"/></linearGradient>
 <linearGradient id="pFranja" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#585E69"/><stop offset="1" stop-color="#3C4048"/></linearGradient>
 <linearGradient id="pSiem" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#44707C"/><stop offset="0.85" stop-color="#47717A"/><stop offset="1" stop-color="#4B6B73"/></linearGradient>
 <linearGradient id="pBanda" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E7685"/><stop offset="1" stop-color="#5E6674"/></linearGradient>
 <linearGradient id="pPuerto" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6A7483"/><stop offset="1" stop-color="#737D8C"/></linearGradient>
 <filter id="sDura" x="-5%" y="-5%" width="110%" height="125%"><feGaussianBlur in="SourceAlpha" stdDeviation="2.2"/><feOffset dy="5"/><feComponentTransfer><feFuncA type="linear" slope="0.38"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sTorn" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="2"/><feOffset dx="1" dy="3"/><feComponentTransfer><feFuncA type="linear" slope="0.35"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sCuerpo" x="-5%" y="-3%" width="112%" height="110%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dx="3" dy="8"/><feComponentTransfer><feFuncA type="linear" slope="0.30"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


def svg_mm(Wpx, Hpx, s, cuerpo, margen=4):
    """Envuelve el dibujo hecho en píxeles de referencia: viewBox en mm, contenido escalado por s (mm/px)."""
    W, H = Wpx * s, Hpx * s
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-margen} {-margen} {W + 2 * margen:.3f} {H + 2 * margen:.3f}" '
            f'width="{W + 2 * margen:.3f}mm" height="{H + 2 * margen:.3f}mm">{DEFS}<g transform="scale({s})">{cuerpo}</g></svg>'), (W, H)


def T(x, y, s, size, color="#1B1F24", peso=400, ancla="middle", rot=0, ls=0):
    r = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{peso}" fill="{color}" '
            f'text-anchor="{ancla}" dominant-baseline="central" letter-spacing="{ls}"{r}>{s}</text>')


def R(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'


def tornillo_cruz(x, y, r):
    """Tornillo de las referencias: anillo claro, disco, cruz recta azul petróleo."""
    a, w = r * 0.6, r * 0.3
    return (f'<g filter="url(#sTorn)"><circle cx="{x}" cy="{y}" r="{r}" fill="url(#rAnillo)" stroke="#B9C4CC" stroke-width="{r * 0.05:.2f}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.8:.2f}" fill="url(#rDisco)" stroke="#C3CDD5" stroke-width="{r * 0.04:.2f}"/></g>'
            f'<rect x="{x - a:.2f}" y="{y - w / 2:.2f}" width="{2 * a:.2f}" height="{w:.2f}" fill="#22495A"/>'
            f'<rect x="{x - w / 2:.2f}" y="{y - a:.2f}" width="{w:.2f}" height="{2 * a:.2f}" fill="#22495A"/>')


def marca_canal(x, y, h, ancho_letras, ancho_caja):
    """Franja de marca con el mismo diseño de la referencia, pero con el nombre del canal (equipo genérico).
    Letras repartidas una por una para que nunca se encimen con la caja."""
    s = []
    for i, l in enumerate("MIGUEL"):
        s.append(T(x + h * 0.4 + i * (ancho_letras - h * 0.8) / 5, y, l, h, "#127779", 700))
    xc = x + ancho_letras + h * 0.25
    s.append(R(xc, y - h * 0.95, ancho_caja, h * 1.9, "url(#rTeal)", 'rx="2"'))
    for i, l in enumerate("ESQUIT"):
        s.append(T(xc + h * 0.9 + i * (ancho_caja - h * 1.8) / 5, y, l, h, "#FFFFFF", 600))
    return "".join(s)


# ============================================================ CONTACTOR (referencia KM0, 602 × 972 px)
def contactor(ref="KM1", px_ancho_mm=45.0):
    Wp, Hp = 602, 972
    s_mm = px_ancho_mm / Wp
    b, c = {}, []
    c.append(f'<g filter="url(#sCuerpo)">{R(6, 0, Wp - 6, Hp, "#ECEEEC")}</g>')
    # bloque superior de potencia
    c.append(R(20, 0, Wp - 34, 175, "url(#rClaro)") + R(20, 0, Wp - 34, 3, "#FFFFFF") + R(Wp - 17, 0, 3, 175, "#CDD1D0"))
    for x, n in zip((113, 303, 497), ("1/L1", "3/L2", "5/L3")):
        c.append(T(x, 30, n, 30, "#3B4148", 700))
        c.append(tornillo_cruz(x, 97, 45))
        b[n] = (x, 97)
    # frente blanco (la franja oscura proyecta sombra sobre él)
    c.append(R(6, 300, Wp - 8, 355, "url(#rFrente)"))
    c.append(marca_canal(20, 357, 17, 158, 158))
    c.append(R(362, 349, 238, 12, "#1F6FBA"))
    # perfil escalonado: línea fina arriba de la ventana y escalón de la placa
    c.append(R(6, 397, Wp - 8, 2, "#D3D6D4") + R(6, 399, Wp - 8, 2, "#FFFFFF") + R(6, 424, Wp - 8, 2, "#D8DBD9"))
    for x0, x1, col in ((188, 237, "#4F4F51"), (237, 283, "#7D7E80"), (283, 343, "#4F4F51"), (343, 386, "#7D7E80"), (386, 443, "#4F4F51")):
        c.append(R(x0, 418, x1 - x0, 86, col))
    c.append(f'<rect x="188" y="418" width="255" height="86" fill="none" stroke="#3A3B3D" stroke-width="3"/>')
    c.append(R(178, 514, 280, 3, "#C9CCCA") + R(178, 517, 280, 2, "#FFFFFF"))
    c.append(R(178, 517, 3, 50, "#C9CCCA") + R(455, 517, 3, 50, "#C9CCCA"))
    c.append(R(6, 565, 175, 3, "#C9CCCA") + R(455, 565, Wp - 457, 3, "#C9CCCA") + R(6, 568, 175, 2, "#FFFFFF") + R(458, 568, Wp - 460, 2, "#FFFFFF"))
    c.append(T(318, 556, f"{ref}", 60, "#0E0F10", 400))
    c.append(R(35, 599, 550, 15, "#1F6FBA"))
    # franjas oscuras de auxiliares y bobina (sobresalen y proyectan sombra)
    for y0, ytx, ytor, nombres in ((172, 284, 225, (("13", "NO"), ("21", "NC"), ("A1", ""))),
                                    (652, 678, 738, (("14", "NO"), ("22", "NC"), ("A2", "")))):
        c.append(f'<g filter="url(#sDura)">{R(6, y0, Wp - 6, 133 if y0 == 172 else 143, "url(#rOsc)")}</g>')
        c.append(R(6, y0, Wp - 6, 2, "#666A77"))
        for x, (num, fn) in zip((233, 378, 515), nombres):
            c.append(tornillo_cruz(x, ytor, 33))
            if fn:
                c.append(f'<text x="{x}" y="{ytx}" font-family="{F}" font-size="28" fill="#FFFFFF" text-anchor="middle" dominant-baseline="central">'
                         f'<tspan font-weight="800">{num}</tspan><tspan font-weight="400" dx="6">{fn}</tspan></text>')
            else:
                c.append(T(x, ytx, num, 28, "#FFFFFF", 800))
            b[num] = (x, ytor)
    # bloque inferior de potencia
    c.append(R(20, 795, Wp - 34, 177, "url(#rClaro)") + R(Wp - 17, 795, 3, 177, "#CDD1D0"))
    for x, n in zip((113, 303, 497), ("2/T1", "4/T2", "6/T3")):
        c.append(tornillo_cruz(x, 877, 45))
        c.append(T(x, 945, n, 30, "#3B4148", 700))
        b[n] = (x, 877)
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ DISYUNTOR 2P (referencia Q1, 482 × 940 px → cuerpo 40…460)
def disyuntor2(ref="Q1", In=20, curva="C", tension="220 - 400 VAC", ancho_mm=36.0):
    x0, x1, Hp = 40, 460, 940
    Wp = x1 - x0
    s_mm = ancho_mm / Wp
    b, c = {}, []
    c.append(f'<g transform="translate({-x0},0)">')
    c.append(f'<g filter="url(#sCuerpo)">{R(x0, 0, Wp, Hp, "#E6E8E6")}</g>')
    # cámaras de bornes
    for y0, h in ((0, 195), (745, 195)):
        c.append(R(x0, y0, Wp, h, "url(#rClaro)"))
    c.append(R(x0, 742, Wp, 6, "#5F6A6C"))  # sombra del frente sobre la cámara inferior
    for xc, n1, n2 in ((150, "1", "2"), (352, "3", "4")):
        c.append(tornillo_cruz(xc, 97, 50) + tornillo_cruz(xc, 840, 50))
        b[n1], b[n2] = (xc - x0, 97), (xc - x0, 840)
    # frente elevado (sombra definida arriba y a la derecha)
    c.append(f'<g filter="url(#sDura)">{R(x0, 192, Wp + 20, 553, "url(#rFrente)")}</g>')
    c.append(R(x0, 192, Wp + 20, 3, "#FFFFFF"))
    c.append(R(255, 0, 2, Hp, "#C7CAC8") + R(257, 0, 2, Hp, "#FAFAFA"))  # separación de polos
    c.append(marca_canal(45, 227, 15, 160, 165) + R(410, 216, 52, 22, "#0F6BB7"))
    c.append(T(45, 292, f"{curva}{In}", 78, "#6F7170", 400, "start", ls=-2))
    c.append(T(212, 262, "2P", 16, "#7B7D7C", 600, "start"))
    c.append(T(48, 332, tension, 19, "#6E706F", 400, "start"))
    # símbolo impreso: 1 * / 3 * con cuchillas y 2 | 4
    for xs, nt, nb in ((318, "1", "2"), (372, "3", "4")):
        c.append(T(xs - 10, 262, nt, 15, "#555", 400) + T(xs - 8, 368, nb, 17, "#555", 400))
        c.append(f'<g stroke="#4A4C4B" stroke-width="2.6" fill="none"><path d="M{xs},262 V300"/>'
                 f'<path d="M{xs - 9},280 l18,14 M{xs + 9},280 l-18,14 M{xs},277 v20"/>'
                 f'<path d="M{xs},343 L{xs - 16},305"/><path d="M{xs},343 V378"/></g>')
    # palanca: barra común con franjas + manijas por polo
    c.append(f'<g filter="url(#sDura)">{R(43, 405, 412, 64, "url(#rPalanca)")}</g>')
    c.append(R(43, 418, 412, 9, "#8E9391") + R(43, 427, 412, 6, "#5E6361") + R(43, 433, 412, 9, "#A5AAA8") + R(43, 442, 412, 5, "#5E6361"))
    for xm in (75, 295):
        c.append(f'<g filter="url(#sDura)">{R(xm, 469, 132, 116, "url(#rPalanca)")}</g>')
        c.append(R(xm, 494, 132, 7, "#9A9C9B") + R(xm, 501, 132, 6, "#5A5D5C") + R(xm, 507, 132, 7, "#B0B3B1"))
    c.append(T(255, 632, ref, 70, "#0E0F10", 400))
    c.append(R(62, 678, 378, 22, "#0270C0"))
    c.append('</g>')
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ CPU 1212C AC/DC/RLY (referencia 1030 × 1290 px, cuerpo 10…1012 × 138…1250)
def _torn_ranura(x, y, r=24):
    d = r * 0.7
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#B4B4B0" stroke="#0A0A0B" stroke-width="3.5"/>'
            f'<line x1="{x - d}" y1="{y - d}" x2="{x + d}" y2="{y + d}" stroke="#050506" stroke-width="9"/>')


def cpu1212(ref="A1", ancho_mm=90.0):
    X0, Y0, X1, Y1 = 10, 138, 1012, 1250
    Wp, Hp = X1 - X0, Y1 - Y0
    s_mm = ancho_mm / Wp
    TX = "#E3E8EF"
    b, c = {}, [f'<g transform="translate({-X0},{-Y0})">']
    c.append("<!--CAPA:Cuerpo-->")
    c.append(f'<g filter="url(#sCuerpo)">{R(X0, Y0, Wp, Hp, "#798394", 'rx="10"')}</g>')
    # franjas horizontales de LEDs (más oscuras) con su arista
    c.append("<!--CAPA:Bandas-->")
    c.append(R(X0, 447, Wp, 50, "url(#pBanda)") + R(X0, 446, Wp, 3, "#485261") + R(X0, 497, Wp, 2, "#8A94A3"))
    c.append(R(X0, 845, Wp, 52, "url(#pBanda)") + R(X0, 843, Wp, 2, "#8A94A3") + R(X0, 895, Wp, 3, "#363D4B"))
    # tapa del puerto (inferior) y contorno de la tapa central
    c.append("<!--CAPA:Tapas-->")
    c.append(R(246, 995, 274, Y1 - 995, "url(#pPuerto)") + R(246, 995, 3, Y1 - 995, "#5B6675") + R(517, 995, 3, Y1 - 995, "#5B6675"))
    c.append(f'<rect x="166" y="392" width="422" height="603" fill="none" stroke="#424C5B" stroke-width="3"/>')
    c.append(R(166, 992, 422, 6, "#3E4757"))
    c.append(R(347, 374, 60, 18, "#3B414C"))
    # SIEMENS
    c.append("<!--CAPA:Marca-->")
    c.append(R(168, 449, 220, 48, "url(#pSiem)") + T(276, 474, "SIEMENS", 34, "#A9ADBA", 700, ls=1))
    # borneras
    xs_sup = [62, 117, 172, 233, 288, 345, 400, 455, 510, 566, 621, 677, 732, 788, 848, 903, 958]
    nom_sup = ["L1", "N", "PE", "L+", "M", "1M", ".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", "2M", "0", "1"]
    c.append("<!--CAPA:Borneras y tornillos-->")
    clv = {".0": "I0.0", ".1": "I0.1", ".2": "I0.2", ".3": "I0.3", ".4": "I0.4", ".5": "I0.5", ".6": "I0.6", ".7": "I0.7", "0": "AI0", "1": "AI1"}
    c.append(f'<g filter="url(#sDura)"><path d="M25,143 H996 V229 Q996,245 980,245 H41 Q25,245 25,229 Z" fill="url(#pFranja)"/></g>')
    for x in (202, 316, 818):
        c.append(R(x - 1, 146, 2.5, 96, "#25282E"))
    for x, n in zip(xs_sup, nom_sup):
        c.append(_torn_ranura(x, 192))
        b[clv.get(n, n)] = (x - X0, 192 - Y0)
    xs_inf = [566, 621, 677, 732, 788, 848, 903, 958]
    nom_inf = ["1L", ".0", ".1", ".2", ".3", "2L", ".4", ".5"]
    clq = {".0": "Q0.0", ".1": "Q0.1", ".2": "Q0.2", ".3": "Q0.3", ".4": "Q0.4", ".5": "Q0.5"}
    c.append(f'<g filter="url(#sDura)"><path d="M527,1163 Q527,1147 543,1147 H981 Q997,1147 997,1163 V1250 H527 Z" fill="url(#pFranja)"/></g>')
    c.append(R(817, 1150, 2.5, 97, "#25282E"))
    for x, n in zip(xs_inf, nom_inf):
        c.append(_torn_ranura(x, 1197))
        b[clq.get(n, n)] = (x - X0, 1197 - Y0)
    c.append("<!--CAPA:Rotulos bornes-->")
    # rótulos superiores (cada número alineado con su tornillo)
    xl = {"L1": 62, "N": 108, "PE": 165, "L+": 225, "M": 287}
    for n, x in xl.items():
        if n != "PE":
            c.append(T(x, 276, n, 21, TX))
    c.append(f'<path d="M150,281 h30 M154,288 h22 M159,295 h12 M165,268 v13" stroke="{TX}" stroke-width="2.6"/>')
    for x, n in zip(xs_sup[5:], nom_sup[5:]):
        c.append(T(x, 276, n, 21, TX))
    br = f'stroke="{TX}" stroke-width="2.6" fill="none"'
    for x0, x1 in ((42, 190), (203, 305), (325, 805), (823, 972)):
        c.append(f'<path d="M{x0},297 V320 H{x1} V297" {br}/>')
    c.append(f'<path d="M108,290 v16" stroke="{TX}" stroke-width="5"/><polygon points="98,304 118,304 108,318" fill="{TX}"/>')
    c.append(f'<path d="M254,300 v16" stroke="{TX}" stroke-width="5"/><polygon points="244,302 264,302 254,288" fill="{TX}"/>')
    c.append(T(400, 305, "DI a", 13, TX) + T(903, 308, "AI", 13, TX))
    c.append(T(108, 346, "120-240VAC", 21, TX) + T(254, 346, "24VDC", 21, TX) + T(566, 346, "24VDC INPUTS", 21, TX))
    c.append(T(893, 346, "ANALOG", 21, TX) + T(893, 376, "INPUTS", 21, TX))
    c.append("<!--CAPA:LEDs-->")
    # LEDs
    led = lambda x, y: R(x - 11, y - 11, 22, 22, "#C1C7D0")
    for x in (58, 98, 138):
        c.append(led(x, 474))
    xs_led = [679 + i * 39.5 for i in range(8)]
    for x in xs_led:
        c.append(led(x, 474))
    for x in xs_led[:6]:      # 1212C: 6 salidas DQ → 6 LEDs
        c.append(led(x, 870))
    c.append("<!--CAPA:Rotulos frente-->")
    for x, n in ((58, "RUN / STOP"), (96, "ERROR"), (134, "MAINT")):
        c.append(T(x, 512, n, 19, TX, 400, "end", rot=-90))
    c.append(f'<path d="M668,520 V545 H968 V520" {br}/>' + "".join(T(683 + i * 39, 527, f".{i}", 17, TX) for i in range(8)) + T(668, 562, "DI a", 13, TX, 400, "start"))
    c.append(T(882, 655, "CPU 1212C", 30, TX, 400) + T(884, 697, "AC/DC/RLY", 30, TX, 400))
    c.append(T(666, 786, "DQ a", 13, TX, 400, "start") + f'<path d="M668,830 V805 H968 V830" {br}/>' + "".join(T(683 + i * 39, 823, f".{i}", 17, TX) for i in range(6)))
    c.append(R(40, 931, 22, 22, "#C1C7D0") + T(78, 942, "LINK", 19, TX, 400, "start"))
    c.append(R(40, 978, 22, 22, "#C1C7D0") + T(78, 989, "Rx/Tx", 19, TX, 400, "start"))
    c.append(T(538, 1037, "DQ a", 13, TX, 400, "start") + T(762, 1040, "RELAY OUTPUTS", 21, TX))
    c.append(f'<path d="M540,1100 V1075 H805 V1100" {br}/><path d="M823,1100 V1075 H985 V1100" {br}/>')
    for x, n in zip(xs_inf, nom_inf):
        c.append(T(x - 8 if n in ("1L", "2L") else x - 10, 1097, n, 18, TX))
    c.append('</g>')
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def a_inkscape(svg, bornes, nombre="equipo"):
    """Convierte un SVG de esta librería en un archivo nativo de Inkscape: unidades mm, una capa por parte
    (<!--CAPA:...--> marca dónde empieza cada una) y una capa oculta 'Bornes' con un punto por borne (id = nombre del borne)."""
    import re
    cab = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" ')
    svg = svg.replace('<svg xmlns="http://www.w3.org/2000/svg" ', cab, 1)
    svg = svg.replace('</defs>', f'</defs><sodipodi:namedview inkscape:document-units="mm" showgrid="false"/>', 1)
    pre, resto = svg.split('<!--CAPA:', 1)
    trans = " ".join(re.findall(r'<g transform="([^"]+)">', pre[pre.index('</sodipodi:namedview>') if '</sodipodi:namedview>' in pre else pre.index('/>', pre.index('<sodipodi:namedview')) + 2:]))
    n_abiertos = len(re.findall(r'<g transform="', pre[pre.index('<sodipodi:namedview'):]))
    pre = re.sub(r'(<g transform="[^"]+">)+$', '', pre)
    resto = re.sub(r'(</g>){%d}</svg>$' % n_abiertos, '', resto)
    partes = re.split(r'<!--CAPA:([^>]+)-->', '<!--CAPA:' + resto)
    out = pre
    for k in range(1, len(partes), 2):
        etiqueta, cuerpo = partes[k], partes[k + 1]
        idc = "capa_" + re.sub(r"\W+", "_", etiqueta.lower())
        out += f'<g inkscape:groupmode="layer" inkscape:label="{etiqueta}" id="{idc}" transform="{trans}">{cuerpo}</g>'
    out += '</svg>'
    pts = "".join(f'<circle id="borne_{k.replace(".", "_").replace("+", "mas")}" cx="{x:.3f}" cy="{y:.3f}" r="0.6" fill="#E11D48"><title>{k}</title></circle>' for k, (x, y) in bornes.items())
    out = out.replace('</svg>', f'<g inkscape:groupmode="layer" inkscape:label="Bornes (puntos de conexión)" id="capa_bornes" style="display:none">{pts}</g></svg>')
    return out

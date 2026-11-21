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


from svgeq import LOGO_POLIS


def logo(x, y, h):
    """Logo vectorial del canal (ME.) con su esquina superior izquierda en (x, y) y altura h."""
    k = h / 394
    return "<g>" + "".join(f'<polygon points="{" ".join(f"{px * k + x:.2f},{py * k + y:.2f}" for px, py in pts)}" fill="{c}"/>'
                           for pts, c in LOGO_POLIS) + "</g>"


def marca_canal(x, y, h, *_):
    """Franja de marca de los equipos genéricos: el logo ME. centrado verticalmente en y (alto ≈ 2,2 h)."""
    H = h * 2.2
    return logo(x, y - H / 2, H)


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
    c.append(R(110, 349, 490, 12, "#1F6FBA"))
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


# ============================================================ DISYUNTOR nP (referencias #1 y #2: 210 px por polo, alto 940 px)
def disyuntor(n=2, In=20, curva="C", ref="Q1", tension="230/400 VAC", polo_mm=18.0):
    P, Hp = 210, 940
    Wp = P * n
    s_mm = polo_mm / P
    b, c = {}, []
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#E6E8E6")}</g>')
    for y0, h in ((0, 195), (745, 195)):
        c.append(R(0, y0, Wp, h, "url(#rClaro)"))
    c.append(R(0, 742, Wp, 6, "#5F6A6C"))                       # sombra del frente sobre la cámara inferior
    for i in range(n):
        xc = P * i + 108
        c.append(tornillo_cruz(xc, 97, 50) + tornillo_cruz(xc, 840, 50))
        b[str(2 * i + 1)], b[str(2 * i + 2)] = (xc, 97), (xc, 840)
    # frente elevado con sombra definida
    c.append(f'<g filter="url(#sDura)">{R(0, 192, Wp, 553, "url(#rFrente)")}</g>' + R(0, 192, Wp, 3, "#FFFFFF"))
    for i in range(1, n):                                         # separación de polos
        c.append(R(P * i - 1, 0, 2, Hp, "#C7CAC8") + R(P * i + 1, 0, 2, Hp, "#FAFAFA"))
    c.append(marca_canal(6, 227, 15) + R(Wp - 52, 216, 50, 22, "#0F6BB7"))
    grande = 78 if n > 1 else 60
    c.append(T(6, 292, f"{curva}{In}", grande, "#6F7170", 400, "start", ls=-2))
    if n > 1:
        c.append(T(6 + grande * 2.15, 262, f"{n}P", 16, "#7B7D7C", 600, "start"))
    c.append(T(8, 332 if n > 1 else 328, tension, 19 if n > 1 else 15, "#6E706F", 400, "start"))
    # símbolo impreso por polo (× = disyuntor, cuchilla abierta)
    for i in range(n):
        xs = Wp - 30 - (n - 1 - i) * 54
        c.append(T(xs - 10, 262, str(2 * i + 1), 15, "#555") + T(xs - 9, 368, str(2 * i + 2), 17, "#555"))
        c.append(f'<g stroke="#4A4C4B" stroke-width="2.6" fill="none"><path d="M{xs},262 V300"/>'
                 f'<path d="M{xs - 9},280 l18,14 M{xs + 9},280 l-18,14"/>'
                 f'<path d="M{xs},343 L{xs - 16},305"/><path d="M{xs},343 V378"/></g>')
    if n > 1:
        c.append(f'<path d="M{Wp - 30 - (n - 1) * 54 - 8},323 H{Wp - 38}" stroke="#4A4C4B" stroke-width="2" stroke-dasharray="5 4"/>')
    # palanca: barra común + manija por polo
    c.append(f'<g filter="url(#sDura)">{R(3, 405, Wp - 8, 64, "url(#rPalanca)")}</g>')
    c.append(R(3, 418, Wp - 8, 9, "#8E9391") + R(3, 427, Wp - 8, 6, "#5E6361") + R(3, 433, Wp - 8, 9, "#A5AAA8") + R(3, 442, Wp - 8, 5, "#5E6361"))
    for i in range(n):
        xm = P * i + 37
        c.append(f'<g filter="url(#sDura)">{R(xm, 469, 132, 116, "url(#rPalanca)")}</g>')
        c.append(R(xm, 494, 132, 7, "#9A9C9B") + R(xm, 501, 132, 6, "#5A5D5C") + R(xm, 507, 132, 7, "#B0B3B1"))
    c.append(T(Wp / 2, 632, ref, 70 if n > 1 else 56, "#0E0F10", 400))
    c.append(R(22, 678, Wp - 44, 22, "#0270C0"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def disyuntor2(ref="Q1", In=20, curva="C", tension="230/400 VAC"):
    return disyuntor(2, In, curva, ref, tension)


# ============================================================ GUARDAMOTOR (referencia #3, cuerpo 372 × 735 px, blanco)
def guardamotor(ref="QM1", rango=(22, 32), ajuste=24.3, ancho_mm=45.0):
    Wp, Hp = 372, 735
    s_mm = ancho_mm / Wp
    b, c = {}, []
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#ECEEEC")}</g>')
    # mordazas de los bornes (asoman arriba y abajo) y cámaras
    for x in (0, 122, 232, 352):
        c.append(R(x, -14, 20, 18, "#3A3B3E") + R(x, Hp - 4, 20, 18, "#3A3B3E"))
    c.append(R(0, 0, Wp, 125, "url(#rClaro)") + R(0, 610, Wp, 125, "url(#rClaro)"))
    xs = (69, 183, 282)
    for x, n1, n2 in zip(xs, ("1/L1", "3/L2", "5/L3"), ("2/T1", "4/T2", "6/T3")):
        c.append(T(x, 16, n1, 17, "#4A505A", 700) + T(x, 712, n2, 17, "#4A505A", 700))
        c.append(tornillo_cruz(x, 62, 30) + tornillo_cruz(x, 668, 30))
        b[n1], b[n2] = (x, 62), (x, 668)
    # línea de separación con los topes del puente de cuchillas
    c.append(R(0, 125, Wp, 3, "#C3C7C9") + R(0, 128, Wp, 2, "#FFFFFF") + R(0, 607, Wp, 3, "#C3C7C9"))
    c.append(R(117, 120, 25, 16, "#3A3B3E") + R(237, 120, 25, 16, "#3A3B3E"))
    # frente elevado
    c.append(f'<g filter="url(#sDura)">{R(8, 150, Wp - 16, 450, "url(#rFrente)")}</g>' + R(8, 150, Wp - 16, 3, "#FFFFFF"))
    # clase de disparo
    c.append(f'<path d="M36,215 v-12 h8 v-6 h8" stroke="#3B3F46" stroke-width="2.4" fill="none"/>' + T(64, 207, "CLASS 10", 17, "#3B3F46", 500, "start"))
    c.append(R(28, 222, 32, 6, "#2E3138") + R(150, 222, 32, 6, "#2E3138"))
    # dial de ajuste térmico (escala del rango)
    cx, cy, r = 77, 290, 36
    import math
    a0, a1 = 215, -35
    for k in range(5):
        ang = math.radians(a0 + (a1 - a0) * k / 4)
        x1, y1 = cx + (r + 4) * math.cos(ang), cy - (r + 4) * math.sin(ang)
        x2, y2 = cx + (r + 12) * math.cos(ang), cy - (r + 12) * math.sin(ang)
        c.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#3B3F46" stroke-width="2"/>')
    lo, hi = rango
    for k, v in ((0, lo), (2, (lo + hi) / 2), (4, hi)):
        ang = math.radians(a0 + (a1 - a0) * k / 4)
        c.append(T(cx + (r + 24) * math.cos(ang), cy - (r + 24) * math.sin(ang), f"{v:g}", 13, "#3B3F46", 600))
    c.append(f'<g filter="url(#sTorn)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#FAFAF8" stroke="#C9CBCB" stroke-width="2"/></g>')
    c.append(R(cx - 22, cy - 7, 44, 14, "#BFC3C6") + R(cx - 7, cy - 22, 14, 44, "#BFC3C6"))
    angp = math.radians(a0 + (a1 - a0) * (ajuste - lo) / (hi - lo))
    c.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + (r - 4) * math.cos(angp):.1f}" y2="{cy - (r - 4) * math.sin(angp):.1f}" stroke="#D92D20" stroke-width="4"/>')
    # ventana de rango
    c.append(R(200, 205, 142, 46, "#F7F8F6", 'stroke="#80858C" stroke-width="2"') + T(271, 228, f"{lo:g}–{hi:g} A", 22, "#2E3138", 700))
    c.append(T(271, 280, f"-{ref}", 32, "#1B1F24", 700))
    # TRIP, I>> y TEST
    c.append(f'<path d="M150,370 Q185,335 225,322" stroke="#3B3F46" stroke-width="6" fill="none"/>' + T(176, 336, "TRIP", 13, "#3B3F46", 700, rot=-30))
    c.append(R(20, 400, 26, 20, "none", 'stroke="#3B3F46" stroke-width="2"') + T(33, 410, "I>", 11, "#3B3F46", 700))
    c.append(T(54, 410, f"{round(hi * 13 / 10) * 10:g} A" if False else f"{int(hi * 13)} A", 18, "#3B3F46", 600, "start"))
    c.append(T(20, 438, "TEST", 13, "#3B3F46", 700, "start") + R(68, 428, 56, 22, "#394052"))
    c.append(f'<path d="M22,452 h40" stroke="#3B3F46" stroke-width="2"/>')
    # mando giratorio (posición OFF/O) y marcas
    c.append(R(300, 318, 5, 20, "#3B3F46") + T(302, 352, "ON", 11, "#3B3F46", 700))
    c.append(f'<g filter="url(#sDura)"><circle cx="247" cy="465" r="88" fill="#3A3936"/></g>')
    c.append(f'<g filter="url(#sDura)"><rect x="168" y="442" width="158" height="48" fill="#2A2927"/></g>')
    c.append(R(122, 445, 48, 42, "#E7E8EA") + R(122, 445, 48, 6, "#FFFFFF"))
    c.append(f'<circle cx="247" cy="465" r="88" fill="none" stroke="#56544F" stroke-width="2"/>')
    c.append(logo(16, 480, 34))
    c.append(f'<circle cx="148" cy="530" r="9" fill="none" stroke="#3B3F46" stroke-width="2.4"/>' + T(165, 530, "O", 12, "#3B3F46", 700, "start") + T(148, 552, "OFF", 11, "#3B3F46", 700))
    c.append(R(20, 582, Wp - 40, 10, "#0270C0"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ RELÉ TÉRMICO (referencia #22, cuerpo 685 × 780 px)
def rele_termico(ref="F2", rango=(23, 32), ajuste=24.3, ancho_mm=45.0):
    import math
    Wp, Hp = 685, 780
    s_mm = ancho_mm / Wp
    b, c = {}, []
    # pines rígidos que entran en 2/T1 4/T2 6/T3 del contactor
    for x, n in zip((140, 342, 545), ("1/L1", "3/L2", "5/L3")):
        c.append(R(x - 22, -30, 44, 60, "#B9BEC3", 'stroke="#8D949B" stroke-width="2"') + R(x - 22, -30, 10, 60, "#DADDE0"))
        c.append(T(x + 30, -12, n, 30, "#3B4148", 700, "start"))
        b[n] = (x, -10)
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#ECEEEC")}</g>')
    c.append(R(0, 0, Wp, 92, "url(#rClaro)"))
    c.append(marca_canal(20, 46, 17) + R(430, 39, 235, 16, "#1F6FBA"))
    # frente elevado
    c.append(f'<g filter="url(#sDura)">{R(0, 92, Wp, 345, "url(#rFrente)")}</g>' + R(0, 92, Wp, 3, "#FFFFFF"))
    c.append(R(42, 138, 336, 212, "#F3F4F2", 'stroke="#BFC3C1" stroke-width="3"'))
    c.append(R(42, 290, 72, 60, "#D7D9D7") + R(220, 290, 158, 60, "#D7D9D7"))
    c.append(f'<polygon points="60,180 80,148 100,180" fill="#5B5F62"/>' + T(330, 158, "TEST", 26, "#4A4F55", 700))
    c.append(T(78, 330, "TEST", 18, "#5B5F62", 700))
    # dial azul de ajuste
    cx, cy, r = 150, 235, 68
    lo, hi = rango
    c.append(f'<g filter="url(#sTorn)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#1F67C4"/></g>')
    for k, v in enumerate((lo, round((lo + hi) / 2), hi)):
        ang = math.radians(150 - k * 60)
        c.append(T(cx + (r - 16) * math.cos(ang), cy - (r - 16) * math.sin(ang), f"{v:g}", 15, "#FFFFFF", 700))
    c.append(R(cx - 34, cy - 9, 68, 18, "#24237F") + R(cx - 9, cy - 34, 18, 68, "#24237F"))
    angp = math.radians(150 - 120 * (ajuste - lo) / (hi - lo))
    c.append(f'<line x1="{cx + 30 * math.cos(angp):.1f}" y1="{cy - 30 * math.sin(angp):.1f}" x2="{cx + (r + 8) * math.cos(angp):.1f}" y2="{cy - (r + 8) * math.sin(angp):.1f}" stroke="#FFFFFF" stroke-width="5"/>')
    c.append(R(cx - 22, 302, 44, 14, "#2E3138"))
    c.append(T(620, 148, f"-{ref}", 58, "#0E0F10", 400))
    c.append(T(540, 210, "STOP", 26, "#4A4F55", 700) + T(642, 210, "RESET", 26, "#4A4F55", 700))
    c.append(f'<g filter="url(#sDura)"><rect x="410" y="240" width="270" height="132" fill="#3F4042"/></g>')
    c.append(f'<circle cx="477" cy="306" r="56" fill="#C7202D"/><circle cx="477" cy="306" r="40" fill="#E8331F"/><circle cx="477" cy="306" r="18" fill="#FF6A13"/>')
    c.append(f'<circle cx="610" cy="306" r="54" fill="#1F67C4"/>' + R(568, 298, 84, 16, "#24237F") + R(602, 264, 16, 84, "#24237F") + T(632, 290, "H", 15, "#FFFFFF", 700) + T(588, 322, "A", 15, "#FFFFFF", 700))
    c.append(T(342, 400, f"{lo:g}–{hi:g} A · CLASS 10A", 20, "#4A4F55", 700))
    # contactos auxiliares
    c.append(R(0, 437, Wp, 150, "url(#rClaro)"))
    for x, n in ((105, "98"), (260, "97"), (425, "96"), (580, "95")):
        c.append(T(x, 465, n, 38, "#4A4F55", 700) + tornillo_cruz(x, 535, 34))
        b[n] = (x, 535)
    c.append(T(182, 497, "NO", 34, "#4A4F55", 700) + T(502, 497, "NC", 34, "#4A4F55", 700))
    # salida de potencia (bloque más angosto, sombreado por el de arriba)
    c.append(R(25, 587, Wp - 60, 193, "url(#rClaro)") + R(25, 587, Wp - 60, 8, "#8D9497"))
    for x, n in zip((140, 342, 545), ("2/T1", "4/T2", "6/T3")):
        c.append(tornillo_cruz(x, 672, 50) + T(x, 752, n, 30, "#4A4F55", 700))
        b[n] = (x, 672)
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ BASE OCTAL + RELÉ / TEMPORIZADOR (referencia #6, cuerpo 490 × 720 px)
def _base_octal(c, b, Wp):
    """Base de 8 pines: arriba 3 4 5 6, abajo 2 1 8 7 (números fuera del cuerpo para que no se encimen)."""
    xs = [62 + i * 122 for i in range(4)]
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 40, Wp, 700, "#D9DBDC")}</g>')
    for y0 in (40, 630):
        c.append(R(0, y0, Wp, 110, "url(#rClaro)"))
        for k in range(1, 4):
            c.append(R(k * 122 + 1, y0 + 6, 3, 98, "#B9BDC0"))
    for x, nt, nb in zip(xs, ("3", "4", "5", "6"), ("2", "1", "8", "7")):
        c.append(T(x, 10, nt, 40, "#111111", 500) + T(x, 778, nb, 40, "#111111", 500))
        c.append(tornillo_cruz(x, 92, 38) + tornillo_cruz(x, 685, 38))
        b[nt], b[nb] = (x, 92), (x, 685)
    return xs


def rele_8p(ref="KA1", bobina="240 VAC", tipo="rele", ancho_mm=38.0):
    if tipo == "timer":
        return temporizador(ref, ancho_mm=ancho_mm)
    Wp = 490
    s_mm = ancho_mm / Wp
    b, c = {}, []
    _base_octal(c, b, Wp)
    # relé enchufado: cuerpo transparente con el frente rotulado
    c.append(f'<g filter="url(#sDura)">{R(20, 150, Wp - 40, 480, "url(#rFrente)", 'stroke="#AEB3B6" stroke-width="3"')}</g>')
    c.append(logo(40, 172, 40) + R(120, 186, 340, 12, "#1F6FBA"))
    c.append(T(Wp / 2, 248, f"-{ref}", 54, "#0E0F10", 400))
    c.append(T(Wp / 2, 298, f"Bobina {bobina}", 24, "#4A4F55", 600) + T(Wp / 2, 328, "2 CO · 10 A 250 VAC", 22, "#6E706F", 600))
    # esquema impreso del patillaje (bobina 2-7, comunes 1 y 8)
    g = '<g stroke="#3B3F46" stroke-width="3" fill="none">'
    g += '<rect x="66" y="430" width="56" height="34"/><path d="M94,410 V430 M94,464 V484"/>'
    for xc, nc, na, com in ((215, "4", "3", "1"), (360, "5", "6", "8")):
        g += f'<path d="M{xc},500 V470 L{xc - 22},420"/><path d="M{xc - 30},405 V420 H{xc - 18}"/><path d="M{xc + 30},405 V432 H{xc + 6}"/>'
    g += '</g>'
    c.append(g)
    for xc, nc, na, com in ((215, "4", "3", "1"), (360, "5", "6", "8")):
        c.append(T(xc - 30, 390, nc, 20, "#3B3F46", 700) + T(xc + 30, 390, na, 20, "#3B3F46", 700) + T(xc + 18, 505, com, 20, "#3B3F46", 700))
    c.append(T(76, 400, "2", 20, "#3B3F46", 700) + T(76, 494, "7", 20, "#3B3F46", 700))
    c.append(f'<rect x="388" y="560" width="54" height="30" fill="#2BD14A" stroke="#1E9E35" stroke-width="2"/>' + T(415, 610, "LED", 16, "#4A4F55", 700))
    c.append(R(60, 556, 90, 36, "#F28C28", 'stroke="#C4661A" stroke-width="2"') + T(105, 610, "TEST", 16, "#4A4F55", 700))
    svg, WH = svg_mm(Wp, 800, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def temporizador(ref="KT1", escala="MIN", ancho_mm=38.0):
    import math
    Wp = 490
    s_mm = ancho_mm / Wp
    b, c = {}, []
    _base_octal(c, b, Wp)
    c.append(f'<g filter="url(#sDura)">{R(0, 150, Wp, 480, "#E9EAEA", 'stroke="#9EA3A6" stroke-width="3"')}</g>')
    c.append(R(10, 160, Wp - 20, 460, "#F4F5F4"))
    c.append(T(70, 196, "POWER", 22, "#3B3F46", 600) + f'<circle cx="70" cy="226" r="11" fill="#5D6062"/>')
    c.append(T(422, 196, "UP", 22, "#3B3F46", 600) + f'<circle cx="440" cy="226" r="11" fill="#5D6062"/>')
    c.append(T(Wp / 2, 196, f"-{ref}", 40, "#0E0F10", 400))
    cx, cy = 232, 405
    c.append(f'<g filter="url(#sDura)"><circle cx="{cx}" cy="{cy}" r="172" fill="#C9CBCC" stroke="#8E9295" stroke-width="3"/></g>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="#2D2D2F"/>')
    for k in range(51):
        ang = math.radians(225 - 270 * k / 50)
        L = 16 if k % 10 == 0 else 9
        c.append(f'<line x1="{cx + 146 * math.cos(ang):.1f}" y1="{cy - 146 * math.sin(ang):.1f}" x2="{cx + (146 - L) * math.cos(ang):.1f}" y2="{cy - (146 - L) * math.sin(ang):.1f}" stroke="#FFFFFF" stroke-width="2"/>')
    for k in range(6):
        ang = math.radians(225 - 270 * k / 5)
        c.append(T(cx + 112 * math.cos(ang), cy - 112 * math.sin(ang), "0" if k == 0 else f".{k}", 20, "#FFFFFF", 600))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="#D8DADB" stroke="#A9ADB0" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="42" fill="#BFC2C4"/>')
    ang = math.radians(225 - 270 * 0.3)
    c.append(f'<line x1="{cx + 60 * math.cos(ang):.1f}" y1="{cy - 60 * math.sin(ang):.1f}" x2="{cx + 140 * math.cos(ang):.1f}" y2="{cy - 140 * math.sin(ang):.1f}" stroke="#E11D2E" stroke-width="7"/>')
    c.append(R(cx - 36, 538, 72, 30, "#E6E7E8", 'stroke="#8E9295" stroke-width="2"') + T(cx, 553, escala, 18, "#2D2D2F", 700))
    c.append(T(430, 545, "MODE", 22, "#3B3F46", 600) + f'<circle cx="60" cy="568" r="20" fill="#2B2B2D"/>' + R(52, 566, 16, 4, "#777"))
    c.append(logo(380, 588, 26))
    svg, WH = svg_mm(Wp, 800, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ OPERADORES DE PUERTA 22 mm (referencias #8 a #11)
def bloque(n1="3", n2="4", nc=False, piloto=False, alto_mm=30.0):
    """Vista trasera del bloque de contacto (o portalámparas): punto de conexión real. 300 × 370 px."""
    Wp, Hp = 300, 370
    s_mm = alto_mm / Hp
    b, c = {}, []
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#26272A")}</g>' + R(0, 0, Wp, 4, "#3C3E42"))
    c.append(R(0, 160, 30, 50, "#8F9396") + f'<circle cx="34" cy="185" r="22" fill="#B4B8BB" stroke="#6D7174" stroke-width="2"/>'
             + R(22, 182, 24, 6, "#6D7174") + R(31, 173, 6, 24, "#6D7174"))
    for y, n in ((72, n1), (290, n2)):
        c.append(f'<circle cx="100" cy="{y}" r="26" fill="#A3A6A8" stroke="#7B7E81" stroke-width="2"/>' + T(150, y, n, 26, "#FFFFFF", 600, rot=90))
        b[n] = (100, y)
    if piloto:
        c.append(R(78, 150, 48, 70, "#F2F2F0") + T(150, 185, "LED", 22, "#FFFFFF", 600, rot=90))
    else:
        col = "#C8202B" if nc else "#1F7A3A"
        c.append(R(78, 150, 48, 70, col) + T(150, 185, "NC" if nc else "NO", 24, "#FFFFFF", 700, rot=90))
        c.append(f'<path d="M180,105 A80,80 0 0 1 180,265" fill="{col}" stroke="#0E0F10" stroke-width="14"/>')
    c.append(R(258, 115, 38, 130, "#9DA1A4") + f'<circle cx="277" cy="180" r="8" fill="#0E0F10"/>')
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def _bisel_puerta(c, Wp=300):
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Wp, "#1E1F21")}</g>' + R(0, 0, Wp, 5, "#3A3B3E") + R(0, Wp - 6, Wp, 6, "#121314"))


def pulsador(color="verde", simbolo="I", ref="S1", ancho_mm=30.0):
    """Frente 2D del pulsador rasante de 22 mm: bisel negro, aro cromado, cabeza de color. I = marcha, O = paro (IEC 60417)."""
    Wp = 300
    s_mm = ancho_mm / Wp
    col = {"verde": ("#3FAE3A", "#2F8C2C"), "rojo": ("#D7262C", "#A51D22"), "negro": ("#2B2C2E", "#161718"), "amarillo": ("#F2C230", "#C99A12"), "azul": ("#1F67C4", "#164E96"), "blanco": ("#F4F4F2", "#C9CACA")}[color]
    c = []
    _bisel_puerta(c)
    c.append(f'<g filter="url(#sDura)"><circle cx="150" cy="150" r="128" fill="#D9DCDE" stroke="#B3B7BA" stroke-width="3"/></g>')
    c.append(f'<circle cx="150" cy="150" r="98" fill="{col[0]}" stroke="{col[1]}" stroke-width="4"/>')
    if simbolo == "I":
        c.append(R(143, 112, 14, 76, "#E9F1E8", 'opacity="0.85"'))
    elif simbolo == "O":
        c.append(f'<circle cx="150" cy="150" r="36" fill="none" stroke="#F4E9E9" stroke-width="12" opacity="0.85"/>')
    c.append(T(150, 330, f"-{ref}", 34, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, 350, s_mm, "".join(c))
    return svg, {}, WH


def emergencia(ref="S3", ancho_mm=40.0):
    """Frente del paro de emergencia: placa amarilla con leyenda y hongo rojo con flechas de desbloqueo por giro."""
    Wp = 400
    s_mm = ancho_mm / Wp
    c = [f'<g filter="url(#sCuerpo)"><circle cx="200" cy="200" r="196" fill="#F5C518" stroke="#C99A12" stroke-width="4"/></g>']
    c.append('<defs><path id="arcoEm" d="M58,200 A142,142 0 0 1 342,200"/><path id="arcoEm2" d="M70,215 A130,130 0 0 0 330,215"/></defs>')
    c.append(f'<text font-family="{F}" font-size="30" font-weight="800" fill="#1B1F24" letter-spacing="3"><textPath href="#arcoEm" startOffset="50%" text-anchor="middle">EMERGENCIA</textPath></text>')
    c.append(f'<g filter="url(#sDura)"><circle cx="200" cy="200" r="118" fill="#B81D24"/></g><circle cx="200" cy="200" r="104" fill="#D7262C"/>')
    c.append(f'<path d="M150,150 A70,70 0 0 1 250,150" stroke="#FFFFFF" stroke-width="7" fill="none" opacity="0.8"/><polygon points="250,150 236,138 262,132" fill="#FFFFFF" opacity="0.8"/>')
    c.append(T(200, 425, f"-{ref}", 34, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, 445, s_mm, "".join(c))
    return svg, {}, WH


def selector(ref="S2", pos=0, ancho_mm=30.0):
    """Frente del selector de 2 posiciones (referencia #8): perilla negra con maneta y franja blanca; 0 a la izquierda, 1 a la derecha."""
    Wp = 300
    s_mm = ancho_mm / Wp
    c = []
    _bisel_puerta(c)
    c.append(T(55, 40, "0", 30, "#FFFFFF", 700) + T(245, 40, "1", 30, "#FFFFFF", 700))
    ang = -45 if pos == 0 else 45
    c.append(f'<g filter="url(#sDura)"><circle cx="150" cy="160" r="118" fill="#D9DCDE" stroke="#B3B7BA" stroke-width="3"/></g>')
    c.append(f'<circle cx="150" cy="160" r="104" fill="#232425"/><circle cx="150" cy="160" r="78" fill="#2C2D2F"/>')
    c.append(f'<g transform="rotate({ang} 150 160)"><g filter="url(#sDura)"><rect x="118" y="44" width="64" height="232" fill="#1A1B1C"/></g>'
             f'<rect x="124" y="50" width="4" height="220" fill="#8A8D90"/><rect x="172" y="50" width="4" height="220" fill="#8A8D90"/>'
             f'<rect x="141" y="56" width="18" height="100" rx="9" fill="#F4F4F2"/></g>')
    c.append(T(150, 330, f"-{ref}", 34, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, 350, s_mm, "".join(c))
    return svg, {}, WH


def piloto(color="verde", ref="H1", encendido=True, ancho_mm=30.0):
    """Frente del piloto (referencia #11): aro gris y difusor con brillo del color."""
    Wp = 300
    s_mm = ancho_mm / Wp
    col = {"verde": "#55F000", "rojo": "#FF2A1F", "amarillo": "#FFC400", "azul": "#2F7BFF", "blanco": "#FFFFFF"}[color]
    c = [f'<defs><radialGradient id="glow_{color}" cx="0.5" cy="0.5" r="0.5"><stop offset="0.55" stop-color="{col}"/>'
         f'<stop offset="0.85" stop-color="{col}" stop-opacity="0.35"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>']
    _bisel_puerta(c)
    c.append(f'<g filter="url(#sDura)"><circle cx="150" cy="150" r="128" fill="#F2F3F4" stroke="#8A8E92" stroke-width="5"/></g>')
    c.append(f'<circle cx="150" cy="150" r="104" fill="url(#glow_{color})" opacity="{1 if encendido else 0.35}"/>')
    c.append(T(150, 330, f"-{ref}", 34, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, 350, s_mm, "".join(c))
    return svg, {}, WH


# ============================================================ SENSORES M18 (referencia #12, vista lateral)
def sensor(tipo="inductivo", ref="B1", salida="PNP · NO", largo_mm=78.0):
    """Sensor cilíndrico M18 de 3 hilos: cable con BN (+), BK (salida), BU (−) y puntera en cada punta (IEC 60947-5-2)."""
    Wp, Hp = 780, 330
    s_mm = largo_mm / Wp
    cara = {"inductivo": ("#3D7FD9", "#2E64B0"), "capacitivo": ("#F08A24", "#C4661A"), "optico": ("#C8202B", "#8E1820")}[tipo]
    b, c = {}, []
    c.append('<defs><linearGradient id="sCil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E9297"/><stop offset="0.25" stop-color="#F4F5F6"/>'
             '<stop offset="0.5" stop-color="#C9CCCF"/><stop offset="1" stop-color="#7C8086"/></linearGradient>'
             '<linearGradient id="sNegro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3B3D"/><stop offset="0.3" stop-color="#18191A"/><stop offset="1" stop-color="#0B0B0C"/></linearGradient></defs>')
    # hilos con puntera y marcador
    for y, col, n, bor in ((150, "#7B5236", "BN", "+"), (200, "#1A1A1A", "BK", "out"), (250, "#3F86D6", "BU", "−")):
        c.append(f'<path d="M210,{200 + (y - 200) * 0.25} C150,{200 + (y - 200) * 0.25} 140,{y} 70,{y}" stroke="{col}" stroke-width="13" fill="none"/>')
        c.append(R(14, y - 9, 56, 18, "#3EA1F0", 'stroke="#2378C0" stroke-width="2"') + R(0, y - 3, 16, 6, "#B9BEC3"))
        c.append(T(98, y - 22, n, 19, "#1B1F24", 700))
        b[n] = (2, y)
    # prensaestopa y cuerpo roscado
    c.append(f'<g filter="url(#sDura)">{R(205, 168, 75, 64, "url(#sNegro)")}</g>')
    c.append(f'<g filter="url(#sDura)">{R(280, 150, 340, 100, "url(#sCil)")}</g>')
    for x in range(352, 618, 7):
        c.append(f'<line x1="{x}" y1="152" x2="{x - 3}" y2="248" stroke="#5E6268" stroke-width="1.6" opacity="0.55"/>')
    c.append(R(345, 150, 18, 100, "#3D7FD9" if tipo != "capacitivo" else "#F08A24"))
    if tipo == "capacitivo":
        c.append(f'<circle cx="310" cy="200" r="13" fill="#D9DCDE" stroke="#6D7174" stroke-width="2"/>' + R(303, 198, 14, 4, "#3A3B3D"))
    c.append(R(298, 162, 12, 10, "#F2C230" if tipo != "optico" else "#F2C230"))
    # tuercas M18 (perfil hexagonal) y arandela
    for x0, w in ((605, 30), (640, 48)):
        c.append(f'<g filter="url(#sDura)"><polygon points="{x0},125 {x0 + w},120 {x0 + w},280 {x0},275" fill="url(#sCil)" stroke="#55595F" stroke-width="2"/></g>')
        c.append(R(x0, 160, w, 3, "#55595F") + R(x0, 238, w, 3, "#55595F"))
    c.append(R(688, 140, 22, 120, "url(#sCil)"))
    c.append(f'<g filter="url(#sDura)">{R(710, 155, 62, 90, cara[0])}</g>' + R(764, 155, 8, 90, cara[1]))
    if tipo == "optico":
        c.append(f'<circle cx="741" cy="182" r="11" fill="#FF7A6E"/><circle cx="741" cy="218" r="11" fill="#2B2C2E"/>')
    c.append(R(560, 132, 3, 3, "none"))
    c.append(R(330, 36, 230, 54, "#3A3F47", 'rx="8"') + T(445, 63, salida, 28, "#FFFFFF", 700))
    c.append(f'<circle cx="610" cy="63" r="12" fill="#2BD14A"/>' + T(630, 63, "LED", 18, "#3A3F47", 700, "start"))
    c.append(T(445, 300, f"-{ref}  ·  M18 · 10–30 VDC", 24, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ FLOTADOR (referencia #13)
def flotador(ref="S5", alto_mm=150.0):
    Wp, Hp = 420, 700
    s_mm = alto_mm / Hp
    b, c = {}, []
    # cable y sus 3 hilos con puntera
    c.append(f'<path d="M210,600 C210,680 120,690 90,600 L70,330" stroke="#1E1F21" stroke-width="22" fill="none" stroke-linecap="round"/>')
    for y, col, n in ((150, "#7B5236", "C"), (205, "#1A1A1A", "NA"), (260, "#3F86D6", "NC")):
        c.append(f'<path d="M70,330 C68,{y + 60} 64,{y} 50,{y}" stroke="{col}" stroke-width="9" fill="none"/>')
        c.append(R(14, y - 8, 38, 16, "#3EA1F0", 'stroke="#2378C0" stroke-width="2"') + R(0, y - 3, 16, 6, "#B9BEC3") + T(33, y - 22, n, 18, "#1B1F24", 700))
        b[n] = (2, y)
    # cuerpo tipo pera
    c.append(f'<g filter="url(#sCuerpo)"><path d="M130,40 H360 Q390,40 390,70 V440 Q390,470 360,470 H130 Q100,470 100,440 V70 Q100,40 130,40 Z" fill="#D7262C"/></g>')
    c.append(f'<path d="M140,55 H350 Q375,55 375,80 V430 Q375,455 350,455 H140 Q115,455 115,430 V80 Q115,55 140,55 Z" fill="#2F6FD0"/>')
    c.append(f'<path d="M165,95 H325 Q345,95 345,115 V355 Q345,375 325,375 H165 Q145,375 145,355 V115 Q145,95 165,95 Z" fill="#5AA5EE"/>')
    c.append(logo(185, 395, 40))
    c.append(f'<path d="M205,470 H285 L270,560 H220 Z" fill="#D7262C"/>' + R(232, 492, 26, 26, "#2F6FD0") + R(205, 560, 80, 40, "#1E1F21"))
    c.append(T(245, 655, f"-{ref}", 34, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ MOTOR (referencia #14, vista desde el ventilador)
def motor(ref="M1", placa="10 hp · 230 V · 24,3 A · 1760 rpm", ancho_mm=260.0):
    import math
    Wp, Hp = 700, 640
    s_mm = ancho_mm / Wp
    c = ['<defs><radialGradient id="mAz" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#4A8BE0"/><stop offset="1" stop-color="#1F5FB8"/></radialGradient></defs>']
    cx, cy = 400, 300
    # patas
    c.append(f'<g filter="url(#sCuerpo)"><polygon points="215,520 295,470 505,470 585,520 610,590 190,590" fill="#2A67C2"/></g>')
    c.append(R(180, 585, 440, 24, "#1F5AAE") + R(212, 560, 40, 16, "#173F7C") + R(548, 560, 40, 16, "#173F7C"))
    # carcasa con aletas
    c.append(f'<g filter="url(#sCuerpo)"><circle cx="{cx}" cy="{cy}" r="250" fill="url(#mAz)"/></g>')
    for k in range(36):
        a = math.radians(k * 10)
        c.append(f'<line x1="{cx + 232 * math.cos(a):.1f}" y1="{cy + 232 * math.sin(a):.1f}" x2="{cx + 262 * math.cos(a):.1f}" y2="{cy + 262 * math.sin(a):.1f}" stroke="#1B4F9C" stroke-width="9"/>')
    # cubierta del ventilador con rejilla
    c.append(f'<circle cx="{cx}" cy="{cy}" r="205" fill="#2C6CC8" stroke="#1B4F9C" stroke-width="6"/>')
    for k in range(12):
        a0 = math.radians(k * 30 + 6)
        a1 = math.radians(k * 30 + 24)
        c.append(f'<path d="M{cx + 95 * math.cos(a0):.1f},{cy + 95 * math.sin(a0):.1f} L{cx + 190 * math.cos(a0):.1f},{cy + 190 * math.sin(a0):.1f} '
                 f'A190,190 0 0 1 {cx + 190 * math.cos(a1):.1f},{cy + 190 * math.sin(a1):.1f} L{cx + 95 * math.cos(a1):.1f},{cy + 95 * math.sin(a1):.1f} '
                 f'A95,95 0 0 0 {cx + 95 * math.cos(a0):.1f},{cy + 95 * math.sin(a0):.1f} Z" fill="#1A4A92"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="88" fill="#3478D2" stroke="#1B4F9C" stroke-width="5"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="38" fill="#C9CCCF" stroke="#8E9297" stroke-width="3"/>' + R(cx - 6, cy - 38, 12, 14, "#6D7174"))
    # caja de bornes a un costado con salida de cable
    c.append(f'<g filter="url(#sDura)">{R(70, 120, 120, 180, "#2A67C2")}</g>' + R(78, 128, 104, 164, "#3478D2") + R(70, 120, 120, 10, "#4A8BE0"))
    c.append(f'<path d="M110,300 V420 Q110,470 60,470 H0" stroke="#2B2C2E" stroke-width="34" fill="none"/>')
    # placa de características
    c.append(R(300, 560, 200, 0.1, "none"))
    c.append(T(400, 625, f"-{ref}  ·  {placa}", 24, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {}, WH


# ============================================================ CAJA DE BORNES DEL MOTOR (referencia #15)
def _tuerca(x, y, r=34):
    import math
    pts = " ".join(f"{x + r * math.cos(math.radians(a)):.1f},{y + r * math.sin(math.radians(a)):.1f}" for a in range(30, 390, 60))
    return (f'<g filter="url(#sTorn)"><polygon points="{pts}" fill="#C7CACD" stroke="#7E8287" stroke-width="2.5"/></g>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.62:.1f}" fill="#E6E8EA" stroke="#9A9EA3" stroke-width="2"/>' + R(x - r * 0.3, y - 2.5, r * 0.6, 5, "#3B3F46"))


def caja_bornes(tipo="6", conexion="delta", ancho_mm=110.0):
    """IEC 6 bornes (U1 V1 W1 / W2 U2 V2) o NEMA 9 puntas (T1…T9). Puentes amarillos según la conexión."""
    Wp, Hp = 520, 420 if tipo == "6" else 520
    s_mm = ancho_mm / Wp
    b, c = {}, []
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#2E3034")}</g>' + R(14, 14, Wp - 28, Hp - 28, "#A4A7AB"))
    c.append(R(60, 50, Wp - 90, Hp - 90, "#D9441F", 'stroke="#2E3034" stroke-width="6"'))
    # PE al costado
    c.append(_tuerca(32, 40, 26) + T(32, 82, "PE", 18, "#1B1F24", 800) + f'<path d="M22,100 h20 M25,107 h14 M29,114 h6 M32,92 v8" stroke="#1B1F24" stroke-width="2.5"/>')
    b["PE"] = (32, 40)
    lab = lambda x, y, t: R(x - 46, y - 17, 92, 34, "#F4F4F2", 'rx="5"') + T(x, y, t, 22, "#1B1F24", 700)
    if tipo == "6":
        xs, y1, y2 = (150, 275, 400), 120, 270
        arriba, abajo = ("U1", "V1", "W1"), ("W2", "U2", "V2")
        nemas = {"U1": "U1/T1", "V1": "V1/T2", "W1": "W1/T3", "W2": "W2/T6", "U2": "U2/T4", "V2": "V2/T5"}
        if conexion == "delta":
            for x in xs:
                c.append(R(x - 22, y1, 44, y2 - y1, "#F2C230", 'stroke="#B48A12" stroke-width="2"'))
        else:
            c.append(R(xs[0], y2 - 18, xs[2] - xs[0], 36, "#F2C230", 'stroke="#B48A12" stroke-width="2"'))
        for x, n1, n2 in zip(xs, arriba, abajo):
            c.append(_tuerca(x, y1) + lab(x, y1 + 62, nemas[n1]) + _tuerca(x, y2) + lab(x, y2 + 62, nemas[n2]))
            b[n1], b[n2] = (x, y1), (x, y2)
    else:
        # NEMA 9 puntas, tensión baja: T1-T6-T7 · T2-T4-T8 · T3-T5-T9 (un puente por columna)
        xs, ys = (150, 275, 400), (110, 230, 350)
        cols = (("T1", "T6", "T7"), ("T2", "T4", "T8"), ("T3", "T5", "T9")) if conexion == "bajo" else (("T1", "T4", "T7"), ("T2", "T5", "T8"), ("T3", "T6", "T9"))
        for x, col in zip(xs, cols):
            if conexion == "bajo":
                c.append(R(x - 22, ys[0], 44, ys[2] - ys[0], "#F2C230", 'stroke="#B48A12" stroke-width="2"'))
            else:
                c.append(R(x - 22, ys[1], 44, ys[2] - ys[1], "#F2C230", 'stroke="#B48A12" stroke-width="2"'))
            for y, n in zip(ys, col):
                c.append(_tuerca(x, y) + lab(x, y + 58, n))
                b[n] = (x, y)
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ BORNERAS DE CABALLETE (referencias #23 a #25)
def bornera(nombres=("L1", "L2", "L3", "PE"), tipos=None, ref="X0", paso_mm=6.2):
    """Bornes de paso en riel: gris = paso · azul = neutro · verde/amarillo = PE. Marcador arriba y abajo, tornillo de ranura, punto de prueba."""
    tipos = tipos or {}
    P, Hp = 80, 400
    n = len(nombres)
    Wp = 120 + P * n + 20
    s_mm = paso_mm / P
    b, c = {}, []
    # tope final con la designación del paquete
    c.append(f'<g filter="url(#sCuerpo)"><path d="M20,70 H120 V330 H20 Q0,330 0,310 V90 Q0,70 20,70 Z" fill="#B98F5A" stroke="#1B1F24" stroke-width="5"/></g>')
    c.append(R(10, 90, 110, 8, "#8C6A3E") + R(10, 300, 110, 8, "#8C6A3E") + f'<path d="M120,165 H60 Q40,165 40,200 Q40,235 60,235 H120" fill="#FFFFFF" stroke="#1B1F24" stroke-width="5"/>')
    c.append(R(26, 110, 74, 40, "#FFFFFF", 'stroke="#1B1F24" stroke-width="3"') + T(63, 130, f"-{ref}", 22, "#1B1F24", 800))
    for i, nm in enumerate(nombres):
        x0 = 120 + P * i
        t = tipos.get(nm, "N" if nm == "N" else "")
        if t == "PE" or nm == "PE":
            cuerpo = f'<rect x="{x0}" y="0" width="{P}" height="{Hp}" fill="#2E9E44"/><rect x="{x0 + P / 2}" y="0" width="{P / 2}" height="{Hp}" fill="#F2D21B"/>'
        elif t == "N":
            cuerpo = R(x0, 0, P, Hp, "#4A6FA5")
        else:
            cuerpo = R(x0, 0, P, Hp, "#A9ABAE")
        c.append(f'<g filter="url(#sDura)">{cuerpo}</g>' + f'<rect x="{x0}" y="0" width="{P}" height="{Hp}" fill="none" stroke="#1B1F24" stroke-width="4"/>')
        for y in (40, 360):
            c.append(R(x0 + 18, y - 9, P - 36, 6, "#1B1F24") + R(x0 + 18, y + 3, P - 36, 6, "#1B1F24"))
        for y in (80, 320):
            c.append(R(x0 + 4, y - 18, P - 8, 36, "#FFFFFF") + T(x0 + P / 2, y, nm, 26, "#1B1F24", 800))
        for y in (140, 260):
            c.append(f'<circle cx="{x0 + P / 2}" cy="{y}" r="28" fill="#1B1F24"/><circle cx="{x0 + P / 2}" cy="{y}" r="22" fill="#B4B4B0"/>'
                     f'<line x1="{x0 + P / 2 - 16}" y1="{y + 16}" x2="{x0 + P / 2 + 16}" y2="{y - 16}" stroke="#0A0A0B" stroke-width="7"/>')
        c.append(f'<circle cx="{x0 + P / 2}" cy="200" r="11" fill="#1B1F24"/>')
        b[f"{nm}_a"], b[f"{nm}_b"] = (x0 + P / 2, 140), (x0 + P / 2, 260)
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ LOGO! 8 12/24RCE + LOGO!Power 24 V 1,3 A (referencia #26, se conserva la marca)
def _torn_logo(x, y, r=17):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#17181A"/><circle cx="{x}" cy="{y}" r="{r * 0.55:.1f}" fill="#2B2D30"/>' + R(x - r * 0.5, y - 2, r, 4, "#4A4D52")


def logo_power(ref="T1", alto_mm=90.0):
    """Todos los bornes arriba (instrucciones SITOP LOGO!Power: montar con los bornes arriba): L N | + + − −; abajo potenciómetro y LED."""
    Wp, Hp = 265, 660
    s_mm = alto_mm / Hp
    b, c = {}, [f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#7B828D")}</g>']
    c.append(R(0, 0, Wp, 150, "#6E7580") + R(0, 150, Wp, 4, "#565C66") + R(0, 545, Wp, 115, "#6A717C") + R(0, 545, Wp, 4, "#565C66"))
    for x, n in zip((30, 70, 125, 160, 197, 233), ("L", "N", "+", "+", "−", "−")):
        c.append(T(x, 14, n, 15, "#E3E6EA", 600) + _torn_logo(x, 50))
        b.setdefault(n, (x, 50)); b[n + ("2" if n in b and b[n] != (x, 50) else "")] = (x, 50)
    c.append(T(50, 95, "INPUT AC 100-240V", 11, "#E3E6EA", 600) + T(180, 95, "OUTPUT DC 24V 1.3A", 11, "#E3E6EA", 600))
    c.append(R(12, 175, 112, 36, "#F2F3F4") + T(68, 193, "SIEMENS", 22, "#2E7A84", 800))
    c.append(T(250, 190, "LOGO!", 32, "#E3E6EA", 400, "end") + T(250, 222, "Power", 20, "#E3E6EA", 400, "end"))
    c.append(R(214, 268, 14, 14, "#2BD14A") + T(221, 294, "DC OK", 10, "#E3E6EA", 600))
    c.append(T(Wp / 2, 450, f"-{ref}", 30, "#F2F3F4", 700))
    c.append(f'<circle cx="80" cy="603" r="22" fill="#141516"/>' + R(70, 601, 20, 4, "#55595F") + f'<circle cx="175" cy="603" r="22" fill="#141516"/><circle cx="175" cy="603" r="12" fill="#2B2D30"/>')
    c.append(T(80, 640, "V adj", 11, "#E3E6EA", 600) + T(175, 640, "I meas.", 11, "#E3E6EA", 600))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    b = {"L": b["L"], "N": b["N"], "+": (125, 50), "+2": (160, 50), "−": (197, 50), "−2": (233, 50)}
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def logo8(ref="A1", alto_mm=90.0):
    """LOGO! 8 12/24RCE (6ED1052-1MD08-0BA1): arriba L+ M I1…I8, abajo Q1…Q4 (1-2 cada una)."""
    Wp, Hp = 530, 660
    s_mm = alto_mm / Hp
    b, c = {}, [f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#7B828D")}</g>']
    c.append(R(0, 0, Wp, 150, "#6E7580") + R(0, 150, Wp, 4, "#565C66") + R(0, 545, Wp, 115, "#6A717C") + R(0, 545, Wp, 4, "#565C66"))
    top = ["L+", "M", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]
    for k, n in enumerate(top):
        x = 75 + k * 41
        c.append(T(x, 18, n, 14, "#E3E6EA", 600) + _torn_logo(x, 55))
        b[n] = (x, 55)
    c.append(T(26, 55, "X10", 13, "#E3E6EA", 600))
    c.append(T(14, 100, "I1…I8 24 VDC · I1,I2,I7,I8 = AI 0–10 V", 12, "#E3E6EA", 600, "start"))
    c.append(R(345, 105, 170, 38, "none", 'stroke="#C9CDD2" stroke-width="2"') + T(430, 124, "DC 12/24V INPUT 8xDC", 11, "#E3E6EA", 600))
    # frente: placa con pantalla y teclado
    c.append(f'<g filter="url(#sDura)">{R(5, 172, 310, 330, "#3E434A")}</g>')
    c.append(R(12, 184, 120, 34, "#F2F3F4") + T(72, 201, "SIEMENS", 21, "#2E7A84", 800) + T(300, 200, "LOGO!", 34, "#E3E6EA", 400, "end"))
    c.append(R(40, 255, 235, 175, "#C9CBC7", 'stroke="#2A2E33" stroke-width="4"') + T(55, 466, "LAN", 15, "#E3E6EA", 600, "start"))
    c.append(R(330, 175, 180, 70, "#868D98", 'stroke="#5B616B" stroke-width="2"') + R(390, 232, 50, 12, "#141516") + T(345, 262, "P0", 12, "#E3E6EA", 600, "start"))
    c.append(T(460, 280, "12/24RCE", 16, "#E3E6EA", 700))
    for (x, y, t) in ((408, 300, "▲"), (355, 350, "◀"), (460, 350, "▶"), (408, 400, "▼"), (355, 450, "ESC")):
        c.append(f'<g filter="url(#sTorn)">{R(x - 23, y - 23, 46, 46, "#AEB9B9", 'stroke="#5B616B" stroke-width="2"')}</g>' + T(x, y, t, 14 if len(t) > 1 else 16, "#4E5862", 700))
    c.append(f'<g filter="url(#sTorn)">{R(437, 427, 46, 46, "#3E9E4A", 'stroke="#2C7A36" stroke-width="2"')}</g>' + T(460, 450, "OK", 14, "#FFFFFF", 700))
    c.append(T(420, 495, "6ED1052-1MD08-0BA1", 12, "#E3E6EA", 600))
    c.append(T(160, 525, f"-{ref}", 30, "#F2F3F4", 700))
    # salidas a relé Q1…Q4
    c.append(T(26, 600, "X11", 13, "#E3E6EA", 600))
    for q in range(4):
        x0 = 72 + q * 118
        for k, n in enumerate(("1", "2")):
            x = x0 + k * 36
            c.append(_torn_logo(x, 600) + T(x, 632, n, 13, "#E3E6EA", 600))
            b[f"Q{q + 1}.{n}"] = (x, 600)
        c.append(f'<path d="M{x0 - 4},628 l12,-10 M{x0 + 6},618 l12,0" stroke="#E3E6EA" stroke-width="2" fill="none"/>' + T(x0 + 18, 652, f"Q{q + 1}", 13, "#E3E6EA", 700))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ ACCESORIOS
def riel_canaleta(ancho_mm=200.0):
    """Riel DIN 35 × 7,5 mm perforado (EN 60715) sobre placa y canaleta ranurada gris en vertical y horizontal."""
    Wp, Hp = 1000, 520
    s_mm = ancho_mm / Wp
    c = [R(0, 0, Wp, Hp, "#E9EAEC")]
    # canaletas
    for x0 in (30, 870):
        c.append(f'<g filter="url(#sDura)">{R(x0, 0, 100, Hp, "#C9CBCE")}</g>' + R(x0 + 40, 0, 20, Hp, "#B4B7BB"))
        for y in range(10, Hp, 34):
            c.append(R(x0, y, 14, 20, "#E9EAEC") + R(x0 + 86, y, 14, 20, "#E9EAEC"))
    c.append(f'<g filter="url(#sDura)">{R(130, 400, 740, 100, "#C9CBCE")}</g>' + R(130, 440, 740, 20, "#B4B7BB"))
    for x in range(140, 870, 34):
        c.append(R(x, 400, 20, 14, "#E9EAEC") + R(x, 486, 20, 14, "#E9EAEC"))
    # riel DIN
    c.append(f'<g filter="url(#sDura)">{R(130, 160, 740, 175, "#D7DADE")}</g>' + R(130, 160, 740, 22, "#AEB3B9") + R(130, 313, 740, 22, "#AEB3B9"))
    for x in range(170, 860, 85):
        c.append(R(x, 228, 50, 40, "#8C9198", 'rx="20"'))
    c.append(T(500, 125, "Riel DIN 35 × 7,5 mm (EN 60715)", 26, "#1B1F24", 700) + T(500, 380, "Canaleta ranurada 40 × 40 mm", 22, "#1B1F24", 700))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {}, WH


def conductores(ancho_mm=160.0):
    """Muestras de conductor con puntera aislada (DIN 46228-4) y marcador del número de hilo, en los colores IEC 60204-1."""
    Wp, Hp = 900, 420
    s_mm = ancho_mm / Wp
    c = []
    filas = (("#1A1A1A", "L1", "Potencia", "#E7C21A", "6 mm²"), ("#D7262C", "12", "Mando AC", "#2F6FD0", "2,5 mm²"), ("#1F5FD0", "24", "Mando DC", "#2F6FD0", "2,5 mm²"),
             ("#7FC4F0", "N", "Neutro", "#2F6FD0", "2,5 mm²"), ("PE", "PE", "Protección", "#E7C21A", "6 mm²"))
    for k, (col, mk, nombre, colp, sec) in enumerate(filas):
        y = 50 + k * 80
        if col == "PE":
            c.append(R(160, y - 11, 560, 22, "#2E9E44") + "".join(R(160 + i * 40, y - 11, 20, 22, "#F2D21B") for i in range(14)))
        else:
            c.append(R(160, y - 11, 560, 22, col))
        c.append(R(720, y - 15, 70, 30, colp, 'stroke="#555" stroke-width="2"') + R(790, y - 5, 60, 10, "#C9CCCF", 'stroke="#8E9297" stroke-width="1.5"'))
        c.append(f'<g filter="url(#sTorn)">{R(620, y - 22, 64, 44, "#FFFFFF", 'stroke="#1B1F24" stroke-width="3" rx="6"')}</g>' + T(652, y, mk, 24, "#1B1F24", 800))
        c.append(T(10, y - 8, nombre, 22, "#1B1F24", 700, "start") + T(10, y + 15, sec, 16, "#555", 600, "start"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {}, WH


def multimetro(lectura="144", unidad="Ω", alto_mm=160.0):
    """Multímetro digital de banco/taller con selector, pantalla, MIN/MAX, AC/DC, ZERO y bornes COM / VΩ (CAT III)."""
    import math
    Wp, Hp = 330, 600
    s_mm = alto_mm / Hp
    c = [f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#E0A320", 'rx="26"')}</g>', R(18, 18, Wp - 36, Hp - 36, "#2A2C30", 'rx="16"')]
    c.append(logo(34, 34, 22) + T(Wp - 34, 45, "TRMS · CAT III 600 V", 12, "#E3E6EA", 700, "end"))
    c.append(R(40, 70, 250, 120, "#B7C4A8", 'stroke="#111" stroke-width="4"'))
    c.append(f'<text x="268" y="132" font-family="DSEG7 Classic, monospace" font-size="62" fill="#1B1F24" text-anchor="end" dominant-baseline="central">{lectura}</text>')
    c.append(T(282, 172, unidad, 22, "#1B1F24", 700, "end") + T(54, 88, "AUTO", 13, "#1B1F24", 700, "start"))
    for k, t in enumerate(("MIN MAX", "AC/DC", "ZERO")):
        c.append(R(40 + k * 86, 210, 76, 40, "#3E4147", 'stroke="#111" stroke-width="2"') + T(78 + k * 86, 230, t, 13, "#FFFFFF", 700))
    cx, cy = 165, 372
    for k, t in enumerate(("OFF", "V~", "V⎓", "Ω", "→|", "A~")):
        a = math.radians(210 - k * 48)
        c.append(T(cx + 98 * math.cos(a), cy - 98 * math.sin(a), t, 16, "#FFFFFF", 700))
    c.append(f'<g filter="url(#sDura)"><circle cx="{cx}" cy="{cy}" r="64" fill="#17181A" stroke="#55595F" stroke-width="3"/></g>')
    ap = math.radians(210 - 3 * 48)
    c.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 58 * math.cos(ap):.1f}" y2="{cy - 58 * math.sin(ap):.1f}" stroke="#E0A320" stroke-width="10" stroke-linecap="round"/>')
    for x, t, col in ((100, "COM", "#111"), (230, "VΩ", "#C8202B")):
        c.append(T(x, 490, t, 16, "#FFFFFF", 700) + f'<circle cx="{x}" cy="530" r="24" fill="#0E0F10" stroke="{col}" stroke-width="7"/><circle cx="{x}" cy="530" r="9" fill="#3A3B3E"/>')
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {"COM": (100 * s_mm, 525 * s_mm), "VΩ": (230 * s_mm, 525 * s_mm)}, WH


def pinza(lectura="24.3", unidad="A~", alto_mm=220.0):
    """Pinza amperimétrica (referencia #33): mordaza roja, cuerpo con selector, pantalla y bornes."""
    import math
    Wp, Hp = 300, 820
    s_mm = alto_mm / Hp
    c = []
    c.append(f'<g filter="url(#sCuerpo)"><path d="M150,10 C40,10 20,120 40,230 L80,250 C60,150 80,70 150,70 C220,70 240,150 220,250 L260,230 C280,120 260,10 150,10 Z" fill="#C8202B"/></g>')
    c.append(R(144, 8, 12, 66, "#2A2C30"))
    c.append(f'<g filter="url(#sCuerpo)">{R(10, 240, 280, 570, "#E0A320", 'rx="24"')}</g>' + R(26, 256, 248, 538, "#2A2C30", 'rx="14"'))
    c.append(logo(42, 274, 20) + T(258, 284, "TRMS", 12, "#E3E6EA", 700, "end"))
    cx, cy = 150, 380
    for k, t in enumerate(("OFF", "V", "A~", "Ω")):
        a = math.radians(160 - k * 47)
        c.append(T(cx + 82 * math.cos(a), cy - 82 * math.sin(a), t, 15, "#FFFFFF", 700))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="55" fill="#17181A" stroke="#55595F" stroke-width="3"/>')
    ap = math.radians(160 - 2 * 47)
    c.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 50 * math.cos(ap):.1f}" y2="{cy - 50 * math.sin(ap):.1f}" stroke="#E0A320" stroke-width="8" stroke-linecap="round"/>')
    c.append(R(48, 470, 204, 120, "#B7C4A8", 'stroke="#111" stroke-width="4"'))
    c.append(f'<text x="236" y="525" font-family="DSEG7 Classic, monospace" font-size="56" fill="#1B1F24" text-anchor="end" dominant-baseline="central">{lectura}</text>' + T(236, 572, unidad, 20, "#1B1F24", 700, "end"))
    for k, t in enumerate(("MIN MAX", "AC/DC", "ZERO")):
        c.append(R(40 + k * 76, 610, 68, 36, "#3E4147", 'stroke="#111" stroke-width="2"') + T(74 + k * 76, 628, t, 11, "#FFFFFF", 700))
    for x, t, col in ((95, "COM", "#111"), (205, "VΩ", "#C8202B")):
        c.append(T(x, 680, t, 14, "#FFFFFF", 700) + f'<circle cx="{x}" cy="730" r="22" fill="#0E0F10" stroke="{col}" stroke-width="6"/>')
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {}, WH


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

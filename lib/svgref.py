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
 <filter id="sDura" x="-8%" y="-8%" width="120%" height="135%"><feGaussianBlur in="SourceAlpha" stdDeviation="3.2"/><feOffset dx="2" dy="7"/><feComponentTransfer><feFuncA type="linear" slope="0.5"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sTorn" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="2.4"/><feOffset dx="1.5" dy="4"/><feComponentTransfer><feFuncA type="linear" slope="0.45"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sCuerpo" x="-8%" y="-5%" width="120%" height="118%"><feGaussianBlur in="SourceAlpha" stdDeviation="7"/><feOffset dx="5" dy="12"/><feComponentTransfer><feFuncA type="linear" slope="0.45"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sMando" x="-25%" y="-25%" width="160%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dx="4" dy="10"/><feComponentTransfer><feFuncA type="linear" slope="0.55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <radialGradient id="rMando" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#4A4A48"/><stop offset="0.6" stop-color="#2A2A28"/><stop offset="1" stop-color="#151514"/></radialGradient>
 <radialGradient id="rPerilla" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.7" stop-color="#D9DCDF"/><stop offset="1" stop-color="#AEB3B8"/></radialGradient>
 <linearGradient id="rCobre" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8C4A1E"/><stop offset="0.3" stop-color="#E8A06A"/><stop offset="0.55" stop-color="#C87533"/><stop offset="1" stop-color="#7A3E16"/></linearGradient>
 <linearGradient id="rAcero" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4F6F8"/><stop offset="0.45" stop-color="#C3C8CE"/><stop offset="0.55" stop-color="#A9AFB6"/><stop offset="1" stop-color="#DDE1E5"/></linearGradient>
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


ME_AZUL = "#0094B0"   # color del logo ME.


ETQ_AMARILLO = "#F5C400"
ETQ_MM = (13.0, 4.8, 3.1)    # ancho, alto y letra de la etiqueta en mm: IGUAL en todos los equipos


def PL(x, y, ref, s_mm, ancla="middle", rot=0):
    """Etiqueta de designación del equipo físico (-F1, -QM1, -KM1…): placa AMARILLA cuadrada, sin borde,
    letras negras y siempre del mismo tamaño real (ETQ_MM), sea cual sea la escala del dibujo (s_mm = mm por unidad)."""
    w, h, fs = (v / s_mm for v in ETQ_MM)
    x0 = x - w / 2 if ancla == "middle" else (x - w if ancla == "end" else x)
    g = (f'<g filter="url(#sTorn)"><rect x="{x0:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{ETQ_AMARILLO}"/></g>'
         + T(x0 + w / 2, y + fs * 0.03, f"-{ref}", round(fs, 1), "#111111", 800))
    return f'<g transform="rotate({rot} {x} {y})">{g}</g>' if rot else g


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
    c.append(PL(318, 556, ref, s_mm))
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
    # datos de placa impresos (como el ejemplo del usuario): tensión, norma, poder de corte, Uimp
    fz = 15 if n > 1 else 13
    for k_, t_ in enumerate((f"Ue: {tension}", "IEC/EN 60898-1", "Icn = 6000 A", "Uimp = 4 kV")):
        c.append(T(8, 326 + k_ * 18, t_, fz, "#555756", 600, "start"))
    # ventana indicadora por polo: verde = abierto (OFF)
    for i in range(n):
        xv = P * i + 135
        c.append(f'<g filter="url(#sTorn)">{R(xv - 18, 236, 36, 16, "#2E3138")}</g>' + R(xv - 14, 239, 28, 10, "#2FA84F"))
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
        c.append(f'<circle cx="{xm + 34}" cy="548" r="9" fill="none" stroke="#C9CCCF" stroke-width="3"/>' + T(xm + 50, 548, "-OFF", 20, "#C9CCCF", 700, "start"))
    c.append(PL(Wp / 2, 632, ref, s_mm))
    c.append(R(22, 678, Wp - 44, 22, "#0270C0"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def disyuntor2(ref="Q1", In=20, curva="C", tension="230/400 VAC"):
    return disyuntor(2, In, curva, ref, tension)


# ============================================================ GUARDAMOTOR (referencia #3, cuerpo 372 × 735 px, blanco)
def guardamotor(ref="QM1", rango=(22, 32), ajuste=24.3, ancho_mm=45.0):
    """Guardamotor con bloque de contactos auxiliares arriba (13-14 NA, 21-22 NC).
    Carátula ordenada como el ejemplo del usuario: clase de disparo, dial con escala, rectángulo para la etiqueta,
    rango, TRIP con su barra curva, disparo magnético I> con su valor, TEST, posición ON, mando giratorio, OFF y símbolo lateral."""
    import math
    Wp, Hp = 372, 860
    s_mm = ancho_mm / Wp
    b, c = {}, []
    K_ = "#2E3138"
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#ECEEEC")}</g>')
    for x in (0, 122, 232, 352):
        c.append(R(x, -14, 20, 18, "#3A3B3E") + R(x, Hp - 4, 20, 18, "#3A3B3E"))
    # bornes de potencia
    c.append(R(0, 0, Wp, 125, "url(#rClaro)") + R(0, Hp - 125, Wp, 125, "url(#rClaro)"))
    xs = (69, 183, 282)
    for x, n1, n2 in zip(xs, ("1/L1", "3/L2", "5/L3"), ("2/T1", "4/T2", "6/T3")):
        c.append(T(x, 16, n1, 17, "#4A505A", 700) + T(x, Hp - 18, n2, 17, "#4A505A", 700))
        c.append(tornillo_cruz(x, 62, 30) + tornillo_cruz(x, Hp - 67, 30))
        b[n1], b[n2] = (x, 62), (x, Hp - 67)
    # bloque de contactos auxiliares (mando) montado arriba: 13-14 NA · 21-22 NC
    c.append(f'<g filter="url(#sDura)">{R(0, 128, Wp, 112, "url(#rOsc)")}</g>' + R(0, 128, Wp, 2, "#666A77"))
    for x, n_, f_ in ((50, "13", "NO"), (138, "14", ""), (234, "21", "NC"), (322, "22", "")):
        c.append(tornillo_cruz(x, 168, 26))
        c.append(T(x, 216, n_, 22, "#FFFFFF", 800))
        b[n_] = (x, 168)
    c.append(T(94, 216, "NO", 18, "#FFFFFF", 500) + T(278, 216, "NC", 18, "#FFFFFF", 500))
    # frente elevado
    y0f = 250
    c.append(f'<g filter="url(#sDura)">{R(8, y0f, Wp - 16, 460, "url(#rFrente)")}</g>' + R(8, y0f, Wp - 16, 3, "#FFFFFF"))
    k = 0.607
    X = lambda xr: 8 + k * xr
    ky = 0.78
    Y = lambda yr: y0f + 8 + ky * yr
    # clase de disparo
    c.append(f'<path d="M{X(48)},{Y(48)} v-12 h10 v-12 h10" stroke="{K_}" stroke-width="2.6" fill="none"/>' + T(X(95), Y(36), "CLASS 10", 16, K_, 800, "start"))
    c.append(R(X(45), Y(62), 20, 6, K_) + R(X(205), Y(56), 16, 5, K_))
    # rectángulo para la etiqueta y rango
    c.append(R(X(312), Y(22), k * 190, ky * 105, "none", f'stroke="{K_}" stroke-width="2.2"'))
    c.append(PL(X(407), Y(74), ref, s_mm))
    lo, hi = rango
    c.append(T(X(407), Y(152), f"{lo:g}–{hi:g} A", 24, "#4A4F55", 800))
    # dial: escala con el máximo arriba a la izquierda y el mínimo abajo a la derecha (como el ejemplo)
    cx, cy, r = X(128), Y(128), 32
    a_hi = 170   # escala en la mitad inferior: máximo a la izquierda, mínimo abajo a la derecha (170° → 320°)
    paso_ = 25
    angulo = lambda kk: math.radians(a_hi + paso_ * kk)
    for kk in range(7):
        ang = angulo(kk)
        c.append(f'<line x1="{cx + (r + 5) * math.cos(ang):.1f}" y1="{cy - (r + 5) * math.sin(ang):.1f}" x2="{cx + (r + 13) * math.cos(ang):.1f}" y2="{cy - (r + 13) * math.sin(ang):.1f}" stroke="{K_}" stroke-width="2"/>')
    for kk, v in ((0, hi), (3, round((lo + hi) / 2)), (6, lo)):
        ang = angulo(kk)
        c.append(T(cx + (r + 27) * math.cos(ang), cy - (r + 27) * math.sin(ang), f"{v:g}", 15, K_, 800))
    angp = a_hi + paso_ * 6 * (hi - ajuste) / (hi - lo)
    c.append(f'<g filter="url(#sTorn)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#rPerilla)" stroke="#8E949A" stroke-width="2"/></g>')
    c.append(f'<g transform="rotate({-angp:.1f} {cx} {cy})">' + R(cx - 22, cy - 5, 44, 10, "#7C838A", 'rx="5"') + R(cx - 5, cy - 22, 10, 44, "#7C838A", 'rx="5"')
             + f'<polygon points="{cx + r - 2},{cy} {cx + r - 12},{cy - 5} {cx + r - 12},{cy + 5}" fill="{K_}"/></g>')
    # TRIP con su barra curva
    c.append(T(X(222), Y(240), "TRIP", 17, K_, 800, rot=-32))
    c.append(f'<path d="M{X(198)},{Y(300)} Q{X(232)},{Y(250)} {X(292)},{Y(222)}" stroke="#8E949A" stroke-width="6" fill="none" stroke-linecap="round"/>')
    c.append(R(X(118), Y(266), 12, 9, "#8E949A") + R(X(121), Y(268), 6, 4, K_))
    # disparo magnético y TEST
    c.append(R(X(48), Y(318), 22, 18, "none", f'stroke="{K_}" stroke-width="2"') + T(X(48) + 11, Y(318) + 9, "I&gt;", 10, K_, 800) + T(X(110), Y(330), f"{int(hi * 13)} A", 18, K_, 700, "start"))
    c.append(T(X(48), Y(365), "TEST", 13, K_, 800, "start") + f'<path d="M{X(110)},{Y(385)} H{X(45)} l8,-5 M{X(45)},{Y(385)} l8,5" stroke="{K_}" stroke-width="2" fill="none"/>')
    c.append(f'<g filter="url(#sTorn)">{R(X(115), Y(345), k * 60, ky * 45, "#2A2D33")}</g>' + R(X(146), Y(400), 11, 11, "#B9BDC1"))
    # posición ON
    c.append(R(X(428), Y(228), 5, 22, K_) + T(X(448), Y(248), "L", 9, K_, 800) + T(X(438), Y(282), "ON", 13, K_, 800))
    # mando giratorio negro con lengüeta clara (posición OFF)
    kx, kyy, kr = X(410), Y(440), 64
    c.append(f'<g filter="url(#sMando)"><circle cx="{kx}" cy="{kyy}" r="{kr}" fill="url(#rMando)"/></g>')
    c.append(f'<g transform="rotate(-6 {kx} {kyy})"><g filter="url(#sMando)"><rect x="{kx - 137}" y="{kyy - 22}" width="197" height="44" rx="6" fill="#1A1A1A"/></g>'
             f'<g filter="url(#sTorn)"><path d="M{kx - 128},{kyy - 20} H{kx - 80} V{kyy + 20} H{kx - 128} Q{kx - 137},{kyy + 20} {kx - 137},{kyy + 10} V{kyy - 10} Q{kx - 137},{kyy - 20} {kx - 128},{kyy - 20} Z" fill="#ECEDEE"/></g>'
             f'<path d="M{kx - 116},{kyy - 12} V{kyy + 12} M{kx - 106},{kyy - 12} V{kyy + 12} M{kx - 96},{kyy - 12} V{kyy + 12}" stroke="#B9BDC1" stroke-width="2.5"/></g>')
    # símbolo lateral impreso (contacto con marca de disyuntor)
    sx = X(536)
    c.append(f'<path d="M{sx},{Y(350)} V{Y(378)} M{sx - 12},{Y(378)} H{sx + 12} M{sx},{Y(384)} L{sx - 14},{Y(432)} M{sx - 2},{Y(440)} V{Y(470)}" stroke="{K_}" stroke-width="2.4" fill="none"/>'
             f'<path d="M{sx - 6},{Y(372)} l12,12 M{sx + 6},{Y(372)} l-12,12" stroke="{K_}" stroke-width="2.4"/>')
    c.append(logo(X(28), Y(470), 30))
    c.append(f'<circle cx="{X(205)}" cy="{Y(500)}" r="8" fill="none" stroke="{K_}" stroke-width="3"/>' + T(X(222), Y(506), "D", 9, K_, 800) + T(X(205), Y(528), "OFF", 13, K_, 800))
    c.append(R(20, 690, Wp - 40, 10, "#0270C0"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {kk: (x * s_mm, y * s_mm) for kk, (x, y) in b.items()}, WH


# ============================================================ RELÉ TÉRMICO (referencia #22, cuerpo 685 × 780 px)
def rele_termico(ref="F2", rango=(23, 32), ajuste=24.3, ancho_mm=45.0):
    import math
    Wp, Hp = 685, 780
    s_mm = ancho_mm / Wp
    b, c = {}, []
    # pines rígidos que entran en 2/T1 4/T2 6/T3 del contactor
    for x, n in zip((140, 342, 545), ("1/L1", "3/L2", "5/L3")):
        c.append(f'<g filter="url(#sTorn)">{R(x - 22, -34, 44, 64, "url(#rCobre)")}</g>' + R(x - 14, -26, 28, 10, "#5E2E10", 'opacity="0.5"'))
        c.append(T(x + 30, -12, n, 30, "#3B4148", 700, "start"))
        b[n] = (x, -10)
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#ECEEEC")}</g>')
    c.append(R(0, 0, Wp, 92, "url(#rClaro)"))
    c.append(marca_canal(20, 46, 17) + R(430, 39, 235, 16, "#1F6FBA"))
    # frente elevado
    c.append(f'<g filter="url(#sDura)">{R(0, 92, Wp, 345, "url(#rFrente)")}</g>' + R(0, 92, Wp, 3, "#FFFFFF"))
    # carátula sencilla como el ejemplo: dial azul, TEST, rectángulo para la etiqueta, STOP y RESET
    c.append(f'<g filter="url(#sTorn)">{R(42, 120, 336, 230, "#F3F4F2")}</g>')
    lo, hi = rango
    c.append(f'<polygon points="58,150 72,126 86,150" fill="#3A3D42"/>')
    cx, cy, r = 190, 228, 72
    c.append(f'<g filter="url(#sDura)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#1F67C4"/></g><circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="none" stroke="#5B92DD" stroke-width="3"/>')
    for k, v in enumerate((lo, round((lo + hi) / 2), hi)):
        ang = math.radians(150 - k * 60)
        c.append(T(cx + (r - 18) * math.cos(ang), cy - (r - 18) * math.sin(ang), f"{v:g}", 16, "#FFFFFF", 800))
    c.append(T(cx - 52, cy + 40, "A", 16, "#FFFFFF", 800))
    c.append(R(cx - 34, cy - 9, 68, 18, "#24237F") + R(cx - 9, cy - 34, 18, 68, "#24237F"))
    c.append(R(62, 318, 22, 16, "#D92D20") + T(108, 326, "TEST", 18, "#3A3D42", 800, "start"))
    # rectángulo donde va la etiqueta
    c.append(R(420, 112, 250, 78, "none", 'stroke="#9AA0A6" stroke-width="3"') + PL(545, 151, ref, s_mm))
    c.append(T(477, 222, "STOP", 26, "#3A3D42", 800) + T(610, 222, "RESET", 26, "#3A3D42", 800))
    c.append(f'<g filter="url(#sDura)"><rect x="410" y="242" width="270" height="130" fill="#3F4042"/></g>')
    c.append(f'<g filter="url(#sTorn)"><circle cx="477" cy="307" r="54" fill="#C7202D"/></g><circle cx="477" cy="307" r="38" fill="#E8331F"/>')
    c.append(f'<g filter="url(#sTorn)"><circle cx="610" cy="307" r="52" fill="#1F67C4"/></g>' + R(570, 299, 80, 16, "#24237F") + R(602, 267, 16, 80, "#24237F"))
    # contactos auxiliares: números ABAJO de los tornillos, como el ejemplo (98 NO 97 · 96 NC 95)
    c.append(R(0, 437, Wp, 150, "url(#rClaro)"))
    for x, n in ((105, "98"), (260, "97"), (425, "96"), (580, "95")):
        c.append(tornillo_cruz(x, 495, 36) + T(x, 562, n, 34, "#3A3D42", 700))
        b[n] = (x, 495)
    c.append(T(182, 562, "NO", 28, "#3A3D42", 600) + T(502, 562, "NC", 28, "#3A3D42", 600))
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
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, 790, "#D9DBDC")}</g>')
    for y0, h0 in ((0, 150), (630, 160)):
        c.append(R(0, y0, Wp, h0, "url(#rClaro)"))
        for k in range(1, 4):
            c.append(R(k * 122 + 1, y0 + 6, 3, h0 - 12, "#B9BDC0"))
    for x, nt, nb in zip(xs, ("3", "4", "5", "6"), ("2", "1", "8", "7")):
        # números impresos en el plástico de la base, junto a cada tornillo
        c.append(T(x, 28, nt, 34, "#2A2D31", 700) + T(x, 758, nb, 34, "#2A2D31", 700))
        c.append(tornillo_cruz(x, 98, 38) + tornillo_cruz(x, 682, 38))
        b[nt], b[nb] = (x, 98), (x, 682)
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
    c.append(PL(Wp / 2, 250, ref, s_mm))
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
    c.append(PL(Wp / 2, 198, ref, s_mm))
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


def diagrama_octal(tipo="rele", ancho_mm=40.0):
    """Diagrama interno del zócalo de 8 pines (vista frontal): bobina 2-7 dentro del zócalo;
    a la izquierda el polo 1 (común 1 · NA 3 · NC 4) y a la derecha el polo 2 (común 8 · NA 6 · NC 5).
    Temporizador: bobina con marca de retardo y contactos con marca de retardo a la conexión."""
    import math
    Wp, Hp = 640, 600
    s_mm = ancho_mm / Wp
    cx, cy, rp = 320, 260, 150
    ret = tipo == "timer"
    c = [f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#EEF2F5")}</g>']
    c.append(f'<g filter="url(#sDura)">{R(150, 90, 340, 340, "#BCC2C8", 'rx="30"')}</g><circle cx="{cx}" cy="{cy}" r="172" fill="#A3A9B0"/>')
    c.append(R(cx - 22, 96, 44, 30, "#7C838A", 'rx="8"'))
    ang = {"4": 112, "5": 68, "3": 157, "6": 23, "2": 203, "7": -23, "1": 248, "8": 292}
    P = {n: (cx + rp * math.cos(math.radians(a)), cy - rp * math.sin(math.radians(a))) for n, a in ang.items()}
    L = 'stroke="#1B1F24" stroke-width="5" fill="none" stroke-linejoin="round" stroke-linecap="round"'
    # bobina 2-7 en una cuerda horizontal dentro del zócalo
    (x2, y2), (x7, y7) = P["2"], P["7"]
    c.append(f'<path d="M{x2:.0f},{y2:.0f} H{cx - 42} M{cx + 42},{y7:.0f} H{x7:.0f}" {L}/>')
    c.append(f'<g filter="url(#sTorn)">{R(cx - 42, y2 - 24, 84, 48, "#FFFFFF", 'stroke="#1B1F24" stroke-width="5"')}</g>')
    if ret:
        c.append(R(cx - 42, y2 - 24, 24, 48, "#1B1F24"))
    for lado, com, nc, na in ((-1, "1", "4", "3"), (1, "8", "5", "6")):
        xp = cx + lado * 262          # pivote de la cuchilla
        xnc, xna = cx + lado * 286, cx + lado * 234
        (xc, yc), (x4, y4), (x3, y3) = P[com], P[nc], P[na]
        c.append(f'<path d="M{xc:.0f},{yc:.0f} V470 H{xp} V330" {L}/>')                          # común
        c.append(f'<path d="M{xp},330 L{xnc},238" {L}/>')                                          # cuchilla en reposo sobre NC
        c.append(f'<path d="M{x4:.0f},{y4:.0f} V60 H{xnc} V238" {L}/>')                            # NC (cerrado)
        c.append(f'<path d="M{x3:.0f},{y3:.0f} H{xna} V250" {L}/>')                               # NA (abierto)
        if ret:
            xm, ym = (xp + xnc) / 2, 284
            c.append(f'<path d="M{xm},{ym} H{xm - lado * 30} M{xm - lado * 30},{ym - 14} A14,14 0 0 {1 if lado < 0 else 0} {xm - lado * 30},{ym + 14}" stroke="#1B1F24" stroke-width="3.5" fill="none"/>')
        c.append(T(xnc + lado * 30, 200, "NC", 20, "#1B1F24", 800) + T(xna - lado * 12, 238, "NA", 20, "#1B1F24", 800, "start" if lado < 0 else "end") + T(xp - lado * 30, 400, "C", 20, "#1B1F24", 800))
    for n, (x, y) in P.items():
        c.append(f'<g filter="url(#sTorn)"><circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="#FFFFFF" stroke="#1B1F24" stroke-width="5"/></g>' + T(x, y, n, 34, "#1B1F24", 800))
    c.append(T(cx, 520, "Bobina 2-7  ·  NA 1-3 / 8-6  ·  NC 1-4 / 8-5", 24, "#1B1F24", 800))
    c.append(T(cx, 560, "Temporizado a la conexión" if ret else "Relé de 2 conmutados", 22, "#4A4F55", 700))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {}, WH


# ============================================================ OPERADORES DE PUERTA 22 mm (referencias #8 a #11)
def bloque(n1="3", n2="4", nc=False, piloto=False, alto_mm=30.0):
    """Bloque de contacto (o portalámparas) visto por detrás, dibujado como la captura del usuario:
    tornillos de conexión arriba (n1) y abajo (n2) con su número, ventana de color (NC roja / NO verde / LED blanca),
    leva semicircular, pestaña gris de enganche con su punto y tornillo de fijación a la izquierda. Cuerpo gris con sombra."""
    tipo = "LED" if piloto else ("NC" if nc else "NO")
    c = ['<defs><linearGradient id="gOpGris" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B7BCC1"/><stop offset="0.5" stop-color="#9097A0"/><stop offset="1" stop-color="#6E757E"/></linearGradient></defs>']
    _bloque_lateral(c, n1, n2, tipo)
    Wp, Hp = 375, 430
    s_mm = alto_mm / Hp
    svg, WH = svg_mm(Wp, Hp, s_mm, '<g transform="translate(-200,-440)">' + "".join(c) + "</g>")
    return svg, {n1: ((340 - 200) * s_mm, (528 - 440) * s_mm), n2: ((340 - 200) * s_mm, (785 - 440) * s_mm)}, WH


def _bisel_puerta(c, Wp=300):
    """Bisel negro de 30 mm con luz arriba-izquierda y sombra proyectada marcada."""
    c.append('<defs><linearGradient id="gBisel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B7BCC1"/><stop offset="0.5" stop-color="#9097A0"/><stop offset="1" stop-color="#6E757E"/></linearGradient>'
             '<radialGradient id="gAro" cx="0.35" cy="0.3" r="0.85"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#D3D7DA"/><stop offset="0.85" stop-color="#9EA4AA"/><stop offset="1" stop-color="#7C838A"/></radialGradient></defs>')
    c.append(f'<g filter="url(#sMando)">{R(0, 0, Wp, Wp, "url(#gBisel)")}</g>' + R(0, 0, Wp, 5, "#D5D9DD") + R(0, 0, 5, Wp, "#C9CED3") + R(0, Wp - 6, Wp, 6, "#5A6068") + R(Wp - 6, 0, 6, Wp, "#626870"))


def _cabeza(c, col, cx=150, cy=150, r=98):
    """Cabeza de color con volumen: degradado radial, brillo y sombra interna en el borde inferior."""
    gid = "gCab" + col[0].strip("#")
    c.append(f'<defs><radialGradient id="{gid}" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="{col[2]}"/><stop offset="0.55" stop-color="{col[0]}"/><stop offset="1" stop-color="{col[1]}"/></radialGradient></defs>')
    c.append(f'<g filter="url(#sTorn)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})"/></g>')
    c.append(f'<path d="M{cx - r * 0.62:.1f},{cy - r * 0.45:.1f} A{r * 0.8:.1f},{r * 0.8:.1f} 0 0 1 {cx + r * 0.45:.1f},{cy - r * 0.66:.1f}" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="{r * 0.1:.1f}" fill="none" stroke-linecap="round"/>')


COLORES = {"verde": ("#3FAE3A", "#1F6E1C", "#8BE07F"), "rojo": ("#D7262C", "#8E1418", "#FF8A80"), "negro": ("#2B2C2E", "#0B0B0C", "#6A6C70"),
           "amarillo": ("#F2C230", "#A97F0C", "#FFE58A"), "azul": ("#1F67C4", "#0F3F80", "#7FB0F0"), "blanco": ("#F4F4F2", "#B9BBBB", "#FFFFFF")}


def pulsador(color="verde", simbolo="I", ref="S1", ancho_mm=30.0):
    """Frente 2D del pulsador rasante de 22 mm. I = marcha, O = paro (IEC 60417)."""
    Wp = 300
    s_mm = ancho_mm / Wp
    c = []
    _bisel_puerta(c)
    c.append(f'<g filter="url(#sDura)"><circle cx="150" cy="150" r="128" fill="url(#gAro)"/></g>')
    c.append(f'<circle cx="150" cy="150" r="106" fill="#5E646A"/>')
    _cabeza(c, COLORES[color])
    if simbolo == "I":
        c.append(R(143, 112, 14, 76, "#FFFFFF", 'opacity="0.85"'))
    elif simbolo == "O":
        c.append(f'<circle cx="150" cy="150" r="36" fill="none" stroke="#FFFFFF" stroke-width="12" opacity="0.85"/>')
    c.append(PL(150, 335, ref, s_mm))
    svg, WH = svg_mm(Wp, 355, s_mm, "".join(c))
    return svg, {}, WH


def emergencia(ref="S3", ancho_mm=40.0):
    """Paro de emergencia: placa amarilla con leyenda y hongo rojo de 40 mm con volumen y sombra proyectada sobre la placa."""
    Wp = 400
    s_mm = ancho_mm / Wp
    c = ['<defs><radialGradient id="gPlaca" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#FFE27A"/><stop offset="0.7" stop-color="#F5C518"/><stop offset="1" stop-color="#C99A12"/></radialGradient>'
         '<radialGradient id="gHongo" cx="0.36" cy="0.3" r="0.85"><stop offset="0" stop-color="#FF8A80"/><stop offset="0.45" stop-color="#E02A2F"/><stop offset="0.85" stop-color="#A3161B"/><stop offset="1" stop-color="#6E0D10"/></radialGradient>'
         '<filter id="sHongo" x="-30%" y="-30%" width="170%" height="180%"><feGaussianBlur in="SourceAlpha" stdDeviation="9"/><feOffset dx="10" dy="18"/><feComponentTransfer><feFuncA type="linear" slope="0.6"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<path id="arcoEm" d="M58,200 A142,142 0 0 1 342,200"/></defs>']
    c.append(f'<g filter="url(#sCuerpo)"><circle cx="200" cy="200" r="196" fill="url(#gPlaca)"/></g>')
    c.append(f'<text font-family="{F}" font-size="30" font-weight="800" fill="#1B1F24" letter-spacing="3"><textPath href="#arcoEm" startOffset="50%" text-anchor="middle">EMERGENCIA</textPath></text>')
    c.append(f'<circle cx="200" cy="200" r="92" fill="#3A3B3E"/>')
    c.append(f'<g filter="url(#sHongo)"><circle cx="200" cy="200" r="122" fill="url(#gHongo)"/></g>')
    c.append(f'<circle cx="200" cy="200" r="104" fill="none" stroke="#7E1014" stroke-opacity="0.35" stroke-width="3"/>')
    c.append(f'<path d="M130,140 A85,85 0 0 1 230,112" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="12" fill="none" stroke-linecap="round"/>')
    # flecha de desbloqueo por giro: arco y punta tangente al final del arco
    c.append('<path d="M160,226 A48,48 0 1 1 242.2,222.7" stroke="#FFFFFF" stroke-width="8" fill="none" opacity="0.9"/>'
             '<polygon points="228.9,242.7 230.8,212.7 255.8,229.3" fill="#FFFFFF" opacity="0.9"/>')
    c.append(PL(200, 428, ref, s_mm))
    svg, WH = svg_mm(Wp, 448, s_mm, "".join(c))
    return svg, {}, WH


def selector(ref="S2", pos=0, ancho_mm=30.0):
    """Selector de 2 posiciones (referencia #8): perilla negra con maneta; 0 a la izquierda, 1 a la derecha."""
    Wp = 300
    s_mm = ancho_mm / Wp
    c = []
    _bisel_puerta(c)
    c.append(T(55, 40, "0", 30, "#1B1F24", 800) + T(245, 40, "1", 30, "#1B1F24", 800))
    ang = -45 if pos == 0 else 45
    c.append(f'<g filter="url(#sDura)"><circle cx="150" cy="160" r="118" fill="url(#gAro)"/></g>')
    c.append(f'<circle cx="150" cy="160" r="104" fill="url(#rMando)"/><circle cx="150" cy="160" r="78" fill="#232425" opacity="0.6"/>')
    c.append(f'<g transform="rotate({ang} 150 160)"><g filter="url(#sMando)"><rect x="118" y="44" width="64" height="232" rx="10" fill="#1A1B1C"/></g>'
             f'<rect x="122" y="50" width="8" height="220" fill="#5E6064"/><rect x="172" y="50" width="4" height="220" fill="#0A0A0B"/>'
             f'<rect x="141" y="56" width="18" height="100" rx="9" fill="#F4F4F2"/></g>')
    c.append(PL(150, 335, ref, s_mm))
    svg, WH = svg_mm(Wp, 355, s_mm, "".join(c))
    return svg, {}, WH


def piloto(color="verde", ref="H1", encendido=False, ancho_mm=30.0):
    """Piloto de 22 mm: apagado = difusor de color tenue; encendido = color pleno con brillo."""
    Wp = 300
    s_mm = ancho_mm / Wp
    col = {"verde": ("#55F000", "#C9E8BE"), "rojo": ("#FF2A1F", "#EFC4C1"), "amarillo": ("#FFC400", "#F2E2B0"), "azul": ("#2F7BFF", "#C2D4F0"), "blanco": ("#FFFFFF", "#ECECEC")}[color]
    gid = f"glow_{color}_{int(encendido)}"
    if encendido:
        c = [f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#F4FFE8"/><stop offset="0.25" stop-color="{col[0]}"/>'
             f'<stop offset="0.8" stop-color="{col[0]}" stop-opacity="0.75"/><stop offset="1" stop-color="{col[0]}" stop-opacity="0.2"/></radialGradient>'
             f'<filter id="brillo_{gid}" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="10"/></filter></defs>']
    else:
        c = [f'<defs><radialGradient id="{gid}" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="{col[1]}"/><stop offset="1" stop-color="#9FB59A"/></radialGradient></defs>']
    _bisel_puerta(c)
    c.append(f'<g filter="url(#sDura)"><circle cx="150" cy="150" r="128" fill="url(#gAro)"/></g>')
    if encendido:
        c.append(f'<circle cx="150" cy="150" r="110" fill="{col[0]}" opacity="0.55" filter="url(#brillo_{gid})"/>')
    c.append(f'<circle cx="150" cy="150" r="104" fill="url(#{gid})"/>')
    c.append(f'<path d="M85,105 A80,80 0 0 1 180,72" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="10" fill="none" stroke-linecap="round"/>')
    c.append(PL(75, 335, ref, s_mm) + T(150, 335, 'encendido' if encendido else 'apagado', 26, "#1B1F24", 700, "start"))
    svg, WH = svg_mm(Wp, 355, s_mm, "".join(c))
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
        c.append(R(766, 168, 8, 64, "#FF8A80") + R(766, 168, 8, 10, "#FFFFFF", 'opacity="0.7"'))
    c.append(R(560, 132, 3, 3, "none"))
    c.append(R(330, 36, 230, 54, "#3A3F47", 'rx="8"') + T(445, 63, salida, 28, "#FFFFFF", 700))
    c.append(f'<circle cx="610" cy="63" r="12" fill="#2BD14A"/>' + T(630, 63, "LED", 18, "#3A3F47", 700, "start"))
    c.append(PL(330, 300, ref, s_mm) + T(410, 300, "M18 · 10–30 VDC", 24, "#1B1F24", 700, "start"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def sensor_optico(modo="difuso", ref="B3", largo_mm=150.0):
    """Sensor óptico M18 en sus tres modos, con el haz recto sobre el eje del sensor:
    difuso (emisor y receptor en la misma cara, rebota en el objeto), réflex (rebota en un reflector), barrera (emisor y receptor separados)."""
    svg0, b0, (W0, H0) = sensor("optico", ref)
    Wp, Hp = 1500, 330
    s_mm = largo_mm / Wp
    k = W0 / 780 / s_mm
    cuerpo = svg0.split('<g transform="scale(')[1].split('">', 1)[1].rsplit('</g></svg>', 1)[0]
    c = [f'<g transform="scale({k:.4f})">{cuerpo}</g>']
    yh = 200 * k
    def haz(x0, x1, dy=0):
        d = 1 if x1 > x0 else -1
        y = yh + dy
        return (f'<polygon points="{x0},{y - 18 * k} {x1},{y - 34 * k} {x1},{y + 34 * k} {x0},{y + 18 * k}" fill="#FF3B30" opacity="0.14"/>'
                f'<line x1="{x0}" y1="{y}" x2="{x1 - d * 16 * k}" y2="{y}" stroke="#E11D2E" stroke-width="{4 * k:.1f}" stroke-dasharray="{14 * k:.0f} {8 * k:.0f}"/>'
                f'<polygon points="{x1},{y} {x1 - d * 20 * k},{y - 10 * k} {x1 - d * 20 * k},{y + 10 * k}" fill="#E11D2E"/>')
    x_cara = 772 * k
    if modo == "difuso":
        c.append(haz(x_cara, 1285, -14) + haz(1285, x_cara + 4, 14))
        c.append(f'<g filter="url(#sDura)">{R(1290, yh - 110, 120, 220, "#8E9AA6")}</g>' + T(1350, yh + 140, "objeto", 30, "#1B1F24", 700))
        c.append(T(1030, yh - 70, "luz que rebota en el objeto", 26, "#1B1F24", 700))
    elif modo == "reflex":
        c.append(haz(x_cara, 1325, -14) + haz(1325, x_cara + 4, 14))
        c.append(f'<g filter="url(#sDura)">{R(1330, yh - 90, 70, 180, "#C8202B")}</g>')
        for yy in range(int(yh - 80), int(yh + 80), 22):
            c.append(f'<polygon points="1338,{yy} 1360,{yy + 11} 1338,{yy + 22}" fill="#FF6A6A"/><polygon points="1392,{yy} 1370,{yy + 11} 1392,{yy + 22}" fill="#FF6A6A"/>')
        c.append(T(1365, yh + 130, "reflector", 30, "#1B1F24", 700) + T(1040, yh - 70, "luz que vuelve del reflector", 26, "#1B1F24", 700))
    else:
        import re as _re
        sin_txt = _re.sub(r'<text.*?</text>', '', cuerpo, flags=_re.S)
        sin_txt = _re.sub(r'<rect x="330" y="36"[^>]*/>|<circle cx="610" cy="63"[^>]*/>', '', sin_txt)
        sin_txt = _re.sub(r'<path d="M210,200[^>]*/>|<rect x="14" y="191"[^>]*/>|<rect x="0" y="197"[^>]*/>', '', sin_txt)   # el emisor solo lleva BN y BU
        c.append(haz(2080 - x_cara, x_cara + 4))
        c.append(f'<g transform="translate(2080,0) scale(-1,1)"><g transform="scale({k:.4f})">{sin_txt}</g></g>')
        c.append(PL(2080 - 640 * k, 300 * k, ref + "E", s_mm) + T(2080 - 560 * k, 300 * k, "emisor (BN +, BU −)", 24, "#1B1F24", 700, "start"))
        c.append(T(1040, yh - 70, "receptor ← emisor: el objeto corta el haz", 26, "#1B1F24", 700))
        Wp = 2080
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {kk: (x * k * s_mm, y * k * s_mm) for kk, (x, y) in {n: (bx / (W0 / 780), by / (W0 / 780)) for n, (bx, by) in b0.items()}.items()}, WH


# ============================================================ FLOTADOR (referencia #13)
def flotador(ref="S5", alto_mm=150.0):
    Wp, Hp = 460, 820
    s_mm = alto_mm / Hp
    b, c = {}, []
    # cable flexible con holgura: baja, hace una curva amplia y sube suelto hasta los hilos
    c.append(f'<g filter="url(#sDura)"><path d="M245,600 C250,700 330,760 250,790 C160,820 60,760 55,640 C50,540 95,470 70,330" stroke="#1E1F21" stroke-width="22" fill="none" stroke-linecap="round"/></g>')
    c.append(f'<path d="M245,600 C250,700 330,760 250,790 C160,820 60,760 55,640 C50,540 95,470 70,330" stroke="#5A5C60" stroke-width="4" fill="none" stroke-linecap="round" transform="translate(-5,-5)" opacity="0.6"/>')
    for y, col, n in ((150, "#7B5236", "C"), (205, "#1A1A1A", "NA"), (260, "#3F86D6", "NC")):
        c.append(f'<path d="M70,330 C68,{y + 60} 64,{y} 50,{y}" stroke="{col}" stroke-width="9" fill="none"/>')
        c.append(R(14, y - 8, 38, 16, "#3EA1F0", 'stroke="#2378C0" stroke-width="2"') + R(0, y - 3, 16, 6, "#B9BEC3") + T(33, y - 22, n, 18, "#1B1F24", 700))
        b[n] = (2, y)
    # cuerpo tipo pera
    c.append(f'<g filter="url(#sMando)"><path d="M130,40 H360 Q390,40 390,70 V440 Q390,470 360,470 H130 Q100,470 100,440 V70 Q100,40 130,40 Z" fill="#D7262C"/></g>')
    c.append(f'<path d="M140,55 H350 Q375,55 375,80 V430 Q375,455 350,455 H140 Q115,455 115,430 V80 Q115,55 140,55 Z" fill="#2F6FD0"/>')
    c.append(f'<path d="M165,95 H325 Q345,95 345,115 V355 Q345,375 325,375 H165 Q145,375 145,355 V115 Q145,95 165,95 Z" fill="#5AA5EE"/>')
    c.append(logo(185, 395, 40))
    c.append(f'<path d="M205,470 H285 L270,560 H220 Z" fill="#D7262C"/>' + R(232, 492, 26, 26, "#2F6FD0") + R(205, 560, 80, 40, "#1E1F21"))
    c.append(PL(400, 520, ref, s_mm))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ MOTOR (referencia del usuario: vista lateral con placa plateada al frente)
def motor(ref="M1", ancho_mm=300.0):
    """Motor trifásico TEFC visto de lado: eje, tapa, carcasa con aletas, ventilador, caja de bornes arriba, patas.
    La placa de características (plateada) va en el costado, con los datos reales del motor del caso base."""
    Wp, Hp = 1000, 660
    s_mm = ancho_mm / Wp
    c = ['<defs><linearGradient id="mCarc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7FB2F0"/><stop offset="0.35" stop-color="#2F78D6"/><stop offset="1" stop-color="#174E9E"/></linearGradient>'
         '<linearGradient id="mOsc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4F8FE0"/><stop offset="1" stop-color="#123F82"/></linearGradient>'
         '<linearGradient id="mPlaca" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7F8F9"/><stop offset="0.5" stop-color="#C9CED3"/><stop offset="1" stop-color="#E9ECEF"/></linearGradient></defs>']
    # base y patas
    c.append(f'<g filter="url(#sCuerpo)">{R(300, 610, 410, 30, "#1F5FB8")}</g>' + f'<polygon points="330,588 680,588 700,612 310,612" fill="url(#mOsc)"/>')
    # eje
    c.append(f'<g filter="url(#sDura)">{R(40, 410, 115, 38, "url(#rAcero)")}</g>' + R(40, 425, 60, 8, "#8E949A"))
    # brida, tapa, carcasa, ventilador
    c.append(f'<g filter="url(#sDura)">{R(150, 345, 42, 170, "url(#mOsc)", 'rx="10"')}</g>')
    c.append(f'<g filter="url(#sDura)">{R(185, 292, 90, 300, "url(#mCarc)", 'rx="28"')}</g>')
    c.append(f'<g filter="url(#sDura)">{R(262, 292, 482, 300, "url(#mCarc)")}</g>')
    for k, y in enumerate(range(302, 586, 20)):
        c.append(R(262, y, 482, 7, "#0F3B7A", 'opacity="0.55"') + R(262, y + 7, 482, 3, "#9CC6F5", 'opacity="0.55"'))
    c.append(R(262, 292, 30, 300, "#0F3B7A", 'opacity="0.25"') + R(714, 292, 30, 300, "#0F3B7A", 'opacity="0.25"'))
    c.append(f'<g filter="url(#sDura)"><path d="M744,292 H810 Q872,292 872,354 V530 Q872,592 810,592 H744 Z" fill="url(#mCarc)"/></g>')
    c.append(R(744, 292, 12, 300, "#0F3B7A", 'opacity="0.35"'))
    # caja de bornes con prensaestopa
    c.append(f'<g filter="url(#sDura)">{R(392, 200, 190, 122, "url(#mCarc)")}</g>' + f'<g filter="url(#sTorn)">{R(378, 182, 218, 24, "url(#mOsc)")}</g>')
    c.append(f'<circle cx="440" cy="262" r="24" fill="#123F82"/><circle cx="440" cy="262" r="13" fill="#0A1E3E"/>')
    c.append(f'<g filter="url(#sTorn)">{R(582, 250, 70, 26, "url(#mOsc)")}</g>')
    # placa de características plateada con datos reales
    c.append(f'<g filter="url(#sDura)">{R(420, 340, 286, 206, "url(#mPlaca)")}</g>')
    for x, y in ((432, 352), (694, 352), (432, 534), (694, 534)):
        c.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#8E949A"/><circle cx="{x - 1.5}" cy="{y - 1.5}" r="2.5" fill="#FFFFFF"/>')
    c.append(R(442, 352, 242, 24, "#2E3A46") + T(563, 364, "MOTOR DE INDUCCIÓN 3~", 15, "#FFFFFF", 800))
    filas = [("HP 10", "kW 7,5", "60 Hz"), ("V 230/460", "A 24,3/12,2", ""), ("rpm 1760", "F.S. 1,25", "Cód. H"),
             ("Ef. 91,7 %", "FP 0,84", "IP55"), ("Aisl. F", "40 °C", "TEFC"), ("BAJA: T1-T6-T7 · T2-T4-T8 · T3-T5-T9", "", ""),
             ("ALTA: T4-T7 · T5-T8 · T6-T9", "", "")]
    for k, f in enumerate(filas):
        y = 392 + k * 21
        if f[1]:
            for t, x in zip(f, (448, 548, 640)):
                c.append(T(x, y, t, 14, "#1B1F24", 700, "start"))
        else:
            c.append(T(448, y, f[0], 12.5, "#1B1F24", 700, "start"))
        c.append(R(442, y + 10, 242, 1, "#9AA0A6"))
    c.append(PL(920, 200, ref, s_mm, "end"))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {}, WH


# ============================================================ CAJA DE BORNES DEL MOTOR (fotos del usuario: placa verde, espárragos, puentes de acero)
def _tuerca(x, y, r=30):
    """Punto de conexión del motor: arandela y espárrago de COBRE con tuerca HEXAGONAL de acero."""
    import math
    pts = " ".join(f"{x + r * math.cos(math.radians(a)):.1f},{y + r * math.sin(math.radians(a)):.1f}" for a in range(0, 360, 60))
    return (f'<g filter="url(#sTorn)"><circle cx="{x}" cy="{y}" r="{r * 1.25:.1f}" fill="url(#rCobreR)"/>'
            f'<polygon points="{pts}" fill="url(#rAcero)" stroke="#7E848B" stroke-width="2"/></g>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.48:.1f}" fill="url(#rCobreR)" stroke="#7A3E16" stroke-width="2"/>'
            f'<circle cx="{x - 3}" cy="{y - 3}" r="{r * 0.18:.1f}" fill="#F4C9A0"/>')


def caja_bornes(tipo="6", conexion="delta", ancho_mm=110.0):
    """IEC 6 bornes: arriba U1 V1 W1, abajo W2 U2 V2 (Δ: puentes verticales U1-W2, V1-U2, W1-V2 · Y: puente W2-U2-V2).
    NEMA 9 puntas: columnas T1-T6-T7 / T2-T4-T8 / T3-T5-T9 (tensión baja) o T4-T7 / T5-T8 / T6-T9 (alta)."""
    filas = 2 if tipo == "6" else 3
    Wp, Hp = 600, 200 + 170 * filas
    s_mm = ancho_mm / Wp
    b, c = {}, ['<defs><linearGradient id="cjCaja" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4A4E53"/><stop offset="1" stop-color="#1E2023"/></linearGradient>'
                '<linearGradient id="cjPlaca" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9CED3"/><stop offset="1" stop-color="#9DA3AA"/></linearGradient>'
                '<radialGradient id="rCobreR" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#F2B98A"/><stop offset="0.55" stop-color="#C87533"/><stop offset="1" stop-color="#7A3E16"/></radialGradient></defs>']
    c.append(f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "url(#cjCaja)")}</g>' + R(0, 0, Wp, 5, "#6A6E73"))
    for x, y in ((34, 34), (Wp - 34, 34), (34, Hp - 34), (Wp - 34, Hp - 34)):
        c.append(f'<circle cx="{x}" cy="{y}" r="16" fill="#0E0F10"/><circle cx="{x}" cy="{y}" r="8" fill="#55595E"/>')
    xs = (170, 300, 430)
    ys = [100 + 170 * k + 70 for k in range(filas)]
    c.append(f'<g filter="url(#sDura)">{R(64, ys[0] - 75, 472, ys[-1] - ys[0] + 150, "url(#cjPlaca)")}</g>' + R(64, ys[0] - 75, 472, 5, "#E4E7EA"))
    for k in range(filas - 1):
        ym = (ys[k] + ys[k + 1]) / 2
        for x in (235, 365):
            c.append(f'<circle cx="{x}" cy="{ym}" r="26" fill="#8C939A"/><circle cx="{x}" cy="{ym}" r="17" fill="#2E3134"/>' + R(x - 10, ym - 3, 20, 6, "#8E949A") + R(x - 3, ym - 10, 6, 20, "#8E949A"))
    if tipo == "6":
        nombres = [("U1", "V1", "W1"), ("W2", "U2", "V2")]
    else:
        nombres = [("T1", "T2", "T3"), ("T6", "T4", "T5"), ("T7", "T8", "T9")] if conexion == "bajo" else [("T1", "T2", "T3"), ("T4", "T5", "T6"), ("T7", "T8", "T9")]
    # hilos del bobinado con su marcador (entran por arriba y por abajo, como en la foto)
    for fila, y in zip(nombres, ys):
        arriba = y == ys[0] or (tipo == "9" and y != ys[-1])
        for x, n in zip(xs, fila):
            if y == ys[0]:
                c.append(f'<path d="M{x},{y} V{y - 115}" stroke="#151617" stroke-width="16"/>')
            elif y == ys[-1]:
                c.append(f'<path d="M{x},{y} V{y + 115}" stroke="#151617" stroke-width="16"/>')
    # puentes de acero
    puente = lambda x0, y0, x1, y1: f'<g filter="url(#sDura)"><rect x="{min(x0, x1) - 24}" y="{min(y0, y1) - 24}" width="{abs(x1 - x0) + 48}" height="{abs(y1 - y0) + 48}" rx="8" fill="url(#rAcero)"/></g>'
    if tipo == "6":
        if conexion == "delta":
            for x in xs:
                c.append(puente(x, ys[0], x, ys[1]))
        else:
            c.append(puente(xs[0], ys[1], xs[2], ys[1]))
    else:
        for x in xs:
            c.append(puente(x, ys[0] if conexion == "bajo" else ys[1], x, ys[2]))
    for fila, y in zip(nombres, ys):
        for x, n in zip(xs, fila):
            c.append(_tuerca(x, y))
            b[n] = (x, y)
    # numeración impresa en el plástico aislante, junto a cada punto de conexión
    for fila, y in zip(nombres, ys):
        for x, n in zip(xs, fila):
            c.append(T(x - 56, y + 48, n, 20, "#1B1F24", 800, "end"))
    tit = {"delta": "Conexión triángulo (Δ)", "estrella": "Conexión estrella (Y)", "bajo": "NEMA 9 puntas · tensión baja", "alto": "NEMA 9 puntas · tensión alta"}[conexion]
    svg, WH = svg_mm(Wp, Hp + 50, s_mm, "".join(c) + T(Wp / 2, Hp + 28, tit, 26, "#1B1F24", 800))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ BORNERAS DE CABALLETE (referencias #23 a #25)
def bornera(nombres=("L1", "L2", "L3", "N", "PE"), tipos=None, ref="X0", paso_mm=6.2):
    """Paquete de bornes de paso en riel, sin contornos (se separan por sombra).
    Gris = paso · azul = neutro (N) · verde/amarillo = tierra (PE). Tornillos de ranura como los del S7-1200.
    Separador al inicio y al final del paquete; la etiqueta (-X0…) va en el separador."""
    tipos = tipos or {}
    P, Hp = 80, 400
    n = len(nombres)
    S = 64                     # separador (ancho = alto de la etiqueta)
    Wp = S + P * n + S
    s_mm = paso_mm / P
    b, c = {}, ['<defs><linearGradient id="bGris" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C9CBCE"/><stop offset="0.75" stop-color="#A9ABAE"/><stop offset="1" stop-color="#8A8D91"/></linearGradient>'
                '<linearGradient id="bAzul" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6E93CC"/><stop offset="0.75" stop-color="#4A6FA5"/><stop offset="1" stop-color="#36588C"/></linearGradient>'
                '<linearGradient id="bSep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E9399"/><stop offset="0.5" stop-color="#6E747B"/><stop offset="1" stop-color="#565B61"/></linearGradient></defs>']
    for i, nm in enumerate(nombres):
        x0 = S + P * i
        t = tipos.get(nm, "PE" if nm == "PE" else ("N" if nm == "N" else ""))
        if t == "PE":
            cuerpo = (f'<rect x="{x0}" y="0" width="{P}" height="{Hp}" fill="#2E9E44"/><rect x="{x0 + P / 2}" y="0" width="{P / 2}" height="{Hp}" fill="#F2D21B"/>'
                      f'<rect x="{x0 + P - 10}" y="0" width="10" height="{Hp}" fill="#000" opacity="0.16"/>')
        elif t == "N":
            cuerpo = R(x0, 0, P, Hp, "url(#bAzul)")
        else:
            cuerpo = R(x0, 0, P, Hp, "url(#bGris)")
        c.append(f'<g filter="url(#sDura)">{cuerpo}</g>' + R(x0, 0, P, 4, "#FFFFFF", 'opacity="0.45"'))
        for y in (80, 320):            # marcador en blanco (se rotula al conectar)
            c.append(f'<g filter="url(#sTorn)">{R(x0 + 8, y - 15, P - 16, 30, "#FFFFFF")}</g>')
        for y in (140, 260):
            c.append(_torn_ranura(x0 + P / 2, y, 24))
            b[f"{nm}_{'a' if y == 140 else 'b'}"] = (x0 + P / 2, y)
        c.append(f'<circle cx="{x0 + P / 2}" cy="200" r="10" fill="#1B1F24"/>')
    # separadores (más altos que los bornes) y etiqueta del paquete en el separador de inicio
    for xs in (0, S + P * n):
        c.append(f'<g filter="url(#sDura)">{R(xs, -30, S, Hp + 60, "url(#bSep)")}</g>' + R(xs, -30, S, 4, "#B5BAC0"))
    c.append(PL(S / 2, Hp / 2, ref, s_mm, rot=-90))
    svg, WH = svg_mm(Wp, Hp + 60, s_mm, f'<g transform="translate(0,30)">{"".join(c)}</g>')
    return svg, {k: (x * s_mm, (y + 30) * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ LOGO! 8 12/24RCE + LOGO!Power 24 V 1,3 A (referencia del usuario, se conserva la marca)
def _torn_logo(x, y, r=16):
    """Mismo tornillo de ranura que el S7-1200 (cabeza gris, aro negro, ranura en diagonal)."""
    return _torn_ranura(x, y, r)


def _regleta(x0, x1, y, h=70):
    """Conector negro de bornes como el del S7-1200 (franja oscura con sombra)."""
    return f'<g filter="url(#sDura)">{R(x0, y - h / 2, x1 - x0, h, "url(#pFranja)", 'rx="8"')}</g>'


def logo_power(ref="T1", alto_mm=90.0):
    """LOGO!Power 24 V 1,3 A: todos los bornes arriba (L N | + + − −); LED O.K. y potenciómetro de ajuste."""
    Wp, Hp = 265, 660
    s_mm = alto_mm / Hp
    b, c = {}, [f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#7B8592")}</g>']
    c.append(R(0, 0, Wp, 150, "#727C89") + R(0, 150, Wp, 4, "#4E5662") + R(0, 545, Wp, 115, "#6E7885") + R(0, 545, Wp, 4, "#4E5662"))
    pos = (("L", 30), ("N", 72), ("+", 118), ("+2", 157), ("−", 196), ("−2", 235))   # separados: ningún tornillo se toca
    c.append(_regleta(8, 94, 52, 52) + _regleta(97, 257, 52, 52))
    for n, x in pos:
        c.append(T(x, 14, n[0], 16, "#E3E6EA", 700) + _torn_logo(x, 52, 13))
        b[n] = (x, 52)
    c.append(T(51, 92, "INPUT", 10.5, "#E3E6EA", 700) + T(51, 106, "AC 100-240V", 10, "#E3E6EA", 600) + T(176, 92, "OUTPUT", 10.5, "#E3E6EA", 700) + T(176, 106, "DC 24V/1.3A", 10, "#E3E6EA", 600))
    c.append(R(112, 118, 128, 26, "none", 'stroke="#C9CDD2" stroke-width="2"'))
    c.append(f'<g filter="url(#sTorn)">{R(12, 175, 116, 36, "#F2F3F4")}</g>' + T(70, 193, "SIEMENS", 21, "#3B6E7A", 800))
    c.append(T(250, 190, "LOGO!", 32, "#F2F3F4", 400, "end") + T(250, 222, "Power", 20, "#F2F3F4", 400, "end"))
    c.append(T(200, 275, "O.K.", 14, "#E3E6EA", 700, "end") + R(208, 266, 18, 18, "#2BD14A"))
    c.append(PL(Wp / 2, 450, ref, s_mm))
    c.append(f'<g filter="url(#sTorn)"><circle cx="190" cy="600" r="22" fill="#0E0F10"/></g><circle cx="190" cy="600" r="16" fill="url(#rPerilla)"/>'
             f'<line x1="180" y1="590" x2="200" y2="610" stroke="#0A0A0B" stroke-width="5"/>' + T(150, 640, "22,2…26,4 V", 12, "#E3E6EA", 600))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


def logo8(ref="A1", alto_mm=90.0):
    """LOGO! 8 12/24RCE (6ED1052-1MD08-0BA1): arriba L+ M I1…I8 (I1, I2 = AI3, AI4 · I7, I8 = AI1, AI2, 0–10 V);
    abajo Q1…Q4, cada salida a relé con sus bornes 1 y 2 y el contacto NA impreso."""
    Wp, Hp = 530, 660
    s_mm = alto_mm / Hp
    b, c = {}, [f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "#7B8592")}</g>']
    c.append(R(0, 0, Wp, 150, "#727C89") + R(0, 150, Wp, 4, "#4E5662") + R(0, 545, Wp, 115, "#6E7885") + R(0, 545, Wp, 4, "#4E5662"))
    c.append(_regleta(34, 132, 54, 56) + _regleta(132 + 4, 500, 54, 56))
    for q in range(4):
        c.append(_regleta(60 + q * 122 - 26, 60 + q * 122 + 72, 600, 56))
    for k, n in enumerate(["L+", "M", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"]):
        x = 60 + k * 46
        c.append(T(x, 16, n, 14, "#E3E6EA", 700) + _torn_logo(x, 54, 16))
        b[n] = (x, 54)
    c.append(T(14, 100, "I1, I2 = AI3, AI4 (0..10V)", 12, "#E3E6EA", 600, "start") + T(14, 120, "I7, I8 = AI1, AI2 (0..10V)", 12, "#E3E6EA", 600, "start"))
    c.append(T(515, 100, "DC 12/24V INPUT 8xDC", 11, "#E3E6EA", 600, "end") + R(380, 112, 135, 30, "none", 'stroke="#C9CDD2" stroke-width="2"'))
    # frente: pantalla y teclado
    c.append(f'<g filter="url(#sDura)">{R(5, 172, 310, 330, "#151618")}</g>')
    c.append(R(14, 184, 128, 34, "#3E8C95") + T(78, 201, "SIEMENS", 21, "#F2F3F4", 800) + T(304, 201, "LOGO!", 34, "#F2F3F4", 400, "end"))
    c.append(R(36, 236, 248, 210, "#5F8A72") + R(36, 236, 248, 8, "#4C6F5C"))
    c.append(T(40, 466, "LAN", 15, "#F2F3F4", 700, "start") + R(40, 480, 16, 12, "#2BD14A"))
    c.append(f'<g filter="url(#sTorn)">{R(330, 175, 185, 78, "#7B8592")}</g>' + R(338, 186, 44, 32, "none", 'stroke="#1B1F24" stroke-width="3"') + R(436, 238, 60, 10, "#141516"))
    for (x, y, t) in ((415, 300, "▲"), (360, 350, "◀"), (470, 350, "▶"), (415, 400, "▼"), (360, 450, "ESC")):
        c.append(f'<g filter="url(#sTorn)">{R(x - 25, y - 25, 50, 50, "#D7DEE4")}</g>' + T(x, y, t, 14 if len(t) > 1 else 18, "#7A8792", 800))
    c.append(f'<g filter="url(#sTorn)">{R(445, 425, 50, 50, "#3E9E4A")}</g>' + T(470, 450, "OK", 15, "#FFFFFF", 800))
    c.append(T(420, 495, "6ED1052-1MD08-0BA1", 12, "#E3E6EA", 600))
    c.append(PL(160, 525, ref, s_mm))
    c.append(T(140, 562, "OUTPUT 4xRELAY/10A", 13, "#E3E6EA", 600, "start"))
    for q in range(4):
        x1 = 60 + q * 122
        x2 = x1 + 46
        for x, n in ((x1, "1"), (x2, "2")):
            c.append(_torn_logo(x, 600, 16))
            b[f"Q{q + 1}.{n}"] = (x, 600)
        # contacto NA impreso entre los bornes 1 y 2
        c.append(f'<path d="M{x1},622 V636 H{x1 + 12} L{x1 + 30},624 M{x1 + 32},636 H{x2} V622" stroke="#E3E6EA" stroke-width="2.4" fill="none"/>')
        c.append(T(x1 - 12, 640, "1", 12, "#E3E6EA", 700) + T(x2 + 12, 640, "2", 12, "#E3E6EA", 700) + T((x1 + x2) / 2, 652, f"Q{q + 1}", 13, "#E3E6EA", 800))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {k: (x * s_mm, y * s_mm) for k, (x, y) in b.items()}, WH


# ============================================================ ACCESORIOS
def riel_canaleta(ancho_mm=200.0):
    """Riel DIN 35 × 7,5 mm perforado (EN 60715) sobre placa y canaleta ranurada gris en vertical y horizontal."""
    Wp, Hp = 1000, 520
    s_mm = ancho_mm / Wp
    c = ['<defs><linearGradient id="gGalv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E4E7EA"/><stop offset="0.5" stop-color="#CBD0D5"/><stop offset="1" stop-color="#DDE1E5"/></linearGradient></defs>',
         f'<g filter="url(#sCuerpo)">{R(0, 0, Wp, Hp, "url(#gGalv)")}</g>']
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
    c.append(T(500, 40, "Placa de montaje del tablero (galvanizada)", 22, "#4A4F55", 700))
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


_DEF_MED = ('<defs><linearGradient id="mAma" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E8A800"/><stop offset="0.25" stop-color="#FFC81E"/><stop offset="0.8" stop-color="#FFC81E"/><stop offset="1" stop-color="#D99A00"/></linearGradient>'
            '<linearGradient id="mRoja" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B8141C"/><stop offset="0.3" stop-color="#F0383E"/><stop offset="1" stop-color="#C21A20"/></linearGradient>'
            '<linearGradient id="mCara" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4D52"/><stop offset="1" stop-color="#34373B"/></linearGradient>'
            '<radialGradient id="mDial" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#FFE27A"/><stop offset="0.6" stop-color="#FFC81E"/><stop offset="1" stop-color="#C48A00"/></radialGradient>'
            '<linearGradient id="mLcd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D5DCCB"/><stop offset="1" stop-color="#B9C3AE"/></linearGradient></defs>')


def _lcd(c, x, y, w, h, lectura, unidad, size):
    c.append(f'<g filter="url(#sTorn)">{R(x, y, w, h, "url(#mLcd)", 'rx="8"')}</g>')
    c.append(f'<text x="{x + w - 18}" y="{y + h / 2 + 6}" font-family="DSEG7 Classic, monospace" font-size="{size}" fill="#1B1F24" text-anchor="end" dominant-baseline="central">{lectura}</text>')
    c.append(T(x + w - 14, y + 18, unidad, 18, "#1B1F24", 800, "end"))


def pinza(lectura="24,3", unidad="AC", alto_mm=230.0):
    """Pinza amperimétrica TRMS calcada del original del usuario (sin marca: logo ME.):
    mordaza roja con marcas de CAT y 1000 A, gatillo rojo, cuerpo amarillo, cara gris con selector giratorio
    (A~ Hz, A⎓ ZERO, iFlex, Ω/continuidad/capacidad, mV/V⎓, V~, OFF), botón SAVE, pantalla 999,9 Amps,
    botones INRUSH, MIN MAX y luz, bornes COM, tierra y VΩ con su categoría."""
    Wp, Hp = 780, 1500
    s_mm = alto_mm / Hp
    O = "#E8A33A"   # textos naranja de la cara
    W_ = "#F2F3F4"
    c = [_DEF_MED, '<defs><linearGradient id="mCaraG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4C4F54"/><stop offset="1" stop-color="#3B3E43"/></linearGradient>'
         '<radialGradient id="mPerillaG" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#5B5E63"/><stop offset="0.8" stop-color="#3F4247"/><stop offset="1" stop-color="#2C2E32"/></radialGradient>'
         '<linearGradient id="mLcdG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4E7E6"/><stop offset="1" stop-color="#C9CDCC"/></linearGradient></defs>']
    # mordaza (dos quijadas que se juntan arriba) con la abertura
    c.append(f'<g filter="url(#sCuerpo)"><path d="M232,490 V250 Q232,92 395,88 Q558,92 558,250 V490 H468 V270 Q468,170 395,166 Q322,170 322,270 V490 Z" fill="url(#mRoja)"/></g>')
    c.append(R(392, 86, 6, 82, "#7A1014"))
    for x in (342, 448):
        c.append(R(x - 18, 110, 36, 30, "#B8141C", 'stroke="#7A1014" stroke-width="2"') + T(x, 125, "ϟ", 20, "#5E0C0F", 800))
    c.append(R(258, 362, 26, 4, "#7A1014") + R(506, 362, 26, 4, "#7A1014"))
    for k, t in enumerate(("CAT III", "1000V", "CAT IV", "600V")):
        c.append(T(262, 398 + k * 18, t, 14, "#7A1014", 800))
    c.append(T(522, 450, "1000A", 15, "#7A1014", 800))
    # gatillo y cuerpo
    c.append(f'<g filter="url(#sDura)"><path d="M228,660 L135,745 Q122,770 150,780 L240,795 Z" fill="url(#mRoja)"/></g>')
    c.append(f'<g filter="url(#sDura)"><path d="M548,520 H578 V585 H548 Z" fill="url(#mRoja)"/></g>')
    c.append(f'<g filter="url(#sCuerpo)"><path d="M232,470 H558 Q575,470 575,500 V1390 Q575,1420 545,1420 H245 Q215,1420 215,1390 V500 Q215,470 232,470 Z" fill="url(#mAma)"/></g>')
    c.append(f'<g filter="url(#sTorn)"><path d="M265,590 H530 Q545,590 545,605 V1380 Q545,1395 530,1395 H260 Q245,1395 245,1380 V605 Q245,590 265,590 Z" fill="url(#mCaraG)"/></g>')
    # cabecera: logo del canal y leyenda
    c.append(f'<g filter="url(#sTorn)">{R(262, 602, 96, 32, "#F5B700")}</g>' + logo(280, 605, 26) + T(370, 618, "TRMS", 20, W_, 800, "start"))
    c.append(T(262, 648, "CLAMP METER", 13, W_, 700, "start"))
    # selector giratorio (perilla gris oscuro) y posiciones
    kx, ky = 455, 830
    c.append(f'<g filter="url(#sMando)"><circle cx="{kx}" cy="{ky}" r="102" fill="url(#mPerillaG)"/></g><circle cx="{kx}" cy="{ky}" r="102" fill="none" stroke="#1E2023" stroke-width="3"/>')
    c.append(f'<line x1="{kx - 52}" y1="{ky - 42}" x2="{kx - 36}" y2="{ky - 28}" stroke="{W_}" stroke-width="7" stroke-linecap="round"/>')
    pos = (("Hz", 352, 690, O), ("Ã", 372, 712, W_), ("ZERO", 425, 672, O), ("A⎓", 448, 692, W_), ("Hz", 516, 660, O), ("iFlex", 514, 684, W_),
           ("⊣⊢ ·)))", 312, 750, O), ("Ω", 333, 778, W_), ("mV", 290, 832, O), ("V⎓", 334, 832, W_), ("Ṽ", 340, 894, W_), ("OFF", 380, 932, W_))
    for t, x, y, col in pos:
        c.append(T(x, y, t, 22 if t in ("Ã", "A⎓", "Ω", "V⎓", "Ṽ") else 15, col, 800))
    c.append(f'<g filter="url(#sTorn)">{R(276, 905, 46, 46, "#2F7CC9", 'rx="8"')}</g>' + f'<circle cx="299" cy="928" r="11" fill="#F5B700"/>' + T(299, 888, "SAVE", 13, "#3FA0E8", 800))
    # pantalla
    c.append(f'<g filter="url(#sTorn)">{R(292, 990, 196, 150, "url(#mLcdG)", 'rx="6"')}</g>')
    c.append(T(468, 1020, "Amps", 20, "#1B1F24", 800, "end") + T(468, 1044, unidad, 20, "#1B1F24", 800, "end"))
    c.append(f'<text x="474" y="1098" font-family="DSEG7 Classic, monospace" font-size="56" fill="#1B1F24" text-anchor="end" dominant-baseline="central">{lectura}</text>')
    # botones
    c.append(T(292, 1172, "LOG 2sec", 12, W_, 700, "start") + T(470, 1172, "☼ 2sec", 12, W_, 700, "end"))
    for x, t, col in ((316, "INRUSH", "#4A4D52"), (392, "MIN\nMAX", "#4A4D52")):
        c.append(f'<g filter="url(#sTorn)">{R(x - 30, 1186, 60, 34, "#5E6166", 'rx="6" stroke="#2A2C30" stroke-width="2"')}</g>')
    c.append(T(316, 1203, "INRUSH", 11, W_, 800) + T(392, 1197, "MIN", 11, W_, 800) + T(392, 1210, "MAX", 11, W_, 800))
    c.append(f'<g filter="url(#sTorn)">{R(440, 1186, 56, 34, "#F5A300", 'rx="6"')}</g>')
    # bornes de prueba
    c.append(T(395, 1258, "CAT III 1000V", 11, "#1B1F24", 800) + T(395, 1272, "CAT IV 600V", 11, "#1B1F24", 800))
    c.append(f'<path d="M335,1290 V1282 H455 V1290" stroke="#1B1F24" stroke-width="2" fill="none"/>')
    c.append(T(330, 1300, "COM", 24, "#2A2C30", 800) + T(460, 1300, "VΩ", 24, "#2A2C30", 800))
    c.append(f'<path d="M395,1286 V1308 M383,1308 H407 M387,1315 H403 M391,1322 H399" stroke="#2A2C30" stroke-width="2.5"/>')
    c.append(R(363, 1285, 3, 110, "#2A2C30", 'opacity="0.6"') + R(425, 1285, 3, 110, "#2A2C30", 'opacity="0.6"'))
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {"COM": (330 * s_mm, 1395 * s_mm), "VΩ": (460 * s_mm, 1395 * s_mm)}, WH


def multimetro(lectura="144.0", unidad="Ω", alto_mm=190.0):
    """Multímetro digital en el mismo estilo: funda amarilla, cara gris, pantalla, selector amarillo y bornes A, COM, VΩ (CAT III 600 V)."""
    import math
    Wp, Hp = 420, 820
    s_mm = alto_mm / Hp
    c = [_DEF_MED]
    c.append(f'<g filter="url(#sCuerpo)">{R(10, 10, 400, 800, "url(#mAma)", 'rx="46"')}</g>')
    c.append(f'<g filter="url(#sTorn)">{R(45, 45, 330, 730, "url(#mCara)", 'rx="22"')}</g>')
    c.append(logo(70, 66, 26) + T(350, 80, "TRMS · CAT III 600 V", 13, "#FFFFFF", 800, "end"))
    _lcd(c, 70, 110, 280, 150, lectura, unidad, 74)
    for k, t in enumerate(("HOLD", "MIN MAX", "RANGE")):
        c.append(f'<g filter="url(#sTorn)">{R(70 + k * 96, 285, 88, 40, "#5B5F66", 'rx="6"')}</g>' + T(114 + k * 96, 305, t, 13, "#FFFFFF", 800))
    cx, cy = 210, 480
    for k, t in enumerate(("OFF", "Ṽ", "V⎓", "mV", "Ω", "→|", "A")):
        a = math.radians(210 - k * 40)
        c.append(T(cx + 118 * math.cos(a), cy - 118 * math.sin(a), t, 20, "#FFFFFF", 800))
    c.append(f'<g filter="url(#sMando)"><circle cx="{cx}" cy="{cy}" r="86" fill="url(#mDial)"/></g>')
    c.append(R(cx - 16, cy - 80, 32, 160, "#E0A800", f'rx="10" transform="rotate({90 - (210 - 4 * 40)} {cx} {cy})"'))
    ap = math.radians(210 - 4 * 40)
    c.append(f'<path d="M{cx},{cy} L{cx + 76 * math.cos(ap):.1f},{cy - 76 * math.sin(ap):.1f}" stroke="#7A5600" stroke-width="8" stroke-linecap="round"/>')
    for x, t, col in ((105, "A", "#C8202B"), (210, "COM", "#1B1F24"), (315, "VΩ", "#C8202B")):
        c.append(T(x, 650, t, 16, "#FFFFFF", 800) + f'<g filter="url(#sTorn)"><circle cx="{x}" cy="705" r="32" fill="#0E0F10"/></g><circle cx="{x}" cy="705" r="22" fill="none" stroke="{col}" stroke-width="7"/><circle cx="{x}" cy="705" r="9" fill="#3A3B3E"/>')
    svg, WH = svg_mm(Wp, Hp, s_mm, "".join(c))
    return svg, {"A": (105 * s_mm, 705 * s_mm), "COM": (210 * s_mm, 705 * s_mm), "VΩ": (315 * s_mm, 705 * s_mm)}, WH


def puntas(alto_mm=200.0):
    """Par de puntas de prueba (roja y negra) con cable flexible y protector."""
    Wp, Hp = 300, 900
    s_mm = alto_mm / Hp
    c = []
    for x, col, osc in ((95, "#D7262C", "#8E1418"), (205, "#2B2C2E", "#0B0B0C")):
        c.append(f'<g filter="url(#sDura)"><path d="M{x},90 C{x - 80},300 {x + 80},460 {x},640" stroke="{col}" stroke-width="10" fill="none"/></g>')
        c.append(R(x - 6, 0, 12, 24, "url(#rAcero)") + f'<g filter="url(#sDura)">{R(x - 22, 20, 44, 72, col, 'rx="8"')}</g>')
        c.append(f'<g filter="url(#sDura)"><path d="M{x - 18},640 H{x + 18} L{x + 12},850 H{x - 12} Z" fill="{col}"/></g>' + R(x - 26, 630, 52, 16, osc, 'rx="6"'))
        c.append(R(x - 3, 850, 6, 44, "url(#rAcero)"))
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
    c.append(PL(882, 600, ref, s_mm))
    c.append(T(882, 655, "CPU 1212C", 30, TX, 400) + T(884, 697, "AC/DC/RLY", 30, TX, 400))
    c.append(T(666, 786, "DQ a", 13, TX, 400, "start") + f'<path d="M668,830 V805 H968 V830" {br}/>' + "".join(T(683 + i * 39, 823, f".{i}", 17, TX) for i in range(6)))
    c.append(R(40, 931, 22, 22, "#C1C7D0") + T(78, 942, "LINK", 19, TX, 400, "start"))
    c.append(R(40, 978, 22, 22, "#C1C7D0") + T(78, 989, "Rx/Tx", 19, TX, 400, "start"))
    c.append(T(538, 1069, "DQ a", 13, TX, 400, "start") + T(762, 1072, "RELAY OUTPUTS", 21, TX))
    c.append(f'<path d="M540,1128 V1104 H805 V1128" {br}/><path d="M823,1128 V1104 H985 V1128" {br}/>')
    for x, n in zip(xs_inf, nom_inf):
        c.append(T(x - 8 if n in ("1L", "2L") else x - 10, 1125, n, 18, TX))
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


# ============================================================ OPERADOR 22 mm + SU CONTACTO (captura de referencia del usuario)
def _bloque_lateral(c, n1, n2, tipo):
    """Bloque de contacto visto de frente como en la referencia: tornillos de conexión arriba (n1) y abajo (n2)
    con su número impreso, ventana de color (NC rojo / NO verde / LED blanco), leva semicircular, pestaña gris
    de enganche y tornillo de fijación a la izquierda. Cuerpo GRIS con sombra para que contraste."""
    col = {"NC": "#C8202B", "NO": "#2E8B3E", "LED": "#F4F4F2"}[tipo]
    c.append(f'<g filter="url(#sMando)">{R(230, 450, 335, 410, "url(#gOpGris)")}</g>' + R(230, 450, 335, 5, "#D5D9DD") + R(230, 855, 335, 5, "#5A6068"))
    c.append(R(300, 470, 80, 100, "#7C838B") + R(300, 735, 80, 100, "#7C838B") + R(440, 470, 100, 60, "#7C838B") + R(440, 780, 100, 60, "#7C838B"))
    for y, n in ((528, n1), (785, n2)):
        c.append(f'<g filter="url(#sTorn)"><circle cx="340" cy="{y}" r="30" fill="url(#rPerilla)"/></g>' + T(402, y, n, 30, "#1B1F24", 800, rot=90))
    c.append(f'<g filter="url(#sTorn)"><circle cx="268" cy="656" r="34" fill="url(#rAcero)" stroke="#6E747B" stroke-width="2"/></g>' + R(248, 653, 40, 7, "#6E747B") + R(265, 636, 7, 40, "#6E747B"))
    c.append(R(322, 618, 48, 76, col, 'stroke="#2A2D31" stroke-width="2"' if tipo == "LED" else ""))
    c.append(T(400, 656, tipo, 30, "#1B1F24", 800, rot=90))
    if tipo != "LED":
        c.append(f'<path d="M428,586 A70,70 0 0 1 428,726" fill="{col}" stroke="#2A2D31" stroke-width="14"/>')
    c.append(f'<g filter="url(#sTorn)">{R(525, 590, 40, 140, "#B9BEC3")}</g>' + f'<circle cx="546" cy="657" r="10" fill="#0E0F10"/>')


def _cuerpo_operador(c):
    """Cuerpo del operador visto de lado (gris, con la pestaña de enganche del bloque) y el aro moleteado."""
    c.append(f'<g filter="url(#sMando)">{R(650, 460, 150, 380, "url(#gOpGris)")}</g>' + R(650, 460, 150, 4, "#D5D9DD"))
    c.append(f'<g filter="url(#sTorn)">{R(636, 580, 22, 50, "url(#rAcero)", 'rx="6"')}</g>')
    c.append(f'<g filter="url(#sMando)">{R(760, 420, 240, 440, "url(#gOpGris)")}</g>' + R(760, 420, 240, 4, "#D5D9DD") + R(760, 855, 240, 5, "#5A6068"))
    c.append(R(800, 540, 4, 200, "#5A6068", 'opacity="0.6"') + R(895, 860, 30, 10, "#5A6068"))


def _aro(c, cx=1005, cy=650, rx=105, ry=215):
    import math
    c.append(f'<g filter="url(#sMando)"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#gAroOp)"/></g>')
    for k in range(40):     # moleteado del aro
        a = math.radians(100 + k * 4)
        c.append(f'<line x1="{cx + rx * math.cos(a):.1f}" y1="{cy - ry * math.sin(a):.1f}" x2="{cx + (rx - 12) * math.cos(a):.1f}" y2="{cy - (ry - 12) * math.sin(a):.1f}" stroke="#7E848B" stroke-width="2.5"/>')


def operador_y_contacto(tipo="pulsador", color="verde", simbolo="I", ref="S1", contacto="NO", n1="3", n2="4", encendido=False, ancho_mm=95.0):
    """Lámina como la captura del usuario: a la izquierda el bloque de contacto (punto de conexión real),
    flecha que indica que se acopla detrás del operador, y a la derecha el operador visto de lado con su cabeza.
    tipo: pulsador · emergencia · selector · piloto. La etiqueta va DEBAJO del operador."""
    Wp, Hp = 1190, 720
    s_mm = ancho_mm / Wp
    c = ['<defs><linearGradient id="gOpGris" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B7BCC1"/><stop offset="0.5" stop-color="#9097A0"/><stop offset="1" stop-color="#6E757E"/></linearGradient>'
         '<linearGradient id="gAroOp" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9AA0A6"/><stop offset="0.45" stop-color="#F4F5F6"/><stop offset="1" stop-color="#C9CDD1"/></linearGradient></defs>']
    _bloque_lateral(c, n1, n2, contacto)
    # flecha azul: el bloque se monta detrás del operador
    c.append('<path d="M520,380 Q640,250 760,350" stroke="#1E8FB8" stroke-width="22" fill="none" stroke-linecap="round"/>'
             '<polygon points="792,382 728,372 770,318" fill="#1E8FB8"/>')
    _cuerpo_operador(c)
    import math
    if tipo == "pulsador":
        col = COLORES[color]
        _aro(c)
        gid = "gOp" + col[0].strip("#")
        c.append(f'<defs><radialGradient id="{gid}" cx="0.45" cy="0.35" r="0.8"><stop offset="0" stop-color="{col[2]}"/><stop offset="0.55" stop-color="{col[0]}"/><stop offset="1" stop-color="{col[1]}"/></radialGradient></defs>')
        c.append(f'<g filter="url(#sTorn)"><ellipse cx="1030" cy="650" rx="78" ry="172" fill="url(#{gid})"/></g>')
        if simbolo == "I":
            c.append(R(1046, 580, 14, 140, "#FFFFFF", 'opacity="0.9"'))
        else:
            c.append('<ellipse cx="1052" cy="650" rx="30" ry="62" fill="none" stroke="#FFFFFF" stroke-width="12" opacity="0.9"/>')
    elif tipo == "emergencia":
        c.append(R(1000, 560, 60, 180, "#3A3B3E"))
        c.append('<defs><radialGradient id="gHongoL" cx="0.55" cy="0.35" r="0.8"><stop offset="0" stop-color="#FF8A80"/><stop offset="0.5" stop-color="#E02A2F"/><stop offset="1" stop-color="#7E1014"/></radialGradient></defs>')
        c.append('<g filter="url(#sMando)"><path d="M1060,400 Q1170,420 1170,650 Q1170,880 1060,900 Z" fill="url(#gHongoL)"/></g>')
        c.append('<path d="M1080,470 Q1140,520 1140,620" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="12" fill="none" stroke-linecap="round"/>')
        c.append('<g filter="url(#sTorn)"><ellipse cx="985" cy="650" rx="22" ry="230" fill="#F5C518"/></g>')
    elif tipo == "selector":
        _aro(c)
        c.append('<g filter="url(#sTorn)"><ellipse cx="1030" cy="650" rx="78" ry="172" fill="url(#rMando)"/></g>')
        c.append('<g filter="url(#sMando)"><path d="M1040,470 H1130 V830 H1040 Z" fill="#1A1B1C"/></g>' + R(1060, 490, 14, 150, "#F4F4F2", 'rx="7"'))
    else:   # piloto
        lum = {"verde": ("#55F000", "#C9E8BE")}.get(color, ("#55F000", "#C9E8BE"))
        _aro(c)
        gid = f"gLente{int(encendido)}"
        if encendido:
            c.append(f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#F4FFE8"/><stop offset="0.35" stop-color="{lum[0]}"/><stop offset="1" stop-color="#2E9E10"/></radialGradient>'
                     f'<filter id="gBr" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter></defs>')
            c.append(f'<ellipse cx="1060" cy="650" rx="100" ry="190" fill="{lum[0]}" opacity="0.5" filter="url(#gBr)"/>')
        else:
            c.append(f'<defs><radialGradient id="{gid}" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="{lum[1]}"/><stop offset="1" stop-color="#8FA98A"/></radialGradient></defs>')
        c.append(f'<g filter="url(#sTorn)"><path d="M1010,478 Q1110,500 1110,650 Q1110,800 1010,822 Z" fill="url(#{gid})"/></g>')
        c.append('<path d="M1030,530 Q1080,560 1088,620" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="10" fill="none" stroke-linecap="round"/>')
    c.append(PL(900, 935, ref, s_mm))
    if tipo == "piloto":
        c.append(T(990, 935, "encendido" if encendido else "apagado", 34, "#1B1F24", 700, "start"))
    svg, WH = svg_mm(Wp, Hp, s_mm, '<g transform="translate(0,-260)">' + "".join(c) + "</g>")
    b = {n1: (340 * s_mm, 268 * s_mm), n2: (340 * s_mm, 525 * s_mm)}
    return svg, b, WH

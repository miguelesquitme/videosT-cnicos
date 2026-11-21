"""Símbolos IEC 60617 en SVG (referencia; el usuario entrega los diagramas definitivos).
Estilo Telesquemario: contacto fijo arriba, cuchilla que pivota abajo; marca de función en el contacto fijo
(semicírculo = contactor, × = disyuntor); números de bornes girados 90° a la izquierda del conductor.
Potencia trazo grueso, mando trazo fino. Ligera sombra para que se lea sobre el documento y en video.
Cada función devuelve (svg, {}, (W_mm, H_mm)) para render_svg.render_lote (1 unidad = 0,1 mm)."""
F = "Inter, Arial, sans-serif"
K = "#1B1F24"
SP, SC = 6, 3.6          # trazo de potencia / de mando


def envolver(W, H, cuerpo, m=20):
    defs = ('<defs><filter id="sSim" x="-10%" y="-10%" width="130%" height="130%"><feGaussianBlur in="SourceAlpha" stdDeviation="2.2"/>'
            '<feOffset dx="3" dy="4"/><feComponentTransfer><feFuncA type="linear" slope="0.28"/></feComponentTransfer>'
            '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-m} {-m} {W + 2 * m} {H + 2 * m}" width="{(W + 2 * m) / 10:.1f}mm" height="{(H + 2 * m) / 10:.1f}mm">'
           f'{defs}<g filter="url(#sSim)">{cuerpo}</g></svg>')
    return svg, {}, (W / 10, H / 10)


def T(x, y, s, size=26, peso=600, ancla="middle", rot=0, color=K):
    r = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{F}" font-size="{size}" font-weight="{peso}" fill="{color}" '
            f'text-anchor="{ancla}" dominant-baseline="central"{r}>{s}</text>')


def ln(x1, y1, x2, y2, w=SC, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{K}" stroke-width="{w}" stroke-linecap="round"{d}/>'


def pth(d, w=SC, fill="none"):
    return f'<path d="{d}" stroke="{K}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round"/>'


def num(x, y, s, size=24):
    """Número de borne girado 90° a la izquierda del conductor."""
    return T(x - 22, y, s, size, 600, rot=-90)


def contacto(x, y0, L=220, na=True, marca=None, n1="", n2="", w=SC, retardo=False):
    """Devuelve (svg, punto medio de la cuchilla) de un contacto vertical entre y0 y y0+L."""
    ya, yb = y0 + 0.36 * L, y0 + 0.66 * L
    s = [ln(x, y0, x, ya, w), ln(x, yb, x, y0 + L, w)]
    if na:
        xe, ye = x - 0.2 * L, ya - 0.02 * L
    else:
        s.append(ln(x, ya, x + 0.16 * L, ya, w))
        xe, ye = x + 0.2 * L, ya - 0.04 * L
    s.append(ln(x, yb, xe, ye, w))
    r = 0.045 * L
    if marca == "contactor":
        s.append(pth(f"M{x - r},{ya} A{r},{r} 0 0 0 {x + r},{ya}" if na else f"M{x - r},{ya} A{r},{r} 0 0 0 {x + r},{ya}", w * 0.75))
    elif marca == "disyuntor":
        s.append(ln(x - r, ya - r, x + r, ya + r, w * 0.8) + ln(x - r, ya + r, x + r, ya - r, w * 0.8))
    if retardo:   # marca de retardo a la conexión (paracaídas) sobre la cuchilla
        xm, ym = (x + xe) / 2, (yb + ye) / 2
        s.append(ln(xm, ym, xm - 0.22 * L, ym, w * 0.8) + pth(f"M{xm - 0.22 * L},{ym - 0.07 * L} A{0.07 * L},{0.07 * L} 0 0 0 {xm - 0.22 * L},{ym + 0.07 * L}", w * 0.8))
    if n1:
        s.append(num(x, y0 + 0.14 * L, n1))
    if n2:
        s.append(num(x, y0 + 0.88 * L, n2))
    return "".join(s), ((x + xe) / 2, (yb + ye) / 2)


def etiqueta(x, y, ref, size=30):
    return T(x, y, f"-{ref}", size, 700, "end")


def bobina(x, y0, ref, n1="A1", n2="A2", L=220, retardo=False):
    s = [ln(x, y0, x, y0 + 0.36 * L), ln(x, y0 + 0.64 * L, x, y0 + L)]
    s.append(f'<rect x="{x - 0.17 * L:.1f}" y="{y0 + 0.36 * L:.1f}" width="{0.34 * L:.1f}" height="{0.28 * L:.1f}" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>')
    if retardo:
        s.append(f'<rect x="{x - 0.17 * L:.1f}" y="{y0 + 0.36 * L:.1f}" width="{0.1 * L:.1f}" height="{0.28 * L:.1f}" fill="{K}"/>')
    s.append(num(x, y0 + 0.16 * L, n1) + num(x, y0 + 0.86 * L, n2) + etiqueta(x - 0.25 * L, y0 + 0.5 * L, ref))
    return "".join(s)


# ----------------------------------------------------------------------------------------------------------- símbolos
def disyuntor(n, ref, nums=None):
    """Símbolo impreso en el propio disyuntor: contacto con × por polo, polos unidos por línea de acción mecánica."""
    nums = nums or [(str(2 * i + 1), str(2 * i + 2)) for i in range(n)]
    W, H, dx = 140 + 110 * n, 300, 110
    s, mids = [], []
    for i in range(n):
        c, m = contacto(150 + i * dx, 40, 230, True, "disyuntor", *nums[i], w=SP)
        s.append(c)
        mids.append(m)
    if n > 1:
        s.append(ln(mids[0][0], mids[0][1], mids[-1][0], mids[-1][1], 2.5, "10 8"))
    s.append(etiqueta(95, 150, ref))
    return envolver(W, H, "".join(s))


def _caja_termica(x0, y, n, dx, h=56, magnetico=False):
    """Cajas de disparo PEGADAS entre polos: fila térmica (escalón) y, si aplica, fila magnética (I>)."""
    s = []
    filas = [("termico", y)] + ([("mag", y + h)] if magnetico else [])
    for tipo, yy in filas:
        s.append(f'<rect x="{x0 - dx / 2:.1f}" y="{yy:.1f}" width="{dx * n:.1f}" height="{h}" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>')
        for i in range(1, n):
            s.append(ln(x0 - dx / 2 + dx * i, yy, x0 - dx / 2 + dx * i, yy + h, SC))
        for i in range(n):
            x = x0 + i * dx
            if tipo == "termico":
                s.append(pth(f"M{x},{yy} V{yy + h * 0.22} H{x + 16} V{yy + h * 0.78} H{x} V{yy + h}", SP))
            else:
                s.append(ln(x, yy, x, yy + h, SP) + T(x + 26, yy + h / 2, "I&gt;", 20, 800))
    return "".join(s), y + h * len(filas)


def guardamotor(ref="QM1"):
    n, dx = 3, 120
    W, H = 560, 470
    s = []
    x0 = 220
    mids = []
    for i, (a, b) in enumerate((("1/L1", ""), ("3/L2", ""), ("5/L3", ""))):
        c, m = contacto(x0 + i * dx, 30, 210, True, "disyuntor", a, "", w=SP)
        s.append(c)
        mids.append(m)
    cj, yfin = _caja_termica(x0, 260, n, dx, 56, True)
    for i in range(n):
        s.append(ln(x0 + i * dx, 240, x0 + i * dx, 260, SP) + ln(x0 + i * dx, yfin, x0 + i * dx, yfin + 70, SP) + num(x0 + i * dx, yfin + 40, ("2/T1", "4/T2", "6/T3")[i]))
    s.append(cj)
    # mando manual ⊞ y línea de acción hacia los polos y los disparadores
    xm, ym = 80, mids[0][1]
    s.append(f'<rect x="{xm - 22}" y="{ym - 22}" width="44" height="44" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>' + ln(xm - 22, ym, xm + 22, ym, 2.5) + ln(xm, ym - 22, xm, ym + 22, 2.5))
    s.append(ln(xm + 22, ym, mids[-1][0], mids[-1][1], 2.5, "10 8") + ln(xm, ym + 22, xm, 316, 2.5, "10 8") + ln(xm, 316, x0 - dx / 2, 316, 2.5, "10 8"))
    s.append(etiqueta(xm - 30, ym, ref))
    return envolver(W, H, "".join(s))


def contactor(ref="KM1"):
    W, H = 900, 560
    s, mids = [], []
    for i, (a, b) in enumerate((("1", "2"), ("3", "4"), ("5", "6"))):
        c, m = contacto(180 + i * 110, 30, 230, True, "contactor", a, b, w=SP)
        s.append(c)
        mids.append(m)
    for x, na, a, b in ((560, True, "13", "14"), (680, False, "21", "22")):
        c, m = contacto(x, 30, 230, na, "contactor", a, b, w=SC)
        s.append(c)
        mids.append(m)
    s.append(ln(mids[0][0], mids[0][1], mids[-1][0] + 20, mids[-1][1], 2.5, "10 8"))
    s.append(etiqueta(120, 140, ref))
    s.append(bobina(400, 300, ref, L=240))
    return envolver(W, H, "".join(s))


def termico(ref="F2"):
    """Parte de potencia (disparadores térmicos pegados) y contactos 95-96 NC / 97-98 NA accionados por el mismo elemento térmico."""
    W, H = 980, 420
    s = []
    x0, dx = 170, 110
    for i, (a, b) in enumerate((("1", "2"), ("3", "4"), ("5", "6"))):
        x = x0 + i * dx
        s.append(ln(x, 30, x, 140, SP) + ln(x, 196, x, 330, SP) + num(x, 70, a) + num(x, 290, b))
    cj, _ = _caja_termica(x0, 140, 3, dx, 56)
    s.append(cj + etiqueta(x0 - dx / 2 - 20, 168, ref))
    # mando: elemento térmico (escalón en caja) y línea de acción a 95-96 y 97-98
    xt, yt = 600, 180
    s.append(f'<rect x="{xt - 30}" y="{yt - 30}" width="60" height="60" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>' + pth(f"M{xt - 20},{yt + 14} H{xt - 6} V{yt - 14} H{xt + 8} V{yt + 14} H{xt + 20}", SC))
    c1, m1 = contacto(760, 30, 300, False, None, "95", "96")
    c2, m2 = contacto(900, 30, 300, True, None, "97", "98")
    s.append(c1 + c2 + ln(xt + 30, yt, m2[0], yt, 2.5, "10 8"))
    s.append(etiqueta(xt - 40, yt - 60, ref, 26))
    return envolver(W, H, "".join(s))


def conmutado(x, y0, com, na, nc, L=260, retardo=False):
    """Conmutado: común abajo (pivote); NC a la izquierda con tope horizontal (cerrado en reposo); NA a la derecha, abierto."""
    yb, ya = y0 + 0.68 * L, y0 + 0.34 * L
    xnc, xna = x - 0.3 * L, x + 0.2 * L
    s = [ln(x, yb, x, y0 + L), num(x, y0 + 0.92 * L, com)]
    s.append(ln(xnc, y0, xnc, ya) + ln(xnc, ya, x - 0.12 * L, ya) + num(xnc, y0 + 0.12 * L, nc))
    s.append(ln(xna, y0, xna, ya + 0.06 * L) + num(xna, y0 + 0.12 * L, na))
    s.append(ln(x, yb, x - 0.14 * L, ya - 0.03 * L))
    xm, ym = x - 0.07 * L, (yb + ya) / 2 - 0.01 * L
    if retardo:
        s.append(ln(xm, ym, xm + 0.24 * L, ym, SC * 0.8) + pth(f"M{xm + 0.24 * L},{ym - 0.07 * L} A{0.07 * L},{0.07 * L} 0 0 1 {xm + 0.24 * L},{ym + 0.07 * L}", SC * 0.8))
    return "".join(s), (xm, ym)


def rele8(ref="KA1", timer=False):
    W, H = 860, 340
    s = [bobina(150, 40, ref, "2", "7", 260, retardo=timer)]
    c1, m1 = conmutado(470, 40, "1", "3", "4", retardo=timer)
    c2, m2 = conmutado(740, 40, "8", "6", "5", retardo=timer)
    s.append(c1 + c2 + ln(150 + 0.17 * 260, 170, m2[0], m2[1], 2.5, "10 8"))
    return envolver(W, H, "".join(s))


def _operador(tipo, xa, ya):
    """Mando manual a la izquierda de la línea de acción (xa, ya)."""
    if tipo == "pulsador":       # E
        return pth(f"M{xa},{ya - 22} H{xa - 16} V{ya + 22} H{xa}", SC)
    if tipo == "giro":           # mando rotativo
        return pth(f"M{xa + 2},{ya - 20} H{xa - 14} V{ya + 20} H{xa - 30}", SC)
    if tipo == "emergencia":     # cabeza de hongo
        return pth(f"M{xa},{ya - 26} A26,26 0 0 0 {xa},{ya + 26} Z", SC, K)
    if tipo == "flotador":       # flotador sobre el nivel del líquido
        return f'<circle cx="{xa - 22}" cy="{ya}" r="16" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>' + ln(xa - 50, ya + 22, xa + 4, ya + 22, 2.5)
    return ""


def mando(na, tipo, n1, n2, ref, funcion=None, W=420, H=320):
    x = 260
    c, m = contacto(x, 40, 240, na, None, n1, n2)
    xa = m[0] - 120
    s = [c, ln(xa, m[1], m[0] - (4 if na else -4), m[1], 2.5, "9 7"), _operador(tipo, xa, m[1])]
    if funcion:
        s.append(f'<circle cx="{x + 74}" cy="{m[1]}" r="22" fill="#FFFFFF" stroke="{K}" stroke-width="2.6"/>')
        s.append(ln(x + 74, m[1] - 12, x + 74, m[1] + 12, 3) if funcion == "I" else f'<circle cx="{x + 74}" cy="{m[1]}" r="10" fill="none" stroke="{K}" stroke-width="3"/>')
    if tipo == "emergencia":     # apertura positiva
        s.append(f'<circle cx="{x + 74}" cy="{m[1]}" r="22" fill="#FFFFFF" stroke="{K}" stroke-width="2.6"/>' + pth(f"M{x + 64},{m[1] + 10} L{x + 84},{m[1] - 10} M{x + 76},{m[1] - 10} H{x + 84} V{m[1] - 2}", 2.6))
    s.append(etiqueta(xa - 40, m[1], ref))
    return envolver(W, H, "".join(s))


def flotador(ref="S5"):
    W, H = 760, 320
    a = mando(True, "flotador", "C", "NA", ref)[0]
    b = mando(False, "flotador", "C", "NC", ref)[0]
    cuerpo = lambda sv: sv.split('<g filter="url(#sSim)">', 1)[1].rsplit("</g></svg>", 1)[0]
    return envolver(W, H, cuerpo(a) + f'<g transform="translate(360,0)">{cuerpo(b)}</g>')


def piloto(ref="H1"):
    W, H = 360, 320
    x, y = 220, 160
    s = [ln(x, 30, x, y - 40), ln(x, y + 40, x, 290), f'<circle cx="{x}" cy="{y}" r="40" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>',
         ln(x - 28, y - 28, x + 28, y + 28) + ln(x - 28, y + 28, x + 28, y - 28), num(x, 70, "X1"), num(x, 250, "X2"), etiqueta(x - 60, y, ref)]
    return envolver(W, H, "".join(s))


def sensor(tipo, ref):
    """Detector de proximidad de 3 hilos: caja con rombo (marca del principio) y salida NA; BN +, BK salida, BU −."""
    W, H = 520, 360
    s = [f'<rect x="150" y="100" width="150" height="150" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>',
         pth("M225,128 L262,175 L225,222 L188,175 Z", SC)]
    if tipo == "inductivo":
        s.append(f'<rect x="212" y="163" width="26" height="24" fill="{K}"/>')
    elif tipo == "capacitivo":
        s.append(ln(214, 158, 214, 192, 3) + ln(236, 158, 236, 192, 3))
    else:
        s.append(pth("M200,165 l22,0 m-7,-6 l7,6 l-7,6 M228,185 l22,0 m-7,-6 l7,6 l-7,6", 2.6))
    s.append(ln(225, 30, 225, 100) + ln(225, 250, 225, 330) + T(250, 45, "BN +", 22, 700, "start") + T(250, 315, "BU −", 22, 700, "start"))
    s.append(ln(300, 175, 360, 175) + pth("M360,175 V120 M360,235 V320 M360,235 L338,175", SC) + T(385, 300, "BK", 22, 700, "start"))
    s.append(etiqueta(135, 175, ref))
    return envolver(W, H, "".join(s))


def motor(ref="M1"):
    W, H = 420, 380
    s = [f'<circle cx="210" cy="250" r="90" fill="#FFFFFF" stroke="{K}" stroke-width="{SP}"/>', T(210, 230, "M", 46, 700), T(210, 280, "3~", 34, 700)]
    for x, t in ((150, "U1"), (210, "V1"), (270, "W1")):
        s.append(ln(x, 30, x, 250 - (90 ** 2 - (x - 210) ** 2) ** 0.5, SP) + num(x, 80, t))
    s.append(ln(330, 230, 380, 230, SC) + ln(380, 230, 380, 200, SC) + ln(365, 200, 395, 200, SC) + ln(370, 192, 390, 192, SC) + ln(376, 184, 384, 184, SC) + T(380, 160, "PE", 20, 700))
    s.append(etiqueta(110, 250, ref))
    return envolver(W, H, "".join(s))


def conexiones():
    """Δ y Y con los nombres de bornes IEC."""
    W, H = 760, 340
    s = []
    p = {"U": (120, 280), "V": (320, 280), "W": (220, 107)}
    s.append(pth(f"M{p['U'][0]},{p['U'][1]} L{p['W'][0]},{p['W'][1]} L{p['V'][0]},{p['V'][1]} Z", SP))
    for k, (x, y) in p.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{K}"/>')
    s.append(T(80, 300, "U1-W2", 22, 700) + T(360, 300, "V1-U2", 22, 700) + T(220, 70, "W1-V2", 22, 700) + T(220, 330, "Triángulo (Δ)", 24, 800))
    c = (560, 200)
    for ang, t in ((90, "U1"), (210, "V1"), (330, "W1")):
        import math
        x, y = c[0] + 110 * math.cos(math.radians(ang)), c[1] - 110 * math.sin(math.radians(ang))
        s.append(ln(c[0], c[1], x, y, SP) + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{K}"/>' + T(x + (0 if ang == 90 else (-30 if ang == 210 else 30)), y - 26 if ang == 90 else y + 26, t, 22, 700))
    s.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="9" fill="{K}"/>' + T(c[0] + 70, c[1] + 10, "W2-U2-V2", 20, 700, "start") + T(560, 330, "Estrella (Y)", 24, 800))
    return envolver(W, H, "".join(s))


def borneras():
    W, H = 760, 420
    s = []
    for fila, (ref, nombres) in enumerate((("X0", ["L1", "L2", "L3", "PE"]), ("X1", ["U", "V", "W", "PE"]), ("X2", ["1", "2", "3", "4", "5"]))):
        y = 70 + fila * 130
        s.append(etiqueta(110, y, ref))
        for i, n in enumerate(nombres):
            x = 170 + i * 110
            s.append(ln(x, y - 50, x, y - 14) + ln(x, y + 14, x, y + 50) + f'<circle cx="{x}" cy="{y}" r="14" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>' + T(x + 26, y - 34, str(i + 1), 18, 700, "start"))
            if n == "PE":
                s.append(ln(x + 30, y + 20, x + 58, y + 20, 2.6) + ln(x + 34, y + 28, x + 54, y + 28, 2.6) + ln(x + 39, y + 36, x + 49, y + 36, 2.6))
            s.append(T(x, y + 72, n, 18, 600))
    return envolver(W, H + 20, "".join(s))


def fuente(ref="T1"):
    W, H = 360, 360
    s = [f'<rect x="120" y="110" width="160" height="160" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>', ln(120, 270, 280, 110, 2.6),
         T(160, 150, "~", 36, 700), T(240, 235, "=", 34, 700)]
    for x, t in ((160, "L"), (240, "N")):
        s.append(ln(x, 30, x, 110) + num(x, 70, t))
    for x, t in ((160, "+"), (240, "−")):
        s.append(ln(x, 270, x, 340) + num(x, 310, t))
    s.append(etiqueta(105, 190, ref))
    return envolver(W, H, "".join(s))


def plc(ref, titulo, entradas, salidas, W=None):
    """PLC como caja: entradas arriba; salidas a relé abajo, cada una con su contacto NA entre sus dos bornes."""
    paso = 72
    n_sal = sum(len(g) for g in salidas)
    W = W or max(len(entradas), n_sal) * paso + 160
    H = 420
    s = [f'<rect x="120" y="110" width="{W - 150}" height="200" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>', T(120 + (W - 150) / 2, 170, titulo, 32, 800)]
    for i, t in enumerate(entradas):
        x = 150 + i * paso
        s.append(ln(x, 30, x, 110) + num(x, 70, t, 20))
    x = 150
    for grupo in salidas:            # grupo = (borne común o "1", borne de salida o "2", rótulo)
        com, out, rot = grupo
        s.append(ln(x, 230, x, 380) + num(x, 350, com, 20))
        s.append(ln(x + paso, 230, x + paso, 380) + num(x + paso, 350, out, 20))
        s.append(ln(x, 230, x + 18, 230) + ln(x + paso, 230, x + paso - 10, 230) + ln(x + 18, 230, x + paso - 18, 212, SC))
        s.append(T(x + paso / 2, 268, rot, 18, 700))
        x += paso * 2 + 20
    s.append(etiqueta(105, 210, ref))
    return envolver(W, H, "".join(s))


def logo_y_fuente():
    a = fuente("T1")[0]
    b = plc("A1", "LOGO! 12/24RCE", ["L+", "M", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"],
            [("1", "2", "Q1"), ("1", "2", "Q2"), ("1", "2", "Q3"), ("1", "2", "Q4")], W=900)[0]
    cuerpo = lambda sv: sv.split('<g filter="url(#sSim)">', 1)[1].rsplit("</g></svg>", 1)[0]
    return envolver(1400, 440, cuerpo(a) + f'<line x1="400" y1="0" x2="400" y2="420" stroke="#B9BDC1" stroke-width="2" stroke-dasharray="6 8"/>' + f'<g transform="translate(470,0)">{cuerpo(b)}</g>')


def s7_1200(ref="A1"):
    """CPU 1212C AC/DC/RLY: arriba L1 N PE (alimentación) L+ M (24 VDC sensores) 1M .0….7 (DI);
    abajo salidas a relé: 1L común de .0….3 y 2L común de .4 y .5 (contactos NA internos)."""
    paso = 66
    ent = ["L1", "N", "PE", "L+", "M", "1M", ".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7"]
    W, H = 150 + len(ent) * paso + 30, 440
    s = [f'<rect x="120" y="110" width="{W - 150}" height="210" fill="#FFFFFF" stroke="{K}" stroke-width="{SC}"/>', T(120 + (W - 150) / 2, 160, "CPU 1212C AC/DC/RLY", 32, 800)]
    for i, t in enumerate(ent):
        x = 150 + i * paso
        s.append(ln(x, 30, x, 110) + num(x, 70, t, 20))
    x = 150
    for com, outs in (("1L", [".0", ".1", ".2", ".3"]), ("2L", [".4", ".5"])):
        xs = [x + paso * (k + 1) for k in range(len(outs))]
        s.append(ln(x, 230, x, 400) + num(x, 370, com, 20) + ln(x, 230, xs[-1] - 26, 230))
        for xo, o in zip(xs, outs):
            s.append(ln(xo - 26, 230, xo - 26, 250) + ln(xo - 26, 250, xo - 4, 276, SC) + ln(xo, 268, xo, 400) + ln(xo - 8, 268, xo, 268) + num(xo, 370, o, 20))
        x = xs[-1] + paso + 10
    s.append(T(150 + paso * 2.5, 300, "DQ a (relé)", 18, 700))
    s.append(etiqueta(105, 215, ref))
    return envolver(W, H, "".join(s))


SIMBOLOS = {
    "01": lambda: disyuntor(1, "F1"), "02": lambda: disyuntor(2, "F1"), "03": lambda: disyuntor(3, "Q1"),
    "04": guardamotor, "05": contactor, "06": termico, "07": lambda: rele8("KA1"), "08": lambda: rele8("KT1", True),
    "09": lambda: mando(True, "giro", "13", "14", "S2"), "10": lambda: mando(True, "pulsador", "13", "14", "S1", "I"),
    "11": lambda: mando(False, "pulsador", "11", "12", "S0", "O"), "12": lambda: mando(False, "emergencia", "11", "12", "S3"),
    "13": piloto, "14": lambda: sensor("inductivo", "B1"), "15": lambda: sensor("capacitivo", "B2"), "16": lambda: sensor("optico", "B3"),
    "17": flotador, "18": motor, "19": conexiones, "20": borneras, "21": logo_y_fuente, "22": s7_1200,
}

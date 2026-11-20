"""Piezas v2 para videos de AUTOMATIZACIÓN (correcciones del usuario, 9-nov-2026).
- Contactor frontal con volumen (caras superior y lateral), bloque de potencia elevado y bloque AUXILIAR separado.
- Tornillos en la orientación correcta: de frente (cabeza Phillips) o de perfil (cabeza + vástago roscado).
- Interruptor de cuchilla real (bisagra, cuchilla, mordaza, mango aislante) abierto/cerrado.
- Símbolos IEC 60617 según el Telesquemario: pulsador con mando de EMPUJE ("E"), relé térmico, motor con bornes,
  referencias de bornes escritas en vertical (se leen de abajo hacia arriba), trazos de potencia más gruesos.
- Interfaz didáctica: portadilla de sección con tecleo + sonido de teclado, cinta de sección fija, insignia PASO n/7,
  tarjetas de alto contraste con texto centrado.
"""
import wave
from piezas_auto import *
from piezas_auto import _t
from comun_e import _osc, _cla

AZUL_CARTA = "#203A7A"     # relleno de tarjetas (más claro que el fondo #0B1C3D)
AZUL_BORDE = "#6F86D6"
TXT = "#FFFFFF"
TXT2 = "#D5DDF5"
ROJO_P = "#E5484D"         # pulsador de paro (rojo, permitido por IEC 60204-1)
VERDE_P = "#12B76A"        # pulsador de marcha (verde, permitido por IEC 60204-1)
SW_POT = 5.0               # trazo de potencia (más grueso)
SW_MAN = 3.0               # trazo de mando


# ===================================================================== interfaz
def _texto_sobre(color):
    """Texto oscuro sobre colores claros, blanco sobre oscuros (por luminancia)."""
    c = ManimColor(color).to_rgb()
    lum = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return "#0B1C3D" if lum > 0.45 else "#FFFFFF"


def carta(titulo, lineas=(), color=MARCA, w=None, size=26, centrado=False, icono=None, oscura=False):
    """Tarjeta cuadrada, alineada a la izquierda, sin líneas internas: bloque de color a la izquierda.
    Clara (por defecto): fondo blanco, título del color de trabajo, texto azul oscuro. Oscura: fondo del color, texto blanco."""
    col_t = _osc(color, 0.28) if not oscura else _texto_sobre(color)
    col_l = "#1D2939" if not oscura else _texto_sobre(color)
    cab = T(titulo, size + 4, col_t, "HEAVY")
    cu = VGroup(*[T(l, size, col_l, "BOLD") for l in lineas])
    if len(cu):
        cu.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    cuerpo = VGroup(cab, cu).arrange(DOWN, buff=0.16, aligned_edge=LEFT) if len(cu) else VGroup(cab)
    if icono is not None:
        cuerpo = VGroup(icono, cuerpo).arrange(RIGHT, buff=0.35)
    W = max(w or 0, cuerpo.width + 0.85)
    H = cuerpo.height + 0.5
    caja = RoundedRectangle(width=W, height=H, corner_radius=0.07, stroke_width=0).set_fill("#FFFFFF" if not oscura else color, 1)
    tab = Rectangle(width=0.16, height=H, stroke_width=0).set_fill(color if not oscura else _osc(color, 0.3), 1).align_to(caja, LEFT)
    sombra_ = caja.copy().set_fill(BLACK, 0.4).set_stroke(width=0).shift(RIGHT * 0.08 + DOWN * 0.08)
    cuerpo.move_to(caja).align_to(caja.get_left() + RIGHT * 0.42, LEFT)
    return VGroup(sombra_, caja, tab, cuerpo)


def etiqueta(texto, color=MARCA, size=26):
    """Rótulo rectangular sólido (esquinas casi rectas)."""
    t = T(texto, size, _texto_sobre(color), "HEAVY")
    caja = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.26, corner_radius=0.05, stroke_width=0).set_fill(color, 1)
    t.move_to(caja)
    return VGroup(caja, t)


def flecha_a(desde, hasta, color=AMBAR, w=4, curva=0.0):
    if abs(curva) > 1e-3:
        return CurvedArrow(desde, hasta, angle=curva, color=color, stroke_width=w, tip_length=0.2)
    return Arrow(desde, hasta, buff=0.05, color=color, stroke_width=w, max_tip_length_to_length_ratio=0.12, tip_length=0.2)


def llamada(texto, punto, pos_texto, color=AMBAR, size=24, curva=-0.5):
    """Rótulo con flecha curva discontinua que señala una pieza (estilo del ejemplo del usuario)."""
    et = etiqueta(texto, color, size).move_to(pos_texto)
    lado = et.get_left() if punto[0] < et.get_center()[0] else et.get_right()
    if abs(punto[1] - et.get_center()[1]) > et.height:
        lado = et.get_bottom() if punto[1] < et.get_center()[1] else et.get_top()
    fl = CurvedArrow(lado, np.array(punto), angle=curva, color=color, stroke_width=3.5, tip_length=0.18)
    fl_d = DashedVMobject(fl[0] if len(fl) > 1 else fl, num_dashes=14).set_stroke(color, 3.5) if False else fl
    return VGroup(fl_d, et)


def cinta(num, titulo, color=MARCA):
    """Cinta de sección (siempre arriba a la izquierda, mismo estilo en todo el video)."""
    t = T(titulo, 26, TXT, "HEAVY")
    n = T(num, 26, "#08142E", "HEAVY")
    caja_n = RoundedRectangle(width=0.62, height=0.56, corner_radius=0.12, stroke_width=0).set_fill(color, 1)
    caja_t = RoundedRectangle(width=t.width + 0.6, height=0.56, corner_radius=0.12, stroke_width=0).set_fill("#13265A", 0.96)
    borde = RoundedRectangle(width=t.width + 0.6, height=0.56, corner_radius=0.12, stroke_color=color, stroke_width=2.4)
    VGroup(caja_n, caja_t).arrange(RIGHT, buff=0.08)
    borde.move_to(caja_t)
    n.move_to(caja_n)
    t.move_to(caja_t)
    g = VGroup(caja_n, caja_t, borde, n, t)
    return g.move_to([-7.75 + g.width / 2, 4.08, 0])


def insignia_paso(n, total=7, color=AMBAR, palabra="CRITERIO"):
    """Insignia fija arriba a la derecha: CRITERIO n de 7 (cuadrada, sin líneas internas)."""
    cuad = RoundedRectangle(width=0.86, height=0.86, corner_radius=0.06, stroke_width=0).set_fill(color, 1)
    num = T(str(n), 46, "#0B1C3D", "HEAVY").move_to(cuad)
    lab = VGroup(T(palabra, 22, TXT, "HEAVY"), T(f"{n} de {total}", 20, color, "BOLD")).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    lab.next_to(cuad, RIGHT, buff=0.18)
    fondo = RoundedRectangle(width=VGroup(cuad, lab).width + 0.32, height=1.02, corner_radius=0.07, stroke_width=0).set_fill("#13265A", 1)
    fondo.move_to(VGroup(cuad, lab))
    gg = VGroup(fondo, cuad, num, lab)
    puntos = VGroup(*[Rectangle(width=0.22, height=0.08, stroke_width=0).set_fill(color if k < n else "#3A4C86", 1) for k in range(total)]).arrange(RIGHT, buff=0.06)
    puntos.next_to(fondo, DOWN, buff=0.1).align_to(fondo, LEFT)
    g = VGroup(gg, puntos)
    return g.move_to([7.75 - g.width / 2, 3.6, 0])


def sonido_tecleo(destino, n_letras, dt, semilla=0, sr=48000):
    """Sintetiza tecleo de teclado mecánico: un clic por letra (ruido filtrado con caída rápida + golpe grave)."""
    rng = np.random.default_rng(semilla)
    total = int(sr * (n_letras * dt + 0.4))
    y = np.zeros(total)
    for k in range(n_letras):
        t0 = int(sr * (k * dt + rng.uniform(-0.008, 0.008)))
        if t0 < 0:
            t0 = 0
        L = int(sr * 0.035)
        t = np.arange(L) / sr
        ruido = rng.normal(0, 1, L)
        ruido = np.diff(np.concatenate([[0], ruido]))            # paso alto: clic brillante
        clic = ruido * np.exp(-t / 0.0022) * rng.uniform(0.6, 1.0)
        golpe = np.sin(2 * np.pi * rng.uniform(140, 190) * t) * np.exp(-t / 0.009) * 0.5
        seg = clic + golpe
        y[t0:t0 + L] += seg[:max(0, min(L, total - t0))]
    y = y / (np.abs(y).max() + 1e-9) * 0.5
    data = (y * 32767).astype(np.int16)
    with wave.open(str(destino), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())
    return destino


# ===================================================================== tornillos
def tornillo_perfil(alto=0.42, ancho=0.26, color="#D5D9DE"):
    """Tornillo visto de PERFIL (eje vertical): cabeza abombada con ranura, arandela y vástago roscado hacia abajo."""
    cab = VMobject()
    cab.set_points_as_corners([P(-ancho / 2, 0), P(-ancho / 2, ancho * 0.28), P(ancho / 2, ancho * 0.28), P(ancho / 2, 0), P(-ancho / 2, 0)])
    cab.set_fill(color, 1).set_stroke("#6B7280", 1.2)
    domo = Arc(radius=ancho / 2, start_angle=0, angle=PI, arc_center=P(0, ancho * 0.28)).stretch(0.45, 1).set_fill(color, 1).set_stroke("#6B7280", 1.2)
    domo.move_to(P(0, ancho * 0.28 + domo.height / 2 - 0.004))
    ranura = Line(P(0, ancho * 0.12), P(0, ancho * 0.28 + domo.height * 0.95)).set_stroke("#4B5563", 2)
    aran = Rectangle(width=ancho * 1.25, height=0.035, stroke_width=0.8, stroke_color="#6B7280").set_fill("#B8BEC8", 1).move_to(P(0, -0.018))
    vas = Rectangle(width=ancho * 0.42, height=alto, stroke_color="#6B7280", stroke_width=1).set_fill("#AEB4BF", 1).move_to(P(0, -0.035 - alto / 2))
    rosca = VGroup(*[Line(P(-ancho * 0.21, y), P(ancho * 0.21, y - 0.03)).set_stroke("#6B7280", 1) for y in np.arange(-0.07, -0.035 - alto + 0.03, -0.055)])
    g = VGroup(vas, rosca, aran, cab, domo, ranura)
    g.cabeza = VGroup(cab, domo, ranura)
    return g


# ===================================================================== contactor con volumen
def _caja3d(w, h, d, frente, arriba=None, lado=None, borde="#5B6573", r=0.08):
    """Caja con perspectiva caballera: frente + cara superior + cara derecha."""
    arriba = arriba or _cla(frente, 0.25)
    lado = lado or _osc(frente, 0.25)
    f = RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=borde, stroke_width=1.4).set_fill(frente, 1)
    dx, dy = d * 0.7, d * 0.45
    tl, tr, br = f.get_corner(UL), f.get_corner(UR), f.get_corner(DR)
    sup = Polygon(tl + RIGHT * r, tr + LEFT * r * 0.3, tr + LEFT * r * 0.3 + RIGHT * dx + UP * dy, tl + RIGHT * r + RIGHT * dx + UP * dy,
                  stroke_color=borde, stroke_width=1.2).set_fill(arriba, 1)
    der = Polygon(tr + DOWN * r * 0.3, br + UP * r, br + UP * r + RIGHT * dx + UP * dy, tr + DOWN * r * 0.3 + RIGHT * dx + UP * dy,
                  stroke_color=borde, stroke_width=1.2).set_fill(lado, 1)
    g = VGroup(der, sup, f)
    g.frente, g.sup, g.der = f, sup, der
    return g


def contactor_3d(s=1.0, ie="18", ref="KM1", aux=True):
    """Contactor tripolar con volumen. Bloques: potencia arriba (1/L1 3/L2 5/L3, elevado), frente central con bobina A1/A2
    e indicador, BLOQUE AUXILIAR separado (13-14 NA, 21-22 NC) y potencia abajo (2/T1 4/T2 6/T3).
    Atributos: .b (bornes), .ind, .ventana, .aux_blq, .pot_sup, .pot_inf, .s"""
    W, H, D = 2.7 * s, 3.9 * s, 0.55 * s
    sombra_ = RoundedRectangle(width=W + 0.3 * s, height=H, corner_radius=0.14 * s, stroke_width=0).set_fill(BLACK, 0.4).shift(RIGHT * 0.25 * s + DOWN * 0.12 * s)
    cuerpo = _caja3d(W, H, D, "#DADFE6", "#EEF1F5", "#AEB5C0", r=0.12 * s)
    g = VGroup(sombra_, cuerpo)
    b = {}
    # bloques de potencia (elevados)
    pot = []
    for y, nombres, arriba in ((H / 2 - 0.62 * s, ("1/L1", "3/L2", "5/L3"), True), (-H / 2 + 0.62 * s, ("2/T1", "4/T2", "6/T3"), False)):
        blq = _caja3d(W * 0.9, 1.0 * s, 0.22 * s, "#C9CFD8", "#E2E6EC", "#9EA6B2", r=0.06 * s).move_to([0, y, 0])
        g.add(blq)
        pot.append(blq)
        for x, n in zip((-0.82 * s, 0, 0.82 * s), nombres):
            c = blq.frente.get_center() + RIGHT * x + (UP * 0.12 * s if arriba else DOWN * 0.12 * s)
            hueco = RoundedRectangle(width=0.52 * s, height=0.52 * s, corner_radius=0.07 * s, stroke_color="#2F3846", stroke_width=1.2).set_fill("#4B5563", 1).move_to(c)
            tor = tornillo_ph(0.19 * s).move_to(c)
            entrada = RoundedRectangle(width=0.4 * s, height=0.13 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#0F1420", 1)
            entrada.move_to(blq.sup.get_center() + RIGHT * x) if arriba else entrada.next_to(hueco, DOWN, buff=0.05 * s)
            if arriba:
                entrada.move_to([c[0] + 0.07 * s, blq.sup.get_center()[1], 0])
            e = tx(n, 0.14 * s, "#1D2939").next_to(hueco, DOWN if arriba else UP, buff=0.05 * s)
            bb = VGroup(hueco, entrada, tor, e)
            bb.tor, bb.entrada, bb.et, bb.hueco = tor, entrada, e, hueco
            b[n] = bb
            g.add(bb)
    # banda de identificación
    banda = Rectangle(width=W * 0.9, height=0.3 * s, stroke_width=0).set_fill("#1F2430", 1).move_to([0, pot[0].frente.get_bottom()[1] - 0.24 * s, 0])
    g.add(banda, tx(ref, 0.15 * s, "#F2F4F7").move_to(banda).shift(LEFT * 0.8 * s), tx(f"{ie} A · AC-3", 0.13 * s, "#F2F4F7").move_to(banda).shift(RIGHT * 0.55 * s))
    # bobina A1 (arriba derecha) y A2 (abajo derecha)
    xa = 1.0 * s
    for n, y in (("A1", banda.get_bottom()[1] - 0.36 * s), ("A2", pot[1].frente.get_top()[1] + 0.34 * s)):
        marco = RoundedRectangle(width=0.32 * s, height=0.32 * s, corner_radius=0.05 * s, stroke_width=0).set_fill("#4B5563", 1).move_to([xa, y, 0])
        tor = tornillo_ph(0.11 * s).move_to(marco)
        e = tx(n, 0.11 * s, "#B42318").next_to(marco, LEFT, buff=0.05 * s)
        bb = VGroup(marco, tor, e)
        bb.tor, bb.et = tor, e
        b[n] = bb
        g.add(bb)
    # indicador mecánico
    ventana = RoundedRectangle(width=0.36 * s, height=0.44 * s, corner_radius=0.05 * s, stroke_color="#8B93A0", stroke_width=1).set_fill("#F8FAFC", 1)
    ventana.move_to([0.62 * s, (b["A1"].get_center()[1] + b["A2"].get_center()[1]) / 2, 0])
    ind = RoundedRectangle(width=0.26 * s, height=0.14 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#9CA3AF", 1).move_to(ventana.get_center() + UP * 0.1 * s)
    g.add(ventana, ind)
    # bloque auxiliar separado (frontal, con su propia carcasa y sombra)
    aux_blq = VGroup()
    if aux:
        ax_c = [-0.5 * s, (b["A1"].get_center()[1] + b["A2"].get_center()[1]) / 2, 0]
        caja = _caja3d(1.45 * s, 1.18 * s, 0.18 * s, "#EEF1F5", "#FFFFFF", "#C2C8D1", r=0.06 * s).move_to(ax_c)
        som = RoundedRectangle(width=1.45 * s, height=1.18 * s, corner_radius=0.06 * s, stroke_width=0).set_fill(BLACK, 0.3).move_to(caja.frente).shift(RIGHT * 0.08 * s + DOWN * 0.08 * s)
        aux_blq.add(som, caja)
        tit = tx("AUX", 0.09 * s, "#667085").move_to(caja.frente.get_top() + DOWN * 0.1 * s)
        aux_blq.add(tit)
        for (n, col), dx in zip((("13", "NO"), ("21", "NC")), (-0.36 * s, 0.36 * s)):
            for fila, num in ((0.16 * s, n), (-0.3 * s, str(int(n) + 1))):
                c = caja.frente.get_center() + RIGHT * dx + UP * fila
                marco = RoundedRectangle(width=0.3 * s, height=0.3 * s, corner_radius=0.04 * s, stroke_width=0).set_fill("#4B5563", 1).move_to(c)
                tor = tornillo_ph(0.1 * s).move_to(c)
                e = tx(num, 0.085 * s, "#1D2939").next_to(marco, RIGHT, buff=0.03 * s)
                bb = VGroup(marco, tor, e)
                bb.tor, bb.et = tor, e
                b[num] = bb
                aux_blq.add(bb)
            aux_blq.add(tx(col, 0.075 * s, "#0E7490").move_to(caja.frente.get_center() + RIGHT * dx + DOWN * 0.07 * s))
        g.add(aux_blq)
    g.b, g.ind, g.ventana, g.aux_blq, g.pot_sup, g.pot_inf, g.s, g.cuerpo = b, ind, ventana, aux_blq, pot[0], pot[1], s, cuerpo
    return g


def indicador(ct, cerrar=True):
    d = (-0.13 if cerrar else 0.13) * ct.s
    return ct.ind.animate.shift(UP * d).set_fill("#12B76A" if cerrar else "#9CA3AF", 1)


# ===================================================================== interruptor de cuchilla (vista lateral)
def interruptor_cuchilla(s=1.0):
    """Base aislante, poste-bisagra a la izquierda, mordaza doble a la derecha, cuchilla de cobre con mango aislante.
    .cuchilla gira alrededor de .piv. Cerrado = horizontal dentro de la mordaza."""
    base = RoundedRectangle(width=3.4 * s, height=0.32 * s, corner_radius=0.06 * s, stroke_color="#4B3B2A", stroke_width=1.4).set_fill("#7A5A3A", 1)
    poste = Rectangle(width=0.3 * s, height=0.55 * s, stroke_color="#7A3B12", stroke_width=1.2).set_fill(CU, 1).move_to(base.get_top() + UP * 0.275 * s + LEFT * 1.25 * s)
    piv = poste.get_top() + DOWN * 0.12 * s
    pin = Circle(radius=0.07 * s, stroke_color="#4B5563", stroke_width=1.2).set_fill("#D5D9DE", 1).move_to(piv)
    mord_x = 1.15 * s
    mordaza = VGroup(Rectangle(width=0.08 * s, height=0.55 * s, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to(base.get_top() + UP * 0.275 * s + RIGHT * (mord_x - 0.09 * s)),
                     Rectangle(width=0.08 * s, height=0.55 * s, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to(base.get_top() + UP * 0.275 * s + RIGHT * (mord_x + 0.09 * s)))
    largo = (base.get_center()[0] + mord_x + 0.22 * s) - piv[0]
    hoja = Rectangle(width=largo, height=0.1 * s, stroke_color="#7A3B12", stroke_width=1).set_fill("#D9894D", 1)
    hoja.move_to(piv + RIGHT * largo / 2)
    mango = RoundedRectangle(width=0.55 * s, height=0.22 * s, corner_radius=0.08 * s, stroke_width=0).set_fill("#B42318", 1).move_to(hoja.get_right() + RIGHT * 0.24 * s)
    cuch = VGroup(hoja, mango)
    tor = VGroup(tornillo_perfil(0.22 * s, 0.2 * s).move_to(poste.get_left() + LEFT * 0.16 * s + DOWN * 0.05 * s),
                 tornillo_perfil(0.22 * s, 0.2 * s).move_to(mordaza.get_right() + RIGHT * 0.16 * s + DOWN * 0.05 * s))
    g = VGroup(base, poste, mordaza, cuch, pin, tor)
    g.cuchilla, g.pin, g.mordaza, g.base, g.poste = cuch, pin, mordaza, base, poste
    return g


# ===================================================================== corte del contactor (vista lateral, esquemática)
def corte_contactor(c=ORIGIN, k=1.0):
    """Corte esquemático: base, núcleo E, bobina, resortes, armadura, portacontactos, puente con pastillas, contactos fijos
    con tornillos DE PERFIL y cámara apagachispas. Devuelve grupo con .movil, .resortes, .gap, .fijos, .pu, .bob, .arm."""
    c = np.array(c, float)
    base = base_contactor(4.6, 0.6).move_to(c + P(0, -3.25))
    nuc = nucleo_E(3.6, 1.6).move_to(c + P(0, -2.15))
    bob = bobina(2.0, 1.05).move_to(c + P(0, -1.95))
    top_col = c[1] - 1.35
    gap = 0.4
    arm = armadura_T(3.6, 0.6).move_to(c + P(0, top_col - c[1] + gap + 0.3))
    resortes = VGroup(*[resorte(1.0, 0.36, 6, "#C7CCD6", 2.6) for _ in range(2)])
    for r_, x in zip(resortes, (-1.25, 1.25)):
        r_.stretch_to_fit_height(arm.get_bottom()[1] - top_col).move_to([c[0] + x, (arm.get_bottom()[1] + top_col) / 2, 0])
    rod = Rectangle(width=0.4, height=1.5, stroke_color="#4D7C0F", stroke_width=1.2).set_fill("#A3D977", 1).move_to([c[0], arm.get_top()[1] + 0.75, 0])
    pu = puente_movil(2.8).move_to([c[0], rod.get_top()[1] + 0.08, 0])
    y_pad = pu[1][0].get_bottom()[1] - gap - 0.04
    fijos = VGroup()
    for lado in (-1, 1):
        tira = Rectangle(width=1.9, height=0.16, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to([c[0] + lado * 2.05, y_pad - 0.12, 0])
        pad = RoundedRectangle(width=0.3, height=0.08, corner_radius=0.02, stroke_width=0.6, stroke_color="#98A2B3").set_fill(AG, 1).move_to([c[0] + lado * 1.2, y_pad, 0])
        tor = tornillo_perfil(0.32, 0.26).move_to([c[0] + lado * 2.7, 0, 0])
        tor.shift(UP * (tira.get_top()[1] - tor[2].get_bottom()[1]))          # la arandela apoya sobre la tira
        fijos.add(VGroup(tira, pad, tor))
    cam = RoundedRectangle(width=4.2, height=1.5, corner_radius=0.1, stroke_color="#8B93A0", stroke_width=1.6).set_fill("#2A2F3A", 0.55).move_to([c[0], pu.get_center()[1] - 0.1, 0])
    placas = VGroup(*[VGroup(*[Rectangle(width=0.05, height=0.7, stroke_width=0).set_fill("#A7AFBA", 0.9).move_to([c[0] + lado * (1.2 + (j - 2) * 0.11), cam.get_center()[1] + 0.25, 0])
                               for j in range(5)]) for lado in (-1, 1)])
    movil = VGroup(arm, rod, pu)
    g = VGroup(base, nuc, bob, resortes, VGroup(cam, placas), fijos, movil)
    g.base, g.nuc, g.bob, g.resortes, g.cam, g.fijos, g.movil, g.pu, g.arm, g.gap = base, nuc, bob, resortes, VGroup(cam, placas), fijos, movil, pu, arm, gap
    g.scale(k, about_point=c)
    g.gap = gap * k
    return g


# ===================================================================== símbolos IEC (Telesquemario)
def bornes_v(sim, n1=None, n2=None, color=SIM, h=0.17, lado=RIGHT):
    """Referencias de bornes escritas en vertical (se leen de abajo hacia arriba), al lado del símbolo."""
    g = VGroup()
    if n1:
        t1 = _t(n1, h, color).rotate(PI / 2).next_to(sim[0], lado, buff=0.07)
        g.add(t1)
    if n2:
        t2 = _t(n2, h, color).rotate(PI / 2).next_to(sim[1], lado, buff=0.07)
        g.add(t2)
    return g


def contacto(no=True, contactor=False, interruptor=False, largo=1.0, color=SIM, n1=None, n2=None, sw=SW_MAN):
    """Contacto vertical IEC con referencias verticales. NA: cuchilla a la izquierda; NC: con tope a la derecha."""
    a, b = P(0, largo / 2), P(0, -largo / 2)
    sup = Line(a, P(0, largo * 0.18)).set_stroke(color, sw)
    inf = Line(P(0, -largo * 0.18), b).set_stroke(color, sw)
    piv = P(0, -largo * 0.18)
    if no:
        cuch = Line(piv, piv + rotate_vector(UP * largo * 0.42, 0.45)).set_stroke(color, sw)
        tope = VGroup()
    else:
        cuch = Line(piv, piv + rotate_vector(UP * largo * 0.42, -0.32)).set_stroke(color, sw)
        tope = Line(P(0, largo * 0.18), P(largo * 0.17, largo * 0.18)).set_stroke(color, sw)
    g = VGroup(sup, inf, cuch, tope)
    if contactor:
        rr = largo * 0.075
        g.add(Arc(radius=rr, start_angle=-PI / 2, angle=PI, arc_center=P(0, largo * 0.18 + rr)).set_stroke(color, sw * 0.85))
    if interruptor:
        cc = P(0, largo * 0.18)
        d = 0.07 * largo / 0.9
        g.add(Line(cc + P(-d, -d), cc + P(d, d)).set_stroke(color, sw * 0.85), Line(cc + P(-d, d), cc + P(d, -d)).set_stroke(color, sw * 0.85))
    bv = bornes_v(g, n1, n2, color)
    if n1 and (contactor or interruptor or not no):
        bv[0].shift(RIGHT * 0.16 + UP * 0.04 * largo)
    g.add(bv)
    g.cuchilla, g.no, g.largo = cuch, no, largo
    return g


def mover(simb, cerrar=True):
    ang = -0.45 if simb.no else 0.77
    if not cerrar:
        ang = -ang
    return Rotate(simb.cuchilla, ang, about_point=simb.cuchilla.get_start())


def mando_empuje(punto, color=SIM, largo=0.5):
    """Mando manual de pulsador (retorno automático) IEC 60617: 'E' de empuje + enlace discontinuo hacia el contacto."""
    p = np.array(punto)
    x0 = p[0] - largo
    dl = DashedLine(p, [x0, p[1], 0], dash_length=0.05).set_stroke(color, 2.2)
    e = VMobject().set_points_as_corners([[x0 + 0.1, p[1] + 0.13, 0], [x0, p[1] + 0.13, 0], [x0, p[1] - 0.13, 0], [x0 + 0.1, p[1] - 0.13, 0]]).set_stroke(color, 2.6)
    return VGroup(dl, e)


def pulsador(no=True, ref="S1", n1=None, n2=None, color=SIM, largo=1.0):
    c = contacto(no, largo=largo, color=color, n1=n1, n2=n2)
    act = mando_empuje(c.cuchilla.get_center(), color)
    r = _t(ref, 0.22, color).next_to(act, LEFT, buff=0.08)
    c.add(act, r)
    c.act, c.ref = act, r
    return c


def termico_aux(ref="F2", color=SIM, largo=1.0):
    """Contacto 95-96 (NC) del relé térmico con su mando térmico (escalón) y enlace."""
    c = contacto(False, largo=largo, color=color, n1="95", n2="96")
    p = c.cuchilla.get_center()
    dl = DashedLine(p, p + LEFT * 0.36, dash_length=0.05).set_stroke(color, 2.2)
    esc = VMobject().set_points_as_corners([p + LEFT * 0.36 + UP * 0.1, p + LEFT * 0.48 + UP * 0.1, p + LEFT * 0.48 + DOWN * 0.1, p + LEFT * 0.6 + DOWN * 0.1]).set_stroke(color, 2.6)
    r = _t(ref, 0.22, color).next_to(esc, LEFT, buff=0.08)
    c.add(dl, esc, r)
    return c


def bobina_sim(ref="KM1", color=SIM, sw=SW_MAN):
    r = Rectangle(width=0.62, height=0.36, stroke_color=color, stroke_width=sw)
    a = Line(P(0, 0.18), P(0, 0.55)).set_stroke(color, sw)
    b = Line(P(0, -0.18), P(0, -0.55)).set_stroke(color, sw)
    t1 = _t("A1", 0.16, color).rotate(PI / 2).next_to(a, RIGHT, buff=0.07)
    t2 = _t("A2", 0.16, color).rotate(PI / 2).next_to(b, RIGHT, buff=0.07)
    g = VGroup(a, r, b, t1, t2, _t(ref, 0.22, color).next_to(r, LEFT, buff=0.12))
    g.rect = r
    return g


def termico_pot(color=SIM, sw=SW_POT):
    """Elemento térmico del relé de sobrecarga (Telesquemario p. 165): recuadro con el conductor en escalón."""
    r = Rectangle(width=0.4, height=0.58, stroke_color=color, stroke_width=sw * 0.55)
    z = VMobject().set_points_as_corners([P(0, 0.29), P(0, 0.12), P(-0.11, 0.12), P(-0.11, -0.12), P(0, -0.12), P(0, -0.29)]).set_stroke(color, sw)
    return VGroup(r, z)


def motor_sim(color=SIM, r=0.62, energizado=False):
    """Motor asíncrono trifásico con bornes U1 V1 W1 arriba (Telesquemario p. 164)."""
    c = Circle(radius=r, stroke_color=color, stroke_width=SW_MAN + 0.5)
    t = VGroup(_t("M", 0.34, color), _t("3~", 0.2, color)).arrange(DOWN, buff=0.04).move_to(c)
    bornes = VGroup()
    xs = (-0.38 * r / 0.62, 0, 0.38 * r / 0.62)
    for x, n in zip(xs, ("U1", "V1", "W1")):
        p = c.get_top() + RIGHT * x + DOWN * (r - np.sqrt(max(r ** 2 - x ** 2, 0)))
        bor = Circle(radius=0.06, stroke_color=color, stroke_width=2).set_fill(FONDO, 1).move_to(p + UP * 0.22)
        pata = Line(p, bor.get_bottom()).set_stroke(color, SW_MAN)
        lab = _t(n, 0.15, color).rotate(PI / 2).next_to(bor, RIGHT, buff=0.04).shift(UP * 0.12)
        bornes.add(VGroup(pata, bor, lab))
    g = VGroup(c, t, bornes)
    g.bornes, g.circ = bornes, c
    return g


# ===================================================================== v3 (correcciones 9-nov tarde): contactor 2D frontal realista
GRIS_CUERPO = "#E4E7EB"
GRIS_SOMBRA = "#B9BFC8"
AZUL_PIEZA = "#2F6FD0"


def tornillo_frente(r=0.16):
    """Tornillo combinado (Phillips/plano) visto de frente, dentro de su alojamiento redondo."""
    aloj = Circle(radius=r * 1.32, stroke_color="#8A929E", stroke_width=1.2).set_fill("#2B2F36", 1)
    cab = Circle(radius=r, stroke_color="#6B7280", stroke_width=1).set_fill("#D9DDE3", 1)
    brillo = Arc(radius=r * 0.78, start_angle=PI * 0.55, angle=PI * 0.5).set_stroke(WHITE, 1.6, 0.7)
    cruz = VGroup(Line(LEFT * r * 0.62, RIGHT * r * 0.62), Line(UP * r * 0.62, DOWN * r * 0.62)).set_stroke("#3A3F47", max(1.5, r * 14))
    cruz.rotate(0.35)
    g = VGroup(aloj, cab, brillo, cruz)
    g.cabeza = cab
    return g


def contactor_2d(s=1.0, ie="18", ref="KM1", aux_integrado=True):
    """Contactor tripolar visto de FRENTE (2D), basado en un contactor real de 9–32 A sin marca:
    - arriba: bornes de bobina A1 (izq.) y A2 (der.) sobresaliendo, y la caja de la bobina al centro;
    - fila superior: 1/L1 3/L2 5/L3 + 13NO (auxiliar integrado);
    - ventana oscura con el portacontactos azul (se mueve al cerrar) y placa blanca de datos;
    - fila inferior: 2/T1 4/T2 6/T3 + 14NO; abajo, las entradas de cable.
    Todos los tornillos se ven de frente. Atributos: .b, .ind, .ventana, .pot_sup, .pot_inf, .aux_blq, .s"""
    W, H = 3.2 * s, 4.0 * s
    xs = [(-1.2 + 0.8 * k) * s for k in range(4)]
    sombra_ = RoundedRectangle(width=W, height=H, corner_radius=0.12 * s, stroke_width=0).set_fill(BLACK, 0.35).shift(RIGHT * 0.12 * s + DOWN * 0.12 * s)
    # caja de bobina (azul) y bornes A1/A2 arriba
    caja_b = RoundedRectangle(width=1.5 * s, height=0.45 * s, corner_radius=0.06 * s, stroke_color="#1D2939", stroke_width=1.2).set_fill("#1F2430", 1).move_to([0, H / 2 + 0.12 * s, 0])
    franja = Rectangle(width=1.3 * s, height=0.16 * s, stroke_width=0).set_fill(AZUL_PIEZA, 1).move_to(caja_b.get_center() + DOWN * 0.04 * s)
    cuerpo = RoundedRectangle(width=W, height=H, corner_radius=0.12 * s, stroke_color="#9AA3AF", stroke_width=1.6).set_fill(GRIS_CUERPO, 1)
    g = VGroup(sombra_, caja_b, franja)
    b = {}
    for n, x in (("A1", xs[0] + 0.05 * s), ("A2", xs[2] + 0.4 * s)):
        torre = RoundedRectangle(width=0.5 * s, height=0.42 * s, corner_radius=0.05 * s, stroke_color="#9AA3AF", stroke_width=1.2).set_fill("#F2F4F6", 1).move_to([x, H / 2 + 0.1 * s, 0])
        tor = tornillo_frente(0.11 * s).move_to(torre.get_center() + UP * 0.02 * s)
        e = tx(n, 0.13 * s, "#FF8A80").next_to(torre, UP, buff=0.05 * s)
        bb = VGroup(torre, tor)
        bb.tor, bb.et, bb.entrada = tor, e, VMobject().move_to(torre.get_top())
        b[n] = bb
        g.add(bb)
    g.add(cuerpo)
    for n in ("A1", "A2"):
        g.add(b[n].et)
    # filas de bornes
    sup_n = ["1/L1", "3/L2", "5/L3", "13NO"]
    inf_n = ["2/T1", "4/T2", "6/T3", "14NO"]
    pot_sup, pot_inf, aux_blq = VGroup(), VGroup(), VGroup()
    y_sup, y_inf = H / 2 - 0.85 * s, -H / 2 + 0.72 * s
    for fila, nombres, y, arriba in ((pot_sup, sup_n, y_sup, True), (pot_inf, inf_n, y_inf, False)):
        for x, n in zip(xs, nombres):
            if not aux_integrado and n.endswith("NO"):
                continue
            tor = tornillo_frente(0.2 * s).move_to([x, y, 0])
            e = tx(n, 0.13 * s, "#475467").next_to(tor, UP if arriba else DOWN, buff=0.08 * s)
            boca = RoundedRectangle(width=0.5 * s, height=0.16 * s, corner_radius=0.04 * s, stroke_width=0).set_fill("#2B2F36", 1)
            boca.move_to([x, (H / 2 - 0.12 * s) if arriba else (-H / 2 + 0.1 * s), 0])
            bb = VGroup(boca, tor, e)
            bb.tor, bb.et, bb.entrada = tor, e, boca
            clave = n.replace("NO", "") if n.endswith("NO") else n
            b[clave] = bb
            (aux_blq if n.endswith("NO") else fila).add(bb)
            g.add(bb)
    # festón inferior (separadores entre entradas de cable)
    for x in xs[:-1]:
        g.add(RoundedRectangle(width=0.12 * s, height=0.2 * s, corner_radius=0.04 * s, stroke_width=0).set_fill(GRIS_SOMBRA, 1).move_to([x + 0.4 * s, -H / 2 + 0.1 * s, 0]))
    # ventana del portacontactos
    ventana = RoundedRectangle(width=2.3 * s, height=1.05 * s, corner_radius=0.05 * s, stroke_width=0).set_fill("#1F2430", 1).move_to([-0.15 * s, 0.2 * s, 0])
    marco = RoundedRectangle(width=0.62 * s, height=0.3 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#2B2F36", 1).move_to(ventana.get_top() + DOWN * 0.18 * s)
    pieza = VGroup(RoundedRectangle(width=2.1 * s, height=0.42 * s, corner_radius=0.04 * s, stroke_color="#1D4E9E", stroke_width=1).set_fill(AZUL_PIEZA, 1),
                   *[Rectangle(width=0.06 * s, height=0.3 * s, stroke_width=0).set_fill("#1D4E9E", 1).move_to([dx * s, 0, 0]) for dx in (-0.55, 0.1, 0.55)],
                   RoundedRectangle(width=0.36 * s, height=0.34 * s, corner_radius=0.03 * s, stroke_color="#1D4E9E", stroke_width=1).set_fill("#3D80E0", 1))
    pieza.move_to(ventana.get_center() + DOWN * 0.05 * s)
    placa = Rectangle(width=1.5 * s, height=0.42 * s, stroke_color="#C9CED6", stroke_width=1).set_fill("#FFFFFF", 1).move_to([-0.15 * s, ventana.get_bottom()[1] - 0.32 * s, 0])
    t_ref = tx(ref, 0.13 * s, "#1D2939").move_to(placa.get_center() + LEFT * 0.38 * s)
    t_ie = tx(f"{ie} A · AC-3", 0.1 * s, "#475467").move_to(placa.get_center() + RIGHT * 0.3 * s)
    linea = Line([0.85 * s, ventana.get_top()[1] - 0.12 * s, 0], [1.5 * s, ventana.get_top()[1] - 0.12 * s, 0]).set_stroke(AZUL_PIEZA, 2.5)
    g.add(ventana, marco, pieza, placa, t_ref, t_ie, linea)
    g.b, g.ind, g.ventana, g.pot_sup, g.pot_inf, g.aux_blq, g.s, g.cuerpo, g.pieza = b, pieza, ventana, pot_sup, pot_inf, aux_blq, s, cuerpo, pieza
    return g


def indicador2(ct, cerrar=True):
    d = (-0.08 if cerrar else 0.08) * ct.s
    return ct.pieza.animate.shift(UP * d)


def bloque_aux_frontal(s=1.0, contactos=(("53", "NO"), ("61", "NC"), ("71", "NC"), ("83", "NO"))):
    """Bloque de contactos auxiliares frontal (sin marca), visto de frente: fila superior 53NO 61NC 71NC 83NO,
    inferior 54NO 62NC 72NC 84NO; se monta sobre la ventana del contactor."""
    n = len(contactos)
    W, H = (0.72 * n + 0.2) * s, 1.75 * s
    cuerpo = RoundedRectangle(width=W, height=H, corner_radius=0.08 * s, stroke_color="#1D2939", stroke_width=1.4).set_fill("#4A505A", 1)
    sombra_ = cuerpo.copy().set_fill(BLACK, 0.35).set_stroke(width=0).shift(RIGHT * 0.1 * s + DOWN * 0.1 * s)
    franja = Line(cuerpo.get_left() + RIGHT * 0.1 * s, cuerpo.get_right() + LEFT * 0.1 * s).set_stroke(AZUL_PIEZA, 3).shift(UP * 0.12 * s)
    vent = Rectangle(width=0.16 * s, height=0.36 * s, stroke_width=0).set_fill(AZUL_PIEZA, 1).move_to(cuerpo.get_center() + DOWN * 0.18 * s + LEFT * 0.25 * s)
    g = VGroup(sombra_, cuerpo, franja, vent)
    b = {}
    xs = [(-0.72 * (n - 1) / 2 + 0.72 * k) * s for k in range(n)]
    for (num, fun), x in zip(contactos, xs):
        for y, nn, arriba in ((0.52 * s, num, True), (-0.55 * s, str(int(num) + 1), False)):
            tor = tornillo_frente(0.15 * s).move_to([x, y, 0])
            e = tx(f"{nn}{fun}", 0.1 * s, "#F2F4F7").next_to(tor, UP if arriba else DOWN, buff=0.05 * s)
            bb = VGroup(tor, e)
            bb.tor, bb.et = tor, e
            b[nn] = bb
            g.add(bb)
    g.b = b
    return g

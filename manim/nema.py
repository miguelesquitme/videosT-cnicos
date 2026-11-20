"""
Equipo eléctrico residencial con forma real (vista frontal, línea fina):
centro de carga NEMA 1 (load center), breaker de 1 polo, caja octagonal 4", caja rectangular 2x4 (device box),
interruptor sencillo (yugo, palanca, tornillos de latón y verde), portalámparas de porcelana con foco A19,
tuerca para empalme (wire nut), probador de voltaje.
Todas las coordenadas del "mundo" del video 2 se definen aquí para compartir rutas de cables.
"""
from comun_e import *
from comun_e import _osc, _cla

GAL = "#E9ECF1"     # lámina galvanizada
GAL2 = "#F5F6F8"
BARRA = "#C8CED8"   # barra estañada
NEGRO_BK = "#2A2E35"

# ------------------------------------------------------------------ geometría del mundo
PANEL_C = np.array([-5.3, -0.45, 0])
PANEL_W, PANEL_H = 2.8, 3.8
ENTRADA_PANEL = np.array([-4.45, PANEL_C[1] + PANEL_H / 2, 0])   # knockout superior
Y_TECHO = 2.75
OCT_C = np.array([-0.2, Y_TECHO, 0])
OCT_R = 0.62
SW_C = np.array([5.3, -0.1, 0])
SW_W, SW_H = 1.05, 1.6
LAMP_TOP = OCT_C[1] - OCT_R * np.cos(PI / 8)


def P(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ piezas pequeñas
def tornillo_cab(c, r=0.045, color=METAL2, ranura=0.5):
    t = tornillo(r, color, ranura).move_to(c)
    return t


def breaker(etiqueta="15", ancho=0.46, alto=0.26, lado=1, on=True, color=NEGRO_BK):
    """Breaker de 1 polo (enchufable) visto de frente. lado=1: terminal de carga a la derecha.
    Índices: [0] cuerpo, [1] ventana, [2] palanca, [3] etiqueta, [4] lug, [5] nervaduras, [6] tornillo."""
    cuerpo = RoundedRectangle(width=ancho, height=alto, corner_radius=0.035, stroke_color="#0B0D11", stroke_width=1.1)
    cuerpo.set_fill(color, 1)
    ventana = RoundedRectangle(width=ancho * 0.34, height=alto * 0.66, corner_radius=0.02, stroke_color="#0B0D11",
                               stroke_width=0.6).set_fill("#1A1D22", 1)
    ventana.shift(RIGHT * ancho * 0.06 * lado)
    palanca = VGroup(RoundedRectangle(width=ancho * 0.15, height=alto * 0.54, corner_radius=0.015, stroke_width=0.7,
                                      stroke_color="#0B0D11").set_fill("#E7E9ED", 1),
                     *[Line([-ancho * 0.045, alto * k * 0.09, 0], [ancho * 0.045, alto * k * 0.09, 0],
                            stroke_color="#98A2B3", stroke_width=0.5) for k in (-1, 0, 1)])
    palanca.move_to(ventana).shift(RIGHT * ancho * 0.08 * (1 if on else -1) * lado)
    sticker = RoundedRectangle(width=ancho * 0.24, height=alto * 0.56, corner_radius=0.012, stroke_width=0).set_fill("#F2F4F7", 1)
    sticker.move_to(cuerpo).shift(LEFT * ancho * 0.28 * lado)
    txt = T(etiqueta, 8, "#101318", "HEAVY")
    txt.scale_to_fit_width(sticker.width * 0.78).move_to(sticker)
    lug = RoundedRectangle(width=ancho * 0.19, height=alto * 0.72, corner_radius=0.012, stroke_color="#667085",
                           stroke_width=0.7).set_fill("#C9CED6", 1)
    lug.move_to(cuerpo.get_center() + RIGHT * lado * (ancho / 2 - ancho * 0.1))
    ribs = VGroup(*[Line(cuerpo.get_top() + LEFT * ancho * 0.42 + DOWN * 0.016 * (k + 1),
                         cuerpo.get_top() + RIGHT * ancho * 0.42 + DOWN * 0.016 * (k + 1), stroke_color="#4A515C",
                         stroke_width=0.5) for k in range(2)])
    term = tornillo(0.03, "#D9DDE3", 0.3).move_to(lug)
    g = VGroup(cuerpo, ventana, palanca, VGroup(sticker, txt), lug, ribs, term)
    g.terminal, g.palanca, g.lado = term, palanca, lado
    return g


def mover_palanca(b, on):
    v = b[1]
    return b.palanca.animate.move_to(v.get_center() + RIGHT * b[0].width * 0.08 * (1 if on else -1) * b.lado)


def tuerca_empalme(c, color=AMBAR, h=0.16, ang=0):
    """Conector de resorte (wire nut): cuerpo cónico con alas y estrías, punta hacia arriba."""
    osc = _osc(color, 0.35)
    m = VMobject().set_points_smoothly([P(-h * 0.44, -h / 2), P(-h * 0.36, 0), P(-h * 0.22, h * 0.42), P(0, h * 0.52),
                                        P(h * 0.22, h * 0.42), P(h * 0.36, 0), P(h * 0.44, -h / 2), P(-h * 0.44, -h / 2)])
    m.set_fill(color, 1).set_stroke(osc, 1)
    alas = VGroup(*[Polygon(P(s * h * 0.36, -h * 0.05), P(s * h * 0.6, -h * 0.12), P(s * h * 0.42, -h * 0.4),
                            stroke_color=osc, stroke_width=0.8).set_fill(color, 1) for s in (-1, 1)])
    estr = VGroup(*[Line(P(-h * (0.3 - 0.04 * k), -h * 0.3 + h * 0.2 * k), P(h * (0.3 - 0.04 * k), -h * 0.3 + h * 0.2 * k))
                    .set_stroke(osc, 0.7) for k in range(3)])
    brillo = Line(P(-h * 0.2, -h * 0.35), P(-h * 0.1, h * 0.35)).set_stroke(WHITE, 1, 0.6)
    return VGroup(alas, m, estr, brillo).rotate(ang).move_to(c)


def foco(encendido=False, h=0.9):
    """Foco A19 de lado, base arriba: vidrio con brillo, soporte de filamento, rosca E26 con hilos e ínsulo."""
    s = h / 0.9
    vidrio = VMobject().set_points_smoothly([P(-0.12, 0.25), P(-0.3, 0.0), P(-0.33, -0.28), P(-0.18, -0.5),
                                             P(0, -0.55), P(0.18, -0.5), P(0.33, -0.28), P(0.3, 0.0),
                                             P(0.12, 0.25), P(-0.12, 0.25)])
    vidrio.set_fill("#FFF3C4" if encendido else "#F4F6F9", 1).set_stroke(LINEA, 1.1)
    reflejo = Arc(radius=0.22, start_angle=PI * 0.6, angle=PI * 0.45, arc_center=P(0.02, -0.22)).set_stroke(WHITE, 2.2, 0.9)
    soporte = VGroup(Line(P(-0.03, 0.22), P(-0.05, -0.1)), Line(P(0.03, 0.22), P(0.05, -0.1))).set_stroke(METAL_OSC, 0.8)
    filamento = VMobject().set_points_smoothly([P(-0.05, -0.1), P(-0.07, -0.2), P(0, -0.25), P(0.07, -0.2), P(0.05, -0.1)])
    filamento.set_stroke(ENERGIA if encendido else METAL_OSC, 1.4)
    cuello = Polygon(P(-0.12, 0.25), P(0.12, 0.25), P(0.12, 0.29), P(-0.12, 0.29), stroke_width=0).set_fill("#E4E7EC", 1)
    rosca = VGroup(RoundedRectangle(width=0.25, height=0.2, corner_radius=0.02, stroke_color=METAL_OSC, stroke_width=0.9)
                   .set_fill("#D0D5DD", 1).move_to(P(0, 0.38)),
                   *[VMobject().set_points_smoothly([P(-0.125, 0.3 + 0.045 * k), P(0, 0.32 + 0.045 * k), P(0.125, 0.3 + 0.045 * k)])
                     .set_stroke(METAL_OSC, 0.8) for k in range(4)],
                   Polygon(P(-0.07, 0.48), P(0.07, 0.48), P(0.04, 0.52), P(-0.04, 0.52), stroke_width=0).set_fill(NEGRO_BK, 1),
                   Dot(P(0, 0.53), radius=0.022, color=LATON))
    g = VGroup(vidrio, reflejo, soporte, filamento, cuello, rosca).scale(s)
    g.vidrio = vidrio
    return g


def portalampara(c=None):
    """Portalámparas keyless de porcelana bajo la caja: borne plateado (rosca/neutro) a la izquierda,
    borne de latón (centro/retorno) a la derecha, foco colgando."""
    base = VMobject().set_points_smoothly([P(-0.58, 0), P(-0.52, -0.2), P(-0.4, -0.32), P(0, -0.35), P(0.4, -0.32),
                                           P(0.52, -0.2), P(0.58, 0)])
    base.add_line_to(P(-0.58, 0)).set_fill(PORCELANA, 1).set_stroke("#B9B4A6", 1.1)
    canto = Line(P(-0.56, -0.02), P(0.56, -0.02)).set_stroke("#D8D2C2", 1.2)
    ranuras = VGroup(*[RoundedRectangle(width=0.1, height=0.045, corner_radius=0.02, stroke_color="#B9B4A6",
                                        stroke_width=0.7).set_fill("#E9E4D6", 1).move_to(P(s * 0.47, -0.08)) for s in (-1, 1)])
    cuello = RoundedRectangle(width=0.44, height=0.2, corner_radius=0.05, stroke_color="#B9B4A6", stroke_width=1.1)
    cuello.set_fill(PORCELANA, 1).move_to(P(0, -0.43))
    bp = borne(P(-0.27, -0.17), 0.05, "#E4E7EC")
    bl = borne(P(0.27, -0.17), 0.05, LATON)
    f = foco(False, 0.85)
    f.move_to(P(0, -0.5 - f.height / 2 + 0.07))
    g = VGroup(f, cuello, base, canto, ranuras, bp, bl)
    g.plata, g.laton, g.foco = bp.tor, bl.tor, f
    if c is not None:
        g.shift(c)
    return g


def probador():
    cuerpo = RoundedRectangle(width=0.22, height=0.9, corner_radius=0.1, stroke_color=LINEA, stroke_width=1.2)
    cuerpo.set_fill(AMBAR, 1)
    franja = Rectangle(width=0.22, height=0.12, stroke_width=0).set_fill("#101318", 1).move_to(P(0, -0.25))
    punta = Polygon(P(-0.06, -0.45), P(0.06, -0.45), P(0.0, -0.68), stroke_color=LINEA, stroke_width=1).set_fill("#E4E7EC", 1)
    luz = Circle(radius=0.05, stroke_width=0.8, stroke_color=LINEA).set_fill(WHITE, 1).move_to(P(0, 0.3))
    clip = RoundedRectangle(width=0.05, height=0.42, corner_radius=0.02, stroke_width=0).set_fill(NEGRO_BK, 1).move_to(P(0.13, 0.15))
    g = VGroup(cuerpo, punta, luz, clip, franja)
    g.luz = luz
    return g


def knockout(c, r=0.09, color_borde=METAL2, fondo=GAL):
    """Knockout concéntrico (½" y ¾") con su lengüeta."""
    a = Circle(radius=r, stroke_color=color_borde, stroke_width=0.8).set_fill(fondo, 1)
    b = Circle(radius=r * 0.72, stroke_color=color_borde, stroke_width=0.7)
    t = Line(P(r * 0.72, 0), P(r, 0), stroke_color=color_borde, stroke_width=1.6)
    return VGroup(a, b, t).move_to(c)


# ------------------------------------------------------------------ centro de carga
def centro_carga():
    c = PANEL_C
    x0, x1 = c[0] - PANEL_W / 2, c[0] + PANEL_W / 2
    y0, y1 = c[1] - PANEL_H / 2, c[1] + PANEL_H / 2
    gabinete = Rectangle(width=PANEL_W, height=PANEL_H, stroke_color=METAL_OSC, stroke_width=1.6).set_fill(GAL, 1).move_to(c)
    pestaña = Rectangle(width=PANEL_W - 0.16, height=PANEL_H - 0.16, stroke_color=METAL2, stroke_width=0.8).set_fill(GAL2, 1).move_to(c)
    llaves = VGroup(*[VGroup(Circle(radius=0.035, stroke_color=METAL2, stroke_width=0.8).set_fill(WHITE, 1),
                             RoundedRectangle(width=0.03, height=0.07, corner_radius=0.012, stroke_width=0).set_fill(WHITE, 1)
                             .shift(DOWN * 0.04)).move_to(P(x, y)) for x in (x0 + 0.2, x1 - 0.2) for y in (y1 - 0.25, y0 + 0.25)])
    kos = VGroup(*[knockout(P(x, y), r) for x, y, r in [(c[0] - 0.7, y1 - 0.13, 0.09), (c[0] - 0.2, y1 - 0.13, 0.09),
                                                         (c[0] - 0.83, y0 + 0.13, 0.11), (c[0] + 0.25, y0 + 0.13, 0.09)]])
    # chasis aislante con barras y dedos (stabs)
    chasis = RoundedRectangle(width=1.25, height=2.55, corner_radius=0.05, stroke_color="#1D2939", stroke_width=1)
    chasis.set_fill("#3A4250", 1).move_to(P(c[0] - 0.05, c[1] - 0.05))
    canales = VGroup(*[Line(P(c[0] - 0.05 + dx, c[1] + 0.85), P(c[0] - 0.05 + dx, c[1] - 1.2), stroke_color="#2B313B", stroke_width=1)
                       for dx in (-0.45, 0.45)])
    filas = [c[1] + 0.55 - 0.32 * k for k in range(5)]
    buses = VGroup()
    for dx in (-0.12, 0.12):
        bus = Rectangle(width=0.1, height=2.15, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(BARRA, 1)
        bus.move_to(P(c[0] - 0.05 + dx, c[1] - 0.15))
        brillo = Line(bus.get_top() + P(-0.025, -0.02), bus.get_bottom() + P(-0.025, 0.02), stroke_color=WHITE,
                      stroke_width=0.8, stroke_opacity=0.8)
        buses.add(VGroup(bus, brillo))
    stabs = VGroup()
    for k, y in enumerate(filas):
        dx = -0.12 if k % 2 == 0 else 0.12
        for lado in (-1, 1):
            stabs.add(RoundedRectangle(width=0.16, height=0.07, corner_radius=0.01, stroke_color=METAL_OSC, stroke_width=0.6)
                      .set_fill(BARRA, 1).move_to(P(c[0] - 0.05 + dx + lado * 0.1, y)))
    buses.add(stabs)
    principal = VGroup(RoundedRectangle(width=0.8, height=0.44, corner_radius=0.04, stroke_color="#0B0D11",
                                        stroke_width=1.2).set_fill(NEGRO_BK, 1),
                       RoundedRectangle(width=0.34, height=0.26, corner_radius=0.02, stroke_color="#0B0D11", stroke_width=0.6)
                       .set_fill("#1A1D22", 1),
                       RoundedRectangle(width=0.24, height=0.12, corner_radius=0.02, stroke_width=0.8,
                                        stroke_color="#0B0D11").set_fill("#E7E9ED", 1),
                       VGroup(RoundedRectangle(width=0.16, height=0.12, corner_radius=0.01, stroke_width=0).set_fill("#F2F4F7", 1),
                              T("100", 8, "#101318", "HEAVY").scale_to_fit_width(0.12)).shift(LEFT * 0.27),
                       VGroup(*[tornillo(0.035, "#D9DDE3", 0.4).move_to(P(s * 0.3, 0.12)) for s in (-1, 1)]).shift(RIGHT * 0.3 + DOWN * 0.12 + LEFT * 0.3),
                       T("MAIN", 6, "#C9CED6", "BOLD").shift(RIGHT * 0.3 + DOWN * 0.13))
    principal[3][1].move_to(principal[3][0])
    principal[4].move_to(P(0.0, 0.0)).shift(UP * 0.16)
    principal.move_to(P(c[0] - 0.05, c[1] + 1.05))
    principal.palanca = principal[2]
    brks = VGroup()
    nuestro = None
    for k, y in enumerate(filas):
        for lado in (-1, 1):
            if k == 0 and lado == 1:
                b = breaker("15", lado=1)
                nuestro = b
            elif k in (1, 2):
                b = breaker("20", lado=lado, color="#2F343C")
            else:
                b = VGroup(RoundedRectangle(width=0.42, height=0.24, corner_radius=0.02, stroke_color="#7C8594",
                                            stroke_width=0.8).set_fill("#59616E", 1),
                           Line(P(-0.12, 0), P(0.12, 0), stroke_color="#7C8594", stroke_width=0.8))
            b.move_to(P(c[0] - 0.05 + lado * 0.29, y))
            brks.add(b)
    # barra de neutros (aislada) a la derecha
    neu_x = c[0] + 0.98
    bloques = VGroup(*[RoundedRectangle(width=0.22, height=0.2, corner_radius=0.03, stroke_color="#B9A37A", stroke_width=0.8)
                       .set_fill("#EADFC4", 1).move_to(P(neu_x, c[1] + yy)) for yy in (0.87, -0.77)])
    neutro = Rectangle(width=0.13, height=1.72, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(BARRA, 1).move_to(P(neu_x, c[1] + 0.05))
    agujeros = VGroup(*[Circle(radius=0.016, stroke_width=0).set_fill("#667085", 1).move_to(P(neu_x - 0.045, c[1] + 0.75 - 0.18 * k))
                        for k in range(9)])
    tn = VGroup(*[tornillo(0.03, "#E4E7EC", 0.0, cruz=False).move_to(P(neu_x + 0.02, c[1] + 0.75 - 0.18 * k)) for k in range(9)])
    letra_n = T("N", 9, "#475467", "HEAVY").move_to(P(neu_x, c[1] - 0.77))
    # barra de tierra (unida al gabinete) abajo
    tierra_b = Rectangle(width=1.3, height=0.13, stroke_color="#7A4A22", stroke_width=0.8).set_fill("#D29A66", 1)
    tierra_b.move_to(P(c[0] - 0.05, y0 + 0.42))
    fij = VGroup(*[tornillo(0.028, METAL, 0.8).move_to(P(c[0] - 0.05 + s * 0.6, y0 + 0.42)) for s in (-1, 1)])
    tt = VGroup(*[tornillo(0.03, TIERRA, 0.0, cruz=False).move_to(P(c[0] - 0.47 + 0.14 * k, y0 + 0.42)) for k in range(7)])
    puente = VGroup(Line(P(neu_x, c[1] - 0.82), P(neu_x, y0 + 0.42)).set_stroke("#0B7A33", 5),
                    Line(P(neu_x, c[1] - 0.82), P(neu_x, y0 + 0.42)).set_stroke(TIERRA, 3.5),
                    Line(P(neu_x, y0 + 0.42), P(c[0] + 0.6, y0 + 0.42)).set_stroke(TIERRA, 3.5),
                    tornillo(0.045, TIERRA, 0.2).move_to(P(neu_x, y0 + 0.42)))
    # acometida (entra por abajo)
    # fases: suben por el costado izquierdo, POR ENCIMA (visibles) y entran desde arriba a los terminales del principal
    lug_n = principal[4][0].get_center()
    lug_r = principal[4][1].get_center()
    acom = VGroup(
        cable(P(c[0] - 0.78, y0 - 0.9), P(c[0] - 0.78, c[1] + 1.36),
              P(c[0] - 0.7, c[1] + 1.44), P(lug_n[0] - 0.08, c[1] + 1.44), P(lug_n[0], c[1] + 1.36), lug_n, color=FASE, w=4),
        cable(P(c[0] - 0.88, y0 - 0.9), P(c[0] - 0.88, c[1] + 1.46),
              P(c[0] - 0.8, c[1] + 1.54), P(lug_r[0] - 0.08, c[1] + 1.54), P(lug_r[0], c[1] + 1.46), lug_r, color=RETORNO, w=4),
        cable(P(c[0] + 0.7, y0 - 0.9), P(c[0] + 0.7, y0 + 0.25), P(neu_x, c[1] - 0.82), color=NEUTRO, w=4),
    )
    g = VGroup(gabinete, pestaña, kos, VGroup(), chasis, buses, principal, brks, bloques, neutro, tn, tierra_b, tt, puente,
               llaves, canales, agujeros, letra_n, fij, acom)
    g.nuestro, g.principal, g.buses, g.neutro, g.tn, g.tierra_b, g.tt, g.puente = \
        nuestro, principal, buses, VGroup(bloques, neutro, agujeros, tn), tn, tierra_b, tt, puente
    g.acom = acom
    return g


def varilla_tierra():
    x = PANEL_C[0] - 0.6
    y0 = PANEL_C[1] - PANEL_H / 2
    suelo = Line(P(x - 1.2, y0 - 1.05), P(x + 1.6, y0 - 1.05), stroke_color=LINEA, stroke_width=1.4)
    rayas = VGroup(*[Line(P(xx, y0 - 1.05), P(xx - 0.15, y0 - 1.25), stroke_color=LINEA, stroke_width=0.8)
                     for xx in np.arange(x - 1.1, x + 1.6, 0.2)])
    gec = cable(P(PANEL_C[0] - 0.4, y0 + 0.42), P(PANEL_C[0] - 0.4, y0 - 1.15), color=COBRE, w=3)
    var = Rectangle(width=0.08, height=1.0, stroke_width=0.8, stroke_color="#7A4A22").set_fill(COBRE, 1)
    var.move_to(P(PANEL_C[0] - 0.4, y0 - 1.6))
    abr = VGroup(RoundedRectangle(width=0.2, height=0.12, corner_radius=0.02, stroke_color="#7A4A22", stroke_width=0.8)
                 .set_fill("#B87333", 1), tornillo(0.025, "#B87333", 0.3).shift(RIGHT * 0.06)).move_to(P(PANEL_C[0] - 0.4, y0 - 1.15))
    return VGroup(suelo, rayas, gec, var, abr)


# ------------------------------------------------------------------ cajas
def caja_octagonal():
    r = OCT_R
    orejas = VGroup()
    for s in (1, -1):
        o = RoundedRectangle(width=0.32, height=0.2, corner_radius=0.05, stroke_color=METAL_OSC, stroke_width=1.1).set_fill(GAL, 1)
        o.move_to(OCT_C + P(0, s * (r * 0.93 + 0.06)))
        orejas.add(VGroup(o, Circle(radius=0.03, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(WHITE, 1).move_to(o)))
    orejas.rotate(PI / 4, about_point=OCT_C)
    oct_ = RegularPolygon(8, start_angle=PI / 8).scale(r).move_to(OCT_C)
    oct_.set_fill(GAL, 1).set_stroke(METAL_OSC, 1.6)
    fondo = RegularPolygon(8, start_angle=PI / 8).scale(r * 0.86).move_to(OCT_C).set_fill(GAL2, 1).set_stroke(METAL2, 0.8)
    biseles = VGroup(*[Line(oct_.get_vertices()[k], fondo.get_vertices()[k], stroke_color=METAL2, stroke_width=0.7) for k in range(8)])
    kos = VGroup(*[knockout(OCT_C + 0.36 * np.array([np.cos(a), np.sin(a), 0]), 0.075, METAL2, GAL2)
                   for a in (PI / 2 + 0.7, PI / 2 - 0.7)], knockout(OCT_C + P(0, 0.08), 0.1, METAL2, GAL2))
    boss = Circle(radius=0.07, stroke_color=METAL2, stroke_width=0.8).set_fill("#E4E7EC", 1).move_to(OCT_C + P(0.0, -0.4))
    tor_tierra = tornillo(0.045, TIERRA, 0.3).move_to(OCT_C + P(0.0, -0.4))
    tor_tierra.submobjects[0].set_fill(TIERRA)
    g = VGroup(orejas, oct_, fondo, biseles, kos, boss, tor_tierra)
    g.tierra = tor_tierra
    return g


def caja_rect():
    caja = Rectangle(width=SW_W, height=SW_H, stroke_color=METAL_OSC, stroke_width=1.6).set_fill(GAL, 1).move_to(SW_C)
    fondo = Rectangle(width=SW_W - 0.16, height=SW_H - 0.16, stroke_color=METAL2, stroke_width=0.8).set_fill(GAL2, 1).move_to(SW_C)
    biseles = VGroup(*[Line(a, b, stroke_color=METAL2, stroke_width=0.7) for a, b in
                       zip(caja.get_vertices(), fondo.get_vertices())])
    orejas = VGroup()
    for s in (1, -1):
        o = RoundedRectangle(width=0.36, height=0.16, corner_radius=0.03, stroke_color=METAL_OSC, stroke_width=1.1).set_fill(GAL, 1)
        o.move_to(SW_C + P(0, s * (SW_H / 2 - 0.1)))
        orejas.add(VGroup(o, tornillo(0.035, METAL, 0.2).move_to(o)))
    kos = VGroup(*[knockout(SW_C + P(s * 0.33, y), 0.06, METAL2, GAL2) for s in (-1, 1) for y in (0.45, -0.45)])
    return VGroup(caja, fondo, biseles, kos, orejas)


def interruptor(on=False):
    """Interruptor sencillo 15 A 120/277 V: yugo con orejas, cuerpo con nervaduras, palanca; dos bornes de latón
    con placa a la derecha y tornillo verde de tierra en el yugo."""
    c = SW_C + P(-0.08, 0)
    yugo = RoundedRectangle(width=0.34, height=1.46, corner_radius=0.05, stroke_color=METAL_OSC, stroke_width=1.1)
    yugo.set_fill("#D9DDE3", 1).move_to(c)
    orejas = VGroup(*[RoundedRectangle(width=0.5, height=0.14, corner_radius=0.03, stroke_color=METAL_OSC, stroke_width=1)
                      .set_fill("#E4E7EC", 1).move_to(c + P(0, s * 0.66)) for s in (1, -1)])
    ranuras_o = VGroup(*[RoundedRectangle(width=0.14, height=0.05, corner_radius=0.02, stroke_width=0.7,
                                          stroke_color=METAL_OSC).set_fill(WHITE, 1).move_to(c + P(0, s * 0.66)) for s in (1, -1)])
    tornillos_m = VGroup(*[tornillo(0.035, "#E4E7EC", 0.2).move_to(c + P(0, s * 0.55)) for s in (1, -1)])
    cuerpo = RoundedRectangle(width=0.44, height=0.86, corner_radius=0.07, stroke_color=LINEA, stroke_width=1.1)
    cuerpo.set_fill("#F7F7F5", 1).move_to(c)
    nerv = VGroup(*[Line(c + P(-0.18, y), c + P(-0.13, y), stroke_color="#C7C5BE", stroke_width=0.7) for y in np.linspace(-0.35, 0.35, 8)])
    ranura = RoundedRectangle(width=0.17, height=0.5, corner_radius=0.05, stroke_color=METAL2, stroke_width=0.8)
    ranura.set_fill("#ECEBE7", 1).move_to(c)
    pal = VGroup(RoundedRectangle(width=0.13, height=0.34, corner_radius=0.05, stroke_color=LINEA, stroke_width=1).set_fill(WHITE, 1),
                 Line(P(-0.04, 0.12), P(0.04, 0.12), stroke_color="#D0D5DD", stroke_width=0.8))
    pal.move_to(c + P(0, 0.12 if on else -0.12))
    b1 = borne(c + P(0.28, 0.27), 0.05, LATON)
    b2 = borne(c + P(0.28, -0.27), 0.05, LATON)
    v = tornillo(0.042, TIERRA, 0.4).move_to(c + P(-0.08, -0.5))
    hex_ = RegularPolygon(6).scale(0.055).set_fill("#0E8A3E", 1).set_stroke("#0B5E2B", 0.8).move_to(v)
    g = VGroup(yugo, orejas, ranuras_o, cuerpo, ranura, pal, b1, b2, hex_, v, nerv, tornillos_m)
    g.l1, g.l2, g.verde, g.palanca, g.guia = b1.tor, b2.tor, v, pal, ranura
    g.on = on
    return g


def palanca_a(sw, on):
    return sw.palanca.animate.move_to(sw.guia.get_center() + P(0, 0.12 if on else -0.12))


# ------------------------------------------------------------------ rutas de tubería y cables
E = ENTRADA_PANEL
TUBO1 = [E, P(E[0], Y_TECHO), OCT_C + P(-OCT_R, 0)]
TUBO2 = [OCT_C + P(OCT_R, 0), P(SW_C[0], Y_TECHO), P(SW_C[0], SW_C[1] + SW_H / 2)]


def ruta_tubo1(o):
    return [E + P(o, 0), P(E[0] + o, Y_TECHO + o), OCT_C + P(-OCT_R, o)]


def ruta_tubo2(o):
    return [OCT_C + P(OCT_R, o), P(SW_C[0] + o, Y_TECHO + o), P(SW_C[0] + o, SW_C[1] + SW_H / 2)]


PC = PANEL_C
NEU_X = PC[0] + 0.98


def rutas_cables(port, sw, panel):
    """Devuelve dict con los tramos de cada conductor (lista de puntos)."""
    b = panel.nuestro.terminal.get_center()
    tn = panel.tn[0].get_center()
    tt = panel.tt[-1].get_center()
    o = OCT_C
    pl, la = port.plata.get_center(), port.laton.get_center()
    tv = OCT_C + P(0.0, -0.4)
    r = {
        # tablero (dentro del gabinete)
        "neg_tab": [E + P(-0.05, 0), P(E[0] - 0.05, b[1] + 0.25), b + P(0.12, 0.05), b],
        "bla_tab": [E + P(0.05, 0), P(E[0] + 0.05, tn[1] + 0.25), P(NEU_X + 0.15, tn[1] + 0.1), tn],
        "ver_tab": [E + P(0.15, 0), P(E[0] + 0.3, E[1] - 0.3), P(E[0] + 0.3, tt[1] + 0.25), P(tt[0] + 0.2, tt[1] + 0.12), tt],
        # tubo 1
        "neg_t1": ruta_tubo1(-0.045), "bla_t1": ruta_tubo1(0.0), "ver_t1": ruta_tubo1(0.045),
        # caja octagonal
        "neg_oct_a": [o + P(-OCT_R, -0.045), o + P(-0.3, 0.12), o + P(-0.05, 0.28)],
        "neg_oct_b": [o + P(OCT_R, 0.045), o + P(0.3, 0.12), o + P(0.05, 0.28)],
        "bla_oct": [o + P(-OCT_R, 0.0), o + P(-0.3, -0.12), o + P(-0.34, -0.5), pl + P(-0.05, 0.08), pl],
        "roj_oct": [o + P(OCT_R, 0.0), o + P(0.3, -0.12), o + P(0.34, -0.5), la + P(0.05, 0.08), la],
        "ver_oct_a": [o + P(-OCT_R, 0.045), o + P(-0.2, -0.18), o + P(-0.04, -0.22)],
        "ver_oct_b": [o + P(OCT_R, -0.045), o + P(0.2, -0.18), o + P(0.04, -0.22)],
        "ver_oct_c": [o + P(0.0, -0.22), tv],
        # tubo 2  (o<0 a la izquierda en el tramo vertical)
        "neg_t2": ruta_tubo2(0.045), "roj_t2": ruta_tubo2(0.0), "ver_t2": ruta_tubo2(-0.045),
        # caja del interruptor
        "neg_sw": [P(SW_C[0] + 0.045, SW_C[1] + SW_H / 2), P(SW_C[0] + 0.4, sw.l1.get_center()[1] + 0.25),
                   sw.l1.get_center() + P(0.12, 0.0), sw.l1.get_center()],
        "roj_sw": [P(SW_C[0], SW_C[1] + SW_H / 2), P(SW_C[0] + 0.42, SW_C[1] + 0.45), P(SW_C[0] + 0.42, sw.l2.get_center()[1]),
                   sw.l2.get_center() + P(0.1, 0), sw.l2.get_center()],
        "ver_sw": [P(SW_C[0] - 0.045, SW_C[1] + SW_H / 2), P(SW_C[0] - 0.4, SW_C[1] + 0.4),
                   P(SW_C[0] - 0.4, sw.verde.get_center()[1]), sw.verde.get_center()],
    }
    return r


COLOR_DE = {"neg": FASE, "bla": NEUTRO, "ver": TIERRA, "roj": RETORNO}


def multimetro():
    """Multímetro digital: carcasa con funda, pantalla LCD, selector rotatorio y bornes. .lcd = rectángulo."""
    funda = RoundedRectangle(width=2.1, height=3.4, corner_radius=0.3, stroke_color="#B54708", stroke_width=1.5).set_fill(AMBAR, 1)
    cuerpo = RoundedRectangle(width=1.75, height=3.05, corner_radius=0.18, stroke_color="#101318", stroke_width=1.2).set_fill("#2A2E35", 1)
    lcd_marco = RoundedRectangle(width=1.45, height=0.85, corner_radius=0.06, stroke_width=0).set_fill("#101318", 1).shift(UP * 0.9)
    lcd = RoundedRectangle(width=1.3, height=0.68, corner_radius=0.04, stroke_width=0).set_fill("#C9D6C3", 1).move_to(lcd_marco)
    dial = Circle(radius=0.5, stroke_color="#101318", stroke_width=1.2).set_fill("#454B55", 1).shift(DOWN * 0.3)
    perilla = RoundedRectangle(width=0.16, height=0.8, corner_radius=0.06, stroke_width=0).set_fill("#D0D5DD", 1).move_to(dial).rotate(-0.6)
    marcas = VGroup(*[Line(dial.get_center() + 0.58 * np.array([np.cos(a), np.sin(a), 0]),
                           dial.get_center() + 0.66 * np.array([np.cos(a), np.sin(a), 0]), stroke_color="#E4E7EC", stroke_width=1)
                      for a in np.linspace(PI * 0.1, PI * 0.9, 7)])
    simb = T("Ω  ·)))", 12, "#E4E7EC", "BOLD").move_to(dial.get_center() + UP * 0.78 + RIGHT * 0.45)
    bornes = VGroup(*[VGroup(Circle(radius=0.11, stroke_color="#101318", stroke_width=1).set_fill(c_, 1),
                             Circle(radius=0.05, stroke_width=0).set_fill("#101318", 1)).move_to(P(x, -1.25))
                      for x, c_ in ((-0.45, "#101318"), (0.0, "#454B55"), (0.45, ROJO))])
    g = VGroup(funda, cuerpo, lcd_marco, lcd, dial, marcas, perilla, simb, bornes)
    g.lcd = lcd
    g.borne_com, g.borne_v = bornes[0], bornes[2]
    return g


def punta_prueba(color=ROJO):
    mango = RoundedRectangle(width=0.18, height=0.9, corner_radius=0.07, stroke_color=_osc(color, 0.4), stroke_width=1).set_fill(color, 1)
    guarda = RoundedRectangle(width=0.28, height=0.06, corner_radius=0.02, stroke_width=0).set_fill(_osc(color, 0.3), 1).shift(DOWN * 0.3)
    punta = Polygon(P(-0.03, -0.45), P(0.03, -0.45), P(0.0, -0.75), stroke_color=METAL_OSC, stroke_width=0.8).set_fill(METAL, 1)
    g = VGroup(mango, guarda, punta)
    g.tip = punta
    return g


def interruptor_inteligente():
    placa = RoundedRectangle(width=1.2, height=1.9, corner_radius=0.12, stroke_color=METAL2, stroke_width=1.4).set_fill(WHITE, 1)
    tecla = RoundedRectangle(width=0.8, height=1.3, corner_radius=0.1, stroke_color="#D0D5DD", stroke_width=1).set_fill("#F7F8FA", 1)
    led = Dot(radius=0.04, color=MARCA).shift(DOWN * 0.45)
    wifi = VGroup(*[Arc(radius=r, start_angle=PI / 4, angle=PI / 2, stroke_color=MARCA, stroke_width=3) for r in (0.12, 0.22, 0.32)],
                  Dot(radius=0.035, color=MARCA)).shift(UP * 0.1)
    for a in wifi[:3]:
        a.move_arc_center_to(wifi[3].get_center())
    return VGroup(placa, tecla, led, wifi)

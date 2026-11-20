"""Ilustraciones planas con detalle (línea fina): pajarito, cuervo, águila, poste con cruceta y aisladores,
camión canastilla con liniero, persona, tanque, pila, iconos."""
from comun_e import *
from comun_e import _osc, _cla

PLUMA = "#4FA3C7"
PLUMA_OSC = "#2B6F8E"
PLUMA_CL = "#8CC8E2"
PECHO = "#F3E3D3"
MADERA = "#A27B5C"
MADERA_OSC = "#6F4E37"
PIEL = "#F2C6A0"
PIEL_OSC = "#D9A47C"


def _cerrada(pts, color, borde=LINEA, w=1.4):
    m = VMobject().set_points_smoothly([np.array([x, y, 0]) for x, y in pts] + [np.array([*pts[0], 0])])
    return m.set_fill(color, 1).set_stroke(borde, w)


def _pluma(base, punta, ancho, color, borde=LINEA, w=1.0):
    """Pluma alargada (hoja) entre base y punta."""
    base, punta = np.array(base, float), np.array(punta, float)
    d = punta - base
    n = np.array([-d[1], d[0], 0]) / (np.linalg.norm(d) + 1e-9)
    pts = [base + n * ancho * 0.5, base + d * 0.55 + n * ancho * 0.55, punta, base + d * 0.55 - n * ancho * 0.55,
           base - n * ancho * 0.5]
    m = VMobject().set_points_smoothly(pts + [pts[0]])
    return m.set_fill(color, 1).set_stroke(borde, w)


def _patas(xs, color="#B07A3A", y_top=0.24):
    """Patas con dedos que abrazan el cable (y=0). [k][0] es la pata; su get_end() = punto de apoyo."""
    g = VGroup()
    for x in xs:
        pata = Line([x, y_top, 0], [x - 0.02, 0.03, 0], stroke_color=color, stroke_width=2.2)
        dedos = VGroup(Arc(radius=0.055, start_angle=PI * 0.15, angle=-PI * 1.05, stroke_color=color, stroke_width=1.8)
                       .move_to([x - 0.04, -0.005, 0]),
                       Arc(radius=0.05, start_angle=PI * 0.9, angle=PI * 0.9, stroke_color=color, stroke_width=1.6)
                       .move_to([x + 0.03, -0.01, 0]))
        g.add(VGroup(pata, dedos))
    return g


def pajarito(mirar=LEFT, plumas=(PLUMA, PLUMA_OSC, PLUMA_CL, PECHO), pico=AMBAR):
    """Pajarito de perfil con plumaje por capas. Las patas terminan en y=0 (el cable). Índice [1] = patas."""
    c_cuerpo, c_osc, c_cl, c_pecho = plumas
    cola = VGroup(*[_pluma([0.38, 0.52, 0], [1.02 + 0.03 * k, 0.88 - 0.13 * k, 0], 0.16, c_osc, w=1.0) for k in range(3)])
    cuerpo = _cerrada([(-0.55, 0.62), (-0.35, 0.95), (0.05, 0.98), (0.45, 0.72), (0.42, 0.4), (0.0, 0.2),
                       (-0.38, 0.28)], c_cuerpo)
    pecho = _cerrada([(-0.52, 0.62), (-0.38, 0.34), (-0.05, 0.23), (0.15, 0.36), (-0.1, 0.55), (-0.35, 0.72)], c_pecho, w=0)
    motas = VGroup(*[Arc(radius=0.03, start_angle=PI * 1.15, angle=PI * 0.7, stroke_color=_osc(c_pecho, 0.25),
                         stroke_width=1).move_to([x, y, 0]) for x, y in ((-0.35, 0.5), (-0.22, 0.4), (-0.08, 0.32),
                                                                          (-0.28, 0.33), (-0.15, 0.48))])
    # ala: cobertoras (escamas) + secundarias + primarias
    primarias = VGroup(*[_pluma([0.05 + 0.04 * k, 0.66 - 0.02 * k, 0], [0.72 - 0.05 * k, 0.5 + 0.03 * k, 0], 0.13, _osc(c_osc, 0.15), w=0.9)
                         for k in range(3)])
    secundarias = VGroup(*[_pluma([-0.08 + 0.05 * k, 0.72, 0], [0.42 + 0.03 * k, 0.6 - 0.02 * k, 0], 0.14, c_osc, w=0.9)
                           for k in range(3)])
    cobert = VGroup(*[Arc(radius=0.07, start_angle=PI, angle=PI, stroke_color=_cla(c_cuerpo, 0.4), stroke_width=1.1)
                      .set_fill(c_cuerpo, 1).move_to([x, y, 0]) for x, y in ((-0.12, 0.8), (0.0, 0.82), (0.12, 0.8),
                                                                              (-0.06, 0.72), (0.06, 0.73))])
    bordes = VGroup(*[Line([0.1 + 0.11 * k, 0.6, 0], [0.24 + 0.11 * k, 0.66, 0], stroke_color=c_cl, stroke_width=0.9)
                      for k in range(3)])
    cabeza = Circle(radius=0.28, stroke_color=LINEA, stroke_width=1.4).set_fill(c_cuerpo, 1).move_to([-0.5, 1.02, 0])
    gorra = Intersection(Circle(radius=0.28).move_to([-0.5, 1.02, 0]), Circle(radius=0.3).move_to([-0.42, 1.24, 0]))
    gorra.set_fill(c_osc, 1).set_stroke(width=0)
    mejilla = Ellipse(width=0.15, height=0.08).set_fill(_cla(c_cuerpo, 0.45), 1).set_stroke(width=0).move_to([-0.52, 0.96, 0])
    pico_s = Polygon([-0.74, 1.08, 0], [-0.98, 1.0, 0], [-0.74, 1.0, 0], stroke_color=_osc(pico, 0.45), stroke_width=1.1).set_fill(pico, 1)
    pico_i = Polygon([-0.74, 1.0, 0], [-0.93, 0.99, 0], [-0.74, 0.94, 0], stroke_color=_osc(pico, 0.45), stroke_width=1.1).set_fill(_osc(pico, 0.15), 1)
    ojo = VGroup(Circle(radius=0.072, stroke_width=0).set_fill(WHITE, 1).move_to([-0.57, 1.08, 0]),
                 Circle(radius=0.052, stroke_width=0).set_fill(TINTA, 1).move_to([-0.575, 1.08, 0]),
                 Circle(radius=0.017, stroke_width=0).set_fill(WHITE, 1).move_to([-0.56, 1.095, 0]))
    patas = _patas((-0.13, 0.13))
    g = VGroup(cola, patas, cuerpo, pecho, VGroup(secundarias, primarias, cobert, bordes), motas, cabeza, gorra, mejilla,
               pico_i, pico_s, ojo)
    if mirar is RIGHT:
        g.flip(UP, about_point=ORIGIN)
    return g


def patas_de(p):
    return [p[1][0][0].get_end(), p[1][1][0].get_end()]


def cuervo():
    """Ave grande oscura (cuervo/zanate) de perfil, patas en y=0. Índice [4] = ala."""
    return pajarito(plumas=("#2B2F3A", "#14171D", "#5A6272", "#3C424F"), pico="#1D2029")


def aguila(envergadura=4.4):
    """Águila calva de frente con alas abiertas: plumas primarias separadas ("dedos"), cabeza blanca, garras.
    Patas en y=0. Índices: [0] ala derecha, [1] ala izquierda, [3] patas."""
    s = envergadura / 4.4
    CAFE, CAFE_OSC, CAFE_CL = "#5A3E2B", "#3E2A1C", "#7B5A41"

    def ala(signo):
        base = Polygon(*[[signo * x, y, 0] for x, y in [(0.25, 0.95), (0.8, 1.28), (1.45, 1.38), (1.85, 1.25),
                                                       (1.75, 0.62), (1.2, 0.5), (0.6, 0.45), (0.25, 0.42)]],
                       stroke_color=LINEA, stroke_width=1.3).set_fill(CAFE, 1)
        cob = VGroup(*[Arc(radius=0.11, start_angle=PI, angle=PI, stroke_color=CAFE_CL, stroke_width=1)
                       .move_to([signo * x, y, 0]) for x, y in ((0.55, 1.12), (0.8, 1.18), (1.05, 1.2), (1.3, 1.2),
                                                                  (0.68, 1.0), (0.93, 1.03), (1.18, 1.03))])
        secs = VGroup(*[_pluma([signo * x, 0.72, 0], [signo * (x + 0.04), 0.36, 0], 0.17, CAFE_OSC, w=0.9)
                        for x in np.linspace(0.4, 1.55, 7)])
        prims = VGroup(*[_pluma([signo * 1.7, 0.95 + 0.05 * k, 0], [signo * (2.25 + 0.03 * k), 0.55 + 0.17 * k, 0], 0.15,
                                CAFE_OSC, w=0.9) for k in range(5)])
        return VGroup(secs, prims, base, cob)

    cola = VGroup(*[_pluma([0, 0.25, 0], [x, -0.2, 0], 0.16, WHITE, w=1.0) for x in (-0.2, -0.07, 0.07, 0.2)])
    patas = VGroup(*[VGroup(Line([x, 0.24, 0], [x, 0.02, 0], stroke_color=AMBAR, stroke_width=4),
                            *[Line([x, 0.03, 0], [x + dx, -0.04, 0], stroke_color="#1D2029", stroke_width=1.6)
                              for dx in (-0.06, 0, 0.06)]) for x in (-0.12, 0.12)])
    cuerpo = _cerrada([(0, 1.22), (0.33, 1.02), (0.38, 0.55), (0.22, 0.2), (0, 0.13), (-0.22, 0.2), (-0.38, 0.55),
                       (-0.33, 1.02)], CAFE)
    pecho = VGroup(*[VMobject().set_points_as_corners([[x - 0.045, y + 0.035, 0], [x, y, 0], [x + 0.045, y + 0.035, 0]])
                     .set_stroke(CAFE_CL, 1) for x, y in ((-0.12, 0.85), (0.1, 0.8), (-0.05, 0.6), (0.14, 0.5),
                                                          (-0.15, 0.42), (0.02, 0.32))])
    cabeza = _cerrada([(0, 1.66), (0.22, 1.58), (0.27, 1.38), (0.18, 1.18), (0, 1.12), (-0.18, 1.18), (-0.27, 1.38),
                       (-0.22, 1.58)], WHITE)
    cejas = VGroup(*[Line([s_ * 0.05, 1.47, 0], [s_ * 0.17, 1.5, 0], stroke_color=LINEA, stroke_width=1.6) for s_ in (-1, 1)])
    ojos = VGroup(*[VGroup(Circle(radius=0.035, stroke_width=0).set_fill(AMBAR, 1),
                           Circle(radius=0.018, stroke_width=0).set_fill(TINTA, 1)).move_to([s_ * 0.11, 1.42, 0]) for s_ in (-1, 1)])
    pico = VGroup(Polygon([-0.07, 1.36, 0], [0.07, 1.36, 0], [0.05, 1.22, 0], [0.0, 1.15, 0], [-0.05, 1.22, 0],
                          stroke_color=_osc(AMBAR, 0.45), stroke_width=1.1).set_fill(AMBAR, 1),
                  Line([-0.06, 1.3, 0], [0.06, 1.3, 0], stroke_color=_osc(AMBAR, 0.45), stroke_width=0.8))
    return VGroup(ala(1), ala(-1), cola, patas, cuerpo, pecho, cabeza, cejas, ojos, pico).scale(s, about_point=ORIGIN)


# ------------------------------------------------------------------ personas
def persona(traje=MARCA, casco=None, piel=PIEL, pantalon="#344054", pelo="#2B2118"):
    """Persona de frente con cara, cuello, camisa con cuello y botones, cinturón, jeans y zapatos. Pies en y=0.
    Índices: [0] piernas, [1] torso, [2] cabeza."""
    zap = VGroup(*[RoundedRectangle(width=0.36, height=0.13, corner_radius=0.06, stroke_color=LINEA, stroke_width=1.2)
                   .set_fill("#1D2029", 1).move_to([x * 1.08, 0.065, 0]) for x in (-0.19, 0.19)])
    piernas = VGroup(*[RoundedRectangle(width=0.3, height=0.95, corner_radius=0.12, stroke_color=LINEA,
                                        stroke_width=1.3).set_fill(pantalon, 1).move_to([x, 0.55, 0]) for x in (-0.18, 0.18)])
    costura = VGroup(*[Line([x, 0.2, 0], [x, 0.95, 0], stroke_color=_cla(pantalon, 0.3), stroke_width=0.7) for x in (-0.12, 0.12)])
    torso = RoundedRectangle(width=0.82, height=1.08, corner_radius=0.25, stroke_color=LINEA, stroke_width=1.3)
    torso.set_fill(traje, 1).move_to([0, 1.5, 0])
    cinturon = Rectangle(width=0.74, height=0.08, stroke_width=0).set_fill("#3B2A20", 1).move_to([0, 1.02, 0])
    hebilla = Rectangle(width=0.1, height=0.07, stroke_color=LATON, stroke_width=1.2).move_to([0, 1.02, 0])
    cuello_c = VGroup(*[Polygon([0, 1.98, 0], [s * 0.16, 2.05, 0], [s * 0.12, 1.88, 0], stroke_color=_osc(traje, 0.35),
                                stroke_width=1).set_fill(_cla(traje, 0.15), 1) for s in (-1, 1)])
    botones = VGroup(*[Dot([0, y, 0], radius=0.018, color=_osc(traje, 0.4)) for y in (1.8, 1.6, 1.4, 1.2)])
    placket = Line([0, 1.9, 0], [0, 1.08, 0], stroke_color=_osc(traje, 0.3), stroke_width=0.8)
    cuello = Rectangle(width=0.16, height=0.12, stroke_width=0).set_fill(PIEL_OSC, 1).move_to([0, 2.04, 0])
    cara = Ellipse(width=0.46, height=0.54, stroke_color=LINEA, stroke_width=1.3).set_fill(piel, 1).move_to([0, 2.33, 0])
    orejas = VGroup(*[Ellipse(width=0.08, height=0.14, stroke_color=LINEA, stroke_width=1).set_fill(piel, 1).move_to([s * 0.23, 2.32, 0])
                      for s in (-1, 1)])
    ojos = VGroup(*[Dot([s * 0.09, 2.36, 0], radius=0.024, color=TINTA) for s in (-1, 1)])
    cejas = VGroup(*[Line([s * 0.05, 2.43, 0], [s * 0.14, 2.44, 0], stroke_color=pelo, stroke_width=1.6) for s in (-1, 1)])
    nariz = Line([0, 2.33, 0], [0.02, 2.27, 0], stroke_color=PIEL_OSC, stroke_width=1.2)
    boca = Arc(radius=0.07, start_angle=PI * 1.2, angle=PI * 0.6, stroke_color="#9A4A3A", stroke_width=1.4).move_to([0, 2.2, 0])
    cabeza = VGroup(orejas, cara, ojos, cejas, nariz, boca)
    if casco:
        cabeza.add(VGroup(Arc(radius=0.29, start_angle=0, angle=PI, stroke_color=_osc(casco, 0.4), stroke_width=1.2)
                          .set_fill(casco, 1).move_to([0, 2.58, 0]),
                          RoundedRectangle(width=0.7, height=0.07, corner_radius=0.03, stroke_color=_osc(casco, 0.4),
                                           stroke_width=1).set_fill(casco, 1).move_to([0, 2.47, 0]),
                          Line([0, 2.5, 0], [0, 2.72, 0], stroke_color=_osc(casco, 0.25), stroke_width=1.4)))
    else:
        cabeza.add(_cerrada([(-0.24, 2.36), (-0.22, 2.56), (0, 2.64), (0.22, 2.56), (0.24, 2.36), (0.14, 2.5), (-0.1, 2.5)],
                            pelo, w=0))
    g = VGroup(VGroup(piernas, costura, zap), VGroup(torso, placket, botones, cuello_c, cinturon, hebilla), cabeza, cuello)
    return g


def brazo(a, b, color=MARCA, w=11, guante=None):
    m = Line(a, b).set_stroke(_osc(color, 0.3), w + 2)
    m2 = Line(a, b).set_stroke(color, w)
    for x in (m, m2):
        x.set_cap_style(CapStyleType.ROUND)
    mano = Circle(radius=0.085, stroke_color=LINEA, stroke_width=1.1).set_fill(guante or PIEL, 1).move_to(b)
    return VGroup(m, m2, mano)


def camion_canastilla(base=np.array([3.0, -3.0, 0]), punta=np.array([0.55, 0.15, 0])):
    """Camión canastilla (bucket truck): cabina con ventana, llantas con rin, plataforma, estabilizadores,
    pluma inferior metálica y superior de fibra aislante (bandas), canastilla de fibra con borde.
    Devuelve VGroup con .canasta y .pluma_aislada."""
    bx, by = base[0], base[1]
    chasis = RoundedRectangle(width=3.3, height=0.32, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.3)
    chasis.set_fill("#475467", 1).move_to([bx, by - 0.05, 0])
    cabina = VGroup(_cerrada([(bx + 0.9, by + 0.1), (bx + 0.9, by + 0.95), (bx + 1.35, by + 0.98), (bx + 1.62, by + 0.55),
                              (bx + 1.65, by + 0.1)], WHITE, w=1.3))
    ventana = Polygon([bx + 1.0, by + 0.86, 0], [bx + 1.32, by + 0.87, 0], [bx + 1.52, by + 0.55, 0], [bx + 1.0, by + 0.55, 0],
                      stroke_color=LINEA, stroke_width=1).set_fill("#BFE3F2", 1)
    puerta = Line([bx + 1.0, by + 0.45, 0], [bx + 1.0, by + 0.12, 0], stroke_color=METAL2, stroke_width=1)
    faro = Circle(radius=0.05, stroke_color=LINEA, stroke_width=0.8).set_fill(AMBAR, 1).move_to([bx + 1.6, by + 0.3, 0])
    franja = Rectangle(width=0.74, height=0.06, stroke_width=0).set_fill(MARCA, 1).move_to([bx + 1.27, by + 0.25, 0])
    caja = RoundedRectangle(width=1.9, height=0.55, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.3).set_fill(WHITE, 1)
    caja.move_to([bx - 0.2, by + 0.38, 0])
    compart = VGroup(*[RoundedRectangle(width=0.5, height=0.38, corner_radius=0.03, stroke_color=METAL2, stroke_width=0.9)
                       .move_to([bx - 0.85 + 0.62 * k, by + 0.38, 0]) for k in range(3)])
    manijas = VGroup(*[Line([bx - 0.95 + 0.62 * k, by + 0.38, 0], [bx - 0.75 + 0.62 * k, by + 0.38, 0], stroke_color=METAL_OSC,
                            stroke_width=1.4) for k in range(3)])

    def llanta(x):
        return VGroup(Circle(radius=0.3, stroke_color=LINEA, stroke_width=1.2).set_fill("#1D2029", 1),
                      Circle(radius=0.15, stroke_color=METAL_OSC, stroke_width=1).set_fill("#D0D5DD", 1),
                      *[Dot(radius=0.018, color=METAL_OSC).shift(0.09 * np.array([np.cos(a), np.sin(a), 0]))
                        for a in np.linspace(0, TAU, 6, endpoint=False)]).move_to([x, by - 0.3, 0])
    llantas = VGroup(llanta(bx - 0.9), llanta(bx + 1.25))
    estab = VGroup(Line([bx - 1.25, by - 0.1, 0], [bx - 1.45, by - 0.55, 0], stroke_color=METAL_OSC, stroke_width=3),
                   RoundedRectangle(width=0.25, height=0.06, corner_radius=0.02, stroke_width=0).set_fill("#475467", 1)
                   .move_to([bx - 1.45, by - 0.57, 0]))
    torreta = RoundedRectangle(width=0.4, height=0.3, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.2)
    torreta.set_fill("#D0D5DD", 1).move_to([bx - 0.5, by + 0.8, 0])
    codo = np.array([bx - 0.5, by + 0.85, 0]) + (punta - np.array([bx - 0.5, by + 0.85, 0])) * 0.45
    inf = VGroup(Line([bx - 0.5, by + 0.85, 0], codo).set_stroke(_osc("#E4E7EC", 0.35), 15),
                 Line([bx - 0.5, by + 0.85, 0], codo).set_stroke("#E4E7EC", 12))
    sup_a = Line(codo, punta).set_stroke(_osc("#FEC84B", 0.35), 13)
    sup_b = Line(codo, punta).set_stroke("#FEC84B", 10)
    d = punta - codo
    n = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
    bandas = VGroup(*[Line(codo + d * t - n * 0.07, codo + d * t + n * 0.07, stroke_color="#B54708", stroke_width=2)
                      for t in (0.15, 0.25, 0.35)])
    piston = Line([bx - 0.3, by + 0.75, 0], codo * 0.5 + np.array([bx - 0.5, by + 0.85, 0]) * 0.5 + n * 0.12,
                  stroke_color=METAL_OSC, stroke_width=3)
    for m in (inf[0], inf[1], sup_a, sup_b):
        m.set_cap_style(CapStyleType.ROUND)
    canasta = VGroup(RoundedRectangle(width=1.0, height=0.95, corner_radius=0.1, stroke_color="#B54708", stroke_width=1.4)
                     .set_fill("#FEC84B", 1),
                     RoundedRectangle(width=1.08, height=0.12, corner_radius=0.05, stroke_color="#B54708", stroke_width=1.2)
                     .set_fill("#FDB022", 1).shift(UP * 0.44),
                     Line([-0.35, -0.3, 0], [0.35, -0.3, 0], stroke_color="#F79009", stroke_width=1),
                     Text("AISLADA", font=SANS, font_size=9, color="#B54708", weight="BOLD").shift(DOWN * 0.12))
    canasta.move_to(punta + np.array([-0.05, 0.42, 0]))
    g = VGroup(estab, llantas, chasis, caja, compart, manijas, cabina, ventana, puerta, franja, faro, torreta,
               piston, inf, sup_a, sup_b, bandas, canasta)
    g.canasta, g.pluma_aislada = canasta, VGroup(sup_a, sup_b, bandas)
    return g


# ------------------------------------------------------------------ poste
def aislador_pin(c, h=0.42, color="#EEF0EA"):
    """Aislador tipo pin (porcelana) con tres faldones, cuello y ranura superior; perno debajo."""
    k_ = h / 0.42
    x, y = c[0], c[1]
    perno = Rectangle(width=0.06, height=0.14, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(METAL2, 1).move_to([x, y - h * 0.05, 0])
    falds = VGroup()
    for k, (w_, yy) in enumerate(((0.44 * k_, 0.12), (0.36 * k_, 0.24), (0.28 * k_, 0.36))):
        f = Polygon([x - w_ / 2, y + yy * h / 0.42 - 0.02, 0], [x + w_ / 2, y + yy * h / 0.42 - 0.02, 0],
                    [x + w_ * 0.3, y + yy * h / 0.42 + 0.06, 0], [x - w_ * 0.3, y + yy * h / 0.42 + 0.06, 0],
                    stroke_color="#9AA096", stroke_width=0.9).set_fill(color, 1)
        falds.add(f)
    cuerpo = RoundedRectangle(width=0.16 * k_, height=h * 0.85, corner_radius=0.05, stroke_color="#9AA096", stroke_width=0.9)
    cuerpo.set_fill(_osc(color, 0.04), 1).move_to([x, y + h * 0.5, 0])
    copa = RoundedRectangle(width=0.22 * k_, height=0.09 * k_, corner_radius=0.03, stroke_color="#9AA096", stroke_width=0.9).set_fill(color, 1)
    copa.move_to([x, y + h + 0.0, 0])
    brillo = Line([x - 0.05, y + h * 0.2, 0], [x - 0.05, y + h * 0.85, 0], stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.9)
    return VGroup(perno, cuerpo, falds, copa, brillo)


def poste(altura=7.0, ancho_cruceta=5.0, n=2):
    """Poste de madera (veta, pernos, conductor de tierra) con cruceta, tirantes metálicos y aisladores de pin.
    Devuelve (grupo, puntos_de_conductor). Índice [3] = cruceta."""
    palo = Rectangle(width=0.36, height=altura, stroke_color=MADERA_OSC, stroke_width=1.4).set_fill(MADERA, 1)
    palo.move_to([0, -altura / 2, 0])
    vetas = VGroup(*[Line([x, -altura + 0.3, 0], [x + 0.01, -0.25, 0], stroke_color=MADERA_OSC, stroke_width=0.7,
                          stroke_opacity=0.55) for x in (-0.1, -0.02, 0.08)],
                   *[Arc(radius=0.05, start_angle=0, angle=PI, stroke_color=MADERA_OSC, stroke_width=0.7, stroke_opacity=0.6)
                     .move_to([0.03, y, 0]) for y in (-1.6, -3.1, -4.4) if y > -altura])
    tope = Polygon([-0.18, 0, 0], [0.18, 0, 0], [0.12, 0.1, 0], [-0.12, 0.1, 0], stroke_color=MADERA_OSC, stroke_width=1.2).set_fill(_osc(MADERA, 0.15), 1)
    cruceta = Rectangle(width=ancho_cruceta, height=0.24, stroke_color=MADERA_OSC, stroke_width=1.4).set_fill(MADERA, 1)
    cruceta.move_to([0, -0.4, 0])
    veta_c = VGroup(*[Line([-ancho_cruceta / 2 + 0.1, -0.4 + dy, 0], [ancho_cruceta / 2 - 0.1, -0.4 + dy, 0], stroke_color=MADERA_OSC,
                           stroke_width=0.6, stroke_opacity=0.5) for dy in (-0.05, 0.05)])
    tir = VGroup()
    for s in (-1, 1):
        a, b = np.array([s * ancho_cruceta * 0.28, -0.52, 0]), np.array([0, -1.35, 0])
        tir.add(Line(a, b).set_stroke(METAL_OSC, 3.2), Line(a, b).set_stroke(METAL, 1.6))
    pernos = VGroup(*[tornillo(0.045, METAL, 0.4, cruz=False).move_to(p) for p in
                      ([0, -0.4, 0], [0, -1.35, 0], [-ancho_cruceta * 0.28, -0.4, 0], [ancho_cruceta * 0.28, -0.4, 0])])
    xs = np.linspace(-ancho_cruceta / 2 + 0.4, ancho_cruceta / 2 - 0.4, n)
    ais = VGroup()
    puntos = []
    for x in xs:
        a = aislador_pin([x, -0.28, 0], 0.72)
        ais.add(a)
        puntos.append(np.array([x, a[3].get_top()[1] + 0.07, 0]))
    tierra_p = Line([0.16, -0.6, 0], [0.16, -altura + 0.2, 0], stroke_color=COBRE, stroke_width=1.6)
    grapas = VGroup(*[Line([0.12, y, 0], [0.2, y, 0], stroke_color=METAL_OSC, stroke_width=1.6) for y in np.arange(-1.0, -altura, -0.7)])
    return VGroup(palo, vetas, tir, cruceta, ais, veta_c, pernos, tope, tierra_p, grapas), puntos


def conductor_frente(c, r=0.15):
    """Conductor ACSR visto de frente: hilos de aluminio alrededor del alma de acero."""
    g = VGroup(Circle(radius=r, stroke_color=LINEA, stroke_width=1.2).set_fill("#B8BEC8", 1))
    for k in range(6):
        a = TAU * k / 6
        g.add(Circle(radius=r * 0.33, stroke_color="#8C96A3", stroke_width=0.7).set_fill("#D0D5DD", 1)
              .move_to(np.array([np.cos(a), np.sin(a), 0]) * r * 0.62))
    g.add(Circle(radius=r * 0.3, stroke_color="#5B6573", stroke_width=0.7).set_fill("#7C8594", 1))
    return g.move_to(c)


def linea_aerea(a, b, flecha=0.25, color="#5B6573", w=3.2):
    a, b = np.array(a, float), np.array(b, float)
    pts = [a + (b - a) * t + DOWN * flecha * 4 * t * (1 - t) for t in np.linspace(0, 1, 30)]
    m = VMobject().set_points_smoothly(pts).set_stroke(color, w)
    return m


def cable_acsr(a, b, w=26):
    """Cable desnudo de aluminio de cerca: hilos trenzados."""
    a, b = np.array(a, float), np.array(b, float)
    base = cable(a, b, color="#B8BEC8", w=w)
    largo = np.linalg.norm(b - a)
    alto = w / 100
    hilos = VGroup(*[Line(a + RIGHT * x + DOWN * alto * 0.45, a + RIGHT * (x + alto * 0.9) + UP * alto * 0.45,
                          stroke_color="#8C96A3", stroke_width=1.1) for x in np.arange(0, largo - alto, alto * 0.42)])
    brillo = Line(a + UP * alto * 0.22, b + UP * alto * 0.22, stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.7)
    return VGroup(base, hilos, brillo)


def tanque(agua=0.6, color="#5AB3E6"):
    caja = Rectangle(width=1.4, height=1.8, stroke_color=LINEA, stroke_width=1.6).set_fill(WHITE, 1)
    nivel = Rectangle(width=1.4, height=1.8 * agua, stroke_width=0).set_fill(color, 0.75)
    nivel.align_to(caja, DOWN)
    return VGroup(caja, nivel, caja.copy().set_fill(opacity=0))


def pila_aa():
    cuerpo = RoundedRectangle(width=0.7, height=1.9, corner_radius=0.08, stroke_color=LINEA, stroke_width=1.6)
    cuerpo.set_fill("#1D2939", 1)
    franja = Rectangle(width=0.7, height=0.55, stroke_width=0).set_fill(AMBAR, 1).move_to(cuerpo.get_top() + DOWN * 0.35)
    tapa = RoundedRectangle(width=0.26, height=0.12, corner_radius=0.03, stroke_color=LINEA, stroke_width=1.2)
    tapa.set_fill(METAL, 1).next_to(cuerpo, UP, buff=0)
    brillo = Line(cuerpo.get_corner(UL) + P(0.12, -0.1), cuerpo.get_corner(DL) + P(0.12, 0.1), stroke_color=WHITE,
                  stroke_width=2, stroke_opacity=0.35)
    txt = T("1.5 V", 22, WHITE, "BOLD").rotate(PI / 2).move_to(cuerpo.get_center() + DOWN * 0.25)
    return VGroup(cuerpo, franja, tapa, brillo, txt)


def P(x, y):
    return np.array([x, y, 0.0])


def no_simbolo(r=0.5, color=ROJO):
    c = Circle(radius=r, stroke_color=color, stroke_width=5)
    l = Line([-r * 0.7, -r * 0.7, 0], [r * 0.7, r * 0.7, 0], stroke_color=color, stroke_width=5)
    return VGroup(c, l)


def check(color=VERDE_OK, s=0.4):
    c = Circle(radius=s, stroke_width=0).set_fill(color, 1)
    v = VMobject().set_points_as_corners([[-0.45 * s, 0, 0], [-0.1 * s, -0.35 * s, 0], [0.5 * s, 0.35 * s, 0]])
    v.set_stroke(WHITE, 4)
    return VGroup(c, v)


def equis(color=ROJO, s=0.4):
    c = Circle(radius=s, stroke_width=0).set_fill(color, 1)
    a = Line([-0.4 * s, -0.4 * s, 0], [0.4 * s, 0.4 * s, 0]).set_stroke(WHITE, 4)
    b = Line([-0.4 * s, 0.4 * s, 0], [0.4 * s, -0.4 * s, 0]).set_stroke(WHITE, 4)
    return VGroup(c, a, b)


def escalera(alto=3.2, ancho=0.6):
    rieles = VGroup(*[VGroup(Line([x, 0, 0], [x, alto, 0], stroke_color="#7A2E0E", stroke_width=5),
                             Line([x, 0, 0], [x, alto, 0], stroke_color="#F79009", stroke_width=3)) for x in (-ancho / 2, ancho / 2)])
    pasos = VGroup(*[VGroup(Line([-ancho / 2, y, 0], [ancho / 2, y, 0], stroke_color="#98A2B3", stroke_width=4),
                            Line([-ancho / 2, y + 0.02, 0], [ancho / 2, y + 0.02, 0], stroke_color=WHITE, stroke_width=1))
                     for y in np.arange(0.35, alto, 0.4)])
    pies = VGroup(*[RoundedRectangle(width=0.12, height=0.06, corner_radius=0.02, stroke_width=0).set_fill("#1D2029", 1)
                    .move_to([x, 0, 0]) for x in (-ancho / 2, ancho / 2)])
    return VGroup(pasos, rieles, pies)


def piscucha():
    rombo = Polygon([0, 0.6, 0], [0.42, 0, 0], [0, -0.75, 0], [-0.42, 0, 0], stroke_color=LINEA, stroke_width=1.4)
    rombo.set_fill(ROJO, 1)
    mitad = Polygon([0, 0.6, 0], [0.42, 0, 0], [0, -0.75, 0], stroke_width=0).set_fill(AMBAR, 1)
    cruz = VGroup(Line([0, 0.6, 0], [0, -0.75, 0]), Line([-0.42, 0, 0], [0.42, 0, 0])).set_stroke(LINEA, 1)
    cola = VMobject().set_points_smoothly([[0, -0.75, 0], [0.15, -1.1, 0], [-0.1, -1.4, 0], [0.1, -1.7, 0]])
    cola.set_stroke(LINEA, 1)
    lazos = VGroup(*[Polygon([0, 0, 0], [0.1, 0.06, 0], [0.1, -0.06, 0], [-0.1, 0.06, 0], [-0.1, -0.06, 0], stroke_width=0)
                     .set_fill(c_, 1).move_to(cola.point_from_proportion(t)) for t, c_ in ((0.3, MARCA), (0.6, VERDE_OK), (0.9, AMBAR))])
    return VGroup(cola, lazos, rombo, mitad, cruz)

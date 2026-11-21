"""Símbolos IEC 60617 dibujados como en el Manual electrotécnico Telesquemario (cap. 7, esquemas básicos).
Reglas tomadas del manual:
- Contacto fijo arriba; su extremo lleva la MARCA DE FUNCIÓN: gancho semicircular (contactor), × con tope (disyuntor),
  tope con aro (seccionador). La cuchilla sale del pivote y sube hacia la izquierda (NA) o cruza el tope a la derecha (NC).
- Polos unidos por enlace mecánico punteado; mando manual ⊞; disparadores en cajas por polo: térmico (escalón) e I>.
- Pulsadores: "E" al final del enlace y círculo de función a la izquierda (Ⓘ marcha, Ⓞ paro).
- Números de bornes girados 90°, a la izquierda del conductor. Bornes de campo: círculo pequeño con su letra.
Todos verticales, alimentación arriba. color: SIM_N (documento) o SIM_B (video)."""
from estilo import *

SW_P = 6.0      # potencia
SW_C = 3.2      # mando
H_NUM = 0.11


def num(texto, p, color, dx=-0.1):
    """Número de borne girado 90° (se lee de abajo hacia arriba), a la izquierda del conductor."""
    tt = txt(texto, H_NUM, color, MEDIUM).rotate(PI / 2)
    tt.move_to(np.array(p) + RIGHT * (dx - tt.width / 2 + 0.02))
    return tt


def _marca(func, yf, color, sw):
    g = VGroup()
    if func == "contactor":
        g.add(Arc(radius=0.055, start_angle=0, angle=PI, arc_center=[-0.055, yf, 0]))
    elif func == "disyuntor":
        g.add(Line([-0.065, yf, 0], [0.065, yf, 0]), Line([-0.05, yf + 0.035, 0], [0.05, yf + 0.135, 0]), Line([-0.05, yf + 0.135, 0], [0.05, yf + 0.035, 0]))
    elif func == "seccionador":
        g.add(Line([-0.06, yf, 0], [0.06, yf, 0]), Circle(radius=0.035).move_to([0, yf - 0.045, 0]))
    g.set_stroke(color, sw)
    return g


def contacto(na=True, func=None, n1=None, n2=None, color=SIM_N, sw=SW_C, L=1.2, bajo=None):
    """Contacto simple. Devuelve VGroup con .a (arriba), .z (abajo), .pm (punto medio de la cuchilla para el enlace).
    bajo: largo del conductor por debajo (para colocar disparadores debajo del pivote)."""
    h = L / 2
    yf = 0.14              # fin del contacto fijo
    yp = -0.2              # pivote
    g = VGroup()
    yfix = yf + (0.045 if func == "seccionador" else 0)
    g.add(Line([0, h, 0], [0, yf, 0]))
    hb_ = h if bajo is None else bajo
    g.add(Line([0, yp, 0], [0, -hb_, 0]))
    if na:
        cuch = Line([0, yp, 0], [-0.2, yf + 0.06, 0])
    else:
        g.add(Line([0, yf, 0], [0.11, yf, 0]))
        cuch = Line([0, yp, 0], [0.16, yf + 0.07, 0])
    g.add(cuch)
    g.set_stroke(color, sw)
    if func:
        g.add(_marca(func, yf, color, min(sw * 0.7, SW_C * 0.95)))
    if n1:
        g.add(num(n1, [0, h * 0.62, 0], color))
    if n2:
        g.add(num(n2, [0, -h * 0.62, 0], color))
    g.a, g.z, g.pm, g.cuch = np.array([0, h, 0]), np.array([0, -hb_, 0]), cuch.point_from_proportion(0.5), cuch
    return g


def circulo_funcion(letra, color, sw):
    c = Circle(radius=0.085, stroke_color=color, stroke_width=sw * 0.8)
    return VGroup(c, txt(letra, 0.085, color, MEDIUM).move_to(c))


def mando(tipo, p, color, sw, largo=0.42, funcion=None):
    """Accionamiento unido por enlace punteado a la cuchilla (p = punto medio de la cuchilla)."""
    g = VGroup()
    x_e = p[0] - largo
    g.add(DashedLine(p, [x_e, p[1], 0], dash_length=0.045, dashed_ratio=0.55).set_stroke(color, sw * 0.7))
    a = np.array([x_e, p[1], 0])
    e = 0.085
    if tipo in ("pulsador", "emergencia"):
        g.add(VMobject().set_points_as_corners([a + UP * e + RIGHT * 0.06, a + UP * e, a + DOWN * e, a + DOWN * e + RIGHT * 0.06]).set_stroke(color, sw))
        if tipo == "emergencia":
            g.add(Arc(radius=0.1, start_angle=PI / 2, angle=PI, arc_center=a + LEFT * 0.03).set_stroke(color, sw), Line(a + LEFT * 0.03 + UP * 0.1, a + LEFT * 0.03 + DOWN * 0.1).set_stroke(color, sw))
        elif funcion:
            g.add(circulo_funcion(funcion, color, sw).move_to(a + LEFT * 0.17))
    elif tipo == "giro":
        g.add(VMobject().set_points_as_corners([a + UP * e + RIGHT * 0.06, a + UP * e, a + DOWN * e, a + DOWN * e + LEFT * 0.06]).set_stroke(color, sw))
    elif tipo == "termico":
        g.add(VMobject().set_points_as_corners([a + UP * 0.12, a + UP * 0.12 + LEFT * 0.06, a + UP * 0.04 + LEFT * 0.06, a + UP * 0.04 + LEFT * 0.13,
                                                a + DOWN * 0.04 + LEFT * 0.13, a + DOWN * 0.04 + LEFT * 0.06, a + DOWN * 0.12 + LEFT * 0.06, a + DOWN * 0.12]).set_stroke(color, sw * 1.4))
    elif tipo == "flotador":
        g.add(Line(a, a + DOWN * 0.12).set_stroke(color, sw), Circle(radius=0.055, stroke_color=color, stroke_width=sw).move_to(a + DOWN * 0.18))
    elif tipo == "proximidad":
        g.add(Square(side_length=0.13).rotate(PI / 4).set_stroke(color, sw).move_to(a + LEFT * 0.09))
    return g


def contacto_mando(na, tipo, n1, n2, ref=None, funcion=None, color=SIM_N, sw=SW_C):
    """Contacto de mando con su accionamiento (pulsador, giro, emergencia, flotador, proximidad, térmico)."""
    c = contacto(na, None, n1, n2, color, sw)
    if tipo == "termico":
        # 95-96 / 97-98: rearme manual (E + Ⓞ) a la izquierda y el disparador térmico a la derecha
        g = VGroup(c, mando("pulsador", c.pm, color, sw, 0.5, "O"))
        p = c.pm
        g.add(DashedLine(p, p + RIGHT * 0.3, dash_length=0.045).set_stroke(color, sw * 0.7))
        a = p + RIGHT * 0.3
        g.add(VMobject().set_points_as_corners([a + UP * 0.14 + RIGHT * 0.06, a + UP * 0.14, a + UP * 0.05, a + UP * 0.05 + RIGHT * 0.08, a + DOWN * 0.05 + RIGHT * 0.08,
                                                a + DOWN * 0.05, a + DOWN * 0.14, a + DOWN * 0.14 + RIGHT * 0.06]).set_stroke(color, sw * 1.6))
    else:
        g = VGroup(c, mando(tipo, c.pm, color, sw, 0.42 if tipo != "proximidad" else 0.3, funcion))
    if ref:
        g.add(txt(ref, 0.13, color, MEDIUM).next_to(g, LEFT, buff=0.08))
    g.a, g.z = c.a, c.z
    return g


def polos(n, func, nums, color=SIM_N, sw=SW_P, sep=0.55, enlace=True, bajo=None):
    g = VGroup()
    cs = VGroup()
    for i in range(n):
        n1, n2 = nums[i] if nums else (None, None)
        c = contacto(True, func, n1, n2, color, sw, bajo=bajo).shift(RIGHT * sep * i)
        cs.add(c)
    g.add(cs)
    if enlace and n > 1:
        y = cs[0].pm[1]
        g.add(DashedLine([cs[0].pm[0], y, 0], [cs[-1].pm[0] + 0.02, y, 0], dash_length=0.05, dashed_ratio=0.55).set_stroke(color, SW_C * 0.7))
    g.cs = cs
    return g


def mando_manual(p, color):
    """Mando manual ⊞ (cuadrado con cruz) usado en disyuntores y guardamotores."""
    q = Square(side_length=0.22, stroke_color=color, stroke_width=SW_C * 0.8).move_to(p)
    return VGroup(q, Line(q.get_top(), q.get_bottom()).set_stroke(color, SW_C * 0.8), Line(q.get_left(), q.get_right()).set_stroke(color, SW_C * 0.8))


def interruptor_automatico(n=3, ref="QM1", nums=None, color=SIM_N, sw=SW_P, termico=True, magnetico=True):
    """Guardamotor / disyuntor magnetotérmico (Telesquemario p. 198): contactos con × y tope, mando manual ⊞,
    y por polo una caja con el disparador térmico (escalón) y otra con el magnético (I>), todo enlazado."""
    sep, hb, w = 0.6, 0.3, 0.46
    if nums is None:
        nums = [("1/L1", "2/T1"), ("3/L2", "4/T2"), ("5/L3", "6/T3")] if n == 3 else [(str(2 * i + 1), str(2 * i + 2)) for i in range(n)]
    p = polos(n, "disyuntor", None, color, sw, sep, bajo=0.3)
    g = VGroup(p)
    filas = [f for f, ok in (("t", termico), ("m", magnetico)) if ok]
    y0 = -0.3
    centros = []
    for j, f in enumerate(filas):
        cy = y0 - hb / 2 - j * hb
        centros.append(cy)
        for i in range(n):
            x = sep * i
            g.add(Rectangle(width=w, height=hb, stroke_color=color, stroke_width=SW_C * 0.8).move_to([x + w / 2 - 0.1, cy, 0]))
            if f == "t":
                g.add(VMobject().set_points_as_corners([[x, cy + hb / 2, 0], [x, cy + 0.075, 0], [x + 0.13, cy + 0.075, 0], [x + 0.13, cy - 0.075, 0], [x, cy - 0.075, 0], [x, cy - hb / 2, 0]]).set_stroke(color, sw))
            else:
                g.add(Line([x, cy + hb / 2, 0], [x, cy - hb / 2, 0]).set_stroke(color, sw),
                      VGroup(txt("I", 0.14, color, MEDIUM), txt(">", 0.14, color, MEDIUM)).arrange(RIGHT, buff=0.02).move_to([x + 0.2, cy, 0]))
    y_fin = y0 - hb * len(filas) - 0.4
    for i in range(n):
        g.add(Line([sep * i, y0 - hb * len(filas), 0], [sep * i, y_fin, 0]).set_stroke(color, sw))
    q = mando_manual([-0.62, p.cs[0].pm[1], 0], color)
    g.add(q, DashedLine(q.get_right(), p.cs[0].pm, dash_length=0.045).set_stroke(color, SW_C * 0.7))
    g.add(DashedLine(q.get_bottom(), [q.get_center()[0], centros[-1], 0], dash_length=0.045).set_stroke(color, SW_C * 0.7))
    for cy in centros:
        g.add(DashedLine([q.get_center()[0], cy, 0], [-0.1, cy, 0], dash_length=0.045).set_stroke(color, SW_C * 0.7))
    for i, (a_, z_) in enumerate(nums):
        g.add(num(a_, [sep * i, p.cs[i].a[1] - 0.17, 0], color), num(z_, [sep * i, y_fin + 0.2, 0], color))
    g.add(txt(f"– {ref}", 0.13, color, MEDIUM).next_to(q, LEFT, buff=0.08))
    g.a = [c.a for c in p.cs]
    g.z = [np.array([sep * i, y_fin, 0]) for i in range(n)]
    return g


def contactor_potencia(ref="KM1", color=SIM_N, sw=SW_P):
    p = polos(3, "contactor", [("1", "2"), ("3", "4"), ("5", "6")], color, sw)
    p.add(txt(f"– {ref}", 0.13, color, MEDIUM).next_to(p, LEFT, buff=0.1).match_y(DashedLine(p.cs[0].pm, p.cs[0].pm + RIGHT)))
    p.a = [c.a for c in p.cs]
    p.z = [c.z for c in p.cs]
    return p


def termico_potencia(ref="F2", color=SIM_N, sw=SW_P, sep=0.55, L=1.2):
    """Relé térmico (elementos bimetálicos): escalón en cada polo y recuadro punteado común."""
    g = VGroup()
    for i in range(3):
        x = sep * i
        g.add(VMobject().set_points_as_corners([[x, L / 2, 0], [x, 0.12, 0], [x + 0.16, 0.12, 0], [x + 0.16, -0.12, 0], [x, -0.12, 0], [x, -L / 2, 0]]).set_stroke(color, sw))
        g.add(num(str(2 * i + 1), [x, 0.3, 0], color), num(str(2 * i + 2), [x, -0.3, 0], color))
    caja = DashedVMobject(Rectangle(width=sep * 2 + 0.5, height=0.42, stroke_color=color, stroke_width=SW_C * 0.6), num_dashes=40).move_to([sep + 0.06, 0, 0])
    g.add(caja, txt(f"– {ref}", 0.13, color, MEDIUM).next_to(caja, LEFT, buff=0.1))
    g.a = [np.array([sep * i, L / 2, 0]) for i in range(3)]
    g.z = [np.array([sep * i, -L / 2, 0]) for i in range(3)]
    return g


def bobina(ref="KM1", n1="A1", n2="A2", tipo=None, color=SIM_N, sw=SW_C, L=1.2):
    r = Rectangle(width=0.42, height=0.2, stroke_color=color, stroke_width=sw)
    g = VGroup(Line([0, L / 2, 0], [0, 0.1, 0]), r, Line([0, -0.1, 0], [0, -L / 2, 0])).set_stroke(color, sw)
    if tipo == "retardo":
        g.add(Rectangle(width=0.14, height=0.2, stroke_color=color, stroke_width=sw).set_fill(color, 1).align_to(r, LEFT))
    g.add(num(n1, [0, 0.3, 0], color), num(n2, [0, -0.3, 0], color), txt(f"– {ref}", 0.13, color, MEDIUM).next_to(r, LEFT, buff=0.1))
    g.a, g.z = np.array([0, L / 2, 0]), np.array([0, -L / 2, 0])
    return g


def lampara(ref="H1", color=SIM_N, sw=SW_C, L=1.2, relleno=None):
    c = Circle(radius=0.12, stroke_color=color, stroke_width=sw)
    x = VGroup(Line(c.point_at_angle(PI / 4), c.point_at_angle(PI * 5 / 4)), Line(c.point_at_angle(PI * 3 / 4), c.point_at_angle(-PI / 4))).set_stroke(color, sw)
    g = VGroup(Line([0, L / 2, 0], [0, 0.12, 0]).set_stroke(color, sw), c, x, Line([0, -0.12, 0], [0, -L / 2, 0]).set_stroke(color, sw))
    if relleno:
        g.add_to_back(c.copy().set_fill(relleno, 0.55).set_stroke(width=0))
    g.add(num("X1", [0, 0.3, 0], color), num("X2", [0, -0.3, 0], color), txt(f"– {ref}", 0.13, color, MEDIUM).next_to(c, LEFT, buff=0.32))
    g.a, g.z = np.array([0, L / 2, 0]), np.array([0, -L / 2, 0])
    return g


def conmutado(c, na_, nc_, retardo=False, color=SIM_N, sw=SW_C, L=1.2):
    """Contacto conmutado: común abajo; NC (tope) a la izquierda, NA a la derecha."""
    h = L / 2
    g = VGroup(Line([0, -h, 0], [0, -0.2, 0]),
               VMobject().set_points_as_corners([[-0.2, h, 0], [-0.2, 0.14, 0], [-0.1, 0.14, 0]]),
               VMobject().set_points_as_corners([[0.2, h, 0], [0.2, 0.14, 0]]),
               Line([0, -0.2, 0], [-0.13, 0.2, 0])).set_stroke(color, sw)
    if retardo:
        p = g[3].point_from_proportion(0.5)
        g.add(DashedLine(p, p + LEFT * 0.3, dash_length=0.045).set_stroke(color, sw * 0.7),
              Arc(radius=0.09, start_angle=PI / 2, angle=PI, arc_center=p + LEFT * 0.39).set_stroke(color, sw))
    g.add(num(c, [0, -0.38, 0], color), num(nc_, [-0.2, 0.38, 0], color), num(na_, [0.2, 0.38, 0], color, dx=0.24))
    return g


def borne_campo(letra, color=SIM_N, sw=SW_C):
    c = Circle(radius=0.045, stroke_color=color, stroke_width=sw * 0.8).set_fill(WHITE if color == SIM_N else BLACK, 1)
    return VGroup(c, txt(letra, 0.11, color, MEDIUM).rotate(PI / 2).next_to(c, LEFT, buff=0.06))


def motor(ref="M1", trifasico=True, color=SIM_N, sw=SW_P, terminales=("U", "V", "W")):
    c = Circle(radius=0.42, stroke_color=color, stroke_width=SW_C)
    g = VGroup(c, txt(ref, 0.12, color, MEDIUM).move_to(c.get_center() + UP * 0.1), VGroup(txt("3" if trifasico else "1", 0.12, color, MEDIUM), txt("∿", 0.16, color, MEDIUM)).arrange(RIGHT, buff=0.03).move_to(c.get_center() + DOWN * 0.1))
    xs = (-0.3, 0, 0.3) if trifasico else (-0.2, 0.2)
    tops = []
    for x, tl in zip(xs, terminales):
        y0 = np.sqrt(0.42 ** 2 - (x * 0.9) ** 2)
        x_c = x * 0.75
        g.add(VMobject().set_points_as_corners([[x, 0.95, 0], [x, 0.62, 0], [x_c, y0 * 0.98, 0]]).set_stroke(color, sw))
        bc = borne_campo(tl, color).move_to([x, 0.75, 0], aligned_edge=ORIGIN)
        bc[0].move_to([x, 0.75, 0])
        bc[1].next_to(bc[0], LEFT, buff=0.06)
        g.add(bc)
        tops.append(np.array([x, 0.95, 0]))
    g.a = tops
    return g


def sensor(tipo="inductivo", ref="B1", color=SIM_N, sw=SW_C):
    """Detector de proximidad de 3 hilos PNP NA (Telesquemario: detector con rombo + contacto)."""
    r = Rectangle(width=0.62, height=0.5, stroke_color=color, stroke_width=sw)
    rombo = Square(side_length=0.14).rotate(PI / 4).set_stroke(color, sw * 0.8).move_to(r.get_center() + LEFT * 0.15)
    signo = {"inductivo": txt("Fe", 0.06, color, MEDIUM), "capacitivo": VGroup(Line(UP * 0.04, DOWN * 0.04), Line(UP * 0.04, DOWN * 0.04).shift(RIGHT * 0.025)).set_stroke(color, sw * 0.6),
             "optico": VGroup(*[Line(LEFT * 0.04, RIGHT * 0.04).shift(UP * d) for d in (0.02, -0.02)]).set_stroke(color, sw * 0.6)}[tipo].move_to(rombo)
    k = contacto(True, None, None, None, color, sw * 0.8, 0.4).move_to(r.get_center() + RIGHT * 0.15)
    g = VGroup(r, rombo, signo, k)
    for x, y, lab, d in ((-0.2, 0.25, "BN", UP), (0.0, -0.25, "BK", DOWN), (0.2, -0.25, "BU", DOWN)):
        p0 = r.get_center() + np.array([x, y, 0])
        g.add(Line(p0, p0 + d * 0.3).set_stroke(color, sw), txt(lab, 0.09, color, MEDIUM).next_to(p0 + d * 0.3, d, buff=0.03))
    g.add(txt(f"– {ref}", 0.13, color, MEDIUM).next_to(r, LEFT, buff=0.1))
    return g


def fuente(ref="T1", color=SIM_N, sw=SW_C, ent=("L", "N"), sal=("+", "−")):
    r = Square(side_length=0.6, stroke_color=color, stroke_width=sw)
    g = VGroup(r, Line(r.get_corner(DL), r.get_corner(UR)).set_stroke(color, sw * 0.7), txt("~", 0.13, color, MEDIUM).move_to(r.get_center() + UL * 0.15), txt("=", 0.13, color, MEDIUM).move_to(r.get_center() + DR * 0.15))
    for i, n in enumerate(ent):
        x = -0.15 + 0.3 * i
        g.add(Line([x, 0.3, 0], [x, 0.55, 0]).set_stroke(color, sw), num(n, [x, 0.45, 0], color))
    for i, n in enumerate(sal):
        x = -0.15 + 0.3 * i
        g.add(Line([x, -0.3, 0], [x, -0.55, 0]).set_stroke(color, sw), num(n, [x, -0.45, 0], color))
    g.add(txt(f"– {ref}", 0.13, color, MEDIUM).next_to(r, LEFT, buff=0.15))
    return g


def plc(entradas, salidas, ref="A1", titulo="PLC", color=SIM_N, sw=SW_C):
    w = max(len(entradas), len(salidas)) * 0.26 + 0.3
    r = Rectangle(width=w, height=0.6, stroke_color=color, stroke_width=sw)
    g = VGroup(r, txt(titulo, 0.11, color, BOLD).move_to(r))
    for i, n in enumerate(entradas):
        x = r.get_left()[0] + 0.22 + 0.26 * i
        g.add(Line([x, 0.3, 0], [x, 0.55, 0]).set_stroke(color, sw), num(n, [x, 0.42, 0], color, dx=-0.06))
    for i, n in enumerate(salidas):
        x = r.get_left()[0] + 0.22 + 0.26 * i
        g.add(Line([x, -0.3, 0], [x, -0.55, 0]).set_stroke(color, sw), num(n, [x, -0.42, 0], color, dx=-0.06))
    g.add(txt(f"– {ref}", 0.13, color, MEDIUM).next_to(r, LEFT, buff=0.15))
    return g


def bornera(nombres, ref="X1", color=SIM_N, sw=SW_C):
    g = VGroup()
    for i, n in enumerate(nombres):
        x = 0.28 * i
        g.add(Line([x, 0.25, 0], [x, -0.25, 0]).set_stroke(color, sw), borne_campo("", color).move_to([x, 0, 0]), txt(n, 0.09, color, MEDIUM).next_to([x, -0.25, 0], DOWN, buff=0.04))
    g.add(txt(f"– {ref}", 0.13, color, MEDIUM).next_to(g, LEFT, buff=0.12))
    return g

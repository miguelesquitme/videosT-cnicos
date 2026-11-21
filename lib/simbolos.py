"""Símbolos IEC 60617 (según el Manual electrotécnico Telesquemario, cap. 6) en un trazo único.
Todos verticales, de arriba (alimentación) hacia abajo. Cada símbolo expone .a (borne superior) y .z (borne inferior).
color: SIM_N (documento, fondo claro) o SIM_B (video, fondo negro)."""
from estilo import *

SW = 4.0          # grosor de línea de los símbolos
L = 1.0           # largo de un contacto


def _num(t, p, color, lado=RIGHT, h=0.13):
    return txt(t, h, color, BOLD).next_to(p, lado, buff=0.07)


def contacto(na=True, func=None, mando=None, n1=None, n2=None, ref=None, color=SIM_N, sw=SW, largo=L, conmutado=False):
    """Contacto vertical. na=True NA (abierto en reposo) / False NC.
    func: None | 'contactor' (semicírculo) | 'disyuntor' (cruz) | 'seccionador' (barra) | 'retardo' (paracaídas, temporizado al trabajo).
    mando: None | 'pulsador' | 'giro' | 'emergencia' | 'termico' | 'flotador' | 'proximidad' | 'manual'."""
    h = largo / 2
    yf = 0.18 * largo           # contacto fijo
    ym = -0.18 * largo          # pivote
    g = VGroup()
    sup = Line([0, h, 0], [0, yf, 0])
    inf = Line([0, ym, 0], [0, -h, 0])
    g.add(sup, inf)
    if na:
        cuch = Line([0, ym, 0], [-0.22 * largo, yf + 0.06 * largo, 0])
    else:
        g.add(Line([0, yf, 0], [0.16 * largo, yf, 0]))
        cuch = Line([0, ym, 0], [0.19 * largo, yf + 0.05 * largo, 0])
    g.add(cuch)
    if func == "contactor":
        g.add(Arc(radius=0.075 * largo, start_angle=PI, angle=PI, arc_center=[0, yf + 0.075 * largo, 0]).set_stroke(color, sw * 0.7))
    elif func == "disyuntor":
        d = 0.06 * largo
        g.add(Line([-d, yf - d, 0], [d, yf + d, 0]), Line([-d, yf + d, 0], [d, yf - d, 0]))
    elif func == "seccionador":
        g.add(Line([-0.07 * largo, yf, 0], [0.07 * largo, yf, 0]))
    p_m = cuch.point_from_proportion(0.55)
    if mando:
        xm = -0.52 * largo
        g.add(DashedLine(p_m, [xm, p_m[1], 0], dash_length=0.05).set_stroke(color, sw * 0.6))
        a = np.array([xm, p_m[1], 0])
        e = 0.09 * largo
        if mando == "pulsador":
            g.add(VMobject().set_points_as_corners([a + UP * e + RIGHT * 0.06, a + UP * e, a + DOWN * e, a + DOWN * e + RIGHT * 0.06]))
        elif mando == "giro":
            g.add(VMobject().set_points_as_corners([a + UP * e + RIGHT * 0.06, a + UP * e, a + DOWN * e, a + DOWN * e + LEFT * 0.06]))
        elif mando == "manual":
            g.add(Line(a + UP * e, a + DOWN * e))
        elif mando == "emergencia":
            g.add(Arc(radius=e * 1.2, start_angle=PI / 2, angle=PI, arc_center=a).set_fill(color, 1), Line(a + UP * e * 1.2, a + DOWN * e * 1.2))
        elif mando == "termico":
            g.add(VMobject().set_points_as_corners([a, a + LEFT * 0.08, a + LEFT * 0.08 + DOWN * 0.08, a + LEFT * 0.16 + DOWN * 0.08, a + LEFT * 0.16]))
        elif mando == "flotador":
            g.add(Line(a, a + DOWN * 0.14), Circle(radius=0.06, stroke_color=color, stroke_width=sw).move_to(a + DOWN * 0.2))
        elif mando == "proximidad":
            g.add(Square(side_length=0.16).rotate(PI / 4).move_to(a + LEFT * 0.11))
    if func == "retardo":
        # paracaídas: arco en la línea del accionamiento (temporizado a la conexión)
        c = p_m + LEFT * 0.2 * largo
        g.add(DashedLine(p_m, c + LEFT * 0.12, dash_length=0.05).set_stroke(color, sw * 0.6),
              Arc(radius=0.1 * largo, start_angle=-PI / 2, angle=PI, arc_center=c + LEFT * 0.06).rotate(PI, about_point=c + LEFT * 0.06))
    g.set_stroke(color, sw)
    if n1:
        g.add(_num(n1, [0.0, h * 0.72, 0], color))
    if n2:
        g.add(_num(n2, [0.0, -h * 0.72, 0], color))
    if ref:
        g.add(txt(ref, 0.17, color, BOLD).next_to(g, LEFT, buff=0.12))
    g.a, g.z, g.cuch = np.array([0, h, 0]), np.array([0, -h, 0]), cuch
    return g


def conmutado(n_c, n_na, n_nc, func=None, color=SIM_N, sw=SW, ref=None):
    """Contacto conmutado (común abajo, NC a la izquierda arriba, NA a la derecha arriba)."""
    g = VGroup()
    c = Line([0, -0.5, 0], [0, -0.18, 0])
    nc = VMobject().set_points_as_corners([[-0.25, 0.5, 0], [-0.25, 0.18, 0], [-0.05, 0.18, 0]])
    na = VMobject().set_points_as_corners([[0.25, 0.5, 0], [0.25, 0.18, 0], [0.13, 0.18, 0]])
    cuch = Line([0, -0.18, 0], [-0.07, 0.2, 0])
    g.add(c, nc, na, cuch)
    if func == "retardo":
        p = cuch.get_center()
        g.add(DashedLine(p, p + LEFT * 0.35, dash_length=0.05).set_stroke(color, sw * 0.6),
              Arc(radius=0.1, start_angle=PI / 2, angle=PI, arc_center=p + LEFT * 0.42))
    g.set_stroke(color, sw)
    g.add(_num(n_c, [0, -0.4, 0], color), _num(n_nc, [-0.25, 0.42, 0], color, LEFT), _num(n_na, [0.25, 0.42, 0], color))
    if ref:
        g.add(txt(ref, 0.17, color, BOLD).next_to(g, LEFT, buff=0.15))
    g.a_nc, g.a_na, g.z = np.array([-0.25, 0.5, 0]), np.array([0.25, 0.5, 0]), np.array([0, -0.5, 0])
    return g


def bobina(n1="A1", n2="A2", ref=None, tipo=None, color=SIM_N, sw=SW):
    """Bobina de mando: rectángulo. tipo='retardo' (relé temporizado al trabajo: rectángulo con zona rayada)."""
    r = Rectangle(width=0.5, height=0.26, stroke_color=color, stroke_width=sw)
    g = VGroup(Line([0, 0.5, 0], [0, 0.13, 0]), r, Line([0, -0.13, 0], [0, -0.5, 0])).set_stroke(color, sw)
    if tipo == "retardo":
        z = Rectangle(width=0.16, height=0.26, stroke_color=color, stroke_width=sw).align_to(r, LEFT)
        ray = VGroup(*[Line(z.get_corner(DL) + RIGHT * 0.04 * i, z.get_corner(DL) + RIGHT * 0.04 * i + UP * 0.26 + RIGHT * 0.0).set_stroke(color, sw * 0.5) for i in range(1, 4)])
        g.add(z, ray)
    g.add(_num(n1, [0, 0.36, 0], color), _num(n2, [0, -0.36, 0], color))
    if ref:
        g.add(txt(ref, 0.17, color, BOLD).next_to(r, LEFT, buff=0.15))
    g.a, g.z = np.array([0, 0.5, 0]), np.array([0, -0.5, 0])
    return g


def lampara(ref="H1", color=SIM_N, sw=SW, col_lampara=None):
    c = Circle(radius=0.17, stroke_color=color, stroke_width=sw)
    x = VGroup(Line(c.point_at_angle(PI / 4), c.point_at_angle(PI * 5 / 4)), Line(c.point_at_angle(PI * 3 / 4), c.point_at_angle(-PI / 4)))
    g = VGroup(Line([0, 0.5, 0], [0, 0.17, 0]), c, x, Line([0, -0.17, 0], [0, -0.5, 0])).set_stroke(color, sw)
    if col_lampara:
        g.add(c.copy().set_fill(col_lampara, 0.6).set_stroke(width=0))
    g.add(_num("X1", [0, 0.36, 0], color), _num("X2", [0, -0.36, 0], color), txt(ref, 0.17, color, BOLD).next_to(c, LEFT, buff=0.15))
    g.a, g.z = np.array([0, 0.5, 0]), np.array([0, -0.5, 0])
    return g


def _tripolar(n, constructor, sep=0.5, color=SIM_N, sw=SW, enlace=True, **kw):
    g = VGroup()
    polos = VGroup()
    for i in range(n):
        c = constructor(i)
        c.shift(RIGHT * sep * i)
        polos.add(c)
    g.add(polos)
    if enlace and n > 1:
        y = polos[0].cuch.point_from_proportion(0.55)[1]
        g.add(DashedLine([polos[0].cuch.point_from_proportion(0.55)[0], y, 0], [polos[-1].cuch.point_from_proportion(0.55)[0], y, 0], dash_length=0.05).set_stroke(color, sw * 0.6))
    g.polos = polos
    return g


def disyuntor_sim(polos=1, ref="F1", color=SIM_N, sw=SW, num=True):
    """Interruptor automático magnetotérmico: contacto con cruz + disparo térmico y magnético (I>) enlazados,
    como en el Telesquemario (accionamiento unido en 2P y 3P)."""
    g = _tripolar(polos, lambda i: contacto(True, "disyuntor", None, str(2 * i + 1) if num else None, str(2 * i + 2) if num else None, color=color, sw=sw), color=color, sw=sw)
    p0 = g.polos[0].cuch.point_from_proportion(0.55)
    xb = p0[0] - 0.55
    term = VMobject().set_points_as_corners([[xb + 0.18, p0[1] + 0.12, 0], [xb + 0.08, p0[1] + 0.12, 0], [xb + 0.08, p0[1] + 0.02, 0], [xb - 0.02, p0[1] + 0.02, 0]]).set_stroke(color, sw * 0.8)
    mag = VGroup(Rectangle(width=0.26, height=0.2, stroke_color=color, stroke_width=sw * 0.8), txt("I>", 0.1, color, BOLD)).move_to([xb + 0.05, p0[1] - 0.2, 0])
    g.add(DashedLine(p0, [xb + 0.18, p0[1], 0], dash_length=0.05).set_stroke(color, sw * 0.6), term, mag)
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(g, LEFT, buff=0.1))
    return g


def guardamotor_sim(ref="QM1", color=SIM_N, sw=SW):
    """Guardamotor (disyuntor-protector de motor): 3 contactos con cruz, disparo térmico (sobrecarga, regulable)
    y magnético (I>) por polo, mando manual giratorio."""
    g = _tripolar(3, lambda i: contacto(True, "disyuntor", None, f"{2 * i + 1}", f"{2 * i + 2}", color=color, sw=sw), color=color, sw=sw)
    p0 = g.polos[0].cuch.point_from_proportion(0.55)
    xb = p0[0] - 0.75
    caja_t = VGroup(Rectangle(width=0.3, height=0.24, stroke_color=color, stroke_width=sw * 0.8),
                    VMobject().set_points_as_corners([[-0.08, 0.05, 0], [0, 0.05, 0], [0, -0.05, 0], [0.08, -0.05, 0]]).set_stroke(color, sw * 0.8)).move_to([xb, p0[1] + 0.18, 0])
    caja_m = VGroup(Rectangle(width=0.3, height=0.24, stroke_color=color, stroke_width=sw * 0.8), txt("I>", 0.1, color, BOLD)).move_to([xb, p0[1] - 0.18, 0])
    giro = VMobject().set_points_as_corners([[xb - 0.26, p0[1] + 0.09, 0], [xb - 0.32, p0[1] + 0.09, 0], [xb - 0.32, p0[1] - 0.09, 0], [xb - 0.38, p0[1] - 0.09, 0]]).set_stroke(color, sw * 0.8)
    g.add(DashedLine(p0, [xb + 0.15, p0[1], 0], dash_length=0.05).set_stroke(color, sw * 0.6),
          Line([xb + 0.15, p0[1] + 0.18, 0], [xb + 0.15, p0[1] - 0.18, 0]).set_stroke(color, sw * 0.6), caja_t, caja_m,
          DashedLine([xb - 0.15, p0[1], 0], [xb - 0.26, p0[1], 0], dash_length=0.04).set_stroke(color, sw * 0.6), giro)
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(g, LEFT, buff=0.1))
    return g


def contactor_pot_sim(ref="KM1", color=SIM_N, sw=SW):
    g = _tripolar(3, lambda i: contacto(True, "contactor", None, f"{2 * i + 1}", f"{2 * i + 2}", color=color, sw=sw), color=color, sw=sw)
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(g, LEFT, buff=0.15))
    return g


def termico_pot_sim(ref="F2", color=SIM_N, sw=SW):
    """Elementos térmicos de potencia (rectángulo con lámina bimetálica), bornes 1-2 3-4 5-6."""
    g = VGroup()
    for i in range(3):
        x = 0.5 * i
        r = Rectangle(width=0.26, height=0.36, stroke_color=color, stroke_width=sw).move_to([x, 0, 0])
        bi = VMobject().set_points_as_corners([[x, 0.5, 0], [x, 0.08, 0], [x - 0.07, 0.08, 0], [x - 0.07, -0.08, 0], [x, -0.08, 0], [x, -0.5, 0]]).set_stroke(color, sw)
        g.add(r, bi, _num(str(2 * i + 1), [x, 0.4, 0], color), _num(str(2 * i + 2), [x, -0.4, 0], color))
    g.add(DashedLine([-0.13, 0, 0], [-0.4, 0, 0], dash_length=0.05).set_stroke(color, sw * 0.6))
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(g, LEFT, buff=0.1))
    return g


def motor_sim(trifasico=True, ref="M1", color=SIM_N, sw=SW, pe=True):
    c = Circle(radius=0.48, stroke_color=color, stroke_width=sw)
    g = VGroup(c, txt("M", 0.24, color, BOLD).move_to(c.get_center() + UP * 0.08), txt("3~" if trifasico else "1~", 0.15, color, BOLD).move_to(c.get_center() + DOWN * 0.2))
    nombres = ("U1", "V1", "W1") if trifasico else ("U1", "U2")
    xs = (-0.3, 0, 0.3) if trifasico else (-0.2, 0.2)
    for x, n in zip(xs, nombres):
        y0 = np.sqrt(max(0.48 ** 2 - x ** 2, 0))
        g.add(Line([x, y0, 0], [x, 0.85, 0]).set_stroke(color, sw), _num(n, [x, 0.7, 0], color, h=0.11))
    if pe:
        g.add(Line(c.get_right(), c.get_right() + RIGHT * 0.3).set_stroke(color, sw), txt("PE", 0.12, color, BOLD).next_to(c.get_right() + RIGHT * 0.3, UP, buff=0.05))
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(c, LEFT, buff=0.15))
    return g


def sensor_sim(tipo="inductivo", ref="B1", color=SIM_N, sw=SW):
    """Detector de proximidad de 3 hilos PNP NA: caja con rombo (proximidad) y signo del principio,
    bornes BN (+), BK (salida), BU (−)."""
    r = Rectangle(width=0.9, height=0.7, stroke_color=color, stroke_width=sw)
    rombo = Square(side_length=0.22).rotate(PI / 4).set_stroke(color, sw * 0.8).move_to(r.get_center() + LEFT * 0.22)
    signo = {"inductivo": txt("Fe", 0.1, color, BOLD), "capacitivo": VGroup(Line(UP * 0.08, DOWN * 0.08), Line(UP * 0.08, DOWN * 0.08).shift(RIGHT * 0.05)).set_stroke(color, sw * 0.7),
             "optico": VGroup(*[Arrow(LEFT * 0.12 + UP * d, RIGHT * 0.12 + UP * d, buff=0, stroke_width=3, tip_length=0.07, max_tip_length_to_length_ratio=0.5, color=color) for d in (0.05, -0.05)]).rotate(-PI / 6)}[tipo]
    signo.move_to(rombo)
    na = contacto(True, None, None, color=color, sw=sw * 0.8, largo=0.5).move_to(r.get_center() + RIGHT * 0.2)
    g = VGroup(r, rombo, signo, na)
    for x, n in ((-0.3, "BN +"), (0.0, "BK"), (0.3, "BU −")):
        y = -0.35 if n != "BN +" else 0.35
    g.add(Line(r.get_top() + LEFT * 0.3, r.get_top() + LEFT * 0.3 + UP * 0.3).set_stroke(color, sw), txt("BN (+)", 0.1, color, BOLD).next_to(r.get_top() + LEFT * 0.3 + UP * 0.3, UP, buff=0.04),
          Line(r.get_bottom() + LEFT * 0.2, r.get_bottom() + LEFT * 0.2 + DOWN * 0.3).set_stroke(color, sw), txt("BK", 0.1, color, BOLD).next_to(r.get_bottom() + LEFT * 0.2 + DOWN * 0.3, DOWN, buff=0.04),
          Line(r.get_bottom() + RIGHT * 0.25, r.get_bottom() + RIGHT * 0.25 + DOWN * 0.3).set_stroke(color, sw), txt("BU (−)", 0.1, color, BOLD).next_to(r.get_bottom() + RIGHT * 0.25 + DOWN * 0.3, DOWN, buff=0.04))
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(r, LEFT, buff=0.15))
    return g


def borne_sim(n, ref="X1", color=SIM_N, sw=SW):
    c = Circle(radius=0.07, stroke_color=color, stroke_width=sw * 0.8)
    return VGroup(c, txt(f"{ref}:{n}", 0.1, color, BOLD).next_to(c, RIGHT, buff=0.06))


def bornera_sim(nombres, ref="X1", color=SIM_N, sw=SW):
    g = VGroup()
    for i, n in enumerate(nombres):
        cel = Rectangle(width=0.32, height=0.32, stroke_color=color, stroke_width=sw * 0.7).move_to([0.32 * i, 0, 0])
        g.add(cel, Circle(radius=0.06, stroke_color=color, stroke_width=sw * 0.6).move_to(cel), txt(n, 0.09, color, BOLD).next_to(cel, DOWN, buff=0.04))
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(g, LEFT, buff=0.15))
    return g


def fuente_sim(ref="T1", color=SIM_N, sw=SW, entrada="L N", salida="+ −"):
    r = Square(side_length=0.8, stroke_color=color, stroke_width=sw)
    d = Line(r.get_corner(DL), r.get_corner(UR)).set_stroke(color, sw * 0.7)
    g = VGroup(r, d, txt("~", 0.16, color, BOLD).move_to(r.get_center() + UL * 0.2), txt("=", 0.16, color, BOLD).move_to(r.get_center() + DR * 0.2))
    g.add(txt(entrada, 0.1, color, BOLD).next_to(r, UP, buff=0.05), txt(salida, 0.1, color, BOLD).next_to(r, DOWN, buff=0.05),
          txt(f"-{ref}", 0.17, color, BOLD).next_to(r, LEFT, buff=0.15))
    return g


def plc_sim(entradas, salidas, ref="A1", titulo="PLC", color=SIM_N, sw=SW):
    """Representación del PLC en el esquema: caja con bornes de entrada arriba y de salida abajo."""
    w = max(len(entradas), len(salidas)) * 0.36 + 0.4
    r = Rectangle(width=w, height=0.8, stroke_color=color, stroke_width=sw)
    g = VGroup(r, txt(titulo, 0.13, color, BOLD).move_to(r))
    for i, n in enumerate(entradas):
        x = r.get_left()[0] + 0.3 + 0.36 * i
        g.add(Line([x, r.get_top()[1], 0], [x, r.get_top()[1] + 0.25, 0]).set_stroke(color, sw * 0.8), txt(n, 0.08, color, BOLD).move_to([x, r.get_top()[1] - 0.12, 0]))
    for i, n in enumerate(salidas):
        x = r.get_left()[0] + 0.3 + 0.36 * i
        g.add(Line([x, r.get_bottom()[1], 0], [x, r.get_bottom()[1] - 0.25, 0]).set_stroke(color, sw * 0.8), txt(n, 0.08, color, BOLD).move_to([x, r.get_bottom()[1] + 0.12, 0]))
    g.add(txt(f"-{ref}", 0.17, color, BOLD).next_to(r, LEFT, buff=0.15))
    return g

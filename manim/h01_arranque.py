"""H01 · Arranque directo de un motor trifásico · Trituradora de piedrín (horizontal).
Guion: h01_guion.py · Equipos: biblioteca svgref (PNG en h01_eq/, bornes en mm en los JSON).
Render: FORMATO=h TEMA=negro VOZ=eleven manim -qh --disable_caching -o h01 h01_arranque.py H01
Previa por secciones: SOLO=mando FORMATO=h TEMA=negro PREVIEW=1 manim -ql ...
"""
import json
from e06b_contactor import *
from h01_guion import GUION as GH, SECCIONES as SH
from comun_e import cable

EQ = DIR / "h01_eq"
LOGO = DIR.parent / "marca" / "logo_oficial.png"
ROJO_M = "#E5484D"        # mando AC
PE_V, PE_A = "#16A34A", "#F2D21B"
C_Q, C_KM, C_F2, C_S, C_F1, C_X = "#F79009", "#22B8CF", "#9E77ED", "#4C8DF6", "#12B76A", "#98A2B3"
LT = "#E4E7EC"            # líneas del diagrama sobre negro


# =========================================================================== equipos de la biblioteca
class Eq(Group):
    """PNG de la biblioteca con sus bornes. k = unidades de escena por mm."""

    def __init__(self, nombre, k):
        d = json.loads((EQ / f"{nombre}.json").read_text())
        img = ImageMobject(str(EQ / f"{nombre}.png"))
        img.height = (d["H"] + 2 * d["margen"]) * k
        super().__init__(img)
        self.img, self.d, self.k, self.nombre = img, d, k, nombre

    def p(self, b):
        x, y = self.d["bornes"][b]
        m = self.d["margen"]
        return self.img.get_corner(UL) + RIGHT * (m + x) * self.k + DOWN * (m + y) * self.k

    def cuerpo(self, lado):
        """Borde del cuerpo sin el margen de sombra: lado = UP/DOWN/LEFT/RIGHT."""
        m = self.d["margen"] * self.k
        c = self.img.get_center()
        if np.allclose(lado, UP):
            return c + UP * (self.img.height / 2 - m)
        if np.allclose(lado, DOWN):
            return c + DOWN * (self.img.height / 2 - m)
        if np.allclose(lado, LEFT):
            return c + LEFT * (self.img.width / 2 - m)
        return c + RIGHT * (self.img.width / 2 - m)

    def poner(self, arriba_izq):
        """Ubica la esquina superior izquierda del CUERPO en el punto dado."""
        m = self.d["margen"] * self.k
        self.img.move_to(np.array(arriba_izq) + RIGHT * (self.img.width / 2 - m) + DOWN * (self.img.height / 2 - m))
        return self


def hilo(pts, color=ROJO_M, w=4.0, num=None, k=1.0):
    """Conductor con puntera en cada punta y marcador con el número de hilo junto a cada puntera."""
    pts = [np.array(p, float) for p in pts]
    if color == "PE":
        base = cable(*pts, color=PE_V, w=w)
        rayas = DashedVMobject(VMobject().set_points_as_corners(pts), num_dashes=max(6, int(sum(np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])) / 0.12)))
        rayas.set_stroke(PE_A, w * 0.6)
        fisico(rayas)
        g = VGroup(base, rayas)
        g.ruta = base.ruta
    else:
        g = cable(*pts, color=color, w=w)
    extras = VGroup()
    for extremo, sig in ((pts[0], pts[1]), (pts[-1], pts[-2])):
        d = sig - extremo
        d = d / (np.linalg.norm(d) + 1e-9)
        pt = Rectangle(width=0.05 * k, height=0.13 * k, stroke_width=0).set_fill("#9AA4B2", 1)
        if abs(d[0]) > abs(d[1]):
            pt.rotate(PI / 2)
        pt.move_to(extremo + d * 0.06 * k)
        extras.add(pt)
        if num is not None:
            t = Text(str(num), font=SANS, font_size=14, weight="BOLD", color="#111111").scale(k)
            caja = Rectangle(width=t.width + 0.05 * k, height=t.height + 0.04 * k, stroke_width=0).set_fill(WHITE, 1)
            mk = VGroup(caja, t.move_to(caja)).move_to(extremo + d * 0.24 * k)
            extras.add(mk)
    return VGroup(g, extras)


def ortho(a, b, *, y=None, x=None):
    a, b = np.array(a, float), np.array(b, float)
    if y is not None:
        return [a, [a[0], y, 0], [b[0], y, 0], b]
    if x is not None:
        return [a, [x, a[1], 0], [x, b[1], 0], b]
    return [a, [a[0], b[1], 0], b]


# =========================================================================== símbolos del diagrama (estilo de la referencia)
def num_borne(p, s, lado=RIGHT, size=18):
    return Text(s, font=SANS, font_size=size, weight="BOLD", color=LT).next_to(p, lado, buff=0.08)


def contacto_d(x, y0, L=0.9, na=True, marca=None, n1="", n2="", sw=2.6, color=LT):
    """Contacto vertical de y0 (arriba) a y0-L. Devuelve VGroup con .medio (punto de la cuchilla)."""
    ya, yb = y0 - 0.36 * L, y0 - 0.66 * L
    g = VGroup(Line([x, y0, 0], [x, ya, 0]), Line([x, yb, 0], [x, y0 - L, 0]))
    if na:
        fin = [x - 0.2 * L, ya + 0.02, 0]
    else:
        g.add(Line([x, ya, 0], [x + 0.17 * L, ya, 0]))
        fin = [x + 0.2 * L, ya - 0.02, 0]
    g.add(Line([x, yb, 0], fin))
    r = 0.05 * L
    if marca == "disy":
        g.add(Line([x - r, ya - r, 0], [x + r, ya + r, 0]), Line([x - r, ya + r, 0], [x + r, ya - r, 0]))
    elif marca == "cont":
        g.add(Arc(radius=r, start_angle=PI, angle=PI, arc_center=[x, ya, 0]))
    g.set_stroke(color, sw)
    if n1:
        g.add(num_borne([x, y0 - 0.12 * L, 0], n1))
    if n2:
        g.add(num_borne([x, y0 - 0.9 * L, 0], n2))
    g.medio = np.array([(x + fin[0]) / 2, (yb + fin[1]) / 2, 0])
    return g


def accion(desde, hasta, color=LT):
    return DashedLine(desde, hasta, dash_length=0.06).set_stroke(color, 1.8)


def pulsador_e(p, color=LT):
    """Mando manual por pulsador (E) a la izquierda del punto p."""
    x, y = p[0], p[1]
    return VMobject().set_points_as_corners([[x + 0.02, y + 0.13, 0], [x - 0.1, y + 0.13, 0], [x - 0.1, y - 0.13, 0], [x + 0.02, y - 0.13, 0]]).set_stroke(color, 2.4)


def caja_color(m, color, pad=0.14):
    r = Rectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=0).set_fill(color, 0.20).move_to(m)
    r.set_z_index(-1)
    return r


def borne_d(p, txt=None, lado=UP):
    c = Circle(radius=0.07, stroke_color=LT, stroke_width=2.4).set_fill(BLACK, 1).move_to(p)
    g = VGroup(c)
    if txt:
        g.add(Text(txt, font=SANS, font_size=18, weight="BOLD", color=LT).next_to(c, lado, buff=0.06))
    return g


def rotulo(texto, p, lado=LEFT, size=22, color=LT):
    return Text(texto, font=SANS, font_size=size, weight="BOLD", color=color).next_to(p, lado, buff=0.1)


def diagrama_mando(x0=-2.6, y_top=3.3, h=7.0, s=1.0):
    """Mando 240 VAC: L1 → -F1(1-2) → -F2(95-96) → -S1(11-12) → -S2(13-14) ∥ -KM1(13-14) → -KM1(A1-A2) → -F1(4-3) → L2.
    Devuelve VGroup y un dict con las partes (para resaltarlas tramo por tramo)."""
    P = {}
    xr = x0 + 2.6          # línea de regreso (L2)
    y = y_top
    P["L1"] = borne_d([x0, y, 0], "L1  (-Q1: 2)", UP)
    P["L2"] = borne_d([xr, y, 0], "L2  (-Q1: 4)", UP)
    # -F1 polo 1 y polo 2 (en el regreso)
    f1a = contacto_d(x0, y - 0.25, 0.9, True, "disy", "1", "2")
    f1b = contacto_d(xr, y - 0.25, 0.9, True, "disy", "3", "4")
    P["F1"] = VGroup(f1a, f1b, accion(f1a.medio, f1b.medio))
    P["F1_et"] = rotulo("-F1", f1a.medio + LEFT * 0.3)
    # -F2 95-96 (NC, accionado por el térmico)
    f2 = contacto_d(x0, y - 1.5, 0.9, False, None, "95", "96")
    term = VGroup(Rectangle(width=0.3, height=0.26).set_stroke(LT, 2.2).move_to(f2.medio + LEFT * 0.62),
                  VMobject().set_points_as_corners([f2.medio + LEFT * 0.72 + DOWN * 0.07, f2.medio + LEFT * 0.62 + DOWN * 0.07, f2.medio + LEFT * 0.62 + UP * 0.07, f2.medio + LEFT * 0.52 + UP * 0.07]).set_stroke(LT, 2.2))
    P["F2"] = VGroup(f2, term, accion(f2.medio + LEFT * 0.47, f2.medio + RIGHT * 0.05))
    P["F2_et"] = rotulo("-F2", term, LEFT)
    # -S1 paro 11-12 (NC)
    s1 = contacto_d(x0, y - 2.75, 0.9, False, None, "11", "12")
    P["S1"] = VGroup(s1, pulsador_e(s1.medio + LEFT * 0.55), accion(s1.medio + LEFT * 0.53, s1.medio + RIGHT * 0.05))
    P["S1_et"] = rotulo("-S1", s1.medio + LEFT * 0.7)
    # nodo de la retención
    yn1, yn2 = y - 3.85, y - 5.15
    P["n_arriba"] = VGroup(Line([x0, y - 3.65, 0], [x0, yn1, 0]), Line([x0, yn1, 0], [x0 + 1.3, yn1, 0]), Dot([x0, yn1, 0], 0.06, color=ROJO_M)).set_stroke(LT, 2.6)
    s2 = contacto_d(x0, yn1 - 0.2, 0.9, True, None, "13", "14")
    P["S2"] = VGroup(s2, pulsador_e(s2.medio + LEFT * 0.55), accion(s2.medio + LEFT * 0.53, s2.medio))
    P["S2_et"] = rotulo("-S2", s2.medio + LEFT * 0.7)
    km = contacto_d(x0 + 1.3, yn1 - 0.2, 0.9, True, "cont", "13", "14")
    P["KM_ret"] = VGroup(Line([x0 + 1.3, yn1, 0], [x0 + 1.3, yn1 - 0.2, 0]), km)
    P["KM_ret_et"] = rotulo("-KM1", km.medio + RIGHT * 0.95, LEFT, 20)
    P["n_abajo"] = VGroup(Line([x0, yn1 - 1.1, 0], [x0, yn2, 0]), Line([x0 + 1.3, yn1 - 1.1, 0], [x0 + 1.3, yn2, 0]),
                          Line([x0, yn2, 0], [x0 + 1.3, yn2, 0]), Dot([x0, yn2, 0], 0.06, color=ROJO_M)).set_stroke(LT, 2.6)
    # bobina
    yb = yn2 - 0.15
    bob = VGroup(Line([x0, yn2, 0], [x0, yb - 0.25, 0]), Rectangle(width=0.62, height=0.4).set_stroke(LT, 2.6).move_to([x0, yb - 0.45, 0]),
                 Line([x0, yb - 0.65, 0], [x0, yb - 0.95, 0]))
    bob.add(num_borne([x0, yb - 0.17, 0], "A1"), num_borne([x0, yb - 0.78, 0], "A2"))
    P["KM_bob"] = bob
    P["KM_bob_et"] = rotulo("-KM1", bob[1], LEFT)
    # conductores entre aparatos y regreso
    ybot = yb - 0.95
    P["lineas"] = VGroup(Line([x0, y - 0.07, 0], [x0, y - 0.25, 0]), Line([x0, y - 1.15, 0], [x0, y - 1.5, 0]), Line([x0, y - 2.4, 0], [x0, y - 2.75, 0]),
                         Line([x0, ybot, 0], [x0, ybot - 0.25, 0]), Line([x0, ybot - 0.25, 0], [xr, ybot - 0.25, 0]), Line([xr, ybot - 0.25, 0], [xr, y - 1.15, 0]),
                         Line([xr, y - 0.07, 0], [xr, y - 0.25, 0])).set_stroke(LT, 2.6)
    # cajas de color por equipo (como la referencia)
    cajas = VGroup(caja_color(P["F1"], C_F1), caja_color(P["F2"], C_F2), caja_color(P["S1"], C_S), caja_color(P["S2"], C_S),
                   caja_color(P["KM_ret"][1], C_KM), caja_color(P["KM_bob"][1], C_KM))
    P["cajas"] = cajas
    todo = VGroup(cajas, *[v for k, v in P.items() if k != "cajas"])
    return todo, P


def diagrama_potencia(x0=-6.4, y_top=3.3, dx=0.75):
    P = {}
    xs = [x0 + i * dx for i in range(3)]
    xpe = x0 + 3 * dx
    P["X0"] = VGroup(*[borne_d([x, y_top, 0], t, UP) for x, t in zip(xs + [xpe], ["L1", "L2", "L3", "PE"])])
    P["X0_et"] = rotulo("-X0", P["X0"][0], LEFT)
    q = VGroup(*[contacto_d(x, y_top - 0.3, 1.0, True, "disy", a, b, sw=3.4) for x, a, b in zip(xs, "135", "246")])
    q.add(accion(q[0].medio, q[2].medio))
    P["Q1"] = q
    P["Q1_et"] = rotulo("-Q1", q[0].medio + LEFT * 0.25)
    k = VGroup(*[contacto_d(x, y_top - 1.65, 1.0, True, "cont", a, b, sw=3.4) for x, a, b in zip(xs, ["1", "3", "5"], ["2", "4", "6"])])
    k.add(accion(k[0].medio, k[2].medio))
    P["KM1"] = k
    P["KM1_et"] = rotulo("-KM1", k[0].medio + LEFT * 0.25)
    yt = y_top - 3.05
    f = VGroup(Rectangle(width=dx * 3, height=0.45).set_stroke(LT, 2.4).move_to([xs[1], yt, 0]))
    for x in xs:
        f.add(VMobject().set_points_as_corners([[x, yt + 0.22, 0], [x, yt + 0.1, 0], [x + 0.12, yt + 0.1, 0], [x + 0.12, yt - 0.1, 0], [x, yt - 0.1, 0], [x, yt - 0.22, 0]]).set_stroke(LT, 3.2))
    f.add(Line([xs[0] - dx / 2, yt, 0], [xs[0] - dx / 2 - 0.3, yt, 0]).set_stroke(LT, 2), )
    P["F2"] = f
    P["F2_et"] = rotulo("-F2", f, LEFT)
    yx1 = y_top - 4.0
    P["X1"] = VGroup(*[borne_d([x, yx1, 0]) for x in xs + [xpe]])
    P["X1_et"] = rotulo("-X1", P["X1"][0], LEFT)
    ym = y_top - 5.35
    mot = VGroup(Circle(radius=0.62).set_stroke(LT, 3.2).move_to([xs[1], ym, 0]),
                 Text("M", font=SANS, font_size=28, weight="BOLD", color=LT).move_to([xs[1], ym + 0.15, 0]),
                 Text("3~", font=SANS, font_size=22, weight="BOLD", color=LT).move_to([xs[1], ym - 0.2, 0]))
    P["M1"] = mot
    P["M1_et"] = rotulo("-M1", mot, LEFT)
    lin = VGroup()
    for x in xs:
        lin.add(Line([x, y_top - 0.07, 0], [x, y_top - 0.3, 0]), Line([x, y_top - 1.3, 0], [x, y_top - 1.65, 0]),
                Line([x, y_top - 2.65, 0], [x, yt + 0.22, 0]), Line([x, yt - 0.22, 0], [x, yx1 + 0.07, 0]))
    import math
    for x, t in zip(xs, ["U1", "V1", "W1"]):
        yc = ym + math.sqrt(max(0.62 ** 2 - (x - xs[1]) ** 2, 0))
        lin.add(Line([x, yx1 - 0.07, 0], [x, yc, 0]))
        lin.add(Text(t, font=SANS, font_size=16, weight="BOLD", color=LT).next_to([x, yx1 - 0.35, 0], RIGHT, buff=0.04))
    lin.add(Line([xpe, y_top - 0.07, 0], [xpe, yx1 + 0.07, 0]).set_stroke(PE_V, 2.6), Line([xpe, yx1 - 0.07, 0], [xpe, ym, 0]).set_stroke(PE_V, 2.6),
            Line([xpe, ym, 0], [xs[2] + 0.45, ym, 0]).set_stroke(PE_V, 2.6))
    lin.set_stroke(width=3.2)
    for m in lin:
        if m.get_stroke_color() != ManimColor(PE_V) and not isinstance(m, Text):
            m.set_stroke(LT)
    P["lineas"] = lin
    P["cajas"] = VGroup(caja_color(P["Q1"], C_Q), caja_color(P["KM1"], C_KM), caja_color(P["F2"], C_F2))
    todo = VGroup(P["cajas"], *[v for kk, v in P.items() if kk != "cajas"])
    return todo, P


# =========================================================================== disposición física y rutas (canaletas)
def disposicion(k=0.029, x0=0.75, ytop=3.72, puerta=True):
    """Equipos como en el tablero real: -Q1 arriba con -F1 a la derecha, -KM1 debajo de -Q1 con -F2 acoplado,
    fila de borneras -X0 -X1 -X2 abajo y los pulsadores de la puerta a la derecha.
    Los cables salen de cada borne hacia una 'canaleta' (carril horizontal o vertical) y entran al borne de destino."""
    E = {}
    Q1 = E["Q1"] = Eq("Q1", k).poner([x0, ytop, 0])
    F1 = E["F1"] = Eq("F1", k).poner([Q1.cuerpo(RIGHT)[0] + 0.32, ytop, 0])
    # -KM1 centrado bajo -Q1 (polo central alineado)
    x_km = Q1.p("3")[0] - 22.6 * k
    KM1 = E["KM1"] = Eq("KM1", k).poner([x_km, Q1.cuerpo(DOWN)[1] - 0.34, 0])
    F2 = E["F2"] = Eq("F2", k).poner([x_km, KM1.cuerpo(DOWN)[1], 0])
    KM1.set_z_index(2)
    F2.set_z_index(1)
    yx = F2.cuerpo(DOWN)[1] - 0.36
    X0 = E["X0"] = Eq("X0", k).poner([x0 - 0.3, yx, 0])
    X1 = E["X1"] = Eq("X1", k).poner([X0.cuerpo(RIGHT)[0] + 0.12, yx, 0])
    X2 = E["X2"] = Eq("X2", k).poner([X1.cuerpo(RIGHT)[0] + 0.55, yx, 0])
    if puerta:
        xb = F1.cuerpo(RIGHT)[0] + 1.25
        E["B1"] = Eq("B1", k * 1.25).poner([xb, ytop - 0.3, 0])
        E["S1"] = Eq("S1", k * 1.1).poner([xb + 1.3, ytop - 0.3, 0])
        E["B2"] = Eq("B2", k * 1.25).poner([xb, ytop - 2.2, 0])
        E["S2"] = Eq("S2", k * 1.1).poner([xb + 1.3, ytop - 2.2, 0])
    return E


def rutas_mando(E):
    """Hilos del mando (rojo 14 AWG). Cada tramo: (clave de voz, partes del diagrama, [(puntos, número de hilo)])."""
    Q1, F1, KM1, F2, X2 = (E[n] for n in ("Q1", "F1", "KM1", "F2", "X2"))
    B1, B2 = E["B1"], E["B2"]
    P = lambda e, b: e.p(b)
    yB = (Q1.cuerpo(DOWN)[1] + KM1.cuerpo(UP)[1]) / 2          # canaleta entre -Q1 y -KM1
    yA = Q1.cuerpo(UP)[1] + 0.22                                # canaleta superior
    yD = (F2.cuerpo(DOWN)[1] + X2.cuerpo(UP)[1]) / 2             # canaleta inferior
    xg = (Q1.cuerpo(RIGHT)[0] + F1.cuerpo(LEFT)[0]) / 2          # paso entre -Q1 y -F1
    xL = KM1.cuerpo(LEFT)[0] - 0.12                              # canaleta izquierda de -KM1
    xR = KM1.cuerpo(RIGHT)[0] + 0.12                             # canaleta derecha de -KM1
    xP = (F1.cuerpo(RIGHT)[0] + B1.cuerpo(LEFT)[0]) / 2          # mazo de la puerta
    d = 0.065
    T = []
    a, b = P(Q1, "2"), P(F1, "1")
    c, e = P(Q1, "4"), P(F1, "3")
    T.append(("c1", ["F1"], [([a, [a[0], yB + d, 0], [xg - d, yB + d, 0], [xg - d, yA + d, 0], [b[0], yA + d, 0], b], 1),
                             ([c, [c[0], yB - 0 * d, 0], [xg + d, yB, 0], [xg + d, yA + 2 * d, 0], [e[0], yA + 2 * d, 0], e], 2)]))
    a, b = P(F1, "2"), P(F2, "95")
    T.append(("c2", ["F1", "F2"], [([a, [a[0], b[1], 0], b], 3)]))
    a, b = P(F2, "96"), P(X2, "1_a")
    T.append(("c3", ["F2", "S1"], [([a, [a[0], yD + d, 0], [b[0], yD + d, 0], b], 4),
                                   ([P(X2, "1_b"), P(X2, "1_b") + DOWN * 0.22, [xP - 1.5 * d, P(X2, "1_b")[1] - 0.22, 0], [xP - 1.5 * d, P(B1, "1")[1], 0], P(B1, "1")], 4)]))
    a = P(KM1, "13")
    T.append(("c4", ["S1", "S2", "KM_ret"], [
        ([P(B1, "2"), [xP - 0.5 * d, P(B1, "2")[1], 0], [xP - 0.5 * d, P(X2, "2_b")[1] - 0.3, 0], [P(X2, "2_b")[0], P(X2, "2_b")[1] - 0.3, 0], P(X2, "2_b")], 5),
        ([P(X2, "2_b"), [P(X2, "2_b")[0] + 0.0, P(X2, "2_b")[1] - 0.3 - d, 0], [xP + 0.5 * d, P(X2, "2_b")[1] - 0.3 - d, 0], [xP + 0.5 * d, P(B2, "3")[1], 0], P(B2, "3")], 5),
        ([a, [xL, a[1], 0], [xL, yD, 0], [P(X2, "2_a")[0], yD, 0], P(X2, "2_a")], 5)]))
    a, a1 = P(KM1, "14"), P(KM1, "A1")
    T.append(("c5", ["S2", "KM_ret", "KM_bob"], [
        ([P(B2, "4"), [xP + 1.5 * d, P(B2, "4")[1], 0], [xP + 1.5 * d, P(X2, "3_b")[1] - 0.3 - 2 * d, 0], [P(X2, "3_b")[0], P(X2, "3_b")[1] - 0.3 - 2 * d, 0], P(X2, "3_b")], 6),
        ([a, [xL - d, a[1], 0], [xL - d, yD - d, 0], [P(X2, "3_a")[0], yD - d, 0], P(X2, "3_a")], 6),
        ([a1, [xR, a1[1], 0], [xR, yD - 2 * d, 0], [P(X2, "3_a")[0] + 0.03, yD - 2 * d, 0], P(X2, "3_a") + RIGHT * 0.03], 6)]))
    a, b = P(KM1, "A2"), P(F1, "4")
    T.append(("c6", ["KM_bob", "F1"], [([a, [xR + d, a[1], 0], [xR + d, yB - d, 0], [b[0], yB - d, 0], b], 7)]))
    return T


def rutas_potencia(E):
    Q1, KM1, F2, X0, X1 = (E[n] for n in ("Q1", "KM1", "F2", "X0", "X1"))
    yA = Q1.cuerpo(UP)[1] + 0.22
    xI = X0.cuerpo(LEFT)[0] - 0.08
    d = 0.09
    R = {}
    R["p1"] = [[X0.p(f + "_a"), X0.p(f + "_a") + UP * (0.18 + d * (2 - i)), [xI - d * (2 - i), X0.p(f + "_a")[1] + 0.18 + d * (2 - i), 0],
                [xI - d * (2 - i), yA + 0.12 + d * i, 0], [Q1.p(str(2 * i + 1))[0], yA + 0.12 + d * i, 0], Q1.p(str(2 * i + 1))] for i, f in enumerate(["L1", "L2", "L3"])]
    ym = (Q1.cuerpo(DOWN)[1] + KM1.cuerpo(UP)[1]) / 2 + 0.06
    R["p2"] = [[Q1.p(str(2 * i + 2)), [Q1.p(str(2 * i + 2))[0], ym, 0], [KM1.p(t)[0], ym, 0], KM1.p(t)] for i, t in enumerate(["1/L1", "3/L2", "5/L3"])]
    yD = (F2.cuerpo(DOWN)[1] + X1.cuerpo(UP)[1]) / 2
    R["p4"] = [[F2.p(t), [F2.p(t)[0], yD - d * i, 0], [X1.p(u + "_a")[0], yD - d * i, 0], X1.p(u + "_a")] for i, (t, u) in enumerate(zip(["2/T1", "4/T2", "6/T3"], ["U", "V", "W"]))]
    yb = X0.cuerpo(DOWN)[1] - 0.12
    R["pe"] = [X0.p("PE_b"), [X0.p("PE_b")[0], yb, 0], [X1.p("PE_b")[0], yb, 0], X1.p("PE_b")]
    return R


# =========================================================================== escena
class Lay(Scene):
    """Vista fija de la disposición con TODOS los hilos (revisión de rutas)."""

    def construct(self):
        self.camera.background_color = "#000000"
        E = disposicion()
        self.add(*E.values())
        for _, _, hs in rutas_mando(E):
            for pts, n in hs:
                self.add(hilo(pts, ROJO_M, 2.6, n, k=0.45))
        R = rutas_potencia(E)
        for kk in ("p1", "p2", "p4"):
            for pts in R[kk]:
                self.add(hilo(pts, FASE, 5, None, k=0.5))
        self.add(hilo(R["pe"], "PE", 5, None, k=0.5))
        d, P = diagrama_mando(x0=-4.9, y_top=3.3)
        d.scale_to_fit_height(7.4).move_to([-4.6, -0.45, 0])
        self.add(d)


class H01(ContactorB):
    CARPETA_VOZ = "voz_h01"
    GUION = GH
    SECC = {k: v for k, v in zip(["gancho", "pregunta", "problema", "materiales", "mando", "potencia", "c_mando", "c_potencia", "tablero", "marcha", "cierre"], SH)}
    PROXIMO = "Siguiente: ARRANQUE CON VARIADOR"
    DURACION_MIN = 0.0

    def construct(self):
        self.cinta_act = None
        self.paso_act = None
        orden = ["gancho", "pregunta", "problema", "materiales", "mando", "potencia", "c_mando", "c_potencia", "tablero", "marcha", "cierre"]
        solo = os.environ.get("SOLO")
        for paso in orden:
            if solo and paso not in solo.split(","):
                continue
            getattr(self, "h_" + paso)()

    # --------------------------------------------------------------- utilidades
    def portadilla(self, clave):
        num, titulo = getattr(self, "SECC", SECCIONES)[clave]
        sale = [m for m in (self.cinta_act, self.paso_act) if m is not None]
        fondo = Rectangle(width=16.2, height=9.2, stroke_width=0).set_fill("#06102A" if TEMA != "negro" else "#050608", 0.97).set_z_index(40)
        grande = T(num if len(num) > 1 else f"0{num}", 300, MARCA, "HEAVY").set_opacity(0.14).move_to([4.6, -0.2, 0]).set_z_index(41)
        sec = T(f"SECCIÓN {num}", 30, AMBAR, "HEAVY")
        tit = T(titulo, 70, TXT, "HEAVY")
        if tit.width > 13.0:
            tit.scale_to_fit_width(13.0)
        VGroup(sec, tit).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 0.2, 0])
        barra = RoundedRectangle(width=tit.width, height=0.14, corner_radius=0.07, stroke_width=0).set_fill(MARCA, 1).next_to(tit, DOWN, buff=0.3, aligned_edge=LEFT)
        cursor = Rectangle(width=0.07, height=tit.height * 0.95, stroke_width=0).set_fill(MARCA, 1)
        for m_ in (sec, tit, barra, cursor):
            m_.set_z_index(42)
        self.play(FadeIn(fondo), FadeIn(grande, scale=1.1), FadeIn(sec, shift=RIGHT * 0.2), *[FadeOut(m) for m in sale], run_time=0.45)
        self.cinta_act = None
        self.paso_act = None
        n = len(tit.submobjects)
        dt = 0.05
        wav = DIR / "sfx" / f"tecleo_{n}.wav"
        if not wav.exists():
            sonido_tecleo(wav, n, dt, semilla=n)
        self.add_sound(str(wav), gain=-9)
        cursor.next_to(tit[0], LEFT, buff=0.05)
        self.add(cursor)
        letras = [m for m in tit.submobjects]
        for m in letras:
            m.set_opacity(0)
        self.add(tit)

        def revelar(mob, alpha):
            k = int(alpha * n + 1e-6)
            for i, m in enumerate(letras):
                m.set_opacity(1 if i < k else 0)
            ultimo = letras[max(0, min(k, n) - 1)]
            cursor.move_to([ultimo.get_right()[0] + 0.08, tit.get_center()[1], 0]) if k > 0 else None
        self.play(UpdateFromAlphaFunc(tit, revelar), run_time=n * dt, rate_func=linear)
        cursor.clear_updaters()
        self.play(GrowFromEdge(barra, LEFT), run_time=0.35)
        self.play(cursor.animate.set_opacity(0), run_time=0.15)
        self.play(cursor.animate.set_opacity(1), run_time=0.15)
        self.wait(0.35)
        ci = cinta(num, titulo)
        self.play(FadeOut(VGroup(fondo, grande, sec, tit, barra, cursor)), FadeIn(ci, shift=RIGHT * 0.3), run_time=0.45)
        self.cinta_act = ci

    def esperar_frac(self, f):
        w = self.resta() * f
        if w > 0.05:
            self.wait(w)

    def seccion(self, clave):
        self.portadilla(clave)
        ci = self.cinta_act
        fr = self.camera.frame
        ci.zz = 1.0
        ci.rel = ci.get_center().copy()

        def seguir(m):
            z = fr.width / 16
            if abs(z - m.zz) > 1e-6:
                m.scale(z / m.zz)
                m.zz = z
            m.move_to(fr.get_center() + m.rel * z)
        ci.add_updater(seguir)

    def salir(self, t=0.5):
        """Limpia la pantalla (menos fondo y cinta) y regresa la cámara al centro."""
        fr = self.camera.frame
        ms = [m for m in self.mobjects if m is not fr and m is not self.cinta_act and all(m is not f for f in self._fondo)]
        for m in ms:
            for sm in m.get_family():
                sm.clear_updaters()
        anims = [FadeOut(m) for m in ms]
        if abs(fr.width - 16) > 1e-3 or np.linalg.norm(fr.get_center()) > 1e-3:
            anims.append(fr.animate.set(width=16).move_to(ORIGIN))
        if anims:
            self.play(*anims, run_time=t)
        self.remove(*ms)

    def setup(self):
        super().setup()
        self._fondo = list(self.mobjects)

    def flujo(self, pts, n=26, color=AMBAR, r=0.045, vel=0.12):
        ruta = VMobject().set_points_as_corners(pts)
        g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
        g.fase = 0.0

        def upd(m, dt):
            m.fase = (m.fase + dt * vel) % 1
            for k, d in enumerate(m):
                d.move_to(ruta.point_from_proportion((m.fase + k / n) % 1))
        g.add_updater(upd)
        upd(g, 0)
        return g

    def zoom(self, centro, ancho=5.0, rt=0.8):
        self.play(self.camera.frame.animate.set(width=ancho).move_to(centro), run_time=rt)

    def zoom_fuera(self, rt=0.8):
        self.play(self.camera.frame.animate.set(width=16).move_to(ORIGIN), run_time=rt)

    def texto(self, s, size=30, color=TXT, peso="HEAVY"):
        return T(s, size, color, peso)

    # =============================================================== 1 · GANCHO
    def h_gancho(self):
        self.voz("gancho")
        mo = Eq("M1", 0.03).move_to([-2.2, 0.2, 0])
        self.play(FadeIn(mo, shift=UP * 0.3), run_time=0.8)
        giro = VGroup(*[Arc(radius=0.5 + 0.18 * i, start_angle=PI / 2 + i, angle=PI * 1.2, stroke_width=3).set_stroke(MARCA, opacity=0.9 - 0.25 * i) for i in range(3)])
        giro.move_to(mo.img.get_left() + RIGHT * 0.5 + DOWN * 0.15)
        self.sfx("motor", -12)
        self.play(Rotate(giro, -TAU * 2, about_point=giro.get_center()), FadeIn(giro), run_time=2.5, rate_func=linear)
        q1 = Eq("Q1", 0.05).move_to([4.3, 0.2, 0])
        self.sfx("breaker", -8)
        self.play(FadeIn(q1, shift=LEFT * 0.4), FadeOut(giro), run_time=0.6)
        aro = Circle(radius=0.9, color=ROJO, stroke_width=7).move_to(q1.img.get_center() + UP * 0.35 + LEFT * 0.15)
        preg = T("¿BIEN CALCULADA?", 64, TXT, "HEAVY").move_to([0, -3.4, 0])
        self.play(Create(aro), Write(preg), run_time=1.0)
        self.esperar_frac(0.55)
        pasos = VGroup(*[pastilla(t, MARCA, 26, i == 0) for i, t in enumerate(["CÁLCULO", "MANDO", "POTENCIA", "CONEXIÓN", "TABLERO", "MARCHA"])]).arrange(RIGHT, buff=0.18).move_to([0, 3.4, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pasos], lag_ratio=0.15), run_time=1.5)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 2 · PREGUNTA
    def h_pregunta(self):
        self.seccion("pregunta")
        self.voz("pregunta")
        a = VGroup(T("MOTOR", 30, TXT2, "BOLD"), T("24,3 A", 110, TXT, "HEAVY")).arrange(DOWN, buff=0.2).move_to([-4.0, 0.6, 0])
        b = VGroup(T("BREAKER", 30, TXT2, "BOLD"), T("70 A", 110, AMBAR, "HEAVY")).arrange(DOWN, buff=0.2).move_to([4.0, 0.6, 0])
        q = T("?", 160, ROJO, "HEAVY").move_to([0, 0.6, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(b, shift=LEFT * 0.3), run_time=0.6)
        self.sfx("pop", -10)
        self.play(FadeIn(q, scale=1.4), run_time=0.4)
        self.esperar_frac(0.25)
        c1 = etiqueta("BREAKER  →  protege el CABLE (cortocircuito)", AMBAR, 30).move_to([0, -2.0, 0])
        self.play(FadeOut(q), FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.esperar_frac(0.35)
        c2 = etiqueta("RELÉ TÉRMICO  →  protege el MOTOR (sobrecarga)", C_F2, 30).move_to([0, -3.1, 0])
        self.sfx("pop", -10)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 3 · PROBLEMA REAL
    def tarjeta_calc(self, norma, lineas, resultado, color, pos):
        cod = pastilla(norma, color, 22, True)
        ls = VGroup(*[T(l, 26, TXT, "MEDIUM") for l in lineas]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        res = T(resultado, 38, color, "HEAVY")
        cuerpo = VGroup(cod, ls, res).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        if cuerpo.width > 4.5:
            cuerpo.scale_to_fit_width(4.5)
        caja = RoundedRectangle(width=5.0, height=2.35, corner_radius=0.08, stroke_color=color, stroke_width=2).set_fill(CARTA, 1)
        cuerpo.move_to(caja)
        return VGroup(caja, cuerpo).move_to(pos)

    def escribir(self, m, rt=0.8):
        n = len(m.family_members_with_points())
        wav = DIR / "sfx" / f"tecleo_{min(26, max(14, n // 4))}.wav"
        if wav.exists():
            self.add_sound(str(wav), gain=-12)
        self.play(FadeIn(m[0]), Write(m[1]), run_time=rt)

    def h_problema(self):
        self.seccion("problema")
        self.voz("placa")
        mo = Eq("M1", 0.036).move_to([0, -0.2, 0])
        self.play(FadeIn(mo), run_time=0.6)
        # la placa plateada está a la derecha del centro del motor
        placa_c = mo.img.get_center() + RIGHT * 0.6 * 0.036 * 1000 / 1000 * 0
        self.zoom(mo.img.get_center() + RIGHT * 1.65 + DOWN * 0.45, 5.2, 1.2)
        self.esperar_frac(0.7)
        self.zoom_fuera(0.8)
        red = etiqueta("RED: 240 V · 3~ · 60 Hz", MARCA, 30).move_to([0, -3.6, 0])
        self.play(FadeIn(red, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(mo.animate.scale(0.45).move_to([-5.4, 2.0, 0]), FadeOut(red), run_time=0.8)
        # tarjetas de cálculo
        self.voz("tabla")
        t1 = self.tarjeta_calc("NEC T430.250", ["10 hp · 230 V · trifásico"], "I tabla = 28 A", MARCA, [0.0, 2.0, 0])
        self.escribir(t1)
        self.cerrar_voz(0.1)
        self.voz("cable")
        t2 = self.tarjeta_calc("NEC 430.22", ["125 % × 28 A = 35 A"], "10 AWG THHN 75 °C", C_F1, [5.4, 2.0, 0])
        self.escribir(t2)
        self.cerrar_voz(0.1)
        self.voz("breaker")
        t3 = self.tarjeta_calc("NEC T430.52", ["250 % × 28 A = 70 A", "arranque: 162 A (LRA)"], "-Q1 · 3P · 70 A", C_Q, [-5.4, -1.2, 0])
        self.escribir(t3)
        self.cerrar_voz(0.1)
        self.voz("termico")
        t4 = self.tarjeta_calc("NEC 430.32(A)(1)", ["F.S. 1,25 → máx 125 % × 24,3 = 30,4 A", "rango 23–32 A"], "-F2 ajuste 24,3 A", C_F2, [0.0, -1.2, 0])
        self.escribir(t4)
        self.cerrar_voz(0.1)
        self.voz("contactor")
        t5 = self.tarjeta_calc("IEC 60947-4-1", ["AC-3 · bobina 240 VAC", "mando: 2P 6 A · 14 AWG"], "-KM1 32 A · -F1 6 A", C_KM, [5.4, -1.2, 0])
        self.escribir(t5)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 4 · MATERIALES
    def h_materiales(self):
        self.seccion("materiales")
        self.voz("materiales")
        filas = [("Q1", 0.022, "-Q1", "Breaker 3P 70 A", C_Q), ("F1", 0.022, "-F1", "Breaker 2P 6 A (mando)", C_F1),
                 ("KM1", 0.024, "-KM1", "Contactor 32 A AC-3 · 240 VAC", C_KM), ("F2", 0.026, "-F2", "Relé térmico 23–32 A", C_F2),
                 ("S1", 0.034, "-S1", "Pulsador rojo · NC (paro)", ROJO), ("S2", 0.034, "-S2", "Pulsador verde · NA (marcha)", VERDE_OK),
                 ("X0", 0.03, "-X0 -X1 -X2", "Borneras: alimentación, motor, puerta", C_X), (None, 0, "Cable", "10 AWG negro · 14 AWG rojo · PE", AMBAR),
                 ("M1", 0.0075, "-M1", "Motor 10 hp · 230 V Δ · 24,3 A", MARCA)]
        cartas = []
        for i, (n, k, ref, desc, col) in enumerate(filas):
            caja = RoundedRectangle(width=4.9, height=2.25, corner_radius=0.08, stroke_color=col, stroke_width=2).set_fill(CARTA, 1)
            if n:
                im = Eq(n, k)
                im.img.scale_to_fit_height(min(im.img.height, 1.9))
                if im.img.width > 1.9:
                    im.img.scale_to_fit_width(1.9)
                im.img.move_to(caja.get_left() + RIGHT * 1.15)
            else:
                cs = VGroup(*[Line(LEFT * 0.8, RIGHT * 0.8).set_stroke(c, w) for c, w in (("#8F9AC8", 9), (ROJO_M, 6), (PE_V, 7))]).arrange(DOWN, buff=0.25)
                im = cs.move_to(caja.get_left() + RIGHT * 1.15)
            t = VGroup(T(ref, 28, col, "HEAVY"), Paragraph(*self.partir(desc, 20), font=SANS, font_size=20, color=TXT, line_spacing=0.8)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            t.next_to(caja.get_left() + RIGHT * 2.25, RIGHT, buff=0).align_to(caja.get_left() + RIGHT * 2.25, LEFT)
            c = Group(caja, im, t)
            c.move_to([-5.3 + (i % 3) * 5.3, 2.1 - (i // 3) * 2.55, 0])
            cartas.append(c)
        pesos = np.array([1.3, 1.2, 1.3, 1.2, 1.1, 1.1, 1.6, 1.4, 0.7])
        lim = np.cumsum(pesos) / pesos.sum()
        t0 = self.renderer.time
        dur = self.fin_voz - t0
        for i, c in enumerate(cartas):
            self.sfx("pop", -14)
            self.play(FadeIn(c, shift=UP * 0.25), run_time=0.45)
            fin = t0 + dur * lim[i] - 0.45
            w = fin - self.renderer.time
            if w > 0.05:
                self.wait(w)
        self.cerrar_voz(0.3)
        self.salir()

    @staticmethod
    def partir(s, n):
        pal, l, out = s.split(), "", []
        for p in pal:
            if len(l) + len(p) + 1 > n and l:
                out.append(l)
                l = p
            else:
                l = (l + " " + p).strip()
        out.append(l)
        return out

    # =============================================================== 5 · DIAGRAMA DE MANDO
    def h_mando(self):
        self.seccion("mando")
        self.voz("mando")
        d, P = diagrama_mando(x0=-1.3, y_top=3.2)
        d.scale_to_fit_height(7.3).move_to([0, -0.4, 0])
        orden = [("L1", "L2", "lineas"), ("F1", "F1_et"), ("F2", "F2_et"), ("S1", "S1_et"), ("n_arriba", "S2", "S2_et"), ("KM_ret", "KM_ret_et"), ("n_abajo", "KM_bob", "KM_bob_et")]
        pesos = np.array([0.8, 1.2, 1.6, 1.2, 1.2, 1.4, 1.5])
        lim = np.cumsum(pesos) / pesos.sum()
        t0 = self.renderer.time
        dur = self.fin_voz - t0
        cajas = {"F1": 0, "F2": 1, "S1": 2, "S2": 3, "KM_ret": 4, "KM_bob": 5}
        for i, grupo in enumerate(orden):
            anims = []
            for k in grupo:
                anims.append(Create(P[k]) if k not in ("L1", "L2") and not k.endswith("_et") else FadeIn(P[k]))
                if k in cajas:
                    anims.append(FadeIn(P["cajas"][cajas[k]]))
            self.add_sound(str(DIR / "sfx" / "tecleo_16.wav"), gain=-16)
            self.play(*anims, run_time=1.0)
            w = t0 + dur * lim[i] - self.renderer.time
            if w > 0.05:
                self.wait(w)
        self.cerrar_voz(0.1)
        # funcionamiento de la retención: corriente animada
        self.voz("retencion")
        x0 = P["L1"][0].get_center()[0]
        ruta1 = [P["L1"][0].get_center(), P["n_arriba"][2].get_center(), P["n_abajo"][3].get_center(), P["KM_bob"][1].get_top()]
        f1 = self.flujo([ruta1[0], ruta1[1], ruta1[2]], 18, AMBAR)
        bob = P["KM_bob"][1]
        pulso = Circle(radius=0.12, color=AMBAR, stroke_width=4).move_to(P["S2"][1].get_center())
        self.play(Indicate(P["S2"], color=AMBAR), Create(pulso), run_time=0.7)
        self.add(f1)
        self.sfx("contactor", -10)
        self.play(bob.animate.set_fill(AMBAR, 0.6), P["KM_ret"].animate.set_color(AMBAR), run_time=0.6)
        self.esperar_frac(0.35)
        ret = P["KM_ret"][1].copy().set_stroke(AMBAR, 4)
        self.play(FadeOut(pulso), ShowPassingFlash(ret, time_width=0.6), run_time=1.0)
        self.esperar_frac(0.4)
        self.play(Indicate(P["S1"], color=ROJO), run_time=0.7)
        self.sfx("contactor", -14)
        f1.clear_updaters()
        self.play(FadeOut(f1), bob.animate.set_fill(BLACK, 1), P["KM_ret"].animate.set_color(LT), run_time=0.6)
        self.cerrar_voz(0.3)
        self.diag_mando = (d, P)
        self.salir()

    # =============================================================== 6 · DIAGRAMA DE POTENCIA
    def h_potencia(self):
        self.seccion("potencia")
        self.voz("potencia")
        d, P = diagrama_potencia(x0=-3.6, y_top=3.2, dx=0.9)
        d.scale_to_fit_height(7.2).move_to([-2.6, -0.45, 0])
        grupos = [("X0", "X0_et"), ("Q1", "Q1_et"), ("KM1", "KM1_et"), ("F2", "F2_et"), ("X1", "X1_et"), ("M1", "M1_et", "lineas")]
        cajas = {"Q1": 0, "KM1": 1, "F2": 2}
        pesos = np.array([1.0, 0.9, 1.4, 0.6, 1.4, 1.2])
        lim = np.cumsum(pesos) / pesos.sum() * 0.62
        t0 = self.renderer.time
        dur = self.fin_voz - t0
        self.play(Create(P["lineas"]), run_time=1.2)
        for i, g in enumerate(grupos):
            anims = []
            for k in g:
                if k == "lineas":
                    continue
                anims.append(FadeIn(P[k]) if k.endswith("_et") or k in ("X0", "X1") else Create(P[k]))
                if k in cajas:
                    anims.append(FadeIn(P["cajas"][cajas[k]]))
            self.add_sound(str(DIR / "sfx" / "tecleo_16.wav"), gain=-16)
            self.play(*anims, run_time=0.9)
            w = t0 + dur * lim[i] - self.renderer.time
            if w > 0.05:
                self.wait(w)
        cb = Eq("CB", 0.04).move_to([4.6, -0.2, 0])
        tit = T("Caja de bornes · triángulo (Δ)", 28, TXT, "HEAVY").next_to(cb, UP, buff=0.25)
        self.play(FadeIn(cb, shift=LEFT * 0.3), FadeIn(tit), run_time=0.7)
        self.zoom(cb.img.get_center(), 6.0, 1.0)
        pares = [("U1", "W2"), ("V1", "U2"), ("W1", "V2")]
        for a, b in pares:
            r = Line(cb.p(a), cb.p(b)).set_stroke(AMBAR, 10, opacity=0.55)
            fisico(r)
            self.sfx("tic", -10)
            self.play(Create(r), run_time=0.45)
            self.wait(0.6)
        self.cerrar_voz(0.2)
        self.zoom_fuera(0.6)
        self.salir()

    # =============================================================== 7 · CONEXIÓN DEL MANDO
    def resaltar(self, partes, P):
        cajas = []
        for p in partes:
            m = P[p][1] if p == "KM_ret" else P[p]
            cajas.append(caja_color(m, AMBAR, 0.08).set_fill(AMBAR, 0.38))
        return VGroup(*cajas)

    def tender(self, pts_lista, color, w, nums, k_et, sonido="tic"):
        hs = [hilo(p, color if not isinstance(color, list) else color[i], w, nums[i], k=k_et) for i, p in enumerate(pts_lista)]
        a = np.array(pts_lista[0][0])
        b = np.array(pts_lista[-1][-1])
        todos = np.array([q for p in pts_lista for q in p], float)
        lo, hi = todos.min(axis=0), todos.max(axis=0)
        ancho = max(3.2, min(9.0, max(hi[0] - lo[0], (hi[1] - lo[1]) * 16 / 9) * 1.25))
        self.zoom((lo + hi) / 2, ancho, 0.6)
        self.play(*[Create(h[0]) for h in hs], run_time=1.1)
        self.sfx(sonido, -10)
        self.play(*[FadeIn(h[1]) for h in hs], run_time=0.25)
        return hs

    def h_c_mando(self):
        self.seccion("c_mando")
        self.voz("c_intro")
        d, P = diagrama_mando(x0=-4.9, y_top=3.3)
        d.scale_to_fit_height(7.4).move_to([-4.6, -0.45, 0])
        E = disposicion()
        puerta = DashedLine([E["B1"].cuerpo(LEFT)[0] - 0.22, 3.9, 0], [E["B1"].cuerpo(LEFT)[0] - 0.22, -0.2, 0], dash_length=0.12).set_stroke(TXT2, 1.6)
        lp = T("PUERTA", 18, TXT2, "BOLD").next_to(puerta, UP, buff=0.04).shift(RIGHT * 0.9)
        self.play(FadeIn(d), *[FadeIn(e) for e in E.values()], Create(puerta), FadeIn(lp), run_time=1.2)
        self.cerrar_voz(0.1)
        self.cables = VGroup()
        for clave, partes, hilos in rutas_mando(E):
            self.voz(clave)
            hl = self.resaltar(partes, P)
            self.play(FadeIn(hl), run_time=0.4)
            for pts, n in hilos:
                self.cables.add(*self.tender([pts], ROJO_M, 3.0, [n], 0.42))
            self.zoom_fuera(0.5)
            self.play(FadeOut(hl), run_time=0.3)
            self.cerrar_voz(0.1)
        self.wait(0.6)
        self.E, self.puerta = E, VGroup(puerta, lp)
        self.play(FadeOut(d), run_time=0.4)

    # =============================================================== 8 · CONEXIÓN DE POTENCIA
    def h_c_potencia(self):
        if not hasattr(self, "E"):
            self.E = disposicion()
            self.puerta = VGroup()
            self.cables = VGroup()
            self.add(*self.E.values())
        E = self.E
        self.seccion("c_potencia")
        self.voz("p_intro")
        d, P = diagrama_potencia(x0=-6.6, y_top=3.3, dx=0.7)
        d.scale_to_fit_height(7.3).move_to([-4.6, -0.45, 0])
        self.play(FadeIn(d), self.cables.animate.set_stroke(opacity=0.3), run_time=0.8)
        self.cerrar_voz(0.1)
        R = rutas_potencia(E)
        Q1, KM1, F2 = E["Q1"], E["KM1"], E["F2"]

        def tanda(clave, partes, lista, colores=FASE, w=5.0):
            self.voz(clave)
            hl = self.resaltar(partes, P)
            self.play(FadeIn(hl), run_time=0.3)
            hs = self.tender(lista, colores, w, [None] * len(lista), 0.5, "tornillo")
            self.cables.add(*hs)
            self.zoom_fuera(0.5)
            self.play(FadeOut(hl), run_time=0.3)
            self.cerrar_voz(0.1)
        tanda("p1", ["X0", "Q1"], R["p1"])
        tanda("p2", ["Q1", "KM1"], R["p2"])
        # p3: el térmico se acopla al contactor
        self.voz("p3")
        hl = self.resaltar(["F2"], P)
        self.play(FadeIn(hl), run_time=0.3)
        self.zoom(KM1.cuerpo(DOWN), 3.6, 0.6)
        self.play(F2.animate.shift(DOWN * 0.45), run_time=0.4)
        self.play(F2.animate.shift(UP * 0.45), run_time=0.8)
        self.sfx("tornillo", -8)
        anillos = VGroup(*[Circle(radius=0.11, color=AMBAR, stroke_width=4).move_to(KM1.p(t)) for t in ("2/T1", "4/T2", "6/T3")])
        self.play(LaggedStart(*[Create(a) for a in anillos], lag_ratio=0.3), run_time=0.9)
        self.play(FadeOut(anillos), run_time=0.3)
        self.zoom_fuera(0.5)
        self.play(FadeOut(hl), run_time=0.3)
        self.cerrar_voz(0.1)
        tanda("p4", ["F2", "X1"], R["p4"] + [R["pe"]], [FASE, FASE, FASE, "PE"])
        # p5: ajuste del dial a 24,3 A
        self.voz("p5")
        dial = F2.img.get_corner(UL) + RIGHT * (4 + 190 / 685 * 45) * F2.k + DOWN * (4 + 228 / 780 * 51.24) * F2.k
        self.zoom(dial, 2.4, 0.8)
        flecha = Arrow(dial + UR * 0.45, dial + UR * 0.1, color=AMBAR, buff=0, stroke_width=5)
        lab = etiqueta("24,3 A", AMBAR, 22).scale(0.3).next_to(flecha.get_start(), UR, buff=0.02)
        self.sfx("tic", -8)
        self.play(GrowArrow(flecha), FadeIn(lab), run_time=0.6)
        self.cerrar_voz(0.2)
        self.play(FadeOut(flecha), FadeOut(lab), run_time=0.3)
        self.zoom_fuera(0.6)
        self.play(FadeOut(d), self.cables.animate.set_stroke(opacity=1), run_time=0.5)

    # =============================================================== 9 · TABLERO
    def h_tablero(self):
        if not hasattr(self, "E"):
            self.E = disposicion()
            R = rutas_potencia(self.E)
            self.cables = VGroup(*[hilo(p, ROJO_M, 3.0, n, k=0.42) for _, _, hs in rutas_mando(self.E) for p, n in hs],
                                 *[hilo(p, FASE, 5, None, k=0.5) for kk in ("p1", "p2", "p4") for p in R[kk]], hilo(R["pe"], "PE", 5, None, k=0.5))
            self.puerta = VGroup()
            self.add(*self.E.values(), self.cables)
        E = self.E
        self.seccion("tablero")
        self.voz("tablero")
        eqs = Group(*E.values(), self.cables, self.puerta)
        # todo el conjunto pasa al centro, más grande
        self.play(eqs.animate.scale(1.05).move_to([0.2, -0.45, 0]), run_time=1.0)
        izq = min(E[n].cuerpo(LEFT)[0] for n in ("Q1", "KM1", "X0")) - 0.55
        der = E["F1"].cuerpo(RIGHT)[0] + 0.55
        arr, aba = E["Q1"].cuerpo(UP)[1] + 0.55, E["X0"].cuerpo(DOWN)[1] - 0.35
        placa = Rectangle(width=der - izq, height=arr - aba, stroke_width=0).set_fill("#5B6470", 1).move_to([(izq + der) / 2, (arr + aba) / 2, 0])
        borde = Rectangle(width=der - izq + 0.25, height=arr - aba + 0.25, stroke_color="#AEB4BB", stroke_width=6).move_to(placa)
        placa.set_z_index(-5)
        borde.set_z_index(-5)
        puerta = Rectangle(width=E["S1"].cuerpo(RIGHT)[0] - E["B1"].cuerpo(LEFT)[0] + 0.6, height=arr - aba + 0.25, stroke_color="#AEB4BB", stroke_width=6).set_fill("#3F4650", 1)
        puerta.move_to([(E["B1"].cuerpo(LEFT)[0] + E["S1"].cuerpo(RIGHT)[0]) / 2, placa.get_center()[1], 0]).set_z_index(-5)
        self.play(FadeIn(placa), Create(borde), FadeIn(puerta), FadeOut(self.puerta), run_time=0.9)
        # etiquetas de zonas, sincronizadas con la voz
        zonas = [(E["Q1"], "PROTECCIONES", 0.22), (E["KM1"], "MANIOBRA", 0.42), (E["X0"], "BORNERAS", 0.55), (E["B1"], "PUERTA", 0.68)]
        t0 = self.renderer.time
        dur = self.fin_voz - t0
        for e, txt, f in zonas:
            w = t0 + dur * f - self.renderer.time
            if w > 0.05:
                self.wait(w)
            self.sfx("pop", -14)
            et = etiqueta(txt, MARCA, 22).scale(0.8).next_to(e.img, LEFT if e is not E["B1"] else UP, buff=0.1)
            self.play(FadeIn(et, shift=RIGHT * 0.2), Indicate(e, scale_factor=1.04, color=MARCA), run_time=0.6)
            self.add(et)
            self.tab_etq = getattr(self, "tab_etq", VGroup())
            self.tab_etq.add(et)
        self.cerrar_voz(0.3)
        self.play(FadeOut(self.tab_etq), run_time=0.4)
        self.tab = Group(placa, borde, puerta, *E.values(), self.cables)

    # =============================================================== 10 · PUESTA EN MARCHA
    def h_marcha(self):
        if not hasattr(self, "tab"):
            self.h_tablero()
        self.seccion("marcha")
        E = self.E
        self.play(self.tab.animate.scale(0.86).move_to([-2.6, -0.3, 0]), run_time=0.8)
        X2 = E["X2"]
        # prueba en frío
        self.voz("prueba_frio")
        mm = Eq("MM", 0.022).move_to([5.3, -0.2, 0])
        self.play(FadeIn(mm, shift=LEFT * 0.3), run_time=0.6)
        pr = VGroup(cable(mm.p("VΩ"), mm.p("VΩ") + DOWN * 0.5, X2.p("1_b") + DOWN * 0.6 + RIGHT * 0.4, X2.p("1_b"), color=ROJO, w=4, suave=True),
                    cable(mm.p("COM"), mm.p("COM") + DOWN * 0.7, X2.p("3_b") + DOWN * 0.8 + RIGHT * 0.3, X2.p("3_b"), color="#2B2C2E", w=4, suave=True))
        self.play(Create(pr), run_time=1.0)
        lec = etiqueta("MARCHA pulsada → R de la bobina", VERDE_OK, 24).move_to([4.2, 3.4, 0])
        lcd_c = mm.img.get_corner(UL) + RIGHT * (4 + 210 / 420 * mm.d["W"]) * mm.k + DOWN * (4 + 185 / 820 * mm.d["H"]) * mm.k
        tapa = VGroup(Rectangle(width=280 / 420 * mm.d["W"] * mm.k, height=150 / 820 * mm.d["H"] * mm.k, stroke_width=0).set_fill("#C9D1C0", 1),
                      Text("R bobina", font=SANS, font_size=20, weight="BOLD", color="#1B1F24")).move_to(lcd_c)
        tapa[1].scale_to_fit_width(tapa[0].width * 0.8).move_to(tapa[0])
        self.play(Indicate(E["S2"], color=VERDE_OK), FadeIn(lec), FadeIn(tapa), run_time=0.8)
        self.esperar_frac(0.5)
        lec2 = etiqueta("PARO pulsado → OL (abierto)", ROJO, 24).move_to([4.2, 3.4, 0])
        self.play(Indicate(E["S1"], color=ROJO), FadeTransform(lec, lec2), FadeOut(tapa), run_time=0.8)
        self.cerrar_voz(0.2)
        self.play(FadeOut(pr), FadeOut(mm), FadeOut(lec2), run_time=0.4)
        # tensión de llegada
        self.voz("prueba_tension")
        Q1 = E["Q1"]
        self.zoom(Q1.img.get_center(), 3.6, 0.6)
        self.sfx("breaker", -6)
        self.play(Flash(Q1.img.get_center(), color=VERDE_OK, line_length=0.25), run_time=0.5)
        self.zoom_fuera(0.5)
        v = etiqueta("L1-L2 · L2-L3 · L1-L3 = 240 V", AMBAR, 26).move_to([4.2, 3.4, 0])
        self.play(FadeIn(v), run_time=0.5)
        self.cerrar_voz(0.2)
        # marcha
        self.voz("marcha")
        self.sfx("breaker", -6)
        self.play(Flash(E["F1"].img.get_center(), color=VERDE_OK, line_length=0.25), FadeOut(v), run_time=0.5)
        self.play(Indicate(E["S2"], color=VERDE_OK, scale_factor=1.1), run_time=0.6)
        self.sfx("contactor", -6)
        self.play(Indicate(E["KM1"], color=AMBAR, scale_factor=1.04), run_time=0.5)
        mo = Eq("M1", 0.016).move_to([5.0, 0.4, 0])
        self.play(FadeIn(mo), run_time=0.4)
        self.sfx("motor", -8)
        giro = VGroup(*[Arc(radius=0.22 + 0.1 * i, start_angle=i, angle=PI * 1.2, stroke_width=3).set_stroke(MARCA, opacity=0.9 - 0.25 * i) for i in range(3)])
        giro.move_to(mo.img.get_left() + RIGHT * 0.12)
        self.add(giro)
        giro.add_updater(lambda m, dt: m.rotate(-dt * 6))
        self.cerrar_voz(0.1)
        # corriente con la pinza
        self.voz("corriente")
        pz = Eq("PZ", 0.013).move_to([5.0, -2.3, 0])
        nota = T("lectura de ejemplo", 18, TXT2, "MEDIUM").next_to(pz, LEFT, buff=0.15)
        self.play(FadeIn(pz, shift=LEFT * 0.3), FadeIn(nota), run_time=0.6)
        ok = etiqueta("< 24,3 A de placa  ✓", VERDE_OK, 26).move_to([4.2, 3.4, 0])
        self.play(FadeIn(ok), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(FadeOut(pz), FadeOut(nota), FadeOut(ok), run_time=0.4)
        # disparo del térmico
        self.voz("disparo")
        F2 = E["F2"]
        self.zoom(F2.img.get_center(), 3.2, 0.6)
        self.sfx("disparo", -4)
        self.play(Flash(F2.img.get_center() + LEFT * 0.3, color=ROJO, line_length=0.2), run_time=0.5)
        self.zoom_fuera(0.5)
        self.sfx("motor_para", -8)
        giro.clear_updaters()
        x = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(ROJO, 10).scale(0.45).move_to(mo)
        self.play(FadeOut(giro), Create(x), run_time=0.8)
        self.esperar_frac(0.45)
        self.play(Indicate(E["S2"], color=VERDE_OK), run_time=0.6)
        no = etiqueta("no arranca", ROJO, 24).move_to([4.2, 3.4, 0])
        self.play(FadeIn(no), run_time=0.4)
        self.esperar_frac(0.6)
        rs = etiqueta("RESET → listo para arrancar", C_S, 24).move_to([4.2, 3.4, 0])
        self.play(FadeTransform(no, rs), FadeOut(x), run_time=0.6)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 11 · CIERRE
    def h_cierre(self):
        self.seccion("cierre")
        self.voz("cierre")
        lg = ImageMobject(str(LOGO)).scale_to_fit_width(2.6).move_to([4.3, 1.5, 0])
        us = T("@miguelesquit", 36, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        yt = pastilla("SUSCRÍBETE", ROJO, 34, True)
        sig = T(self.PROXIMO, 32, TXT, "HEAVY").move_to([-3.6, 3.0, 0])
        caja = RoundedRectangle(width=6.4, height=3.6, corner_radius=0.15, stroke_color=MARCA, stroke_width=2).set_fill(CARTA, 1).move_to([-3.6, 0.6, 0])
        caja = VGroup(caja, VGroup(T("ARRANQUE CON", 34, TXT, "HEAVY"), T("VARIADOR DE FRECUENCIA", 34, MARCA, "HEAVY")).arrange(DOWN, buff=0.2).move_to(caja))
        shorts = VGroup(*[VGroup(RoundedRectangle(width=1.9, height=1.6, corner_radius=0.1, stroke_color=AMBAR, stroke_width=2).set_fill(CARTA, 1),
                                 Paragraph(*t, font=SANS, font_size=16, color=TXT, alignment="center")) for t in
                          (["Así funciona", "la retención"], ["Así se calcula", "la protección"], ["Así funciona", "el térmico"])]).arrange(RIGHT, buff=0.2)
        for s in shorts:
            s[1].move_to(s[0])
        shorts.move_to([-3.6, -2.6, 0])
        ls = T("SHORTS", 24, AMBAR, "HEAVY").next_to(shorts, UP, buff=0.12)
        yt.next_to(us, DOWN, buff=0.4)
        self.play(FadeIn(sig), FadeIn(caja, shift=UP * 0.2), FadeIn(lg, scale=0.8), FadeIn(us), run_time=0.7)
        self.play(FadeIn(yt, scale=1.2), run_time=0.5)
        self.esperar_frac(0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in shorts], lag_ratio=0.2), FadeIn(ls), run_time=0.9)
        self.cerrar_voz(0.2)
        self.wait(6.0)

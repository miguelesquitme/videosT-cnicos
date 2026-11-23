"""H01 v3 · Conexión didáctica (Correcciones_V7, puntos 7-9 y 12).
- Sin plancha: los equipos sobre el fondo gris claro; arriba protecciones y contactor (el contactor con el relé térmico
  debajo, como en el diagrama), abajo las borneras sobre su riel DIN. A la derecha, la parte trasera de la puerta.
- Cada cable entra a su borne POR DEBAJO DEL PLÁSTICO: la puntera (collar de color DIN 46228-4) llega al borde del
  equipo frente al tornillo y el pin metálico queda escondido; el tornillo se ve encima. Marcador blanco con el número.
- Cables SIN borde (solo un cable blanco lo llevaría para no perderse en el fondo).
Bocas de entrada medidas en la biblioteca (mm del cuerpo): ver ENTRADAS."""
import json
import numpy as np
from comun_e import *          # noqa: F401,F403

EQ3 = DIR / "h01v3_eq"
K = 0.026                       # tablero didáctico: unidades por mm
KD = 0.036                      # bloques traseros de la puerta
KF = 0.019                      # frente de los operadores

ROJO_M = "#D92D20"
NEUTRO_C = "#5DB4F0"
NEGRO_P = "#161616"
PE_V, PE_A = "#1E9E3E", "#F2D21B"
COLLAR = {"mando": "#2F6FD0", "pot": "#C8202B"}       # 2,5 mm² azul · 10 mm² rojo (DIN 46228-4)
W_CABLE = {"mando": 5.0, "pot": 9.0}

# bocas: (x_mm, y_mm, dirección hacia afuera) en coordenadas del cuerpo del equipo
_S = 45 / 602          # contactor mm/px
_T = 45 / 685          # relé térmico mm/px
ENTRADAS = {
    "F2": {"1": (9.26, 0, "u"), "3": (27.26, 0, "u"), "5": (45.26, 0, "u"), "2": (9.26, 80.57, "d"), "4": (27.26, 80.57, "d"), "6": (45.26, 80.57, "d")},
    "F1": {"1": (9.26, 0, "u"), "2": (9.26, 80.57, "d")},
    "KM1": {"1/L1": (8.45, 0, "u"), "3/L2": (22.65, 0, "u"), "5/L3": (37.15, 0, "u"),
            "13": (0.45, 16.82, "l"), "21": (28.26, 172 * _S, "u"), "A1": (45.0, 16.82, "r"),
            "14": (0.45, 55.17, "l"), "22": (28.26, 795 * _S, "d"), "A2": (45.0, 55.17, "r")},
    "F3": {"2/T1": (9.2, 51.24, "d"), "4/T2": (22.47, 51.24, "d"), "6/T3": (35.8, 51.24, "d"),
           "95": (45.0, 32.52, "r"), "96": (27.92, 587 * _T, "d")},
    "X0": {f"{i}_a": (13.26 + 10.2 * (i - 1), 0, "u") for i in range(1, 6)} | {f"{i}_b": (13.26 + 10.2 * (i - 1), 51.0, "d") for i in range(1, 6)},
    "X1": {f"{i}_a": (13.26 + 10.2 * (i - 1), 0, "u") for i in range(1, 5)} | {f"{i}_b": (13.26 + 10.2 * (i - 1), 51.0, "d") for i in range(1, 5)},
}
for _b, (_n1, _n2) in {"S0b": ("1", "2"), "S1b": ("3", "4"), "H1b": ("X1", "X2"), "H2b": ("X1", "X2")}.items():
    ENTRADAS[_b] = {_n1: (8.02, 1.05, "u"), _n2: (8.02, 28.26, "d")}
DIRS = {"u": UP, "d": DOWN, "l": LEFT, "r": RIGHT}


class Eq3(Group):
    def __init__(self, nombre, k=K, base=None):
        d = json.loads((EQ3 / f"{nombre}.json").read_text())
        img = ImageMobject(str(EQ3 / f"{nombre}.png"))
        img.height = (d["H"] + 2 * d["margen"]) * k
        super().__init__(img)
        self.img, self.d, self.k, self.nombre = img, d, k, nombre
        self.base = base or (nombre[:-2] if nombre.endswith(("on", "tr")) else nombre[:-1] if nombre in ("S0p", "S1p") else nombre)

    def mm(self, x, y):
        m = self.d["margen"]
        return self.img.get_corner(UL) + RIGHT * (m + x) * self.k + DOWN * (m + y) * self.k

    def p(self, b):
        x, y = self.d["bornes"][b]
        return self.mm(x, y)

    def boca(self, b, clave=None):
        x, y, d = ENTRADAS[clave or self.base][b]
        return self.mm(x, y), DIRS[d]

    def borde(self, lado):
        m = self.d["margen"] * self.k
        c = self.img.get_center()
        h, w = self.img.height / 2 - m, self.img.width / 2 - m
        return {"u": c[1] + h, "d": c[1] - h, "l": c[0] - w, "r": c[0] + w}[lado]

    def poner(self, x_izq, y_arr):
        m = self.d["margen"] * self.k
        self.img.move_to([x_izq + self.img.width / 2 - m, y_arr - self.img.height / 2 + m, 0])
        return self


def ruta_redondeada(pts, r=0.13):
    pts = [np.array(p, float) for p in pts]
    limpio = [pts[0]]
    for q in pts[1:]:
        if np.linalg.norm(q - limpio[-1]) > 1e-6:
            limpio.append(q)
    pts = limpio
    m = VMobject()
    m.start_new_path(pts[0])
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        l1, l2 = np.linalg.norm(b - a), np.linalg.norm(c - b)
        rr = min(r, l1 / 2, l2 / 2)
        m.add_line_to(b - (b - a) / l1 * rr)
        m.add_quadratic_bezier_curve_to(b, b + (c - b) / l2 * rr)
    m.add_line_to(pts[-1])
    return m


def puntera(E, d, clase, k):
    """Collar aislado de la puntera (lo único que se ve: el pin metálico entra bajo el plástico del equipo).
    Forma real: manguito recto con el embudo un poco más ancho del lado del cable."""
    perp = np.array([-d[1], d[0], 0])
    ancho = {"mando": 0.048, "pot": 0.085}[clase] * (k / K) ** 0.5
    largo = {"mando": 0.085, "pot": 0.13}[clase] * (k / K) ** 0.5
    col = COLLAR[clase]
    p0 = E - d * 0.004
    p1 = E + d * largo * 0.72
    p2 = E + d * largo
    cuerpo = Polygon(p0 - perp * ancho / 2, p0 + perp * ancho / 2, p1 + perp * ancho / 2, p1 - perp * ancho / 2).set_fill(col, 1).set_stroke(width=0)
    embudo = Polygon(p1 - perp * ancho * 0.62, p1 + perp * ancho * 0.62, p2 + perp * ancho * 0.66, p2 - perp * ancho * 0.66).set_fill(col, 1).set_stroke(width=0)
    brillo = Polygon(p0 - perp * ancho * 0.28, p0 - perp * ancho * 0.12, p1 - perp * ancho * 0.12, p1 - perp * ancho * 0.28).set_fill(WHITE, 0.35).set_stroke(width=0)
    sombra = Polygon(p0 + perp * ancho * 0.30, p0 + perp * ancho / 2, p2 + perp * ancho * 0.66, p2 + perp * ancho * 0.40).set_fill(BLACK, 0.25).set_stroke(width=0)
    return fisico(VGroup(cuerpo, embudo, brillo, sombra)), largo


class Cable3(Group):
    """a, b = (punto de boca, dirección hacia afuera). medio = puntos intermedios de la ruta."""

    def __init__(self, a, b, medio, color, clase, num, ka=K, kb=K, marcador=True, L0=0.2):
        super().__init__()
        (A, da), (B, db) = a, b
        w = W_CABLE[clase] * ((ka + kb) / 2 / K) ** 0.5
        pa, la = puntera(A, da, clase, ka)
        pb, lb = puntera(B, db, clase, kb)
        ini, fin = A + da * la, B + db * lb
        pts = [ini, A + da * (la + L0)] + [np.array(p, float) for p in medio] + [B + db * (lb + L0), fin]
        base = ruta_redondeada(pts)
        if color == "PE":
            capa = VGroup(base.copy().set_stroke(PE_V, w),
                          DashedVMobject(base.copy(), num_dashes=max(4, int(base.get_arc_length() / 0.08)), dashed_ratio=0.5).set_stroke(PE_A, w))
        elif color == "#FFFFFF":
            capa = VGroup(base.copy().set_stroke("#98A2B3", w + 2), base.copy().set_stroke(color, w))
        else:
            capa = VGroup(base.copy().set_stroke(color, w))
        for s in capa.family_members_with_points():
            s.set_fill(opacity=0)
        self.conductor = fisico(capa)
        self.puntas = Group()
        for P0, d, larg, pu in ((A, da, la, pa), (B, db, lb, pb)):
            g = Group(pu)
            if marcador and num is not None:
                t = Text(str(num), font=SANS, font_size=40, weight="BOLD", color="#111111")
                t.scale_to_fit_height(0.045 if clase == "mando" else 0.06)
                vertical = abs(d[1]) > abs(d[0])
                if vertical:
                    t.rotate(PI / 2)
                largo = max(t.height if vertical else t.width, 0.06) + 0.03
                grosor = w / 100 * 2.0
                caja = Rectangle(width=grosor if vertical else largo, height=largo if vertical else grosor, stroke_width=1, stroke_color="#9AA0A6").set_fill(WHITE, 1)
                c0 = P0 + d * (larg + 0.025 + largo / 2)
                caja.move_to(c0)
                t.move_to(c0)
                g.add(fisico(VGroup(caja, t)))
            self.puntas.add(g)
        self.add(self.conductor, self.puntas)
        self.conductor.set_z_index(6)
        for g in self.puntas:
            for sm in g:
                sm.set_z_index(7)
        self.ruta = base


# ------------------------------------------------------------------------------ disposición didáctica
def disposicion():
    E = {}
    x0, y0 = -1.05, 3.55
    F2 = E["F2"] = Eq3("F2").poner(x0, y0)
    E["F1"] = Eq3("F1").poner(F2.borde("r") + 0.28, y0)
    x_km = F2.borde("l") + (27.26 - 22.65) * K          # polos del contactor alineados con los del breaker
    KM1 = E["KM1"] = Eq3("KM1").poner(x_km, F2.borde("d") - 0.42)
    F3 = E["F3"] = Eq3("F3").poner(x_km + (22.65 - 22.47) * K, KM1.borde("d"))
    KM1.set_z_index(2)
    F3.set_z_index(1)
    yx = F3.borde("d") - 0.62
    E["X0"] = Eq3("X0").poner(-1.25, yx)
    E["X1"] = Eq3("X1").poner(E["X0"].borde("r") + 0.30, yx)
    # puerta (vista trasera): frente arriba para reconocerlo y su bloque de contacto abajo, en una sola fila
    for i, n in enumerate(("S0", "S1", "H1", "H2")):
        x = 4.05 + 1.0 * i
        E[n] = Eq3(n, KF)
        E[n].img.move_to([x + 0.435, 3.05, 0])
        E[n + "b"] = Eq3(n + "b", KD).poner(x, 2.20)
    return E


def riel_din(E, k=K):
    """Riel DIN 35 mm (EN 60715) bajo las borneras."""
    X0, X1 = E["X0"], E["X1"]
    yc = (X0.borde("u") + X0.borde("d")) / 2
    x0, x1 = X0.borde("l") - 0.25, X1.borde("r") + 0.25
    r = Rectangle(width=x1 - x0, height=35 * k, stroke_width=0).set_fill("#C9CED4", 1).move_to([(x0 + x1) / 2, yc, 0])
    lab = VGroup(Rectangle(width=x1 - x0, height=7.5 * k, stroke_width=0).set_fill("#E7EAED", 1).move_to(r.get_top() + DOWN * 3.75 * k),
                 Rectangle(width=x1 - x0, height=7.5 * k, stroke_width=0).set_fill("#A9B0B8", 1).move_to(r.get_bottom() + UP * 3.75 * k))
    ran = VGroup(*[RoundedRectangle(width=15 * k, height=5.2 * k, corner_radius=2.5 * k, stroke_width=0).set_fill("#7E858C", 1).move_to([x, yc, 0])
                   for x in np.arange(x0 + 0.25, x1 - 0.1, 25 * k)])
    return VGroup(r, lab, ran)


def puerta_marco(E):
    xs = [E[n].borde(l) for n in ("S0b", "H2b") for l in ("l", "r")]
    ys = [E[n].borde(l) for n in ("S0", "S0b") for l in ("u", "d")]
    m = DashedVMobject(Rectangle(width=max(xs) - min(xs) + 0.4, height=max(ys) - min(ys) + 0.55), num_dashes=60).set_stroke("#667085", 2)
    m.move_to([(max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2 - 0.08, 0])
    t = T("PUERTA · vista trasera", 18, "#475467", "HEAVY").next_to(m, UP, buff=0.06).align_to(m, LEFT)
    return VGroup(m, t)


def canales(E):
    F2, F1, KM1, F3, X0 = E["F2"], E["F1"], E["KM1"], E["F3"], E["X0"]
    return dict(
        yA=F2.borde("u") + 0.22,                                # arriba de los breakers
        yB=(F2.borde("d") + KM1.borde("u")) / 2,                # entre breakers y contactor
        yD=F3.borde("d") - 0.16,                                # debajo del térmico
        xL=KM1.borde("l") - 0.22,                               # izquierda del contactor
        xR=KM1.borde("r") + 0.22,                               # derecha del contactor (debajo de -F1)
        xP=E["S0b"].borde("l") - 0.25,                          # bajada hacia la puerta
        yS=KM1.borde("d") + 0.04,                               # junta contactor / térmico
        yG=(E["S0"].borde("d") + E["S0b"].borde("u")) / 2,      # entre frentes y bloques (bocas de arriba)
        yU=E["S0b"].borde("d") - 0.22,                          # debajo de los bloques (bocas de abajo)
    )


def hilos_mando(E):
    """[(clave de voz, [Cable3…], [claves de marca en el diagrama])]"""
    c = canales(E)
    F2, F1, KM1, F3, X0 = E["F2"], E["F1"], E["KM1"], E["F3"], E["X0"]
    S0, S1, H1, H2 = E["S0b"], E["S1b"], E["H1b"], E["H2b"]
    R, N = ROJO_M, NEUTRO_C
    yA, yB, yD, xL, xR, xP, yS, yG, yU = (c[k] for k in ("yA", "yB", "yD", "xL", "xR", "xP", "yS", "yG", "yU"))
    def C(a, b, medio, col, num, ka=K, kb=K):
        return Cable3(a, b, medio, col, "mando", num, ka, kb)
    def gap(bl):                       # pasillo a la derecha de cada bloque de la puerta
        return bl.borde("r") + 0.065
    H = []
    a, b = F2.boca("1"), F1.boca("1")
    H.append(("c1", [C(a, b, [[a[0][0], yA + 0.02, 0], [b[0][0], yA + 0.02, 0]], R, "1")], ["1"]))
    a, b, e = F1.boca("2"), F3.boca("95"), KM1.boca("21")
    H.append(("c2", [C(a, b, [[a[0][0], yB - 0.05, 0], [xR, yB - 0.05, 0], [xR, b[0][1], 0]], R, "2"),
                     C(b, e, [[xR + 0.08, b[0][1] - 0.05, 0], [xR + 0.08, yB + 0.05, 0], [e[0][0], yB + 0.05, 0]], R, "2")], ["2"]))
    a, b = F3.boca("96"), S0.boca("1")
    H.append(("c3", [C(a, b, [[a[0][0], yD, 0], [xP, yD, 0], [xP, yG, 0], [b[0][0], yG, 0]], R, "3", K, KD)], ["3"]))
    a, b, e = S0.boca("2"), S1.boca("3"), KM1.boca("13")
    H.append(("c4", [C(a, b, [[a[0][0] + 0.06, yU, 0], [gap(S0), yU, 0], [gap(S0), yG, 0], [b[0][0], yG, 0]], R, "4", KD, KD),
                     C(a, e, [[a[0][0] - 0.06, yU - 0.06, 0], [xP + 0.07, yU - 0.06, 0], [xP + 0.07, yB + 0.12, 0], [xL, yB + 0.12, 0], [xL, e[0][1], 0]], R, "4", KD, K)], ["4"]))
    a, b, a1, h1 = S1.boca("4"), KM1.boca("14"), KM1.boca("A1"), H1.boca("X1")
    H.append(("c5", [C(a, b, [[a[0][0] - 0.06, yU - 0.12, 0], [xP + 0.14, yU - 0.12, 0], [xP + 0.14, yB + 0.19, 0], [xL - 0.07, yB + 0.19, 0], [xL - 0.07, b[0][1], 0]], R, "5", KD, K),
                     C(b, a1, [[xL - 0.14, b[0][1] - 0.05, 0], [xL - 0.14, yB + 0.26, 0], [xR + 0.16, yB + 0.26, 0], [xR + 0.16, a1[0][1], 0]], R, "5"),
                     C(a, h1, [[a[0][0] + 0.06, yU, 0], [gap(S1), yU, 0], [gap(S1), yG, 0], [h1[0][0], yG, 0]], R, "5", KD, KD)], ["5"]))
    a, b = KM1.boca("22"), H2.boca("X1")
    H.append(("c6", [C(a, b, [[a[0][0], yS, 0], [xR + 0.24, yS, 0], [xR + 0.24, yB - 0.12, 0], [xP + 0.21, yB - 0.12, 0], [xP + 0.21, yG + 0.07, 0], [b[0][0], yG + 0.07, 0]], R, "6", K, KD)], ["6"]))
    a, b, h1, h2 = X0.boca("4_a"), KM1.boca("A2"), H1.boca("X2"), H2.boca("X2")
    H.append(("c7", [C(a, b, [[a[0][0], yD - 0.12, 0], [xR + 0.32, yD - 0.12, 0], [xR + 0.32, b[0][1], 0]], N, "N"),
                     C(b, h1, [[xR + 0.40, b[0][1] - 0.05, 0], [xR + 0.40, yB - 0.20, 0], [xP + 0.28, yB - 0.20, 0], [xP + 0.28, yU - 0.20, 0], [h1[0][0] - 0.06, yU - 0.20, 0]], N, "N", K, KD),
                     C(h1, h2, [[h1[0][0] + 0.06, yU - 0.27, 0], [h2[0][0], yU - 0.27, 0]], N, "N", KD, KD)], ["N"]))
    return H


def hilos_potencia(E):
    c = canales(E)
    F2, KM1, F3, X0, X1 = E["F2"], E["KM1"], E["F3"], E["X0"], E["X1"]
    yA, yB, yD = c["yA"], c["yB"], c["yD"]
    T_ = {}
    T_["p1"] = []
    xi = X0.borde("l") - 0.12
    for i, (b, t, nm) in enumerate((("1_a", "1", "L1"), ("2_a", "3", "L2"), ("3_a", "5", "L3"))):
        a, z = X0.boca(b), F2.boca(t)
        T_["p1"].append(Cable3(a, z, [[a[0][0], a[0][1] + 0.30 + 0.12 * (2 - i), 0], [xi - 0.13 * (2 - i), a[0][1] + 0.30 + 0.12 * (2 - i), 0],
                                      [xi - 0.13 * (2 - i), yA + 0.18 + 0.12 * i, 0], [z[0][0], yA + 0.18 + 0.12 * i, 0]], NEGRO_P, "pot", nm))
    T_["p2"] = []
    for t, u, nm in (("2", "1/L1", "L1"), ("4", "3/L2", "L2"), ("6", "5/L3", "L3")):
        a, z = F2.boca(t), KM1.boca(u)
        T_["p2"].append(Cable3(a, z, [[a[0][0], yB - 0.02, 0], [z[0][0], yB - 0.02, 0]], NEGRO_P, "pot", nm, L0=0.08))
    T_["p4"] = []
    for i, (t, u, nm) in enumerate((("2/T1", "1_a", "T1"), ("4/T2", "2_a", "T2"), ("6/T3", "3_a", "T3"))):
        a, z = F3.boca(t), X1.boca(u)
        yy = F3.borde("d") - 0.22 - 0.11 * (2 - i)
        T_["p4"].append(Cable3(a, z, [[a[0][0], yy, 0], [z[0][0], yy, 0]], NEGRO_P, "pot", nm, L0=0.08))
    a, z = X0.boca("5_a"), X1.boca("4_a")
    yy = X0.borde("u") + 0.20
    T_["pe"] = [Cable3(a, z, [[a[0][0], yy, 0], [z[0][0], yy, 0]], "PE", "pot", "PE", L0=0.08)]
    return T_

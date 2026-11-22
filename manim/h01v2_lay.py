"""H01 v2 · Disposición física de los equipos y rutas de los cables (equipos de la biblioteca svgref, PNG en h01v2_eq/).
Cada cable: ruta con esquinas REDONDEADAS, puntera (pin metálico + collar DIN 46228-4) que entra DEBAJO del tornillo,
marcador blanco con el número IEC del hilo, y la cabeza del tornillo dibujada encima del pin.
Reglas de acceso (corrección del usuario, image11): 95/96 del térmico se alcanzan por ABAJO; la fila superior de
auxiliares del contactor: 13 desde la izquierda, 21 desde arriba, A1 desde la derecha; la inferior: 14 desde la
izquierda, 22 desde abajo (entre filas), A2 desde la derecha. Ningún cable cruza la cara de un equipo salvo para
llegar a su borne."""
import json
import numpy as np
from comun_e import *          # noqa: F401,F403  (DIR, fisico, T, …)

EQ2 = DIR / "h01v2_eq"
K = 0.026                       # unidades de escena por mm (equipos del tablero)
KD = 0.034                      # puerta (bloques de contacto)
KF = 0.034                      # frentes de la puerta

ROJO_M = "#E0262B"              # mando AC (IEC 60204-1)
NEUTRO_C = "#7FC4F0"            # neutro azul claro
NEGRO_P = "#161616"             # potencia
PE_V, PE_A = "#1E9E3E", "#F2D21B"
# collar de la puntera (DIN 46228-4): 2,5 mm² azul · 10 mm² rojo
COLLAR = {"mando": "#2F6FD0", "pot": "#C8202B"}
W_CABLE = {"mando": 6.0, "pot": 11.0}


class Eq2(Group):
    def __init__(self, nombre, k=K):
        d = json.loads((EQ2 / f"{nombre}.json").read_text())
        img = ImageMobject(str(EQ2 / f"{nombre}.png"))
        img.height = (d["H"] + 2 * d["margen"]) * k
        super().__init__(img)
        self.img, self.d, self.k, self.nombre = img, d, k, nombre

    def p(self, b):
        x, y = self.d["bornes"][b]
        m = self.d["margen"]
        return self.img.get_corner(UL) + RIGHT * (m + x) * self.k + DOWN * (m + y) * self.k

    def mm(self, x, y):
        m = self.d["margen"]
        return self.img.get_corner(UL) + RIGHT * (m + x) * self.k + DOWN * (m + y) * self.k

    def borde(self, lado):
        m = self.d["margen"] * self.k
        c = self.img.get_center()
        h, w = self.img.height / 2 - m, self.img.width / 2 - m
        return {"u": c[1] + h, "d": c[1] - h, "l": c[0] - w, "r": c[0] + w}[lado]

    def poner(self, x_izq, y_arr):
        m = self.d["margen"] * self.k
        self.img.move_to([x_izq + self.img.width / 2 - m, y_arr - self.img.height / 2 + m, 0])
        return self


# radio de la cabeza del tornillo de cada equipo (mm, de la biblioteca) y tipo
TORN = {"F2": (4.3, "cruz"), "F1": (4.3, "cruz"), "KM1p": (3.36, "cruz"), "KM1a": (2.47, "cruz"), "F3a": (2.37, "cruz"),
        "F3p": (3.28, "cruz"), "X": (3.06, "ranura"), "B": (2.3, "cruz")}


def cabeza(p, r, tipo):
    """Cabeza del tornillo dibujada ENCIMA de la puntera: así se ve que el pin queda debajo del tornillo."""
    if tipo == "ranura":
        g = VGroup(Circle(radius=r).set_fill("#B4B4B0", 1).set_stroke("#0A0A0B", r * 30),
                   Line([-0.7 * r, -0.7 * r, 0], [0.7 * r, 0.7 * r, 0]).set_stroke("#050506", r * 75))
    else:
        g = VGroup(Circle(radius=r).set_fill("#E8EDF1", 1).set_stroke("#AEB9C2", r * 12),
                   Circle(radius=r * 0.8).set_fill("#D2DAE0", 1).set_stroke(width=0),
                   Rectangle(width=1.2 * r, height=0.3 * r, stroke_width=0).set_fill("#22495A", 1),
                   Rectangle(width=0.3 * r, height=1.2 * r, stroke_width=0).set_fill("#22495A", 1))
    return fisico(g.move_to(p))


def ruta_redondeada(pts, r=0.14):
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
        p1 = b - (b - a) / l1 * rr
        p2 = b + (c - b) / l2 * rr
        m.add_line_to(p1)
        m.add_quadratic_bezier_curve_to(b, p2)
    m.add_line_to(pts[-1])
    return m


class Cable(Group):
    """Cable completo: conductor (ruta redondeada) + en cada punta puntera, collar, marcador y cabeza del tornillo."""

    def __init__(self, pts, color, clase, num, torn_a, torn_b, k=K, kb=None, marcador=True):
        super().__init__()
        pts = [np.array(p, float) for p in pts]
        ka = k
        kb = kb or k
        w = W_CABLE[clase] * (k / K)
        lm = {"mando": 0.075, "pot": 0.12}[clase]          # largo del pin metálico
        lc = {"mando": 0.06, "pot": 0.09}[clase]           # collar aislado
        # recortar la ruta para que el conductor termine en el collar
        def recorta(p0, p1, L):
            d = (p1 - p0) / np.linalg.norm(p1 - p0)
            return p0 + d * L, d
        a_fin, da = recorta(pts[0], pts[1], lm + lc)
        b_fin, db = recorta(pts[-1], pts[-2], lm + lc)
        ruta = [a_fin] + pts[1:-1] + [b_fin]
        base = ruta_redondeada(ruta)
        if color == "PE":
            capa = VGroup(base.copy().set_stroke("#0E3B1A", w + 2.5), base.copy().set_stroke(PE_V, w),
                          DashedVMobject(base.copy(), num_dashes=max(4, int(base.get_arc_length() / 0.09)), dashed_ratio=0.5).set_stroke(PE_A, w))
        else:
            borde = "#000000" if color != NEGRO_P else "#80868D"
            capa = VGroup(base.copy().set_stroke(borde, w + 2.5), base.copy().set_stroke(color, w))
        for s in capa.family_members_with_points():
            s.set_fill(opacity=0)
        self.conductor = fisico(capa)
        self.puntas = Group()
        def a_lo_largo(seq, dist):
            """Punto y dirección a 'dist' del borne, siguiendo la ruta (para que el marcador no caiga sobre otro borne)."""
            for p0, p1 in zip(seq, seq[1:]):
                L = np.linalg.norm(p1 - p0)
                if dist <= L - 0.02 or p1 is seq[-1]:
                    dd = (p1 - p0) / L
                    return p0 + dd * min(dist, L), dd
                dist -= L
            return seq[-1], (seq[-1] - seq[-2]) / np.linalg.norm(seq[-1] - seq[-2])
        for P0, d, (rt, tt), kk, seq in ((pts[0], da, torn_a, ka, pts), (pts[-1], db, torn_b, kb, pts[::-1])):
            perp = np.array([-d[1], d[0], 0])
            ancho_pin = {"mando": 0.03, "pot": 0.05}[clase]
            pin = Polygon(P0 - perp * ancho_pin / 2, P0 + perp * ancho_pin / 2, P0 + d * lm + perp * ancho_pin / 2, P0 + d * lm - perp * ancho_pin / 2)
            pin.set_fill("#C9CDD2", 1).set_stroke("#7E848B", 1)
            ca = w / 100 * 1.5
            col = Polygon(P0 + d * lm - perp * ca / 2, P0 + d * lm + perp * ca / 2, P0 + d * (lm + lc) + perp * ca * 0.4, P0 + d * (lm + lc) - perp * ca * 0.4)
            col.set_fill(COLLAR[clase], 1).set_stroke("#000000", 1)
            g = Group(fisico(VGroup(pin, col)))
            if marcador and num is not None:
                t = Text(str(num), font=SANS, font_size=40, weight="BOLD", color="#111111")
                t.scale_to_fit_height(0.05 if clase == "mando" else 0.065)
                largo0 = 0.11
                c0, dm = a_lo_largo(seq, lm + lc + 0.03 + largo0 / 2)
                vertical = abs(dm[1]) > abs(dm[0])
                if vertical:
                    t.rotate(PI / 2)
                largo = max(t.height if vertical else t.width, 0.07) + 0.035
                grosor = w / 100 * 1.9
                caja = Rectangle(width=grosor if vertical else largo, height=largo if vertical else grosor, stroke_width=1, stroke_color="#555555").set_fill(WHITE, 1)
                caja.move_to(c0)
                t.move_to(c0)
                g.add(fisico(VGroup(caja, t)))
            g.add(cabeza(P0, rt * kk, tt))
            self.puntas.add(g)
        self.add(self.conductor, self.puntas)
        self.conductor.set_z_index(6)
        for g in self.puntas:
            for i, sm in enumerate(g):
                sm.set_z_index(7 + i)
        self.ruta = base


# ---------------------------------------------------------------------------------- disposición
def disposicion():
    E = {}
    y0 = 3.75
    F2 = E["F2"] = Eq2("F2").poner(0.50, y0)
    F1 = E["F1"] = Eq2("F1").poner(F2.borde("r") + 0.25, y0)
    x_km = F2.borde("l") + (27.3 - 22.6) * K
    KM1 = E["KM1"] = Eq2("KM1").poner(x_km, F2.borde("d") - 0.50)
    F3 = E["F3"] = Eq2("F3").poner(x_km + (22.6 - 22.5) * K, KM1.borde("d"))
    KM1.set_z_index(2)
    F3.set_z_index(1)
    yx = F3.borde("d") - 0.95
    E["X0"] = Eq2("X0").poner(-0.65, yx)
    E["X1"] = Eq2("X1").poner(E["X0"].borde("r") + 0.35, yx)
    # puerta: bloques de contacto (punto de conexión) a la izquierda y el frente del operador a la derecha
    xb = 4.40
    filas = [("S0", 3.70), ("S1", 1.75), ("H1", -0.20), ("H2", -2.15)]
    for n, y in filas:
        E[n + "b"] = Eq2(n + "b", KD).poner(xb, y)
        E[n] = Eq2(n, KF).poner(xb + 1.40, y + 0.05)
    return E


def canales(E):
    F2, F1, KM1, F3, X0 = E["F2"], E["F1"], E["KM1"], E["F3"], E["X0"]
    return dict(
        yA=F2.borde("u") + 0.24,                              # canaleta superior
        yB=(F2.borde("d") + KM1.borde("u")) / 2,              # entre breakers y contactor
        yD=F3.borde("d") - 0.12,                              # primera ranura de la franja entre térmico y borneras
        xL=KM1.borde("l") - 0.20,                             # izquierda del contactor
        xR=KM1.borde("r") + 0.22,                             # derecha del contactor
        xI=X0.borde("l") - 0.30,                              # subida de la potencia
        xP=3.95,                                              # mazo de la puerta
        yG=KM1.p("22")[1] - 0.115,                            # entre la fila inferior de auxiliares y 2/T1
        yQ=F3.p("95")[1] - 0.135,                             # debajo de 95/96 (acceso por abajo)
    )


def hilos_mando(E):
    """[(clave de voz, [(pts, color, num, torn_a, torn_b, ka, kb)], [claves de marca en el diagrama])]"""
    c = canales(E)
    F2, F1, KM1, F3, X0 = E["F2"], E["F1"], E["KM1"], E["F3"], E["X0"]
    S0, S1, H1, H2 = E["S0b"], E["S1b"], E["H1b"], E["H2b"]
    tF2, tKa, tF3a, tX, tB = TORN["F2"], TORN["KM1a"], TORN["F3a"], TORN["X"], TORN["B"]
    R, N = ROJO_M, NEUTRO_C
    yA, yB, yD, xL, xR, xP, yG, yQ = (c[k] for k in ("yA", "yB", "yD", "xL", "xR", "xP", "yG", "yQ"))
    def P(e, b):
        return e.p(b)
    H = []
    a, b = P(F2, "1"), P(F1, "1")
    H.append(("c1", [([a, [a[0] + 0.10, yA, 0], [b[0], yA, 0], b], R, "1", tF2, tF2, K, K)], ["1"]))
    a, b, e = P(F1, "2"), P(F3, "95"), P(KM1, "21")
    H.append(("c2", [([a, [a[0], yB + 0.05, 0], [xR + 0.06, yB + 0.05, 0], [xR + 0.06, yQ, 0], [b[0], yQ, 0], b], R, "2", tF2, tF3a, K, K),
                     ([b, [b[0], yQ - 0.05, 0], [xR + 0.12, yQ - 0.05, 0], [xR + 0.12, yB - 0.05, 0], [e[0], yB - 0.05, 0], e], R, "2", tF3a, tKa, K, K)], ["2"]))
    a, b = P(F3, "96"), P(S0, "1")
    H.append(("c3", [([a, [a[0], yD, 0], [xP - 0.06, yD, 0], [xP - 0.06, b[1] + 0.30, 0], [b[0], b[1] + 0.30, 0], b], R, "3", tF3a, tB, K, KD)], ["3"]))
    a, b, e = P(S0, "2"), P(S1, "3"), P(KM1, "13")
    puente = lambda a, b: [a, [a[0] + 0.07, a[1] - 0.30, 0], [b[0] + 0.07, b[1] + 0.30, 0], b]
    H.append(("c4", [(puente(a, b), R, "4", tB, tB, KD, KD),
                     ([a, [a[0] - 0.06, a[1] - 0.34, 0], [xP, a[1] - 0.34, 0], [xP, yB + 0.11, 0], [xL, yB + 0.11, 0], [xL, e[1], 0], e], R, "4", tB, tKa, KD, K)], ["4"]))
    a, b, a1, h1 = P(S1, "4"), P(KM1, "14"), P(KM1, "A1"), P(H1, "X1")
    H.append(("c5", [([a, [a[0] - 0.06, a[1] - 0.34, 0], [xP + 0.06, a[1] - 0.34, 0], [xP + 0.06, yB + 0.17, 0], [xL - 0.06, yB + 0.17, 0], [xL - 0.06, b[1], 0], b], R, "5", tB, tKa, KD, K),
                     ([b, [xL - 0.12, b[1] - 0.07, 0], [xL - 0.12, yB + 0.23, 0], [xR - 0.10, yB + 0.23, 0], [xR - 0.10, a1[1], 0], a1], R, "5", tKa, tKa, K, K),
                     (puente(a, h1), R, "5", tB, tB, KD, KD)], ["5"]))
    a, b = P(KM1, "22"), P(H2, "X1")
    H.append(("c6", [([a, [a[0], yG, 0], [xR + 0.18, yG, 0], [xR + 0.18, yD - 0.07, 0], [xP + 0.12, yD - 0.07, 0], [xP + 0.12, b[1] + 0.30, 0], [b[0], b[1] + 0.30, 0], b], R, "6", tKa, tB, K, KD)], ["6"]))
    a, b, h1, h2 = P(X0, "4_a"), P(KM1, "A2"), P(H1, "X2"), P(H2, "X2")
    H.append(("c7", [([a, [a[0], yD - 0.14, 0], [xR + 0.24, yD - 0.14, 0], [xR + 0.24, b[1], 0], b], N, "N", tX, tKa, K, K),
                     ([b, [xR + 0.30, b[1], 0], [xR + 0.30, yD - 0.21, 0], [xP + 0.18, yD - 0.21, 0], [xP + 0.18, h1[1] - 0.36, 0], [h1[0] - 0.06, h1[1] - 0.36, 0], h1], N, "N", tKa, tB, K, KD),
                     ([h1, [h1[0] + 0.07, h1[1] - 0.30, 0], [h1[0] + 0.07, h1[1] - 0.45, 0], [xP + 0.24, h1[1] - 0.45, 0], [xP + 0.24, h2[1] - 0.30, 0], [h2[0], h2[1] - 0.30, 0], h2], N, "N", tB, tB, KD, KD)], ["N"]))
    return H


def hilos_potencia(E):
    c = canales(E)
    F2, KM1, F3, X0, X1 = E["F2"], E["KM1"], E["F3"], E["X0"], E["X1"]
    yA, yB, yD, xI = c["yA"], c["yB"], c["yD"], c["xI"]
    tF2, tKp, tF3p, tX = TORN["F2"], TORN["KM1p"], TORN["F3p"], TORN["X"]
    T_ = {}
    T_["p1"] = []
    for i, (b, t, nm) in enumerate((("1_a", "1", "L1"), ("2_a", "3", "L2"), ("3_a", "5", "L3"))):
        a, z = X0.p(b), F2.p(t)
        T_["p1"].append(([a, [a[0], yA + 0.06 + 0.13 * i, 0], [z[0], yA + 0.06 + 0.13 * i, 0], z], NEGRO_P, nm, tX, tF2))
    T_["p2"] = []
    for t, u, nm in (("2", "1/L1", "L1"), ("4", "3/L2", "L2"), ("6", "5/L3", "L3")):
        a, z = F2.p(t), KM1.p(u)
        T_["p2"].append(([a, [a[0], yB, 0], [z[0], yB - 0.02, 0], z], NEGRO_P, nm, tF2, tKp))
    T_["p4"] = []
    for i, (t, u, nm) in enumerate((("2/T1", "1_a", "T1"), ("4/T2", "2_a", "T2"), ("6/T3", "3_a", "T3"))):
        a, z = F3.p(t), X1.p(u)
        yy = yD - 0.36 - 0.13 * (2 - i)
        T_["p4"].append(([a, [a[0], yy, 0], [z[0], yy, 0], z], NEGRO_P, nm, tF3p, tX))
    a, z = X0.p("5_a"), X1.p("4_a")
    yy = X0.borde("u") + 0.12
    T_["pe"] = [([a, [a[0], yy, 0], [z[0], yy, 0], z], "PE", "PE", tX, tX)]
    return T_

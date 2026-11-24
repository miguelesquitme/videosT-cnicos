"""H01 v5 · Conexión didáctica (Correcciones_V del usuario, 23-nov).
Cambios respecto de h01v3_lay:
- P1: bloques traseros nuevos (contacto GRIS sobre adaptador negro) del MISMO tamaño que el cuadro del frente (KD = KF).
- P2: borneras y riel DIN nuevos (svgref.bornera) en h01v5_eq/.
- P3: los cables entran a cada borne DESDE ARRIBA o DESDE ABAJO (nunca de lado): ENTRADAS con dirección u/d.
  Auxiliares del contactor: arriba 13 · 21 · A1, abajo 14 · 22 · A2; A1/A2 se toman a la derecha del tornillo de
  5/L3 y 6/T3 (x 42,5 mm) para no pasar encima de ellos. 95/96 del térmico por abajo.
- P4: curvas ABIERTAS (radio grande) y un tramo recto a la salida de cada puntera donde cabe el marcador.
- P5: equipos más separados (diagrama más pequeño a la izquierda).
- P9: salida al motor con manguera TSJ 4 × 8 AWG (negro × 3 + verde/amarillo), no cables sueltos.
Coordenadas de pantalla (Manim): x −7,1…7,1 · y −4…4."""
import numpy as np
from comun_e import *          # noqa: F401,F403
import h01v3_lay as _L3
from h01v3_lay import Eq3, ruta_redondeada, ENTRADAS, DIRS, ROJO_M, NEUTRO_C, NEGRO_P, PE_V, PE_A, COLLAR

EQ5 = DIR / "h01v5_eq"
_L3.EQ3 = EQ5                   # todos los Eq3 cargan la biblioteca v5 (bloques, borneras)
K = 0.023                       # equipos de riel
KB = K * 0.72                   # borneras (proporción real respecto de los equipos)
KD = 0.030                      # bloques traseros de la puerta
KF = KD                         # frente = MISMO tamaño que el bloque (P1-C)
W_CABLE = {"mando": 4.6, "pot": 8.0}

# ---------------------------------------------------------------------------------------------- entradas (P3)
ENTRADAS.update({
    "KM1": {"1/L1": (8.45, 0, "u"), "3/L2": (22.65, 0, "u"), "5/L3": (37.15, 0, "u"),
            "13": (17.42, 12.8, "u"), "21": (28.26, 12.8, "u"), "A1": (42.5, 12.8, "u"),
            "14": (17.42, 59.3, "d"), "22": (28.26, 59.3, "d"), "A2": (42.5, 59.3, "d"),
            "2/T1": (8.45, 72.66, "d"), "4/T2": (22.65, 72.66, "d"), "6/T3": (37.15, 72.66, "d")},
    "F3": {"2/T1": (9.2, 51.24, "d"), "4/T2": (22.47, 51.24, "d"), "6/T3": (35.8, 51.24, "d"),
           "95": (41.6, 38.6, "d"), "96": (27.92, 38.6, "d")},
    "X0": {f"{i}_a": (x, 0, "u") for i, x in zip(range(1, 6), (13.26, 23.46, 33.66, 41.36, 49.06))}
          | {f"{i}_b": (x, 51.0, "d") for i, x in zip(range(1, 6), (13.26, 23.46, 33.66, 41.36, 49.06))},
    "X1": {f"{i}_a": (x, 0, "u") for i, x in zip(range(1, 5), (13.26, 23.46, 33.66, 43.86))}
          | {f"{i}_b": (x, 51.0, "d") for i, x in zip(range(1, 5), (13.26, 23.46, 33.66, 43.86))},
})
for _b, (_n1, _n2) in {"S0b": ("1", "2"), "S1b": ("3", "4"), "H1b": ("X1", "X2"), "H2b": ("X1", "X2")}.items():
    ENTRADAS[_b] = {_n1: (11.25, 0.0, "u"), _n2: (11.25, 30.0, "d")}


def puntera(E, d, clase, k=K):
    """Collar de la puntera (DIN 46228-4): lo único que se ve, el pin entra bajo el plástico del borne."""
    perp = np.array([-d[1], d[0], 0])
    f = (k / K) ** 0.5
    ancho = {"mando": 0.044, "pot": 0.075}[clase] * f
    largo = {"mando": 0.080, "pot": 0.115}[clase] * f
    col = COLLAR[clase]
    p0, p1, p2 = E - d * 0.004, E + d * largo * 0.72, E + d * largo
    cuerpo = Polygon(p0 - perp * ancho / 2, p0 + perp * ancho / 2, p1 + perp * ancho / 2, p1 - perp * ancho / 2).set_fill(col, 1).set_stroke(width=0)
    embudo = Polygon(p1 - perp * ancho * 0.62, p1 + perp * ancho * 0.62, p2 + perp * ancho * 0.66, p2 - perp * ancho * 0.66).set_fill(col, 1).set_stroke(width=0)
    brillo = Polygon(p0 - perp * ancho * 0.28, p0 - perp * ancho * 0.12, p1 - perp * ancho * 0.12, p1 - perp * ancho * 0.28).set_fill(WHITE, 0.35).set_stroke(width=0)
    sombra = Polygon(p0 + perp * ancho * 0.30, p0 + perp * ancho / 2, p2 + perp * ancho * 0.66, p2 + perp * ancho * 0.40).set_fill(BLACK, 0.25).set_stroke(width=0)
    return fisico(VGroup(cuerpo, embudo, brillo, sombra)), largo


def marcador(num, P0, d, clase, w):
    """Marcador blanco con el número del hilo, centrado sobre el conductor y orientado con él."""
    t = Text(str(num), font=SANS, font_size=40, weight="BOLD", color="#111111")
    t.scale_to_fit_height(0.042 if clase == "mando" else 0.055)
    vertical = abs(d[1]) > abs(d[0])
    if vertical:
        t.rotate(PI / 2)
    largo = max(t.height if vertical else t.width, 0.055) + 0.028
    grosor = (0.075 if clase == "mando" else 0.105)
    caja = Rectangle(width=grosor if vertical else largo, height=largo if vertical else grosor, stroke_width=1, stroke_color="#9AA0A6").set_fill(WHITE, 1)
    c0 = P0 + d * (largo / 2)
    caja.move_to(c0)
    t.move_to(c0)
    return fisico(VGroup(caja, t)), largo


class Cable5(Group):
    """Cable de a (boca, dirección) a b. medio = vértices de la ruta. Curvas ABIERTAS (r grande) y tramo recto de
    salida L0 ≥ puntera + marcador + radio, para que el marcador quede siempre en recta (P4)."""

    def __init__(self, a, b, medio, color, clase, num, ka=K, kb=K, r=0.2, L0=None, marcas=(0.0, 0.0), dx=(0.0, 0.0),
                 marca_en=(None, None)):
        super().__init__()
        (A, da), (B, db) = a, b
        A = A + RIGHT * dx[0]
        B = B + RIGHT * dx[1]
        w = W_CABLE[clase]
        pa, la = puntera(A, da, clase, ka)
        pb, lb = puntera(B, db, clase, kb)
        L0 = L0 if L0 is not None else (0.30 if clase == "mando" else 0.36)
        L0a, L0b = L0 if isinstance(L0, tuple) else (L0, L0)
        ini, fin = A + da * la, B + db * lb
        pts = [ini, A + da * (la + L0a + marcas[0])] + [np.array(p, float) for p in medio] + [B + db * (lb + L0b + marcas[1]), fin]
        base = ruta_redondeada(pts, r)
        if color == "PE":
            capa = VGroup(base.copy().set_stroke(PE_V, w),
                          DashedVMobject(base.copy(), num_dashes=max(4, int(base.get_arc_length() / 0.07)), dashed_ratio=0.5).set_stroke(PE_A, w))
        else:
            capa = VGroup(base.copy().set_stroke(color, w))
        for s in capa.family_members_with_points():
            s.set_fill(opacity=0)
        self.conductor = fisico(capa)
        self.puntas = Group()
        Lr = base.get_arc_length()
        for j, (P0, d, larg, pu, extra) in enumerate(((A, da, la, pa, marcas[0]), (B, db, lb, pb, marcas[1]))):
            g = Group(pu)
            if num is not None:
                if marca_en[j] is not None:          # marcador sobre un tramo recto más adelante (arco desde la punta)
                    s0 = marca_en[j] if j == 0 else Lr - marca_en[j]
                    q0 = base.point_from_proportion(np.clip((s0 - 0.04) / Lr, 0, 1))
                    q1 = base.point_from_proportion(np.clip((s0 + 0.04) / Lr, 0, 1))
                    tg = (q1 - q0) / np.linalg.norm(q1 - q0)
                    mk, lm = marcador(num, ORIGIN, tg, clase, w)
                    mk.move_to(base.point_from_proportion(np.clip(s0 / Lr, 0, 1)))
                else:
                    mk, _ = marcador(num, P0 + d * (larg + 0.02 + extra), d, clase, w)
                g.add(mk)
            self.puntas.add(g)
        self.add(self.conductor, self.puntas)
        self.conductor.set_z_index(6)
        for g in self.puntas:
            for sm in g:
                sm.set_z_index(7)
        self.ruta = base

    def opaco(self, op=0.3):
        return [self.conductor.animate.set_stroke(opacity=op), self.puntas.animate.set_opacity(op)]


# ---------------------------------------------------------------------------------------------- disposición (P5)
def disposicion():
    E = {}
    F2 = E["F2"] = Eq3("F2", K).poner(-0.95, 3.22)
    E["F1"] = Eq3("F1", K).poner(1.30, 3.22)
    x_km = F2.borde("l") + (27.26 - 22.65) * K          # polos del contactor alineados con los del breaker
    KM1 = E["KM1"] = Eq3("KM1", K).poner(x_km, F2.borde("d") - 0.68)
    F3 = E["F3"] = Eq3("F3", K).poner(x_km + (22.65 - 22.47) * K, KM1.borde("d"))
    KM1.set_z_index(2)
    F3.set_z_index(1)
    yx = F3.borde("d") - 0.70
    xt2 = F3.mm(22.47, 0)[0]
    E["X1"] = Eq3("X1", KB).poner(xt2 - 23.46 * KB, yx)          # -X1 debajo del térmico (T2 alineado)
    E["X0"] = Eq3("X0", KB).poner(E["X1"].borde("l") - 0.27 - 62.32 * KB, yx)
    # puerta (vista trasera) a la derecha, a media altura
    for i, n in enumerate(("S0", "S1", "H1", "H2")):
        b = E[n + "b"] = Eq3(n + "b", KD).poner(2.80 + 1.06 * i, 0.80)
        f = E[n] = Eq3(n, KF).poner(b.borde("l"), b.borde("u") + 15.5 * KF)   # frente: su cuadro sobre el del bloque
    return E


def riel_din(E, k=KB):
    """Riel DIN 35 mm (EN 60715) metálico con ranuras, sin bordes, detrás de las dos borneras."""
    X0, X1 = E["X0"], E["X1"]
    yc = (X0.borde("u") + X0.borde("d")) / 2
    x0, x1 = X0.borde("l") - 0.20, X1.borde("r") + 0.20
    cx = (x0 + x1) / 2
    W = x1 - x0
    g = VGroup()
    g.add(Rectangle(width=W, height=35 * k, stroke_width=0).set_fill("#C4CAD1", 1).move_to([cx, yc, 0]))
    g.add(Rectangle(width=W, height=27 * k, stroke_width=0).set_fill("#D9DEE3", 1).move_to([cx, yc, 0]))
    g.add(Rectangle(width=W, height=4 * k, stroke_width=0).set_fill("#EEF1F4", 1).move_to([cx, yc + 15.5 * k, 0]))
    g.add(Rectangle(width=W, height=4 * k, stroke_width=0).set_fill("#9CA3AB", 1).move_to([cx, yc - 15.5 * k, 0]))
    g.add(Rectangle(width=W, height=1.2 * k, stroke_width=0).set_fill("#8C939B", 1).move_to([cx, yc + 13.4 * k, 0]))
    for x in np.arange(x0 + 0.12, x1 - 0.05, 25 * k):
        g.add(RoundedRectangle(width=15 * k, height=5.2 * k, corner_radius=2.6 * k, stroke_width=0).set_fill("#6F767E", 1).move_to([x, yc, 0]))
        g.add(RoundedRectangle(width=15 * k, height=1.6 * k, corner_radius=0.8 * k, stroke_width=0).set_fill("#50565C", 1).move_to([x, yc + 1.8 * k, 0]))
    return g


def puerta_marco(E):
    xs = [E[n].borde(l) for n in ("S0b", "H2b") for l in ("l", "r")]
    ys = [E["S0b"].borde(l) for l in ("u", "d")]
    m = DashedVMobject(Rectangle(width=max(xs) - min(xs) + 0.34, height=max(ys) - min(ys) + 1.25), num_dashes=70).set_stroke("#667085", 2)
    m.move_to([(max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0])
    t = T("PUERTA · vista trasera", 17, "#475467", "HEAVY").next_to(m, UP, buff=0.06).align_to(m, LEFT)
    return VGroup(m, t)


# ---------------------------------------------------------------------------------------------- rutas
def geo(E):
    F2, F1, KM1, F3, X0, X1 = (E[k] for k in ("F2", "F1", "KM1", "F3", "X0", "X1"))
    S0 = E["S0b"]
    return dict(
        yTop=F2.borde("u"),
        yF2b=F2.borde("d"), yKMt=KM1.borde("u"), yKMb=KM1.borde("d"), yF3b=F3.borde("d"), yX=X0.borde("u"),
        yDu=S0.borde("u"), yDd=S0.borde("d"),
        xR=KM1.borde("r"),
        lane=lambda i: 0.48 + 0.19 * i,                        # carriles verticales entre el tablero y la puerta
        gap=lambda bl: bl.borde("r") + 0.10,                  # pasillo a la derecha de cada bloque de la puerta
    )


def hilos_mando(E):
    """[(clave de voz, Cable5, [claves de marca en el diagrama])] · UN hilo por paso (P6)."""
    g = geo(E)
    F2, F1, KM1, F3, X0 = (E[k] for k in ("F2", "F1", "KM1", "F3", "X0"))
    S0, S1, H1, H2 = E["S0b"], E["S1b"], E["H1b"], E["H2b"]
    R, N = ROJO_M, NEUTRO_C
    ln = g["lane"]
    yT = g["yTop"]
    yDu, yDd = g["yDu"], g["yDd"]
    yG1, yG2 = yDu + 0.24, yDu + 0.36            # canal sobre los bloques
    yU1, yU2, yU3 = yDd - 0.26, yDd - 0.38, yDd - 0.50
    def C(a, b, medio, col, num, ka=K, kb=K, **kw):
        return Cable5(a, b, medio, col, "mando", num, ka, kb, **kw)
    def X(p):
        return p[0][0]
    H = []
    # 1 · L desde -F2:1 (entrada) a -F1:1, por arriba
    # (diagrama del usuario: X0:1 = L1 llega a la entrada 5 de -F2; ahí se toma la L del mando)
    a, b = F2.boca("5"), F1.boca("1")
    H.append(("c1", C(a, b, [[X(a) + 0.035, yT + 0.40, 0], [X(b), yT + 0.40, 0]], R, "1", dx=(0.035, 0)), ["1"]))
    # 2 · -F1:2 → -KM1:21 (arriba)
    a, b = F1.boca("2"), KM1.boca("21")
    yb_hi = g["yF2b"] - 0.24
    H.append(("c2a", C(a, b, [[X(a) - 0.035, yb_hi, 0], [X(b), yb_hi, 0]], R, "2", dx=(-0.035, 0), r=0.16), ["2"]))
    # 2 · -F1:2 → -F3:95 (por ABAJO)
    a, b = F1.boca("2"), F3.boca("95")
    y95 = g["yF3b"] - 0.06
    H.append(("c2b", C(a, b, [[X(a) + 0.035, yb_hi - 0.12, 0], [ln(0), yb_hi - 0.12, 0], [ln(0), y95, 0], [X(b), y95, 0]], R, "2", dx=(0.035, 0)), []))
    # 3 · -F3:96 (abajo) → -S0:1 (arriba)
    a, b = F3.boca("96"), S0.boca("1")
    y96 = y95 - 0.13
    H.append(("c3", C(a, b, [[X(a), y96, 0], [ln(1), y96, 0], [ln(1), yG1, 0], [X(b), yG1, 0]], R, "3", K, KD), ["3"]))
    # 4 · -S0:2 (abajo) → -S1:3 (arriba)
    a, b = S0.boca("2"), S1.boca("3")
    H.append(("c4a", C(a, b, [[X(a), yU1, 0], [g["gap"](S0), yU1, 0], [g["gap"](S0), yG1, 0], [X(b), yG1, 0]], R, "4", KD, KD, r=0.14, dx=(0.03, 0)), ["4"]))
    # 4 · -S0:2 → -KM1:13 (arriba)
    a, b = S0.boca("2"), KM1.boca("13")
    yb_lo = yb_hi - 0.24
    H.append(("c4b", C(a, b, [[X(a) - 0.03, yU2, 0], [ln(2), yU2, 0], [ln(2), yb_lo, 0], [X(b), yb_lo, 0]], R, "4", KD, K, dx=(-0.03, 0)), []))
    # 5 · -S1:4 (abajo) → -KM1:14 (por ABAJO)
    a, b = S1.boca("4"), KM1.boca("14")
    def ymm(v):
        return KM1.mm(0, v)[1]
    jb = dict(L0=(0.10, 0.30), marca_en=(0.42, None))          # J inferiores: marcador en el tramo horizontal
    y14 = ymm(77.5)
    H.append(("c5a", C(a, b, [[X(a) - 0.03, yU3, 0], [ln(3), yU3, 0], [ln(3), y14, 0], [X(b) - 0.03, y14, 0]], R, "5", KD, K, dx=(-0.03, -0.03), L0=(0.30, 0.10), marca_en=(None, 0.42)), ["5"]))
    # 5 · -KM1:14 → -KM1:A1 (puente de retención: abajo → arriba)
    a, b = KM1.boca("14"), KM1.boca("A1")
    H.append(("c5b", C(a, b, [[X(a) + 0.03, ymm(80.0), 0], [ln(4), ymm(80.0), 0], [ln(4), yb_lo - 0.12, 0], [X(b), yb_lo - 0.12, 0]], R, "5", dx=(0.03, 0), **jb), []))
    # 5 · -S1:4 → -H1:X1 (arriba)
    a, b = S1.boca("4"), H1.boca("X1")
    H.append(("c5c", C(a, b, [[X(a) + 0.03, yU1, 0], [g["gap"](S1), yU1, 0], [g["gap"](S1), yG1, 0], [X(b), yG1, 0]], R, "5", KD, KD, r=0.14, dx=(0.03, 0)), []))
    # 6 · -KM1:22 (abajo) → -H2:X1 (arriba)
    a, b = KM1.boca("22"), H2.boca("X1")
    y22 = ymm(75.0)
    H.append(("c6", C(a, b, [[X(a), y22, 0], [ln(5), y22, 0], [ln(5), yG2, 0], [X(b), yG2, 0]], R, "6", K, KD, **jb), ["6"]))
    # N · -X0:4 (arriba) → -KM1:A2 (abajo)
    a, b = X0.boca("4_a"), KM1.boca("A2")
    yA2 = ymm(72.5)
    yN = g["yF3b"] - 0.44
    H.append(("c7a", C(a, b, [[X(a), yN, 0], [ln(6), yN, 0], [ln(6), yA2, 0], [X(b) + 0.03, yA2, 0]], N, "N", KB, K, dx=(0, 0.03), L0=(0.30, 0.10), marca_en=(None, 0.42)), ["N"]))
    # N · -KM1:A2 → -H1:X2 (abajo)
    a, b = KM1.boca("A2"), H1.boca("X2")
    yU4 = yDd - 0.62
    H.append(("c7b", C(a, b, [[X(a) - 0.03, ymm(70.0), 0], [ln(7), ymm(70.0), 0], [ln(7), yU4, 0], [X(b) - 0.03, yU4, 0]], N, "N", K, KD, dx=(-0.03, -0.03), **jb), []))
    # N · -H1:X2 → -H2:X2 (abajo)
    a, b = H1.boca("X2"), H2.boca("X2")
    H.append(("c7c", C(a, b, [[X(a) + 0.03, yU2, 0], [X(b), yU2, 0]], N, "N", KD, KD, dx=(0.03, 0)), []))
    return H


def hilos_potencia(E):
    """Un hilo por paso (P6): p1 L1 L2 L3 · p2 L1 L2 L3 · p4 T1 T2 T3 · PE."""
    g = geo(E)
    F2, KM1, F3, X0, X1 = (E[k] for k in ("F2", "KM1", "F3", "X0", "X1"))
    P = lambda *a, **k: Cable5(*a, **k)
    out = {}
    yT = g["yTop"]
    out["p1"] = []
    # literal del diagrama del usuario: L1 (X0:1) → entrada 5 · L2 (X0:2) → 3 · L3 (X0:3) → 1 (rutas anidadas, sin cruces)
    for i, (bx, t, nm) in enumerate((("1_a", "5", "L1"), ("2_a", "3", "L2"), ("3_a", "1", "L3"))):
        a, z = X0.boca(bx), F2.boca(t)
        yy = yT + 0.62 - 0.12 * i
        out["p1"].append(P(a, z, [[a[0][0], yy, 0], [z[0][0] - (0.035 if t == "5" else 0), yy, 0]], NEGRO_P, "pot", nm, KB, K, r=0.22,
                           L0=(0.36, 0.20), dx=(0, -0.035 if t == "5" else 0)))
    out["p2"] = []
    for t, u, nm in (("2", "1/L1", "L3"), ("4", "3/L2", "L2"), ("6", "5/L3", "L1")):
        a, z = F2.boca(t), KM1.boca(u)
        ym = (g["yF2b"] + g["yKMt"]) / 2
        out["p2"].append(P(a, z, [[a[0][0], ym, 0], [z[0][0], ym, 0]], NEGRO_P, "pot", nm, L0=0.15, r=0.08))
    out["p4"] = []
    for t, u, nm in (("2/T1", "1_a", "T1"), ("4/T2", "2_a", "T2"), ("6/T3", "3_a", "T3")):
        a, z = F3.boca(t), X1.boca(u)
        ym = (g["yF3b"] + g["yX"]) / 2 - 0.12
        out["p4"].append(P(a, z, [[a[0][0], ym, 0], [z[0][0], ym, 0]], NEGRO_P, "pot", nm, K, KB, L0=0.26, r=0.10))
    a, z = X0.boca("5_a"), X1.boca("4_a")
    yy = g["yX"] + 0.30
    out["pe"] = [P(a, z, [[a[0][0], yy, 0], [z[0][0], yy, 0]], "PE", "pot", "PE", KB, KB, L0=0.14, r=0.12)]
    return out


def red_entrada(E):
    """Acometida de la red bajo -X0 (lado de campo)."""
    X0 = E["X0"]
    red = VGroup()
    for b, col in (("1_b", NEGRO_P), ("2_b", NEGRO_P), ("3_b", NEGRO_P), ("4_b", NEUTRO_C), ("5_b", PE_V)):
        A, d = X0.boca(b)
        pu, lp = puntera(A, d, "pot", KB)
        ln = Line(A + d * lp, [A[0], -4.6, 0]).set_stroke(col, 6)
        gg = VGroup(fisico(ln), pu)
        if col == PE_V:
            gg.add(fisico(DashedLine(A + d * lp, [A[0], -4.6, 0], dash_length=0.05).set_stroke(PE_A, 6)))
        red.add(gg)
    return red


def manguera_tsj(E, mo):
    """P9: -X1 → motor con manguera TSJ 4 × 8 AWG. Colas sueltas cortas en cada borne, chaqueta negra en el recorrido.
    Devuelve (grupo, punto de la cola T1 junto al motor para la pinza)."""
    X1 = E["X1"]
    caja = mo.mm(146, 56)               # tapa de la caja de conexiones (arriba)
    y_bajo = X1.borde("d") - 0.30
    x_sube = mo.img.get_left()[0] + 0.25
    y_alto = caja[1] + 0.55
    colas = VGroup()
    cols = (NEGRO_P, NEGRO_P, NEGRO_P, "PE")
    xs_b = [X1.boca(f"{i}_b")[0][0] for i in range(1, 5)]
    xg = sum(xs_b) / 4
    for i, col in enumerate(cols):
        A, d = X1.boca(f"{i + 1}_b")
        pu, lp = puntera(A, d, "pot", KB)
        m = ruta_redondeada([A + d * lp, [A[0], y_bajo + 0.12, 0], [xg + (i - 1.5) * 0.025, y_bajo, 0]], 0.08)
        capa = VGroup(m.copy().set_stroke(PE_V if col == "PE" else col, 5))
        if col == "PE":
            capa.add(DashedVMobject(m.copy(), num_dashes=6, dashed_ratio=0.5).set_stroke(PE_A, 5))
        for s in capa.family_members_with_points():
            s.set_fill(opacity=0)
        colas.add(VGroup(fisico(capa), pu))
    ruta = ruta_redondeada([[xg, y_bajo, 0], [xg, y_bajo - 0.18, 0], [x_sube, y_bajo - 0.18, 0], [x_sube, y_alto, 0],
                            [caja[0], y_alto, 0], [caja[0], caja[1] + 0.25, 0]], 0.30)
    chaqueta = fisico(VGroup(ruta.copy().set_stroke("#0B0B0C", 15), ruta.copy().set_stroke("#2A2D31", 9).shift(UP * 0.004 + LEFT * 0.004)))
    for s in chaqueta.family_members_with_points():
        s.set_fill(opacity=0)
    # colas dentro de la caja (se ven al abrir la tapa)
    rotulo = T("TSJ 4 × 8 AWG", 13, "#344054", "HEAVY").next_to([x_sube, (y_bajo + y_alto) / 2, 0], LEFT, buff=0.08).rotate(PI / 2)
    return VGroup(colas, chaqueta, rotulo)

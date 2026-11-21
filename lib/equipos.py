"""Equipos dibujados en el estilo único (ver estilo.py). Medidas reales en mm; k = unidades por mm.
Cada equipo expone .b[nombre] -> Borne (con .p = punto de conexión) para cablear siguiendo el diagrama.
Fuentes de forma y bornes: hojas de datos oficiales (ver referencias/LEEME.md) + Word del usuario."""
from estilo import *

K0 = 1 / 18.0   # 1 módulo DIN = 1 unidad


def _sombra(m, k):
    s = m.copy().set_fill(BLACK, 0.35).set_stroke(width=0).shift(RIGHT * 1.0 * k + DOWN * 1.2 * k)
    return s


# =================================================================== DISYUNTOR MODULAR (1P / 2P / 3P)
def disyuntor(polos=1, In=6, curva="C", k=K0, ref="F1", on=False):
    """Interruptor automático modular (IEC 60898-1): 18 mm por polo × 90 mm. Bornes 1,3,5 arriba / 2,4,6 abajo.
    Palanca común a todos los polos (accionamiento unido)."""
    W, H = 18 * polos, 90
    g = VGroup()
    cuerpo = caja(W, H, k, CUERPO, r=1.4)
    g.add(_sombra(cuerpo, k), cuerpo)
    # cuello superior/inferior (zona de bornes más angosta en profundidad: se dibuja como franja)
    for y in (H / 2 - 14, -H / 2 + 14):
        g.add(Rectangle(width=W * k, height=28 * k, stroke_width=0).set_fill(CUERPO_OS, 1).move_to([0, y * k, 0]))
    g.add(RoundedRectangle(width=W * k, height=H * k, corner_radius=1.4 * k, stroke_color=BORDE, stroke_width=1.6).set_fill(opacity=0))
    b = {}
    for i in range(polos):
        x = (-W / 2 + 9 + 18 * i) * k
        b[str(2 * i + 1)] = Borne(str(2 * i + 1), k, lado=DOWN).move_to([x, (H / 2 - 9) * k, 0])
        b[str(2 * i + 2)] = Borne(str(2 * i + 2), k, lado=UP).move_to([x, (-H / 2 + 9) * k, 0])
        # separación entre polos
        if i:
            g.add(Line([(-W / 2 + 18 * i) * k, (H / 2) * k, 0], [(-W / 2 + 18 * i) * k, (-H / 2) * k, 0]).set_stroke(BORDE, 1.2))
    # ajuste de posición de etiquetas: debajo del tornillo superior y encima del inferior
    for n, bo in b.items():
        g.add(bo)
    # frente central: rótulo de calibre, ventana de estado y palanca
    fr = Rectangle(width=W * k, height=34 * k, stroke_color=BORDE, stroke_width=1).set_fill(CUERPO_CL, 1).move_to([0, 0, 0])
    g.add(fr)
    cal = txt(f"{curva}{In}", 4.6 * k, TXT_EQ).move_to([0, 12.5 * k, 0]) if polos == 1 else txt(f"{curva}{In}", 5.2 * k, TXT_EQ).move_to([(-W / 2 + 8.5) * k, 10 * k, 0])
    ten = txt("230/400 V~", 1.5 * k, TXT_EQ, MEDIUM)
    if polos == 1:
        ten.next_to(cal, DOWN, buff=0.8 * k)
    else:
        ten.next_to(cal, DOWN, buff=0.9 * k, aligned_edge=LEFT)
    g.add(cal, ten)
    # palanca (ancho de todos los polos, unida)
    ranura = RoundedRectangle(width=(W - 5) * k, height=13 * k, corner_radius=1 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, -8 * k, 0])
    pal = RoundedRectangle(width=(W - 7) * k, height=6 * k, corner_radius=1 * k, stroke_color=BORDE, stroke_width=1).set_fill("#2B2F36", 1)
    pal.move_to(ranura.get_center() + (UP if on else DOWN) * 3.2 * k)
    ven = RoundedRectangle(width=4 * k, height=2.4 * k, corner_radius=0.4 * k, stroke_width=0).set_fill("#D92D20" if on else "#12B76A", 1).move_to([(W / 2 - 4) * k, 10 * k, 0] if polos > 1 else [4.5 * k, 2.6 * k, 0])
    g.add(ranura, pal, ven)
    g.add(txt("I ON", 1.4 * k, TXT_EQ).next_to(ranura, UP, buff=0.5 * k).shift(RIGHT * 0 * k), txt("O OFF", 1.4 * k, TXT_EQ).next_to(ranura, DOWN, buff=0.5 * k))
    lg = logo_marca(4 * k).move_to([(W / 2 - 4.5) * k, 3.5 * k, 0] if polos > 1 else [-3.5 * k, 2.6 * k, 0])
    eti = RoundedRectangle(width=(W - 4) * k, height=5 * k, corner_radius=0.4 * k, stroke_width=0).set_fill(WHITE, 1).move_to([0, 22.5 * k, 0])
    g.add(eti, txt(f"-{ref}", 3 * k, TXT_OS).move_to(eti))
    g.add(lg)
    g.b, g.pal, g.ranura, g.ven, g.k, g.on = b, pal, ranura, ven, k, on
    g.ficha = dict(nombre=f"Disyuntor {polos}P", W=W, H=H)
    return g


def disyuntor_mover(d, on=True):
    """Animación de la palanca (ON arriba / OFF abajo) y ventana de estado."""
    dy = (6.4 if on else -6.4) * d.k
    d.on = on
    return AnimationGroup(d.pal.animate.shift(UP * dy), d.ven.animate.set_fill("#D92D20" if on else "#12B76A", 1))


# =================================================================== GUARDAMOTOR
def guardamotor(rango=(22, 32), ajuste=24.3, k=K0, ref="QM1", on=False):
    """Guardamotor tamaño S0: 45 × 97 mm (hoja de datos oficial). Arriba 1/L1 3/L2 5/L3, abajo 2/T1 4/T2 6/T3.
    Frente: dial de ajuste (A), botón TEST, mando giratorio I/O, rótulo."""
    W, H = 45, 97
    g = VGroup()
    cu = caja(W, H, k)
    g.add(_sombra(cu, k), cu)
    for y in (H / 2 - 10, -H / 2 + 10):
        g.add(Rectangle(width=W * k, height=20 * k, stroke_width=0).set_fill(CUERPO_OS, 1).move_to([0, y * k, 0]))
    g.add(caja(W, H, k, CUERPO).set_fill(opacity=0))
    b = {}
    for x, (na, nb) in zip((-14, 0, 14), (("1/L1", "2/T1"), ("3/L2", "4/T2"), ("5/L3", "6/T3"))):
        b[na] = Borne(na, k, lado=DOWN).move_to([x * k, (H / 2 - 8) * k, 0])
        b[nb] = Borne(nb, k, lado=UP).move_to([x * k, (-H / 2 + 8) * k, 0])
    g.add(*b.values())
    fr = caja(41, 55, k, CUERPO_CL, r=1.2).move_to([0, 0, 0])
    g.add(fr)
    # dial de ajuste
    cx, cy = -10 * k, 16 * k
    aro = Circle(radius=6.5 * k, stroke_color=BORDE, stroke_width=1.2).set_fill("#E4E7EC", 1).move_to([cx, cy, 0])
    dial = Circle(radius=4.2 * k, stroke_color=BORDE, stroke_width=1).set_fill(TORN, 1).move_to([cx, cy, 0])
    a0, a1 = PI * 1.25, -PI * 0.25
    ang = a0 + (a1 - a0) * (ajuste - rango[0]) / (rango[1] - rango[0])
    flecha = Line([cx, cy, 0], [cx, cy, 0] + 4.2 * k * np.array([np.cos(ang), np.sin(ang), 0])).set_stroke("#D92D20", 2.2)
    escala = VGroup(*[txt(str(v), 1.5 * k, TXT_OS).move_to([cx, cy, 0] + 8.2 * k * np.array([np.cos(a0 + (a1 - a0) * (v - rango[0]) / (rango[1] - rango[0])), np.sin(a0 + (a1 - a0) * (v - rango[0]) / (rango[1] - rango[0])), 0]))
                      for v in (rango[0], (rango[0] + rango[1]) // 2, rango[1])])
    escala.set_color(TXT_EQ)
    g.add(aro, dial, flecha, escala, txt("A", 1.6 * k, TXT_EQ).move_to([cx + 6 * k, cy - 7.5 * k, 0]))
    test = RoundedRectangle(width=7 * k, height=3.2 * k, corner_radius=0.6 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([10 * k, 20 * k, 0])
    g.add(test, txt("TEST", 1.4 * k, TXT_EQ).next_to(test, DOWN, buff=0.6 * k))
    # mando giratorio
    mx, my = 6 * k, -8 * k
    base = Circle(radius=10.5 * k, stroke_color=BORDE, stroke_width=1.2).set_fill(CUERPO_OS, 1).move_to([mx, my, 0])
    perilla = RoundedRectangle(width=6 * k, height=19 * k, corner_radius=2.5 * k, stroke_color=BORDE, stroke_width=1).set_fill("#1F2329", 1).move_to([mx, my, 0])
    ind = Line([mx, my + 3 * k, 0], [mx, my + 8.5 * k, 0]).set_stroke(WHITE, 2.4)
    mando = VGroup(perilla, ind)
    if not on:
        mando.rotate(PI / 2, about_point=np.array([mx, my, 0]))
    g.add(base, mando, txt("I", 2.2 * k, TXT_EQ).move_to([mx, my + 13 * k, 0]), txt("O", 2.2 * k, TXT_EQ).move_to([mx - 13 * k, my, 0]))
    eti = RoundedRectangle(width=15 * k, height=5 * k, corner_radius=0.4 * k, stroke_width=0).set_fill(WHITE, 1).move_to([-12 * k, -20 * k, 0])
    g.add(eti, txt(f"-{ref}", 2.8 * k, TXT_OS).move_to(eti), logo_marca(4.5 * k).move_to([-12 * k, 5 * k, 0]))
    g.add(txt(f"{rango[0]}–{rango[1]} A", 1.7 * k, TXT_EQ).move_to([-12 * k, -11 * k, 0]))
    g.b, g.mando, g.c_mando, g.k, g.on = b, mando, np.array([mx, my, 0]), k, on
    g.ficha = dict(nombre="Guardamotor", W=W, H=H)
    return g


# =================================================================== CONTACTOR
def contactor(k=K0, ref="KM1", bobina="240 V~", ie="32 A AC-3"):
    """Contactor 3 polos 45 × 85 mm con 1 NA + 1 NC integrados (disposición del Word del usuario, igual a la de los
    contactores de catálogo de 9–38 A): arriba 1/L1 3/L2 5/L3 y en el escalón 13NO 21NC A1; abajo 14NO 22NC A2 y 2/T1 4/T2 6/T3."""
    W, H = 45, 85
    g = VGroup()
    cu = caja(W, H, k)
    g.add(_sombra(cu, k), cu)
    b = {}
    # fila superior (potencia)
    for x, n in zip((-14, 0, 14), ("1/L1", "3/L2", "5/L3")):
        b[n] = Borne(n, k, lado=UP).move_to([x * k, (H / 2 - 7) * k, 0])
    for x, n in zip((-14, 0, 14), ("2/T1", "4/T2", "6/T3")):
        b[n] = Borne(n, k, lado=DOWN).move_to([x * k, (-H / 2 + 7) * k, 0])
    # escalones auxiliares
    for y in (H / 2 - 21, -H / 2 + 21):
        g.add(Rectangle(width=W * k, height=14 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, y * k, 0]))
    for x, n, et in zip((-9, 3, 15), ("13", "21", "A1"), ("13 NO", "21 NC", "A1")):
        b[n] = Borne(et, k, lado=DOWN, cavidad="#1E2329").move_to([x * k, (H / 2 - 19) * k, 0])
    for x, n, et in zip((-9, 3, 15), ("14", "22", "A2"), ("14 NO", "22 NC", "A2")):
        b[n] = Borne(et, k, lado=UP, cavidad="#1E2329").move_to([x * k, (-H / 2 + 19) * k, 0])
    g.add(*b.values())
    # frente: ventana de contactos y rótulo
    fr = Rectangle(width=W * k, height=29 * k, stroke_color=BORDE, stroke_width=1).set_fill(CUERPO_CL, 1)
    ven = RoundedRectangle(width=24 * k, height=8 * k, corner_radius=0.6 * k, stroke_width=0).set_fill("#1F2329", 1).move_to([0, 5.5 * k, 0])
    barras = VGroup(*[Rectangle(width=4.5 * k, height=6 * k, stroke_width=0).set_fill("#5B6472", 1).move_to([x * k, 5.5 * k, 0]) for x in (-8, -2.7, 2.7, 8)])
    eti = RoundedRectangle(width=22 * k, height=6.5 * k, corner_radius=0.4 * k, stroke_width=0).set_fill(WHITE, 1).move_to([0, -6 * k, 0])
    g.add(fr, ven, barras, eti, txt(f"-{ref}", 3.6 * k, TXT_OS).move_to(eti), logo_marca(3.6 * k).move_to([-17 * k, 5.5 * k, 0]),
          txt(bobina, 1.5 * k, TXT_EQ).move_to([16 * k, 7.5 * k, 0]), txt(ie, 1.5 * k, TXT_EQ).move_to([16 * k, 3.5 * k, 0]))
    g.b, g.barras, g.k = b, barras, k
    g.ficha = dict(nombre="Contactor", W=W, H=H)
    return g


def contactor_cerrar(ct, on=True):
    """Las barras de la ventana bajan al cerrar (indicador de posición)."""
    return ct.barras.animate.shift(DOWN * (1.5 if on else -1.5) * ct.k)


# =================================================================== RELÉ TÉRMICO
def rele_termico(rango=(23, 32), ajuste=24.3, k=K0, ref="F2"):
    """Relé térmico de montaje directo bajo el contactor, 45 × 66 mm (como la referencia del usuario):
    arriba 98 NO 97 · 96 NC 95; dial de ajuste, TEST, STOP (rojo) y RESET (azul, M/A); abajo 2/T1 4/T2 6/T3.
    Sus pines (1/L1 3/L2 5/L3) entran en 2/T1 4/T2 6/T3 del contactor."""
    W, H = 45, 66
    g = VGroup()
    cu = caja(W, H, k)
    g.add(_sombra(cu, k), cu)
    b = {}
    g.add(Rectangle(width=W * k, height=14 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, 5 * k, 0]))
    for x, n in zip((-16, -6, 6, 16), ("98", "97", "96", "95")):
        b[n] = Borne(n, k, lado=DOWN, h_txt=2.0, cavidad="#1E2329").move_to([x * k, 7 * k, 0])
    g.add(txt("NO", 1.5 * k, TXT_EQ).move_to([-11 * k, 1.2 * k, 0]), txt("NC", 1.5 * k, TXT_EQ).move_to([11 * k, 1.2 * k, 0]))
    for x, n in zip((-14, 0, 14), ("2/T1", "4/T2", "6/T3")):
        b[n] = Borne(n, k, lado=UP).move_to([x * k, (-H / 2 + 7) * k, 0])
    g.add(*b.values())
    fr = caja(43, 20, k, CUERPO_CL, r=1).move_to([0, (H / 2 - 9) * k, 0])
    g.add(fr)
    cx, cy = -14 * k, (H / 2 - 9) * k
    dial = Circle(radius=6.2 * k, stroke_color=BORDE, stroke_width=1).set_fill("#2F6FD0", 1).move_to([cx, cy, 0])
    a0, a1 = PI * 1.2, -PI * 0.2
    ang = a0 + (a1 - a0) * (ajuste - rango[0]) / (rango[1] - rango[0])
    flecha = VGroup(Line([cx, cy, 0], [cx, cy, 0] + 5 * k * np.array([np.cos(ang), np.sin(ang), 0])).set_stroke(WHITE, 2.6),
                    Line([cx, cy, 0], [cx, cy, 0] - 3 * k * np.array([np.cos(ang), np.sin(ang), 0])).set_stroke(WHITE, 2.6))
    g.add(dial, flecha, txt(f"{rango[0]}–{rango[1]} A", 1.5 * k, TXT_EQ).next_to(dial, DOWN, buff=0.4 * k))
    test = RoundedRectangle(width=6 * k, height=2.6 * k, corner_radius=0.5 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([-3 * k, (H / 2 - 4.5) * k, 0])
    g.add(test, txt("TEST", 1.4 * k, TXT_EQ).next_to(test, RIGHT, buff=0.6 * k))
    stop = Circle(radius=4.2 * k, stroke_color="#7A271A", stroke_width=1).set_fill("#D92D20", 1).move_to([7 * k, (H / 2 - 11.5) * k, 0])
    reset = Circle(radius=4.2 * k, stroke_color="#1849A9", stroke_width=1).set_fill("#2F6FD0", 1).move_to([17 * k, (H / 2 - 11.5) * k, 0])
    g.add(stop, reset, txt("STOP", 1.3 * k, TXT_EQ).move_to([7 * k, (H / 2 - 4.5) * k, 0]).shift(RIGHT * 4 * k), txt("RESET", 1.3 * k, TXT_EQ).move_to([17 * k, (H / 2 - 4.5) * k, 0]).shift(RIGHT * 2 * k),
          txt("M A", 1.4 * k, WHITE).move_to(reset))
    eti = RoundedRectangle(width=14 * k, height=5 * k, corner_radius=0.4 * k, stroke_width=0).set_fill(WHITE, 1).move_to([0, -11 * k, 0])
    g.add(eti, txt(f"-{ref}", 2.8 * k, TXT_OS).move_to(eti), logo_marca(3.6 * k).move_to([-15 * k, -11 * k, 0]), txt("CLASS 10", 1.4 * k, TXT_EQ).move_to([14 * k, -11 * k, 0]))
    g.b, g.test, g.stop, g.reset, g.k = b, test, stop, reset, k
    g.ficha = dict(nombre="Relé térmico", W=W, H=H)
    return g


# =================================================================== BASE DE 8 PINES + RELÉ / TEMPORIZADOR
def base_8p(k=K0):
    """Base para riel DIN de 8 pines (octal), 38 × 70 mm: arriba 3 4 5 6, abajo 2 1 8 7 (como la referencia del usuario)."""
    W, H = 38, 70
    g = VGroup()
    cu = caja(W, H, k, CUERPO_OS)
    g.add(_sombra(cu, k), cu)
    b = {}
    for x, n in zip((-13.5, -4.5, 4.5, 13.5), ("3", "4", "5", "6")):
        b[n] = Borne(n, k, w=8, h=8, lado=UP, h_txt=2.4).move_to([x * k, (H / 2 - 6) * k, 0])
    for x, n in zip((-13.5, -4.5, 4.5, 13.5), ("2", "1", "8", "7")):
        b[n] = Borne(n, k, w=8, h=8, lado=DOWN, h_txt=2.4).move_to([x * k, (-H / 2 + 6) * k, 0])
    g.add(*b.values())
    g.b = b
    return g


def rele_8p(k=K0, ref="KA1", bobina="240 V~", tipo="rele"):
    """Relé de 2 contactos conmutados enchufado en su base de 8 pines (patillaje octal estándar):
    bobina 2-7; polo 1: común 1, NA 3, NC 4; polo 2: común 8, NA 6, NC 5. tipo='timer' dibuja el temporizador."""
    base = base_8p(k)
    W, H = 35, 46
    tapa = caja(W, H, k, CUERPO if tipo == "rele" else CUERPO_CL, r=2)
    g = VGroup(base, _sombra(tapa, k), tapa)
    if tipo == "rele":
        g.add(logo_marca(4 * k).move_to([-10 * k, 17 * k, 0]), txt(f"-{ref}", 3 * k, TXT_EQ).move_to([6 * k, 17 * k, 0]))
        # esquema impreso de los contactos (como en la carcasa real)
        y0 = 4 * k
        for i, (c, na, nc) in enumerate((("1", "3", "4"), ("8", "6", "5"))):
            x = (-8 + 16 * i) * k
            g.add(VGroup(Line([x, y0 - 6 * k, 0], [x, y0, 0]), Line([x, y0, 0], [x + 3 * k, y0 + 5 * k, 0]),
                         Line([x - 3 * k, y0 + 7 * k, 0], [x - 3 * k, y0 + 4 * k, 0]), Line([x + 3 * k, y0 + 7 * k, 0], [x + 3 * k, y0 + 5 * k, 0])).set_stroke(TXT_EQ, 1.4))
            g.add(txt(c, 1.5 * k, TXT_EQ).move_to([x, y0 - 8 * k, 0]), txt(nc, 1.5 * k, TXT_EQ).move_to([x - 3 * k, y0 + 9 * k, 0]), txt(na, 1.5 * k, TXT_EQ).move_to([x + 3 * k, y0 + 9 * k, 0]))
        bob = Rectangle(width=9 * k, height=4 * k, stroke_color=TXT_EQ, stroke_width=1.4).move_to([0, -12 * k, 0])
        g.add(bob, txt("2", 1.5 * k, TXT_EQ).next_to(bob, LEFT, buff=0.8 * k), txt("7", 1.5 * k, TXT_EQ).next_to(bob, RIGHT, buff=0.8 * k),
              txt(bobina, 1.6 * k, TXT_EQ).move_to([0, -18 * k, 0]))
        led = Circle(radius=1.3 * k, stroke_width=0).set_fill("#2E7D32", 1).move_to([13 * k, -17 * k, 0])
        g.add(led)
        g.led = led
    else:
        # temporizador analógico: dial grande, LEDs POWER / UP, selector de rango
        cx, cy = 0, 0
        aro = Circle(radius=14 * k, stroke_color=BORDE, stroke_width=1.2).set_fill("#E4E7EC", 1).move_to([cx, cy, 0])
        mar = VGroup(*[Line([cx, cy, 0] + 12.5 * k * np.array([np.cos(a), np.sin(a), 0]), [cx, cy, 0] + 13.6 * k * np.array([np.cos(a), np.sin(a), 0])).set_stroke(TXT_OS, 1)
                       for a in np.linspace(PI * 1.25, -PI * 0.25, 26)])
        nums = VGroup(*[txt(t, 1.5 * k, TXT_OS).move_to([cx, cy, 0] + 10.5 * k * np.array([np.cos(a), np.sin(a), 0]))
                        for t, a in zip(("0", "1", "2", "3", "4", "5", "6"), np.linspace(PI * 1.25, -PI * 0.25, 7))])
        perilla = Circle(radius=6 * k, stroke_color=BORDE, stroke_width=1).set_fill("#2B3038", 1).move_to([cx, cy, 0])
        aguja = Line([cx, cy, 0], [cx, cy, 0] + 9 * k * np.array([np.cos(PI * 0.6), np.sin(PI * 0.6), 0])).set_stroke("#D92D20", 2.4)
        g.add(aro, mar, nums, perilla, aguja)
        for n, x, c in (("POWER", -11, "#12B76A"), ("UP", 11, "#F79009")):
            g.add(Circle(radius=1.3 * k, stroke_width=0).set_fill(c, 0.35).move_to([x * k, 19 * k, 0]), txt(n, 1.3 * k, TXT_OS).move_to([x * k, 16.5 * k, 0]))
        g.add(txt(f"-{ref}", 2.6 * k, TXT_OS).move_to([0, -18 * k, 0]), logo_marca(3.4 * k).move_to([12 * k, -18 * k, 0]), txt("s · min · h", 1.4 * k, TXT_OS).move_to([-11 * k, -18 * k, 0]))
        g.aguja = aguja
    g.b, g.k = base.b, k
    g.ficha = dict(nombre="Relé 8 pines" if tipo == "rele" else "Temporizador", W=38, H=70)
    return g


# =================================================================== PUERTA: PULSADORES, SELECTOR, PILOTO, EMERGENCIA (vista 2D)
COLORES_IEC = {"verde": ("#12B76A", "#05603A"), "rojo": ("#E5484D", "#7A271A"), "amarillo": ("#FDB022", "#93370D"),
               "azul": ("#2E90FA", "#194185"), "blanco": ("#F2F4F7", "#667085"), "negro": ("#2B2F36", "#101828")}


def operador_22(tipo="pulsador", color="verde", k=K0, ref="S1", simbolo="I", pos=0):
    """Frente del operador de 22 mm (vista 2D de frente, en la puerta).
    tipo: pulsador | selector | piloto | emergencia. Marco cuadrado de 30 mm como en las referencias."""
    c, co = COLORES_IEC[color]
    g = VGroup()
    if tipo == "emergencia":
        placa = Circle(radius=30 * k, stroke_color="#93370D", stroke_width=1.4).set_fill("#FDB022", 1)
        g.add(placa, txt("PARO DE EMERGENCIA", 1.9 * k, TXT_OS).move_to([0, -25.5 * k, 0]))
        hongo = Circle(radius=19 * k, stroke_color="#7A271A", stroke_width=1.6).set_fill("#D92D20", 1)
        g.add(Circle(radius=21 * k, stroke_width=0).set_fill(BLACK, 0.25).shift(RIGHT * 1 * k + DOWN * 1.4 * k), hongo,
              Arc(radius=14 * k, start_angle=PI * 0.55, angle=PI * 0.45).set_stroke(WHITE, 3, 0.5))
        g.add(Arrow([-6 * k, -8 * k, 0], [6 * k, -8 * k, 0], buff=0, stroke_width=3, color=WHITE, tip_length=0.08).set_opacity(0.85),
              txt("GIRAR", 1.8 * k, WHITE).move_to([0, -12.5 * k, 0]))
        g.boton = hongo
    else:
        marco = RoundedRectangle(width=30 * k, height=30 * k, corner_radius=2.5 * k, stroke_color=BORDE, stroke_width=1.4).set_fill(CUERPO_OS, 1)
        bisel = Circle(radius=12.5 * k, stroke_color=METAL, stroke_width=2).set_fill("#20242B", 1)
        g.add(_sombra(marco, k), marco, bisel)
        if tipo == "pulsador":
            bot = Circle(radius=10.5 * k, stroke_color=co, stroke_width=1.4).set_fill(c, 1)
            g.add(bot, Arc(radius=8 * k, start_angle=PI * 0.6, angle=PI * 0.5).set_stroke(WHITE, 2.4, 0.5))
            if simbolo:
                g.add(txt(simbolo, 7 * k, WHITE if color != "blanco" else TXT_OS))
            g.boton = bot
        elif tipo == "piloto":
            lente = Circle(radius=10.5 * k, stroke_color=co, stroke_width=1.4).set_fill(c, 0.55)
            anillos = VGroup(*[Circle(radius=(8.5 - 2.6 * i) * k, stroke_color=co, stroke_width=1).set_fill(opacity=0) for i in range(3)])
            g.add(lente, anillos)
            g.boton = lente
        elif tipo == "selector":
            bot = Circle(radius=10.5 * k, stroke_color="#101828", stroke_width=1.4).set_fill("#2B2F36", 1)
            maneta = RoundedRectangle(width=5.5 * k, height=19 * k, corner_radius=2 * k, stroke_color=BORDE, stroke_width=1).set_fill("#101828", 1)
            ind = Line(UP * 3 * k, UP * 8 * k).set_stroke(WHITE, 3)
            mango = VGroup(maneta, ind).rotate(PI / 4 * (1 if pos else -1))
            g.add(bot, mango, txt("0", 2.6 * k, TXT_EQ).move_to([-10 * k, 11.5 * k, 0]), txt("1", 2.6 * k, TXT_EQ).move_to([10 * k, 11.5 * k, 0]))
            g.boton, g.mango = bot, mango
    porta = RoundedRectangle(width=28 * k, height=8 * k, corner_radius=0.8 * k, stroke_color="#98A2B3", stroke_width=0.8).set_fill(WHITE, 1)
    porta.next_to(g, DOWN, buff=3 * k)
    g.add(porta, txt(f"-{ref}", 3.4 * k, TXT_OS).move_to(porta))
    g.k = k
    g.ficha = dict(nombre=tipo, W=30, H=30)
    return g


def bloque_contacto(n1, n2, nc=False, k=K0, piloto=False):
    """Vista trasera del operador: bloque de contacto (o portalámparas) con sus dos tornillos de conexión.
    Numeración sobre el bloque: NA 3-4 / NC 1-2 (en el esquema: 13-14 / 11-12 o 21-22 según la posición)."""
    g = VGroup()
    cuerpo = caja(14, 32, k, "#1F2329", r=1.4)
    g.add(_sombra(cuerpo, k), cuerpo)
    b = {n1: Borne(n1, k, w=8, h=8, lado=LEFT, h_txt=2.4, cavidad="#3A414C").move_to([0, 9 * k, 0]),
         n2: Borne(n2, k, w=8, h=8, lado=LEFT, h_txt=2.4, cavidad="#3A414C").move_to([0, -9 * k, 0])}
    g.add(*b.values())
    if piloto:
        led = RoundedRectangle(width=9 * k, height=5 * k, corner_radius=1 * k, stroke_width=0).set_fill("#98A2B3", 1)
        g.add(led, txt("LED", 1.8 * k, TXT_OS).move_to(led))
    else:
        tag = RoundedRectangle(width=9 * k, height=5 * k, corner_radius=1 * k, stroke_width=0).set_fill("#D92D20" if nc else "#12B76A", 1)
        g.add(tag, txt("NC" if nc else "NO", 2.0 * k, WHITE).move_to(tag))
    # collarín de fijación (vista desde atrás)
    g.add(RoundedRectangle(width=30 * k, height=6 * k, corner_radius=1 * k, stroke_color=BORDE, stroke_width=1).set_fill(CUERPO_OS, 1).next_to(cuerpo, UP, buff=0))
    g.b, g.k = b, k
    return g


# =================================================================== SENSORES (M18) Y FLOTADOR
def sensor_m18(tipo="inductivo", k=K0, ref="B1"):
    """Sensor cilíndrico M18 de 3 hilos PNP (vista lateral, cara a la derecha): cuerpo roscado, 2 tuercas,
    LED, conector M12 (1 BN +, 3 BU −, 4 BK salida). tipo: inductivo | capacitivo | optico."""
    L = 70
    g = VGroup()
    cuerpo = Rectangle(width=L * k, height=18 * k, stroke_color=BORDE, stroke_width=1.2).set_fill(METAL, 1)
    hilos = VGroup(*[Line([x * k, 9 * k, 0], [(x + 1.2) * k, -9 * k, 0]).set_stroke("#8A929E", 1) for x in np.arange(-L / 2 + 2, L / 2 - 4, 1.6)])
    g.add(cuerpo, hilos)
    for x in (-12, 4):
        g.add(RoundedRectangle(width=5 * k, height=26 * k, corner_radius=0.8 * k, stroke_color=BORDE, stroke_width=1).set_fill("#9AA4B2", 1).move_to([x * k, 0, 0]))
    cara_c = {"inductivo": "#2E90FA", "capacitivo": "#F79009", "optico": "#2B2F36"}[tipo]
    cara = RoundedRectangle(width=6 * k, height=17 * k, corner_radius=1.5 * k, stroke_color=BORDE, stroke_width=1).set_fill(cara_c, 1).move_to([(L / 2 + 2) * k, 0, 0])
    g.add(cara)
    if tipo == "optico":
        g.add(Circle(radius=3 * k, stroke_width=0).set_fill("#D92D20", 0.9).move_to(cara.get_center() + UP * 3.5 * k),
              Circle(radius=3 * k, stroke_width=0).set_fill("#667085", 1).move_to(cara.get_center() + DOWN * 3.5 * k))
    cola = RoundedRectangle(width=14 * k, height=15 * k, corner_radius=1.5 * k, stroke_color=BORDE, stroke_width=1).set_fill("#2B2F36", 1).move_to([(-L / 2 - 7) * k, 0, 0])
    led = Circle(radius=1.8 * k, stroke_width=0).set_fill("#F79009", 1).move_to(cola.get_center() + UP * 3.5 * k)
    g.add(cola, led)
    if tipo == "capacitivo":
        g.add(Circle(radius=2.2 * k, stroke_color=WHITE, stroke_width=1).set_fill("#667085", 1).move_to(cola.get_center() + DOWN * 3.5 * k))
    m12 = RoundedRectangle(width=10 * k, height=12 * k, corner_radius=1 * k, stroke_color=BORDE, stroke_width=1).set_fill(METAL, 1).move_to([(-L / 2 - 19) * k, 0, 0])
    g.add(m12, txt("M12", 1.8 * k, TXT_OS).move_to(m12))
    b = {}
    for i, (n, col, nombre) in enumerate((("1", "#7A4A16", "BN +"), ("4", "#15171B", "BK salida"), ("3", "#2E90FA", "BU −"))):
        y = (6 - 6 * i) * k
        hilo = Line([(-L / 2 - 24) * k, y, 0], [(-L / 2 - 44) * k, y, 0]).set_stroke(col, 5)
        g.add(hilo)
        b[nombre.split()[0]] = VGroup(Dot(hilo.get_end(), radius=0.6 * k, color=col))
        g.add(txt(f"{n} {nombre}", 2.6 * k, FUERA["c"]).next_to(hilo, UP, buff=0.4 * k).shift(LEFT * 2 * k))
    g.add(txt(f"-{ref}", 3.4 * k, FUERA["c"]).move_to([-4 * k, 17 * k, 0]))
    g.b, g.led, g.k = b, led, k
    g.ficha = dict(nombre=f"Sensor {tipo}", W=L, H=18)
    return g


def flotador(k=K0, ref="S5"):
    """Interruptor de nivel tipo pera (cable de 3 hilos): común + contacto que cierra al subir + contacto que cierra al bajar.
    Colores de los hilos según el fabricante (verificar en su hoja); se rotulan C, NA y NC."""
    g = VGroup()
    pera = RoundedRectangle(width=40 * k, height=62 * k, corner_radius=16 * k, stroke_color=BORDE, stroke_width=1.4).set_fill(CUERPO, 1)
    g.add(_sombra(pera, k), pera, RoundedRectangle(width=30 * k, height=46 * k, corner_radius=12 * k, stroke_width=0).set_fill(CUERPO_CL, 1),
          logo_marca(6 * k).move_to([0, 6 * k, 0]), txt(f"-{ref}", 3.4 * k, TXT_EQ).move_to([0, -8 * k, 0]))
    cuello = RoundedRectangle(width=10 * k, height=12 * k, corner_radius=2 * k, stroke_width=0).set_fill("#2B2F36", 1).next_to(pera, DOWN, buff=-2 * k)
    cable = CubicBezier(cuello.get_bottom(), cuello.get_bottom() + DOWN * 20 * k, cuello.get_bottom() + DOWN * 20 * k + LEFT * 30 * k, cuello.get_bottom() + LEFT * 40 * k + DOWN * 5 * k).set_stroke("#2B2F36", 9)
    g.add(cable, cuello)
    b = {}
    fin = cable.get_end()
    for i, (n, col) in enumerate((("C", "#15171B"), ("NA", "#7A4A16"), ("NC", "#2E90FA"))):
        y = (6 - 6 * i) * k
        h = Line(fin, fin + LEFT * 22 * k + UP * y).set_stroke(col, 4)
        g.add(h, txt(n, 3.2 * k, FUERA["c"]).next_to(h.get_end(), LEFT, buff=0.6 * k))
        b[n] = VGroup(Dot(h.get_end(), radius=0.6 * k, color=col))
    g.b, g.k = b, k
    g.ficha = dict(nombre="Flotador", W=40, H=62)
    return g


# =================================================================== MOTOR, PLACA DE DATOS Y CAJA DE BORNES
def motor(k=K0, ref="M1", trifasico=True, carcasa=1.0):
    """Motor TEFC (vista lateral): aletas, caja de bornes, eje con chaveta, patas. Escala dada por 'carcasa'."""
    s = carcasa
    W, H = 260 * s, 180 * s
    g = VGroup()
    azul = "#3E6A9E"
    cu = RoundedRectangle(width=W * k, height=H * k, corner_radius=16 * k * s, stroke_color="#1F3A5B", stroke_width=2).set_fill(azul, 1)
    g.add(cu)
    for i in range(9):
        y = (-H / 2 + 22 * s + i * (H - 44 * s) / 8) * k
        g.add(Line([(-W / 2 + 18 * s) * k, y, 0], [(W / 2 - 22 * s) * k, y, 0]).set_stroke("#2D5280", 6))
    tapa_v = RoundedRectangle(width=55 * s * k, height=(H - 18 * s) * k, corner_radius=22 * s * k, stroke_color="#1F3A5B", stroke_width=2).set_fill("#35608F", 1).move_to([(-W / 2 - 20 * s) * k, 0, 0])
    g.add_to_back(tapa_v)
    for y in np.linspace(-H / 2 + 30 * s, H / 2 - 30 * s, 7):
        g.add(Line([(-W / 2 - 40 * s) * k, y * k, 0], [(-W / 2 - 5 * s) * k, y * k, 0]).set_stroke("#22476F", 3))
    eje = Rectangle(width=60 * s * k, height=28 * s * k, stroke_color="#667085", stroke_width=1.4).set_fill(METAL, 1).move_to([(W / 2 + 30 * s) * k, 0, 0])
    chav = Rectangle(width=34 * s * k, height=7 * s * k, stroke_width=0).set_fill("#5B6472", 1).move_to(eje.get_center() + UP * 6 * s * k + RIGHT * 6 * s * k)
    g.add(eje, chav)
    caja_b = RoundedRectangle(width=90 * s * k, height=50 * s * k, corner_radius=6 * s * k, stroke_color="#1F3A5B", stroke_width=2).set_fill("#4B79B0", 1).move_to([0, (H / 2 + 22 * s) * k, 0])
    g.add(caja_b, Circle(radius=9 * s * k, stroke_color="#1F3A5B", stroke_width=1.5).set_fill("#2B2F36", 1).move_to(caja_b.get_left() + LEFT * 6 * s * k))
    for x in (-W / 2 + 40 * s, W / 2 - 40 * s):
        g.add(Polygon([(x - 26 * s) * k, (-H / 2 - 22 * s) * k, 0], [(x + 26 * s) * k, (-H / 2 - 22 * s) * k, 0], [(x + 16 * s) * k, (-H / 2 + 4 * s) * k, 0], [(x - 16 * s) * k, (-H / 2 + 4 * s) * k, 0], stroke_color="#1F3A5B", stroke_width=1.5).set_fill("#35608F", 1))
    placa = RoundedRectangle(width=70 * s * k, height=40 * s * k, corner_radius=3 * s * k, stroke_color="#667085", stroke_width=1).set_fill("#D0D5DD", 1).move_to([10 * s * k, -6 * s * k, 0])
    g.add(placa, txt("3~" if trifasico else "1~", 9 * s * k, TXT_OS).move_to(placa.get_center() + UP * 6 * s * k), txt(f"-{ref}", 7 * s * k, TXT_OS).move_to(placa.get_center() + DOWN * 9 * s * k))
    g.eje, g.chaveta, g.caja_b, g.k = eje, chav, caja_b, k
    g.ficha = dict(nombre="Motor", W=W, H=H)
    return g


def girar_eje(m, rps=2.0):
    t0 = [0.0]
    ini = m.chaveta.get_center().copy()
    c = m.eje.get_center()
    amp = m.eje.height * 0.36

    def upd(mob, dt):
        t0[0] += dt
        mob.move_to([mob.get_center()[0], c[1] + amp * np.sin(2 * PI * rps * t0[0]), 0])
        mob.set_opacity(0.4 + 0.6 * abs(np.cos(2 * PI * rps * t0[0])))
    m.chaveta.add_updater(upd)


def placa_datos(datos, k=K0, ancho=110):
    """Placa de características (filas de pares) en estilo plano. datos: lista de (izq, der)."""
    H = 10 + 9 * len(datos)
    g = VGroup(RoundedRectangle(width=ancho * k, height=H * k, corner_radius=2 * k, stroke_color="#667085", stroke_width=1.4).set_fill("#E7E9EC", 1))
    for i, (a, b) in enumerate(datos):
        y = (H / 2 - 9 - 9 * i) * k
        g.add(txt(a, 3.0 * k, TXT_OS).move_to([-ancho / 4 * k, y, 0]), txt(b, 3.0 * k, TXT_OS).move_to([ancho / 4 * k, y, 0]))
        if i:
            g.add(Line([(-ancho / 2 + 4) * k, y + 4.5 * k, 0], [(ancho / 2 - 4) * k, y + 4.5 * k, 0]).set_stroke("#C3C8CF", 1))
    return g


def caja_bornes_9(k=K0, conexion="bajo"):
    """Placa de conexión de un motor NEMA de 9 puntas en triángulo (dato de catálogo: '9-lead Δ').
    Tensión baja (230 V): unir T1-T6-T7, T2-T4-T8, T3-T5-T9; línea a T1 T2 T3.
    Tensión alta (460 V): unir T4-T7, T5-T8, T6-T9; línea a T1 T2 T3."""
    g = VGroup(RoundedRectangle(width=110 * k, height=80 * k, corner_radius=6 * k, stroke_color="#1F3A5B", stroke_width=2).set_fill("#3E6A9E", 1),
               RoundedRectangle(width=100 * k, height=70 * k, corner_radius=4 * k, stroke_width=0).set_fill("#E8E2D0", 1))
    grupos = (("T1", "T6", "T7"), ("T2", "T4", "T8"), ("T3", "T5", "T9")) if conexion == "bajo" else (("T1",), ("T2",), ("T3",), ("T4", "T7"), ("T5", "T8"), ("T6", "T9"))
    b = {}
    pos = {}
    if conexion == "bajo":
        for i, gr in enumerate(grupos):
            for j, n in enumerate(gr):
                pos[n] = np.array([(-30 + 30 * i) * k, (20 - 18 * j) * k, 0])
    else:
        for i, n in enumerate(("T1", "T2", "T3")):
            pos[n] = np.array([(-30 + 30 * i) * k, 22 * k, 0])
        for i, (a, c) in enumerate((("T4", "T7"), ("T5", "T8"), ("T6", "T9"))):
            pos[a] = np.array([(-30 + 30 * i) * k, 2 * k, 0])
            pos[c] = np.array([(-30 + 30 * i) * k, -16 * k, 0])
    for n, p in pos.items():
        punta = VGroup(Circle(radius=4 * k, stroke_color="#7A5A10", stroke_width=1).set_fill("#C9A227", 1).move_to(p))
        g.add(punta, txt(n, 3 * k, TXT_OS).next_to(punta, RIGHT, buff=1.2 * k))
        b[n] = punta
    for gr in (grupos if conexion == "bajo" else grupos[3:]):
        if len(gr) > 1:
            pts = [pos[n] for n in gr]
            g.add(Line(pts[0], pts[-1]).set_stroke("#B54708", 7, 0.85))
    g.b, g.k = b, k
    return g


def caja_bornes_6(k=K0, conexion="delta"):
    """Placa IEC de 6 bornes: U1 V1 W1 arriba, W2 U2 V2 abajo. Δ: puentes verticales; Y: puente horizontal abajo."""
    g = VGroup(RoundedRectangle(width=96 * k, height=70 * k, corner_radius=6 * k, stroke_color="#1F3A5B", stroke_width=2).set_fill("#3E6A9E", 1),
               RoundedRectangle(width=86 * k, height=60 * k, corner_radius=4 * k, stroke_width=0).set_fill("#E8E2D0", 1))
    b = {}
    for i, (a, c) in enumerate((("U1", "W2"), ("V1", "U2"), ("W1", "V2"))):
        for n, y in ((a, 12), (c, -12)):
            p = np.array([(-26 + 26 * i) * k, y * k, 0])
            esp = VGroup(Circle(radius=5 * k, stroke_color="#7A5A10", stroke_width=1).set_fill("#C9A227", 1), RegularPolygon(6).scale(3 * k).set_fill("#A8841A", 1).set_stroke("#6E520E", 1)).move_to(p)
            g.add(esp, txt(n, 3.2 * k, TXT_OS).move_to(p + (UP if y > 0 else DOWN) * 9 * k))
            b[n] = esp
    pu = VGroup()
    if conexion == "delta":
        for a, c in (("U1", "W2"), ("V1", "U2"), ("W1", "V2")):
            pu.add(RoundedRectangle(width=6 * k, height=30 * k, corner_radius=1.5 * k, stroke_color="#7A4A16", stroke_width=1).set_fill("#C96F3B", 0.9).move_to((b[a].get_center() + b[c].get_center()) / 2))
    else:
        pu.add(RoundedRectangle(width=58 * k, height=6 * k, corner_radius=1.5 * k, stroke_color="#7A4A16", stroke_width=1).set_fill("#C96F3B", 0.9).move_to(b["U2"].get_center()))
    g.add(pu)
    g.b, g.puentes, g.k = b, pu, k
    return g


# =================================================================== BORNERAS DE CABALLETE
def bornera(nombres, k=K0, ref="X1", tipos=None):
    """Bornera de paso de tornillo (bornes de 6,2 mm). tipos[n]: 'paso' gris, 'N' azul, 'PE' verde/amarillo.
    Vista de frente: número impreso en el centro y tornillo arriba y abajo."""
    tipos = tipos or {}
    g = VGroup()
    sup, inf = {}, {}
    paso = 6.2
    x0 = -paso * (len(nombres) - 1) / 2
    for i, n in enumerate(nombres):
        x = (x0 + i * paso) * k
        t = tipos.get(n, "paso")
        col = {"paso": "#9DA5B0", "N": "#2E90FA", "PE": C_PE[0]}[t]
        cu = RoundedRectangle(width=5.9 * k, height=52 * k, corner_radius=0.8 * k, stroke_color="#5B6472", stroke_width=0.8).set_fill(col, 1).move_to([x, 0, 0])
        g.add(cu)
        if t == "PE":
            for yy in np.arange(-22, 23, 6):
                g.add(Line([x - 2.8 * k, (yy - 2) * k, 0], [x + 2.8 * k, (yy + 2) * k, 0]).set_stroke(C_PE[1], 3))
        tag = RoundedRectangle(width=5 * k, height=6 * k, corner_radius=0.4 * k, stroke_width=0).set_fill(WHITE, 1).move_to([x, 0, 0])
        g.add(tag, txt(n, 2.0 * k, TXT_OS).move_to(tag))
        ts = tornillo(1.8 * k).move_to([x, 17 * k, 0])
        ti = tornillo(1.8 * k).move_to([x, -17 * k, 0])
        g.add(ts, ti)
        sup[n], inf[n] = ts, ti
    tapa = Rectangle(width=2 * k, height=52 * k, stroke_width=0).set_fill("#5B6472", 1).next_to(g, RIGHT, buff=0)
    tope = VGroup(*[Rectangle(width=5 * k, height=56 * k, stroke_color="#344054", stroke_width=0.8).set_fill("#475467", 1) for _ in range(1)]).next_to(g, LEFT, buff=0)
    g.add(tapa, tope)
    g.add(txt(f"-{ref}", 3.6 * k, FUERA["c"]).next_to(tope, UP, buff=1.5 * k))
    g.sup, g.inf, g.k = sup, inf, k
    return g


# =================================================================== RIEL Y CANALETA
def riel_din(largo_mm, k=K0):
    r = VGroup(Rectangle(width=largo_mm * k, height=35 * k, stroke_width=0).set_fill("#A9B0BA", 1),
               Rectangle(width=largo_mm * k, height=25 * k, stroke_width=0).set_fill("#C9CED6", 1))
    for x in np.arange(-largo_mm / 2 + 12, largo_mm / 2, 25):
        r.add(RoundedRectangle(width=11 * k, height=5.2 * k, corner_radius=2.4 * k, stroke_width=0).set_fill("#7C8594", 1).move_to([x * k, 0, 0]))
    return r


def canaleta(largo_mm, ancho_mm=40, k=K0, vertical=False):
    """Canaleta ranurada con tapa (vista de frente)."""
    w, h = (largo_mm * k, ancho_mm * k) if not vertical else (ancho_mm * k, largo_mm * k)
    c = VGroup(Rectangle(width=w, height=h, stroke_color="#7C8594", stroke_width=1).set_fill("#B7BDC6", 1))
    n = int(largo_mm / 8)
    for i in range(n):
        f = (-largo_mm / 2 + (i + 0.5) * largo_mm / n) * k
        if not vertical:
            c.add(Line([f, h / 2, 0], [f, h / 2 - 6 * k, 0]).set_stroke("#8A929E", 1.6), Line([f, -h / 2, 0], [f, -h / 2 + 6 * k, 0]).set_stroke("#8A929E", 1.6))
        else:
            c.add(Line([w / 2, f, 0], [w / 2 - 6 * k, f, 0]).set_stroke("#8A929E", 1.6), Line([-w / 2, f, 0], [-w / 2 + 6 * k, f, 0]).set_stroke("#8A929E", 1.6))
    c.add(Rectangle(width=w - 8 * k, height=h - 8 * k, stroke_width=0).set_fill("#C3C8CF", 1))
    return c


# =================================================================== CONDUCTOR CON PUNTERA Y MARCADOR
def conductor(pts, color=C_POT, w=6, marca=None, k=K0, puntera=True):
    """Conductor con puntera (ferrule) en la punta inicial y marcador con su número (pineado y etiquetado)."""
    pts = [np.array(p, float) for p in pts]
    cab = VMobject().set_points_as_corners(pts).set_stroke(color, w)
    cab.joint_type = LineJointType.ROUND
    g = VGroup(cab.copy().set_stroke("#FFFFFF", w + 2, 0.6), cab)
    if puntera:
        d = pts[1] - pts[0]
        d = d / (np.linalg.norm(d) + 1e-9)
        p = Line(pts[0], pts[0] + d * 7 * k).set_stroke(METAL, w + 1)
        g.add(p)
        if marca:
            r = RoundedRectangle(width=max(7, 2.4 * len(marca) + 3) * k, height=4.5 * k, corner_radius=0.6 * k, stroke_color="#667085", stroke_width=0.8).set_fill(WHITE, 1)
            m = VGroup(r, txt(marca, 2.4 * k, TXT_OS).move_to(r)).move_to(pts[0] + d * 13 * k)
            g.add(m)
    return g

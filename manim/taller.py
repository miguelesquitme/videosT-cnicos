"""Base para los videos horizontales del canal de electricidad: cámara, tarjetas, corriente fluida,
piezas nuevas (interruptor de 3 vías, tomacorriente NEMA 5-15R, foco LED, electrodomésticos) y cierre."""
from nema import *
from comun_e import _osc, _cla
from dibujos_aves import check, equis, PIEL

ELECTRON = "#1E88E5"
ELECTRON_CL = "#7CC8FF"
VIAJERO_1 = "#D92D20"   # rojo
VIAJERO_2 = "#F5B800"   # amarillo
RET_AZUL = "#1F6FEB"    # retorno azul


# ------------------------------------------------------------------ geometría
def paralela(pts, o):
    """Desplaza una polilínea ortogonal una distancia o (normal izquierda)."""
    pts = [np.array(p, float) for p in pts]
    out = []
    for i, p in enumerate(pts):
        ns = []
        if i > 0:
            d = pts[i] - pts[i - 1]
            d /= np.linalg.norm(d)
            ns.append(np.array([-d[1], d[0], 0]))
        if i < len(pts) - 1:
            d = pts[i + 1] - pts[i]
            d /= np.linalg.norm(d)
            ns.append(np.array([-d[1], d[0], 0]))
        off = sum(ns) * o if len(ns) == 2 and abs(np.dot(ns[0], ns[1])) < 0.5 else ns[0] * o
        out.append(p + off)
    return out


def concatenar(*tramos):
    pts = []
    for t in tramos:
        for p in t:
            p = np.array(p, float)
            if not pts or np.linalg.norm(pts[-1] - p) > 1e-4:
                pts.append(p)
    return pts


def inv(t):
    return list(reversed(t))


class Polilinea:
    """Recorrido por distancia (para mover partículas a velocidad constante)."""

    def __init__(self, pts):
        self.p = [np.array(q, float) for q in pts]
        self.l = [np.linalg.norm(b - a) for a, b in zip(self.p[:-1], self.p[1:])]
        self.total = sum(self.l)

    def punto(self, s):
        s = s % self.total
        for a, b, l in zip(self.p[:-1], self.p[1:], self.l):
            if s <= l and l > 0:
                return a + (b - a) * (s / l)
            s -= l
        return self.p[-1]


CIAN_CORRIENTE = "#6FF2FF"


def corriente(pts, n=None, vel=0.7, color=ELECTRON, color2=ELECTRON_CL, escala=1.0, espacio=0.55):
    """Corriente como línea punteada que avanza sobre el conductor (estilo pedido por el usuario, 29-oct-2026)."""
    ruta = Polilinea(pts)
    col = CIAN_CORRIENTE if color == ELECTRON else color
    guion, hueco = 0.085 * escala, 0.065 * escala
    per = guion + hueco
    n = max(3, int(ruta.total / per))
    per = ruta.total / n
    g = VGroup(*[Line(ORIGIN, RIGHT * 0.01).set_stroke(col, 3.6 * escala).set_cap_style(CapStyleType.ROUND) for _ in range(n)])
    fisico(g)
    g.s0 = 0.0

    def upd(m, dt):
        m.s0 = (m.s0 + dt * vel * 0.8) % ruta.total
        for k, d in enumerate(m):
            s = (m.s0 + k * per) % ruta.total
            e = min(s + guion, ruta.total)
            a, b = ruta.punto(s), ruta.punto(e - 1e-6)
            if np.linalg.norm(b - a) < 1e-5:
                b = a + RIGHT * 1e-4
            d.put_start_and_end_on(a, b)
    g.add_updater(upd)
    upd(g, 0)
    return g


def corriente_cometa(pts, n=None, vel=0.55, color=ELECTRON, color2=ELECTRON_CL, escala=1.0, espacio=0.55):
    """Electrones como 'cometas': cabeza brillante + estela que se desvanece. Lento y fluido."""
    ruta = Polilinea(pts)
    n = n or max(4, int(ruta.total / (espacio * escala)))
    cola = 0.22 * escala
    g = VGroup()
    for _ in range(n):
        estela = VGroup(*[Line(ORIGIN, RIGHT * 0.01).set_stroke(color, (4.5 - k) * escala * 1.2, 0.55 - 0.12 * k)
                          for k in range(4)])
        cabeza = VGroup(Circle(radius=0.055 * escala, stroke_width=0).set_fill(color2, 0.45),
                        Circle(radius=0.032 * escala, stroke_width=0).set_fill(color, 1),
                        Circle(radius=0.012 * escala, stroke_width=0).set_fill(WHITE, 0.9))
        for s_ in estela:
            s_.set_cap_style(CapStyleType.ROUND)
        g.add(VGroup(estela, cabeza))
    g.s0 = 0.0

    def upd(m, dt):
        m.s0 += dt * vel * escala
        for k, part in enumerate(m):
            s = m.s0 + k * ruta.total / n
            cab = ruta.punto(s)
            part[1].move_to(cab)
            for j, seg in enumerate(part[0]):
                sa, sb = (s - cola * j / 4) % ruta.total, (s - cola * (j + 1) / 4) % ruta.total
                a = ruta.punto(sa)
                b = ruta.punto(sb) if sb <= sa else a
                if np.linalg.norm(a - b) < 1e-5:
                    b = a + RIGHT * 1e-4
                seg.put_start_and_end_on(b, a)
    g.add_updater(upd)
    upd(g, 0)
    return g


# ------------------------------------------------------------------ piezas parametrizadas
def caja_rect_en(c, w=SW_W, h=SW_H, tornillo_tierra=True):
    caja = Rectangle(width=w, height=h, stroke_color=METAL_OSC, stroke_width=1.6).set_fill(GAL, 1).move_to(c)
    fondo = Rectangle(width=w - 0.16, height=h - 0.16, stroke_color=METAL2, stroke_width=0.8).set_fill(GAL2, 1).move_to(c)
    biseles = VGroup(*[Line(a, b, stroke_color=METAL2, stroke_width=0.7) for a, b in zip(caja.get_vertices(), fondo.get_vertices())])
    orejas = VGroup()
    for s in (1, -1):
        o = RoundedRectangle(width=0.36, height=0.16, corner_radius=0.03, stroke_color=METAL_OSC, stroke_width=1.1).set_fill(GAL, 1)
        o.move_to(c + P(0, s * (h / 2 - 0.1)))
        orejas.add(VGroup(o, tornillo(0.035, METAL, 0.2).move_to(o)))
    kos = VGroup(*[knockout(c + P(s * (w / 2 - 0.18), y), 0.06, METAL2, GAL2) for s in (-1, 1) for y in (0.45, -0.45)])
    g = VGroup(caja, fondo, biseles, kos, orejas)
    g.tierra = None
    if tornillo_tierra:
        t = tornillo(0.04, TIERRA, 0.3).move_to(c + P(w / 2 - 0.2, -h / 2 + 0.3))
        g.add(t)
        g.tierra = t
    return g


def interruptor3(c, pos=1):
    """Interruptor de 3 vías: común (tornillo oscuro) a la izquierda, dos viajeros de latón a la derecha,
    tornillo verde en el yugo. pos=1 → común unido al viajero de arriba; pos=2 → al de abajo."""
    yugo = RoundedRectangle(width=0.34, height=1.46, corner_radius=0.05, stroke_color=METAL_OSC, stroke_width=1.1).set_fill("#D9DDE3", 1).move_to(c)
    orejas = VGroup(*[RoundedRectangle(width=0.5, height=0.14, corner_radius=0.03, stroke_color=METAL_OSC, stroke_width=1)
                      .set_fill("#E4E7EC", 1).move_to(c + P(0, s * 0.66)) for s in (1, -1)])
    ranuras_o = VGroup(*[RoundedRectangle(width=0.14, height=0.05, corner_radius=0.02, stroke_width=0.7, stroke_color=METAL_OSC)
                         .set_fill(WHITE, 1).move_to(c + P(0, s * 0.66)) for s in (1, -1)])
    tm = VGroup(*[tornillo(0.035, "#E4E7EC", 0.2).move_to(c + P(0, s * 0.55)) for s in (1, -1)])
    cuerpo = RoundedRectangle(width=0.44, height=0.86, corner_radius=0.07, stroke_color=LINEA, stroke_width=1.1).set_fill("#F7F7F5", 1).move_to(c)
    guia = RoundedRectangle(width=0.17, height=0.5, corner_radius=0.05, stroke_color=METAL2, stroke_width=0.8).set_fill("#ECEBE7", 1).move_to(c)
    pal = VGroup(RoundedRectangle(width=0.13, height=0.34, corner_radius=0.05, stroke_color=LINEA, stroke_width=1).set_fill(WHITE, 1))
    pal.move_to(c + P(0, 0.12 if pos == 1 else -0.12))
    t1 = borne(c + P(0.28, 0.27), 0.05, LATON)
    t2 = borne(c + P(0.28, -0.27), 0.05, LATON)
    com = borne(c + P(-0.28, 0.12), 0.05, "#3A3F47")
    v = tornillo(0.042, TIERRA, 0.4).move_to(c + P(-0.06, -0.5))
    hex_ = RegularPolygon(6).scale(0.055).set_fill("#0E8A3E", 1).set_stroke("#0B5E2B", 0.8).move_to(v)
    g = VGroup(yugo, orejas, ranuras_o, cuerpo, guia, pal, t1, t2, com, hex_, v, tm)
    g.t1, g.t2, g.com, g.verde, g.palanca, g.guia, g.pos = t1.tor, t2.tor, com.tor, v, pal, guia, pos
    return g


def palanca3(sw, pos):
    sw.pos = pos
    return sw.palanca.animate.move_to(sw.guia.get_center() + P(0, 0.12 if pos == 1 else -0.12))


def foco_led(encendido=False, h=0.9):
    """Foco LED A19, base arriba: difusor lechoso, cuerpo disipador con aletas, base E26."""
    s = h / 0.9
    dif = VMobject().set_points_smoothly([P(-0.14, 0.12), P(-0.31, -0.05), P(-0.34, -0.28), P(-0.2, -0.5), P(0, -0.55),
                                          P(0.2, -0.5), P(0.34, -0.28), P(0.31, -0.05), P(0.14, 0.12), P(-0.14, 0.12)])
    dif.set_fill("#FFF8DA" if encendido else "#F7F8FA", 1).set_stroke(LINEA, 1.1)
    brillo = Arc(radius=0.2, start_angle=PI * 0.62, angle=PI * 0.4, arc_center=P(0.02, -0.25)).set_stroke(WHITE, 2.4, 0.95)
    cuerpo = Polygon(P(-0.16, 0.12), P(0.16, 0.12), P(0.13, 0.3), P(-0.13, 0.3), stroke_color=METAL_OSC, stroke_width=1).set_fill("#E4E7EC", 1)
    aletas = VGroup(*[Line(P(x, 0.13), P(x * 0.82, 0.29), stroke_color="#B8BEC8", stroke_width=0.8) for x in (-0.1, -0.03, 0.04, 0.11)])
    rosca = VGroup(RoundedRectangle(width=0.23, height=0.17, corner_radius=0.02, stroke_color=METAL_OSC, stroke_width=0.9)
                   .set_fill("#D0D5DD", 1).move_to(P(0, 0.385)),
                   *[VMobject().set_points_smoothly([P(-0.115, 0.32 + 0.045 * k), P(0, 0.34 + 0.045 * k), P(0.115, 0.32 + 0.045 * k)])
                     .set_stroke(METAL_OSC, 0.8) for k in range(3)],
                   Polygon(P(-0.065, 0.47), P(0.065, 0.47), P(0.035, 0.51), P(-0.035, 0.51), stroke_width=0).set_fill(NEGRO_BK, 1),
                   Dot(P(0, 0.52), radius=0.02, color=LATON))
    chips = VGroup(*[Rectangle(width=0.035, height=0.02, stroke_width=0).set_fill("#F5B800" if encendido else "#C9CED6", 1)
                     .move_to(P(x, 0.08)) for x in (-0.07, 0, 0.07)])
    g = VGroup(dif, chips, brillo, cuerpo, aletas, rosca).scale(s)
    g.vidrio = dif
    return g


def portalampara_led(c=None):
    g = portalampara(None)
    f = foco_led(False, 0.85)
    f.move_to(g.foco)
    g.remove(g.foco)
    g.add_to_back(f)
    g.foco = f
    if c is not None:
        g.shift(c)
    return g


def tomacorriente(c, tr=True):
    """Tomacorriente dúplex NEMA 5-15R con tierra: ranura corta = fase, larga = neutro, U = tierra.
    Bornes de latón (fase) a la derecha y plateados (neutro) a la izquierda con pestañas; verde abajo."""
    yugo = RoundedRectangle(width=0.36, height=1.46, corner_radius=0.05, stroke_color=METAL_OSC, stroke_width=1.1).set_fill("#D9DDE3", 1).move_to(c)
    orejas = VGroup(*[RoundedRectangle(width=0.52, height=0.14, corner_radius=0.03, stroke_color=METAL_OSC, stroke_width=1)
                      .set_fill("#E4E7EC", 1).move_to(c + P(0, s * 0.66)) for s in (1, -1)])
    tm = VGroup(*[tornillo(0.035, "#E4E7EC", 0.2).move_to(c + P(0, s * 0.55)) for s in (1, -1)])
    cuerpo = RoundedRectangle(width=0.5, height=0.98, corner_radius=0.08, stroke_color=LINEA, stroke_width=1.1).set_fill("#F7F7F5", 1).move_to(c)
    caras = VGroup()
    for s in (1, -1):
        cc = c + P(0, s * 0.24)
        cara = RoundedRectangle(width=0.38, height=0.36, corner_radius=0.13, stroke_color="#C7C5BE", stroke_width=0.9).set_fill("#FBFBF9", 1).move_to(cc)
        fase_r = RoundedRectangle(width=0.035, height=0.1, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(cc + P(0.08, 0.04))
        neu_r = RoundedRectangle(width=0.035, height=0.13, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(cc + P(-0.08, 0.04))
        tie = VGroup(Arc(radius=0.035, start_angle=PI, angle=PI, stroke_width=0).set_fill("#2A2E35", 1),
                     Rectangle(width=0.07, height=0.03, stroke_width=0).set_fill("#2A2E35", 1).shift(UP * 0.015)).move_to(cc + P(0, -0.1))
        caras.add(VGroup(cara, fase_r, neu_r, tie))
    tor_c = tornillo(0.03, "#E4E7EC", 0.3).move_to(c)
    marca = T("TR", 6, "#98A2B3", "BOLD").move_to(c + P(0.17, 0.0)) if tr else VGroup()
    bl1, bl2 = borne(c + P(0.31, 0.24), 0.05, LATON), borne(c + P(0.31, -0.24), 0.05, LATON)
    bp1, bp2 = borne(c + P(-0.31, 0.24), 0.05, "#E4E7EC"), borne(c + P(-0.31, -0.24), 0.05, "#E4E7EC")
    pest_l = Rectangle(width=0.05, height=0.3, stroke_color="#8A6D12", stroke_width=0.7).set_fill(LATON, 1).move_to(c + P(0.31, 0))
    pest_p = Rectangle(width=0.05, height=0.3, stroke_color=METAL_OSC, stroke_width=0.7).set_fill("#D0D5DD", 1).move_to(c + P(-0.31, 0))
    v = tornillo(0.042, TIERRA, 0.4).move_to(c + P(0.0, -0.6))
    hex_ = RegularPolygon(6).scale(0.055).set_fill("#0E8A3E", 1).set_stroke("#0B5E2B", 0.8).move_to(v)
    g = VGroup(yugo, orejas, tm, pest_l, pest_p, cuerpo, caras, tor_c, marca, bl1, bl2, bp1, bp2, hex_, v)
    g.l1, g.l2, g.p1, g.p2, g.verde, g.caras, g.pest_l = bl1.tor, bl2.tor, bp1.tor, bp2.tor, v, caras, pest_l
    return g


def placa_toma(c):
    pl = RoundedRectangle(width=0.82, height=1.3, corner_radius=0.06, stroke_color=METAL2, stroke_width=1.3).set_fill("#FBFBFA", 1).move_to(c)
    hs = VGroup()
    for s in (1, -1):
        cc = c + P(0, s * 0.24)
        hs.add(RoundedRectangle(width=0.4, height=0.38, corner_radius=0.14, stroke_color="#D0D5DD", stroke_width=1).set_fill("#F7F7F5", 1).move_to(cc),
               RoundedRectangle(width=0.035, height=0.1, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(cc + P(0.08, 0.04)),
               RoundedRectangle(width=0.035, height=0.13, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(cc + P(-0.08, 0.04)),
               Arc(radius=0.035, start_angle=PI, angle=PI, stroke_width=0).set_fill("#2A2E35", 1).move_to(cc + P(0, -0.1)))
    return VGroup(pl, hs, tornillo(0.03, METAL, 0.3).move_to(c))


def placa_interruptor(c, pos=1):
    pl = RoundedRectangle(width=0.82, height=1.3, corner_radius=0.06, stroke_color=METAL2, stroke_width=1.3).set_fill("#FBFBFA", 1).move_to(c)
    pal = RoundedRectangle(width=0.14, height=0.32, corner_radius=0.05, stroke_color=LINEA, stroke_width=1).set_fill(WHITE, 1)
    pal.move_to(c + P(0, 0.12 if pos == 1 else -0.12))
    tor = VGroup(tornillo(0.035, METAL, 0.3).move_to(c + P(0, 0.45)), tornillo(0.035, METAL, 0.3).move_to(c + P(0, -0.45)))
    g = VGroup(pl, pal, tor)
    g.pal, g.c = pal, c
    return g


def cable_hilos(largo=2.0, color=FASE, w=0.5, pelado=0.6, abierto=False):
    """Cable de 7 hilos de cerca: aislamiento + hilos de cobre (abiertos o torcidos)."""
    ais = RoundedRectangle(width=largo, height=w, corner_radius=w / 2, stroke_color=_osc(color, 0.4) if color != NEUTRO else NEUTRO_BORDE,
                           stroke_width=1.4).set_fill(color, 1)
    ais.move_to(LEFT * pelado / 2)
    brillo = Line(ais.get_left() + RIGHT * 0.2 + UP * w * 0.22, ais.get_right() + LEFT * 0.2 + UP * w * 0.22,
                  stroke_color=WHITE, stroke_width=2, stroke_opacity=0.35)
    x0 = ais.get_right()[0] - 0.05
    hilos = VGroup()
    for k in range(7):
        y = (k - 3) * w * 0.11
        if abierto:
            pts = [P(x0, y * 0.9), P(x0 + pelado * 0.5, y * 1.6), P(x0 + pelado, y * 2.4)]
        else:
            pts = [P(x0, y * 0.9), P(x0 + pelado * 0.5, y * 0.6), P(x0 + pelado, y * 0.35)]
        h = VMobject().set_points_smoothly(pts).set_stroke(COBRE, 3.2)
        hilos.add(VGroup(h.copy().set_stroke(_osc(COBRE, 0.4), 4.6), h))
    espiral = VGroup(*[Line(P(x0 + pelado * t, -w * 0.25), P(x0 + pelado * (t + 0.07), w * 0.25), stroke_color=_osc(COBRE, 0.35), stroke_width=1.1)
                       for t in np.arange(0.05, 0.9, 0.12)]) if not abierto else VGroup()
    return VGroup(hilos, espiral, ais, brillo)


# ------------------------------------------------------------------ electrodomésticos (para la ley de Ohm)
def hervidor():
    cuerpo = Polygon(P(-0.55, -0.6), P(0.55, -0.6), P(0.45, 0.45), P(-0.45, 0.45), stroke_color=LINEA, stroke_width=1.4).set_fill("#E4E7EC", 1)
    tapa = RoundedRectangle(width=0.7, height=0.14, corner_radius=0.06, stroke_color=LINEA, stroke_width=1.2).set_fill("#344054", 1).move_to(P(0, 0.52))
    asa = VMobject().set_points_smoothly([P(0.45, 0.35), P(0.85, 0.3), P(0.85, -0.3), P(0.5, -0.4)]).set_stroke("#344054", 9)
    pico = Polygon(P(-0.5, 0.2), P(-0.85, 0.42), P(-0.82, 0.48), P(-0.46, 0.38), stroke_color=LINEA, stroke_width=1.2).set_fill("#E4E7EC", 1)
    base = RoundedRectangle(width=1.3, height=0.16, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.2).set_fill("#344054", 1).move_to(P(0, -0.7))
    nivel = Line(P(0.3, -0.4), P(0.28, 0.2), stroke_color=MARCA, stroke_width=4)
    brillo = Line(P(-0.32, -0.45), P(-0.26, 0.3), stroke_color=WHITE, stroke_width=3, stroke_opacity=0.8)
    return VGroup(asa, cuerpo, pico, tapa, base, nivel, brillo)


def plancha():
    suela = Polygon(P(-0.9, -0.3), P(0.75, -0.3), P(0.95, -0.15), P(0.6, 0.15), P(-0.9, 0.15), stroke_color=LINEA, stroke_width=1.3).set_fill("#B8BEC8", 1)
    cuerpo = VMobject().set_points_smoothly([P(-0.85, 0.15), P(-0.7, 0.45), P(0.1, 0.5), P(0.6, 0.18)]).add_line_to(P(-0.85, 0.15))
    cuerpo.set_fill(MARCA, 1).set_stroke(LINEA, 1.3)
    asa = VMobject().set_points_smoothly([P(-0.65, 0.45), P(-0.55, 0.85), P(0.15, 0.85), P(0.1, 0.5)]).set_stroke("#1D2939", 9)
    perilla = Circle(radius=0.07, stroke_color=LINEA, stroke_width=1).set_fill(AMBAR, 1).move_to(P(-0.2, 0.33))
    return VGroup(asa, cuerpo, suela, perilla)


def microondas():
    caja = RoundedRectangle(width=1.9, height=1.1, corner_radius=0.08, stroke_color=LINEA, stroke_width=1.4).set_fill("#F2F4F7", 1)
    puerta = RoundedRectangle(width=1.25, height=0.85, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.1).set_fill("#344054", 1).shift(LEFT * 0.25)
    vidrio = RoundedRectangle(width=1.05, height=0.65, corner_radius=0.04, stroke_width=0).set_fill("#475467", 1).move_to(puerta)
    panel = VGroup(Rectangle(width=0.36, height=0.14, stroke_width=0).set_fill("#101318", 1).move_to(P(0.65, 0.3)),
                   *[Circle(radius=0.035, stroke_width=0.8, stroke_color=LINEA).set_fill(WHITE, 1).move_to(P(0.6 + 0.1 * (k % 3), 0.05 - 0.1 * (k // 3)))
                     for k in range(9)])
    return VGroup(caja, puerta, vidrio, panel)


def ventilador():
    base = RoundedRectangle(width=0.9, height=0.12, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.2).set_fill("#344054", 1).move_to(P(0, -1.0))
    poste_ = Rectangle(width=0.08, height=0.8, stroke_color=LINEA, stroke_width=1).set_fill("#D0D5DD", 1).move_to(P(0, -0.55))
    jaula = Circle(radius=0.6, stroke_color=METAL_OSC, stroke_width=1.6).set_fill(WHITE, 0.2).move_to(P(0, 0.35))
    rayos = VGroup(*[Line(P(0, 0.35), P(0, 0.35) + 0.6 * np.array([np.cos(a), np.sin(a), 0]), stroke_color=METAL2, stroke_width=0.8)
                     for a in np.linspace(0, TAU, 12, endpoint=False)])
    aspas = VGroup(*[Ellipse(width=0.22, height=0.48, stroke_color=_osc(MARCA, 0.3), stroke_width=1).set_fill(MARCA, 0.85)
                     .move_to(P(0, 0.35) + 0.27 * np.array([np.cos(a), np.sin(a), 0])).rotate(a - PI / 2) for a in (PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3)])
    centro = Circle(radius=0.08, stroke_width=0).set_fill("#344054", 1).move_to(P(0, 0.35))
    return VGroup(base, poste_, aspas, centro, rayos, jaula)


def regleta():
    cuerpo = RoundedRectangle(width=2.6, height=0.5, corner_radius=0.12, stroke_color=LINEA, stroke_width=1.3).set_fill(WHITE, 1)
    tomas = VGroup(*[VGroup(RoundedRectangle(width=0.36, height=0.34, corner_radius=0.12, stroke_color="#C7C5BE", stroke_width=0.9).set_fill("#F7F7F5", 1),
                            RoundedRectangle(width=0.03, height=0.09, corner_radius=0.01, stroke_width=0).set_fill("#2A2E35", 1).shift(RIGHT * 0.07 + UP * 0.03),
                            RoundedRectangle(width=0.03, height=0.12, corner_radius=0.01, stroke_width=0).set_fill("#2A2E35", 1).shift(LEFT * 0.07 + UP * 0.03),
                            Dot(radius=0.025, color="#2A2E35").shift(DOWN * 0.1)).move_to(P(-0.85 + 0.5 * k, 0)) for k in range(4)])
    boton = RoundedRectangle(width=0.22, height=0.26, corner_radius=0.05, stroke_color="#B42318", stroke_width=1).set_fill(ROJO, 1).move_to(P(1.1, 0))
    cordon = VMobject().set_points_smoothly([P(-1.3, 0), P(-1.7, -0.1), P(-1.9, -0.5)]).set_stroke("#1D2939" if TEMA != "oscuro" else "#9AA6D1", 5)
    return VGroup(cordon, cuerpo, tomas, boton)


def gancho_amperimetro():
    cuerpo = RoundedRectangle(width=0.7, height=1.6, corner_radius=0.18, stroke_color="#B54708", stroke_width=1.4).set_fill(AMBAR, 1)
    pantalla = RoundedRectangle(width=0.52, height=0.34, corner_radius=0.04, stroke_width=0).set_fill("#C9D6C3", 1).shift(DOWN * 0.1)
    mordaza = VGroup(Arc(radius=0.42, start_angle=PI * 0.05, angle=PI * 0.9, stroke_color="#101318", stroke_width=14).shift(UP * 1.0))
    gatillo = RoundedRectangle(width=0.12, height=0.3, corner_radius=0.04, stroke_width=0).set_fill("#101318", 1).move_to(P(0.35, 0.45))
    g = VGroup(mordaza, cuerpo, pantalla, gatillo)
    g.lcd = pantalla
    return g


# ------------------------------------------------------------------ escena base
class TallerH(Escena):
    FIN_SEG = 7.0          # pantalla final corta (YouTube pide mínimo 5 s)
    DURACION_MIN = 482.0   # ≥ 8:00 para anuncios a mitad del video

    @property
    def z(self):
        return self.camera.frame.width / 16

    def ir(self, centro, ancho, rt=1.2, *extra):
        self.play(self.camera.frame.animate.set(width=ancho).move_to(centro), *extra, run_time=rt)

    def pant(self, m, pos):
        p = np.array(list(pos) + [0] * (3 - len(pos)), float)
        for sm in m.family_members_with_points():
            sm.fisico = False
        m.scale(self.z).move_to(self.camera.frame.get_center() + p * self.z)
        return m

    def chip(self, texto, pos_mundo, color=MARCA, size=24, solido=False):
        return pastilla(texto, color, size, solido).scale(self.z).move_to(pos_mundo)

    def carta_nec(self, codigo, texto, pos=(4.6, 2.9), ancho=5.6, color=MARCA):
        cod = pastilla(codigo, color, 24, True)
        lineas = VGroup(*[T(l, 24, TINTA, "MEDIUM") for l in texto.split("\n")]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        cuerpo = VGroup(cod, lineas).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        caja = tarjeta(max(ancho, cuerpo.width + 0.5), cuerpo.height + 0.45, color=interpolate_color(ManimColor(color), ManimColor(WHITE), 0.3))
        caja.set_stroke(width=1.4)
        cuerpo.move_to(caja)
        return self.pant(VGroup(sombra(caja), caja, cuerpo), pos)

    def limpiar(self, *ms, t=0.4):
        ms = [m for m in ms if m is not None]
        for m in ms:
            for s in m.get_family():
                s.clear_updaters()
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=t)

    def limpiar_todo(self, t=0.4):
        ms = [m for m in self.mobjects[1:] if m is not self.camera.frame]
        self.limpiar(*ms, t=t)

    def esperar_frac(self, f):
        w = self.resta() * f
        if w > 0.05:
            self.wait(w)

    def apretar(self, objetivo, t=1.0):
        d = destornillador(1.4).scale(self.z * 1.4)
        punta = d[1].get_bottom()
        d.shift(objetivo.get_center() - punta + UP * 0.6 * self.z)
        self.play(FadeIn(d), d.animate.shift(DOWN * 0.6 * self.z), run_time=0.4)
        self.play(Rotate(objetivo[1], PI * 1.5), run_time=t * 0.5)
        self.play(FadeOut(d, shift=UP * 0.4 * self.z), run_time=0.3)

    def titulo(self, l1, l2, sub, ilustracion=None):
        t1 = T(l1, 60, TINTA, "HEAVY")
        t2 = T(l2, 74, MARCA, "HEAVY")
        t3 = T(sub, 30, TINTA2, "MEDIUM")
        tit = VGroup(t1, t2, t3).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        if tit.width > 8.6:
            tit.scale_to_fit_width(8.6)
        tit.move_to([2.4, 0.9, 0])
        barra = RoundedRectangle(width=1.4, height=0.1, corner_radius=0.05, stroke_width=0).set_fill(MARCA, 1)
        barra.next_to(tit, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(tit, shift=RIGHT * 0.3), GrowFromEdge(barra, LEFT), run_time=0.8)
        return VGroup(tit, barra)

    def tarjetas(self, items, titulo_txt="MATERIALES", filas=2, cols=4, w=3.4, h=3.0):
        tit = T(titulo_txt, 46, TINTA, "HEAVY").move_to([0, 3.75, 0])
        self.play(FadeIn(tit), run_time=0.3)
        celdas = VGroup()
        for fn, nombre in items:
            caja = tarjeta(w, h, METAL)
            ic = fn()
            if ic.height > h * 0.5:
                ic.scale_to_fit_height(h * 0.5)
            if ic.width > w * 0.78:
                ic.scale_to_fit_width(w * 0.78)
            ic.move_to(caja.get_center() + UP * 0.35)
            nm = VGroup(*[T(l, 21, TINTA, "BOLD") for l in nombre.split("\n")]).arrange(DOWN, buff=0.06)
            nm.move_to(caja.get_center() + DOWN * (h / 2 - 0.5))
            celdas.add(VGroup(caja, ic, nm))
        celdas.arrange_in_grid(filas, cols, buff=(0.35, 0.3)).move_to([0, -0.2, 0])
        dur = max(3.0, self.resta() - 1.2)
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.25) for c_ in celdas], lag_ratio=0.85), run_time=dur)
        return VGroup(tit, celdas)

    def tres_errores(self, textos, ilus):
        tit = T("3 ERRORES MUY COMUNES", 46, TINTA, "HEAVY").move_to([0, 3.7, 0])
        self.play(FadeIn(tit), run_time=0.4)
        cartas = VGroup()
        for (num, t1, t2), il in zip(textos, ilus):
            caja = tarjeta(4.7, 5.6, METAL)
            n = VGroup(Circle(radius=0.32, stroke_width=0).set_fill(ROJO, 1), T(num, 30, WHITE, "HEAVY"))
            n[1].move_to(n[0])
            n.move_to(caja.get_top() + DOWN * 0.55)
            a = VGroup(*[T(l, 26, TINTA, "HEAVY") for l in t1.split("\n")]).arrange(DOWN, buff=0.05).next_to(n, DOWN, buff=0.22)
            il.scale_to_fit_width(3.3)
            if il.height > 1.7:
                il.scale_to_fit_height(1.7)
            il.move_to(caja.get_center() + DOWN * 0.25)
            b = VGroup(*[T(l, 21, TINTA2, "MEDIUM") for l in t2.split("\n")]).arrange(DOWN, buff=0.06)
            b.move_to(caja.get_bottom() + UP * 0.75)
            cartas.add(VGroup(caja, n, a, il, b))
        cartas.arrange(RIGHT, buff=0.35).move_to([0, -0.5, 0])
        cortes = [0.02, 0.3, 0.4]
        for k, c_ in enumerate(cartas):
            self.esperar_frac(cortes[k])
            self.sfx("pop", -10)
            self.play(FadeIn(c_, shift=UP * 0.3), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(tit, cartas)

    def f_seguridad(self):
        """Tres pasos de seguridad: bajar breaker, verificar sin tensión, nunca suponer."""
        self.voz("seguridad")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        tit = T("ANTES DE TOCAR UN CABLE", 46, TINTA, "HEAVY").move_to([0, 3.5, 0])
        self.play(FadeIn(tit), run_time=0.3)
        cartas = VGroup()
        bk = breaker("20", 0.46, 0.26).scale(5.0)
        pr = probador().scale(2.6).rotate(-0.4)
        ojo = VGroup(check(VERDE_OK, 0.6))
        for k, (il, txt) in enumerate(((bk, "1 · Baja el breaker"), (pr, "2 · Verifica sin tensión"), (ojo, "3 · Compruébalo siempre"))):
            caja = tarjeta(4.6, 4.6, METAL)
            il.move_to(caja.get_center() + UP * 0.45)
            nm = T(txt, 28, TINTA, "HEAVY").move_to(caja.get_center() + DOWN * 1.65)
            cartas.add(VGroup(caja, il, nm))
        cartas.arrange(RIGHT, buff=0.4).move_to([0, -0.3, 0])
        self.play(FadeIn(cartas[0], shift=UP * 0.2), run_time=0.5)
        self.wait(0.6)
        self.sfx("tic", -6)
        self.play(mover_palanca(bk, False), run_time=0.4)
        off = pastilla("OFF", ROJO, 26, True).next_to(bk, DOWN, buff=0.2)
        self.play(FadeIn(off), run_time=0.3)
        self.esperar_frac(0.15)
        self.play(FadeIn(cartas[1], shift=UP * 0.2), run_time=0.5)
        cero = pastilla("sin luz = sin tensión", VERDE_OK, 22, True).move_to(cartas[1][0].get_center() + DOWN * 1.05)
        self.play(Indicate(pr.luz, color=METAL2), FadeIn(cero), run_time=0.7)
        self.esperar_frac(0.4)
        self.play(FadeIn(cartas[2], shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(tit, cartas, off, cero)

    def resumen_y_final(self, clave, reglas):
        self.voz(clave)
        self.camera.frame.set(width=16).move_to(ORIGIN)
        tit = T("EN RESUMEN", 46, TINTA, "HEAVY")
        filas = VGroup(*[VGroup(check(VERDE_OK, 0.24), T(r, 30, TINTA, "BOLD")).arrange(RIGHT, buff=0.3) for r in reglas])
        filas.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([-2.6, 0.2, 0])
        tit.next_to(filas, UP, buff=0.55, aligned_edge=LEFT)
        self.play(FadeIn(tit), run_time=0.3)
        frac = self.resta() * 0.5 / len(reglas)
        for f in filas:
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.4)
            if frac > 0.45:
                self.wait(frac - 0.4)
        self.cerrar_voz(-1.2)
        self.play(FadeOut(VGroup(tit, filas)), run_time=0.4)
        # pantalla final: sirve para YouTube y Facebook
        lg = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(2.8).move_to([3.9, 1.6, 0])
        us = T("@miguelesquit", 36, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        yt = pastilla("SUSCRÍBETE", ROJO, 34, True)
        fb = pastilla("SÍGUEME", MARCA, 34, True)
        botones = VGroup(yt, fb).arrange(DOWN, buff=0.25).next_to(us, DOWN, buff=0.4)
        sig = T("Mira también", 38, TINTA, "HEAVY").move_to([-3.6, 3.1, 0])
        cajas = VGroup(*[RoundedRectangle(width=5.6, height=3.15, corner_radius=0.2, stroke_color=METAL2, stroke_width=2)
                         .set_fill(GAL2 if TEMA != "oscuro" else CARTA, 1) for _ in range(2)]).arrange(DOWN, buff=0.45).move_to([-3.6, -0.6, 0])
        self.play(FadeIn(sig), FadeIn(cajas, shift=UP * 0.2), FadeIn(lg, scale=0.8), FadeIn(us), run_time=0.7)
        self.play(LaggedStart(FadeIn(yt, scale=1.2), FadeIn(fb, scale=1.2), lag_ratio=0.5), run_time=0.6)
        restante = self.fin_voz - self.renderer.time
        espera = max(self.FIN_SEG, restante + 1.0, self.DURACION_MIN - self.renderer.time)
        self.wait(espera)


def pinza_icono(pelacables=False):
    """Pinza / pelacables: mangos con funda de color, pivote y quijadas de acero."""
    col = ROJO if pelacables else "#F79009"
    piv = P(0, 0.25)
    mangos = VGroup(*[VMobject().set_points_smoothly([piv + P(0.06 * s_, -0.1), P(0.22 * s_, -0.5), P(0.42 * s_, -1.2)])
                      .set_stroke(_osc(col, 0.35), 20).set_cap_style(CapStyleType.ROUND) for s_ in (-1, 1)])
    fundas = VGroup(*[VMobject().set_points_smoothly([P(0.18 * s_, -0.4), P(0.3 * s_, -0.8), P(0.42 * s_, -1.2)])
                      .set_stroke(col, 15).set_cap_style(CapStyleType.ROUND) for s_ in (-1, 1)])
    largo = 0.95 if pelacables else 0.7
    quij = VGroup(*[Polygon(piv + P(0.13 * s_, 0), piv + P(0.02 * s_, largo), piv + P(-0.04 * s_, largo), piv + P(-0.05 * s_, 0.05),
                            stroke_color=METAL_OSC, stroke_width=1.2).set_fill(METAL, 1) for s_ in (-1, 1)])
    eje = VGroup(Circle(radius=0.11, stroke_color=METAL_OSC, stroke_width=1.2).set_fill(METAL2, 1).move_to(piv),
                 Circle(radius=0.035, stroke_width=0).set_fill(METAL_OSC, 1).move_to(piv))
    g = VGroup(mangos, fundas, quij, eje)
    if pelacables:
        g.add(VGroup(*[Circle(radius=0.025 + 0.008 * k, stroke_width=0).set_fill(WHITE, 1).move_to(piv + P(0, 0.3 + 0.14 * k)) for k in range(4)]))
    return g


def rutas_tablero(pan, ea, terminal=None):
    """Rutas dentro del tablero desde la entrada superior hasta breaker, barra de neutros y barra de tierra."""
    b = (terminal or pan.nuestro.terminal).get_center()
    tn = pan.tn[1].get_center()
    tt = pan.tt[-2].get_center()
    return {
        "neg_tab": [ea["neg"], P(ea["neg"][0], b[1] + 0.25), b + P(0.12, 0.05), b],
        "bla_tab": [ea["bla"], P(ea["bla"][0], tn[1] + 0.25), P(NEU_X + 0.15, tn[1] + 0.1), tn],
        "ver_tab": [ea["ver"], P(E[0] + 0.3, E[1] - 0.3), P(E[0] + 0.3, tt[1] + 0.25), P(tt[0] + 0.2, tt[1] + 0.12), tt],
    }


def probador_tomas():
    """Probador de tomacorrientes de 3 luces."""
    cuerpo = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.18, stroke_color="#B54708", stroke_width=1.4).set_fill(AMBAR, 1)
    luces = VGroup(*[Circle(radius=0.09, stroke_color=LINEA, stroke_width=1).set_fill("#E4E7EC", 1).move_to(P(-0.35 + 0.35 * k, 0.15)) for k in range(3)])
    tabla = VGroup(*[Line(P(-0.45, -0.1 - 0.08 * k), P(0.45, -0.1 - 0.08 * k), stroke_color="#7A4A22", stroke_width=1) for k in range(4)])
    patas = VGroup(Rectangle(width=0.06, height=0.3, stroke_width=0).set_fill(METAL, 1).move_to(P(-0.15, -0.6)),
                   Rectangle(width=0.06, height=0.3, stroke_width=0).set_fill(METAL, 1).move_to(P(0.15, -0.6)),
                   RoundedRectangle(width=0.07, height=0.36, corner_radius=0.03, stroke_width=0).set_fill(METAL, 1).move_to(P(0, -0.65)))
    g = VGroup(patas, cuerpo, luces, tabla)
    g.luces = luces
    return g


def clavija(tipo="5-15P", polarizada=True):
    cuerpo = RoundedRectangle(width=0.9, height=1.0, corner_radius=0.2, stroke_color=LINEA if TEMA != "oscuro" else "#8F9AC8", stroke_width=1.4 if TEMA != "oscuro" else 2.4).set_fill("#2A2E35", 1)
    fase = Rectangle(width=0.07, height=0.42, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(METAL, 1).move_to(P(0.18, 0.68))
    neu = Rectangle(width=0.11 if polarizada else 0.07, height=0.42, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(METAL, 1).move_to(P(-0.18, 0.68))
    if tipo == "5-20P":
        neu.rotate(PI / 2).move_to(P(-0.22, 0.6))
    tierra = RoundedRectangle(width=0.1, height=0.55, corner_radius=0.04, stroke_color=METAL_OSC, stroke_width=0.8).set_fill(METAL, 1).move_to(P(0, 0.74))
    cordon = Line(P(0, -0.5), P(0, -1.3), stroke_color="#2A2E35" if TEMA != "oscuro" else "#5C6894", stroke_width=10)
    g = VGroup(cordon, tierra, fase, neu, cuerpo)
    g.fase_p, g.neu_p, g.tie_p = fase, neu, tierra
    return g

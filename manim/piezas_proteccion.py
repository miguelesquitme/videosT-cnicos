"""Piezas para los videos de PROTECCIONES (disyuntor y relé térmico), mismo estilo que piezas_auto2:
2D, de frente, realistas, sin marca, todos los tornillos visibles de frente (o de perfil solo en los cortes).
"""
from piezas_auto2 import *
from piezas_auto2 import _texto_sobre
from piezas_auto import _t
from comun_e import _osc, _cla

GRIS_BK = "#E6E9ED"      # cuerpo del breaker
GRIS_FR = "#F4F6F8"      # frente elevado
NEGRO_P = "#22262E"      # palanca
VERDE_ON = "#12B76A"
ROJO_OFF = "#E5484D"


# ===================================================================== DISYUNTOR MODULAR (riel DIN), vista frontal
def breaker_din(polos=1, In=20, curva="C", icn="6000", s=1.0, tension="230/400 V~", ref="Q1"):
    """Interruptor automático modular visto de frente. Cada polo = un módulo de 18 mm.
    Arriba y abajo: bornes con tornillo visto de frente (en su alojamiento). En medio: frente elevado con palanca común,
    marcado de curva y corriente (p. ej. C20), poder de corte en un rectángulo (6000) y ventana de estado.
    Atributos: .palanca, .ventana, .tor_sup, .tor_inf, .on (bool), .s, .cuerpo"""
    w = 1.0 * s
    W, H = w * polos, 4.6 * s
    sombra_ = RoundedRectangle(width=W, height=H, corner_radius=0.08 * s, stroke_width=0).set_fill(BLACK, 0.35).shift(RIGHT * 0.1 * s + DOWN * 0.1 * s)
    cuerpo = RoundedRectangle(width=W, height=H, corner_radius=0.08 * s, stroke_color="#98A2B3", stroke_width=1.4).set_fill(GRIS_BK, 1)
    g = VGroup(sombra_, cuerpo)
    tor_sup, tor_inf = VGroup(), VGroup()
    for k in range(polos):
        x = -W / 2 + w * (k + 0.5)
        if k:
            g.add(Line([x - w / 2, H / 2 - 0.05 * s, 0], [x - w / 2, -H / 2 + 0.05 * s, 0]).set_stroke("#B9BFC8", 1.2))
        for y, grupo in ((H / 2 - 0.55 * s, tor_sup), (-H / 2 + 0.55 * s, tor_inf)):
            boca = RoundedRectangle(width=0.62 * s, height=0.18 * s, corner_radius=0.04 * s, stroke_width=0).set_fill("#2B2F36", 1)
            boca.move_to([x, y + (0.38 * s if y > 0 else -0.38 * s), 0])
            t_ = tornillo_frente(0.2 * s).move_to([x, y, 0])
            t_.boca = boca
            grupo.add(t_)
            g.add(boca, t_)
        g.add(tx(str(2 * k + 1), 0.13 * s, "#475467").move_to([x, H / 2 - 0.88 * s, 0]),
              tx(str(2 * k + 2), 0.13 * s, "#475467").move_to([x, -H / 2 + 0.88 * s, 0]))
    # frente elevado (zona de la palanca)
    frente = RoundedRectangle(width=W - 0.1 * s, height=2.3 * s, corner_radius=0.06 * s, stroke_color="#B9BFC8", stroke_width=1.2).set_fill(GRIS_FR, 1)
    frente.move_to([0, 0.05 * s, 0])
    ranura = RoundedRectangle(width=W - 0.36 * s, height=0.95 * s, corner_radius=0.05 * s, stroke_width=0).set_fill("#1F2430", 1).move_to(frente.get_center() + UP * 0.45 * s)
    palanca = RoundedRectangle(width=W - 0.48 * s, height=0.42 * s, corner_radius=0.05 * s, stroke_color="#0E1116", stroke_width=1).set_fill(NEGRO_P, 1)
    palanca.add(*[Line([xx, -0.12 * s, 0], [xx, 0.12 * s, 0]).set_stroke("#3A3F47", 2) for xx in np.linspace(-(W - 0.7 * s) / 2, (W - 0.7 * s) / 2, max(3, polos * 3))])
    palanca.move_to(ranura.get_center() + UP * 0.22 * s)
    lab_on = tx("I ON", 0.11 * s, "#475467").next_to(ranura, UP, buff=0.04 * s)
    lab_off = tx("O OFF", 0.11 * s, "#475467").next_to(ranura, DOWN, buff=0.04 * s)
    ventana = RoundedRectangle(width=0.36 * s, height=0.16 * s, corner_radius=0.03 * s, stroke_width=0).set_fill(ROJO_OFF, 1)
    marca = tx(f"{curva}{In}", 0.3 * s, "#101828").move_to(frente.get_center() + DOWN * 0.48 * s + LEFT * (0.0 if polos == 1 else 0.2 * s))
    caja_icn = VGroup(Rectangle(width=0.62 * s, height=0.22 * s, stroke_color="#101828", stroke_width=1.2), tx(icn, 0.12 * s, "#101828"))
    caja_icn[1].move_to(caja_icn[0])
    caja_icn.next_to(marca, DOWN, buff=0.08 * s)
    if polos > 1:
        ventana.next_to(marca, RIGHT, buff=0.18 * s)
    else:
        ventana.move_to(frente.get_bottom() + UP * 0.12 * s)
        caja_icn.next_to(marca, DOWN, buff=0.06 * s)
    tens = tx(tension, 0.085 * s, "#475467").move_to([0, frente.get_bottom()[1] - 0.12 * s, 0])
    clip = Rectangle(width=min(W, 0.5 * s), height=0.12 * s, stroke_width=0).set_fill("#9AA3AF", 1).move_to([0, -H / 2 - 0.05 * s, 0])
    g.add(frente, ranura, palanca, lab_on, lab_off, ventana, marca, caja_icn, tens, clip)
    g.palanca, g.ventana, g.tor_sup, g.tor_inf, g.s, g.cuerpo, g.ranura, g.marca, g.icn = palanca, ventana, tor_sup, tor_inf, s, cuerpo, ranura, marca, caja_icn
    g.on = False
    return g


def palanca_breaker(b, on=True):
    """Anima la palanca: ON arriba (ventana roja = contactos cerrados), OFF abajo (ventana verde)."""
    d = 0.44 * b.s
    destino = b.ranura.get_center() + (UP if on else DOWN) * 0.22 * b.s
    b.on = on
    return AnimationGroup(b.palanca.animate.move_to(destino), b.ventana.animate.set_fill(ROJO_OFF if on else VERDE_ON, 1))


def breaker_on(b):
    """Deja el breaker en ON sin animar."""
    b.palanca.move_to(b.ranura.get_center() + UP * 0.22 * b.s)
    b.ventana.set_fill(ROJO_OFF, 1)
    b.on = True
    return b


# ===================================================================== DISYUNTOR EN CORTE (didáctico)
def breaker_corte(s=1.0):
    """Corte didáctico de un interruptor automático modular. Camino de la corriente:
    borne superior → bobina (disparador magnético) → contacto fijo → contacto móvil → trenza → bimetal (disparador
    térmico) → borne inferior. Cámara apagachispas junto a los contactos, palanca y cerradura arriba.
    Atributos para animar: .brazo (gira sobre .piv para abrir), .embolo, .bimetal, .bimetal_curvo, .barra, .palanca,
    .piv_pal, .camara, .camino (lista de puntos), .pad_fijo, .pad_movil"""
    k = s
    caja = RoundedRectangle(width=4.6 * k, height=6.4 * k, corner_radius=0.18 * k, stroke_color="#8B93A0", stroke_width=2.4).set_fill("#2A2F3A", 0.92)
    g = VGroup(caja)
    # palanca arriba (con su eje)
    piv_pal = np.array([0.9 * k, 2.85 * k, 0])
    palanca = RoundedRectangle(width=0.42 * k, height=1.2 * k, corner_radius=0.08 * k, stroke_color="#0E1116", stroke_width=1).set_fill(NEGRO_P, 1)
    palanca.move_to(piv_pal + UP * 0.55 * k).rotate(-0.35, about_point=piv_pal)
    eje = Circle(radius=0.12 * k, stroke_color="#98A2B3", stroke_width=1.5).set_fill("#D0D5DD", 1).move_to(piv_pal)
    # cerradura (mecanismo) y su resorte
    cerr = VGroup(Polygon([0.3 * k, 2.3 * k, 0], [1.5 * k, 2.3 * k, 0], [1.5 * k, 1.6 * k, 0], [0.6 * k, 1.4 * k, 0], stroke_color="#98A2B3", stroke_width=1.5).set_fill("#5B6573", 1),
                  resorte(0.7 * k, 0.25 * k, 5, "#C7CCD6", 2).rotate(PI / 2).move_to([2.0 * k, 1.95 * k, 0]))
    # borne superior con tornillo de perfil
    bsup = Rectangle(width=1.0 * k, height=0.55 * k, stroke_color="#7A3B12", stroke_width=1.2).set_fill(CU, 1).move_to([-1.45 * k, 2.55 * k, 0])
    tsup = tornillo_perfil(0.42 * k, 0.32 * k).move_to([-1.45 * k, 0, 0])
    tsup.shift(UP * (bsup.get_top()[1] - tsup[2].get_bottom()[1]))
    # bobina magnética con émbolo
    nucleo = Rectangle(width=0.95 * k, height=1.5 * k, stroke_color="#5B6573", stroke_width=1.4).set_fill("#9AA3AF", 1).move_to([-1.45 * k, 1.15 * k, 0])
    espiras = VGroup(*[RoundedRectangle(width=1.15 * k, height=0.13 * k, corner_radius=0.06 * k, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1)
                       .move_to([-1.45 * k, (0.55 + 0.15 * j) * k, 0]) for j in range(9)])
    embolo = Rectangle(width=0.22 * k, height=1.2 * k, stroke_color="#4B5563", stroke_width=1).set_fill("#D0D5DD", 1).move_to([-1.45 * k, 0.15 * k, 0])
    alim = Line(bsup.get_bottom(), nucleo.get_top()).set_stroke(CU, 7 * k)
    # contactos
    fijo = Rectangle(width=0.9 * k, height=0.16 * k, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to([-0.55 * k, -0.6 * k, 0])
    lead = VMobject().set_points_as_corners([[-1.95 * k, 0.55 * k, 0], [-2.05 * k, 0.55 * k, 0], [-2.05 * k, -0.6 * k, 0], [-1.0 * k, -0.6 * k, 0]]).set_stroke(CU, 6 * k)
    pad_fijo = RoundedRectangle(width=0.32 * k, height=0.1 * k, corner_radius=0.02 * k, stroke_width=0).set_fill(AG, 1).move_to([-0.3 * k, -0.47 * k, 0])
    piv = np.array([1.05 * k, 0.2 * k, 0])
    brazo = VGroup(Line(piv, [-0.3 * k, -0.3 * k, 0]).set_stroke("#B87333", 9 * k),
                   RoundedRectangle(width=0.32 * k, height=0.1 * k, corner_radius=0.02 * k, stroke_width=0).set_fill(AG, 1).move_to([-0.3 * k, -0.36 * k, 0]))
    eje_b = Circle(radius=0.1 * k, stroke_color="#98A2B3", stroke_width=1.2).set_fill("#D0D5DD", 1).move_to(piv)
    # cámara apagachispas (abajo a la izquierda)
    camara = VGroup(*[Rectangle(width=1.3 * k, height=0.07 * k, stroke_width=0).set_fill("#B8BEC8", 1).move_to([-1.35 * k, (-1.2 - 0.2 * j) * k, 0]) for j in range(8)])
    guia = Line([-0.3 * k, -0.62 * k, 0], [-0.75 * k, -1.1 * k, 0]).set_stroke(CU, 4 * k)
    # trenza y bimetal
    trenza = VMobject().set_points_smoothly([[1.05 * k, 0.2 * k, 0], [1.5 * k, -0.2 * k, 0], [1.25 * k, -0.6 * k, 0], [1.55 * k, -0.95 * k, 0]]).set_stroke("#D9A066", 5 * k)
    b_top, b_bot = np.array([1.55 * k, -0.95 * k, 0]), np.array([1.55 * k, -2.55 * k, 0])
    bim = VGroup(Line(b_top + LEFT * 0.06 * k, b_bot + LEFT * 0.06 * k).set_stroke("#C0C6CF", 8 * k), Line(b_top + RIGHT * 0.06 * k, b_bot + RIGHT * 0.06 * k).set_stroke("#D9844A", 8 * k))
    bim_c = VGroup(ArcBetweenPoints(b_bot + LEFT * 0.06 * k, b_top + LEFT * 0.06 * k + LEFT * 0.45 * k, angle=-0.5).set_stroke("#C0C6CF", 8 * k),
                   ArcBetweenPoints(b_bot + RIGHT * 0.06 * k, b_top + RIGHT * 0.06 * k + LEFT * 0.45 * k, angle=-0.5).set_stroke("#D9844A", 8 * k))
    barra = Rectangle(width=2.1 * k, height=0.14 * k, stroke_color="#98A2B3", stroke_width=1).set_fill("#667085", 1).move_to([0.55 * k, -1.0 * k, 0])
    binf = Rectangle(width=1.0 * k, height=0.55 * k, stroke_color="#7A3B12", stroke_width=1.2).set_fill(CU, 1).move_to([1.45 * k, -2.85 * k, 0])
    tinf = tornillo_perfil(0.42 * k, 0.32 * k).move_to([1.45 * k, 0, 0])
    tinf.shift(UP * (binf.get_top()[1] - tinf[2].get_bottom()[1]))
    bim_c.set_stroke(opacity=0)
    g.add(cerr, alim, lead, nucleo, espiras, embolo, bsup, tsup, fijo, pad_fijo, camara, guia, trenza, bim, bim_c, barra, binf, tinf, brazo, eje_b, palanca, eje)
    g.brazo, g.piv, g.embolo, g.bimetal, g.bimetal_curvo, g.barra, g.palanca, g.piv_pal = brazo, piv, embolo, bim, bim_c, barra, palanca, piv_pal
    g.camara, g.espiras, g.pad_fijo, g.pad_movil, g.nucleo, g.cerr, g.bsup, g.binf = camara, espiras, pad_fijo, brazo[1], nucleo, cerr, bsup, binf
    g.camino = [bsup.get_top() + UP * 0.3 * k, bsup.get_center(), nucleo.get_center(), [-2.05 * k, 0.55 * k, 0], [-2.05 * k, -0.6 * k, 0], [-0.3 * k, -0.42 * k, 0],
                piv, [1.5 * k, -0.2 * k, 0], b_top, b_bot, binf.get_center(), binf.get_bottom() + DOWN * 0.3 * k]
    return g


# ===================================================================== símbolo IEC del interruptor automático
def sim_interruptor_auto(ref="Q1", color=SIM, largo=1.2, sw=SW_POT, n1="1", n2="2"):
    """Contacto con cruz (función interruptor automático) + mandos: térmico (escalón) y magnético (I>), con enlace."""
    c = contacto(True, interruptor=True, largo=largo, color=color, n1=n1, n2=n2, sw=sw)
    p = c.cuchilla.get_center()
    dl = DashedLine(p, p + LEFT * 0.55, dash_length=0.05).set_stroke(color, 2.2)
    caja_m = Rectangle(width=0.42, height=0.32, stroke_color=color, stroke_width=2.2).move_to(p + LEFT * 0.78 + UP * 0.2)
    im = _t("I>", 0.16, color).move_to(caja_m)
    caja_t = Rectangle(width=0.42, height=0.32, stroke_color=color, stroke_width=2.2).move_to(p + LEFT * 0.78 + DOWN * 0.2)
    esc = VMobject().set_points_as_corners([caja_t.get_center() + P(-0.13, -0.06), caja_t.get_center() + P(-0.03, -0.06), caja_t.get_center() + P(-0.03, 0.06),
                                            caja_t.get_center() + P(0.13, 0.06)]).set_stroke(color, 2)
    r = _t(ref, 0.22, color).next_to(VGroup(caja_m, caja_t), LEFT, buff=0.1)
    c.add(dl, caja_m, im, caja_t, esc, r)
    return c


# ===================================================================== gráfica log-log de curvas de disparo
class GraficaLog(VGroup):
    """Ejes log-log dibujados a mano: x = múltiplos de In (1…100), y = tiempo (0,01 s … 10 000 s)."""

    def __init__(self, w=7.0, h=5.0, xr=(1, 100), yr=(0.01, 10000), xlab="múltiplos de In", ylab="tiempo (s)", **kw):
        super().__init__(**kw)
        self.w, self.h, self.xr, self.yr = w, h, xr, yr
        marco = Rectangle(width=w, height=h, stroke_color="#6F86D6", stroke_width=2).set_fill("#0F2250", 1)
        self.add(marco)
        self.marco = marco
        lx0, lx1 = np.log10(xr[0]), np.log10(xr[1])
        ly0, ly1 = np.log10(yr[0]), np.log10(yr[1])
        for d in range(int(np.floor(lx0)), int(np.ceil(lx1)) + 1):
            for m in range(1, 10):
                v = m * 10 ** d
                if xr[0] <= v <= xr[1]:
                    x = self._x(v)
                    self.add(Line([x, -h / 2, 0], [x, h / 2, 0]).set_stroke("#3A4C86", 2 if m == 1 else 0.8))
                    if m in (1, 2, 5):
                        self.add(T(f"{v:g}", 16, TXT2, "BOLD").move_to([x, -h / 2 - 0.22, 0]))
        for d in range(int(np.floor(ly0)), int(np.ceil(ly1)) + 1):
            v = 10 ** d
            if yr[0] <= v <= yr[1]:
                y = self._y(v)
                self.add(Line([-w / 2, y, 0], [w / 2, y, 0]).set_stroke("#3A4C86", 1.6))
                self.add(T(f"{v:g}", 16, TXT2, "BOLD").move_to([-w / 2 - 0.42, y, 0]))
        self.add(T(xlab, 20, TXT, "BOLD").move_to([0, -h / 2 - 0.58, 0]), T(ylab, 20, TXT, "BOLD").rotate(PI / 2).move_to([-w / 2 - 0.95, 0, 0]))

    def _x(self, v):
        lx0, lx1 = np.log10(self.xr[0]), np.log10(self.xr[1])
        return -self.w / 2 + self.w * (np.log10(v) - lx0) / (lx1 - lx0)

    def _y(self, v):
        ly0, ly1 = np.log10(self.yr[0]), np.log10(self.yr[1])
        return -self.h / 2 + self.h * (np.log10(v) - ly0) / (ly1 - ly0)

    def p(self, xv, yv):
        return self.get_center() + np.array([self._x(xv), self._y(yv), 0]) - self.marco.get_center() + self.marco.get_center() - self.get_center() + (self.marco.get_center())

    def pt(self, xv, yv):
        return self.marco.get_center() + np.array([self._x(xv), self._y(yv), 0])

    def curva(self, f, x0, x1, color, sw=5, n=80):
        xs = np.logspace(np.log10(x0), np.log10(x1), n)
        pts = [self.pt(x, min(max(f(x), self.yr[0]), self.yr[1])) for x in xs]
        return VMobject().set_points_smoothly(pts).set_stroke(color, sw)


def banda_disparo(gr, k_mag0, k_mag1, color, op=0.3):
    """Banda de disparo de un interruptor IEC 60898-1: térmica (tiempo inverso) + magnética (k_mag0…k_mag1, < 0,1 s).
    Curva térmica aproximada (didáctica) que respeta 1,13 In (sin disparo en 1 h) y 1,45 In (disparo < 1 h)."""
    def t_lento(x):          # límite superior (no dispara antes): asintótico a 1,13
        return 3600 * ((1.45 - 1.13) / max(x - 1.13, 1e-3)) ** 1.6
    def t_rapido(x):         # límite inferior
        return 3600 * ((1.45 - 1.30) / max(x - 1.30, 1e-3)) ** 1.6 * 0.12
    sup = [gr.pt(x, min(t_lento(x), 9000)) for x in np.logspace(np.log10(1.16), np.log10(k_mag1), 70)] + [gr.pt(k_mag1, 0.01)]
    inf = [gr.pt(x, min(max(t_rapido(x), 0.1), 9000)) for x in np.logspace(np.log10(1.36), np.log10(k_mag0), 60)] + [gr.pt(k_mag0, 0.1), gr.pt(k_mag0, 0.01)]
    poly = Polygon(*(sup + inf[::-1]), stroke_color=color, stroke_width=3).set_fill(color, op)
    return poly


# ===================================================================== RELÉ TÉRMICO, vista frontal
def rele_termico(s=1.0, rango=(12, 18), ref="F2", clase="10A"):
    """Relé térmico de sobrecarga visto de frente (sin marca), para montar debajo de un contactor:
    tres pines de cobre arriba; bornes auxiliares 97-98 (NA) y 95-96 (NC) arriba; dial de ajuste con escala;
    botón azul de rearme (R), botón rojo de paro (STOP), prueba (TEST) y ventana de disparo;
    abajo, bornes 2/T1 4/T2 6/T3 con tornillos. Atributos: .pines, .aguja, .dial, .reset, .stop, .test, .flag, .b"""
    W, H = 3.2 * s, 2.7 * s
    xs = [(-1.2 + 0.8 * k) * s for k in range(3)]
    sombra_ = RoundedRectangle(width=W, height=H, corner_radius=0.1 * s, stroke_width=0).set_fill(BLACK, 0.35).shift(RIGHT * 0.12 * s + DOWN * 0.12 * s)
    pines = VGroup(*[Rectangle(width=0.16 * s, height=0.62 * s, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to([x, H / 2 + 0.26 * s, 0]) for x in xs])
    cuerpo = RoundedRectangle(width=W, height=H, corner_radius=0.1 * s, stroke_color="#8B93A0", stroke_width=1.6).set_fill("#D5D9DF", 1)
    g = VGroup(sombra_, pines, cuerpo)
    b = {}
    # bornes auxiliares arriba a la derecha
    for n, x in (("97", 0.55 * s), ("98", 0.9 * s), ("95", 1.25 * s)):
        pass
    aux_x = {"97": 0.42 * s, "98": 0.8 * s, "95": 1.18 * s, "96": 1.18 * s}
    for n, (x, y) in {"97": (0.38 * s, H / 2 - 0.3 * s), "98": (0.78 * s, H / 2 - 0.3 * s), "95": (1.18 * s, H / 2 - 0.3 * s),
                      "96": (1.18 * s, -0.05 * s)}.items():
        t_ = tornillo_frente(0.12 * s).move_to([x, y, 0])
        e = tx(n, 0.1 * s, "#B42318" if n in ("95", "96") else "#1D4E9E").next_to(t_, LEFT if n == "96" else DOWN, buff=0.03 * s)
        bb = VGroup(t_, e)
        bb.tor, bb.et = t_, e
        b[n] = bb
        g.add(bb)
    # dial de ajuste
    dial = Circle(radius=0.42 * s, stroke_color="#475467", stroke_width=1.6).set_fill("#F8FAFC", 1).move_to([-0.75 * s, 0.25 * s, 0])
    i0, i1 = rango
    marcas = VGroup()
    for j, a in enumerate(np.linspace(PI * 1.15, -PI * 0.15, 7)):
        p0 = dial.get_center() + 0.42 * s * np.array([np.cos(a), np.sin(a), 0])
        p1 = dial.get_center() + 0.33 * s * np.array([np.cos(a), np.sin(a), 0])
        marcas.add(Line(p0, p1).set_stroke("#475467", 1.4))
    nums = VGroup(*[tx(f"{v:g}", 0.1 * s, "#101828").move_to(dial.get_center() + 0.58 * s * np.array([np.cos(a), np.sin(a), 0]))
                    for v, a in ((i0, PI * 1.15), ((i0 + i1) / 2, PI / 2), (i1, -PI * 0.15))])
    ranura = Line(dial.get_center() + LEFT * 0.22 * s, dial.get_center() + RIGHT * 0.22 * s).set_stroke("#101828", 4)
    aguja = VGroup(ranura, Triangle().scale(0.06 * s).set_fill("#101828", 1).set_stroke(width=0).move_to(dial.get_center() + UP * 0.27 * s))
    aguja.rotate(PI * 0.3, about_point=dial.get_center())
    unidad = tx("A", 0.1 * s, "#475467").next_to(dial, DOWN, buff=0.04 * s)
    # botones
    reset = VGroup(Circle(radius=0.2 * s, stroke_color="#1D4E9E", stroke_width=1.4).set_fill("#2F6FD0", 1), tx("R", 0.13 * s, "#FFFFFF"))
    reset.move_to([0.32 * s, 0.25 * s, 0])
    stop = VGroup(RoundedRectangle(width=0.36 * s, height=0.26 * s, corner_radius=0.05 * s, stroke_color="#8F1D1D", stroke_width=1.2).set_fill("#E5484D", 1),
                  tx("STOP", 0.07 * s, "#FFFFFF")).move_to([0.32 * s, -0.25 * s, 0])
    test = VGroup(RoundedRectangle(width=0.32 * s, height=0.14 * s, corner_radius=0.03 * s, stroke_color="#475467", stroke_width=1).set_fill("#98A2B3", 1),
                  tx("TEST", 0.06 * s, "#101828")).move_to([0.75 * s, -0.42 * s, 0])
    ventana = RoundedRectangle(width=0.32 * s, height=0.2 * s, corner_radius=0.03 * s, stroke_color="#475467", stroke_width=1).set_fill("#1F2430", 1).move_to([0.75 * s, 0.25 * s, 0])
    flag = Rectangle(width=0.26 * s, height=0.14 * s, stroke_width=0).set_fill("#667085", 1).move_to(ventana)
    tclase = tx(f"CLASE {clase}", 0.08 * s, "#475467").move_to([-0.75 * s, -0.42 * s, 0])
    g.add(dial, marcas, nums, aguja, unidad, reset, stop, test, ventana, flag, tclase)
    # bornes de potencia abajo
    for x, n in zip(xs, ("2/T1", "4/T2", "6/T3")):
        t_ = tornillo_frente(0.19 * s).move_to([x, -H / 2 + 0.45 * s, 0])
        e = tx(n, 0.11 * s, "#475467").next_to(t_, UP, buff=0.05 * s)
        boca = RoundedRectangle(width=0.46 * s, height=0.14 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#2B2F36", 1).move_to([x, -H / 2 + 0.09 * s, 0])
        bb = VGroup(boca, t_, e)
        bb.tor, bb.et, bb.entrada = t_, e, boca
        b[n] = bb
        g.add(bb)
    g.add(tx(ref, 0.12 * s, "#1D2939").move_to([-1.2 * s, H / 2 - 0.22 * s, 0]))
    g.pines, g.aguja, g.dial, g.reset, g.stop, g.test, g.flag, g.b, g.s, g.cuerpo, g.rango = pines, aguja, dial, reset, stop, test, flag, b, s, cuerpo, rango
    return g


def ajustar_dial(r, valor):
    """Gira la aguja del dial al valor (A) dentro del rango."""
    i0, i1 = r.rango
    f = (valor - i0) / (i1 - i0)
    ang_obj = PI * 1.15 + (-PI * 0.15 - PI * 1.15) * f        # ángulo de la marca
    # la aguja apunta hacia UP rotada; su ángulo actual:
    v = r.aguja[1].get_center() - r.dial.get_center()
    actual = np.arctan2(v[1], v[0])
    return Rotate(r.aguja, ang_obj - actual, about_point=r.dial.get_center())


def disparar_rele(r):
    return r.flag.animate.set_fill("#F5A524", 1)


def montar_rele(ct, r):
    """Coloca el relé debajo del contactor con los pines dentro de los bornes 2/T1 4/T2 6/T3."""
    destino = ct.b["4/T2"].tor.get_center()
    r.shift(destino - r.pines[1].get_top() + DOWN * 0.02)
    return r


# ===================================================================== RELÉ TÉRMICO EN CORTE (didáctico)
def rele_corte(s=1.0):
    """Tres bimetales con su calefactor (cobre en espiral), regleta diferencial doble, bimetal de compensación,
    palanca de disparo y contactos 95-96 (NC) / 97-98 (NA). Atributos: .bims, .bims_c (curvados), .regleta_a,
    .regleta_b, .palanca, .nc_movil, .no_movil, .compensa"""
    k = s
    caja = RoundedRectangle(width=6.6 * k, height=5.2 * k, corner_radius=0.18 * k, stroke_color="#8B93A0", stroke_width=2.4).set_fill("#2A2F3A", 0.92)
    g = VGroup(caja)
    xs = [(-2.4 + 1.2 * j) * k for j in range(3)]
    bims, bims_c, calef = VGroup(), VGroup(), VGroup()
    for x in xs:
        top, bot = np.array([x, 1.4 * k, 0]), np.array([x, -1.6 * k, 0])
        bim = VGroup(Line(bot + LEFT * 0.06 * k, top + LEFT * 0.06 * k).set_stroke("#C0C6CF", 9 * k), Line(bot + RIGHT * 0.06 * k, top + RIGHT * 0.06 * k).set_stroke("#D9844A", 9 * k))
        cur = VGroup(ArcBetweenPoints(bot + LEFT * 0.06 * k, top + LEFT * 0.06 * k + RIGHT * 0.42 * k, angle=0.45).set_stroke("#C0C6CF", 9 * k),
                     ArcBetweenPoints(bot + RIGHT * 0.06 * k, top + RIGHT * 0.06 * k + RIGHT * 0.42 * k, angle=0.45).set_stroke("#D9844A", 9 * k))
        esp = VGroup(*[Ellipse(width=0.42 * k, height=0.1 * k).set_stroke(CU, 3 * k) .move_to([x, (-1.3 + 0.18 * j) * k, 0]) for j in range(12)])
        bims.add(bim)
        bims_c.add(cur)
        calef.add(esp)
        g.add(Rectangle(width=0.5 * k, height=0.25 * k, stroke_width=0).set_fill("#667085", 1).move_to(bot + DOWN * 0.1 * k))
    bims_c.set_stroke(opacity=0)
    g.add(bims, bims_c, calef)
    regleta_a = Rectangle(width=4.0 * k, height=0.16 * k, stroke_color="#98A2B3", stroke_width=1).set_fill("#98A2B3", 1).move_to([-1.0 * k, 1.75 * k, 0])
    regleta_b = Rectangle(width=4.0 * k, height=0.16 * k, stroke_color="#98A2B3", stroke_width=1).set_fill("#667085", 1).move_to([-1.0 * k, 2.05 * k, 0])
    dientes = VGroup(*[Rectangle(width=0.08 * k, height=0.42 * k, stroke_width=0).set_fill("#98A2B3", 1).move_to([x + 0.2 * k, 1.85 * k, 0]) for x in xs])
    compensa = VGroup(Line([1.55 * k, 1.9 * k, 0], [1.55 * k, 0.6 * k, 0]).set_stroke("#C0C6CF", 8 * k), Line([1.67 * k, 1.9 * k, 0], [1.67 * k, 0.6 * k, 0]).set_stroke("#D9844A", 8 * k))
    piv = np.array([2.2 * k, 0.6 * k, 0])
    palanca = Line(piv, piv + UP * 1.5 * k).set_stroke("#D0D5DD", 8 * k)
    eje = Circle(radius=0.1 * k, stroke_color="#98A2B3", stroke_width=1.2).set_fill("#D0D5DD", 1).move_to(piv)
    # contactos 95-96 (NC) y 97-98 (NA)
    c95 = VGroup(Rectangle(width=0.5 * k, height=0.1 * k, stroke_width=0).set_fill(CU, 1).move_to([2.55 * k, -0.4 * k, 0]), tx("95", 0.16 * k, "#FF8A80").move_to([2.2 * k, -0.4 * k, 0]))
    c96 = VGroup(Rectangle(width=0.5 * k, height=0.1 * k, stroke_width=0).set_fill(CU, 1).move_to([2.55 * k, -0.9 * k, 0]), tx("96", 0.16 * k, "#FF8A80").move_to([2.2 * k, -0.9 * k, 0]))
    nc_movil = Line([2.85 * k, -0.4 * k, 0], [2.85 * k, -0.9 * k, 0]).set_stroke(AG, 7 * k)
    c97 = VGroup(Rectangle(width=0.5 * k, height=0.1 * k, stroke_width=0).set_fill(CU, 1).move_to([2.55 * k, -1.5 * k, 0]), tx("97", 0.16 * k, "#8AB4FF").move_to([2.2 * k, -1.5 * k, 0]))
    c98 = VGroup(Rectangle(width=0.5 * k, height=0.1 * k, stroke_width=0).set_fill(CU, 1).move_to([2.55 * k, -2.0 * k, 0]), tx("98", 0.16 * k, "#8AB4FF").move_to([2.2 * k, -2.0 * k, 0]))
    no_movil = Line([2.85 * k, -1.5 * k, 0], [2.6 * k, -1.95 * k, 0]).set_stroke(AG, 7 * k)
    varilla = DashedLine(piv, [2.85 * k, -0.65 * k, 0], dash_length=0.08 * k).set_stroke("#D0D5DD", 3)
    g.add(regleta_a, regleta_b, dientes, compensa, palanca, eje, c95, c96, nc_movil, c97, c98, no_movil, varilla)
    g.bims, g.bims_c, g.calef, g.regleta_a, g.regleta_b, g.dientes, g.palanca, g.piv, g.nc_movil, g.no_movil, g.compensa = \
        bims, bims_c, calef, regleta_a, regleta_b, dientes, palanca, piv, nc_movil, no_movil, compensa
    return g


# ===================================================================== placa de datos de un motor (sin marca)
def placa_motor(datos, s=1.0, titulo="MOTOR DE INDUCCIÓN TRIFÁSICO"):
    """datos: lista de (etiqueta, valor, resaltar). Placa metálica con remaches."""
    filas = VGroup()
    for et, val, res in datos:
        a = tx(et, 0.15 * s, "#344054")
        b = tx(val, 0.2 * s, "#B42318" if res else "#101828")
        caja = Rectangle(width=1.5 * s, height=0.48 * s, stroke_color="#98A2B3", stroke_width=1).set_fill("#FFFFFF" if not res else "#FFF4E5", 1)
        VGroup(a, b).arrange(DOWN, buff=0.03 * s).move_to(caja)
        filas.add(VGroup(caja, a, b))
    filas.arrange_in_grid(cols=3, buff=0.06 * s)
    cab = tx(titulo, 0.16 * s, "#101828").next_to(filas, UP, buff=0.12 * s)
    placa = RoundedRectangle(width=filas.width + 0.5 * s, height=filas.height + cab.height + 0.55 * s, corner_radius=0.08 * s, stroke_color="#667085", stroke_width=2).set_fill("#D0D5DD", 1)
    VGroup(cab, filas).move_to(placa)
    rem = VGroup(*[Circle(radius=0.06 * s, stroke_color="#667085", stroke_width=1).set_fill("#98A2B3", 1).move_to(placa.get_corner(c) + (-c) * 0.14 * s) for c in (UL, UR, DL, DR)])
    g = VGroup(placa, rem, cab, filas)
    g.filas = filas
    return g

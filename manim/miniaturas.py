"""Miniaturas: FORMATO=h → MiniH (1920x1080, YouTube) · FORMATO=v → MiniV (1080x1920, portada de reel)."""
from comun_e import *
from comun_e import _osc
import os

AZUL_A, AZUL_B = "#0B2540", "#0E4A6B"


def fondo_azul():
    w, h = config.frame_width, config.frame_height
    base = Rectangle(width=w, height=h, stroke_width=0).set_fill(color=[AZUL_A, AZUL_B], opacity=1)
    base.set_sheen_direction(UR)
    rej = VGroup(*[Line([x, -h / 2, 0], [x, h / 2, 0]) for x in np.arange(-w / 2, w / 2 + 0.01, 0.5)],
                 *[Line([-w / 2, y, 0], [w / 2, y, 0]) for y in np.arange(-h / 2, h / 2 + 0.01, 0.5)]).set_stroke(WHITE, 1, 0.07)
    return VGroup(base, rej)


def contorno(t, color=AZUL_A, w=14):
    return VGroup(t.copy().set_stroke(color, w).set_fill(color, 1), t)


class MiniH(MovingCameraScene):
    def construct(self):
        from nema import portalampara, foco, interruptor, breaker, P, LAMP_TOP, OCT_C, SW_C
        self.add(fondo_azul())
        # izquierda: texto
        l1 = T("CÓMO CONECTAR", 92, WHITE, "HEAVY")
        l2 = T("UNA LÁMPARA", 104, AMBAR, "HEAVY")
        l3 = T("del tablero al foco", 52, WHITE, "BOLD")
        txt = VGroup(l1, l2, l3).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        txt.scale_to_fit_width(8.6).to_edge(LEFT, buff=0.55).shift(UP * 1.25)
        nec = pastilla("NEC 2020", MARCA, 46, True).next_to(txt, DOWN, buff=0.45, aligned_edge=LEFT)
        alerta = VGroup(T("¡NO cortes el", 50, WHITE, "HEAVY"), T("NEUTRO!", 62, "#FF5A5F", "HEAVY")).arrange(RIGHT, buff=0.22)
        alerta.next_to(nec, DOWN, buff=0.45, aligned_edge=LEFT)
        self.add(*[contorno(m) for m in (l1, l2, l3)], nec, *[contorno(m) for m in alerta])
        # derecha: foco encendido + portalámparas + interruptor
        port = portalampara(P(0, 0)).scale(3.4)
        port.scale(0.92).move_to([5.0, 1.75, 0])
        on = foco(True, 0.85).scale(3.4).move_to(port.foco)
        port.foco.become(on)
        glow = resplandor(port.foco.vidrio.get_center(), 3.2, AMBAR, 14, 0.06)
        cordon = VGroup(Line(port.get_top() + LEFT * 0.4, port.get_top() + LEFT * 0.4 + UP * 1.5).set_stroke(WHITE, 7),
                        Line(port.get_top() + RIGHT * 0.4, port.get_top() + RIGHT * 0.4 + UP * 1.5).set_stroke("#FF5A5F", 7))
        sw = interruptor(True).scale(2.2).move_to([6.6, -2.2, 0]).rotate(0.08)
        rayo_ = simbolo_rayo(AMBAR, 1.3).move_to([1.6, -2.9, 0]).rotate(0.15)
        self.add(glow, cordon, port, sw, rayo_)
        lg = ImageMobject(str(DIR / "logo_letras.png")).scale_to_fit_width(1.5).move_to([-6.9, -3.8, 0])
        self.add(lg)


class MiniV(MovingCameraScene):
    def construct(self):
        from dibujos_aves import pajarito, linea_aerea, aislador_pin, MADERA, MADERA_OSC
        self.add(fondo_azul())
        l1 = T("¿POR QUÉ LOS", 86, WHITE, "HEAVY")
        l2 = T("PÁJAROS", 128, AMBAR, "HEAVY")
        l3 = T("NO SE", 86, WHITE, "HEAVY")
        l4 = T("ELECTROCUTAN?", 92, "#FF5A5F", "HEAVY")
        txt = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.12)
        for m in txt:
            if m.width > 8.0:
                m.scale_to_fit_width(8.0)
        txt.arrange(DOWN, buff=0.12).move_to([0, 4.85, 0])
        self.add(*[contorno(m) for m in txt])
        cab = linea_aerea([-5.5, -1.9, 0], [5.5, -2.2, 0], 0.35, color="#C9CED6", w=7)
        self.add(cab)
        # chispas eléctricas a lo largo del cable
        for k, x in enumerate((-3.6, 3.0)):
            p0 = cab.point_from_proportion((x + 5.5) / 11)
            self.add(rayo(p0 + UP * 0.05 + LEFT * 0.3, p0 + UP * 0.9 + RIGHT * 0.2, AMBAR, 5, 0.14, k + 3, 5))
        p = pajarito().scale(2.7)
        base = cab.point_from_proportion(0.5)
        p.shift(base - (p[1][0][0].get_end() + p[1][1][0].get_end()) / 2)
        self.add(p)
        mv = VGroup(T("miles de", 60, WHITE, "HEAVY"), T("VOLTIOS", 84, AMBAR, "HEAVY")).arrange(DOWN, buff=0.05)
        mv.move_to([0, -4.5, 0])
        self.add(*[contorno(m) for m in mv], simbolo_rayo(AMBAR, 1.6).move_to([-3.2, -4.5, 0]).rotate(0.2),
                 simbolo_rayo(AMBAR, 1.6).move_to([3.2, -4.5, 0]).rotate(-0.2))
        lg = ImageMobject(str(DIR / "logo_letras.png")).scale_to_fit_width(1.6).move_to([0, -6.4, 0])
        self.add(lg)


def _texto_izq(self, a, b, c, extra=None, col_b=AMBAR):
    l1 = T(a, 92, WHITE, "HEAVY")
    l2 = T(b, 110, col_b, "HEAVY")
    l3 = T(c, 52, WHITE, "BOLD")
    txt = VGroup(l1, l2, l3).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    txt.scale_to_fit_width(8.4).to_edge(LEFT, buff=0.55).shift(UP * 1.0)
    self.add(*[contorno(m) for m in (l1, l2, l3)])
    if extra is not None:
        extra.next_to(txt, DOWN, buff=0.5, aligned_edge=LEFT)
        self.add(extra)
    lg = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(1.6).move_to([-6.7, -3.75, 0])
    self.add(lg)


class MiniE03(MovingCameraScene):
    def construct(self):
        from taller import placa_interruptor, foco_led, P
        self.add(fondo_azul())
        _texto_izq(self, "APAGADOR DE", "ESCALERA", "3 vías · paso a paso",
                   pastilla("2 interruptores · 1 foco", MARCA, 44, True))
        f = foco_led(True, 0.9).scale(3.6).move_to([4.6, 2.0, 0])
        glow = resplandor(f[0].get_center(), 3.0, AMBAR, 14, 0.06)
        esc = VGroup(*[VGroup(Line(P(1.2 + 0.7 * k, -3.6 + 0.45 * k), P(1.9 + 0.7 * k, -3.6 + 0.45 * k)),
                              Line(P(1.9 + 0.7 * k, -3.6 + 0.45 * k), P(1.9 + 0.7 * k, -3.15 + 0.45 * k))) for k in range(8)]).set_stroke(WHITE, 5, 0.5)
        s1 = placa_interruptor(P(0, 0), 1).scale(2.0).move_to([2.0, -2.4, 0])
        s2 = placa_interruptor(P(0, 0), 2).scale(2.0).move_to([6.8, -0.4, 0])
        cord = Line([4.6, 4.2, 0], f.get_top()).set_stroke(WHITE, 6)
        self.add(esc, glow, cord, f, s1, s2)


class MiniE04(MovingCameraScene):
    def construct(self):
        from taller import tomacorriente, placa_toma, P
        self.add(fondo_azul())
        _texto_izq(self, "CÓMO CONECTAR UN", "TOMACORRIENTE", "con tierra · NEMA 5-15",
                   VGroup(T("¿Y el", 54, WHITE, "HEAVY"), T("REDONDO?", 64, "#7CFF9B", "HEAVY")).arrange(RIGHT, buff=0.2))
        t = tomacorriente(P(0, 0)).scale(4.6).move_to([4.7, 0.0, 0])
        cab = VGroup(Line(t.l1.get_center(), t.l1.get_center() + RIGHT * 2.0).set_stroke("#1B1B1B", 16),
                     Line(t.p1.get_center(), t.p1.get_center() + LEFT * 1.2 + UP * 0.6).set_stroke(WHITE, 16),
                     Line(t.verde.get_center(), t.verde.get_center() + DOWN * 1.2 + RIGHT * 1.5).set_stroke("#16A34A", 16))
        self.add(cab, t)


class MiniE05(MovingCameraScene):
    def construct(self):
        from taller import hervidor, plancha, foco_led, P
        self.add(fondo_azul())
        _texto_izq(self, "LEY DE", "OHM", "con cosas de tu casa",
                   VGroup(T("¿Por qué se", 50, WHITE, "HEAVY"), T("DISPARA?", 62, "#FF5A5F", "HEAVY")).arrange(RIGHT, buff=0.2))
        f = MathTex(r"V = I \times R", color=WHITE).scale(2.4)
        caja = RoundedRectangle(width=f.width + 0.8, height=f.height + 0.6, corner_radius=0.25, stroke_color=AMBAR, stroke_width=8).set_fill(AZUL_A, 0.9)
        g = VGroup(caja, f).move_to([4.3, 2.4, 0])
        f.move_to(caja)
        h = hervidor().scale(1.7).move_to([3.3, -1.9, 0])
        p = plancha().scale(1.5).move_to([6.2, -2.1, 0])
        self.add(g, h, p)


# ===================== portadas v2: gancho + escena + color propio =====================
def texto_gancho(lineas, size=86, borde="#000000", w=16):
    """lineas = [(texto, color), ...] apiladas, con contorno grueso y sombra dura."""
    g = VGroup()
    for t, c in lineas:
        m = T(t, size, c, "HEAVY")
        sh = m.copy().set_fill("#000000", 0.55).set_stroke(width=0).shift(RIGHT * 0.09 + DOWN * 0.09)
        g.add(VGroup(sh, m.copy().set_stroke(borde, w).set_fill(borde, 1), m))
    return g.arrange(DOWN, buff=0.12, aligned_edge=LEFT)


def sticker(txt, bg, fg="#FFFFFF", size=40, ang=0.0):
    t = T(txt, size, fg, "HEAVY")
    caja = RoundedRectangle(width=t.width + 0.6, height=t.height + 0.38, corner_radius=0.14, stroke_color="#000000", stroke_width=6).set_fill(bg, 1)
    sh = caja.copy().set_fill("#000000", 1).shift(RIGHT * 0.08 + DOWN * 0.08)
    return VGroup(sh, caja, t.move_to(caja)).rotate(ang)


def logo_esq(scene, pos=(6.9, -3.75)):
    lg = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(1.35).move_to([pos[0], pos[1], 0])
    scene.add(lg)


class Portada03(MovingCameraScene):
    """Cuarto de noche: puerta con apagador, cama con apagador, lámpara encendida."""
    def construct(self):
        from taller import foco_led, placa_interruptor, P
        W, H = config.frame_width, config.frame_height
        pared = Rectangle(width=W, height=H, stroke_width=0).set_fill("#1B1640", 1)
        piso = Polygon([-W / 2, -2.4, 0], [W / 2, -2.4, 0], [W / 2, -H / 2, 0], [-W / 2, -H / 2, 0], stroke_width=0).set_fill("#2A1F4F", 1)
        self.add(pared, piso)
        # luz cálida desde la lámpara
        f = foco_led(True, 0.9).scale(2.6).move_to([2.6, 2.5, 0])
        cono = Polygon(f.get_bottom() + LEFT * 0.4, f.get_bottom() + RIGHT * 0.4, [6.6, -4.1, 0], [-1.4, -4.1, 0], stroke_width=0).set_fill("#FFD36A", 0.16)
        glow = resplandor(f[0].get_center(), 3.4, "#FFC94A", 16, 0.06)
        cord = Line([2.6, 4.2, 0], f.get_top()).set_stroke("#E6E1FF", 5)
        # puerta
        puerta = VGroup(Rectangle(width=2.2, height=4.4, stroke_color="#0E0B24", stroke_width=6).set_fill("#5B3A86", 1),
                        Rectangle(width=1.6, height=1.5, stroke_color="#3F2763", stroke_width=4).shift(UP * 1.0),
                        Rectangle(width=1.6, height=1.5, stroke_color="#3F2763", stroke_width=4).shift(DOWN * 0.9),
                        Circle(radius=0.11, stroke_width=0).set_fill("#FFD36A", 1).shift(RIGHT * 0.75 + DOWN * 0.2)).move_to([-1.2, -0.2, 0])
        # cama
        cama = VGroup(RoundedRectangle(width=4.2, height=1.0, corner_radius=0.15, stroke_color="#0E0B24", stroke_width=6).set_fill("#E85D75", 1).move_to([5.0, -2.5, 0]),
                      RoundedRectangle(width=4.2, height=0.5, corner_radius=0.1, stroke_color="#0E0B24", stroke_width=6).set_fill("#F4F1FF", 1).move_to([5.0, -1.85, 0]),
                      RoundedRectangle(width=1.3, height=0.55, corner_radius=0.2, stroke_color="#0E0B24", stroke_width=5).set_fill("#FFFFFF", 1).move_to([6.4, -1.4, 0]),
                      RoundedRectangle(width=0.35, height=2.4, corner_radius=0.08, stroke_color="#0E0B24", stroke_width=6).set_fill("#7A4E2D", 1).move_to([7.2, -1.9, 0]),
                      Rectangle(width=0.2, height=0.5, stroke_width=0).set_fill("#0E0B24", 1).move_to([3.1, -3.15, 0]))
        s1 = placa_interruptor(P(0, 0), 1).scale(1.5).move_to([0.55, -0.1, 0])
        s2 = placa_interruptor(P(0, 0), 2).scale(1.5).move_to([3.6, -0.6, 0])
        aros = VGroup(*[Circle(radius=0.62, stroke_color="#FF3B30", stroke_width=10).move_to(s) for s in (s1, s2)])
        self.add(cono, glow, cord, puerta, cama, f, s1, s2, aros)
        n = VGroup(*[VGroup(Circle(radius=0.32, stroke_color="#000000", stroke_width=5).set_fill("#FF3B30", 1), T(str(k + 1), 34, WHITE, "HEAVY"))
                     for k in range(2)])
        for k, (c_, s) in enumerate(zip(n, (s1, s2))):
            c_[1].move_to(c_[0])
            c_.move_to(s.get_center() + UP * 0.85 + RIGHT * 0.5)
        self.add(n)
        txt = texto_gancho([("¿ENCENDER en la", "#FFFFFF"), ("PUERTA y apagar", "#FFD60A"), ("desde la CAMA?", "#FFFFFF")], 80)
        txt.scale_to_fit_width(7.6).move_to([-3.75, 2.35, 0])
        if txt.get_left()[0] < -7.7:
            txt.shift(RIGHT * (-7.7 - txt.get_left()[0]))
        st = sticker("APAGADOR DE ESCALERA", "#FF3B30", size=40, ang=0.05).move_to([-3.6, -2.45, 0])
        self.add(txt, st)
        logo_esq(self, (-6.9, 3.65 - 7.4))


class Portada04(MovingCameraScene):
    """Fondo amarillo, tomacorriente gigante, aro rojo en el agujero de tierra."""
    def construct(self):
        from taller import P
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill("#FFD60A", 1))
        rayos = VGroup(*[Polygon([4.2, 0, 0], [4.2 + 12 * np.cos(a), 12 * np.sin(a), 0], [4.2 + 12 * np.cos(a + 0.13), 12 * np.sin(a + 0.13), 0], stroke_width=0)
                         .set_fill("#FFC300", 1) for a in np.arange(0, TAU, 0.26)])
        self.add(rayos)
        placa = RoundedRectangle(width=4.6, height=6.6, corner_radius=0.35, stroke_color="#000000", stroke_width=8).set_fill("#FBFBF7", 1).move_to([4.3, -0.1, 0])
        sh = placa.copy().set_fill("#000000", 0.35).set_stroke(width=0).shift(RIGHT * 0.18 + DOWN * 0.18)
        caras = VGroup()
        for y in (1.45, -1.55):
            cara = RoundedRectangle(width=2.9, height=2.65, corner_radius=1.0, stroke_color="#BDB8AA", stroke_width=4).set_fill("#F3F1EA", 1).move_to([4.3, y, 0])
            fa = RoundedRectangle(width=0.27, height=0.8, corner_radius=0.08, stroke_width=0).set_fill("#202227", 1).move_to([4.95, y + 0.3, 0])
            ne = RoundedRectangle(width=0.27, height=1.0, corner_radius=0.08, stroke_width=0).set_fill("#202227", 1).move_to([3.65, y + 0.3, 0])
            ti = VGroup(Arc(radius=0.27, start_angle=PI, angle=PI, stroke_width=0).set_fill("#202227", 1),
                        Rectangle(width=0.54, height=0.22, stroke_width=0).set_fill("#202227", 1).shift(UP * 0.11)).move_to([4.3, y - 0.75, 0])
            caras.add(VGroup(cara, fa, ne, ti))
        tor = VGroup(Circle(radius=0.17, stroke_color="#8C8C8C", stroke_width=3).set_fill("#D9D9D9", 1), Line(LEFT * 0.12, RIGHT * 0.12).set_stroke("#6B6B6B", 4)).move_to([4.3, -0.05, 0])
        aro = Circle(radius=0.62, stroke_color="#E10600", stroke_width=14).move_to(caras[0][3])
        flecha = Arrow([1.3, -0.3, 0], aro.get_left() + LEFT * 0.05, color="#E10600", stroke_width=22, buff=0.05, max_tip_length_to_length_ratio=0.25)
        flecha.set_stroke("#E10600")
        self.add(sh, placa, caras, tor, flecha, aro)
        txt = texto_gancho([("¿Y ESTE", "#000000"), ("AGUJERO?", "#E10600")], 140, borde="#FFFFFF", w=18)
        txt.scale_to_fit_width(7.4).move_to([-3.7, 1.6, 0])
        st = sticker("¿Dónde va cada cable?", "#000000", "#FFD60A", 44, -0.04).move_to([-3.6, -1.15, 0])
        st2 = sticker("TOMACORRIENTE CON TIERRA", "#1F6FEB", size=34, ang=0.0).move_to([-3.6, -2.55, 0])
        self.add(txt, st, st2)
        logo_esq(self, (-6.9, -3.75))


class Portada05(MovingCameraScene):
    """Fondo rojo: breaker disparado con ¡CLIC!, hervidor + plancha."""
    def construct(self):
        from taller import hervidor, plancha, P
        from nema import breaker
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill("#D7263D", 1))
        franja = Polygon([-W / 2, -1.2, 0], [W / 2, -2.4, 0], [W / 2, -H / 2, 0], [-W / 2, -H / 2, 0], stroke_width=0).set_fill("#A4161A", 1)
        self.add(franja)
        bk = breaker("20", 0.46, 0.26, on=False).scale(9.0).rotate(PI / 2).move_to([4.6, 1.0, 0])
        boom = VGroup(*[Line([0, 0, 0], [1.4 * np.cos(a), 1.4 * np.sin(a), 0]).set_stroke("#FFD60A", 10) for a in np.linspace(0.2, PI - 0.2, 7)]).move_to(bk.get_top() + UP * 0.9 + RIGHT * 0.0)
        clic = sticker("¡CLIC!", "#FFD60A", "#000000", 56, 0.12).move_to([6.0, 3.3, 0])
        h = hervidor().scale(1.6).move_to([2.7, -2.4, 0])
        p = plancha().scale(1.5).move_to([5.9, -2.6, 0])
        mas = T("+", 120, "#FFFFFF", "HEAVY").move_to([4.35, -2.4, 0])
        self.add(boom, bk, clic, h, p, mas)
        txt = texto_gancho([("¿POR QUÉ SE", "#FFFFFF"), ("DISPARA EL", "#FFFFFF"), ("BREAKER?", "#FFD60A")], 104)
        txt.scale_to_fit_width(7.4).move_to([-3.6, 1.35, 0])
        st = sticker("LEY DE OHM · fácil", "#000000", "#FFFFFF", 44, -0.04).move_to([-3.9, -1.75, 0])
        self.add(txt, st)
        logo_esq(self, (-6.9, -3.75))


class PortadaV02(MovingCameraScene):
    """Portada vertical (2 primeros cuadros del Short): fondo azul marino, gancho grande."""
    def construct(self):
        from v02_cable import alambre, cable7
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=["#08142E", "#12305A"], opacity=1).set_sheen_direction(UR))
        txt = texto_gancho([("¿CABLE", "#FFFFFF"), ("o ALAMBRE?", "#2EC4DD")], 120)
        txt.scale_to_fit_width(8.0).move_to([0, 5.0, 0])
        a = alambre(6.4, 1.1, 1.6).move_to([-0.1, 1.0, 0])
        c = cable7(6.4, 1.1, 1.6, abierto=True).move_to([-0.1, -1.8, 0])
        la = sticker("1 HILO", "#FFFFFF", "#0B1C3D", 40, -0.05).next_to(a, UP, buff=0.3).align_to(a, LEFT)
        lc = sticker("7 HILOS", "#0E9BB5", "#FFFFFF", 40, 0.04).next_to(c, UP, buff=0.3).align_to(c, LEFT)
        st = sticker("NO son lo mismo", "#E5484D", size=52, ang=-0.04).move_to([0, -4.0, 0])
        self.add(txt, a, c, la, lc, st)
        logo_esq(self, (0, -6.2))


# ===================== portadas verticales de los shorts (azul marino, gancho + pieza protagonista)
def _ilus_short(k):
    import shorts_v as S
    from taller import foco_led, clavija, tomacorriente, P as PP, cable_hilos
    from nema import breaker, multimetro
    from dibujos_aves import aislador_pin
    if k == "v03":
        return VGroup(*[S.esfera(c_, 0.9) for c_ in ("#F79009", "#FFFFFF", "#FDB022")]).arrange(RIGHT, buff=0.3)
    if k == "v04":
        return S.transformador().scale(2.0)
    if k == "v05":
        return S.cara(11.0)
    if k == "v06":
        return clavija("5-15P", True).scale(4.2).rotate(PI)
    if k == "v07":
        d = S.ducha().scale(2.4)
        return VGroup(d, S.gotas(d[2].get_center() + DOWN * 0.9, 11).scale(2.2))
    if k in ("v08", "v09"):
        return breaker("20" if k == "v08" else "30", 0.46, 0.26).scale(9.0)
    if k == "v10":
        return aislador_pin(PP(0, 0), 0.42).scale(6.5)
    if k == "v11":
        return foco_led(True, 0.9).scale(4.8)
    if k == "v12":
        return VGroup(T("100", 220, "#E5484D", "HEAVY"), T("mA", 90, "#FFFFFF", "HEAVY")).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
    if k == "v13":
        c = cable_hilos(7.0, "#1B1B1B", 1.1, 1.2)
        return VGroup(resplandor(c.get_center(), 2.4, "#E5484D", 12, 0.06).stretch(2.2, 0), c)
    if k == "v14":
        return VGroup(S.seccion_awg(2.08, 1.6), S.seccion_awg(3.31, 1.6)).arrange(RIGHT, buff=0.6)
    if k == "v15":
        return VGroup(*[RoundedRectangle(width=6.5, height=0.7, corner_radius=0.35, stroke_width=2, stroke_color="#8F9AC8").set_fill(c_, 1)
                        for c_ in ("#16A34A", "#FFFFFF", "#1B1B1B")]).arrange(DOWN, buff=0.35)
    if k == "v16":
        return S.extintor("C").scale(2.6)
    if k == "v17":
        return multimetro().scale(2.6)
    if k == "v18":
        return S.motor().scale(2.4)


_STICK = {"v03": "NO son adornos", "v04": "120 Hz", "v05": "no es un error", "v06": "a propósito", "v07": "¡cuidado!",
          "v08": "protege al cable", "v09": "¡NO lo hagas!", "v10": "el aire aísla", "v11": "75 % menos", "v12": "muy poca",
          "v13": "I² × R", "v14": "al revés", "v15": "NEC vs IEC", "v16": "¡NUNCA!", "v17": "puede salvarte", "v18": "varias veces"}


class PortadaShort(MovingCameraScene):
    def construct(self):
        import os
        from shorts_guiones import SHORTS
        k = os.environ["CLAVE"]
        t1, t2, _ = SHORTS[k]
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=["#08142E", "#12305A"], opacity=1).set_sheen_direction(UR))
        txt = texto_gancho([(t1.upper() if len(t1) < 14 else t1, "#FFFFFF"), (t2, "#2EC4DD")], 100)
        txt.scale_to_fit_width(min(8.2, txt.width)).move_to([0, 4.6, 0])
        if txt.width > 8.2:
            txt.scale_to_fit_width(8.2)
        il = _ilus_short(k)
        il.scale_to_fit_height(min(5.0, il.height)).move_to([0, 0.2, 0])
        if il.width > 8.0:
            il.scale_to_fit_width(8.0)
        st = sticker(_STICK[k], "#E5484D", size=56, ang=-0.04).move_to([0, -3.6, 0])
        self.add(il, txt, st)
        logo_esq(self, (0, -6.2))

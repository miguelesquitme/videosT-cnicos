"""Reel R2 · ASÍ DETECTA UN SENSOR CAPACITIVO (fondo negro, paleta neón de alto contraste).
Render: FORMATO=v VOZ=eleven manim -qh --disable_caching -o final_r2 r2_capacitivo.py R2"""
from reel_base import *
from piezas_sensores import *
from guiones_r import R

shorts_v.SHORTS["r2"] = R["r2"]
P = lambda x, y: np.array([x, y, 0.0])
AGUA = "#1E90FF"


def tanque(w=3.6, h=5.6, nivel=0.0):
    """Tanque de polietileno, vista lateral: paredes translúcidas con costillas, tapa roscada, válvula de bola de salida."""
    g = VGroup()
    pared = RoundedRectangle(width=w, height=h, corner_radius=0.35, stroke_color="#C9D6E8", stroke_width=4).set_fill("#DCE6F2", 0.10)
    costillas = VGroup(*[Line(P(-w / 2 + 0.06, y), P(w / 2 - 0.06, y)).set_stroke("#C9D6E8", 1.5, 0.35) for y in np.linspace(-h / 2 + 0.6, h / 2 - 0.6, 6)])
    cuello = Rectangle(width=1.0, height=0.3, stroke_color="#C9D6E8", stroke_width=3).set_fill("#DCE6F2", 0.15).move_to(P(0, h / 2 + 0.15))
    tapa = RoundedRectangle(width=1.25, height=0.32, corner_radius=0.06, stroke_color="#0B4F9C", stroke_width=2).set_fill("#1D4ED8", 1).move_to(P(0, h / 2 + 0.46))
    estrias = VGroup(*[Line(P(x, h / 2 + 0.32), P(x, h / 2 + 0.6)).set_stroke("#0B3A7A", 1.2) for x in np.linspace(-0.55, 0.55, 12)])
    tubo = Rectangle(width=0.7, height=0.28, stroke_color="#98A2B3", stroke_width=1.5).set_fill("#5B6472", 1).move_to(P(w / 2 + 0.35, -h / 2 + 0.45))
    valv = VGroup(Rectangle(width=0.5, height=0.5, stroke_color="#98A2B3", stroke_width=1.5).set_fill("#C9CED6", 1),
                  Rectangle(width=0.7, height=0.14, stroke_width=0).set_fill("#E5484D", 1).shift(UP * 0.36 + RIGHT * 0.1)).move_to(P(w / 2 + 0.95, -h / 2 + 0.45))
    marcas = VGroup(*[VGroup(Line(P(-w / 2 + 0.08, y), P(-w / 2 + 0.36, y)).set_stroke("#E4E7EC", 2), T(f"{int(l)} L", 14, "#E4E7EC", "BOLD").move_to(P(-w / 2 + 0.7, y)))
                      for y, l in zip(np.linspace(-h / 2 + 0.9, h / 2 - 0.9, 4), (250, 500, 750, 1000))])
    agua = Rectangle(width=w - 0.12, height=0.01, stroke_width=0).set_fill(AGUA, 0.55).move_to(P(0, -h / 2 + 0.06), aligned_edge=DOWN)
    sup = Line(P(-w / 2 + 0.08, 0), P(w / 2 - 0.08, 0)).set_stroke("#7FD1FF", 3)
    sup.add_updater(lambda m: m.move_to(P(agua.get_x(), agua.get_top()[1])))
    g.add(agua, sup, pared, costillas, cuello, tapa, estrias, tubo, valv, marcas)
    g.agua, g.sup, g.pared, g.base_y, g.w, g.h = agua, sup, pared, -h / 2 + 0.06, w, h
    return g


def llenar(t, altura):
    return t.agua.animate.stretch_to_fit_height(max(0.01, altura), about_edge=DOWN)


def soporte_l(p, s=1.0):
    """Escuadra de acero galvanizado en L con 2 tornillos."""
    a = Rectangle(width=0.16, height=1.6, stroke_color="#5B6472", stroke_width=1.5).set_fill("#B8BEC8", 1)
    b = Rectangle(width=1.1, height=0.16, stroke_color="#5B6472", stroke_width=1.5).set_fill("#B8BEC8", 1).move_to(P(0.47, -0.72))
    tor = VGroup(*[Circle(radius=0.06, stroke_color="#475467", stroke_width=1).set_fill("#E4E7EC", 1).move_to(P(0, y)) for y in (0.45, -0.35)])
    return VGroup(a, b, tor).scale(s).move_to(p)


def corte_capacitivo(s=1.0):
    """Corte del sensor capacitivo: electrodo activo en la cara, electrodo de compensación (blindaje), oscilador RC,
    demodulador, disparador, salida y potenciómetro de sensibilidad. Cara a la DERECHA. Largo ≈ 6,6, alto ≈ 1,9."""
    g = VGroup()
    h = 1.9
    funda = Rectangle(width=6.4, height=h, stroke_color=NIQ_OO, stroke_width=2).set_fill(NIQ, 1)
    interior = Rectangle(width=6.3, height=h - 0.24, stroke_width=0).set_fill("#2B2416", 1)
    cara = Rectangle(width=0.3, height=h - 0.1, stroke_color="#475467", stroke_width=1.5).set_fill("#2B3038", 1).move_to(P(3.35, 0))
    e_act = Rectangle(width=0.08, height=1.25, stroke_width=0).set_fill("#E0A86E", 1).move_to(P(3.12, 0))
    e_blind = VGroup(Rectangle(width=0.06, height=1.55, stroke_width=0).set_fill("#9A6A3A", 1).move_to(P(2.85, 0)),
                     Rectangle(width=0.5, height=0.06, stroke_width=0).set_fill("#9A6A3A", 1).move_to(P(3.08, 0.78)),
                     Rectangle(width=0.5, height=0.06, stroke_width=0).set_fill("#9A6A3A", 1).move_to(P(3.08, -0.78)))
    pcb = Rectangle(width=4.4, height=0.14, stroke_width=0).set_fill("#166534", 1).move_to(P(0.3, -0.12))
    comps = VGroup(); ics = []
    for x, n in ((1.85, "OSC RC"), (1.0, "DEMOD"), (0.15, "DISPARO"), (-0.7, "SALIDA")):
        ic = Rectangle(width=0.62, height=0.28, stroke_color="#000000", stroke_width=1).set_fill("#111318", 1).move_to(P(x, 0.09))
        comps.add(ic, T(n, 5.2, "#E4E7EC", "HEAVY").move_to(ic)); ics.append(ic)
    pot = VGroup(Rectangle(width=0.36, height=0.36, stroke_color="#000", stroke_width=1).set_fill("#1D4ED8", 1).move_to(P(-2.3, 0.18)),
                 Circle(radius=0.12, stroke_width=0).set_fill("#E4E7EC", 1).move_to(P(-2.3, 0.18)),
                 Line(P(-2.38, 0.18), P(-2.22, 0.18)).set_stroke("#101828", 2))
    alam = VGroup(Line(P(3.08, 0.0), P(2.2, 0.05)).set_stroke("#E0A86E", 2), Line(P(2.85, -0.5), P(2.2, -0.08)).set_stroke("#9A6A3A", 2))
    led = Rectangle(width=0.12, height=h - 0.25, stroke_width=0).set_fill("#FFB020", 0.9).move_to(P(-2.95, 0))
    cables = VGroup(*[Line(P(-3.2, y), P(-2.55, y)).set_stroke(c, 3) for y, c in ((0.5, "#8B5A2B"), (-0.45, "#1D4ED8"), (-0.65, "#B8C0CC"))])
    g.add(funda, interior, cara, e_blind, e_act, pcb, comps, pot, alam, led, cables)
    g.scale(s)
    g.e_act, g.e_blind, g.ics, g.pot = e_act, e_blind, ics, pot
    return g


def lineas_campo(p, r=1.6, n=7, color="#00E5FF"):
    """Líneas del campo eléctrico que salen del electrodo activo y regresan por los bordes (campo esférico)."""
    g = VGroup()
    for k in range(n):
        y0 = (k - (n - 1) / 2) * 0.16
        alto = 0.35 + abs(y0) * 2.2
        c = CubicBezier(p + UP * y0, p + RIGHT * r * (0.6 + 0.08 * k % 2) + UP * (y0 * 2.2), p + RIGHT * 0.2 + UP * (np.sign(y0 + 1e-6) * (alto + 0.3)),
                        p + LEFT * 0.25 + UP * np.sign(y0 + 1e-6) * 0.78)
        g.add(DashedVMobject(c.set_stroke(color, 2.5), num_dashes=14))
    return g


class R2(ReelTec):
    TEMA = "negro"
    CLAVE = "r2"
    TIT1, TIT2 = R["r2"][0], R["r2"][1]

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        # ------------------------------------------------ gancho
        self.voz("gancho")
        tq = tanque(3.6, 6.0).move_to([-1.2, -0.5, 0])
        self.play(FadeIn(tq), run_time=0.5)
        y_s = tq.base_y + tq.get_y() - (-0.5) + 3.6  # altura del sensor sobre el fondo
        y_s = tq.get_bottom()[1] + 3.8
        sen = sensor_m18(0.7, "capacitivo", "#2B3038")
        sen.rotate(PI).move_to([0, y_s, 0])
        sen.shift(np.array([tq.pared.get_right()[0] + 0.02, y_s, 0]) - sen.cara.get_left())
        sop = soporte_l([tq.pared.get_right()[0] + 1.2, y_s - 0.2, 0], 0.8)
        self.play(FadeIn(sen, shift=LEFT * 0.3), FadeIn(sop), run_time=0.4)
        self.frac(0.1)
        alt = y_s - tq.agua.get_bottom()[1] + 0.25
        self.play(llenar(tq, alt), run_time=2.6, rate_func=linear)
        self.play(sen.led.animate.set_fill("#FFB020"), Flash(sen.led, color=Am, flash_radius=0.4), run_time=0.35)
        t1 = self.tag("sin contacto con el agua", C, 28).move_to([1.6, 2.6, 0])
        t2 = self.tag("a través de la pared", G, 28).move_to([1.6, 1.85, 0])
        self.play(FadeIn(t1, shift=DOWN * 0.1), FadeIn(t2, shift=DOWN * 0.1), run_time=0.35)
        er = self.card("CONSTANTE DIELÉCTRICA", ["εr: la clave de este sensor"], Am, 7.8, 30).move_to([0, -4.6, 0])
        self.frac(0.35)
        self.play(FadeIn(er, shift=UP * 0.15), run_time=0.35)
        self.cerrar_voz(0.05)
        tq.sup.clear_updaters()
        self.limpiar(tq, sen, sop, t1, t2, er)

        # ------------------------------------------------ p1 electrodo y oscilador
        self.voz("p1")
        self.chip("1", "POR DENTRO", C)
        co = corte_capacitivo(1.05).move_to([-1.05, 1.6, 0])
        self.play(FadeIn(co), run_time=0.5)
        cara_p = np.array([co.get_right()[0], co.get_y(), 0])
        l1 = self.leyenda("electrodo activo", co.e_act.get_top(), [1.0, 3.3, 0], C, 26)
        l2 = self.leyenda("electrodo de compensación", co.e_blind[0].get_bottom(), [-0.9, -0.35, 0], Am, 24)
        self.play(FadeIn(l1), run_time=0.3)
        self.frac(0.1)
        campo = lineas_campo(cara_p + LEFT * 0.35, 1.6, 7, C)
        self.play(Create(campo), run_time=0.9)
        cap = self.tag("capacitor abierto", C, 28).move_to([2.55, -1.2, 0])
        self.play(FadeIn(cap), FadeIn(l2), run_time=0.35)
        self.frac(0.35)
        l3 = self.leyenda("oscilador RC", co.ics[0].get_bottom(), [-2.3, -1.2, 0], G, 26)
        ax = self.ejes(7.4, 1.8, (0, 1, 0.25), (-1.2, 1.2, 1)).move_to([0, -3.0, 0])
        plano = ax.plot(lambda t: 0.04 * np.sin(TAU * 18 * t), x_range=[0, 1, 0.002], color=G, stroke_width=4)
        tp = self.tx("capacitancia baja: el oscilador NO arranca", 26, self.th["txt"], "HEAVY").next_to(ax, DOWN, buff=0.15)
        self.play(FadeIn(l3), Create(ax), Create(plano), FadeIn(tp), run_time=0.8)
        self.cerrar_voz(0.05)
        self.limpiar(l1, l2, l3, cap, ax, plano, tp)

        # ------------------------------------------------ p2 fórmula
        self.voz("p2")
        self.chip("2", "LA FÓRMULA", Am)
        self.play(VGroup(co, campo).animate.scale(0.75, about_point=cara_p).shift(LEFT * 1.0 + DOWN * 0.1), run_time=0.5)
        cara_p = cara_p + LEFT * 1.0 + DOWN * 0.1
        f = MathTex(r"C=\varepsilon_0\cdot", r"\varepsilon_r", r"\cdot\frac{A}{d}", color=WHITE).scale(1.6).move_to([0, -0.4, 0])
        f[1].set_color(Am)
        self.play(Write(f), run_time=1.0)
        cuerpo = Square(1.1, stroke_color="#7FD1FF", stroke_width=3).set_fill(AGUA, 0.6).move_to([cara_p[0] + 1.9, cara_p[1], 0])
        self.frac(0.3)
        self.play(FadeIn(cuerpo), run_time=0.3)
        self.play(cuerpo.animate.move_to([cara_p[0] + 0.85, cara_p[1], 0]), Indicate(f[1], color=Am, scale_factor=1.3), run_time=0.9)
        ax = self.ejes(7.4, 1.8, (0, 1, 0.25), (-1.2, 1.2, 1)).move_to([0, -2.6, 0])
        osc = ax.plot(lambda t: (0.04 if t < 0.3 else min(1, 0.04 + (t - 0.3) * 4)) * np.sin(TAU * 18 * t), x_range=[0, 1, 0.001], color=G, stroke_width=4)
        self.play(Create(ax), Create(osc), run_time=1.0)
        sal = self.tag("C sube → oscila → salida conmuta", G, 28).move_to([0, -4.3, 0])
        self.play(FadeIn(sal), run_time=0.3)
        self.cerrar_voz(0.05)
        self.limpiar(co, campo, f, cuerpo, ax, osc, sal)

        # ------------------------------------------------ p3 constante dieléctrica
        self.voz("p3")
        self.chip("3", "CONSTANTE DIELÉCTRICA εr", Am)
        x0, w = -1.6, 4.6
        logx = lambda v: x0 + w * np.log10(v) / 2.0
        eje = VGroup(Line([x0, 3.2, 0], [x0, 0.3, 0]).set_stroke(self.th["ejes"], 2.5),
                     *[VGroup(DashedLine([logx(v), 3.2, 0], [logx(v), 0.3, 0]).set_stroke("#2A2F38", 1.5), self.tx(str(v), 22, self.th["txt2"]).move_to([logx(v), 0.05, 0])) for v in (1, 10, 100)])
        fl = VGroup(self.tx("escala logarítmica", 18, self.th["txt2"]).move_to([2.6, -0.3, 0]))
        filas = VGroup()
        for k, (nom, a_, b_, col) in enumerate((("AIRE", 1, 1, "#5B6472"), ("PLÁSTICO", 2, 4, Vi), ("AGUA", 80, 80, C))):
            y = 2.75 - k * 1.0
            t = self.tx(nom, 26, self.th["txt"], "HEAVY").move_to([-3.05, y, 0])
            ancho = max(0.06, logx(b_) - x0)
            barra = Rectangle(width=ancho, height=0.55, stroke_width=0).set_fill(col, 1).move_to([x0 + ancho / 2, y, 0])
            val = self.tx("≈ 1" if b_ == 1 else ("2–4" if nom == "PLÁSTICO" else "≈ 80"), 26, col if col != "#5B6472" else WHITE, "HEAVY").next_to(barra, RIGHT, buff=0.12)
            filas.add(VGroup(t, barra, val))
        self.play(FadeIn(eje), FadeIn(fl), run_time=0.3)
        for k, f_ in enumerate(filas):
            self.play(FadeIn(f_[0]), GrowFromEdge(f_[1], LEFT), FadeIn(f_[2]), run_time=0.45)
            self.frac(0.08)
        # corte de la pared con agua
        yy = -2.6
        pared = Rectangle(width=0.5, height=2.6, stroke_color="#C9D6E8", stroke_width=2).set_fill("#DCE6F2", 0.35).move_to([0.2, yy, 0])
        agua = Rectangle(width=3.4, height=2.6, stroke_width=0).set_fill(AGUA, 0.6).move_to([2.15, yy, 0])
        sen = sensor_m18(0.85, "capacitivo", "#2B3038", True)
        sen.shift(np.array([-0.06, yy, 0]) - sen.cara.get_right())
        cota = VGroup(DoubleArrow([-0.05, yy - 1.55, 0], [0.45, yy - 1.55, 0], buff=0, stroke_width=3, tip_length=0.12, color=Rr),
                      self.tx("pared ≤ 4 mm", 24, Rr, "HEAVY").move_to([0.2, yy - 1.95, 0]))
        lin = VGroup(*[DashedLine([0.0, yy + dy, 0], [3.4, yy + dy * 1.6, 0], dash_length=0.12).set_stroke(C, 3) for dy in (-0.6, -0.3, 0, 0.3, 0.6)])
        self.frac(0.12)
        self.play(FadeIn(agua), FadeIn(pared), FadeIn(sen), run_time=0.5)
        self.play(Create(lin), FadeIn(cota), run_time=0.7)
        ti = VGroup(self.tx("pared", 22, "#C9D6E8", "HEAVY").next_to(pared, UP, buff=0.1), self.tx("agua", 24, "#7FD1FF", "HEAVY").move_to(agua.get_top() + DOWN * 0.3 + RIGHT * 0.9))
        self.play(FadeIn(ti), run_time=0.25)
        self.cerrar_voz(0.05)
        self.limpiar(eje, fl, filas, pared, agua, sen, cota, lin, ti)

        # ------------------------------------------------ p3b factor de corrección
        self.voz("p3b")
        self.chip("4", "FACTOR DE CORRECCIÓN", Vi)
        ref = self.card("Sn SE MIDE CON METAL ATERRIZADO", ["placa Fe 360 de 1 mm"], "#5B6472", 7.8, 26).move_to([0, 3.0, 0])
        self.play(FadeIn(ref, shift=DOWN * 0.15), run_time=0.35)
        x0, w = -1.0, 5.0
        filas = VGroup()
        for k, (nom, a_, b_, col) in enumerate((("AGUA", 1.0, 1.0, C), ("VIDRIO", 0.4, 0.6, Vi), ("PVC", 0.2, 0.47, Am))):
            y = 1.55 - k * 1.05
            t = self.tx(nom, 26, self.th["txt"], "HEAVY").move_to([-2.85, y, 0])
            b1 = Rectangle(width=w * a_, height=0.55, stroke_width=0).set_fill(col, 1).move_to([x0 + w * a_ / 2, y, 0])
            b2 = Rectangle(width=max(0.01, w * (b_ - a_)), height=0.55, stroke_color=col, stroke_width=2).set_fill(col, 0.3).move_to([x0 + w * (a_ + b_) / 2, y, 0])
            txt = "1 (referencia)" if a_ == b_ else f"{a_:.1f}–{b_:.2f}".replace(".", ",").replace("0,4–0,60", "0,4–0,6")
            val = self.tx(txt, 24, "#000000" if a_ == b_ else WHITE, "HEAVY")
            val.move_to(b1) if a_ == b_ else val.next_to(b2, RIGHT, buff=0.1)
            filas.add(VGroup(t, b1, b2, val))
        for f_ in filas:
            self.play(FadeIn(f_[0]), GrowFromEdge(f_[1], LEFT), FadeIn(f_[2]), FadeIn(f_[3]), run_time=0.4)
            self.frac(0.1)
        botella = VGroup(RoundedRectangle(width=1.2, height=2.3, corner_radius=0.3, stroke_color="#A7F3D0", stroke_width=4).set_fill("#A7F3D0", 0.08),
                         Rectangle(width=0.5, height=0.5, stroke_color="#A7F3D0", stroke_width=4).set_fill("#A7F3D0", 0.08).shift(UP * 1.4),
                         Rectangle(width=0.6, height=0.18, stroke_width=0).set_fill(Rr, 1).shift(UP * 1.72)).move_to([2.6, -3.1, 0])
        sen = sensor_m18(0.8, "capacitivo", "#2B3038", False)
        sen.shift(np.array([1.75, -3.1, 0]) - sen.cara.get_right())
        nodet = self.tag("vidrio vacío: no lo ve", Rr, 28).move_to([0, -4.95, 0])
        self.frac(0.12)
        self.play(FadeIn(botella), FadeIn(sen), run_time=0.4)
        self.play(FadeIn(nodet), run_time=0.3)
        self.cerrar_voz(0.05)
        self.limpiar(ref, filas, botella, sen, nodet)

        # ------------------------------------------------ p4 ajuste del potenciómetro
        self.voz("p4")
        self.chip("5", "AJUSTE DE SENSIBILIDAD", G)
        sen = sensor_m18(1.7, "capacitivo", "#2B3038", True)
        sen.move_to([1.4, 2.0, 0])
        self.play(FadeIn(sen), run_time=0.35)
        self.zoom_a(sen, sen.pot, 0.75, [0.0, 3.05, 0], 0.8)
        pc = sen.pot[0].get_center()
        dial = VGroup(Circle(radius=1.6, stroke_color="#2A2F38", stroke_width=6).move_to([0, -3.3, 0]),
                      Circle(radius=1.15, stroke_color="#98A2B3", stroke_width=3).set_fill("#2B3038", 1).move_to([0, -3.3, 0]))
        ranura = Line([-0.9, -3.3, 0], [0.9, -3.3, 0]).set_stroke(WHITE, 10)
        mm_ = VGroup(self.tx("−", 40, Rr, "HEAVY").move_to([-2.1, -3.3, 0]), self.tx("+", 40, G, "HEAVY").move_to([2.1, -3.3, 0]))
        self.play(FadeIn(dial), FadeIn(ranura), FadeIn(mm_), run_time=0.35)
        c0 = np.array([0, -3.3, 0])
        p1_ = self.tag("1 · izquierda hasta APAGAR", Rr, 26).move_to([0, -1.2, 0])
        self.play(FadeIn(p1_), Rotate(ranura, PI / 3, about_point=c0), sen.led.animate.set_fill("#5A4A1E"), run_time=1.0)
        self.frac(0.35)
        p2_ = self.tag("2 · derecha hasta ENCENDER", G, 26).move_to([0, -1.2, 0])
        self.play(FadeOut(p1_), FadeIn(p2_), Rotate(ranura, -PI / 2, about_point=c0), run_time=0.9)
        self.play(sen.led.animate.set_fill("#FFB020"), run_time=0.2)
        self.frac(0.3)
        p3_ = self.tag("3 · media vuelta más (180°)", C, 26).move_to([0, -1.2, 0])
        arco = Arc(radius=1.95, start_angle=PI / 2 + 0.25, angle=-PI, color=C, stroke_width=6).move_arc_center_to(c0).add_tip(tip_length=0.25)
        self.play(FadeOut(p2_), FadeIn(p3_), Create(arco), Rotate(ranura, -PI, about_point=c0), run_time=1.2)
        fx = self.tx("compensa humedad y temperatura", 26, self.th["txt2"], "HEAVY").move_to([0, -5.4, 0])
        self.play(FadeIn(fx), run_time=0.25)
        self.cerrar_voz(0.05)
        self.limpiar(sen, dial, ranura, mm_, p3_, arco, fx)

        # ------------------------------------------------ p5 cuidados
        self.voz("p5")
        self.chip("!", "DOS FALLAS TÍPICAS", Rr)
        tq1 = tanque(2.3, 4.4).move_to([-2.75, 0.6, 0])
        tq2 = tanque(2.3, 4.4).move_to([2.1, 0.6, 0])
        tq1.sup.clear_updaters(); tq2.sup.clear_updaters()
        tq1.remove(tq1.sup); tq2.remove(tq2.sup)
        tq1.agua.stretch_to_fit_height(1.6, about_edge=DOWN)
        espuma = VGroup(*[Circle(radius=np.random.uniform(0.08, 0.17), stroke_color="#E4E7EC", stroke_width=2).set_fill(WHITE, 0.6).move_to([tq1.get_x() + np.random.uniform(-0.95, 0.95), tq1.agua.get_top()[1] + np.random.uniform(0.05, 0.9), 0]) for _ in range(26)])
        s1 = sensor_m18(0.42, "capacitivo", "#2B3038", True)
        s1.rotate(PI); s1.shift(np.array([tq1.pared.get_right()[0] + 0.02, tq1.agua.get_top()[1] + 0.75, 0]) - s1.cara.get_left())
        s2 = sensor_m18(0.42, "capacitivo", "#2B3038", True)
        s2.rotate(PI); s2.shift(np.array([tq2.pared.get_right()[0] + 0.02, tq2.get_y() + 0.4, 0]) - s2.cara.get_left())
        costra = VGroup(*[Ellipse(width=0.18, height=np.random.uniform(0.3, 0.7)).set_fill("#8B5A2B", 0.85).set_stroke(width=0).move_to([tq2.pared.get_right()[0] - 0.12, tq2.get_y() + 0.4 + np.random.uniform(-0.5, 0.5), 0]) for _ in range(6)])
        self.play(FadeIn(tq1), FadeIn(espuma), FadeIn(s1), run_time=0.5)
        a1 = self.card("1 · SENSIBILIDAD ALTA", ["ve la pared o la espuma"], Am, 7.8, 26).move_to([0, -2.6, 0])
        self.play(FadeIn(a1, shift=UP * 0.15), run_time=0.35)
        self.frac(0.45)
        self.play(FadeIn(tq2), FadeIn(s2), FadeIn(costra), run_time=0.5)
        vacio = self.tag("tanque vacío", "#5B6472", 22).next_to(tq2, UP, buff=0.12)
        a2 = self.card("2 · PRODUCTO PEGADO", ["salida activada con el tanque vacío"], Rr, 7.8, 26).move_to([0, -4.0, 0])
        self.play(FadeIn(vacio), FadeIn(a2, shift=UP * 0.15), run_time=0.4)
        self.cerrar_voz(0.05)
        self.limpiar(tq1, tq2, espuma, s1, s2, costra, a1, a2, vacio)
        self.quitar_chip()
        self.final("Detecta εr: agua sí, pared de plástico casi no")


class PortadaR2(Scene):
    def construct(self):
        from miniaturas import sticker, logo_esq
        self.add(Rectangle(width=9.2, height=16.4, stroke_width=0).set_fill("#000000", 1))
        t = VGroup(T("ASÍ DETECTA", 96, "#FFFFFF", "HEAVY"), T("A TRAVÉS", 110, "#00E5FF", "HEAVY"), T("DEL PLÁSTICO", 104, "#FFB020", "HEAVY")).arrange(DOWN, buff=0.12)
        t.scale_to_fit_width(8.4).move_to([0, 4.7, 0])
        tq = tanque(3.6, 5.4).move_to([-1.3, -1.0, 0])
        tq.sup.clear_updaters()
        tq.agua.stretch_to_fit_height(3.4, about_edge=DOWN)
        tq.sup.move_to([tq.agua.get_x(), tq.agua.get_top()[1], 0])
        sen = sensor_m18(0.85, "capacitivo", "#2B3038", True)
        sen.rotate(PI)
        sen.shift(np.array([tq.pared.get_right()[0] + 0.02, tq.get_bottom()[1] + 2.6, 0]) - sen.cara.get_left())
        st = sticker("SENSOR CAPACITIVO", "#FF4D6D", size=60, ang=-0.03).move_to([0, -5.2, 0])
        st.scale_to_fit_width(min(st.width, 8.3))
        self.add(tq, sen, t, st)
        logo_esq(self, (3.6, 7.3))

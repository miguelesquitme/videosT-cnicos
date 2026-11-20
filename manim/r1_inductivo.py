"""Reel R1 · ASÍ DETECTA METAL UN SENSOR INDUCTIVO (fondo blanco).
Render: FORMATO=v VOZ=eleven manim -qh --disable_caching -o final_r1 r1_inductivo.py R1"""
from reel_base import *
from piezas_sensores import *
from guiones_r import R

shorts_v.SHORTS["r1"] = R["r1"]
MM = 0.45  # unidades de pantalla por milímetro en la regla


class R1(ReelTec):
    TEMA = "blanco"
    CLAVE = "r1"
    TIT1, TIT2 = R["r1"][0], R["r1"][1]

    def regla(self, x0, y, mm=10, marcas=(0, 2, 4, 6, 8, 10)):
        base = Line([x0, y, 0], [x0 + mm * MM, y, 0]).set_stroke(self.th["txt"], 3)
        ticks = VGroup(*[Line([x0 + k * MM, y, 0], [x0 + k * MM, y + (0.18 if k % 2 == 0 else 0.1), 0]).set_stroke(self.th["txt"], 2) for k in range(mm + 1)])
        nums = VGroup(*[self.tx(str(k), 20, self.th["txt2"]).move_to([x0 + k * MM, y - 0.25, 0]) for k in marcas])
        u = self.tx("mm", 20, self.th["txt2"]).next_to(base, RIGHT, buff=0.12)
        return VGroup(base, ticks, nums, u)

    def cuerpo(self):
        A, N, V, Rj = self.ac(0), self.ac(1), self.ac(2), self.ac(3)
        # ------------------------------------------------ gancho
        self.voz("gancho")
        sen = sensor_m18(1.3)
        sen.shift(np.array([-0.55, 1.9, 0]) - sen.cara.get_right())
        cx = sen.cara.get_right()[0]
        self.play(FadeIn(sen, shift=RIGHT * 0.3), run_time=0.5)
        rg = self.regla(cx, 0.75)
        self.play(FadeIn(rg), run_time=0.3)
        ac_ = placa_metal("acero", 0.26, 2.0).move_to([3.9, 1.9, 0])
        t_ac = self.tag("ACERO", "#475467", 24).next_to(ac_, UP, buff=0.12)
        self.play(FadeIn(ac_), FadeIn(t_ac), run_time=0.3)
        destino = cx + 8 * MM + 0.13
        self.play(ac_.animate.set_x(destino), t_ac.animate.set_x(destino), run_time=0.9)
        self.play(sen.led.animate.set_fill("#FDB022"), Flash(sen.led, color=N, flash_radius=0.35), run_time=0.3)
        r8 = self.tag("ACERO: detecta a 8 mm", V, 34).move_to([0, -0.7, 0])
        self.play(FadeIn(r8), run_time=0.25)
        self.frac(0.42)
        al = placa_metal("aluminio", 0.26, 2.0).move_to([3.9, 1.9, 0])
        t_al = self.tag("ALUMINIO", "#98A2B3", 24).next_to(al, UP, buff=0.12)
        self.play(FadeOut(ac_), FadeOut(t_ac), sen.led.animate.set_fill("#8A6A1E"), FadeIn(al), FadeIn(t_al), run_time=0.35)
        self.play(al.animate.set_x(cx + 8 * MM + 0.13), t_al.animate.set_x(cx + 8 * MM + 0.13), run_time=0.6)
        x_ = self.tag("ALUMINIO a 8 mm: no detecta", Rj, 34).move_to([0, -1.75, 0])
        self.play(FadeIn(x_), run_time=0.25)
        self.play(al.animate.set_x(cx + 3.6 * MM + 0.13), t_al.animate.set_x(cx + 3.6 * MM + 0.13), run_time=0.9)
        self.play(sen.led.animate.set_fill("#FDB022"), run_time=0.2)
        r4 = self.tag("ALUMINIO: detecta a menos de 4 mm", N, 34).move_to([0, -2.8, 0])
        self.play(FadeIn(r4), run_time=0.25)
        q = self.card("¿POR QUÉ?", ["la respuesta está en el principio físico"], A, 7.8, 32).move_to([0, -4.4, 0])
        self.frac(0.25)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.35)
        self.cerrar_voz(0.05)
        self.limpiar(sen, rg, al, t_al, r8, x_, r4, q)

        # ------------------------------------------------ p1 principio
        self.voz("p1")
        self.chip("1", "POR DENTRO", A)
        co = corte_inductivo(1.25).move_to([-0.15, 1.5, 0])
        self.play(FadeIn(co), run_time=0.6)
        l1 = self.leyenda("núcleo de ferrita tipo copa", co.nucleo.get_top() + LEFT * 0.05, [-0.6, 3.25, 0], "#344054", 26)
        l2 = self.leyenda("bobina", co.bobina.get_bottom(), [2.9, -0.5, 0], N, 26)
        l3 = self.leyenda("oscilador LC", co.ics[0].get_bottom(), [0.3, -0.5, 0], A, 26)
        self.play(FadeIn(l1), run_time=0.3)
        self.frac(0.15)
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.35)
        self.frac(0.3)
        cara_p = np.array([co.get_right()[0] + 0.02, co.get_y(), 0])
        ondas = VGroup(*[campo_frente(cara_p, 4, 0.25, 0.25, A, 4) for _ in range(1)])
        self.play(Create(ondas), run_time=0.6)
        ax = self.ejes(7.6, 2.6, (0, 1, 0.25), (-1.2, 1.2, 1)).move_to([0, -2.9, 0])
        osc = ax.plot(lambda t: 0.95 * np.sin(TAU * 14 * t), x_range=[0, 1, 0.001], color=A, stroke_width=3)
        lab = self.tx("oscilación de alta frecuencia: amplitud constante", 26, self.th["txt"], "HEAVY").next_to(ax, DOWN, buff=0.15)
        self.play(Create(ax), Create(osc), FadeIn(lab), run_time=1.0)
        for _ in range(2):
            self.play(ondas.animate.scale(1.08, about_point=cara_p).set_stroke(opacity=0.5), run_time=0.45)
            self.play(ondas.animate.scale(1 / 1.08, about_point=cara_p).set_stroke(opacity=1), run_time=0.45)
        self.cerrar_voz(0.05)
        self.play(FadeOut(VGroup(l1, l2, l3, ax, osc, lab)), run_time=0.3)

        # ------------------------------------------------ p2 Foucault
        self.voz("p2")
        self.chip("2", "CORRIENTES DE FOUCAULT", N)
        self.play(VGroup(co, ondas).animate.scale(0.8, about_point=cara_p).shift(LEFT * 1.0), run_time=0.6)
        cara_p = np.array([co.get_right()[0] + 0.02, co.get_y(), 0])
        pl = placa_metal("acero", 0.3, 2.2).move_to([cara_p[0] + 0.75, cara_p[1], 0])
        self.play(FadeIn(pl, shift=LEFT * 0.3), run_time=0.4)
        rem = VGroup(*[Ellipse(width=0.16, height=h, stroke_color=N, stroke_width=3).move_to(pl.get_center()) for h in (0.5, 0.95, 1.4)])
        flech = VGroup(*[Triangle(fill_opacity=1, stroke_width=0).set_fill(N, 1).scale(0.07).move_to(e.get_top()).rotate(-PI / 2) for e in rem])
        self.play(Create(rem), FadeIn(flech), run_time=0.6)
        tf = self.tag("corrientes de Foucault en el metal", N, 28).move_to([0, -0.15, 0])
        self.play(FadeIn(tf), run_time=0.25)
        ax = self.ejes(7.4, 2.4, (0, 1, 0.25), (-1.2, 1.2, 1)).move_to([0.25, -2.0, 0])
        amp = lambda t: 0.95 if t < 0.35 else (0.95 - 0.7 * min(1, (t - 0.35) / 0.25))
        osc = ax.plot(lambda t: amp(t) * np.sin(TAU * 20 * t), x_range=[0, 1, 0.0008], color=A, stroke_width=3)
        env = ax.plot(lambda t: amp(t), x_range=[0, 1, 0.005], color=N, stroke_width=3)
        u_on = DashedLine(ax.c2p(0, 0.5), ax.c2p(1, 0.5)).set_stroke(Rj, 3)
        u_off = DashedLine(ax.c2p(0, 0.62), ax.c2p(1, 0.62)).set_stroke("#F79009", 3)
        lu = VGroup(self.tx("conecta", 20, Rj, "HEAVY").move_to(ax.c2p(0.86, 0.5) + DOWN * 0.17), self.tx("desconecta", 20, "#B54708", "HEAVY").move_to(ax.c2p(0.86, 0.62) + UP * 0.17))
        self.frac(0.12)
        self.play(Create(ax), Create(osc), run_time=1.2)
        self.play(Create(env), run_time=0.5)
        self.frac(0.15)
        self.play(Create(u_on), Create(u_off), FadeIn(lu), run_time=0.4)
        hb = self.tag("histéresis: dos umbrales", Rj, 26).move_to([1.8, -0.75, 0])
        self.play(FadeIn(hb), run_time=0.25)
        ax2 = self.ejes(7.4, 1.1, (0, 1, 0.25), (0, 1.2, 1)).move_to([0.25, -4.25, 0])
        sal = ax2.plot(lambda t: 1.0 if t > 0.54 else 0.05, x_range=[0, 1, 0.002], color=V, stroke_width=5, use_smoothing=False)
        ls = self.tx("salida PNP conmuta a 24 V", 26, V, "HEAVY").next_to(ax2, DOWN, buff=0.1)
        self.play(Create(ax2), Create(sal), FadeIn(ls), run_time=0.7)
        self.cerrar_voz(0.05)
        self.limpiar(co, ondas, pl, rem, flech, tf, ax, osc, env, u_on, u_off, lu, hb, ax2, sal, ls)

        # ------------------------------------------------ p3 materiales
        self.voz("p3")
        self.chip("3", "FACTOR DE CORRECCIÓN", V)
        datos = [("acero", "ACERO DULCE", 1.0, 1.0), ("inox", "INOXIDABLE", 0.60, 1.00), ("laton", "LATÓN", 0.35, 0.50),
                 ("aluminio", "ALUMINIO", 0.35, 0.50), ("cobre", "COBRE", 0.25, 0.45)]
        x0, w = -1.0, 4.9
        eje = VGroup(Line([x0, 3.1, 0], [x0, -3.4, 0]).set_stroke(self.th["ejes"], 2.5),
                     *[VGroup(DashedLine([x0 + w * v, 3.1, 0], [x0 + w * v, -3.4, 0]).set_stroke("#D0D5DD", 1.5),
                              self.tx(f"{v:.2f}".replace(".", ","), 22, self.th["txt2"]).move_to([x0 + w * v, -3.7, 0])) for v in (0.25, 0.5, 0.75, 1.0)])
        self.play(FadeIn(eje), run_time=0.3)
        filas = VGroup()
        for k, (m, nom, a_, b_) in enumerate(datos):
            y = 2.55 - k * 1.42
            sw = placa_metal(m, 0.6, 0.6).move_to([-3.85, y, 0])
            t = self.tx(nom, 24, self.th["txt"], "HEAVY").next_to(sw, RIGHT, buff=0.1)
            if t.get_right()[0] > x0 - 0.05:
                t.scale_to_fit_width(x0 - 0.05 - t.get_left()[0])
            if a_ == b_:
                barra = Rectangle(width=w * b_, height=0.62, stroke_width=0).set_fill("#5B6472", 1).move_to([x0 + w * b_ / 2, y, 0])
                val = self.tx("1,00 (referencia)", 24, "#FFFFFF", "HEAVY").move_to(barra)
                rng = VGroup()
            else:
                barra = Rectangle(width=w * a_, height=0.62, stroke_width=0).set_fill([A, N, N, N][k - 1] if k else A, 1).move_to([x0 + w * a_ / 2, y, 0])
                rng = Rectangle(width=w * (b_ - a_), height=0.62, stroke_color=barra.get_fill_color(), stroke_width=2).set_fill(barra.get_fill_color(), 0.25).move_to([x0 + w * (a_ + b_) / 2, y, 0])
                val = self.tx(f"{a_:.2f}–{b_:.2f}".replace(".", ","), 24, self.th["txt"], "HEAVY").next_to(rng, RIGHT, buff=0.08)
                if val.get_right()[0] > 4.3:
                    val.move_to(rng).set_color(self.th["txt"])
            fila = VGroup(sw, t, barra, rng, val)
            filas.add(fila)
        for k, f in enumerate(filas):
            self.play(FadeIn(f[0]), FadeIn(f[1]), GrowFromEdge(f[2], LEFT), FadeIn(f[3]), FadeIn(f[4]), run_time=0.45)
            self.frac(0.12 if k else 0.06)
        fuente_ = self.tx("Factores típicos de ficha de fabricante · referencia: acero dulce", 20, self.th["txt2"]).move_to([0, -4.3, 0])
        if fuente_.width > 8.3:
            fuente_.scale_to_fit_width(8.3)
        self.play(FadeIn(fuente_), run_time=0.25)
        self.cerrar_voz(0.05)
        self.limpiar(eje, filas, fuente_)

        # ------------------------------------------------ p4 Sn vs Sa
        self.voz("p4")
        self.chip("4", "Sn vs Sa", Rj)
        sen = sensor_m18(1.1)
        sen.shift(np.array([-0.9, 2.4, 0]) - sen.cara.get_right())
        cx = sen.cara.get_right()[0]
        self.play(FadeIn(sen), run_time=0.35)
        mm = 0.45
        y0 = 0.9
        zona_sa = Rectangle(width=6.48 * mm, height=0.6, stroke_width=0).set_fill(V, 0.9).move_to([cx + 6.48 * mm / 2, y0, 0])
        zona_su = Rectangle(width=(9.68 - 6.48) * mm, height=0.6, stroke_color="#B54708", stroke_width=2).set_fill("#FDB022", 0.35).move_to([cx + (6.48 + 9.68) / 2 * mm, y0, 0])
        rayas = VGroup(*[Line([x, y0 - 0.3, 0], [x + 0.3, y0 + 0.3, 0]).set_stroke("#B54708", 1.5) for x in np.arange(cx + 6.48 * mm, cx + 9.4 * mm, 0.22)])
        sn = DashedLine([cx + 8 * mm, 3.2, 0], [cx + 8 * mm, y0 - 0.5, 0]).set_stroke(self.th["txt"], 3)
        tsn = self.tag("Sn = 8 mm (nominal)", "#101828", 26).move_to([1.6, -0.25, 0])
        pl = placa_metal("acero", 0.2, 1.4).move_to([cx + 8 * mm + 0.1, 2.4, 0])
        cota = self.tx("placa de acero de 1 mm", 22, self.th["txt2"], "HEAVY").next_to(pl, LEFT, buff=0.15).shift(UP * 0.95)
        self.frac(0.05)
        self.play(Create(sn), FadeIn(pl), FadeIn(cota), run_time=0.4)
        self.play(FadeIn(tsn), run_time=0.25)
        self.frac(0.25)
        tsa = self.tag("Sa ≤ 0,81 × Sn = 6,5 mm  (asegurada)", V, 26).move_to([0, -1.15, 0])
        self.play(GrowFromEdge(zona_sa, LEFT), FadeIn(tsa), run_time=0.5)
        self.frac(0.15)
        tsu = self.tag("0,81–1,21 Sn: depende de cada sensor", "#B54708", 26).move_to([0, -2.0, 0])
        self.play(FadeIn(zona_su), FadeIn(rayas), FadeIn(tsu), run_time=0.4)
        cs = VGroup(self.card("TOLERANCIA DE FABRICACIÓN", [], "#344054", 7.8, 24), self.card("VOLTAJE 85–110 %", [], "#344054", 7.8, 24),
                    self.card("TEMPERATURA DE OPERACIÓN", [], "#344054", 7.8, 24)).arrange(DOWN, buff=0.14).move_to([0, -4.05, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cs], lag_ratio=0.25), run_time=0.7)
        fu = self.tx("IEC 60947-5-2", 20, self.th["txt2"], "HEAVY").move_to([3.3, -5.55, 0])
        self.play(FadeIn(fu), run_time=0.2)
        self.cerrar_voz(0.05)
        self.limpiar(sen, zona_sa, zona_su, rayas, sn, tsn, tsa, tsu, pl, cota, cs, fu)

        # ------------------------------------------------ p4b blanco estándar
        self.voz("p4b")
        self.chip("5", "BLANCO ESTÁNDAR", A)
        k = 0.19
        cara = VGroup(Circle(radius=9 * k, stroke_color="#7A3E00", stroke_width=3).set_fill("#F79009", 0.9), self.tx("cara Ø 18 mm", 20, "#101828", "HEAVY")).move_to([-2.0, 1.3, 0])
        cuad = VGroup(Square(24 * k, stroke_color="#5B6472", stroke_width=3).set_fill("#8A929C", 0.85),
                      self.tx("24 × 24 mm", 28, "#FFFFFF", "HEAVY")).move_to([2.0, 1.3, 0])
        self.play(FadeIn(cara), run_time=0.3)
        reg = self.card("LADO = EL MAYOR DE:", ["Ø de la cara (18 mm)  ó  3 × Sn (24 mm)"], A, 7.8, 30).move_to([0, -2.0, 0])
        self.play(FadeIn(reg), FadeIn(cuad), run_time=0.45)
        self.frac(0.45)
        peq = VGroup(Square(10 * k, stroke_color="#5B6472", stroke_width=3).set_fill("#8A929C", 0.85), self.tx("10 mm", 22, "#FFFFFF", "HEAVY")).move_to([2.0, 1.3, 0])
        self.play(Transform(cuad, peq), run_time=0.5)
        baja = self.tag("pieza más chica → menos distancia", Rj, 32).move_to([0, -3.7, 0])
        self.play(FadeIn(baja), run_time=0.25)
        self.cerrar_voz(0.05)
        self.limpiar(cara, cuad, reg, baja)

        # ------------------------------------------------ p5 regla de campo
        self.voz("p5")
        self.chip("6", "REGLA DE CAMPO", V)
        f = MathTex(r"S_{montaje}=S_n\times 0{,}81\times k_{material}", color=self.th["txt"]).scale(0.95).move_to([0, 3.0, 0])
        self.play(Write(f), run_time=0.8)
        c = MathTex(r"8\ \text{mm}\times 0{,}81\times 0{,}4\approx 2{,}6\ \text{mm}", color=N).scale(1.15).move_to([0, 1.9, 0])
        self.frac(0.25)
        self.play(Write(c), run_time=0.9)
        sen = sensor_m18(1.25)
        sen.shift(np.array([0.6, -0.3, 0]) - sen.cara.get_right())
        cx = sen.cara.get_right()[0]
        k5 = 0.6
        al = placa_metal("aluminio", 0.28, 2.0).move_to([cx + 2.6 * k5 + 0.14, -0.3, 0])
        cota = VGroup(DoubleArrow([cx, -1.6, 0], [cx + 2.6 * k5, -1.6, 0], buff=0, stroke_width=4, color=N, tip_length=0.18),
                      self.tx("2,6 mm", 30, N, "HEAVY").move_to([cx + 1.3 * k5, -2.05, 0]))
        self.play(FadeIn(sen), FadeIn(al), run_time=0.4)
        self.play(FadeIn(cota), sen.led.animate.set_fill("#FDB022"), run_time=0.4)
        ok = self.card("ASÍ DETECTA SIEMPRE", ["aunque cambien voltaje y temperatura"], V, 7.8, 30).move_to([0, -3.7, 0])
        self.play(FadeIn(ok, shift=UP * 0.15), run_time=0.35)
        self.cerrar_voz(0.05)
        self.limpiar(f, c, sen, al, cota, ok)
        self.quitar_chip()
        self.final("Sn × 0,81 × factor del material")


class PortadaR1(Scene):
    def construct(self):
        from miniaturas import texto_gancho, sticker, logo_esq
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill("#FFFFFF", 1))
        self.add(VGroup(*[Line([x, -8.2, 0], [x, 8.2, 0]) for x in np.arange(-4.5, 4.6, 0.5)], *[Line([-4.6, y, 0], [4.6, y, 0]) for y in np.arange(-8, 8.1, 0.5)]).set_stroke("#EEF2F7", 1.2))
        t = VGroup(T("ASÍ DETECTA METAL", 86, "#101828", "HEAVY"), T("EL SENSOR", 110, "#0057B8", "HEAVY"), T("INDUCTIVO", 120, "#C2410C", "HEAVY")).arrange(DOWN, buff=0.12)
        t.scale_to_fit_width(8.4).move_to([0, 4.6, 0])
        sen = sensor_m18(1.55, led_on=True)
        sen.shift(np.array([0.2, -0.4, 0]) - sen.cara.get_right())
        ondas = campo_frente(sen.cara.get_right() + RIGHT * 0.05, 4, 0.3, 0.3, "#0057B8", 6)
        ac = placa_metal("acero", 0.36, 2.6).move_to([2.6, -0.4, 0])
        al = placa_metal("aluminio", 0.36, 2.6).move_to([3.8, -0.4, 0])
        n1 = T("acero: 8 mm", 46, "#047857", "HEAVY").move_to([1.6, -2.3, 0])
        n2 = T("aluminio: < 4 mm", 40, "#C2410C", "HEAVY").move_to([1.6, 1.5, 0])
        st = sticker("¿POR QUÉ CAMBIA?", "#B42318", size=56, ang=-0.03).move_to([0, -4.4, 0])
        st.scale_to_fit_width(min(st.width, 8.2))
        self.add(sen, ondas, ac, al, n1, n2, t, st)
        logo_esq(self, (3.6, 7.3))

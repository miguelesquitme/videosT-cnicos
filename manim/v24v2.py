"""V24 v2 · Efecto corona. Piezas: lib/svgv24.py → v24v2_eq/. Guion: guion_v24v2.py."""
from reel_v2 import *  # noqa: F401,F403


class V24v2(ReelV2):
    CLAVE = "v24v2"
    GUION_MOD = "guion_v24v2"

    def brillo(self, pts, r=0.28):
        return VGroup(*[VGroup(Circle(radius=r * 1.8, stroke_width=0).set_fill("#6FB7FF", 0.3),
                               Circle(radius=r * 0.7, stroke_width=0).set_fill("#D7ECFF", 0.9)).move_to(p) for p in pts])

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"
        AZ = "#6FB7FF"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        cielo = Rectangle(width=9.2, height=12.2, stroke_width=0).set_fill("#0B1530", 0).move_to([0, -1.8, 0]).set_z_index(-60)
        to = Pieza("torre", alto=10.6).move_to([0, -1.9, 0])
        self.play(FadeIn(cielo), FadeIn(to), run_time=0.5)
        self.en("noche")
        self.play(cielo.animate.set_fill(opacity=0.9), run_time=0.8)
        self.en("chisporroteo")
        br = self.brillo([to.p(f"fase{k}") for k in range(3)], 0.22)
        self.sfx("corona", -10)
        self.play(FadeIn(br), run_time=0.3)
        self.play(br.animate.set_opacity(0.4), run_time=0.25)
        self.play(br.animate.set_opacity(1), run_time=0.25)
        self.en("rompiendo")
        n1 = self.nota("el aire alrededor del cable se rompe", AZ, [0, 3.2, 0], 24)
        self.play(FadeIn(n1), run_time=0.3)
        self.en("corona")
        ca = self.card("EFECTO CORONA", ["ionización del aire junto al conductor"], AZ, 7.8, 30).move_to([0, 2.7, 0])
        self.play(FadeOut(n1), FadeIn(ca, shift=DOWN * 0.15), run_time=0.4)
        self.cerrar(to, br, ca, cielo)

        # ------------------------------------------------------------ p1 el conductor
        self.voz("p1")
        self.chip("1", "EL CONDUCTOR", C)
        ac = Pieza("acsr", 6.4).move_to([0, -0.4, 0])
        self.play(FadeIn(ac, scale=0.9), run_time=0.5)
        self.en("ACSR|drake")
        t0 = self.nota("ACSR 795 kcmil «Drake» 26/7", C, [0, 3.2, 0], 26)
        self.play(FadeIn(t0), run_time=0.3)
        self.en("7|siete")
        a1 = self.flecha("7 hilos de acero: resistencia mecánica", ac.p("acero"), [0, -4.6, 0], GR, 22)
        self.play(FadeIn(a1), run_time=0.35)
        self.en("26|veintiséis")
        a2 = self.flecha("26 hilos de aluminio: corriente", ac.p("aluminio"), [1.5, 2.5, 0], Am, 22)
        self.play(FadeIn(a2), run_time=0.35)
        self.en("28|veintiocho")
        y = ac.img.get_bottom()[1] - 0.25
        dm = VGroup(DoubleArrow([ac.img.get_left()[0] + 0.1, y, 0], [ac.img.get_right()[0] - 0.1, y, 0], buff=0, color=C, stroke_width=5),
                    T("Ø 28,14 mm", 28, C, "HEAVY").move_to([0, y - 0.45, 0]))
        self.play(FadeOut(a1), Create(dm), run_time=0.4)
        self.en("forro")
        nf = self.nota("conductor desnudo: sin forro", Rr, [0, -6.3, 0], 24)
        self.play(FadeIn(nf), run_time=0.3)
        self.cerrar(ac, t0, a2, dm, nf)

        # ------------------------------------------------------------ p2 el campo
        self.voz("p2")
        self.chip("2", "EL CAMPO EN LA SUPERFICIE", Am)
        co = Pieza("cond", 8.4).move_to([0, 2.0, 0])
        self.play(FadeIn(co), run_time=0.4)
        self.en("superficie")
        ax, g = self.ejes([0.3, -2.6, 0], 7.4, 3.6, (14, 60), (0, 40), "distancia al centro (mm)", "kV/cm")
        curva = ax.plot(lambda r: 36 * 14.07 / r, x_range=[14.07, 60], color=Am, stroke_width=6)
        self.play(Create(ax), FadeIn(g), Create(curva), run_time=0.9)
        sup = Dot(ax.c2p(14.07, 36), radius=0.11, color=Rr)
        ns = self.nota("máximo en la superficie", Rr, ax.c2p(34, 34), 22)
        self.play(FadeIn(sup, scale=1.5), FadeIn(ns), run_time=0.3)
        self.en("30|treinta")
        lim = DashedLine(ax.c2p(14, 30), ax.c2p(60, 30), dash_length=0.12).set_stroke(Rr, 4)
        nl = self.nota("≈ 30 kV/cm: rigidez del aire seco", Rr, ax.c2p(37, 24), 22)
        self.play(Create(lim), FadeOut(ns), FadeIn(nl), run_time=0.4)
        self.en("ioniza")
        halo = Rectangle(width=co.img.width - 0.2, height=1.0, stroke_width=0).set_fill(AZ, 0.0).move_to(co.p("conductor"))
        self.add(halo)
        self.sfx("corona", -12)
        self.play(halo.animate.set_fill(AZ, 0.35), run_time=0.4)
        self.en("azul")
        self.play(halo.animate.set_fill(AZ, 0.15), run_time=0.2)
        self.play(halo.animate.set_fill(AZ, 0.4), run_time=0.2)
        self.cerrar(co, ax, g, curva, sup, lim, nl, halo)

        # ------------------------------------------------------------ p3 la lluvia
        self.voz("p3")
        self.chip("3", "LLUVIA Y NEBLINA", C)
        cg = Pieza("cond_gotas", 8.4).move_to([0, 1.5, 0])
        self.play(FadeIn(cg), run_time=0.4)
        self.en("gotas")
        ag = self.aro(cg.p("gota"), 0.35, AZ)
        self.play(Create(ag), run_time=0.3)
        self.en("puntas")
        cc = Pieza("cond_corona", 8.4)
        self.sfx("corona", -8)
        self.poner(cc, cg)
        np_ = self.nota("en cada gota el campo se concentra", AZ, [0, 3.2, 0], 24)
        self.play(FadeIn(np_), run_time=0.3)
        self.en("ruido")
        nr = self.nota("más ruido: 1 a 20 kHz", Am, [0, -1.4, 0], 26)
        self.play(FadeIn(nr), run_time=0.3)
        self.en("ozono|osono")
        oz = self.card("OZONO (O₃) Y ÓXIDOS DE NITRÓGENO", ["el aire ionizado reacciona"], G, 7.8, 26).move_to([0, -3.1, 0])
        self.play(FadeIn(oz, shift=UP * 0.15), run_time=0.35)
        self.en("1|uno")
        pe = self.card("PÉRDIDAS < 1 %", ["en una línea bien diseñada"], Am, 7.8, 28).move_to([0, -5.2, 0])
        self.play(FadeIn(pe, shift=UP * 0.15), run_time=0.35)
        self.cerrar(cc, ag, np_, nr, oz, pe)

        # ------------------------------------------------------------ p4 el haz
        self.voz("p4")
        self.chip("4", "CONDUCTORES EN HAZ", G)
        uno = Pieza("acsr", 2.2).move_to([0, 1.2, 0])
        t1 = self.nota("1 conductor por fase", GR, [0, 3.1, 0], 24)
        self.play(FadeIn(uno), FadeIn(t1), run_time=0.4)
        self.en("dos")
        h = Group(Pieza("acsr", 2.2).move_to([-1.9, -2.6, 0]), Pieza("acsr", 2.2).move_to([1.9, -2.6, 0]))
        self.play(FadeIn(h[0]), FadeIn(h[1]), run_time=0.35)
        self.en("espaciadores")
        sp = Rectangle(width=1.6, height=0.32, stroke_width=0).set_fill("#9DA4AB", 1).move_to([0, -2.6, 0])
        ns = self.nota("espaciador", GR, [0, -1.9, 0], 22)
        self.play(FadeIn(sp), FadeIn(ns), run_time=0.3)
        self.en("grueso")
        eq = DashedVMobject(Circle(radius=3.4, color=G, stroke_width=5), num_dashes=40).move_to([0, -2.6, 0])
        ne = self.nota("se comporta como un conductor más grueso", G, [0, -6.4, 0], 22)
        self.play(Create(eq), FadeIn(ne), run_time=0.5)
        self.en("baja")
        nb = self.card("CAMPO EN LA SUPERFICIE ↓", ["menos corona y menos ruido"], G, 7.8, 28).move_to([0, 2.6, 0])
        self.play(FadeOut(t1), FadeOut(uno), FadeIn(nb, shift=DOWN * 0.15), run_time=0.4)
        self.cerrar(h, sp, ns, eq, ne, nb)

        # ------------------------------------------------------------ p5 aisladores y anillo
        self.voz("p5")
        self.chip("5", "AISLADORES Y ANILLO", Vi)
        cad = Pieza("cadena_corona", alto=10.6).move_to([-1.6, -1.8, 0])
        self.play(FadeIn(cad), run_time=0.45)
        self.en("disco")
        a1 = self.flecha("vidrio templado · Ø 255 mm", cad.p("disco"), [2.0, 2.6, 0], C, 22)
        self.play(FadeIn(a1), run_time=0.35)
        self.en("bola")
        a2 = self.flecha("bola y casquillo · cada 146 mm", cad.p("disco2"), [2.0, 1.4, 0], Am, 22)
        self.play(FadeIn(a2), run_time=0.35)
        self.en("aro")
        cr = Pieza("cadena", alto=10.6)
        self.poner(cr, cad)
        a3 = self.flecha("anillo anticorona (aluminio)", cr.p("anillo"), [2.2, -3.4, 0], G, 22)
        self.play(FadeIn(a3), run_time=0.35)
        self.en("reparte")
        n4 = self.nota("reparte el campo: sin brillo en los herrajes", G, [0.6, -6.6, 0], 22)
        self.play(FadeIn(n4), run_time=0.3)
        self.cerrar(cr, a1, a2, a3, n4)

        # ------------------------------------------------------------ p6 seguridad
        self.voz("p6")
        self.chip("6", "SEGURIDAD", Rr)
        to = Pieza("torre", alto=8.0).move_to([0, -1.2, 0])
        self.play(FadeIn(to), run_time=0.4)
        self.en("energizada")
        av = self.card("LÍNEA ENERGIZADA", ["el sonido es una advertencia"], Rr, 7.8, 30).move_to([0, 2.9, 0])
        self.play(FadeIn(av, shift=DOWN * 0.15), run_time=0.35)
        self.en("varillas")
        nn = self.nota("nunca: varillas · escaleras · barriletes", Am, [0, -6.0, 0], 24)
        self.play(FadeIn(nn), run_time=0.3)
        self.cerrar(to, av, nn)
        self.quitar_chip()
        self.final("Corona: el aire se ioniza a ≈ 30 kV/cm junto al conductor")


class PortadaV24v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v24v2_eq"
        cc = Pieza("cond_corona", 8.6).move_to([0, -4.6, 0])
        ac = Pieza("acsr", 5.6)
        portada_v(self, ["¿POR QUÉ", "SUENAN LOS", "CABLES?"], ac, "EFECTO CORONA", extra=cc)

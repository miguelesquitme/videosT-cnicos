"""V25 v2 · ¿Cómo funciona un FUSIBLE? Piezas: lib/svgv25.py → v25v2_eq/. Guion: guion_v25v2.py."""
from reel_v2 import *  # noqa: F401,F403

XF, YF, HF = -2.55, -1.55, 9.0     # posición y alto del fusible


class V25v2(ReelV2):
    CLAVE = "v25v2"
    GUION_MOD = "guion_v25v2"

    def fus(self, nombre):
        return Pieza(nombre, alto=HF).move_to([XF, YF, 0])

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"
        XR = 1.75   # columna derecha

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        fu = Pieza("fusible", alto=HF).move_to([0, YF, 0])
        self.play(FadeIn(fu, scale=0.95), run_time=0.5)
        self.en("derrite")
        n1 = self.nota("metal que se funde a propósito", Am, [0, 3.2, 0], 26)
        self.play(FadeIn(n1), run_time=0.3)
        self.en("cuarto")
        n2 = self.nota("abre un cortocircuito en < ¼ de ciclo", Rr, [0, -6.8, 0], 26)
        self.play(FadeIn(n2), run_time=0.3)
        self.en("abrir")
        self.play(fu.animate.move_to([XF, YF, 0]), FadeOut(n1), FadeOut(n2), run_time=0.5)
        self.cerrar(fu)

        # ------------------------------------------------------------ p1 por fuera
        self.voz("p1")
        self.chip("1", "POR FUERA", C)
        fu = self.fus("fusible")
        self.play(FadeIn(fu), run_time=0.35)
        self.en("10|diez")
        top, bot = fu.mm(0, 0), fu.mm(0, 38)
        x = fu.img.get_left()[0] - 0.35
        d1 = VGroup(DoubleArrow([x, top[1], 0], [x, bot[1], 0], buff=0, color=C, stroke_width=5),
                    T("38 mm", 26, C, "HEAVY").rotate(PI / 2).move_to([x - 0.35, YF, 0]))
        y = fu.img.get_top()[1] + 0.25
        d2 = VGroup(DoubleArrow([fu.img.get_left()[0], y, 0], [fu.img.get_right()[0], y, 0], buff=0, color=C, stroke_width=5),
                    T("Ø 10,3", 24, C, "HEAVY").next_to([XF, y, 0], UP, buff=0.08))
        self.play(Create(d1), Create(d2), run_time=0.5)
        self.en("GG|clase")
        g1 = self.nota("clase gG · IEC 60269", Am, [XR, 2.4, 0], 26)
        self.play(FadeIn(g1), run_time=0.3)
        self.en("cerámica")
        a1 = self.flecha("cuerpo de cerámica", fu.p("cuerpo") + RIGHT * 0.9 + UP * 1.2, [XR, 1.0, 0], C, 24)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("casquillos")
        a2 = self.flecha("casquillo plateado: contacto", fu.p("casq_sup"), [XR, 3.2, 0], GR, 22)
        a3 = Line(a2[2].get_bottom() + DOWN * 0.02, fu.p("casq_inf")).set_stroke(GR, 4)
        self.play(FadeIn(a2), Create(a3), FadeOut(g1), run_time=0.35)
        self.en("16|impreso")
        ar = self.recuadro(fu.p("texto"), 1.7, 3.6, Rr)
        n3 = self.card("16 A · 500 V~", ["corriente y tensión nominal"], Rr, 4.9, 26).move_to([XR, -2.2, 0])
        self.play(Create(ar), FadeIn(n3), run_time=0.4)
        self.cerrar(fu, d1, d2, a1, a2, a3, ar, n3)

        # ------------------------------------------------------------ p2 por dentro
        self.voz("p2")
        self.chip("2", "POR DENTRO", Am)
        co = self.fus("corte")
        self.play(FadeIn(co), run_time=0.4)
        self.en("lámina")
        a1 = self.flecha("lámina metálica", co.p("lamina"), [XR, 2.6, 0], C, 24)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("cuellos")
        aros = VGroup(*[self.aro(co.p(f"cuello{i}"), 0.3, Am) for i in range(4)])
        a2 = self.nota("cuellos: partes angostas", Am, [XR, 1.5, 0], 24)
        self.play(Create(aros), FadeIn(a2), run_time=0.4)
        self.en("arena")
        a3 = self.flecha("arena", co.p("arena"), [XR, 0.3, 0], "#C9BC9A", 24)
        self.play(FadeIn(a3), run_time=0.3)
        self.en("sección")
        k = self.card("SECCIÓN MENOR", ["→ resistencia mayor", "→ se calienta primero"], Rr, 4.9, 26).move_to([XR, -2.6, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.en("calienta")
        cc = self.fus("corte_cal")
        self.poner(cc, co)
        self.cerrar(cc, a1, aros, a2, a3, k)

        # ------------------------------------------------------------ p3 sobrecarga
        self.voz("p3")
        self.chip("3", "SOBRECARGA", Am)
        cc = self.fus("corte_cal")
        self.play(FadeIn(cc), run_time=0.35)
        self.en("abre")
        so = self.fus("corte_sob")
        self.sfx("pop", -10)
        self.poner(so, cc)
        a1 = self.flecha("un cuello se funde", so.p("cuello2"), [XR, 2.0, 0], Rr, 24)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("segundos")
        t1 = self.nota("segundos o minutos", Am, [XR, 0.9, 0], 26)
        self.play(FadeIn(t1), run_time=0.3)
        self.en("cuadrado")
        k = self.card("I² · t", ["energía térmica:", "más corriente → abre más rápido"], C, 4.9, 26).move_to([XR, -1.6, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.cerrar(so, a1, t1, k)

        # ------------------------------------------------------------ p4 cortocircuito
        self.voz("p4")
        self.chip("4", "CORTOCIRCUITO", Rr)
        co = self.fus("corte")
        self.play(FadeIn(co), run_time=0.3)
        self.en("varios")
        cc = self.fus("corte_cc")
        self.poner(cc, co)
        self.en("arcos")
        ar = self.fus("arcos")
        self.sfx("disparo", -8)
        self.play(FadeIn(ar), run_time=0.15)
        self.play(ar.animate.set_opacity(0.3), run_time=0.15)
        self.play(ar.animate.set_opacity(1), run_time=0.15)
        self.en("arena")
        self.play(FadeOut(ar), run_time=0.3)
        self.en("fulgurita")
        a1 = self.flecha("fulgurita: arena fundida", cc.p("cuello1") + RIGHT * 0.4, [XR, 2.7, 0], "#C9BC9A", 22)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("cero")
        ax, g = self.ejes([XR + 0.1, -1.4, 0], 4.6, 3.0, (0, 8.33), (-0.2, 1.1), "ms", "A")
        pros = ax.plot(lambda t: np.sin(PI * t / 8.33), x_range=[0, 8.33], color=GR, stroke_width=4)
        pros = DashedVMobject(pros, num_dashes=30)
        lim = ax.plot(lambda t: (np.sin(PI * t / 8.33) if t < 1.6 else np.sin(PI * 1.6 / 8.33) * max(0, 1 - (t - 1.6) / 0.9)),
                      x_range=[0, 2.5, 0.02], color=Rr, stroke_width=6)
        np_ = T("sin fusible", 20, GR, "BOLD").move_to(ax.c2p(5.6, 1.08))
        nl = T("con fusible", 20, Rr, "BOLD").move_to(ax.c2p(2.0, 0.65))
        self.play(Create(ax), FadeIn(g), Create(pros), FadeIn(np_), run_time=0.6)
        self.play(Create(lim), FadeIn(nl), run_time=0.5)
        self.en("pico")
        q = self.nota("abre en < ¼ de ciclo", Rr, [XR, -3.6, 0], 24)
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar(cc, a1, ax, g, pros, lim, np_, nl, q)

        # ------------------------------------------------------------ p5 gG / aM
        self.voz("p5")
        self.chip("5", "gG O aM", Vi)
        self.en("GG|G.")
        k1 = self.card("gG · uso general", ["sobrecarga + cortocircuito", "protege cables"], G, 7.8, 30).move_to([0, 1.8, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.4)
        self.en("A,|AM|A")
        k2 = self.card("aM · motores", ["solo cortocircuito", "+ relé térmico para la sobrecarga"], Am, 7.8, 30).move_to([0, -1.0, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.4)
        self.en("motores")
        self.play(Indicate(k2, scale_factor=1.04, color=Am), run_time=0.5)
        self.cerrar(k1, k2)

        # ------------------------------------------------------------ p6 el error
        self.voz("p6")
        self.chip("6", "EL ERROR MÁS PELIGROSO", Rr)
        self.en("alambre")
        pu = Pieza("puenteado", alto=HF).move_to([XF + 0.3, YF, 0])
        xx = VGroup(Line(UL, DR), Line(UR, DL)).scale(1.2).set_stroke(Rr, 12).move_to(pu)
        self.play(FadeIn(pu), run_time=0.35)
        self.play(Create(xx), run_time=0.3)
        self.en("cable")
        k = self.card("PROTEGE AL CABLE", ["no debe pasar la capacidad", "del conductor"], C, 4.9, 24).move_to([XR, 1.8, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.en("aislamiento")
        k2 = self.nota("se funde el aislamiento en la pared", Rr, [XR, -0.6, 0], 22)
        self.play(FadeIn(k2), run_time=0.3)
        self.en("igual")
        fu = Pieza("fusible", alto=HF).move_to([XF, YF, 0])
        ok = self.nota("✓ uno igual: 16 A gG", G, [XR, -2.4, 0], 28)
        self.play(FadeOut(pu), FadeOut(xx), FadeIn(fu), FadeIn(ok, scale=1.2), run_time=0.45)
        self.cerrar(fu, k, k2, ok)
        self.quitar_chip()
        self.final("Cuellos + arena: abre en < ¼ de ciclo ante un cortocircuito")


class PortadaV25v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v25v2_eq"
        a = Pieza("fusible", alto=7.6).move_to([-1.6, -0.9, 0])
        b = Pieza("corte_cc", alto=7.6).move_to([1.6, -0.9, 0])
        portada_v(self, ["¿QUÉ HAY", "DENTRO DE UN", "FUSIBLE?"], Group(a, b), "ARENA Y CUELLOS")

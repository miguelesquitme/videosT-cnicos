"""V26 v2 · Factor de potencia. Piezas: lib/svgv26.py → v26v2_eq/. Guion: guion_v26v2.py."""
from reel_v2 import *  # noqa: F401,F403


class V26v2(ReelV2):
    CLAVE = "v26v2"
    GUION_MOD = "guion_v26v2"

    def barra(self, x, y0, valor, k, color, texto):
        b = Rectangle(width=1.3, height=valor * k, stroke_width=0).set_fill(color, 1).move_to([x, y0, 0], aligned_edge=DOWN)
        t = T(texto, 28, color, "HEAVY").next_to(b, UP, buff=0.12)
        return b, t

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        m1 = Pieza("motor", 4.6).move_to([-1.9, 1.4, 0])
        m2 = Pieza("motor", 4.6).move_to([-1.9, -2.6, 0])
        f1 = T("FP 0,95", 28, G, "HEAVY").next_to(m1, DOWN, buff=0.1)
        f2 = T("FP 0,70", 28, Rr, "HEAVY").next_to(m2, DOWN, buff=0.1)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.5)
        self.en("pide")
        b1, t1 = self.barra(2.6, 0.2, 12.7, 0.15, G, "12,7 A")
        b2, t2 = self.barra(2.6, -3.8, 17.2, 0.15, Rr, "17,2 A")
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(t1), FadeIn(t2), run_time=0.6)
        self.en("36|treinta")
        n = self.nota("+36 % de corriente, mismo trabajo", Rr, [0, -6.3, 0], 26)
        self.play(FadeIn(n, scale=1.15), run_time=0.3)
        self.en("factor")
        self.play(FadeIn(f1), FadeIn(f2), run_time=0.3)
        self.cerrar(m1, m2, f1, f2, b1, b2, t1, t2, n)

        # ------------------------------------------------------------ p1 dos potencias
        self.voz("p1")
        self.chip("1", "DOS POTENCIAS", C)
        mo = Pieza("motor", 7.6).move_to([0.3, 0.2, 0])
        self.play(FadeIn(mo), run_time=0.4)
        self.en("activa")
        eje = mo.mm(6, 92)
        a1 = self.flecha("ACTIVA (kW): mueve el eje", eje, [-1.2, 3.1, 0], G, 26)
        g1 = Arc(radius=0.55, start_angle=PI * 0.9, angle=-PI * 1.3, color=G, stroke_width=7).add_tip(tip_length=0.25).move_arc_center_to(eje)
        self.play(FadeIn(a1), Create(g1), run_time=0.4)
        self.en("reactiva")
        red = T("RED", 30, Vi, "HEAVY").move_to([-3.2, -4.3, 0])
        mt = T("MOTOR", 30, Vi, "HEAVY").move_to([3.0, -4.3, 0])
        fl = DoubleArrow([-2.5, -4.3, 0], [2.0, -4.3, 0], buff=0, color=Vi, stroke_width=7)
        nr = self.nota("REACTIVA (kvar): campo magnético", Vi, [0, -3.2, 0], 24)
        self.play(FadeIn(red), FadeIn(mt), GrowFromCenter(fl), FadeIn(nr), run_time=0.45)
        self.en("viene")
        for _ in range(2):
            self.play(fl.animate.shift(RIGHT * 0.4), run_time=0.3)
            self.play(fl.animate.shift(LEFT * 0.4), run_time=0.3)
        ns = self.nota("no hace trabajo", GR, [0, -5.4, 0], 24)
        self.play(FadeIn(ns), run_time=0.25)
        self.cerrar(mo, a1, g1, red, mt, fl, nr, ns)

        # ------------------------------------------------------------ p2 triángulo
        self.voz("p2")
        self.chip("2", "EL TRIÁNGULO", Am)
        k = 0.05
        o = np.array([-3.0, -2.6, 0])
        A, B = o + RIGHT * 100 * k, o + RIGHT * 100 * k + UP * 75 * k
        self.en("triángulo")
        P = Arrow(o, A, buff=0, color=G, stroke_width=9, max_tip_length_to_length_ratio=0.06)
        Q = Arrow(A, B, buff=0, color=Vi, stroke_width=9, max_tip_length_to_length_ratio=0.08)
        tp = T("P = 100 kW", 28, G, "HEAVY").next_to(P, DOWN, buff=0.15)
        tq = T("Q = 75 kvar", 28, Vi, "HEAVY").next_to(Q, RIGHT, buff=0.15)
        self.play(GrowArrow(P), FadeIn(tp), run_time=0.4)
        self.play(GrowArrow(Q), FadeIn(tq), run_time=0.4)
        self.en("hipotenusa")
        Sv = Arrow(o, B, buff=0, color=Am, stroke_width=9, max_tip_length_to_length_ratio=0.05)
        ts = T("S = 125 kVA", 28, Am, "HEAVY").next_to(Sv.get_center(), UL, buff=0.15)
        self.play(GrowArrow(Sv), FadeIn(ts), run_time=0.45)
        self.en("entregar")
        nn = self.nota("lo que la red entrega", Am, [0, 3.2, 0], 24)
        self.play(FadeIn(nn), run_time=0.25)
        self.en("activa")
        fp = self.card("FP = P / S", ["activa ÷ aparente"], C, 7.8, 30).move_to([0, 2.3, 0])
        self.play(FadeOut(nn), FadeIn(fp, shift=DOWN * 0.15), run_time=0.35)
        self.en("100|cien")
        r = self.card("100 kW ÷ 125 kVA = 0,80", [], C, 7.8, 32).move_to([0, -5.4, 0])
        self.play(FadeIn(r, shift=UP * 0.15), run_time=0.35)
        self.cerrar(P, Q, Sv, tp, tq, ts, fp, r)

        # ------------------------------------------------------------ p3 la corriente
        self.voz("p3")
        self.chip("3", "LA CORRIENTE", Rr)
        self.en("corriente")
        f = self.card("I = P / (√3 · V · FP)", ["trifásico"], C, 7.8, 32).move_to([0, 2.5, 0])
        self.play(FadeIn(f, shift=DOWN * 0.15), run_time=0.4)
        self.en("10|diez")
        d = self.nota("10 kW · 480 V", GR, [0, 1.0, 0], 28)
        self.play(FadeIn(d), run_time=0.25)
        self.en("95|0")
        b1, t1 = self.barra(-1.6, -4.6, 12.7, 0.25, G, "12,7 A")
        l1 = T("FP 0,95", 26, G, "HEAVY").next_to(b1, DOWN, buff=0.12)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(t1), FadeIn(l1), run_time=0.45)
        self.en("70")
        b2, t2 = self.barra(1.6, -4.6, 17.2, 0.25, Rr, "17,2 A")
        l2 = T("FP 0,70", 26, Rr, "HEAVY").next_to(b2, DOWN, buff=0.12)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(t2), FadeIn(l2), run_time=0.45)
        self.en("36|treinta")
        mas = self.nota("+36 %", Rr, [3.4, -0.6, 0], 34)
        self.play(FadeIn(mas, scale=1.2), run_time=0.3)
        self.cerrar(f, d, b1, t1, l1, b2, t2, l2, mas)

        # ------------------------------------------------------------ p4 el costo
        self.voz("p4")
        self.chip("4", "EL COSTO", Am)
        self.en("calor")
        k1 = self.card("MÁS CALOR", ["pérdidas I² · R en cables", "y transformadores"], Rr, 7.8, 30).move_to([0, 2.2, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("recargos")
        k2 = self.card("RECARGOS", ["la distribuidora cobra el bajo FP", "a la industria"], Am, 7.8, 30).move_to([0, -0.4, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.en("meta")
        k3 = self.card("META USUAL: FP 0,95", [], G, 7.8, 34).move_to([0, -2.8, 0])
        self.play(FadeIn(k3, shift=UP * 0.15), run_time=0.35)
        self.cerrar(k1, k2, k3)

        # ------------------------------------------------------------ p5 el capacitor
        self.voz("p5")
        self.chip("5", "EL CAPACITOR", G)
        ca = Pieza("cap", alto=9.4).move_to([-2.3, -1.6, 0])
        self.play(FadeIn(ca), run_time=0.4)
        self.en("dentro")
        cc = Pieza("cap_corte", alto=8.0).move_to([1.9, -2.3, 0])
        self.play(FadeIn(cc, shift=LEFT * 0.3), run_time=0.4)
        self.en("polipropileno")
        a1 = self.flecha("polipropileno metalizado", cc.p("bobina0"), [1.6, 2.9, 0], C, 22)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("resina")
        a2 = self.aro(cc.p("resina"), 0.3, "#C9B98A")
        n2 = self.nota("resina", "#8C7A4A", [1.9, -6.8, 0], 22)
        self.play(Create(a2), FadeIn(n2), run_time=0.3)
        self.en("aluminio")
        a3 = self.flecha("bote de aluminio", ca.p("ranura"), [-1.8, 3.4, 0], GR, 22)
        self.play(FadeIn(a3), run_time=0.3)
        self.en("reactiva")
        k = self.card("ENTREGA LOS kvar", ["junto al motor"], G, 7.8, 28).move_to([0, -5.5, 0])
        self.play(FadeOut(n2), FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.cerrar(ca, cc, a1, a2, a3, k)

        # ------------------------------------------------------------ p6 seguridad
        self.voz("p6")
        self.chip("6", "SEGURIDAD", Rr)
        ca = Pieza("cap", alto=9.6).move_to([-2.1, -1.6, 0])
        self.play(FadeIn(ca), run_time=0.4)
        self.en("resistencias")
        a1 = self.flecha("resistencias de descarga", ca.p("resistencia"), [1.9, 2.6, 0], C, 22)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("50|cincuenta")
        k1 = self.card("< 50 V EN 1 MINUTO", ["al desconectarlo (NEC)"], C, 4.6, 24).move_to([2.0, 1.2, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("infla")
        ci = Pieza("cap_inflado", alto=9.6)
        self.poner(ci, ca)
        self.sfx("pop", -8)
        self.en("desconectador")
        k2 = self.card("DESCONECTADOR", ["por sobrepresión:", "lo saca del circuito"], Am, 4.6, 24).move_to([2.0, -1.3, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.en("toques")
        k3 = self.card("NO LO TOQUES", ["cámbialo desenergizado"], Rr, 4.6, 24).move_to([2.0, -3.8, 0])
        self.play(FadeIn(k3, shift=UP * 0.15), run_time=0.35)
        self.cerrar(ci, a1, k1, k2, k3)
        self.quitar_chip()
        self.final("FP = kW ÷ kVA · el capacitor entrega los kvar junto al motor")


class PortadaV26v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v26v2_eq"
        ca = Pieza("cap", alto=7.6).move_to([-1.8, -1.0, 0])
        cc = Pieza("cap_corte", alto=6.6).move_to([1.9, -1.4, 0])
        portada_v(self, ["¿POR QUÉ", "PIDE MÁS", "CORRIENTE?"], Group(ca, cc), "FACTOR DE POTENCIA")

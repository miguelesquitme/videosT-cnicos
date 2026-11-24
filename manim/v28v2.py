"""V28 v2 · 120 V a 240 V. Piezas: lib/svgv28.py → v28v2_eq/. Guion: guion_v28v2.py."""
from reel_v2 import *  # noqa: F401,F403


class V28v2(ReelV2):
    CLAVE = "v28v2"
    GUION_MOD = "guion_v28v2"

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        et = Pieza("etq", 5.4).move_to([-1.3, 2.2, 0])
        tm = Pieza("t615", alto=4.2).move_to([2.8, 1.6, 0])
        self.play(FadeIn(et), run_time=0.4)
        self.en("240")
        self.play(FadeIn(tm), run_time=0.35)
        self.en("quemado")
        r2 = Pieza("res_240", 8.6).move_to([0, -3.4, 0])
        self.sfx("pop", -10)
        self.play(FadeIn(r2), run_time=0.4)
        self.en("doble")
        n = self.nota("¿solo el doble?", Am, [0, -6.0, 0], 30)
        self.play(FadeIn(n, scale=1.2), run_time=0.3)
        self.cerrar(et, tm, r2, n)

        # ------------------------------------------------------------ p1 la resistencia
        self.voz("p1")
        self.chip("1", "POR DENTRO", C)
        rf = Pieza("res_frio", 8.6).move_to([0, -0.4, 0])
        self.play(FadeIn(rf), run_time=0.4)
        self.en("níquel|alambre")
        a1 = self.flecha("espiral de níquel cromo (80/20)", rf.p("espiral"), [0, 3.1, 0], Am, 24)
        self.play(FadeIn(a1), run_time=0.35)
        self.en("óxido")
        a2 = self.flecha("óxido de magnesio compactado", rf.p("mgo"), [0.8, -3.4, 0], "#C9C4B8", 24)
        self.play(FadeIn(a2), run_time=0.35)
        self.en("acero")
        a3 = self.flecha("tubo de acero Ø 8 mm", rf.p("vaina"), [1.6, 2.0, 0], GR, 24)
        self.play(FadeIn(a3), run_time=0.35)
        self.en("aísla")
        k = self.card("EL MgO AÍSLA", ["pero deja pasar el calor"], C, 7.8, 28).move_to([0, -5.3, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.cerrar(rf, a1, a2, a3, k)

        # ------------------------------------------------------------ p2 la resistencia en ohmios
        self.voz("p2")
        self.chip("2", "SU RESISTENCIA", Am)
        et = Pieza("etq", 6.0).move_to([0, 2.0, 0])
        self.play(FadeIn(et), run_time=0.4)
        self.en("ohm")
        f = self.card("R = V² / P", ["120² ÷ 1000"], C, 7.8, 32).move_to([0, -0.9, 0])
        self.play(FadeIn(f, shift=UP * 0.15), run_time=0.35)
        self.en("14|catorce")
        r = self.card("R = 14,4 Ω", [], Am, 7.8, 40).move_to([0, -2.9, 0])
        self.play(FadeIn(r, scale=1.1), run_time=0.35)
        self.en("cambia")
        r1 = Pieza("res_120", 8.6).move_to([0, -5.4, 0])
        self.play(FadeIn(r1), run_time=0.35)
        self.cerrar(et, f, r, r1)

        # ------------------------------------------------------------ p3 a 240 V
        self.voz("p3")
        self.chip("3", "A 240 V", Rr)
        r1 = Pieza("res_120", 8.6).move_to([0, 2.4, 0])
        self.play(FadeIn(r1), run_time=0.35)
        self.en("duplica")
        k1 = self.card("I = 240 ÷ 14,4 = 16,7 A", ["el doble de corriente"], Am, 7.8, 28).move_to([0, 0.2, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("4000|cuatro")
        ax_y0 = -5.6
        b1 = Rectangle(width=1.4, height=1000 * 0.00075, stroke_width=0).set_fill(G, 1).move_to([-1.6, ax_y0, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.4, height=4000 * 0.00075, stroke_width=0).set_fill(Rr, 1).move_to([1.6, ax_y0, 0], aligned_edge=DOWN)
        t1 = T("120 V: 1000 W", 24, G, "HEAVY").next_to(b1, UP, buff=0.1)
        t2 = T("240 V: 4000 W", 24, Rr, "HEAVY").next_to(b2, UP, buff=0.1)
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(t1), FadeIn(t2), run_time=0.5)
        self.en("cuatro|4")
        nn = self.nota("2× voltaje → 4× potencia", Rr, [0, -6.4, 0], 26)
        self.play(FadeIn(nn, scale=1.15), run_time=0.3)
        self.en("amarillo")
        r2 = Pieza("res_240", 8.6)
        self.poner(r2, r1)
        self.en("funde")
        a = self.aro(r2.p("falla"), 0.35, Rr)
        self.sfx("pop", -8)
        self.play(Create(a), run_time=0.3)
        self.cerrar(r2, a, k1, b1, b2, t1, t2, nn)

        # ------------------------------------------------------------ p4 al revés
        self.voz("p4")
        self.chip("4", "AL REVÉS", C)
        self.en("calentador")
        rf = Pieza("res_frio", 8.6).move_to([0, 2.2, 0])
        self.play(FadeIn(rf), run_time=0.35)
        self.en("cuarta")
        k = self.card("240 V NOMINAL EN 120 V", ["P = (120/240)² = ¼ de la potencia"], C, 7.8, 28).move_to([0, -0.6, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.en("calienta")
        n = self.nota("no se quema, pero casi no calienta", GR, [0, -2.4, 0], 26)
        self.play(FadeIn(n), run_time=0.3)
        self.cerrar(rf, k, n)

        # ------------------------------------------------------------ p5 tomacorrientes
        self.voz("p5")
        self.chip("5", "FORMAS DISTINTAS", G)
        a = Pieza("t515", alto=6.0).move_to([-2.1, -0.6, 0])
        b = Pieza("t615", alto=6.0).move_to([2.1, -0.6, 0])
        self.play(FadeIn(a), FadeIn(b), run_time=0.4)
        self.en("515|cinco")
        a1 = self.aro(a.p("ranuras"), 0.75, G)
        n1 = self.nota("verticales · 125 V", G, [-2.1, 3.1, 0], 24)
        self.play(Create(a1), FadeIn(n1), run_time=0.35)
        self.en("615|seis")
        a2 = self.aro(b.p("ranuras"), 0.75, Am)
        n2 = self.nota("horizontales · 250 V", Am, [2.1, 3.1, 0], 24)
        self.play(Create(a2), FadeIn(n2), run_time=0.35)
        self.en("entre")
        n3 = self.nota("la clavija de 120 V no entra", GR, [0, -4.4, 0], 24)
        self.play(FadeIn(n3), run_time=0.3)
        self.en("adaptador")
        n4 = self.card("NUNCA CON ADAPTADOR", [], Rr, 7.8, 30).move_to([0, -5.6, 0])
        self.play(FadeIn(n4, shift=UP * 0.15), run_time=0.35)
        self.cerrar(a, b, a1, a2, n1, n2, n3, n4)

        # ------------------------------------------------------------ p6 la etiqueta
        self.voz("p6")
        self.chip("6", "LEE LA ETIQUETA", Am)
        cg = Pieza("cargador", alto=5.2).move_to([-2.2, 0.0, 0])
        et = Pieza("etq", 4.2).move_to([2.2, 0.4, 0])
        self.play(FadeIn(cg), FadeIn(et), run_time=0.4)
        self.en("100|cien")
        n1 = self.nota("✓ 100–240 V: sirve en ambos", G, [-1.6, -3.4, 0], 24)
        self.play(FadeIn(n1), run_time=0.3)
        self.en("solo|sólo")
        n2 = self.nota("solo 120 V: solo 120", Rr, [2.2, -2.0, 0], 24)
        self.play(FadeIn(n2), run_time=0.3)
        self.cerrar(cg, et, n1, n2)
        self.quitar_chip()
        self.final("P = V² / R: el doble de voltaje es cuatro veces la potencia")


class PortadaV28v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v28v2_eq"
        r = Pieza("res_240", 8.6).move_to([0, -4.4, 0])
        t = Pieza("t615", alto=4.2)
        portada_v(self, ["¿120 V", "EN 240 V?", "×4 LA POTENCIA"], t, "SE QUEMA EN SEGUNDOS", extra=r)

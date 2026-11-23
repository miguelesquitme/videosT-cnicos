"""V23 v2 · ¿Por qué el motor gira al revés? Piezas: lib/svgv23.py → v23v2_eq/. Guion: guion_v23v2.py."""
from reel_v2 import *  # noqa: F401,F403

COL = {"L1": "#B07A45", "L2": "#E4E7EC", "L3": "#8E959C"}   # L1 café, L2 negro (se dibuja claro sobre el fondo), L3 gris


class V23v2(ReelV2):
    CLAVE = "v23v2"
    GUION_MOD = "guion_v23v2"

    def giro(self, centro, r, horario, color):
        a = Arc(radius=r, start_angle=PI * 0.9, angle=(-1 if horario else 1) * PI * 1.3, color=color, stroke_width=8)
        a.add_tip(tip_length=0.3)
        return a.move_arc_center_to(centro)

    def ondas(self, ax, orden=("L1", "L2", "L3")):
        g = VGroup()
        for k, f in enumerate(orden):
            g.add(ax.plot(lambda t, k=k: np.sin(t - k * 2 * PI / 3), x_range=[0, 4 * PI, 0.05], color=COL[f], stroke_width=6))
        return g

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        mo = Pieza("motor", 8.2).move_to([0.2, 0.6, 0])
        eje = mo.mm(6, 92)
        self.play(FadeIn(mo), run_time=0.5)
        self.en("arrancas")
        g1 = self.giro(eje, 0.75, True, G)
        self.sfx("contactor", -12)
        self.play(Create(g1), run_time=0.5)
        self.en("revés")
        g2 = self.giro(eje, 0.75, False, Rr)
        self.play(ReplacementTransform(g1, g2), run_time=0.4)
        nr = self.nota("gira al revés", Rr, [-1.8, 3.2, 0], 30)
        self.play(FadeIn(nr, scale=1.2), run_time=0.3)
        self.en("cables")
        cab = VGroup(*[VGroup(Line(UP * 1.3, DOWN * 1.3).set_stroke(COL[f], 14), T(f, 30, COL[f], "HEAVY").next_to(UP * 1.3, UP, buff=0.12))
                       for f in ("L1", "L2", "L3")]).arrange(RIGHT, buff=1.3).move_to([0, -4.6, 0])
        self.play(FadeIn(cab), run_time=0.35)
        self.en("cualquiera")
        p1, p2 = cab[1].get_center(), cab[2].get_center()
        self.play(cab[1].animate.move_to(p2), cab[2].animate.move_to(p1), run_time=0.7)
        self.en("funciona")
        g3 = self.giro(eje, 0.75, True, G)
        self.play(ReplacementTransform(g2, g3), FadeOut(nr), run_time=0.4)
        self.cerrar(mo, g3, cab)

        # ------------------------------------------------------------ p1 por dentro
        self.voz("p1")
        self.chip("1", "POR DENTRO", C)
        es = Pieza("estator", 7.8).move_to([0, -1.0, 0])
        self.play(FadeIn(es, scale=0.95), run_time=0.5)
        self.en("láminas")
        l1 = self.flecha("láminas de acero al silicio · 0,5 mm", es.p("laminas"), [0, 3.4, 0], C, 24)
        self.play(FadeIn(l1), run_time=0.35)
        self.en("ranuras")
        a1 = self.aro(es.p("r_7"), 0.35, Am)
        self.play(Create(a1), run_time=0.3)
        self.en("cobre")
        l2 = self.nota("bobinado de cobre en las ranuras", Am, [0, 2.65, 0], 24)
        self.play(FadeOut(l1), FadeIn(l2), run_time=0.3)
        self.en("fase")
        ley = VGroup(*[VGroup(Square(0.34, stroke_width=0).set_fill(COL[f] if f != "L2" else "#1A1A1A", 1).set_stroke("#FFFFFF", 2),
                              T(f + (" café" if f == "L1" else " negro" if f == "L2" else " gris"), 24, self.th["txt"], "BOLD")).arrange(RIGHT, buff=0.15)
                       for f in ("L1", "L2", "L3")]).arrange(RIGHT, buff=0.45).move_to([0, -6.1, 0])
        self.play(FadeIn(ley), run_time=0.35)
        self.en("jaula")
        a2 = self.aro(es.p("barra"), 0.3, G)
        l3 = self.nota("rotor de jaula: barras de aluminio", G, [0, 2.65, 0], 24)
        self.play(FadeOut(l2), FadeOut(a1), Create(a2), FadeIn(l3), run_time=0.35)
        self.en("anillos")
        l4 = self.nota("unidas por 2 anillos en los extremos", G, [0, -5.3, 0], 22)
        self.play(FadeIn(l4), run_time=0.3)
        self.cerrar(es, a2, l3, l4, ley)

        # ------------------------------------------------------------ p2 secuencia
        self.voz("p2")
        self.chip("2", "SECUENCIA DE FASES", Am)
        ax, g = self.ejes([0.2, 0.6, 0], 7.6, 3.6, (0, 4 * PI), (-1.3, 1.3), "tiempo", "")
        on = self.ondas(ax)
        self.play(Create(ax), FadeIn(g), run_time=0.3)
        self.play(*[Create(o) for o in on], run_time=1.2)
        self.en("120|ciento")
        t1 = self.nota("separadas 120°", Am, [0, 3.3, 0], 28)
        self.play(FadeIn(t1), run_time=0.3)
        marcas = []
        for k, f in enumerate(("L1", "L2", "L3")):
            self.en(f)
            x = PI / 2 + k * 2 * PI / 3
            d = Dot(ax.c2p(x, 1), radius=0.13, color=COL[f])
            n = T(str(k + 1), 34, COL[f], "HEAVY").next_to(d, UP, buff=0.1)
            self.play(FadeIn(d, scale=1.6), FadeIn(n), run_time=0.25)
            marcas += [d, n]
        self.en("secuencia")
        sq = self.card("SECUENCIA", ["L1 → L2 → L3"], C, 7.8, 30).move_to([0, -3.4, 0])
        self.play(FadeIn(sq, shift=UP * 0.15), run_time=0.35)
        self.cerrar(ax, g, on, t1, sq, *marcas)

        # ------------------------------------------------------------ p3 campo giratorio
        self.voz("p3")
        self.chip("3", "CAMPO GIRATORIO", G)
        es = Pieza("estator_solo", 7.4).move_to([0, -0.6, 0])
        ro = Pieza("rotor", 7.4).move_to(es)
        cen = es.p("centro")
        self.play(FadeIn(es), FadeIn(ro), run_time=0.4)
        ang = ValueTracker(0)
        cam = always_redraw(lambda: VGroup(
            Arrow(cen + rotate_vector(DOWN * 2.3, ang.get_value()), cen + rotate_vector(UP * 2.3, ang.get_value()), buff=0,
                  stroke_width=10, color=Vi, max_tip_length_to_length_ratio=0.12),
            T("N", 30, Vi, "HEAVY").move_to(cen + rotate_vector(UP * 2.75, ang.get_value())),
            T("S", 30, Vi, "HEAVY").move_to(cen + rotate_vector(DOWN * 2.75, ang.get_value()))))
        self.en("gira")
        self.add(cam)
        self.play(ang.animate.set_value(-PI), run_time=1.6, rate_func=linear)
        self.en("60|sesenta")
        fm = self.card("n = 120 · f / p", ["120 · 60 / 4 = 1800 rpm"], Vi, 7.8, 30).move_to([0, 3.0, 0])
        self.play(FadeIn(fm, shift=DOWN * 0.15), ang.animate.set_value(-2 * PI), run_time=1.0, rate_func=linear)
        self.en("persigue")
        self.play(ang.animate.set_value(-3 * PI), Rotate(ro, -PI * 0.95, about_point=cen), run_time=1.6, rate_func=linear)
        self.en("1760|mil")
        rr = self.card("ROTOR: 1760 rpm", ["2,2 % más lento (deslizamiento)"], G, 7.8, 28).move_to([0, -5.6, 0])
        self.play(FadeIn(rr, shift=UP * 0.15), ang.animate.set_value(-4 * PI), Rotate(ro, -PI * 0.95, about_point=cen), run_time=1.6, rate_func=linear)
        self.remove(cam)
        self.cerrar(es, ro, fm, rr)

        # ------------------------------------------------------------ p4 invertir dos fases
        self.voz("p4")
        self.chip("4", "INVERTIR DOS FASES", Rr)
        ax, g = self.ejes([0.2, 1.2, 0], 7.6, 3.2, (0, 4 * PI), (-1.3, 1.3), "tiempo", "")
        on = self.ondas(ax)
        self.add(ax, g, on)
        self.play(FadeIn(VGroup(ax, g, on)), run_time=0.3)
        self.en("intercambias")
        on2 = self.ondas(ax, ("L1", "L3", "L2"))
        self.play(Transform(on, on2), run_time=0.8)
        self.en("queda")
        sq = self.card("SECUENCIA", ["L1 → L3 → L2"], Rr, 7.8, 30).move_to([0, -2.0, 0])
        self.play(FadeIn(sq, shift=UP * 0.15), run_time=0.35)
        self.en("revés")
        gi = self.giro([0, -4.6, 0], 0.9, False, Rr)
        tg = self.nota("el campo gira al revés", Rr, [0, -6.2, 0], 26)
        self.play(Create(gi), FadeIn(tg), run_time=0.45)
        self.en("tres")
        sq2 = self.card("LAS TRES EN ORDEN", ["L2 → L3 → L1 = misma secuencia"], C, 7.8, 28).move_to([0, -2.0, 0])
        gi2 = self.giro([0, -4.6, 0], 0.9, True, G)
        tg2 = self.nota("no cambia", G, [0, -6.2, 0], 26)
        self.play(FadeOut(sq), FadeIn(sq2), ReplacementTransform(gi, gi2), FadeOut(tg), FadeIn(tg2), run_time=0.5)
        self.en("solo")
        dos = self.nota("DOS, y solo dos", Am, [0, 3.3, 0], 32)
        self.play(FadeIn(dos, scale=1.2), run_time=0.3)
        self.cerrar(ax, g, on, sq2, gi2, tg2, dos)

        # ------------------------------------------------------------ p5 IEC 60034-8
        self.voz("p5")
        self.chip("5", "IEC 60034-8", C)
        cj = Pieza("caja", 6.0).move_to([0, -0.4, 0])
        self.play(FadeIn(cj), run_time=0.4)
        lin = []
        for f, b in (("L1", "U1"), ("L2", "V1"), ("L3", "W1")):
            self.en(f)
            pt = cj.p(b)
            ln = Line(pt + UP * 2.2, pt).set_stroke(COL[f], 12)
            tx = T(f, 28, COL[f], "HEAVY").next_to(ln, UP, buff=0.08)
            self.play(Create(ln), FadeIn(tx), run_time=0.25)
            lin += [ln, tx]
        self.en("horario")
        mo = Pieza("motor", 5.2).move_to([0.4, -4.6, 0])
        eje = mo.mm(6, 92)
        gi = self.giro(eje, 0.6, True, G)
        hr = self.nota("horario", G, [-2.8, -3.0, 0], 28)
        self.play(FadeIn(mo), Create(gi), FadeIn(hr), run_time=0.5)
        self.en("visto")
        vl = self.nota("visto desde el lado del eje", GR, [0.2, -6.6, 0], 24)
        self.play(FadeIn(vl), run_time=0.3)
        self.cerrar(cj, mo, gi, hr, vl, *lin)

        # ------------------------------------------------------------ p6 en campo
        self.voz("p6")
        self.chip("6", "EN CAMPO", Am)
        self.en("compresor")
        cp = self.card("COMPRESOR DE TORNILLO", ["al revés no bombea aceite", "se destruye en segundos"], Rr, 7.8, 28).move_to([0, 2.4, 0])
        self.play(FadeIn(cp, shift=DOWN * 0.15), run_time=0.4)
        self.en("indicador")
        ia = Pieza("ind_a", alto=8.6).move_to([0.9, -2.4, 0])
        self.play(FadeOut(cp), FadeIn(ia), run_time=0.4)
        self.wait(0.4)
        ih = Pieza("ind_h", alto=8.6)
        self.sfx("tic", -8)
        self.poner(ih, ia)
        ok = self.flecha("secuencia correcta", ih.p("led_h"), [-2.4, 2.0, 0], G, 26)
        self.play(FadeIn(ok), run_time=0.3)
        self.en("carga")
        sc = self.nota("o arranca sin carga y revisa el giro", Am, [0, 3.0, 0], 24)
        self.play(FadeIn(sc), run_time=0.3)
        self.cerrar(ih, ok, sc)
        self.quitar_chip()
        self.final("Dos fases cambiadas = campo al revés = motor al revés")


class PortadaV23v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v23v2_eq"
        es = Pieza("estator", 7.8)
        portada_v(self, ["¿POR QUÉ", "GIRA AL", "REVÉS?"], es, "CAMBIA SOLO DOS FASES")

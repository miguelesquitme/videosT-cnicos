"""V32 v2 · Estrella o triángulo. Piezas: lib/svgv32.py → v32v2_eq/. Guion: guion_v32v2.py."""
from reel_v2 import *  # noqa: F401,F403

COLF = {"L1": "#B07A45", "L2": "#E4E7EC", "L3": "#8E959C"}


class V32v2(ReelV2):
    CLAVE = "v32v2"
    GUION_MOD = "guion_v32v2"

    def bob(self, nombre, inicio, fin):
        """Coloca la bobina con su punta 'a' en inicio y 'b' en fin."""
        largo = np.linalg.norm(np.array(inicio) - np.array(fin))
        b = Pieza(nombre, alto=largo / 0.92)
        v = np.array(inicio) - np.array(fin)
        ang = np.arctan2(v[1], v[0]) - PI / 2
        b.rotate(ang)
        b.move_to((np.array(inicio) + np.array(fin)) / 2)
        return b

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        cd = Pieza("caja_d", 7.0).move_to([0, -0.6, 0])
        self.play(FadeIn(cd), run_time=0.5)
        self.en("seis")
        aros = VGroup(*[self.aro(cd.p(n), 0.42, C) for n in ("U1", "V1", "W1", "W2", "U2", "V2")])
        self.play(Create(aros), run_time=0.4)
        self.en("puentes")
        self.play(FadeOut(aros), Indicate(cd, scale_factor=1.03, color=Am), run_time=0.5)
        self.en("230")
        n1 = self.nota("230 V", Am, [-2.0, 3.2, 0], 34)
        n2 = self.nota("400 V", C, [2.0, 3.2, 0], 34)
        self.play(FadeIn(n1), run_time=0.25)
        self.play(FadeIn(n2), run_time=0.25)
        self.en("estrella")
        cy = Pieza("caja_y", 7.0)
        self.poner(cy, cd)
        t1 = self.nota("ESTRELLA (Y)", C, [0, -5.2, 0], 30)
        self.play(FadeIn(t1), run_time=0.25)
        self.en("triángulo")
        cd2 = Pieza("caja_d", 7.0)
        self.poner(cd2, cy)
        t2 = self.nota("TRIÁNGULO (Δ)", Am, [0, -5.2, 0], 30)
        self.play(FadeOut(t1), FadeIn(t2), run_time=0.25)
        self.cerrar(cd2, n1, n2, t2)

        # ------------------------------------------------------------ p1 las tres bobinas
        self.voz("p1")
        self.chip("1", "TRES BOBINAS", C)
        bs = Group(*[Pieza(n, alto=4.0) for n in ("bU", "bV", "bW")]).arrange(RIGHT, buff=1.0).move_to([0, 1.2, 0])
        self.en("bobinas")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bs], lag_ratio=0.2), run_time=0.7)
        cl = Pieza("caja_l", 5.6).move_to([0, -4.2, 0])
        self.en("caja")
        self.play(FadeIn(cl), run_time=0.35)
        self.en("U1")
        r1 = self.recuadro((cl.p("U1") + cl.p("W1")) / 2, 4.0, 0.9, G)
        n1 = self.nota("inicios", G, [-3.3, cl.p("U1")[1], 0], 24)
        self.play(Create(r1), FadeIn(n1), run_time=0.35)
        self.en("W2")
        r2 = self.recuadro((cl.p("W2") + cl.p("V2")) / 2, 4.0, 0.9, Am)
        n2 = self.nota("finales", Am, [-3.3, cl.p("W2")[1], 0], 24)
        self.play(Create(r2), FadeIn(n2), run_time=0.35)
        self.en("corridos")
        n3 = self.nota("W2 U2 V2: corridos un lugar", Am, [0, -6.8, 0], 24)
        self.play(FadeIn(n3), run_time=0.3)
        self.cerrar(bs, cl, r1, r2, n1, n2, n3)

        # ------------------------------------------------------------ p2 estrella
        self.voz("p2")
        self.chip("2", "ESTRELLA (Y)", C)
        cen = np.array([0, 0.5, 0])
        Rb = 2.5
        dirs = [np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 + 4 * PI / 3)]
        bobs = Group(*[self.bob(n, cen + d * Rb, cen) for n, d in zip(("bU", "bV", "bW"), dirs)])
        self.en("puentes")
        cy = Pieza("caja_y", 3.8).move_to([0, -5.6, 0])
        self.play(FadeIn(cy), run_time=0.35)
        self.en("común")
        pc = Dot(cen, radius=0.16, color=Am)
        self.play(FadeIn(bobs), FadeIn(pc, scale=1.6), run_time=0.6)
        fases = VGroup(*[T(f, 28, COLF[f], "HEAVY").move_to(cen + d * (Rb + 0.4)) for f, d in zip(("L1", "L2", "L3"), dirs)])
        self.play(FadeIn(fases), run_time=0.3)
        self.en("raíz")
        k = self.nota("V bobina = V línea / √3", Am, [0, -1.75, 0], 26)
        self.play(FadeIn(k), run_time=0.3)
        self.en("400")
        k2 = self.card("400 V ÷ √3 = 230 V", ["en cada bobina"], C, 7.8, 28).move_to([0, -3.0, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.cerrar(bobs, pc, fases, cy, k, k2)

        # ------------------------------------------------------------ p3 triángulo
        self.voz("p3")
        self.chip("3", "TRIÁNGULO (Δ)", Am)
        cen = np.array([0, 0.4, 0])
        Rv = 2.7
        V = [cen + Rv * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 - 2 * PI / 3, PI / 2 + 2 * PI / 3)]
        cd = Pieza("caja_d", 4.6).move_to([0, -5.0, 0])
        self.en("verticales")
        self.play(FadeIn(cd), run_time=0.35)
        bU = self.bob("bU", V[0], V[1])
        bV = self.bob("bV", V[1], V[2])
        bW = self.bob("bW", V[2], V[0])
        self.en("U1")
        self.play(FadeIn(bU), run_time=0.3)
        self.en("B1|V1")
        self.play(FadeIn(bV), run_time=0.3)
        self.en("W1")
        self.play(FadeIn(bW), run_time=0.3)
        fases = VGroup(*[T(f, 28, COLF[f], "HEAVY").move_to(v + (v - cen) / np.linalg.norm(v - cen) * 0.5) for f, v in zip(("L1", "L2", "L3"), V)])
        self.en("dos")
        self.play(FadeIn(fases), run_time=0.3)
        self.en("completo")
        k = self.card("V bobina = V línea = 230 V", [], Am, 7.8, 28).move_to([0, -2.7, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.cerrar(bU, bV, bW, fases, cd, k)

        # ------------------------------------------------------------ p4 la placa
        self.voz("p4")
        self.chip("4", "LA PLACA", G)
        pl = Pieza("placa", 6.4).move_to([0, 1.6, 0])
        self.play(FadeIn(pl), run_time=0.4)
        self.en("siempre")
        k1 = self.card("LAS BOBINAS VEN 230 V", ["en Δ a 230 · en Y a 400"], G, 7.8, 28).move_to([0, -1.6, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("conectas")
        k2 = self.card("Δ EN 400 V", ["√3 veces más en cada bobina → se quema"], Rr, 7.8, 28).move_to([0, -3.9, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.cerrar(pl, k1, k2)

        # ------------------------------------------------------------ p5 arranque estrella-triángulo
        self.voz("p5")
        self.chip("5", "ARRANQUE Y-Δ", Vi)
        self.en("arrancarlo")
        y0 = -2.4
        b1 = Rectangle(width=1.6, height=4.5, stroke_width=0).set_fill(Rr, 1).move_to([-1.8, y0, 0], aligned_edge=DOWN)
        t1 = T("directo", 26, Rr, "HEAVY").next_to(b1, DOWN, buff=0.12)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(t1), run_time=0.4)
        self.en("tercio")
        b2 = Rectangle(width=1.6, height=1.5, stroke_width=0).set_fill(G, 1).move_to([1.8, y0, 0], aligned_edge=DOWN)
        t2 = T("en estrella", 26, G, "HEAVY").next_to(b2, DOWN, buff=0.12)
        n = self.nota("⅓ de corriente y de par", G, [1.8, -0.4, 0], 24)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(t2), FadeIn(n), run_time=0.45)
        self.en("80|ochenta")
        k = self.card("≈ 80 % DE LA VELOCIDAD", ["se cambia a triángulo"], Vi, 7.8, 28).move_to([0, -4.9, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.cerrar(b1, b2, t1, t2, n, k)

        # ------------------------------------------------------------ p6 en campo
        self.voz("p6")
        self.chip("6", "EN CAMPO", Am)
        cl = Pieza("caja_l", 6.0).move_to([0, 1.0, 0])
        self.play(FadeIn(cl), run_time=0.35)
        self.en("contactores")
        k1 = self.card("SEIS BORNES LIBRES", ["tres contactores: línea, estrella y triángulo"], C, 7.8, 26).move_to([0, -2.6, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("58|0")
        k2 = self.card("RELÉ TÉRMICO = 0,58 × In", ["mide la corriente de las bobinas"], Am, 7.8, 26).move_to([0, -4.8, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.cerrar(cl, k1, k2)
        self.quitar_chip()
        self.final("Y: V/√3 por bobina · Δ: V completo · placa 230 Δ / 400 Y")


class PortadaV32v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v32v2_eq"
        a = Pieza("caja_y", 4.2).move_to([-2.1, -1.0, 0])
        b = Pieza("caja_d", 4.2).move_to([2.1, -1.0, 0])
        portada_v(self, ["¿ESTRELLA", "O", "TRIÁNGULO?"], Group(a, b), "6 BORNES, 3 PUENTES")

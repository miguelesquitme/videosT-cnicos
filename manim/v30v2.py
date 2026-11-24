"""V30 v2 · Kilovatio hora. Piezas: lib/svgv30.py → v30v2_eq/. Guion: guion_v30v2.py."""
from reel_v2 import *  # noqa: F401,F403


class V30v2(ReelV2):
    CLAVE = "v30v2"
    GUION_MOD = "guion_v30v2"

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        md = Pieza("medidor", 6.8).move_to([0, -1.0, 0])
        self.play(FadeIn(md), run_time=0.5)
        self.en("voltios")
        x1 = self.nota("voltios ✗   amperios ✗", Rr, [0, 3.2, 0], 28)
        self.play(FadeIn(x1), run_time=0.3)
        self.en("kilovatios")
        a = self.recuadro(md.p("lcd"), 4.3, 1.4, G)
        x2 = self.nota("kilovatios hora (kWh) ✓", G, [0, 2.4, 0], 28)
        self.play(Create(a), FadeIn(x2), run_time=0.35)
        self.cerrar(md, x1, x2, a)

        # ------------------------------------------------------------ p1 potencia y energía
        self.voz("p1")
        self.chip("1", "POTENCIA Y ENERGÍA", C)
        self.en("vatio")
        k1 = self.card("VATIO (W) = POTENCIA", ["qué tan rápido se usa la energía"], C, 7.8, 30).move_to([0, 2.2, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("kilovatio")
        k2 = self.card("kWh = ENERGÍA", ["potencia × tiempo"], Am, 7.8, 30).move_to([0, -0.1, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.en("mil")
        k3 = self.card("1000 W × 1 h = 1 kWh", ["= 3 600 000 J (3,6 MJ)"], G, 7.8, 30).move_to([0, -2.4, 0])
        self.play(FadeIn(k3, shift=UP * 0.15), run_time=0.35)
        self.cerrar(k1, k2, k3)

        # ------------------------------------------------------------ p2 el medidor
        self.voz("p2")
        self.chip("2", "EL MEDIDOR", Am)
        md = Pieza("medidor", 7.6).move_to([0, -0.4, 0])
        self.play(FadeIn(md), run_time=0.4)
        self.en("2S|forma")
        a1 = self.flecha("forma 2S · CL200 · 120/240 V", md.p("placa"), [0, -5.6, 0], C, 24)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("multiplica")
        f = self.nota("energía = Σ V · I · Δt", Am, [0, 3.3, 0], 28)
        self.play(FadeIn(f), run_time=0.3)
        self.en("registro")
        md2 = Pieza("medidor2", 7.6)
        self.poner(md2, md)
        a2 = self.recuadro(md2.p("lcd"), 4.6, 1.5, G)
        self.play(Create(a2), run_time=0.3)
        self.en("led")
        a3 = self.aro(md2.p("led"), 0.3, Rr)
        pul = Dot(md2.p("led"), radius=0.16, color="#FF4D6D")
        self.play(Create(a3), run_time=0.25)
        for _ in range(3):
            self.play(FadeIn(pul, run_time=0.12))
            self.play(FadeOut(pul, run_time=0.25))
        n = self.nota("LED infrarrojo: pulsos proporcionales a la energía", Rr, [0, -6.6, 0], 20)
        self.play(FadeIn(n), run_time=0.3)
        self.cerrar(md2, a1, f, a2, a3, n)

        # ------------------------------------------------------------ p3 la cuenta
        self.voz("p3")
        self.chip("3", "LA CUENTA", G)
        pl = Pieza("plancha", 5.6).move_to([-1.3, 2.2, 0])
        self.en("plancha")
        self.play(FadeIn(pl), run_time=0.35)
        self.en("media")
        k1 = self.card("1200 W × 0,5 h = 0,6 kWh", [], Am, 7.8, 30).move_to([0, 0.0, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("televisor")
        tv = Pieza("tele", 4.6).move_to([-1.6, -2.8, 0])
        self.play(FadeIn(tv), run_time=0.35)
        self.en("15|mes")
        k2 = self.card("100 W × 5 h × 30 días", ["= 15 kWh al mes"], C, 7.8, 28).move_to([0, -5.6, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.cerrar(pl, k1, tv, k2)

        # ------------------------------------------------------------ p4 lo que más gasta
        self.voz("p4")
        self.chip("4", "LO QUE MÁS GASTA", Rr)
        self.en("calor")
        k1 = self.card("LO QUE CALIENTA", ["plancha · ducha · estufa · secadora", "mucha potencia"], Rr, 7.8, 28).move_to([0, 1.6, 0])
        pl = Pieza("plancha", 4.4).move_to([0, -3.6, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), FadeIn(pl), run_time=0.35)
        self.en("electrónicos")
        k2 = self.card("ELECTRÓNICOS", ["poca potencia, muchas horas"], C, 7.8, 28).move_to([0, -0.9, 0])
        tv = Pieza("tele", 3.6).move_to([0, -5.8, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), pl.animate.move_to([0, -3.4, 0]).scale(0.85), FadeIn(tv), run_time=0.35)
        self.cerrar(k1, k2, pl, tv)

        # ------------------------------------------------------------ p5 consumo en espera
        self.voz("p5")
        self.chip("5", "CONSUMO EN ESPERA", Vi)
        cg = Pieza("cargador", alto=4.8).move_to([0, 1.0, 0])
        self.en("espera")
        self.play(FadeIn(cg), run_time=0.35)
        self.en("5|cinco")
        k1 = self.card("5 W × 720 h = 3,6 kWh", ["todo un mes, sin usarlo"], Vi, 7.8, 30).move_to([0, -2.7, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("10|diez")
        n = self.nota("espera: 5–10 % de la energía de una casa", Am, [0, -4.6, 0], 24)
        self.play(FadeIn(n), run_time=0.3)
        self.cerrar(cg, k1, n)

        # ------------------------------------------------------------ p6 la fórmula
        self.voz("p6")
        self.chip("6", "LA FÓRMULA", G)
        self.en("fórmula")
        f = self.card("kWh = W × h/día × días ÷ 1000", [], G, 7.8, 30).move_to([0, 1.6, 0])
        self.play(FadeIn(f, shift=UP * 0.15), run_time=0.35)
        self.en("precio")
        q = self.card("COSTO = kWh × precio del kWh", ["el precio está en tu recibo"], Am, 7.8, 28).move_to([0, -0.8, 0])
        md = Pieza("medidor", 5.2).move_to([0, -4.4, 0])
        self.play(FadeIn(q, shift=UP * 0.15), FadeIn(md), run_time=0.35)
        self.cerrar(f, q, md)
        self.quitar_chip()
        self.final("kWh = vatios × horas ÷ 1000")


class PortadaV30v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v30v2_eq"
        md = Pieza("medidor", 7.6)
        portada_v(self, ["¿QUÉ TE", "COBRAN EN", "EL RECIBO?"], md, "EL KILOVATIO HORA")

"""V33 v2 · IP65. Piezas: lib/svgv33.py → v33v2_eq/. Guion: guion_v33v2.py."""
from reel_v2 import *  # noqa: F401,F403


class V33v2(ReelV2):
    CLAVE = "v33v2"
    GUION_MOD = "guion_v33v2"

    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        GR = "#5B6472"
        AZ = "#4FA3E0"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        gb = Pieza("gab", 6.4).move_to([0, -0.8, 0])
        self.play(FadeIn(gb), run_time=0.5)
        self.en("IP")
        n = self.nota("IP65 · IP66 · IP67", C, [0, 3.2, 0], 34)
        self.play(FadeIn(n, scale=1.2), run_time=0.3)
        self.en("ensayo")
        k = self.card("IEC 60529", ["cada número = un ensayo"], Am, 7.8, 30).move_to([0, -5.4, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.cerrar(gb, n, k)

        # ------------------------------------------------------------ p1 el código
        self.voz("p1")
        self.chip("1", "EL CÓDIGO", C)
        ip = T("IP", 150, self.th["txt"], "HEAVY")
        d1 = T("6", 150, Am, "HEAVY")
        d2 = T("5", 150, AZ, "HEAVY")
        cod = VGroup(ip, d1, d2).arrange(RIGHT, buff=0.35).move_to([0, 1.6, 0])
        self.play(FadeIn(ip), run_time=0.3)
        self.en("primera")
        b1 = Brace(d1, DOWN, color=Am)
        t1 = self.nota("sólidos y polvo: 0 a 6", Am, [-1.6, -0.6, 0], 26)
        self.play(FadeIn(d1), GrowFromCenter(b1), FadeIn(t1), run_time=0.4)
        self.en("segunda")
        b2 = Brace(d2, DOWN, color=AZ)
        t2 = self.nota("agua: 0 a 9", AZ, [2.0, -1.5, 0], 26)
        self.play(FadeIn(d2), GrowFromCenter(b2), FadeIn(t2), run_time=0.4)
        self.en("X|IPX5")
        kx = self.card("IPX5", ["X = cifra no ensayada"], GR, 7.8, 32).move_to([0, -4.0, 0])
        self.play(FadeIn(kx, shift=UP * 0.15), run_time=0.35)
        self.cerrar(cod, b1, b2, t1, t2, kx)

        # ------------------------------------------------------------ p2 primera cifra
        self.voz("p2")
        self.chip("2", "PRIMERA CIFRA", Am)
        so = Pieza("sondas", 8.4).move_to([0, 0.2, 0])
        self.en("calibres")
        self.play(FadeIn(so), run_time=0.4)
        marcas = []
        for pal, k, txt in (("esfera|uno", 1, "1 · Ø 50 mm"), ("dos|dedo", 2, "2 · dedo Ø 12"), ("tres|varilla", 3, "3 · Ø 2,5"), ("cuatro|alambre", 4, "4 · Ø 1,0")):
            self.en(pal)
            t = self.nota(txt, Am, so.p(f"s{k}") + DOWN * 0.45, 20)
            self.play(FadeIn(t, shift=UP * 0.1), run_time=0.25)
            marcas.append(t)
        self.en("seis")
        k6 = self.card("6 · HERMÉTICO AL POLVO", ["cámara de polvo con vacío:", "sin depósito de polvo adentro"], Am, 7.8, 26).move_to([0, -5.3, 0])
        self.play(FadeIn(k6, shift=UP * 0.15), run_time=0.35)
        self.cerrar(so, k6, *marcas)

        # ------------------------------------------------------------ p3 segunda cifra
        self.voz("p3")
        self.chip("3", "SEGUNDA CIFRA", C)
        self.en("5|cinco")
        b5 = Pieza("boq5", 8.0).move_to([0, 2.5, 0])
        self.sfx("whoosh", -14)
        self.play(FadeIn(b5, shift=RIGHT * 0.3), run_time=0.4)
        self.en("boquilla")
        k5 = self.card("5 · CHORROS", ["Ø 6,3 mm · 12,5 L/min · 3 m · ≥ 3 min"], AZ, 7.8, 26).move_to([0, 0.6, 0])
        self.play(FadeIn(k5, shift=UP * 0.15), run_time=0.35)
        self.en("6|seis")
        b6 = Pieza("boq6", 8.0).move_to([0, -1.6, 0])
        k6 = self.card("6 · CHORROS FUERTES", ["Ø 12,5 mm · 100 L/min"], C, 7.8, 26).move_to([0, -3.4, 0])
        self.play(FadeIn(b6, shift=RIGHT * 0.3), FadeIn(k6, shift=UP * 0.15), run_time=0.45)
        self.en("7|siete|sumergido")
        k7 = self.card("7 · INMERSIÓN", ["1 m durante 30 min"], Vi, 7.8, 26).move_to([0, -5.4, 0])
        self.play(FadeIn(k7, shift=UP * 0.15), run_time=0.35)
        self.cerrar(b5, k5, b6, k6, k7)

        # ------------------------------------------------------------ p4 ojo
        self.voz("p4")
        self.chip("4", "OJO", Rr)
        self.en("7|siete")
        k1 = self.card("IP67 NO ES «MÁS» QUE IP66", ["inmersión ≠ chorros fuertes"], Rr, 7.8, 28).move_to([0, 1.6, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("marcados")
        k2 = self.card("IP66 / IP67", ["pasó los dos ensayos"], G, 7.8, 34).move_to([0, -0.8, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.cerrar(k1, k2)

        # ------------------------------------------------------------ p5 la instalación
        self.voz("p5")
        self.chip("5", "LA INSTALACIÓN", Am)
        gb = Pieza("gab", 4.4).move_to([-2.1, 1.3, 0])
        ju = Pieza("junta", 4.2).move_to([2.2, 1.3, 0])
        self.play(FadeIn(gb), run_time=0.35)
        self.en("empaque")
        self.play(FadeIn(ju), run_time=0.35)
        a1 = self.flecha("silicona", ju.p("empaque"), [2.2, 3.5, 0], Am, 22)
        self.play(FadeIn(a1), run_time=0.25)
        self.en("tornillos")
        aro = self.aro(gb.p("flojo"), 0.3, C)
        self.play(Create(aro), run_time=0.3)
        self.en("flojo")
        gf = Pieza("gab_flojo", 4.4)
        jf = Pieza("junta_flojo", 4.2)
        self.poner(gf, gb)
        self.poner(jf, ju)
        n1 = self.nota("tornillo flojo: no sella", Rr, [0, -1.3, 0], 24)
        self.play(FadeIn(n1), run_time=0.3)
        self.en("agujero")
        ag = Pieza("agujero", 4.4).move_to([0, -4.2, 0])
        self.play(FadeIn(ag), run_time=0.35)
        self.en("nada|hipe")
        n2 = self.nota("sin prensaestopas: ya no es IP nada", Rr, [0, -6.6, 0], 24)
        self.play(FadeIn(n2), run_time=0.3)
        self.cerrar(gf, jf, a1, aro, n1, ag, n2)

        # ------------------------------------------------------------ p6 el prensaestopas
        self.voz("p6")
        self.chip("6", "EL PRENSAESTOPAS", G)
        pe = Pieza("prensa", alto=9.0).move_to([-1.9, -1.6, 0])
        self.play(FadeIn(pe), run_time=0.4)
        self.en("sello")
        a1 = self.flecha("sello con laminillas", pe.p("inserto"), [2.1, 2.4, 0], Am, 22)
        self.play(FadeIn(a1), run_time=0.3)
        self.en("tuerca")
        a2 = self.flecha("tuerca ciega", pe.p("tuerca"), [2.1, 3.3, 0], C, 22)
        self.play(FadeIn(a2), run_time=0.3)
        self.en("7|siete")
        k1 = self.card("M20 × 1,5", ["cable de 7 a 13 mm"], C, 4.6, 26).move_to([2.2, 0.6, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.35)
        self.en("IP68")
        k2 = self.card("IP68", [], G, 4.6, 34).move_to([2.2, -1.2, 0])
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.35)
        self.en("par")
        k3 = self.card("PAR DEL FABRICANTE", ["p. ej. 12 N·m en M20"], Am, 4.6, 24).move_to([2.2, -3.0, 0])
        self.play(FadeIn(k3, shift=UP * 0.15), run_time=0.35)
        self.cerrar(pe, a1, a2, k1, k2, k3)
        self.quitar_chip()
        self.final("IP = polvo + agua · cada cifra es un ensayo de IEC 60529")


class PortadaV33v2(Scene):
    def construct(self):
        import reel_v2
        reel_v2.Pieza.CARPETA = DIR / "v33v2_eq"
        gb = Pieza("gab", 5.0).move_to([-1.4, -1.6, 0])
        bq = Pieza("boq6", 5.4).move_to([2.0, 0.6, 0]).rotate(PI)
        portada_v(self, ["¿QUÉ", "SIGNIFICA", "IP65?"], Group(gb, bq), "POLVO + AGUA")

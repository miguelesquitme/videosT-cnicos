"""Shorts V03–V10 rehechos (estándar nuevo). Guiones y fuentes en guiones_c.py.
Render: FORMATO=v VOZ=eleven manim -qh -o final shorts_c.py V03C
"""
from shorts_b import *  # noqa: F401,F403  (ShortV, T/pastilla con ancho limitado, caja_dato, seccion, llama, etc.)
from shorts_b import _osc
import shorts_v
from shorts_v import transformador, ducha, avioneta, nucleo
from dibujos_aves import poste, linea_aerea, aislador_pin, pajarito, escalera, piscucha, conductor_frente
from taller import portalampara_led
from guiones_c import GUIONES_C

shorts_v.SHORTS.update(GUIONES_C)
DUR_MIN = 93.0


class ShortC(ShortV):
    def construct(self):
        super().construct()
        resto = DUR_MIN - self.renderer.time
        if resto > 0:
            self.wait(resto)


def esfera_m(color, r=0.4):
    return VGroup(Circle(radius=r, stroke_color=_osc(color, 0.35), stroke_width=2).set_fill(color, 1),
                  Arc(radius=r * 0.62, start_angle=PI * 0.55, angle=PI * 0.35).set_stroke(WHITE, 3, 0.6),
                  Line([0, r, 0], [0, r + 0.12, 0]).set_stroke("#5B6573", 4))


def ondas_sonido(c, n=3, r0=0.6, dr=0.45, ang=PI / 2.5, color=CIAN, direc=0.0):
    return VGroup(*[Arc(radius=r0 + dr * k, start_angle=direc - ang / 2, angle=ang, arc_center=c).set_stroke(color, 5 - k, 1 - 0.2 * k)
                    for k in range(n)])


def rosca_portalamparas(s=1.0):
    """Portalámparas en corte: rosca metálica (neutro) y contacto central (fase)."""
    cuerpo = RoundedRectangle(width=1.8, height=2.2, corner_radius=0.2, stroke_color="#8F9AC8", stroke_width=2).set_fill("#2A2E35", 1)
    rosca = VGroup(Rectangle(width=1.2, height=1.4, stroke_color=METAL_OSC, stroke_width=2).set_fill("#C9CED6", 1).shift(DOWN * 0.25),
                   *[Line([-0.6, y, 0], [0.6, y + 0.12, 0]).set_stroke(METAL_OSC, 2) for y in np.linspace(-0.8, 0.25, 5)])
    centro = RoundedRectangle(width=0.36, height=0.18, corner_radius=0.05, stroke_color="#7A5A12", stroke_width=1.5).set_fill(LATON, 1).move_to([0, 0.62, 0])
    g = VGroup(cuerpo, rosca, centro).scale(s)
    g.rosca, g.centro = rosca, centro
    return g


def interruptor_sw(on=True):
    base = Dot(radius=0.09, color=TINTA)
    b2 = Dot(radius=0.09, color=TINTA).shift(RIGHT * 1.2)
    pal = Line(ORIGIN, RIGHT * 1.15 if on else np.array([1.0, 0.55, 0])).set_stroke(TINTA, 6)
    return VGroup(base, b2, pal)


def probador():
    cuerpo = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.25, stroke_color="#C7CCD6", stroke_width=2).set_fill(AMBAR, 1)
    luces = VGroup(*[Circle(radius=0.16, stroke_color="#7A5A12", stroke_width=1.5).set_fill("#5A4A20", 1) for _ in range(3)]).arrange(RIGHT, buff=0.25)
    luces.move_to(cuerpo.get_center() + UP * 0.18)
    txt = T("PROBADOR", 18, "#1D2939", "HEAVY").move_to(cuerpo.get_center() + DOWN * 0.35)
    g = VGroup(cuerpo, luces, txt)
    g.luces = luces
    return g


# ====================================================================== V03 · bolas de colores
class V03C(ShortC):
    CLAVE = "v03c"

    def escena_rio(self, y_cable=1.6):
        agua = Rectangle(width=9.2, height=2.6, stroke_width=0).set_fill("#1E5B8A", 1).move_to([0, -4.4, 0])
        ol = VGroup(*[onda(lambda x: np.sin(x * 4 + k), -4.4, 4.4, -3.7 - 0.5 * k, 0.06, "#5AB3E6", 3) for k in range(3)])
        orillas = VGroup(Polygon([-4.6, -3.1, 0], [-3.0, -3.1, 0], [-2.2, -5.8, 0], [-4.6, -5.8, 0], stroke_width=0).set_fill("#2E4A2A", 1),
                         Polygon([4.6, -3.1, 0], [3.0, -3.1, 0], [2.2, -5.8, 0], [4.6, -5.8, 0], stroke_width=0).set_fill("#2E4A2A", 1))
        torres = VGroup(*[VGroup(Line([x, -3.1, 0], [x, y_cable + 0.3, 0]).set_stroke("#98A2B3", 8),
                                 Line([x - 0.5, y_cable + 0.3, 0], [x + 0.5, y_cable + 0.3, 0]).set_stroke("#98A2B3", 6)) for x in (-3.8, 3.8)])
        cab = linea_aerea([-3.8, y_cable + 0.3, 0], [3.8, y_cable + 0.3, 0], 0.9, "#C7CCD6", 4)
        return agua, ol, orillas, torres, cab

    def cuerpo(self):
        self.voz("gancho")
        agua, ol, orillas, torres, cab = self.escena_rio()
        self.play(FadeIn(agua), FadeIn(ol), FadeIn(orillas), FadeIn(torres), run_time=0.5)
        self.play(Create(cab), run_time=0.6)
        cols = [NARANJA, WHITE, AMAR_FR, NARANJA, WHITE]
        bolas = VGroup(*[esfera_m(c, 0.32).move_to(cab.point_from_proportion(t) + DOWN * 0.3) for c, t in zip(cols, np.linspace(0.17, 0.83, 5))])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in bolas], lag_ratio=0.15), run_time=0.9)
        av = avioneta().scale(0.55).move_to([-3.4, 3.2, 0])
        self.frac(0.25)
        q = VGroup(T("no son adornos", 40, TINTA, "HEAVY"), pastilla("son para los PILOTOS", NARANJA, 40, True)).arrange(DOWN, buff=0.2).move_to([0.6, -1.0, 0])
        self.play(FadeIn(q[0]), run_time=0.3)
        self.play(FadeIn(av, shift=RIGHT * 0.5), FadeIn(q[1], scale=1.1), run_time=0.5)
        self.play(av.animate.shift(RIGHT * 2.5), run_time=1.0)
        self.cerrar_voz(0.15)
        self.limpiar(agua, ol, orillas, torres, cab, bolas, av, q)

        # p1: el cable es casi invisible
        self.voz("p1")
        cielo = Rectangle(width=9.2, height=9.0, stroke_width=0).set_fill(color=["#7FB2E5", "#CFE3F5"], opacity=1).set_sheen_direction(UP).move_to([0, 0, 0])
        mont = Polygon([-4.6, -4.5, 0], [-2.5, -1.2, 0], [-1.0, -2.6, 0], [1.2, -0.6, 0], [4.6, -3.0, 0], [4.6, -4.5, 0], stroke_width=0).set_fill("#4F6B4A", 1)
        hilo = linea_aerea([-4.6, 1.6, 0], [4.6, 1.2, 0], 0.6, "#8C96A3", 1.4)
        self.play(FadeIn(cielo), FadeIn(mont), Create(hilo), run_time=0.7)
        ves = T("¿lo ves?", 56, "#1D2939", "HEAVY").move_to([0, 3.6, 0])
        self.play(FadeIn(ves), run_time=0.3)
        self.frac(0.12)
        lupa_c = Circle(radius=1.4, stroke_color=AMBAR, stroke_width=6).move_to([1.6, -1.8, 0])
        dentro = Circle(radius=1.38, stroke_width=0).set_fill("#CFE3F5", 1).move_to(lupa_c)
        grueso = Line(lupa_c.get_left() + RIGHT * 0.05 + UP * 0.1, lupa_c.get_right() + LEFT * 0.05 + DOWN * 0.1).set_stroke("#8C96A3", 22)
        mango = Line(lupa_c.get_corner(DR) + UL * 0.25, lupa_c.get_corner(DR) + DR * 0.55).set_stroke(AMBAR, 12)
        guia = DashedLine(hilo.point_from_proportion(0.65), lupa_c.get_top(), color=AMBAR)
        cota = VGroup(T("1 – 2 cm", 40, "#1D2939", "HEAVY")).next_to(lupa_c, LEFT, buff=0.2)
        self.play(Create(guia), FadeIn(dentro), Create(lupa_c), Create(mango), run_time=0.6)
        self.play(GrowFromCenter(grueso), FadeIn(cota), run_time=0.5)
        self.frac(0.3)
        heli = avioneta().scale(0.5).move_to([-3.6, 2.4, 0])
        self.play(FadeIn(heli), run_time=0.3)
        self.play(heli.animate.move_to([-0.4, 1.7, 0]), run_time=1.2)
        x_ = equis(ROJO, 0.45).move_to([-0.2, 1.4, 0])
        mort = pastilla("chocar con un cable es mortal", ROJO, 36, True).move_to([0, -5.0, 0])
        self.play(FadeIn(x_, scale=1.5), FadeIn(mort), Flash([-0.2, 1.4, 0], color=ROJO), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(cielo, mont, hilo, ves, lupa_c, dentro, grueso, mango, guia, cota, heli, x_, mort)

        # p2: 91 cm en cruces largos — escala con una persona
        self.voz("p2")
        tit = caja_dato("FAA · AC 70/7460-1L", "marcadores esféricos", NARANJA, 5.4, 28).move_to([0, 3.6, 0])
        self.play(FadeIn(tit), run_time=0.4)
        suelo = Line([-4.0, -4.2, 0], [4.0, -4.2, 0]).set_stroke("#4A5AA0", 4)
        pe = persona("#2F6FB0").scale(1.0 / 2.7 * 3.4).move_to([-2.2, -4.2, 0], aligned_edge=DOWN)  # 1.70 m ≈ 3.4 u
        bola = esfera_m(NARANJA, 0.91).move_to([0.6, -4.2 + 0.91, 0])
        bola[2].set_opacity(0)
        cota = VGroup(DoubleArrow(bola.get_corner(UR) + RIGHT * 0.3 + DOWN * 0.0, bola.get_corner(DR) + RIGHT * 0.3, buff=0, color=TINTA, stroke_width=4, tip_length=0.2),
                      T("≥ 91 cm", 44, NARANJA, "HEAVY").next_to(bola, RIGHT, buff=0.45))
        h17 = VGroup(DoubleArrow([-3.4, -4.2, 0], [-3.4, -0.8, 0], buff=0, color=CLARO, stroke_width=3, tip_length=0.2), T("1.70 m", 28, CLARO, "BOLD").move_to([-3.4, -0.4, 0]))
        self.play(Create(suelo), FadeIn(pe), FadeIn(h17), run_time=0.5)
        self.frac(0.2)
        self.play(GrowFromCenter(bola), FadeIn(cota), run_time=0.7)
        donde = VGroup(*[pastilla(t_, MARCA, 30, True) for t_ in ("cañones", "lagos", "ríos")]).arrange(RIGHT, buff=0.25).move_to([0, 1.6, 0])
        self.frac(0.15)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in donde], lag_ratio=0.3), run_time=0.8)
        self.cerrar_voz(0.15)
        self.limpiar(tit, suelo, pe, bola, cota, h17, donde)

        # p3: 51 cm cerca de pistas, separación ≈ 60 m
        self.voz("p3")
        pista = VGroup(Rectangle(width=8.6, height=1.6, stroke_width=0).set_fill("#3A3F48", 1).move_to([0, -3.6, 0]),
                       *[Rectangle(width=0.6, height=0.1, stroke_width=0).set_fill(WHITE, 1).move_to([x, -3.6, 0]) for x in np.arange(-3.8, 4.0, 1.2)])
        self.play(FadeIn(pista), run_time=0.4)
        cab2 = linea_aerea([-4.4, 1.0, 0], [4.4, 1.0, 0], 0.5, "#C7CCD6", 4)
        self.play(Create(cab2), run_time=0.4)
        bs = VGroup(*[esfera_m(c, 0.26).move_to(cab2.point_from_proportion(t) + DOWN * 0.25) for c, t in zip([AMAR_FR, WHITE, NARANJA], (0.2, 0.5, 0.8))])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in bs], lag_ratio=0.2), run_time=0.6)
        t51 = T("51 cm cerca de pistas", 40, AMAR_FR, "HEAVY").move_to([0, 2.6, 0])
        self.play(FadeIn(t51), run_time=0.3)
        self.frac(0.25)
        sep = VGroup(DoubleArrow(bs[0].get_bottom() + DOWN * 0.3, bs[1].get_bottom() + DOWN * 0.3, buff=0, color=TINTA, stroke_width=4, tip_length=0.2),
                     T("≈ 60 m", 44, TINTA, "HEAVY").next_to(bs[0:2], DOWN, buff=0.75))
        self.play(GrowFromCenter(sep[0]), FadeIn(sep[1]), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(pista, cab2, bs, t51, sep)

        # p4: contraste en tres fondos
        self.voz("p4")
        paneles = VGroup()
        for k, (nom, col1, col2) in enumerate([("cielo", "#7FB2E5", "#CFE3F5"), ("montaña", "#2E4A2A", "#4F6B4A"), ("agua", "#1E5B8A", "#2F78B0")]):
            p_ = RoundedRectangle(width=2.7, height=4.2, corner_radius=0.2, stroke_color="#4A5AA0", stroke_width=3).set_fill(color=[col1, col2], opacity=1)
            p_.set_sheen_direction(UP).move_to([-2.9 + 2.9 * k, 0.3, 0])
            l_ = T(nom, 32, TINTA, "HEAVY").next_to(p_, UP, buff=0.15)
            trio = VGroup(*[esfera_m(c, 0.3) for c in (NARANJA, WHITE, AMAR_FR)]).arrange(DOWN, buff=0.35).move_to(p_)
            paneles.add(VGroup(p_, l_, trio))
        self.play(LaggedStart(*[FadeIn(p_[0:2]) for p_ in paneles], lag_ratio=0.2), run_time=0.7)
        self.play(*[LaggedStart(*[FadeIn(b, scale=0.5) for b in p_[2]], lag_ratio=0.2) for p_ in paneles], run_time=0.7)
        self.frac(0.25)
        mejor = [paneles[0][2][0], paneles[1][2][2], paneles[2][2][1]]
        self.play(*[Indicate(b, color=None, scale_factor=1.35) for b in mejor], run_time=0.8)
        alt = pastilla("alternados: siempre hay uno que resalta", NARANJA, 32, True).move_to([0, -3.4, 0])
        self.play(FadeIn(alt, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(paneles, alt)

        # p4b: esfera vs placa girando
        self.voz("p4b")
        bola = esfera_m(NARANJA, 1.1).move_to([-2.0, 0.8, 0])
        bola[2].set_opacity(0)
        placa = Rectangle(width=2.2, height=2.2, stroke_color=_osc(NARANJA, 0.35), stroke_width=3).set_fill(NARANJA, 1).move_to([2.0, 0.8, 0])
        lb = T("esfera", 36, TINTA, "HEAVY").move_to([-2.0, -1.0, 0])
        lp = T("placa plana", 36, TINTA, "HEAVY").move_to([2.0, -1.0, 0])
        self.play(FadeIn(bola), FadeIn(placa), FadeIn(lb), FadeIn(lp), run_time=0.5)
        ang = ValueTracker(0.0)
        placa.add_updater(lambda m: m.stretch_to_fit_width(max(0.06, 2.2 * abs(np.cos(ang.get_value())))).move_to([2.0, 0.8, 0]))
        self.frac(0.15)
        self.play(ang.animate.set_value(PI / 2), Rotate(bola[1], PI, about_point=bola.get_center()), run_time=1.8)
        ok = VGroup(check(VERDE_OK, 0.3), T("igual desde cualquier ángulo", 32, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -2.6, 0])
        no = VGroup(equis(ROJO, 0.3), T("de canto casi desaparece", 32, ROJO, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -3.5, 0])
        self.play(FadeIn(ok, shift=UP * 0.2), run_time=0.35)
        self.frac(0.3)
        self.play(FadeIn(no, shift=UP * 0.2), run_time=0.35)
        self.cerrar_voz(0.15)
        placa.clear_updaters()
        self.limpiar(bola, placa, lb, lp, ok, no)

        # p5: desviadores de aves
        self.voz("p5")
        cab3 = linea_aerea([-4.4, 1.8, 0], [4.4, 1.8, 0], 0.4, "#C7CCD6", 5)
        self.play(Create(cab3), run_time=0.4)
        espiral = VGroup(*[onda(lambda x: np.sin(x * 22), -0.6, 0.6, 0, 0.16, AMAR_FR, 6).move_to(cab3.point_from_proportion(t)) for t in (0.25, 0.75)])
        placa_a = VGroup(Line(ORIGIN, DOWN * 0.4).set_stroke("#5B6573", 3),
                         RoundedRectangle(width=0.35, height=0.6, corner_radius=0.06, stroke_width=0).set_fill(NARANJA, 1).shift(DOWN * 0.7)).move_to(cab3.point_from_proportion(0.5) + DOWN * 0.45)
        self.play(FadeIn(espiral), FadeIn(placa_a), run_time=0.5)
        self.play(Rotate(placa_a[1], PI / 6, about_point=placa_a[0].get_end()), run_time=0.4, rate_func=there_and_back)
        aves = VGroup(*[pajarito().scale(0.7).move_to([x, -1.2 + 0.4 * k, 0]) for k, x in enumerate((-2.6, 2.4))])
        self.frac(0.1)
        self.play(FadeIn(aves[0], shift=RIGHT * 0.5), FadeIn(aves[1], shift=LEFT * 0.5), run_time=0.6)
        des = caja_dato("desviadores de aves", "espirales y placas: para que las aves vean el cable", VERDE_OK, 7.0, 26).move_to([0, -3.4, 0])
        self.play(FadeIn(des, shift=UP * 0.2), run_time=0.4)
        self.frac(0.35)
        conc = pastilla("bolas = aviso para pilotos", NARANJA, 38, True).move_to([0, 3.4, 0])
        self.play(FadeIn(conc, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(cab3, espiral, placa_a, aves, des, conc)
        self.final("Bolas de colores: avisan a los pilotos")


# ====================================================================== V04 · zumbido del transformador
class V04C(ShortC):
    CLAVE = "v04c"

    def cuerpo(self):
        self.voz("gancho")
        pg, _ = poste(9.0, 2.6, 2)
        pg.move_to([-1.0, -0.9, 0])
        tr = transformador().scale(1.2).move_to([0.6, 0.1, 0])
        self.play(FadeIn(pg), FadeIn(tr, shift=LEFT * 0.2), run_time=0.6)
        ond = ondas_sonido(tr.get_right() + RIGHT * 0.1, 4, 0.5, 0.45, PI / 2, CIAN, 0.0)
        self.play(LaggedStart(*[Create(o) for o in ond], lag_ratio=0.2), run_time=0.8)
        self.play(Wiggle(tr, scale_value=1.02, rotation_angle=0.01, n_wiggles=8), run_time=1.0)
        hz = VGroup(T("bzzzz…", 60, CIAN, "HEAVY"), T("¿por qué?", 54, TINTA, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0.6, -4.2, 0])
        self.play(FadeIn(hz, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(pg, tr, ond, hz)

        # p0: dos bobinas sobre el mismo núcleo
        self.voz("p0")
        nuc = VGroup(Rectangle(width=5.2, height=4.4, stroke_width=0).set_fill("#8C96A3", 1),
                     Rectangle(width=2.6, height=2.0, stroke_width=0).set_fill(FONDO, 1)).move_to([0, 0.6, 0])
        bob1 = VGroup(*[RoundedRectangle(width=1.4, height=0.18, corner_radius=0.08, stroke_color="#7A3B12", stroke_width=1).set_fill(COBRE_V, 1)
                        .move_to([-1.95, 1.5 - 0.22 * k, 0]) for k in range(9)])
        bob2 = VGroup(*[RoundedRectangle(width=1.6, height=0.32, corner_radius=0.1, stroke_color="#7A3B12", stroke_width=1).set_fill(COBRE_V, 1)
                        .move_to([1.95, 1.2 - 0.4 * k, 0]) for k in range(4)])
        self.play(FadeIn(nuc), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b) for b in bob1], lag_ratio=0.05), LaggedStart(*[FadeIn(b) for b in bob2], lag_ratio=0.1), run_time=0.8)
        l1 = T("línea de\ndistribución", 30, TINTA, "BOLD").move_to([-2.6, -2.3, 0])
        l2 = T("120 / 240 V", 40, VERDE_OK, "HEAVY").move_to([2.2, -2.3, 0])
        fl = Arrow([-1.0, -2.3, 0], [0.6, -2.3, 0], buff=0, color=AMBAR, stroke_width=6)
        self.frac(0.1)
        self.play(FadeIn(l1), GrowArrow(fl), FadeIn(l2), run_time=0.6)
        nl = T("núcleo de acero", 30, CLARO, "HEAVY").move_to([0, 3.15, 0])
        self.play(FadeIn(nl), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(bob1, bob2, l1, l2, fl, nl)

        # p1: dominios que se alinean → magnetostricción
        self.voz("p1")
        self.play(nuc.animate.scale(0.7).move_to([0, 2.2, 0]), run_time=0.4)
        rng = np.random.default_rng(5)
        marco = RoundedRectangle(width=7.4, height=3.6, corner_radius=0.2, stroke_color=CLARO, stroke_width=2).move_to([0, -1.9, 0])
        flechas = VGroup()
        for x in np.linspace(-3.0, 3.0, 7):
            for y in np.linspace(-3.2, -0.6, 4):
                a = rng.uniform(0, TAU)
                f = Arrow(ORIGIN, 0.6 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=AMBAR, stroke_width=4, tip_length=0.15, max_stroke_width_to_length_ratio=10)
                f.move_to([x, y, 0])
                f.ang0 = a
                flechas.add(f)
        dom = T("dominios magnéticos", 28, CLARO, "BOLD").next_to(marco, DOWN, buff=0.15)
        self.play(Create(marco), FadeIn(flechas), FadeIn(dom), run_time=0.6)
        self.frac(0.15)
        self.play(*[Rotate(f, -f.ang0) for f in flechas], run_time=1.2)
        self.play(marco.animate.stretch(1.06, 0), nuc.animate.stretch(1.06, 0), run_time=0.4)
        mg = VGroup(T("magnetostricción", 50, MARCA, "HEAVY"), T("el acero cambia de tamaño (exagerado)", 26, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, -5.2, 0])
        self.play(FadeIn(mg, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(nuc, marco, flechas, dom, mg)

        # p2: 60 Hz → 120 Hz
        self.voz("p2")
        ax1 = Line([-4.0, 2.0, 0], [4.0, 2.0, 0]).set_stroke(CLARO, 2)
        ax2 = Line([-4.0, -1.8, 0], [4.0, -1.8, 0]).set_stroke(CLARO, 2)
        cur = onda(lambda x: np.sin(x * PI / 2), -4.0, 4.0, 2.0, 1.2, CIAN, 5)
        est = onda(lambda x: np.sin(x * PI / 2) ** 2, -4.0, 4.0, -1.8, 1.4, NARANJA, 5)
        t1 = T("corriente · 60 Hz", 32, CIAN, "HEAVY").move_to([0, 3.7, 0])
        t2 = T("estiramiento del acero · 120 Hz", 32, NARANJA, "HEAVY").move_to([0, 0.3, 0])
        self.play(Create(ax1), Create(cur), FadeIn(t1), run_time=0.9)
        self.frac(0.2)
        self.play(Create(ax2), Create(est), FadeIn(t2), run_time=0.9)
        picos = VGroup(*[Dot([x, -1.8 + 1.4, 0], radius=0.12, color=AMBAR) for x in (-3, -1, 1, 3)])
        self.play(LaggedStart(*[FadeIn(p, scale=2) for p in picos], lag_ratio=0.2), run_time=0.7)
        x2 = pastilla("un estirón en cada medio ciclo → ×2", NARANJA, 32, True).move_to([0, -4.4, 0])
        self.play(FadeIn(x2), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(ax1, ax2, cur, est, t1, t2, picos, x2)

        # p3: 120 Hz vs 100 Hz
        self.voz("p3")
        tr = transformador().scale(1.1).move_to([0, 1.8, 0])
        self.play(FadeIn(tr), run_time=0.3)
        ond = VGroup(ondas_sonido(tr.get_left() + LEFT * 0.1, 3, 0.5, 0.4, PI / 2, CIAN, PI), ondas_sonido(tr.get_right() + RIGHT * 0.1, 3, 0.5, 0.4, PI / 2, CIAN, 0))
        self.play(LaggedStart(*[Create(o) for o in ond], lag_ratio=0.1), run_time=0.7)
        f1 = VGroup(T("red de 60 Hz", 34, TINTA, "BOLD"), T("120 Hz", 64, CIAN, "HEAVY")).arrange(DOWN, buff=0.08).move_to([-2.2, -2.0, 0])
        f2 = VGroup(T("red de 50 Hz", 34, TINTA, "BOLD"), T("100 Hz", 64, AMBAR, "HEAVY")).arrange(DOWN, buff=0.08).move_to([2.2, -2.0, 0])
        self.play(FadeIn(f1, shift=UP * 0.2), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(f2, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(tr, ond, f1, f2)

        # p4: núcleo laminado vs sólido (corrientes parásitas)
        self.voz("p4")
        sol = Rectangle(width=3.4, height=3.4, stroke_color="#5B6573", stroke_width=3).set_fill("#8C96A3", 1).move_to([-2.1, 0.6, 0])
        lam = VGroup(*[Rectangle(width=3.4, height=0.3, stroke_color="#3A4250", stroke_width=1.5).set_fill("#A7B0BC", 1) for _ in range(10)]).arrange(DOWN, buff=0.04).move_to([2.1, 0.6, 0])
        ls = T("bloque sólido", 32, TINTA, "HEAVY").next_to(sol, DOWN, buff=0.2)
        ll_ = T("láminas aisladas", 32, TINTA, "HEAVY").next_to(lam, DOWN, buff=0.2).align_to(ls, UP)
        self.play(FadeIn(sol), FadeIn(lam), FadeIn(ls), FadeIn(ll_), run_time=0.5)
        rem1 = VGroup(*[Circle(radius=r).set_stroke(ROJO, 5).move_to(sol) for r in (0.5, 1.0, 1.45)])
        rem2 = VGroup(*[Ellipse(width=2.8, height=0.14).set_stroke(ROJO, 2.5).move_to(l) for l in lam])
        self.frac(0.2)
        self.play(LaggedStart(*[Create(r) for r in rem1], lag_ratio=0.2), run_time=0.7)
        gl = resplandor(sol.get_center(), 2.4, CALOR, 10, 0.05)
        self.play(FadeIn(gl), run_time=0.3)
        self.frac(0.15)
        self.play(LaggedStart(*[Create(r) for r in rem2], lag_ratio=0.05), run_time=0.7)
        res = VGroup(pastilla("corrientes parásitas grandes", ROJO, 30, True).move_to([-2.1, -2.6, 0]),
                     pastilla("mucho menos calor", VERDE_OK, 30, True).move_to([2.1, -2.6, 0]))
        for r in res:
            if r.width > 4.1:
                r.scale_to_fit_width(4.1)
        self.play(FadeIn(res), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(sol, lam, ls, ll_, rem1, rem2, gl, res)

        # p4b: zumbido según voltaje
        self.voz("p4b")
        perilla = VGroup(Circle(radius=1.1, stroke_color=CLARO, stroke_width=4).set_fill("#16294F", 1),
                         Line(ORIGIN, UP * 0.9).set_stroke(AMBAR, 8)).move_to([-2.0, 1.2, 0])
        lv = T("voltaje", 34, AMBAR, "HEAVY").next_to(perilla, DOWN, buff=0.2)
        barra_m = Rectangle(width=1.0, height=0.3, stroke_width=0).set_fill(CIAN, 1).move_to([2.0, -0.3, 0], aligned_edge=DOWN)
        marco_b = Rectangle(width=1.2, height=3.4, stroke_color=CLARO, stroke_width=2).move_to([2.0, 1.4, 0])
        lb = T("magnetización", 30, CIAN, "HEAVY").next_to(marco_b, DOWN, buff=0.2)
        self.play(FadeIn(perilla), FadeIn(lv), FadeIn(marco_b), FadeIn(barra_m), FadeIn(lb), run_time=0.5)
        self.frac(0.05)
        self.play(Rotate(perilla[1], -PI * 0.7, about_point=perilla[0].get_center()), barra_m.animate.stretch_to_fit_height(3.2, about_edge=DOWN), run_time=1.2)
        z = T("más voltaje → más zumbido del núcleo", 32, TINTA, "HEAVY").move_to([0, -2.4, 0])
        self.play(FadeIn(z), run_time=0.3)
        self.frac(0.3)
        cg = caja_dato("con mucha carga", "las bobinas también vibran un poco", NARANJA, 6.4, 28).move_to([0, -3.9, 0])
        self.play(FadeIn(cg, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(perilla, lv, barra_m, marco_b, lb, z, cg)

        # p5: normal vs peligro
        self.voz("p5")
        a = VGroup(transformador().scale(0.8), ondas_sonido(ORIGIN, 2, 0.4, 0.35, PI / 2, CIAN, 0).shift(RIGHT * 1.0)).move_to([-2.2, 1.6, 0])
        b = transformador().scale(0.8).move_to([2.2, 1.6, 0])
        ch = VGroup(*[rayo(b.get_top() + LEFT * 0.3, b.get_top() + UP * 0.9 + RIGHT * 0.2 * k, semilla=k) for k in range(2)])
        gota = VMobject().set_points_smoothly([b.get_bottom() + RIGHT * 0.3, b.get_bottom() + RIGHT * 0.38 + DOWN * 0.3, b.get_bottom() + RIGHT * 0.3 + DOWN * 0.45,
                                               b.get_bottom() + RIGHT * 0.22 + DOWN * 0.3, b.get_bottom() + RIGHT * 0.3]).set_fill("#B08B2E", 1).set_stroke(width=0)
        la = VGroup(check(VERDE_OK, 0.32), T("zumbido parejo:\nnormal", 30, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.15).next_to(a, DOWN, buff=0.3)
        lb2 = VGroup(equis(ROJO, 0.32), T("chasquidos,\nchispas, aceite", 30, ROJO, "HEAVY")).arrange(DOWN, buff=0.15).next_to(b, DOWN, buff=0.3)
        self.play(FadeIn(a), FadeIn(la), run_time=0.5)
        self.frac(0.2)
        self.play(FadeIn(b), FadeIn(ch), FadeIn(gota, shift=DOWN * 0.2), FadeIn(lb2), run_time=0.6)
        rep = pastilla("aléjate y repórtalo a la empresa eléctrica", ROJO, 32, True).move_to([0, -3.6, 0])
        self.play(FadeIn(rep, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(a, b, ch, gota, la, lb2, rep)
        self.final("El zumbido: el acero vibra a 120 Hz")


# ====================================================================== V05 · polaridad
class V05C(ShortC):
    CLAVE = "v05c"

    def cuerpo(self):
        self.voz("gancho")
        tm = cara(10.0).move_to([0, 0.3, 0])
        self.play(FadeIn(tm, scale=0.9), run_time=0.5)
        c1 = VGroup(DoubleArrow(tm.fa.get_bottom() + RIGHT * 0.5, tm.fa.get_top() + RIGHT * 0.5, buff=0, color=AMBAR, stroke_width=4, tip_length=0.18),
                    T("corta", 30, AMBAR, "HEAVY").next_to(tm.fa, RIGHT, buff=0.75))
        c2 = VGroup(DoubleArrow(tm.ne.get_bottom() + LEFT * 0.5, tm.ne.get_top() + LEFT * 0.5, buff=0, color=CIAN, stroke_width=4, tip_length=0.18),
                    T("larga", 30, CIAN, "HEAVY").next_to(tm.ne, LEFT, buff=0.75))
        self.frac(0.15)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        pol = pastilla("POLARIDAD", MARCA, 48, True).move_to([0, -3.8, 0])
        self.frac(0.35)
        self.play(FadeIn(pol, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(c1, c2, pol)

        # p1: fase / neutro / tierra y el puente neutro-tierra en el tablero
        self.voz("p1")
        self.play(tm.animate.scale(0.55).move_to([-2.2, 2.0, 0]), run_time=0.5)
        e_f = pastilla("fase: 120 V", NEGRO_BK, 30, True).move_to([1.6, 2.9, 0])
        e_n = pastilla("neutro: ≈ 0 V a tierra", "#ECECEC", 30, True).move_to([1.6, 2.0, 0])
        e_t = pastilla("tierra", VERDE_T, 30, True).move_to([1.6, 1.1, 0])
        cf = Line(tm.fa.get_center(), e_f.get_left()).set_stroke(TINTA, 2)
        self.play(FadeIn(e_f), Create(cf), run_time=0.4)
        self.frac(0.15)
        self.play(FadeIn(e_n), run_time=0.4)
        tab = RoundedRectangle(width=3.2, height=3.0, corner_radius=0.15, stroke_color=METAL_OSC, stroke_width=3).set_fill("#C9CED6", 1).move_to([0, -2.6, 0])
        bn = Rectangle(width=2.4, height=0.25, stroke_width=0).set_fill("#E8E8E8", 1).move_to([0, -2.1, 0])
        bt = Rectangle(width=2.4, height=0.25, stroke_width=0).set_fill(VERDE_T, 1).move_to([0, -3.3, 0])
        puente = Line([1.0, -2.1, 0], [1.0, -3.3, 0]).set_stroke(COBRE_V, 10)
        ln_ = T("N", 28, "#1D2939", "HEAVY").move_to([-1.5, -2.1, 0]); lt_ = T("T", 28, "#1D2939", "HEAVY").move_to([-1.5, -3.3, 0])
        self.frac(0.1)
        self.play(FadeIn(tab), FadeIn(bn), FadeIn(bt), FadeIn(ln_), FadeIn(lt_), run_time=0.5)
        self.play(Create(puente), Flash(puente.get_center(), color=AMBAR), run_time=0.5)
        un = T("se unen en un solo punto: el tablero principal", 28, TINTA, "HEAVY").move_to([0, -4.7, 0])
        self.play(FadeIn(un), run_time=0.3)
        self.frac(0.3)
        lleva = pastilla("el neutro LLEVA corriente: no es tierra", AMBAR, 30, True).move_to([0, -5.6, 0])
        self.play(FadeIn(lleva), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(tm, e_f, e_n, cf, tab, bn, bt, puente, ln_, lt_, un, lleva)

        # p2: clavija polarizada solo entra de una forma + 200.10(B)
        self.voz("p2")
        tm = cara(6.0).move_to([0, 1.6, 0])
        cl = clavija("5-15P", polarizada=True).scale(2.4).move_to([0, -2.4, 0])
        self.play(FadeIn(tm), FadeIn(cl), run_time=0.4)
        self.play(cl.animate.flip(UP), run_time=0.5)
        self.play(cl.animate.shift(UP * 1.0), run_time=0.4)
        x_ = equis(ROJO, 0.5).move_to([2.6, 0.0, 0])
        self.play(FadeIn(x_, scale=1.4), cl.animate.shift(DOWN * 0.25), run_time=0.3)
        self.play(FadeOut(x_), cl.animate.shift(DOWN * 0.75).flip(UP), run_time=0.5)
        self.play(cl.animate.shift(UP * 1.0), run_time=0.4)
        ok = check(VERDE_OK, 0.5).move_to([2.6, 0.0, 0])
        self.play(FadeIn(ok, scale=1.4), run_time=0.3)
        nec = caja_dato("NEC · 200.10(B)", "terminal del neutro: blanco o plateado", MARCA, 6.4, 28).move_to([0, -5.0, 0])
        tor = VGroup(tornillo(0.42, "#D0D5DD"), tornillo(0.42, LATON)).arrange(RIGHT, buff=0.6).move_to([0, -3.4, 0])
        self.frac(0.2)
        self.play(FadeIn(nec, shift=UP * 0.2), FadeIn(tor), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(tm, cl, ok, nec, tor)

        # p3: portalámparas: neutro a la rosca (410.50)
        self.voz("p3")
        pl = rosca_portalamparas(1.7).move_to([-1.6, 0.6, 0])
        self.play(FadeIn(pl, shift=UP * 0.2), run_time=0.5)
        lr = VGroup(pastilla("rosca = NEUTRO", "#ECECEC", 32, True), pastilla("centro = FASE", NEGRO_BK, 32, True)).arrange(DOWN, buff=0.4).move_to([2.2, 0.6, 0])
        a1 = Arrow(lr[0].get_left(), pl.rosca.get_right(), buff=0.1, color=TINTA, stroke_width=4)
        a2 = Arrow(lr[1].get_left(), pl.centro.get_right(), buff=0.1, color=TINTA, stroke_width=4)
        self.frac(0.12)
        self.play(FadeIn(lr[1]), GrowArrow(a2), run_time=0.4)
        self.play(FadeIn(lr[0]), GrowArrow(a1), run_time=0.4)
        mano = VGroup(Circle(radius=0.35).set_fill(PIEL, 1).set_stroke("#9A6A4A", 2)).move_to(pl.rosca.get_left() + LEFT * 0.4)
        lt = T("la parte que podrías tocar", 30, TINTA, "HEAVY").move_to([0, -2.6, 0])
        self.frac(0.2)
        self.play(FadeIn(mano, shift=RIGHT * 0.3), FadeIn(lt), run_time=0.4)
        nec = caja_dato("NEC · 410.50", "el neutro va a la rosca", MARCA, 5.4, 28).move_to([0, -4.0, 0])
        self.play(FadeIn(nec), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(pl, lr, a1, a2, mano, lt, nec)

        # p4: el interruptor corta la fase (404.2(B))
        self.voz("p4")
        tit = caja_dato("NEC · 404.2(B)", "el interruptor no debe cortar el neutro", MARCA, 6.6, 28).move_to([0, 3.6, 0])
        self.play(FadeIn(tit), run_time=0.4)

        def circuito(y, en_fase, color_ok):
            fuente_ = VGroup(T("F", 30, TINTA, "HEAVY").move_to([-3.8, y + 0.6, 0]), T("N", 30, TINTA, "HEAVY").move_to([-3.8, y - 0.6, 0]))
            lf = Line([-3.5, y + 0.6, 0], [-1.2, y + 0.6, 0]).set_stroke(NEGRO_BK if True else ROJO, 6)
            ln = Line([-3.5, y - 0.6, 0], [2.4, y - 0.6, 0]).set_stroke("#ECECEC", 6)
            sw = interruptor_sw(False).move_to([-0.6, y + 0.6 if en_fase else y - 0.6, 0])
            lf2 = Line([0.0, y + 0.6, 0], [2.4, y + 0.6, 0]).set_stroke(NEGRO_BK, 6)
            foco = Circle(radius=0.45, stroke_color=CLARO, stroke_width=3).set_fill("#3A3F48", 1).move_to([2.8, y, 0])
            l1 = Line([2.4, y + 0.6, 0], [2.6, y + 0.35, 0]).set_stroke(NEGRO_BK, 6)
            l2 = Line([2.4, y - 0.6, 0], [2.6, y - 0.35, 0]).set_stroke("#ECECEC", 6)
            g = VGroup(fuente_, lf, ln, lf2, l1, l2, foco, sw)
            if not en_fase:
                ln.put_start_and_end_on([-3.5, y - 0.6, 0], [-1.2, y - 0.6, 0])
                lf.put_start_and_end_on([-3.5, y + 0.6, 0], [2.4, y + 0.6, 0])
                g.add(Line([0.0, y - 0.6, 0], [2.4, y - 0.6, 0]).set_stroke("#ECECEC", 6))
            g.foco = foco
            return g
        bien = circuito(1.0, True, VERDE_OK)
        mal = circuito(-2.6, False, ROJO)
        lb = VGroup(check(VERDE_OK, 0.3), T("corta la fase", 30, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, 2.3, 0])
        lm = VGroup(equis(ROJO, 0.3), T("cortara el neutro", 30, ROJO, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -1.3, 0])
        self.play(FadeIn(bien), FadeIn(lb), run_time=0.5)
        sin = T("rosca y foco sin tensión", 26, VERDE_OK, "BOLD").next_to(bien.foco, DOWN, buff=0.75).shift(LEFT * 1.0)
        self.play(FadeIn(sin), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(mal), FadeIn(lm), run_time=0.5)
        glow = resplandor(mal.foco.get_center(), 0.9, ROJO, 8, 0.1)
        ct = T("apagado… pero CON tensión", 28, ROJO, "HEAVY").move_to([0, -4.3, 0])
        self.play(FadeIn(glow), FadeIn(ct), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(tit, bien, mal, lb, lm, sin, glow, ct)

        # p5: no forzar; probador de tomacorrientes
        self.voz("p5")
        cl = clavija("5-15P", polarizada=True).scale(2.0).move_to([-1.2, 1.0, 0])
        lima = VGroup(Rectangle(width=1.6, height=0.25, stroke_width=0).set_fill("#5B6573", 1), *[Line([x, -0.12, 0], [x + 0.1, 0.12, 0]).set_stroke("#3A4250", 2) for x in np.arange(-0.7, 0.7, 0.15)]).move_to(cl.get_top() + UP * 0.2 + RIGHT * 0.6).rotate(0.4)
        x_ = equis(ROJO, 0.45).next_to(cl, RIGHT, buff=0.4)
        self.play(FadeIn(cl), FadeIn(lima), run_time=0.4)
        self.play(lima.animate.shift(RIGHT * 0.3), run_time=0.3, rate_func=there_and_back)
        self.play(FadeIn(x_, scale=1.4), run_time=0.3)
        nf = T("nunca la fuerces ni la limes", 36, ROJO, "HEAVY").move_to([0, -1.5, 0])
        self.play(FadeIn(nf), run_time=0.3)
        self.frac(0.35)
        pr = probador().scale(1.6).move_to([0, -3.3, 0])
        self.play(FadeIn(pr, shift=UP * 0.2), run_time=0.4)
        self.play(*[l.animate.set_fill(c, 1) for l, c in zip(pr.luces, (AMBAR, AMBAR, ROJO))], run_time=0.4)
        lp = T("sus luces te dicen si la polaridad está invertida", 26, TINTA, "BOLD").move_to([0, -5.0, 0])
        self.play(FadeIn(lp), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cl, lima, x_, nf, pr, lp)
        self.final("Ranura corta = fase · larga = neutro")


# ====================================================================== V06 · pata de tierra más larga
def clavija_lado(s=1.0):
    """Clavija vista de lado: cuerpo, patas planas (fase y neutro) y pata redonda de tierra más larga."""
    cuerpo = RoundedRectangle(width=1.6, height=1.2, corner_radius=0.2, stroke_color="#8F9AC8", stroke_width=2).set_fill("#2A2E35", 1)
    plana = Rectangle(width=1.1, height=0.16, stroke_color=METAL_OSC, stroke_width=1.5).set_fill("#C9CED6", 1).next_to(cuerpo, RIGHT, buff=0).shift(UP * 0.28)
    tierra = Rectangle(width=1.45, height=0.2, stroke_color=METAL_OSC, stroke_width=1.5).set_fill("#B8BEC8", 1).next_to(cuerpo, RIGHT, buff=0).shift(DOWN * 0.28)
    cordon = Line(cuerpo.get_left(), cuerpo.get_left() + LEFT * 2.0).set_stroke(NEGRO_BK, 18)
    g = VGroup(cordon, cuerpo, plana, tierra).scale(s)
    g.plana, g.tierra = plana, tierra
    return g


class V06C(ShortC):
    CLAVE = "v06c"

    def cuerpo(self):
        self.voz("gancho")
        cl = clavija_lado(1.6).move_to([-0.4, 0.8, 0])
        self.play(FadeIn(cl, shift=RIGHT * 0.3), run_time=0.5)
        dif = VGroup(DashedLine(cl.plana.get_right() + UP * 0.6, cl.plana.get_right() + DOWN * 1.8, color=AMBAR),
                     DashedLine(cl.tierra.get_right() + UP * 1.1, cl.tierra.get_right() + DOWN * 0.8, color=VERDE_OK))
        self.frac(0.15)
        self.play(Create(dif), Indicate(cl.tierra, color=VERDE_OK), run_time=0.7)
        lt = T("más larga", 44, VERDE_OK, "HEAVY").next_to(cl.tierra, DOWN, buff=0.7)
        self.play(FadeIn(lt), run_time=0.3)
        pr = pastilla("diseñada para protegerte", MARCA, 40, True).move_to([0, -3.4, 0])
        self.frac(0.3)
        self.play(FadeIn(pr, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(cl, dif, lt, pr)

        # p1: la tierra une el metal del aparato con el tablero
        self.voz("p1")
        ap = VGroup(RoundedRectangle(width=2.6, height=2.0, corner_radius=0.15, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1),
                    T("carcasa metálica", 22, "#1D2939", "HEAVY")).move_to([-2.2, 2.4, 0])
        tab = RoundedRectangle(width=1.6, height=2.2, corner_radius=0.12, stroke_color=METAL_OSC, stroke_width=3).set_fill("#C9CED6", 1).move_to([2.6, -1.4, 0])
        bt = Rectangle(width=1.1, height=0.2, stroke_width=0).set_fill(VERDE_T, 1).move_to(tab.get_bottom() + UP * 0.4)
        lt_ = T("tablero", 26, CLARO, "BOLD").next_to(tab, UP, buff=0.1)
        verde = VMobject().set_points_as_corners([ap.get_bottom(), ap.get_bottom() + DOWN * 1.5, [0.4, 0.9, 0], [0.4, -3.4, 0], [2.6, -3.4, 0], bt.get_bottom()]).set_stroke(VERDE_T, 12)
        tm = cara(2.6).move_to([0.4, -0.8, 0])
        self.play(FadeIn(ap), FadeIn(tab), FadeIn(bt), FadeIn(lt_), run_time=0.5)
        self.play(Create(verde), FadeIn(tm), run_time=1.0)
        self.play(Indicate(tm.ti, color=VERDE_OK, scale_factor=1.6), run_time=0.5)
        tv = pastilla("al tornillo verde", VERDE_T, 32, True).move_to([-1.8, -2.0, 0])
        self.frac(0.3)
        self.play(FadeIn(tv), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ap, tab, bt, lt_, verde, tm, tv)

        # p2–p3: animación de enchufar y desenchufar (corte lateral)
        rec = VGroup(RoundedRectangle(width=2.4, height=3.0, corner_radius=0.12, stroke_color="#C7C5BE", stroke_width=3).set_fill("#F7F7F5", 1))
        rec.move_to([2.4, 0.6, 0])
        cont_p = Rectangle(width=1.2, height=0.3, stroke_color=LATON, stroke_width=3).move_to([2.2, 0.6 + 0.56, 0])
        cont_t = Rectangle(width=1.2, height=0.34, stroke_color=VERDE_T, stroke_width=3).move_to([2.2, 0.6 - 0.56, 0])
        cl = clavija_lado(2.0).move_to([-2.2, 0.6, 0])
        self.voz("p2")
        self.play(FadeIn(rec), FadeIn(cont_p), FadeIn(cont_t), FadeIn(cl), run_time=0.5)
        dx_t = cont_t.get_left()[0] - cl.tierra.get_right()[0] + 0.1
        self.play(cl.animate.shift(RIGHT * dx_t), run_time=1.0)
        f1 = Flash(cl.tierra.get_right(), color=VERDE_OK, flash_radius=0.4)
        n1 = VGroup(pastilla("1 · TIERRA conecta", VERDE_T, 34, True)).move_to([0, -2.4, 0])
        self.play(f1, FadeIn(n1), cont_t.animate.set_fill(VERDE_T, 0.6), run_time=0.5)
        self.frac(0.2)
        dx_p = cont_p.get_left()[0] - cl.plana.get_right()[0] + 0.1
        self.play(cl.animate.shift(RIGHT * dx_p), run_time=0.6)
        n2 = pastilla("2 · fase y neutro conectan", AMBAR, 34, True).move_to([0, -3.4, 0])
        self.play(Flash(cl.plana.get_right(), color=AMBAR, flash_radius=0.4), FadeIn(n2), cont_p.animate.set_fill(LATON, 0.6), run_time=0.5)
        ya = T("el aparato ya estaba aterrizado", 30, VERDE_OK, "HEAVY").move_to([0, -4.4, 0])
        self.play(FadeIn(ya), run_time=0.3)
        self.cerrar_voz(0.15)
        self.play(FadeOut(n1), FadeOut(n2), FadeOut(ya), run_time=0.3)

        self.voz("p3")
        self.play(cl.animate.shift(LEFT * dx_p), cont_p.animate.set_fill(opacity=0), run_time=0.8)
        m1 = pastilla("1 · fase y neutro se separan", AMBAR, 34, True).move_to([0, -2.4, 0])
        self.play(FadeIn(m1), run_time=0.3)
        self.frac(0.25)
        self.play(cl.animate.shift(LEFT * (dx_t + 0.4)), cont_t.animate.set_fill(opacity=0), run_time=0.8)
        m2 = pastilla("2 · la TIERRA se suelta de último", VERDE_T, 34, True).move_to([0, -3.4, 0])
        self.play(FadeIn(m2), run_time=0.3)
        nunca = T("nunca con tensión y sin tierra", 32, VERDE_OK, "HEAVY").move_to([0, -4.4, 0])
        self.frac(0.3)
        self.play(FadeIn(nunca), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(rec, cont_p, cont_t, cl, m1, m2, nunca)

        # p3b: falla → la tierra se lleva la corriente y el breaker dispara
        self.voz("p3b")
        ap = RoundedRectangle(width=3.0, height=2.2, corner_radius=0.15, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1).move_to([-1.8, 2.0, 0])
        tab = RoundedRectangle(width=1.8, height=2.6, corner_radius=0.12, stroke_color=METAL_OSC, stroke_width=3).set_fill("#C9CED6", 1).move_to([2.6, -1.6, 0])
        brk = breaker("20", lado=1).scale(2.6).move_to(tab.get_center() + UP * 0.5)
        fase = VMobject().set_points_as_corners([brk.get_right() + RIGHT * 0.1, [3.8, -0.6, 0], [3.8, 3.6, 0], [-1.0, 3.6, 0], [-1.0, ap.get_top()[1] - 0.3, 0]]).set_stroke(NEGRO_BK, 8)
        fase_b = fase.copy().set_stroke("#8F9AC8", 12)
        verde = VMobject().set_points_as_corners([ap.get_bottom(), [-1.8, -3.0, 0], [2.6, -3.0, 0], tab.get_bottom()]).set_stroke(VERDE_T, 10)
        self.play(FadeIn(ap), FadeIn(tab), FadeIn(brk), Create(fase_b), Create(fase), Create(verde), run_time=0.7)
        ch = rayo([-1.0, ap.get_top()[1] - 0.3, 0], [-1.6, ap.get_center()[1], 0], semilla=2)
        self.sfx("pop", -8)
        self.play(FadeIn(ch), Flash([-1.2, 2.4, 0], color=AMBAR), run_time=0.4)
        cf = corriente([brk.get_right() + RIGHT * 0.1, [3.8, -0.6, 0], [3.8, 3.6, 0], [-1.0, 3.6, 0], [-1.0, ap.get_top()[1] - 0.3, 0], [-1.6, ap.get_center()[1], 0],
                        ap.get_bottom(), [-1.8, -3.0, 0], [2.6, -3.0, 0], tab.get_bottom()], vel=2.4, escala=1.5, color=ROJO)
        self.add(cf)
        self.frac(0.35)
        self.sfx("tic", -4)
        self.play(mover_palanca(brk, False), run_time=0.25)
        self.remove(cf)
        ok = VGroup(check(VERDE_OK, 0.32), T("breaker dispara · carcasa segura", 30, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -4.4, 0])
        self.play(FadeOut(ch), FadeIn(ok), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ap, tab, brk, fase, fase_b, verde, ok)

        # p4: NEC 250.124(A)
        self.voz("p4")
        tt = caja_dato("NEC · 250.124(A)", "first-make, last-break", VERDE_OK, 5.6, 30).move_to([0, 3.0, 0])
        self.play(FadeIn(tt, scale=1.05), run_time=0.4)
        lin = Line([-3.6, 0, 0], [3.6, 0, 0]).set_stroke(CLARO, 3)
        e1 = VGroup(Dot([-2.4, 0, 0], radius=0.16, color=VERDE_OK), T("conecta PRIMERO", 34, VERDE_OK, "HEAVY").move_to([-2.0, 0.8, 0]))
        e2 = VGroup(Dot([2.4, 0, 0], radius=0.16, color=VERDE_OK), T("desconecta de ÚLTIMO", 34, VERDE_OK, "HEAVY").move_to([1.2, -0.8, 0]))
        self.frac(0.15)
        self.play(Create(lin), FadeIn(e1), run_time=0.6)
        self.frac(0.15)
        self.play(FadeIn(e2), run_time=0.4)
        ap_ = T("clavijas y tomacorrientes", 32, TINTA, "BOLD").move_to([0, -2.6, 0])
        self.play(FadeIn(ap_), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(tt, lin, e1, e2, ap_)

        # p5: no cortar la pata
        self.voz("p5")
        cl = clavija_lado(1.6).move_to([-0.8, 2.4, 0])
        tij = VGroup(Line([-0.5, 0.3, 0], [0.5, -0.3, 0]).set_stroke("#C7CCD6", 8), Line([-0.5, -0.3, 0], [0.5, 0.3, 0]).set_stroke("#C7CCD6", 8),
                     Circle(radius=0.2).set_stroke(ROJO, 5).move_to([-0.7, 0.4, 0]), Circle(radius=0.2).set_stroke(ROJO, 5).move_to([-0.7, -0.4, 0])).move_to(cl.tierra.get_right() + RIGHT * 0.2)
        self.play(FadeIn(cl), FadeIn(tij), run_time=0.4)
        x1 = equis(ROJO, 0.45).next_to(cl, DOWN, buff=0.2).shift(RIGHT * 1.0)
        self.play(FadeIn(x1, scale=1.4), run_time=0.3)
        n1 = T("cortarla te quita la protección", 32, ROJO, "HEAVY").move_to([0, 0.2, 0])
        self.play(FadeIn(n1), run_time=0.3)
        self.frac(0.25)
        adap = VGroup(RoundedRectangle(width=1.4, height=1.0, corner_radius=0.15, stroke_color="#C7C5BE", stroke_width=2).set_fill("#F7F7F5", 1),
                      Line([0.5, -0.3, 0], [1.3, -0.9, 0]).set_stroke(VERDE_T, 4)).move_to([-2.0, -2.0, 0])
        xa = equis(ROJO, 0.4).next_to(adap, RIGHT, buff=0.3)
        bien = VGroup(cara(3.0), check(VERDE_OK, 0.4)).arrange(RIGHT, buff=0.3).move_to([2.0, -2.0, 0])
        self.play(FadeIn(adap), FadeIn(xa), run_time=0.4)
        self.frac(0.2)
        self.play(FadeIn(bien, shift=UP * 0.2), run_time=0.4)
        sol = pastilla("instala un tomacorriente con tierra", VERDE_OK, 32, True).move_to([0, -4.2, 0])
        self.play(FadeIn(sol), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cl, tij, x1, n1, adap, xa, bien, sol)
        self.final("La tierra: primero conecta, último desconecta")


# ====================================================================== V07 · toque en la ducha
class V07C(ShortC):
    CLAVE = "v07c"

    def cuerpo(self):
        self.voz("gancho")
        az = azulejos(8.6, 9.6, np.array([0, -0.6, 0]))
        du = ducha().scale(1.7).move_to([0.6, 2.2, 0])
        gt = VGroup(*[gotas(du[2].get_center() + DOWN * (0.7 + 0.5 * k), 9, "#7FD1FF").scale(1.6) for k in range(4)])
        self.play(FadeIn(az), FadeIn(du), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.3) for g in gt], lag_ratio=0.2), run_time=0.6)
        mano = VGroup(Circle(radius=0.4).set_fill(PIEL, 1).set_stroke("#9A6A4A", 2), Line([0, -0.4, 0], [-1.6, -2.4, 0]).set_stroke(PIEL, 26)).move_to([-1.0, 0.8, 0])
        self.play(FadeIn(mano, shift=RIGHT * 0.4), run_time=0.4)
        zap = VGroup(*[rayo(mano[0].get_center(), du.get_left() + RIGHT * 0.3, semilla=k) for k in range(2)])
        self.sfx("pop", -6)
        self.play(FadeIn(zap), Flash(mano[0].get_center(), color=AMBAR, flash_radius=0.6), run_time=0.4)
        nn = pastilla("no es normal", ROJO, 46, True).move_to([0, -4.0, 0])
        self.play(FadeIn(nn, scale=1.2), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(az, du, gt, mano, zap, nn)

        # p1: corte de la ducha: resistencia en agua + circuito exclusivo
        self.voz("p1")
        cam = RoundedRectangle(width=4.6, height=3.0, corner_radius=0.4, stroke_color="#98A2B3", stroke_width=3).set_fill("#1E5B8A", 0.8).move_to([0, 2.0, 0])
        coil = onda(lambda x: np.sin(x * 9), -1.8, 1.8, 2.0, 0.35, COBRE_V, 7)
        lc = T("resistencia en el agua", 30, TINTA, "HEAVY").next_to(cam, UP, buff=0.15)
        self.play(FadeIn(cam), Create(coil), FadeIn(lc), run_time=0.8)
        ais = coil.copy().set_stroke("#E8E8E8", 13, 0.35)
        la = T("solo la separa su aislamiento", 28, CLARO, "BOLD").next_to(cam, DOWN, buff=0.15)
        self.frac(0.1)
        self.play(FadeIn(ais), FadeIn(la), run_time=0.4)
        sel = VGroup(*[pastilla(t_, c_, 28, True) for t_, c_ in (("tibia", AMBAR), ("caliente", ROJO))]).arrange(RIGHT, buff=0.4).move_to([0, -0.4, 0])
        self.frac(0.12)
        self.play(FadeIn(sel), run_time=0.3)
        self.play(Indicate(sel[1], color=ROJO), coil.animate.set_stroke(CALOR), run_time=0.6)
        mas = T("más potencia → más corriente", 32, ROJO, "HEAVY").move_to([0, -1.4, 0])
        self.play(FadeIn(mas), run_time=0.3)
        brk = breaker("?", lado=1).scale(3.4).move_to([-3.0, -3.4, 0])
        cab = seccion(5.26, 0.6).move_to([-1.1, -3.4, 0])
        ex = caja_dato("circuito exclusivo", "calibre y breaker\nque indique el fabricante", MARCA, 3.6, 26).move_to([1.95, -3.4, 0])
        self.frac(0.15)
        self.play(FadeIn(brk), FadeIn(cab), FadeIn(ex), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(cam, coil, lc, ais, la, sel, mas, brk, cab, ex)

        # p2: sarro, aislamiento dañado, fuga
        self.voz("p2")
        cam = RoundedRectangle(width=6.0, height=3.4, corner_radius=0.4, stroke_color="#98A2B3", stroke_width=4).set_fill("#1E5B8A", 0.8).move_to([0, 1.4, 0])
        coil = onda(lambda x: np.sin(x * 7), -2.4, 2.4, 1.4, 0.45, COBRE_V, 8)
        self.play(FadeIn(cam), Create(coil), run_time=0.5)
        rng = np.random.default_rng(7)
        sarro = VGroup(*[Dot(coil.point_from_proportion(t) + np.array([0, rng.uniform(-0.12, 0.12), 0]), radius=rng.uniform(0.06, 0.13), color="#E8DFC8") for t in np.linspace(0.05, 0.95, 26)])
        self.play(LaggedStart(*[FadeIn(s, scale=0.4) for s in sarro], lag_ratio=0.03), run_time=0.8)
        ls = T("sarro + calor dañan el aislamiento", 30, TINTA, "HEAVY").move_to([0, 3.6, 0])
        self.play(FadeIn(ls), run_time=0.3)
        self.frac(0.15)
        fuga = corriente([coil.point_from_proportion(0.6), cam.get_bottom() + RIGHT * 0.6, [0.6, -1.6, 0], [0.6, -3.2, 0]], vel=1.2, escala=1.4, color=ROJO)
        self.add(fuga)
        sin_t = VGroup(equis(ROJO, 0.32), T("sin tierra: busca otro camino", 32, ROJO, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -0.6 - 3.0, 0])
        self.frac(0.15)
        self.play(FadeIn(sin_t), run_time=0.3)
        tu = pastilla("TU CUERPO", ROJO, 46, True).move_to([0, -4.8, 0])
        self.frac(0.25)
        self.play(FadeIn(tu, scale=1.2), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cam, coil, sarro, ls, fuga, sin_t, tu)

        # p3: piel mojada → 120 mA
        self.voz("p3")
        az = azulejos(8.6, 4.2, np.array([0, 2.2, 0]))
        pie = VGroup(*[Ellipse(width=0.9, height=1.6).set_fill(PIEL, 1).set_stroke("#9A6A4A", 2).move_to([x, 2.0, 0]) for x in (-0.7, 0.7)])
        gt = VGroup(*[gotas(np.array([x, 3.6, 0]), 7, "#7FD1FF") for x in (-1.8, 0, 1.8)])
        self.play(FadeIn(az), FadeIn(pie), FadeIn(gt), run_time=0.5)
        f = VGroup(T("120 V ÷ 1 000 Ω", 56, TINTA, "HEAVY"), T("= 120 mA", 76, ROJO, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0, -1.2, 0])
        self.frac(0.25)
        self.play(Write(f[0]), run_time=0.8)
        self.play(FadeIn(f[1], scale=1.2), run_time=0.4)
        cz = corazon(0.6).next_to(f[1], RIGHT, buff=0.3)
        fib = T("suficiente para la fibrilación", 32, ROJO, "HEAVY").move_to([0, -3.4, 0])
        self.play(FadeIn(cz, scale=0.5), FadeIn(fib), run_time=0.4)
        src = fuente("OSHA eTool · ejemplo con piel mojada", [0, -4.4, 0], 24)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(az, pie, gt, f, cz, fib, src)

        # p4: tierra → breaker dispara (250.110)
        self.voz("p4")
        du = ducha().scale(1.3).move_to([-2.2, 2.0, 0])
        tab = RoundedRectangle(width=1.8, height=2.6, corner_radius=0.12, stroke_color=METAL_OSC, stroke_width=3).set_fill("#C9CED6", 1).move_to([2.6, -1.0, 0])
        brk = breaker("40", lado=1).scale(2.6).move_to(tab.get_center() + UP * 0.5)
        verde = VMobject().set_points_as_corners([du.get_right(), [0.4, du.get_right()[1], 0], [0.4, -3.2, 0], [2.6, -3.2, 0], tab.get_bottom()]).set_stroke(VERDE_T, 12)
        self.play(FadeIn(du), FadeIn(tab), FadeIn(brk), run_time=0.4)
        self.play(Create(verde), run_time=0.8)
        nec = caja_dato("NEC · 250.110", "partes metálicas de equipos fijos → a tierra", VERDE_OK, 7.6, 26).move_to([0, 4.0, 0])
        self.play(FadeIn(nec), run_time=0.4)
        cf = corriente([du.get_right(), [0.4, du.get_right()[1], 0], [0.4, -3.2, 0], [2.6, -3.2, 0], tab.get_bottom()], vel=2.2, escala=1.5, color=ROJO)
        self.frac(0.3)
        self.add(cf)
        self.wait(0.8)
        self.sfx("tic", -4)
        self.play(mover_palanca(brk, False), run_time=0.25)
        self.remove(cf)
        ok = VGroup(check(VERDE_OK, 0.32), T("la falla dispara el breaker", 32, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -4.6, 0])
        self.play(FadeIn(ok), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(du, tab, brk, verde, nec, ok)

        # p5: qué hacer
        self.voz("p5")
        tt = T("si tu ducha da toques:", 46, AMBAR, "HEAVY").move_to([0, 3.6, 0])
        self.play(FadeIn(tt), run_time=0.3)
        pasos = VGroup(*[caja_dato(a, b, c, 7.4, 28) for a, b, c in [("1 · corta el breaker", "y no la uses", ROJO),
                                                                    ("2 · revisa la tierra", "el cable verde hasta el tablero", VERDE_OK),
                                                                    ("3 · cambia la resistencia", "si está dañada", NARANJA),
                                                                    ("+ interruptor de falla a tierra", "otra capa de protección", MARCA)]]).arrange(DOWN, buff=0.3).move_to([0, -0.6, 0])
        for p_ in pasos:
            self.play(FadeIn(p_, shift=RIGHT * 0.3), run_time=0.4)
            self.frac(0.18)
        self.cerrar_voz(0.15)
        self.limpiar(tt, pasos)
        self.final("Ducha que da toques: córtala y revisa la tierra")


# ====================================================================== V08 · número del breaker
def curva_disparo(ax):
    """Curva tiempo-corriente esquemática: zona térmica (inversa) + zona magnética (instantánea)."""
    term = ax.plot(lambda x: 3.0 / (x - 0.9), x_range=[1.25, 7.0], color=AMBAR, stroke_width=6)
    mag = Line(ax.c2p(7.0, 3.0 / 6.1), ax.c2p(7.0, 0.08)).set_stroke(ROJO, 6)
    base = Line(ax.c2p(7.0, 0.08), ax.c2p(10, 0.08)).set_stroke(ROJO, 6)
    return VGroup(term, mag, base)


class V08C(ShortC):
    CLAVE = "v08c"

    def cuerpo(self):
        self.voz("gancho")
        tab = RoundedRectangle(width=4.6, height=6.0, corner_radius=0.2, stroke_color=METAL_OSC, stroke_width=4).set_fill("#C9CED6", 1).move_to([0, 0.4, 0])
        brs = VGroup(*[breaker(a, lado=1).scale(3.2) for a in ("15", "20", "30", "20")]).arrange(DOWN, buff=0.35).move_to(tab)
        self.play(FadeIn(tab), LaggedStart(*[FadeIn(b, shift=LEFT * 0.2) for b in brs], lag_ratio=0.15), run_time=0.8)
        self.frac(0.2)
        self.play(*[Indicate(b[3], scale_factor=1.6, color=AMBAR) for b in brs], run_time=0.7)
        pista = VGroup(T("no protege al aparato", 36, TINTA, "HEAVY"), pastilla("protege al CABLE", MARCA, 40, True)).arrange(DOWN, buff=0.2).move_to([0, -4.0, 0])
        self.frac(0.3)
        self.play(FadeIn(pista[0]), run_time=0.3)
        self.play(FadeIn(pista[1], scale=1.1), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(tab, brs, pista)

        # p1: valores normalizados 240.6(A)
        self.voz("p1")
        b = breaker("20", lado=1).scale(6.5).move_to([0, 2.8, 0])
        flecha = Arrow([2.4, 1.3, 0], b[3].get_bottom() + DOWN * 0.05, buff=0.1, color=AMBAR, stroke_width=5)
        lp = T("impreso en la palanca", 28, AMBAR, "HEAVY").move_to([2.4, 1.0, 0])
        self.play(FadeIn(b), run_time=0.4)
        self.play(GrowArrow(flecha), FadeIn(lp), run_time=0.4)
        tit = caja_dato("NEC · Tabla 240.6(A)", "valores normalizados (A)", MARCA, 5.4, 28).move_to([0, -0.2, 0])
        vals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90]
        celdas = VGroup(*[VGroup(RoundedRectangle(width=1.2, height=0.7, corner_radius=0.1, stroke_color="#4A5AA0", stroke_width=2).set_fill(CARTA, 1),
                                 T(str(v), 34, TINTA, "HEAVY")) for v in vals]).arrange_in_grid(3, 4, buff=0.18).move_to([0, -2.8, 0])
        for c in celdas:
            c[1].move_to(c[0])
        self.frac(0.1)
        self.play(FadeIn(tit), LaggedStart(*[FadeIn(c, scale=0.6) for c in celdas], lag_ratio=0.05), run_time=1.0)
        self.play(*[c[0].animate.set_fill(MARCA, 1) for c in celdas[:4]], run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(b, flecha, lp, tit, celdas)

        # p2: por dentro: bimetal + bobina; curva de disparo
        self.voz("p2")
        caja = RoundedRectangle(width=7.6, height=3.6, corner_radius=0.2, stroke_color="#8F9AC8", stroke_width=3).set_fill("#1B2433", 1).move_to([0, 2.2, 0])
        bim = VGroup(Rectangle(width=0.22, height=2.2, stroke_width=0).set_fill(COBRE_V, 1), Rectangle(width=0.22, height=2.2, stroke_width=0).set_fill("#B8BEC8", 1)).arrange(RIGHT, buff=0).move_to([-2.2, 2.1, 0])
        lb = T("bimetal", 28, AMBAR, "HEAVY").next_to(bim, DOWN, buff=0.15)
        bob = VGroup(*[Ellipse(width=1.1, height=0.3).set_stroke(COBRE_V, 5).move_to([1.8, 1.5 + 0.22 * k, 0]) for k in range(6)])
        nuc_ = Rectangle(width=0.3, height=1.8, stroke_width=0).set_fill("#8C96A3", 1).move_to([1.8, 2.3, 0])
        lbob = T("bobina", 28, ROJO, "HEAVY").next_to(bob, DOWN, buff=0.15)
        self.play(FadeIn(caja), FadeIn(bim), FadeIn(lb), FadeIn(bob), FadeIn(nuc_), FadeIn(lbob), run_time=0.6)
        t1 = T("sobrecarga → se calienta y se dobla", 26, AMBAR, "BOLD").move_to([0, 4.3, 0])
        self.frac(0.05)
        self.play(FadeIn(t1), bim.animate.apply_function(lambda p: p + np.array([0.25 * ((p[1] - 1.0) / 2.2) ** 2 * 4, 0, 0])), bim[0].animate.set_fill(CALOR, 1), run_time=1.0)
        self.frac(0.2)
        t2 = T("cortocircuito → jala al instante", 26, ROJO, "HEAVY").move_to([0, 4.3, 0])
        self.play(FadeOut(t1), FadeIn(t2), nuc_.animate.shift(UP * 0.5), Flash(bob.get_center(), color=ROJO), run_time=0.5)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 8, 1], x_length=6.6, y_length=3.6, tips=False,
                  axis_config={"color": CLARO, "stroke_width": 3, "include_ticks": False}).move_to([0.2, -2.4, 0])
        lx = T("corriente (× la nominal)", 24, CLARO, "BOLD").next_to(ax.x_axis, DOWN, buff=0.12)
        ly = T("tiempo", 24, CLARO, "BOLD").next_to(ax.y_axis, UP, buff=0.1)
        cv = curva_disparo(ax)
        self.frac(0.1)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly), run_time=0.4)
        self.play(Create(cv[0]), run_time=0.8)
        self.play(Create(cv[1]), Create(cv[2]), run_time=0.5)
        zt = T("minutos", 26, AMBAR, "HEAVY").move_to(ax.c2p(2.6, 3.4))
        zm = T("segundos", 26, ROJO, "HEAVY").move_to(ax.c2p(8.6, 1.4))
        self.play(FadeIn(zt), FadeIn(zm), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(caja, bim, lb, bob, nuc_, lbob, t2, ax, lx, ly, cv, zt, zm)

        # p3: cable → breaker (240.4(D)), filas horizontales
        self.voz("p3")
        tit = caja_dato("NEC · 240.4(D)", "cobre: calibre → breaker máximo", MARCA, 6.0, 28).move_to([0, 3.6, 0])
        self.play(FadeIn(tit), run_time=0.4)
        filas = VGroup()
        for k, (n, a, amp, col) in enumerate([("14 AWG", 2.08, "15", AMBAR), ("12 AWG", 3.31, "20", NARANJA), ("10 AWG", 5.26, "30", ROJO)]):
            y = 1.6 - 1.9 * k
            c = cable_lateral(3.2, 0.25 + 0.06 * k, NEGRO_BK).move_to([-1.9, y, 0])
            ln = T(n, 30, TINTA, "HEAVY").next_to(c, UP, buff=0.1)
            fl = Arrow([0.0, y, 0], [1.0, y, 0], buff=0, color=CLARO, stroke_width=5)
            b = breaker(amp, lado=1).scale(4.2).move_to([2.6, y, 0])
            filas.add(VGroup(c, ln, fl, b))
        self.frac(0.1)
        for f_ in filas:
            self.play(FadeIn(f_[0]), FadeIn(f_[1]), run_time=0.3)
            self.play(GrowArrow(f_[2]), FadeIn(f_[3], shift=LEFT * 0.2), run_time=0.35)
            self.frac(0.08)
        av = caja_dato("si el breaker fuera más grande", "el cable se calienta y el breaker no reacciona", ROJO, 7.4, 26).move_to([0, -4.6, 0])
        self.play(FadeIn(av, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(tit, filas, av)

        # p4: carga continua: 125 % → 80 %
        self.voz("p4")
        reloj = VGroup(Circle(radius=1.0, stroke_color=CLARO, stroke_width=5), Line(ORIGIN, UP * 0.7).set_stroke(TINTA, 6), Line(ORIGIN, RIGHT * 0.5).set_stroke(TINTA, 6)).move_to([-2.4, 2.6, 0])
        t3 = VGroup(T("carga continua", 36, AMBAR, "HEAVY"), T("3 horas o más", 34, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([1.4, 2.6, 0])
        self.play(FadeIn(reloj), FadeIn(t3), run_time=0.5)
        self.play(Rotate(reloj[1], -TAU * 0.75, about_point=reloj[0].get_center()), run_time=0.8)
        barra = Rectangle(width=7.0, height=1.0, stroke_color=CLARO, stroke_width=3).move_to([0, -0.4, 0])
        rel = Rectangle(width=7.0 * 0.8, height=1.0, stroke_width=0).set_fill(VERDE_OK, 0.9).align_to(barra, LEFT).move_to([barra.get_left()[0] + 2.8, -0.4, 0])
        l20 = T("breaker 20 A", 32, TINTA, "HEAVY").next_to(barra, UP, buff=0.15)
        l16 = T("16 A continuos (80 %)", 34, VERDE_OK, "HEAVY").next_to(barra, DOWN, buff=0.2)
        self.frac(0.1)
        self.play(Create(barra), FadeIn(l20), run_time=0.4)
        self.play(GrowFromEdge(rel, LEFT), run_time=0.7)
        self.play(FadeIn(l16), run_time=0.3)
        nec = caja_dato("NEC · 210.20(A)", "breaker ≥ 125 % de la carga continua", MARCA, 6.4, 26).move_to([0, -3.4, 0])
        self.frac(0.2)
        self.play(FadeIn(nec), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(reloj, t3, barra, rel, l20, l16, nec)

        # p5: resumen
        self.voz("p5")
        b = breaker("20", lado=1).scale(6.0).move_to([0, 2.0, 0])
        self.play(FadeIn(b), run_time=0.3)
        r1 = T("dice cuánta corriente aguanta el CIRCUITO", 34, TINTA, "HEAVY").move_to([0, -0.2, 0])
        self.play(FadeIn(r1), run_time=0.3)
        self.frac(0.3)
        self.play(mover_palanca(b, False), run_time=0.3)
        r2 = pastilla("si se dispara, está haciendo su trabajo", VERDE_OK, 34, True).move_to([0, -1.8, 0])
        self.play(FadeIn(r2, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.15)
        self.limpiar(b, r1, r2)
        self.final("El número del breaker protege al cable")


# ====================================================================== V09 · breaker más grande
class V09C(ShortC):
    CLAVE = "v09c"

    def cuerpo(self):
        self.voz("gancho")
        b = breaker("20", lado=1).scale(6.0).move_to([0, 1.8, 0])
        self.play(FadeIn(b), run_time=0.3)
        for _ in range(2):
            self.sfx("tic", -8)
            self.play(mover_palanca(b, False), run_time=0.2)
            self.play(mover_palanca(b, True), run_time=0.3)
        b30 = breaker("30", lado=1).scale(6.0).move_to([0, -1.6, 0])
        q = T("¿pongo uno más grande?", 44, TINTA, "HEAVY").move_to([0, 0.0, 0])
        self.play(FadeIn(q), FadeIn(b30, shift=UP * 0.3), run_time=0.5)
        x_ = equis(ROJO, 0.7).move_to(b30)
        self.frac(0.3)
        self.play(FadeIn(x_, scale=1.5), run_time=0.3)
        err = pastilla("uno de los errores más peligrosos", ROJO, 36, True).move_to([0, -3.6, 0])
        self.play(FadeIn(err), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(b, b30, q, x_, err)

        # p1: el breaker cuida al cable
        self.voz("p1")
        c = cable_lateral(7.4, 0.9).move_to([0, -0.4, 0])
        b = breaker("20", lado=1).scale(5.0).move_to([0, 2.4, 0])
        escudo = VMobject().set_points_smoothly([[-1.2, 1.2, 0], [0, 1.6, 0], [1.2, 1.2, 0], [1.0, 0.1, 0], [0, -0.6, 0], [-1.0, 0.1, 0], [-1.2, 1.2, 0]])
        escudo.set_fill(MARCA, 0.25).set_stroke(MARCA, 5).scale(0.8).next_to(c, UP, buff=0.1)
        self.play(FadeIn(c), FadeIn(b), run_time=0.4)
        self.play(DrawBorderThenFill(escudo), run_time=0.6)
        nec = caja_dato("NEC · 240.4", "cada conductor protegido según su ampacidad", MARCA, 7.2, 26).move_to([0, -3.2, 0])
        self.frac(0.2)
        self.play(FadeIn(nec), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(c, b, escudo, nec)

        # p2: 12 AWG soporta 25 A (75 °C) pero el breaker deja pasar 30
        self.voz("p2")
        s12 = seccion(3.31, 0.9).move_to([-3.2, -2.4, 0])
        l12 = T("12 AWG", 36, TINTA, "HEAVY").next_to(s12, DOWN, buff=0.15)
        self.play(FadeIn(s12), FadeIn(l12), run_time=0.4)
        escala = Line([-1.4, -4.0, 0], [-1.4, 3.2, 0]).set_stroke(CLARO, 3)
        def yv(a):
            return -4.0 + a / 32 * 7.2
        marcas = VGroup(*[VGroup(Line([-1.55, yv(a), 0], [-1.25, yv(a), 0]).set_stroke(CLARO, 2), T(f"{a} A", 26, CLARO, "BOLD").next_to([-1.55, yv(a), 0], LEFT, buff=0.1)) for a in (0, 10, 20, 25, 30)])
        self.play(Create(escala), FadeIn(marcas), run_time=0.5)
        ok = Rectangle(width=1.2, height=yv(25) - yv(0), stroke_width=0).set_fill(VERDE_OK, 0.85).move_to([-0.5, (yv(25) + yv(0)) / 2, 0])
        lok = T("cable: hasta 25 A\n(Tabla 310.16, 75 °C)", 28, VERDE_OK, "HEAVY").move_to([2.3, -1.6, 0])
        self.frac(0.1)
        self.play(GrowFromEdge(ok, DOWN), FadeIn(lok), run_time=0.6)
        b20 = Line([-1.2, yv(20), 0], [0.6, yv(20), 0]).set_stroke(AMBAR, 6)
        lb20 = T("breaker 20 A ✓", 28, AMBAR, "HEAVY").next_to(b20, RIGHT, buff=0.1)
        self.play(Create(b20), FadeIn(lb20), run_time=0.4)
        self.frac(0.2)
        exc = Rectangle(width=1.2, height=yv(30) - yv(25), stroke_width=0).set_fill(ROJO, 0.9).move_to([-0.5, (yv(25) + yv(30)) / 2, 0])
        b30 = Line([-1.2, yv(30), 0], [0.6, yv(30), 0]).set_stroke(ROJO, 6)
        lb30 = T("breaker 30 A ✗", 28, ROJO, "HEAVY").next_to(b30, RIGHT, buff=0.1)
        self.play(GrowFromEdge(exc, DOWN), Create(b30), FadeIn(lb30), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(s12, l12, escala, marcas, ok, lok, b20, lb20, exc, b30, lb30)

        # p3: calor ∝ I²: cuadrados 20² vs 30²
        self.voz("p3")
        k = 0.12
        q20 = Square(20 * k * 1.0).set_fill(AMBAR, 0.85).set_stroke(WHITE, 2)
        q30 = Square(30 * k * 1.0).set_fill(ROJO, 0.85).set_stroke(WHITE, 2)
        q20.move_to([-2.4, 0.6, 0], aligned_edge=DOWN)
        q30.move_to([1.7, 0.6 - 0.0, 0], aligned_edge=DOWN)
        t20 = VGroup(T("20 A", 36, AMBAR, "HEAVY"), T("20² = 400", 28, TINTA, "BOLD")).arrange(DOWN, buff=0.05).next_to(q20, DOWN, buff=0.2)
        t30 = VGroup(T("30 A", 36, ROJO, "HEAVY"), T("30² = 900", 28, TINTA, "BOLD")).arrange(DOWN, buff=0.05).next_to(q30, DOWN, buff=0.2)
        f = T("calor = I² × R", 56, CALOR, "HEAVY").move_to([0, 4.0, 0])
        self.play(FadeIn(f), run_time=0.4)
        self.play(GrowFromEdge(q20, DOWN), FadeIn(t20), run_time=0.5)
        self.frac(0.15)
        self.play(GrowFromEdge(q30, DOWN), FadeIn(t30), run_time=0.6)
        r = VGroup(T("+50 % corriente", 36, TINTA, "HEAVY"), T("× 2.25 calor", 64, ROJO, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, -3.4, 0])
        self.frac(0.2)
        self.play(FadeIn(r, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(q20, q30, t20, t30, f, r)

        # p4: pared por dentro: el cable se degrada y el breaker "no se entera"
        self.voz("p4")
        pared = Rectangle(width=8.6, height=6.2, stroke_width=0).set_fill("#8B7355", 0.9).move_to([0, 0.6, 0])
        ladr = VGroup(*[Line([-4.3, y, 0], [4.3, y, 0]).set_stroke("#6E5A42", 2) for y in np.arange(-2.4, 3.7, 0.6)])
        tub = VMobject().set_points_smoothly([[-4.3, 2.0, 0], [-1.0, 2.2, 0], [1.4, 0.4, 0], [4.3, 0.2, 0]]).set_stroke("#3A3F48", 26)
        cab = tub.copy().set_stroke(NEGRO_BK, 12)
        self.play(FadeIn(pared), FadeIn(ladr), FadeIn(tub), FadeIn(cab), run_time=0.5)
        cur = corriente([tub.point_from_proportion(t) for t in np.linspace(0, 1, 20)], vel=2.0, escala=1.4)
        self.add(cur)
        self.play(cab.animate.set_stroke("#7A2410"), run_time=1.0)
        hm = humo(tub.point_from_proportion(0.55) + UP * 0.3, 4)
        gl = resplandor(tub.point_from_proportion(0.55), 1.4, CALOR, 10, 0.06)
        self.play(FadeIn(gl), FadeIn(hm, shift=UP * 0.3), run_time=0.5)
        b = breaker("30", lado=1).scale(4.0).move_to([-2.4, -3.6, 0])
        bur = VGroup(RoundedRectangle(width=3.8, height=1.0, corner_radius=0.25, stroke_color=CLARO, stroke_width=2).set_fill(CARTA, 1),
                     T("“30 A es normal”", 30, TINTA, "HEAVY")).move_to([1.6, -3.6, 0])
        bur[1].move_to(bur[0])
        self.frac(0.2)
        self.play(FadeIn(b), FadeIn(bur, shift=LEFT * 0.2), run_time=0.5)
        inc = pastilla("así empiezan incendios dentro de la pared", ROJO, 30, True).move_to([0, -5.0, 0])
        self.frac(0.25)
        self.play(FadeIn(inc), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(pared, ladr, tub, cab, cur, hm, gl, b, bur, inc)

        # p5: el disparo es un aviso → suma de cargas → solución
        self.voz("p5")
        av = pastilla("el disparo es un AVISO", AMBAR, 40, True).move_to([0, 3.8, 0])
        self.play(FadeIn(av), run_time=0.3)
        from taller import plancha, hervidor
        pl = plancha().scale(1.3).move_to([-3.0, 1.8, 0])
        cf = hervidor().scale(1.3).move_to([-0.7, 1.8, 0])
        t1 = T("1200 W\n10 A", 28, TINTA, "HEAVY").next_to(pl, DOWN, buff=0.2)
        t2 = T("1000 W\n8.3 A", 28, TINTA, "HEAVY").next_to(cf, DOWN, buff=0.2)
        self.frac(0.12)
        self.play(FadeIn(pl), FadeIn(cf), FadeIn(t1), FadeIn(t2), run_time=0.5)
        suma = VGroup(T("=", 60, TINTA, "HEAVY"), T("18.3 A", 56, ROJO, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([2.5, 1.8, 0])
        self.play(FadeIn(suma, shift=LEFT * 0.2), run_time=0.4)
        sol = VGroup(*[caja_dato(a, b_, c, 7.2, 26) for a, b_, c in [("reparte las cargas", "en otros circuitos", VERDE_OK),
                                                                    ("o haz un circuito nuevo", "con el calibre correcto", VERDE_OK),
                                                                    ("¿dispara sin carga?", "puede ser un cortocircuito: electricista", ROJO)]]).arrange(DOWN, buff=0.25).move_to([0, -2.6, 0])
        self.frac(0.12)
        for s_ in sol:
            self.play(FadeIn(s_, shift=RIGHT * 0.3), run_time=0.35)
            self.frac(0.12)
        self.cerrar_voz(0.15)
        self.limpiar(av, pl, cf, t1, t2, suma, sol)
        self.final("Nunca subas el breaker sin subir el cable")


# ====================================================================== V10 · cables del poste sin forro
class V10C(ShortC):
    CLAVE = "v10c"

    def cuerpo(self):
        self.voz("gancho")
        pg, pts = poste(7.5, 4.4, 2)
        pg.move_to([1.8, -0.8, 0])
        pts = [p + pg.get_center() - np.array([0, -7.5 / 2 + 0.0, 0]) * 0 for p in pts]
        cab_a = VGroup(*[Line([-4.6, pg[4][k].get_top()[1] + 0.05, 0], [4.6, pg[4][k].get_top()[1] + 0.05, 0]).set_stroke("#C7CCD6", 4) for k in range(2)])
        self.play(FadeIn(pg), Create(cab_a), run_time=0.7)
        ld = pastilla("desnudos", AMBAR, 36, True).move_to([-2.2, 4.0, 0])
        self.play(FadeIn(ld), run_time=0.3)
        casa = VGroup(seccion(3.31, 0.8).move_to([-2.4, -2.6, 0]), T("cable de casa:\ncon forro", 28, TINTA, "HEAVY").move_to([-2.4, -4.2, 0]))
        self.frac(0.15)
        self.play(FadeIn(casa), run_time=0.4)
        q = T("¿por qué?", 56, TINTA, "HEAVY").move_to([1.8, -5.2, 0])
        self.frac(0.25)
        self.play(FadeIn(q, scale=1.2), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(pg, cab_a, ld, casa, q)

        # p1: el aire aísla — campo entre conductores
        self.voz("p1")
        c1 = conductor_frente([-2.2, 1.4, 0], 0.5)
        c2 = conductor_frente([2.2, 1.4, 0], 0.5)
        campo = VGroup(*[ArcBetweenPoints([-1.7, 1.4 + dy * 0.12, 0], [1.7, 1.4 + dy * 0.12, 0], angle=-dy * 0.25).set_stroke(CIAN, 2, 0.6) for dy in range(-4, 5)])
        aire = T("aire", 44, CIAN, "HEAVY").move_to([0, 2.8, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        self.play(LaggedStart(*[Create(c) for c in campo], lag_ratio=0.05), FadeIn(aire), run_time=0.8)
        rig = VGroup(T("≈ 3 000 V", 64, AMBAR, "HEAVY"), T("por milímetro de aire seco", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, -0.8, 0])
        self.frac(0.1)
        self.play(FadeIn(rig, scale=1.1), run_time=0.4)
        sep = caja_dato("bien separados", "entre sí y del poste", MARCA, 5.4, 28).move_to([0, -2.8, 0])
        self.frac(0.15)
        self.play(FadeIn(sep), run_time=0.35)
        tr = T("transmisión: separaciones de metros", 30, CLARO, "HEAVY").move_to([0, -4.3, 0])
        self.frac(0.2)
        self.play(FadeIn(tr), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(c1, c2, campo, aire, rig, sep, tr)

        # p2: aisladores: distancia de fuga y cadenas
        self.voz("p2")
        ai = aislador_pin([-1.8, -0.6, 0], 3.6)
        self.play(FadeIn(ai, shift=UP * 0.3), run_time=0.5)
        fuga = VMobject().set_points_as_corners([ai[3].get_top() + LEFT * 0.4, ai[2][2].get_corner(UL), ai[2][2].get_corner(DL), ai[2][1].get_corner(UL),
                                                 ai[2][1].get_corner(DL), ai[2][0].get_corner(UL), ai[2][0].get_corner(DL), ai[0].get_bottom()]).set_stroke(AMBAR, 5)
        recta = DashedLine(ai[3].get_top() + RIGHT * 0.5, ai[0].get_bottom() + RIGHT * 0.5, color=ROJO)
        self.frac(0.1)
        self.play(Create(recta), run_time=0.4)
        self.play(Create(fuga), run_time=1.0)
        lf = VGroup(T("camino más largo", 32, AMBAR, "HEAVY"), T("por la superficie", 28, TINTA, "BOLD"), T("lluvia y polvo no hacen puente", 26, CLARO, "BOLD")).arrange(DOWN, buff=0.1).move_to([1.8, 1.6, 0])
        self.play(FadeIn(lf), run_time=0.4)
        cad = VGroup(*[Ellipse(width=1.3, height=0.35).set_fill("#B8653A", 1).set_stroke("#7A3B12", 2) for _ in range(6)]).arrange(DOWN, buff=0.08).move_to([2.2, -2.6, 0])
        lc = T("más voltaje → más discos", 28, TINTA, "HEAVY").next_to(cad, LEFT, buff=0.3)
        self.frac(0.2)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.1) for d in cad], lag_ratio=0.1), FadeIn(lc), run_time=0.7)
        self.cerrar_voz(0.15)
        self.limpiar(ai, fuga, recta, lf, cad, lc)

        # p3: forro grueso pesado y que atrapa calor vs desnudo que se enfría
        self.voz("p3")
        g1 = VGroup(Circle(radius=1.6).set_fill("#2A2E35", 1).set_stroke("#8F9AC8", 3), conductor_frente(ORIGIN, 0.6)).move_to([-2.1, 1.4, 0])
        g2 = conductor_frente([2.1, 1.4, 0], 0.6)
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.4)
        cal1 = resplandor(g1.get_center(), 1.0, CALOR, 8, 0.12)
        fl2 = VGroup(*[Arrow(g2.get_center() + 0.7 * np.array([np.cos(a), np.sin(a), 0]), g2.get_center() + 1.5 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=CALOR, stroke_width=4, tip_length=0.15)
                       for a in np.linspace(0, TAU, 8, endpoint=False)])
        self.frac(0.1)
        self.play(FadeIn(cal1), run_time=0.4)
        self.play(LaggedStart(*[GrowArrow(f) for f in fl2], lag_ratio=0.05), run_time=0.6)
        l1 = VGroup(T("forro grueso", 30, TINTA, "HEAVY"), T("pesado · atrapa calor", 26, ROJO, "BOLD")).arrange(DOWN, buff=0.08).next_to(g1, DOWN, buff=0.3)
        l2 = VGroup(T("desnudo", 30, TINTA, "HEAVY"), T("se enfría con el aire", 26, VERDE_OK, "BOLD")).arrange(DOWN, buff=0.08).next_to(g2, DOWN, buff=1.0).align_to(l1, UP)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        mas = pastilla("puede llevar más corriente", VERDE_OK, 34, True).move_to([0, -3.4, 0])
        self.frac(0.2)
        self.play(FadeIn(mas, scale=1.1), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(g1, g2, cal1, fl2, l1, l2, mas)

        # p4: ACSR: aluminio + alma de acero; densidades
        self.voz("p4")
        corte = VGroup()
        R = 0.32
        for k in range(7):
            pos = ORIGIN if k == 0 else 2 * R * np.array([np.cos(TAU * k / 6), np.sin(TAU * k / 6), 0])
            corte.add(Circle(radius=R).set_fill("#7C8594", 1).set_stroke("#3A4250", 2).move_to(pos))
        for k in range(12):
            a = TAU * k / 12
            corte.add(Circle(radius=R * 0.95).set_fill("#D0D5DD", 1).set_stroke("#8C96A3", 2).move_to(4 * R * np.array([np.cos(a), np.sin(a), 0])))
        corte.move_to([0.5, 2.3, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in corte], lag_ratio=0.03), run_time=0.8)
        la = T("aluminio", 30, "#D0D5DD", "HEAVY").next_to(corte, RIGHT, buff=0.2)
        lac = T("alma de acero", 30, "#98A2B3", "HEAVY").next_to(corte, LEFT, buff=0.2)
        self.play(FadeIn(la), FadeIn(lac), run_time=0.3)
        def barra(v, vmax, col, txt, y):
            b = Rectangle(width=v / vmax * 4.4, height=0.6, stroke_width=0).set_fill(col, 0.95).move_to([-2.4 + v / vmax * 4.4 / 2, y, 0])
            t_ = T(txt, 28, TINTA, "HEAVY").next_to([-2.4, y, 0], LEFT, buff=0.15)
            tv = T(f"{v} g/cm³", 26, col, "HEAVY").next_to(b, RIGHT, buff=0.1)
            return VGroup(b, t_, tv)
        den = T("densidad", 28, CLARO, "BOLD").move_to([0, -0.4, 0])
        bal = barra(2.70, 8.96, "#D0D5DD", "Al", -1.2)
        bcu = barra(8.96, 8.96, COBRE_V, "Cu", -2.1)
        self.frac(0.12)
        self.play(FadeIn(den), FadeIn(bal[1]), FadeIn(bcu[1]), GrowFromEdge(bal[0], LEFT), GrowFromEdge(bcu[0], LEFT), run_time=0.7)
        self.play(FadeIn(bal[2]), FadeIn(bcu[2]), run_time=0.3)
        c61 = VGroup(T("conduce ≈ 61 %", 36, AMBAR, "HEAVY"), T("del cobre", 28, TINTA, "BOLD")).arrange(RIGHT, buff=0.2).move_to([0, -3.3, 0])
        self.frac(0.15)
        self.play(FadeIn(c61), run_time=0.35)
        ac = T("el acero da resistencia para claros largos", 28, CLARO, "HEAVY").move_to([0, -4.3, 0])
        self.frac(0.1)
        self.play(FadeIn(ac), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(corte, la, lac, den, bal, bcu, c61, ac)

        # p5: cubierta ≠ aislamiento; nunca acercarse
        self.voz("p5")
        pg, _ = poste(7.0, 4.0, 2)
        pg.move_to([1.6, -0.6, 0])
        cab_a = VGroup(*[Line([-4.6, pg[4][k].get_top()[1] + 0.05, 0], [4.6, pg[4][k].get_top()[1] + 0.05, 0]).set_stroke("#C7CCD6", 4) for k in range(2)])
        self.play(FadeIn(pg), FadeIn(cab_a), run_time=0.4)
        cub = caja_dato("cable con cubierta", "en zonas con árboles: NO es aislamiento completo", AMBAR, 7.6, 26).move_to([0, 3.9, 0])
        self.play(FadeIn(cub), run_time=0.4)
        esc = escalera(4.6, 0.7).move_to([-2.6, -2.2, 0]).rotate(-0.25)
        pis = piscucha().scale(0.8).move_to([-1.4, 1.0, 0])
        self.frac(0.25)
        self.play(FadeIn(esc), FadeIn(pis), run_time=0.4)
        x1 = equis(ROJO, 0.45).next_to(esc, RIGHT, buff=0.1)
        x2 = equis(ROJO, 0.4).next_to(pis, LEFT, buff=0.1)
        self.play(FadeIn(x1, scale=1.4), FadeIn(x2, scale=1.4), run_time=0.3)
        reg = pastilla("trata toda línea como ENERGIZADA", ROJO, 34, True).move_to([0, -5.1, 0])
        self.frac(0.2)
        self.play(FadeIn(reg, scale=1.1), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(pg, cab_a, cub, esc, pis, x1, x2, reg)
        self.final("El aire aísla: mantén la distancia")


# ====================================================================== portadas V03–V10
class PortadaC(MovingCameraScene):
    def construct(self):
        import os
        from miniaturas import texto_gancho, sticker, logo_esq
        k = os.environ["CLAVE"]
        fondos = {"v03c": ["#0B2A4A", "#3A6EA5"], "v04c": ["#1A1A1A", "#2F4F4F"], "v05c": ["#2A1F05", "#12305A"], "v06c": ["#062A1A", "#12305A"],
                  "v07c": ["#0A2A3A", "#1E5B8A"], "v08c": ["#20140A", "#12305A"], "v09c": ["#2E0A06", "#12305A"], "v10c": ["#16213E", "#4A6FA5"]}
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=fondos[k], opacity=1).set_sheen_direction(UR))
        txt = {"v03c": [("¿PARA QUÉ SON", "#FFFFFF"), ("ESTAS BOLAS?", "#FF9F1C")], "v04c": [("¿POR QUÉ", "#FFFFFF"), ("ZUMBA?", "#6FF2FF")],
               "v05c": [("¿POR QUÉ UNA", "#FFFFFF"), ("ES MÁS GRANDE?", "#FFD84D")], "v06c": [("¿POR QUÉ ES", "#FFFFFF"), ("MÁS LARGA?", "#3DDC84")],
               "v07c": [("¿TU DUCHA", "#FFFFFF"), ("DA TOQUES?", "#FF5A5F")], "v08c": [("¿QUÉ SIGNIFICA", "#FFFFFF"), ("ESTE NÚMERO?", "#FFD84D")],
               "v09c": [("¿UN BREAKER", "#FFFFFF"), ("MÁS GRANDE?", "#FF5A5F")], "v10c": [("¿POR QUÉ NO", "#FFFFFF"), ("TIENEN FORRO?", "#FFD84D")]}[k]
        st_txt = {"v03c": "no son adornos", "v04c": "120 Hz", "v05c": "no es un error", "v06c": "te protege",
                  "v07c": "¡no es normal!", "v08c": "protege al cable", "v09c": "¡NO lo hagas!", "v10c": "el aire aísla"}[k]
        t = texto_gancho(txt, 100)
        t.scale_to_fit_width(min(8.2, t.width)).move_to([0, 5.0, 0])
        il = VGroup()
        if k == "v03c":
            cab = linea_aerea([-4.6, 1.6, 0], [4.6, 1.6, 0], 1.0, "#C7CCD6", 6)
            il.add(cab, *[esfera_m(c, 0.75).move_to(cab.point_from_proportion(tt) + DOWN * 0.7) for c, tt in zip([NARANJA, WHITE, AMAR_FR], (0.2, 0.5, 0.8))])
        elif k == "v04c":
            tr = transformador().scale(2.0).move_to([0, 0.4, 0])
            il.add(tr, ondas_sonido(tr.get_right() + RIGHT * 0.1, 3, 0.5, 0.45, PI / 2, CIAN, 0), ondas_sonido(tr.get_left() + LEFT * 0.1, 3, 0.5, 0.45, PI / 2, CIAN, PI))
        elif k == "v05c":
            tm = cara(10.0).move_to([0, 0.3, 0])
            il.add(tm, SurroundingRectangle(tm.ne, color="#FFD84D", buff=0.15, stroke_width=8))
        elif k == "v06c":
            cl = clavija_lado(2.0).move_to([-0.9, 0.4, 0])
            il.add(cl, SurroundingRectangle(cl.tierra, color="#3DDC84", buff=0.12, stroke_width=8))
        elif k == "v07c":
            du = ducha().scale(1.8).move_to([0, 0.6, 0])
            il.add(du, *[rayo(du.get_bottom() + LEFT * 0.6 * s, du.get_bottom() + DOWN * 1.6 + LEFT * 1.2 * s, semilla=i) for i, s in enumerate((1, -1))])
        elif k == "v08c":
            b = breaker("20", lado=1).scale(8.0).move_to([0, 0.4, 0])
            il.add(b, Circle(radius=0.9).set_stroke("#FFD84D", 10).move_to(b[3]))
        elif k == "v09c":
            b1 = breaker("20", lado=1).scale(6.0).move_to([-2.2, 0.4, 0]); b2 = breaker("30", lado=1).scale(6.0).move_to([2.2, 0.4, 0])
            il.add(b1, b2, Arrow(b1.get_right(), b2.get_left(), buff=0.15, color=ROJO, stroke_width=10), equis(ROJO, 0.6).move_to([0, -1.2, 0]))
        else:
            pg, _ = poste(8.0, 4.4, 2)
            pg.move_to([0, -1.2, 0])
            il.add(pg, *[Line([-4.6, pg[4][j].get_top()[1] + 0.05, 0], [4.6, pg[4][j].get_top()[1] + 0.05, 0]).set_stroke("#C7CCD6", 6) for j in range(2)])
        st = sticker(st_txt, "#E5484D", size=56, ang=-0.04).move_to([0, -4.3, 0])
        self.add(il, t, st)
        logo_esq(self, (0, -6.2))

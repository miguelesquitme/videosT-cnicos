"""E05 · Ley de Ohm con cosas de tu casa. Guion, fuentes y aritmética en e05_guion.py."""
from taller import *
from comun_e import _osc, _cla
from e05_guion import GUION

V_COL, I_COL, R_COL, P_COL = "#E5484D", "#1E88E5", "#12B76A", "#F79009"


def M(tex, size=1.0, color=TINTA):
    return MathTex(tex, color=color).scale(size)


def cafetera():
    base = RoundedRectangle(width=1.2, height=0.18, corner_radius=0.05, stroke_color=LINEA, stroke_width=1.2).set_fill("#344054", 1).move_to(P(0, -0.75))
    torre = RoundedRectangle(width=0.4, height=1.5, corner_radius=0.08, stroke_color=LINEA, stroke_width=1.2).set_fill("#344054", 1).move_to(P(0.38, 0.0))
    techo = RoundedRectangle(width=1.2, height=0.25, corner_radius=0.08, stroke_color=LINEA, stroke_width=1.2).set_fill("#344054", 1).move_to(P(0, 0.7))
    jarra = Polygon(P(-0.5, -0.65), P(0.1, -0.65), P(0.15, 0.0), P(-0.55, 0.0), stroke_color=LINEA, stroke_width=1.2).set_fill("#EAF4F7", 0.9)
    cafe = Polygon(P(-0.49, -0.64), P(0.09, -0.64), P(0.12, -0.3), P(-0.52, -0.3), stroke_width=0).set_fill("#6B3F22", 1)
    asa = Arc(radius=0.18, start_angle=-PI / 2, angle=PI, arc_center=P(-0.58, -0.32)).set_stroke(LINEA, 5).rotate(PI)
    luz = Circle(radius=0.04, stroke_width=0).set_fill(ROJO, 1).move_to(P(0.38, 0.4))
    return VGroup(base, torre, techo, cafe, jarra, asa, luz)


def tostadora():
    cuerpo = RoundedRectangle(width=1.6, height=1.0, corner_radius=0.3, stroke_color=LINEA, stroke_width=1.3).set_fill("#E4E7EC", 1)
    ranuras = VGroup(*[RoundedRectangle(width=0.5, height=0.08, corner_radius=0.03, stroke_width=0).set_fill("#344054", 1).move_to(P(x, 0.5)) for x in (-0.35, 0.35)])
    panes = VGroup(*[RoundedRectangle(width=0.45, height=0.3, corner_radius=0.1, stroke_color="#B54708", stroke_width=1).set_fill("#E9B872", 1).move_to(P(x, 0.62)) for x in (-0.35, 0.35)])
    palanca = RoundedRectangle(width=0.12, height=0.08, corner_radius=0.02, stroke_width=0).set_fill("#344054", 1).move_to(P(0.86, 0.1))
    patas = VGroup(*[Rectangle(width=0.15, height=0.06, stroke_width=0).set_fill("#344054", 1).move_to(P(x, -0.53)) for x in (-0.5, 0.5)])
    return VGroup(panes, cuerpo, ranuras, palanca, patas)


def etiqueta_w(txt, color=TINTA):
    """Etiqueta plateada de datos del aparato."""
    caja = RoundedRectangle(width=1.6, height=0.62, corner_radius=0.06, stroke_color=METAL_OSC, stroke_width=1.2).set_fill("#EEF0F3", 1)
    t = VGroup(T(txt, 30, "#1D2939", "HEAVY"), T("120 V ~ 60 Hz", 14, "#5B6B7F", "MEDIUM")).arrange(DOWN, buff=0.04).move_to(caja)
    if t.width > 1.45:
        caja.stretch_to_fit_width(t.width + 0.2)
    return VGroup(caja, t)


def foco_viejo():
    """Foco antiguo genérico (solo la silueta, sin detalle interno)."""
    g = foco_led(False, 0.9)
    g[3].set_fill("#F2F4F7")
    g[0].set_fill("#FFFDF5", 1)
    return VGroup(g[0], g[5])


class Ohm(TallerH):
    CARPETA_VOZ = "voz_e05"
    GUION = GUION

    def construct(self):
        for paso in ("intro", "agua", "unidades", "ley", "triangulo", "alterna", "potencia", "led", "comparacion", "hervidor",
                     "plancha", "microondas", "focos", "paralelo", "breaker", "regleta", "serie", "cable", "caida", "calor",
                     "joule", "medir", "seguridad", "energia", "reto", "ejercicio", "repaso"):
            getattr(self, "f_" + paso)()
        self.resumen_y_final("cierre", ["V = I × R", "P = V × I", "En paralelo, las corrientes se suman",
                                        "Cable largo: más resistencia y más calor"])

    # -------------------------------------------------------------- utilidades
    def pasos_calc(self, lineas, pos, fracs, size=1.15, buff=0.35):
        """Escribe líneas de cálculo una a una, repartidas en la voz."""
        g = VGroup(*[M(l, size) for l in lineas]).arrange(DOWN, buff=buff, aligned_edge=LEFT).move_to(pos)
        for k, (m, f) in enumerate(zip(g, fracs)):
            self.play(Write(m), run_time=0.7)
            self.esperar_frac(f)
        return g

    def aparato(self, icono, etiqueta, pos=(-4.3, 0.3), alto=2.6):
        icono.scale_to_fit_height(alto).move_to([pos[0], pos[1], 0])
        et = etiqueta_w(etiqueta).next_to(icono, DOWN, buff=0.35)
        self.play(FadeIn(icono, shift=UP * 0.2), FadeIn(et), run_time=0.6)
        return VGroup(icono, et)

    def resultado(self, txt, color, pos):
        r = pastilla(txt, color, 34, True).move_to(pos)
        self.sfx("pop", -10)
        self.play(FadeIn(r, scale=1.2), run_time=0.4)
        return r

    # -------------------------------------------------------------- secciones
    def f_intro(self):
        self.voz("intro")
        ic = VGroup(VGroup(hervidor(), plancha()).arrange(RIGHT, buff=0.3), foco_led(True, 0.9), cable_hilos(2.0, FASE, 0.45, 0.6))
        for m, y, hh in zip(ic, (2.2, 0.0, -2.2), (1.2, 1.4, 0.45)):
            m.scale_to_fit_height(hh).move_to([-6.0, y, 0])
        q = [pastilla("¿por qué se dispara?", ROJO, 22, True), pastilla("¿por qué gasta poco?", MARCA, 22, True),
             pastilla("¿por qué se calienta?", P_COL, 22, True)]
        for x, m in zip(q, ic):
            x.move_to([-3.2, m.get_center()[1], 0])
        self.play(LaggedStart(*[FadeIn(m, scale=0.9) for m in ic], lag_ratio=0.3), run_time=1.2)
        tit = self.titulo("LEY DE", "OHM", "con cosas de tu casa")
        for k, x in enumerate(q):
            self.esperar_frac(0.12)
            self.play(FadeIn(x, shift=UP * 0.15), run_time=0.4)
        f = M(r"V = I \times R", 1.8).next_to(tit, DOWN, buff=0.5, aligned_edge=LEFT)
        self.esperar_frac(0.5)
        self.play(Write(f), run_time=0.8)
        self.cerrar_voz()
        self.limpiar(ic, *q, tit, f)

    def f_agua(self):
        self.voz("agua")
        y = 0.4
        arriba = [P(-6.6, y + 0.5), P(-1.2, y + 0.5), P(-0.6, y + 0.18), P(1.4, y + 0.18), P(2.0, y + 0.5), P(6.6, y + 0.5)]
        abajo = [P(x, 2 * y - p[1]) for p in arriba for x in [p[0]]]
        borde = VGroup(VMobject().set_points_as_corners(arriba), VMobject().set_points_as_corners(abajo)).set_stroke(LINEA, 4)
        agua = Polygon(*arriba, *abajo[::-1], stroke_width=0).set_fill(MARCA_CL, 1)
        tanque = VGroup(Rectangle(width=1.0, height=2.6, stroke_color=LINEA, stroke_width=3).set_fill(WHITE, 1).move_to(P(-7.0, y + 0.7)),
                        Rectangle(width=0.96, height=2.0, stroke_width=0).set_fill(MARCA_CL, 1).move_to(P(-7.0, y + 0.4)))
        self.play(FadeIn(tanque), FadeIn(agua), Create(borde), run_time=0.8)
        fl = corriente([P(-6.6, y), P(6.6, y)], vel=0.7, color=MARCA, color2=MARCA_CL, escala=1.6, espacio=0.7)
        self.add(fl)
        e1 = VGroup(T("PRESIÓN", 30, V_COL, "HEAVY"), T("= voltaje", 24, TINTA, "BOLD")).arrange(DOWN, buff=0.08).move_to([-5.3, 2.6, 0])
        e2 = VGroup(T("CAUDAL", 30, I_COL, "HEAVY"), T("= corriente", 24, TINTA, "BOLD")).arrange(DOWN, buff=0.08).move_to([4.6, 2.6, 0])
        e3 = VGroup(T("ANGOSTURA", 30, R_COL, "HEAVY"), T("= resistencia", 24, TINTA, "BOLD")).arrange(DOWN, buff=0.08).move_to([0.4, -1.4, 0])
        fl1 = Arrow([-6.4, 2.0, 0], [-6.4, 1.2, 0], color=V_COL, stroke_width=6, buff=0)
        for k, (e, f) in enumerate(((e1, 0.25), (e2, 0.35), (e3, 0.6))):
            anims = [FadeIn(e, shift=UP * 0.15)] + ([GrowArrow(fl1)] if k == 0 else [])
            self.play(*anims, run_time=0.5)
            self.esperar_frac(f)
        nota = pastilla("más angosta → le cuesta más pasar", R_COL, 24, True).move_to([0.4, -2.6, 0])
        self.play(FadeIn(nota), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tanque, agua, borde, fl, e1, e2, e3, fl1, nota)

    def f_unidades(self):
        self.voz("unidades")
        datos = [("V", "Voltaje", "voltios", V_COL), ("I", "Corriente", "amperios (A)", I_COL), ("R", "Resistencia", "ohmios (Ω)", R_COL)]
        cartas = VGroup()
        for letra, nom, uni, col in datos:
            caja = tarjeta(3.6, 3.4, METAL)
            l = M(letra, 2.6, col).move_to(caja.get_center() + UP * 0.6)
            n = T(nom, 32, TINTA, "HEAVY").move_to(caja.get_center() + DOWN * 0.6)
            u = T(uni, 24, TINTA2, "MEDIUM").next_to(n, DOWN, buff=0.15)
            cartas.add(VGroup(caja, l, n, u))
        cartas.arrange(RIGHT, buff=0.45).move_to([-1.8, 0.4, 0])
        for k, c_ in enumerate(cartas):
            self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
            self.esperar_frac(0.18)
        t = tomacorriente(P(0, 0)).scale(2.2).move_to([5.5, 0.6, 0])
        pl = placa_toma(P(0, 0)).scale(2.2).move_to(t)
        v = pastilla("≈ 120 V", V_COL, 34, True).next_to(pl, DOWN, buff=0.3)
        self.play(FadeIn(pl), FadeIn(v, scale=1.2), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(cartas, pl, v)

    def f_ley(self):
        self.voz("ley")
        a = T("1827", 80, MARCA, "HEAVY").move_to([0, 2.3, 0])
        b = T("Georg Simon Ohm · físico alemán", 32, TINTA2, "BOLD").next_to(a, DOWN, buff=0.2)
        self.play(FadeIn(a, shift=DOWN * 0.2), FadeIn(b), run_time=0.6)
        self.esperar_frac(0.35)
        f = MathTex(r"V", r"=", r"I", r"\times", r"R", color=TINTA).scale(3.2).move_to([0, -0.8, 0])
        f[0].set_color(V_COL)
        f[2].set_color(I_COL)
        f[4].set_color(R_COL)
        self.play(Write(f), run_time=1.2)
        marco = SurroundingRectangle(f, buff=0.35, color=MARCA, corner_radius=0.2, stroke_width=3)
        self.play(Create(marco), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(a, b, f, marco)

    def f_triangulo(self):
        self.voz("triangulo")
        c = np.array([-3.3, 0.0, 0])
        tri = Polygon(c + P(0, 2.4), c + P(-2.6, -1.8), c + P(2.6, -1.8), stroke_color=TINTA, stroke_width=5).set_fill(WHITE, 1)
        hz = Line(c + P(-1.33, 0.35), c + P(1.33, 0.35), stroke_color=TINTA, stroke_width=4)
        vt = Line(c + P(0, 0.35), c + P(0, -1.8), stroke_color=TINTA, stroke_width=4)
        lv = M("V", 2.4, V_COL).move_to(c + P(0, 1.1))
        li = M("I", 2.4, I_COL).move_to(c + P(-0.85, -0.65))
        lr = M("R", 2.4, R_COL).move_to(c + P(0.85, -0.65))
        mult = M(r"\times", 1.3).move_to(c + P(0, -0.65)).set_opacity(0)
        self.play(DrawBorderThenFill(tri), Create(hz), Create(vt), run_time=0.8)
        self.play(FadeIn(lv), FadeIn(li), FadeIn(lr), run_time=0.5)
        self.esperar_frac(0.18)
        casos = [(li, r"I = \dfrac{V}{R}", I_COL), (lr, r"R = \dfrac{V}{I}", R_COL), (lv, r"V = I \times R", V_COL)]
        prev = None
        mano = None
        for k, (tap, tex, col) in enumerate(casos):
            tapa = Circle(radius=0.55, stroke_color=col, stroke_width=4).set_fill(col, 0.85).move_to(tap)
            res = M(tex, 2.0, col).move_to([3.6, 0.2, 0])
            anims = [FadeIn(tapa, scale=1.3), FadeIn(res, shift=LEFT * 0.2)]
            if prev is not None:
                anims += [FadeOut(prev[0]), FadeOut(prev[1])]
            self.play(*anims, run_time=0.5)
            prev = (tapa, res)
            self.esperar_frac([0.33, 0.5, 0.9][k])
        self.cerrar_voz()
        self.limpiar(tri, hz, vt, lv, li, lr, *prev)

    def f_alterna(self):
        self.voz("alterna")
        ax = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.3, 1.3, 1], x_length=6.0, y_length=2.4, tips=False,
                  axis_config={"stroke_color": METAL2, "stroke_width": 2}).move_to([-3.6, 1.6, 0])
        onda = ax.plot(lambda x: np.sin(x), color=V_COL, stroke_width=5)
        tx = T("corriente alterna · 60 Hz", 26, TINTA, "BOLD").next_to(ax, DOWN, buff=0.25)
        self.play(Create(ax), Create(onda), FadeIn(tx), run_time=1.2)
        self.esperar_frac(0.2)
        bien = VGroup(hervidor().scale(0.9), plancha().scale(0.9)).arrange(RIGHT, buff=0.6).move_to([2.6, 1.8, 0])
        b_t = pastilla("calientan: Ohm funciona muy bien", VERDE_OK, 24, True).next_to(bien, DOWN, buff=0.25)
        self.play(FadeIn(bien), FadeIn(b_t), run_time=0.6)
        self.esperar_frac(0.4)
        comp = VGroup(ventilador().scale(0.85), microondas().scale(0.8)).arrange(RIGHT, buff=0.6).move_to([2.6, -1.4, 0])
        c_t = pastilla("motores y electrónica: más complejo", P_COL, 24, True).next_to(comp, DOWN, buff=0.25)
        self.play(FadeIn(comp), FadeIn(c_t), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(ax, onda, tx, bien, b_t, comp, c_t)

    def f_potencia(self):
        self.voz("potencia")
        ap = self.aparato(plancha(), "1200 W", (-4.0, 0.6), 2.2)
        lupa = Circle(radius=0.95, stroke_color=MARCA, stroke_width=4).move_to(ap[1])
        self.play(Create(lupa), run_time=0.5)
        q = T("¿ohmios? → casi nunca", 28, TINTA2, "BOLD").move_to([2.6, 2.3, 0])
        self.play(FadeIn(q), run_time=0.4)
        self.esperar_frac(0.35)
        f = MathTex(r"P", r"=", r"V", r"\times", r"I", color=TINTA).scale(3.0).move_to([2.6, 0.2, 0])
        f[0].set_color(P_COL)
        f[2].set_color(V_COL)
        f[4].set_color(I_COL)
        self.play(Write(f), run_time=1.0)
        w = T("P = potencia, en vatios (W)", 26, P_COL, "HEAVY").next_to(f, DOWN, buff=0.4)
        self.play(FadeIn(w), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ap, lupa, q, f, w)

    def f_led(self):
        self.voz("led")
        ap = self.aparato(foco_led(True, 0.9), "9 W", (-4.3, 0.6), 2.4)
        g = resplandor(ap[0][0].get_center(), 1.5, AMBAR, 10, 0.05)
        self.add_foreground_mobject(ap[0])
        self.play(FadeIn(g), run_time=0.4)
        c = self.pasos_calc([r"I = \dfrac{P}{V}", r"I = \dfrac{9\,\mathrm{W}}{120\,\mathrm{V}}", r"I = 0.075\,\mathrm{A}"],
                            [1.4, 0.8, 0], [0.05, 0.12, 0.05])
        r = self.resultado("75 miliamperios", I_COL, [1.4, -2.0, 0])
        self.cerrar_voz()
        self.remove_foreground_mobject(ap[0])
        self.limpiar(ap, g, c, r)

    def f_comparacion(self):
        self.voz("comparacion")
        izq = foco_viejo().scale_to_fit_height(2.0).move_to([-4.2, 1.6, 0])
        der = foco_led(True, 0.9).scale_to_fit_height(2.0).move_to([0.2, 1.6, 0])
        ti = VGroup(T("antiguo · 60 W", 26, TINTA, "HEAVY"), M(r"60 \div 120 = 0.5\,\mathrm{A}", 0.9)).arrange(DOWN, buff=0.15).next_to(izq, DOWN, buff=0.25)
        td = VGroup(T("LED · 9 W", 26, TINTA, "HEAVY"), M(r"9 \div 120 = 0.075\,\mathrm{A}", 0.9)).arrange(DOWN, buff=0.15).next_to(der, DOWN, buff=0.25)
        self.play(FadeIn(izq), FadeIn(ti), run_time=0.6)
        self.esperar_frac(0.35)
        self.play(FadeIn(der), FadeIn(td), run_time=0.6)
        base = -3.2
        b1 = Rectangle(width=1.0, height=3.2 * 0.5 / 0.5, stroke_width=0).set_fill(P_COL, 1)
        b2 = Rectangle(width=1.0, height=3.2 * 0.075 / 0.5, stroke_width=0).set_fill(I_COL, 1)
        b1.move_to([4.4, base, 0], aligned_edge=DOWN)
        b2.move_to([5.8, base, 0], aligned_edge=DOWN)
        eje = Line([3.7, base, 0], [6.5, base, 0], stroke_color=LINEA, stroke_width=2)
        tit = T("corriente", 24, TINTA2, "BOLD").move_to([5.1, 0.5 + 0.0, 0])
        self.play(Create(eje), GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(tit), run_time=0.8)
        x7 = pastilla("casi 7 veces más", ROJO, 26, True).move_to([5.1, 1.2, 0])
        self.play(FadeIn(x7, scale=1.2), run_time=0.4)
        self.esperar_frac(0.5)
        rec = pastilla("se nota en el recibo", VERDE_OK, 28, True).move_to([-2.0, -3.2, 0])
        self.play(FadeIn(rec), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(izq, der, ti, td, b1, b2, eje, tit, x7, rec)

    def f_hervidor(self):
        self.voz("hervidor")
        ap = self.aparato(hervidor(), "1500 W", (-4.3, 0.6), 2.4)
        c = self.pasos_calc([r"I = \dfrac{1500}{120} = 12.5\,\mathrm{A}"], [1.6, 1.6, 0], [0.2])
        r1 = self.resultado("12.5 A", I_COL, [1.6, 0.3, 0])
        self.esperar_frac(0.1)
        c2 = M(r"R = \dfrac{V}{I} = \dfrac{120}{12.5} = 9.6\,\Omega", 1.15).move_to([1.6, -1.2, 0])
        self.play(Write(c2), run_time=0.8)
        r2 = pastilla("funcionando", R_COL, 24, True).next_to(c2, DOWN, buff=0.3)
        self.play(FadeIn(r2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ap, c, r1, c2, r2)

    def f_plancha(self):
        self.voz("plancha")
        ap = self.aparato(plancha(), "1200 W", (-4.3, 0.6), 2.0)
        c = self.pasos_calc([r"I = \dfrac{1200}{120} = 10\,\mathrm{A}"], [1.6, 1.0, 0], [0.1])
        r = self.resultado("10 A", I_COL, [1.6, -0.6, 0])
        self.cerrar_voz()
        self.limpiar(ap, c, r)

    def f_microondas(self):
        self.voz("microondas")
        ap = self.aparato(microondas(), "1200 W", (-4.3, 0.6), 1.8)
        c = self.pasos_calc([r"I = \dfrac{1200}{120} = 10\,\mathrm{A}"], [1.6, 1.4, 0], [0.15])
        r = self.resultado("10 A · igual que la plancha", I_COL, [1.6, 0.0, 0])
        self.esperar_frac(0.3)
        n = pastilla("en la cocina: varios circuitos", MARCA, 26, True).move_to([1.6, -1.6, 0])
        self.play(FadeIn(n), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ap, c, r, n)

    def f_focos(self):
        self.voz("focos")
        pl = plancha().scale_to_fit_height(1.6).move_to([-5.4, 2.4, 0])
        eq = M(r"10 \div 0.075 \approx 133", 1.3).move_to([0.6, 2.6, 0])
        self.play(FadeIn(pl), Write(eq), run_time=0.8)
        focos = VGroup(*[foco_led(True, 0.9).scale(0.32) for _ in range(133)])
        focos.arrange_in_grid(7, 19, buff=(0.22, 0.12)).move_to([0.4, -0.9, 0])
        self.play(LaggedStart(*[FadeIn(f, scale=0.5) for f in focos], lag_ratio=0.03), run_time=max(2.0, self.resta() * 0.6))
        n = pastilla("133 focos LED", AMBAR, 30, True).move_to([-5.2, 0.6, 0])
        self.play(FadeIn(n, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(pl, eq, focos, n)

    # -------------------------------------------------------------- paralelo y breaker
    def red_paralelo(self):
        xs, xd = -5.6, 4.6
        yt, yb = 1.6, -1.6
        fuente_ = VGroup(RoundedRectangle(width=1.3, height=3.8, corner_radius=0.12, stroke_color=LINEA, stroke_width=2).set_fill(GAL, 1),
                         T("120 V", 26, V_COL, "HEAVY")).move_to([xs, 0, 0])
        fase = cable(P(xs + 0.65, yt), P(xd, yt), color=FASE, w=6)
        neu = cable(P(xs + 0.65, yb), P(xd, yb), color=NEUTRO, w=6)
        ram = VGroup()
        aps = VGroup()
        for x, ap in ((0.2, hervidor()), (3.4, plancha())):
            ram.add(cable(P(x, yt), P(x, 0.75), color=FASE, w=5), cable(P(x, -0.75), P(x, yb), color=NEUTRO, w=5))
            ap.scale_to_fit_height(1.2).move_to([x, 0, 0])
            aps.add(ap)
        nodos = VGroup(*[Dot(P(x, y), radius=0.08, color=TINTA) for x in (0.2, 3.4) for y in (yt, yb)])
        g = VGroup(fuente_, fase, neu, ram, aps, nodos)
        g.rutas = [[P(xs + 0.65, yt), P(0.2, yt), P(0.2, yb), P(xs + 0.65, yb)], [P(xs + 0.65, yt), P(3.4, yt), P(3.4, yb), P(xs + 0.65, yb)]]
        g.xs, g.yt = xs, yt
        return g

    def f_paralelo(self):
        self.voz("paralelo")
        red = self.red_paralelo()
        self.play(FadeIn(red), run_time=0.8)
        v = VGroup(pastilla("120 V", V_COL, 22, True).move_to([1.15, 0, 0]), pastilla("120 V", V_COL, 22, True).move_to([4.6, 0, 0]))
        self.play(FadeIn(v), run_time=0.4)
        self.esperar_frac(0.25)
        fls = [corriente(r_, vel=0.7) for r_ in red.rutas]
        self.add(*fls)
        i1 = pastilla("12.5 A", I_COL, 22, True).move_to([0.2, 2.15, 0]).shift(LEFT * 0.8)
        i2 = pastilla("10 A", I_COL, 22, True).move_to([3.4, 2.15, 0])
        self.play(FadeIn(i1), FadeIn(i2), run_time=0.4)
        self.esperar_frac(0.3)
        tot = M(r"12.5 + 10 = 22.5\,\mathrm{A}", 1.3, I_COL).move_to([-1.6, -2.7, 0])
        self.play(Write(tot), run_time=0.8)
        self.cerrar_voz()
        self.red_guardada = (red, v, fls, i1, i2, tot)

    def f_breaker(self):
        self.voz("breaker")
        red, v, fls, i1, i2, tot = self.red_guardada
        bk = breaker("20", 0.46, 0.26).scale(4.0).move_to([-3.4, 2.9, 0])
        e = T("breaker 20 A", 24, TINTA, "HEAVY").next_to(bk, RIGHT, buff=0.3)
        self.play(FadeOut(v), FadeOut(i1), FadeOut(i2), FadeIn(bk), FadeIn(e), run_time=0.5)
        comp = M(r"22.5\,\mathrm{A} > 20\,\mathrm{A}", 1.3, ROJO).move_to(tot)
        self.play(Transform(tot, comp), run_time=0.5)
        self.esperar_frac(0.05)
        self.sfx("tic", -2)
        for f_ in fls:
            f_.clear_updaters()
        self.play(mover_palanca(bk, False), *[FadeOut(f_) for f_ in fls], Flash(bk, color=ROJO), run_time=0.5)
        ok = pastilla("está haciendo su trabajo", VERDE_OK, 24, True).next_to(e, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(ok), run_time=0.4)
        self.esperar_frac(0.35)
        no = VGroup(breaker("30", 0.46, 0.26).scale(3.6), equis(ROJO, 0.4)).arrange(RIGHT, buff=0.2)
        no.move_to([4.8, 2.9, 0])
        self.play(FadeIn(no), run_time=0.4)
        self.esperar_frac(0.4)
        sol = pastilla("solución: repartir en distintos circuitos", MARCA, 26, True).move_to([4.0, -2.7, 0])
        self.play(FadeIn(sol, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(red, i1, i2, tot, bk, e, ok, no, sol)

    def f_regleta(self):
        self.voz("regleta")
        reg = regleta().scale(2.0).move_to([-2.4, -0.4, 0])
        et = pastilla("15 A", TINTA, 26, True).next_to(reg, DOWN, buff=0.3)
        h = hervidor().scale_to_fit_height(1.6).move_to([-3.6, 2.2, 0])
        p = plancha().scale_to_fit_height(1.3).move_to([-1.0, 2.2, 0])
        cords = VGroup(cable(h.get_bottom(), P(-3.6, 0.4), reg[2][0].get_center(), color="#1D2939" if TEMA != "oscuro" else "#9AA6D1", w=4, suave=True),
                       cable(p.get_bottom(), P(-1.0, 0.6), reg[2][1].get_center(), color="#1D2939" if TEMA != "oscuro" else "#9AA6D1", w=4, suave=True))
        self.play(FadeIn(reg), FadeIn(et), run_time=0.5)
        self.play(FadeIn(h), FadeIn(p), Create(cords), run_time=0.7)
        self.esperar_frac(0.2)
        c = M(r"22.5\,\mathrm{A} > 15\,\mathrm{A}", 1.4, ROJO).move_to([3.6, 1.4, 0])
        self.play(Write(c), run_time=0.7)
        calor = resplandor(reg.get_center(), 1.8, ROJO, 10, 0.05)
        self.play(FadeIn(calor), reg[1].animate.set_fill("#FEE4E2"), run_time=0.8)
        r = pastilla("riesgo de incendio", ROJO, 28, True).move_to([3.6, 0.0, 0])
        self.play(FadeIn(r, scale=1.2), run_time=0.4)
        self.esperar_frac(0.5)
        s = pastilla("suma las corrientes antes de conectar", VERDE_OK, 24, True).move_to([3.6, -1.4, 0])
        self.play(FadeIn(s), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(reg, et, h, p, cords, c, calor, r, s)

    def f_serie(self):
        self.voz("serie")
        n = 7
        xs = np.linspace(-4.8, 4.8, n)
        y = 0.8
        linea = cable(P(-6.6, y), P(6.6, y), color="#2F6F3E", w=5)
        focos = VGroup(*[foco_led(True, 0.9).scale(0.85).move_to([x, y - 0.42, 0]) for x in xs])
        colores = [ROJO, AMBAR, VERDE_OK, I_COL, ROJO, AMBAR, VERDE_OK]
        brillos = VGroup(*[resplandor(f[0].get_center(), 0.6, c_, 8, 0.06) for f, c_ in zip(focos, colores)])
        self.play(Create(linea), FadeIn(focos), FadeIn(brillos), run_time=0.8)
        fl = corriente([P(-6.6, y + 0.0), P(6.6, y)], vel=0.8)
        self.add(fl)
        t1 = pastilla("misma corriente por todos", I_COL, 26, True).move_to([-2.6, -1.4, 0])
        t2 = pastilla("el voltaje se reparte", V_COL, 26, True).move_to([2.6, -1.4, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.esperar_frac(0.15)
        self.play(FadeIn(t2), run_time=0.4)
        self.esperar_frac(0.35)
        x = equis(ROJO, 0.4).move_to(focos[3].get_center() + UP * 0.9)
        fl.clear_updaters()
        apag = VGroup(*[foco_led(False, 0.9).scale(0.85).move_to(f) for f in focos])
        self.play(FadeIn(x, scale=1.3), FadeOut(brillos), FadeOut(fl), *[Transform(a, b) for a, b in zip(focos, apag)], run_time=0.6)
        t3 = pastilla("se abre el único camino → todo se apaga", ROJO, 26, True).move_to([0, -2.6, 0])
        self.play(FadeIn(t3), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(linea, focos, x, t1, t2, t3)

    # -------------------------------------------------------------- cable
    def f_cable(self):
        self.voz("cable")
        c = cable_hilos(7.0, FASE, 1.0, 1.4).move_to([-1.0, 1.2, 0])
        self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.7)
        e = VGroup(T("cobre · 12 AWG · 7 hilos", 30, TINTA, "HEAVY"), M(r"6.50\,\Omega \text{ por km}", 1.4, R_COL)).arrange(DOWN, buff=0.25).move_to([-1.0, -0.8, 0])
        self.esperar_frac(0.15)
        self.play(FadeIn(e[0]), Write(e[1]), run_time=0.8)
        carta = self.carta_nec("NEC 2020 · Cap. 9, Tabla 8", "Cobre 12 AWG, 7 hilos:\n6.50 Ω/km (a 75 °C).", (4.4, -2.7), 5.0)
        self.play(FadeIn(carta), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(c, e, carta)

    def f_caida(self):
        self.voz("caida")
        pan = centro_carga().scale(0.7).move_to([-5.4, 0.6, 0])
        t = placa_toma(P(0, 0)).scale(1.8).move_to([5.4, 0.6, 0])
        ida = cable(P(-4.6, 1.0), P(4.9, 1.0), color=FASE, w=6)
        vuelta = cable(P(4.9, 0.2), P(-4.6, 0.2), color=NEUTRO, w=6)
        self.play(FadeIn(pan), FadeIn(t), Create(ida), Create(vuelta), run_time=0.9)
        m25 = pastilla("25 m", TINTA, 26, True).move_to([0.2, 1.55, 0])
        self.play(FadeIn(m25), run_time=0.3)
        self.esperar_frac(0.05)
        fl = corriente([P(-4.6, 1.0), P(4.9, 1.0), P(4.9, 0.2), P(-4.6, 0.2)], vel=0.9)
        self.add(fl)
        m50 = pastilla("ida y vuelta: 50 m", MARCA, 26, True).move_to([0.2, -0.35, 0])
        self.play(FadeIn(m50), run_time=0.4)
        self.esperar_frac(0.05)
        c = self.pasos_calc([r"R = 6.50 \times 0.050 = 0.325\,\Omega", r"V = I \times R = 15 \times 0.325 \approx 4.9\,\mathrm{V}"],
                            [-1.0, -2.2, 0], [0.25, 0.2], size=1.0, buff=0.25)
        r = pastilla("llegan ≈ 115 V", ROJO, 30, True).move_to([5.0, -2.2, 0])
        self.play(FadeIn(r, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(pan, t, ida, vuelta, m25, fl, m50, c, r)

    def f_calor(self):
        self.voz("calor")
        del_ = cable_hilos(5.0, FASE, 0.45, 0.8).move_to([-1.6, 1.6, 0])
        gru = cable_hilos(5.0, FASE, 0.85, 1.0).move_to([-1.6, -1.2, 0])
        c1 = resplandor(del_.get_center() + LEFT * 0.4, 1.4, ROJO, 10, 0.05).stretch(2.2, 0)
        self.play(FadeIn(del_), run_time=0.5)
        self.play(FadeIn(c1), run_time=0.8)
        t1 = pastilla("energía → calor", ROJO, 26, True).move_to([4.6, 1.6, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.esperar_frac(0.3)
        self.play(FadeIn(gru), run_time=0.5)
        t2 = VGroup(*[pastilla(x, VERDE_OK, 22, True) for x in ("más grueso", "menos resistencia", "menos pérdida y calor")]).arrange(DOWN, buff=0.15).move_to([4.6, -1.2, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in t2], lag_ratio=0.5), run_time=1.2)
        self.cerrar_voz()
        self.limpiar(del_, gru, c1, t1, t2)

    def f_joule(self):
        self.voz("joule")
        f = MathTex(r"P", r"=", r"I^2", r"\times", r"R", color=TINTA).scale(2.4).move_to([0, 2.5, 0])
        f[0].set_color(P_COL)
        f[2].set_color(I_COL)
        f[4].set_color(R_COL)
        self.play(Write(f), run_time=0.8)
        self.esperar_frac(0.1)
        c = self.pasos_calc([r"15^2 = 225", r"225 \times 0.325 \approx 73\,\mathrm{W}"], [-2.0, 0.2, 0], [0.12, 0.15], size=1.3)
        r = self.resultado("≈ 73 W de calor en el cable", ROJO, [-1.0, -2.0, 0])
        cab = cable_hilos(3.0, FASE, 0.4, 0.5).move_to([4.4, 0.2, 0])
        glow = resplandor(cab.get_center(), 1.2, ROJO, 10, 0.05).stretch(1.8, 0)
        self.play(FadeIn(cab), FadeIn(glow), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(f, c, r, cab, glow)

    def f_medir(self):
        self.voz("medir")
        mm = multimetro().scale(1.1).move_to([-5.0, 0.2, 0])
        t = placa_toma(P(0, 0)).scale(2.2).move_to([-2.2, 0.6, 0])
        lec = T("120.4", 34, "#1D2939", "HEAVY", MONO).scale_to_fit_height(0.32).move_to(mm.lcd)
        roja, negra = punta_prueba(ROJO).move_to(t.get_center() + P(0.3, 1.4)), punta_prueba("#2A2E35").move_to(t.get_center() + P(-0.3, 1.4))
        self.play(FadeIn(mm), FadeIn(t), FadeIn(roja), FadeIn(negra), run_time=0.6)
        self.play(FadeIn(lec), run_time=0.3)
        e1 = pastilla("voltaje", V_COL, 24, True).next_to(mm, UP, buff=0.2)
        self.play(FadeIn(e1), run_time=0.3)
        self.esperar_frac(0.18)
        cab = VGroup(cable(P(0.4, -0.9), P(6.4, -0.9), color=FASE, w=8))
        gan = gancho_amperimetro().scale(1.4).move_to([3.4, -0.9 - 0.2, 0])
        gan.shift(cab[0].get_center() - gan[0].get_center() + DOWN * 0.15)
        lec2 = T("12.5 A", 30, "#1D2939", "HEAVY", MONO).scale_to_fit_width(gan.lcd.width * 0.85).move_to(gan.lcd)
        e2 = pastilla("corriente: abraza UN solo cable", I_COL, 24, True).move_to([3.4, 2.6, 0])
        self.play(Create(cab), FadeIn(gan), run_time=0.6)
        fl = corriente([P(0.4, -0.9), P(6.4, -0.9)], vel=0.8)
        self.add(fl)
        self.play(FadeIn(lec2), FadeIn(e2), run_time=0.4)
        self.esperar_frac(0.35)
        e3 = pastilla("resistencia: aparato desconectado", R_COL, 24, True).move_to([3.4, 1.9, 0])
        self.play(FadeIn(e3), run_time=0.4)
        self.esperar_frac(0.4)
        e4 = pastilla("frío ≠ funcionando", P_COL, 24, True).move_to([3.4, 1.2, 0])
        self.play(FadeIn(e4), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(mm, t, lec, roja, negra, e1, cab, gan, lec2, fl, e2, e3, e4)

    def f_seguridad(self):
        self.voz("seguridad")
        izq = VGroup(multimetro().scale(0.9), placa_toma(P(0, 0)).scale(1.8)).arrange(RIGHT, buff=0.6).move_to([-3.6, 0.4, 0])
        der = VGroup(multimetro().scale(0.9), hervidor().scale(1.2)).arrange(RIGHT, buff=0.6).move_to([3.6, 0.4, 0])
        for g in (izq, der):
            g.add(T("Ω", 34, R_COL, "HEAVY").next_to(g[0], UP, buff=0.15))
        tx1 = pastilla("Ω con voltaje: NUNCA", ROJO, 28, True).next_to(izq, DOWN, buff=0.4)
        tx2 = pastilla("Ω desconectado: sí", VERDE_OK, 28, True).next_to(der, DOWN, buff=0.4)
        x = equis(ROJO, 0.55).move_to(izq.get_corner(UR))
        ok = check(VERDE_OK, 0.55).move_to(der.get_corner(UR))
        self.play(FadeIn(izq), run_time=0.5)
        self.play(FadeIn(x, scale=1.3), FadeIn(tx1), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(FadeIn(der), FadeIn(ok, scale=1.3), FadeIn(tx2), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(izq, der, tx1, tx2, x, ok)

    def f_energia(self):
        self.voz("energia")
        rec = VGroup(RoundedRectangle(width=3.0, height=3.8, corner_radius=0.1, stroke_color=LINEA, stroke_width=1.6).set_fill(WHITE, 1),
                     T("RECIBO", 26, "#1D2939", "HEAVY"), *[Line(LEFT * 1.1, RIGHT * 1.1, stroke_color=METAL, stroke_width=3) for _ in range(4)],
                     T("kWh", 40, MARCA, "HEAVY"))
        rec[1].move_to(rec[0].get_top() + DOWN * 0.45)
        for k in range(4):
            rec[2 + k].move_to(rec[0].get_center() + UP * (0.7 - 0.35 * k))
        rec[6].move_to(rec[0].get_bottom() + UP * 0.7)
        rec.move_to([-5.0, 0.3, 0])
        self.play(FadeIn(rec, shift=UP * 0.2), run_time=0.6)
        f = M(r"\text{energía} = P \times t", 1.3).move_to([1.6, 2.7, 0])
        self.play(Write(f), run_time=0.7)
        self.esperar_frac(0.18)
        h = hervidor().scale_to_fit_height(1.0).move_to([-1.6, 1.0, 0])
        c1 = M(r"1500\,\mathrm{W} \times \tfrac{1}{6}\,\mathrm{h} = 0.25\,\mathrm{kWh}", 1.0).next_to(h, RIGHT, buff=0.4)
        self.play(FadeIn(h), Write(c1), run_time=0.8)
        self.esperar_frac(0.4)
        fo = foco_led(True, 0.9).scale_to_fit_height(1.0).move_to([-1.6, -1.2, 0])
        c2 = M(r"9\,\mathrm{W} \times 5\,\mathrm{h} \times 30 = 1.35\,\mathrm{kWh}", 1.0).next_to(fo, RIGHT, buff=0.4)
        self.play(FadeIn(fo), Write(c2), run_time=0.8)
        self.cerrar_voz()
        self.limpiar(rec, f, h, c1, fo, c2)

    def f_reto(self):
        self.voz("reto")
        tit = T("RETO", 60, MARCA, "HEAVY").move_to([0, 3.2, 0])
        ap = self.aparato(ventilador(), "60 W", (-4.0, 0.2), 2.4)
        self.play(FadeIn(tit), run_time=0.3)
        q = M(r"I = \; ?", 2.2, I_COL).move_to([2.4, 0.6, 0])
        self.play(Write(q), run_time=0.6)
        # cuenta regresiva hasta que la voz da la respuesta (~70 % del bloque)
        dur = self.resta()
        t_resp = dur * 0.62
        cuenta = None
        n = 3
        t0 = self.renderer.time
        espera = max(0.0, (t_resp - (n * 1.0)) - 0.2)
        self.wait(espera * 0.5)
        for k in range(n, 0, -1):
            c_ = T(str(k), 90, P_COL, "HEAVY").move_to([2.4, -1.6, 0])
            self.play(FadeIn(c_, scale=1.4) if cuenta is None else Transform(cuenta, c_), run_time=0.3)
            cuenta = cuenta or c_
            self.wait(0.7)
        self.play(FadeOut(cuenta), run_time=0.2)
        self.esperar_frac(0.35)
        r = M(r"I = \dfrac{60}{120} = 0.5\,\mathrm{A}", 1.4, I_COL).move_to(q)
        self.play(Transform(q, r), run_time=0.6)
        ok = pastilla("medio amperio", VERDE_OK, 30, True).move_to([2.4, -1.4, 0])
        self.play(FadeIn(ok, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, ap, q, ok)

    def f_ejercicio(self):
        self.voz("ejercicio")
        bk = breaker("20", 0.46, 0.26).scale(3.6).move_to([0, 3.0, 0])
        e = T("circuito de 20 A", 24, TINTA, "HEAVY").next_to(bk, RIGHT, buff=0.3)
        caf = cafetera().scale_to_fit_height(1.8).move_to([-5.0, 0.8, 0])
        tos = tostadora().scale_to_fit_height(1.3).move_to([-5.0, -1.8, 0])
        e1 = etiqueta_w("900 W").scale(0.8).next_to(caf, RIGHT, buff=0.3)
        e2 = etiqueta_w("800 W").scale(0.8).next_to(tos, RIGHT, buff=0.3)
        self.play(FadeIn(bk), FadeIn(e), run_time=0.5)
        self.play(FadeIn(caf), FadeIn(e1), FadeIn(tos), FadeIn(e2), run_time=0.7)
        q = pastilla("¿se dispara?", ROJO, 28, True).move_to([3.8, 1.9, 0])
        self.play(FadeIn(q), run_time=0.3)
        self.esperar_frac(0.12)
        c1 = M(r"900 \div 120 = 7.5\,\mathrm{A}", 1.1).move_to([2.6, 0.8, 0])
        self.play(Write(c1), run_time=0.6)
        self.esperar_frac(0.2)
        c2 = M(r"800 \div 120 \approx 6.7\,\mathrm{A}", 1.1).move_to([2.6, -0.2, 0])
        self.play(Write(c2), run_time=0.6)
        self.esperar_frac(0.25)
        c3 = M(r"7.5 + 6.7 \approx 14.2\,\mathrm{A} < 20\,\mathrm{A}", 1.1, VERDE_OK).move_to([2.6, -1.3, 0])
        self.play(Write(c3), run_time=0.7)
        self.esperar_frac(0.4)
        ok = pastilla("el breaker aguanta", VERDE_OK, 30, True).move_to([2.6, -2.6, 0])
        self.play(FadeIn(ok, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(bk, e, caf, tos, e1, e2, q, c1, c2, c3, ok)

    def f_repaso(self):
        self.voz("repaso")
        tit = T("REPASO", 50, TINTA, "HEAVY").move_to([0, 3.4, 0])
        self.play(FadeIn(tit), run_time=0.3)
        tres = VGroup(*[VGroup(M(l, 1.8, c_), T(t, 26, TINTA, "BOLD")).arrange(DOWN, buff=0.15)
                        for l, t, c_ in (("V", "empuja", V_COL), ("I", "fluye", I_COL), ("R", "se opone", R_COL))]).arrange(RIGHT, buff=1.8).move_to([0, 1.8, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in tres], lag_ratio=0.5), run_time=1.6)
        self.esperar_frac(0.15)
        cartas = VGroup()
        for tex, txt, col in ((r"I = \dfrac{V}{R}", "corriente", I_COL), (r"P = V \times I", "potencia", P_COL),
                              (r"I_{total} = I_1 + I_2", "en paralelo", MARCA), (r"\text{cable} \to \text{calor}", "y caída de voltaje", ROJO)):
            caja = tarjeta(3.4, 2.4, METAL)
            m = M(tex, 1.1, col).move_to(caja.get_center() + UP * 0.25)
            t = T(txt, 22, TINTA2, "BOLD").move_to(caja.get_center() + DOWN * 0.75)
            cartas.add(VGroup(caja, m, t))
        cartas.arrange(RIGHT, buff=0.3).move_to([0, -1.4, 0])
        for k, c_ in enumerate(cartas):
            self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
            self.esperar_frac([0.2, 0.25, 0.4, 0.5][k])
        self.cerrar_voz()
        self.limpiar(tit, tres, cartas)

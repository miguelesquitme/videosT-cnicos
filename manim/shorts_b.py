"""Shorts V12–V17 rehechos (estándar nuevo: 1:30–3:00, fundamento técnico, diseño distinto en cada escena).
Guiones y fuentes en guiones_b.py.  Render: FORMATO=v VOZ=eleven manim -qh -o final shorts_b.py V12B
"""
from comun_e import *
from comun_e import _osc, _cla
from taller import corriente, foco_led, P, tomacorriente, regleta, clavija
from nema import NEGRO_BK, breaker, mover_palanca, multimetro, punta_prueba
from dibujos_aves import persona, brazo, check, equis, PIEL
import shorts_v
from shorts_v import ShortV, onda, CLARO, extintor, gotas, cara
from taller import microondas
from v11_led import CALOR, AMARILLO_F, ondas_calor, foton
from guiones_b import GUIONES_B

shorts_v.SHORTS.update(GUIONES_B)

_pastilla, _T = pastilla, T


def pastilla(*a, **k):
    m = _pastilla(*a, **k)
    return m.scale_to_fit_width(8.3) if m.width > 8.3 else m


def T(*a, **k):
    m = _T(*a, **k)
    return m.scale_to_fit_width(8.4) if m.width > 8.4 else m

CIAN = "#6FF2FF"
NARANJA = "#F79009"
VERDE_T = "#2E9E4F"
AMAR_FR = "#F5C400"
AZUL_N = "#2F6FDB"
GRIS_N = "#AEB4BF"
COBRE_V = "#D9844A"


# ====================================================================== piezas comunes
def caja_dato(titulo, cuerpo, color=MARCA, w=4.2, size=30):
    cab = T(titulo, size + 4, color, "HEAVY")
    lineas = VGroup(*[T(l, size, TINTA, "MEDIUM") for l in cuerpo.split("\n")]).arrange(DOWN, buff=0.07)
    g = VGroup(cab, lineas).arrange(DOWN, buff=0.16)
    caja = tarjeta(max(w, g.width + 0.5), g.height + 0.45, color="#4A5AA0")
    barra = RoundedRectangle(width=0.12, height=caja.height - 0.2, corner_radius=0.05, stroke_width=0).set_fill(color, 1)
    barra.move_to(caja.get_left() + RIGHT * 0.16)
    g.move_to(caja).shift(RIGHT * 0.08)
    return VGroup(caja, barra, g)


def seccion(area, k=0.62, aisl=True, color=COBRE_V, borde_col=NEGRO_BK):
    """Corte transversal de un conductor: radio proporcional a la raíz del área (mm²)."""
    r = np.sqrt(area / PI) * k
    g = VGroup()
    if aisl:
        g.add(Circle(radius=r + 0.16 + r * 0.25, stroke_color="#8F9AC8", stroke_width=2).set_fill(borde_col, 1))
    g.add(Circle(radius=r, stroke_color=_osc(color, 0.35), stroke_width=2).set_fill(color, 1),
          Arc(radius=r * 0.65, start_angle=PI * 0.55, angle=PI * 0.35).set_stroke(WHITE, 3, 0.55))
    g.r = r
    return g


def cable_lateral(largo=6.0, h=0.5, color=NEGRO_BK, cobre=True):
    ais = RoundedRectangle(width=largo, height=h, corner_radius=h / 2, stroke_color="#8F9AC8", stroke_width=2).set_fill(color, 1)
    g = VGroup(ais)
    if cobre:
        cu = Rectangle(width=0.7, height=h * 0.55, stroke_color=_osc(COBRE_V, 0.3), stroke_width=1.5).set_fill(COBRE_V, 1)
        cu.next_to(ais, RIGHT, buff=-0.05)
        g.add(cu)
    return g


def llama(s=1.0):
    capas = VGroup()
    for k, (col, f) in enumerate([("#E5484D", 1.0), ("#F79009", 0.72), ("#FFD84D", 0.45)]):
        m = VMobject().set_points_smoothly([P(-0.5 * f, 0), P(-0.55 * f, 0.5 * f), P(-0.2 * f, 1.0 * f), P(-0.05 * f, 1.6 * f),
                                            P(0.15 * f, 1.0 * f), P(0.45 * f, 0.7 * f), P(0.5 * f, 0.3 * f), P(0.35 * f, 0), P(-0.5 * f, 0)])
        m.set_fill(col, 1).set_stroke(width=0)
        capas.add(m)
    capas.arrange(ORIGIN, aligned_edge=DOWN)
    capas.scale(s)
    capas.t = 0.0
    base = capas.get_bottom()

    def upd(m, dt):
        m.t += dt
        for i, c in enumerate(m):
            f = 1 + 0.06 * np.sin(m.t * 11 + i * 1.7)
            c.stretch_to_fit_height(c.alto0 * f, about_point=base)
    for c in capas:
        c.alto0 = c.height
    capas.add_updater(upd)
    return capas


def humo(c, n=4):
    return VGroup(*[Circle(radius=0.25 + 0.1 * k, stroke_width=0).set_fill("#98A2B3", 0.25 - 0.04 * k).move_to(c + UP * (0.5 * k) + RIGHT * 0.2 * np.sin(k))
                    for k in range(n)])


def corazon(s=1.0, color=ROJO):
    a = Circle(radius=0.32).move_to(P(-0.26, 0.15))
    b = Circle(radius=0.32).move_to(P(0.26, 0.15))
    t = Polygon(P(-0.56, 0.05), P(0.56, 0.05), P(0, -0.7))
    g = VGroup(a, b, t).set_fill(color, 1).set_stroke(width=0)
    return g.scale(s)


def gfci(c=ORIGIN):
    placa = RoundedRectangle(width=1.7, height=2.9, corner_radius=0.12, stroke_color="#C7C5BE", stroke_width=2).set_fill("#F7F7F5", 1)
    tomas = VGroup(*[cara(1.6, True).move_to(P(0, y)) for y in (0.85, -0.85)])
    test = RoundedRectangle(width=0.55, height=0.26, corner_radius=0.05, stroke_width=1).set_fill("#2A2E35", 1).move_to(P(-0.33, 0))
    reset = RoundedRectangle(width=0.55, height=0.26, corner_radius=0.05, stroke_width=1).set_fill(ROJO, 1).move_to(P(0.33, 0))
    tt = T("TEST", 11, WHITE, "HEAVY").move_to(test)
    tr = T("RESET", 11, WHITE, "HEAVY").move_to(reset)
    g = VGroup(placa, tomas, test, reset, tt, tr).move_to(c)
    g.reset = VGroup(reset, tr)
    return g


def azulejos(w=8.4, h=7.0, c=ORIGIN, l=0.7):
    g = VGroup()
    nx, ny = int(w / l), int(h / l)
    for i in range(nx):
        for j in range(ny):
            g.add(Square(l * 0.96, stroke_width=0).set_fill("#1E3E6E", 0.6).move_to(c + np.array([(i - (nx - 1) / 2) * l, (j - (ny - 1) / 2) * l, 0])))
    return g


def regla_log(y0, y1, vmin, vmax, x=0.0):
    def ypos(v):
        return y0 + (np.log10(v) - np.log10(vmin)) / (np.log10(vmax) - np.log10(vmin)) * (y1 - y0)
    return ypos


# ====================================================================== V12 · corriente que mata
class V12B(ShortV):
    CLAVE = "v12b"

    def cuerpo(self):
        # gancho: persona tocando un conductor, la corriente la atraviesa
        self.voz("gancho")
        base = np.array([-1.9, -5.0, 0])
        pe = persona("#2F6FB0").scale(2.1).move_to(base, aligned_edge=DOWN)
        hombro = base + 2.1 * np.array([0.36, 1.92, 0])
        mano = np.array([0.4, 0.6, 0])
        br = brazo(hombro, mano, "#2F6FB0", 22)
        br2 = brazo(base + 2.1 * np.array([-0.36, 1.92, 0]), base + 2.1 * np.array([-0.6, 1.05, 0]), "#2F6FB0", 22)
        suelo = Line([-4.5, -5.0, 0], [4.5, -5.0, 0]).set_stroke("#4A5AA0", 4)
        cab = VGroup(Line(mano + RIGHT * 0.25, [4.6, 0.6, 0]).set_stroke("#8F9AC8", 24), Line(mano + RIGHT * 0.25, [4.6, 0.6, 0]).set_stroke(NEGRO_BK, 18),
                     Line(mano + RIGHT * 0.05, mano + RIGHT * 0.45).set_stroke(COBRE_V, 10))
        self.play(FadeIn(suelo), FadeIn(pe), FadeIn(br2), run_time=0.5)
        self.play(Create(cab), Create(br), run_time=0.6)
        self.add(br, cab)
        pie = base + 2.1 * np.array([0.19, 0.05, 0])
        ruta = [[4.6, 0.6, 0], mano, hombro, hombro + DOWN * 1.6 + LEFT * 0.35, pie + UP * 1.0, pie, pie + DOWN * 0.02 + RIGHT * 2.5]
        cur = corriente(ruta, vel=1.2, escala=1.5)
        self.sfx("pop", -12)
        self.add(cur)
        fl = resplandor(mano, 0.6, AMBAR, 8, 0.08)
        self.play(FadeIn(fl), run_time=0.3)
        q = VGroup(pastilla("¿VOLTAJE?", AMBAR, 40, True), pastilla("¿CORRIENTE?", CIAN, 40, True)).arrange(DOWN, buff=0.3).move_to([1.7, 3.0, 0])
        self.frac(0.15)
        self.play(FadeIn(q[0], shift=LEFT * 0.3), run_time=0.35)
        self.play(FadeIn(q[1], shift=LEFT * 0.3), run_time=0.35)
        self.frac(0.25)
        ck = check(VERDE_OK, 0.32).next_to(q[1], LEFT, buff=0.15)
        self.play(q[0].animate.set_opacity(0.3), q[1].animate.scale(1.15), FadeIn(ck, scale=1.4), run_time=0.45)
        self.cerrar_voz(0.1)
        self.limpiar(pe, br, br2, cab, cur, fl, suelo, q, ck)

        # p1: amperio vs miliamperio + LED 75 mA
        self.voz("p1")
        barra = Rectangle(width=7.6, height=0.7, stroke_color=CIAN, stroke_width=3).set_fill(CIAN, 0.18).move_to([0, 2.8, 0])
        t1 = T("1 A", 54, CIAN, "HEAVY").next_to(barra, UP, buff=0.15)
        self.play(GrowFromEdge(barra, LEFT), FadeIn(t1), run_time=0.6)
        rebanadas = VGroup(*[Line(barra.get_corner(DL) + RIGHT * x, barra.get_corner(UL) + RIGHT * x).set_stroke(CIAN, 1, 0.5)
                             for x in np.linspace(0.0076, 7.6, 100, endpoint=False)])
        self.play(Create(rebanadas, lag_ratio=0.01), run_time=0.8)
        lupa = Rectangle(width=0.076 * 6, height=0.9, stroke_color=AMBAR, stroke_width=4).move_to(barra.get_left() + RIGHT * 0.23)
        mA = VGroup(T("1 mA", 64, AMBAR, "HEAVY"), T("= una milésima de amperio", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, 1.0, 0])
        self.frac(0.1)
        self.play(Create(lupa), FadeIn(mA, shift=DOWN * 0.2), run_time=0.6)
        led = foco_led(True, 0.9).scale(2.6).move_to([-2.4, -2.6, 0])
        gl = resplandor(led.vidrio.get_center(), 1.5, AMBAR, 10, 0.05)
        cuenta = VGroup(T("9 W ÷ 120 V", 40, TINTA, "BOLD"), T("= 0.075 A", 40, TINTA, "BOLD"), T("= 75 mA", 64, AMBAR, "HEAVY")).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([1.5, -2.6, 0])
        self.frac(0.25)
        self.play(FadeIn(gl), FadeIn(led, shift=UP * 0.2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cuenta], lag_ratio=0.5), run_time=1.2)
        self.cerrar_voz(0.1)
        self.limpiar(barra, t1, rebanadas, lupa, mA, led, gl, cuenta)

        # p2–p4: escala logarítmica de efectos (OSHA)
        y0, y1 = -5.2, 3.6
        yp = regla_log(y0, y1, 0.7, 3000)
        xb = -2.9
        tubo_ = RoundedRectangle(width=0.55, height=y1 - y0 + 0.4, corner_radius=0.27, stroke_color=CLARO, stroke_width=2.5).set_fill("#0B1C3D", 1).move_to([xb, (y0 + y1) / 2, 0])
        zonas = [(1, 5.5, "#7FD1AE"), (5.5, 16.5, AMBAR), (16.5, 99.5, NARANJA), (99.5, 2000, ROJO)]
        rell = [Rectangle(width=0.4, height=yp(b) - yp(a), stroke_width=0).set_fill(c, 0.9).move_to([xb, (yp(a) + yp(b)) / 2, 0]) for a, b, c in zonas]
        marcas = VGroup(*[VGroup(Line([xb + 0.3, yp(v), 0], [xb + 0.5, yp(v), 0]).set_stroke(CLARO, 2),
                                 T(f"{v}", 24, CLARO, "BOLD").next_to([xb + 0.5, yp(v), 0], RIGHT, buff=0.08)) for v in (1, 5, 16, 100, 2000)])
        unidad = T("mA", 30, CLARO, "HEAVY").next_to(tubo_, DOWN, buff=0.12)
        src = fuente("OSHA eTool · NIOSH 1998 · 60 Hz, mano-pie, 1 s", [0.6, -6.1, 0], 22)

        def tarjeta_z(a, titulo, txt, col, ycen):
            c = caja_dato(titulo, txt, col, 5.2, 28).move_to([1.6, ycen, 0])
            con = DashedLine([xb + 0.3, yp(a), 0], c.get_left(), color=col, dash_length=0.08)
            return VGroup(con, c)

        self.voz("p2")
        self.play(FadeIn(tubo_), FadeIn(unidad), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(m) for m in marcas], lag_ratio=0.15), FadeIn(src), run_time=0.7)
        self.frac(0.35)
        self.play(GrowFromEdge(rell[0], DOWN), run_time=0.5)
        z1 = tarjeta_z(1.6, "1 mA", "cosquilleo", "#7FD1AE", -4.4)
        self.play(FadeIn(z1, shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.4)
        z2 = tarjeta_z(5, "5 mA", "choque leve: te sueltas", "#7FD1AE", -2.9)
        self.play(FadeIn(z2, shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)

        self.voz("p3")
        self.play(GrowFromEdge(rell[1], DOWN), run_time=0.5)
        z3 = tarjeta_z(10, "6 – 16 mA", "dolor · pierdes el control\nNO te puedes soltar", AMBAR, -1.2)
        self.play(FadeIn(z3, shift=RIGHT * 0.2), run_time=0.45)
        self.cerrar_voz(0.1)

        self.voz("p4")
        self.play(GrowFromEdge(rell[2], DOWN), run_time=0.5)
        z4 = tarjeta_z(40, "17 – 99 mA", "dolor extremo\nparo respiratorio", NARANJA, 0.6)
        self.play(FadeIn(z4, shift=RIGHT * 0.2), run_time=0.45)
        self.frac(0.35)
        self.play(GrowFromEdge(rell[3], DOWN), run_time=0.5)
        z5 = tarjeta_z(400, "100 mA o más", "fibrilación ventricular\nmuerte probable", ROJO, 2.55)
        cz = corazon(0.5).next_to(z5, RIGHT, buff=0.1).shift(LEFT * 0.75 + UP * 0.05)
        self.play(FadeIn(z5, shift=RIGHT * 0.2), run_time=0.45)
        ecg = VMobject().set_points_as_corners([P(x, 0.25 * np.sin(x * 23) * np.cos(x * 7)) for x in np.linspace(0, 4.4, 60)]).set_stroke(ROJO, 4)
        ecg.move_to([1.6, 3.9, 0])
        self.play(Create(ecg), FadeIn(cz, scale=0.6), run_time=0.8)
        self.cerrar_voz(0.1)

        # p5: el LED (75 mA) ya está en zona mortal; ley de Ohm
        self.voz("p5")
        led_m = VGroup(Triangle().scale(0.18).rotate(-PI / 2).set_fill(AMBAR, 1).set_stroke(width=0),
                       T("LED\n75 mA", 26, AMBAR, "HEAVY")).arrange(LEFT, buff=0.1)
        led_m.next_to([xb - 0.3, yp(75), 0], LEFT, buff=0.05)
        if led_m.get_left()[0] < -4.4:
            led_m.shift(RIGHT * (-4.4 - led_m.get_left()[0]))
        self.play(FadeIn(led_m, shift=RIGHT * 0.3), Indicate(z4, color=NARANJA, scale_factor=1.05), run_time=0.7)
        self.frac(0.3)
        self.limpiar(z1, z2, z3, z4, z5, cz, ecg, t=0.3)
        ohm = VGroup(T("I = V / R", 86, CIAN, "HEAVY"), T("corriente = voltaje ÷ resistencia", 28, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([1.6, 1.0, 0])
        self.play(Write(ohm[0]), FadeIn(ohm[1]), run_time=0.9)
        self.cerrar_voz(0.1)

        # p6: piel seca vs mojada
        self.voz("p6")
        self.play(ohm.animate.scale(0.7).move_to([1.6, 3.4, 0]), run_time=0.4)
        seca = caja_dato("piel seca", "120 V ÷ 100 000 Ω\n= 1 mA", "#7FD1AE", 5.2, 32).move_to([1.6, 1.0, 0])
        moj = caja_dato("piel mojada", "120 V ÷ 1 000 Ω\n= 120 mA", ROJO, 5.2, 32).move_to([1.6, -2.1, 0])
        gt = gotas(moj.get_corner(UR) + LEFT * 0.6 + DOWN * 0.3, 5, "#7FD1FF").scale(0.7)
        p_s = Dot([xb, yp(1), 0], radius=0.17, color=WHITE)
        self.frac(0.05)
        self.play(FadeIn(seca, shift=RIGHT * 0.2), FadeIn(p_s, scale=0.4), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(moj, shift=RIGHT * 0.2), FadeIn(gt), run_time=0.5)
        self.play(p_s.animate.move_to([xb, yp(120), 0]).set_color(ROJO), run_time=1.4, rate_func=rate_functions.ease_in_out_cubic)
        self.play(Flash(p_s, color=ROJO, flash_radius=0.5, line_length=0.3), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(tubo_, *rell, marcas, unidad, src, led_m, ohm, seca, moj, gt, p_s)

        # p7: GFCI en el baño
        self.voz("p7")
        az = azulejos(8.6, 9.0, np.array([0, -0.4, 0]))
        gf = gfci([0, 0.6, 0]).scale(1.6)
        self.play(FadeIn(az), FadeIn(gf, scale=0.9), run_time=0.6)
        lab = pastilla("GFCI · NEC 210.8", MARCA, 34, True).move_to([0, 3.9, 0])
        self.play(FadeIn(lab), run_time=0.3)
        ruta = [gf.get_bottom() + DOWN * 0.1, gf.get_bottom() + DOWN * 0.8, [2.6, gf.get_bottom()[1] - 0.8, 0], [2.6, -4.2, 0]]
        fuga = corriente(ruta, vel=1.0, escala=1.4, color=ROJO)
        fl = T("fuga de pocos mA", 40, ROJO, "HEAVY").move_to([-1.3, -3.4, 0])
        self.frac(0.25)
        self.add(fuga)
        self.play(FadeIn(fl), run_time=0.4)
        self.frac(0.25)
        self.sfx("tic", -6)
        self.play(gf.reset.animate.shift(RIGHT * 0.12).scale(1.12), run_time=0.2)
        self.remove(fuga)
        corte = pastilla("¡corta en una fracción de segundo!", VERDE_OK, 36, True).move_to([0, -5.0, 0])
        self.play(FadeIn(corte, scale=1.1), fl.animate.set_opacity(0.3), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(az, gf, lab, fl, corte)

        # p8: reglas
        self.voz("p8")
        reglas = VGroup(*[VGroup(ic, T(t, 40, TINTA, "HEAVY")).arrange(RIGHT, buff=0.35) for ic, t in [
            (check(VERDE_OK, 0.32), "importa la corriente"), (check(VERDE_OK, 0.32), "trabaja sin tensión"), (check(VERDE_OK, 0.32), "manos secas")]])
        reglas.arrange(DOWN, buff=0.7, aligned_edge=LEFT).scale(1.2).move_to([0, -0.8, 0])
        v120 = T("120 V", 140, ROJO, "HEAVY").move_to([0, 2.6, 0])
        self.play(FadeIn(v120, scale=1.2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in reglas], lag_ratio=0.5), run_time=1.6)
        self.cerrar_voz(0.1)
        self.limpiar(v120, reglas)
        self.final("La corriente es la que mata")


# ====================================================================== V13 · por qué se calienta un cable
class V13B(ShortV):
    CLAVE = "v13b"

    def cuerpo(self):
        self.voz("gancho")
        cab = cable_lateral(7.4, 1.3).move_to([-0.3, 0.4, 0])
        self.play(FadeIn(cab, shift=RIGHT * 0.3), run_time=0.5)
        cur = corriente([[-3.9, 0.4, 0], [3.4, 0.4, 0]], vel=1.6, escala=1.8)
        self.add(cur)
        self.play(cab[0].animate.set_fill("#5A1E12", 1), run_time=1.2)
        gl = resplandor(cab.get_center(), 2.6, CALOR, 12, 0.05)
        oc = ondas_calor(np.array([-0.3, 1.3, 0]), 7, CALOR, 1.6, 0.9)
        self.play(FadeIn(gl), Create(oc), run_time=0.6)
        q = T("¿de dónde sale el calor?", 46, TINTA, "HEAVY").move_to([0, -2.4, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cab, cur, gl, oc, q)

        # p1: resistencia del cobre (Tabla 8)
        self.voz("p1")
        s12 = seccion(3.31, 1.1).move_to([-2.0, 1.6, 0])
        l12 = T("12 AWG", 40, TINTA, "HEAVY").next_to(s12, DOWN, buff=0.2)
        self.play(FadeIn(s12, scale=0.8), FadeIn(l12), run_time=0.5)
        km = VGroup(Line([-3.8, -1.6, 0], [3.8, -1.6, 0]).set_stroke(COBRE_V, 10),
                    Line([-3.8, -1.9, 0], [-3.8, -1.3, 0]).set_stroke(CLARO, 3), Line([3.8, -1.9, 0], [3.8, -1.3, 0]).set_stroke(CLARO, 3),
                    T("1 km", 32, CLARO, "BOLD").move_to([0, -2.2, 0]))
        self.frac(0.25)
        self.play(Create(km[0]), FadeIn(km[1:]), run_time=0.7)
        dato = caja_dato("NEC · Tabla 8", "12 AWG cobre trenzado\n6.50 Ω por km", MARCA, 4.3, 28).move_to([1.9, 1.6, 0])
        self.play(FadeIn(dato, shift=LEFT * 0.2), run_time=0.45)
        self.frac(0.4)
        nz = pastilla("poco… pero no es cero", AMBAR, 38, True).move_to([0, -3.7, 0])
        self.play(FadeIn(nz, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(s12, l12, km, dato, nz)

        # p2: red de átomos que vibran (efecto Joule)
        self.voz("p2")
        marco = RoundedRectangle(width=8.2, height=5.0, corner_radius=0.3, stroke_color=COBRE_V, stroke_width=3).set_fill("#2A1A12", 0.5).move_to([0, 0.5, 0])
        atomos = VGroup(*[Circle(radius=0.3, stroke_color=_osc(COBRE_V, 0.3), stroke_width=2).set_fill(COBRE_V, 1).move_to([x, y, 0])
                          for x in np.linspace(-3.3, 3.3, 7) for y in np.linspace(-1.3, 2.3, 4)])
        for a in atomos:
            a.c0 = a.get_center()
        self.play(FadeIn(marco), LaggedStart(*[FadeIn(a, scale=0.5) for a in atomos], lag_ratio=0.01), run_time=0.7)
        rng = np.random.default_rng(1)
        elec = VGroup(*[Dot([x, y, 0], radius=0.09, color=CIAN) for x, y in zip(rng.uniform(-3.9, 3.9, 22), rng.uniform(-1.6, 2.6, 22))])
        for e in elec:
            e.v = np.array([rng.uniform(1.4, 2.2), rng.uniform(-1.2, 1.2), 0])

        def mov_e(m, dt):
            for e in m:
                p = e.get_center() + e.v * dt
                if p[1] > 2.7 or p[1] < -1.7:
                    e.v[1] *= -1
                if p[0] > 3.95:
                    p[0] = -3.95
                e.move_to(p)
        elec.add_updater(mov_e)
        self.add(elec)
        amp = ValueTracker(0.0)
        reloj = ValueTracker(0.0)

        def vib(m):
            t = reloj.get_value()
            for i, a in enumerate(m):
                a.move_to(a.c0 + amp.get_value() * np.array([np.sin(t * 31 + i), np.cos(t * 27 + 2 * i), 0]))
        atomos.add_updater(vib)
        reloj.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(reloj)
        self.frac(0.2)
        self.play(amp.animate.set_value(0.07), atomos.animate.set_fill("#FF7A3D"), run_time=1.6)
        oc = ondas_calor(np.array([0, 3.0, 0]), 6, CALOR, 0.9, 1.2)
        jl = pastilla("efecto Joule: choques → vibración → calor", CALOR, 30, True).move_to([0, -2.9, 0])
        self.play(Create(oc), FadeIn(jl), run_time=0.6)
        self.cerrar_voz(0.1)
        atomos.clear_updaters()
        reloj.clear_updaters()
        self.remove(reloj)
        self.limpiar(marco, atomos, elec, oc, jl)

        # p3: P = I²R, parábola
        self.voz("p3")
        f = VGroup(T("P = I² × R", 84, CALOR, "HEAVY")).move_to([0, 3.4, 0])
        self.play(Write(f), run_time=0.8)
        ax = Axes(x_range=[0, 22, 5], y_range=[0, 100, 25], x_length=6.6, y_length=4.6, tips=False,
                  axis_config={"color": CLARO, "stroke_width": 3, "include_ticks": False}).move_to([0.2, -0.6, 0])
        lx = T("corriente", 26, CLARO, "BOLD").next_to(ax.x_axis, DOWN, buff=0.15)
        ly = T("calor", 26, CLARO, "BOLD").next_to(ax.y_axis, UP, buff=0.12)
        curva = ax.plot(lambda x: 0.2 * x * x, x_range=[0, 21.5], color=CALOR, stroke_width=6)
        self.frac(0.15)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly), run_time=0.5)
        self.play(Create(curva), run_time=1.0)
        p1_ = ax.c2p(10, 20); p2_ = ax.c2p(20, 80)
        g1 = VGroup(DashedLine(ax.c2p(10, 0), p1_, color=TINTA), DashedLine(ax.c2p(0, 20), p1_, color=TINTA), Dot(p1_, radius=0.12, color=AMBAR),
                    T("I", 30, AMBAR, "HEAVY").next_to(ax.c2p(10, 0), DOWN, buff=0.1), T("1×", 30, AMBAR, "HEAVY").next_to(ax.c2p(0, 20), LEFT, buff=0.1))
        g2 = VGroup(DashedLine(ax.c2p(20, 0), p2_, color=TINTA), DashedLine(ax.c2p(0, 80), p2_, color=TINTA), Dot(p2_, radius=0.12, color=ROJO),
                    T("2I", 30, ROJO, "HEAVY").next_to(ax.c2p(20, 0), DOWN, buff=0.1), T("4×", 30, ROJO, "HEAVY").next_to(ax.c2p(0, 80), LEFT, buff=0.1))
        self.frac(0.2)
        self.play(FadeIn(g1), run_time=0.4)
        self.frac(0.25)
        self.play(FadeIn(g2), run_time=0.4)
        msg = pastilla("doble corriente = cuatro veces calor", ROJO, 32, True).move_to([0, -4.3, 0])
        self.play(FadeIn(msg, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(f, ax, lx, ly, curva, g1, g2, msg)

        # p4: circuito de 15 m
        self.voz("p4")
        tab = RoundedRectangle(width=1.3, height=1.9, corner_radius=0.1, stroke_color=METAL_OSC, stroke_width=2).set_fill("#C9CED6", 1).move_to([-3.4, 2.4, 0])
        brk = breaker("20", lado=1).scale(2.0).move_to(tab)
        tm = cara(4.0).move_to([3.4, 2.4, 0])
        ida = Line([-2.7, 2.65, 0], [2.9, 2.65, 0]).set_stroke(NEGRO_BK, 9)
        vuelta = Line([-2.7, 2.15, 0], [2.9, 2.15, 0]).set_stroke("#E8E8E8", 9)
        self.play(FadeIn(tab), FadeIn(brk), FadeIn(tm), run_time=0.4)
        self.play(Create(ida), Create(vuelta), run_time=0.6)
        cota = VGroup(DoubleArrow([-2.7, 3.3, 0], [2.9, 3.3, 0], buff=0, color=CLARO, stroke_width=3, tip_length=0.2),
                      T("15 m", 30, CLARO, "BOLD").move_to([0.1, 3.65, 0]))
        rr = pastilla("ida + vuelta = 30 m → 0.2 Ω", MARCA, 32, True).move_to([0, 1.2, 0])
        self.play(FadeIn(cota), run_time=0.3)
        self.frac(0.1)
        self.play(FadeIn(rr), run_time=0.4)
        cur = corriente([[-2.7, 2.65, 0], [2.9, 2.65, 0], [2.9, 2.15, 0], [-2.7, 2.15, 0]], vel=1.2, escala=1.2)
        self.add(cur)

        def fila(I, W, col, y, k):
            b = Rectangle(width=W * 0.058, height=0.75, stroke_width=0).set_fill(col, 0.95)
            b.move_to([-2.2 + W * 0.058 / 2, y, 0])
            ti = T(f"{I} A", 40, TINTA, "HEAVY").move_to([-3.4, y, 0])
            tw = T(f"≈ {W} W", 40, col, "HEAVY").next_to(b, RIGHT, buff=0.2)
            return VGroup(ti, b, tw)
        f10 = fila(10, 20, AMBAR, -0.8, 1)
        f20 = fila(20, 78, ROJO, -2.3, 2)
        tit = T("calor perdido en el cable", 28, CLARO, "BOLD").move_to([0, 0.2, 0])
        self.frac(0.2)
        self.play(FadeIn(tit), FadeIn(f10[0]), GrowFromEdge(f10[1], LEFT), FadeIn(f10[2]), run_time=0.6)
        self.frac(0.3)
        self.play(FadeIn(f20[0]), GrowFromEdge(f20[1], LEFT), FadeIn(f20[2]), run_time=0.6)
        x4 = T("×4", 60, ROJO, "HEAVY").move_to([2.7, -3.7, 0])
        self.play(FadeIn(x4, scale=1.3), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tab, brk, tm, ida, vuelta, cota, rr, cur, f10, f20, tit, x4)

        # p5: Tabla 310.16 — termómetros por temperatura de aislamiento
        self.voz("p5")
        tit = caja_dato("NEC · Tabla 310.16", "12 AWG cobre", MARCA, 5.0, 30).move_to([0, 3.4, 0])
        self.play(FadeIn(tit), run_time=0.4)
        cols = VGroup()
        for k, (tc, a, col) in enumerate([("60 °C", "20 A", AMBAR), ("75 °C", "25 A", NARANJA), ("90 °C", "30 A", ROJO)]):
            x = -2.7 + 2.7 * k
            h = 1.6 + 0.9 * k
            bulbo = Circle(radius=0.38, stroke_color=CLARO, stroke_width=2.5).set_fill(col, 1).move_to([x, -2.6, 0])
            vaso = RoundedRectangle(width=0.36, height=3.6, corner_radius=0.18, stroke_color=CLARO, stroke_width=2.5).set_fill("#0B1C3D", 1).move_to([x, -0.6, 0])
            liq = Rectangle(width=0.2, height=h, stroke_width=0).set_fill(col, 1).move_to([x, -2.3 + h / 2, 0])
            ttc = T(tc, 34, TINTA, "HEAVY").move_to([x, 1.6, 0])
            ta = T(a, 52, col, "HEAVY").move_to([x, -3.6, 0])
            cols.add(VGroup(vaso, liq, bulbo, ttc, ta))
        self.frac(0.25)
        for k, c in enumerate(cols):
            self.play(FadeIn(c[0]), FadeIn(c[2]), GrowFromEdge(c[1], DOWN), FadeIn(c[3]), run_time=0.45)
            self.play(FadeIn(c[4], scale=1.2), run_time=0.3)
            self.frac(0.12)
        ai = T("temperatura que soporta el aislamiento", 28, CLARO, "BOLD").move_to([0, -4.6, 0])
        self.play(FadeIn(ai), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tit, cols, ai)

        # p6: muchos conductores en un tubo (Tabla 310.15(C)(1))
        self.voz("p6")
        tit = caja_dato("NEC · Tabla 310.15(C)(1)", "más conductores → menos corriente", MARCA, 6.0, 26).move_to([0, 3.4, 0])
        self.play(FadeIn(tit), run_time=0.4)

        def tubo_corte(n, x, pct, col, etq):
            r = 1.25
            t_ = Circle(radius=r, stroke_color=METAL2, stroke_width=6).set_fill("#121E36", 1).move_to([x, 0.2, 0])
            ang = np.linspace(0, TAU, n, endpoint=False)
            rr_ = 0.0 if n == 1 else (0.55 if n <= 3 else 0.72)
            cs = VGroup(*[Circle(radius=0.27 if n <= 6 else 0.24, stroke_color="#8F9AC8", stroke_width=1.5).set_fill(c, 1)
                          .move_to([x + rr_ * np.cos(a) * (1 if n <= 6 else 0.95), 0.2 + rr_ * np.sin(a), 0])
                          for a, c in zip(ang, [NEGRO_BK, ROJO, AZUL_N, NEGRO_BK, ROJO, AZUL_N, NEGRO_BK, ROJO, AZUL_N])])
            if n == 9:
                cs[-1].move_to([x, 0.2, 0])
                for i, a in enumerate(ang[:8]):
                    cs[i].move_to([x + 0.78 * np.cos(a), 0.2 + 0.78 * np.sin(a), 0])
            gl = resplandor([x, 0.2, 0], 1.3 + 0.08 * n, CALOR, 10, 0.006 * n)
            tp = T(pct, 54, col, "HEAVY").move_to([x, -1.8, 0])
            tn = T(etq, 30, TINTA, "BOLD").move_to([x, -2.6, 0])
            return VGroup(gl, t_, cs, tp, tn)
        tubos = [tubo_corte(3, -2.85, "100 %", VERDE_OK, "1–3"), tubo_corte(6, 0, "80 %", AMBAR, "4–6"), tubo_corte(9, 2.85, "70 %", ROJO, "7–9")]
        lab = T("conductores con corriente", 26, CLARO, "BOLD").move_to([0, -3.2, 0])
        self.frac(0.15)
        for k, t_ in enumerate(tubos):
            self.play(FadeIn(t_[1]), LaggedStart(*[FadeIn(c, scale=0.5) for c in t_[2]], lag_ratio=0.05), FadeIn(t_[0]), run_time=0.6)
            self.play(FadeIn(t_[3], scale=1.2), FadeIn(t_[4]), run_time=0.3)
            if k == 0:
                self.play(FadeIn(lab), run_time=0.2)
            self.frac(0.15)
        self.cerrar_voz(0.1)
        self.limpiar(tit, *tubos, lab)

        # p7: conexión floja
        self.voz("p7")
        placa = RoundedRectangle(width=3.0, height=2.4, corner_radius=0.15, stroke_color=METAL_OSC, stroke_width=2).set_fill("#B8BEC8", 1).move_to([0, 1.2, 0])
        tor = tornillo(0.62, LATON).move_to([0, 1.2, 0])
        gancho = Arc(radius=0.78, start_angle=PI * 0.9, angle=-PI * 1.55, arc_center=[0, 1.2, 0]).set_stroke(COBRE_V, 14)
        cond = VGroup(Line([-4.6, 1.33, 0], [-0.95, 1.33, 0]).set_stroke(NEGRO_BK, 30), Line([-1.1, 1.33, 0], [-0.75, 1.33, 0]).set_stroke(COBRE_V, 14))
        cond = VGroup(Line([-3.0, 1.33, 0], [-0.95, 1.33, 0]).set_stroke(NEGRO_BK, 30), Line([-1.1, 1.33, 0], [-0.75, 1.33, 0]).set_stroke(COBRE_V, 14))
        VGroup(placa, tor, gancho, cond).scale(1.45, about_point=np.array([0, 1.2, 0]))
        self.play(FadeIn(placa), FadeIn(cond), Create(gancho), FadeIn(tor), run_time=0.7)
        punto = resplandor(gancho.point_from_proportion(0.5), 1.1, CALOR, 12, 0.09)
        fl = VGroup(pastilla("tornillo flojo", ROJO, 34, True), T("poco contacto → más resistencia → calor", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.18).move_to([0, -2.4, 0])
        self.frac(0.12)
        self.play(FadeIn(punto, scale=0.5), FadeIn(fl[0]), run_time=0.5)
        self.play(FadeIn(fl[1]), run_time=0.4)
        self.frac(0.4)
        self.play(Rotate(tor[1], PI * 1.5), punto.animate.set_opacity(0), run_time=0.9)
        ok = VGroup(check(VERDE_OK, 0.36), T("bien apretado", 40, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.25).move_to([0, -4.2, 0])
        self.play(FadeIn(ok, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(placa, tor, gancho, cond, punto, fl, ok)

        # p8: diagnóstico
        self.voz("p8")
        tt = T("¿cable o toma caliente?", 50, CALOR, "HEAVY").move_to([0, 3.2, 0])
        self.play(FadeIn(tt, scale=1.1), run_time=0.4)
        cs = VGroup(*[caja_dato(a, b, c, 6.4, 28) for a, b, c in [("demasiada corriente", "más carga de la que soporta", ROJO),
                                                                 ("calibre pequeño", "cable delgado para el breaker", NARANJA),
                                                                 ("mala conexión", "tornillo flojo o empalme mal hecho", AMBAR)]]).arrange(DOWN, buff=0.45).scale(1.25).move_to([0, -0.6, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in cs], lag_ratio=0.45), run_time=1.6)
        self.cerrar_voz(0.1)
        self.limpiar(tt, cs)
        self.final("El calor avisa: revisa corriente, calibre y conexiones")


# ====================================================================== V14 · calibre AWG
class V14B(ShortV):
    CLAVE = "v14b"

    def cuerpo(self):
        self.voz("gancho")
        s14 = seccion(2.08, 1.15).move_to([-2.0, 1.0, 0])
        s12 = seccion(3.31, 1.15).move_to([2.0, 1.0, 0])
        l14 = T("14", 90, TINTA, "HEAVY").move_to([-2.0, -1.4, 0])
        l12 = T("12", 90, AMBAR, "HEAVY").move_to([2.0, -1.4, 0])
        self.play(FadeIn(s14, scale=0.7), FadeIn(l14), run_time=0.45)
        self.play(FadeIn(s12, scale=0.7), FadeIn(l12), run_time=0.45)
        self.frac(0.3)
        fl = VGroup(T("número menor", 40, TINTA, "HEAVY"), T("→", 50, AMBAR, "HEAVY"), T("más grueso", 40, AMBAR, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -3.0, 0])
        if fl.width > 8.3:
            fl.scale_to_fit_width(8.3)
        self.play(FadeIn(fl, shift=UP * 0.2), run_time=0.45)
        q = T("¿al revés?", 64, CLARO, "HEAVY").move_to([0, -4.3, 0])
        self.frac(0.4)
        self.play(FadeIn(q, scale=1.2), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(s14, s12, l14, l12, fl, q)

        # p1: trefilado: el alambre pasa por dados cada vez más pequeños
        self.voz("p1")
        xs = [-2.4, -0.4, 1.6, 3.6]
        gros = [0.7, 0.55, 0.42, 0.32]
        dados = VGroup()
        for x, g in zip(xs, gros):
            d = VGroup(Polygon([x - 0.35, g / 2 + 0.85, 0], [x + 0.35, g / 2 + 0.85, 0], [x + 0.35, g / 2 - 0.05, 0], [x - 0.35, g / 2 + 0.25, 0]),
                       Polygon([x - 0.35, -g / 2 - 0.85, 0], [x + 0.35, -g / 2 - 0.85, 0], [x + 0.35, -g / 2 + 0.05, 0], [x - 0.35, -g / 2 - 0.25, 0]))
            d.set_fill("#5B6573", 1).set_stroke("#98A2B3", 2)
            dados.add(d.shift(UP * 1.4))
        tit = T("trefilado", 54, AMBAR, "HEAVY").move_to([0, 3.9, 0])
        self.play(FadeIn(tit), LaggedStart(*[FadeIn(d) for d in dados], lag_ratio=0.15), run_time=0.8)
        tramos = VGroup()
        prev = -4.4
        anchos = [0.9] + gros
        segs = [(-4.4, xs[0])] + [(xs[i], xs[i + 1]) for i in range(3)] + [(xs[3], 4.5)]
        for (a, b), g in zip(segs, anchos):
            tramos.add(Rectangle(width=b - a, height=g, stroke_width=0).set_fill(COBRE_V, 1).move_to([(a + b) / 2, 1.4, 0]))
        cont = VGroup(T("pasadas:", 44, TINTA, "BOLD"), T("0", 80, AMBAR, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([-0.3, -1.0, 0])
        self.add(tramos[0])
        self.play(FadeIn(cont), run_time=0.3)
        self.frac(0.12)
        for i in range(1, 5):
            self.play(GrowFromEdge(tramos[i], LEFT), Transform(cont[1], T(str(i), 80, AMBAR, "HEAVY").move_to(cont[1])), run_time=0.55)
        regla = VGroup(T("más pasadas", 38, TINTA, "HEAVY"), T("alambre más delgado", 38, TINTA, "HEAVY"), T("número más grande", 46, AMBAR, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, -3.6, 0])
        self.frac(0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in regla], lag_ratio=0.4), run_time=1.0)
        self.cerrar_voz(0.1)
        self.limpiar(tit, dados, tramos, cont, regla)

        # p2: AWG definido por dos extremos y 39 pasos
        self.voz("p2")
        awg = T("AWG", 90, MARCA, "HEAVY").move_to([0, 3.7, 0])
        sub = T("American Wire Gauge · calibre americano", 26, CLARO, "BOLD").next_to(awg, DOWN, buff=0.1)
        self.play(FadeIn(awg), FadeIn(sub), run_time=0.5)
        reg = Line([-3.8, -0.6, 0], [3.8, -0.6, 0]).set_stroke(CLARO, 4)
        ticks = VGroup(*[Line([x, -0.75, 0], [x, -0.45 if k % 5 else -0.3, 0]).set_stroke(CLARO, 2) for k, x in enumerate(np.linspace(-3.8, 3.8, 40))])
        self.frac(0.1)
        self.play(Create(reg), LaggedStart(*[Create(t_) for t_ in ticks], lag_ratio=0.02), run_time=1.0)
        e1 = VGroup(T("36", 44, TINTA, "HEAVY"), T("0.005 in", 30, AMBAR, "BOLD"), T("0.127 mm", 24, CLARO, "BOLD")).arrange(DOWN, buff=0.08).move_to([-3.1, -1.9, 0])
        e2 = VGroup(T("4/0", 44, TINTA, "HEAVY"), T("0.46 in", 30, AMBAR, "BOLD"), T("11.68 mm", 24, CLARO, "BOLD")).arrange(DOWN, buff=0.08).move_to([3.1, -1.9, 0])
        d1 = Dot([-3.1, 0.4, 0], radius=0.03, color=COBRE_V)
        d2 = Circle(radius=0.7, stroke_color=_osc(COBRE_V, 0.3), stroke_width=2).set_fill(COBRE_V, 1).move_to([3.1, 0.75, 0])
        self.frac(0.12)
        self.play(FadeIn(e1), FadeIn(d1, scale=3), run_time=0.45)
        self.frac(0.15)
        self.play(FadeIn(e2), GrowFromCenter(d2), run_time=0.5)
        pasos = VGroup(T("39 pasos", 56, MARCA, "HEAVY"), T("cada paso: diámetro × 1.123", 34, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, -3.9, 0])
        self.frac(0.25)
        self.play(FadeIn(pasos[0], scale=1.1), run_time=0.4)
        self.play(FadeIn(pasos[1]), run_time=0.4)
        src = fuente("AWG: 36 = 0.005 in · 0000 = 0.46 in", [0, -5.2, 0], 22)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.1)
        self.limpiar(awg, sub, reg, ticks, e1, e2, d1, d2, pasos, src)

        # p3: reglas ×2
        self.voz("p3")
        a1 = Circle(radius=0.8, stroke_width=2, stroke_color=_osc(COBRE_V, 0.3)).set_fill(COBRE_V, 1).move_to([-2.4, 2.0, 0])
        a2 = Circle(radius=0.8 * np.sqrt(2), stroke_width=2, stroke_color=_osc(COBRE_V, 0.3)).set_fill(COBRE_V, 1).move_to([1.6, 2.0, 0])
        r1 = VGroup(T("−3 calibres", 40, AMBAR, "HEAVY"), T("área × 2", 50, TINTA, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, 0.1, 0])
        self.play(FadeIn(a1), run_time=0.3)
        self.play(TransformFromCopy(a1, a2), FadeIn(r1), run_time=0.7)
        b1 = Circle(radius=0.6, stroke_width=2, stroke_color=_osc(COBRE_V, 0.3)).set_fill(COBRE_V, 1).move_to([-2.4, -2.4, 0])
        b2 = Circle(radius=1.2, stroke_width=2, stroke_color=_osc(COBRE_V, 0.3)).set_fill(COBRE_V, 1).move_to([1.6, -2.4, 0])
        r2 = VGroup(T("−6 calibres", 40, AMBAR, "HEAVY"), T("diámetro × 2", 50, TINTA, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, -4.5, 0])
        dd1 = DoubleArrow(b1.get_left(), b1.get_right(), buff=0, color=WHITE, stroke_width=3, tip_length=0.15)
        dd2 = DoubleArrow(b2.get_left(), b2.get_right(), buff=0, color=WHITE, stroke_width=3, tip_length=0.15)
        self.frac(0.25)
        self.play(FadeIn(b1), FadeIn(dd1), run_time=0.3)
        self.play(TransformFromCopy(b1, b2), TransformFromCopy(dd1, dd2), FadeIn(r2), run_time=0.7)
        self.cerrar_voz(0.1)
        self.limpiar(a1, a2, r1, b1, b2, r2, dd1, dd2)

        # p4: Tabla 8 a escala
        self.voz("p4")
        tit = caja_dato("NEC · Tabla 8", "área de cobre en mm²", MARCA, 5.0, 28).move_to([0, 3.5, 0])
        self.play(FadeIn(tit), run_time=0.4)
        datos = [("14", 2.08), ("12", 3.31), ("10", 5.26), ("8", 8.37)]
        xs = [-3.3, -1.75, 0.15, 2.65]
        cs = VGroup()
        for (n, a), x in zip(datos, xs):
            s = seccion(a, 0.68, aisl=False).move_to([x, 1.2, 0])
            ln = T(n, 46, TINTA, "HEAVY").move_to([x, -0.6, 0])
            la = T(f"{a}", 34, AMBAR, "HEAVY").move_to([x, -1.3, 0])
            cs.add(VGroup(s, ln, la))
        self.frac(0.12)
        for c in cs:
            self.play(GrowFromCenter(c[0]), FadeIn(c[1]), FadeIn(c[2]), run_time=0.45)
            self.frac(0.1)
        cuatro = VGroup(*[seccion(2.08, 0.68, aisl=False) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.02).move_to([1.6, -2.7, 0])
        igual = T("≈", 70, TINTA, "HEAVY").move_to([0.0, -2.7, 0])
        ocho = cs[3][0].copy()
        self.play(ocho.animate.move_to([-1.6, -2.7, 0]), FadeIn(igual), LaggedStart(*[FadeIn(c, scale=0.5) for c in cuatro], lag_ratio=0.15), run_time=0.9)
        x4 = T("8 AWG ≈ 4 × 14 AWG", 40, AMBAR, "HEAVY").move_to([0, -4.6, 0])
        self.play(FadeIn(x4), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tit, cs, cuatro, igual, ocho, x4)

        # p5: calibre → breaker máximo (240.4(D))
        self.voz("p5")
        tit = caja_dato("NEC · 240.4(D)", "protección máxima del cobre", MARCA, 5.4, 28).move_to([0, 3.5, 0])
        self.play(FadeIn(tit), run_time=0.4)
        grupo = VGroup()
        for k, (n, a, amp) in enumerate([("14", 2.08, "15"), ("12", 3.31, "20"), ("10", 5.26, "30")]):
            x = -2.8 + 2.8 * k
            b = breaker(amp, lado=1).scale(5.2).move_to([x, 1.3, 0])
            s = seccion(a, 0.9).move_to([x, -1.2, 0])
            ln = T(f"{n} AWG", 34, TINTA, "HEAVY").move_to([x, -2.6, 0])
            la = T(f"{amp} A", 52, AMBAR, "HEAVY").move_to([x, -3.5, 0])
            grupo.add(VGroup(b, s, ln, la))
        self.frac(0.2)
        for g in grupo:
            self.play(FadeIn(g[1], scale=0.6), FadeIn(g[2]), run_time=0.35)
            self.play(FadeIn(g[0], shift=DOWN * 0.2), FadeIn(g[3], scale=1.2), run_time=0.4)
            self.frac(0.1)
        mm = T("más cobre → menos resistencia → menos calor", 28, CLARO, "BOLD").scale_to_fit_width(8.2).move_to([0, -4.6, 0])
        self.play(FadeIn(mm), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tit, grupo, mm)

        # p6: kcmil
        self.voz("p6")
        tt = VGroup(T("más grueso que 4/0", 40, TINTA, "HEAVY"), T("kcmil", 96, MARCA, "HEAVY"),
                    T("miles de milésimas circulares", 30, CLARO, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, 3.0, 0])
        self.play(FadeIn(tt[0]), run_time=0.3)
        self.play(FadeIn(tt[1], scale=1.2), FadeIn(tt[2]), run_time=0.5)
        cc = VGroup()
        for k, (n, a) in enumerate([("4/0", 107.2), ("250", 127), ("500", 253)]):
            s = seccion(a, 0.17, aisl=False)
            cc.add(VGroup(s, T(n, 34, AMBAR if k else TINTA, "HEAVY").next_to(s, DOWN, buff=0.2)))
        cc.arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to([0, -1.6, 0])
        self.frac(0.2)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cc], lag_ratio=0.35), run_time=1.2)
        sube = pastilla("aquí el número SÍ crece con el tamaño", VERDE_OK, 30, True).move_to([0, -3.9, 0])
        self.play(FadeIn(sube, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(tt, cc, sube)

        # p7: repaso + advertencia
        self.voz("p7")
        r = VGroup(T("AWG", 70, MARCA, "HEAVY"), T("número menor = cable más grueso", 38, TINTA, "HEAVY").scale_to_fit_width(8.2)).arrange(DOWN, buff=0.2).move_to([0, 2.6, 0])
        self.play(FadeIn(r, scale=1.1), run_time=0.5)
        b1 = breaker("20", lado=1).scale(5.5).move_to([-2.3, -0.9, 0])
        b2 = breaker("30", lado=1).scale(5.5).move_to([2.3, -0.9, 0])
        fl = Arrow(b1.get_right(), b2.get_left(), buff=0.2, color=ROJO, stroke_width=6)
        x_ = equis(ROJO, 0.5).move_to(fl)
        av = T("sin revisar el calibre", 36, ROJO, "HEAVY").move_to([0, -3.2, 0])
        self.frac(0.2)
        self.play(FadeIn(b1), GrowArrow(fl), FadeIn(b2), run_time=0.6)
        self.play(FadeIn(x_, scale=1.4), FadeIn(av), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(r, b1, b2, fl, x_, av)
        self.final("AWG: número menor, cable más grueso")


# ====================================================================== V15 · tierra verde
def cond_caja(pts, color, w=16, borde="#8F9AC8"):
    m = VMobject().set_points_smoothly([np.array(p, dtype=float) for p in pts])
    return VGroup(m.copy().set_stroke(borde, w + 4), m.set_stroke(color, w))


def rayado(largo=4.0, h=0.5):
    base = RoundedRectangle(width=largo, height=h, corner_radius=h / 2, stroke_color="#8F9AC8", stroke_width=2).set_fill(VERDE_T, 1)
    fr = VGroup(*[Polygon([x, -h / 2 + 0.03, 0], [x + 0.18, -h / 2 + 0.03, 0], [x + 0.38, h / 2 - 0.03, 0], [x + 0.2, h / 2 - 0.03, 0], stroke_width=0)
                  .set_fill(AMAR_FR, 1) for x in np.arange(-largo / 2 + 0.25, largo / 2 - 0.5, 0.65)])
    return VGroup(base, fr)


class V15B(ShortV):
    CLAVE = "v15b"

    def cuerpo(self):
        self.voz("gancho")
        caja = RoundedRectangle(width=3.6, height=4.6, corner_radius=0.2, stroke_color=METAL_OSC, stroke_width=3).set_fill("#9AA3AF", 1).move_to([0, -1.6, 0])
        fondo_c = RoundedRectangle(width=3.1, height=4.1, corner_radius=0.15, stroke_width=0).set_fill("#5B6573", 1).move_to(caja)
        ko = Circle(radius=0.35, stroke_color=METAL_OSC, stroke_width=2).set_fill("#3A4250", 1).move_to([0, 0.5, 0])
        negro = cond_caja([[-0.15, 0.5, 0], [-0.3, 1.2, 0], [-1.6, 2.2, 0], [-2.2, 2.8, 0]], NEGRO_BK)
        blanco = cond_caja([[0.0, 0.5, 0], [0.0, 1.4, 0], [0.1, 2.4, 0], [0.0, 3.1, 0]], "#ECECEC")
        verde = cond_caja([[0.15, 0.5, 0], [0.3, 1.2, 0], [1.6, 2.2, 0], [2.2, 2.8, 0]], VERDE_T)
        self.play(FadeIn(caja), FadeIn(fondo_c), FadeIn(ko), run_time=0.4)
        self.play(Create(negro), Create(blanco), Create(verde), run_time=0.8)
        nolleva = VGroup(T("normalmente", 30, TINTA, "BOLD"), T("NO lleva corriente", 36, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.06).move_to([1.6, 3.85, 0])
        self.frac(0.3)
        self.play(Indicate(verde, color=VERDE_OK, scale_factor=1.05), FadeIn(nolleva), run_time=0.7)
        q = T("¿para qué está?", 56, TINTA, "HEAVY").move_to(fondo_c)
        self.frac(0.4)
        self.play(FadeIn(q, scale=1.15), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(caja, fondo_c, ko, negro, blanco, verde, nolleva, q)

        # p1: red de tierra: tablero → caja → toma → aparato
        self.voz("p1")
        tab = RoundedRectangle(width=1.8, height=2.6, corner_radius=0.12, stroke_color=METAL_OSC, stroke_width=2.5).set_fill("#C9CED6", 1).move_to([-3.2, 2.2, 0])
        barra_t = Rectangle(width=1.3, height=0.2, stroke_color=_osc(VERDE_T, 0.3), stroke_width=1.5).set_fill(VERDE_T, 1).move_to([-3.2, 1.25, 0])
        brk = breaker("20", lado=1).scale(2.3).move_to([-3.2, 2.6, 0])
        tt = T("tablero", 26, CLARO, "BOLD").next_to(tab, UP, buff=0.1)
        toma = cara(3.2).move_to([0.6, 2.2, 0])
        mw = microondas().scale(1.7).move_to([2.6, -1.6, 0])
        self.play(FadeIn(tab), FadeIn(barra_t), FadeIn(brk), FadeIn(tt), FadeIn(toma), FadeIn(mw), run_time=0.6)
        ruta_v = [[-3.2, 1.15, 0], [-3.2, -0.2, 0], [0.6, -0.2, 0], [0.6, 1.6, 0]]
        rv = VMobject().set_points_as_corners(ruta_v).set_stroke(VERDE_T, 12)
        rv2 = VMobject().set_points_as_corners([[0.6, -0.2, 0], [2.6, -0.2, 0], [2.6, mw.get_top()[1], 0]]).set_stroke(VERDE_T, 12)
        self.frac(0.1)
        self.play(Create(rv), run_time=0.8)
        self.play(Create(rv2), Indicate(toma.ti, color=VERDE_OK), run_time=0.7)
        nom = caja_dato("conductor de puesta a tierra", "de equipos · une todo el metal", VERDE_OK, 6.5, 28).move_to([-0.6, -4.3, 0])
        self.play(FadeIn(nom, shift=UP * 0.2), run_time=0.45)
        self.cerrar_voz(0.1)

        # p2: falla a carcasa → corriente alta por el verde → breaker dispara
        self.voz("p2")
        self.play(FadeOut(nom), run_time=0.3)
        fase = VMobject().set_points_as_corners([[-2.7, 2.6, 0], [-1.6, 2.6, 0], [-1.6, -0.9, 0], [mw.get_left()[0] + 0.2, -0.9, 0]]).set_stroke(NEGRO_BK, 10)
        fase_b = fase.copy().set_stroke("#8F9AC8", 14)
        self.play(Create(fase_b), Create(fase), run_time=0.6)
        chispa = VGroup(*[rayo(mw.get_left() + RIGHT * 0.2 + UP * 0.1, mw.get_left() + RIGHT * 0.8 + UP * (0.5 - 0.5 * k), semilla=k) for k in range(2)])
        self.sfx("pop", -8)
        self.play(FadeIn(chispa), Flash(mw.get_left() + RIGHT * 0.3, color=AMBAR), run_time=0.4)
        ruta_f = [[-2.7, 2.6, 0], [-1.6, 2.6, 0], [-1.6, -0.9, 0], [mw.get_left()[0] + 0.2, -0.9, 0], [2.6, mw.get_top()[1], 0],
                  [2.6, -0.2, 0], [0.6, -0.2, 0], [-3.2, -0.2, 0], [-3.2, 1.15, 0]]
        cf = corriente(ruta_f, vel=2.6, escala=1.6, color=ROJO)
        self.add(cf)
        alta = pastilla("corriente MUY alta", ROJO, 36, True).move_to([-0.5, -3.3, 0])
        self.frac(0.15)
        self.play(FadeIn(alta, scale=1.1), run_time=0.35)
        self.frac(0.25)
        self.sfx("tic", -4)
        self.play(mover_palanca(brk, False), run_time=0.25)
        self.remove(cf)
        ok = VGroup(check(VERDE_OK, 0.32), T("breaker se dispara · carcasa sin tensión", 28, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -4.4, 0])
        if ok.width > 8.4:
            ok.scale_to_fit_width(8.4)
        self.play(FadeOut(chispa), FadeIn(ok, shift=UP * 0.2), run_time=0.4)
        src = fuente("NEC 2020 · 250.4(A)(5) camino efectivo de falla", [0, -5.3, 0], 22)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.1)

        # p3: sin tierra: la persona es el camino
        self.voz("p3")
        self.play(FadeOut(rv), FadeOut(rv2), FadeOut(ok), FadeOut(alta), FadeOut(src), mover_palanca(brk, True), run_time=0.4)
        carc = resplandor(mw.get_center(), 1.6, ROJO, 10, 0.06)
        base = np.array([0.0, -5.6, 0])
        pe = persona("#2F6FB0").scale(1.3).move_to(base, aligned_edge=DOWN)
        mano = mw.get_left() + RIGHT * 0.05 + DOWN * 0.25
        br = brazo(base + 1.3 * np.array([0.36, 1.9, 0]), mano, "#2F6FB0", 14)
        self.play(FadeIn(carc), FadeIn(pe), Create(br), run_time=0.5)
        cp = corriente([mano, base + 1.3 * np.array([0.36, 1.9, 0]), base + 1.3 * np.array([0.1, 0.8, 0]), base + np.array([0.25, 0, 0]), base + np.array([2.2, 0, 0])],
                       vel=1.4, escala=1.3, color=ROJO)
        self.add(cp)
        tu = pastilla("el camino a tierra eres TÚ", ROJO, 36, True).move_to([-1.2, 4.0, 0])
        self.frac(0.25)
        self.play(FadeIn(tu, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(tab, barra_t, brk, tt, toma, mw, fase, fase_b, carc, pe, br, cp, tu)

        # p4: NEC 250.119 — colores permitidos
        self.voz("p4")
        tit = caja_dato("NEC · 250.119", "tierra de equipos", VERDE_OK, 5.0, 30).move_to([0, 3.5, 0])
        self.play(FadeIn(tit), run_time=0.4)
        desn = RoundedRectangle(width=5.0, height=0.36, corner_radius=0.18, stroke_color=_osc(COBRE_V, 0.3), stroke_width=2).set_fill(COBRE_V, 1)
        ver = RoundedRectangle(width=5.0, height=0.55, corner_radius=0.27, stroke_color="#8F9AC8", stroke_width=2).set_fill(VERDE_T, 1)
        vya = rayado(5.0, 0.55)
        filas = VGroup()
        for k, (m, t_) in enumerate([(desn, "desnudo"), (ver, "verde"), (vya, "verde con franjas amarillas")]):
            y = 1.7 - 1.25 * k
            m.move_to([0, y, 0])
            filas.add(VGroup(m, T(t_, 30, TINTA, "BOLD").next_to(m, DOWN, buff=0.12)))
        self.frac(0.25)
        for f_ in filas:
            self.play(FadeIn(f_, shift=RIGHT * 0.3), run_time=0.4)
            self.frac(0.08)
        prob = VGroup(ver.copy().scale(0.6), T("como fase o neutro", 30, TINTA, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([0, -2.9, 0])
        xx = equis(ROJO, 0.4).next_to(prob, LEFT, buff=0.25)
        nop = T("PROHIBIDO", 46, ROJO, "HEAVY").move_to([0, -4.0, 0])
        self.frac(0.3)
        self.play(FadeIn(prob), FadeIn(xx, scale=1.4), FadeIn(nop), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(tit, filas, prob, xx, nop)

        # p5: tabla de colores NEC
        self.voz("p5")
        filas = VGroup()
        for k, (col, nom_, ref, cl) in enumerate([(VERDE_T, "tierra", "250.119", VERDE_OK), ("#ECECEC", "neutro", "200.6 · blanco o gris", CLARO),
                                                   (NEGRO_BK, "fase", "costumbre: negro / rojo", AMBAR)]):
            c1 = RoundedRectangle(width=2.0, height=0.6, corner_radius=0.3, stroke_color="#8F9AC8", stroke_width=2).set_fill(col, 1)
            if k == 1:
                c1 = VGroup(c1, RoundedRectangle(width=2.0, height=0.6, corner_radius=0.3, stroke_color="#8F9AC8", stroke_width=2).set_fill(GRIS_N, 1)).arrange(DOWN, buff=0.12)
            if k == 2:
                c1 = VGroup(c1, RoundedRectangle(width=2.0, height=0.6, corner_radius=0.3, stroke_color="#8F9AC8", stroke_width=2).set_fill(ROJO, 1)).arrange(DOWN, buff=0.12)
            tx = VGroup(T(nom_, 44, TINTA, "HEAVY"), T(ref, 26, cl, "BOLD")).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            filas.add(VGroup(c1, tx).arrange(RIGHT, buff=0.5))
        filas.arrange(DOWN, buff=0.6, aligned_edge=LEFT).scale(1.25).move_to([0, 0.7, 0])
        for f_ in filas:
            self.play(FadeIn(f_, shift=RIGHT * 0.3), run_time=0.45)
            self.frac(0.22)
        sin = pastilla("sin adivinar", MARCA, 40, True).move_to([0, -3.4, 0])
        self.play(FadeIn(sin, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(filas, sin)

        # p6: NEC vs IEC
        self.voz("p6")
        h1 = T("NEC", 54, MARCA, "HEAVY").move_to([-2.2, 3.5, 0])
        h2 = T("IEC", 54, AMBAR, "HEAVY").move_to([2.2, 3.5, 0])
        sep = DashedLine([0, 3.9, 0], [0, -3.2, 0], color=CLARO)
        self.play(FadeIn(h1), FadeIn(h2), Create(sep), run_time=0.5)

        def col(x, items):
            g = VGroup()
            for k, (m, t_) in enumerate(items):
                y = 1.8 - 2.3 * k
                m.move_to([x, y, 0])
                g.add(VGroup(m, T(t_, 30, TINTA, "BOLD").next_to(m, DOWN, buff=0.15)))
            return g
        cn = col(-2.2, [(RoundedRectangle(width=3.0, height=0.55, corner_radius=0.27, stroke_color="#8F9AC8", stroke_width=2).set_fill(VERDE_T, 1), "tierra"),
                        (RoundedRectangle(width=3.0, height=0.55, corner_radius=0.27, stroke_color="#8F9AC8", stroke_width=2).set_fill("#ECECEC", 1), "neutro")])
        ci = col(2.2, [(rayado(3.0, 0.55), "tierra (PE)"),
                       (RoundedRectangle(width=3.0, height=0.55, corner_radius=0.27, stroke_color="#8F9AC8", stroke_width=2).set_fill(AZUL_N, 1), "neutro (N)")])
        self.play(FadeIn(cn), run_time=0.4)
        self.frac(0.2)
        self.play(FadeIn(ci[0], shift=LEFT * 0.2), run_time=0.4)
        self.frac(0.1)
        self.play(FadeIn(ci[1], shift=LEFT * 0.2), run_time=0.4)
        ojo = pastilla("equipo importado: ¡ojo!", AMBAR, 34, True).move_to([0, -4.1, 0])
        self.frac(0.3)
        self.play(FadeIn(ojo, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(h1, h2, sep, cn, ci, ojo)

        # p7: reglas de identificación
        self.voz("p7")
        r1 = VGroup(equis(ROJO, 0.34), RoundedRectangle(width=2.2, height=0.5, corner_radius=0.25, stroke_color="#8F9AC8", stroke_width=2).set_fill(VERDE_T, 1),
                    T("verde como fase", 42, TINTA, "HEAVY")).arrange(RIGHT, buff=0.3)
        neg = RoundedRectangle(width=2.2, height=0.5, corner_radius=0.25, stroke_color="#8F9AC8", stroke_width=2).set_fill(NEGRO_BK, 1)
        cinta = Rectangle(width=0.5, height=0.56, stroke_width=0).set_fill(VERDE_T, 1).move_to(neg)
        r2 = VGroup(equis(ROJO, 0.34), VGroup(neg, cinta), T("negro marcado verde\n(calibre pequeño)", 38, TINTA, "HEAVY")).arrange(RIGHT, buff=0.3)
        big = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.45, stroke_color="#8F9AC8", stroke_width=2).set_fill(NEGRO_BK, 1)
        cinta2 = Rectangle(width=0.5, height=0.96, stroke_width=0).set_fill(VERDE_T, 1).move_to(big)
        r3 = VGroup(check(VERDE_OK, 0.34), VGroup(big, cinta2), T("4 AWG o mayor:\nse puede marcar", 38, TINTA, "HEAVY")).arrange(RIGHT, buff=0.3)
        rs = VGroup(r1, r2, r3).arrange(DOWN, buff=0.9, aligned_edge=LEFT).scale(1.15).move_to([0, 0.2, 0])
        if rs.width > 8.4:
            rs.scale_to_fit_width(8.4)
        for r_ in rs:
            self.play(FadeIn(r_, shift=RIGHT * 0.3), run_time=0.45)
            self.frac(0.22)
        self.cerrar_voz(0.1)
        self.limpiar(rs)
        self.final("Verde = tierra de equipos: tu protección")


# ====================================================================== V16 · agua en fuego eléctrico
class V16B(ShortV):
    CLAVE = "v16b"

    def cuerpo(self):
        self.voz("gancho")
        rg = regleta().scale(2.6).move_to([0, -1.9, 0])
        cl = clavija().scale(1.1).rotate(PI).move_to(rg.get_center() + LEFT * 1.6 + UP * 0.95)
        cordon = VMobject().set_points_smoothly([cl.get_top(), cl.get_top() + UP * 1.0 + LEFT * 0.4, [-3.6, 2.6, 0], [-4.6, 3.0, 0]]).set_stroke(NEGRO_BK, 9)
        self.play(FadeIn(rg), FadeIn(cl), Create(cordon), run_time=0.5)
        ll = llama(1.6).move_to(rg.get_center() + UP * 1.6 + RIGHT * 0.6)
        hm = humo(ll.get_top() + UP * 0.2, 5)
        self.add(ll)
        self.play(FadeIn(ll, scale=0.4), FadeIn(hm, shift=UP * 0.4), run_time=0.6)
        cubo = VGroup(Polygon([-0.5, 0.5, 0], [0.5, 0.5, 0], [0.38, -0.5, 0], [-0.38, -0.5, 0]).set_fill("#5AB3E6", 1).set_stroke("#2E7FB8", 3),
                      Arc(radius=0.5, start_angle=0, angle=PI).set_stroke("#98A2B3", 4).shift(UP * 0.5)).scale(1.5).move_to([2.9, 2.6, 0])
        q = T("¿agua?", 70, "#7FD1FF", "HEAVY").move_to([-1.6, 3.4, 0])
        self.frac(0.25)
        self.play(FadeIn(cubo, shift=LEFT * 0.4), FadeIn(q), run_time=0.45)
        self.frac(0.3)
        xx = equis(ROJO, 0.7).move_to(cubo)
        err = T("puede ser tu último error", 46, ROJO, "HEAVY").move_to([0, -4.4, 0])
        self.play(FadeIn(xx, scale=1.5), FadeIn(err), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(rg, cl, cordon, ll, hm, cubo, q, xx, err)

        # p1: clases de fuego (pictogramas NFPA 10)
        self.voz("p1")

        def pic(letra, forma, col, txt):
            if forma == "tri":
                f = Triangle().scale(0.62).set_fill(col, 1).set_stroke(WHITE, 3)
            elif forma == "cua":
                f = Square(1.05).set_fill(col, 1).set_stroke(WHITE, 3)
            elif forma == "cir":
                f = Circle(radius=0.56).set_fill(col, 1).set_stroke(WHITE, 3)
            elif forma == "est":
                f = Star(5, outer_radius=0.66, inner_radius=0.3).set_fill(col, 1).set_stroke(WHITE, 3)
            else:
                f = RegularPolygon(6).scale(0.6).set_fill(col, 1).set_stroke(WHITE, 3)
            l = T(letra, 44, WHITE if col != "#FFD84D" else "#1D2939", "HEAVY").move_to(f.get_center() + (DOWN * 0.12 if forma == "tri" else 0))
            t_ = T(txt, 30, TINTA, "BOLD")
            return VGroup(VGroup(f, l), t_).arrange(RIGHT, buff=0.4)
        cls = VGroup(pic("A", "tri", "#12B76A", "madera, papel, tela"), pic("B", "cua", ROJO, "líquidos inflamables"),
                     pic("C", "cir", AZUL_N, "equipo eléctrico energizado"), pic("D", "est", "#FFD84D", "metales combustibles"),
                     pic("K", "hex", "#1D2939", "aceites de cocina")).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, 0.3, 0])
        cls.scale_to_fit_width(8.2).move_to([0, 0.0, 0])
        self.frac(0.05)
        for k, c in enumerate(cls):
            self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=0.4)
            self.frac(0.13)
        marco = SurroundingRectangle(cls[2], color=AZUL_N, buff=0.15, corner_radius=0.15, stroke_width=5)
        self.play(Create(marco), cls[0].animate.set_opacity(0.3), cls[1].animate.set_opacity(0.3), cls[3].animate.set_opacity(0.3),
                  cls[4].animate.set_opacity(0.3), run_time=0.5)
        src = fuente("OSHA eTool · Portable Fire Extinguishers", [0, -4.4, 0], 22)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.1)
        self.limpiar(cls, marco, src)

        # p2: el chorro de agua conduce
        self.voz("p2")
        rg = regleta().scale(1.7).move_to([1.9, -3.2, 0])
        ll = llama(1.2).move_to(rg.get_center() + UP * 1.2)
        self.add(ll)
        base = np.array([-3.0, -5.2, 0])
        pe = persona("#2F6FB0").scale(1.75).move_to(base, aligned_edge=DOWN)
        hombro = base + 1.75 * np.array([0.36, 1.92, 0])
        mano = hombro + np.array([0.9, 0.5, 0])
        br = brazo(hombro, mano, "#2F6FB0", 16)
        self.play(FadeIn(rg), FadeIn(ll), FadeIn(pe), Create(br), run_time=0.6)
        chorro = VMobject().set_points_smoothly([mano + RIGHT * 0.15, mano + np.array([1.6, 0.9, 0]), mano + np.array([3.2, 0.2, 0]), ll.get_center() + UP * 0.2])
        chorro.set_stroke("#7FD1FF", 14, 0.8)
        self.play(Create(chorro), run_time=0.6)
        gota = Circle(radius=1.2, stroke_color="#7FD1FF", stroke_width=4).set_fill("#1E5B8A", 0.6).move_to([0.6, 2.4, 0])
        iones = VGroup(*[T(s, 32, c_, "HEAVY").move_to(gota.get_center() + np.array([0.55 * np.cos(a), 0.55 * np.sin(a), 0]))
                         for s, c_, a in [("Na⁺", AMBAR, 0.3), ("Cl⁻", CIAN, 2.2), ("Ca²⁺", AMBAR, 4.0), ("Cl⁻", CIAN, 5.4)]])
        lab = T("sales y minerales = conduce", 30, TINTA, "HEAVY").next_to(gota, DOWN, buff=0.15)
        self.frac(0.2)
        self.play(FadeIn(gota, scale=0.5), LaggedStart(*[FadeIn(i) for i in iones], lag_ratio=0.2), FadeIn(lab), run_time=0.8)
        self.frac(0.25)
        cur = corriente([ll.get_center() + UP * 0.2, mano + np.array([3.2, 0.2, 0]), mano + np.array([1.6, 0.9, 0]), mano + RIGHT * 0.15, hombro,
                         base + 1.75 * np.array([0.12, 0.8, 0]), base + np.array([0.3, 0, 0])], vel=1.5, escala=1.4, color=ROJO)
        self.add(cur)
        self.play(Flash(mano, color=ROJO, flash_radius=0.4), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(rg, ll, pe, br, chorro, gota, iones, lab, cur)

        # p3: cita OSHA
        self.voz("p3")
        cita = VGroup(T("“Nunca uses agua", 58, TINTA, "HEAVY"), T("en un fuego eléctrico”", 58, TINTA, "HEAVY")).arrange(DOWN, buff=0.12).move_to([0, 1.4, 0])
        if cita.width > 8.4:
            cita.scale_to_fit_width(8.4)
        barra = Rectangle(width=0.14, height=cita.height + 0.3, stroke_width=0).set_fill(ROJO, 1).next_to(cita, LEFT, buff=0.25)
        osha = T("— OSHA", 36, ROJO, "HEAVY").next_to(cita, DOWN, buff=0.3).align_to(cita, RIGHT)
        self.play(FadeIn(barra), Write(cita), run_time=1.0)
        self.play(FadeIn(osha), run_time=0.3)
        pr = pastilla("primero: desenergizar", VERDE_OK, 40, True).move_to([0, -2.4, 0])
        self.frac(0.3)
        self.play(FadeIn(pr, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(cita, barra, osha, pr)

        # p4: cortar la energía
        self.voz("p4")
        tab = RoundedRectangle(width=3.4, height=5.0, corner_radius=0.15, stroke_color=METAL_OSC, stroke_width=3).set_fill("#C9CED6", 1).move_to([-1.9, 0.6, 0])
        brs = VGroup(*[breaker(a, lado=1).scale(2.8) for a in ("20", "15", "20", "15")]).arrange(DOWN, buff=0.25).move_to(tab)
        princ = breaker("100", lado=1).scale(3.2).next_to(brs, UP, buff=0.3)
        self.play(FadeIn(tab), FadeIn(brs), FadeIn(princ), run_time=0.5)
        ll = llama(1.3).move_to([2.4, -0.4, 0])
        self.add(ll)
        etq = VGroup(pastilla("C", AZUL_N, 40, True)).next_to(ll, UP, buff=0.2)
        self.play(FadeIn(ll), FadeIn(etq), run_time=0.4)
        self.frac(0.2)
        self.sfx("tic", -4)
        self.play(mover_palanca(brs[1], False), Indicate(brs[1], color=AMBAR), run_time=0.5)
        nueva = pastilla("A", "#12B76A", 40, True).move_to(etq)
        lbl = T("sin tensión = fuego común", 36, TINTA, "HEAVY").move_to([0, -3.9, 0])
        self.frac(0.3)
        self.play(Transform(etq, nueva), FadeIn(lbl), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(tab, brs, princ, ll, etq, lbl)

        # p5: extintores
        self.voz("p5")
        e1 = extintor("C").scale(1.7).move_to([-2.1, 0.6, 0])
        co2 = T("CO₂", 44, WHITE, "HEAVY").move_to(e1[1].get_center() + DOWN * 1.3)
        e2 = extintor("C").scale(1.7).move_to([2.1, 0.6, 0])
        abc = VGroup(*[T(l, 34, WHITE, "HEAVY") for l in "ABC"]).arrange(RIGHT, buff=0.12).move_to(e2[1].get_center() + DOWN * 1.3)
        n1 = T("dióxido de carbono", 30, TINTA, "BOLD").next_to(e1, DOWN, buff=0.3)
        n2 = T("polvo químico", 30, TINTA, "BOLD").next_to(e2, DOWN, buff=0.3).align_to(n1, UP)
        self.play(FadeIn(e1, shift=UP * 0.3), FadeIn(co2), FadeIn(n1), run_time=0.5)
        self.play(FadeIn(e2, shift=UP * 0.3), FadeIn(abc), FadeIn(n2), run_time=0.5)
        nc = pastilla("agente que NO conduce", MARCA, 36, True).move_to([0, 3.9, 0])
        self.play(FadeIn(nc), run_time=0.3)
        self.frac(0.25)
        self.play(Circumscribe(e1[5], color=AMBAR), Circumscribe(e2[5], color=AMBAR), run_time=0.9)
        busca = T("busca la letra C", 44, AMBAR, "HEAVY").move_to([0, -4.0, 0])
        self.play(FadeIn(busca), run_time=0.3)
        self.frac(0.35)
        abc_t = T("ABC: sirve para las tres clases", 36, TINTA, "HEAVY").move_to([0, -4.9, 0])
        self.play(FadeIn(abc_t), Indicate(abc, color=AMBAR), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(e1, e2, co2, abc, n1, n2, nc, busca, abc_t)

        # p6: CO2 vs polvo
        self.voz("p6")
        sep = DashedLine([0, 3.9, 0], [0, -4.6, 0], color=CLARO)
        h1 = T("CO₂", 54, CLARO, "HEAVY").move_to([-2.2, 3.5, 0])
        h2 = T("polvo químico", 44, AMBAR, "HEAVY").move_to([2.2, 3.5, 0])
        self.play(Create(sep), FadeIn(h1), FadeIn(h2), run_time=0.4)
        l1 = llama(1.0).move_to([-2.2, 0.6, 0])
        l2 = llama(1.0).move_to([2.2, 0.6, 0])
        self.add(l1, l2)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.3)
        rng = np.random.default_rng(4)
        o2 = VGroup(*[T("O₂", 24, "#7FD1FF", "HEAVY").move_to([-2.2 + rng.uniform(-1.2, 1.2), 0.8 + rng.uniform(-1.0, 1.4), 0]) for _ in range(7)])
        self.play(FadeIn(o2), run_time=0.3)
        nube = VGroup(*[Circle(radius=rng.uniform(0.35, 0.6), stroke_width=0).set_fill(WHITE, 0.55).move_to([-2.2 + rng.uniform(-1.0, 1.0), 0.8 + rng.uniform(-0.8, 1.0), 0]) for _ in range(10)])
        self.play(FadeIn(nube, scale=0.5), *[o.animate.shift((o.get_center() - np.array([-2.2, 0.8, 0])) * 1.3).set_opacity(0) for o in o2],
                  l1.animate.scale(0.05), run_time=1.0)
        t1 = VGroup(T("desplaza el oxígeno", 26, TINTA, "BOLD"), T("sin residuo", 30, VERDE_OK, "HEAVY"), T("tableros · electrónica", 26, CLARO, "BOLD")).arrange(DOWN, buff=0.1).move_to([-2.2, -2.5, 0])
        self.play(FadeIn(t1), run_time=0.4)
        self.frac(0.2)
        polvo = VGroup(*[Dot([2.2 + rng.uniform(-1.3, 1.3), 0.8 + rng.uniform(-1.0, 1.2), 0], radius=rng.uniform(0.03, 0.08), color="#FFE7A3") for _ in range(70)])
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in polvo], lag_ratio=0.01), l2.animate.scale(0.05), run_time=1.0)
        piso = VGroup(*[Dot([2.2 + rng.uniform(-1.5, 1.5), -0.9 + rng.uniform(-0.1, 0.1), 0], radius=0.06, color="#FFE7A3") for _ in range(40)])
        t2 = VGroup(T("interrumpe la reacción", 26, TINTA, "BOLD"), T("deja residuo", 30, AMBAR, "HEAVY"), T("hay que limpiar", 26, CLARO, "BOLD")).arrange(DOWN, buff=0.1).move_to([2.2, -2.5, 0])
        self.play(FadeIn(piso), FadeIn(t2), run_time=0.4)
        self.cerrar_voz(0.1)
        l1.clear_updaters(); l2.clear_updaters()
        self.limpiar(sep, h1, h2, l1, l2, o2, nube, t1, polvo, piso, t2)

        # p7: salir y llamar a los bomberos
        self.voz("p7")
        puerta = VGroup(RoundedRectangle(width=2.4, height=4.0, corner_radius=0.08, stroke_color="#12B76A", stroke_width=5).set_fill("#0E3B2A", 1),
                        T("SALIDA", 36, "#12B76A", "HEAVY").shift(UP * 2.5)).move_to([-1.6, 0.4, 0])
        fl = Arrow([1.3, 0.4, 0], [-0.2, 0.4, 0], color="#12B76A", stroke_width=16, max_tip_length_to_length_ratio=0.45)
        ll = llama(1.8).move_to([2.6, -1.2, 0])
        self.add(ll)
        self.play(FadeIn(ll), FadeIn(puerta), GrowArrow(fl), run_time=0.6)
        b = VGroup(T("¡sal y llama a los bomberos!", 40, TINTA, "HEAVY"), T("tu vida vale más que cualquier aparato", 28, AMBAR, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, -3.6, 0])
        if b.width > 8.4:
            b.scale_to_fit_width(8.4)
        self.frac(0.2)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.1)
        ll.clear_updaters()
        self.limpiar(puerta, fl, ll, b)
        self.final("Fuego eléctrico: corta la energía, nunca agua")


# ====================================================================== V17 · CAT III
def edificio_zonas():
    """Poste → medidor (CAT IV) → tablero (CAT III) → tomacorriente y aparato (CAT II)."""
    g = VGroup()
    poste_ = Rectangle(width=0.22, height=4.6, stroke_width=0).set_fill("#8B6A4A", 1).move_to([-3.8, 0.2, 0])
    trafo = RoundedRectangle(width=0.7, height=0.9, corner_radius=0.1, stroke_color="#5B6573", stroke_width=2).set_fill("#9AA3AF", 1).move_to([-3.5, 1.6, 0])
    casa = Polygon([-2.4, -2.1, 0], [3.8, -2.1, 0], [3.8, 1.2, 0], [0.7, 2.7, 0], [-2.4, 1.2, 0], stroke_color=CLARO, stroke_width=3).set_fill("#16294F", 1)
    acom = VMobject().set_points_smoothly([[-3.5, 2.1, 0], [-2.9, 1.7, 0], [-2.3, 0.9, 0]]).set_stroke(NEGRO_BK, 6)
    med = VGroup(Circle(radius=0.38, stroke_color="#C7CCD6", stroke_width=3).set_fill("#E4E7EC", 1), Dot(radius=0.06, color=ROJO)).move_to([-1.8, 0.6, 0])
    tab = RoundedRectangle(width=0.9, height=1.3, corner_radius=0.08, stroke_color=METAL_OSC, stroke_width=2).set_fill("#C9CED6", 1).move_to([0.2, 0.0, 0])
    cab1 = Line([-1.42, 0.6, 0], [-0.25, 0.3, 0]).set_stroke(NEGRO_BK, 5)
    cab2 = VMobject().set_points_as_corners([[0.65, 0.0, 0], [2.2, 0.0, 0], [2.2, -0.9, 0]]).set_stroke(NEGRO_BK, 5)
    toma = cara(1.8).move_to([2.2, -1.25, 0])
    g.add(casa, poste_, trafo, acom, med, tab, cab1, cab2, toma)
    g.med, g.tab, g.toma, g.casa = med, tab, toma, casa
    return g


class V17B(ShortV):
    CLAVE = "v17b"

    def cuerpo(self):
        self.voz("gancho")
        mm = multimetro().scale(1.9).move_to([0, 0.2, 0])
        etq = VGroup(RoundedRectangle(width=2.3, height=0.55, corner_radius=0.08, stroke_width=0).set_fill("#101318", 1),
                     T("CAT III 600V", 26, AMBAR, "HEAVY")).move_to(mm.get_bottom() + UP * 0.55)
        etq[1].move_to(etq[0])
        self.play(FadeIn(mm, shift=UP * 0.3), FadeIn(etq), run_time=0.5)
        self.frac(0.12)
        self.play(self.camera.frame.animate.scale(0.5).move_to(etq), run_time=0.8)
        self.frac(0.25)
        self.play(self.camera.frame.animate.scale(2.0).move_to(ORIGIN), run_time=0.6)
        mito = VGroup(T("¿solo el voltaje máximo?", 40, TINTA, "HEAVY")).move_to([0, 3.9, 0])
        self.play(FadeIn(mito), run_time=0.35)
        self.frac(0.35)
        boom = VGroup(Star(12, outer_radius=2.2, inner_radius=1.1).set_fill(NARANJA, 0.9).set_stroke(AMBAR, 4),
                      Star(12, outer_radius=1.3, inner_radius=0.7).set_fill("#FFD84D", 1).set_stroke(width=0)).move_to(mm.get_center())
        self.sfx("pop", -4)
        self.play(FadeIn(boom, scale=0.3), run_time=0.25)
        self.play(FadeOut(boom, scale=1.4), run_time=0.4)
        pt = VGroup(pastilla("te protege", VERDE_OK, 38, True), T("o", 40, TINTA, "HEAVY"), pastilla("te explota", ROJO, 38, True)).arrange(RIGHT, buff=0.3).move_to([0, -4.3, 0])
        self.play(FadeIn(pt, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(mm, etq, mito, pt)

        # p1: transitorios
        self.voz("p1")
        tit = caja_dato("CAT = categoría de medición", "norma IEC 61010", MARCA, 6.2, 28).move_to([0, 3.5, 0])
        self.play(FadeIn(tit), run_time=0.4)
        ax = Line([-4.0, 0.0, 0], [4.0, 0.0, 0]).set_stroke(CLARO, 2)
        sen = onda(lambda x: np.sin(x * 2.4), -4.0, 4.0, 0.0, 1.0, CIAN, 5)
        self.play(Create(ax), Create(sen), run_time=0.9)
        n120 = T("tu voltaje normal", 26, CIAN, "BOLD").move_to([-2.6, -1.4, 0])
        self.play(FadeIn(n120), run_time=0.3)
        self.frac(0.25)
        pico = VMobject().set_points_as_corners([[0.62, 0.95, 0], [0.7, 3.0, 0], [0.78, 0.0, 0], [0.84, 0.7, 0]]).set_stroke(ROJO, 6)
        tp = VGroup(T("transitorio", 40, ROJO, "HEAVY"), T("microsegundos", 28, TINTA, "BOLD")).arrange(DOWN, buff=0.06).move_to([2.6, 2.1, 0])
        self.sfx("pop", -10)
        self.play(Create(pico), FadeIn(tp), run_time=0.5)
        causas = VGroup(VGroup(simbolo_rayo(AMBAR, 0.6), T("rayos", 34, TINTA, "HEAVY")).arrange(RIGHT, buff=0.2),
                        VGroup(Circle(radius=0.28, stroke_color=AMBAR, stroke_width=4).add(T("M", 26, AMBAR, "HEAVY")), T("conmutación de cargas grandes", 30, TINTA, "HEAVY")).arrange(RIGHT, buff=0.2)
                        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0, -3.2, 0])
        self.frac(0.25)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in causas], lag_ratio=0.5), run_time=0.9)
        self.cerrar_voz(0.1)
        self.limpiar(tit, ax, sen, n120, pico, tp, causas)

        # p2 + p3: zonas de la instalación
        self.voz("p2")
        ez = edificio_zonas().move_to([0.2, 0.6, 0])
        self.play(FadeIn(ez), run_time=0.6)
        grad = VGroup(*[Rectangle(width=0.8, height=0.5, stroke_width=0).set_fill(interpolate_color(ManimColor(ROJO), ManimColor(AMBAR), k / 9), 1)
                        for k in range(10)]).arrange(RIGHT, buff=0).move_to([0, -3.2, 0])
        gl = VGroup(T("más energía", 28, ROJO, "HEAVY").next_to(grad, DOWN, buff=0.15).align_to(grad, LEFT),
                    T("menos", 28, AMBAR, "HEAVY").next_to(grad, DOWN, buff=0.15).align_to(grad, RIGHT))
        self.frac(0.1)
        self.play(GrowFromEdge(grad, LEFT), FadeIn(gl), run_time=0.7)
        imp = T("cerca de la acometida: menos impedancia que frene", 26, TINTA, "BOLD").move_to([0, -4.4, 0])
        if imp.width > 8.4:
            imp.scale_to_fit_width(8.4)
        self.play(FadeIn(imp), run_time=0.3)
        self.cerrar_voz(0.1)
        self.play(FadeOut(grad), FadeOut(gl), FadeOut(imp), run_time=0.3)

        self.voz("p3")

        def zona(m, txt, col, pos):
            rr = SurroundingRectangle(m, color=col, buff=0.18, corner_radius=0.12, stroke_width=5)
            p_ = pastilla(txt, col, 34, True).move_to(pos)
            return VGroup(rr, p_)
        z2 = zona(ez.toma, "CAT II", AMBAR, [2.6, -2.6, 0])
        z3 = zona(ez.tab, "CAT III", NARANJA, [0.4, -2.6, 0])
        z4 = zona(VGroup(ez.med, ez[2]), "CAT IV", ROJO, [-2.4, -2.6, 0])
        des = [VGroup(T("CAT II", 34, AMBAR, "HEAVY"), T("lo que se enchufa: aparatos, herramientas", 26, TINTA, "BOLD")),
               VGroup(T("CAT III", 34, NARANJA, "HEAVY"), T("instalación fija: tableros, breakers, cableado", 26, TINTA, "BOLD")),
               VGroup(T("CAT IV", 34, ROJO, "HEAVY"), T("origen: acometida, medidor, líneas", 26, TINTA, "BOLD"))]
        for k, d in enumerate(des):
            d.arrange(DOWN, buff=0.04, aligned_edge=LEFT).move_to([0, -3.3 - 0.0 * k, 0])
        for z, d in zip((z2, z3, z4), des):
            self.play(Create(z[0]), FadeIn(z[1], scale=1.1), FadeIn(d.move_to([0, -3.7, 0])), run_time=0.5)
            self.frac(0.42 if d is not des[-1] else 0.0)
            if d is not des[-1]:
                self.play(FadeOut(d), run_time=0.2)
        self.cerrar_voz(0.1)
        self.limpiar(ez, z2, z3, z4, des[-1])

        # p4: impulsos que debe soportar (600 V)
        self.voz("p4")
        tit = caja_dato("IEC 61010-1 · 600 V", "impulso que debe soportar", MARCA, 5.6, 28).move_to([0, 3.5, 0])
        self.play(FadeIn(tit), run_time=0.4)
        barras = VGroup()
        for k, (c, v, col) in enumerate([("CAT II", 4000, AMBAR), ("CAT III", 6000, NARANJA), ("CAT IV", 8000, ROJO)]):
            x = -2.6 + 2.6 * k
            h = v / 8000 * 4.6
            b = Rectangle(width=1.7, height=h, stroke_width=0).set_fill(col, 0.95).move_to([x, -3.4 + h / 2, 0])
            tv = T(f"{v:,} V".replace(",", " "), 36, TINTA, "HEAVY").next_to(b, UP, buff=0.12)
            tc = T(c, 32, col, "HEAVY").next_to(b, DOWN, buff=0.15)
            barras.add(VGroup(b, tv, tc))
        base_l = Line([-3.9, -3.4, 0], [3.9, -3.4, 0]).set_stroke(CLARO, 2)
        self.play(Create(base_l), run_time=0.3)
        self.frac(0.1)
        for b in barras:
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[2]), run_time=0.45)
            self.play(FadeIn(b[1], shift=UP * 0.1), run_time=0.25)
            self.frac(0.22)
        self.cerrar_voz(0.1)
        self.limpiar(tit, barras, base_l)

        # p5: la trampa: CAT II 1000 V = CAT III 600 V
        self.voz("p5")
        m1 = multimetro().scale(1.15).move_to([-2.2, 1.4, 0])
        m2 = multimetro().scale(1.15).move_to([2.2, 1.4, 0])
        e1 = pastilla("CAT II 1000 V", AMBAR, 30, True).next_to(m1, DOWN, buff=0.2)
        e2 = pastilla("CAT III 600 V", NARANJA, 30, True).next_to(m2, DOWN, buff=0.2)
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(e1), FadeIn(e2), run_time=0.5)
        i1 = T("6 000 V", 48, TINTA, "HEAVY").next_to(e1, DOWN, buff=0.3)
        i2 = T("6 000 V", 48, TINTA, "HEAVY").next_to(e2, DOWN, buff=0.3)
        eq = T("=", 70, AMBAR, "HEAVY").move_to([0, i1.get_y(), 0])
        self.frac(0.2)
        self.play(FadeIn(i1), FadeIn(i2), FadeIn(eq), run_time=0.45)
        lugar = pastilla("mira la categoría del LUGAR", MARCA, 36, True).move_to([0, -3.6, 0])
        self.frac(0.35)
        self.play(FadeIn(lugar, scale=1.1), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(m1, m2, e1, e2, i1, i2, eq, lugar)

        # p6: la regla
        self.voz("p6")
        regla = VGroup(T("categoría del multímetro", 36, TINTA, "HEAVY"), T("≥", 70, AMBAR, "HEAVY"), T("categoría del lugar", 36, TINTA, "HEAVY")).arrange(DOWN, buff=0.12).scale(1.2).move_to([0, 2.4, 0])
        self.play(FadeIn(regla, scale=1.1), run_time=0.5)
        f1 = VGroup(RoundedRectangle(width=1.0, height=1.4, corner_radius=0.08, stroke_color=METAL_OSC, stroke_width=2).set_fill("#C9CED6", 1),
                    T("tablero", 34, TINTA, "HEAVY"), T("→", 40, CLARO, "HEAVY"), pastilla("CAT III", NARANJA, 34, True)).arrange(RIGHT, buff=0.3)
        f2 = VGroup(VGroup(Circle(radius=0.5, stroke_color="#C7CCD6", stroke_width=3).set_fill("#E4E7EC", 1), Dot(radius=0.07, color=ROJO)),
                    T("medidor / acometida", 34, TINTA, "HEAVY"), T("→", 40, CLARO, "HEAVY"), pastilla("CAT IV", ROJO, 34, True)).arrange(RIGHT, buff=0.3)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.8, aligned_edge=LEFT).scale(1.25).move_to([0, -1.6, 0])
        if fs.width > 8.4:
            fs.scale_to_fit_width(8.4)
        self.frac(0.25)
        self.play(FadeIn(f1, shift=RIGHT * 0.3), run_time=0.45)
        self.frac(0.3)
        self.play(FadeIn(f2, shift=RIGHT * 0.3), run_time=0.45)
        self.cerrar_voz(0.1)
        self.limpiar(regla, fs)

        # p7: la parte más débil
        self.voz("p7")
        mm = multimetro().scale(1.3).move_to([0, 1.6, 0])
        p1 = punta_prueba(ROJO).scale(1.6).move_to([-1.6, -1.6, 0])
        p2 = punta_prueba(NEGRO_BK).scale(1.6).move_to([1.6, -1.6, 0])
        c1 = VMobject().set_points_smoothly([mm.get_bottom() + LEFT * 0.3, [-1.0, -0.2, 0], p1.get_top()]).set_stroke(ROJO, 6)
        c2 = VMobject().set_points_smoothly([mm.get_bottom() + RIGHT * 0.3, [1.0, -0.2, 0], p2.get_top()]).set_stroke("#3A3F48", 6)
        l1 = pastilla("CAT III", NARANJA, 30, True).next_to(mm, RIGHT, buff=0.2)
        l2 = pastilla("CAT II", AMBAR, 30, True).move_to([0, -1.6, 0])
        self.play(FadeIn(mm), FadeIn(p1), FadeIn(p2), Create(c1), Create(c2), FadeIn(l1), run_time=0.6)
        self.frac(0.1)
        self.play(FadeIn(l2, scale=1.2), Indicate(p1, color=AMBAR), Indicate(p2, color=AMBAR), run_time=0.6)
        todo = pastilla("todo el equipo = CAT II", ROJO, 38, True).move_to([0, -3.6, 0])
        self.play(Transform(l1, pastilla("CAT II", AMBAR, 30, True).move_to(l1)), FadeIn(todo, scale=1.1), run_time=0.5)
        deb = T("vale lo que su parte más débil", 32, TINTA, "HEAVY").move_to([0, -4.6, 0])
        self.play(FadeIn(deb), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(mm, p1, p2, c1, c2, l1, l2, todo, deb)
        self.final("CAT del multímetro ≥ CAT del lugar")


# ====================================================================== portadas V12–V17
class PortadaB(MovingCameraScene):
    def construct(self):
        import os
        from miniaturas import texto_gancho, sticker, logo_esq
        k = os.environ["CLAVE"]
        fondos = {"v12b": ["#2A0B12", "#12305A"], "v13b": ["#2B1306", "#12305A"], "v14b": ["#1E1407", "#0F3B4F"],
                  "v15b": ["#06261A", "#12305A"], "v16b": ["#2E0A06", "#1A1A3A"], "v17b": ["#241A02", "#12305A"]}
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=fondos[k], opacity=1).set_sheen_direction(UR))
        txt = {"v12b": [("¿CUÁNTA", "#FFFFFF"), ("CORRIENTE", "#FFFFFF"), ("TE MATA?", "#FF5A5F")], "v13b": [("¿POR QUÉ SE", "#FFFFFF"), ("CALIENTA?", "#FF8A3D")],
               "v14b": [("¿EL 12 ES MÁS", "#FFFFFF"), ("GRUESO?", "#FFD84D")], "v15b": [("¿POR QUÉ", "#FFFFFF"), ("ES VERDE?", "#3DDC84")],
               "v16b": [("¿AGUA AL", "#FFFFFF"), ("FUEGO?", "#7FD1FF")], "v17b": [("¿QUÉ ES", "#FFFFFF"), ("CAT III?", "#FFD84D")]}[k]
        t = texto_gancho(txt, 100)
        t.scale_to_fit_width(min(8.2, t.width)).move_to([0, 5.0 if len(txt) < 3 else 4.6, 0])
        st_txt = {"v12b": "solo 0.1 A", "v13b": "la física lo explica", "v14b": "no es un error", "v15b": "puede salvarte",
                  "v16b": "¡NUNCA!", "v17b": "te protege o explota"}[k]
        il = VGroup()
        if k == "v12b":
            il.add(corazon(2.2).shift(DOWN * 0.6), T("100 mA", 90, WHITE, "HEAVY").move_to([0, -0.7, 0]))
            ecg = VMobject().set_points_as_corners([P(x, 0.4 * np.sin(x * 9) * np.cos(x * 3)) for x in np.linspace(-4, 4, 80)]).set_stroke("#FF5A5F", 6).move_to([0, -2.3, 0])
            il.add(ecg)
        elif k == "v13b":
            c = cable_lateral(7.0, 1.4).move_to([0, 0.3, 0])
            c[0].set_fill("#7A2410", 1)
            il.add(resplandor([0, 0.3, 0], 3.0, CALOR, 12, 0.06), c, ondas_calor(np.array([0, 1.1, 0]), 7, CALOR, 1.6, 0.9))
        elif k == "v14b":
            s14 = seccion(2.08, 1.6).move_to([-2.0, 0.5, 0]); s12 = seccion(3.31, 1.6).move_to([2.0, 0.5, 0])
            il.add(s14, s12, T("14", 110, WHITE, "HEAVY").move_to([-2.0, -2.0, 0]), T("12", 110, "#FFD84D", "HEAVY").move_to([2.0, -2.0, 0]))
        elif k == "v15b":
            for kk, col in enumerate([NEGRO_BK, "#ECECEC", VERDE_T]):
                il.add(RoundedRectangle(width=7.0, height=0.8, corner_radius=0.4, stroke_color="#8F9AC8", stroke_width=3).set_fill(col, 1).move_to([0, 1.4 - 1.3 * kk, 0]))
            il.add(SurroundingRectangle(il[2], color="#3DDC84", buff=0.18, corner_radius=0.3, stroke_width=8))
        elif k == "v16b":
            rg = regleta().scale(2.6).move_to([0, -1.6, 0])
            ll = llama(2.4).move_to([0.3, 0.6, 0]); ll.clear_updaters()
            il.add(rg, ll, equis(ROJO, 0.9).move_to([2.6, 1.8, 0]))
        else:
            mm = multimetro().scale(1.75).move_to([0, -0.6, 0])
            et = VGroup(RoundedRectangle(width=3.0, height=0.7, corner_radius=0.1, stroke_width=0).set_fill("#101318", 1), T("CAT III 600V", 34, "#FFD84D", "HEAVY"))
            et[1].move_to(et[0]); et.move_to(mm.get_bottom() + UP * 0.7)
            il.add(mm, et)
        st = sticker(st_txt, "#E5484D", size=56, ang=-0.04).move_to([0, -4.3, 0])
        self.add(il, t, st)
        logo_esq(self, (0, -6.2))

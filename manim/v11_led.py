"""Short V11 (rehecho, estándar nuevo 1:30–3:00): ¿Por qué la lámpara LED gasta tan poco?
Render: FORMATO=v VOZ=eleven manim -o final v11_led.py LED

Fuentes verificadas:
- FTC (EE. UU.), "Shopping for Light Bulbs": una incandescente estándar de 60 W produce unos 800 lúmenes;
  los vatios indican energía consumida, los lúmenes indican brillo.
- U.S. DOE, Energy Saver FAQ (Lighting Choices): en las incandescentes ~90 % de la energía se desperdicia como calor.
- U.S. DOE, Energy Saver (LED Lighting): LED residenciales usan al menos 75 % menos energía y duran hasta 25 veces más.
- Light-emitting diode (Wikipedia, con refs.): electrones se recombinan con huecos y liberan fotones
  (electroluminiscencia); el color lo fija la banda prohibida del semiconductor; el LED blanco común = chip azul
  + fósforo amarillo (Ce:YAG).
- Cálculo propio: 60 W × 5 h × 30 d = 9 kWh; 9 W × 5 h × 30 d = 1.35 kWh.
"""
from comun_e import *
from comun_e import _osc
from taller import corriente, foco_led, P
from nema import NEGRO_BK
from shorts_v import ShortV, onda, CLARO
import shorts_v

GUION_LED = {
    "gancho": "Una lámpara incandescente de sesenta vatios y una LED de nueve vatios dan casi la misma luz. "
              "¿Cómo puede ser? La respuesta está en la física de cada una.",
    "p1": "Primero, una aclaración: los vatios no miden la luz. Miden la energía que consume la lámpara. "
          "La luz se mide en lúmenes. Según la Comisión Federal de Comercio de Estados Unidos, una incandescente "
          "de sesenta vatios produce unos ochocientos lúmenes.",
    "p2": "La lámpara incandescente funciona por calor. La corriente atraviesa un filamento de tungsteno muy delgado, "
          "que tiene resistencia. Se calienta tanto que se pone al rojo blanco, y entonces brilla. "
          "Ese es el problema: para dar luz, primero tiene que calentarse.",
    "p3": "El Departamento de Energía de Estados Unidos lo resume así: en una incandescente, cerca del noventa por "
          "ciento de la energía se desperdicia como calor. De cada cien vatios, solo unos diez se convierten en luz.",
    "p4": "La LED es otra cosa. Es un diodo emisor de luz: un semiconductor con dos zonas. La zona N, con electrones "
          "de sobra, y la zona P, con huecos. Cuando pasa la corriente, los electrones cruzan la unión y se "
          "recombinan con los huecos. En cada recombinación se libera energía en forma de luz. "
          "A eso se le llama electroluminiscencia.",
    "p5": "El color depende del material del semiconductor. ¿Y la luz blanca? La mayoría de las LED blancas son, en "
          "realidad, un chip azul cubierto con un fósforo amarillo. El azul y el amarillo juntos, a nuestros ojos, "
          "se ven blancos.",
    "p6": "Ojo: la LED también produce algo de calor, pero mucho menos, y lo saca por detrás, por ese cuerpo con "
          "aletas. Es un disipador. Si la LED se calienta de más, su vida se acorta. Por eso no conviene encerrarla "
          "en una lámpara sin ventilación, a menos que el empaque diga que sí se puede.",
    "p7": "El resultado, según el Departamento de Energía: una LED residencial usa por lo menos setenta y cinco por "
          "ciento menos energía, y dura hasta veinticinco veces más.",
    "p8": "Hagamos la cuenta. Una lámpara encendida cinco horas al día, durante treinta días. La incandescente de "
          "sesenta vatios consume nueve kilovatios hora al mes. La LED de nueve vatios, uno punto treinta y cinco. "
          "Multiplica la diferencia por el precio del kilovatio hora de tu recibo, y por cada lámpara de tu casa.",
    "p9": "Entonces, cuando compres una lámpara, no te guíes por los vatios: busca los lúmenes. Ochocientos lúmenes "
          "dan la luz de una incandescente de sesenta vatios.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}
shorts_v.SHORTS["v11b"] = ("¿Por qué la LED", "gasta TAN POCO?", GUION_LED)

AZUL_LED = "#3D7BFF"
AMARILLO_F = "#FFD84D"
CALOR = "#FF6B3D"
TUNG_OFF = "#8A6A48"


# ---------------------------------------------------------------------- piezas
def lampara_inc(s=1.0):
    """Lámpara incandescente A19 colgando (rosca arriba): vidrio, soporte, hilos de alimentación, filamento."""
    vid = VMobject().set_points_smoothly([P(-0.34, 0.9), P(-0.4, 0.55), P(-0.8, 0.05), P(-0.86, -0.38), P(-0.6, -0.86),
                                          P(0, -1.06), P(0.6, -0.86), P(0.86, -0.38), P(0.8, 0.05), P(0.4, 0.55), P(0.34, 0.9)])
    vid.set_fill("#DDE7FF", 0.16).set_stroke(CLARO, 2.2)
    brillo = Arc(radius=0.55, start_angle=PI * 0.6, angle=PI * 0.35, arc_center=P(0.05, -0.35)).set_stroke(WHITE, 3, 0.55)
    soporte = Polygon(P(-0.14, 0.88), P(0.14, 0.88), P(0.04, 0.2), P(-0.04, 0.2), stroke_color=CLARO, stroke_width=1).set_fill(WHITE, 0.18)
    hilos = VGroup(Line(P(-0.07, 0.86), P(-0.36, -0.28)), Line(P(0.07, 0.86), P(0.36, -0.28))).set_stroke("#C7CCD6", 2.6)
    xs = np.linspace(-0.36, 0.36, 90)
    fil = VMobject().set_points_smoothly([P(x, -0.28 + 0.055 * np.sin(x * 70)) for x in xs]).set_stroke(TUNG_OFF, 3.2)
    rosca = VGroup(RoundedRectangle(width=0.74, height=0.52, corner_radius=0.05, stroke_color=METAL_OSC, stroke_width=1.4)
                   .set_fill("#C9CED6", 1).move_to(P(0, 1.16)),
                   *[VMobject().set_points_smoothly([P(-0.37, 0.98 + 0.12 * k), P(0, 1.03 + 0.12 * k), P(0.37, 0.98 + 0.12 * k)])
                     .set_stroke(METAL_OSC, 1.4) for k in range(4)],
                   Polygon(P(-0.22, 1.42), P(0.22, 1.42), P(0.12, 1.54), P(-0.12, 1.54), stroke_width=0).set_fill(NEGRO_BK, 1),
                   Dot(P(0, 1.56), radius=0.06, color=LATON))
    g = VGroup(vid, soporte, hilos, fil, brillo, rosca).scale(s)
    g.vid, g.hilos, g.fil = vid, hilos, fil
    return g


def cordon(arriba, abajo):
    return Line(arriba, abajo).set_stroke("#1B2433", 5)


def foton(c, color=AMARILLO_F, largo=1.1):
    w = onda(lambda x: np.sin(x * 14), 0, largo, 0, 0.09, color, 4).rotate(PI / 2)
    w.move_to(c + UP * largo / 2)
    punta = Triangle().scale(0.09).set_fill(color, 1).set_stroke(width=0).move_to(w.get_top() + UP * 0.05)
    return VGroup(w, punta)


def ondas_calor(c, n=4, color=CALOR, alto=1.2, sep=0.42):
    g = VGroup()
    for k in range(n):
        x = c[0] + (k - (n - 1) / 2) * sep
        g.add(onda(lambda y: np.sin(y * 9 + k), 0, alto, 0, 0.06, color, 3.5).rotate(PI / 2).move_to([x, c[1] + alto / 2, 0]))
    return g


def led_corte(s=1.0):
    """Lámpara LED de pie (rosca abajo) en corte: difusor, placa con chips, cuerpo disipador con aletas, rosca."""
    dif = VMobject().set_points_smoothly([P(-0.62, 0.0), P(-0.82, 0.45), P(-0.6, 1.0), P(0, 1.18), P(0.6, 1.0),
                                          P(0.82, 0.45), P(0.62, 0.0)]).set_fill("#FFF8DA", 0.45).set_stroke(CLARO, 2)
    placa = RoundedRectangle(width=1.3, height=0.12, corner_radius=0.03, stroke_width=0).set_fill("#2E7D32", 1).move_to(P(0, 0.02))
    chips = VGroup(*[Rectangle(width=0.16, height=0.08, stroke_width=0).set_fill(AMARILLO_F, 1).move_to(P(x, 0.12))
                     for x in (-0.4, 0, 0.4)])
    cuerpo = Polygon(P(-0.66, -0.04), P(0.66, -0.04), P(0.36, -1.0), P(-0.36, -1.0), stroke_color=METAL_OSC, stroke_width=1.6).set_fill("#B8C0CC", 1)
    aletas = VGroup(*[Line(P(x, -0.08), P(x * 0.55, -0.96), stroke_color="#8C96A3", stroke_width=2.2) for x in np.linspace(-0.5, 0.5, 6)])
    rosca = VGroup(RoundedRectangle(width=0.62, height=0.42, corner_radius=0.05, stroke_color=METAL_OSC, stroke_width=1.4)
                   .set_fill("#C9CED6", 1).move_to(P(0, -1.2)),
                   *[VMobject().set_points_smoothly([P(-0.31, -1.08 - 0.1 * k), P(0, -1.04 - 0.1 * k), P(0.31, -1.08 - 0.1 * k)])
                     .set_stroke(METAL_OSC, 1.3) for k in range(3)],
                   Polygon(P(-0.18, -1.41), P(0.18, -1.41), P(0.1, -1.52), P(-0.1, -1.52), stroke_width=0).set_fill(NEGRO_BK, 1),
                   Dot(P(0, -1.54), radius=0.05, color=LATON))
    g = VGroup(cuerpo, aletas, rosca, placa, chips, dif).scale(s)
    g.chips, g.cuerpo, g.dif = chips, cuerpo, dif
    return g


def mini_inc(s=0.32, color=TUNG_OFF):
    g = lampara_inc(s)
    g.fil.set_stroke(color, 2)
    return g


# ---------------------------------------------------------------------- escena
class LED(ShortV):
    CLAVE = "v11b"

    def cuerpo(self):
        # ---------- gancho: dos lámparas colgando, misma luz
        self.voz("gancho")
        inc = lampara_inc(1.5).move_to([-2.1, 0.7, 0])
        led = foco_led(True, 0.9).scale(3.6).move_to([2.1, 0.6, 0])
        c1, c2 = cordon([-2.1, 4.3, 0], inc.get_top()), cordon([2.1, 4.3, 0], led.get_top())
        self.play(Create(c1), Create(c2), FadeIn(inc, shift=DOWN * 0.3), FadeIn(led, shift=DOWN * 0.3), run_time=0.7)
        g1 = resplandor(inc.vid.get_center(), 2.5, AMBAR, 12, 0.045)
        g2 = resplandor(led.vidrio.get_center(), 2.5, AMBAR, 12, 0.045)
        self.frac(0.15)
        self.play(FadeIn(g1), FadeIn(g2), inc.fil.animate.set_stroke("#FFF3C4", 4), run_time=0.6)
        w1 = VGroup(T("60 W", 64, ROJO, "HEAVY"), T("incandescente", 28, CLARO, "BOLD")).arrange(DOWN, buff=0.08)
        w2 = VGroup(T("9 W", 64, VERDE_OK, "HEAVY"), T("LED", 28, CLARO, "BOLD")).arrange(DOWN, buff=0.08)
        w1.move_to([-2.1, -2.7, 0]); w2.move_to([2.1, -2.7, 0])
        self.frac(0.1)
        self.sfx("pop", -12)
        self.play(FadeIn(w1, shift=UP * 0.2), FadeIn(w2, shift=UP * 0.2), run_time=0.5)
        igual = VGroup(T("misma luz", 44, AMBAR, "HEAVY"), T("¿cómo?", 70, TINTA, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, -4.8, 0])
        self.frac(0.3)
        self.play(FadeIn(igual, scale=1.15), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(w1, w2, igual)

        # ---------- p1: vatios vs lúmenes
        self.voz("p1")
        self.play(VGroup(c1, inc, g1).animate.shift(LEFT * 0.0), VGroup(c2, led, g2).animate.shift(RIGHT * 0.0), run_time=0.05)
        izq = self.carta_dato("VATIOS (W)", "energía que\nconsume", ROJO, [-2.2, -3.4, 0])
        der = self.carta_dato("LÚMENES (lm)", "luz que\nentrega", AMBAR, [2.2, -3.4, 0])
        self.play(FadeIn(izq, shift=UP * 0.2), run_time=0.45)
        self.frac(0.12)
        self.play(FadeIn(der, shift=UP * 0.2), run_time=0.45)
        self.frac(0.35)
        self.limpiar(izq, der, c2, led, g2, t=0.3)
        self.play(VGroup(c1, inc, g1).animate.move_to([0, 1.6, 0]), run_time=0.5)
        rayos = VGroup(*[Line(inc.vid.get_center() + 1.1 * np.array([np.cos(a), np.sin(a), 0]),
                              inc.vid.get_center() + 1.75 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(AMBAR, 5)
                         for a in np.linspace(-PI * 0.95, -PI * 0.05, 7)])
        self.play(LaggedStart(*[Create(r) for r in rayos], lag_ratio=0.08), run_time=0.6)
        dato = VGroup(T("60 W", 60, ROJO, "HEAVY"), T("→", 60, CLARO, "HEAVY"), T("≈ 800 lm", 60, AMBAR, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        self.play(FadeIn(dato, scale=1.1), run_time=0.5)
        src = fuente("FTC (EE. UU.) · Shopping for Light Bulbs", [0, -3.8, 0], 26)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(rayos, dato, src, g1, c1)

        # ---------- p2: el filamento por dentro (zoom)
        self.voz("p2")
        self.play(inc.animate.scale(1.6).move_to([0, 0.6, 0]), run_time=0.6)
        hl, hr = inc.hilos
        ruta = [hl.get_start() + UP * 0.9, hl.get_start(), hl.get_end(), hr.get_end(), hr.get_start(), hr.get_start() + UP * 0.9]
        cur = corriente(ruta, vel=0.9, escala=1.3)
        self.add(cur)
        et = pastilla("filamento de tungsteno", MARCA, 34, True).move_to([0, -3.7, 0])
        flecha = Arrow(et.get_top(), inc.fil.get_bottom() + DOWN * 0.05, buff=0.1, color=MARCA, stroke_width=5)
        self.frac(0.12)
        self.play(FadeIn(et), GrowArrow(flecha), run_time=0.5)
        self.frac(0.15)
        res = pastilla("resistencia → calor", ROJO, 32, True).move_to([0, -4.7, 0])
        self.play(FadeIn(res), run_time=0.35)
        for col, w_ in (("#B5321E", 5), ("#FF7A1A", 5.5), ("#FFC84A", 6), ("#FFF6D8", 6.5)):
            self.play(inc.fil.animate.set_stroke(col, w_), run_time=0.45)
        gl = resplandor(inc.fil.get_center(), 2.6, AMBAR, 14, 0.05)
        oc = ondas_calor(inc.vid.get_top() + DOWN * 0.3 + LEFT * 0.0, 5, CALOR, 1.0, 0.5).shift(DOWN * 2.6)
        self.play(FadeIn(gl), Create(oc), run_time=0.7)
        prob = pastilla("primero calor... luego luz", CALOR, 36, True).move_to([0, -5.7, 0])
        self.frac(0.4)
        self.play(FadeIn(prob, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cur, et, flecha, res, gl, oc, prob, inc)

        # ---------- p3: diagrama de flujo de energía (Sankey)
        self.voz("p3")
        entrada = Polygon(P(-3.9, 1.5), P(-1.8, 1.5), P(-1.8, -1.5), P(-3.9, -1.5), stroke_width=0).set_fill(ENERGIA, 0.95)
        t_in = VGroup(T("100 W", 46, TINTA, "HEAVY"), T("entran", 26, TINTA, "BOLD")).arrange(DOWN, buff=0.05).move_to(entrada)
        luz_ = VMobject(stroke_width=0).set_points_as_corners([P(-1.8, 1.5), P(0, 1.5), P(1.2, 3.1), P(3.9, 3.1), P(3.9, 2.8), P(1.2, 2.8),
                                                                 P(0, 1.2), P(-1.8, 1.2), P(-1.8, 1.5)]).set_fill(AMBAR, 1)
        calor_ = VMobject(stroke_width=0).set_points_as_corners([P(-1.8, 1.2), P(0, 1.2), P(1.2, -0.1), P(3.9, -0.1), P(3.9, -2.8), P(1.2, -2.8),
                                                                   P(0, -1.5), P(-1.8, -1.5), P(-1.8, 1.2)]).set_fill(CALOR, 0.95)
        t_c = VGroup(T("≈ 90 W", 54, TINTA, "HEAVY"), T("CALOR", 32, TINTA, "HEAVY")).arrange(DOWN, buff=0.05).move_to([2.55, -1.45, 0])
        t_l = T("≈ 10 W  LUZ", 36, AMBAR, "HEAVY").move_to([2.4, 3.55, 0])
        oc3 = ondas_calor(np.array([2.55, 0.15, 0]), 5, CALOR, 0.9, 0.5)
        self.play(FadeIn(entrada, shift=RIGHT * 0.3), FadeIn(t_in), run_time=0.5)
        self.frac(0.2)
        self.play(FadeIn(calor_, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(t_c), Create(oc3), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(luz_, shift=RIGHT * 0.3), FadeIn(t_l), run_time=0.5)
        src = fuente("U.S. Department of Energy · Energy Saver", [0, -5.0, 0], 26)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(entrada, t_in, calor_, luz_, t_c, t_l, src, oc3)

        # ---------- p4: unión P-N
        self.voz("p4")
        tit = VGroup(T("LED", 64, MARCA, "HEAVY"), T("Light Emitting Diode · diodo emisor de luz", 26, CLARO, "BOLD")).arrange(DOWN, buff=0.08).move_to([0, 3.4, 0])
        self.play(FadeIn(tit), run_time=0.4)
        zn = Rectangle(width=3.4, height=2.6, stroke_width=0).set_fill(AZUL_LED, 0.28).move_to([-1.7, 0, 0])
        zp = Rectangle(width=3.4, height=2.6, stroke_width=0).set_fill(ROJO, 0.26).move_to([1.7, 0, 0])
        marco = Rectangle(width=6.8, height=2.6, stroke_color=CLARO, stroke_width=2)
        union = DashedLine([0, 1.3, 0], [0, -1.3, 0], color=WHITE, dash_length=0.12)
        ln = T("N", 60, AZUL_LED, "HEAVY").move_to([-1.7, -1.9, 0]); lp = T("P", 60, ROJO, "HEAVY").move_to([1.7, -1.9, 0])
        sn = T("electrones de sobra", 24, CLARO, "BOLD").next_to(ln, DOWN, buff=0.08)
        sp = T("huecos", 24, CLARO, "BOLD").next_to(lp, DOWN, buff=0.08)
        rng = np.random.default_rng(3)
        elec = VGroup(*[Dot([x, y, 0], radius=0.1, color=CIAN_E) for x, y in zip(rng.uniform(-3.1, -0.4, 12), rng.uniform(-1.0, 1.0, 12))])
        huec = VGroup(*[Circle(radius=0.1, stroke_color=WHITE, stroke_width=2.5).move_to([x, y, 0]) for x, y in zip(rng.uniform(0.4, 3.1, 12), rng.uniform(-1.0, 1.0, 12))])
        self.frac(0.12)
        self.play(FadeIn(zn), FadeIn(zp), Create(marco), Create(union), FadeIn(ln), FadeIn(sn), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in elec], lag_ratio=0.05), run_time=0.5)
        self.frac(0.08)
        self.play(FadeIn(lp), FadeIn(sp), LaggedStart(*[FadeIn(h, scale=0.5) for h in huec], lag_ratio=0.05), run_time=0.6)
        # alimentación
        cabl = VGroup(Line([-3.4, 0, 0], [-4.1, 0, 0]), Line([-4.1, 0, 0], [-4.1, -3.6, 0]), Line([-4.1, -3.6, 0], [4.1, -3.6, 0]),
                      Line([4.1, -3.6, 0], [4.1, 0, 0]), Line([4.1, 0, 0], [3.4, 0, 0])).set_stroke("#AAB3CF", 4)
        mas = T("−", 40, AZUL_LED, "HEAVY").move_to([-3.75, 0.35, 0]); men = T("+", 40, ROJO, "HEAVY").move_to([3.75, 0.35, 0])
        self.frac(0.1)
        self.play(Create(cabl), FadeIn(mas), FadeIn(men), run_time=0.5)
        cur = corriente([[3.4, 0, 0], [4.1, 0, 0], [4.1, -3.6, 0], [-4.1, -3.6, 0], [-4.1, 0, 0], [-3.4, 0, 0]], vel=0.9, escala=1.2)
        self.add(cur)
        # recombinaciones: pares que se encuentran en la unión y sueltan un fotón
        orden_e = sorted(range(12), key=lambda i: -elec[i].get_x())
        orden_h = sorted(range(12), key=lambda i: huec[i].get_x())
        luz_tot = VGroup()
        for ronda in range(3):
            anims, fot = [], VGroup()
            for j in range(ronda * 4, ronda * 4 + 4):
                e, h = elec[orden_e[j]], huec[orden_h[j]]
                y = np.clip((e.get_y() + h.get_y()) / 2, -0.9, 0.9)
                anims += [e.animate.move_to([-0.06, y, 0]), h.animate.move_to([0.06, y, 0])]
                fot.add(foton(np.array([0, 1.3, 0]) + RIGHT * (y * 0.9), AMARILLO_F, 0.9))
            self.play(*anims, run_time=0.55)
            idx = range(ronda * 4, ronda * 4 + 4)
            self.sfx("pop", -16)
            self.play(*[FadeOut(elec[orden_e[j]], scale=0.3) for j in idx], *[FadeOut(huec[orden_h[j]], scale=0.3) for j in idx],
                      *[FadeIn(f, shift=UP * 0.4) for f in fot], run_time=0.4)
            luz_tot.add(fot)
            if ronda == 0:
                self.frac(0.08)
        nom = pastilla("electroluminiscencia", AMARILLO_F, 40, True).move_to([0, -5.0, 0])
        self.frac(0.5)
        self.play(FadeIn(nom, scale=1.15), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(tit, zn, zp, marco, union, ln, lp, sn, sp, elec, huec, cabl, mas, men, cur, luz_tot, nom)

        # ---------- p5: chip azul + fósforo = blanco
        self.voz("p5")
        colores = VGroup(*[Circle(radius=0.32, stroke_width=0).set_fill(c, 1) for c in ("#E5484D", "#FFB020", "#12B76A", AZUL_LED)]).arrange(RIGHT, buff=0.35).move_to([0, 3.3, 0])
        lc = T("el material define el color", 30, CLARO, "BOLD").next_to(colores, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in colores], lag_ratio=0.15), FadeIn(lc), run_time=0.7)
        base = RoundedRectangle(width=3.2, height=0.4, corner_radius=0.08, stroke_width=0).set_fill("#2E3B55", 1).move_to([0, -3.0, 0])
        chip = Rectangle(width=1.0, height=0.3, stroke_width=0).set_fill(AZUL_LED, 1).move_to([0, -2.65, 0])
        lchip = T("chip azul", 30, AZUL_LED, "HEAVY").next_to(base, DOWN, buff=0.2).shift(LEFT * 1.4)
        self.frac(0.12)
        self.play(FadeIn(base), FadeIn(chip), FadeIn(lchip), run_time=0.4)
        def haz(color, r0=0.4, r1=3.8, op=1.0):
            return VGroup(*[Line(chip.get_top() + r0 * np.array([np.cos(a), np.sin(a), 0]), chip.get_top() + r1 * np.array([np.cos(a), np.sin(a), 0]))
                            .set_stroke(color, 5, op) for a in np.linspace(PI * 0.2, PI * 0.8, 7)])
        azul = haz(AZUL_LED)
        self.play(LaggedStart(*[Create(r) for r in azul], lag_ratio=0.06), run_time=0.6)
        self.frac(0.15)
        domo = Arc(radius=1.2, start_angle=0, angle=PI, arc_center=chip.get_top()).set_fill(AMARILLO_F, 0.85).set_stroke(_osc(AMARILLO_F, 0.3), 2)
        domo.add_line_to(domo.get_start())
        lf = T("fósforo amarillo", 30, AMARILLO_F, "HEAVY").next_to(base, DOWN, buff=0.2).shift(RIGHT * 1.4)
        blanco = haz(WHITE, 1.25, 3.8)
        self.play(FadeIn(domo, scale=0.8), FadeIn(lf), Transform(azul, blanco), run_time=0.7)
        eq = VGroup(Circle(radius=0.34, stroke_width=0).set_fill(AZUL_LED, 1), T("+", 46, TINTA, "HEAVY"),
                    Circle(radius=0.34, stroke_width=0).set_fill(AMARILLO_F, 1), T("=", 46, TINTA, "HEAVY"),
                    Circle(radius=0.34, stroke_color=CLARO, stroke_width=2).set_fill(WHITE, 1)).arrange(RIGHT, buff=0.3).move_to([0, -5.0, 0])
        self.frac(0.3)
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(colores, lc, base, chip, lchip, azul, domo, lf, eq)

        # ---------- p6: disipador
        self.voz("p6")
        lc_ = led_corte(2.6).move_to([0, 0.3, 0])
        self.play(FadeIn(lc_, shift=UP * 0.2), run_time=0.5)
        luzup = VGroup(*[Line(lc_.dif.get_top() + 0.15 * np.array([np.cos(a), np.sin(a), 0]), lc_.dif.get_top() + 1.1 * np.array([np.cos(a), np.sin(a), 0]))
                         .set_stroke(AMBAR, 5) for a in np.linspace(PI * 0.2, PI * 0.8, 5)])
        self.play(LaggedStart(*[Create(r) for r in luzup], lag_ratio=0.08), run_time=0.5)
        self.frac(0.12)
        flechas = VGroup()
        for lado in (-1, 1):
            for k, yy in enumerate((0.0, -0.8)):
                a = lc_.cuerpo.get_center() + np.array([lado * 0.4, yy + 0.4, 0])
                b = a + np.array([lado * 1.6, -0.3, 0])
                flechas.add(CurvedArrow(a, b, angle=-lado * 0.6, color=CALOR, stroke_width=6, tip_length=0.22))
        ld = pastilla("disipador: saca el calor", CALOR, 36, True).move_to([0, -4.0, 0])
        self.play(LaggedStart(*[Create(f) for f in flechas], lag_ratio=0.12), FadeIn(ld), run_time=0.8)
        self.frac(0.25)
        av = VGroup(T("calor de más = menos vida", 34, TINTA, "HEAVY"),
                    T("lámpara cerrada: revisa el empaque", 30, AMBAR, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, -5.3, 0])
        self.play(FadeIn(av, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(lc_, luzup, flechas, ld, av)

        # ---------- p7: 75 % y 25×
        self.voz("p7")
        b_inc = Rectangle(width=6.4, height=0.7, stroke_width=0).set_fill(ROJO, 0.95).move_to([0, 2.8, 0])
        b_led = Rectangle(width=1.6, height=0.7, stroke_width=0).set_fill(VERDE_OK, 1).move_to(b_inc.get_left() + RIGHT * 0.8 + DOWN * 1.0)
        l1 = T("incandescente  100 %", 28, TINTA, "BOLD").move_to(b_inc)
        l2 = T("LED  ≤ 25 %", 28, TINTA, "BOLD").next_to(b_led, RIGHT, buff=0.25)
        tt = T("energía", 30, CLARO, "BOLD").next_to(b_inc, UP, buff=0.15)
        self.play(FadeIn(tt), GrowFromEdge(b_inc, LEFT), FadeIn(l1), run_time=0.5)
        self.frac(0.1)
        self.play(GrowFromEdge(b_led, LEFT), FadeIn(l2), run_time=0.5)
        n75 = T("−75 %", 80, VERDE_OK, "HEAVY").move_to([2.1, 1.4, 0])
        self.play(FadeIn(n75, scale=1.2), run_time=0.4)
        self.frac(0.2)
        vida = T("vida útil (hasta)", 32, CLARO, "BOLD").move_to([0, 0.1, 0])
        rej = VGroup(*[mini_inc(0.33) for _ in range(25)]).arrange_in_grid(5, 5, buff=(0.3, 0.12)).move_to([-1.8, -2.6, 0])
        un_led = foco_led(True, 0.9).scale(3.0).move_to([2.6, -2.6, 0])
        igual = T("=", 70, TINTA, "HEAVY").move_to([0.95, -2.6, 0])
        x25 = T("25 incandescentes", 28, ROJO, "BOLD").next_to(rej, DOWN, buff=0.2)
        x1 = T("1 LED", 28, VERDE_OK, "BOLD").next_to(un_led, DOWN, buff=0.2).align_to(x25, UP)
        self.play(FadeIn(vida), LaggedStart(*[FadeIn(m, scale=0.6) for m in rej], lag_ratio=0.03), run_time=0.9)
        self.play(FadeIn(igual), FadeIn(un_led, scale=0.8), FadeIn(x25), FadeIn(x1), run_time=0.5)
        src = fuente("U.S. Department of Energy · LED Lighting", [0, -6.3, 0], 26)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(b_inc, b_led, l1, l2, tt, n75, vida, rej, un_led, igual, x25, x1, src)

        # ---------- p8: la cuenta
        self.voz("p8")
        cond = VGroup(pastilla("5 h al día", MARCA, 32, True), pastilla("30 días", MARCA, 32, True)).arrange(RIGHT, buff=0.3).move_to([0, 3.6, 0])
        self.play(FadeIn(cond, shift=DOWN * 0.2), run_time=0.4)
        f1 = VGroup(T("60 W × 5 h × 30 =", 38, TINTA, "BOLD"), T("9 kWh", 46, ROJO, "HEAVY")).arrange(RIGHT, buff=0.25).move_to([0, 2.6, 0])
        f2 = VGroup(T("9 W × 5 h × 30 =", 38, TINTA, "BOLD"), T("1.35 kWh", 46, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.25).move_to([0, 1.7, 0])
        self.frac(0.2)
        self.play(Write(f1), run_time=0.8)
        self.frac(0.15)
        self.play(Write(f2), run_time=0.8)
        eje = Line([-3.2, -4.0, 0], [3.2, -4.0, 0]).set_stroke(CLARO, 2)
        k = 0.42
        bi = Rectangle(width=1.6, height=9 * k, stroke_width=0).set_fill(ROJO, 0.95).move_to([-1.4, -4.0 + 9 * k / 2, 0])
        bl = Rectangle(width=1.6, height=1.35 * k, stroke_width=0).set_fill(VERDE_OK, 1).move_to([1.4, -4.0 + 1.35 * k / 2, 0])
        ti = T("9", 40, TINTA, "HEAVY").move_to(bi)
        tl = T("1.35", 36, VERDE_OK, "HEAVY").next_to(bl, UP, buff=0.12)
        ei = mini_inc(0.38, "#FFC84A").next_to(eje, DOWN, buff=0.15).set_x(-1.4)
        el = foco_led(True, 0.9).scale(1.15).next_to(eje, DOWN, buff=0.15).set_x(1.4)
        u = T("kWh / mes por lámpara", 26, CLARO, "BOLD").next_to(ei, DOWN, buff=0.15).set_x(0)
        self.play(Create(eje), GrowFromEdge(bi, DOWN), GrowFromEdge(bl, DOWN), FadeIn(ei), FadeIn(el), run_time=0.7)
        self.play(FadeIn(ti), FadeIn(tl), FadeIn(u), run_time=0.4)
        ahorro = pastilla("ahorro: 7.65 kWh/mes", AMBAR, 36, True).move_to([0, 0.65, 0])
        self.frac(0.25)
        self.play(FadeIn(ahorro, scale=1.15), run_time=0.4)
        mult = T("× precio del kWh × lámparas de tu casa", 30, AMBAR, "BOLD").move_to([0, -6.0, 0])
        self.frac(0.4)
        self.play(FadeIn(mult, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cond, f1, f2, eje, bi, bl, ti, tl, ei, el, u, ahorro, mult)

        # ---------- p9: empaque: busca los lúmenes
        self.voz("p9")
        caja = RoundedRectangle(width=5.0, height=6.6, corner_radius=0.2, stroke_color="#4A5AA0", stroke_width=3).set_fill("#F2F4F7", 1).move_to([0, 0.0, 0])
        franja = Rectangle(width=5.0, height=0.9, stroke_width=0).set_fill(MARCA, 1).move_to(caja.get_top() + DOWN * 0.45)
        marca_ = T("LÁMPARA LED", 34, WHITE, "HEAVY").move_to(franja)
        dib = foco_led(True, 0.9).scale(2.4).move_to([0, 1.0, 0])
        lm = T("800 lm", 90, "#1D2939", "HEAVY").move_to([0, -1.2, 0])
        ww = T("9 W", 34, "#667085", "BOLD").move_to([-1.4, -2.5, 0])
        eqv = T("≈ 60 W incand.", 28, "#667085", "BOLD").move_to([0.8, -2.5, 0])
        self.play(FadeIn(caja, shift=UP * 0.3), FadeIn(franja), FadeIn(marca_), FadeIn(dib), run_time=0.6)
        self.play(FadeIn(ww), FadeIn(eqv), FadeIn(lm), run_time=0.4)
        tach = T("los vatios = consumo", 24, "#667085", "BOLD").move_to([0, -3.0, 0])
        self.frac(0.25)
        self.play(ww.animate.set_opacity(0.35), eqv.animate.set_opacity(0.35), FadeIn(tach), run_time=0.35)
        self.play(Circumscribe(lm, color=VERDE_OK, buff=0.15, stroke_width=6), run_time=0.9)
        regla = pastilla("compra por lúmenes", VERDE_OK, 42, True).move_to([0, -4.3, 0])
        self.frac(0.3)
        self.play(FadeIn(regla, scale=1.15), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(caja, franja, marca_, dib, lm, ww, eqv, tach, regla)
        self.final("Menos calor, más luz por vatio")

    def carta_dato(self, titulo, texto, color, pos):
        cab = T(titulo, 32, color, "HEAVY")
        cuerpo = VGroup(*[T(l, 28, TINTA, "MEDIUM") for l in texto.split("\n")]).arrange(DOWN, buff=0.06)
        g = VGroup(cab, cuerpo).arrange(DOWN, buff=0.2)
        caja = tarjeta(max(3.8, g.width + 0.4), g.height + 0.5, color="#4A5AA0")
        g.move_to(caja)
        return VGroup(caja, g).move_to(pos)


CIAN_E = "#6FF2FF"


class PortadaLED(MovingCameraScene):
    def construct(self):
        from miniaturas import texto_gancho, sticker, logo_esq
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=["#1A0F2E", "#12305A"], opacity=1).set_sheen_direction(UR))
        txt = texto_gancho([("60 W vs 9 W", "#FFFFFF"), ("¿MISMA LUZ?", "#FFD84D")], 100)
        txt.scale_to_fit_width(8.2).move_to([0, 5.0, 0])
        inc = lampara_inc(1.9).move_to([-2.1, 0.4, 0])
        inc.fil.set_stroke("#FFF3C4", 6)
        led = foco_led(True, 0.9).scale(4.4).move_to([2.1, 0.3, 0])
        g1 = resplandor(inc.vid.get_center(), 2.6, CALOR, 14, 0.06)
        g2 = resplandor(led.vidrio.get_center(), 2.6, AMBAR, 14, 0.05)
        oc = ondas_calor(inc.vid.get_top() + UP * 0.1, 4, CALOR, 1.1, 0.45)
        c1, c2 = cordon([-2.1, 3.6, 0], inc.get_top()), cordon([2.1, 3.6, 0], led.get_top())
        w1 = T("60 W", 80, ROJO, "HEAVY").move_to([-2.1, -2.75, 0])
        w2 = T("9 W", 80, VERDE_OK, "HEAVY").move_to([2.1, -2.75, 0])
        st = sticker("la física lo explica", "#E5484D", size=56, ang=-0.04).move_to([0, -4.3, 0])
        self.add(g1, g2, c1, c2, inc, led, w1, w2, txt, st)
        logo_esq(self, (0, -6.2))

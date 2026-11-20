"""Shorts V19–V38 (9-nov-2026). Guiones y fuentes en guiones_d.py.
Estilo nuevo: tarjetas blancas cuadradas alineadas a la izquierda, aparatos en 2D de frente y sin marca, una composición
distinta en cada escena.  Render: FORMATO=v VOZ=eleven manim -qh --disable_caching -o final shorts_d.py V19D
"""
from shorts_c import *  # noqa: F401,F403
from shorts_c import _osc
import shorts_v
from guiones_d import GUIONES_D
from piezas_auto2 import tornillo_frente, carta as _carta, etiqueta as _etiqueta, contactor_2d, contacto, bobina_sim, motor_sim, SIM, SW_MAN, SW_POT
from piezas_proteccion import breaker_din, breaker_on, palanca_breaker, GraficaLog, placa_motor
from e06_contactor import motor_3f, horno, pulsador_fis
from e06b_contactor import plc

shorts_v.SHORTS.update(GUIONES_D)
ROJO_P = "#E5484D"
AZUL_C = "#2F6FD0"


def card(titulo, lineas=(), color=MARCA, w=7.6, size=30):
    m = _carta(titulo, lineas, color, w, size)
    return m.scale_to_fit_width(8.3) if m.width > 8.3 else m


def tag(texto, color=MARCA, size=34):
    m = _etiqueta(texto, color, size)
    return m.scale_to_fit_width(8.3) if m.width > 8.3 else m


def num_grande(valor, unidad, color=AMBAR, s=110):
    a = T(valor, s, color, "HEAVY")
    b = T(unidad, int(s * 0.45), color, "HEAVY").next_to(a, RIGHT, buff=0.15, aligned_edge=DOWN)
    return VGroup(a, b)


def varilla_tierra(h=3.2):
    tierra = Rectangle(width=6.0, height=h, stroke_width=0).set_fill("#5A3E2B", 1)
    capas = VGroup(*[Line([-3.0, y, 0], [3.0, y, 0]).set_stroke("#6B4A33", 3) for y in np.linspace(-h / 2 + 0.4, h / 2 - 0.2, 5)])
    var = Rectangle(width=0.16, height=h * 0.85, stroke_width=0).set_fill("#C8743F", 1).move_to([0, h / 2 - h * 0.425 + 0.3, 0])
    pasto = Line([-3.0, h / 2, 0], [3.0, h / 2, 0]).set_stroke("#3F8F3A", 8)
    return VGroup(tierra, capas, pasto, var)


def lavadora(s=1.0):
    cuerpo = RoundedRectangle(width=2.6 * s, height=3.0 * s, corner_radius=0.15 * s, stroke_color="#98A2B3", stroke_width=2).set_fill("#E4E7EC", 1)
    panel = Rectangle(width=2.6 * s, height=0.5 * s, stroke_width=0).set_fill("#C9CED6", 1).move_to(cuerpo.get_top() + DOWN * 0.25 * s)
    puerta = Circle(radius=0.85 * s, stroke_color="#667085", stroke_width=4).set_fill("#5B7FA6", 1).move_to(cuerpo.get_center() + DOWN * 0.3 * s)
    vid = Circle(radius=0.6 * s, stroke_width=0).set_fill("#8FB4D9", 1).move_to(puerta)
    perilla = Circle(radius=0.12 * s, stroke_width=0).set_fill("#667085", 1).move_to(panel.get_center() + RIGHT * 0.8 * s)
    return VGroup(cuerpo, panel, puerta, vid, perilla)


def bateria(s=1.0):
    c = RoundedRectangle(width=2.4 * s, height=1.5 * s, corner_radius=0.1 * s, stroke_color="#1D2939", stroke_width=2).set_fill("#344054", 1)
    t1 = Rectangle(width=0.35 * s, height=0.2 * s, stroke_width=0).set_fill(ROJO_P, 1).move_to(c.get_corner(UL) + RIGHT * 0.45 * s + UP * 0.1 * s)
    t2 = Rectangle(width=0.35 * s, height=0.2 * s, stroke_width=0).set_fill("#98A2B3", 1).move_to(c.get_corner(UR) + LEFT * 0.45 * s + UP * 0.1 * s)
    mas = T("+", 30, WHITE, "HEAVY").move_to(c.get_center() + LEFT * 0.7 * s)
    men = T("−", 30, WHITE, "HEAVY").move_to(c.get_center() + RIGHT * 0.7 * s)
    v = T("12 V", 26, AMBAR, "HEAVY").move_to(c)
    return VGroup(c, t1, t2, mas, men, v)


def fusible_vidrio(s=1.0, fundido=False):
    vid = RoundedRectangle(width=3.6 * s, height=0.9 * s, corner_radius=0.3 * s, stroke_color="#C7CCD6", stroke_width=2).set_fill("#DDE7F0", 0.25)
    caps = VGroup(*[Rectangle(width=0.7 * s, height=1.0 * s, stroke_color="#7A6A3A", stroke_width=1.5).set_fill("#D9C38A", 1).move_to([x * s, 0, 0]) for x in (-1.85, 1.85)])
    if not fundido:
        hilo = Line([-1.5 * s, 0, 0], [1.5 * s, 0, 0]).set_stroke("#D9D9D9", 5)
    else:
        hilo = VGroup(Line([-1.5 * s, 0, 0], [-0.15 * s, 0, 0]).set_stroke("#D9D9D9", 5), Line([0.15 * s, 0, 0], [1.5 * s, 0, 0]).set_stroke("#D9D9D9", 5))
    return VGroup(vid, hilo, caps)


def fotocelda(s=1.0):
    base = RoundedRectangle(width=1.6 * s, height=0.35 * s, corner_radius=0.08 * s, stroke_width=0).set_fill("#344054", 1)
    domo = Arc(radius=0.75 * s, start_angle=0, angle=PI).set_fill("#9CC7E8", 0.85).set_stroke("#C7D7E8", 2).next_to(base, UP, buff=0)
    ventana = RoundedRectangle(width=0.36 * s, height=0.3 * s, corner_radius=0.05 * s, stroke_width=0).set_fill("#1F2430", 1).move_to(domo.get_center() + DOWN * 0.05 * s)
    return VGroup(base, domo, ventana)


def luminaria(s=1.0, encendida=False):
    poste_ = Rectangle(width=0.22 * s, height=6.0 * s, stroke_width=0).set_fill("#667085", 1)
    brazo_ = Line(poste_.get_top(), poste_.get_top() + RIGHT * 2.0 * s + UP * 0.2 * s).set_stroke("#667085", 10 * s)
    cabeza = RoundedRectangle(width=1.6 * s, height=0.45 * s, corner_radius=0.18 * s, stroke_width=0).set_fill("#98A2B3", 1).move_to(brazo_.get_end() + RIGHT * 0.4 * s)
    lente = Rectangle(width=1.2 * s, height=0.12 * s, stroke_width=0).set_fill("#FFE8A3" if encendida else "#475467", 1).next_to(cabeza, DOWN, buff=0)
    g = VGroup(poste_, brazo_, cabeza, lente)
    g.lente, g.cabeza = lente, cabeza
    return g


def sensor_inductivo(s=1.0, led=False):
    cuerpo = Rectangle(width=3.4 * s, height=0.7 * s, stroke_color="#667085", stroke_width=1.5).set_fill("#C9CED6", 1)
    rosca = VGroup(*[Line([x * s, -0.35 * s, 0], [x * s + 0.08 * s, 0.35 * s, 0]).set_stroke("#98A2B3", 2) for x in np.linspace(-1.5, 1.2, 16)])
    cara_ = Rectangle(width=0.35 * s, height=0.7 * s, stroke_width=0).set_fill("#1F2430", 1).next_to(cuerpo, RIGHT, buff=0)
    tuercas = VGroup(*[Rectangle(width=0.22 * s, height=0.95 * s, stroke_width=0).set_fill("#98A2B3", 1).move_to([x * s, 0, 0]) for x in (-0.8, 0.5)])
    luz = Circle(radius=0.08 * s, stroke_width=0).set_fill("#F5A524" if led else "#475467", 1).move_to(cuerpo.get_left() + RIGHT * 0.3 * s + UP * 0.2 * s)
    cab = VGroup(*[Line(cuerpo.get_left() + UP * dy * s, cuerpo.get_left() + LEFT * 1.2 * s + UP * dy * 2 * s).set_stroke(c, 5) for dy, c in ((0.15, "#8B5A2B"), (0, "#2F6FD0"), (-0.15, "#1F2430"))])
    g = VGroup(cab, cuerpo, rosca, tuercas, cara_, luz)
    g.cara, g.luz = cara_, luz
    return g


def hongo_emergencia(s=1.0):
    placa = Circle(radius=1.6 * s, stroke_width=0).set_fill("#F5C400", 1)
    txt_ = VGroup(*[T(c, 20, "#101828", "HEAVY") for c in "EMERGENCIA"])
    for k, c in enumerate(txt_):
        a = PI * 0.85 - k * PI * 0.7 / 9
        c.move_to(placa.get_center() + 1.3 * s * np.array([np.cos(a), np.sin(a), 0])).rotate(a - PI / 2)
    base = Circle(radius=0.85 * s, stroke_width=0).set_fill("#98A2B3", 1)
    hongo = Circle(radius=0.75 * s, stroke_color="#8F1D1D", stroke_width=3).set_fill("#E5484D", 1)
    brillo = Arc(radius=0.55 * s, start_angle=PI * 0.55, angle=PI * 0.4).set_stroke(WHITE, 4, 0.5)
    g = VGroup(placa, txt_, base, hongo, brillo)
    g.hongo = VGroup(hongo, brillo)
    return g


def pararrayos_edificio():
    ed = Rectangle(width=4.2, height=5.0, stroke_color="#98A2B3", stroke_width=2).set_fill("#475467", 1).move_to([0, -1.9, 0])
    vent = VGroup(*[Rectangle(width=0.55, height=0.5, stroke_width=0).set_fill("#9CC7E8", 0.7).move_to([x, y, 0]) for x in (-1.3, 0, 1.3) for y in (-0.2, -1.2, -2.2, -3.2)])
    puntas = VGroup(*[Line([x, 0.6, 0], [x, 1.3, 0]).set_stroke("#C8743F", 5) for x in (-2.0, 2.0)])
    cab = Line([-2.0, 0.62, 0], [2.0, 0.62, 0]).set_stroke("#C8743F", 4)
    baj = VGroup(*[Line([x, 0.62, 0], [x, -4.4, 0]).set_stroke("#C8743F", 4) for x in (-2.12, 2.12)])
    suelo = Rectangle(width=8.4, height=1.2, stroke_width=0).set_fill("#5A3E2B", 1).move_to([0, -5.0, 0])
    elec = VGroup(*[Rectangle(width=0.14, height=0.9, stroke_width=0).set_fill("#C8743F", 1).move_to([x, -4.85, 0]) for x in (-2.12, 2.12)])
    g = VGroup(suelo, ed, vent, cab, baj, puntas, elec)
    g.puntas, g.baj, g.elec = puntas, baj, elec
    return g


def bornera_motor(s=1.0):
    """Caja de bornes de 6 terminales (IEC 60034-8): arriba W2 U2 V2, abajo U1 V1 W1."""
    caja = RoundedRectangle(width=4.2 * s, height=3.0 * s, corner_radius=0.12 * s, stroke_color="#667085", stroke_width=2).set_fill("#E4E7EC", 1)
    b = {}
    for fila, nombres, y in ((0, ("W2", "U2", "V2"), 0.6), (1, ("U1", "V1", "W1"), -0.6)):
        for x, n in zip((-1.3, 0, 1.3), nombres):
            p = np.array([x * s, y * s, 0])
            per = Circle(radius=0.28 * s, stroke_color="#7A6A3A", stroke_width=2).set_fill("#D9C38A", 1).move_to(p)
            tu = RegularPolygon(6).scale(0.16 * s).set_fill("#98A2B3", 1).set_stroke("#475467", 1).move_to(p)
            e = T(n, 22, "#101828", "HEAVY").next_to(per, UP if fila == 0 else DOWN, buff=0.08)
            b[n] = VGroup(per, tu, e)
    g = VGroup(caja, *b.values())
    g.b = b
    return g


def puente(a, b, s=1.0):
    return RoundedRectangle(width=np.linalg.norm(b - a) + 0.5 * s, height=0.26 * s, corner_radius=0.1 * s, stroke_color="#7A3B12", stroke_width=1.5).set_fill(COBRE_V, 1).rotate(
        np.arctan2((b - a)[1], (b - a)[0])).move_to((a + b) / 2)


def fuente(texto, pos=None, size=22):
    f = T("Fuente: " + texto, size, TINTA2 if "TINTA2" in globals() else CLARO, "MEDIUM").set_opacity(0.95)
    if f.width > 8.2:
        f.scale_to_fit_width(8.2)
    return f.move_to(pos if pos is not None else [0, -5.3, 0])


def br_din(s=0.62):
    return breaker_on(breaker_din(1, 20, "C", s=s, tension="120/240 V~"))


class ShortD(ShortC):
    pass


# ====================================================================== V19 · tierra física
class V19D(ShortD):
    CLAVE = "v19"

    def cuerpo(self):
        self.voz("gancho")
        vt = varilla_tierra(3.6).move_to([0, -2.6, 0])
        self.play(FadeIn(vt), run_time=0.6)
        q = tag("¿te protege por sí sola?", ROJO_P, 40).move_to([0, 2.6, 0])
        self.frac(0.4)
        self.play(FadeIn(q, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(vt, q)

        self.voz("p1")
        lv = lavadora(1.3).move_to([1.4, 1.2, 0])
        p_ = persona().scale(1.5).move_to([-2.6, -0.6, 0])
        self.play(FadeIn(lv), FadeIn(p_), run_time=0.5)
        self.frac(0.25)
        cab = Line(lv.get_left() + UP * 0.5 + RIGHT * 0.2, lv.get_left() + RIGHT * 0.2 + DOWN * 0.3).set_stroke(NEGRO_BK, 8)
        zap = VGroup(*[rayo(cab.get_end(), cab.get_end() + RIGHT * 0.5 + DOWN * 0.3, semilla=k) for k in range(2)])
        self.sfx("pop", -8)
        self.play(Create(cab), FadeIn(zap), run_time=0.5)
        v = tag("carcasa con 120 V", ROJO_P, 40).move_to([0, -4.0, 0])
        self.play(FadeIn(v), lv[0].animate.set_stroke(ROJO_P, 5), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(lv, p_, cab, zap, v)

        self.voz("p2")
        vt = varilla_tierra(2.6).move_to([0, -3.6, 0])
        f = VGroup(T("120 V ÷ 25 Ω", 64, TINTA, "HEAVY"), T("= 4,8 A", 90, AMBAR, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0, 2.7, 0])
        self.play(FadeIn(vt), run_time=0.4)
        self.frac(0.2)
        self.play(Write(f[0]), run_time=0.8)
        self.play(FadeIn(f[1], scale=1.2), run_time=0.4)
        br = br_din(0.48).move_to([0, 0.15, 0])
        nn = tag("un breaker de 20 A ni se entera", ROJO_P, 34).move_to([0, -1.9, 0])
        self.frac(0.3)
        self.play(FadeIn(br), FadeIn(nn), run_time=0.4)
        src = fuente("NEC 2020 · 250.53(A)(2) Excepción: electrodo de 25 Ω o menos", [0, -5.4, 0], 22)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(vt, f, br, nn, src)

        self.voz("p3")
        tab = RoundedRectangle(width=2.6, height=3.6, corner_radius=0.12, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1).move_to([-2.4, 1.4, 0])
        barra = VGroup(Rectangle(width=2.0, height=0.2, stroke_width=0).set_fill(COBRE_V, 1).move_to(tab.get_center() + DOWN * 0.8),
                       T("N + tierra", 24, "#101828", "HEAVY").move_to(tab.get_center() + DOWN * 0.45))
        lv = lavadora(1.0).move_to([2.4, 1.0, 0])
        verde = VMobject().set_points_as_corners([lv.get_bottom(), [2.4, -1.6, 0], [-2.4, -1.6, 0], tab.get_bottom()]).set_stroke(VERDE_T, 12)
        self.play(FadeIn(tab), FadeIn(barra), FadeIn(lv), run_time=0.5)
        self.frac(0.25)
        self.play(Create(verde), run_time=0.8)
        c = card("NEC · 250.4(A)(5)", ["la tierra NO es un camino", "efectivo para la falla"], VERDE_OK, 7.6, 30).move_to([0, -3.6, 0])
        self.play(FadeIn(c, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(tab, barra, lv, verde, c)

        self.voz("p4")
        tab = RoundedRectangle(width=2.4, height=3.2, corner_radius=0.12, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1).move_to([-2.4, 1.4, 0])
        br = br_din(0.55).move_to(tab)
        lv = lavadora(1.0).move_to([2.4, 1.0, 0])
        verde = VMobject().set_points_as_corners([lv.get_bottom(), [2.4, -1.6, 0], [-2.4, -1.6, 0], tab.get_bottom()]).set_stroke(VERDE_T, 12)
        self.play(FadeIn(tab), FadeIn(br), FadeIn(lv), FadeIn(verde), run_time=0.5)
        cf = corriente([lv.get_bottom(), [2.4, -1.6, 0], [-2.4, -1.6, 0], tab.get_bottom()], vel=2.6, escala=1.5, color=ROJO)
        self.add(cf)
        cien = tag("cientos de amperios", ROJO_P, 36).move_to([0, -2.8, 0])
        self.play(FadeIn(cien), run_time=0.3)
        self.frac(0.3)
        self.sfx("tic", -4)
        self.play(palanca_breaker(br, False), run_time=0.25)
        self.remove(cf)
        ok = VGroup(check(VERDE_OK, 0.35), T("carcasa sin tensión", 40, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -4.2, 0])
        self.play(FadeIn(ok), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(tab, br, lv, verde, cien, ok)

        self.voz("p5")
        vt = varilla_tierra(3.0).move_to([0, -3.4, 0])
        ry = VGroup(*[rayo([0.3 * k, 4.2, 0], [0, -1.6, 0], color=c_, semilla=k, amp=0.35, w=w_) for k, (c_, w_) in enumerate(((AMBAR, 8), (WHITE, 3)))])
        self.play(FadeIn(vt), run_time=0.4)
        self.sfx("pop", -10)
        self.play(FadeIn(ry), Flash([0, -1.6, 0], color=AMBAR, flash_radius=0.8), run_time=0.4)
        self.play(FadeOut(ry), run_time=0.3)
        usos = VGroup(card("VARILLA", ["rayos y sobretensiones"], AMBAR, 7.6, 30), card("CABLE VERDE", ["hasta cada aparato"], VERDE_OK, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 1.8, 0])
        self.frac(0.2)
        self.play(FadeIn(usos[0], shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.4)
        self.play(FadeIn(usos[1], shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(vt, usos)

        self.voz("p6")
        to = tomacorriente(np.array([0, 1.4, 0])).scale(2.2).move_to([-1.6, 1.4, 0])
        pr = probador().scale(1.2).move_to([2.2, 1.4, 0])
        self.play(FadeIn(to), FadeIn(pr), run_time=0.5)
        q = tag("¿el agujero redondo está conectado?", AMBAR, 32).move_to([0, -1.4, 0])
        self.frac(0.3)
        self.play(FadeIn(q), run_time=0.3)
        self.frac(0.4)
        r = tag("revísalo con un probador", MARCA, 36).move_to([0, -2.6, 0])
        self.play(FadeIn(r), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(to, pr, q, r)
        self.final("Varilla + cable verde: necesitas los dos")


# ====================================================================== V20 · CA vs CC
class V20D(ShortD):
    CLAVE = "v20"

    def cuerpo(self):
        self.voz("gancho")
        ba = bateria(1.5).move_to([-2.2, 1.6, 0])
        to = tomacorriente(np.array([2.2, 1.6, 0])).scale(1.8).move_to([2.2, 1.6, 0])
        self.play(FadeIn(ba), FadeIn(to), run_time=0.5)
        l = VGroup(tag("CONTINUA", AMBAR, 34).next_to(ba, DOWN, buff=0.5), tag("ALTERNA", MARCA, 34).next_to(to, DOWN, buff=0.5))
        self.frac(0.4)
        self.play(FadeIn(l[0]), run_time=0.3)
        self.play(FadeIn(l[1]), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ba, to, l)

        self.voz("p1")
        ax = Axes(x_range=[0, 4, 1], y_range=[-1.2, 1.2, 1], x_length=7.6, y_length=3.0, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.6, 0])
        cc = ax.plot(lambda t: 0.8, x_range=[0, 4], color=AMBAR, stroke_width=6)
        self.play(Create(ax), Create(cc), run_time=0.8)
        el = VGroup(*[Dot(radius=0.12, color=CIAN).move_to([-3.4 + 0.8 * k, -2.0, 0]) for k in range(9)])
        cab = Line([-3.8, -2.0, 0], [3.8, -2.0, 0]).set_stroke(COBRE_V, 26)
        self.play(FadeIn(cab), FadeIn(el), run_time=0.4)
        self.play(el.animate.shift(RIGHT * 0.8), run_time=1.0, rate_func=linear)
        self.play(el.animate.shift(RIGHT * 0.8), run_time=1.0, rate_func=linear)
        ej = VGroup(tag("baterías", AMBAR, 30), tag("paneles solares", AMBAR, 30), tag("electrónica", AMBAR, 30)).arrange(RIGHT, buff=0.2).move_to([0, -3.8, 0])
        ej.scale_to_fit_width(min(ej.width, 8.2))
        self.play(FadeIn(ej), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ax, cc, el, cab, ej)

        self.voz("p2")
        ax = Axes(x_range=[0, 2, 1], y_range=[-1.2, 1.2, 1], x_length=7.6, y_length=3.6, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.4, 0])
        s = ax.plot(lambda t: np.sin(TAU * t), x_range=[0, 2], color=CIAN, stroke_width=6)
        self.play(Create(ax), Create(s), run_time=1.2)
        hz = tag("60 veces por segundo = 60 Hz", MARCA, 34).move_to([0, -1.2, 0])
        self.play(FadeIn(hz), run_time=0.3)
        self.frac(0.25)
        pk = DashedLine(ax.c2p(0, 1), ax.c2p(2, 1)).set_stroke(ROJO_P, 3)
        ef = DashedLine(ax.c2p(0, 0.707), ax.c2p(2, 0.707)).set_stroke(AMBAR, 3)
        lv = VGroup(card("EFICAZ: 120 V", ["lo que dice el voltímetro"], AMBAR, 7.6, 30), card("PICO: ≈ 170 V", ["120 × √2"], ROJO_P, 7.6, 30)).arrange(DOWN, buff=0.25).move_to([0, -3.4, 0])
        self.play(Create(ef), FadeIn(lv[0]), run_time=0.4)
        self.frac(0.3)
        self.play(Create(pk), FadeIn(lv[1]), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ax, s, hz, pk, ef, lv)

        self.voz("p3")
        tr = transformador().scale(1.8).move_to([0, 1.4, 0])
        self.play(FadeIn(tr), run_time=0.5)
        sub = VGroup(tag("13 800 V", ROJO_P, 34), T("→", 50, TINTA, "HEAVY"), tag("120/240 V", VERDE_OK, 34)).arrange(RIGHT, buff=0.25).move_to([0, -1.6, 0])
        self.frac(0.3)
        self.play(FadeIn(sub), run_time=0.4)
        f = card("SOLO CON CA", ["el campo magnético debe cambiar", "(inducción de Faraday)"], MARCA, 7.6, 28).move_to([0, -3.6, 0])
        self.play(FadeIn(f, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(tr, sub, f)

        self.voz("p4")
        f = VGroup(T("P = I² · R", 80, AMBAR, "HEAVY")).move_to([0, 2.8, 0])
        self.play(Write(f), run_time=0.7)
        b1 = Rectangle(width=1.6, height=4.0, stroke_width=0).set_fill(ROJO_P, 1).move_to([-1.6, -3.2, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.6, height=0.04, stroke_width=0).set_fill(VERDE_OK, 1).move_to([1.6, -3.2, 0], aligned_edge=DOWN)
        l1 = VGroup(T("I", 40, TINTA, "HEAVY"), T("100 pérdidas", 26, ROJO_P, "BOLD")).arrange(DOWN, buff=0.05).next_to(b1, DOWN, buff=0.1)
        l2 = VGroup(T("I ÷ 10", 40, TINTA, "HEAVY"), T("1 pérdida", 26, VERDE_OK, "BOLD")).arrange(DOWN, buff=0.05).next_to(b2, DOWN, buff=0.1)
        self.frac(0.2)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=0.6)
        self.frac(0.25)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(f, b1, b2, l1, l2)

        self.voz("p5")
        to = tomacorriente(np.array([-2.4, 1.4, 0])).scale(1.6).move_to([-2.6, 1.4, 0])
        car = RoundedRectangle(width=1.6, height=1.9, corner_radius=0.2, stroke_color="#C7CCD6", stroke_width=2).set_fill("#F2F4F7", 1).move_to([0.4, 1.4, 0])
        cel = RoundedRectangle(width=1.3, height=2.5, corner_radius=0.18, stroke_color="#98A2B3", stroke_width=3).set_fill("#1F2430", 1).move_to([2.9, 1.4, 0])
        self.play(FadeIn(to), FadeIn(car), FadeIn(cel), run_time=0.5)
        ondas = VGroup(onda(lambda x: np.sin(x * 5), -1.8, -0.6, -1.0, 0.3, CIAN, 5), onda(lambda x: 0, 1.4, 2.6, -1.0, 0.3, AMBAR, 5))
        tx_ = VGroup(T("120 V ~", 30, CIAN, "HEAVY").move_to([-1.2, -1.8, 0]), T("5 V ⎓", 30, AMBAR, "HEAVY").move_to([2.0, -1.8, 0]))
        self.frac(0.25)
        self.play(Create(ondas), FadeIn(tx_), run_time=0.7)
        conv = tag("el cargador convierte CA en CC", MARCA, 34).move_to([0, -3.3, 0])
        self.play(FadeIn(conv), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(to, car, cel, ondas, tx_, conv)

        self.voz("p6")
        mo = motor_3f(1.4).move_to([0, 1.8, 0])
        self.play(FadeIn(mo), run_time=0.4)
        c1 = card("MOTOR DE INDUCCIÓN", ["sin escobillas gracias a la CA"], MARCA, 7.6, 30).move_to([0, -1.0, 0])
        c2 = card("LÍNEAS LARGAS Y SOLARES", ["usan CC: electrónica de potencia"], AMBAR, 7.6, 30).move_to([0, -3.2, 0])
        self.frac(0.1)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.45)
        self.play(FadeIn(c2, shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(mo, c1, c2)
        self.final("CA para transportar · CC para la electrónica")


# ====================================================================== V21 · fotocelda
class V21D(ShortD):
    CLAVE = "v21"

    def cuerpo(self):
        self.voz("gancho")
        cielo = Rectangle(width=9, height=10.3, stroke_width=0).set_fill("#F79009", 0.25).move_to([0, -0.85, 0])
        lu = luminaria(1.0).move_to([-0.6, 0.2, 0])
        self.play(FadeIn(cielo), FadeIn(lu), run_time=0.5)
        self.frac(0.3)
        self.play(cielo.animate.set_fill("#0B1530", 0.6), run_time=1.2)
        haz = Polygon(lu.lente.get_left(), lu.lente.get_right(), lu.lente.get_center() + DOWN * 5 + RIGHT * 2.0, lu.lente.get_center() + DOWN * 5 + LEFT * 2.0, stroke_width=0).set_fill("#FFE8A3", 0.25)
        self.play(lu.lente.animate.set_fill("#FFE8A3"), FadeIn(haz), run_time=0.4)
        q = tag("¿quién la enciende?", AMBAR, 40).move_to([0, 3.4, 0])
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cielo, lu, haz, q)

        self.voz("p1")
        fc = fotocelda(2.6).move_to([0, 1.8, 0])
        self.play(FadeIn(fc, scale=0.8), run_time=0.5)
        self.frac(0.2)
        se = VGroup(Circle(radius=0.8, stroke_color=AMBAR, stroke_width=4).move_to([0, -1.6, 0]),
                    VMobject().set_points_as_corners([[-0.5, -1.6, 0], [-0.3, -1.4, 0], [-0.1, -1.8, 0], [0.1, -1.4, 0], [0.3, -1.8, 0], [0.5, -1.6, 0]]).set_stroke(AMBAR, 4))
        ls = tag("fotorresistencia o fotodiodo", AMBAR, 32).move_to([0, -3.0, 0])
        self.play(FadeIn(se), FadeIn(ls), run_time=0.4)
        fl = VGroup(*[Arrow([x - 1.0, 0.0, 0], [x - 0.3, -0.9, 0], buff=0, color="#FFE8A3", stroke_width=5) for x in (-0.3, 0.3)])
        self.play(GrowArrow(fl[0]), GrowArrow(fl[1]), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(fc, se, ls, fl)

        self.voz("p2")
        x0, x1 = -3.8, 3.8
        eje = Line([x0, 1.0, 0], [x1, 1.0, 0]).set_stroke(GRIS_N, 3)
        grad = Rectangle(width=x1 - x0, height=0.6, stroke_width=0).set_fill(color=["#0B1530", "#F5C400"], opacity=1).move_to([0, 1.5, 0])
        grad.set_sheen_direction(RIGHT)
        self.play(FadeIn(grad), Create(eje), run_time=0.5)
        on = VGroup(Triangle().scale(0.2).rotate(PI).set_fill(VERDE_OK, 1).set_stroke(width=0), T("enciende: 1,5 fc ≈ 16 lux", 28, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.1).move_to([-1.8, 2.7, 0])
        self.frac(0.3)
        self.play(FadeIn(on, shift=DOWN * 0.2), run_time=0.4)
        rel = card("UN RELÉ", ["conecta la lámpara"], MARCA, 7.6, 30).move_to([0, -1.2, 0])
        self.play(FadeIn(rel), run_time=0.3)
        src = fuente("Especificación de fotocontroles según ANSI C136.10", [0, -5.3, 0], 22)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(eje, grad, on, rel, src)

        self.voz("p3")
        x0, x1 = -3.8, 3.8
        eje = Line([x0, 1.0, 0], [x1, 1.0, 0]).set_stroke(GRIS_N, 3)
        on = Line([-1.8, 0.6, 0], [-1.8, 2.2, 0]).set_stroke(VERDE_OK, 6)
        off = Line([-0.2, 0.6, 0], [-0.2, 2.2, 0]).set_stroke(ROJO_P, 6)
        banda = Rectangle(width=1.6, height=1.6, stroke_width=0).set_fill(AMBAR, 0.3).move_to([-1.0, 1.4, 0])
        lb = VGroup(T("enciende", 26, VERDE_OK, "HEAVY").next_to(on, UP, buff=0.1).shift(LEFT * 0.6), T("apaga ≤ 1,5×", 26, ROJO_P, "HEAVY").next_to(off, UP, buff=0.1).shift(RIGHT * 0.9))
        self.play(Create(eje), Create(on), Create(off), FadeIn(banda), FadeIn(lb), run_time=0.6)
        self.frac(0.2)
        car = VGroup(RoundedRectangle(width=2.4, height=0.9, corner_radius=0.2, stroke_width=0).set_fill("#344054", 1), Circle(radius=0.15, stroke_width=0).set_fill("#FFE8A3", 1).shift(RIGHT * 1.0)).move_to([-3.0, -2.2, 0])
        self.play(FadeIn(car), car.animate.shift(RIGHT * 5.5), run_time=1.2)
        rt = tag("retardo de 3 a 5 s", MARCA, 36).move_to([0, -3.8, 0])
        self.play(FadeIn(rt), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(eje, on, off, banda, lb, car, rt)

        self.voz("p4")
        lu = luminaria(0.9, True).move_to([-0.6, 0.4, 0])
        sol = Circle(radius=0.7, stroke_width=0).set_fill("#F5C400", 1).move_to([3.0, 3.6, 0])
        self.play(FadeIn(lu), FadeIn(sol), run_time=0.4)
        fx = tag("falla → queda ENCENDIDA", AMBAR, 36).move_to([0, -3.6, 0])
        self.frac(0.25)
        self.play(FadeIn(fx), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(lu, sol, fx)

        self.voz("p5")
        fc = fotocelda(2.0).move_to([0, 2.2, 0])
        base3 = VGroup(Circle(radius=1.4, stroke_color="#98A2B3", stroke_width=3).set_fill("#344054", 1),
                       *[RoundedRectangle(width=0.18, height=0.5, corner_radius=0.05, stroke_width=0).set_fill(COBRE_V, 1).move_to(1.0 * np.array([np.cos(a), np.sin(a), 0])).rotate(a + PI / 2)
                         for a in (PI / 2, PI / 2 + 2.1, PI / 2 - 2.1)]).move_to([0, -0.6, 0])
        self.play(FadeIn(fc), FadeIn(base3), run_time=0.5)
        self.play(Rotate(fc, 0.4), run_time=0.5)
        tip = card("SI PARPADEA", ["su propia luz o un anuncio", "le pega a la fotocelda"], ROJO_P, 7.6, 28).move_to([0, -3.4, 0])
        self.frac(0.35)
        self.play(FadeIn(tip, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(fc, base3, tip)

        self.voz("p6")
        casa = VGroup(Polygon([-2.2, 0.4, 0], [2.2, 0.4, 0], [0, 2.4, 0], stroke_width=0).set_fill("#B54708", 1), Rectangle(width=3.6, height=2.6, stroke_width=0).set_fill("#E4E7EC", 1).move_to([0, -0.9, 0]))
        fcx = fotocelda(0.7).move_to([2.3, 0.0, 0])
        self.play(FadeIn(casa), FadeIn(fcx), run_time=0.4)
        con = VGroup(tag("fase entra", NEGRO_BK, 28), tag("salida → lámpara", ROJO_P, 28), tag("neutro", "#F2F4F7", 28)).arrange(DOWN, buff=0.2).move_to([0, -3.6, 0])
        self.frac(0.3)
        self.play(LaggedStart(*[FadeIn(c_) for c_ in con], lag_ratio=0.3), run_time=0.8)
        self.cerrar_voz(0.15)
        self.limpiar(casa, fcx, con)
        self.final("Fotocelda: sensor de luz + relé")


# ====================================================================== V22 · toques
class V22D(ShortD):
    CLAVE = "v22"

    def cuerpo(self):
        self.voz("gancho")
        man = VGroup(RoundedRectangle(width=2.4, height=0.5, corner_radius=0.25, stroke_width=0).set_fill("#C9CED6", 1), Circle(radius=0.5, stroke_width=0).set_fill("#98A2B3", 1).shift(LEFT * 1.3)).move_to([1.2, 1.6, 0])
        mano = Circle(radius=0.55).set_fill(PIEL, 1).set_stroke("#9A6A4A", 2).move_to([-2.4, 1.6, 0])
        self.play(FadeIn(man), FadeIn(mano), run_time=0.4)
        self.play(mano.animate.move_to([-0.5, 1.6, 0]), run_time=0.6)
        self.sfx("pop", -8)
        ch = rayo(mano.get_right(), man.get_left() + LEFT * 0.0, color=CIAN, amp=0.08)
        self.play(FadeIn(ch), Flash(mano.get_right(), color=CIAN), run_time=0.3)
        dos = VGroup(tag("uno es inofensivo", VERDE_OK, 34), tag("el otro puede matarte", ROJO_P, 34)).arrange(DOWN, buff=0.25).move_to([0, -2.0, 0])
        self.frac(0.3)
        self.play(FadeIn(dos[0]), run_time=0.3)
        self.play(FadeIn(dos[1]), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(man, mano, ch, dos)

        self.voz("p1")
        p_ = persona().scale(1.6).move_to([0, 0.6, 0])
        cargas = VGroup(*[T("−", 40, CIAN, "HEAVY").move_to(p_.get_center() + np.array([np.cos(a) * 1.4, np.sin(a) * 2.2, 0])) for a in np.linspace(0, TAU, 10, endpoint=False)])
        self.play(FadeIn(p_), run_time=0.4)
        self.frac(0.2)
        self.play(LaggedStart(*[FadeIn(c_, scale=0.5) for c_ in cargas], lag_ratio=0.1), run_time=1.0)
        tb = tag("efecto triboeléctrico", MARCA, 36).move_to([0, -3.4, 0])
        self.play(FadeIn(tb), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(p_, cargas, tb)

        self.voz("p2")
        d = VGroup(card("MILES DE VOLTIOS", ["pero dura microsegundos"], CIAN, 7.6, 30), card("MUY POCA ENERGÍA", ["solo un susto"], VERDE_OK, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        self.play(FadeIn(d[0], shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(d[1], shift=RIGHT * 0.2), run_time=0.4)
        hum = VGroup(gotas(np.array([-1.0, -2.0, 0]), 7, "#7FD1FF").scale(1.4), T("la humedad disipa la carga", 30, CLARO, "BOLD").move_to([0, -3.8, 0]))
        self.frac(0.3)
        self.play(FadeIn(hum), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(d, hum)

        self.voz("p3")
        lv = lavadora(1.4).move_to([1.4, 1.2, 0])
        self.play(FadeIn(lv), run_time=0.4)
        cab = Line(lv.get_left() + UP * 0.5 + RIGHT * 0.25, lv.get_left() + RIGHT * 0.25 + DOWN * 0.4).set_stroke(NEGRO_BK, 8)
        self.frac(0.15)
        self.play(Create(cab), lv[0].animate.set_stroke(ROJO_P, 5), run_time=0.5)
        sin = VGroup(equis(ROJO, 0.3), T("sin tierra", 36, ROJO_P, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([0, -1.6, 0])
        self.play(FadeIn(sin), run_time=0.3)
        hor = tag("hormigueo constante", AMBAR, 38).move_to([0, -3.2, 0])
        self.frac(0.35)
        self.play(FadeIn(hor), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(lv, cab, sin, hor)

        self.voz("p4")
        f = VGroup(T("120 V", 90, ROJO_P, "HEAVY"), T("pasando por ti", 40, TINTA, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0, 2.0, 0])
        self.play(FadeIn(f, scale=1.1), run_time=0.4)
        rl = regla_log(-4.8, -0.6, 1, 100, x=0.0) if False else VGroup()
        esc = VGroup(card("6–16 mA", ["no te puedes soltar (OSHA)"], ROJO_P, 7.6, 30)).move_to([0, -1.6, 0])
        self.frac(0.35)
        self.play(FadeIn(esc, shift=UP * 0.2), run_time=0.4)
        cz = corazon(0.8).move_to([0, -4.0, 0])
        self.play(FadeIn(cz, scale=0.5), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(f, esc, cz)

        self.voz("p5")
        tt = T("LA REGLA", 50, AMBAR, "HEAVY").move_to([0, 3.4, 0])
        a = card("CHISPA DE UN INSTANTE", ["estática"], VERDE_OK, 7.6, 30)
        b = card("HORMIGUEO QUE SE REPITE", ["falla: desconecta y revisa"], ROJO_P, 7.6, 30)
        VGroup(a, b).arrange(DOWN, buff=0.4).move_to([0, 0.2, 0])
        self.play(FadeIn(tt), run_time=0.3)
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(tt, a, b)

        self.voz("p6")
        ll = VGroup(Rectangle(width=3.0, height=0.5, stroke_width=0).set_fill("#C9CED6", 1), Circle(radius=0.45, stroke_width=0).set_fill("#98A2B3", 1).shift(LEFT * 1.7)).move_to([0, 2.0, 0])
        self.play(FadeIn(ll), run_time=0.3)
        tr = tag("toca primero con una llave", MARCA, 36).move_to([0, 0.4, 0])
        self.play(FadeIn(tr), run_time=0.3)
        self.frac(0.4)
        fx = card("PARA UN APARATO CON FUGA", ["reparar + conductor de tierra"], ROJO_P, 7.6, 30).move_to([0, -2.4, 0])
        self.play(FadeIn(fx, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ll, tr, fx)
        self.final("Chispa: estática · Hormigueo: falla")


# ====================================================================== V23 · giro del motor
class V23D(ShortD):
    CLAVE = "v23"

    def estator(self, c=ORIGIN, r=2.2):
        anillo = Annulus(inner_radius=r * 0.72, outer_radius=r, stroke_width=0).set_fill("#667085", 1).move_to(c)
        cols = [ROJO_P, AMBAR, AZUL_C]
        bob = VGroup(*[RoundedRectangle(width=0.7, height=0.45, corner_radius=0.1, stroke_width=0).set_fill(cols[k % 3], 1)
                       .move_to(c + r * 0.86 * np.array([np.cos(a), np.sin(a), 0])).rotate(a) for k, a in enumerate(np.linspace(PI / 2, PI / 2 + TAU, 6, endpoint=False))])
        rotor = Circle(radius=r * 0.6, stroke_color="#98A2B3", stroke_width=3).set_fill("#344054", 1).move_to(c)
        barras = VGroup(*[Line(c + r * 0.15 * np.array([np.cos(a), np.sin(a), 0]), c + r * 0.55 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(COBRE_V, 4) for a in np.linspace(0, TAU, 12, endpoint=False)])
        return VGroup(anillo, bob, rotor, barras)

    def cuerpo(self):
        self.voz("gancho")
        mo = motor_3f(1.5).move_to([0, 1.6, 0])
        self.play(FadeIn(mo), run_time=0.4)
        g = Arc(radius=1.6, start_angle=0, angle=PI * 1.4, color=ROJO_P, stroke_width=6).move_arc_center_to(mo.get_center()).add_tip()
        self.play(Create(g), run_time=0.6)
        sol = tag("cambia DOS cables", VERDE_OK, 40).move_to([0, -1.8, 0])
        self.frac(0.35)
        self.play(FadeIn(sol, scale=1.1), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(mo, g, sol)

        self.voz("p1")
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-1.2, 1.2, 1], x_length=7.6, y_length=3.2, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.4, 0])
        cs = VGroup(*[ax.plot(lambda t, k=k: np.sin(TAU * t - k * TAU / 3), x_range=[0, 1], color=c, stroke_width=5) for k, c in enumerate((ROJO_P, AMBAR, AZUL_C))])
        self.play(Create(ax), run_time=0.3)
        for c_ in cs:
            self.play(Create(c_), run_time=0.6)
        lab = tag("separadas 120°", MARCA, 36).move_to([0, -1.6, 0])
        self.play(FadeIn(lab), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ax, cs, lab)

        self.voz("p2")
        es = self.estator([0, 1.0, 0])
        self.play(FadeIn(es), run_time=0.5)
        fl = Arrow([0, 1.0, 0], [0, 2.3, 0], buff=0, color=CIAN, stroke_width=10)
        self.add(fl)
        self.play(Rotate(fl, -TAU, about_point=[0, 1.0, 0]), Rotate(es[3], -TAU * 0.9, about_point=[0, 1.0, 0]), run_time=2.5, rate_func=linear)
        rpm = VGroup(T("120 × 60 ÷ 4", 48, TINTA, "HEAVY"), T("= 1800 rpm", 64, AMBAR, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, -3.0, 0])
        self.play(Write(rpm), run_time=0.8)
        self.cerrar_voz(0.15)
        self.limpiar(es, fl, rpm)

        self.voz("p3")
        fases = VGroup(*[tag(t, c, 44) for t, c in (("L1", ROJO_P), ("L2", AMBAR), ("L3", AZUL_C))]).arrange(RIGHT, buff=0.6).move_to([0, 2.6, 0])
        self.play(FadeIn(fases), run_time=0.4)
        self.frac(0.25)
        self.sfx("whoosh", -12)
        self.play(Swap(fases[1], fases[2]), run_time=0.8)
        es = self.estator([0, -1.6, 0], 1.8)
        fl = Arrow([0, -1.6, 0], [0, -0.5, 0], buff=0, color=CIAN, stroke_width=10)
        self.play(FadeIn(es), FadeIn(fl), run_time=0.3)
        self.play(Rotate(fl, TAU, about_point=[0, -1.6, 0]), Rotate(es[3], TAU * 0.9, about_point=[0, -1.6, 0]), run_time=2.0, rate_func=linear)
        self.cerrar_voz(0.15)
        self.limpiar(fases, es, fl)

        self.voz("p4")
        a = VGroup(*[tag(t, c, 40) for t, c in (("L1", ROJO_P), ("L2", AMBAR), ("L3", AZUL_C))]).arrange(RIGHT, buff=0.5).move_to([0, 2.4, 0])
        self.play(FadeIn(a), run_time=0.3)
        self.play(a[0].animate.move_to(a[1].get_center()), a[1].animate.move_to(a[2].get_center()), a[2].animate.move_to(a[0].get_center()), run_time=0.8)
        ig = card("LAS TRES EN ORDEN", ["misma secuencia: mismo giro"], AMBAR, 7.6, 30).move_to([0, -0.4, 0])
        self.play(FadeIn(ig), run_time=0.4)
        dd = tag("DOS, y solo dos", VERDE_OK, 44).move_to([0, -2.8, 0])
        self.frac(0.3)
        self.play(FadeIn(dd, scale=1.1), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(a, ig, dd)

        self.voz("p5")
        mo = motor_3f(1.2).move_to([0, 2.0, 0])
        self.play(FadeIn(mo), run_time=0.3)
        p1 = card("BOMBAS Y COMPRESORES", ["algunos se dañan al revés"], ROJO_P, 7.6, 30).move_to([0, -0.6, 0])
        p2 = card("PULSO CORTO", ["revisa el sentido antes de acoplar"], VERDE_OK, 7.6, 30).move_to([0, -2.6, 0])
        self.play(FadeIn(p1), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(p2), run_time=0.4)
        inv = tag("inversor de giro: 2 contactores", MARCA, 32).move_to([0, -4.4, 0])
        self.frac(0.3)
        self.play(FadeIn(inv), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(mo, p1, p2, inv)

        self.voz("p6")
        es = self.estator([0, 1.4, 0], 1.9)
        f1 = Arrow([0, 1.4, 0], [0, 2.5, 0], buff=0, color=CIAN, stroke_width=10)
        self.play(FadeIn(es), FadeIn(f1), run_time=0.3)
        self.play(Rotate(f1, -TAU, about_point=[0, 1.4, 0]), Rotate(es[3], -TAU * 0.96, about_point=[0, 1.4, 0]), run_time=2.0, rate_func=linear)
        d = VGroup(T("1800 → ~1765 rpm", 52, AMBAR, "HEAVY"), T("deslizamiento", 36, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, -1.8, 0])
        self.play(FadeIn(d), run_time=0.4)
        md = tag("medidor de secuencia de fases", MARCA, 32).move_to([0, -3.9, 0])
        self.frac(0.3)
        self.play(FadeIn(md), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(es, f1, d, md)
        self.final("Invierte dos fases, nunca las tres")


# ====================================================================== V24 · efecto corona
class V24D(ShortD):
    CLAVE = "v24"

    def cuerpo(self):
        self.voz("gancho")
        noche = Rectangle(width=9, height=10.3, stroke_width=0).set_fill("#060C1C", 0.8).move_to([0, -0.85, 0])
        lin = VGroup(*[linea_aerea(P(-4.6, y), P(4.6, y), 0.3, "#B8BEC8", 4) for y in (2.6, 1.6, 0.6)])
        self.play(FadeIn(noche), Create(lin), run_time=0.7)
        glow = VGroup(*[l.copy().set_stroke("#9EC5FF", 14, 0.25) for l in lin])
        ondas = ondas_sonido(np.array([0, -1.6, 0]), 3, 0.5, 0.4, PI / 2, CIAN, PI / 2)
        self.play(FadeIn(glow), Create(ondas), run_time=0.8)
        nm = tag("EFECTO CORONA", MARCA, 44).move_to([0, -3.8, 0])
        self.frac(0.3)
        self.play(FadeIn(nm, scale=1.1), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(noche, lin, glow, ondas, nm)

        self.voz("p1")
        cond = Circle(radius=0.6, stroke_width=0).set_fill("#B8BEC8", 1).move_to([0, 1.0, 0])
        lineas = VGroup(*[Arrow(cond.get_center() + 0.65 * np.array([np.cos(a), np.sin(a), 0]), cond.get_center() + 2.6 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=AMBAR, stroke_width=4) for a in np.linspace(0, TAU, 16, endpoint=False)])
        self.play(FadeIn(cond), LaggedStart(*[GrowArrow(l) for l in lineas], lag_ratio=0.05), run_time=1.2)
        lc = tag("el campo es mayor junto al cable", AMBAR, 32).move_to([0, -2.6, 0])
        self.play(FadeIn(lc), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cond, lineas, lc)

        self.voz("p2")
        n = VGroup(T("≈ 30 kV/cm", 80, AMBAR, "HEAVY"), T("rigidez del aire (nivel del mar)", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, 3.0, 0])
        self.play(FadeIn(n), run_time=0.4)
        cond = Circle(radius=0.55, stroke_width=0).set_fill("#B8BEC8", 1).move_to([0, -0.8, 0])
        halo = VGroup(*[Circle(radius=0.6 + 0.12 * k, stroke_width=0).set_fill("#9EC5FF", 0.18 - 0.03 * k).move_to(cond) for k in range(5)])
        self.frac(0.2)
        self.play(FadeIn(cond), FadeIn(halo), run_time=0.6)
        de = VGroup(*[rayo(cond.get_center() + 0.55 * np.array([np.cos(a), np.sin(a), 0]), cond.get_center() + 1.1 * np.array([np.cos(a), np.sin(a), 0]), color="#C9DCFF", semilla=k, amp=0.06, w=2) for k, a in enumerate(np.linspace(0, TAU, 10, endpoint=False))])
        self.sfx("pop", -16)
        self.play(FadeIn(de), run_time=0.3)
        az = tag("brillo azul + zumbido", MARCA, 34).move_to([0, -3.4, 0])
        self.play(FadeIn(az), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(n, cond, halo, de, az)

        self.voz("p3")
        cab = Line([-4.0, 1.4, 0], [4.0, 1.4, 0]).set_stroke("#B8BEC8", 22)
        self.play(Create(cab), run_time=0.4)
        gt = VGroup(*[Circle(radius=0.12, stroke_width=0).set_fill("#7FD1FF", 1).move_to([x, 1.15, 0]) for x in np.linspace(-3.4, 3.4, 9)])
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.1) for g in gt], lag_ratio=0.08), run_time=0.8)
        pts = VGroup(*[rayo(g.get_bottom(), g.get_bottom() + DOWN * 0.5, color="#C9DCFF", semilla=k, amp=0.05, w=2) for k, g in enumerate(gt)])
        self.play(FadeIn(pts), run_time=0.3)
        tt = tag("con humedad: más ruido", AMBAR, 36).move_to([0, -1.6, 0])
        self.play(FadeIn(tt), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cab, gt, pts, tt)

        self.voz("p4")
        un = Circle(radius=0.55, stroke_width=0).set_fill("#B8BEC8", 1).move_to([-2.0, 1.6, 0])
        haz = VGroup(*[Circle(radius=0.32, stroke_width=0).set_fill("#B8BEC8", 1).move_to([2.0 + 0.5 * np.cos(a), 1.6 + 0.5 * np.sin(a), 0]) for a in (PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4)])
        sep = VGroup(*[Line(haz[k].get_center(), haz[(k + 1) % 4].get_center()).set_stroke("#667085", 3) for k in range(4)])
        self.play(FadeIn(un), FadeIn(sep), FadeIn(haz), run_time=0.5)
        l = VGroup(T("1 conductor", 28, TINTA, "BOLD").next_to(un, DOWN, buff=0.5), T("haz de 4", 28, TINTA, "BOLD").next_to(haz, DOWN, buff=0.5))
        self.play(FadeIn(l), run_time=0.3)
        p = card("ENERGÍA PERDIDA", ["e interferencia de radio"], ROJO_P, 7.6, 30).move_to([0, -1.6, 0])
        q = card("HACES DE CONDUCTORES", ["menos campo en la superficie"], VERDE_OK, 7.6, 30).move_to([0, -3.6, 0])
        self.frac(0.05)
        self.play(FadeIn(p), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(q), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(un, haz, sep, l, p, q)

        self.voz("p5")
        po = poste(6.0, 4.4, 2)[0].move_to([0, 0.0, 0])
        es = escalera(3.6, 0.7).move_to([2.6, -2.4, 0])
        self.play(FadeIn(po), FadeIn(es), run_time=0.5)
        x_ = equis(ROJO, 0.5).move_to(es.get_top() + UP * 0.6)
        self.frac(0.3)
        self.play(FadeIn(x_, scale=1.4), run_time=0.3)
        ad = tag("está energizada: aléjate", ROJO_P, 38).move_to([0, -5.0, 0])
        self.play(FadeIn(ad), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(po, es, x_, ad)

        self.voz("p6")
        an = VGroup(Circle(radius=1.6, stroke_color="#C9CED6", stroke_width=14), Circle(radius=1.1, stroke_color="#C9CED6", stroke_width=6)).move_to([0, 2.0, 0])
        ai = VGroup(*[Ellipse(width=1.6, height=0.4).set_fill("#EEF0EA", 1).set_stroke("#98A2B3", 2).move_to([0, 2.0 - 0.35 * k, 0]) for k in range(5)]).move_to([0, 2.0, 0])
        self.play(FadeIn(ai), FadeIn(an), run_time=0.5)
        l = tag("anillos anticorona", MARCA, 36).move_to([0, -0.4, 0])
        self.play(FadeIn(l), run_time=0.3)
        uv = card("CÁMARAS ULTRAVIOLETA", ["ven la corona de día"], VIOLETA if 'VIOLETA' in globals() else "#9E77ED", 7.6, 30).move_to([0, -2.6, 0])
        self.frac(0.35)
        self.play(FadeIn(uv, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(an, ai, l, uv)
        self.final("Corona: el aire se ioniza junto al cable")


# ====================================================================== V25 · fusible
class V25D(ShortD):
    CLAVE = "v25"

    def cuerpo(self):
        self.voz("gancho")
        fu = fusible_vidrio(1.6).move_to([0, 1.6, 0])
        self.play(FadeIn(fu, scale=0.8), run_time=0.5)
        q = tag("metal que se derrite a propósito", AMBAR, 34).move_to([0, -1.2, 0])
        self.frac(0.35)
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(fu, q)

        self.voz("p1")
        el = VGroup()
        for k in range(4):
            el.add(Rectangle(width=1.0, height=0.9, stroke_width=0).set_fill("#D9D9D9", 1).move_to([-3.0 + 2.0 * k, 1.6, 0]))
            if k < 3:
                el.add(Rectangle(width=1.0, height=0.25, stroke_width=0).set_fill("#D9D9D9", 1).move_to([-2.0 + 2.0 * k, 1.6, 0]))
        self.play(FadeIn(el), run_time=0.5)
        cu = VGroup(*[Circle(radius=0.35, stroke_color=AMBAR, stroke_width=4).move_to([-2.0 + 2.0 * k, 1.6, 0]) for k in range(3)])
        lc = tag("CUELLOS: más resistencia", AMBAR, 36).move_to([0, -0.4, 0])
        self.frac(0.25)
        self.play(Create(cu), FadeIn(lc), run_time=0.5)
        self.frac(0.3)
        self.play(*[c_.animate.set_fill("#FF6B3D", 0.6) for c_ in cu], run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(el, cu, lc)

        self.voz("p2")
        f = VGroup(T("calor ∝ I² · t", 72, AMBAR, "HEAVY")).move_to([0, 3.0, 0])
        self.play(Write(f), run_time=0.7)
        b1 = VGroup(card("SOBRECARGA", ["tarda: segundos o minutos"], AMBAR, 7.6, 30), card("CORTOCIRCUITO", ["milisegundos"], ROJO_P, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        self.frac(0.15)
        self.play(FadeIn(b1[0], shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.25)
        self.play(FadeIn(b1[1], shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(f, b1)

        self.voz("p3")
        cuerpo = RoundedRectangle(width=6.6, height=2.4, corner_radius=0.3, stroke_color="#C7CCD6", stroke_width=3).set_fill("#EEF0EA", 1).move_to([0, 1.2, 0])
        arena = VGroup(*[Dot(radius=0.05, color="#D9C38A").move_to([np.random.uniform(-3.0, 3.0), np.random.uniform(0.2, 2.2), 0]) for _ in range(140)])
        el = Line([-3.2, 1.2, 0], [3.2, 1.2, 0]).set_stroke("#9AA3AF", 6)
        self.play(FadeIn(cuerpo), FadeIn(arena), Create(el), run_time=0.6)
        self.sfx("pop", -10)
        ar = rayo([-0.4, 1.2, 0], [0.4, 1.2, 0], color=AMBAR, amp=0.2, w=6)
        self.play(FadeIn(ar), Flash([0, 1.2, 0], color=AMBAR), run_time=0.3)
        self.play(FadeOut(ar), run_time=0.6)
        ls = tag("arena de sílice: absorbe el calor y apaga el arco", MARCA, 30).move_to([0, -1.4, 0])
        self.play(FadeIn(ls), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cuerpo, arena, el, ls)

        self.voz("p4")
        fu = fusible_vidrio(0.9, True).move_to([-2.0, 1.8, 0])
        br = breaker_on(breaker_din(1, 20, "C", s=0.7)).move_to([2.2, 1.6, 0])
        self.play(FadeIn(fu), FadeIn(br), run_time=0.4)
        cmp_ = VGroup(card("FUSIBLE", ["simple, rápido, barato", "se cambia cada vez"], AMBAR, 7.6, 30), card("BREAKER", ["se rearma con la palanca"], MARCA, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, -1.8, 0])
        self.frac(0.15)
        self.play(FadeIn(cmp_), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(fu, br, cmp_)

        self.voz("p5")
        fu = fusible_vidrio(1.4).move_to([0, 2.0, 0])
        alam = Line([-2.2, 2.0, 0], [2.2, 2.0, 0]).set_stroke(COBRE_V, 10)
        self.play(FadeIn(fu), run_time=0.3)
        self.frac(0.15)
        self.play(Create(alam), run_time=0.4)
        x_ = equis(ROJO, 0.6).move_to([0, 2.0, 0])
        self.play(FadeIn(x_, scale=1.4), run_time=0.3)
        ll = llama(1.0).move_to([0, -1.2, 0])
        lp = tag("se quema el aislamiento dentro de la pared", ROJO_P, 30).move_to([0, -3.0, 0])
        self.frac(0.25)
        self.play(FadeIn(ll), FadeIn(lp), run_time=0.4)
        ok = tag("reemplázalo por uno IGUAL", VERDE_OK, 36).move_to([0, -4.4, 0])
        self.frac(0.3)
        self.play(FadeIn(ok), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(fu, alam, x_, ll, lp, ok)

        self.voz("p6")
        tipos = VGroup(card("RÁPIDO", ["electrónica"], CIAN, 7.6, 30), card("RETARDADO", ["aguanta el arranque de un motor"], AMBAR, 7.6, 30),
                       card("gG · aM", ["uso general · acompañamiento de motores"], MARCA, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 0.4, 0])
        for t_ in tipos:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.4)
            self.frac(0.25)
        self.cerrar_voz(0.15)
        self.limpiar(tipos)
        self.final("El fusible protege al cable: nunca lo puentees")


# ====================================================================== V26 · factor de potencia
class V26D(ShortD):
    CLAVE = "v26"

    def cuerpo(self):
        self.voz("gancho")
        m = VGroup(motor_3f(0.9), motor_3f(0.9)).arrange(RIGHT, buff=0.6).move_to([0, 2.0, 0])
        self.play(FadeIn(m), run_time=0.4)
        a = VGroup(T("12,7 A", 54, VERDE_OK, "HEAVY").next_to(m[0], DOWN, buff=0.4), T("17,2 A", 54, ROJO_P, "HEAVY").next_to(m[1], DOWN, buff=0.4))
        self.frac(0.3)
        self.play(FadeIn(a), run_time=0.4)
        q = tag("¿mismo trabajo?", AMBAR, 40).move_to([0, -2.2, 0])
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(m, a, q)

        self.voz("p1")
        p = card("POTENCIA ACTIVA · kW", ["hace el trabajo"], VERDE_OK, 7.6, 30).move_to([0, 2.2, 0])
        q = card("POTENCIA REACTIVA · kvar", ["crea el campo magnético", "va y viene sin hacer trabajo"], AMBAR, 7.6, 30).move_to([0, -0.2, 0])
        self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(p, q)

        self.voz("p2")
        o = np.array([-3.0, -1.0, 0])
        pa = Arrow(o, o + RIGHT * 5.5, buff=0, color=VERDE_OK, stroke_width=10)
        pr = Arrow(o + RIGHT * 5.5, o + RIGHT * 5.5 + UP * 3.4, buff=0, color=AMBAR, stroke_width=10)
        ps = Arrow(o, o + RIGHT * 5.5 + UP * 3.4, buff=0, color=MARCA, stroke_width=10)
        self.play(GrowArrow(pa), run_time=0.5)
        self.play(GrowArrow(pr), run_time=0.5)
        self.play(GrowArrow(ps), run_time=0.5)
        lb = VGroup(T("kW", 34, VERDE_OK, "HEAVY").next_to(pa, DOWN, buff=0.15), T("kvar", 34, AMBAR, "HEAVY").next_to(pr, RIGHT, buff=0.1), T("kVA", 34, MARCA, "HEAVY").move_to(o + RIGHT * 2.2 + UP * 2.2))
        self.play(FadeIn(lb), run_time=0.3)
        fp = VGroup(T("FP = kW ÷ kVA", 56, TINTA, "HEAVY")).move_to([0, -3.6, 0])
        self.frac(0.25)
        self.play(Write(fp), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(pa, pr, ps, lb, fp)

        self.voz("p3")
        f = MathTex(r"P=\sqrt{3}\,V\,I\,\cos\varphi", color=TINTA).scale(1.6).move_to([0, 3.0, 0])
        self.play(Write(f), run_time=0.7)
        b1 = Rectangle(width=1.6, height=2.6, stroke_width=0).set_fill(VERDE_OK, 1).move_to([-1.6, -2.8, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.6, height=2.6 * 1.357, stroke_width=0).set_fill(ROJO_P, 1).move_to([1.6, -2.8, 0], aligned_edge=DOWN)
        l = VGroup(T("FP 0,95", 30, VERDE_OK, "HEAVY").next_to(b1, DOWN, buff=0.1), T("FP 0,70", 30, ROJO_P, "HEAVY").next_to(b2, DOWN, buff=0.1))
        self.frac(0.25)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l[0]), run_time=0.5)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l[1]), run_time=0.5)
        m36 = tag("+36 % de corriente", ROJO_P, 36).next_to(b2, UP, buff=0.2)
        self.play(FadeIn(m36), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(f, b1, b2, l, m36)

        self.voz("p4")
        it = VGroup(card("CABLES MÁS CALIENTES", [], ROJO_P, 7.6, 28), card("MÁS PÉRDIDAS", [], AMBAR, 7.6, 28), card("TRANSFORMADOR MÁS CARGADO", [], AMBAR, 7.6, 28),
                    card("RECARGO EN LA FACTURA", ["en la industria"], MARCA, 7.6, 28)).arrange(DOWN, buff=0.25).move_to([0, 0.4, 0])
        for t_ in it:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.35)
            self.frac(0.18)
        self.cerrar_voz(0.15)
        self.limpiar(it)

        self.voz("p5")
        cap = VGroup(RoundedRectangle(width=1.6, height=2.6, corner_radius=0.3, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1), T("kvar", 30, "#101828", "HEAVY")).move_to([-2.0, 1.6, 0])
        mo = motor_3f(0.9).move_to([2.0, 1.6, 0])
        self.play(FadeIn(cap), FadeIn(mo), run_time=0.4)
        fl = VGroup(Arrow(cap.get_right(), mo.get_left(), buff=0.1, color=AMBAR, stroke_width=8), Arrow(mo.get_left() + DOWN * 0.4, cap.get_right() + DOWN * 0.4, buff=0.1, color=AMBAR, stroke_width=8))
        self.play(GrowArrow(fl[0]), GrowArrow(fl[1]), run_time=0.6)
        tx_ = tag("los capacitores dan la reactiva cerca del motor", MARCA, 30).move_to([0, -1.4, 0])
        self.play(FadeIn(tx_), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cap, mo, fl, tx_)

        self.voz("p6")
        d = VGroup(T("10 kW · 480 V", 50, TINTA, "HEAVY"), T("FP 0,95 → 12,7 A", 44, VERDE_OK, "HEAVY"), T("FP 0,70 → 17,2 A", 44, ROJO_P, "HEAVY")).arrange(DOWN, buff=0.3).move_to([0, 2.0, 0])
        for l in d:
            self.play(FadeIn(l, shift=UP * 0.15), run_time=0.35)
            self.frac(0.15)
        sob = card("MOTOR SOBREDIMENSIONADO", ["poca carga = peor factor de potencia"], AMBAR, 7.6, 30).move_to([0, -2.4, 0])
        self.frac(0.2)
        self.play(FadeIn(sob), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(d, sob)
        self.final("FP bajo = más corriente para el mismo trabajo")


# ====================================================================== V27 · sensor inductivo
class V27D(ShortD):
    CLAVE = "v27"

    def cuerpo(self):
        self.voz("gancho")
        se = sensor_inductivo(1.3).move_to([-0.6, 1.6, 0])
        pz = Square(1.0, stroke_width=0).set_fill("#98A2B3", 1).move_to([4.0, 1.6, 0])
        self.play(FadeIn(se), FadeIn(pz), run_time=0.4)
        self.play(pz.animate.move_to([2.2, 1.6, 0]), run_time=0.8)
        self.play(se.luz.animate.set_fill("#F5A524"), run_time=0.2)
        q = tag("sin tocarla", AMBAR, 40).move_to([0, -1.2, 0])
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(se, pz, q)

        self.voz("p1")
        bob = VGroup(*[Ellipse(width=0.6, height=2.0).set_stroke(COBRE_V, 4).move_to([-0.6 + 0.2 * k, 1.4, 0]) for k in range(6)])
        osc = onda(lambda x: np.sin(x * 6), -3.8, -1.6, 1.4, 0.4, CIAN, 4)
        campo = VGroup(*[Arc(radius=0.8 + 0.4 * k, start_angle=-PI / 3, angle=2 * PI / 3).set_stroke(MARCA, 3).move_arc_center_to([0.6, 1.4, 0]) for k in range(4)])
        self.play(Create(osc), FadeIn(bob), run_time=0.6)
        self.play(LaggedStart(*[Create(c) for c in campo], lag_ratio=0.2), run_time=0.8)
        lt = tag("oscilador + bobina = campo alterno", MARCA, 32).move_to([0, -1.6, 0])
        self.play(FadeIn(lt), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(bob, osc, campo, lt)

        self.voz("p2")
        pz = Rectangle(width=2.4, height=2.4, stroke_width=0).set_fill("#98A2B3", 1).move_to([0, 1.6, 0])
        rem = VGroup(*[Circle(radius=r).set_stroke(ROJO_P, 4).move_to(pz) for r in (0.4, 0.8)])
        self.play(FadeIn(pz), run_time=0.3)
        self.play(Create(rem), run_time=0.6)
        lf = tag("corrientes de Foucault", ROJO_P, 34).move_to([0, -0.4, 0])
        self.play(FadeIn(lf), run_time=0.3)
        os_ = onda(lambda x: np.sin(x * 6) * np.exp(-max(x + 1.0, 0) * 0.8), -3.8, 3.8, -2.6, 0.6, CIAN, 4)
        self.frac(0.2)
        self.play(Create(os_), run_time=1.0)
        sal = tag("la oscilación baja → salida activa", VERDE_OK, 32).move_to([0, -4.4, 0])
        self.play(FadeIn(sal), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(pz, rem, lf, os_, sal)

        self.voz("p3")
        d = [("ACERO", 1.0, "#98A2B3"), ("ALUMINIO", 0.4, "#C9CED6"), ("COBRE", 0.3, COBRE_V)]
        filas = VGroup()
        for k, (n, f, c) in enumerate(d):
            b = Rectangle(width=6.0 * f, height=0.6, stroke_width=0).set_fill(c, 1)
            t = T(n, 28, TINTA, "HEAVY")
            fila = VGroup(t, b).arrange(RIGHT, buff=0.3)
            fila.move_to([0, 2.2 - 1.3 * k, 0]).align_to([-3.8, 0, 0], LEFT)
            filas.add(fila)
        self.play(LaggedStart(*[FadeIn(f_, shift=RIGHT * 0.2) for f_ in filas], lag_ratio=0.3), run_time=1.0)
        nt = tag("distancia de detección (ejemplo, ver factor del fabricante)", GRIS_N, 24).move_to([0, -2.2, 0])
        self.play(FadeIn(nt), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(filas, nt)

        self.voz("p4")
        se = sensor_inductivo(1.6).move_to([1.0, 2.2, 0])
        self.play(FadeIn(se), run_time=0.4)
        hil = VGroup(card("CAFÉ  →  +24 V", [], "#8B5A2B", 7.6, 32), card("AZUL  →  0 V", [], AZUL_C, 7.6, 32), card("NEGRO  →  salida", [], NEGRO_BK, 7.6, 32)).arrange(DOWN, buff=0.25).move_to([0, -1.2, 0])
        for h in hil:
            self.play(FadeIn(h, shift=RIGHT * 0.2), run_time=0.35)
            self.frac(0.15)
        src = fuente("IEC 60947-5-2 · colores de conexión", [0, -4.6, 0], 22)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(se, hil, src)

        self.voz("p5")
        pnp = card("PNP", ["la salida entrega +24 V", "(fuente de corriente)"], ROJO_P, 7.6, 30).move_to([0, 2.0, 0])
        npn = card("NPN", ["la salida entrega 0 V", "(sumidero de corriente)"], AZUL_C, 7.6, 30).move_to([0, -0.4, 0])
        self.play(FadeIn(pnp), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(npn), run_time=0.4)
        pl = plc(1.4).move_to([0, -3.2, 0])
        self.frac(0.15)
        self.play(FadeIn(pl), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(pnp, npn, pl)

        self.voz("p6")
        se = sensor_inductivo(1.6).move_to([0, 1.6, 0])
        self.play(FadeIn(se), run_time=0.3)
        self.play(se.luz.animate.set_fill("#F5A524").scale(1.8), run_time=0.4)
        lb = tag("mira primero su LED", AMBAR, 36).move_to([0, -0.6, 0])
        self.play(FadeIn(lb), run_time=0.3)
        cap = card("CAPACITIVOS", ["detectan líquidos y plásticos"], MARCA, 7.6, 30).move_to([0, -2.8, 0])
        self.frac(0.4)
        self.play(FadeIn(cap), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(se, lb, cap)
        self.final("Inductivo: solo metales · PNP o NPN según tu PLC")


# ====================================================================== V28 · 120 V a 240 V
class V28D(ShortD):
    CLAVE = "v28"

    def cuerpo(self):
        self.voz("gancho")
        hn = horno(1.4).move_to([0, 1.6, 0])
        self.play(FadeIn(hn), run_time=0.4)
        x4 = VGroup(T("× 4", 140, ROJO_P, "HEAVY"), T("la potencia", 40, TINTA, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, -2.0, 0])
        self.frac(0.35)
        self.play(FadeIn(x4, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(hn, x4)

        self.voz("p1")
        f = VGroup(MathTex(r"R=\frac{V^2}{P}", color=TINTA).scale(1.8), MathTex(r"=\frac{120^2}{1000}=14{,}4\ \Omega", color=AMBAR).scale(1.4)).arrange(DOWN, buff=0.4).move_to([0, 1.4, 0])
        self.play(Write(f[0]), run_time=0.7)
        self.frac(0.3)
        self.play(Write(f[1]), run_time=0.8)
        self.cerrar_voz(0.15)
        self.limpiar(f)

        self.voz("p2")
        f = VGroup(MathTex(r"P=\frac{240^2}{14{,}4}", color=TINTA).scale(1.6), MathTex(r"=4000\ \text{W}", color=ROJO_P).scale(1.8), MathTex(r"I=16{,}7\ \text{A}", color=AMBAR).scale(1.5)).arrange(DOWN, buff=0.4).move_to([0, 1.2, 0])
        self.play(Write(f[0]), run_time=0.7)
        self.play(FadeIn(f[1], scale=1.2), run_time=0.4)
        self.frac(0.25)
        self.play(FadeIn(f[2]), run_time=0.3)
        bars = VGroup(Rectangle(width=1.0, height=0.6, stroke_width=0).set_fill(VERDE_OK, 1), Rectangle(width=1.0, height=2.4, stroke_width=0).set_fill(ROJO_P, 1)).arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to([0, -3.8, 0])
        self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(f, bars)

        self.voz("p3")
        res = onda(lambda x: np.sin(x * 8), -3.0, 3.0, 1.6, 0.4, COBRE_V, 10)
        self.play(Create(res), run_time=0.5)
        self.frac(0.1)
        self.play(res.animate.set_stroke("#FF6B3D"), run_time=0.6)
        self.sfx("pop", -8)
        hum = humo(np.array([0, 2.4, 0]), 5)
        self.play(FadeIn(hum, shift=UP * 0.3), res.animate.set_stroke("#3A2A20"), run_time=0.6)
        t = tag("se quema en segundos", ROJO_P, 40).move_to([0, -1.6, 0])
        self.play(FadeIn(t), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(res, hum, t)

        self.voz("p4")
        f = VGroup(T("240 V → 120 V", 56, TINTA, "HEAVY"), T("¼ de la potencia", 64, AMBAR, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0, 2.4, 0])
        self.play(FadeIn(f), run_time=0.4)
        c = VGroup(card("CALENTADOR", ["apenas calienta"], AMBAR, 7.6, 30), card("MOTOR", ["puede no arrancar y sobrecalentarse"], ROJO_P, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, -1.2, 0])
        self.frac(0.25)
        self.play(FadeIn(c[0]), run_time=0.4)
        self.frac(0.2)
        self.play(FadeIn(c[1]), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(f, c)

        self.voz("p5")
        et = RoundedRectangle(width=6.0, height=3.0, corner_radius=0.1, stroke_color="#98A2B3", stroke_width=2).set_fill("#F2F4F7", 1).move_to([0, 1.6, 0])
        tx_ = VGroup(T("INPUT: 100–240 V ~", 40, "#101828", "HEAVY"), T("50/60 Hz  1,5 A", 34, "#344054", "BOLD")).arrange(DOWN, buff=0.15).move_to(et)
        self.play(FadeIn(et), FadeIn(tx_), run_time=0.4)
        rc = SurroundingRectangle(tx_[0], color=VERDE_OK, buff=0.1, stroke_width=5)
        self.frac(0.2)
        self.play(Create(rc), run_time=0.4)
        ok = tag("funciona en los dos", VERDE_OK, 36).move_to([0, -1.2, 0])
        un = tag("un solo voltaje: respétalo", ROJO_P, 36).move_to([0, -2.6, 0])
        self.play(FadeIn(ok), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(un), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(et, tx_, rc, ok, un)

        self.voz("p6")
        a = VGroup(tomacorriente(np.array([0, 0, 0])).scale(1.4), T("NEMA 5-15 · 120 V", 26, TINTA, "BOLD")).arrange(DOWN, buff=0.3).move_to([-2.0, 1.4, 0])
        cara240 = VGroup(RoundedRectangle(width=1.8, height=2.4, corner_radius=0.2, stroke_color="#C7C5BE", stroke_width=2).set_fill("#F7F7F5", 1),
                         Rectangle(width=0.36, height=0.09, stroke_width=0).set_fill("#2B2F36", 1).shift(LEFT * 0.4 + UP * 0.3),
                         Rectangle(width=0.36, height=0.09, stroke_width=0).set_fill("#2B2F36", 1).shift(RIGHT * 0.4 + UP * 0.3),
                         Arc(radius=0.14, start_angle=0, angle=PI).set_stroke("#2B2F36", 5).shift(DOWN * 0.4))
        b = VGroup(cara240, T("NEMA 6-15 · 240 V", 26, TINTA, "BOLD")).arrange(DOWN, buff=0.3).move_to([2.0, 1.4, 0])
        self.play(FadeIn(a), FadeIn(b), run_time=0.5)
        nt = tag("otra forma: no se puede confundir", MARCA, 32).move_to([0, -1.6, 0])
        na = tag("no uses adaptadores para forzarla", ROJO_P, 32).move_to([0, -3.0, 0])
        self.frac(0.2)
        self.play(FadeIn(nt), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(na), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(a, b, nt, na)
        self.final("Doble voltaje = cuatro veces la potencia")


# ====================================================================== V29 · luces bajan
class V29D(ShortD):
    CLAVE = "v29"

    def foco(self, pos, k=1.0):
        f = foco_led(True).scale(1.6 * k).move_to(pos)
        return f

    def cuerpo(self):
        self.voz("gancho")
        fo = VGroup(*[foco_led(True).scale(1.5).move_to([x, 2.6, 0]) for x in (-2.4, 0, 2.4)])
        halo = VGroup(*[Circle(radius=0.9, stroke_width=0).set_fill("#FFE8A3", 0.25).move_to(f.get_top() + DOWN * 0.5) for f in fo])
        mi = horno(1.2).move_to([0, -1.4, 0])
        self.play(FadeIn(fo), FadeIn(halo), FadeIn(mi), run_time=0.5)
        self.frac(0.25)
        self.play(halo.animate.set_fill(opacity=0.06), run_time=0.25)
        self.play(halo.animate.set_fill(opacity=0.25), run_time=0.6)
        q = tag("¿cuándo preocuparte?", AMBAR, 38).move_to([0, -4.0, 0])
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(fo, halo, mi, q)

        self.voz("p1")
        tr = transformador().scale(1.2).move_to([-2.8, 2.4, 0])
        cab = Line([-2.0, 2.0, 0], [3.0, 2.0, 0]).set_stroke(COBRE_V, 14)
        rs = VGroup(*[onda(lambda x: 0.25 * np.sign(np.sin(x * 12)), x0, x0 + 0.9, 2.0, 1, AMBAR, 5) for x0 in (-1.0, 1.0)])
        self.play(FadeIn(tr), Create(cab), run_time=0.5)
        self.play(FadeIn(rs), run_time=0.3)
        f = VGroup(T("V = I · R", 90, AMBAR, "HEAVY"), T("caída de tensión", 40, TINTA, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, -1.2, 0])
        self.frac(0.35)
        self.play(Write(f[0]), FadeIn(f[1]), run_time=0.7)
        self.cerrar_voz(0.15)
        self.limpiar(tr, cab, rs, f)

        self.voz("p2")
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 8, 2], x_length=7.4, y_length=4.4, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.2, 0])
        c = ax.plot(lambda t: 1 + 5.6 * np.exp(-((t - 0.25) ** 2) / 0.05) if t > 0.05 else 0, x_range=[0, 3, 0.01], color=ROJO_P, stroke_width=6)
        self.play(Create(ax), run_time=0.3)
        self.play(Create(c), run_time=1.2)
        lb = VGroup(T("arranque: 5–8 × In", 34, ROJO_P, "HEAVY").move_to(ax.c2p(1.6, 6.2)), T("nominal", 30, VERDE_OK, "HEAVY").move_to(ax.c2p(2.4, 1.8)))
        self.play(FadeIn(lb), run_time=0.3)
        mo = card("MOTOR DE 5 hp", ["más de 6 × su corriente"], AMBAR, 7.6, 30).move_to([0, -2.6, 0])
        self.frac(0.3)
        self.play(FadeIn(mo), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ax, c, lb, mo)

        self.voz("p3")
        ax = Axes(x_range=[0, 3, 1], y_range=[100, 125, 5], x_length=7.4, y_length=3.6, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.4, 0])
        v = ax.plot(lambda t: 120 - 12 * np.exp(-((t - 0.3) ** 2) / 0.04), x_range=[0, 3, 0.01], color=CIAN, stroke_width=6)
        self.play(Create(ax), run_time=0.3)
        self.play(Create(v), run_time=1.4)
        lb = T("el voltaje baja un instante", 34, CIAN, "HEAVY").move_to([0, -1.1, 0])
        self.play(FadeIn(lb), run_time=0.3)
        rec = tag("el motor acelera → la luz vuelve", VERDE_OK, 34).move_to([0, -2.6, 0])
        self.frac(0.45)
        self.play(FadeIn(rec), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ax, v, lb, rec)

        self.voz("p4")
        ok = card("PARPADEO LEVE", ["normal al arrancar un motor"], VERDE_OK, 7.6, 30).move_to([0, 3.0, 0])
        self.play(FadeIn(ok, shift=RIGHT * 0.2), run_time=0.4)
        fo = VGroup(foco_led(True).scale(1.3).move_to([-1.6, 0.0, 0]), foco_led(True).scale(1.3).move_to([1.6, 0.0, 0]))
        h1 = Circle(radius=0.8, stroke_width=0).set_fill("#FFE8A3", 0.25).move_to(fo[0].get_top() + DOWN * 0.45)
        h2 = h1.copy().move_to(fo[1].get_top() + DOWN * 0.45)
        self.frac(0.2)
        self.play(FadeIn(fo), FadeIn(h1), FadeIn(h2), run_time=0.4)
        self.play(h1.animate.scale(1.6).set_fill(opacity=0.45), h2.animate.scale(0.5).set_fill(opacity=0.06), run_time=0.6)
        nf = card("NEUTRO FLOJO", ["unas suben y otras bajan: PELIGRO"], ROJO_P, 7.6, 30).move_to([0, -3.0, 0])
        self.play(FadeIn(nf, shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ok, fo, h1, h2, nf)

        self.voz("p5")
        tab = RoundedRectangle(width=3.4, height=4.6, corner_radius=0.12, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1).move_to([0, 1.8, 0])
        brs = VGroup(*[br_din(0.42) for _ in range(3)]).arrange(RIGHT, buff=0.08).move_to(tab)
        self.play(FadeIn(tab), FadeIn(brs), run_time=0.4)
        a = VGroup(tag("apaga lo sensible", AMBAR, 34), tag("llama a un electricista", MARCA, 34)).arrange(DOWN, buff=0.3).move_to([0, -2.6, 0])
        self.frac(0.1)
        self.play(FadeIn(a[0]), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(a[1]), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(tab, brs, a)

        self.voz("p6")
        b = VGroup(card("3 %", ["en un circuito"], AMBAR, 7.6, 34), card("5 %", ["total: acometida → último aparato"], ROJO_P, 7.6, 34)).arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        self.frac(0.25)
        self.play(FadeIn(b[0], shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.15)
        self.play(FadeIn(b[1], shift=RIGHT * 0.2), run_time=0.4)
        src = fuente("NEC 2020 · 210.19(A)(1) Nota informativa 4 (recomendación)", [0, -2.0, 0])
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(b, src)
        self.final("Parpadeo leve: normal · Luces dispares: neutro flojo")


# ====================================================================== V30 · kWh
class V30D(ShortD):
    CLAVE = "v30"

    def cuerpo(self):
        self.voz("gancho")
        rec = RoundedRectangle(width=5.6, height=6.4, corner_radius=0.15, stroke_color="#C7CCD6", stroke_width=2).set_fill(WHITE, 1).move_to([0, 0.4, 0])
        li = VGroup(*[Rectangle(width=4.4 if k % 2 else 3.2, height=0.12, stroke_width=0).set_fill("#D0D5DD", 1) for k in range(6)]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, 1.2, 0])
        kw = T("185 kWh", 64, "#101828", "HEAVY").move_to([0, -1.6, 0])
        self.play(FadeIn(rec), FadeIn(li), run_time=0.4)
        self.frac(0.25)
        self.play(FadeIn(kw, scale=1.2), run_time=0.4)
        self.play(Indicate(kw, color=AMBAR), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(rec, li, kw)

        self.voz("p1")
        a = card("VATIO (W)", ["potencia: qué tan rápido usa energía"], MARCA, 7.6, 30).move_to([0, 3.0, 0])
        b = card("KILOVATIO HORA (kWh)", ["energía = potencia × tiempo"], AMBAR, 7.6, 30).move_to([0, 0.9, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.25)
        self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.4)
        f = T("1000 W × 1 h = 1 kWh", 54, TINTA, "HEAVY").move_to([0, -1.6, 0])
        self.frac(0.4)
        self.play(Write(f), run_time=0.7)
        self.cerrar_voz(0.15)
        self.limpiar(a, b, f)

        self.voz("p2")
        r1 = VGroup(T("PLANCHA", 36, AMBAR, "HEAVY"), T("1,2 kW × 0,5 h = 0,6 kWh", 44, TINTA, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, 2.6, 0])
        r2 = VGroup(T("TELEVISOR", 36, CIAN, "HEAVY"), T("0,1 kW × 5 h × 30 d", 44, TINTA, "HEAVY"), T("= 15 kWh / mes", 60, CIAN, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, -0.8, 0])
        self.play(FadeIn(r1), run_time=0.5)
        self.frac(0.35)
        self.play(FadeIn(r2[:2]), run_time=0.5)
        self.frac(0.6)
        self.play(FadeIn(r2[2], scale=1.2), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(r1, r2)

        self.voz("p3")
        ax = Axes(x_range=[0, 24, 6], y_range=[0, 1, 1], x_length=7.4, y_length=2.4, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.8, 0])
        ciclo = ax.plot(lambda t: 0.8 if (t % 2) < 0.9 else 0.05, x_range=[0, 24, 0.02], color=CIAN, stroke_width=4, use_smoothing=False)
        self.play(Create(ax), run_time=0.3)
        self.play(Create(ciclo), run_time=1.6)
        l = VGroup(T("0 h", 26, GRIS_N, "BOLD").next_to(ax.c2p(0, 0), DOWN, buff=0.1), T("24 h", 26, GRIS_N, "BOLD").next_to(ax.c2p(24, 0), DOWN, buff=0.1))
        rf = tag("refrigeradora: todo el día", CIAN, 36).move_to([0, -0.9, 0])
        self.play(FadeIn(l), FadeIn(rf), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ax, ciclo, l, rf)

        self.voz("p4")
        du = ducha().scale(1.2).move_to([-1.8, 1.6, 0])
        ll = llama(1.0).move_to([2.0, 1.4, 0])
        self.play(FadeIn(du), FadeIn(ll), run_time=0.4)
        c = card("CALOR = MUCHA ENERGÍA", ["ducha, plancha, calentador"], ROJO_P, 7.6, 30).move_to([0, -2.0, 0])
        self.frac(0.2)
        self.play(FadeIn(c), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(du, ll, c)

        self.voz("p5")
        f = VGroup(T("kWh × tarifa", 70, AMBAR, "HEAVY"), T("= lo que pagas", 50, TINTA, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0, 2.0, 0])
        self.play(Write(f[0]), run_time=0.6)
        self.play(FadeIn(f[1]), run_time=0.3)
        ej = card("EJEMPLO (tarifa ilustrativa)", ["15 kWh × Q2,00 = Q30 al mes"], MARCA, 7.6, 30).move_to([0, -1.2, 0])
        self.frac(0.3)
        self.play(FadeIn(ej), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(f, ej)

        self.voz("p6")
        de = VGroup(RoundedRectangle(width=3.0, height=0.8, corner_radius=0.1, stroke_width=0).set_fill("#1F2430", 1), Dot(radius=0.09, color=ROJO_P).shift(RIGHT * 1.1)).move_to([0, 3.0, 0])
        self.play(FadeIn(de), run_time=0.3)
        f = VGroup(T("5 W × 24 h × 30 d", 50, TINTA, "HEAVY"), T("= 3,6 kWh", 70, AMBAR, "HEAVY")).arrange(DOWN, buff=0.2).move_to([0, 0.8, 0])
        self.frac(0.1)
        self.play(Write(f[0]), run_time=0.6)
        self.play(FadeIn(f[1], scale=1.2), run_time=0.3)
        md = card("MEDIDOR ENCHUFABLE", ["mide cuánto gasta cada aparato"], MARCA, 7.6, 30).move_to([0, -2.4, 0])
        self.frac(0.45)
        self.play(FadeIn(md), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(de, f, md)
        self.final("kWh = potencia × tiempo")


# ====================================================================== V31 · variador
class V31D(ShortD):
    CLAVE = "v31"

    def bloques(self):
        cols = [("RECTIFICADOR", "CA → CC", AMBAR), ("BUS DE CC", "capacitores", MARCA), ("INVERSOR IGBT", "CC → CA variable", ROJO_P)]
        g = VGroup()
        for t, s, c in cols:
            g.add(card(t, [s], c, 7.6, 30))
        return g.arrange(DOWN, buff=0.35).move_to([0, 0.4, 0])

    def cuerpo(self):
        self.voz("gancho")
        vfd = VGroup(RoundedRectangle(width=3.0, height=4.4, corner_radius=0.15, stroke_color="#98A2B3", stroke_width=3).set_fill("#E4E7EC", 1),
                     RoundedRectangle(width=2.0, height=0.9, corner_radius=0.08, stroke_width=0).set_fill("#101828", 1).shift(UP * 1.2),
                     T("45.0 Hz", 34, "#4ADE80", "HEAVY").shift(UP * 1.2),
                     *[Circle(radius=0.18, stroke_width=0).set_fill(c, 1).shift(RIGHT * x + DOWN * 0.1) for x, c in ((-0.6, "#98A2B3"), (0, "#98A2B3"), (0.6, "#98A2B3"))],
                     Circle(radius=0.4, stroke_color="#475467", stroke_width=4).set_fill("#C9CED6", 1).shift(DOWN * 1.1)).move_to([-1.9, 1.4, 0])
        mo = motor_3f(0.9).move_to([2.2, 1.4, 0])
        self.play(FadeIn(vfd), FadeIn(mo), run_time=0.5)
        q = tag("¿cómo cambia la velocidad?", AMBAR, 36).move_to([0, -2.2, 0])
        self.frac(0.4)
        self.play(FadeIn(q), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(vfd, mo, q)

        self.voz("p1")
        f = MathTex(r"n_s=\frac{120\,f}{p}", color=TINTA).scale(2.0).move_to([0, 2.8, 0])
        self.play(Write(f), run_time=0.7)
        r = VGroup(T("60 Hz → 1800 rpm", 50, TINTA, "HEAVY"), T("30 Hz → 900 rpm", 50, AMBAR, "HEAVY")).arrange(DOWN, buff=0.3).move_to([0, 0.0, 0])
        self.frac(0.2)
        self.play(FadeIn(r[0]), run_time=0.3)
        self.frac(0.4)
        self.play(FadeIn(r[1], scale=1.1), run_time=0.3)
        p4 = tag("motor de 4 polos", MARCA, 30).move_to([0, -2.0, 0])
        self.play(FadeIn(p4), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(f, r, p4)

        self.voz("p2")
        bl = self.bloques()
        self.frac(0.1)
        self.play(FadeIn(bl[0], shift=RIGHT * 0.2), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(bl[1], shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)

        self.voz("p3")
        self.play(FadeIn(bl[2], shift=RIGHT * 0.2), run_time=0.4)
        self.play(bl.animate.scale(0.7).move_to([0, 2.6, 0]), run_time=0.5)
        pw = VMobject()
        pts = []
        for k in range(24):
            w = 0.5 * (1 + np.sin(2 * np.pi * k / 24))
            x = -3.6 + 0.3 * k
            pts += [[x, -1.6, 0], [x, -0.6, 0], [x + 0.3 * w, -0.6, 0], [x + 0.3 * w, -1.6, 0]]
        pw.set_points_as_corners(pts).set_stroke(GRIS_N, 3)
        sn = onda(lambda x: 0.6 * np.sin(2 * np.pi * (x + 3.6) / 7.2), -3.6, 3.6, -1.1, 1, ROJO_P, 5)
        self.play(Create(pw), run_time=1.2)
        self.play(Create(sn), run_time=0.6)
        vf = tag("baja V junto con f (V/f)", MARCA, 32).move_to([0, -3.2, 0])
        self.frac(0.5)
        self.play(FadeIn(vf), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(bl, pw, sn, vf)

        self.voz("p4")
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2], x_length=6.4, y_length=4.4, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.4, 0])
        c = ax.plot(lambda t: t ** 3, x_range=[0, 1], color=AMBAR, stroke_width=6)
        self.play(Create(ax), Create(c), run_time=1.0)
        d = Dot(ax.c2p(0.8, 0.512), radius=0.12, color=ROJO_P)
        gl = VGroup(DashedLine(ax.c2p(0.8, 0), ax.c2p(0.8, 0.512)).set_stroke(ROJO_P, 3), DashedLine(ax.c2p(0, 0.512), ax.c2p(0.8, 0.512)).set_stroke(ROJO_P, 3))
        self.frac(0.3)
        self.play(FadeIn(d), Create(gl), run_time=0.5)
        r = VGroup(T("80 % velocidad", 40, TINTA, "HEAVY"), T("≈ 51 % potencia", 56, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.15).move_to([0, -2.2, 0])
        self.play(FadeIn(r), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(ax, c, d, gl, r)

        self.voz("p5")
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 7, 1], x_length=7.4, y_length=4.0, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 1.4, 0])
        di = ax.plot(lambda t: 1 + 5.4 * np.exp(-((t - 0.3) ** 2) / 0.06) if t > 0.05 else 0, x_range=[0, 3, 0.01], color=ROJO_P, stroke_width=5)
        su = ax.plot(lambda t: min(1.3, t * 1.3), x_range=[0, 3, 0.01], color=VERDE_OK, stroke_width=6)
        self.play(Create(ax), Create(di), run_time=0.8)
        self.play(Create(su), run_time=0.8)
        lb = VGroup(tag("directo", ROJO_P, 30), tag("con variador", VERDE_OK, 30)).arrange(RIGHT, buff=0.3).move_to([0, -1.4, 0])
        self.play(FadeIn(lb), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ax, di, su, lb)

        self.voz("p6")
        it = VGroup(card("RUIDO ELÉCTRICO", ["cable apantallado + buena tierra"], AMBAR, 7.6, 30), card("BAJA VELOCIDAD", ["el ventilador del motor enfría poco"], ROJO_P, 7.6, 30),
                    card("PROTECCIÓN", ["según el manual del fabricante"], MARCA, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 0.6, 0])
        for t_ in it:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.4)
            self.frac(0.22)
        self.cerrar_voz(0.15)
        self.limpiar(it)
        self.final("Variador: cambia la frecuencia, cambia la velocidad")


# ====================================================================== V32 · estrella / triángulo
class V32D(ShortD):
    CLAVE = "v32"

    def puentes(self, bo, tipo):
        b = bo.b
        c = lambda n: b[n][0].get_center()
        if tipo == "Y":
            return VGroup(puente(c("W2"), c("U2")), puente(c("U2"), c("V2")))
        return VGroup(puente(c("W2"), c("U1")), puente(c("U2"), c("V1")), puente(c("V2"), c("W1")))

    def sim(self, tipo, c, r=1.2, col=AMBAR):
        c = np.array(c)
        if tipo == "Y":
            pts = [c + r * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 - 2 * PI / 3)]
            return VGroup(*[Line(c, p).set_stroke(col, 8) for p in pts], Dot(c, radius=0.1, color=col))
        pts = [c + r * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 - 2 * PI / 3)]
        return Polygon(*pts).set_stroke(col, 8)

    def cuerpo(self):
        self.voz("gancho")
        bo = bornera_motor(1.4).move_to([0, 1.6, 0])
        self.play(FadeIn(bo), run_time=0.5)
        q = VGroup(tag("6 bornes", MARCA, 38), tag("3 fases", AMBAR, 38)).arrange(RIGHT, buff=0.4).move_to([0, -1.4, 0])
        self.frac(0.2)
        self.play(FadeIn(q), run_time=0.4)
        yd = VGroup(self.sim("Y", [-1.6, -3.6, 0], 0.8), self.sim("D", [1.6, -3.6, 0], 0.9, CIAN))
        self.frac(0.4)
        self.play(Create(yd), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(bo, q, yd)

        self.voz("p1")
        bo = bornera_motor(1.5).move_to([0, 1.4, 0])
        self.play(FadeIn(bo), run_time=0.4)
        dev = VGroup(*[VGroup(Line(bo.b[a][0].get_center(), bo.b[b][0].get_center()).set_stroke(c, 5, 0.8)) for a, b, c in (("U1", "U2", ROJO_P), ("V1", "V2", AMBAR), ("W1", "W2", AZUL_C))])
        self.frac(0.15)
        self.play(LaggedStart(*[Create(d) for d in dev], lag_ratio=0.3), run_time=1.2)
        l = tag("cada devanado: dos extremos", MARCA, 34).move_to([0, -1.6, 0])
        self.play(FadeIn(l), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(bo, dev, l)

        self.voz("p2")
        y = self.sim("Y", [-2.0, 2.2, 0], 1.3)
        d = self.sim("D", [2.0, 2.0, 0], 1.5, CIAN)
        ly = VGroup(T("ESTRELLA", 34, AMBAR, "HEAVY"), T("V ÷ √3", 44, TINTA, "HEAVY")).arrange(DOWN, buff=0.15).move_to([-2.0, -0.2, 0])
        ld = VGroup(T("TRIÁNGULO", 34, CIAN, "HEAVY"), T("V completo", 44, TINTA, "HEAVY")).arrange(DOWN, buff=0.15).move_to([2.0, -0.2, 0])
        self.play(Create(y), run_time=0.6)
        self.play(FadeIn(ly), run_time=0.3)
        self.frac(0.5)
        self.play(Create(d), FadeIn(ld), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(y, d, ly, ld)

        self.voz("p3")
        pl = placa_motor([("V", "230 Δ / 400 Y", True), ("A", "19,6 / 11,3", False), ("kW", "5,5", False), ("Hz", "50", False)], 1.6, "MOTOR 3~")
        pl.move_to([0, 2.0, 0])
        pl.scale_to_fit_width(7.8)
        self.play(FadeIn(pl), run_time=0.5)
        r = VGroup(card("230 V → TRIÁNGULO", [], CIAN, 7.6, 32), card("400 V → ESTRELLA", [], AMBAR, 7.6, 32)).arrange(DOWN, buff=0.25).move_to([0, -2.4, 0])
        self.frac(0.2)
        self.play(FadeIn(r[0], shift=RIGHT * 0.2), run_time=0.4)
        self.play(FadeIn(r[1], shift=RIGHT * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(pl, r)

        self.voz("p4")
        a = VGroup(self.sim("Y", [0, 0, 0], 1.1), T("arranque", 30, AMBAR, "HEAVY").shift(DOWN * 1.5)).move_to([-2.0, 2.2, 0])
        b = VGroup(self.sim("D", [0, 0, 0], 1.2, CIAN), T("marcha", 30, CIAN, "HEAVY").shift(DOWN * 1.5)).move_to([2.0, 2.2, 0])
        ar = Arrow([-0.7, 2.4, 0], [0.7, 2.4, 0], buff=0, color=TINTA, stroke_width=8)
        self.play(FadeIn(a), run_time=0.4)
        self.play(GrowArrow(ar), FadeIn(b), run_time=0.5)
        f = VGroup(T("I y par ≈ ⅓", 80, VERDE_OK, "HEAVY")).move_to([0, -1.4, 0])
        self.frac(0.4)
        self.play(FadeIn(f, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(a, b, ar, f)

        self.voz("p5")
        d = self.sim("D", [0, 2.0, 0], 1.6, ROJO_P)
        self.play(Create(d), run_time=0.5)
        f = VGroup(T("√3 × más voltaje", 54, ROJO_P, "HEAVY")).move_to([0, -0.4, 0])
        self.frac(0.3)
        self.play(FadeIn(f), run_time=0.3)
        hu = humo(np.array([0, 3.0, 0]), 4)
        self.play(FadeIn(hu, shift=UP * 0.3), run_time=0.5)
        r = tag("revisa la placa y los puentes", MARCA, 34).move_to([0, -2.2, 0])
        self.play(FadeIn(r), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(d, f, hu, r)

        self.voz("p6")
        b1 = bornera_motor(1.1).move_to([0, 1.5, 0])
        b2 = bornera_motor(1.1).move_to([0, -3.0, 0])
        t1 = tag("ESTRELLA", AMBAR, 30).next_to(b1, UP, buff=0.15)
        t2 = tag("TRIÁNGULO", CIAN, 30).next_to(b2, UP, buff=0.15)
        self.play(FadeIn(b1), FadeIn(t1), run_time=0.4)
        self.frac(0.1)
        p1 = self.puentes(b1, "Y")
        self.play(FadeIn(p1, shift=DOWN * 0.2), run_time=0.5)
        self.frac(0.5)
        self.play(FadeIn(b2), FadeIn(t2), run_time=0.4)
        p2 = self.puentes(b2, "D")
        self.play(FadeIn(p2, shift=DOWN * 0.2), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(b1, b2, t1, t2, p1, p2)
        self.final("Voltaje menor: triángulo · Mayor: estrella")


# ====================================================================== V33 · IP65
class V33D(ShortD):
    CLAVE = "v33"

    def codigo(self, a, b, s=150):
        g = VGroup(T("IP", s, TINTA, "HEAVY"), T(a, s, AMBAR, "HEAVY"), T(b, s, CIAN, "HEAVY")).arrange(RIGHT, buff=0.15)
        return g

    def cuerpo(self):
        self.voz("gancho")
        cj = VGroup(RoundedRectangle(width=4.2, height=4.2, corner_radius=0.25, stroke_color="#98A2B3", stroke_width=3).set_fill("#E4E7EC", 1),
                    *[tornillo_frente(0.14).move_to([x, y, 0]) for x in (-1.7, 1.7) for y in (-1.7, 1.7)],
                    T("IP65", 54, "#101828", "HEAVY")).move_to([0, 2.0, 0])
        self.play(FadeIn(cj), run_time=0.5)
        no = tag("no es un modelo", ROJO_P, 36).move_to([0, -1.2, 0])
        n = tag("IEC 60529", MARCA, 38).move_to([0, -2.6, 0])
        self.frac(0.25)
        self.play(FadeIn(no), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(n), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cj, no, n)

        self.voz("p1")
        c = self.codigo("6", "5").move_to([0, 3.0, 0])
        self.play(FadeIn(c), run_time=0.4)
        self.play(c[2].animate.set_opacity(0.2), Indicate(c[1], color=AMBAR), run_time=0.6)
        caja = RoundedRectangle(width=3.0, height=2.4, corner_radius=0.2, stroke_color="#98A2B3", stroke_width=3).set_fill("#E4E7EC", 1).move_to([0, -0.4, 0])
        polvo = VGroup(*[Dot(radius=0.04, color="#D9C38A").move_to([np.random.uniform(-3.8, 3.8), np.random.uniform(-2.4, 1.6), 0]) for _ in range(120)])
        polvo = VGroup(*[d for d in polvo if not (abs(d.get_x()) < 1.6 and abs(d.get_y() + 0.4) < 1.3)])
        self.play(FadeIn(caja), FadeIn(polvo), run_time=0.6)
        l = card("6 = HERMÉTICO AL POLVO", ["cámara de polvo con vacío"], AMBAR, 7.6, 30).move_to([0, -3.4, 0])
        self.play(FadeIn(l), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(c, caja, polvo, l)

        self.voz("p2")
        c = self.codigo("6", "5").move_to([0, 3.0, 0])
        c[1].set_opacity(0.2)
        self.play(FadeIn(c), run_time=0.3)
        self.play(Indicate(c[2], color=CIAN), run_time=0.5)
        bq = VGroup(Rectangle(width=0.9, height=0.4, stroke_width=0).set_fill("#98A2B3", 1), Triangle().scale(0.25).rotate(-PI / 2).set_fill("#98A2B3", 1).set_stroke(width=0).shift(RIGHT * 0.55)).move_to([-3.2, 0.2, 0])
        ch = VGroup(*[Line([-2.6, 0.2 + dy, 0], [1.6, -0.2 + dy * 3, 0]).set_stroke("#7FD1FF", 5, 0.8) for dy in (-0.08, 0, 0.08)])
        cj = RoundedRectangle(width=1.8, height=2.0, corner_radius=0.15, stroke_color="#98A2B3", stroke_width=3).set_fill("#E4E7EC", 1).move_to([2.6, -0.2, 0])
        self.play(FadeIn(bq), FadeIn(cj), run_time=0.3)
        self.play(Create(ch), run_time=0.6)
        d = VGroup(tag("12,5 L/min", CIAN, 32), tag("boquilla 6,3 mm", CIAN, 32), tag("a 3 m", CIAN, 32)).arrange(DOWN, buff=0.2).move_to([0, -3.0, 0])
        self.frac(0.3)
        self.play(LaggedStart(*[FadeIn(x) for x in d], lag_ratio=0.3), run_time=0.9)
        self.cerrar_voz(0.15)
        self.limpiar(c, bq, ch, cj, d)

        self.voz("p3")
        agua = Rectangle(width=7.6, height=5.0, stroke_width=0).set_fill("#2F6FD0", 0.35).move_to([0, 0.0, 0])
        sup = Line([-3.8, 2.5, 0], [3.8, 2.5, 0]).set_stroke("#7FD1FF", 4)
        cj = RoundedRectangle(width=1.6, height=1.6, corner_radius=0.15, stroke_color="#98A2B3", stroke_width=3).set_fill("#E4E7EC", 1).move_to([0, -1.2, 0])
        m = VGroup(DoubleArrow([2.4, 2.5, 0], [2.4, -0.4, 0], buff=0, color=TINTA, stroke_width=4), T("1 m", 34, TINTA, "HEAVY").move_to([3.2, 1.0, 0]))
        c = VGroup(T("IP67", 80, CIAN, "HEAVY")).move_to([0, 3.6, 0])
        self.play(FadeIn(c), FadeIn(agua), Create(sup), FadeIn(cj), run_time=0.5)
        self.play(FadeIn(m), run_time=0.3)
        t30 = tag("30 minutos", MARCA, 34).move_to([0, -3.2, 0])
        self.play(FadeIn(t30), run_time=0.3)
        oj = tag("inmersión ≠ chorros", ROJO_P, 36).move_to([0, -4.6, 0])
        self.frac(0.35)
        self.play(FadeIn(oj), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(agua, sup, cj, m, c, t30, oj)

        self.voz("p4")
        c = self.codigo("X", "5").move_to([0, 2.4, 0])
        self.play(FadeIn(c), run_time=0.4)
        self.play(Indicate(c[1], color=AMBAR), run_time=0.5)
        l = tag("X = no se ensayó", AMBAR, 40).move_to([0, -0.6, 0])
        self.play(FadeIn(l), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(c, l)

        self.voz("p5")
        lluv = VGroup(*[Line([x, y, 0], [x - 0.15, y - 0.5, 0]).set_stroke("#7FD1FF", 3, 0.7) for x in np.linspace(-3.6, 3.6, 12) for y in (4.0, 3.0)])
        cj = VGroup(RoundedRectangle(width=3.0, height=2.6, corner_radius=0.2, stroke_color="#98A2B3", stroke_width=3).set_fill("#E4E7EC", 1), T("IP65", 40, "#101828", "HEAVY")).move_to([0, 0.6, 0])
        pr = VGroup(Rectangle(width=0.6, height=0.4, stroke_width=0).set_fill("#344054", 1), Line(DOWN * 0.2, DOWN * 1.4).set_stroke(NEGRO_BK, 10)).next_to(cj, DOWN, buff=0)
        self.play(FadeIn(lluv), FadeIn(cj), run_time=0.4)
        self.frac(0.25)
        self.play(FadeIn(pr), run_time=0.3)
        r = tag("prensaestopas y empaque: mantén el grado", MARCA, 30).move_to([0, -3.4, 0])
        self.play(FadeIn(r), Indicate(pr[0], color=AMBAR), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(lluv, cj, pr, r)

        self.voz("p6")
        ej = VGroup(card("IP20", ["interiores: no se meten los dedos"], GRIS_N, 7.6, 30), card("IP44", ["resiste salpicaduras"], AMBAR, 7.6, 30),
                    card("IP65 / IP66", ["exteriores y lavado a presión"], CIAN, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 0.6, 0])
        for t_ in ej:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.4)
            self.frac(0.22)
        self.cerrar_voz(0.15)
        self.limpiar(ej)
        self.final("1.ª cifra: polvo · 2.ª cifra: agua")


# ====================================================================== V34 · paro de emergencia
class V34D(ShortD):
    CLAVE = "v34"

    def cuerpo(self):
        self.voz("gancho")
        e = hongo_emergencia(1.5).move_to([0, 1.4, 0])
        self.play(FadeIn(e, scale=0.8), run_time=0.5)
        r = tag("reglas muy estrictas", ROJO_P, 38).move_to([0, -2.4, 0])
        self.frac(0.5)
        self.play(FadeIn(r), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(e, r)

        self.voz("p1")
        n = VGroup(tag("ISO 13850", MARCA, 34), tag("IEC 60204-1", MARCA, 34)).arrange(RIGHT, buff=0.3).move_to([0, 3.6, 0])
        e = hongo_emergencia(1.3).move_to([0, 0.6, 0])
        self.play(FadeIn(n), run_time=0.3)
        self.play(FadeIn(e), run_time=0.4)
        mano = VGroup(RoundedRectangle(width=1.8, height=1.0, corner_radius=0.4, stroke_width=0).set_fill(PIEL, 1)).move_to([0, 3.0, 0])
        self.frac(0.45)
        self.play(FadeIn(mano), run_time=0.2)
        self.play(mano.animate.move_to(e.hongo.get_center() + UP * 0.7), e.hongo.animate.scale(0.92), run_time=0.3)
        c = card("ROJO SOBRE AMARILLO", ["hongo: se golpea con la palma"], ROJO_P, 7.6, 30).move_to([0, -3.0, 0])
        self.play(FadeIn(c), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(n, e, mano, c)

        self.voz("p2")
        e = hongo_emergencia(1.4).move_to([0, 1.6, 0])
        self.play(FadeIn(e), run_time=0.3)
        self.play(e.hongo.animate.scale(0.9), run_time=0.2)
        lk = tag("ENCLAVADO", ROJO_P, 40).move_to([0, -1.4, 0])
        self.play(FadeIn(lk), run_time=0.3)
        g = Arc(radius=1.4, start_angle=PI / 4, angle=-PI / 2, color=AMBAR, stroke_width=7).move_arc_center_to(e.get_center()).add_tip()
        self.frac(0.35)
        self.play(Create(g), Rotate(e.hongo, -PI / 4), run_time=0.6)
        d = tag("girar para soltar: acción deliberada", AMBAR, 32).move_to([0, -2.8, 0])
        self.play(FadeIn(d), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(e, lk, g, d)

        self.voz("p3")
        cs = contacto(no=False, n1="11", n2="12").scale_to_fit_height(2.6).move_to([0, 1.4, 0])
        fl = SVGMobject if False else None
        sim = T("⊖", 1, TINTA)
        self.play(FadeIn(cs), run_time=0.4)
        emp = Arrow([0, 4.0, 0], [0, 2.6, 0], buff=0, color=ROJO_P, stroke_width=10)
        self.frac(0.25)
        self.play(GrowArrow(emp), run_time=0.4)
        c = card("APERTURA DIRECTA", ["el empuje separa los contactos", "aunque estén soldados"], VERDE_OK, 7.6, 30).move_to([0, -1.8, 0])
        self.play(FadeIn(c), run_time=0.4)
        src = fuente("IEC 60947-5-1, Anexo K (apertura directa)", [0, -4.0, 0])
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(cs, emp, c, src)

        self.voz("p4")
        e = hongo_emergencia(0.9).move_to([-2.0, 2.0, 0])
        m = pulsador_fis("#16A34A", "I", 1.3).move_to([2.0, 2.0, 0])
        self.play(FadeIn(e), FadeIn(m), run_time=0.4)
        a = card("SOLTAR EL HONGO", ["NO arranca la máquina"], ROJO_P, 7.6, 30).move_to([0, -0.8, 0])
        b = card("PULSAR MARCHA", ["arranque intencional"], VERDE_OK, 7.6, 30).move_to([0, -2.8, 0])
        self.frac(0.1)
        self.play(FadeIn(a), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(b), Indicate(m), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(e, m, a, b)

        self.voz("p5")
        it = VGroup(card("MEDIDA COMPLEMENTARIA", [], AMBAR, 7.6, 32), card("NO REEMPLAZA GUARDAS", [], ROJO_P, 7.6, 32), card("NI EL BLOQUEO (LOTO)", [], ROJO_P, 7.6, 32)).arrange(DOWN, buff=0.3).move_to([0, 1.8, 0])
        for t_ in it:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.35)
            self.frac(0.2)
        self.cerrar_voz(0.15)
        self.limpiar(it)

        self.voz("p6")
        xr = -2.2
        es = contacto(no=False, color=ROJO_P).scale_to_fit_height(1.1).move_to([xr, 3.3, 0])
        pa = contacto(no=False).scale_to_fit_height(1.1).move_to([xr, 1.8, 0])
        ma = contacto(no=True).scale_to_fit_height(1.1).move_to([xr, 0.3, 0])
        bo = bobina_sim("KM1").scale_to_fit_height(0.9).move_to([xr, -1.1, 0])
        ys = [4.3] + [v for m in (es, pa, ma, bo) for v in (m.get_top()[1], m.get_bottom()[1])] + [-1.9]
        l1 = VGroup(*[Line([xr, ys[k], 0], [xr, ys[k + 1], 0]) for k in range(0, len(ys), 2)]).set_stroke(TINTA, 4)
        lb = VGroup(T("PARO DE EMERGENCIA", 28, ROJO_P, "HEAVY").next_to(es, RIGHT, buff=0.5), T("PARO", 28, TINTA, "BOLD").next_to(pa, RIGHT, buff=0.5),
                    T("MARCHA", 28, TINTA, "BOLD").next_to(ma, RIGHT, buff=0.5), T("BOBINA KM1", 28, TINTA, "BOLD").next_to(bo, RIGHT, buff=0.5))
        self.play(Create(l1), run_time=0.3)
        self.play(FadeIn(es), FadeIn(pa), FadeIn(ma), FadeIn(bo), FadeIn(lb), run_time=0.6)
        sr = tag("en serie con todo el mando", MARCA, 32).move_to([0, -2.6, 0])
        self.play(FadeIn(sr), run_time=0.3)
        cats = VGroup(card("CATEGORÍA 0", ["corte inmediato de energía"], ROJO_P, 7.6, 28), card("CATEGORÍA 1", ["parada controlada y luego corte"], AMBAR, 7.6, 28)).arrange(DOWN, buff=0.25).move_to([0, -4.6, 0])
        self.frac(0.35)
        self.play(FadeIn(cats[0]), run_time=0.4)
        self.play(FadeIn(cats[1]), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(l1, es, pa, ma, bo, lb, sr, cats)
        self.final("Rojo/amarillo · enclavado · apertura directa")


# ====================================================================== V35 · LED apagado
class V35D(ShortD):
    CLAVE = "v35"

    def cuerpo(self):
        self.voz("gancho")
        fo = foco_led(False).scale(2.2).move_to([0, 1.6, 0])
        ha = Circle(radius=1.0, stroke_width=0).set_fill("#FFE8A3", 0.0).move_to(fo.get_top() + DOWN * 0.7)
        sw = interruptor_sw(False).scale(1.4).move_to([0, -2.2, 0])
        self.play(FadeIn(fo), FadeIn(sw), FadeIn(ha), run_time=0.4)
        self.frac(0.2)
        for _ in range(2):
            self.play(ha.animate.set_fill(opacity=0.35), run_time=0.15)
            self.play(ha.animate.set_fill(opacity=0.0), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(fo, ha, sw)

        self.voz("p1")
        pcb = RoundedRectangle(width=6.0, height=2.6, corner_radius=0.15, stroke_width=0).set_fill("#166534", 1).move_to([0, 1.6, 0])
        cap = VGroup(Rectangle(width=0.9, height=1.5, stroke_width=0).set_fill("#1F2430", 1), Rectangle(width=0.9, height=0.2, stroke_width=0).set_fill("#98A2B3", 1).shift(UP * 0.65)).move_to([-1.6, 1.8, 0])
        ics = VGroup(*[Rectangle(width=0.6, height=0.4, stroke_width=0).set_fill("#101828", 1).move_to([x, 1.2, 0]) for x in (0.4, 1.6)])
        self.play(FadeIn(pcb), FadeIn(cap), FadeIn(ics), run_time=0.5)
        l = VGroup(tag("driver", MARCA, 32).move_to([1.0, 3.3, 0]), tag("capacitor", AMBAR, 32).move_to([-1.6, -0.2, 0]))
        self.play(FadeIn(l), run_time=0.3)
        mi = tag("necesita muy poca corriente", CIAN, 34).move_to([0, -1.8, 0])
        self.frac(0.4)
        self.play(FadeIn(mi), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(pcb, cap, ics, l, mi)

        self.voz("p2")
        n1 = tag("1", ROJO_P, 40).move_to([-3.4, 3.6, 0])
        f = Line([-3.6, 2.2, 0], [2.3, 2.2, 0]).set_stroke("#8A94A6", 10)
        n = Line([-3.6, 0.6, 0], [-0.4, 0.6, 0]).set_stroke("#F2F4F7", 10)
        n2 = Line([0.8, 0.6, 0], [1.6, 0.6, 0]).set_stroke("#F2F4F7", 10)
        sw = Line([-0.4, 0.6, 0], [0.6, 1.1, 0]).set_stroke(ROJO_P, 8)
        fo = foco_led(False).scale(1.3).move_to([2.6, 1.4, 0])
        lb = VGroup(T("fase", 26, TINTA, "BOLD").move_to([-3.0, 2.6, 0]), T("neutro", 26, TINTA, "BOLD").move_to([-3.0, 1.0, 0]))
        self.play(FadeIn(n1), Create(f), Create(n), Create(n2), Create(sw), FadeIn(fo), FadeIn(lb), run_time=0.7)
        mal = tag("interruptor en el NEUTRO", ROJO_P, 34).move_to([0, -0.9, 0])
        self.frac(0.1)
        self.play(FadeIn(mal), run_time=0.3)
        pel = card("PORTALÁMPARAS ENERGIZADO", ["aun con el interruptor apagado"], ROJO_P, 7.6, 30).move_to([0, -2.8, 0])
        self.frac(0.35)
        self.play(FadeIn(pel), run_time=0.4)
        src = fuente("NEC 2020 · 404.2(B): el interruptor no debe desconectar el neutro", [0, -4.6, 0])
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(n1, f, n, n2, sw, fo, lb, mal, pel, src)

        self.voz("p3")
        n2_ = tag("2", AMBAR, 40).move_to([-3.4, 3.6, 0])
        c1 = Line([-3.6, 2.0, 0], [3.6, 2.0, 0]).set_stroke("#8A94A6", 10)
        c2 = Line([-3.6, 1.2, 0], [3.6, 1.2, 0]).set_stroke(ROJO_P, 10)
        caps = VGroup(*[VGroup(Line([x, 1.85, 0], [x, 1.65, 0]).set_stroke(CIAN, 3), Line([x - 0.15, 1.65, 0], [x + 0.15, 1.65, 0]).set_stroke(CIAN, 3),
                               Line([x - 0.15, 1.55, 0], [x + 0.15, 1.55, 0]).set_stroke(CIAN, 3), Line([x, 1.55, 0], [x, 1.35, 0]).set_stroke(CIAN, 3)) for x in np.linspace(-3.0, 3.0, 6)])
        self.play(FadeIn(n2_), Create(c1), Create(c2), run_time=0.5)
        self.frac(0.25)
        self.play(LaggedStart(*[FadeIn(c) for c in caps], lag_ratio=0.15), run_time=0.8)
        t = tag("cables largos en paralelo = capacitor", CIAN, 32).move_to([0, -0.6, 0])
        self.play(FadeIn(t), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(n2_, c1, c2, caps, t)

        self.voz("p4")
        n3 = tag("3", MARCA, 40).move_to([-3.4, 3.6, 0])
        pl = VGroup(RoundedRectangle(width=2.2, height=3.4, corner_radius=0.15, stroke_color="#C7CCD6", stroke_width=2).set_fill("#F7F7F5", 1),
                    RoundedRectangle(width=1.2, height=2.0, corner_radius=0.1, stroke_color="#C7CCD6", stroke_width=2).set_fill(WHITE, 1),
                    Dot(radius=0.09, color="#F79009").shift(DOWN * 0.6)).move_to([0, 1.4, 0])
        self.play(FadeIn(n3), FadeIn(pl), run_time=0.4)
        self.play(Flash(pl[2], color=AMBAR), run_time=0.5)
        c = card("INTERRUPTOR CON LUZ PILOTO", ["o sensor: toma corriente por el foco"], MARCA, 7.6, 28).move_to([0, -1.8, 0])
        self.play(FadeIn(c), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(n3, pl, c)

        self.voz("p5")
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1, 1], x_length=7.4, y_length=2.8, tips=False, axis_config={"color": GRIS_N, "stroke_width": 2, "include_ticks": False}).move_to([0, 2.0, 0])
        cv = ax.plot(lambda t: (t % 2) / 2, x_range=[0, 5.99, 0.01], color=AMBAR, stroke_width=5, use_smoothing=False)
        self.play(Create(ax), run_time=0.3)
        self.play(Create(cv), run_time=1.6)
        fl = VGroup(*[Star(5, outer_radius=0.22, color="#FFE8A3", fill_opacity=1).move_to(ax.c2p(x, 1.1)) for x in (2, 4, 6)])
        self.play(LaggedStart(*[FadeIn(f, scale=1.5) for f in fl], lag_ratio=0.3), run_time=0.6)
        a = VGroup(tag("1.º: el interruptor debe cortar la FASE", VERDE_OK, 30), tag("cargas de compensación", MARCA, 30)).arrange(DOWN, buff=0.25).move_to([0, -1.6, 0])
        self.frac(0.35)
        self.play(FadeIn(a[0]), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(a[1]), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ax, cv, fl, a)

        self.voz("p6")
        pr = probador().scale(1.3).move_to([1.8, 1.6, 0])
        pt = portalampara_led(np.array([-1.8, 1.6, 0])) if True else VGroup()
        pt.scale_to_fit_height(2.6).move_to([-1.8, 1.6, 0])
        self.play(FadeIn(pr), FadeIn(pt), run_time=0.4)
        a = card("MARCA VOLTAJE", ["interruptor en el neutro: corrígelo"], ROJO_P, 7.6, 28).move_to([0, -1.2, 0])
        b = card("NO MARCA", ["prueba un foco de otra marca"], VERDE_OK, 7.6, 28).move_to([0, -3.2, 0])
        self.frac(0.2)
        self.play(FadeIn(a), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(b), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(pr, pt, a, b)
        self.final("LED que brilla apagado: revisa que se corte la fase")


# ====================================================================== V36 · agua pura
class V36D(ShortD):
    CLAVE = "v36"

    def vaso(self, c, liquido="#9CC7E8", iones=0, s=1.0):
        v = VGroup(Polygon([-1.0 * s, 1.3 * s, 0], [1.0 * s, 1.3 * s, 0], [0.8 * s, -1.3 * s, 0], [-0.8 * s, -1.3 * s, 0]).set_stroke("#C7CCD6", 3).set_fill(WHITE, 0.06))
        liq = Polygon([-0.95 * s, 0.8 * s, 0], [0.95 * s, 0.8 * s, 0], [0.8 * s, -1.25 * s, 0], [-0.8 * s, -1.25 * s, 0], stroke_width=0).set_fill(liquido, 0.5)
        rng = np.random.default_rng(iones + 3)
        io = VGroup()
        for k in range(iones):
            p = np.array([rng.uniform(-0.65, 0.65) * s, rng.uniform(-1.0, 0.6) * s, 0])
            io.add(T("+" if k % 2 else "−", 22, ROJO_P if k % 2 else CIAN, "HEAVY").move_to(p))
        g = VGroup(liq, io, v).move_to(c)
        g.io = io
        return g

    def cuerpo(self):
        self.voz("gancho")
        v = self.vaso([0, 1.6, 0], s=1.6)
        self.play(FadeIn(v), run_time=0.4)
        q = tag("¿el agua conduce?", CIAN, 40).move_to([0, -1.6, 0])
        self.frac(0.25)
        self.play(FadeIn(q), run_time=0.3)
        r = tag("lo que conduce es lo disuelto", AMBAR, 36).move_to([0, -3.0, 0])
        self.frac(0.4)
        self.play(FadeIn(r), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(v, q, r)

        self.voz("p1")
        cab = Line([-3.8, 2.6, 0], [3.8, 2.6, 0]).set_stroke(COBRE_V, 30)
        el = VGroup(*[Dot(radius=0.09, color=CIAN).move_to([x, 2.6, 0]) for x in np.linspace(-3.4, 3.4, 10)])
        self.play(FadeIn(cab), FadeIn(el), run_time=0.4)
        self.play(el.animate.shift(RIGHT * 0.6), run_time=0.8, rate_func=linear)
        l1 = tag("metal: electrones libres", COBRE_V, 32).move_to([0, 1.4, 0])
        self.play(FadeIn(l1), run_time=0.3)
        v = self.vaso([0, -1.6, 0], "#9CC7E8", 14, 1.3)
        self.frac(0.4)
        self.play(FadeIn(v), run_time=0.4)
        l2 = tag("agua: iones", CIAN, 32).move_to([0, -4.0, 0])
        self.play(FadeIn(l2), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(cab, el, l1, v, l2)

        self.voz("p2")
        a = self.vaso([-2.0, 2.0, 0], "#DDEFFF", 2, 1.1)
        b = self.vaso([2.0, 2.0, 0], "#2F6FD0", 30, 1.1)
        la = VGroup(T("destilada", 30, TINTA, "HEAVY"), T("≈ 1 µS/cm", 34, CIAN, "HEAVY")).arrange(DOWN, buff=0.1).next_to(a, DOWN, buff=0.3)
        lb = VGroup(T("mar", 30, TINTA, "HEAVY"), T("≈ 50 000 µS/cm", 34, AMBAR, "HEAVY")).arrange(DOWN, buff=0.1).next_to(b, DOWN, buff=0.3)
        self.play(FadeIn(a), FadeIn(la), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(b), FadeIn(lb), run_time=0.4)
        x = T("× 50 000", 90, ROJO_P, "HEAVY").move_to([0, -2.8, 0])
        self.frac(0.3)
        self.play(FadeIn(x, scale=1.3), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(a, b, la, lb, x)

        self.voz("p3")
        ej = VGroup(card("AGUA DE LA LLAVE", ["minerales disueltos"], CIAN, 7.6, 30), card("LLUVIA EN EL SUELO", ["arrastra sales"], MARCA, 7.6, 30), card("SUDOR", ["sal"], AMBAR, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 1.4, 0])
        for t_ in ej:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.35)
            self.frac(0.18)
        r = tag("en la práctica: TODA conduce", ROJO_P, 36).move_to([0, -2.8, 0])
        self.play(FadeIn(r), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ej, r)

        self.voz("p4")
        sec = VGroup(T("piel seca", 34, TINTA, "HEAVY"), T("100 000 Ω", 60, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, 3.0, 0])
        moj = VGroup(T("piel mojada", 34, TINTA, "HEAVY"), T("≈ 1000 Ω", 60, ROJO_P, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, 0.8, 0])
        self.play(FadeIn(sec), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(moj), run_time=0.4)
        x = VGroup(T("I × 100", 90, ROJO_P, "HEAVY")).move_to([0, -1.8, 0])
        self.frac(0.25)
        self.play(FadeIn(x, scale=1.2), run_time=0.4)
        cz = corazon(0.7).move_to([0, -3.8, 0])
        self.play(FadeIn(cz), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(sec, moj, x, cz)

        self.voz("p5")
        to = tomacorriente(np.array([0, 0, 0])).scale(1.8).move_to([-1.6, 1.6, 0])
        go = gotas(np.array([1.8, 1.6, 0]), 7, "#7FD1FF").scale(1.6)
        x = equis(ROJO, 0.6).move_to([0, 1.6, 0])
        self.play(FadeIn(to), FadeIn(go), run_time=0.4)
        self.frac(0.3)
        self.play(FadeIn(x, scale=1.4), run_time=0.3)
        r = tag("nunca con las manos mojadas", ROJO_P, 36).move_to([0, -1.6, 0])
        self.play(FadeIn(r), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(to, go, x, r)

        self.voz("p6")
        u = VGroup(card("LABORATORIO Y BATERÍAS", ["agua destilada: sin minerales"], CIAN, 7.6, 30), card("FUEGO ELÉCTRICO", ["no uses agua común: extintor CO₂ o PQS"], ROJO_P, 7.6, 28),
                   card("INDUSTRIA", ["se mide la conductividad"], MARCA, 7.6, 30)).arrange(DOWN, buff=0.3).move_to([0, 0.8, 0])
        for t_ in u:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.4)
            self.frac(0.22)
        self.cerrar_voz(0.15)
        self.limpiar(u)
        self.final("El agua pura casi no conduce, la de tu casa sí")


# ====================================================================== V37 · pararrayos
class V37D(ShortD):
    CLAVE = "v37"

    def cuerpo(self):
        self.voz("gancho")
        ed = pararrayos_edificio().scale(0.8).move_to([0, 0.2, 0])
        self.play(FadeIn(ed), run_time=0.5)
        a = VGroup(tag("no atrae", ROJO_P, 34), tag("no evita", ROJO_P, 34)).arrange(RIGHT, buff=0.3).move_to([0, 4.0, 0])
        self.play(FadeIn(a[0]), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(a[1]), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ed, a)

        self.voz("p1")
        ed = pararrayos_edificio().scale(0.85).move_to([0, 0.6, 0])
        self.play(FadeIn(ed), run_time=0.4)
        lb = VGroup(tag("puntas captoras", AMBAR, 28).next_to(ed.puntas, UP, buff=0.15), tag("bajantes", COBRE_V, 28).move_to([0, 0.8, 0]), tag("electrodos", "#8B5A2B", 28).move_to([0, -4.5, 0]))
        for l, m in zip(lb, (ed.puntas, ed.baj, ed.elec)):
            self.play(FadeIn(l), Indicate(m, color=AMBAR), run_time=0.5)
            self.frac(0.2)
        self.cerrar_voz(0.15)
        self.limpiar(ed, lb)

        self.voz("p2")
        ed = pararrayos_edificio().scale(0.85).move_to([0, 0.0, 0])
        self.play(FadeIn(ed), run_time=0.3)
        tip = ed.puntas[1].get_top()
        ry = VGroup(rayo(tip + UP * 4 + LEFT * 0.8, tip, color=AMBAR, amp=0.4, w=8, semilla=2), rayo(tip + UP * 4 + LEFT * 0.8, tip, color=WHITE, amp=0.4, w=3, semilla=2))
        self.frac(0.2)
        self.sfx("pop", -8)
        self.play(FadeIn(ry), Flash(tip, color=AMBAR, flash_radius=0.6), run_time=0.3)
        self.play(FadeOut(ry), run_time=0.4)
        l = tag("punto de impacto preparado", AMBAR, 32).move_to([0, -5.3, 0])
        self.play(FadeIn(l), run_time=0.3)
        self.cerrar_voz(0.15)
        self.limpiar(ed, l)

        self.voz("p3")
        ed = pararrayos_edificio().scale(0.85).move_to([0, 0.4, 0])
        self.play(FadeIn(ed), run_time=0.3)
        cf = corriente([ed.puntas[1].get_top(), ed.baj[1].get_start(), ed.baj[1].get_end()], vel=3.0, escala=1.4, color=AMBAR)
        self.add(cf)
        n = tag("decenas de miles de amperios", ROJO_P, 32).move_to([0, 4.3, 0])
        self.play(FadeIn(n), run_time=0.3)
        self.wait(1.4)
        self.remove(cf)
        self.cerrar_voz(0.15)
        self.limpiar(ed, n)

        self.voz("p4")
        ed = VGroup(Rectangle(width=2.6, height=3.0, stroke_width=0).set_fill("#475467", 1).move_to([-1.4, -2.5, 0]), Rectangle(width=1.8, height=1.6, stroke_width=0).set_fill("#475467", 1).move_to([1.2, -3.2, 0]))
        suelo = Line([-4.2, -4.0, 0], [4.2, -4.0, 0]).set_stroke("#5A3E2B", 10)
        self.play(FadeIn(ed), Create(suelo), run_time=0.4)
        R = 2.4
        es = Circle(radius=R, stroke_color=CIAN, stroke_width=4).set_fill(CIAN, 0.08).move_to([-1.6, -4.0 + R + 0.3, 0])
        self.frac(0.2)
        self.play(FadeIn(es), run_time=0.3)
        self.play(es.animate.move_to([-0.6, -1.0 + R, 0]), run_time=0.8)
        self.play(es.animate.move_to([1.6, -2.4 + R * 0.75, 0]), run_time=0.8)
        d = VGroup(T("esfera de 46 m", 44, CIAN, "HEAVY")).move_to([0, 3.6, 0])
        self.play(FadeIn(d), run_time=0.3)
        src = fuente("NFPA 780 · método de la esfera rodante", [0, -5.3, 0])
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz(0.15)
        self.limpiar(ed, suelo, es, d, src)

        self.voz("p5")
        tab = RoundedRectangle(width=3.0, height=4.0, corner_radius=0.12, stroke_color="#98A2B3", stroke_width=3).set_fill("#C9CED6", 1).move_to([-1.8, 1.6, 0])
        spd = VGroup(Rectangle(width=1.2, height=2.0, stroke_width=0).set_fill("#344054", 1), T("SPD", 26, WHITE, "HEAVY")).move_to(tab)
        self.play(FadeIn(tab), FadeIn(spd), run_time=0.4)
        it = VGroup(tag("unir tuberías", MARCA, 30), tag("unir la tierra eléctrica", VERDE_OK, 30), tag("supresor en el tablero", AMBAR, 30)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0, -2.0, 0])
        for t_ in it:
            self.play(FadeIn(t_, shift=RIGHT * 0.2), run_time=0.35)
            self.frac(0.18)
        self.cerrar_voz(0.15)
        self.limpiar(tab, spd, it)

        self.voz("p6")
        n = VGroup(T("≈ 30 000 A", 90, AMBAR, "HEAVY"), T("promedio", 36, TINTA, "BOLD"), T("> 100 000 A", 70, ROJO_P, "HEAVY"), T("algunos", 36, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, 2.2, 0])
        self.play(FadeIn(n[:2]), run_time=0.4)
        self.frac(0.15)
        self.play(FadeIn(n[2:]), run_time=0.4)
        c = card("CONEXIONES FIRMES", ["sin curvas cerradas en los bajantes"], MARCA, 7.6, 30).move_to([0, -2.4, 0])
        self.frac(0.3)
        self.play(FadeIn(c), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(n, c)
        self.final("Captar, bajar y disipar el rayo")


# ====================================================================== V38 · PLC
class V38D(ShortD):
    CLAVE = "v38"

    def cuerpo(self):
        self.voz("gancho")
        rel = VGroup(*[RoundedRectangle(width=0.7, height=1.0, corner_radius=0.06, stroke_color="#475467", stroke_width=1.5).set_fill("#C9CED6", 1).move_to([-3.2 + 0.85 * (k % 8), 3.2 - 1.2 * (k // 8), 0]) for k in range(24)])
        self.play(LaggedStart(*[FadeIn(r) for r in rel], lag_ratio=0.03), run_time=0.8)
        pl = plc(1.6).move_to([0, -2.0, 0])
        self.frac(0.4)
        self.play(rel.animate.set_opacity(0.25), FadeIn(pl, scale=0.8), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(rel, pl)

        self.voz("p1")
        pl = plc(1.8).move_to([0, 2.2, 0])
        self.play(FadeIn(pl), run_time=0.4)
        s = VGroup(tag("P", MARCA, 50), tag("L", MARCA, 50), tag("C", MARCA, 50)).arrange(RIGHT, buff=0.2).move_to([0, -0.4, 0])
        d = T("controlador lógico programable", 34, TINTA, "HEAVY").move_to([0, -1.6, 0])
        self.play(FadeIn(s), FadeIn(d), run_time=0.4)
        a = VGroup(tag("polvo", GRIS_N, 28), tag("calor", AMBAR, 28), tag("ruido eléctrico", ROJO_P, 28)).arrange(RIGHT, buff=0.2).move_to([0, -3.0, 0])
        self.frac(0.4)
        self.play(FadeIn(a), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(pl, s, d, a)

        self.voz("p2")
        pl = plc(1.6).move_to([0, 1.0, 0])
        ent = VGroup(card("ENTRADAS", ["pulsadores · sensores · flotadores"], VERDE_OK, 7.6, 30)).move_to([0, -1.6, 0])
        sal = VGroup(card("SALIDAS", ["bobinas · luces · válvulas"], AMBAR, 7.6, 30)).move_to([0, -3.6, 0])
        self.play(FadeIn(pl), run_time=0.3)
        self.play(FadeIn(ent, shift=UP * 0.2), run_time=0.4)
        self.frac(0.45)
        self.play(FadeIn(sal, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(pl, ent, sal)

        self.voz("p3")
        c = np.array([0, 1.4, 0])
        R = 2.2
        et = [("LEER\nENTRADAS", VERDE_OK), ("EJECUTAR\nPROGRAMA", MARCA), ("ACTUALIZAR\nSALIDAS", AMBAR)]
        nodos = VGroup()
        for k, (t, col) in enumerate(et):
            a = PI / 2 - k * 2 * PI / 3
            p = c + R * np.array([np.cos(a), np.sin(a), 0])
            tt = T(t, 22, "#101828", "HEAVY")
            if tt.width > 1.6:
                tt.scale_to_fit_width(1.6)
            nodos.add(VGroup(Circle(radius=0.95, stroke_width=0).set_fill(col, 1), tt).move_to(p))
        arcs = VGroup(*[CurvedArrow(nodos[k].get_center() + 1.0 * normalize(nodos[(k + 1) % 3].get_center() - nodos[k].get_center()),
                                    nodos[(k + 1) % 3].get_center() + 1.0 * normalize(nodos[k].get_center() - nodos[(k + 1) % 3].get_center()), angle=-PI / 4, color=TINTA, stroke_width=5) for k in range(3)])
        self.play(LaggedStart(*[FadeIn(n_, scale=0.8) for n_ in nodos], lag_ratio=0.3), run_time=1.0)
        self.play(Create(arcs), run_time=0.6)
        ms = tag("cada pocos milisegundos", CIAN, 34).move_to([0, -2.6, 0])
        self.play(FadeIn(ms), run_time=0.3)
        self.play(Rotate(VGroup(arcs), -2 * PI, about_point=c), run_time=1.6)
        self.cerrar_voz(0.15)
        self.limpiar(nodos, arcs, ms)

        self.voz("p4")
        n = tag("IEC 61131-3", MARCA, 38).move_to([0, 4.0, 0])
        self.play(FadeIn(n), run_time=0.3)
        y = 2.0
        rl = VGroup(Line([-3.8, 3.0, 0], [-3.8, -1.0, 0]).set_stroke(TINTA, 5), Line([3.8, 3.0, 0], [3.8, -1.0, 0]).set_stroke(TINTA, 5))
        ln = VGroup(*[Line([a, y, 0], [b, y, 0]) for a, b in ((-3.8, -2.6), (-2.2, -0.6), (-0.2, 2.05), (2.75, 3.8))]).set_stroke(TINTA, 3)
        c1 = VGroup(Line([-2.6, y - 0.35, 0], [-2.6, y + 0.35, 0]), Line([-2.2, y - 0.35, 0], [-2.2, y + 0.35, 0])).set_stroke(TINTA, 5)
        c2 = VGroup(Line([-0.6, y - 0.35, 0], [-0.6, y + 0.35, 0]), Line([-0.2, y - 0.35, 0], [-0.2, y + 0.35, 0]), Line([-0.7, y - 0.35, 0], [-0.1, y + 0.35, 0])).set_stroke(TINTA, 5)
        bo = VGroup(Arc(radius=0.35, start_angle=PI * 0.6, angle=PI * 0.8), Arc(radius=0.35, start_angle=-PI * 0.4, angle=PI * 0.8)).set_stroke(TINTA, 5).move_to([2.4, y, 0])
        lb = VGroup(T("nivel bajo", 22, TINTA, "BOLD").move_to([-2.4, y + 0.7, 0]), T("no alto", 22, TINTA, "BOLD").move_to([-0.4, y + 0.7, 0]), T("BOMBA", 22, AMBAR, "HEAVY").move_to([2.4, y + 0.7, 0]))
        self.play(Create(rl), Create(ln), run_time=0.4)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(bo), FadeIn(lb), run_time=0.5)
        lad = tag("diagrama escalera", MARCA, 34).move_to([0, -0.2, 0])
        self.play(FadeIn(lad), run_time=0.3)
        cf = VGroup(*[Line([a, y, 0], [b, y, 0]) for a, b in ((-3.8, -2.6), (-2.2, -0.6), (-0.2, 2.05))]).set_stroke(VERDE_OK, 8)
        self.frac(0.5)
        self.play(Create(cf), c1.animate.set_stroke(VERDE_OK), c2.animate.set_stroke(VERDE_OK), bo.animate.set_stroke(VERDE_OK), run_time=0.6)
        self.cerrar_voz(0.15)
        self.limpiar(n, rl, ln, c1, c2, bo, lb, lad, cf)

        self.voz("p5")
        a = card("CAMBIAS EL PROGRAMA", ["no el cableado"], VERDE_OK, 7.6, 32).move_to([0, 2.4, 0])
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.4)
        pl = plc(1.4).move_to([0, -1.0, 0])
        self.frac(0.35)
        self.play(FadeIn(pl), run_time=0.4)
        self.cerrar_voz(0.15)
        self.limpiar(a, pl)

        self.voz("p6")
        tq = Rectangle(width=2.6, height=5.0, stroke_color="#98A2B3", stroke_width=4).set_fill("#0B1530", 0.2).move_to([-1.8, 0.6, 0])
        ag = Rectangle(width=2.5, height=1.2, stroke_width=0).set_fill("#2F6FD0", 0.7).move_to(tq.get_bottom() + UP * 0.65)
        fa = VGroup(Circle(radius=0.2, stroke_width=0).set_fill(AMBAR, 1).move_to([-0.3, 2.4, 0]), T("ALTO", 22, AMBAR, "HEAVY").move_to([0.6, 2.4, 0]))
        fb = VGroup(Circle(radius=0.2, stroke_width=0).set_fill(VERDE_OK, 1).move_to([-0.3, -1.0, 0]), T("BAJO", 22, VERDE_OK, "HEAVY").move_to([0.6, -1.0, 0]))
        bo = motor_3f(0.6).move_to([2.6, -2.6, 0])
        self.play(FadeIn(tq), FadeIn(ag), FadeIn(fa), FadeIn(fb), FadeIn(bo), run_time=0.5)
        self.frac(0.15)
        self.play(Indicate(fb), run_time=0.4)
        on = tag("BOMBA ON", VERDE_OK, 30).move_to([2.6, -4.0, 0])
        self.play(FadeIn(on), run_time=0.2)
        self.play(ag.animate.stretch_to_fit_height(4.2).move_to(tq.get_bottom() + UP * 2.15), run_time=2.0)
        off = tag("BOMBA OFF", ROJO_P, 30).move_to([2.6, -4.0, 0])
        self.play(Indicate(fa), FadeTransform(on, off), run_time=0.5)
        self.cerrar_voz(0.15)
        self.limpiar(tq, ag, fa, fb, bo, off)
        self.final("PLC: lee, decide y actúa en un ciclo")


# ====================================================================== portadas V19–V38
PORT_D = {
    "v19": (["#062A1A", "#12305A"], [("¿LA VARILLA", "#FFFFFF"), ("TE PROTEGE?", "#3DDC84")], "¡no basta!"),
    "v20": (["#2A1F05", "#12305A"], [("¿ALTERNA O", "#FFFFFF"), ("CONTINUA?", "#FFD84D")], "60 Hz"),
    "v21": (["#0B1530", "#3A2A6E"], [("¿QUIÉN ENCIENDE", "#FFFFFF"), ("LAS LUCES?", "#FFD84D")], "fotocelda"),
    "v22": (["#0A2A3A", "#1E5B8A"], [("¿POR QUÉ", "#FFFFFF"), ("ME DA TOQUES?", "#6FF2FF")], "¿estática o falla?"),
    "v23": (["#1A1A1A", "#2F4F4F"], [("¿GIRA", "#FFFFFF"), ("AL REVÉS?", "#FF5A5F")], "cambia 2 fases"),
    "v24": (["#060C1C", "#1E3A6E"], [("¿POR QUÉ", "#FFFFFF"), ("ZUMBAN?", "#9EC5FF")], "efecto corona"),
    "v25": (["#20140A", "#12305A"], [("¿CÓMO FUNCIONA", "#FFFFFF"), ("UN FUSIBLE?", "#FFD84D")], "¡no lo puentees!"),
    "v26": (["#2E0A06", "#12305A"], [("¿FACTOR DE", "#FFFFFF"), ("POTENCIA?", "#FF9F1C")], "+36 % corriente"),
    "v27": (["#16213E", "#4A6FA5"], [("¿CÓMO DETECTA", "#FFFFFF"), ("EL METAL?", "#6FF2FF")], "sin tocarlo"),
    "v28": (["#2E0A06", "#3A1A1A"], [("¿120 V", "#FFFFFF"), ("A 240 V?", "#FF5A5F")], "× 4 la potencia"),
    "v29": (["#0B2A4A", "#3A6EA5"], [("¿POR QUÉ", "#FFFFFF"), ("BAJAN LAS LUCES?", "#FFD84D")], "¿neutro flojo?"),
    "v30": (["#062A1A", "#1E5B8A"], [("¿QUÉ ES UN", "#FFFFFF"), ("kWh?", "#3DDC84")], "lo que pagas"),
    "v31": (["#1A1A1A", "#12305A"], [("¿CÓMO FUNCIONA", "#FFFFFF"), ("UN VARIADOR?", "#6FF2FF")], "Hz = velocidad"),
    "v32": (["#20140A", "#2F4F4F"], [("¿ESTRELLA O", "#FFFFFF"), ("TRIÁNGULO?", "#FFD84D")], "lee la placa"),
    "v33": (["#0A2A3A", "#12305A"], [("¿QUÉ SIGNIFICA", "#FFFFFF"), ("IP65?", "#6FF2FF")], "polvo · agua"),
    "v34": (["#2A1F05", "#3A1A1A"], [("¿POR QUÉ ES", "#FFFFFF"), ("ASÍ?", "#FFD84D")], "paro de emergencia"),
    "v35": (["#0B1530", "#2F4F4F"], [("¿BRILLA", "#FFFFFF"), ("APAGADO?", "#FFD84D")], "¡revisa la fase!"),
    "v36": (["#0A2A3A", "#2F6FD0"], [("¿EL AGUA PURA", "#FFFFFF"), ("CONDUCE?", "#6FF2FF")], "casi nada"),
    "v37": (["#060C1C", "#3A2A6E"], [("¿CÓMO FUNCIONA", "#FFFFFF"), ("UN PARARRAYOS?", "#FFD84D")], "no atrae rayos"),
    "v38": (["#16213E", "#1E5B8A"], [("¿QUÉ ES", "#FFFFFF"), ("UN PLC?", "#3DDC84")], "lee · decide · actúa"),
}


class PortadaD(MovingCameraScene):
    def construct(self):
        import os
        from miniaturas import texto_gancho, sticker, logo_esq
        k = os.environ["CLAVE"]
        fondo, txt, st_txt = PORT_D[k]
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=fondo, opacity=1).set_sheen_direction(UR))
        t = texto_gancho(txt, 100)
        t.scale_to_fit_width(min(8.2, t.width)).move_to([0, 5.0, 0])
        il = self.ilustra(k)
        if il.width > 8.4:
            il.scale_to_fit_width(8.4)
        if il.height > 6.6:
            il.scale_to_fit_height(6.6)
        il.move_to([0, 0.3, 0])
        st = sticker(st_txt, "#E5484D", size=56, ang=-0.04).move_to([0, -4.3, 0])
        self.add(il, t, st)
        logo_esq(self, (0, -6.2))

    def ilustra(self, k):
        if k == "v19":
            return VGroup(varilla_tierra(4.0), equis(ROJO, 0.7).move_to([2.0, 1.0, 0]))
        if k == "v20":
            ax = VGroup(onda(lambda x: np.sin(x * 2), -3.6, 3.6, 1.2, 1.0, CIAN, 10), Line([-3.6, -1.4, 0], [3.6, -1.4, 0]).set_stroke(AMBAR, 10))
            return VGroup(ax, T("~", 120, CIAN, "HEAVY").move_to([0, 2.8, 0]), T("⎓", 120, AMBAR, "HEAVY").move_to([0, -2.6, 0]))
        if k == "v21":
            lu = luminaria(1.0, True)
            haz = Polygon(lu.lente.get_left(), lu.lente.get_right(), lu.lente.get_center() + DOWN * 4 + RIGHT * 1.8, lu.lente.get_center() + DOWN * 4 + LEFT * 1.8, stroke_width=0).set_fill("#FFE8A3", 0.3)
            fc = fotocelda(1.0).next_to(lu.cabeza, UP, buff=0)
            return VGroup(haz, lu, fc)
        if k == "v22":
            mano = Circle(radius=0.9).set_fill(PIEL, 1).set_stroke("#9A6A4A", 2).move_to([-2.0, 0, 0])
            man = VGroup(RoundedRectangle(width=3.2, height=0.7, corner_radius=0.3, stroke_width=0).set_fill("#C9CED6", 1), Circle(radius=0.7, stroke_width=0).set_fill("#98A2B3", 1).shift(LEFT * 1.7)).move_to([2.2, 0, 0])
            return VGroup(mano, man, rayo(mano.get_right(), man.get_left(), color=CIAN, amp=0.15, w=8))
        if k == "v23":
            mo = motor_3f(2.2)
            return VGroup(mo, Arc(radius=2.6, start_angle=0, angle=PI * 1.4, color=ROJO_P, stroke_width=12).move_arc_center_to(mo.get_center()).add_tip())
        if k == "v24":
            cond = Circle(radius=1.0, stroke_width=0).set_fill("#B8BEC8", 1)
            halo = VGroup(*[Circle(radius=1.1 + 0.25 * j, stroke_width=0).set_fill("#9EC5FF", 0.2 - 0.03 * j) for j in range(6)])
            de = VGroup(*[rayo(1.0 * np.array([np.cos(a), np.sin(a), 0]), 2.0 * np.array([np.cos(a), np.sin(a), 0]), color="#C9DCFF", semilla=j, amp=0.1, w=4) for j, a in enumerate(np.linspace(0, TAU, 12, endpoint=False))])
            return VGroup(halo, cond, de)
        if k == "v25":
            return VGroup(fusible_vidrio(1.8, True), llama(0.9).move_to([0, 1.4, 0]))
        if k == "v26":
            o = np.array([-3.0, -1.6, 0])
            return VGroup(Arrow(o, o + RIGHT * 6, buff=0, color=VERDE_OK, stroke_width=16), Arrow(o + RIGHT * 6, o + RIGHT * 6 + UP * 3.8, buff=0, color=AMBAR, stroke_width=16),
                          Arrow(o, o + RIGHT * 6 + UP * 3.8, buff=0, color=MARCA, stroke_width=16), T("cos φ", 80, TINTA, "HEAVY").move_to(o + RIGHT * 2.0 + UP * 0.6))
        if k == "v27":
            se = sensor_inductivo(2.0, True)
            return VGroup(se, Square(1.4, stroke_width=0).set_fill("#98A2B3", 1).next_to(se, RIGHT, buff=0.4))
        if k == "v28":
            hn = horno(1.6)
            return VGroup(hn, humo(hn.get_top(), 5), T("× 4", 140, ROJO_P, "HEAVY").next_to(hn, DOWN, buff=0.3))
        if k == "v29":
            return VGroup(*[foco_led(True).scale(2.0).move_to([x, 0, 0]).set_opacity(o) for x, o in ((-2.6, 1.0), (0, 0.55), (2.6, 0.3))])
        if k == "v30":
            return VGroup(T("1000 W", 90, TINTA, "HEAVY"), T("× 1 h", 90, AMBAR, "HEAVY"), T("= 1 kWh", 110, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.3)
        if k == "v31":
            return VGroup(RoundedRectangle(width=3.6, height=5.2, corner_radius=0.2, stroke_color="#98A2B3", stroke_width=4).set_fill("#E4E7EC", 1),
                          RoundedRectangle(width=2.6, height=1.2, corner_radius=0.1, stroke_width=0).set_fill("#101828", 1).shift(UP * 1.4), T("45.0 Hz", 46, "#4ADE80", "HEAVY").shift(UP * 1.4),
                          Circle(radius=0.6, stroke_color="#475467", stroke_width=6).set_fill("#C9CED6", 1).shift(DOWN * 1.2))
        if k == "v32":
            y = VGroup(*[Line(ORIGIN, 1.8 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(AMBAR, 14) for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 - 2 * PI / 3)]).move_to([-2.2, 0, 0])
            d = Polygon(*[2.0 * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + 2 * PI / 3, PI / 2 - 2 * PI / 3)]).set_stroke(CIAN, 14).move_to([2.2, 0, 0])
            return VGroup(y, d)
        if k == "v33":
            return VGroup(RoundedRectangle(width=5.0, height=5.0, corner_radius=0.3, stroke_color="#98A2B3", stroke_width=4).set_fill("#E4E7EC", 1),
                          *[tornillo_frente(0.18).move_to([x, y, 0]) for x in (-2.0, 2.0) for y in (-2.0, 2.0)], T("IP65", 110, "#101828", "HEAVY"))
        if k == "v34":
            return hongo_emergencia(2.2)
        if k == "v35":
            fo = foco_led(False).scale(3.0)
            return VGroup(Circle(radius=1.2, stroke_width=0).set_fill("#FFE8A3", 0.35).move_to(fo.get_top() + DOWN * 1.1), fo)
        if k == "v36":
            return VGroup(*[Circle(radius=0.0)]) if False else VGroup(V36D.vaso(None, [0, 0, 0], "#9CC7E8", 20, 2.2))
        if k == "v37":
            ed = pararrayos_edificio()
            tip = ed.puntas[1].get_top()
            return VGroup(ed, rayo(tip + UP * 3 + LEFT * 1.0, tip, color=AMBAR, amp=0.4, w=10, semilla=2))
        return plc(2.6)

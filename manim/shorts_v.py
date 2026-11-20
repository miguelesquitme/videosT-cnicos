"""Shorts verticales V03–V18 (1080x1920, fondo azul marino). Guiones y fuentes en shorts_guiones.py.
Render: FORMATO=v VOZ=eleven manim -o final shorts_v.py V03"""
from comun_e import *
from comun_e import _osc
from shorts_guiones import SHORTS
from taller import (corriente, cable_hilos, foco_led, tomacorriente, placa_toma, clavija, P, hervidor, plancha,
                    ventilador, regleta, pinza_icono)
from nema import breaker, centro_carga, multimetro, punta_prueba, mover_palanca
from dibujos_aves import poste, linea_aerea, aislador_pin, check, equis, escalera, piscucha, pajarito

CLARO = "#C9D1F0"
COBRE_CL = "#E6A16A"


# ---------------------------------------------------------------------- piezas nuevas
def avioneta(color="#E4E7EC"):
    fus = VMobject().set_points_smoothly([P(-1.6, 0.0), P(-1.2, 0.22), P(0.6, 0.26), P(1.5, 0.12), P(1.7, 0.0),
                                          P(1.5, -0.12), P(0.6, -0.22), P(-1.2, -0.2), P(-1.6, 0.0)])
    fus.set_fill(color, 1).set_stroke(LINEA, 2)
    ala = Polygon(P(-0.1, 0.05), P(0.5, 0.05), P(-0.2, -0.9), P(-0.6, -0.9), stroke_color=LINEA, stroke_width=2).set_fill("#C9CED6", 1)
    ala2 = Polygon(P(0.0, 0.1), P(0.45, 0.1), P(-0.1, 0.7), P(-0.4, 0.7), stroke_color=LINEA, stroke_width=2).set_fill("#B8BEC8", 1)
    cola = Polygon(P(-1.25, 0.15), P(-1.55, 0.75), P(-1.35, 0.75), P(-1.0, 0.2), stroke_color=LINEA, stroke_width=2).set_fill(ROJO, 1)
    vent = VGroup(*[RoundedRectangle(width=0.13, height=0.1, corner_radius=0.03, stroke_width=0).set_fill("#3A86C8", 1).move_to(P(x, 0.08)) for x in (0.3, 0.55, 0.8)])
    cab = Polygon(P(1.1, 0.12), P(1.45, 0.1), P(1.55, 0.03), P(1.15, 0.03), stroke_width=0).set_fill("#3A86C8", 1)
    helice = Line(P(1.72, 0.35), P(1.72, -0.35), stroke_color=METAL2, stroke_width=4)
    return VGroup(ala2, fus, ala, cola, vent, cab, helice)


def esfera(color, r=0.32):
    return VGroup(Circle(radius=r, stroke_color=_osc(color, 0.35), stroke_width=2).set_fill(color, 1),
                  Arc(radius=r * 0.65, start_angle=PI * 0.55, angle=PI * 0.35).set_stroke(WHITE, 3, 0.7))


def nucleo(n=7, w=2.6, h=2.2):
    lams = VGroup(*[Rectangle(width=w, height=h * 0.12, stroke_color="#3A4250", stroke_width=1.2).set_fill("#8C96A3" if k % 2 else "#A7B0BC", 1)
                    for k in range(n)]).arrange(DOWN, buff=0.02)
    return lams


def transformador():
    tanque_ = RoundedRectangle(width=1.6, height=2.2, corner_radius=0.18, stroke_color="#5B6573", stroke_width=2).set_fill("#9AA3AF", 1)
    aletas = VGroup(*[Line(P(x, -0.9), P(x, 0.8), stroke_color="#7C8594", stroke_width=3) for x in np.linspace(-0.6, 0.6, 7)])
    tapa = RoundedRectangle(width=1.8, height=0.22, corner_radius=0.08, stroke_color="#5B6573", stroke_width=2).set_fill("#B8BEC8", 1).move_to(P(0, 1.15))
    buj = VGroup(*[VGroup(*[RoundedRectangle(width=0.28 - 0.04 * k, height=0.1, corner_radius=0.04, stroke_color="#9C9A8E", stroke_width=1)
                            .set_fill("#EEF0EA", 1).move_to(P(x, 1.33 + 0.12 * k)) for k in range(3)]) for x in (-0.45, 0.45)])
    return VGroup(tanque_, aletas, tapa, buj)


def onda(fun, x0, x1, y0, amp, color, w=5, n=200):
    xs = np.linspace(x0, x1, n)
    return VMobject().set_points_smoothly([P(x, y0 + amp * fun(x)) for x in xs]).set_stroke(color, w)


def ducha():
    cuerpo = RoundedRectangle(width=1.5, height=1.1, corner_radius=0.35, stroke_color="#98A2B3", stroke_width=2).set_fill("#F2F4F7", 1)
    cabeza = Circle(radius=0.62, stroke_color="#98A2B3", stroke_width=2).set_fill("#E4E7EC", 1).move_to(P(0, -0.75))
    agujeros = VGroup(*[Dot(P(0.25 * np.cos(a), -0.75 + 0.25 * np.sin(a)), radius=0.04, color="#667085") for a in np.linspace(0, TAU, 8, endpoint=False)])
    brazo_ = Rectangle(width=0.2, height=1.0, stroke_color="#98A2B3", stroke_width=2).set_fill("#D0D5DD", 1).move_to(P(0, 1.0))
    selector = Circle(radius=0.14, stroke_width=0).set_fill(ROJO, 1).move_to(P(0.45, 0.15))
    return VGroup(brazo_, cuerpo, cabeza, agujeros, selector)


def gotas(c, n=9, color="#7FD1FF"):
    return VGroup(*[Line(c + P(x, -0.2 - 0.25 * (k % 3)), c + P(x, -0.45 - 0.25 * (k % 3)), stroke_color=color, stroke_width=4)
                    for k, x in enumerate(np.linspace(-0.45, 0.45, n))])


def extintor(clase="C"):
    cil = RoundedRectangle(width=1.1, height=2.6, corner_radius=0.4, stroke_color=_osc(ROJO, 0.4), stroke_width=2).set_fill("#D92D20", 1)
    cuello = Rectangle(width=0.36, height=0.3, stroke_width=0).set_fill("#1D2939", 1).move_to(P(0, 1.45))
    manija = Polygon(P(-0.15, 1.6), P(0.6, 1.75), P(0.62, 1.65), P(-0.1, 1.55), stroke_width=0).set_fill("#344054", 1)
    manguera = VMobject().set_points_smoothly([P(0.1, 1.55), P(0.75, 1.3), P(0.85, 0.3), P(0.75, -0.4)]).set_stroke("#1D2939", 7)
    etiqueta = RoundedRectangle(width=0.8, height=0.9, corner_radius=0.08, stroke_width=0).set_fill(WHITE, 1).move_to(P(0, 0.1))
    letra = VGroup(Square(0.5, stroke_width=0).set_fill("#1570EF", 1), T(clase, 30, WHITE, "HEAVY")).move_to(etiqueta)
    letra[1].move_to(letra[0])
    return VGroup(manguera, cil, cuello, manija, etiqueta, letra)


def motor():
    cuerpo = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.2, stroke_color="#3A4250", stroke_width=2).set_fill("#2F6FB0", 1)
    aletas = VGroup(*[Line(P(x, -0.7), P(x, 0.7), stroke_color="#245A90", stroke_width=3) for x in np.linspace(-1.0, 1.0, 9)])
    tapa = RoundedRectangle(width=0.3, height=1.4, corner_radius=0.1, stroke_color="#3A4250", stroke_width=2).set_fill("#3A86C8", 1).move_to(P(1.4, 0))
    eje = Rectangle(width=0.6, height=0.18, stroke_color=METAL_OSC, stroke_width=1.5).set_fill(METAL, 1).move_to(P(1.85, 0))
    pata = Rectangle(width=2.2, height=0.15, stroke_width=0).set_fill("#344054", 1).move_to(P(0, -0.9))
    placa_ = RoundedRectangle(width=0.8, height=0.5, corner_radius=0.05, stroke_width=0).set_fill("#E4E7EC", 1).move_to(P(-0.4, 0.2))
    letra = T("CODE G", 12, "#1D2939", "HEAVY").move_to(placa_)
    return VGroup(pata, cuerpo, aletas, tapa, eje, placa_, letra)


def conductor_color(color, largo=5.0, w=0.55, texto=None):
    borde = "#8F9AC8" if color == FASE else (_osc(color, 0.35) if color != NEUTRO else NEUTRO_BORDE)
    c = RoundedRectangle(width=largo, height=w, corner_radius=w / 2, stroke_color=borde, stroke_width=2).set_fill(color, 1)
    if color == TIERRA + "_FRANJA":
        pass
    return c


def seccion_awg(area_mm2, escala=0.55, color=COBRE):
    r = np.sqrt(area_mm2 / PI) * escala
    return VGroup(Circle(radius=r * 1.45, stroke_color="#8F9AC8", stroke_width=2).set_fill(FASE, 1),
                  Circle(radius=r, stroke_color=_osc(color, 0.35), stroke_width=2).set_fill(color, 1))


# ---------------------------------------------------------------------- escena base
class ShortV(Escena):
    CLAVE = "v03"

    def setup(self):
        self.CARPETA_VOZ = f"voz_{self.CLAVE}"
        self.TIT1, self.TIT2, self.GUION = SHORTS[self.CLAVE]
        super().setup()

    def limpiar(self, *ms, t=0.35):
        ms = [m for m in ms if m is not None]
        for m in ms:
            for s in m.get_family():
                s.clear_updaters()
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=t)

    def frac(self, f):
        w = self.resta() * f
        if w > 0.05:
            self.wait(w)

    def pills(self, textos, y0, col=MARCA, size=36, paso=0.85, fracs=None):
        g = VGroup()
        for k, t_ in enumerate(textos):
            c_ = col[k] if isinstance(col, (list, tuple)) else col
            p_ = pastilla(t_, c_, size, True).move_to([0, y0 - paso * k, 0])
            if p_.width > 8.2:
                p_.scale_to_fit_width(8.2)
            if fracs:
                self.frac(fracs[k])
            self.play(FadeIn(p_, shift=UP * 0.15), run_time=0.35)
            g.add(p_)
        return g

    def texto(self, l1, l2=None, y=3.6, c1=TINTA, c2=MARCA, s1=46, s2=62):
        g = VGroup(T(l1, s1, c1, "HEAVY"))
        if l2:
            g.add(T(l2, s2, c2, "HEAVY"))
        g.arrange(DOWN, buff=0.12).move_to([0, y, 0])
        if g.width > 8.4:
            g.scale_to_fit_width(8.4)
        return g

    def carta(self, codigo, texto, pos):
        cod = pastilla(codigo, MARCA, 30, True)
        lineas = VGroup(*[T(l, 30, TINTA, "MEDIUM") for l in texto.split("\n")]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        cuerpo = VGroup(cod, lineas).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        caja = tarjeta(max(7.6, cuerpo.width + 0.6), cuerpo.height + 0.5, color="#4A5AA0")
        cuerpo.move_to(caja)
        g = VGroup(caja, cuerpo).move_to(pos)
        if g.width > 8.5:
            g.scale_to_fit_width(8.5)
        return g

    def final(self, resumen=None):
        self.voz("cierre")
        objs = []
        if resumen:
            r = pastilla(resumen, MARCA, 38, True).move_to([0, 2.6, 0])
            if r.width > 8.2:
                r.scale_to_fit_width(8.2)
            self.play(FadeIn(r, scale=1.1), run_time=0.4)
            objs.append(r)
        logo = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(2.2)
        usuario = T("@miguelesquit", 44, MARCA, "HEAVY")
        bs = VGroup(pastilla("SUSCRÍBETE", ROJO, 42, True), pastilla("SÍGUEME", MARCA, 42, True)).arrange(RIGHT, buff=0.3)
        fin = Group(logo, usuario, bs).arrange(DOWN, buff=0.3).move_to([0, -1.0, 0])
        fondo_t = RoundedRectangle(width=7.6, height=fin.height + 0.8, corner_radius=0.3, stroke_color="#4A5AA0",
                                   stroke_width=2).set_fill(CARTA, 0.95).move_to(fin)
        self.sfx("ding", -10)
        self.play(FadeIn(fondo_t, scale=0.9), FadeIn(logo, scale=0.7), FadeIn(usuario), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=1.3) for b in bs], lag_ratio=0.4), run_time=0.6)
        self.cerrar_voz(2.2)

    def construct(self):
        self.add(encabezado(self.TIT1, self.TIT2))
        self.cuerpo()


# ====================================================================== V03 bolas de colores
class V03(ShortV):
    CLAVE = "v03"

    def cuerpo(self):
        self.voz("gancho")
        izq, der = P(-3.9, 2.6), P(3.9, 2.6)
        torres = VGroup(*[VGroup(Line(P(x, -1.2), P(x, 2.8)).set_stroke("#8C96A3", 8), Line(P(x - 0.6, 2.6), P(x + 0.6, 2.6)).set_stroke("#8C96A3", 6))
                          for x in (-3.9, 3.9)])
        lin = linea_aerea(izq, der, 0.45, "#B8BEC8", 4)
        cols = ["#F79009", WHITE, "#FDB022", "#F79009", WHITE]
        bolas = VGroup(*[esfera(cols[k], 0.3).move_to(lin.point_from_proportion(t)) for k, t in enumerate(np.linspace(0.12, 0.88, 5))])
        self.play(FadeIn(torres), Create(lin), run_time=0.7)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bolas], lag_ratio=0.2), run_time=1.2)
        no = pastilla("no son adornos", ROJO, 42, True).move_to([0, -2.4, 0])
        self.frac(0.4)
        self.play(FadeIn(no, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(no)

        self.voz("p1")
        rio = VGroup(Rectangle(width=9, height=1.3, stroke_width=0).set_fill("#1F6FB2", 0.8).move_to([0, -1.3, 0]),
                     *[onda(lambda x, k=k: 0.06 * np.sin(4 * x + k), -4.3, 4.3, -1.1 - 0.35 * k, 1, "#7FD1FF", 2) for k in range(3)])
        av = avioneta().scale(1.0).move_to([-5.5, 0.9, 0])
        self.play(FadeIn(rio), run_time=0.5)
        self.play(av.animate.move_to([1.6, 1.0, 0]), run_time=2.2, rate_func=linear)
        txt = pastilla("casi invisible desde el aire", TINTA2 if False else "#475467", 36, True).move_to([0, -3.3, 0])
        self.play(FadeIn(txt), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(av, txt)

        self.voz("p2")
        g = VGroup(esfera("#F79009", 1.0), esfera(WHITE, 0.6)).arrange(RIGHT, buff=1.2).move_to([0, -1.2, 0])
        self.play(FadeOut(rio), FadeIn(g[0], scale=0.5), run_time=0.6)
        m1 = T("≥ 91 cm", 50, "#F79009", "HEAVY").next_to(g[0], DOWN, buff=0.3)
        l1 = T("ríos, lagos, cañones", 28, CLARO, "BOLD").next_to(m1, DOWN, buff=0.1)
        self.play(FadeIn(m1), FadeIn(l1), run_time=0.4)
        self.frac(0.4)
        m2 = T("51 cm", 50, TINTA, "HEAVY").next_to(g[1], DOWN, buff=0.3).align_to(m1, UP)
        l2 = T("cerca de aeropuertos", 28, CLARO, "BOLD").next_to(m2, DOWN, buff=0.1)
        self.play(FadeIn(g[1], scale=0.5), FadeIn(m2), FadeIn(l2), run_time=0.5)
        faa = self.carta("FAA · AC 70/7460-1", "Marcadores esféricos en líneas\nque cruzan ríos y cañones.", [0, -4.3, 0])
        self.play(FadeIn(faa), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(g, m1, l1, m2, l2, faa)

        self.voz("p3")
        cols3 = VGroup(*[VGroup(esfera(c_, 0.55), T(n_, 30, TINTA, "BOLD")).arrange(DOWN, buff=0.2) for c_, n_ in
                         (("#F79009", "naranja"), (WHITE, "blanco"), ("#FDB022", "amarillo"))]).arrange(RIGHT, buff=0.7).move_to([0, -1.0, 0])
        self.play(LaggedStart(*[FadeIn(c_, scale=0.6) for c_ in cols3], lag_ratio=0.3), run_time=1.0)
        self.frac(0.45)
        cota = VGroup(DoubleArrow(bolas[1].get_center() + DOWN * 0.5, bolas[2].get_center() + DOWN * 0.5, buff=0, color=CLARO, stroke_width=3),
                      T("≈ 60 m", 34, CLARO, "HEAVY").move_to((bolas[1].get_center() + bolas[2].get_center()) / 2 + DOWN * 0.95))
        self.play(FadeIn(cota), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cols3, cota)

        self.voz("p4")
        av2 = avioneta().move_to([-5.5, 0.4, 0])
        self.play(av2.animate.move_to([0, 0.4, 0]), run_time=1.4, rate_func=rate_functions.ease_out_sine)
        self.play(av2.animate.shift(UP * 1.6 + RIGHT * 5.5).rotate(0.25), run_time=1.2)
        piloto = pastilla("para que el piloto vea el cable", VERDE_OK, 36, True).move_to([0, -2.4, 0])
        self.play(FadeIn(piloto, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(av2, piloto)

        self.voz("p5")
        espirales = VGroup(*[VMobject().set_points_smoothly([lin.point_from_proportion(t) + P(0.18 * np.sin(k), -0.1 * k) for k in np.linspace(0, 6 * PI, 30)])
                             .set_stroke("#FDB022", 4) for t in (0.3, 0.7)])
        p = pajarito().scale(1.4).move_to([0, -1.6, 0])
        self.play(Create(espirales), FadeIn(p, shift=LEFT * 0.4), run_time=0.8)
        aves = pastilla("espirales: estas sí son para las aves", "#B58900", 34, True).move_to([0, -3.4, 0])
        self.play(FadeIn(aves), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(espirales, p, aves, bolas, lin, torres)
        self.final("bolas = para los pilotos")


# ====================================================================== V04 zumbido
class V04(ShortV):
    CLAVE = "v04"

    def cuerpo(self):
        self.voz("gancho")
        pst = VGroup(Rectangle(width=0.5, height=7, stroke_width=0).set_fill("#8A6440", 1).move_to([-1.6, -0.5, 0]))
        tr = transformador().scale(1.9).move_to([-0.1, 0.4, 0])
        self.play(FadeIn(pst), FadeIn(tr, shift=UP * 0.2), run_time=0.6)
        ondas_ = VGroup(*[Arc(radius=0.5 + 0.35 * k, start_angle=-0.6, angle=1.2).set_stroke(MARCA, 4, 1 - 0.25 * k).move_to(tr.get_right() + RIGHT * (0.4 + 0.35 * k)) for k in range(3)])
        bz = T("bzzzz", 64, MARCA, "HEAVY").move_to([2.4, 2.6, 0])
        self.play(LaggedStart(*[Create(o) for o in ondas_], lag_ratio=0.3), FadeIn(bz), run_time=0.9)
        self.cerrar_voz(0.1)
        self.limpiar(pst, ondas_, bz)

        self.voz("p1")
        self.play(tr.animate.scale(0.5).move_to([-2.8, 3.0, 0]), run_time=0.5)
        nu = nucleo(7, 3.6, 2.6).move_to([0, 0.3, 0])
        lab = pastilla("núcleo de láminas de hierro", "#475467", 34, True).next_to(nu, DOWN, buff=0.4)
        self.play(FadeIn(nu), FadeIn(lab), run_time=0.5)
        self.frac(0.35)
        for _ in range(3):
            self.play(nu.animate.stretch(1.06, 0), run_time=0.25)
            self.play(nu.animate.stretch(1 / 1.06, 0), run_time=0.25)
        mg = pastilla("magnetostricción: se estira y se encoge", MARCA, 32, True).move_to([0, -3.0, 0])
        self.play(FadeIn(mg, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(nu, lab, mg, tr)

        self.voz("p2")
        ax1 = Line(P(-3.8, 1.6), P(3.8, 1.6)).set_stroke("#4A5AA0", 2)
        ax2 = Line(P(-3.8, -1.6), P(3.8, -1.6)).set_stroke("#4A5AA0", 2)
        w1 = onda(lambda x: np.sin(2 * PI * (x + 3.8) / 3.8), -3.8, 3.8, 1.6, 1.0, ROJO, 6)
        w2 = onda(lambda x: abs(np.sin(2 * PI * (x + 3.8) / 3.8)), -3.8, 3.8, -2.4, 1.6, MARCA, 6)
        e1 = T("corriente: 60 Hz", 34, ROJO, "HEAVY").move_to([0, 3.1, 0])
        e2 = T("estiramiento: 120 Hz", 34, MARCA, "HEAVY").move_to([0, -0.3, 0])
        self.play(Create(ax1), Create(w1), FadeIn(e1), run_time=1.0)
        self.frac(0.35)
        self.play(Create(ax2), Create(w2), FadeIn(e2), run_time=1.0)
        x2 = pastilla("el doble", VERDE_OK, 40, True).move_to([0, -4.3, 0])
        self.play(FadeIn(x2, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(ax1, ax2, w1, w2, e1, e2, x2)

        self.voz("p3")
        nu2 = nucleo(7, 3.0, 2.2).move_to([-1.8, 0.6, 0])
        aire = VGroup(*[Arc(radius=0.6 + 0.45 * k, start_angle=-0.7, angle=1.4).set_stroke(MARCA, 5, 1 - 0.2 * k).move_to([0.6 + 0.45 * k, 0.6, 0]) for k in range(4)])
        oreja = T("120 Hz", 70, MARCA, "HEAVY").move_to([2.5, -1.8, 0])
        self.play(FadeIn(nu2), run_time=0.4)
        self.play(LaggedStart(*[Create(a_) for a_ in aire], lag_ratio=0.25), FadeIn(oreja), run_time=1.0)
        self.cerrar_voz(0.1)
        self.limpiar(nu2, aire, oreja)

        self.voz("p4")
        ok = VGroup(check(VERDE_OK, 0.5), T("zumbido parejo: normal", 38, TINTA, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([0, 1.6, 0])
        mal = VGroup(equis(ROJO, 0.5), T("chasquidos o chispas", 38, TINTA, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([0, 0.0, 0])
        rep = pastilla("aléjate y repórtalo", ROJO, 40, True).move_to([0, -1.6, 0])
        self.play(FadeIn(ok, shift=UP * 0.15), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(mal, shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(rep, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(ok, mal, rep)

        self.voz("p5")
        tab = VGroup(VGroup(T("red", 34, CLARO, "BOLD"), T("zumbido", 34, CLARO, "BOLD")).arrange(RIGHT, buff=2.2),
                     VGroup(T("60 Hz", 50, TINTA, "HEAVY"), T("120 Hz", 50, MARCA, "HEAVY")).arrange(RIGHT, buff=1.5),
                     VGroup(T("50 Hz", 50, TINTA, "HEAVY"), T("100 Hz", 50, MARCA, "HEAVY")).arrange(RIGHT, buff=1.5)).arrange(DOWN, buff=0.5).move_to([0, 0.4, 0])
        caja = tarjeta(7.6, tab.height + 0.8, color="#4A5AA0").move_to(tab)
        self.play(FadeIn(caja), FadeIn(tab[0]), FadeIn(tab[1]), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(tab[2], shift=UP * 0.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(caja, tab)
        self.final("el hierro vibra al doble de la red")


# ====================================================================== V05 agujero más grande
def cara(escala=5.0, tierra=True):
    c = RoundedRectangle(width=0.38, height=0.36, corner_radius=0.13, stroke_color="#C7C5BE", stroke_width=1.6).set_fill("#FBFBF9", 1)
    fa = RoundedRectangle(width=0.035, height=0.1, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(P(0.08, 0.04))
    ne = RoundedRectangle(width=0.035, height=0.13, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(P(-0.08, 0.04))
    ti = VGroup(Arc(radius=0.035, start_angle=PI, angle=PI, stroke_width=0).set_fill("#2A2E35", 1),
                Rectangle(width=0.07, height=0.03, stroke_width=0).set_fill("#2A2E35", 1).shift(UP * 0.015)).move_to(P(0, -0.1))
    g = VGroup(c, fa, ne, ti if tierra else VGroup()).scale(escala)
    g.fa, g.ne, g.ti = fa, ne, ti
    return g


class V05(ShortV):
    CLAVE = "v05"

    def cuerpo(self):
        self.voz("gancho")
        cr = cara(9.0).move_to([0, 0.4, 0])
        self.play(FadeIn(cr, scale=0.8), run_time=0.6)
        self.frac(0.35)
        aros = VGroup(Circle(radius=0.75, stroke_color=ROJO, stroke_width=6).move_to(cr.ne), Circle(radius=0.6, stroke_color=MARCA, stroke_width=6).move_to(cr.fa))
        self.play(Create(aros), run_time=0.6)
        nf = pastilla("no es un error", ROJO, 40, True).move_to([0, -3.0, 0])
        self.play(FadeIn(nf, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(aros, nf)

        self.voz("p1")
        e = [(cr.fa, "FASE · pequeña", FASE, RIGHT), (cr.ne, "NEUTRO · grande", "#475467", LEFT), (cr.ti, "TIERRA · redonda", TIERRA, DOWN)]
        etq = VGroup()
        for obj, txt, col, lado in e:
            p_ = pastilla(txt, col, 32, True)
            if lado is DOWN:
                p_.move_to(obj.get_center() + DOWN * 1.6)
            else:
                p_.move_to([2.3 * lado[0], obj.get_center()[1] + 2.0, 0])
            ln = Line(obj.get_center(), p_.get_center(), stroke_color=CLARO, stroke_width=2)
            self.play(Create(ln), FadeIn(p_), run_time=0.4)
            etq.add(ln, p_)
            self.frac(0.2)
        self.cerrar_voz(0.1)
        self.limpiar(etq)

        self.voz("p2")
        self.play(cr.animate.scale(0.6).move_to([0, 2.2, 0]), run_time=0.5)
        cl = clavija("5-15P", True).scale(2.4).rotate(PI).move_to([0, -2.2, 0])
        self.play(FadeIn(cl, shift=UP * 0.3), run_time=0.5)
        ancha = Circle(radius=0.55, stroke_color=ROJO, stroke_width=5).move_to(cl.neu_p)
        self.play(Create(ancha), run_time=0.4)
        pol = pastilla("solo entra de una forma = POLARIDAD", MARCA, 32, True).move_to([0, -4.4, 0])
        self.frac(0.4)
        self.play(FadeIn(pol, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cl, ancha, pol, cr)

        self.voz("p3")
        f = foco_led(False, 0.9).scale(3.2).move_to([0, 0.8, 0])
        rosca = f[5][0]
        rl = pastilla("rosca = neutro", "#475467", 32, True).move_to([-2.2, -2.2, 0])
        cl_ = pastilla("centro = fase", FASE, 32, True).move_to([2.2, -2.2, 0])
        self.play(FadeIn(f), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(rl), Indicate(rosca, color=CLARO), FadeIn(cl_), run_time=0.7)
        seg = pastilla("tocar la rosca: menos peligroso", VERDE_OK, 32, True).move_to([0, -3.4, 0])
        self.frac(0.4)
        self.play(FadeIn(seg), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(f, rl, cl_, seg)

        self.voz("p4")
        t = tomacorriente(P(0, 0)).scale(4.0).move_to([0, 0.6, 0])
        self.play(FadeIn(t), run_time=0.5)
        pl = pastilla("plateado → neutro", "#475467", 32, True).move_to([-2.0, -2.4, 0])
        la = pastilla("latón → fase", "#8A6D12", 32, True).move_to([2.2, -2.4, 0])
        self.play(Indicate(t.p1, color=WHITE, scale_factor=1.6), FadeIn(pl), run_time=0.6)
        self.play(Indicate(t.l1, color=AMBAR, scale_factor=1.6), FadeIn(la), run_time=0.6)
        nec = self.carta("NEC 2020 · 200.10(B)", "El terminal del neutro\nse identifica: plateado.", [0, -3.9, 0])
        self.play(FadeIn(nec), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(t, pl, la, nec)

        self.voz("p5")
        f2 = foco_led(False, 0.9).scale(2.6).move_to([0, 1.2, 0])
        mal = pastilla("tomacorriente al revés", ROJO, 34, True).move_to([0, -1.2, 0])
        rayo_ = simbolo_rayo(AMBAR, 0.9).move_to(f2[5].get_center() + RIGHT * 1.2)
        self.play(FadeIn(f2), FadeIn(mal), run_time=0.5)
        self.play(FadeIn(rayo_, scale=1.3), Indicate(f2[5], color=ROJO), run_time=0.6)
        pr = pastilla("revísalo con un probador", VERDE_OK, 34, True).move_to([0, -2.6, 0])
        self.frac(0.4)
        self.play(FadeIn(pr), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(f2, mal, rayo_, pr)
        self.final("ranura grande = neutro")


# ====================================================================== V06 pata más larga
class V06(ShortV):
    CLAVE = "v06"

    def cuerpo(self):
        self.voz("gancho")
        cl = clavija("5-15P", True).scale(3.4).rotate(PI).move_to([0, 0.0, 0])
        self.play(FadeIn(cl, scale=0.8), run_time=0.6)
        self.frac(0.4)
        y_t, y_f = cl.tie_p.get_bottom()[1], cl.fase_p.get_bottom()[1]
        cota = VGroup(DashedLine(P(-3.2, y_t), P(3.2, y_t), color=ROJO, stroke_width=3),
                      DashedLine(P(-3.2, y_f), P(3.2, y_f), color=CLARO, stroke_width=3))
        self.play(Create(cota), Indicate(cl.tie_p, color=VERDE_OK), run_time=0.8)
        q = pastilla("¿por qué más larga?", MARCA, 40, True).move_to([0, -4.0, 0])
        self.play(FadeIn(q), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cota, q)

        self.voz("p1")
        self.play(cl.animate.scale(0.75).move_to([0, 2.6, 0]), run_time=0.5)
        t = cara(7.0).move_to([0, -1.8, 0])
        self.play(FadeIn(t), run_time=0.4)
        self.frac(0.2)
        self.play(cl.animate.shift(DOWN * 1.15), run_time=1.0)
        c1 = pastilla("1° tierra", VERDE_OK, 36, True).move_to([2.6, 0.9, 0])
        self.play(FadeIn(c1, scale=1.2), Flash(cl.tie_p.get_bottom(), color=VERDE_OK), run_time=0.5)
        self.cerrar_voz(0.1)

        self.voz("p2")
        self.play(cl.animate.shift(DOWN * 0.45), run_time=0.8)
        c2 = pastilla("2° fase y neutro", MARCA, 36, True).move_to([2.6, 0.1, 0])
        self.play(FadeIn(c2, scale=1.2), run_time=0.4)
        txt = pastilla("la carcasa ya está protegida", VERDE_OK, 34, True).move_to([0, -4.3, 0])
        self.frac(0.3)
        self.play(FadeIn(txt), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(c1, c2, txt)

        self.voz("p3")
        self.play(cl.animate.shift(UP * 0.45), run_time=0.8)
        u1 = pastilla("se sueltan fase y neutro", MARCA, 34, True).move_to([0, 3.9, 0])
        self.play(FadeIn(u1), run_time=0.3)
        self.frac(0.3)
        self.play(cl.animate.shift(UP * 1.15), run_time=0.8)
        u2 = pastilla("la tierra, de última", VERDE_OK, 36, True).move_to([0, -4.3, 0])
        self.play(FadeIn(u2), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(u1, u2, t)

        self.voz("p4")
        self.play(cl.animate.scale(1.2).move_to([0, 0.6, 0]), run_time=0.5)
        corte = Line(cl.tie_p.get_left() + LEFT * 0.3 + DOWN * 0.1, cl.tie_p.get_right() + RIGHT * 0.3 + UP * 0.1).set_stroke(ROJO, 8)
        pinza = pinza_icono(False).scale(1.4).rotate(-0.6).move_to(cl.tie_p.get_center() + RIGHT * 1.6)
        self.play(FadeIn(pinza), run_time=0.4)
        x = equis(ROJO, 0.9).move_to(cl.tie_p)
        self.play(Create(corte), FadeIn(x, scale=1.3), run_time=0.5)
        nunca = pastilla("nunca le cortes la tierra", ROJO, 40, True).move_to([0, -3.3, 0])
        self.play(FadeIn(nunca, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cl, corte, pinza, x, nunca)

        self.voz("p5")
        t3 = cara(6.5).move_to([0, 1.2, 0])
        sin = VGroup(Circle(radius=0.6, stroke_color=ROJO, stroke_width=6).move_to(t3.ti), T("sin cable verde", 34, ROJO, "HEAVY").move_to([0, -1.4, 0]))
        self.play(FadeIn(t3), run_time=0.4)
        self.frac(0.25)
        self.play(Create(sin[0]), FadeIn(sin[1]), run_time=0.5)
        eng = pastilla("parece seguro, pero no lo es", ROJO, 36, True).move_to([0, -2.8, 0])
        self.play(FadeIn(eng), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(t3, sin, eng)
        self.final("tierra: primero en entrar, último en salir")


# ====================================================================== V07 ducha
class V07(ShortV):
    CLAVE = "v07"

    def cuerpo(self):
        self.voz("gancho")
        d = ducha().scale(1.6).move_to([0, 2.0, 0])
        ag = gotas(d[2].get_center() + DOWN * 0.6, 11).scale(1.6)
        self.play(FadeIn(d), FadeIn(ag), run_time=0.6)
        llave = VGroup(RoundedRectangle(width=0.6, height=0.6, corner_radius=0.2, stroke_width=2, stroke_color="#98A2B3").set_fill("#E4E7EC", 1),
                       Rectangle(width=1.0, height=0.16, stroke_width=0).set_fill("#B8BEC8", 1)).move_to([2.6, -1.0, 0])
        mano = Circle(radius=0.32, stroke_width=0).set_fill(PIEL if False else "#E0A47A", 1).move_to([3.4, -1.0, 0])
        self.play(FadeIn(llave), FadeIn(mano), run_time=0.4)
        self.frac(0.3)
        toque = VGroup(*[rayo(mano.get_center(), mano.get_center() + 0.9 * np.array([np.cos(a), np.sin(a), 0]), AMBAR, 5, 0.1, k, 3) for k, a in enumerate(np.linspace(0, TAU, 6, endpoint=False))])
        self.sfx("pop", -6)
        self.play(FadeIn(toque, scale=0.5), run_time=0.3)
        q = pastilla("¡toque!", ROJO, 46, True).move_to([0, -3.0, 0])
        self.play(FadeIn(q, scale=1.3), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(llave, mano, toque, q)

        self.voz("p1")
        res = VMobject().set_points_as_corners([d[1].get_left() + RIGHT * 0.3 + DOWN * 0.1 + RIGHT * 0.25 * k + (UP * 0.2 if k % 2 else DOWN * 0.2) for k in range(9)]).set_stroke(ROJO, 6)
        self.play(Create(res), run_time=0.6)
        rr = pastilla("resistencia que calienta el agua", ROJO, 32, True).move_to([0, -0.4, 0])
        self.play(FadeIn(rr), run_time=0.4)
        self.frac(0.35)
        falla = pastilla("si falla el aislamiento: agua y metal con voltaje", AMBAR, 28, True).move_to([0, -1.6, 0])
        self.play(FadeIn(falla), ag.animate.set_color(AMBAR), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(rr, falla, res)

        self.voz("p2")
        sin = pastilla("SIN tierra", ROJO, 40, True).move_to([0, -0.5, 0])
        cuerpo_ = VGroup(Circle(radius=0.35, stroke_width=0).set_fill("#E0A47A", 1).move_to([0, -1.6, 0]),
                         RoundedRectangle(width=1.0, height=1.8, corner_radius=0.3, stroke_width=0).set_fill("#E0A47A", 1).move_to([0, -3.0, 0]))
        cam = corriente([P(0, -0.2), P(0, -1.6), P(0, -3.0), P(0, -4.2)], vel=1.2, color=ROJO, escala=2.5)
        piso = Line(P(-3, -4.2), P(3, -4.2)).set_stroke("#4A5AA0", 4)
        self.play(FadeIn(sin), FadeIn(cuerpo_), Create(piso), run_time=0.5)
        self.frac(0.25)
        self.add(cam)
        tc = pastilla("la corriente busca tu cuerpo", ROJO, 32, True).move_to([0, 0.5, 0])
        self.play(FadeIn(tc), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(sin, cuerpo_, cam, piso, tc)

        self.voz("p3")
        bk = breaker("40", 0.46, 0.26).scale(5.0).move_to([2.2, -2.6, 0])
        tierra_c = VMobject().set_points_smoothly([d[1].get_right(), P(2.2, 0.6), P(1.4, -1.6), bk.get_left()]).set_stroke(TIERRA, 10)
        self.play(Create(tierra_c), FadeIn(bk), run_time=0.8)
        fl = corriente([d[1].get_right(), P(2.2, 0.6), P(1.4, -1.6), bk.get_left()], vel=1.4, escala=2.4)
        self.add(fl)
        con = pastilla("CON tierra: la falla regresa al tablero", VERDE_OK, 30, True).move_to([0, -0.4, 0])
        self.play(FadeIn(con), run_time=0.4)
        self.frac(0.4)
        self.sfx("tic", -2)
        self.play(mover_palanca(bk, False), Flash(bk, color=AMBAR), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(tierra_c, bk, fl, con)

        self.voz("p4")
        nec = self.carta("NEC 2020 · 250.110", "Las partes de metal de un equipo fijo\nque pueden energizarse van a tierra.", [0, -0.6, 0])
        self.play(FadeIn(nec), run_time=0.4)
        self.frac(0.45)
        bj = pastilla("si da toques: baja el breaker y no la uses", ROJO, 30, True).move_to([0, -2.8, 0])
        self.play(FadeIn(bj, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(nec, bj)

        self.voz("p5")
        pan = centro_carga().scale(0.9).move_to([2.4, -1.5, 0])
        ok = VMobject().set_points_smoothly([d[1].get_right(), P(1.8, 0.8), P(1.6, -0.5), pan.tt.get_center()]).set_stroke(TIERRA, 8)
        mal = VMobject().set_points_smoothly([d[1].get_left(), P(-2.2, 0.6), P(-2.6, -1.5)]).set_stroke(TIERRA, 8)
        xm = equis(ROJO, 0.4).move_to([-2.6, -1.8, 0])
        self.play(FadeIn(pan), Create(ok), run_time=0.7)
        ch = check(VERDE_OK, 0.4).move_to(pan.get_top() + UP * 0.4)
        self.play(FadeIn(ch), run_time=0.3)
        self.frac(0.3)
        self.play(Create(mal), FadeIn(xm), run_time=0.5)
        sl = pastilla("suelto en la pared: no sirve", ROJO, 32, True).move_to([-1.2, -3.6, 0])
        self.play(FadeIn(sl), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(pan, ok, mal, xm, ch, sl, d, ag)
        self.final("tierra hasta el tablero = sin toques")


# ====================================================================== V08 número del breaker
class V08(ShortV):
    CLAVE = "v08"

    def cuerpo(self):
        self.voz("gancho")
        bks = VGroup(*[breaker(n, 0.46, 0.26).scale(6.5) for n in ("15", "20", "30")]).arrange(DOWN, buff=0.4).move_to([0, 0.3, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in bks], lag_ratio=0.3), run_time=1.0)
        q = pastilla("¿qué significa el número?", MARCA, 38, True).move_to([0, -3.0, 0])
        self.frac(0.3)
        self.play(FadeIn(q), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(q)

        self.voz("p1")
        self.play(bks[0].animate.scale(0.6).move_to([-2.6, 2.8, 0]), bks[1].animate.scale(0.6).move_to([0, 2.8, 0]), bks[2].animate.scale(0.6).move_to([2.6, 2.8, 0]), run_time=0.5)
        a = VGroup(T("amperios", 54, MARCA, "HEAVY"), T("corriente máxima", 34, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, 0.6, 0])
        self.play(FadeIn(a), run_time=0.4)
        medidor = VGroup(RoundedRectangle(width=6.0, height=0.5, corner_radius=0.25, stroke_color="#4A5AA0", stroke_width=2).set_fill(CARTA, 1)).move_to([0, -1.5, 0])
        barra = RoundedRectangle(width=0.1, height=0.4, corner_radius=0.2, stroke_width=0).set_fill(VERDE_OK, 1).align_to(medidor, LEFT).shift(RIGHT * 0.05).set_y(-1.5)
        self.play(FadeIn(medidor), FadeIn(barra), run_time=0.3)
        self.play(barra.animate.stretch_to_fit_width(5.9).align_to(medidor, LEFT).shift(RIGHT * 0.05).set_fill(ROJO), run_time=1.4)
        self.sfx("tic", -2)
        self.play(mover_palanca(bks[0], False), Flash(bks[0], color=AMBAR), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(a, medidor, barra)

        self.voz("p2")
        cab = cable_hilos(6.5, FASE, 0.6, 0.6).move_to([0, 0.2, 0])
        cab[2].set_stroke("#8F9AC8", 2)
        self.play(FadeIn(cab), run_time=0.4)
        prot = pastilla("protege al CABLE", MARCA, 44, True).move_to([0, -1.4, 0])
        self.play(FadeIn(prot, scale=1.2), run_time=0.4)
        self.frac(0.35)
        calor = resplandor(cab.get_center(), 2.0, ROJO, 10, 0.05).stretch(2.4, 0)
        sc = T("sin sobrecalentarse", 36, CLARO, "BOLD").move_to([0, -2.6, 0])
        self.play(FadeIn(calor), FadeIn(sc), run_time=0.6)
        self.play(FadeOut(calor), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cab, prot, sc)

        self.voz("p3")
        filas = VGroup(*[VGroup(cable_hilos(2.6, FASE, w, 0.4), T(c_, 44, TINTA, "HEAVY"), T("→", 44, CLARO, "HEAVY"), pastilla(a_, VERDE_OK, 40, True)).arrange(RIGHT, buff=0.35)
                         for w, c_, a_ in ((0.32, "14 AWG", "15 A"), (0.42, "12 AWG", "20 A"))]).arrange(DOWN, buff=0.7).move_to([0, 0.3, 0])
        for f in filas:
            f[0][2].set_stroke("#8F9AC8", 2)
            self.play(FadeIn(f, shift=UP * 0.15), run_time=0.5)
            self.frac(0.25)
        nec = self.carta("NEC 2020 · 240.4(D)", "Cobre 14 AWG → 15 A\nCobre 12 AWG → 20 A", [0, -2.4, 0])
        self.play(FadeIn(nec), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(filas, nec)

        self.voz("p4")
        r = VGroup(bks[0].copy().scale(1.4), T("=", 70, CLARO, "HEAVY"), T("cable 14", 56, MARCA, "HEAVY")).arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        self.play(FadeIn(r), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(r)

        self.voz("p5")
        ter = VGroup(T("térmica", 50, AMBAR, "HEAVY"), T("sobrecarga · poco a poco", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, 0.6, 0])
        mag = VGroup(T("magnética", 50, MARCA, "HEAVY"), T("cortocircuito · al instante", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, -1.4, 0])
        self.play(FadeIn(ter, shift=UP * 0.15), run_time=0.4)
        self.frac(0.4)
        self.play(FadeIn(mag, shift=UP * 0.15), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(ter, mag, bks)
        self.final("el número protege al cable")


# ====================================================================== V09 breaker más grande
class V09(ShortV):
    CLAVE = "v09"

    def cuerpo(self):
        self.voz("gancho")
        b15 = breaker("15", 0.46, 0.26).scale(6.5).move_to([-2.1, 0.8, 0])
        b30 = breaker("30", 0.46, 0.26).scale(6.5).move_to([2.1, 0.8, 0])
        flecha = Arrow(P(-0.5, 0.8), P(0.5, 0.8), color=CLARO)
        self.play(FadeIn(b15), run_time=0.4)
        self.frac(0.35)
        self.play(GrowArrow(flecha), FadeIn(b30), run_time=0.5)
        no = VGroup(equis(ROJO, 0.7).move_to(b30)), pastilla("¡NO!", ROJO, 50, True).move_to([0, -2.0, 0])
        self.play(FadeIn(no[0], scale=1.3), FadeIn(no[1], scale=1.3), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(b15, b30, flecha, *no)

        self.voz("p1")
        filas = VGroup(*[VGroup(T(c_, 46, TINTA, "HEAVY"), T("→", 46, CLARO, "HEAVY"), pastilla(a_, VERDE_OK, 42, True)).arrange(RIGHT, buff=0.35)
                         for c_, a_ in (("cable 14", "15 A"), ("cable 12", "20 A"))]).arrange(DOWN, buff=0.6).move_to([0, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(f) for f in filas], lag_ratio=0.5), run_time=1.0)
        self.cerrar_voz(0.1)
        self.limpiar(filas)

        self.voz("p2")
        cab = cable_hilos(6.0, FASE, 0.5, 0.5).move_to([0, 2.2, 0])
        cab[2].set_stroke("#8F9AC8", 2)
        t14 = T("cable 14 + breaker 30", 38, ROJO, "HEAVY").move_to([0, 3.3, 0])
        self.play(FadeIn(cab), FadeIn(t14), run_time=0.4)
        f1 = MathTex(r"2\times I \;\Rightarrow\; 4\times \text{calor}", color=TINTA).scale(1.6).move_to([0, 0.4, 0])
        jou = MathTex(r"P = I^2 \times R", color=MARCA).scale(1.4).move_to([0, -1.0, 0])
        self.frac(0.35)
        self.play(Write(jou), run_time=0.6)
        self.play(Write(f1), run_time=0.6)
        calor = resplandor(cab.get_center(), 2.0, ROJO, 12, 0.06).stretch(2.2, 0)
        self.play(FadeIn(calor), run_time=0.6)
        self.cerrar_voz(0.1)
        self.limpiar(f1, jou, t14)

        self.voz("p3")
        humo = VGroup(*[VMobject().set_points_smoothly([P(x, 2.6), P(x + 0.2, 3.1), P(x - 0.15, 3.6), P(x + 0.1, 4.1)]).set_stroke("#98A2B3", 5, 0.8) for x in (-1.2, 0, 1.2)])
        self.play(Create(humo), cab[2].animate.set_fill("#5A3A1A"), run_time=0.8)
        inc = pastilla("riesgo de incendio dentro de la pared", ROJO, 32, True).move_to([0, -0.6, 0])
        self.play(FadeIn(inc, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cab, calor, humo, inc)

        self.voz("p4")
        tr = pastilla("si se dispara, está haciendo su trabajo", VERDE_OK, 30, True).move_to([0, 2.2, 0])
        self.play(FadeIn(tr), run_time=0.4)
        self.frac(0.3)
        sol = self.pills(["repartir las cargas", "circuito nuevo con su cable"], 0.4, MARCA, 36, 0.9, [0.0, 0.25])
        self.cerrar_voz(0.1)
        self.limpiar(tr, sol)

        self.voz("p5")
        b = breaker("20", 0.46, 0.26, on=False).scale(8.0).move_to([0, 1.2, 0])
        self.play(FadeIn(b), run_time=0.4)
        cc = pastilla("se dispara al subirlo = posible corto", ROJO, 30, True).move_to([0, -1.2, 0])
        self.play(FadeIn(cc), run_time=0.4)
        self.frac(0.3)
        bf = pastilla("no lo fuerces: busca la falla", AMBAR, 34, True).move_to([0, -2.4, 0])
        self.play(FadeIn(bf), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(b, cc, bf)
        self.final("el breaker va con el cable")


# ====================================================================== V10 alta tensión sin forro
class V10(ShortV):
    CLAVE = "v10"

    def cuerpo(self):
        self.voz("gancho")
        cab = cable_hilos(3.6, FASE, 0.5, 0.6).move_to([-1.8, 2.4, 0])
        cab[2].set_stroke("#8F9AC8", 2)
        casa = T("tu casa: con forro", 32, TINTA, "BOLD").next_to(cab, DOWN, buff=0.25)
        pg, _ = poste(7.0, 4.6, 2)
        pg.scale(0.95).move_to([1.4, -1.4, 0])
        post = T("poste: desnudos", 32, MARCA, "BOLD").move_to([1.8, -4.6, 0])
        self.play(FadeIn(cab), FadeIn(casa), run_time=0.5)
        self.frac(0.25)
        self.play(FadeIn(pg, shift=UP * 0.3), FadeIn(post), run_time=0.6)
        self.cerrar_voz(0.1)
        self.limpiar(cab, casa, post)

        self.voz("p1")
        self.play(pg.animate.move_to([0, -0.6, 0]).scale(1.15), run_time=0.5)
        aire = pastilla("el aislante es el AIRE", MARCA, 40, True).move_to([0, 3.4, 0])
        self.play(FadeIn(aire, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(aire)

        self.voz("p2")
        ais = aislador_pin(P(0, 0), 0.42).scale(6.5).move_to([0, 0.6, 0])
        self.play(FadeOut(pg), FadeIn(ais, scale=0.8), run_time=0.6)
        ta = pastilla("aislador de porcelana o polímero", "#475467", 32, True).move_to([0, -2.6, 0])
        self.play(FadeIn(ta), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(ais, ta)

        self.voz("p3")
        grueso = VGroup(Circle(radius=1.5, stroke_color="#8F9AC8", stroke_width=3).set_fill("#2A2E35", 1), Circle(radius=0.6, stroke_width=2, stroke_color="#8C96A3").set_fill("#B8BEC8", 1)).move_to([-1.9, 1.0, 0])
        desn = Circle(radius=0.6, stroke_width=2, stroke_color="#8C96A3").set_fill("#B8BEC8", 1).move_to([1.9, 1.0, 0])
        t1 = T("con forro:\ngrueso y pesado", 30, ROJO, "BOLD").next_to(grueso, DOWN, buff=0.3)
        t2 = T("desnudo:\nliviano, se enfría", 30, VERDE_OK, "BOLD").next_to(desn, DOWN, buff=0.3).align_to(t1, UP)
        self.play(FadeIn(grueso), FadeIn(t1), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(desn), FadeIn(t2), run_time=0.5)
        exc = pastilla("con forro existen, pero son la excepción", "#475467", 30, True).move_to([0, -2.6, 0])
        self.frac(0.4)
        self.play(FadeIn(exc), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(grueso, desn, t1, t2, exc)

        self.voz("p4")
        nt = pastilla("ese forro NO te protegería", ROJO, 40, True).move_to([0, 1.0, 0])
        al = pastilla("nunca toques ni te acerques", ROJO, 36, True).move_to([0, -0.4, 0])
        self.play(FadeIn(nt, scale=1.1), run_time=0.4)
        self.frac(0.4)
        self.play(FadeIn(al), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(nt, al)

        self.voz("p5")
        objs = VGroup(escalera(3.0, 0.7), piscucha().scale(1.2)).arrange(RIGHT, buff=1.4).move_to([0, 0.8, 0])
        self.play(LaggedStart(*[FadeIn(o) for o in objs], lag_ratio=0.4), run_time=0.8)
        d = pastilla("la distancia es tu protección", VERDE_OK, 36, True).move_to([0, -2.4, 0])
        self.frac(0.35)
        self.play(FadeIn(d), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(objs, d)
        self.final("alta tensión: el aire es el aislante")


# ====================================================================== V11 LED
class V11(ShortV):
    CLAVE = "v11"

    def cuerpo(self):
        self.voz("gancho")
        viejo = VGroup(foco_led(True, 0.9)[0].copy(), foco_led(True, 0.9)[5].copy()).scale(2.6).move_to([-2.0, 1.0, 0])
        led = foco_led(True, 0.9).scale(2.6).move_to([2.0, 1.0, 0])
        g1, g2 = resplandor(viejo[0].get_center(), 1.4, AMBAR, 10, 0.05), resplandor(led[0].get_center(), 1.4, AMBAR, 10, 0.05)
        self.play(FadeIn(g1), FadeIn(viejo), FadeIn(g2), FadeIn(led), run_time=0.6)
        w1 = T("60 W", 50, ROJO, "HEAVY").next_to(viejo, DOWN, buff=0.4)
        w2 = T("9 W", 50, VERDE_OK, "HEAVY").next_to(led, DOWN, buff=0.4).align_to(w1, UP)
        self.frac(0.3)
        self.play(FadeIn(w1), FadeIn(w2), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(w1, w2, g2, led)

        self.voz("p1")
        self.play(viejo.animate.move_to([0, 1.0, 0]), g1.animate.move_to([0, 1.4, 0]), run_time=0.5)
        fil = VMobject().set_points_as_corners([P(-0.4, 1.1), P(-0.2, 1.4), P(0, 1.1), P(0.2, 1.4), P(0.4, 1.1)]).set_stroke("#FFE08A", 6)
        self.play(Create(fil), run_time=0.4)
        calor = resplandor(viejo.get_center(), 2.6, ROJO, 12, 0.05)
        bar = VGroup(Rectangle(width=6.0, height=0.5, stroke_width=0).set_fill(ROJO, 1), Rectangle(width=0.6, height=0.5, stroke_width=0).set_fill(AMBAR, 1)).arrange(RIGHT, buff=0).move_to([0, -2.4, 0])
        lb = VGroup(T("calor", 30, ROJO, "HEAVY").next_to(bar[0], DOWN, buff=0.15), T("luz", 30, AMBAR, "HEAVY").next_to(bar[1], DOWN, buff=0.15))
        self.frac(0.25)
        self.play(FadeIn(calor), GrowFromEdge(bar, LEFT), FadeIn(lb), run_time=0.8)
        self.cerrar_voz(0.1)
        self.limpiar(viejo, fil, g1, calor, bar, lb)

        self.voz("p2")
        led2 = foco_led(True, 0.9).scale(3.0).move_to([0, 1.2, 0])
        chip = VGroup(*[Square(0.35, stroke_width=0).set_fill("#FFD34D", 1) for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to([0, -1.2, 0])
        self.play(FadeIn(led2), run_time=0.4)
        sem = pastilla("semiconductor: luz directa", MARCA, 36, True).move_to([0, -2.4, 0])
        self.play(FadeIn(chip), FadeIn(sem), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(chip, sem)

        self.voz("p3")
        self.play(led2.animate.scale(0.6).move_to([0, 3.0, 0]), run_time=0.4)
        n1 = VGroup(T("75 %", 110, VERDE_OK, "HEAVY"), T("menos energía (mínimo)", 32, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, 0.5, 0])
        n2 = VGroup(T("25×", 100, MARCA, "HEAVY"), T("más vida (hasta)", 32, TINTA, "BOLD")).arrange(DOWN, buff=0.1).move_to([0, -2.1, 0])
        self.frac(0.25)
        self.play(FadeIn(n1, scale=1.1), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(n2, scale=1.1), run_time=0.5)
        src = fuente("U.S. Department of Energy · Energy Saver", [0, -4.0, 0], 26)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(n1, n2, src, led2)

        self.voz("p4")
        eq = VGroup(T("9 W", 80, VERDE_OK, "HEAVY"), T("≈", 80, CLARO, "HEAVY"), T("60 W", 80, ROJO, "HEAVY")).arrange(RIGHT, buff=0.4).move_to([0, 0.8, 0])
        self.play(FadeIn(eq), run_time=0.5)
        rec = pastilla("se nota en el recibo", VERDE_OK, 40, True).move_to([0, -1.2, 0])
        self.frac(0.35)
        self.play(FadeIn(rec, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(eq, rec)

        self.voz("p5")
        ter = VGroup(T("menos calor", 54, MARCA, "HEAVY"), T("en la lámpara y en el cuarto", 32, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, 0.6, 0])
        self.play(FadeIn(ter), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(ter)
        self.final("LED: casi toda la energía se vuelve luz")


# ====================================================================== V12 corriente que mata
class V12(ShortV):
    CLAVE = "v12"

    def barra_ma(self):
        niveles = [("1 mA", "cosquilleo", VERDE_OK), ("6–16 mA", "no te puedes soltar", AMBAR),
                   ("17–99 mA", "paro respiratorio", "#F97316"), ("≥ 100 mA", "fibrilación del corazón", ROJO)]
        filas = VGroup()
        for ma, ef, col in niveles:
            caja = RoundedRectangle(width=8.0, height=1.05, corner_radius=0.18, stroke_color=col, stroke_width=3).set_fill(col, 0.16)
            t1 = T(ma, 40, col, "HEAVY").move_to(caja.get_left() + RIGHT * 1.35)
            t2 = T(ef, 32, TINTA, "BOLD").move_to(caja.get_center() + RIGHT * 1.3)
            filas.add(VGroup(caja, t1, t2))
        return filas.arrange(DOWN, buff=0.25).move_to([0, 0.0, 0])

    def cuerpo(self):
        self.voz("gancho")
        v = T("voltaje", 60, CLARO, "HEAVY").move_to([0, 2.6, 0])
        i = T("CORRIENTE", 80, ROJO, "HEAVY").move_to([0, 0.6, 0])
        self.play(FadeIn(v), run_time=0.4)
        self.frac(0.25)
        tacha = Line(v.get_left(), v.get_right()).set_stroke(ROJO, 6)
        self.play(Create(tacha), FadeIn(i, scale=1.2), run_time=0.6)
        muy = pastilla("hace falta MUY poca", ROJO, 40, True).move_to([0, -1.4, 0])
        self.frac(0.45)
        self.play(FadeIn(muy), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(v, i, tacha, muy)
        filas = self.barra_ma()
        for k in range(4):
            self.voz(["p1", "p2", "p3", "p3"][k]) if k < 3 else None
            if k == 3:
                self.frac(0.45)
            self.play(FadeIn(filas[k], shift=RIGHT * 0.3), run_time=0.5)
            if k in (0, 1):
                self.cerrar_voz(0.1)
        self.cerrar_voz(0.1)

        self.voz("p4")
        self.play(filas.animate.scale(0.75).move_to([0, 1.6, 0]), run_time=0.5)
        f = foco_led(True, 0.9).scale(1.6).move_to([-2.4, -2.2, 0])
        tf = VGroup(T("foco LED 9 W", 32, TINTA, "BOLD"), T("≈ 75 mA", 54, ROJO, "HEAVY")).arrange(DOWN, buff=0.1).move_to([1.2, -2.2, 0])
        self.play(FadeIn(f), FadeIn(tf), run_time=0.5)
        src = fuente("OSHA / NIOSH · choque de 60 Hz, mano-pie, 1 s", [0, -4.2, 0], 24)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(filas, f, tf, src)

        self.voz("p5")
        f1 = MathTex(r"I = \dfrac{V}{R}", color=TINTA).scale(2.0).move_to([0, 1.6, 0])
        self.play(Write(f1), run_time=0.6)
        g = pastilla("más voltaje → más corriente por tu cuerpo", AMBAR, 30, True).move_to([0, -0.4, 0])
        self.play(FadeIn(g), run_time=0.4)
        self.frac(0.35)
        mj = pastilla("piel mojada = menos resistencia", ROJO, 34, True).move_to([0, -1.7, 0])
        self.play(FadeIn(mj), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(f1, g, mj)
        self.final("respeta siempre la electricidad")


# ====================================================================== V13 cable se calienta
class V13(ShortV):
    CLAVE = "v13"

    def cuerpo(self):
        self.voz("gancho")
        cab = cable_hilos(7.0, FASE, 0.7, 0.8).move_to([0, 1.0, 0])
        cab[2].set_stroke("#8F9AC8", 2)
        fl = corriente([cab[2].get_left() + RIGHT * 0.3, cab[2].get_right() + RIGHT * 0.8], vel=1.2, escala=2.6)
        self.play(FadeIn(cab), run_time=0.4)
        self.add(fl)
        calor = resplandor(cab.get_center(), 1.8, ROJO, 12, 0.05).stretch(2.4, 0)
        self.frac(0.3)
        self.play(FadeIn(calor), run_time=0.8)
        tib = pastilla("está tibio... ¿por qué?", AMBAR, 38, True).move_to([0, -1.6, 0])
        self.play(FadeIn(tib), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(tib)

        self.voz("p1")
        r = pastilla("el cobre tiene una pequeña resistencia", MARCA, 32, True).move_to([0, -1.2, 0])
        self.play(FadeIn(r), run_time=0.4)
        self.frac(0.35)
        e = pastilla("energía → calor", ROJO, 38, True).move_to([0, -2.4, 0])
        self.play(FadeIn(e), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(r, e)

        self.voz("p2")
        f = MathTex(r"P", r"=", r"I^2", r"\times", r"R", color=TINTA).scale(2.4).move_to([0, -1.0, 0])
        f[2].set_color(ROJO)
        self.play(Write(f), run_time=0.8)
        self.frac(0.35)
        ej = VGroup(T("2× corriente", 44, TINTA, "HEAVY"), T("→", 44, CLARO, "HEAVY"), T("4× calor", 50, ROJO, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([0, -3.0, 0])
        self.play(FadeIn(ej), calor.animate.scale(1.4), run_time=0.6)
        self.cerrar_voz(0.1)
        self.limpiar(f, ej)

        self.voz("p3")
        filas = VGroup(VGroup(T("12 AWG cobre", 34, TINTA, "HEAVY"), T("60 °C: 20 A", 32, CLARO, "BOLD"), T("75 °C: 25 A", 32, CLARO, "BOLD"), T("90 °C: 30 A", 32, CLARO, "BOLD")).arrange(DOWN, buff=0.15)).move_to([0, -1.6, 0])
        nec = self.carta("NEC 2020 · Tabla 310.16", "Corriente máxima según el calibre\ny la temperatura del aislamiento.", [0, -3.9, 0])
        self.play(FadeIn(filas), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(nec), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(filas, nec)

        self.voz("p4")
        adv = pastilla("cable caliente = corriente de más", ROJO, 36, True).move_to([0, -1.4, 0])
        self.play(FadeIn(adv, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(adv, cab, fl, calor)

        self.voz("p5")
        tubo_ = RoundedRectangle(width=7.4, height=2.2, corner_radius=0.3, stroke_color=METAL_OSC, stroke_width=3).set_fill(METAL, 0.15).move_to([0, 1.2, 0])
        cs = VGroup(*[cable_hilos(7.0, col, 0.32, 0.0) for col in (FASE, ROJO, RET_AZUL if "RET_AZUL" in globals() else "#1570EF", NEUTRO, FASE, ROJO)]).arrange(DOWN, buff=0.03).move_to(tubo_)
        self.play(FadeIn(tubo_), FadeIn(cs), run_time=0.5)
        cal = resplandor(tubo_.get_center(), 2.0, ROJO, 10, 0.05).stretch(2.2, 0)
        self.play(FadeIn(cal), run_time=0.5)
        red = pastilla("más cables juntos = reducir la corriente", AMBAR, 30, True).move_to([0, -1.4, 0])
        nec2 = fuente("NEC 2020 · 310.15(C)(1), factores de ajuste", [0, -2.4, 0], 26)
        self.play(FadeIn(red), FadeIn(nec2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(tubo_, cs, cal, red, nec2)
        self.final("calor = I² × R")


# ====================================================================== V14 AWG
class V14(ShortV):
    CLAVE = "v14"

    def cuerpo(self):
        self.voz("gancho")
        s14, s12 = seccion_awg(2.08, 1.1).move_to([-2.0, 1.0, 0]), seccion_awg(3.31, 1.1).move_to([2.0, 1.0, 0])
        t14, t12 = T("14", 70, TINTA, "HEAVY").next_to(s14, DOWN, buff=0.3), T("12", 70, MARCA, "HEAVY").next_to(s12, DOWN, buff=0.3)
        t14.align_to(t12, UP)
        self.play(FadeIn(s14), FadeIn(t14), FadeIn(s12), FadeIn(t12), run_time=0.6)
        self.frac(0.35)
        g = pastilla("el 12 es MÁS grueso", VERDE_OK, 40, True).move_to([0, -2.4, 0])
        self.play(FadeIn(g, scale=1.1), Indicate(s12, color=COBRE_CL), run_time=0.6)
        self.cerrar_voz(0.1)
        self.limpiar(g)

        self.voz("p1")
        al = VGroup(T("número mayor", 44, TINTA, "HEAVY"), T("↓", 60, CLARO, "HEAVY"), T("cable más delgado", 44, MARCA, "HEAVY")).arrange(DOWN, buff=0.1).move_to([0, -3.3, 0])
        self.play(FadeIn(al), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(al, s14, s12, t14, t12)

        self.voz("p2")
        dados = VGroup(*[VGroup(RoundedRectangle(width=0.9, height=1.4, corner_radius=0.1, stroke_color="#4A5AA0", stroke_width=2).set_fill(CARTA, 1),
                                Circle(radius=0.32 - 0.06 * k, stroke_width=0).set_fill("#0B1C3D", 1)) for k in range(4)]).arrange(RIGHT, buff=0.7).move_to([0, 0.8, 0])
        alam = VMobject().set_points_as_corners([P(-4.4, 0.8), P(4.4, 0.8)]).set_stroke(COBRE, 22)
        self.play(FadeIn(dados), run_time=0.4)
        self.play(Create(alam), run_time=1.2)
        self.play(alam.animate.set_stroke(width=10), run_time=0.6)
        pas = pastilla("número = cuántas pasadas", MARCA, 36, True).move_to([0, -1.6, 0])
        self.play(FadeIn(pas), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(dados, alam, pas)

        self.voz("p3")
        datos = [(14, 2.08), (12, 3.31), (10, 5.26), (8, 8.37)]
        secs = VGroup(*[VGroup(seccion_awg(a_, 0.62), T(f"{n} AWG", 32, TINTA, "HEAVY"), T(f"{a_} mm²", 30, COBRE_CL, "BOLD")).arrange(DOWN, buff=0.15) for n, a_ in datos]).arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([0, 0.6, 0])
        if secs.width > 8.4:
            secs.scale_to_fit_width(8.4)
        for s in secs:
            self.play(FadeIn(s, shift=UP * 0.15), run_time=0.4)
            self.frac(0.12)
        x4 = pastilla("8 AWG ≈ 4 veces el 14", VERDE_OK, 36, True).move_to([0, -2.4, 0])
        self.play(FadeIn(x4), run_time=0.4)
        nec = fuente("NEC 2020 · Cap. 9, Tabla 8", [0, -3.5, 0], 26)
        self.play(FadeIn(nec), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(x4, nec)

        self.voz("p4")
        r = pastilla("baja el número, sube el cobre", MARCA, 40, True).move_to([0, -2.6, 0])
        self.play(FadeIn(r, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(secs, r)

        self.voz("p5")
        ceros = VGroup(*[T(t_, 50, TINTA, "HEAVY") for t_ in ("1/0", "2/0", "3/0", "4/0")]).arrange(RIGHT, buff=0.6).move_to([0, 1.0, 0])
        self.play(LaggedStart(*[FadeIn(c_) for c_ in ceros], lag_ratio=0.3), run_time=1.0)
        self.frac(0.35)
        kc = pastilla("después: kcmil", MARCA, 40, True).move_to([0, -1.0, 0])
        self.play(FadeIn(kc), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(ceros, kc)
        self.final("menor número = más cobre")


# ====================================================================== V15 colores
class V15(ShortV):
    CLAVE = "v15"

    def fila(self, col, txt, y, franja=False):
        c = RoundedRectangle(width=4.2, height=0.5, corner_radius=0.25, stroke_color="#8F9AC8" if col == FASE else _osc(col, 0.3), stroke_width=2).set_fill(col, 1)
        g = VGroup(c)
        if franja:
            g.add(*[Line(P(-1.9 + 0.5 * k, -0.25), P(-1.7 + 0.5 * k, 0.25)).set_stroke("#FDE047", 8) for k in range(8)])
        g.move_to([-1.7, y, 0])
        t = T(txt, 32, TINTA, "HEAVY").move_to([2.5, y, 0])
        return VGroup(g, t)

    def cuerpo(self):
        self.voz("gancho")
        cs = VGroup(*[self.fila(c_, "", 1.8 - 0.8 * k) for k, c_ in enumerate((FASE, NEUTRO, TIERRA, ROJO))])
        self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.3) for c_ in cs], lag_ratio=0.2), run_time=0.8)
        q = pastilla("¿y el verde para qué es?", TIERRA, 38, True).move_to([0, -2.4, 0])
        self.frac(0.3)
        self.play(FadeIn(q), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cs, q)

        self.voz("p1")
        h = pastilla("los colores hablan sin palabras", MARCA, 38, True).move_to([0, 0.6, 0])
        self.play(FadeIn(h, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(h)

        self.voz("p2")
        tit = T("NEC (América)", 46, MARCA, "HEAVY").move_to([0, 3.4, 0])
        f1 = self.fila(TIERRA, "tierra", 2.3)
        f2 = self.fila(TIERRA, "tierra", 1.5, True)
        f3 = VGroup(VMobject().set_points_as_corners([P(-3.8, 0.7), P(0.4, 0.7)]).set_stroke(COBRE, 12), T("tierra (desnudo)", 32, TINTA, "HEAVY").move_to([2.5, 0.7, 0]))
        f4 = self.fila(NEUTRO, "neutro", -0.3)
        f5 = self.fila("#98A2B3", "neutro", -1.1)
        self.play(FadeIn(tit), run_time=0.3)
        for f in (f1, f2, f3):
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.35)
        self.frac(0.3)
        for f in (f4, f5):
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.35)
        nec = fuente("NEC 2020 · 250.119 y 200.6", [0, -2.2, 0], 28)
        self.play(FadeIn(nec), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tit, f1, f2, f3, f4, f5, nec)

        self.voz("p3")
        tit = T("IEC (Europa)", 46, AMBAR, "HEAVY").move_to([0, 3.0, 0])
        e1 = self.fila(TIERRA, "tierra", 1.8, True)
        e2 = self.fila("#1570EF", "neutro", 0.9)
        self.play(FadeIn(tit), FadeIn(e1), FadeIn(e2), run_time=0.6)
        src = fuente("IEC 60445", [0, -0.4, 0], 28)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tit, e1, e2, src)

        self.voz("p4")
        c = pastilla("confirma qué norma se usó", MARCA, 38, True).move_to([0, 1.2, 0])
        n = pastilla("nunca uses el verde como fase", ROJO, 38, True).move_to([0, -0.2, 0])
        self.play(FadeIn(c), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(n), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(c, n)

        self.voz("p5")
        fs = VGroup(*[self.fila(c_, "", 2.2 - 0.75 * k) for k, c_ in enumerate((FASE, ROJO, "#1570EF"))])
        tf = T("fase: otro color", 40, TINTA, "HEAVY").move_to([0, -0.6, 0])
        nn = pastilla("no blanco, no gris, no verde", AMBAR, 34, True).move_to([0, -1.8, 0])
        self.play(FadeIn(fs), FadeIn(tf), run_time=0.5)
        self.frac(0.3)
        self.play(FadeIn(nn), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(fs, tf, nn)
        self.final("verde = tierra · blanco = neutro")


# ====================================================================== V16 agua y fuego eléctrico
class V16(ShortV):
    CLAVE = "v16"

    def cuerpo(self):
        self.voz("gancho")
        ap = microondas_ = __import__("taller").microondas().scale(2.2).move_to([0, 1.0, 0])
        fuego = VGroup(*[VMobject().set_points_smoothly([P(x - 0.25, 2.2), P(x - 0.1, 2.9), P(x, 3.4), P(x + 0.12, 2.9), P(x + 0.25, 2.2)]).set_fill(c_, 0.9).set_stroke(width=0)
                         for x, c_ in ((-0.8, "#F97316"), (0, "#FDB022"), (0.8, "#F97316"))])
        self.play(FadeIn(ap), FadeIn(fuego, shift=UP * 0.2), run_time=0.6)
        agua = pastilla("¿agua?", "#1570EF", 44, True).move_to([0, -1.6, 0])
        self.frac(0.25)
        self.play(FadeIn(agua), run_time=0.3)
        err = pastilla("¡ERROR!", ROJO, 50, True).move_to([0, -2.8, 0])
        self.frac(0.3)
        self.play(FadeIn(err, scale=1.3), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(agua, err)

        self.voz("p1")
        chorro = VMobject().set_points_smoothly([P(-3.6, -3.4), P(-2.4, -1.0), P(-1.0, 0.6)]).set_stroke("#7FD1FF", 14)
        self.play(Create(chorro), run_time=0.6)
        fl = corriente([P(-1.0, 0.6), P(-2.4, -1.0), P(-3.6, -3.4)], vel=1.3, color=ROJO, escala=2.4)
        self.add(fl)
        t = pastilla("la corriente viaja por el chorro", ROJO, 32, True).move_to([0.6, -2.8, 0])
        self.play(FadeIn(t), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(chorro, fl, t)

        self.voz("p2")
        bk = breaker("20", 0.46, 0.26).scale(5.0).move_to([0, -1.8, 0])
        self.play(FadeIn(bk), run_time=0.4)
        self.sfx("tic", -4)
        self.play(mover_palanca(bk, False), run_time=0.4)
        p1 = pastilla("1° corta la energía", VERDE_OK, 38, True).move_to([0, -3.4, 0])
        self.play(FadeIn(p1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(bk, p1)

        self.voz("p3")
        self.limpiar(ap, fuego)
        ex = extintor("C").scale(1.6).move_to([-2.4, -1.2, 0])
        self.play(FadeIn(ex, shift=UP * 0.2), run_time=0.5)
        tx = VGroup(T("clase C", 54, "#1570EF", "HEAVY"), T("equipo energizado", 30, TINTA, "BOLD"), T("agente que NO conduce", 30, VERDE_OK, "BOLD"), T("CO₂ · polvo químico", 30, CLARO, "BOLD")).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([1.4, -1.4, 0])
        self.play(FadeIn(tx), run_time=0.5)
        src = fuente("NFPA 10 · extintores portátiles", [0, -4.2, 0], 26)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(tx, src)

        self.voz("p4")
        self.play(ex.animate.scale(1.25).move_to([0, -1.2, 0]), run_time=0.5)
        aro = Circle(radius=0.6, stroke_color=AMBAR, stroke_width=6).move_to(ex[5])
        self.play(Create(aro), run_time=0.4)
        rv = pastilla("si dice C: sirve para fuego eléctrico", "#1570EF", 30, True).move_to([0, -4.0, 0])
        self.play(FadeIn(rv), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(ex, aro, rv)

        self.voz("p5")
        sal = pastilla("fuego grande: sal y llama a los bomberos", ROJO, 30, True).move_to([0, 1.0, 0])
        vida = pastilla("tu vida vale más que cualquier aparato", VERDE_OK, 30, True).move_to([0, -0.3, 0])
        self.play(FadeIn(sal), run_time=0.4)
        self.frac(0.35)
        self.play(FadeIn(vida), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(sal, vida)
        self.final("fuego eléctrico: nunca agua")


# ====================================================================== V17 CAT III
class V17(ShortV):
    CLAVE = "v17"

    def cuerpo(self):
        self.voz("gancho")
        mm = multimetro().scale(2.4).move_to([0, 0.6, 0])
        et = pastilla("CAT III 600 V", AMBAR, 40, True).move_to([0, -2.6, 0])
        self.play(FadeIn(mm), run_time=0.5)
        self.frac(0.2)
        self.play(FadeIn(et, scale=1.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(et)

        self.voz("p1")
        self.play(mm.animate.scale(0.6).move_to([-2.6, 2.6, 0]), run_time=0.4)
        onda_ = onda(lambda x: np.sin(2 * PI * (x + 3.6) / 2.4), -3.6, 3.6, 0.2, 0.8, MARCA, 5)
        pico = VMobject().set_points_as_corners([P(0.2, 0.2), P(0.35, 3.0), P(0.5, 0.2)]).set_stroke(ROJO, 6)
        self.play(Create(onda_), run_time=0.7)
        self.frac(0.35)
        self.play(Create(pico), run_time=0.4)
        tp = pastilla("picos de voltaje", ROJO, 38, True).move_to([0, -2.0, 0])
        self.play(FadeIn(tp), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(onda_, pico, tp, mm)

        self.voz("p2")
        cats = [("CAT IV", "acometida y medidor", ROJO), ("CAT III", "tableros, circuitos, tomacorrientes", AMBAR), ("CAT II", "aparatos enchufados", VERDE_OK)]
        filas = VGroup()
        for n, d, c_ in cats:
            caja = RoundedRectangle(width=8.0, height=1.3, corner_radius=0.2, stroke_color=c_, stroke_width=3).set_fill(c_, 0.15)
            t1 = T(n, 44, c_, "HEAVY").move_to(caja.get_left() + RIGHT * 1.3)
            t2 = T(d, 26, TINTA, "BOLD")
            if t2.width > 5.0:
                t2.scale_to_fit_width(5.0)
            t2.move_to(caja.get_right() + LEFT * (0.25 + t2.width / 2))
            filas.add(VGroup(caja, t1, t2))
        filas.arrange(DOWN, buff=0.3).move_to([0, 0.4, 0])
        for k in (2, 1, 0):
            self.play(FadeIn(filas[k], shift=UP * 0.15), run_time=0.4)
            self.frac(0.22)
        src = fuente("IEC 61010-1 · IEC 61010-2-030", [0, -2.6, 0], 26)
        self.play(FadeIn(src), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(src)

        self.voz("p3")
        fl = Arrow(P(3.6, -2.4), P(3.6, 2.0), color=ROJO, stroke_width=8, buff=0)
        tx = T("más energía", 30, ROJO, "HEAVY").rotate(PI / 2).next_to(fl, LEFT, buff=0.1)
        self.play(filas.animate.shift(LEFT * 0.4).scale(0.9), GrowArrow(fl), FadeIn(tx), run_time=0.6)
        ex = pastilla("sin categoría puede explotar", ROJO, 34, True).move_to([0, -3.4, 0])
        self.frac(0.4)
        self.play(FadeIn(ex, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(filas, fl, tx, ex)

        self.voz("p4")
        mm2 = multimetro().scale(1.3).move_to([-1.6, 0.6, 0])
        pr = VGroup(punta_prueba(ROJO).scale(2.0), punta_prueba("#2A2E35").scale(2.0)).arrange(RIGHT, buff=0.3).move_to([2.0, 0.6, 0])
        self.play(FadeIn(mm2), FadeIn(pr), run_time=0.5)
        us = pastilla("categoría y voltaje del lugar", VERDE_OK, 34, True).move_to([0, -2.6, 0])
        self.play(FadeIn(us), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(us)

        self.voz("p5")
        e1 = pastilla("CAT III", AMBAR, 36, True).next_to(mm2, DOWN, buff=0.3)
        e2 = pastilla("CAT II", VERDE_OK, 36, True).next_to(pr, DOWN, buff=0.3)
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.4)
        self.frac(0.35)
        r = pastilla("el conjunto queda en CAT II", ROJO, 36, True).move_to([0, -3.4, 0])
        self.play(FadeIn(r, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(mm2, pr, e1, e2, r)
        self.final("mide según la categoría")


# ====================================================================== V18 arranque de motor
class V18(ShortV):
    CLAVE = "v18"

    def cuerpo(self):
        self.voz("gancho")
        m = motor().scale(2.0).move_to([0, 1.4, 0])
        f = foco_led(True, 0.9).scale(1.6).move_to([0, -2.0, 0])
        g = resplandor(f[0].get_center(), 1.2, AMBAR, 10, 0.06)
        self.play(FadeIn(m), FadeIn(g), FadeIn(f), run_time=0.5)
        self.frac(0.25)
        self.play(g.animate.set_opacity(0.15), run_time=0.25)
        self.play(g.animate.set_opacity(1), run_time=0.4)
        bj = pastilla("las luces bajan un instante", AMBAR, 34, True).move_to([0, -3.8, 0])
        self.play(FadeIn(bj), run_time=0.3)
        self.cerrar_voz(0.1)
        self.limpiar(f, g, bj)

        self.voz("p1")
        cc = pastilla("motor detenido ≈ casi un corto", ROJO, 34, True).move_to([0, -1.0, 0])
        self.play(FadeIn(cc), run_time=0.4)
        self.frac(0.3)
        fcem = pastilla("aún no genera su fuerza contraelectromotriz", "#475467", 26, True).move_to([0, -2.2, 0])
        self.play(FadeIn(fcem), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(cc, fcem)

        self.voz("p2")
        self.play(m.animate.scale(0.6).move_to([-2.4, 3.2, 0]), run_time=0.4)
        ax = VGroup(Arrow(P(-3.8, -2.6), P(3.9, -2.6), buff=0, color=CLARO, stroke_width=3), Arrow(P(-3.6, -2.8), P(-3.6, 2.2), buff=0, color=CLARO, stroke_width=3))
        lab = VGroup(T("tiempo", 26, CLARO, "BOLD").next_to(ax[0], DOWN, buff=0.1).align_to(ax[0], RIGHT), T("corriente", 26, CLARO, "BOLD").rotate(PI / 2).next_to(ax[1], LEFT, buff=0.1))
        curva = VMobject().set_points_smoothly([P(-3.6, -2.6), P(-3.3, 1.8), P(-2.6, 1.7), P(-1.6, 0.2), P(-0.6, -1.5), P(1.0, -1.7), P(3.6, -1.7)]).set_stroke(ROJO, 6)
        nom = DashedLine(P(-3.6, -1.7), P(3.7, -1.7), color=VERDE_OK)
        self.play(Create(ax), FadeIn(lab), run_time=0.5)
        self.play(Create(curva), run_time=1.6)
        t1 = T("arranque: varias veces", 30, ROJO, "HEAVY").move_to([0.6, 1.6, 0])
        t2 = T("normal", 30, VERDE_OK, "HEAVY").move_to([2.4, -1.25, 0])
        self.play(FadeIn(t1), Create(nom), FadeIn(t2), run_time=0.5)
        self.cerrar_voz(0.1)
        self.limpiar(ax, lab, curva, nom, t1, t2)

        self.voz("p3")
        self.play(m.animate.scale(2.0).move_to([0, 1.2, 0]), run_time=0.5)
        aro = Circle(radius=0.75, stroke_color=AMBAR, stroke_width=6).move_to(m[5])
        self.play(Create(aro), run_time=0.4)
        nec = self.carta("NEC 2020 · Tabla 430.7(B)", "Letra de código: kVA por HP\ncon el rotor bloqueado.", [0, -2.4, 0])
        self.play(FadeIn(nec), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(aro, nec)

        self.voz("p4")
        p = pastilla("la protección debe aguantar el arranque", MARCA, 30, True).move_to([0, -1.6, 0])
        self.play(FadeIn(p), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(p)

        self.voz("p5")
        self.play(m.animate.scale(0.6).move_to([0, 2.8, 0]), run_time=0.4)
        g2 = self.pills(["estrella–triángulo", "arrancador suave", "variador de frecuencia"], 0.6, [MARCA, VERDE_OK, AMBAR], 38, 1.0, [0.1, 0.2, 0.2])
        self.cerrar_voz(0.1)
        self.limpiar(m, g2)
        self.final("arranque = varias veces la corriente")

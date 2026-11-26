import os
"""F01 · Así funciona una FOTOCELDA (reel vertical v2, 23-nov): dibujo real pieza por pieza (lib/svgfoto.py → f01_eq/),
voz clonada y cada evento anclado a su palabra (alin_f01/, faster-whisper). Guion y fuentes: guion_f01.py.
Render: FORMATO=v VOZ=eleven manim -qh --disable_caching -o cuerpo_f01 f01_fotocelda.py F01"""
from reel_base import *  # noqa: F401,F403   (importa comun_e primero → voz clonada)
import json
import re
import unicodedata
import shorts_v
from guion_f01 import GUION, TIT

shorts_v.SHORTS["f01"] = (TIT[0], TIT[1], GUION)
EQ = DIR / "f01_eq"
ALIN = DIR / "alin_f01"


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


class Pieza(Group):
    """PNG de svgfoto con sus puntos en mm para anclar llamadas."""
    def __init__(self, nombre, ancho):
        d = json.loads((EQ / f"{nombre}.json").read_text())
        img = ImageMobject(str(EQ / f"{nombre}.png"))
        img.width = ancho
        super().__init__(img)
        self.img, self.d = img, d
        self.k = ancho / (d["W"] + 2 * d["margen"])

    def mm(self, x, y):
        m = self.d["margen"]
        return self.img.get_corner(UL) + RIGHT * (m + x) * self.k + DOWN * (m + y) * self.k

    def p(self, b):
        return self.mm(*self.d["bornes"][b])


class F01(ReelTec):
    TEMA = "negro"
    CLAVE = "f01"
    TIT1, TIT2 = TIT

    # ------------------------------------------------ voz anclada a palabras
    def voz(self, clave):
        self.ini_voz = self.renderer.time
        if os.environ.get("LOG_VOZ"):
            with open(os.environ["LOG_VOZ"], "a") as fh:
                fh.write(json.dumps([self.CLAVE, clave, round(self.renderer.time, 3)]) + "\n")
        ruta = ALIN / f"{clave}.json"
        self.palabras = json.loads(ruta.read_text()) if ruta.exists() else []
        self.cursor = 0
        return super().voz(clave)

    def hasta(self, t):
        w = t - self.renderer.time
        if w > 0.05:
            self.wait(w)

    def en(self, palabra, antes=0.15):
        objs = [_norm(x) for x in palabra.split("|")]
        for i in range(self.cursor, len(self.palabras)):
            if any(_norm(self.palabras[i][2]).startswith(o) for o in objs):
                self.cursor = i + 1
                self.hasta(self.ini_voz + self.palabras[i][0] - antes)
                return
        print("NO ENCONTRADA:", palabra)

    # ------------------------------------------------ llamadas
    def flecha(self, texto, punto, desde, color, size=26):
        t = self.tag(texto, color, size).move_to(desde)
        lado = t.get_left() if punto[0] > t.get_x() + t.width / 2 else (t.get_right() if punto[0] < t.get_x() - t.width / 2 else
                                                                         (t.get_bottom() if punto[1] < t.get_y() else t.get_top()))
        ln = Line(lado, punto).set_stroke(color, 4)
        dot = Dot(punto, radius=0.075, color=color)
        return VGroup(ln, dot, t)

    def recuadro(self, centro, w, h, color):
        return Rectangle(width=w, height=h, stroke_color=color, stroke_width=5).move_to(centro)

    def cambiar(self, viejo, nuevo, rt=0.25):
        nuevo.move_to(viejo)
        self.play(FadeIn(nuevo), run_time=rt)
        self.remove(viejo)
        return nuevo

    def rayo(self, centro, esc=1.0, color="#FFE066"):
        pts = [[0.15, 0.9], [-0.25, 0.05], [0.05, 0.05], [-0.2, -0.9], [0.3, 0.15], [0.0, 0.15], [0.25, 0.9]]
        return Polygon(*[np.array([x, y, 0]) * esc for x, y in pts], stroke_width=0).set_fill(color, 1).move_to(centro)

    def sol(self, centro, r=0.55):
        rayos = VGroup(*[Line(ORIGIN, RIGHT * 0.3).shift(RIGHT * (r + 0.12)).rotate(a, about_point=ORIGIN) for a in np.arange(0, TAU, TAU / 12)])
        return VGroup(rayos.set_stroke("#FFB020", 5), Circle(radius=r, stroke_width=0).set_fill("#FFC83D", 1)).move_to(centro)

    # ================================================================== cuerpo
    def cuerpo(self):
        C, Am, G, Rr, Vi = self.ac(0), self.ac(1), self.ac(2), self.ac(3), self.ac(4)
        BL = "#F2F4F7"

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        cielo = Rectangle(width=9.2, height=12.2, stroke_width=0).set_fill("#F79009", 0.32).move_to([0, -1.8, 0]).set_z_index(-60)
        lum = Pieza("lum_off", 8.0).move_to([0.2, -2.4, 0])
        lum_on = Pieza("lum_on", 8.0).move_to(lum)
        self.play(FadeIn(cielo), FadeIn(lum), run_time=0.6)
        self.en("tarde")
        self.play(cielo.animate.set_fill("#0B1530", 0.85), run_time=1.6)
        self.en("encienden")
        self.sfx("tic", -8)
        self.play(FadeIn(lum_on), run_time=0.3)
        self.remove(lum)
        self.en("interruptor")
        q = self.tag("¿quién la enciende?", Am, 34).move_to([0, 3.2, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.3)
        self.en("responsable")
        foto = lum_on.p("foto")
        aro = Circle(radius=0.42, stroke_color=C, stroke_width=6).move_to(foto)
        self.play(Create(aro), FadeOut(q), run_time=0.4)
        self.en("esta", 0.1)
        fc = Pieza("fc_frente", 7.8).move_to([0, -1.6, 0])
        fc_ini = fc.copy().scale(0.06).move_to(foto)
        self.add(fc_ini)
        self.sfx("whoosh", -12)
        self.play(Transform(fc_ini, fc), FadeOut(lum_on), FadeOut(aro), cielo.animate.set_fill(opacity=0), run_time=0.8)
        self.remove(fc_ini)
        self.add(fc)
        self.en("tres")
        patas = self.flecha("3 patas", fc.p("pata"), [-2.6, -6.1, 0], Am, 28)
        self.play(FadeIn(patas), run_time=0.3)
        self.en("fotocontrol")
        nom = self.card("FOTOCONTROL", ["o fotocelda · ANSI C136.10"], C, 7.8, 30).move_to([0, 2.75, 0])
        self.play(FadeIn(nom, shift=DOWN * 0.15), run_time=0.35)
        self.cerrar_voz(0.05)
        self.limpiar(patas, nom, cielo)

        # ------------------------------------------------------------ p1 por fuera
        self.voz("p1")
        self.chip("1", "POR FUERA", C)
        self.play(fc.animate.scale(1.08).move_to([0.25, -1.3, 0]), run_time=0.5)
        self.en("cubierta")
        l1 = self.flecha("cubierta de polipropileno UV", fc.mm(10, 28), [-1.0, 3.05, 0], C, 26)
        self.play(FadeIn(l1), run_time=0.35)
        self.en("color")
        l2 = self.tag("gris = 120 V (código de color ANSI)", BL, 24).set_color(BLACK).move_to([0, 2.35, 0])
        l2 = self.tag("gris = 120 V · código ANSI", "#9AA1AA", 26).move_to([0, 2.35, 0])
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.3)
        self.en("ventana")
        mv = self.recuadro(fc.p("ventana"), 18 * fc.k + 0.12, 13 * fc.k + 0.12, Am)
        l3 = self.flecha("ventana de acrílico", fc.p("ventana") + LEFT * 0.95, [-2.4, -5.6, 0], Am, 26)
        self.play(FadeOut(l1), FadeOut(l2), Create(mv), FadeIn(l3), run_time=0.4)
        self.en("norte")
        nn = Circle(radius=0.32, stroke_color=G, stroke_width=5).move_to(fc.p("norte"))
        l4 = self.flecha("ventana hacia el NORTE", fc.p("norte") + RIGHT * 0.3, [2.1, 3.0, 0], G, 26)
        self.play(Create(nn), FadeIn(l4), run_time=0.4)
        self.en("sol")
        s_ = self.sol([3.4, -6.0, 0], 0.4)
        nos = self.tag("el sol no le pega de frente", Am, 24).move_to([0.4, -6.9, 0])
        self.play(FadeIn(s_), FadeIn(nos), run_time=0.35)
        self.en("base")
        l5 = self.flecha("base", fc.p("base"), [-2.9, -5.6, 0], BL, 26)
        self.play(*[FadeOut(m) for m in (mv, l3, nn, l4, s_, nos)], FadeIn(l5), run_time=0.4)
        self.en("latón")
        l6 = self.flecha("3 patas de latón", fc.p("pata"), [0.2, -6.9, 0], Am, 26)
        self.play(FadeIn(l6), run_time=0.3)
        self.en("empaque")
        l7 = self.flecha("empaque", fc.p("empaque"), [2.9, -5.6, 0], C, 26)
        self.play(FadeIn(l7), run_time=0.3)
        self.cerrar_voz(0.05)
        self.limpiar(fc, l5, l6, l7)

        # ------------------------------------------------------------ p2 la base de giro
        self.voz("p2")
        self.chip("2", "BASE DE GIRO", Am)
        ab = Pieza("fc_abajo", 4.3).move_to([-2.2, 0.45, 0])
        rc = Pieza("receptaculo", 6.2).move_to([1.3, -3.7, 0])
        t_ab = self.tag("fotocontrol visto de abajo", BL, 22).next_to(ab, UP, buff=0.05)
        t_rc = self.tag("receptáculo de la lámpara", BL, 22).move_to([1.6, -0.75, 0])
        self.play(FadeIn(ab), FadeIn(t_ab), run_time=0.5)
        self.en("receptáculo")
        self.play(FadeIn(rc), FadeIn(t_rc), run_time=0.45)
        self.en("gira")
        arco = Arc(radius=1.55, start_angle=PI * 0.75, angle=-PI * 0.5, color=Am, stroke_width=7).add_tip(tip_length=0.3).move_arc_center_to(rc.p("linea") + DOWN * 0.95 * 1)
        arco.move_to(rc.img.get_center() + UP * 0.25 + DOWN * 0.0)
        ab_g = Pieza("fc_abajo_g", 4.3).move_to(ab)
        self.play(Create(arco), run_time=0.4)
        self.sfx("tornillo", -10)
        self.play(FadeIn(ab_g), FadeOut(ab), run_time=0.5)
        self.play(FadeIn(ab), FadeOut(ab_g), run_time=0.01)
        tr = self.tag("a la derecha hasta trabar", Am, 24).move_to([1.3, -7.0, 0])
        self.play(FadeIn(tr), run_time=0.25)
        self.en("función")
        self.play(FadeOut(arco), FadeOut(tr), FadeOut(t_ab), FadeOut(t_rc), run_time=0.3)
        info = [("línea", "linea", "LÍNEA · trae la fase", "#E4E7EC", [2.25, 2.9, 0]),
                ("carga", "carga", "CARGA · va a la lámpara", Rr, [2.25, 2.2, 0]),
                ("neutro", "neutro", "NEUTRO", BL, [2.25, 1.5, 0])]
        marcas = []
        for pal, b, txt, col, pos in info:
            self.en(pal)
            a1 = Circle(radius=0.36, stroke_color=col, stroke_width=6).move_to(ab.p(b))
            a2 = Circle(radius=0.36, stroke_color=col, stroke_width=6).move_to(rc.p(b))
            t_ = self.tag(txt, col, 24).move_to(pos)
            if col in ("#E4E7EC", BL):
                t_ = self.tag(txt, "#5B6472", 24).move_to(pos)
            self.play(Create(a1), Create(a2), FadeIn(t_), run_time=0.35)
            marcas += [a1, a2, t_]
        for pal, b, txt, col in (("negro", "h_linea", "negro", "#5B6472"), ("rojo", "h_carga", "rojo", Rr), ("blanco", "h_neutro", "blanco", "#5B6472")):
            self.en(pal)
            pt = rc.p(b)
            t_ = self.tag(txt, col, 24).next_to(pt, DOWN, buff=0.12)
            self.play(Indicate(Dot(pt, radius=0.01)), FadeIn(t_, shift=UP * 0.1), run_time=0.3)
            marcas.append(t_)
        self.cerrar_voz(0.05)
        self.limpiar(ab, rc, *marcas)

        # ------------------------------------------------------------ p3 por dentro
        self.voz("p3")
        self.chip("3", "POR DENTRO", G)
        co = Pieza("fc_corte", 7.8).move_to([0, -1.2, 0])
        self.play(FadeIn(co, scale=0.95), run_time=0.5)
        self.en("ventana")
        tj = Pieza("tarjeta", 7.6).move_to([0, -0.9, 0])
        self.play(FadeOut(co), FadeIn(tj), run_time=0.5)
        vt = self.tag("ventana", "#5B6472", 22).next_to(tj.p("ventana"), UP, buff=0.12)
        self.play(FadeIn(vt), run_time=0.2)
        self.en("sensor")
        ms = Circle(radius=0.45, stroke_color=Am, stroke_width=6).move_to(tj.p("sensor"))
        self.play(Create(ms), run_time=0.3)
        self.en("fotorresistencia|fotoresistencia")
        cds = Pieza("cds", 1.7).move_to([-2.6, -6.4, 0])
        t_cds = self.tag("fotorresistencia CdS", Am, 22).next_to(cds, UP, buff=0.1)
        ant = T("modelos antiguos", 20, self.th["txt2"], "BOLD").next_to(cds, DOWN, buff=0.08)
        self.play(FadeIn(cds), FadeIn(t_cds), FadeIn(ant), run_time=0.4)
        self.en("fototransistor")
        ftr = Pieza("fototr", 0.9).move_to([2.6, -6.4, 0])
        t_ft = self.tag("fototransistor de silicio", C, 22).next_to(ftr, UP, buff=0.1)
        ele = T("electrónicos", 20, self.th["txt2"], "BOLD").next_to(ftr, DOWN, buff=0.08)
        lnk = Line(ms.get_bottom(), t_ft.get_top()).set_stroke(C, 3)
        self.play(FadeIn(ftr), FadeIn(t_ft), FadeIn(ele), Create(lnk), run_time=0.4)
        self.en("fuente")
        self.play(*[FadeOut(m) for m in (cds, t_cds, ant, ftr, t_ft, ele, lnk, ms, vt)], run_time=0.3)
        mf = self.recuadro(tj.mm(39, 49), 34 * tj.k, 50 * tj.k, BL)
        t_f = self.tag("fuente de CD", "#5B6472", 26).move_to([-2.3, -5.6, 0])
        self.play(Create(mf), FadeIn(t_f), run_time=0.4)
        self.en("relé|relay")
        mr = self.recuadro(tj.p("rele"), 22 * tj.k, 18 * tj.k, C)
        t_r = self.tag("relé de CD (K1)", C, 26).move_to([2.3, -5.6, 0])
        self.play(Create(mr), FadeIn(t_r), run_time=0.4)
        self.en("conecta")
        self.play(Indicate(mr, color=C, scale_factor=1.06), run_time=0.6)
        self.en("disco")
        mm_ = Circle(radius=10 * tj.k, stroke_color=Rr, stroke_width=6).move_to(tj.p("mov"))
        self.play(FadeOut(mf), FadeOut(t_f), Create(mm_), run_time=0.35)
        self.en("varistor|baristor")
        t_m = self.tag("varistor (MOV)", Rr, 26).move_to([-2.0, -6.2, 0])
        self.play(FadeIn(t_m), FadeOut(mr), FadeOut(t_r), run_time=0.3)
        self.en("rayos")
        ry = self.rayo(tj.p("mov") + UP * 1.7 + RIGHT * 1.6, 1.1)
        self.sfx("disparo", -14)
        self.play(FadeIn(ry, shift=DOWN * 0.3), Flash(tj.p("mov"), color="#FFE066", flash_radius=1.0, line_length=0.35), run_time=0.45)
        sob = self.tag("absorbe la sobretensión", Am, 24).move_to([1.3, -6.9, 0])
        self.play(FadeIn(sob), run_time=0.25)
        self.cerrar_voz(0.05)
        self.limpiar(tj, mm_, t_m, ry, sob)

        # ------------------------------------------------------------ p4 cómo enciende
        self.voz("p4")
        self.chip("4", "AL ATARDECER", Am)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 60, 10], x_length=7.6, y_length=2.8, tips=False,
                  axis_config={"color": self.th["ejes"], "stroke_width": 3, "include_ticks": False}).move_to([0.2, 1.2, 0])
        yl = T("lux", 22, self.th["txt2"], "BOLD").next_to(ax.y_axis, UP, buff=0.08)
        xl = T("tarde  →  noche", 22, self.th["txt2"], "BOLD").next_to(ax.x_axis, DOWN, buff=0.12)
        rl = Pieza("rele_off", 4.4).move_to([-2.1, -4.2, 0])
        rl_on = Pieza("rele_on", 4.4).move_to(rl)
        lm = Pieza("lum_off", 4.6).move_to([2.35, -4.2, 0])
        lm_on = Pieza("lum_on", 4.6).move_to(lm)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(rl), FadeIn(lm), run_time=0.6)
        curva = ax.plot(lambda x: 58 / (1 + np.exp((x - 5.2) * 1.15)) + 2, x_range=[0, 10], color=Am, stroke_width=6)
        self.en("día")
        s_ = self.sol(ax.c2p(1.2, 52) + UP * 0.25, 0.3)
        self.play(FadeIn(s_), Create(curva, rate_func=lambda t: 0.25 * t), run_time=0.5)
        self.en("abierto")
        ab_t = self.tag("contacto ABIERTO", Rr, 24).next_to(rl, UP, buff=0.1)
        self.play(FadeIn(ab_t), run_time=0.3)
        self.en("apagada")
        ap = self.tag("apagada", "#5B6472", 24).next_to(lm, UP, buff=0.1)
        self.play(FadeIn(ap), run_time=0.25)
        self.en("atardecer")
        umbral = DashedLine(ax.c2p(0, 16), ax.c2p(10, 16), dash_length=0.12).set_stroke(G, 4)
        self.play(FadeOut(s_), run_time=0.2)
        self.play(Create(curva, rate_func=lambda t: 0.25 + 0.4 * t), run_time=1.2)
        self.en("uno|1")
        u_t = self.tag("1,5 fc ≈ 16 lux", G, 26).move_to(ax.c2p(7.6, 30))
        self.play(Create(umbral), FadeIn(u_t), run_time=0.45)
        x16 = 5.2 + np.log(58 / 14 - 1) / 1.15
        pto = Dot(ax.c2p(x16, 16), radius=0.11, color=G)
        self.play(FadeIn(pto, scale=1.6), run_time=0.25)
        self.en("bobina")
        self.play(Indicate(rl, scale_factor=1.04, color=Am), run_time=0.5)
        self.en("cierra")
        self.sfx("contactor", -12)
        rl_on.move_to(rl)
        self.add(rl_on)
        self.remove(rl)
        ce_t = self.tag("contacto CERRADO", G, 24).move_to(ab_t)
        self.play(FadeOut(ab_t), FadeIn(ce_t), run_time=0.25)
        self.en("enciende|encienga")
        self.add(lm_on)
        self.remove(lm)
        en_t = self.tag("encendida al instante", G, 24).move_to(ap)
        self.play(FadeOut(ap), FadeIn(en_t), Create(curva, rate_func=lambda t: 0.65 + 0.35 * t), run_time=0.5)
        self.cerrar_voz(0.05)
        self.limpiar(ax, yl, xl, curva, umbral, u_t, pto, rl_on, lm_on, ce_t, en_t)

        # ------------------------------------------------------------ p5 histéresis y retardo
        self.voz("p5")
        self.chip("5", "HISTÉRESIS Y RETARDO", Vi)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 60, 10], x_length=7.6, y_length=5.0, tips=False,
                  axis_config={"color": self.th["ejes"], "stroke_width": 3, "include_ticks": False}).move_to([0.2, 0.2, 0])
        yl = T("lux", 22, self.th["txt2"], "BOLD").next_to(ax.y_axis, UP, buff=0.08)
        xl = T("noche  →  mañana", 22, self.th["txt2"], "BOLD").next_to(ax.x_axis, DOWN, buff=0.12)
        on_l = DashedLine(ax.c2p(0, 16), ax.c2p(10, 16), dash_length=0.12).set_stroke(G, 4)
        on_t = T("enciende 16 lx", 22, G, "HEAVY").next_to(ax.c2p(0.15, 16), DOWN, buff=0.08).align_to(ax.c2p(0.15, 0), LEFT)

        def f5(x):
            base = 2 + 56 / (1 + np.exp(-(x - 7.6) * 1.4))
            return base + 34 * np.exp(-((x - 5.0) / 0.16) ** 2)     # faros de un carro (pico corto)

        curva = ax.plot(f5, x_range=[0, 10, 0.02], color=Am, stroke_width=6)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(on_l), FadeIn(on_t), run_time=0.6)
        self.en("mañana")
        self.play(Create(curva), run_time=1.4)
        self.en("uno|1")
        off_l = DashedLine(ax.c2p(0, 24), ax.c2p(10, 24), dash_length=0.12).set_stroke(Rr, 4)
        off_t = T("apaga hasta 24 lx (1,5 ×)", 20, Rr, "HEAVY").next_to(ax.c2p(0.15, 24), UP, buff=0.08).align_to(ax.c2p(0.15, 0), LEFT)
        self.play(Create(off_l), FadeIn(off_t), run_time=0.45)
        self.en("diferencia")
        banda = Polygon(ax.c2p(0, 16), ax.c2p(10, 16), ax.c2p(10, 24), ax.c2p(0, 24), stroke_width=0).set_fill(Vi, 0.35)
        h_t = self.tag("histéresis: no parpadea", Vi, 26).move_to([0.6, -3.4, 0])
        self.play(FadeIn(banda), FadeIn(h_t), run_time=0.4)
        self.en("tres|3")
        rt = self.card("RETARDO AL APAGAR", ["3 a 5 segundos"], C, 7.8, 28).move_to([0, -4.9, 0])
        self.play(FadeOut(h_t), FadeIn(rt, shift=UP * 0.15), run_time=0.4)
        self.en("faros")
        pico = Circle(radius=0.42, stroke_color=BL, stroke_width=5).move_to(ax.c2p(5.0, 30))
        f_t = self.tag("faros: dura menos de 3 s", BL, 22).set_color(BLACK)
        f_t = self.tag("faros: < 3 s → no se apaga", "#5B6472", 22).move_to(ax.c2p(4.4, 52))
        self.play(Create(pico), FadeIn(f_t), run_time=0.4)
        self.en("relámpago")
        ry = self.rayo(ax.c2p(6.2, 40), 0.55)
        self.play(FadeIn(ry, scale=1.3), run_time=0.25)
        self.cerrar_voz(0.05)
        self.limpiar(ax, yl, xl, on_l, on_t, off_l, off_t, banda, curva, rt, pico, f_t, ry)

        # ------------------------------------------------------------ p6 falla encendido
        self.voz("p6")
        self.chip("6", "FALLA SEGURA", Rr)
        dia = Rectangle(width=9.2, height=12.2, stroke_width=0).set_fill("#7CB7E8", 0.35).move_to([0, -1.8, 0]).set_z_index(-60)
        lm = Pieza("lum_on", 8.0).move_to([0.3, -2.5, 0])
        s_ = self.sol([-3.3, 2.9, 0], 0.4)
        self.play(FadeIn(dia), FadeIn(lm), FadeIn(s_), run_time=0.5)
        self.en("falla")
        fo = self.card("FALLA ENCENDIDO", ["(fail-on)"], Rr, 7.8, 30).scale(0.8).move_to([1.0, 2.9, 0])
        self.play(FadeIn(fo, shift=DOWN * 0.15), run_time=0.35)
        self.en("mediodía")
        pis = self.tag("encendida de día = revisar el fotocontrol", Am, 24).move_to([0, -7.0, 0])
        aro = Circle(radius=0.45, stroke_color=Am, stroke_width=6).move_to(lm.p("foto"))
        self.play(FadeIn(pis), Create(aro), run_time=0.4)
        self.cerrar_voz(0.05)
        self.limpiar(dia, lm, s_, fo, pis, aro)

        # ------------------------------------------------------------ p7 consejos de campo
        self.voz("p7")
        self.chip("7", "EN CAMPO", G)
        lm = Pieza("lum_on", 7.0).move_to([-0.9, -2.3, 0])
        lm_off = Pieza("lum_off", 6.4).move_to(lm)
        rotulo = VGroup(Rectangle(width=1.5, height=3.0, stroke_width=0).set_fill("#E4E7EC", 1),
                        T("RÓTULO", 20, "#101828", "HEAVY").rotate(PI / 2)).move_to([3.4, -0.7, 0])
        self.play(FadeIn(lm), run_time=0.4)
        self.en("enciende")
        self.play(FadeIn(rotulo), run_time=0.3)
        luz = lm.p("lente")
        ruta = VMobject().set_points_as_corners([luz, rotulo.get_left() + DOWN * 0.3, lm.p("foto") + RIGHT * 0.12]).set_stroke("#FFE066", 5)
        self.play(Create(ruta), run_time=0.5)
        for _ in range(2):
            self.add(lm_off); self.remove(lm); self.wait(0.25)
            self.add(lm); self.remove(lm_off); self.wait(0.25)
        self.en("sensor")
        cic = self.tag("la luz le pega al sensor", Am, 24).move_to([0, 2.9, 0])
        self.play(FadeIn(cic), run_time=0.3)
        self.en("probarla")
        self.play(FadeOut(lm), FadeOut(lm_off), FadeOut(rotulo), FadeOut(ruta), FadeOut(cic), run_time=0.35)
        fc = Pieza("fc_frente", 7.8).move_to([0, -1.2, 0])
        self.play(FadeIn(fc), run_time=0.35)
        self.en("cinta")
        fcc = Pieza("fc_cinta", 7.8).move_to(fc)
        self.play(FadeIn(fcc, shift=LEFT * 0.4), run_time=0.45)
        self.remove(fc)
        c_t = self.tag("cinta negra opaca ✓", G, 26).move_to([0, 2.95, 0])
        self.play(FadeIn(c_t), run_time=0.25)
        self.en("dedo")
        d_t = self.tag("el dedo deja pasar luz ✗", Rr, 26).move_to([0, -5.5, 0])
        self.play(FadeIn(d_t), run_time=0.3)
        self.en("minutos")
        reloj = VGroup(Circle(radius=0.55, stroke_color=C, stroke_width=5), Line(ORIGIN, UP * 0.4).set_stroke(C, 5),
                       Line(ORIGIN, RIGHT * 0.3).set_stroke(C, 5)).move_to([-2.6, -6.7, 0])
        r_t = self.tag("≈ 2 minutos", C, 26).next_to(reloj, RIGHT, buff=0.2)
        self.play(FadeIn(reloj), FadeIn(r_t), Rotate(reloj[1], -TAU, about_point=reloj[0].get_center()), run_time=0.9)
        self.en("encender")
        ok = self.tag("enciende ✓", G, 28).move_to([2.4, -6.7, 0])
        self.sfx("ding", -12)
        self.play(FadeIn(ok, scale=1.2), run_time=0.3)
        self.cerrar_voz(0.05)
        self.limpiar(fcc, c_t, d_t, reloj, r_t, ok)
        self.quitar_chip()
        self.final("Sensor de luz + relé + varistor, en una base de giro")


class PortadaF01(Scene):
    def construct(self):
        from miniaturas import sticker, logo_esq
        self.add(Rectangle(width=9.2, height=16.4, stroke_width=0).set_fill("#000000", 1))
        t = VGroup(T("¿QUIÉN ENCIENDE", 96, "#FFFFFF", "HEAVY"), T("LAS LÁMPARAS", 104, "#00E5FF", "HEAVY"),
                   T("DE LA CALLE?", 104, "#FFB020", "HEAVY")).arrange(DOWN, buff=0.12)
        t.scale_to_fit_width(8.4).move_to([0, 4.9, 0])
        fc = Pieza("fc_frente", 8.2).move_to([0, -0.9, 0])
        tj = Pieza("tarjeta", 3.6).move_to([2.4, -4.6, 0])
        st = sticker("FOTOCELDA POR DENTRO", "#FF4D6D", size=56, ang=-0.03)
        st.scale_to_fit_width(min(st.width, 7.8)).move_to([0, -6.6, 0])
        self.add(fc, tj, t, st)
        logo_esq(self, (3.6, 7.3))

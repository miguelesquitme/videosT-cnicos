"""E06 · EL CONTACTOR (horizontal, 15+ min). Guion y fuentes en e06_guion.py; piezas en piezas_auto.py.
Render: FORMATO=h VOZ=eleven manim -qh --disable_caching -o final e06_contactor.py Contactor
"""
from taller import *
from comun_e import _osc, _cla
from piezas_auto import *
from nema import breaker, mover_palanca
from dibujos_aves import check, equis
from e06_guion import GUION

ROJO_C = "#E5484D"
VIOLETA = "#9E77ED"


def alinear(m, x):
    """Coloca el símbolo para que su conductor principal (m[0]) quede en la abscisa x."""
    m.shift(RIGHT * (x - m[0].get_start()[0]))
    return m


def caja_info(titulo, lineas, color=MARCA, w=5.6, size=26):
    cab = T(titulo, size + 4, color, "HEAVY")
    cu = VGroup(*[T(l, size, TINTA, "MEDIUM") for l in lineas]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    g = VGroup(cab, cu).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    caja = tarjeta(max(w, g.width + 0.6), g.height + 0.5, color="#4A5AA0")
    barra = RoundedRectangle(width=0.12, height=caja.height - 0.24, corner_radius=0.05, stroke_width=0).set_fill(color, 1).move_to(caja.get_left() + RIGHT * 0.16)
    g.move_to(caja).shift(RIGHT * 0.1)
    return VGroup(caja, barra, g)


def motor_3f(s=1.0):
    """Motor trifásico de jaula (vista lateral): carcasa con aletas, caja de bornes, eje y patas."""
    cuerpo = RoundedRectangle(width=3.0 * s, height=1.9 * s, corner_radius=0.25 * s, stroke_color="#3A4250", stroke_width=1.6).set_fill("#4F6D8F", 1)
    aletas = VGroup(*[Line(P(-1.35 * s, y), P(1.2 * s, y)).set_stroke("#3B5675", 2.2) for y in np.linspace(-0.7 * s, 0.7 * s, 8)])
    tapa = RoundedRectangle(width=0.35 * s, height=1.7 * s, corner_radius=0.1 * s, stroke_color="#3A4250", stroke_width=1.4).set_fill("#5E7EA2", 1).move_to(P(1.6 * s, 0))
    eje = Rectangle(width=0.6 * s, height=0.22 * s, stroke_color="#6B7280", stroke_width=1.2).set_fill("#C9CED6", 1).move_to(P(2.05 * s, 0))
    caja_b = RoundedRectangle(width=0.9 * s, height=0.45 * s, corner_radius=0.06 * s, stroke_color="#3A4250", stroke_width=1.4).set_fill("#5E7EA2", 1).move_to(P(-0.2 * s, 1.15 * s))
    patas = VGroup(*[Rectangle(width=0.45 * s, height=0.28 * s, stroke_width=0).set_fill("#3B5675", 1).move_to(P(x * s, -1.05 * s)) for x in (-1.0, 0.9)])
    placa = RoundedRectangle(width=0.8 * s, height=0.42 * s, corner_radius=0.04 * s, stroke_color="#98A2B3", stroke_width=1).set_fill("#E4E7EC", 1).move_to(P(-0.4 * s, 0.05 * s))
    g = VGroup(patas, cuerpo, aletas, tapa, eje, caja_b, placa)
    g.eje, g.caja_b, g.placa = eje, caja_b, placa
    return g


def pulsador_fis(color="#1F2430", simbolo="O", s=1.0):
    """Pulsador de 22 mm (vista frontal): bisel metálico y botón; símbolos IEC 60417: I = marcha, O = paro."""
    bisel = Circle(radius=0.5 * s, stroke_color="#6B7280", stroke_width=1.6).set_fill("#C9CED6", 1)
    aro = Circle(radius=0.42 * s, stroke_color="#4B5563", stroke_width=1.2).set_fill("#9CA3AF", 1)
    boton = Circle(radius=0.34 * s, stroke_color=_osc(color, 0.4), stroke_width=1.2).set_fill(color, 1)
    sim = tx(simbolo, 0.3 * s, "#FFFFFF" if color in ("#1F2430", ROJO_C, "#12B76A") else "#1D2939")
    brillo = Arc(radius=0.24 * s, start_angle=PI * 0.6, angle=PI * 0.4).set_stroke(WHITE, 2, 0.5)
    return VGroup(bisel, aro, boton, sim, brillo)


def horno(s=1.0):
    caja = RoundedRectangle(width=2.6 * s, height=2.0 * s, corner_radius=0.12 * s, stroke_color="#4B5563", stroke_width=1.6).set_fill("#9AA3AF", 1)
    ventana = RoundedRectangle(width=2.1 * s, height=1.4 * s, corner_radius=0.08 * s, stroke_width=0).set_fill("#1F2430", 1).move_to(caja).shift(DOWN * 0.1 * s)
    res = VGroup(*[VMobject().set_points_as_corners([P(x, y) for x, y in zip(np.linspace(-0.9 * s, 0.9 * s, 15), [(0.1 * s if k % 2 else -0.1 * s) + yy for k in range(15)])])
                   .set_stroke("#FF6B3D", 3.2) for yy in (0.35 * s, -0.05 * s, -0.45 * s)]).move_to(ventana)
    perilla = Circle(radius=0.08 * s, stroke_width=0).set_fill("#1F2430", 1).move_to(caja.get_top() + DOWN * 0.18 * s + RIGHT * 0.9 * s)
    return VGroup(caja, ventana, res, perilla)


def barra_pasos(pasos, x=-5.3, y0=2.9, dy=1.1, w=4.6):
    g = VGroup()
    for k, t_ in enumerate(pasos):
        caja = RoundedRectangle(width=w, height=0.82, corner_radius=0.16, stroke_color="#4A5AA0", stroke_width=1.6).set_fill(CARTA, 1)
        num = VGroup(Circle(radius=0.26, stroke_width=0).set_fill("#4A5AA0", 1), T(str(k + 1), 26, WHITE, "HEAVY"))
        num[1].move_to(num[0])
        num.move_to(caja.get_left() + RIGHT * 0.45)
        tt = T(t_, 22, TINTA, "BOLD")
        if tt.width > w - 1.2:
            tt.scale_to_fit_width(w - 1.2)
        tt.next_to(num, RIGHT, buff=0.22)
        fila = VGroup(caja, num, tt).move_to([x, y0 - k * dy, 0])
        g.add(fila)
    return g


def activar_paso(fila):
    return [fila[0].animate.set_stroke(MARCA, 3).set_fill("#123A5A", 1), fila[1][0].animate.set_fill(MARCA, 1)]


def completar_paso(fila):
    ck = check(VERDE_OK, 0.2).move_to(fila[0].get_right() + LEFT * 0.35)
    return [fila[0].animate.set_stroke("#4A5AA0", 1.6).set_fill(CARTA, 1), fila[1][0].animate.set_fill(VERDE_OK, 1), FadeIn(ck)], ck


class Contactor(TallerH):
    CARPETA_VOZ = "voz_e06"
    GUION = GUION
    DURACION_MIN = 900.0

    def construct(self):
        solo = os.environ.get("SOLO")
        orden = ["intro", "problema", "definicion", "partes", "electroiman", "laminas", "anillo", "llamada", "contactos", "arco",
                 "bornes", "simbolos", "mando", "potencia", "bobina", "categorias", "placa", "auxiliares", "soldadura", "familia",
                 "seleccion", "ejemplo1", "ejemplo2", "errores", "seguridad", "repaso"]
        for paso in orden:
            if solo and paso not in solo.split(","):
                continue
            getattr(self, "f_" + paso)()
        if not solo:
            self.f_final()

    # ------------------------------------------------------------------ utilidades de escena
    def cables_arriba(self, ct, alto=1.6, etiquetas=("L1", "L2", "L3"), color=C_POT, w=11):
        cs = VGroup()
        for n, e in zip(("1/L1", "3/L2", "5/L3"), etiquetas):
            p = ct.b[n].entrada.get_center()
            cs.add(cable([p, p + UP * alto], color, w=w, etiqueta=e))
        return cs

    def cables_abajo(self, ct, alto=1.4, etiquetas=("T1", "T2", "T3"), color=C_POT, w=11):
        cs = VGroup()
        for n, e in zip(("2/T1", "4/T2", "6/T3"), etiquetas):
            p = ct.b[n].entrada.get_center()
            cs.add(cable([p, p + DOWN * alto], color, w=w, etiqueta=e))
        return cs

    # ------------------------------------------------------------------ 1 · intro
    def f_intro(self):
        self.voz("intro")
        rl = riel_din(6.0, 1.2).move_to([-4.6, 0.0, 0])
        ct = contactor_frente(1.25).move_to([-4.6, 0.0, 0])
        cs = self.cables_arriba(ct, 1.5)
        ci = self.cables_abajo(ct, 1.3)
        self.add(cs, ci)
        self.play(FadeIn(rl), FadeIn(ct, shift=UP * 0.2), Create(cs), Create(ci), run_time=1.0)
        tit = self.titulo("EL", "CONTACTOR", "qué es, cómo funciona y cómo elegirlo")
        self.esperar_frac(0.12)
        va = pastilla("bobina: solo 7 VA", ROJO_C, 26, True).move_to([1.9, -1.9, 0])
        fl = CurvedArrow(va.get_left() + LEFT * 0.05, ct.b["A1"].tor.get_right() + RIGHT * 0.12, angle=-0.6, color=ROJO_C, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(va), Create(fl), run_time=0.5)
        self.esperar_frac(0.1)
        self.sfx("tic", -8)
        self.play(cerrar_indicador(ct, True), run_time=0.3)
        cur = VGroup(*[corriente([c_.ruta.get_end(), c_.ruta.get_start()], vel=1.2, escala=1.2) for c_ in cs] +
                     [corriente([c_.ruta.get_start(), c_.ruta.get_end()], vel=1.2, escala=1.2) for c_ in ci])
        self.add(cur)
        hp = pastilla("motor: 5 hp ≈ 3,7 kW", AMBAR, 26, True).next_to(ci, DOWN, buff=0.15)
        self.play(FadeIn(hp), run_time=0.4)
        self.esperar_frac(0.5)
        datos = pastilla("con datos reales", VERDE_OK, 26, True).move_to([1.9, -2.7, 0]).align_to(va, LEFT)
        self.play(FadeIn(datos, shift=UP * 0.1), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(rl, ct, cs, ci, tit, va, fl, cur, hp, datos)

    # ------------------------------------------------------------------ 2 · por qué no un interruptor
    def f_problema(self):
        self.voz("problema")
        # interruptor manual con arco
        base = RoundedRectangle(width=2.0, height=0.3, corner_radius=0.06, stroke_color="#6B7280", stroke_width=1.4).set_fill("#9CA3AF", 1).move_to([-4.6, 1.2, 0])
        piv = base.get_left() + RIGHT * 0.3 + UP * 0.15
        cuch = Line(piv, piv + rotate_vector(RIGHT * 1.5, 0.5)).set_stroke("#D0D5DD", 10)
        mang = RoundedRectangle(width=0.5, height=0.22, corner_radius=0.08, stroke_width=0).set_fill(ROJO_C, 1).move_to(cuch.get_end())
        arco_ = VGroup(*[rayo(cuch.get_end() + DOWN * 0.1, base.get_right() + LEFT * 0.25 + UP * 0.15, color=AMBAR, semilla=k, amp=0.1) for k in range(2)])
        cab = VGroup(cable([base.get_left() + RIGHT * 0.1 + DOWN * 0.1, [-6.6, 1.05, 0], [-6.6, -1.2, 0]], C_POT, w=16, puntera=False),
                     cable([base.get_right() + LEFT * 0.1 + DOWN * 0.1, [-2.6, 1.05, 0], [-2.6, -1.2, 0]], C_POT, w=16, puntera=False))
        self.play(FadeIn(base), Create(cuch), FadeIn(mang), FadeIn(cab), run_time=0.7)
        l1 = T("cables gruesos hasta el operador", 24, TINTA, "BOLD").move_to([-4.6, -1.8, 0])
        self.play(FadeIn(l1), run_time=0.3)
        self.esperar_frac(0.2)
        self.sfx("pop", -10)
        self.play(FadeIn(arco_), Flash(cuch.get_end(), color=AMBAR), run_time=0.4)
        l2 = T("arco en cada apertura", 24, AMBAR, "BOLD").move_to([-4.6, -2.4, 0])
        x_ = equis(ROJO_C, 0.45).move_to([-4.6, 2.6, 0])
        self.play(FadeIn(l2), FadeIn(x_, scale=1.4), run_time=0.4)
        self.esperar_frac(0.25)
        # dos mundos
        sep = DashedLine([1.5, 3.6, 0], [1.5, -3.6, 0], color=TINTA2)
        m1 = VGroup(T("MANDO", 36, ROJO_C, "HEAVY"), T("poca corriente · 24 a 230 V", 22, TINTA, "BOLD")).arrange(DOWN, buff=0.08).move_to([-0.6, 3.2, 0])
        m2 = VGroup(T("POTENCIA", 36, AMBAR, "HEAVY"), T("corriente del motor", 22, TINTA, "BOLD")).arrange(DOWN, buff=0.08).move_to([4.9, 3.2, 0])
        pb = pulsador_fis("#12B76A", "I", 0.9).move_to([-0.6, 1.0, 0])
        hilo = cable([pb.get_bottom() + DOWN * 0.05, [-0.6, -0.8, 0], [0.8, -0.8, 0]], C_MANDO, w=6, puntera=False)
        ct = contactor_frente(0.75).move_to([1.5, -0.6, 0])
        mo = motor_3f(0.75).move_to([5.3, -0.6, 0])
        gru = VGroup(cable([ct.b["2/T1"].entrada.get_center(), ct.b["2/T1"].entrada.get_center() + DOWN * 0.6, [3.7, -2.5, 0], [4.9, -2.5, 0], [4.9, -1.3, 0]], C_POT, w=14, puntera=False))
        self.play(Create(sep), FadeIn(m1), FadeIn(m2), run_time=0.5)
        self.play(FadeIn(pb), Create(hilo), FadeIn(mo), run_time=0.6)
        self.esperar_frac(0.3)
        puente = pastilla("el puente: CONTACTOR", MARCA, 28, True).move_to([1.5, -3.4, 0])
        self.add(gru)
        self.play(FadeIn(ct, scale=0.9), Create(gru), FadeIn(puente), run_time=0.7)
        self.cerrar_voz()
        self.limpiar(base, cuch, mang, arco_, cab, l1, l2, x_, sep, m1, m2, pb, hilo, ct, mo, gru, puente)

    # ------------------------------------------------------------------ 3 · definición IEV
    def f_definicion(self):
        self.voz("definicion")
        src = fuente("IEC 60050 · IEV 441-14-33 (contactor mecánico)", [0, -4.05, 0], 22)
        lineas = [("aparato mecánico de conexión", TINTA), ("con UNA SOLA POSICIÓN DE REPOSO,", AMBAR), ("que NO se acciona a mano,", AMBAR),
                  ("capaz de ESTABLECER, SOPORTAR e INTERRUMPIR corrientes", TINTA), ("en condiciones NORMALES, incluidas las", TINTA),
                  ("SOBRECARGAS DE SERVICIO.", TINTA)]
        txt = VGroup(*[T(l, 30, c, "BOLD") for l, c in lineas]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        caja = tarjeta(txt.width + 1.0, txt.height + 0.8, color="#4A5AA0")
        comi = T("“", 120, MARCA, "HEAVY").move_to(caja.get_corner(UL) + RIGHT * 0.35 + DOWN * 0.35)
        bloque = VGroup(caja, txt, comi).move_to([0, 1.2, 0])
        txt.move_to(caja)
        self.play(FadeIn(caja), FadeIn(comi), FadeIn(src), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in txt], lag_ratio=0.5), run_time=min(9.0, self.resta() * 0.4))
        self.esperar_frac(0.15)
        # dos detalles
        d1 = caja_info("1 · posición de reposo", ["sin tensión en la bobina", "→ siempre ABIERTO"], AMBAR, 5.6, 24).move_to([-3.6, -2.4, 0])
        d2 = caja_info("2 · condiciones normales", ["NO corta cortocircuitos", "→ disyuntor o fusibles"], ROJO_C, 5.6, 24).move_to([3.6, -2.4, 0])
        self.play(bloque.animate.shift(UP * 0.55).scale(0.86), src.animate.shift(DOWN * 0.1), run_time=0.4)
        self.play(FadeIn(d1, shift=UP * 0.2), run_time=0.4)
        self.esperar_frac(0.45)
        self.play(FadeIn(d2, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(bloque, src, d1, d2)

    # ------------------------------------------------------------------ 4 · despiece
    def construir_despiece(self, x=-2.6):
        piezas = [
            ("cámara apagachispas", camara_apaga(3.6, 1.2)),
            ("contactos fijos y bornes", VGroup(contacto_fijo(-1), contacto_fijo(1))),
            ("contacto móvil (puente)", puente_movil(2.4)),
            ("portacontactos", portacontactos(1.0)),
            ("armadura móvil (martillo)", armadura_T(3.2, 0.55)),
            ("resorte de retorno", resorte(0.8, 0.6, 7, "#C7CCD6", 3)),
            ("bobina", bobina(1.8, 1.0)),
            ("circuito magnético fijo (culata)", nucleo_E(3.2, 1.3)),
            ("base", base_contactor(3.8, 0.7)),
        ]
        g = VGroup(*[p for _, p in piezas]).arrange(DOWN, buff=0.18).scale_to_fit_height(8.2).move_to([x, 0, 0])
        return piezas, g

    def f_partes(self):
        self.voz("partes")
        piezas, g = self.construir_despiece(-2.8)
        destino = [p.get_center() for _, p in piezas]
        junto = g.copy()
        # posición armada (todas comprimidas en el centro)
        for p in g:
            p.move_to([-2.8, p.get_center()[1] * 0.35, 0])
        self.play(FadeIn(g, scale=0.9), run_time=0.6)
        self.play(*[p.animate.move_to(d) for (_, p), d in zip(piezas, destino)], run_time=1.2)
        etqs = VGroup()
        frac = (self.resta() - 4.0) / len(piezas)
        for k, (nom, p) in enumerate(piezas):
            col = AMBAR if nom.startswith(("bobina", "armadura", "circuito")) else TINTA
            e = T(nom, 26, col, "BOLD").move_to([3.4, p.get_center()[1], 0], aligned_edge=LEFT).shift(LEFT * 0.0)
            e.align_to([1.4, 0, 0], LEFT)
            ln = DashedLine(p.get_right() + RIGHT * 0.1, e.get_left() + LEFT * 0.12, dash_length=0.07, color=TINTA2)
            self.play(Create(ln), FadeIn(e, shift=LEFT * 0.1), Indicate(p, scale_factor=1.04, color=None), run_time=0.5)
            etqs.add(VGroup(ln, e))
            if frac > 0.6:
                self.wait(frac - 0.5)
        ele = VGroup(*[etqs[i][1] for i in (4, 6, 7)])
        caja = SurroundingRectangle(ele, color=AMBAR, buff=0.12, corner_radius=0.12)
        lab = pastilla("ELECTROIMÁN", AMBAR, 26, True).rotate(PI / 2).next_to(caja, RIGHT, buff=0.15)
        self.play(Create(caja), FadeIn(lab), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(g, etqs, caja, lab)

    # ------------------------------------------------------------------ corte funcional (reutilizable)
    def corte(self, cx=-2.0, cy=0.0, k=1.0):
        """Contactor en corte esquemático. Devuelve grupo con referencias para animar (abierto)."""
        c = np.array([cx, cy, 0])
        base = base_contactor(4.6, 0.6).move_to(c + P(0, -3.25))
        nuc = nucleo_E(3.6, 1.6).move_to(c + P(0, -2.15))           # columnas: top en y = cy-1.35
        bob = bobina(2.0, 1.05).move_to(c + P(0, -1.95))
        top_col = c[1] - 1.35
        gap = 0.4
        arm = armadura_T(3.6, 0.6).move_to(c + P(0, top_col - c[1] + gap + 0.3))
        resortes = VGroup(*[resorte(1.0, 0.36, 6, "#C7CCD6", 2.6) for _ in range(2)])
        for r_, x in zip(resortes, (-1.25, 1.25)):
            r_.stretch_to_fit_height(arm.get_bottom()[1] - (c[1] - 1.35)).move_to([cx + x, (arm.get_bottom()[1] + top_col) / 2, 0])
        rod = Rectangle(width=0.4, height=1.5, stroke_color="#4D7C0F", stroke_width=1.2).set_fill("#A3D977", 1)
        rod.move_to([cx, arm.get_top()[1] + 0.75, 0])
        pu = puente_movil(2.8).move_to([cx, rod.get_top()[1] + 0.08, 0])
        y_pad_fijo = pu[1][0].get_bottom()[1] - gap - 0.04
        fijos = VGroup()
        for lado in (-1, 1):
            tira = Rectangle(width=1.9, height=0.16, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1)
            tira.move_to([cx + lado * 2.05, y_pad_fijo - 0.12, 0])
            pad = RoundedRectangle(width=0.3, height=0.08, corner_radius=0.02, stroke_width=0.6, stroke_color="#98A2B3").set_fill(AG, 1)
            pad.move_to([cx + lado * 1.2, y_pad_fijo, 0])
            tor = tornillo_ph(0.17).move_to([cx + lado * 2.75, y_pad_fijo + 0.08, 0])
            fijos.add(VGroup(tira, pad, tor))
        cam = RoundedRectangle(width=4.2, height=1.5, corner_radius=0.1, stroke_color="#6B7280", stroke_width=1.6).set_fill("#2A2F3A", 0.55)
        cam.move_to([cx, pu.get_center()[1] - 0.1, 0])
        placas = VGroup(*[VGroup(*[Rectangle(width=0.05, height=0.7, stroke_width=0).set_fill("#A7AFBA", 0.9).move_to([cx + lado * (1.2 + (j - 2) * 0.11), cam.get_center()[1] + 0.25, 0])
                                   for j in range(5)]) for lado in (-1, 1)])
        cam_g = VGroup(cam, placas)
        movil = VGroup(arm, rod, pu)
        g = VGroup(base, nuc, bob, resortes, cam_g, fijos, movil)
        g.base, g.nuc, g.bob, g.resortes, g.cam, g.fijos, g.movil, g.pu, g.arm = base, nuc, bob, resortes, cam_g, fijos, movil, pu, arm
        g.gap, g.top_col = gap, top_col
        return g

    def mover_corte(self, ct, cerrar=True, rt=0.35):
        d = -ct.gap if cerrar else ct.gap
        anims = [ct.movil.animate.shift(UP * d)]
        for r_ in ct.resortes:
            nuevo_h = r_.height + d
            anims.append(r_.animate.stretch_to_fit_height(max(0.05, nuevo_h)).shift(UP * d / 2))
        self.play(*anims, run_time=rt)

    # ------------------------------------------------------------------ 5 · electroimán en acción
    def f_electroiman(self):
        self.voz("electroiman")
        ct = self.corte(-2.6, 0.6)
        self.play(FadeIn(ct), run_time=0.6)
        a1 = cable([ct.bob.get_left() + RIGHT * 0.05 + UP * 0.25, ct.bob.get_left() + LEFT * 1.0 + UP * 0.25, [-6.6, -1.45, 0]], C_MANDO, w=6, puntera=False)
        a2 = cable([ct.bob.get_left() + RIGHT * 0.05 + DOWN * 0.25, ct.bob.get_left() + LEFT * 1.0 + DOWN * 0.25, [-6.6, -1.95, 0]], C_NEUTRO, w=6, puntera=False)
        la = VGroup(T("A1", 24, ROJO_C, "HEAVY").move_to([-7.1, -1.45, 0]), T("A2", 24, TINTA, "HEAVY").move_to([-7.1, -1.95, 0]))
        lin = cable([ct.fijos[0][2].get_center(), ct.fijos[0][2].get_center() + UP * 1.6], C_POT, w=12, etiqueta="L1")
        lout = cable([ct.fijos[1][2].get_center(), ct.fijos[1][2].get_center() + UP * 1.6], C_POT, w=12, etiqueta="T1")
        self.add(lin, lout)
        self.play(Create(a1), Create(a2), FadeIn(la), Create(lin), Create(lout), run_time=0.7)
        pasos = VGroup(*[T(t_, 26, TINTA, "BOLD") for t_ in ("1 · tensión en A1–A2", "2 · la bobina crea flujo", "3 · el núcleo atrae a la armadura",
                                                             "4 · los contactos se cierran", "5 · sin tensión: el resorte la regresa")]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.3, 0.8, 0])
        self.esperar_frac(0.05)
        self.play(FadeIn(pasos[0], shift=LEFT * 0.1), run_time=0.3)
        ca = corriente([[-6.6, -1.45, 0], ct.bob.get_left() + LEFT * 1.0 + UP * 0.25, ct.bob.get_left() + UP * 0.25], vel=1.0, escala=1.0, color=ROJO_C)
        self.add(ca)
        self.play(ct.bob[0].animate.set_fill("#E8955A"), run_time=0.4)
        flujo = VGroup(*[RoundedRectangle(width=w_, height=h_, corner_radius=0.3).set_stroke(VIOLETA, 3).move_to(ct.nuc.get_center() + UP * 0.35)
                         for w_, h_ in ((1.5, 1.5), (2.7, 1.9))])
        for f_ in flujo:
            f_.set_stroke(opacity=0.0)
        flujo_d = VGroup(*[DashedVMobject(RoundedRectangle(width=w_, height=h_, corner_radius=0.3), num_dashes=26).set_stroke(VIOLETA, 3)
                           .move_to([ct.nuc.get_center()[0] + s_ * w_ / 2 * 0.0 + s_ * 0.9, ct.nuc.get_center()[1] + 0.45, 0]) for s_, w_, h_ in ((-1, 1.6, 1.7), (1, 1.6, 1.7))])
        self.play(FadeIn(pasos[1], shift=LEFT * 0.1), Create(flujo_d), run_time=0.7)
        self.esperar_frac(0.1)
        self.play(FadeIn(pasos[2], shift=LEFT * 0.1), run_time=0.3)
        self.sfx("tic", -6)
        self.mover_corte(ct, True, 0.3)
        self.play(FadeIn(pasos[3], shift=LEFT * 0.1), run_time=0.3)
        cp = corriente([lin.ruta.get_end(), ct.fijos[0][2].get_center(), ct.fijos[0][1].get_center(), ct.pu.get_center() + LEFT * 1.2, ct.pu.get_center() + RIGHT * 1.2,
                        ct.fijos[1][1].get_center(), ct.fijos[1][2].get_center(), lout.ruta.get_end()], vel=1.4, escala=1.3)
        self.add(cp)
        mo = motor_3f(0.55).move_to([2.4, 3.3, 0])
        self.play(FadeIn(mo), run_time=0.3)
        self.esperar_frac(0.35)
        self.play(FadeIn(pasos[4], shift=LEFT * 0.1), run_time=0.3)
        self.remove(ca, cp)
        self.play(FadeOut(flujo_d), ct.bob[0].animate.set_fill(CU), run_time=0.3)
        self.mover_corte(ct, False, 0.35)
        ms = pastilla("cierre: 12 a 22 ms", MARCA, 26, True).move_to([4.3, -2.4, 0])
        src = fuente("Ficha técnica Schneider Electric LC1D18 · tiempos de maniobra", [4.3, -3.2, 0], 18)
        self.esperar_frac(0.3)
        self.play(FadeIn(ms), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ct, a1, a2, la, lin, lout, pasos, mo, ms, src)

    # ------------------------------------------------------------------ 6 · núcleo laminado
    def f_laminas(self):
        self.voz("laminas")
        sol = Rectangle(width=3.6, height=3.0, stroke_color="#5B6573", stroke_width=3).set_fill("#8C96A3", 1).move_to([-3.6, 0.4, 0])
        lam = VGroup(*[Rectangle(width=3.6, height=0.24, stroke_color="#3A4250", stroke_width=1.3).set_fill("#A7B0BC", 1) for _ in range(12)]).arrange(DOWN, buff=0.025).move_to([3.6, 0.4, 0])
        ls = T("bloque sólido", 30, TINTA, "HEAVY").next_to(sol, DOWN, buff=0.3)
        ll_ = T("chapas de acero al silicio aisladas", 28, TINTA, "HEAVY").next_to(lam, DOWN, buff=0.3).align_to(ls, UP)
        self.play(FadeIn(sol), FadeIn(lam), FadeIn(ls), FadeIn(ll_), run_time=0.5)
        rem = VGroup(*[Circle(radius=r).set_stroke(ROJO_C, 5).move_to(sol) for r in (0.5, 0.95, 1.35)])
        flechas = VGroup(*[Arrow(rem[2].point_at_angle(a), rem[2].point_at_angle(a + 0.4), buff=0, color=ROJO_C, stroke_width=4, max_tip_length_to_length_ratio=0.5)
                           for a in (0.3, 2.4, 4.5)])
        self.esperar_frac(0.15)
        self.play(LaggedStart(*[Create(r) for r in rem], lag_ratio=0.2), FadeIn(flechas), run_time=0.8)
        fo = pastilla("corrientes de Foucault", ROJO_C, 26, True).move_to([-3.6, 2.4, 0])
        gl = resplandor(sol.get_center(), 2.0, CALOR if 'CALOR' in globals() else "#FF6B3D", 10, 0.05)
        self.play(FadeIn(fo), FadeIn(gl), run_time=0.4)
        self.esperar_frac(0.35)
        rem2 = VGroup(*[Ellipse(width=3.0, height=0.12).set_stroke(ROJO_C, 2.4).move_to(l) for l in lam])
        self.play(LaggedStart(*[Create(r) for r in rem2], lag_ratio=0.04), run_time=0.8)
        ok = pastilla("mucho menos calor y pérdidas", VERDE_OK, 26, True).move_to([3.6, 2.4, 0])
        self.play(FadeIn(ok), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(sol, lam, ls, ll_, rem, flechas, fo, gl, rem2, ok)

    # ------------------------------------------------------------------ 7 · espira de sombra
    def f_anillo(self):
        self.voz("anillo")
        ax = Axes(x_range=[0, 2, 0.5], y_range=[-1.1, 1.1, 1], x_length=7.2, y_length=2.2, tips=False,
                  axis_config={"color": TINTA2, "stroke_width": 2, "include_ticks": False}).move_to([2.6, 2.0, 0])
        ax2 = Axes(x_range=[0, 2, 0.5], y_range=[0, 1.2, 1], x_length=7.2, y_length=2.0, tips=False,
                   axis_config={"color": TINTA2, "stroke_width": 2, "include_ticks": False}).move_to([2.6, -1.4, 0])
        fi = ax.plot(lambda t: np.sin(TAU * t), x_range=[0, 2], color=CIAN_CORRIENTE, stroke_width=4)
        lfi = T("flujo Φ (60 Hz)", 24, CIAN_CORRIENTE, "BOLD").next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        fu = ax2.plot(lambda t: np.sin(TAU * t) ** 2, x_range=[0, 2], color=AMBAR, stroke_width=4)
        lfu = T("fuerza ∝ Φ²", 24, AMBAR, "BOLD").next_to(ax2, UP, buff=0.05).align_to(ax2, LEFT)
        # cara del polo con anillo (vista superior)
        polo = Rectangle(width=2.6, height=1.8, stroke_color="#5B6573", stroke_width=2).set_fill("#9AA3AF", 1).move_to([-4.8, 0.6, 0])
        lams = VGroup(*[Line(polo.get_left() + RIGHT * 0.05 + UP * y, polo.get_right() + LEFT * 0.05 + UP * y).set_stroke("#6B7280", 1) for y in np.linspace(-0.8, 0.8, 9)])
        anillo_ = Rectangle(width=1.2, height=1.9, stroke_color="#7A3B12", stroke_width=10).move_to(polo.get_center() + RIGHT * 0.55)
        anillo_.set_stroke(CU, 9)
        lp = T("cara del núcleo", 24, TINTA, "BOLD").next_to(polo, UP, buff=0.2)
        self.play(FadeIn(polo), FadeIn(lams), FadeIn(lp), Create(ax), Create(ax2), run_time=0.5)
        self.play(Create(fi), FadeIn(lfi), run_time=1.0)
        self.esperar_frac(0.08)
        self.play(Create(fu), FadeIn(lfu), run_time=1.0)
        ceros = VGroup(*[Dot(ax2.c2p(t, 0), radius=0.09, color=ROJO_C) for t in (0, 0.5, 1.0, 1.5, 2.0)])
        n120 = pastilla("fuerza = 0 · 120 veces por segundo", ROJO_C, 24, True).move_to([2.6, -3.0, 0])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in ceros], lag_ratio=0.15), FadeIn(n120), run_time=0.8)
        vib = pastilla("vibración y zumbido", ROJO_C, 24, True).next_to(polo, DOWN, buff=0.4)
        self.play(FadeIn(vib), Wiggle(polo, scale_value=1.02, rotation_angle=0.02), run_time=0.8)
        self.esperar_frac(0.25)
        self.play(Create(anillo_), FadeOut(vib), run_time=0.6)
        la = pastilla("espira de sombra (anillo de cobre)", CU, 24, True).next_to(polo, DOWN, buff=0.4)
        self.play(FadeIn(la), run_time=0.3)
        fi2 = ax.plot(lambda t: 0.75 * np.sin(TAU * t - PI / 2.2), x_range=[0, 2], color=CU, stroke_width=3.5)
        fu2 = ax2.plot(lambda t: np.sin(TAU * t) ** 2 * 0.62 + 0.75 ** 2 * np.sin(TAU * t - PI / 2.2) ** 2 * 0.75 + 0.05, x_range=[0, 2], color=VERDE_OK, stroke_width=5)
        self.esperar_frac(0.2)
        self.play(Create(fi2), run_time=0.8)
        self.play(Create(fu2), FadeOut(ceros), FadeOut(n120), run_time=0.9)
        ok = pastilla("la fuerza total nunca llega a cero", VERDE_OK, 24, True).move_to([2.6, -3.0, 0])
        self.play(FadeIn(ok), run_time=0.3)
        src = fuente("Schneider/Telemecanique · Conmutación todo o nada, p. 25", [2.6, -3.75, 0], 18)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz()
        self.limpiar(ax, ax2, fi, lfi, fu, lfu, polo, lams, anillo_, lp, la, fi2, fu2, ok, src)

    # ------------------------------------------------------------------ 8 · corriente de llamada
    def f_llamada(self):
        self.voz("llamada")
        izq = self.corte(-4.0, 0.9)
        izq.scale(0.62, about_point=[-4.0, 0.9, 0])
        der = self.corte(4.0, 0.9)
        der.scale(0.62, about_point=[4.0, 0.9, 0])
        self.play(FadeIn(izq), FadeIn(der), run_time=0.5)
        der.movil.shift(DOWN * der.gap * 0.62)
        for r_ in der.resortes:
            r_.stretch_to_fit_height(0.06).move_to([r_.get_center()[0], der.arm.get_bottom()[1] - 0.03, 0])
        aire = VGroup(*[Rectangle(width=0.5, height=izq.gap * 0.62, stroke_color=AMBAR, stroke_width=2).set_fill(AMBAR, 0.25)
                        .move_to([x, izq.arm.get_bottom()[1] - izq.gap * 0.31, 0]) for x in (-4.0 - 0.95, -4.0, -4.0 + 0.95)])
        la = pastilla("espacio de aire: se opone al flujo", AMBAR, 22, True).next_to(izq, DOWN, buff=0.15)
        t1 = T("ABIERTO (llamada)", 28, TINTA, "HEAVY").next_to(izq, UP, buff=0.1)
        t2 = T("CERRADO (mantenimiento)", 28, TINTA, "HEAVY").next_to(der, UP, buff=0.1)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.3)
        self.esperar_frac(0.1)
        self.play(FadeIn(aire), FadeIn(la), run_time=0.5)
        self.esperar_frac(0.25)
        # barras VA
        b1 = Rectangle(width=0.9, height=70 / 70 * 2.2, stroke_width=0).set_fill(ROJO_C, 0.95).move_to([-1.0, -2.8, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=0.9, height=7.5 / 70 * 2.2, stroke_width=0).set_fill(VERDE_OK, 1).move_to([1.0, -2.8, 0], aligned_edge=DOWN)
        e1 = T("70 VA", 30, ROJO_C, "HEAVY").next_to(b1, UP, buff=0.08)
        e2 = T("7,5 VA", 30, VERDE_OK, "HEAVY").next_to(b2, UP, buff=0.08)
        base_ = Line([-2.0, -2.8, 0], [2.0, -2.8, 0]).set_stroke(TINTA2, 2)
        self.play(FadeOut(la), Create(base_), GrowFromEdge(b1, DOWN), FadeIn(e1), run_time=0.6)
        self.esperar_frac(0.2)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(e2), run_time=0.5)
        x10 = pastilla("casi 10 veces menos", VERDE_OK, 26, True).move_to([0, -3.6, 0])
        src = fuente("Ficha LC1D18 · bobina a 60 Hz", [0, -4.15, 0], 18)
        self.play(FadeIn(x10), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(izq, der, aire, t1, t2, b1, b2, e1, e2, base_, x10, src)

    # ------------------------------------------------------------------ 9 · polos y doble corte
    def f_contactos(self):
        self.voz("contactos")
        ct = self.corte(0.0, -0.4)
        self.play(FadeIn(ct), run_time=0.4)
        self.ir([0, 1.4, 0], 9.5, 1.0)
        z = self.z
        pads = VGroup(ct.pu[1], *[f_[1] for f_ in ct.fijos])
        lp = self.chip("aleación de plata", ct.cam.get_left() + LEFT * 1.3 * z + UP * 0.2 * z, AMBAR, 22, True)
        flp = Line(lp.get_right(), ct.fijos[0][1].get_center(), stroke_width=2, color=AMBAR)
        self.play(Indicate(pads, color=WHITE, scale_factor=1.3), FadeIn(lp), Create(flp), run_time=0.8)
        self.esperar_frac(0.2)
        r_p = resorte(0.5, 0.3, 5, "#C7CCD6", 2.4).move_to(ct.pu.get_top() + UP * 0.3)
        lr = self.chip("resorte de presión", ct.cam.get_right() + RIGHT * 1.2 * z + UP * 0.2 * z, TINTA2, 20, True)
        flr = Line(lr.get_left(), r_p.get_right(), stroke_width=2, color=TINTA2)
        self.play(FadeIn(r_p), FadeIn(lr), Create(flr), run_time=0.5)
        self.esperar_frac(0.3)
        g1 = DoubleArrow(ct.fijos[0][1].get_top(), ct.pu[1][0].get_bottom(), buff=0.02, color=AMBAR, stroke_width=3, tip_length=0.12)
        g2 = DoubleArrow(ct.fijos[1][1].get_top(), ct.pu[1][1].get_bottom(), buff=0.02, color=AMBAR, stroke_width=3, tip_length=0.12)
        ld = self.chip("DOBLE CORTE: abre en 2 puntos", [0, ct.cam.get_bottom()[1] - 0.55 * z, 0], MARCA, 22, True)
        self.play(GrowFromCenter(g1), GrowFromCenter(g2), FadeIn(ld), run_time=0.6)
        arcos = VGroup(*[rayo(ct.fijos[i][1].get_top(), ct.pu[1][i].get_bottom(), color=AMBAR, semilla=i, amp=0.05) for i in (0, 1)])
        self.play(FadeIn(arcos), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(ct, lp, flp, r_p, lr, flr, g1, g2, ld, arcos)
        self.ir(ORIGIN, 16, 0.6)

    # ------------------------------------------------------------------ 10 · arco eléctrico y cámara
    def f_arco(self):
        self.voz("arco")
        f1 = Rectangle(width=2.6, height=0.4, stroke_color="#7A3B12", stroke_width=1.4).set_fill(CU, 1).move_to([-3.4, -1.6, 0])
        m1 = Rectangle(width=2.6, height=0.4, stroke_color="#7A3B12", stroke_width=1.4).set_fill(CU, 1).move_to([-3.4, -0.9, 0])
        pad1 = RoundedRectangle(width=0.6, height=0.14, corner_radius=0.03, stroke_width=0).set_fill(AG, 1).move_to(f1.get_top() + UP * 0.07 + RIGHT * 0.8)
        pad2 = RoundedRectangle(width=0.6, height=0.14, corner_radius=0.03, stroke_width=0).set_fill(AG, 1).move_to(m1.get_bottom() + DOWN * 0.07 + RIGHT * 0.8)
        movil = VGroup(m1, pad2)
        self.play(FadeIn(f1), FadeIn(pad1), FadeIn(movil), run_time=0.4)
        self.play(movil.animate.shift(UP * 1.2), run_time=0.8)
        arco_ = VGroup(*[rayo(pad1.get_top(), pad2.get_bottom(), color=c_, semilla=k, amp=0.12, w=w_) for k, (c_, w_) in enumerate(((AMBAR, 8), (WHITE, 3)))])
        glow = resplandor((pad1.get_top() + pad2.get_bottom()) / 2, 1.0, AMBAR, 10, 0.08)
        self.sfx("pop", -8)
        self.play(FadeIn(arco_), FadeIn(glow), run_time=0.3)
        tt = pastilla("plasma: varios miles de °C", AMBAR, 24, True).move_to([-3.4, 1.6, 0])
        self.play(FadeIn(tt), run_time=0.3)
        self.esperar_frac(0.2)
        # cámara con plaquetas
        cam = RoundedRectangle(width=4.4, height=3.6, corner_radius=0.12, stroke_color="#6B7280", stroke_width=2).set_fill("#2A2F3A", 0.7).move_to([3.6, 0.4, 0])
        plq = VGroup(*[Rectangle(width=3.0, height=0.1, stroke_width=0).set_fill("#A7AFBA", 1).move_to([3.6, 0.4 + 0.3 * (j - 3), 0]) for j in range(7)])
        lc = T("plaquetas de la cámara apagachispas", 24, TINTA, "BOLD").next_to(cam, UP, buff=0.15)
        self.play(FadeIn(cam), LaggedStart(*[FadeIn(p) for p in plq], lag_ratio=0.08), FadeIn(lc), run_time=0.7)
        arco_l = VGroup(*[rayo([3.6, plq[j].get_center()[1] + 0.05, 0] + LEFT * 1.6, [3.6, plq[j + 1].get_center()[1] - 0.05, 0] + LEFT * 1.6, color=AMBAR, semilla=j, amp=0.06, w=5)
                          for j in range(6)])
        largo = rayo([2.0, -1.2, 0], [2.0, 2.0, 0], color=AMBAR, amp=0.15, w=7)
        self.play(FadeIn(largo), run_time=0.3)
        self.play(ReplacementTransform(largo, arco_l), run_time=0.8)
        div = pastilla("lo alarga, lo divide y lo enfría", MARCA, 24, True).next_to(cam, DOWN, buff=0.2)
        self.play(FadeIn(div), run_time=0.3)
        self.esperar_frac(0.25)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-1.1, 1.1, 1], x_length=4.0, y_length=1.4, tips=False,
                  axis_config={"color": TINTA2, "stroke_width": 2, "include_ticks": False}).move_to([-3.4, -3.3, 0])
        sen = ax.plot(lambda t: np.sin(TAU * t), x_range=[0, 1], color=CIAN_CORRIENTE, stroke_width=4)
        cero = Dot(ax.c2p(0.5, 0), radius=0.1, color=VERDE_OK)
        lz = T("I = 0: el arco se apaga", 22, VERDE_OK, "BOLD").next_to(ax, RIGHT, buff=0.2)
        self.play(Create(ax), Create(sen), run_time=0.6)
        self.play(FadeIn(cero, scale=2), FadeIn(lz), FadeOut(arco_), FadeOut(glow), FadeOut(arco_l), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(f1, pad1, movil, tt, cam, plq, lc, div, ax, sen, cero, lz)

    # ------------------------------------------------------------------ 11 · bornes y marcado
    def f_bornes(self):
        self.voz("bornes")
        rl = riel_din(5.0, 1.5).move_to([-3.8, -0.1, 0])
        ct = contactor_frente(1.6).move_to([-3.8, -0.1, 0])
        self.play(FadeIn(rl), FadeIn(ct, shift=UP * 0.2), run_time=0.6)
        sup = VGroup(*[ct.b[n] for n in ("1/L1", "3/L2", "5/L3")])
        inf = VGroup(*[ct.b[n] for n in ("2/T1", "4/T2", "6/T3")])
        c1 = caja_info("ALIMENTACIÓN (arriba)", ["1/L1 · 3/L2 · 5/L3", "números impares"], AMBAR, 5.2, 24).move_to([3.6, 2.6, 0])
        c2 = caja_info("CARGA (abajo)", ["2/T1 · 4/T2 · 6/T3", "números pares"], VERDE_OK, 5.2, 24).move_to([3.6, 0.6, 0])
        r1 = SurroundingRectangle(sup, color=AMBAR, buff=0.08, corner_radius=0.1)
        r2 = SurroundingRectangle(inf, color=VERDE_OK, buff=0.08, corner_radius=0.1)
        self.esperar_frac(0.04)
        self.play(Create(r1), FadeIn(c1, shift=LEFT * 0.2), run_time=0.5)
        self.esperar_frac(0.06)
        self.play(Create(r2), FadeIn(c2, shift=LEFT * 0.2), run_time=0.5)
        self.esperar_frac(0.08)
        rb = SurroundingRectangle(VGroup(ct.b["A1"], ct.b["A2"]), color=ROJO_C, buff=0.06, corner_radius=0.08)
        c3 = caja_info("BOBINA", ["A1 – A2"], ROJO_C, 5.2, 24).move_to([3.6, -1.2, 0])
        self.play(FadeOut(r1), FadeOut(r2), Create(rb), FadeIn(c3, shift=LEFT * 0.2), run_time=0.5)
        self.esperar_frac(0.1)
        ra = SurroundingRectangle(VGroup(ct.b["13"], ct.b["14"], ct.b["21"], ct.b["22"]), color=MARCA, buff=0.06, corner_radius=0.08)
        c4 = caja_info("AUXILIARES (2 cifras)", ["decena = número de orden", "unidad = función:", "1-2 NC (cerrado) · 3-4 NA (abierto)", "13-14 = NA · 21-22 = NC"], MARCA, 5.2, 22).move_to([3.6, -3.0, 0])
        self.play(FadeOut(rb), Create(ra), FadeOut(c1), FadeOut(c2), c3.animate.move_to([3.6, 2.8, 0]), run_time=0.5)
        c4.move_to([3.6, 0.6, 0])
        self.play(FadeIn(c4, shift=LEFT * 0.2), run_time=0.5)
        self.esperar_frac(0.35)
        # puntera y par de apriete (zoom a un borne)
        self.play(FadeOut(ra), FadeOut(c3), FadeOut(c4), run_time=0.3)
        b = ct.b["1/L1"]
        cab = cable([b.entrada.get_center(), b.entrada.get_center() + UP * 1.4], C_POT, w=16, etiqueta="L1")
        self.add(cab)
        self.bring_to_front(ct)
        self.play(Create(cab), run_time=0.5)
        self.ir(b.get_center() + UP * 0.35 + RIGHT * 0.9, 4.6, 1.0)
        z = self.z
        lp = self.chip("puntera + marquilla", b.get_center() + UP * 1.35 + RIGHT * 1.3, MARCA, 22, True)
        self.play(FadeIn(lp), run_time=0.3)
        self.apretar(b.tor, 1.0)
        par = self.chip("par: 1,7 N·m (contactor de 12 A)", b.get_center() + UP * 0.75 + RIGHT * 2.0, AMBAR, 22, True)
        src = self.chip("ficha LC1D12 · Schneider Electric", par.get_center() + DOWN * 0.42 * z, TINTA2, 16, False)
        self.play(FadeIn(par), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(rl, ct, cab, lp, par, src)
        self.ir(ORIGIN, 16, 0.5)

    # ------------------------------------------------------------------ 12 · símbolos IEC 60617
    def f_simbolos(self):
        self.voz("simbolos")
        self.camera.frame.set(width=12.8).move_to([-0.2, 0.1, 0])
        tit = T("SÍMBOLOS · IEC 60617", 34, TINTA, "HEAVY").move_to([-0.2, 3.15, 0])
        self.play(FadeIn(tit), run_time=0.3)
        bob = sim_bobina("KM1").scale(1.4).move_to([-5.2, 0.2, 0])
        lb = T("bobina", 24, TINTA2, "BOLD").next_to(bob, DOWN, buff=0.3)
        self.play(FadeIn(bob), FadeIn(lb), run_time=0.5)
        self.esperar_frac(0.1)
        pri = VGroup(*[sim_contacto(True, contactor=True, n1=a, n2=b, largo=1.4) for a, b in (("1", "2"), ("3", "4"), ("5", "6"))]).arrange(RIGHT, buff=0.75).move_to([-1.0, 0.2, 0])
        lk = T("KM1", 26, SIM, "HEAVY").next_to(pri, LEFT, buff=0.3)
        link = DashedLine(pri[0].cuchilla.get_center(), pri[2].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2)
        lp = T("contactos principales", 24, TINTA2, "BOLD").next_to(pri, DOWN, buff=0.3)
        self.play(FadeIn(pri), FadeIn(lk), FadeIn(lp), run_time=0.5)
        semis = VGroup(*[SurroundingRectangle(p[-3] if False else p[4], color=AMBAR, buff=0.05) for p in pri])
        nota = pastilla("semicírculo = contacto de contactor", AMBAR, 20, True).move_to([-1.0, 2.2, 0])
        self.play(Create(semis), FadeIn(nota), run_time=0.5)
        self.esperar_frac(0.25)
        aux = VGroup(sim_contacto(True, n1="13", n2="14", largo=1.4), sim_contacto(False, n1="21", n2="22", largo=1.4)).arrange(RIGHT, buff=0.9).move_to([4.6, 0.2, 0])
        lka = T("KM1", 26, SIM, "HEAVY").next_to(aux, LEFT, buff=0.3)
        la = T("auxiliares NA y NC", 24, TINTA2, "BOLD").next_to(aux, DOWN, buff=0.3)
        self.play(FadeOut(semis), FadeIn(aux), FadeIn(lka), FadeIn(la), run_time=0.5)
        self.esperar_frac(0.35)
        self.play(Create(link), Indicate(VGroup(lk, lka, bob[-1]), color=AMBAR), run_time=0.7)
        mismo = pastilla("misma identificación: KM1 · línea discontinua = se mueven juntos", MARCA, 20, True).move_to([-0.2, -2.6, 0])
        self.play(FadeIn(mismo), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(tit, bob, lb, pri, lk, link, lp, nota, aux, lka, la, mismo)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    # ------------------------------------------------------------------ 13 · circuito de mando
    def f_mando(self):
        self.voz("mando")
        X0, YT, YB = -3.6, 3.3, -3.5
        top = Line([X0 - 1.6, YT, 0], [X0 + 2.6, YT, 0]).set_stroke(ROJO_C, 4)
        bot = Line([X0 - 1.6, YB, 0], [X0 + 2.6, YB, 0]).set_stroke(TINTA, 4)
        lt = T("L · 120 V (mando)", 22, ROJO_C, "HEAVY").next_to(top, UP, buff=0.08).align_to(top, LEFT)
        lbt = T("N", 22, TINTA, "HEAVY").next_to(bot, DOWN, buff=0.08).align_to(bot, LEFT)
        f2 = sim_termico_contacto().move_to([X0, 2.4, 0])
        s1 = sim_pulsador(False, ref="S1", n1="11", n2="12").move_to([X0, 1.0, 0])
        s2 = sim_pulsador(True, ref="S2", n1="13", n2="14").move_to([X0, -0.6, 0])
        km_a = sim_contacto(True, n1="13", n2="14").move_to([X0 + 1.8, -0.6, 0])
        lka = T("KM1", 20, SIM, "HEAVY").next_to(km_a, RIGHT, buff=0.35)
        bob = sim_bobina("KM1").move_to([X0, -2.5, 0])
        for m_ in (f2, s1, s2, bob):
            alinear(m_, X0)
        alinear(km_a, X0 + 1.8)
        lka.next_to(km_a, RIGHT, buff=0.35)
        w = lambda a, b: Line(a, b).set_stroke(SIM, SW)
        cables_ = VGroup(w([X0, YT, 0], f2[0].get_start()), w(f2[1].get_end(), s1[0].get_start()), w(s1[1].get_end(), s2[0].get_start()),
                         w(s2[1].get_end(), bob[0].get_start()), w(bob[2].get_end(), [X0, YB, 0]),
                         w(s2[0].get_start() + DOWN * 0.0, [X0 + 1.8, s2[0].get_start()[1], 0]), w([X0 + 1.8, s2[0].get_start()[1], 0], km_a[0].get_start()),
                         w(km_a[1].get_end(), [X0 + 1.8, s2[1].get_end()[1], 0]), w([X0 + 1.8, s2[1].get_end()[1], 0], s2[1].get_end()))
        nodos = VGroup(*[Dot(p, radius=0.06, color=SIM) for p in (s2[0].get_start(), s2[1].get_end())])
        circ = VGroup(top, bot, lt, lbt, f2, s1, s2, km_a, lka, bob, cables_, nodos)
        self.play(Create(VGroup(top, bot)), FadeIn(VGroup(lt, lbt)), run_time=0.4)
        self.play(LaggedStart(FadeIn(f2), FadeIn(s1), FadeIn(s2), FadeIn(bob), Create(cables_), FadeIn(km_a), FadeIn(lka), FadeIn(nodos), lag_ratio=0.15), run_time=1.6)
        # botonera real (IEC 60204-1: paro negro preferente, marcha blanco preferente)
        bot_p = pulsador_fis("#1F2430", "O", 1.0).move_to([2.6, 1.9, 0])
        bot_m = pulsador_fis("#F2F4F7", "I", 1.0).move_to([5.9, 1.9, 0])
        lbp = VGroup(T("S1 · PARO", 22, TINTA, "HEAVY"), T("negro (rojo permitido)", 18, TINTA2, "BOLD")).arrange(DOWN, buff=0.05).next_to(bot_p, DOWN, buff=0.15)
        lbm = VGroup(T("S2 · MARCHA", 22, TINTA, "HEAVY"), T("blanco (verde permitido)", 18, TINTA2, "BOLD")).arrange(DOWN, buff=0.05).next_to(bot_m, DOWN, buff=0.15)
        src = fuente("Colores: IEC 60204-1 · Símbolos: IEC 60617", [4.2, -3.9, 0], 18)
        self.play(FadeIn(bot_p), FadeIn(bot_m), FadeIn(lbp), FadeIn(lbm), FadeIn(src), run_time=0.5)
        estado = T("", 24)
        e_box = caja_info("estado", ["motor detenido"], TINTA2, 4.6, 24).move_to([4.2, -1.5, 0])
        self.play(FadeIn(e_box), run_time=0.3)

        def set_estado(txt, col):
            nuevo = caja_info("estado", [txt], col, 4.6, 24).move_to(e_box)
            return Transform(e_box, nuevo)
        self.esperar_frac(0.12)
        # presionar marcha
        self.play(bot_m[2].animate.scale(0.9), accionar(s2, True), run_time=0.3)
        p1 = [[X0, YT, 0], [X0, s2[0].get_start()[1], 0], [X0, YB + 0.0, 0]]
        cur1 = corriente([[X0, YT, 0], f2[0].get_start(), s1[1].get_end(), s2[0].get_start(), s2[1].get_end(), bob[0].get_start(), bob[2].get_end(), [X0, YB, 0]],
                         vel=1.2, escala=1.0, color=ROJO_C)
        self.add(cur1)
        self.sfx("tic", -6)
        self.play(accionar(km_a, True), bob.rect.animate.set_fill(ROJO_C, 0.5), set_estado("bobina energizada · motor en marcha", VERDE_OK), run_time=0.4)
        self.esperar_frac(0.18)
        # soltar marcha: queda autoenclavado por KM1 13-14
        self.play(bot_m[2].animate.scale(1 / 0.9), accionar(s2, False), run_time=0.3)
        self.remove(cur1)
        cur2 = corriente([[X0, YT, 0], f2[0].get_start(), s1[1].get_end(), s2[0].get_start(), [X0 + 1.8, s2[0].get_start()[1], 0], km_a[0].get_start(),
                          km_a[1].get_end(), [X0 + 1.8, s2[1].get_end()[1], 0], s2[1].get_end(), bob[0].get_start(), bob[2].get_end(), [X0, YB, 0]],
                         vel=1.2, escala=1.0, color=ROJO_C)
        self.add(cur2)
        auto = pastilla("AUTOENCLAVAMIENTO (13-14)", AMBAR, 22, True).next_to(lka, RIGHT, buff=0.3)
        self.play(FadeIn(auto), set_estado("sigue en marcha sin el botón", VERDE_OK), run_time=0.4)
        self.esperar_frac(0.3)
        # paro
        self.play(bot_p[2].animate.scale(0.9), accionar(s1, True), run_time=0.3)
        self.remove(cur2)
        self.play(accionar(km_a, False), bob.rect.animate.set_fill(opacity=0), set_estado("paro: bobina sin tensión", ROJO_C), FadeOut(auto), run_time=0.4)
        self.play(bot_p[2].animate.scale(1 / 0.9), accionar(s1, False), run_time=0.3)
        self.esperar_frac(0.4)
        ce = set_estado("corte de energía: no arranca solo", AMBAR)
        self.play(ce, run_time=0.4)
        self.cerrar_voz()
        self.limpiar(circ, bot_p, bot_m, lbp, lbm, src, e_box)

    # ------------------------------------------------------------------ 14 · circuito de potencia
    def f_potencia(self):
        self.voz("potencia")
        xs = [-3.2, -2.2, -1.2]
        L = VGroup(*[T(n, 24, TINTA, "HEAVY").move_to([x, 3.85, 0]) for x, n in zip(xs, ("L1", "L2", "L3"))])
        q1 = VGroup(*[sim_contacto(True, interruptor=True, largo=1.0, n1=str(2 * i + 1), n2=str(2 * i + 2)).move_to([x, 2.5, 0]) for i, x in enumerate(xs)])
        km = VGroup(*[sim_contacto(True, contactor=True, largo=1.0, n1=str(2 * i + 1), n2=str(2 * i + 2)).move_to([x, 0.7, 0]) for i, x in enumerate(xs)])
        f2 = VGroup(*[sim_termico_pot().move_to([x, -1.0, 0]) for x in xs])
        for i, x in enumerate(xs):
            alinear(q1[i], x)
            alinear(km[i], x)
        mot = sim_motor().scale(1.15).move_to([-2.2, -2.9, 0])
        w = lambda a, b: Line(a, b).set_stroke(SIM, SW)
        lin = VGroup()
        for i, x in enumerate(xs):
            lin.add(w([x, 3.6, 0], q1[i][0].get_start()), w(q1[i][1].get_end(), km[i][0].get_start()), w(km[i][1].get_end(), f2[i].get_top()),
                    w(f2[i].get_bottom(), mot.get_top() + RIGHT * (x + 2.2) * 0.45 + DOWN * abs(x + 2.2) * 0.1))
        lq = T("Q1", 24, SIM, "HEAVY").next_to(q1, LEFT, buff=0.3)
        lk = T("KM1", 24, SIM, "HEAVY").next_to(km, LEFT, buff=0.3)
        lf = T("F2", 24, SIM, "HEAVY").next_to(f2, LEFT, buff=0.3)
        lm = VGroup(*[T(t_, 18, SIM, "BOLD").move_to(mot.get_top() + RIGHT * (x + 2.2) * 0.45 + UP * 0.25 + RIGHT * 0.22) for x, t_ in zip(xs, ("U1", "V1", "W1"))])
        dq = DashedLine(q1[0].cuchilla.get_center(), q1[2].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2)
        dk = DashedLine(km[0].cuchilla.get_center(), km[2].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2)
        todo = VGroup(L, q1, km, f2, mot, lin, lq, lk, lf, lm, dq, dk)
        self.play(LaggedStart(FadeIn(L), FadeIn(q1), FadeIn(km), FadeIn(f2), FadeIn(mot), Create(lin), FadeIn(VGroup(lq, lk, lf, lm, dq, dk)), lag_ratio=0.1), run_time=1.6)
        notas = VGroup(caja_info("Q1 · protección contra cortocircuito", ["disyuntor o fusibles → próximo video"], ROJO_C, 6.6, 22),
                       caja_info("KM1 · contactor", ["solo conecta y desconecta"], MARCA, 6.6, 22),
                       caja_info("F2 · relé térmico", ["protección contra sobrecarga"], AMBAR, 6.6, 22)).arrange(DOWN, buff=0.3).move_to([3.9, 0.3, 0])
        self.play(FadeIn(notas[1], shift=LEFT * 0.2), Indicate(km, color=MARCA), run_time=0.5)
        self.play(*[accionar(q, True) for q in q1], run_time=0.3)
        self.play(*[accionar(k, True) for k in km], run_time=0.3)
        curs = VGroup(*[corriente([[x, 3.6, 0], [x, mot.get_top()[1] + 0.1, 0]], vel=1.0, escala=1.0) for x in xs])
        self.add(curs)
        self.esperar_frac(0.3)
        self.play(FadeIn(notas[0], shift=LEFT * 0.2), Indicate(q1, color=ROJO_C), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(FadeIn(notas[2], shift=LEFT * 0.2), Indicate(f2, color=AMBAR), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(todo, notas, curs)

    # ------------------------------------------------------------------ 15 · tensión de bobina
    def f_bobina(self):
        self.voz("bobina")
        ref = VGroup(T("LC1D", 54, TINTA, "HEAVY"), T("18", 54, AMBAR, "HEAVY"), T("G7", 54, ROJO_C, "HEAVY")).arrange(RIGHT, buff=0.08).move_to([-3.6, 2.9, 0])
        lr = VGroup(T("familia", 20, TINTA2, "BOLD").next_to(ref[0], DOWN, buff=0.12), T("calibre", 20, AMBAR, "BOLD").next_to(ref[1], DOWN, buff=0.12),
                    T("bobina", 20, ROJO_C, "BOLD").next_to(ref[2], DOWN, buff=0.12))
        self.play(FadeIn(ref), FadeIn(lr), run_time=0.5)
        nota = pastilla("la bobina = tensión del MANDO, no del motor", ROJO_C, 24, True).move_to([-3.6, 1.4, 0])
        self.play(FadeIn(nota), run_time=0.3)
        self.esperar_frac(0.15)
        codigos = [("B7", "24 V"), ("F7", "110 V"), ("G7", "120 V"), ("M7", "220 V"), ("P7", "230 V"), ("U7", "240 V")]
        filas = VGroup(*[VGroup(RoundedRectangle(width=1.1, height=0.55, corner_radius=0.1, stroke_width=0).set_fill(ROJO_C if c in ("G7", "M7", "P7") else "#4A5AA0", 1),
                                T(c, 26, WHITE, "HEAVY"), T(v + " CA · 50/60 Hz", 24, TINTA, "BOLD")) for c, v in codigos])
        for f_ in filas:
            f_[1].move_to(f_[0])
            f_[2].next_to(f_[0], RIGHT, buff=0.25)
        filas.arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([-4.2, -1.5, 0])
        src = fuente("Códigos de bobina TeSys D 09–38 · Schneider Electric FAQ FA105276", [-3.6, -4.0, 0], 16)
        self.play(LaggedStart(*[FadeIn(f_, shift=RIGHT * 0.1) for f_ in filas], lag_ratio=0.15), FadeIn(src), run_time=1.0)
        self.esperar_frac(0.2)
        # rango de operación
        x0, x1 = 1.0, 7.2
        def xp(p):
            return x0 + (x1 - x0) * p / 120
        eje = Line([x0, 0.0, 0], [x1, 0.0, 0]).set_stroke(TINTA2, 3)
        marcas = VGroup(*[VGroup(Line([xp(p), -0.1, 0], [xp(p), 0.1, 0]).set_stroke(TINTA2, 2), T(f"{p} %", 18, TINTA2, "BOLD").move_to([xp(p), -0.35, 0])) for p in (0, 30, 60, 85, 110)])
        zona_ok = Rectangle(width=xp(110) - xp(85), height=0.5, stroke_width=0).set_fill(VERDE_OK, 0.85).move_to([(xp(85) + xp(110)) / 2, 0.45, 0])
        zona_sol = Rectangle(width=xp(60) - xp(30), height=0.5, stroke_width=0).set_fill(AMBAR, 0.85).move_to([(xp(30) + xp(60)) / 2, 0.45, 0])
        lz1 = T("cierra: 85–110 % Uc (60 Hz)", 20, VERDE_OK, "HEAVY").move_to([0, 1.5, 0]).align_to(zona_ok, RIGHT)
        lz2 = T("se suelta: 30–60 % Uc", 20, AMBAR, "HEAVY").move_to([(xp(30) + xp(60)) / 2, -0.85, 0])
        tit_r = T("rango de la bobina (ficha LC1D18)", 24, TINTA, "HEAVY").move_to([(x0 + x1) / 2, 2.3, 0])
        self.play(FadeIn(tit_r), Create(eje), FadeIn(marcas), run_time=0.5)
        self.play(GrowFromEdge(zona_ok, LEFT), FadeIn(lz1), run_time=0.5)
        self.play(GrowFromEdge(zona_sol, LEFT), FadeIn(lz2), run_time=0.5)
        self.esperar_frac(0.3)
        aguja = Triangle().scale(0.16).rotate(PI).set_fill(TINTA, 1).set_stroke(width=0).move_to([xp(100), 0.95, 0])
        self.play(FadeIn(aguja), run_time=0.2)
        self.play(aguja.animate.move_to([xp(72), 0.95, 0]), run_time=1.0)
        reb = VGroup(*[rayo([xp(72) - 0.3 + 0.3 * k, -1.4, 0], [xp(72) - 0.2 + 0.3 * k, -2.0, 0], color=AMBAR, semilla=k, amp=0.05) for k in range(3)])
        lreb = pastilla("no cierra del todo: rebotes → soldadura", ROJO_C, 22, True).move_to([(x0 + x1) / 2, -2.6, 0])
        self.sfx("pop", -12)
        self.play(FadeIn(reb), FadeIn(lreb), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ref, lr, nota, filas, src, eje, marcas, zona_ok, zona_sol, lz1, lz2, tit_r, aguja, reb, lreb)

    # ------------------------------------------------------------------ 16 · categorías de empleo
    def f_categorias(self):
        self.voz("categorias")
        tit = T("CATEGORÍAS DE EMPLEO · IEC 60947-4-1", 36, TINTA, "HEAVY").move_to([0, 3.7, 0])
        self.play(FadeIn(tit), run_time=0.3)

        def ic_res():
            return horno(0.55)

        def ic_anillos():
            m = motor_3f(0.45)
            an = VGroup(*[Rectangle(width=0.08, height=0.5, stroke_width=0).set_fill(LATON, 1).move_to(m.eje.get_center() + LEFT * 0.12 * k + RIGHT * 0.1) for k in range(3)])
            return VGroup(m, an)

        def ic_jaula():
            return motor_3f(0.5)

        def ic_inch():
            m = motor_3f(0.45)
            fl = VGroup(CurvedArrow(m.get_top() + LEFT * 0.4 + UP * 0.2, m.get_top() + RIGHT * 0.4 + UP * 0.2, angle=-1.2, color=AMBAR, stroke_width=4),
                        CurvedArrow(m.get_bottom() + RIGHT * 0.4 + DOWN * 0.2, m.get_bottom() + LEFT * 0.4 + DOWN * 0.2, angle=-1.2, color=AMBAR, stroke_width=4))
            return VGroup(m, fl)
        datos = [("AC-1", "resistencias, hornos", "poco inductivo", ic_res, VERDE_OK), ("AC-2", "motores de", "anillos rozantes", ic_anillos, MARCA),
                 ("AC-3", "motores de jaula", "arranque y paro girando", ic_jaula, AMBAR), ("AC-4", "jaula: frenado por", "contracorriente e impulsos", ic_inch, ROJO_C)]
        cartas = VGroup()
        for cod, t1, t2, fn, col in datos:
            caja = tarjeta(3.5, 4.4, color="#4A5AA0")
            cab = RoundedRectangle(width=3.5, height=0.8, corner_radius=0.18, stroke_width=0).set_fill(col, 1).move_to(caja.get_top() + DOWN * 0.4)
            tc = T(cod, 40, WHITE if col != AMBAR else "#1D2939", "HEAVY").move_to(cab)
            il = fn()
            il.scale_to_fit_width(2.4) if il.width > 2.4 else None
            if il.height > 1.6:
                il.scale_to_fit_height(1.6)
            il.move_to(caja.get_center() + UP * 0.05)
            tx_ = VGroup(T(t1, 20, TINTA, "BOLD"), T(t2, 20, TINTA, "BOLD")).arrange(DOWN, buff=0.06).move_to(caja.get_bottom() + UP * 0.7)
            cartas.add(VGroup(caja, cab, tc, il, tx_))
        cartas.arrange(RIGHT, buff=0.3).move_to([0, 0.6, 0])
        cortes = [0.12, 0.08, 0.08, 0.12]
        for c_, f_ in zip(cartas, cortes):
            self.esperar_frac(f_)
            self.play(FadeIn(c_, shift=UP * 0.2), run_time=0.5)
        comun = pastilla("la más común en la industria", AMBAR, 20, True).next_to(cartas[2], DOWN, buff=0.15)
        self.play(FadeIn(comun), run_time=0.3)
        self.esperar_frac(0.25)
        b1 = VGroup(T("AC-3 corta:", 26, TINTA, "BOLD"), Rectangle(width=0.9, height=0.4, stroke_width=0).set_fill(AMBAR, 1), T("1 × Ie", 26, AMBAR, "HEAVY")).arrange(RIGHT, buff=0.25)
        b2 = VGroup(T("AC-4 corta:", 26, TINTA, "BOLD"), Rectangle(width=5.4, height=0.4, stroke_width=0).set_fill(ROJO_C, 1), T("6 × Ie", 26, ROJO_C, "HEAVY")).arrange(RIGHT, buff=0.25)
        bs = VGroup(b1, b2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0, -3.3, 0])
        self.play(FadeOut(comun), FadeIn(b1, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(b2, shift=UP * 0.1), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, cartas, bs)

    # ------------------------------------------------------------------ 17 · datos de placa reales
    def f_placa(self):
        self.voz("placa")
        ct = contactor_frente(1.15, "18").move_to([-5.4, 0.2, 0])
        self.play(FadeIn(ct, shift=RIGHT * 0.2), run_time=0.4)
        filas = [("Ie AC-3 (≤ 440 V)", "18 A", AMBAR), ("Ie AC-1", "32 A", VERDE_OK), ("Motor AC-3 · 220–230 V", "4 kW", TINTA), ("Motor AC-3 · 380–400 V", "7,5 kW", TINTA),
                 ("Tensión de aislamiento Ui", "690 V", TINTA), ("Tensión de impulso Uimp", "6 kV", TINTA), ("Poder de cierre y de corte", "300 A", TINTA),
                 ("Vida mecánica", "15 millones", MARCA), ("Vida eléctrica AC-3 (18 A)", "1,65 millones", ROJO_C)]
        tabla = VGroup()
        for i, (k, v, col) in enumerate(filas):
            fondo = Rectangle(width=8.6, height=0.62, stroke_width=0).set_fill(CARTA if i % 2 == 0 else "#22306A", 1)
            tk = T(k, 22, TINTA, "BOLD").move_to(fondo.get_left() + RIGHT * 0.2, aligned_edge=LEFT)
            tv = T(v, 24, col, "HEAVY").move_to(fondo.get_right() + LEFT * 0.2, aligned_edge=RIGHT)
            tabla.add(VGroup(fondo, tk, tv))
        tabla.arrange(DOWN, buff=0.0).move_to([2.4, 0.5, 0])
        cab = VGroup(Rectangle(width=8.6, height=0.6, stroke_width=0).set_fill("#4A5AA0", 1), T("Ficha técnica · TeSys D LC1D18 (Schneider Electric)", 22, WHITE, "HEAVY"))
        cab[1].move_to(cab[0])
        cab.next_to(tabla, UP, buff=0)
        self.play(FadeIn(cab), run_time=0.3)
        n = len(tabla)
        for i, f_ in enumerate(tabla):
            self.play(FadeIn(f_, shift=LEFT * 0.15), run_time=0.35)
            self.esperar_frac(0.75 / max(1, n - i) if i < n - 2 else 0.08)
        vid = VGroup(T("mecánica 15 M", 22, MARCA, "HEAVY"), T("eléctrica 1,65 M", 22, ROJO_C, "HEAVY"))
        b1 = Rectangle(width=6.0, height=0.3, stroke_width=0).set_fill(MARCA, 1)
        b2 = Rectangle(width=6.0 * 1.65 / 15, height=0.3, stroke_width=0).set_fill(ROJO_C, 1)
        barras = VGroup(VGroup(b1, vid[0]).arrange(RIGHT, buff=0.2), VGroup(b2, vid[1]).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([2.2, -3.75, 0])
        self.play(FadeIn(barras), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(ct, tabla, cab, barras)

    # ------------------------------------------------------------------ 18 · auxiliares e inversor
    def f_auxiliares(self):
        self.voz("auxiliares")
        ct = contactor_frente(1.2).move_to([-5.2, 0.4, 0])
        blq = VGroup(RoundedRectangle(width=1.9, height=1.1, corner_radius=0.08, stroke_color=BORDE, stroke_width=1.4).set_fill("#E5E7EB", 1),
                     *[borne_aux([x, 0.25, 0], 1.0, n) for x, n in ((-0.55, "53/NO"), (0.35, "61/NC"))],
                     *[borne_aux([x, -0.25, 0], 1.0, n) for x, n in ((-0.55, "54/NO"), (0.35, "62/NC"))])
        blq.move_to(ct.ventana.get_center() + UP * 3.0)
        self.play(FadeIn(ct), run_time=0.4)
        usos = VGroup(pastilla("autoenclavamiento", MARCA, 22, True), pastilla("luz piloto: en marcha", VERDE_OK, 22, True), pastilla("bloqueo de otro contactor", AMBAR, 22, True)).arrange(DOWN, buff=0.25).move_to([-1.0, 2.4, 0])
        for u in usos:
            self.esperar_frac(0.06)
            self.play(FadeIn(u, shift=RIGHT * 0.15), run_time=0.3)
        # enclavamiento eléctrico de un inversor
        X1, X2, YT, YB = 2.6, 5.6, 3.3, -2.6
        top = Line([X1 - 0.8, YT, 0], [X2 + 0.8, YT, 0]).set_stroke(ROJO_C, 3)
        bot = Line([X1 - 0.8, YB, 0], [X2 + 0.8, YB, 0]).set_stroke(TINTA, 3)
        nc1 = sim_contacto(False, n1="21", n2="22").move_to([X1, 1.6, 0])
        nc2 = sim_contacto(False, n1="21", n2="22").move_to([X2, 1.6, 0])
        l1 = T("KM2", 20, SIM, "HEAVY").next_to(nc1, LEFT, buff=0.15)
        l2 = T("KM1", 20, SIM, "HEAVY").next_to(nc2, LEFT, buff=0.15)
        b1 = sim_bobina("KM1").move_to([X1, -0.9, 0])
        b2 = sim_bobina("KM2").move_to([X2, -0.9, 0])
        for m_, x_ in ((nc1, X1), (b1, X1), (nc2, X2), (b2, X2)):
            alinear(m_, x_)
        l1.next_to(nc1, LEFT, buff=0.15)
        l2.next_to(nc2, LEFT, buff=0.15)
        w = lambda a, b: Line(a, b).set_stroke(SIM, SW)
        lin = VGroup(w([X1, YT, 0], nc1[0].get_start()), w(nc1[1].get_end(), b1[0].get_start()), w(b1[2].get_end(), [X1, YB, 0]),
                     w([X2, YT, 0], nc2[0].get_start()), w(nc2[1].get_end(), b2[0].get_start()), w(b2[2].get_end(), [X2, YB, 0]))
        t_inv = T("inversor de giro: enclavamiento", 22, TINTA, "HEAVY").next_to(top, UP, buff=0.12)
        self.play(FadeIn(VGroup(top, bot, nc1, nc2, l1, l2, b1, b2, lin, t_inv)), run_time=0.8)
        self.esperar_frac(0.15)
        self.play(b1.rect.animate.set_fill(ROJO_C, 0.5), accionar(nc2, False), run_time=0.4)
        bloq = pastilla("KM1 cerrado → KM2 bloqueado", AMBAR, 22, True).move_to([(X1 + X2) / 2, -3.3, 0])
        self.play(FadeIn(bloq), run_time=0.3)
        nunca = pastilla("nunca los dos: cortocircuito entre fases", ROJO_C, 22, True).move_to([(X1 + X2) / 2, -3.95, 0])
        self.esperar_frac(0.2)
        self.play(FadeIn(nunca), run_time=0.3)
        self.esperar_frac(0.3)
        self.play(FadeIn(blq, shift=DOWN * 0.3), run_time=0.3)
        self.play(blq.animate.move_to(ct.ventana.get_center() + UP * 0.05), run_time=0.6)
        lb = pastilla("bloque auxiliar frontal", MARCA, 20, True).next_to(ct, DOWN, buff=0.2)
        self.sfx("tic", -8)
        self.play(FadeIn(lb), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(ct, blq, usos, top, bot, nc1, nc2, l1, l2, b1, b2, lin, t_inv, bloq, nunca, lb)

    # ------------------------------------------------------------------ 19 · contactos soldados
    def f_soldadura(self):
        self.voz("soldadura")
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 120, 20], x_length=6.4, y_length=3.0, tips=False,
                  axis_config={"color": TINTA2, "stroke_width": 2, "include_ticks": False}).move_to([-3.6, 1.4, 0])
        u = ax.plot(lambda t: 100 if t < 1 else (100 - 30 * np.exp(-(t - 1) * 0.0) if t < 2.2 else 100 - 30 * np.exp(-(t - 2.2) * 3)), x_range=[0, 4], color=CIAN_CORRIENTE, stroke_width=4, discontinuities=[1.0], use_smoothing=False)
        l85 = DashedLine(ax.c2p(0, 85), ax.c2p(4, 85), dash_length=0.1).set_stroke(VERDE_OK, 2)
        t85 = T("85 % Uc", 20, VERDE_OK, "BOLD").next_to(l85, RIGHT, buff=0.1)
        tu = T("tensión del mando al arrancar el motor", 22, TINTA, "BOLD").next_to(ax, UP, buff=0.1)
        self.play(Create(ax), FadeIn(tu), Create(l85), FadeIn(t85), run_time=0.5)
        self.play(Create(u), run_time=1.2)
        caida = pastilla("caída de tensión", ROJO_C, 22, True).move_to(ax.c2p(1.6, 30))
        self.play(FadeIn(caida), run_time=0.3)
        self.esperar_frac(0.1)
        # contactos que rebotan
        f1 = Rectangle(width=2.6, height=0.3, stroke_width=0).set_fill(CU, 1).move_to([3.4, 1.2, 0])
        m1 = Rectangle(width=2.6, height=0.3, stroke_width=0).set_fill(CU, 1).move_to([3.4, 2.0, 0])
        self.play(FadeIn(f1), FadeIn(m1), run_time=0.3)
        for k in range(3):
            self.play(m1.animate.move_to([3.4, 1.52, 0]), run_time=0.15)
            self.add(*[rayo([3.0 + 0.4 * k, 1.36, 0], [3.1 + 0.4 * k, 1.66, 0], color=AMBAR, semilla=k, amp=0.04)]) if False else None
            self.play(m1.animate.move_to([3.4, 1.75, 0]), run_time=0.12)
        self.sfx("pop", -10)
        sold = VGroup(m1.copy().move_to([3.4, 1.5, 0]), Rectangle(width=1.0, height=0.25, stroke_width=0).set_fill("#FFB066", 1).move_to([3.4, 1.37, 0]))
        glow = resplandor([3.4, 1.37, 0], 0.9, AMBAR, 8, 0.07)
        self.play(Transform(m1, sold[0]), FadeIn(sold[1]), FadeIn(glow), run_time=0.3)
        ls = pastilla("contactos SOLDADOS", ROJO_C, 26, True).move_to([3.4, 0.3, 0])
        self.play(FadeIn(ls), run_time=0.3)
        self.esperar_frac(0.3)
        rev = VGroup(pastilla("revisa sección y largo de cables", MARCA, 22, True), pastilla("revisa la tensión del mando", MARCA, 22, True)).arrange(DOWN, buff=0.2).move_to([-3.6, -1.6, 0])
        self.play(FadeIn(rev, shift=UP * 0.15), run_time=0.4)
        self.esperar_frac(0.3)
        # relé auxiliar KA1
        X, YT, YB = 2.4, -0.6, -3.9
        w = lambda a, b: Line(a, b).set_stroke(SIM, SW)
        c1 = sim_contacto(True, n1="", n2="").scale(0.8).move_to([X, -1.6, 0])
        ka = sim_bobina("KA1").scale(0.8).move_to([X, -3.0, 0])
        c2 = sim_contacto(True).scale(0.8).move_to([X + 2.6, -1.6, 0])
        lc2 = T("KA1", 18, SIM, "HEAVY").next_to(c2, LEFT, buff=0.1)
        lc1 = T("S1", 18, SIM, "HEAVY")
        km = sim_bobina("KM1").scale(0.8).move_to([X + 2.6, -3.0, 0])
        for m_, x_ in ((c1, X), (ka, X), (c2, X + 2.6), (km, X + 2.6)):
            alinear(m_, x_)
        lc2.next_to(c2, LEFT, buff=0.1)
        lc1.next_to(c1, LEFT, buff=0.1)
        lu = VGroup(T("Uc 24 V", 18, ROJO_C, "HEAVY").move_to([X, -0.4, 0]), T("Us red", 18, AMBAR, "HEAVY").move_to([X + 2.6, -0.4, 0]))
        lin = VGroup(w([X, -0.65, 0], c1[0].get_start()), w(c1[1].get_end(), ka[0].get_start()), w(ka[2].get_end(), [X, -3.8, 0]),
                     w([X + 2.6, -0.65, 0], c2[0].get_start()), w(c2[1].get_end(), km[0].get_start()), w(km[2].get_end(), [X + 2.6, -3.8, 0]))
        self.play(FadeOut(ls), FadeIn(VGroup(c1, lc1, ka, c2, lc2, km, lu, lin)), run_time=0.6)
        sol = pastilla("relé auxiliar KA1 → bobina KM1", VERDE_OK, 20, True).move_to([X + 1.3, -4.15, 0])
        self.play(FadeIn(sol), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(ax, u, l85, t85, tu, caida, f1, m1, sold[1], glow, rev, c1, lc1, ka, c2, lc2, km, lu, lin, sol)

    # ------------------------------------------------------------------ 20 · familia
    def f_familia(self):
        self.voz("familia")
        tams = [(0.55, "9 A"), (0.7, "18 A"), (0.9, "40 A"), (1.15, "95 A"), (1.45, "cientos de A")]
        fila = VGroup(*[VGroup(contactor_frente(s, ie=l.split()[0] if "cientos" not in l else "400"), T(l, 26, TINTA, "HEAVY")) for s, l in tams])
        for g in fila:
            g[1].next_to(g[0], DOWN, buff=0.2)
        fila.arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to([0, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in fila], lag_ratio=0.25), run_time=2.0)
        mismo = pastilla("mismo principio: electroimán + contactos", MARCA, 26, True).move_to([0, 3.4, 0])
        self.play(FadeIn(mismo), run_time=0.4)
        self.esperar_frac(0.5)
        dc = pastilla("calibres grandes: bobinas de CC o electrónicas → menos consumo", AMBAR, 22, True).move_to([0, -3.6, 0])
        self.play(FadeIn(dc), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(fila, mismo, dc)

    # ------------------------------------------------------------------ 21 · selección paso a paso
    def f_seleccion(self):
        self.voz("seleccion")
        pasos = ["tipo de carga → categoría", "tensión y corriente de la carga", "Ie (categoría) ≥ corriente", "tensión de la bobina = mando",
                 "contactos auxiliares", "coordinar protecciones"]
        bar = barra_pasos(pasos, x=-4.6, y0=3.0, dy=1.15, w=6.4)
        tit = T("CÓMO ELEGIR UN CONTACTOR", 34, TINTA, "HEAVY").move_to([3.4, 3.6, 0])
        self.play(FadeIn(tit), LaggedStart(*[FadeIn(f_, shift=RIGHT * 0.2) for f_ in bar], lag_ratio=0.1), run_time=1.0)
        ilus = [VGroup(horno(0.5), motor_3f(0.45)).arrange(RIGHT, buff=0.3), VGroup(motor_3f(0.6)), VGroup(T("Ie ≥ I", 60, AMBAR, "HEAVY")),
                VGroup(T("G7 · M7 · P7", 48, ROJO_C, "HEAVY")), VGroup(sim_contacto(True, n1="13", n2="14", largo=1.2), sim_contacto(False, n1="21", n2="22", largo=1.2)).arrange(RIGHT, buff=0.8),
                VGroup(T("Q1 + KM1 + F2", 48, MARCA, "HEAVY"))]
        cks = VGroup()
        prev = None
        for k, (f_, il) in enumerate(zip(bar, ilus)):
            il.move_to([3.4, 0.2, 0])
            self.play(*activar_paso(f_), FadeIn(il, scale=0.9), *( [FadeOut(prev)] if prev is not None else []), run_time=0.4)
            self.esperar_frac(1.0 / (len(bar) - k) * 0.85)
            anim, ck = completar_paso(f_)
            self.play(*anim, run_time=0.25)
            cks.add(ck)
            prev = il
        self.cerrar_voz()
        self.limpiar(bar, tit, prev, cks)

    # ------------------------------------------------------------------ 22 · ejemplo 1 (motor AC-3)
    def f_ejemplo1(self):
        self.voz("ejemplo1")
        tit = T("EJEMPLO 1 · MOTOR DE BOMBA", 34, TINTA, "HEAVY").move_to([0, 3.7, 0])
        mo = motor_3f(1.0).move_to([-4.6, 1.6, 0])
        placa = caja_info("datos", ["3~ · jaula de ardilla", "5 hp · 230 V · 60 Hz"], MARCA, 4.4, 24).move_to([-4.6, -0.8, 0])
        self.play(FadeIn(tit), FadeIn(mo), FadeIn(placa), run_time=0.6)
        self.esperar_frac(0.1)
        cat = pastilla("AC-3", AMBAR, 36, True).next_to(mo, RIGHT, buff=0.3)
        self.play(FadeIn(cat, scale=1.2), run_time=0.3)
        self.esperar_frac(0.1)
        flc = caja_info("NEC 2020 · Tabla 430.250", ["5 hp · 230 V → 15,2 A"], AMBAR, 4.4, 24).move_to([-4.6, -2.9, 0])
        self.play(FadeIn(flc, shift=UP * 0.2), run_time=0.4)
        self.esperar_frac(0.12)
        c12 = caja_info("contactor de 12 A", ["AC-3: 12 A · 3 hp a 230 V", "12 A < 15,2 A"], ROJO_C, 5.0, 24).move_to([2.0, 1.6, 0])
        x12 = equis(ROJO_C, 0.35).next_to(c12, RIGHT, buff=0.2)
        self.play(FadeIn(c12, shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(x12, scale=1.4), run_time=0.3)
        self.esperar_frac(0.2)
        c18 = caja_info("contactor de 18 A", ["AC-3: 18 A · 5 hp a 230/240 V", "18 A ≥ 15,2 A"], VERDE_OK, 5.0, 24).move_to([2.0, -0.6, 0])
        v18 = check(VERDE_OK, 0.35).next_to(c18, RIGHT, buff=0.2)
        self.play(FadeIn(c18, shift=LEFT * 0.2), run_time=0.4)
        self.sfx("ding", -12)
        self.play(FadeIn(v18, scale=1.4), run_time=0.3)
        self.esperar_frac(0.3)
        bob = pastilla("mando 120 V → bobina G7", ROJO_C, 26, True).move_to([2.0, -2.4, 0])
        self.play(FadeIn(bob), run_time=0.3)
        self.esperar_frac(0.4)
        res = VGroup(T("RESULTADO:", 26, TINTA2, "HEAVY"), T("LC1D18G7", 44, AMBAR, "HEAVY")).arrange(RIGHT, buff=0.3).move_to([2.0, -3.5, 0])
        src = fuente("Fichas LC1D12 / LC1D18 · Schneider Electric", [2.0, -4.15, 0], 16)
        self.play(FadeIn(res, scale=1.1), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, mo, placa, cat, flc, c12, x12, c18, v18, bob, res, src)

    # ------------------------------------------------------------------ 23 · ejemplo 2 (resistencias AC-1)
    def f_ejemplo2(self):
        self.voz("ejemplo2")
        tit = T("EJEMPLO 2 · HORNO DE RESISTENCIAS", 34, TINTA, "HEAVY").move_to([0, 3.7, 0])
        hn = horno(1.2).move_to([-4.6, 1.6, 0])
        gl = resplandor(hn.get_center(), 1.4, "#FF6B3D", 8, 0.04)
        datos = caja_info("datos", ["3~ · 12 kW · 240 V"], MARCA, 4.4, 24).move_to([-4.6, -0.6, 0])
        self.play(FadeIn(tit), FadeIn(hn), FadeIn(gl), FadeIn(datos), run_time=0.6)
        cat = pastilla("AC-1", VERDE_OK, 36, True).next_to(hn, RIGHT, buff=0.3)
        self.esperar_frac(0.05)
        self.play(FadeIn(cat, scale=1.2), run_time=0.3)
        f = VGroup(MathTex(r"I = \frac{P}{\sqrt{3}\,V}", color=TINTA).scale(1.1), MathTex(r"= \frac{12\,000}{1{,}73 \times 240}", color=TINTA).scale(1.0),
                   MathTex(r"= 28{,}9\ \text{A}", color=AMBAR).scale(1.2)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([2.2, 1.35, 0])
        self.esperar_frac(0.05)
        for p in f:
            self.play(Write(p), run_time=0.7)
            self.esperar_frac(0.05)
        c18 = caja_info("mismo contactor de 18 A", ["AC-1: 32 A", "32 A ≥ 28,9 A"], VERDE_OK, 5.0, 24).move_to([2.2, -1.45, 0])
        v = check(VERDE_OK, 0.35).next_to(c18, RIGHT, buff=0.2)
        self.play(FadeIn(c18, shift=LEFT * 0.2), run_time=0.4)
        self.sfx("ding", -12)
        self.play(FadeIn(v, scale=1.4), run_time=0.3)
        self.esperar_frac(0.2)
        mot = pastilla("si fuera un motor de 28,9 A (AC-3): contactor más grande", ROJO_C, 22, True).move_to([0, -2.7, 0])
        self.play(FadeIn(mot), run_time=0.3)
        self.esperar_frac(0.3)
        bob = pastilla("mando 220 V → bobina M7 → LC1D18M7", ROJO_C, 22, True).move_to([-4.2, -1.75, 0])
        self.play(FadeIn(bob), run_time=0.3)
        self.esperar_frac(0.3)
        cmp_ = VGroup(pastilla("motor (AC-3): 18 A", AMBAR, 28, True), pastilla("resistencias (AC-1): 32 A", VERDE_OK, 28, True)).arrange(RIGHT, buff=0.4).move_to([0, -3.6, 0])
        self.play(FadeOut(mot), FadeIn(cmp_, shift=UP * 0.15), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, hn, gl, datos, cat, f, c18, v, bob, cmp_)

    # ------------------------------------------------------------------ 24 · errores, seguridad, repaso, final
    def f_errores(self):
        self.voz("errores")
        il1 = VGroup(T("18 A", 60, AMBAR, "HEAVY"), T("¿AC-1 o AC-3?", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.1)
        il2 = VGroup(sim_bobina("KM1").scale(1.4), T("¿24 / 120 / 220 V?", 26, ROJO_C, "BOLD")).arrange(DOWN, buff=0.2)
        il3 = VGroup(contactor_frente(0.6), equis(ROJO_C, 0.3)).arrange(RIGHT, buff=0.2)
        self.tres_errores([("1", "Elegir solo\npor amperios", "revisa la categoría\nde empleo"),
                           ("2", "Bobina de\ntensión equivocada", "menor: se quema ·\nmayor: no cierra bien"),
                           ("3", "Creer que\nprotege al motor", "necesita protección\ncontra cortocircuito y sobrecarga")],
                          [il1, il2, il3])

    def f_repaso(self):
        self.voz("repaso")
        tit = T("EN RESUMEN", 46, TINTA, "HEAVY")
        reglas = ["Electroimán: pocos VA mueven la potencia del motor", "Se elige por categoría de empleo (AC-1, AC-3…)",
                  "Ie en esa categoría ≥ corriente de la carga", "Bobina = tensión del mando", "Siempre con protección contra cortocircuito y sobrecarga"]
        filas = VGroup(*[VGroup(check(VERDE_OK, 0.24), T(r, 28, TINTA, "BOLD")).arrange(RIGHT, buff=0.3) for r in reglas])
        filas.arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([0, -0.2, 0])
        tit.next_to(filas, UP, buff=0.55, aligned_edge=LEFT)
        self.play(FadeIn(tit), run_time=0.3)
        for f_ in filas:
            self.play(FadeIn(f_, shift=RIGHT * 0.2), run_time=0.4)
            self.esperar_frac(0.18)
        self.cerrar_voz()
        self.limpiar(tit, filas)

    def f_final(self):
        self.voz("cierre")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        lg = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(2.8).move_to([3.9, 1.6, 0])
        us = T("@miguelesquit", 36, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        yt = pastilla("SUSCRÍBETE", ROJO, 34, True)
        fb = pastilla("SÍGUEME", MARCA, 34, True)
        botones = VGroup(yt, fb).arrange(DOWN, buff=0.25).next_to(us, DOWN, buff=0.4)
        sig = T("Próximo: EL DISYUNTOR", 34, TINTA, "HEAVY").move_to([-3.6, 3.1, 0])
        cajas = VGroup(*[RoundedRectangle(width=5.6, height=3.15, corner_radius=0.2, stroke_color=METAL2, stroke_width=2).set_fill(CARTA, 1) for _ in range(2)]).arrange(DOWN, buff=0.45).move_to([-3.6, -0.6, 0])
        self.play(FadeIn(sig), FadeIn(cajas, shift=UP * 0.2), FadeIn(lg, scale=0.8), FadeIn(us), run_time=0.7)
        self.play(LaggedStart(FadeIn(yt, scale=1.2), FadeIn(fb, scale=1.2), lag_ratio=0.5), run_time=0.6)
        restante = self.fin_voz - self.renderer.time
        espera = max(self.FIN_SEG, restante + 1.0, min(20.0, self.DURACION_MIN - self.renderer.time))
        self.wait(espera)

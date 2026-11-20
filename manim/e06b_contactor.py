"""E06b · SELECCIONA EL CONTACTOR CORRECTO · ¿Cómo funciona el contactor? (rehecho con las correcciones del usuario).
Guion y fuentes: e06b_guion.py · piezas: piezas_auto2.py
Render: FORMATO=h VOZ=eleven manim -qh --disable_caching -o final_e06b e06b_contactor.py ContactorB
"""
from taller import *
from comun_e import _osc, _cla
from piezas_auto2 import *
from e06_contactor import motor_3f, horno, pulsador_fis
from dibujos_aves import check, equis
from e06b_guion import GUION, SECCIONES


def plc(s=1.0):
    caja = RoundedRectangle(width=2.2 * s, height=1.5 * s, corner_radius=0.08 * s, stroke_color="#4B5563", stroke_width=1.6).set_fill("#D9DDE2", 1)
    fr = Rectangle(width=2.0 * s, height=0.3 * s, stroke_width=0).set_fill("#1F2430", 1).move_to(caja.get_top() + DOWN * 0.25 * s)
    t = tx("PLC · 24 V CC", 0.14 * s, "#F2F4F7").move_to(fr)
    leds = VGroup(*[Circle(radius=0.05 * s, stroke_width=0).set_fill("#12B76A" if k in (0, 3) else "#667085", 1) for k in range(8)]).arrange(RIGHT, buff=0.12 * s)
    leds.move_to(caja.get_center() + UP * 0.05 * s)
    bor = VGroup(*[VGroup(RoundedRectangle(width=0.18 * s, height=0.18 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#4B5563", 1),
                          tornillo_ph(0.06 * s)) for _ in range(8)]).arrange(RIGHT, buff=0.06 * s).move_to(caja.get_bottom() + UP * 0.28 * s)
    return VGroup(caja, fr, t, leds, bor)


class ContactorB(TallerH):
    CARPETA_VOZ = "voz_e06b"
    GUION = GUION
    DURACION_MIN = 600.0

    def construct(self):
        self.cinta_act = None
        self.paso_act = None
        orden = ["gancho", "que_es", "partes", "funciona", "criticos", "seleccion", "ejemplo1", "ejemplo2"]
        solo = os.environ.get("SOLO")
        for paso in orden:
            if solo and paso not in solo.split(","):
                continue
            getattr(self, "f_" + paso)()
        if not solo:
            self.f_final()

    # ================================================================ utilidades didácticas
    def portadilla(self, clave):
        num, titulo = getattr(self, "SECC", SECCIONES)[clave]
        sale = [m for m in (self.cinta_act, self.paso_act) if m is not None]
        fondo = Rectangle(width=16.2, height=9.2, stroke_width=0).set_fill("#06102A" if TEMA != "negro" else "#050608", 0.97).set_z_index(40)
        grande = T(f"0{num}", 300, MARCA, "HEAVY").set_opacity(0.14).move_to([4.6, -0.2, 0]).set_z_index(41)
        sec = T(f"SECCIÓN {num}", 30, AMBAR, "HEAVY")
        tit = T(titulo, 70, TXT, "HEAVY")
        if tit.width > 13.0:
            tit.scale_to_fit_width(13.0)
        VGroup(sec, tit).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 0.2, 0])
        barra = RoundedRectangle(width=tit.width, height=0.14, corner_radius=0.07, stroke_width=0).set_fill(MARCA, 1).next_to(tit, DOWN, buff=0.3, aligned_edge=LEFT)
        cursor = Rectangle(width=0.07, height=tit.height * 0.95, stroke_width=0).set_fill(MARCA, 1)
        for m_ in (sec, tit, barra, cursor):
            m_.set_z_index(42)
        self.play(FadeIn(fondo), FadeIn(grande, scale=1.1), FadeIn(sec, shift=RIGHT * 0.2), *[FadeOut(m) for m in sale], run_time=0.45)
        self.cinta_act = None
        self.paso_act = None
        n = len(tit.submobjects)
        dt = 0.05
        wav = DIR / "sfx" / f"tecleo_{n}.wav"
        if not wav.exists():
            sonido_tecleo(wav, n, dt, semilla=n)
        self.add_sound(str(wav), gain=-9)
        cursor.next_to(tit[0], LEFT, buff=0.05)
        self.add(cursor)
        letras = [m for m in tit.submobjects]
        for m in letras:
            m.set_opacity(0)
        self.add(tit)

        def revelar(mob, alpha):
            k = int(alpha * n + 1e-6)
            for i, m in enumerate(letras):
                m.set_opacity(1 if i < k else 0)
            ultimo = letras[max(0, min(k, n) - 1)]
            cursor.move_to([ultimo.get_right()[0] + 0.08, tit.get_center()[1], 0]) if k > 0 else None
        self.play(UpdateFromAlphaFunc(tit, revelar), run_time=n * dt, rate_func=linear)
        cursor.clear_updaters()
        self.play(GrowFromEdge(barra, LEFT), run_time=0.35)
        self.play(cursor.animate.set_opacity(0), run_time=0.15)
        self.play(cursor.animate.set_opacity(1), run_time=0.15)
        self.wait(0.35)
        ci = cinta(num, titulo)
        self.play(FadeOut(VGroup(fondo, grande, sec, tit, barra, cursor)), FadeIn(ci, shift=RIGHT * 0.3), run_time=0.45)
        self.cinta_act = ci

    def pasar_paso(self, n):
        nuevo = insignia_paso(n, getattr(self, "N_CRIT", 7))
        self.sfx("tic", -10)
        if self.paso_act is None:
            self.play(FadeIn(nuevo, scale=0.8), run_time=0.35)
        else:
            viejo = self.paso_act
            self.play(FadeOut(viejo, scale=0.9), FadeIn(nuevo, scale=1.1), run_time=0.35)
        self.paso_act = nuevo

    def subtitulo(self, texto, color=AMBAR):
        t = T(texto, 34, TXT, "HEAVY")
        if t.width > 9.0:
            t.scale_to_fit_width(9.0)
        lin = RoundedRectangle(width=t.width + 0.2, height=0.08, corner_radius=0.04, stroke_width=0).set_fill(color, 1).next_to(t, DOWN, buff=0.12)
        g = VGroup(t, lin)
        lin.align_to(t, LEFT)
        return g.move_to([-7.55 + g.width / 2, 3.05, 0])

    # ================================================================ GANCHO
    def f_gancho(self):
        self.voz("gancho")
        ct = contactor_2d(0.95).move_to([0, 0.55, 0])
        mo = motor_3f(1.0).move_to([-5.2, 0.4, 0])
        hn = horno(1.05).move_to([5.3, 0.4, 0])
        gl = resplandor(hn[2].get_center(), 1.2, "#FF6B3D", 8, 0.04)
        self.play(FadeIn(ct, shift=UP * 0.2), run_time=0.6)
        self.esperar_frac(0.06)
        f1 = flecha_a(ct.get_left() + LEFT * 0.1, mo.get_right() + RIGHT * 0.15, AMBAR, 6)
        e1 = etiqueta("motor (AC-3): 18 A", AMBAR, 30).next_to(mo, DOWN, buff=0.45)
        self.play(FadeIn(mo, shift=RIGHT * 0.2), GrowArrow(f1), run_time=0.5)
        self.sfx("pop", -14)
        self.play(FadeIn(e1, scale=1.1), run_time=0.3)
        self.esperar_frac(0.15)
        f2 = flecha_a(ct.get_right() + RIGHT * 0.35, hn.get_left() + LEFT * 0.15, VERDE_OK, 6)
        e2 = etiqueta("horno (AC-1): 32 A", VERDE_OK, 30).next_to(hn, DOWN, buff=0.45)
        self.play(FadeIn(hn, shift=LEFT * 0.2), FadeIn(gl), GrowArrow(f2), run_time=0.5)
        self.sfx("pop", -14)
        self.play(FadeIn(e2, scale=1.1), run_time=0.3)
        self.esperar_frac(0.1)
        preg = T("¿EL MISMO APARATO?", 54, TXT, "HEAVY").move_to([0, -3.3, 0])
        self.play(Write(preg), run_time=0.7)
        self.esperar_frac(0.25)
        # título del video
        self.limpiar(ct, mo, hn, gl, f1, f2, e1, e2, preg, t=0.4)
        t1 = T("SELECCIONA EL", 58, TXT, "HEAVY")
        t2 = T("CONTACTOR CORRECTO", 78, MARCA, "HEAVY")
        t3 = T("¿Cómo funciona el contactor?", 34, TXT2, "BOLD")
        tit = VGroup(t1, t2, t3).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        if tit.width > 10.0:
            tit.scale_to_fit_width(10.0)
        tit.move_to([-7.3 + tit.width / 2, 1.5, 0])

        def bloque_num(n, l1, l2, col):
            cu = RoundedRectangle(width=1.25, height=1.25, corner_radius=0.07, stroke_width=0).set_fill(col, 1)
            nn = T(n, 72, "#0B1C3D", "HEAVY").move_to(cu)
            tx_ = VGroup(T(l1, 30, "#0B1C3D", "HEAVY"), T(l2, 24, "#344054", "BOLD")).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            fondo = RoundedRectangle(width=tx_.width + 1.25 + 0.75, height=1.25, corner_radius=0.07, stroke_width=0).set_fill(WHITE, 1)
            fondo.align_to(cu, LEFT).align_to(cu, UP)
            tx_.next_to(cu, RIGHT, buff=0.3)
            return VGroup(fondo, cu, nn, tx_)
        tags = VGroup(bloque_num("7", "CRITERIOS", "de selección", AMBAR), bloque_num("2", "EJEMPLOS", "con datos reales", VERDE_OK)).arrange(RIGHT, buff=0.4)
        tags.next_to(tit, DOWN, buff=0.55, aligned_edge=LEFT)
        ctm = contactor_2d(0.75).move_to([5.75, -0.6, 0])
        self.sfx("whoosh", -12)
        self.play(FadeIn(t1, shift=UP * 0.2), FadeIn(t2, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(t3), FadeIn(ctm, shift=LEFT * 0.2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.2) for t_ in tags], lag_ratio=0.4), run_time=0.7)
        self.cerrar_voz(0.2)
        self.limpiar(tit, ctm, tags)

    # ================================================================ 1 · QUÉ ES
    def f_que_es(self):
        self.portadilla("q_problema")
        # --- el problema: interruptor de cuchilla
        self.voz("q_problema")
        k = interruptor_cuchilla(1.55).move_to([-3.4, 0.3, 0])
        y_b = k.base.get_bottom()[1]
        c1 = cable([[k.poste.get_center()[0], y_b + 0.05, 0], [k.poste.get_center()[0], y_b - 1.6, 0]], C_POT, w=16, puntera=False)
        c2 = cable([[k.mordaza.get_center()[0], y_b + 0.05, 0], [k.mordaza.get_center()[0], y_b - 1.6, 0]], C_POT, w=16, puntera=False)
        lp = T("cables de potencia", 24, TXT2, "BOLD").move_to([-3.4, y_b - 1.95, 0])
        self.add(c1, c2)
        self.bring_to_front(k)
        self.play(FadeIn(k), Create(c1), Create(c2), FadeIn(lp), run_time=0.7)
        estado = etiqueta("CERRADO", VERDE_OK, 24).next_to(k, UP, buff=0.9)
        self.play(FadeIn(estado), run_time=0.3)
        self.esperar_frac(0.18)
        punta_m = k.mordaza.get_top()
        self.sfx("pop", -8)
        self.play(Rotate(k.cuchilla, 0.75, about_point=k.pin.get_center()), Transform(estado, etiqueta("ABIERTO", ROJO_P, 24).move_to(estado)), run_time=0.6)
        arco = VGroup(*[rayo(punta_m + UP * 0.05, k.cuchilla[0].get_corner(DR) + LEFT * 0.4, color=c_, semilla=j, amp=0.12, w=w_)
                        for j, (c_, w_) in enumerate(((AMBAR, 7), (WHITE, 2.5)))])
        glow = resplandor((punta_m + k.cuchilla[0].get_corner(DR)) / 2, 0.9, AMBAR, 8, 0.07)
        self.play(FadeIn(arco), FadeIn(glow), run_time=0.25)
        pts = VGroup(carta("1 · Arco en cada apertura", (), AMBAR, 6.4, 26), carta("2 · El operador junto a la potencia", (), ROJO_P, 6.4, 26),
                     carta("3 · Sin mando a distancia", (), ROJO_P, 6.4, 26)).arrange(DOWN, buff=0.3).move_to([3.9, 0.4, 0])
        self.play(FadeIn(pts[0], shift=LEFT * 0.2), run_time=0.35)
        self.esperar_frac(0.3)
        self.play(FadeIn(pts[1], shift=LEFT * 0.2), FadeOut(arco), FadeOut(glow), run_time=0.35)
        self.esperar_frac(0.45)
        self.play(FadeIn(pts[2], shift=LEFT * 0.2), run_time=0.35)
        self.cerrar_voz()
        self.limpiar(k, c1, c2, lp, estado, pts)
        # --- definición
        self.voz("q_definicion")
        frases = [("Aparato mecánico de conexión", TXT), ("con una sola posición de reposo,", AMBAR), ("que no se acciona a mano,", AMBAR),
                  ("capaz de establecer, soportar e interrumpir corrientes", TXT), ("en condiciones normales,", TXT), ("incluidas las sobrecargas de servicio.", TXT)]
        lin = VGroup(*[T(f, 32, c, "BOLD") for f, c in frases]).arrange(DOWN, buff=0.17)
        caja = RoundedRectangle(width=lin.width + 1.4, height=lin.height + 1.2, corner_radius=0.25, stroke_color=MARCA, stroke_width=3).set_fill(AZUL_CARTA, 1)
        comi = T("“", 150, MARCA, "HEAVY").move_to(caja.get_corner(UL) + RIGHT * 0.45 + DOWN * 0.5)
        g = VGroup(caja, comi, lin.move_to(caja)).move_to([0, 0.75, 0])
        src = fuente("IEC 60050 · IEV 441-14-33 (definición de contactor)", [0, -4.1, 0], 22)
        self.play(FadeIn(caja), FadeIn(comi), FadeIn(src), run_time=0.4)
        for i, l in enumerate(lin):
            self.play(FadeIn(l, shift=RIGHT * 0.15), run_time=0.45)
            self.esperar_frac(0.11)
        sim = contacto(True, contactor=True, largo=1.3, n1="1", n2="2").move_to([-2.2, -2.75, 0])
        rep = etiqueta("en reposo: contactos principales ABIERTOS", VERDE_OK, 26).next_to(sim, RIGHT, buff=0.5)
        self.play(g.animate.shift(UP * 0.3), FadeIn(sim), FadeIn(rep, shift=LEFT * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(g, src, sim, rep)
        # --- dos circuitos
        self.voz("q_mundos")
        sep = DashedLine([0, 3.3, 0], [0, -3.8, 0], dash_length=0.12).set_stroke(TXT2, 2)
        hm = carta("CIRCUITO DE MANDO", ["poca corriente · pulsadores"], ROJO_P, 6.4, 24).move_to([-4.0, 2.55, 0])
        hp = carta("CIRCUITO DE POTENCIA", ["corriente de la carga · motor"], AMBAR, 6.4, 24).move_to([4.0, 2.55, 0])
        pb = pulsador_fis(VERDE_P, "I", 1.0).move_to([-5.6, -0.6, 0])
        ct = contactor_2d(0.72).move_to([0, -0.9, 0])
        hilo = cable([ct.b["A1"].tor.get_center(), ct.b["A1"].tor.get_center() + RIGHT * 0.0 + UP * 0.0 + LEFT * 0.01, [-2.0, ct.b["A1"].get_center()[1], 0],
                      [-2.0, -0.6, 0], pb.get_right() + RIGHT * 0.05], C_MANDO, w=6, puntera=False)
        mo = motor_3f(0.95).move_to([5.0, -1.3, 0])
        gru = cable([ct.b["4/T2"].entrada.get_center(), ct.b["4/T2"].entrada.get_center() + DOWN * 0.55, [3.2, ct.b["4/T2"].entrada.get_center()[1] - 0.55, 0],
                     [3.2, mo.caja_b.get_center()[1] + 0.9, 0], [mo.caja_b.get_center()[0], mo.caja_b.get_center()[1] + 0.9, 0], mo.caja_b.get_top()], C_POT, w=18, puntera=False)
        self.play(Create(sep), FadeIn(hm, shift=DOWN * 0.2), FadeIn(hp, shift=DOWN * 0.2), run_time=0.6)
        self.esperar_frac(0.05)
        self.add(hilo)
        self.play(FadeIn(pb), Create(hilo), run_time=0.6)
        self.esperar_frac(0.2)
        self.add(gru)
        self.play(FadeIn(mo), Create(gru), run_time=0.6)
        self.bring_to_front(ct)
        self.play(FadeIn(ct, scale=0.9), run_time=0.4)
        lv = VGroup(etiqueta("pocos vatios", ROJO_P, 26).next_to(pb, DOWN, buff=0.5), etiqueta("kilovatios", AMBAR, 26).next_to(mo, DOWN, buff=0.4))
        self.esperar_frac(0.35)
        self.play(FadeIn(lv[0], scale=1.1), run_time=0.3)
        self.play(FadeIn(lv[1], scale=1.1), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(sep, hm, hp, pb, ct, hilo, mo, gru, lv)

    # ================================================================ 2 · PARTES
    def despiece(self):
        piezas = [("cam", camara_apaga(3.6, 1.2)), ("fij", VGroup(contacto_fijo(-1), contacto_fijo(1))), ("pue", puente_movil(2.4)), ("por", portacontactos(1.0)),
                  ("arm", armadura_T(3.2, 0.55)), ("res", resorte(0.8, 0.6, 7, "#C7CCD6", 3)), ("bob", bobina(1.8, 1.0)), ("nuc", nucleo_E(3.2, 1.3)), ("bas", base_contactor(3.8, 0.7))]
        g = VGroup(*[p for _, p in piezas]).arrange(DOWN, buff=0.16).scale_to_fit_height(6.9).move_to([-5.75, -0.55, 0])
        return dict(piezas), g

    def resaltar(self, d, g, claves):
        sel = VGroup(*[d[k] for k in claves])
        otros = [p for k, p in d.items() if k not in claves]
        caja = SurroundingRectangle(sel, color=AMBAR, buff=0.08, corner_radius=0.1, stroke_width=3.5)
        return caja, [*[p.animate.set_opacity(0.3) for p in otros], *[d[k].animate.set_opacity(1) for k in claves]]

    def f_partes(self):
        self.portadilla("p_intro")
        self.voz("p_intro")
        d, g = self.despiece()
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in g], lag_ratio=0.12), run_time=1.6)
        nombres = [("cam", "cámara apagachispas"), ("pue", "contactos (polos)"), ("arm", "armadura móvil"), ("res", "resorte"), ("bob", "bobina"), ("nuc", "núcleo fijo")]
        marcas = VGroup()
        for kk, nom in nombres:
            p = d[kk]
            e = T(nom, 24, TXT, "BOLD").move_to([0.0, p.get_center()[1], 0]).align_to([-3.2, 0, 0], LEFT)
            fl = Arrow(e.get_left() + LEFT * 0.08, p.get_right() + RIGHT * 0.05, buff=0.02, color=AMBAR, stroke_width=3.5, max_tip_length_to_length_ratio=0.25, tip_length=0.16)
            marcas.add(VGroup(fl, e))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(m[0]), FadeIn(m[1], shift=LEFT * 0.1)) for m in marcas], lag_ratio=0.25), run_time=min(3.5, max(1.0, self.resta() - 0.5)))
        self.cerrar_voz()
        self.play(FadeOut(marcas), run_time=0.3)
        zona = [1.3, -0.3, 0]       # centro de la zona de zoom

        # --- bobina
        self.voz("p_bobina")
        caja, an = self.resaltar(d, g, ["bob"])
        self.play(Create(caja), *an, run_time=0.5)
        bz = bobina(3.4, 2.0).move_to([-0.6, 0.1, 0])
        la1 = cable([bz.get_corner(UR) + LEFT * 0.35 + DOWN * 0.05, bz.get_corner(UR) + LEFT * 0.35 + UP * 0.9, [1.9, bz.get_top()[1] + 0.9, 0]], C_MANDO, w=8, puntera=False)
        la2 = cable([bz.get_corner(DR) + LEFT * 0.35 + UP * 0.05, bz.get_corner(DR) + LEFT * 0.35 + DOWN * 0.9, [1.9, bz.get_bottom()[1] - 0.9, 0]], C_NEUTRO, w=8, puntera=False)
        ta = VGroup(etiqueta("A1", ROJO_P, 28).next_to(la1.ruta.get_end(), RIGHT, buff=0.15), etiqueta("A2", "#667085", 28).next_to(la2.ruta.get_end(), RIGHT, buff=0.15))
        zl = VGroup()
        self.play(FadeIn(bz, scale=0.7), FadeIn(zl), run_time=0.6)
        self.play(Create(la1), Create(la2), FadeIn(ta), run_time=0.6)
        self.esperar_frac(0.12)
        self.play(bz[0].animate.set_fill("#F0A15E"), run_time=0.4)
        self.esperar_frac(0.25)
        sim = bobina_sim("KM1").scale(1.9).move_to([5.5, 1.3, 0])
        cs = carta("SÍMBOLO DE LA BOBINA", ["bornes A1 – A2", "identificación: KM1"], ROJO_P, 4.4, 22).move_to([5.4, -1.9, 0])
        self.play(FadeIn(sim, scale=0.8), run_time=0.5)
        self.play(FadeIn(cs, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(bz, la1, la2, ta, zl, sim, cs, caja)

        # --- núcleo y armadura (electroimán)
        self.voz("p_nucleo")
        caja, an = self.resaltar(d, g, ["arm", "bob", "nuc"])
        self.play(Create(caja), *an, run_time=0.5)
        nz = nucleo_E(4.2, 1.9).move_to([0.3, -1.3, 0])
        bz = bobina(2.3, 1.2).move_to(nz.get_center() + UP * 0.25)
        az = armadura_T(4.2, 0.7).move_to(nz.get_top() + UP * 0.75)
        zl = VGroup()
        self.play(FadeIn(nz), FadeIn(bz), FadeIn(az), FadeIn(zl), run_time=0.6)
        ce = carta("ELECTROIMÁN", ["bobina + núcleo fijo", "+ armadura móvil"], MARCA, 4.4, 22).move_to([5.3, 2.1, 0])
        self.play(FadeIn(ce, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.15)
        lam = VGroup(*[Line(az.get_left() + RIGHT * 0.05 + UP * y, az.get_right() + LEFT * 0.05 + UP * y).set_stroke("#334155", 1.4) for y in np.linspace(-0.3, 0.3, 7)])
        c1 = llamada("chapas de acero al silicio", az.get_right() + LEFT * 0.4, [5.0, 0.55, 0], AMBAR, 22, -0.4)
        self.play(Create(lam), FadeIn(c1), run_time=0.5)
        cf = etiqueta("menos corrientes de Foucault y calor", AMBAR, 20).next_to(c1[1], DOWN, buff=0.15)
        self.play(FadeIn(cf), run_time=0.3)
        self.esperar_frac(0.35)
        an_ = nz.anillos
        brillo = VGroup(*[Circle(radius=0.2).set_stroke(CU, 4).move_to(a) for a in an_])
        c2 = llamada("espiras de sombra (cobre)", an_[1].get_center(), [5.0, -1.4, 0], CU, 22, 0.4)
        self.play(Create(brillo), FadeIn(c2), Indicate(an_, color=AMBAR, scale_factor=1.6), run_time=0.7)
        cv = etiqueta("la fuerza no cae a cero: no vibra", CU, 20).next_to(c2[1], DOWN, buff=0.15)
        self.play(FadeIn(cv), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(nz, bz, az, zl, ce, lam, c1, cf, brillo, c2, cv, caja)

        # --- resorte
        self.voz("p_resorte")
        caja, an = self.resaltar(d, g, ["res"])
        self.play(Create(caja), *an, run_time=0.4)
        base_ = Rectangle(width=3.0, height=0.5, stroke_color="#5B6573", stroke_width=1.4).set_fill("#9AA3AF", 1).move_to([0.3, -2.2, 0])
        rz = resorte(1.6, 0.9, 7, "#D0D5DD", 5).move_to([0.3, -1.15, 0])
        arz = armadura_T(3.0, 0.5).move_to([0.3, -0.1, 0])
        self.play(FadeIn(base_), FadeIn(rz), FadeIn(arz), run_time=0.4)
        self.play(arz.animate.shift(DOWN * 0.7), rz.animate.stretch_to_fit_height(0.9).shift(DOWN * 0.35), run_time=0.5)
        self.play(arz.animate.shift(UP * 0.7), rz.animate.stretch_to_fit_height(1.6).shift(UP * 0.35), run_time=0.5)
        cr = carta("RESORTE DE RETORNO", ["sin tensión → posición de reposo", "contactos principales abiertos"], VERDE_OK, 5.6, 22).move_to([5.0, 0.6, 0])
        self.play(FadeIn(cr, shift=LEFT * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(base_, rz, arz, cr, caja)

        # --- polos
        self.voz("p_polos")
        caja, an = self.resaltar(d, g, ["pue", "fij", "por"])
        self.play(Create(caja), *an, run_time=0.4)
        ct = contactor_2d(1.0).move_to([0.0, -0.45, 0])
        self.play(FadeIn(ct, scale=0.9), run_time=0.5)
        self.esperar_frac(0.12)
        r1 = SurroundingRectangle(ct.pot_sup, color=AMBAR, buff=0.06, corner_radius=0.1, stroke_width=4)
        r2 = SurroundingRectangle(ct.pot_inf, color=VERDE_OK, buff=0.06, corner_radius=0.1, stroke_width=4)
        k1 = carta("1·3·5 → ALIMENTACIÓN", ["impares, arriba (L1 L2 L3)"], AMBAR, 4.6, 20).move_to([5.1, 2.1, 0])
        k2 = carta("2·4·6 → CARGA", ["pares, abajo (T1 T2 T3)"], VERDE_OK, 4.6, 20).move_to([5.1, 0.35, 0])
        self.play(Create(r1), FadeIn(k1, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.18)
        self.play(Create(r2), FadeIn(k2, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.25)
        sims = VGroup(*[contacto(True, contactor=True, largo=1.25, n1=a, n2=b, sw=SW_POT) for a, b in (("1", "2"), ("3", "4"), ("5", "6"))]).arrange(RIGHT, buff=0.7).move_to([5.3, -2.15, 0])
        dl = DashedLine(sims[0].cuchilla.get_center(), sims[2].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2)
        lk = T("KM1", 26, SIM, "HEAVY").next_to(sims, LEFT, buff=0.3)
        self.play(FadeOut(k2), FadeIn(sims), Create(dl), FadeIn(lk), run_time=0.5)
        semis = VGroup(*[Circle(radius=0.17).set_stroke(AMBAR, 4).move_to(s_[4].get_center()) for s_ in sims])
        ls = etiqueta("semicírculo = función contactor", AMBAR, 22).next_to(sims, DOWN, buff=0.25)
        self.play(Create(semis), FadeIn(ls), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(r1, r2, k1, sims, dl, lk, semis, ls, caja)

        # --- auxiliares
        self.voz("p_aux")
        self.play(ct.animate.scale(0.9).move_to([-1.9, -0.45, 0]), *[p.animate.set_opacity(0.3) for p in g], run_time=0.4)
        ra = SurroundingRectangle(ct.aux_blq, color=MARCA, buff=0.06, corner_radius=0.06, stroke_width=4)
        la = etiqueta("13-14 integrado", MARCA, 20).next_to(ra, UP, buff=0.12)
        blq_a = bloque_aux_frontal(ct.ventana.width / 1.65, (("21", "NC"), ("33", "NO"))).move_to(ct.ventana)
        lb_a = etiqueta("bloque frontal: 21-22 · 33-34", MARCA, 20).next_to(ct, DOWN, buff=0.15)
        self.play(Create(ra), FadeIn(la), run_time=0.4)
        self.play(FadeIn(blq_a, shift=DOWN * 0.3), FadeIn(lb_a), run_time=0.5)
        self.esperar_frac(0.08)
        regla = VGroup(T("1  3", 66, AMBAR, "HEAVY"), T("2  1", 66, AMBAR, "HEAVY"))
        for r_ in regla:
            r_[1].set_color(MARCA)
        regla.arrange(DOWN, buff=0.15).move_to([4.6, 1.2, 0])
        dec = VGroup(T("decena:", 22, AMBAR, "BOLD"), T("número de orden", 22, TXT, "BOLD")).arrange(DOWN, buff=0.05).next_to(regla, LEFT, buff=0.5)
        uni = VGroup(T("unidad:", 22, MARCA, "BOLD"), T("función", 22, TXT, "BOLD")).arrange(DOWN, buff=0.05).next_to(regla, RIGHT, buff=0.5)
        self.play(FadeIn(regla), FadeIn(dec), FadeIn(uni), run_time=0.5)
        self.esperar_frac(0.15)
        fun = VGroup(carta("1 – 2 = NC", ["normalmente cerrado"], ROJO_P, 3.2, 20), carta("3 – 4 = NA", ["normalmente abierto"], VERDE_OK, 3.2, 20)).arrange(RIGHT, buff=0.25).move_to([4.5, -1.1, 0])
        self.play(FadeIn(fun, shift=UP * 0.2), run_time=0.4)
        self.esperar_frac(0.2)
        sa = VGroup(contacto(True, largo=1.3, n1="13", n2="14"), contacto(False, largo=1.3, n1="21", n2="22")).arrange(RIGHT, buff=1.2).move_to([4.5, -1.3, 0])
        lka = T("KM1", 24, SIM, "HEAVY").next_to(sa, LEFT, buff=0.3)
        sinsemi = etiqueta("sin semicírculo", MARCA, 20).next_to(sa, DOWN, buff=0.25)
        self.play(FadeOut(fun), FadeIn(sa), FadeIn(lka), FadeIn(sinsemi), run_time=0.5)
        self.esperar_frac(0.4)
        cmp_ = VGroup(carta("PRINCIPALES · potencia", ["corriente de la carga"], AMBAR, 4.2, 20), carta("AUXILIARES · mando", ["pocos amperios: ¡nunca la carga!"], MARCA, 4.2, 20)).arrange(DOWN, buff=0.2)
        cmp_.move_to([4.5, -1.35, 0])
        self.play(FadeOut(VGroup(sa, lka, sinsemi)), FadeIn(cmp_, shift=UP * 0.2), run_time=0.45)
        self.cerrar_voz()
        self.limpiar(ct, ra, la, blq_a, lb_a, regla, dec, uni, cmp_)

        # --- cámara apagachispas
        self.voz("p_camara")
        caja, an = self.resaltar(d, g, ["cam"])
        self.play(Create(caja), *an, run_time=0.4)
        cam = RoundedRectangle(width=4.6, height=3.4, corner_radius=0.14, stroke_color="#8B93A0", stroke_width=2).set_fill("#2A2F3A", 0.8).move_to([0.6, -0.4, 0])
        plq = VGroup(*[Rectangle(width=3.2, height=0.1, stroke_width=0).set_fill("#A7AFBA", 1).move_to([0.6, -0.4 + 0.32 * (j - 3), 0]) for j in range(7)])
        self.play(FadeIn(cam), LaggedStart(*[FadeIn(p) for p in plq], lag_ratio=0.08), run_time=0.6)
        largo = rayo([-1.2, -2.0, 0], [-1.2, 1.2, 0], color=AMBAR, amp=0.15, w=7)
        self.sfx("pop", -10)
        self.play(FadeIn(largo), run_time=0.3)
        arcs = VGroup(*[rayo([-0.6, plq[j].get_center()[1] + 0.06, 0], [-0.6, plq[j + 1].get_center()[1] - 0.06, 0], color=AMBAR, semilla=j, amp=0.05, w=5) for j in range(6)])
        self.play(ReplacementTransform(largo, arcs), run_time=0.7)
        cc = carta("CÁMARA APAGACHISPAS", ["alarga, divide y enfría el arco", "se apaga al pasar la corriente por cero"], MARCA, 4.8, 19).move_to([5.2, 1.3, 0])
        self.play(FadeIn(cc, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.5)
        self.play(FadeOut(arcs), run_time=0.3)
        src = fuente("Telesquemario Telemecanique, págs. 24–29 · Símbolos: IEC 60617", [0, -4.1, 0], 20)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz()
        self.limpiar(cam, plq, cc, caja, g, src)

    # ================================================================ 3 · CÓMO FUNCIONA
    def mover_corte(self, ct, cerrar=True, rt=0.35):
        dd = -ct.gap if cerrar else ct.gap
        anims = [ct.movil.animate.shift(UP * dd)]
        for r_ in ct.resortes:
            anims.append(r_.animate.stretch_to_fit_height(max(0.05, r_.height + dd)).shift(UP * dd / 2))
        self.play(*anims, run_time=rt)

    def f_funciona(self):
        self.portadilla("f_corte")
        self.voz("f_corte")
        ct = corte_contactor([-2.6, 0.2, 0], 0.95)
        self.play(FadeIn(ct), run_time=0.5)
        t1 = ct.fijos[0][2].cabeza.get_top()
        t2 = ct.fijos[1][2].cabeza.get_top()
        lin = cable([t1, t1 + UP * 1.55], C_POT, w=12, etiqueta="L1")
        lout = cable([t2, t2 + UP * 1.55], C_POT, w=12, etiqueta="T1")
        p_a1 = ct.bob.get_left() + RIGHT * 0.05 + UP * 0.25
        p_a2 = ct.bob.get_left() + RIGHT * 0.05 + DOWN * 0.25
        a1 = cable([p_a1, p_a1 + LEFT * 1.0, [-7.0, p_a1[1], 0]], C_MANDO, w=6, puntera=False)
        a2 = cable([p_a2, p_a2 + LEFT * 1.0, [-7.0, p_a2[1], 0]], C_NEUTRO, w=6, puntera=False)
        la = VGroup(T("A1", 22, ROJO_P, "HEAVY").next_to(a1.ruta.get_end(), UP, buff=0.06).shift(RIGHT * 0.3),
                    T("A2", 22, TXT, "HEAVY").next_to(a2.ruta.get_end(), DOWN, buff=0.06).shift(RIGHT * 0.3))
        self.add(lin, lout)
        self.play(Create(lin), Create(lout), Create(a1), Create(a2), FadeIn(la), run_time=0.6)
        pasos = VGroup(*[carta(t_, (), c_, 5.4, 20) for t_, c_ in (("1 · Reposo: contactos abiertos", TXT2), ("2 · Tensión en A1–A2", ROJO_P),
                                                                   ("3 · El núcleo atrae la armadura", AMBAR), ("4 · Contactos cerrados: doble corte", VERDE_OK),
                                                                   ("5 · Sin tensión: el resorte la regresa", MARCA))]).arrange(DOWN, buff=0.18).move_to([4.55, -0.35, 0])
        self.play(FadeIn(pasos[0], shift=LEFT * 0.15), run_time=0.3)
        self.esperar_frac(0.12)
        self.play(FadeIn(pasos[1], shift=LEFT * 0.15), run_time=0.3)
        ca = corriente([a1.ruta.get_end(), p_a1 + LEFT * 1.0, p_a1], vel=1.0, escala=1.0, color=ROJO_P)
        self.add(ca)
        flujo = VGroup(*[DashedVMobject(RoundedRectangle(width=1.5, height=1.6, corner_radius=0.3), num_dashes=24).set_stroke(VIOLETA if 'VIOLETA' in globals() else "#9E77ED", 3)
                         .move_to([ct.nuc.get_center()[0] + s_ * 0.85, ct.nuc.get_center()[1] + 0.4, 0]) for s_ in (-1, 1)])
        self.play(ct.bob[0].animate.set_fill("#F0A15E"), Create(flujo), run_time=0.6)
        self.esperar_frac(0.1)
        self.play(FadeIn(pasos[2], shift=LEFT * 0.15), run_time=0.3)
        self.sfx("tic", -6)
        self.mover_corte(ct, True, 0.3)
        self.play(FadeIn(pasos[3], shift=LEFT * 0.15), run_time=0.3)
        cp = corriente([lin.ruta.get_end(), t1, ct.fijos[0][1].get_center(), ct.pu.get_center() + LEFT * 1.25, ct.pu.get_center() + RIGHT * 1.25,
                        ct.fijos[1][1].get_center(), t2, lout.ruta.get_end()], vel=1.4, escala=1.3)
        self.add(cp)
        dc = VGroup(*[Circle(radius=0.28).set_stroke(VERDE_OK, 4).move_to(ct.fijos[i][1].get_center() + UP * 0.05) for i in (0, 1)])
        self.play(Create(dc), run_time=0.4)
        self.esperar_frac(0.4)
        self.play(FadeIn(pasos[4], shift=LEFT * 0.15), run_time=0.3)
        self.remove(ca, cp)
        self.play(FadeOut(flujo), FadeOut(dc), ct.bob[0].animate.set_fill(CU), run_time=0.3)
        self.mover_corte(ct, False, 0.35)
        self.cerrar_voz()
        self.limpiar(pasos)
        # --- corriente de llamada
        self.voz("f_llamada")
        self.play(VGroup(ct, lin, lout, a1, a2, la).animate.scale(0.75, about_point=[-7.0, 0.2, 0]), run_time=0.5)
        ct.gap *= 0.75
        gap_r = Rectangle(width=2.6 * 0.75 * 0.95, height=ct.gap, stroke_color=AMBAR, stroke_width=2).set_fill(AMBAR, 0.3)
        gap_r.move_to([ct.arm.get_center()[0], ct.arm.get_bottom()[1] - ct.gap / 2, 0])
        lg = etiqueta("entrehierro grande", AMBAR, 20).next_to(ct, DOWN, buff=0.1)
        self.play(FadeIn(gap_r), FadeIn(lg), run_time=0.4)
        b0 = Line([1.0, -2.6, 0], [7.0, -2.6, 0]).set_stroke(TXT2, 2)
        bl = Rectangle(width=1.4, height=4.6, stroke_width=0).set_fill(ROJO_P, 1).move_to([2.2, -2.6, 0], aligned_edge=DOWN)
        bm = Rectangle(width=1.4, height=4.6 / 8, stroke_width=0).set_fill(VERDE_OK, 1).move_to([5.6, -2.6, 0], aligned_edge=DOWN)
        el = VGroup(T("LLAMADA", 24, TXT, "HEAVY"), T("Ia", 22, ROJO_P, "HEAVY")).arrange(DOWN, buff=0.05).next_to(b0, DOWN, buff=0.12).set_x(2.2)
        em = VGroup(T("MANTENIMIENTO", 24, TXT, "HEAVY"), T("If", 22, VERDE_OK, "HEAVY")).arrange(DOWN, buff=0.05).next_to(b0, DOWN, buff=0.12).set_x(5.6)
        self.play(Create(b0), GrowFromEdge(bl, DOWN), FadeIn(el), run_time=0.6)
        self.esperar_frac(0.35)
        self.mover_corte(ct, True, 0.3)
        self.play(FadeOut(gap_r), GrowFromEdge(bm, DOWN), FadeIn(em), run_time=0.5)
        x = etiqueta("6 a 10 veces menor", VERDE_OK, 26).next_to(bm, UP, buff=0.3)
        src = fuente("Telesquemario Telemecanique, p. 27", [3.8, -4.1, 0], 18)
        self.play(FadeIn(x, scale=1.1), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ct, lin, lout, a1, a2, la, lg, b0, bl, bm, el, em, x, src)
        self.f_mando_circuito()
        self.f_potencia()

    def f_mando_circuito(self):
        self.voz("f_mando")
        X0, YT, YB = -3.4, 2.75, -3.55
        top = VGroup(Line([X0 - 2.6, YT, 0], [X0 + 2.6, YT, 0]).set_stroke(SIM, SW_MAN))
        bot = VGroup(Line([X0 - 2.6, YB, 0], [X0 + 2.6, YB, 0]).set_stroke("#6F9BFF", SW_MAN))
        lt = VGroup(T("L1", 24, SIM, "HEAVY").next_to(top, LEFT, buff=0.15), T("L1", 24, SIM, "HEAVY").next_to(top, RIGHT, buff=0.15))
        lbt = VGroup(T("N", 24, "#6F9BFF", "HEAVY").next_to(bot, LEFT, buff=0.15), T("N", 24, "#6F9BFF", "HEAVY").next_to(bot, RIGHT, buff=0.15))
        f2 = termico_aux("F2").move_to([X0, 1.85, 0])
        s1 = pulsador(False, "S1", "11", "12").move_to([X0, 0.55, 0])
        s2 = pulsador(True, "S2", "13", "14").move_to([X0, -0.95, 0])
        km = contacto(True, n1="13", n2="14").move_to([X0 + 1.8, -0.95, 0])
        lkm = T("KM1", 22, SIM, "HEAVY").next_to(km, LEFT, buff=0.12).shift(RIGHT * 0.0)
        bob = bobina_sim("KM1").move_to([X0, -2.6, 0])
        for m_ in (f2, s1, s2, bob):
            m_.shift(RIGHT * (X0 - m_[0].get_start()[0]))
        km.shift(RIGHT * (X0 + 1.8 - km[0].get_start()[0]))
        lkm.next_to(km[2], LEFT, buff=0.12)
        w = lambda a, b: Line(a, b).set_stroke(SIM, SW_MAN)
        n_sup, n_inf = s2[0].get_start() + UP * 0.25, s2[1].get_end() + DOWN * 0.25
        lin = VGroup(w([X0, YT, 0], f2[0].get_start()), w(f2[1].get_end(), s1[0].get_start()), w(s1[1].get_end(), n_sup), w(n_sup, s2[0].get_start()),
                     w(s2[1].get_end(), n_inf), w(n_inf, bob[0].get_start()), w(bob[2].get_end(), [X0, YB, 0]),
                     w(n_sup, [X0 + 1.8, n_sup[1], 0]), w([X0 + 1.8, n_sup[1], 0], km[0].get_start()), w(km[1].get_end(), [X0 + 1.8, n_inf[1], 0]),
                     w([X0 + 1.8, n_inf[1], 0], n_inf))
        nodos = VGroup(*[Dot(p, radius=0.07, color=SIM) for p in (n_sup, n_inf, [X0, YT, 0], [X0, YB, 0])])
        # recuadros de color (como el ejemplo del usuario)
        def fondo_c(m, col):
            return SurroundingRectangle(m, buff=0.14, corner_radius=0.12, stroke_width=0).set_fill(col, 0.22)
        bf = fondo_c(f2, AMBAR)
        b1 = fondo_c(s1, ROJO_P)
        b2 = fondo_c(s2, VERDE_P)
        b3 = fondo_c(VGroup(km, lkm), "#6F86D6")
        circ = VGroup(bf, b1, b2, b3, top, bot, lt, lbt, f2, s1, s2, km, lkm, bob, lin, nodos)
        self.play(Create(VGroup(top, bot)), FadeIn(lt), FadeIn(lbt), run_time=0.4)
        self.play(FadeIn(bf), FadeIn(f2), Create(lin[0]), Create(lin[1]), run_time=0.4)
        c_f2 = llamada("Relé térmico (95-96)", f2.get_left() + LEFT * 0.7, [X0 - 2.4 - 0.4, 2.0, 0], AMBAR, 20, 0.5) if False else None
        lbl_f2 = VGroup()
        self.esperar_frac(0.25)
        lbl_s1 = VGroup()
        self.play(FadeIn(b1), FadeIn(s1), Create(lin[2]), FadeIn(lbl_s1), run_time=0.45)
        self.esperar_frac(0.3)
        lbl_s2 = VGroup()
        self.play(FadeIn(b2), FadeIn(s2), Create(lin[3]), Create(lin[4]), FadeIn(lbl_s2), FadeIn(km), FadeIn(lkm), *[Create(l_) for l_ in lin[7:]], run_time=0.5)
        self.play(FadeIn(bob), Create(lin[5]), Create(lin[6]), FadeIn(nodos), run_time=0.4)
        # botonera real
        bp = pulsador_fis(ROJO_P, "O", 1.15).move_to([3.0, 1.7, 0])
        bm = pulsador_fis(VERDE_P, "I", 1.15).move_to([5.6, 1.7, 0])
        tbp = VGroup(T("S1 · PARO", 24, TXT, "HEAVY"), T("rojo", 20, ROJO_P, "BOLD")).arrange(DOWN, buff=0.05).next_to(bp, DOWN, buff=0.18)
        tbm = VGroup(T("S2 · MARCHA", 24, TXT, "HEAVY"), T("verde", 20, VERDE_P, "BOLD")).arrange(DOWN, buff=0.05).next_to(bm, DOWN, buff=0.18)
        self.play(FadeIn(bp), FadeIn(bm), FadeIn(tbp), FadeIn(tbm), run_time=0.4)
        self.cerrar_voz()
        # --- marcha y autoenclavamiento
        self.voz("f_marcha")
        estado = carta("MOTOR DETENIDO", (), TXT2, 5.4, 20).move_to([4.3, -2.6, 0])
        self.play(FadeIn(estado), run_time=0.3)

        def set_estado(txt, col):
            nueva = carta(txt, (), col, 5.4, 20)
            return Transform(estado, nueva.move_to([7.5 - nueva.width / 2, -2.6, 0]))
        self.esperar_frac(0.04)
        self.sfx("tic", -8)
        self.play(bm[2].animate.scale(0.88), mover(s2, True), run_time=0.3)
        ruta1 = [[X0, YT, 0], f2[0].get_start(), f2[1].get_end(), s1[0].get_start(), s1[1].get_end(), n_sup, s2[0].get_start(), s2[1].get_end(), n_inf,
                 bob[0].get_start(), bob[2].get_end(), [X0, YB, 0]]
        cur1 = corriente(ruta1, vel=1.2, escala=1.0, color=CIAN_CORRIENTE)
        self.add(cur1)
        self.play(bob.rect.animate.set_fill(ROJO_P, 0.6), set_estado("BOBINA ENERGIZADA", VERDE_OK), run_time=0.4)
        self.esperar_frac(0.1)
        self.sfx("tic", -10)
        self.play(FadeIn(b3), mover(km, True), run_time=0.35)
        lbl_km = etiqueta("autoenclavamiento", "#6F86D6", 20).next_to(b3, RIGHT, buff=0.15)
        self.play(FadeIn(lbl_km), run_time=0.3)
        self.esperar_frac(0.3)
        self.play(bm[2].animate.scale(1 / 0.88), mover(s2, False), run_time=0.3)
        self.remove(cur1)
        ruta2 = ruta1[:6] + [[X0 + 1.8, n_sup[1], 0], km[0].get_start(), km[1].get_end(), [X0 + 1.8, n_inf[1], 0], n_inf, bob[0].get_start(), bob[2].get_end(), [X0, YB, 0]]
        cur2 = corriente(ruta2, vel=1.2, escala=1.0, color=CIAN_CORRIENTE)
        self.add(cur2)
        self.play(set_estado("ENCLAVADO: sigue en marcha", VERDE_OK), run_time=0.4)
        self.cerrar_voz()
        # --- paro
        self.voz("f_paro")
        self.esperar_frac(0.04)
        self.sfx("tic", -8)
        self.play(bp[2].animate.scale(0.88), mover(s1, True), run_time=0.3)
        self.remove(cur2)
        self.play(mover(km, False), bob.rect.animate.set_fill(opacity=0), set_estado("PARO: bobina sin tensión", ROJO_P), run_time=0.4)
        self.play(bp[2].animate.scale(1 / 0.88), mover(s1, False), run_time=0.3)
        self.esperar_frac(0.08)
        self.play(Indicate(VGroup(bf, f2), color=AMBAR, scale_factor=1.05), run_time=0.6)
        self.esperar_frac(0.2)
        self.play(set_estado("VUELVE LA ENERGÍA: NO ARRANCA SOLO", AMBAR), run_time=0.4)
        self.esperar_frac(0.3)
        nota = T("IEC 60204-1: verde y rojo permitidos", 20, TXT2, "BOLD").move_to([4.3, 0.15, 0])
        self.play(FadeIn(nota), Indicate(VGroup(bp, bm), scale_factor=1.06), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(circ, lbl_f2, lbl_s1, lbl_s2, lbl_km, bp, bm, tbp, tbm, estado, nota)

    def f_potencia(self):
        self.voz("f_potencia")
        xs = [-4.6, -3.6, -2.6]
        YT = 3.0
        L = VGroup(*[T(n, 24, SIM, "HEAVY").move_to([x, YT + 0.3, 0]) for x, n in zip(xs, ("L1", "L2", "L3"))])
        q1 = VGroup(*[contacto(True, interruptor=True, largo=1.0, n1=str(2 * i + 1), n2=str(2 * i + 2), sw=SW_POT).move_to([x, 1.85, 0]) for i, x in enumerate(xs)])
        km = VGroup(*[contacto(True, contactor=True, largo=1.0, n1=str(2 * i + 1), n2=str(2 * i + 2), sw=SW_POT).move_to([x, 0.15, 0]) for i, x in enumerate(xs)])
        f2 = VGroup(*[termico_pot().move_to([x, -1.35, 0]) for x in xs])
        for i, x in enumerate(xs):
            q1[i].shift(RIGHT * (x - q1[i][0].get_start()[0]))
            km[i].shift(RIGHT * (x - km[i][0].get_start()[0]))
            f2[i].shift(RIGHT * (x - f2[i][1].get_start()[0]))
        mo = motor_sim(r=0.75).move_to([-3.6, -3.15, 0])
        # las líneas bajan rectas y entran por los bornes del motor
        w = lambda a, b: Line(a, b).set_stroke(SIM, SW_POT)
        lin = VGroup()
        for i, x in enumerate(xs):
            bor = mo.bornes[i][1].get_center()
            y_q = -2.05
            lin.add(w([x, YT, 0], q1[i][0].get_start()), w(q1[i][1].get_end(), km[i][0].get_start()), w(km[i][1].get_end(), f2[i][1].get_start()),
                    w(f2[i][1].get_end(), [x, y_q, 0]))
            lin.add(VMobject().set_points_as_corners([[x, y_q, 0], [bor[0], y_q - 0.25, 0], bor + UP * 0.06]).set_stroke(SIM, SW_POT))
        dq = DashedLine(q1[0].cuchilla.get_center(), q1[2].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2)
        dk = DashedLine(km[0].cuchilla.get_center(), km[2].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2)
        df = DashedLine(f2[0].get_center(), f2[2].get_center(), dash_length=0.08).set_stroke(SIM, 2)
        lq = T("Q1", 24, SIM, "HEAVY").next_to(q1, LEFT, buff=0.3)
        lk = T("KM1", 24, SIM, "HEAVY").next_to(km, LEFT, buff=0.3)
        lf = T("F2", 24, SIM, "HEAVY").next_to(f2, LEFT, buff=0.3)
        todo = VGroup(L, q1, km, f2, mo, lin, dq, dk, df, lq, lk, lf)
        self.play(LaggedStart(FadeIn(L), FadeIn(q1), FadeIn(km), FadeIn(f2), FadeIn(mo), Create(lin), FadeIn(VGroup(dq, dk, df, lq, lk, lf)), lag_ratio=0.1), run_time=1.5)
        notas = VGroup(carta("Q1 · disyuntor", ["protección contra cortocircuito"], ROJO_P, 5.4, 21),
                       carta("KM1 · contactor", ["conecta y desconecta"], MARCA, 5.4, 21),
                       carta("F2 · relé térmico", ["protección contra sobrecarga"], AMBAR, 5.4, 21)).arrange(DOWN, buff=0.25).move_to([3.6, 0.4, 0])
        self.esperar_frac(0.05)
        self.play(FadeIn(notas[0], shift=LEFT * 0.2), Indicate(q1, color=ROJO_P, scale_factor=1.05), *[mover(q, True) for q in q1], run_time=0.6)
        self.esperar_frac(0.18)
        self.sfx("tic", -8)
        self.play(FadeIn(notas[1], shift=LEFT * 0.2), *[mover(k, True) for k in km], run_time=0.5)
        self.esperar_frac(0.2)
        self.play(FadeIn(notas[2], shift=LEFT * 0.2), Indicate(f2, color=AMBAR, scale_factor=1.05), run_time=0.6)
        self.esperar_frac(0.25)
        curs = VGroup(*[corriente([[x, YT, 0], [x, -2.05, 0], [mo.bornes[i][1].get_center()[0], -2.3, 0], mo.bornes[i][1].get_center()], vel=1.0, escala=1.0)
                        for i, x in enumerate(xs)])
        self.add(curs)
        glow = resplandor(mo.circ.get_center(), 1.1, CIAN_CORRIENTE, 8, 0.05)
        giro = Arc(radius=0.98, start_angle=PI / 6, angle=PI * 1.3, color=VERDE_OK, stroke_width=5).move_arc_center_to(mo.circ.get_center()).add_tip(tip_length=0.2)
        self.play(FadeIn(glow), Create(giro), mo.circ.animate.set_stroke(VERDE_OK), run_time=0.6)
        self.play(Rotate(giro, -TAU, about_point=mo.circ.get_center()), run_time=max(0.5, self.resta() - 0.3), rate_func=linear)
        self.cerrar_voz()
        self.limpiar(todo, notas, curs, glow, giro)

    # ================================================================ 4 · ASPECTOS CRÍTICOS
    def num_critico(self, n):
        c = VGroup(Circle(radius=0.42, stroke_width=0).set_fill(ROJO_P, 1), T(str(n), 40, WHITE, "HEAVY"))
        c[1].move_to(c[0])
        return c

    def f_criticos(self):
        self.portadilla("c_proteccion")
        # 1 · no es protección
        self.voz("c_proteccion")
        n1 = self.num_critico(1).move_to([-6.6, 2.9, 0])
        t1 = T("El contactor NO es una protección", 36, TXT, "HEAVY").next_to(n1, RIGHT, buff=0.3)
        self.play(FadeIn(n1, scale=1.2), FadeIn(t1, shift=RIGHT * 0.2), run_time=0.5)
        ct = contactor_2d(0.85).move_to([-3.6, -0.6, 0])
        ry = VGroup(*[rayo([-1.2, 1.4, 0], [-2.4, -0.2, 0], color=c_, semilla=k, amp=0.15, w=w_) for k, (c_, w_) in enumerate(((AMBAR, 8), (WHITE, 3)))])
        cc = etiqueta("cortocircuito: miles de amperios", ROJO_P, 24).move_to([0.6, 1.9, 0])
        self.play(FadeIn(ct), run_time=0.4)
        self.sfx("pop", -8)
        self.play(FadeIn(ry), FadeIn(cc), Flash([-2.4, -0.2, 0], color=AMBAR), run_time=0.5)
        x_ = equis(ROJO_P, 0.5).next_to(ct, LEFT, buff=0.3)
        self.play(FadeIn(x_, scale=1.4), run_time=0.3)
        self.esperar_frac(0.2)
        nec = VGroup(carta("Q1 · disyuntor o fusibles", ["contra cortocircuito"], ROJO_P, 5.4, 22), carta("F2 · relé de sobrecarga", ["contra sobrecarga"], AMBAR, 5.4, 22)).arrange(DOWN, buff=0.3).move_to([3.9, -0.6, 0])
        self.play(FadeOut(ry), FadeIn(nec[0], shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.4)
        self.play(FadeIn(nec[1], shift=LEFT * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(n1, t1, ct, cc, x_, nec)
        # 2 · tensión de bobina
        self.voz("c_tension")
        n2 = self.num_critico(2).move_to([-6.6, 2.9, 0])
        t2 = T("La tensión de la bobina", 36, TXT, "HEAVY").next_to(n2, RIGHT, buff=0.3)
        self.play(FadeIn(n2, scale=1.2), FadeIn(t2, shift=RIGHT * 0.2), run_time=0.5)
        x0, x1 = -6.0, 6.0

        def xp(p):
            return x0 + (x1 - x0) * p / 200
        eje = Line([x0, 0.6, 0], [x1, 0.6, 0]).set_stroke(TXT2, 3)
        marcas = VGroup(*[VGroup(Line([xp(p), 0.5, 0], [xp(p), 0.7, 0]).set_stroke(TXT2, 2), T(f"{p} %", 20, TXT2, "BOLD").move_to([xp(p), 0.2, 0])) for p in (0, 50, 85, 110, 150, 200)])
        ok = Rectangle(width=xp(110) - xp(85), height=0.6, stroke_width=0).set_fill(VERDE_OK, 0.9).move_to([(xp(85) + xp(110)) / 2, 1.05, 0])
        lok = etiqueta("85 – 110 %: cierra correctamente", VERDE_OK, 22).next_to(ok, UP, buff=0.2)
        src = fuente("IEC 60947-4-1 · límites de funcionamiento del electroimán", [0, -4.1, 0], 20)
        self.play(Create(eje), FadeIn(marcas), run_time=0.5)
        self.play(GrowFromEdge(ok, LEFT), FadeIn(lok), FadeIn(src), run_time=0.5)
        self.esperar_frac(0.2)
        bob = bobina(2.0, 1.1).move_to([-3.6, -2.0, 0])
        lb = etiqueta("bobina de 120 V", ROJO_P, 22).next_to(bob, LEFT, buff=0.3)
        aguja = Triangle().scale(0.18).rotate(PI).set_fill(TXT, 1).set_stroke(width=0).move_to([xp(100), 1.55, 0])
        self.play(FadeIn(bob), FadeIn(lb), FadeIn(aguja), run_time=0.4)
        self.esperar_frac(0.15)
        self.play(aguja.animate.move_to([xp(183), 1.55, 0]), run_time=0.8)
        humo_ = VGroup(*[Circle(radius=0.2 + 0.08 * k).set_fill("#6B7280", 0.35).set_stroke(width=0).move_to(bob.get_top() + UP * (0.3 + 0.35 * k) + RIGHT * 0.15 * (-1) ** k) for k in range(4)])
        q = etiqueta("220 V → se quema", ROJO_P, 24).next_to(bob, RIGHT, buff=0.5)
        self.sfx("pop", -10)
        self.play(bob[0].animate.set_fill("#3A2A20"), FadeIn(humo_, shift=UP * 0.2), FadeIn(q), run_time=0.6)
        self.esperar_frac(0.3)
        self.play(aguja.animate.move_to([xp(60), 1.55, 0]), FadeOut(humo_), bob[0].animate.set_fill(CU), Transform(q, etiqueta("muy poca tensión → no cierra con fuerza", AMBAR, 24).next_to(bob, RIGHT, buff=0.5)), run_time=0.8)
        self.cerrar_voz()
        self.limpiar(n2, t2, eje, marcas, ok, lok, src, bob, lb, aguja, q)
        # 3 · contactos soldados
        self.voz("c_soldadura")
        n3 = self.num_critico(3).move_to([-6.6, 2.9, 0])
        t3 = T("Contactos soldados", 36, TXT, "HEAVY").next_to(n3, RIGHT, buff=0.3)
        self.play(FadeIn(n3, scale=1.2), FadeIn(t3, shift=RIGHT * 0.2), run_time=0.5)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 120, 20], x_length=6.0, y_length=2.8, tips=False, axis_config={"color": TXT2, "stroke_width": 2, "include_ticks": False}).move_to([-3.6, 0.4, 0])
        u = ax.plot(lambda t: 100 if t < 1 else (70 if t < 2.2 else 100 - 30 * np.exp(-(t - 2.2) * 3)), x_range=[0, 4], color=CIAN_CORRIENTE, stroke_width=4, discontinuities=[1.0], use_smoothing=False)
        l85 = DashedLine(ax.c2p(0, 85), ax.c2p(4, 85), dash_length=0.1).set_stroke(VERDE_OK, 2)
        t85 = T("85 %", 20, VERDE_OK, "BOLD").next_to(l85, RIGHT, buff=0.1)
        tu = T("tensión del mando al arrancar el motor", 22, TXT, "BOLD").next_to(ax, UP, buff=0.12)
        self.play(Create(ax), FadeIn(tu), Create(l85), FadeIn(t85), run_time=0.5)
        self.play(Create(u), run_time=1.0)
        cd = etiqueta("caída de tensión", ROJO_P, 22).move_to(ax.c2p(1.6, 35))
        self.play(FadeIn(cd), run_time=0.3)
        self.esperar_frac(0.1)
        f1 = Rectangle(width=2.6, height=0.32, stroke_width=0).set_fill(CU, 1).move_to([3.4, 0.0, 0])
        m1 = Rectangle(width=2.6, height=0.32, stroke_width=0).set_fill(CU, 1).move_to([3.4, 0.9, 0])
        pads = VGroup(*[RoundedRectangle(width=0.5, height=0.1, corner_radius=0.02, stroke_width=0).set_fill(AG, 1).move_to([3.4 + dx, 0.21, 0]) for dx in (-0.8, 0.8)])
        self.play(FadeIn(f1), FadeIn(m1), FadeIn(pads), run_time=0.3)
        for _ in range(3):
            self.play(m1.animate.move_to([3.4, 0.42, 0]), run_time=0.13)
            self.play(m1.animate.move_to([3.4, 0.64, 0]), run_time=0.11)
        self.sfx("pop", -10)
        sold = VGroup(*[Rectangle(width=0.55, height=0.2, stroke_width=0).set_fill("#FFB066", 1).move_to([3.4 + dx, 0.3, 0]) for dx in (-0.8, 0.8)])
        glow = VGroup(*[resplandor([3.4 + dx, 0.3, 0], 0.6, AMBAR, 6, 0.08) for dx in (-0.8, 0.8)])
        self.play(m1.animate.move_to([3.4, 0.4, 0]), FadeIn(sold), FadeIn(glow), run_time=0.3)
        ls = etiqueta("contactos SOLDADOS", ROJO_P, 26).move_to([3.4, -0.9, 0])
        self.play(FadeIn(ls), run_time=0.3)
        self.esperar_frac(0.25)
        pp = etiqueta("pulsas PARO… y el motor sigue girando", AMBAR, 22).move_to([3.4, -1.7, 0])
        self.play(FadeIn(pp), run_time=0.3)
        self.esperar_frac(0.3)
        rev = carta("REVISA", ["sección y largo de los cables", "tensión del circuito de mando"], VERDE_OK, 6.0, 22).move_to([-3.6, -2.6, 0])
        src = fuente("Telesquemario Telemecanique, p. 30", [3.4, -4.1, 0], 18)
        self.play(FadeIn(rev, shift=UP * 0.2), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(n3, t3, ax, u, l85, t85, tu, cd, f1, m1, pads, sold, glow, ls, pp, rev, src)

    # ================================================================ 5 · SELECCIÓN (7 pasos)
    def f_seleccion(self):
        self.portadilla("s_intro")
        self.voz("s_intro")
        crit = ["Corriente nominal", "Tensión de potencia (CA/CC)", "Tensión de control", "Número de polos", "Polos NA o NC", "Categoría de empleo", "Contactos auxiliares"]
        chips = VGroup()
        for i, c_ in enumerate(crit):
            n = VGroup(RoundedRectangle(width=0.56, height=0.56, corner_radius=0.05, stroke_width=0).set_fill(AMBAR, 1), T(str(i + 1), 28, "#08142E", "HEAVY"))
            n[1].move_to(n[0])
            t_ = T(c_, 24, TXT, "BOLD")
            fila = VGroup(n, t_).arrange(RIGHT, buff=0.25)
            caja = RoundedRectangle(width=6.6, height=0.78, corner_radius=0.06, stroke_width=0).set_fill(AZUL_CARTA, 1)
            fila.move_to(caja).align_to(caja.get_left() + RIGHT * 0.25, LEFT)
            chips.add(VGroup(caja, fila))
        col1 = VGroup(*chips[:4]).arrange(DOWN, buff=0.22)
        col2 = VGroup(*chips[4:]).arrange(DOWN, buff=0.22)
        VGroup(col1, col2).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, -0.3, 0])
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in chips], lag_ratio=0.12), run_time=min(2.2, self.resta() - 0.3))
        self.cerrar_voz()
        self.limpiar(chips)
        for i in range(1, 8):
            getattr(self, f"paso{i}")(crit[i - 1])
        self.limpiar(self.paso_act)
        self.paso_act = None

    def encabezado(self, n, texto):
        self.pasar_paso(n)
        st = self.subtitulo(texto)
        self.play(FadeIn(st, shift=DOWN * 0.15), run_time=0.35)
        return st

    def paso1(self, nom):
        self.voz("s1")
        st = self.encabezado(1, "Corriente nominal del circuito de potencia")
        bc = Rectangle(width=1.4, height=3.2, stroke_width=0).set_fill(MARCA, 1).move_to([-2.0, -3.0, 0], aligned_edge=DOWN)
        bl = Rectangle(width=1.4, height=2.4, stroke_width=0).set_fill(AMBAR, 1).move_to([1.0, -3.0, 0], aligned_edge=DOWN)
        b0 = Line([-3.4, -3.0, 0], [2.4, -3.0, 0]).set_stroke(TXT2, 2)
        e1 = T("contactor", 26, MARCA, "HEAVY").next_to(bc, UP, buff=0.12)
        e2 = T("carga", 26, AMBAR, "HEAVY").next_to(bl, UP, buff=0.12)
        ge = T("≥", 90, TXT, "HEAVY").move_to([-0.5, -1.6, 0])
        self.play(Create(b0), GrowFromEdge(bl, DOWN), FadeIn(e2), run_time=0.5)
        self.esperar_frac(0.1)
        self.play(GrowFromEdge(bc, DOWN), FadeIn(e1), FadeIn(ge, scale=1.3), run_time=0.5)
        self.esperar_frac(0.35)
        pl = carta("o como POTENCIA", ["kW o hp, para cada tensión"], AMBAR, 4.6, 22).move_to([5.0, -1.0, 0])
        self.play(FadeIn(pl, shift=LEFT * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(st, bc, bl, b0, e1, e2, ge, pl)

    def paso2(self, nom):
        self.voz("s2")
        st = self.encabezado(2, "Tensión de potencia: ¿alterna o continua?")
        a1 = Axes(x_range=[0, 2, 1], y_range=[-1.2, 1.2, 1], x_length=5.0, y_length=2.2, tips=False, axis_config={"color": TXT2, "stroke_width": 2, "include_ticks": False}).move_to([-3.6, -0.6, 0])
        a2 = a1.copy().move_to([3.4, -0.6, 0])
        s_ = a1.plot(lambda t: np.sin(TAU * t), x_range=[0, 2], color=CIAN_CORRIENTE, stroke_width=4)
        d_ = a2.plot(lambda t: 0.85, x_range=[0, 2], color=AMBAR, stroke_width=4)
        h1 = carta("CA · alterna", (), CIAN_CORRIENTE, 4.0, 24).next_to(a1, UP, buff=0.35)
        h2 = carta("CC · continua", (), AMBAR, 4.0, 24).next_to(a2, UP, buff=0.35)
        self.play(FadeIn(h1), Create(a1), Create(s_), run_time=0.6)
        self.play(FadeIn(h2), Create(a2), Create(d_), run_time=0.6)
        self.esperar_frac(0.3)
        ceros = VGroup(*[Dot(a1.c2p(t, 0), radius=0.09, color=VERDE_OK) for t in (0.5, 1.0, 1.5)])
        z1 = etiqueta("pasa por cero: el arco se apaga", VERDE_OK, 20).next_to(a1, DOWN, buff=0.3)
        z2 = etiqueta("no pasa por cero: arco más difícil", AMBAR, 20).next_to(a2, DOWN, buff=0.3)
        self.play(FadeIn(ceros, scale=2), FadeIn(z1), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(FadeIn(z2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(st, a1, a2, s_, d_, h1, h2, ceros, z1, z2)

    def paso3(self, nom):
        self.voz("s3")
        st = self.encabezado(3, "Tensión de control = tensión de la bobina")
        sim = bobina_sim("KM1").scale(2.0).move_to([-3.6, -0.7, 0])
        o1 = etiqueta("120 V CA ~", ROJO_P, 34).move_to([2.6, 0.4, 0])
        o2 = etiqueta("24 V CC", MARCA, 34).move_to([2.6, -1.6, 0])
        f1 = flecha_a(sim.rect.get_right() + RIGHT * 0.1, o1.get_left(), ROJO_P, 4)
        f2 = flecha_a(sim.rect.get_right() + RIGHT * 0.1, o2.get_left(), MARCA, 4)
        self.play(FadeIn(sim, scale=0.8), run_time=0.4)
        self.esperar_frac(0.25)
        self.play(GrowArrow(f1), FadeIn(o1), run_time=0.4)
        self.esperar_frac(0.3)
        self.play(GrowArrow(f2), FadeIn(o2), run_time=0.4)
        vt = etiqueta("en valor y en tipo", AMBAR, 24).move_to([2.6, -2.9, 0])
        self.play(FadeIn(vt), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(st, sim, o1, o2, f1, f2, vt)

    def paso4(self, nom):
        self.voz("s4")
        st = self.encabezado(4, "Número de polos")
        grupos = VGroup()
        for n, lab in ((1, "1 polo"), (2, "2 polos"), (3, "3 polos"), (4, "4 polos")):
            cs = VGroup(*[contacto(True, contactor=True, largo=1.2, sw=SW_POT) for _ in range(n)]).arrange(RIGHT, buff=0.45)
            if n > 1:
                cs.add(DashedLine(cs[0].cuchilla.get_center(), cs[n - 1].cuchilla.get_center(), dash_length=0.08).set_stroke(SIM, 2))
            t_ = T(lab, 26, TXT, "HEAVY").next_to(cs, DOWN, buff=0.3)
            grupos.add(VGroup(cs, t_))
        grupos.arrange(RIGHT, buff=0.9).move_to([0, -0.6, 0])
        uso = VGroup(etiqueta("monofásico", TXT2, 20).next_to(VGroup(grupos[0], grupos[1]), DOWN, buff=0.35), etiqueta("trifásico", AMBAR, 20).next_to(grupos[2], DOWN, buff=0.35),
                     etiqueta("3 fases + neutro", MARCA, 20).next_to(grupos[3], DOWN, buff=0.35))
        self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in grupos], lag_ratio=0.25), run_time=1.2)
        self.esperar_frac(0.2)
        self.play(LaggedStart(*[FadeIn(u_) for u_ in uso], lag_ratio=0.4), run_time=1.0)
        self.cerrar_voz()
        self.limpiar(st, grupos, uso)

    def paso5(self, nom):
        self.voz("s5")
        st = self.encabezado(5, "Estado de los polos en reposo")
        na = VGroup(*[contacto(True, contactor=True, largo=1.4, sw=SW_POT) for _ in range(3)]).arrange(RIGHT, buff=0.5)
        nc = VGroup(*[contacto(False, contactor=True, largo=1.4, sw=SW_POT) for _ in range(3)]).arrange(RIGHT, buff=0.5)
        VGroup(na, nc).arrange(RIGHT, buff=4.6).move_to([0, -0.3, 0])
        ta = carta("NA · normalmente abiertos", ["lo normal"], VERDE_OK, 4.4, 20).next_to(na, DOWN, buff=0.45)
        tc = carta("NC · normalmente cerrados", ["se piden así"], AMBAR, 4.4, 20).next_to(nc, DOWN, buff=0.45)
        self.play(FadeIn(na), FadeIn(ta, shift=UP * 0.15), run_time=0.5)
        self.esperar_frac(0.4)
        self.play(FadeIn(nc), FadeIn(tc, shift=UP * 0.15), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(st, na, nc, ta, tc)

    def curva_cat(self, cod, k_cierre, k_corte, col, nota):
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 7, 1], x_length=4.2, y_length=3.0, tips=False, axis_config={"color": TXT2, "stroke_width": 2, "include_ticks": False})
        ie = DashedLine(ax.c2p(0, 1), ax.c2p(4, 1), dash_length=0.08).set_stroke(TXT2, 1.5)
        lie = T("Ie", 18, TXT2, "BOLD").next_to(ie, LEFT, buff=0.08)

        def f(t):
            if t < 0.6:
                return 0
            if t < 3.1:
                return 1 + (k_cierre - 1) * np.exp(-(t - 0.6) * (3.0 if k_corte == 1 else 0.0))
            return 0
        cur = ax.plot(f, x_range=[0, 4, 0.01], color=col, stroke_width=4, use_smoothing=False, discontinuities=[0.6, 3.1])
        cierre = VGroup(Dot(ax.c2p(0.6, k_cierre), radius=0.07, color=col), T(f"cierra {k_cierre}×Ie", 20, col, "BOLD").next_to(ax.c2p(0.6, k_cierre), UP + RIGHT, buff=0.08))
        corte = VGroup(Dot(ax.c2p(3.1, k_corte), radius=0.07, color=col), T(f"abre {k_corte}×Ie", 20, col, "BOLD").next_to(ax.c2p(3.1, k_corte), UP, buff=0.12))
        tit = carta(cod, (nota,), col, 4.6, 20)
        tit.next_to(ax, UP, buff=0.3)
        return VGroup(tit, ax, ie, lie, cur, cierre, corte)

    def paso6(self, nom):
        self.voz("s6")
        st = self.encabezado(6, "Tipo de carga: categoría de empleo")
        c1 = self.curva_cat("AC-1", 1, 1, VERDE_OK, "resistencias, hornos")
        c3 = self.curva_cat("AC-3", 6, 1, AMBAR, "motor de jaula girando")
        c4 = self.curva_cat("AC-4", 6, 6, ROJO_P, "frenado, impulsos")
        cs = VGroup(c1, c3, c4).arrange(RIGHT, buff=0.55).move_to([0, -0.75, 0])
        src = fuente("IEC 60947-4-1 · condiciones de cierre y corte por categoría", [0, -4.1, 0], 20)
        self.play(FadeIn(src), run_time=0.2)
        self.esperar_frac(0.08)
        for c_, f_ in ((c1, 0.12), (c3, 0.38), (c4, 0.5)):
            self.play(FadeIn(c_[0], shift=DOWN * 0.15), Create(c_[1]), FadeIn(c_[2]), FadeIn(c_[3]), run_time=0.45)
            self.play(Create(c_[4]), run_time=1.0)
            self.play(FadeIn(c_[5]), run_time=0.3)
            self.play(FadeIn(c_[6]), run_time=0.3)
            if c_ is c3:
                n17 = etiqueta("con tensión reducida (≈ 17 %)", AMBAR, 16).next_to(c3[1], DOWN, buff=0.2)
                self.play(FadeIn(n17), run_time=0.3)
            self.esperar_frac(f_)
        res = etiqueta("mismo aparato: corriente en AC-1 > corriente en AC-3", MARCA, 24).move_to([0, -3.55, 0])
        self.play(FadeOut(n17), FadeIn(res, scale=1.05), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(st, cs, src, res)

    def paso7(self, nom):
        self.voz("s7")
        st = self.encabezado(7, "Contactos auxiliares")
        ct = contactor_2d(0.9).move_to([-3.8, -0.75, 0])
        self.play(FadeIn(ct), run_time=0.4)
        usos = VGroup(etiqueta("autoenclavamiento · 1 NA", MARCA, 24), etiqueta("luz piloto · 1 NA", VERDE_OK, 24), etiqueta("enclavamiento · 1 NC", AMBAR, 24)).arrange(DOWN, buff=0.3).move_to([3.6, 0.3, 0])
        for u_ in usos:
            self.esperar_frac(0.1)
            self.play(FadeIn(u_, shift=LEFT * 0.2), run_time=0.3)
        self.esperar_frac(0.3)
        blq = bloque_aux_frontal(0.62)
        blq.move_to([1.4, -2.3, 0])
        lb = etiqueta("+ bloque auxiliar", MARCA, 22).next_to(blq, RIGHT, buff=0.25)
        self.play(FadeIn(blq, shift=UP * 0.3), FadeIn(lb), run_time=0.4)
        self.sfx("tic", -8)
        self.play(blq.animate.move_to(ct.ventana), FadeOut(lb), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(st, ct, usos, blq)

    # ================================================================ 6 y 7 · EJEMPLOS
    def tabla_pasos(self, x=2.5, y0=2.55):
        filas = VGroup()
        nombres = getattr(self, "CRIT_CORTOS", ["Corriente", "Tensión de potencia", "Tensión de control", "Polos", "Estado en reposo", "Categoría", "Auxiliares"])
        for i, n in enumerate(nombres):
            caja = RoundedRectangle(width=9.4, height=0.7, corner_radius=0.06, stroke_color=AZUL_CARTA, stroke_width=2.4).set_fill(AZUL_CARTA, 1)
            num = VGroup(RoundedRectangle(width=0.46, height=0.46, corner_radius=0.05, stroke_width=0).set_fill(AMBAR, 1), T(str(i + 1), 22, "#08142E", "HEAVY"))
            num[1].move_to(num[0])
            num.move_to(caja.get_left() + RIGHT * 0.42)
            t_ = T(n, 22, TXT2, "BOLD").next_to(num, RIGHT, buff=0.2)
            fila = VGroup(caja, num, t_).move_to([x, y0 - i * 0.82, 0])
            filas.add(fila)
        return filas

    def llenar(self, fila, texto, ok=True, color=TXT):
        v = T(texto, 24, color, "HEAVY")
        if v.width > 4.8:
            v.scale_to_fit_width(4.8)
        v.move_to(fila[0].get_center() + RIGHT * 1.7)
        ck = (check(VERDE_OK, 0.2) if ok else equis(ROJO_P, 0.2)).move_to(fila[0].get_right() + LEFT * 0.35)
        self.play(FadeIn(v, shift=LEFT * 0.15), fila[0].animate.set_stroke(VERDE_OK if ok else ROJO_P, 2.4), run_time=0.3)
        self.sfx("tic", -14)
        self.play(FadeIn(ck, scale=1.3), run_time=0.2)
        return VGroup(v, ck)

    def f_ejemplo1(self):
        self.portadilla("e1_datos")
        self.voz("e1_datos")
        mo = motor_3f(1.05).move_to([-5.0, 1.3, 0])
        datos = carta("BOMBA", ["motor 3~ de jaula · 5 hp", "230 V · 60 Hz · arranque directo", "mando 120 V CA · luz piloto"], MARCA, 4.9, 20).move_to([-5.0, -1.4, 0])
        tabla = self.tabla_pasos()
        self.play(FadeIn(mo), run_time=0.4)
        self.play(FadeIn(datos, shift=UP * 0.2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(f_, shift=LEFT * 0.15) for f_ in tabla], lag_ratio=0.1), run_time=1.0)
        self.cerrar_voz()
        self.voz("e1_pasos")
        vals = VGroup()
        cortes = [0.0, 0.28, 0.12, 0.12, 0.1]
        textos = ["15,2 A  (NEC Tabla 430.250)", "230 V CA trifásica", "bobina 120 V CA", "3 polos", "normalmente abiertos (NA)"]
        for i, (t_, f_) in enumerate(zip(textos, cortes)):
            self.esperar_frac(f_ if i else 0.03)
            vals.add(self.llenar(tabla[i], t_))
            if i == 0:
                self.esperar_frac(0.25)
        self.cerrar_voz()
        self.voz("e1_cat")
        self.esperar_frac(0.05)
        self.play(tabla[5][0].animate.set_stroke(AMBAR, 3), run_time=0.2)
        c12 = carta("Contactor 12 A en AC-3", ["12 A < 15,2 A"], ROJO_P, 4.9, 21).move_to([-5.0, -1.4, 0])
        self.play(FadeOut(datos), FadeIn(c12, shift=UP * 0.2), run_time=0.4)
        x12 = equis(ROJO_P, 0.3).next_to(c12, UP, buff=0.1).align_to(c12, RIGHT)
        self.play(FadeIn(x12, scale=1.4), run_time=0.25)
        self.esperar_frac(0.12)
        c18 = carta("Contactor 18 A en AC-3", ["Schneider LC1D18: 5 hp a 230 V", "ABB AF16: 5 hp a 220–240 V"], VERDE_OK, 4.9, 19).move_to([-5.0, -1.4, 0])
        self.play(FadeOut(c12), FadeOut(x12), FadeIn(c18, shift=UP * 0.2), run_time=0.4)
        vals.add(self.llenar(tabla[5], "AC-3 → 18 A ≥ 15,2 A"))
        self.esperar_frac(0.35)
        vals.add(self.llenar(tabla[6], "2 NA (13-14 + piloto)"))
        res = carta("RESULTADO", ["3 polos NA · 18 A en AC-3 · bobina 120 V CA · 2 NA"], AMBAR, 9.4, 22).move_to([2.5, -3.45, 0])
        src = fuente("Fichas técnicas Schneider LC1D18 y ABB AF16-30-10", [2.5, -4.25, 0], 16)
        self.sfx("ding", -12)
        self.play(FadeIn(res, shift=UP * 0.2), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(mo, tabla, vals, c18, res, src)

    def f_ejemplo2(self):
        self.portadilla("e2_datos")
        self.voz("e2_datos")
        hn = horno(1.05).move_to([-5.0, 1.65, 0])
        gl = resplandor(hn[2].get_center(), 1.0, "#FF6B3D", 8, 0.04)
        pl = plc(1.0).move_to([-5.0, -0.35, 0])
        datos = carta("HORNO", ["3~ · 12 kW · 240 V", "control: PLC a 24 V CC"], MARCA, 4.9, 20).move_to([-5.0, -2.25, 0])
        tabla = self.tabla_pasos()
        self.play(FadeIn(hn), FadeIn(gl), run_time=0.4)
        self.play(FadeIn(pl), FadeIn(datos, shift=UP * 0.2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(f_, shift=LEFT * 0.15) for f_ in tabla], lag_ratio=0.1), run_time=1.0)
        self.cerrar_voz()
        self.voz("e2_pasos")
        f = VGroup(MathTex(r"I=\frac{P}{\sqrt{3}\,V}=\frac{12\,000}{1{,}732\times 240}", color=TXT).scale(0.8), MathTex(r"=28{,}9\ \text{A}", color=AMBAR).scale(0.95))
        f.arrange(RIGHT, buff=0.2).scale_to_fit_width(4.9).move_to([-5.0, -3.7, 0])
        self.play(Write(f), run_time=1.2)
        vals = VGroup()
        cortes = [0.12, 0.22, 0.14, 0.14, 0.1]
        textos = ["28,9 A", "240 V CA trifásica", "bobina 24 V CC", "3 polos", "normalmente abiertos (NA)"]
        for i, (t_, f_) in enumerate(zip(textos, cortes)):
            self.esperar_frac(f_)
            vals.add(self.llenar(tabla[i], t_))
        self.cerrar_voz()
        self.voz("e2_cat")
        self.esperar_frac(0.05)
        c18 = carta("Mismo calibre de 18 A (AC-3)", ["en AC-1: Schneider LC1D18 → 32 A", "ABB AF16 → 30 A (40 °C)"], VERDE_OK, 4.9, 19).move_to([-5.0, -0.5, 0])
        self.play(FadeOut(pl), FadeOut(datos), FadeIn(c18, shift=UP * 0.2), run_time=0.4)
        vals.add(self.llenar(tabla[5], "AC-1 → 30–32 A ≥ 28,9 A"))
        self.esperar_frac(0.2)
        mg = carta("POCO MARGEN", ["revisa la temperatura del tablero"], AMBAR, 4.9, 18).move_to([-5.0, -2.3, 0])
        self.play(FadeIn(mg), run_time=0.3)
        self.esperar_frac(0.35)
        vals.add(self.llenar(tabla[6], "1 NA → entrada del PLC"))
        res = carta("RESULTADO", ["3 polos NA · 18 A (AC-3) = 30–32 A en AC-1 · bobina 24 V CC · 1 NA"], AMBAR, 9.4, 19).move_to([2.5, -3.45, 0])
        src = fuente("Fichas técnicas Schneider LC1D18 y ABB AF16-30-10", [2.5, -4.25, 0], 16)
        self.sfx("ding", -12)
        self.play(FadeOut(f), FadeIn(res, shift=UP * 0.2), FadeIn(src), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(hn, gl, tabla, vals, c18, mg, res, src, self.cinta_act)
        self.cinta_act = None

    # ================================================================ cierre
    def f_final(self):
        self.voz("cierre")
        lg = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(2.8).move_to([3.9, 1.6, 0])
        us = T("@miguelesquit", 36, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        yt = pastilla("SUSCRÍBETE", ROJO, 34, True)
        fb = pastilla("SÍGUEME", MARCA, 34, True)
        botones = VGroup(yt, fb).arrange(DOWN, buff=0.25).next_to(us, DOWN, buff=0.4)
        sig = T(getattr(self, "PROXIMO", "Próximo: EL DISYUNTOR"), 34, TXT, "HEAVY").move_to([-3.6, 3.1, 0])
        cajas = VGroup(*[RoundedRectangle(width=5.6, height=3.15, corner_radius=0.2, stroke_color=METAL2, stroke_width=2).set_fill(CARTA, 1) for _ in range(2)]).arrange(DOWN, buff=0.45).move_to([-3.6, -0.6, 0])
        self.play(FadeIn(sig), FadeIn(cajas, shift=UP * 0.2), FadeIn(lg, scale=0.8), FadeIn(us), run_time=0.7)
        self.play(LaggedStart(FadeIn(yt, scale=1.2), FadeIn(fb, scale=1.2), lag_ratio=0.5), run_time=0.6)
        restante = self.fin_voz - self.renderer.time
        espera = max(self.FIN_SEG, restante + 1.0, min(20.0, self.DURACION_MIN - self.renderer.time))
        self.wait(espera)

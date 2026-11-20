"""E07 · H21 · ¿CÓMO FUNCIONA EL DISYUNTOR? · Selecciona el disyuntor correcto (horizontal, ~6,5 min).
Hereda la línea visual de e06b (portadilla con tecleo, cinta fija, insignia CRITERIO n de 6, tablas de ejemplo).
Render: FORMATO=h VOZ=eleven manim -qh --disable_caching -o final_e07 e07_disyuntor.py DisyuntorB
"""
from e06b_contactor import *
from piezas_proteccion import *
from e07_guion import GUION as G7, SECCIONES as S7


def cable_v(p0, largo, color=C_POT, w=12, etiqueta=None, abajo=False):
    p0 = np.array(p0, float)
    return cable([p0, p0 + (DOWN if abajo else UP) * largo], color, w=w, etiqueta=etiqueta)


class DisyuntorB(ContactorB):
    CARPETA_VOZ = "voz_e07"
    GUION = G7
    SECC = S7
    N_CRIT = 6
    DURACION_MIN = 300.0
    PROXIMO = "Próximo: EL RELÉ TÉRMICO"
    CRIT_CORTOS = ["Tensión y tipo", "Corriente nominal", "Polos", "Curva", "Poder de corte", "Tipo de carga"]

    def construct(self):
        self.cinta_act = None
        self.paso_act = None
        orden = ["gancho", "que_es", "partes", "funciona", "criticos", "seleccion", "ejemplo1", "ejemplo2"]
        solo = os.environ.get("SOLO")
        for paso in orden:
            if solo and paso not in solo.split(","):
                continue
            print(f"@@CAP {paso} {self.renderer.time:.1f}", flush=True)
            getattr(self, "f_" + paso)()
        if not solo:
            self.f_final()

    # ================================================================ GANCHO
    def f_gancho(self):
        self.voz("gancho")
        br = breaker_on(breaker_din(1, 20, "C", s=1.05)).move_to([-5.2, 0.3, 0])
        self.play(FadeIn(br, shift=UP * 0.2), run_time=0.5)
        izq = carta("1,13 × In", ["más de 1 hora", "sin disparar"], VERDE_OK, 4.2, 24).move_to([-1.1, 1.3, 0])
        der = carta("cortocircuito", ["miles de amperios", "abre en < 0,1 s"], ROJO_P, 4.2, 24).move_to([3.9, 1.3, 0])
        self.esperar_frac(0.06)
        self.play(FadeIn(izq, shift=RIGHT * 0.2), run_time=0.4)
        reloj = Arc(radius=0.55, start_angle=PI / 2, angle=-TAU * 0.999, color=VERDE_OK, stroke_width=7).move_to([-1.1, -1.2, 0])
        self.play(Create(reloj), run_time=1.6)
        self.esperar_frac(0.15)
        ry = VGroup(*[rayo([3.0, -0.5, 0], [4.8, -1.9, 0], color=c_, semilla=k, amp=0.18, w=w_) for k, (c_, w_) in enumerate(((AMBAR, 8), (WHITE, 3)))])
        self.sfx("pop", -8)
        self.play(FadeIn(der, shift=LEFT * 0.2), FadeIn(ry), run_time=0.4)
        self.sfx("tic", -4)
        self.play(palanca_breaker(br, False), FadeOut(ry), run_time=0.2)
        preg = T("¿CÓMO SABE LA DIFERENCIA?", 50, TXT, "HEAVY").move_to([1.4, -3.3, 0])
        self.play(Write(preg), run_time=0.7)
        self.esperar_frac(0.3)
        self.limpiar(br, izq, der, reloj, preg, t=0.4)
        t1 = T("¿CÓMO FUNCIONA EL", 54, TXT, "HEAVY")
        t2 = T("DISYUNTOR?", 84, MARCA, "HEAVY")
        t3 = T("Selecciona el disyuntor correcto", 32, TXT2, "BOLD")
        tit = VGroup(t1, t2, t3).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        tit.move_to([-7.3 + tit.width / 2, 1.5, 0])

        def bloque_num(n, l1, l2, col):
            cu = RoundedRectangle(width=1.25, height=1.25, corner_radius=0.07, stroke_width=0).set_fill(col, 1)
            nn = T(n, 72, "#0B1C3D", "HEAVY").move_to(cu)
            tx_ = VGroup(T(l1, 30, "#0B1C3D", "HEAVY"), T(l2, 24, "#344054", "BOLD")).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            fondo = RoundedRectangle(width=tx_.width + 2.0, height=1.25, corner_radius=0.07, stroke_width=0).set_fill(WHITE, 1)
            fondo.align_to(cu, LEFT).align_to(cu, UP)
            tx_.next_to(cu, RIGHT, buff=0.3)
            return VGroup(fondo, cu, nn, tx_)
        tags = VGroup(bloque_num("6", "CRITERIOS", "de selección", AMBAR), bloque_num("2", "EJEMPLOS", "con datos reales", VERDE_OK)).arrange(RIGHT, buff=0.4)
        tags.next_to(tit, DOWN, buff=0.55, aligned_edge=LEFT)
        brs = VGroup(breaker_on(breaker_din(1, 20, "C", s=0.72)), breaker_on(breaker_din(2, 25, "C", s=0.72)), breaker_on(breaker_din(3, 40, "D", s=0.72))).arrange(RIGHT, buff=0.12)
        brs.move_to([5.0, -0.2, 0])
        self.sfx("whoosh", -12)
        self.play(FadeIn(t1, shift=UP * 0.2), FadeIn(t2, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(t3), LaggedStart(*[FadeIn(b_, shift=LEFT * 0.2) for b_ in brs], lag_ratio=0.2), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.2) for t_ in tags], lag_ratio=0.4), run_time=0.7)
        self.cerrar_voz(0.2)
        self.limpiar(tit, brs, tags)

    # ================================================================ 1 · QUÉ ES
    def f_que_es(self):
        self.portadilla("q_def")
        self.voz("q_def")
        nombres = VGroup(etiqueta("DISYUNTOR", MARCA, 30), etiqueta("INTERRUPTOR AUTOMÁTICO", AMBAR, 30), etiqueta("BREAKER", VERDE_OK, 30)).arrange(RIGHT, buff=0.3).move_to([0, 2.7, 0])
        igual = T("= el mismo aparato", 30, TXT2, "BOLD").next_to(nombres, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(n_, shift=DOWN * 0.15) for n_ in nombres], lag_ratio=0.3), run_time=0.9)
        self.play(FadeIn(igual), run_time=0.3)
        self.esperar_frac(0.12)
        lin = VGroup(T("aparato mecánico de conexión capaz de establecer, soportar e interrumpir", 28, TXT, "BOLD"),
                     T("corrientes en condiciones NORMALES, y también interrumpir", 28, TXT, "BOLD"),
                     T("corrientes ANORMALES, como las de CORTOCIRCUITO.", 28, AMBAR, "HEAVY")).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        caja = RoundedRectangle(width=lin.width + 1.0, height=lin.height + 0.8, corner_radius=0.07, stroke_width=0).set_fill(WHITE, 1)
        tab = Rectangle(width=0.16, height=caja.height, stroke_width=0).set_fill(MARCA, 1).align_to(caja, LEFT)
        for l in lin:
            l.set_color("#1D2939")
        lin[2].set_color("#B54708")
        g = VGroup(caja, tab, lin.move_to(caja).shift(RIGHT * 0.1)).move_to([0, -0.6, 0])
        src = fuente("IEC 60050 · IEV 441-14-20 (interruptor automático)", [0, -4.1, 0], 20)
        self.play(FadeIn(caja), FadeIn(tab), FadeIn(src), run_time=0.4)
        for l in lin:
            self.play(FadeIn(l, shift=RIGHT * 0.15), run_time=0.45)
            self.esperar_frac(0.18)
        self.cerrar_voz()
        self.limpiar(nombres, igual, g, src)
        # --- diferencias
        self.voz("q_dif")
        ct = contactor_2d(0.72).move_to([-5.0, 0.4, 0])
        br = breaker_on(breaker_din(1, 20, "C", s=0.82)).move_to([0, 0.4, 0])
        fu = VGroup(RoundedRectangle(width=0.9, height=2.6, corner_radius=0.4, stroke_color="#98A2B3", stroke_width=2).set_fill("#F2F4F7", 1),
                    *[Rectangle(width=1.0, height=0.35, stroke_color="#7A6A3A", stroke_width=1).set_fill("#D9C38A", 1).move_to([0, y, 0]) for y in (1.3, -1.3)])
        fu.move_to([5.0, 0.4, 0])
        l1 = carta("CONTACTOR", ["solo condiciones normales"], TXT2, 3.8, 20).next_to(ct, DOWN, buff=0.35)
        l2 = carta("DISYUNTOR", ["también cortocircuito", "se rearma con la palanca"], VERDE_OK, 3.8, 20).next_to(br, DOWN, buff=0.35)
        l3 = carta("FUSIBLE", ["se funde: hay que cambiarlo"], AMBAR, 3.8, 20).next_to(fu, DOWN, buff=0.35)
        l1.set_y(-2.7); l2.set_y(-2.7); l3.set_y(-2.7)
        self.play(FadeIn(ct), FadeIn(l1, shift=UP * 0.15), run_time=0.5)
        self.esperar_frac(0.25)
        self.play(FadeIn(fu), FadeIn(l3, shift=UP * 0.15), run_time=0.5)
        self.esperar_frac(0.2)
        self.play(FadeIn(br), FadeIn(l2, shift=UP * 0.15), run_time=0.5)
        self.sfx("tic", -8)
        self.play(palanca_breaker(br, False), run_time=0.25)
        self.play(palanca_breaker(br, True), run_time=0.25)
        prot = etiqueta("protege al CONDUCTOR", MARCA, 30).move_to([0, 3.0, 0])
        self.esperar_frac(0.35)
        self.play(FadeIn(prot, scale=1.1), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ct, br, fu, l1, l2, l3, prot)

    # ================================================================ 2 · PARTES
    def f_partes(self):
        self.portadilla("p_intro")
        self.voz("p_intro")
        co = breaker_corte(0.95).move_to([-3.6, -0.35, 0])
        bf = breaker_on(breaker_din(1, 20, "C", s=0.95)).move_to([-3.6, -0.3, 0])
        self.play(FadeIn(bf), run_time=0.4)
        self.esperar_frac(0.2)
        self.sfx("whoosh", -14)
        self.play(FadeOut(bf, scale=1.1), FadeIn(co, scale=0.9), run_time=0.8)
        self.cerrar_voz()
        partes = [("p_palanca", VGroup(co.palanca, co.cerr), "PALANCA Y CERRADURA", ["resortes que abren de golpe", "aunque sostengas la palanca"], MARCA),
                  ("p_contactos", VGroup(co.brazo, co.pad_fijo, co.camara), "CONTACTOS Y CÁMARA", ["pastillas de aleación de plata", "plaquetas que apagan el arco"], AMBAR),
                  ("p_termico", VGroup(co.bimetal, co.barra), "DISPARADOR TÉRMICO", ["lámina bimetálica", "se curva con el calor"], ROJO_P),
                  ("p_magnetico", VGroup(co.espiras, co.embolo, co.nucleo), "DISPARADOR MAGNÉTICO", ["bobina + émbolo", "actúa en milisegundos"], VERDE_OK)]
        for clave, piezas, tit, lin, col in partes:
            self.voz(clave)
            caja = SurroundingRectangle(piezas, color=col, buff=0.1, corner_radius=0.06, stroke_width=4)
            c_ = carta(tit, lin, col, 5.6, 22).move_to([3.9, 1.6, 0])
            self.play(Create(caja), FadeIn(c_, shift=LEFT * 0.2), run_time=0.5)
            ilu = VGroup()
            if clave == "p_palanca":
                self.esperar_frac(0.3)
                self.play(Rotate(co.palanca, 0.7, about_point=co.piv_pal), run_time=0.3)
                self.sfx("tic", -8)
                self.play(Rotate(co.palanca, -0.7, about_point=co.piv_pal), run_time=0.2)
            elif clave == "p_contactos":
                self.esperar_frac(0.3)
                ry = VGroup(*[rayo(co.pad_fijo.get_center(), co.camara.get_top() + LEFT * 0.2 + DOWN * 0.2 * j, color=AMBAR, semilla=j, amp=0.06, w=4) for j in range(3)])
                self.play(FadeIn(ry), run_time=0.3)
                self.play(FadeOut(ry), run_time=0.4)
            elif clave == "p_termico":
                # zoom didáctico del bimetal
                tira = VGroup(Rectangle(width=4.0, height=0.25, stroke_width=0).set_fill("#C0C6CF", 1), Rectangle(width=4.0, height=0.25, stroke_width=0).set_fill("#D9844A", 1)).arrange(DOWN, buff=0)
                tira.move_to([3.9, -1.3, 0])
                la = T("metal A: se dilata poco", 18, TXT2, "BOLD").next_to(tira, UP, buff=0.1)
                lb = T("metal B: se dilata más", 18, "#F0A15E", "BOLD").next_to(tira, DOWN, buff=0.1)
                self.play(FadeIn(tira), FadeIn(la), FadeIn(lb), run_time=0.4)
                self.esperar_frac(0.3)
                curva = VGroup(ArcBetweenPoints(tira[0].get_left(), tira[0].get_right(), angle=-0.7).set_stroke("#C0C6CF", 14),
                               ArcBetweenPoints(tira[1].get_left(), tira[1].get_right(), angle=-0.7).set_stroke("#D9844A", 14)).arrange(DOWN, buff=-0.02).move_to(tira).shift(UP * 0.15)
                gl = resplandor(tira.get_center(), 1.2, "#FF6B3D", 8, 0.05)
                self.play(ReplacementTransform(tira, curva), FadeOut(la), FadeOut(lb), FadeIn(gl), run_time=0.9)
                la, lb = VGroup(), VGroup()
                ilu.add(curva, la, lb, gl)
            elif clave == "p_magnetico":
                self.esperar_frac(0.35)
                self.play(co.espiras.animate.set_fill("#F0A15E"), run_time=0.3)
                self.play(co.embolo.animate.shift(DOWN * 0.35), run_time=0.15)
                self.play(co.embolo.animate.shift(UP * 0.35), co.espiras.animate.set_fill(CU), run_time=0.3)
            self.cerrar_voz()
            self.limpiar(caja, c_, ilu)
        # símbolo
        self.voz("p_simbolo")
        sim = sim_interruptor_auto("Q1").scale(1.6).move_to([3.0, 0.4, 0])
        cs = carta("SÍMBOLO · IEC 60617", ["contacto con CRUZ = interruptor automático", "I> magnético · escalón = térmico", "identificación: Q"], MARCA, 5.6, 20).move_to([4.0, -2.6, 0])
        self.play(co.animate.scale(0.8).move_to([-4.6, -0.2, 0]), run_time=0.5)
        self.play(FadeIn(sim, scale=0.8), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(FadeIn(cs, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(co, sim, cs)

    # ================================================================ 3 · FUNCIONAMIENTO
    def f_funciona(self):
        self.portadilla("f_sobrecarga")
        self.voz("f_sobrecarga")
        co = breaker_corte(0.95).move_to([-3.8, -0.3, 0])
        self.play(FadeIn(co), run_time=0.4)
        cur = corriente(co.camino, vel=0.8, escala=1.1)
        self.add(cur)
        med = carta("1,2 × In", ["sobrecarga leve"], AMBAR, 4.0, 22).move_to([3.6, 2.4, 0])
        self.play(FadeIn(med, shift=LEFT * 0.2), run_time=0.4)
        gl = resplandor(co.bimetal.get_center(), 1.0, "#FF6B3D", 8, 0.0)
        self.add(gl)
        self.play(*[c_.animate.set_fill(opacity=0.05) for c_ in gl], run_time=2.5)
        self.esperar_frac(0.15)
        bc = co.bimetal_curvo
        self.play(FadeOut(co.bimetal), bc.animate.set_stroke(opacity=1), co.barra.animate.shift(LEFT * 0.35), run_time=1.6)
        self.sfx("tic", -6)
        self.remove(cur)
        self.play(Rotate(co.brazo, 0.5, about_point=co.piv), run_time=0.2)
        # tiempo inverso: barras
        ejes = VGroup(Line([1.0, -2.6, 0], [7.0, -2.6, 0]).set_stroke(TXT2, 2))
        datos = [(1.2, "1,2×", 2.2, AMBAR), (2, "2×", 1.2, "#F79009"), (4, "4×", 0.5, ROJO_P)]
        barras = VGroup()
        for i, (k, et, h, c_) in enumerate(datos):
            b_ = Rectangle(width=1.1, height=h, stroke_width=0).set_fill(c_, 1).move_to([2.0 + 1.9 * i, -2.6, 0], aligned_edge=DOWN)
            barras.add(VGroup(b_, T(et, 24, TXT, "HEAVY").next_to(b_, DOWN, buff=0.12)))
        tt = T("tiempo de disparo", 22, TXT2, "BOLD").move_to([4.0, 0.0, 0])
        self.esperar_frac(0.15)
        self.play(Create(ejes), FadeIn(tt), LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in barras], lag_ratio=0.3), *[FadeIn(b_[1]) for b_ in barras], run_time=1.2)
        inv = etiqueta("TIEMPO INVERSO: más corriente, menos tiempo", MARCA, 22).move_to([4.0, 1.1, 0])
        self.play(FadeIn(inv), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(co, bc, gl, med, ejes, barras, tt, inv)
        # --- cortocircuito
        self.voz("f_corto")
        co = breaker_corte(0.95).move_to([-3.8, -0.3, 0])
        self.play(FadeIn(co), run_time=0.3)
        med = carta("CORTOCIRCUITO", ["cientos o miles de amperios"], ROJO_P, 4.6, 22).move_to([3.6, 2.4, 0])
        cur = corriente(co.camino, vel=3.0, escala=1.3, color=ROJO)
        self.add(cur)
        self.play(FadeIn(med, shift=LEFT * 0.2), co.espiras.animate.set_fill("#F0A15E"), run_time=0.5)
        self.esperar_frac(0.15)
        self.play(co.embolo.animate.shift(DOWN * 0.4), run_time=0.12)
        self.sfx("pop", -6)
        self.play(Rotate(co.brazo, 0.5, about_point=co.piv), run_time=0.12)
        self.remove(cur)
        arcos = VGroup(*[rayo(co.pad_fijo.get_center() + LEFT * 0.1 * j, co.camara[j * 2].get_center() + RIGHT * 0.3, color=AMBAR, semilla=j, amp=0.08, w=5) for j in range(4)])
        glow = resplandor(co.camara.get_center(), 0.9, AMBAR, 8, 0.07)
        self.play(FadeIn(arcos), FadeIn(glow), run_time=0.2)
        self.esperar_frac(0.2)
        self.play(FadeOut(arcos), FadeOut(glow), co.espiras.animate.set_fill(CU), run_time=0.4)
        t01 = VGroup(T("< 0,1 s", 90, AMBAR, "HEAVY"), T("todo el proceso", 26, TXT2, "BOLD")).arrange(DOWN, buff=0.1).move_to([3.6, -0.6, 0])
        self.play(FadeIn(t01, scale=1.1), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(co, med, t01)
        # --- curva de disparo
        self.voz("f_curva")
        gr = GraficaLog(7.6, 5.6).move_to([-2.2, 0.2, 0])
        self.play(FadeIn(gr), run_time=0.5)
        x113 = DashedLine(gr.pt(1.13, 0.01), gr.pt(1.13, 10000), dash_length=0.08).set_stroke(VERDE_OK, 3)
        x145 = DashedLine(gr.pt(1.45, 0.01), gr.pt(1.45, 10000), dash_length=0.08).set_stroke(ROJO_P, 3)
        h1 = DashedLine(gr.pt(1, 3600), gr.pt(100, 3600), dash_length=0.08).set_stroke(TXT2, 1.5)
        c1 = carta("1,13 × In", ["NO dispara en 1 h"], VERDE_OK, 3.6, 20).move_to([5.5, 2.5, 0])
        c2 = carta("1,45 × In", ["dispara antes de 1 h"], ROJO_P, 3.6, 20).move_to([5.5, 1.0, 0])
        self.esperar_frac(0.05)
        self.play(Create(h1), Create(x113), FadeIn(c1, shift=LEFT * 0.2), run_time=0.6)
        self.esperar_frac(0.12)
        self.play(Create(x145), FadeIn(c2, shift=LEFT * 0.2), run_time=0.6)
        self.esperar_frac(0.1)
        bandas = [(3, 5, VERDE_OK, "B · 3–5 In"), (5, 10, AMBAR, "C · 5–10 In"), (10, 20, ROJO_P, "D · 10–20 In")]
        cartas = VGroup()
        for i, (k0, k1, c_, txt_) in enumerate(bandas):
            bd = banda_disparo(gr, k0, k1, c_, 0.25)
            et = etiqueta(txt_, c_, 22).move_to([5.5, -0.6 - 0.75 * i, 0])
            self.play(FadeIn(bd), FadeIn(et, shift=LEFT * 0.2), run_time=0.6)
            cartas.add(VGroup(bd, et))
            self.esperar_frac(0.2)
        src = fuente("IEC 60898-1 · curvas B, C y D (referencia 30 °C)", [0, -4.1, 0], 20)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz()
        self.limpiar(gr, x113, x145, h1, c1, c2, cartas, src)

    # ================================================================ 4 · CRÍTICOS
    def f_criticos(self):
        self.portadilla("c_cable")
        self.voz("c_cable")
        n1 = self.num_critico(1).move_to([-6.6, 2.9, 0])
        t1 = T("Protege al CABLE, no al aparato", 36, TXT, "HEAVY").next_to(n1, RIGHT, buff=0.3)
        self.play(FadeIn(n1, scale=1.2), FadeIn(t1, shift=RIGHT * 0.2), run_time=0.5)
        br = breaker_on(breaker_din(1, 20, "C", s=0.9)).move_to([-4.6, -0.6, 0])
        cab = cable([br.tor_inf[0].get_center(), br.tor_inf[0].get_center() + DOWN * 0.8, [1.0, br.tor_inf[0].get_center()[1] - 0.8, 0]], C_POT, w=16, etiqueta="12 AWG")
        self.add(cab)
        self.bring_to_front(br)
        self.play(FadeIn(br), Create(cab), run_time=0.6)
        regla = VGroup(T("I breaker ≤ I conductor", 48, AMBAR, "HEAVY"), T("12 AWG → máximo 20 A", 34, TXT, "BOLD")).arrange(DOWN, buff=0.25).move_to([3.3, 0.4, 0])
        self.esperar_frac(0.2)
        self.play(Write(regla[0]), run_time=0.7)
        self.esperar_frac(0.3)
        self.play(FadeIn(regla[1], shift=UP * 0.15), run_time=0.4)
        src = fuente("NEC 2020 · 240.4(D)", [3.3, -1.3, 0], 20)
        self.play(FadeIn(src), run_time=0.2)
        self.cerrar_voz()
        self.limpiar(n1, t1, br, cab, regla, src)
        # 2 poder de corte
        self.voz("c_poder")
        n2 = self.num_critico(2).move_to([-6.6, 2.9, 0])
        t2 = T("El poder de corte", 36, TXT, "HEAVY").next_to(n2, RIGHT, buff=0.3)
        self.play(FadeIn(n2, scale=1.2), FadeIn(t2, shift=RIGHT * 0.2), run_time=0.5)
        br = breaker_on(breaker_din(1, 20, "C", s=1.2)).move_to([-4.6, -0.6, 0])
        self.play(FadeIn(br), run_time=0.4)
        self.esperar_frac(0.25)
        rc = SurroundingRectangle(br.icn, color=AMBAR, buff=0.08, stroke_width=4)
        self.play(Create(rc), Indicate(br.icn, color=AMBAR, scale_factor=1.3), run_time=0.6)
        k6 = VGroup(T("6000", 80, AMBAR, "HEAVY"), T("= 6 kA = 6 000 A", 34, TXT, "BOLD")).arrange(DOWN, buff=0.15).move_to([2.6, 0.9, 0])
        self.play(FadeIn(k6, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.3)
        reg = carta("NEC · 110.9", ["poder de corte ≥ corriente de falla", "disponible en los bornes"], MARCA, 6.0, 22).move_to([2.6, -2.2, 0])
        self.play(FadeIn(reg, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(n2, t2, br, rc, k6, reg)
        # 3 temperatura
        self.voz("c_temp")
        n3 = self.num_critico(3).move_to([-6.6, 2.9, 0])
        t3 = T("La temperatura del tablero", 36, TXT, "HEAVY").next_to(n3, RIGHT, buff=0.3)
        self.play(FadeIn(n3, scale=1.2), FadeIn(t3, shift=RIGHT * 0.2), run_time=0.5)
        fila = VGroup(*[breaker_on(breaker_din(1, 20, "C", s=0.62)) for _ in range(6)]).arrange(RIGHT, buff=0.0).move_to([-2.6, -0.4, 0])
        self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.15) for b_ in fila], lag_ratio=0.1), run_time=0.7)
        t30 = etiqueta("curva calibrada a 30 °C", VERDE_OK, 26).move_to([3.8, 1.3, 0])
        self.play(FadeIn(t30), run_time=0.3)
        self.esperar_frac(0.25)
        gl = resplandor(fila.get_center(), 3.0, "#FF6B3D", 10, 0.04)
        t50 = etiqueta("tablero caliente → dispara antes", ROJO_P, 26).move_to([3.8, 0.2, 0])
        self.play(FadeIn(gl), FadeIn(t50), run_time=0.7)
        self.esperar_frac(0.3)
        ven = etiqueta("ventila y deja espacio", MARCA, 26).move_to([3.8, -0.9, 0])
        self.play(FadeIn(ven), FadeOut(gl), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(n3, t3, fila, t30, t50, ven)

    # ================================================================ 5 · SELECCIÓN
    def f_seleccion(self):
        self.portadilla("s_intro")
        self.voz("s_intro")
        crit = ["Tensión y tipo de corriente", "Corriente nominal", "Número de polos", "Curva de disparo", "Poder de corte", "Tipo de carga"]
        chips = VGroup()
        for i, c_ in enumerate(crit):
            n = VGroup(RoundedRectangle(width=0.56, height=0.56, corner_radius=0.05, stroke_width=0).set_fill(AMBAR, 1), T(str(i + 1), 28, "#08142E", "HEAVY"))
            n[1].move_to(n[0])
            t_ = T(c_, 24, TXT, "BOLD")
            fila = VGroup(n, t_).arrange(RIGHT, buff=0.25)
            caja = RoundedRectangle(width=6.6, height=0.78, corner_radius=0.06, stroke_width=0).set_fill(AZUL_CARTA, 1)
            fila.move_to(caja).align_to(caja.get_left() + RIGHT * 0.25, LEFT)
            chips.add(VGroup(caja, fila))
        col1 = VGroup(*chips[:3]).arrange(DOWN, buff=0.22)
        col2 = VGroup(*chips[3:]).arrange(DOWN, buff=0.22)
        VGroup(col1, col2).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, -0.3, 0])
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in chips], lag_ratio=0.12), run_time=min(1.8, max(0.6, self.resta() - 0.3)))
        self.cerrar_voz()
        self.limpiar(chips)
        for i in range(1, 7):
            getattr(self, f"crit{i}")()
        self.limpiar(self.paso_act)
        self.paso_act = None

    def crit1(self):
        self.voz("s1")
        st = self.encabezado(1, "Tensión y tipo de corriente")
        br = breaker_on(breaker_din(2, 20, "C", s=1.05)).move_to([-4.2, -0.8, 0])
        self.play(FadeIn(br), run_time=0.4)
        rc = SurroundingRectangle(br[-2], color=AMBAR, buff=0.06)
        self.play(Create(rc), run_time=0.4)
        ok = VGroup(carta("U breaker ≥ U circuito", ["p. ej. 230/400 V~ en un circuito de 240 V"], VERDE_OK, 6.4, 22),
                    carta("CA (~) o CC (⎓)", ["la corriente continua no pasa por cero", "el arco es más difícil de apagar"], AMBAR, 6.4, 22)).arrange(DOWN, buff=0.35).move_to([3.0, -0.6, 0])
        self.esperar_frac(0.2)
        self.play(FadeIn(ok[0], shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.35)
        self.play(FadeIn(ok[1], shift=LEFT * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(st, br, rc, ok)

    def crit2(self):
        self.voz("s2")
        st = self.encabezado(2, "Corriente nominal: entre la carga y el cable")
        b0 = Line([-5.0, -3.0, 0], [3.0, -3.0, 0]).set_stroke(TXT2, 2)
        bl = Rectangle(width=1.5, height=1.9, stroke_width=0).set_fill(AMBAR, 1).move_to([-3.6, -3.0, 0], aligned_edge=DOWN)
        bb = Rectangle(width=1.5, height=2.6, stroke_width=0).set_fill(MARCA, 1).move_to([-1.0, -3.0, 0], aligned_edge=DOWN)
        bc = Rectangle(width=1.5, height=3.1, stroke_width=0).set_fill(VERDE_OK, 1).move_to([1.6, -3.0, 0], aligned_edge=DOWN)
        et = VGroup(T("carga", 24, AMBAR, "HEAVY").next_to(bl, UP, buff=0.1), T("breaker", 24, MARCA, "HEAVY").next_to(bb, UP, buff=0.1), T("cable", 24, VERDE_OK, "HEAVY").next_to(bc, UP, buff=0.1))
        le = VGroup(T("≤", 70, TXT, "HEAVY").move_to([-2.3, -1.4, 0]), T("≤", 70, TXT, "HEAVY").move_to([0.3, -1.2, 0]))
        self.play(Create(b0), GrowFromEdge(bl, DOWN), FadeIn(et[0]), run_time=0.5)
        self.esperar_frac(0.2)
        self.play(GrowFromEdge(bb, DOWN), FadeIn(et[1]), FadeIn(le[0]), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(GrowFromEdge(bc, DOWN), FadeIn(et[2]), FadeIn(le[1]), run_time=0.5)
        vals = carta("valores normalizados", ["15 · 20 · 25 · 30 · 35 · 40 A…", "NEC Tabla 240.6(A)"], MARCA, 4.6, 20).move_to([5.3, -0.8, 0])
        self.play(FadeIn(vals, shift=LEFT * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(st, b0, bl, bb, bc, et, le, vals)

    def crit3(self):
        self.voz("s3")
        st = self.encabezado(3, "Número de polos")
        brs = VGroup(breaker_on(breaker_din(1, 20, "C", s=0.85)), breaker_on(breaker_din(2, 20, "C", s=0.85)), breaker_on(breaker_din(3, 20, "C", s=0.85))).arrange(RIGHT, buff=1.4).move_to([0, -0.3, 0])
        labs = [("1 polo", "120 V"), ("2 polos", "240 V"), ("3 polos", "trifásico")]
        for b_, (a, c_) in zip(brs, labs):
            l_ = VGroup(T(a, 28, TXT, "HEAVY"), T(c_, 24, AMBAR, "BOLD")).arrange(DOWN, buff=0.06).next_to(b_, DOWN, buff=0.25)
            self.play(FadeIn(b_, shift=UP * 0.2), FadeIn(l_), run_time=0.45)
            b_.add(l_)
            self.esperar_frac(0.22)
        self.cerrar_voz()
        self.limpiar(st, brs)

    def crit4(self):
        self.voz("s4")
        st = self.encabezado(4, "Curva de disparo")
        gr = GraficaLog(6.0, 4.4).move_to([-3.2, -0.6, 0])
        self.play(FadeIn(gr), run_time=0.4)
        usos = [(3, 5, VERDE_OK, "B", "sin arranque · cables largos"), (5, 10, AMBAR, "C", "uso general: luces y tomas"), (10, 20, ROJO_P, "D", "motores y transformadores")]
        extra = VGroup()
        for i, (k0, k1, c_, cod, uso) in enumerate(usos):
            bd = banda_disparo(gr, k0, k1, c_, 0.25)
            cc = carta(f"CURVA {cod}", [uso], c_, 5.0, 22).move_to([4.2, 1.2 - 1.45 * i, 0])
            self.play(FadeIn(bd), FadeIn(cc, shift=LEFT * 0.2), run_time=0.5)
            extra.add(bd, cc)
            self.esperar_frac(0.28)
        self.cerrar_voz()
        self.limpiar(st, gr, extra)

    def crit5(self):
        self.voz("s5")
        st = self.encabezado(5, "Poder de corte ≥ falla disponible")
        br = breaker_on(breaker_din(1, 20, "C", s=1.1, icn="10000")).move_to([-4.2, -0.8, 0])
        self.play(FadeIn(br), run_time=0.4)
        b0 = Line([-1.0, -3.0, 0], [5.0, -3.0, 0]).set_stroke(TXT2, 2)
        bf = Rectangle(width=1.4, height=2.2, stroke_width=0).set_fill(ROJO_P, 1).move_to([0.6, -3.0, 0], aligned_edge=DOWN)
        bp = Rectangle(width=1.4, height=3.3, stroke_width=0).set_fill(VERDE_OK, 1).move_to([3.4, -3.0, 0], aligned_edge=DOWN)
        e1 = VGroup(T("falla disponible", 22, ROJO_P, "HEAVY"), T("p. ej. 7 kA", 20, TXT2, "BOLD")).arrange(DOWN, buff=0.04).next_to(bf, UP, buff=0.1)
        e2 = VGroup(T("poder de corte", 22, VERDE_OK, "HEAVY"), T("10 kA", 20, TXT2, "BOLD")).arrange(DOWN, buff=0.04).next_to(bp, UP, buff=0.1)
        self.play(Create(b0), GrowFromEdge(bf, DOWN), FadeIn(e1), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(GrowFromEdge(bp, DOWN), FadeIn(e2), Indicate(br.icn, color=VERDE_OK, scale_factor=1.3), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(st, br, b0, bf, bp, e1, e2)

    def crit6(self):
        self.voz("s6")
        st = self.encabezado(6, "Tipo de carga: ¿es un motor?")
        ct = contactor_2d(0.62)
        rl = rele_termico(0.62)
        montar_rele(ct, rl)
        grupo = VGroup(rl, ct)
        br = breaker_on(breaker_din(3, 40, "D", s=0.62))
        col = VGroup(br, grupo).arrange(DOWN, buff=0.3)
        col.scale_to_fit_height(5.6).move_to([-4.2, -1.15, 0])
        self.play(FadeIn(col, shift=UP * 0.2), run_time=0.6)
        c1 = carta("BREAKER", ["solo cortocircuito", "puede ser más grande (Art. 430)"], ROJO_P, 5.4, 22).move_to([3.0, 0.9, 0])
        c2 = carta("RELÉ TÉRMICO", ["cuida la sobrecarga del motor"], AMBAR, 5.4, 22).move_to([3.0, -1.4, 0])
        f1 = flecha_a(c1.get_left(), br.get_right() + RIGHT * 0.1, ROJO_P, 4)
        f2 = flecha_a(c2.get_left(), rl.get_right() + RIGHT * 0.1, AMBAR, 4)
        self.esperar_frac(0.2)
        self.play(FadeIn(c1, shift=LEFT * 0.2), GrowArrow(f1), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(FadeIn(c2, shift=LEFT * 0.2), GrowArrow(f2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(st, col, c1, c2, f1, f2)

    # ================================================================ EJEMPLOS
    def calentador(self, s=1.0):
        tanque = RoundedRectangle(width=2.0 * s, height=3.2 * s, corner_radius=0.9 * s, stroke_color="#98A2B3", stroke_width=2).set_fill("#E4E7EC", 1)
        franja = Rectangle(width=2.0 * s, height=0.3 * s, stroke_width=0).set_fill("#2F6FD0", 1).move_to(tanque.get_center() + UP * 0.6 * s)
        tubos = VGroup(*[Rectangle(width=0.16 * s, height=0.5 * s, stroke_width=0).set_fill("#98A2B3", 1).move_to(tanque.get_top() + RIGHT * x * s + UP * 0.15 * s) for x in (-0.5, 0.5)])
        caja = Rectangle(width=0.7 * s, height=0.5 * s, stroke_color="#667085", stroke_width=1).set_fill("#D0D5DD", 1).move_to(tanque.get_center() + DOWN * 0.7 * s)
        dato = tx("4500 W · 240 V", 0.13 * s, "#101828").move_to(tanque.get_center() + DOWN * 0.1 * s)
        return VGroup(tubos, tanque, franja, caja, dato)

    def f_ejemplo1(self):
        self.portadilla("e1_datos")
        self.voz("e1_datos")
        ca = self.calentador(1.0).move_to([-5.0, 1.0, 0])
        datos = carta("CALENTADOR", ["de almacenamiento", "4 500 W · 240 V"], MARCA, 4.6, 22).move_to([-5.0, -1.9, 0])
        tabla = self.tabla_pasos(y0=2.4)
        self.play(FadeIn(ca), FadeIn(datos, shift=UP * 0.2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(f_, shift=LEFT * 0.15) for f_ in tabla], lag_ratio=0.1), run_time=0.9)
        self.cerrar_voz()
        self.voz("e1_pasos")
        vals = VGroup()
        vals.add(self.llenar(tabla[0], "240 V CA"))
        self.esperar_frac(0.1)
        f = VGroup(MathTex(r"I=\frac{4500\,\text{W}}{240\,\text{V}}=18{,}75\ \text{A}", color=TXT).scale(0.8),
                   MathTex(r"18{,}75\times1{,}25=23{,}4\ \text{A}", color=AMBAR).scale(0.8)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        f.move_to([-5.0, -3.3, 0])
        self.play(FadeOut(datos), Write(f[0]), run_time=0.9)
        self.esperar_frac(0.25)
        nec = etiqueta("NEC 422.13: 125 %", MARCA, 20).move_to([-5.0, -1.75, 0])
        self.play(Write(f[1]), FadeIn(nec), run_time=0.9)
        self.esperar_frac(0.3)
        vals.add(self.llenar(tabla[1], "25 A · cable 10 AWG"))
        self.cerrar_voz()
        self.voz("e1_resto")
        textos = ["2 polos", "curva C (resistencia)", "≥ falla disponible (10 kA)", "resistiva"]
        for i, t_ in enumerate(textos):
            self.esperar_frac(0.1 if i else 0.03)
            vals.add(self.llenar(tabla[2 + i], t_))
        res = carta("RESULTADO", ["breaker 2 polos · C25 · poder de corte según el tablero"], AMBAR, 9.4, 20).move_to([2.5, -3.5, 0])
        self.sfx("ding", -12)
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.4)
        b25 = breaker_on(breaker_din(2, 25, "C", s=0.5, icn="10000")).move_to([-5.0, 1.0, 0])
        self.play(FadeOut(ca), FadeIn(b25, scale=0.9), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(b25, tabla, vals, f, nec, res)

    def f_ejemplo2(self):
        self.portadilla("e2_datos")
        self.voz("e2_datos")
        mo = motor_3f(1.05).move_to([-5.0, 1.3, 0])
        datos = carta("BOMBA", ["motor 3~ de jaula", "5 hp · 230 V"], MARCA, 4.6, 22).move_to([-5.0, -1.4, 0])
        tabla = self.tabla_pasos(y0=2.4)
        self.play(FadeIn(mo), FadeIn(datos, shift=UP * 0.2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(f_, shift=LEFT * 0.15) for f_ in tabla], lag_ratio=0.1), run_time=0.9)
        self.cerrar_voz()
        self.voz("e2_pasos")
        vals = VGroup()
        textos = ["230 V CA trifásica", "15,2 A (NEC Tabla 430.250)", "3 polos", "curva D (arranque)"]
        cortes = [0.03, 0.15, 0.3, 0.12]
        for i, (t_, c_) in enumerate(zip(textos, cortes)):
            self.esperar_frac(c_)
            vals.add(self.llenar(tabla[i], t_))
        self.cerrar_voz()
        self.voz("e2_resto")
        vals.add(self.llenar(tabla[4], "según el tablero"))
        self.esperar_frac(0.15)
        f = VGroup(MathTex(r"15{,}2\times2{,}5=38\ \text{A}", color=TXT).scale(0.85), MathTex(r"\rightarrow 40\ \text{A}", color=AMBAR).scale(0.95)).arrange(RIGHT, buff=0.25)
        f.move_to([-5.0, -3.3, 0])
        nec = etiqueta("NEC Tabla 430.52: 250 %", MARCA, 20).move_to([-5.0, -2.55, 0])
        self.play(FadeOut(datos), FadeIn(nec), Write(f[0]), run_time=0.9)
        self.esperar_frac(0.3)
        self.play(Write(f[1]), run_time=0.5)
        vals.add(self.llenar(tabla[5], "motor → 40 A, solo cortocircuito"))
        self.esperar_frac(0.3)
        res = carta("RESULTADO", ["breaker 3 polos · D40 · + relé térmico para la sobrecarga"], AMBAR, 9.4, 20).move_to([2.5, -3.5, 0])
        self.sfx("ding", -12)
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(mo, tabla, vals, f, nec, res, self.cinta_act)
        self.cinta_act = None

"""E04 · Tomacorriente con tierra NEMA 5-15. Guion y fuentes en e04_guion.py."""
from taller import *
from comun_e import _osc, _cla
from e04_guion import GUION

R1_C = P(-0.6, -1.3)
R2_C = P(4.4, -1.3)
TOP1 = R1_C[1] + SW_H / 2
XA1, XB1 = R1_C[0] - 0.25, R1_C[0] + 0.25
TA = [E, P(E[0], 2.0), P(XA1, 2.0), P(XA1, TOP1)]
TB = [P(XB1, TOP1), P(XB1, 1.5), P(R2_C[0], 1.5), P(R2_C[0], R2_C[1] + SW_H / 2)]
COL = {"neg": FASE, "bla": NEUTRO, "ver": TIERRA}
OFF = {"neg": -0.045, "bla": 0.0, "ver": 0.045}


class Tomacorriente(TallerH):
    CARPETA_VOZ = "voz_e04"
    GUION = GUION

    def armar(self):
        self.pan = centro_carga()
        self.pan.nuestro[3][1].become(T("20", 8, "#101318", "HEAVY").scale_to_fit_width(self.pan.nuestro[3][0].width * 0.78).move_to(self.pan.nuestro[3][0]))
        self.var = varilla_tierra()
        self.c1 = caja_rect_en(R1_C)
        self.c2 = caja_rect_en(R2_C)
        self.t1 = tomacorriente(R1_C)
        self.t2 = tomacorriente(R2_C)
        self.tubos = VGroup(tubo(*TA), tubo(*TB))
        self.cons = VGroup(conector(E + P(0, 0.12), PI / 2), conector(P(XA1, TOP1 + 0.12), -PI / 2),
                           conector(P(XB1, TOP1 + 0.12), -PI / 2), conector(P(R2_C[0], R2_C[1] + SW_H / 2 + 0.12), -PI / 2))
        self.abr = VGroup(abrazadera(P(E[0], 1.75), True), abrazadera(P(-2.8, 2.0)), abrazadera(P(XA1, 1.2), True),
                          abrazadera(P(XB1, 1.0), True), abrazadera(P(2.2, 1.5)), abrazadera(P(R2_C[0], 0.6), True))
        self.piso = Line(P(-7.5, -3.3), P(7.5, -3.3), stroke_color="#D0D5DD", stroke_width=3)
        R = {}
        for k, o in OFF.items():
            R[k + "_ta"] = paralela(TA, o)
            R[k + "_tb"] = paralela(TB, o)
        R.update(rutas_tablero(self.pan, {k: R[k + "_ta"][0] for k in OFF}))
        c, t = R1_C, self.t1
        fa = {k: R[k + "_ta"][-1] for k in OFF}
        fb = {k: R[k + "_tb"][0] for k in OFF}
        self.nut_n, self.nut_b, self.nut_v = c + P(0.39, 0.5), c + P(-0.39, 0.5), c + P(-0.36, -0.52)
        R["neg_in"] = [fa["neg"], fa["neg"] + P(0, -0.15), self.nut_n + P(-0.06, 0.08)]
        R["neg_out"] = [fb["neg"], fb["neg"] + P(0, -0.1), self.nut_n + P(0.02, 0.09)]
        R["neg_cola"] = [self.nut_n + P(0, -0.06), self.nut_n + P(0.02, -0.18), t.l1.get_center() + P(0.12, 0.02), t.l1.get_center()]
        R["bla_in"] = [fa["bla"], fa["bla"] + P(0, -0.1), self.nut_b + P(0.04, 0.09)]
        R["bla_out"] = [fb["bla"], fb["bla"] + P(0, -0.18), self.nut_b + P(0.08, 0.08)]
        R["bla_cola"] = [self.nut_b + P(0, -0.06), self.nut_b + P(-0.02, -0.18), t.p1.get_center() + P(-0.12, 0.02), t.p1.get_center()]
        R["ver_in"] = [fa["ver"], P(c[0] - 0.47, c[1] + 0.35), self.nut_v + P(-0.06, 0.08)]
        R["ver_out"] = [fb["ver"], P(c[0] + 0.0, c[1] + 0.72), P(c[0] - 0.47, c[1] + 0.3), self.nut_v + P(-0.02, 0.09)]
        R["ver_cola"] = [self.nut_v + P(0.02, -0.06), t.verde.get_center() + P(-0.12, -0.04), t.verde.get_center()]
        R["ver_caja"] = [self.nut_v + P(0.04, -0.06), P(c[0] - 0.2, c[1] - 0.72), P(c[0] + 0.2, c[1] - 0.72), self.c1.tierra.get_center()]
        c2, t2 = R2_C, self.t2
        f2 = {k: R[k + "_tb"][-1] for k in OFF}
        self.nut_v2 = c2 + P(-0.36, -0.52)
        R["neg_2"] = [f2["neg"], f2["neg"] + P(0.35, -0.2), t2.l1.get_center() + P(0.14, 0.04), t2.l1.get_center()]
        R["bla_2"] = [f2["bla"], f2["bla"] + P(-0.32, -0.25), t2.p1.get_center() + P(-0.14, 0.04), t2.p1.get_center()]
        R["ver_2"] = [f2["ver"], P(c2[0] + 0.47, c2[1] + 0.3), P(c2[0] + 0.47, c2[1] - 0.2), self.nut_v2 + P(0.4, 0.05), self.nut_v2 + P(0.05, 0.06)]
        R["ver_2c"] = [self.nut_v2 + P(0.02, -0.06), t2.verde.get_center() + P(-0.12, -0.04), t2.verde.get_center()]
        R["ver_2k"] = [self.nut_v2 + P(0.04, -0.06), P(c2[0] - 0.2, c2[1] - 0.72), P(c2[0] + 0.2, c2[1] - 0.72), self.c2.tierra.get_center()]
        self.R = R
        self.cab = {}
        self.mundo = VGroup(self.piso, self.var, self.pan, self.tubos, self.c1, self.c2, self.t1, self.t2, self.cons, self.abr)

    GANCHO = {"neg_cola": 0.05, "bla_cola": 0.05, "ver_cola": 0.045, "ver_caja": 0.04, "neg_2": 0.05, "bla_2": 0.05,
              "ver_2c": 0.045, "ver_2k": 0.04, "neg_tab": 0, "bla_tab": 0, "ver_tab": 0}

    def c(self, k, w=2.6):
        if k not in self.cab:
            cb = cable(*self.R[k], color=COL[k[:3]], w=w)
            if k in self.GANCHO:
                cb.add(punta_pelada(cb.ruta, 0.07, w, self.GANCHO[k]))
            self.cab[k] = cb
        return self.cab[k]

    def tornillos_encima(self):
        self.bring_to_front(self.t1.l1, self.t1.p1, self.t1.verde, self.t2.l1, self.t2.p1, self.t2.verde, self.c1.tierra,
                            self.c2.tierra, self.pan.nuestro.terminal)

    def construct(self):
        self.armar()
        for paso in ("intro", "nema", "agujeros", "polarizada", "terminales", "tierra_para", "circuito", "veinte", "vatios",
                     "herramientas", "materiales", "recorrido", "cableado", "tablero", "colas", "conexion", "tierra_caja",
                     "segunda", "tr", "dividido", "placa", "prueba", "probador", "repaso", "caliente", "viejo", "errores"):
            getattr(self, "f_" + paso)()
        self.resumen_y_final("cierre", ["Ranura pequeña: fase → latón", "Ranura grande: neutro → plateado",
                                        "Redonda: tierra → verde y a la caja", "Neutro y tierra: solo se unen en el tablero"])

    # -------------------------------------------------------------- secciones
    def cara_grande(self, escala=4.0, tipo="5-15R"):
        cc = ORIGIN
        cara = RoundedRectangle(width=0.38, height=0.36, corner_radius=0.13, stroke_color="#C7C5BE", stroke_width=1.2).set_fill("#FBFBF9", 1)
        fase = RoundedRectangle(width=0.035, height=0.1, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(P(0.08, 0.04))
        neu = RoundedRectangle(width=0.035, height=0.13, corner_radius=0.012, stroke_width=0).set_fill("#2A2E35", 1).move_to(P(-0.08, 0.04))
        if tipo == "5-20R":
            neu = VGroup(neu, RoundedRectangle(width=0.07, height=0.03, corner_radius=0.01, stroke_width=0).set_fill("#2A2E35", 1).move_to(P(-0.1, 0.04)))
        tie = VGroup(Arc(radius=0.035, start_angle=PI, angle=PI, stroke_width=0).set_fill("#2A2E35", 1),
                     Rectangle(width=0.07, height=0.03, stroke_width=0).set_fill("#2A2E35", 1).shift(UP * 0.015)).move_to(P(0, -0.1))
        g = VGroup(cara, fase, neu, tie).scale(escala)
        g.fase, g.neu, g.tie = fase, neu, tie
        return g

    def f_intro(self):
        self.voz("intro")
        t = tomacorriente(P(0, 0)).scale(2.6).move_to([-4.3, 0.0, 0])
        pl = placa_toma(P(0, 0)).scale(2.6).move_to(t)
        self.play(FadeIn(pl, scale=0.9), run_time=0.6)
        tit = self.titulo("TOMACORRIENTE", "CON TIERRA", "NEMA 5-15 · del tablero a la placa")
        self.esperar_frac(0.25)
        q = VGroup(*[pastilla(x, MARCA, 26) for x in ("¿qué significa cada agujero?", "¿por qué uno es más grande?", "¿para qué el redondo?")])
        q.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(tit, DOWN, buff=0.35, aligned_edge=LEFT)
        for x in q:
            self.play(FadeIn(x, shift=UP * 0.15), run_time=0.4)
            self.wait(max(0.3, self.resta() * 0.12))
        self.cerrar_voz()
        self.play(FadeOut(pl), FadeIn(t), run_time=0.5)
        self.limpiar(t, tit, q)

    def f_nema(self):
        self.voz("nema")
        big = VGroup(T("NEMA", 70, TINTA, "HEAVY"), T("5", 110, MARCA, "HEAVY"), T("-", 90, TINTA2, "HEAVY"), T("15", 110, ENERGIA, "HEAVY"),
                     T("R", 110, "#7A5AF8", "HEAVY")).arrange(RIGHT, buff=0.25).move_to([0, 2.0, 0])
        self.play(FadeIn(big[:2]), run_time=0.5)
        e5 = VGroup(T("5 =", 34, MARCA, "HEAVY"), T("125 V con tierra", 32, TINTA, "BOLD")).arrange(RIGHT, buff=0.2).move_to([-3.8, -0.4, 0])
        self.play(FadeIn(e5, shift=UP * 0.2), run_time=0.4)
        self.esperar_frac(0.3)
        self.play(FadeIn(big[2:4]), run_time=0.4)
        e15 = VGroup(T("15 =", 34, ENERGIA, "HEAVY"), T("15 amperios", 32, TINTA, "BOLD")).arrange(RIGHT, buff=0.2).move_to([-3.8, -1.3, 0])
        self.play(FadeIn(e15, shift=UP * 0.2), run_time=0.4)
        self.esperar_frac(0.4)
        self.play(FadeIn(big[4]), run_time=0.4)
        r = VGroup(self.cara_grande(3.0), T("R = receptáculo", 26, "#7A5AF8", "BOLD")).arrange(DOWN, buff=0.2)
        p_ = VGroup(clavija().scale(0.9), T("P = clavija", 26, "#7A5AF8", "BOLD")).arrange(DOWN, buff=0.2)
        rp = VGroup(r, p_).arrange(RIGHT, buff=1.0).move_to([3.4, -1.1, 0])
        self.play(FadeIn(rp, shift=UP * 0.2), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(big, e5, e15, rp)

    def f_agujeros(self):
        self.voz("agujeros")
        cara = self.cara_grande(9.0).move_to([-3.4, 0.0, 0])
        self.play(FadeIn(cara, scale=0.9), run_time=0.6)
        info = [(cara.fase, "FASE · ranura pequeña", FASE, RIGHT), (cara.neu, "NEUTRO · ranura grande", "#475467", LEFT),
                (cara.tie, "TIERRA · redonda", TIERRA, DOWN)]
        etq = VGroup()
        for obj, txt, col, lado in info:
            p = pastilla(txt, col, 26, True)
            if lado is DOWN:
                p.next_to(obj, DOWN, buff=0.9)
            else:
                p.move_to(obj.get_center() + lado * 3.4 + UP * 1.3)
            ln = Line(obj.get_center(), p.get_center(), stroke_color=col, stroke_width=1.8)
            ln.put_start_and_end_on(obj.get_center(), p.get_edge_center(-lado if lado is not DOWN else UP))
            self.play(Indicate(obj, color=col), FadeIn(p), Create(ln), run_time=0.6)
            etq.add(ln, p)
            self.wait(max(0.2, self.resta() * 0.08))
        cl = clavija().scale(1.6).rotate(PI).move_to([4.2, 1.9, 0])
        self.play(FadeIn(cl, shift=DOWN * 0.3), run_time=0.5)
        anc = pastilla("pata ancha = neutro", "#475467", 24, True).next_to(cl, DOWN, buff=0.25)
        self.play(FadeIn(anc), Indicate(cl.neu_p), run_time=0.6)
        self.esperar_frac(0.35)
        larga = pastilla("tierra: más larga, conecta primero", TIERRA, 24, True).move_to([4.2, -1.6, 0])
        self.play(Indicate(cl.tie_p, color=TIERRA), FadeIn(larga), run_time=0.7)
        self.cerrar_voz()
        self.limpiar(cara, etq, cl, anc, larga)

    def f_polarizada(self):
        self.voz("polarizada")
        lam = portalampara_led(P(0, 0)).scale(2.2).move_to([3.6, 0.4, 0])
        cl = clavija().scale(1.2).move_to([-4.0, -0.6, 0])
        wn = cable(cl.neu_p.get_top() + UP * 0.1, P(-4.2, 2.4), P(1.4, 2.4), lam.plata.get_center(), color=NEUTRO, w=6)
        wf = cable(cl.fase_p.get_top() + UP * 0.1, P(-3.8, 2.0), P(5.6, 2.0), lam.laton.get_center(), color=FASE, w=6)
        self.play(FadeIn(cl), FadeIn(lam), run_time=0.5)
        self.play(Create(wn), Create(wf), run_time=1.0)
        n = pastilla("pata ancha (neutro) → rosca", "#475467", 26, True).move_to([0.2, -1.9, 0])
        self.play(FadeIn(n), Indicate(lam.plata), run_time=0.6)
        ref = pastilla("igual que en el video de la lámpara", MARCA, 22).move_to([0.2, -2.8, 0])
        self.play(FadeIn(ref), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(lam, cl, wn, wf, n, ref)

    def f_terminales(self):
        self.voz("terminales")
        t = tomacorriente(P(0, 0)).scale(3.3).move_to([-2.0, -0.2, 0])
        self.play(FadeIn(t, scale=0.9), run_time=0.5)
        info = [(t.l1, "LATÓN → fase (negro)", "#8A6D12", RIGHT), (t.p1, "PLATEADO → neutro (blanco)", "#475467", LEFT),
                (t.verde, "VERDE → tierra", TIERRA, DOWN)]
        etq = VGroup()
        for obj, txt, col, lado in info:
            p = pastilla(txt, col, 24, True)
            p.move_to(obj.get_center() + (lado * 3.0 if lado is not DOWN else DOWN * 0.9 + RIGHT * 2.6))
            if p.get_left()[0] < -7.6:
                p.shift(RIGHT * (-7.6 - p.get_left()[0]) + UP * 0.6)
            ln = Line(obj.get_center(), p.get_center(), stroke_color=col, stroke_width=1.6)
            self.play(FadeIn(p), Create(ln), run_time=0.5)
            etq.add(ln, p)
            self.wait(max(0.2, self.resta() * 0.12))
        carta = self.carta_nec("NEC 2020 · 200.10(B)", "El terminal del neutro se identifica\ncon metal blanco o plateado.", (4.4, 2.8), 5.4)
        self.play(FadeIn(carta), run_time=0.4)
        self.esperar_frac(0.4)
        pes = pastilla("pestaña: une los dos tornillos", AMBAR, 24, True).move_to([4.3, -2.6, 0])
        self.play(Indicate(t.pest_l, color=ENERGIA, scale_factor=1.3), FadeIn(pes), run_time=0.7)
        self.cerrar_voz()
        self.limpiar(t, etq, carta, pes)

    def electrodomestico(self):
        caja = RoundedRectangle(width=2.6, height=3.0, corner_radius=0.15, stroke_color=METAL_OSC, stroke_width=2).set_fill("#E4E7EC", 1)
        puerta = Circle(radius=0.8, stroke_color=METAL_OSC, stroke_width=2).set_fill("#B8D8E8", 1).shift(DOWN * 0.3)
        panel = Rectangle(width=2.6, height=0.5, stroke_width=0).set_fill("#D0D5DD", 1).move_to(caja.get_top() + DOWN * 0.25)
        perillas = VGroup(*[Circle(radius=0.1, stroke_color=LINEA, stroke_width=1).set_fill(WHITE, 1).move_to(panel.get_center() + RIGHT * x) for x in (-0.8, 0.8)])
        return VGroup(caja, panel, perillas, puerta)

    def f_tierra_para(self):
        self.voz("tierra_para")
        sin = self.electrodomestico().scale(0.9).move_to([-3.8, 0.0, 0])
        con = self.electrodomestico().scale(0.9).move_to([3.0, 0.0, 0])
        t1 = pastilla("SIN TIERRA", ROJO, 26, True).next_to(sin, UP, buff=0.3)
        t2 = pastilla("CON TIERRA", VERDE_OK, 26, True).next_to(con, UP, buff=0.3)
        div = DashedLine([-0.4, 2.6, 0], [-0.4, -3.0, 0], stroke_color=METAL2, stroke_width=1.5)
        self.play(FadeIn(sin), FadeIn(con), FadeIn(t1), FadeIn(t2), Create(div), run_time=0.7)
        self.esperar_frac(0.2)
        for ap in (sin, con):
            self.add(rayo(ap[0].get_corner(UR) + P(-0.6, -0.5), ap[0].get_corner(UR) + P(-0.15, -0.9), ENERGIA, 3, 0.04, 3, 3))
        self.sfx("pop", -6)
        en = VGroup(simbolo_rayo(ROJO, 0.5), T("carcasa energizada", 26, ROJO, "HEAVY")).arrange(RIGHT, buff=0.15).next_to(sin, DOWN, buff=0.3)
        self.play(FadeIn(en), run_time=0.4)
        self.esperar_frac(0.3)
        ruta = [con[0].get_corner(UR) + P(-0.2, -0.9), con[0].get_corner(DR) + P(0.4, 0.3), P(6.3, -2.6), P(6.3, -3.1)]
        tier = cable(*ruta, color=TIERRA, w=6)
        fl = corriente(ruta, vel=1.2, color="#E5484D", color2="#FFB3B5")
        self.play(Create(tier), run_time=0.5)
        self.add(fl)
        br = breaker("20", 0.46, 0.26).scale(2.2).move_to([5.0, -2.7, 0])
        self.play(FadeIn(br), run_time=0.3)
        self.esperar_frac(0.3)
        self.sfx("tic", -2)
        self.play(mover_palanca(br, False), run_time=0.2)
        di = pastilla("el breaker se dispara", VERDE_OK, 24, True).next_to(br, LEFT, buff=0.3)
        self.play(FadeIn(di), run_time=0.3)
        self.cerrar_voz()
        fl.clear_updaters()
        self.limpiar_todo()

    def f_circuito(self):
        self.voz("circuito")
        br = breaker("20", 0.46, 0.26).scale(3.0).move_to([-4.8, 1.8, 0])
        ca = cable_hilos(3.0, FASE, 0.5, 0.7).move_to([-1.6, 1.8, 0])
        et = T("cable 12 AWG cobre", 26, TINTA, "BOLD").next_to(ca, DOWN, buff=0.2)
        self.play(FadeIn(br), FadeIn(ca), FadeIn(et), run_time=0.6)
        carta = self.carta_nec("NEC 2020 · 240.4(D)", "Cobre 12 AWG → protección\nmáxima de 20 A.", (4.6, 2.5), 5.0)
        self.play(FadeIn(carta), run_time=0.4)
        self.esperar_frac(0.25)
        a = VGroup(tarjeta(5.6, 2.6, METAL), T("2 o más tomacorrientes", 26, TINTA, "HEAVY"), T("de 15 A en circuito de 20 A", 24, TINTA2, "MEDIUM"),
                   check(VERDE_OK, 0.3))
        a[1:3].arrange(DOWN, buff=0.12).move_to(a[0].get_center() + UP * 0.35)
        a[3].move_to(a[0].get_center() + DOWN * 0.75)
        b = VGroup(tarjeta(5.6, 2.6, METAL), T("1 solo tomacorriente", 26, TINTA, "HEAVY"), T("en circuito exclusivo de 20 A", 24, TINTA2, "MEDIUM"),
                   T("debe ser de 20 A", 30, ENERGIA, "HEAVY"))
        b[1:3].arrange(DOWN, buff=0.12).move_to(b[0].get_center() + UP * 0.35)
        b[3].move_to(b[0].get_center() + DOWN * 0.75)
        VGroup(a, b).arrange(RIGHT, buff=0.5).move_to([0, -1.6, 0])
        self.play(FadeIn(a, shift=UP * 0.2), run_time=0.5)
        self.esperar_frac(0.4)
        self.play(FadeIn(b, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(br, ca, et, carta, a, b)

    def f_veinte(self):
        self.voz("veinte")
        c15 = self.cara_grande(6.0).move_to([-3.4, 0.4, 0])
        c20 = self.cara_grande(6.0, "5-20R").move_to([3.4, 0.4, 0])
        e15 = T("5-15R", 34, TINTA, "HEAVY").next_to(c15, DOWN, buff=0.3)
        e20 = T("5-20R", 34, ENERGIA, "HEAVY").next_to(c20, DOWN, buff=0.3)
        self.play(FadeIn(c15), FadeIn(e15), run_time=0.5)
        self.play(FadeIn(c20), FadeIn(e20), run_time=0.5)
        t = pastilla("neutro en forma de T", ENERGIA, 26, True).next_to(e20, DOWN, buff=0.25)
        self.play(Indicate(c20.neu, color=ENERGIA), FadeIn(t), run_time=0.7)
        self.esperar_frac(0.4)
        no = VGroup(T("clavija de 20 A en uno de 15 A:", 26, TINTA, "BOLD"), T("NO entra", 30, ROJO, "HEAVY")).arrange(RIGHT, buff=0.2).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(no), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(c15, c20, e15, e20, t, no)

    def f_vatios(self):
        self.voz("vatios")
        f = MathTex(r"P = V \cdot I = 120\,\mathrm{V} \times 15\,\mathrm{A}", color=TINTA).scale(1.3).move_to([0, 2.6, 0])
        r = VGroup(display("1800", "W", ENERGIA, 100)).move_to([0, 1.0, 0])
        self.play(Write(f), run_time=1.0)
        self.play(FadeIn(r, scale=1.1), run_time=0.5)
        self.esperar_frac(0.3)
        reg = regleta().scale(1.2).move_to([-2.6, -1.8, 0])
        h, pl = hervidor().scale(0.8).move_to([2.2, -1.5, 0]), plancha().scale(0.8).move_to([4.8, -1.6, 0])
        self.play(FadeIn(reg), FadeIn(h), FadeIn(pl), run_time=0.6)
        av = pastilla("¡te pasas fácilmente!", ROJO, 26, True).move_to([0.5, -3.3, 0])
        self.play(FadeIn(av, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(f, r, reg, h, pl, av)

    def f_herramientas(self):
        self.voz("herramientas")
        def desarmador(punta_cruz=False):
            d = destornillador(1.6).rotate(-PI / 4)
            return d
        items = [(lambda: desarmador(), "Desarmador plano"), (lambda: desarmador(True), "Desarmador de estrella"),
                 (lambda: pinza_icono(True), "Pelacables"),
                 (lambda: multimetro().scale(0.5), "Multímetro"), (lambda: probador(), "Probador de voltaje"),
                 (lambda: pinza_icono(False), "Pinza")]
        g = self.tarjetas(items, "HERRAMIENTAS", 2, 3, 3.6, 2.9)
        self.cerrar_voz()
        self.limpiar(g)

    def f_materiales(self):
        self.voz("materiales")
        items = [
            (lambda: breaker("20", 0.46, 0.26).scale(3.2), "Breaker 1 polo · 20 A"),
            (lambda: VGroup(tubo(P(-1.0, 0), P(0.6, 0), d=0.22), conector(P(0.78, 0), 0, 0.22), abrazadera(P(-0.4, 0), d=0.22)), "Tubo EMT ½\"\nconectores y abrazaderas"),
            (lambda: VGroup(caja_rect_en(P(-0.7, 0)), caja_rect_en(P(0.7, 0))), "2 cajas rectangulares"),
            (lambda: VGroup(tomacorriente(P(-0.45, 0)), tomacorriente(P(0.45, 0))), "2 tomacorrientes\ndúplex con tierra"),
            (lambda: VGroup(placa_toma(P(-0.5, 0)), placa_toma(P(0.5, 0))), "2 placas"),
            (lambda: VGroup(tuerca_empalme(P(-0.35, 0), AMBAR, 0.45), tuerca_empalme(P(0.35, 0), TIERRA, 0.45)), "Conectores\nde empalme"),
            (lambda: VGroup(cable_hilos(2.0, FASE, 0.4, 0.6).shift(UP * 0.5), cable_hilos(2.0, NEUTRO, 0.4, 0.6), cable_hilos(2.0, TIERRA, 0.4, 0.6).shift(DOWN * 0.5)),
             "Cable THHN 12 AWG\nnegro · blanco · verde"),
            (lambda: probador_tomas(), "Probador de\ntomacorrientes"),
        ]
        g = self.tarjetas(items)
        self.cerrar_voz()
        self.limpiar(g)

    def f_recorrido(self):
        self.voz("recorrido")
        self.camera.frame.set(width=16).move_to(P(0, -0.2))
        self.play(FadeIn(self.piso), FadeIn(self.var), FadeIn(self.pan), run_time=0.6)
        self.play(Create(self.tubos[0]), FadeIn(self.c1), FadeIn(self.t1), run_time=1.0)
        e1 = pastilla("Caja 1", TINTA, 24).move_to(R1_C + P(0, -1.2))
        self.play(FadeIn(e1), run_time=0.3)
        self.esperar_frac(0.35)
        self.play(Create(self.tubos[1]), FadeIn(self.c2), FadeIn(self.t2), run_time=1.0)
        e2 = pastilla("Caja 2", TINTA, 24).move_to(R2_C + P(0, -1.2))
        self.play(FadeIn(e2), FadeIn(self.cons), FadeIn(self.abr), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(e1, e2)

    def f_cableado(self):
        self.voz("cableado")
        self.play(self.tubos.animate.set_stroke(opacity=0.28), run_time=0.4)
        for k, gr in enumerate((["neg_ta", "bla_ta", "ver_ta"], ["neg_tb", "bla_tb", "ver_tb"])):
            ws = [self.c(x, 2.2) for x in gr]
            self.play(*[Create(w) for w in ws], run_time=1.3)
            self.mundo.add(*ws)
            self.esperar_frac(0.3)
        self.play(self.tubos.animate.set_stroke(opacity=1), run_time=0.4)
        self.bring_to_front(self.tubos, self.cons, self.abr)
        carta = pastilla("deja ≥ 15 cm de cable libre en cada caja", MARCA, 26, True).move_to([-1.5, -3.0, 0])
        self.play(FadeIn(carta), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(carta)

    def f_tablero(self):
        self.voz("tablero")
        self.ir(P(-3.9, -0.45), 7.6, 1.0)
        etq = VGroup()
        for k, (cl, txt, col) in enumerate((("neg_tab", "negro → breaker 20 A", FASE), ("bla_tab", "blanco → barra de neutros", "#475467"),
                                            ("ver_tab", "verde → barra de tierra", TIERRA))):
            w = self.c(cl)
            e = self.chip(txt, P(-2.45, 0.2 - 0.5 * k), col, 20, True)
            self.play(Create(w), FadeIn(e), run_time=0.8)
            self.mundo.add(w)
            etq.add(e)
        self.tornillos_encima()
        self.apretar(self.pan.nuestro.terminal, 0.8)
        self.cerrar_voz()
        self.limpiar(etq)

    def f_colas(self):
        self.voz("colas")
        self.ir(R1_C + P(1.0, 0.0), 4.4, 1.0)
        nin, nout = self.c("neg_in"), self.c("neg_out")
        self.play(Create(nin), Create(nout), run_time=0.7)
        n1 = tuerca_empalme(self.nut_n, AMBAR, 0.14)
        cola_n = self.c("neg_cola")
        self.play(FadeIn(n1), Create(cola_n), run_time=0.7)
        e = pastilla("cola", MARCA, 22, True)
        self.pant(e, (4.2, 1.6))
        ln = Line(e.get_left(), cola_n.ruta.point_from_proportion(0.5), stroke_color=MARCA, stroke_width=1.5)
        self.play(FadeIn(e), Create(ln), run_time=0.4)
        self.esperar_frac(0.25)
        bin_, bout = self.c("bla_in"), self.c("bla_out")
        n2 = tuerca_empalme(self.nut_b, AMBAR, 0.14)
        self.play(Create(bin_), Create(bout), run_time=0.6)
        self.play(FadeIn(n2), Create(self.c("bla_cola")), run_time=0.6)
        self.esperar_frac(0.2)
        vin, vout = self.c("ver_in"), self.c("ver_out")
        n3 = tuerca_empalme(self.nut_v, TIERRA, 0.13)
        self.play(Create(vin), Create(vout), run_time=0.6)
        self.play(FadeIn(n3), Create(self.c("ver_cola")), run_time=0.6)
        ventaja = pastilla("si uno falla, el siguiente sigue funcionando", VERDE_OK, 22, True)
        self.pant(ventaja, (3.2, -2.9))
        self.play(FadeIn(ventaja), run_time=0.4)
        self.mundo.add(nin, nout, n1, cola_n, bin_, bout, n2, self.c("bla_cola"), vin, vout, n3, self.c("ver_cola"))
        self.tornillos_encima()
        self.cerrar_voz()
        self.limpiar(e, ln, ventaja)

    def f_conexion(self):
        self.voz("conexion")
        cx = np.array([-3.4, 0.3, 0])
        lupa = Circle(radius=1.9, stroke_color=TINTA2, stroke_width=2).set_fill(WHITE, 1).move_to(cx)
        tor = tornillo(0.5, LATON, 0.5).move_to(cx)
        gancho = VMobject().set_points_smoothly([cx + P(-1.9, -0.9), cx + P(-1.0, -0.7), cx + P(-0.6, -0.25), cx + P(-0.52, 0.25),
                                                 cx + P(0, 0.58), cx + P(0.52, 0.28), cx + P(0.56, -0.15)])
        g1 = gancho.copy().set_stroke(_osc(COBRE, 0.4), 22)
        g2 = gancho.copy().set_stroke(COBRE, 16)
        espiral = VGroup(*[Line(gancho.point_from_proportion(t) + P(-0.07, -0.07), gancho.point_from_proportion(t) + P(0.07, 0.07),
                                stroke_color=_osc(COBRE, 0.45), stroke_width=2) for t in np.linspace(0.05, 0.95, 14)])
        flecha = CurvedArrow(cx + P(-0.85, 0.7), cx + P(0.9, 0.55), angle=-1.2, color=MARCA, stroke_width=4, tip_length=0.22)
        tx = pastilla("hilos torcidos · sentido del reloj ↻", MARCA, 22, True).next_to(lupa, DOWN, buff=0.3)
        lp = VGroup(lupa, g1, g2, espiral, tor, flecha, tx)
        self.pant(lp, (-3.4, 0.3))
        self.play(FadeIn(lp[0]), FadeIn(lp[4]), run_time=0.4)
        self.play(Create(lp[1]), Create(lp[2]), FadeIn(lp[3]), run_time=0.9)
        self.play(Create(lp[5]), FadeIn(lp[6]), run_time=0.5)
        self.esperar_frac(0.2)
        etq = VGroup(*[pastilla(t, c_, 20, True) for t, c_ in (("negro → latón", FASE), ("blanco → plateado", "#475467"), ("verde → verde", TIERRA))])
        etq.arrange(DOWN, buff=0.15)
        self.pant(etq, (4.6, 2.2))
        for k, (e, t) in enumerate(zip(etq, (self.t1.l1, self.t1.p1, self.t1.verde))):
            self.play(FadeIn(e), Indicate(t, scale_factor=1.6), run_time=0.6)
            self.wait(max(0.2, self.resta() * 0.15))
        self.apretar(self.t1.l1, 0.7)
        self.cerrar_voz()
        self.limpiar(lp, etq)

    def f_tierra_caja(self):
        self.voz("tierra_caja")
        vc = self.c("ver_caja")
        self.play(Create(vc), Indicate(self.c1.tierra, color=TIERRA, scale_factor=1.6), run_time=0.8)
        self.mundo.add(vc)
        self.tornillos_encima()
        e = pastilla("cola verde → caja metálica", TIERRA, 22, True)
        self.pant(e, (3.6, -2.8))
        self.play(FadeIn(e), run_time=0.4)
        self.esperar_frac(0.3)
        fl = corriente(concatenar(self.R["ver_caja"][::-1][1:], self.R["ver_in"][::-1], inv(self.R["ver_ta"]), self.R["ver_tab"]),
                       vel=0.9, color="#E5484D", color2="#FFB3B5", escala=self.z * 2.2)
        self.add(fl)
        self.cerrar_voz()
        fl.clear_updaters()
        self.limpiar(e, fl)

    def f_segunda(self):
        self.voz("segunda")
        self.ir(R2_C + P(-0.9, 0.0), 4.4, 1.0)
        etq = VGroup()
        for k, (cl, txt, col) in enumerate((("neg_2", "negro → latón", FASE), ("bla_2", "blanco → plateado", "#475467"),
                                            ("ver_2", "verde → empalme", TIERRA))):
            w = self.c(cl)
            e = pastilla(txt, col, 20, True)
            self.pant(e, (-4.4, 2.0 - 0.75 * k))
            self.play(Create(w), FadeIn(e), run_time=0.6)
            self.mundo.add(w)
            etq.add(e)
        n = tuerca_empalme(self.nut_v2, TIERRA, 0.13)
        w2, w3 = self.c("ver_2c"), self.c("ver_2k")
        self.play(FadeIn(n), Create(w2), Create(w3), run_time=0.8)
        self.mundo.add(n, w2, w3)
        self.tornillos_encima()
        self.cerrar_voz()
        self.limpiar(etq)

    def f_tr(self):
        self.voz("tr")
        resto = [m for m in self.mobjects[1:] if m is not self.camera.frame]
        for m in resto:
            m.clear_updaters()
        self.ir(ORIGIN, 16, 0.5, *[FadeOut(m) for m in resto])
        cara = self.cara_grande(8.0).move_to([-3.4, 0.2, 0])
        pers = VGroup(*[Rectangle(width=0.45, height=1.2, stroke_color="#98A2B3", stroke_width=1.2).set_fill("#E4E7EC", 1).move_to(r.get_center())
                        for r in (cara.fase, cara.neu)])
        tr = T("TR", 40, "#98A2B3", "HEAVY").move_to(cara.get_corner(UR) + P(-0.6, -0.5))
        self.play(FadeIn(cara), FadeIn(pers), FadeIn(tr), run_time=0.6)
        carta = self.carta_nec("NEC 2020 · 406.12", "En viviendas: tomacorrientes a prueba\nde manipulación (TR).", (4.0, 2.4), 5.6)
        self.play(FadeIn(carta), run_time=0.4)
        self.esperar_frac(0.35)
        llave = VGroup(RoundedRectangle(width=0.18, height=1.4, corner_radius=0.05, stroke_color=LINEA, stroke_width=1).set_fill(METAL, 1)).move_to(cara.fase.get_center() + UP * 1.6)
        self.play(FadeIn(llave), llave.animate.shift(DOWN * 0.8), run_time=0.6)
        no = pastilla("un solo objeto: no entra", ROJO, 24, True).move_to([3.6, -0.3, 0])
        self.play(FadeIn(no), run_time=0.3)
        self.play(FadeOut(llave), run_time=0.2)
        self.esperar_frac(0.3)
        cl = clavija().scale(2.6).rotate(PI).move_to(cara.get_center() + UP * 3.4)
        self.play(FadeIn(cl), cl.animate.shift(DOWN * 1.2), pers.animate.set_opacity(0.15), run_time=0.8)
        si = pastilla("dos patas a la vez: se abre", VERDE_OK, 24, True).move_to([3.6, -1.2, 0])
        self.play(FadeIn(si), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(cara, pers, tr, carta, no, cl, si)

    def f_dividido(self):
        self.voz("dividido")
        t = tomacorriente(P(0, 0)).scale(3.2).move_to([-2.4, -0.2, 0])
        self.play(FadeIn(t), run_time=0.4)
        pin = VGroup(Line(P(0.8, 1.2), P(-0.2, 0.0)).set_stroke("#B42318", 12), Line(P(0.8, -1.2), P(-0.2, 0.0)).set_stroke("#B42318", 12)).scale(0.8)
        pin.next_to(t.pest_l, RIGHT, buff=0.05)
        self.play(FadeIn(pin, shift=LEFT * 0.3), run_time=0.5)
        self.sfx("tic", -4)
        self.play(FadeOut(t.pest_l, shift=RIGHT * 0.4), FadeOut(pin, shift=RIGHT * 0.4), run_time=0.5)
        txt = VGroup(T("cada mitad independiente", 30, TINTA, "HEAVY"), T("rompe solo la pestaña de LATÓN", 26, ENERGIA, "BOLD"),
                     T("la plateada se queda", 24, TINTA2, "MEDIUM")).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([3.6, 0.2, 0])
        self.play(FadeIn(txt, shift=RIGHT * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(t, txt)

    def f_placa(self):
        self.voz("placa")
        self.camera.frame.set(width=16).move_to(P(0, -0.2))
        self.play(FadeIn(self.mundo), *[FadeIn(w) for w in self.cab.values()], run_time=0.6)
        self.pl1, self.pl2 = placa_toma(R1_C), placa_toma(R2_C)
        self.esperar_frac(0.3)
        self.play(FadeIn(self.pl1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(self.pl2, shift=UP * 0.1), run_time=0.5)
        self.esperar_frac(0.5)
        self.sfx("tic", -4)
        self.play(mover_palanca(self.pan.nuestro, True), run_time=0.3)
        self.mundo.add(self.pl1, self.pl2)
        self.cerrar_voz()

    def f_prueba(self):
        self.voz("prueba")
        self.ir(R1_C + P(1.8, 0.4), 6.4, 0.8)
        mm = multimetro()
        self.pant(mm, (4.8, -0.2))
        self.play(FadeIn(mm), run_time=0.4)
        cara = self.pl1[1][:4]
        fase_r, neu_r, tie_r = self.pl1[1][1], self.pl1[1][2], self.pl1[1][3]
        roja, negra = punta_prueba(ROJO).scale(self.z * 0.9), punta_prueba("#2A2E35").scale(self.z * 0.9)
        roja.move_to(R1_C + P(1.4, 1.4))
        negra.move_to(R1_C + P(-1.0, 1.4))

        def tocar(a, b):
            return [roja.animate.shift(a.get_center() - roja.tip.get_bottom()), negra.animate.shift(b.get_center() - negra.tip.get_bottom())]

        def lect(txt, col):
            return T(txt, 40, col, "HEAVY", MONO).scale_to_fit_height(0.3 * self.z).move_to(mm.lcd)
        self.play(FadeIn(roja), FadeIn(negra), run_time=0.3)
        pruebas = [(fase_r, neu_r, "120 V", "fase – neutro ≈ 120 V"), (fase_r, tie_r, "120 V", "fase – tierra ≈ 120 V"),
                   (neu_r, tie_r, "0 V", "neutro – tierra ≈ 0 V")]
        l = None
        etq = VGroup()
        for k, (a, b, val, txt) in enumerate(pruebas):
            self.play(*tocar(a, b), run_time=0.6)
            nl = lect(val, "#1D2939")
            e = pastilla(txt, VERDE_OK, 22, True)
            self.pant(e, (-4.4, 2.0 - 0.8 * k))
            self.play(FadeIn(e), (Transform(l, nl) if l is not None else FadeIn(nl)), run_time=0.4)
            if l is None:
                l = nl
            etq.add(e)
            self.wait(max(0.3, self.resta() * 0.25))
        self.cerrar_voz()
        self.limpiar(mm, roja, negra, l, etq)

    def f_probador(self):
        self.voz("probador")
        p = probador_tomas()
        self.pant(p, (0.0, 0.0))
        p.move_to(R1_C + P(0, 0.3 + 0.24) + UP * 0.9)
        self.play(FadeIn(p), p.animate.shift(DOWN * 0.8), run_time=0.6)
        self.play(p.luces[1].animate.set_fill(AMBAR), p.luces[2].animate.set_fill(AMBAR), run_time=0.4)
        tabla = VGroup(*[VGroup(VGroup(*[Circle(radius=0.12, stroke_color=LINEA, stroke_width=1).set_fill(c_, 1) for c_ in cs]).arrange(RIGHT, buff=0.12),
                                T(t, 22, TINTA, "BOLD")).arrange(RIGHT, buff=0.35) for cs, t in
                         (((METAL, AMBAR, AMBAR), "correcto"), ((METAL, AMBAR, METAL), "falta la tierra"), ((METAL, METAL, METAL), "falta el neutro o la fase"),
                          ((ROJO, AMBAR, METAL), "fase y neutro invertidos"))]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        fondo_ = tarjeta(tabla.width + 0.6, tabla.height + 0.6, METAL).move_to(tabla)
        g = VGroup(fondo_, tabla)
        self.pant(g, (4.4, -0.6))
        self.play(FadeIn(g), run_time=0.5)
        nota = pastilla("ejemplo: revisa la tabla de TU probador", TINTA2, 20)
        self.pant(nota, (4.4, -3.2))
        self.play(FadeIn(nota), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(p, g, nota)

    def f_caliente(self):
        self.voz("caliente")
        resto = [m for m in self.mobjects[1:] if m is not self.camera.frame]
        for m in resto:
            m.clear_updaters()
        self.ir(ORIGIN, 16, 0.5, *[FadeOut(m) for m in resto])
        t = placa_toma(P(0, 0)).scale(3.0).move_to([-3.4, 0.0, 0])
        manchas = VGroup(*[Ellipse(width=w, height=h, stroke_width=0).set_fill("#6B4F3A", 0.55).move_to(t.get_center() + p)
                           for w, h, p in ((0.7, 0.4, P(0.4, 0.95)), (0.5, 0.3, P(0.25, 0.75)), (0.4, 0.25, P(0.55, -0.4)))])
        humo = VGroup(*[VMobject().set_points_smoothly([P(x, 1.6), P(x + 0.15, 2.0), P(x - 0.1, 2.4), P(x + 0.1, 2.8)]).set_stroke("#98A2B3", 4, 0.7)
                        for x in (-3.3, -2.9)])
        self.play(FadeIn(t), FadeIn(manchas), Create(humo), run_time=0.7)
        pasos = VGroup(*[pastilla(x, c_, 26, True) for x, c_ in (("1 · baja el breaker", ROJO), ("2 · revisa los tornillos", MARCA),
                                                                   ("3 · reaprieta o cambia", VERDE_OK))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.2, 0, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in pasos], lag_ratio=0.5), run_time=1.4)
        self.cerrar_voz()
        self.limpiar(t, manchas, humo, pasos)

    def f_repaso(self):
        self.voz("repaso")
        self.ir(P(0, -0.2), 16, 0.6)
        R = self.R
        fase = concatenar(inv(R["neg_tab"]), R["neg_ta"], R["neg_in"], R["neg_cola"])
        fase2 = concatenar(R["neg_out"][::-1], R["neg_tb"], R["neg_2"])
        pasos = [("del tablero: circuito de 20 A", FASE, [fase], [self.pan.nuestro], 0.18),
                 ("caja 1: colas de fase, neutro y tierra", MARCA, [fase], [self.c1], 0.3),
                 ("caja 2: conexión directa", MARCA, [fase2], [self.c2], 0.25),
                 ("la tierra llega también al metal de la caja", TIERRA, [], [self.c1.tierra, self.c2.tierra], 0.9)]
        prev = []
        for k, (txt, col, rutas, foco_, f) in enumerate(pasos):
            e = pastilla(txt, col, 26, True).move_to([1.5, 3.3, 0])
            fls = [corriente(r_, vel=0.9) for r_ in rutas]
            marcos = [SurroundingRectangle(m, buff=0.12, color=col, stroke_width=3) for m in foco_]
            self.play(*[FadeOut(m) for m in prev], FadeIn(e, shift=DOWN * 0.15), *[Create(m) for m in marcos], run_time=0.5)
            self.add(*fls)
            prev = [e, *fls, *marcos]
            self.esperar_frac(f)
        self.cerrar_voz()
        self.limpiar(*prev)

    def f_viejo(self):
        self.voz("viejo")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        viejo = self.cara_grande(7.0)
        viejo.remove(viejo.tie)
        viejo.move_to([-4.6, 0.6, 0])
        et = T("viejo: 2 agujeros", 28, TINTA, "HEAVY").next_to(viejo, DOWN, buff=0.3)
        self.play(FadeIn(viejo, scale=0.9), FadeIn(et), run_time=0.6)
        self.esperar_frac(0.15)
        nuevo = self.cara_grande(7.0).move_to(viejo)
        sinc = VGroup(Circle(radius=0.32, stroke_color=ROJO, stroke_width=5).move_to(nuevo.tie), T("sin conectar", 24, ROJO, "HEAVY").next_to(nuevo, DOWN, buff=0.3))
        x = equis(ROJO, 0.45).next_to(nuevo, UR, buff=-0.2)
        self.play(FadeOut(et), Transform(viejo, nuevo), run_time=0.5)
        self.play(Create(sinc[0]), FadeIn(sinc[1]), FadeIn(x, scale=1.3), run_time=0.5)
        self.esperar_frac(0.3)
        op1 = self.cara_grande(3.2)
        op1.remove(op1.tie)
        gf = self.cara_grande(2.9)
        botones = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.24, corner_radius=0.06, stroke_color="#C7C5BE", stroke_width=1.2).set_fill(c_, 1),
                                  T(t_, 13, WHITE if c_ != "#FBFBF9" else TINTA, "HEAVY")) for t_, c_ in (("TEST", "#2A2E35"), ("RESET", "#FBFBF9"))]).arrange(RIGHT, buff=0.12)
        for b_ in botones:
            b_[1].move_to(b_[0])
        op2 = VGroup(gf, botones.next_to(gf, DOWN, buff=0.12))
        cartas = VGroup()
        for il, t1, t2 in ((op1, "Otro sin tierra", "de 2 agujeros"), (op2, "Con protección GFCI", "marcado: \"No Equipment Ground\"")):
            caja = tarjeta(4.4, 3.9, METAL)
            il.move_to(caja.get_center() + UP * 0.45)
            a = T(t1, 26, TINTA, "HEAVY").move_to(caja.get_center() + DOWN * 1.15)
            b = T(t2, 21, TINTA2, "MEDIUM").next_to(a, DOWN, buff=0.12)
            cartas.add(VGroup(caja, il, a, b))
        cartas.arrange(RIGHT, buff=0.35).move_to([2.6, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cartas], lag_ratio=0.6), run_time=1.2)
        carta = self.carta_nec("NEC 2020 · 406.4(D)(2)", "Reemplazos donde no hay tierra de equipos:\nhay opciones permitidas (ver el código).", (2.6, -3.0), 7.0)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(viejo, sinc, x, cartas, carta)

    def f_errores(self):
        self.voz("errores")
        i1 = VGroup(self.cara_grande(2.5), T("F ↔ N", 30, ROJO, "HEAVY")).arrange(DOWN, buff=0.2)
        i2 = VGroup(tomacorriente(P(0, 0)).scale(1.3), Circle(radius=0.3, stroke_color=ROJO, stroke_width=4))
        i2[1].move_to(i2[0].verde)
        i3 = VGroup(cable(P(-1.2, 0.4), P(1.2, 0.4), color=NEUTRO, w=8), cable(P(-1.2, -0.4), P(1.2, -0.4), color=TIERRA, w=8),
                    Line(P(0, 0.4), P(0, -0.4)).set_stroke(ROJO, 8), equis(ROJO, 0.3).move_to(P(0.8, 0)))
        self.tres_errores([("1", "Invertir fase\ny neutro", "partes que deberían estar\nsin tensión quedan energizadas"),
                           ("2", "Dejar la tierra\nsin conectar", "todo funciona…\nhasta que hay una falla"),
                           ("3", "Puente neutro–tierra\nen el tomacorriente", "prohibido: solo se unen\nen el tablero principal")], [i1, i2, i3])

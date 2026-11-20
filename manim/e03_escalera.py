"""E03 · Apagador de escalera (3 vías). Guion y fuentes en e03_guion.py."""
from taller import *
from comun_e import _osc, _cla
from e03_guion import GUION

# ------------------------------------------------------------------ geometría del mundo
S1_C = P(-2.2, -0.9)
S2_C = P(5.3, 0.6)
O_C = P(1.0, 2.75)
O_R = OCT_R
LAMP_T = O_C[1] - O_R * np.cos(PI / 8)
XA, XB = S1_C[0] - 0.25, S1_C[0] + 0.25
TA = [E, P(E[0], 2.0), P(XA, 2.0), P(XA, S1_C[1] + SW_H / 2)]
TB = [P(XB, S1_C[1] + SW_H / 2), P(XB, O_C[1]), O_C + P(-O_R, 0)]
TC = [O_C + P(O_R, 0), P(S2_C[0], O_C[1]), P(S2_C[0], S2_C[1] + SW_H / 2)]
COL = {"neg": FASE, "bla": NEUTRO, "ver": TIERRA, "roj": VIAJERO_1, "ama": VIAJERO_2, "azu": RET_AZUL}
OFF_A = {"neg": -0.045, "bla": 0.0, "ver": 0.045}
OFF_B = {"roj": 0.06, "ama": 0.02, "bla": -0.02, "ver": -0.06}
OFF_C = {"roj": 0.06, "ama": 0.02, "azu": -0.02, "ver": -0.06}


def escalera_fondo():
    g = VGroup()
    x, y = -1.2, -3.9
    for k in range(9):
        g.add(Line(P(x, y), P(x, y + 0.42)), Line(P(x, y + 0.42), P(x + 0.62, y + 0.42)))
        x, y = x + 0.62, y + 0.42
    g.set_stroke("#D0D5DD", 3)
    baranda = Line(P(-1.2, -2.9), P(4.4, 0.9)).set_stroke("#D0D5DD", 3)
    piso = VGroup(Line(P(-6.9, -3.9), P(-1.2, -3.9)), Line(P(4.38, -0.12), P(7.5, -0.12))).set_stroke("#D0D5DD", 3)
    return VGroup(g, baranda, piso)


class Escalera(TallerH):
    CARPETA_VOZ = "voz_e03"
    GUION = GUION

    # -------------------------------------------------------------- mundo
    def armar(self):
        self.pan = centro_carga()
        self.var = varilla_tierra()
        self.fondo_esc = escalera_fondo()
        self.c1 = caja_rect_en(S1_C)
        self.c2 = caja_rect_en(S2_C)
        self.sw1 = interruptor3(S1_C + P(-0.08, 0), 1)
        self.sw2 = interruptor3(S2_C + P(-0.08, 0), 1)
        self.oc = caja_octagonal().shift(O_C - OCT_C)
        self.oc.tierra = self.oc[-1]
        self.port = portalampara_led(P(O_C[0], LAMP_T))
        self.tubos = VGroup(tubo(*TA), tubo(*TB), tubo(*TC))
        self.cons = VGroup(conector(E + P(0, 0.12), PI / 2), conector(P(XA, S1_C[1] + SW_H / 2 + 0.12), -PI / 2),
                           conector(P(XB, S1_C[1] + SW_H / 2 + 0.12), -PI / 2), conector(O_C + P(-O_R - 0.1, 0), 0),
                           conector(O_C + P(O_R + 0.1, 0), PI), conector(P(S2_C[0], S2_C[1] + SW_H / 2 + 0.12), -PI / 2))
        self.abr = VGroup(abrazadera(P(E[0], 1.75), True), abrazadera(P(-3.5, 2.0)), abrazadera(P(XB, 1.3), True),
                          abrazadera(P(-0.5, O_C[1])), abrazadera(P(3.2, O_C[1])), abrazadera(P(S2_C[0], 2.0), True))
        self.rutas()
        self.cab = {}
        self.mundo = VGroup(self.fondo_esc, self.var, self.pan, self.tubos, self.c1, self.c2, self.sw1, self.sw2, self.oc,
                            self.port, self.cons, self.abr)

    def rutas(self):
        R = {}
        for k, o in OFF_A.items():
            R[k + "_ta"] = paralela(TA, o)
        for k, o in OFF_B.items():
            R[k + "_tb"] = paralela(TB, o)
        for k, o in OFF_C.items():
            R[k + "_tc"] = paralela(TC, o)
        b = self.pan.nuestro.terminal.get_center()
        tn = self.pan.tn[1].get_center()
        tt = self.pan.tt[-2].get_center()
        ea = {k: R[k + "_ta"][0] for k in OFF_A}
        R["neg_tab"] = [ea["neg"], P(ea["neg"][0], b[1] + 0.25), b + P(0.12, 0.05), b]
        R["bla_tab"] = [ea["bla"], P(ea["bla"][0], tn[1] + 0.25), P(NEU_X + 0.15, tn[1] + 0.1), tn]
        R["ver_tab"] = [ea["ver"], P(E[0] + 0.3, E[1] - 0.3), P(E[0] + 0.3, tt[1] + 0.25), P(tt[0] + 0.2, tt[1] + 0.12), tt]
        # S1
        fa = {k: R[k + "_ta"][-1] for k in OFF_A}
        fb = {k: R[k + "_tb"][0] for k in OFF_B}
        s1 = self.sw1
        R["neg_s1"] = [fa["neg"], fa["neg"] + P(-0.15, -0.3), s1.com.get_center() + P(-0.18, 0.05), s1.com.get_center()]
        R["bla_s1"] = [fa["bla"], fa["bla"] + P(0, -0.32), fb["bla"] + P(0, -0.32), fb["bla"]]
        R["ver_s1"] = [fa["ver"], P(S1_C[0] - 0.46, S1_C[1] + 0.35), P(S1_C[0] - 0.46, s1.verde.get_center()[1] - 0.05), s1.verde.get_center()]
        R["roj_s1"] = [fb["roj"], fb["roj"] + P(0.18, -0.25), s1.t1.get_center() + P(0.16, 0.0), s1.t1.get_center()]
        R["ama_s1"] = [fb["ama"], P(S1_C[0] + 0.47, S1_C[1] + 0.4), P(S1_C[0] + 0.47, s1.t2.get_center()[1]), s1.t2.get_center()]
        R["ver2_s1"] = [fb["ver"], fb["ver"] + P(-0.05, -0.25), P(S1_C[0] + 0.2, S1_C[1] - 0.6), self.c1.tierra.get_center()]
        # caja octagonal
        lb = {k: R[k + "_tb"][-1] for k in OFF_B}
        lc = {k: R[k + "_tc"][0] for k in OFF_C}
        o = O_C
        pl, la = self.port.plata.get_center(), self.port.laton.get_center()
        R["roj_oa"] = [lb["roj"], o + P(-0.3, 0.22), o + P(-0.17, 0.3)]
        R["roj_ob"] = [lc["roj"], o + P(0.1, 0.2), o + P(-0.11, 0.3)]
        R["ama_oa"] = [lb["ama"], o + P(-0.05, 0.12), o + P(0.11, 0.3)]
        R["ama_ob"] = [lc["ama"], o + P(0.3, 0.12), o + P(0.17, 0.3)]
        R["bla_o"] = [lb["bla"], o + P(-0.32, -0.12), o + P(-0.34, -0.5), pl + P(-0.05, 0.08), pl]
        R["azu_o"] = [lc["azu"], o + P(0.32, -0.12), o + P(0.34, -0.5), la + P(0.05, 0.08), la]
        R["ver_oa"] = [lb["ver"], o + P(-0.2, -0.2), o + P(-0.04, -0.24)]
        R["ver_ob"] = [lc["ver"], o + P(0.2, -0.2), o + P(0.04, -0.24)]
        R["ver_oc"] = [o + P(0, -0.24), self.oc.tierra.get_center()]
        # S2
        f2 = {k: R[k + "_tc"][-1] for k in OFF_C}
        s2 = self.sw2
        R["azu_s2"] = [f2["azu"], f2["azu"] + P(-0.2, -0.2), s2.com.get_center() + P(-0.18, 0.05), s2.com.get_center()]
        R["roj_s2"] = [f2["roj"], f2["roj"] + P(0.2, -0.25), s2.t1.get_center() + P(0.16, 0), s2.t1.get_center()]
        R["ama_s2"] = [f2["ama"], P(S2_C[0] + 0.47, S2_C[1] + 0.4), P(S2_C[0] + 0.47, s2.t2.get_center()[1]), s2.t2.get_center()]
        R["ver_s2"] = [f2["ver"], P(S2_C[0] - 0.46, S2_C[1] + 0.35), P(S2_C[0] - 0.46, s2.verde.get_center()[1] - 0.05), s2.verde.get_center()]
        self.R = R

    GANCHO = {"neg_s1": 0.05, "roj_s1": 0.05, "ama_s1": 0.05, "ver_s1": 0.045, "ver2_s1": 0.04, "bla_o": 0.05, "azu_o": 0.05,
              "azu_s2": 0.05, "roj_s2": 0.05, "ama_s2": 0.05, "ver_s2": 0.045, "neg_tab": 0, "bla_tab": 0, "ver_tab": 0}

    def c(self, k, w=2.6):
        if k not in self.cab:
            cb = cable(*self.R[k], color=COL[k[:3]], w=w)
            if k in self.GANCHO:
                cb.add(punta_pelada(cb.ruta, 0.07, w, self.GANCHO[k]))
            self.cab[k] = cb
        return self.cab[k]

    def tornillos_encima(self):
        ts = [self.sw1.t1, self.sw1.t2, self.sw1.com, self.sw1.verde, self.sw2.t1, self.sw2.t2, self.sw2.com, self.sw2.verde,
              self.port.plata, self.port.laton, self.pan.nuestro.terminal, self.c1.tierra]
        self.bring_to_front(*ts)

    # -------------------------------------------------------------- esquema simbólico (para idea, esquema, tabla)
    def esquema(self, p1=1, p2=1, escala=1.0):
        """Esquema unifilar: F → común S1 ; viajeros ; común S2 → foco ; N → foco."""
        g = VGroup()
        xF, x1, x2, xL = -4.6, -2.0, 2.0, 4.4
        yT1, yT2 = 0.7, -0.3
        fuente_ = VGroup(RoundedRectangle(width=0.9, height=2.6, corner_radius=0.08, stroke_color=METAL_OSC, stroke_width=1.6).set_fill(GAL, 1),
                         T("F", 26, FASE, "HEAVY").shift(UP * 0.8), T("N", 26, "#667085", "HEAVY").shift(DOWN * 0.95)).move_to(P(xF, 0.0))
        com1, com2 = P(x1 - 0.55, 0.2), P(x2 + 0.55, 0.2)
        t11, t12, t21, t22 = P(x1 + 0.45, yT1), P(x1 + 0.45, yT2), P(x2 - 0.45, yT1), P(x2 - 0.45, yT2)
        cf = cable(P(xF + 0.45, 0.8), P(com1[0], 0.8), com1, color=FASE, w=6)
        v1 = cable(t11, t21, color=VIAJERO_1, w=6)
        v2 = cable(t12, t22, color=VIAJERO_2, w=6)
        ret = cable(com2, P(xL, 0.2), P(xL, 0.45), color=RET_AZUL, w=6)
        neu = cable(P(xF + 0.45, -0.95), P(xL, -0.95), P(xL, -0.45), color=NEUTRO, w=6)
        foco = foco_led(False, 0.9).rotate(PI / 2).scale(1.0)
        sock = Rectangle(width=0.5, height=0.9, stroke_color=METAL_OSC, stroke_width=1.2).set_fill(METAL, 1).move_to(P(xL, 0.0))
        foco.next_to(sock, RIGHT, buff=-0.1)
        bornes = VGroup(*[Dot(p, radius=0.07, color=TINTA) for p in (com1, t11, t12, com2, t21, t22)])
        cuch1 = Line(com1, t11 if p1 == 1 else t12, stroke_color=TINTA, stroke_width=6)
        cuch2 = Line(com2, t21 if p2 == 1 else t22, stroke_color=TINTA, stroke_width=6)
        et = VGroup(T("S1", 26, TINTA, "HEAVY").move_to(P(x1, 1.5)), T("S2", 26, TINTA, "HEAVY").move_to(P(x2, 1.5)),
                    T("común", 18, TINTA2, "BOLD").next_to(com1, DOWN, buff=0.15), T("común", 18, TINTA2, "BOLD").next_to(com2, DOWN, buff=0.15),
                    T("viajeros", 20, TINTA2, "BOLD").move_to(P(0, 1.15)))
        g.add(fuente_, cf, v1, v2, ret, neu, sock, foco, bornes, cuch1, cuch2, et)
        g.cuch1, g.cuch2, g.foco, g.sock = cuch1, cuch2, foco, sock
        g.pts = dict(com1=com1, com2=com2, t11=t11, t12=t12, t21=t21, t22=t22, xF=xF, xL=xL)
        g.scale(escala)
        return g

    def ruta_esquema(self, e, p1, p2):
        q = e.pts
        s = e.get_center()  # no usado: el esquema ya está colocado
        a = e.cuch1.get_start()
        a1 = e.cuch1.get_end()
        b1 = e.cuch2.get_end()
        b = e.cuch2.get_start()
        f0 = e[1].ruta.get_start()
        return [f0, e[1].ruta.get_points()[-1] if False else e[1].ruta.point_from_proportion(0.5), a, a1, b1, b,
                e[4].ruta.get_end()]

    def encendido_esquema(self, e, on):
        nuevo = foco_led(on, 0.9).rotate(PI / 2)
        nuevo.match_height(e.foco).move_to(e.foco)
        g = resplandor(e.foco.get_center(), 0.9 * e.foco.height, AMBAR, 10, 0.05) if on else VGroup()
        return nuevo, g

    # ============================================================== guion
    def construct(self):
        self.armar()
        for paso in ("intro", "usos", "nombre", "idea", "anatomia", "esquema_", "tabla", "identificar", "regla",
                     "seguridad", "materiales", "colores", "recorrido", "cableado", "continuidad", "pelado", "s1", "caja", "led", "s2",
                     "tierra", "placa", "prueba", "encender", "repaso", "errores", "cuatro"):
            if os.environ.get("SOLO") and paso not in os.environ["SOLO"].split(","):
                continue
            getattr(self, "f_" + paso)()
        self.resumen_y_final("cierre", ["La fase va al común del primero", "Los viajeros unen los dos interruptores",
                                        "El retorno sale del común del segundo", "El neutro va directo al foco"])

    # -------------------------------------------------------------- secciones
    def f_intro(self):
        self.voz("intro")
        esc = escalera_fondo().scale(0.62).move_to([-4.2, -1.0, 0])
        s_ab = placa_interruptor(P(-6.3, -2.2), 1).scale(0.9)
        s_ar = placa_interruptor(P(-2.0, 0.9), 1).scale(0.9)
        f = foco_led(False, 0.9).scale(1.8).move_to([-4.2, 2.6, 0])
        cordon = Line([-4.2, 4.6, 0], f.get_top(), stroke_color=LINEA, stroke_width=2)
        self.play(FadeIn(esc), FadeIn(s_ab), FadeIn(s_ar), Create(cordon), FadeIn(f), run_time=0.8)
        tit = self.titulo("APAGADOR DE", "ESCALERA", "interruptores de 3 vías · paso a paso")
        estado = [False]

        def alternar(sw):
            estado[0] = not estado[0]
            on = foco_led(estado[0], 0.9).scale(1.8).move_to(f)
            self.sfx("tic", -6)
            return [sw.pal.animate.shift(DOWN * 0.22 if sw.pal.get_center()[1] > sw.c[1] else UP * 0.22), Transform(f, on)]
        glow_ = resplandor(f[0].get_center(), 1.4, AMBAR, 10, 0.05)
        self.wait(1.0)
        self.play(*alternar(s_ab), FadeIn(glow_), run_time=0.4)
        self.wait(1.2)
        self.play(*alternar(s_ar), FadeOut(glow_), run_time=0.4)
        self.esperar_frac(0.3)
        self.play(*alternar(s_ar), FadeIn(glow_), run_time=0.4)
        self.esperar_frac(0.5)
        self.play(*alternar(s_ab), FadeOut(glow_), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(esc, s_ab, s_ar, f, cordon, tit, glow_)

    def f_usos(self):
        self.voz("usos")
        def icono(tipo):
            if tipo == 0:
                g = VGroup(*[Line(P(-0.9 + 0.3 * k, -0.6 + 0.25 * k), P(-0.6 + 0.3 * k, -0.6 + 0.25 * k)) for k in range(6)],
                           *[Line(P(-0.6 + 0.3 * k, -0.6 + 0.25 * k), P(-0.6 + 0.3 * k, -0.35 + 0.25 * k)) for k in range(6)])
            elif tipo == 1:
                g = VGroup(Line(P(-1, 0.6), P(-0.3, 0.2)), Line(P(-1, -0.6), P(-0.3, -0.2)), Line(P(1, 0.6), P(0.3, 0.2)),
                           Line(P(1, -0.6), P(0.3, -0.2)), Rectangle(width=0.6, height=0.4).move_to(ORIGIN))
            elif tipo == 2:
                g = VGroup(Rectangle(width=1.8, height=1.2), Rectangle(width=0.35, height=0.6).move_to(P(-0.9, -0.3)).set_fill(WHITE, 1),
                           Rectangle(width=0.35, height=0.6).move_to(P(0.9, -0.3)).set_fill(WHITE, 1))
            else:
                g = VGroup(Polygon(P(-1, 0.2), P(0, 0.8), P(1, 0.2)), Rectangle(width=1.6, height=0.9).move_to(P(0, -0.25)),
                           *[Line(P(-0.6, y), P(0.6, y)) for y in (-0.05, -0.25, -0.45)])
            return g.set_stroke(TINTA, 3)
        nombres = ["escaleras", "pasillos", "cuartos con\ndos puertas", "garajes"]
        cartas = VGroup()
        for k, n in enumerate(nombres):
            caja = tarjeta(3.3, 3.2, METAL)
            ic = icono(k).move_to(caja.get_center() + UP * 0.4)
            nm = VGroup(*[T(l, 28, TINTA, "BOLD") for l in n.split("\n")]).arrange(DOWN, buff=0.05).move_to(caja.get_center() + DOWN * 1.0)
            cartas.add(VGroup(caja, ic, nm))
        cartas.arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        tit = T("¿DÓNDE SE USA?", 46, TINTA, "HEAVY").move_to([0, 3.4, 0])
        self.play(FadeIn(tit), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cartas], lag_ratio=0.6), run_time=max(2.0, self.resta() * 0.6))
        self.cerrar_voz()
        self.limpiar(tit, cartas)

    def f_nombre(self):
        self.voz("nombre")
        sw = interruptor3(P(0, 0), 1).scale(3.2).move_to([-2.5, -0.2, 0])
        self.play(FadeIn(sw, scale=0.9), run_time=0.6)
        nums = VGroup()
        for k, t in enumerate((sw.com, sw.t1, sw.t2)):
            c_ = Circle(radius=0.38, stroke_color=MARCA, stroke_width=4).move_to(t)
            n = VGroup(Circle(radius=0.22, stroke_width=0).set_fill(MARCA, 1), T(str(k + 1), 22, WHITE, "HEAVY")).move_to(t.get_center() + (LEFT if k == 0 else RIGHT) * 0.75)
            n[1].move_to(n[0])
            nums.add(VGroup(c_, n))
        self.play(LaggedStart(*[FadeIn(n, scale=1.2) for n in nums], lag_ratio=0.4), run_time=1.4)
        tx = VGroup(T("3 VÍAS", 80, MARCA, "HEAVY"), T("= 3 terminales de conexión", 32, TINTA, "BOLD"),
                    T("(sin contar la tierra)", 26, TINTA2, "MEDIUM"), T("también: conmutador o interruptor de escalera", 26, TINTA2, "MEDIUM"))
        tx.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.6, 0.0, 0])
        self.play(FadeIn(tx[0], shift=RIGHT * 0.2), FadeIn(tx[1]), FadeIn(tx[2]), run_time=0.6)
        self.esperar_frac(0.4)
        self.play(FadeIn(tx[3]), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(sw, nums, tx)

    def f_idea(self):
        self.voz("idea")
        # izquierda: interruptor sencillo como puerta
        a, b = P(-6.2, 0.5), P(-3.2, 0.5)
        l1 = cable(a, P(-5.0, 0.5), color=FASE, w=7)
        l2 = cable(P(-4.2, 0.5), b, color=FASE, w=7)
        piv = Dot(P(-5.0, 0.5), radius=0.08, color=TINTA)
        cont = Dot(P(-4.2, 0.5), radius=0.08, color=TINTA)
        cuch = Line(P(-5.0, 0.5), P(-4.3, 1.0), stroke_color=TINTA, stroke_width=7)
        izq = VGroup(l1, l2, piv, cont, cuch, T("sencillo: abre o cierra", 28, TINTA, "BOLD").move_to(P(-4.7, -0.4)))
        # derecha: 3 vías como selector
        c0 = P(2.0, 0.2)
        t1, t2 = P(4.2, 1.0), P(4.2, -0.6)
        lc = cable(P(0.4, 0.2), c0, color=FASE, w=7)
        v1 = cable(t1, P(6.0, 1.0), color=VIAJERO_1, w=7)
        v2 = cable(t2, P(6.0, -0.6), color=VIAJERO_2, w=7)
        bor = VGroup(*[Dot(p, radius=0.09, color=TINTA) for p in (c0, t1, t2)])
        sel = Line(c0, t1, stroke_color=TINTA, stroke_width=7)
        et = VGroup(T("común", 26, TINTA, "HEAVY").next_to(c0, DOWN, buff=0.25), T("viajero 1", 24, VIAJERO_1, "BOLD").next_to(t1, UP, buff=0.18),
                    T("viajero 2", 24, "#B58900", "BOLD").next_to(t2, DOWN, buff=0.18))
        der = VGroup(lc, v1, v2, bor, sel, et, T("3 vías: selector", 28, TINTA, "BOLD").move_to(P(3.2, -1.7)))
        div = DashedLine([-1.2, 2.4, 0], [-1.2, -2.6, 0], stroke_color=METAL2, stroke_width=1.5)
        self.play(FadeIn(izq), Create(div), run_time=0.7)
        self.play(cuch.animate.put_start_and_end_on(P(-5.0, 0.5), P(-4.2, 0.5)), run_time=0.5)
        self.esperar_frac(0.2)
        self.play(FadeIn(der), run_time=0.7)
        for k in range(3):
            self.wait(max(0.3, self.resta() * 0.15))
            self.sfx("tic", -8)
            self.play(sel.animate.put_start_and_end_on(c0, t2 if k % 2 == 0 else t1), run_time=0.4)
        nunca = pastilla("nunca está simplemente apagado", MARCA, 28, True).move_to([3.2, -2.6, 0])
        self.play(FadeIn(nunca, scale=1.1), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(izq, der, div, nunca)

    def f_anatomia(self):
        self.voz("anatomia")
        sw = interruptor3(P(0, 0), 1).scale(3.4).move_to([-2.2, -0.2, 0])
        self.play(FadeIn(sw, scale=0.9), run_time=0.5)
        et = [(sw.com, "COMÚN · tornillo oscuro", "#3A3F47", LEFT), (sw.t1, "VIAJERO · latón", "#8A6D12", RIGHT),
              (sw.t2, "VIAJERO · latón", "#8A6D12", RIGHT), (sw.verde, "TIERRA · verde", TIERRA, LEFT)]
        grupos = VGroup()
        for t, txt, col, lado in et:
            p = pastilla(txt, col, 24, True)
            p.move_to(t.get_center() + lado * 2.6)
            ln = Line(t.get_center() + lado * 0.15, p.get_edge_center(-lado), stroke_color=col, stroke_width=1.6)
            grupos.add(VGroup(ln, p))
        for g in grupos:
            self.play(FadeIn(g), run_time=0.4)
            self.wait(max(0.2, self.resta() * 0.12))
        nota = VGroup(T("la palanca NO dice", 28, TINTA, "BOLD"), T("ON / OFF", 40, ROJO, "HEAVY")).arrange(DOWN, buff=0.05).move_to([4.3, -2.6, 0])
        self.play(Indicate(sw.palanca), FadeIn(nota), run_time=0.7)
        self.cerrar_voz()
        self.limpiar(sw, grupos, nota)

    def f_esquema_(self):
        self.voz("esquema")
        e = self.esquema(1, 1).move_to([0, 0.2, 0])
        fuente_, cf, v1, v2, ret, neu, sock, foco, bornes, c1, c2, et = e
        self.play(FadeIn(fuente_), FadeIn(bornes), FadeIn(c1), FadeIn(c2), FadeIn(sock), FadeIn(foco), FadeIn(et), run_time=0.6)
        self.play(Create(cf), run_time=0.8)
        self.esperar_frac(0.12)
        self.play(Create(v1), Create(v2), run_time=1.0)
        self.esperar_frac(0.2)
        self.play(Create(ret), run_time=0.8)
        self.esperar_frac(0.35)
        self.play(Create(neu), run_time=0.9)
        nota = pastilla("el neutro no pasa por ningún interruptor", "#475467", 26, True).move_to([0, -2.3, 0])
        self.play(FadeIn(nota), run_time=0.4)
        on, glow_ = self.encendido_esquema(e, True)
        ruta = [cf.ruta.get_start(), *cf.ruta.get_anchors()[1:], c1.get_end(), *v1.ruta.get_anchors(), c2.get_start(), *ret.ruta.get_anchors()]
        fl = corriente(concatenar([cf.ruta.get_start(), P(cf.ruta.get_end()[0], cf.ruta.get_start()[1]), cf.ruta.get_end()],
                                  [c1.get_end()], [v1.ruta.get_start(), v1.ruta.get_end()], [c2.get_start()],
                                  [ret.ruta.get_start(), P(ret.ruta.get_end()[0], ret.ruta.get_start()[1]), ret.ruta.get_end()]), vel=0.9)
        self.add(fl)
        self.play(Transform(foco, on), FadeIn(glow_), run_time=0.5)
        self.cerrar_voz()
        self.esq = e
        fl.clear_updaters()
        self.limpiar(fl, glow_, nota)
        self.play(FadeOut(e), run_time=0.3)

    def f_tabla(self):
        self.voz("tabla")
        celdas = VGroup()
        estados = [(1, 1), (1, 2), (2, 1), (2, 2)]
        for p1, p2 in estados:
            e = self.esquema(p1, p2, 0.48)
            on = p1 == p2
            if on:
                nuevo, glow_ = self.encendido_esquema(e, True)
                e.foco.become(nuevo)
                e.add_to_back(glow_)
            marco = tarjeta(e.width + 0.4, e.height + 0.9, METAL)
            estado = pastilla("ENCENDIDO" if on else "APAGADO", VERDE_OK if on else "#667085", 20, True)
            celdas.add(VGroup(marco, e, estado))
        for c_ in celdas:
            c_[1].move_to(c_[0].get_center() + UP * 0.25)
            c_[2].move_to(c_[0].get_bottom() + UP * 0.32)
        celdas.arrange_in_grid(2, 2, buff=(0.35, 0.3)).move_to([0, -0.15, 0])
        tit = T("LAS 4 COMBINACIONES", 40, TINTA, "HEAVY").move_to([0, 3.85, 0])
        self.play(FadeIn(tit), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in celdas], lag_ratio=0.5), run_time=2.4)
        self.esperar_frac(0.35)
        for k in (0, 3):
            self.play(Indicate(celdas[k][0], color=VERDE_OK, scale_factor=1.03), run_time=0.6)
        self.esperar_frac(0.4)
        for k in (1, 2):
            self.play(Indicate(celdas[k][0], color="#667085", scale_factor=1.03), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(tit, celdas)

    def f_identificar(self):
        self.voz("identificar")
        sw = interruptor3(P(0, 0), 1).scale(2.6).move_to([2.6, -0.2, 0])
        mm = multimetro().scale(0.95).move_to([-5.0, -0.3, 0])
        self.play(FadeIn(sw), FadeIn(mm), run_time=0.6)
        roja, negra = punta_prueba(ROJO), punta_prueba("#2A2E35")
        roja.rotate(0.4).move_to([0.6, 1.4, 0])
        negra.rotate(-0.4).move_to([0.6, -1.8, 0])
        self.play(FadeIn(roja), FadeIn(negra), run_time=0.3)

        def lect(txt, col):
            return T(txt, 40, col, "HEAVY", MONO).scale_to_fit_height(0.3).move_to(mm.lcd)

        def tocar(a, b):
            return [roja.animate.shift(a.get_center() - roja.tip.get_bottom()), negra.animate.shift(b.get_center() - negra.tip.get_bottom())]
        self.play(*tocar(sw.com, sw.t1), run_time=0.6)
        l = lect("·))) 0.0", VERDE_OK)
        n = pastilla("común ↔ viajero 1: continuidad", VERDE_OK, 24, True).move_to([2.6, 3.0, 0])
        self.play(FadeIn(l), FadeIn(n), run_time=0.4)
        self.esperar_frac(0.2)
        self.play(palanca3(sw, 2), run_time=0.3)
        l2 = lect("OL", "#1D2939")
        n2 = pastilla("palanca abajo: ahora con el viajero 2", MARCA, 24, True).move_to([2.6, 3.0, 0])
        self.play(Transform(l, l2), Transform(n, n2), run_time=0.4)
        self.esperar_frac(0.3)
        self.play(*tocar(sw.t1, sw.t2), run_time=0.6)
        n3 = pastilla("viajero ↔ viajero: nunca", ROJO, 24, True).move_to([2.6, 3.0, 0])
        self.play(Transform(n, n3), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(sw, mm, roja, negra, l, n)

    def f_regla(self):
        self.voz("regla")
        e = self.esquema(1, 1, 0.85).move_to([-2.4, 0.6, 0])
        self.play(FadeIn(e), run_time=0.5)
        marco = SurroundingRectangle(VGroup(e.cuch1, e.cuch2), buff=0.3, color=ENERGIA, stroke_width=3)
        sf = pastilla("solo la FASE se conmuta", ENERGIA, 26, True).next_to(marco, UP, buff=0.15)
        self.play(Create(marco), FadeIn(sf), run_time=0.6)
        carta = self.carta_nec("NEC 2020 · 404.2(A)", "Los de 3 y 4 vías conmutan solo el\nconductor no puesto a tierra (fase).", (4.4, 2.2), 5.4)
        self.play(FadeIn(carta, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.35)
        tub = tubo(P(-6.5, -2.6), P(1.5, -2.6), d=0.5)
        hilos = VGroup(*[cable(P(-6.4, -2.6 + o), P(1.4, -2.6 + o), color=cc, w=4) for o, cc in
                         ((0.15, FASE), (0.05, VIAJERO_1), (-0.05, VIAJERO_2), (-0.15, NEUTRO))])
        tub.set_opacity(0.35)
        txt = T("en tubo metálico: todos juntos, también el neutro", 26, TINTA, "BOLD").move_to([-2.5, -3.35, 0])
        self.play(FadeIn(tub), Create(hilos), FadeIn(txt), run_time=0.8)
        self.cerrar_voz()
        self.limpiar(e, marco, sf, carta, tub, hilos, txt)

    def f_materiales(self):
        self.voz("materiales")
        items = [
            (lambda: breaker("15", 0.46, 0.26).scale(3.2), "Breaker 1 polo · 15 A"),
            (lambda: VGroup(tubo(P(-1.0, 0), P(0.6, 0), d=0.22), conector(P(0.78, 0), 0, 0.22), abrazadera(P(-0.4, 0), d=0.22)), "Tubo EMT ½\"\nconectores y abrazaderas"),
            (lambda: VGroup(caja_rect_en(P(-0.7, 0), tornillo_tierra=False), caja_rect_en(P(0.7, 0), tornillo_tierra=False)), "2 cajas rectangulares\n2×4"),
            (lambda: caja_octagonal(), "Caja octagonal 4\""),
            (lambda: VGroup(interruptor3(P(-0.45, 0)), interruptor3(P(0.45, 0))), "2 interruptores\nde 3 vías"),
            (lambda: portalampara_led(), "Portalámparas\ncon foco LED"),
            (lambda: VGroup(tuerca_empalme(P(-0.35, 0), AMBAR, 0.45), tuerca_empalme(P(0.35, 0), TIERRA, 0.45)), "Conectores\nde empalme"),
            (lambda: cable_hilos(2.0, FASE, 0.5, 0.7), "Cable THHN 14 AWG\nde varios hilos"),
        ]
        g = self.tarjetas(items)
        self.cerrar_voz()
        self.limpiar(g)

    def f_colores(self):
        self.voz("colores")
        tit = T("COLORES DE ESTE CIRCUITO", 44, TINTA, "HEAVY").move_to([0, 3.75, 0])
        self.play(FadeIn(tit), run_time=0.3)
        filas = [(FASE, "FASE", "negro"), (NEUTRO, "NEUTRO", "blanco"), (TIERRA, "TIERRA", "verde"),
                 (VIAJERO_1, "VIAJERO", "rojo"), (VIAJERO_2, "VIAJERO", "amarillo"), (RET_AZUL, "RETORNO", "azul")]
        grupos = VGroup()
        for k, (col, nombre, desc) in enumerate(filas):
            y = 2.6 - 0.85 * k
            w = cable(P(-6.6, y), P(-2.0, y), color=col, w=14)
            w.add(punta_pelada(w.ruta, 0.3, 14))
            nm = T(nombre, 34, col if col not in (NEUTRO, VIAJERO_2, FASE) else {NEUTRO: "#667085" if TEMA != "oscuro" else "#E4E7EC", VIAJERO_2: "#B58900" if TEMA != "oscuro" else "#FDB022", FASE: FASE if TEMA != "oscuro" else "#C9D1F0"}[col], "HEAVY")
            nm.move_to([-0.9, y, 0], aligned_edge=LEFT)
            ds = T(desc, 24, TINTA2, "MEDIUM").next_to(nm, RIGHT, buff=0.3)
            grupos.add(VGroup(w, nm, ds))
        for k, g in enumerate(grupos):
            self.play(Create(g[0]), FadeIn(g[1:]), run_time=0.5)
            if k == 2:
                self.esperar_frac(0.2)
        nota = self.carta_nec("NEC", "Blanco/gris = neutro · verde = tierra.\nViajeros y retorno: cualquier otro color.", (3.8, -3.0), 5.6)
        self.play(FadeIn(nota, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, grupos, nota)

    def f_recorrido(self):
        self.voz("recorrido")
        self.camera.frame.set(width=16).move_to(P(0, -0.2))
        self.play(FadeIn(self.fondo_esc), FadeIn(self.var), FadeIn(self.pan), run_time=0.6)
        self.play(Create(self.tubos[0]), FadeIn(self.c1), FadeIn(self.sw1), run_time=1.0)
        e1 = pastilla("Interruptor 1 · abajo", TINTA, 24).move_to(S1_C + P(0, -1.25))
        self.play(FadeIn(e1), run_time=0.3)
        self.esperar_frac(0.25)
        self.play(Create(self.tubos[1]), FadeIn(self.oc), FadeIn(self.port), run_time=1.0)
        e2 = pastilla("Foco · caja octagonal", TINTA, 24).move_to(O_C + P(0, 0.95))
        self.play(FadeIn(e2), run_time=0.3)
        self.esperar_frac(0.4)
        self.play(Create(self.tubos[2]), FadeIn(self.c2), FadeIn(self.sw2), run_time=1.0)
        e3 = pastilla("Interruptor 2 · arriba", TINTA, 24).move_to(S2_C + P(0, -1.2))
        self.play(FadeIn(e3), FadeIn(self.cons), FadeIn(self.abr), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(e1, e2, e3)

    def f_cableado(self):
        self.voz("cableado")
        self.play(self.tubos.animate.set_stroke(opacity=0.28), run_time=0.4)
        grupos = [["neg_ta", "bla_ta", "ver_ta"], ["roj_tb", "ama_tb", "bla_tb", "ver_tb"], ["roj_tc", "ama_tc", "azu_tc", "ver_tc"]]
        textos = [("negro · blanco · verde", P(-3.5, 2.45)), ("rojo · amarillo · blanco · verde", P(-0.6, 3.25)),
                  ("rojo · amarillo · azul · verde", P(3.3, 3.25))]
        chips = VGroup()
        for k, (gr, (txt, pos)) in enumerate(zip(grupos, textos)):
            ws = [self.c(x, 2.2) for x in gr]
            self.play(*[Create(w) for w in ws], run_time=1.3)
            ch = self.chip(txt, pos, TINTA, 20)
            self.play(FadeIn(ch), run_time=0.3)
            chips.add(ch)
            self.mundo.add(*ws)
            self.esperar_frac(0.2 if k < 2 else 0.0)
        self.play(self.tubos.animate.set_stroke(opacity=1), run_time=0.4)
        self.bring_to_front(self.tubos, self.cons, self.abr)
        self.cerrar_voz()
        self.limpiar(chips)

    def f_continuidad(self):
        self.voz("continuidad")
        cr = cable_hilos(3.2, VIAJERO_1, 0.42, 0.6).move_to([-2.2, 0.8, 0])
        ca = cable_hilos(3.2, VIAJERO_2, 0.42, 0.6).move_to([-2.2, -0.4, 0])
        ce = cable_hilos(3.2, RET_AZUL, 0.42, 0.6).move_to([-2.2, -1.6, 0])
        fondo_ = tarjeta(9.0, 5.0, METAL).move_to([0, -0.2, 0])
        self.ir(ORIGIN, 16, 0.5, FadeOut(self.mundo))
        self.play(FadeIn(fondo_), FadeIn(cr), FadeIn(ca), FadeIn(ce), run_time=0.5)
        cintas = VGroup(*[RoundedRectangle(width=0.32, height=0.52, corner_radius=0.06, stroke_color="#344054", stroke_width=1)
                          .set_fill(c_, 1).move_to(w[2].get_center() + RIGHT * 1.0) for w, c_ in ((cr, WHITE), (ca, WHITE))])
        for ci in cintas:
            ci.add(T("V", 16, TINTA, "HEAVY").move_to(ci))
        self.play(LaggedStart(*[FadeIn(ci, scale=1.4) for ci in cintas], lag_ratio=0.4), run_time=0.8)
        txt = VGroup(T("cinta = viajero", 30, TINTA, "HEAVY"), T("sin cinta = retorno", 26, TINTA2, "BOLD")).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        txt.move_to([2.9, -0.4, 0])
        self.play(FadeIn(txt), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(fondo_, cr, ca, ce, cintas, txt)
        self.play(FadeIn(self.mundo), run_time=0.4)

    def f_pelado(self):
        self.voz("pelado")
        self.ir(ORIGIN, 16, 0.4, FadeOut(self.mundo))
        ab = cable_hilos(5.0, FASE, 0.55, 1.4, abierto=True).move_to([-2.0, 0.8, 0])
        to = cable_hilos(5.0, FASE, 0.55, 1.4, abierto=False).move_to([-2.0, 0.8, 0])
        t1 = T("hilos abiertos", 26, ROJO, "BOLD").move_to([-2.0, -0.2, 0])
        self.play(FadeIn(ab), FadeIn(t1), run_time=0.5)
        self.esperar_frac(0.2)
        t2 = T("tuércelos: quedan juntos", 26, VERDE_OK, "BOLD").move_to([-2.0, -0.2, 0])
        self.play(Transform(ab, to), Transform(t1, t2), run_time=1.2)
        cx = np.array([4.4, 0.3, 0])
        lupa = Circle(radius=1.9, stroke_color=TINTA2, stroke_width=2).set_fill(WHITE, 1).move_to(cx)
        tor = tornillo(0.5, LATON, 0.5).move_to(cx)
        gancho = VMobject().set_points_smoothly([cx + P(-1.9, -0.9), cx + P(-1.0, -0.7), cx + P(-0.6, -0.25),
                                                 cx + P(-0.52, 0.25), cx + P(0, 0.58), cx + P(0.52, 0.28), cx + P(0.56, -0.15)])
        g1 = gancho.copy().set_stroke(_osc(COBRE, 0.4), 22)
        g2 = gancho.copy().set_stroke(COBRE, 16)
        flecha = CurvedArrow(cx + P(-0.85, 0.7), cx + P(0.9, 0.55), angle=-1.2, color=MARCA, stroke_width=4, tip_length=0.22)
        tx = T("en sentido del reloj ↻", 26, MARCA, "HEAVY").next_to(lupa, DOWN, buff=0.2)
        self.play(FadeIn(lupa), FadeIn(tor), run_time=0.4)
        self.play(Create(g1), Create(g2), run_time=0.8)
        self.play(Create(flecha), FadeIn(tx), run_time=0.5)
        self.play(Rotate(tor[1], PI), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(ab, t1, lupa, tor, g1, g2, flecha, tx)
        self.play(FadeIn(self.mundo), run_time=0.4)

    def f_s1(self):
        self.voz("s1")
        self.ir(S1_C + P(1.3, 0.1), 4.6, 1.0)
        pasos = [("neg_s1", "negro → común (oscuro)", FASE), ("roj_s1", "rojo → latón", VIAJERO_1), ("ama_s1", "amarillo → latón", "#B58900"),
                 ("bla_s1", "blanco: sigue de paso", "#475467"), ("ver_s1", "verde → interruptor", TIERRA), ("ver2_s1", "verde → caja", TIERRA)]
        etq = VGroup()
        for k, (cl, txt, col) in enumerate(pasos):
            w = self.c(cl)
            e = pastilla(txt, col, 20, True)
            self.pant(e, (4.6, 2.6 - 0.75 * k))
            self.play(Create(w), FadeIn(e), run_time=0.6)
            self.mundo.add(w)
            etq.add(e)
            self.esperar_frac(0.1)
        self.tornillos_encima()
        self.apretar(self.sw1.com, 0.8)
        self.cerrar_voz()
        self.limpiar(etq)

    def f_caja(self):
        self.voz("caja")
        self.ir(O_C + P(0.6, -0.3), 3.4, 1.0)
        ra, rb, aa, ab = self.c("roj_oa"), self.c("roj_ob"), self.c("ama_oa"), self.c("ama_ob")
        self.play(Create(ra), Create(rb), run_time=0.6)
        n1 = tuerca_empalme(O_C + P(-0.14, 0.37), "#F04438", 0.14)
        self.play(FadeIn(n1, shift=DOWN * 0.05), run_time=0.3)
        self.play(Create(aa), Create(ab), run_time=0.6)
        n2 = tuerca_empalme(O_C + P(0.14, 0.37), AMBAR, 0.14)
        self.play(FadeIn(n2, shift=DOWN * 0.05), run_time=0.3)
        e1 = self.chip("rojo+rojo · amarillo+amarillo", O_C + P(1.35, 0.55), TINTA, 18, True)
        self.play(FadeIn(e1), run_time=0.3)
        self.esperar_frac(0.2)
        b = self.c("bla_o")
        e2 = self.chip("blanco → rosca", self.port.plata.get_center() + P(-0.25, -0.3), "#475467", 18, True)
        self.play(Create(b), FadeIn(e2), run_time=0.7)
        self.esperar_frac(0.2)
        a = self.c("azu_o")
        e3 = self.chip("azul (retorno) → centro", self.port.laton.get_center() + P(1.0, -0.15), RET_AZUL, 18, True)
        self.play(Create(a), FadeIn(e3), run_time=0.7)
        self.esperar_frac(0.3)
        v = VGroup(self.c("ver_oa"), self.c("ver_ob"), self.c("ver_oc"))
        n3 = tuerca_empalme(O_C + P(0, -0.19), TIERRA, 0.12)
        self.play(Create(v), run_time=0.7)
        self.play(FadeIn(n3), Indicate(self.oc.tierra, color=TIERRA), run_time=0.5)
        self.mundo.add(ra, rb, aa, ab, b, a, v, n1, n2, n3)
        self.tornillos_encima()
        self.cerrar_voz()
        self.limpiar(e1, e2, e3)

    def f_led(self):
        self.voz("led")
        self.ir(P(O_C[0], LAMP_T - 0.7), 3.0, 0.8)
        f = foco_led(False, 0.9).scale(3.0)
        pnl = VGroup(tarjeta(4.0, 4.6, METAL), f)
        f.move_to(pnl[0].get_center() + UP * 0.3)
        etq = VGroup(T("difusor", 22, TINTA2, "BOLD").next_to(f, LEFT, buff=0.1).shift(DOWN * 0.6),
                     T("disipador", 22, TINTA2, "BOLD").next_to(f, RIGHT, buff=0.1).shift(UP * 0.55),
                     T("base E26", 22, TINTA2, "BOLD").next_to(f, RIGHT, buff=0.1).shift(UP * 1.1))
        pnl.add(etq)
        pnl.add(T("foco LED", 30, MARCA, "HEAVY").move_to(pnl[0].get_bottom() + UP * 0.45))
        self.pant(pnl, (4.6, 0.0))
        self.play(FadeIn(pnl, shift=LEFT * 0.2), run_time=0.6)
        self.esperar_frac(0.45)
        r = VGroup(pastilla("neutro → rosca", "#475467", 22, True), pastilla("retorno → centro", RET_AZUL, 22, True)).arrange(DOWN, buff=0.15)
        self.pant(r, (-4.6, -2.6))
        self.play(FadeIn(r), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(pnl, r)

    def f_s2(self):
        self.voz("s2")
        self.ir(S2_C + P(1.3, 0.1), 4.6, 1.0)
        pasos = [("azu_s2", "azul (retorno) → común", RET_AZUL), ("roj_s2", "rojo → latón", VIAJERO_1),
                 ("ama_s2", "amarillo → latón", "#B58900"), ("ver_s2", "verde → tornillo verde", TIERRA)]
        etq = VGroup()
        for k, (cl, txt, col) in enumerate(pasos):
            w = self.c(cl)
            e = pastilla(txt, col, 20, True)
            self.pant(e, (4.6, 2.2 - 0.8 * k))
            self.play(Create(w), FadeIn(e), run_time=0.6)
            self.mundo.add(w)
            etq.add(e)
            self.esperar_frac(0.14)
        self.tornillos_encima()
        cl = pastilla("lo clave: no confundir el común", ROJO, 22, True)
        self.pant(cl, (3.8, -2.9))
        self.play(FadeIn(cl, scale=1.1), Indicate(self.sw2.com, color=ROJO), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(etq, cl)

    def f_tierra(self):
        self.voz("tierra")
        self.ir(P(0.2, -0.2), 16, 1.0)
        verdes = VGroup(*[self.cab[k] for k in self.cab if k.startswith("ver")])
        metal = VGroup(self.c1[0], self.c2[0], self.oc[1], *self.tubos)
        self.play(Indicate(metal, color=METAL_OSC, scale_factor=1.0), run_time=0.8)
        self.play(*[Indicate(v, color="#0B7A33", scale_factor=1.0) for v in verdes], run_time=1.0)
        chispa_ = rayo(S2_C + P(0.2, 0.3), S2_C + P(0.5, 0.45), ENERGIA, 3, 0.04, 2, 3)
        self.esperar_frac(0.3)
        self.sfx("pop", -4)
        self.add(chispa_)
        ruta = concatenar(inv(self.R["ver_s2"]), inv(self.R["ver_tc"]), [O_C + P(0.04, -0.24)], self.R["ver_oa"][::-1][1:],
                          inv(self.R["ver_tb"]), self.R["ver2_s1"][:1][::-1], inv(self.R["ver_ta"]), inv(self.R["ver_tab"])[::-1][::-1])
        fl = corriente(concatenar(inv(self.R["ver_tc"]), inv(self.R["ver_tb"]), inv(self.R["ver_ta"]), self.R["ver_tab"]),
                       vel=1.4, color="#E5484D", color2="#FFB3B5")
        self.add(fl)
        self.esperar_frac(0.5)
        self.sfx("tic", -2)
        self.play(mover_palanca(self.pan.nuestro, False), run_time=0.2)
        ab = self.chip("¡el breaker se dispara!", self.pan.nuestro.get_center() + P(2.2, 0.0), ROJO, 24, True)
        self.play(FadeIn(ab, scale=1.2), run_time=0.3)
        self.cerrar_voz()
        fl.clear_updaters()
        self.limpiar(fl, chispa_, ab)
        self.pan.nuestro.palanca.move_to(self.pan.nuestro[1].get_center() + RIGHT * self.pan.nuestro[0].width * 0.08)

    def f_placa(self):
        self.voz("placa")
        self.ir(P(0.2, -0.2), 16, 0.4)
        self.pl1 = placa_interruptor(S1_C + P(-0.08, 0), 1)
        self.pl2 = placa_interruptor(S2_C + P(-0.08, 0), 1)
        self.tapa_o = Circle(radius=OCT_R * 0.98, stroke_color=METAL_OSC, stroke_width=1.2).set_fill("#F0F2F5", 1).move_to(O_C)
        self.wait(0.6)
        self.play(FadeIn(self.pl1, shift=UP * 0.1), run_time=0.6)
        self.esperar_frac(0.3)
        self.play(FadeIn(self.pl2, shift=UP * 0.1), FadeIn(self.tapa_o), run_time=0.6)
        self.bring_to_front(self.port)
        self.cerrar_voz()
        self.mundo.add(self.pl1, self.pl2, self.tapa_o)

    def f_prueba(self):
        self.voz("prueba")
        lista = VGroup(*[VGroup(check(VERDE_OK, 0.2), T(t, 26, TINTA, "BOLD")).arrange(RIGHT, buff=0.2) for t in
                         ("fase → común del interruptor 1", "retorno ← común del interruptor 2", "neutro → foco, sin interruptores")])
        lista.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        caja = tarjeta(lista.width + 0.7, lista.height + 0.6, METAL).move_to(lista)
        g = VGroup(caja, lista).move_to([1.6, -2.75, 0])
        self.play(FadeIn(caja), run_time=0.2)
        for f in lista:
            self.play(FadeIn(f, shift=RIGHT * 0.15), run_time=0.4)
            self.wait(max(0.2, self.resta() * 0.18))
        self.cerrar_voz(-0.9)
        self.sfx("tic", -4)
        self.play(FadeOut(g), run_time=0.3)

    def ruta_encendida(self, p1, p2):
        R = self.R
        b = self.pan.nuestro.terminal.get_center()
        s1t = self.sw1.t1.get_center() if p1 == 1 else self.sw1.t2.get_center()
        via1 = "roj" if p1 == 1 else "ama"
        via2 = "roj" if p2 == 1 else "ama"
        tramo_v = concatenar(R[f"{via1}_s1"][::-1], R[f"{via1}_tb"], R[f"{via1}_oa"], R[f"{via2}_ob"][::-1] if via1 == via2 else [],
                             R[f"{via1}_tc"] if via1 == via2 else [], R[f"{via1}_s2"] if via1 == via2 else [])
        return concatenar(inv(R["neg_tab"]), R["neg_ta"], R["neg_s1"], [self.sw1.com.get_center(), s1t], tramo_v,
                          [self.sw2.com.get_center()], inv(R["azu_s2"]), inv(R["azu_tc"]), R["azu_o"],
                          [self.port.laton.get_center(), self.port.foco.vidrio.get_center(), self.port.plata.get_center()],
                          inv(R["bla_o"]), inv(R["bla_tb"]), inv(R["bla_s1"]), inv(R["bla_ta"]), R["bla_tab"])

    def f_encender(self):
        self.voz("encender")
        self.play(self.tubos.animate.set_stroke(opacity=0.3), run_time=0.4)   # tubos translúcidos: se ve la corriente
        self.play(mover_palanca(self.pan.nuestro, True), run_time=0.3)
        estados = [(1, 1), (2, 1), (2, 2), (1, 2), (1, 1)]
        fl = None
        glow_ = VGroup()
        cap = pastilla("abajo: 1 · arriba: 1", TINTA, 24, True).move_to([1.6, -3.1, 0])
        self.add(cap)
        dur = self.resta()
        for k, (p1, p2) in enumerate(estados):
            on = p1 == p2
            anims = []
            if k > 0:
                pl = self.pl1 if estados[k - 1][0] != p1 else self.pl2
                pos = p1 if pl is self.pl1 else p2
                anims.append(pl.pal.animate.move_to(pl.c + P(0, 0.12 if pos == 1 else -0.12)))
                self.sfx("tic", -4)
            nuevo = foco_led(on, 0.85).move_to(self.port.foco)
            anims.append(Transform(self.port.foco, nuevo))
            if fl is not None:
                fl.clear_updaters()
                anims.append(FadeOut(fl))
            nuevo_glow = resplandor(self.port.foco.vidrio.get_center(), 1.4, AMBAR, 12, 0.05) if on else VGroup()
            anims += [FadeOut(glow_), FadeIn(nuevo_glow)]
            anims.append(Transform(cap, pastilla(f"abajo: {p1} · arriba: {p2}  →  {'ENCENDIDO' if on else 'APAGADO'}",
                                                 VERDE_OK if on else "#667085", 24, True).move_to([1.6, -3.1, 0])))
            self.play(*anims, run_time=0.45)
            glow_ = nuevo_glow
            fl = corriente(self.ruta_encendida(p1, p2), vel=0.8) if on else corriente(
                concatenar(inv(self.R["neg_tab"]), self.R["neg_ta"], self.R["neg_s1"],
                           [self.sw1.com.get_center(), self.sw1.t1.get_center() if p1 == 1 else self.sw1.t2.get_center()]), vel=0.8)
            self.add(fl)
            self.wait(max(2.2, dur / len(estados) - 0.45) if k < len(estados) - 1 else 0.5)
        self.cerrar_voz()
        if self.renderer.time < 360:
            self.wait(1.5)
        fl.clear_updaters()
        self.play(self.tubos.animate.set_stroke(opacity=1), run_time=0.3)
        self.limpiar(fl, glow_, cap)
        self.limpiar(self.mundo, *self.cab.values(), t=0.4)

    def f_repaso(self):
        self.voz("repaso")
        self.camera.frame.set(width=16).move_to(P(0, -0.2))
        cabs = list(self.cab.values())
        self.play(FadeIn(self.mundo), *[FadeIn(c_) for c_ in cabs], run_time=0.8)
        self.tornillos_encima()
        self.play(self.tubos.animate.set_stroke(opacity=0.3), run_time=0.3)
        R = self.R
        tramos = [
            ("fase → común del 1", FASE, concatenar(inv(R["neg_tab"]), R["neg_ta"], R["neg_s1"]), 0.12),
            ("viajeros: 1 → caja → 2", VIAJERO_1, concatenar(inv(R["roj_s1"]), R["roj_tb"], R["roj_oa"], inv(R["roj_ob"]), R["roj_tc"], R["roj_s2"]), 0.3),
            ("retorno: común del 2 → centro", RET_AZUL, concatenar(inv(R["azu_s2"]), inv(R["azu_tc"]), R["azu_o"]), 0.25),
            ("neutro y tierra: sin interruptor", "#475467", concatenar(inv(R["bla_o"]), inv(R["bla_tb"]), inv(R["bla_s1"]), inv(R["bla_ta"]), R["bla_tab"]), 0.3),
        ]
        prev = []
        for k, (txt, col, ruta, f) in enumerate(tramos):
            e = pastilla(txt, col, 26, True).move_to([3.2, -2.9, 0])
            fl = corriente(ruta, vel=0.9)
            self.play(*[FadeOut(m) for m in prev], FadeIn(e, shift=UP * 0.15), run_time=0.4)
            self.add(fl)
            prev = [e, fl]
            self.esperar_frac(f if k < len(tramos) - 1 else 0.9)
        self.cerrar_voz()
        self.limpiar(*prev)
        self.tubos.set_stroke(opacity=1)
        self.limpiar(self.mundo, *cabs, t=0.4)

    def f_errores(self):
        self.voz("errores")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        i1 = self.esquema(1, 1, 0.5)
        i1.add(equis(ROJO, 0.3).move_to(i1.pts["t11"] + UP * 0.6))
        i2 = interruptor3(P(0, 0), 1).scale(1.6)
        i2.add(Circle(radius=0.3, stroke_color=ROJO, stroke_width=4).move_to(i2.com), T("¿común?", 22, ROJO, "HEAVY").next_to(i2, LEFT, buff=0.1))
        i3 = VGroup(cable(P(-1.4, 0.2), P(1.4, 0.2), color=NEUTRO, w=8), T("neutro", 22, "#667085", "BOLD").move_to(P(0, 0.55)),
                    Line(P(-0.3, 0.2), P(0.3, 0.6), stroke_color=TINTA, stroke_width=6), equis(ROJO, 0.3).move_to(P(0.9, -0.4)))
        self.tres_errores([("1", "Fase en un\nviajero", "el foco solo funciona\nen algunas posiciones"),
                           ("2", "Confundir\nel común", "busca siempre\nel tornillo oscuro"),
                           ("3", "Conmutar\nel neutro", "el portalámparas\nqueda energizado")], [i1, i2, i3])

    def f_cuatro(self):
        self.voz("cuatro")
        g = VGroup()
        xs = (-4.5, 0.0, 4.5)
        caja = [RoundedRectangle(width=2.2, height=1.8, corner_radius=0.15, stroke_color=TINTA, stroke_width=2).set_fill(CARTA, 1).move_to(P(x, 0.2)) for x in xs]
        nombres = [T(t, 28, TINTA, "HEAVY").move_to(P(x, 1.55)) for t, x in zip(("3 vías", "4 vías", "3 vías"), xs)]
        v = VGroup(cable(P(-3.4, 0.6), P(-1.1, 0.6), color=VIAJERO_1, w=7), cable(P(-3.4, -0.2), P(-1.1, -0.2), color=VIAJERO_2, w=7),
                   cable(P(1.1, 0.6), P(3.4, 0.6), color=VIAJERO_1, w=7), cable(P(1.1, -0.2), P(3.4, -0.2), color=VIAJERO_2, w=7))
        cruz = VGroup(Line(P(-1.1, 0.6), P(1.1, -0.2)), Line(P(-1.1, -0.2), P(1.1, 0.6))).set_stroke(TINTA, 5)
        recto = VGroup(Line(P(-1.1, 0.6), P(1.1, 0.6)), Line(P(-1.1, -0.2), P(1.1, -0.2))).set_stroke(TINTA, 5)
        g.add(*caja, *nombres, v)
        self.play(FadeIn(g), Create(recto), run_time=0.8)
        txt = T("cruza los viajeros", 30, MARCA, "HEAVY").move_to(P(0, -1.3))
        self.esperar_frac(0.3)
        self.play(Transform(recto, cruz), FadeIn(txt), run_time=0.6)
        prox = pastilla("próximo video", MARCA, 26, True).move_to(P(0, -2.6))
        self.play(FadeIn(prox, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(g, recto, txt, prox)

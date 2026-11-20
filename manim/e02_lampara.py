"""E02 · Circuito simple con lámpara (horizontal). Guion y fuentes en e02_guion.py."""
from nema import *
from e02_guion import GUION
from dibujos_aves import check, equis, PIEL

VISTA_PANEL = (P(-3.9, -0.45), 7.6)


def concatenar(*tramos):
    pts = []
    for t in tramos:
        for p in t:
            p = np.array(p, float)
            if not pts or np.linalg.norm(pts[-1] - p) > 1e-4:
                pts.append(p)
    return pts


def inv(t):
    return list(reversed(t))


class Lampara(Escena):
    CARPETA_VOZ = "voz_e02"
    GUION = GUION

    # -------------------------------------------------------------- utilidades de cámara y pantalla
    @property
    def z(self):
        return self.camera.frame.width / 16

    def ir(self, centro, ancho, rt=1.2, *extra):
        self.play(self.camera.frame.animate.set(width=ancho).move_to(centro), *extra, run_time=rt)

    def pant(self, m, pos):
        """Coloca m (diseñado para pantalla completa) en la posición de pantalla pos, con la cámara actual."""
        p = np.array(list(pos) + [0] * (3 - len(pos)), float)
        for sm in m.family_members_with_points():
            sm.fisico = False
        m.scale(self.z).move_to(self.camera.frame.get_center() + p * self.z)
        return m

    def et(self, texto, pos_mundo, color=TINTA, size=28, peso="BOLD"):
        return T(texto, size, color, peso).scale(self.z).move_to(pos_mundo)

    def chip(self, texto, pos_mundo, color=MARCA, size=24, solido=False):
        return pastilla(texto, color, size, solido).scale(self.z).move_to(pos_mundo)

    def carta_nec(self, codigo, texto, pos=(4.6, 2.9), ancho=5.6, color=MARCA):
        cod = pastilla(codigo, color, 24, True)
        lineas = VGroup(*[T(l, 24, TINTA, "MEDIUM") for l in texto.split("\n")]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        cuerpo = VGroup(cod, lineas).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        caja = tarjeta(max(ancho, cuerpo.width + 0.5), cuerpo.height + 0.45, color=interpolate_color(ManimColor(color), ManimColor(WHITE), 0.3))
        caja.set_stroke(width=1.4)
        cuerpo.move_to(caja)
        g = VGroup(sombra(caja), caja, cuerpo)
        return self.pant(g, pos)

    def fuente_p(self, texto):
        return self.pant(fuente(texto, [0, -4.15, 0], 20), [-1.6, -4.15])

    def limpiar(self, *ms, t=0.4):
        ms = [m for m in ms if m is not None]
        for m in ms:
            for s in m.get_family():
                s.clear_updaters()
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=t)

    def esperar_frac(self, f):
        w = self.resta() * f
        if w > 0.05:
            self.wait(w)

    def flujo(self, pts, n=26, color=ENERGIA, r=0.035, vel=0.06):
        ruta = VMobject().set_points_as_corners(pts)
        g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
        g.fase = 0.0

        def upd(m, dt):
            m.fase = (m.fase + dt * vel) % 1
            for k, d in enumerate(m):
                d.move_to(ruta.point_from_proportion((m.fase + k / n) % 1))
        g.add_updater(upd)
        upd(g, 0)
        return g

    def apretar(self, objetivo, t=1.0):
        """Destornillador baja y gira el tornillo."""
        d = destornillador(1.4).scale(self.z * 1.4)
        punta = d[1].get_bottom()
        d.shift(objetivo.get_center() - punta + UP * 0.6 * self.z)
        self.play(FadeIn(d), d.animate.shift(DOWN * 0.6 * self.z), run_time=0.4)
        self.play(Rotate(objetivo[1], PI * 1.5), d.animate.stretch(0.8, 0), run_time=t * 0.5)
        self.play(d.animate.stretch(1 / 0.8, 0), run_time=0.15)
        self.play(FadeOut(d, shift=UP * 0.4 * self.z), run_time=0.3)

    # -------------------------------------------------------------- mundo
    def armar_mundo(self):
        self.pan = centro_carga()
        self.var = varilla_tierra()
        self.oc = caja_octagonal()
        self.cr = caja_rect()
        self.sw = interruptor(False)
        self.port = portalampara(P(OCT_C[0], LAMP_TOP))
        self.t1 = tubo(*TUBO1)
        self.t2 = tubo(*TUBO2)
        self.cons = VGroup(conector(E + P(0, 0.12), PI / 2), conector(OCT_C + P(-OCT_R - 0.1, 0), 0),
                           conector(OCT_C + P(OCT_R + 0.1, 0), PI), conector(P(SW_C[0], SW_C[1] + SW_H / 2 + 0.12), -PI / 2))
        self.R = rutas_cables(self.port, self.sw, self.pan)
        self.cab = {}

    PUNTAS = {"neg_tab": 0, "bla_tab": 0, "ver_tab": 0, "bla_oct": 0.05, "roj_oct": 0.05,
              "neg_sw": 0.05, "roj_sw": 0.05, "ver_sw": 0.045}

    def c(self, clave, w=2.6):
        if clave not in self.cab:
            cb = cable(*self.R[clave], color=COLOR_DE[clave[:3]], w=w)
            if clave in self.PUNTAS:
                cb.add(punta_pelada(cb.ruta, 0.07, w, self.PUNTAS[clave]))
            self.cab[clave] = cb
        return self.cab[clave]

    def tornillos_encima(self):
        self.bring_to_front(self.sw.l1, self.sw.l2, self.sw.verde, self.port.plata, self.port.laton, self.pan.nuestro.terminal)

    # ============================================================== guion
    def construct(self):
        self.armar_mundo()
        self.intro()
        self.plano()
        self.materiales()
        self.colores()
        self.seguridad()
        self.tablero()
        self.breaker_()
        self.tuberia()
        self.cableado()
        self.conexiones()
        self.caja()
        self.tierra()
        self.relleno()
        self.interruptor_()
        self.neutro_sw()
        self.lampara()
        self.rosca()
        self.regla()
        self.pruebas()
        self.encender()
        self.errores()
        self.cierre()

    # -------------------------------------------------------------- 1 intro
    def intro(self):
        self.voz("intro")
        f = foco(False, 0.9).scale(4.2).move_to([-4.2, -0.2, 0])
        cordon = Line([-4.2, 4.6, 0], f.get_top(), stroke_color=LINEA, stroke_width=2)
        self.play(Create(cordon), FadeIn(f, shift=DOWN * 0.4), run_time=0.8)
        t1 = T("CIRCUITO SIMPLE", 64, TINTA, "HEAVY")
        t2 = T("CON LÁMPARA", 78, MARCA, "HEAVY")
        t3 = T("del tablero al foco · según el NEC", 32, TINTA2, "MEDIUM")
        tit = VGroup(t1, t2, t3).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([2.6, 0.9, 0])
        barra = RoundedRectangle(width=1.4, height=0.1, corner_radius=0.05, stroke_width=0).set_fill(MARCA, 1)
        barra.next_to(tit, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(tit, shift=RIGHT * 0.3), GrowFromEdge(barra, LEFT), run_time=0.8)
        self.wait(0.6)
        on = foco(True, 0.9).scale(4.2).move_to(f)
        glow_ = resplandor(on[0].get_center(), 2.6, AMBAR, 12, 0.045)
        self.sfx("tic", -4)
        self.play(FadeIn(glow_), Transform(f, on), run_time=0.5)
        self.esperar_frac(0.35)
        q = VGroup(pastilla("¿por qué el interruptor corta la fase?", ENERGIA, 28),
                   pastilla("¿por qué el neutro va a la lámpara?", MARCA, 28)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        q.next_to(barra, DOWN, buff=0.5, aligned_edge=LEFT)
        self.esperar_frac(0.45)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in q], lag_ratio=0.5), run_time=1.2)
        self.cerrar_voz()
        self.limpiar(f, cordon, glow_, tit, barra, q)

    # -------------------------------------------------------------- 2 plano general
    def plano(self):
        self.voz("plano")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.play(FadeIn(self.var), FadeIn(self.pan, shift=UP * 0.2), run_time=0.8)
        e1 = pastilla("Centro de carga", TINTA, 26).move_to([-2.2, -1.2, 0])
        l1 = Line(e1.get_left(), PANEL_C + P(1.45, -0.6), stroke_color=TINTA2, stroke_width=1.2)
        self.play(FadeIn(e1), Create(l1), run_time=0.4)
        self.play(Create(self.t1), run_time=1.6)
        self.play(FadeIn(self.oc, scale=0.8), run_time=0.5)
        e2 = pastilla("Caja octagonal 4\"", TINTA, 26).move_to(OCT_C + P(0, 1.05))
        e3 = pastilla("Tubo EMT ½\"", TINTA2, 24).move_to(P(-2.6, Y_TECHO + 0.55))
        self.play(FadeIn(e2), FadeIn(e3), FadeIn(self.port), run_time=0.6)
        e4 = pastilla("Lámpara", TINTA, 26).move_to(P(1.6, 1.2))
        l4 = Line(e4.get_left(), self.port.foco.get_right(), stroke_color=TINTA2, stroke_width=1.2)
        self.play(FadeIn(e4), Create(l4), run_time=0.4)
        self.esperar_frac(0.15)
        self.play(Create(self.t2), run_time=1.6)
        self.play(FadeIn(self.cr), FadeIn(self.sw), run_time=0.5)
        e5 = pastilla("Caja 2×4 + interruptor", TINTA, 26).move_to(SW_C + P(-2.4, -1.25))
        l5 = Line(e5.get_right(), SW_C + P(-0.55, -0.5), stroke_color=TINTA2, stroke_width=1.2)
        self.play(FadeIn(e5), Create(l5), run_time=0.4)
        self.esperar_frac(0.35)
        nec = VGroup(T("NEC", 60, MARCA, "HEAVY"), T("2020 · Código Eléctrico Nacional · NFPA 70", 28, TINTA, "BOLD")).arrange(RIGHT, buff=0.3)
        nec.move_to([1.2, -3.2, 0])
        self.play(FadeIn(nec, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.etiquetas_plano = VGroup(e1, l1, e2, e3, e4, l4, e5, l5, nec)
        self.limpiar(self.etiquetas_plano)
        self.mundo = VGroup(self.var, self.pan, self.t1, self.t2, self.oc, self.cr, self.sw, self.port)

    # -------------------------------------------------------------- 3 materiales
    def materiales(self):
        self.voz("materiales")
        self.play(FadeOut(self.mundo), run_time=0.4)
        tit = T("MATERIALES", 46, TINTA, "HEAVY").move_to([0, 3.75, 0])
        self.play(FadeIn(tit), run_time=0.3)

        def icono_tubo():
            return VGroup(tubo(P(-1.0, 0), P(0.6, 0), d=0.22), conector(P(0.78, 0), 0, 0.22), abrazadera(P(-0.4, 0), d=0.22))

        def icono_cables():
            return VGroup(*[cable(P(-1.0, y), P(1.0, y), color=c, w=7) for y, c in
                            zip((0.36, 0.12, -0.12, -0.36), (FASE, NEUTRO, RETORNO, TIERRA))])

        items = [
            (lambda: breaker("15", 0.46, 0.26).scale(3.2), "Breaker 1 polo · 15 A"),
            (icono_tubo, "Tubo EMT ½\" + conectores\ny abrazaderas"),
            (lambda: caja_octagonal().scale(1.25), "Caja octagonal 4\""),
            (lambda: caja_rect().scale(0.9), "Caja rectangular 2×4"),
            (lambda: interruptor().scale(1.0), "Interruptor sencillo\n15 A"),
            (lambda: portalampara().scale(1.15), "Portalámparas\nde porcelana"),
            (icono_cables, "Cable THHN 14 AWG\n4 colores"),
            (lambda: VGroup(tuerca_empalme(P(-0.35, 0), AMBAR, 0.45), tuerca_empalme(P(0.35, 0), TIERRA, 0.45)),
             "Conectores de empalme"),
        ]
        celdas = VGroup()
        for k, (fn, nombre) in enumerate(items):
            caja = tarjeta(3.4, 3.0, METAL)
            ic = fn()
            ic.scale_to_fit_height(min(1.5, ic.height)) if ic.height > 1.5 else None
            if ic.width > 2.6:
                ic.scale_to_fit_width(2.6)
            ic.move_to(caja.get_center() + UP * 0.35)
            nm = VGroup(*[T(l, 21, TINTA, "BOLD") for l in nombre.split("\n")]).arrange(DOWN, buff=0.06)
            nm.move_to(caja.get_center() + DOWN * 1.0)
            celdas.add(VGroup(caja, ic, nm))
        celdas.arrange_in_grid(2, 4, buff=(0.35, 0.3)).move_to([0, -0.2, 0])
        dur = max(4.0, self.resta() - 1.5)
        self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.25) for c_ in celdas], lag_ratio=0.85), run_time=dur)
        self.cerrar_voz()
        self.limpiar(tit, celdas)

    # -------------------------------------------------------------- 4 colores
    def colores(self):
        self.voz("colores")
        tit = T("LOS COLORES SÍ IMPORTAN", 46, TINTA, "HEAVY").move_to([0, 3.75, 0])
        self.play(FadeIn(tit), run_time=0.3)
        filas = [
            (NEUTRO, "NEUTRO", "blanco o gris", "NEC 200.6", "#98A2B3"),
            (TIERRA, "TIERRA", "verde o desnudo", "NEC 250.119", TIERRA),
            (FASE, "FASE", "cualquier otro color (aquí: negro)", "NEC 200.7", FASE),
            (RETORNO, "RETORNO", "del interruptor a la lámpara (rojo)", "convención", RETORNO),
        ]
        grupos = VGroup()
        for k, (col, nombre, desc, ref, tc) in enumerate(filas):
            y = 2.3 - 1.25 * k
            w = cable(P(-7.0, y), P(-2.2, y), color=col, w=16)
            pel = VGroup(Polygon(P(-2.2, y + 0.08), P(-1.9, y + 0.05), P(-1.9, y - 0.05), P(-2.2, y - 0.08),
                                 stroke_width=0).set_fill(COBRE, 1))
            nm = T(nombre, 40, tc if col != NEUTRO else "#667085", "HEAVY").move_to([0.0, y + 0.18, 0], aligned_edge=LEFT)
            nm.shift(RIGHT * (-1.3 - nm.get_left()[0]))
            ds = T(desc, 24, TINTA2, "MEDIUM").next_to(nm, DOWN, buff=0.08, aligned_edge=LEFT)
            rf = pastilla(ref, MARCA if "NEC" in ref else TINTA2, 22).move_to([5.9, y, 0])
            grupos.add(VGroup(w, pel, nm, ds, rf))
        extra = cable(P(-7.0, 1.0), P(-4.8, 1.0), color="#C8773A", w=10)  # desnudo
        extra.shift(DOWN * 0.0)
        cortes = [0.0, 0.17, 0.2, 0.3]
        for k, g in enumerate(grupos):
            self.esperar_frac(cortes[k])
            self.play(Create(g[0]), FadeIn(g[1]), FadeIn(g[2], shift=RIGHT * 0.2), FadeIn(g[3]), FadeIn(g[4]), run_time=0.8)
        self.esperar_frac(0.35)
        azul = VGroup(cable(P(-3.0, 0), P(-1.2, 0), color="#2E90FA", w=14),
                      T("En las normas IEC (IEC 60445) el neutro es azul", 26, "#1570EF", "BOLD")).arrange(RIGHT, buff=0.3)
        azul.move_to([0, -3.35, 0])
        self.play(FadeIn(azul, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(tit, grupos, azul)

    # -------------------------------------------------------------- 5 seguridad
    def seguridad(self):
        self.voz("seguridad")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.play(FadeIn(self.mundo), run_time=0.5)
        self.ir(*VISTA_PANEL, 1.0)
        self.play(self.pan.principal.palanca.animate.shift(LEFT * 0.14), run_time=0.4)
        self.sfx("tic", -4)
        off = self.chip("principal: OFF", self.pan.principal.get_center() + P(0, 0.45), ROJO, 22, True)
        self.play(FadeIn(off), run_time=0.3)
        pr = probador().scale(0.9)
        objetivo = self.pan.nuestro.terminal.get_center()
        pr.rotate(-0.5).shift(objetivo - pr[1].get_vertices()[2] + P(0.9, 0.6))
        self.play(FadeIn(pr), run_time=0.3)
        self.play(pr.animate.shift(P(-0.9, -0.6)), run_time=0.6)
        cero = VGroup(display("0", "V", VERDE_OK, 60), check(VERDE_OK, 0.28)).arrange(RIGHT, buff=0.25)
        self.pant(cero, (4.5, 0.6))
        self.play(FadeIn(cero, scale=1.2), run_time=0.4)
        carta = self.carta_nec("NFPA 70E", "Verifica la ausencia de tensión\nantes de trabajar.", (4.3, 2.6), 5.0)
        self.play(FadeIn(carta, shift=LEFT * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.play(pr.animate.shift(P(0.9, 0.6)), run_time=0.3)
        self.limpiar(pr, cero, carta, off)

    # -------------------------------------------------------------- 6 tablero por dentro
    def tablero(self):
        self.voz("tablero")
        z = self.z
        marco = lambda m, col: SurroundingRectangle(m, buff=0.05, color=col, stroke_width=3, corner_radius=0.04)
        b = marco(self.pan.buses, ENERGIA)
        eb = self.chip("barras energizadas", P(-2.45, 1.15), ENERGIA, 22, True)
        lb = Line(eb.get_left(), self.pan.buses.get_right() + P(0, 0.75), stroke_color=ENERGIA, stroke_width=1.5)
        self.play(Create(b), FadeIn(eb), Create(lb), run_time=0.6)
        self.esperar_frac(0.2)
        n = marco(self.pan.neutro, "#667085")
        en = self.chip("barra de neutros (aislada)", P(-2.45, 0.35), "#475467", 22, True)
        ln = Line(en.get_left(), P(self.pan.neutro.get_right()[0] + 0.02, 0.35), stroke_color="#475467", stroke_width=1.5)
        self.play(Create(n), FadeIn(en), Create(ln), run_time=0.6)
        self.esperar_frac(0.18)
        t = marco(self.pan.tierra_b, TIERRA)
        et = self.chip("barra de tierra", P(-2.45, -1.45), TIERRA, 22, True)
        lt = Line(et.get_left(), self.pan.tierra_b.get_right() + P(0.02, 0), stroke_color=TIERRA, stroke_width=1.5)
        self.play(Create(t), FadeIn(et), Create(lt), run_time=0.6)
        self.esperar_frac(0.25)
        p_ = self.pan.puente
        ep = self.chip("puente de unión principal", P(-2.45, -2.15), TIERRA, 22)
        self.play(Indicate(p_, color="#0B7A33", scale_factor=1.15), FadeIn(ep), run_time=0.9)
        carta = self.carta_nec("NEC 250.24", "Neutro y tierra se unen solo en el\nequipo de acometida (tablero principal).",
                               (4.4, -0.35), 5.6, TIERRA)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(b, eb, lb, n, en, ln, t, et, lt, ep, carta)

    # -------------------------------------------------------------- 7 por qué 15 A
    def breaker_(self):
        self.voz("breaker")
        br = self.pan.nuestro
        self.ir(br.get_center() + P(0.9, -0.15), 3.6, 1.0)
        mrc = SurroundingRectangle(br, buff=0.04, color=MARCA, stroke_width=3, corner_radius=0.03)
        self.play(Create(mrc), run_time=0.4)
        carta = self.carta_nec("NEC 240.4(D)", "Cobre 14 AWG → protección\nmáxima de 15 A.", (4.2, 2.7), 5.0)
        self.play(FadeIn(carta, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.3)
        msg = VGroup(T("El breaker no protege al foco:", 30, TINTA, "BOLD"),
                     T("protege al CABLE", 40, MARCA, "HEAVY")).arrange(DOWN, buff=0.1)
        self.pant(msg, (4.0, 0.4))
        self.play(FadeIn(msg, shift=UP * 0.2), run_time=0.5)
        self.esperar_frac(0.35)
        # comparación: 20 A en cable 14 → se calienta
        alambre = cable(P(-5.0, 0), P(-1.0, 0), color=FASE, w=14)
        b20 = breaker("20", 0.46, 0.26).scale(2.4).next_to(alambre, LEFT, buff=0.1)
        lbl = T("14 AWG", 22, TINTA2, "BOLD").next_to(alambre, UP, buff=0.12)
        grp = VGroup(b20, alambre, lbl)
        fondo_g = tarjeta(grp.width + 0.6, grp.height + 1.2, METAL).move_to(grp).shift(UP * 0.25)
        grp = VGroup(fondo_g, b20, alambre, lbl)
        self.pant(grp, (4.0, -2.45))
        self.play(FadeIn(grp), run_time=0.4)
        calor = alambre.copy()
        for s in calor:
            s.set_stroke(color=ENERGIA)
        x = equis(ROJO, 0.3)
        self.pant(x, (7.0, -2.45))
        ondas = VGroup(*[VMobject().set_points_smoothly([P(xx, 0.2), P(xx + 0.08, 0.35), P(xx, 0.5), P(xx + 0.08, 0.65)])
                         .set_stroke(ENERGIA, 2) for xx in np.linspace(-4.4, -1.6, 5)])
        self.pant(ondas, (4.3, -2.0))
        self.play(Transform(alambre, calor), FadeIn(ondas, shift=UP * 0.1), FadeIn(x, scale=1.3), run_time=0.8)
        self.cerrar_voz()
        self.limpiar(mrc, carta, msg, grp, ondas, x)

    # -------------------------------------------------------------- 8 tubería
    def tuberia(self):
        self.voz("tubo")
        self.ir(P(0, 0.4), 15.5, 1.0)
        for k, cn in enumerate(self.cons):
            self.sfx("pop", -10)
            self.play(FadeIn(cn, scale=1.4), run_time=0.3)
        ec = self.chip("conector + contratuerca", self.cons[1].get_center() + P(-1.3, -0.7), TINTA, 22)
        self.play(FadeIn(ec), run_time=0.3)
        self.esperar_frac(0.25)
        abr = VGroup(abrazadera(P(E[0], E[1] + 0.55), True), abrazadera(P(-1.55, Y_TECHO)), abrazadera(P(-3.4, Y_TECHO)),
                     abrazadera(P(1.25, Y_TECHO)), abrazadera(P(3.3, Y_TECHO)), abrazadera(P(SW_C[0], SW_C[1] + SW_H / 2 + 0.75), True))
        self.play(LaggedStart(*[FadeIn(a, scale=1.5) for a in abr], lag_ratio=0.3), run_time=1.4)
        self.abr = abr
        y = Y_TECHO + 0.42

        def cota(x0, x1, txt, col=MARCA):
            a = DoubleArrow(P(x0, y), P(x1, y), buff=0, stroke_width=2, color=col, tip_length=0.14,
                            max_tip_length_to_length_ratio=0.15)
            t = T(txt, 22, col, "BOLD").next_to(a, UP, buff=0.08)
            return VGroup(a, t)
        c1 = cota(-1.55, OCT_C[0] - OCT_R, "≤ 90 cm")
        c2 = cota(-3.4, -1.55, "≤ 3 m")
        c3 = cota(OCT_C[0] + OCT_R, 1.25, "≤ 90 cm")
        self.play(FadeIn(c1), FadeIn(c3), run_time=0.5)
        self.play(FadeIn(c2), run_time=0.4)
        carta = self.carta_nec("NEC 358.30", "EMT: fijar a ≤ 90 cm (3 ft) de cada caja\ny luego cada ≤ 3 m (10 ft).",
                               (2.8, -2.8), 6.0)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(ec, c1, c2, c3, carta)
        self.mundo.add(self.cons, self.abr)

    # -------------------------------------------------------------- 9 cableado
    def cableado(self):
        self.voz("cableado")
        tubos = VGroup(self.t1, self.t2)
        self.play(tubos.animate.set_opacity(0.28), run_time=0.5)
        guia = VMobject().set_points_as_corners(TUBO1).set_stroke("#475467", 1.6)
        fisico(guia)
        eg = self.chip("guía", P(-4.0, Y_TECHO + 0.45), TINTA2, 22)
        self.play(Create(guia), FadeIn(eg), run_time=1.0)
        self.play(FadeOut(guia), FadeOut(eg), run_time=0.2)
        w1 = [self.c("neg_t1", 2.2), self.c("bla_t1", 2.2), self.c("ver_t1", 2.2)]
        self.play(*[Create(w) for w in w1], run_time=1.6)
        tres = self.chip("negro · blanco · verde", P(-2.4, Y_TECHO + 0.5), TINTA, 22)
        self.play(FadeIn(tres), run_time=0.3)
        self.esperar_frac(0.3)
        w2 = [self.c("neg_t2", 2.2), self.c("roj_t2", 2.2), self.c("ver_t2", 2.2)]
        self.play(*[Create(w) for w in w2], run_time=1.6)
        tres2 = self.chip("negro · rojo · verde", P(2.9, Y_TECHO + 0.5), TINTA, 22)
        self.play(FadeIn(tres2), run_time=0.3)
        self.esperar_frac(0.35)
        # colas sueltas en cada caja
        def cola(p0, d, col, curva=0.25):
            return cable(p0, p0 + d * 0.5 + P(curva, 0), p0 + d, color=col, w=2.6, suave=True)
        colas = VGroup(
            *[cola(E + P(o, 0), P(0.0, -0.75), c_, 0.15 * s) for o, c_, s in ((-0.05, FASE, -1), (0.05, NEUTRO, 1), (0.15, TIERRA, 1))],
            *[cola(OCT_C + P(-OCT_R, o), P(0.4, -0.25 + o), c_, 0.0) for o, c_ in ((-0.045, FASE), (0.0, NEUTRO), (0.045, TIERRA))],
            *[cola(OCT_C + P(OCT_R, o), P(-0.4, -0.25 + o), c_, 0.0) for o, c_ in ((0.045, FASE), (0.0, RETORNO), (-0.045, TIERRA))],
            *[cola(P(SW_C[0] + o, SW_C[1] + SW_H / 2), P(o * 4, -0.7), c_, 0.0) for o, c_ in ((0.045, FASE), (0.0, RETORNO), (-0.045, TIERRA))])
        self.play(LaggedStart(*[Create(c_) for c_ in colas], lag_ratio=0.1), tubos.animate.set_opacity(1), run_time=1.2)
        self.bring_to_front(self.t1, self.t2, self.cons, self.abr)
        self.colas = colas
        carta = self.carta_nec("NEC 300.14", "Deja al menos 15 cm (6 in) de cable\nlibre en cada caja.", (2.8, -2.8), 5.6)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tres, tres2, carta)
        self.mundo.add(*w1, *w2)

    # -------------------------------------------------------------- 10 conexiones en el tablero
    def conexiones(self):
        self.voz("conex")
        self.ir(*VISTA_PANEL, 1.0)
        self.play(FadeOut(VGroup(*self.colas[:3])), run_time=0.3)
        pares = [("neg_tab", "negro → breaker", P(-2.45, 0.2), FASE),
                 ("bla_tab", "blanco → barra de neutros", P(-2.45, -0.3), "#475467"),
                 ("ver_tab", "verde → barra de tierra", P(-2.45, -0.8), TIERRA)]
        etq = VGroup()
        for clave, txt, pos, col in pares:
            w = self.c(clave)
            e = self.chip(txt, pos, col, 20, True)
            self.play(Create(w), FadeIn(e), run_time=0.9)
            etq.add(e)
            self.mundo.add(w)
        self.tornillos_encima()
        self.esperar_frac(0.12)
        self.apretar(self.pan.nuestro.terminal, 1.0)
        carta = self.carta_nec("NEC 2020 · 110.14(D)", "Usa un medio aprobado (p. ej. torquímetro)\npara el torque que indica el fabricante.",
                               (4.1, 2.75), 5.4)
        self.play(FadeIn(carta, shift=LEFT * 0.2), run_time=0.4)
        self.esperar_frac(0.5)
        malo = VGroup(VGroup(T("flojo", 30, ENERGIA, "HEAVY"), T("se calienta", 24, TINTA2, "MEDIUM")).arrange(DOWN, buff=0.05),
                      VGroup(T("muy apretado", 30, ROJO, "HEAVY"), T("daña el cable", 24, TINTA2, "MEDIUM")).arrange(DOWN, buff=0.05)
                      ).arrange(RIGHT, buff=0.8)
        self.pant(malo, (4.1, -2.6))
        self.play(FadeIn(malo, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(etq, carta, malo)

    # -------------------------------------------------------------- 11 caja octagonal: empalmes
    def caja(self):
        self.voz("caja")
        self.ir(OCT_C + P(0.55, -0.25), 3.3, 1.2)
        self.play(FadeOut(VGroup(*self.colas[3:9])), run_time=0.3)
        n1, n2 = self.c("neg_oct_a"), self.c("neg_oct_b")
        self.play(Create(n1), Create(n2), run_time=0.8)
        nut = tuerca_empalme(OCT_C + P(0, 0.34), AMBAR, 0.15)
        self.play(FadeIn(nut, shift=DOWN * 0.1), run_time=0.3)
        self.play(Rotate(nut, PI / 10), run_time=0.15)
        self.play(Rotate(nut, -PI / 10), run_time=0.15)
        e1 = self.chip("negro + negro", OCT_C + P(1.25, 0.42), FASE, 20, True)
        self.play(FadeIn(e1), run_time=0.3)
        self.esperar_frac(0.18)
        b = self.c("bla_oct")
        e2 = self.chip("blanco → lámpara", self.port.plata.get_center() + P(-0.2, -0.32), "#475467", 20, True)
        self.play(Create(b), FadeIn(e2), run_time=0.8)
        self.esperar_frac(0.25)
        r = self.c("roj_oct")
        e3 = self.chip("rojo → lámpara", self.port.laton.get_center() + P(0.95, -0.2), RETORNO, 20, True)
        self.play(Create(r), FadeIn(e3), run_time=0.8)
        self.esperar_frac(0.3)
        v = VGroup(self.c("ver_oct_a"), self.c("ver_oct_b"), self.c("ver_oct_c"))
        nut2 = tuerca_empalme(OCT_C + P(0, -0.17), TIERRA, 0.12)
        self.play(Create(v), run_time=0.8)
        self.play(FadeIn(nut2), Indicate(self.oc.tierra, color=TIERRA), run_time=0.5)
        e4 = self.chip("verdes → tornillo de tierra", OCT_C + P(1.35, -0.45), TIERRA, 20, True)
        self.play(FadeIn(e4), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(e1, e2, e3, e4)
        self.mundo.add(n1, n2, b, r, v, nut, nut2)
        self.tornillos_encima()
        self.nuts = VGroup(nut, nut2)

    # -------------------------------------------------------------- 12 para qué la tierra
    def tierra(self):
        self.voz("tierra")
        self.ir(P(-2.2, 0.6), 11.5, 1.0)
        punto = OCT_C + P(-0.42, 0.2)
        chispa_ = rayo(OCT_C + P(-0.3, 0.12), punto, ENERGIA, 3, 0.03, 2, 2.5)
        falla = self.chip("fase pelada toca la caja", OCT_C + P(-2.1, 0.72), ROJO, 22, True)
        self.esperar_frac(0.3)
        self.sfx("pop", -4)
        self.play(FadeIn(chispa_), FadeIn(falla), run_time=0.4)
        ruta = concatenar([punto, self.oc.tierra.get_center()], inv(self.R["ver_oct_c"]), inv(self.R["ver_oct_a"]),
                          inv(self.R["ver_t1"]), inv(self.R["ver_tab"]),
                          [self.pan.tt[-1].get_center(), P(NEU_X, PANEL_C[1] - PANEL_H / 2 + 0.42),
                           P(NEU_X, self.pan.tn[0].get_center()[1])])
        fl = self.flujo(ruta, 30, ROJO, 0.045, 0.12)
        cam = self.chip("camino de baja resistencia", P(-2.6, 1.95), TIERRA, 24, True)
        self.add(fl)
        self.play(FadeIn(cam), run_time=0.4)
        self.esperar_frac(0.45)
        self.sfx("tic", -2)
        self.play(mover_palanca(self.pan.nuestro, False), run_time=0.2)
        abre = self.chip("¡el breaker se dispara!", self.pan.nuestro.get_center() + P(2.2, 0.0), ROJO, 24, True)
        self.play(FadeIn(abre, scale=1.2), run_time=0.3)
        fl.clear_updaters()
        self.play(FadeOut(fl), FadeOut(chispa_), run_time=0.4)
        carta = self.carta_nec("NEC 250.4(A)(5)", "La tierra crea un camino efectivo\npara la corriente de falla.", (4.0, -2.7), 5.4, TIERRA)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(falla, cam, abre, carta)

    # -------------------------------------------------------------- 13 relleno de caja
    def relleno(self):
        self.voz("relleno")
        self.ir(OCT_C + P(1.55, -0.55), 4.6, 1.0)
        filas = [("4 conductores × 2.00 in³", "8.00"), ("tierras (hasta 4 = 1) × 2.00 in³", "2.00")]
        tabla = VGroup()
        for a, b in filas:
            tabla.add(VGroup(T(a, 26, TINTA, "MEDIUM"), T(b + " in³", 26, TINTA, "BOLD")))
        for f in tabla:
            f[1].move_to(f[0].get_right() + RIGHT * 2.0, aligned_edge=RIGHT)
        tabla.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        for f in tabla:
            f[1].align_to(tabla, RIGHT)
        linea = Line(tabla.get_corner(DL) + DOWN * 0.15, tabla.get_corner(DR) + DOWN * 0.15, stroke_color=TINTA2, stroke_width=1.5)
        total = VGroup(T("total", 30, TINTA, "HEAVY"), T("10.00 in³", 32, MARCA, "HEAVY"))
        total.add(T("(con portalámparas como dispositivo: 14.00)", 20, TINTA2, "MEDIUM"))
        total[:2].arrange(RIGHT, buff=0.5)
        total[2].next_to(total[:2], DOWN, buff=0.1, aligned_edge=RIGHT)
        total.next_to(linea, DOWN, buff=0.2).align_to(tabla, RIGHT)
        cap = VGroup(T("caja octagonal 4\" × 1½\"", 26, TINTA, "MEDIUM"), T("15.5 in³", 32, TINTA, "HEAVY")).arrange(RIGHT, buff=0.5)
        cap.next_to(total, DOWN, buff=0.3).align_to(tabla, RIGHT)
        barra = Rectangle(width=5.6, height=0.36, stroke_color=TINTA2, stroke_width=1.5)
        lleno = Rectangle(width=5.6 * 10 / 15.5, height=0.36, stroke_width=0).set_fill(MARCA, 0.85)
        extra_ = Rectangle(width=5.6 * 4 / 15.5, height=0.36, stroke_width=0).set_fill(MARCA, 0.3)
        barra.next_to(cap, DOWN, buff=0.35).align_to(tabla, RIGHT)
        lleno.align_to(barra, LEFT).align_to(barra, DOWN)
        extra_.next_to(lleno, RIGHT, buff=0)
        cabe = VGroup(check(VERDE_OK, 0.22), T("¡Sí cabe!", 32, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.15).next_to(barra, DOWN, buff=0.25)
        tit = pastilla("NEC 2020 · 314.16 · relleno de cajas", MARCA, 24, True).next_to(tabla, UP, buff=0.35).align_to(tabla, LEFT)
        panel = VGroup(tit, tabla, linea, total, cap, barra, lleno, extra_, cabe)
        fondo_ = tarjeta(panel.width + 0.7, panel.height + 0.6, METAL).move_to(panel)
        todo = VGroup(sombra(fondo_), fondo_, panel)
        self.pant(todo, (3.6, 0.0))
        self.play(FadeIn(todo[0]), FadeIn(todo[1]), FadeIn(tit), run_time=0.4)
        self.esperar_frac(0.15)
        for k, f in enumerate(tabla):
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.4)
            self.esperar_frac(0.18)
        self.play(Create(linea), FadeIn(total), run_time=0.5)
        self.esperar_frac(0.3)
        self.play(FadeIn(cap), Create(barra), run_time=0.5)
        self.play(GrowFromEdge(lleno, LEFT), run_time=0.7)
        self.play(FadeIn(extra_), run_time=0.3)
        self.sfx("ding", -12)
        self.play(FadeIn(cabe, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(todo)

    # -------------------------------------------------------------- 14 interruptor
    def interruptor_(self):
        self.voz("interruptor")
        self.ir(SW_C + P(-1.4, 0.0), 4.4, 1.2)
        self.play(FadeOut(VGroup(*self.colas[9:])), run_time=0.3)
        trios = [("neg_sw", "negro → latón", P(4.12, 0.55), FASE),
                 ("roj_sw", "rojo → latón", P(4.12, -0.05), RETORNO),
                 ("ver_sw", "verde → tornillo verde", P(4.12, -0.65), TIERRA)]
        etq = VGroup()
        for clave, txt, pos, col in trios:
            w = self.c(clave)
            e = self.chip(txt, pos, col, 20, True)
            self.play(Create(w), FadeIn(e), run_time=0.8)
            etq.add(e)
            self.mundo.add(w)
            self.tornillos_encima()
            self.esperar_frac(0.12)
        # lupa: gancho en sentido horario
        cx = np.array([-3.2, 0.2, 0])
        lupa = Circle(radius=2.0, stroke_color=TINTA2, stroke_width=2).set_fill(WHITE, 1).move_to(cx)
        tor = tornillo(0.55, LATON, 0.5).move_to(cx)
        gancho = VMobject().set_points_smoothly([cx + P(-2.0, -1.0), cx + P(-1.0, -0.75), cx + P(-0.62, -0.25),
                                                 cx + P(-0.55, 0.25), cx + P(0, 0.62), cx + P(0.55, 0.3), cx + P(0.6, -0.15)])
        g1 = gancho.copy().set_stroke("#101318", 22)
        g2 = gancho.copy().set_stroke(COBRE, 16)
        flecha = CurvedArrow(cx + P(-0.9, 0.75), cx + P(0.95, 0.6), angle=-1.2, color=MARCA, stroke_width=4, tip_length=0.22)
        txt = VGroup(T("en sentido del reloj ↻", 26, MARCA, "HEAVY"), T("al apretar, lo jala hacia adentro", 22, TINTA2, "MEDIUM")).arrange(DOWN, buff=0.06)
        txt.next_to(lupa, DOWN, buff=0.18)
        lp = VGroup(lupa, g1, g2, tor, flecha, txt)
        lp.scale(self.z).move_to(self.camera.frame.get_center() + (cx - ORIGIN) * self.z)
        self.esperar_frac(0.1)
        self.play(FadeIn(lp[0]), FadeIn(lp[3]), run_time=0.4)
        self.play(Create(lp[1]), Create(lp[2]), run_time=0.9)
        self.play(Create(lp[4]), FadeIn(lp[5]), run_time=0.6)
        self.play(Rotate(lp[3][1], PI), run_time=0.6)
        self.apretar(self.sw.l1, 0.8)
        self.cerrar_voz()
        self.limpiar(etq, lp)

    # -------------------------------------------------------------- 14b neutro en la caja del interruptor (404.2(C))
    def neutro_sw(self):
        self.voz("neutro_sw")
        self.ir(SW_C + P(-1.6, 0.4), 6.0, 1.0)
        fantasma = DashedVMobject(VMobject().set_points_as_corners(
            [P(SW_C[0] + 0.09, Y_TECHO), P(SW_C[0] + 0.09, SW_C[1] + SW_H / 2), P(SW_C[0] + 0.25, SW_C[1] + 0.2)]),
            num_dashes=22).set_stroke("#98A2B3", 3)
        fisico(fantasma)
        en = self.chip("neutro (blanco)", P(SW_C[0] - 1.25, SW_C[1] + 1.35), "#475467", 22, True)
        self.play(Create(fantasma), FadeIn(en), run_time=0.9)
        smart = interruptor_inteligente().scale(1.5)
        txt = T("interruptor inteligente", 30, MARCA, "HEAVY")
        nec = T("necesita neutro para funcionar", 24, TINTA2, "MEDIUM")
        grupo = VGroup(smart, txt, nec).arrange(DOWN, buff=0.22)
        self.pant(grupo, (-4.0, 1.3))
        self.play(FadeIn(grupo[:2], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(nec), run_time=0.4)
        self.esperar_frac(0.35)
        exc = self.carta_nec("NEC 2020 · 404.2(C)", "Neutro en la caja del interruptor (baños,\npasillos, habitaciones). Excepción: si llega\npor tubería con espacio para agregarlo.",
                             (-3.0, -2.75), 6.4)
        self.play(FadeIn(exc, shift=UP * 0.2), Indicate(self.t2, color=MARCA, scale_factor=1.0), run_time=0.8)
        ok = self.chip("nuestro caso: tubo EMT ✓", P(SW_C[0] - 1.35, 1.6), VERDE_OK, 22, True)
        self.play(FadeIn(ok, scale=1.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(fantasma, en, grupo, exc, ok)

    # -------------------------------------------------------------- 15 lámpara (corte del portalámparas)
    def corte_portalampara(self):
        g = VGroup()
        cuerpo = Polygon(P(-1.6, 1.4), P(1.6, 1.4), P(1.25, -1.9), P(-1.25, -1.9), stroke_color=METAL2, stroke_width=2)
        cuerpo.set_fill(PORCELANA, 1)
        hueco = Rectangle(width=1.6, height=2.6, stroke_width=0).set_fill(WHITE, 1).move_to(P(0, -0.6))
        rosca_ = VGroup(*[VMobject().set_points_as_corners([P(s * 0.8, 0.7 - 0.25 * k), P(s * 0.92, 0.58 - 0.25 * k),
                                                             P(s * 0.8, 0.45 - 0.25 * k)]).set_stroke("#98A2B3", 5)
                          for s in (-1, 1) for k in range(8)])
        centro = RoundedRectangle(width=0.5, height=0.18, corner_radius=0.05, stroke_color="#8A6D12", stroke_width=1.5).set_fill(LATON, 1)
        centro.move_to(P(0, 0.62))
        tp = tornillo(0.16, "#E4E7EC", 0.4).move_to(P(-1.25, 1.0))
        tl = tornillo(0.16, LATON, 0.4).move_to(P(1.25, 1.0))
        ip = Line(P(-1.1, 1.0), P(-0.86, 0.6), stroke_color="#98A2B3", stroke_width=5)
        il = VMobject().set_points_as_corners([P(1.1, 1.0), P(0.6, 1.0), P(0.0, 0.72)]).set_stroke(LATON, 5)
        wb = cable(P(-3.4, 1.9), P(-1.6, 1.9), P(-1.3, 1.1), color=NEUTRO, w=9)
        wr = cable(P(3.4, 1.9), P(1.6, 1.9), P(1.3, 1.1), color=RETORNO, w=9)
        f = foco(False, 0.9).scale(2.6).move_to(P(0, -1.9))
        g.add(f, cuerpo, hueco, rosca_, centro, ip, il, tp, tl, wb, wr)
        g.rosca, g.centro, g.foco = rosca_, centro, f
        return g

    def lampara(self):
        self.voz("lampara")
        self.ir(P(OCT_C[0], LAMP_TOP - 0.55), 3.2, 1.0)
        self.esperar_frac(0.12)
        self.ir(ORIGIN, 16, 0.6, FadeOut(self.mundo))
        corte = self.corte_portalampara().scale(1.3).move_to([-3.6, -0.3, 0])
        self.corte = corte
        tit = T("Portalámparas por dentro", 36, TINTA, "HEAVY").move_to([3.4, 3.4, 0])
        self.play(FadeIn(corte, shift=UP * 0.2), FadeIn(tit), run_time=0.7)
        ec = pastilla("contacto central (al fondo)", "#8A6D12", 26).move_to([3.4, 1.9, 0])
        lc = Line(ec.get_left(), corte.centro.get_right(), stroke_color="#8A6D12", stroke_width=1.5)
        self.play(FadeIn(ec), Create(lc), Indicate(corte.centro, color=AMBAR), run_time=0.8)
        self.esperar_frac(0.15)
        er = pastilla("rosca (la que puedes tocar)", "#667085", 26).move_to([3.4, 0.6, 0])
        lr = Line(er.get_left(), corte.rosca.get_right() + P(0, 0.2), stroke_color="#667085", stroke_width=1.5)
        self.play(FadeIn(er), Create(lr), Indicate(corte.rosca, color="#475467"), run_time=0.8)
        self.esperar_frac(0.3)
        r1 = VGroup(T("NEUTRO (blanco)", 32, "#475467", "HEAVY"), T("→  rosca", 32, TINTA, "BOLD")).arrange(RIGHT, buff=0.25)
        r2 = VGroup(T("RETORNO (rojo)", 32, RETORNO, "HEAVY"), T("→  centro", 32, TINTA, "BOLD")).arrange(RIGHT, buff=0.25)
        rr = VGroup(r1, r2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, -1.05, 0])
        self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=0.5)
        self.esperar_frac(0.4)
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.5)
        carta = self.carta_nec("NEC 410.90", "El conductor puesto a tierra (neutro)\nse conecta a la rosca.", (3.4, -3.0), 5.6)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, ec, lc, er, lr, rr, carta)

    # -------------------------------------------------------------- 16 por qué la rosca
    def rosca(self):
        self.voz("rosca")
        corte = self.corte
        dedo = VGroup(RoundedRectangle(width=2.4, height=0.55, corner_radius=0.27, stroke_color=LINEA, stroke_width=1.5).set_fill(PIEL, 1),
                      RoundedRectangle(width=0.4, height=0.36, corner_radius=0.12, stroke_color="#C9A27E", stroke_width=1).set_fill("#F8DCC4", 1).shift(LEFT * 0.85))
        dedo.move_to(corte.rosca.get_left() + P(-1.4, -0.4))
        self.play(FadeIn(dedo, shift=RIGHT * 0.4), run_time=0.6)
        self.play(dedo.animate.shift(RIGHT * 0.25), run_time=0.4)
        mal = VGroup(equis(ROJO, 0.3), T("si fuera fase: 120 V en tus dedos", 28, ROJO, "HEAVY")).arrange(RIGHT, buff=0.2)
        mal.move_to([3.3, 1.2, 0])
        self.esperar_frac(0.25)
        self.play(FadeIn(mal, shift=LEFT * 0.2), run_time=0.5)
        self.esperar_frac(0.5)
        bien = VGroup(check(VERDE_OK, 0.3), T("con el neutro: ≈ 0 V", 32, VERDE_OK, "HEAVY")).arrange(RIGHT, buff=0.2)
        bien.move_to([3.0, -0.3, 0])
        self.play(FadeIn(bien, shift=LEFT * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(corte, dedo, mal, bien)

    # -------------------------------------------------------------- 17 la regla de oro (comparación)
    def mini_circuito(self, corta_fase=True):
        g = VGroup()
        fuente_ = RoundedRectangle(width=1.1, height=2.4, corner_radius=0.08, stroke_color=METAL_OSC, stroke_width=1.6).set_fill(GAL, 1)
        fuente_.move_to(P(-2.6, 0))
        lf = T("F", 24, FASE, "HEAVY").move_to(P(-2.6, 0.7))
        ln = T("N", 24, "#667085", "HEAVY").move_to(P(-2.6, -0.7))
        yF, yN = 0.7, -0.7
        # interruptor (abierto) en F o en N
        ys = yF if corta_fase else yN
        a, b = P(-0.6, ys), P(0.2, ys)
        cuchilla = Line(a, a + P(0.72, 0.42), stroke_color=TINTA, stroke_width=4)
        bornes = VGroup(Dot(a, radius=0.06, color=TINTA), Dot(b, radius=0.06, color=TINTA))
        fF = [P(-2.05, yF), P(1.6, yF), P(1.6, 0.35)] if not corta_fase else None
        tramos = VGroup()
        if corta_fase:
            tramos.add(cable(P(-2.05, yF), a, color=FASE, w=6), cable(b, P(1.6, yF), P(1.6, 0.35), color=FASE, w=6),
                       cable(P(-2.05, yN), P(1.6, yN), P(1.6, -0.35), color=NEUTRO, w=6))
        else:
            tramos.add(cable(P(-2.05, yF), P(1.6, yF), P(1.6, 0.35), color=FASE, w=6),
                       cable(P(-2.05, yN), a, color=NEUTRO, w=6), cable(b, P(1.6, yN), P(1.6, -0.35), color=NEUTRO, w=6))
        sock = Rectangle(width=0.5, height=0.7, stroke_color=METAL_OSC, stroke_width=1.2).set_fill(METAL, 1).move_to(P(1.6, 0))
        f = foco(False, 1.1).rotate(PI / 2)
        f.next_to(sock, RIGHT, buff=-0.1)
        g.add(fuente_, lf, ln, tramos, sock, f, cuchilla, bornes)
        g.sock, g.tramos = sock, tramos
        return g

    def regla(self):
        self.voz("regla")
        tit = VGroup(T("LA REGLA DE ORO:", 40, TINTA, "HEAVY"), T("el interruptor corta la FASE", 40, ENERGIA, "HEAVY")).arrange(RIGHT, buff=0.3)
        tit.move_to([0, 3.7, 0])
        self.play(FadeIn(tit, shift=DOWN * 0.2), run_time=0.5)
        A = self.mini_circuito(True).scale(1.08).move_to([-4.0, 0.35, 0])
        B = self.mini_circuito(False).scale(1.08).move_to([4.0, 0.35, 0])
        tA = pastilla("CORRECTO: corta la fase", VERDE_OK, 26, True).move_to([-4.0, 2.4, 0])
        tB = pastilla("INCORRECTO: corta el neutro", ROJO, 26, True).move_to([4.0, 2.4, 0])
        div = DashedLine([0, 2.8, 0], [0, -3.3, 0], stroke_color=METAL2, stroke_width=1.5)
        self.esperar_frac(0.12)
        self.play(FadeIn(A), FadeIn(tA), Create(div), run_time=0.7)
        self.esperar_frac(0.25)
        okA = VGroup(T("lámpara sin tensión", 26, VERDE_OK, "BOLD"), display("0", "V", VERDE_OK, 44)).arrange(RIGHT, buff=0.25)
        okA.move_to([-4.0, -1.75, 0])
        self.play(FadeIn(okA), run_time=0.4)
        self.esperar_frac(0.2)
        self.play(FadeIn(B), FadeIn(tB), run_time=0.7)
        self.esperar_frac(0.3)
        viva = B.tramos[0].copy()
        for s in viva:
            s.set_stroke(color=ENERGIA)
        brillo = SurroundingRectangle(B.sock, buff=0.08, color=ROJO, stroke_width=4, corner_radius=0.06)
        malB = VGroup(T("foco apagado, pero…", 26, ROJO, "BOLD"), display("120", "V", ROJO, 44)).arrange(RIGHT, buff=0.25)
        malB.move_to([4.0, -1.75, 0])
        self.sfx("pop", -6)
        self.play(Transform(B.tramos[0], viva), Create(brillo), FadeIn(malB), run_time=0.7)
        self.play(Indicate(brillo, color=ROJO), run_time=0.6)
        self.esperar_frac(0.4)
        carta = self.carta_nec("NEC 404.2(B)", "Los interruptores no deben desconectar\nel conductor puesto a tierra (neutro).", (0, -3.3), 7.0, ROJO)
        self.play(FadeIn(carta, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(tit, A, B, tA, tB, div, okA, malB, brillo, carta)

    # -------------------------------------------------------------- 17b pruebas antes de energizar
    def pruebas(self):
        self.voz("pruebas")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        tit = T("PRUEBA ANTES DE ENERGIZAR", 44, TINTA, "HEAVY").move_to([0, 3.75, 0])
        mm = multimetro().scale(1.05).move_to([-5.0, -0.2, 0])
        self.play(FadeIn(tit), FadeIn(mm, shift=RIGHT * 0.3), run_time=0.6)
        # extremos sueltos en el tablero
        ext = {}
        for k, (col, y, nom) in enumerate(((FASE, 1.4, "negro"), (NEUTRO, 0.2, "blanco"), (TIERRA, -1.0, "verde"))):
            w = cable(P(5.6, y), P(0.9, y), color=col, w=10)
            w.add(punta_pelada(w.ruta, 0.35, 10))
            et = T(nom, 26, TINTA if col != NEUTRO else "#667085", "BOLD").next_to(w, RIGHT, buff=0.15).shift(LEFT * 0.0)
            et.move_to(P(6.3, y))
            ext[nom] = (w, et, P(0.62, y))
        self.play(*[FadeIn(VGroup(w, e)) for w, e, _ in ext.values()], run_time=0.5)
        lect = Text("", font=MONO).move_to(mm.lcd)

        def lectura(txt, color="#1D2939"):
            return T(txt, 40, color, "HEAVY", MONO).scale_to_fit_height(0.32).move_to(mm.lcd)

        roja, negra = punta_prueba(ROJO), punta_prueba("#2A2E35")
        roja.move_to([-2.2, 2.2, 0]).rotate(-0.5)
        negra.move_to([-2.2, -2.4, 0]).rotate(0.5)
        cr = always_redraw(lambda: VMobject().set_points_smoothly([mm.borne_v.get_center(), mm.borne_v.get_center() + DOWN * 0.8 + RIGHT * 1.2,
                                                                   roja[0].get_bottom() + DOWN * 0.1 + LEFT * 0.5, roja[0].get_bottom()]).set_stroke(ROJO, 3))
        cn = always_redraw(lambda: VMobject().set_points_smoothly([mm.borne_com.get_center(), mm.borne_com.get_center() + DOWN * 1.0 + RIGHT * 0.8,
                                                                   negra[0].get_bottom() + DOWN * 0.3 + LEFT * 0.6, negra[0].get_bottom()]).set_stroke("#2A2E35", 3))
        self.add(cr, cn)
        self.play(FadeIn(roja), FadeIn(negra), run_time=0.4)

        def tocar(a, b, txt, color, nota, nota_col, extra=None):
            pa, pb = ext[a][2], ext[b][2]
            self.play(roja.animate.shift(pa - roja.tip.get_bottom()), negra.animate.shift(pb - negra.tip.get_bottom()), run_time=0.6)
            l = lectura(txt, color)
            n = pastilla(nota, nota_col, 26, True).move_to([2.6, -2.75, 0])
            anims = [FadeIn(l), FadeIn(n, scale=1.1)]
            if extra is not None:
                anims.append(FadeIn(extra))
            self.play(*anims, run_time=0.4)
            return l, n

        self.esperar_frac(0.12)
        l1, n1 = tocar("negro", "blanco", "OL", "#1D2939", "negro–blanco: abierto · sin corto ✓", VERDE_OK)
        self.esperar_frac(0.2)
        self.play(FadeOut(l1), FadeOut(n1), run_time=0.2)
        l2, n2 = tocar("negro", "verde", "OL", "#1D2939", "negro–verde: abierto · sin falla a tierra ✓", VERDE_OK)
        self.esperar_frac(0.25)
        self.play(FadeOut(l2), FadeOut(n2), run_time=0.2)
        cond = pastilla("con foco y el interruptor arriba", AMBAR, 24).move_to([2.6, 2.75, 0])
        self.play(FadeIn(cond), run_time=0.3)
        l3, n3 = tocar("negro", "blanco", "Ω bajo", VERDE_OK, "marca la resistencia del filamento ✓", VERDE_OK)
        self.esperar_frac(0.4)
        cond2 = pastilla("interruptor abajo", TINTA2, 24).move_to([2.6, 2.75, 0])
        l4 = lectura("OL", "#1D2939")
        self.play(Transform(cond, cond2), Transform(l3, l4), run_time=0.4)
        self.cerrar_voz()
        cr.clear_updaters()
        cn.clear_updaters()
        self.limpiar(tit, mm, roja, negra, cr, cn, l3, n3, cond, *[VGroup(w, e) for w, e, _ in ext.values()])

    # -------------------------------------------------------------- 18 encender
    def encender(self):
        self.voz("encender")
        self.camera.frame.set(width=16).move_to(P(0, 0.2))
        # restituir el breaker (quedó disparado en la escena de la tierra)
        self.pan.nuestro.palanca.move_to(self.pan.nuestro[1].get_center() + RIGHT * self.pan.nuestro[0].width * 0.08 * -1)
        self.play(FadeIn(self.mundo), run_time=0.6)
        placa = RoundedRectangle(width=0.82, height=1.3, corner_radius=0.06, stroke_color=METAL2, stroke_width=1.4).set_fill("#FBFBFA", 1)
        placa.move_to(SW_C + P(-0.08, 0))
        pal = RoundedRectangle(width=0.14, height=0.32, corner_radius=0.05, stroke_color=LINEA, stroke_width=1).set_fill(WHITE, 1)
        pal.move_to(placa.get_center() + P(0, -0.12))
        tor = VGroup(tornillo(0.035, METAL, 0.3).move_to(placa.get_center() + P(0, 0.45)),
                     tornillo(0.035, METAL, 0.3).move_to(placa.get_center() + P(0, -0.45)))
        tapa_sw = VGroup(placa, pal, tor)
        tapa_p = Rectangle(width=PANEL_W - 0.3, height=PANEL_H - 0.3, stroke_color=METAL_OSC, stroke_width=1.4).set_fill("#DDE1E7", 1)
        tapa_p.move_to(PANEL_C)
        hueco = Rectangle(width=1.0, height=2.25, stroke_color=METAL_OSC, stroke_width=1).set_fill(opacity=0).move_to(PANEL_C + P(-0.05, 0.25))
        tapa_oct = Circle(radius=OCT_R * 0.98, stroke_color=METAL_OSC, stroke_width=1.2).set_fill("#F0F2F5", 1).move_to(OCT_C)
        # la tapa del tablero deja ver los breakers (frente muerto)
        self.play(FadeIn(tapa_sw), run_time=0.5)
        self.play(FadeIn(tapa_oct), run_time=0.4)
        brks = VGroup(self.pan.principal, self.pan[7]).copy()
        self.play(FadeIn(tapa_p), FadeIn(hueco), FadeIn(brks), run_time=0.5)
        self.esperar_frac(0.05)
        principal_on = brks[0][2].animate.shift(RIGHT * 0.14)
        nuestro = brks[1][1] if False else None
        self.sfx("tic", -4)
        self.play(principal_on, run_time=0.3)
        nb = brks[1][1]
        self.play(nb[2].animate.move_to(nb[1].get_center() + RIGHT * nb[0].width * 0.08), run_time=0.3)
        self.sfx("tic", -4)
        self.play(pal.animate.shift(UP * 0.24), run_time=0.3)
        on = foco(True, 0.85).move_to(self.port.foco)
        glow_ = resplandor(self.port.foco[0].get_center(), 1.4, AMBAR, 12, 0.05)
        self.play(Transform(self.port.foco, on), FadeIn(glow_), run_time=0.4)
        R = self.R
        sw = self.sw
        ruta = concatenar(inv(R["neg_tab"]), R["neg_t1"], R["neg_oct_a"], inv(R["neg_oct_b"]), R["neg_t2"], R["neg_sw"],
                          [sw.l1.get_center(), sw.l2.get_center()], inv(R["roj_sw"]), inv(R["roj_t2"]), R["roj_oct"],
                          [self.port.laton.get_center(), self.port.foco[0].get_center(), self.port.plata.get_center()],
                          inv(R["bla_oct"]), inv(R["bla_t1"]), R["bla_tab"])
        fl = self.flujo(ruta, 60, ENERGIA, 0.05, 0.05)
        self.add(fl)
        pasos = [("1 · fase del tablero", P(-2.4, 1.0)), ("2 · breaker", P(-2.4, 0.5)), ("3 · baja al interruptor", P(-2.4, 0.0)),
                 ("4 · regresa por el rojo", P(-2.4, -0.5)), ("5 · atraviesa el foco", P(-2.4, -1.0)),
                 ("6 · vuelve por el neutro", P(-2.4, -1.5))]
        lista = VGroup(*[T(t, 26, TINTA, "BOLD").move_to(p, aligned_edge=LEFT) for t, p in pasos])
        lista.move_to([1.6, -2.3, 0]).arrange(DOWN, buff=0.12, aligned_edge=LEFT).shift(RIGHT * 0.2)
        lista.arrange_in_grid(3, 2, buff=(0.6, 0.15), flow_order="dr").move_to([1.4, -2.6, 0])
        dur = max(2.0, self.resta() - 0.6)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in lista], lag_ratio=0.9), run_time=dur)
        self.cerrar_voz()
        fl.clear_updaters()
        self.encendido = VGroup(fl, glow_, tapa_sw, tapa_oct, tapa_p, hueco, brks)
        self.limpiar(lista, self.encendido, self.mundo)

    # -------------------------------------------------------------- 19 errores comunes
    def errores(self):
        self.voz("errores")
        self.camera.frame.set(width=16).move_to(ORIGIN)
        tit = T("3 ERRORES MUY COMUNES", 46, TINTA, "HEAVY").move_to([0, 3.7, 0])
        self.play(FadeIn(tit), run_time=0.4)
        cartas = VGroup()
        textos = [("1", "Interruptor en el neutro", "la lámpara se apaga,\npero sigue energizada", "NEC 404.2(B)"),
                  ("2", "Breaker más grande", "el problema se esconde\ny el cable se calienta", "NEC 240.4(D)"),
                  ("3", "Empalme con solo cinta", "usa conectores identificados\npara empalmes", "NEC 110.14(B)")]
        ilus = []
        # 1: mini esquema
        i1 = VGroup(cable(P(-1.1, 0.3), P(0.7, 0.3), color=FASE, w=5), cable(P(-1.1, -0.3), P(-0.2, -0.3), color=NEUTRO, w=5),
                    Line(P(-0.2, -0.3), P(0.25, 0.0), stroke_color=TINTA, stroke_width=3),
                    cable(P(0.3, -0.3), P(0.7, -0.3), color=NEUTRO, w=5),
                    Rectangle(width=0.3, height=0.8, stroke_color=ROJO, stroke_width=3).set_fill(METAL, 1).move_to(P(0.85, 0)),
                    T("120 V", 20, ROJO, "HEAVY").move_to(P(0.85, 0.65)))
        # 2: breaker 20 + cable caliente
        i2 = VGroup(breaker("20", 0.46, 0.26).scale(2.0).move_to(P(-0.8, 0)), cable(P(-0.3, 0), P(1.2, 0), color=ENERGIA, w=9),
                    *[VMobject().set_points_smoothly([P(x, 0.15), P(x + 0.06, 0.3), P(x, 0.45), P(x + 0.06, 0.6)]).set_stroke(ENERGIA, 2)
                      for x in (0.0, 0.4, 0.8)])
        # 3: torcido + cinta  vs  conector
        tor = VGroup(*[VMobject().set_points_smoothly([P(-1.2, 0.08 * s), P(-0.8, -0.08 * s), P(-0.4, 0.08 * s), P(-0.1, -0.05 * s)])
                       .set_stroke(c_, 5) for s, c_ in ((1, FASE), (-1, FASE))])
        cinta = Rectangle(width=0.55, height=0.32, stroke_width=0).set_fill("#101318", 1).move_to(P(-0.5, 0))
        bueno = VGroup(cable(P(0.3, -0.35), P(0.62, 0.0), color=FASE, w=5), cable(P(0.95, -0.35), P(0.7, 0.0), color=FASE, w=5),
                       tuerca_empalme(P(0.66, 0.15), AMBAR, 0.36))
        i3 = VGroup(tor, cinta, equis(ROJO, 0.16).move_to(P(-0.5, 0.45)), bueno, check(VERDE_OK, 0.16).move_to(P(1.1, 0.4)))
        ilus = [i1, i2, i3]
        for (num, t1, t2, ref), il in zip(textos, ilus):
            caja = tarjeta(4.7, 5.6, METAL)
            n = VGroup(Circle(radius=0.32, stroke_width=0).set_fill(ROJO, 1), T(num, 30, WHITE, "HEAVY"))
            n[1].move_to(n[0])
            n.move_to(caja.get_top() + DOWN * 0.55)
            a = T(t1, 28, TINTA, "HEAVY").next_to(n, DOWN, buff=0.25)
            il.move_to(caja.get_center() + DOWN * 0.1)
            il.scale_to_fit_width(3.5)
            if il.height > 1.6:
                il.scale_to_fit_height(1.6)
            b = VGroup(*[T(l, 22, TINTA2, "MEDIUM") for l in t2.split("\n")]).arrange(DOWN, buff=0.06)
            b.move_to(caja.get_center() + DOWN * 1.55)
            r = pastilla(ref, MARCA, 20).move_to(caja.get_bottom() + UP * 0.45)
            cartas.add(VGroup(caja, n, a, il, b, r))
        cartas.arrange(RIGHT, buff=0.35).move_to([0, -0.5, 0])
        cortes = [0.02, 0.32, 0.38]
        for k, c_ in enumerate(cartas):
            self.esperar_frac(cortes[k])
            self.sfx("pop", -10)
            self.play(FadeIn(c_, shift=UP * 0.3), run_time=0.6)
        self.cerrar_voz()
        self.limpiar(tit, cartas)

    # -------------------------------------------------------------- 20 cierre
    def cierre(self):
        self.voz("cierre")
        tit = T("EN RESUMEN", 46, TINTA, "HEAVY").move_to([-3.4, 3.2, 0])
        reglas = ["Neutro blanco → a la rosca", "El interruptor corta la FASE", "Breaker 15 A para calibre 14",
                  "Tierra en todas las partes metálicas"]
        filas = VGroup(*[VGroup(check(VERDE_OK, 0.24), T(r, 32, TINTA, "BOLD")).arrange(RIGHT, buff=0.3) for r in reglas])
        filas.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-3.0, 0.3, 0])
        tit.align_to(filas, LEFT)
        self.play(FadeIn(tit), run_time=0.3)
        frac = self.resta() * 0.45 / 4
        for f in filas:
            self.play(FadeIn(f, shift=RIGHT * 0.2), run_time=0.4)
            if frac > 0.45:
                self.wait(frac - 0.4)
        logo = ImageMobject(str(DIR / "logo_me.png")).scale_to_fit_height(2.2).move_to([4.4, 1.2, 0])
        usuario = T("@miguelesquit", 34, MARCA, "HEAVY").next_to(logo, DOWN, buff=0.3)
        sus = pastilla("SUSCRÍBETE", ROJO, 34, True).next_to(usuario, DOWN, buff=0.35)
        self.play(FadeIn(logo, scale=0.8), FadeIn(usuario), run_time=0.5)
        self.play(FadeIn(sus, scale=1.3), run_time=0.4)
        self.esperar_frac(0.5)
        aviso = VGroup(simbolo_rayo(ENERGIA, 0.4), T("Si no estás calificado, llama a un electricista.", 28, TINTA, "BOLD")).arrange(RIGHT, buff=0.2)
        aviso.move_to([0, -3.1, 0])
        self.play(FadeIn(aviso, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.5)
        # pantalla final (end screen de YouTube: 5–20 s)
        self.play(FadeOut(VGroup(tit, filas, usuario, sus, aviso)), FadeOut(logo), run_time=0.6)
        sig = T("Mira también", 40, TINTA, "HEAVY").move_to([-3.6, 3.1, 0])
        cajas = VGroup(*[RoundedRectangle(width=5.6, height=3.15, corner_radius=0.2, stroke_color=METAL2, stroke_width=2)
                         .set_fill(GAL2, 1) for _ in range(2)]).arrange(DOWN, buff=0.45).move_to([-3.6, -0.6, 0])
        lg = ImageMobject(str(DIR / "logo_letras.png")).scale_to_fit_width(2.6).move_to([4.2, 1.0, 0])
        us = T("@miguelesquit", 34, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        sb = pastilla("SUSCRÍBETE", ROJO, 34, True).next_to(us, DOWN, buff=0.35)
        self.play(FadeIn(sig), FadeIn(cajas, shift=UP * 0.2), FadeIn(lg, scale=0.8), FadeIn(us), FadeIn(sb), run_time=0.8)
        objetivo = max(486.0, self.renderer.time + 15.0)
        self.wait(objetivo - self.renderer.time)

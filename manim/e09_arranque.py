"""E09 · H23 · MI PRIMER ARRANQUE CON CONTACTORES · Sigue el diagrama borne por borne (horizontal, 8+ min).
Guion y fuentes: e09_guion.py · piezas recreadas de documentación oficial: piezas_siemens.py
Render: FORMATO=h VOZ=eleven manim -qh --disable_caching -o final_e09 e09_arranque.py Arranque1
Previa por secciones: SOLO=potencia,control FORMATO=h VOZ=eleven manim -ql ...
"""
from e06b_contactor import *
from piezas_siemens import *
from piezas_vfd import multimetro_cat, punta, motor_tefc, girar_eje
from piezas_proteccion import palanca_breaker, VERDE_ON
from e09_guion import GUION as G9, SECCIONES as S9

AMB = "#FDB022"
CIAN = "#6FF2FF"
S_TAB = 0.45          # escala del tablero


def lampara_sim(ref="H1", color=SIM, sw=SW_MAN):
    c = Circle(radius=0.26, stroke_color=color, stroke_width=sw)
    x = VGroup(Line(c.point_at_angle(PI / 4), c.point_at_angle(PI * 5 / 4)), Line(c.point_at_angle(PI * 3 / 4), c.point_at_angle(-PI / 4))).set_stroke(color, sw * 0.8)
    a = Line(UP * 0.26, UP * 0.55).set_stroke(color, sw)
    b = Line(DOWN * 0.26, DOWN * 0.55).set_stroke(color, sw)
    r = T(ref, 18, color, "HEAVY").next_to(c, LEFT, buff=0.12)
    g = VGroup(a, c, x, b, r)
    g.circ = c
    return g


def termico_na(ref="F2", color=SIM, largo=0.9):
    c = contacto(True, largo=largo, color=color, n1="97", n2="98")
    p = c.cuchilla.get_center()
    dl = DashedLine(p, p + LEFT * 0.36, dash_length=0.05).set_stroke(color, 2.2)
    esc = VMobject().set_points_as_corners([p + LEFT * 0.36 + UP * 0.1, p + LEFT * 0.48 + UP * 0.1, p + LEFT * 0.48 + DOWN * 0.1, p + LEFT * 0.6 + DOWN * 0.1]).set_stroke(color, 2.6)
    c.add(dl, esc)
    return c


def multimetro_ohm(s=1.0, lectura="OL"):
    """Multímetro (mismo dibujo del canal) con el selector en Ω."""
    m = multimetro_cat(s, lectura)
    uni = T("Ω", 9 * s, "#101828", "HEAVY").move_to(m[4])
    m[4].become(uni)
    m[6].rotate(1.23, about_point=m[5].get_center())
    return m


def pantalla_mm(m, texto):
    nuevo = Tm(texto, 22 * m.height / 3.1, "#101828", "BOLD").move_to(m.dig)
    return Transform(m.dig, nuevo)


class Arranque1(ContactorB):
    CARPETA_VOZ = "voz_e09"
    GUION = G9
    SECC = S9
    DURACION_MIN = 482.0

    def construct(self):
        self.cinta_act = None
        self.paso_act = None
        orden = ["gancho", "materiales", "dimension", "leer", "potencia", "control", "pruebas", "energizar", "errores", "final"]
        solo = os.environ.get("SOLO")
        self.armar_tablero()
        for paso in orden:
            if solo and paso not in solo.split(","):
                continue
            getattr(self, "f_" + paso)()

    # ================================================================ tablero (se arma una sola vez)
    def armar_tablero(self):
        s = S_TAB
        fondo = RoundedRectangle(width=9.0, height=10.0, corner_radius=0.12, stroke_color="#4A5568", stroke_width=3).set_fill("#2A3140", 1).move_to([3.35, -0.35, 0])
        placa = Rectangle(width=8.6, height=9.6, stroke_color="#8A929E", stroke_width=1.2).set_fill("#BFC5CD", 1).move_to(fondo)
        tornillos = VGroup(*[tornillo_frente(0.06).move_to(placa.get_corner(c) + (-c) * 0.18) for c in (UL, UR, DL, DR)])
        d1 = canaleta(8.2, 30, s).move_to([3.15, 3.95, 0])
        d2 = canaleta(8.2, 30, s).move_to([3.15, 0.285, 0])
        d3 = canaleta(8.2, 30, s).move_to([3.15, -4.175, 0])
        dv = canaleta(8.9, 30, s, vertical=True).move_to([7.25, -0.1, 0])
        r1 = riel_din(7.6, s).move_to([3.15, 2.115, 0])
        r2 = riel_din(7.6, s).move_to([3.15, -1.225, 0])
        q1 = breaker_din(3, 15, "C", s=s, ref="Q1").move_to([0.35, 2.115, 0])
        f1 = breaker_din(2, 6, "C", s=s, ref="F1").move_to([1.95, 2.115, 0])
        t1 = fuente_24v(s * 0.92).move_to([3.7, 2.115, 0])
        for b_ in (q1, f1):      # se cablea SIEMPRE sin tensión: palancas abajo (OFF, ventana verde)
            b_.palanca.move_to(b_.ranura.get_center() + DOWN * 0.22 * b_.s)
            b_.ventana.set_fill(VERDE_ON, 1)
            b_.on = False
        arr = arrancador_s00(s, (3.5, 5.0), 3.9)
        arr.move_to([0.75, 0, 0])
        arr.shift(UP * (-0.5 - arr.ct[1].get_top()[1]))
        x1 = bornera(["1", "2", "3", "4", "5", "U", "V", "W", "PE"], s, pe=("PE",)).move_to([4.5, -1.225, 0])
        rot_q1 = tx("-Q1", 0.2, "#101828").next_to(q1, UP, buff=0.05)
        rot_f1 = tx("-F1", 0.2, "#101828").next_to(f1, UP, buff=0.05)
        pe_bar = VGroup(Rectangle(width=1.5, height=0.16, stroke_width=0).set_fill(LATON, 1),
                        *[tornillo_frente(0.05).move_to([x, 0, 0]) for x in np.linspace(-0.6, 0.6, 5)]).move_to([5.9, 1.3, 0])
        pe_lab = VGroup(tierra_icono(0.22), tx("PE", 0.16, "#101828")).arrange(RIGHT, buff=0.06).next_to(pe_bar, UP, buff=0.08)
        self.tab = VGroup(fondo, placa, tornillos, r1, r2, q1, f1, t1, arr, x1, dv, d1, d2, d3, rot_q1, rot_f1, pe_bar, pe_lab)
        self.q1, self.f1, self.t1, self.arr, self.x1, self.ct, self.rl = q1, f1, t1, arr, x1, arr.ct, arr.r
        self.d = {"d1": d1, "d2": d2, "d3": d3}
        self.pe_bar = pe_bar
        self.cables = VGroup()
        self.tab.add(self.cables)
        self.tab.scale_to_fit_height(8.1).move_to([3.95, -0.3, 0])
        self.tab.set_z_index(1)

    # -------- puntos de bornes (siempre leídos del objeto ya colocado)
    def pq(self, k, arriba=True):
        return (self.q1.tor_sup if arriba else self.q1.tor_inf)[k].get_center()

    def pf(self, k, arriba=True):
        return (self.f1.tor_sup if arriba else self.f1.tor_inf)[k].get_center()

    def pct(self, n):
        return self.ct.b[n].tor.get_center()

    def prl(self, n):
        return self.rl.b[n].tor.get_center()

    def pt1(self, n):
        return self.t1.b[n].tor.get_center()

    def px(self, n, arriba=True):
        return (self.x1.sup if arriba else self.x1.inf)[n][0].get_center()

    def yd(self, nombre, lado):
        d = self.d[nombre]
        return d.get_top()[1] if lado == "arriba" else d.get_bottom()[1]

    def add_cab(self, *cs):
        for c in cs:
            c.set_z_index(3)
        self.cables.add(*cs)

    def aux_dx(self, n):
        """Desplazamiento para que los cables de 95..14/22 bajen por los huecos de la fila inferior del relé."""
        x_mm = {"95": -18, "96": -9, "97": 0, "98": 9, "14/22": 18}[n]
        hueco = {"95": -21.8, "96": -10.5, "97": -0.5, "98": 10.0, "14/22": 21.8}[n]
        return (hueco - x_mm) * MM * S_TAB

    def tramo(self, p, ducto, lado, color=NEGRO_POT, dx=0.0, w=4.2, marca=None):
        """Conductor desde un borne hasta el borde de una canaleta (el resto del recorrido va dentro de ella)."""
        y = self.yd(ducto, lado)
        pts = [p, p + RIGHT * dx + (UP if y > p[1] else DOWN) * 0.12, np.array([p[0] + dx, y, 0])] if dx else [p, np.array([p[0], y, 0])]
        c = cable_ruta(pts, color, w)
        if marca:
            c.add(marcador(marca, p + (UP if y > p[1] else DOWN) * 0.2 + RIGHT * dx * 0.5, 0.42))
        return c

    # -------- zoom de contenido (los letreros fijos no se mueven)
    def zoom_tab(self, punto, factor, destino=(3.95, -0.35, 0), rt=1.0):
        """Acerca el tablero (contenido) alrededor de 'punto'. Se deshace con unzoom() con la transformación inversa exacta,
        así los cables agregados durante el zoom quedan en su lugar."""
        p = np.array(punto, float)
        d = np.array(destino, float)
        self._z = (factor, p, d)
        self.sfx("whoosh", -16)
        self.play(self.tab.animate.scale(factor, about_point=p, scale_stroke=True).shift(d - p), run_time=rt)

    def unzoom(self, rt=0.8):
        f, p, d = self._z
        self.play(self.tab.animate.shift(p - d).scale(1 / f, about_point=p, scale_stroke=True), run_time=rt)

    def marco(self, m, color=MARCA, buff=0.08):
        return SurroundingRectangle(m, color=color, buff=buff, stroke_width=4, corner_radius=0.06)

    # ================================================================ diagramas IEC
    def tarjeta_diag(self, titulo, x0=-7.85, x1=-1.45):
        w = x1 - x0
        f = RoundedRectangle(width=w, height=8.0, corner_radius=0.16, stroke_color="#2E3542", stroke_width=2).set_fill("#0F1218", 1).move_to([(x0 + x1) / 2, -0.4, 0])
        t = T(titulo, 22, AMB, "HEAVY").move_to([(x0 + x1) / 2, 3.42, 0])
        g = VGroup(f, t)
        g.set_z_index(10)
        return g

    def diag_potencia(self, cx=-4.65):
        """Esquema de potencia: L1 L2 L3 → Q1 → KM1 → F2 → M1 (con PE)."""
        g = VGroup()
        d = 0.85
        xs = [cx - d, cx, cx + d]
        tr = {}
        for k, (x, n) in enumerate(zip(xs, ("L1", "L2", "L3"))):
            g.add(T(n, 18, TXT, "HEAVY").move_to([x, 2.95, 0]))
        sw = SW_POT
        q, km, f2 = VGroup(), VGroup(), VGroup()
        for k, x in enumerate(xs):
            c = contacto(True, interruptor=True, largo=0.85, n1=str(2 * k + 1), n2=str(2 * k + 2), sw=sw).move_to([x, 1.85, 0])
            q.add(c)
            c2 = contacto(True, contactor=True, largo=0.85, n1=str(2 * k + 1), n2=str(2 * k + 2), sw=sw).move_to([x, 0.35, 0])
            km.add(c2)
            t_ = termico_pot().move_to([x, -1.05, 0])
            f2.add(t_)
        g.add(DashedLine(q[0].cuchilla.get_center(), q[2].cuchilla.get_center(), dash_length=0.06).set_stroke(SIM, 2), T("-Q1", 18, TXT, "HEAVY").next_to(q, LEFT, buff=0.15))
        g.add(DashedLine(km[0].cuchilla.get_center(), km[2].cuchilla.get_center(), dash_length=0.06).set_stroke(SIM, 2), T("-KM1", 18, TXT, "HEAVY").next_to(km, LEFT, buff=0.15))
        g.add(T("-F2", 18, TXT, "HEAVY").next_to(f2, LEFT, buff=0.15))
        mo = motor_sim(r=0.75).move_to([cx, -2.95, 0])
        g.add(T("-M1", 18, TXT, "HEAVY").next_to(mo, LEFT, buff=0.2))
        segs = {"t1": VGroup(), "t2": VGroup(), "t3": VGroup(), "t4": VGroup(), "pe": VGroup()}
        for k, x in enumerate(xs):
            segs["t1"].add(Line([x, 2.75, 0], q[k][0].get_start()))
            segs["t2"].add(Line(q[k][1].get_end(), km[k][0].get_start()))
            segs["t3"].add(Line(km[k][1].get_end(), f2[k][1].get_top()))
            bor = mo.bornes[k][1].get_top()
            ym = -2.0
            segs["t4"].add(VMobject().set_points_as_corners([f2[k][1].get_bottom(), [x, ym, 0], [bor[0], ym + 0.0, 0], bor]))
        # PE: línea a la derecha que baja a la carcasa
        xpe = cx + 1.75
        segs["pe"].add(VMobject().set_points_as_corners([[xpe, 2.75, 0], [xpe, -2.95, 0], [mo.circ.get_right()[0], -2.95, 0]]))
        g.add(T("PE", 18, "#9BE15D", "HEAVY").move_to([xpe, 2.95, 0]))
        for k_, v in segs.items():
            v.set_stroke(SIM if k_ != "pe" else "#9BE15D", SW_POT if k_ != "pe" else 3)
        g.add(q, km, f2, mo, *segs.values())
        g.q, g.km, g.f2, g.mo, g.segs = q, km, f2, mo, segs
        g.set_z_index(11)
        return g

    def diag_mando(self, xa=-6.05):
        """Esquema de mando 24 V DC: +24 → F2 95-96 → S0 11-12 → S1 13-14 ∥ KM1 13-14 → KM1 A1-A2 → 0 V; rama: F2 97-98 → H1."""
        g = VGroup()
        xb, xc = xa + 1.15, xa + 2.95
        yp, y0 = 2.85, -3.75
        rail_p = Line([xa - 0.35, yp, 0], [xc + 0.5, yp, 0]).set_stroke(ROJO, 3.4)
        rail_0 = Line([xa - 0.35, y0, 0], [xc + 0.5, y0, 0]).set_stroke("#4C8DFF", 3.4)
        g.add(rail_p, rail_0, T("+24 V", 18, ROJO, "HEAVY").next_to(rail_p, LEFT, buff=0.1),
              T("0 V", 18, "#4C8DFF", "HEAVY").next_to(rail_0, LEFT, buff=0.1))
        f2a = termico_aux("F2", largo=0.85).move_to([xa, 2.1, 0])
        s0 = pulsador(False, "S0", "11", "12", largo=0.85).move_to([xa, 0.85, 0])
        s1 = pulsador(True, "S1", "13", "14", largo=0.85).move_to([xa, -0.45, 0])
        km = contacto(True, contactor=True, largo=0.85, n1="13", n2="14").move_to([xb, -0.45, 0])
        kml = T("KM1", 16, SIM, "HEAVY").next_to(km, RIGHT, buff=0.35)
        bo = bobina_sim("KM1").move_to([xa, -2.25, 0])
        f2b = termico_na(largo=0.85).move_to([xc, 2.1, 0])
        h1 = lampara_sim("H1").move_to([xc, -2.25, 0])
        lazo = DashedLine(f2a.cuchilla.get_center() + LEFT * 0.6, f2b.cuchilla.get_center() + LEFT * 0.6, dash_length=0.06).set_stroke(SIM, 1.6, 0.6)
        y_j1, y_j2 = 0.18, -1.15
        segs = {
            "a0": Line([xa, yp, 0], f2a[0].get_start()),
            "a1": Line(f2a[1].get_end(), s0[0].get_start()),
            "a2": Line(s0[1].get_end(), [xa, y_j1, 0]),
            "a3": Line([xa, y_j1, 0], s1[0].get_start()),
            "l1": VMobject().set_points_as_corners([[xa, y_j1, 0], [xb, y_j1, 0], km[0].get_start()]),
            "a4": Line(s1[1].get_end(), [xa, y_j2, 0]),
            "l2": VMobject().set_points_as_corners([km[1].get_end(), [xb, y_j2, 0], [xa, y_j2, 0]]),
            "a5": Line([xa, y_j2, 0], bo[0].get_start()),
            "a6": Line(bo[2].get_end(), [xa, y0, 0]),
            "b0": Line([xc, yp, 0], f2b[0].get_start()),
            "b1": Line(f2b[1].get_end(), h1[0].get_start()),
            "b2": Line(h1[3].get_end(), [xc, y0, 0]),
        }
        for v in segs.values():
            v.set_stroke(SIM, SW_MAN)
        nodos = VGroup(*[Dot([x, y, 0], radius=0.06, color=SIM) for x, y in ((xa, y_j1), (xa, y_j2))])
        g.add(*segs.values(), f2a, s0, s1, km, kml, bo, f2b, h1, lazo, nodos)
        g.f2a, g.s0, g.s1, g.km, g.bo, g.f2b, g.h1, g.segs = f2a, s0, s1, km, bo, f2b, h1, segs
        g.set_z_index(11)
        return g

    def resaltar(self, *ms, color=AMB, w=7):
        g = VGroup(*[m.copy() for m in ms])
        for sm in g.family_members_with_points():
            es_texto = any(isinstance(a_, (Text, MarkupText)) for a_ in [sm]) or sm.get_fill_opacity() > 0.5
            if es_texto:
                sm.set_opacity(0)
            else:
                sm.set_stroke(color, w)
        g.set_z_index(12)
        return g

    # ================================================================ GANCHO
    def f_gancho(self):
        self.voz("gancho")
        dp = self.diag_potencia(-4.9)
        dm = self.diag_mando(2.2)
        dm.shift(RIGHT * 0.6)
        tit_p = T("POTENCIA", 24, AMB, "HEAVY").move_to([-4.9, 3.6, 0])
        tit_m = T("MANDO 24 V DC", 24, AMB, "HEAVY").move_to([4.0, 3.6, 0])
        self.play(LaggedStart(FadeIn(dp, lag_ratio=0.02), FadeIn(dm, lag_ratio=0.02), lag_ratio=0.3), FadeIn(tit_p), FadeIn(tit_m), run_time=2.0)
        preg = VGroup(T("¿Y AHORA", 54, TXT, "HEAVY"), T("POR DÓNDE EMPIEZO?", 54, AMB, "HEAVY")).arrange(DOWN, buff=0.12)
        caja = RoundedRectangle(width=preg.width + 0.8, height=preg.height + 0.6, corner_radius=0.2, stroke_color=AMB, stroke_width=3).set_fill("#000000", 0.94)
        pg = VGroup(caja, preg).move_to([0, -0.2, 0]).set_z_index(20)
        self.esperar_frac(0.05)
        self.sfx("pop", -12)
        self.play(FadeIn(pg, scale=1.08), run_time=0.5)
        self.esperar_frac(0.22)
        self.play(FadeOut(pg), FadeOut(dp), FadeOut(dm), FadeOut(tit_p), FadeOut(tit_m), run_time=0.5)
        # el tablero terminado (vista previa) y los pasos del video
        self.play(FadeIn(self.tab), run_time=0.8)
        pasos = VGroup(*[VGroup(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.1, stroke_width=0).set_fill(c, 1), T(str(k + 1), 22, "#000000", "HEAVY"), T(t, 24, TXT, "HEAVY"))
                         for k, (t, c) in enumerate((("Leer", MARCA), ("Potencia", AMB), ("Mando", "#4C8DFF"), ("Prueba en frío", "#C084FC"), ("Energizar", VERDE_OK)))])
        for p in pasos:
            p[1].move_to(p[0]); p[2].next_to(p[0], RIGHT, buff=0.18)
        pasos.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([-4.6, -0.2, 0]).set_z_index(15)
        for k, p in enumerate(pasos):
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.35)
            self.esperar_frac(0.1)
        self.esperar_frac(0.5)
        self.play(FadeOut(pasos), run_time=0.3)
        t1 = T("MI PRIMER ARRANQUE", 56, TXT, "HEAVY")
        t2 = T("CON CONTACTORES", 70, MARCA, "HEAVY")
        t3 = T("Sigue el diagrama borne por borne", 30, TXT2, "BOLD")
        tit = VGroup(t1, t2, t3).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        tit.scale_to_fit_width(min(tit.width, 6.6)).move_to([-4.4, 0.4, 0]).set_z_index(15)
        self.play(FadeIn(tit, shift=RIGHT * 0.3), run_time=0.7)
        self.cerrar_voz(0.4)
        self.play(FadeOut(tit), run_time=0.4)

    # ================================================================ 1 · MATERIALES
    def f_materiales(self):
        self.portadilla("materiales")
        self.voz("materiales")
        s = 0.62
        items = [
            ("-Q1", "Interruptor 3P · 15 A · C", breaker_on(breaker_din(3, 15, "C", s=s * 0.8))),
            ("-F1", "Interruptor 2P · fuente", breaker_on(breaker_din(2, 6, "C", s=s * 0.8))),
            ("-T1", "Fuente 24 V DC", fuente_24v(s * 0.75)),
            ("-KM1", "Contactor S00 · 7 A AC-3", contactor_s00(s)),
            ("-F2", "Relé térmico 3,5–5 A", termico_s00(s)),
            ("-S0 / -S1", "Paro NC · Marcha NA", VGroup(pulsador_22("rojo", s * 0.9, "S0", "O"), pulsador_22("verde", s * 0.9, "S1", "I")).arrange(RIGHT, buff=0.15)),
            ("-H1", "Piloto ámbar · falla", pulsador_22("ambar", s * 0.9, "H1", "", luminoso=True)),
            ("-X1", "Bornera", bornera(["1", "2", "3", "U", "PE"], s, pe=("PE",))),
            ("-M1", "Motor 1 hp · 230 V Δ", placa_datos_motor(0.55)),
        ]
        celdas = VGroup()
        for ref, nom, ic in items:
            caja = RoundedRectangle(width=3.0, height=2.35, corner_radius=0.14, stroke_color="#2E3542", stroke_width=2).set_fill("#151922", 1)
            if ic.height > 1.35:
                ic.scale_to_fit_height(1.35)
            if ic.width > 2.6:
                ic.scale_to_fit_width(2.6)
            ic.move_to(caja.get_center() + UP * 0.22)
            r = pastilla(ref, AMB, 20, True).move_to(caja.get_corner(UL) + RIGHT * 0.55 + DOWN * 0.24)
            n = T(nom, 18, TXT, "BOLD").move_to(caja.get_bottom() + UP * 0.26)
            if n.width > 2.8:
                n.scale_to_fit_width(2.8)
            celdas.add(VGroup(caja, ic, r, n))
        celdas.arrange_in_grid(3, 3, buff=(0.22, 0.2))
        celdas.scale_to_fit_width(7.3).move_to([-4.1, -0.45, 0]).set_z_index(15)
        # los equipos aparecen al nombrarlos (posición aproximada de cada uno en la voz)
        marcas = [0.06, 0.2, 0.27, 0.36, 0.55, 0.68, 0.8, 0.86, 0.9]
        mapa = [self.q1, self.f1, self.t1, self.ct, self.rl, None, None, self.x1, None]
        for k, (c_, f) in enumerate(zip(celdas, marcas)):
            espera = self.fin_voz - self.renderer.time - (1 - f) * (self.fin_voz - self.renderer.time) if False else None
            objetivo = f * self.GUION_DUR["materiales"] if hasattr(self, "GUION_DUR") else None
            self.wait_hasta(f)
            anims = [FadeIn(c_, shift=UP * 0.2)]
            if mapa[k] is not None:
                fr = self.marco(mapa[k], AMB)
                anims.append(Create(fr))
                self.play(*anims, run_time=0.45)
                self.play(FadeOut(fr), run_time=0.3)
            else:
                self.play(*anims, run_time=0.45)
        self.cerrar_voz()
        self.mat = celdas

    def wait_hasta(self, f):
        """Espera hasta la fracción f de la voz actual (desde su inicio)."""
        ini = self.fin_voz - self.dur_voz
        t = ini + f * self.dur_voz
        w = t - self.renderer.time
        if w > 0.03:
            self.wait(w)

    def voz(self, clave):
        d = super().voz(clave)
        self.dur_voz = d
        return d

    # ---------------------------------------------------------------- dimensionamiento
    def f_dimension(self):
        self.voz("dimension")
        self.play(FadeOut(self.mat), run_time=0.4)
        placa = placa_datos_motor(0.95).move_to([-4.7, 2.0, 0]).set_z_index(15)
        self.play(FadeIn(placa, shift=UP * 0.2), run_time=0.5)
        filas = [
            ("NEC T430.250", "1 hp · 230 V · 3~", "4,2 A", MARCA, 0.08),
            ("NEC 430.22", "4,2 × 1,25 = 5,25 A", "14 AWG", "#4C8DFF", 0.3),
            ("NEC 430.52", "4,2 × 2,5 = 10,5 A", "Q1: 15 A", AMB, 0.55),
            ("NEC 430.32", "ajuste = corriente de placa", "F2: 3,9 A", VERDE_OK, 0.82),
        ]
        cajas = VGroup()
        for cod, txt, res, col, f in filas:
            c = carta(cod, [txt], col, w=5.9, size=22)
            rr = pastilla(res, col, 24, True).next_to(c, RIGHT, buff=0.15)
            cajas.add(VGroup(c, rr))
        cajas.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([-4.15, -1.55, 0]).set_z_index(15)
        if cajas.width > 6.6:
            cajas.scale_to_fit_width(6.6)
        for k, (cj, fila) in enumerate(zip(cajas, filas)):
            self.wait_hasta(fila[4])
            self.sfx("tic", -12)
            self.play(FadeIn(cj, shift=RIGHT * 0.2), run_time=0.4)
            if k == 3:
                self.zoom_tab(self.rl.dial.get_center(), 3.2, (4.3, -0.4, 0))
                fr = Circle(radius=0.95, color=VERDE_OK, stroke_width=5).move_to([4.3, -0.4, 0])
                self.play(Create(fr), run_time=0.4)
                self.esperar_frac(0.6)
                self.play(FadeOut(fr), run_time=0.3)
                self.unzoom()
        self.cerrar_voz()
        self.limpiar(placa, cajas)

    # ================================================================ 2 · LEER EL DIAGRAMA
    def f_leer(self):
        self.portadilla("leer")
        self.voz("leer")
        self.play(FadeOut(self.tab), run_time=0.3)
        dm = self.diag_mando(-2.6).shift(UP * 0.1)
        dm.scale(1.0)
        dp = self.diag_potencia(-5.6).scale(0.82).shift(DOWN * 0.2)
        self.play(FadeIn(dm), run_time=0.6)
        reglas = [
            ("1", "Todo en REPOSO", "sin tensión, sin pulsar", 0.03),
            ("2", "Letra + número", "KM contactor · F protección · S pulsador · H piloto", 0.16),
            ("3", "Números de bornes", "1-3-5 entran, 2-4-6 salen · x1-x2 NC · x3-x4 NA", 0.33),
            ("4", "De + a 0 V", "de arriba hacia abajo", 0.86),
        ]
        cart = VGroup()
        for n, a, b_, _ in reglas:
            c = carta(f"{n} · {a}", [b_], [MARCA, AMB, "#4C8DFF", VERDE_OK][int(n) - 1], w=6.3, size=20)
            cart.add(c)
        cart.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([4.15, -0.2, 0])
        if cart.height > 6.8:
            cart.scale_to_fit_height(6.8)
        # regla 1
        self.wait_hasta(reglas[0][3])
        self.play(FadeIn(cart[0], shift=LEFT * 0.2), run_time=0.4)
        self.wait_hasta(0.08)
        f0 = self.marco(dm.s0, ROJO); f1_ = self.marco(dm.s1, VERDE_OK)
        l0 = T("cerrado", 18, ROJO, "HEAVY").next_to(f0, RIGHT, buff=0.1).set_z_index(13)
        l1 = T("abierto", 18, VERDE_OK, "HEAVY").next_to(f1_, LEFT, buff=0.1).shift(LEFT * 0.0).set_z_index(13)
        VGroup(f0, f1_).set_z_index(13)
        self.play(Create(f0), Create(f1_), FadeIn(l0), FadeIn(l1), run_time=0.6)
        # regla 2
        self.wait_hasta(reglas[1][3])
        self.play(FadeIn(cart[1], shift=LEFT * 0.2), FadeOut(VGroup(f0, f1_, l0, l1)), run_time=0.4)
        for m in (dm.bo, dm.f2a, dm.s0, dm.h1):
            self.play(Indicate(m, color=AMB, scale_factor=1.12), run_time=0.55)
        nq = pastilla("IEC 81346-2 actual: el contactor también se designa -Q", "#4C8DFF", 18, True).move_to([-2.9, -4.15, 0]).set_z_index(30)
        self.play(FadeIn(nq), run_time=0.3)
        self.wait(1.6)
        self.play(FadeOut(nq), run_time=0.3)
        # regla 3: números de bornes
        self.wait_hasta(reglas[2][3])
        self.play(FadeIn(cart[2], shift=LEFT * 0.2), FadeOut(dm), run_time=0.4)
        ej = VGroup(
            VGroup(contacto(True, contactor=True, largo=1.2, n1="1", n2="2", sw=SW_POT), T("potencia", 18, TXT2, "BOLD")),
            VGroup(contacto(True, contactor=True, largo=1.2, n1="13", n2="14"), T("NA: x3-x4", 18, VERDE_OK, "HEAVY")),
            VGroup(contacto(False, contactor=True, largo=1.2, n1="21", n2="22"), T("NC: x1-x2", 18, ROJO, "HEAVY")),
            VGroup(bobina_sim("KM1"), T("bobina A1-A2", 18, TXT2, "BOLD")),
            VGroup(termico_aux("F2", largo=1.2), T("95-96 NC", 18, ROJO, "HEAVY")),
            VGroup(termico_na(largo=1.2), T("97-98 NA", 18, VERDE_OK, "HEAVY")),
        )
        for e in ej:
            e[1].next_to(e[0], DOWN, buff=0.25)
        ej.arrange_in_grid(2, 3, buff=(0.75, 0.55)).move_to([-3.6, -0.3, 0])
        ej.set_z_index(11)
        for k, e in enumerate(ej):
            self.wait_hasta(0.36 + k * 0.08)
            self.play(FadeIn(e, shift=UP * 0.15), run_time=0.4)
        # regla 4: la corriente recorre el mando de arriba hacia abajo
        self.wait_hasta(reglas[3][3])
        self.play(FadeOut(ej), FadeIn(cart[3], shift=LEFT * 0.2), FadeIn(dm), run_time=0.45)
        ruta = [dm.segs[k] for k in ("a0",)] + [dm.f2a[0], dm.f2a[1]]
        camino = VMobject().set_points_as_corners([[-2.6, 2.85, 0], [-2.6, -3.75, 0]]).set_stroke(AMB, 0)
        punto = Dot(color=AMB, radius=0.12).move_to(camino.get_start()).set_z_index(14)
        flecha = Arrow([-1.5, 2.6, 0], [-1.5, -3.4, 0], color=AMB, stroke_width=8, buff=0).set_z_index(14)
        self.play(FadeIn(punto), GrowArrow(flecha), run_time=0.4)
        self.play(MoveAlongPath(punto, camino), run_time=max(1.0, self.resta() - 1.0), rate_func=linear)
        self.cerrar_voz()
        self.limpiar(dm, cart, punto, flecha)

    # ================================================================ 3 · POTENCIA
    def f_potencia(self):
        self.portadilla("potencia")
        self.voz("potencia")
        card = self.tarjeta_diag("ESQUEMA DE POTENCIA")
        dp = self.diag_potencia(-4.65)
        self.play(FadeIn(card), FadeIn(dp), FadeIn(self.tab), run_time=0.6)
        neg = NEGRO_POT
        # ---- tramo 1: L1 L2 L3 → Q1 1-3-5
        self.wait_hasta(0.1)
        h = self.resaltar(*dp.segs["t1"])
        self.play(Create(h), run_time=0.5)
        cab = VGroup(*[self.tramo(self.pq(k), "d1", "abajo", neg, marca=f"L{k + 1}") for k in range(3)])
        self.add_cab(cab)
        self.zoom_tab(self.pq(1), 2.6, (3.95, 0.3, 0))
        self.play(Create(cab), run_time=0.9)
        for k in range(3):
            self.sfx("tic", -14)
            self.play(Rotate(self.q1.tor_sup[k][3], PI, about_point=self.q1.tor_sup[k].get_center()), run_time=0.22)
        self.unzoom()
        # ---- tramo 2: Q1 2-4-6 → KM1 1/L1 3/L2 5/L3
        self.wait_hasta(0.22)
        self.play(FadeOut(h), run_time=0.2)
        h = self.resaltar(*dp.segs["t2"])
        self.play(Create(h), run_time=0.5)
        sal = VGroup(*[self.tramo(self.pq(k, False), "d2", "arriba", neg, marca=f"{2 * k + 2}") for k in range(3)])
        ent = VGroup(*[self.tramo(self.pct(n), "d2", "abajo", neg, marca=n) for n in ("1/L1", "3/L2", "5/L3")])
        self.add_cab(sal, ent)
        centro = (self.pq(1, False) + self.pct("3/L2")) / 2
        self.zoom_tab(centro, 2.3, (3.95, -0.35, 0))
        self.play(Create(sal), run_time=0.7)
        self.play(Create(ent), run_time=0.7)
        regla = pastilla("mismo orden de fases", AMB, 24, True).move_to([3.95, 3.3, 0]).set_z_index(30)
        self.play(FadeIn(regla), run_time=0.3)
        self.wait_hasta(0.42)
        self.play(FadeOut(regla), run_time=0.3)
        self.unzoom()
        # ---- tramo 3: el relé se monta debajo (los pines entran en 2/T1 4/T2 6/T3)
        self.wait_hasta(0.47)
        self.play(FadeOut(h), run_time=0.2)
        h = self.resaltar(*dp.segs["t3"])
        self.play(Create(h), run_time=0.5)
        self.zoom_tab(self.rl.get_top(), 2.4, (3.95, 0.2, 0))
        self.play(self.rl.animate.shift(DOWN * 0.5), run_time=0.01)
        self.play(self.rl.animate.shift(UP * 0.5), run_time=0.9, rate_func=smooth)
        self.sfx("tic", -8)
        self.wait_hasta(0.56)
        self.unzoom()
        # ---- tramo 4: F2 → X1 U V W → motor U1 V1 W1 (puentes en triángulo)
        self.wait_hasta(0.58)
        self.play(FadeOut(h), run_time=0.2)
        h = self.resaltar(*dp.segs["t4"])
        self.play(Create(h), run_time=0.5)
        sf2 = VGroup(*[self.tramo(self.prl(n), "d3", "arriba", neg, marca=n) for n in ("2/T1", "4/T2", "6/T3")])
        xin = VGroup(*[self.tramo(self.px(n), "d2", "abajo", neg, marca=n) for n in ("U", "V", "W")])
        xout = VGroup(*[self.tramo(self.px(n, False), "d3", "arriba", neg) for n in ("U", "V", "W")])
        self.add_cab(sf2, xin, xout)
        self.zoom_tab((self.prl("4/T2") + self.px("V")) / 2, 1.9, (3.95, -0.6, 0))
        self.play(Create(sf2), run_time=0.6)
        self.play(Create(xin), run_time=0.6)
        self.play(Create(xout), run_time=0.5)
        self.unzoom()
        # placa de bornes del motor (sobre la tarjeta del diagrama)
        self.wait_hasta(0.7)
        cb = caja_bornes_motor(1.3, "delta").move_to([3.95, 0.0, 0]).set_z_index(25)
        tapa = Rectangle(width=9.2, height=8.6, stroke_width=0).set_fill("#000000", 0.92).move_to([3.95, -0.35, 0]).set_z_index(24)
        cb.puentes.set_opacity(0)
        self.play(FadeIn(tapa), FadeIn(cb, scale=0.9), run_time=0.5)
        llegan = VGroup(*[cable_ruta([cb.b[n].get_center() + UP * 2.2, cb.b[n].get_center() + UP * 0.3], neg, 6).set_z_index(26) for n in ("U1", "V1", "W1")])
        llegan_t = VGroup(*[T(n[0], 20, TXT, "HEAVY").move_to(cb.b[n].get_center() + UP * 2.4) for n in ("U1", "V1", "W1")]).set_z_index(26)
        self.play(Create(llegan), FadeIn(llegan_t), run_time=0.6)
        self.wait_hasta(0.78)
        for p_ in cb.puentes:
            self.sfx("tic", -14)
            self.play(p_.animate.set_opacity(1), run_time=0.35)
        nota = pastilla("230 V → triángulo: U1-W2 · V1-U2 · W1-V2", AMB, 22, True).move_to([3.95, -2.6, 0]).set_z_index(27)
        self.play(FadeIn(nota), run_time=0.3)
        # PE
        self.wait_hasta(0.89)
        self.play(FadeOut(h), run_time=0.2)
        h = self.resaltar(*dp.segs["pe"], color="#9BE15D")
        pe_c = cable_ruta([cb.b["PE"].get_center() + RIGHT * 1.6 + UP * 1.2, cb.b["PE"].get_center() + RIGHT * 1.6, cb.b["PE"].get_center()], VERDE_AM[0], 6).set_z_index(26)
        pe_c.add(DashedLine(pe_c[1].get_start(), pe_c[1].get_end(), dash_length=0.12).set_stroke(VERDE_AM[1], 3).set_z_index(27))
        self.play(Create(h), Create(pe_c), run_time=0.7)
        self.cerrar_voz()
        self.play(FadeOut(VGroup(tapa, cb, llegan, llegan_t, nota, pe_c)), run_time=0.4)
        # PE dentro del tablero: barra → X1 PE
        pe_in = VGroup(cable_ruta([self.pe_bar.get_bottom(), [self.pe_bar.get_center()[0], self.yd("d2", "arriba"), 0]], VERDE_AM[0], 4.2),
                       cable_ruta([self.pe_bar[1].get_center(), self.pe_bar[1].get_center() + RIGHT * 0.0 + UP * 0.12, [self.pe_bar[1].get_center()[0], self.yd("d1", "abajo"), 0]], VERDE_AM[0], 4.2),
                       self.tramo(self.px("PE"), "d2", "abajo", VERDE_AM[0]), self.tramo(self.px("PE", False), "d3", "arriba", VERDE_AM[0]))
        self.add_cab(pe_in)
        self.play(Create(pe_in), run_time=0.5)
        self.limpiar(card, dp, h)

    # ================================================================ 4 · MANDO
    def f_control(self):
        self.portadilla("control")
        self.voz("control")
        card = self.tarjeta_diag("ESQUEMA DE MANDO 24 V DC")
        dm = self.diag_mando(-6.15)
        self.play(FadeIn(card), FadeIn(dm), run_time=0.5)
        az = AZUL_DC
        # alimentación de la fuente: F1 → T1 L N (y F1 desde L1-L2 de la acometida)
        f1in = VGroup(*[self.tramo(self.pf(k), "d1", "abajo", neg_ := NEGRO_POT) for k in range(2)])
        f1out = VGroup(*[self.tramo(self.pf(k, False), "d2", "arriba", NEGRO_POT) for k in range(2)])
        t1in = VGroup(self.tramo(self.pt1("L"), "d1", "abajo", NEGRO_POT), self.tramo(self.pt1("N"), "d1", "abajo", NEGRO_POT), self.tramo(self.pt1("PE"), "d1", "abajo", VERDE_AM[0]))
        self.add_cab(f1in, f1out, t1in)
        self.play(Create(f1in), Create(f1out), Create(t1in), run_time=0.8)
        # ---- +24 V → F2 95
        self.wait_hasta(0.04)
        h = self.resaltar(dm.segs["a0"], dm.f2a)
        self.play(Create(h), run_time=0.5)
        c1 = self.tramo(self.pt1("+"), "d2", "arriba", az, marca="1")
        c95 = self.tramo(self.prl("95"), "d3", "arriba", az, dx=self.aux_dx("95"), marca="1")
        c97 = cable_ruta([self.prl("95"), self.prl("95") + DOWN * 0.16, self.prl("97") + DOWN * 0.16, self.prl("97")], az, 3.0)
        self.add_cab(c1, c95)
        self.zoom_tab(self.prl("96"), 3.0, (3.95, -0.3, 0))
        self.play(Create(c95), run_time=0.6)
        self.wait_hasta(0.17)
        # ---- F2 96 → X1:1 → S0 11-12 → X1:2 → S1 13-14
        self.unzoom()
        self.play(FadeOut(h), run_time=0.2)
        h = self.resaltar(dm.segs["a1"], dm.s0, dm.segs["a2"], dm.segs["a3"], dm.s1)
        self.play(Create(h), run_time=0.6)
        c96 = self.tramo(self.prl("96"), "d3", "arriba", az, dx=self.aux_dx("96"), marca="2")
        x1_1 = self.tramo(self.px("1"), "d2", "abajo", az, marca="2")
        x1_2 = self.tramo(self.px("2"), "d2", "abajo", az, marca="3")
        x1_3 = self.tramo(self.px("3"), "d2", "abajo", az, marca="4")
        self.add_cab(c96, x1_1, x1_2, x1_3)
        self.play(Create(c96), Create(x1_1), Create(x1_2), Create(x1_3), run_time=0.8)
        # puerta (vista posterior): S0 y S1 con sus módulos de contacto
        self.wait_hasta(0.27)
        puerta = self.vista_puerta().set_z_index(25)
        self.play(FadeIn(puerta, shift=LEFT * 0.3), run_time=0.5)
        self.wait_hasta(0.36)
        # ---- S1 14 → X1:3 → KM1 A1 ; A2 → 0 V
        self.play(FadeOut(puerta), FadeOut(h), run_time=0.4)
        h = self.resaltar(dm.segs["a4"], dm.segs["a5"], dm.bo, dm.segs["a6"])
        self.play(Create(h), run_time=0.5)
        a1 = self.tramo(self.pct("A1"), "d2", "abajo", az, marca="4")
        a2 = self.tramo(self.prl("A2"), "d3", "arriba", az, marca="0V")
        m0 = self.tramo(self.pt1("−"), "d2", "arriba", az, marca="0V")
        self.add_cab(a1, a2, m0)
        self.zoom_tab((self.pct("A1") + self.prl("A2")) / 2, 1.9, (3.95, -0.3, 0))
        self.play(Create(a1), Create(a2), run_time=0.7)
        self.unzoom()
        self.play(Create(m0), run_time=0.4)
        # ---- autoenclavamiento: KM1 13-14 en paralelo con S1
        self.wait_hasta(0.47)
        self.play(FadeOut(h), run_time=0.2)
        h = self.resaltar(dm.segs["l1"], dm.km, dm.segs["l2"], color=VERDE_OK)
        self.play(Create(h), run_time=0.6)
        ae = pastilla("AUTOENCLAVAMIENTO", VERDE_OK, 26, True).move_to([-4.65, -4.05, 0]).set_z_index(30)
        self.play(FadeIn(ae), run_time=0.3)
        k13 = self.tramo(self.pct("13"), "d2", "abajo", az, marca="3")
        k14 = self.tramo(self.prl("14/22"), "d3", "arriba", az, dx=self.aux_dx("14/22"), marca="4")
        self.add_cab(k13, k14)
        self.zoom_tab((self.pct("13") + self.prl("14/22")) / 2, 1.9, (3.95, -0.3, 0))
        self.play(Create(k13), run_time=0.5)
        self.play(Create(k14), run_time=0.5)
        self.wait_hasta(0.72)
        self.unzoom()
        # ---- piloto de falla: + → 97-98 → X1:4 → H1 → X1:5 → 0 V
        self.wait_hasta(0.75)
        self.play(FadeOut(h), FadeOut(ae), run_time=0.2)
        h = self.resaltar(dm.segs["b0"], dm.f2b, dm.segs["b1"], dm.h1, dm.segs["b2"])
        self.play(Create(h), run_time=0.5)
        c98 = self.tramo(self.prl("98"), "d3", "arriba", az, dx=self.aux_dx("98"), marca="5")
        x1_4 = self.tramo(self.px("4"), "d2", "abajo", az, marca="5")
        x1_5 = self.tramo(self.px("5"), "d2", "abajo", az, marca="0V")
        self.add_cab(c97, c98, x1_4, x1_5)
        self.zoom_tab(self.prl("97"), 2.8, (3.95, -0.3, 0))
        self.play(Create(c97), run_time=0.5)
        self.play(Create(c98), run_time=0.5)
        self.unzoom()
        self.play(Create(x1_4), Create(x1_5), run_time=0.5)
        # salida de la bornera hacia la puerta (abajo)
        xo = VGroup(*[self.tramo(self.px(n, False), "d3", "arriba", az) for n in ("1", "2", "3", "4", "5")])
        self.add_cab(xo)
        self.play(Create(xo), run_time=0.5)
        nota = pastilla("mando DC: azul · cada punta con su número", "#4C8DFF", 22, True).move_to([3.95, 4.05, 0]).set_z_index(30)
        self.play(FadeIn(nota), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(card, dm, h, nota)

    def vista_puerta(self):
        """Parte trasera de la puerta: S0 (NC 11-12), S1 (NA 13-14) y H1 (X1-X2), cableados a la bornera X1."""
        fondo = RoundedRectangle(width=6.2, height=7.4, corner_radius=0.16, stroke_color="#4A5568", stroke_width=3).set_fill("#5B6472", 1)
        tit = T("PUERTA · vista posterior", 22, TXT, "HEAVY").next_to(fondo.get_top(), DOWN, buff=0.25)
        s0 = VGroup(pulsador_22("rojo", 0.75, "S0", "O"), modulo_contacto("11", "12", 0.75, nc=True)).arrange(DOWN, buff=0.15)
        s1 = VGroup(pulsador_22("verde", 0.75, "S1", "I"), modulo_contacto("13", "14", 0.75)).arrange(DOWN, buff=0.15)
        h1 = VGroup(pulsador_22("ambar", 0.75, "H1", "", luminoso=True), modulo_contacto("X1", "X2", 0.75)).arrange(DOWN, buff=0.15)
        h1[1][-2].set_fill("#F79009"); h1[1][-1].become(tx("LED", 1.4 * MM * 0.75, WHITE).move_to(h1[1][-1]))
        fila = VGroup(s0, s1, h1).arrange(RIGHT, buff=0.35).move_to(fondo.get_center() + UP * 0.6)
        g = VGroup(fondo, tit, fila)
        # cables: 2 → S0.11, 3 → S0.12 y S1.13, 4 → S1.14, 5 → H1.X1, 0V → H1.X2
        az = AZUL_DC
        def pb(m, n):
            return m[1].b[n].tor.get_center()
        y_bus = fondo.get_bottom()[1] + 0.55
        rutas = [
            ([pb(s0, "11"), pb(s0, "11") + LEFT * 0.42, [pb(s0, "11")[0] - 0.42, y_bus, 0]], "2"),
            ([pb(s0, "12"), pb(s0, "12") + RIGHT * 0.3, pb(s1, "13") + LEFT * 0.3, pb(s1, "13")], None),
            ([pb(s0, "12"), pb(s0, "12") + DOWN * 0.0 + LEFT * 0.18, [pb(s0, "12")[0] - 0.18, y_bus, 0]], "3"),
            ([pb(s1, "14"), pb(s1, "14") + LEFT * 0.25, [pb(s1, "14")[0] - 0.25, y_bus, 0]], "4"),
            ([pb(h1, "X1"), pb(h1, "X1") + LEFT * 0.3, [pb(h1, "X1")[0] - 0.3, y_bus, 0]], "5"),
            ([pb(h1, "X2"), pb(h1, "X2") + RIGHT * 0.3, [pb(h1, "X2")[0] + 0.3, y_bus, 0]], "0V"),
        ]
        cab = VGroup()
        for pts, num in rutas:
            c = cable_ruta(pts, az, 4)
            if num:
                c.add(marcador(num, pts[0] + (pts[1] - pts[0]) * 0.55, 0.5))
            cab.add(c)
        haz = VGroup(RoundedRectangle(width=5.2, height=0.28, corner_radius=0.14, stroke_width=0).set_fill("#2B3A7A", 1).move_to([fondo.get_center()[0], y_bus - 0.05, 0]),
                     T("a la bornera -X1 (1 a 5)", 16, TXT, "HEAVY").move_to([fondo.get_center()[0], y_bus - 0.42, 0]))
        g.add(cab, haz)
        g.move_to([-4.65, -0.4, 0])
        return g

    # ================================================================ 5 · PRUEBAS EN FRÍO
    def f_pruebas(self):
        self.portadilla("pruebas")
        self.voz("pruebas")
        mm = multimetro_ohm(1.25, "----").move_to([-5.4, 0.2, 0]).set_z_index(15)
        self.play(FadeIn(mm, shift=UP * 0.2), run_time=0.5)
        # bobina A1-A2
        self.wait_hasta(0.05)
        self.zoom_tab((self.pct("A1") + self.prl("A2")) / 2, 2.0, (3.9, -0.3, 0))
        pr = punta(mm.jack_v.get_center(), self.pct("A1") + DOWN * 0.05, "#E5484D").set_z_index(20)
        pn = punta(mm.jack_com.get_center(), self.prl("A2") + DOWN * 0.05, "#101828").set_z_index(20)
        self.play(Create(pr), Create(pn), run_time=0.7)
        self.play(pantalla_mm(mm, "144"), run_time=0.3)
        self.sfx("ding", -12)
        calc = carta("R ≈ V² / P", ["24² / 4 W ≈ 144 Ω"], MARCA, w=4.4, size=22).move_to([-5.2, 3.0, 0]).set_z_index(15)
        self.play(FadeIn(calc), run_time=0.4)
        self.wait_hasta(0.21)
        mal = VGroup(pastilla("0 Ω → corto", ROJO, 20, True), pastilla("OL → bobina abierta", ROJO, 20, True)).arrange(DOWN, buff=0.1).move_to([-5.2, -3.3, 0]).set_z_index(15)
        self.play(FadeIn(mal), run_time=0.4)
        self.wait_hasta(0.32)
        self.play(FadeOut(VGroup(pr, pn, mal, calc)), run_time=0.3)
        self.unzoom()
        # mando: se suelta el + de la fuente y se mide entre esa punta y 0 V
        self.zoom_tab(self.pt1("+"), 2.6, (3.9, -0.2, 0))
        cab_mas = [c for c in self.cables if isinstance(c, VGroup)]
        suelto = pastilla("+ suelto de la fuente", AMB, 22, True).move_to([3.9, 3.4, 0]).set_z_index(30)
        self.play(FadeIn(suelto), run_time=0.3)
        p_mas = self.pt1("+") + DOWN * 0.45 + LEFT * 0.25
        pr = punta(mm.jack_v.get_center(), p_mas, "#E5484D").set_z_index(20)
        pn = punta(mm.jack_com.get_center(), self.pt1("−") + DOWN * 0.05, "#101828").set_z_index(20)
        self.play(Create(pr), Create(pn), run_time=0.6)
        self.play(pantalla_mm(mm, "OL"), run_time=0.3)
        self.wait_hasta(0.5)
        est = VGroup(T("S1 pulsado", 26, VERDE_OK, "HEAVY")).move_to([-5.4, -3.4, 0]).set_z_index(15)
        self.play(FadeIn(est), pantalla_mm(mm, "144"), run_time=0.4)
        self.sfx("ding", -12)
        self.wait_hasta(0.66)
        est2 = T("S1 + S0 pulsados", 26, ROJO, "HEAVY").move_to(est).set_z_index(15)
        self.play(Transform(est, est2), pantalla_mm(mm, "OL"), run_time=0.4)
        self.sfx("tic", -10)
        self.wait_hasta(0.74)
        self.play(FadeOut(VGroup(pr, pn, suelto, est)), run_time=0.3)
        self.unzoom()
        # potencia
        lista = VGroup(*[VGroup(check(VERDE_OK, 0.22), T(t, 22, TXT, "BOLD")).arrange(RIGHT, buff=0.2) for t in
                         ("KM1 abierto: nada entre fases", "Motor: U-V = V-W = W-U", "PE: continuidad hasta la carcasa")]).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-4.7, -3.0, 0])
        self.play(FadeOut(mm), run_time=0.3)
        lista.move_to([-4.6, 0.0, 0]).set_z_index(15)
        for k, l in enumerate(lista):
            self.wait_hasta(0.76 + k * 0.07)
            self.play(FadeIn(l, shift=RIGHT * 0.2), run_time=0.35)
        self.cerrar_voz()
        self.limpiar(lista)

    # ================================================================ 6 · ENERGIZAR
    def f_energizar(self):
        self.portadilla("energizar")
        self.voz("energizar")
        card = self.tarjeta_diag("MANDO EN TIEMPO REAL")
        dm = self.diag_mando(-6.15)
        self.play(FadeIn(card), FadeIn(dm), run_time=0.4)
        # Q1 y F1 a ON, LED de la fuente
        self.wait_hasta(0.02)
        self.sfx("tic", -6)
        self.play(palanca_breaker(self.q1, True), palanca_breaker(self.f1, True), run_time=0.4)
        self.play(self.t1.led.animate.set_fill("#3DFF8F", 1), Indicate(self.t1.led, color="#3DFF8F", scale_factor=2), run_time=0.5)
        caliente = VGroup(dm.segs["a0"], dm.f2a, dm.segs["a1"], dm.s0, dm.segs["a2"], dm.segs["a3"]).copy().set_stroke(ROJO, 6).set_z_index(12)
        self.play(Create(caliente), run_time=0.5)
        # marcha
        self.wait_hasta(0.12)
        self.sfx("tic", -8)
        self.play(mover(dm.s1, True), run_time=0.3)
        rama = VGroup(dm.s1.copy(), dm.segs["a4"], dm.segs["a5"], dm.bo, dm.segs["a6"]).copy().set_stroke(ROJO, 6).set_z_index(12)
        self.play(Create(rama), run_time=0.4)
        self.play(contactor_cerrar(self.ct, True), mover(dm.km, True), run_time=0.3)
        self.sfx("tic", -6)
        lazo = VGroup(dm.segs["l1"], dm.km, dm.segs["l2"]).copy().set_stroke(VERDE_OK, 6).set_z_index(12)
        self.play(Create(lazo), run_time=0.4)
        mot = motor_tefc(0.62).move_to([3.95, -0.4, 0]).set_z_index(26)
        tapa = Rectangle(width=9.2, height=8.6, stroke_width=0).set_fill("#000000", 0.9).move_to([3.95, -0.35, 0]).set_z_index(25)
        estado = pastilla("MOTOR EN MARCHA", VERDE_OK, 26, True).move_to([3.95, 2.6, 0]).set_z_index(27)
        self.wait_hasta(0.27)
        self.play(FadeIn(tapa), FadeIn(mot), FadeIn(estado), run_time=0.5)
        girar_eje(mot, 3.0)
        # se suelta marcha: sigue por el 13-14
        self.wait_hasta(0.33)
        self.play(mover(dm.s1, False), FadeOut(rama[0]), run_time=0.3)
        self.wait_hasta(0.42)
        # paro
        self.sfx("tic", -8)
        self.play(mover(dm.s0, False), run_time=0.3)
        self.play(FadeOut(caliente), FadeOut(rama), FadeOut(lazo), mover(dm.km, False), contactor_cerrar(self.ct, False), run_time=0.4)
        mot.chaveta.clear_updaters()
        self.play(Transform(estado, pastilla("PARO", ROJO, 26, True).move_to(estado).set_z_index(27)), run_time=0.3)
        self.play(mover(dm.s0, True), run_time=0.3)
        self.wait_hasta(0.55)
        self.play(FadeOut(VGroup(tapa, mot, estado)), run_time=0.4)
        # sobrecarga simulada con TEST
        self.zoom_tab(self.rl.test.get_center(), 2.4, (3.95, -0.3, 0))
        self.sfx("tic", -6)
        self.play(self.rl.test.animate.shift(DOWN * 0.25), run_time=0.3)
        self.play(mover(dm.f2a, False), mover(dm.f2b, True), run_time=0.3)
        fal = VGroup(dm.segs["b0"], dm.f2b, dm.segs["b1"], dm.h1, dm.segs["b2"]).copy().set_stroke(AMB, 6).set_z_index(12)
        brillo = Circle(radius=0.38, stroke_width=0).set_fill(AMB, 0.55).move_to(dm.h1.circ).set_z_index(12)
        self.play(Create(fal), FadeIn(brillo), run_time=0.5)
        al = pastilla("SOBRECARGA: KM1 cae · H1 enciende", AMB, 24, True).move_to([3.95, 3.4, 0]).set_z_index(30)
        self.play(FadeIn(al), run_time=0.3)
        self.wait_hasta(0.84)
        self.play(FadeOut(al), run_time=0.3)
        self.play(Indicate(self.rl.reset, color=WHITE, scale_factor=1.4), run_time=0.6)
        self.play(self.rl.test.animate.shift(UP * 0.25), mover(dm.f2a, True), mover(dm.f2b, False), FadeOut(fal), FadeOut(brillo), run_time=0.4)
        self.unzoom()
        nota = pastilla("rearme ≠ arranque: hay que pulsar MARCHA", VERDE_OK, 24, True).move_to([3.95, 3.95, 0]).set_z_index(30)
        self.play(FadeIn(nota), run_time=0.3)
        self.cerrar_voz()
        self.limpiar(card, dm, nota)

    # ================================================================ errores y final
    def mini_mando(self, error):
        g = VGroup()
        s0 = pulsador(False, "S0", None, None, largo=0.8).move_to([0, 0.9, 0])
        s1 = pulsador(error != 2, "S1", None, None, largo=0.8).move_to([0, -0.3, 0])
        if error == 2:
            s0 = pulsador(True, "S0", None, None, largo=0.8).move_to([0, 0.9, 0])
            s1 = pulsador(True, "S1", None, None, largo=0.8).move_to([0, -0.3, 0])
        km = contacto(True, contactor=True, largo=0.8).move_to([1.0, -0.3 if error != 1 else 0.3, 0])
        g.add(Line([0, 1.6, 0], s0[0].get_start()), s0, Line(s0[1].get_end(), s1[0].get_start()), s1, Line(s1[1].get_end(), [0, -1.2, 0]))
        if error == 1:
            g.add(VMobject().set_points_as_corners([[0, 1.45, 0], [1.0, 1.45, 0], km[0].get_start()]), km, VMobject().set_points_as_corners([km[1].get_end(), [1.0, -0.95, 0], [0, -0.95, 0]]))
        else:
            g.add(VMobject().set_points_as_corners([[0, 0.3, 0], [1.0, 0.3, 0], km[0].get_start()]), km, VMobject().set_points_as_corners([km[1].get_end(), [1.0, -0.95, 0], [0, -0.95, 0]]))
        g.set_stroke(SIM, 3)
        return g

    def f_errores(self):
        self.voz("errores")
        self.play(FadeOut(self.tab), run_time=0.3)
        e1 = self.mini_mando(1)
        e1.add(equis(ROJO, 0.5).move_to([1.5, 1.0, 0]))
        e2 = self.mini_mando(2)
        e2.add(equis(ROJO, 0.5).move_to([-0.9, 0.9, 0]))
        e3 = termico_s00(1.0, ajuste=5.0)
        e3.add(equis(ROJO, 0.9).move_to(e3.dial))
        self.tres_errores([("1", "Enclavamiento\nantes del paro", "13-14 en paralelo con S0 y S1:\nya no se puede detener"),
                           ("2", "Paro con\ncontacto NA", "si un cable se corta,\nla máquina no para"),
                           ("3", "Térmico al máximo", "el dial va a la corriente\nde placa del motor")], [e1, e2, e3])

    def f_final(self):
        self.resumen_y_final("final", ["Lee el diagrama en reposo", "Sigue cada tramo de + a 0 V", "Mismo orden de fases en potencia",
                                       "Enclavamiento solo en paralelo con marcha", "Prueba en frío y ajusta el térmico a la placa"])


def breaker_mover(b):
    return b.palanca.animate.shift(UP * 0.42 * b.s)


class PortadaH23(Scene):
    """Miniatura 16:9 al estilo de las referencias del usuario: fondo gris claro, título con recuadro de color y el equipo dibujado."""
    def construct(self):
        from PIL import Image
        w, h = config.pixel_width, config.pixel_height
        x = np.linspace(0, 1, w)[None, :, None]
        y = np.linspace(0, 1, h)[:, None, None]
        a = np.array([244, 246, 248])[None, None, :]
        b = np.array([196, 202, 211])[None, None, :]
        t = np.clip(0.55 * x + 0.45 * y, 0, 1)
        img = (a * (1 - t) + b * t).astype(np.uint8)
        ruta = DIR / f"fondo_claro_{w}x{h}.png"
        Image.fromarray(np.broadcast_to(img, (h, w, 3)).copy()).save(ruta)
        self.camera.background_image = str(ruta)
        self.camera.init_background()
        TU = "#1BA8C4"; MO = "#6D28D9"; OS = "#1D2939"
        l1 = T("Mi primer", 64, OS, "HEAVY")
        l2t = T("ARRANQUE", 104, WHITE, "HEAVY")
        l2 = VGroup(Rectangle(width=l2t.width + 0.5, height=l2t.height + 0.42, stroke_width=0).set_fill(TU, 1), l2t)
        l3t = T("con contactores", 64, WHITE, "HEAVY")
        l3 = VGroup(Rectangle(width=l3t.width + 0.4, height=l3t.height + 0.34, stroke_width=0).set_fill(MO, 1), l3t)
        tit = VGroup(l1, l2, l3).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        tit.scale_to_fit_width(7.4)
        tit.move_to([-7.4 + tit.width / 2, 1.0, 0])
        sub = VGroup(Circle(radius=0.36, stroke_width=0).set_fill("#F79009", 1), T("borne por borne", 40, OS, "HEAVY")).arrange(RIGHT, buff=0.25)
        sub[0].add(T("✓", 34, WHITE, "HEAVY").move_to(sub[0]))
        sub.next_to(tit, DOWN, buff=0.5, aligned_edge=LEFT)
        arr = arrancador_s00(0.95, (3.5, 5.0), 3.9)
        arr.move_to([3.4, -0.55, 0])
        riel = riel_din(4.0, 0.95).move_to([3.4, arr.ct[1].get_center()[1], 0])
        bots = VGroup(pulsador_22("verde", 0.9, "S1", "I"), pulsador_22("rojo", 0.9, "S0", "O")).arrange(DOWN, buff=0.3).move_to([6.5, -0.4, 0])
        cab = VGroup(*[cable_ruta([arr.ct.b[n].tor.get_center(), arr.ct.b[n].tor.get_center() + UP * 1.4], NEGRO_POT, 9) for n in ("1/L1", "3/L2", "5/L3")],
                     *[cable_ruta([arr.ct.b[n].tor.get_center(), arr.ct.b[n].tor.get_center() + UP * 1.4], AZUL_DC, 9) for n in ("13", "A1")])
        self.add(riel, cab, arr, bots, tit, sub)

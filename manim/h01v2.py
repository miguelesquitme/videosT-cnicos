"""H01 v2 · Arranque directo · Trituradora de piedrín (horizontal) — con las Correcciones_V6 del usuario.
Guion: h01_guion.py · Diagramas literales: h01v2_diag.py · Equipos y cables: h01v2_lay.py (PNG en h01v2_eq/).
Render: FORMATO=h TEMA=negro VOZ=eleven manim -qh --disable_caching -o h01v2 h01v2.py H01v2
Previa: SOLO=gancho,mando FORMATO=h TEMA=negro VOZ=mudo PREVIEW=1 manim -ql ... """
from h01_arranque import H01, cinta, etiqueta, pastilla, sonido_tecleo, TXT, TXT2, LOGO   # noqa: F401
from h01_arranque import *                                                             # noqa: F401,F403
from h01_guion import GUION as G2, SECCIONES as S2, MATERIALES
from h01v2_lay import (Eq2, Cable, disposicion, hilos_mando, hilos_potencia, K, KD, KF, ROJO_M, NEUTRO_C, NEGRO_P,
                       PE_V, PE_A, TORN, cabeza, ruta_redondeada)
from h01v2_diag import diagrama_mando, diagrama_potencia, HILOS_MANDO, HILOS_POT

AMB = "#FDB022"
NARANJA_PLACA = "#D9682F"
GRIS_PUERTA = "#5B636D"


def eje_girando(mo, vel=14.0):
    """Eje del motor girando (vista lateral): chaveta y marcas que suben y bajan con el giro, sin flechas ni arcos."""
    x0, y0 = mo.mm(12.0, 123.0), mo.mm(46.5, 136.4)
    cx, cy = (x0[0] + y0[0]) / 2, (x0[1] + y0[1]) / 2
    L, R_ = y0[0] - x0[0], (x0[1] - y0[1]) / 2
    bandas = VGroup(*[Rectangle(width=L * 0.92, height=R_ * 0.28, stroke_width=0).set_fill(c, 1) for c in ("#3E444B", "#E9EEF2", "#565D65")])
    bandas.fase = 0.0
    desf = (0.0, 2.1, 4.2)

    def upd(m, dt):
        m.fase += dt * vel
        for b, d in zip(m, desf):
            a = m.fase + d
            s = np.sin(a)
            b.stretch_to_fit_height(max(R_ * 0.30 * abs(s), 1e-3))
            b.move_to([cx, cy + R_ * 0.78 * np.cos(a), 0])
            b.set_opacity(0.85 if s > 0 else 0.0)
    bandas.add_updater(upd)
    upd(bandas, 0)
    return bandas


def tabla(filas, anchos, x0, y0, alto=0.36, size=17, encabezado=None, col_enc="#0E9BB5"):
    g = VGroup()
    y = y0
    if encabezado:
        x = x0
        fila = VGroup()
        for t, w in zip(encabezado, anchos):
            fila.add(Rectangle(width=w, height=alto + 0.04, stroke_width=1, stroke_color="#2A3140").set_fill(col_enc, 1).move_to([x + w / 2, y - (alto + 0.04) / 2, 0]))
            fila.add(Text(t, font=SANS, font_size=size + 1, weight="HEAVY", color="#06121E").move_to([x + w / 2, y - (alto + 0.04) / 2, 0]))
            x += w
        g.add(fila)
        y -= alto + 0.04
    for i, f in enumerate(filas):
        lineas = max(len(str(c).split("\n")) for c in f)
        h = alto * (1 + 0.75 * (lineas - 1))
        x = x0
        fila = VGroup()
        for j, (t, w) in enumerate(zip(f, anchos)):
            fila.add(Rectangle(width=w, height=h, stroke_width=1, stroke_color="#2A3140").set_fill("#141922" if i % 2 else "#1B2130", 1).move_to([x + w / 2, y - h / 2, 0]))
            if t:
                tt = Paragraph(*str(t).split("\n"), font=SANS, font_size=size, color=TXT if j != 1 else "#FFFFFF", line_spacing=0.6,
                               weight="BOLD" if j == 1 else "NORMAL")
                if tt.width > w - 0.14:
                    tt.scale_to_fit_width(w - 0.14)
                tt.move_to([x + 0.08 + tt.width / 2 if j > 0 else x + w / 2, y - h / 2, 0])
                fila.add(tt)
            x += w
        g.add(fila)
        y -= h
    return g


class H01v2(H01):
    CARPETA_VOZ = "voz_h01v2"
    GUION = G2
    SECC = {k: v for k, v in zip(["gancho", "pregunta", "problema", "materiales", "mando", "potencia", "c_mando", "c_potencia", "tablero", "marcha", "cierre"], S2)}

    def construct(self):
        self.cinta_act = None
        self.paso_act = None
        orden = ["gancho", "pregunta", "problema", "materiales", "mando", "potencia", "c_mando", "c_potencia", "tablero", "marcha", "cierre"]
        solo = os.environ.get("SOLO")
        for paso in orden:
            if solo and paso not in solo.split(","):
                continue
            getattr(self, "h_" + paso)()

    # ------------------------------------------------------------------ utilidades
    def repartir(self, n, f=0.9):
        """Tiempos para n pasos repartidos dentro de la voz en curso."""
        t0 = self.renderer.time
        dur = self.fin_voz - t0
        return [t0 + dur * f * (i + 1) / n for i in range(n)]

    def hasta(self, t):
        w = t - self.renderer.time
        if w > 0.05:
            self.wait(w)

    def dibujar_parte(self, H, key, rt=1.2):
        g = H.partes[key]
        lineas = [m for m in g if getattr(m, "tipo", "") == "linea"]
        otros = [m for m in g if getattr(m, "tipo", "") != "linea"]
        self.add_sound(str(DIR / "sfx" / "tecleo_16.wav"), gain=-17)
        if lineas:
            self.play(LaggedStart(*[Create(m) for m in lineas], lag_ratio=0.12), run_time=rt)
        if otros:
            self.play(LaggedStart(*[FadeIn(m) if getattr(m, "tipo", "") == "punto" else Write(m) for m in otros], lag_ratio=0.05), run_time=0.6)

    def nota(self, texto, pos):
        n = etiqueta(texto, MARCA, 26).move_to(pos)
        if n.width > 5.6:
            n.scale_to_fit_width(5.6)
        anims = [FadeIn(n, shift=UP * 0.15)]
        if self.nota_act is not None:
            anims.append(FadeOut(self.nota_act, shift=UP * 0.15))
        self.play(*anims, run_time=0.35)
        self.nota_act = n

    def cambiar(self, viejo, nombre, k):
        """Reemplaza un equipo por otro estado (encendido, presionado, disparado) en el mismo lugar."""
        n = Eq2(nombre, k)
        n.img.scale_to_fit_height(viejo.img.height).move_to(viejo.img)
        n.set_z_index(viejo.z_index)
        self.remove(viejo)
        self.add(n)
        return n

    # =============================================================== 1 · GANCHO (dato curioso + pregunta)
    def h_gancho(self):
        self.voz("gancho")
        mo = Eq2("M1", 0.030).move_to([-3.2, -0.4, 0])
        self.play(FadeIn(mo, shift=UP * 0.3), run_time=0.8)
        eje = eje_girando(mo)
        self.add(eje)
        self.sfx("motor", -12)
        t = self.repartir(4)
        self.hasta(t[0])
        a = VGroup(T("CORRIENTE NORMAL", 24, TXT2, "BOLD"), T("26,5 A", 84, TXT, "HEAVY")).arrange(DOWN, buff=0.12).move_to([4.6, 2.2, 0])
        self.play(FadeIn(a, shift=LEFT * 0.3), run_time=0.6)
        self.hasta(t[1])
        b = VGroup(T("AL ARRANCAR", 24, TXT2, "BOLD"), T("178 A", 96, ROJO, "HEAVY"), T("≈ 7 veces · NEC T430.251(B), diseño B", 20, TXT2, "MEDIUM")).arrange(DOWN, buff=0.12).move_to([4.6, -0.6, 0])
        self.sfx("pop", -10)
        self.play(FadeIn(b, scale=1.15), run_time=0.6)
        self.hasta(t[2])
        q = T("¿Cómo lo protegemos sin que el breaker se dispare?", 36, AMB, "HEAVY").move_to([0, -3.55, 0])
        if q.width > 15:
            q.scale_to_fit_width(15)
        self.play(Write(q), run_time=1.2)
        self.cerrar_voz(0.2)
        self.voz("gancho2")
        pasos = VGroup(*[pastilla(s, MARCA, 26, i == 0) for i, s in enumerate(["CÁLCULO", "MANDO", "POTENCIA", "CONEXIÓN", "TABLERO", "MARCHA"])]).arrange(RIGHT, buff=0.18).move_to([0, 3.5, 0])
        t = self.repartir(6, 0.85)
        self.play(FadeOut(a), FadeOut(b), run_time=0.4)
        for i, p in enumerate(pasos):
            self.sfx("pop", -16)
            self.play(FadeIn(p, shift=DOWN * 0.2), run_time=0.3)
            self.hasta(t[i] - 0.3)
        self.cerrar_voz(0.3)
        eje.clear_updaters()
        self.salir()

    # =============================================================== 2 · PREGUNTA
    def h_pregunta(self):
        self.seccion("pregunta")
        self.voz("pregunta")
        a = VGroup(T("MOTOR", 30, TXT2, "BOLD"), T("26,5 A", 110, TXT, "HEAVY")).arrange(DOWN, buff=0.2).move_to([-4.0, 0.8, 0])
        b = VGroup(T("BREAKER", 30, TXT2, "BOLD"), T("80 A", 110, AMB, "HEAVY")).arrange(DOWN, buff=0.2).move_to([4.0, 0.8, 0])
        q = T("?", 160, ROJO, "HEAVY").move_to([0, 0.8, 0])
        t = self.repartir(4)
        self.play(FadeIn(a, shift=RIGHT * 0.3), run_time=0.6)
        self.play(FadeIn(b, shift=LEFT * 0.3), run_time=0.6)
        self.sfx("pop", -10)
        self.play(FadeIn(q, scale=1.4), run_time=0.4)
        self.hasta(t[1])
        c1 = etiqueta("BREAKER  →  corta el CORTOCIRCUITO y protege el CABLE", AMB, 28).move_to([0, -2.0, 0])
        self.play(FadeOut(q), FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.hasta(t[2])
        c2 = etiqueta("RELÉ TÉRMICO  →  protege al MOTOR de la SOBRECARGA", "#9E77ED", 28).move_to([0, -3.1, 0])
        self.sfx("pop", -10)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 3 · PROBLEMA REAL
    def h_problema(self):
        self.seccion("problema")
        self.voz("placa")
        mo = Eq2("M1", 0.030).move_to([0, -0.3, 0])
        self.play(FadeIn(mo), run_time=0.6)
        centro = mo.mm(169, 133)
        self.zoom(centro, 4.6, 1.0)
        # datos de la placa encerrados en rectángulos (px de la placa × 0,3 mm/px)
        def caja(x0, x1, fila, color):
            y = 392 + 18.5 * fila
            p0, p1 = mo.mm(x0 * 0.3, (y - 9) * 0.3), mo.mm(x1 * 0.3, (y + 9) * 0.3)
            r = Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), stroke_color=color, stroke_width=4).move_to((p0 + p1) / 2)
            return r
        cajas = [caja(444, 494, 0, AMB), caja(444, 548, 1, MARCA), caja(444, 548, 2, ROJO), caja(545, 618, 3, VERDE_OK)]
        t = self.repartir(5, 0.8)
        for i, c in enumerate(cajas):
            self.hasta(t[i])
            self.sfx("tic", -12)
            self.play(Create(c), run_time=0.45)
        self.hasta(t[4])
        self.zoom_fuera(0.8)
        red = etiqueta("RED: 208Y/120 V · 3~ · 60 Hz", MARCA, 30).move_to([0, -3.7, 0])
        self.play(FadeIn(red, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(FadeOut(VGroup(*cajas)), mo.animate.scale(0.42).move_to([-5.6, 2.6, 0]), red.animate.scale(0.6).move_to([-5.6, 1.35, 0]), run_time=0.8)
        tarjetas = [
            ("tabla", "NEC T430.250", ["10 hp · 208 V · trifásico"], "I tabla = 30,8 A", MARCA, [-0.3, 2.4, 0]),
            ("cable", "NEC 430.22", ["125 % × 30,8 = 38,5 A", "10 AWG no alcanza (35 A)"], "8 AWG THHN 75 °C", VERDE_OK, [5.0, 2.4, 0]),
            ("breaker", "NEC T430.52", ["250 % × 30,8 = 77 A", "→ siguiente estándar"], "-F2 · 3P · C80", AMB, [-5.3, -0.4, 0]),
            ("termico", "NEC 430.32(A)(1)", ["F.S. 1,25 → máx 125 % = 33,1 A", "rango 23–32 A"], "-F3 ajuste 26,5 A", "#9E77ED", [0.0, -0.4, 0]),
            ("contactor", "AC-3 a 208 V (UL)", ["32 A → 7,5 hp  ✗   38 A → 10 hp  ✓", "bobina 120 VAC"], "-KM1 · 38 A", "#22B8CF", [5.3, -0.4, 0]),
            ("mando_prot", "Mando 120 VAC (L-N)", ["breaker 1 polo, curva C", "cable 14 AWG"], "-F1 · 1P · C2", "#4C8DF6", [0.0, -2.95, 0]),
        ]
        hechas = []
        for clave, norma, lineas, res, col, pos in tarjetas:
            self.voz(clave)
            tj = self.tarjeta_calc(norma, lineas, res, col, pos)
            if clave == "mando_prot":
                tj.scale(0.85)
            self.escribir(tj)
            hechas.append(tj)
            self.cerrar_voz(0.1)
        self.wait(0.6)
        self.salir()

    # =============================================================== 4 · MATERIALES
    def h_materiales(self):
        self.seccion("materiales")
        self.voz("materiales")
        anchos = [1.25, 3.0, 7.6, 3.4]
        x0 = -sum(anchos) / 2
        paginas = [MATERIALES[:11], MATERIALES[11:]]
        pesos = [len(m[2]) + 12 for m in MATERIALES]
        acum = np.cumsum(pesos) / sum(pesos)
        t0 = self.renderer.time
        dur = self.fin_voz - t0
        idx = 0
        for pg, filas in enumerate(paginas):
            tb = tabla(filas, anchos, x0, 3.55, 0.5, 17, ["Cantidad", "Nombre", "Características", "Observación"])
            self.play(FadeIn(tb[0]), run_time=0.4)
            for fila in tb[1:]:
                self.sfx("pop", -18)
                self.play(FadeIn(fila, shift=UP * 0.1), run_time=0.3)
                self.hasta(t0 + dur * acum[idx] * 0.97 - 0.3)
                idx += 1
            if pg == 0:
                self.play(FadeOut(tb), run_time=0.4)
        self.cerrar_voz(0.4)
        self.wait(1.2)
        self.salir()

    # =============================================================== 5 · DIAGRAMA DE MANDO (tramo por tramo)
    def h_mando(self):
        self.seccion("mando")
        H = diagrama_mando(alto=7.75, centro=(-1.6, -0.3))
        self.play(FadeIn(H.fondo), run_time=0.4)
        notas = ["Fase L desde -X0", "-F1 · breaker de mando 1P C2", "-F3 · 95-96 NC del relé térmico", "-S0 · PARO · 11-12 NC",
                 "-S1 · ARRANQUE · 13-14 NA", "-KM1 13-14 · RETENCIÓN", "-KM1 A1-A2 bobina  ∥  -H1 verde", "Regreso al neutro N de -X0",
                 "-KM1 21-22 NC  →  -H2 roja"]
        self.nota_act = None
        for i in range(1, 10):
            self.voz(f"m{i}")
            self.nota(notas[i - 1], [4.6, 0.0, 0])
            self.dibujar_parte(H, f"m{i}", 1.3 if i not in (1, 8) else 1.0)
            self.cerrar_voz(0.05)
        self.play(FadeOut(self.nota_act), run_time=0.3)
        self.nota_act = None
        # funcionamiento
        self.voz("retencion")
        t = self.repartir(5, 0.95)
        h2 = Circle(radius=14.5 * H.s).move_to(H.P(317, 591)).set_fill("#FF3B30", 0.8).set_stroke(width=0)
        rama_off = VGroup(H.marca([(47, 51), (137, 51), (137, 186), (317, 186), (317, 576)]), H.marca([(317, 606), (317, 651)], "#7FC4F0"))
        self.play(Create(rama_off), FadeIn(h2), run_time=0.8)
        self.hasta(t[0])
        pulso = Circle(radius=0.16, color=AMB, stroke_width=5).move_to(H.P(112, 441))
        marcha = VGroup(H.marca([(137, 186), (137, 571)]), H.marca([(137, 611), (137, 651)], "#7FC4F0"))
        bob = Rectangle(width=40 * H.s, height=20 * H.s).move_to(H.P(137, 591)).set_fill(AMB, 0.7).set_stroke(width=0)
        self.play(Create(pulso), run_time=0.3)
        self.sfx("contactor", -10)
        cierra_13 = Line(H.P(227, 425), H.P(227, 457)).set_stroke(AMB, 6)
        reten = VGroup(H.marca([(137, 381), (227, 381), (227, 576)]), H.marca([(227, 606), (227, 651)], "#7FC4F0"), cierra_13)
        h1 = Circle(radius=14.5 * H.s).move_to(H.P(227, 591)).set_fill("#39E15A", 0.85).set_stroke(width=0)
        abre = Cross(scale_factor=0.12, stroke_color="#E5484D", stroke_width=5).move_to(H.P(325, 441))
        self.play(Create(marcha), FadeIn(bob), run_time=0.8)
        self.play(Create(reten), FadeIn(h1), FadeOut(h2), FadeOut(rama_off[0]), FadeOut(rama_off[1]), Create(abre), run_time=0.8)
        self.hasta(t[2])
        self.play(FadeOut(pulso), FadeOut(marcha[0]), run_time=0.5)
        sigue = VGroup(H.marca([(137, 186), (137, 381)]), H.marca([(137, 516), (137, 571)]), H.marca([(227, 470), (227, 516), (137, 516)]))
        self.play(Create(sigue), run_time=0.6)
        self.hasta(t[3])
        p0 = Circle(radius=0.16, color=ROJO, stroke_width=5).move_to(H.P(112, 337))
        self.play(Create(p0), run_time=0.3)
        self.sfx("contactor", -14)
        self.play(FadeOut(VGroup(sigue, reten, bob, h1, marcha[1], abre, p0)), FadeIn(h2), Create(rama_off), run_time=0.8)
        self.cerrar_voz(0.3)
        self.wait(0.4)
        self.salir()

    # =============================================================== 6 · DIAGRAMA DE POTENCIA
    def h_potencia(self):
        self.seccion("potencia")
        H = diagrama_potencia(alto=7.75, centro=(-2.2, -0.3))
        self.play(FadeIn(H.fondo), run_time=0.4)
        notas = ["-X0 · L1 L2 L3 N PE", "-F2 · breaker 3P C80", "-KM1 · contactos principales", "-F3 · relé térmico 23-32 A",
                 "-X1 → -M1 · T1 T2 T3 + PE"]
        self.nota_act = None
        for i in range(1, 6):
            self.voz(f"p_d{i}")
            self.nota(notas[i - 1], [4.9, 0.0, 0])
            self.dibujar_parte(H, f"pd{i}", 1.4 if i != 5 else 2.2)
            self.cerrar_voz(0.05)
        self.play(FadeOut(self.nota_act), run_time=0.3)
        self.nota_act = None
        self.wait(0.8)
        self.salir()

    # =============================================================== 7 · CONEXIÓN DEL MANDO
    def montar_tablero_conexion(self, diag):
        E = disposicion()
        placa = Rectangle(width=4.9, height=8.85, stroke_width=0).set_fill(NARANJA_PLACA, 1).move_to([0.9, -0.05, 0])
        puerta = Rectangle(width=3.75, height=8.85, stroke_width=0).set_fill(GRIS_PUERTA, 1).move_to([5.95, -0.05, 0])
        lp = T("PUERTA", 18, "#C9CED6", "HEAVY").move_to([5.95, -4.25, 0])
        H = diag(alto=7.9, centro=(-4.55, -0.25))
        return E, Group(placa, puerta, lp), H

    def tender(self, H, cables, marcas, rt=1.6):
        """Tiende los cables en los equipos y, al mismo tiempo, marca el tramo en el diagrama."""
        self.marcas = getattr(self, "marcas", [])
        self.marcas += marcas
        self.play(*[Create(c.conductor) for c in cables], *[Create(m) for m in marcas], run_time=rt)
        self.sfx("tornillo", -10)
        self.play(*[FadeIn(c.puntas) for c in cables], run_time=0.35)

    def lupa(self, punto, ancho=1.9, espera=0.7):
        fr = self.camera.frame
        c0, w0 = fr.get_center().copy(), fr.width
        self.play(fr.animate.set(width=ancho).move_to(punto), run_time=0.55)
        self.wait(espera)
        self.play(fr.animate.set(width=w0).move_to(c0), run_time=0.5)

    def h_c_mando(self):
        self.seccion("c_mando")
        self.voz("c_intro")
        E, fondo, H = self.montar_tablero_conexion(diagrama_mando)
        self.play(FadeIn(fondo), FadeIn(H.todo()), *[FadeIn(e) for e in E.values()], run_time=1.2)
        # muestra de puntera y marcador
        self.cerrar_voz(0.1)
        self.cables = Group()
        for clave, hs, marcas in hilos_mando(E):
            self.voz(clave)
            cs = [Cable(pts, col, "mando", n, ta, tb, ka, kb) for pts, col, n, ta, tb, ka, kb in hs]
            ms = [H.marca(tr) for key in marcas for tr in HILOS_MANDO[key]]
            self.tender(H, cs, ms, 1.4 + 0.5 * len(cs))
            self.cables.add(*cs)
            self.lupa(hs[0][0][-1], 1.9, 0.6)
            self.cerrar_voz(0.05)
            for m in ms:
                m.set_stroke(opacity=0.35)
        self.wait(0.6)
        self.E, self.fondo_tab = E, fondo
        self.play(FadeOut(H.todo()), *[FadeOut(m) for m in self.marcas], run_time=0.4)
        self.marcas = []

    # =============================================================== 8 · CONEXIÓN DE POTENCIA
    def h_c_potencia(self):
        if not hasattr(self, "E"):
            E, fondo, _ = self.montar_tablero_conexion(diagrama_mando)
            self.E, self.fondo_tab = E, fondo
            self.cables = Group(*[Cable(pts, col, "mando", n, ta, tb, ka, kb) for _, hs, _ in hilos_mando(E) for pts, col, n, ta, tb, ka, kb in hs])
            self.add(fondo, *E.values(), self.cables)
        E = self.E
        self.seccion("c_potencia")
        self.voz("p_intro")
        H = diagrama_potencia(alto=7.9, centro=(-4.55, -0.25))
        self.play(FadeIn(H.todo()), *[c.animate.set_opacity(0.3) for c in self.cables], run_time=0.8)
        self.cerrar_voz(0.1)
        P = hilos_potencia(E)
        self.cab_pot = Group()
        # alimentación de la red que llega a -X0 por abajo (lado de campo)
        X0 = E["X0"]
        red = Group()
        for b, col in (("1_b", NEGRO_P), ("2_b", NEGRO_P), ("3_b", NEGRO_P), ("4_b", NEUTRO_C), ("5_b", "PE")):
            a = X0.p(b)
            red.add(Cable([a, a + DOWN * 1.2], col, "pot", None, TORN["X"], TORN["X"], marcador=False))
        lred = T("Red 208Y/120 V", 16, TXT2, "BOLD").next_to(X0.img, DOWN, buff=0.02).shift(LEFT * 1.3)

        def tanda(clave, listas, marcas):
            self.voz(clave)
            cs = [Cable(pts, col, "pot", n, ta, tb) for pts, col, n, ta, tb in listas]
            ms = [H.marca(tr) for key in marcas for tr in HILOS_POT[key]]
            self.tender(H, cs, ms, 2.0)
            self.cab_pot.add(*cs)
            self.lupa(listas[0][0][-1], 2.2, 0.6)
            self.cerrar_voz(0.05)
        self.play(FadeIn(red), FadeIn(lred), run_time=0.5)
        tanda("p1", P["p1"], ["p1"])
        tanda("p2", P["p2"], ["p2"])
        # p3: el térmico se acopla al contactor
        self.voz("p3")
        F3, KM1 = E["F3"], E["KM1"]
        ms = [H.marca(tr) for tr in HILOS_POT["p3"]]
        self.zoom(KM1.p("4/T2") + DOWN * 0.25, 3.0, 0.6)
        self.play(F3.animate.shift(DOWN * 0.35), run_time=0.4)
        self.play(F3.animate.shift(UP * 0.35), *[Create(m) for m in ms], run_time=0.9)
        self.sfx("tornillo", -8)
        anillos = VGroup(*[Circle(radius=0.11, color=AMB, stroke_width=5).move_to(KM1.p(t)) for t in ("2/T1", "4/T2", "6/T3")])
        self.play(LaggedStart(*[Create(a) for a in anillos], lag_ratio=0.3), run_time=0.9)
        self.play(FadeOut(anillos), run_time=0.3)
        self.zoom_fuera(0.5)
        self.cerrar_voz(0.05)
        tanda("p4", P["p4"] + P["pe"], ["p4", "pe"])
        # p5: caja de bornes del motor (9 puntas en estrella, tensión baja)
        self.voz("p5")
        velo = Rectangle(width=16.5, height=9.5, stroke_width=0).set_fill("#000000", 0.82).set_z_index(30)
        cb = Eq2("CB", 0.040).move_to([1.8, -0.2, 0]).set_z_index(31)
        tit = T("Caja del motor · 9 puntas en estrella · 208 V", 26, TXT, "HEAVY").next_to(cb, UP, buff=0.2).set_z_index(31)
        ms = [H.marca(tr) for tr in HILOS_POT["p5"]]
        self.play(FadeIn(velo), FadeIn(cb), FadeIn(tit), *[Create(m) for m in ms], run_time=0.8)
        cables_m = Group()
        for tt, nm in (("T1", "T1"), ("T2", "T2"), ("T3", "T3")):
            a = cb.p(tt)
            c = Cable([a + UP * 1.9 + LEFT * 0.0, a + UP * 0.9, a], NEGRO_P, "pot", None, (4.0, "cruz"), (4.0, "cruz"), 0.040, 0.040)
            c.puntas[0].set_opacity(0)
            c.set_z_index(32)
            cables_m.add(c)
        for c in cables_m:
            for sm in c.get_family():
                sm.set_z_index(32)
        for c in cables_m:
            for g_ in c.puntas:
                g_.remove(g_[-1])          # en el motor el cable va con terminal de ojo bajo la tuerca, sin tornillo de cruz
        self.play(*[Create(c.conductor) for c in cables_m], run_time=1.0)
        self.play(FadeIn(Group(*[c.puntas[1] for c in cables_m])), run_time=0.3)
        t = self.repartir(4, 0.9)
        pares = [("T1", "T7"), ("T2", "T8"), ("T3", "T9")]
        for i, (a, b) in enumerate(pares):
            r = Line(cb.p(a), cb.p(b)).set_stroke(AMB, 14, opacity=0.6).set_z_index(33)
            self.sfx("tic", -10)
            self.play(Create(r), run_time=0.4)
            self.hasta(t[i])
        r = Line(cb.p("T4"), cb.p("T6")).set_stroke(AMB, 14, opacity=0.6).set_z_index(33)
        self.play(Create(r), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(*[FadeOut(m) for m in self.mobjects if getattr(m, "z_index", 0) >= 30], run_time=0.5)
        # p6: ajuste del dial
        self.voz("p6")
        dial = F3.mm(196 * 45 / 685, 222 * 45 / 685)
        self.zoom(dial, 1.8, 0.8)
        lab = etiqueta("ajuste 26,5 A", AMB, 22).scale(0.22).next_to(dial, UP, buff=0.42)
        self.sfx("tic", -8)
        self.play(FadeIn(lab), Indicate(F3.img, scale_factor=1.0, color=AMB), run_time=0.7)
        self.cerrar_voz(0.2)
        self.play(FadeOut(lab), run_time=0.3)
        self.zoom_fuera(0.6)
        self.play(FadeOut(H.todo()), *[FadeOut(m) for m in self.marcas], *[c.animate.set_opacity(1) for c in self.cables], run_time=0.6)
        self.marcas = []
        self.salir()

    # =============================================================== 9 · TABLERO (gabinete real por etapas)
    def armar_gabinete(self, centro=(-3.6, -0.15), alto=8.3, animar=True):
        """Gabinete 500 × 400 × 200 mm con plancha, canaletas ranuradas 40 × 40, rieles DIN y equipos."""
        kt = alto / 500.0
        cx, cy = centro
        def P(xmm, ymm):                       # mm desde la esquina superior izquierda del gabinete
            return np.array([cx + (xmm - 200) * kt, cy - (ymm - 250) * kt, 0])
        g = {}
        caja = Rectangle(width=400 * kt, height=500 * kt, stroke_color="#9AA3AD", stroke_width=6).set_fill("#B9C0C8", 1).move_to(P(200, 250))
        interior = Rectangle(width=370 * kt, height=470 * kt, stroke_color="#7D8690", stroke_width=3).set_fill("#8C949D", 1).move_to(P(200, 250))
        g["gabinete"] = VGroup(caja, interior)
        g["plancha"] = Rectangle(width=350 * kt, height=450 * kt, stroke_width=0).set_fill(NARANJA_PLACA, 1).move_to(P(200, 250))
        # canaletas ranuradas (40 mm): arriba, entre filas, abajo y a los lados
        def canaleta(x0, y0, x1, y1):
            w, h = (x1 - x0) * kt, (y1 - y0) * kt
            base = Rectangle(width=w, height=h, stroke_color="#6E767F", stroke_width=2).set_fill("#9EA6AE", 1).move_to(P((x0 + x1) / 2, (y0 + y1) / 2))
            tapa = Rectangle(width=w * (0.62 if w < h else 1), height=h * (0.62 if h <= w else 1), stroke_width=0).set_fill("#C5CBD1", 1).move_to(base)
            dientes = VGroup()
            if w > h:
                for x in np.arange(x0 + 6, x1 - 4, 12):
                    for yy in (y0 + 4, y1 - 4):
                        dientes.add(Rectangle(width=5 * kt, height=8 * kt, stroke_width=0).set_fill("#5A626B", 1).move_to(P(x, yy)))
            else:
                for y in np.arange(y0 + 6, y1 - 4, 12):
                    for xx in (x0 + 4, x1 - 4):
                        dientes.add(Rectangle(width=8 * kt, height=5 * kt, stroke_width=0).set_fill("#5A626B", 1).move_to(P(xx, y)))
            return VGroup(base, dientes, tapa)
        filas_c = [(30, 30, 370, 70), (30, 170, 370, 210), (30, 340, 370, 380), (30, 440, 370, 475)]
        g["canaletas"] = VGroup(*[canaleta(*f) for f in filas_c], canaleta(30, 70, 70, 440), canaleta(330, 70, 370, 440))
        def riel(y):
            r = Rectangle(width=250 * kt, height=35 * kt, stroke_color="#8D949B", stroke_width=2).set_fill("#D6DADF", 1).move_to(P(200, y))
            ran = VGroup(*[RoundedRectangle(width=15 * kt, height=5 * kt, corner_radius=2.4 * kt, stroke_width=0).set_fill("#7E858C", 1).move_to(P(x, y)) for x in np.arange(90, 315, 25)])
            return VGroup(r, ran)
        ys = (120, 275, 410)
        g["rieles"] = VGroup(*[riel(y) for y in ys])
        g["tornillos"] = VGroup(*[Circle(radius=4 * kt).set_fill("#3A3F45", 1).set_stroke("#1B1F24", 1).move_to(P(x, y)) for y in ys for x in (85, 315)])
        # equipos (mismas piezas de la biblioteca, a escala del gabinete)
        e = {}
        e["F2"] = Eq2("F2", kt).poner(*P(120, 120 - 40.3)[:2])
        e["F1"] = Eq2("F1", kt).poner(*P(186, 120 - 40.3)[:2])
        e["KM1"] = Eq2("KM1", kt).poner(*P(128, 275 - 60)[:2])
        e["F3"] = Eq2("F3", kt).poner(*P(128, 275 - 60 + 72.7)[:2])
        e["KM1"].set_z_index(2)
        e["F3"].set_z_index(1)
        e["X0"] = Eq2("X0", kt).poner(*P(95, 410 - 25.5)[:2])
        e["X1"] = Eq2("X1", kt).poner(*P(180, 410 - 25.5)[:2])
        g["equipos"] = e
        # puerta abierta a la derecha con los operadores
        kp = kt * 1.0
        x_p = P(400, 0)[0] + 0.35
        puerta = Rectangle(width=400 * kt * 0.45, height=500 * kt, stroke_color="#9AA3AD", stroke_width=6).set_fill("#6A737D", 1)
        puerta.move_to([x_p + puerta.width / 2, cy, 0])
        g["puerta"] = puerta
        ops = {}
        xs = puerta.get_center()[0]
        for n, yy in (("S1", 2.15), ("S0", 0.55), ("H1", -1.05), ("H2", -2.65)):
            ops[n] = Eq2(n, kp * 1.7).move_to([xs, cy + yy, 0])
        g["ops"] = ops
        g["P"], g["kt"] = P, kt
        return g

    def h_tablero(self):
        self.seccion("tablero")
        g = self.armar_gabinete()
        P = g["P"]
        self.voz("t1")
        self.play(FadeIn(g["gabinete"], shift=UP * 0.2), run_time=0.9)
        cot = VGroup(T("500 mm", 20, TXT2, "BOLD").rotate(PI / 2).next_to(g["gabinete"], LEFT, buff=0.12),
                     T("400 mm", 20, TXT2, "BOLD").next_to(g["gabinete"], DOWN, buff=0.08))
        self.play(FadeIn(cot), run_time=0.4)
        self.cerrar_voz(0.05)
        self.voz("t2")
        self.play(FadeIn(g["plancha"], shift=DOWN * 0.15), run_time=0.8)
        self.cerrar_voz(0.05)
        self.voz("t3")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in g["canaletas"]], lag_ratio=0.25), run_time=1.6)
        self.cerrar_voz(0.05)
        self.voz("t4")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in g["rieles"]], lag_ratio=0.3), run_time=1.2)
        for tr in g["tornillos"]:
            self.sfx("tornillo", -14)
            self.play(FadeIn(tr, scale=1.6), run_time=0.18)
        self.cerrar_voz(0.05)
        self.voz("t5")
        e = g["equipos"]
        t = self.repartir(3, 0.9)
        self.sfx("breaker", -10)
        self.play(FadeIn(e["F2"], shift=DOWN * 0.3), FadeIn(e["F1"], shift=DOWN * 0.3), run_time=0.6)
        self.hasta(t[0])
        self.sfx("contactor", -10)
        self.play(FadeIn(e["KM1"], shift=DOWN * 0.3), FadeIn(e["F3"], shift=DOWN * 0.3), run_time=0.6)
        self.hasta(t[1])
        self.sfx("tic", -10)
        self.play(FadeIn(e["X0"], shift=DOWN * 0.3), FadeIn(e["X1"], shift=DOWN * 0.3), run_time=0.6)
        self.cerrar_voz(0.05)
        self.voz("t6")
        self.play(FadeIn(g["puerta"], shift=LEFT * 0.3), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(o, scale=0.9) for o in g["ops"].values()], lag_ratio=0.2), run_time=1.2)
        self.cerrar_voz(0.05)
        self.voz("t7")
        cables = self.cables_gabinete(g)
        self.play(LaggedStart(*[Create(c) for c in cables], lag_ratio=0.04), run_time=3.0)
        self.cerrar_voz(0.3)
        self.gab = g
        self.cab_gab = cables
        self.cot = cot

    def cables_gabinete(self, g):
        """Cableado en el gabinete: cada borne sale con su cable curvo hacia la canaleta más cercana (como en un tablero real)."""
        P, kt, e = g["P"], g["kt"], g["equipos"]
        y_can = {"sup": P(0, 50)[1], "m1": P(0, 190)[1], "m2": P(0, 360)[1], "inf": P(0, 457)[1]}
        out = VGroup()
        def baja(p, y, col, w):
            m = ruta_redondeada([p, [p[0], (p[1] + y) / 2, 0], [p[0], y, 0]])
            return fisico(VGroup(m.copy().set_stroke("#000000", w + 2), m.set_stroke(col, w)))
        def c(e_, b, destino, col, w):
            return baja(e_.p(b), y_can[destino], col, w)
        wp, wm = 6.0, 3.5
        for b in ("1", "3", "5"):
            out.add(c(e["F2"], b, "sup", NEGRO_P, wp))
        for b in ("2", "4", "6"):
            out.add(c(e["F2"], b, "m1", NEGRO_P, wp))
        out.add(c(e["F1"], "1", "sup", ROJO_M, wm), c(e["F1"], "2", "m1", ROJO_M, wm))
        for b in ("1/L1", "3/L2", "5/L3", "13", "21", "A1"):
            out.add(c(e["KM1"], b, "m1", NEGRO_P if "/" in b else ROJO_M, wp if "/" in b else wm))
        for b, col in (("2/T1", NEGRO_P), ("4/T2", NEGRO_P), ("6/T3", NEGRO_P), ("95", ROJO_M), ("96", ROJO_M)):
            out.add(c(e["F3"], b, "m2", col, wp if col == NEGRO_P else wm))
        for b, col in (("1_a", NEGRO_P), ("2_a", NEGRO_P), ("3_a", NEGRO_P), ("4_a", NEUTRO_C), ("5_a", "#1E9E3E")):
            out.add(c(e["X0"], b, "m2", col, wp))
        for b, col in (("1_a", NEGRO_P), ("2_a", NEGRO_P), ("3_a", NEGRO_P), ("4_a", "#1E9E3E")):
            out.add(c(e["X1"], b, "m2", col, wp))
        for b, col in (("1_b", NEGRO_P), ("2_b", NEGRO_P), ("3_b", NEGRO_P), ("4_b", NEUTRO_C), ("5_b", "#1E9E3E")):
            out.add(c(e["X0"], b, "inf", col, wp))
        # mazo hacia la puerta (cable flexible que pasa por la bisagra)
        pu = g["puerta"]
        a = P(370, 300)
        maz = ruta_redondeada([a, [a[0] + 0.25, a[1], 0], [pu.get_left()[0] + 0.25, a[1] - 0.6, 0], [pu.get_left()[0] + 0.25, pu.get_top()[1] - 0.6, 0]], 0.3)
        out.add(fisico(VGroup(maz.copy().set_stroke("#000", 9), maz.copy().set_stroke(ROJO_M, 6), maz.copy().shift(RIGHT * 0.05).set_stroke(NEUTRO_C, 4))))
        for o in g["ops"].values():
            q = o.img.get_left() + RIGHT * 0.05
            ruta = ruta_redondeada([[pu.get_left()[0] + 0.25, q[1] + 0.3, 0], [pu.get_left()[0] + 0.25, q[1], 0], q])
            out.add(fisico(VGroup(ruta.copy().set_stroke("#000", 7), ruta.set_stroke(ROJO_M, 4))))
        return out

    # =============================================================== 10 · PUESTA EN MARCHA
    def h_marcha(self):
        if not hasattr(self, "gab"):
            g = self.armar_gabinete()
            cab = self.cables_gabinete(g)
            self.add(g["gabinete"], g["plancha"], g["canaletas"], g["rieles"], g["tornillos"], *g["equipos"].values(), g["puerta"], *g["ops"].values(), cab)
            self.gab, self.cab_gab = g, cab
            self.cot = VGroup()
        self.seccion("marcha")
        g = self.gab
        e, ops = g["equipos"], g["ops"]
        todo = Group(*[m for m in self.mobjects if m is not self.cinta_act and m is not self.camera.frame and m is not self.cot and all(m is not f for f in self._fondo)])
        self.play(todo.animate.scale(0.82).move_to([-3.6, -0.1, 0]), FadeOut(self.cot), run_time=0.9)
        for q in list(e.values()) + list(ops.values()):
            q.k *= 0.82
        # motor a la derecha con su cable desde -X1
        mo = Eq2("M1", 0.0145).move_to([4.6, 2.3, 0])
        cab_m = VGroup()
        cj = mo.mm(146, 55)
        self.x_t1 = None
        for i, (b, col) in enumerate((("1_b", NEGRO_P), ("2_b", NEGRO_P), ("3_b", NEGRO_P), ("4_b", PE_V))):
            a = e["X1"].p(b)
            xv = 2.55 + 0.14 * i
            yt = cj[1] + 0.25 + 0.1 * (3 - i)
            m = ruta_redondeada([a, [a[0], -4.05 - 0.09 * i, 0], [xv, -4.05 - 0.09 * i, 0], [xv, yt, 0], [cj[0] - 0.15 + 0.1 * i, yt, 0], [cj[0] - 0.15 + 0.1 * i, cj[1], 0]], 0.18)
            cab_m.add(fisico(VGroup(m.copy().set_stroke("#80868D" if col == NEGRO_P else "#0E3B1A", 7), m.set_stroke(col, 5))))
            if i == 0:
                self.x_t1 = xv
        self.play(FadeIn(mo), Create(cab_m), run_time=1.0)
        # prueba en frío
        self.voz("prueba_frio")
        mm = Eq2("MM", 0.016).move_to([4.6, -1.6, 0])
        self.play(FadeIn(mm, shift=LEFT * 0.3), run_time=0.5)
        a, b = e["F1"].p("2"), e["X0"].p("4_a")
        puntas = VGroup(cable(mm.p("VΩ"), mm.p("VΩ") + DOWN * 0.4, [a[0] + 1.2, -4.0, 0], a + DOWN * 0.2, a, color=ROJO, w=4, suave=True),
                        cable(mm.p("COM"), mm.p("COM") + DOWN * 0.6, [b[0] + 1.0, -4.3, 0], b + DOWN * 0.25, b, color="#2B2C2E", w=4, suave=True))
        self.play(Create(puntas), run_time=1.0)
        lcd = mm.mm(48.7, 47.0)
        tapa = VGroup(Rectangle(width=60 * mm.k, height=30 * mm.k, stroke_width=0).set_fill("#C9D1C0", 1), Text("R bobina", font=SANS, font_size=20, weight="BOLD", color="#1B1F24")).move_to(lcd)
        tapa[1].scale_to_fit_width(tapa[0].width * 0.8).move_to(tapa[0])
        t = self.repartir(3, 0.9)
        self.hasta(t[0])
        s1p = self.cambiar(ops["S1"], "S1p", ops["S1"].k)
        lec = etiqueta("ARRANQUE pulsado → resistencia de la bobina", VERDE_OK, 24).move_to([2.6, 3.75, 0]).scale(0.85)
        self.play(FadeIn(tapa), FadeIn(lec), run_time=0.6)
        self.hasta(t[1])
        ops["S1"] = self.cambiar(s1p, "S1", s1p.k)
        s0p = self.cambiar(ops["S0"], "S0p", ops["S0"].k)
        lec2 = etiqueta("PARO pulsado → OL (circuito abierto)", ROJO, 24).move_to([2.6, 3.75, 0]).scale(0.85)
        self.play(FadeOut(tapa), FadeTransform(lec, lec2), run_time=0.6)
        self.cerrar_voz(0.1)
        ops["S0"] = self.cambiar(s0p, "S0", s0p.k)
        self.play(FadeOut(puntas), FadeOut(lec2), run_time=0.4)
        # tensión
        self.voz("prueba_tension")
        self.sfx("breaker", -6)
        e["F2"] = self.cambiar(e["F2"], "F2on", e["F2"].k)
        self.play(Flash(e["F2"].img.get_center(), color=VERDE_OK, line_length=0.2), run_time=0.5)
        a, b = e["X0"].p("1_b"), e["X0"].p("2_b")
        puntas = VGroup(cable(mm.p("VΩ"), mm.p("VΩ") + DOWN * 0.4, [a[0] + 1.2, -4.0, 0], a + DOWN * 0.2, a, color=ROJO, w=4, suave=True),
                        cable(mm.p("COM"), mm.p("COM") + DOWN * 0.6, [b[0] + 1.0, -4.3, 0], b + DOWN * 0.25, b, color="#2B2C2E", w=4, suave=True))
        self.play(Create(puntas), run_time=0.8)
        v = etiqueta("L1-L2 = L2-L3 = L1-L3 = 208 V   ·   L-N = 120 V", AMB, 24).move_to([2.6, 3.75, 0]).scale(0.85)
        self.play(FadeIn(v), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(FadeOut(puntas), FadeOut(v), FadeOut(mm), run_time=0.4)
        # marcha
        self.voz("marcha")
        t = self.repartir(3, 0.9)
        self.sfx("breaker", -6)
        e["F1"] = self.cambiar(e["F1"], "F1on", e["F1"].k)
        ops["H2"] = self.cambiar(ops["H2"], "H2on", ops["H2"].k)
        self.play(Flash(ops["H2"].img.get_center(), color="#FF3B30", line_length=0.25), run_time=0.5)
        self.hasta(t[0])
        s1p = self.cambiar(ops["S1"], "S1p", ops["S1"].k)
        self.wait(0.3)
        self.sfx("contactor", -6)
        e["KM1"] = self.cambiar(e["KM1"], "KM1on", e["KM1"].k)
        ops["H1"] = self.cambiar(ops["H1"], "H1on", ops["H1"].k)
        ops["H2"] = self.cambiar(ops["H2"], "H2", ops["H2"].k)
        ops["S1"] = self.cambiar(s1p, "S1", s1p.k)
        self.play(Flash(ops["H1"].img.get_center(), color="#39E15A", line_length=0.25), run_time=0.5)
        self.hasta(t[1])
        self.sfx("motor", -8)
        eje = eje_girando(mo, 16.0)
        self.add(eje)
        self.cerrar_voz(0.1)
        # corriente con la pinza (una sola fase)
        self.voz("corriente")
        pz = Eq2("PZ", 0.011)
        H_, W_ = pz.img.height, pz.img.width
        jaw = np.array([self.x_t1, -0.7, 0])
        pz.img.move_to(jaw + DOWN * (0.29 * H_) + LEFT * (0.007 * W_))
        pz.set_z_index(8)
        nota = Paragraph("una sola fase (T1)", "dentro de la pinza", font=SANS, font_size=18, color=TXT2).next_to(pz, RIGHT, buff=0.15)
        self.play(FadeIn(pz, shift=LEFT * 0.3), FadeIn(nota), run_time=0.6)
        ok = etiqueta("corriente de trabajo < 26,5 A de placa  ✓", VERDE_OK, 24).move_to([2.6, 3.75, 0]).scale(0.85)
        self.play(FadeIn(ok), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(FadeOut(pz), FadeOut(nota), FadeOut(ok), run_time=0.4)
        # disparo del térmico con TEST
        self.voz("disparo")
        t = self.repartir(4, 0.92)
        self.zoom(e["F3"].img.get_center(), 3.0, 0.6)
        self.sfx("disparo", -4)
        e["F3"] = self.cambiar(e["F3"], "F3tr", e["F3"].k)
        self.play(Flash(e["F3"].img.get_center() + LEFT * 0.2, color=ROJO, line_length=0.18), run_time=0.5)
        self.zoom_fuera(0.5)
        self.sfx("motor_para", -8)
        eje.clear_updaters()
        self.remove(eje)
        e["KM1"] = self.cambiar(e["KM1"], "KM1", e["KM1"].k)
        ops["H1"] = self.cambiar(ops["H1"], "H1", ops["H1"].k)
        ops["H2"] = self.cambiar(ops["H2"], "H2on", ops["H2"].k)
        self.hasta(t[1])
        s1p = self.cambiar(ops["S1"], "S1p", ops["S1"].k)
        no = etiqueta("ARRANQUE pulsado → no arranca", ROJO, 24).move_to([2.6, 3.75, 0]).scale(0.85)
        self.play(FadeIn(no), run_time=0.4)
        ops["S1"] = self.cambiar(s1p, "S1", s1p.k)
        self.hasta(t[2])
        e["F3"] = self.cambiar(e["F3"], "F3", e["F3"].k)
        rs = etiqueta("RESET → listo para arrancar", "#4C8DF6", 24).move_to([2.6, 3.75, 0]).scale(0.85)
        self.sfx("tic", -6)
        self.play(FadeTransform(no, rs), run_time=0.6)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 11 · CIERRE
    def h_cierre(self):
        self.seccion("cierre")
        self.voz("cierre")
        lg = ImageMobject(str(LOGO)).scale_to_fit_width(2.8).move_to([0, 1.6, 0])
        us = T("@miguelesquit", 40, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        yt = VGroup(pastilla("SUSCRÍBETE", ROJO, 34, True), pastilla("SÍGUEME", MARCA, 34, True)).arrange(RIGHT, buff=0.4).next_to(us, DOWN, buff=0.45)
        sig = T("Mira mi siguiente video", 34, TXT, "HEAVY").next_to(yt, DOWN, buff=0.55)
        self.play(FadeIn(lg, scale=0.8), FadeIn(us), run_time=0.7)
        self.play(FadeIn(yt, scale=1.15), run_time=0.5)
        self.esperar_frac(0.55)
        self.play(FadeIn(sig, shift=UP * 0.2), run_time=0.6)
        self.cerrar_voz(0.2)
        self.wait(5.0)

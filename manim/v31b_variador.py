"""V31b · ASÍ FUNCIONA UN VARIADOR DE FRECUENCIA — Short técnico (prueba de la nueva línea, 18-nov-2026).
Render: FORMATO=v VOZ=eleven manim -qh --disable_caching -o final_v31b v31b_variador.py V31b
"""
from shorts_c import *  # noqa
import shorts_v
from piezas_auto2 import carta as _carta, etiqueta as _etiqueta
from piezas_vfd import *
from guion_vfd import TIT1, TIT2, GUION

shorts_v.SHORTS["v31b"] = (TIT1, TIT2, GUION)

AMB = "#FDB022"; CY = "#38E8FF"; RJ = "#FF5A5F"; VD = "#3DDC84"; AZ = "#7AA7FF"
FONDO_BANDA = "#0A0F2C"


def card(titulo, lineas=(), color=MARCA, w=7.8, size=28):
    m = _carta(titulo, lineas, color, w, size)
    return m.scale_to_fit_width(8.4) if m.width > 8.4 else m


def tag(texto, color=MARCA, size=30):
    m = _etiqueta(texto, color, size)
    return m.scale_to_fit_width(8.4) if m.width > 8.4 else m


def flecha(a, b, color=WHITE, sw=4):
    return Arrow(a, b, buff=0.05, stroke_width=sw, color=color, max_tip_length_to_length_ratio=0.18)


def ejes(x_len=7.6, y_len=2.6, xr=(0, 1, 0.25), yr=(-1.2, 1.2, 1)):
    return Axes(x_range=list(xr), y_range=list(yr), x_length=x_len, y_length=y_len, tips=False,
                axis_config={"color": "#5B6B9A", "stroke_width": 2, "include_ticks": False})


class V31b(ShortC):
    CLAVE = "v31b"

    # ------------------------------------------------------------------ marco fijo
    def construct(self):
        banda = Rectangle(width=9.2, height=3.55, stroke_width=0).set_fill(FONDO_BANDA, 1).move_to([0, 6.3, 0])
        linea = Line([-4.6, 4.53, 0], [4.6, 4.53, 0]).set_stroke(MARCA, 4)
        t1 = T(TIT1, 40, WHITE, "HEAVY")
        t2 = T(TIT2, 62, MARCA, "HEAVY")
        tt = VGroup(t1, t2).arrange(DOWN, buff=0.12).move_to([0, 5.55, 0])
        for m in tt:
            if m.width > 8.2:
                m.scale_to_fit_width(8.2)
        self.marco = VGroup(banda, linea, tt).set_z_index(50)
        self.add(self.marco)
        self.chip_act = None
        self.cuerpo()
        resto = DUR_MIN - self.renderer.time
        if resto > 0:
            self.wait(resto)

    def chip(self, num, texto, color=MARCA):
        n = VGroup(Square(0.62, stroke_width=0).set_fill(color, 1), T(num, 30, "#0B1030", "HEAVY"))
        t = T(texto, 30, WHITE, "HEAVY")
        caja = RoundedRectangle(width=t.width + 0.5, height=0.62, corner_radius=0.04, stroke_width=0).set_fill("#141B4A", 1)
        t.move_to(caja)
        g = VGroup(n, VGroup(caja, t)).arrange(RIGHT, buff=0).move_to([0, 4.0, 0]).align_to([-4.2, 0, 0], LEFT).set_z_index(49)
        anim = [FadeIn(g, shift=RIGHT * 0.3)]
        if self.chip_act is not None:
            anim.append(FadeOut(self.chip_act, shift=LEFT * 0.3))
        self.play(*anim, run_time=0.35)
        self.chip_act = g

    def zoom(self, mob, punto, factor, destino, rt=1.0):
        punto = np.array(punto, float)
        self.play(mob.animate.scale(factor, about_point=punto).shift(np.array(destino, float) - punto), run_time=rt, rate_func=smooth)

    def zoom_a(self, mob, sub, ancho, destino, rt=1.0, marco=True):
        f = ancho / sub.width
        if marco:
            r = SurroundingRectangle(sub, color=CY, buff=0.06, corner_radius=0.04, stroke_width=4)
            self.play(Create(r), run_time=0.3)
            mob.add(r)
        self.zoom(mob, sub.get_center(), f, destino, rt)
        if marco:
            self.play(FadeOut(r), run_time=0.2)
            mob.remove(r)

    def flujo(self, pts, color=CY, vel=2.2, esc=1.4):
        c = corriente([np.array(p, float) for p in pts], vel=vel, escala=esc, color=color)
        self.add(c)
        return c

    # ------------------------------------------------------------------ guion visual
    def cuerpo(self):
        self.s_gancho()
        self.s_ext()
        self.s_bloques_rect_pre_bus()
        self.s_seguridad()
        self.s_inversor_pwm()
        self.s_vhz()
        self.s_rampa()
        self.s_frenado()
        self.s_campo()
        self.s_dato()
        self.final("Rectifica · filtra · invierte")

    # ---------------------------------------------------------------- 0 · gancho
    def s_gancho(self):
        self.voz("gancho")
        mot = motor_tefc(1.2).move_to([0.2, 1.3, 0])
        self.play(FadeIn(mot, shift=UP * 0.2), run_time=0.5)
        girar_eje(mot, 3.0)
        ins = VGroup(tag("60 Hz", MARCA, 34), tag("4 polos", "#475467", 34)).arrange(RIGHT, buff=0.25).move_to([0, -0.9, 0])
        self.play(FadeIn(ins, shift=UP * 0.15), run_time=0.35)
        f = MathTex(r"n_s=\frac{120\,f}{p}=\frac{120\cdot 60}{4}=1800\ \text{rpm}", color=WHITE).scale(0.95).move_to([0, -2.3, 0])
        self.frac(0.12)
        self.play(Write(f), run_time=0.9)
        real = tag("con carga: ≈ 1750 rpm (deslizamiento)", AMB, 28).move_to([0, -3.4, 0])
        self.play(FadeIn(real), run_time=0.3)
        self.frac(0.35)
        clave = card("PARA CAMBIAR LA VELOCIDAD", ["cambia la FRECUENCIA"], RJ, 7.8, 30).move_to([0, -4.9, 0])
        self.play(FadeIn(clave, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)
        mot.chaveta.clear_updaters()
        self.limpiar(mot, ins, f, real, clave)

    # ---------------------------------------------------------------- 1 · por fuera
    def s_ext(self):
        self.voz("ext")
        self.chip("1", "POR FUERA")
        v = variador(1.35).move_to([0, -1.25, 0])
        self.play(FadeIn(v, shift=UP * 0.3), run_time=0.6)
        self.frac(0.04)
        # teclado
        self.zoom_a(v, v.teclado, 6.4, [0, 0.4, 0], 1.0)
        l1 = VGroup(tag("display: frecuencia de salida", CY, 26).move_to([0, 3.2, 0]),
                    tag("RUN / STOP", VD, 26).move_to([-2.4, -2.7, 0]), tag("potenciómetro", AMB, 26).move_to([2.4, -2.7, 0]))
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in l1], lag_ratio=0.3), run_time=0.8)
        self.frac(0.25)
        self.play(FadeOut(l1), run_time=0.25)
        # bornera de potencia
        bp = v.bp
        self.zoom_a(v, v.pot_bloque, 8.4, [0, 0.4, 0], 1.1)
        def sobre(nombres, txt, col, y):
            grp = VGroup(*[bp[n] for n in nombres])
            br = Brace(grp, DOWN, color=col, buff=0.12)
            t = tag(txt, col, 24).next_to(br, DOWN, buff=0.12)
            if t.get_left()[0] < -4.3:
                t.shift(RIGHT * (-4.3 - t.get_left()[0]))
            if t.get_right()[0] > 4.3:
                t.shift(LEFT * (t.get_right()[0] - 4.3))
            return VGroup(br, t)
        a = sobre(["L1", "L2", "L3"], "ALIMENTACIÓN 3F", CY, 0)
        b = sobre(["U", "V", "W"], "SALIDA AL MOTOR", VD, 0)
        c = sobre(["+", "−", "BR"], "BUS DC + FRENO", AMB, 0)
        c.shift(DOWN * 1.15)
        self.play(FadeIn(a), run_time=0.35)
        self.frac(0.12)
        self.play(FadeIn(b), run_time=0.35)
        self.frac(0.12)
        pe = tag("PE: tierra del equipo y del motor", "#12B76A", 24).move_to([0, 2.4, 0])
        self.play(FadeIn(c), FadeIn(pe), run_time=0.35)
        self.frac(0.22)
        self.play(FadeOut(VGroup(a, b, c, pe)), run_time=0.25)
        # bornera de control
        self.zoom_a(v, v.ctrl_bloque, 8.3, [0, 0.6, 0], 0.9)
        bc = v.bc
        def marca(nombres, txt, col, lado):
            grp = VGroup(*[bc[n] for n in nombres])
            br = Brace(grp, UP if lado == "up" else DOWN, color=col, buff=0.1)
            t = tag(txt, col, 22).next_to(br, UP if lado == "up" else DOWN, buff=0.1)
            t.shift(RIGHT * max(0, -4.3 - t.get_left()[0])).shift(LEFT * max(0, t.get_right()[0] - 4.3))
            return VGroup(br, t)
        m1 = marca(["DI1", "DI2", "DI3", "DI4"], "entradas digitales", VD, "up")
        m2 = marca(["AI1", "AI2"], "0–10 V · 4–20 mA", CY, "down")
        m3 = marca(["RA", "RB", "RC"], "relé de falla", RJ, "up")
        m3.shift(UP * 0.0)
        if m3[1].get_bottom()[1] < m1[1].get_top()[1] and abs(m3[1].get_x() - m1[1].get_x()) < (m3[1].width + m1[1].width) / 2:
            m3[1].next_to(m1[1], UP, buff=0.1)
        self.play(FadeIn(m1), run_time=0.3)
        self.frac(0.3)
        self.play(FadeIn(m2), run_time=0.3)
        self.frac(0.45)
        self.play(FadeIn(m3), run_time=0.3)
        self.cerrar_voz(0.05)
        self.limpiar(v, m1, m2, m3)

    # ---------------------------------------------------------------- 2 · bloques, rectificador, precarga y bus
    def s_bloques_rect_pre_bus(self):
        self.voz("bloques")
        self.chip("2", "POR DENTRO: 3 ETAPAS")
        cp = circuito_potencia().scale(0.98).move_to([0.05, 1.2, 0])
        self.play(Create(cp, lag_ratio=0.02), run_time=2.0)
        def zona(grp, col, txt):
            r = Rectangle(width=grp.width + 0.16, height=3.9, stroke_color=col, stroke_width=3).set_fill(col, 0.12)
            r.move_to([grp.get_x(), cp.get_y(), 0])
            t = tag(txt, col, 24).next_to(r, DOWN, buff=0.15)
            return VGroup(r, t)
        z1 = zona(cp.rect, AMB, "RECTIFICADOR")
        z2 = zona(VGroup(cp.pre, cp.bus, cp.ldc), CY, "BUS DC")
        z3 = zona(cp.inv, RJ, "INVERSOR")
        z2[1].shift(DOWN * 0.75)
        for z in (z1, z2, z3):
            self.play(FadeIn(z), run_time=0.35)
        io = VGroup(tag("3F · 60 Hz fijos", "#475467", 24).move_to([-2.4, -2.3, 0]), tag("0–400 Hz variable", VD, 24).move_to([2.3, -2.3, 0]))
        io.shift(DOWN * 0.9)
        self.play(FadeIn(io), run_time=0.3)
        self.cerrar_voz(0.05)
        self.play(FadeOut(VGroup(z1, z2, z3, io)), run_time=0.3)

        # --- rectificador
        self.voz("rect")
        self.chip("3", "ETAPA 1 · RECTIFICADOR", AMB)
        self.zoom(cp, cp.rect.get_center(), 2.0, [0.5, 1.0, 0], 1.0)
        xr = [x for x in cp.rect[0]]
        # trayecto: L1 → diodo superior de la pierna 1 → riel +, regreso por riel − → diodo inferior de la pierna 2 → L2
        p_l1 = cp.rect[7].get_center() if False else None
        leg1, leg2 = cp.rect[0][0], cp.rect[0][1]
        top1 = leg1.get_start(); mid1 = cp.rect[7].get_center(); bot2 = leg2.get_end(); mid2 = cp.rect[8].get_center()
        f1 = self.flujo([mid1 + LEFT * 1.3, mid1, top1, top1 + RIGHT * 2.2], AMB, 2.6, 1.6)
        f2 = self.flujo([bot2 + RIGHT * 2.2, bot2, mid2, mid2 + LEFT * 2.3], CY, 2.6, 1.6)
        ax = ejes(7.4, 2.0, (0, 1, 0.25), (0, 1.15, 0.5)).move_to([0, -3.0, 0])
        th = np.linspace(0, 1, 600)
        def env(t):
            a = [np.sin(TAU * t - k * TAU / 3) for k in range(3)]
            return (max(a) - min(a)) / np.sqrt(3)
        fases = VGroup(*[ax.plot(lambda t, k=k: 0.5 + 0.5 * np.sin(TAU * t - k * TAU / 3) * 0.0 + 0 * t, x_range=[0, 1]) for k in range(0)])
        cur = ax.plot(env, x_range=[0, 1, 0.002], color=AMB, stroke_width=5)
        prom = DashedLine(ax.c2p(0, 0.955), ax.c2p(1, 0.955)).set_stroke(WHITE, 2)
        self.frac(0.15)
        self.play(Create(ax), Create(cur), run_time=1.2)
        lab = VGroup(T("6 pulsos por ciclo · rizado de 360 Hz", 22, AMB, "BOLD").next_to(ax, UP, buff=0.08))
        self.play(FadeIn(lab), Create(prom), run_time=0.4)
        n = VGroup(T("480 V CA", 44, WHITE, "HEAVY"), T("→", 44, WHITE, "HEAVY"), T("≈ 650 V DC", 44, AMB, "HEAVY")).arrange(RIGHT, buff=0.25).move_to([0, -4.8, 0])
        n2 = T("1,35 × 480 = 648 V (más cerca del pico con capacitores)", 20, CLARO, "BOLD").next_to(n, DOWN, buff=0.12)
        self.frac(0.25)
        self.play(FadeIn(n, shift=UP * 0.15), FadeIn(n2), run_time=0.45)
        self.cerrar_voz(0.05)
        self.remove(f1, f2)
        self.play(FadeOut(VGroup(ax, cur, prom, lab, n, n2)), run_time=0.3)

        # --- precarga
        self.voz("precarga")
        self.chip("4", "PRECARGA DEL BUS", AMB)
        pr = cp.pre
        self.zoom(cp, pr.get_center(), 1.35, [0, 1.6, 0], 0.9)
        r_c = pr[0][1].get_center()
        f3 = self.flujo([r_c + LEFT * 2.2, r_c, r_c + RIGHT * 2.2], AMB, 1.6, 1.5)
        t1 = tag("R pre limita la corriente de carga", AMB, 26).move_to([0, -0.9, 0])
        self.play(FadeIn(t1), run_time=0.3)
        # medidor de bus
        barra = Rectangle(width=6.6, height=0.4, stroke_color="#5B6B9A", stroke_width=2).move_to([0, -2.6, 0])
        llen = Rectangle(width=0.01, height=0.38, stroke_width=0).set_fill(CY, 1).align_to(barra, LEFT).set_y(-2.6)
        uv = T("V DC en el bus", 26, CLARO, "BOLD").move_to([0.75, -3.3, 0])
        vb = T("0", 36, CY, "HEAVY").next_to(uv, LEFT, buff=0.15)
        vb.add_updater(lambda m: m.become(T(f"{int(648 * llen.width / 6.58)}", 36, CY, "HEAVY").next_to(uv, LEFT, buff=0.15)))
        self.add(barra, llen, vb, uv)
        self.play(llen.animate.stretch_to_fit_width(6.3, about_edge=LEFT), run_time=self.resta() * 0.45, rate_func=lambda t: 1 - np.exp(-3 * t))
        self.sfx("tic", -6)
        k1 = cp.k1c
        mv = k1.mov
        self.remove(f3)
        a_, b_ = mv.get_start(), k1[2].get_start()
        self.play(mv.animate.put_start_and_end_on(a_, b_), run_time=0.2)
        y_k = a_[1]
        f4 = self.flujo([P(a_[0] - 1.2, y_k), P(b_[0] + 1.2, y_k)], VD, 2.4, 1.5)
        t2 = tag("K1 cierra y puentea la resistencia", VD, 26).move_to([0, -4.4, 0])
        self.play(FadeIn(t2), llen.animate.stretch_to_fit_width(6.58, about_edge=LEFT), run_time=0.4)
        self.cerrar_voz(0.05)
        vb.clear_updaters()
        self.remove(f4)
        self.play(FadeOut(VGroup(t1, t2, barra, llen, vb, uv)), run_time=0.3)

        # --- bus DC
        self.voz("bus")
        self.chip("5", "ETAPA 2 · BUS DC", CY)
        self.play(FadeOut(cp), run_time=0.3)
        self.remove(cp)
        bk = banco_capacitores(1.9).move_to([0, 1.05, 0])
        self.play(FadeIn(bk, shift=UP * 0.2), run_time=0.5)
        ax = ejes(7.2, 1.7, (0, 1, 0.25), (0.8, 1.02, 0.1)).move_to([0.2, -2.55, 0])
        pul = ax.plot(lambda t: abs(np.sin(PI * 6 * t)) * 0.134 + 0.866, x_range=[0, 1, 0.002], color=AMB, stroke_width=3)
        fil = ax.plot(lambda t: 0.975 + 0.006 * np.sin(TAU * 6 * t), x_range=[0, 1, 0.002], color=CY, stroke_width=6)
        lb = VGroup(T("sin capacitores", 22, AMB, "BOLD"), T("con capacitores", 22, CY, "BOLD")).arrange(RIGHT, buff=0.6).next_to(ax, UP, buff=0.1)
        self.play(Create(ax), Create(pul), FadeIn(lb[0]), run_time=0.7)
        self.play(Create(fil), FadeIn(lb[1]), run_time=0.6)
        self.frac(0.3)
        nucleo = VGroup(*[Rectangle(width=2.2, height=0.06, stroke_width=0).set_fill("#8A929C" if k % 2 else "#6B7280", 1).move_to([0, -0.45 + 0.06 * k, 0]) for k in range(16)])
        bob = VGroup(*[VGroup(RoundedRectangle(width=0.7, height=1.25, corner_radius=0.12, stroke_color="#7A3B12", stroke_width=1.5).set_fill(CU, 1),
                              *[Line([-0.33, y, 0], [0.33, y, 0]).set_stroke("#9A5528", 1.2) for y in np.linspace(-0.5, 0.5, 9)]).move_to([x, 0.05, 0]) for x in (-0.55, 0.55)])
        term = VGroup(*[tornillo(np.array([x, 0.85, 0]), 0.07) for x in (-0.55, 0.55)])
        choke = VGroup(nucleo, bob, term).move_to([-2.2, -4.45, 0])
        t_l = card("REACTOR DC", ["menos armónicos hacia la red"], VD, 5.0, 24).move_to([1.35, -4.45, 0])
        self.play(FadeIn(choke, shift=UP * 0.15), FadeIn(t_l, shift=LEFT * 0.15), run_time=0.5)
        self.cerrar_voz(0.05)
        self.limpiar(bk, ax, pul, fil, lb, choke, t_l)
        self.cp = circuito_potencia().scale(0.98).move_to([0.05, 1.2, 0])

    # ---------------------------------------------------------------- seguridad
    def s_seguridad(self):
        self.voz("seguridad")
        self.chip("!", "SEGURIDAD", RJ)
        v = variador(1.35).move_to([0, -1.25, 0])
        self.add(v)
        cbus = VGroup(v.bp["+"], v.bp["−"], v.charge).get_center()
        v.scale(2.4, about_point=cbus).shift(np.array([0, 0.9, 0]) - cbus)
        self.play(FadeIn(v), run_time=0.4)
        led = v.charge_led
        halo = Circle(radius=0.25, stroke_width=0).set_fill("#FF3B30", 0.35).move_to(led)
        self.play(FadeIn(halo), Flash(led, color="#FF3B30", flash_radius=0.35), run_time=0.5)
        mm = multimetro_cat(1.05).move_to([2.95, -3.3, 0])
        self.play(FadeIn(mm, shift=LEFT * 0.3), run_time=0.4)
        pr = punta(mm.jack_v.get_center(), v.bp["+"][2].get_center(), "#E5484D")
        pn = punta(mm.jack_com.get_center(), v.bp["−"][2].get_center(), "#344054")
        self.play(Create(pr), Create(pn), run_time=0.6)
        lst = VGroup(card("1 · TIEMPO DE LA ETIQUETA", [], AMB, 5.2, 24), card("2 · LED CHARGE APAGADO", [], RJ, 5.2, 24),
                     card("3 · MIDE + y − : < 50 V DC", [], VD, 5.2, 24)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([-1.6, -3.4, 0])
        self.play(FadeIn(lst[0], shift=RIGHT * 0.2), run_time=0.35)
        lect = ValueTracker(648)
        dig = mm.dig
        def upd(m):
            nuevo = Tm(f"{int(lect.get_value()):>3d}", 24, "#101828", "BOLD").move_to(m)
            m.become(nuevo)
        dig.add_updater(upd)
        self.play(lect.animate.set_value(260), run_time=self.resta() * 0.35, rate_func=linear)
        self.play(FadeIn(lst[1], shift=RIGHT * 0.2), FadeOut(halo), led.animate.set_fill("#3A3F47"), run_time=0.35)
        self.play(lect.animate.set_value(32), run_time=max(0.5, self.resta() * 0.4), rate_func=linear)
        self.play(FadeIn(lst[2], shift=RIGHT * 0.2), run_time=0.35)
        dig.clear_updaters()
        self.cerrar_voz(0.05)
        self.limpiar(v, mm, pr, pn, lst)

    # ---------------------------------------------------------------- inversor + PWM
    def s_inversor_pwm(self):
        self.voz("inversor")
        self.chip("6", "ETAPA 3 · INVERSOR IGBT", RJ)
        cp = self.cp
        self.add(cp)
        self.play(FadeIn(cp), run_time=0.4)
        cinv = VGroup(cp.inv, cp.motor).get_center()
        self.zoom(cp, cinv, 1.6, [-0.5, 1.0, 0], 1.0)
        (q1, q2), (q3, q4), _ = cp.qs
        self.frac(0.12)
        self.play(q1.animate.set_color(VD), q4.animate.set_color(VD), run_time=0.3)
        xi = [q[0][3][1].get_start()[0] for q in cp.qs]
        yp = cp.inv[0][0].get_start()[1]; yn = cp.inv[0][2].get_end()[1]
        yu = cp.salidas[0].get_start()[1] if hasattr(cp, "salidas") else None
        u = cp.inv[7].get_center(); vv = cp.inv[17].get_center()
        mc = cp.motor[0].get_center()
        ruta = [P(xi[0] - 2.0, yp), P(xi[0], yp), P(xi[0], u[1]), P(mc[0] - 0.5, u[1]), P(mc[0] - 0.5, vv[1]), P(xi[1], vv[1]), P(xi[1], yn), P(xi[1] - 2.9, yn)]
        f = self.flujo(ruta, VD, 2.6, 1.6)
        t1 = tag("Q1 + Q4 conducen: corriente de U a V", VD, 26).move_to([0, -1.9, 0])
        self.play(FadeIn(t1), run_time=0.3)
        self.frac(0.35)
        # prohibido: Q1 y Q2 a la vez
        self.remove(f)
        self.play(q4.animate.set_color(WHITE), q2.animate.set_color(RJ), q1.animate.set_color(RJ), FadeOut(t1), run_time=0.3)
        x = Cross(VGroup(q1, q2), stroke_color=RJ, stroke_width=8, scale_factor=0.9)
        t2 = tag("Q1 + Q2 a la vez = CORTO DEL BUS", RJ, 26).move_to([0, -1.9, 0])
        self.play(Create(x), FadeIn(t2), run_time=0.35)
        # tiempo muerto
        ax = ejes(7.4, 1.9, (0, 1, 0.25), (0, 2.6, 1)).move_to([0, -3.9, 0])
        def g(t, inv=False):
            T_ = 0.25; dt = 0.025
            ph = (t % T_) / T_
            on = 0.0 + dt / T_ < ph < 0.5 if not inv else 0.5 + dt / T_ < ph < 1.0
            return on
        sq1 = ax.plot(lambda t: 1.4 + 1.0 * g(t), x_range=[0, 1, 0.001], color=VD, stroke_width=4, use_smoothing=False)
        sq2 = ax.plot(lambda t: 0.1 + 1.0 * g(t, True), x_range=[0, 1, 0.001], color=AMB, stroke_width=4, use_smoothing=False)
        et = VGroup(T("Q1", 20, VD, "HEAVY").next_to(ax.c2p(0, 1.9), LEFT, buff=0.1), T("Q2", 20, AMB, "HEAVY").next_to(ax.c2p(0, 0.6), LEFT, buff=0.1))
        self.frac(0.2)
        self.play(FadeOut(t2), Create(ax), Create(sq1), Create(sq2), FadeIn(et), run_time=0.8)
        zona = Rectangle(width=ax.c2p(0.025, 0)[0] - ax.c2p(0, 0)[0], height=2.0, stroke_width=0).set_fill(RJ, 0.35).move_to(ax.c2p(0.1375, 1.25))
        tm = tag("tiempo muerto: microsegundos", RJ, 24).next_to(ax, UP, buff=0.1)
        self.play(FadeIn(zona), FadeIn(tm), run_time=0.3)
        self.cerrar_voz(0.05)
        self.play(FadeOut(VGroup(x, ax, sq1, sq2, et, zona, tm)), q1.animate.set_color(WHITE), q2.animate.set_color(WHITE), run_time=0.3)

        self.voz("pwm")
        self.chip("7", "MODULACIÓN PWM", RJ)
        self.play(FadeOut(cp), run_time=0.4)
        self.remove(cp)
        ax = ejes(7.6, 2.4, (0, 1, 0.25), (-1.2, 1.2, 1)).move_to([0, 1.7, 0])
        fc = 18
        tri = ax.plot(lambda t: 2 * abs(2 * ((t * fc) % 1) - 1) - 1, x_range=[0, 1, 0.0005], color="#8892B0", stroke_width=2, use_smoothing=False)
        sen = ax.plot(lambda t: 0.85 * np.sin(TAU * t), x_range=[0, 1, 0.002], color=CY, stroke_width=5)
        l1 = VGroup(T("portadora 2–16 kHz", 20, "#AEB6D8", "BOLD"), T("referencia senoidal", 20, CY, "BOLD")).arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.08)
        self.play(Create(ax), Create(tri), run_time=0.8)
        self.play(Create(sen), FadeIn(l1), run_time=0.6)
        ax2 = ejes(7.6, 2.4, (0, 1, 0.25), (-1.2, 1.2, 1)).move_to([0, -1.9, 0])
        pw = ax2.plot(lambda t: 1.0 if 0.85 * np.sin(TAU * t) > 2 * abs(2 * ((t * fc) % 1) - 1) - 1 else -1.0, x_range=[0, 1, 0.0005], color=AMB, stroke_width=2.6, use_smoothing=False)
        self.frac(0.2)
        self.play(Create(ax2), Create(pw), run_time=1.4)
        corr = ax2.plot(lambda t: 0.8 * np.sin(TAU * t - 0.35), x_range=[0, 1, 0.002], color=VD, stroke_width=6)
        l2 = VGroup(T("voltaje PWM", 20, AMB, "BOLD"), T("corriente en el motor", 20, VD, "BOLD")).arrange(RIGHT, buff=0.5).next_to(ax2, DOWN, buff=0.1)
        self.frac(0.25)
        self.play(Create(corr), FadeIn(l2), run_time=0.9)
        self.cerrar_voz(0.05)
        self.limpiar(ax, tri, sen, l1, ax2, pw, corr, l2)

    # ---------------------------------------------------------------- V/Hz
    def s_vhz(self):
        self.voz("vhz")
        self.chip("8", "CONTROL V/Hz", VD)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 500, 100], x_length=6.6, y_length=3.6, tips=False,
                  axis_config={"color": "#5B6B9A", "stroke_width": 2, "include_ticks": True, "font_size": 20},
                  x_axis_config={"numbers_to_include": [0, 30, 60]}, y_axis_config={"numbers_to_include": [0, 230, 460]}).move_to([0.35, 1.4, 0])
        xl = T("f (Hz)", 20, CLARO, "BOLD").next_to(ax.x_axis, DOWN, buff=0.35).align_to(ax.x_axis, RIGHT)
        yl = T("V", 22, CLARO, "BOLD").next_to(ax.y_axis, UP, buff=0.1)
        lin = ax.plot(lambda f: 460 * f / 60, x_range=[0, 60], color=VD, stroke_width=6)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.6)
        sat = tag("solo bajar f = saturación", RJ, 24).move_to([0, 3.2, 0])
        self.play(FadeIn(sat), run_time=0.3)
        self.frac(0.15)
        self.play(Create(lin), FadeOut(sat), run_time=0.8)
        k = card("460 V ÷ 60 Hz = 7,67 V/Hz", [], VD, 6.0, 28).move_to([0, -1.55, 0])
        self.play(FadeIn(k, shift=UP * 0.15), run_time=0.35)
        self.frac(0.2)
        p60 = Dot(ax.c2p(60, 460), radius=0.1, color=WHITE)
        p30 = Dot(ax.c2p(30, 230), radius=0.12, color=AMB)
        gl = VGroup(DashedLine(ax.c2p(30, 0), ax.c2p(30, 230)), DashedLine(ax.c2p(0, 230), ax.c2p(30, 230))).set_stroke(AMB, 3)
        self.play(FadeIn(p60), FadeIn(p30), Create(gl), run_time=0.5)
        mot = motor_tefc(0.62).move_to([-1.9, -3.75, 0])
        kp = VGroup(RoundedRectangle(width=2.5, height=1.0, corner_radius=0.08, stroke_color="#5F6876", stroke_width=1.4).set_fill("#1B1F27", 1),
                    RoundedRectangle(width=2.2, height=0.7, corner_radius=0.04, stroke_width=0).set_fill("#06110B", 1)).move_to([2.3, -3.75, 0])
        hz = ValueTracker(60)
        dsp = always_redraw(lambda: Tm(f"{hz.get_value():05.2f}", 36, "#39FF88", "BOLD").move_to(kp[1]))
        rpm = always_redraw(lambda: T(f"n_s = {int(round(30 * hz.get_value()))} rpm", 30, WHITE, "HEAVY").move_to([0, -5.05, 0]))
        self.play(FadeIn(mot), FadeIn(kp), FadeIn(dsp), FadeIn(rpm), run_time=0.4)
        girar_eje(mot, 3.0)
        mot.chaveta.rps = 3.0
        self.play(hz.animate.set_value(30), run_time=max(1.0, self.resta() * 0.6), rate_func=smooth,
                  )
        mot.chaveta.rps = 1.5
        self.cerrar_voz(0.05)
        mot.chaveta.clear_updaters()
        dsp.clear_updaters(); rpm.clear_updaters()
        self.limpiar(ax, xl, yl, lin, k, p60, p30, gl, mot, kp, dsp, rpm)

    # ---------------------------------------------------------------- rampa
    def s_rampa(self):
        self.voz("rampa")
        self.chip("9", "ARRANQUE EN RAMPA", AMB)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 8, 2], x_length=7.0, y_length=4.2, tips=False,
                  axis_config={"color": "#5B6B9A", "stroke_width": 2, "include_ticks": True, "font_size": 20},
                  y_axis_config={"numbers_to_include": [2, 4, 6, 8]}).move_to([0.3, 1.1, 0])
        yl = T("I / In", 22, CLARO, "BOLD").next_to(ax.y_axis, UP, buff=0.1)
        xl = T("t (s)", 20, CLARO, "BOLD").next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        dol = ax.plot(lambda t: 1 + 6.0 * np.exp(-((t - 0.25) / 1.0) ** 2) if t > 0.03 else 0, x_range=[0, 10, 0.01], color=RJ, stroke_width=6)
        vfd = ax.plot(lambda t: min(1.5, 0.15 + t * 0.5) if t < 6 else 1.5 - (t - 6) * 0.125 if t < 10 else 1.0, x_range=[0, 10, 0.01], color=VD, stroke_width=6)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), run_time=0.5)
        self.play(Create(dol), run_time=0.9)
        t1 = tag("arranque directo: 6 a 8 × In", RJ, 26).move_to([0, -1.75, 0])
        self.play(FadeIn(t1), run_time=0.3)
        self.frac(0.25)
        self.play(Create(vfd), run_time=1.2)
        t2 = tag("con variador: ≤ 150 % · 60 s (servicio pesado)", VD, 26).move_to([0, -2.85, 0])
        self.play(FadeIn(t2), run_time=0.3)
        r = card("RAMPA 0 → 60 Hz", ["aceleración y desaceleración por parámetro"], AMB, 7.8, 26).move_to([0, -4.45, 0])
        self.frac(0.3)
        self.play(FadeIn(r, shift=UP * 0.15), run_time=0.35)
        self.cerrar_voz(0.05)
        self.limpiar(ax, yl, xl, dol, vfd, t1, t2, r)

    # ---------------------------------------------------------------- frenado
    def s_frenado(self):
        self.voz("frenado")
        self.chip("10", "FRENADO DINÁMICO", AMB)
        cp = circuito_potencia().scale(0.98).move_to([0.05, 1.2, 0])
        self.add(cp)
        cchop = cp.chop.get_center()
        cp.scale(2.0, about_point=cchop).shift(np.array([-0.4, 1.6, 0]) - cchop)
        self.play(FadeIn(cp), run_time=0.4)
        barra = Rectangle(width=6.6, height=0.4, stroke_color="#5B6B9A", stroke_width=2).move_to([0, -1.3, 0])
        llen = Rectangle(width=4.6, height=0.38, stroke_width=0).set_fill(CY, 1).align_to(barra, LEFT).set_y(-1.3)
        um = DashedLine(barra.get_left() + RIGHT * 5.6 + UP * 0.35, barra.get_left() + RIGHT * 5.6 + DOWN * 0.35).set_stroke(RJ, 4)
        tum = T("umbral de frenado", 20, RJ, "BOLD").next_to(um, UP, buff=0.05)
        tb = T("voltaje del bus", 22, CLARO, "BOLD").next_to(barra, DOWN, buff=0.1)
        self.play(FadeIn(barra), FadeIn(llen), Create(um), FadeIn(tum), FadeIn(tb), run_time=0.4)
        reg = tag("el motor regenera", AMB, 26).move_to([0, -0.4, 0])
        self.play(FadeIn(reg), llen.animate.stretch_to_fit_width(5.75, about_edge=LEFT).set_fill(RJ), run_time=1.2)
        self.frac(0.25)
        q7 = cp.chop[2]
        self.play(q7.animate.set_color(VD), run_time=0.25)
        rr = cp.chop[0]
        p_top = rr[0].get_start(); p_bot = cp.chop[3].get_end()
        f = self.flujo([p_top + LEFT * 1.6, p_top, P(p_top[0], p_bot[1]), p_bot + LEFT * 1.6], AMB, 2.6, 1.6)
        rf = resistencia_frenado(1.3).move_to([0.3, -3.3, 0])
        self.play(FadeIn(rf, shift=UP * 0.2), llen.animate.stretch_to_fit_width(4.8, about_edge=LEFT).set_fill(CY), run_time=0.7)
        self.play(rf.brillo.animate.set_fill(opacity=0.45), run_time=0.8)
        sin = tag("sin chopper: falla OV (sobretensión)", RJ, 24).move_to([0, -4.75, 0])
        self.play(FadeIn(sin), run_time=0.3)
        self.cerrar_voz(0.05)
        self.remove(f)
        self.limpiar(cp, barra, llen, um, tum, tb, reg, rf, sin)

    # ---------------------------------------------------------------- reglas de campo
    def s_campo(self):
        self.voz("campo")
        self.chip("11", "EN CAMPO: 4 REGLAS", MARCA)
        lista = VGroup(card("1 · 125 % DE LA I DE ENTRADA", ["NEC 430.122(A)"], AMB, 7.8, 22),
                       card("2 · CABLE APANTALLADO PARA VFD", ["malla a tierra en ambos extremos"], CY, 7.8, 22),
                       card("3 · MOTOR PARA INVERSOR", ["NEMA MG 1 Parte 31 · picos de 1600 V"], VD, 7.8, 22),
                       card("4 · SELECCIÓN POR CORRIENTE", ["corriente de salida, no solo hp"], RJ, 7.8, 22)).arrange(DOWN, buff=0.14).move_to([0, -3.35, 0]).set_z_index(5)
        fondo_l = Rectangle(width=9.2, height=lista.height + 0.5, stroke_width=0).set_fill("#0E1440", 0.97).move_to(lista).set_z_index(4)
        borde_l = Line(fondo_l.get_corner(UL), fondo_l.get_corner(UR)).set_stroke(MARCA, 3).set_z_index(4)
        self.play(FadeIn(fondo_l), FadeIn(borde_l), run_time=0.25)
        # 1: conductores
        ilu1 = VGroup(*[VGroup(RoundedRectangle(width=6.0, height=0.34, corner_radius=0.17, stroke_width=0).set_fill(c, 1),
                               RoundedRectangle(width=0.6, height=0.22, corner_radius=0.05, stroke_width=0).set_fill(CU, 1).shift(RIGHT * 3.25))
                        for c in ("#101828", "#B42318", "#1D4ED8")]).arrange(DOWN, buff=0.18).move_to([0, 1.45, 0])
        f1 = T("I alim ≥ 1,25 × I entrada nominal", 30, AMB, "HEAVY").next_to(ilu1, DOWN, buff=0.3)
        ej = T("ej.: 14,5 A × 1,25 = 18,1 A", 26, CLARO, "BOLD").next_to(f1, DOWN, buff=0.12)
        self.play(FadeIn(ilu1), FadeIn(lista[0], shift=RIGHT * 0.2), run_time=0.45)
        self.play(FadeIn(f1), FadeIn(ej), run_time=0.35)
        self.frac(0.22)
        # 2: cable
        cab = cable_vfd(1.45).move_to([-1.6, 1.4, 0])
        nt = VGroup(T("3 fases", 22, WHITE, "BOLD"), T("3 tierras simétricas", 22, "#E0A86E", "BOLD"), T("malla + lámina", 22, "#E0A86E", "BOLD"),
                    T("prensaestopas EMC 360°", 22, CY, "HEAVY")).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([2.1, 1.4, 0])
        self.play(FadeOut(VGroup(ilu1, f1, ej)), FadeIn(cab), FadeIn(nt), FadeIn(lista[1], shift=RIGHT * 0.2), run_time=0.45)
        self.frac(0.3)
        # 3: placa del motor
        mot = motor_tefc(1.15).move_to([0, 1.3, 0])
        self.play(FadeOut(VGroup(cab, nt)), FadeIn(mot), FadeIn(lista[2], shift=RIGHT * 0.2), run_time=0.45)
        self.zoom_a(mot, mot.placa_d, 6.6, [0, 1.4, 0], 0.8)
        sub = SurroundingRectangle(mot.placa_d[2][3], color=VD, buff=0.04, stroke_width=4)
        self.play(Create(sub), run_time=0.35)
        self.frac(0.35)
        # 4: placa del variador
        v = variador(0.8).move_to([0, 1.2, 0])
        self.play(FadeOut(VGroup(mot, sub)), FadeIn(v), FadeIn(lista[3], shift=RIGHT * 0.2), run_time=0.45)
        self.zoom_a(v, v.placa, 7.0, [0, 1.6, 0], 0.8)
        sal = SurroundingRectangle(v.placa[1][2], color=RJ, buff=0.04, stroke_width=4)
        self.play(Create(sal), run_time=0.35)
        self.cerrar_voz(0.05)
        self.limpiar(v, sal, lista, fondo_l, borde_l)

    # ---------------------------------------------------------------- dato
    def s_dato(self):
        self.voz("dato")
        self.chip("★", "EL DATO QUE VENDE VARIADORES", AMB)
        mot = motor_tefc(0.55).move_to([-1.65, 2.35, 0])
        ac = acople(0.42).move_to(mot.eje.get_right() + RIGHT * 0.18)
        bo = bomba(0.6)
        bo.next_to(ac, RIGHT, buff=0.0).align_to(mot, DOWN).shift(UP * 0.05)
        sk = base_skid(mot.get_left()[0] - 0.1, bo.get_right()[0] + 0.1, mot.get_bottom()[1] - 0.1, 0.8)
        grp = VGroup(sk, mot, ac, bo)
        if grp.width > 8.3:
            grp.scale_to_fit_width(8.3)
        grp.move_to([0, 2.3, 0])
        self.play(FadeIn(grp), run_time=0.45)
        girar_eje(mot, 2.0)
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2], x_length=5.6, y_length=3.0, tips=False,
                  axis_config={"color": "#5B6B9A", "stroke_width": 2, "include_ticks": False}).move_to([0.2, -1.35, 0])
        c = ax.plot(lambda n: n ** 3, x_range=[0, 1, 0.01], color=AMB, stroke_width=6)
        yl = T("P", 24, CLARO, "BOLD").next_to(ax.y_axis, UP, buff=0.08)
        xl = T("velocidad", 20, CLARO, "BOLD").next_to(ax.x_axis, DOWN, buff=0.1).align_to(ax.x_axis, RIGHT)
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(c), run_time=0.9)
        d = Dot(ax.c2p(0.8, 0.512), radius=0.12, color=VD)
        gl = VGroup(DashedLine(ax.c2p(0.8, 0), ax.c2p(0.8, 0.512)), DashedLine(ax.c2p(0, 0.512), ax.c2p(0.8, 0.512))).set_stroke(VD, 3)
        self.frac(0.25)
        self.play(FadeIn(d), Create(gl), run_time=0.4)
        r = VGroup(T("0,8³ = 0,51", 46, WHITE, "HEAVY"), T("80 % velocidad → ≈ 51 % potencia", 28, VD, "HEAVY")).arrange(DOWN, buff=0.12).move_to([0, -4.0, 0])
        self.play(FadeIn(r, shift=UP * 0.15), run_time=0.4)
        self.cerrar_voz(0.05)
        mot.chaveta.clear_updaters()
        self.limpiar(grp, ax, c, yl, xl, d, gl, r)
        if self.chip_act is not None:
            self.play(FadeOut(self.chip_act), run_time=0.25)
            self.chip_act = None


class PortadaV31b(Scene):
    def construct(self):
        from miniaturas import texto_gancho, sticker, logo_esq
        W, H = config.frame_width, config.frame_height
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(color=["#070A1F", "#141B4A"], opacity=1).set_sheen_direction(UR))
        glow = VGroup(*[Circle(radius=0.6 + 0.35 * k, stroke_width=0).set_fill("#38E8FF", 0.05) for k in range(9)]).move_to([0.3, -0.6, 0])
        t = texto_gancho([("ASÍ FUNCIONA", "#FFFFFF"), ("EL VARIADOR", "#38E8FF"), ("DE FRECUENCIA", "#FDB022")], 96)
        t.scale_to_fit_width(min(8.4, t.width)).move_to([0, 5.2, 0])
        v = variador(1.2, "30.00").move_to([-0.9, -0.9, 0])
        m = motor_tefc(0.62).move_to([2.6, -3.6, 0])
        st = sticker("RECTIFICA · FILTRA · INVIERTE", "#E5484D", size=40, ang=-0.03).move_to([0, -6.0, 0])
        self.add(glow, v, m, t, st)
        logo_esq(self, (3.6, 7.2))

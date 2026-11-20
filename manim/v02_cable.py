"""
V02 · ¿CABLE o ALAMBRE? (vertical 1080x1920, estilo azul marino)
Fuentes (verificadas en el PDF del NEC 2020 del usuario):
 - NEC 2020, Cap. 9, Tabla 8 (Conductor Properties), cobre 12 AWG: área 3.31 mm² (sólido y de 7 hilos);
   sólido: 1 hilo, diámetro 2.05 mm, 6.34 Ω/km (sin recubrimiento, 75 °C);
   trenzado: 7 hilos de 0.78 mm, diámetro total 2.32 mm, 6.50 Ω/km.
 - NEC 2020 310.3(C): "Where installed in raceways, conductors 8 AWG and larger shall be stranded,
   unless specifically permitted or required elsewhere in this Code to be solid."
 - Jerga: alambre = conductor sólido de un hilo; cable = conductor de varios hilos (así lo usan los fabricantes
   en sus catálogos: "alambre THW" / "cable THW").
"""
from comun_e import *

GUION = {
    "gancho": "¿Cable o alambre? Parecen lo mismo, pero no lo son. Y saber la diferencia te ahorra problemas en "
              "una instalación.",
    "p1": "El alambre es un solo hilo de cobre, sólido, como una varilla delgada. El cable, en cambio, está hecho "
          "de varios hilos más delgados, trenzados entre sí.",
    "p2": "En las instalaciones de casa, el más común es el cable de siete hilos: uno al centro, y seis alrededor.",
    "p3": "Y aquí viene un dato que pocos saben: un alambre calibre doce, y un cable calibre doce de siete hilos, "
          "tienen la misma área de cobre: tres punto treinta y uno milímetros cuadrados. Así lo indica la tabla "
          "ocho del Nec dos mil veinte.",
    "p4": "Entonces, ¿cuál es la diferencia? La flexibilidad. Al doblar el alambre, todo el esfuerzo cae en una "
          "sola pieza. En el cable, el esfuerzo se reparte entre los hilos delgados. Por eso se dobla más fácil, "
          "aguanta mejor las vibraciones, y se jala más fácil por la tubería.",
    "p5": "El cable es un poquito más grueso, por los espacios entre hilos, y su resistencia es apenas mayor: seis "
          "punto cinco ohmios por kilómetro, contra seis punto tres cuatro del alambre. En la práctica, conducen "
          "casi igual.",
    "p6": "Y en calibres grandes no hay discusión: según el Nec, dentro de tubería, del calibre ocho en adelante, "
          "los conductores deben ser de cable.",
    "p7": "Un consejo al conectar cable: tuerce bien los hilos antes de ponerlo en el tornillo. Un hilo suelto "
          "puede tocar otro terminal y provocar un corto.",
    "cierre": "Cable: varios hilos, y flexible. Alambre: un solo hilo, y rígido. Si te sirvió, suscríbete y "
              "sígueme.",
}

if __name__ == "__main__":
    assert abs(7 * 3.14159 * (0.78 / 2) ** 2 - 3.31) < 0.05   # 7 hilos de 0.78 mm ≈ 3.34 mm² (tabla: 3.31)
    tot = 0
    for k, t in GUION.items():
        w, d = audio(DIR / f"voz_v02_{SUFIJO_VOZ}", k, t)
        tot += d
        print(k, round(d, 1))
    print("total", round(tot, 1), "s ·", sum(len(t) for t in GUION.values()), "caracteres")


# ====================================================================== animación
from taller import corriente, cable_hilos, Polilinea, P
from comun_e import _osc

COBRE_CL = "#E6A16A"


def alambre(largo=5.0, w=0.5, pelado=1.0, color=FASE):
    """Conductor sólido: aislamiento + una sola varilla de cobre con brillo."""
    ais = RoundedRectangle(width=largo, height=w, corner_radius=w / 2, stroke_color="#8F9AC8", stroke_width=2).set_fill(color, 1)
    ais.move_to(LEFT * pelado / 2)
    x0 = ais.get_right()[0] - 0.05
    nucleo = RoundedRectangle(width=pelado + 0.05, height=w * 0.46, corner_radius=w * 0.2, stroke_color=_osc(COBRE, 0.35),
                              stroke_width=1.5).set_fill(COBRE, 1).move_to([x0 + pelado / 2, 0, 0])
    brillo = Line(nucleo.get_left() + RIGHT * 0.05 + UP * w * 0.09, nucleo.get_right() + LEFT * 0.08 + UP * w * 0.09,
                  stroke_color=COBRE_CL, stroke_width=3)
    b2 = Line(ais.get_left() + RIGHT * 0.2 + UP * w * 0.22, ais.get_right() + LEFT * 0.2 + UP * w * 0.22, stroke_color=WHITE,
              stroke_width=2, stroke_opacity=0.3)
    return VGroup(nucleo, brillo, ais, b2)


def cable7(largo=5.0, w=0.5, pelado=1.0, abierto=False, color=FASE):
    g = cable_hilos(largo, color, w, pelado, abierto)
    g[2].set_stroke("#8F9AC8", 2)
    return g


def corte(solido=True, r=1.15, color=FASE):
    """Corte transversal: aislamiento + cobre (1 círculo o 7 hilos)."""
    ais = Circle(radius=r, stroke_color="#8F9AC8", stroke_width=3).set_fill(color, 1)
    if solido:
        cu = VGroup(Circle(radius=r * 0.62, stroke_color=_osc(COBRE, 0.35), stroke_width=2).set_fill(COBRE, 1),
                    Arc(radius=r * 0.45, start_angle=PI * 0.6, angle=PI * 0.35).set_stroke(COBRE_CL, 4))
    else:
        rh = r * 0.62 / 3
        cu = VGroup(*[Circle(radius=rh, stroke_color=_osc(COBRE, 0.35), stroke_width=2).set_fill(COBRE, 1)
                      .move_to(2 * rh * np.array([np.cos(a), np.sin(a), 0]) if k else ORIGIN)
                      for k, a in enumerate([0] + list(np.linspace(0, TAU, 6, endpoint=False)))])
    return VGroup(ais, cu)


def tornillo_con(c, bien=True):
    """Tornillo de latón con cable de 7 hilos: torcido y en gancho (bien) o con un hilo suelto (mal)."""
    from comun_e import tornillo
    placa = RoundedRectangle(width=1.3, height=1.3, corner_radius=0.12, stroke_color=_osc(LATON, 0.4), stroke_width=2).set_fill(LATON, 1)
    t = tornillo(0.42, LATON, 0.4)
    ais = VMobject().set_points_smoothly([P(-3.2, -1.6), P(-2.0, -1.2), P(-1.0, -0.75), P(-0.62, -0.5)])
    cab = VGroup(ais.copy().set_stroke("#8F9AC8", 26), ais.copy().set_stroke(FASE, 22))
    gancho = VMobject().set_points_smoothly([P(-0.62, -0.5), P(-0.15, -0.6), P(0.45, -0.3), P(0.55, 0.25), P(0.1, 0.58), P(-0.42, 0.38)])
    g = VGroup(gancho.copy().set_stroke(_osc(COBRE, 0.4), 15), gancho.copy().set_stroke(COBRE, 11),
               *[Line(gancho.point_from_proportion(p_) + P(-0.06, -0.06), gancho.point_from_proportion(p_) + P(0.06, 0.06),
                      stroke_color=_osc(COBRE, 0.45), stroke_width=2) for p_ in np.linspace(0.05, 0.95, 12)])
    out = VGroup(placa, cab, g, t)
    if not bien:
        suelto = VMobject().set_points_smoothly([P(-0.5, -0.45), P(-0.2, -1.0), P(0.5, -1.25), P(1.1, -1.2)]).set_stroke(COBRE, 4)
        out.add(suelto)
        out.suelto = suelto
    return out.move_to(c)


class Cable(Escena):
    CARPETA_VOZ = "voz_v02"
    GUION = GUION

    def limpiar(self, *ms, t=0.35):
        ms = [m for m in ms if m is not None]
        for m in ms:
            for s in m.get_family():
                s.clear_updaters()
        if ms:
            self.play(*[FadeOut(m) for m in ms], run_time=t)

    def construct(self):
        self.add(encabezado("¿CABLE o", "ALAMBRE?"))

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        a = alambre(6.4, 0.9, 1.5).move_to([0, 2.6, 0])
        c = cable7(6.4, 0.9, 1.5).move_to([0, -0.6, 0])
        la = T("ALAMBRE", 54, TINTA, "HEAVY").next_to(a, UP, buff=0.3).align_to(a, LEFT)
        lc = T("CABLE", 54, MARCA, "HEAVY").next_to(c, UP, buff=0.3).align_to(c, LEFT)
        self.play(FadeIn(a, shift=RIGHT * 0.5), FadeIn(la), run_time=0.6)
        self.play(FadeIn(c, shift=RIGHT * 0.5), FadeIn(lc), run_time=0.6)
        q = VGroup(T("parecen lo mismo...", 46, TINTA2, "BOLD"), T("pero NO lo son", 62, ROJO, "HEAVY")).arrange(DOWN, buff=0.15)
        q.move_to([0, -3.2, 0])
        self.wait(max(0.1, self.resta() * 0.2))
        self.play(FadeIn(q[0]), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.25))
        self.sfx("pop", -8)
        self.play(FadeIn(q[1], scale=1.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(q)

        # ------------------------------------------------------------ p1: un hilo vs varios
        self.voz("p1")
        e1 = pastilla("1 solo hilo sólido", TINTA, 36, True).next_to(a, DOWN, buff=0.35)
        self.play(Indicate(a[0], color=COBRE_CL, scale_factor=1.15), FadeIn(e1), run_time=0.8)
        self.wait(max(0.1, self.resta() * 0.45))
        c2 = cable7(6.4, 0.9, 1.5, abierto=True).move_to(c)
        e2 = pastilla("varios hilos trenzados", MARCA, 36, True).next_to(c, DOWN, buff=0.45)
        self.play(Transform(c, c2), FadeIn(e2), run_time=0.8)
        self.cerrar_voz(0.1)
        self.limpiar(a, c, la, lc, e1, e2)

        # ------------------------------------------------------------ p2: 7 hilos
        self.voz("p2")
        s7 = corte(False, 2.0).move_to([0, 1.2, 0])
        self.play(FadeIn(s7[0]), run_time=0.4)
        centro, aro = s7[1][0], VGroup(*s7[1][1:])
        self.play(GrowFromCenter(centro), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(h) for h in aro], lag_ratio=0.15), run_time=1.2)
        n1 = T("1 al centro", 40, COBRE_CL, "HEAVY").move_to([-1.7, -1.5, 0])
        n2 = T("+ 6 alrededor", 40, COBRE_CL, "HEAVY").move_to([1.6, -1.5, 0])
        tot = pastilla("cable de 7 hilos", MARCA, 40, True).move_to([0, -2.7, 0])
        self.play(FadeIn(n1), Indicate(centro, color=WHITE), run_time=0.5)
        self.play(FadeIn(n2), *[Indicate(h, color=WHITE) for h in aro], run_time=0.6)
        self.play(FadeIn(tot, scale=1.1), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(n1, n2, tot)

        # ------------------------------------------------------------ p3: misma área
        self.voz("p3")
        s1 = corte(True, 1.5).move_to([-2.0, 2.4, 0])
        self.play(s7.animate.scale(0.75).move_to([2.0, 2.4, 0]), FadeIn(s1), run_time=0.7)
        t1 = T("alambre 12", 36, TINTA, "HEAVY").next_to(s1, DOWN, buff=0.25)
        t2 = T("cable 12 · 7 hilos", 36, MARCA, "HEAVY").next_to(s7, DOWN, buff=0.25)
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.25))
        igual = T("=", 120, VERDE_OK, "HEAVY").move_to([0, 2.4, 0])
        area = VGroup(T("3.31 mm²", 96, COBRE_CL, "HEAVY"), T("de cobre en los dos", 38, TINTA, "BOLD")).arrange(DOWN, buff=0.15).move_to([0, -0.9, 0])
        self.sfx("ding", -10)
        self.play(FadeIn(igual, scale=1.4), FadeIn(area, shift=UP * 0.2), run_time=0.6)
        self.wait(max(0.1, self.resta() * 0.3))
        nec = self.carta("NEC 2020 · Cap. 9, Tabla 8", "Cobre 12 AWG: 3.31 mm²,\nsólido o de 7 hilos.", [0, -3.3, 0])
        self.play(FadeIn(nec, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(s1, s7, t1, t2, igual, area, nec)

        # ------------------------------------------------------------ p4: flexibilidad
        self.voz("p4")
        tit = T("la diferencia:", 40, TINTA2, "BOLD").move_to([0, 4.0, 0])
        tit2 = T("FLEXIBILIDAD", 72, MARCA, "HEAVY").next_to(tit, DOWN, buff=0.12)
        self.play(FadeIn(tit), FadeIn(tit2, scale=1.1), run_time=0.5)
        # alambre: se dobla en un quiebre, con esfuerzo concentrado
        recta_a = VMobject().set_points_as_corners([P(-3.6, 1.6), P(-0.4, 1.6)])
        dob_a = VMobject().set_points_as_corners([P(-3.6, 1.6), P(-2.0, 1.6), P(-0.9, 0.5)])
        wa = VGroup(recta_a.copy().set_stroke("#8F9AC8", 62), recta_a.copy().set_stroke(FASE, 54))
        wa_d = VGroup(dob_a.copy().set_stroke("#8F9AC8", 62), dob_a.copy().set_stroke(FASE, 54))
        for m in (*wa, *wa_d):
            m.set_joint_type(LineJointType.MITER)
        # cable: curva suave
        recta_c = VMobject().set_points_smoothly([P(0.4, 1.6), P(1.5, 1.6), P(2.6, 1.6), P(3.6, 1.6)])
        dob_c = VMobject().set_points_smoothly([P(0.4, 1.6), P(1.7, 1.55), P(2.7, 1.0), P(3.1, 0.2)])
        wc = VGroup(recta_c.copy().set_stroke("#8F9AC8", 62), recta_c.copy().set_stroke(FASE, 54))
        wc_d = VGroup(dob_c.copy().set_stroke("#8F9AC8", 62), dob_c.copy().set_stroke(FASE, 54))
        for m in (*wc, *wc_d):
            m.set_cap_style(CapStyleType.ROUND)
        la = T("alambre", 36, TINTA, "HEAVY").move_to([-2.0, 2.4, 0])
        lc = T("cable", 36, MARCA, "HEAVY").move_to([2.0, 2.4, 0])
        self.play(Create(wa), Create(wc), FadeIn(la), FadeIn(lc), run_time=0.6)
        self.wait(max(0.1, self.resta() * 0.12))
        self.play(Transform(wa, wa_d), run_time=0.8)
        esf = VGroup(resplandor(P(-2.0, 1.6), 0.7, ROJO, 8, 0.07), T("todo el esfuerzo\naquí", 30, ROJO, "HEAVY").move_to([-2.2, -0.2, 0]))
        self.play(FadeIn(esf), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.2))
        self.play(Transform(wc, wc_d), run_time=0.9)
        rep = T("se reparte\nentre hilos", 30, VERDE_OK, "HEAVY").move_to([2.0, -0.4, 0])
        self.play(FadeIn(rep), run_time=0.4)
        ventajas = VGroup(*[pastilla(t_, VERDE_OK, 32, True) for t_ in ("✓ se dobla fácil", "✓ aguanta vibraciones", "✓ se jala fácil por el tubo")])
        ventajas.arrange(DOWN, buff=0.22).move_to([0, -2.9, 0])
        for v in ventajas:
            self.wait(max(0.05, self.resta() * 0.12))
            self.play(FadeIn(v, shift=UP * 0.15), run_time=0.35)
        self.cerrar_voz(0.1)
        self.limpiar(tit, tit2, wa, wc, la, lc, esf, rep, ventajas)

        # ------------------------------------------------------------ p5: diámetro y resistencia
        self.voz("p5")
        a = alambre(6.6, 0.75, 1.3).move_to([0, 3.3, 0])
        c = cable7(6.6, 0.85, 1.3).move_to([0, 1.4, 0])
        self.play(FadeIn(a), FadeIn(c), run_time=0.5)
        fa = corriente([a[2].get_left() + RIGHT * 0.2, a[0].get_right()], vel=0.9, escala=2.4)
        fc = corriente([c[2].get_left() + RIGHT * 0.2, c[2].get_right() + RIGHT * 1.2], vel=0.9, escala=2.4)
        self.add(fa, fc)
        filas = VGroup(
            VGroup(T("", 30), T("alambre", 32, TINTA, "HEAVY"), T("cable", 32, MARCA, "HEAVY")),
            VGroup(T("diámetro", 30, TINTA2, "BOLD"), T("2.05 mm", 34, TINTA, "HEAVY"), T("2.32 mm", 34, TINTA, "HEAVY")),
            VGroup(T("resistencia", 30, TINTA2, "BOLD"), T("6.34 Ω/km", 34, TINTA, "HEAVY"), T("6.50 Ω/km", 34, TINTA, "HEAVY")))
        for f in filas:
            for k, m in enumerate(f):
                m.move_to([[-2.6, 0.0, 2.6][k], 0, 0])
        filas.arrange(DOWN, buff=0.45).move_to([0, -1.4, 0])
        caja = tarjeta(8.2, filas.height + 0.7).move_to(filas)
        self.play(FadeIn(caja), FadeIn(filas[0]), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.12))
        self.play(FadeIn(filas[1], shift=UP * 0.1), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.25))
        self.play(FadeIn(filas[2], shift=UP * 0.1), run_time=0.4)
        casi = pastilla("conducen casi igual", VERDE_OK, 40, True).move_to([0, -3.7, 0])
        self.wait(max(0.1, self.resta() * 0.5))
        self.play(FadeIn(casi, scale=1.15), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(a, c, fa, fc, caja, filas, casi)

        # ------------------------------------------------------------ p6: NEC 310.3(C)
        self.voz("p6")
        tubo_ = VGroup(Rectangle(width=7.4, height=1.5, stroke_color=METAL_OSC, stroke_width=3).set_fill(METAL, 0.18),
                       Line(P(-3.7, 0.55), P(3.7, 0.55), stroke_color=WHITE, stroke_width=3, stroke_opacity=0.4)).move_to([0, 2.2, 0])
        gruesos = VGroup(*[cable7(7.0, 0.38, 0.0).move_to([0.2, 2.2 + dy, 0]) for dy in (0.42, 0.0, -0.42)])
        for g_, col in zip(gruesos, (FASE, NEUTRO, TIERRA)):
            g_[2].set_fill(col)
        self.play(FadeIn(tubo_), LaggedStart(*[FadeIn(g_, shift=RIGHT * 1.5) for g_ in gruesos], lag_ratio=0.3), run_time=1.2)
        g8 = pastilla("calibre 8 y mayores", ENERGIA, 40, True).move_to([0, 0.3, 0])
        self.play(FadeIn(g8, scale=1.1), run_time=0.4)
        nec = self.carta("NEC 2020 · 310.3(C)", "En tubería, los conductores 8 AWG\ny mayores deben ser trenzados (cable).", [0, -1.6, 0])
        self.wait(max(0.1, self.resta() * 0.3))
        self.play(FadeIn(nec, shift=UP * 0.2), run_time=0.4)
        self.cerrar_voz(0.1)
        self.limpiar(tubo_, gruesos, g8, nec)

        # ------------------------------------------------------------ p7: consejo al conectar
        self.voz("p7")
        bien = tornillo_con([0.6, 2.7, 0], True).scale(1.15)
        tb = pastilla("✓ hilos torcidos, gancho horario", VERDE_OK, 32, True).next_to(bien, DOWN, buff=0.35)
        self.play(FadeIn(bien), run_time=0.5)
        self.play(FadeIn(tb), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.35))
        mal = tornillo_con([0.6, -1.4, 0], False).scale(1.15)
        vecino = VGroup(RoundedRectangle(width=1.0, height=1.0, corner_radius=0.1, stroke_color=METAL_OSC, stroke_width=2).set_fill("#D9DDE3", 1),
                        Circle(radius=0.3, stroke_color=METAL_OSC, stroke_width=2).set_fill("#E4E7EC", 1)).move_to(mal.get_center() + P(2.6, -1.0))
        self.play(FadeIn(mal), FadeIn(vecino), run_time=0.5)
        chispa = VGroup(*[Line(ORIGIN, 0.35 * np.array([np.cos(t_), np.sin(t_), 0])).set_stroke(AMBAR, 5) for t_ in np.linspace(0, TAU, 8, endpoint=False)])
        chispa.move_to(mal.suelto.get_end())
        tm = pastilla("✗ un hilo suelto = corto", ROJO, 32, True).move_to([0.2, -4.1, 0])
        self.sfx("pop", -6)
        self.play(Indicate(mal.suelto, color=ROJO, scale_factor=1.0), FadeIn(chispa, scale=0.3), FadeIn(tm), run_time=0.6)
        self.cerrar_voz(0.1)
        self.limpiar(bien, tb, mal, vecino, chispa, tm)

        # ------------------------------------------------------------ cierre
        self.voz("cierre")
        r1 = VGroup(cable7(3.6, 0.5, 0.9, abierto=True), VGroup(T("CABLE", 44, MARCA, "HEAVY"), T("varios hilos · flexible", 30, TINTA, "BOLD")).arrange(DOWN, buff=0.1, aligned_edge=LEFT)).arrange(RIGHT, buff=0.4)
        r2 = VGroup(alambre(3.6, 0.5, 0.9), VGroup(T("ALAMBRE", 44, TINTA, "HEAVY"), T("un solo hilo · rígido", 30, TINTA2, "BOLD")).arrange(DOWN, buff=0.1, aligned_edge=LEFT)).arrange(RIGHT, buff=0.4)
        res = VGroup(r1, r2).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, 2.8, 0])
        if res.width > 8.2:
            res.scale_to_fit_width(8.2)
        self.play(FadeIn(r1, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(max(0.1, self.resta() * 0.2))
        self.play(FadeIn(r2, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(max(0.1, self.resta() * 0.25))
        logo = ImageMobject(str(DIR / "logo_oficial.png")).scale_to_fit_width(2.2)
        usuario = T("@miguelesquit", 44, MARCA, "HEAVY")
        bs = VGroup(pastilla("SUSCRÍBETE", ROJO, 42, True), pastilla("SÍGUEME", MARCA, 42, True)).arrange(RIGHT, buff=0.3)
        fin = Group(logo, usuario, bs).arrange(DOWN, buff=0.3).move_to([0, -2.0, 0])
        fondo_t = RoundedRectangle(width=7.6, height=fin.height + 0.8, corner_radius=0.3, stroke_color="#4A5AA0", stroke_width=2).set_fill(CARTA, 0.95).move_to(fin)
        self.sfx("ding", -10)
        self.play(FadeIn(fondo_t, scale=0.9), FadeIn(logo, scale=0.7), FadeIn(usuario), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=1.3) for b in bs], lag_ratio=0.4), run_time=0.6)
        self.cerrar_voz(1.2)

    def carta(self, codigo, texto, pos):
        cod = pastilla(codigo, MARCA, 30, True)
        lineas = VGroup(*[T(l, 30, TINTA, "MEDIUM") for l in texto.split("\n")]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        cuerpo = VGroup(cod, lineas).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        caja = tarjeta(max(7.6, cuerpo.width + 0.6), cuerpo.height + 0.5, color="#4A5AA0")
        cuerpo.move_to(caja)
        return VGroup(caja, cuerpo).move_to(pos)

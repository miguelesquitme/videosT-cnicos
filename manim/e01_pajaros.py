"""
E01 · ¿POR QUÉ LOS PÁJAROS NO SE ELECTROCUTAN? (vertical 1080x1920)
Fuentes:
 - APLIC (Avian Power Line Interaction Committee), aplic.org/Electrocutions: electrocución cuando el ave une dos partes
   energizadas, o una energizada y un herraje aterrizado; plumas secas aíslan; más afectadas águilas, halcones, cuervos;
   separación recomendada 60 in (152 cm) horizontal y 40 in (102 cm) vertical.
 - Southwire, ACSR "Raven" 1/0 AWG: 0.8408 ohm/milla a 20 °C  → 5 cm a 100 A = 2.6 mV (cálculo propio).
 - OSHA eTool "Live-line bare-hand work": trabajador unido al conductor, al mismo potencial, ropa conductora,
   plataforma aislada de tierra.
"""
from comun_e import *

GUION = {
    "gancho": "Este cable lleva miles de voltios. Y este pajarito está parado encima, como si nada. "
              "¿Por qué no se electrocuta?",
    "p1": "Primero, un secreto: el voltaje, por sí solo, no hace nada. La corriente necesita una diferencia: "
          "un punto alto y un punto bajo. Es como el agua: si no hay desnivel, no corre.",
    "p2": "Ahora mira las patas del pajarito. Las dos están sobre el mismo cable, al mismo voltaje. No hay desnivel "
          "entre ellas. Así que la corriente sigue de largo por el cable, que es su camino fácil, y casi nada "
          "entra al pajarito.",
    "p3": "¿Y qué tan parecido es el voltaje en sus patas? Hicimos la cuenta con un cable de distribución típico, "
          "de aluminio con alma de acero, llevando cien amperios. Entre dos patas separadas cinco centímetros, hay "
          "menos de tres milésimas de voltio. Más de quinientas veces menos que una pila doble A.",
    "p4": "El peligro aparece cuando toca dos cosas distintas a la vez: dos cables, o un cable y un herraje "
          "conectado a tierra. Ahí sí hay desnivel, y la corriente cruza por su cuerpo.",
    "p5": "Por eso las víctimas más comunes son aves grandes: águilas, halcones y cuervos. Con las alas abiertas "
          "alcanzan dos puntos a la vez. Para protegerlas, se recomienda separar los cables por lo menos un metro "
          "y medio, o cubrirlos.",
    "p6": "Y lo más increíble: hay linieros que trabajan con las manos desnudas en líneas energizadas. Usan un "
          "traje conductor, se conectan al cable y quedan al mismo voltaje, igual que el pajarito, mientras están "
          "aislados de la tierra.",
    "p7": "Pero ojo: tú no eres un pajarito. Si estás en el suelo o en una escalera y tocas un cable, tu cuerpo "
          "une el cable con la tierra. Nunca te acerques a las líneas, ni con escaleras, varillas o piscuchas.",
    "loop": "Así que la próxima vez que veas un pajarito en un cable, ya sabes: no es valiente. "
            "Simplemente, sus dos patas están al mismo voltaje.",
    "sigueme": "Y si te gustó, sígueme para más datos de electricidad.",
}

if __name__ == "__main__":
    import sys
    tot = 0
    for k, t in GUION.items():
        w, d = audio(DIR / f"voz_e01_{SUFIJO_VOZ}", k, t)
        tot += d
        print(k, round(d, 1))
    print("total", round(tot, 1), "s ·", sum(len(t) for t in GUION.values()), "caracteres")


# ====================================================================== animación
from dibujos_aves import *
from comun_e import _osc


def y_en(curva, x):
    pts = np.array([curva.point_from_proportion(t) for t in np.linspace(0, 1, 200)])
    i = np.argmin(np.abs(pts[:, 0] - x))
    return pts[i]


def flujo(curva, n=10, color=ENERGIA, r=0.06, vel=0.18):
    """Puntos que recorren una curva continuamente (corriente)."""
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    g.fase = 0.0

    def upd(m, dt):
        m.fase = (m.fase + dt * vel) % 1
        for k, d in enumerate(m):
            d.move_to(curva.point_from_proportion((m.fase + k / n) % 1))
    g.add_updater(upd)
    upd(g, 0)
    return g


def linea_con_poste(xp=3.95, yi=0.45):
    """Vista lateral: poste de madera con la cruceta de punta, aislador de pin y el cable pasando encima."""
    palo = Rectangle(width=0.34, height=8.0, stroke_color=MADERA_OSC, stroke_width=1.4).set_fill(MADERA, 1)
    palo.move_to([xp, yi - 0.55 - 4.0, 0])
    vetas = VGroup(*[Line([xp + dx, yi - 0.7, 0], [xp + dx, yi - 8, 0], stroke_color=MADERA_OSC, stroke_width=0.7,
                          stroke_opacity=0.5) for dx in (-0.08, 0.02, 0.1)])
    punta_c = Rectangle(width=0.5, height=0.26, stroke_color=MADERA_OSC, stroke_width=1.3).set_fill(_osc(MADERA, 0.1), 1)
    punta_c.move_to([xp, yi - 0.62, 0])
    anillos = VGroup(*[Circle(radius=r, stroke_color=MADERA_OSC, stroke_width=0.6, stroke_opacity=0.6).move_to(punta_c)
                       for r in (0.05, 0.09)])
    ais = aislador_pin([xp, yi - 0.5, 0], 0.42)
    ais.shift(UP * (yi - ais[3].get_top()[1] - 0.02))
    tir = Line([xp, yi - 0.75, 0], [xp, yi - 1.6, 0], stroke_color=METAL_OSC, stroke_width=3)
    g = VGroup(palo, vetas, tir, punta_c, anillos, ais)
    c1 = linea_aerea([-5.5, yi + 0.45, 0], [xp, yi + 0.06, 0], 0.28, w=4.5)
    c2 = linea_aerea([xp, yi + 0.06, 0], [5.6, yi + 0.3, 0], 0.08, w=4.5)
    return g, c1, c2


class Pajaros(Escena):
    CARPETA_VOZ = "voz_e01"
    GUION = GUION

    def limpiar(self, *ms, t=0.4):
        ms = [m for m in ms if m is not None]
        for m in ms:
            for s in m.get_family():
                s.clear_updaters()
        self.play(*[FadeOut(m) for m in ms], run_time=t)

    def construct(self):
        self.add(encabezado("¿POR QUÉ LOS PÁJAROS", "NO SE ELECTROCUTAN?"))

        # ------------------------------------------------------------ gancho
        self.voz("gancho")
        poste_g, cab, cab2 = linea_con_poste()
        corr = flujo(cab, 14, ENERGIA, 0.05, 0.12)
        self.play(FadeIn(poste_g, shift=UP * 0.3), Create(cab), Create(cab2), run_time=0.6)
        self.add(corr)
        aviso = VGroup(simbolo_rayo(ENERGIA, 0.6), T("miles de voltios", 46, ENERGIA, "HEAVY")).arrange(RIGHT, buff=0.15)
        aviso.move_to([0.3, 3.5, 0])
        self.play(FadeIn(aviso, shift=DOWN * 0.2), run_time=0.5)
        self.sfx("whoosh", -8)
        p = pajarito().scale(1.9)
        base = y_en(cab, 0.4)
        p.shift(base - (p[1][0][0].get_end() + p[1][1][0].get_end()) / 2 + DOWN * 0.03)
        destino = p.get_center()
        p.move_to([3.6, 4.0, 0]).scale(0.6)
        self.play(p.animate.scale(1 / 0.6).move_to(destino), run_time=1.3, rate_func=rate_functions.ease_out_back)
        self.sfx("pop", -6)
        nada = pastilla("como si nada", VERDE_OK, 36).move_to([0.3, -0.9, 0])
        self.play(FadeIn(nada, scale=1.2), run_time=0.4)
        pregunta = VGroup(T("¿Por qué no se", 66, TINTA, "HEAVY"), T("electrocuta?", 84, MARCA, "HEAVY")).arrange(DOWN, buff=0.12)
        pregunta.move_to([0.3, -2.9, 0])
        self.wait(max(0.1, self.resta() - 1.9))
        self.play(FadeIn(pregunta, shift=UP * 0.3), run_time=0.5)
        self.cerrar_voz(0.2)
        self.limpiar(cab, cab2, poste_g, corr, aviso, p, nada, pregunta)

        # ------------------------------------------------------------ p1: el agua necesita desnivel
        self.voz("p1")
        t1 = VGroup(T("el voltaje, solo,", 48, TINTA, "HEAVY"), T("no hace nada", 60, ROJO, "HEAVY")).arrange(DOWN, buff=0.1)
        t1.move_to([0.3, 3.5, 0])
        self.play(FadeIn(t1, shift=DOWN * 0.2), run_time=0.5)
        A, B = tanque(0.6).scale(1.45).move_to([-1.75, 0.5, 0]), tanque(0.6).scale(1.45).move_to([2.35, 0.5, 0])
        tubo_ = Rectangle(width=B.get_left()[0] - A.get_right()[0] + 0.02, height=0.3, stroke_color=LINEA, stroke_width=1.6).set_fill("#5AB3E6", 0.75)
        tubo_.move_to([(A.get_right()[0] + B.get_left()[0]) / 2, A.get_bottom()[1] + 0.25, 0])
        self.play(FadeIn(A), FadeIn(B), FadeIn(tubo_), run_time=0.5)
        e1 = pastilla("mismo nivel → no corre", TINTA2, 36).move_to([0.3, -1.6, 0])
        self.play(FadeIn(e1), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.38))
        hA = A[1].copy().stretch_to_fit_height(A[0].height * 0.92).align_to(A[0], DOWN)
        hB = B[1].copy().stretch_to_fit_height(B[0].height * 0.28).align_to(B[0], DOWN)
        gotas = VGroup(*[Dot(radius=0.07, color="#1570EF") for _ in range(7)])
        gotas.fase = 0.0
        x0, x1, yt = tubo_.get_left()[0], tubo_.get_right()[0], tubo_.get_center()[1]

        def mover(m, dt):
            m.fase = (m.fase + dt * 0.5) % 1
            for k, d in enumerate(m):
                d.move_to([x0 + (x1 - x0) * ((m.fase + k / 7) % 1), yt, 0])
        gotas.add_updater(mover)
        e2 = pastilla("desnivel → ¡corre!", "#1570EF", 38).move_to([0.3, -1.6, 0])
        self.add(gotas)
        self.play(Transform(A[1], hA), Transform(B[1], hB), FadeOut(e1), FadeIn(e2), run_time=1.0)
        eq = VGroup(T("nivel  =  voltaje", 40, TINTA, "BOLD"),
                    T("desnivel = diferencia de voltaje", 34, MARCA, "BOLD")).arrange(DOWN, buff=0.25)
        eq.move_to([0.3, -3.2, 0])
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz()
        self.limpiar(t1, A, B, tubo_, gotas, e2, eq)

        # ------------------------------------------------------------ p2: las dos patas al mismo voltaje
        self.voz("p2")
        alambre = cable_acsr([-5.5, -0.6, 0], [5.5, -0.6, 0], 26)
        hilos = VGroup()
        p = pajarito().scale(2.7)
        pies = (p[1][0][0].get_end() + p[1][1][0].get_end()) / 2
        p.shift(np.array([0.3, -0.6 + 0.13, 0]) - pies)
        self.play(FadeIn(alambre), FadeIn(hilos), FadeIn(p, shift=DOWN * 0.3), run_time=0.6)
        ruta = Line([-5.5, -0.6, 0], [5.5, -0.6, 0])
        corr = flujo(ruta, 16, ENERGIA, 0.07, 0.1)
        self.add(corr)
        f1, f2 = p[1][0][0].get_end(), p[1][1][0].get_end()
        v1 = pastilla("V", MARCA, 40, True).move_to([f1[0] - 0.7, -1.85, 0])
        v2 = pastilla("V", MARCA, 40, True).move_to([f2[0] + 0.7, -1.85, 0])
        igual = T("=", 66, MARCA, "HEAVY").move_to([(f1[0] + f2[0]) / 2, -1.85, 0])
        ls = VGroup(DashedLine(f1 + DOWN * 0.15, v1.get_top(), stroke_color=MARCA, stroke_width=1.5, dash_length=0.06),
                    DashedLine(f2 + DOWN * 0.15, v2.get_top(), stroke_color=MARCA, stroke_width=1.5, dash_length=0.06))
        self.wait(1.0)
        self.play(Create(ls), FadeIn(v1), FadeIn(v2), run_time=0.6)
        self.play(FadeIn(igual, scale=1.4), run_time=0.3)
        dif = VGroup(T("diferencia", 46, TINTA, "BOLD"), display("0", "V", MARCA, 90)).arrange(RIGHT, buff=0.3)
        dif.move_to([0.3, -3.1, 0])
        self.play(FadeIn(dif, shift=UP * 0.2), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.4))
        sigue = pastilla("la corriente sigue por el cable", ENERGIA, 32).move_to([0.3, 3.7, 0])
        self.play(FadeIn(sigue), run_time=0.4)
        casi = T("casi nada entra al pajarito", 34, TINTA2, "BOLD").move_to([0.3, -4.1, 0])
        self.play(FadeIn(casi), run_time=0.4)
        self.cerrar_voz()
        self.limpiar(alambre, hilos, p, corr, v1, v2, igual, ls, dif, sigue, casi)

        # ------------------------------------------------------------ p3: la cuenta
        self.voz("p3")
        tit = T("HICIMOS LA CUENTA", 54, TINTA, "HEAVY").move_to([0.3, 3.85, 0])
        datos = VGroup(
            VGroup(T("cable", 32, TINTA2, "MEDIUM"), T("aluminio + acero (ACSR 1/0)", 32, TINTA, "BOLD")),
            VGroup(T("corriente", 32, TINTA2, "MEDIUM"), T("100 A", 32, TINTA, "BOLD")),
            VGroup(T("entre patas", 32, TINTA2, "MEDIUM"), T("5 cm", 32, TINTA, "BOLD")))
        for d in datos:
            d.arrange(RIGHT, buff=0.3)
        datos.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([0.3, 2.2, 0])
        caja = tarjeta(datos.width + 0.7, datos.height + 0.6).move_to(datos)
        self.play(FadeIn(tit), run_time=0.4)
        self.play(FadeIn(caja), LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in datos], lag_ratio=0.5), run_time=2.6)
        form = MathTex(r"V = I\cdot R = 100\,\mathrm{A}\times 26\,\mu\Omega", color=TINTA).scale(1.05).move_to([0.3, 0.3, 0])
        self.play(Write(form), run_time=1.2)
        res = VGroup(display("0.0026", "V", ENERGIA, 110)).move_to([0.3, -1.05, 0])
        self.sfx("ding", -12)
        self.play(FadeIn(res, scale=1.15), run_time=0.5)
        mil = T("menos de 3 milésimas de voltio", 34, ENERGIA, "BOLD").move_to([0.3, -2.1, 0])
        self.play(FadeIn(mil), run_time=0.4)
        self.wait(max(0.1, self.resta() - 4.6))
        pila = pila_aa().scale(0.62).move_to([-2.5, -3.2, 0])
        b1 = Rectangle(width=4.6, height=0.36, stroke_width=0).set_fill(TINTA, 0.85)
        b1.move_to([-1.9, -2.95, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=0.02, height=0.36, stroke_width=0).set_fill(ENERGIA, 1)
        b2.move_to([-1.9, -3.5, 0], aligned_edge=LEFT)
        l1 = T("pila AA: 1.5 V", 26, WHITE, "BOLD").move_to(b1)
        l2 = T("pajarito: 0.0026 V", 26, ENERGIA, "BOLD").next_to(b2, RIGHT, buff=0.15)
        self.play(FadeIn(pila), GrowFromEdge(b1, LEFT), FadeIn(l1), run_time=0.7)
        self.play(FadeIn(b2), FadeIn(l2), run_time=0.4)
        x500 = pastilla("más de 500 veces menos", MARCA, 32, True).move_to([0.3, -4.15, 0])
        self.play(FadeIn(x500, scale=1.2), run_time=0.4)
        fu = fuente("Southwire ACSR Raven 1/0 · cálculo propio", [0.3, -4.6, 0], 20)
        self.add(fu)
        self.cerrar_voz()
        self.limpiar(tit, caja, datos, form, res, mil, pila, b1, b2, l1, l2, x500, fu)

        # ------------------------------------------------------------ p4: dos cosas a la vez
        self.voz("p4")
        wA = cable_acsr([-5.5, 2.0, 0], [5.5, 2.0, 0], 16)
        wB = cable_acsr([-5.5, -0.4, 0], [5.5, -0.4, 0], 16)
        eA = pastilla("cable A", TINTA2, 28).move_to([2.5, 2.6, 0])
        eB = pastilla("cable B", TINTA2, 28).move_to([2.5, 0.2, 0])
        self.play(FadeIn(wA), FadeIn(wB), FadeIn(eA), FadeIn(eB), run_time=0.5)
        # ave grande parada en B que toca A con el ala
        cuervo_ = cuervo().scale(2.0)
        pies = (cuervo_[1][0][0].get_end() + cuervo_[1][1][0].get_end()) / 2
        cuervo_.shift(np.array([-0.9, -0.4 + 0.1, 0]) - pies)
        hombro = cuervo_[4].get_center()
        ala_up = Polygon(hombro + LEFT * 0.15, hombro + RIGHT * 0.25, np.array([0.5, 2.0 - 0.08, 0]),
                         np.array([0.1, 2.0 - 0.08, 0]), stroke_color=LINEA, stroke_width=1.6).set_fill("#14171D", 1)
        self.play(FadeIn(cuervo_, shift=DOWN * 0.2), run_time=0.5)
        self.play(GrowFromPoint(ala_up, hombro), run_time=0.6)
        r1 = rayo([0.3, 1.9, 0], cuervo_[1][0][0].get_end(), ENERGIA, 6, 0.12, 2)
        self.sfx("pop", -4)
        self.add(r1)
        x1 = equis(ROJO, 0.4).move_to([1.7, 1.0, 0])
        c1 = pastilla("cable + cable", ROJO, 32).move_to([0.3, 3.3, 0])
        self.play(FadeIn(x1, scale=1.4), FadeIn(c1), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.25))
        # caso 2: cable + herraje aterrizado
        herr = VGroup(Rectangle(width=3.2, height=0.22, stroke_color=METAL_OSC, stroke_width=1.4).set_fill(METAL2, 1)
                      .move_to([-0.6, -2.55, 0]),
                      Line([-0.6, -2.66, 0], [-0.6, -3.3, 0], stroke_color=TIERRA, stroke_width=3))
        tierra_s = VGroup(*[Line([-0.6 - w, -3.3 - 0.13 * k, 0], [-0.6 + w, -3.3 - 0.13 * k, 0], stroke_color=TIERRA,
                                 stroke_width=3) for k, w in enumerate((0.32, 0.21, 0.1))])
        et = T("herraje a tierra", 28, TIERRA, "BOLD").move_to([2.4, -2.55, 0])
        self.play(FadeIn(herr), FadeIn(tierra_s), FadeIn(et), FadeOut(r1), run_time=0.5)
        r2 = rayo([-1.3, -0.52, 0], [-1.3, -2.44, 0], ENERGIA, 6, 0.12, 4)
        self.sfx("pop", -4)
        self.add(r2)
        c2 = pastilla("cable + tierra", ROJO, 32).move_to([0.3, -3.95, 0])
        self.play(FadeIn(c2), FadeIn(equis(ROJO, 0.4).move_to([1.2, -1.5, 0]), scale=1.4), run_time=0.3)
        desn = T("¡ahí sí hay desnivel!", 44, ROJO, "HEAVY").move_to([0.3, 3.95, 0])
        self.play(FadeIn(desn, shift=DOWN * 0.2), run_time=0.4)
        self.add(fuente("APLIC · aplic.org/Electrocutions", [0.3, -4.55, 0]))
        self.cerrar_voz()
        self.limpiar(*[m for m in self.mobjects[2:]])

        # ------------------------------------------------------------ p5: águilas y separación
        self.voz("p5")
        po, pts = poste(6.5, 6.4, 2)
        delta = np.array([0.3, 0.2, 0]) - np.array([0, pts[0][1], 0])
        po.shift(delta)
        pts = [q + delta for q in pts]
        conds = VGroup(*[conductor_frente(q, 0.17) for q in pts])
        econd = VGroup(*[T("cable", 26, TINTA2, "BOLD").next_to(c, UP, buff=0.2) for c in conds])
        vista = T("vista de frente", 26, TINTA2, "MEDIUM").move_to([2.4, -1.35, 0])
        self.play(FadeIn(po, shift=UP * 0.3), FadeIn(conds), FadeIn(econd), FadeIn(vista), run_time=0.7)
        espec = VGroup(pastilla("águilas", "#5A3E2B", 30), pastilla("halcones", "#5A3E2B", 30),
                       pastilla("cuervos", "#5A3E2B", 30)).arrange(RIGHT, buff=0.18).move_to([0.3, 3.85, 0])
        self.play(LaggedStart(*[FadeIn(e, scale=1.2) for e in espec], lag_ratio=0.3), run_time=1.0)
        cruceta_top = po[3].get_top()[1]
        ag = aguila(envergadura=6.3)
        ag.shift(np.array([0.3, cruceta_top, 0]) - ag[3].get_bottom())
        self.play(FadeOut(econd), FadeIn(ag, scale=0.6), run_time=0.8)
        self.wait(max(0.1, self.resta() * 0.15))
        ra = rayo(pts[0] + UP * 0.12, [pts[0][0], ag[0][0].get_bottom()[1] + 0.02, 0], ENERGIA, 3, 0.05, 1, 4)
        rb = rayo(pts[1] + UP * 0.12, [pts[1][0], ag[1][0].get_bottom()[1] + 0.02, 0], ENERGIA, 3, 0.05, 3, 4)
        dos = pastilla("alcanza dos cables a la vez", ROJO, 34).move_to([0.3, 3.0, 0])
        self.sfx("pop", -5)
        self.play(FadeIn(ra), FadeIn(rb), FadeIn(dos, scale=1.1), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.4))
        self.play(FadeOut(ag), FadeOut(ra), FadeOut(rb), FadeOut(dos), FadeOut(espec), run_time=0.4)
        y_m = pts[0][1] + 1.0
        med = DoubleArrow([pts[0][0], y_m, 0], [pts[1][0], y_m, 0], buff=0, stroke_width=2.5, color=MARCA,
                          tip_length=0.22, max_tip_length_to_length_ratio=0.1)
        marcas = VGroup(*[DashedLine([x, pts[0][1] + 0.2, 0], [x, y_m + 0.18, 0], stroke_color=MARCA, stroke_width=1.5,
                                     dash_length=0.07) for x in (pts[0][0], pts[1][0])])
        cifra = VGroup(T("al menos", 32, MARCA, "BOLD"), T("152 cm", 72, MARCA, "HEAVY")).arrange(DOWN, buff=0.05)
        cifra.next_to(med, UP, buff=0.15)
        self.play(GrowFromCenter(med), Create(marcas), FadeIn(cifra), run_time=0.7)
        cub = VGroup(*[Arc(radius=0.24, start_angle=-0.2, angle=PI + 0.4, stroke_color="#B54708", stroke_width=1.5)
                       .set_fill(ENERGIA, 1).move_to(q + UP * 0.08) for q in pts])
        o = pastilla("o cubrir los cables", ENERGIA, 36).move_to([0.3, -2.0, 0])
        self.play(FadeIn(cub), FadeIn(o), run_time=0.5)
        self.add(fuente("APLIC: 60 in (152 cm) horizontal · 40 in (102 cm) vertical", [0.3, -4.0, 0], 22))
        self.cerrar_voz()
        self.limpiar(*[m for m in self.mobjects[2:]])

        # ------------------------------------------------------------ p6: linieros a mano desnuda
        self.voz("p6")
        wl = cable_acsr([-5.5, 3.0, 0], [5.5, 3.0, 0], 16)
        suelo = VGroup(Line([-5.5, -3.75, 0], [5.5, -3.75, 0], stroke_color=LINEA, stroke_width=2),
                       *[Line([x, -3.75, 0], [x - 0.2, -3.98, 0], stroke_color=LINEA, stroke_width=1) for x in np.arange(-4, 5, 0.35)])
        camion = camion_canastilla(np.array([2.0, -3.15, 0]), np.array([0.45, -0.45, 0]))
        camion.scale(1.25, about_point=np.array([2.0, -3.5, 0]))
        canasta = camion.canasta
        lin = persona(METAL2, "#FEC84B").scale(0.85)
        lin.move_to(canasta.get_center() + DOWN * 0.15, aligned_edge=DOWN)
        malla = VGroup(*[Line(lin[1][0].get_corner(DL) + RIGHT * x, lin[1][0].get_corner(DL) + RIGHT * x + UP * 0.6,
                              stroke_color=_osc(METAL2, 0.25), stroke_width=0.6) for x in np.arange(0.06, 0.5, 0.07)])
        br = brazo(lin[1].get_top() + DOWN * 0.15 + RIGHT * 0.18, [1.2, 2.92, 0], METAL2, 11, guante="#667085")
        pertiga = cable(canasta.get_corner(UL) + RIGHT * 0.08, [-0.6, 2.1, 0], [-0.8, 3.0, 0], color=ENERGIA, w=4, suave=True)
        puente = pertiga
        pinza = RoundedRectangle(width=0.16, height=0.22, corner_radius=0.04, stroke_color=LINEA, stroke_width=1).set_fill(METAL2, 1).move_to([-0.8, 3.05, 0])
        self.play(FadeIn(wl), Create(suelo), FadeIn(camion), run_time=0.6)
        self.play(FadeIn(lin), FadeIn(malla), run_time=0.5)
        self.bring_to_front(canasta)
        self.play(FadeIn(br), run_time=0.4)
        mano = pastilla("¡con la mano desnuda!", ENERGIA, 34).move_to([0.3, 3.85, 0])
        self.play(FadeIn(mano, scale=1.2), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.25))
        traje = T("traje conductor", 30, METAL_OSC, "BOLD").move_to([-2.3, 1.2, 0])
        self.play(Create(puente), FadeIn(pinza), FadeIn(traje), run_time=0.7)
        mismo = pastilla("mismo voltaje que el cable", MARCA, 32, True).move_to([0.3, 3.85, 0])
        self.play(FadeOut(mano), FadeIn(mismo, scale=1.1), run_time=0.4)
        self.wait(max(0.1, self.resta() * 0.35))
        ais = VGroup(T("pluma aislada", 30, "#B54708", "BOLD").move_to([-1.6, -0.6, 0]),
                     T("aislado de tierra", 40, TINTA, "HEAVY").move_to([-1.6, -2.6, 0]))
        self.play(FadeIn(ais), run_time=0.5)
        self.add(fuente("OSHA, Live-line bare-hand work (eTool)", [0.3, -4.7, 0], 22))
        self.cerrar_voz()
        self.limpiar(*[m for m in self.mobjects[2:]])

        # ------------------------------------------------------------ p7: tú no eres un pajarito
        self.voz("p7")
        wl = cable_acsr([-5.5, 3.3, 0], [5.5, 3.3, 0], 16)
        suelo = VGroup(Line([-5.5, -2.6, 0], [5.5, -2.6, 0], stroke_color=LINEA, stroke_width=2),
                       *[Line([x, -2.6, 0], [x - 0.2, -2.85, 0], stroke_color=LINEA, stroke_width=1) for x in np.arange(-4, 5, 0.35)])
        yo = persona(MARCA).scale(1.55).move_to([-0.9, -2.6, 0], aligned_edge=DOWN)
        hombro = yo[1].get_top() + RIGHT * 0.4 + DOWN * 0.15
        mano_ = hombro + np.array([0.75, 0.6, 0])
        br = brazo(hombro, mano_, MARCA, 15)
        varilla = Line(mano_ + DOWN * 0.2 + LEFT * 0.15, [2.3, 3.3, 0], stroke_color=METAL_OSC, stroke_width=5)
        noeres = T("tú no eres un pajarito", 44, TINTA, "HEAVY").move_to([0.3, 4.0, 0])
        self.play(FadeIn(noeres), FadeIn(wl), FadeIn(suelo), FadeIn(yo), FadeIn(br), run_time=0.5)
        self.play(Create(varilla), run_time=0.7)
        camino = VMobject().set_points_as_corners([[2.3, 3.25, 0], mano_, yo[1].get_center(), yo[0][0].get_bottom() + UP * 0.05,
                                                   [-1.2, -2.6, 0]])
        camino.set_stroke(ROJO, 7, 0.85)
        self.sfx("pop", -3)
        self.play(Create(camino), run_time=0.7)
        une = pastilla("tu cuerpo une cable y tierra", ROJO, 32).move_to([0.3, -3.5, 0])
        self.play(FadeIn(une), FadeIn(equis(ROJO, 0.45).move_to([2.6, 0.5, 0]), scale=1.3), run_time=0.4)
        self.wait(max(0.1, self.resta() - 4.8))
        self.limpiar(*[m for m in self.mobjects[2:]], t=0.3)
        nunca = VGroup(T("NUNCA", 76, ROJO, "HEAVY"), T("te acerques a las líneas", 40, TINTA, "HEAVY")).arrange(DOWN, buff=0.12)
        nunca.move_to([0.3, 3.3, 0])
        iconos = VGroup(escalera(2.2, 0.6), Line([0, 0, 0], [0, 2.3, 0], stroke_color=METAL_OSC, stroke_width=5),
                        piscucha().scale(1.15))
        iconos.arrange(RIGHT, buff=1.75).move_to([0.3, 0.2, 0])
        prohib = VGroup(*[no_simbolo(0.95).move_to(i) for i in iconos])
        nombres = VGroup(*[T(n, 32, TINTA, "BOLD").move_to([i.get_center()[0], -1.45, 0]) for n, i in
                           zip(("escaleras", "varillas", "piscuchas"), iconos)])
        self.play(FadeIn(nunca, scale=1.1), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(i) for i in iconos], lag_ratio=0.3), FadeIn(nombres), run_time=0.9)
        self.sfx("tic", -6)
        self.play(LaggedStart(*[Create(p_) for p_ in prohib], lag_ratio=0.25), run_time=0.8)
        self.cerrar_voz()
        self.limpiar(nunca, iconos, prohib, nombres)

        # ------------------------------------------------------------ cierre en bucle
        self.voz("loop")
        poste_g, cab, cab2 = linea_con_poste()
        corr = flujo(cab, 14, ENERGIA, 0.05, 0.12)
        p = pajarito().scale(1.9)
        base = y_en(cab, 0.4)
        p.shift(base - (p[1][0][0].get_end() + p[1][1][0].get_end()) / 2 + DOWN * 0.03)
        self.play(FadeIn(poste_g), Create(cab), Create(cab2), FadeIn(p), run_time=0.6)
        self.add(corr)
        val = T("no es valiente", 60, TINTA2, "HEAVY").move_to([0.3, -1.4, 0])
        self.play(FadeIn(val), run_time=0.4)
        tacha = Line(val.get_left() + LEFT * 0.1, val.get_right() + RIGHT * 0.1, stroke_color=ROJO, stroke_width=5)
        self.wait(max(0.1, self.resta() * 0.25))
        self.play(Create(tacha), run_time=0.4)
        mv = pastilla("sus dos patas: mismo voltaje", MARCA, 36, True).move_to([0.3, -2.9, 0])
        self.play(FadeIn(mv, scale=1.15), run_time=0.5)
        self.cerrar_voz(0.1)

        # ------------------------------------------------------------ sígueme
        self.voz("sigueme")
        logo = ImageMobject(str(DIR / "logo_letras.png")).scale_to_fit_width(2.2)
        usuario = T("@miguelesquit", 44, MARCA, "HEAVY")
        boton = pastilla("SÍGUEME", ROJO, 50, True)
        sub = T("más datos de electricidad ⚡", 32, TINTA, "BOLD")
        tarjeta_ = Group(logo, usuario, boton, sub).arrange(DOWN, buff=0.3).move_to([0.3, -2.5, 0])
        fondo_t = RoundedRectangle(width=6.6, height=tarjeta_.height + 0.7, corner_radius=0.3, stroke_color=MARCA_CL,
                                   stroke_width=2).set_fill(WHITE, 0.97).move_to(tarjeta_)
        self.play(FadeOut(val), FadeOut(tacha), FadeOut(mv), FadeIn(fondo_t, scale=0.9), run_time=0.35)
        self.sfx("ding", -10)
        self.play(FadeIn(logo, scale=0.7), FadeIn(usuario, shift=UP * 0.2), run_time=0.45)
        self.play(FadeIn(boton, scale=1.4), FadeIn(sub), run_time=0.4)
        self.play(boton.animate.scale(1.08), run_time=0.25)
        self.play(boton.animate.scale(1 / 1.08), run_time=0.25)
        self.cerrar_voz(0.9)

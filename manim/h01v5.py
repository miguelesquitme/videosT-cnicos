"""H01 v5 · Arranque directo — Correcciones_V del usuario (23-nov).
P1 bloques traseros nuevos; el frente de la puerta solo al inicio ("por temas didácticos se ve por detrás").
P2 borneras y riel DIN nuevos.  P3 cables por arriba o por abajo.  P4 curvas abiertas, marcador en recta.
P5 más espacio.  P6 un hilo a la vez.  P7 los hilos ya conectados se opacan.  P8 cableado más lento.
P9 manguera TSJ 4 × 8 AWG al motor; medición de corriente con zoom en la caja del motor, un solo conductor.
P10 puesta en marcha: continuidad bajo -F2 sin energía (fases entre sí y contra tierra), luego energía y corriente.
Render: FORMATO=h TEMA=gris VOZ=eleven manim -qh --disable_caching -o h01v5 h01v5.py H01v5"""
import os
os.environ.setdefault("TEMA", "gris")
import h01v3 as _V3
from h01v3 import *                                          # noqa: F401,F403
from h01v3 import H01v3, eje_girando, MARCA_D, OSC, OSC2
import h01v5_lay as L5
from h01v5_lay import Eq3, K, KB, KD, KF, ROJO_M, NEUTRO_C, NEGRO_P, PE_V, PE_A
from h01v5_guion import GUION as G5
from diag_lit import diagrama_mando, diagrama_potencia
from h01v2_diag import HILOS_POT

# P9: la salida al motor es una manguera TSJ (fila nueva en la lista de materiales)
for _i, _f in enumerate(_V3.MATERIALES):
    if _f[1] == "Cable de potencia":
        _V3.MATERIALES[_i] = (_f[0], _f[1], _f[2], "Dentro del gabinete")
if not any(f[1] == "Manguera TSJ" for f in _V3.MATERIALES):
    _V3.MATERIALES.append(("Según distancia", "Manguera TSJ", "4 × 8 AWG · 3 negros + verde/amarillo · 600 V", "-X1 → -M1"))

# marcas en el diagrama de mando, UNA por hilo (coordenadas del original)
M_MANDO = {
    "c1": [[(47, 40), (47, 51), (137, 51), (137, 96)]],
    "c2a": [[(137, 155), (137, 186), (317, 186), (317, 412)]],
    "c2b": [[(137, 155), (137, 186), (137, 215)]],
    "c3": [[(137, 273), (137, 307)]],
    "c4a": [[(137, 363), (137, 412)]],
    "c4b": [[(137, 363), (137, 381), (227, 381), (227, 412)]],
    "c5a": [[(137, 470), (137, 516), (227, 516)], [(227, 470), (227, 516)]],
    "c5b": [[(227, 470), (227, 516), (137, 516), (137, 571)]],
    "c5c": [[(137, 470), (137, 516), (227, 516), (227, 576)]],
    "c6": [[(317, 470), (317, 576)]],
    "c7a": [[(32, 639), (32, 651), (137, 651), (137, 611)]],
    "c7b": [[(137, 651), (227, 651), (227, 606)]],
    "c7c": [[(227, 651), (317, 651), (317, 606)]],
}
M_POT = {
    "p1a": [HILOS_POT["p1"][0]], "p1b": [HILOS_POT["p1"][1]], "p1c": [HILOS_POT["p1"][2]],
    "p2a": [HILOS_POT["p2"][0]], "p2b": [HILOS_POT["p2"][1]], "p2c": [HILOS_POT["p2"][2]],
    "p4a": [HILOS_POT["p4"][0]], "p4b": [HILOS_POT["p4"][1]], "p4c": [HILOS_POT["p4"][2]],
    "pe": HILOS_POT["pe"],
}
DIAG_MANDO = dict(alto=6.8, centro=(-4.75, -0.35))
DIAG_POT = dict(alto=6.4, centro=(-4.7, -0.35))
RT_CABLE = 2.8          # P8: más lento


class H01v5(H01v3):
    CARPETA_VOZ = "voz_h01v2"
    GUION = G5

    # ------------------------------------------------------------------ utilidades
    def cambiar(self, viejo, nombre, k=None):
        n = Eq3(nombre, k or viejo.k, base=viejo.base)
        n.img.scale_to_fit_height(viejo.img.height).move_to(viejo.img)
        n.k = viejo.k
        n.set_z_index(viejo.z_index)
        self.remove(viejo)
        self.add(n)
        return n

    def montar(self):
        E = L5.disposicion()
        return E, Group(L5.riel_din(E))

    def aro(self, p, col=None, r=0.075):
        return Circle(radius=r, color=col or "#F79009", stroke_width=5).move_to(p).set_z_index(9)

    def tender5(self, c, marcas, ancla_ini=None, rt=RT_CABLE):
        """P6-P8: un solo cable, lento; aros en el origen y en el destino; al terminar se queda a color."""
        self.marcas = getattr(self, "marcas", [])
        self.marcas += marcas
        a0 = c.ruta.get_start()
        a1 = c.ruta.get_end()
        r0 = self.aro(a0)
        if ancla_ini:
            self.en(ancla_ini, 0.25)
        self.play(Create(r0), run_time=0.35)
        self.play(Create(c.conductor), *[Create(m) for m in marcas], run_time=rt, rate_func=linear)
        r1 = self.aro(a1)
        self.sfx("tornillo", -10)
        self.play(FadeIn(c.puntas), Create(r1), run_time=0.5)
        self.play(FadeOut(r0), FadeOut(r1), run_time=0.3)

    def opacar(self, cables, marcas, op=0.32):
        anims = [a for c in cables for a in c.opaco(op)] + [m.animate.set_stroke(opacity=0.30) for m in marcas]
        if anims:
            self.play(*anims, run_time=0.35)

    # =============================================================== 4 · MATERIALES (+ fila de la manguera TSJ)
    def h_materiales(self):
        self.seccion("materiales")
        self.voz("materiales")
        anchos = [1.25, 3.0, 7.6, 3.4]
        x0 = -sum(anchos) / 2
        anclas = ["motor", "F2", "F1", "KM1", "F3", "S0", "S1", "H1", "H2", "6", "azul",
                  "2", "separador", "negro", "rojo", "claro", "verde", "tierra", "rieldin", "canaleta", "gabinete", "gabinete"]
        M = _V3.MATERIALES
        paginas = [M[:11], M[11:]]
        idx = 0
        for pg, filas in enumerate(paginas):
            tb = _V3.tabla_clara(filas, anchos, x0, 3.55, 0.5, 17, ["Cantidad", "Nombre", "Características", "Observación"])
            if pg == 0:
                self.play(FadeIn(tb[0]), run_time=0.4)
            for k, fila in enumerate(tb[1:]):
                self.en(anclas[min(idx, len(anclas) - 1)], 0.2)
                if pg == 1 and k == 0:
                    self.play(FadeOut(self.tb_ant[1:]), FadeIn(tb[0]), FadeOut(self.tb_ant[0]), run_time=0.35)
                self.sfx("pop", -18)
                self.play(FadeIn(fila, shift=UP * 0.1), run_time=0.3)
                idx += 1
            self.tb_ant = tb
        self.cerrar_voz(0.4)
        self.wait(1.2)
        self.salir()

    # =============================================================== 7 · CONEXIÓN DEL MANDO
    def h_c_mando(self):
        self.seccion("c_mando")
        E, fondo = self.montar()
        H = diagrama_mando(**DIAG_MANDO)
        frentes = [E[n] for n in ("S0", "S1", "H1", "H2")]
        traseros = [E[n + "b"] for n in ("S0", "S1", "H1", "H2")]
        marco = L5.puerta_marco(E)
        t_frente = T("PUERTA · vista frontal", 17, "#475467", "HEAVY").move_to(marco[1]).align_to(marco[1], LEFT)
        equipos = [E[k] for k in ("F2", "F1", "KM1", "F3", "X0", "X1")]
        self.voz("c_intro_5")
        self.play(FadeIn(H.todo()), FadeIn(fondo), *[FadeIn(e) for e in equipos], FadeIn(marco[0]), FadeIn(t_frente),
                  *[FadeIn(f, shift=UP * 0.1) for f in frentes], run_time=1.2)
        self.en("frente", 0.1)
        aros = VGroup(*[SurroundingRectangle(f.img, buff=-0.02, color="#F79009", stroke_width=4) for f in frentes])
        self.play(LaggedStart(*[Create(a) for a in aros], lag_ratio=0.15), run_time=0.8)
        self.play(FadeOut(aros), run_time=0.3)
        self.en("detrás", 0.2)
        # P1-D: se gira la puerta: el frente se va y aparece la parte de atrás (mismo cuadro)
        self.play(*[f.animate.stretch(0.02, 0) for f in frentes], run_time=0.45)
        for b in traseros:
            b.stretch(0.02, 0)
        self.remove(*frentes)
        self.play(*[b.animate.stretch(50, 0) for b in traseros], FadeTransform(t_frente, marco[1]), run_time=0.45)
        for b, f in zip(traseros, frentes):
            b.img.move_to([f.img.get_center()[0], b.img.get_center()[1], 0])
        self.en("bloque", 0.1)
        cont = VGroup(*[SurroundingRectangle(b.img, buff=0.0, color="#F79009", stroke_width=4) for b in traseros])
        self.play(LaggedStart(*[Create(a) for a in cont], lag_ratio=0.15), run_time=0.8)
        self.play(FadeOut(cont), run_time=0.3)
        self.cerrar_voz(0.1)
        for n in ("S0", "S1", "H1", "H2"):
            E.pop(n)
        self.cables = Group()
        hechos, marcas_hechas = [], []
        for clave, c, _ in L5.hilos_mando(E):
            self.voz(clave + "_5")
            self.opacar(hechos, marcas_hechas)
            ms = [H.marca(tr) for tr in M_MANDO[clave]]
            self.wait(0.3)
            self.tender5(c, ms)
            self.cables.add(c)
            hechos, marcas_hechas = [c], ms
            self.cerrar_voz(0.25)
        self.opacar(hechos, marcas_hechas)
        self.play(*[cc.conductor.animate.set_stroke(opacity=1) for cc in self.cables], *[cc.puntas.animate.set_opacity(1) for cc in self.cables],
                  run_time=0.6)
        self.wait(0.8)
        self.E, self.fondo_tab, self.marco = E, fondo, marco
        self.play(FadeOut(H.todo()), *[FadeOut(m) for m in self.marcas], run_time=0.4)
        self.marcas = []

    # =============================================================== 8 · CONEXIÓN DE POTENCIA
    def asegurar_mando(self):
        if not hasattr(self, "E"):
            E, fondo = self.montar()
            for n in ("S0", "S1", "H1", "H2"):
                E.pop(n)
            self.E, self.fondo_tab = E, fondo
            self.marco = L5.puerta_marco(E)
            self.cables = Group(*[c for _, c, _ in L5.hilos_mando(E)])
            self.add(fondo, self.marco, *E.values(), self.cables)

    def motor_en_esquema(self):
        mo = Eq3("M1", 0.0095)
        mo.img.move_to([5.2, -2.55, 0])
        tsj = L5.manguera_tsj(self.E, mo)
        return mo, tsj

    def h_c_potencia(self):
        self.asegurar_mando()
        E = self.E
        self.seccion("c_potencia")
        self.voz("p_intro_5")
        H = diagrama_potencia(**DIAG_POT)
        self.play(FadeIn(H.todo()), *[a for c in self.cables for a in c.opaco(0.22)], run_time=0.8)
        red = L5.red_entrada(E)
        lred = T("Red 208Y/120 V", 16, TXT2, "BOLD").next_to(E["X0"].img, DOWN, buff=0.45).shift(LEFT * 0.9)
        self.play(FadeIn(red), FadeIn(lred), run_time=0.5)
        self.cerrar_voz(0.1)
        P = L5.hilos_potencia(E)
        self.cab_pot = Group()
        hechos, mh = [], []

        def uno(clave, c):
            nonlocal hechos, mh
            self.voz(clave + "_5")
            self.opacar(hechos, mh)
            ms = [H.marca(tr) for tr in M_POT[clave]]
            self.wait(0.3)
            self.tender5(c, ms)
            self.cab_pot.add(c)
            hechos, mh = [c], ms
            self.cerrar_voz(0.25)
        for i, k in enumerate(("p1a", "p1b", "p1c")):
            uno(k, P["p1"][i])
        for i, k in enumerate(("p2a", "p2b", "p2c")):
            uno(k, P["p2"][i])
        self.opacar(hechos, mh)
        hechos, mh = [], []
        # p3 · el térmico se monta debajo del contactor
        self.voz("p3")
        F3, KM1 = E["F3"], E["KM1"]
        ms = [H.marca(tr) for tr in HILOS_POT["p3"]]
        self.play(F3.animate.shift(DOWN * 0.30), run_time=0.4)
        self.play(F3.animate.shift(UP * 0.30), *[Create(m) for m in ms], run_time=0.9)
        self.marcas += ms
        self.sfx("tornillo", -8)
        anillos = VGroup(*[Circle(radius=0.085, color=AMB, stroke_width=5).move_to(KM1.p(t)) for t in ("2/T1", "4/T2", "6/T3")])
        self.play(LaggedStart(*[Create(a) for a in anillos], lag_ratio=0.3), run_time=0.9)
        self.play(FadeOut(anillos), *[m.animate.set_stroke(opacity=0.3) for m in ms], run_time=0.3)
        self.cerrar_voz(0.05)
        for i, k in enumerate(("p4a", "p4b", "p4c")):
            uno(k, P["p4"][i])
        uno("pe", P["pe"][0])
        self.opacar(hechos, mh)
        # P9 · manguera TSJ hasta el motor
        self.voz("tsj_5")
        mo, tsj = self.motor_en_esquema()
        ms = [H.marca(tr) for tr in HILOS_POT["p5"]]
        self.marcas += ms
        self.play(FadeIn(mo, shift=LEFT * 0.2), run_time=0.6)
        self.en("manguera", 0.2)
        self.play(Create(tsj[0]), run_time=1.0)
        self.play(Create(tsj[1]), *[Create(m) for m in ms], run_time=2.6, rate_func=linear)
        self.en("tsj", 0.2)
        self.play(FadeIn(tsj[2]), run_time=0.4)
        self.cerrar_voz(0.2)
        self.mo, self.tsj = mo, tsj
        # caja del motor (reutiliza el clip p5)
        self.voz("p5")
        velo = Rectangle(width=16.5, height=9.5, stroke_width=0).set_fill("#E4E7EB", 0.94).set_z_index(30)
        cb = Eq3("CB", 0.036).move_to([1.8, -0.5, 0]).set_z_index(31)
        tit = Paragraph("Caja del motor", "9 puntas en estrella · 208 V", font=SANS, font_size=26, weight="HEAVY", color=TXT, line_spacing=0.7).next_to(cb, LEFT, buff=0.6).shift(UP * 1.2).set_z_index(31)
        llegan = self.colas_caja(cb, z=32)
        self.play(FadeIn(velo), FadeIn(cb), FadeIn(tit), run_time=0.7)
        self.play(Create(llegan), run_time=1.0)
        for a_, b_, pal in (("T1", "T7", "t1"), ("T2", "T8", "t2"), ("T3", "T9", "t3")):
            self.en(pal, 0.2)
            r = Line(cb.p(a_), cb.p(b_)).set_stroke(MARCA_D, 14, opacity=0.65).set_z_index(34)
            self.sfx("tic", -10)
            self.play(Create(r), run_time=0.4)
        self.en("t4", 0.2)
        r = Line(cb.p("T4"), cb.p("T6")).set_stroke(MARCA_D, 14, opacity=0.65).set_z_index(34)
        self.play(Create(r), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(*[FadeOut(m) for m in self.mobjects if getattr(m, "z_index", 0) >= 30 and m is not self.cinta_act], run_time=0.5)
        # ajuste del dial
        self.voz("p6")
        dial = F3.mm(196 * 45 / 685, 222 * 45 / 685)
        lab = etiqueta("ajuste 26,5 A", AMB, 22).scale(0.55).next_to(dial, LEFT, buff=0.55)
        aro = Circle(radius=0.14, color=AMB, stroke_width=5).move_to(dial)
        self.sfx("tic", -8)
        self.play(FadeIn(lab), Create(aro), run_time=0.7)
        self.cerrar_voz(0.2)
        self.play(FadeOut(lab), FadeOut(aro), run_time=0.3)
        self.play(FadeOut(H.todo()), *[FadeOut(m) for m in self.marcas],
                  *[a for c in list(self.cables) + list(self.cab_pot) for a in c.opaco(1.0)], run_time=0.6)
        self.marcas = []

    def colas_caja(self, cb, z=32):
        """Manguera TSJ entrando a la caja: se abre la chaqueta y cada conductor va a su borne (T1 T2 T3) + PE a la caja."""
        g = VGroup()
        top = cb.img.get_top()[1] + 0.9
        xs = [cb.p(t)[0] for t in ("T1", "T2", "T3")]
        xc = sum(xs) / 3
        jac = Line([xc, top + 1.2, 0], [xc, top, 0]).set_stroke("#0B0B0C", 34)
        g.add(fisico(jac))
        for t, x in zip(("T1", "T2", "T3"), xs):
            a = cb.p(t)
            m = ruta_redondeada([[xc + (x - xc) * 0.08, top, 0], [x, top - 0.45, 0], [x, a[1], 0]], 0.3).set_stroke(NEGRO_P, 12).set_fill(opacity=0)
            ojo = Circle(radius=0.10).set_stroke("#B87333", 6).set_fill(opacity=0).move_to(a)
            g.add(VGroup(fisico(m), ojo))
        pe_p = cb.img.get_corner(UR) + LEFT * 0.32 + DOWN * 0.32
        m = ruta_redondeada([[xc + 0.05, top, 0], [pe_p[0], top - 0.3, 0], pe_p], 0.3).set_fill(opacity=0)
        g.add(VGroup(fisico(m.copy().set_stroke(PE_V, 12)), fisico(DashedVMobject(m.copy(), num_dashes=14).set_stroke(PE_A, 12)),
                     T("PE", 18, TXT, "HEAVY").next_to(pe_p, LEFT, buff=0.12)))
        g.set_z_index(z)
        return g

    # =============================================================== 9 · PUESTA EN MARCHA (P10)
    def h_marcha(self):
        if not hasattr(self, "mo"):
            self.asegurar_mando()
            P = L5.hilos_potencia(self.E)
            self.cab_pot = Group(*[c for v in P.values() for c in v])
            self.mo, self.tsj = self.motor_en_esquema()
            self.add(L5.red_entrada(self.E), self.cab_pot, self.mo, self.tsj)
        self.seccion("marcha")
        E, mo = self.E, self.mo
        mm = Eq3("MMol", 0.024).move_to([-5.3, -1.75, 0])

        def sondas(a, b):
            ra = cable(mm.p("VΩ"), mm.p("VΩ") + DOWN * 0.5, [mm.p("VΩ")[0] + 0.5, -4.1, 0], [a[0] - 0.4, a[1] - 0.6, 0], a, color=ROJO, w=4, suave=True)
            rb = cable(mm.p("COM"), mm.p("COM") + DOWN * 0.7, [mm.p("COM")[0] + 0.3, -4.35, 0], [b[0] - 0.3, b[1] - 0.6, 0], b, color="#2B2C2E", w=4, suave=True)
            tips = VGroup(Dot(a, radius=0.045, color=ROJO), Dot(b, radius=0.045, color="#2B2C2E"))
            return VGroup(ra, rb, tips).set_z_index(12)

        def pantalla(nombre):
            nuevo = Eq3(nombre, mm.k)
            nuevo.img.move_to(mm.img)
            return nuevo

        def nota(txt, col, y):
            return etiqueta(txt, col, 24).scale(0.75).move_to([-4.6, y, 0])

        # ---- P10 · continuidad bajo -F2, sin energía y con -F2 cerrado
        self.voz("frio_5")
        self.play(FadeIn(mm, shift=RIGHT * 0.3), run_time=0.5)
        self.en("cerramos")
        self.sfx("breaker", -6)
        E["F2"] = self.cambiar(E["F2"], "F2on")
        sin = nota("SIN energía · -F2 cerrado (ON)", "#B42318", 3.05)
        self.play(FadeIn(sin), Flash(E["F2"].img.get_center(), color=VERDE_OK, line_length=0.2), run_time=0.5)
        F2 = E["F2"]
        lista = VGroup()
        pr = None
        for k, (a, b, txt) in enumerate((("2", "4", "2 – 4 : OL  ✓"), ("4", "6", "4 – 6 : OL  ✓"), ("2", "6", "2 – 6 : OL  ✓"))):
            self.en("entre", 0.2)
            nuevo = sondas(F2.p(a), F2.p(b) + RIGHT * 0.001)
            ln = nota(txt, VERDE_OK, 2.55 - 0.45 * k)
            lista.add(ln)
            if pr is None:
                self.play(Create(nuevo), run_time=0.8)
            else:
                self.play(Transform(pr, nuevo), run_time=0.6)
                nuevo = pr
            pr = nuevo
            self.play(FadeIn(ln, shift=RIGHT * 0.1), run_time=0.3)
        self.en("tierra", 0.2)
        pe = E["X0"].p("5_a")
        for k, a in enumerate(("2", "4", "6")):
            nuevo = sondas(F2.p(a), pe)
            self.play(Transform(pr, nuevo), run_time=0.45)
            self.wait(0.15)
        ln = nota("2 · 4 · 6 – PE : OL  ✓", VERDE_OK, 1.2)
        self.play(FadeIn(ln, shift=RIGHT * 0.1), run_time=0.3)
        lista.add(ln)
        self.en("corto", 0.2)
        mal = nota("si suena: hay corto → NO se energiza", ROJO, 0.75)
        self.play(FadeIn(mal), run_time=0.4)
        self.cerrar_voz(0.2)
        self.play(FadeOut(pr), FadeOut(lista), FadeOut(mal), run_time=0.4)
        # ---- mando en frío (ohmios)
        self.voz("mando_frio_5")
        mo_ = pantalla("MM")
        self.play(FadeIn(mo_), run_time=0.3)
        self.remove(mm)
        mm.img.move_to(mo_.img)
        self.en("hilo")
        pr = sondas(E["F3"].p("96"), E["X0"].p("4_a"))
        self.play(Create(pr), run_time=0.9)
        self.en("pulsar")
        s1 = E["S1b"]
        p1 = VGroup(self.aro(s1.img.get_center(), "#12B76A", 0.55), T("-S1 pulsado", 16, "#067647", "HEAVY").next_to(s1.img, DOWN, buff=0.75))
        mr = pantalla("MMr")
        l1 = nota("ARRANQUE pulsado → resistencia de la bobina", VERDE_OK, 2.55)
        self.play(FadeIn(p1), FadeIn(mr), FadeIn(l1), run_time=0.5)
        self.en("paro")
        s0 = E["S0b"]
        p0 = VGroup(self.aro(s0.img.get_center(), ROJO, 0.55), T("-S0 pulsado", 16, "#B42318", "HEAVY").next_to(s0.img, DOWN, buff=0.75))
        l2 = nota("+ PARO pulsado → OL (abierto)", ROJO, 2.1)
        self.play(FadeIn(p0), FadeOut(mr), FadeIn(l2), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(FadeOut(VGroup(pr, p1, p0, l1, l2, sin)), FadeOut(mo_), run_time=0.4)
        # ---- energía: tensión en -X0
        self.voz("tension_5")
        mm = Eq3("MM", 0.024).move_to([-5.3, -1.75, 0])
        self.en("llega")
        X0 = E["X0"]
        rayo = VGroup(*[Line(X0.p(f"{i}_b") + DOWN * 1.4, X0.p(f"{i}_b") + DOWN * 0.3).set_stroke("#F79009", 6, 0.8) for i in (1, 2, 3, 4)])
        self.play(LaggedStart(*[ShowPassingFlash(r.copy(), time_width=0.5) for r in rayo], lag_ratio=0.1), FadeIn(mm), run_time=0.8)
        self.en("medimos")
        pr = sondas(X0.p("1_b"), X0.p("2_b"))
        self.play(Create(pr), run_time=0.8)
        m208 = pantalla("MMv208")
        v = nota("L1-L2 = L2-L3 = L1-L3 = 208 V", AMB, 2.55)
        self.play(FadeIn(m208), FadeIn(v), run_time=0.4)
        self.en("120")
        pr2 = sondas(X0.p("1_b"), X0.p("4_b"))
        v2 = nota("L-N = 120 V", AMB, 2.1)
        m120 = pantalla("MMv120")
        self.play(Transform(pr, pr2), FadeIn(v2), FadeIn(m120), FadeOut(m208), run_time=0.6)
        self.cerrar_voz(0.2)
        self.play(FadeOut(pr), FadeOut(v), FadeOut(v2), FadeOut(mm), FadeOut(m120), run_time=0.4)
        # ---- marcha
        self.voz("marcha")
        self.en("cerramos")
        self.sfx("breaker", -6)
        E["F1"] = self.cambiar(E["F1"], "F1on")
        self.en("enciende")
        E["H2b"] = self.cambiar(E["H2b"], "H2bon")
        self.play(Flash(E["H2b"].img.get_center(), color="#FF3B30", line_length=0.2), run_time=0.4)
        self.en("pulsamos")
        p1 = VGroup(self.aro(E["S1b"].img.get_center(), "#12B76A", 0.55), T("-S1 pulsado", 16, "#067647", "HEAVY").next_to(E["S1b"].img, DOWN, buff=0.75))
        self.play(FadeIn(p1), run_time=0.3)
        self.en("contactor")
        self.sfx("contactor", -6)
        E["KM1"] = self.cambiar(E["KM1"], "KM1on")
        self.play(FadeOut(p1), run_time=0.3)
        self.en("enciende")
        E["H1b"] = self.cambiar(E["H1b"], "H1bon")
        E["H2b"] = self.cambiar(E["H2b"], "H2b")
        self.play(Flash(E["H1b"].img.get_center(), color="#39E15A", line_length=0.2), run_time=0.4)
        self.en("motor")
        self.sfx("motor", -8)
        eje = eje_girando(mo, 16.0)
        self.add(eje)
        self.cerrar_voz(0.1)
        # ---- P9/P10 · corriente en la caja del motor: UN solo conductor
        self.voz("corriente_5")
        self.en("motor", 0.2)
        caja = mo.mm(146, 70)
        self.zoom(caja, 3.2, 0.9)
        self.en("abrimos", 0.1)
        velo = Rectangle(width=16.5, height=9.5, stroke_width=0).set_fill("#E4E7EB", 0.95).set_z_index(30)
        cb = Eq3("CB", 0.036).move_to([1.8, -0.5, 0]).set_z_index(31)
        cb_n = VGroup(Paragraph("Caja de conexiones", "de -M1 (abierta)", font=SANS, font_size=26, weight="HEAVY", color=TXT, line_spacing=0.7)).next_to(cb, LEFT, buff=0.6).shift(UP * 2.0).set_z_index(31)
        colas = self.colas_caja(cb, z=32)
        puentes = VGroup(*[Line(cb.p(a), cb.p(b)).set_stroke(MARCA_D, 14, opacity=0.5) for a, b in (("T1", "T7"), ("T2", "T8"), ("T3", "T9"), ("T4", "T6"))]).set_z_index(33)
        self.zoom_fuera(0.01)
        self.play(FadeIn(velo), FadeIn(cb), FadeIn(cb_n), FadeIn(colas), FadeIn(puentes), run_time=0.7)
        x_t1 = cb.p("T1")[0]
        top = cb.img.get_top()[1] + 0.9
        jaw = np.array([x_t1, top - 0.75, 0])
        pz = Eq3("PZ", 0.0125)
        H_, W_ = pz.img.height, pz.img.width
        pz.img.move_to(jaw + DOWN * (0.29 * H_) + LEFT * (0.007 * W_))
        pz.set_z_index(36)
        self.en("pinza", 0.2)
        self.play(FadeIn(pz, shift=UP * 0.3), run_time=0.7)
        resal = Line(jaw + DOWN * 0.45, jaw + UP * 0.45).set_stroke(MARCA_D, 22, opacity=0.5).set_z_index(35)
        ok1 = etiqueta("UN SOLO conductor (T1) dentro de la mordaza", VERDE_OK, 24).scale(0.8).next_to(cb, LEFT, buff=0.35).shift(UP * 0.3).set_z_index(37)
        self.play(Create(resal), FadeIn(ok1), run_time=0.6)
        self.en("manguera", 0.2)
        # forma INCORRECTA: abrazar toda la manguera → casi cero
        jac_c = np.array([(cb.p("T1")[0] + cb.p("T3")[0]) / 2, top + 0.7, 0])
        fantasma = Eq3("PZ", 0.0125)
        fantasma.img.move_to(jac_c + DOWN * (0.29 * H_) + LEFT * (0.007 * W_) + RIGHT * 3.4).set_opacity(0.0)
        malo = VGroup(Circle(radius=0.38, color=ROJO, stroke_width=6).move_to(jac_c),
                      Cross(scale_factor=0.2, stroke_color=ROJO, stroke_width=8).move_to(jac_c + RIGHT * 0.62 + UP * 0.25),
                      etiqueta("toda la manguera → ≈ 0 A", ROJO, 24).scale(0.7).next_to(jac_c, RIGHT, buff=0.9)).set_z_index(37)
        self.play(FadeIn(malo), run_time=0.5)
        self.en("corriente", 0.2)
        ok = etiqueta("corriente de trabajo < 26,5 A de placa  ✓", VERDE_OK, 24).scale(0.8).next_to(ok1, DOWN, buff=0.2).set_z_index(37)
        self.play(FadeIn(ok), FadeOut(malo), run_time=0.5)
        self.cerrar_voz(0.3)
        self.play(*[FadeOut(m) for m in (velo, cb, cb_n, colas, puentes, pz, resal, ok1, ok)], run_time=0.5)
        # ---- disparo del térmico
        self.voz("disparo")
        F3 = E["F3"]
        self.en("test")
        self.zoom(F3.img.get_center(), 2.6, 0.5)
        self.sfx("disparo", -4)
        E["F3"] = self.cambiar(E["F3"], "F3tr")
        self.play(Flash(E["F3"].img.get_center() + LEFT * 0.2, color=ROJO, line_length=0.15), run_time=0.4)
        self.en("abre")
        self.zoom_fuera(0.5)
        self.en("cae")
        self.sfx("motor_para", -8)
        eje.clear_updaters()
        self.remove(eje)
        E["KM1"] = self.cambiar(E["KM1"], "KM1")
        E["H1b"] = self.cambiar(E["H1b"], "H1b")
        E["H2b"] = self.cambiar(E["H2b"], "H2bon")
        self.en("aunque")
        p1 = VGroup(self.aro(E["S1b"].img.get_center(), "#12B76A", 0.55), T("-S1 pulsado", 16, "#067647", "HEAVY").next_to(E["S1b"].img, DOWN, buff=0.75))
        no = nota("ARRANQUE pulsado → no arranca", ROJO, 3.05)
        self.play(FadeIn(no), FadeIn(p1), run_time=0.4)
        self.play(FadeOut(p1), run_time=0.3)
        self.en("reset")
        E["F3"] = self.cambiar(E["F3"], "F3")
        rs = nota("RESET → listo para arrancar", "#2563EB", 3.05)
        self.sfx("tic", -6)
        self.play(FadeTransform(no, rs), run_time=0.5)
        self.cerrar_voz(0.3)
        self.salir()

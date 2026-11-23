"""H01 v3 · Arranque directo · Trituradora de piedrín — Correcciones_V7 del usuario (22-nov).
- Fondo GRIS CLARO con cuadrícula gris suave (TEMA=gris); textos y cuadros con contraste.
- Lo que se ve coincide con lo que se dice: cada evento se ancla a la palabra (alineación faster-whisper en alin_h01v2/).
- Diagramas recreados PIXEL POR PIXEL del original del usuario, en un solo color (diag_lit.py).
- Conexión didáctica sin plancha (h01v3_lay.py): punteras que entran bajo el plástico del borne, cables sin borde.
- Puesta en marcha en el mismo esquema de conexión (antes del tablero).
- Tablero real 400 × 300 × 200 mm con canaleta ranurada 40 × 60 mm y riel DIN 35 mm (estilo de la referencia del usuario).
Render: FORMATO=h TEMA=gris VOZ=eleven manim -qh --disable_caching -o h01v3 h01v3.py H01v3"""
import json
import os
import re
import unicodedata
os.environ.setdefault("TEMA", "gris")
import h01_arranque as _H
import h01v2 as _V2
OSC, OSC2 = "#141821", "#475467"
for _m in (_H, _V2):
    _m.TXT, _m.TXT2 = OSC, OSC2
_V2.AMB = "#E8590C"
from h01v2 import *                                          # noqa: F401,F403
from h01v2 import H01v2, eje_girando
from h01_guion import GUION as G3, MATERIALES
from h01v3_lay import (Eq3, Cable3, disposicion, hilos_mando, hilos_potencia, riel_din, puerta_marco, ruta_redondeada,
                       K, KD, KF, ROJO_M, NEUTRO_C, NEGRO_P, PE_V, PE_A, ENTRADAS, DIRS, puntera)
from diag_lit import diagrama_mando, diagrama_potencia
from h01v2_diag import HILOS_MANDO, HILOS_POT

TXT, TXT2, AMB = OSC, OSC2, "#E8590C"
MARCA_D = "#F79009"          # resaltado sobre el diagrama
ORDEN = ["gancho", "pregunta", "problema", "materiales", "mando", "potencia", "c_mando", "c_potencia", "marcha", "cierre"]   # sin tablero (V8 p.11)
TITULOS = ["El dato curioso", "La pregunta técnica", "El problema real", "Lista de materiales", "Diagrama de mando IEC",
           "Diagrama de potencia IEC", "Conexión del mando", "Conexión de potencia", "Puesta en marcha", "Cierre"]


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def tabla_clara(filas, anchos, x0, y0, alto=0.5, size=17, encabezado=None):
    g = VGroup()
    y = y0
    if encabezado:
        x = x0
        fila = VGroup()
        for t, w in zip(encabezado, anchos):
            fila.add(Rectangle(width=w, height=alto + 0.04, stroke_width=1.2, stroke_color="#98A2B3").set_fill("#0E7490", 1).move_to([x + w / 2, y - (alto + 0.04) / 2, 0]))
            fila.add(Text(t, font=SANS, font_size=size + 1, weight="HEAVY", color="#FFFFFF").move_to([x + w / 2, y - (alto + 0.04) / 2, 0]))
            x += w
        g.add(fila)
        y -= alto + 0.04
    for i, f in enumerate(filas):
        lineas = max(len(str(c).split("\n")) for c in f)
        h = alto * (1 + 0.75 * (lineas - 1))
        x = x0
        fila = VGroup()
        for j, (t, w) in enumerate(zip(f, anchos)):
            fila.add(Rectangle(width=w, height=h, stroke_width=1.2, stroke_color="#98A2B3").set_fill("#FFFFFF" if i % 2 == 0 else "#F2F4F7", 1).move_to([x + w / 2, y - h / 2, 0]))
            if t:
                tt = Paragraph(*str(t).split("\n"), font=SANS, font_size=size, color=OSC, line_spacing=0.6, weight="BOLD" if j == 1 else "NORMAL")
                if tt.width > w - 0.14:
                    tt.scale_to_fit_width(w - 0.14)
                tt.move_to([x + 0.08 + tt.width / 2 if j > 0 else x + w / 2, y - h / 2, 0])
                fila.add(tt)
            x += w
        g.add(fila)
        y -= h
    return g


class H01v3(H01v2):
    CARPETA_VOZ = "voz_h01v2"
    GUION = G3
    SECC = {k: (str(i + 1), t) for i, (k, t) in enumerate(zip(ORDEN, TITULOS))}

    def construct(self):
        self.cinta_act = None
        self.paso_act = None
        self.nota_act = None
        solo = os.environ.get("SOLO")
        for paso in ORDEN:
            if solo and paso not in solo.split(","):
                continue
            getattr(self, "h_" + paso)()

    # ------------------------------------------------------------------ voz anclada a palabras
    def voz(self, clave):
        self.ini_voz = self.renderer.time
        self.clave_voz = clave
        ruta = DIR / "alin_h01v2" / f"{clave}.json"
        self.palabras = json.loads(ruta.read_text()) if ruta.exists() else []
        self.cursor = 0
        return super().voz(clave)

    def t(self, palabra, despues=True):
        """Tiempo absoluto de la siguiente palabra que coincide (busca hacia adelante desde el cursor)."""
        objetivo = _norm(palabra)
        for i in range(self.cursor, len(self.palabras)):
            if _norm(self.palabras[i][2]).startswith(objetivo):
                if despues:
                    self.cursor = i + 1
                return self.ini_voz + self.palabras[i][0]
        return None

    def en(self, palabra, antes=0.15):
        tt = self.t(palabra)
        if tt is not None:
            self.hasta(tt - antes)

    # ------------------------------------------------------------------ portadilla clara
    def portadilla(self, clave):
        num, titulo = self.SECC[clave]
        sale = [m for m in (self.cinta_act, self.paso_act) if m is not None]
        fondo = Rectangle(width=16.2, height=9.2, stroke_width=0).set_fill("#F4F5F7", 0.97).set_z_index(40)
        grande = T(num if len(num) > 1 else f"0{num}", 300, MARCA, "HEAVY").set_opacity(0.16).move_to([4.6, -0.2, 0]).set_z_index(41)
        sec = T(f"SECCIÓN {num}", 30, AMB, "HEAVY")
        tit = T(titulo, 70, OSC, "HEAVY")
        if tit.width > 13.0:
            tit.scale_to_fit_width(13.0)
        VGroup(sec, tit).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 0.2, 0])
        barra = RoundedRectangle(width=tit.width, height=0.14, corner_radius=0.07, stroke_width=0).set_fill(MARCA, 1).next_to(tit, DOWN, buff=0.3, aligned_edge=LEFT)
        cursor = Rectangle(width=0.07, height=tit.height * 0.95, stroke_width=0).set_fill(MARCA, 1)
        for m_ in (sec, tit, barra, cursor):
            m_.set_z_index(42)
        self.play(FadeIn(fondo), FadeIn(grande, scale=1.1), FadeIn(sec, shift=RIGHT * 0.2), *[FadeOut(m) for m in sale], run_time=0.45)
        self.cinta_act = None
        self.paso_act = None
        n = len(tit.submobjects)
        dt = 0.05
        wav = DIR / "sfx" / f"tecleo_{n}.wav"
        if not wav.exists():
            sonido_tecleo(wav, n, dt, semilla=n)
        self.add_sound(str(wav), gain=-9)
        cursor.next_to(tit[0], LEFT, buff=0.05)
        self.add(cursor)
        letras = list(tit.submobjects)
        for m in letras:
            m.set_opacity(0)
        self.add(tit)

        def revelar(mob, alpha):
            k = int(alpha * n + 1e-6)
            for i, m in enumerate(letras):
                m.set_opacity(1 if i < k else 0)
            if k > 0:
                ultimo = letras[max(0, min(k, n) - 1)]
                cursor.move_to([ultimo.get_right()[0] + 0.08, tit.get_center()[1], 0])
        self.play(UpdateFromAlphaFunc(tit, revelar), run_time=n * dt, rate_func=linear)
        self.play(GrowFromEdge(barra, LEFT), run_time=0.35)
        self.wait(0.35)
        ci = cinta(num, titulo)
        self.play(FadeOut(VGroup(fondo, grande, sec, tit, barra, cursor)), FadeIn(ci, shift=RIGHT * 0.3), run_time=0.45)
        self.cinta_act = ci

    def cambiar(self, viejo, nombre, k=None):
        n = Eq3(nombre, k or viejo.k, base=viejo.base)
        n.img.scale_to_fit_height(viejo.img.height).move_to(viejo.img)
        n.k = viejo.k
        n.set_z_index(viejo.z_index)
        self.remove(viejo)
        self.add(n)
        return n

    def dibujar_parte(self, H, key, rt=1.3):
        g = H.partes[key]
        dib = [m for m in g if getattr(m, "tipo", "") == "dibujo"]
        txt = [m for m in g if getattr(m, "tipo", "") != "dibujo"]
        self.add_sound(str(DIR / "sfx" / "tecleo_16.wav"), gain=-17)
        if dib:
            self.play(*[DrawBorderThenFill(m, stroke_width=1.5, stroke_color=BLACK) for m in dib], run_time=rt)
        if txt:
            self.play(LaggedStart(*[Write(m) for m in txt], lag_ratio=0.04), run_time=0.6)

    def nota(self, texto, pos):
        n = etiqueta(texto, "#0E7490", 26).move_to(pos)
        if n.width > 5.6:
            n.scale_to_fit_width(5.6)
        anims = [FadeIn(n, shift=UP * 0.15)]
        if self.nota_act is not None:
            anims.append(FadeOut(self.nota_act, shift=UP * 0.15))
        self.play(*anims, run_time=0.35)
        self.nota_act = n

    # =============================================================== 1 · GANCHO
    def h_gancho(self):
        self.voz("gancho")
        mo = Eq3("M1", 0.030).move_to([-3.2, -0.4, 0])
        self.play(FadeIn(mo, shift=UP * 0.3), run_time=0.8)
        eje = eje_girando(mo)
        self.add(eje)
        self.sfx("motor", -12)
        self.en("26")
        a = VGroup(T("CORRIENTE NORMAL", 24, TXT2, "BOLD"), T("26,5 A", 84, TXT, "HEAVY")).arrange(DOWN, buff=0.12).move_to([4.6, 2.2, 0])
        self.play(FadeIn(a, shift=LEFT * 0.3), run_time=0.5)
        self.en("170")
        b = VGroup(T("AL ARRANCAR", 24, TXT2, "BOLD"), T("178 A", 96, ROJO, "HEAVY"), T("≈ 7 veces · NEC T430.251(B), diseño B", 20, TXT2, "MEDIUM")).arrange(DOWN, buff=0.12).move_to([4.6, -0.6, 0])
        self.sfx("pop", -10)
        self.play(FadeIn(b, scale=1.15), run_time=0.5)
        self.en("como")
        q = T("¿Cómo lo protegemos sin que el breaker se dispare?", 36, AMB, "HEAVY").move_to([0, -3.55, 0])
        if q.width > 15:
            q.scale_to_fit_width(15)
        self.play(Write(q), run_time=1.2)
        self.cerrar_voz(0.2)
        self.voz("gancho2")
        self.play(FadeOut(a), FadeOut(b), run_time=0.3)
        for pal, s in (("calculamos", "CÁLCULO"), ("mando", "MANDO"), ("potencia", "POTENCIA"), ("conectamos", "CONEXIÓN"), ("marcha", "MARCHA")):
            self.en(pal, 0.2)
            p = pastilla(s, MARCA, 26, True)
            p.move_to([-5.2 + 2.6 * ["CÁLCULO", "MANDO", "POTENCIA", "CONEXIÓN", "MARCHA"].index(s), 3.5, 0])
            self.sfx("pop", -16)
            self.play(FadeIn(p, shift=DOWN * 0.2), run_time=0.3)
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
        self.en("motor")
        self.play(FadeIn(a, shift=RIGHT * 0.3), run_time=0.5)
        self.en("breaker")
        self.play(FadeIn(b, shift=LEFT * 0.3), run_time=0.5)
        self.en("80")
        self.sfx("pop", -10)
        self.play(FadeIn(q, scale=1.4), run_time=0.4)
        self.en("cortar")
        c1 = etiqueta("BREAKER  →  corta el CORTOCIRCUITO y protege el CABLE", AMB, 28).move_to([0, -2.0, 0])
        self.play(FadeOut(q), FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        self.en("rele")
        c2 = etiqueta("RELÉ TÉRMICO  →  protege al MOTOR de la SOBRECARGA", "#7A5AF8", 28).move_to([0, -3.1, 0])
        self.sfx("pop", -10)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== 3 · PROBLEMA REAL
    def h_problema(self):
        self.seccion("problema")
        self.voz("placa")
        mo = Eq3("M1", 0.030).move_to([0, -0.3, 0])
        self.play(FadeIn(mo), run_time=0.6)
        self.zoom(mo.mm(169, 133), 4.6, 1.0)

        def caja(x0, x1, fila, color):
            y = 392 + 18.5 * fila
            p0, p1 = mo.mm(x0 * 0.3, (y - 9) * 0.3), mo.mm(x1 * 0.3, (y + 9) * 0.3)
            return Rectangle(width=abs(p1[0] - p0[0]), height=abs(p1[1] - p0[1]), stroke_color=color, stroke_width=4).move_to((p0 + p1) / 2)
        cajas = []
        for pal, args in (("10", (444, 494, 0, AMB)), ("tension", (444, 548, 1, MARCA)), ("corriente", (444, 548, 2, ROJO)), ("factor", (545, 618, 3, VERDE_OK))):
            self.en(pal, 0.25)
            c = caja(*args)
            cajas.append(c)
            self.sfx("tic", -12)
            self.play(Create(c), run_time=0.4)
        self.en("red", 0.4)
        self.zoom_fuera(0.7)
        red = etiqueta("RED: 208Y/120 V · 3~ · 60 Hz", MARCA, 30).move_to([0, -3.7, 0])
        self.play(FadeIn(red, shift=UP * 0.2), run_time=0.5)
        self.cerrar_voz(0.2)
        self.play(FadeOut(VGroup(*cajas)), mo.animate.scale(0.42).move_to([-5.6, 2.6, 0]), red.animate.scale(0.6).move_to([-5.6, 1.35, 0]), run_time=0.8)
        tarjetas = [
            ("tabla", "NEC T430.250", ["10 hp · 208 V · trifásico"], "I tabla = 30,8 A", MARCA, [-0.3, 2.4, 0]),
            ("cable", "NEC 430.22", ["125 % × 30,8 = 38,5 A", "10 AWG no alcanza (35 A)"], "8 AWG THHN 75 °C", VERDE_OK, [5.0, 2.4, 0]),
            ("breaker", "NEC T430.52", ["250 % × 30,8 = 77 A", "→ siguiente estándar"], "-F2 · 3P · C80", AMB, [-5.3, -0.4, 0]),
            ("termico", "NEC 430.32(A)(1)", ["F.S. 1,25 → máx 125 % = 33,1 A", "rango 23–32 A"], "-F3 ajuste 26,5 A", "#7A5AF8", [0.0, -0.4, 0]),
            ("contactor", "AC-3 a 208 V (UL)", ["32 A → 7,5 hp  ✗   38 A → 10 hp  ✓", "bobina 120 VAC"], "-KM1 · 38 A", "#0E7490", [5.3, -0.4, 0]),
            ("mando_prot", "Mando 120 VAC (L-N)", ["breaker 1 polo, curva C", "cable 14 AWG"], "-F1 · 1P · C2", "#2563EB", [0.0, -2.95, 0]),
        ]
        for clave, norma, lineas, res, col, pos in tarjetas:
            self.voz(clave)
            tj = self.tarjeta_calc(norma, lineas, res, col, pos)
            tj[0].set_stroke(col, 2.5)
            if clave == "mando_prot":
                tj.scale(0.85)
            self.escribir(tj)
            self.cerrar_voz(0.1)
        self.wait(0.6)
        self.salir()

    # =============================================================== 4 · MATERIALES (cada fila cuando se nombra)
    def h_materiales(self):
        self.seccion("materiales")
        self.voz("materiales")
        anchos = [1.25, 3.0, 7.6, 3.4]
        x0 = -sum(anchos) / 2
        anclas = ["motor", "F2", "F1", "KM1", "F3", "S0", "S1", "H1", "H2", "6", "azul",
                  "2", "separador", "negro", "rojo", "claro", "verde", "tierra", "rieldin", "canaleta", "gabinete"]
        paginas = [MATERIALES[:11], MATERIALES[11:]]
        idx = 0
        for pg, filas in enumerate(paginas):
            tb = tabla_clara(filas, anchos, x0, 3.55, 0.5, 17, ["Cantidad", "Nombre", "Características", "Observación"])
            if pg == 0:
                self.play(FadeIn(tb[0]), run_time=0.4)
            for k, fila in enumerate(tb[1:]):
                self.en(anclas[idx], 0.2)
                if pg == 1 and k == 0:
                    self.play(FadeOut(self.tb_ant[1:]), FadeIn(tb[0]), FadeOut(self.tb_ant[0]), run_time=0.35)
                self.sfx("pop", -18)
                self.play(FadeIn(fila, shift=UP * 0.1), run_time=0.3)
                idx += 1
            self.tb_ant = tb
        self.cerrar_voz(0.4)
        self.wait(1.2)
        self.salir()

    # =============================================================== 5 · DIAGRAMA DE MANDO
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
            self.dibujar_parte(H, f"m{i}", 1.3)
            self.cerrar_voz(0.05)
        self.play(FadeOut(self.nota_act), run_time=0.3)
        self.nota_act = None
        self.voz("retencion")
        h2 = Circle(radius=14.5 * H.s).move_to(H.P(317, 591)).set_fill("#FF3B30", 0.8).set_stroke(width=0)
        rama_off = VGroup(H.marca([(47, 51), (137, 51), (137, 186), (317, 186), (317, 576)]), H.marca([(317, 606), (317, 651)], "#2F80ED"))
        self.en("luz")
        self.play(Create(rama_off), FadeIn(h2), run_time=0.8)
        self.en("pulsas")
        pulso = Circle(radius=0.16, color=AMB, stroke_width=5).move_to(H.P(112, 441))
        self.play(Create(pulso), run_time=0.3)
        self.en("bobina")
        marcha = VGroup(H.marca([(137, 186), (137, 571)]), H.marca([(137, 611), (137, 651)], "#2F80ED"))
        bob = Rectangle(width=40 * H.s, height=20 * H.s).move_to(H.P(137, 591)).set_fill(MARCA_D, 0.7).set_stroke(width=0)
        self.sfx("contactor", -10)
        self.play(Create(marcha), FadeIn(bob), run_time=0.7)
        self.en("13")
        cierra_13 = Line(H.P(227, 425), H.P(227, 457)).set_stroke(MARCA_D, 6)
        reten = VGroup(H.marca([(137, 381), (227, 381), (227, 576)]), H.marca([(227, 606), (227, 651)], "#2F80ED"), cierra_13)
        self.play(Create(reten), run_time=0.6)
        self.en("verde")
        h1 = Circle(radius=14.5 * H.s).move_to(H.P(227, 591)).set_fill("#39E15A", 0.85).set_stroke(width=0)
        self.play(FadeIn(h1), run_time=0.4)
        self.en("roja")
        abre = Cross(scale_factor=0.12, stroke_color="#E5484D", stroke_width=5).move_to(H.P(325, 441))
        self.play(FadeOut(h2), FadeOut(rama_off), Create(abre), run_time=0.6)
        self.en("sueltas")
        sigue = VGroup(H.marca([(137, 186), (137, 381)]), H.marca([(137, 516), (137, 571)]), H.marca([(227, 470), (227, 516), (137, 516)]))
        self.play(FadeOut(pulso), FadeOut(marcha[0]), Create(sigue), run_time=0.7)
        self.en("pulsas")
        p0 = Circle(radius=0.16, color=ROJO, stroke_width=5).move_to(H.P(112, 337))
        self.play(Create(p0), run_time=0.3)
        self.en("cae")
        self.sfx("contactor", -14)
        rama_off2 = VGroup(H.marca([(47, 51), (137, 51), (137, 186), (317, 186), (317, 576)]), H.marca([(317, 606), (317, 651)], "#2F80ED"))
        self.play(FadeOut(VGroup(sigue, reten, bob, h1, marcha[1], abre, p0)), FadeIn(h2), Create(rama_off2), run_time=0.8)
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

    # =============================================================== 7 · CONEXIÓN DEL MANDO (didáctica, sin plancha)
    def montar(self):
        E = disposicion()
        fondo = Group(riel_din(E), puerta_marco(E))
        return E, fondo

    def tender(self, cables, marcas, rt=1.5):
        self.marcas = getattr(self, "marcas", [])
        self.marcas += marcas
        self.play(*[Create(c.conductor) for c in cables], *[Create(m) for m in marcas], run_time=rt)
        self.sfx("tornillo", -10)
        self.play(*[FadeIn(c.puntas) for c in cables], run_time=0.3)

    def lupa(self, punto, ancho=1.7, espera=0.6):
        fr = self.camera.frame
        c0, w0 = fr.get_center().copy(), fr.width
        self.play(fr.animate.set(width=ancho).move_to(punto), run_time=0.5)
        self.wait(espera)
        self.play(fr.animate.set(width=w0).move_to(c0), run_time=0.45)

    ANCLAS_MANDO = {"c2": [None, "puente"], "c4": [None, "regreso"], "c5": [None, "a1", "x1"], "c7": ["del", "puerta", "roja"]}

    def h_c_mando(self):
        self.seccion("c_mando")
        self.voz("c_intro")
        E, fondo = self.montar()
        H = diagrama_mando(alto=7.9, centro=(-4.75, -0.25))
        self.play(FadeIn(fondo), FadeIn(H.todo()), *[FadeIn(e) for e in E.values()], run_time=1.2)
        self.cerrar_voz(0.1)
        self.cables = Group()
        for clave, cs, marcas in hilos_mando(E):
            self.voz(clave)
            anclas = self.ANCLAS_MANDO.get(clave, [None] * len(cs))
            ms_todas = [H.marca(tr) for key in marcas for tr in HILOS_MANDO[key]]
            for i, c in enumerate(cs):
                if anclas[i]:
                    self.en(anclas[i], 0.3)
                ms = ms_todas if i == 0 else []
                self.tender([c], ms, 1.4)
                self.cables.add(c)
            self.cerrar_voz(0.05)
            for m in ms_todas:
                m.set_stroke(opacity=0.35)
        self.wait(0.4)
        self.E, self.fondo_tab = E, fondo
        self.play(FadeOut(H.todo()), *[FadeOut(m) for m in self.marcas], run_time=0.4)
        self.marcas = []

    # =============================================================== 8 · CONEXIÓN DE POTENCIA + motor
    def asegurar_mando(self):
        if not hasattr(self, "E"):
            E, fondo = self.montar()
            self.E, self.fondo_tab = E, fondo
            self.cables = Group(*[c for _, cs, _ in hilos_mando(E) for c in cs])
            self.add(fondo, *E.values(), self.cables)

    def motor_en_esquema(self):
        """Motor abajo a la derecha, cableado desde -X1 (lado de campo) a su caja: T1 T2 T3 y PE por separado."""
        E = self.E
        mo = Eq3("M1", 0.0118)
        mo.img.move_to([6.0, -2.55, 0])
        cj = mo.mm(146, 56)
        cab = VGroup()
        xs = []
        for i, (b, col) in enumerate((("1_b", NEGRO_P), ("2_b", NEGRO_P), ("3_b", NEGRO_P), ("4_b", PE_V))):
            (A, d) = E["X1"].boca(b)
            xv = 3.10 if i == 0 else 3.55 + 0.13 * (i - 1)      # T1 va SEPARADO: ahí se coloca la pinza
            yb = -4.22 + 0.0 * i - 0.07 * (3 - i)
            yt = cj[1] + 0.22 + 0.08 * (3 - i)
            pu, lp = puntera(A, d, "pot", K)
            m = ruta_redondeada([A + d * lp, [A[0], yb, 0], [xv, yb, 0], [xv, yt, 0], [cj[0] - 0.12 + 0.08 * i, yt, 0], [cj[0] - 0.12 + 0.08 * i, cj[1], 0]], 0.15)
            m.set_stroke(col, 7).set_fill(opacity=0)
            g = VGroup(fisico(m))
            if col == PE_V:
                g.add(fisico(DashedVMobject(m.copy(), num_dashes=60, dashed_ratio=0.5).set_stroke(PE_A, 7)))
            cab.add(VGroup(g, pu))
            xs.append(xv)
        self.x_t1 = xs[0]
        self.y_t1 = -3.05
        return mo, cab

    ANCLAS_POT = {"p1": None, "p2": None}

    def h_c_potencia(self):
        self.asegurar_mando()
        E = self.E
        self.seccion("c_potencia")
        self.voz("p_intro")
        H = diagrama_potencia(alto=7.9, centro=(-4.75, -0.25))
        self.play(FadeIn(H.todo()), *[c.animate.set_opacity(0.3) for c in self.cables], run_time=0.8)
        X0 = E["X0"]
        red = VGroup()
        for b, col in (("1_b", NEGRO_P), ("2_b", NEGRO_P), ("3_b", NEGRO_P), ("4_b", NEUTRO_C), ("5_b", PE_V)):
            A, d = X0.boca(b)
            pu, lp = puntera(A, d, "pot", K)
            ln = Line(A + d * lp, [A[0], -4.6, 0]).set_stroke(col, 7)
            g = VGroup(fisico(ln), pu)
            if col == PE_V:
                g.add(fisico(DashedLine(A + d * lp, [A[0], -4.6, 0], dash_length=0.05).set_stroke(PE_A, 7)))
            red.add(g)
        lred = T("Red 208Y/120 V", 16, TXT2, "BOLD").next_to(X0.img, LEFT, buff=0.05).shift(DOWN * 0.55)
        self.play(FadeIn(red), FadeIn(lred), run_time=0.5)
        self.cerrar_voz(0.1)
        P = hilos_potencia(E)
        self.cab_pot = Group()

        def tanda(clave, cables, marcas, anclas=None):
            self.voz(clave)
            if anclas:
                grupos = anclas
            else:
                grupos = [(None, cables, marcas)]
            for ancla, cs, mk in grupos:
                if ancla:
                    self.en(ancla, 0.3)
                ms = [H.marca(tr) for key in mk for tr in HILOS_POT[key]]
                self.tender(cs, ms, 1.8)
                self.cab_pot.add(*cs)
            self.cerrar_voz(0.05)
        tanda("p1", P["p1"], ["p1"])
        tanda("p2", P["p2"], ["p2"])
        self.voz("p3")
        F3, KM1 = E["F3"], E["KM1"]
        ms = [H.marca(tr) for tr in HILOS_POT["p3"]]
        self.play(F3.animate.shift(DOWN * 0.35), run_time=0.4)
        self.play(F3.animate.shift(UP * 0.35), *[Create(m) for m in ms], run_time=0.9)
        self.marcas += ms
        self.sfx("tornillo", -8)
        anillos = VGroup(*[Circle(radius=0.10, color=AMB, stroke_width=5).move_to(KM1.p(t)) for t in ("2/T1", "4/T2", "6/T3")])
        self.play(LaggedStart(*[Create(a) for a in anillos], lag_ratio=0.3), run_time=0.9)
        self.play(FadeOut(anillos), run_time=0.3)
        self.cerrar_voz(0.05)
        tanda("p4", P["p4"] + P["pe"], None, anclas=[(None, P["p4"], ["p4"]), ("tierra", P["pe"], ["pe"])])
        # caja del motor
        self.voz("p5")
        velo = Rectangle(width=16.5, height=9.5, stroke_width=0).set_fill("#E4E7EB", 0.92).set_z_index(30)
        cb = Eq3("CB", 0.040).move_to([1.8, -0.4, 0]).set_z_index(31)
        tit = T("Caja del motor · 9 puntas en estrella · 208 V", 26, TXT, "HEAVY").next_to(cb, UP, buff=0.2).set_z_index(31)
        ms = [H.marca(tr) for tr in HILOS_POT["p5"]]
        self.marcas += ms
        self.play(FadeIn(velo), FadeIn(cb), FadeIn(tit), *[Create(m) for m in ms], run_time=0.8)
        llegan = VGroup()
        for tt_ in ("T1", "T2", "T3"):
            a = cb.p(tt_)
            ln = fisico(Line(a + UP * 1.6, a).set_stroke(NEGRO_P, 10)).set_z_index(32)
            ojo = Circle(radius=0.11).set_stroke("#B87333", 5).set_fill(opacity=0).move_to(a).set_z_index(33)
            llegan.add(VGroup(ln, ojo))
        self.play(LaggedStart(*[Create(l) for l in llegan], lag_ratio=0.2), run_time=0.9)
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
        mo, cab_m = self.motor_en_esquema()
        self.play(FadeIn(mo), Create(cab_m), run_time=1.0)
        self.mo, self.cab_m = mo, cab_m
        # ajuste del dial
        self.voz("p6")
        dial = F3.mm(196 * 45 / 685, 222 * 45 / 685)
        lab = etiqueta("ajuste 26,5 A", AMB, 22).scale(0.55).next_to(dial, LEFT, buff=0.35)
        aro = Circle(radius=0.16, color=AMB, stroke_width=5).move_to(dial)
        self.sfx("tic", -8)
        self.play(FadeIn(lab), Create(aro), run_time=0.7)
        self.cerrar_voz(0.2)
        self.play(FadeOut(lab), FadeOut(aro), run_time=0.3)
        self.play(FadeOut(H.todo()), *[FadeOut(m) for m in self.marcas], *[c.animate.set_opacity(1) for c in self.cables], run_time=0.6)
        self.marcas = []

    # =============================================================== 9 · PUESTA EN MARCHA (en el mismo esquema, antes del tablero)
    def h_marcha(self):
        if not hasattr(self, "mo"):
            self.asegurar_mando()
            P = hilos_potencia(self.E)
            self.cab_pot = Group(*[c for v in P.values() for c in v])
            self.mo, self.cab_m = self.motor_en_esquema()
            self.add(self.cab_pot, self.mo, self.cab_m)
        self.seccion("marcha")
        E, mo = self.E, self.mo
        mm = Eq3("MM", 0.024).move_to([-4.6, -0.6, 0])
        self.voz("prueba_frio")
        self.play(FadeIn(mm, shift=RIGHT * 0.3), run_time=0.5)

        def sondas(a, b):
            ra = cable(mm.p("VΩ"), mm.p("VΩ") + DOWN * 0.5, [mm.p("VΩ")[0] + 0.5, -4.1, 0], [a[0] - 0.4, a[1] - 0.6, 0], a, color=ROJO, w=4, suave=True)
            rb = cable(mm.p("COM"), mm.p("COM") + DOWN * 0.7, [mm.p("COM")[0] + 0.3, -4.35, 0], [b[0] - 0.3, b[1] - 0.6, 0], b, color="#2B2C2E", w=4, suave=True)
            tips = VGroup(Dot(a, radius=0.05, color=ROJO), Dot(b, radius=0.05, color="#2B2C2E"))
            return VGroup(ra, rb, tips)
        self.en("hilo")
        pr = sondas(E["F1"].p("2"), E["X0"].p("4_a"))
        self.play(Create(pr), run_time=1.0)

        def pantalla(nombre):
            nuevo = Eq3(nombre, mm.k)
            nuevo.img.move_to(mm.img)
            return nuevo
        ops = {n: E[n] for n in ("S0", "S1", "H1", "H2")}
        self.en("pulsar")
        s1p = self.cambiar(ops["S1"], "S1p")
        lec = etiqueta("ARRANQUE pulsado → resistencia de la bobina", VERDE_OK, 24).move_to([-4.6, 3.3, 0]).scale(0.8)
        mmr = pantalla("MMr")
        self.play(FadeIn(mmr), FadeIn(lec), run_time=0.5)
        self.en("pulsar")
        ops["S1"] = self.cambiar(s1p, "S1")
        s0p = self.cambiar(ops["S0"], "S0p")
        lec2 = etiqueta("PARO pulsado → OL (circuito abierto)", ROJO, 24).move_to([-4.6, 3.3, 0]).scale(0.8)
        self.play(FadeOut(mmr), FadeTransform(lec, lec2), run_time=0.5)
        self.cerrar_voz(0.1)
        ops["S0"] = self.cambiar(s0p, "S0")
        self.play(FadeOut(pr), FadeOut(lec2), run_time=0.4)
        self.voz("prueba_tension")
        self.en("cerramos")
        self.sfx("breaker", -6)
        E["F2"] = self.cambiar(E["F2"], "F2on")
        self.play(Flash(E["F2"].img.get_center(), color=VERDE_OK, line_length=0.2), run_time=0.4)
        self.en("medimos")
        pr = sondas(E["X0"].p("1_b"), E["X0"].p("2_b"))
        self.play(Create(pr), run_time=0.8)
        v = etiqueta("L1-L2 = L2-L3 = L1-L3 = 208 V", AMB, 24).move_to([-4.6, 3.3, 0]).scale(0.8)
        m208 = pantalla("MMv208")       # selector en V~ y la pantalla en VOLTIOS (V8 p.9)
        self.play(FadeIn(m208), FadeIn(v), run_time=0.4)
        self.en("120")
        pr2 = sondas(E["X0"].p("1_b"), E["X0"].p("4_b"))
        v2 = etiqueta("L-N = 120 V", AMB, 24).move_to([-4.6, 2.7, 0]).scale(0.8)
        m120 = pantalla("MMv120")
        self.play(Transform(pr, pr2), FadeIn(v2), FadeIn(m120), FadeOut(m208), run_time=0.6)
        self.cerrar_voz(0.2)
        self.play(FadeOut(pr), FadeOut(v), FadeOut(v2), FadeOut(mm), FadeOut(m120), run_time=0.4)
        self.voz("marcha")
        self.en("cerramos")
        self.sfx("breaker", -6)
        E["F1"] = self.cambiar(E["F1"], "F1on")
        self.en("enciende")
        ops["H2"] = self.cambiar(ops["H2"], "H2on")
        self.play(Flash(ops["H2"].img.get_center(), color="#FF3B30", line_length=0.2), run_time=0.4)
        self.en("pulsamos")
        s1p = self.cambiar(ops["S1"], "S1p")
        self.en("contactor")
        self.sfx("contactor", -6)
        E["KM1"] = self.cambiar(E["KM1"], "KM1on")
        ops["S1"] = self.cambiar(s1p, "S1")
        self.en("enciende")
        ops["H1"] = self.cambiar(ops["H1"], "H1on")
        ops["H2"] = self.cambiar(ops["H2"], "H2")
        self.play(Flash(ops["H1"].img.get_center(), color="#39E15A", line_length=0.2), run_time=0.4)
        self.en("motor")
        self.sfx("motor", -8)
        eje = eje_girando(mo, 16.0)
        self.add(eje)
        self.cerrar_voz(0.1)
        self.voz("corriente")
        pz = Eq3("PZ", 0.0085)
        H_, W_ = pz.img.height, pz.img.width
        jaw = np.array([self.x_t1, self.y_t1, 0])
        pz.img.move_to(jaw + DOWN * (0.29 * H_) + LEFT * (0.007 * W_))
        pz.set_z_index(8)
        self.en("pinza")
        nota = Paragraph("UN SOLO cable (T1)", "dentro de la mordaza", font=SANS, font_size=17, color=OSC, weight="BOLD").next_to(jaw, LEFT, buff=0.75).scale(0.8)
        resal = Line(jaw + DOWN * 0.55, jaw + UP * 0.55).set_stroke(MARCA_D, 16, opacity=0.55).set_z_index(5)
        self.play(FadeIn(pz, shift=UP * 0.3), run_time=0.6)
        self.zoom(jaw + LEFT * 1.05, 4.4, 0.6)
        self.play(Create(resal), FadeIn(nota), run_time=0.6)
        self.en("debe")
        ok = etiqueta("corriente de trabajo < 26,5 A de placa  ✓", VERDE_OK, 24).move_to([-4.6, 3.3, 0]).scale(0.8)
        ok.scale(0.45).next_to(nota, DOWN, buff=0.15)
        self.play(FadeIn(ok), run_time=0.4)
        self.cerrar_voz(0.2)
        self.zoom_fuera(0.5)
        self.play(FadeOut(pz), FadeOut(nota), FadeOut(ok), FadeOut(resal), run_time=0.4)
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
        ops["H1"] = self.cambiar(ops["H1"], "H1")
        ops["H2"] = self.cambiar(ops["H2"], "H2on")
        self.en("aunque")
        s1p = self.cambiar(ops["S1"], "S1p")
        no = etiqueta("ARRANQUE pulsado → no arranca", ROJO, 24).move_to([-4.6, 3.3, 0]).scale(0.8)
        self.play(FadeIn(no), run_time=0.4)
        ops["S1"] = self.cambiar(s1p, "S1")
        self.en("reset")
        E["F3"] = self.cambiar(E["F3"], "F3")
        rs = etiqueta("RESET → listo para arrancar", "#2563EB", 24).move_to([-4.6, 3.3, 0]).scale(0.8)
        self.sfx("tic", -6)
        self.play(FadeTransform(no, rs), run_time=0.5)
        self.cerrar_voz(0.3)
        self.salir()

    # =============================================================== CIERRE (sin portadilla: no es parte de la práctica)
    def h_cierre(self):
        self.voz("cierre")
        lg = ImageMobject(str(LOGO)).scale_to_fit_width(2.8).move_to([0, 1.6, 0])
        us = T("@miguelesquit", 40, MARCA, "HEAVY").next_to(lg, DOWN, buff=0.35)
        yt = VGroup(pastilla("SUSCRÍBETE", ROJO, 34, True), pastilla("SÍGUEME", MARCA, 34, True)).arrange(RIGHT, buff=0.4).next_to(us, DOWN, buff=0.45)
        sig = T("Mira mi siguiente video", 34, TXT, "HEAVY").next_to(yt, DOWN, buff=0.55)
        self.play(FadeIn(lg, scale=0.8), FadeIn(us), run_time=0.7)
        self.en("suscribete", 0.2)
        self.play(FadeIn(yt[0], scale=1.15), run_time=0.4)
        self.en("sigueme", 0.2)
        self.play(FadeIn(yt[1], scale=1.15), run_time=0.4)
        self.en("siguiente", 0.3)
        self.play(FadeIn(sig, shift=UP * 0.2), run_time=0.6)
        self.cerrar_voz(0.2)
        self.wait(5.0)

    # =============================================================== (ya no se usa) TABLERO
    def gabinete(self, centro=(-4.35, -0.2), alto=7.6):
        """Plancha de 400 × 300 mm: canaleta ranurada 40 × 60 mm en el perímetro y entre filas, riel DIN 35 mm dorado con tornillos."""
        kt = alto / 400.0
        cx, cy = centro
        def P(x, y):
            return np.array([cx + (x - 150) * kt, cy - (y - 200) * kt, 0])
        g = {"P": P, "kt": kt}
        marco = Rectangle(width=300 * kt + 0.16, height=400 * kt + 0.16, stroke_color="#4B5159", stroke_width=4).set_fill("#AEB4BA", 1).move_to(P(150, 200))
        g["gabinete"] = VGroup(marco, Text("400 mm", font=SANS, font_size=20, weight="BOLD", color=OSC2).rotate(PI / 2).next_to(marco, LEFT, buff=0.1),
                               Text("300 mm", font=SANS, font_size=20, weight="BOLD", color=OSC2).next_to(marco, DOWN, buff=0.08))
        g["plancha"] = Rectangle(width=300 * kt, height=400 * kt, stroke_color="#5F6670", stroke_width=2).set_fill("#E6E9EB", 1).move_to(P(150, 200))

        def canaleta(x0, y0, x1, y1):
            w, h = (x1 - x0) * kt, (y1 - y0) * kt
            base = Rectangle(width=w, height=h, stroke_color="#3F454D", stroke_width=2.2).set_fill("#C3C8CD", 1).move_to(P((x0 + x1) / 2, (y0 + y1) / 2))
            det = VGroup()
            horiz = (x1 - x0) > (y1 - y0)
            L = (x1 - x0) if horiz else (y1 - y0)
            n = int(L // 22)
            for k_ in range(n):
                s_ = 11 + 22 * k_
                if horiz:
                    c = P(x0 + s_, (y0 + y1) / 2)
                    if k_ % 2 == 0:
                        det.add(RoundedRectangle(width=13 * kt, height=4.5 * kt, corner_radius=2.2 * kt, stroke_color="#3F454D", stroke_width=1.2).set_fill("#FFFFFF", 1).move_to(c))
                    else:
                        det.add(Circle(radius=1.6 * kt, stroke_color="#3F454D", stroke_width=1.2).set_fill("#FFFFFF", 1).move_to(c))
                else:
                    c = P((x0 + x1) / 2, y0 + s_)
                    if k_ % 2 == 0:
                        det.add(RoundedRectangle(width=4.5 * kt, height=13 * kt, corner_radius=2.2 * kt, stroke_color="#3F454D", stroke_width=1.2).set_fill("#FFFFFF", 1).move_to(c))
                    else:
                        det.add(Circle(radius=1.6 * kt, stroke_color="#3F454D", stroke_width=1.2).set_fill("#FFFFFF", 1).move_to(c))
            # dientes de la canaleta ranurada a lo largo de los bordes
            for k_ in range(int(L // 6)):
                s_ = 3 + 6 * k_
                if horiz:
                    for yy in (y0 + 1.2, y1 - 1.2):
                        det.add(Rectangle(width=2.4 * kt, height=2.4 * kt, stroke_width=0).set_fill("#5F6670", 1).move_to(P(x0 + s_, yy)))
                else:
                    for xx in (x0 + 1.2, x1 - 1.2):
                        det.add(Rectangle(width=2.4 * kt, height=2.4 * kt, stroke_width=0).set_fill("#5F6670", 1).move_to(P(xx, y0 + s_)))
            return VGroup(base, det)
        cans = VGroup(canaleta(0, 0, 300, 40), canaleta(0, 360, 300, 400), canaleta(0, 40, 40, 360), canaleta(260, 40, 300, 360), canaleta(40, 215, 260, 255))
        cans.add(*[Line(P(*a), P(*b)).set_stroke("#3F454D", 2) for a, b in (((0, 0), (40, 40)), ((300, 0), (260, 40)), ((0, 400), (40, 360)), ((300, 400), (260, 360)))])
        tor_c = VGroup(*[self._tornillo_n(P(x, y), 3.2 * kt) for x, y in ((80, 20), (150, 20), (220, 20), (20, 110), (20, 300), (280, 110), (280, 300), (80, 380), (220, 380), (110, 235), (190, 235))])
        g["canaletas"] = VGroup(cans, tor_c)

        def riel(y):
            r = Rectangle(width=220 * kt, height=35 * kt, stroke_color="#7A5C12", stroke_width=1.6).set_fill("#E6BE57", 1).move_to(P(150, y))
            lineas = VGroup(Line(P(40, y - 13.5), P(260, y - 13.5)), Line(P(40, y + 13.5), P(260, y + 13.5))).set_stroke("#7A5C12", 1.4)
            return VGroup(r, lineas)
        g["rieles"] = VGroup(riel(120), riel(305))
        g["tornillos"] = VGroup(*[self._tornillo_n(P(x, y), 3.4 * kt) for y in (120, 305) for x in (48, 252)])
        e = {}
        e["F2"] = Eq3("F2", kt).poner(*P(52, 120 - 40.3)[:2])
        e["F1"] = Eq3("F1", kt).poner(*P(114, 120 - 40.3)[:2])
        e["KM1"] = Eq3("KM1", kt).poner(*P(150, 84)[:2])
        e["F3"] = Eq3("F3", kt).poner(*P(150.14, 84 + 72.66)[:2])
        e["KM1"].set_z_index(2)
        e["F3"].set_z_index(1)
        e["X0"] = Eq3("X0", kt).poner(*P(58, 305 - 25.5)[:2])
        e["X1"] = Eq3("X1", kt).poner(*P(148, 305 - 25.5)[:2])
        g["equipos"] = e
        # puerta abierta (vista interior) con los bloques de contacto
        x_p = P(300, 0)[0] + 0.35
        puerta = Rectangle(width=2.6, height=400 * kt + 0.16, stroke_color="#4B5159", stroke_width=4).set_fill("#D2D6DB", 1)
        puerta.move_to([x_p + 1.3, cy, 0])
        g["puerta"] = puerta
        ops = {}
        for i, n in enumerate(("S0", "S1", "H1", "H2")):
            yy = cy + 2.6 - 1.55 * i
            b = Eq3(n + "b", 0.030)
            b.img.move_to([puerta.get_center()[0] + 0.35, yy, 0])
            tag = VGroup(Rectangle(width=0.62, height=0.28, stroke_width=0).set_fill("#F5C400", 1), Text(f"-{n}", font=SANS, font_size=16, weight="HEAVY", color=OSC))
            tag[1].move_to(tag[0])
            tag.next_to(b.img, LEFT, buff=0.12)
            ops[n] = Group(b, tag)
            ops[n].b = b
        g["ops"] = ops
        return g

    def _tornillo_n(self, p, r):
        return VGroup(Circle(radius=r).set_fill("#F28C28", 1).set_stroke("#7A3E0B", 1.2),
                      Line([-0.6 * r, -0.6 * r, 0], [0.6 * r, 0.6 * r, 0]).set_stroke("#7A3E0B", 1.4),
                      Line([-0.6 * r, 0.6 * r, 0], [0.6 * r, -0.6 * r, 0]).set_stroke("#7A3E0B", 1.4)).move_to(p)

    def cableado_gabinete(self, g):
        """Cada borne usado: cable con puntera y número que va recto a la canaleta más cercana (entra por la ranura)."""
        P, kt, e = g["P"], g["kt"], g["equipos"]
        out = Group()
        y_sup, y_med_a, y_med_b, y_inf, x_der = P(0, 38)[1], P(0, 217)[1], P(0, 253)[1], P(0, 362)[1], P(262, 0)[0]
        x_gap = P(141, 0)[0]

        def stub(eq, b, pts, col, cl, num):
            A, d = eq.boca(b)
            pu, lp = puntera(A, d, cl, kt)
            pu.set_z_index(6)
            ini = A + d * lp
            ruta = ruta_redondeada([ini] + [np.array(p, float) for p in pts], 0.06)
            w = (4.0 if cl == "pot" else 2.6)
            ruta.set_stroke(col, w).set_fill(opacity=0)
            gg = Group(fisico(ruta), pu)
            if col == PE_V:
                gg.add(fisico(DashedVMobject(ruta.copy(), num_dashes=20, dashed_ratio=0.5).set_stroke(PE_A, w)))
            return gg
        def arriba(eq, b, col, cl, num, y=y_sup):
            A, _ = eq.boca(b)
            return stub(eq, b, [[A[0], y, 0]], col, cl, num)
        def abajo(eq, b, col, cl, num, y):
            A, _ = eq.boca(b)
            return stub(eq, b, [[A[0], y, 0]], col, cl, num)
        F2, F1, KM1, F3, X0, X1 = (e[k] for k in ("F2", "F1", "KM1", "F3", "X0", "X1"))
        for b, n in (("1", "L1"), ("3", "L2"), ("5", "L3")):
            out.add(arriba(F2, b, NEGRO_P, "pot", n))
        out.add(arriba(F1, "1", ROJO_M, "mando", "1"))
        for b, n in (("2", "L1"), ("4", "L2"), ("6", "L3")):
            out.add(abajo(F2, b, NEGRO_P, "pot", n, y_med_a))
        out.add(abajo(F1, "2", ROJO_M, "mando", "2", y_med_a))
        for b, n in (("1/L1", "L1"), ("3/L2", "L2"), ("5/L3", "L3")):
            out.add(arriba(KM1, b, NEGRO_P, "pot", n))
        out.add(arriba(KM1, "21", ROJO_M, "mando", "2"))
        for b, n, dx in (("13", "4", 0.0), ("14", "5", 0.05)):
            A, _ = KM1.boca(b)
            out.add(stub(KM1, b, [[x_gap + dx, A[1], 0], [x_gap + dx, y_sup, 0]], ROJO_M, "mando", n))
        for b, n, col in (("A1", "5", ROJO_M), ("A2", "N", NEUTRO_C), ("95", "2", ROJO_M)):
            eq = F3 if b == "95" else KM1
            A, _ = eq.boca(b)
            out.add(stub(eq, b, [[x_der, A[1], 0]], col, "mando", n))
        A, _ = KM1.boca("22")
        out.add(stub(KM1, "22", [[A[0], KM1.borde("d") + 0.02, 0], [x_der, KM1.borde("d") + 0.02, 0]], ROJO_M, "mando", "6"))
        for b, n in (("2/T1", "T1"), ("4/T2", "T2"), ("6/T3", "T3")):
            out.add(abajo(F3, b, NEGRO_P, "pot", n, y_med_a))
        out.add(abajo(F3, "96", ROJO_M, "mando", "3", y_med_a))
        for i, (b, col, n) in enumerate((("1", NEGRO_P, "L1"), ("2", NEGRO_P, "L2"), ("3", NEGRO_P, "L3"), ("4", NEUTRO_C, "N"), ("5", PE_V, "PE"))):
            out.add(arriba(X0, f"{b}_a", col, "pot", n, y_med_b))
            out.add(abajo(X0, f"{b}_b", col, "pot", None, y_inf))
        for b, col, n in (("1", NEGRO_P, "T1"), ("2", NEGRO_P, "T2"), ("3", NEGRO_P, "T3"), ("4", PE_V, "PE")):
            out.add(arriba(X1, f"{b}_a", col, "pot", n, y_med_b))
            out.add(abajo(X1, f"{b}_b", col, "pot", None, y_inf))
        # puerta: mazo flexible desde la canaleta derecha, por la bisagra, hasta cada bloque
        pu_ = g["puerta"]
        xb = pu_.get_left()[0] + 0.32
        a = P(285, 150)
        maz = ruta_redondeada([a, [pu_.get_left()[0] - 0.05, a[1], 0], [xb, a[1] - 0.25, 0], [xb, pu_.get_bottom()[1] + 0.5, 0]], 0.25)
        espiral = DashedVMobject(maz.copy(), num_dashes=70, dashed_ratio=0.55).set_stroke("#1F2937", 9)
        out.add(fisico(VGroup(maz.copy().set_stroke("#D92D20", 7), maz.copy().shift(RIGHT * 0.06).set_stroke(NEUTRO_C, 5), espiral)))
        for n, o in g["ops"].items():
            b = o.b
            for bn in ENTRADAS[n + "b"]:
                A, d = b.boca(bn, n + "b")
                col = NEUTRO_C if bn == "X2" else ROJO_M
                pu, lp = puntera(A, d, "mando", 0.030)
                yy = A[1] + d[1] * 0.28
                r = ruta_redondeada([A + d * lp, [A[0], yy, 0], [xb + 0.06, yy, 0]], 0.08).set_stroke(col, 2.6).set_fill(opacity=0)
                out.add(Group(fisico(r), pu))
        return out

    def h_tablero(self):
        self.seccion("tablero")
        g = self.gabinete()
        P = g["P"]
        self.voz("t1")
        self.play(FadeIn(g["gabinete"], shift=UP * 0.2), run_time=0.9)
        self.cerrar_voz(0.05)
        self.voz("t2")
        self.play(FadeIn(g["plancha"], shift=DOWN * 0.15), run_time=0.8)
        self.cerrar_voz(0.05)
        self.voz("t3")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in g["canaletas"][0]], lag_ratio=0.2), run_time=1.5)
        lc = etiqueta("Canaleta ranurada 40 × 60 mm", "#475467", 22).scale(0.9).move_to([3.9, 2.8, 0])
        fl = Arrow(lc.get_left(), P(275, 120), buff=0.1, color="#475467", stroke_width=3, max_tip_length_to_length_ratio=0.06)
        self.play(FadeIn(lc), GrowArrow(fl), FadeIn(g["canaletas"][1]), run_time=0.6)
        self.cerrar_voz(0.05)
        self.voz("t4")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in g["rieles"]], lag_ratio=0.3), run_time=1.0)
        lr = etiqueta("Riel DIN 35 mm", "#7A5C12", 22).scale(0.9).move_to([3.9, 1.8, 0])
        fr_ = Arrow(lr.get_left(), P(230, 120), buff=0.1, color="#7A5C12", stroke_width=3, max_tip_length_to_length_ratio=0.06)
        self.play(FadeIn(lr), GrowArrow(fr_), run_time=0.5)
        for tr in g["tornillos"]:
            self.sfx("tornillo", -14)
            self.play(FadeIn(tr, scale=1.6), run_time=0.16)
        self.cerrar_voz(0.05)
        self.play(FadeOut(VGroup(lc, fl, lr, fr_)), run_time=0.3)
        self.voz("t5")
        e = g["equipos"]
        self.en("arriba")
        self.sfx("breaker", -10)
        self.play(FadeIn(e["F2"], shift=DOWN * 0.3), FadeIn(e["F1"], shift=DOWN * 0.3), run_time=0.5)
        self.en("contactor")
        self.sfx("contactor", -10)
        self.play(FadeIn(e["KM1"], shift=DOWN * 0.3), FadeIn(e["F3"], shift=DOWN * 0.3), run_time=0.5)
        self.en("abajo")
        self.sfx("tic", -10)
        self.play(FadeIn(e["X0"], shift=DOWN * 0.3), FadeIn(e["X1"], shift=DOWN * 0.3), run_time=0.5)
        self.cerrar_voz(0.05)
        self.voz("t6")
        self.play(FadeIn(g["puerta"], shift=LEFT * 0.3), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(o, scale=0.9) for o in g["ops"].values()], lag_ratio=0.2), run_time=1.0)
        self.cerrar_voz(0.05)
        self.voz("t7")
        cab = self.cableado_gabinete(g)
        # las canaletas tapan la punta de cada cable (entra por la ranura)
        for c in g["canaletas"]:
            c.set_z_index(9)
        mo = Eq3("M1", 0.0145).move_to([5.6, -1.6, 0])
        x1b = e["X1"].boca("2_b")[0]
        gl = mo.mm(132, 79)
        manguera = ruta_redondeada([[x1b[0], P(0, 400)[1], 0], [x1b[0], -4.2, 0], [gl[0] - 1.0, -4.2, 0], [gl[0] - 1.0, gl[1], 0], gl], 0.35)
        manguera = fisico(VGroup(manguera.copy().set_stroke("#6B7280", 14), manguera.copy().set_stroke("#C9CED4", 10)))
        self.play(LaggedStart(*[FadeIn(c) for c in cab], lag_ratio=0.03), run_time=3.0)
        self.play(FadeIn(mo), Create(manguera), run_time=1.0)
        self.cerrar_voz(0.4)
        self.wait(1.0)
        self.salir()

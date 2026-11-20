"""Piezas detalladas para el Short del variador de frecuencia (nov-2026).
Regla del usuario: cada pieza con detalle real (tornillería, rótulos, texturas, sombras); sin marcas comerciales.
Referencias de apariencia: variadores compactos de 7,5 hp / 480 V (teclado con display de 7 segmentos, potenciómetro,
bornera de potencia L1 L2 L3 / + − BR / U V W / PE y bornera de control DI, AI 0–10 V y 4–20 mA, AO, relé de falla),
motor TEFC (NEMA), bomba centrífuga de succión axial, capacitores electrolíticos de terminal de tornillo y resistencias de
frenado en carcasa de aluminio.
"""
from manim import *
import numpy as np
from comun_e import T, Tm

P = lambda x, y: np.array([x, y, 0.0])

ACERO = "#C9CED6"; ACERO_O = "#8A929C"; ACERO_OO = "#59616E"
NEGRO_P = "#1B1F27"; CU = "#C8743F"


def tornillo(p, r=0.06, fondo="#C9CED6", cruz=True):
    c = Circle(radius=r, stroke_color="#475467", stroke_width=max(0.6, r * 12)).set_fill(fondo, 1).move_to(p)
    br = Arc(radius=r * 0.75, start_angle=PI * 0.55, angle=PI * 0.6).set_stroke(WHITE, max(0.5, r * 8), 0.6).move_arc_center_to(p)
    if cruz:
        l1 = Line(p + LEFT * r * 0.6, p + RIGHT * r * 0.6).set_stroke("#344054", max(0.6, r * 14))
        l2 = Line(p + DOWN * r * 0.6, p + UP * r * 0.6).set_stroke("#344054", max(0.6, r * 14))
        return VGroup(c, br, l1, l2)
    l1 = Line(p + LEFT * r * 0.6 + DOWN * r * 0.3, p + RIGHT * r * 0.6 + UP * r * 0.3).set_stroke("#344054", max(0.6, r * 14))
    return VGroup(c, br, l1)


def tuerca_hex(p, r=0.08, color="#98A2B3"):
    h = RegularPolygon(6, radius=r).set_fill(color, 1).set_stroke("#475467", max(0.6, r * 10)).move_to(p)
    return VGroup(h, Circle(radius=r * 0.45, stroke_color="#475467", stroke_width=max(0.5, r * 8)).set_fill("#D0D5DD", 1).move_to(p))


def rotulo(texto, size, color=WHITE, peso="BOLD"):
    return T(texto, size, color, peso)


# ============================================================================ VARIADOR (vista frontal)
def variador(s=1.0, hz="60.00"):
    """Variador compacto de 7,5 hp, de frente, con la tapa de bornes retirada. Unidades a s=1: 3,6 × 6,0."""
    g = VGroup()
    # disipador (detrás) y aletas visibles a los lados
    dis = Rectangle(width=4.0, height=5.7, stroke_color="#667085", stroke_width=1.2).set_fill("#A7AFBA", 1).move_to(P(0, -0.05))
    aletas = VGroup(*[Line(P(x, -2.85), P(x, 2.75)).set_stroke("#7D8592", 1.4) for x in list(np.linspace(-1.98, -1.84, 4)) + list(np.linspace(1.84, 1.98, 4))])
    g.add(dis, aletas)
    cuerpo = RoundedRectangle(width=3.6, height=6.0, corner_radius=0.12, stroke_color="#0F1216", stroke_width=2).set_fill("#2E343D", 1)
    brillo = RoundedRectangle(width=3.56, height=5.96, corner_radius=0.11, stroke_width=0).set_fill(WHITE, 0.035)
    brillo.stretch(0.5, 0).align_to(cuerpo, LEFT)
    g.add(cuerpo, brillo)
    # ventilador superior (rejilla)
    rej = RoundedRectangle(width=2.9, height=0.34, corner_radius=0.05, stroke_width=0).set_fill("#1A1E24", 1).move_to(P(0, 2.74))
    ran = VGroup(*[RoundedRectangle(width=0.06, height=0.24, corner_radius=0.02, stroke_width=0).set_fill("#0A0C0F", 1).move_to(P(x, 2.74)) for x in np.linspace(-1.3, 1.3, 22)])
    g.add(rej, ran)
    # tapa frontal
    tapa = RoundedRectangle(width=3.32, height=3.35, corner_radius=0.08, stroke_color="#4B5360", stroke_width=1.4).set_fill("#3A414C", 1).move_to(P(0, 0.88))
    g.add(tapa)
    # ---------------- teclado
    kp = RoundedRectangle(width=2.76, height=1.82, corner_radius=0.08, stroke_color="#5F6876", stroke_width=1.4).set_fill(NEGRO_P, 1).move_to(P(0, 1.55))
    disp_marco = RoundedRectangle(width=1.72, height=0.56, corner_radius=0.04, stroke_color="#4B5360", stroke_width=1).set_fill("#06110B", 1).move_to(P(-0.36, 2.15))
    digitos = Tm(hz, 25, "#39FF88", "BOLD").move_to(disp_marco).shift(LEFT * 0.08)
    sombra_dig = Tm("88.88", 25, "#123222", "BOLD").move_to(digitos)
    unidades = VGroup()
    for k, (u, on) in enumerate((("Hz", True), ("A", False), ("V", False))):
        led = Circle(radius=0.035, stroke_width=0).set_fill("#39FF88" if on else "#2C3A31", 1).move_to(P(0.66, 2.33 - 0.17 * k))
        unidades.add(led, T(u, 7, "#C9D1D9", "BOLD").next_to(led, RIGHT, buff=0.05))
    est = VGroup()
    for k, (u, col, on) in enumerate((("RUN", "#39FF88", True), ("FWD", "#39FF88", True), ("REV", "#39FF88", False), ("FLT", "#FF4D4D", False))):
        led = Circle(radius=0.03, stroke_width=0).set_fill(col if on else "#3A3F47", 1).move_to(P(-1.08 + 0.42 * k, 1.78))
        est.add(led, T(u, 6, "#AEB6C2", "BOLD").next_to(led, RIGHT, buff=0.04))
    teclas = VGroup()
    def tecla(p, txt, col="#2E343D", tcol="#E4E7EC", w=0.42, h=0.24):
        b = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color="#0B0D10", stroke_width=1).set_fill(col, 1).move_to(p)
        hl = Line(b.get_corner(UL) + RIGHT * 0.05 + DOWN * 0.03, b.get_corner(UR) + LEFT * 0.05 + DOWN * 0.03).set_stroke(WHITE, 0.8, 0.25)
        return VGroup(b, hl, T(txt, 7, tcol, "HEAVY").move_to(p))
    for k, t_ in enumerate(("ESC", "▲", "ENT")):
        teclas.add(tecla(P(-1.0 + 0.5 * k, 1.47), t_))
    for k, t_ in enumerate(("◄", "▼", "PRG")):
        teclas.add(tecla(P(-1.0 + 0.5 * k, 1.17), t_))
    run = tecla(P(-0.8, 0.83), "RUN", "#12924F", WHITE, 0.62, 0.26)
    stop = tecla(P(-0.1, 0.83), "STOP/RST", "#C0262D", WHITE, 0.62, 0.26)
    teclas.add(run, stop)
    # potenciómetro
    pc = P(0.86, 1.2)
    escala = VGroup(*[Line(pc + 0.36 * np.array([np.cos(a), np.sin(a), 0]), pc + 0.42 * np.array([np.cos(a), np.sin(a), 0])).set_stroke("#AEB6C2", 1)
                      for a in np.linspace(-PI / 4 - 0.3, PI * 1.25 + 0.3, 11)])
    perilla = Circle(radius=0.28, stroke_color="#0B0D10", stroke_width=1.2).set_fill("#3A414C", 1).move_to(pc)
    estria = VGroup(*[Line(pc + 0.22 * np.array([np.cos(a), np.sin(a), 0]), pc + 0.28 * np.array([np.cos(a), np.sin(a), 0])).set_stroke("#1B1F27", 1.2) for a in np.linspace(0, TAU, 24, endpoint=False)])
    indic = Line(pc, pc + 0.2 * np.array([np.cos(PI * 0.15), np.sin(PI * 0.15), 0])).set_stroke("#FDB022", 2)
    mm = VGroup(T("MIN", 5, "#AEB6C2", "BOLD").move_to(pc + P(-0.3, -0.4)), T("MAX", 5, "#AEB6C2", "BOLD").move_to(pc + P(0.3, -0.4)))
    pot = VGroup(escala, perilla, estria, indic, mm)
    g.add(kp, disp_marco, sombra_dig, digitos, unidades, est, teclas, pot)
    # ---------------- placa de datos y advertencia
    placa = RoundedRectangle(width=2.0, height=0.82, corner_radius=0.03, stroke_color="#98A2B3", stroke_width=0.8).set_fill("#F2F4F7", 1).move_to(P(-0.42, 0.0) + DOWN * 0.08)
    lin = VGroup(T("VARIADOR DE FRECUENCIA · 5,5 kW / 7,5 hp", 5.2, "#101828", "HEAVY"),
                 T("ENTRADA: 3F 380–480 V  50/60 Hz  14,5 A", 5, "#344054", "BOLD"),
                 T("SALIDA:  3F 0–480 V  0–400 Hz  13 A (servicio pesado)", 5, "#344054", "BOLD"),
                 T("IP20 · IEC 61800-5-1 · Temp. amb. −10…+50 °C", 5, "#344054", "BOLD")).arrange(DOWN, buff=0.045, aligned_edge=LEFT)
    lin.scale_to_fit_width(1.84).move_to(placa)
    adv = VGroup(RoundedRectangle(width=0.82, height=0.82, corner_radius=0.03, stroke_width=0).set_fill("#F5C400", 1),
                 Triangle(stroke_color="#101828", stroke_width=1.5).set_fill("#F5C400", 1).scale(0.17).shift(UP * 0.16),
                 T("!", 9, "#101828", "HEAVY").shift(UP * 0.13),
                 T("ALTA TENSIÓN", 4.5, "#101828", "HEAVY").shift(DOWN * 0.1),
                 T("Bus DC cargado:", 3.8, "#101828", "BOLD").shift(DOWN * 0.22),
                 T("espere antes de abrir", 3.8, "#101828", "BOLD").shift(DOWN * 0.31)).move_to(P(1.06, -0.08))
    g.add(placa, lin, adv)
    tt = VGroup(*[tornillo(P(x, -0.66), 0.055) for x in (-1.4, 1.4)])
    g.add(tt)
    # ---------------- zona de bornes (tapa retirada)
    cav = RoundedRectangle(width=3.32, height=2.12, corner_radius=0.05, stroke_color="#0F1216", stroke_width=1.2).set_fill("#14171C", 1).move_to(P(0, -1.84))
    g.add(cav)
    # bornera de control
    nombres_c = ["DI1", "DI2", "DI3", "DI4", "COM", "+24V", "AI1", "AI2", "GND", "+10V", "AO1", "RA", "RB", "RC"]
    ctrl = VGroup(); bc = {}
    x0 = -1.43
    for k, n in enumerate(nombres_c):
        x = x0 + 0.212 * k + (0.06 if k >= 11 else 0)
        cuerpo_t = Rectangle(width=0.2, height=0.34, stroke_color="#0B0D10", stroke_width=0.8).set_fill("#4E8A57" if k < 11 else "#2F6FD0", 1).move_to(P(x, -1.14))
        ranura = Rectangle(width=0.12, height=0.07, stroke_width=0).set_fill("#0B0D10", 1).move_to(P(x, -1.27))
        tor = tornillo(P(x, -1.08), 0.045, cruz=False)
        et = T(n, 4.4, "#E4E7EC", "BOLD").move_to(P(x, -0.88))
        pieza = VGroup(cuerpo_t, ranura, tor, et)
        ctrl.add(pieza); bc[n] = pieza
    dip = VGroup(Rectangle(width=0.32, height=0.16, stroke_width=0).set_fill("#C0262D", 1), Rectangle(width=0.06, height=0.08, stroke_width=0).set_fill(WHITE, 1).shift(LEFT * 0.06 + UP * 0.02),
                 Rectangle(width=0.06, height=0.08, stroke_width=0).set_fill(WHITE, 1).shift(RIGHT * 0.06 + DOWN * 0.02), T("AI2: V / I", 3.6, "#E4E7EC", "BOLD").shift(DOWN * 0.14)).move_to(P(-0.95, -1.55))
    ctrl.add(dip)
    # bornera de potencia
    nombres_p = [("L1", 0), ("L2", 0), ("L3", 0), ("PE", 0), ("+", 1), ("−", 1), ("BR", 1), ("U", 2), ("V", 2), ("W", 2), ("PE ", 2)]
    pot_b = VGroup(); bp = {}
    xs = []
    x = -1.42
    grupo_prev = 0
    for n, gr in nombres_p:
        if gr != grupo_prev:
            x += 0.1
            grupo_prev = gr
        xs.append(x); x += 0.262
    cols_g = {0: "#D0D5DD", 1: "#D0D5DD", 2: "#D0D5DD"}
    for (n, gr), x in zip(nombres_p, xs):
        caja = Rectangle(width=0.25, height=0.52, stroke_color="#475467", stroke_width=1).set_fill(cols_g[gr], 1).move_to(P(x, -2.18))
        pared = Rectangle(width=0.03, height=0.6, stroke_width=0).set_fill("#98A2B3", 1).move_to(P(x + 0.131, -2.18))
        tor = tornillo(P(x, -2.08), 0.075)
        boca = Rectangle(width=0.16, height=0.1, stroke_width=0).set_fill("#101828", 1).move_to(P(x, -2.36))
        colr = {"+": "#E5484D", "−": "#7AA7FF", "BR": "#FDB022"}.get(n, "#E4E7EC")
        if n.strip() == "PE":
            et = VGroup(Line(P(-0.05, 0.02), P(0.05, 0.02)), Line(P(-0.035, -0.0), P(0.035, -0.0)), Line(P(-0.02, -0.02), P(0.02, -0.02)), Line(P(0, 0.02), P(0, 0.06))).set_stroke("#3DDC84", 1.2).move_to(P(x, -1.83))
        else:
            et = T(n, 6.5, colr, "HEAVY").move_to(P(x, -1.83))
        pieza = VGroup(caja, pared, tor, boca, et)
        pot_b.add(pieza); bp[n.strip() if n.strip() != "PE" or "in" else n] = pieza
    bp["PE_in"], bp["PE_out"] = pot_b[3], pot_b[10]
    grupos = VGroup(T("ALIMENTACIÓN", 3.8, "#AEB6C2", "BOLD").move_to(P(np.mean(xs[0:4]), -2.53)),
                    T("BUS DC / FRENO", 3.8, "#AEB6C2", "BOLD").move_to(P(np.mean(xs[4:7]), -2.53)),
                    T("MOTOR", 3.8, "#AEB6C2", "BOLD").move_to(P(np.mean(xs[7:11]), -2.53)))
    charge = VGroup(Circle(radius=0.035, stroke_width=0).set_fill("#FF3B30", 1), T("CHARGE", 3.8, "#FF8A80", "BOLD").shift(RIGHT * 0.17)).move_to(P(np.mean(xs[4:7]) + 0.05, -1.6))
    g.add(ctrl, pot_b, grupos, charge)
    # placa de prensaestopas
    base = RoundedRectangle(width=3.2, height=0.3, corner_radius=0.04, stroke_color="#0F1216", stroke_width=1).set_fill("#262B33", 1).move_to(P(0, -2.83))
    pe = VGroup(*[VGroup(Circle(radius=0.12, stroke_width=0).set_fill("#0F1216", 1), tuerca_hex(ORIGIN, 0.1, "#4B5360")).move_to(P(x, -2.83)) for x in (-0.95, 0.0, 0.95)])
    g.add(base, pe)
    g.scale(s)
    g.digitos, g.teclado, g.pot_bloque, g.ctrl_bloque, g.bp, g.bc = digitos, VGroup(kp, disp_marco, digitos, teclas, pot), pot_b, ctrl, bp, bc
    g.charge, g.charge_led, g.placa, g.run, g.stop, g.est = charge, charge[0], VGroup(placa, lin), run, stop, est
    return g


# ============================================================================ MOTOR TEFC (vista lateral)
def motor_tefc(s=1.0, color="#3E6A8C"):
    g = VGroup()
    osc = "#25455E"; cl = "#5C8BB0"
    base_l = Line(P(-2.75, -1.38), P(3.3, -1.38)).set_stroke("#475467", 3)
    patas = VGroup()
    for x in (-1.2, 1.15):
        pt = Polygon(P(x - 0.45, -1.35), P(x + 0.45, -1.35), P(x + 0.32, -0.9), P(x - 0.32, -0.9), stroke_color=osc, stroke_width=1.5).set_fill(color, 1)
        patas.add(pt, tuerca_hex(P(x - 0.3, -1.22), 0.07), tuerca_hex(P(x + 0.3, -1.22), 0.07))
    carc = RoundedRectangle(width=3.5, height=2.0, corner_radius=0.18, stroke_color=osc, stroke_width=2).set_fill(color, 1).move_to(P(0, 0))
    aletas = VGroup()
    for y in np.linspace(-0.82, 0.82, 12):
        aletas.add(Line(P(-1.62, y), P(1.62, y)).set_stroke(osc, 2.2), Line(P(-1.62, y + 0.04), P(1.62, y + 0.04)).set_stroke(cl, 0.9, 0.8))
    brillo = Rectangle(width=3.3, height=0.35, stroke_width=0).set_fill(WHITE, 0.08).move_to(P(0, 0.62))
    # escudo lado acople (DE) y cubo de rodamiento
    esc_de = RoundedRectangle(width=0.32, height=1.86, corner_radius=0.1, stroke_color=osc, stroke_width=1.6).set_fill(cl, 1).move_to(P(1.88, 0))
    tor_de = VGroup(*[tuerca_hex(P(1.88, y), 0.055) for y in (-0.7, 0.7)])
    cubo = RoundedRectangle(width=0.22, height=0.8, corner_radius=0.05, stroke_color=osc, stroke_width=1.2).set_fill(color, 1).move_to(P(2.13, 0))
    eje = Rectangle(width=1.0, height=0.34, stroke_color="#667085", stroke_width=1.2).set_fill(ACERO, 1).move_to(P(2.74, 0))
    eje_b = Rectangle(width=1.0, height=0.08, stroke_width=0).set_fill(WHITE, 0.45).move_to(P(2.74, 0.09))
    chav = Rectangle(width=0.55, height=0.07, stroke_width=0).set_fill("#667085", 1).move_to(P(2.84, 0.135))
    # cubierta del ventilador (NDE)
    cub = RoundedRectangle(width=0.95, height=1.9, corner_radius=0.3, stroke_color=osc, stroke_width=1.6).set_fill("#34556F", 1).move_to(P(-2.2, 0))
    ranuras = VGroup(*[RoundedRectangle(width=0.06, height=0.32, corner_radius=0.02, stroke_width=0).set_fill("#14212C", 1).move_to(P(x, y))
                       for x in np.linspace(-2.52, -1.88, 5) for y in (-0.55, -0.1, 0.35)])
    # caja de bornes, cáncamo y placa
    cb = RoundedRectangle(width=1.05, height=0.55, corner_radius=0.06, stroke_color=osc, stroke_width=1.5).set_fill(cl, 1).move_to(P(-0.25, 1.26))
    tapa_cb = RoundedRectangle(width=1.15, height=0.12, corner_radius=0.04, stroke_color=osc, stroke_width=1.2).set_fill(color, 1).move_to(P(-0.25, 1.56))
    tor_cb = VGroup(*[tornillo(P(x, 1.56), 0.035) for x in (-0.72, 0.22)])
    prensa = VGroup(Rectangle(width=0.22, height=0.26, stroke_color=osc, stroke_width=1).set_fill(ACERO_O, 1), tuerca_hex(ORIGIN, 0.09, ACERO)).move_to(P(0.39, 1.2))
    cana = VGroup(Annulus(inner_radius=0.08, outer_radius=0.15, stroke_width=0).set_fill(ACERO_O, 1).move_to(P(0.95, 1.22)),
                  Rectangle(width=0.08, height=0.14, stroke_width=0).set_fill(ACERO_O, 1).move_to(P(0.95, 1.04)))
    placa = RoundedRectangle(width=1.05, height=0.62, corner_radius=0.03, stroke_color="#98A2B3", stroke_width=0.8).set_fill("#E4E7EC", 1).move_to(P(-0.35, -0.05))
    remaches = VGroup(*[Dot(P(-0.35 + dx, -0.05 + dy), radius=0.02, color="#98A2B3") for dx in (-0.47, 0.47) for dy in (-0.25, 0.25)])
    txt = VGroup(T("MOTOR DE INDUCCIÓN 3~  NEMA", 3.8, "#101828", "HEAVY"), T("7,5 hp  460 V  60 Hz  9,2 A", 3.8, "#344054", "BOLD"),
                 T("1765 rpm  FS 1,15  Ef. 91,7 %", 3.8, "#344054", "BOLD"), T("USO CON INVERSOR · MG 1 Parte 31", 3.8, "#0E9BB5", "HEAVY")).arrange(DOWN, buff=0.03, aligned_edge=LEFT)
    txt.scale_to_fit_width(0.95).move_to(placa)
    g.add(base_l, patas, carc, aletas, brillo, esc_de, tor_de, cubo, eje, eje_b, chav, cub, ranuras, cb, tapa_cb, tor_cb, prensa, cana, placa, remaches, txt)
    g.scale(s)
    g.eje, g.chaveta, g.placa_d, g.caja_b = eje, chav, VGroup(placa, remaches, txt), cb
    return g


def girar_eje(mot, rps=1.0):
    """Updater: la chaveta sube y baja como si el eje girara (vista lateral)."""
    ch = mot.chaveta
    c = mot.eje.get_center(); h = mot.eje.height
    ch.fase = 0.0
    ch.rps = rps

    def upd(m, dt):
        m.fase = (m.fase + dt * m.rps * TAU) % TAU
        y = np.sin(m.fase) * h * 0.4
        m.move_to([m.get_x(), c[1] + y, 0])
        m.set_opacity(0.25 if np.cos(m.fase) < 0 else 1)
    ch.add_updater(upd)
    return ch


# ============================================================================ BOMBA CENTRÍFUGA (para el dato)
def bomba(s=1.0, color="#B4443A"):
    g = VGroup()
    osc = "#6E241D"
    soporte = RoundedRectangle(width=1.3, height=0.8, corner_radius=0.08, stroke_color=osc, stroke_width=1.4).set_fill(color, 1).move_to(P(-0.2, -0.1))
    eje = Rectangle(width=0.5, height=0.22, stroke_color="#667085", stroke_width=1).set_fill(ACERO, 1).move_to(P(-1.05, -0.1))
    voluta = Ellipse(width=1.3, height=2.1, stroke_color=osc, stroke_width=2).set_fill(color, 1).move_to(P(1.05, 0.05))
    nervio = Ellipse(width=0.9, height=1.6, stroke_color=osc, stroke_width=1.2).set_fill(opacity=0).move_to(P(1.05, 0.05))
    desc = Rectangle(width=0.5, height=0.7, stroke_color=osc, stroke_width=1.4).set_fill(color, 1).move_to(P(1.05, 1.35))
    br_d = Rectangle(width=0.8, height=0.14, stroke_color=osc, stroke_width=1.2).set_fill(color, 1).move_to(P(1.05, 1.74))
    tor_d = VGroup(*[tuerca_hex(P(1.05 + dx, 1.74), 0.04) for dx in (-0.3, 0.3)])
    suc = Rectangle(width=0.55, height=0.55, stroke_color=osc, stroke_width=1.4).set_fill(color, 1).move_to(P(1.95, -0.2))
    br_s = Rectangle(width=0.14, height=0.85, stroke_color=osc, stroke_width=1.2).set_fill(color, 1).move_to(P(2.25, -0.2))
    tor_s = VGroup(*[tuerca_hex(P(2.25, -0.2 + dy), 0.04) for dy in (-0.32, 0.32)])
    pata = Polygon(P(0.6, -1.1), P(1.5, -1.1), P(1.3, -0.8), P(0.8, -0.8), stroke_color=osc, stroke_width=1.2).set_fill(color, 1)
    pata2 = Polygon(P(-0.7, -1.1), P(0.3, -1.1), P(0.15, -0.5), P(-0.55, -0.5), stroke_color=osc, stroke_width=1.2).set_fill(color, 1)
    tapon = tuerca_hex(P(1.05, -0.85), 0.05)
    flecha = VGroup(Arrow(P(2.9, -0.2), P(2.35, -0.2), buff=0, stroke_width=4, color="#7FD1FF"), Arrow(P(1.05, 1.85), P(1.05, 2.45), buff=0, stroke_width=4, color="#7FD1FF"))
    g.add(pata, pata2, soporte, eje, voluta, nervio, desc, br_d, tor_d, suc, br_s, tor_s, tapon, flecha)
    g.scale(s)
    return g


def acople(s=1.0):
    guarda = RoundedRectangle(width=0.9, height=0.8, corner_radius=0.06, stroke_color="#8F5B00", stroke_width=1.4).set_fill("#F5B400", 1)
    malla = VGroup(*[Line(P(x, -0.36), P(x + 0.25, 0.36)).set_stroke("#8F5B00", 1, 0.6) for x in np.linspace(-0.5, 0.3, 7)])
    return VGroup(guarda, malla).scale(s)


def base_skid(x0, x1, y, s=1.0):
    b = Rectangle(width=(x1 - x0), height=0.22 * s, stroke_color="#344054", stroke_width=1.5).set_fill("#475467", 1).move_to(P((x0 + x1) / 2, y))
    tors = VGroup(*[tuerca_hex(P(x, y), 0.05 * s) for x in np.linspace(x0 + 0.2, x1 - 0.2, 6)])
    return VGroup(b, tors)


# ============================================================================ CAPACITOR ELECTROLÍTICO y BANCO
def capacitor_e(s=1.0, color="#1F3A93"):
    cuerpo = RoundedRectangle(width=0.8, height=1.5, corner_radius=0.08, stroke_color="#0E1B47", stroke_width=1.4).set_fill(color, 1)
    franja = Rectangle(width=0.16, height=1.36, stroke_width=0).set_fill("#C9D3F5", 1).move_to(P(0.24, 0))
    menos = VGroup(*[T("−", 7, color, "HEAVY").move_to(P(0.24, y)) for y in np.linspace(-0.55, 0.55, 5)])
    tapa = Ellipse(width=0.8, height=0.16, stroke_color="#667085", stroke_width=1).set_fill(ACERO, 1).move_to(P(0, 0.75))
    ranura = Line(P(-0.36, 0.62), P(0.36, 0.62)).set_stroke("#0E1B47", 1.5)
    bornes = VGroup(*[VGroup(Rectangle(width=0.14, height=0.12, stroke_width=0).set_fill(ACERO_O, 1).move_to(P(x, 0.86)), tuerca_hex(P(x, 0.92), 0.06)) for x in (-0.2, 0.2)])
    pol = VGroup(T("+", 6, "#E5484D", "HEAVY").move_to(P(-0.2, 1.06)), T("−", 6, "#7AA7FF", "HEAVY").move_to(P(0.2, 1.06)))
    txt = VGroup(T("4700 µF", 4.6, WHITE, "HEAVY"), T("400 V", 4.6, WHITE, "HEAVY"), T("85 °C", 4, "#C9D3F5", "BOLD")).arrange(DOWN, buff=0.04).move_to(P(-0.1, -0.05))
    brillo = Rectangle(width=0.1, height=1.3, stroke_width=0).set_fill(WHITE, 0.12).move_to(P(-0.28, 0))
    return VGroup(cuerpo, brillo, franja, menos, ranura, tapa, bornes, pol, txt).scale(s)


def banco_capacitores(s=1.0):
    pcb = RoundedRectangle(width=3.6, height=2.6, corner_radius=0.06, stroke_color="#0B3D20", stroke_width=1.4).set_fill("#14532D", 1)
    caps = VGroup(*[capacitor_e(0.95).move_to(P(x, -0.15)) for x in (-1.2, -0.4, 0.4, 1.2)])
    barra_p = RoundedRectangle(width=1.5, height=0.1, corner_radius=0.03, stroke_width=0).set_fill(CU, 1).move_to(P(-0.8 - 0.19, 0.78))
    barra_n = RoundedRectangle(width=1.5, height=0.1, corner_radius=0.03, stroke_width=0).set_fill(CU, 1).move_to(P(0.8 + 0.19, 0.78))
    res_bal = VGroup(*[VGroup(Rectangle(width=0.32, height=0.1, stroke_width=0).set_fill("#D9C38A", 1),
                              *[Rectangle(width=0.03, height=0.1, stroke_width=0).set_fill(c, 1).shift(RIGHT * dx) for c, dx in (("#8B5A2B", -0.09), ("#101828", -0.03), ("#E5484D", 0.03), ("#F5C400", 0.09))]).move_to(P(x, -1.05))
                      for x in (-0.8, 0.8)])
    pistas = VGroup(*[Line(P(x, -0.9), P(x, -1.0)).set_stroke("#C9A227", 2) for x in (-1.2, -0.4, 0.4, 1.2)])
    et = VGroup(T("2 en serie · 2 en paralelo", 5, "#D1FADF", "BOLD").move_to(P(0, 1.12)), T("resistencias de equilibrio", 4, "#A6F4C5", "BOLD").move_to(P(0, -1.2)))
    hoyos = VGroup(*[Circle(radius=0.05, stroke_color="#C9A227", stroke_width=1).set_fill("#0B3D20", 1).move_to(P(x, y)) for x in (-1.7, 1.7) for y in (-1.2, 1.2)])
    return VGroup(pcb, hoyos, pistas, caps, barra_p, barra_n, res_bal, et).scale(s)


# ============================================================================ RESISTENCIA DE FRENADO
def resistencia_frenado(s=1.0, calor=0.0):
    cuerpo = RoundedRectangle(width=3.0, height=0.7, corner_radius=0.06, stroke_color="#475467", stroke_width=1.4).set_fill("#B8BEC8", 1)
    aletas = VGroup(*[Line(P(-1.4, y), P(1.4, y)).set_stroke("#8A929C", 1.4) for y in np.linspace(-0.25, 0.25, 6)])
    tapas = VGroup(*[RoundedRectangle(width=0.2, height=0.62, corner_radius=0.04, stroke_color="#475467", stroke_width=1).set_fill("#344054", 1).move_to(P(x, 0)) for x in (-1.6, 1.6)])
    pestanas = VGroup(*[VGroup(Rectangle(width=0.3, height=0.16, stroke_color="#475467", stroke_width=1).set_fill(ACERO_O, 1), Circle(radius=0.04, stroke_width=0).set_fill("#101828", 1)).move_to(P(x, -0.42)) for x in (-1.25, 1.25)])
    cables = VGroup(Line(P(-1.7, 0.1), P(-2.3, 0.1)).set_stroke("#5B6472", 6), Line(P(-1.7, -0.1), P(-2.3, -0.1)).set_stroke("#5B6472", 6))
    et = T("RESISTENCIA DE FRENADO  60 Ω · 1,5 kW", 7, "#E4E7EC", "HEAVY").move_to(P(0, 0.56))
    brillo = cuerpo.copy().set_fill("#FF6B3D", calor).set_stroke(width=0)
    g = VGroup(cables, pestanas, cuerpo, aletas, tapas, brillo, et).scale(s)
    g.brillo = brillo
    return g


# ============================================================================ MULTÍMETRO (CAT III)
def multimetro_cat(s=1.0, lectura="648"):
    funda = RoundedRectangle(width=1.7, height=3.1, corner_radius=0.22, stroke_color="#8F5B00", stroke_width=1.6).set_fill("#F5B400", 1)
    cuerpo = RoundedRectangle(width=1.42, height=2.82, corner_radius=0.14, stroke_color="#101828", stroke_width=1.2).set_fill("#2B3038", 1)
    lcd = RoundedRectangle(width=1.16, height=0.66, corner_radius=0.05, stroke_color="#101828", stroke_width=1).set_fill("#B7C9A8", 1).move_to(P(0, 0.92))
    dig = Tm(lectura, 22, "#101828", "BOLD").move_to(P(-0.08, 0.92))
    uni = T("VDC", 7, "#101828", "HEAVY").move_to(P(0.42, 0.8))
    sel = Circle(radius=0.42, stroke_color="#101828", stroke_width=1.2).set_fill("#3A414C", 1).move_to(P(0, -0.12))
    mando = RoundedRectangle(width=0.18, height=0.7, corner_radius=0.06, stroke_width=0).set_fill("#E4E7EC", 1).move_to(sel).rotate(-PI / 5)
    pos = VGroup(*[T(t, 5, "#E4E7EC", "BOLD").move_to(sel.get_center() + 0.58 * np.array([np.cos(a), np.sin(a), 0]))
                   for t, a in (("OFF", PI / 2), ("VAC", PI / 2 - 0.6), ("VDC", PI / 2 - 1.2), ("Ω", PI / 2 + 0.6), ("A", PI / 2 + 1.2))])
    jacks = VGroup(*[VGroup(Circle(radius=0.09, stroke_width=0).set_fill(c, 1), Circle(radius=0.04, stroke_width=0).set_fill("#101828", 1)).move_to(P(x, -0.98)) for x, c in ((-0.4, "#344054"), (0, "#101828"), (0.4, "#E5484D"))])
    cat = VGroup(T("CAT III 1000 V", 4.8, "#F5B400", "HEAVY"), T("CAT IV 600 V", 4.8, "#F5B400", "HEAVY")).arrange(DOWN, buff=0.03).move_to(P(0, -1.26))
    g = VGroup(funda, cuerpo, lcd, dig, uni, sel, mando, pos, jacks, cat).scale(s)
    g.dig, g.jack_com, g.jack_v = dig, jacks[1], jacks[2]
    return g


def punta(p_ini, p_fin, color="#E5484D"):
    cable = CubicBezier(p_ini, p_ini + DOWN * 0.8, p_fin + DOWN * 1.2, p_fin + DOWN * 0.4).set_stroke(color, 4)
    mango = RoundedRectangle(width=0.1, height=0.55, corner_radius=0.04, stroke_width=0).set_fill(color, 1).move_to(p_fin + DOWN * 0.32)
    guarda = Rectangle(width=0.16, height=0.04, stroke_width=0).set_fill(color, 1).move_to(p_fin + DOWN * 0.06)
    aguja = Line(p_fin + DOWN * 0.05, p_fin + UP * 0.12).set_stroke(ACERO, 2.5)
    return VGroup(cable, mango, guarda, aguja)


# ============================================================================ CABLE PARA VARIADOR (corte)
def cable_vfd(s=1.0):
    g = VGroup()
    g.add(Circle(radius=1.0, stroke_width=0).set_fill("#1B1F27", 1))
    g.add(Circle(radius=0.86, stroke_width=0).set_fill("#9A6A3A", 1))
    malla = VGroup(*[Dot(0.82 * np.array([np.cos(a), np.sin(a), 0]), radius=0.03, color="#E0A86E") for a in np.linspace(0, TAU, 60, endpoint=False)])
    g.add(malla, Circle(radius=0.78, stroke_color="#D9DDE3", stroke_width=2).set_fill("#2B3038", 1))
    for k, (c, n) in enumerate((("#101828", "L1"), ("#6B4423", "L2"), ("#6B7280", "L3"))):
        a = PI / 2 + k * TAU / 3
        p = 0.4 * np.array([np.cos(a), np.sin(a), 0])
        g.add(Circle(radius=0.27, stroke_color="#475467", stroke_width=1).set_fill(c, 1).move_to(p))
        g.add(VGroup(*[Dot(p + 0.09 * np.array([np.cos(b), np.sin(b), 0]), radius=0.045, color=CU) for b in np.linspace(0, TAU, 6, endpoint=False)], Dot(p, radius=0.045, color=CU)))
        g.add(T(n, 5, WHITE, "HEAVY").move_to(p + UP * 0.17))
        a2 = a + TAU / 6
        q = 0.5 * np.array([np.cos(a2), np.sin(a2), 0])
        g.add(VGroup(*[Dot(q + 0.05 * np.array([np.cos(b), np.sin(b), 0]), radius=0.03, color="#E0A86E") for b in np.linspace(0, TAU, 6, endpoint=False)], Dot(q, radius=0.03, color="#E0A86E")))
    return g.scale(s)


# ============================================================================ SÍMBOLOS IEC 60617
def diodo(p, h=0.36, color=WHITE, sw=2.2, arriba=True):
    """Diodo vertical, conduce hacia arriba (ánodo abajo)."""
    d = 1 if arriba else -1
    tri = Polygon(p + DOWN * d * h / 2 + LEFT * h * 0.42, p + DOWN * d * h / 2 + RIGHT * h * 0.42, p + UP * d * h * 0.18, stroke_color=color, stroke_width=sw).set_fill(color, 0)
    bar = Line(p + UP * d * h * 0.18 + LEFT * h * 0.42, p + UP * d * h * 0.18 + RIGHT * h * 0.42).set_stroke(color, sw)
    return VGroup(tri, bar)


def igbt(p, h=0.5, color=WHITE, sw=2.2):
    """IGBT canal N (IEC 60617): colector arriba, emisor abajo; p = punto medio del camino colector-emisor (eje x de los terminales)."""
    xb = p[0] - h * 0.32
    canal = Line(P(xb, p[1] - h * 0.3), P(xb, p[1] + h * 0.3)).set_stroke(color, sw)
    comp = Line(P(xb - h * 0.12, p[1] - h * 0.3), P(xb - h * 0.12, p[1] + h * 0.3)).set_stroke(color, sw)
    comp_g = Line(P(xb - h * 0.12, p[1] - h * 0.22), P(xb - h * 0.45, p[1] - h * 0.22)).set_stroke(color, sw)
    col = VGroup(Line(P(xb, p[1] + h * 0.16), P(p[0], p[1] + h * 0.34)), Line(P(p[0], p[1] + h * 0.34), P(p[0], p[1] + h * 0.5))).set_stroke(color, sw)
    emi = VGroup(Line(P(xb, p[1] - h * 0.16), P(p[0], p[1] - h * 0.34)), Line(P(p[0], p[1] - h * 0.34), P(p[0], p[1] - h * 0.5))).set_stroke(color, sw)
    v = normalize(P(p[0], p[1] - h * 0.34) - P(xb, p[1] - h * 0.16))
    tip = P(p[0], p[1] - h * 0.34) - v * h * 0.04
    perp = np.array([-v[1], v[0], 0])
    flecha = Polygon(tip, tip - v * h * 0.16 + perp * h * 0.07, tip - v * h * 0.16 - perp * h * 0.07, stroke_width=0).set_fill(color, 1)
    g = VGroup(canal, comp, comp_g, col, emi, flecha)
    g.gate = P(xb - h * 0.45, p[1] - h * 0.22)
    return g


def resistencia_sim(a, b, color=WHITE, sw=2.2, w=0.14):
    """Resistencia IEC (rectángulo) entre a y b."""
    v = b - a; L = np.linalg.norm(v); u = v / L
    caja = Rectangle(width=L * 0.5, height=w, stroke_color=color, stroke_width=sw).set_fill(opacity=0).rotate(np.arctan2(u[1], u[0])).move_to((a + b) / 2)
    l1 = Line(a, a + u * L * 0.25).set_stroke(color, sw); l2 = Line(b - u * L * 0.25, b).set_stroke(color, sw)
    return VGroup(l1, caja, l2)


def cap_pol(p, w=0.36, color=WHITE, sw=2.2, gap=0.09):
    top = Line(p + UP * gap / 2 + LEFT * w / 2, p + UP * gap / 2 + RIGHT * w / 2).set_stroke(color, sw)
    bot = Rectangle(width=w, height=0.05, stroke_width=0).set_fill(color, 1).move_to(p + DOWN * gap / 2 + DOWN * 0.025)
    mas = T("+", 9, color, "HEAVY").move_to(p + UP * 0.12 + LEFT * w * 0.55)
    return VGroup(top, bot, mas)


def contacto_no_h(a, b, color=WHITE, sw=2.2, cerrado=False):
    """Contacto NA horizontal entre a y b."""
    L = b[0] - a[0]
    l1 = Line(a, a + RIGHT * L * 0.3).set_stroke(color, sw)
    l2 = Line(b - RIGHT * L * 0.3, b).set_stroke(color, sw)
    mov = Line(a + RIGHT * L * 0.3, b - RIGHT * L * 0.28 + (UP * L * 0.22 if not cerrado else ORIGIN)).set_stroke(color, sw)
    g = VGroup(l1, mov, l2)
    g.mov = mov
    return g


def bobina_l(a, b, color=WHITE, sw=2.2, n=4):
    L = b[0] - a[0]
    r = L * 0.6 / n / 2
    x0 = a[0] + L * 0.2
    arcs = VGroup(*[Arc(radius=r, start_angle=PI, angle=-PI).move_arc_center_to(P(x0 + r + 2 * r * k, a[1])) for k in range(n)]).set_stroke(color, sw)
    return VGroup(Line(a, P(x0, a[1])).set_stroke(color, sw), arcs, Line(P(x0 + 2 * r * n, a[1]), b).set_stroke(color, sw))


def linea_salto(a, b, cruces, r=0.07, color=WHITE, sw=2.2):
    """Línea horizontal de a a b con saltos semicirculares en las x de `cruces`."""
    xs = sorted([c for c in cruces if min(a[0], b[0]) + r < c < max(a[0], b[0]) - r])
    pts = []
    g = VGroup()
    x_prev = a[0]
    for c in xs:
        g.add(Line(P(x_prev, a[1]), P(c - r, a[1])))
        g.add(Arc(radius=r, start_angle=PI, angle=-PI).move_arc_center_to(P(c, a[1])))
        x_prev = c + r
    g.add(Line(P(x_prev, a[1]), b))
    return g.set_stroke(color, sw)


def borne(p, txt, color=WHITE, lado=LEFT, size=10):
    c = Circle(radius=0.055, stroke_color=color, stroke_width=1.8).set_fill("#0B1030", 1).move_to(p)
    return VGroup(c, T(txt, size, color, "HEAVY").next_to(c, lado, buff=0.06))


def motor_sim(p, r=0.36, color=WHITE, sw=2.2):
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=sw).move_to(p), T("M", 13, color, "HEAVY").move_to(p + UP * 0.08), T("3~", 9, color, "HEAVY").move_to(p + DOWN * 0.13))


# ============================================================================ CIRCUITO DE POTENCIA COMPLETO
def circuito_potencia(color=WHITE):
    """Circuito de potencia del variador (IEC 60617): rectificador de 6 pulsos, precarga con bypass, reactor DC,
    bus con capacitores en serie y resistencias de equilibrio, chopper de frenado e inversor de 6 IGBT con diodos de
    rueda libre. Ancho ≈ 8,4; alto ≈ 3,4. Devuelve el grupo con sus partes y puntos clave."""
    sw = 2.2
    yp, yn = 1.35, -1.35
    g = VGroup()
    # --- rectificador
    xr = [-3.15, -2.65, -2.15]
    ys_in = [0.42, 0.0, -0.42]
    rect = VGroup()
    for x, yi in zip(xr, ys_in):
        rect.add(Line(P(x, yp), P(x, yi + 0.42)).set_stroke(color, sw), diodo(P(x, (yp + yi) / 2 + 0.05), 0.34, color, sw),
                 Line(P(x, yi - 0.42), P(x, yn)).set_stroke(color, sw), diodo(P(x, (yn + yi) / 2 - 0.05), 0.34, color, sw),
                 Dot(P(x, yi), radius=0.035, color=color))
        # tramos del diodo a la pierna (se dibujan como un solo conductor vertical con los diodos encima)
    piernas = VGroup()
    for x, yi in zip(xr, ys_in):
        piernas.add(Line(P(x, yp), P(x, yn)).set_stroke(color, sw))
    rect = VGroup(piernas, *[diodo(P(x, (yp + yi) / 2 + 0.02), 0.32, color, sw) for x, yi in zip(xr, ys_in)],
                  *[diodo(P(x, (yn + yi) / 2 - 0.02), 0.32, color, sw) for x, yi in zip(xr, ys_in)],
                  *[Dot(P(x, yi), radius=0.035, color=color) for x, yi in zip(xr, ys_in)])
    # tapar el conductor dentro de los diodos (el símbolo va sobre la línea; aceptable en IEC)
    entradas = VGroup()
    bornes_in = VGroup()
    for k, (x, yi) in enumerate(zip(xr, ys_in)):
        entradas.add(linea_salto(P(-3.85, yi), P(x, yi), xr[:k], color=color, sw=sw))
        bornes_in.add(borne(P(-3.9, yi), f"L{k + 1}", color, LEFT, 10))
    # --- rieles
    riel_p = VGroup(Line(P(-3.15, yp), P(-1.85, yp)), Line(P(-1.15, yp), P(3.23, yp))).set_stroke(color, sw)
    riel_n = VGroup(Line(P(-3.15, yn), P(-1.85, yn)), Line(P(-1.15, yn), P(3.23, yn))).set_stroke(color, sw)
    # --- precarga (+) con contacto de bypass K1
    r_pre = resistencia_sim(P(-1.85, yp), P(-1.15, yp), color, sw, 0.13)
    k1 = VGroup(Line(P(-1.95, yp), P(-1.95, yp + 0.4)), Line(P(-1.05, yp + 0.4), P(-1.05, yp))).set_stroke(color, sw)
    k1c = contacto_no_h(P(-1.95, yp + 0.4), P(-1.05, yp + 0.4), color, sw)
    k1_et = T("K1", 9, color, "HEAVY").move_to(P(-1.5, yp + 0.72))
    r_et = T("R pre", 8, color, "BOLD").move_to(P(-1.5, yp - 0.2))
    pre = VGroup(r_pre, k1, k1c, k1_et, r_et, Dot(P(-1.95, yp), radius=0.03, color=color), Dot(P(-1.05, yp), radius=0.03, color=color))
    # --- reactor DC (−), opcional
    l_dc = bobina_l(P(-1.85, yn), P(-1.15, yn), color, sw)
    l_et = T("L DC", 8, color, "BOLD").move_to(P(-1.5, yn - 0.22))
    # --- capacitores en serie + resistencias de equilibrio
    xc = -0.65
    caps = VGroup(Line(P(xc, yp), P(xc, 0.75)), Line(P(xc, 0.6), P(xc, -0.6)), Line(P(xc, -0.75), P(xc, yn))).set_stroke(color, sw)
    caps.add(cap_pol(P(xc, 0.68), 0.36, color, sw), cap_pol(P(xc, -0.68), 0.36, color, sw), Dot(P(xc, 0), radius=0.03, color=color))
    xrb = -0.25
    rbal = VGroup(resistencia_sim(P(xrb, yp), P(xrb, 0), color, sw, 0.11), resistencia_sim(P(xrb, 0), P(xrb, yn), color, sw, 0.11), Line(P(xc, 0), P(xrb, 0)).set_stroke(color, sw))
    c_et = T("C", 9, color, "HEAVY").move_to(P(xc - 0.3, 0.68))
    bus = VGroup(caps, rbal, c_et)
    # --- chopper de frenado
    xb = 0.35
    rbr = resistencia_sim(P(xb, yp), P(xb, 0.2), color, sw, 0.12)
    q7 = igbt(P(xb, -0.55), 0.55, color, sw)
    chop = VGroup(rbr, Line(P(xb, 0.2), P(xb, -0.28)).set_stroke(color, sw), q7, Line(P(xb, -0.83), P(xb, yn)).set_stroke(color, sw),
                  Dot(P(xb, 0.2), radius=0.03, color=color), Line(P(xb, 0.2), P(xb + 0.3, 0.2)).set_stroke(color, sw),
                  borne(P(xb + 0.36, 0.2), "BR", "#FDB022", RIGHT, 8), T("R fr", 8, color, "BOLD").move_to(P(xb - 0.32, 0.78)))
    bornes_bus = VGroup(borne(P(0.0, yp + 0.0), "+", "#FF6B6B", UP, 10), borne(P(0.0, yn), "−", "#7AA7FF", DOWN, 10))
    # --- inversor
    xi = [1.05, 2.0, 2.95]
    ys_out = [0.42, 0.0, -0.42]
    inv = VGroup(); qs = []; ds = []
    for k, (x, yo) in enumerate(zip(xi, ys_out)):
        qa = igbt(P(x, (yp + yo) / 2), 0.55, color, sw)
        qb = igbt(P(x, (yn + yo) / 2), 0.55, color, sw)
        ya, yb = (yp + yo) / 2, (yn + yo) / 2
        leg = VGroup(Line(P(x, yp), P(x, ya + 0.275)), Line(P(x, ya - 0.275), P(x, yb + 0.275)), Line(P(x, yb - 0.275), P(x, yn))).set_stroke(color, sw)
        xd = x + 0.28
        da = VGroup(Line(P(x, ya + 0.3), P(xd, ya + 0.3)), Line(P(xd, ya + 0.3), P(xd, ya + 0.17)), Line(P(xd, ya - 0.17), P(xd, ya - 0.3)), Line(P(xd, ya - 0.3), P(x, ya - 0.3))).set_stroke(color, sw * 0.8)
        db = VGroup(Line(P(x, yb + 0.3), P(xd, yb + 0.3)), Line(P(xd, yb + 0.3), P(xd, yb + 0.17)), Line(P(xd, yb - 0.17), P(xd, yb - 0.3)), Line(P(xd, yb - 0.3), P(x, yb - 0.3))).set_stroke(color, sw * 0.8)
        dda = diodo(P(xd, ya), 0.3, color, sw * 0.8); ddb = diodo(P(xd, yb), 0.3, color, sw * 0.8)
        inv.add(leg, qa, qb, da, db, dda, ddb, Dot(P(x, yo), radius=0.035, color=color))
        qs.append((qa, qb)); ds.append((dda, ddb))
        n = 2 * k + 1
        inv.add(T(f"Q{n}", 7, color, "BOLD").move_to(P(x - 0.38, ya + 0.22)), T(f"Q{n + 1}", 7, color, "BOLD").move_to(P(x - 0.38, yb + 0.22)))
    salidas = VGroup()
    bornes_out = VGroup()
    for k, (x, yo, n) in enumerate(zip(xi, ys_out, "UVW")):
        cruces = [xx for xx in xi[k + 1:]] + [xx + 0.28 for xx in xi[k + 1:]]
        salidas.add(linea_salto(P(x, yo), P(3.62, yo), cruces, color=color, sw=sw))
        bornes_out.add(borne(P(3.67, yo), n, color, UP, 8))
    m = motor_sim(P(4.2, 0.0), 0.32, color, sw)
    al_m = VGroup(*[Line(P(3.72, yo), m[0].point_at_angle(np.pi - np.arcsin(yo / 0.32) if abs(yo) < 0.32 else np.pi)).set_stroke(color, sw) for yo in ys_out])
    g.add(entradas, bornes_in, rect, riel_p, riel_n, pre, l_dc, l_et, bus, chop, bornes_bus, inv, salidas, bornes_out, al_m, m)
    g.rect, g.pre, g.k1c, g.bus, g.chop, g.inv, g.qs, g.ds, g.motor = rect, pre, k1c, bus, chop, inv, qs, ds, m
    g.ldc = VGroup(l_dc, l_et)
    g.xr, g.xi, g.yp, g.yn, g.ys_out, g.xc, g.xb = xr, xi, yp, yn, ys_out, xc, xb
    return g

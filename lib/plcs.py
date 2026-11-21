"""PLC, fuentes e instrumentos. En los PLC se CONSERVA la marca y el modelo (pedido del usuario: se trabaja sobre ese modelo).
Medidas de las hojas de datos oficiales."""
from equipos import *


def _bornera_fila(nombres, k, y, x0, paso, lado, g, b, w=6.2, h=7.0, h_txt=1.9):
    for i, n in enumerate(nombres):
        if n is None:
            continue
        bo = Borne(n, k, w=w, h=h, r=2.1, lado=lado, h_txt=h_txt).move_to([(x0 + i * paso) * k, y * k, 0])
        g.add(bo)
        b[n if n not in b else n + "_"] = bo


def logo8(k=K0, ref="A1"):
    """LOGO! 8 12/24RCE: 71,5 × 90 mm. Arriba: L+ M I1…I8. Abajo: Q1 (1 2) Q2 (1 2) Q3 (1 2) Q4 (1 2).
    Frente: display, 4 teclas de cursor, ESC y OK, puerto Ethernet."""
    W, H = 71.5, 90
    g = VGroup()
    cu = caja(W, H, k, CUERPO)
    g.add(cu)
    g.add(Rectangle(width=W * k, height=16 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, (H / 2 - 8) * k, 0]),
          Rectangle(width=W * k, height=16 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, (-H / 2 + 8) * k, 0]),
          caja(W, H, k, CUERPO).set_fill(opacity=0))
    b = {}
    _bornera_fila(["L+", "M", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8"], k, H / 2 - 9, -W / 2 + 4.6, 6.9, DOWN, g, b)
    sal = []
    for q in range(1, 5):
        sal += [f"Q{q}.1", f"Q{q}.2"]
    for i, n in enumerate(sal):
        x = -W / 2 + 6 + i * 8.4
        bo = Borne(n.split(".")[1], k, w=6.2, h=7, r=2.1, lado=UP, h_txt=1.9).move_to([x * k, (-H / 2 + 9) * k, 0])
        g.add(bo)
        b[n] = bo
    for q in range(4):
        x = -W / 2 + 6 + (2 * q + 0.5) * 8.4
        g.add(txt(f"Q{q + 1}", 1.9 * k, TXT_EQ).move_to([x * k, (-H / 2 + 21) * k, 0]))
    fr = caja(W - 4, 50, k, CUERPO_CL, r=1).move_to([0, 0, 0])
    disp = RoundedRectangle(width=30 * k, height=20 * k, corner_radius=1 * k, stroke_color=BORDE, stroke_width=1).set_fill("#B8D8C4", 1).move_to([-12 * k, 4 * k, 0])
    g.add(fr, disp, txt("SIEMENS", 2.6 * k, TXT_EQ).move_to([-12 * k, 19 * k, 0]), txt("LOGO!", 3.4 * k, TXT_EQ).move_to([14 * k, 19 * k, 0]),
          txt("12/24RCE", 1.8 * k, TXT_EQ).move_to([-12 * k, -11 * k, 0]))
    for dx, dy in ((0, 5), (0, -5), (-5, 0), (5, 0)):
        g.add(RoundedRectangle(width=4.6 * k, height=4.6 * k, corner_radius=0.6 * k, stroke_color=BORDE, stroke_width=0.8).set_fill("#4A5462", 1).move_to([(15 + dx) * k, (4 + dy) * k, 0]))
    for x, t in ((9, "ESC"), (21, "OK")):
        bt = RoundedRectangle(width=6.4 * k, height=4.4 * k, corner_radius=0.6 * k, stroke_color=BORDE, stroke_width=0.8).set_fill("#4A5462", 1).move_to([x * k, -8 * k, 0])
        g.add(bt, txt(t, 1.5 * k, TXT_EQ).move_to(bt))
    g.add(RoundedRectangle(width=11 * k, height=8 * k, corner_radius=0.6 * k, stroke_color=BORDE, stroke_width=0.8).set_fill("#1F2329", 1).move_to([-26 * k, -16 * k, 0]),
          txt("LAN", 1.5 * k, TXT_EQ).move_to([-26 * k, -11 * k, 0]))
    g.add(txt(f"-{ref}", 2.8 * k, TXT_EQ).move_to([22 * k, -18 * k, 0]))
    g.b, g.disp, g.k = b, disp, k
    return g


def logo_power(k=K0, ref="T1"):
    """LOGO!Power 24 V 1,3 A: 36 × 90 mm. Arriba L N, abajo + + − −. LED DC OK y potenciómetro."""
    W, H = 36, 90
    g = VGroup(caja(W, H, k, CUERPO))
    g.add(Rectangle(width=W * k, height=16 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, (H / 2 - 8) * k, 0]),
          Rectangle(width=W * k, height=16 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, (-H / 2 + 8) * k, 0]))
    b = {}
    _bornera_fila(["L", "N"], k, H / 2 - 9, -6, 12, DOWN, g, b)
    _bornera_fila(["+", "+ ", "−", "− "], k, -H / 2 + 9, -12.6, 8.4, UP, g, b)
    fr = caja(W - 4, 50, k, CUERPO_CL, r=1)
    g.add(fr, txt("SIEMENS", 2.0 * k, TXT_EQ).move_to([0, 18 * k, 0]), txt("LOGO!Power", 2.0 * k, TXT_EQ).move_to([0, 13 * k, 0]),
          txt("24 V · 1,3 A", 1.7 * k, TXT_EQ).move_to([0, 8 * k, 0]))
    led = Circle(radius=1.4 * k, stroke_width=0).set_fill("#1E4D2E", 1).move_to([-7 * k, -6 * k, 0])
    pot = VGroup(Circle(radius=2.4 * k, stroke_color=BORDE, stroke_width=1).set_fill("#E4E7EC", 1), Line(LEFT * 1.8 * k, RIGHT * 1.8 * k).set_stroke(TXT_OS, 1.4)).move_to([7 * k, -6 * k, 0])
    g.add(led, txt("DC OK", 1.4 * k, TXT_EQ).next_to(led, DOWN, buff=0.7 * k), pot, txt(f"-{ref}", 2.6 * k, TXT_EQ).move_to([0, -17 * k, 0]))
    g.b, g.led, g.k = b, led, k
    return g


def cpu1212(k=K0, ref="A1"):
    """S7-1200 CPU 1212C AC/DC/RLY: 90 × 100 mm. Arriba: L1 N ⏚ L+ M 1M .0….7 2M 0 1. Abajo: 1L .0 .1 .2 .3 2L .4 .5.
    LEDs RUN/STOP, ERROR, MAINT; LEDs de E/S; puerto PROFINET."""
    W, H = 90, 100
    g = VGroup(caja(W, H, k, CUERPO))
    g.add(Rectangle(width=W * k, height=14 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([0, (H / 2 - 7) * k, 0]),
          Rectangle(width=50 * k, height=14 * k, stroke_width=0).set_fill(BORNERA, 1).move_to([18 * k, (-H / 2 + 7) * k, 0]))
    b = {}
    arriba = ["L1", "N", "PE", "L+", "M", "1M", "I.0", "I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7", "2M", "AI0", "AI1"]
    for i, n in enumerate(arriba):
        x = -W / 2 + 3.2 + i * 5.05
        bo = Borne(n.replace("I.", ".").replace("AI", ""), k, w=4.6, h=6, r=1.8, lado=DOWN, h_txt=1.5).move_to([x * k, (H / 2 - 5) * k, 0])
        g.add(bo)
        b[n] = bo
    abajo = ["1L", "Q.0", "Q.1", "Q.2", "Q.3", "2L", "Q.4", "Q.5"]
    for i, n in enumerate(abajo):
        x = -4 + i * 6
        bo = Borne(n.replace("Q.", "."), k, w=5, h=6, r=1.9, lado=UP, h_txt=1.5).move_to([x * k, (-H / 2 + 5) * k, 0])
        g.add(bo)
        b[n] = bo
    fr = caja(W - 6, 60, k, CUERPO_CL, r=1).move_to([0, 0, 0])
    tapa = caja(30, 40, k, CUERPO, r=1).move_to([-8 * k, 0, 0])
    g.add(fr, tapa, txt("SIEMENS", 2.6 * k, TXT_EQ).move_to([-27 * k, 25 * k, 0]), txt("CPU 1212C", 2.4 * k, TXT_EQ).move_to([28 * k, 6 * k, 0]),
          txt("AC/DC/RLY", 2.0 * k, TXT_EQ).move_to([28 * k, 2 * k, 0]))
    for i, t in enumerate(("RUN/STOP", "ERROR", "MAINT")):
        g.add(Rectangle(width=2.2 * k, height=1.4 * k, stroke_width=0).set_fill("#98A2B3", 1).move_to([-40 * k, (16 - 4 * i) * k, 0]), txt(t, 1.1 * k, TXT_EQ).move_to([-35 * k, (16 - 4 * i) * k, 0]))
    for j, n in enumerate((8, 6)):
        for i in range(n):
            g.add(Rectangle(width=2 * k, height=1.4 * k, stroke_width=0).set_fill("#98A2B3", 1).move_to([(14 + 3.2 * i) * k, (20 - 30 * j) * k, 0]))
        g.add(txt("DI a" if j == 0 else "DQ a", 1.2 * k, TXT_EQ).move_to([(14 + 3.2 * n + 4) * k, (20 - 30 * j) * k, 0]))
    g.add(RoundedRectangle(width=10 * k, height=8 * k, corner_radius=0.5 * k, stroke_color=BORDE, stroke_width=0.8).set_fill("#1F2329", 1).move_to([-33 * k, -38 * k, 0]),
          txt("X1 P1", 1.3 * k, TXT_EQ).move_to([-33 * k, -32 * k, 0]), txt(f"-{ref}", 2.8 * k, TXT_EQ).move_to([28 * k, -14 * k, 0]))
    g.b, g.k = b, k
    return g


def multimetro(k=K0, lectura="0.000"):
    """Multímetro digital (estilo de la referencia del usuario): carcasa amarilla, display, selector, bornes COM y V/Ω."""
    W, H = 90, 180
    g = VGroup(RoundedRectangle(width=W * k, height=H * k, corner_radius=12 * k, stroke_color="#7A5A10", stroke_width=2).set_fill("#F5B800", 1),
               RoundedRectangle(width=(W - 12) * k, height=(H - 12) * k, corner_radius=8 * k, stroke_width=0).set_fill("#2B2F36", 1))
    disp = RoundedRectangle(width=64 * k, height=34 * k, corner_radius=3 * k, stroke_width=0).set_fill("#C9D8C5", 1).move_to([0, 52 * k, 0])
    dig = txt(lectura, 13 * k, TXT_OS).move_to(disp)
    sel = Circle(radius=22 * k, stroke_color="#101828", stroke_width=2).set_fill("#3A414C", 1).move_to([0, 0, 0])
    man = RoundedRectangle(width=8 * k, height=38 * k, corner_radius=3 * k, stroke_width=0).set_fill("#101828", 1).rotate(-PI / 5).move_to(sel)
    pos = VGroup(*[txt(t, 4 * k, WHITE).move_to(sel.get_center() + 30 * k * np.array([np.cos(a), np.sin(a), 0]))
                   for t, a in (("OFF", PI * 0.9), ("V~", PI * 0.62), ("V⎓", PI * 0.38), ("Ω", PI * 0.1), ("A", -PI * 0.15))])
    com = Circle(radius=7 * k, stroke_color="#101828", stroke_width=2).set_fill("#101828", 1).move_to([-18 * k, -62 * k, 0])
    vo = Circle(radius=7 * k, stroke_color="#7A271A", stroke_width=2).set_fill("#B42318", 1).move_to([18 * k, -62 * k, 0])
    g.add(disp, dig, sel, man, pos, com, vo, txt("COM", 4 * k, WHITE).next_to(com, UP, buff=2 * k), txt("VΩ", 4 * k, WHITE).next_to(vo, UP, buff=2 * k),
          logo_marca(8 * k).move_to([0, 75 * k, 0]).set_opacity(0) if False else VGroup())
    g.dig, g.jack_com, g.jack_v, g.man, g.k = dig, com, vo, man, k
    return g


def pinza(k=K0, lectura="0.0"):
    """Pinza amperimétrica: mordaza abierta arriba, display y selector."""
    g = VGroup()
    mord = VGroup(Arc(radius=34 * k, start_angle=-PI * 0.1, angle=PI * 1.2).set_stroke("#B42318", 14 * k * 18),).move_to([0, 70 * k, 0])
    cuerpo = RoundedRectangle(width=70 * k, height=130 * k, corner_radius=10 * k, stroke_color="#7A271A", stroke_width=2).set_fill("#B42318", 1).move_to([0, -30 * k, 0])
    frente = RoundedRectangle(width=58 * k, height=112 * k, corner_radius=6 * k, stroke_width=0).set_fill("#2B2F36", 1).move_to(cuerpo)
    disp = RoundedRectangle(width=48 * k, height=26 * k, corner_radius=2 * k, stroke_width=0).set_fill("#C9D8C5", 1).move_to([0, -2 * k, 0])
    dig = txt(lectura, 10 * k, TXT_OS).move_to(disp)
    sel = Circle(radius=14 * k, stroke_color="#101828", stroke_width=2).set_fill("#3A414C", 1).move_to([0, -38 * k, 0])
    g.add(mord, cuerpo, frente, disp, dig, sel, txt("A~", 4 * k, WHITE).move_to([16 * k, -26 * k, 0]))
    g.dig, g.k = dig, k
    return g

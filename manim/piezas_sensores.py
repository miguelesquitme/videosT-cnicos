"""Piezas detalladas de sensores de proximidad (vista lateral, sin marcas). Referencias: sensores M18 de 3 hilos
(cuerpo roscado de latón niquelado, 2 tuercas hexagonales con arandela, cara activa de plástico, LED anular trasero y
conector M12 de 4 pines; capacitivos con potenciómetro de sensibilidad trasero), núcleo de ferrita tipo copa.
"""
from manim import *
import numpy as np
from comun_e import T

P = lambda x, y: np.array([x, y, 0.0])
NIQ = "#C9CED6"; NIQ_O = "#8A929C"; NIQ_OO = "#5B6472"


def _tuerca_lado(x, h, w=0.32, color=NIQ):
    """Tuerca hexagonal vista de lado (3 caras visibles) + arandela."""
    cuerpo = Rectangle(width=w, height=h, stroke_color=NIQ_OO, stroke_width=1.4).set_fill(color, 1).move_to(P(x, 0))
    caras = VGroup(Line(P(x - w / 2, h * 0.22), P(x + w / 2, h * 0.22)), Line(P(x - w / 2, -h * 0.22), P(x + w / 2, -h * 0.22))).set_stroke(NIQ_OO, 1.2)
    luz = Rectangle(width=w, height=h * 0.42, stroke_width=0).set_fill(WHITE, 0.35).move_to(P(x, 0.0))
    cham = VGroup(Line(P(x - w / 2, h / 2), P(x - w / 2 + 0.05, h / 2 - 0.05)), Line(P(x + w / 2, h / 2), P(x + w / 2 - 0.05, h / 2 - 0.05)),
                  Line(P(x - w / 2, -h / 2), P(x - w / 2 + 0.05, -h / 2 + 0.05)), Line(P(x + w / 2, -h / 2), P(x + w / 2 - 0.05, -h / 2 + 0.05))).set_stroke(NIQ_OO, 1)
    arand = Rectangle(width=0.06, height=h * 0.86, stroke_color=NIQ_OO, stroke_width=1).set_fill("#DDE1E7", 1).move_to(P(x + w / 2 + 0.03, 0))
    return VGroup(cuerpo, luz, caras, cham, arand)


def sensor_m18(s=1.0, tipo="inductivo", cara_color="#F79009", led_on=False, rotulo=None):
    """Sensor M18 de 3 hilos, vista lateral, cara activa hacia la DERECHA. Largo ≈ 4,6; diámetro 1,0 (a s=1)."""
    g = VGroup()
    d = 1.0
    x0, x1 = -1.75, 1.75  # cuerpo roscado
    cuerpo = Rectangle(width=x1 - x0, height=d, stroke_color=NIQ_OO, stroke_width=1.5).set_fill(NIQ, 1)
    luz = Rectangle(width=x1 - x0, height=d * 0.25, stroke_width=0).set_fill(WHITE, 0.45).move_to(P(0, d * 0.18))
    sombra = Rectangle(width=x1 - x0, height=d * 0.22, stroke_width=0).set_fill("#6B7280", 0.35).move_to(P(0, -d * 0.36))
    rosca = VGroup(*[Line(P(x, -d / 2), P(x + 0.06, d / 2)).set_stroke(NIQ_OO, 0.9, 0.85) for x in np.arange(x0 + 0.03, x1 - 0.06, 0.075)])
    dientes = VGroup(*[VGroup(Line(P(x, d / 2), P(x + 0.0375, d / 2 + 0.035)), Line(P(x + 0.0375, d / 2 + 0.035), P(x + 0.075, d / 2)),
                              Line(P(x, -d / 2), P(x + 0.0375, -d / 2 - 0.035)), Line(P(x + 0.0375, -d / 2 - 0.035), P(x + 0.075, -d / 2))).set_stroke(NIQ_OO, 0.9)
                     for x in np.arange(x0, x1 - 0.07, 0.075)])
    g.add(cuerpo, luz, sombra, rosca, dientes)
    # rotulado grabado
    rot = rotulo or ("M18 · Sn 8 mm · PNP NA · 10–30 V DC" if tipo == "inductivo" else "M18 · Sn 1–8 mm (ajust.) · PNP NA · 10–30 V DC")
    if tipo == "inductivo" and rotulo is None:
        rr = VGroup(T("M18 · Sn 8 mm", 5.6, "#2B3038", "HEAVY"), T("PNP NA · 10–30 V DC", 4.8, "#3B4250", "BOLD")).arrange(DOWN, buff=0.04)
    elif rotulo is None:
        rr = VGroup(T("M18 · CAPACITIVO", 5.6, "#2B3038", "HEAVY"), T("Sn 8 mm ajust. · PNP NA", 4.8, "#3B4250", "BOLD")).arrange(DOWN, buff=0.04)
    else:
        rr = T(rotulo, 5.2, "#3B4250", "BOLD")
    g.add(rr.move_to(P(0.05, 0.0)))
    # tuercas
    tu = VGroup(_tuerca_lado(-0.95, 1.38), _tuerca_lado(1.05, 1.38))
    g.add(tu)
    # cara activa (no enrasada: sobresale)
    cara = RoundedRectangle(width=0.42, height=0.9, corner_radius=0.1, stroke_color="#7A3E00" if tipo == "inductivo" else "#1D2939", stroke_width=1.4).set_fill(cara_color, 1).move_to(P(x1 + 0.17, 0))
    cara_l = Rectangle(width=0.08, height=0.78, stroke_width=0).set_fill(WHITE, 0.3).move_to(P(x1 + 0.1, 0.0))
    g.add(cara, cara_l)
    # parte trasera: tapa con LED anular y potenciómetro (capacitivo)
    tapa = Rectangle(width=0.42, height=0.94, stroke_color="#1D2939", stroke_width=1.4).set_fill("#344054", 1).move_to(P(x0 - 0.21, 0))
    led = Rectangle(width=0.1, height=0.94, stroke_width=0).set_fill("#FDB022" if led_on else "#8A6A1E", 1).move_to(P(x0 - 0.05, 0))
    g.add(tapa, led)
    pot = VGroup()
    if tipo == "capacitivo":
        pot = VGroup(Circle(radius=0.11, stroke_color="#101828", stroke_width=1.2).set_fill("#98A2B3", 1).move_to(P(x0 - 0.24, 0.62)),
                     Line(P(x0 - 0.3, 0.62), P(x0 - 0.18, 0.62)).set_stroke("#101828", 1.6),
                     Rectangle(width=0.16, height=0.18, stroke_width=0).set_fill("#344054", 1).move_to(P(x0 - 0.24, 0.5)))
        g.add(pot)
    # conector M12
    m12 = Rectangle(width=0.5, height=0.62, stroke_color="#475467", stroke_width=1.2).set_fill(NIQ_O, 1).move_to(P(x0 - 0.67, 0))
    knurl = VGroup(*[Line(P(x, -0.31), P(x, 0.31)).set_stroke(NIQ_OO, 0.8) for x in np.linspace(x0 - 0.9, x0 - 0.44, 9)])
    cuerpo_c = Rectangle(width=0.55, height=0.52, stroke_color="#101828", stroke_width=1).set_fill("#2B3038", 1).move_to(P(x0 - 1.2, 0))
    cable = Rectangle(width=0.9, height=0.3, stroke_width=0).set_fill("#2B3038", 1).move_to(P(x0 - 1.9, 0))
    g.add(cuerpo_c, cable, m12, knurl)
    g.scale(s)
    g.cara, g.led, g.tuercas, g.pot = cara, led, tu, pot
    return g


def corte_inductivo(s=1.0):
    """Corte longitudinal del sensor inductivo: núcleo de ferrita tipo copa con bobina, PCB con oscilador,
    demodulador, comparador con histéresis y etapa de salida, LED, resina. Cara a la DERECHA. Largo ≈ 7, alto ≈ 2."""
    g = VGroup()
    h = 1.9
    pared = 0.12
    funda = Rectangle(width=6.4, height=h, stroke_color=NIQ_OO, stroke_width=2).set_fill(NIQ, 1)
    interior = Rectangle(width=6.4 - 0.1, height=h - 2 * pared, stroke_width=0).set_fill("#F6E7C1", 1)  # resina
    textura = VGroup(*[Dot(P(np.random.uniform(-3.1, 3.1), np.random.uniform(-0.75, 0.75)), radius=0.012, color="#D9C38A") for _ in range(160)])
    g.add(funda, interior, textura)
    # cara y núcleo
    cara = Rectangle(width=0.3, height=h - 0.1, stroke_color="#7A3E00", stroke_width=1.5).set_fill("#F79009", 1).move_to(P(3.35, 0))
    fer = "#3A3F47"
    nucleo = VGroup(Rectangle(width=0.18, height=1.5, stroke_width=0).set_fill(fer, 1).move_to(P(2.42, 0)),  # placa trasera
                    Rectangle(width=0.62, height=0.16, stroke_width=0).set_fill(fer, 1).move_to(P(2.82, 0.67)),  # pared exterior sup
                    Rectangle(width=0.62, height=0.16, stroke_width=0).set_fill(fer, 1).move_to(P(2.82, -0.67)),
                    Rectangle(width=0.62, height=0.22, stroke_width=0).set_fill(fer, 1).move_to(P(2.82, 0)))  # poste central
    bob = VGroup()
    for yc in (0.34, -0.34):
        for i in range(4):
            for j in range(3):
                p = P(2.6 + i * 0.13, yc - 0.13 + j * 0.13)
                bob.add(Circle(radius=0.055, stroke_color="#7A3B12", stroke_width=0.8).set_fill("#C8743F", 1).move_to(p))
    g.add(cara, nucleo, bob)
    # PCB y componentes
    pcb = Rectangle(width=4.6, height=0.14, stroke_width=0).set_fill("#166534", 1).move_to(P(-0.1, -0.12))
    comps = VGroup()
    etiquetas = []
    for x, w, n in ((1.55, 0.55, "OSC"), (0.75, 0.55, "DEMOD"), (-0.1, 0.55, "COMP"), (-1.0, 0.55, "SALIDA")):
        ic = Rectangle(width=w, height=0.26, stroke_color="#101828", stroke_width=1).set_fill("#1F2430", 1).move_to(P(x, 0.08))
        pines = VGroup(*[Line(P(x - w / 2 + 0.06 + k * 0.1, -0.05), P(x - w / 2 + 0.06 + k * 0.1, -0.0)).set_stroke(NIQ_O, 1.4) for k in range(5)])
        comps.add(ic, pines, T(n, 5.5, "#E4E7EC", "HEAVY").move_to(ic))
        etiquetas.append(ic)
    smd = VGroup(*[Rectangle(width=0.12, height=0.07, stroke_width=0).set_fill(c, 1).move_to(P(x, -0.24)) for x, c in
                   zip(np.linspace(-2.2, 2.0, 14), ["#8A6A1E", "#5B6472"] * 7)])
    alambres = VGroup(Line(P(2.42, 0.4), P(1.9, 0.1)), Line(P(2.42, -0.4), P(1.9, -0.06))).set_stroke("#C8743F", 2)
    led = Rectangle(width=0.12, height=h - 0.2, stroke_width=0).set_fill("#FDB022", 0.85).move_to(P(-2.95, 0))
    cables = VGroup(*[Line(P(-3.2, y), P(-2.4, y)).set_stroke(c, 3) for y, c in ((0.35, "#8B5A2B"), (0.0, "#1D4ED8"), (-0.35, "#101828"))])
    g.add(pcb, smd, comps, alambres, led, cables)
    g.scale(s)
    g.cara, g.nucleo, g.bobina, g.ics, g.led = cara, nucleo, bob, etiquetas, led
    g.cara_x = cara.get_right()[0]
    return g


def placa_metal(material="acero", w=0.3, h=2.2, s=1.0):
    col = {"acero": ("#8A929C", "#5B6472"), "inox": ("#C9CED6", "#8A929C"), "aluminio": ("#D9DEE6", "#98A2B3"),
           "laton": ("#D9B44A", "#9A7B1E"), "cobre": ("#C8743F", "#7A3B12")}[material]
    r = Rectangle(width=w, height=h, stroke_color=col[1], stroke_width=1.5).set_fill(col[0], 1)
    hatch = VGroup(*[Line(P(-w / 2, y), P(w / 2, y + w)).set_stroke(col[1], 0.8, 0.6) for y in np.arange(-h / 2, h / 2 - w, 0.12)])
    return VGroup(r, hatch).scale(s)


def campo_frente(p, n=4, r0=0.25, dr=0.22, color="#0057B8", sw=3, ang=1.6):
    """Lóbulos del campo alterno frente a la cara (arcos)."""
    return VGroup(*[Arc(radius=r0 + dr * k, start_angle=-ang / 2, angle=ang).set_stroke(color, sw, 1 - k * 0.18).move_arc_center_to(p) for k in range(n)])

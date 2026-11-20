"""Piezas gráficas para videos de AUTOMATIZACIÓN INDUSTRIAL (canal @miguelesquit).
Estilo: aparatos realistas (cuerpo gris, bornes con tornillo Phillips, marcas IEC), riel DIN, cables con puntera y
marquilla, símbolos IEC 60617 y colores de conductores NFPA 79 (potencia negro, mando CA rojo, neutro blanco,
tierra verde).
"""
from comun_e import *
from comun_e import _osc, _cla
from taller import P, corriente

GRIS_C = "#D9DDE2"      # cuerpo del aparato
GRIS_B = "#C4C9D0"      # bloque de bornes
GRIS_O = "#4B5563"      # hueco del borne
BANDA = "#1F2430"
PLATA = "#E9ECEF"
BORDE = "#5B6573"
TXT_AP = "#1D2939"      # texto impreso en el aparato
C_POT = "#1B1B1B"       # NFPA 79 13.2.4.3(1): potencia CA, negro
C_MANDO = "#D92D20"     # NFPA 79 13.2.4.3(2): mando CA, rojo
C_NEUTRO = "#F2F4F7"    # NFPA 79 13.2.4.2: puesto a tierra, blanco
C_TIERRA = "#16A34A"    # tierra de equipos, verde
CU = "#C8773A"
AG = "#E4E7EB"          # pastilla de contacto (aleación de plata)


def tx(texto, alto, color=TXT_AP, peso="HEAVY"):
    t = T(texto, 40, color, peso)
    return t.scale_to_fit_height(alto)


# ===================================================================== tornillos y bornes
def tornillo_ph(r=0.16):
    """Tornillo de borne con cabeza Phillips/Pozidriv (como en contactores y guardamotores)."""
    cab = Circle(radius=r, stroke_color=BORDE, stroke_width=1.4).set_fill("#E5E7EB", 1)
    aro = Circle(radius=r * 0.8, stroke_color="#AEB4BF", stroke_width=1.0).set_fill("#F3F4F6", 1)
    w = max(1.4, r * 16)
    cruz = VGroup(Line([-r * 0.55, 0, 0], [r * 0.55, 0, 0]), Line([0, -r * 0.55, 0], [0, r * 0.55, 0])).set_stroke("#4B5563", w)
    cruz.set_cap_style(CapStyleType.ROUND)
    brillo = Arc(radius=r * 0.62, start_angle=PI * 0.6, angle=PI * 0.45).set_stroke(WHITE, max(0.8, r * 10), 0.8)
    return VGroup(VGroup(cab, aro), cruz, brillo)


def borne_pot(c, s=1.0, etiqueta=None, arriba=True):
    """Borne de potencia: hueco oscuro + tornillo; etiqueta impresa debajo (arriba=True) o encima."""
    hueco = RoundedRectangle(width=0.5 * s, height=0.5 * s, corner_radius=0.06 * s, stroke_color="#374151", stroke_width=1.2).set_fill(GRIS_O, 1)
    entrada = RoundedRectangle(width=0.34 * s, height=0.14 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#111827", 1)
    entrada.next_to(hueco, UP if arriba else DOWN, buff=0.03 * s)
    tor = tornillo_ph(0.18 * s)
    g = VGroup(hueco, entrada, tor).move_to(c)
    hueco.move_to(c), tor.move_to(c)
    entrada.next_to(hueco, UP if arriba else DOWN, buff=0.03 * s)
    g.tor, g.entrada = tor, entrada
    if etiqueta:
        e = tx(etiqueta, 0.13 * s).next_to(hueco, DOWN if arriba else UP, buff=0.06 * s)
        g.add(e)
        g.et = e
    return g


def borne_aux(c, s=1.0, etiqueta=None, lado=RIGHT):
    tor = tornillo_ph(0.105 * s).move_to(c)
    marco = RoundedRectangle(width=0.3 * s, height=0.3 * s, corner_radius=0.04 * s, stroke_width=0).set_fill(GRIS_O, 1).move_to(c)
    g = VGroup(marco, tor)
    g.tor = tor
    if etiqueta:
        e = VGroup(*[tx(l, 0.085 * s) for l in etiqueta.split("/")]).arrange(DOWN, buff=0.02 * s, aligned_edge=LEFT)
        e.next_to(marco, lado, buff=0.05 * s)
        g.add(e)
        g.et = e
    return g


# ===================================================================== contactor (vista frontal)
def contactor_frente(s=1.0, ie="18", ref="KM1", aux=("13/NO", "21/NC")):
    """Contactor tripolar de riel DIN, vista frontal, marcado IEC: 1/L1 3/L2 5/L3 · 2/T1 4/T2 6/T3 · A1 A2 · 13-14 NA · 21-22 NC.
    Atributos: .b (dict de bornes), .ind (indicador mecánico que baja al cerrar), .cuerpo."""
    W, H = 2.6 * s, 3.6 * s
    sombra_ = RoundedRectangle(width=W, height=H, corner_radius=0.14 * s, stroke_width=0).set_fill(BLACK, 0.35).shift(RIGHT * 0.07 * s + DOWN * 0.08 * s)
    cuerpo = RoundedRectangle(width=W, height=H, corner_radius=0.14 * s, stroke_color=BORDE, stroke_width=1.6).set_fill(GRIS_C, 1)
    lado = Rectangle(width=0.1 * s, height=H * 0.94, stroke_width=0).set_fill("#B9BEC6", 1).move_to(cuerpo.get_right() + LEFT * 0.08 * s)
    blq_sup = RoundedRectangle(width=W * 0.94, height=0.95 * s, corner_radius=0.06 * s, stroke_color="#9AA1AB", stroke_width=1).set_fill(GRIS_B, 1)
    blq_sup.move_to(cuerpo.get_top() + DOWN * 0.56 * s)
    blq_inf = blq_sup.copy().move_to(cuerpo.get_bottom() + UP * 0.56 * s)
    banda = Rectangle(width=W * 0.94, height=0.3 * s, stroke_width=0).set_fill(BANDA, 1).move_to(cuerpo.get_top() + DOWN * 1.2 * s)
    marca_t = tx(f"{ref}", 0.15 * s, "#F2F4F7").move_to(banda).shift(LEFT * 0.75 * s)
    ie_t = tx(f"{ie} A · AC-3", 0.13 * s, "#F2F4F7").move_to(banda).shift(RIGHT * 0.5 * s)
    g = VGroup(sombra_, cuerpo, lado, blq_sup, blq_inf, banda, marca_t, ie_t)
    b = {}
    xs = [-0.78 * s, 0, 0.78 * s]
    ysup = blq_sup.get_center()[1] + 0.12 * s
    yinf = blq_inf.get_center()[1] - 0.12 * s
    for x, n in zip(xs, ("1/L1", "3/L2", "5/L3")):
        bb = borne_pot([x, ysup, 0], s, n, arriba=True)
        b[n] = bb
        g.add(bb)
    for x, n in zip(xs, ("2/T1", "4/T2", "6/T3")):
        bb = borne_pot([x, yinf, 0], s, n, arriba=False)
        b[n] = bb
        g.add(bb)
    # zona central: auxiliares arriba (13, 21, A1), indicador, auxiliares abajo (14, 22, A2)
    y1 = banda.get_center()[1] - 0.36 * s
    y2 = blq_inf.get_top()[1] + 0.24 * s
    xa = [-0.95 * s, -0.25 * s, 0.6 * s]
    sup = [aux[0], aux[1], "A1"]
    inf = [aux[0].replace("3/", "4/").replace("1/", "2/").replace("13", "14").replace("21", "22"),
           aux[1].replace("21", "22").replace("13", "14"), "A2"]
    inf = ["14/NO", "22/NC", "A2"] if aux == ("13/NO", "21/NC") else inf
    for x, n in zip(xa, sup):
        bb = borne_aux([x, y1, 0], s, n)
        b[n.split("/")[0]] = bb
        g.add(bb)
    for x, n in zip(xa, inf):
        bb = borne_aux([x, y2, 0], s, n)
        b[n.split("/")[0]] = bb
        g.add(bb)
    ventana = RoundedRectangle(width=1.5 * s, height=0.42 * s, corner_radius=0.05 * s, stroke_color="#9AA1AB", stroke_width=1).set_fill("#F8FAFC", 1)
    ventana.move_to([0.05 * s, (y1 + y2) / 2, 0])
    ind = RoundedRectangle(width=0.5 * s, height=0.2 * s, corner_radius=0.03 * s, stroke_width=0).set_fill("#9CA3AF", 1).move_to(ventana.get_center() + UP * 0.07 * s)
    marcas_ind = VGroup(tx("O", 0.1 * s, "#667085").next_to(ventana, LEFT, buff=0.05 * s).shift(UP * 0.06 * s),
                        tx("I", 0.1 * s, "#667085").next_to(ventana, LEFT, buff=0.05 * s).shift(DOWN * 0.08 * s))
    g.add(ventana, ind, marcas_ind)
    g.b, g.ind, g.cuerpo, g.ventana = b, ind, cuerpo, ventana
    g.s = s
    return g


def cerrar_indicador(ct, cerrar=True):
    d = (-0.13 if cerrar else 0.13) * ct.s
    return ct.ind.animate.shift(UP * d).set_fill("#12B76A" if cerrar else "#9CA3AF", 1)


def riel_din(largo=10.0, s=1.0):
    r = Rectangle(width=largo, height=0.7 * s, stroke_color="#7B8491", stroke_width=1.4).set_fill("#B8BEC8", 1)
    pestanas = VGroup(Rectangle(width=largo, height=0.08 * s, stroke_width=0).set_fill("#9AA2AD", 1).move_to(r.get_top() + DOWN * 0.04 * s),
                      Rectangle(width=largo, height=0.08 * s, stroke_width=0).set_fill("#9AA2AD", 1).move_to(r.get_bottom() + UP * 0.04 * s))
    ran = VGroup(*[RoundedRectangle(width=0.5 * s, height=0.2 * s, corner_radius=0.1 * s, stroke_width=0).set_fill("#6B7280", 1).move_to([x, 0, 0])
                   for x in np.arange(-largo / 2 + 0.6 * s, largo / 2 - 0.3 * s, 1.0 * s)])
    return VGroup(r, pestanas, ran)


# ===================================================================== cables con puntera y marquilla
def ruta_redondeada(pts, r=0.25):
    pts = [np.array(p, float) for p in pts]
    m = VMobject()
    m.start_new_path(pts[0])
    for i in range(1, len(pts) - 1):
        a, c, b = pts[i - 1], pts[i], pts[i + 1]
        d1 = (c - a) / (np.linalg.norm(c - a) + 1e-9)
        d2 = (b - c) / (np.linalg.norm(b - c) + 1e-9)
        rr = min(r, np.linalg.norm(c - a) / 2, np.linalg.norm(b - c) / 2)
        p1, p2 = c - d1 * rr, c + d2 * rr
        m.add_line_to(p1)
        m.add_quadratic_bezier_curve_to(c, p2)
    m.add_line_to(pts[-1])
    return m


def cable(pts, color=C_POT, w=11, r=0.3, etiqueta=None, pos_et=0.0, et_color="#FFFFFF", puntera=True, borde="#8F9AC8"):
    """Cable con forro (borde claro para el fondo azul), puntera metálica en el extremo inicial y marquilla con texto.
    pts[0] es el punto del borne (donde entra la puntera)."""
    pts = [np.array(p, float) for p in pts]
    ruta = ruta_redondeada(pts, r)
    fondo = ruta.copy().set_stroke(borde, w + 4)
    cuerpo = ruta.copy().set_stroke(color, w)
    brillo = ruta.copy().set_stroke(WHITE, max(1.0, w * 0.18), 0.22 if color != C_NEUTRO else 0.0)
    for x in (fondo, cuerpo, brillo):
        x.set_cap_style(CapStyleType.ROUND)
    g = VGroup(fondo, cuerpo, brillo)
    d = pts[1] - pts[0]
    d = d / (np.linalg.norm(d) + 1e-9)
    an = w / 100
    if puntera:
        pun = Polygon(pts[0] - np.array([-d[1], d[0], 0]) * an * 0.42, pts[0] + np.array([-d[1], d[0], 0]) * an * 0.42,
                      pts[0] + d * 0.22 + np.array([-d[1], d[0], 0]) * an * 0.42, pts[0] + d * 0.22 - np.array([-d[1], d[0], 0]) * an * 0.42,
                      stroke_color="#8C939E", stroke_width=1).set_fill("#D5D9DE", 1)
        collar = Polygon(*[pts[0] + d * t + np.array([-d[1], d[0], 0]) * an * sgn * 0.62 for t, sgn in ((0.22, 1), (0.22, -1), (0.36, -1), (0.36, 1))],
                         stroke_width=0).set_fill(color if color not in (C_POT,) else "#3A3F48", 1)
        g.add(pun, collar)
    if etiqueta:
        c = pts[0] + d * (0.62 + pos_et)
        ang = np.arctan2(d[1], d[0])
        caja = RoundedRectangle(width=0.5, height=an * 1.5, corner_radius=0.03, stroke_color="#98A2B3", stroke_width=0.8).set_fill(et_color, 1)
        t_ = tx(etiqueta, an * 0.95)
        e = VGroup(caja, t_)
        if abs(np.cos(ang)) < 0.5:          # cable vertical: marquilla tipo manga, texto horizontal y legible
            caja.stretch_to_fit_width(max(an * 1.7, t_.width + 0.16)).stretch_to_fit_height(max(0.34, an * 2.2))
        e.move_to(c)
        t_.move_to(caja)
        g.add(e)
    fisico(g)
    g.ruta = ruta
    return g


# ===================================================================== despiece (vista en corte esquemática)
def laminado(w, h, n=9, color="#9AA3AF", borde="#5B6573"):
    base = Rectangle(width=w, height=h, stroke_color=borde, stroke_width=1.4).set_fill(color, 1)
    lin = VGroup(*[Line([x, -h / 2 + 0.03, 0], [x, h / 2 - 0.03, 0]).set_stroke("#6B7280", 0.9) for x in np.linspace(-w / 2 + w / n, w / 2 - w / n, n - 1)])
    return VGroup(base, lin)


def nucleo_E(w=3.2, h=1.5, laminas=True):
    """Circuito magnético fijo (culata) en E, laminado, con espiras de sombra en las columnas laterales."""
    col = "#9AA3AF"
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (w / 2 - 0.42, h / 2), (w / 2 - 0.42, -h / 2 + 0.42), (0.21, -h / 2 + 0.42),
           (0.21, h / 2), (-0.21, h / 2), (-0.21, -h / 2 + 0.42), (-w / 2 + 0.42, -h / 2 + 0.42), (-w / 2 + 0.42, h / 2), (-w / 2, h / 2)]
    e = Polygon(*[P(*p) for p in pts], stroke_color="#5B6573", stroke_width=1.6).set_fill(col, 1)
    g = VGroup(e)
    if laminas:
        for y in np.linspace(-h / 2 + 0.06, -h / 2 + 0.38, 5):
            g.add(Line(P(-w / 2 + 0.04, y), P(w / 2 - 0.04, y)).set_stroke("#6B7280", 0.8))
    anillos = VGroup(*[Rectangle(width=0.2, height=0.12, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to(P(x, h / 2 - 0.06))
                       for x in (-w / 2 + 0.21, w / 2 - 0.21)])
    g.add(anillos)
    g.anillos = anillos
    return g


def armadura_T(w=3.2, h=0.62):
    """Armadura móvil (martillo), laminada, con la columna del portacontactos."""
    a = laminado(w, h, 14)
    return a


def bobina(w=1.7, h=1.05):
    """Bobina en su carrete: bridas blancas y devanado de cobre; bornes A1/A2."""
    carr = VGroup(Rectangle(width=w, height=0.1, stroke_color="#98A2B3", stroke_width=1).set_fill("#F2F4F7", 1).move_to(UP * h / 2),
                  Rectangle(width=w, height=0.1, stroke_color="#98A2B3", stroke_width=1).set_fill("#F2F4F7", 1).move_to(DOWN * h / 2))
    dev = Rectangle(width=w - 0.14, height=h - 0.1, stroke_color="#9A4F1E", stroke_width=1).set_fill(CU, 1)
    esp = VGroup(*[Line(P(-w / 2 + 0.1, y), P(w / 2 - 0.1, y + 0.02)).set_stroke("#9A4F1E", 0.8) for y in np.linspace(-h / 2 + 0.12, h / 2 - 0.12, 8)])
    hueco = Rectangle(width=0.46, height=h - 0.1, stroke_width=0).set_fill("#2A3446", 1)
    return VGroup(dev, esp, hueco, carr)


def resorte(alto=1.0, ancho=0.5, n=7, color="#C7CCD6", w=3):
    pts = [P(0, -alto / 2)]
    for k in range(1, 2 * n):
        pts.append(P(ancho / 2 * (1 if k % 2 else -1), -alto / 2 + alto * k / (2 * n)))
    pts.append(P(0, alto / 2))
    return VMobject().set_points_as_corners(pts).set_stroke(color, w)


def puente_movil(w=2.2):
    barra = RoundedRectangle(width=w, height=0.16, corner_radius=0.04, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1)
    pads = VGroup(*[RoundedRectangle(width=0.26, height=0.08, corner_radius=0.02, stroke_width=0.6, stroke_color="#98A2B3").set_fill(AG, 1)
                    .move_to(P(x, -0.12)) for x in (-w / 2 + 0.2, w / 2 - 0.2)])
    return VGroup(barra, pads)


def contacto_fijo(lado=-1, largo=1.4):
    """Contacto fijo en L con pastilla de plata y su tornillo de borne en el extremo."""
    x0 = lado * 1.1
    tira = VGroup(Rectangle(width=largo, height=0.16, stroke_color="#7A3B12", stroke_width=1).set_fill(CU, 1).move_to(P(x0 + lado * largo / 2 - lado * 0.0, 0)))
    pad = RoundedRectangle(width=0.26, height=0.08, corner_radius=0.02, stroke_width=0.6, stroke_color="#98A2B3").set_fill(AG, 1).move_to(P(x0 - lado * 0.0 + lado * 0.0, 0.12))
    pad.move_to(tira[0].get_edge_center(-lado * RIGHT) + UP * 0.12 + lado * RIGHT * 0.18)
    tor = tornillo_ph(0.15).move_to(tira[0].get_edge_center(lado * RIGHT) + UP * 0.2 - lado * RIGHT * 0.25)
    return VGroup(tira, pad, tor)


def camara_apaga(w=3.2, h=1.25, n=7):
    caja = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color="#4B5563", stroke_width=1.6).set_fill("#3A3F48", 0.92)
    placas = VGroup(*[VGroup(*[Rectangle(width=0.06, height=h * 0.6, stroke_width=0).set_fill("#A7AFBA", 1).move_to(P(x0 + k * 0.1, 0.08))
                               for k in range(n)]) for x0 in (-w / 2 + 0.35, w / 2 - 0.35 - (n - 1) * 0.1)])
    return VGroup(caja, placas)


def portacontactos(h=1.4):
    return VGroup(Rectangle(width=0.36, height=h, stroke_color="#4D7C0F", stroke_width=1.2).set_fill("#A3D977", 1))


def base_contactor(w=3.6, h=0.9):
    cuerpo = Polygon(P(-w / 2, h / 2), P(w / 2, h / 2), P(w / 2, -h / 2), P(-w / 2, -h / 2), stroke_color="#8C939E", stroke_width=1.6).set_fill("#CBD0D7", 1)
    pie = VGroup(*[Rectangle(width=0.5, height=0.18, stroke_width=0).set_fill("#8C939E", 1).move_to(P(x, -h / 2 - 0.09)) for x in (-w / 2 + 0.5, w / 2 - 0.5)])
    return VGroup(cuerpo, pie)


# ===================================================================== símbolos IEC 60617 (trazo de plano)
SIM = "#F2F4F7"
SW = 3.2


def _t(texto, h=0.2, color=SIM):
    return tx(texto, h, color, "BOLD")


def sim_contacto(no=True, contactor=False, interruptor=False, largo=1.0, cerrado=False, color=SIM, n1=None, n2=None):
    """Contacto vertical (de arriba hacia abajo). NA: cuchilla inclinada a la izquierda. NC: con tope.
    contactor=True agrega el semicírculo (IEC 60617 07-13-02); interruptor=True agrega la cruz (función interruptor)."""
    a, b = P(0, largo / 2), P(0, -largo / 2)
    sup = Line(a, P(0, largo * 0.18)).set_stroke(color, SW)
    inf = Line(P(0, -largo * 0.18), b).set_stroke(color, SW)
    piv = P(0, -largo * 0.18)
    if no:
        ang = 0.0 if cerrado else 0.45
        cuch = Line(piv, piv + rotate_vector(UP * largo * 0.42, ang)).set_stroke(color, SW)
        extra = VGroup()
    else:
        ang = 0.0 if not cerrado else -0.45  # aquí cerrado=True significa "accionado" (abierto)
        cuch = Line(piv, piv + rotate_vector(UP * largo * 0.42, -0.3 if not cerrado else 0.45)).set_stroke(color, SW)
        extra = Line(P(0, largo * 0.18), P(largo * 0.16, largo * 0.18)).set_stroke(color, SW)
    g = VGroup(sup, inf, cuch, extra)
    if contactor:
        rr = largo * 0.075
        g.add(Arc(radius=rr, start_angle=-PI / 2, angle=PI, arc_center=P(0, largo * 0.18 + rr)).set_stroke(color, SW * 0.9))
    if interruptor:
        c = P(0, largo * 0.18)
        g.add(Line(c + P(-0.07, -0.07), c + P(0.07, 0.07)).set_stroke(color, SW * 0.9), Line(c + P(-0.07, 0.07), c + P(0.07, -0.07)).set_stroke(color, SW * 0.9))
    if n1:
        g.add(_t(n1, 0.17, color).next_to(sup, RIGHT, buff=0.08).shift(UP * 0.05))
    if n2:
        g.add(_t(n2, 0.17, color).next_to(inf, RIGHT, buff=0.08).shift(DOWN * 0.05))
    g.cuchilla, g.piv, g.largo, g.no = cuch, piv, largo, no
    return g


def accionar(simb, cerrar=True):
    """Animación: gira la cuchilla del contacto (NA cierra, NC abre)."""
    ang = -0.45 if simb.no else 0.75
    if not cerrar:
        ang = -ang
    return Rotate(simb.cuchilla, ang, about_point=simb.cuchilla.get_start())


def sim_bobina(ref="KM1", color=SIM):
    r = Rectangle(width=0.62, height=0.36, stroke_color=color, stroke_width=SW)
    a = Line(P(0, 0.18), P(0, 0.55)).set_stroke(color, SW)
    b = Line(P(0, -0.18), P(0, -0.55)).set_stroke(color, SW)
    g = VGroup(a, r, b, _t("A1", 0.16, color).next_to(a, RIGHT, buff=0.06), _t("A2", 0.16, color).next_to(b, RIGHT, buff=0.06),
               _t(ref, 0.2, color).next_to(r, LEFT, buff=0.12))
    g.rect = r
    return g


def sim_pulsador(no=True, color=SIM, n1=None, n2=None, ref=None):
    c = sim_contacto(no, largo=1.0, color=color, n1=n1, n2=n2)
    mid = c.cuchilla.get_center()
    act = VGroup(DashedLine(mid, mid + LEFT * 0.42, dash_length=0.05).set_stroke(color, SW * 0.7),
                 Line(mid + LEFT * 0.42 + UP * 0.12, mid + LEFT * 0.42 + DOWN * 0.12).set_stroke(color, SW * 0.8),
                 Line(mid + LEFT * 0.42 + UP * 0.12, mid + LEFT * 0.52 + UP * 0.12).set_stroke(color, SW * 0.8),
                 Line(mid + LEFT * 0.42 + DOWN * 0.12, mid + LEFT * 0.52 + DOWN * 0.12).set_stroke(color, SW * 0.8))
    c.add(act)
    if ref:
        c.add(_t(ref, 0.2, color).next_to(act, LEFT, buff=0.1))
    c.act = act
    return c


def sim_termico_contacto(color=SIM):
    c = sim_contacto(False, largo=1.0, color=color, n1="95", n2="96")
    mid = c.cuchilla.get_center()
    act = VGroup(DashedLine(mid, mid + LEFT * 0.36, dash_length=0.05).set_stroke(color, SW * 0.7),
                 VMobject().set_points_as_corners([mid + LEFT * 0.36 + UP * 0.1, mid + LEFT * 0.5 + UP * 0.1, mid + LEFT * 0.5 + DOWN * 0.1,
                                                    mid + LEFT * 0.64 + DOWN * 0.1]).set_stroke(color, SW * 0.8))
    c.add(act, _t("F2", 0.2, color).next_to(act, LEFT, buff=0.08))
    return c


def sim_motor(color=SIM):
    c = Circle(radius=0.55, stroke_color=color, stroke_width=SW)
    t = VGroup(_t("M", 0.32, color), _t("3~", 0.2, color)).arrange(DOWN, buff=0.04).move_to(c)
    return VGroup(c, t)


def sim_termico_pot(color=SIM):
    """Elemento térmico del relé de sobrecarga (IEC 60617): rectángulo con el trazo en escalón."""
    r = Rectangle(width=0.34, height=0.5, stroke_color=color, stroke_width=SW * 0.9)
    z = VMobject().set_points_as_corners([P(0, 0.25), P(0, 0.08), P(0.1, 0.08), P(0.1, -0.08), P(0, -0.08), P(0, -0.25)]).set_stroke(color, SW * 0.9)
    return VGroup(r, z)


def flecha_datos(texto, color=MARCA):
    return pastilla(texto, color, 22, True)

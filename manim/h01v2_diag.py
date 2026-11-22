"""H01 v2 · Diagramas IEC del usuario recreados LITERAL (Correcciones_V6: image6 = mando, image5 = potencia).
Coordenadas en píxeles de las imágenes originales (mando 400×708, potencia 553×759); se dibujan sobre una hoja
blanca como el original: líneas de mando granate y neutro azul, símbolos negros, PE verde punteado, rótulos turquesa.
Solo cambian los VALORES al motor de 10 hp (C80, 10hp, 23-32A, placa Nidec) y -X1 U1 V1 W1 → T1 T2 T3.
El mando se dibuja con trazo un poco más fino que la potencia (pedido del usuario)."""
import numpy as np
from manim import (VGroup, VMobject, Line, DashedLine, Circle, Dot, Rectangle, Polygon, Text, Square,
                   DashedVMobject, PI)

GRANATE = "#800000"
AZUL_N = "#0000FF"
NEGRO = "#000000"
VERDE_PE = "#008A00"
TURQ = "#008B8B"
FUENTE = "Liberation Sans"


class Hoja:
    """Hoja blanca con el diagrama. Cada primitiva se guarda en una 'parte' (tramo) para animarlo en orden."""

    def __init__(self, w_px, h_px, alto, centro, sw, pad=14):
        self.w, self.h = w_px, h_px
        self.s = alto / h_px
        self.c = np.array([centro[0], centro[1], 0.0], float)
        self.sw = sw
        self.partes = {}
        self.orden = []
        self.fondo = Rectangle(width=(w_px + 2 * pad) * self.s, height=(h_px + 2 * pad) * self.s, stroke_width=0).set_fill("#FFFFFF", 1).move_to(self.c)
        ref = Text("0", font=FUENTE, font_size=48)
        self.k_txt = 1.0 / ref.height          # escala: altura de un dígito = 1 unidad

    def P(self, x, y):
        return np.array([self.c[0] + (x - self.w / 2) * self.s, self.c[1] - (y - self.h / 2) * self.s, 0.0])

    def _add(self, key, m):
        if key not in self.partes:
            self.partes[key] = VGroup()
            self.orden.append(key)
        self.partes[key].add(m)
        return m

    def ln(self, key, pts, color=NEGRO, w=None, dash=False):
        w = self.sw if w is None else w
        ps = [self.P(*p) for p in pts]
        m = VMobject().set_points_as_corners(ps).set_stroke(color, w).set_fill(opacity=0)
        if dash:
            largo = sum(np.linalg.norm(b - a) for a, b in zip(ps, ps[1:]))
            m = DashedVMobject(m, num_dashes=max(2, int(largo / (6 * self.s))), dashed_ratio=0.55)
            m.set_stroke(color, w)
        m.tipo = "linea"
        return self._add(key, m)

    def tx(self, key, s, x, y, color=NEGRO, alto_px=8.6, bold=False, rot=0.0, ancla="c"):
        t = Text(s, font=FUENTE, font_size=48, color=color, weight="BOLD" if bold else "NORMAL")
        t.scale(alto_px * self.s * self.k_txt)
        if rot:
            t.rotate(rot)
        p = self.P(x, y)
        if ancla == "l":
            t.move_to(p + np.array([t.width / 2, 0, 0]))
        elif ancla == "r":
            t.move_to(p - np.array([t.width / 2, 0, 0]))
        else:
            t.move_to(p)
        t.tipo = "texto"
        return self._add(key, t)

    def circ(self, key, x, y, r, color=NEGRO, w=None):
        m = Circle(radius=r * self.s).set_stroke(color, self.sw if w is None else w).set_fill("#FFFFFF", 1).move_to(self.P(x, y))
        m.tipo = "linea"
        return self._add(key, m)

    def dot(self, key, x, y, color=GRANATE):
        m = Dot(self.P(x, y), radius=3.2 * self.s, color=color)
        m.tipo = "punto"
        return self._add(key, m)

    def rect(self, key, x0, y0, x1, y1, color=NEGRO, fill=None):
        m = Polygon(self.P(x0, y0), self.P(x1, y0), self.P(x1, y1), self.P(x0, y1)).set_stroke(color, self.sw)
        m.set_fill(fill or "#FFFFFF", 1 if fill else 0)
        m.tipo = "linea"
        return self._add(key, m)

    def cuad_negro(self, key, x, y, a=9.0, b=7.0, ang=-0.55):
        """Marca negra rellena del disyuntor sobre la cuchilla (como el software del usuario)."""
        m = Rectangle(width=a * self.s, height=b * self.s, stroke_width=0).set_fill(NEGRO, 1).rotate(ang).move_to(self.P(x, y))
        m.tipo = "punto"
        return self._add(key, m)

    def lampara(self, key, x, y, r=14.5):
        self.circ(key, x, y, r)
        d = r * 0.707
        self.ln(key, [(x - d, y - d), (x + d, y + d)])
        self.ln(key, [(x - d, y + d), (x + d, y - d)])

    def tierra(self, key, x, y, color=NEGRO):
        """Símbolo de tierra: tres trazos decrecientes desde y."""
        for k, hw in enumerate((15, 10, 5)):
            self.ln(key, [(x - hw, y + 7 * k), (x + hw, y + 7 * k)], color)

    def todo(self):
        return VGroup(self.fondo, *[self.partes[k] for k in self.orden])

    def marca(self, pts, color="#FDB022", w=9.0):
        """Trazo de resaltado sobre el diagrama (el hilo que se está tendiendo en los equipos)."""
        m = VMobject().set_points_as_corners([self.P(*p) for p in pts]).set_stroke(color, w, opacity=0.75).set_fill(opacity=0)
        return m


# ============================================================================ MANDO (image6, 400 × 708)
def _na(H, key, x, y1, y2, n1, n2, actuador=False, sw=None):
    """Contacto NA vertical entre y1 (arriba) y y2 (abajo): talones de 13 px y cuchilla abierta hacia la izquierda."""
    H.ln(key, [(x, y1), (x, y1 + 13)])
    H.ln(key, [(x, y2), (x - 15, y1 + 13)])
    H.ln(key, [(x, y2), (x, y2 + 13)])
    H.tx(key, n1, x + 5, y1 + 7, ancla="l")
    H.tx(key, n2, x + 5, y2 + 7, ancla="l")
    if actuador:
        ym = (y1 + 13 + y2) / 2
        H.ln(key, [(x - 21, ym - 6), (x - 29, ym - 6), (x - 29, ym + 6), (x - 21, ym + 6)])
        H.ln(key, [(x - 29, ym), (x - 25, ym)])
        H.ln(key, [(x - 18, ym), (x - 9, ym)], dash=True)


def _nc(H, key, x, y1, y2, n1, n2, actuador=None):
    """Contacto NC: talón superior con gancho a la derecha y cuchilla que cruza hacia la derecha."""
    H.ln(key, [(x, y1), (x, y1 + 18), (x + 17, y1 + 18)])
    H.ln(key, [(x, y2), (x + 15, y1 + 13)])
    H.ln(key, [(x, y2), (x, y2 + 13)])
    H.tx(key, n1, x + 5, y1 + 7, ancla="l")
    H.tx(key, n2, x + 5, y2 + 7, ancla="l")
    ym = (y1 + 18 + y2) / 2
    if actuador == "pulsador":
        H.ln(key, [(x - 21, ym - 6), (x - 29, ym - 6), (x - 29, ym + 6), (x - 21, ym + 6)])
        H.ln(key, [(x - 29, ym), (x - 25, ym)])
        H.ln(key, [(x - 18, ym), (x + 4, ym)], dash=True)
    elif actuador == "termico":
        H.ln(key, [(x - 29, ym + 5), (x - 29, ym - 5), (x - 21, ym - 5), (x - 21, ym + 5)])     # ⊓ del relé
        H.ln(key, [(x - 17, ym - 1), (x + 4, ym - 1)], dash=True)
        H.ln(key, [(x + 18, ym - 6), (x + 25, ym - 6), (x + 25, ym + 4), (x + 20, ym + 4), (x + 20, ym + 8)])   # elemento térmico


def diagrama_mando(alto=7.6, centro=(-4.0, -0.35), sw=2.2):
    H = Hoja(400, 708, alto, centro, sw)
    G, A = GRANATE, AZUL_N
    # m1 · fase L de -X0 y barra superior
    H.circ("m1", 47, 36, 4)
    H.tx("m1", "L", 47, 23)
    H.tx("m1", "-X0", 37, 36, ancla="r")
    H.ln("m1", [(47, 40), (47, 51), (317, 51)], G)
    H.dot("m1", 137, 51)
    # m2 · -F1 C2 (1-2)
    H.ln("m2", [(137, 51), (137, 96)], G)
    H.ln("m2", [(137, 96), (137, 109)])
    H.ln("m2", [(137, 142), (122, 111)])
    H.cuad_negro("m2", 122, 122)
    H.ln("m2", [(137, 142), (137, 155)])
    H.tx("m2", "1", 142, 104, ancla="l")
    H.tx("m2", "2", 142, 148, ancla="l")
    H.tx("m2", "-F1", 108, 125, ancla="r")
    H.tx("m2", "C2", 108, 141, ancla="r")
    H.ln("m2", [(137, 155), (137, 186)], G)
    H.dot("m2", 137, 186)
    # m3 · -F3 95-96 (NC accionado por el térmico)
    H.ln("m3", [(137, 186), (137, 215)], G)
    _nc(H, "m3", 137, 215, 260, "95", "96", "termico")
    H.tx("m3", "-F3", 98, 246, ancla="r")
    H.tx("m3", "23-32A", 98, 261, ancla="r")
    # m4 · -S0 paro 11-12
    H.ln("m4", [(137, 273), (137, 307)], G)
    _nc(H, "m4", 137, 307, 350, "11", "12", "pulsador")
    H.tx("m4", "-S0", 98, 336, ancla="r")
    H.tx("m4", "Paro", 77, 359, TURQ, ancla="l")
    # m5 · nodo y -S1 arranque 13-14
    H.ln("m5", [(137, 363), (137, 412)], G)
    H.dot("m5", 137, 381)
    _na(H, "m5", 137, 412, 457, "13", "14", actuador=True)
    H.tx("m5", "-S1", 98, 441, ancla="r")
    H.tx("m5", "Arranque", 77, 464, TURQ, ancla="l")
    # m6 · retención -KM1 13-14 en paralelo
    H.ln("m6", [(137, 381), (227, 381), (227, 412)], G)
    _na(H, "m6", 227, 412, 457, "13", "14")
    H.tx("m6", "-KM1", 207, 441, ancla="r")
    H.ln("m6", [(137, 470), (137, 516)], G)
    H.ln("m6", [(227, 470), (227, 516)], G)
    H.ln("m6", [(137, 516), (227, 516)], G)
    H.dot("m6", 137, 516)
    H.dot("m6", 227, 516)
    # m7 · bobina -KM1 A1-A2 y piloto -H1 en paralelo
    H.ln("m7", [(137, 516), (137, 571)], G)
    H.ln("m7", [(137, 571), (137, 581)])
    H.rect("m7", 117, 581, 157, 601)
    H.ln("m7", [(137, 601), (137, 611)])
    H.tx("m7", "A1", 142, 568, ancla="l")
    H.tx("m7", "A2", 142, 614, ancla="l")
    H.tx("m7", "-KM1", 106, 591, ancla="r")
    H.ln("m7", [(227, 516), (227, 571)], G)
    H.ln("m7", [(227, 571), (227, 576.5)])
    H.lampara("m7", 227, 591)
    H.ln("m7", [(227, 605.5), (227, 611)])
    H.tx("m7", "X1", 232, 568, ancla="l")
    H.tx("m7", "X2", 232, 614, ancla="l")
    H.tx("m7", "-H1", 196, 591, ancla="r")
    H.tx("m7", "Motor 1", 129, 674, TURQ)
    H.tx("m7", "Piloto M1 On", 220, 674, TURQ)
    # m8 · regreso al neutro de -X0
    H.circ("m8", 32, 635, 4)
    H.tx("m8", "N", 32, 622)
    H.tx("m8", "-X0", 22, 635, ancla="r")
    H.ln("m8", [(32, 639), (32, 651), (376, 651)], A)
    for x in (137, 227):
        H.ln("m8", [(x, 611), (x, 651)], A)
        H.dot("m8", x, 651)
    # m9 · rama de -H2: -F1:2 → -KM1 21-22 → -H2
    H.ln("m9", [(137, 186), (317, 186), (317, 412)], G)
    _nc(H, "m9", 317, 412, 457, "21", "22")
    H.tx("m9", "-KM1", 297, 441, ancla="r")
    H.ln("m9", [(317, 470), (317, 571)], G)
    H.ln("m9", [(317, 571), (317, 576.5)])
    H.lampara("m9", 317, 591)
    H.ln("m9", [(317, 605.5), (317, 611)])
    H.tx("m9", "X1", 322, 568, ancla="l")
    H.tx("m9", "X2", 322, 614, ancla="l")
    H.tx("m9", "-H2", 286, 591, ancla="r")
    H.ln("m9", [(317, 611), (317, 651)], A)
    H.dot("m9", 317, 651)
    H.tx("m9", "Piloto M1 Off", 325, 674, TURQ)
    return H


# Trazos del diagrama de mando que corresponden a cada hilo físico (para marcarlos mientras se tienden)
HILOS_MANDO = {
    "1": [[(47, 40), (47, 51), (137, 51), (137, 96)]],
    "2": [[(137, 155), (137, 186), (137, 215)], [(137, 186), (317, 186), (317, 412)]],
    "3": [[(137, 273), (137, 307)]],
    "4": [[(137, 363), (137, 412)], [(137, 381), (227, 381), (227, 412)]],
    "5": [[(137, 470), (137, 571)], [(137, 516), (227, 516), (227, 576)], [(227, 470), (227, 516)]],
    "6": [[(317, 470), (317, 576)]],
    "N": [[(32, 639), (32, 651), (317, 651)], [(137, 611), (137, 651)], [(227, 606), (227, 651)], [(317, 606), (317, 651)]],
}


# ============================================================================ POTENCIA (image5, 553 × 759)
def diagrama_potencia(alto=7.6, centro=(-4.0, -0.35), sw=3.0):
    H = Hoja(553, 759, alto, centro, sw)
    G = GRANATE
    filas = (("PE", 21, VERDE_PE, "5"), ("N", 51, AZUL_N, "4"), ("L3", 81, G, "3"), ("L2", 111, G, "2"), ("L1", 141, G, "1"))
    # p_d1 · bornera -X0
    for nom, y, col, num in filas:
        H.tx("pd1", nom, 20, y, rot=PI / 2)
        H.circ("pd1", 34, y, 4)
        H.ln("pd1", [(38, y), (50, y)])
        H.ln("pd1", [(50, y), (91, y)], col, dash=(nom == "PE"))
        H.circ("pd1", 95, y, 4)
        H.ln("pd1", [(99, y), (515, y)], col, dash=(nom == "PE"))
        H.tx("pd1", num, 76, y + 9)
    H.tx("pd1", "-X0", 76, 133)
    # p_d2 · -F2 C80
    for x, yr, n1, n2 in ((245, 81, "1", "2"), (275, 111, "3", "4"), (305, 141, "5", "6")):
        H.dot("pd2", x, yr)
        H.ln("pd2", [(x, yr), (x, 230)], G)
        H.ln("pd2", [(x, 230), (x, 245)])
        H.ln("pd2", [(x, 276), (x - 15, 246)])
        H.cuad_negro("pd2", x - 14, 258)
        H.ln("pd2", [(x - 7, 261), (x + 4, 261)])
        H.ln("pd2", [(x, 276), (x, 290)])
        H.tx("pd2", n1, x + 5, 239, ancla="l")
        H.tx("pd2", n2, x + 5, 284, ancla="l")
        H.ln("pd2", [(x, 290), (x, 352)], G)
    H.tx("pd2", "-F2", 215, 260, ancla="r")
    H.tx("pd2", "C80", 215, 275, ancla="r")
    # p_d3 · -KM1
    for x, n1, n2 in ((245, "1", "2"), (275, "3", "4"), (305, "5", "6")):
        H.ln("pd3", [(x, 352), (x, 365)])
        H.ln("pd3", [(x, 397), (x - 15, 366)])
        H.ln("pd3", [(x - 8, 380), (x + 2, 380)])
        H.ln("pd3", [(x, 397), (x, 410)])
        H.tx("pd3", n1, x + 5, 359, ancla="l")
        H.tx("pd3", n2, x + 5, 404, ancla="l")
        H.ln("pd3", [(x, 410), (x, 471)], G)
    H.tx("pd3", "-KM1", 225, 381, ancla="r")
    H.tx("pd3", "10hp", 225, 396, ancla="r")
    # p_d4 · -F3 relé térmico
    H.rect("pd4", 238, 471, 328, 501)
    for x, n1, n2 in ((245, "1", "2"), (275, "3", "4"), (305, "5", "6")):
        H.ln("pd4", [(x, 464), (x, 480), (x + 15, 480), (x + 15, 492), (x, 492), (x, 508)])
        H.tx("pd4", n1, x + 5, 464, ancla="l")
        H.tx("pd4", n2, x + 5, 509, ancla="l")
    H.tx("pd4", "-F3", 216, 486, ancla="r")
    H.tx("pd4", "23-32A", 216, 501, ancla="r")
    # p_d5 · -X1, motor y tierra
    for x in (245, 275, 305):
        H.ln("pd5", [(x, 508), (x, 557)], G)
    for x in (245, 275, 305, 335):
        H.circ("pd5", x, 561, 4)
    H.tx("pd5", "-X1", 226, 554)
    for x, n in ((226, "1"), (256, "2"), (286, "3"), (316, "4")):
        H.tx("pd5", n, x, 569)
    import math
    for x, t in ((245, "T1"), (275, "T2"), (305, "T3")):
        yc = 667 - math.sqrt(max(44 ** 2 - (x - 275) ** 2, 0))
        H.ln("pd5", [(x, 565), (x, 605)], G)
        H.ln("pd5", [(x, 605), (x, yc)])
        H.tx("pd5", t, x + 4, 613, ancla="l")
    H.tx("pd5", "PE", 340, 613, ancla="l")
    H.circ("pd5", 275, 667, 44)
    H.tx("pd5", "M", 275, 654)
    H.tx("pd5", "3", 260, 675)
    H.ln("pd5", [(280, 676), (284, 672), (288, 672), (292, 676), (296, 680), (300, 680), (304, 676)])
    H.tx("pd5", "-M1", 225, 667, ancla="r")
    H.ln("pd5", [(335, 565), (335, 576)], VERDE_PE, dash=True)
    H.dot("pd5", 335, 576)
    H.ln("pd5", [(335, 576), (335, 605)], VERDE_PE, dash=True)
    H.ln("pd5", [(335, 605), (335, 667), (330, 667)])
    H.ln("pd5", [(325, 660), (325, 674)])
    H.ln("pd5", [(328, 660), (328, 674)])
    H.ln("pd5", [(335, 576), (395, 576), (395, 598)], VERDE_PE, dash=True)
    H.ln("pd5", [(395, 598), (395, 606)])
    H.tierra("pd5", 395, 606)
    H.ln("pd5", [(335, 21), (335, 557)], VERDE_PE, dash=True)
    H.dot("pd5", 335, 21)
    H.dot("pd5", 440, 21)
    H.ln("pd5", [(440, 21), (440, 185)], VERDE_PE, dash=True)
    H.ln("pd5", [(440, 185), (440, 200)])
    H.tierra("pd5", 440, 200)
    placa = ["NIDEC US MOTORS PH:3", "MOD. U10P2D", "10 HP", "208-230/460VAC 26.5A 60Hz", "SER.F:1.25 DES:B",
             "RPM: 1760 EFF: 91.7%", "FRAME 215T"]
    for i, t in enumerate(placa):
        H.tx("pd5", t, 350, 644 + 15 * i, TURQ, bold=(i == 0), ancla="l")
    return H


HILOS_POT = {
    "p1": [[(99, 141), (305, 141), (305, 230)], [(99, 111), (275, 111), (275, 230)], [(99, 81), (245, 81), (245, 230)]],
    "p2": [[(x, 290), (x, 352)] for x in (245, 275, 305)],
    "p3": [[(x, 410), (x, 471)] for x in (245, 275, 305)],
    "p4": [[(x, 508), (x, 557)] for x in (245, 275, 305)],
    "pe": [[(99, 21), (335, 21), (335, 557)]],
    "p5": [[(x, 565), (x, 625)] for x in (245, 275, 305)],
}

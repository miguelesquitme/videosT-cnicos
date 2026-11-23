"""Diagramas del usuario recreados PIXEL POR PIXEL (Correcciones_V7, puntos 4-6).
Se parte de la imagen original del usuario (referencias/diagramas_h01/*_original.png):
  1. se borran SOLO los textos (componentes conectados que caben completos en cada caja de texto);
  2. el dibujo (líneas y símbolos) se pasa a UN SOLO COLOR (negro) y se vectoriza con potrace (×4), así cada
     símbolo queda idéntico al original y nítido a cualquier tamaño;
  3. los textos se vuelven a escribir en la misma posición y tamaño; solo cambian los que dependen del caso
     (capacidades, nombres, placa del motor, bornes del motor).
Cada tramo (para dibujarlo en orden con la voz) se separa por regiones del original."""
import numpy as np
from PIL import Image
from scipy import ndimage
import potrace
from manim import VGroup, VMobject, Text, Rectangle, PI

ESC = 4                    # sobremuestreo antes de vectorizar
FUENTE = "Liberation Sans"
NEGRO = "#000000"


def _mascara_dibujo(a, cajas):
    """a: RGB del original. Devuelve (dibujo binario sin textos, info de textos: bbox real de cada caja)."""
    s = a.astype(int).sum(axis=2)
    tinta = s < 640
    lab, n = ndimage.label(tinta, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    borrar = np.zeros(n + 1, bool)
    reales = []
    for (x0, y0, x1, y1) in cajas:
        ys, xs = [], []
        for i, sl in enumerate(objs):
            if sl[0].start >= y0 and sl[0].stop <= y1 + 1 and sl[1].start >= x0 and sl[1].stop <= x1 + 1:
                borrar[i + 1] = True
                ys += [sl[0].start, sl[0].stop]
                xs += [sl[1].start, sl[1].stop]
        reales.append((min(xs), min(ys), max(xs), max(ys)) if xs else (x0, y0, x1, y1))
    limpio = tinta & ~borrar[lab]
    return limpio, reales


def _trazar(mask):
    """Vectoriza una máscara (px del original) → lista de subtrazos en px del original (bezier cúbicas)."""
    if not mask.any():
        return []
    im = Image.fromarray((mask * 255).astype(np.uint8)).resize((mask.shape[1] * ESC, mask.shape[0] * ESC), Image.BILINEAR)
    bm = potrace.Bitmap(np.array(im) <= 110)   # potracer traza lo False como tinta
    plist = bm.trace(turdsize=3, alphamax=0.55, opttolerance=0.15)
    curvas = []
    for c in plist:
        segs = []
        p0 = (c.start_point.x / ESC, c.start_point.y / ESC)
        cur = p0
        for sg in c.segments:
            if sg.is_corner:
                segs.append(("L", cur, (sg.c.x / ESC, sg.c.y / ESC)))
                segs.append(("L", (sg.c.x / ESC, sg.c.y / ESC), (sg.end_point.x / ESC, sg.end_point.y / ESC)))
            else:
                segs.append(("C", cur, (sg.c1.x / ESC, sg.c1.y / ESC), (sg.c2.x / ESC, sg.c2.y / ESC), (sg.end_point.x / ESC, sg.end_point.y / ESC)))
            cur = (sg.end_point.x / ESC, sg.end_point.y / ESC)
        curvas.append((p0, segs))
    return curvas


class Literal:
    """Diagrama literal: .partes[clave] = VGroup (dibujo vectorizado + textos), .orden, .fondo, .P(x, y), .marca()."""

    def __init__(self, ruta, alto, centro, textos, regiones, pad=12, color=NEGRO):
        a = np.array(Image.open(ruta).convert("RGB"))
        self.h, self.w = a.shape[:2]
        self.s = alto / self.h
        self.c = np.array([centro[0], centro[1], 0.0])
        self.fondo = Rectangle(width=(self.w + 2 * pad) * self.s, height=(self.h + 2 * pad) * self.s, stroke_width=0).set_fill("#FFFFFF", 1).move_to(self.c)
        cajas = [t[1] for t in textos]
        dibujo, reales = _mascara_dibujo(a, cajas)
        # escala del texto: altura de un dígito del original (9 px)
        ref = Text("0", font=FUENTE, font_size=48)
        self.k_txt = 9.0 * self.s / ref.height
        # reparto del dibujo en tramos
        yy, xx = np.mgrid[0:self.h, 0:self.w]
        asignado = np.zeros_like(dibujo, bool)
        self.orden = []
        self.partes = {}
        for clave, fn in regiones:
            m = fn(xx, yy, dibujo) & dibujo & ~asignado
            asignado |= m
            self._parte(clave).add(self._vm(_trazar(m), color))
        resto = dibujo & ~asignado
        if resto.any():
            self._parte(regiones[0][0]).add(self._vm(_trazar(resto), color))
        for (txt, _, ancla, clave, *extra), (x0, y0, x1, y1) in zip(textos, reales):
            if txt is None:
                continue
            bold = bool(extra and extra[0])
            t = Text(txt, font=FUENTE, font_size=48, color=color, weight="BOLD" if bold else "NORMAL").scale(self.k_txt)
            if ancla == "r":
                t.move_to(self.P(x1, (y0 + y1) / 2) - np.array([t.width / 2, 0, 0]))
            elif ancla == "l":
                t.move_to(self.P(x0, (y0 + y1) / 2) + np.array([t.width / 2, 0, 0]))
            elif ancla == "v":           # rotado 90° (se lee de abajo hacia arriba)
                t.rotate(PI / 2).move_to(self.P((x0 + x1) / 2, (y0 + y1) / 2))
            else:
                t.move_to(self.P((x0 + x1) / 2, (y0 + y1) / 2))
            t.tipo = "texto"
            self._parte(clave).add(t)

    def _parte(self, clave):
        if clave not in self.partes:
            self.partes[clave] = VGroup()
            self.orden.append(clave)
        return self.partes[clave]

    def P(self, x, y):
        return np.array([self.c[0] + (x - self.w / 2) * self.s, self.c[1] - (y - self.h / 2) * self.s, 0.0])

    def _vm(self, curvas, color):
        m = VMobject()
        for p0, segs in curvas:
            m.start_new_path(self.P(*p0))
            for sg in segs:
                if sg[0] == "L":
                    m.add_line_to(self.P(*sg[2]))
                else:
                    m.add_cubic_bezier_curve_to(self.P(*sg[2]), self.P(*sg[3]), self.P(*sg[4]))
        m.set_fill(color, 1).set_stroke(width=0)
        m.tipo = "dibujo"
        return m

    def todo(self):
        return VGroup(self.fondo, *[self.partes[k] for k in self.orden])

    def marca(self, pts, color="#F79009", w=8.0, op=0.8):
        m = VMobject().set_points_as_corners([self.P(*p) for p in pts]).set_stroke(color, w, opacity=op).set_fill(opacity=0)
        return m


# ============================================================================ MANDO (400 × 708)
def _r(x0, y0, x1, y1):
    return lambda xx, yy, d: (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)


def _o(*fs):
    return lambda xx, yy, d: np.logical_or.reduce([f(xx, yy, d) for f in fs])


TEXTOS_MANDO = [  # (texto nuevo o None para borrarlo, caja del original, ancla, tramo)
    ("L", (42, 17, 51, 29), "c", "m1"), ("-X0", (17, 29, 39, 41), "r", "m1"),
    ("1", (140, 97, 149, 110), "c", "m2"), ("-F1", (86, 119, 111, 132), "r", "m2"), ("C2", (86, 134, 111, 147), "r", "m2"), ("2", (140, 142, 150, 154), "c", "m2"),
    ("95", (141, 217, 158, 229), "c", "m3"), ("96", (141, 262, 158, 274), "c", "m3"), ("-F3", (75, 239, 100, 252), "r", "m3"), ("23-32A", (75, 253, 100, 266), "r", "m3"),
    ("11", (141, 307, 157, 319), "c", "m4"), ("12", (141, 352, 158, 364), "c", "m4"), ("-S0", (76, 329, 99, 342), "r", "m4"), ("Paro", (74, 350, 110, 368), "c", "m4"),
    ("13", (141, 412, 157, 424), "c", "m5"), ("14", (141, 457, 157, 469), "c", "m5"), ("-S1", (76, 434, 99, 446), "r", "m5"), ("Arranque", (74, 457, 132, 473), "c", "m5"),
    ("13", (231, 412, 247, 424), "c", "m6"), ("14", (231, 457, 247, 469), "c", "m6"), ("-KM1", (175, 434, 206, 446), "r", "m6"),
    ("A1", (140, 562, 156, 574), "c", "m7"), ("A2", (140, 607, 158, 619), "c", "m7"), ("-KM1", (75, 583, 108, 597), "r", "m7"),
    ("X1", (230, 562, 246, 574), "c", "m7"), ("X2", (230, 607, 248, 619), "c", "m7"), ("-H1", (172, 584, 197, 596), "r", "m7"),
    ("Motor 1", (100, 665, 160, 681), "c", "m7"), ("Piloto M1 On", (175, 665, 268, 681), "c", "m7"),
    ("N", (27, 617, 38, 629), "c", "m8"), ("-X0", (1, 629, 25, 641), "r", "m8"),
    ("21", (320, 412, 337, 424), "c", "m9"), ("22", (320, 457, 338, 469), "c", "m9"), ("-KM1", (265, 434, 296, 446), "r", "m9"),
    ("X1", (320, 562, 336, 574), "c", "m9"), ("X2", (320, 607, 338, 619), "c", "m9"), ("-H2", (262, 584, 289, 596), "r", "m9"),
    ("Piloto M1 Off", (278, 665, 375, 681), "c", "m9"),
]

REG_MANDO = [
    ("m8", _o(_r(0, 612, 400, 708), _r(0, 615, 45, 650))),
    ("m1", _r(0, 0, 400, 57)),
    ("m9", _o(_r(200, 180, 400, 192), _r(290, 192, 400, 612))),
    ("m6", _o(_r(140, 377, 240, 386), _r(200, 372, 290, 476), _r(60, 476, 290, 528))),
    ("m2", _r(0, 57, 290, 191)),
    ("m3", _r(0, 191, 290, 277)),
    ("m4", _r(0, 277, 290, 372)),
    ("m5", _r(0, 372, 200, 476)),
    ("m7", _r(0, 528, 290, 612)),
]


def diagrama_mando(alto=7.75, centro=(0, -0.3)):
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "referencias" / "diagramas_h01" / "mando_original.png"
    return Literal(str(ruta), alto, centro, TEXTOS_MANDO, REG_MANDO)


# ============================================================================ POTENCIA (553 × 759)
_PLACA = ["NIDEC US MOTORS PH:3", "MOD. U10P2D", "10 HP", "208-230/460VAC 26.5A 60Hz", "SER.F:1.25 DES:B", "RPM: 1760 EFF: 91.7%", "FRAME 215T"]
TEXTOS_POT = [
    ("PE", (14, 10, 30, 30), "v", "pd1"), ("N", (14, 44, 30, 57), "v", "pd1"), ("L3", (14, 74, 30, 90), "v", "pd1"), ("L2", (14, 104, 30, 120), "v", "pd1"), ("L1", (14, 135, 30, 151), "v", "pd1"),
    ("5", (71, 22, 82, 34), "c", "pd1"), ("4", (71, 52, 82, 64), "c", "pd1"), ("3", (71, 82, 82, 94), "c", "pd1"), ("2", (71, 112, 82, 124), "c", "pd1"),
    ("-X0", (64, 127, 87, 139), "c", "pd1"), ("1", (71, 142, 82, 154), "c", "pd1"),
    ("1", (249, 232, 257, 244), "c", "pd2"), ("3", (278, 232, 288, 244), "c", "pd2"), ("5", (308, 232, 318, 244), "c", "pd2"),
    ("2", (248, 278, 257, 289), "c", "pd2"), ("4", (278, 278, 288, 289), "c", "pd2"), ("6", (308, 278, 318, 289), "c", "pd2"),
    ("-F2", (183, 254, 216, 267), "r", "pd2"), ("C80", (183, 268, 216, 281), "r", "pd2"),
    ("1", (249, 352, 257, 364), "c", "pd3"), ("3", (278, 352, 288, 364), "c", "pd3"), ("5", (308, 352, 318, 364), "c", "pd3"),
    ("2", (248, 397, 257, 409), "c", "pd3"), ("4", (278, 397, 288, 409), "c", "pd3"), ("6", (308, 397, 318, 409), "c", "pd3"),
    ("-KM1", (195, 374, 225, 387), "r", "pd3"), ("10hp", (195, 389, 225, 401), "r", "pd3"),
    ("1", (249, 457, 257, 469), "c", "pd4"), ("3", (278, 457, 288, 469), "c", "pd4"), ("5", (308, 457, 318, 469), "c", "pd4"),
    ("2", (248, 502, 257, 514), "c", "pd4"), ("4", (278, 502, 288, 514), "c", "pd4"), ("6", (308, 502, 318, 514), "c", "pd4"),
    ("-F3", (193, 479, 215, 492), "r", "pd4"), ("23-32A", (193, 494, 215, 506), "r", "pd4"),
    ("-X1", (214, 547, 233, 559), "c", "pd5"), ("1", (220, 562, 233, 575), "c", "pd5"), ("2", (250, 562, 260, 575), "c", "pd5"),
    ("3", (280, 562, 290, 575), "c", "pd5"), ("4", (310, 562, 320, 575), "c", "pd5"),
    ("T1", (249, 607, 268, 620), "l", "pd5"), ("T2", (279, 607, 298, 620), "l", "pd5"), ("T3", (309, 607, 328, 620), "l", "pd5"), ("PE", (339, 607, 358, 620), "l", "pd5"),
    ("M", (269, 647, 282, 660), "c", "pd5"), ("3", (254, 669, 265, 684), "c", "pd5"), ("-M1", (202, 662, 225, 675), "r", "pd5"),
] + [(t, (348, 637 + 15 * i, 540, 650 + 15 * i) if i == 0 else (348, 637 + 15 * i, 540, 650 + 15 * i), "l", "pd5", i == 0) for i, t in enumerate(_PLACA)]


def _reg_pot():
    def pe(xx, yy, d):
        return ((xx >= 331) & (xx <= 339) & (yy >= 15) & (yy < 560)) | ((xx >= 420) & (xx <= 462) & (yy >= 14) & (yy < 225))

    def bajadas(xx, yy, d):
        v = ndimage.binary_opening(d, structure=np.ones((7, 1)))
        dots = np.zeros_like(d)
        for (x, y) in ((245, 81), (275, 111), (305, 141)):
            dots |= (xx - x) ** 2 + (yy - y) ** 2 <= 25
        return ((v & (xx >= 240) & (xx <= 310) & (yy < 160)) | dots)
    return [
        ("pd5", _o(pe, _r(0, 525, 553, 759))),
        ("pd2", _o(bajadas, _r(0, 160, 553, 330))),
        ("pd1", _r(0, 0, 553, 160)),
        ("pd3", _r(0, 330, 553, 440)),
        ("pd4", _r(0, 440, 553, 525)),
    ]


def diagrama_potencia(alto=7.75, centro=(0, -0.3)):
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent / "referencias" / "diagramas_h01" / "potencia_original.png"
    H = Literal(str(ruta), alto, centro, TEXTOS_POT, _reg_pot())
    # orden de dibujo: X0 → F2 → KM1 → F3 → X1/motor/tierra
    H.orden = ["pd1", "pd2", "pd3", "pd4", "pd5"]
    return H

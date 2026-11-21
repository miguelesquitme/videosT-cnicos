"""Estilo único de la librería @miguelesquit (referencia: CPU 1212C, Word del usuario 21-nov-2026).
Equipos planos gris pizarra con líneas de contorno, bornes con tornillo blanco "+", textos pequeños claros.
Escala: todas las piezas se dibujan en milímetros reales y se convierten con K (unidades Manim por mm)."""
from manim import *
import numpy as np
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LOGO = RAIZ / "marca" / "logo_oficial.png"

# ---- paleta de equipos (CPU 1212 como base, tono propio)
CUERPO = "#606C7B"       # carcasa
CUERPO_CL = "#727F8F"    # frente elevado / zonas claras
CUERPO_OS = "#4A5462"    # franjas y zonas oscuras
BORNERA = "#2E343D"      # bloque de bornes (oscuro, como en el CPU 1212)
BORDE = "#262C34"        # contorno
LINEA_DET = "#8D99A8"    # líneas de detalle sobre la carcasa
TXT_EQ = "#EEF1F5"       # textos impresos sobre el equipo
TXT_OS = "#1D2939"       # textos oscuros (sobre etiquetas blancas)
TURQ = "#1BA8C4"         # acento de marca
TORN = "#F2F4F7"         # tornillo
TORN_AR = "#9AA4B2"      # aro del tornillo
METAL = "#B8C0CA"
# ---- conductores (IEC 60204-1 / práctica regional)
C_POT = "#15171B"        # potencia: negro
C_AC = "#D92D20"         # mando en AC: rojo
C_DC = "#1F5FD6"         # mando en DC: azul
C_N = "#53B1FD"          # neutro: azul claro
C_PE = ("#2E9E44", "#F2C200")
# ---- símbolos
SIM_N = "#101828"        # símbolos sobre fondo claro (documento)
SIM_B = "#F2F4F7"        # símbolos sobre fondo negro (video)

FUENTE = "Montserrat"
# color de textos que quedan FUERA del equipo (hilos, rótulos de bornera): blanco en video, oscuro en documento
FUERA = {"c": TXT_EQ}


def txt(s, h, color=TXT_EQ, peso=BOLD, fuente=FUENTE):
    """Texto cuyo alto de mayúsculas es ~h (unidades)."""
    t = Text(s, font=fuente, weight=peso, color=color)
    ref = Text("H", font=fuente, weight=peso)
    t.scale(h / max(ref.height, 1e-6))
    return t


def caja(w, h, k, color=CUERPO, r=1.6, borde=BORDE, sw=1.6):
    return RoundedRectangle(width=w * k, height=h * k, corner_radius=r * k, stroke_color=borde, stroke_width=sw).set_fill(color, 1)


def tornillo(r):
    """Tornillo blanco con cruz (como en las referencias), r en unidades."""
    aro = Circle(radius=r, stroke_color=TORN_AR, stroke_width=max(1, r * 9)).set_fill(TORN, 1)
    cruz = VGroup(Line(LEFT * r * 0.55, RIGHT * r * 0.55), Line(DOWN * r * 0.55, UP * r * 0.55)).set_stroke("#3A414C", max(1.2, r * 14))
    return VGroup(aro, cruz)


class Borne(VGroup):
    """Borne de tornillo dentro de su cavidad. .p = centro del tornillo (punto de conexión)."""
    def __init__(self, nombre, k, w=7.0, h=7.0, r=2.4, etiqueta=True, lado=UP, h_txt=2.0, color_txt=TXT_EQ, cavidad=BORNERA):
        super().__init__()
        cav = RoundedRectangle(width=w * k, height=h * k, corner_radius=1.0 * k, stroke_width=0).set_fill(cavidad, 1)
        self.tor = tornillo(r * k)
        self.add(cav, self.tor)
        self.nombre = nombre
        if etiqueta and nombre:
            self.txt = txt(nombre, h_txt * k, color_txt)
            self.txt.next_to(cav, lado, buff=0.9 * k)
            self.add(self.txt)

    @property
    def p(self):
        return self.tor.get_center()


LOGO_POLIS = [  # trazado exacto del logo oficial (643 × 394 px): (puntos), color
    ([(0, 3), (114.5, 3), (170, 176), (224.5, 3), (224.5, 215), (199, 303.5), (141, 303.5), (103.5, 177), (103.5, 390.5), (0, 390.5)], "#91D4DF"),
    ([(245, 3), (345.5, 3), (345.5, 390.5), (245, 390.5)], "#0094B0"),
    ([(366, 3), (524.5, 3), (524.5, 88.5), (366, 88.5)], "#0094B0"),
    ([(366, 154), (481.5, 154), (481.5, 239.5), (366, 239.5)], "#0094B0"),
    ([(366, 305), (524.5, 305), (524.5, 390.5), (366, 390.5)], "#0094B0"),
    ([(562, 304), (639.5, 304), (639.5, 390.5), (562, 390.5)], "#0094B0"),
]


def logo_marca(alto):
    """Logo del canal en vector (reemplaza la marca del fabricante en equipos genéricos)."""
    g = VGroup()
    for pts, col in LOGO_POLIS:
        g.add(Polygon(*[[x, -y, 0] for x, y in pts], stroke_width=0).set_fill(col, 1))
    g.scale_to_fit_height(alto)
    return g


def cota(a, b, texto, k_txt=0.18, color="#667085", off=0.25, lado=DOWN):
    """Cota de dimensión entre dos puntos (para el catálogo)."""
    a, b = np.array(a), np.array(b)
    d = lado * off
    l = DoubleArrow(a + d, b + d, buff=0, stroke_width=2, tip_length=0.1, color=color, max_tip_length_to_length_ratio=0.08)
    t = txt(texto, k_txt, color, BOLD).next_to(l, lado, buff=0.06)
    return VGroup(l, t)

"""Base de los reels v2 (dibujo real + voz anclada a palabras). Modelo: f01_fotocelda.py.
Uso:
    from reel_v2 import *
    class V22(ReelV2):
        CLAVE = "v22v2"; GUION_MOD = "guion_v22v2"
        def cuerpo(self): ...
Render: FORMATO=v VOZ=eleven manim -qh --disable_caching -o cuerpo_<clave> <archivo>.py <Clase>
"""
from reel_base import *  # noqa: F401,F403   (importa comun_e primero → voz clonada)
import importlib
import json
import re
import unicodedata
import shorts_v


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


class Pieza(Group):
    """PNG de una librería svg* con sus puntos en mm (JSON de render_svg) para anclar llamadas."""
    CARPETA = None

    def __init__(self, nombre, ancho=None, alto=None, carpeta=None):
        carp = carpeta or Pieza.CARPETA
        d = json.loads((carp / f"{nombre}.json").read_text())
        img = ImageMobject(str(carp / f"{nombre}.png"))
        if alto is not None:
            img.height = alto
        else:
            img.width = ancho
        super().__init__(img)
        self.img, self.d = img, d
        self.k = img.width / (d["W"] + 2 * d["margen"])

    def mm(self, x, y):
        m = self.d["margen"]
        return self.img.get_corner(UL) + RIGHT * (m + x) * self.k + DOWN * (m + y) * self.k

    def p(self, b):
        return self.mm(*self.d["bornes"][b])


def registrar(clave, guion_mod):
    g = importlib.import_module(guion_mod)
    shorts_v.SHORTS[clave] = (g.TIT[0], g.TIT[1], g.GUION)
    return g


class ReelV2(ReelTec):
    TEMA = "negro"
    CLAVE = ""
    GUION_MOD = ""

    def setup(self):
        g = registrar(self.CLAVE, self.GUION_MOD)
        self.TIT1, self.TIT2 = g.TIT
        Pieza.CARPETA = DIR / f"{self.CLAVE}_eq"
        self.ALIN = DIR / f"alin_{self.CLAVE}"
        super().setup()

    # ------------------------------------------------ voz anclada a palabras
    def voz(self, clave):
        self.ini_voz = self.renderer.time
        ruta = self.ALIN / f"{clave}.json"
        self.palabras = json.loads(ruta.read_text()) if ruta.exists() else []
        self.cursor = 0
        return super().voz(clave)

    def hasta(self, t):
        w = t - self.renderer.time
        if w > 0.05:
            self.wait(w)

    def en(self, palabra, antes=0.15):
        objs = [_norm(x) for x in palabra.split("|")]
        for i in range(self.cursor, len(self.palabras)):
            if any(_norm(self.palabras[i][2]).startswith(o) for o in objs):
                self.cursor = i + 1
                self.hasta(self.ini_voz + self.palabras[i][0] - antes)
                return
        print("NO ENCONTRADA:", palabra)

    # ------------------------------------------------ ayudas visuales
    def flecha(self, texto, punto, desde, color, size=26):
        t = self.tag(texto, color, size).move_to(desde)
        if punto[0] > t.get_right()[0]:
            lado = t.get_right()
        elif punto[0] < t.get_left()[0]:
            lado = t.get_left()
        else:
            lado = t.get_bottom() if punto[1] < t.get_y() else t.get_top()
        ln = Line(lado, punto).set_stroke(color, 4)
        dot = Dot(punto, radius=0.075, color=color)
        return VGroup(ln, dot, t)

    def recuadro(self, centro, w, h, color):
        return Rectangle(width=w, height=h, stroke_color=color, stroke_width=5).move_to(centro)

    def aro(self, centro, r, color):
        return Circle(radius=r, stroke_color=color, stroke_width=6).move_to(centro)

    def poner(self, nueva, vieja=None):
        """Cambio instantáneo de estado (la pieza nueva ocupa el lugar de la vieja)."""
        if vieja is not None:
            nueva.move_to(vieja)
            self.add(nueva)
            self.remove(vieja)
        else:
            self.add(nueva)
        return nueva

    def rayo(self, centro, esc=1.0, color="#FFE066"):
        pts = [[0.15, 0.9], [-0.25, 0.05], [0.05, 0.05], [-0.2, -0.9], [0.3, 0.15], [0.0, 0.15], [0.25, 0.9]]
        return Polygon(*[np.array([x, y, 0]) * esc for x, y in pts], stroke_width=0).set_fill(color, 1).move_to(centro)

    def sol(self, centro, r=0.55):
        rayos = VGroup(*[Line(ORIGIN, RIGHT * 0.3).shift(RIGHT * (r + 0.12)).rotate(a, about_point=ORIGIN) for a in np.arange(0, TAU, TAU / 12)])
        return VGroup(rayos.set_stroke("#FFB020", 5), Circle(radius=r, stroke_width=0).set_fill("#FFC83D", 1)).move_to(centro)

    def ejes(self, centro, w=7.6, h=3.0, xr=(0, 10), yr=(0, 60), xlab="", ylab=""):
        ax = Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 10], x_length=w, y_length=h, tips=False,
                  axis_config={"color": self.th["ejes"], "stroke_width": 3, "include_ticks": False}).move_to(centro)
        g = VGroup()
        if ylab:
            g.add(T(ylab, 22, self.th["txt2"], "BOLD").next_to(ax.y_axis, UP, buff=0.08))
        if xlab:
            g.add(T(xlab, 22, self.th["txt2"], "BOLD").next_to(ax.x_axis, DOWN, buff=0.12).align_to(ax.x_axis, RIGHT))
        return ax, g

    def nota(self, texto, color, pos, size=24):
        return self.tag(texto, color, size).move_to(pos)

    def cerrar(self, *mobs):
        self.cerrar_voz(0.05)
        self.limpiar(*mobs)


def portada_v(scene, preg, pieza_grande, sticker_txt, color_st="#FF4D6D", extra=None):
    """Portada vertical estilo F01: 3 líneas de pregunta, pieza real grande, sticker."""
    from miniaturas import sticker, logo_esq
    scene.add(Rectangle(width=9.2, height=16.4, stroke_width=0).set_fill("#000000", 1))
    cols = ["#FFFFFF", "#00E5FF", "#FFB020"]
    t = VGroup(*[T(l, 100, cols[i % 3], "HEAVY") for i, l in enumerate(preg)]).arrange(DOWN, buff=0.12)
    t.scale_to_fit_width(min(8.4, t.width)).move_to([0, 4.9, 0])
    if t.height > 3.4:
        t.scale_to_fit_height(3.4).move_to([0, 4.9, 0])
    pieza_grande.move_to([0, -0.9, 0])
    st = sticker(sticker_txt, color_st, size=56, ang=-0.03)
    st.scale_to_fit_width(min(st.width, 7.8)).move_to([0, -6.6, 0])
    scene.add(pieza_grande)
    if extra is not None:
        scene.add(extra)
    scene.add(t, st)
    logo_esq(scene, (3.6, 7.3))

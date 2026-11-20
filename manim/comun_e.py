"""
Estilo "Ing. Miguel Esquit · Electricidad": fondo blanco, líneas finas, ilustración técnica limpia.
Reutiliza voz ElevenLabs, efectos y música de comun_v.py.
  FORMATO=v (1080x1920, vertical)  |  FORMATO=h (1920x1080, YouTube)
Contornos con grosor constante en pixeles aunque la cámara haga zoom; los objetos "físicos"
(cables, tubos) marcados con fisico(m) sí crecen con el zoom, como en la vida real.
"""
import os
from comun_v import (audio, efectos, musica, np, Path, config)  # noqa: F401  (config ya importado por manim)
from manim import *
from manim.camera.camera import Camera

FORMATO = os.environ.get("FORMATO", "v")
# Voz por formato (ElevenLabs). Ambos con la voz clonada de Miguel; cambia aquí la de reels si se desea.
VOZ_MIGUEL = "GMbq1msYteTjwXUs4sky"
VOZ_ALBERTO = "l1zE9xgNpUTaQCZzpNJa"
VOCES = {"h": VOZ_MIGUEL, "v": VOZ_MIGUEL}
os.environ.setdefault("ELEVEN_VOZ_ID", VOCES[FORMATO])
SUFIJO_VOZ = os.environ["ELEVEN_VOZ_ID"][:6]
if FORMATO == "h":
    config.frame_width, config.frame_height = 16, 9
    if os.environ.get("PREVIEW"):
        config.pixel_width, config.pixel_height, config.frame_rate = 960, 540, 10
    else:
        config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 30
else:
    config.frame_width, config.frame_height = 9, 16
    if os.environ.get("PREVIEW"):
        config.pixel_width, config.pixel_height, config.frame_rate = 540, 960, 10
    else:
        config.pixel_width, config.pixel_height, config.frame_rate = 1080, 1920, 30

# ------------------------------------------------------------------ paleta
FONDO = "#FFFFFF"
REJILLA = "#EEF2F6"
TINTA = "#1D2939"        # texto principal
TINTA2 = "#5B6B7F"       # texto secundario
LINEA = "#344054"        # contornos
MARCA = "#0E9BB5"        # turquesa del logo
MARCA_CL = "#CDEBF2"     # celeste claro del logo
FASE = "#1B1B1B"         # NEC: fase (negro)
RETORNO = "#D92D20"      # retorno del interruptor (rojo, convención)
NEUTRO = "#FFFFFF"       # NEC 200.6: blanco o gris
NEUTRO_BORDE = "#98A2B3"
TIERRA = "#16A34A"       # NEC 250.119: verde o desnudo
ENERGIA = "#F79009"      # corriente / peligro
AMBAR = "#FDB022"
ROJO = "#E5484D"
VERDE_OK = "#12B76A"
METAL = "#D0D5DD"
METAL2 = "#98A2B3"
METAL_OSC = "#667085"
COBRE = "#C8773A"
LATON = "#C9A227"
PORCELANA = "#F7F4EC"
TEMA = os.environ.get("TEMA", "oscuro")   # desde 29-oct-2026 el canal usa fondo azul marino
CARTA = "#FFFFFF"        # relleno de tarjetas
if TEMA == "oscuro":     # fondo azul marino con degradado (referencia del usuario)
    FONDO = "#0B1C3D"
    REJILLA = "#16294F"
    TINTA = "#F2F4F7"
    TINTA2 = "#B9C2E3"
    CARTA = "#2B3A7A"      # tarjetas con contraste sobre el azul (pedido 30-oct)

if TEMA == "negro":      # fondo negro con cuadrícula (pedido 19-nov-2026, verticales y horizontales)
    FONDO = "#000000"
    REJILLA = "#161A21"
    TINTA = "#F2F4F7"
    TINTA2 = "#B8C0CC"
    CARTA = "#1A1E26"

SANS = "Inter"
MONO = "JetBrains Mono"
SEG = "DSEG7 Classic"
config.background_color = FONDO

DIR = Path(__file__).resolve().parent
KIT = Path("/home/claude/kit/videos_verticales")

# ------------------------------------------------------------------ grosor constante al hacer zoom
_orig_stroke = Camera.apply_stroke


def _stroke(self, ctx, vmobject, background=False):
    w = vmobject.get_stroke_width(background)
    if w == 0:
        return self
    if getattr(vmobject, "fisico", False):
        k = 1.0
    else:
        k = self.frame_width / config.frame_width
    self.set_cairo_context_color(ctx, self.get_stroke_rgbas(vmobject, background=background), vmobject)
    ctx.set_line_width(w * self.cairo_line_width_multiple * k)
    from manim.constants import LineJointType, CapStyleType
    from manim.camera.camera import LINE_JOIN_MAP, CAP_STYLE_MAP
    if vmobject.joint_type != LineJointType.AUTO:
        ctx.set_line_join(LINE_JOIN_MAP[vmobject.joint_type])
    if vmobject.cap_style != CapStyleType.AUTO:
        ctx.set_line_cap(CAP_STYLE_MAP[vmobject.cap_style])
    ctx.stroke_preserve()
    return self


Camera.apply_stroke = _stroke


def fisico(m):
    for s in m.family_members_with_points():
        s.fisico = True
    return m


# ------------------------------------------------------------------ texto
def T(texto, size=36, color=TINTA, peso="BOLD", fuente=SANS):
    return Text(texto, font=fuente, font_size=size, color=color, weight=peso)


def Tm(texto, size=30, color=TINTA, peso="MEDIUM"):
    return T(texto, size, color, peso, MONO)


def pastilla(texto, color=MARCA, size=28, solido=False):
    lum = ManimColor(color).to_rgb() @ np.array([0.299, 0.587, 0.114])
    t = T(texto, size, ("#10143A" if lum > 0.75 else WHITE) if solido else color, "BOLD")
    h = t.height + 0.3
    caja = RoundedRectangle(width=t.width + 0.5, height=h, corner_radius=h / 2, stroke_color=color, stroke_width=2)
    caja.set_fill(color, 1 if solido else 0.10)
    base = caja.copy().set_fill(FONDO if TEMA in ("oscuro", "negro") else WHITE, 1).set_stroke(width=0)
    return VGroup(base, caja, t.move_to(caja))


def tarjeta(ancho, alto, color=LINEA, relleno=None, r=0.18):
    relleno = relleno or CARTA
    if TEMA in ("oscuro", "negro") and isinstance(color, str) and color in (LINEA, METAL):
        color = "#4A5AA0"
    c = RoundedRectangle(width=ancho, height=alto, corner_radius=r, stroke_color=color, stroke_width=1.6)
    c.set_fill(relleno, 1)
    return c


def sombra(m, dx=0.06, dy=-0.08, op=0.10):
    s = m.copy().set_fill(BLACK, op).set_stroke(width=0).shift([dx, dy, 0])
    return s


def fuente(texto, pos=None, size=22):
    f = T("Fuente: " + texto, size, TINTA2, "MEDIUM").set_opacity(0.95)
    if pos is None:
        pos = [0, -4.55, 0] if FORMATO == "v" else [0, -4.15, 0]
    return f.move_to(pos)


def fondo_degradado(scene):
    """Degradado fijo (no se mueve con el zoom): azul noche a la izquierda, índigo/violeta a la derecha."""
    from PIL import Image
    ca = os.environ.get("FONDO_A", "08142E"); cb = os.environ.get("FONDO_B", "12305A")
    ruta = DIR / f"fondo_oscuro_{ca}_{cb}_{config.pixel_width}x{config.pixel_height}.png"
    if not ruta.exists():
        w, h = config.pixel_width, config.pixel_height
        x = np.linspace(0, 1, w)[None, :, None]
        y = np.linspace(0, 1, h)[:, None, None]
        a = np.array([int(ca[i:i + 2], 16) for i in (0, 2, 4)])[None, None, :]
        b = np.array([int(cb[i:i + 2], 16) for i in (0, 2, 4)])[None, None, :]
        t = np.clip(0.75 * x + 0.25 * y, 0, 1)
        img = (a * (1 - t) + b * t).astype(np.uint8)
        Image.fromarray(np.broadcast_to(img, (h, w, 3)).copy()).save(ruta)
    scene.camera.background_image = str(ruta)
    scene.camera.init_background()


def rejilla():
    w, h = config.frame_width * 3, config.frame_height * 3
    paso = 0.5
    g = VGroup(*[Line([x, -h / 2, 0], [x, h / 2, 0]) for x in np.arange(-w / 2, w / 2 + 0.01, paso)],
               *[Line([-w / 2, y, 0], [w / 2, y, 0]) for y in np.arange(-h / 2, h / 2 + 0.01, paso)])
    g.set_stroke(REJILLA, 1)
    return g


def encabezado(l1, l2, c2=MARCA, s1=46, s2=66):
    a = T(l1, s1, TINTA, "HEAVY")
    b = T(l2, s2, c2, "HEAVY")
    g = VGroup(a, b).arrange(DOWN, buff=0.14)
    for m in (a, b):
        if m.width > 7.6:
            m.scale_to_fit_width(7.6)
    g.move_to([0, 5.6, 0])
    barra = RoundedRectangle(width=1.2, height=0.09, corner_radius=0.045, stroke_width=0).set_fill(c2, 1)
    barra.next_to(g, DOWN, buff=0.18)
    return VGroup(g, barra)


def display(valor, unidad="", color=TINTA, size=70):
    num = T(valor, size, color, "NORMAL", SEG)
    sombra_ = T("".join("8" if ch.isdigit() else ch for ch in valor), size, color, "NORMAL", SEG).set_opacity(0.07)
    sombra_.move_to(num, aligned_edge=RIGHT)
    g = VGroup(sombra_, num)
    if unidad:
        g.add(T(unidad, int(size * 0.5), color, "BOLD").next_to(num, RIGHT, buff=0.15, aligned_edge=DOWN))
    return g


def resplandor(centro, r=1.0, color=AMBAR, capas=10, op=0.05):
    return VGroup(*[Circle(radius=r * (i + 1) / capas, stroke_width=0).set_fill(color, op).move_to(centro)
                    for i in range(capas)])


def rayo(a, b, color=ENERGIA, n=7, amp=0.16, semilla=0, w=4):
    a, b = np.array(a, float), np.array(b, float)
    d = b - a
    nrm = np.array([-d[1], d[0], 0]) / (np.linalg.norm(d) + 1e-9)
    rng = np.random.default_rng(semilla)
    pts = [a] + [a + d * k / n + nrm * amp * rng.uniform(-1, 1) for k in range(1, n)] + [b]
    m = VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(pts)
    return VGroup(m.copy().set_stroke(AMBAR, w * 3, 0.25), m, m.copy().set_stroke(WHITE, w * 0.35))


def simbolo_rayo(color=ENERGIA, h=0.6):
    p = Polygon([0.05, 0.5, 0], [-0.28, -0.05, 0], [-0.02, -0.05, 0], [-0.12, -0.5, 0], [0.3, 0.1, 0], [0.03, 0.1, 0],
                stroke_width=0).set_fill(color, 1)
    return p.scale_to_fit_height(h)


# ------------------------------------------------------------------ cables y tubos
def cable(*pts, color=FASE, w=6, suave=False):
    """Conductor aislado. El neutro (blanco) lleva borde gris para verse sobre fondo blanco."""
    m = VMobject()
    if suave:
        m.set_points_smoothly([np.array(p, float) for p in pts])
    else:
        m.set_points_as_corners([np.array(p, float) for p in pts])
    m.set_stroke(width=0).set_fill(opacity=0)
    if color == NEUTRO:
        g = VGroup(m.copy().set_stroke(NEUTRO_BORDE, w + 2.4), m.copy().set_stroke(WHITE, w))
    else:
        borde = interpolate_color(ManimColor(color), ManimColor(BLACK), 0.35)
        if TEMA in ("oscuro", "negro") and color == FASE:
            borde = "#8F9AC8"   # contorno claro para que el cable negro se vea sobre fondo oscuro
        g = VGroup(m.copy().set_stroke(borde, w + (2.6 if TEMA in ("oscuro", "negro") and color == FASE else 1.6)), m.copy().set_stroke(color, w))
    for s in g:
        s.set_cap_style(CapStyleType.ROUND)
        s.set_joint_type(LineJointType.ROUND)
    g.ruta = m
    return fisico(g)


def tubo(*pts, d=0.16):
    """Tubo EMT visto de frente: banda metálica con brillo."""
    m = VMobject().set_points_as_corners([np.array(p, float) for p in pts])
    escala = 120 * config.frame_width / 16 if FORMATO == "h" else 120
    w = d * 100  # unidades de stroke: 0.01 de unidad de Manim
    g = VGroup(m.copy().set_stroke(METAL_OSC, w + 2.5), m.copy().set_stroke(METAL, w),
               m.copy().set_stroke(WHITE, w * 0.22, 0.85).shift([0, d * 0.18, 0]))
    for s in g:
        s.set_joint_type(LineJointType.ROUND)
    g.ruta = m
    return fisico(g)


def _osc(c, k=0.4):
    return interpolate_color(ManimColor(c), ManimColor(BLACK), k)


def _cla(c, k=0.5):
    return interpolate_color(ManimColor(c), ManimColor(WHITE), k)


def abrazadera(p, vertical=False, d=0.16):
    """Abrazadera de un agujero (one-hole strap) sobre el tubo, con su tornillo."""
    banda = RoundedRectangle(width=d * 0.62, height=d * 1.75, corner_radius=d * 0.12, stroke_color=METAL_OSC,
                             stroke_width=1).set_fill("#C9CED6", 1)
    brillo = Line([-d * 0.12, -d * 0.7, 0], [-d * 0.12, d * 0.7, 0], stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.8)
    pie = RoundedRectangle(width=d * 0.62, height=d * 0.75, corner_radius=d * 0.1, stroke_color=METAL_OSC,
                           stroke_width=1).set_fill("#B8BEC8", 1).shift([0, d * 1.2, 0])
    tor = tornillo(d * 0.2, "#D0D5DD", 0.5).move_to(pie)
    g = VGroup(pie, banda, brillo, tor)
    if vertical:
        g.rotate(PI / 2)
    return g.move_to(p)


def conector(p, angulo=0, d=0.16):
    """Conector EMT de tornillo (set-screw) + contratuerca dentada, entrando a una caja por la derecha."""
    cuerpo = RoundedRectangle(width=d * 1.7, height=d * 1.3, corner_radius=d * 0.12, stroke_color=METAL_OSC,
                              stroke_width=1).set_fill("#BFC5CE", 1)
    anillo = Rectangle(width=d * 0.28, height=d * 1.5, stroke_color=METAL_OSC, stroke_width=1).set_fill("#AEB5BF", 1)
    anillo.next_to(cuerpo, RIGHT, buff=0)
    dientes = []
    h = d * 2.0
    n = 6
    for k in range(n + 1):
        y = -h / 2 + h * k / n
        dientes += [[0, y, 0], [d * 0.14, y + h / (2 * n), 0]] if k < n else [[0, y, 0]]
    tuerca = Polygon(*dientes[:-1], [0, h / 2, 0], [-d * 0.18, h / 2, 0], [-d * 0.18, -h / 2, 0],
                     stroke_color=METAL_OSC, stroke_width=1).set_fill("#9AA2AE", 1)
    tuerca.next_to(anillo, RIGHT, buff=0)
    tor = tornillo(d * 0.24, "#D9DDE3", 0.3).move_to(cuerpo).shift([-d * 0.15, 0, 0])
    brillo = Line([-d * 0.75, d * 0.42, 0], [d * 0.6, d * 0.42, 0], stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.8)
    g = VGroup(cuerpo, brillo, anillo, tuerca, tor)
    g.rotate(angulo)
    return g.move_to(p)


def tornillo(r=0.09, color=LATON, ranura=0, cruz=True):
    """Tornillo de cabeza redonda (binding head) con ranura combinada, borde oscuro y brillo.
    Índices: [0] cabeza, [1] ranuras (gira al apretar), [2] brillo."""
    borde = _osc(color, 0.45)
    c = Circle(radius=r, stroke_color=borde, stroke_width=1.1).set_fill(color, 1)
    interior = Circle(radius=r * 0.78, stroke_width=0).set_fill(_cla(color, 0.18), 1)
    w = max(1.0, r * 22)
    rs = VGroup(Line([-r * 0.62, 0, 0], [r * 0.62, 0, 0], stroke_color=_osc(color, 0.6), stroke_width=w))
    if cruz:
        rs.add(Line([0, -r * 0.42, 0], [0, r * 0.42, 0], stroke_color=_osc(color, 0.6), stroke_width=w))
    rs.rotate(ranura)
    brillo = Arc(radius=r * 0.62, start_angle=PI * 0.55, angle=PI * 0.5, stroke_color=WHITE, stroke_width=max(0.8, r * 14),
                 stroke_opacity=0.75)
    return VGroup(VGroup(c, interior), rs, brillo)


def borne(c, r=0.06, color=LATON, plato=True):
    """Tornillo de terminal con su placa de presión (como en interruptores y tomacorrientes)."""
    t = tornillo(r, color, 0.5).move_to(c)
    if not plato:
        return t
    placa = RoundedRectangle(width=r * 2.9, height=r * 2.9, corner_radius=r * 0.3, stroke_color=_osc(color, 0.45),
                             stroke_width=1).set_fill(_osc(color, 0.12), 1).move_to(c)
    g = VGroup(placa, t)
    g.tor = t
    return g


def punta_pelada(ruta, largo=0.08, w=2.6, gancho=0.0):
    """Extremo pelado de cobre al final de una ruta (y opcional gancho alrededor del tornillo)."""
    pts = ruta.get_points()
    fin = ruta.get_end()
    d = fin - ruta.point_from_proportion(0.995)
    d = d / (np.linalg.norm(d) + 1e-9)
    g = VGroup(Line(fin - d * largo, fin).set_stroke(_osc(COBRE, 0.3), w + 1.2), Line(fin - d * largo, fin).set_stroke(COBRE, w))
    # hilos torcidos del cable (7 hilos): rayitas diagonales sobre el cobre
    n_ = np.array([-d[1], d[0], 0])
    an = w / 100 * 0.5
    for t in np.linspace(0.15, 0.85, 4):
        p0 = fin - d * largo * t
        g.add(Line(p0 - n_ * an - d * an * 0.6, p0 + n_ * an + d * an * 0.6).set_stroke(_osc(COBRE, 0.45), max(0.6, w * 0.25)))
    if gancho:
        a0 = np.arctan2(-d[1], -d[0])
        arc = Arc(radius=gancho, start_angle=a0 + 0.3, angle=-TAU * 0.8, arc_center=fin).set_stroke(COBRE, w)
        g.add(arc.copy().set_stroke(_osc(COBRE, 0.3), w + 1.2), arc)
    for s in g:
        s.set_cap_style(CapStyleType.ROUND)
    return fisico(g)


def destornillador(largo=1.6):
    mango = RoundedRectangle(width=0.34, height=largo * 0.45, corner_radius=0.12, stroke_color="#B42318",
                             stroke_width=1.4).set_fill("#F04438", 1)
    estr = VGroup(*[Line([x, -largo * 0.2, 0], [x, largo * 0.2, 0], stroke_color="#B42318", stroke_width=1)
                    for x in (-0.07, 0, 0.07)])
    vastago = Rectangle(width=0.07, height=largo * 0.55, stroke_color=METAL_OSC, stroke_width=1).set_fill(METAL, 1)
    vastago.next_to(mango, DOWN, buff=0)
    punta = Polygon([-0.035, 0, 0], [0.035, 0, 0], [0.015, -0.08, 0], [-0.015, -0.08, 0], stroke_width=0).set_fill(METAL_OSC, 1)
    punta.next_to(vastago, DOWN, buff=0)
    g = VGroup(vastago, punta, mango, estr.move_to(mango))
    return g  # la punta queda abajo: g[1].get_bottom()


# ------------------------------------------------------------------ escena base con voz
class Escena(MovingCameraScene):
    GUION: dict = {}
    CARPETA_VOZ = "voz"
    REJILLA = True

    def setup(self):
        super().setup()
        efectos(DIR / "sfx")
        self.camera.background_color = FONDO
        if TEMA == "oscuro":
            fondo_degradado(self)
        if self.REJILLA:
            self.add(rejilla())
        self.srt = []

    def voz(self, clave):
        wav, dur = audio(DIR / f"{self.CARPETA_VOZ}_{SUFIJO_VOZ}", clave, self.GUION[clave])
        inicio = self.renderer.time
        self.add_sound(str(wav))
        self.fin_voz = inicio + dur
        pal = self.GUION[clave].split()
        bloques = [" ".join(pal[i:i + 7]) for i in range(0, len(pal), 7)]
        pesos = np.array([len(b) + 4 for b in bloques], float)
        lim = inicio + np.concatenate([[0], np.cumsum(pesos) / pesos.sum() * dur])
        self.srt += [(a, z, b) for b, a, z in zip(bloques, lim[:-1], lim[1:])]
        return dur

    def resta(self):
        return self.fin_voz - self.renderer.time

    def cerrar_voz(self, extra=-0.2):
        w = self.fin_voz - self.renderer.time + extra
        if w > 0.02:
            self.wait(w)

    def sfx(self, nombre, gain=-10):
        self.add_sound(str(DIR / "sfx" / f"{nombre}.wav"), gain=gain)

    def tear_down(self):
        import json
        (DIR / f"{type(self).__name__}.srt.json").write_text(json.dumps(self.srt, ensure_ascii=False))

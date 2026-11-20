"""Piezas recreadas desde la documentación oficial del fabricante de referencia (SIN logo ni nombre comercial).
Escala común: 1 unidad Manim = 18 mm (un módulo DIN) cuando s = 1.

Referencias (hojas de datos oficiales, ver referencias/LEEME.md del repo):
- Contactor tamaño S00, 3 polos, 7 A AC-3/400 V (3 kW), bobina 24 V DC 4 W, 1 NA integrado 13-14:
  45 mm ancho × 58 mm alto × 73 mm fondo; bornes 1/L1 3/L2 5/L3 → 2/T1 4/T2 6/T3, A1(+) A2(−), 13 14;
  conductor 0,5–4 mm² (AWG 20–12); montaje en riel 35 mm (EN 60715).
- Relé de sobrecarga térmico tamaño S00, clase 10, montaje directo al contactor, ajuste 3,5–5 A (otros: 4,5–6,3 / 5,5–8 / 7–10 A);
  1 NC 95-96 + 1 NA 97-98; TEST, STOP, RESET manual/automático, indicador de posición; borne de bobina repetido (A2); 45 mm de ancho.
- Módulo lógico 12/24 V DC, 8 entradas digitales (4 usables 0–10 V), 4 salidas a relé 10 A resistiva / 3 A inductiva;
  71,5 × 90 × 60 mm, 4 módulos DIN, display, Ethernet.
- Variador compacto 380–480 V tamaño AA (0,55–2,2 kW): 73 mm ancho × 181 mm alto; bornes de potencia abajo
  (L1 L2 L3 PE / U2 V2 W2 PE / DCP/R1 R2); bornera de control al frente detrás de puertas; panel en -X21, USB -X22.
"""
from piezas_auto2 import *
from piezas_auto2 import _texto_sobre
from piezas_proteccion import breaker_din, breaker_on, GRIS_BK, GRIS_FR, NEGRO_P, ROJO_OFF

MM = 1 / 18.0                 # unidades por mm a s = 1
SIR_CUERPO = "#D9DDE2"        # gris claro de la carcasa
SIR_LUZ = "#EEF0F3"
SIR_SOMBRA = "#AEB4BC"
SIR_FRENTE = "#C7CCD3"
SIR_OSC = "#3B4250"           # bocas de bornes / zonas oscuras
TXT_PZ = "#1D2939"
AZUL_DC = "#1F5FD6"           # cableado de mando en DC (IEC 60204-1: azul)
NEGRO_POT = "#15171B"         # potencia (IEC 60204-1: negro)
VERDE_AM = ("#2E9E44", "#F2C200")  # PE verde/amarillo


def borne_t(nombre, x, y, s, r=1.8, etiqueta=True, arriba=True, h_txt=1.6, bh=7.6):
    """Borne con tornillo combinado visto de frente dentro de su boca; etiqueta impresa encima o debajo."""
    boca = RoundedRectangle(width=7.2 * MM * s, height=bh * MM * s, corner_radius=1.2 * MM * s, stroke_width=0).set_fill(SIR_OSC, 1)
    boca.move_to([x, y, 0])
    tor = tornillo_frente(r * MM * s).move_to([x, y, 0])
    g = VGroup(boca, tor)
    if etiqueta:
        t = tx(nombre, h_txt * MM * s, TXT_PZ)
        t.move_to([x, y + ((bh / 2 + 2.4) if arriba else -(bh / 2 + 2.4)) * MM * s, 0])
        g.add(t)
        g.txt = t
    g.tor = tor
    g.nombre = nombre
    g.p = np.array([x, y, 0])
    return g


def _caja(w, h, s, color=SIR_CUERPO, r=2.0):
    sh = RoundedRectangle(width=w * MM * s, height=h * MM * s, corner_radius=r * MM * s, stroke_width=0).set_fill(BLACK, 0.35).shift(RIGHT * 1.2 * MM * s + DOWN * 1.5 * MM * s)
    c = RoundedRectangle(width=w * MM * s, height=h * MM * s, corner_radius=r * MM * s, stroke_color=SIR_SOMBRA, stroke_width=1.3).set_fill(color, 1)
    luz = Line(c.get_corner(UL) + RIGHT * r * MM * s + DOWN * 0.6 * MM * s, c.get_corner(UR) + LEFT * r * MM * s + DOWN * 0.6 * MM * s).set_stroke(SIR_LUZ, 2)
    return VGroup(sh, c, luz)


CT_CUERPO = "#566170"        # gris pizarra (referencia del usuario, sin marca y con el tono ligeramente cambiado)
CT_FRENTE = "#677385"
CT_BORDE = "#2E343D"
CT_BOCA = "#262B33"
CT_TXT = "#F2F4F7"


def _caja_ct(w, h, s, color=CT_CUERPO, r=2.0):
    sh = RoundedRectangle(width=w * MM * s, height=h * MM * s, corner_radius=r * MM * s, stroke_width=0).set_fill(BLACK, 0.45).shift(RIGHT * 1.2 * MM * s + DOWN * 1.5 * MM * s)
    c = RoundedRectangle(width=w * MM * s, height=h * MM * s, corner_radius=r * MM * s, stroke_color=CT_BORDE, stroke_width=1.4).set_fill(color, 1)
    luz = Line(c.get_corner(UL) + RIGHT * r * MM * s + DOWN * 0.6 * MM * s, c.get_corner(UR) + LEFT * r * MM * s + DOWN * 0.6 * MM * s).set_stroke("#8A96A8", 2)
    return VGroup(sh, c, luz)


def borne_ct(nombre, x, y, s, arriba=True, h_txt=1.7, r=2.3, bw=8.0, bh=8.4):
    boca = RoundedRectangle(width=bw * MM * s, height=bh * MM * s, corner_radius=1.2 * MM * s, stroke_color="#1A1E24", stroke_width=0.8).set_fill(CT_BOCA, 1).move_to([x, y, 0])
    tor = tornillo_frente(r * MM * s).move_to([x, y, 0])
    g = VGroup(boca, tor)
    t = tx(nombre, h_txt * MM * s, CT_TXT).move_to([x, y + ((bh / 2 + 2.2) if arriba else -(bh / 2 + 2.2)) * MM * s, 0])
    g.add(t)
    g.txt, g.tor, g.nombre = t, tor, nombre
    return g


def contactor_s00(s=1.0, ref="KM1"):
    """Contactor tamaño S00 de frente (45 × 58 mm), disposición de la hoja de datos oficial:
    arriba 1/L1 3/L2 5/L3 13NO A1+ ; abajo 2/T1 4/T2 6/T3 14NO A2−.
    Atributos: .b[nombre], .ind (indicador de posición), .placa"""
    W, H = 45, 58
    g = _caja_ct(W, H, s)
    xs = [-18, -9, 0, 9, 18]
    b = {}
    for x, n in zip(xs, ["1/L1", "3/L2", "5/L3", "13", "A1"]):
        b[n] = borne_ct(n, x * MM * s, (H / 2 - 10.5) * MM * s, s, arriba=True)
    for x, n in zip(xs, ["2/T1", "4/T2", "6/T3", "14", "A2"]):
        b[n] = borne_ct(n, x * MM * s, (-H / 2 + 10.5) * MM * s, s, arriba=False)
    b["13"].txt.become(tx("13NO", 1.5 * MM * s, CT_TXT).move_to(b["13"].txt))
    b["14"].txt.become(tx("14NO", 1.5 * MM * s, CT_TXT).move_to(b["14"].txt))
    b["A1"].txt.become(tx("A1+", 1.7 * MM * s, "#FF8A8A").move_to(b["A1"].txt))
    b["A2"].txt.become(tx("A2−", 1.7 * MM * s, "#8AB4FF").move_to(b["A2"].txt))
    for k in b.values():
        g.add(k)
    # frente: indicador de posición (ranura con pivote) a la izquierda, rótulo abajo a la izquierda, rejillas a la derecha
    fr = RoundedRectangle(width=41 * MM * s, height=21 * MM * s, corner_radius=1.4 * MM * s, stroke_color=CT_BORDE, stroke_width=1).set_fill(CT_FRENTE, 1).move_to([0, 0, 0])
    ven = RoundedRectangle(width=12 * MM * s, height=11 * MM * s, corner_radius=1 * MM * s, stroke_color="#1A1E24", stroke_width=1).set_fill("#2B3038", 1).move_to([-10 * MM * s, 3.5 * MM * s, 0])
    ind = RoundedRectangle(width=4 * MM * s, height=7 * MM * s, corner_radius=0.8 * MM * s, stroke_width=0).set_fill("#E4E7EB", 1).move_to(ven.get_center() + UP * 1.2 * MM * s)
    placa = RoundedRectangle(width=20 * MM * s, height=6.5 * MM * s, corner_radius=0.6 * MM * s, stroke_color="#98A2B3", stroke_width=0.8).set_fill(WHITE, 1).move_to([-8 * MM * s, -6 * MM * s, 0])
    pt = tx(f"-{ref}", 3.2 * MM * s, TXT_PZ).move_to(placa)
    rejas = VGroup(*[RoundedRectangle(width=6 * MM * s, height=2.6 * MM * s, corner_radius=0.4 * MM * s, stroke_color="#1A1E24", stroke_width=0.8).set_fill("#4A5361", 1).move_to([13 * MM * s, y * MM * s, 0]) for y in (6, 0.5)])
    datos = VGroup(tx("24 V DC", 1.5 * MM * s, CT_TXT), tx("7 A AC-3", 1.5 * MM * s, CT_TXT)).arrange(DOWN, buff=0.6 * MM * s).move_to([12 * MM * s, -6 * MM * s, 0])
    g.add(fr, ven, ind, placa, pt, rejas, datos)
    g.add(Rectangle(width=20 * MM * s, height=1.6 * MM * s, stroke_width=0).set_fill("#8A929E", 1).move_to([0, -H / 2 * MM * s - 0.8 * MM * s, 0]))
    g.b, g.ind, g.placa, g.ven, g.s, g.W, g.H = b, ind, placa, ven, s, W * MM * s, H * MM * s
    g.on = False
    return g


def contactor_cerrar(ct, on=True):
    """Indicador de posición: abajo y verde = cerrado; arriba y blanco = abierto."""
    d = (-2.4 if on else 2.4) * MM * ct.s
    ct.on = on
    return ct.ind.animate.shift(UP * d).set_fill("#12B76A" if on else "#E4E7EB", 1)


def termico_s00(s=1.0, ref="F2", rango=(3.5, 5.0), ajuste=3.9):
    """Relé de sobrecarga tamaño S00 (montaje directo), según el dibujo dimensional oficial: 45 mm × 61,7 mm.
    Cinco pines arriba que entran en 2/T1 4/T2 6/T3 14 A2 del contactor; repite A2 y 14/22.
    Frente: rótulo, TEST/indicador, STOP, RESET (M/A), dial; fila media 95 96 97 98 14/22; fila inferior 2/T1 4/T2 6/T3 A2.
    Atributos: .b, .dial, .aguja, .test, .reset, .stop"""
    W, H = 45, 61.7
    g = _caja_ct(W, H, s)
    b = {}
    for x, n in zip([-18, -9, 0, 9, 18], ["95", "96", "97", "98", "14/22"]):
        b[n] = borne_ct(n, x * MM * s, -9.5 * MM * s, s, arriba=True, h_txt=1.5, bw=7.6, bh=8.0)
    for x, n in zip([-15.5, -5.5, 4.5, 15.5], ["2/T1", "4/T2", "6/T3", "A2"]):
        b[n] = borne_ct(n, x * MM * s, -23.8 * MM * s, s, arriba=False, h_txt=1.5, bw=8.4, bh=8.0)
    b["A2"].txt.become(tx("A2−", 1.5 * MM * s, "#8AB4FF").move_to(b["A2"].txt))
    g.add(Line([-21 * MM * s, -17.2 * MM * s, 0], [21 * MM * s, -17.2 * MM * s, 0]).set_stroke("#3A414C", 1.4))
    for k in b.values():
        g.add(k)
    placa = RoundedRectangle(width=17 * MM * s, height=6 * MM * s, corner_radius=0.6 * MM * s, stroke_color="#98A2B3", stroke_width=0.8).set_fill(WHITE, 1).move_to([-11 * MM * s, 23 * MM * s, 0])
    g.add(placa, tx(f"-{ref}", 3 * MM * s, TXT_PZ).move_to(placa))
    # TEST (corredera) e indicador arriba a la derecha
    test = RoundedRectangle(width=6 * MM * s, height=3 * MM * s, corner_radius=0.6 * MM * s, stroke_color="#7A271A", stroke_width=1).set_fill("#E5484D", 1).move_to([10 * MM * s, 23.5 * MM * s, 0])
    g.add(RoundedRectangle(width=9 * MM * s, height=4.4 * MM * s, corner_radius=0.8 * MM * s, stroke_width=0).set_fill(CT_BOCA, 1).move_to([10 * MM * s, 23.5 * MM * s, 0]), test,
          tx("TEST", 1.3 * MM * s, CT_TXT).move_to([17.5 * MM * s, 23.5 * MM * s, 0]))
    # STOP y RESET (M/A) a la izquierda, dial grande a la derecha
    stop = Circle(radius=3.0 * MM * s, stroke_color="#7A271A", stroke_width=1).set_fill("#C0392B", 1).move_to([-16 * MM * s, 9 * MM * s, 0])
    reset = Circle(radius=3.4 * MM * s, stroke_color="#1849A9", stroke_width=1).set_fill("#2F6FD0", 1).move_to([-7 * MM * s, 9 * MM * s, 0])
    g.add(stop, tx("STOP", 1.25 * MM * s, CT_TXT).next_to(stop, DOWN, buff=0.7 * MM * s), reset,
          tx("M", 1.6 * MM * s, WHITE).move_to(reset.get_center() + LEFT * 1.3 * MM * s), tx("A", 1.6 * MM * s, WHITE).move_to(reset.get_center() + RIGHT * 1.3 * MM * s),
          tx("RESET", 1.25 * MM * s, CT_TXT).next_to(reset, DOWN, buff=0.7 * MM * s))
    cx, cy = 10 * MM * s, 8 * MM * s
    aro = Circle(radius=8.2 * MM * s, stroke_color="#1A1E24", stroke_width=1.4).set_fill("#E9EBEF", 1).move_to([cx, cy, 0])
    dial = Circle(radius=5.4 * MM * s, stroke_color="#475467", stroke_width=1.2).set_fill("#2F6FD0", 1).move_to([cx, cy, 0])
    ranura = Line(LEFT * 4.2 * MM * s, RIGHT * 4.2 * MM * s).set_stroke(WHITE, 3.2 * s).move_to([cx, cy, 0])
    a0, a1 = PI * 1.2, -PI * 0.2
    escala = VGroup()
    for v in np.linspace(rango[0], rango[1], 4):
        ang = a0 + (a1 - a0) * (v - rango[0]) / (rango[1] - rango[0])
        p = np.array([cx, cy, 0]) + 7.0 * MM * s * np.array([np.cos(ang), np.sin(ang), 0])
        escala.add(tx(f"{v:.1f}".replace(".", ","), 1.25 * MM * s, TXT_PZ).move_to(p))
    ang = a0 + (a1 - a0) * (ajuste - rango[0]) / (rango[1] - rango[0])
    aguja = VGroup(ranura, Triangle().set_fill(WHITE, 1).set_stroke(width=0).scale(0.9 * MM * s).move_to([cx, cy, 0] + RIGHT * 4.6 * MM * s))
    aguja.rotate(ang, about_point=np.array([cx, cy, 0]))
    g.add(aro, dial, escala, aguja, tx("A", 1.4 * MM * s, CT_TXT).move_to([cx + 8 * MM * s, cy - 7 * MM * s, 0]),
          tx("CLASS 10", 1.2 * MM * s, CT_TXT).move_to([-11.5 * MM * s, 1.5 * MM * s, 0]))
    # pines superiores (se ven solo si el relé está suelto)
    pines = VGroup(*[Rectangle(width=1.6 * MM * s, height=9 * MM * s, stroke_width=0).set_fill("#C9A227", 1).move_to([x * MM * s, (H / 2 + 4.5) * MM * s, 0]) for x in (-18, -9, 0, 9, 18)])
    g.add_to_back(pines)
    g.b, g.dial, g.aguja, g.test, g.stop, g.reset, g.s, g.pines = b, dial, aguja, test, stop, reset, s, pines
    g.rango, g.ajuste, g.c_dial, g.a0, g.a1 = rango, ajuste, np.array([cx, cy, 0]), a0, a1
    return g


def ajustar_termico(r, valor):
    ang_act = r.a0 + (r.a1 - r.a0) * (r.ajuste - r.rango[0]) / (r.rango[1] - r.rango[0])
    ang = r.a0 + (r.a1 - r.a0) * (valor - r.rango[0]) / (r.rango[1] - r.rango[0])
    r.ajuste = valor
    return Rotate(r.aguja, ang - ang_act, about_point=r.dial.get_center())


def arrancador_s00(s=1.0, rango=(3.5, 5.0), ajuste=3.9):
    """Contactor + relé montado debajo: los 5 pines del relé entran en 2/T1 4/T2 6/T3 14 A2 (que quedan tapados)."""
    ct = contactor_s00(s)
    r = termico_s00(s, rango=rango, ajuste=ajuste)
    r.move_to(ct[1].get_bottom() + DOWN * (61.7 / 2 - 4) * MM * s)
    r.match_x(ct[1])
    r.shift(RIGHT * (ct[1].get_center()[0] - r[2].get_center()[0]) if False else ORIGIN)
    for n in ("2/T1", "4/T2", "6/T3", "14", "A2"):
        ct.b[n].set_opacity(0)
    r.pines.set_opacity(0)
    g = VGroup(ct, r)
    g.ct, g.r = ct, r
    return g


def fuente_24v(s=1.0, ref="T1"):
    """Fuente conmutada para riel DIN, 24 V DC (frente): entrada L N PE arriba, salida + + − − abajo, LED DC OK, potenciómetro."""
    W, H = 52, 90
    g = _caja(W, H, s, color="#C9CED6")
    b = {}
    for x, n in zip((-15, -3, 11), ("L", "N", "PE")):
        b[n] = borne_t(n, x * MM * s, (H / 2 - 9) * MM * s, s)
    for x, n in zip((-18, -7, 7, 18), ("+", "+ ", "−", "− ")):
        b[n] = borne_t(n.strip(), x * MM * s, (-H / 2 + 9) * MM * s, s, arriba=False)
    for k in b.values():
        g.add(k)
    rej = VGroup(*[Line([-20 * MM * s, y * MM * s, 0], [20 * MM * s, y * MM * s, 0]).set_stroke("#9AA3AF", 2.2 * s) for y in np.arange(8, 26, 3)])
    led = Circle(radius=1.4 * MM * s, stroke_width=0).set_fill("#1E4D2E", 1).move_to([-12 * MM * s, -10 * MM * s, 0])
    pot = VGroup(Circle(radius=2.4 * MM * s, stroke_color="#475467", stroke_width=1).set_fill("#E4E7EB", 1), Line(LEFT * 1.8 * MM * s, RIGHT * 1.8 * MM * s).set_stroke("#344054", 1.6)).move_to([6 * MM * s, -10 * MM * s, 0])
    placa = RoundedRectangle(width=34 * MM * s, height=10 * MM * s, corner_radius=0.6 * MM * s, stroke_color="#98A2B3", stroke_width=0.8).set_fill(WHITE, 1).move_to([0, -0 * MM * s, 0])
    g.add(rej, placa, tx(f"-{ref}", 3 * MM * s, TXT_PZ).move_to(placa.get_center() + UP * 1.6 * MM * s),
          tx("IN 120–230 V~  OUT 24 V DC 2,5 A", 1.25 * MM * s, "#475467").move_to(placa.get_center() + DOWN * 2.4 * MM * s),
          led, tx("DC OK", 1.3 * MM * s, TXT_PZ).next_to(led, DOWN, buff=0.6 * MM * s), pot, tx("24–28 V", 1.3 * MM * s, TXT_PZ).next_to(pot, DOWN, buff=0.6 * MM * s))
    g.b, g.led, g.s = b, led, s
    return g


def bornera(nombres, s=1.0, ref="X1", pe=()):
    """Bornera de paso (bornes de 6 mm de ancho) con número impreso; los PE en verde/amarillo. Bornes arriba y abajo."""
    g = VGroup()
    b_sup, b_inf = {}, {}
    paso = 6.2
    x0 = -paso * (len(nombres) - 1) / 2
    for k, n in enumerate(nombres):
        x = (x0 + k * paso) * MM * s
        es_pe = n in pe
        cuerpo = RoundedRectangle(width=5.8 * MM * s, height=46 * MM * s, corner_radius=0.8 * MM * s, stroke_color="#7C8594", stroke_width=0.8).set_fill("#9DA5B0" if not es_pe else VERDE_AM[0], 1).move_to([x, 0, 0])
        g.add(cuerpo)
        if es_pe:
            for yy in np.arange(-20, 21, 6):
                g.add(Line([x - 2.8 * MM * s, (yy - 2) * MM * s, 0], [x + 2.8 * MM * s, (yy + 2) * MM * s, 0]).set_stroke(VERDE_AM[1], 3.2 * s))
        tag = RoundedRectangle(width=5 * MM * s, height=5 * MM * s, corner_radius=0.4 * MM * s, stroke_width=0).set_fill(WHITE, 1).move_to([x, 0, 0])
        g.add(tag, tx(n, 1.7 * MM * s, TXT_PZ).move_to(tag))
        ts = tornillo_frente(1.6 * MM * s).move_to([x, 15 * MM * s, 0])
        ti = tornillo_frente(1.6 * MM * s).move_to([x, -15 * MM * s, 0])
        g.add(ts, ti)
        b_sup[n] = VGroup(ts); b_sup[n].p = ts.get_center()
        b_inf[n] = VGroup(ti); b_inf[n].p = ti.get_center()
    tapa = Rectangle(width=2 * MM * s, height=46 * MM * s, stroke_width=0).set_fill("#6B7280", 1).next_to(g, RIGHT, buff=0)
    g.add(tapa, tx(f"-{ref}", 3 * MM * s, WHITE).next_to(g, LEFT, buff=1.5 * MM * s))
    g.sup, g.inf = b_sup, b_inf
    return g


def riel_din(largo, s=1.0):
    r = VGroup(Rectangle(width=largo, height=35 * MM * s, stroke_width=0).set_fill("#A9B0BA", 1),
               Rectangle(width=largo, height=25 * MM * s, stroke_width=0).set_fill("#C9CED6", 1))
    for x in np.arange(-largo / 2 + 0.3, largo / 2, 0.9):
        r.add(RoundedRectangle(width=10 * MM * s, height=5 * MM * s, corner_radius=2.4 * MM * s, stroke_width=0).set_fill("#7C8594", 1).move_to([x, 0, 0]))
    return r


def canaleta(largo, alto=40, s=1.0, vertical=False):
    """Canaleta ranurada gris (vista de frente con la tapa puesta)."""
    w, h = (largo, alto * MM * s) if not vertical else (alto * MM * s, largo)
    c = VGroup(Rectangle(width=w, height=h, stroke_color="#7C8594", stroke_width=1).set_fill("#B7BDC6", 1))
    n = int((largo) / (8 * MM * s))
    for k in range(n):
        f = -largo / 2 + (k + 0.5) * largo / n
        if not vertical:
            c.add(Line([f, h / 2, 0], [f, h / 2 - 5 * MM * s, 0]).set_stroke("#8A929E", 1.6), Line([f, -h / 2, 0], [f, -h / 2 + 5 * MM * s, 0]).set_stroke("#8A929E", 1.6))
        else:
            c.add(Line([w / 2, f, 0], [w / 2 - 5 * MM * s, f, 0]).set_stroke("#8A929E", 1.6), Line([-w / 2, f, 0], [-w / 2 + 5 * MM * s, f, 0]).set_stroke("#8A929E", 1.6))
    c.add(Rectangle(width=w - 6 * MM * s, height=h - 6 * MM * s, stroke_width=0).set_fill("#C3C8CF", 1))
    return c


def pulsador_22(color="verde", s=1.0, ref="S1", texto="I", contacto=("13", "14"), luminoso=False):
    """Pulsador de 22 mm en la puerta (frente): aro metálico, botón rasante del color IEC 60204-1 y portaetiqueta.
    Detrás, módulo de contacto con sus dos bornes (se dibuja aparte con modulo_contacto)."""
    cols = {"verde": ("#12B76A", "#05603A"), "rojo": ("#E5484D", "#7A271A"), "ambar": ("#F79009", "#93370D"), "blanco": ("#F2F4F7", "#667085")}
    c, co = cols[color]
    aro = Circle(radius=15 * MM * s, stroke_color="#667085", stroke_width=1.6).set_fill("#D0D5DD", 1)
    aro2 = Circle(radius=12.5 * MM * s, stroke_color="#98A2B3", stroke_width=1).set_fill("#2B2F36", 1)
    bot = Circle(radius=11 * MM * s, stroke_color=co, stroke_width=1.4).set_fill(c, 1)
    brillo = Arc(radius=8 * MM * s, start_angle=PI * 0.6, angle=PI * 0.5).set_stroke(WHITE, 2.4 * s, 0.55)
    sim = tx(texto, 7 * MM * s, WHITE if color != "blanco" else TXT_PZ)
    g = VGroup(aro, aro2, bot, brillo, sim)
    if luminoso:
        lente = VGroup(*[Circle(radius=(9 - 2.5 * k) * MM * s, stroke_color=co, stroke_width=0.8).set_fill(opacity=0) for k in range(3)])
        g.add(lente)
    porta = RoundedRectangle(width=26 * MM * s, height=8 * MM * s, corner_radius=0.8 * MM * s, stroke_color="#98A2B3", stroke_width=0.8).set_fill(WHITE, 1).next_to(aro, DOWN, buff=3 * MM * s)
    g.add(porta, tx(ref, 3 * MM * s, TXT_PZ).move_to(porta))
    g.boton, g.col, g.s = bot, c, s
    return g


def modulo_contacto(n1, n2, s=1.0, nc=False):
    """Módulo de contacto para pulsador (vista posterior): cuerpo con dos bornes y la indicación NA/NC."""
    g = _caja(12, 30, s, color="#E4E7EB", r=1.5)
    b = {n1: borne_t(n1, 0, 8 * MM * s, s, r=1.5, h_txt=1.4), n2: borne_t(n2, 0, -8 * MM * s, s, r=1.5, arriba=False, h_txt=1.4)}
    g.add(*b.values(), RoundedRectangle(width=8 * MM * s, height=4 * MM * s, corner_radius=0.5 * MM * s, stroke_width=0).set_fill("#B42318" if nc else "#12B76A", 1).move_to([0, 0, 0]),
          tx("NC" if nc else "NO", 1.4 * MM * s, WHITE).move_to([0, 0, 0]))
    g.b = b
    return g


def caja_bornes_motor(s=1.0, conexion="delta"):
    """Placa de bornes IEC de un motor de 6 terminales: U1 V1 W1 arriba, W2 U2 V2 abajo + PE.
    'delta': puentes verticales U1-W2, V1-U2, W1-V2. 'estrella': puente horizontal W2-U2-V2."""
    W, H = 70, 52
    g = VGroup(RoundedRectangle(width=W * MM * s, height=H * MM * s, corner_radius=3 * MM * s, stroke_color="#25455E", stroke_width=2).set_fill("#3E6A8C", 1),
               RoundedRectangle(width=(W - 8) * MM * s, height=(H - 8) * MM * s, corner_radius=2 * MM * s, stroke_width=0).set_fill("#E8E2D0", 1))
    b = {}
    for k, (n_up, n_dn) in enumerate((("U1", "W2"), ("V1", "U2"), ("W1", "V2"))):
        x = (-17 + 17 * k) * MM * s
        for n, y in ((n_up, 8), (n_dn, -10)):
            esp = VGroup(Circle(radius=4.2 * MM * s, stroke_color="#7A5A10", stroke_width=1).set_fill(LATON, 1), RegularPolygon(6).scale(2.6 * MM * s).set_fill("#B08A1E", 1).set_stroke("#6E520E", 1))
            esp.move_to([x, y * MM * s, 0])
            t = tx(n, 2.4 * MM * s, TXT_PZ).move_to([x, (y + (7 if y > 0 else -7)) * MM * s, 0])
            g.add(esp, t)
            b[n] = VGroup(esp); b[n].p = esp.get_center()
    pe = VGroup(Circle(radius=3 * MM * s, stroke_width=0).set_fill(LATON, 1)).move_to([27 * MM * s, -18 * MM * s, 0])
    g.add(pe, tierra_icono(2.5 * MM * s * 3).next_to(pe, UP, buff=0.8 * MM * s))
    b["PE"] = pe; b["PE"].p = pe.get_center()
    puentes = VGroup()
    if conexion == "delta":
        for a_, z_ in (("U1", "W2"), ("V1", "U2"), ("W1", "V2")):
            puentes.add(RoundedRectangle(width=5 * MM * s, height=24 * MM * s, corner_radius=1 * MM * s, stroke_color="#7A4A16", stroke_width=1).set_fill(COBRE, 0.9).move_to((b[a_].p + b[z_].p) / 2))
    else:
        puentes.add(RoundedRectangle(width=40 * MM * s, height=5 * MM * s, corner_radius=1 * MM * s, stroke_color="#7A4A16", stroke_width=1).set_fill(COBRE, 0.9).move_to((b["W2"].p + b["V2"].p) / 2))
    g.add(puentes)
    g.b, g.puentes = b, puentes
    return g


def tierra_icono(h=0.3, color=TXT_PZ):
    l1 = Line(UP * h / 2, ORIGIN)
    ls = VGroup(*[Line(LEFT * h * (0.5 - 0.15 * k), RIGHT * h * (0.5 - 0.15 * k)).shift(DOWN * h * 0.17 * k) for k in range(3)])
    return VGroup(l1, ls).set_stroke(color, max(1.2, h * 6))


def placa_datos_motor(s=1.0):
    """Placa de datos del motor del ejemplo (1 hp, 230 Δ / 400 Y V, 60 Hz)."""
    g = VGroup(RoundedRectangle(width=4.2 * s, height=2.3 * s, corner_radius=0.08 * s, stroke_color="#667085", stroke_width=1.5).set_fill("#E7E9EC", 1))
    filas = [("3~ MOTOR", "IEC 60034"), ("1 hp  0,75 kW", "60 Hz"), ("230 Δ / 400 Y V", "3,9 / 2,25 A"), ("1720 rpm", "cos φ 0,80"), ("S.F. 1,15", "IP55  Cl. F")]
    for k, (a, b_) in enumerate(filas):
        y = 0.82 * s - k * 0.42 * s
        g.add(tx(a, 0.2 * s, TXT_PZ).move_to([-0.95 * s, y, 0]), tx(b_, 0.2 * s, TXT_PZ).move_to([1.1 * s, y, 0]))
    for (x, y) in ((-1.95, 0.98), (1.95, 0.98), (-1.95, -0.98), (1.95, -0.98)):
        g.add(Circle(radius=0.06 * s, stroke_width=0).set_fill("#98A2B3", 1).move_to([x * s, y * s, 0]))
    return g


def cable_ruta(pts, color=NEGRO_POT, w=5, borde=True):
    """Conductor (vista de tablero) con esquinas redondeadas y borde claro para leerse sobre fondo oscuro."""
    pts = [np.array(p, float) for p in pts]
    m = VMobject().set_points_as_corners(pts)
    m.joint_type = LineJointType.ROUND
    m.set_stroke(color, w)
    if borde:
        b = m.copy().set_stroke("#9AA6C8" if color in (NEGRO_POT, AZUL_DC) else "#FFFFFF", w + 2.2, 0.75)
        return VGroup(b, m)
    return VGroup(m)


def marcador(texto, p, s=1.0, color=WHITE):
    """Marcador de cable (anillo con número) en la punta del conductor."""
    r = RoundedRectangle(width=max(6, 2.2 * len(texto) + 2) * MM * s, height=3.6 * MM * s, corner_radius=0.6 * MM * s, stroke_color="#667085", stroke_width=0.8).set_fill(color, 1)
    return VGroup(r, tx(texto, 2.0 * MM * s, TXT_PZ).move_to(r)).move_to(p)

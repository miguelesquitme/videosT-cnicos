"""Fotocontrol de alumbrado público (ANSI C136.10, base de giro de 3 patas) dibujado pieza por pieza, con medidas reales.
Fuentes:
- JL-205C (hoja de datos Long-Join / prideled / csc-led): Ø84 × 66 mm, ≈85 g; sensor fototransistor/fotodiodo; MOV; retardo;
  falla encendido; empaque de espuma o silicona (IP54–IP67); se instala con la ventana al NORTE (marca en la tapa);
  se gira a la derecha para trabar; prueba de día con cinta negra opaca (no el dedo), ≈2 min.
- NSi "Photocontrols catalog" serie 5200: cubierta de polipropileno estabilizado UV con color ANSI por tensión (gris 105–130 V);
  ventana de acrílico transparente resistente a UV; base de policarbonato/fenólico; patas de latón macizo; sensor CdS o de silicio;
  relé de CD en los electrónicos; MOV 255/360 J; enciende a 1,5 fc ±0,2; relación apagado/encendido 1,5:1; enciende al instante,
  apaga con 3–5 s de retardo; falla encendido. Cableado: negro = línea, rojo = carga, blanco = neutro.
- Intermatic K122 (receptáculo de giro ANSI C136.10): Ø65 mm × 54,1 mm, fenólico negro, contactos de latón/bronce fosforado,
  empaque integrado, hilos 14 AWG 105 °C.
Todas las funciones devuelven (svg, puntos_mm, (W, H)) como svgref: los puntos sirven para anclar llamadas en Manim.
"""
import math
from svgref import svg_mm, T, R, logo

DEFS_F = """<defs>
 <linearGradient id="fCub" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5D636B"/><stop offset="0.18" stop-color="#9AA1AA"/>
  <stop offset="0.36" stop-color="#B9C0C8"/><stop offset="0.62" stop-color="#8E959E"/><stop offset="1" stop-color="#4E535A"/></linearGradient>
 <linearGradient id="fCubT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9CFD6"/><stop offset="1" stop-color="#9AA1AA"/></linearGradient>
 <linearGradient id="fBase" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121315"/><stop offset="0.22" stop-color="#3A3D42"/>
  <stop offset="0.4" stop-color="#4A4E54"/><stop offset="0.7" stop-color="#26282C"/><stop offset="1" stop-color="#0D0E10"/></linearGradient>
 <linearGradient id="fLaton" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A6A1E"/><stop offset="0.3" stop-color="#F1D27A"/>
  <stop offset="0.55" stop-color="#D2A944"/><stop offset="1" stop-color="#7C5C16"/></linearGradient>
 <radialGradient id="fLatonR" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#F6DC8C"/><stop offset="0.7" stop-color="#C99B36"/><stop offset="1" stop-color="#8A6A1E"/></radialGradient>
 <linearGradient id="fVent" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2B3A48"/><stop offset="0.5" stop-color="#3E5163"/><stop offset="1" stop-color="#1B2530"/></linearGradient>
 <linearGradient id="fPcb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F7A3E"/><stop offset="1" stop-color="#14602F"/></linearGradient>
 <radialGradient id="fPcbR" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#2A8E4C"/><stop offset="1" stop-color="#145C2D"/></radialGradient>
 <radialGradient id="fMov" cx="0.38" cy="0.34" r="0.75"><stop offset="0" stop-color="#5A8FE0"/><stop offset="0.7" stop-color="#1F55B5"/><stop offset="1" stop-color="#143C86"/></radialGradient>
 <linearGradient id="fRele" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2F3237"/><stop offset="1" stop-color="#141518"/></linearGradient>
 <linearGradient id="fCapF" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E2503C"/><stop offset="1" stop-color="#A52B1E"/></linearGradient>
 <radialGradient id="fElec" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#3B3F46"/><stop offset="1" stop-color="#111215"/></radialGradient>
 <radialGradient id="fEpoxi" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="0.5" stop-color="#D8E6F0" stop-opacity="0.7"/><stop offset="1" stop-color="#9DB3C4" stop-opacity="0.8"/></radialGradient>
 <radialGradient id="fCds" cx="0.4" cy="0.35" r="0.75"><stop offset="0" stop-color="#F3EEE4"/><stop offset="1" stop-color="#CFC5B2"/></radialGradient>
 <linearGradient id="fAlu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7EAED"/><stop offset="0.45" stop-color="#B8BEC5"/><stop offset="1" stop-color="#868D95"/></linearGradient>
 <linearGradient id="fPoste" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7D848B"/><stop offset="0.35" stop-color="#D5DADF"/><stop offset="0.6" stop-color="#A9B0B7"/><stop offset="1" stop-color="#6B7178"/></linearGradient>
 <linearGradient id="fRefr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDE7EE"/><stop offset="1" stop-color="#AFC0CC"/></linearGradient>
 <linearGradient id="fCono" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE9A8" stop-opacity="0.85"/><stop offset="1" stop-color="#FFE9A8" stop-opacity="0"/></linearGradient>
 <linearGradient id="fCobreB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8C4A1E"/><stop offset="0.35" stop-color="#E8A06A"/><stop offset="1" stop-color="#8C4A1E"/></linearGradient>
</defs>"""

COLORES_ANSI = {"gris": ("#5D636B", "#9AA1AA", "#B9C0C8", "#4E535A")}   # 105–130 V (NSi): solo se usa el gris (120 V)


def _sombra(cont, f="sDura"):
    return f'<g filter="url(#{f})">{cont}</g>'


# ============================================================ FOTOCONTROL: vista de frente (Ø84 × 66 mm + patas)
def fotocontrol(transparente=False, cinta=False, ancho_mm=84.0):
    """Vista de frente (ventana hacia el observador, que es el NORTE). Escala 10 px = 1 mm.
    Cubierta gris (ANSI 105–130 V) con domo, ventana de acrílico, datos impresos, base negra, empaque y 3 patas de latón."""
    Wp, Hp = 840, 760
    s = ancho_mm / Wp
    c, p = [DEFS_F], {}
    # --- patas de latón (bajo la base): una al frente y dos a ±120° (se ven más cortas por la perspectiva)
    for x, w, osc in ((230, 46, 0.35), (420, 74, 0.0), (610, 46, 0.35)):
        c.append(_sombra(f'<path d="M{x - w / 2},620 h{w} v78 h{w * 0.55} v20 h-{w * 1.55} Z" fill="url(#fLaton)"/>', "sTorn"))
        if osc:
            c.append(f'<path d="M{x - w / 2},620 h{w} v78 h{w * 0.55} v20 h-{w * 1.55} Z" fill="#000" opacity="{osc}"/>')
    p["pata"] = (420, 690)
    # --- empaque (espuma negra) bajo la base
    c.append(R(40, 612, 760, 16, "#0B0B0C") + R(40, 612, 760, 4, "#2A2B2E"))
    p["empaque"] = (720, 620)
    # --- base negra (policarbonato/fenólico) con aro de agarre
    c.append(_sombra(R(0, 470, 840, 145, "url(#fBase)"), "sCuerpo"))
    for x in range(30, 830, 34):
        c.append(R(x, 486, 10, 112, "#000", 'opacity="0.35"') + R(x + 10, 486, 4, 112, "#6A6F76", 'opacity="0.35"'))
    c.append(R(0, 470, 840, 10, "#5B6067", 'opacity="0.6"'))
    p["base"] = (110, 545)
    # --- cubierta (polipropileno UV, gris = 105–130 V) con domo
    tapa = 'M30,470 L30,205 C30,95 180,52 420,50 C660,52 810,95 810,205 L810,470 Z'
    op = 0.38 if transparente else 1
    c.append(_sombra(f'<path d="{tapa}" fill="url(#fCub)" opacity="{op}"/>', "sCuerpo") if not transparente
             else f'<path d="{tapa}" fill="url(#fCub)" opacity="{op}" stroke="#C9CFD6" stroke-width="3"/>')
    # domo: elipse superior iluminada y brillo vertical
    c.append(f'<path d="M30,205 C30,95 180,52 420,50 C660,52 810,95 810,205 C700,165 560,150 420,150 C280,150 140,165 30,205 Z" fill="url(#fCubT)" opacity="{0.55 * op:.2f}"/>')
    c.append(f'<path d="M180,120 C175,250 175,380 182,465 L232,465 C226,380 226,250 232,95 Z" fill="#FFFFFF" opacity="{0.16 * op:.2f}"/>')
    c.append(R(30, 455, 780, 15, "#3E434A", f'opacity="{0.8 * op:.2f}"'))
    # marca del NORTE en el domo
    c.append(f'<polygon points="420,66 404,100 436,100" fill="#2B2F35" opacity="{op}"/>' + T(420, 122, "N", 26, "#2B2F35", 900))
    p["norte"] = (420, 95)
    # --- interior visible (solo en el corte transparente)
    if transparente:
        c.append(_interior_frente())
    # --- ventana de acrílico (con el sensor detrás)
    c.append(_sombra(R(330, 200, 180, 130, "url(#fVent)"), "sTorn"))
    c.append(R(330, 200, 180, 8, "#0E141A", 'opacity="0.6"'))
    c.append(f'<rect x="402" y="245" width="36" height="46" fill="#C4D3DE" opacity="0.55"/>'
             f'<circle cx="420" cy="252" r="18" fill="url(#fEpoxi)" opacity="0.8"/>')
    c.append('<polygon points="338,322 380,208 410,208 368,322" fill="#FFFFFF" opacity="0.22"/>'
             '<polygon points="420,322 450,208 462,208 432,322" fill="#FFFFFF" opacity="0.14"/>')
    p["ventana"] = (420, 265)
    p["sensor"] = (420, 252)
    if cinta:   # prueba de día: cinta negra opaca sobre la ventana
        c.append(_sombra('<polygon points="305,188 538,182 541,342 302,348" fill="#111214"/>', "sTorn")
                 + '<polygon points="305,188 538,182 539,196 306,202" fill="#2C2E32"/>')
        p["cinta"] = (420, 265)
    # --- datos impresos (blanco sobre la cubierta) y logo del canal
    if not transparente:
        c.append(T(420, 368, "120 V~ 60 Hz", 24, "#FFFFFF", 800) + T(420, 400, "1000 W · 1800 VA", 21, "#F2F4F7", 700)
                 + T(420, 428, "ANSI C136.10", 19, "#E4E7EC", 700))
        c.append(logo(700, 380, 46))
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=6)
    return svg, {k: (x * s, y * s) for k, (x, y) in p.items()}, WH


def _interior_frente():
    """Corte: la tarjeta vertical vista a través de la cubierta (componentes de frente)."""
    c = []
    c.append(_sombra(R(80, 160, 680, 300, "url(#fPcb)"), "sTorn"))
    for y in (200, 240, 400):
        c.append(f'<path d="M100,{y} H300 L330,{y + 20} H700" stroke="#C8A951" stroke-width="5" fill="none" opacity="0.55"/>')
    # relé
    c.append(_sombra(R(540, 250, 190, 175, "url(#fRele)")) + T(635, 300, "K1", 26, "#E4E7EC", 800))
    # varistor
    c.append(_sombra('<circle cx="190" cy="330" r="82" fill="url(#fMov)"/>') + T(190, 330, "MOV", 30, "#E8EEF8", 800))
    # capacitor de película
    c.append(_sombra(R(300, 350, 200, 90, "url(#fCapF)")))
    return "".join(c)


# ============================================================ FOTOCONTROL: vista de abajo (3 patas de giro)
def fotocontrol_abajo(ancho_mm=84.0, rot=0.0):
    """Base vista desde abajo: empaque, 3 patas curvas de latón a 120°, y su función. rot en grados (giro de traba)."""
    Wp = Hp = 900
    s = ancho_mm / 840
    cx = cy = 450
    c, p = [DEFS_F], {}
    c.append(_sombra(f'<circle cx="{cx}" cy="{cy}" r="420" fill="url(#fBase)"/>', "sCuerpo"))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="400" fill="none" stroke="#0A0A0B" stroke-width="34"/>')   # empaque
    c.append(f'<circle cx="{cx}" cy="{cy}" r="382" fill="none" stroke="#2C2E32" stroke-width="3"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="300" fill="#24262A"/>')
    g = []
    r = 215
    for k, (nombre, ang) in enumerate((("linea", 90), ("carga", 330), ("neutro", 210))):  # vista de abajo = espejo del receptáculo
        a0, a1 = math.radians(ang - 17), math.radians(ang + 17)
        x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        g.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" stroke="url(#fLatonR)" stroke-width="44" fill="none" stroke-linecap="butt"/>')
        g.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" stroke="#FFF1BE" stroke-width="6" fill="none" opacity="0.6"/>')
        am = math.radians(ang + rot)
        p[nombre] = (cx + r * math.cos(am), cy - r * math.sin(am))
    c.append(f'<g transform="rotate({-rot} {cx} {cy})" filter="url(#sTorn)">{"".join(g)}</g>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="#3A3D42"/>')
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=4)
    return svg, {k: (x * s, y * s) for k, (x, y) in p.items()}, WH


# ============================================================ RECEPTÁCULO de giro (Ø65 mm, fenólico negro) visto de arriba
def receptaculo(ancho_mm=65.0):
    """Receptáculo ANSI C136.10 de 3 contactos (Intermatic K122: Ø65 mm, fenólico negro, contactos de latón).
    Se ve de arriba, con los 3 hilos 14 AWG saliendo por abajo: negro = línea, rojo = carga, blanco = neutro."""
    Wp, Hp = 1100, 900
    s = ancho_mm / 650
    cx, cy = 550, 400
    c, p = [DEFS_F], {}
    # hilos (por debajo del cuerpo, salen hacia abajo)
    hil = (("linea", 90, "#151515", 440), ("carga", 210, "#C62828", 300), ("neutro", 330, "#F4F4F2", 800))
    for nombre, ang, col, xf in hil:
        a = math.radians(ang)
        x0, y0 = cx + 250 * math.cos(a), cy - 250 * math.sin(a) + 120
        c.append(f'<path d="M{x0:.0f},{y0:.0f} C{x0:.0f},{y0 + 260:.0f} {xf},{cy + 300} {xf},{Hp - 40}" stroke="#0006" stroke-width="40" fill="none" transform="translate(6,10)"/>')
        c.append(f'<path d="M{x0:.0f},{y0:.0f} C{x0:.0f},{y0 + 260:.0f} {xf},{cy + 300} {xf},{Hp - 40}" stroke="{col}" stroke-width="36" fill="none"/>')
        c.append(f'<path d="M{x0 - 8:.0f},{y0:.0f} C{x0 - 8:.0f},{y0 + 260:.0f} {xf - 8},{cy + 300} {xf - 8},{Hp - 40}" stroke="#FFFFFF" stroke-width="6" fill="none" opacity="0.25"/>')
        p["h_" + nombre] = (xf, Hp - 60)
    # cuerpo
    c.append(_sombra(f'<circle cx="{cx}" cy="{cy}" r="325" fill="url(#fBase)"/>', "sCuerpo"))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="300" fill="#1E2023"/><circle cx="{cx}" cy="{cy}" r="300" fill="none" stroke="#3B3F45" stroke-width="5"/>')
    r = 165
    for nombre, ang, col, _ in hil:
        a0, a1 = math.radians(ang - 19), math.radians(ang + 19)
        x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        c.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" stroke="#050505" stroke-width="44" fill="none"/>')
        c.append(f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" stroke="url(#fLatonR)" stroke-width="12" fill="none" transform="translate(0,6)"/>')
        a = math.radians(ang)
        p[nombre] = (cx + r * math.cos(a), cy - r * math.sin(a))
    for ang in (30, 150, 270):   # tornillos de la tapa trasera
        a = math.radians(ang)
        x, y = cx + 250 * math.cos(a), cy - 250 * math.sin(a)
        c.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="#8D949B"/><rect x="{x - 10:.0f}" y="{y - 3:.0f}" width="20" height="6" fill="#3A3D42"/>')
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=4)
    return svg, {k: (x * s, y * s) for k, (x, y) in p.items()}, WH


# ============================================================ INTERIOR: tarjeta electrónica vista de arriba (sin cubierta)
def tarjeta(ancho_mm=84.0, rele_on=False):
    """Base abierta vista de arriba: tarjeta (Ø≈74 mm) con sensor junto a la ventana (arriba = norte), fuente
    (capacitor de película, puente de diodos, electrolítico, resistencias), relé de CD K1 y varistor (MOV)."""
    Wp = Hp = 900
    s = ancho_mm / 840
    cx, cy = 450, 450
    c, p = [DEFS_F], {}
    c.append(_sombra(f'<circle cx="{cx}" cy="{cy}" r="420" fill="url(#fBase)"/>', "sCuerpo"))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="372" fill="url(#fPcbR)"/>')
    # pistas de cobre bajo la máscara
    pistas = ["M300,230 H420 V330", "M560,520 V600 H650", "M240,560 H380 L420,600 H520", "M610,300 H700 V430",
              "M330,700 H560", "M260,420 H360", "M520,360 H600"]
    for d in pistas:
        c.append(f'<path d="{d}" stroke="#2FA35A" stroke-width="14" fill="none" stroke-linejoin="round"/>')
    for x, y in ((300, 230), (420, 330), (650, 600), (520, 600), (240, 560), (700, 430), (330, 700), (560, 700), (260, 420), (360, 420), (600, 360)):
        c.append(f'<circle cx="{x}" cy="{y}" r="11" fill="#D9D3C4"/><circle cx="{x}" cy="{y}" r="4" fill="#6E6A60"/>')
    # sensor (fototransistor en epoxi transparente) asomado a la ventana, arriba
    c.append(R(420, 112, 60, 18, "#1A1C1F"))    # portasensor
    c.append(_sombra(f'<rect x="432" y="118" width="36" height="58" fill="url(#fEpoxi)"/><circle cx="450" cy="118" r="18" fill="url(#fEpoxi)"/>', "sTorn"))
    c.append(R(437, 176, 6, 34, "#C9CED3") + R(457, 176, 6, 34, "#C9CED3"))
    c.append(T(510, 150, "Q1", 22, "#FFFFFF", 800, "start"))
    p["sensor"] = (450, 140)
    c.append(R(380, 70, 140, 14, "#4B6A84", 'opacity="0.85"'))     # ventana (borde norte)
    p["ventana"] = (450, 77)
    # fuente: capacitor de película (rojo), puente de 4 diodos, electrolítico, resistencias
    c.append(_sombra(R(230, 250, 170, 110, "url(#fCapF)")) + T(315, 305, "C1", 24, "#FFFFFF", 800))
    for k in range(4):
        x, y = 250 + (k % 2) * 90, 450 + (k // 2) * 60
        c.append(_sombra(R(x, y, 64, 26, "#18191B"), "sTorn") + R(x + 50, y, 9, 26, "#C9CED3"))
    c.append(T(320, 432, "D1–D4", 20, "#FFFFFF", 800))
    c.append(_sombra(f'<circle cx="320" cy="640" r="52" fill="url(#fElec)"/>') +
             f'<path d="M320,588 A52,52 0 0 1 366,615 L320,640 Z" fill="#8D949B" opacity="0.8"/>'
             f'<path d="M300,640 H340 M320,620 V660" stroke="#5C6168" stroke-width="5"/>' + T(320, 718, "C2", 22, "#FFFFFF", 800))
    for k, x in enumerate((460, 520)):
        c.append(_sombra(f'<rect x="{x}" y="620" width="26" height="80" fill="#D8C29B"/>', "sTorn"))
        for j, col in enumerate(("#7A3E16", "#111111", "#C62828", "#C9A227")):
            c.append(R(x, 632 + j * 15, 26, 7, col))
    c.append(T(505, 730, "R1 R2", 20, "#FFFFFF", 800))
    p["fuente"] = (330, 480)
    # relé de CD (K1) con su símbolo impreso
    c.append(_sombra(R(560, 380, 200, 160, "url(#fRele)")))
    c.append(T(660, 412, "K1", 26, "#E4E7EC", 800))
    c.append(f'<rect x="590" y="440" width="34" height="56" fill="none" stroke="#C9CED3" stroke-width="4"/>'
             f'<line x1="590" y1="440" x2="624" y2="496" stroke="#C9CED3" stroke-width="3"/>'
             f'<path d="M660,500 V476 L{702 if rele_on else 712},{448 if rele_on else 458} M700,450 V430" stroke="#C9CED3" stroke-width="4" fill="none"/>')
    p["rele"] = (660, 460)
    # varistor (MOV) azul doblado sobre la tarjeta
    c.append(_sombra(f'<circle cx="610" cy="245" r="88" fill="url(#fMov)"/>') + T(610, 245, "MOV", 30, "#E8EEF8", 800))
    p["mov"] = (610, 245)
    # remaches de latón de las 3 patas con su hilo soldado
    hil = (("linea", 90, "#151515"), ("carga", 210, "#C62828"), ("neutro", 330, "#F4F4F2"))
    for nombre, ang, col in hil:
        a = math.radians(ang + 180)   # vistas desde arriba, las patas quedan reflejadas
        x, y = cx + 300 * math.cos(a), cy - 300 * math.sin(a)
        c.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="30" fill="url(#fLatonR)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#8A6A1E"/>')
        p["r_" + nombre] = (x, y)
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=4)
    return svg, {k: (x * s, y * s) for k, (x, y) in p.items()}, WH


# ============================================================ SENSORES sueltos
def celda_cds(ancho_mm=12.0):
    """Fotorresistencia de sulfuro de cadmio: disco cerámico con la pista CdS en serpentín (naranja) y dos patas."""
    Wp, Hp = 400, 600
    s = ancho_mm / 400
    c = [DEFS_F]
    c.append(R(150, 330, 14, 260, "#C9CED3") + R(236, 330, 14, 260, "#C9CED3"))
    c.append(_sombra('<circle cx="200" cy="200" r="190" fill="url(#fCds)"/>', "sCuerpo"))
    c.append('<circle cx="200" cy="200" r="150" fill="#E6DCC6"/>')
    d = "M80,110 " + " ".join(f"H320 V{130 + 40 * k} H80 V{150 + 40 * k}" for k in range(0, 5, 1))
    c.append(f'<path d="M80,110 H320 V150 H80 V190 H320 V230 H80 V270 H320" stroke="#D2691E" stroke-width="20" fill="none"/>')
    c.append(R(50, 90, 26, 200, "#C9CED3") + R(324, 110, 26, 200, "#C9CED3"))
    c.append('<circle cx="200" cy="200" r="190" fill="#FFFFFF" opacity="0.1"/>')
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=1)
    return svg, {}, WH


def fototransistor(alto_mm=30.0):
    """Fototransistor de silicio en encapsulado de epoxi transparente de 5 mm (lente) con 2 patas: colector y emisor."""
    Wp, Hp = 300, 900
    s = alto_mm / 900
    c = [DEFS_F]
    c.append(R(100, 400, 18, 480, "#C9CED3") + R(182, 400, 18, 500, "#C9CED3"))
    c.append(_sombra('<path d="M50,420 V160 A100,100 0 0 1 250,160 V420 H268 V450 H32 V420 Z" fill="url(#fEpoxi)"/>', "sCuerpo"))
    c.append(R(92, 270, 40, 140, "#BFC6CC") + R(160, 250, 50, 160, "#BFC6CC"))
    c.append('<rect x="120" y="230" width="48" height="40" fill="#2B2F35"/><path d="M146,250 Q170,200 182,250" stroke="#E4E7EC" stroke-width="4" fill="none"/>')
    c.append('<path d="M90,110 Q120,70 160,66" stroke="#FFFFFF" stroke-width="14" fill="none" opacity="0.8"/>')
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=1)
    return svg, {}, WH


# ============================================================ RELÉ de CD en corte (bobina, armadura y contacto)
def rele_corte(on=False, ancho_mm=60.0):
    """Relé de tarjeta en corte: bobina de cobre en su carrete, núcleo, armadura con resorte y contacto NA
    (común → NA). on=True: la bobina atrae la armadura y el contacto cierra."""
    Wp, Hp = 900, 700
    s = ancho_mm / 900
    c, p = [DEFS_F], {}
    c.append(R(40, 40, 820, 560, "#1B1D21", 'opacity="0.25" stroke="#8D949B" stroke-width="6"'))   # carcasa transparente
    c.append(R(40, 600, 820, 40, "#2B2E33"))                                                              # base
    for x in (180, 300, 620, 760):
        c.append(R(x, 640, 22, 60, "#C9CED3"))                                                            # pines
    # yugo (hierro) en L y núcleo
    c.append(R(120, 120, 40, 470, "#6B7178") + R(120, 560, 360, 30, "#6B7178"))
    c.append(R(260, 150, 70, 410, "#7D848B"))
    # carrete y bobina de cobre
    c.append(R(210, 200, 170, 22, "#1A1C1F") + R(210, 540, 170, 22, "#1A1C1F"))
    c.append(R(225, 222, 140, 318, "url(#fCobreB)"))
    for y in range(226, 536, 12):
        c.append(f'<line x1="225" y1="{y}" x2="365" y2="{y}" stroke="#7A3E16" stroke-width="3" opacity="0.6"/>')
    p["bobina"] = (295, 380)
    # armadura (pivota en la esquina del yugo) y resorte
    ang = 0 if on else -9
    arm = (f'<g transform="rotate({ang} 140 120)">{R(140, 110, 480, 34, "#9AA1AA")}'
           f'<path d="M560,144 V250" stroke="#C9A227" stroke-width="16"/>'       # lámina del común
           f'<circle cx="560" cy="262" r="18" fill="#E8E8E8" stroke="#A8A8A8" stroke-width="3"/></g>')
    c.append(arm)
    c.append('<path d="M450,110 l-12,-14 l24,-14 l-24,-14 l24,-14 l-12,-14" stroke="#B8BEC5" stroke-width="5" fill="none"/>')
    # contacto fijo NA
    c.append(R(520, 300, 200, 18, "#C9A227") + '<circle cx="560" cy="296" r="18" fill="#E8E8E8" stroke="#A8A8A8" stroke-width="3"/>')
    c.append(R(700, 300, 20, 340, "#C9A227"))
    c.append(R(610, 140, 18, 500, "#C9A227"))
    p["contacto"] = (560, 285)
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=3)
    return svg, {k: (x * s, y * s) for k, (x, y) in p.items()}, WH


# ============================================================ LUMINARIA tipo cobra en poste, con el fotocontrol arriba
def luminaria(encendida=False, ancho_mm=900.0):
    """Luminaria de alumbrado público vista de lado (aluminio, refractor abajo), brazo y poste galvanizado.
    El receptáculo va en la parte superior y el fotocontrol se ve montado encima."""
    Wp, Hp = 1800, 2200
    s = ancho_mm / Wp
    c, p = [DEFS_F], {}
    if encendida:
        c.append('<polygon points="900,520 1500,520 1820,2200 520,2200" fill="url(#fCono)"/>')
    # poste y brazo
    c.append(_sombra(R(130, 360, 90, 1840, "url(#fPoste)"), "sCuerpo"))
    c.append(_sombra('<path d="M175,420 C175,330 260,300 420,300 H700 V340 H430 C300,340 220,360 220,430 Z" fill="url(#fPoste)"/>'))
    # cuerpo de la luminaria (cabeza tipo cobra)
    c.append(_sombra('<path d="M640,300 C640,270 700,250 820,250 H1350 C1560,250 1640,330 1640,420 C1640,470 1600,500 1520,500 H820 C700,500 640,460 640,420 Z" fill="url(#fAlu)"/>', "sCuerpo"))
    c.append('<path d="M700,300 H1580" stroke="#FFFFFF" stroke-width="10" opacity="0.5"/>')
    c.append(R(650, 330, 60, 120, "#9AA1AA"))
    # refractor / lente LED
    luz = "#FFF3C4" if encendida else "#B9C7D2"
    c.append(f'<path d="M860,500 H1520 C1500,560 1440,585 1350,585 H980 C910,585 870,560 860,500 Z" fill="{luz}" stroke="#8D949B" stroke-width="6"/>')
    if encendida:
        c.append('<path d="M880,505 H1500 C1480,550 1430,570 1350,570 H985 C925,570 890,550 880,505 Z" fill="#FFFFFF" opacity="0.8"/>')
    p["lente"] = (1190, 545)
    # receptáculo y fotocontrol encima (a escala: Ø84 mm)
    k = 1 / s   # px por mm
    xr, yr = 1110, 250
    c.append(R(xr - 33 * k, yr - 22 * k, 66 * k, 22 * k, "#1E2023"))
    c.append(_sombra(R(xr - 42 * k, yr - 22 * k - 66 * k, 84 * k, 66 * k, "url(#fCub)", ''), "sTorn"))
    c.append(R(xr - 42 * k, yr - 22 * k - 15 * k, 84 * k, 15 * k, "url(#fBase)"))
    c.append(R(xr - 10 * k, yr - 22 * k - 50 * k, 20 * k, 14 * k, "url(#fVent)"))
    p["foto"] = (xr, yr - 22 * k - 33 * k)
    svg, WH = svg_mm(Wp, Hp, s, "".join(c), margen=10)
    return svg, {k_: (x * s, y * s) for k_, (x, y) in p.items()}, WH


CATALOGO = {
    "fc_frente": lambda: fotocontrol(),
    "fc_corte": lambda: fotocontrol(transparente=True),
    "fc_cinta": lambda: fotocontrol(cinta=True),
    "fc_abajo": lambda: fotocontrol_abajo(),
    "fc_abajo_g": lambda: fotocontrol_abajo(rot=35),
    "receptaculo": lambda: receptaculo(),
    "tarjeta": lambda: tarjeta(),
    "tarjeta_on": lambda: tarjeta(rele_on=True),
    "cds": lambda: celda_cds(),
    "fototr": lambda: fototransistor(),
    "rele_off": lambda: rele_corte(False),
    "rele_on": lambda: rele_corte(True),
    "lum_off": lambda: luminaria(False),
    "lum_on": lambda: luminaria(True),
}

if __name__ == "__main__":
    import sys
    from render_svg import render_lote, margen_de
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/fc"
    sel = sys.argv[2].split(",") if len(sys.argv) > 2 else list(CATALOGO)
    lote = []
    for n in sel:
        r = CATALOGO[n]()
        lote.append((n, r, margen_de(r[0])))
    render_lote(lote, out, px_mm=int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    print("ok", out)

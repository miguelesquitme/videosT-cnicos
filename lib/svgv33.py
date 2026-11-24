"""V33 v2 · ¿Qué significa IP65? Piezas reales.
Fuentes (referencias/v33_fuentes.md): IEC 60529:2013 (calibres 50 / 12,5 / 2,5 / 1,0 mm; dedo articulado de 12 mm × 80 mm;
5 y 6: cámara de polvo con vacío, 6 sin depósito de polvo; 5: boquilla 6,3 mm, 12,5 L/min ±5 %, 2,5–3 m, 1 min/m² mín. 3 min;
6: 12,5 mm, 100 L/min; 7: 1 m (envolventes < 850 mm) por 30 min; X = cifra no especificada); Hammond 1554 (policarbonato UL94 V-0,
IP66, empaque de silicona en lengüeta y ranura, tornillos M4 de acero inoxidable cautivos con insertos de acero inoxidable,
gris RAL 7035); LAPP SKINTOP (IP68; M20 × 1,5: 7–13 mm; rosca 17 mm; par de la tuerca 12 N·m); Oriental Motor (IP65/66/67)."""
import math
from svgv2 import pieza, sombra, T, R, tornillo


def gabinete(flojo=False):
    """Gabinete de policarbonato gris (RAL 7035) visto de frente: tapa con 4 tornillos M4 de acero inoxidable en las
    esquinas, nervadura y placa de datos IP66. flojo=True: un tornillo sobresale y la tapa no asienta."""
    Wp, Hp = 1200, 1200
    c, p = [], {}
    c.append(sombra(R(0, 0, 1200, 1200, "#C9CBC6"), "sCuerpo"))
    c.append(R(40, 40, 1120, 1120, "#D7D9D4") + R(40, 40, 1120, 14, "#E9EAE6"))
    for (x, y) in ((110, 110), (1090, 110), (110, 1090), (1090, 1090)):
        if flojo and x > 600 and y < 600:
            c.append(f'<circle cx="{x + 8}" cy="{y + 8}" r="46" fill="#00000055"/>')
            c.append(tornillo(x - 6, y - 6, 40, "cruz", 40))
        else:
            c.append(tornillo(x, y, 36, "cruz", 15))
        p[f"t{x}{y}"] = (x, y)
    c.append(R(380, 900, 440, 140, "#E9EAE6") + T(600, 945, "IP66", 64, "#1B1F24", 900) + T(600, 1005, "IEC 60529", 34, "#5B6067", 800))
    p["placa"] = (600, 970)
    p["flojo"] = (1084, 104)
    return pieza(Wp, Hp, 0.1, "".join(c), p)


def junta(flojo=False):
    """Corte del borde de la tapa: la lengüeta de la tapa entra en la ranura de la caja y aprieta el empaque de silicona.
    flojo=True: queda una rendija y el agua entra."""
    Wp, Hp = 1000, 700
    c, p = [], {}
    gap = 60 if flojo else 0
    # caja con ranura
    c.append(R(100, 360, 800, 340, "#BFC2BC") + R(380, 360, 240, 120, "#2A2D33"))
    c.append(R(400, 400 + (0 if flojo else 0), 200, 80, "#E25A3A" if False else "#F0B429"))   # empaque de silicona
    # tapa con lengüeta
    c.append(R(100, 160 - gap, 800, 200, "#CBCDC8") + R(430, 360 - gap, 140, 60 + (0 if flojo else 20), "#CBCDC8"))
    if not flojo:
        c.append(R(400, 420, 200, 60, "#F0B429"))
    if flojo:
        for k in range(4):
            c.append(f'<path d="M{60 + k * 30},{300 + k * 10} C{200},{330} {320},{330} {400},{350}" stroke="#4FA3E0" stroke-width="10" fill="none" opacity="0.85"/>')
        p["agua"] = (330, 330)
    p["empaque"] = (500, 440)
    p["tapa"] = (200, 260 - gap)
    p["caja"] = (200, 560)
    return pieza(Wp, Hp, 0.03, "".join(c), p)


def prensaestopas(cable=True, apretado=True):
    """Prensaestopas M20 × 1,5 de poliamida en corte: cuerpo hexagonal, rosca M20 (17 mm), contratuerca, junta tórica,
    inserto de sellado con laminillas y tuerca ciega; el cable (7–13 mm) pasa por el centro."""
    K = 30
    Wp, Hp = int(40 * K), int(60 * K)
    cx = Wp / 2
    c, p = [], {}
    g = "#8E959C"
    # pared del gabinete
    c.append(R(0, 30 * K, Wp, 3 * K, "#C9CBC6"))
    # rosca bajo la pared + contratuerca
    c.append(R(cx - 10 * K, 33 * K, 20 * K, 17 * K, g))
    for y in range(int(33 * K), int(50 * K), int(1.5 * K)):
        c.append(R(cx - 10 * K, y, 20 * K, 0.5 * K, "#6E757D"))
    c.append(R(cx - 14 * K, 35 * K, 28 * K, 5 * K, "#7D848B"))
    # junta tórica bajo el hexágono
    c.append(R(cx - 11 * K, 29 * K, 22 * K, 1.2 * K, "#1B1C1F"))
    # cuerpo hexagonal
    c.append(sombra(R(cx - 13.5 * K, 22 * K, 27 * K, 7 * K, g), "sTorn"))
    # inserto de sellado y laminillas
    ap = 0 if apretado else 1.2 * K
    c.append(R(cx - 8 * K - ap, 10 * K, 16 * K + 2 * ap, 12 * K, "#2A2D33"))
    for k in range(5):
        y = 10.5 * K + k * 2.2 * K
        c.append(f'<path d="M{cx - 8 * K - ap},{y} L{cx - 9.5 * K - ap},{y + 1.6 * K}" stroke="#7D848B" stroke-width="{0.5 * K}"/>'
                 f'<path d="M{cx + 8 * K + ap},{y} L{cx + 9.5 * K + ap},{y + 1.6 * K}" stroke="#7D848B" stroke-width="{0.5 * K}"/>')
    # tuerca ciega (domo)
    c.append(sombra(f'<path d="M{cx - 13 * K},{22 * K} V{12 * K} Q{cx - 13 * K},{6 * K} {cx - 6 * K},{5 * K} H{cx + 6 * K} Q{cx + 13 * K},{6 * K} {cx + 13 * K},{12 * K} V{22 * K} Z" fill="{g}" fill-opacity="0.55"/>', "sTorn"))
    if cable:
        dcab = 10 * K
        c.append(R(cx - dcab / 2, 0, dcab, Hp, "url(#gNegro)") + R(cx - dcab / 2 + 0.6 * K, 0, 1.2 * K, Hp, "#5B6067", 'opacity="0.6"'))
    p["inserto"] = (cx + 8 * K, 16 * K)
    p["tuerca"] = (cx + 12 * K, 9 * K)
    p["rosca"] = (cx + 10 * K, 44 * K)
    p["torica"] = (cx + 11 * K, 29.5 * K)
    p["cable"] = (cx, 55 * K)
    return pieza(Wp, Hp, 1 / K, "".join(c), p, margen=1)


def agujero():
    """Cable pasado por un agujero taladrado sin prensaestopas: queda una rendija alrededor."""
    K = 30
    Wp, Hp = int(40 * K), int(30 * K)
    cx = Wp / 2
    c = [R(0, 12 * K, Wp, 3 * K, "#C9CBC6"), R(cx - 8 * K, 12 * K, 16 * K, 3 * K, "#0B0B0C"),
         R(cx - 5 * K, 0, 10 * K, Hp, "url(#gNegro)")]
    for k in range(3):
        c.append(f'<path d="M{cx - 7.5 * K},{8 * K + k * K} C{cx - 7 * K},{12 * K} {cx - 6.5 * K},{14 * K} {cx - 6.5 * K},{20 * K}" stroke="#4FA3E0" stroke-width="10" fill="none"/>')
    return pieza(Wp, Hp, 1 / K, "".join(c), {"rendija": (cx - 6.5 * K, 13.5 * K)}, margen=1)


def boquilla(chorro=True, d=6.3):
    """Boquilla de ensayo (latón) con el chorro de agua."""
    Wp, Hp = 1600, 500
    c, p = [], {}
    c.append(R(0, 190, 400, 120, "#2A2D33"))
    c.append(sombra('<path d="M400,170 H620 L700,215 V285 L620,330 H400 Z" fill="url(#gLaton)"/>', "sTorn"))
    if chorro:
        w = 30 if d < 10 else 60
        c.append(f'<path d="M700,{250 - w / 2} L1600,{250 - w * 3} V{250 + w * 3} L700,{250 + w / 2} Z" fill="#4FA3E0" opacity="0.75"/>')
        for k in range(10):
            x = 800 + k * 80
            c.append(f'<circle cx="{x}" cy="{250 + (k % 3 - 1) * w}" r="{6 + k % 3 * 2}" fill="#BFE3FA"/>')
    p["boquilla"] = (700, 250)
    return pieza(Wp, Hp, 0.05, "".join(c), p)


def sondas():
    """Calibres de acceso de IEC 60529 a la misma escala: esfera Ø50 mm (1), dedo articulado Ø12 × 80 mm (2),
    varilla Ø2,5 mm (3) y alambre Ø1,0 mm (4), cada uno con su mango aislante."""
    K = 8
    Wp, Hp = 160 * K, 140 * K
    c, p = [], {}
    xs = (25, 65, 100, 135)
    for i, x in enumerate(xs):
        X = x * K
        c.append(R(X - 6 * K, 2 * K, 12 * K, 30 * K, "#C62828"))      # mango
        c.append(R(X - 1.5 * K, 32 * K, 3 * K, 20 * K, "url(#gAcero)"))
    # 1: esfera 50 mm
    c.append(sombra(f'<circle cx="{xs[0] * K}" cy="{77 * K}" r="{25 * K}" fill="url(#gAceroR)"/>', "sTorn"))
    # 2: dedo articulado Ø12 × 80
    X = xs[1] * K
    c.append(sombra(f'<path d="M{X - 6 * K},{52 * K} V{126 * K} A{6 * K},{6 * K} 0 0 0 {X + 6 * K},{126 * K} V{52 * K} Z" fill="url(#gAcero)"/>', "sTorn"))
    c.append(R(X - 6 * K, 80 * K, 12 * K, 1 * K, "#5E646B") + R(X - 6 * K, 105 * K, 12 * K, 1 * K, "#5E646B"))
    # 3: varilla 2,5 mm  · 4: alambre 1,0 mm
    c.append(R(xs[2] * K - 1.25 * K, 52 * K, 2.5 * K, 80 * K, "url(#gAcero)"))
    c.append(R(xs[3] * K - 0.5 * K, 52 * K, 1.0 * K, 80 * K, "url(#gAcero)"))
    for i, (x, t) in enumerate(zip(xs, ("Ø 50", "Ø 12", "Ø 2,5", "Ø 1,0"))):
        p[f"s{i + 1}"] = (x * K, 136 * K)
    return pieza(Wp, Hp, 1 / K, "".join(c), p, margen=1)


CATALOGO = {"sondas": sondas, "gab": lambda: gabinete(False), "gab_flojo": lambda: gabinete(True), "junta": lambda: junta(False),
            "junta_flojo": lambda: junta(True), "prensa": lambda: prensaestopas(True, True), "agujero": agujero,
            "boq5": lambda: boquilla(True, 6.3), "boq6": lambda: boquilla(True, 12.5)}
GRUPOS = {8: ["sondas"], 6: ["gab", "gab_flojo"], 20: ["junta", "junta_flojo"], 24: ["prensa", "agujero"], 10: ["boq5", "boq6"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

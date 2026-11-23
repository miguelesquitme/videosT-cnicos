"""V22 v2 · Toques al tocar metal: estática vs fuga. Piezas reales en mm.
Fuentes (ficha: referencias/v22_fuentes.md):
- worldstandards.eu (tipo B / NEMA 5-15): patas planas 6,3 × 1,5 mm, largo 15,9–18,3 mm, separadas 12,7 mm;
  pata de tierra Ø4,8 mm, 3,2 mm más larga, a 11,9 mm del punto medio entre las patas.
- Museo de clavijas (plugsocketmuseum.nl): en la 5-15P la pata de tierra es más larga que las de línea.
- Leviton 5266-C (ficha comercial): cuerpo de clavija Ø1,53 in (38,9 mm) × 1,98 in (50,3 mm).
- IEC 61000-4-2 (PDF ITU): modelo del cuerpo 150 pF + 330 Ω; 8 kV contacto: pico 30 A, subida 0,8 ns, 16 A a 30 ns, 8 A a 60 ns.
- ESDA "Fundamentals of ESD" parte 1: caminar sobre alfombra 35 000 V (10–25 % HR) / 1 500 V (65–90 % HR).
- InCompliance "Static electricity and people": pocos notan < 1 000 V; casi todos se quejan > 3 000 V.
- OSHA (efectos de la corriente): 1 mA se percibe; 6–16 mA no se puede soltar; NEC 2020 250.4(A)(5) camino efectivo de falla.
"""
import math
from svgv2 import pieza, sombra, T, R, logo, tornillo

S = 0.1   # 10 px = 1 mm


# ------------------------------------------------------------------ clavija NEMA 5-15P de lado
def clavija_lado(cable_mm=60):
    """Vista lateral perpendicular a las patas: se ve una pata plana (6,3 × 15,9 mm) y debajo, a 11,9 mm,
    la pata redonda de tierra Ø4,8 mm, 3,2 mm más larga. Cuerpo Ø38,9 × 50,3 mm con funda del cordón."""
    L = cable_mm * 10
    Wp, Hp = L + 503 + 230, 560
    c, p = [], {}
    y0 = 280                     # eje del cuerpo
    # cordón SJT negro y funda (alivio de tensión)
    c.append(R(0, y0 - 45, L, 90, "url(#gNegro)") + R(0, y0 - 40, L, 10, "#5A5E64", 'opacity="0.6"'))
    for k in range(6):
        c.append(R(L - 150 + k * 25, y0 - 62, 14, 124, "#1A1B1E"))
    c.append(sombra(f'<path d="M{L - 160},{y0 - 60} L{L},{y0 - 120} V{y0 + 120} L{L - 160},{y0 + 60} Z" fill="url(#gNegro)"/>'))
    # cuerpo (50,3 mm largo × 38,9 mm alto)
    xb = L
    c.append(sombra(R(xb, y0 - 195, 503, 390, "url(#gNegro)"), "sCuerpo"))
    c.append(R(xb + 20, y0 - 180, 463, 26, "#5B6067", 'opacity="0.55"'))
    for k in range(9):
        c.append(R(xb + 40 + k * 48, y0 - 195, 10, 390, "#000", 'opacity="0.25"'))
    c.append(R(xb + 470, y0 - 195, 33, 390, "#2C2F34"))
    c.append(logo(xb + 70, y0 + 60, 70))
    xf = xb + 503
    # pata plana (latón niquelado): 15,9 mm × 6,3 mm, con su agujero Ø3 mm
    c.append(sombra(R(xf, y0 - 31 - 60, 159, 63, "url(#gLatonV)"), "sTorn"))
    c.append(f'<circle cx="{xf + 115}" cy="{y0 - 60}" r="15" fill="#2A2D33"/>')
    p["pata_plana"] = (xf + 80, y0 - 60)
    # pata redonda de tierra: Ø4,8 mm, 19,1 mm de largo, 11,9 mm más abajo
    yt = y0 - 60 + 119
    c.append(sombra(f'<path d="M{xf},{yt - 24} H{xf + 167} A24,24 0 0 1 {xf + 167},{yt + 24} H{xf} Z" fill="url(#gLatonV)"/>', "sTorn"))
    c.append(R(xf, yt - 18, 191 - 24, 8, "#FFF1BE", 'opacity="0.55"'))
    p["pata_tierra"] = (xf + 100, yt)
    p["punta_tierra"] = (xf + 191, yt)
    p["punta_plana"] = (xf + 159, y0 - 60)
    p["cuerpo"] = (xb + 250, y0)
    return pieza(Wp, Hp, S, "".join(c), p)


def clavija_frente(tierra=True):
    """Cara de la clavija (vista de las puntas): 2 patas planas a 12,7 mm y la redonda a 11,9 mm (o arrancada)."""
    Wp = Hp = 440
    c, p = [], {}
    cx, cy = 220, 200
    c.append(sombra(f'<circle cx="{cx}" cy="{cy + 20}" r="195" fill="url(#gNegro)"/>', "sCuerpo"))
    c.append(f'<circle cx="{cx}" cy="{cy + 20}" r="170" fill="#26282C"/>')
    for dx, nom in ((-63.5, "fase"), (63.5, "neutro")):
        c.append(sombra(R(cx + dx - 7.5, cy - 31.5, 15, 63, "url(#gLaton)"), "sTorn"))
        p[nom] = (cx + dx, cy)
    if tierra:
        c.append(sombra(f'<circle cx="{cx}" cy="{cy + 119}" r="24" fill="url(#fLatonR)"/>', "sTorn"))
    else:
        c.append(f'<circle cx="{cx}" cy="{cy + 119}" r="24" fill="#3B3E43"/><circle cx="{cx}" cy="{cy + 119}" r="14" fill="#8A6A1E" opacity="0.7"/>')
    p["tierra"] = (cx, cy + 119)
    return pieza(Wp, Hp, S, "".join(c), p)


# ------------------------------------------------------------------ tomacorriente dúplex 5-15R con placa
def tomacorriente():
    """Placa estándar 70 × 114 mm (blanca) con tomacorriente dúplex NEMA 5-15R (cara ≈ 34 mm)."""
    Wp, Hp = 700, 1140
    c, p = [], {}
    c.append(sombra(R(0, 0, 700, 1140, "url(#gBlancoP)"), "sCuerpo"))
    c.append(R(8, 8, 684, 1124, "none", 'stroke="#C9CAC2" stroke-width="6"'))
    for k, yc in enumerate((330, 810)):
        c.append(sombra(f'<rect x="180" y="{yc - 190}" width="340" height="380" fill="url(#gBlancoP)"/>', "sTorn"))
        c.append(f'<path d="M180,{yc - 120} A170,170 0 0 1 520,{yc - 120} V{yc + 120} A170,170 0 0 1 180,{yc + 120} Z" fill="#F4F4EF" stroke="#D2D3CB" stroke-width="4"/>')
        c.append(R(272, yc - 80, 20, 72, "#1B1C1F"))           # ranura corta = fase (latón)
        c.append(R(408, yc - 88, 20, 88, "#1B1C1F"))           # ranura larga = neutro
        c.append(f'<path d="M326,{yc + 120} V{yc + 92} A24,24 0 0 1 374,{yc + 92} V{yc + 120} Z" fill="#1B1C1F"/>')   # tierra en U
        p[f"fase{k}"] = (282, yc - 44)
        p[f"neutro{k}"] = (418, yc - 44)
        p[f"tierra{k}"] = (350, yc + 100)
    c.append(tornillo(350, 570, 26, "ranura", 90))
    return pieza(Wp, Hp, S, "".join(c), p)


# ------------------------------------------------------------------ lavadora (gabinete de acero esmaltado)
def lavadora():
    """Lavadora de carga superior vista de frente (≈ 690 × 1080 mm): gabinete de acero esmaltado, consola con perillas
    y pantalla, tapa, patas niveladoras y el cordón que sale por atrás hacia la clavija."""
    Wp, Hp = 1000, 1200
    s = 0.69
    c, p = [], {}
    # consola trasera
    c.append(sombra(R(0, 0, 1000, 210, "url(#gEsmalte)"), "sCuerpo"))
    c.append(R(30, 40, 940, 130, "#E3E7EB"))
    for x in (130, 300, 700, 870):
        c.append(sombra(f'<circle cx="{x}" cy="105" r="48" fill="url(#gAceroR)"/>', "sTorn") + f'<rect x="{x - 4}" y="62" width="8" height="30" fill="#2A2E33"/>')
    c.append(R(410, 70, 180, 70, "#1B2430") + T(500, 105, "0:48", 46, "#7FE7FF", 800))
    c.append(logo(460, 150, 26))
    # gabinete
    c.append(sombra(R(0, 210, 1000, 900, "url(#gEsmalte)"), "sCuerpo"))
    c.append(R(0, 210, 1000, 70, "#DDE2E7"))               # tapa
    c.append(R(380, 236, 240, 22, "#B9C0C7"))               # manija de la tapa
    c.append(R(0, 278, 1000, 6, "#C3C9CF"))
    c.append(R(0, 1040, 1000, 70, "#D3D8DE") + R(60, 1060, 880, 10, "#B9C0C7"))
    for x in (70, 930):
        c.append(R(x - 30, 1110, 60, 60, "url(#gAcero)") + R(x - 40, 1160, 80, 20, "#2A2D33"))
    c.append('<path d="M120,320 V1000" stroke="#FFFFFF" stroke-width="22" opacity="0.6"/>')
    p["chasis"] = (760, 640)
    p["tapa"] = (500, 245)
    p["cordon"] = (980, 900)
    return pieza(Wp, Hp, s, "".join(c), p)


# ------------------------------------------------------------------ corte en la entrada del cordón (la falla)
def falla(tierra=False, chispa=False):
    """Corte en la entrada del cordón al chasis: lámina de acero, pasacables negro, cordón SJT con sus 3 conductores.
    El negro (fase) rozó con el borde de la lámina y se peló: el cobre toca el chasis. tierra=True: el verde
    está atornillado al chasis (camino de falla); False: no hay conductor de tierra."""
    Wp, Hp = 1200, 800
    c, p = [], {}
    # lámina del chasis (vista en corte) con su borde
    c.append(R(0, 0, 1200, 800, "#2A2D33"))
    c.append(sombra(R(500, 0, 100, 800, "url(#gEsmalte)")))
    c.append(R(500, 0, 22, 800, "url(#gAcero)") + R(578, 0, 22, 800, "url(#gAcero)"))
    c.append(T(550, 120, "CHASIS", 34, "#1B1F24", 900, rot=90) + T(550, 690, "CHASIS", 34, "#1B1F24", 900, rot=90))
    # pasacables (alivio de tensión)
    c.append(sombra(R(470, 300, 160, 200, "url(#gNegro)")))
    # cordón (afuera, a la izquierda)
    c.append(R(0, 330, 500, 140, "url(#gGris)") + R(0, 340, 500, 16, "#C7CCD2", 'opacity="0.5"'))
    # conductores adentro
    hil = [("#151515", 360, "fase"), ("#F4F4F2", 400, "neutro")] + ([("#2EA043", 440, "tierra")] if tierra else [])
    for col, y, nom in hil:
        c.append(f'<path d="M620,{y} C760,{y} 820,{y - 120 if nom == "fase" else y} 1200,{y - 120 if nom == "fase" else y}" stroke="{col}" stroke-width="30" fill="none"/>')
    # la fase pelada contra el borde de la lámina
    c.append(R(585, 345, 70, 30, "url(#gCobreH)"))
    for k in range(6):
        c.append(f'<line x1="{590 + k * 11}" y1="347" x2="{590 + k * 11}" y2="373" stroke="#8C4A1E" stroke-width="3"/>')
    p["falla"] = (585, 360)
    if tierra:
        c.append(f'<path d="M760,440 C820,460 860,560 760,620 L600,640" stroke="#2EA043" stroke-width="30" fill="none"/>')
        c.append('<path d="M760,440 C820,460 860,560 760,620 L600,640" stroke="#F2C200" stroke-width="8" stroke-dasharray="26 22" fill="none"/>')
        c.append(R(582, 620, 60, 40, "url(#gCobre)"))
        c.append(tornillo(612, 640, 26, "cruz", 15))
        c.append(f'<circle cx="612" cy="640" r="12" fill="#2EA043" opacity="0.7"/>')
        p["tierra"] = (612, 640)
    if chispa:
        c.append('<circle cx="600" cy="345" r="70" fill="#FFE066" opacity="0.35"/>'
                 '<path d="M600,345 l-60,-60 l26,-6 l-50,-70 l80,56 l-26,10 l60,60 Z" fill="#FFE066"/>')
    return pieza(Wp, Hp, 0.05, "".join(c), p)


# ------------------------------------------------------------------ manija de puerta + dedo (descarga estática)
def manija(chispa=False):
    """Manija de palanca de acero satinado con roseta Ø64 mm, y un dedo índice que se acerca.
    chispa=True: el arco de la descarga salta entre la yema y el metal."""
    Wp, Hp = 1500, 800
    c, p = [], {}
    c.append(R(0, 0, 1500, 800, "#C9B79C"))   # puerta de madera
    for y in range(0, 800, 46):
        c.append(f'<path d="M0,{y + 12} C400,{y + 4} 900,{y + 24} 1500,{y + 10}" stroke="#B19C7D" stroke-width="5" fill="none" opacity="0.7"/>')
    c.append(sombra('<circle cx="300" cy="400" r="160" fill="url(#gAceroR)"/>', "sCuerpo"))
    c.append('<circle cx="300" cy="400" r="120" fill="none" stroke="#E6EAEE" stroke-width="6" opacity="0.6"/>')
    c.append(sombra('<path d="M300,340 H860 C910,340 930,370 930,400 C930,430 910,460 860,460 H300 Z" fill="url(#gAceroV)"/>', "sCuerpo"))
    c.append('<path d="M320,352 H860" stroke="#FFFFFF" stroke-width="12" opacity="0.7"/>')
    p["manija"] = (930, 400)
    # dedo índice que llega desde la derecha
    x0 = 1010 if chispa else 1090
    dedo = (f'<path d="M1500,300 H{x0 + 120} C{x0 + 40},300 {x0},340 {x0},400 C{x0},460 {x0 + 40},500 {x0 + 120},500 H1500 Z" fill="url(#gPiel)"/>'
            f'<path d="M{x0 + 60},335 C{x0 + 20},350 {x0 + 15},380 {x0 + 25},395 L{x0 + 120},392 C{x0 + 130},360 {x0 + 110},335 {x0 + 60},335 Z" fill="#F1C9AE" opacity="0.9"/>'
            f'<path d="M{x0 + 290},320 C{x0 + 300},360 {x0 + 300},440 {x0 + 290},480" stroke="#B57B55" stroke-width="6" fill="none"/>'
            f'<path d="M{x0 + 320},320 C{x0 + 330},360 {x0 + 330},440 {x0 + 320},480" stroke="#B57B55" stroke-width="4" fill="none"/>')
    c.append(sombra(dedo, "sCuerpo"))
    p["yema"] = (x0, 400)
    if chispa:
        c.append(f'<path d="M930,400 L955,385 L962,410 L985,392 L990,414 L{x0},400" stroke="#E8F7FF" stroke-width="10" fill="none"/>'
                 f'<path d="M930,400 L955,385 L962,410 L985,392 L990,414 L{x0},400" stroke="#7FD3FF" stroke-width="22" fill="none" opacity="0.45"/>')
    return pieza(Wp, Hp, 0.06, "".join(c), p)


def _multimetro(lectura, unidad, pos):
    import svgref
    return svgref.multimetro(lectura, unidad, alto_mm=190.0, pos=pos)


CATALOGO = {
    "clavija_lado": lambda: clavija_lado(),
    "clavija_frente": lambda: clavija_frente(True),
    "clavija_sin_tierra": lambda: clavija_frente(False),
    "tomacorriente": lambda: tomacorriente(),
    "lavadora": lambda: lavadora(),
    "falla_sin": lambda: falla(False, False),
    "falla_chispa": lambda: falla(False, True),
    "falla_tierra": lambda: falla(True, False),
    "manija": lambda: manija(False),
    "manija_chispa": lambda: manija(True),
    "mm_120": lambda: _multimetro("120.4", "V~", 1),
    "mm_0": lambda: _multimetro("0.2", "V~", 1),
    "brk_on": lambda: __import__("svgref").disyuntor(n=1, In=15, curva="C", ref="F1", tension="120 VAC", on=True),
    "brk_off": lambda: __import__("svgref").disyuntor(n=1, In=15, curva="C", ref="F1", tension="120 VAC", on=False),
}
GRUPOS = {16: ["clavija_lado", "clavija_frente", "clavija_sin_tierra", "tomacorriente"], 2: ["lavadora"],
          12: ["falla_sin", "falla_chispa", "falla_tierra", "manija", "manija_chispa"], 6: ["mm_120", "mm_0"], 14: ["brk_on", "brk_off"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

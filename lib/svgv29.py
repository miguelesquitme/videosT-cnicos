"""V29 v2 · ¿Por qué BAJAN las luces cuando algo arranca? Piezas reales.
Fuentes (referencias/v29_fuentes.md): NEC 2020 Tabla 430.248 (½ hp 115 V = 9,8 A) y Tabla 430.251(A) (½ hp 115 V: rotor
bloqueado 58,8 A); NEC 2020 210.19(A) Nota informativa (3 % circuito, 5 % total); NEC Cap. 9 Tabla 8 (12 AWG trenzado 6,50 Ω/km);
IDC "Motor starting sags" (varias veces la corriente nominal al arrancar; caída fuerte y recuperación); Power Monitors Inc.
"Identifying loose neutrals" (una línea baja y la otra sube: 119/121 → 105/135 V; unas luces más brillantes y otras más tenues);
EC&M "The case of the defective neutral" (neutro de la acometida roto: luces que bajan, cable coaxial quemado)."""
from svgv2 import pieza, sombra, T, R, logo, tornillo


def foco(nivel=1.0):
    """Foco LED A19 (Ø60 × 110 mm): bulbo opalino, cuerpo disipador blanco, rosca E26 de aluminio con contacto.
    nivel: 0 apagado … 1 normal … 1.4 más brillante (sobretensión)."""
    Wp, Hp = 600, 1100
    c, p = [], {}
    if nivel > 0:
        op = min(0.85, 0.45 * nivel)
        pass
    bulbo = "#FFF6D8" if nivel > 0 else "#E6E8EA"
    if nivel > 1.1:
        bulbo = "#FFFFFF"
    c.append(sombra(f'<path d="M300,10 C470,10 590,140 590,300 C590,430 500,520 440,600 L440,660 H160 L160,600 C100,520 10,430 10,300 C10,140 130,10 300,10 Z" fill="{bulbo}"/>', "sCuerpo"))
    if nivel > 0:
        c.append(f'<ellipse cx="300" cy="300" rx="200" ry="180" fill="#FFFFFF" opacity="{min(0.9, 0.5 * nivel):.2f}"/>')
    c.append(R(160, 650, 280, 130, "url(#gBlancoP)"))
    for y in range(660, 780, 20):
        c.append(R(160, y, 280, 4, "#D5D6CF"))
    c.append(R(190, 780, 220, 230, "url(#gAlu)"))
    for k in range(5):
        y = 800 + k * 44
        c.append(f'<path d="M185,{y} L415,{y + 22}" stroke="#8D949B" stroke-width="12"/>')
    c.append(R(230, 1010, 140, 40, "#1B1C1F") + f'<path d="M260,1050 H340 L320,1090 H280 Z" fill="url(#gLaton)"/>')
    p["bulbo"] = (300, 300)
    return pieza(Wp, Hp, 0.1, "".join(c), p)


def tablero(neutro_flojo=False):
    """Centro de carga residencial 120/240 V sin tapa muerta: caja de acero, principal 2P arriba, dos barras de fase
    con lengüetas alternadas, 8 breakers de 1 polo, barra de neutro (cables blancos) y barra de tierra (desnudos/verdes).
    neutro_flojo=True: el neutro de la acometida con el tornillo flojo y el aislamiento recalentado."""
    Wp, Hp = 1000, 1700
    c, p = [], {}
    c.append(sombra(R(0, 0, 1000, 1700, "url(#gGris)"), "sCuerpo"))
    c.append(R(30, 30, 940, 1640, "#3B4148"))
    # acometida: 2 fases negras/rojas y neutro blanco entrando arriba
    for x, col in ((420, "#151515"), (580, "#151515"), (500, "#F4F4F2")):
        c.append(f'<path d="M{x},0 V{220 if x != 500 else 150}" stroke="{col}" stroke-width="34"/>')
    # principal 2P
    c.append(sombra(R(360, 200, 280, 230, "url(#gNegro)")))
    c.append(R(450, 280, 100, 80, "#2A2D33") + R(470, 250, 60, 70, "#111"))
    c.append(T(500, 400, "PRINCIPAL", 26, "#FFFFFF", 800))
    # barras de fase
    c.append(R(445, 430, 40, 1000, "url(#gCobreH)") + R(515, 430, 40, 1000, "url(#gCobreH)"))
    # breakers 1P a ambos lados
    for k in range(4):
        y = 500 + k * 220
        for lado, x in (("i", 210), ("d", 560)):
            c.append(sombra(R(x, y, 230, 190, "url(#gNegro)")))
            c.append(R(x + 80 if lado == "i" else x + 60, y + 60, 90, 70, "#111") + R(x + 95 if lado == "i" else x + 75, y + 40, 60, 60, "#2A2D33"))
            c.append(T(x + 115, y + 160, "20", 30, "#FFFFFF", 900))
    # barra de neutro (izquierda) y tierra (derecha)
    c.append(R(80, 480, 60, 900, "url(#gAcero)") + R(860, 480, 60, 900, "url(#gAcero)"))
    for k in range(12):
        y = 520 + k * 72
        c.append(tornillo(110, y, 18, "ranura", 0) + tornillo(890, y, 18, "ranura", 0))
        c.append(f'<path d="M130,{y} H200" stroke="#F4F4F2" stroke-width="12"/>')
        c.append(f'<path d="M870,{y} H800" stroke="#2EA043" stroke-width="10"/>')
    # neutro de la acometida a la barra
    c.append('<path d="M500,150 C500,300 110,300 110,470" stroke="#F4F4F2" stroke-width="30" fill="none"/>')
    c.append(R(80, 440, 60, 50, "url(#gAcero)"))
    if neutro_flojo:
        c.append('<path d="M180,300 C150,330 120,380 110,440" stroke="#8C5A2B" stroke-width="30" fill="none" opacity="0.85"/>')
        c.append('<circle cx="110" cy="460" r="34" fill="#FF6A00" opacity="0.45"/>')
        c.append(tornillo(110, 452, 22, "ranura", 35))
        c.append(R(98, 470, 26, 10, "#111"))
    else:
        c.append(tornillo(110, 462, 22, "ranura", 0))
    p["neutro"] = (110, 460)
    p["principal"] = (500, 300)
    p["barra_n"] = (110, 900)
    p["barra_t"] = (890, 900)
    p["fase_a"] = (465, 1000)
    return pieza(Wp, Hp, 0.4, "".join(c), p)


def compresor():
    """Compresor hermético de refrigeradora: domo de acero negro, tubos de cobre (succión, descarga, servicio),
    caja de terminales con el relé de arranque, base con amortiguadores."""
    Wp, Hp = 1000, 1020
    c, p = ['<g transform="translate(0,120)">'], {}
    c.append(R(80, 760, 840, 60, "#3A3F45"))
    for x in (180, 820):
        c.append(R(x - 50, 700, 100, 70, "#111") + f'<circle cx="{x}" cy="735" r="22" fill="#5E646B"/>')
    c.append(sombra('<path d="M150,720 V380 C150,170 330,90 500,90 C670,90 850,170 850,380 V720 Z" fill="url(#gNegro)"/>', "sCuerpo"))
    c.append('<path d="M230,330 C260,220 340,160 440,140" stroke="#5B6067" stroke-width="22" fill="none" opacity="0.7"/>')
    c.append(R(150, 520, 700, 16, "#2A2D33"))
    for x, h in ((300, 300), (380, 240), (460, 260)):
        c.append(f'<path d="M{x},140 V{140 - h * 0.4} C{x},{80 - h * 0.4} {x + 40},{70 - h * 0.4} {x + 80},{70 - h * 0.4}" stroke="url(#gCobreH)" stroke-width="26" fill="none"/>')
    c.append(sombra(R(620, 380, 220, 220, "#1B1C1F")))
    c.append(R(650, 410, 160, 90, "#E6E8EA") + T(730, 455, "RELÉ", 30, "#111", 900))
    c.append(f'<path d="M840,450 C930,450 950,520 990,520" stroke="#151515" stroke-width="20" fill="none"/>')
    c.append('</g>')
    p["domo"] = (500, 420)
    p["terminales"] = (730, 610)
    return pieza(Wp, Hp, 0.25, "".join(c), p)


def _mm(lectura):
    import svgref
    return svgref.multimetro(lectura, "V~", alto_mm=190.0, pos=1)


CATALOGO = {"foco_on": lambda: foco(1.0), "foco_bajo": lambda: foco(0.45), "foco_alto": lambda: foco(1.45),
            "tablero": lambda: tablero(False), "tablero_flojo": lambda: tablero(True), "compresor": compresor,
            "mm_120": lambda: _mm("120.1"), "mm_105": lambda: _mm("105.2"), "mm_135": lambda: _mm("135.0")}
GRUPOS = {10: ["foco_on", "foco_bajo", "foco_alto"], 3: ["tablero", "tablero_flojo"], 4: ["compresor"], 6: ["mm_120", "mm_105", "mm_135"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

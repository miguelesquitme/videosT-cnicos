"""V26 v2 · ¿Qué es el FACTOR DE POTENCIA? Capacitor de corrección real.
Fuentes (referencias/v26_fuentes.md): Eaton "Power factor correction: a guide for the plant engineer" (kW, kvar, kVA; FP = kW/kVA;
100 kW / 125 kVA = 0,80; meta ≈ 0,95; 0,75 → 0,95 baja la corriente ≈ 21 %; NEC: < 50 V en 1 min (≤ 600 V); caja inflada =
actuó el interruptor; no exceder los kvar máximos del fabricante del motor); TDK FilterCap MKP B3236 (bote de aluminio con
perno M12 abajo, polipropileno metalizado autorregenerable, resina de poliuretano, desconectador por sobrepresión, Ø63,5–85 mm,
H hasta 267 mm, ≥ 20 mm libres arriba); Schneider VarPlus Can (bote de aluminio, bornes a prueba de dedo, resistencias de
descarga montadas, desconectador sensible a la presión, hasta 50 kvar / 830 V); Fluke "Power factor formula" (kW, kVA, kvar;
recargos por bajo FP)."""
import math
from svgv2 import pieza, sombra, T, R, logo, tornillo

S = 0.1


def capacitor(inflado=False):
    """Capacitor trifásico de bote (Ø85 × 245 mm + bornes): aluminio, ranura de expansión, 3 bornes a prueba de dedo
    con las resistencias de descarga, perno M12 abajo, etiqueta. inflado=True: tapa abombada (actuó el desconectador)."""
    Wp, Hp = 1100, 3300
    c, p = [], {}
    x0, w = 125, 850
    ytop, ybot = 520, 3000
    # perno M12
    c.append(R(490, ybot, 120, 260, "url(#gAcero)"))
    for y in range(ybot + 20, ybot + 260, 26):
        c.append(R(490, y, 120, 6, "#5E646B"))
    # bote
    c.append(sombra(R(x0, ytop, w, ybot - ytop, "url(#gAcero)"), "sCuerpo"))
    c.append(R(x0, ytop + 120, w, 30, "#6E757D") + R(x0, ytop + 150, w, 8, "#E6EAEE"))     # ranura de expansión
    c.append(R(x0, ybot - 40, w, 40, "#5E646B"))
    # etiqueta
    c.append(R(x0 + 60, 1250, w - 120, 1150, "#1E3F7A"))
    c.append(T(550, 1340, "CAPACITOR DE POTENCIA", 52, "#FFFFFF", 900))
    c.append(T(550, 1430, "MKP · autorregenerable", 46, "#C9D7F2", 700))
    for k, (a, b) in enumerate((("3~", "60 Hz"), ("480 V", "25 kvar"), ("Δ", "con resistencias"), ("", "de descarga"))):
        c.append(T(360, 1560 + k * 110, a, 64, "#FFFFFF", 900) + T(700, 1560 + k * 110, b, 54, "#FFFFFF", 800))
    c.append(logo(470, 2060, 90))
    c.append(T(550, 2290, "IEC 60831-1", 44, "#C9D7F2", 700))
    p["bote"] = (x0 + w, 2000)
    p["etiqueta"] = (550, 1600)
    p["ranura"] = (x0 + w, ytop + 135)
    p["perno"] = (610, ybot + 150)
    # tapa (abombada si actuó)
    if inflado:
        c.append(sombra(f'<path d="M{x0},{ytop} Q550,{ytop - 330} {x0 + w},{ytop} Z" fill="url(#gAceroV)"/>', "sTorn"))
        ytb = ytop - 160
    else:
        c.append(sombra(R(x0, ytop - 60, w, 60, "url(#gAceroV)"), "sTorn"))
        ytb = ytop - 60
    # bloque de bornes (plástico negro, a prueba de dedo) y resistencias de descarga
    c.append(sombra(R(260, ytb - 300, 580, 300, "url(#gNegro)")))
    xs = (360, 550, 740)
    for k, x in enumerate(xs):
        c.append(R(x - 60, ytb - 420, 120, 140, "#1B1C1F"))
        c.append(tornillo(x, ytb - 350, 40, "cruz", 15))
        c.append(T(x, ytb - 230, ("L1", "L2", "L3")[k], 44, "#FFFFFF", 900))
        p[f"borne{k}"] = (x, ytb - 350)
    for x1, x2 in ((360, 550), (550, 740)):
        xm = (x1 + x2) / 2
        c.append(f'<path d="M{x1 + 40},{ytb - 120} H{xm - 50}" stroke="#C9CED3" stroke-width="8"/>'
                 f'<path d="M{xm + 50},{ytb - 120} H{x2 - 40}" stroke="#C9CED3" stroke-width="8"/>')
        c.append(sombra(R(xm - 55, ytb - 145, 110, 50, "#3B7DD8"), "sTorn"))
        for j, col in enumerate(("#7A3E16", "#111", "#C9A227")):
            c.append(R(xm - 35 + j * 22, ytb - 145, 10, 50, col))
    p["resistencia"] = ((360 + 550) / 2, ytb - 120)
    p["tapa"] = (550, ytb + 20)
    return pieza(Wp, Hp, S, "".join(c), p)


def capacitor_corte():
    """Corte del capacitor: 3 bobinas de película de polipropileno metalizado (vistas en espiral), resina de poliuretano,
    conexiones con el hilo del desconectador por sobrepresión bajo la tapa."""
    Wp, Hp = 1100, 2800
    c, p = [], {}
    x0, w = 125, 850
    c.append(sombra(R(x0, 300, w, 2400, "url(#gAcero)"), "sCuerpo"))
    c.append(R(x0 + 30, 330, w - 60, 2340, "#C9B98A"))          # resina
    for k in range(3):
        yc = 760 + k * 700
        c.append(f'<ellipse cx="550" cy="{yc}" rx="330" ry="300" fill="#8E959C"/>')
        for r in range(40, 330, 14):
            c.append(f'<ellipse cx="550" cy="{yc}" rx="{r}" ry="{r * 300 / 330:.0f}" fill="none" stroke="{"#D9DEE3" if (r // 14) % 2 else "#B7C2CC"}" stroke-width="7"/>')
        c.append(f'<circle cx="550" cy="{yc}" r="30" fill="#5E646B"/>')
        p[f"bobina{k}"] = (880, yc)
    # hilos al desconectador
    c.append('<path d="M450,460 V300 M550,460 V300 M650,460 V300" stroke="url(#gCobreH)" stroke-width="16"/>')
    c.append('<path d="M420,300 H680" stroke="#C9CED3" stroke-width="10" stroke-dasharray="30 14"/>')
    p["desconectador"] = (680, 300)
    c.append(sombra(R(x0, 220, w, 80, "url(#gAceroV)"), "sTorn"))
    p["resina"] = (x0 + 60, 1110)
    return pieza(Wp, Hp, S, "".join(c), p)


def _motor():
    import svgref
    return svgref.motor(ref="M1", ancho_mm=300.0, placa="nidec")


CATALOGO = {"cap": lambda: capacitor(False), "cap_inflado": lambda: capacitor(True), "cap_corte": capacitor_corte, "motor": _motor}
GRUPOS = {8: ["cap", "cap_inflado", "cap_corte"], 4: ["motor"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

"""V23 v2 · ¿Por qué el motor gira al revés? Piezas reales.
Fuentes (referencias/v23_fuentes.md): Siemens "Motor rotation direction" (IEC 60034-8: sentido visto desde el lado del eje;
U1-V1-W1 a L1-L2-L3 → horario; cambiar dos fases invierte); WEG manual de instalación (invertir dos fases; probar sin carga
antes de acoplar; ventiladores unidireccionales); Fluke 9040 manual (indicador de rotación de fases 40–690 V, 124 × 61 × 27 mm,
3 puntas); Fluke "Don't run it backwards" (compresores de tornillo destruidos en segundos: sin bombeo de aceite);
Britannica (láminas de acero al silicio ≈ 0,5 mm; jaula de aluminio fundido con barras y anillos; velocidad cae 1–5 %);
SEW (sentido horario mirando al extremo del eje). Placa Nidec U10P2D: 1760 rpm."""
import math
from svgv2 import pieza, sombra, T, R, tornillo

# IEC 60445: L1 café, L2 negro, L3 gris
FASES = {"L1": "#8B5A2B", "L2": "#1A1A1A", "L3": "#8E959C"}


def estator(rot_ang=0.0, ns=36, nr=28, partes="todo"):
    """Corte transversal real: carcasa con aletas, paquete de láminas con 36 ranuras, bobinado trifásico de cobre
    (cada fase ocupa grupos de ranuras repartidos; colores de las fases por IEC 60445), entrehierro, rotor de jaula
    con 28 barras de aluminio, eje con chaveta."""
    Wp = Hp = 1000
    cx = cy = 500
    c, p = [], {}
    if partes == "rotor":
        c.append(f'<rect x="0" y="0" width="{Wp}" height="{Hp}" fill="none"/>')
    # carcasa con aletas (TEFC)
    for k in range(40):
        a = k * 2 * math.pi / 40
        x1, y1 = cx + 440 * math.cos(a), cy + 440 * math.sin(a)
        x2, y2 = cx + 492 * math.cos(a), cy + 492 * math.sin(a)
        c.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#3E5A74" stroke-width="16"/>')
    c.append(sombra(f'<circle cx="{cx}" cy="{cy}" r="445" fill="#3E5A74"/>', "sCuerpo"))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="420" fill="#2E465C"/>')
    # paquete de láminas del estator
    c.append(f'<circle cx="{cx}" cy="{cy}" r="410" fill="url(#gAceroR)"/>')
    for r in range(220, 410, 14):
        c.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#6E757D" stroke-width="1.2" opacity="0.5"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="215" fill="#14161A"/>')
    # ranuras con su bobinado: grupos de 3 ranuras por fase (A, -C, B, -A, C, -B) → secuencia espacial L1 L2 L3
    orden = ["L1", "L3", "L2"] * 2
    for k in range(ns):
        a = k * 2 * math.pi / ns - math.pi / 2
        fase = orden[(k // 3) % 6]
        col = FASES[fase]
        g = (f'<g transform="rotate({math.degrees(a) + 90:.2f} {cx} {cy})">'
             f'<path d="M{cx - 9},{cy - 222} L{cx - 13},{cy - 300} A13,13 0 0 1 {cx + 13},{cy - 300} L{cx + 9},{cy - 222} Z" fill="#101214"/>'
             f'<path d="M{cx - 7},{cy - 232} L{cx - 10},{cy - 298} A10,10 0 0 1 {cx + 10},{cy - 298} L{cx + 7},{cy - 232} Z" fill="url(#gCobre)"/>'
             f'<path d="M{cx - 8},{cy - 230} L{cx - 9},{cy - 262} H{cx + 9} L{cx + 8},{cy - 230} Z" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/></g>')
        c.append(g)
        if k % 3 == 1:
            p[f"r_{k}"] = (cx + 262 * math.cos(a), cy + 262 * math.sin(a))
    if partes == "rotor":
        c = [f'<rect x="0" y="0" width="{Wp}" height="{Hp}" fill="#000" opacity="0"/>']
    # rotor de jaula (aluminio) que puede girar
    rot = [f'<circle cx="{cx}" cy="{cy}" r="205" fill="url(#gAceroR)"/>']
    for k in range(nr):
        a = k * 2 * math.pi / nr
        rot.append(f'<g transform="rotate({math.degrees(a):.2f} {cx} {cy})"><ellipse cx="{cx}" cy="{cy - 180}" rx="11" ry="20" fill="url(#gAluR)"/></g>')
    rot.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="url(#gAcero)"/><rect x="{cx - 12}" y="{cy - 60}" width="24" height="22" fill="#3A3F45"/>')
    rot.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="#2A2E33" stroke-width="4"/>')
    if partes != "estator":
        c.append(sombra(f'<g transform="rotate({rot_ang} {cx} {cy})">{"".join(rot)}</g>', "sTorn"))
    p["centro"] = (cx, cy)
    p["laminas"] = (cx + 360 * math.cos(0.6), cy + 360 * math.sin(0.6))
    p["barra"] = (cx, cy - 180)
    p["eje"] = (cx, cy)
    p["carcasa"] = (cx - 470, cy)
    return pieza(Wp, Hp, 0.25, "".join(c), p)


def indicador(sentido="horario"):
    """Indicador de rotación de fases genérico (124 × 61 × 27 mm, 40–690 V~): caja amarilla con funda, 2 LED de giro
    (horario / antihorario), LED por fase L1 L2 L3 y 3 puntas negras rotuladas."""
    Wp, Hp = 1240, 1700
    c, p = [], {}
    c.append(sombra(R(0, 0, 610, 1240, "#E8B400"), "sCuerpo"))
    c.append(R(40, 40, 530, 1160, "#2A2D33"))
    c.append(T(305, 110, "INDICADOR DE ROTACIÓN DE FASES", 26, "#FFFFFF", 800))
    c.append(T(305, 150, "40 – 690 V~  ·  CAT III", 22, "#C9CED3", 700))
    from svgref import logo
    c.append(logo(80, 180, 40))
    for k, f in enumerate(("L1", "L2", "L3")):
        x = 160 + k * 145
        on = True
        c.append(f'<circle cx="{x}" cy="330" r="30" fill="{"#39FF88" if on else "#2E4A3A"}"/>' + T(x, 390, f, 30, "#FFFFFF", 900))
    # flechas de giro
    for k, (lab, cxx) in enumerate((("HORARIO", 175), ("ANTIHORARIO", 435))):
        on = (sentido == "horario") == (k == 0)
        col = "#39FF88" if on and k == 0 else ("#FF4D6D" if on else "#3A3F45")
        sw = 1 if k == 0 else -1
        c.append(f'<path d="M{cxx - 70},560 A90,90 0 1 {1 if sw > 0 else 0} {cxx + 70},560" stroke="{col}" stroke-width="22" fill="none"/>')
        tip = (cxx + 70, 560) if sw > 0 else (cxx - 70, 560)
        c.append(f'<polygon points="{tip[0] - 26},{560 - 6} {tip[0] + 26},{560 - 6} {tip[0]},{600}" fill="{col}"/>')
        c.append(f'<circle cx="{cxx}" cy="700" r="28" fill="{col}"/>' + T(cxx, 760, lab, 24, "#FFFFFF", 800))
        p["led_" + ("h" if k == 0 else "a")] = (cxx, 700)
    c.append(R(80, 860, 450, 280, "#1B1D21"))
    # cables y puntas
    for k, f in enumerate(("L1", "L2", "L3")):
        x = 160 + k * 145
        c.append(f'<path d="M{x},1240 C{x},1400 {700 + k * 160},1300 {760 + k * 160},1500" stroke="#151515" stroke-width="26" fill="none"/>')
        c.append(R(735 + k * 160, 1490, 50, 150, "#151515") + R(752 + k * 160, 1640, 16, 60, "url(#gAcero)"))
        c.append(R(730 + k * 160, 1520, 60, 40, "#FFFFFF") + T(760 + k * 160, 1540, f, 24, "#111", 900))
        p["p" + f] = (760 + k * 160, 1690)
    return pieza(Wp, Hp, 0.1, "".join(c), p)


def _motor():
    import svgref
    return svgref.motor(ref="M1", ancho_mm=300.0, placa="nidec")


def _caja():
    import svgref
    return svgref.caja_bornes("6", "delta", ancho_mm=110.0)


CATALOGO = {"estator": lambda: estator(0), "estator_solo": lambda: estator(0, partes="estator"), "rotor": lambda: estator(0, partes="rotor"), "motor": _motor, "caja": _caja,
            "ind_h": lambda: indicador("horario"), "ind_a": lambda: indicador("antihorario")}
GRUPOS = {8: ["estator", "estator_solo", "rotor"], 4: ["motor"], 14: ["caja"], 10: ["ind_h", "ind_a"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

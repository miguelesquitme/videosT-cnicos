"""V28 v2 · ¿Qué pasa si conectas 120 V a 240 V? Piezas reales.
Fuentes (referencias/v28_fuentes.md): Tempco "All about tubular heating elements" (bobina helicoidal 80 % Ni 20 % Cr, MgO grado A
compactado, pin frío de acero niquelado soldado por fusión); Watlow WATROD (Ni-Cr bobinado, MgO compactado, vainas de acero,
304/316, aleación 800; Ø 6,6 / 8,0 / 10,9 mm); Leviton 5661 (NEMA 6-15R 15 A 250 V); Plug & socket museum (5-20R / 6-20R);
worldstandards.eu (NEMA 5-15: patas 6,3 × 1,5 mm a 12,7 mm, tierra Ø4,8); Apple manual adaptador USB-C (entrada 100–240 V~,
50–60 Hz)."""
from svgv2 import pieza, sombra, T, R, logo, tornillo

K = 60   # px por mm


def resistencia(estado="frio"):
    """Corte de una resistencia tubular Ø8,0 mm: vaina de acero, MgO compactado (blanco), espiral de Ni-Cr centrada,
    pin frío soldado. estado: frio · 120 (rojo opaco) · 240 (amarillo-blanco y la espiral fundida)."""
    L = 38.0
    W, H = int(L * K), int(14 * K)
    y0 = H / 2
    r = 4.0 * K
    c, p = [], {}
    col = {"frio": "#7D848B", "120": "#E0522C", "240": "#FFF3B0"}[estado]
    glow = {"frio": 0, "120": 0.35, "240": 0.75}[estado]
    # pin frío y sello
    c.append(R(0, y0 - 0.9 * K, 10 * K, 1.8 * K, "url(#gAceroV)"))
    c.append(R(8 * K, y0 - r - 0.2 * K, 2 * K, 2 * r + 0.4 * K, "#2A2D33"))
    # vaina cortada: pared superior e inferior
    c.append(sombra(R(10 * K, y0 - r, W - 10 * K, 0.6 * K, "url(#gAceroV)"), "sTorn"))
    c.append(sombra(R(10 * K, y0 + r - 0.6 * K, W - 10 * K, 0.6 * K, "url(#gAceroV)"), "sTorn"))
    c.append(R(10 * K, y0 - r + 0.6 * K, W - 10 * K, 2 * r - 1.2 * K, {"frio": "#EFEDE6", "120": "#F3D9C8", "240": "#FFF4C9"}[estado]))
    for i in range(0, int((W - 10 * K) / 18)):
        x = 10 * K + i * 18 + (i * 7) % 11
        c.append(f'<circle cx="{x}" cy="{y0 - r + 0.9 * K + (i * 37) % int(2 * r - 1.8 * K)}" r="3" fill="#D3D0C6"/>')
    # pin dentro hasta la soldadura
    c.append(R(10 * K, y0 - 0.9 * K, 6 * K, 1.8 * K, "url(#gAceroV)"))
    p["pin"] = (5 * K, y0)
    # espiral de Ni-Cr
    paso = 0.9 * K
    x = 16 * K
    k = 0
    while x < W - 1.5 * K:
        roto = estado == "240" and 26 * K < x < 29 * K
        if not roto:
            c.append(f'<ellipse cx="{x}" cy="{y0}" rx="{paso * 0.35}" ry="{1.6 * K}" fill="none" stroke="{col}" stroke-width="{0.35 * K}"/>')
        x += paso
        k += 1
    if estado == "240":
        c.append(f'<circle cx="{27.5 * K}" cy="{y0}" r="{0.9 * K}" fill="#FFFFFF" opacity="0.9"/>')
        p["falla"] = (27.5 * K, y0)
    p["espiral"] = (22 * K, y0 - 1.6 * K)
    p["mgo"] = (31 * K, y0 + 2.6 * K)
    p["vaina"] = (34 * K, y0 - r)
    p["diam"] = (W - 0.5 * K, y0)
    return pieza(W, H, 1 / K, "".join(c), p, margen=1)


def etiqueta(texto=("120 V~ 60 Hz", "1000 W"), titulo="DATOS", ancho_mm=60.0):
    """Placa/etiqueta plateada de datos del aparato (impresión negra)."""
    Wp, Hp = 600, 300
    c = [sombra(R(0, 0, Wp, Hp, "url(#gAlu)"), "sTorn"), R(16, 16, Wp - 32, 50, "#1B1F24"), T(Wp / 2, 41, titulo, 30, "#FFFFFF", 900)]
    for i, t in enumerate(texto):
        c.append(T(Wp / 2, 120 + i * 80, t, 56 if i == 0 else 50, "#111", 900))
    c.append(logo(Wp - 90, Hp - 70, 40))
    return pieza(Wp, Hp, ancho_mm / Wp, "".join(c), {"centro": (Wp / 2, Hp / 2)})


def tomacorriente(tipo="5-15"):
    """Tomacorriente sencillo con placa (70 × 114 mm): 5-15R (ranuras verticales, 125 V) o 6-15R (horizontales, 250 V)."""
    Wp, Hp = 700, 1140
    c, p = [], {}
    c.append(sombra(R(0, 0, 700, 1140, "url(#gBlancoP)"), "sCuerpo"))
    c.append(R(8, 8, 684, 1124, "none", 'stroke="#C9CAC2" stroke-width="6"'))
    yc = 570
    c.append(sombra(f'<circle cx="350" cy="{yc}" r="200" fill="url(#gBlancoP)"/>', "sTorn"))
    c.append(f'<circle cx="350" cy="{yc}" r="200" fill="none" stroke="#D2D3CB" stroke-width="4"/>')
    if tipo == "5-15":
        c.append(R(272, yc - 100, 20, 72, "#1B1C1F") + R(408, yc - 108, 20, 88, "#1B1C1F"))
    else:
        c.append(R(228, yc - 74, 72, 20, "#1B1C1F") + R(400, yc - 74, 72, 20, "#1B1C1F"))
    c.append(f'<path d="M326,{yc + 110} V{yc + 82} A24,24 0 0 1 374,{yc + 82} V{yc + 110} Z" fill="#1B1C1F"/>')
    c.append(T(350, 850, "125 V · 15 A" if tipo == "5-15" else "250 V · 15 A", 46, "#6E757D", 800))
    c.append(T(350, 905, "NEMA " + tipo + "R", 40, "#9AA1A8", 800))
    c.append(tornillo(350, 180, 22, "ranura", 90) + tornillo(350, 960 + 60, 22, "ranura", 90))
    p["ranuras"] = (350, yc - 60)
    return pieza(Wp, Hp, 0.1, "".join(c), p)


def cargador():
    """Cargador USB-C genérico (cubo blanco) con la impresión de entrada 100–240 V~ 50/60 Hz."""
    Wp, Hp = 600, 760
    c = [R(150, 0, 60, 180, "url(#gAceroV)"), R(390, 0, 60, 180, "url(#gAceroV)")]
    c.append(sombra(R(40, 160, 520, 600, "url(#gBlancoP)"), "sCuerpo"))
    c.append(T(300, 330, "INPUT", 44, "#6E757D", 800))
    c.append(T(300, 410, "100–240 V~", 70, "#1B1F24", 900))
    c.append(T(300, 480, "50/60 Hz", 50, "#1B1F24", 800))
    c.append(R(250, 640, 100, 40, "#2A2D33"))
    return pieza(Wp, Hp, 0.08, "".join(c), {"texto": (300, 410)})


CATALOGO = {"res_frio": lambda: resistencia("frio"), "res_120": lambda: resistencia("120"), "res_240": lambda: resistencia("240"),
            "etq": lambda: etiqueta(), "t515": lambda: tomacorriente("5-15"), "t615": lambda: tomacorriente("6-15"), "cargador": cargador}
GRUPOS = {14: ["res_frio", "res_120", "res_240"], 12: ["etq", "t515", "t615", "cargador"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

"""V25 v2 · ¿Cómo funciona un FUSIBLE? Piezas reales (cilíndrico 10 × 38 gG).
Fuentes (referencias/v25_fuentes.md): Ferraz Shawmut/Mersen gG cilíndricos (cuerpo cerámico, casquillos plateados, arena;
10 × 38: Ø10,3 × 38 mm, casquillo 10,5 mm); Mersen 10×38 gG 400–690 V (0,5–32 A, cerámica, contactos plateados);
Eaton Bussmann "Fuseology" (cuello restringido se funde primero; con falla se funden varias secciones; relleno granular
que absorbe el arco y forma fulgurita; corta en < ¼ de ciclo; el fusible no debe exceder la capacidad del conductor);
AutomationDirect "Fuse terms" (I²t; limitador < ½ ciclo); Electrokit (gG rango completo; aM solo cortocircuito, motores)."""
from svgv2 import pieza, sombra, T, R, logo

K = 40   # px por mm (10 × 38 mm → 412 × 1520 px)
L, D, CAP = 38.0, 10.3, 10.5


def _cuerpo(c, corte):
    w, h = D * K, L * K
    cap = CAP * K
    x0 = 0
    if not corte:
        c.append(sombra(R(x0 + 18, cap - 20, w - 36, h - 2 * cap + 40, "url(#gCeram)"), "sCuerpo"))
    else:
        c.append(R(x0 + 18, cap - 20, w - 36, h - 2 * cap + 40, "#D7CFBE"))
        c.append(R(x0 + 46, cap - 20, w - 92, h - 2 * cap + 40, "url(#pArena)"))
        c.append(R(x0 + 18, cap - 20, 28, h - 2 * cap + 40, "url(#gCeram)") + R(x0 + w - 46, cap - 20, 28, h - 2 * cap + 40, "url(#gCeram)"))
    for y in (0, h - cap):
        c.append(sombra(R(x0, y, w, cap, "url(#gAcero)"), "sTorn"))
        c.append(R(x0, y + (cap - 30 if y == 0 else 0), w, 30, "#8D949B"))
        c.append(R(x0 + 40, y + 20, 30, cap - 40, "#FFFFFF", 'opacity="0.45"'))
    return w, h, cap


def fusible(texto=True):
    c, p = [], {}
    w, h, cap = _cuerpo(c, False)
    if texto:
        ym = h / 2
        c.append(T(w / 2, ym + 265, "gG", 90, "#1B1F24", 900, rot=-90))
        c.append(T(w / 2, ym + 50, "16 A", 95, "#C62828", 900, rot=-90))
        c.append(T(w / 2, ym - 215, "500 V~", 62, "#1B1F24", 800, rot=-90))
    p["cuerpo"] = (w / 2, h / 2)
    p["casq_sup"] = (w, cap / 2)
    p["casq_inf"] = (w, h - cap / 2)
    p["texto"] = (w / 2, h / 2)
    return pieza(w, h, 1 / K, "".join(c), p, margen=2)


def fusible_corte(estado="normal"):
    """Corte longitudinal: lámina con 4 cuellos (perforaciones), soldada a los casquillos, rodeada de arena.
    estado: normal · caliente (cuellos rojos) · sobrecarga (un cuello abierto) · corto (varios cuellos vaporizados,
    arcos y fulgurita)."""
    c, p = [], {}
    w, h, cap = _cuerpo(c, True)
    xm = w / 2
    ys = [cap + (h - 2 * cap) * f for f in (0.2, 0.4, 0.6, 0.8)]
    lam = "#D9DEE3"
    c.append(R(xm - 60, cap - 60, 120, h - 2 * cap + 120, lam))
    c.append(R(xm - 60, cap - 60, 20, h - 2 * cap + 120, "#FFFFFF", 'opacity="0.6"'))
    for i, y in enumerate(ys):
        abierto = (estado == "sobrecarga" and i == 2) or (estado == "corto")
        if abierto:
            gap = 40 if estado == "sobrecarga" else 90
            c.append(R(xm - 62, y - gap / 2, 124, gap, "url(#pArena)"))
            if estado == "corto":
                c.append(f'<ellipse cx="{xm}" cy="{y}" rx="110" ry="{gap * 0.9}" fill="#6E6152" opacity="0.85"/>'
                         f'<ellipse cx="{xm}" cy="{y}" rx="70" ry="{gap * 0.55}" fill="#3D342B"/>')
            else:
                c.append(f'<path d="M{xm - 60},{y - 20} q20,10 0,20 M{xm + 60},{y + 20} q-20,-10 0,-20" stroke="#8D949B" stroke-width="10" fill="none"/>')
        else:
            col = "#FF5A1F" if estado == "caliente" else "#2A2D33"
            c.append(f'<circle cx="{xm - 34}" cy="{y}" r="22" fill="{col}"/><circle cx="{xm + 34}" cy="{y}" r="22" fill="{col}"/>')
            if estado == "caliente":
                c.append(f'<rect x="{xm - 12}" y="{y - 22}" width="24" height="44" fill="#FFB020"/>')
        p[f"cuello{i}"] = (xm, y)
    if estado == "corto":
        for y in ys:
            c.append(f'<circle cx="{xm}" cy="{y}" r="140" fill="#FFE066" opacity="0.0"/>')
    p["lamina"] = (xm + 60, (ys[0] + ys[1]) / 2)
    p["arena"] = (w - 70, (ys[2] + ys[3]) / 2)
    p["soldadura"] = (xm, cap - 30)
    return pieza(w, h, 1 / K, "".join(c), p, margen=2)


def arcos():
    """Capa con los arcos del cortocircuito sobre los cuellos (para superponer al corte)."""
    w, h = D * K, L * K
    cap = CAP * K
    ys = [cap + (h - 2 * cap) * f for f in (0.2, 0.4, 0.6, 0.8)]
    c = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="none"/>']
    for y in ys:
        c.append(f'<ellipse cx="{w / 2}" cy="{y}" rx="120" ry="70" fill="#7FD3FF" opacity="0.45"/>'
                 f'<path d="M{w / 2},{y - 45} l-20,25 l26,6 l-24,30" stroke="#FFFFFF" stroke-width="10" fill="none"/>')
    return pieza(w, h, 1 / K, "".join(c), {}, margen=2)


def puenteado():
    """Fusible 'puenteado': un alambre de cobre enrollado de casquillo a casquillo (práctica prohibida)."""
    c, p = [], {}
    w, h, cap = _cuerpo(c, False)
    c.append(T(w / 2, h / 2 - 20, "16 A", 110, "#C62828", 900, rot=-90))
    for y0 in (cap * 0.5, h - cap * 0.5):
        for k in range(3):
            c.append(f'<ellipse cx="{w / 2}" cy="{y0 - 60 + k * 50}" rx="{w / 2 + 14}" ry="18" fill="none" stroke="url(#gCobre)" stroke-width="16"/>')
    c.append(f'<path d="M{w + 10},{cap * 0.5} C{w + 160},{h * 0.3} {w + 160},{h * 0.7} {w + 10},{h - cap * 0.5}" stroke="url(#gCobreH)" stroke-width="16" fill="none"/>')
    p["alambre"] = (w + 130, h / 2)
    return pieza(w + 200, h, 1 / K, "".join(c), p, margen=2)


CATALOGO = {"fusible": fusible, "corte": lambda: fusible_corte("normal"), "corte_cal": lambda: fusible_corte("caliente"),
            "corte_sob": lambda: fusible_corte("sobrecarga"), "corte_cc": lambda: fusible_corte("corto"), "arcos": arcos,
            "puenteado": puenteado}
GRUPOS = {30: list(CATALOGO)}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

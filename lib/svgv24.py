"""V24 v2 · ¿Por qué suenan los cables de alta tensión? Efecto corona. Piezas reales.
Fuentes (referencias/v24_fuentes.md): Nassau National Cable / Southwire (ACSR 795 kcmil Drake 26/7: Al 0,1749 in, acero
0,1360 in, núcleo 0,408 in, total 1,108 in = 28,14 mm); MacLean Power MG523Z (aislador ANSI 52-3, vidrio templado,
Ø255 mm, paso 146 mm, fuga 321 mm, bola y casquillo, flameo en seco 80 kV / húmedo 50 kV); EEPower "Understanding corona
discharge" (≈30 kV/cm en aire seco; lluvia/neblina lo empeoran; ruido 1–20 kHz; ozono; pérdidas < 1 %; haces y anillos
anticorona; brillo azulado); Wikipedia "Peek's law" (factor de irregularidad: cables 0,87–0,83)."""
import math
from svgv2 import pieza, sombra, T, R


def acsr(ancho_mm=28.14):
    """Corte del ACSR Drake 26/7 a escala: 7 hilos de acero galvanizado (1 + 6) Ø3,45 mm, 10 + 16 hilos de aluminio
    Ø4,44 mm (Ø total 28,14 mm)."""
    k = 30          # px por mm
    W = H = int(29.5 * k)
    cx = cy = W / 2
    c, p = [], {}
    ra, rs = 4.443 / 2 * k, 3.454 / 2 * k
    def hilo(x, y, r, grad, borde):
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 1:.1f}" fill="url(#{grad})" stroke="{borde}" stroke-width="2"/>'
    capas = [(16, (3.454 * 1.5 + 4.443 * 1.5) * k, "gAluR", "#7F868D", ra), (10, (3.454 * 1.5 + 4.443 * 0.5) * k, "gAluR", "#7F868D", ra),
             (6, 3.454 * k, "gAceroR", "#3E444B", rs)]
    c.append(f'<circle cx="{cx}" cy="{cy}" r="{14.07 * k}" fill="#1E2126"/>')
    for n, rc, g, b, r in capas:
        for i in range(n):
            a = 2 * math.pi * i / n + (0.1 if n == 16 else 0)
            c.append(hilo(cx + rc * math.cos(a), cy + rc * math.sin(a), r, g, b))
    c.append(hilo(cx, cy, rs, "gAceroR", "#3E444B"))
    p["acero"] = (cx, cy)
    p["aluminio"] = (cx + (3.454 * 1.5 + 4.443 * 1.5) * k, cy)
    p["borde"] = (cx, cy - 14.07 * k)
    return pieza(W, H, 1 / k, "".join(c), p, margen=1)


def conductor(gotas=False, corona=False):
    """Tramo del conductor visto de lado (hilos de aluminio trenzados), con gotas de lluvia colgando y el brillo
    azulado de la corona en las puntas de las gotas."""
    Wp, Hp = 1600, 500
    c, p = [], {}
    y0 = 220
    c.append(sombra(R(0, y0 - 70, 1600, 140, "url(#gAlu)"), "sCuerpo"))
    c.append(f'<clipPath id="ccond"><rect x="0" y="{y0 - 70}" width="1600" height="140"/></clipPath><g clip-path="url(#ccond)">')
    for x in range(-200, 1700, 34):
        c.append(f'<path d="M{x},{y0 - 70} L{x + 90},{y0 + 70}" stroke="#7F868D" stroke-width="5" opacity="0.8"/>')
        c.append(f'<path d="M{x + 6},{y0 - 70} L{x + 96},{y0 + 70}" stroke="#F4F6F8" stroke-width="4" opacity="0.6"/>')
    c.append('</g>')
    p["conductor"] = (800, y0)
    if gotas:
        for k, x in enumerate(range(140, 1600, 230)):
            h = 46 + (k % 3) * 10
            c.append(f'<path d="M{x - 20},{y0 + 68} C{x - 20},{y0 + 68 + h * 0.6} {x},{y0 + 68 + h} {x},{y0 + 68 + h} '
                     f'C{x},{y0 + 68 + h} {x + 20},{y0 + 68 + h * 0.6} {x + 20},{y0 + 68} Z" fill="#9FD3F2" opacity="0.85"/>')
            c.append(f'<circle cx="{x - 6}" cy="{y0 + 80}" r="5" fill="#FFFFFF" opacity="0.8"/>')
            if corona:
                yt = y0 + 68 + h
                c.append(f'<circle cx="{x}" cy="{yt + 6}" r="34" fill="#6FB7FF" opacity="0.35"/>'
                         f'<circle cx="{x}" cy="{yt + 4}" r="16" fill="#C9E6FF" opacity="0.8"/>')
                for j in range(5):
                    a = math.pi / 2 + (j - 2) * 0.35
                    c.append(f'<line x1="{x}" y1="{yt}" x2="{x + 40 * math.cos(a):.0f}" y2="{yt + 40 * math.sin(a):.0f}" stroke="#B5DBFF" stroke-width="3" opacity="0.8"/>')
            if k == 2:
                p["gota"] = (x, y0 + 68 + h)
    return pieza(Wp, Hp, 0.05, "".join(c), p)


def cadena(anillo=True, n=12, corona=False):
    """Cadena de suspensión: n discos ANSI 52-3 de vidrio templado (Ø255, paso 146 mm), herrajes de bola y casquillo,
    anillo anticorona de aluminio en el lado de la línea, grapa de suspensión y haz de 2 conductores con separador."""
    paso = 146
    Wp, Hp = 900, 260 + n * paso + 520
    cx = 450
    c, p = [], {}
    c.append(R(cx - 60, 0, 120, 120, "url(#gGalv)"))              # herraje a la cruceta
    c.append(f'<circle cx="{cx}" cy="150" r="26" fill="url(#gAceroR)"/>')
    for i in range(n):
        y = 200 + i * paso
        c.append(R(cx - 16, y - 20, 32, paso, "url(#gGalv)"))     # perno y casquillo
        c.append(sombra(f'<ellipse cx="{cx}" cy="{y + 40}" rx="127" ry="38" fill="#4E8E7A" opacity="0.92"/>', "sTorn"))
        c.append(f'<ellipse cx="{cx}" cy="{y + 32}" rx="118" ry="30" fill="#7DC2AA" opacity="0.85"/>')
        c.append(f'<ellipse cx="{cx}" cy="{y + 30}" rx="60" ry="14" fill="#BFE8D8" opacity="0.6"/>')
        c.append(R(cx - 26, y + 40, 52, 34, "url(#gGalv)"))       # casquillo
    yf = 200 + n * paso
    p["disco"] = (cx + 127, 200 + 2 * paso + 40)
    p["disco2"] = (cx + 127, 200 + 3 * paso + 40)
    # grapa de suspensión y anillo
    c.append(R(cx - 40, yf - 10, 80, 90, "url(#gGalv)"))
    if anillo:
        c.append(sombra(f'<ellipse cx="{cx}" cy="{yf - 30}" rx="230" ry="60" fill="none" stroke="url(#gAlu)" stroke-width="34"/>', "sTorn"))
        p["anillo"] = (cx + 230, yf - 30)
        if corona:
            pass
    else:
        p["anillo"] = (cx, yf - 30)
    yb = yf + 160
    c.append(R(cx - 300, yf + 70, 600, 40, "url(#gGalv)"))          # yugo del haz
    for dx in (-260, 260):
        c.append(sombra(f'<circle cx="{cx + dx}" cy="{yb}" r="70" fill="url(#gAluR)"/>', "sTorn"))
        c.append(R(cx + dx - 14, yf + 100, 28, 60, "url(#gGalv)"))
    c.append(R(cx - 200, yb + 160, 400, 36, "url(#gGalv)"))          # separador (abajo, a lo largo del vano)
    for dx in (-260, 260):
        c.append(f'<circle cx="{cx + dx}" cy="{yb + 178}" r="44" fill="url(#gGalv)"/>')
    p["haz"] = (cx, yb)
    p["separador"] = (cx, yb + 178)
    if corona:
        for (x, y) in ((cx - 40, yf + 20), (cx + 40, yf + 20), (cx, yf + 75)):
            c.append(f'<circle cx="{x}" cy="{y}" r="40" fill="#6FB7FF" opacity="0.4"/><circle cx="{x}" cy="{y}" r="16" fill="#D7ECFF" opacity="0.85"/>')
    return pieza(Wp, Hp, 1.0, "".join(c), p, margen=20)


def torre(noche=False):
    """Torre de celosía de acero galvanizado (circuito sencillo horizontal) con 3 cadenas y fases en haz de 2,
    y el hilo de guarda arriba. Escena (no a escala de mm reales: 1 px ≈ 25 mm)."""
    Wp, Hp = 1400, 2000
    c, p = [], {}
    if noche:
        c.append(R(0, 0, Wp, Hp, "#0B1530", 'opacity="0.0"'))
    gal = "#9DA4AB"
    def L(x1, y1, x2, y2, w=8, col=gal):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"/>'
    # patas y cuerpo
    base = [(330, 2000), (1070, 2000)]
    cint = [(560, 700), (840, 700)]
    c.append(L(330, 2000, 560, 700, 16) + L(1070, 2000, 840, 700, 16))
    for i in range(10):
        t1, t2 = i / 10, (i + 1) / 10
        xa1 = 330 + (560 - 330) * t1; ya1 = 2000 - 1300 * t1
        xb1 = 1070 + (840 - 1070) * t1
        xa2 = 330 + (560 - 330) * t2; ya2 = 2000 - 1300 * t2
        xb2 = 1070 + (840 - 1070) * t2
        c.append(L(xa1, ya1, xb2, ya2) + L(xb1, ya1, xa2, ya2) + L(xa1, ya1, xb1, ya1, 6))
    # cabeza y cruceta
    c.append(L(560, 700, 600, 420, 14) + L(840, 700, 800, 420, 14))
    c.append(L(560, 700, 800, 420) + L(840, 700, 600, 420))
    c.append(L(60, 420, 1340, 420, 14) + L(60, 520, 1340, 520, 10))
    for x in range(60, 1340, 80):
        c.append(L(x, 420, x + 80, 520, 6) + L(x + 80, 420, x, 520, 6))
    c.append(L(600, 420, 700, 120, 12) + L(800, 420, 700, 120, 12) + L(640, 300, 760, 300, 8))
    c.append(L(60, 420, 60, 520, 10) + L(1340, 420, 1340, 520, 10))
    # hilo de guarda
    c.append(L(0, 130, 1400, 130, 6, "#6E757D"))
    p["guarda"] = (1000, 130)
    # 3 cadenas y fases en haz de 2
    for k, x in enumerate((180, 700, 1220)):
        c.append(L(x, 520, x, 520 + 12, 10))
        for i in range(8):
            y = 540 + i * 26
            c.append(f'<ellipse cx="{x}" cy="{y}" rx="28" ry="8" fill="#5FA58D"/>')
        c.append(f'<ellipse cx="{x}" cy="{540 + 8 * 26}" rx="44" ry="11" fill="none" stroke="#D9DEE3" stroke-width="7"/>')
        yc = 540 + 8 * 26 + 30
        c.append(L(x - 40, yc, x + 40, yc, 8))
        for dx in (-40, 40):
            c.append(L(0, yc + 6, 1400, yc + 6, 0))
        p[f"fase{k}"] = (x, yc)
    yc = 540 + 8 * 26 + 30
    for dy in (0, 26):
        c.append(f'<path d="M0,{yc + 40 + dy} Q700,{yc + 10 + dy} 1400,{yc + 40 + dy}" stroke="#C3C9CF" stroke-width="7" fill="none"/>')
    p["cadena"] = (700, 640)
    return pieza(Wp, Hp, 0.25, "".join(c), p)


CATALOGO = {"acsr": acsr, "cond": lambda: conductor(False, False), "cond_gotas": lambda: conductor(True, False),
            "cond_corona": lambda: conductor(True, True), "cadena": lambda: cadena(True), "cadena_sin": lambda: cadena(False),
            "cadena_corona": lambda: cadena(False, corona=True), "torre": lambda: torre()}
GRUPOS = {40: ["acsr"], 12: ["cond", "cond_gotas", "cond_corona"], 1: ["cadena", "cadena_sin", "cadena_corona"], 6: ["torre"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

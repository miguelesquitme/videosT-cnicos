"""Lote H v2 (25-nov): 5 equipos × 6 infografías con FOTOS OFICIALES del fabricante (sin marcas de agua).
Correcciones del usuario: fotos nítidas y bien definidas; recuadros de color SIN borde; versus entre TIPOS de equipo
(guardamotor vs breaker, breaker vs fusible, relé vs contactor, inductivo vs capacitivo; sin versus del contactor);
no escribir marca, serie ni código del equipo en los textos. Fuentes en referencias/loteH_fuentes.md."""
import math
import subprocess
import sys
from pathlib import Path

AQ = Path(__file__).parent
sys.path.insert(0, str(AQ))
from base import (Img, page, kick, T, svg, tabla, chips, nota, DID, NAV, AZ, TEAL, NAR, RJ, VER, MOR, CL,  # noqa: E402
                  hexa, cajas, marcas, letras, ph, cap, crit, versus, vsbadge, leyenda, blk, flecha, tx, curva, pts, YT)

FOTO = "imagen oficial del fabricante"
P = {}


def tarjetas(x, y, w, items, gap=12, size=30):
    """Tarjetas con franja de color (sin borde): (título, texto, color)."""
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;display:grid;gap:{gap}px'>"
            + "".join(f"<div style='border-radius:16px;background:{hexa(c, .08)};padding:10px 16px 11px;font:500 17px/1.3 Montserrat;color:#1d2939;"
                      f"box-shadow:inset 8px 0 0 {c}'><b style='display:block;font:900 {size}px/1.05 \"Barlow C\";color:{c};padding-left:4px'>{t}</b>"
                      f"<span style='display:block;padding-left:4px'>{d}</span></div>" for t, d, c in items) + "</div>")


def pasos(x, y, w, items, gap=10):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;display:grid;gap:{gap}px'>"
            + "".join(f"<div style='display:flex;gap:12px;align-items:center;border-radius:14px;background:#F6FAFF;padding:8px 12px;font:500 16px/1.28 Montserrat;color:#1d2939'>"
                      f"<div style='flex:none;width:38px;height:38px;border-radius:50%;background:{CL[(n - 1) % 8]};color:#fff;font:800 19px/38px Montserrat;text-align:center'>{n}</div>"
                      f"<div><b style='color:#0B1F4D'>{t}</b> {d}</div></div>" for n, t, d in items) + "</div>")


def duelo(fa, fb, ta, tb, ca, cb, top=280, h=430):
    """Dos fotos de tipos distintos con VS al centro."""
    return (ph(40, top, 470, h) + fa.html(False) + ph(570, top, 470, h) + fb.html(False)
            + f"<div style='position:absolute;left:40px;top:{top + h - 62}px;width:470px;text-align:center'><span style='background:{ca};color:#fff;font:900 30px \"Barlow C\";padding:6px 18px;border-radius:10px'>{ta}</span></div>"
            + f"<div style='position:absolute;left:570px;top:{top + h - 62}px;width:470px;text-align:center'><span style='background:{cb};color:#fff;font:900 30px \"Barlow C\";padding:6px 18px;border-radius:10px'>{tb}</span></div>"
            + vsbadge(540, top + h / 2 - 20))


def usar(top, a, b, ca, cb):
    """Cuándo usar cada uno: dos tarjetas."""
    return (f"<div style='position:absolute;left:40px;right:40px;top:{top}px;display:grid;grid-template-columns:1fr 1fr;gap:16px'>"
            + "".join(f"<div style='border-radius:16px;background:{hexa(c, .10)};padding:12px 16px;font:500 17px/1.32 Montserrat;color:#1d2939'>"
                      f"<b style='display:block;font:900 24px \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for (t, d), c in ((a, ca), (b, cb))) + "</div>")


class _Box:
    def __init__(s, x, y, w, h):
        s.x, s.y, s.w, s.h = x, y, w, h

    def r(s, b):
        return s.x + b[0] * s.w, s.y + b[1] * s.h, s.x + b[2] * s.w, s.y + b[3] * s.h


# ===================================================================== GUARDAMOTOR (9–14 A, pulsadores)
C1 = AZ
F_GM = "hoja de datos y placa del fabricante · IEC 60947-2 · IEC 60947-4-1"
GMB = {"ent": (.40, .21, .74, .31), "dial": (.43, .44, .57, .57), "test": (.55, .64, .66, .70), "sal": (.40, .78, .74, .88),
       "on": (.71, .40, .88, .62), "off": (.57, .43, .70, .65), "iec": (.67, .64, .84, .70)}
f = Img("gm_f", 250, 270, w=600)
P["H01_guardamotor_partes"] = page(DID,
    kick("GUARDAMOTOR · PARTES", C1) + T("Las partes del", "guardamotor", C1, sub="9–14 A · pulsadores I/O · disparo térmico + magnético", size=60)
    + f.html() + cajas(f, [
        (1, GMB["ent"], "Entrada 1/L1 3/L2 5/L3", "llega la red", 30, 400),
        (2, GMB["dial"], "Dial 9–14 A", "ajuste del térmico (Ir)", 30, 560),
        (3, GMB["test"], "TEST", "prueba el disparo", 30, 720),
        (4, GMB["sal"], "Salida 2/T1 4/T2 6/T3", "va al contactor / motor", 30, 900),
        (5, GMB["on"], "Pulsador I (ON)", "cierra los 3 polos", 790, 430),
        (6, GMB["off"], "Pulsador O (OFF)", "abre a mano", 790, 600),
        (7, GMB["iec"], "IEC 60947-2 / -4-1", "normas impresas", 790, 760)], wl=270)
    + chips(1015, [("9–14 A", "Rango del térmico: el dial va a la corriente de placa del motor.", C1),
                   ("170 A", "Disparo magnético instantáneo (cortocircuito).", RJ),
                   ("CLASE 10A", "A 7,2 × Ir dispara entre 2 y 10 s.", NAR)])
    + nota(1150, "Un solo aparato: <b>seccionador + sobrecarga + cortocircuito + falta de fase</b>. Va en riel DIN de 35 mm."),
    F_GM, FOTO)


def _gm_curva(P):
    s = []
    up = [(1.2, 7200), (1.5, 120), (3, 30), (7.2, 10), (12.1, 6), (12.1, .01)]
    s.append(f"<polyline points='{pts(P, up)}' fill='none' stroke='{AZ}' stroke-width='4' stroke-dasharray='10 6'/>")
    x7, y10 = P(7.2, 10)
    _, y2 = P(7.2, 2)
    s.append(f"<line x1='{x7:.0f}' y1='{y10:.0f}' x2='{x7:.0f}' y2='{y2:.0f}' stroke='{NAR}' stroke-width='12' stroke-linecap='round'/>")
    s.append(tx(x7 - 12, (y10 + y2) / 2, "7,2×: 2–10 s", 17, 800, NAR, "end"))
    for a, b, t, c, dy in ((1.05, 7200, "1,05×: NO dispara en 2 h", VER, -16), (1.2, 7200, "1,2×: dispara &lt; 2 h", AZ, 18), (1.5, 120, "1,5×: &lt; 2 min", AZ, 0)):
        px, py = P(a, b)
        s.append(f"<circle cx='{px:.0f}' cy='{py:.0f}' r='8' fill='{c}' stroke='#fff' stroke-width='3'/>")
        s.append(tx(px + 14, py + dy, t, 16, 800, c, "start"))
    xm, _ = P(12.1, 1)
    s.append(f"<rect x='{xm - 4:.0f}' y='{P(12.1, 1)[1]:.0f}' width='8' height='{P(12.1, .01)[1] - P(12.1, 1)[1]:.0f}' fill='{RJ}' rx='4'/>")
    s.append(tx(xm - 10, P(12.1, .03)[1], "170 A = 12 × 14 A", 17, 800, RJ, "end"))
    s.append(tx(P(1.3, .02)[0], P(1.3, .02)[1], "curva: forma ilustrativa", 14, 600, "#98A2B3", "start"))
    return "".join(s)


f = Img("gm_f", 40, 265, h=420)
P["H02_guardamotor_funcionamiento"] = page(DID,
    kick("GUARDAMOTOR · CÓMO DISPARA", C1) + T("Tres disparos en", "un aparato", C1, sub="Térmico, magnético y falta de fase actúan sobre el mismo mecanismo", size=58)
    + f.html() + marcas(f, [(1, GMB["dial"]), (2, GMB["test"])])
    + tarjetas(430, 265, 610, [
        ("TÉRMICO · SOBRECARGA", "Un <b>bimetal por fase</b> se calienta con la corriente. Al pasar de 1,2 × Ir se dobla, empuja la regleta y abre los 3 polos.", AZ),
        ("MAGNÉTICO · CORTOCIRCUITO", "Una <b>bobina por fase</b> atrae su núcleo al llegar a <b>170 A</b> y golpea el mecanismo: abre al instante, sin fusibles.", RJ),
        ("FALTA DE FASE", "La regleta <b>diferencial</b> compara las 3 fases: una en cero y las otras a 1,15 × Ir → dispara en menos de 2 h.", NAR)], gap=10, size=28)
    + curva(130, 730, 900, 340, (1, 20), (.01, 7200), _gm_curva,
            [(1, "1"), (1.2, "1,2"), (1.5, "1,5"), (2, "2"), (3, "3"), (5, "5"), (7.2, "7,2"), (10, "10"), (12.1, "12"), (20, "20")], YT,
            "múltiplos de la corriente ajustada Ir (con Ir = 14 A)")
    + nota(1150, "1 = dial: fija Ir entre 9 y 14 A · 2 = TEST: dispara el mecanismo sin corriente, para probarlo."),
    F_GM + " (tabla de disparo clase 10A y falta de fase)", FOTO)

f = Img("gm_pc", 40, 290, w=490)
P["H03_guardamotor_criterios"] = page(DID,
    kick("GUARDAMOTOR · SELECCIÓN", C1) + T("Cómo escoger el", "guardamotor", C1, sub="Todo está en la placa lateral del equipo y en la del motor", size=60)
    + ph(30, 280, 510, 590) + f.html(False) + letras(f, [
        ("A", (.50, .29, .93, .48), AZ, "tr"), ("B", (.51, .48, .92, .92), RJ, "br"), ("C", (.13, .64, .50, .82), VER, "bl")])
    + leyenda(890, [("A", "Ie 9–14 A · Ue 690 V", "AC-3, Uimp 8 kV", AZ), ("B", "Icu / Ics", "100 kA a 230/240 V · 15 kA a 400 V", RJ),
                    ("C", "Potencia", "3 kW a 230 V · 5,5 kW a 400 V", VER)], cols=1, x=30, w=510)
    + crit(285, [("Corriente del motor", "La de placa debe caer en el rango; el dial se pone en ella.", "9–14 A", AZ),
                 ("Tensión de la red", "Ue del equipo ≥ tensión entre fases (208/240 V).", "690 V", NAV),
                 ("Poder de corte", "Icu ≥ corriente de cortocircuito donde se instala.", "100 kA", RJ),
                 ("Clase de disparo", "10A = arranque normal. Arranques largos piden clase 20 o 30.", "10A", NAR),
                 ("Potencia de referencia", "Placa: 3 kW a 230 V, 5,5 kW a 400 V.", "3 kW", VER),
                 ("Accesorios", "Contactos auxiliares frontales o laterales (1NA+1NC o 2NA).", "AUX", MOR)], x=560, w=480)
    + nota(1100, "Si el motor marca más de 14 A, no es este rango: sube al siguiente (13–18 A). Nunca pongas el dial <b>por encima</b> de la placa."),
    F_GM, FOTO)

fq = Img("gm_f", 150, 370, h=320)
fk = Img("km_f", 120, 700, h=290)
P["H04_guardamotor_aplicacion"] = page(DID,
    kick("GUARDAMOTOR · CASO REAL", C1) + T("Bomba de 3 hp con", "guardamotor", C1, sub="Red 208 V trifásica · arranque directo · sin fusibles", size=58)
    + blk(150, 280, 270, "RED 208 V 3~", "L1 · L2 · L3 · PE", NAV)
    + fq.html() + marcas(fq, [(1, GMB["dial"])])
    + fk.html()
    + blk(150, 1005, 270, "MOTOR 3 hp", "208 V · jaula de ardilla", NAV)
    + svg(0, 0, 1080, 1350, flecha(285, 355, 285, 385) + flecha(285, 675, 285, 712) + flecha(285, 975, 285, 1005))
    + "<div style='position:absolute;left:40px;top:500px;font:900 32px \"Barlow C\";color:#0057FF'>-QM1</div>"
    + "<div style='position:absolute;left:40px;top:830px;font:900 32px \"Barlow C\";color:#0B1F4D'>-KM1</div>"
    + tarjetas(620, 280, 420, [
        ("10,6 A", "Corriente de tabla NEC 430.250 para 3 hp a 208 V → cae en 9–14 A.", AZ),
        ("DIAL = PLACA", "1 = dial: se ajusta a la corriente de placa del motor, no a la de tabla.", NAR),
        ("14 AWG", "Conductor al 125 %: 13,3 A → 14 AWG THHN (75 °C).", VER),
        ("170 A", "Si hay cortocircuito, el magnético abre en milisegundos.", RJ),
        ("100 kA", "Icu a 230/240 V: soporta la falla del tablero sin fusibles.", MOR)])
    + nota(1110, "En instalaciones NEC, para proteger <b>solo</b> el cortocircuito debe estar listado como <b>Tipo E</b>; si no, se pone breaker o fusibles antes."),
    F_GM + " · NEC 2020 T430.250, 430.22, 430.32, 430.52", FOTO)

fa = Img("gm_f", 140, 290, h=340)
fb = Img("br_f", 700, 290, h=340)
P["H05_guardamotor_vs_breaker"] = page(DID,
    kick("COMPARACIÓN · PROTECCIONES", C1) + T("Guardamotor contra", "breaker", C1, sub="Los dos son termomagnéticos, pero protegen cosas distintas", size=58)
    + duelo(fa, fb, "GUARDAMOTOR", "BREAKER", AZ, NAR)
    + versus(740, "Guardamotor", "Breaker", [
        ("Protege", "al motor", "al cable"), ("Ajuste térmico", "9–14 A regulable", "fijo: 63 A"),
        ("Disparo magnético", "170 A (≈ 12 × Ir)", "315–630 A (curva C)"), ("Falta de fase", "sí", "no"),
        ("Poder de corte", "100 kA a 230 V", "6 kA"), ("Norma", "IEC 60947-2 / -4-1", "IEC 60898-1")], dif=(1, 3))
    + usar(1100, ("USA GUARDAMOTOR", "Para cada motor: se ajusta a su placa y detecta fase perdida."),
           ("USA BREAKER", "Para alimentadores, tomas, iluminación y cargas sin ajuste."), AZ, NAR),
    F_GM + " · hoja de datos del breaker · IEC 60898-1", FOTO)

s = Img("04_guardamotor_simbolo", 40, 300, w=470)
f = Img("gm_f", 580, 270, h=470)
f2 = Img("gm_pc", 650, 770, w=330)
P["H06_guardamotor_simbolo"] = page(DID,
    kick("GUARDAMOTOR · SÍMBOLO IEC 60617", C1) + T("Símbolo del", "guardamotor", C1, sub="Cada parte del símbolo está en el equipo", size=60)
    + ph(30, 280, 490, 450) + s.html(False)
    + letras(s, [("A", (.10, .22, .22, .36), AZ), ("B", (.30, .02, .82, .38), RJ, "tr"), ("C", (.28, .53, .88, .65), NAR, "tr"),
                 ("D", (.28, .65, .88, .77), MOR, "br"), ("E", (.30, .78, .82, .94), VER, "bl")])
    + f.html() + letras(f, [("A", (.57, .40, .88, .65), AZ, "tr"), ("B", GMB["ent"], RJ, "tr"), ("C", GMB["dial"], NAR),
                            ("E", GMB["sal"], VER, "bl")])
    + f2.html() + letras(f2, [("F", (.13, .34, .34, .58), TEAL, "tl")])
    + cap(620, 1160, 400, "F: el mismo símbolo impreso en la placa lateral")
    + leyenda(750, [("A", "Mando manual", "→ pulsadores I / O", AZ), ("B", "Polos 1/L1 3/L2 5/L3 (×)", "→ bornes de entrada", RJ),
                    ("C", "Disparador térmico", "→ dial 9–14 A", NAR), ("D", "Disparador magnético I&gt;", "→ adentro, 170 A (no se ve)", MOR),
                    ("E", "Salidas 2/T1 4/T2 6/T3", "→ bornes de abajo", VER), ("F", "Símbolo en placa", "→ costado del equipo", TEAL)], cols=1, x=30, w=500),
    "IEC 60617 (símbolos) · IEC 81346 (-QM) · " + F_GM, FOTO + " · símbolo: catálogo @miguelesquit")

# ===================================================================== BREAKER 2P C63
C2 = NAR
F_BR = "hoja de datos del fabricante · IEC 60898-1 · marcado del equipo"
BRB = {"ent": (.24, .13, .78, .22), "c63": (.23, .33, .37, .40), "v": (.23, .40, .33, .45), "iec": (.23, .45, .44, .48), "sal": (.24, .75, .78, .85),
       "ven": (.35, .38, .41, .43), "sim": (.57, .42, .67, .51), "onoff": (.38, .45, .49, .51), "pal": (.24, .52, .76, .71)}
f = Img("br_f", 300, 270, h=720)
P["H07_breaker_partes"] = page(DID,
    kick("BREAKER · PARTES", C2) + T("Las partes del", "breaker", C2, sub="Interruptor termomagnético de 2 polos, 63 A, curva C", size=62)
    + f.html() + cajas(f, [
        (1, BRB["ent"], "Entrada 1 · 3", "bornes de arriba", 30, 380),
        (2, BRB["c63"], "C63", "curva C · In = 63 A", 30, 520),
        (3, BRB["v"], "400 V~ · 6000", "tensión e Icn = 6000 A", 30, 640),
        (4, BRB["sal"], "Salida 2 · 4", "bornes de abajo", 30, 900),
        (5, BRB["ven"], "Ventanilla", "posición del contacto", 790, 400),
        (6, BRB["sim"], "Símbolo impreso", "1-3 arriba, 2-4 abajo", 790, 530),
        (7, BRB["onoff"], "I ON · O OFF", "posiciones de la palanca", 790, 660),
        (8, BRB["pal"], "Palanca unida", "los 2 polos abren juntos", 790, 790)], wl=260)
    + chips(1015, [("63 A", "Corriente nominal In.", C2), ("CURVA C", "Magnético entre 5 y 10 × In: 315–630 A.", RJ),
                   ("6 kA", "Icn: máxima falla que interrumpe.", AZ)])
    + nota(1150, "Arriba entra la línea y abajo sale la carga; la palanca <b>única</b> evita que quede una fase energizada."),
    F_BR, FOTO)


def _br_curva(P):
    s = []
    x5, _ = P(5, 7200)
    x10, ybot = P(10, .01)
    _, y01 = P(5, .1)
    s.append(f"<rect x='{x5:.0f}' y='{y01:.0f}' width='{x10 - x5:.0f}' height='{ybot - y01:.0f}' fill='{hexa(RJ, .25)}'/>")
    s.append(tx((x5 + x10) / 2, y01 - 16, "magnético C", 16, 800, RJ))
    s.append(tx((x5 + x10) / 2, (y01 + ybot) / 2, "5–10 × In", 16, 800, RJ))
    xa, ya = P(2.55, 120)
    _, yb = P(2.55, 1)
    s.append(f"<line x1='{xa:.0f}' y1='{ya:.0f}' x2='{xa:.0f}' y2='{yb:.0f}' stroke='{NAR}' stroke-width='12' stroke-linecap='round'/>")
    s.append(tx(xa + 14, (ya + yb) / 2, "2,55×: 1–120 s", 16, 800, NAR, "start"))
    for a, b, t, c, dy in ((1.13, 3600, "1,13×: NO dispara en 1 h", VER, -18), (1.45, 3600, "1,45×: dispara &lt; 1 h", AZ, 18)):
        px, py = P(a, b)
        s.append(f"<circle cx='{px:.0f}' cy='{py:.0f}' r='8' fill='{c}' stroke='#fff' stroke-width='3'/>")
        s.append(tx(px + 14, py + dy, t, 16, 800, c, "start"))
    up = [(1.45, 3600), (2.55, 120), (5, 25), (10, 8), (10, .01)]
    s.append(f"<polyline points='{pts(P, up)}' fill='none' stroke='{AZ}' stroke-width='4' stroke-dasharray='10 6'/>")
    s.append(tx(P(1.2, .02)[0], P(1.2, .02)[1], "curva: forma ilustrativa", 14, 600, "#98A2B3", "start"))
    return "".join(s)


f = Img("br_3", 60, 265, h=420)
P["H08_breaker_funcionamiento"] = page(DID,
    kick("BREAKER · CÓMO DISPARA", C2) + T("Así dispara un", "breaker C63", C2, sub="Dos disparadores por polo y una cámara que apaga el arco", size=60)
    + f.html()
    + tarjetas(430, 265, 610, [
        ("BIMETAL · SOBRECARGA", "Con 63 A: <b>71 A</b> (1,13 ×) no dispara en 1 h; <b>91 A</b> (1,45 ×) dispara en menos de 1 h; <b>161 A</b> (2,55 ×) entre 1 y 120 s.", AZ),
        ("BOBINA · CORTOCIRCUITO", "Curva C: a <b>315 A</b> (5 ×) no debe disparar en 0,1 s; a <b>630 A</b> (10 ×) dispara en menos de 0,1 s.", RJ),
        ("CÁMARA DE ARCO", "Placas metálicas dividen y enfrían el arco al abrir; corta hasta <b>6000 A</b> (Icn).", NAR)], gap=10, size=28)
    + curva(130, 730, 900, 340, (1, 20), (.01, 7200), _br_curva,
            [(1, "1"), (1.13, ""), (1.45, "1,45"), (2, "2"), (2.55, "2,55"), (5, "5"), (10, "10"), (20, "20")], YT,
            "múltiplos de In  (In = 63 A → 5 × = 315 A, 10 × = 630 A)")
    + nota(1150, "La zona roja es la <b>curva C</b>: tolera el arranque de motores pequeños y transformadores sin disparar."),
    F_BR + " · tiempos convencionales para In ≤ 63 A", FOTO)

f = Img("br_f", 110, 290, h=560)
P["H09_breaker_criterios"] = page(DID,
    kick("BREAKER · SELECCIÓN", C2) + T("Cómo escoger el", "breaker", C2, sub="Lo que dice el frente y lo que debes comprobar", size=60)
    + ph(30, 280, 510, 580) + f.html(False)
    + letras(f, [("A", BRB["c63"], AZ), ("B", BRB["v"], RJ, "bl"), ("C", BRB["iec"], VER, "br"), ("D", BRB["pal"], NAR, "tr")])
    + leyenda(880, [("A", "C63", "curva C y 63 A", AZ), ("B", "400 V~ · 6000", "tensión y Icn en A", RJ), ("C", "IEC/EN 60898-1", "norma", VER),
                    ("D", "2 polos", "una palanca", NAR)], cols=2, x=30, w=510)
    + crit(285, [("Corriente In", "Protege al CONDUCTOR: 63 A pide mínimo 6 AWG THHN (65 A a 75 °C).", "63 A", AZ),
                 ("Curva", "B: resistivas · C: motores pequeños y transformadores · D: arranques fuertes.", "C", RJ),
                 ("Poder de corte", "Icn ≥ corriente de cortocircuito en el tablero.", "6 kA", NAR),
                 ("Polos", "A 208/240 V entre fases las dos líneas tienen tensión: 2 polos.", "2P", VER),
                 ("Tensión", "400 V~: sirve en redes de 120/208 V y 120/240 V.", "400 V", NAV),
                 ("Vida útil", "Eléctrica 10 000 maniobras · mecánica 20 000.", "10 000", MOR)], x=560, w=480)
    + nota(1090, "Primero el <b>conductor</b>, luego el breaker: el breaker nunca debe ser mayor que lo que aguanta el cable."),
    F_BR + " · NEC 2020 T310.16", FOTO)

fb = Img("br_f", 350, 400, h=330)
P["H10_breaker_aplicacion"] = page(DID,
    kick("BREAKER · CASO REAL", C2) + T("Calentador de 10 kW a", "208 V", C2, sub="Carga resistiva continua entre dos fases", size=58)
    + blk(320, 280, 270, "BARRAS L1 · L2", "208 V entre fases", NAV)
    + fb.html()
    + "<div style='position:absolute;left:270px;top:540px;font:900 34px \"Barlow C\";color:#FF8A00'>-F1</div>"
    + blk(320, 770, 270, "6 AWG THHN", "2 líneas + tierra", NAV)
    + blk(320, 900, 270, "CALENTADOR", "10 kW · 208 V · 1~", NAR)
    + svg(0, 0, 1080, 1350, flecha(455, 355, 455, 398) + flecha(455, 735, 455, 770) + flecha(455, 845, 455, 900))
    + tarjetas(640, 280, 400, [
        ("48,1 A", "I = 10 000 W ÷ 208 V.", AZ),
        ("× 1,25 = 60,1 A", "Carga continua (3 h o más): protección al 125 %.", NAR),
        ("63 A · 2P", "Valor IEC siguiente; 2 polos porque L1 y L2 tienen tensión.", RJ),
        ("6 AWG", "65 A a 75 °C ≥ 63 A del breaker.", VER),
        ("CURVA C", "Aquí bastaría B; la C también sirve (no hay arranque).", MOR)])
    + nota(1060, "Con breaker de 1 polo, al disparar quedaría <b>L2 energizada</b> dentro del calentador: por eso 2P con palanca unida."),
    F_BR + " · NEC 2020 210.19(A), 210.20(A), T310.16", FOTO)

fa = Img("br_f", 165, 290, h=340)
fb = Img("fu", 730, 290, h=340)
P["H11_breaker_vs_fusible"] = page(DID,
    kick("COMPARACIÓN · PROTECCIONES", C2) + T("Breaker contra", "fusible", C2, sub="Breaker 2P C63 frente a fusible NH000 gG de 63 A", size=60)
    + duelo(fa, fb, "BREAKER", "FUSIBLE", NAR, RJ)
    + versus(740, "Breaker", "Fusible", [
        ("Después de la falla", "se rearma", "se cambia"), ("Poder de corte", "6 kA", "120 kA"),
        ("Sobrecarga (en 1 h)", "1,13× no · 1,45× sí", "1,25× no · 1,6× sí"), ("Cortocircuito", "curva C: 315–630 A", "gG: funde en todo el rango"),
        ("Tensión", "400 V~", "500 V~ · 250 V="), ("Norma", "IEC 60898-1", "IEC 60269")], dif=(0, 1))
    + usar(1100, ("USA BREAKER", "Circuitos finales donde la falla es baja y conviene rearmar rápido."),
           ("USA FUSIBLE", "Donde la falla es muy alta o como respaldo de otros equipos."), NAR, RJ),
    F_BR + " · hoja de datos del fusible · IEC 60269-1", FOTO)

s = Img("02_disyuntor_2p_simbolo", 70, 300, w=420)
f = Img("br_f", 580, 270, h=760)
P["H12_breaker_simbolo"] = page(DID,
    kick("BREAKER · SÍMBOLO IEC 60617", C2) + T("Símbolo del", "breaker 2P", C2, sub="El símbolo viene impreso en el propio frente", size=60)
    + ph(30, 280, 480, 420) + s.html(False)
    + letras(s, [("A", (.30, .08, .80, .30), AZ, "tr"), ("B", (.36, .32, .80, .48), RJ, "tr"), ("C", (.38, .45, .64, .53), NAR, "bl"),
                 ("D", (.30, .60, .80, .95), VER, "br")])
    + f.html() + letras(f, [("A", BRB["ent"], AZ, "tr"), ("C", BRB["pal"], NAR, "tr"), ("D", BRB["sal"], VER, "br"), ("E", BRB["sim"], TEAL, "tr")])
    + leyenda(740, [("A", "Bornes 1 y 3", "→ entradas de arriba", AZ), ("B", "× función de disyuntor", "→ disparo térmico y magnético dentro", RJ),
                    ("C", "Línea de acción", "→ palanca unida de los 2 polos", NAR), ("D", "Bornes 2 y 4", "→ salidas de abajo", VER),
                    ("E", "Símbolo impreso", "→ al lado de la palanca", TEAL)], cols=1, x=30, w=480)
    + nota(1100, "La <b>×</b> en el contacto distingue al disyuntor del simple interruptor; la línea punteada dice que los polos se mueven juntos.").replace("left:40px;right:40px", "left:40px;right:560px"),
    "IEC 60617 · IEC 81346 (-F) · " + F_BR, FOTO + " · símbolo: catálogo @miguelesquit")

# ===================================================================== RELÉ 2 CO 230 VAC
C3 = RJ
F_RE = "hoja de datos del fabricante · marcado del relé · EN 50005"
REB = {"test": (.50, .06, .80, .16), "led": (.03, .09, .21, .16), "bob": (.15, .27, .49, .62), "emp": (.32, .51, .58, .67),
       "con": (.43, .63, .57, .78), "pin": (.17, .82, .89, .99), "pal": (.74, .12, .97, .58)}
f = Img("re_f", 265, 265, h=760)
P["H13_rele_partes"] = page(DID,
    kick("RELÉ · PARTES", C3) + T("Las partes del", "relé", C3, sub="Relé enchufable de 2 contactos conmutados, bobina 230 VAC", size=62)
    + f.html() + cajas(f, [
        (1, REB["led"], "LED", "bobina energizada", 20, 320),
        (2, REB["bob"], "Bobina 230 VAC", "1,6 VA a 50 Hz", 20, 500),
        (3, REB["emp"], "Empujador", "mueve los contactos", 20, 680),
        (4, REB["pin"], "Pines planos", "al zócalo de riel", 20, 900),
        (5, REB["test"], "Botón de prueba", "bloqueable · naranja = AC", 800, 320),
        (6, REB["pal"], "Palanca de prueba", "baja hasta el empujador", 800, 480),
        (7, REB["con"], "Contactos AgNi", "12 A a 250 VAC", 800, 680)], wl=260)
    + chips(1040, [("2 CO", "Dos conmutados: 11-12-14 y 41-42-44.", C3), ("12 A · 250 VAC", "Carga resistiva AC1 (3000 VA).", AZ),
                   ("27 × 21 × 36 mm", "Se enchufa en zócalo de riel DIN.", NAR)])
    + nota(1170, "Tapa transparente: se ve la bobina y el contacto. El botón naranja indica <b>bobina de AC</b> (verde = DC)."),
    F_RE, FOTO)

f = Img("re_f", 40, 265, h=560)
P["H14_rele_funcionamiento"] = page(DID,
    kick("RELÉ · CÓMO FUNCIONA", C3) + T("Así conmuta un", "relé", C3, sub="Se ve a través de la tapa transparente", size=62)
    + f.html() + marcas(f, [(1, REB["bob"]), (2, REB["emp"]), (3, REB["con"]), (4, REB["led"])])
    + pasos(470, 270, 570, [(1, "Bobina:", "llegan 230 VAC a A1-A2 y circulan ≈ 7 mA (1,6 VA)."),
                            (2, "Armadura y empujador:", "el campo atrae la armadura y el empujador mueve la carta de contactos."),
                            (3, "Contactos:", "los comunes 11 y 41 dejan el NC (12, 42) y tocan el NA (14, 44)."),
                            (4, "LED:", "se enciende mientras haya tensión en la bobina.")])
    + tabla(860, [("Bobina A1-A2", "0 V  →  230 V"), ("11-12 · 41-42 (NC)", "cerrado → ABIERTO"), ("11-14 · 41-44 (NA)", "abierto → CERRADO"),
                  ("LED", "apagado → ENCENDIDO")], cab="<span>ESTADO</span><span style='flex:none'>REPOSO → ENERGIZADO</span>", extra="font-size:20px")
    + nota(1160, "Cierra con <b>184 a 253 V</b> en la bobina. El botón de prueba mueve los contactos a mano para <b>probar sin tensión</b>."),
    F_RE, FOTO)

f = Img("re_z", 40, 285, w=490)
P["H15_rele_criterios"] = page(DID,
    kick("RELÉ · SELECCIÓN", C3) + T("Cómo escoger el", "relé", C3, sub="La tensión de la bobina y el tipo de carga deciden", size=62)
    + ph(30, 280, 510, 560) + f.html(False)
    + letras(f, [("A", (.36, .24, .62, .55), AZ, "tr"), ("B", (.12, .40, .34, .70), RJ, "tl"), ("C", (.06, .66, .96, .96), NAR, "bl")])
    + leyenda(860, [("A", "Relé enchufable", "2 conmutados, 12 A", AZ), ("B", "Módulo enchufable", "opcional: señal o supresión", RJ),
                    ("C", "Zócalo con clip", "12 A · 300 VAC, bornes de tornillo", NAR)], cols=1, x=30, w=510)
    + crit(285, [("Tensión de bobina", "Cierra entre 184 y 253 V: sirve a 208 o 240 V entre fases; a 120 V NO.", "230 VAC", AZ),
                 ("Carga resistiva", "AC1 12 A a 250 V (3000 VA). DC1: 12 A a 24 V.", "12 A", RJ),
                 ("Carga inductiva", "Bobinas y pilotos (AC15): 1,5 A a 240 V, 3 A a 120 V.", "1,5 A", NAR),
                 ("Carga mínima", "10 V / 5 mA. Para señales de PLC usa contactos dorados.", "5 mA", VER),
                 ("Zócalo", "Del mismo fabricante: 12 A, 300 V, riel 35 mm.", "35 mm", NAV),
                 ("Temperatura", "Con bobina AC: −40 a +55 °C.", "55 °C", MOR)], x=560, w=480)
    + nota(1090, "Los 12 A son para carga <b>resistiva</b>. Para una bobina de contactor o un motor mira la categoría AC15, que es mucho menor."),
    F_RE, FOTO)

fr = Img("re_z", 400, 400, h=330)
P["H16_rele_aplicacion"] = page(DID,
    kick("RELÉ · CASO REAL", C3) + T("El PLC sabe que el", "motor arrancó", C3, sub="Mando a 240 V separado de las entradas de 24 VDC", size=56)
    + blk(330, 285, 420, "MANDO 240 VAC", "A1-A2 en paralelo con la bobina de -KM1", NAV)
    + fr.html()
    + "<div style='position:absolute;left:250px;top:540px;font:900 34px \"Barlow C\";color:#E5383B'>-KA1</div>"
    + blk(40, 860, 470, "11-14 → PLC  I0.0", "24 VDC; aislamiento entre bobina y contactos", AZ)
    + blk(570, 860, 470, "41-44 → PILOTO -H1", "verde 240 V: «motor en marcha»", VER)
    + svg(0, 0, 1080, 1350, flecha(540, 370, 540, 400) + flecha(480, 740, 275, 855, AZ) + flecha(600, 740, 805, 855, VER))
    + chips(1010, [("CARGA MÍNIMA", "Una entrada de PLC toma ≈ 4 mA: menos que 5 mA → pide contactos dorados.", RJ),
                   ("NC LIBRES", "11-12 y 41-42 quedan para alarmas o enclavamientos.", NAR)], cols=2)
    + nota(1150, "El relé <b>separa</b> dos tensiones: 240 VAC del mando y 24 VDC del PLC nunca se tocan."),
    F_RE + " · entrada típica de PLC 24 VDC ≈ 4 mA", FOTO)

fa = Img("re_f", 170, 290, h=340)
fb = Img("km_f", 635, 290, h=340)
P["H17_rele_vs_contactor"] = page(DID,
    kick("COMPARACIÓN · MANIOBRA", C3) + T("Relé contra", "contactor", C3, sub="Los dos son electroimanes con contactos, pero de tamaños distintos", size=58)
    + duelo(fa, fb, "RELÉ", "CONTACTOR", RJ, VER)
    + versus(740, "Relé", "Contactor", [
        ("Corriente", "12 A (AC1)", "50 A (AC-3) · 80 A (AC-1)"), ("Contactos", "2 conmutados", "3 polos NA + 1NA+1NC"),
        ("Bobina 220/230 V", "1,6 VA", "140 VA al cerrar · 13 VA"), ("Vida mecánica", "20 millones", "6 millones"),
        ("Carga mínima", "10 V / 5 mA", "17 V / 5 mA (aux.)"), ("Norma", "IEC 61810-1", "IEC 60947-4-1")], dif=(0, 2))
    + usar(1100, ("USA RELÉ", "Señales, interfaz con PLC, pilotos y bobinas pequeñas."),
           ("USA CONTACTOR", "Motores y cargas de potencia: categoría AC-3."), RJ, VER),
    F_RE + " · hoja de datos del contactor · IEC 60947-4-1", FOTO)

sym = (AQ / "img" / "rele_r2n_simbolo.svg").read_text().replace("<svg ", "<svg style='position:absolute;left:30px;top:300px;width:500px;height:198px' ", 1)
sb = _Box(30, 300, 500, 198)
f = Img("re_f", 640, 270, h=600)
P["H18_rele_simbolo"] = page(DID,
    kick("RELÉ · SÍMBOLO IEC 60617", C3) + T("Símbolo del", "relé 2 CO", C3, sub="Numeración nueva (EN 50005) y antigua del zócalo", size=60)
    + ph(20, 285, 520, 230) + sym
    + letras(sb, [("A", (.15, .12, .27, .88), AZ), ("B", (.42, .12, .62, .88), RJ, "tr"), ("C", (.70, .12, .90, .88), VER, "tr"),
                  ("D", (.27, .44, .82, .56), TEAL, "br")])
    + f.html() + letras(f, [("A", REB["bob"], AZ), ("B", REB["con"], RJ, "tr"), ("D", REB["emp"], TEAL, "bl")])
    + leyenda(545, [("A", "Bobina A1-A2", "→ bobina de cobre", AZ), ("B", "Contacto 11-12-14", "→ contacto AgNi", RJ),
                    ("C", "Contacto 41-42-44", "→ el gemelo, detrás", VER), ("D", "Línea punteada", "→ empujador que mueve ambos", TEAL)], cols=1, x=30, w=510)
    + tabla(900, [("A · bobina", "A1 = 13 · A2 = 14"), ("B · contacto 1", "11 = 9 · 12 = 1 · 14 = 5"), ("C · contacto 2", "41 = 12 · 42 = 4 · 44 = 8")],
            cab="<span>NUEVA = ANTIGUA (pin del zócalo)</span>", extra="font-size:19px")
    + nota(1150, "<b>11/41</b> = común · <b>12/42</b> = NC · <b>14/44</b> = NA. No es el relé octal de 8 pines (bobina 2-7): sus bornes son distintos."),
    "IEC 60617 · EN 50005 (numeración de bornes) · " + F_RE, FOTO + " · símbolo armado con la librería IEC @miguelesquit")

# ===================================================================== SENSOR INDUCTIVO M12 (4 mm, PNP NA, conector M12)
C4 = TEAL
F_SE = "hoja de datos del fabricante · IEC 60947-5-2"
SEB = {"cara": (.88, .31, .94, .69), "ros": (.66, .29, .88, .70), "tue": (.49, .17, .68, .83), "led": (.24, .34, .31, .68),
       "con": (.08, .30, .19, .70), "cuer": (.19, .29, .49, .70)}
f = Img("se_f", 40, 380, w=1000)
P["H19_sensor_partes"] = page(DID,
    kick("SENSOR INDUCTIVO · PARTES", C4) + T("Las partes del", "sensor inductivo", C4, sub="M12 · 4 mm · PNP normalmente abierto · conector M12", size=58)
    + f.html() + cajas(f, [
        (1, SEB["con"], "Conector M12", "3 contactos dorados", 20, 340),
        (2, SEB["led"], "4 LED amarillos", "estado de la salida", 310, 340),
        (3, SEB["tue"], "2 tuercas", "fijan y ajustan la distancia", 620, 340),
        (4, SEB["cuer"], "Cuerpo de latón", "recubierto, rosca M12 × 1", 120, 1000),
        (5, SEB["ros"], "Rosca M12 × 1", "enrasable en metal", 470, 1000),
        (6, SEB["cara"], "Cara activa", "plástico PBT: sale el campo", 780, 900)], wl=270)
    + chips(1075, [("4 mm", "Distancia nominal Sn (acero).", C4), ("700 Hz", "Frecuencia de conmutación máx.", AZ),
                   ("10–30 VDC", "Consumo &lt; 10 mA · salida 100 mA.", NAR), ("IP67", "Polvo y agua.", VER)], cols=4)
    + nota(1195, "No necesita tocar la pieza: detecta <b>metal</b> por campo magnético; no se desgasta."),
    F_SE, FOTO)

blocks = [("OSCILADOR", "LC a alta frecuencia", AZ), ("BOBINA", "ferrita abierta: campo en la cara", TEAL),
          ("METAL", "corrientes de Foucault roban energía", NAR), ("COMPARADOR", "umbral con histéresis", MOR), ("SALIDA PNP", "conecta la salida a +V", RJ)]


def _amp():
    x, y, w, h = 560, 650, 460, 290
    s = [f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='#F6FAFF' rx='6'/>"]
    p_ = []
    for i in range(61):
        d = 8 * i / 60
        a = 1 - math.exp(-.6 * d)
        p_.append(f"{x + d / 8 * w:.0f},{y + h - 20 - a * (h - 50):.0f}")
    s.append(f"<polyline points='{' '.join(p_)}' fill='none' stroke='{AZ}' stroke-width='4'/>")
    a4 = 1 - math.exp(-.6 * 4)
    yu = y + h - 20 - a4 * (h - 50)
    xs = x + 4 / 8 * w
    s.append(f"<line x1='{x}' y1='{yu:.0f}' x2='{x + w}' y2='{yu:.0f}' stroke='{RJ}' stroke-width='2.5' stroke-dasharray='8 6'/>")
    s.append(f"<line x1='{xs:.0f}' y1='{y}' x2='{xs:.0f}' y2='{y + h}' stroke='{NAV}' stroke-width='2'/>")
    s.append(tx(xs, y + h + 18, "Sn = 4 mm", 16, 800, NAV) + tx(x, y + h + 18, "0", 15, 700, "#475467") + tx(x + w, y + h + 18, "8 mm", 15, 700, "#475467"))
    s.append(tx(x + w - 8, yu - 14, "umbral", 15, 800, RJ, "end"))
    s.append(f"<rect x='{x}' y='{y}' width='{xs - x:.0f}' height='{h}' fill='{hexa(RJ, .10)}'/>")
    s.append(tx(x + (xs - x) / 2, y + 26, "DETECTA", 17, 900, RJ) + tx(xs + 40, y + 26, "no detecta", 15, 700, "#475467", "start"))
    s.append(tx(x + w / 2, y + h + 44, "distancia del metal a la cara (forma ilustrativa)", 15, 800, NAV))
    return "".join(s)


f = Img("se_f", 20, 680, w=500)
P["H20_sensor_funcionamiento"] = page(DID,
    kick("SENSOR INDUCTIVO · CÓMO FUNCIONA", C4) + T("Así detecta el", "metal", C4, sub="Un oscilador que se «frena» cuando llega una pieza metálica", size=62)
    + "".join(blk(20 + i * 210, 290, 196, t, d, c, h=150) for i, (t, d, c) in enumerate(blocks))
    + svg(0, 0, 1080, 1350, "".join(flecha(216 + i * 210, 365, 230 + i * 210, 365, NAV, 4) for i in range(4)))
    + "<div style='position:absolute;left:40px;right:40px;top:465px;font:500 19px/1.4 Montserrat;color:#1d2939;background:#F6FAFF;border-radius:16px;padding:14px 20px'>"
      "Sin metal, el oscilador trabaja a <b>amplitud máxima</b>. Al acercarse el metal, las corrientes de Foucault le quitan energía y la amplitud cae; "
      "al pasar el <b>umbral</b>, el comparador activa la salida PNP y encienden los LED. La histéresis (3–15 % de Sr) evita parpadeos.</div>"
    + f.html() + marcas(f, [(1, SEB["cara"]), (2, SEB["led"])])
    + "<div style='position:absolute;left:40px;top:970px;width:480px;font:600 16px/1.35 Montserrat;color:#475467'>1 = cara activa (aquí sale el campo) · 2 = LED de estado</div>"
    + svg(0, 0, 1080, 1350, _amp())
    + tabla(1060, [("Metal presente", "salida ≈ +V − 2,5 V · LED ON"), ("Sin metal", "salida abierta · LED OFF")], extra="font-size:20px"),
    F_SE + " · guía técnica de sensores de proximidad", FOTO)

P["H21_sensor_criterios"] = page(DID,
    kick("SENSOR INDUCTIVO · SELECCIÓN", C4) + T("Cómo escoger el", "sensor inductivo", C4, sub="El metal cambia la distancia: aplica el factor de corrección", size=56)
    + "<div style='position:absolute;left:40px;right:40px;top:290px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px'>"
    + "".join(f"<div style='border-radius:16px;background:{c};color:#fff;text-align:center;padding:12px 6px'>"
              f"<div style='font:900 48px/1 \"Barlow C\"'>{v}</div><div style='font:800 17px Montserrat;margin-top:4px'>{m}</div>"
              f"<div style='font:600 15px Montserrat;opacity:.9'>{d}</div></div>" for v, m, d, c in (
                  ("× 1", "Acero", "4,0 mm", NAV), ("× 0,7", "Inoxidable", "2,8 mm", AZ), ("× 0,5", "Latón", "2,0 mm", NAR),
                  ("× 0,4", "Aluminio", "1,6 mm", TEAL), ("× 0,3", "Cobre", "1,2 mm", RJ)))
    + "</div>"
    + crit(450, [("Distancia de trabajo", "Instálalo entre 0 y 3,24 mm de una pieza de acero para que detecte siempre.", "0–3,24 mm", TEAL),
                 ("Montaje", "Enrasable: puede ir embutido en metal sin detectarlo.", "enrasable", AZ),
                 ("PNP o NPN", "PNP entrega +V en la salida → entrada de PLC tipo sumidero (común a 0 V).", "PNP", RJ),
                 ("Alimentación y carga", "10–30 VDC; salida máx. 100 mA; caída máx. 2,5 V.", "100 mA", NAR),
                 ("Velocidad", "Frecuencia de conmutación máx. 700 Hz.", "700 Hz", VER),
                 ("Conexión", "Conector M12 código A: cambias el sensor sin recablear.", "M12", MOR)])
    + nota(1160, "Un sensor <b>PNP en una entrada para NPN</b> no funciona: revisa el común del PLC antes de comprar."),
    F_SE + " (factores de corrección del fabricante)", "tabla propia con datos del fabricante")


def _engr():
    cx, cy, R, r = 770, 520, 140, 110
    s, pp = [], []
    n = 12
    for i in range(n * 4):
        a = 2 * math.pi * i / (n * 4)
        rr = R if (i % 4) in (1, 2) else r
        pp.append(f"{cx + rr * math.cos(a):.0f},{cy + rr * math.sin(a):.0f}")
    s.append(f"<polygon points='{' '.join(pp)}' fill='#98A2B3'/><circle cx='{cx}' cy='{cy}' r='34' fill='#fff'/>")
    s.append(tx(cx, cy + R + 28, "engranaje de 12 dientes", 16, 800, NAV))
    s.append(flecha(560, 520, 625, 520, TEAL, 5))
    return "".join(s)


fs = Img("se_f", 50, 420, w=470)
P["H22_sensor_aplicacion"] = page(DID,
    kick("SENSOR INDUCTIVO · CASO REAL", C4) + T("Vigilar la velocidad de", "un eje", C4, sub="El sensor cuenta dientes y el PLC calcula las rpm", size=56)
    + ph(40, 280, 490, 430) + fs.html(False)
    + "<div style='position:absolute;left:60px;top:305px;width:450px;font:800 20px/1.3 Montserrat;color:#0B1F4D'>Cara activa a ≤ 3,24 mm del diente<br><span style='font-weight:600;color:#475467'>(distancia segura para acero)</span></div>"
    + svg(0, 0, 1080, 1350, _engr())
    + "<div style='position:absolute;left:40px;right:40px;top:740px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px'>"
    + "".join(f"<div style='border-radius:14px;padding:10px 14px;background:{bg};color:#fff;font:600 17px/1.3 Montserrat'>"
              f"<b style='display:block;font:900 32px/1 \"Barlow C\"'>{t}</b>{d}</div>" for t, d, bg in (
                  ("PIN 1 BN → L+", "24 VDC de la fuente", "#7B4A2A"), ("PIN 3 BU → M", "0 V de la fuente", "#1D4ED8"), ("PIN 4 BK → I0.0", "entrada del PLC (sumidero)", "#111")))
    + "</div>"
    + "<div style='position:absolute;left:40px;right:40px;top:880px;border-radius:18px;background:#F6FAFF;padding:16px 22px;font:500 21px/1.4 Montserrat;color:#1d2939'>"
      "<b style='font:900 34px \"Barlow C\";color:#0FA3A3'>f = dientes × rpm ÷ 60</b><br>"
      "A 3000 rpm con 12 dientes: 12 × 3000 ÷ 60 = <b>600 pulsos por segundo</b> → menor que 700 Hz ✓. "
      "Si la frecuencia cae (correa rota o eje trabado), el PLC detiene el motor y da alarma.</div>"
    + nota(1150, "La entrada del PLC también debe ser rápida: una entrada normal filtra pulsos; para 600 Hz usa un <b>contador rápido</b>."),
    F_SE + " · IEC 60947-5-2 (colores y pines M12)", FOTO)

fa = Img("se_f", 60, 390, w=430)
fb = Img("se_c", 640, 290, h=340)
P["H23_inductivo_vs_capacitivo"] = page(DID,
    kick("COMPARACIÓN · SENSORES", C4) + T("Inductivo contra", "capacitivo", C4, sub="Los dos detectan sin tocar, pero no ven lo mismo", size=60)
    + duelo(fa, fb, "INDUCTIVO", "CAPACITIVO", TEAL, MOR)
    + versus(740, "Inductivo", "Capacitivo", [
        ("Detecta", "solo metales", "líquidos, granos, plástico, metal"), ("Distancia", "4 mm (M12)", "20 mm (M30)"),
        ("Frecuencia", "700 Hz", "10 Hz"), ("Ajuste", "no requiere", "botón o IO-Link"),
        ("Salida", "PNP NA · 100 mA", "PNP NA/NC · 200 mA"), ("Protección", "IP67", "IP65 / IP67")], dif=(0, 2))
    + usar(1100, ("USA INDUCTIVO", "Piezas metálicas, posición de cilindros, dientes y levas."),
           ("USA CAPACITIVO", "Nivel de tolvas y tanques, a veces a través de la pared."), TEAL, MOR),
    F_SE + " · hojas de datos de ambos sensores", FOTO)

s = Img("14_sensor_inductivo_simbolo", 40, 300, w=470)
f = Img("se_f", 545, 330, w=500)
P["H24_sensor_simbolo"] = page(DID,
    kick("SENSOR INDUCTIVO · SÍMBOLO IEC 60617", C4) + T("Símbolo del", "sensor inductivo", C4, sub="Detector de proximidad de 3 hilos con salida NA", size=58)
    + ph(30, 280, 490, 380) + s.html(False)
    + letras(s, [("A", (.28, .25, .58, .68), AZ), ("B", (.40, .03, .62, .25), "#7B4A2A", "tr"), ("C", (.40, .68, .62, .96), "#1D4ED8", "br"),
                 ("D", (.58, .30, .80, .96), "#111", "tr")])
    + f.html() + letras(f, [("A", SEB["cara"], AZ, "tr"), ("E", SEB["cuer"], TEAL, "tl"), ("F", SEB["con"], "#111", "bl")])
    + "<div style='position:absolute;left:560px;top:640px;width:480px;display:grid;gap:8px'>"
    + "".join(f"<div style='display:flex;align-items:center;gap:12px;border-radius:12px;background:#F6FAFF;padding:8px 12px;font:600 18px Montserrat;color:#1d2939'>"
              f"<span style='width:30px;height:30px;border-radius:50%;background:{c}'></span><b style='width:70px'>Pin {p}</b>{t}</div>" for p, c, t in (
                  ("1", "#7B4A2A", "café BN → + (B)"), ("3", "#1D4ED8", "azul BU → − (C)"), ("4", "#111", "negro BK → salida (D)")))
    + "</div>"
    + leyenda(700, [("A", "Rombo + cuadro lleno", "= detector inductivo → cara activa", AZ), ("B", "BN +", "→ pin 1, café", "#7B4A2A"),
                    ("C", "BU −", "→ pin 3, azul", "#1D4ED8"), ("D", "BK salida NA", "→ pin 4, negro", "#111"),
                    ("E", "Recuadro", "= el cuerpo del sensor", TEAL), ("F", "Conector M12", "→ por donde salen B-C-D", "#111")], cols=1, x=30, w=490)
    + nota(1150, "Los colores y pines los fija la <b>IEC 60947-5-2</b> para todas las marcas: el cable M12 de 3 hilos se conecta igual."),
    "IEC 60617 · IEC 60947-5-2 · IEC 81346 (-B) · " + F_SE, FOTO + " · símbolo: catálogo @miguelesquit")

# ===================================================================== CONTACTOR 50 A, bobina 220 VAC
C5 = VER
F_KM = "hoja de datos del fabricante · marcado del equipo · IEC 60947-4-1"
KMB = {"bob1": (.66, .36, .75, .43), "bob2": (.66, .66, .75, .73), "aux1": (.52, .36, .66, .43), "aux2": (.52, .66, .66, .73),
       "ent": (.38, .13, .73, .21), "sal": (.38, .84, .73, .91), "fre": (.44, .46, .79, .65), "num": (.44, .28, .74, .33)}
f = Img("km_f", 190, 265, w=700)
P["H25_contactor_partes"] = page(DID,
    kick("CONTACTOR · PARTES", C5) + T("Las partes del", "contactor", C5, sub="50 A AC-3 · bobina 220 VAC · 1NA + 1NC", size=62)
    + f.html() + cajas(f, [
        (1, KMB["ent"], "Entrada 1/L1 3/L2 5/L3", "tornillo hexagonal 4 mm", 20, 330),
        (2, KMB["aux1"], "Auxiliares arriba", "13 NA · 21 NC", 20, 520),
        (3, KMB["aux2"], "Auxiliares abajo", "14 NA · 22 NC", 20, 720),
        (4, KMB["sal"], "Salida 2/T1 4/T2 6/T3", "al relé térmico / motor", 20, 900),
        (5, KMB["bob1"], "Bobina A1", "arriba a la derecha", 800, 430),
        (6, KMB["fre"], "Frente", "tapa de identificación", 800, 580),
        (7, KMB["bob2"], "Bobina A2", "abajo a la derecha", 800, 740)], wl=260)
    + chips(1015, [("50 A AC-3", "Motores: 15 kW a 230 V · 22 kW a 400 V.", C5), ("80 A AC-1", "Cargas resistivas (Ith).", AZ),
                   ("1NA + 1NC", "Autoenclavamiento y enclavamiento.", NAR)])
    + nota(1150, "Arriba entra la red, abajo sale al motor; la <b>bobina</b> tiene A1 arriba y A2 abajo, y los auxiliares van junto a ella."),
    F_KM, FOTO)

f = Img("km_f", 0, 265, w=540)
P["H26_contactor_funcionamiento"] = page(DID,
    kick("CONTACTOR · CÓMO FUNCIONA", C5) + T("Así cierra un", "contactor", C5, sub="Un electroimán que mueve todos los contactos a la vez", size=62)
    + f.html() + marcas(f, [(1, KMB["bob1"]), (3, KMB["ent"]), (4, KMB["aux1"])])
    + pasos(540, 270, 500, [(1, "Bobina A1-A2:", "con 220 VAC el núcleo en E se magnetiza."),
                            (2, "Armadura:", "es atraída y arrastra el portacontactos (12–26 ms)."),
                            (3, "Polos 1-2, 3-4, 5-6:", "cierran y el motor recibe tensión."),
                            (4, "Auxiliares:", "13-14 cierra y 21-22 abre junto con los polos."),
                            (5, "Sin tensión:", "un resorte regresa todo a reposo (4–19 ms).")])
    + tabla(830, [("Cierra a 60 Hz (0,85–1,1 Uc)", "187 – 242 V"), ("Abre (0,3–0,6 Uc)", "66 – 132 V"),
                  ("Al cerrar / mantenido (60 Hz)", "140 VA / 13 VA")], cab="<span>BOBINA 220 VAC</span>", extra="font-size:20px")
    + nota(1070, "Al cerrar, la bobina pide <b>10 veces</b> más potencia que al mantenerse: dimensiona el transformador de mando con ese pico. A 120 V no cierra."),
    F_KM, FOTO)

f = Img("km_f", 30, 285, w=510)
P["H27_contactor_criterios"] = page(DID,
    kick("CONTACTOR · SELECCIÓN", C5) + T("Cómo escoger el", "contactor", C5, sub="Lo que trae marcado el frente y lo que dice su hoja", size=60)
    + ph(20, 280, 520, 530) + f.html(False)
    + letras(f, [("A", (.42, .28, .74, .33), AZ, "tr"), ("B", (.52, .36, .75, .43), RJ, "tr"), ("C", (.52, .66, .75, .73), VER, "br"),
                 ("D", (.38, .84, .73, .91), NAR, "bl")])
    + leyenda(830, [("A", "1/L1 3/L2 5/L3", "polos de potencia", AZ), ("B", "13 NO · 21 NC · A1", "auxiliares y bobina", RJ),
                    ("C", "14 NO · 22 NC · A2", "auxiliares y bobina", VER), ("D", "2/T1 4/T2 6/T3", "salida al motor", NAR)], cols=2, x=30, w=510)
    + crit(285, [("Categoría AC-3", "Motor jaula: corriente del motor ≤ corriente AC-3.", "50 A", C5),
                 ("Potencia a tu tensión", "15 hp a 200/208 V y 230/240 V (trifásico).", "15 hp", AZ),
                 ("Tensión de bobina", "220 VAC: a 60 Hz cierra de 187 a 242 V. A 120 V no sirve.", "220 V", RJ),
                 ("Auxiliares", "13-14 autoenclavamiento · 21-22 enclavamiento.", "1NA+1NC", NAR),
                 ("Cargas resistivas", "Hornos y resistencias: AC-1 hasta 80 A.", "80 A", NAV),
                 ("Cable y apriete", "Potencia 1–25 mm² con 5 N·m; mando 1,7 N·m.", "5 N·m", MOR)], x=560, w=480)
    + nota(1080, "No escojas solo por los amperios del <b>modelo</b>: compara con la corriente del motor en <b>AC-3</b> a la tensión de tu red."),
    F_KM, FOTO)

fk = Img("km_f", 300, 400, h=320)
P["H28_contactor_aplicacion"] = page(DID,
    kick("CONTACTOR · CASO REAL", C5) + T("Motor de 15 hp a", "208 V", C5, sub="Arranque directo con autoenclavamiento", size=60)
    + blk(320, 280, 270, "PROTECCIÓN", "breaker o fusibles (NEC 430.52)", NAV)
    + fk.html()
    + "<div style='position:absolute;left:180px;top:540px;font:900 34px \"Barlow C\";color:#22A559'>-KM1</div>"
    + blk(320, 760, 270, "RELÉ TÉRMICO", "ajustado a la placa del motor", NAV)
    + blk(320, 900, 270, "MOTOR 15 hp", "208 V · 3~", C5)
    + svg(0, 0, 1080, 1350, flecha(455, 365, 455, 400) + flecha(455, 722, 455, 760) + flecha(455, 845, 455, 900))
    + tarjetas(640, 280, 400, [
        ("46,2 A", "Corriente de tabla NEC 430.250, 15 hp a 208 V → menor que 50 A AC-3 ✓.", C5),
        ("6 AWG", "Conductor al 125 %: 57,8 A → 6 AWG THHN (65 A a 75 °C).", AZ),
        ("BOBINA ENTRE FASES", "220 V entre L1 y L2: 208 V está dentro de 187–242 V.", RJ),
        ("13-14", "En paralelo con el pulsador de marcha: autoenclavamiento.", NAR),
        ("100 A gG", "Fusible máximo asociado para coordinación tipo 2.", MOR)])
    + nota(1060, "El contactor <b>maniobra</b>; no protege. La sobrecarga la cuida el relé térmico y el cortocircuito el breaker o los fusibles."),
    F_KM + " · NEC 2020 T430.250, 430.22, T310.16", FOTO)

s = Img("05_contactor_simbolo", 30, 310, w=500)
f = Img("km_f", 530, 270, w=540)
P["H30_contactor_simbolo"] = page(DID,
    kick("CONTACTOR · SÍMBOLO IEC 60617", C5) + T("Símbolo del", "contactor", C5, sub="Polos, auxiliares y bobina: cada uno en su lugar del equipo", size=60)
    + ph(20, 280, 520, 380) + s.html(False)
    + letras(s, [("A", (.14, .02, .30, .49), AZ), ("B", (.33, .02, .47, .49), RJ, "tr"), ("C", (.54, .02, .82, .49), NAR, "tr"),
                 ("D", (.28, .50, .50, .98), VER, "bl")])
    + f.html() + letras(f, [("A", KMB["ent"], AZ), ("B", KMB["sal"], RJ, "bl"), ("C", KMB["aux1"], NAR, "tl"), ("C", KMB["aux2"], NAR, "bl"),
                            ("D", KMB["bob1"], VER, "tr"), ("D", KMB["bob2"], VER, "br")])
    + leyenda(700, [("A", "Polos 1-3-5", "→ bornes de entrada", AZ), ("B", "Polos 2-4-6", "→ bornes de salida", RJ),
                    ("C", "13-14 NA · 21-22 NC", "→ 13 y 21 arriba, 14 y 22 abajo", NAR),
                    ("D", "Bobina A1-A2", "→ A1 arriba, A2 abajo", VER)], cols=1, x=30, w=490)
    + nota(1150, "El <b>semicírculo</b> en el contacto marca la función de contactor; la línea punteada une todo lo que mueve la bobina."),
    "IEC 60617 · IEC 81346 (-KM) · " + F_KM, FOTO + " · símbolo: catálogo @miguelesquit")

if __name__ == "__main__":
    sel = sys.argv[1:] or list(P)
    for k in sel:
        (AQ / "html" / f"{k}.html").write_text(P[k], encoding="utf-8")
    subprocess.run(["node", "shot.js", *sel], cwd=AQ, check=True)
    print("ok", len(sel))

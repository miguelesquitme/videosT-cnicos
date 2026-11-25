"""Lote E (25-nov): serie de 6 infografías de UN dispositivo: relé térmico CHINT NR2-25 (9–13 A), el de
larssystemgt.com/1347. Estructura pedida por el usuario: partes · funcionamiento · selección · aplicación · versus ·
símbolo. Ilustración del catálogo (lib/svgref.rele_termico, rango 9–13) y corte de lib/svgarr.rele_corte.
Fuentes en referencias/loteE_fuentes.md."""
import importlib.util
import subprocess
from pathlib import Path
from PIL import Image

AQ = Path(__file__).parent


def _load(n, p):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


g = _load("g10", AQ.parent / "posts10" / "gen.py")
page, rot, kick, T, svg, tabla, L = g.page, g.rot, g.kick, g.T, g.svg, g.tabla, g.L
DID, BIG, OSC = g.DID, g.BIG, g.OSC
NAV, AZ, TEAL, NAR, RJ, VER, AM = g.NAV, g.AZ, g.TEAL, g.NAR, g.RJ, g.VER, g.AM
ILU = "ilustración @miguelesquit basada en el CHINT NR2-25 (larssystemgt.com/1347)"
F_NR2 = "CHINT, NR2 Thermal Overload Relay (PDF, mantech/lemona) · CHINT, NR2 User Instruction 2020.04 · chintglobal.com, NR2 · larssystemgt.com/1347"


class Img(g.Img):
    def __init__(self, src, x, y, w=None, h=None):
        path = AQ / "img" / f"{src}.png"
        W, H = Image.open(path).size
        if w and not h:
            h = w * H / W
        if h and not w:
            w = h * W / H
        self.foto, self.src = False, f"../img/{src}.png"
        self.x, self.y, self.w, self.h = x, y, w, h


KICK = "RELÉ TÉRMICO · CHINT NR2-25"
P = {}

# ===================================================================== E01 · Partes (numerado a los dos lados)
def lados(f, items, wl=250):
    """items: (n, fx, fy, título, sub, lado 'i'|'d', y de la etiqueta). Línea punteada número → pieza."""
    sv, out = [], []
    for n, fa, fb, t, sub, lado, y in items:
        px, py = f.p(fa, fb)
        x0 = 40 if lado == "i" else 1040 - wl
        xe = x0 + wl + 8 if lado == "i" else x0 - 8
        sv.append(f"<polyline points='{xe},{y} {px:.0f},{py:.0f}' fill='none' stroke='#fff' stroke-width='7' opacity='.9'/>"
                  f"<polyline points='{xe},{y} {px:.0f},{py:.0f}' fill='none' stroke='#0057FF' stroke-width='3' stroke-dasharray='9 7'/>"
                  f"<circle cx='{px:.0f}' cy='{py:.0f}' r='9' fill='#0057FF' stroke='#fff' stroke-width='3'/>")
        al = "" if lado == "i" else "flex-direction:row-reverse;text-align:right;"
        out.append(f"<div style='position:absolute;left:{x0}px;top:{y - 30}px;width:{wl}px;display:flex;gap:10px;align-items:center;{al}'>"
                   f"<div style='flex:none;width:46px;height:46px;border-radius:50%;background:#0057FF;color:#fff;font:800 22px Montserrat;"
                   f"display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.3)'>{n}</div>"
                   f"<div><div style='font:800 21px/1.1 Montserrat;color:#0B1F4D'>{t}</div><div style='font:500 16px/1.2 Montserrat;color:#475467'>{sub}</div></div></div>")
    return svg(0, 0, 1080, 1350, "".join(sv)) + "".join(out)


f = Img("nr2", 300, 370, w=480)
P["E01_partes"] = page(DID,
    kick(KICK, NAR) + T("Las partes del", "relé térmico", NAR, sub="CHINT NR2-25 · rango 9–13 A · clase 10A", size=66)
    + f.html() + lados(f, [
        (1, .21, .02, "Pines de entrada", "1/L1 · 3/L2 · 5/L3", "i", 382),
        (2, .29, .29, "Dial de ajuste", "a la corriente de placa", "i", 500),
        (3, .12, .43, "Botón TEST", "simula un disparo", "i", 600),
        (4, .47, .43, "Indicador", "se ve al disparar", "i", 700),
        (5, .265, .63, "Auxiliar NA 97-98", "piloto de falla", "i", 790),
        (6, .21, .84, "Salida al motor", "2/T1 · 4/T2 · 6/T3", "i", 910),
        (7, .86, .40, "RESET H / A", "manual o automático", "d", 560),
        (8, .655, .44, "Botón STOP", "abre 95-96", "d", 690),
        (9, .71, .63, "Auxiliar NC 95-96", "en serie con la bobina", "d", 800)])
    + "<div class='nota' style='top:1010px'>Se <b>enchufa</b> directo bajo el contactor CHINT NC1 o NC7 (09 a 32): sus pines entran en 2/T1, 4/T2 y 6/T3 del contactor.</div>"
    + "<div class='nota' style='top:1135px;background:#FFF4E5;color:#1d2939;border:3px solid #FF8A00'>Protege al motor de <b style='color:#E5383B'>sobrecarga</b> y <b style='color:#E5383B'>falta de fase</b>; no de cortocircuito.</div>",
    F_NR2 + " · IEC 60947-4-1", ILU)

# ===================================================================== E02 · Funcionamiento (corte normal vs disparado)
a = Img("corte", 40, 350, w=490)
b = Img("corted", 550, 350, w=490)
P["E02_funcionamiento"] = page(DID,
    kick(KICK, NAR) + T("Así", "funciona", NAR, sub="Por dentro: bimetales que se doblan con el calor", size=72)
    + a.html() + b.html()
    + "<div style='position:absolute;left:40px;top:792px;width:490px;text-align:center;font:900 34px \"Barlow C\";color:#22A559'>NORMAL · 95-96 CERRADO</div>"
    + "<div style='position:absolute;left:550px;top:792px;width:490px;text-align:center;font:900 34px \"Barlow C\";color:#E5383B'>SOBRECARGA · DISPARADO</div>"
    + rot(a, [dict(t="Calefactor", s="cobre", x=150, y=318, w=170, to=(.15, .40), c=NAR)])
    + rot(b, [dict(t="Bimetal", s="se dobla", x=760, y=318, w=160, to=(.17, .70), c=RJ),
              dict(t="Regleta", s="empuja el mecanismo", x=960, y=318, w=170, h=82, to=(.55, .19), c=AZ)])
    + "<div style='position:absolute;left:40px;right:40px;top:840px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px'>"
    + "".join(f"<div style='background:{c};color:#fff;border-radius:18px;padding:12px 14px;font:500 18px/1.3 Montserrat'>"
              f"<b style='display:block;font:900 40px/1 \"Barlow C\"'>{n}</b>{t}</div>"
              for n, t, c in (("1", "La corriente del motor pasa por el <b>calefactor</b> de cada fase.", NAR),
                              ("2", "Si sube, el <b>bimetal</b> (dos metales que dilatan distinto) se curva.", RJ),
                              ("3", "La <b>regleta</b> libera el mecanismo: <b>95-96 abre</b> y <b>97-98 cierra</b>.", AZ),
                              ("4", "La bobina del contactor se queda sin mando y el <b>motor para</b>.", NAV)))
    + "</div>"
    + g.tabla(1015, [("1,05 × Ir (en frío)", "no dispara en 2 h"), ("1,5 × Ir (en caliente)", "≤ 2 min"), ("7,2 × Ir (en frío)", "2 – 10 s")],
              cab="<span>CLASE 10A · TIEMPOS DE DISPARO DEL NR2</span>", extra="font-size:20px")
    + "<div style='position:absolute;left:40px;right:40px;top:1240px;font:600 16px Montserrat;color:#475467'>No corta cortocircuitos: para eso va un fusible o breaker antes. Si falta una fase, la regleta diferencial también lo dispara.</div>",
    "IEC 60947-4-1 · CHINT, NR2 (PDF), tabla 4.1 · Schneider FAQ FA364937 (bimetal y pérdida de fase) · viox.com, Thermal overload relay explained",
    "esquema @miguelesquit (corte didáctico, no a escala)")

# ===================================================================== E03 · Criterios de selección
crit = [
    ("1", "CORRIENTE DE PLACA", "Que la corriente del motor quede <b>dentro del rango</b>: 9,6 A cabe en 9–13 A; 8,6 A no, va el de 7–10 A.", AZ),
    ("2", "CLASE DE DISPARO", "<b>10A</b> = 2 a 10 s a 7,2 × Ir: arranque normal. Arranques largos (molinos, ventiladores grandes) piden clase 20 o 30.", RJ),
    ("3", "CONTACTOR", "El NR2-25 se enchufa en el <b>NC1 o NC7 de 09 a 32</b>. Para montarlo aparte se usa la base <b>MB-2</b>.", NAR),
    ("4", "CORTOCIRCUITO", "El térmico no lo corta. Fusible para el rango 9–13 A: <b>aM 16 A o gG 25 A</b> (RT16).", NAV),
    ("5", "TENSIÓN Y AUXILIARES", "Ue <b>690 V</b>. 1NA + 1NC: <b>2,73 A a 220 V AC-15</b>: maneja la bobina del contactor.", TEAL),
    ("6", "REARME Y AMBIENTE", "<b>H</b> si el arranque es automático (más seguro). Trabaja de <b>−5 a +40 °C</b> con compensación.", VER),
]
P["E03_seleccion"] = page(DID,
    kick(KICK, NAR) + T("6 criterios para", "elegirlo bien", NAR, sub="Lo que revisas antes de comprar un relé térmico", size=64)
    + "<div style='position:absolute;left:40px;right:40px;top:330px;display:grid;grid-template-columns:1fr 1fr;gap:18px'>"
    + "".join(f"<div style='background:#F6FAFF;border:3px solid {c};border-radius:22px;padding:16px 20px;height:196px;box-sizing:border-box'>"
              f"<div style='display:flex;align-items:center;gap:12px;margin-bottom:10px'><div style='flex:none;width:52px;height:52px;border-radius:50%;"
              f"background:{c};color:#fff;font:900 32px \"Barlow C\";display:flex;align-items:center;justify-content:center'>{n}</div>"
              f"<div style='font:900 30px/1 \"Barlow C\";color:{c}'>{t}</div></div>"
              f"<div style='font:500 20px/1.35 Montserrat;color:#1d2939'>{d}</div></div>" for n, t, d, c in crit)
    + "</div>"
    + "<div style='position:absolute;left:40px;right:40px;top:1000px;font:800 20px Montserrat;color:#0B1F4D'>RANGOS DEL NR2-25 (A) · ESCOGE EL QUE CONTENGA TU CORRIENTE</div>"
    + "<div style='position:absolute;left:40px;right:40px;top:1034px;display:flex;gap:10px'>"
    + "".join(f"<div style='flex:1;text-align:center;border-radius:12px;padding:8px 0;font:900 30px Barlow C;"
              f"{'background:#FF8A00;color:#fff' if r == '9–13' else 'background:#EEF2F8;color:#0B1F4D'}'>{r}</div>"
              for r in ("4–6", "5,5–8", "7–10", "9–13", "12–18", "17–25"))
    + "</div>"
    + "<div class='nota' style='top:1110px'>Regla NEC 430.32(A)(1): ajuste a la <b>corriente de placa</b>; máximo <b>125 %</b> si F.S. ≥ 1,15. En IEC se ajusta a la corriente asignada del motor.</div>",
    F_NR2 + " · IEC 60947-4-1 · NEC 430.32",
    "sin foto")

# ===================================================================== E04 · Aplicación real
f = Img("nr2", 640, 150, w=380)
P["E04_aplicacion"] = page(BIG,
    kick("APLICACIÓN REAL · NR2-25", "#0B1220")
    + "<div class='big' style='font-size:250px;top:110px'>9,6 A</div>"
    + "<div class='t' style='top:360px;width:560px'>ajuste del dial para un motor de <em>3 hp a 208 V</em></div>"
    + f.html()
    + "<div class='sub2' style='top:640px'>Bomba, ventilador o banda con un motor trifásico de <b>3 hp</b> (Baldor VM3661T-9, 208-230/460 V). "
      "A 208 V su placa dice <b>9,6 A</b>: cae dentro del NR2-25 de <b>9–13 A</b>.</div>"
    + svg(0, 0, 1080, 1350, "<circle cx='%.0f' cy='%.0f' r='56' fill='none' stroke='#E3001B' stroke-width='6'/>" % f.p(.29, .29))
    + tabla(760, [("Placa del motor a 208 V (FLA)", "9,6 A"), ("Ajuste del dial", "9,6 A"),
                  ("Máximo NEC 430.32 (F.S. 1,15 → 125 %)", "12,0 A"), ("Fusible para 9–13 A (CHINT)", "aM 16 A / gG 25 A")],
            cab="<span>DATOS DEL CASO</span>", extra="border-color:#E3001B")
    + "<div class='nota' style='top:1060px'>Conexión: <b>95-96 en serie</b> con la bobina del contactor; <b>97-98</b> enciende el piloto amarillo de falla.</div>",
    "Baldor, VM3661T-9 customer information packet · NEC 430.32(A)(1) · " + F_NR2 + " · IEC 60204-1 (amarillo = anormal)",
    ILU)

# ===================================================================== E05 · Versus Schneider LRD16
filas = [("Rango de ajuste", "9 – 13 A", "9 – 13 A"), ("Clase de disparo", "10A", "10A"), ("Tensión Ue / Uimp", "690 V / 6 kV", "690 V / 6 kV"),
         ("Auxiliares", "1NA + 1NC", "1NA + 1NC"), ("AC-15 del auxiliar", "2,73 A a 220 V", "1,5 A a 240 V"),
         ("Pérdida de fase", "Sí", "Sí (130 % Ir en 2 fases)"), ("Rearme", "Manual / Automático", "Manual / Automático"),
         ("Temperatura de trabajo", "−5 a +40 °C", "−20 a +60 °C"), ("Se enchufa en", "CHINT NC1 / NC7 09–32", "Schneider LC1D12 – D38")]
f = Img("nr2", 90, 290, h=320)
P["E05_versus"] = page(DID,
    kick("COMPARACIÓN", NAV) + T("CHINT NR2-25", "vs LRD16", RJ, sub="Dos relés térmicos de 9–13 A, misma norma IEC 60947-4-1", size=64)
    + f.html()
    + "<div style='position:absolute;left:470px;top:350px;font:900 120px/1 \"Barlow C\";color:#E5383B'>VS</div>"
    + "<div style='position:absolute;left:660px;top:330px;width:380px;height:240px;border-radius:24px;background:#3DCD58;color:#fff;"
      "display:flex;flex-direction:column;justify-content:center;align-items:center;font:900 64px/1 \"Barlow C\"'>LRD16<span style='font:700 22px Montserrat;margin-top:10px'>Schneider TeSys Deca</span></div>"
    + "<div style='position:absolute;left:40px;right:40px;top:640px;border:3px solid #0B1F4D;border-radius:18px;overflow:hidden;font:600 20px Montserrat'>"
    + "<div style='display:grid;grid-template-columns:1.1fr 1fr 1fr;background:#0B1F4D;color:#fff;font:800 20px Montserrat'><div style='padding:10px 16px'>DATO</div>"
      "<div style='padding:10px 16px;background:#FF8A00'>CHINT NR2-25</div><div style='padding:10px 16px;background:#3DCD58'>SCHNEIDER LRD16</div></div>"
    + "".join(f"<div style='display:grid;grid-template-columns:1.1fr 1fr 1fr;border-top:2px solid #E4E7EC;background:{'#fff' if i % 2 else '#F6FAFF'}'>"
              f"<div style='padding:8px 16px;color:#475467'>{d}</div><div style='padding:8px 16px;font-weight:800;color:#0B1F4D'>{x}</div>"
              f"<div style='padding:8px 16px;font-weight:800;color:#0B1F4D'>{y}</div></div>" for i, (d, x, y) in enumerate(filas))
    + "</div>"
    + "<div class='nota' style='top:1110px;padding:12px 24px;font-size:21px'>Mismo rango y clase: escoge el de la <b>marca de tu contactor</b>. Si el tablero pasa de <b>40 °C</b>, el LRD aguanta hasta 60 °C.</div>",
    "CHINT, NR2 (PDF) y User Instruction · Schneider, ficha LRD16 (PDF) · se.com, LRD16 y FAQ FA28091 (H/A) · RS Components, LRD16",
    ILU + " · Schneider sin foto")

# ===================================================================== E06 · Símbolo IEC señalado en el equipo (cajas de color con letra)
s = Img("simb", 40, 250, w=1000)
f = Img("nr2", 340, 730, h=480)


def caja(im, x0, y0, x1, y1, c, letra, lado="tl"):
    (ax, ay), (bx, by) = im.p(x0, y0), im.p(x1, y1)
    bxx = ax - 16 if "l" in lado else bx - 20
    byy = ay - 16 if "t" in lado else by - 20
    return (f"<rect x='{ax:.0f}' y='{ay:.0f}' width='{bx - ax:.0f}' height='{by - ay:.0f}' rx='10' fill='{c}' fill-opacity='.10' stroke='{c}' stroke-width='4'/>"
            f"<circle cx='{bxx + 18:.0f}' cy='{byy + 18:.0f}' r='19' fill='{c}' stroke='#fff' stroke-width='3'/>"
            f"<text x='{bxx + 18:.0f}' y='{byy + 19:.0f}' font-family='Montserrat' font-weight='900' font-size='21' fill='#fff' text-anchor='middle' dominant-baseline='central'>{letra}</text>")


GR = [("A", RJ, "ENTRADA 1 · 3 · 5", "llega del contactor (1/L1, 3/L2, 5/L3)", (.165, .06, .45, .25), (.13, -.02, .87, .05)),
      ("B", "#B42318", "SALIDA 2 · 4 · 6", "va al motor (2/T1, 4/T2, 6/T3)", (.165, .60, .45, .78), (.07, .76, .93, .97)),
      ("C", NAR, "ELEMENTO TÉRMICO", "los bimetales; su corriente se ajusta en el dial", (.165, .32, .50, .50), (.15, .17, .42, .41)),
      ("D", AZ, "95-96 · NC", "cerrado; abre al disparar → corta la bobina", (.72, .08, .82, .80), (.53, .57, .88, .74)),
      ("E", VER, "97-98 · NA", "abierto; cierra al disparar → piloto de falla", (.865, .08, .945, .80), (.09, .57, .45, .74))]
P["E06_simbolo"] = page(DID,
    kick(KICK, NAR) + T("Su símbolo", "en el equipo", NAR, sub="IEC 60617: cada letra del símbolo está en el equipo real", size=66)
    + s.html(sombra=False) + f.html()
    + svg(0, 0, 1080, 1350, "".join(caja(s, *sb, c, l) + caja(f, *fb, c, l, "tr" if l == "C" else "bl" if l == "B" else "tl")
                                    for l, c, _, _, sb, fb in GR)
          + "".join(f"<rect x='{a:.0f}' y='{b:.0f}' width='{w}' height='{h}' rx='8' fill='none' stroke='#E0A800' stroke-width='4' stroke-dasharray='10 6'/>"
                    for a, b, w, h in ((*s.p(.058, .355), 70, 50), (*s.p(.518, .255), 70, 50), (*f.p(.56, .135), 150, 52))))
    + "<div style='position:absolute;left:40px;top:715px;width:280px;display:flex;flex-direction:column;gap:12px'>"
    + "".join(f"<div style='display:flex;gap:10px;align-items:flex-start;background:#F6FAFF;border-radius:12px;padding:8px 10px'>"
              f"<div style='flex:none;width:34px;height:34px;border-radius:50%;background:{c};color:#fff;font:900 19px Montserrat;display:flex;align-items:center;justify-content:center'>{l}</div>"
              f"<div><b style='display:block;font:900 23px/1 \"Barlow C\";color:{c}'>{t}</b><span style='font:500 15px/1.25 Montserrat;color:#1d2939'>{d}</span></div></div>"
              for l, c, t, d, _, _ in GR)
    + "</div>"
    + "<div style='position:absolute;left:770px;top:740px;width:270px;background:#FFF8D6;border:3px solid #E0A800;border-radius:16px;padding:12px 14px;"
      "font:500 18px/1.3 Montserrat;color:#1d2939'><b style='display:block;font:900 30px/1 \"Barlow C\";color:#B98900'>-F2</b>Designación IEC 81346: "
      "la misma en el diagrama y en la placa amarilla del equipo.</div>"
    + "<div style='position:absolute;left:770px;top:960px;width:270px;background:#F6FAFF;border:3px solid #CFE0F5;border-radius:16px;padding:12px 14px;"
      "font:500 18px/1.3 Montserrat;color:#1d2939'><b style='display:block;font:900 30px/1 \"Barlow C\";color:#0B1F4D'>LÍNEA PUNTEADA</b>"
      "une el mando térmico con sus contactos: <b>95-96 y 97-98 cambian juntos</b>.</div>",
    "IEC 60617 (símbolos) · IEC 81346-2 (-F) · IEC 60947-4-1 / EN 50005 (95-96, 97-98) · CHINT, NR2 User Instruction (marcado de bornes)",
    ILU + " · símbolo de la librería del canal")

if __name__ == "__main__":
    import sys
    sel = sys.argv[1:] or list(P)
    for k in sel:
        (AQ / "html" / f"{k}.html").write_text(P[k], encoding="utf-8")
    subprocess.run(["node", "shot.js", *sel], cwd=AQ, check=True)
    print("ok", len(sel))

"""Publicaciones v7 (25-nov): 10 piezas con los estilos que eligió el usuario:
E01 miniatura oscura · E02 partes numeradas con línea punteada al nombre · E04 dato número gigante ·
E09 ficha técnica con líneas a la pieza · v5 'por dentro' blanco con título resaltado. Solo electricidad industrial."""
import importlib.util
import subprocess
from pathlib import Path

AQ = Path(__file__).parent


def _load(n, p):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


p4 = _load("p4", AQ.parent / "posts4" / "gen.py")
p6 = _load("p6", AQ.parent / "posts6" / "gen.py")
Foto, CC, page = p4.Foto, p4.CC, p6.page
AM, ROJO, CIAN = "#FFD400", "#FF4D4D", "#2EC4FF"

# ------------------------------------------------------------------ estilos base
DARK = """body{background:radial-gradient(circle at 50% 58%,#1d3f94 0%,#0b1636 52%,#04060d 100%)!important;color:#fff}
.lab{background:#0B1220!important;color:#fff;border-width:3px!important}.lab small{color:#AFC3E8!important}
.card{border-color:#FFD400!important;box-shadow:0 0 0 4px #FFD400,0 0 60px rgba(255,212,0,.45)!important}
.h{position:absolute;left:40px;right:40px;top:96px;text-align:center;font-family:Montserrat;font-weight:900;font-size:84px;line-height:.98;letter-spacing:-2px;text-transform:uppercase}
.h em{font-style:normal;color:#FFD400;text-shadow:0 0 30px rgba(255,212,0,.55)}
.pills{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:18px;font-family:'Barlow C';font-weight:800;font-size:31px}
.pills div{padding:6px 20px;border-radius:10px}"""


def oscuro(tag, h1, h2, cuerpo, pills, top_p=1150):
    pl = "".join(f"<div style='background:{bg};color:{c}'>{t}</div>" for t, bg, c in pills)
    return (f"<div class='tag' style='left:50%;transform:translateX(-50%);top:34px;background:{AM};color:#0B1220'>{tag}</div>"
            f"<div class='h'>{h1}<br>{h2}</div>{cuerpo}<div class='pills' style='top:{top_p}px'>{pl}</div>")


NUM = """body{background:#fff!important}
.h1b{position:absolute;left:50px;top:56px;font-family:'Barlow C';font-weight:900;font-style:italic;color:#0B1F4D;text-transform:uppercase;line-height:.88}
.n{position:absolute;width:50px;height:50px;border-radius:50%;background:#0057FF;color:#fff;font:800 25px Montserrat;display:flex;align-items:center;justify-content:center;
 transform:translate(-50%,-50%);border:4px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.35);z-index:3}
.li{position:absolute;left:44px;width:430px;display:flex;gap:14px;align-items:center;z-index:2}
.li b{display:block;font:800 26px Montserrat;color:#0B1F4D;line-height:1.1}.li span{font:500 19px Montserrat;color:#475467}
svg.ov{z-index:1}"""


def numerado(t1, t2, f, items, top0=520, paso=100):
    """items: (n, fx, fy, nombre, detalle). Línea punteada del número de la lista al punto de la foto."""
    svg, out = [], []
    for i, (n, a, b, t, s) in enumerate(items):
        y = top0 + i * paso
        px, py = f.p(a, b)
        x0 = 44 + 25
        xm = 500
        svg.append(f"<polyline points='{x0 + 30},{y} {xm},{y} {px:.0f},{py:.0f}' fill='none' stroke='#0057FF' stroke-width='3' stroke-dasharray='9 7'/>"
                   f"<circle cx='{px:.0f}' cy='{py:.0f}' r='7' fill='#0057FF' stroke='#fff' stroke-width='3'/>")
        out.append(f"<div class='li' style='top:{y - 25}px'><div class='n' style='position:relative;transform:none;flex:none'>{n}</div>"
                   f"<div style='background:#fff;padding-right:10px'><b>{t}</b><span>{s}</span></div></div>")
    return (f"<div class='h1b'><div style='font-size:60px;color:#0057FF'>{t1}</div><div style='font-size:{140 if len(t2) < 11 else 112}px'>{t2}</div>"
            f"<div style='width:160px;height:12px;background:#0057FF;margin-top:14px;border-radius:6px'></div></div>"
            + f.html() + f"<svg class='ov' viewBox='0 0 1080 1350'>{''.join(svg)}</svg>" + "".join(out))


BIG = """body{background:#fff!important}
.big{position:absolute;left:40px;top:140px;font-family:'Barlow C';font-weight:900;line-height:.8;color:#E3001B;letter-spacing:-4px}
.t{position:absolute;left:50px;width:500px;font:800 38px/1.15 Montserrat;color:#0B1220}
.t em{font-style:normal;background:#E3001B;color:#fff;padding:0 8px}
.ph{position:absolute;border-radius:36px;overflow:hidden;border:8px solid #E3001B;box-shadow:0 20px 40px rgba(0,0,0,.22);background:#fff}
.ph img{width:100%;height:100%;object-fit:cover}
.tb{position:absolute;left:50px;right:50px;border-radius:18px;overflow:hidden;font:600 26px Montserrat;border:3px solid #0B1220}
.tb div{display:flex;justify-content:space-between;padding:12px 24px;border-top:2px solid #E4E7EC}.tb div:first-child{border-top:0}
.tb b{font-family:'Barlow C';font-weight:900;font-size:34px}"""

FICHA = """body{background:#0B1220!important;color:#fff}
.h{position:absolute;left:50px;right:50px;top:84px;font-family:'Archivo Black';font-size:64px;line-height:1}
.h em{font-style:normal;color:#2EC4FF}
.card{border-color:#24345A!important;background:#EEF2F8!important;box-shadow:0 0 50px rgba(46,196,255,.25)!important}
.tl{position:absolute;width:270px;background:#16213A;border:2px solid #2EC4FF;border-radius:16px;padding:14px 16px;z-index:2}
.tl b{display:block;font:900 38px 'Barlow C';color:#2EC4FF;line-height:1}.tl span{font:600 18px Montserrat;color:#C9D2E3}"""


def ficha(f, tiles):
    """tiles: (x, y, valor, texto, fx, fy) — línea de la tarjeta al punto de la foto."""
    svg, out = [], []
    for x, y, v, t, a, b in tiles:
        px, py = f.p(a, b)
        sx = x + 270 if px > x + 270 else x
        sy = y + 45
        svg.append(f"<polyline points='{sx},{sy} {px:.0f},{py:.0f}' fill='none' stroke='#2EC4FF' stroke-width='3'/>"
                   f"<circle cx='{px:.0f}' cy='{py:.0f}' r='9' fill='#2EC4FF' stroke='#0B1220' stroke-width='3'/>")
        out.append(f"<div class='tl' style='left:{x}px;top:{y}px'><b>{v}</b><span>{t}</span></div>")
    return f.html() + f"<svg class='ov' viewBox='0 0 1080 1350' style='z-index:1'>{''.join(svg)}</svg>" + "".join(out)


BLANCO = """body{background:#fff!important}
.k{position:absolute;left:0;right:0;top:36px;text-align:center;font:800 32px Montserrat;color:#0B1F4D;letter-spacing:7px}
.hh{position:absolute;left:0;right:0;top:82px;text-align:center}
.hh span{display:inline-block;font:900 96px Montserrat;letter-spacing:-3px;color:#0B1F4D;text-transform:uppercase;
 background:linear-gradient(transparent 58%,#FFD400 58%);padding:0 14px;line-height:1.05}
.chip{position:absolute;left:50%;transform:translateX(-50%) rotate(-2deg);top:200px;background:#0057FF;color:#fff;font:900 34px 'Barlow C';letter-spacing:3px;
 padding:4px 26px;border-radius:10px;box-shadow:0 6px 0 #0B1F4D}
.sub{position:absolute;left:60px;right:60px;background:#F4F7FB;border-left:8px solid #0057FF;border-radius:14px;padding:14px 24px;font:500 23px/1.32 Montserrat}
.sub b{font-weight:800}"""

P = {}

# 1 · E01 diferencial por dentro
f = Foto("n01_rcd_c", 262, 420, h=700)
P["01_dentro_diferencial"] = page(DARK, oscuro("POR DENTRO", "¿Qué hay dentro", "de un <em>diferencial</em>?",
    f.html() + p4.rotulos(f, [
        dict(t="Bornes", s="fases y neutro", x=140, y=480, w=220, to=(.12, .105), c=AM),
        dict(t="Fases y neutro", s="pasan por el toroide", x=140, y=660, w=230, to=(.18, .45), c=CIAN),
        dict(t="Relé de disparo", x=140, y=850, w=220, to=(.30, .58), c=ROJO),
        dict(t="Contactos", s="4 polos", x=140, y=1030, w=220, to=(.14, .74), c=AM),
        dict(t="Toroide", s="detecta la fuga", x=945, y=640, w=210, to=(.56, .42), c=ROJO),
        dict(t="Trenza de cobre", x=945, y=830, w=210, to=(.87, .50), c=CIAN)]),
    [("FUGA ≥ IΔn → DISPARA", ROJO, "#fff"), ("30 mA → PROTEGE PERSONAS", CIAN, "#04121f")], 1160),
    "IEC 61008-1 · IEC 60364-4-41 (411.3.3) · Schneider Electric, guía de protección diferencial", f"“RCD inside”, WagnerTh, CC BY-SA 4.0, {CC}", True)

# 2 · E01 contactor por dentro
f = Foto("n07_contactor", 40, 470, w=1000)
P["02_dentro_contactor"] = page(DARK, oscuro("POR DENTRO", "¿Qué hay dentro", "de un <em>contactor</em>?",
    f.html() + p4.rotulos(f, [
        dict(t="Núcleo fijo", s="+ resorte", x=170, y=1100, w=230, to=(.07, .70), c=AM),
        dict(t="Bobina A1-A2", x=440, y=1100, w=230, to=(.25, .62), c=ROJO),
        dict(t="Portacontactos", s="armadura móvil", x=720, y=1100, w=250, to=(.42, .62), c=CIAN),
        dict(t="Contactos fijos", x=930, y=420, w=230, to=(.63, .14), c=AM)]),
    [("BOBINA CON TENSIÓN → CIERRA", ROJO, "#fff"), ("SIN TENSIÓN → EL RESORTE ABRE", CIAN, "#04121f")], 1180),
    "IEC 60947-4-1 · Siemens, ficha 3RT1017 (12 A · 5,5 kW AC-3) · Schneider, guía TeSys D", f"“Disassembled SIEMENS 3RT1017-1AV01”, Dmitry G, CC BY-SA 3.0, {CC}", True)

# 3 · E02 partes del relé térmico
f = Foto("p04_rele_c", 530, 400, h=690)
ox, oy, sx, sy = .28, .07, .46, .81
g = lambda fx, fy: ((fx - ox) / sx, (fy - oy) / sy)
P["03_partes_rele_termico"] = page(NUM, numerado("Partes del", "Relé térmico", f, [
    (1, *g(.57, .16), "Pines de entrada", "se enchufan al contactor"), (2, *g(.43, .27), "Dial de ajuste", "7,5 a 10,5 A"),
    (3, *g(.62, .38), "Reset H / A", "manual o automático"), (4, *g(.575, .47), "Botón STOP", "abre el 95-96"),
    (5, *g(.44, .46), "Bornes de salida", "2/T1 · 4/T2 · 6/T3"), (6, *g(.52, .67), "Contacto NC 95-96", "corta la bobina")], top0=470, paso=125),
    "GE, catálogo C-2000 (relé MT03) · IEC 60947-4-1 · NEC 430.32", f"“GE MTO3N”, Dmitry G, CC BY-SA 3.0, {CC}")

# 4 · E02 partes del contactor
f = Foto("p10_iek", 505, 390, h=680)
P["04_partes_contactor"] = page(NUM, numerado("Partes del", "Contactor", f, [
    (1, .33, .27, "Entrada de potencia", "1/L1 · 3/L2 · 5/L3"), (2, .43, .17, "Auxiliar NA 13", "señal / autoenclavamiento"),
    (3, .48, .31, "Portacontactos", "se ve moverse"), (4, .60, .45, "Salida al motor", "2/T1 · 4/T2 · 6/T3"),
    (5, .79, .55, "Borne de bobina A2", "A1 al otro lado"), (6, .30, .50, "Datos impresos", "AC-3, Ue, bobina"),
    (7, .30, .78, "Clip de riel DIN", "35 mm")], top0=460, paso=110),
    "IEC 60947-4-1 · IEK, ficha KMI-11810 · IEC 60715 (riel DIN)", f"“Contactor DIN IEK”, Kae, CC BY-SA 3.0, {CC}")

# 5 · E04 7,2 × Ie
P["05_dato_clase_disparo"] = page(BIG,
    "<div class='tag' style='left:50px;top:50px;background:#0B1220;color:#fff'>DATO CLAVE · RELÉ TÉRMICO</div>"
    "<div class='big' style='font-size:290px'>7,2<span style='font-size:150px'>×Ie</span></div>"
    "<div class='t' style='top:440px'>con esa corriente se prueba la <em>clase de disparo</em></div>"
    "<div class='ph' style='left:600px;top:430px;width:430px;height:560px'><img src='../../posts3/fotos/p09_mpcb.jpg' style='object-position:50% 40%'></div>"
    "<div class='abs' style='left:50px;width:500px;top:640px;font:500 24px/1.35 Montserrat;color:#344054'>El número de la clase es el <b>tiempo máximo</b> en segundos que tarda en disparar con el motor bloqueado.</div>"
    "<div class='tb' style='top:1010px'>" + "".join(f"<div><b>CLASE {a}</b><span>{b}</span></div>" for a, b in
        [("10", "más de 4 s y hasta 10 s"), ("20", "más de 6 s y hasta 20 s"), ("30", "más de 9 s y hasta 30 s")]) + "</div>",
    "IEC 60947-4-1, tabla de clases de disparo · Schneider Electric, Trip class designation · Siemens, manual SIRIUS 3RV2", f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0, {CC}")

# 6 · E04 curva C
P["06_dato_curva_c"] = page(BIG,
    "<div class='tag' style='left:50px;top:50px;background:#0B1220;color:#fff'>DATO CLAVE · TERMOMAGNÉTICO</div>"
    "<div class='big' style='font-size:250px'>5–10<span style='font-size:130px'>×In</span></div>"
    "<div class='t' style='top:400px'>dispara al instante un breaker <em>curva C</em></div>"
    "<div class='ph' style='left:620px;top:390px;width:410px;height:560px'><img src='../../posts3/fotos/p03_mcb.jpg' style='object-position:55% 50%'></div>"
    "<div class='abs' style='left:50px;width:520px;top:560px;font:500 24px/1.35 Montserrat;color:#344054'>Un C16 dispara “magnético” entre <b>80 y 160 A</b>. Debajo de eso actúa el bimetal, con retardo.</div>"
    "<div class='tb' style='top:990px'>" + "".join(f"<div><b>CURVA {a}</b><span>{b}</span></div>" for a, b in
        [("B", "3 a 5 × In · resistivas, cables largos"), ("C", "5 a 10 × In · uso general"), ("D", "10 a 20 × In · motores, transformadores")]) + "</div>",
    "IEC 60898-1 (tipos B, C, D) · ABB, What you need to know about MCB trip curves · Siemens, MCB primer", f"“Circuit breaker structure ON”, Kae, CC BY-SA 3.0, {CC}")

# 7 · E09 ficha guardamotor
f = Foto("p09_mpcb", 315, 230, h=780)
P["07_ficha_guardamotor"] = page(FICHA,
    "<div class='tag' style='left:50px;top:30px;background:#2EC4FF;color:#0B1220'>FICHA RÁPIDA</div><div class='h' style='font-size:58px'>Guardamotor <em>3RV2</em></div>" +
    ficha(f, [(40, 290, "13-14 · 23-24", "contactos auxiliares NA", .25, .2), (40, 540, "0,55–0,8 A", "dial de ajuste (Ir)", .17, .39),
              (40, 790, "CLASS 10", "disparo térmico", .15, .49), (770, 290, "ON · OFF", "mando giratorio", .66, .47),
              (770, 540, "I&gt; 10 A", "disparo magnético", .15, .565), (770, 790, "2/T1 4/T2 6/T3", "salida al motor", .5, .9)]) +
    "<div class='bar' style='top:1070px;background:#16213A;border:2px solid #24345A;font-size:24px'>Protege contra <b style='color:#FFD400'>sobrecarga</b> y <b style='color:#FFD400'>cortocircuito</b> en un solo aparato · Siemens 3RV2011-0HA10</div>",
    "Siemens, ficha 3RV2011-0HA10 · IEC 60947-2 · IEC 60947-4-1", f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0, {CC}", True)

# 8 · E09 ficha relé térmico
f = Foto("p04_rele_c", 331, 260, h=550)
P["08_ficha_rele_termico"] = page(FICHA,
    "<div class='tag' style='left:50px;top:30px;background:#2EC4FF;color:#0B1220'>FICHA RÁPIDA</div><div class='h' style='font-size:58px'>Relé térmico <em>MT03N</em></div>" +
    ficha(f, [(40, 290, "7,5–10,5 A", "dial de ajuste", *g(.43, .27)), (40, 540, "2/T1 4/T2 6/T3", "salida al motor", *g(.40, .46)),
              (40, 790, "95-96 NC", "abre la bobina", *g(.52, .67)), (770, 290, "Pines", "directo al contactor", *g(.57, .16)),
              (770, 540, "H / A", "reset manual o automático", *g(.62, .38)), (770, 790, "STOP", "prueba de paro", *g(.575, .47))]) +
    "<div class='bar' style='top:1070px;background:#16213A;border:2px solid #24345A;font-size:24px'>Solo <b style='color:#FFD400'>sobrecarga</b> y falta de fase: el cortocircuito lo cubre el breaker o los fusibles</div>",
    "GE, catálogo C-2000 (MT03) · IEC 60947-4-1 · NEC 2020 430.32", f"“GE MTO3N”, Dmitry G, CC BY-SA 3.0, {CC}", True)

# 9 · v5 blanco con título resaltado: transformador por dentro
f = Foto("n03_trafo_aceite", 300, 400, h=780)
P["09_dentro_transformador"] = page(BLANCO,
    "<div class='k'>ASÍ ES UN</div><div class='hh'><span>Transformador</span></div><div class='chip'>POR DENTRO</div>"
    "<div class='sub' style='top:272px'>En cada columna del núcleo va el devanado de <b>baja tensión adentro</b> y el de <b>alta afuera</b>; el aceite aísla y enfría.</div>" +
    f.html() + p4.rotulos(f, [
        dict(t="Aisladores de alta", x=140, y=450, w=240, to=(.36, .10), c="#0057FF"),
        dict(t="Prensas de madera", s="sujetan el yugo", x=140, y=680, w=240, to=(.12, .53), c=ROJO),
        dict(t="Núcleo laminado", x=140, y=870, w=240, to=(.21, .64), c="#0057FF"),
        dict(t="Devanado de baja", s="interior", x=140, y=1070, w=240, to=(.44, .66), c=ROJO),
        dict(t="Tanque conservador", x=940, y=450, w=240, to=(.75, .06), c=ROJO),
        dict(t="Conexiones", x=940, y=640, w=240, to=(.47, .45), c="#0057FF"),
        dict(t="Cuba con aletas", s="aceite", x=940, y=830, w=240, to=(.93, .55), c=ROJO),
        dict(t="Devanado de alta", s="en discos", x=940, y=1030, w=240, to=(.72, .74), c="#0057FF")]),
    "IEC 60076-1 · ABB, Transformer Handbook · Deutsches Museum", f"“DMM Öltransformator Schnittmodell”, Dmm2va7, CC BY 3.0, {CC}")


# 10 · E01 tipos de diferencial (iconos propios)
def onda(t):
    W, H, m = 150, 70, 35
    import math
    if t == "AC":
        d = "M0,35 " + " ".join(f"L{x},{35 - 25 * math.sin(x / 150 * 4 * math.pi):.1f}" for x in range(0, 151, 5))
    elif t == "A":
        d = "M0,60 " + " ".join(f"L{x},{60 - 45 * max(0, math.sin(x / 150 * 4 * math.pi)):.1f}" for x in range(0, 151, 3))
    elif t == "F":
        d = "M0,35 " + " ".join(f"L{x},{35 - 18 * math.sin(x / 150 * 4 * math.pi) - 9 * math.sin(x / 150 * 26 * math.pi):.1f}" for x in range(0, 151, 2))
    else:
        d = "M0,20 L150,20 M0,48 " + " ".join(f"L{x},{48 - 12 * max(0, math.sin(x / 150 * 4 * math.pi)):.1f}" for x in range(0, 151, 3))
    return f"<svg width='{W}' height='{H}' viewBox='0 0 150 70'><path d='{d}' fill='none' stroke='#FFD400' stroke-width='5' stroke-linejoin='round'/></svg>"


tipos = [("AC", "Solo fuga alterna senoidal", "cargas simples: resistencias, alumbrado"),
         ("A", "AC + continua pulsante", "electrónica monofásica, cargadores"),
         ("F", "A + mezcla de frecuencias", "variadores monofásicos, lavadoras inverter"),
         ("B", "F + continua lisa", "variadores trifásicos, cargadores de VE, FV")]
P["10_tipos_diferencial"] = page(DARK + """.row{position:absolute;left:50px;right:50px;height:190px;display:flex;align-items:center;gap:26px;background:rgba(11,18,32,.75);
 border:2px solid #2A3C66;border-radius:22px;padding:0 26px}.row .l{font:900 110px 'Barlow C';color:#FFD400;width:110px;text-align:center}
.row .ic{background:#0B1220;border-radius:14px;padding:8px}.row b{display:block;font:800 30px Montserrat}.row span{font:500 21px Montserrat;color:#AFC3E8}""",
    oscuro("DIFERENCIALES", "¿Qué tipo", "de <em>diferencial</em> usar?",
           "".join(f"<div class='row' style='top:{330 + i * 205}px'><div class='l'>{a}</div><div class='ic'>{onda(a)}</div><div><b>{b}</b><span>{c}</span></div></div>"
                   for i, (a, b, c) in enumerate(tipos)),
           [("CADA TIPO CUBRE AL ANTERIOR", AM, "#0B1220")], 1170),
    "IEC 61008-1 / 61009-1 (tipos AC y A) · IEC 62423 (tipos F y B) · Schneider Electric, guía de selección de diferenciales", "iconos propios", True)

if __name__ == "__main__":
    import sys
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    import shutil
    shutil.copytree(AQ.parent / "posts6" / "fonts", AQ / "fonts", dirs_exist_ok=True)
    ks = [k for k in P if not sys.argv[1:] or any(a in k for a in sys.argv[1:])]
    for k in ks:
        (AQ / "html" / f"{k}.html").write_text(P[k])
    (AQ / "shot.js").write_text(p4.JS)
    subprocess.run(["node", "shot.js", *ks], cwd=AQ, check=True)
    print(len(ks))

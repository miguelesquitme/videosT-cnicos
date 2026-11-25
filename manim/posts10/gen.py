"""Lote D (25-nov): 30 imágenes de COMPONENTES. Fotos reales de Commons (posts3/fotos) y las ilustraciones
del catálogo del canal (catalogo/img, recortadas en posts10/img). Títulos más vistosos (cinta inclinada).
Cada dato cruzado con PDF de fabricante/norma + páginas web: referencias/loteD_fuentes.md.
Sin símbolos IEC dibujados a mano."""
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


p4 = _load("p4", AQ.parent / "posts4" / "gen.py")
p6 = _load("p6", AQ.parent / "posts6" / "gen.py")
p7 = _load("p7", AQ.parent / "posts7" / "gen.py")
CC, page, rot = p4.CC, p6.page, p4.rotulos
NAV, AZ, TEAL, NAR, RJ, VER, AM = "#0B1F4D", "#0057FF", "#0FA3A3", "#FF8A00", "#E5383B", "#22A559", "#FFD400"
FOT = AQ.parent / "posts3" / "fotos"
CAT = "ilustración del catálogo @miguelesquit"


class Img:
    """Imagen (PNG del catálogo o foto jpg) posicionada en el lienzo; p(fx, fy) da coordenadas absolutas."""

    def __init__(self, src, x, y, w=None, h=None, foto=False):
        self.foto = foto
        path = FOT / f"{src}.jpg" if foto else AQ / "img" / f"{src}.png"
        W, H = Image.open(path).size
        if w and not h:
            h = w * H / W
        if h and not w:
            w = h * W / H
        self.src = f"../../posts3/fotos/{src}.jpg" if foto else f"../img/{src}.png"
        self.x, self.y, self.w, self.h = x, y, w, h

    def p(self, fx, fy):
        return self.x + fx * self.w, self.y + fy * self.h

    def html(self, marco=None, sombra=True):
        if marco:
            return (f"<div class='card' style='left:{self.x - 6:.0f}px;top:{self.y - 6:.0f}px;width:{self.w + 12:.0f}px;"
                    f"height:{self.h + 12:.0f}px;{marco}'><img src='{self.src}'></div>")
        sh = "filter:drop-shadow(0 14px 22px rgba(11,31,77,.22));" if sombra else ""
        return (f"<img src='{self.src}' style='position:absolute;left:{self.x:.0f}px;top:{self.y:.0f}px;"
                f"width:{self.w:.0f}px;height:{self.h:.0f}px;{sh}'>")


# ------------------------------------------------------------------ estilos
TIT = """
svg{position:absolute;overflow:visible}
.kk{position:absolute;left:50px;top:36px;font:800 22px Montserrat;letter-spacing:3px;color:#fff;padding:7px 18px;border-radius:8px}
.T{position:absolute;left:44px;right:36px;top:84px;font:900 70px/1.02 Montserrat;color:#0B1F4D;letter-spacing:-2px;text-transform:uppercase;
 text-shadow:0 3px 0 rgba(11,31,77,.10)}
.T em{font-style:normal;color:#fff;display:inline-block;padding:2px 16px 4px;transform:skew(-9deg) rotate(-1.5deg);margin:6px 4px 0 0;
 text-shadow:0 3px 0 rgba(0,0,0,.25)}
.T small{display:block;font-size:30px;letter-spacing:0;text-transform:none;color:#475467;font-weight:700;margin-top:18px;text-shadow:none}
"""
DID = TIT + """body{background:#fff!important}
.pn{position:absolute;left:40px;right:40px;border-radius:26px;border:3px solid #CFE0F5;background:#F6FAFF}
.tx{position:absolute;left:56px;right:56px;font:500 24px/1.38 Montserrat;color:#1d2939}.tx b{font-weight:800;color:#0B1F4D}
.cd{position:absolute;border-radius:20px;padding:16px 20px;color:#fff;font:500 21px/1.32 Montserrat}
.cd b{display:block;font:900 34px/1 'Barlow C';margin-bottom:6px}
.wc{position:absolute;background:#fff;border:3px solid #CFE0F5;border-radius:20px;padding:16px 20px;font:500 21px/1.32 Montserrat;color:#1d2939}
.wc b{font-weight:800;color:#0B1F4D}
.nota{position:absolute;left:40px;right:40px;border-radius:18px;background:#0B1F4D;color:#fff;font:600 23px/1.32 Montserrat;padding:16px 24px}
.nota b{color:#FFD400}
.tbl{position:absolute;left:40px;right:40px;border-radius:18px;overflow:hidden;border:3px solid #0B1F4D;font:600 22px Montserrat}
.tbl div{display:flex;align-items:center;padding:10px 20px;border-top:2px solid #E4E7EC;gap:12px}.tbl div:first-child{border-top:0}
.tbl div.h{background:#0B1F4D;color:#fff;font:800 20px Montserrat}
.tbl span{flex:1}.tbl b{font:900 30px 'Barlow C';color:#0B1F4D}
svg{position:absolute;overflow:visible}"""
OSC = TIT + p7.DARK + """
.T{color:#fff;text-align:center;text-shadow:0 4px 0 rgba(0,0,0,.35)}
.T em{color:#0B1220}
.T small{color:#C9D2E3}"""
FICHA = TIT + p7.FICHA + """
.T{color:#fff;text-shadow:0 4px 0 rgba(0,0,0,.4)}.T em{color:#0B1220}.T small{color:#AFC3E8}
.card{background:transparent!important;border:0!important;box-shadow:none!important}"""
TBL = """.tbl{position:absolute;left:40px;right:40px;border-radius:18px;overflow:hidden;border:3px solid #0B1F4D;font:600 22px Montserrat;background:#fff}
.tbl div{display:flex;align-items:center;padding:10px 20px;border-top:2px solid #E4E7EC;gap:12px}.tbl div:first-child{border-top:0}
.tbl div.h{background:#0B1F4D;color:#fff;font:800 20px Montserrat}
.tbl span{flex:1}.tbl b{font:900 30px 'Barlow C';color:#0B1F4D}"""
BIG = TIT + TBL + p7.BIG + """
.sub2{position:absolute;left:50px;right:50px;font:500 24px/1.38 Montserrat;color:#1d2939}.sub2 b{font-weight:800;color:#0B1220}
.tb div{align-items:center}.tb div span{font:500 22px Montserrat;color:#475467}
.nota{position:absolute;left:40px;right:40px;border-radius:18px;background:#0B1220;color:#fff;font:600 23px/1.32 Montserrat;padding:16px 24px}
.nota b{color:#FFD400}
svg{position:absolute;overflow:visible}"""


def kick(t, col):
    return f"<div class='kk' style='background:{col}'>{t}</div>"


def T(l1, em, col, l2="", sub="", size=70, top=84, center=False):
    al = "text-align:center;" if center else ""
    s = f"<small>{sub}</small>" if sub else ""
    return (f"<div class='T' style='font-size:{size}px;top:{top}px;{al}'>{l1} <em style='background:{col};box-shadow:7px 7px 0 "
            f"{'#0B1F4D' if col == AM else AM}'>{em}</em> {l2}{s}</div>")


def svg(x, y, w, h, body):
    return f"<svg style='left:{x}px;top:{y}px' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{body}</svg>"


def L(x1, y1, x2, y2, c=NAV, w=3, dash=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{c}' stroke-width='{w}' stroke-linecap='round'{d}/>"


def R(x, y, w, h, f="#fff", c=NAV, sw=3, r=6):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{f}' stroke='{c}' stroke-width='{sw}'/>"


def Tx(x, y, s, size=24, w=700, c=NAV, a="middle", fam="Montserrat"):
    return f"<text x='{x}' y='{y}' font-family='{fam}' font-size='{size}' font-weight='{w}' fill='{c}' text-anchor='{a}' dominant-baseline='central'>{s}</text>"


def tabla(top, filas, cab=None, extra=""):
    h = f"<div class='h'>{cab}</div>" if cab else ""
    return f"<div class='tbl' style='top:{top}px;{extra}'>{h}" + "".join(f"<div><span>{a}</span><b>{b}</b></div>" for a, b in filas) + "</div>"


def numerado(f, items, x0=44, top0=340, paso=96, xm=None, ancho=420):
    """Lista numerada a la izquierda con línea punteada a la pieza (estilo 'partes numeradas')."""
    svgs, out = [], []
    xm = xm or (x0 + ancho + 20)
    for i, (n, a, b, t, s) in enumerate(items):
        y = top0 + i * paso
        px, py = f.p(a, b)
        svgs.append(f"<polyline points='{x0 + 50},{y} {xm},{y} {px:.0f},{py:.0f}' fill='none' stroke='#0057FF' stroke-width='3' stroke-dasharray='9 7'/>"
                    f"<circle cx='{px:.0f}' cy='{py:.0f}' r='8' fill='#0057FF' stroke='#fff' stroke-width='3'/>")
        out.append(f"<div style='position:absolute;left:{x0}px;top:{y - 26}px;width:{ancho}px;display:flex;gap:12px;align-items:center;z-index:2'>"
                   f"<div style='flex:none;width:50px;height:50px;border-radius:50%;background:#0057FF;color:#fff;font:800 24px Montserrat;"
                   f"display:flex;align-items:center;justify-content:center;border:4px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.3)'>{n}</div>"
                   f"<div style='background:#fff;padding-right:8px'><div style='font:800 24px/1.1 Montserrat;color:#0B1F4D'>{t}</div>"
                   f"<div style='font:500 18px Montserrat;color:#475467'>{s}</div></div></div>")
    return f"<svg style='left:0;top:0;z-index:1' width='1080' height='1350' viewBox='0 0 1080 1350'>{''.join(svgs)}</svg>" + "".join(out)


def lineas_ficha(f, items):
    """Tarjetas de ficha técnica con línea hasta la pieza. items: (x, y, w, valor, texto, (fx, fy))."""
    s, h = [], []
    for x, y, w, v, t, to in items:
        tx, ty = f.p(*to)
        cx = x + w if tx > x + w else x
        cy = y + 40
        s.append(f"<polyline points='{cx},{cy} {tx:.0f},{cy} {tx:.0f},{ty:.0f}' fill='none' stroke='#2EC4FF' stroke-width='3'/>"
                 f"<circle cx='{tx:.0f}' cy='{ty:.0f}' r='8' fill='#2EC4FF' stroke='#0B1220' stroke-width='3'/>")
        h.append(f"<div class='tl' style='left:{x}px;top:{y}px;width:{w}px'><b>{v}</b><span>{t}</span></div>")
    return f"<svg style='left:0;top:0' width='1080' height='1350' viewBox='0 0 1080 1350'>{''.join(s)}</svg>" + "".join(h)


P = {}

# ===================================================================== D01 · Leer el breaker (ficha oscura, etiqueta ampliada)
f = Img("br1z", 40, 300, w=600)
cards = [("Ventana", "muestra si está cerrado", (.66, .32)), ("C6", "curva C · In = 6 A", (.40, .52)),
         ("Ue 230/400 VAC", "tensión de trabajo", (.585, .64)), ("IEC/EN 60898-1", "norma del breaker", (.53, .71)),
         ("Icn = 6000 A", "poder de corte: 6 kA", (.47, .78)), ("Uimp = 4 kV", "aguante a sobretensión", (.42, .845))]
ln, cd = [], []
for i, (v, t, to) in enumerate(cards):
    cy = 345 + i * 112
    tx, ty = f.p(*to)
    ln.append(f"<line x1='690' y1='{cy}' x2='{tx:.0f}' y2='{ty:.0f}' stroke='#2EC4FF' stroke-width='3'/>"
              f"<circle cx='{tx:.0f}' cy='{ty:.0f}' r='8' fill='#2EC4FF' stroke='#0B1220' stroke-width='3'/>")
    cd.append(f"<div class='tl' style='left:690px;top:{cy - 44}px;width:350px'><b>{v}</b><span>{t}</span></div>")
P["D01_leer_breaker"] = page(FICHA,
    T("Lo que dice", "tu breaker", AM, sub="Cada texto impreso tiene un significado (IEC 60898-1)", size=66, top=60)
    + f.html().replace("filter:", "border-radius:18px;filter:")
    + f"<svg style='left:0;top:0' width='1080' height='1350' viewBox='0 0 1080 1350'>{''.join(ln)}</svg>" + "".join(cd)
    + "<div class='bar' style='top:1010px;background:#16213A;border:2px solid #2EC4FF'>En un breaker real el poder de corte va en un <b>recuadro: 6000</b> (en A). No confundas C6 con 6 kA.</div>"
    + "<div class='bar' style='top:1120px;background:#16213A;border:2px solid #FFD400'>Si dice <b>IEC 60947-2</b> es un interruptor industrial: su poder de corte viene en <b>kA</b> (ej. 10 kA).</div>",
    "IEC 60898-1 · BEAMA, Markings and symbols for circuit protection (PDF) · Schneider Electric, IEC 60898-1 vs 60947-2 · viox.com, How to read an MCB nameplate",
    CAT, True)

# ===================================================================== D02 · Breaker por dentro (miniatura oscura, foto)
f = Img("p03_mcb", 150, 420, w=780, foto=True)
P["D02_breaker_dentro"] = page(OSC,
    "<div class='kk' style='background:#FFD400;color:#0B1220;left:50%;transform:translateX(-50%)'>POR DENTRO</div>"
    + T("¿Qué hay dentro<br>de un", "breaker", AM, "?", size=76, top=90, center=True)
    + f.html(marco="border-color:#FFD400") +
    rot(f, [dict(t="Palanca", s="ON / OFF", x=150, y=440, w=190, to=(.52, .17), c=AM),
            dict(t="Bobina", s="cortocircuito", x=150, y=760, w=200, to=(.52, .47), modo="d", c="#FF4D4D"),
            dict(t="Cámara de arco", s="apaga el arco", x=150, y=1050, w=230, to=(.50, .72), modo="d", c=AM),
            dict(t="Mecanismo", s="libera el disparo", x=930, y=440, w=210, to=(.60, .27), c="#2EC4FF"),
            dict(t="Bimetal", s="sobrecarga", x=930, y=760, w=200, to=(.74, .52), modo="d", c="#FF4D4D"),
            dict(t="Borne", s="tornillo", x=930, y=1050, w=190, to=(.86, .80), modo="d", c="#2EC4FF")])
    + "<div class='pills' style='top:1170px'><div style='background:#FF4D4D'>BIMETAL → SOBRECARGA</div>"
      "<div style='background:#2EC4FF;color:#04121f'>BOBINA → CORTOCIRCUITO</div></div>",
    "IEC 60898-1 · Phoenix Contact/DigiKey, What's inside a circuit breaker · viox.com, How does an MCB work · patente US 5196815 (arc chute)",
    f"“Circuit breaker structure ON”, Kae, CC BY-SA 3.0, {CC}", True)

# ===================================================================== D03 · Guardamotor partes (numerado)
f = Img("gm", 560, 300, h=900)
P["D03_guardamotor_partes"] = page(DID,
    kick("GUARDAMOTOR", AZ) + T("Las partes del", "guardamotor", AZ, size=64)
    + f.html() + numerado(f, [
        (1, .20, .09, "Entrada de línea", "1/L1 · 3/L2 · 5/L3"),
        (2, .25, .22, "Auxiliar NA", "13-14 (señal)"),
        (3, .72, .22, "Auxiliar NC", "21-22"),
        (4, .115, .36, "Clase de disparo", "CLASS 10"),
        (5, .23, .43, "Dial de ajuste", "corriente del motor"),
        (6, .47, .52, "Indicador TRIP", "disparó"),
        (7, .26, .62, "Botón TEST", "prueba el disparo"),
        (8, .65, .66, "Mando giratorio", "ON / OFF"),
        (9, .20, .92, "Salida al motor", "2/T1 · 4/T2 · 6/T3")], top0=330, paso=98, ancho=440)
    + "<div class='nota' style='top:1180px;padding:12px 24px;font-size:21px'>Térmico (sobrecarga) + magnético (cortocircuito) en un solo equipo. El dial va a la corriente de placa.</div>",
    "IEC 60947-2 · IEC 60947-4-1 · Siemens, manual SIRIUS 3RV2 · WEG, MPW · Siemens, catálogo IC 10 cap. 7",
    CAT)

# ===================================================================== D04 · Guardamotor magnético 13 × (dato gigante)
f = Img("p09_mpcb", 640, 130, h=500, foto=True)
P["D04_guardamotor_13x"] = page(BIG,
    kick("DATO CLAVE · GUARDAMOTOR", "#0B1220")
    + "<div class='big' style='font-size:280px;top:110px'>13×</div>"
    + "<div class='t' style='top:400px;width:560px'>el máximo del dial: ahí dispara el <em>magnético</em> del 3RV2</div>"
    + f"<div class='ph' style='left:{f.x - 8:.0f}px;top:{f.y - 8:.0f}px;width:{f.w + 16:.0f}px;height:{f.h + 16:.0f}px'><img src='{f.src}'></div>"
    + "<div class='sub2' style='top:660px'>En el Siemens SIRIUS 3RV2 para motores, el disparo instantáneo por cortocircuito está fijo en <b>13 veces</b> el valor máximo del dial. "
      "No se ajusta: solo se ajusta el térmico.</div>"
    + tabla(820, [("La foto: 3RV2011-0HA10 · dial 0,55–0,8 A", "10 A (impreso)"), ("3RV2011-1DA10 · dial 2,2–3,2 A", "42 A"),
                  ("3RV2021-4BA10 · dial 13–20 A", "260 A")], cab="<span>MODELO · RANGO DEL DIAL</span><span style='text-align:right'>DISPARO MAGNÉTICO</span>",
            extra="border-color:#E3001B")
    + "<div class='nota' style='top:1110px'>Siemens: el guardamotor se escoge por la <b>corriente de placa</b> del motor; los hp son solo referencia.</div>",
    "Siemens, catálogo IC 10 cap. 7 (3RV2) · Siemens, fichas 3RV2021-4BA10 y 3RV2011-1DA10 · Siemens USA, MSP chapter 1 · Mouser, SIRIUS 3RV2",
    f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0, {CC}")

# ===================================================================== D05 · Contactor: bornes
f = Img("km", 286, 290, h=820)
P["D05_contactor_bornes"] = page(DID,
    kick("CONTACTOR", RJ) + T("Así se numera", "el contactor", RJ, size=62)
    + f.html() +
    rot(f, [dict(t="Entrada de potencia", s="1/L1 · 3/L2 · 5/L3 (impares)", x=150, y=340, w=250, h=86, to=(.18, .07), c=RJ),
            dict(t="Auxiliar NA", s="13 (arriba) - 14 (abajo)", x=150, y=479, w=250, h=86, to=(.39, .23), c=VER),
            dict(t="Auxiliar NC", s="21 - 22", x=930, y=395, w=220, h=86, to=(.63, .23), c=RJ),
            dict(t="Bobina A1", s="llega el mando", x=930, y=520, w=220, h=86, to=(.86, .25), c=NAR),
            dict(t="Ventana", s="muestra si cerró", x=930, y=667, w=220, h=86, to=(.55, .46), c=AZ),
            dict(t="Bobina A2", s="regresa el mando", x=930, y=889, w=220, h=86, to=(.86, .73), c=NAR),
            dict(t="Salida al motor", s="2/T1 · 4/T2 · 6/T3 (pares)", x=150, y=1020, w=250, h=86, to=(.18, .90), c=RJ)])
    + "<div class='nota' style='top:1135px'>Potencia: <b>un dígito</b> (impar entra, par sale). Auxiliares: <b>dos dígitos</b>. Bobina: <b>A1‑A2</b>.</div>",
    "IEC 60947-4-1 · EN 50012 · ABB, catálogo contactores (marcado de bornes) · Siemens, 3RT2 auxiliares · industrialmonitordirect.com",
    CAT)

# ===================================================================== D06 · AC-1 vs AC-3 (foto ABB)
f = Img("p10_abb", 640, 130, h=500, foto=True)
P["D06_ac1_ac3"] = page(BIG,
    kick("DATO CLAVE · CONTACTOR", "#0B1220")
    + "<div class='big' style='font-size:210px;top:120px'>AC-3</div>"
    + "<div class='t' style='top:350px;width:560px'>es la categoría para <em>motores</em>: el mismo contactor aguanta menos</div>"
    + f"<div class='ph' style='left:{f.x - 8:.0f}px;top:{f.y - 8:.0f}px;width:{f.w + 16:.0f}px;height:{f.h + 16:.0f}px'><img src='{f.src}' style='transform:scale(1.6);transform-origin:50% 45%'></div>"
    + "<div class='sub2' style='top:660px'><b>AC-1</b>: cargas resistivas (resistencias, hornos). <b>AC-3</b>: motores de jaula que arrancan y se apagan andando; "
      "al cerrar soportan la corriente de arranque. Por eso el valor AC-3 es menor.</div>"
    + tabla(800, [("ABB ESB 24-40 (impreso en la foto) · AC-1", "24 A"), ("ABB ESB 24-40 · AC-3, 400 V", "4 kW"),
                  ("Schneider LC1D80 · AC-1", "125 A"), ("Schneider LC1D80 · AC-3, ≤ 440 V", "80 A")], extra="border-color:#E3001B")
    + "<div class='nota' style='top:1100px'>Para un motor se elige por <b>AC-3</b> a la tensión del motor.</div>",
    "IEC 60947-4-1 · Schneider, ficha LC1D80 (PDF) · Omron, categorías IEC 947-4-1 (PDF) · Schneider FAQ AC1/AC3 · Wikipedia, Utilization categories",
    f"“Installationsschuetz ABB ESB 24 40”, Cherubino, CC BY-SA 2.5, {CC}")

# ===================================================================== D07 · Relé térmico H / A
f = Img("ft", 300, 290, w=480)
x0, y0 = f.p(.88, .40)
P["D07_termico_reset"] = page(DID,
    kick("RELÉ TÉRMICO", NAR) + T("RESET en", "H o en A", NAR, sub="El selector azul decide cómo vuelve a arrancar", size=70)
    + f.html()
    + svg(0, 0, 1080, 1350, f"<circle cx='{x0:.0f}' cy='{y0:.0f}' r='46' fill='none' stroke='{RJ}' stroke-width='6'/>")
    + "<div class='cd' style='left:40px;top:880px;width:490px;height:200px;background:#0057FF'><b>H · MANUAL (Hand)</b>Después del disparo hay que <b style='display:inline;font:800 21px Montserrat'>presionar RESET</b> cuando el bimetal enfríe. Es una acción intencional.</div>"
    + "<div class='cd' style='left:550px;top:880px;width:490px;height:200px;background:#E5383B'><b>A · AUTOMÁTICO</b>Se rearma solo al enfriarse. Con un mando de contacto mantenido, el motor puede <b style='display:inline;font:800 21px Montserrat'>volver a arrancar sin aviso</b>.</div>"
    + "<div class='nota' style='top:1110px'>Por seguridad Schneider entrega el TeSys LRD en <b>H</b>, con el selector tapado: pasar a A exige una acción deliberada.</div>",
    "IEC 60947-4-1 · Schneider, TeSys LRD (catálogo PDF y FAQ FA28091 / FA100669) · Schneider, LR7K0310 · Siemens 3RU/3RB (Manual-Automatic-Reset)",
    CAT)

# ===================================================================== D08 · Ajuste del térmico 125 %
f = Img("ft", 640, 160, w=390)
P["D08_ajuste_termico"] = page(BIG,
    kick("DATO CLAVE · NEC 430.32", "#0B1220")
    + "<div class='big' style='font-size:250px;top:110px'>125%</div>"
    + "<div class='t' style='top:380px;width:540px'>de la corriente de placa: el <em>máximo</em> para el relé térmico</div>"
    + f.html()
    + "<div class='sub2' style='top:640px'>NEC 430.32(A)(1): el relé de sobrecarga se ajusta a la <b>corriente de placa</b>. Máximo <b>125 %</b> si el motor tiene F.S. ≥ 1,15 "
      "o elevación ≤ 40 °C; <b>115 %</b> para los demás.</div>"
    + tabla(790, [("Placa del motor (FLA)", "26,5 A"), ("F.S. 1,25 → máximo 125 %", "33,1 A"), ("Si no tuviera F.S. ni elevación ≤ 40 °C → 115 %", "30,5 A")],
            cab="<span>EJEMPLO: MOTOR DEL CANAL · 10 HP · 208 V · F.S. 1,25</span>", extra="border-color:#E3001B")
    + "<div class='nota' style='top:1080px'>No se ajusta a la corriente del contactor ni al tope del dial: <b>el dial va a la placa</b>.</div>",
    "NEC 2023, 430.32(A)(1) · EC&M, Motors and the NEC · EEPower, Sizing overload protection · CSE magazine, Motor circuit protection",
    CAT)

# ===================================================================== D09 · Relé de 8 pines
f = Img("ka", 70, 300, h=640)
fb = Img("kab", 520, 330, w=520)
P["D09_rele_8_pines"] = page(DID,
    kick("RELÉ", TEAL) + T("Los 8 pines", "del relé", TEAL, sub="Relé octal de 2 contactos conmutados (DPDT)", size=72)
    + f.html() + fb.html(sombra=False)
    + "<div style='position:absolute;left:40px;right:40px;top:980px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px'>"
      "<div class='cd' style='position:static;background:#B7791F'><b>2 – 7</b>bobina</div>"
      "<div class='cd' style='position:static;background:#22A559'><b>1-3 · 8-6</b>NA (cierran al energizar)</div>"
      "<div class='cd' style='position:static;background:#E5383B'><b>1-4 · 8-5</b>NC (abren al energizar)</div></div>"
    + "<div class='nota' style='top:1150px'>Es la convención más común (Omron, IDEC, AutomationDirect), pero <b>confirma en el costado del relé</b>: hay marcas que cambian la bobina a 1-8.</div>",
    "Omron, MK datasheet (PDF) · Omron, sockets PF083A (PDF) · control.com, relay terminal numbering · industrialmonitordirect.com, octal relays",
    CAT)

# ===================================================================== D10 · Temporizador 5 modos
f = Img("kt", 60, 300, h=760)
modos = [("A", "ON-delay: cuenta y luego cambia el contacto"), ("B", "Intermitente, inicia apagado"), ("B2", "Intermitente, inicia encendido"),
         ("E", "Intervalo: actúa solo durante el tiempo"), ("J", "Pulso único (one-shot)")]
P["D10_temporizador_modos"] = page(DID,
    kick("TEMPORIZADOR", NAR) + T("Un temporizador,", "5 modos", NAR, sub="Multifunción de 8 pines tipo Omron H3CR-A8", size=64)
    + f.html()
    + "".join(f"<div class='wc' style='left:600px;top:{320 + i * 140}px;width:440px;display:flex;gap:14px;align-items:center'>"
              f"<div style='flex:none;width:72px;height:72px;border-radius:14px;background:{NAR if k == 'A' else '#0B1F4D'};color:#fff;font:900 40px \"Barlow C\";display:flex;align-items:center;justify-content:center'>{k}</div>"
              f"<div>{t}</div></div>" for i, (k, t) in enumerate(modos))
    + "<div class='nota' style='top:1100px'>El de 8 pines arranca al <b>energizarlo</b> (modo A = retardo a la conexión). Contactos de salida: <b>5 A a 250 VAC</b> resistivo.</div>",
    "Omron, ficha H3CR-A (PDF, EN y JP) · Omron, guía técnica de timers (PDF) · ia.omron.com, especificaciones H3CR · farnell.com (H3CR-A)",
    CAT)

# ===================================================================== D11 · Colores de pulsadores
fs1 = Img("s1", 200, 330, h=430)
fs0 = Img("s0", 600, 330, h=430)
P["D11_pulsador_colores"] = page(DID,
    kick("PULSADORES · IEC 60204-1", VER) + T("¿Marcha verde,", "paro rojo?", VER, sub="La norma prefiere blanco para marcha y negro para paro", size=66)
    + fs1.html() + fs0.html()
    + "<div class='wc' style='left:40px;top:790px;width:490px'><b style='font:900 32px \"Barlow C\";display:block'>MARCHA / ON</b>Blanco (preferido), gris, negro o verde. <b style='color:#E5383B'>Rojo: nunca.</b></div>"
    + "<div class='wc' style='left:550px;top:790px;width:490px'><b style='font:900 32px \"Barlow C\";display:block'>PARO / OFF</b>Negro (preferido), gris o blanco. Rojo permitido lejos del paro de emergencia. <b style='color:#E5383B'>Verde: nunca.</b></div>"
    + "<div style='position:absolute;left:40px;right:40px;top:1010px;display:flex;gap:14px'>"
      "<div class='cd' style='position:static;flex:1;background:#1446C8'><b>AZUL</b>rearme (reset)</div>"
      "<div class='cd' style='position:static;flex:1;background:#F2C500;color:#0B1F4D'><b>AMARILLO</b>condición anormal</div>"
      "<div class='cd' style='position:static;flex:1;background:#E5383B'><b>ROJO + FONDO AMARILLO</b>solo emergencia</div></div>"
    + "<div class='nota' style='top:1175px;padding:12px 24px'>El verde (I) y el rojo (O) que usamos <b>sí cumplen</b>: son colores permitidos.</div>",
    "IEC 60204-1:2021, 10.2.1 · Schneider Electric, FAQ FA28043 y FAQ000283554 · Schneider, blog colores de pulsadores · wevolver.com",
    CAT)

# ===================================================================== D12 · Paro de emergencia
f = Img("s3", 60, 300, h=640)
fb = Img("s3b", 560, 330, w=300)
P["D12_paro_emergencia"] = page(DID,
    kick("SEGURIDAD · ISO 13850", RJ) + T("El paro de", "emergencia", RJ, sub="Lo que exige la norma (IEC 60947-5-5)", size=70)
    + f.html() + fb.html()
    + "<div class='wc' style='left:560px;top:650px;width:480px'><b>Contacto NC de apertura directa</b>: el empuje separa los contactos aunque estén soldados.</div>"
    + "<div style='position:absolute;left:40px;right:40px;top:980px;display:grid;grid-template-columns:repeat(2,1fr);gap:14px'>"
      "<div class='cd' style='position:static;background:#E5383B'><b>ROJO SOBRE AMARILLO</b>combinación solo para emergencia</div>"
      "<div class='cd' style='position:static;background:#0B1F4D'><b>SE ENCLAVA</b>queda abajo hasta desbloquearlo</div>"
      "<div class='cd' style='position:static;background:#0B1F4D'><b>DESBLOQUEO</b>por giro, tirón o llave</div>"
      "<div class='cd' style='position:static;background:#0B1F4D'><b>NO REEMPLAZA</b>al paro normal de la máquina</div></div>",
    "ISO 13850 · IEC 60947-5-5 · Comisión Europea, guía de paros de emergencia (PDF) · ABB, Training Guide No. 2 E-stops (PDF) · RS DesignSpark · Schneider FAQ",
    CAT)

# ===================================================================== D13 · Pilotos (colores)
lamps = [("ROJO", "#E5383B", "Emergencia", "condición peligrosa: actuar ya"), ("AMARILLO", "#F2C500", "Anormal", "condición crítica que se acerca"),
         ("AZUL", "#1446C8", "Obligatorio", "el operador debe actuar"), ("VERDE", "#22A559", "Normal", "funcionamiento correcto"),
         ("BLANCO", "#F1F3F6", "Neutro", "información general")]


def lamp(c):
    return (f"<div style='width:96px;height:96px;border-radius:50%;background:#1b1f27;display:flex;align-items:center;justify-content:center;flex:none;box-shadow:0 6px 12px rgba(0,0,0,.25)'>"
            f"<div style='width:70px;height:70px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0%,{c} 38%,{c} 70%,rgba(0,0,0,.35) 100%);box-shadow:0 0 26px {c}'></div></div>")


P["D13_pilotos_colores"] = page(DID,
    kick("PILOTOS · IEC 60204-1", AZ) + T("¿Qué dice el", "color", AZ, "del piloto?", size=66)
    + "".join(f"<div class='wc' style='left:40px;top:{300 + i * 150}px;width:1000px;display:flex;gap:26px;align-items:center;padding:14px 24px'>{lamp(c)}"
              f"<div><div style='font:900 40px \"Barlow C\";color:#0B1F4D'>{n} · {m}</div><div style='font:500 22px Montserrat;color:#475467'>{d}</div></div></div>"
              for i, (n, c, m, d) in enumerate(lamps))
    + "<div class='nota' style='top:1065px'>Ejemplo práctico: máquina andando normal = <b>verde</b> · advertencia con la máquina andando = <b>amarillo</b> · falla con la máquina detenida = <b>rojo</b>.</div>",
    "IEC 60204-1, 10.3 (tabla de colores de pilotos) · Schneider, blog colores de pulsadores y pilotos · industrialmonitordirect.com · plctalk.net (tabla 3 EN 60204-1)",
    "ilustración propia")

# ===================================================================== D14 · Bloques de contacto: decena y unidad
f = Img("s1b", 70, 320, w=380)
fb = Img("s0b", 70, 740, w=380)
P["D14_bloques_contacto"] = page(DID,
    kick("PULSADORES Y AUXILIARES", TEAL) + T("Los números", "13-14 y 21-22", TEAL, sub="Qué significa cada dígito", size=64)
    + f.html() + fb.html()
    + "<div class='cd' style='left:500px;top:330px;width:540px;background:#0B1F4D'><b>DECENA = POSICIÓN</b>1.º contacto: 1x · 2.º: 2x · 3.º: 3x… (número de orden en el aparato)</div>"
    + "<div class='cd' style='left:500px;top:520px;width:540px;background:#22A559'><b>UNIDAD 3-4 = NA</b>cierra al accionar (13-14, 23-24, 33-34)</div>"
    + "<div class='cd' style='left:500px;top:680px;width:540px;background:#E5383B'><b>UNIDAD 1-2 = NC</b>abre al accionar (11-12, 21-22, 31-32)</div>"
    + "<div class='cd' style='left:500px;top:840px;width:540px;background:#5B6474'><b>5-6 · 7-8</b>NC y NA con función especial (temporizados, adelantados)</div>"
    + "<div class='nota' style='top:1120px'>En el bloque del pulsador ves solo <b>3-4</b> o <b>1-2</b>; en el plano se le suma la decena según su posición: <b>13-14</b>, <b>21-22</b>.</div>",
    "EN 50012 / EN 50013 · IEC 60947-1 · ABB, catálogo CA5 marcado de bornes (PDF) · Siemens, auxiliares 3RH29 (PDF) · electrotechnical-officer.com",
    CAT)

# ===================================================================== D15 · Sensor inductivo partes
f = Img("b1", 40, 520, w=1000)
P["D15_sensor_inductivo"] = page(DID,
    kick("SENSORES", AZ) + T("Las partes del", "sensor inductivo", AZ, sub="3 hilos · PNP · NA · M18", size=60)
    + f.html() +
    rot(f, [dict(t="Marrón BN", s="+24 V", x=150, y=360, w=170, to=(.17, .29), c="#8B4513"),
            dict(t="Negro BK", s="salida", x=150, y=820, w=170, to=(.14, .53), modo="d", c="#111"),
            dict(t="Azul BU", s="0 V", x=360, y=820, w=150, to=(.19, .73), modo="d", c="#1446C8"),
            dict(t="LED", s="indica detección", x=420, y=360, w=190, to=(.39, .27), c=NAR),
            dict(t="Datos impresos", s="PNP · NO · 10–30 VDC", x=660, y=360, w=260, to=(.63, .40), c=AZ),
            dict(t="Tuercas", s="fijación en rosca M18", x=640, y=820, w=230, to=(.82, .80), modo="d", c=AZ),
            dict(t="Cara activa", s="aquí detecta", x=930, y=820, w=190, to=(.95, .75), modo="d", c=RJ)])
    + tabla(900, [("Detecta", "solo metales"), ("Distancia nominal M18 (P+F)", "5 mm enrasado · 8 mm no enrasado"), ("Colores de hilos", "IEC 60947-5-2")])
    + "<div class='nota' style='top:1120px'><b>NO</b> (normalmente abierto): la salida BK se activa cuando hay metal frente a la cara activa. <b>PNP</b>: entrega +24 V en BK.</div>",
    "IEC 60947-5-2 · Pepperl+Fuchs, catálogo Sensors & Systems (PDF) · SICK, IM18 (PDF) · pepperl-fuchs.com, operating distance · baumer.com",
    CAT)

# ===================================================================== D16 · Enrasado vs no enrasado
def sens_v(cx, cara, fondo, color_cara="#2E8BFF"):
    """Sensor cilíndrico vertical (cara arriba) con rosca."""
    w = 90
    x = cx - w / 2
    g = R(x, cara, w, fondo - cara, "#C7CED9", NAV, 3, 6)
    g += "".join(L(x + 4, y, x + w - 4, y + 6, "#8E98A8", 2) for y in range(cara + 30, fondo - 10, 13))
    g += R(x, cara, w, 18, color_cara, NAV, 3, 4)
    return g


def placa(x0, x1, y0, y1, hueco=None):
    g = R(x0, y0, x1 - x0, y1 - y0, "#9AA3B0", NAV, 2, 2)
    g += "".join(L(x, y0 + 4, x - 30, y1 - 4, "#7D8695", 2) for x in range(x0 + 34, x1, 26))
    return g


cxa, cxb = 290, 790
d1 = placa(90, 490, 430, 520) + sens_v(cxa, 430, 760)
d1 += R(cxa - 70, 520, 140, 26, "#6B7280", NAV, 2, 3)  # tuerca
d1 += f"<path d='M{cxa - 45} 428 Q{cxa} 360 {cxa + 45} 428' fill='none' stroke='{VER}' stroke-width='4' stroke-dasharray='8 6'/>"
d1 += Tx(cxa, 318, "ENRASADO (flush)", 34, 900, NAV, fam="Barlow C") + Tx(cxa, 352, "la cara queda al ras del metal", 20, 600, "#475467")
d2 = placa(590, 1000, 560, 650) + sens_v(cxb, 430, 760)
d2 += R(cxb - 70, 534, 140, 26, "#6B7280", NAV, 2, 3)
d2 += f"<rect x='{cxb - 135}' y='430' width='270' height='130' fill='rgba(34,165,89,.08)' stroke='{VER}' stroke-width='3' stroke-dasharray='10 7'/>"
d2 += f"<path d='M{cxb - 45} 428 Q{cxb - 90} 392 {cxb} 392 Q{cxb + 90} 392 {cxb + 45} 428' fill='none' stroke='{VER}' stroke-width='4' stroke-dasharray='8 6'/>"
d2 += Tx(cxb, 318, "NO ENRASADO (non-flush)", 34, 900, NAV, fam="Barlow C") + Tx(cxb, 352, "sobresale: zona libre sin metal", 20, 600, "#475467")
d2 += L(cxb - 135, 672, cxb + 135, 672, NAR, 3) + L(cxb - 135, 662, cxb - 135, 682, NAR, 3) + L(cxb + 135, 662, cxb + 135, 682, NAR, 3) + R(cxb - 120, 685, 240, 30, "#F6FAFF", "#F6FAFF", 0, 4) + Tx(cxb, 700, "zona libre: 3 × diámetro", 20, 800, NAR)
d2 += L(cxb + 160, 430, cxb + 160, 560, NAR, 3) + Tx(cxb + 170, 495, "2 × sn", 22, 900, NAR, a="start", fam="Barlow C")
dib = svg(0, 0, 1080, 1350, d1 + d2 + Tx(cxa, 800, "metal alrededor", 20, 700, "#475467") + Tx(cxb, 800, "metal más atrás", 20, 700, "#475467"))
P["D16_enrasado"] = page(DID,
    kick("SENSORES INDUCTIVOS", AZ) + T("¿Enrasado o", "no enrasado", AZ, "?", size=62)
    + "<div class='pn' style='top:280px;height:560px'></div>" + dib
    + tabla(860, [("M8", "1,5 mm · 2 mm"), ("M12", "2 mm · 4 mm"), ("M18", "5 mm · 8 mm"), ("M30", "10 mm · 15 mm")],
            cab="<span>Diámetro</span><span style='text-align:right'>sn enrasado · no enrasado</span>")
    + "<div class='nota' style='top:1185px;padding:12px 24px;font-size:21px'>El no enrasado llega más lejos, pero pide zona libre: <b>3 × diámetro</b> alrededor y <b>2 × sn</b> de fondo.</div>",
    "IEC 60947-5-2 · Pepperl+Fuchs, tdoct6955a (PDF) · Bernstein, catálogo inductivos (PDF) · pepperl-fuchs.com, installation conditions · ifm.com · balluff.com",
    "ilustración propia")

# ===================================================================== D17 · Sensor capacitivo
f = Img("b2", 40, 340, w=1000)
mats = ["Agua", "Granos", "Plástico", "Madera", "Vidrio", "Papel", "Aceite", "Metal"]
P["D17_sensor_capacitivo"] = page(DID,
    kick("SENSORES", NAR) + T("El capacitivo", "ve el agua", NAR, sub="y casi cualquier material", size=72)
    + f.html() +
    rot(f, [dict(t="Potenciómetro", s="ajuste de sensibilidad", x=420, y=660, w=260, to=(.39, .50), modo="d", c=NAR),
            dict(t="Cara activa", s="campo eléctrico", x=900, y=660, w=220, to=(.96, .62), modo="d", c=RJ)])
    + "<div style='position:absolute;left:40px;right:40px;top:760px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px'>"
    + "".join(f"<div style='background:#FFF1E0;border:3px solid #FFD2A1;border-radius:16px;padding:12px;text-align:center;font:900 30px \"Barlow C\";color:#0B1F4D'>{m}</div>" for m in mats)
    + "</div>"
    + "<div class='tx' style='top:960px;font-size:23px'>Detecta materiales <b>conductores y no conductores</b>; también a través de la pared de un tanque de plástico o vidrio. "
      "Mientras mayor la <b>constante dieléctrica</b> del material, más fácil lo detecta.</div>"
    + "<div class='nota' style='top:1150px'>Subir mucho la sensibilidad lo vuelve sensible a <b>humedad, temperatura y suciedad</b>.</div>",
    "IEC 60947-5-2 · Pepperl+Fuchs, Introduction to capacitive sensors (catálogo PDF) · Bernstein, catálogo capacitivos · balluff.com · ifm.com",
    CAT)

# ===================================================================== D18 · Fotoeléctricos 3 tipos
fs = [Img("op1", 50, 350 + i * 255, w=450) for i in range(3)]


def haz(y, x1, x2, ida_vuelta=True):
    s = L(x1, y - 10, x2, y - 10, RJ, 4, "12 8")
    if ida_vuelta:
        s += L(x2 - 6, y + 10, x1, y + 10, RJ, 4, "12 8")
    return s


fy = [f.p(1, .58)[1] for f in fs]
xf = fs[0].p(1, .5)[0] + 8
emisor = (R(880, fy[2] - 40, 150, 80, "#C7CED9", NAV, 3, 10) + R(868, fy[2] - 30, 22, 60, "#E5383B", NAV, 3, 4)
          + Tx(960, fy[2], "EMISOR", 20, 900, NAV, fam="Barlow C") + Tx(955, fy[2] + 62, "2 hilos: BN + · BU −", 17, 700, "#475467"))
dib = svg(0, 0, 1080, 1350,
          haz(fy[0], xf, 760) + R(760, fy[0] - 60, 70, 120, "#9AA3B0", NAV, 3, 6) + Tx(795, fy[0] + 82, "objeto", 18, 800, "#475467")
          + haz(fy[1], xf, 880) + R(880, fy[1] - 60, 44, 120, "#E5383B", NAV, 3, 4)
          + "".join(L(882, fy[1] - 52 + k * 22, 920, fy[1] - 36 + k * 22, "#fff", 2) for k in range(5)) + Tx(902, fy[1] + 82, "reflector", 18, 800, "#475467")
          + L(xf, fy[2], 866, fy[2], RJ, 4, "12 8") + emisor)
P["D18_fotoelectricos"] = page(DID,
    kick("SENSORES FOTOELÉCTRICOS", RJ) + T("Los 3 tipos de", "fotocelda", RJ, size=70)
    + "".join(f.html() for f in fs) + dib
    + "".join(f"<div style='position:absolute;left:56px;top:{350 + i * 255 - 50}px;font:900 36px \"Barlow C\";color:#0B1F4D'>{t}</div>"
              f"<div style='position:absolute;left:56px;top:{350 + i * 255 + 120}px;width:660px;font:500 21px Montserrat;color:#475467'>{d}</div>"
              for i, (t, d) in enumerate([("1 · DIFUSO", "La luz rebota en el objeto y vuelve al mismo sensor: se instala en un solo punto."),
                                          ("2 · RÉFLEX", "La luz va y vuelve del reflector; detecta cuando el objeto corta el haz."),
                                          ("3 · BARRERA", "Emisor frente a receptor; detecta cuando el objeto corta el haz. Es el de mayor alcance.")]))
    + "<div class='nota' style='top:1150px'>Alcance: <b>barrera</b> &gt; <b>réflex</b> &gt; <b>difuso</b>. La barrera necesita cablear dos equipos.</div>",
    "Omron, Photomicrosensors technical guide (PDF) · AutomationDirect, Photo sensors overview (PDF) · ifm.com, photoelectric sensors · element14 (Bulgin)",
    CAT)

# ===================================================================== D19 · PNP vs NPN
def esquema(ox, pnp):
    BNc, BUc = "#8B4513", "#1446C8"
    s = L(ox + 20, 60, ox + 470, 60, BNc, 7) + Tx(ox + 470, 34, "+24 V", 26, 900, BNc, a="end", fam="Barlow C")
    s += L(ox + 20, 400, ox + 470, 400, BUc, 7) + Tx(ox + 470, 428, "0 V", 26, 900, BUc, a="end", fam="Barlow C")
    s += R(ox + 30, 150, 170, 170, "#C7CED9", NAV, 3, 14) + Tx(ox + 115, 205, "SENSOR", 26, 900, NAV, fam="Barlow C")
    s += Tx(ox + 115, 250, "PNP" if pnp else "NPN", 44, 900, AZ if pnp else NAR, fam="Barlow C")
    s += f"<polyline points='{ox + 200},180 {ox + 250},180 {ox + 250},60' fill='none' stroke='{BNc}' stroke-width='6'/>" + Tx(ox + 212, 165, "BN", 18, 800, BNc, a="start")
    s += f"<polyline points='{ox + 200},290 {ox + 290},290 {ox + 290},400' fill='none' stroke='{BUc}' stroke-width='6'/>" + Tx(ox + 212, 310, "BU", 18, 800, BUc, a="start")
    s += L(ox + 200, 235, ox + 390, 235, "#111", 6) + Tx(ox + 212, 220, "BK", 18, 800, "#111", a="start")
    if pnp:
        s += L(ox + 390, 235, ox + 390, 285, "#111", 6) + R(ox + 345, 285, 90, 56, AM, NAV, 3, 8) + Tx(ox + 390, 313, "carga", 20, 800, NAV) + L(ox + 390, 341, ox + 390, 400, BUc, 6)
    else:
        s += L(ox + 390, 60, ox + 390, 120, BNc, 6) + R(ox + 345, 120, 90, 56, AM, NAV, 3, 8) + Tx(ox + 390, 148, "carga", 20, 800, NAV) + L(ox + 390, 176, ox + 390, 235, "#111", 6)
    s += f"<circle cx='{ox + 390}' cy='235' r='7' fill='#111'/>"
    return s


P["D19_pnp_npn"] = page(DID,
    kick("SENSORES · 3 HILOS", AZ) + T("¿PNP o", "NPN?", AZ, sub="Dónde va la carga en un sensor de 3 hilos", size=74)
    + "<div class='pn' style='top:290px;height:470px'></div>"
    + svg(40, 300, 500, 450, esquema(10, True)) + svg(540, 300, 500, 450, esquema(10, False))
    + "<div class='cd' style='left:40px;top:790px;width:490px;background:#0057FF'><b>PNP · “sourcing”</b>Entrega <b style='display:inline;font:800 21px Montserrat'>+24 V</b> por BK. La carga va entre BK y 0 V (BU).</div>"
    + "<div class='cd' style='left:550px;top:790px;width:490px;background:#FF8A00'><b>NPN · “sinking”</b>Conecta BK a <b style='display:inline;font:800 21px Montserrat'>0 V</b>. La carga va entre BK y +24 V (BN).</div>"
    + "<div class='nota' style='top:960px'>En un PLC: sensor <b>PNP</b> → entrada <b>sink</b> (común a 0 V) · sensor <b>NPN</b> → entrada <b>source</b>. Deben coincidir o la entrada no funciona.</div>"
    + "<div class='wc' style='left:40px;top:1090px;width:1000px'><b>¿Qué es la “carga”?</b> La bobina de un relé, la entrada de un relé-contactor o la entrada de un PLC.</div>",
    "IEC 60947-5-2 · Pepperl+Fuchs, Sensor connections (catálogo PDF) · Schneider, FAQ FA23633 · pepperl-fuchs.com, 3-wire sensors · RS, PNP vs NPN",
    "ilustración propia")

# ===================================================================== D20 · Placa del motor (foto, recuadros de color)
f = Img("p07_placa", 40, 280, w=1000, foto=True)
zonas = [("Potencia", "0,37 kW = 0,5 HP", RJ, (.14, .575, .58, .655)),
         ("Velocidad y frecuencia", "2730 rpm · 50 Hz (2 polos)", AZ, (.05, .675, .55, .755)),
         ("Aislamiento", "clase F (155 °C)", NAR, (.585, .47, .79, .555)),
         ("Protección", "IP55 (polvo y chorros)", VER, (.585, .575, .79, .655)),
         ("Conexión", "Δ / Y (triángulo / estrella)", "#8E44AD", (.585, .675, .86, .755)),
         ("Tensión y corriente", "230/400 V · 1,67/0,97 A", "#0B1F4D", (.05, .775, .60, .86))]
rects = ""
for n, d, c, (x0, y0, x1, y1) in zonas:
    ax, ay = f.p(x0, y0)
    bx, by = f.p(x1, y1)
    rects += (f"<rect x='{ax:.0f}' y='{ay:.0f}' width='{bx - ax:.0f}' height='{by - ay:.0f}' rx='8' fill='none' stroke='#fff' stroke-width='9'/>"
              f"<rect x='{ax:.0f}' y='{ay:.0f}' width='{bx - ax:.0f}' height='{by - ay:.0f}' rx='8' fill='none' stroke='{c}' stroke-width='5'/>")
cards = "".join(f"<div style='border-radius:16px;padding:12px 16px;background:#fff;border:4px solid {c}'>"
                f"<div style='font:900 28px \"Barlow C\";color:{c}'>{n}</div><div style='font:600 19px Montserrat;color:#1d2939'>{d}</div></div>"
                for n, d, c, _ in zonas)
P["D20_placa_motor"] = page(DID,
    kick("MOTOR", AZ) + T("Así se lee la", "placa del motor", AZ, size=62)
    + f.html(marco="") + svg(0, 0, 1080, 1350, rects)
    + f"<div style='position:absolute;left:40px;right:40px;top:850px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px'>{cards}</div>"
    + "<div class='wc' style='left:40px;top:1080px;width:1000px;padding:12px 20px'>A <b>230 V</b> se conecta en <b>triángulo</b> y toma 1,67 A; a <b>400 V</b>, en <b>estrella</b> y toma 0,97 A. La tensión mayor siempre va en estrella.</div>"
    + "",
    "IEC 60034-1 · ABB, How to read a motor nameplate · Siemens, manual 1LG0 (conexiones, PDF) · Bitzer, arranque en estrella o triángulo · IEC 60529",
    f"“Motor nameplate Malmbergs”, Olgailga2, CC0, {CC}")

# ===================================================================== D21 · Caja de bornes Δ / Y
fd = Img("bmd", 40, 300, w=490)
fy_ = Img("bmy", 550, 300, w=490)
P["D21_delta_estrella"] = page(DID,
    kick("MOTOR · 6 BORNES", NAR) + T("Triángulo o", "estrella", NAR, sub="Los puentes en la caja de bornes (IEC 60034-8)", size=70)
    + fd.html(sombra=False) + fy_.html(sombra=False)
    + "<div class='cd' style='left:40px;top:830px;width:490px;height:170px;background:#0B1F4D'><b>TRIÁNGULO (Δ)</b>Puentes verticales: U1-W2 · V1-U2 · W1-V2. Línea a U1, V1, W1. Para la tensión <b style='display:inline;font:800 21px Montserrat;color:#FFD400'>menor</b> de la placa.</div>"
    + "<div class='cd' style='left:550px;top:830px;width:490px;height:170px;background:#FF8A00'><b>ESTRELLA (Y)</b>Un puente une W2-U2-V2. Línea a U1, V1, W1. Para la tensión <b style='display:inline;font:800 21px Montserrat;color:#0B1F4D'>mayor</b> de la placa.</div>"
    + tabla(1040, [("Placa 230/400 V", "Δ a 230 V · Y a 400 V"), ("Placa 400/690 V", "Δ a 400 V · Y a 690 V")]),
    "IEC 60034-8 · Siemens, manual 1LG0 y SIRIUS CD-FE-III-001 (PDF) · dev.to, star and delta · industrialmonitordirect.com, 6-wire motors",
    CAT)

# ===================================================================== D22 · NEMA 9 puntas
f = Img("p02_motor", 640, 285, w=360, foto=True)
P["D22_nema_9_puntas"] = page(DID,
    kick("MOTOR NEMA · 9 PUNTAS", RJ) + T("9 puntas:", "baja o alta", RJ, sub="Motor de doble tensión en estrella (230/460 V)", size=64)
    + f.html(marco='')
    + "<div class='wc' style='left:40px;top:320px;width:490px'>Cada fase tiene <b>dos bobinas</b>: en tensión baja van en <b>paralelo</b> y en alta en <b>serie</b>. La placa trae el diagrama: síguelo siempre.</div>"
    + tabla(590, [("L1", "T1 + T7"), ("L2", "T2 + T8"), ("L3", "T3 + T9"), ("Unir", "T4 + T5 + T6")],
            cab="<span>TENSIÓN BAJA (230 V) · estrella paralela</span>")
    + tabla(900, [("L1 · L2 · L3", "T1 · T2 · T3"), ("Unir", "T4-T7 · T5-T8 · T6-T9")],
            cab="<span>TENSIÓN ALTA (460 V) · estrella serie</span>", extra="border-color:#E5383B")
    + "<div class='nota' style='top:1120px'>Para invertir el giro: intercambia <b>dos líneas</b> (por ejemplo L1 y L2).</div>",
    "NEMA MG 1 · US Motors (Nidec), diagramas de conexión 9 puntas (PDF) · control.com, Motors and wiring eBook (PDF) · bccampus.ca, Basic motor control · electricmotorwarehouse.com",
    f"“TMW 50906 Schnittmodell einer Drehstrommaschine”, dominio público, {CC}")

# ===================================================================== D23 · Motor por dentro (miniatura oscura)
f = Img("p05_motor2", 140, 420, w=800, foto=True)
P["D23_motor_dentro"] = page(OSC,
    "<div class='kk' style='background:#FFD400;color:#0B1220;left:50%;transform:translateX(-50%)'>POR DENTRO</div>"
    + T("¿Qué hay dentro<br>de un", "motor", AM, "?", size=76, top=90, center=True)
    + f.html(marco="border-color:#FFD400") +
    rot(f, [dict(t="Caja de bornes", x=180, y=420, w=230, to=(.47, .27), c=AM),
            dict(t="Eje", x=130, y=700, w=120, to=(.17, .45), modo="d", c="#2EC4FF"),
            dict(t="Devanado", s="estator", x=120, y=880, w=190, to=(.25, .60), modo="d", c="#FF4D4D"),
            dict(t="Rotor", s="jaula de ardilla", x=660, y=1060, w=220, to=(.45, .50), modo="d", c=AM),
            dict(t="Ventilador", x=930, y=700, w=190, to=(.83, .57), modo="d", c="#2EC4FF"),
            dict(t="Aletas", s="disipan calor", x=330, y=1060, w=190, to=(.38, .77), modo="d", c="#2EC4FF")])
    + "<div class='pills' style='top:1170px'><div style='background:#FF4D4D'>ESTATOR → CAMPO GIRATORIO</div>"
      "<div style='background:#FFD400;color:#0B1220'>ROTOR → GIRA</div></div>",
    "IEC 60034-1 · Pumps & Systems, Induction motor construction · patente US 10804764 (motor TEFC) · Scribd EE462, partes del motor de inducción",
    f"“Cut-away version of an electric motor (1)”, S.J. de Waard, CC BY 2.5, {CC}", True)

# ===================================================================== D24 · Rotor jaula de ardilla (foto, por dentro blanco)
f = Img("p08_rotor", 40, 470, w=1000, foto=True)
P["D24_rotor_jaula"] = page(DID,
    kick("MOTOR", VER) + T("El rotor", "jaula de ardilla", VER, size=64)
    + "<div class='wc' style='left:40px;top:300px;width:1000px;border-left:8px solid #22A559'>Barras de <b>aluminio</b> metidas en un paquete de <b>chapas de acero</b> y unidas en los extremos por <b>anillos de cortocircuito</b>. "
      "En motores chicos el aluminio se inyecta fundido; las barras van <b>inclinadas</b> para bajar ruido y vibración.</div>"
    + f.html(marco="")
    + rot(f, [dict(t="Barras inclinadas", s="aluminio", x=560, y=1140, w=240, to=(.55, .55), modo="d", c=RJ),
              dict(t="Anillo de cortocircuito", x=900, y=470, w=270, to=(.735, .575), c=AZ),
              dict(t="Chapas de acero", s="laminadas", x=300, y=1140, w=230, to=(.45, .62), modo="d", c=AZ),
              dict(t="Rodamiento", x=840, y=1140, w=200, to=(.80, .74), modo="d", c=RJ),
              dict(t="Eje", x=960, y=1020, w=110, to=(.92, .86), c=AZ),
              dict(t="Tapa", s="escudo con rodamiento", x=170, y=470, w=230, to=(.13, .55), modo="d", c=AZ)]),
    "IEC 60034-1 · patente US 8701270 (rotor de jaula) · patente EP 0435313 (barras inclinadas) · Wikipedia, Squirrel-cage rotor",
    f"“Wirnik by Zureks”, Zureks, CC BY-SA 3.0, {CC}")

# ===================================================================== D25 · Borneras
f = Img("x0", 260, 380, w=560)
P["D25_borneras"] = page(DID,
    kick("TABLERO · BORNERAS", TEAL) + T("El color de la", "bornera", TEAL, sub="Paquete -X0 de alimentación", size=70)
    + f.html() +
    rot(f, [dict(t="Gris", s="paso (fases)", x=150, y=880, w=170, to=(.30, .80), modo="d", c="#5B6474"),
            dict(t="Azul", s="neutro (N)", x=480, y=880, w=170, to=(.60, .80), modo="d", c="#1446C8"),
            dict(t="Verde-amarillo", s="tierra (PE)", x=820, y=880, w=220, to=(.80, .80), modo="d", c=VER),
            dict(t="Designación", s="-X0", x=130, y=360, w=170, to=(.06, .55), c=NAR),
            dict(t="Marcador", s="número de borne", x=930, y=360, w=230, to=(.79, .16), c=AZ)])
    + "<div style='position:absolute;left:40px;right:40px;top:960px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px'>"
      "<div class='cd' style='position:static;background:#5B6474'><b>-X0</b>alimentación</div>"
      "<div class='cd' style='position:static;background:#0B1F4D'><b>-X1</b>motores</div>"
      "<div class='cd' style='position:static;background:#0057FF'><b>-X2 / -X3</b>puerta y campo</div></div>"
    + "<div class='nota' style='top:1110px'>El color dice la función: <b>gris</b> paso, <b>azul</b> neutro, <b>verde-amarillo</b> tierra. Los nombres -X0…-X3 son convención de taller (IEC 81346 deja libre el número).</div>",
    "IEC 60947-7-1 · IEC 60947-7-2 · Phoenix Contact, PT 4-PE y PTS 2,5-PE (PDF) · phoenixcontact.com, borneras PE · IEC 81346-2",
    CAT)

# ===================================================================== D26 · LOGO!
f = Img("logo", 40, 330, w=1000)
P["D26_logo_partes"] = page(DID,
    kick("PLC · SIEMENS", TEAL) + T("Las partes del", "LOGO! 8", TEAL, sub="12/24RCE (6ED1052-1MD08-0BA1) + fuente LOGO!Power", size=66)
    + f.html() +
    rot(f, [dict(t="Alimentación", s="L+ · M (12/24 VDC)", x=520, y=290, w=240, to=(.48, .08), c=RJ),
            dict(t="8 entradas", s="I1…I8 · 4 analógicas 0–10 V", x=860, y=290, w=320, to=(.74, .08), c=AZ),
            dict(t="Pantalla", s="y teclas", x=600, y=1150, w=170, to=(.57, .55), modo="d", c=AZ),
            dict(t="Ethernet", s="LAN", x=380, y=1150, w=160, to=(.442, .714), modo="d", c=AZ),
            dict(t="4 salidas a relé", s="10 A resistiva · 3 A inductiva", x=870, y=1150, w=320, to=(.755, .895), modo="d", c=RJ),
            dict(t="Fuente -T1", s="24 VDC", x=150, y=1150, w=170, to=(.14, .48), modo="d", c=NAR)])
    + "",
    "Siemens, ficha 6ED1052-1MD08-0BA1 (PDF) · Siemens, ficha 6ED1052-2MD08 (PDF) · Siemens Industry Mall · RS Components, LOGO! 12/24RCE",
    CAT)

# ===================================================================== D27 · S7-1200 1212C
f = Img("s7", 220, 330, w=640)
P["D27_s7_1200"] = page(DID,
    kick("PLC · SIEMENS", AZ) + T("Las partes del", "S7-1200", AZ, sub="CPU 1212C AC/DC/RLY (6ES7212-1BE40-0XB0)", size=70)
    + f.html() +
    rot(f, [dict(t="Alimentación", s="85–264 VAC", x=120, y=330, w=200, to=(.08, .09), c=RJ),
            dict(t="Salida 24 VDC", s="para sensores", x=120, y=520, w=200, to=(.25, .09), modo="d", c=NAR),
            dict(t="8 entradas", s="24 VDC", x=960, y=330, w=180, to=(.55, .09), c=AZ),
            dict(t="2 analógicas", s="0–10 V", x=960, y=520, w=180, to=(.92, .09), modo="d", c=AZ),
            dict(t="LED de estado", s="RUN/STOP · ERROR", x=120, y=760, w=220, to=(.05, .34), modo="d", c=AZ),
            dict(t="LED de E/S", x=960, y=760, w=170, to=(.83, .65), modo="d", c=AZ),
            dict(t="6 salidas a relé", s="2 A", x=960, y=1150, w=200, to=(.80, .93), modo="d", c=RJ),
            dict(t="Ethernet", s="PROFINET", x=120, y=1150, w=180, to=(.30, .78), modo="d", c=AZ)])
    + "",
    "Siemens, ficha 6ES7212-1BE40-0XB0 (PDF, EN y DE) · Siemens, SIPLUS 6AG1212-1BE40 (PDF) · Siemens Industry Mall (1212C AC/DC/relé)",
    CAT)

# ===================================================================== D28 · Multímetro CAT (dato gigante)
f = Img("mm", 680, 120, h=540)
P["D28_multimetro_cat"] = page(BIG,
    kick("DATO CLAVE · MULTÍMETRO", "#0B1220")
    + "<div class='big' style='font-size:220px;top:120px'>CAT III</div>"
    + "<div class='t' style='top:360px;width:560px'>el <em>mínimo</em> para medir en un tablero industrial</div>"
    + f.html()
    + "<div class='sub2' style='top:690px'>La categoría (IEC 61010-1) indica qué <b>sobretensión</b> aguanta el medidor según dónde mides. "
      "Un <b>CAT III 600 V</b> protege más que un CAT II 1000 V.</div>"
    + tabla(860, [("CAT IV · acometida, medidor, exterior", "más severa"), ("CAT III · tableros, motores, barras", "industria"),
                  ("CAT II · tomacorrientes y aparatos", "casa"), ("CAT I · electrónica protegida", "menos severa")], extra="border-color:#E3001B")
    + "<div class='nota' style='top:1170px;padding:12px 24px'>Para un tablero de 480 V: <b>CAT III 600 V</b> o mejor.</div>",
    "IEC 61010-1 · Fluke, ABCs of multimeter safety (PDF) · Fluke, safety pages (PDF) · fluke.com, Guide to digital multimeter safety",
    CAT)

# ===================================================================== D29 · Pinza: un solo conductor
f = Img("pz", 80, 300, h=820)
dib = svg(0, 0, 1080, 1350,
          "<circle cx='241' cy='425' r='30' fill='#111' stroke='#fff' stroke-width='3'/><circle cx='241' cy='425' r='17' fill='#C8793A'/>")
P["D29_pinza_un_conductor"] = page(DID,
    kick("MEDICIÓN", RJ) + T("La pinza:", "un solo cable", RJ, sub="Si abrazas dos, los campos se cancelan", size=66)
    + f.html() + dib
    + "<div class='cd' style='left:470px;top:340px;width:570px;background:#22A559'><b>✔ UNA FASE</b>Abraza un conductor a la vez. En trifásico mide L1, L2 y L3 por separado.</div>"
    + "<div class='cd' style='left:470px;top:560px;width:570px;background:#E5383B'><b>✘ IDA Y VUELTA JUNTAS</b>Fase y neutro (o las 3 fases) dentro de la mordaza: la lectura da 0 o un valor falso.</div>"
    + "<div class='cd' style='left:470px;top:780px;width:570px;background:#0B1F4D'><b>EXCEPCIÓN</b>Para buscar corriente de fuga sí se abrazan todos los conductores del circuito (pinza de fuga).</div>"
    + "<div class='nota' style='top:1150px'>En la puesta en marcha del motor: pinza en <b>un solo conductor</b> y compara con la corriente de placa.</div>",
    "Fluke, Clamp meter readings: problems and solutions · Fluke, How to measure current with a clamp meter · Hioki, How to use clamp meters",
    CAT)

# ===================================================================== D30 · El riel también es tierra
f = Img("x0", 60, 330, w=470)
P["D30_riel_tierra"] = page(DID,
    kick("TABLERO · PE", VER) + T("El riel DIN", "también es tierra", VER, sub="Bornera PE con pie metálico (IEC 60947-7-2)", size=62)
    + f.html()
    + rot(f, [dict(t="Bornera PE", s="pie metálico al riel", x=820, y=420, w=250, to=(.80, .50), c=VER)])
    + "<div class='wc' style='left:560px;top:520px;width:480px'>La bornera verde-amarilla se engancha al riel con un <b>pie metálico</b>: el riel queda unido a tierra y conduce la corriente de falla.</div>"
    + tabla(780, [("Riel 35 × 7,5 de acero", "≈ 16 mm² de cobre"), ("Riel 35 × 15 de acero (Phoenix NS 35/15)", "≈ 25 mm² de cobre"),
                  ("Riel 35 × 15 de cobre (Phoenix NS 35/15 CU)", "≈ 95 mm² de cobre")], cab="<span>EQUIVALENCIA DEL RIEL COMO CONDUCTOR PE</span>")
    + "<div class='nota' style='top:1100px'>Por eso el riel debe ir <b>atornillado y conectado a la barra de tierra</b>; respeta la capacidad del riel que indica el fabricante.</div>",
    "IEC 60947-7-2 · Phoenix Contact, NS 35/15 y NS 35/15 CU (PDF) · Phoenix Contact, PTS 2,5-PE (PDF) · Eaton/efobasen, riel TS35×7,5 · phoenixcontact.com, UKK 5-PE",
    CAT)


if __name__ == "__main__":
    import sys
    sel = sys.argv[1:] or list(P)
    for k in sel:
        (AQ / "html" / f"{k}.html").write_text(P[k], encoding="utf-8")
    subprocess.run(["node", "shot.js", *sel], cwd=AQ, check=True)
    print("ok", len(sel))

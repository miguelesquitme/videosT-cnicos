"""Lote C (25-nov): 10 imágenes de temas MUY específicos, cada dato cruzado con 2 PDF + 2 páginas web
(ver referencias/loteC_fuentes.md). SIN símbolos IEC dibujados a mano (error del lote B): solo datos de norma,
gráficos simples, tablas, tarjetas de color y fotos reales de Commons. Estilos aprobados: didáctico y dato gigante."""
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
p7 = _load("p7", AQ.parent / "posts7" / "gen.py")
Foto, CC, page = p4.Foto, p4.CC, p6.page
NAV, AZ, TEAL, NAR, RJ, VER, AM, CU, GR = "#0B1F4D", "#0057FF", "#0FA3A3", "#FF8A00", "#E5383B", "#22A559", "#FFD400", "#E08A2E", "#8A94A6"
ROJO_BIG = "#E3001B"

DID = """body{background:#fff!important}
.kk{position:absolute;left:50px;top:40px;font:800 22px Montserrat;letter-spacing:3px;color:#fff;padding:6px 16px;border-radius:8px}
.tt{position:absolute;left:46px;right:40px;top:86px;font:900 66px/1.04 Montserrat;color:#0B1F4D;letter-spacing:-1.8px}
.tt em{font-style:normal;background:linear-gradient(transparent 56%,#FFD400 56%);padding:0 6px}
.pn{position:absolute;left:40px;right:40px;border-radius:26px;border:3px solid #CFE0F5;background:#F6FAFF}
.tx{position:absolute;left:56px;right:56px;font:500 24px/1.38 Montserrat;color:#1d2939}.tx b{font-weight:800;color:#0B1F4D}
.cd{position:absolute;border-radius:20px;padding:16px 20px;color:#fff;font:500 21px/1.3 Montserrat}
.cd b{display:block;font:900 36px/1 'Barlow C';margin-bottom:6px}
.wc{position:absolute;background:#fff;border:3px solid #CFE0F5;border-radius:20px;padding:16px 20px;font:500 21px/1.3 Montserrat;color:#1d2939}
.wc b{font-weight:800;color:#0B1F4D}
.nota{position:absolute;left:40px;right:40px;border-radius:18px;background:#0B1F4D;color:#fff;font:600 23px/1.32 Montserrat;padding:16px 24px}
.nota b{color:#FFD400}
svg{position:absolute;overflow:visible}"""

BIG = p7.BIG + """
.sub2{position:absolute;left:50px;right:50px;font:500 25px/1.36 Montserrat;color:#1d2939}.sub2 b{font-weight:800;color:#0B1220}
.tb div{align-items:center}.tb div span{font:500 23px Montserrat;color:#475467}
svg{position:absolute;overflow:visible}"""


def head(kick, col, t):
    return f"<div class='kk' style='background:{col}'>{kick}</div><div class='tt'>{t}</div>"


def svg(x, y, w, h, body):
    return f"<svg style='left:{x}px;top:{y}px' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{body}</svg>"


def L(x1, y1, x2, y2, c=NAV, w=3):
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{c}' stroke-width='{w}' stroke-linecap='round'/>"


def R(x, y, w, h, f="#fff", c=NAV, sw=3, r=6):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{r}' fill='{f}' stroke='{c}' stroke-width='{sw}'/>"


def T(x, y, s, size=24, w=700, c=NAV, a="middle", fam="Montserrat"):
    return f"<text x='{x}' y='{y}' font-family='{fam}' font-size='{size}' font-weight='{w}' fill='{c}' text-anchor='{a}' dominant-baseline='central'>{s}</text>"


def cota_h(x1, x2, y, txt, c=NAV, size=26):
    """Cota horizontal con flechas en ambos extremos y texto encima."""
    a = 12
    return (L(x1, y, x2, y, c, 2.5)
            + f"<polygon points='{x1},{y} {x1 + a},{y - 6} {x1 + a},{y + 6}' fill='{c}'/>"
            + f"<polygon points='{x2},{y} {x2 - a},{y - 6} {x2 - a},{y + 6}' fill='{c}'/>"
            + f"<rect x='{(x1 + x2) / 2 - 62}' y='{y - 19}' width='124' height='38' rx='8' fill='#F6FAFF'/>"
            + T((x1 + x2) / 2, y, txt, size, 800, c, fam="Barlow C"))


def cota_v(x, y1, y2, txt, c=NAV, size=26, lado=1):
    a = 12
    return (L(x, y1, x, y2, c, 2.5)
            + f"<polygon points='{x},{y1} {x - 6},{y1 + a} {x + 6},{y1 + a}' fill='{c}'/>"
            + f"<polygon points='{x},{y2} {x - 6},{y2 - a} {x + 6},{y2 - a}' fill='{c}'/>"
            + T(x + lado * 14, (y1 + y2) / 2, txt, size, 800, c, a="start" if lado > 0 else "end", fam="Barlow C"))


P = {}

# ===================================================================== C01 · IP65
cajas = (
    "<div class='cd' style='left:56px;top:300px;width:470px;height:280px;background:#0B1F4D'>"
    "<div style='display:flex;align-items:center;gap:18px'><div style='font:900 150px/0.9 \"Barlow C\";color:#FFD400'>6</div>"
    "<div><b>POLVO</b>hermético:<br>no entra nada</div></div>"
    "<div style='margin-top:14px;font-size:20px;line-height:1.35'>Prueba: cámara con talco y el equipo en depresión (hasta 2 kPa) durante <b style='display:inline;font:800 21px Montserrat;color:#FFD400'>8 h</b>. "
    "Al abrir no debe haber polvo.</div></div>"
    "<div class='cd' style='left:554px;top:300px;width:470px;height:280px;background:#0057FF'>"
    "<div style='display:flex;align-items:center;gap:18px'><div style='font:900 150px/0.9 \"Barlow C\";color:#fff'>5</div>"
    "<div><b>AGUA</b>chorros desde<br>cualquier dirección</div></div>"
    "<div style='margin-top:14px;font-size:20px;line-height:1.35'>Prueba: boquilla de <b style='display:inline;font:800 21px Montserrat;color:#FFD400'>6,3 mm</b>, 12,5 L/min, "
    "a 2,5–3 m, mínimo 3 min. No debe entrar agua que haga daño.</div></div>")
# esquema: gabinete con chorros de varias direcciones
g = []
gx, gy, gw, gh = 380, 70, 250, 170
g.append(R(gx, gy, gw, gh, "#E9EEF6", NAV, 4, 14) + R(gx + 30, gy + 30, gw - 60, gh - 60, "#fff", "#9AA9C2", 2, 8))
g.append(T(gx + gw / 2, gy + gh / 2, "IP65", 46, 900, NAV, fam="Barlow C"))
for (x1, y1, x2, y2) in [(150, 40, gx - 20, gy + 40), (150, 260, gx - 20, gy + gh - 30), (860, 40, gx + gw + 20, gy + 40),
                         (860, 260, gx + gw + 20, gy + gh - 30), (gx + gw / 2, -30, gx + gw / 2, gy - 18)]:
    g.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#2E8BFF' stroke-width='9' stroke-dasharray='16 10' stroke-linecap='round'/>")
    g.append(f"<circle cx='{x1}' cy='{y1}' r='15' fill='#0B1F4D'/>")
esquema = svg(40, 640, 1000, 300, "".join(g))
P["C01_ip65"] = page(DID,
    head("GRADO IP · IEC 60529", AZ, "¿Qué significa<br>un <em>IP65</em>?")
    + "<div class='pn' style='top:280px;height:680px'></div>" + cajas + esquema
    + "<div class='tx' style='top:990px'>El <b>primer dígito</b> protege a las personas y al equipo contra sólidos; el <b>segundo</b>, solo contra el agua. "
      "Son pruebas distintas: un IP65 no está probado para sumergirse (eso es el 7).</div>"
    + "<div class='nota' style='top:1150px'><b>IP66</b> = chorro potente (boquilla de 12,5 mm, 100 L/min) · <b>IP67</b> = inmersión temporal. Cada número es otra prueba.</div>",
    "IEC 60529 · Rolec, Info IP65 (EN 60529) · HellermannTyton, helaguard p.143 · bopla.de · newark.com", "ilustración propia")

# ===================================================================== C02 · Clase F 155 °C
f = Foto("p07_placa", 486, 300, w=544)
bx, by, bw = 130, 40, 110
esc = 3.4  # px por °C
y0 = 590
seg = [(40, "#9AA9C2", "40 °C", "ambiente"), (105, NAR, "105 K", "elevación"), (10, RJ, "10 K", "punto caliente")]
b, acc = [], 0
for v, c, t1, t2 in seg:
    h = v * esc
    yy = y0 - (acc + v) * esc
    b.append(R(bx, yy, bw, h, c, "#fff", 3, 4))
    b.append(T(bx + bw / 2, yy + h / 2, t1, 34 if h > 40 else 26, 900, "#fff", fam="Barlow C"))
    b.append(L(bx + bw + 8, yy + h / 2, bx + bw + 30, yy + h / 2, c, 3) + T(bx + bw + 36, yy + h / 2, t2, 20, 800, NAV, a="start"))
    acc += v
b.append(L(bx - 20, y0 - 155 * esc, bx + bw + 20, y0 - 155 * esc, NAV, 4))
b.append(T(bx - 30, y0 - 155 * esc, "155 °C", 40, 900, NAV, a="end", fam="Barlow C"))
b.append(L(bx - 20, y0, bx + bw + 20, y0, NAV, 3) + T(bx - 30, y0, "0 °C", 26, 800, GR, a="end", fam="Barlow C"))
barra = svg(40, 300, 420, 640, "".join(b))
x0, y0r = f.p(.585, .435)
x1, y1r = f.p(.94, .60)
resalta = (f"<svg style='left:0;top:0' width='1080' height='1350' viewBox='0 0 1080 1350'>"
           f"<rect x='{x0:.0f}' y='{y0r:.0f}' width='{x1 - x0:.0f}' height='{y1r - y0r:.0f}' rx='8' fill='none' stroke='#fff' stroke-width='9'/>"
           f"<rect x='{x0:.0f}' y='{y0r:.0f}' width='{x1 - x0:.0f}' height='{y1r - y0r:.0f}' rx='8' fill='none' stroke='{RJ}' stroke-width='5'/></svg>")
tabla = ("<div style='position:absolute;left:40px;right:40px;top:960px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px'>"
         + "".join(f"<div style='border-radius:16px;padding:10px 6px;text-align:center;background:{bg};color:{c}'>"
                   f"<div style='font:900 46px/1 \"Barlow C\"'>{k}</div><div style='font:800 26px \"Barlow C\"'>{v} °C</div>"
                   f"<div style='font:600 16px Montserrat;opacity:.9'>{r}</div></div>"
                   for k, v, r, bg, c in [("A", 105, "elev. 60 K", "#E9EEF6", NAV), ("E", 120, "—", "#E9EEF6", NAV),
                                          ("B", 130, "elev. 80 K", "#DCE7FA", NAV), ("F", 155, "elev. 105 K", NAR, "#fff"),
                                          ("H", 180, "elev. 125 K", "#E9EEF6", NAV)])
         + "</div>")
P["C02_clase_F"] = page(DID,
    head("MOTOR · AISLAMIENTO", NAR, "Clase <em>F</em>: ¿de dónde<br>salen los 155 °C?")
    + "<div class='pn' style='top:280px;height:660px'></div>" + barra + f.html() + resalta
    + "<div class='wc' style='left:486px;top:640px;width:530px'><b>En la placa: INS. CL F.</b> Es el máximo que aguanta el aislamiento del devanado. "
      "Muchos motores industriales traen aislamiento F pero trabajan con elevación de clase B (80 K): les queda margen y viven más.</div>"
    + tabla
    + "<div class='tx' style='top:1100px;font-size:23px'>Elevaciones para F.S. 1,0 y ambiente de 40 °C. Con F.S. 1,15 NEMA permite 10 K más (B 90 K, F 115 K).</div>",
    "NEMA, MG 1 vs IEC 60034 (tabla de clases) · Toshiba, Tech Notes Temperature Rise · ABB, How to read a NEMA nameplate · Engineering ToolBox",
    f"“Motor nameplate Malmbergs”, Olgailga2, CC0, {CC}")

# ===================================================================== C03 · Factor de servicio 1,15
f = Foto("p05_motor2", 560, 140, w=470)
P["C03_factor_servicio"] = page(BIG,
    "<div class='tag' style='left:50px;top:40px;background:#0B1220;color:#fff'>DATO CLAVE · PLACA NEMA</div>"
    "<div class='big' style='font-size:300px;top:110px'>1,15</div>"
    "<div class='t' style='top:400px;width:520px'>es el <em>factor de servicio</em> de muchos motores NEMA</div>"
    f"<div class='ph' style='left:{f.x - 8:.0f}px;top:{f.y - 8:.0f}px;width:{f.w + 16:.0f}px;height:{f.h + 16:.0f}px'><img src='../../posts3/fotos/p05_motor2.jpg'></div>"
    "<div class='sub2' style='top:600px'>Indica cuánta <b>sobrecarga continua</b> aguanta a tensión y frecuencia de placa: "
    "<b>hp × F.S.</b> Un motor de 10 hp con F.S. 1,15 llega a <b>11,5 hp</b>, pero trabaja más caliente y su vida esperada baja (NEMA MG 1, 9.15.1).</div>"
    "<div class='tb' style='top:750px'>"
    "<div><span>10 hp × 1,15</span><b>11,5 hp</b></div>"
    "<div><span>Con variador (Inverter / Vector Duty)</span><b>F.S. 1,0</b></div>"
    "<div><span>Arriba de 3300 ft (≈ 1000 m) de altitud</span><b>F.S. 1,0</b></div>"
    "<div><span>Motores IEC</span><b>NO USAN F.S.</b></div></div>"
    "<div class='nota' style='position:absolute;left:40px;right:40px;top:1080px;border-radius:18px;background:#0B1220;color:#fff;font:600 24px/1.32 Montserrat;padding:16px 24px'>En la Ciudad de Guatemala (≈ 1500 m) no cuentes con el 1,15: el aire enfría menos y el F.S. efectivo baja a <b style='color:#FFD400'>1,0</b>, salvo que el ambiente sea más frío o el fabricante diga otra cosa.</div>",
    "NEMA MG 1 · ABB/Baldor, placa NEMA (9AKK108388) y 9AKK106886 · NEMA, MG 1 vs IEC · ABB, How to read a NEMA nameplate · PetroWiki",
    f"“Cut-away version of an electric motor (1)”, S.J. de Waard, CC BY 2.5, {CC}")


# ===================================================================== C04 · Riel DIN TH35
def perfil(ox, oy, fondo, k=9.0, esp=1.0):
    """Perfil de sombrero visto de canto. oy = plano de montaje (pared). Escala k px/mm."""
    W, I = 35 * k, 27 * k
    xa, xb = ox + (W - I) / 2, ox + (W + I) / 2
    yt = oy - fondo * k
    e = esp * k
    pts = [(xa, oy), (xb, oy), (xb, yt), (ox + W, yt), (ox + W, yt - e), (xb - e, yt - e), (xb - e, oy - e),
           (xa + e, oy - e), (xa + e, yt - e), (ox, yt - e), (ox, yt), (xa, yt)]
    d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    s = f"<rect x='{ox - 40}' y='{oy}' width='{W + 80}' height='16' fill='#D5DCE8'/>"
    s += f"<polygon points='{d}' fill='#B9C2CF' stroke='{NAV}' stroke-width='2.5' stroke-linejoin='round'/>"
    s += cota_h(ox, ox + W, yt - e - 46, "35 mm")
    s += cota_h(xa, xb, oy + 48, "27 mm")
    s += f"<line x1='{ox + W}' y1='{yt - e}' x2='{ox + W + 50}' y2='{yt - e}' stroke='{GR}' stroke-width='2' stroke-dasharray='5 5'/>"
    s += cota_v(ox + W + 40, yt - e, oy, f"{str(fondo).replace('.', ',')} mm", NAR, 30)
    return s


r1 = svg(40, 296, 500, 390, T(250, 24, "TH 35-7,5", 40, 900, NAV, fam="Barlow C") + T(250, 60, "fondo normal", 21, 600, GR)
         + perfil(70, 310, 7.5))
r2 = svg(540, 296, 500, 390, T(250, 24, "TH 35-15", 40, 900, NAV, fam="Barlow C") + T(250, 60, "fondo profundo", 21, 600, GR)
         + perfil(70, 310, 15))
f = Foto("p10_iek", 712, 740, h=370)
P["C04_riel_din"] = page(DID,
    head("TABLERO · IEC 60715", TEAL, "Riel DIN: las <em>dos</em><br><em>medidas</em> de norma")
    + "<div class='pn' style='top:280px;height:430px'></div>" + r1 + r2
    + "<div class='wc' style='left:40px;top:740px;width:620px;height:370px'>"
      "<b style='font:900 34px \"Barlow C\";display:block;margin-bottom:8px'>LO QUE DICE LA NORMA</b>"
      "• Mismo ancho: <b>35 mm</b> por fuera y <b>27 mm</b> de base en la placa.<br>"
      "• Cambia el fondo: <b>7,5 mm</b> o <b>15 mm</b>.<br>"
      "• Perforado: ranuras de <b>15 × 6,2 mm</b> cada <b>25 mm</b>.<br>"
      "• Antes se llamaba DIN 46277-3 / EN 50022; hoy es <b>IEC/EN 60715</b>.<br>• Se fabrica en acero, aluminio y cobre.</div>"
    + f.html()
    + "<div class='nota' style='top:1140px'>El equipo se engancha en las alas de <b>35 mm</b>, iguales en los dos perfiles: lo que dice “riel TH35, EN 60715” entra en cualquiera.</div>",
    "IEC 60715:2017 · Phoenix Contact, NS 35/7,5 (0843103) y NS 35/15 (1207655) · Wikipedia, DIN rail · Rittal, rieles EN 60715",
    f"“Contactor DIN IEK”, Kae, CC BY-SA 3.0, {CC}")
# Nota: "entra en cualquiera de los dos" — el equipo se engancha en las alas de 35 mm, iguales en ambos perfiles.

# ===================================================================== C05 · Bobina 85–110 %
f = Foto("p01_contactor", 600, 130, w=430)
esc_v = 820 / 140  # px por voltio, escala 0–140 V
def vx(v):
    return 30 + v * esc_v
esq = []
esq.append(R(vx(0), 70, vx(140) - vx(0), 34, "#EEF2F8", "#CFD6E2", 2, 8))
esq.append(R(vx(24), 70, vx(90) - vx(24), 34, "#FFE2E2", RJ, 2, 6) + T((vx(24) + vx(90)) / 2, 87, "aquí debe soltar", 20, 800, RJ))
esq.append(R(vx(102), 70, vx(132) - vx(102), 34, "#DDF5E5", VER, 2, 6) + T((vx(102) + vx(132)) / 2, 87, "cierra firme", 20, 800, VER))
for v in (0, 24, 90, 102, 120, 132):
    esq.append(L(vx(v), 110, vx(v), 124, NAV, 3) + T(vx(v), 146, f"{v} V", 22, 800, NAV, fam="Barlow C"))
escala = svg(80, 940, 920, 170, "".join(esq))
P["C05_bobina_85"] = page(BIG,
    "<div class='tag' style='left:50px;top:40px;background:#0B1220;color:#fff'>DATO CLAVE · CONTACTOR</div>"
    "<div class='big' style='font-size:300px;top:110px'>85%</div>"
    "<div class='t' style='top:400px;width:540px'>de su tensión: con eso la <em>bobina</em> ya debe cerrar firme</div>"
    f"<div class='ph' style='left:{f.x - 8:.0f}px;top:{f.y - 8:.0f}px;width:{f.w + 16:.0f}px;height:{f.h + 16:.0f}px'><img src='../../posts3/fotos/p01_contactor.jpg'></div>"
    "<div class='sub2' style='top:600px'>La IEC 60947-4-1 prueba el contactor ya caliente: debe cerrar bien entre el <b>85&nbsp;% y el 110&nbsp;%</b> de su tensión de mando (Us). "
    "Y al quitar tensión debe soltar entre el <b>75&nbsp;% y el 20&nbsp;%</b> en CA (hasta 10&nbsp;% en CC).</div>"
    "<div class='tb' style='top:760px'>"
    "<div><span>Cierra (85–110 % Us)</span><b>102 a 132 V</b></div>"
    "<div><span>Suelta en CA (75–20 % Us)</span><b>90 a 24 V</b></div></div>"
    "<div class='sub2' style='top:930px;font-size:24px;font-weight:800;color:#0B1220'>Ejemplo con bobina de 120 V CA:</div>" + escala
    + "<div style='position:absolute;left:40px;right:40px;top:1130px;border-radius:18px;background:#0B1220;color:#fff;font:600 24px/1.32 Montserrat;padding:16px 24px'>Si el mando cae por debajo del <b style='color:#FFD400'>85&nbsp;%</b>, la norma ya no garantiza que cierre: mide la tensión en A1-A2 con el contactor energizado.</div>"
    + p4.rotulos(f, [dict(t='Bobina', s='electroimán', x=930, y=530, w=170, to=(.56, .62), c=RJ)]),
    "IEC 60947-4-1 · ENEC, guía de ensayos 60947-4-1 · Schneider, ficha TeSys D · ABB, catálogo Motor Protection and Control · CR4 GlobalSpec",
    f"“Telemecanique contactor”, Dmitry G, CC BY-SA 3.0, {CC}")

# ===================================================================== C06 · Sensor inductivo sa ≤ 0,81 sn
sx0, sxw = 300, 640  # eje 0 % → 125 %
def px(p):
    return sx0 + p / 125 * sxw
s = []
# sensor (cilindro roscado, sin símbolos)
s.append(R(40, 60, 230, 90, "#C7CED9", NAV, 3, 10))
for i in range(9):
    s.append(L(60 + i * 22, 62, 60 + i * 22, 148, "#9AA6B8", 3))
s.append(R(250, 66, 50, 78, "#2E8BFF", NAV, 3, 6))
s.append(T(155, 178, "sensor M12/M18…", 20, 700, GR))
for p in (0, 20, 40, 60, 81, 100, 120):
    s.append(L(px(p), 60, px(p), 560, "#E3E8F0", 2))
    s.append(T(px(p), 585, f"{p} %", 21, 800, NAV if p in (0, 81, 100) else GR, fam="Barlow C"))
filas = [("sn", "nominal", 100, 100, NAV), ("sr", "real (±10 %)", 90, 110, AZ), ("su", "útil (±10 % de sr)", 81, 121, TEAL), ("sa", "asegurada", 0, 81, VER)]
for i, (k, n, a, b2, c) in enumerate(filas):
    y = 220 + i * 85
    s.append(T(40, y, k, 40, 900, c, a="start", fam="Barlow C") + T(90, y, n, 20, 700, NAV, a="start"))
    if a == b2:
        s.append(L(px(a), y - 26, px(a), y + 26, c, 7))
    else:
        s.append(R(px(a), y - 20, px(b2) - px(a), 40, c, c, 0, 8))
        s.append(T((px(a) + px(b2)) / 2, y, f"{a}–{b2} %", 22, 900, "#fff", fam="Barlow C"))
grafico = svg(40, 290, 1000, 600, "".join(s))
P["C06_sensor_081"] = page(DID,
    head("SENSORES · IEC 60947-5-2", AZ, "Sensor de sn = 8 mm:<br>solo asegura <em>6,48 mm</em>")
    + "<div class='pn' style='top:280px;height:640px'></div>" + grafico
    + "<div class='cd' style='left:40px;top:945px;width:490px;background:#22A559'><b>sa ≤ 0,81 · sn</b>Monta el objeto dentro de esa distancia y detecta siempre, aun con temperatura y tensión en el peor caso. 0,81 = 0,9 × 0,9.</div>"
    + "<div class='cd' style='left:550px;top:945px;width:490px;background:#0B1F4D'><b>EJEMPLO REAL</b>SICK IHM06: sn = 2 mm → sa = 1,62 mm.<br>Uno de sn = 8 mm → sa = 6,48 mm.</div>"
    + "<div class='tx' style='top:1130px;font-size:22px'>sn se mide con una placa cuadrada de acero <b>Fe 360</b> de 1 mm: lado = diámetro de la cara del sensor o 3 · sn (el mayor). Con otro metal o un objeto más chico la distancia baja.</div>",
    "IEC 60947-5-2 · Pepperl+Fuchs, catálogo Sensors & Systems p.32 · Bernstein, A1 Inductive General · SICK, ficha IHM06-02BPSVT0S · pepperl-fuchs.com · baumer.com",
    "ilustración propia")

# ===================================================================== C07 · Colores IEC 60204-1
colores = [("NEGRO", "#111", "#fff", "Potencia en CA y CC", "fases que van al motor, salida de variadores"),
           ("ROJO", "#D7263D", "#fff", "Mando en CA", "bobinas, pulsadores y pilotos a 120/230 V CA"),
           ("AZUL", "#1446C8", "#fff", "Mando en CC", "24 V CC de PLC, sensores y relés"),
           ("NARANJA", "#FF8A00", "#111", "Circuitos exceptuados", "siguen con tensión aunque abras el seccionador"),
           ("AZUL CLARO", "#7EC8F5", "#0B1F4D", "Neutro (N)", "solo para el neutro si el color es la única marca"),
           ("VERDE-AMARILLO", "repeating-linear-gradient(115deg,#1FA34A 0 22px,#FFD400 22px 44px)", "#0B1F4D", "Protección (PE)", "exclusivo de tierra; nunca otra función")]
filas = []
for i, (n, bg, fc, t1, t2) in enumerate(colores):
    y = 290 + i * 140
    if "gradient" in bg:
        nom = f"<div style='position:absolute;left:84px;top:{y + 42}px;font:900 30px/1.2 \"Barlow C\";color:#0B1F4D;letter-spacing:1px;background:#fff;border-radius:8px;padding:0 8px'>{n}</div>"
    else:
        nom = f"<div style='position:absolute;left:90px;top:{y + 42}px;font:900 30px/1.2 \"Barlow C\";color:{fc};letter-spacing:1px'>{n}</div>"
    filas.append(f"<div style='position:absolute;left:40px;top:{y}px;width:1000px;height:120px;border-radius:20px;background:#F6FAFF;border:3px solid #CFE0F5'></div>"
                 f"<div style='position:absolute;left:70px;top:{y + 38}px;width:300px;height:44px;border-radius:22px;background:{bg};box-shadow:inset 0 -6px 0 rgba(0,0,0,.18),inset 0 6px 0 rgba(255,255,255,.25)'></div>"
                 f"<div style='position:absolute;left:370px;top:{y + 44}px;width:46px;height:32px;background:linear-gradient(#E9D6A8,#C49A45);border-radius:0 6px 6px 0'></div>"
                 + nom +
                 f"<div style='position:absolute;left:450px;top:{y + 18}px;width:570px'><div style='font:900 34px \"Barlow C\";color:#0B1F4D'>{t1}</div>"
                 f"<div style='font:500 21px Montserrat;color:#475467'>{t2}</div></div>")
P["C07_colores_60204"] = page(DID,
    head("TABLERO · IEC 60204-1", RJ, "¿De qué color va<br><em>cada cable</em>?")
    + "".join(filas)
    + "<div class='nota' style='top:1135px'>Son los colores <b>recomendados</b> para cables sueltos dentro del tablero. El <b>verde‑amarillo</b> es obligatorio para PE y no se usa en nada más.</div>",
    "IEC 60204-1 (13.2) · Siemens, Control Panels compliant with IEC (6.8.1) · PPMA/IET, Cable colours in machines · industrialmonitordirect.com · wevolver.com (Rowse)",
    "ilustración propia")

# ===================================================================== C08 · Punteras DIN 46228-4
pt = [("0,5", "20", "#F4F4F4", NAV), ("0,75", "18", "#9AA0A6", "#fff"), ("1", "18", "#D7263D", "#fff"),
      ("1,5", "16", "#111", "#fff"), ("2,5", "14", "#1446C8", "#fff"), ("4", "12", "#9AA0A6", "#fff"),
      ("6", "10", "#F2C500", NAV), ("10", "8", "#D7263D", "#fff"), ("16", "6", "#1446C8", "#fff")]


def puntera(c):
    return ("<svg width='170' height='70' viewBox='0 0 170 70' style='position:static'>"
            f"<path d='M10 12 h70 l22 10 v26 l-22 10 h-70 z' fill='{c}' stroke='#0B1F4D' stroke-width='3' stroke-linejoin='round'/>"
            "<rect x='100' y='24' width='62' height='22' rx='3' fill='#D9DEE6' stroke='#0B1F4D' stroke-width='2.5'/></svg>")


cards = "".join(
    f"<div style='background:#F6FAFF;border:3px solid #CFE0F5;border-radius:20px;padding:12px 14px;display:flex;flex-direction:column;align-items:center'>"
    f"{puntera(c)}<div style='font:900 44px/1 \"Barlow C\";color:#0B1F4D;margin-top:6px'>{m} mm²</div>"
    f"<div style='font:600 19px Montserrat;color:#475467'>≈ {a} AWG</div></div>" for m, a, c, _ in pt)
f = Foto("p06_punteras", 560, 255, w=470)
P["C08_punteras_din"] = page(DID,
    head("TABLERO · DIN 46228-4", TEAL, "El color de la<br><em>puntera</em> dice<br>su calibre")
    + f.html()
    + f"<div style='position:absolute;left:40px;right:40px;top:520px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px'>{cards}</div>"
    + "<div class='nota' style='top:1140px'>Ojo: el código <b>francés</b> (NF C 63-023) usa otros colores: ahí 2,5 mm² es <b>gris</b>, no azul. No mezcles marcas sin revisar.</div>",
    "DIN 46228-4 · Phoenix Contact, tabla de colores de punteras · Rapid, surtido 06-3117 (código DIN) · industrialmonitordirect.com · Bossard",
    f"“Wire ferrules with and without insulation”, Simon A. Eugster, CC BY-SA 3.0, {CC}")

# ===================================================================== C09 · NEC 240.4(D)
cab = []
for i, (awg, d, a90, ocpd) in enumerate([("14", 70, 25, 15), ("12", 88, 30, 20), ("10", 110, 40, 30)]):
    cx = 100 + i * 150
    cab.append(f"<circle cx='{cx}' cy='120' r='{d / 2 + 14}' fill='#1446C8' stroke='#0B1F4D' stroke-width='3'/>"
               f"<circle cx='{cx}' cy='120' r='{d / 2}' fill='#D9873A' stroke='#8A4B16' stroke-width='3'/>"
               + T(cx, 120, awg, 36, 900, "#fff", fam="Barlow C") + T(cx, 210, "AWG", 20, 800, NAV))
P["C09_nec_240_4D"] = page(BIG,
    "<div class='tag' style='left:50px;top:40px;background:#0B1220;color:#fff'>DATO CLAVE · NEC 240.4(D)</div>"
    "<div class='big' style='font-size:300px;top:110px'>20 A</div>"
    "<div class='t' style='top:400px;width:560px'>es el breaker máximo para un <em>12 AWG</em> de cobre</div>"
    + svg(560, 170, 460, 240, "".join(cab))
    + "<div class='sub2' style='top:600px'>Aunque la tabla 310.16 le da <b>30 A</b> a un 12 AWG THHN (columna 90 °C), la regla de <b>conductores pequeños</b> limita su protección. "
      "Los 90 °C sirven para aplicar factores de corrección, no para subir el breaker.</div>"
    "<div class='tb' style='top:760px'>"
    "<div><span>14 AWG Cu · tabla 90 °C: 25 A</span><b>MÁX. 15 A</b></div>"
    "<div><span>12 AWG Cu · tabla 90 °C: 30 A</span><b>MÁX. 20 A</b></div>"
    "<div><span>10 AWG Cu · tabla 90 °C: 40 A</span><b>MÁX. 30 A</b></div></div>"
    "<div style='position:absolute;left:40px;right:40px;top:1060px;border-radius:18px;background:#0B1220;color:#fff;font:600 24px/1.32 Montserrat;padding:16px 24px'>Se aplica <b style='color:#FFD400'>después</b> de corregir por temperatura y número de conductores, salvo las excepciones de 240.4(E) y (G).</div>",
    "NEC 2023, 240.4(D) y tabla 310.16 · Mike Holt, NEC cap. 240 y Conductor Sizing and Protection · EC&M, Conductor sizing part 1 · Encore Wire, ampacity table",
    "ilustración propia")

# ===================================================================== C10 · NEC 110.14(C)
e = []
e.append(R(30, 60, 190, 150, "#0B1F4D", NAV, 0, 16) + T(125, 105, "BREAKER", 24, 900, "#fff", fam="Barlow C") + T(125, 150, "borne 60 °C", 26, 900, "#FFD400", fam="Barlow C"))
e.append(R(740, 60, 190, 150, "#0B1F4D", NAV, 0, 16) + T(835, 105, "CONTACTOR", 24, 900, "#fff", fam="Barlow C") + T(835, 150, "borne 75 °C", 26, 900, "#7EE2A0", fam="Barlow C"))
e.append(f"<rect x='220' y='120' width='520' height='30' rx='15' fill='#111'/>")
e.append(T(480, 92, "THHN · aislamiento 90 °C", 24, 800, NAV))
e.append(f"<circle cx='125' cy='135' r='86' fill='none' stroke='{RJ}' stroke-width='6' stroke-dasharray='14 8'/>")
e.append(T(125, 250, "este manda", 24, 900, RJ))
esquema = svg(60, 300, 960, 280, "".join(e))
P["C10_nec_110_14C"] = page(DID,
    head("NEC · 110.14(C)", NAR, "El cable lo limita el<br><em>borne más débil</em>")
    + "<div class='pn' style='top:280px;height:310px'></div>" + esquema
    + "<div class='cd' style='left:40px;top:615px;width:490px;height:200px;background:#0B1F4D;font-size:22px'><b>≤ 100 A · 14 a 1 AWG</b>Columna de <b style='display:inline;font:800 22px Montserrat;color:#FFD400'>60 °C</b> de la tabla 310.16, salvo que el borne esté marcado 75 °C. Motores de diseño B, C o D: 75 °C.</div>"
    + "<div class='cd' style='left:550px;top:615px;width:490px;height:200px;background:#0057FF;font-size:22px'><b>&gt; 100 A · mayor que 1 AWG</b>Columna de <b style='display:inline;font:800 22px Montserrat;color:#FFD400'>75 °C</b> de la tabla 310.16. Igual: si un extremo tiene borne de menor temperatura, manda ese.</div>"
    + "<div class='wc' style='left:40px;top:845px;width:1000px;font-size:23px'><b style='font:900 34px \"Barlow C\";display:block'>EJEMPLO: CIRCUITO DE 50 A CON THHN</b>"
      "<div style='display:flex;gap:18px;margin-top:10px'>"
      "<div style='flex:1;background:#FFF1E0;border-radius:14px;padding:10px 14px'>Bornes de <b>60 °C</b> → <b>6 AWG</b> (55 A)</div>"
      "<div style='flex:1;background:#E3F6EA;border-radius:14px;padding:10px 14px'>Bornes de <b>75 °C</b> → <b>8 AWG</b> (50 A)</div></div>"
      "<div style='margin-top:10px;font-size:21px;color:#475467'>El 8 AWG THHN tiene 55 A en la columna de 90 °C, pero con bornes de 75 °C solo cuenta 50 A.</div></div>"
    + "<div class='nota' style='top:1110px'>La columna de <b>90 °C</b> solo sirve para aplicar factores de corrección y ajuste; la ampacidad final no puede pasar la columna del borne.</div>",
    "NEC 2023, 110.14(C)(1) · Eaton/Bussmann, Conductor ampacities · Mike Holt, Terminal ratings 110.14(C) · Schneider Electric, 0110DB9901 · EC&M",
    "ilustración propia")


if __name__ == "__main__":
    import sys
    sel = sys.argv[1:] or list(P)
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    for k in sel:
        (AQ / "html" / f"{k}.html").write_text(P[k], encoding="utf-8")
    subprocess.run(["node", "shot.js", *sel], cwd=AQ, check=True)
    print("ok", len(sel))

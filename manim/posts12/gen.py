"""Lote G (25-nov): equipos en 3D/foto real señalados.
G01–G05: modelos 3D de FreeCAD Parts Library (CC BY 3.0), convertidos STEP→GLB (lib/visor3d) y renderizados con three.js.
G06: contactor Siemens 3RT2015-1AP01 (render, STEP y dibujo de Siemens Industry Bilddatenbank).
G07: relé térmico CHINT NR2-25 9–13 A, fotos de larssystemgt.com/1347 (pedidas por el usuario).
Fuentes en referencias/loteG_fuentes.md."""
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


g11 = _load("g11", AQ.parent / "posts11" / "gen.py")
g = g11.g
page, kick, T, svg, tabla = g.page, g.kick, g.T, g.svg, g.tabla
DID = g.DID
NAV, AZ, TEAL, NAR, RJ, VER = g.NAV, g.AZ, g.TEAL, g.NAR, g.RJ, g.VER
lados = g11.lados


class Img(g.Img):
    def __init__(self, src, x, y, w=None, h=None):
        W, H = Image.open(AQ / "img" / f"{src}.png").size
        if w and not h:
            h = w * H / W
        if h and not w:
            w = h * W / H
        self.foto, self.src = False, f"../img/{src}.png"
        self.x, self.y, self.w, self.h = x, y, w, h


def marc(f, items, wl=230):
    """items: (n, fx, fy, título, sub, lx, ly). Etiqueta libre (lx = borde izq., ly = centro); línea punteada al punto."""
    sv, out = [], []
    for n, fa, fb, t, sub, lx, ly in items:
        px, py = f.p(fa, fb)
        ex = lx + wl + 6 if px > lx + wl else (lx - 6 if px < lx else px)
        ey = ly if (px > lx + wl or px < lx) else (ly + 34 if py > ly else ly - 34)
        sv.append(f"<polyline points='{ex},{ey} {px:.0f},{py:.0f}' fill='none' stroke='#fff' stroke-width='7' opacity='.9'/>"
                  f"<polyline points='{ex},{ey} {px:.0f},{py:.0f}' fill='none' stroke='#0057FF' stroke-width='3' stroke-dasharray='9 7'/>"
                  f"<circle cx='{px:.0f}' cy='{py:.0f}' r='9' fill='#0057FF' stroke='#fff' stroke-width='3'/>")
        out.append(f"<div style='position:absolute;left:{lx}px;top:{ly - 30}px;width:{wl}px;display:flex;gap:10px;align-items:center;"
                   f"background:rgba(255,255,255,.92);border-radius:14px;padding:4px 6px'>"
                   f"<div style='flex:none;width:44px;height:44px;border-radius:50%;background:#0057FF;color:#fff;font:800 21px Montserrat;"
                   f"display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.3)'>{n}</div>"
                   f"<div><div style='font:800 20px/1.1 Montserrat;color:#0B1F4D'>{t}</div><div style='font:500 15px/1.2 Montserrat;color:#475467'>{sub}</div></div></div>")
    return svg(0, 0, 1080, 1350, "".join(sv)) + "".join(out)


FC = "Modelo 3D: FreeCAD Parts Library ({a}), CC BY 3.0 · render @miguelesquit"


def chips(top, items, cols=None):
    cols = cols or len(items)
    return (f"<div style='position:absolute;left:40px;right:40px;top:{top}px;display:grid;grid-template-columns:repeat({cols},1fr);gap:12px'>"
            + "".join(f"<div style='background:#F6FAFF;border-top:6px solid {c};border-radius:14px;padding:10px 14px;font:500 17px/1.3 Montserrat;color:#1d2939'>"
                      f"<b style='display:block;font:900 30px/1.05 \"Barlow C\";color:{c}'>{t}</b>{d}</div>" for t, d, c in items)
            + "</div>")


def nota(top, html, color="#0B1F4D"):
    return f"<div class='nota' style='top:{top}px;padding:12px 22px;font-size:20px;background:{color}'>{html}</div>"


P = {}

# ===================================================================== G01 · Paro de emergencia LAY37
f = Img("estop", 330, 320, h=700)
P["G01_paro_emergencia"] = page(DID,
    kick("PARO DE EMERGENCIA · 22 mm", RJ) + T("Las partes del", "paro de emergencia", RJ, sub="Tipo LAY37 · hongo Ø40 mm · 1NA + 1NC", size=60)
    + f.html() + lados(f, [
        (1, .50, .06, "Hongo rojo", "empujar = enclava", "i", 380),
        (2, .50, .24, "Vástago", "gira para liberar", "i", 500),
        (3, .30, .36, "Aro de fijación", "rosca al panel Ø22 mm", "i", 620),
        (4, .12, .80, "Bornes", "tornillo, 4 terminales", "i", 800),
        (5, .84, .40, "Placa amarilla", "fondo del hongo", "d", 470),
        (6, .66, .60, "Cuerpo", "detrás del tablero", "d", 640),
        (7, .80, .80, "Bloques de contacto", "1NA + 1NC", "d", 800)])
    + chips(1060, [("ROJO / AMARILLO", "Actuador rojo sobre fondo amarillo (IEC 60204-1, ISO 13850).", RJ),
                   ("SE QUEDA ENCLAVADO", "Hasta girarlo; la máquina no arranca sola al soltar.", NAR),
                   ("NC DE APERTURA DIRECTA", "El NC abre por fuerza mecánica (IEC 60947-5-5).", AZ)])
    + nota(1185, "El <b>NC</b> va en serie con la bobina del contactor: al presionar, corta el mando aunque el contacto esté soldado."),
    "IEC 60204-1 · ISO 13850 · IEC 60947-5-5 · ficha LAY37-11ZS (1NA+1NC, 10 A, 660 V, montaje 22 mm)",
    FC.format(a="AngelLM"))

# ===================================================================== G02 · Pulsador verde 22 mm
f = Img("pbv", 170, 470, w=820)
P["G02_pulsador_verde"] = page(DID,
    kick("PULSADOR 22 mm", VER) + T("Así es un", "pulsador", VER, sub="Pulsador rasante verde de marcha, con bloques de contacto", size=66)
    + f.html() + marc(f, [
        (1, .10, .66, "Botón", "rasante, vuelve por resorte", 40, 960),
        (2, .25, .30, "Bisel frontal", "asienta en el tablero", 60, 340),
        (3, .40, .70, "Anillo de fijación", "aprieta por detrás", 330, 1000),
        (4, .55, .14, "Adaptador", "une operador y bloques", 380, 340),
        (5, .80, .30, "Bloques de contacto", "NA 3-4 · NC 1-2", 790, 340),
        (6, .86, .62, "Bornes", "tornillo, por detrás", 790, 960)])
    + chips(1080, [("Ø22,3 mm", "Agujero del tablero (EAO, Omron, Eaton).", AZ),
                   ("MOMENTÁNEO", "Cierra solo mientras se presiona.", NAR),
                   ("VERDE = MARCHA", "Permitido; IEC 60204-1 prefiere blanco. Nunca rojo.", VER)])
    + nota(1195, "Detrás se <b>apilan</b> los bloques: cada uno agrega un NA o un NC al mismo botón."),
    "IEC 60204-1 (colores) · IEC 60947-5-1 (bloques de contacto, AC-15) · catálogos EAO 45, Omron A22NN, Eaton RMQ-Titan",
    FC.format(a="Henrique Enzweiler"))

# ===================================================================== G03 · Pulsador tipo hongo rojo (no es emergencia)
f = Img("seta", 170, 450, w=820)
P["G03_hongo_rojo"] = page(DID,
    kick("PULSADOR TIPO HONGO · 22 mm", RJ) + T("Hongo rojo", "no es emergencia", RJ, sub="Se parece al paro de emergencia, pero no lo sustituye", size=60)
    + f.html() + marc(f, [
        (1, .10, .55, "Cabeza de hongo", "fácil de golpear", 40, 330),
        (2, .40, .72, "Anillo de fijación", "panel Ø22 mm", 330, 990),
        (3, .55, .14, "Adaptador", "mismo sistema 22 mm", 420, 330),
        (4, .80, .30, "Bloques de contacto", "NC 1-2 para paro", 790, 330),
        (5, .86, .62, "Bornes", "tornillo", 790, 990)])
    + "<div style='position:absolute;left:40px;right:40px;top:1080px;display:grid;grid-template-columns:1fr 1fr;gap:14px'>"
      "<div style='background:#FFF1F1;border:3px solid #E5383B;border-radius:16px;padding:10px 16px;font:500 18px/1.3 Montserrat'><b style='display:block;font:900 30px \"Barlow C\";color:#E5383B'>ESTE HONGO</b>Momentáneo: al soltarlo vuelve. Sirve como paro normal (rojo permitido, IEC 60204-1).</div>"
      "<div style='background:#FFF8D6;border:3px solid #E0A800;border-radius:16px;padding:10px 16px;font:500 18px/1.3 Montserrat'><b style='display:block;font:900 30px \"Barlow C\";color:#B98900'>PARO DE EMERGENCIA</b>Debe enclavar, tener fondo amarillo y NC de apertura directa (ISO 13850, IEC 60947-5-5).</div></div>"
    + nota(1205, "Para paro normal sirve; para <b>emergencia</b> usa el hongo que enclava sobre fondo amarillo."),
    "IEC 60204-1 · ISO 13850 · IEC 60947-5-5 · catálogo EAO 45 (hongo Ø30/40/60 mm)",
    FC.format(a="Henrique Enzweiler"))

# ===================================================================== G04 · Fuente conmutada por dentro
fi = Img("psu_in", 250, 300, h=640)
P["G04_fuente_conmutada"] = page(DID,
    kick("FUENTE CONMUTADA · 24 VDC", AZ) + T("Así es una fuente", "por dentro", AZ, sub="De 120/230 VAC a 24 VDC para PLC, sensores y relés", size=58)
    + fi.html() + marc(fi, [
        (1, .18, .55, "Bornera", "L · N · ⏚ · −V · +V", 30, 560),
        (6, .34, .48, "Placa electrónica", "conmuta a alta frecuencia", 30, 850),
        (5, .87, .25, "Ventilador", "enfría al cargar", 810, 360),
        (4, .66, .33, "Capacitores", "filtran la tensión", 810, 500),
        (3, .57, .50, "Transformador", "de alta frecuencia", 810, 650),
        (2, .47, .58, "Bobina toroidal", "filtro", 810, 800)])
    + tabla(955, [("Salida", "24 VDC · 14,6 A · 350 W"), ("Ajuste V.ADJ", "21,6 – 28,8 V"), ("Entrada", "115 / 230 VAC por selector")],
            cab="<span>EJEMPLO REAL · MEAN WELL LRS-350-24</span>", extra="font-size:19px")
    + nota(1200, "Protegida contra corto, sobrecarga, sobretensión y temperatura. El mando de 24 VDC va en <b>azul</b> (IEC 60204-1)."),
    "Mean Well, LRS-350 (hoja de datos y catálogo industrial) · IEC 60204-1 · el modelo 3D es genérico, los datos son de ejemplo",
    FC.format(a="Henrique Enzweiler"))

# ===================================================================== G05 · Sensor inductivo
f = Img("ind", 280, 380, w=760)
P["G05_sensor_inductivo"] = page(DID,
    kick("SENSOR INDUCTIVO", TEAL) + T("Las partes del", "sensor inductivo", TEAL, sub="Detecta metal sin tocarlo · 3 hilos PNP/NPN", size=60)
    + f.html() + marc(f, [
        (1, .08, .82, "Cara activa", "aquí sale el campo", 30, 880),
        (2, .30, .79, "LED", "enciende al detectar", 30, 740),
        (3, .38, .60, "Cabezal", "bobina y oscilador", 30, 600),
        (4, .66, .40, "Cuerpo", "M12 / M18 roscado", 330, 330),
        (5, .95, .14, "Cable o conector", "salida de 3 hilos", 640, 330)])
    + "<div style='position:absolute;left:40px;right:40px;top:960px;display:flex;gap:10px'>"
    + "".join(f"<div style='flex:1;border-radius:12px;padding:10px 12px;background:{bg};color:{fg};font:900 26px \"Barlow C\";text-align:center'>{t}<div style='font:600 14px Montserrat'>{d}</div></div>"
              for t, d, bg, fg in (("BN", "café · +V", "#7B4A2A", "#fff"), ("BU", "azul · 0 V", "#1D4ED8", "#fff"), ("BK", "negro · salida", "#111", "#fff")))
    + "</div>"
    + tabla(1060, [("Alcance M12 enrasado / no enrasado", "2 mm / 4 mm"), ("Detecta", "solo metales"), ("Colores de hilos", "IEC 60947-5-2")],
            cab="<span>DATOS CLAVE</span>", extra="font-size:19px"),
    "IEC 60947-5-2 · Pepperl+Fuchs y Omron (alcance nominal Sn M12) · el modelo 3D es genérico",
    FC.format(a="fran6t"))

# ===================================================================== G06 · Contactor Siemens 3RT2015-1AP01
f = Img("sie_foto", 300, 330, h=560)
d = Img("sie_dim", 40, 960, w=600)
P["G06_contactor_siemens"] = page(DID,
    kick("CONTACTOR · SIEMENS SIRIUS", TEAL) + T("Contactor", "3RT2015-1AP01", TEAL, sub="7 A AC-3 · 3 kW a 400 V · bobina 230 VAC · 1NA · tamaño S00", size=60)
    + f.html() + marc(f, [
        (1, .193, .432, "Entradas 1/L1 3/L2 5/L3", "de la protección", 30, 420),
        (2, .247, .634, "Indicador de maniobra", "muestra si cerró", 30, 640),
        (3, .193, .848, "Salidas 2/T1 4/T2 6/T3", "al motor", 30, 860),
        (7, .408, .057, "Agujeros de fijación", "o riel DIN 35 mm", 800, 330),
        (4, .429, .432, "Auxiliar 13NO-14NO", "autoenclavamiento", 800, 480),
        (5, .55, .464, "Bobina A1", "230 VAC 50/60 Hz", 800, 620),
        (6, .55, .889, "Bobina A2", "abajo a la derecha", 800, 840)])
    + d.html()
    + "<div style='position:absolute;left:660px;top:960px;width:380px'>"
    + chips(0, [("45 × 57,5 × 73 mm", "Ancho × alto × fondo (dibujo Siemens).", AZ), ("Ø5 · 35 × 50 mm", "Tornillos de fijación.", NAR)], cols=1).replace("left:40px;right:40px;top:0px", "left:0;right:0;top:0")
    + "</div>"
    + nota(1180, "Mismo orden de bornes que el diagrama: entra arriba (1-3-5), sale abajo (2-4-6); bobina A1-A2 a la derecha."),
    "Siemens SiePortal, 3RT2015-1AP01 · Siemens Industry Bilddatenbank (render G_NSA0_XX_00822, dibujo G_NSA0_XX_00821, STEP G_NSA0_XX_00834)",
    "Imagen y dibujo: Siemens AG (Industry Bilddatenbank, uso gratuito)")

# ===================================================================== G07 · NR2-25 foto real
f = Img("nr2_f1", 280, 320, w=520)
f2 = Img("nr2_f2", 830, 845, h=190)
P["G07_nr2_foto_real"] = page(DID,
    kick("RELÉ TÉRMICO · CHINT NR2-25", NAR) + T("El relé térmico", "real", NAR, sub="NR2-25 · 9–13 A · clase 10A · se enchufa bajo el contactor", size=62)
    + f.html() + f2.html() + marc(f, [
        (1, .44, .10, "Pines de cobre", "entran al contactor", 30, 360),
        (2, .33, .41, "Dial 9–13 A", "corriente de placa", 30, 480),
        (3, .29, .54, "TEST", "simula el disparo", 30, 600),
        (4, .36, .67, "98 NO 97", "piloto de falla", 30, 720),
        (5, .45, .87, "2/T1 4/T2 6/T3", "salida al motor", 30, 840),
        (7, .68, .51, "RESET H / A", "manual o automático", 820, 560),
        (6, .56, .55, "STOP", "abre 95-96", 820, 660),
        (8, .64, .67, "96 NC 95", "en serie con la bobina", 820, 760)])
    + "<div style='position:absolute;left:830px;top:1040px;width:210px;font:700 14px Montserrat;color:#475467;text-align:center'>vista lateral</div>"
    + chips(1075, [("CLASE 10A", "Dispara en 2 a 10 s a 7,2 × Ir.", RJ), ("1NA + 1NC", "AC-15 2,73 A a 220 V.", AZ), ("FALTA DE FASE", "También dispara.", NAR)])
    + nota(1190, "Ajusta el dial a la <b>corriente de placa</b> del motor; el cortocircuito lo corta el fusible o el breaker."),
    "CHINT, NR2 Thermal Overload Relay (PDF) · CHINT NR2 User Instruction · IEC 60947-4-1",
    "LARSSYSTEM Guatemala (larssystemgt.com/1347), usadas a pedido del autor")

if __name__ == "__main__":
    import sys
    sel = sys.argv[1:] or list(P)
    for k in sel:
        (AQ / "html" / f"{k}.html").write_text(P[k], encoding="utf-8")
    subprocess.run(["node", "shot.js", *sel], cwd=AQ, check=True)
    print("ok", len(sel))

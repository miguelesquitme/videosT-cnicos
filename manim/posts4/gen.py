"""Publicaciones v4 (25-nov): estilo de las referencias del usuario (Suiler / electricistapro).
Sin cuadrícula, título grande que dice lo que enseña, foto REAL con rótulos señalados (línea + punto),
sin saturar. Fotos de Wikimedia Commons en ../posts3/fotos (crédito al pie). 1080 × 1350."""
import subprocess
from pathlib import Path
from PIL import Image

AQ = Path(__file__).parent
FOT = AQ.parent / "posts3" / "fotos"
NAV, AZ, AZ2, ROJO = "#0B1F4D", "#1565C0", "#0D47A1", "#E53935"
CC = "Wikimedia Commons"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Montserrat,sans-serif;color:#111827;
 background:linear-gradient(165deg,#F9FAFC 0%,#EEF2F7 55%,#E6ECF4 100%)}
.dec{position:absolute;border-radius:18px;background:#C9D8F2;opacity:.35}
.wave{position:absolute;left:-200px;width:1500px;height:420px;border-radius:50%;border:2px solid rgba(255,255,255,.9)}
.tit{position:absolute;left:30px;right:30px;text-align:center;text-transform:uppercase;line-height:1.02}
.t1{font-weight:900;color:#0B1F4D;letter-spacing:-.5px}
.t3{font-weight:900;color:#fff;-webkit-text-stroke:3px #1565C0;paint-order:stroke fill;letter-spacing:-.5px;
 text-shadow:0 3px 0 #1565C0,0 6px 0 #0D47A1,0 9px 0 #0B3C8C,0 14px 18px rgba(11,31,77,.35)}
.pill{display:inline-block;background:linear-gradient(180deg,#1E88E5,#1565C0);color:#fff;font-weight:900;border-radius:22px;padding:6px 34px 10px;
 box-shadow:0 8px 18px rgba(21,101,192,.35)}
.sub{position:absolute;left:60px;right:60px;background:rgba(255,255,255,.85);border:2px solid #D3DCEA;border-radius:24px;padding:16px 26px;
 font-size:25px;line-height:1.32;text-align:center;font-weight:500;box-shadow:0 6px 16px rgba(11,31,77,.08)}
.sub b{font-weight:800}
.card{position:absolute;border-radius:24px;overflow:hidden;background:#fff;border:6px solid #fff;box-shadow:0 14px 34px rgba(11,31,77,.22)}
.card img{width:100%;height:100%;object-fit:cover;display:block}
svg.ov{position:absolute;left:0;top:0;width:1080px;height:1350px;pointer-events:none}
.lab{position:absolute;transform:translate(-50%,-50%);background:#fff;border:3.5px solid;border-radius:14px;padding:8px 12px;
 font-size:21px;font-weight:700;text-align:center;line-height:1.18;box-shadow:0 4px 10px rgba(0,0,0,.12)}
.lab small{display:block;font-size:16px;font-weight:500;color:#475467;margin-top:2px}
.pie{position:absolute;left:40px;right:40px;bottom:14px;text-align:center}
.pie .m{display:flex;justify-content:center;align-items:center;gap:12px;font-weight:800;font-size:28px;color:#0B1F4D;letter-spacing:1px}
.pie .m img{height:46px}
.pie .f{font-size:13.5px;color:#667085;line-height:1.3;margin-top:6px}
.box{position:absolute;border-radius:20px;background:rgba(255,255,255,.9);border:2px solid #D3DCEA;box-shadow:0 6px 16px rgba(11,31,77,.08)}
.chip{position:absolute;transform:translate(-50%,-50%);background:#1E88E5;color:#fff;font-weight:800;border-radius:14px;padding:8px 18px;font-size:22px}
.bar{position:absolute;left:40px;right:40px;background:#0B1F4D;color:#fff;border-radius:18px;text-align:center;font-weight:700;font-size:25px;padding:14px 20px}
.bar b{color:#FFC94D}
"""


def deco():
    return ("<div class='wave' style='top:520px;transform:rotate(-8deg)'></div><div class='wave' style='top:880px;transform:rotate(-12deg)'></div>"
            "<div class='dec' style='left:-40px;top:40px;width:150px;height:300px'></div>"
            "<div class='dec' style='left:60px;top:-40px;width:150px;height:150px;opacity:.25'></div>"
            "<div class='dec' style='right:-50px;bottom:120px;width:170px;height:330px'></div>"
            "<div class='dec' style='right:80px;bottom:-60px;width:180px;height:180px;opacity:.25'></div>")


def page(cuerpo, fuentes, foto_cred):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{deco()}{cuerpo}"
            f"<div class='pie'><div class='m'><img src='../../logo_oficial.png'>@miguelesquit</div>"
            f"<div class='f'><b>Fuentes:</b> {fuentes} · <b>Foto:</b> {foto_cred}</div></div></body></html>")


def titulo(l1, l2, top=46, s1=60, s2=88, estilo="t3"):
    if estilo == "pill":
        b = f"<div style='margin-top:10px'><span class='pill' style='font-size:{s2}px'>{l2}</span></div>"
    else:
        b = f"<div class='t3' style='font-size:{s2}px;margin-top:6px'>{l2}</div>"
    return f"<div class='tit' style='top:{top}px'><div class='t1' style='font-size:{s1}px'>{l1}</div>{b}</div>"


def sub(t, top):
    return f"<div class='sub' style='top:{top}px'>{t}</div>"


class Foto:
    def __init__(self, src, x, y, w=None, h=None):
        W, H = Image.open(FOT / f"{src}.jpg").size
        if w and not h:
            h = w * H / W
        if h and not w:
            w = h * W / H
        self.src, self.x, self.y, self.w, self.h = src, x, y, w, h

    def p(self, fx, fy):
        return self.x + fx * self.w, self.y + fy * self.h

    def html(self):
        return (f"<div class='card' style='left:{self.x - 6:.0f}px;top:{self.y - 6:.0f}px;width:{self.w + 12:.0f}px;height:{self.h + 12:.0f}px'>"
                f"<img src='../../posts3/fotos/{self.src}.jpg'></div>")


def rotulos(f, items):
    """items: dict(t, s=sub, x, y, w, to=(fx,fy), rect=(fx0,fy0,fx1,fy1), c=color, modo='e'|'d')"""
    svg, labs = [], []
    for it in items:
        c = it.get("c", ROJO)
        lx, ly, lw = it["x"], it["y"], it.get("w", 250)
        lh = it.get("h", 62 if not it.get("s") else 82)
        if it.get("rect"):
            x0, y0 = f.p(*it["rect"][:2]); x1, y1 = f.p(*it["rect"][2:])
            svg.append(f"<rect x='{x0:.0f}' y='{y0:.0f}' width='{x1 - x0:.0f}' height='{y1 - y0:.0f}' rx='8' fill='none' stroke='#fff' stroke-width='8' opacity='.8'/>"
                       f"<rect x='{x0:.0f}' y='{y0:.0f}' width='{x1 - x0:.0f}' height='{y1 - y0:.0f}' rx='8' fill='none' stroke='{c}' stroke-width='4'/>")
        tx, ty = f.p(*it["to"])
        L, R, T, B = lx - lw / 2, lx + lw / 2, ly - lh / 2, ly + lh / 2
        if it.get("modo") == "d":
            sx = L if tx < L else R if tx > R else lx
            sy = ly if (tx < L or tx > R) else (T if ty < T else B)
            pts = [(sx, sy), (tx, ty)]
        elif tx < L or tx > R:
            sx = L if tx < L else R
            pts = [(sx, ly), (tx, ly), (tx, ty)]
        else:
            sy = T if ty < T else B
            pts = [(tx if L < tx < R else lx, sy), (tx, ty)]
        d = " ".join(f"{a:.0f},{b:.0f}" for a, b in pts)
        svg.append(f"<polyline points='{d}' fill='none' stroke='#fff' stroke-width='7' stroke-linejoin='round' opacity='.85'/>"
                   f"<polyline points='{d}' fill='none' stroke='{c}' stroke-width='3.5' stroke-linejoin='round'/>"
                   f"<circle cx='{tx:.0f}' cy='{ty:.0f}' r='9' fill='{c}' stroke='#fff' stroke-width='3.5'/>")
        s = f"<small>{it['s']}</small>" if it.get("s") else ""
        labs.append(f"<div class='lab' style='left:{lx}px;top:{ly}px;width:{lw}px;border-color:{c}'>{it['t']}{s}</div>")
    return f"<svg class='ov' viewBox='0 0 1080 1350'>{''.join(svg)}</svg>{''.join(labs)}"


P = {}

# 1 · guardamotor (vista frontal)
f = Foto("p09_mpcb", 330, 410, h=750)
R, A = ROJO, AZ
P["01_partes_guardamotor"] = page(
    titulo("Partes de un", "guardamotor") +
    sub("Protege al motor contra <b>sobrecarga</b> y <b>cortocircuito</b> en un solo aparato. Vista frontal de un Siemens 3RV2 de 0,55–0,8 A.", 238) +
    f.html() + rotulos(f, [
        dict(t="Contactos auxiliares", s="13-14 y 23-24 (NA)", x=165, y=540, to=(.03, .20), rect=(.03, .12, .97, .27), c=A),
        dict(t="Dial de ajuste", s="corriente del motor (Ir)", x=165, y=690, to=(.17, .39), c=R),
        dict(t="Clase 10 · I&gt; 10 A", s="disparo térmico y magnético", x=165, y=840, to=(.02, .53), rect=(.02, .47, .32, .59), c=A),
        dict(t="Botón TEST", s="simula el disparo", x=165, y=990, to=(.13, .605), c=R),
        dict(t="Mando giratorio", s="ON · OFF · TRIPPED", x=915, y=620, to=(.60, .47), c=R),
        dict(t="Etiqueta de designación", s="-QB001 en el tablero", x=915, y=800, to=(.62, .70), c=A),
        dict(t="Referencia", s="3RV2011-0HA10", x=915, y=960, to=(.87, .77), c=R),
        dict(t="Bornes de salida", s="2/T1 · 4/T2 · 6/T3", x=915, y=1110, to=(.92, .91), rect=(.08, .83, .92, .99), c=A)]),
    "Siemens, ficha 3RV2011-0HA10 y manual SIRIUS 3RV2 · IEC 60947-2 · IEC 60947-4-1",
    f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0, {CC}")

# 2 · relé térmico (vista frontal)
f = Foto("p04_rele_c", 262, 410, h=750)
ox, oy, sx, sy = .28, .07, .46, .81
g = lambda fx, fy: ((fx - ox) / sx, (fy - oy) / sy)
P["02_partes_rele_termico"] = page(
    titulo("Partes del", "relé térmico") +
    sub("Se enchufa bajo el contactor y lo abre si el motor se <b>sobrecarga</b> o le <b>falta una fase</b>. GE MT03N de 7,5–10,5 A.", 238) +
    f.html() + rotulos(f, [
        dict(t="Dial de ajuste", s="7,5 a 10,5 A", x=150, y=560, w=230, to=g(.43, .27), c=R),
        dict(t="Bornes de salida", s="2/T1 · 4/T2 · 6/T3", x=150, y=740, w=230, to=g(.33, .46), rect=(*g(.33, .37), *g(.54, .55)), c=A),
        dict(t="Borne 14/22", s="paso de auxiliares", x=150, y=930, w=230, to=g(.38, .635), c=R),
        dict(t="Pines de entrada", s="se enchufan al contactor", x=930, y=480, w=230, to=g(.57, .16), c=A),
        dict(t="Pin a A2", s="de la bobina", x=930, y=610, w=230, to=g(.69, .25), c=R),
        dict(t="Reset H / A", s="manual o automático", x=930, y=735, w=230, to=g(.62, .38), c=A),
        dict(t="Botón STOP", s="abre el 95-96", x=930, y=860, w=230, to=g(.575, .47), c=R),
        dict(t="Contacto NC 95-96", s="en serie con la bobina", x=930, y=990, w=230, to=g(.52, .67), c=A)]),
    "GE, catálogo C-2000 Mini-Contactors (relé MT03) · IEC 60947-4-1 (relés de sobrecarga) · NEC 2020 430.32",
    f"“GE MTO3N”, Dmitry G, CC BY-SA 3.0, {CC}")

# 3 · contactor por dentro
f = Foto("p01_contactor", 40, 400, w=1000)
P["03_contactor_por_dentro"] = page(
    titulo("Así es un contactor", "por dentro", s1=58) +
    sub("Al energizar la <b>bobina A1-A2</b>, el núcleo atrae la armadura y el portacontactos <b>cierra los contactos</b>. El resorte los abre al quitar la tensión.", 238) +
    f.html() + rotulos(f, [
        dict(t="Carcasa", s="contactos fijos y bornes", x=300, y=470, w=250, to=(.28, .29), rect=(.17, .29, .39, .64), c=A),
        dict(t="Portacontactos", s="puentes móviles", x=600, y=470, w=240, to=(.545, .29), rect=(.45, .29, .64, .44), c=R),
        dict(t="Carcasa", s="lado opuesto", x=880, y=470, w=220, to=(.83, .28), rect=(.72, .28, .94, .64), c=A),
        dict(t="Bobina A1-A2", s="crea el campo magnético", x=880, y=920, w=270, to=(.63, .55), rect=(.48, .47, .63, .63), c=R),
        dict(t="Resorte de retorno", s="abre al desenergizar", x=880, y=1040, w=270, to=(.64, .755), rect=(.52, .67, .64, .84), c=A),
        dict(t="Núcleo fijo en E", s="chapa laminada", x=270, y=1090, w=270, to=(.48, .915), rect=(.48, .85, .70, .98), c=R)]),
    "IEC 60947-4-1 (contactores) · Schneider Electric, guía TeSys D · Siemens, manual SIRIUS 3RT2",
    f"“Telemecanique contactor”, Dmitry G, CC BY-SA 3.0, {CC}")

# 4 · termomagnético por dentro
f = Foto("p03_mcb", 170, 410, w=740)
P["04_termomagnetico_por_dentro"] = page(
    titulo("Así es un termomagnético", "por dentro", s1=50) +
    sub("Tiene <b>dos disparadores</b>: el <b>térmico</b> (bimetal) para la sobrecarga y el <b>magnético</b> (bobina) para el cortocircuito.", 238) +
    f.html() + rotulos(f, [
        dict(t="Palanca", s="ON / OFF", x=150, y=450, w=220, to=(.51, .12), c=A),
        dict(t="Borne de conexión", x=150, y=690, w=220, to=(.27, .52), c=R),
        dict(t="Cámara de extinción", s="apaga el arco", x=150, y=960, w=220, to=(.55, .74), modo="d", c=A),
        dict(t="Clip de riel DIN", x=330, y=1120, w=220, to=(.31, .875), c=R),
        dict(t="Mecanismo de disparo", x=930, y=520, w=220, to=(.62, .29), c=R),
        dict(t="Bimetal", s="disparo térmico", x=930, y=690, w=220, to=(.74, .50), c=A),
        dict(t="Bobina", s="disparo magnético", x=930, y=860, w=220, to=(.565, .50), modo="d", c=R)]),
    "IEC 60898-1 (interruptores automáticos) · IEK, ficha VA47 C40 · ABB, guía técnica de interruptores modulares",
    f"“Circuit breaker structure ON”, Kae, CC BY-SA 3.0, {CC}")

# 5 · motor por dentro
f = Foto("p02_motor", 262, 420, w=790)
P["05_motor_por_dentro"] = page(
    titulo("Así es un motor trifásico", "por dentro", s1=50) +
    sub("El <b>estator</b> crea un campo magnético giratorio y el <b>rotor de jaula</b> lo sigue, un poco más lento: eso es el <b>deslizamiento</b>.", 238) +
    f.html() + rotulos(f, [
        dict(t="Caja de bornes", x=140, y=470, w=230, to=(.32, .14), c=A),
        dict(t="Devanado del estator", x=140, y=600, w=230, to=(.255, .355), c=R),
        dict(t="Eje", x=140, y=715, w=230, to=(.07, .455), c=A),
        dict(t="Rodamiento", x=140, y=830, w=230, to=(.195, .50), c=R),
        dict(t="Carcasa con aletas", x=140, y=990, w=230, to=(.33, .76), c=A),
        dict(t="Rotor de jaula", x=930, y=470, w=230, to=(.50, .43), modo="d", c=R),
        dict(t="Ventilador", x=930, y=640, w=230, to=(.88, .56), c=A),
        dict(t="Núcleo del estator", s="chapa laminada", x=640, y=1150, w=280, to=(.47, .66), c=R)]),
    "IEC 60034-1 (máquinas rotativas) · ABB, catálogo de motores de baja tensión · Technisches Museum Wien (modelo en corte)",
    f"“TMW 50906 Schnittmodell einer Drehstrommaschine”, dominio público, {CC}")

# 6 · ¿sabías qué? motores y electricidad
f = Foto("p05_motor2", 160, 470, w=760)
stats = [("&gt; 40 %", "IEA, 2011"), ("&gt; 45 %", "ABB"), ("53 %", "IEA 4E, 2025")]
P["06_sabias_motores"] = page(
    titulo("¿Sabías que los motores usan", "casi la mitad", s1=44) +
    "<div class='tit t1' style='top:252px;font-size:40px'>de toda la electricidad del mundo?</div>" +
    f.html() +
    "".join(f"<div class='box' style='left:{60 + i * 330}px;top:1060px;width:300px;height:120px;text-align:center;padding-top:12px'>"
            f"<div style='font-size:46px;font-weight:900;color:{AZ}'>{a}</div><div style='font-size:19px;font-weight:600;color:#475467'>{b}</div></div>"
            for i, (a, b) in enumerate(stats)) +
    "<div class='bar' style='top:330px;font-size:22px;background:rgba(255,255,255,.88);color:#111827;border:2px solid #D3DCEA'>"
    "Bombas, ventiladores, compresores y bandas: los <b style='color:#1565C0'>sistemas accionados por motor</b>. Por eso un motor IE3/IE4 bien dimensionado ahorra tanto.</div>",
    "IEA, “Energy-Efficiency Policy Opportunities for Electric Motor-Driven Systems” (2011) · ABB, “Energy efficiency” · IEA 4E EMSA, Policy Brief (2025)",
    f"“Cut-away version of an electric motor (1)”, S.J. de Waard, CC BY 2.5, {CC}")

# 7 · ¿sabías qué? punteras
f = Foto("p06_punteras", 40, 470, w=1000)
cols = (("#FFFFFF", "0,5"), ("#9AA0A6", "0,75"), ("#D92D20", "1"), ("#111111", "1,5"), ("#1E4FD8", "2,5"))
P["07_sabias_punteras"] = page(
    titulo("El color de la puntera", "dice el calibre", s1=54) +
    sub("Compacta los hilos del cable flexible para que el tornillo apriete <b>todos</b>: sin ella se abren, se cortan y la conexión <b>se calienta</b>.", 238) +
    f.html() + rotulos(f, [
        dict(t="Puntera aislada", s="tubo + collar de color", x=640, y=520, w=250, to=(.43, .17), c=A),
        dict(t="Puntera crimpada", x=900, y=640, w=230, to=(.63, .23), c=R),
        dict(t="Sin aislar", x=640, y=900, w=200, to=(.44, .80), c=A),
        dict(t="Pinza crimpadora", s="nunca con alicate", x=170, y=1010, w=260, to=(.15, .88), c=R)]) +
    "<div class='box' style='left:40px;top:1070px;width:1000px;height:120px'></div>" +
    "".join(f"<div style='position:absolute;left:{70 + i * 196}px;top:1082px;width:170px;text-align:center;font-weight:800;font-size:22px'>"
            f"<div style='height:44px;border-radius:10px;background:{c};border:2px solid #98A2B3;margin-bottom:6px'></div>{t} mm²</div>"
            for i, (c, t) in enumerate(cols)) +
    "<div style='position:absolute;left:40px;right:40px;top:1194px;text-align:center;font-size:16px;color:#475467'>Código DIN 46228-4 (existe otro código francés: revisa la caja del fabricante)</div>",
    "DIN 46228-1/-4 · Phoenix Contact, punteras AI · Weidmüller, punteras H (tabla de colores)",
    f"“Wire ferrules with and without insulation”, Simon A. Eugster, CC BY-SA 3.0, {CC}")

# 8 · placa del motor (números sobre la placa + leyenda)
f = Foto("p07_placa", 40, 330, w=1000)
nums = [(1, .11, .515), (2, .56, .515), (3, .12, .615), (4, .59, .615), (5, .03, .71), (6, .59, .71), (7, .03, .81)]
ley = [("FRAME MS 711-2", "carcasa 71 · “-2” = 2 polos"), ("INS.CL F", "aislamiento clase F (155 °C)"),
       ("0,37 kW = 0,5 HP", "potencia en el eje"), ("IP 55", "polvo y chorros de agua"),
       ("2730 rpm · 50 Hz", "síncrona 3000 → desliz. 9 %"), ("CONN. Δ / Y", "Δ en 230 V · Y en 400 V"),
       ("230/400 V · 1,67/0,97 A", "la corriente baja √3 en estrella")]
P["08_placa_motor"] = page(
    titulo("Lo que te dice la", "placa de un motor", s1=54, s2=80) +
    f.html() +
    "".join(f"<div class='chip' style='left:{f.p(a, b)[0]:.0f}px;top:{f.p(a, b)[1]:.0f}px;border-radius:50%;width:44px;height:44px;padding:0;"
            f"line-height:44px;text-align:center;border:3px solid #fff'>{n}</div>" for n, a, b in nums) +
    "".join(f"<div style='position:absolute;left:{50 + (i // 4) * 500}px;top:{880 + (i % 4) * 64}px;display:flex;gap:12px;align-items:center'>"
            f"<div style='width:40px;height:40px;border-radius:50%;background:#1E88E5;color:#fff;font-weight:800;text-align:center;line-height:40px;font-size:21px'>{i + 1}</div>"
            f"<div style='font-size:21px;font-weight:800'>{a}<div style='font-size:17px;font-weight:500;color:#475467'>{b}</div></div></div>"
            for i, (a, b) in enumerate(ley)) +
    "<div class='bar' style='top:1145px;font-size:21px'>n<sub>s</sub> = 120 × f ÷ polos = <b>3000 rpm</b> · (3000 − 2730) ÷ 3000 = <b>9 %</b> · 1,67 ÷ 0,97 ≈ <b>√3</b></div>",
    "IEC 60034-1 (placa) · IEC 60529 (IP) · IEC 60085 (clases térmicas) · IEC 60072-1 (carcasas)",
    f"“Motor nameplate Malmbergs”, Olgailga2, CC0, {CC}")


def comp(l1, l2, t1, t2, f1, f2, b1, b2, conclusion):
    li = lambda xs: "".join(f"<li style='margin:0 0 12px 24px'>{x}</li>" for x in xs)
    out = titulo(l1, l2, s1=62, s2=78)
    for i, (t, fo, b) in enumerate(((t1, f1, b1), (t2, f2, b2))):
        x = 40 + i * 520
        out += (f"<div class='box' style='left:{x}px;top:300px;width:480px;height:830px;background:#E3ECFA;border:0;overflow:hidden'>"
                f"<div style='background:{NAV};color:#fff;font-weight:800;font-size:30px;text-align:center;padding:14px'>{t}</div>"
                f"<div style='margin:18px;height:380px;background:#fff;border-radius:16px;display:flex;align-items:center;justify-content:center;overflow:hidden'>"
                f"<img src='../../posts3/fotos/{fo}.jpg' style='max-width:100%;max-height:100%'></div>"
                f"<ul style='font-size:23px;font-weight:500;line-height:1.3;padding:0 22px 0 8px'>{li(b)}</ul></div>")
    out += ("<div style='position:absolute;left:490px;top:560px;width:100px;height:100px;border-radius:50%;background:#1E88E5;color:#fff;"
            "font-weight:900;font-size:40px;text-align:center;line-height:92px;border:5px solid #fff;box-shadow:0 8px 18px rgba(0,0,0,.25)'>VS</div>")
    return out + f"<div class='bar' style='top:1146px'>{conclusion}</div>"


P["09_comp_guardamotor"] = page(comp(
    "Guardamotor", "vs relé térmico", "GUARDAMOTOR", "RELÉ TÉRMICO", "p09_mpcb", "p04_rele_c",
    ["Protege de <b>sobrecarga y cortocircuito</b>", "Corta el cortocircuito (aquí Icu 100 kA)", "Tiene mando ON / OFF: también secciona",
     "Ajuste 0,55–0,8 A · CLASS 10 · I&gt; 10 A", "Auxiliares 13-14 / 23-24"],
    ["Protege solo de <b>sobrecarga</b> y falta de fase", "Necesita breaker o fusibles antes", "Va bajo el contactor y abre su bobina (95-96)",
     "Ajuste 7,5–10,5 A · clase 10A", "STOP y RESET manual / automático"],
    "Un aparato o dos, pero <b>los dos necesitan un contactor</b> para arrancar a distancia"),
    "Siemens, 3RV2011-0HA10 · GE, catálogo C-2000, relé MT03 · IEC 60947-2 y 60947-4-1",
    f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0 · “GE MTO3N”, Dmitry G, CC BY-SA 3.0 · {CC}")

P["10_comp_contactores"] = page(comp(
    "Contactor industrial", "vs modular", "INDUSTRIAL", "MODULAR", "p10_iek", "p10_abb",
    ["3 polos de potencia + auxiliares", "Hecho para <b>motores</b>: corriente <b>AC-3</b>", "Bornes 1/L1… 2/T1… y bobina A1-A2",
     "Acepta relé térmico y bloques auxiliares", "Riel DIN o placa de montaje"],
    ["Hasta 4 polos (ABB ESB24-40: 4 NA)", "Para <b>resistencias e iluminación</b> (AC-1 / AC-7a)", "<b>24 A en AC-1</b> pero solo <b>9 A (4 kW) en AC-3</b>",
     "36 mm de ancho, como los breakers", "Bobina silenciosa AC/DC"],
    "Para un motor, compara la corriente <b>AC-3</b>, no la que dice el frente"),
    "IEC 60947-4-1 (AC-1, AC-3) · ABB, ficha ESB24-40 · IEC 61095 (AC-7a)",
    f"“Contactor DIN IEK”, Kae, CC BY-SA 3.0 · “Installationsschuetz ABB ESB 24 40”, Cherubino, CC BY-SA 2.5 · {CC}")

JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const k of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/html/'+k+'.html');await p.waitForTimeout(500);await p.screenshot({path:'png/'+k+'.png'});}
await b.close()})();"""

if __name__ == "__main__":
    import sys
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    ks = [k for k in P if not sys.argv[1:] or any(a in k for a in sys.argv[1:])]
    for k in ks:
        (AQ / "html" / f"{k}.html").write_text(P[k])
    (AQ / "shot.js").write_text(JS)
    subprocess.run(["node", "shot.js", *ks], cwd=AQ, check=True)
    print(len(ks))

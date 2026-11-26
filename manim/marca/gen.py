"""Marca del canal (26-nov): 3 fotos de perfil (800×800), 3 banners YouTube (2560×1440) y 3 portadas Facebook (1640×624).
Equipos del catálogo propio (h01v5_eq, recortados en eq/), logo ME. turquesa. HTML + Playwright."""
import subprocess
from pathlib import Path
from PIL import Image

AQ = Path(__file__).parent
T1, T2, NAV = "#94D3DF", "#0095B0", "#0B1F2A"
ESC = 0.23   # px de pantalla por px del catálogo (misma escala para todos los equipos de riel)
EQ = {k: Image.open(AQ / "eq" / f"{k}.png").size for k in ("F2on", "KM1on", "F3", "F1on", "M1", "H1on", "S1", "X1")}

FONTS = "@font-face{font-family:'Barlow C';src:url('../posts6/fonts/barlow-condensed-latin-900-normal.woff2');font-weight:900}"
BASE = FONTS + """*{margin:0;padding:0;box-sizing:border-box}body{position:relative;overflow:hidden;font-family:Montserrat}
.a{position:absolute}.eq{position:absolute;filter:drop-shadow(0 18px 22px rgba(0,0,0,.35))}
.chip{display:inline-block;border-radius:999px;font-weight:700;letter-spacing:.5px}"""


def eq(k, x, ybase, esc=ESC, extra=""):
    w, h = EQ[k]
    return f"<img class='eq' src='eq/{k}.png' style='left:{x}px;top:{ybase - h * esc:.0f}px;width:{w * esc:.0f}px;{extra}'>"


def riel(x, y, w, col="#B8C2CC"):
    return (f"<div class='a' style='left:{x}px;top:{y}px;width:{w}px;height:34px;border-radius:3px;"
            f"background:linear-gradient(180deg,#E6EBF0,{col} 45%,#8E99A5);box-shadow:0 6px 12px rgba(0,0,0,.25)'></div>"
            + "".join(f"<div class='a' style='left:{x + 14 + i * 46}px;top:{y + 11}px;width:26px;height:12px;border-radius:6px;background:#6D7884'></div>"
                      for i in range(int((w - 30) / 46))))


def tablero(x, ybase, esc=ESC, rail="#B8C2CC"):
    yc = ybase - EQ["F2on"][1] * esc / 2
    """F2 + KM1 con F3 + F1 sobre riel; devuelve html y ancho."""
    s, cx = [], x
    for k, gap in (("F2on", 26), ("KM1on", 26), ("F3", 26), ("F1on", 0)):
        w, h = EQ[k]
        yb = ybase if k != "F3" else ybase - 0
        s.append(eq(k, cx, yc + h * esc / 2, esc))
        cx += w * esc + gap
    tot = cx - x
    return riel(x - 30, yc - 17, tot + 60, rail) + "".join(s), tot


def cables(y0, n, cols, x0=-50, x1=2700, sep=16, w=9, curva=None):
    p = []
    for i, c in enumerate(cols * (n // len(cols) + 1)):
        if i >= n:
            break
        y = y0 + i * sep
        d = f"M{x0},{y} H{x1}" if not curva else curva(y, i)
        dash = "" if c != "GY" else ""
        if c == "GY":
            p.append(f"<path d='{d}' stroke='#1E9E4A' stroke-width='{w}' fill='none' stroke-linecap='round'/>"
                     f"<path d='{d}' stroke='#F2C200' stroke-width='{w}' fill='none' stroke-dasharray='22 22' stroke-linecap='butt'/>")
        else:
            p.append(f"<path d='{d}' stroke='{c}' stroke-width='{w}' fill='none' stroke-linecap='round'/>")
    return "".join(p)


def trazas(W, H, col, op=.18, seed=3):
    """Recorridos de cableado tipo plano (líneas con quiebres a 90° y nodos), decorativos, sin símbolos."""
    import random
    random.seed(seed)
    s = []
    for _ in range(26):
        x, y = random.randrange(0, W, 40), random.randrange(0, H, 40)
        d = f"M{x},{y}"
        for _ in range(random.randint(2, 4)):
            if random.random() < .5:
                x += random.choice((-1, 1)) * random.randrange(120, 520, 40)
            else:
                y += random.choice((-1, 1)) * random.randrange(80, 320, 40)
            d += f" L{x},{y}"
        s.append(f"<path d='{d}' stroke='{col}' stroke-width='3' fill='none' opacity='{op}'/><circle cx='{x}' cy='{y}' r='7' fill='{col}' opacity='{op * 1.6}'/>")
    return f"<svg class='a' style='left:0;top:0' width='{W}' height='{H}'>{''.join(s)}</svg>"


def texto(x, y, nombre_c, sub_c, chip_bg, chip_c, esc=1.0, logo="logo.png", chips=True, align="left"):
    f = lambda v: f"{v * esc:.0f}px"
    ch = "".join(f"<span class='chip' style='font-size:{f(25)};padding:{f(9)} {f(22)};margin:0 {f(10)} {f(10)} 0;background:{chip_bg};color:{chip_c}'>{t}</span>"
                 for t in ("Tableros eléctricos", "Arranque de motores", "PLC", "Normas IEC · NEC"))
    return (f"<div class='a' style='left:{x}px;top:{y}px;text-align:{align}'>"
            f"<div style='display:flex;align-items:center;gap:{f(34)}'><img src='{logo}' style='height:{f(150)}'>"
            f"<div><div style='font-weight:900;font-size:{f(104)};line-height:.92;letter-spacing:{f(-2)};color:{nombre_c}'>MIGUEL ESQUIT</div>"
            f"<div style='font-weight:700;font-size:{f(33)};letter-spacing:{f(5)};color:{sub_c};margin-top:{f(14)}'>ELECTRICIDAD Y AUTOMATIZACIÓN INDUSTRIAL</div></div></div>"
            + (f"<div style='margin-top:{f(30)}'>{ch}</div>" if chips else "") + "</div>")


# ------------------------------------------------------------------ YouTube 2560×1440 (zona segura 1546×423 en x 507–2053, y 508–931)
YT = {}
tb, tw = tablero(0, 0)
# 1 · oscuro
t, w = tablero(1420, 860, .16)
MOT = eq("M1", 2085, 880, .085)
YT["yt1_oscuro"] = ("background:radial-gradient(ellipse at 70% 50%,#0E3442 0%,#08202A 45%,#050F14 100%)",
    trazas(2560, 1440, T2, .22) +
    "<div class='a' style='left:0;top:0;width:2560px;height:1440px;background-image:linear-gradient(rgba(148,211,223,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(148,211,223,.06) 2px,transparent 2px);background-size:80px 80px'></div>"
    + MOT + texto(545, 615, "#FFFFFF", T1, "rgba(0,149,176,.22)", "#D8F3F8", .64) + t +
    f"<div class='a' style='left:0;top:960px;width:2560px;height:4px;background:linear-gradient(90deg,transparent,{T2},transparent)'></div>")
# 2 · claro
t, w = tablero(1420, 860, .16, rail="#C3CCD5")
YT["yt2_claro"] = ("background:#F3F6F8",
    f"<div class='a' style='left:-120px;top:420px;width:520px;height:600px;background:{T2};transform:skewX(-14deg)'></div>"
    f"<div class='a' style='left:330px;top:420px;width:90px;height:600px;background:{T1};transform:skewX(-14deg)'></div>"
    f"<div class='a' style='left:2180px;top:420px;width:520px;height:600px;background:{T1};opacity:.55;transform:skewX(-14deg)'></div>"
    + MOT + texto(545, 615, NAV, T2, "#FFFFFF", NAV, .64) + t +
    "<style>.chip{box-shadow:0 2px 0 #D5DEE5;border:2px solid #DDE5EB}</style>")


# 3 · turquesa con cables
def curva3(y, i):
    return f"M-50,{y} H1450 C1520,{y} 1530,{y + 240} 1600,{y + 240} H2700"


t, w = tablero(1420, 860, .16, rail="#DCE3EA")
YT["yt3_turquesa"] = (f"background:linear-gradient(120deg,{T2} 0%,#007E95 60%,#006376 100%)",
    f"<svg class='a' style='left:0;top:0' width='2560' height='1440'>{cables(960, 4, ['#16181B', '#16181B', '#16181B', 'GY'], sep=22, w=12)}"
    f"{cables(480, 3, ['#D7262D', '#D7262D', '#1E56C8'], sep=18, w=7)}</svg>"
    + MOT + texto(545, 615, "#FFFFFF", "#D8F3F8", "rgba(255,255,255,.16)", "#FFFFFF", .64, logo="logo_blanco.png") + t)

# ------------------------------------------------------------------ Facebook 1640×624 (contenido al centro: móvil recorta los lados)
FB = {}
MOTF = eq("M1", 1400, 470, .044)
k = .47
t, w = tablero(905, 455, .1)
FB["fb1_oscuro"] = (YT["yt1_oscuro"][0], trazas(1640, 624, T2, .22, 5) +
    "<div class='a' style='left:0;top:0;width:1640px;height:624px;background-image:linear-gradient(rgba(148,211,223,.06) 2px,transparent 2px),linear-gradient(90deg,rgba(148,211,223,.06) 2px,transparent 2px);background-size:52px 52px'></div>"
    + MOTF + texto(290, 205, "#FFFFFF", T1, "rgba(0,149,176,.22)", "#D8F3F8", k) + t)
t, w = tablero(905, 455, .1, rail="#C3CCD5")
FB["fb2_claro"] = ("background:#F3F6F8",
    f"<div class='a' style='left:-160px;top:-40px;width:400px;height:720px;background:{T2};transform:skewX(-14deg)'></div>"
    f"<div class='a' style='left:200px;top:-40px;width:60px;height:720px;background:{T1};transform:skewX(-14deg)'></div>"
    + MOTF + texto(290, 205, NAV, T2, "#FFFFFF", NAV, k) + t + "<style>.chip{border:2px solid #DDE5EB}</style>")
t, w = tablero(905, 455, .1, rail="#DCE3EA")
FB["fb3_turquesa"] = (YT["yt3_turquesa"][0],
    f"<svg class='a' style='left:0;top:0' width='1640' height='624'>{cables(585, 4, ['#16181B', '#16181B', '#16181B', 'GY'], sep=14, w=8, x1=1700)}"
    f"{cables(60, 3, ['#D7262D', '#D7262D', '#1E56C8'], sep=12, w=5, x1=1700)}</svg>"
    + MOTF + texto(290, 205, "#FFFFFF", "#D8F3F8", "rgba(255,255,255,.16)", "#FFFFFF", k, logo="logo_blanco.png") + t)

# ------------------------------------------------------------------ Perfil 800×800 (se recorta en círculo)
PF = {
    "perfil1_blanco": ("background:#FFFFFF", f"<div class='a' style='inset:40px;border-radius:50%;border:14px solid {T2}'></div>"
                       "<img class='a' src='logo.png' style='left:170px;top:270px;width:460px'>"),
    "perfil2_oscuro": ("background:radial-gradient(circle,#0E3442 0%,#06161D 100%)",
                       f"<div class='a' style='inset:40px;border-radius:50%;border:10px solid {T2};box-shadow:0 0 50px rgba(0,149,176,.45)'></div>"
                       "<img class='a' src='logo.png' style='left:170px;top:270px;width:460px'>"),
    "perfil3_turquesa": (f"background:linear-gradient(135deg,{T2},#006376)",
                         "<img class='a' src='logo_blanco.png' style='left:170px;top:270px;width:460px'>"),
}


def html(bg, body, W, H):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}body{{width:{W}px;height:{H}px;{bg}}}</style></head><body>{body}</body></html>"


JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const a of process.argv.slice(2)){const [k,w,h]=a.split(':');const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto('file://'+process.cwd()+'/'+k+'.html');await p.waitForTimeout(700);await p.screenshot({path:'out/'+k+'.png'});await p.close();}
await b.close()})();"""

if __name__ == "__main__":
    (AQ / "out").mkdir(exist_ok=True)
    args = []
    for D, W, H in ((YT, 2560, 1440), (FB, 1640, 624), (PF, 800, 800)):
        for k, (bg, body) in D.items():
            (AQ / f"{k}.html").write_text(html(bg, body, W, H))
            args.append(f"{k}:{W}:{H}")
    (AQ / "shot.js").write_text(JS)
    subprocess.run(["node", "shot.js", *args], cwd=AQ, check=True)
    print(len(args))

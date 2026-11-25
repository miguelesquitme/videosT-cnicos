"""Relé térmico CHINT NR2-25 (2,5–4 A) modelado en 3D (three.js, modelo.html → render3d.js) y señalado.
Estilo E02 'partes numeradas' con línea punteada + vista lateral para la placa. Datos: ficha LARSSYSTEM/CHINT NR2."""
import importlib.util
import json
import shutil
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
cr = json.load(open(AQ / "crop.json"))
AZ, NAV = "#0057FF", "#0B1F4D"


def dims(v):
    b = cr[v]["bb"]
    return b[2] - b[0], b[3] - b[1]


# imagen principal (iso)
w0, h0 = dims("iso")
H = 860
W = H * w0 / h0
X, Y = 1060 - W, 250
pp = lambda k, v="iso", x=X, y=Y, w=W, h=H: (x + cr[v]["pts"][k][0] * w, y + cr[v]["pts"][k][1] * h)
# vista lateral pequeña
w1, h1 = dims("izq")
HL = 250
WL = HL * w1 / h1
XL, YL = 70, 1010

items = [(1, "pines", "Pines de entrada", "a 2/T1·4/T2·6/T3 del contactor"), (2, "gancho", "Gancho de sujeción", "lo fija al contactor"),
         (3, "indicador", "Indicador de disparo", "muestra si disparó"), (4, "dial", "Dial de ajuste", "2,5 a 4 A · corriente del motor"),
         (5, "stop", "Botón STOP", "abre solo 95-96"), (6, "reset", "RESET H / A", "manual o automático"),
         (7, "test", "Botón TEST", "simula el disparo"), (8, "aux", "Auxiliares", "97-98 NA · 95-96 NC"), (9, "salida", "Bornes de salida", "2/T1·4/T2·6/T3 al motor")]
svg, li = [], []
y0, paso = 300, 80
for i, (n, k, t, s) in enumerate(items):
    y = y0 + i * paso
    px, py = pp(k)
    svg.append(f"<polyline points='96,{y} 440,{y} {px:.0f},{py:.0f}' fill='none' stroke='{AZ}' stroke-width='3' stroke-dasharray='9 7'/>"
               f"<circle cx='{px:.0f}' cy='{py:.0f}' r='8' fill='{AZ}' stroke='#fff' stroke-width='3'/>")
    li.append(f"<div class='li' style='top:{y - 25}px'><div class='n'>{n}</div><div class='bx'><b>{t}</b><span>{s}</span></div></div>")
qx, qy = pp("placa", "izq", XL, YL, WL, HL)
svg.append(f"<polyline points='{qx:.0f},{qy:.0f} {XL + WL + 30:.0f},{qy:.0f}' fill='none' stroke='{AZ}' stroke-width='3' stroke-dasharray='9 7'/>"
           f"<circle cx='{qx:.0f}' cy='{qy:.0f}' r='8' fill='{AZ}' stroke='#fff' stroke-width='3'/>")
li.append(f"<div class='li' style='left:{XL + WL + 30:.0f}px;width:330px;top:{qy - 25:.0f}px'><div class='n'>10</div><div class='bx'><b>Placa de datos</b><span>en el costado: Ue, clase, norma</span></div></div>")

CSS = """body{background:#fff!important}
.h1b{position:absolute;left:46px;top:40px;font-family:'Barlow C';font-weight:900;font-style:italic;color:#0B1F4D;text-transform:uppercase;line-height:.88}
.mdl{position:absolute;left:50px;top:232px;font:800 22px Montserrat;color:#fff;background:#0B1F4D;border-radius:10px;padding:6px 14px}
.mdl em{font-style:normal;color:#FFD400}
.li{position:absolute;left:44px;display:flex;gap:14px;align-items:center;z-index:2}
.n{width:48px;height:48px;border-radius:50%;background:#0057FF;color:#fff;font:800 23px Montserrat;display:flex;align-items:center;justify-content:center;border:4px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.3);flex:none}
.bx{background:#fff;padding-right:8px}.li b{display:block;font:800 24px Montserrat;color:#0B1F4D;line-height:1.1}.li span{font:500 17px Montserrat;color:#475467}
svg.ov{position:absolute;left:0;top:0;z-index:1}
.r3{position:absolute;filter:drop-shadow(0 18px 26px rgba(11,31,77,.25))}
.ins{position:absolute;border:3px solid #CFE0F5;border-radius:22px;background:#F6FAFF}
.spec{position:absolute;left:700px;right:40px;top:1100px;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.spec div{background:#0B1F4D;color:#fff;border-radius:14px;padding:10px 14px;font:500 16px Montserrat}.spec b{display:block;font:900 26px 'Barlow C';color:#FFD400}"""
spec = [("Clase 10A", "disparo"), ("690 V", "tensión Ue"), ("1 NA + 1 NC", "auxiliares"), ("Falta de fase", "protección incluida")]
html = (f"<div class='h1b'><div style='font-size:58px;color:{AZ}'>Partes del</div><div style='font-size:132px'>Relé térmico</div></div>"
        "<div class='mdl'>CHINT <em>NR2-25</em> · 2,5–4 A · modelo 3D</div>"
        f"<img class='r3' src='../c3d_iso.png' style='left:{X:.0f}px;top:{Y}px;width:{W:.0f}px;height:{H}px'>"
        f"<div class='ins' style='left:{XL - 20}px;top:{YL - 14}px;width:{WL + 40:.0f}px;height:{HL + 28}px'></div>"
        f"<img src='../c3d_izq.png' style='position:absolute;left:{XL}px;top:{YL}px;width:{WL:.0f}px;height:{HL}px'>"
        f"<svg class='ov' width='1080' height='1350' viewBox='0 0 1080 1350'>{''.join(svg)}</svg>" + "".join(li) +
        "<div class='spec'>" + "".join(f"<div><b>{a}</b>{b}</div>" for a, b in spec) + "</div>")
P = {"NR2_25_partes_3d": p6.page(CSS, html, "CHINT, ficha NR2 · LARSSYSTEM Guatemala, NR2-25 2,5-4 A · IEC/EN 60947-4-1",
                                 "modelo 3D propio (three.js) basado en el producto")}

if __name__ == "__main__":
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    shutil.copytree(AQ.parent / "posts6" / "fonts", AQ / "fonts", dirs_exist_ok=True)
    for k, v in P.items():
        (AQ / "html" / f"{k}.html").write_text(v)
    (AQ / "shot.js").write_text(p4.JS)
    subprocess.run(["node", "shot.js", *P], cwd=AQ, check=True)

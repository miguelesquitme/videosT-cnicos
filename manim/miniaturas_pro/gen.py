"""Miniaturas 'pro' (24-nov): misma energía de H01v5 pero más sobrias. python3 gen.py → ../miniatura_<clave>_pro.png"""
import subprocess, pathlib
AQUI = pathlib.Path(__file__).parent
EQ = "../h01v5_eq"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;overflow:hidden;font-family:'Montserrat';position:relative;
 background:radial-gradient(ellipse 60% 75% at 73% 50%,#1d5fc0 0%,#0c2d66 38%,#061330 75%,#040c20 100%)}
.rayos{position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 73% 50%,rgba(255,255,255,.035) 0 5deg,transparent 5deg 14deg);
 -webkit-mask:radial-gradient(circle at 73% 50%,#000 10%,transparent 62%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:48px 48px}
.franja{position:absolute;left:-60px;bottom:-40px;width:900px;height:16px;background:#FFC400;transform:rotate(-8deg);opacity:.9}
.franja2{position:absolute;left:-60px;bottom:-8px;width:620px;height:6px;background:#FFC400;transform:rotate(-8deg);opacity:.5}
.halo{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(120,190,255,.55),rgba(60,140,255,.15) 45%,transparent 70%)}
.suelo{position:absolute;border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.55),transparent 70%)}
img.eq{position:absolute;filter:drop-shadow(0 30px 34px rgba(0,0,0,.6)) drop-shadow(0 0 1px rgba(255,255,255,.4))}
.kicker{position:absolute;left:96px;top:118px;display:flex;align-items:center;gap:18px}
.kicker span{background:#FFC400;color:#0a1430;font-weight:900;font-size:46px;letter-spacing:3px;padding:6px 22px 8px;border-radius:6px;transform:skew(-8deg)}
.kicker i{display:block;width:120px;height:5px;background:#FFC400;border-radius:3px}
.titulo{position:absolute;left:92px;top:205px;width:1040px;color:#fff;font-weight:900;font-size:128px;line-height:1.0;letter-spacing:-2.5px;
 text-transform:uppercase;text-shadow:0 6px 18px rgba(0,0,0,.45)}
.titulo b{color:#FFC400}
.titulo em{font-style:normal;color:#4FD1FF}
.chips{position:absolute;left:96px;bottom:118px;display:flex;gap:22px}
.chip{display:flex;align-items:center;gap:18px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.28);border-radius:18px;padding:14px 30px 14px 20px;
 backdrop-filter:blur(6px)}
.chip .n{font-weight:900;font-size:84px;color:#FFC400;line-height:1}
.chip .t{color:#fff;font-weight:800;font-size:38px;line-height:1.05}
.chip .t small{display:block;font-weight:600;font-size:28px;color:#c9d6ee}
.chip .ico{width:46px;height:46px;border-radius:50%;background:#12B76A;box-shadow:0 0 18px #12B76A}
.logo{position:absolute;right:60px;top:50px;height:76px}
.tag{position:absolute;font-weight:800;font-size:30px;color:#fff;background:rgba(6,19,48,.85);border:2px solid #FFC400;border-radius:10px;padding:6px 16px}
"""


def pagina(cuerpo):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" \
           f"<div class='rayos'></div><div class='grid'></div>{cuerpo}<div class='franja'></div><div class='franja2'></div>" \
           f"<img class='logo' src='../logo_oficial.png'></body></html>"


def chip(n, a, b):
    return f"<div class='chip'><div class='n'>{n}</div><div class='t'>{a}<small>{b}</small></div></div>"


MINIS = {
    "H21_disyuntor": pagina(f"""
<div class='halo' style='left:1080px;top:110px;width:860px;height:860px'></div>
<div class='suelo' style='left:1150px;top:880px;width:700px;height:110px'></div>
<img class='eq' src='{EQ}/F1on.png' style='left:1140px;top:190px;height:680px'>
<img class='eq' src='{EQ}/F2on.png' style='left:1360px;top:190px;height:680px'>
<div class='kicker'><span>GUÍA PRÁCTICA</span><i></i></div>
<div class='titulo'>Selecciona el <b>disyuntor</b> <em>correcto</em></div>
<div class='chips'>{chip(6, "CRITERIOS", "de selección")}{chip(2, "EJEMPLOS", "reales")}</div>"""),
    "H22_rele_termico": pagina(f"""
<div class='halo' style='left:1060px;top:90px;width:900px;height:900px'></div>
<div class='suelo' style='left:1130px;top:870px;width:760px;height:110px'></div>
<img class='eq' src='{EQ}/F3.png' style='left:1150px;top:200px;width:700px'>
<div class='kicker'><span>GUÍA PRÁCTICA</span><i></i></div>
<div class='titulo'>Ajusta el <b>relé térmico</b> <em>correcto</em></div>
<div class='chips'>{chip(6, "CRITERIOS", "de selección")}{chip(2, "EJEMPLOS", "reales")}</div>"""),
    "H01_arranque": pagina(f"""
<div class='halo' style='left:1050px;top:40px;width:920px;height:920px'></div>
<img class='eq' src='{EQ}/M1.png' style='left:1080px;top:600px;height:470px'>
<img class='eq' src='{EQ}/KM1on.png' style='left:1240px;top:70px;height:590px'>
<img class='eq' src='{EQ}/H1on.png' style='left:1670px;top:230px;height:320px'>
<div class='kicker'><span>¡POR FIN!</span><i></i></div>
<div class='titulo' style='font-size:112px;width:1120px'>Arranco mi <b>primer motor</b> con <em>contactor</em></div>
<div class='chips'><div class='chip'><div class='ico'></div><div class='t'>PASO A PASO<small>del diagrama al arranque</small></div></div>{chip("10", "HP", "208 V · real")}</div>"""),
}

JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
for(const k of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/'+k+'.html');await p.waitForTimeout(400);await p.screenshot({path:'../miniatura_'+k+'_pro.png'});}
await b.close()})();"""

if __name__ == "__main__":
    for k, h in MINIS.items():
        (AQUI / f"{k}.html").write_text(h)
    (AQUI / "shot.js").write_text(JS)
    subprocess.run(["node", "shot.js", *MINIS], cwd=AQUI, check=True)

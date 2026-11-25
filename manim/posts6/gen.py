"""Publicaciones v6 (25-nov): 10 ESTILOS distintos para que el usuario elija. Solo electricidad industrial.
Fotos reales de Commons (posts3/fotos). Reusa Foto/rotulos de posts4."""
import importlib.util
import subprocess
from pathlib import Path

AQ = Path(__file__).parent
sp = importlib.util.spec_from_file_location("p4", AQ.parent / "posts4" / "gen.py")
p4 = importlib.util.module_from_spec(sp)
sp.loader.exec_module(p4)
Foto, CC = p4.Foto, p4.CC

FONTS = "".join(f"@font-face{{font-family:'{n}';src:url('../fonts/{f}.woff2');font-weight:{w};font-style:{s}}}" for n, f, w, s in [
    ("Barlow C", "barlow-condensed-latin-800-normal", 800, "normal"), ("Barlow C", "barlow-condensed-latin-900-normal", 900, "normal"),
    ("Barlow C", "barlow-condensed-latin-900-italic", 900, "italic"), ("Archivo Black", "archivo-black-latin-400-normal", 400, "normal"),
    ("Bebas", "bebas-neue-latin-400-normal", 400, "normal")])
BASE = p4.CSS + FONTS + """
.abs{position:absolute}
.tag{position:absolute;font-family:'Barlow C';font-weight:800;font-size:28px;letter-spacing:3px;padding:6px 18px;border-radius:8px}
.pie2{position:absolute;left:40px;right:40px;bottom:16px;display:flex;align-items:flex-end;gap:18px}
.pie2 .f{flex:1;font-size:13.5px;line-height:1.3}
.pie2 .m{display:flex;align-items:center;gap:10px;font-weight:800;font-size:24px;white-space:nowrap}
.pie2 .m img{height:40px;background:#fff;border-radius:8px;padding:3px 6px}
"""


def page(css, cuerpo, fuentes, cred, oscuro=False):
    col = "#C9D2E3" if oscuro else "#667085"
    mc = "#fff" if oscuro else "#0B1F4D"
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{cuerpo}"
            f"<div class='pie2'><div class='f' style='color:{col}'><b>Fuentes:</b> {fuentes} · <b>Foto:</b> {cred}</div>"
            f"<div class='m' style='color:{mc}'><img src='../../logo_oficial.png'>@miguelesquit</div></div></body></html>")


P = {}

# ---------------------------------------------------------------- 1 · POR DENTRO estilo miniatura (oscuro + amarillo)
f = Foto("p03_mcb", 150, 470, w=780)
css = """body{background:radial-gradient(circle at 50% 58%,#1d3f94 0%,#0b1636 52%,#04060d 100%)!important;color:#fff}
.lab{background:#0B1220!important;color:#fff;border-width:3px!important}.lab small{color:#AFC3E8!important}
.card{border-color:#FFD400!important;box-shadow:0 0 0 4px #FFD400,0 0 60px rgba(255,212,0,.45)!important}
.h{position:absolute;left:40px;right:40px;top:96px;text-align:center;font-family:Montserrat;font-weight:900;font-size:86px;line-height:.98;letter-spacing:-2px;text-transform:uppercase}
.h em{font-style:normal;color:#FFD400;text-shadow:0 0 30px rgba(255,212,0,.55)}"""
P["estilo01_miniatura_oscura"] = page(css,
    "<div class='tag' style='left:50%;transform:translateX(-50%);top:34px;background:#FFD400;color:#0B1220'>POR DENTRO</div>"
    "<div class='h'>¿Qué hay dentro<br>de un <em>breaker</em>?</div>" + f.html() +
    p4.rotulos(f, [dict(t="Palanca", x=150, y=470, w=200, to=(.51, .12), c="#FFD400"),
                   dict(t="Bobina", s="cortocircuito", x=150, y=760, w=200, to=(.565, .50), modo="d", c="#FF4D4D"),
                   dict(t="Cámara de arco", x=150, y=1010, w=220, to=(.55, .74), modo="d", c="#FFD400"),
                   dict(t="Mecanismo", s="disparo libre", x=930, y=520, w=200, to=(.62, .29), c="#2EC4FF"),
                   dict(t="Bimetal", s="sobrecarga", x=930, y=760, w=200, to=(.74, .50), c="#FF4D4D")]) +
    "<div class='abs' style='left:0;right:0;top:1150px;display:flex;justify-content:center;gap:18px;font-family:\"Barlow C\";font-weight:800;font-size:32px'>"
    "<div style='background:#FF4D4D;padding:6px 20px;border-radius:10px'>BIMETAL → SOBRECARGA</div>"
    "<div style='background:#2EC4FF;color:#04121f;padding:6px 20px;border-radius:10px'>BOBINA → CORTOCIRCUITO</div></div>",
    "IEC 60898-1 · IEK, ficha VA47 C40 · ABB, guía de interruptores modulares", f"“Circuit breaker structure ON”, Kae, CC BY-SA 3.0, {CC}", True)

# ---------------------------------------------------------------- 2 · PARTES vista frontal, numerado limpio
f = Foto("p09_mpcb", 560, 300, h=900)
nums = [(1, .50, .20, "Contactos auxiliares", "13-14 y 23-24 (NA)"), (2, .17, .39, "Dial de ajuste", "corriente del motor"),
        (3, .62, .47, "Mando giratorio", "ON · OFF · TRIPPED"), (4, .15, .53, "Clase 10 · I&gt; 10 A", "térmico + magnético"),
        (5, .13, .605, "Botón TEST", "simula el disparo"), (6, .50, .91, "Bornes de salida", "2/T1 · 4/T2 · 6/T3")]
css = """body{background:#fff!important}
.h1b{position:absolute;left:50px;top:60px;font-family:'Barlow C';font-weight:900;font-style:italic;color:#0B1F4D;text-transform:uppercase;line-height:.88}
.n{position:absolute;width:52px;height:52px;border-radius:50%;background:#0057FF;color:#fff;font:800 26px Montserrat;display:flex;align-items:center;justify-content:center;
 transform:translate(-50%,-50%);border:4px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.35)}
.li{position:absolute;left:50px;width:470px;display:flex;gap:16px;align-items:center}
.li b{display:block;font:800 27px Montserrat;color:#0B1F4D}.li span{font:500 20px Montserrat;color:#475467}"""
P["estilo02_partes_numeradas"] = page(css,
    "<div class='h1b'><div style='font-size:62px;color:#0057FF'>Partes del</div><div style='font-size:150px'>Guarda-<br>motor</div>"
    "<div style='width:160px;height:12px;background:#0057FF;margin-top:16px;border-radius:6px'></div></div>" + f.html() +
    "".join(f"<div class='n' style='left:{f.p(a, b)[0]:.0f}px;top:{f.p(a, b)[1]:.0f}px'>{n}</div>" for n, a, b, *_ in nums) +
    "".join(f"<div class='li' style='top:{540 + i * 105}px'><div class='n' style='position:relative;transform:none;flex:none'>{n}</div><div><b>{t}</b><span>{s}</span></div></div>"
            for i, (n, a, b, t, s) in enumerate(nums)),
    "Siemens, ficha 3RV2011-0HA10 · IEC 60947-2 · IEC 60947-4-1", f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0, {CC}")

# ---------------------------------------------------------------- 3 · COMPARACIÓN diagonal azul / naranja
css = """body{background:#0057FF!important}
.der{position:absolute;inset:0;background:#FF7A00;clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)}
.h{position:absolute;left:30px;right:30px;top:40px;text-align:center;font-family:'Archivo Black';color:#fff;font-size:76px;line-height:1;text-shadow:0 6px 0 rgba(0,0,0,.25)}
.ph{position:absolute;top:250px;width:430px;height:470px;background:#fff;border-radius:28px;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.ph img{max-width:92%;max-height:92%}
.nm{position:absolute;top:740px;width:430px;text-align:center;font-family:'Barlow C';font-weight:900;font-size:58px;color:#fff;letter-spacing:1px}
.bl{position:absolute;top:830px;width:440px;color:#fff;font:600 30px/1.3 Montserrat}.bl div{margin-bottom:22px;padding-left:34px;position:relative}
.bl div:before{content:'⚡';position:absolute;left:0}
.vs{position:absolute;left:470px;top:415px;width:140px;height:140px;border-radius:50%;background:#0B1220;color:#FFD400;font:900 58px 'Barlow C';
 display:flex;align-items:center;justify-content:center;border:6px solid #fff}
.ver{position:absolute;left:40px;right:40px;top:1110px;background:#fff;border-radius:18px;padding:16px;text-align:center;font:800 28px Montserrat;color:#0B1220}"""
P["estilo03_comparacion_vs"] = page(css,
    "<div class='der'></div><div class='h'>¿INDUSTRIAL<br>O MODULAR?</div>"
    "<div class='ph' style='left:50px'><img src='../../posts3/fotos/p10_iek.jpg'></div><div class='ph' style='left:600px'><img src='../../posts3/fotos/p10_abb.jpg'></div>"
    "<div class='vs'>VS</div><div class='nm' style='left:50px'>INDUSTRIAL</div><div class='nm' style='left:600px'>MODULAR</div>"
    "<div class='bl' style='left:45px'><div>Para <b>motores</b> (AC-3)</div><div>Acepta relé térmico</div><div>3 polos + auxiliares</div></div>"
    "<div class='bl' style='left:600px'><div>Para <b>iluminación</b> (AC-7a)</div><div>ESB24-40: 24 A en AC-1</div><div>…pero solo <b>9 A en AC-3</b></div></div>"
    "<div class='ver'>Para un motor, compara la corriente <span style='color:#0057FF'>AC-3</span>, no la del frente</div>",
    "IEC 60947-4-1 · IEC 61095 · ABB, ficha ESB24-40", f"Kae, CC BY-SA 3.0 · Cherubino, CC BY-SA 2.5 · {CC}", True)

# ---------------------------------------------------------------- 4 · DATO CLAVE número gigante
css = """body{background:#fff!important}
.big{position:absolute;left:30px;top:150px;font-family:'Barlow C';font-weight:900;font-size:330px;line-height:.8;color:#E3001B;letter-spacing:-6px}
.big small{font-size:150px;letter-spacing:0}
.t{position:absolute;left:50px;width:470px;top:470px;font:800 40px/1.15 Montserrat;color:#0B1220}
.t em{font-style:normal;background:#E3001B;color:#fff;padding:0 10px}
.circ{position:absolute;left:560px;top:520px;width:500px;height:640px;border-radius:40px;overflow:hidden;border:8px solid #E3001B;box-shadow:0 20px 40px rgba(0,0,0,.25)}
.circ img{width:100%;height:100%;object-fit:cover;object-position:30% 50%}
.nota{position:absolute;left:50px;width:460px;top:880px;font:500 25px/1.35 Montserrat;color:#344054;border-left:8px solid #0B1220;padding-left:18px}"""
P["estilo04_dato_numero"] = page(css,
    "<div class='tag' style='left:50px;top:50px;background:#0B1220;color:#fff'>DATO CLAVE · DIFERENCIAL</div>"
    "<div class='big'>30<small> mA</small></div>"
    "<div class='t'>es la fuga que dispara el diferencial que <em>protege a las personas</em></div>"
    "<div class='circ'><img src='../../posts3/fotos/n01_rcd_c.jpg'></div>"
    "<div class='nota'>Los de <b>300 o 500 mA</b> (como el de la foto) protegen contra <b>incendio</b>, no contra choque eléctrico.</div>",
    "IEC 60364-4-41 (411.3.3) · IEC 61008-1 · Schneider Electric, guía de protección diferencial", f"“RCD inside”, WagnerTh, CC BY-SA 4.0, {CC}")

# ---------------------------------------------------------------- 5 · TIP DE TABLERISTA (amarillo industrial)
f = Foto("p06_punteras", 60, 380, w=960)
css = """body{background:#FFC400!important}
.stripe{position:absolute;left:0;right:0;height:34px;background:repeating-linear-gradient(-45deg,#111 0 26px,#FFC400 26px 52px)}
.h{position:absolute;left:50px;right:50px;top:110px;font-family:'Archivo Black';font-size:74px;line-height:1;color:#111}
.card{border-color:#111!important;border-radius:20px!important}
.ch{position:absolute;top:920px;width:180px;text-align:center;font:800 26px Montserrat;color:#111}
.ch div{height:86px;border-radius:14px;border:4px solid #111;margin-bottom:8px}"""
cols = (("#FFFFFF", "0,5"), ("#9AA0A6", "0,75"), ("#D92D20", "1"), ("#111111", "1,5"), ("#1E4FD8", "2,5"))
P["estilo05_tip_tablerista"] = page(css,
    "<div class='stripe' style='top:0'></div><div class='tag' style='left:50px;top:52px;background:#111;color:#FFC400'>TIP DE TABLERISTA</div>"
    "<div class='h'>El color de la puntera<br>te dice el calibre</div>" + f.html() +
    "".join(f"<div class='ch' style='left:{60 + i * 196}px'><div style='background:{c}'></div>{t} mm²</div>" for i, (c, t) in enumerate(cols)) +
    "<div class='abs' style='left:50px;right:50px;top:1080px;font:700 26px/1.35 Montserrat;color:#111'>✔ Crímpala con pinza, nunca con alicate &nbsp;·&nbsp; ✔ Código DIN 46228-4</div>",
    "DIN 46228-4 · Phoenix Contact, punteras AI · Weidmüller, punteras H", f"Simon A. Eugster, CC BY-SA 3.0, {CC}")

# ---------------------------------------------------------------- 6 · CÓMO SE LEE (acero oscuro)
f = Foto("p07_placa", 40, 330, w=1000)
it = [(1, .14, .57, .60, .66, "0,37 kW = 0,5 HP", "potencia en el eje"), (2, .05, .76, .60, .86, "230 / 400 V", "Δ en 230 · Y en 400"),
      (3, .61, .66, .86, .76, "Δ / Y", "cómo se conecta"), (4, .05, .66, .60, .76, "2730 rpm", "2 polos · desliz. 9 %"),
      (5, .61, .57, .76, .66, "IP 55", "polvo y chorros de agua"), (6, .58, .47, .80, .56, "Clase F", "aislamiento 155 °C")]
css = """body{background:linear-gradient(160deg,#2a2f37,#0f1115)!important;color:#fff}
.h{position:absolute;left:40px;right:40px;top:60px;text-align:center;font-family:'Bebas';font-size:120px;line-height:.9;letter-spacing:2px}
.h em{font-style:normal;color:#FFD400}
.hb{position:absolute;border:4px solid #FFD400;border-radius:6px;box-shadow:0 0 18px rgba(255,212,0,.6)}
.nb{position:absolute;width:44px;height:44px;border-radius:50%;background:#FFD400;color:#111;font:900 24px Montserrat;display:flex;align-items:center;justify-content:center;transform:translate(-60%,-60%)}
.lg{position:absolute;width:480px;display:flex;gap:14px;align-items:center}.lg b{font:800 27px Montserrat;display:block}.lg span{font:500 19px Montserrat;color:#C9D2E3}"""
P["estilo06_como_se_lee"] = page(css,
    "<div class='h'>Aprende a leer<br><em>la placa del motor</em></div>" + f.html() +
    "".join(f"<div class='hb' style='left:{f.p(a, b)[0]:.0f}px;top:{f.p(a, b)[1]:.0f}px;width:{f.p(c, d)[0] - f.p(a, b)[0]:.0f}px;height:{f.p(c, d)[1] - f.p(a, b)[1]:.0f}px'></div>"
            f"<div class='nb' style='left:{f.p(a, b)[0]:.0f}px;top:{f.p(a, b)[1]:.0f}px'>{n}</div>" for n, a, b, c, d, *_ in it) +
    "".join(f"<div class='lg' style='left:{50 + (i % 2) * 510}px;top:{900 + (i // 2) * 88}px'><div class='nb' style='position:relative;transform:none;flex:none'>{n}</div><div><b>{t}</b><span>{s}</span></div></div>"
            for i, (n, a, b, c, d, t, s) in enumerate(it)),
    "IEC 60034-1 · IEC 60529 · IEC 60085", f"“Motor nameplate Malmbergs”, Olgailga2, CC0, {CC}", True)

# ---------------------------------------------------------------- 7 · ¿SABÍAS QUÉ? degradado naranja
css = """body{background:linear-gradient(150deg,#FF8A00 0%,#FF3D00 100%)!important;color:#fff}
.q{position:absolute;left:50px;top:60px;font-family:'Barlow C';font-weight:900;font-style:italic;font-size:70px}
.n{position:absolute;left:40px;top:120px;font-family:'Barlow C';font-weight:900;font-size:400px;line-height:.85;letter-spacing:-10px;text-shadow:0 12px 0 rgba(0,0,0,.15)}
.n small{font-size:200px}
.t{position:absolute;left:50px;width:560px;top:500px;font:800 44px/1.12 Montserrat}
.c{position:absolute;left:560px;top:560px;width:470px;height:470px;border-radius:50%;overflow:hidden;border:10px solid #fff;box-shadow:0 20px 50px rgba(0,0,0,.3)}
.c img{width:100%;height:100%;object-fit:cover}
.s{position:absolute;left:50px;width:470px;top:780px;font:500 25px/1.35 Montserrat;background:rgba(0,0,0,.18);padding:18px;border-radius:16px}"""
P["estilo07_sabias_que"] = page(css,
    "<div class='q'>¿SABÍAS QUE…</div><div class='n'>53<small>%</small></div>"
    "<div class='t'>de la electricidad del mundo la consumen <u>motores eléctricos</u></div>"
    "<div class='c'><img src='../../posts3/fotos/p05_motor2.jpg'></div>"
    "<div class='s'>Bombas, ventiladores, compresores y bandas. Por eso un motor <b>IE3/IE4</b> bien dimensionado ahorra tanto.</div>",
    "IEA 4E EMSA, Policy Brief (2025) · IEA (2011) · ABB, Energy efficiency", f"S.J. de Waard, CC BY 2.5, {CC}", True)

# ---------------------------------------------------------------- 8 · CÓMO FUNCIONA paso a paso
css = """body{background:#F3F6FA!important}
.h{position:absolute;left:40px;right:40px;top:50px;text-align:center;font:900 66px/1.02 Montserrat;color:#0B1F4D;letter-spacing:-1.5px}
.h em{font-style:normal;background:linear-gradient(transparent 55%,#7CFFB2 55%)}
.st{position:absolute;left:50px;right:50px;height:280px;background:#fff;border-radius:24px;box-shadow:0 10px 26px rgba(11,31,77,.12);display:flex;align-items:center;gap:26px;padding:20px}
.st img{width:320px;height:240px;object-fit:contain;background:#E9EEF5;border-radius:16px}
.st .k{font:900 90px 'Barlow C';color:#00A859;width:70px;text-align:center}
.st b{display:block;font:800 32px Montserrat;color:#0B1F4D;margin-bottom:6px}.st span{font:500 23px/1.3 Montserrat;color:#344054}"""
steps = [("bob", "Energizas A1-A2", "La bobina crea un campo magnético en el núcleo."),
         ("arm", "Se mueve la armadura", "El núcleo la atrae y arrastra el portacontactos."),
         ("con", "Se cierran los polos", "1-2, 3-4, 5-6 conducen y el motor arranca. Sin tensión, el resorte los abre.")]
P["estilo08_paso_a_paso"] = page(css,
    "<div class='h'>¿Cómo funciona un<br><em>contactor</em>?</div>" +
    "".join(f"<div class='st' style='top:{260 + i * 310}px'><div class='k'>{i + 1}</div><img src='../crop/{im}.jpg'><div><b>{t}</b><span>{s}</span></div></div>"
            for i, (im, t, s) in enumerate(steps)),
    "IEC 60947-4-1 · Siemens, manual SIRIUS 3RT · Schneider, guía TeSys D", f"“Disassembled SIEMENS 3RT1017-1AV01”, Dmitry G, CC BY-SA 3.0, {CC}")

# ---------------------------------------------------------------- 9 · FICHA TÉCNICA (tarjeta de producto oscura)
css = """body{background:#0B1220!important;color:#fff}
.ph{position:absolute;left:50px;right:50px;top:190px;height:560px;border-radius:28px;background:linear-gradient(160deg,#EEF2F8,#C9D3E3);overflow:hidden;display:flex;align-items:center;justify-content:center}
.ph img{height:100%}
.h{position:absolute;left:50px;top:80px;font-family:'Archivo Black';font-size:72px;line-height:1}
.h em{font-style:normal;color:#2EC4FF}
.g{position:absolute;left:50px;right:50px;top:790px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.g div{background:#16213A;border:2px solid #24345A;border-radius:18px;padding:16px 18px}
.g b{display:block;font:900 48px 'Barlow C';color:#2EC4FF}.g span{font:600 21px Montserrat;color:#C9D2E3}.g div{padding:26px 20px!important}"""
spec = [("220 V CA", "tensión de bobina"), ("3 conmutados", "contactos 3PDT"), ("10 A · 250 V", "por contacto"),
        ("11 pines", "base octal enchufable"), ("Finder 60.13", "modelo de la foto"), ("Mando", "lógica y señalización")]
P["estilo09_ficha_tecnica"] = page(css,
    "<div class='tag' style='left:50px;top:36px;background:#2EC4FF;color:#0B1220'>FICHA RÁPIDA</div>"
    "<div class='h'>Relé de <em>11 pines</em></div><div class='ph'><img src='../../posts3/fotos/n09_rele11.jpg'></div>"
    "<div class='g'>" + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in spec) + "</div>",
    "Finder, ficha serie 60 · IEC 61810-1 · Omron, guía de relés MK", f"“11pin 3PDT relay”, 32RB17, CC0, {CC}", True)

# ---------------------------------------------------------------- 10 · EDITORIAL foto a sangre (transformador)
f = Foto("n03_trafo_aceite", 420, 0, h=1350)
css = """body{background:#05070D!important;color:#fff}
.card{border:0!important;border-radius:0!important;box-shadow:none!important}
.fade{position:absolute;left:0;top:0;width:640px;height:1350px;background:linear-gradient(90deg,#05070D 62%,rgba(5,7,13,0))}
.h{position:absolute;left:50px;top:150px;width:520px;font-family:'Barlow C';font-weight:900;font-size:128px;line-height:.86;text-transform:uppercase}
.h em{font-style:normal;color:#00E0A4}
.s{position:absolute;left:50px;top:600px;width:440px;font:500 26px/1.4 Montserrat;color:#D5DCE8}
.lab{background:rgba(5,7,13,.85)!important;color:#fff}.lab small{color:#9fb0c9!important}"""
P["estilo10_editorial"] = page(css,
    f.html() + "<div class='fade'></div><div class='tag' style='left:50px;top:70px;border:2px solid #00E0A4;color:#00E0A4'>POR DENTRO</div>"
    "<div class='h'>El corazón<br>de la <em>red</em></div>"
    "<div class='s'>Transformador trifásico en aceite: en cada columna del núcleo va la <b>baja tensión adentro</b> y la <b>alta afuera</b>.</div>" +
    p4.rotulos(f, [dict(t="Devanado de alta", s="en discos", x=900, y=1120, w=240, to=(.72, .74), c="#00E0A4"),
                   dict(t="Núcleo laminado", x=330, y=1010, w=240, to=(.21, .64), c="#00E0A4"),
                   dict(t="Aisladores", s="alta tensión", x=330, y=860, w=220, to=(.36, .12), modo="d", c="#00E0A4")]),
    "IEC 60076-1 · ABB, Transformer Handbook · Deutsches Museum", f"Dmm2va7, CC BY 3.0, {CC}", True)

if __name__ == "__main__":
    import sys
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    ks = [k for k in P if not sys.argv[1:] or any(a in k for a in sys.argv[1:])]
    for k in ks:
        (AQ / "html" / f"{k}.html").write_text(P[k])
    (AQ / "shot.js").write_text(p4.JS)
    subprocess.run(["node", "shot.js", *ks], cwd=AQ, check=True)
    print(len(ks))

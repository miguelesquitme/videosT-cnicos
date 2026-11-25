"""20 publicaciones 1080×1350 (FB, IG y comunidad de YT) · 24-nov.
Datos verificados: IEC 60947-4-1 (AC-1/AC-3, clase 10), IEC 60898-1 (curvas B/C/D), IEC 60204-1 (colores 13.2.4, paro de
emergencia 10.7), EN 50005 (numeración), NEC 2020 430.32(A)(1), T430.52, T430.250, NEMA MG 1 (factor de servicio, 9 puntas),
IEC 60034-8 (sentido de giro), placa Nidec U10P2D (caso base). Aritmética comprobada en Python.
Uso: python3 gen_posts.py  →  posts/png/post_XX.png"""
import subprocess, pathlib
AQ = pathlib.Path(__file__).resolve().parent
EQ, EQ5 = "eq", "../h01v5_eq"
TEMAS = {"azul": ("#0B1D3F", "#16407F"), "morado": ("#1E0B40", "#4B1C8F"), "verde": ("#062824", "#0E5A4C"), "grafito": ("#121418", "#2B303A"),
         "rojo": ("#2A0A0E", "#6E1620")}
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:'Montserrat';color:#fff;position:relative;background:radial-gradient(ellipse 80% 60% at 50% 48%,VAR2 0%,VAR1 70%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:40px 40px}
.tag{position:absolute;left:64px;top:60px;background:#FFC400;color:#0a1430;font-weight:900;font-size:30px;letter-spacing:2px;padding:8px 20px;border-radius:6px;text-transform:uppercase}
.num{position:absolute;right:64px;top:62px;font-weight:800;font-size:26px;color:rgba(255,255,255,.55)}
h1{position:absolute;left:64px;top:140px;width:952px;font-weight:900;font-size:76px;line-height:1.02;letter-spacing:-1.5px;text-transform:uppercase}
h1 b{color:#FFC400} h1 em{font-style:normal;color:#4FD1FF}
img.eq{position:absolute;filter:drop-shadow(0 22px 26px rgba(0,0,0,.55))}
.halo{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(130,190,255,.35),transparent 68%)}
.caja{position:absolute;left:64px;right:64px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.22);border-radius:22px;padding:26px 32px;font-size:33px;font-weight:600;line-height:1.25}
.caja b{color:#FFC400;font-weight:800}
.big{position:absolute;font-weight:900;color:#FFC400;line-height:.9;letter-spacing:-4px;text-shadow:0 0 40px rgba(255,196,0,.35)}
.lbl{position:absolute;font-weight:800;font-size:30px;text-align:center;text-transform:uppercase}
.fila{display:flex;align-items:center;gap:22px;margin:0 0 16px}
.fila .c{flex:0 0 74px;height:44px;border-radius:8px}
.fila span{font-size:32px;font-weight:700}
.fila span small{display:block;font-size:24px;font-weight:500;color:#c8d3e6}
.pie{position:absolute;left:64px;right:64px;bottom:44px;display:flex;align-items:center;justify-content:space-between;border-top:2px solid rgba(255,255,255,.18);padding-top:20px}
.pie .f{font-size:21px;color:#b9c4d8;max-width:720px;line-height:1.25}
.pie .m{display:flex;align-items:center;gap:14px;font-weight:800;font-size:26px}
.pie img{height:54px}
.ok{color:#3DDC84}.no{color:#FF5A5F}.cy{color:#4FD1FF}.am{color:#FFC400}
"""


def pagina(n, tema, tag, titulo, cuerpo, fuente):
    v1, v2 = TEMAS[tema]
    css = CSS.replace("VAR1", v1).replace("VAR2", v2)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body><div class='grid'></div>"
            f"<div class='tag'>{tag}</div><div class='num'>{n:02d}/20</div><h1 id='t'>{titulo}</h1><div style='position:absolute;left:0;top:40px;width:1080px;height:1350px'>{cuerpo}</div>"
            f"<div class='pie'><div class='f'>Fuente: {fuente}</div><div class='m'><img src='../../logo_oficial.png'>@miguelesquit</div></div><script>const t=document.getElementById('t');let f=76;while(t.offsetHeight>235&&f>50){{f-=2;t.style.fontSize=f+'px';}}</script></body></html>")


def img(src, x, y, h=None, w=None, extra=""):
    t = f"height:{h}px" if h else f"width:{w}px"
    return f"<img class='eq' src='{src}' style='left:{x}px;top:{y}px;{t};{extra}'>"


def caja(y, html, h=None):
    hh = f"height:{h}px;" if h else ""
    return f"<div class='caja' style='top:{y}px;{hh}'>{html}</div>"


def halo(x, y, d):
    return f"<div class='halo' style='left:{x}px;top:{y}px;width:{d}px;height:{d}px'></div>"


def lbl(x, y, w, txt, cls=""):
    return f"<div class='lbl {cls}' style='left:{x}px;top:{y}px;width:{w}px'>{txt}</div>"


def big(x, y, size, txt):
    return f"<div class='big' style='left:{x}px;top:{y}px;font-size:{size}px'>{txt}</div>"


P = []
# 1 · corriente de arranque
P.append(("azul", "Motores", "¿Por qué el motor pide <b>hasta 8 veces</b> su corriente al arrancar?",
          halo(140, 400, 800) + img(f"{EQ5}/M1.png", 120, 430, w=840) +
          caja(900, "Con el rotor quieto no hay <b>fuerza contraelectromotriz</b>: el motor se comporta casi como un transformador en corto. "
                    "En arranque directo pide <b>6 a 8 veces</b> la corriente nominal durante unos segundos.<br><span class='cy'>Motor de 26,5 A → ≈ 160 a 210 A al arrancar.</span>"),
          "catálogos de fabricantes de motores (valores típicos de arranque directo) · placa Nidec U10P2D"))
# 2 · estrella-delta
P.append(("morado", "Arranques", "Estrella-delta: arranca con <b>un tercio</b> de la corriente",
          big(64, 360, 300, "⅓") +
          img(f"{EQ}/KM1.png", 450, 380, h=300) + img(f"{EQ}/KM2.png", 645, 380, h=300) + img(f"{EQ}/KM3.png", 840, 380, h=300) +
          img(f"{EQ}/KT1.png", 300, 650, h=250) +
          lbl(435, 695, 215, "Línea") + lbl(630, 695, 215, "Triángulo") + lbl(825, 695, 215, "Estrella") +
          caja(930, "En estrella cada bobina recibe la tensión de línea <b>÷ √3</b>. Por eso la corriente de línea y el par de arranque bajan a <b>1/3</b> "
                    "de los de arranque directo. El temporizador <b>-KT1</b> decide cuándo pasar a triángulo."),
          "teoría de máquinas eléctricas (I<sub>Y</sub> = I<sub>Δ</sub> / 3) · IEC 60947-4-1 (arrancadores)"))
# 3 · numeración 13-14
filas = "".join(f"<div class='fila'><div class='c' style='background:{c}'></div><span>{a}<small>{b}</small></span></div>" for c, a, b in (
    ("#E5484D", "x1 – x2 · contacto NC", "normalmente cerrado: 11-12, 21-22…"),
    ("#30A46C", "x3 – x4 · contacto NA", "normalmente abierto: 13-14, 43-44…"),
    ("#F5A524", "x5 – x6 · NC especial", "por ejemplo temporizado o del térmico: 95-96"),
    ("#4FD1FF", "x7 – x8 · NA especial", "por ejemplo temporizado o del térmico: 97-98")))
P.append(("grafito", "Normas", "¿Qué significan el <b>13-14</b> y el <b>21-22</b>?",
          img(f"{EQ}/KM1.png", 640, 330, h=560) +
          f"<div style='position:absolute;left:64px;top:360px;width:560px;font-size:34px;font-weight:700;line-height:1.3'>"
          f"Primer dígito = <span class='am'>número de orden</span> del contacto.<br>Segundo dígito = <span class='cy'>función</span>.</div>" +
          f"<div style='position:absolute;left:64px;top:840px;width:960px'>{filas}</div>",
          "EN 50005 / IEC 60947-1 (marcado de bornes de aparamenta)"))
# 4 · AC-1 vs AC-3
P.append(("azul", "Contactores", "El mismo contactor, <b>dos corrientes</b>: AC-1 y AC-3",
          img(f"{EQ}/KM1on.png", 360, 330, h=520) +
          lbl(64, 420, 280, "<span class='ok'>AC-1</span><br><small style='font-size:24px;font-weight:600;text-transform:none'>cargas resistivas<br>(hornos, calefacción)</small>") +
          lbl(740, 420, 280, "<span class='no'>AC-3</span><br><small style='font-size:24px;font-weight:600;text-transform:none'>motores jaula de ardilla<br>(arranque y paro en marcha)</small>") +
          caja(900, "La categoría de empleo dice <b>para qué carga</b> vale la corriente del contactor. Con un motor manda <b>AC-3</b>, que normalmente es menor que la de AC-1, "
                    "porque el contacto debe soportar la corriente de arranque y cortar con arco."),
          "IEC 60947-4-1 (categorías de empleo AC-1, AC-3, AC-4)"))
# 5 · colores IEC 60204-1
cols = "".join(f"<div class='fila'><div class='c' style='background:{c}'></div><span>{a}<small>{b}</small></span></div>" for c, a, b in (
    ("#111", "Negro", "circuitos de potencia en CA y CC"),
    ("#D92D20", "Rojo", "circuitos de mando en CA"),
    ("#1E4FD8", "Azul", "circuitos de mando en CC"),
    ("#F79009", "Naranja", "enclavamientos alimentados desde una fuente externa"),
    ("#5DB4F0", "Azul claro", "neutro"),
    ("repeating-linear-gradient(90deg,#2DA44E 0 18px,#F5D90A 18px 36px)", "Verde / amarillo", "conductor de protección (PE)")))
P.append(("grafito", "Tableros", "¿Por qué el mando va en <b>rojo</b> y la potencia en <em>negro</em>?",
          img(f"{EQ}/X0.png", 700, 330, h=300) +
          f"<div style='position:absolute;left:64px;top:360px;width:600px;font-size:32px;font-weight:600;line-height:1.3'>No es gusto: la norma de máquinas recomienda un color por función para que el que dé mantenimiento sepa qué toca.</div>" +
          f"<div style='position:absolute;left:64px;top:690px;width:960px'>{cols}</div>",
          "IEC 60204-1, 13.2.4 (colores recomendados de los conductores)"))
# 6 · curvas B C D
P.append(("azul", "Breakers", "Curva <b>B</b>, <b>C</b> o <b>D</b>: ¿cuál va con un motor?",
          img(f"{EQ}/QB.png", 150, 340, h=470) + img(f"{EQ}/QC.png", 450, 340, h=470) + img(f"{EQ}/QD.png", 750, 340, h=470) +
          lbl(100, 830, 280, "3 a 5 × In") + lbl(400, 830, 280, "5 a 10 × In") + lbl(700, 830, 280, "10 a 20 × In") +
          caja(930, "La letra es el rango del <b>disparo magnético</b> (instantáneo). <span class='cy'>B</span> cargas resistivas y cables largos, "
                    "<span class='cy'>C</span> uso general y motores, <span class='cy'>D</span> arranques muy pesados y transformadores."),
          "IEC 60898-1 (características de disparo instantáneo B, C y D)"))
# 7 · clase 10
P.append(("rojo", "Protecciones", "Relé térmico <b>clase 10</b>: ¿qué significa?",
          halo(560, 330, 520) + img(f"{EQ}/F3tr.png", 560, 380, w=460) +
          big(64, 360, 250, "10 s") +
          f"<div style='position:absolute;left:70px;top:620px;width:470px;font-size:32px;font-weight:700;line-height:1.3'>tiempo máximo de disparo<br>con <span class='am'>7,2 ×</span> la corriente ajustada</div>" +
          caja(930, "Partiendo en frío, un relé clase 10 debe disparar entre <b>4 y 10 s</b> a 7,2 veces su ajuste. "
                    "Clase 20 y 30 aguantan más: son para motores con arranques largos (ventiladores grandes, molinos)."),
          "IEC 60947-4-1 (clases de disparo de relés de sobrecarga)"))
# 8 · ajuste del térmico
P.append(("verde", "Protecciones", "¿A cuánto ajusto el <b>relé térmico</b>?",
          img(f"{EQ}/F3.png", 560, 340, w=460) +
          big(64, 350, 200, "26,5 A") +
          f"<div style='position:absolute;left:70px;top:570px;width:460px;font-size:32px;font-weight:700;line-height:1.3'>a la corriente de <span class='am'>PLACA</span> del motor, no a la del breaker</div>" +
          caja(900, "El NEC permite como máximo el <b>125 %</b> de la corriente de placa en motores con factor de servicio ≥ 1,15 "
                    "(115 % en los demás).<br><span class='cy'>Motor de 26,5 A × 1,25 = 33,1 A máximo.</span>"),
          "NEC 2020 430.32(A)(1) · placa Nidec U10P2D"))
# 9 · breaker 80 A
P.append(("azul", "Cálculo real", "¿Breaker de <b>80 A</b> para un motor de <em>26,5 A</em>?",
          img(f"{EQ5}/F2on.png", 90, 350, h=480) + img(f"{EQ}/F3.png", 560, 400, w=430) +
          lbl(90, 845, 350, "cortocircuito") + lbl(560, 845, 430, "sobrecarga") +
          caja(930, "El breaker del motor solo cuida el <b>cortocircuito</b>: se calcula hasta el <b>250 %</b> de la corriente de tabla (30,8 A → 77 A → 80 A). "
                    "La <b>sobrecarga</b> la cuida el relé térmico, ajustado a 26,5 A."),
          "NEC 2020 Tabla 430.250, Tabla 430.52 y 430.52(C)(1) Exc. 1"))
# 10 · pinza cero
P.append(("grafito", "Mediciones", "¿Por qué la pinza marca <b>0</b> en la manguera?",
          img(f"{EQ}/PZ0.png", 120, 330, h=520) + img(f"{EQ}/PZ.png", 600, 330, h=520) +
          lbl(60, 870, 420, "<span class='no'>✗ toda la manguera</span>") + lbl(540, 870, 420, "<span class='ok'>✓ un solo conductor</span>") +
          caja(960, "La pinza mide el campo magnético del conductor. En una manguera trifásica las tres corrientes suman <b>cero</b> y sus campos se cancelan. "
                    "Se abraza <b>un solo</b> conductor."),
          "principio de la pinza amperimétrica (ley de Ampère) · manuales de pinzas de corriente"))
# 11 · prueba en frío
P.append(("verde", "Puesta en marcha", "Antes de energizar: <b>la prueba</b> que te salva el tablero",
          img(f"{EQ}/MM.png", 640, 330, h=560) +
          f"<div style='position:absolute;left:64px;top:380px;width:540px;font-size:34px;font-weight:700;line-height:1.45'>Sin energía y con el breaker cerrado, en sus salidas:<br>"
          f"<span class='cy'>2 – 4</span> · <span class='cy'>4 – 6</span> · <span class='cy'>2 – 6</span><br>y cada fase contra <span class='am'>PE</span></div>" +
          caja(930, "Todas deben marcar <b>OL</b> (sin continuidad). Si el multímetro pita, hay un corto o un cable cruzado: "
                    "se corrige <b>antes</b> de cerrar el breaker con tensión."),
          "buena práctica de puesta en marcha; NFPA 70E (verificar ausencia de tensión antes de medir)"))
# 12 · 9 puntas
P.append(("morado", "Motores", "Motor de <b>9 puntas</b> a 208 V: ¿cómo lo conecto?",
          img(f"{EQ5}/CB.png", 560, 330, w=460) +
          f"<div style='position:absolute;left:64px;top:360px;width:470px;font-size:36px;font-weight:800;line-height:1.55'>"
          f"L1 → <span class='am'>T1 + T7</span><br>L2 → <span class='am'>T2 + T8</span><br>L3 → <span class='am'>T3 + T9</span><br><span class='cy'>T4 + T5 + T6</span> unidos</div>" +
          caja(930, "Es la conexión en <b>estrella de tensión baja</b> (dos estrellas en paralelo). En 460 V se unen T4-T7, T5-T8, T6-T9 "
                    "y la línea va a T1, T2 y T3. Confírmalo siempre con la placa de conexiones del motor."),
          "NEMA MG 1 (marcado de terminales de motores de 9 puntas) · placa Nidec U10P2D"))
# 13 · inversión de giro
P.append(("morado", "Arranques", "Para invertir el giro basta con <b>cambiar dos fases</b>",
          img(f"{EQ}/KM1on.png", 170, 350, h=470) + img(f"{EQ}/KM2.png", 590, 350, h=470) +
          lbl(120, 840, 360, "Adelante: L1 L2 L3") + lbl(540, 840, 380, "Atrás: L3 L2 L1") +
          caja(930, "Al cruzar dos fases el campo magnético del estator gira al revés y el motor también. En el tablero lo hacen "
                    "<b>dos contactores</b>: -KM1 conecta en orden y -KM2 cruza L1 con L3."),
          "IEC 60034-8 (sentido de giro y marcado de terminales)"))
# 14 · enclavamiento
P.append(("rojo", "Seguridad", "El <b>contacto NC</b> que evita un cortocircuito",
          img(f"{EQ}/KM1on.png", 170, 350, h=470) + img(f"{EQ}/KM2.png", 590, 350, h=470) +
          f"<div style='position:absolute;left:420px;top:520px;font-size:120px;font-weight:900;color:#FF5A5F'>✗</div>" +
          caja(900, "Si -KM1 y -KM2 cierran juntos, dos fases quedan en <b>corto</b>. Por eso el NC de cada contactor va en serie con la bobina del otro "
                    "(<b>enclavamiento eléctrico</b>) y se suma un bloque <b>mecánico</b> que impide que ambos cierren."),
          "esquemas de inversión de giro de fabricantes (enclavamiento eléctrico y mecánico) · IEC 60947-4-1"))
# 15 · paro de emergencia
P.append(("rojo", "Seguridad", "¿Por qué el paro de emergencia es <b>rojo sobre amarillo</b>?",
          halo(270, 330, 560) + img(f"{EQ}/S3.png", 330, 350, h=520) +
          caja(930, "Para verlo al instante en una emergencia. Además se <b>enclava</b> al presionarlo: la máquina no vuelve a arrancar hasta "
                    "desenclavarlo y dar un nuevo arranque. Nunca se usa como paro normal."),
          "IEC 60204-1, 10.7 · ISO 13850 (función de paro de emergencia)"))
# 16 · autoenclavamiento
P.append(("verde", "Mando", "¿Por qué el motor sigue encendido si <b>sueltas el botón</b>?",
          img(f"{EQ}/S1.png", 80, 360, h=330) + img(f"{EQ}/KM1on.png", 380, 330, h=520) + img(f"{EQ}/S0.png", 800, 360, h=330) +
          caja(930, "El contacto NA <b>13-14</b> del contactor va en paralelo con el pulsador de arranque: cuando la bobina cierra, ese contacto "
                    "la mantiene alimentada. Eso es el <b>autoenclavamiento</b>. El paro, un NC en serie, lo rompe."),
          "esquema de arranque directo IEC (mando con autoenclavamiento)"))
# 17 · factor de servicio
P.append(("azul", "Motores", "Factor de servicio <b>1,25</b>: ¿más potencia gratis?",
          img(f"{EQ5}/M1.png", 120, 380, w=840) + big(700, 300, 150, "1,25") +
          caja(900, "Significa que el motor puede trabajar de forma continua al <b>125 %</b> de su potencia nominal, a tensión y frecuencia nominales, "
                    "pero con <b>más calentamiento</b> y menos vida del aislamiento. Es un margen, no una potencia extra."),
          "NEMA MG 1 (factor de servicio) · placa Nidec U10P2D: F.S. 1,25"))
# 18 · 1760 rpm
P.append(("grafito", "Motores", "¿Por qué <b>1760 rpm</b> y no 1800?",
          img(f"{EQ5}/M1.png", 160, 540, w=760) +
          f"<div style='position:absolute;left:64px;top:360px;width:952px;font-size:44px;font-weight:800;line-height:1.35'>"
          f"n<sub>s</sub> = 120 × <span class='am'>60 Hz</span> ÷ <span class='am'>4 polos</span> = <span class='cy'>1800 rpm</span><br>"
          f"deslizamiento = (1800 − 1760) ÷ 1800 = <span class='am'>2,2 %</span></div>" +
          caja(990, "El rotor siempre gira un poco más lento que el campo: esa diferencia induce la corriente que produce el par."),
          "teoría del motor de inducción · placa Nidec U10P2D (1760 rpm, 60 Hz)"))
# 19 · eficiencia
P.append(("verde", "Motores", "Eficiencia <b>91,7 %</b>: ¿cuánto se pierde en calor?",
          img(f"{EQ5}/M1.png", 160, 560, w=760) +
          f"<div style='position:absolute;left:64px;top:360px;width:952px;font-size:40px;font-weight:800;line-height:1.4'>"
          f"Salida: 10 hp = <span class='cy'>7,46 kW</span><br>Entrada: 7,46 ÷ 0,917 = <span class='am'>8,13 kW</span><br>"
          f"Pérdidas: ≈ <span class='no'>0,68 kW</span> en calor</div>" +
          caja(1000, "Ese calor sale por las aletas y el ventilador: por eso un motor <b>TEFC</b> sucio o tapado se recalienta."),
          "placa Nidec U10P2D (10 hp, Ef. 91,7 %, TEFC) · 1 hp = 745,7 W"))
# 20 · guardamotor
P.append(("azul", "Protecciones", "Guardamotor: <b>tres funciones</b> en un aparato",
          halo(560, 320, 520) + img(f"{EQ}/QM1.png", 620, 340, h=560) +
          f"<div style='position:absolute;left:64px;top:380px;width:520px;font-size:34px;font-weight:700;line-height:1.5'>"
          f"<span class='am'>1</span> Seccionamiento manual (ON/OFF)<br><span class='am'>2</span> Disparo magnético: cortocircuito<br>"
          f"<span class='am'>3</span> Disparo térmico ajustable: sobrecarga</div>" +
          caja(960, "Reemplaza al breaker más el relé térmico. Pero no sustituye al <b>contactor</b>: para arrancar y parar con pulsadores "
                    "o con un PLC sigue haciendo falta."),
          "IEC 60947-2 / 60947-4-1 (interruptores de protección de motor) · catálogos de guardamotores"))

JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
const n=parseInt(process.argv[2]);for(let i=1;i<=n;i++){const k=String(i).padStart(2,'0');await p.goto('file://'+process.cwd()+'/html/post_'+k+'.html');
await p.waitForTimeout(250);await p.screenshot({path:'png/post_'+k+'.png'});}await b.close()})();"""

if __name__ == "__main__":
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    for i, (tema, tag, tit, cuerpo, fuente) in enumerate(P, 1):
        h = pagina(i, tema, tag, tit, cuerpo, fuente).replace("src='eq/", "src='../eq/").replace("src='../h01v5_eq/", "src='../../h01v5_eq/")
        (AQ / "html" / f"post_{i:02d}.html").write_text(h)
    (AQ / "shot.js").write_text(JS)
    subprocess.run(["node", "shot.js", str(len(P))], cwd=AQ, check=True)
    print(len(P))

"""20 publicaciones v2 (24-nov): FONDO BLANCO estilo de las referencias del usuario (banda superior con pregunta, título en
dos líneas con cinta inclinada, texto explicativo, equipo grande con FLECHAS punteadas que señalan sus partes, logo ME. abajo a la
izquierda y sello "¿Sabías esto?…" abajo a la derecha) + fuente al pie. Equipos del catálogo (../arr_eq). Fuente Oswald (OFL).
Datos: ver docstring de gen_posts.py (IEC 60947-4-1, 60898-1, 60204-1, EN 50005, NEC 2020 430, NEMA MG 1, DIN 46228-4, placa Nidec).
Uso: python3 gen_posts2.py → png2/post_XX.png"""
import json, subprocess, pathlib
from PIL import Image

AQ = pathlib.Path(__file__).resolve().parent
EQ = AQ.parent / "arr_eq"
TEMAS = [("#0E7C86", "#0B3A8C"), ("#5B21B6", "#3B0F7A"), ("#0B6BCB", "#0A2E6E"), ("#B42318", "#7A1A12")]

CSS = """
@font-face{font-family:Osw;src:url(../fonts/oswald-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:Osw;src:url(../fonts/oswald-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:Osw;src:url(../fonts/oswald-latin-700-normal.woff2);font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;background:#fff;font-family:Inter;color:#101828;position:relative}
.band{position:absolute;left:0;top:0;width:1080px;height:96px;display:flex;align-items:center;justify-content:center;font-family:Osw;font-weight:500;font-size:40px;color:#fff}
.t1{position:absolute;left:0;width:1080px;text-align:center;font-family:Osw;font-weight:600;font-size:66px;line-height:1.05}
.rib{position:absolute;left:50%;transform:translateX(-50%) skewX(-14deg);padding:4px 46px 8px;font-family:Osw;font-weight:600;font-size:56px;color:#fff;white-space:nowrap}
.rib span{display:inline-block;transform:skewX(14deg)}
.txt{position:absolute;left:60px;width:960px;font-size:28px;line-height:1.38;text-align:justify}
.txt b{font-weight:800}
img.eq{position:absolute;filter:drop-shadow(0 10px 14px rgba(16,24,40,.22))}
.lb{position:absolute;background:#fff;border:2.5px solid VAR1;border-radius:10px;padding:5px 12px;font-size:23px;font-weight:700;line-height:1.15;white-space:nowrap;box-shadow:0 4px 10px rgba(16,24,40,.12)}
.lb small{display:block;font-weight:500;font-size:19px;color:#475467}
.fu{position:absolute;left:60px;right:60px;bottom:120px;font-size:18px;color:#667085;border-top:1.5px solid #EAECF0;padding-top:10px}
.logo{position:absolute;left:52px;bottom:34px;height:66px}
.sello{position:absolute;right:40px;bottom:34px;display:flex;align-items:center}
.sello .ic{width:78px;height:78px;border-radius:50%;background:#fff;border:5px solid VAR1;display:flex;align-items:center;justify-content:center;z-index:2}
.sello .p{margin-left:-24px;padding:10px 26px 12px 36px;background:VAR1;color:#fff;font-family:Osw;font-weight:500;font-size:34px;transform:skewX(-12deg)}
.sello .p span{display:inline-block;transform:skewX(12deg)}
.box{position:absolute;border-radius:14px;padding:14px 20px;font-size:26px;line-height:1.3}
"""

BOMBILLA = ("<svg width='44' height='44' viewBox='0 0 24 24' fill='none' stroke='VAR1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
            "<path d='M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z'/>"
            "<path d='M12 7v3M10.5 9.5 12 11l1.5-1.5' /></svg>")


def tam(n):
    return Image.open(EQ / f"{n}.png").size


def punto(im, ref):
    """im = (nombre, left, top, width). ref = (fx, fy) o clave del JSON (mm)."""
    n, x, y, w = im
    W, H = tam(n)
    h = w * H / W
    if isinstance(ref, str):
        d = json.loads((EQ / f"{n}.json").read_text())
        m = d["margen"]
        bx, by = d["bornes"][ref]
        fx, fy = (m + bx) / (d["W"] + 2 * m), (m + by) / (d["H"] + 2 * m)
    else:
        fx, fy = ref
    return x + fx * w, y + fy * h


def pagina(n, tema, banda, t1, rib, texto, y_txt, imgs, flechas, fuente, extra="", y_t1=120, y_rib=200):
    c1, c2 = TEMAS[tema]
    css = CSS.replace("VAR1", c1)
    h = [f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>",
         f"<div class='band' style='background:{c2}'>{banda}</div>",
         f"<div class='t1' style='top:{y_t1}px;color:{c1}'>{t1}</div>",
         f"<div class='rib' style='top:{y_rib}px;background:{c1}'><span>{rib}</span></div>",
         f"<div class='txt' style='top:{y_txt}px;color:{c1 if tema != 3 else '#101828'}'>{texto}</div>"]
    for (nm, x, y, w) in imgs:
        h.append(f"<img class='eq' src='../../arr_eq/{nm}.png' style='left:{x}px;top:{y}px;width:{w}px'>")
    svg = [f"<svg id='fl' style='position:absolute;left:0;top:0' width='1080' height='1350'><defs><marker id='ah' markerWidth='12' markerHeight='12' refX='9' refY='6' orient='auto'>"
           f"<path d='M0,0 L12,6 L0,12 Z' fill='{c1}'/></marker></defs>"]
    labs = []
    for i, ref, lab, (lx, ly), lado in flechas:
        px, py = punto(imgs[i], ref) if isinstance(i, int) else i(ref)
        tr = {"r": "translate(-100%,-50%)", "l": "translate(0,-50%)", "b": "translate(-50%,-100%)", "t": "translate(-50%,0)"}[lado]
        labs.append(f"<div class='lb' data-x='{px:.0f}' data-y='{py:.0f}' style='left:{lx}px;top:{ly}px;transform:{tr}'>{lab}</div>")
    svg.append("</svg>")
    h += svg + labs + [extra,
                       f"<div class='fu'>Fuente: {fuente}</div>",
                       "<img class='logo' src='../../logo_oficial.png'>",
                       f"<div class='sello'><div class='ic'>{BOMBILLA.replace('VAR1', c1)}</div><div class='p'><span>¿Sabías esto?...</span></div></div>" + JSF.replace("VARC", c1) + "</body></html>"]
    return "".join(h)


JSF = """<script>
const C='VARC';const sv=document.getElementById('fl');
document.querySelectorAll('.lb[data-x]').forEach(l=>{let r=l.getBoundingClientRect();
 let dx=0,dy=0; if(r.left<16)dx=16-r.left; if(r.right>1064)dx=1064-r.right; if(r.top<104)dy=104-r.top; if(r.bottom>1190)dy=1190-r.bottom;
 if(dx||dy){l.style.marginLeft=dx+'px';l.style.marginTop=dy+'px';r=l.getBoundingClientRect();}
 const px=+l.dataset.x,py=+l.dataset.y;let sx,sy;
 if(px<r.left){sx=r.left;sy=(r.top+r.bottom)/2}else if(px>r.right){sx=r.right;sy=(r.top+r.bottom)/2}else if(py>r.bottom){sx=(r.left+r.right)/2;sy=r.bottom}else{sx=(r.left+r.right)/2;sy=r.top}
 const cx=(sx+px)/2+(Math.abs(px-sx)>Math.abs(py-sy)?0:30),cy=(sy+py)/2-(Math.abs(px-sx)>Math.abs(py-sy)?35:0);
 const ns='http://www.w3.org/2000/svg';const pa=document.createElementNS(ns,'path');pa.setAttribute('d',`M${sx},${sy} Q${cx},${cy} ${px},${py}`);
 pa.setAttribute('fill','none');pa.setAttribute('stroke',C);pa.setAttribute('stroke-width','4');pa.setAttribute('stroke-dasharray','10 8');pa.setAttribute('marker-end','url(#ah)');sv.appendChild(pa);
 const ci=document.createElementNS(ns,'circle');ci.setAttribute('cx',px);ci.setAttribute('cy',py);ci.setAttribute('r','7');ci.setAttribute('fill','#fff');ci.setAttribute('stroke',C);ci.setAttribute('stroke-width','4');sv.appendChild(ci);});
</script>"""


def caja(x, y, w, html, col, fondo="#F2F4F7"):
    return f"<div class='box' style='left:{x}px;top:{y}px;width:{w}px;background:{fondo};border-left:8px solid {col}'>{html}</div>"



def DG(ref):
    """Punto del diagrama de mando del usuario (400 × 708) dibujado con alto 740 en (330, 420)."""
    k = 740 / 708
    return 330 + ref[0] * k, 420 + ref[1] * k


P = []
# 01 partes del disyuntor
P.append(dict(tema=2, banda="¿Qué te dice el frente de un disyuntor?", t1="Partes de un", rib="DISYUNTOR (BREAKER)",
              texto="Todo lo que necesitas para elegirlo viene impreso: la <b>curva</b> y la <b>corriente nominal</b> (C80), la capacidad de corte "
                    "<b>Icn</b>, la tensión <b>Ue</b> y la norma. La ventana verde indica que está cerrado.", y_txt=300,
              imgs=[("F2on", 330, 450, 420)],
              fl=[(0, (0.2, 0.33), "C80<small>curva C · 80 A</small>", (250, 560), "r"),
                  (0, (0.22, 0.25), "Ventana indicadora<small>verde = cerrado</small>", (250, 470), "r"),
                  (0, (0.5, 0.47), "Manijas ON / OFF<small>unidas: 3 polos</small>", (830, 720), "l"),
                  (0, "1", "Entrada 1 · 3 · 5", (830, 480), "l"),
                  (0, "2", "Salida 2 · 4 · 6", (250, 1020), "r"),
                  (0, (0.5, 0.66), "Etiqueta -F2", (830, 880), "l"),
                  (0, (0.15, 0.4), "Ue · norma · Icn · Uimp", (250, 680), "r")],
              fuente="IEC 60898-1 (marcado de interruptores automáticos) · NEC 2020 430.52"))
# 02 partes del relé térmico
P.append(dict(tema=0, banda="¿Para qué es cada botón del relé térmico?", t1="Partes del", rib="RELÉ TÉRMICO",
              texto="Se monta debajo del contactor con sus pines <b>1/L1 3/L2 5/L3</b>. El dial se ajusta a la <b>corriente de placa</b> del motor "
                    "y los contactos 95-96 (NC) y 97-98 (NA) van al mando.", y_txt=300,
              imgs=[("F3", 270, 470, 540)],
              fl=[(0, (0.27, 0.32), "Dial de ajuste<small>23–32 A</small>", (230, 560), "r"),
                  (0, (0.13, 0.44), "TEST<small>simula el disparo</small>", (230, 700), "r"),
                  (0, (0.7, 0.42), "STOP", (860, 560), "l"),
                  (0, (0.88, 0.42), "RESET H / A<small>manual o automático</small>", (860, 680), "l"),
                  (0, "96", "95-96 NC<small>abre con sobrecarga</small>", (860, 840), "l"),
                  (0, "97", "97-98 NA<small>luz de falla</small>", (230, 840), "r"),
                  (0, "4/T2", "Salidas al motor", (540, 1060), "t")],
              fuente="IEC 60947-4-1 · NEC 2020 430.32(A)(1) · hoja de datos de relés tipo NR2"))
# 03 relé por dentro
P.append(dict(tema=3, banda="¿Cómo mide la corriente un relé térmico?", t1="Así es el relé térmico", rib="POR DENTRO",
              texto="Cada fase pasa por un <b>calefactor</b> enrollado en una <b>lámina bimetálica</b>. Con sobrecarga la lámina se curva, empuja "
                    "la <b>regleta</b> y el mecanismo abre el <b>95-96</b>: el contactor suelta.", y_txt=300,
              imgs=[("rc_tr", 200, 450, 680)],
              fl=[(0, "calefactor", "Calefactor de cobre", (150, 640), "r"),
                  (0, "bimetal", "Lámina bimetálica<small>se curva con el calor</small>", (150, 900), "r"),
                  (0, "regleta", "Regleta de disparo", (560, 445), "b"),
                  (0, "nc", "95-96 NC: abre", (930, 600), "l"),
                  (0, "no", "97-98 NA: cierra", (930, 730), "l"),
                  (0, "resorte", "Resorte del mecanismo", (930, 880), "l")],
              fuente="IEC 60947-4-1 · catálogos de relés de sobrecarga (Schneider TeSys, Siemens 3RU2) · vista en corte ilustrativa"))
# 04 partes del contactor (numeración)
P.append(dict(tema=0, banda="¿Qué significa cada número del contactor?", t1="Bornes del", rib="CONTACTOR",
              texto="Principales: <b>1/L1 3/L2 5/L3</b> entran y <b>2/T1 4/T2 6/T3</b> salen. Auxiliares: segundo dígito <b>3-4 = NA</b>, "
                    "<b>1-2 = NC</b>. La bobina siempre es <b>A1-A2</b>.", y_txt=300,
              imgs=[("KM1", 340, 440, 400)],
              fl=[(0, "1/L1", "Entradas 1/L1 3/L2 5/L3", (280, 470), "r"),
                  (0, "13", "13-14 NA", (280, 610), "r"),
                  (0, "21", "21-22 NC", (800, 560), "l"),
                  (0, "A1", "Bobina A1-A2", (800, 640), "l"),
                  (0, "14", "14 (NA)", (280, 860), "r"),
                  (0, "22", "22 (NC)", (800, 860), "l"),
                  (0, "6/T3", "Salidas 2/T1 4/T2 6/T3", (800, 1050), "l")],
              fuente="EN 50005 / IEC 60947-1 (marcado de bornes)"))
# 05 bobina por dentro
P.append(dict(tema=1, banda="¿Cómo mueve una bobina pequeña contactos tan grandes?", t1="La bobina del contactor", rib="POR DENTRO",
              texto="Al energizar <b>A1-A2</b> el núcleo se vuelve electroimán y atrae a la <b>armadura</b>, que cierra los contactos. La "
                    "<b>espira de sombra</b> evita que zumbe en corriente alterna.", y_txt=300,
              imgs=[("bc_on", 290, 430, 500)],
              fl=[(0, "contacto", "Contactos cerrados", (180, 470), "r"),
                  (0, "armadura", "Armadura móvil", (900, 560), "l"),
                  (0, "bobina", "Bobina de cobre", (180, 760), "r"),
                  (0, "espira", "Espira de sombra", (180, 650), "r"),
                  (0, "nucleo", "Núcleo en E laminado", (900, 900), "l"),
                  (0, "resorte", "Resorte de retorno", (900, 740), "l"),
                  (0, "A1", "A1", (180, 1030), "r")],
              fuente="Schneider Electric FAQ FA129583 (VA de llamada y de mantenimiento) · manuales de contactores · vista en corte ilustrativa"))
# 06 guardamotor
P.append(dict(tema=2, banda="¿Guardamotor o breaker + relé térmico?", t1="Partes del", rib="GUARDAMOTOR",
              texto="Junta <b>seccionamiento</b>, disparo <b>magnético</b> (cortocircuito) y <b>térmico ajustable</b> (sobrecarga). No reemplaza "
                    "al contactor: para arrancar con pulsadores o un PLC, sigue haciendo falta.", y_txt=300,
              imgs=[("QM1on", 370, 440, 340)],
              fl=[(0, (0.2, 0.47), "Dial de ajuste térmico", (300, 640), "r"),
                  (0, (0.6, 0.46), "Rango 22–32 A", (780, 560), "l"),
                  (0, (0.6, 0.63), "Mando ON / OFF", (780, 760), "l"),
                  (0, (0.12, 0.62), "TEST", (300, 800), "r"),
                  (0, "13", "Aux. 13-14 NA", (300, 480), "r"),
                  (0, "21", "Aux. 21-22 NC", (780, 470), "l"),
                  (0, (0.2, 0.37), "CLASS 10", (300, 560), "r")],
              fuente="IEC 60947-2 / 60947-4-1 · catálogos de guardamotores (WEG MPW40 como referencia de forma)"))
# 07 paro de emergencia
P.append(dict(tema=3, banda="¿Por qué el paro de emergencia es así?", t1="Paro de", rib="EMERGENCIA",
              texto="Actuador <b>rojo</b> sobre fondo <b>amarillo</b> para verlo al instante. Se <b>enclava</b> al presionarlo: la máquina no "
                    "arranca hasta desenclavarlo (girar) y dar un nuevo arranque. Nunca es el paro normal.", y_txt=300,
              imgs=[("S3", 330, 460, 420)],
              fl=[(0, (0.45, 0.58), "Hongo rojo<small>se enclava</small>", (230, 620), "r"),
                  (0, (0.1, 0.78), "Fondo amarillo", (230, 940), "r"),
                  (0, (0.6, 0.62), "Flecha: girar para desenclavar", (860, 760), "l"),
                  (0, (0.5, 0.15), "Portaetiqueta -S3", (860, 500), "l")],
              fuente="IEC 60204-1, 10.7 · ISO 13850"))
# 08 pinza
P.append(dict(tema=0, banda="¿Por qué la pinza marca cero en la manguera?", t1="Cómo se mide con la", rib="PINZA AMPERIMÉTRICA",
              texto="La mordaza es un núcleo magnético que mide el campo del conductor. En una manguera trifásica las corrientes suman <b>cero</b>. "
                    "Abraza <b>un solo conductor</b>.", y_txt=300,
              imgs=[("PZ26", 420, 440, 240)],
              fl=[(0, (0.5, 0.1), "Mordaza: un solo conductor", (820, 470), "l"),
                  (0, (0.62, 0.52), "Selector en A~", (820, 700), "l"),
                  (0, (0.5, 0.74), "Lectura 26,4 A", (260, 880), "r"),
                  (0, (0.05, 0.42), "Gatillo para abrir", (260, 680), "r")],
              fuente="principio de la pinza amperimétrica (ley de Ampère) · manuales de pinzas de corriente"))
# 09 multímetro prueba en frío
P.append(dict(tema=2, banda="Antes de energizar el tablero", t1="La prueba en frío con el", rib="MULTÍMETRO",
              texto="Sin energía y con el breaker cerrado, mide continuidad en sus salidas: <b>2-4, 4-6, 2-6</b> y cada fase contra <b>PE</b>. "
                    "Todo debe marcar <b>OL</b>. Si suena, hay un corto.", y_txt=300,
              imgs=[("MMol", 380, 440, 320)],
              fl=[(0, (0.5, 0.2), "Pantalla: OL = abierto", (300, 520), "r"),
                  (0, (0.83, 0.55), "Continuidad →|", (780, 640), "l"),
                  (0, (0.5, 0.62), "Selector", (300, 760), "r"),
                  (0, (0.5, 0.88), "COM (negra)", (300, 1000), "r"),
                  (0, (0.78, 0.88), "VΩ (roja)", (780, 1000), "l")],
              fuente="buena práctica de puesta en marcha · NFPA 70E (verificar ausencia de tensión)"))
# 10 caja de 9 puntas
P.append(dict(tema=1, banda="Motor de 9 puntas a 208 V", t1="Conexión en", rib="ESTRELLA DOBLE (BAJA)",
              texto="<b>L1 → T1+T7 · L2 → T2+T8 · L3 → T3+T9</b> y <b>T4+T5+T6</b> unidos. En 460 V se unen T4-T7, T5-T8, T6-T9 y la "
                    "línea va a T1, T2 y T3. Confírmalo con la placa del motor.", y_txt=300,
              imgs=[("CB", 300, 450, 480)],
              fl=[(0, "T1", "L1", (220, 520), "r"), (0, "T2", "L2", (540, 450), "b"), (0, "T3", "L3", (860, 520), "l"),
                  (0, "T7", "T7 con T1", (220, 720), "r"), (0, "T9", "T9 con T3", (860, 720), "l"),
                  (0, "T5", "T4 + T5 + T6 unidos", (540, 1080), "t")],
              fuente="NEMA MG 1 (marcado de terminales) · placa Nidec U10P2D"))
# 11 placa del motor
P.append(dict(tema=0, banda="¿Qué dice la placa del motor?", t1="Lee la", rib="PLACA DEL MOTOR",
              texto="10 hp · 208-230/460 V · <b>26,5</b>/23,9/12 A · <b>1760 rpm</b> · F.S. <b>1,25</b> · Ef. <b>91,7 %</b>. Con la corriente de "
                    "placa se ajusta el térmico; con la de la tabla del NEC se calculan cable y breaker.", y_txt=300,
              imgs=[("M1", 140, 470, 800)],
              fl=[(0, (0.79, 0.47), "Placa de datos", (900, 460), "b"),
                  (0, (0.5, 0.26), "Caja de conexiones", (300, 460), "b"),
                  (0, (0.1, 0.5), "Eje", (130, 900), "t"),
                  (0, (0.9, 0.5), "Ventilador (TEFC)", (930, 900), "t")],
              extra=caja(60, 990, 960, "<b>1760 rpm:</b> 120 × 60 Hz ÷ 4 polos = 1800 rpm síncronas → deslizamiento 2,2 %.", "#0E7C86"),
              fuente="placa Nidec U10P2D · NEMA MG 1 · NEC 2020 Tabla 430.250"))
# 12 curvas B C D
P.append(dict(tema=2, banda="¿Qué curva va con un motor?", t1="Curvas", rib="B · C · D",
              texto="La letra es el rango del <b>disparo magnético</b>: B de 3 a 5 × In, C de 5 a 10 × In, D de 10 a 20 × In. Para motores, "
                    "<b>C</b> en general y <b>D</b> para arranques muy pesados.", y_txt=300,
              imgs=[("QB", 170, 470, 170), ("QC", 455, 470, 170), ("QD", 740, 470, 170)],
              fl=[(0, (0.3, 0.35), "B: 3–5 × In", (255, 1030), "t"), (1, (0.3, 0.35), "C: 5–10 × In", (540, 1030), "t"),
                  (2, (0.3, 0.35), "D: 10–20 × In", (825, 1030), "t")], fuente="IEC 60898-1 (disparo instantáneo B, C y D)"))
# 13 estrella-delta
P.append(dict(tema=1, banda="Arranque estrella-delta", t1="Arranca con", rib="UN TERCIO DE LA CORRIENTE",
              texto="En estrella cada bobina recibe la tensión de línea <b>÷ √3</b>: corriente y par de arranque bajan a <b>1/3</b>. El "
                    "temporizador -KT1 pasa a triángulo con una pausa de unos <b>50 ms</b>.", y_txt=300,
              imgs=[("KM1on", 90, 470, 270), ("KM3on", 405, 470, 270), ("KM2", 720, 470, 270)],
              fl=[(0, (0.5, 0.42), "Línea", (225, 1020), "t"), (1, (0.5, 0.42), "Estrella", (540, 1020), "t"),
                  (2, (0.5, 0.42), "Triángulo", (855, 1020), "t")],
              fuente="teoría de máquinas (IY = IΔ/3) · Eaton ETR4 (pausa 50 ms) · IEC 60947-4-1"))
# 14 inversión de giro
P.append(dict(tema=1, banda="Inversión de giro", t1="Basta con", rib="CRUZAR DOS FASES",
              texto="-KM1 conecta <b>L1 L2 L3</b> en orden; -KM2 cruza <b>L1 con L3</b>. L2 pasa igual por los dos. El campo del estator "
                    "gira al revés y el motor también.", y_txt=300,
              imgs=[("KM1on", 170, 520, 330), ("KM2", 580, 520, 330)],
              fl=[(0, "1/L1", "L1", (250, 450), "b"), (0, "5/L3", "L3", (440, 450), "b"), (1, "1/L1", "L3", (660, 450), "b"), (1, "5/L3", "L1", (850, 450), "b")],
              extra=caja(60, 1000, 960, "<b>Siempre con enclavamiento:</b> si cierran los dos a la vez, L1 y L3 quedan en corto.", "#B42318"),
              fuente="IEC 60034-8 (sentido de giro)"))
# 15 enclavamiento
P.append(dict(tema=3, banda="Inversión de giro segura", t1="El contacto NC que", rib="EVITA UN CORTO",
              texto="El <b>21-22</b> (NC) de -KM1 va en serie con la bobina de -KM2, y el de -KM2 con la de -KM1: si uno está cerrado, el otro "
                    "no puede cerrar. Además, un <b>bloque mecánico</b> entre los dos.", y_txt=300,
              imgs=[("KM1on", 170, 500, 330), ("KM2", 580, 500, 330)],
              fl=[(0, "21", "21-22 de -KM1", (260, 1040), "t"), (1, "21", "21-22 de -KM2", (820, 1040), "t")],
              fuente="esquemas de inversión de fabricantes (enclavamiento eléctrico y mecánico) · IEC 60947-4-1"))
# 16 puntera
P.append(dict(tema=0, banda="¿Para qué sirve la puntera?", t1="La", rib="PUNTERA (FERRULE)",
              texto="Sin puntera, los hilos del cable flexible se abren bajo el tornillo. La puntera los compacta en una pieza que el borne aprieta "
                    "completa. El <b>color del collar</b> indica la sección (DIN 46228-4).", y_txt=300,
              imgs=[("pt_hilos", 120, 470, 840), ("pt_azul", 120, 760, 840)],
              fl=[(0, (0.75, 0.35), "Sin puntera: hilos abiertos", (760, 460), "b"),
                  (1, "collar", "Collar de color", (420, 1000), "t"),
                  (1, "tubo", "Tubo de cobre estañado, crimpado", (760, 1000), "t"),
                  (1, "aislamiento", "Aislamiento", (200, 1000), "t")],
              fuente="DIN 46228-4 · Phoenix Contact, guía de punteras"))
# 17 colores IEC
P.append(dict(tema=2, banda="¿Por qué los cables del tablero tienen colores?", t1="Colores del", rib="CABLEADO IEC 60204-1",
              texto="La norma de máquinas recomienda un color por función, para que el que da mantenimiento sepa qué toca sin adivinar.",
              y_txt=300, imgs=[], fl=[],
              extra="".join(caja(60, 430 + i * 92, 960, f"<b>{a}</b> · {b}", c, "#F9FAFB") for i, (c, a, b) in enumerate((
                  ("#111111", "Negro", "potencia en CA y CC"), ("#D92D20", "Rojo", "mando en CA"), ("#1E4FD8", "Azul", "mando en CC"),
                  ("#F79009", "Naranja", "enclavamientos alimentados desde otra fuente"), ("#5DB4F0", "Azul claro", "neutro"),
                  ("#2DA44E", "Verde / amarillo", "solo el conductor de protección (PE)")))),
              fuente="IEC 60204-1, 13.2.4"))
# 18 autoenclavamiento (sobre el diagrama del usuario)
P.append(dict(tema=0, banda="¿Por qué el motor sigue encendido si sueltas el botón?", t1="Simple, pero", rib="INQUEBRANTABLE",
              texto="El NA <b>13-14</b> del contactor va en paralelo con el pulsador de arranque: al cerrar, mantiene alimentada su propia bobina. "
                    "El paro, un NC en serie, rompe la retención.", y_txt=300, imgs=[],
              extra="<img src='../../../referencias/diagramas_h01/mando_original.png' style='position:absolute;left:330px;top:420px;height:740px'>",
              fl=[(DG, (137, 441), "Arranque 13-14 (NA)", (200, 760), "r"), (DG, (227, 441), "KM1 13-14<small>retención</small>", (880, 760), "l"),
                  (DG, (137, 335), "Paro 11-12 (NC)", (200, 640), "r"), (DG, (137, 591), "Bobina A1-A2", (200, 960), "r")],
              fuente="diagrama de mando del canal (arranque directo IEC con autoenclavamiento)"))
# 19 AC-1 vs AC-3
P.append(dict(tema=3, banda="Mi motor es de 26,5 A y el contactor de 32 A…", t1="¿Por qué", rib="NO ALCANZA?",
              texto="La corriente del contactor depende de la <b>categoría de empleo</b>. Para motores manda <b>AC-3</b> (arranque y corte con "
                    "arco), que es menor que la de AC-1 (resistencias). Para 10 hp a 208 V va uno de <b>38 A</b>.", y_txt=300,
              imgs=[("KM1", 360, 480, 360)],
              fl=[], extra=caja(60, 500, 280, "<b>AC-1</b><br>hornos y calefacción", "#039855") + caja(740, 500, 280, "<b>AC-3</b><br>motores de jaula", "#B42318"),
              fuente="IEC 60947-4-1 · NEC 2020 Tabla 430.250 (10 hp, 208 V: 30,8 A)"))
# 20 breaker 80 A
P.append(dict(tema=2, banda="¿Breaker de 80 A para un motor de 26,5 A?", t1="Cada protección", rib="CUIDA ALGO DISTINTO",
              texto="El breaker cuida el <b>cortocircuito</b>: hasta 250 % de la corriente de tabla (30,8 A → 77 A → <b>80 A</b>). La "
                    "<b>sobrecarga</b> la cuida el relé térmico ajustado a 26,5 A.", y_txt=300,
              imgs=[("F2on", 120, 470, 360), ("F3", 560, 520, 420)],
              fl=[(0, (0.5, 0.5), "Cortocircuito", (300, 1060), "t"), (1, (0.27, 0.32), "Sobrecarga: 26,5 A", (770, 1060), "t")],
              fuente="NEC 2020 Tabla 430.250, Tabla 430.52 y 430.52(C)(1) Exc. 1 · 430.32(A)(1)"))

JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
const n=parseInt(process.argv[2]);for(let i=1;i<=n;i++){const k=String(i).padStart(2,'0');await p.goto('file://'+process.cwd()+'/html2/post_'+k+'.html');
await p.waitForTimeout(350);await p.screenshot({path:'png2/post_'+k+'.png'});}await b.close()})();"""

if __name__ == "__main__":
    (AQ / "html2").mkdir(exist_ok=True)
    (AQ / "png2").mkdir(exist_ok=True)
    for i, d in enumerate(P, 1):
        h = pagina(i, d["tema"], d["banda"], d["t1"], d["rib"], d["texto"], d["y_txt"], d["imgs"], d["fl"], d["fuente"], d.get("extra", ""))
        (AQ / "html2" / f"post_{i:02d}.html").write_text(h)
    (AQ / "shot2.js").write_text(JS)
    subprocess.run(["node", "shot2.js", str(len(P))], cwd=AQ, check=True)
    print(len(P))

"""Publicaciones v3 (25-nov): FOTOS REALES de Wikimedia Commons (licencias libres, con crédito) + partes encerradas en
rectángulos numerados + leyenda técnica. 4 estilos: PARTES · ¿SABÍAS QUÉ? · DATO INTERESANTE · COMPARACIÓN.
Marco metálico con remaches y panel blanco (estilo de las referencias del usuario), sin preguntas de trivia.
Fotos en fotos/ (descargadas con el navegador del usuario; ver CREDITOS). Uso: python3 gen.py → png/"""
import subprocess, pathlib
AQ = pathlib.Path(__file__).resolve().parent

C = dict(nav="#0B2545", az="#1565C0", nar="#F08C00", ver="#12804A", roj="#C62828", gri="#475467")
CAT = {"partes": ("PARTES DE UN COMPONENTE", C["az"]), "sabias": ("¿SABÍAS QUÉ?", C["nar"]),
       "dato": ("DATO INTERESANTE", C["ver"]), "comp": ("COMPARACIÓN", "#6D28D9")}
BOX = ["#E53935", "#1E88E5", "#F9A825", "#43A047", "#8E24AA", "#FB8C00", "#00897B", "#D81B60", "#3949AB"]

CSS = """
@font-face{font-family:Osw;src:url(../../posts/fonts/oswald-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:Osw;src:url(../../posts/fonts/oswald-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Osw;src:url(../../posts/fonts/oswald-latin-500-normal.woff2);font-weight:500}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:Inter;color:#101828;position:relative;
 background:linear-gradient(135deg,#c9cfd6 0%,#f1f3f5 22%,#aab2bb 48%,#eef0f2 70%,#9da6b0 100%)}
.riv{position:absolute;width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff,#9aa3ad 55%,#5b636c)}
.pan{position:absolute;left:30px;top:30px;width:1020px;height:1290px;background:#fff;border:5px solid ACC;border-radius:10px;
 box-shadow:inset 0 0 0 3px #fff,0 6px 18px rgba(0,0,0,.35);overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(#EEF2F6 1px,transparent 1px),linear-gradient(90deg,#EEF2F6 1px,transparent 1px);background-size:30px 30px}
.cat{position:absolute;left:28px;top:24px;background:ACC;color:#fff;font-family:Osw;font-weight:600;font-size:26px;letter-spacing:1.5px;padding:4px 18px 6px;border-radius:6px}
.h1{position:absolute;left:28px;right:28px;top:76px;font-family:Osw;font-weight:700;font-size:62px;line-height:1.02;color:NAV;text-transform:uppercase}
.h1 b{color:ACC}
.sub{position:absolute;left:30px;right:30px;font-size:25px;line-height:1.32;color:#344054}
.sub b{color:#101828}
.foto{position:absolute;border-radius:10px;overflow:hidden;box-shadow:0 6px 16px rgba(16,24,40,.25)}
.foto img{display:block;width:100%;height:100%;object-fit:cover}
.bx{position:absolute;border:4px solid;border-radius:6px;box-shadow:0 0 0 2px rgba(255,255,255,.85)}
.bx i{position:absolute;left:-4px;top:-4px;transform:translate(-45%,-45%);width:38px;height:38px;border-radius:50%;color:#fff;font-style:normal;
 font-family:Osw;font-weight:700;font-size:23px;display:flex;align-items:center;justify-content:center;border:3px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4)}
.leg{position:absolute;left:28px;right:28px;display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}
.it{display:flex;gap:12px;align-items:flex-start;background:#F8FAFC;border:1.5px solid #E4E7EC;border-radius:10px;padding:9px 12px}
.it i{flex:0 0 34px;height:34px;border-radius:50%;color:#fff;font-style:normal;font-family:Osw;font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center}
.it div{font-size:19px;line-height:1.25;color:#475467}
.it div b{display:block;font-size:21px;color:#101828}
.pie{position:absolute;left:28px;right:28px;bottom:16px;display:flex;align-items:flex-end;gap:16px;border-top:2px solid #EAECF0;padding-top:10px}
.pie .f{flex:1;font-size:14.5px;line-height:1.3;color:#667085}
.pie .f b{color:#475467}
.pie .m{display:flex;align-items:center;gap:8px;font-family:Osw;font-weight:600;font-size:24px;color:NAV}
.pie .m img{height:46px}
.big{font-family:Osw;font-weight:700;color:ACC;line-height:.9}
.card{position:absolute;border-radius:12px;padding:14px 18px;font-size:22px;line-height:1.3}
.card b{color:#101828}
.vs{position:absolute;width:92px;height:92px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#4C1D95);color:#fff;font-family:Osw;font-weight:700;font-size:40px;
 display:flex;align-items:center;justify-content:center;border:5px solid #fff;box-shadow:0 4px 14px rgba(0,0,0,.35)}
.col{position:absolute;width:458px}
.col h3{font-family:Osw;font-weight:600;font-size:34px;text-align:center;color:#fff;border-radius:8px 8px 0 0;padding:4px}
.col ul{list-style:none;background:#F8FAFC;border:1.5px solid #E4E7EC;border-top:0;border-radius:0 0 10px 10px;padding:10px 14px}
.col li{font-size:19.5px;line-height:1.3;padding:6px 0 6px 30px;position:relative;border-bottom:1px dashed #E4E7EC}
.col li:last-child{border:0}
.col li:before{content:'';position:absolute;left:4px;top:11px;width:14px;height:14px;border-radius:3px;background:var(--c)}
.flow{position:absolute;left:28px;right:28px;top:76px;bottom:96px;display:flex;flex-direction:column;gap:14px}
.flow .h1,.flow .sub,.flow .leg,.flow .card{position:relative!important;left:auto!important;right:auto!important;top:auto!important;width:auto!important}
.flow .foto{position:relative!important;left:auto!important;top:auto!important;margin:0 auto;flex:none}
.bar{position:absolute;left:0;right:0;bottom:92px;background:NAV;color:#fff;text-align:center;font-family:Osw;font-weight:600;font-size:30px;padding:10px 20px;letter-spacing:.5px}
.bar b{color:#FFC94D}
"""


def page(cat, cuerpo, fuentes, foto_cred, flow=True):
    nombre, acc = CAT[cat]
    css = CSS.replace("ACC", acc).replace("NAV", C["nav"])
    riv = "".join(f"<div class='riv' style='left:{x}px;top:{y}px'></div>" for x in (6, 1052) for y in (6, 1322))
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{riv}<div class='pan'><div class='grid'></div>"
            f"<div class='cat'>{nombre}</div>" + (f"<div class='flow'>{cuerpo}</div>" if flow else cuerpo) +
            f"<div class='pie'><div class='f'><b>Fuentes:</b> {fuentes}<br><b>Foto:</b> {foto_cred}</div>"
            f"<div class='m'><img src='../../logo_oficial.png'>@miguelesquit</div></div></div></body></html>")


def foto(src, x, y, w, h, cajas=(), pos="center"):
    """cajas: (n, x0, y0, x1, y1) en fracción de la FOTO VISIBLE (object-fit cover con la proporción original)."""
    bx = "".join(f"<div class='bx' style='left:{x0 * 100:.1f}%;top:{y0 * 100:.1f}%;width:{(x1 - x0) * 100:.1f}%;height:{(y1 - y0) * 100:.1f}%;"
                 f"border-color:{BOX[(n - 1) % 9]}'><i style='background:{BOX[(n - 1) % 9]}'>{n}</i></div>" for n, x0, y0, x1, y1 in cajas)
    from PIL import Image
    W, H = Image.open(AQ / "fotos" / f"{src}.jpg").size
    k = min(w / W, h / H)
    ww, hh = W * k, H * k
    x, y = x + (w - ww) / 2, y + (h - hh) / 2
    return f"<div class='foto' style='left:{x:.0f}px;top:{y:.0f}px;width:{ww:.0f}px;height:{hh:.0f}px'><img src='../fotos/{src}.jpg'>{bx}</div>"


def leyenda(y, items, cols=2):
    its = "".join(f"<div class='it'><i style='background:{BOX[(n - 1) % 9]}'>{n}</i><div><b>{a}</b>{b}</div></div>" for n, a, b in items)
    return f"<div class='leg' style='top:{y}px;grid-template-columns:{' '.join(['1fr'] * cols)}'>{its}</div>"


def h1(t, top=76, size=62):
    return f"<div class='h1' style='top:{top}px;font-size:{size}px'>{t}</div>"


def sub(t, top):
    return f"<div class='sub' style='top:{top}px'>{t}</div>"


CC = "Wikimedia Commons"
P = {}
# ------------------------------------------------------------------ 1 · contactor por dentro
P["01_partes_contactor"] = page("partes",
    h1("Partes de un <b>contactor</b> por dentro") +
    sub("Un contactor tripolar de riel DIN desarmado. Al energizar la <b>bobina (A1-A2)</b>, el electroimán vence al resorte y el "
        "portacontactos cierra los contactos principales.", 216) +
    foto("p01_contactor", 28, 318, 964, 540, [(1, .17, .29, .39, .64), (2, .45, .29, .64, .44), (3, .48, .47, .63, .63),
                                               (4, .52, .67, .64, .84), (5, .48, .85, .70, .98), (6, .72, .28, .94, .64)]) +
    leyenda(894, [(1, "Carcasa (un lado)", "contactos fijos y bornes de conexión"),
                  (2, "Portacontactos móvil", "lleva los puentes de contacto; lo arrastra la armadura"),
                  (3, "Bobina (A1-A2)", "cobre esmaltado: crea el campo que cierra el contactor"),
                  (4, "Resorte de retorno", "abre los contactos al quitar la tensión de la bobina"),
                  (5, "Núcleo magnético fijo", "chapa en E con amortiguadores en los extremos"),
                  (6, "Carcasa (otro lado)", "contactos fijos y bornes del lado opuesto")]),
    "IEC 60947-4-1 (contactores) · Schneider Electric, guía TeSys D · Siemens, manual SIRIUS 3RT2",
    f"“Telemecanique contactor”, Dmitry G, CC BY-SA 3.0, {CC}")

# ------------------------------------------------------------------ 2 · motor de inducción en corte
P["02_partes_motor"] = page("partes",
    h1("Partes del <b>motor de inducción</b> trifásico") +
    sub("Modelo en corte de un motor de jaula de ardilla con carcasa de aluminio aleteada (TEFC). "
        "El estator crea el campo giratorio y el rotor lo sigue con un pequeño <b>deslizamiento</b>.", 216) +
    foto("p02_motor", 28, 318, 964, 470, [(1, .14, .05, .50, .23), (2, .01, .40, .16, .51), (3, .16, .38, .23, .57),
                                           (4, .20, .32, .31, .39), (5, .30, .60, .56, .71), (6, .30, .39, .58, .60),
                                           (7, .80, .38, .96, .71), (8, .20, .71, .70, .80)]) +
    leyenda(874, [(1, "Caja de bornes", "aquí se conecta la línea (estrella o triángulo)"),
                  (2, "Eje", "transmite el par a la carga"),
                  (3, "Rodamiento", "sostiene el eje en el escudo (tapa)"),
                  (4, "Devanado del estator", "bobinas de cobre: crean el campo giratorio"),
                  (5, "Núcleo del estator", "chapa de acero laminada al silicio"),
                  (6, "Rotor de jaula", "barras en cortocircuito, sin escobillas"),
                  (7, "Ventilador", "enfría la carcasa por fuera (TEFC)"),
                  (8, "Carcasa con aletas", "disipa el calor de las pérdidas")]),
    "IEC 60034-1 (máquinas rotativas) · ABB, catálogo de motores de baja tensión · Technisches Museum Wien (modelo en corte)",
    f"“TMW 50906 Schnittmodell einer Drehstrommaschine”, dominio público, {CC}")

# ------------------------------------------------------------------ 3 · interruptor termomagnético por dentro
P["03_partes_termomagnetico"] = page("partes",
    h1("Partes del <b>interruptor termomagnético</b>") +
    sub("Interruptor de 1 polo, curva C, 40 A, abierto (posición ON). Tiene <b>dos disparadores</b>: el térmico para la "
        "sobrecarga y el magnético para el cortocircuito.", 216) +
    foto("p03_mcb", 28, 318, 964, 540, [(1, .43, .07, .59, .25), (2, .46, .17, .73, .41), (3, .48, .41, .65, .59),
                                         (4, .68, .30, .80, .76), (5, .43, .59, .67, .84), (6, .20, .33, .34, .71),
                                         (7, .18, .83, .45, .92)]) +
    leyenda(874, [(1, "Palanca de maniobra", "cierre/apertura manual e indicación ON-OFF"),
                  (2, "Mecanismo de disparo libre", "abre aunque la palanca se sostenga en ON"),
                  (3, "Disparador magnético", "bobina que abre al instante con cortocircuito"),
                  (4, "Lámina bimetálica", "se curva con la sobrecarga y dispara con retardo"),
                  (5, "Cámara de extinción", "placas que dividen y enfrían el arco"),
                  (6, "Borne de conexión", "tornillo de jaula (otro igual a la derecha)"),
                  (7, "Clip de riel DIN", "fijación a riel de 35 mm")]),
    "IEC 60898-1 (interruptores automáticos) · Wikimedia, “Circuitbreaker.jpg” (descripción de partes) · IEK, ficha VA47 C40",
    f"“Circuit breaker structure ON”, Kae, CC BY-SA 3.0, {CC}")

# ------------------------------------------------------------------ 4 · relé térmico
P["04_partes_rele_termico"] = page("partes",
    h1("Partes del <b>relé térmico</b> de sobrecarga") +
    sub("Relé GE MT03N (7,5–10,5 A, clase 10A) que se enchufa directamente bajo el contactor. Protege al motor de la "
        "<b>sobrecarga</b> y de la <b>falta de fase</b>.", 216) +
    foto("p04_rele", 28, 318, 964, 540, [(1, .38, .20, .50, .34), (2, .50, .07, .77, .33), (3, .54, .41, .61, .54),
                                          (4, .59, .33, .71, .44), (5, .33, .36, .54, .55), (6, .49, .54, .59, .78),
                                          (7, .33, .55, .44, .74)]) +
    leyenda(874, [(1, "Dial de ajuste", "se fija a la corriente de placa del motor"),
                  (2, "Pines al contactor", "entran en 2/T1, 4/T2, 6/T3 y A2"),
                  (3, "Botón STOP (rojo)", "abre el contacto NC y detiene el motor"),
                  (4, "Reset H / A", "rearme manual (H) o automático (A)"),
                  (5, "Bornes 2T1 · 4T2 · 6T3", "salida de potencia hacia el motor"),
                  (6, "Contacto 95-96 (NC)", "va en serie con la bobina: abre al disparar"),
                  (7, "Borne 14/22", "paso de los auxiliares del contactor")]),
    "GE, catálogo C-2000 Mini-Contactors, relé MT03 · IEC 60947-4-1 (relés de sobrecarga) · NEC 2020 430.32",
    f"“GE MTO3N”, Dmitry G, CC BY-SA 3.0, {CC}")

# ------------------------------------------------------------------ 5 · ¿sabías qué? motores y electricidad
P["05_sabias_motores"] = page("sabias",
    h1("Los motores eléctricos consumen <b>casi la mitad</b> de la electricidad del mundo", 76, 54) +
    foto("p05_motor2", 28, 300, 964, 520) +
    "<div class='card' style='left:28px;top:880px;width:964px;background:#FFF7E6;border-left:8px solid #F08C00'>"
    "<div style='display:flex;gap:28px;align-items:center'>"
    "<div class='big' style='font-size:132px'>&gt;40&nbsp;%</div>"
    "<div>Según la <b>Agencia Internacional de Energía</b>, los sistemas accionados por motor (bombas, ventiladores, compresores, "
    "bandas) usan <b>más del 40 %</b> de la electricidad mundial. ABB habla de más del 45 % y el programa 4E de la IEA (2025) estima el <b>53 %</b>.</div></div></div>"
    "<div class='card' style='left:28px;top:1110px;width:964px;background:#F0F7FF;border-left:8px solid #1565C0'>"
    "<b>Por eso importa la eficiencia:</b> un motor IE3 o IE4 bien dimensionado, con variador donde la carga lo pida, ahorra más energía que casi cualquier otra medida en una planta.</div>",
    "IEA, “Energy-Efficiency Policy Opportunities for Electric Motor-Driven Systems” (2011) · ABB, “Energy efficiency” · IEA 4E EMSA, Policy Brief (dic. 2025)",
    f"“Cut-away version of an electric motor (1)”, S.J. de Waard, CC BY 2.5, {CC}")

# ------------------------------------------------------------------ 6 · ¿sabías qué? punteras
P["06_sabias_punteras"] = page("sabias",
    h1("El color de la <b>puntera</b> te dice la sección del cable") +
    sub("La puntera compacta los hilos del cable flexible para que el tornillo apriete <b>todos</b>: sin ella los hilos se abren, "
        "se cortan y la conexión se calienta. El collar sigue el código <b>DIN 46228-4</b>:", 216) +
    foto("p06_punteras", 28, 330, 964, 400, [(1, .31, .04, .43, .38), (2, .34, .66, .44, .92), (3, .52, .17, .63, .29), (4, .00, .10, .27, .95)]) +
    leyenda(826, [(1, "Punteras aisladas", "tubo de cobre estañado + collar de plástico"),
                  (2, "Punteras sin aislar", "solo el tubo metálico"),
                  (3, "Puntera crimpada", "los hilos quedan en una sola pieza"),
                  (4, "Pinza crimpadora", "con matriz del calibre: nunca con alicate")]) +
    "<div class='card' style='left:28px;top:1010px;width:964px;background:#F8FAFC;border:1.5px solid #E4E7EC'>"
    "<div style='display:flex;justify-content:space-between;font-size:21px;font-weight:700'>" +
    "".join(f"<div style='text-align:center'><div style='width:110px;height:34px;border-radius:6px;background:{c};border:2px solid #98A2B3;margin:0 auto 6px'></div>{t}</div>"
            for c, t in (("#FFFFFF", "0,5 mm²"), ("#9AA0A6", "0,75 mm²"), ("#D92D20", "1 mm²"), ("#111111", "1,5 mm²"), ("#1E4FD8", "2,5 mm²"))) +
    "</div><div style='font-size:18px;color:#667085;margin-top:8px;text-align:center'>Código alemán DIN 46228-4 (hay otro código francés con colores distintos: revisa la caja del fabricante)</div></div>",
    "DIN 46228-1/-4 · Phoenix Contact, guía de punteras AI · Weidmüller, punteras H (tabla de colores)",
    f"“Wire ferrules with and without insulation”, Simon A. Eugster, CC BY-SA 3.0, {CC}")

# ------------------------------------------------------------------ 7 · dato: la placa del motor
P["07_dato_placa"] = page("dato",
    h1("Lo que dice la <b>placa</b> de un motor", 76, 54) +
    sub("Placa real de un motor trifásico de 0,37 kW. Con estos datos se elige la conexión, se ajusta el térmico y se "
        "dimensiona el cable.", 156) +
    foto("p07_placa", 28, 250, 964, 430, [(1, .13, .47, .43, .56), (2, .58, .47, .80, .56), (3, .14, .57, .60, .66), (4, .61, .57, .76, .66),
                                           (5, .05, .66, .60, .76), (6, .61, .66, .86, .76), (7, .05, .76, .60, .86)]) +
    leyenda(790, [(1, "FRAME MS 711-2", "carcasa 71 y “-2” = 2 polos"),
                  (2, "INS.CL F", "aislamiento clase F: 155 °C (IEC 60085)"),
                  (3, "0,37 kW = 0,5 HP", "potencia mecánica en el eje"),
                  (4, "IP 55", "protegido contra polvo y chorros de agua"),
                  (5, "2730 rpm a 50 Hz", "síncrona 3000 rpm → deslizamiento 9 %"),
                  (6, "CONN. Δ / Y", "triángulo en 230 V, estrella en 400 V"),
                  (7, "230/400 V · 1,67/0,97 A", "la corriente baja √3 veces en estrella")]) +
    "<div class='card' style='left:28px;top:1080px;width:964px;background:#ECFDF3;border-left:8px solid #12804A'>"
    "<b>n<sub>s</sub> = 120 × f ÷ polos = 120 × 50 ÷ 2 = 3000 rpm</b> · (3000 − 2730) ÷ 3000 = 9 % de deslizamiento. "
    "1,67 A ÷ 0,97 A ≈ 1,72 ≈ √3 ✓ · El térmico se ajusta a la corriente de la conexión usada.</div>",
    "IEC 60034-1 (placa de características) · IEC 60529 (código IP) · IEC 60085 (clases térmicas) · IEC 60072-1 (tamaños de carcasa)",
    f"“Motor nameplate Malmbergs”, Olgailga2, CC0, {CC}")

# ------------------------------------------------------------------ 8 · dato: historia del motor de inducción
tl = [("1885", "Galileo Ferraris", "construye en Turín el primer motor de inducción (bifásico) con campo giratorio."),
      ("1888", "Nikola Tesla", "patenta el motor polifásico; Westinghouse compra sus patentes en julio de 1888."),
      ("1889", "M. Dolivo-Dobrovolsky", "en AEG diseña el motor TRIFÁSICO de jaula de ardilla: el que usamos hoy."),
      ("1891", "Lauffen → Frankfurt", "primera línea trifásica: 175 km, hasta 25 kV y ≈ 96 % de eficiencia.")]
P["08_dato_historia"] = page("dato",
    h1("El motor de <b>jaula de ardilla</b> tiene más de <b>135 años</b>", 76, 56) +
    foto("p08_rotor", 28, 300, 520, 430, [(1, .33, .24, .82, .82), (2, .78, .41, .86, .75)], "center") +
    "<div class='leg' style='top:300px;left:568px;right:28px;grid-template-columns:1fr'>"
    f"<div class='it'><i style='background:{BOX[0]}'>1</i><div><b>Núcleo con barras inclinadas</b>la inclinación reduce el ruido y el rizado del par</div></div>"
    f"<div class='it'><i style='background:{BOX[1]}'>2</i><div><b>Anillo de cortocircuito</b>une todas las barras: la “jaula”</div></div>"
    "<div class='card' style='position:relative;background:#F8FAFC;border:1.5px solid #E4E7EC;font-size:19px'>Rotor real de 0,75 kW, 1420 rpm, "
    "50 Hz: barras de aluminio inyectado en chapa laminada.</div></div>" +
    "".join(f"<div class='card' style='left:28px;top:{760 + i * 108}px;width:964px;background:#FFFFFF;border:1.5px solid #E4E7EC;display:flex;gap:20px;align-items:center'>"
            f"<div class='big' style='font-size:58px;width:150px'>{a}</div><div><b style='font-size:24px'>{b}</b><br>{c}</div></div>"
            for i, (a, b, c) in enumerate(tl)),
    "KIT – Elektrotechnisches Institut, “The invention of the electric motor 1856-1893” · IEEE Spectrum, “May 1888: Tesla files his patents” · Wikipedia, “Squirrel-cage rotor”",
    f"“Wirnik by Zureks”, Zureks, CC BY-SA 3.0, {CC}", flow=False)

# ------------------------------------------------------------------ 9 · comparación guardamotor vs relé térmico


def comp(t1, t2, f1, f2, b1, b2, c1, c2, h, conclusion, cuerpo_extra="", ytop=232, fh=390):
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return (h + f"<div class='foto' style='left:28px;top:{ytop}px;width:458px;height:{fh}px;background:#fff'><img src='../fotos/{f1}.jpg' style='object-fit:contain'></div>"
            f"<div class='foto' style='left:534px;top:{ytop}px;width:458px;height:{fh}px;background:#fff'><img src='../fotos/{f2}.jpg' style='object-fit:contain'></div>"
            f"<div class='vs' style='left:464px;top:{ytop + fh / 2 - 46}px'>VS</div>"
            f"<div class='col' style='left:28px;top:{ytop + fh + 16}px;--c:{c1}'><h3 style='background:{c1}'>{t1}</h3><ul>{li(b1)}</ul></div>"
            f"<div class='col' style='left:534px;top:{ytop + fh + 16}px;--c:{c2}'><h3 style='background:{c2}'>{t2}</h3><ul>{li(b2)}</ul></div>"
            f"{cuerpo_extra}<div class='bar'>{conclusion}</div>")


P["09_comp_guardamotor"] = page("comp", comp(
    "GUARDAMOTOR", "RELÉ TÉRMICO", "p09_mpcb", "p04_rele",
    ["Térmico <b>+ magnético</b> en un solo aparato", "Corta el cortocircuito (aquí Icu 100 kA)", "Maniobra manual ON / OFF y seccionamiento",
     "Ajuste: 0,55–0,8 A · CLASS 10 · I&gt; 10 A", "Auxiliares 13-14 / 23-24 para avisar al PLC"],
    ["Solo protege contra <b>sobrecarga</b> y falta de fase", "Necesita breaker o fusibles antes (cortocircuito)", "Se monta bajo el contactor; abre su 95-96",
     "Ajuste: 7,5–10,5 A · clase 10A", "STOP rojo y RESET manual / automático"],
    "#1565C0", "#C62828", h1("<b>Guardamotor</b> vs relé térmico", 76, 60),
    "Un aparato o dos: <b>los dos necesitan un contactor</b> para arrancar a distancia"),
    "Siemens, 3RV2011-0HA10 (datos en el frente y ficha RS 706-1752) · GE, catálogo C-2000, relé MT03 · IEC 60947-2 y 60947-4-1",
    f"“Siemens MPCB”, Sarah Adrita, CC BY-SA 4.0 · “GE MTO3N”, Dmitry G, CC BY-SA 3.0 · {CC}", flow=False)

P["10_comp_contactores"] = page("comp", comp(
    "CONTACTOR INDUSTRIAL", "CONTACTOR MODULAR", "p10_iek", "p10_abb",
    ["3 polos de potencia + auxiliares (NA / NC)", "Diseñado para <b>motores</b>: corriente <b>AC-3</b>", "Bornes 1/L1… 2/T1… y bobina A1-A2",
     "Acepta relé térmico, bloques auxiliares y temporizadores", "Riel DIN o placa de montaje"],
    ["Hasta 4 polos (ej. ABB ESB24-40: 4 NA)", "Para <b>cargas resistivas</b> e iluminación (AC-1 / AC-7a)", "ESB24-40: <b>24 A en AC-1</b>, pero solo <b>9 A (4 kW) en AC-3</b>",
     "Formato de 36 mm, igual que los breakers del tablero", "Bobina AC/DC silenciosa"],
    "#0B6BCB", "#12804A", h1("Contactor <b>industrial</b> vs modular", 76, 60),
    "Para un motor, compara la corriente <b>AC-3</b>, no la del frente"),
    "IEC 60947-4-1 (categorías AC-1 y AC-3) · ABB, ficha ESB24-40 (Farnell 2081164) · IEC 61095 (contactores de uso doméstico, AC-7a)",
    f"“Contactor DIN IEK”, Kae, CC BY-SA 3.0 · “Installationsschuetz ABB ESB 24 40”, Cherubino, CC BY-SA 2.5 · {CC}", flow=False)

JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const k of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/html/'+k+'.html');await p.waitForTimeout(400);await p.screenshot({path:'png/'+k+'.png'});}
await b.close()})();"""

if __name__ == "__main__":
    (AQ / "html").mkdir(exist_ok=True)
    (AQ / "png").mkdir(exist_ok=True)
    for k, h in P.items():
        (AQ / "html" / f"{k}.html").write_text(h)
    (AQ / "shot.js").write_text(JS)
    subprocess.run(["node", "shot.js", *P], cwd=AQ, check=True)
    print(len(P))

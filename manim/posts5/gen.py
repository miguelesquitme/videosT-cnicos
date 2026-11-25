"""Publicaciones v5 (25-nov): formato aprobado "ASÍ ES UN X POR DENTRO" (foto real en corte o abierta + rótulos
señalados), FONDO BLANCO, título Anton naranja con sombra azul marino + cinta "POR DENTRO". Reusa Foto/rotulos de posts4."""
import importlib.util
import subprocess
from pathlib import Path

AQ = Path(__file__).parent
sp = importlib.util.spec_from_file_location("p4", AQ.parent / "posts4" / "gen.py")
p4 = importlib.util.module_from_spec(sp)
sp.loader.exec_module(p4)
Foto, ROJO, AZ, CC = p4.Foto, p4.ROJO, p4.AZ, p4.CC
NAR = "#FF6A00"

CSS = p4.CSS + """
@font-face{font-family:Anton;src:url('../fonts/anton-latin-400-normal.woff2')}
body{background:#FFFFFF!important}
.kick{font-family:Montserrat;font-weight:800;color:#0B1F4D;letter-spacing:6px;font-size:34px}
.big{font-family:Anton;color:#FF6A00;letter-spacing:1px;line-height:1.05;text-shadow:5px 5px 0 #0B1F4D}
.cinta{display:inline-block;font-family:Anton;font-size:46px;color:#fff;background:#0B1F4D;padding:2px 34px 6px;border-radius:12px;letter-spacing:3px;
 transform:rotate(-2deg);box-shadow:0 6px 0 #FF6A00}
.sub{background:#F4F7FB!important;border:0!important;box-shadow:none!important;border-left:8px solid #FF6A00!important;border-radius:14px!important;text-align:left!important}
"""


def page(cuerpo, fuentes, cred):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cuerpo}"
            f"<div class='pie'><div class='m'><img src='../../logo_oficial.png'>@miguelesquit</div>"
            f"<div class='f'><b>Fuentes:</b> {fuentes} · <b>Foto:</b> {cred}</div></div></body></html>")


def titulo(nombre, kick="ASÍ ES UN", cinta="POR DENTRO"):
    s = min(118, int(990 / (0.43 * len(nombre))))
    return (f"<div class='tit' style='top:26px'><div class='kick'>{kick}</div>"
            f"<div class='big' style='font-size:{s}px'>{nombre}</div>"
            f"<div style='margin-top:6px'><span class='cinta'>{cinta}</span></div></div>")


def sub(t, top=262):
    return f"<div class='sub' style='top:{top}px;font-size:23px;padding:14px 24px'>{t}</div>"


def rot(f, items, dy=0):
    for it in items:
        it["y"] += dy
    return p4.rotulos(f, items)


P = {}

# 1 · termomagnético (aprobado, nuevo título)
f = Foto("p03_mcb", 170, 430, w=740)
P["01_termomagnetico"] = page(
    titulo("TERMOMAGNÉTICO") +
    sub("Tiene <b>dos disparadores</b>: el <b>térmico</b> (bimetal) para la sobrecarga y el <b>magnético</b> (bobina) para el cortocircuito.") +
    f.html() + rot(f, [
        dict(t="Palanca", s="ON / OFF", x=150, y=450, w=220, to=(.51, .12), c=AZ),
        dict(t="Borne de conexión", x=150, y=690, w=220, to=(.27, .52), c=ROJO),
        dict(t="Cámara de extinción", s="apaga el arco", x=150, y=960, w=220, to=(.55, .74), modo="d", c=AZ),
        dict(t="Clip de riel DIN", x=330, y=1120, w=220, to=(.31, .875), c=ROJO),
        dict(t="Mecanismo de disparo", x=930, y=520, w=220, to=(.62, .29), c=ROJO),
        dict(t="Bimetal", s="disparo térmico", x=930, y=690, w=220, to=(.74, .50), c=AZ),
        dict(t="Bobina", s="disparo magnético", x=930, y=860, w=220, to=(.565, .50), modo="d", c=ROJO)], dy=20),
    "IEC 60898-1 · IEK, ficha VA47 C40 · ABB, guía técnica de interruptores modulares",
    f"“Circuit breaker structure ON”, Kae, CC BY-SA 3.0, {CC}")

# 2 · motor trifásico (aprobado, nuevo título)
f = Foto("p02_motor", 262, 440, w=790)
P["02_motor_trifasico"] = page(
    titulo("MOTOR TRIFÁSICO") +
    sub("El <b>estator</b> crea un campo magnético giratorio y el <b>rotor de jaula</b> lo sigue, un poco más lento: eso es el <b>deslizamiento</b>.") +
    f.html() + rot(f, [
        dict(t="Caja de bornes", x=140, y=470, w=230, to=(.32, .14), c=AZ),
        dict(t="Devanado del estator", x=140, y=600, w=230, to=(.255, .355), c=ROJO),
        dict(t="Eje", x=140, y=715, w=230, to=(.07, .455), c=AZ),
        dict(t="Rodamiento", x=140, y=830, w=230, to=(.195, .50), c=ROJO),
        dict(t="Carcasa con aletas", x=140, y=990, w=230, to=(.33, .76), c=AZ),
        dict(t="Rotor de jaula", x=930, y=470, w=230, to=(.50, .43), modo="d", c=ROJO),
        dict(t="Ventilador", x=930, y=640, w=230, to=(.88, .56), c=AZ),
        dict(t="Núcleo del estator", s="chapa laminada", x=640, y=1150, w=280, to=(.47, .66), c=ROJO)], dy=20),
    "IEC 60034-1 · ABB, catálogo de motores de baja tensión · Technisches Museum Wien (modelo en corte)",
    f"“TMW 50906 Schnittmodell einer Drehstrommaschine”, dominio público, {CC}")

# 3 · interruptor diferencial
f = Foto("n01_rcd_c", 242, 440, h=740)
P["03_diferencial"] = page(
    titulo("INTERRUPTOR DIFERENCIAL") +
    sub("Compara la corriente que <b>entra</b> con la que <b>sale</b>. Si la diferencia supera IΔn, dispara. Este es de <b>500 mA</b> (contra incendio); para proteger <b>personas</b> se usa <b>30 mA</b>.") +
    f.html() + rot(f, [
        dict(t="Bornes de entrada", s="fases y neutro", x=130, y=480, w=230, to=(.12, .105), rect=(.12, .03, .93, .18), c=AZ),
        dict(t="Fases y neutro", s="atraviesan el toroide", x=130, y=640, w=230, to=(.18, .45), c=ROJO),
        dict(t="Relé de disparo", s="abre los contactos", x=130, y=860, w=230, to=(.30, .58), c=AZ),
        dict(t="Contactos", s="4 polos", x=130, y=1050, w=230, to=(.14, .74), rect=(.14, .68, .95, .80), c=ROJO),
        dict(t="Transformador toroidal", s="detecta la fuga", x=950, y=640, w=230, to=(.56, .42), c=ROJO),
        dict(t="Trenza de cobre", s="conexión flexible", x=950, y=830, w=230, to=(.87, .50), c=AZ)]),
    "IEC 61008-1 (interruptores diferenciales) · IEC 60364-4-41 (protección adicional 30 mA) · Schneider Electric, guía de protección diferencial",
    f"“RCD inside”, WagnerTh, CC BY-SA 4.0, {CC}")

# 4 · transformador en aceite
f = Foto("n03_trafo_aceite", 300, 440, h=750)
P["04_transformador"] = page(
    titulo("TRANSFORMADOR") +
    sub("Trifásico en aceite, como los de poste o subestación. En cada columna del núcleo va el devanado de <b>baja tensión adentro</b> y el de <b>alta afuera</b>.") +
    f.html() + rot(f, [
        dict(t="Aisladores de alta", s="porcelana", x=140, y=470, w=240, to=(.36, .10), c=AZ),
        dict(t="Prensas de madera", s="sujetan el yugo", x=140, y=680, w=240, to=(.12, .53), c=ROJO),
        dict(t="Núcleo laminado", s="acero al silicio", x=140, y=870, w=240, to=(.21, .64), c=AZ),
        dict(t="Devanado de baja", s="interior", x=140, y=1060, w=240, to=(.44, .66), c=ROJO),
        dict(t="Tanque conservador", s="reserva de aceite", x=940, y=470, w=240, to=(.75, .06), c=ROJO),
        dict(t="Conexiones", s="hacia los aisladores", x=940, y=640, w=240, to=(.47, .45), c=AZ),
        dict(t="Cuba con aletas", s="aceite: aísla y enfría", x=940, y=820, w=240, to=(.93, .55), c=ROJO),
        dict(t="Devanado de alta", s="exterior, en discos", x=940, y=1010, w=240, to=(.72, .74), c=AZ)]),
    "IEC 60076-1 (transformadores de potencia) · ABB, Transformer Handbook · Deutsches Museum (modelo en corte)",
    f"“DMM Öltransformator Schnittmodell”, Dmm2va7, CC BY 3.0, {CC}")

# 5 · motor DC
f = Foto("n04_motor_dc", 40, 530, w=1000)
P["05_motor_dc"] = page(
    titulo("MOTOR DC") +
    sub("Siemens 1HU3 de <b>imanes permanentes</b>. El <b>colector</b> y las <b>escobillas</b> invierten la corriente en el inducido para que gire siempre hacia el mismo lado.") +
    f.html() + rot(f, [
        dict(t="Eje", x=130, y=470, w=200, to=(.06, .48), c=AZ),
        dict(t="Placa de datos", x=420, y=470, w=230, to=(.42, .14), c=ROJO),
        dict(t="Caja de bornes", x=700, y=470, w=230, to=(.69, .30), c=AZ),
        dict(t="Tacogenerador", s="mide la velocidad", x=950, y=470, w=230, to=(.86, .50), c=ROJO),
        dict(t="Rodamiento", x=140, y=1050, w=220, to=(.16, .50), c=ROJO),
        dict(t="Inducido", s="ranuras inclinadas", x=390, y=1050, w=230, to=(.43, .62), c=AZ),
        dict(t="Colector", s="delgas de cobre", x=650, y=1050, w=230, to=(.64, .50), c=ROJO),
        dict(t="Escobillas", x=900, y=1050, w=220, to=(.69, .73), modo="d", c=AZ)]),
    "IEC 60034-1 · Siemens, motores 1HU3 (placa del motor) · Chapman, Máquinas eléctricas (máquinas de CC)",
    f"“DC motor with permanent magnet excitation”, Oliver Wallscheid, CC BY 4.0, {CC}")

# 6 · alternador
f = Foto("n05_alternador", 178, 440, h=740)
P["06_alternador"] = page(
    titulo("ALTERNADOR") +
    sub("El rotor gira con la banda y genera <b>corriente alterna trifásica</b> en el estator; un <b>puente de diodos</b> la rectifica a CC para cargar la batería.") +
    f.html() + rot(f, [
        dict(t="Borne de salida", x=120, y=560, w=220, to=(.08, .33), c=AZ),
        dict(t="Escobillas", s="y regulador", x=120, y=760, w=220, to=(.24, .47), c=ROJO),
        dict(t="Carcasa", s="de aluminio", x=120, y=1060, w=220, to=(.40, .80), c=AZ),
        dict(t="Devanado del estator", x=960, y=480, w=230, to=(.44, .27), c=ROJO),
        dict(t="Ventilador", x=960, y=640, w=220, to=(.68, .35), c=AZ),
        dict(t="Rotor de garras", s="electroimán", x=960, y=800, w=220, to=(.45, .47), modo="d", c=ROJO),
        dict(t="Polea", s="la mueve la banda", x=960, y=990, w=220, to=(.85, .60), c=AZ)]),
    "Bosch, Automotive Handbook (alternadores trifásicos) · IEC 60034-1 · Hella, Tech World: el alternador",
    f"“Alternator (cut-away) (01)”, S.J. de Waard, CC BY 2.5, {CC}")

# 7 · foco LED
f = Foto("n06_led", 50, 450, w=980)
P["07_foco_led"] = page(
    titulo("FOCO LED") +
    sub("Un <b>driver</b> (fuente conmutada) convierte 120 V CA en corriente continua para los LED. Este FEIT da <b>300 lúmenes con 4,8 W</b>.") +
    f.html() + rot(f, [
        dict(t="LED SMD", s="sobre placa", x=330, y=480, w=200, to=(.33, .21), c=ROJO),
        dict(t="Driver", s="fuente conmutada", x=880, y=480, w=240, to=(.69, .15), c=AZ),
        dict(t="Transformador", s="alta frecuencia", x=900, y=650, w=220, to=(.73, .24), c=ROJO),
        dict(t="Capacitor de filtro", x=900, y=790, w=240, to=(.665, .36), c=AZ),
        dict(t="Casquillo E12", s="rosca", x=520, y=780, w=200, to=(.53, .24), c=ROJO),
        dict(t="Difusor", s="vidrio / policarbonato", x=200, y=1010, w=250, to=(.25, .56), c=AZ),
        dict(t="Datos impresos", s="120 V 60 Hz · 300 lm", x=760, y=1120, w=250, to=(.60, .62), c=ROJO)]),
    "IEC 62560 (lámparas LED con balasto incorporado) · FEIT Electric, ficha del foco · DOE, Lighting Facts",
    f"“LED bulb internals”, ArnoldReinhold, CC BY-SA 3.0, {CC}")

# 8 · contactor desarmado
f = Foto("n07_contactor", 40, 480, w=1000)
P["08_contactor"] = page(
    titulo("CONTACTOR", cinta="DESARMADO") +
    sub("Siemens 3RT1017 (<b>12 A · 5,5 kW en AC-3</b> a 400 V). Al energizar A1-A2 la bobina atrae la armadura y el portacontactos <b>cierra los polos</b>.") +
    f.html() + rot(f, [
        dict(t="Núcleo fijo", s="y resorte de retorno", x=160, y=470, w=250, to=(.07, .33), c=AZ),
        dict(t="Bobina A1-A2", s="cobre esmaltado", x=430, y=470, w=230, to=(.25, .36), c=ROJO),
        dict(t="Portacontactos", s="con la armadura móvil", x=720, y=470, w=270, to=(.42, .33), c=AZ),
        dict(t="Contactos fijos", s="y tornillos de bornes", x=420, y=1100, w=260, to=(.63, .76), rect=(.52, .14, .74, .86), c=ROJO),
        dict(t="Carcasa frontal", s="1/L1 · 3/L2 · 5/L3 · A1-A2", x=830, y=1100, w=320, to=(.88, .72), c=AZ)]),
    "Siemens, ficha 3RT1017 (SIRIUS S00) · IEC 60947-4-1 (contactores) · RS Components, 3RT1 12 A 5,5 kW",
    f"“Disassembled SIEMENS 3RT1017-1AV01”, Dmitry G, CC BY-SA 3.0, {CC}")

# 9 · relé de 11 pines
f = Foto("n09_rele11", 90, 460, w=900)
P["09_rele_11_pines"] = page(
    titulo("RELÉ DE 11 PINES") +
    sub("Finder 60.13: bobina de <b>220 V CA</b> y <b>3 contactos conmutados</b> de 10 A / 250 V. La bobina atrae la armadura y la palanca cambia los contactos.") +
    f.html() + rot(f, [
        dict(t="Resorte de retorno", x=290, y=480, w=230, to=(.45, .25), c=AZ),
        dict(t="Armadura", s="palanca móvil", x=560, y=480, w=220, to=(.55, .30), c=ROJO),
        dict(t="Carcasa transparente", x=870, y=480, w=250, to=(.86, .22), c=AZ),
        dict(t="Pines", s="base octal de 11", x=200, y=1100, w=220, to=(.12, .67), c=ROJO),
        dict(t="Bobina 220 V CA", x=560, y=1100, w=230, to=(.60, .55), c=AZ),
        dict(t="Yugo magnético", x=870, y=1100, w=230, to=(.78, .50), c=ROJO)]),
    "Finder, ficha serie 60 (60.13) · IEC 61810-1 (relés electromecánicos) · Omron, guía técnica de relés MK",
    f"“11pin 3PDT relay”, 32RB17, CC0, {CC}")

# 10 · multímetro
f = Foto("n10_multimetro", 40, 480, w=1000)
P["10_multimetro"] = page(
    titulo("MULTÍMETRO DIGITAL") +
    sub("El <b>selector</b> cambia el circuito de medida, un convertidor A/D lo digitaliza y la <b>pantalla</b> muestra el valor. Los <b>fusibles</b> protegen los rangos de corriente.") +
    f.html() + rot(f, [
        dict(t="Circuito integrado", s="amplificador", x=300, y=470, w=230, to=(.39, .17), c=AZ),
        dict(t="Fusibles", s="rangos de corriente", x=620, y=470, w=230, to=(.765, .20), c=ROJO),
        dict(t="Bornes de las puntas", x=920, y=470, w=230, to=(.825, .13), rect=(.79, .13, .86, .52), c=AZ),
        dict(t="Pantalla LCD", x=170, y=1100, w=220, to=(.17, .60), c=ROJO),
        dict(t="Trimmer", s="de calibración", x=410, y=1100, w=200, to=(.33, .33), c=AZ),
        dict(t="Selector rotativo", x=650, y=1100, w=230, to=(.53, .60), c=ROJO),
        dict(t="Shunt de 10 A", x=900, y=1100, w=210, to=(.77, .45), c=AZ)]),
    "Fluke, “ABCs of DMMs” · IEC 61010-1 / 61010-2-033 (seguridad de multímetros) · Renesas, hoja de datos ICL7106",
    f"“Digital multimeter inside”, Jstapko, CC BY-SA 3.0, {CC}")

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

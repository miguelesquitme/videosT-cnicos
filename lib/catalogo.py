"""Catálogo de componentes @miguelesquit: dibujo del equipo + símbolo IEC + datos técnicos.
Uso: python3 catalogo.py [salida_dir]  → genera PNG por componente (equipo y símbolo, fondo transparente).
Datos dimensionados para el caso base del canal: trituradora de piedrín, motor 10 hp, 240 V 3~, mando 240 VAC."""
import sys
from manim import *
from equipos import *
from simbolos import *
from plcs import *

K = K0
FUERA["c"] = TXT_OS     # documento: textos externos oscuros


def item(id_, nombre, desig, equipo, simbolo, bornes, datos, notas="", fuente=""):
    return dict(id=id_, nombre=nombre, desig=desig, equipo=equipo, simbolo=simbolo, bornes=bornes, datos=datos, notas=notas, fuente=fuente)


ITEMS = [
    item("01_disyuntor_1p", "Disyuntor monopolar (1P)", "-F",
         lambda: disyuntor(1, 6, "C", K, "F1"), lambda: disyuntor_sim(1, "F1"),
         "1 (entrada) · 2 (salida)",
         ["Interruptor automático modular, IEC 60898-1 · 18 mm (1 módulo) × 90 mm", "Curvas: B (3–5 In), C (5–10 In), D (10–20 In)",
          "Poder de corte típico: 6 kA / 10 kA", "Capacidad: según la corriente de la carga y el calibre del conductor que protege"],
         "Solo para circuitos fase-neutro (120 V). Un mando de 240 V entre dos fases necesita 2P (corta las dos fases).", "IEC 60898-1 · NEC 240.4"),
    item("02_disyuntor_2p", "Disyuntor bipolar (2P)", "-F",
         lambda: disyuntor(2, 6, "C", K, "F1"), lambda: disyuntor_sim(2, "F1"),
         "1-2 · 3-4 (accionamiento unido)",
         ["36 mm (2 módulos) × 90 mm, palanca común", "CASO BASE: protección del mando 240 VAC (L1-L2): 2P · curva C · 6 A",
          "Conductor de mando: 14 AWG (2,5 mm²)"],
         "Doble del monopolar con accionamiento unido: si dispara una fase, abre las dos.", "IEC 60898-1 · NEC 430.72"),
    item("03_disyuntor_3p", "Disyuntor tripolar (3P)", "-Q",
         lambda: disyuntor(3, 70, "C", K, "Q1"), lambda: disyuntor_sim(3, "Q1"),
         "1-2 · 3-4 · 5-6",
         ["54 mm (3 módulos) × 90 mm", "CASO BASE (si se usa breaker + relé térmico): circuito ramal del motor de 10 hp",
          "NEC T430.250: 28 A · Tabla 430.52: 250 % × 28 A = 70 A → 70 A (tamaño estándar)", "Conductor: 125 % × 28 A = 35 A → 10 AWG THHN 75 °C (NEC 430.22, T310.16)"],
         "Protege contra cortocircuito al motor y al cable; la sobrecarga la cubre el relé térmico.", "NEC 2020 430.52, 240.6"),
    item("04_guardamotor", "Guardamotor", "-QM",
         lambda: guardamotor((22, 32), 24.3, K, "QM1"), lambda: guardamotor_sim("QM1"),
         "1/L1 3/L2 5/L3 → 2/T1 4/T2 6/T3",
         ["Tamaño S0 · 45 × 97 × 97 mm (hoja de datos oficial)", "Rango térmico 22–32 A · disparo magnético ≈ 400 A",
          "Icu = 25 kA a 240 V", "CASO BASE: ajuste = 24,3 A (corriente de placa del motor)"],
         "Protege contra cortocircuito (magnético) y sobrecarga (térmico) en un solo equipo. El dial va a la corriente de placa.",
         "Hoja de datos 3RV2021 (ref.) · IEC 60947-2/-4-1"),
    item("05_contactor", "Contactor electromagnético", "-KM",
         lambda: contactor(K, "KM1", "240 V~", "32 A AC-3"),
         lambda: VGroup(contactor_pot_sim("KM1"), VGroup(contacto(True, "contactor", None, "13", "14"), contacto(False, "contactor", None, "21", "22")).arrange(RIGHT, buff=0.5), bobina(ref="-KM1")).arrange(RIGHT, buff=0.7),
         "Potencia 1/L1-2/T1 · 3/L2-4/T2 · 5/L3-6/T3 · Aux 13-14 NO · 21-22 NC · Bobina A1-A2",
         ["45 × 85 mm · riel DIN 35 mm", "CASO BASE: 32 A en AC-3 (motor de 10 hp a 230 V)", "Bobina 240 VAC 60 Hz · 1 NA + 1 NC integrados"],
         "Se elige por categoría AC-3 a la tensión del motor, no por la corriente térmica.", "IEC 60947-4-1"),
    item("06_rele_termico", "Relé térmico de sobrecarga", "-F",
         lambda: rele_termico((23, 32), 24.3, K, "F2"),
         lambda: VGroup(termico_pot_sim("F2"), VGroup(contacto(False, None, "termico", "95", "96"), contacto(True, None, "termico", "97", "98")).arrange(RIGHT, buff=0.5)).arrange(RIGHT, buff=0.7),
         "Pines 1/L1 3/L2 5/L3 (entran al contactor) · 2/T1 4/T2 6/T3 · 95-96 NC · 97-98 NO",
         ["Montaje directo bajo el contactor · 45 mm", "CASO BASE: rango 23–32 A, ajuste 24,3 A (placa)",
          "Límite NEC 430.32(A)(1) con F.S. 1,25: 125 % × 24,3 = 30,4 A", "Clase 10 · TEST, STOP, RESET manual/automático"],
         "Cuidado con un rango anormal: el rango debe contener la corriente de placa; no se ajusta a la del contactor ni al máximo.", "IEC 60947-4-1 · NEC 430.32"),
    item("07_rele_8p", "Relé de 8 pines (2 conmutados)", "-KA",
         lambda: rele_8p(K, "KA1", "240 V~"), lambda: VGroup(bobina("2", "7", "-KA1"), conmutado("1", "3", "4"), conmutado("8", "6", "5")).arrange(RIGHT, buff=0.6),
         "Bobina 2-7 · Polo 1: común 1, NA 3, NC 4 · Polo 2: común 8, NA 6, NC 5 (patillaje octal estándar)",
         ["Base DIN de 8 pines: arriba 3 4 5 6, abajo 2 1 8 7", "Bobina 240 VAC · contactos 10 A / 250 VAC (carga resistiva)"],
         "Los números de la base son los mismos del relé enchufado. En el esquema se pueden marcar 1-3 / 1-4 tal cual.", "Hoja de datos MK2P / base PF083A (ref.)"),
    item("08_temporizador", "Temporizador (retardo a la conexión)", "-KT",
         lambda: rele_8p(K, "KT1", tipo="timer"), lambda: VGroup(bobina("2", "7", "-KT1", "retardo"), conmutado("1", "3", "4", "retardo")).arrange(RIGHT, buff=0.7),
         "Alimentación 2-7 · Contactos temporizados: común 1, NA 3, NC 4 · común 8, NA 6, NC 5",
         ["Misma base de 8 pines", "100–240 VAC · multirrango (s / min / h)", "Contactos 5 A / 250 VAC (carga resistiva)"],
         "Al energizar 2-7 empieza a contar; al terminar el tiempo conmutan los contactos (LED UP).", "Hoja de datos H3CR-A8 (ref.)"),
    item("09_selector", "Selector de 2 posiciones", "-S",
         lambda: Group(operador_22("selector", "negro", K, "S2"), bloque_contacto("3", "4", k=K)).arrange(RIGHT, buff=0.4), lambda: contacto(True, None, "giro", "13", "14", "-S2"),
         "Bloque NA: 3-4 (en el esquema 13-14)",
         ["Operador de 22 mm · 2 posiciones fijas (0-1)", "Bloque de contacto: Ithe 10 A · AC-15 3 A / 240 V"],
         "Vista trasera = punto de conexión real (bloque atornillado al collarín).", "IEC 60947-5-1"),
    item("10_pulsador_na", "Pulsador con contacto NA (marcha)", "-S",
         lambda: Group(operador_22("pulsador", "verde", K, "S1", "I"), bloque_contacto("3", "4", k=K)).arrange(RIGHT, buff=0.4), lambda: contacto(True, None, "pulsador", "13", "14", "-S1"),
         "Bloque NA: 3-4 (en el esquema 13-14)",
         ["22 mm · verde (o blanco) para ARRANQUE (IEC 60204-1)", "Bloque: Ithe 10 A · AC-15 3 A / 240 V"],
         "Vista 2D de frente, como pidió el usuario.", "IEC 60204-1 10.2 · IEC 60947-5-1"),
    item("11_pulsador_nc", "Pulsador con contacto NC (paro)", "-S",
         lambda: Group(operador_22("pulsador", "rojo", K, "S0", "O"), bloque_contacto("1", "2", nc=True, k=K)).arrange(RIGHT, buff=0.4), lambda: contacto(False, None, "pulsador", "11", "12", "-S0"),
         "Bloque NC: 1-2 (en el esquema 11-12 o 21-22)",
         ["22 mm · rojo (o negro) para PARO (IEC 60204-1)", "Bloque: Ithe 10 A · AC-15 3 A / 240 V"],
         "El paro siempre es NC: si un cable se corta, la máquina se detiene.", "IEC 60204-1 9.2.2"),
    item("12_emergencia", "Paro de emergencia", "-S",
         lambda: Group(operador_22("emergencia", "rojo", K, "S3"), bloque_contacto("1", "2", nc=True, k=K)).arrange(RIGHT, buff=0.4), lambda: contacto(False, None, "emergencia", "11", "12", "-S3"),
         "Bloque NC de apertura forzada: 1-2 (esquema 11-12; a menudo 2 NC)",
         ["Hongo rojo de 40 mm sobre fondo amarillo", "Enclavamiento mecánico; desbloqueo por giro", "Contacto de apertura positiva"],
         "Corta el mando directamente (categoría de paro 0 o 1). No sustituye al paro normal.", "ISO 13850 · IEC 60947-5-5 · IEC 60204-1"),
    item("13_piloto", "Luz piloto", "-H",
         lambda: Group(operador_22("piloto", "verde", K, "H1"), bloque_contacto("X1", "X2", k=K, piloto=True)).arrange(RIGHT, buff=0.4), lambda: lampara("H1", col_lampara="#12B76A"),
         "X1 · X2 (portalámparas LED)",
         ["22 mm · LED integrado 240 VAC", "Colores IEC 60204-1: rojo = emergencia · amarillo = anormal · verde = normal · azul = obligatorio · blanco = neutro"],
         "El color cambia según la función; el dibujo es el mismo.", "IEC 60204-1 10.3"),
    item("14_sensor_inductivo", "Sensor inductivo M18", "-B",
         lambda: sensor_m18("inductivo", K, "B1"), lambda: sensor_sim("inductivo", "B1"),
         "BN (1) +24 V · BU (3) 0 V · BK (4) salida PNP",
         ["M18 · 10–30 VDC · PNP NA", "Distancia nominal típica: 5 mm enrasado / 8 mm no enrasado", "Detecta solo metales"],
         "Colores de hilos según IEC 60947-5-2.", "IEC 60947-5-2"),
    item("15_sensor_capacitivo", "Sensor capacitivo M18", "-B",
         lambda: sensor_m18("capacitivo", K, "B2"), lambda: sensor_sim("capacitivo", "B2"),
         "BN +24 V · BU 0 V · BK salida PNP",
         ["M18 · 10–30 VDC · PNP NA · potenciómetro de sensibilidad", "Detecta metales y no metales (agua, granos, plásticos)"], "", "IEC 60947-5-2"),
    item("16_sensor_optico", "Sensor óptico difuso M18", "-B",
         lambda: sensor_m18("optico", K, "B3"), lambda: sensor_sim("optico", "B3"),
         "BN +24 V · BU 0 V · BK salida PNP",
         ["M18 · 10–30 VDC · PNP · emisor y receptor en la misma cara", "Modo light-on / dark-on"], "", "IEC 60947-5-2"),
    item("17_flotador", "Interruptor de nivel (flotador)", "-S",
         lambda: flotador(K, "S5"), lambda: VGroup(contacto(True, None, "flotador", "C", "NA", "-S5"), contacto(False, None, "flotador", "C", "NC")).arrange(RIGHT, buff=0.5),
         "C común · NA (cierra al subir) · NC (cierra al bajar)",
         ["Tipo pera con contrapeso · cable de 3 hilos", "Contacto típico 10 A / 250 VAC"],
         "Los colores de los hilos cambian entre fabricantes: siempre se verifica con su hoja antes de cablear.", "Hoja del fabricante"),
    item("18_motor_3f", "Motor trifásico", "-M",
         lambda: Group(motor(K * 0.55, "M1"), placa_datos([("3~ MOTOR", "60 Hz"), ("10 HP", "1760 rpm"), ("230/460 V", "24,3/12,2 A"), ("F.S. 1,25", "Ef. 91,7 %"), ("f.p. 0,84", "Clase F"), ("TEFC IP55", "Código H")], K * 0.9)).arrange(DOWN, buff=0.3),
         lambda: motor_sim(True, "M1"),
         "9 puntas: T1…T9 (NEMA) · en IEC: U1 V1 W1 / W2 U2 V2",
         ["CASO BASE (dato real de catálogo): 10 hp, 230/460 V, 24,3/12,2 A, 1760 rpm", "Corriente de arranque (rotor bloqueado): 162 A a 230 V",
          "NEC T430.250 (para calcular cable y protección): 28 A a 230 V", "A 240 V: conexión de tensión baja"],
         "De los datos del motor salen la protección, el contactor, el relé térmico y el cable.", "Hoja de datos del motor de catálogo · NEC 430.6"),
    item("19_bornes_motor", "Caja de bornes del motor", "-M (bornes)",
         lambda: Group(caja_bornes_9(K, "bajo"), caja_bornes_6(K, "delta")).arrange(RIGHT, buff=0.5), lambda: motor_sim(True, "M1"),
         "NEMA 9 puntas tensión baja: T1-T6-T7 · T2-T4-T8 · T3-T5-T9 · IEC 6 bornes Δ: U1-W2 · V1-U2 · W1-V2",
         ["Se muestra al lado del motor con zoom, como en la referencia", "Tensión alta (460 V): T4-T7 · T5-T8 · T6-T9; línea a T1 T2 T3"],
         "Siempre se toma de la placa del motor.", "NEMA MG 1 · IEC 60034-8"),
    item("20_borneras", "Borneras de caballete por paquetes", "-X",
         lambda: Group(bornera(["L1", "L2", "L3", "PE"], K, "X0", {"PE": "PE"}), bornera(["U", "V", "W", "PE"], K, "X1", {"PE": "PE"}), bornera(["1", "2", "3", "4", "5"], K, "X2")).arrange(RIGHT, buff=0.6),
         lambda: VGroup(bornera_sim(["L1", "L2", "L3", "PE"], "X0"), bornera_sim(["U", "V", "W", "PE"], "X1"), bornera_sim(["1", "2", "3", "4", "5"], "X2")).arrange(DOWN, buff=0.4, aligned_edge=LEFT),
         "-X0 alimentación · -X1 motores · -X2 puerta/mando · -X3 campo (sensores)",
         ["Gris = paso · azul = neutro · verde/amarillo = PE", "Potencia 10 AWG → borne de 6 mm² · mando 14 AWG → borne de 2,5 mm²"],
         "Agrupación por función (convención de taller; IEC 81346 deja libre el número del paquete).", "IEC 60947-7-1/-2 · IEC 81346-2"),
    item("21_logo", "PLC LOGO! 12/24RCE + fuente LOGO!Power", "-A / -T",
         lambda: Group(logo_power(K), logo8(K)).arrange(RIGHT, buff=0.25), lambda: VGroup(fuente_sim("T1"), plc_sim(["L+", "M", "I1", "I2", "I3", "I4"], ["Q1", "Q2", "Q3", "Q4"], "A1", "LOGO!")).arrange(RIGHT, buff=0.7),
         "LOGO!: L+ M I1…I8 arriba · Q1…Q4 (1-2) abajo · Fuente: L N arriba · + + − − abajo",
         ["LOGO! 8 12/24RCE: 71,5 × 90 × 60 mm · 12/24 VDC · 8 DI (4 analógicas 0–10 V)", "4 salidas a relé: 10 A resistiva / 3 A inductiva · Ethernet",
          "LOGO!Power 24 V: 100–240 VAC → 24 VDC 1,3 A · 36 mm"],
         "Se conserva la marca (se trabaja sobre ese modelo). La fuente va aparte.", "Hoja de datos 6ED1052-1MD08-0BA1"),
    item("22_s7_1200", "PLC S7-1200 CPU 1212C AC/DC/RLY", "-A",
         lambda: cpu1212(K), lambda: plc_sim(["L1", "N", "L+", "M", "1M", ".0", ".1", ".2"], [".0", ".1", ".2", ".3", ".4", ".5"], "A1", "CPU 1212C"),
         "L1 N ⏚ · L+ M (24 VDC sensores) · 1M .0….7 · 2M 0 1 (AI) · salidas 1L .0–.3 · 2L .4 .5",
         ["90 × 100 × 75 mm · 85–264 VAC", "8 DI 24 VDC · 6 DQ a relé 2 A · 2 AI 0–10 V", "Fuente de sensores 24 VDC 300 mA"],
         "Se conserva la marca y el modelo.", "Manual del sistema S7-1200"),
    item("23_riel_canaleta", "Riel DIN 35 mm y canaleta ranurada", "—",
         lambda: Group(canaleta(160, 40, K), riel_din(160, K)).arrange(DOWN, buff=0.15), lambda: VGroup(),
         "—", ["Riel 35 × 7,5 mm (EN 60715)", "Canaleta 40 × 40 mm o 60 × 60 mm; relleno máximo recomendado ~50 %"], "", "EN 60715"),
    item("24_conductor", "Conductor con puntera y marcador", "—",
         lambda: VGroup(*[conductor([[0, 0, 0], [0, -2.2, 0]], c, 8, m, K).shift(RIGHT * 0.7 * i) for i, (c, m) in enumerate(((C_POT, "L1"), (C_POT, "U"), (C_AC, "3"), (C_N, "N"), (C_PE[0], "PE")))]),
         lambda: VGroup(),
         "Puntera (ferrule) + marcador con el número del hilo en cada punta",
         ["Colores: potencia negro · mando AC rojo · mando DC azul · neutro azul claro · PE verde/amarillo (IEC 60204-1)",
          "Punteras aisladas (DIN 46228-4): 1,5 mm² negra · 2,5 mm² azul · 4 mm² gris · 6 mm² amarilla"],
         "Todo punto de conexión: pineado + etiquetado.", "IEC 60204-1 13.2 · DIN 46228-4"),
    item("25_multimetro", "Multímetro y pinza amperimétrica", "—",
         lambda: Group(multimetro(K), pinza(K)).arrange(RIGHT, buff=0.5), lambda: VGroup(),
         "COM (negra) · V/Ω (roja)",
         ["Categoría CAT III 600 V mínimo para tableros", "Ω: en frío; V~: con tensión; A~: pinza alrededor de UN conductor"], "", "IEC 61010-1"),
]


def render_item(it, out, modo="equipo"):
    from manim import tempconfig
    class Esc(Scene):
        def construct(self):
            m = it[modo]()
            if len(m) == 0 if hasattr(m, "__len__") else False:
                return
            m.move_to(ORIGIN)
            fw, fh = config.frame_width * 0.9, config.frame_height * 0.88
            f_aj = min(fw / max(m.width, 1e-3), fh / max(m.height, 1e-3))
            m.scale(min(f_aj, 2.2) if modo == "simbolo" else f_aj)   # símbolos: misma escala para todos
            self.add(m)
    with tempconfig({"transparent": True, "pixel_width": 1600, "pixel_height": 1200, "frame_width": 8.0, "frame_height": 6.0,
                     "output_file": f"{it['id']}_{modo}", "media_dir": out, "format": "png", "save_last_frame": True, "write_to_movie": False, "disable_caching": True, "verbosity": "ERROR"}):
        Esc().render()


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/cat/out"
    solo = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    for it in ITEMS:
        if solo and not any(it["id"].startswith(s) for s in solo):
            continue
        for modo in ("equipo", "simbolo"):
            render_item(it, out, modo)
        print("ok", it["id"], flush=True)

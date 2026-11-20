"""H23 · MI PRIMER ARRANQUE CON CONTACTORES · Sigue el diagrama borne por borne (horizontal, 8+ min).

Fuentes verificadas:
- Contactor tamaño S00, 3 kW / 7 A AC-3 a 400 V, bobina 24 V DC 4 W (cierre y retención), 1 NA 13-14, bornes 1/L1…6/T3, A1(+) A2(−),
  conductor 0,5–4 mm² (AWG 20–12), riel 35 mm EN 60715 (hoja de datos oficial del fabricante, modelo de 24 V DC con 1 NA).
- Relé de sobrecarga S00 clase 10, 3,5–5 A, 1 NC 95-96 + 1 NA 97-98, TEST, STOP, RESET manual/automático, montaje directo (catálogo oficial).
- NEC 2020 Tabla 430.250: motor trifásico 1 hp a 230 V = 4,2 A.
- NEC 430.22: conductores del motor ≥ 125 % de la corriente de tabla → 5,25 A (14 AWG basta; 430.6(A)(1) usa la tabla).
- NEC Tabla 430.52: interruptor de tiempo inverso ≤ 250 % → 10,5 A; 430.52(C)(1) Excepción 1: el tamaño estándar siguiente, 15 A (240.6(A)).
- NEC 430.32(A)(1): protección de sobrecarga ≤ 125 % de la corriente de placa si F.S. ≥ 1,15. Se ajusta a la corriente de placa.
- IEC 60204-1: colores de pulsadores (verde marcha, rojo paro), conductores de mando en DC azules, protección PE verde/amarillo;
  el paro se hace con contacto NC (desconexión por apertura).
- Designaciones IEC 81346 / Telesquemario: -Q1, -KM1, -F2, -T1, -S0, -S1, -H1, -X1, -M1. Numeración de bornes EN 50005 / EN 50012.
- Bobina: P = V²/R → R ≈ 24² / 4 = 144 Ω (valor aproximado en frío para un multímetro).
"""

GUION = {
    "gancho": (
        "¿Tienes el diagrama en la mano y no sabes por dónde empezar a cablear? Inténtalo con esta guía. "
        "Hoy armamos un arranque directo de un motor trifásico, borne por borne, siguiendo el diagrama normalizado. "
        "Primero aprendes a leerlo, después cableas la potencia, luego el mando, lo pruebas en frío con el multímetro "
        "y al final lo energizas. Si al terminar puedes seguir cualquier diagrama de arranque, este video cumplió."
    ),
    "materiales": (
        "Estos son los equipos, con su designación del diagrama. Menos Q uno: interruptor automático tripolar de quince amperios, curva C, protege el circuito del motor contra cortocircuito. "
        "Menos F uno: interruptor de dos polos para la fuente de mando. Menos T uno: fuente de veinticuatro voltios de corriente directa. "
        "Menos KM uno: contactor tamaño ese cero cero, siete amperios en categoría A C tres, con bobina de veinticuatro voltios directa y un contacto normalmente abierto, el trece catorce. "
        "Menos F dos: relé térmico de sobrecarga, clase diez, con rango de tres punto cinco a cinco amperios, que se monta directo debajo del contactor. "
        "Menos S cero: pulsador rojo de paro, normalmente cerrado. Menos S uno: pulsador verde de marcha, normalmente abierto. "
        "Menos H uno: piloto ámbar de falla. Menos X uno: la bornera. Y menos M uno: un motor de un caballo, doscientos treinta voltios en triángulo, tres punto nueve amperios de placa."
    ),
    "dimension": (
        "¿Por qué esos tamaños? La tabla cuatro treinta punto doscientos cincuenta del Nec da cuatro punto dos amperios para un motor trifásico de un caballo a doscientos treinta voltios. "
        "Los conductores se calculan al ciento veinticinco por ciento: cinco punto dos cinco amperios, así que el catorce A W G sobra. "
        "El interruptor de tiempo inverso puede llegar al doscientos cincuenta por ciento: diez punto cinco amperios, y el Nec permite subir al tamaño estándar siguiente, quince. "
        "Y el relé térmico se ajusta a la corriente de placa, tres punto nueve, nunca a la del contactor."
    ),
    "leer": (
        "Ahora, a leer el diagrama. Regla uno: todo se dibuja en reposo, sin tensión y sin pulsar nada. Por eso el paro aparece cerrado y la marcha abierta. "
        "Regla dos: cada aparato lleva una letra y un número. K M es el contactor, F el relé de protección, S los pulsadores, H el piloto. "
        "Regla tres: los números de los bornes te dicen qué contacto es. En potencia, los impares entran y los pares salen: uno, tres y cinco arriba, dos, cuatro y seis abajo. "
        "En los auxiliares, el último dígito manda: uno dos es normalmente cerrado, tres cuatro es normalmente abierto. La bobina siempre es A uno, A dos. "
        "Y el relé térmico usa noventa y cinco noventa y seis para su contacto cerrado y noventa y siete noventa y ocho para el abierto. "
        "Regla cuatro: el mando se lee de arriba hacia abajo, del positivo al cero voltios, como si fueras la corriente."
    ),
    "potencia": (
        "Empezamos por la potencia, y vamos a seguir el diagrama tramo por tramo. Primer tramo: L uno, L dos y L tres de la acometida entran a los bornes uno, tres y cinco de menos Q uno. "
        "Segundo tramo: de dos, cuatro y seis de Q uno, a uno L uno, tres L dos y cinco L tres del contactor. Conductor negro, catorce A W G, y el mismo orden de fases en todo el recorrido: el que entra por la izquierda, sale por la izquierda. "
        "Tercer tramo: el relé térmico se monta debajo del contactor; sus tres pines entran directo en dos T uno, cuatro T dos y seis T tres, y se aprietan esos tornillos. "
        "Cuarto tramo: de la salida del relé a la bornera, U, V y W, y de ahí a la placa de bornes del motor: U uno, V uno, W uno. "
        "Como el motor es de doscientos treinta en triángulo, los puentes van verticales: U uno con W dos, V uno con U dos, W uno con V dos. "
        "Y no te olvides del conductor de protección: verde y amarillo, de la barra P E a la bornera y al borne de tierra de la carcasa del motor."
    ),
    "control": (
        "Ahora el mando, y aquí es donde se aprende de verdad. Sigue la línea desde el positivo de veinticuatro voltios. "
        "Primero pasa por el noventa y cinco noventa y seis del relé térmico: si hay sobrecarga, se abre y corta todo el mando. "
        "Después baja al paro, S cero, contactos once doce, normalmente cerrado. Después a la marcha, S uno, trece catorce, normalmente abierto. "
        "Y de ahí llega a A uno de la bobina del contactor. A dos regresa al cero voltios de la fuente. "
        "Falta el truco: en paralelo con la marcha va el contacto trece catorce del propio contactor. Ese es el autoenclavamiento. "
        "Al pulsar marcha, la bobina se energiza, el trece catorce se cierra y la corriente encuentra un camino propio. Sueltas el botón y el contactor sigue cerrado. "
        "Para el piloto de falla, otra rama: positivo, noventa y siete noventa y ocho del relé, y el piloto ámbar a cero voltios. "
        "Todo el mando en conductor azul, porque es corriente directa, y cada punta con su marcador de número de hilo."
    ),
    "pruebas": (
        "Antes de energizar, se prueba en frío. Interruptores abiertos y multímetro en ohmios. "
        "Primero la bobina: entre A uno y A dos deberías leer unos ciento cuarenta ohmios, porque cuatro vatios a veinticuatro voltios dan esa resistencia. "
        "Si lees cero, hay un corto; si no marca nada, la bobina está abierta. "
        "Después el mando: suelta el cable del positivo en la fuente, para no medir a través de ella, y mide entre esa punta y el cero voltios. "
        "Sin pulsar nada, el circuito está abierto. Pulsas marcha y lees los mismos ciento cuarenta ohmios: estás viendo la bobina a través de todo el mando. "
        "Con la marcha pulsada, aprietas el paro: se abre otra vez. Ahí compruebas que el paro manda sobre la marcha. "
        "Y en la potencia: con el contactor abierto, nada entre fases a la salida de Q uno; en la bornera del motor, la misma resistencia entre U y V, V y W, W y U; y continuidad del P E hasta la carcasa."
    ),
    "energizar": (
        "Ahora sí. Cierras Q uno y F uno, y la fuente enciende su led de veinticuatro voltios. "
        "Pulsas marcha: la bobina recibe tensión, el núcleo atrae la armadura, cierran los tres polos de potencia y el trece catorce. El motor arranca. "
        "Sueltas el botón: el motor sigue, gracias al autoenclavamiento. Pulsas paro: se abre el mando, la bobina se desenergiza y el motor se detiene. "
        "Ahora simula una sobrecarga con la corredera de prueba del relé: se abre el noventa y cinco noventa y seis, el contactor cae, se cierra el noventa y siete noventa y ocho y enciende el piloto ámbar. "
        "Con el reset en manual, el relé queda disparado hasta que lo rearmes. Y como el mando es por autoenclavamiento, aunque lo rearmes el motor no arranca solo: hay que pulsar marcha."
    ),
    "errores": (
        "Tres errores muy comunes. Uno: el enclavamiento conectado antes del paro. El trece catorce queda en paralelo con S cero y S uno, y el motor ya no se puede detener. "
        "Dos: usar un contacto abierto para el paro. Si un cable se corta, la máquina no se detiene. Por eso el paro siempre es normalmente cerrado. "
        "Tres: ajustar el térmico al máximo del rango o a la corriente del contactor. El dial va a la corriente de placa del motor."
    ),
    "final": (
        "En resumen: lee el diagrama en reposo, sigue cada tramo de arriba hacia abajo, conecta la potencia con el mismo orden de fases, "
        "el autoenclavamiento en paralelo solo con la marcha, prueba en frío y ajusta el térmico a la placa. "
        "Si te sirvió, suscríbete y sígueme. Nos vemos en el próximo video."
    ),
}

SECCIONES = {
    "materiales": ("1", "LOS EQUIPOS"),
    "leer": ("2", "CÓMO SE LEE EL DIAGRAMA"),
    "potencia": ("3", "CABLEADO DE POTENCIA"),
    "control": ("4", "CABLEADO DE MANDO"),
    "pruebas": ("5", "PRUEBAS EN FRÍO"),
    "energizar": ("6", "ARRANQUE, PARO Y FALLA"),
}

if __name__ == "__main__":
    t = sum(len(v) for v in GUION.values())
    print(t, "caracteres ≈", round(t / 16), "s de voz")
    for k, v in GUION.items():
        print(k, len(v), round(len(v) / 16), "s")

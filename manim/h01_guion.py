"""H01 · Arranque directo de un motor trifásico · Trituradora de piedrín (horizontal, ~11 min).
Referencia de estructura: referencias/H01_referencia_arranque_directo.jpg. Equipos: biblioteca svgref.
Cálculo (NEC 2020): T430.250 10 hp 230 V = 28 A · 430.22 conductor 125 % = 35 A → 10 AWG THHN 75 °C ·
T430.52 breaker tiempo inverso 250 % = 70 A · 430.32(A)(1) F.S. 1,25 → ajuste máx 125 % placa = 30,4 A ·
contactor AC-3 32 A bobina 240 VAC · mando F1 2P 6 A, 14 AWG (430.72(B), tomas dentro del tablero).
Mando: Q1(2)→F1(1)→F1(2)→F2(95-96)→S1(11-12) paro→S2(13-14)‖KM1(13-14)→KM1(A1-A2)→F1(4)←F1(3)←Q1(4).
"""

GUION = {
    # 1 · gancho
    "gancho": (
        "Este motor de diez caballos mueve una trituradora de piedrín. Y la protección que casi todos le ponen… está mal calculada. "
        "Hoy la calculamos con números, armamos el diagrama de mando y el de potencia, lo conectamos borne por borne, "
        "lo pasamos al tablero y lo ponemos en marcha."
    ),
    # 2 · justificar
    "pregunta": (
        "Te hago una pregunta. Si el motor consume veinticuatro amperios… ¿por qué el breaker es de setenta? ¿No se quema el motor? "
        "No. Porque el breaker no protege al motor de una sobrecarga: protege al cable de un cortocircuito. "
        "Del motor se encarga otro equipo: el relé térmico. Entender esa diferencia es lo que separa un tablero que dura años, "
        "de uno que se dispara cada vez que arranca la trituradora."
    ),
    # 3 · problema real
    "placa": (
        "Todo empieza en la placa del motor. Diez caballos, doscientos treinta voltios en triángulo, "
        "veinticuatro punto tres amperios, y factor de servicio uno punto veinticinco. La red de la planta es de doscientos cuarenta voltios, trifásica."
    ),
    "tabla": (
        "Para el cable y el breaker, la norma no usa la placa: usa la tabla cuatro treinta punto doscientos cincuenta. "
        "Para diez caballos, a doscientos treinta voltios, veintiocho amperios."
    ),
    "cable": (
        "El cable: ciento veinticinco por ciento de veintiocho, treinta y cinco amperios. Calibre diez, T H H N, a setenta y cinco grados."
    ),
    "breaker": (
        "El breaker: la tabla cuatro treinta punto cincuenta y dos permite hasta el doscientos cincuenta por ciento en un breaker de tiempo inverso. "
        "Setenta amperios, tripolar. Así aguanta la corriente de arranque, que en este motor llega a ciento sesenta y dos amperios, sin dispararse."
    ),
    "termico": (
        "El relé térmico sí usa la placa. Con factor de servicio uno punto veinticinco, el ajuste máximo es el ciento veinticinco por ciento de veinticuatro punto tres: "
        "treinta punto cuatro amperios. Escogemos uno de veintitrés a treinta y dos, y lo ajustamos a la corriente de placa: veinticuatro punto tres."
    ),
    "contactor": (
        "El contactor: categoría A C tres, treinta y dos amperios, con bobina de doscientos cuarenta voltios. "
        "Y el mando lo protegemos aparte, con un breaker de dos polos de seis amperios y cable catorce."
    ),
    # 4 · materiales
    "materiales": (
        "Esta es la lista de materiales. Menos Q uno, breaker tripolar de setenta amperios. Menos F uno, breaker de dos polos de seis amperios para el mando. "
        "Menos K M uno, contactor de treinta y dos amperios con bobina de doscientos cuarenta voltios. Menos F dos, relé térmico de veintitrés a treinta y dos amperios. "
        "Menos S uno, pulsador rojo de paro, normalmente cerrado. Menos S dos, pulsador verde de marcha, normalmente abierto. "
        "Las borneras: equis cero para la alimentación, equis uno para el motor y equis dos para la puerta. "
        "Cable diez negro para la potencia, catorce rojo para el mando, y verde amarillo para la tierra. Y el motor, menos M uno."
    ),
    # 5 · diagrama de mando
    "mando": (
        "Ahora el diagrama de mando, que es el cerebro. Se lee de arriba hacia abajo, como si fueras la corriente. "
        "La fase L uno entra por el breaker de mando, menos F uno. Pasa por el noventa y cinco noventa y seis del relé térmico: un contacto cerrado que se abre si hay sobrecarga. "
        "Luego el paro, menos S uno, once doce, normalmente cerrado. Luego la marcha, menos S dos, trece catorce, normalmente abierta. "
        "Y en paralelo con la marcha, el trece catorce del propio contactor: la retención. "
        "Llegamos a la bobina, A uno, A dos, y regresamos a L dos por el otro polo de menos F uno."
    ),
    "retencion": (
        "¿Cómo funciona? Pulsas marcha, la bobina se energiza y el contactor cierra, también su trece catorce. "
        "Sueltas el botón… y la corriente sigue pasando por la retención. Para apagar, el paro abre el circuito, la bobina cae y la retención se abre."
    ),
    # 6 · diagrama de potencia
    "potencia": (
        "La potencia es más sencilla. Las tres fases entran a la bornera equis cero y pasan por el breaker de setenta, "
        "por los contactos principales del contactor, uno a dos, tres a cuatro, cinco a seis, "
        "por el relé térmico, y salen por la bornera equis uno hacia el motor: U uno, V uno, W uno. Y la tierra, a la carcasa. "
        "En la caja de bornes, los puentes en triángulo: U uno con W dos, V uno con U dos, y W uno con V dos."
    ),
    # 7 · conexión del mando, tramo por tramo
    "c_intro": "Ahora sí, a conectar. Primero el mando, a la par del diagrama, tramo por tramo. Cable rojo, calibre catorce, con puntera y su número de hilo.",
    "c1": "Hilo uno y dos: de la salida dos y cuatro del breaker principal, a la entrada uno y tres de menos F uno.",
    "c2": "Hilo tres: de dos de menos F uno, al noventa y cinco del relé térmico.",
    "c3": "Hilo cuatro: del noventa y seis del térmico, a la bornera equis dos, borne uno… y de ahí, al once del paro.",
    "c4": "Hilo cinco: del doce del paro, a la bornera equis dos, borne dos… y de ahí al trece de la marcha. Del mismo borne, un puente al trece del contactor.",
    "c5": "Hilo seis: del catorce de la marcha, a la bornera equis dos, borne tres… y al catorce del contactor, y del catorce, un puente a A uno de la bobina.",
    "c6": "Hilo siete: de A dos de la bobina, al cuatro de menos F uno, que es el regreso a L dos. Y el mando está completo.",
    # 8 · conexión de potencia
    "p_intro": "Ahora la potencia. Cable negro, calibre diez, y el mismo orden de fases en todo el recorrido.",
    "p1": "Las tres fases, de la bornera equis cero, a uno, tres y cinco del breaker de setenta.",
    "p2": "De dos, cuatro y seis del breaker, a uno L uno, tres L dos y cinco L tres del contactor.",
    "p3": "El relé térmico se monta debajo del contactor: sus pines de cobre entran directo en dos T uno, cuatro T dos y seis T tres, y se aprietan esos tornillos.",
    "p4": "De la salida del térmico, a la bornera equis uno: U, V y W. Y la tierra, verde amarillo, de equis cero a equis uno.",
    "p5": "Ajustamos el dial del térmico a la corriente de placa: veinticuatro punto tres amperios.",
    # 9 · tablero
    "tablero": (
        "Ahora lo pasamos al tablero. En la placa de montaje, el riel DIN y la canaleta. Arriba la alimentación y las protecciones: menos Q uno y menos F uno. "
        "En medio, el contactor con el relé térmico acoplado. Abajo las borneras. Y en la puerta, el paro y la marcha. "
        "La potencia baja en el mismo sentido que el diagrama, el mando va separado, y cada cable lleva su número."
    ),
    # 10 · puesta en marcha
    "prueba_frio": (
        "Antes de energizar, prueba en frío. Con todo apagado, el multímetro en ohmios entre los bornes del mando: "
        "al pulsar marcha debe marcar la resistencia de la bobina, y al pulsar paro, circuito abierto."
    ),
    "prueba_tension": "Cerramos el breaker principal y medimos la llegada: doscientos cuarenta voltios entre fases.",
    "marcha": "Cerramos el breaker de mando… pulsamos marcha… el contactor cierra… y el motor arranca.",
    "corriente": "Con la pinza medimos la corriente de trabajo: por debajo de los veinticuatro punto tres amperios de placa. Todo bien.",
    "disparo": (
        "Y probamos la protección. Con el botón TEST simulamos una sobrecarga: el noventa y cinco noventa y seis se abre, la bobina cae y el motor para. "
        "Aunque pulses marcha, no arranca, hasta que se reconoce la falla con RESET."
    ),
    # 11 · cierre
    "cierre": (
        "Si te sirvió, suscríbete. En el siguiente video arrancamos este mismo motor con un variador de frecuencia. "
        "Y si quieres repasar rápido, aquí tienes los shorts de este tema."
    ),
}

SECCIONES = [
    ("1", "El gancho"), ("2", "La pregunta técnica"), ("3", "El problema real"), ("4", "Lista de materiales"),
    ("5", "Diagrama de mando IEC"), ("6", "Diagrama de potencia IEC"), ("7", "Conexión del mando"),
    ("8", "Conexión de potencia"), ("9", "Al tablero"), ("10", "Puesta en marcha"), ("11", "Cierre"),
]

if __name__ == "__main__":
    print(sum(len(v) for v in GUION.values()), "caracteres")

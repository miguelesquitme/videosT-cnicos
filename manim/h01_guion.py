"""H01 v2 · Arranque directo de un motor trifásico · Trituradora de piedrín (horizontal).
Diagramas: los del usuario (Correcciones_V6), literal; valores adaptados al motor real.
Motor: Nidec US Motors U10P2D · 10 hp · 208-230/460 V · 26,5/23,9/12 A · 1760 rpm · F.S. 1,25 · Ef. 91,7 % · NEMA B · 215T · TEFC.
Red 208Y/120 V · mando 120 VAC L-N.
NEC 2020 a 208 V: T430.250 30,8 A · 430.22 125 % = 38,5 A → 8 AWG THHN 75 °C · T430.52 250 % = 77 A → C80 (430.52(C)(1) Exc.1)
· 430.32(A)(1) F.S. 1,25 → máx 33,1 A, ajuste 26,5 A · contactor 38 A AC-3 (10 hp a 200/208 V, UL) · T430.251(B) rotor bloqueado 10 hp 208 V = 178 A.
Regla: NUNCA se pronuncia "menos" por el guion de la designación (se dice "Q uno", "K M uno").
"""

GUION = {
    # 1 · gancho: dato curioso + pregunta (sin decir que otros lo hacen mal)
    "gancho": (
        "¿Sabías que, en el instante en que arranca, este motor de diez caballos puede pedir casi siete veces su corriente normal? "
        "Pasa de veintiséis amperios… a más de ciento setenta, durante unos segundos. "
        "Entonces, ¿cómo lo protegemos sin que el breaker se dispare cada vez que arranca?"
    ),
    "gancho2": (
        "En este video lo calculamos con la norma, armamos el diagrama de mando y el de potencia, lo conectamos cable por cable, "
        "lo pasamos al tablero y lo ponemos en marcha."
    ),
    # 2 · justificar
    "pregunta": (
        "Y aquí viene la pregunta que más confunde: si el motor consume veintiséis punto cinco amperios, ¿por qué el breaker es de ochenta? "
        "La respuesta: el breaker no está para cuidar al motor de una sobrecarga. Está para cortar un cortocircuito y proteger el cable. "
        "De la sobrecarga se encarga otro equipo, el relé térmico, que sí se ajusta a la corriente del motor."
    ),
    # 3 · problema real
    "placa": (
        "Todo empieza en la placa. Este es un motor real, de catálogo: diez caballos. "
        "Tensión: doscientos ocho a doscientos treinta, o cuatrocientos sesenta voltios. "
        "Corriente a doscientos ocho voltios: veintiséis punto cinco amperios. "
        "Y factor de servicio: uno punto veinticinco. "
        "La red de la planta es de doscientos ocho voltios, trifásica, con neutro: doscientos ocho entre fases y ciento veinte de fase a neutro."
    ),
    "tabla": (
        "Para el cable y el breaker, la norma no usa la placa: usa la tabla cuatro treinta punto doscientos cincuenta. "
        "Diez caballos, a doscientos ocho voltios: treinta punto ocho amperios."
    ),
    "cable": (
        "El cable: ciento veinticinco por ciento de treinta punto ocho, treinta y ocho punto cinco amperios. "
        "El calibre diez no alcanza, así que usamos calibre ocho, T H H N, a setenta y cinco grados."
    ),
    "breaker": (
        "El breaker: la tabla cuatro treinta punto cincuenta y dos permite hasta el doscientos cincuenta por ciento en un breaker de tiempo inverso. "
        "Eso da setenta y siete amperios, y la norma deja subir al siguiente tamaño estándar: ochenta amperios, tres polos, curva C. "
        "Así aguanta el arranque sin dispararse."
    ),
    "termico": (
        "El relé térmico sí usa la placa. Con factor de servicio uno punto veinticinco, puede ajustarse hasta el ciento veinticinco por ciento: treinta y tres punto uno amperios. "
        "Escogemos uno de veintitrés a treinta y dos, y lo ajustamos a la corriente de placa: veintiséis punto cinco."
    ),
    "contactor": (
        "El contactor se escoge por la potencia del motor a la tensión de trabajo, en categoría A C tres. "
        "Ojo aquí: uno de treinta y dos amperios solo está listado para siete punto cinco caballos a doscientos ocho voltios. "
        "Para diez caballos necesitamos el de treinta y ocho amperios. Y su bobina, de ciento veinte voltios, porque el mando va entre fase y neutro."
    ),
    "mando_prot": "El mando lo protegemos aparte, con un breaker de un polo de dos amperios, curva C, y cable catorce.",
    # 4 · materiales (en pantalla va la tabla completa)
    "materiales": (
        "Esta es la lista de materiales. "
        "El motor de diez caballos. "
        "F dos, breaker de tres polos, ochenta amperios, curva C, para riel DIN de treinta y cinco milímetros. "
        "F uno, breaker de un polo, dos amperios, para el mando. "
        "K M uno, contactor: en potencia, treinta y ocho amperios A C tres, diez caballos a doscientos ocho voltios; en mando, bobina de ciento veinte voltios y un contacto abierto y uno cerrado. "
        "F tres, relé térmico de veintitrés a treinta y dos amperios, compatible con ese contactor. "
        "S cero, pulsador rojo de paro, y S uno, pulsador verde de arranque. "
        "H uno, luz piloto verde, y H dos, luz piloto roja, de ciento veinte voltios. "
        "Las borneras las contamos en el diagrama: seis grises para las líneas, una azul para el neutro, dos verde amarillo para la tierra, y un separador al inicio y al final de cada paquete. "
        "El cable, en cantidades aproximadas: negro calibre ocho para la potencia, rojo catorce para el mando, azul claro catorce para el neutro, y verde amarillo calibre ocho para la tierra. "
        "Y para armarlo: riel DIN, canaleta ranurada, y un gabinete de quinientos por cuatrocientos por doscientos milímetros."
    ),
    # 5 · diagrama de mando, tramo por tramo
    "m1": "Ahora el diagrama de mando. Se lee de arriba hacia abajo, como si fueras la corriente. Arriba, la fase L, que sale de la bornera X cero.",
    "m2": "La fase baja al breaker de mando, F uno, borne uno y borne dos.",
    "m3": "De ahí, al contacto noventa y cinco, noventa y seis del relé térmico, F tres. Es cerrado: se abre solo si hay una sobrecarga.",
    "m4": "Sigue el pulsador de paro, S cero: once doce, normalmente cerrado.",
    "m5": "Luego el pulsador de arranque, S uno: trece catorce, normalmente abierto.",
    "m6": "Y en paralelo con el arranque, el trece catorce del propio contactor. Esta es la retención, la que mantiene encendido el motor cuando sueltas el botón.",
    "m7": "Llegamos a la bobina del contactor, A uno, A dos. Y en paralelo, la luz verde, H uno: motor encendido.",
    "m8": "Abajo, todo regresa al neutro de X cero.",
    "m9": "Y una rama más: desde la salida de F uno, el contacto veintiuno veintidós del contactor, que es cerrado, enciende la luz roja, H dos: motor apagado.",
    "retencion": (
        "¿Cómo funciona? Con el motor apagado, la luz roja está encendida. Pulsas arranque: la bobina se energiza, el contactor cierra, "
        "su trece catorce también cierra, la luz verde enciende y la roja se apaga porque se abrió el veintiuno veintidós. "
        "Sueltas el botón… y la corriente sigue por la retención. Pulsas paro: la bobina cae y todo regresa."
    ),
    # 6 · diagrama de potencia, tramo por tramo
    "p_d1": "Ahora la potencia. Arriba, la bornera X cero: L uno, L dos, L tres, el neutro y la tierra.",
    "p_d2": "Las tres fases bajan al breaker F dos: uno, tres y cinco entran; dos, cuatro y seis salen.",
    "p_d3": "Siguen a los contactos principales del contactor K M uno.",
    "p_d4": "Luego al relé térmico, F tres.",
    "p_d5": "Y salen por la bornera X uno, bornes uno, dos y tres, hacia el motor: T uno, T dos y T tres. La tierra, del borne cinco de X cero al borne cuatro de X uno, y de ahí a la carcasa.",
    # 7 · conexión del mando, cable por cable
    "c_intro": (
        "Ahora sí, a conectar. Primero el mando, a la par del diagrama. Cable rojo calibre catorce. "
        "Cada punta lleva su terminal de puntera, que es lo que entra debajo del tornillo, y su marcador con el número del hilo."
    ),
    "c1": "Hilo uno: de la entrada uno del breaker F dos, que es la fase L uno, a la entrada uno de F uno.",
    "c2": "Hilo dos: de la salida dos de F uno al noventa y cinco del relé térmico. Del mismo noventa y cinco, un puente al veintiuno del contactor, para la luz roja.",
    "c3": "Hilo tres: del noventa y seis del térmico, a la puerta, al once del pulsador de paro.",
    "c4": "Hilo cuatro: del doce del paro, un puente al trece del arranque. Y del mismo punto, un cable de regreso al trece del contactor.",
    "c5": "Hilo cinco: del catorce del arranque al catorce del contactor, y de ahí un puente a A uno de la bobina. Del catorce del arranque, también un puente a X uno de la luz verde.",
    "c6": "Hilo seis: del veintidós del contactor, a X uno de la luz roja.",
    "c7": "Y el neutro, en azul claro: del borne cuatro de X cero a A dos de la bobina, y a la puerta, a X dos de la luz verde y de la luz roja. El mando está completo.",
    # 8 · conexión de potencia
    "p_intro": "Ahora la potencia. Cable negro calibre ocho, con su puntera y su marcador, y el mismo orden de fases en todo el recorrido.",
    "p1": "L uno, L dos y L tres: de X cero, bornes uno, dos y tres, a la entrada uno, tres y cinco del breaker F dos.",
    "p2": "De la salida dos, cuatro y seis del breaker, a uno L uno, tres L dos y cinco L tres del contactor.",
    "p3": "El relé térmico se monta directo debajo del contactor: sus pines de cobre entran en dos T uno, cuatro T dos y seis T tres, y se aprietan esos tornillos.",
    "p4": "De la salida del térmico a X uno: bornes uno, dos y tres. Y la tierra, verde amarillo, del borne cinco de X cero al borne cuatro de X uno.",
    "p5": (
        "En la caja del motor, conexión de baja tensión para doscientos ocho voltios: T uno con T siete, T dos con T ocho, T tres con T nueve, "
        "y T cuatro, T cinco y T seis unidos. Esa conexión se confirma siempre con la placa del motor."
    ),
    "p6": "Por último, ajustamos el dial del térmico a la corriente de placa: veintiséis punto cinco amperios.",
    # 9 · tablero
    "t1": "Ahora lo pasamos al tablero. Primero el gabinete, de quinientos por cuatrocientos por doscientos milímetros.",
    "t2": "Adentro, la plancha de montaje.",
    "t3": "Sobre la plancha, la canaleta ranurada, que es por donde van a correr los cables.",
    "t4": "Luego los rieles DIN, y los atornillamos.",
    "t5": "Montamos los equipos: arriba los breakers, en medio el contactor con el relé térmico, y abajo las borneras.",
    "t6": "Y en la puerta, el paro, el arranque y las dos luces piloto.",
    "t7": "Se cablea igual que antes: la potencia baja en el mismo orden que el diagrama, el mando corre por la canaleta, y cada cable con su número.",
    # 10 · puesta en marcha
    "prueba_frio": (
        "Antes de energizar, prueba en frío. Todo apagado, multímetro en ohmios entre el hilo dos y el neutro: "
        "al pulsar arranque debe marcar la resistencia de la bobina, y al pulsar paro, circuito abierto."
    ),
    "prueba_tension": "Cerramos el breaker F dos y medimos en X cero: doscientos ocho voltios entre fases, y ciento veinte de fase a neutro.",
    "marcha": "Cerramos F uno: enciende la luz roja, motor apagado. Pulsamos arranque… el contactor cierra, enciende la luz verde, y el motor arranca.",
    "corriente": "Con la pinza, en una sola fase, medimos la corriente de trabajo. Debe quedar por debajo de los veintiséis punto cinco amperios de placa.",
    "disparo": (
        "Y probamos la protección. Con el botón TEST del relé térmico simulamos una sobrecarga: el noventa y cinco noventa y seis se abre, la bobina cae y el motor para. "
        "Aunque pulses arranque, no arranca, hasta que se reconoce la falla con RESET."
    ),
    # 11 · cierre
    "cierre": (
        "Si te sirvió, suscríbete y sígueme. Voy a seguir subiendo más contenido como este. "
        "Y no te pierdas mi siguiente video."
    ),
}

SECCIONES = [
    ("1", "El dato curioso"), ("2", "La pregunta técnica"), ("3", "El problema real"), ("4", "Lista de materiales"),
    ("5", "Diagrama de mando IEC"), ("6", "Diagrama de potencia IEC"), ("7", "Conexión del mando"),
    ("8", "Conexión de potencia"), ("9", "Al tablero"), ("10", "Puesta en marcha"), ("11", "Cierre"),
]

# Lista de materiales (tabla en pantalla): cantidad, nombre, características, observación
MATERIALES = [
    ("1", "Motor trifásico -M1", "10 hp · 208-230/460 V · 26,5 A a 208 V · 60 Hz · 1760 rpm · F.S. 1,25 · NEMA B · 215T · TEFC", "Nidec U10P2D · 9 puntas"),
    ("1", "Breaker -F2", "3 polos · 80 A · curva C · 240 VAC · riel DIN 35 mm", "Cortocircuito del ramal"),
    ("1", "Breaker -F1", "1 polo · 2 A · curva C · 120 VAC · riel DIN 35 mm", "Protección del mando"),
    ("1", "Contactor -KM1", "Potencia: 38 A AC-3 · 10 hp a 208 VAC · 3 polos\nMando: bobina 120 VAC 60 Hz · 1 NA + 1 NC · riel DIN 35 mm", ""),
    ("1", "Relé térmico -F3", "23–32 A · clase 10 · 95-96 NC · 97-98 NA", "Compatible con -KM1 · ajuste 26,5 A"),
    ("1", "Pulsador -S0", "Rojo · 22 mm · 1 NC", "PARO"),
    ("1", "Pulsador -S1", "Verde · 22 mm · 1 NA", "ARRANQUE"),
    ("1", "Luz piloto -H1", "Verde · 22 mm · LED · 120 VAC 60 Hz", "M1 ON"),
    ("1", "Luz piloto -H2", "Roja · 22 mm · LED · 120 VAC 60 Hz", "M1 OFF"),
    ("6", "Bornera gris", "Caballete · riel DIN 35 mm · 10 mm² (8 AWG) · línea", "-X0: 3 · -X1: 3"),
    ("1", "Bornera azul", "Caballete · riel DIN 35 mm · 10 mm² · neutro", "-X0"),
    ("2", "Bornera verde/amarilla", "Caballete · riel DIN 35 mm · 10 mm² · tierra (PE)", "-X0: 1 · -X1: 1"),
    ("4", "Separador de bornera", "Inicio y final de cada paquete", "-X0 · -X1"),
    ("≈ 6 m", "Cable de potencia", "THHN 8 AWG · negro", "Cantidad aproximada"),
    ("≈ 3 m", "Cable de tierra", "THHN 8 AWG · verde/amarillo", "Cantidad aproximada"),
    ("≈ 10 m", "Cable de mando", "THHN 14 AWG · rojo", "Cantidad aproximada"),
    ("≈ 4 m", "Cable de neutro", "THHN 14 AWG · azul claro", "Cantidad aproximada"),
    ("1 lote", "Punteras y marcadores", "Punteras aisladas DIN 46228-4 · marcadores de hilo", "En cada punta"),
    ("1,5 m", "Riel DIN", "35 × 7,5 mm (EN 60715)", ""),
    ("3 m", "Canaleta ranurada", "40 × 40 mm con tapa", ""),
    ("1", "Gabinete", "Metálico · 500 × 400 × 200 mm · con plancha de montaje", "Paro, arranque y pilotos en la puerta"),
]

if __name__ == "__main__":
    print(sum(len(v) for v in GUION.values()), "caracteres")

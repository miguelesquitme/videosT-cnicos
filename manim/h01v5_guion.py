"""Guion H01 v5 (Correcciones_V, 23-nov). Extiende el de H01 v3/v4: claves nuevas con sufijo _5 para no
reutilizar audio viejo. Un hilo por clip (P6). Los números van en letras para la voz."""
from h01_guion import GUION as G3

NUEVOS = {
    # ---------------------------------------------------------------- 7 · conexión del mando
    "c_intro_5": "Ahora sí, a conectar el mando, a la par del diagrama. En la puerta van dos pulsadores y dos luces; así se ven "
                 "por el frente. Pero sus bornes están atrás, así que, para que se entienda mejor, desde aquí los vamos a ver "
                 "por detrás, con su bloque de contacto. Cable rojo calibre catorce; cada punta con su puntera y su marcador "
                 "con el número del hilo. Y vamos hilo por hilo.",
    "c1_5": "Hilo uno: de la entrada cinco del breaker F dos, que es la fase L uno que llega de X cero, a la entrada uno de F uno. "
            "Los dos entran por arriba.",
    "c2a_5": "Hilo dos: de la salida dos de F uno al veintiuno del contactor, que se conecta por arriba. Ese contacto cerrado "
             "es para la luz roja.",
    "c2b_5": "Del mismo borne dos de F uno, un segundo cable baja al noventa y cinco del relé térmico, y entra por abajo.",
    "c3_5": "Hilo tres: del noventa y seis del térmico, también por abajo, hasta la puerta: al borne uno del pulsador de paro, "
            "que en el diagrama es el once.",
    "c4a_5": "Hilo cuatro: del borne dos del paro, un puente al borne tres del arranque, el trece del diagrama.",
    "c4b_5": "Y del mismo borne dos del paro, un cable de regreso al trece del contactor, por arriba.",
    "c5a_5": "Hilo cinco: del borne cuatro del arranque al catorce del contactor. El catorce se conecta por abajo.",
    "c5b_5": "Del catorce, un puente a A uno de la bobina, que entra por arriba. Ese es el contacto de retención.",
    "c5c_5": "Y del borne cuatro del arranque, otro cable a X uno de la luz verde.",
    "c6_5": "Hilo seis: del veintidós del contactor, por abajo, a X uno de la luz roja.",
    "c7a_5": "Y el neutro, en azul claro. Primero, del borne cuatro de X cero a A dos de la bobina, que se conecta por abajo.",
    "c7b_5": "De A dos, a X dos de la luz verde.",
    "c7c_5": "Y de X dos de la verde, a X dos de la roja. El mando está completo.",
    # ---------------------------------------------------------------- 8 · conexión de potencia
    "p_intro_5": "Ahora la potencia. Cable negro calibre ocho, con su puntera y su marcador. Y también un hilo a la vez, "
                 "siguiendo el diagrama.",
    "p1a_5": "Primero L uno: del borne uno de X cero a la entrada cinco del breaker F dos, tal como lo marca el diagrama.",
    "p1b_5": "L dos: del borne dos de X cero a la entrada tres.",
    "p1c_5": "Y L tres: del borne tres de X cero a la entrada uno.",
    "p2a_5": "Ahora del breaker al contactor. De la salida dos, al uno L uno del contactor.",
    "p2b_5": "De la salida cuatro, al tres L dos.",
    "p2c_5": "Y de la salida seis, al cinco L tres.",
    "p4a_5": "De la salida del térmico a X uno: de dos T uno, al borne uno.",
    "p4b_5": "De cuatro T dos, al borne dos.",
    "p4c_5": "Y de seis T tres, al borne tres.",
    "pe_5": "La tierra, verde amarillo: del borne cinco de X cero al borne cuatro de X uno.",
    "tsj_5": "Del lado de afuera de X uno sale una sola manguera: un cable TSJ de cuatro por ocho, con tres conductores negros "
             "y el verde amarillo dentro de la misma chaqueta. Va hasta la caja de conexiones del motor.",
    # ---------------------------------------------------------------- 9 · puesta en marcha
    "frio_5": "Antes de energizar, pruebas sin energía. Cerramos el breaker F dos, y con el multímetro en continuidad medimos "
              "abajo, en sus salidas: entre dos y cuatro, entre cuatro y seis, y entre dos y seis. No debe haber continuidad. "
              "Y cada fase contra tierra: tampoco. Si suena, hay un corto, y no se energiza.",
    "mando_frio_5": "Ahora el mando, también sin energía. Multímetro en ohmios, entre el hilo tres y el neutro: abierto. "
                    "Al pulsar arranque, marca la resistencia de la bobina. Y si pulsas paro, vuelve a abrir.",
    "tension_5": "Ahora sí, llega la energía. Con F dos cerrado medimos en X cero: doscientos ocho voltios entre fases, "
                 "y ciento veinte de fase a neutro.",
    "corriente_5": "Y ahora vamos al motor. Abrimos la caja de conexiones, y la pinza abraza un solo conductor: T uno. "
                   "Si abrazas toda la manguera, las corrientes de las fases se cancelan y marca casi cero. "
                   "La corriente de trabajo debe quedar por debajo de los veintiséis punto cinco amperios de placa.",
}

GUION = {**G3, **NUEVOS}

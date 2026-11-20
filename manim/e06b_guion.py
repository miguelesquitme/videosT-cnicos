"""E06b · SELECCIONA EL CONTACTOR CORRECTO · ¿Cómo funciona el contactor? — horizontal, ~11 min (rehecho con las
correcciones del usuario, 9-nov-2026).

Estructura pedida: gancho → qué es → partes (cada parte con su símbolo) → funcionamiento → aspectos críticos →
selección (7 criterios del usuario, uno por uno) → 2 ejemplos que recorren los 7 pasos.

Fuentes verificadas:
- IEC 60050 (IEV 441-14-33): definición de contactor (una sola posición de reposo, no manual, establece, soporta e
  interrumpe corrientes en condiciones normales, incluidas las sobrecargas de servicio).
- Telemecanique, Manual electrotécnico Telesquemario (PDF del usuario): págs. 24–31 (partes: bobina, circuito magnético
  fijo, armadura móvil, resorte de retorno, portacontactos, polos de aleación de plata, doble corte, cámara apagachispas
  con plaquetas; chapas de acero al silicio contra corrientes de Foucault; espiras de desfase (Frager) evitan la anulación
  periódica del flujo y las vibraciones; corriente de llamada 6 a 10 veces la de mantenimiento; arco que se apaga al
  pasar la corriente por cero; caída de tensión → no cierra → polos soldados; revisar longitud y sección de cables);
  pág. 26 (contactos auxiliares NA/NC: autoenclavamiento, señalización, enclavamiento); págs. 52–57 (criterios de
  elección; AC-1 resistencias, AC-3 motor lanzado, AC-4 motor calado); págs. 156–170 (símbolos IEC: contactor = contacto
  NA con semicírculo; pulsador = mando "E" de empuje con retorno automático; relé térmico; referencias de bornes: polos
  1 a 6 impares arriba, auxiliares de 2 cifras: unidad 1-2 apertura, 3-4 cierre, 5-6/7-8 especiales, 9 relés de
  protección (95-96, 97-98); bobina A1-A2; escritura de bornes de abajo hacia arriba; letras KM, KA, Q, F, S, M);
  pág. 197 (arranque directo: Q1, KM1, F1; mando I/O con autoenclavamiento KM1 13-14 y F 95-96).
- IEC 60947-4-1, condiciones de cierre y corte para durabilidad eléctrica (tabla de categorías, EN 60947-4-1 vía Omron):
  AC-1 cierra 1·Ie / corta 1·Ie; AC-3 cierra 6·Ie / corta 1·Ie con Ur/Ue = 0,17; AC-4 cierra 6·Ie / corta 6·Ie.
  Cierre y funcionamiento correcto del electroimán entre 85 % y 110 % de Us (también indicado en fichas ABB/Hitachi).
- IEC 60204-1 (Schneider FAQ FA28043): ARRANQUE blanco preferente, gris, negro o VERDE permitidos (rojo no);
  PARO negro preferente, gris, blanco o ROJO permitidos (verde no). El usuario pide verde/rojo: ambos permitidos.
- NEC 2020 Tabla 430.250: motor trifásico 5 hp a 230 V = 15,2 A.
- Dos marcas, mismo calibre de 18 A en AC-3:
  · Schneider TeSys D LC1D18: AC-3 18 A (≤ 440 V), AC-1 32 A (θ ≤ 60 °C), UL 5 hp 230/240 V 3~.
  · ABB AF16-30-10: AC-3 18 A (400 V, 230 V), AC-1 30 A (40 °C), UL/CSA 5 hp 220–240 V 3~.
  Calibre de 12 A en AC-3 (p. ej. LC1D12): 12 A < 15,2 A → no sirve.
- Cálculo ejemplo 2: 12 000 W / (√3 × 240 V) = 28,87 A ≈ 28,9 A.
"""

GUION = {
    "gancho": "Un contactor de dieciocho amperios puede controlar un motor de cinco caballos. Pero si lo conectas a un "
              "horno de resistencias, el mismo aparato aguanta treinta y dos amperios. ¿Cómo es posible? Al terminar este "
              "video vas a saber cómo funciona un contactor por dentro y cómo seleccionar el correcto, con siete criterios "
              "y dos ejemplos reales.",
    # ---------------- QUÉ ES
    "q_problema": "Imagina que quieres arrancar un motor con un interruptor de cuchilla. El operador tendría que estar "
                  "junto a los cables de potencia, y cada vez que abre con carga, salta un arco entre la cuchilla y la "
                  "mordaza. Además, no podrías encenderlo a distancia ni desde un automatismo.",
    "q_definicion": "La norma I E C sesenta mil cincuenta lo define así: un aparato mecánico de conexión, con una sola "
                    "posición de reposo, que no se acciona a mano, capaz de establecer, soportar e interrumpir corrientes "
                    "en condiciones normales, incluidas las sobrecargas de servicio. En reposo, sin tensión en la bobina, "
                    "sus contactos principales están abiertos.",
    "q_mundos": "La idea clave es que separa dos circuitos. El circuito de mando, con poca corriente, donde están los "
                "pulsadores. Y el circuito de potencia, que lleva la corriente del motor. Una bobina de pocos vatios "
                "controla kilovatios.",
    # ---------------- PARTES
    "p_intro": "Vamos a desarmarlo. Cada pieza tiene una función, y las más importantes tienen su propio símbolo en los "
               "esquemas, según la norma I E C sesenta y seis diecisiete.",
    "p_bobina": "Primero, la bobina. Es un devanado de alambre de cobre esmaltado que, al recibir tensión, crea el campo "
                "magnético. Sus bornes se marcan A uno y A dos, y en el esquema se dibuja como un rectángulo, con la "
                "identificación del contactor: K M uno.",
    "p_nucleo": "La bobina se monta en el circuito magnético fijo, y frente a él está la armadura móvil: juntos forman el "
                "electroimán. En corriente alterna se fabrican con chapas de acero al silicio, para reducir las "
                "corrientes de Foucault y el calentamiento. Y llevan unas espiras de cobre, las espiras de sombra, que "
                "evitan que la fuerza de atracción caiga a cero en cada ciclo y el contactor vibre.",
    "p_resorte": "El resorte de retorno empuja la armadura hacia afuera. Gracias a él, cuando se quita la tensión, el "
                 "contactor vuelve solo a su posición de reposo.",
    "p_polos": "La armadura mueve el portacontactos, que lleva los contactos principales, también llamados polos. Por "
               "ellos pasa la corriente de la carga. Sus bornes tienen una sola cifra: impares arriba, uno, tres y cinco, "
               "donde llega la alimentación; y pares abajo, dos, cuatro y seis, hacia la carga. Su símbolo es un contacto "
               "normalmente abierto con un pequeño semicírculo: ese semicírculo indica la función de contactor.",
    "p_aux": "Los contactos auxiliares son más pequeños, porque solo llevan la corriente del circuito de mando. Sus bornes "
             "tienen dos cifras: la decena es el número de orden y la unidad, la función. Uno y dos es un contacto "
             "normalmente cerrado; tres y cuatro, normalmente abierto. Por eso el trece catorce es el primer contacto, "
             "abierto, y el veintiuno veintidós, el segundo, cerrado. En el símbolo no llevan semicírculo, y nunca se usan "
             "para alimentar la carga.",
    "p_camara": "Encima de los polos está la cámara apagachispas. Sus plaquetas metálicas alargan, dividen y enfrían el "
                "arco que se forma al abrir, hasta que se apaga cuando la corriente alterna pasa por cero.",
    # ---------------- FUNCIONAMIENTO
    "f_corte": "Veámoslo en corte. Sin tensión, el resorte mantiene separada la armadura y los polos abiertos. Al aplicar "
               "tensión entre A uno y A dos, la bobina crea un flujo, el núcleo atrae a la armadura y el puente móvil "
               "cierra los contactos: la corriente llega al motor. Cada polo abre en dos puntos, lo que se llama doble "
               "corte. Al quitar la tensión, el resorte regresa la armadura y los contactos se abren.",
    "f_llamada": "Un detalle importante: con el electroimán abierto hay mucho espacio de aire, así que la bobina absorbe "
                 "una corriente de llamada alta. Ya cerrado, esa corriente baja de seis a diez veces: es la corriente de "
                 "mantenimiento.",
    "f_mando": "Ahora, el circuito de mando más usado: arranque y paro con autoenclavamiento. Entre la fase y el neutro "
               "conectamos en serie el contacto noventa y cinco noventa y seis del relé térmico, el pulsador de paro, "
               "normalmente cerrado, y el pulsador de marcha, normalmente abierto, hasta la bobina.",
    "f_marcha": "Al presionar marcha, la bobina se energiza y se cierra el contacto auxiliar trece catorce del contactor, "
                "que está en paralelo con el pulsador. Al soltar marcha, la corriente sigue por ese contacto: el contactor "
                "se queda enclavado.",
    "f_paro": "Al presionar paro, o si dispara el relé térmico, la bobina se desenergiza y todo vuelve al reposo. Y si se "
              "va la energía, el motor no arranca solo cuando regresa. Para los pulsadores usamos verde para marcha y rojo "
              "para paro, colores permitidos por la norma I E C sesenta y dos cero cuatro.",
    "f_potencia": "En el circuito de potencia, las tres fases pasan por el disyuntor Q uno, que protege contra "
                  "cortocircuitos; luego por los polos del contactor K M uno, que conecta y desconecta; después por el relé "
                  "térmico F dos, contra sobrecargas; y llegan al motor por sus bornes U uno, V uno y W uno.",
    # ---------------- ASPECTOS CRÍTICOS
    "c_proteccion": "Primer punto crítico: el contactor no es una protección. No está hecho para interrumpir un "
                    "cortocircuito. Siempre necesita un disyuntor o fusibles, y un relé de sobrecarga.",
    "c_tension": "Segundo: la tensión de la bobina. La norma I E C sesenta mil novecientos cuarenta y siete, parte cuatro "
                 "uno, exige que el contactor cierre correctamente entre el ochenta y cinco y el ciento diez por ciento "
                 "de su tensión nominal. Si una bobina de ciento veinte voltios recibe doscientos veinte, se quema. Si "
                 "recibe muy poca tensión, no cierra con fuerza.",
    "c_soldadura": "Y eso lleva al tercer punto: los contactos soldados. Si al arrancar el motor la tensión cae, el "
                   "electroimán no termina de cerrar, los contactos rebotan con poca presión y se sueldan. Al pulsar paro, "
                   "el motor sigue girando. Por eso hay que revisar la sección y el largo de los cables, y la tensión del "
                   "mando.",
    # ---------------- SELECCIÓN
    "s_intro": "Para seleccionar un contactor revisamos siete criterios. Vamos uno por uno.",
    "s1": "Criterio uno: la corriente nominal del circuito de potencia. La corriente del contactor debe ser igual o mayor que "
          "la de la carga. Muchas veces el fabricante también la indica como potencia, en kilovatios o caballos, para "
          "cada tensión.",
    "s2": "Criterio dos: la tensión nominal del circuito de potencia, y si es corriente alterna o continua. No es lo mismo "
          "cortar una corriente alterna que una continua: la continua no pasa por cero, y el arco es más difícil de "
          "apagar.",
    "s3": "Criterio tres: la tensión de control. La bobina debe coincidir con la tensión del mando, en valor y en tipo: por "
          "ejemplo, ciento veinte voltios alternos, o veinticuatro voltios continuos.",
    "s4": "Criterio cuatro: el número de polos. Tres polos para cargas trifásicas; uno o dos para monofásicas; y cuatro cuando "
          "también se debe cortar el neutro.",
    "s5": "Criterio cinco: el estado de los polos en reposo. Lo normal es que sean normalmente abiertos. Si necesitas alguno "
          "normalmente cerrado, hay que pedirlo así.",
    "s6": "Criterio seis, el más importante: el tipo de carga, o categoría de empleo. Fíjate en las curvas de corriente. En "
          "A C uno, resistencias, la corriente al cerrar y al abrir es prácticamente la nominal. En A C tres, motores de "
          "jaula, al cerrar soporta la corriente de arranque, unas seis veces la nominal; pero abre con el motor ya "
          "girando, a la corriente nominal y con una tensión reducida. En A C cuatro, frenado o impulsos, abre con el "
          "motor todavía arrancando: seis veces la nominal. Por eso el mismo aparato tiene una corriente mayor en A C uno "
          "que en A C tres.",
    "s7": "Criterio siete: los contactos auxiliares. Cuenta cuántos necesitas, abiertos y cerrados, para el autoenclavamiento, "
          "las luces piloto o los enclavamientos. Si no alcanzan, se agrega un bloque auxiliar.",
    # ---------------- EJEMPLOS
    "e1_datos": "Ejemplo uno: una bomba con motor trifásico de jaula de cinco caballos, a doscientos treinta voltios, con "
                "arranque directo, mando a ciento veinte voltios y una luz piloto de marcha.",
    "e1_pasos": "Criterio uno: según la tabla cuatrocientos treinta punto doscientos cincuenta del Nec, su corriente a plena "
                "carga es de quince punto dos amperios. Criterio dos: doscientos treinta voltios alternos. Criterio tres: bobina "
                "de ciento veinte voltios alternos. Criterio cuatro: tres polos. Criterio cinco: normalmente abiertos.",
    "e1_cat": "Criterio seis: es un motor de jaula, categoría A C tres. Un contactor de doce amperios en A C tres no alcanza. "
              "Uno de dieciocho sí: en dos marcas distintas, ese calibre está especificado para cinco caballos a "
              "doscientos treinta voltios. Criterio siete: un contacto abierto para el autoenclavamiento y otro para la luz "
              "piloto.",
    "e2_datos": "Ejemplo dos: un horno de resistencias trifásico de doce kilovatios a doscientos cuarenta voltios, "
                "controlado por un P L C a veinticuatro voltios continuos.",
    "e2_pasos": "Criterio uno: la corriente es la potencia entre raíz de tres por la tensión: veintiocho punto nueve amperios. "
                "Criterio dos: doscientos cuarenta voltios alternos. Criterio tres: bobina de veinticuatro voltios continuos. Criterio "
                "cuatro: tres polos. Criterio cinco: normalmente abiertos.",
    "e2_cat": "Criterio seis: resistencias, categoría A C uno. Y aquí está la respuesta del inicio: el mismo calibre de "
              "dieciocho amperios en A C tres tiene treinta o treinta y dos amperios en A C uno, según la marca. Sirve, "
              "aunque con poco margen, así que revisa la temperatura dentro del tablero. Criterio siete: un contacto abierto "
              "para avisarle al P L C que el contactor cerró.",
    "cierre": "Ahora ya sabes cómo funciona un contactor y cómo seleccionarlo. En el próximo video: el disyuntor. Si te "
              "sirvió, suscríbete y sígueme. Nos vemos en el próximo video.",
}

SECCIONES = {  # clave de inicio → (número, título de la portadilla / cinta)
    "q_problema": ("1", "¿QUÉ ES UN CONTACTOR?"),
    "p_intro": ("2", "PARTES DEL CONTACTOR"),
    "f_corte": ("3", "¿CÓMO FUNCIONA?"),
    "c_proteccion": ("4", "ASPECTOS CRÍTICOS"),
    "s_intro": ("5", "SELECCIONA EL CONTACTOR"),
    "e1_datos": ("6", "EJEMPLO 1 · MOTOR DE 5 hp"),
    "e2_datos": ("7", "EJEMPLO 2 · HORNO DE 12 kW"),
}

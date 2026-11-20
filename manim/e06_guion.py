"""E06 · EL CONTACTOR — horizontal, 15+ min.
Pregunta central: ¿Cómo una bobina de unos pocos voltamperios enciende y apaga un motor de varios caballos,
y cómo eliges el contactor correcto?

Fuentes verificadas (9-nov-2026):
- IEC 60050 (IEV 441-14-33): contactor = "mechanical switching device having only one position of rest, operated
  otherwise than by hand, capable of making, carrying and breaking currents under normal circuit conditions including
  operating overload conditions". Electromagnético: la fuerza de cierre la da un electroimán.
- Schneider Electric / Telemecanique, "Conmutación todo o nada" (págs. 23–33, PDF del usuario): partes (bobina,
  circuito magnético laminado, corrientes de Foucault, espiras de sombra/anillos de desfase, resorte de retorno, polos de
  aleación de plata, doble corte, cámara apagachispas con plaquetas), corriente de llamada 6 a 10 veces la de
  mantenimiento, arco de miles de grados que se apaga al pasar la corriente por cero, contactos NA/NC, KM1 A1-A2.
- Wikipedia "Shading coil": el anillo crea un flujo desfasado ~90° que mantiene fuerza cuando el flujo principal pasa
  por cero. Fuerza ∝ flujo² → cae a cero dos veces por ciclo (120 veces por segundo a 60 Hz).
- Ficha técnica Schneider TeSys Deca LC1D18M7 / LC1D18P7: Ie AC-3 18 A (≤440 V, <60 °C); Ie AC-1 32 A; 4 kW a 220–230 V;
  7,5 kW a 380–400 V; 9 kW a 415–440 V; UL 5 hp a 230/240 V trifásico; Ui 690 V; Uimp 6 kV; bobina 220 V M7;
  enganche 0,85–1,1 Uc a 60 Hz (0,8–1,1 a 50 Hz); caída 0,3–0,6 Uc; llamada 70 VA; mantenimiento 7,5 VA a 60 Hz;
  durabilidad mecánica 15 millones de ciclos; eléctrica 1,65 millones a 18 A AC-3; poder de cierre y de corte 300 A a
  440 V; 1 NA + 1 NC; cierre 12–22 ms; apertura 4–19 ms; protección con fusible gG 35 A coordinación tipo 2.
- LC1D12P7: 12 A AC-3, 25 A AC-1, 3 kW a 220–230 V, UL 3 hp a 230/240 V; par de apriete potencia 1,7 N·m.
- LC1D25P7: 25 A AC-3, 40 A AC-1, 5,5 kW a 220–230 V, UL 7,5 hp a 230/240 V; par 2,5 N·m potencia, 1,7 N·m mando.
- Códigos de bobina TeSys D 09–38 (FAQ Schneider FA105276): B7 24 V, F7 110 V, G7 120 V, M7 220 V, P7 230 V, U7 240 V.
- Categorías de empleo (IEC 60947-4-1): AC-1 cargas no inductivas o poco inductivas, hornos de resistencias;
  AC-2 motores de anillos rozantes; AC-3 motores de jaula de ardilla: arranque y desconexión con el motor girando;
  AC-4 motores de jaula: arranque, frenado por contracorriente e impulsos (inching). Corte normal AC-3 = Ie; AC-4 = 6 Ie.
- Marcado de bornes (IEC 60947 / EN 50012; NHP Motor Control Pocket Book): 1/L1-2/T1, 3/L2-4/T2, 5/L3-6/T3; bobina A1-A2;
  auxiliares de dos cifras: decena = número de orden, unidad = función (1-2 NC, 3-4 NA); relé térmico 95-96 NC, 97-98 NA.
- Símbolos IEC 60617: contacto principal de contactor (07-13-02) = contacto NA con semicírculo (función contactor);
  bobina = rectángulo; enlace mecánico = línea discontinua.
- IEC 60204-1 (Schneider FAQ FA28043): ARRANQUE blanco, gris, negro o verde (preferente blanco, rojo no permitido);
  PARADA negro, gris o blanco (preferente negro; rojo permitido); paro de emergencia rojo sobre fondo amarillo.
- NEC 2020 Tabla 430.250: motor trifásico 5 hp a 230 V = 15,2 A; 10 hp a 230 V = 28 A.
- Cálculo ejemplo 2: 12 000 W / (√3 × 240 V) = 28,9 A.
"""

GUION = {
    "intro": "Un botón pequeño, una bobina que consume apenas siete voltamperios, y un motor trifásico de cinco caballos "
             "que arranca. ¿Cómo es posible? El responsable es el contactor, el aparato que vas a encontrar en casi "
             "cualquier tablero de control. En este video vas a ver qué es, cómo funciona por dentro, cómo se conecta, "
             "y lo más importante: cómo elegir el correcto, con datos reales.",
    "problema": "Imagina que quieres encender un motor con un interruptor común. Tendrías que llevar los cables de "
                "potencia, gruesos y con corrientes altas, hasta el lugar donde está el operador. No podrías encenderlo a "
                "distancia, ni desde un sensor, ni desde un controlador programable. Y cada vez que lo abras con carga, el "
                "interruptor sufriría un arco eléctrico. La solución es separar dos mundos: un circuito de mando, con poca "
                "corriente, y un circuito de potencia, con la corriente del motor. El puente entre los dos es el contactor.",
    "definicion": "La Comisión Electrotécnica Internacional lo define así: un aparato mecánico de conexión que tiene una "
                  "sola posición de reposo, que no se acciona a mano, y que es capaz de establecer, soportar e "
                  "interrumpir corrientes en condiciones normales del circuito, incluidas las sobrecargas de servicio. "
                  "Fíjate en dos detalles. Una sola posición de reposo: si le quitas la energía a la bobina, siempre "
                  "vuelve a abrirse. Y condiciones normales: el contactor no está hecho para cortar un cortocircuito. Para "
                  "eso necesita una protección aparte, como un disyuntor o fusibles.",
    "partes": "Vamos a desarmarlo. Arriba está la cámara apagachispas, que encierra los contactos. Los contactos fijos "
              "están unidos a los bornes de conexión. Los contactos móviles van en el portacontactos, una pieza aislante "
              "que sube y baja. Debajo está la armadura móvil, también llamada martillo, y el resorte de retorno. Luego "
              "la bobina, y dentro de ella el circuito magnético fijo, también llamado culata o núcleo. Todo se apoya "
              "en la base, que se monta sobre el riel. El electroimán, formado por la bobina, la culata y la armadura, "
              "es el motor de todo el aparato.",
    "electroiman": "Cuando aplicas tensión entre los bornes A uno y A dos, la corriente recorre las espiras de la "
                   "bobina y crea un flujo magnético. Ese flujo se cierra por el núcleo de hierro y atrae a la armadura "
                   "móvil, venciendo la fuerza del resorte. La armadura arrastra al portacontactos, y los contactos "
                   "móviles se juntan con los fijos: el circuito de potencia se cierra y el motor arranca. Cuando quitas "
                   "la tensión, el flujo desaparece y el resorte devuelve todo a su posición de reposo. En un contactor "
                   "típico de este tamaño, el cierre tarda entre doce y veintidós milisegundos.",
    "laminas": "¿Por qué el núcleo no es un bloque de hierro sólido? Porque con corriente alterna, el flujo variable "
               "induce corrientes dentro del metal, llamadas corrientes de Foucault. Esas corrientes calientan el núcleo "
               "y desperdician energía. Por eso se construye con chapas de acero al silicio, aisladas y unidas entre sí: "
               "cada chapa corta el camino de esas corrientes.",
    "anillo": "Hay otro detalle que casi nadie ve. La fuerza del electroimán es proporcional al cuadrado del flujo, y en "
              "corriente alterna el flujo pasa por cero dos veces en cada ciclo. Con sesenta hercios, la fuerza se "
              "anula ciento veinte veces por segundo, y el resorte intentaría abrir la armadura: el contactor vibraría y "
              "zumbaría. La solución es un anillo de cobre en la cara del núcleo, llamado espira de sombra o anillo de "
              "desfase. En ese anillo se induce una corriente que crea un segundo flujo, desfasado. Cuando el flujo "
              "principal pasa por cero, el del anillo sigue sosteniendo la armadura.",
    "llamada": "Ahora, un dato que sorprende. Al momento de cerrar, la armadura está separada del núcleo por un espacio de "
               "aire, y el aire se opone mucho al paso del flujo. La bobina necesita una corriente grande para atraerla: "
               "es la corriente de llamada. Pero una vez cerrado, el circuito magnético casi no tiene aire, la impedancia "
               "de la bobina sube y la corriente baja. En el contactor de dieciocho amperios que usaremos de ejemplo, la "
               "ficha técnica indica setenta voltamperios en la llamada, y apenas siete punto cinco para mantenerlo "
               "cerrado a sesenta hercios. Casi diez veces menos.",
    "contactos": "Los polos son los contactos que manejan la corriente del motor. Están hechos de una aleación de plata, "
                 "resistente a la oxidación, al desgaste y al arco. Unos resortes los presionan con la fuerza correcta para "
                 "que no se calienten. Y casi todos los contactores modernos usan doble corte: el puente móvil abre el "
                 "circuito en dos puntos a la vez. Así el arco se divide en dos arcos más cortos, que se apagan con más "
                 "facilidad.",
    "arco": "Hablemos del arco. Cuando los contactos se separan con un motor funcionando, la corriente no se interrumpe de "
            "inmediato: salta por el aire formando un plasma que puede superar varios miles de grados. Si durara mucho, "
            "fundiría los contactos. La cámara apagachispas tiene plaquetas metálicas que atraen el arco, lo alargan y lo "
            "dividen en arcos pequeños, mientras lo enfrían. En corriente alterna hay una ayuda extra: la corriente pasa "
            "por cero en cada medio ciclo, y en ese instante el arco se apaga. El trabajo de la cámara es que no se "
            "vuelva a encender.",
    "bornes": "Ahora míralo de frente, como lo vas a encontrar en el tablero. Los bornes de potencia tienen doble marca. "
              "Arriba, uno L uno, tres L dos y cinco L tres: ahí llega la alimentación. Abajo, dos T uno, cuatro T dos y "
              "seis T tres: hacia la carga. Los números impares entran y los pares salen. La bobina siempre se marca "
              "A uno y A dos. Los contactos auxiliares llevan dos cifras: la decena es el número de orden, y la unidad "
              "dice la función. Uno y dos, normalmente cerrado. Tres y cuatro, normalmente abierto. Por eso trece catorce "
              "es abierto, y veintiuno veintidós es cerrado. Cada conductor entra al borne con su terminal o puntera, y "
              "el tornillo se aprieta con el par que indica el fabricante, por ejemplo uno punto siete newton metro en "
              "los bornes de potencia de un contactor de doce amperios.",
    "simbolos": "En los planos, el contactor se dibuja con los símbolos de la norma I E C sesenta mil seiscientos "
                "diecisiete. La bobina es un rectángulo con sus bornes A uno y A dos. Los contactos principales son "
                "contactos normalmente abiertos con un pequeño semicírculo, que indica que es un contacto de contactor. "
                "Los auxiliares se dibujan como contactos simples, abiertos o cerrados. Y todos llevan la misma "
                "identificación, por ejemplo K M uno, aunque estén en distintas partes del plano. Una línea discontinua "
                "indica que se mueven juntos.",
    "mando": "Veamos el circuito de mando clásico: arranque y paro con autoenclavamiento. La corriente pasa por el contacto "
             "del relé térmico, noventa y cinco noventa y seis, luego por el pulsador de paro, normalmente cerrado, y por "
             "el pulsador de arranque, normalmente abierto, hasta la bobina. Al presionar arranque, la bobina se energiza "
             "y el contactor cierra. Su contacto auxiliar trece catorce, conectado en paralelo con el pulsador, también "
             "se cierra. Ahora, aunque sueltes el botón, la bobina sigue alimentada por ese contacto: eso es el "
             "autoenclavamiento. Al presionar paro, el circuito se abre, la bobina se desenergiza y el contacto trece "
             "catorce también se abre. Y si se corta la energía, el motor no arranca solo cuando vuelve: hay que "
             "presionar arranque otra vez. Según la norma I E C sesenta mil doscientos cuatro guion uno, el pulsador de "
             "paro se recomienda negro, aunque se permite rojo, y el de arranque, blanco, aunque se permite verde.",
    "potencia": "Y el circuito de potencia: las tres fases pasan primero por la protección contra cortocircuito, luego por "
                "los polos del contactor, después por el relé térmico, y llegan a los bornes U uno, V uno y W uno del "
                "motor. El contactor solo conecta y desconecta. La protección contra cortocircuito y contra sobrecarga "
                "la hacen otros aparatos, que veremos en los próximos videos.",
    "bobina": "Un error muy común es la tensión de la bobina. La bobina no tiene que ser igual al voltaje del motor: es la "
              "tensión de tu circuito de mando. Puede ser de veinticuatro voltios, de ciento veinte o de doscientos "
              "veinte, en alterna o en continua. En la referencia del fabricante viene codificada: por ejemplo, G siete "
              "es ciento veinte voltios, M siete es doscientos veinte, y P siete es doscientos treinta, para cincuenta y "
              "sesenta hercios. La ficha también dice su rango: a sesenta hercios, este contactor cierra bien entre el "
              "ochenta y cinco y el ciento diez por ciento de su tensión, y se suelta entre el treinta y el sesenta por "
              "ciento. Si la tensión de mando cae demasiado, la bobina no tiene fuerza para cerrar del todo, los "
              "contactos rebotan y se pueden soldar.",
    "categorias": "Ahora la clave de la selección: la categoría de empleo, definida en la norma I E C sesenta mil "
                  "novecientos cuarenta y siete, parte cuatro uno. No es lo mismo cortar una resistencia que un motor. "
                  "A C uno: cargas no inductivas o poco inductivas, como hornos de resistencias. A C dos: motores de "
                  "anillos rozantes. A C tres: motores de jaula de ardilla, que arrancan y se desconectan girando; es la "
                  "categoría más común en la industria. Y A C cuatro: motores de jaula con arranque, frenado por "
                  "contracorriente e impulsos, el servicio más duro. En A C tres, al desconectar, el motor ya está "
                  "girando y la corriente es la nominal. En A C cuatro el contactor puede tener que cortar cerca de seis "
                  "veces esa corriente. Por eso un mismo contactor tiene una corriente distinta para cada categoría.",
    "placa": "Veamos los datos reales de un contactor de dieciocho amperios, de la serie TeSys D de Schneider Electric. En "
             "A C tres: dieciocho amperios hasta cuatrocientos cuarenta voltios. En A C uno: treinta y dos amperios. "
             "Potencia de motor en A C tres: cuatro kilovatios a doscientos veinte o doscientos treinta voltios, y siete "
             "punto cinco kilovatios a cuatrocientos. Tensión de aislamiento: seiscientos noventa voltios. Tensión de "
             "impulso soportada: seis kilovoltios. Poder de cierre y de corte: trescientos amperios. Vida mecánica: "
             "quince millones de maniobras. Pero vida eléctrica, cortando dieciocho amperios en A C tres: un millón "
             "seiscientas cincuenta mil. Los contactos se gastan mucho antes que el mecanismo.",
    "auxiliares": "Los contactos auxiliares no llevan la corriente del motor: sirven para el mando. Con ellos haces el "
                  "autoenclavamiento, enciendes una luz piloto que indica que el motor está en marcha, o bloqueas a otro "
                  "contactor. Por ejemplo, en un inversor de giro, un contacto normalmente cerrado de cada contactor va en "
                  "serie con la bobina del otro, para que nunca cierren los dos a la vez, porque eso sería un "
                  "cortocircuito entre fases. Si necesitas más contactos, se agregan bloques auxiliares que se montan al "
                  "frente o al costado, incluso temporizados.",
    "soldadura": "¿Por qué se sueldan los contactos? Casi siempre la causa está en el mando. Si al arrancar el motor la "
                 "tensión de la red cae mucho, o si el circuito de mando tiene poca tensión y muchos contactos en serie, "
                 "la bobina no tiene fuerza para cerrar del todo. Los polos se tocan sin presión, rebotan, se forma un arco "
                 "entre ellos y se sueldan. Por eso hay que revisar la sección y el largo de los cables, y la tensión del "
                 "mando. En mandos de baja tensión con muchos contactos, se usa un relé auxiliar que a su vez alimenta la "
                 "bobina del contactor principal.",
    "familia": "Este principio es el mismo en toda la familia: desde contactores de nueve amperios, del tamaño de una "
               "mano, hasta aparatos de cientos de amperios para motores grandes. Cambian el tamaño de los polos, la "
               "cámara apagachispas y el electroimán. Y en los calibres grandes es común encontrar bobinas para corriente "
               "continua o con electrónica, que reducen el consumo de la bobina cuando el contactor ya está cerrado.",
    "seleccion": "Entonces, para elegir un contactor, sigue estos pasos. Uno: identifica el tipo de carga y su categoría de "
                 "empleo. Dos: busca la tensión de la red y la corriente de la carga, en la placa del motor o en una "
                 "tabla. Tres: elige un contactor cuya corriente en esa categoría sea igual o mayor. Cuatro: elige la "
                 "tensión de la bobina según tu circuito de mando. Cinco: revisa cuántos contactos auxiliares necesitas. "
                 "Y seis: coordínalo con su protección contra cortocircuito y sobrecarga.",
    "ejemplo1": "Primer ejemplo. Un motor trifásico de jaula de ardilla, de cinco caballos, a doscientos treinta voltios, "
                "para una bomba. Arranca y se detiene normalmente, así que es A C tres. Según la tabla cuatro treinta punto "
                "doscientos cincuenta del Nec, su corriente a plena carga es de quince punto dos amperios. ¿Sirve el "
                "contactor de doce amperios? No: en A C tres solo llega a doce amperios y a tres caballos. El de dieciocho "
                "amperios sí: dieciocho es mayor que quince punto dos, y su ficha lo autoriza para cinco caballos a "
                "doscientos treinta voltios. El mando es de ciento veinte voltios, entonces la bobina es G siete. "
                "Resultado: contactor de dieciocho amperios, bobina de ciento veinte voltios.",
    "ejemplo2": "Segundo ejemplo. Un horno de resistencias trifásico de doce kilovatios, a doscientos cuarenta voltios. Es una "
                "carga resistiva: A C uno. La corriente es la potencia entre raíz de tres por el voltaje: doce mil entre "
                "uno punto siete tres por doscientos cuarenta, igual a veintiocho punto nueve amperios. En A C uno, el "
                "mismo contactor de dieciocho amperios soporta treinta y dos. Treinta y dos es mayor que veintiocho punto "
                "nueve: sirve. Y si fuera un motor de veintiocho punto nueve amperios, necesitarías un contactor mucho más "
                "grande. Con un mando de doscientos veinte voltios, la bobina es M siete. Fíjate: el mismo aparato "
                "maneja dieciocho amperios de motor o treinta y dos de resistencias.",
    "errores": "Tres errores muy comunes. Uno: elegir solo por los amperios, sin ver la categoría de empleo. Dos: una "
               "bobina de tensión equivocada; si es menor que la del mando, se quema, y si es mayor, no cierra bien. Y tres: "
               "creer que el contactor protege al motor; no protege contra cortocircuito ni contra sobrecarga.",
    "seguridad": "Y antes de tocar cualquier tablero: baja el interruptor principal, verifica que no haya tensión con un "
                 "instrumento adecuado, y nunca supongas que está desenergizado.",
    "repaso": "Repasemos. El contactor es un interruptor accionado por un electroimán. Una bobina de pocos voltamperios "
              "mueve contactos que manejan la corriente de un motor. Se elige por su categoría de empleo, su corriente, su "
              "tensión de bobina y sus contactos auxiliares. Y siempre va acompañado de sus protecciones.",
    "cierre": "Si te sirvió, suscríbete y sígueme. En el próximo video: el disyuntor. Nos vemos en el próximo video.",
}

if __name__ == "__main__":
    n = sum(len(v) for v in GUION.values())
    print(n, "caracteres ≈", round(n / 15.5 / 60, 1), "min ≈", round(n * 0.33), "créditos")
    import math
    print(12000 / (math.sqrt(3) * 240))

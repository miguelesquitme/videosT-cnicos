"""Serie ARRANQUES · guiones de los 15 reels A01–A15 (V39–V53), 24-nov.
Fuentes generales: NEC 2020 (T430.250, T430.52, 430.52(C)(1) Exc. 1, 430.22, 430.32(A)(1)); IEC 60947-4-1 (AC-1/AC-3, clase 10,
arrancadores); IEC 60947-1 / EN 50005 (marcado de bornes); IEC 60204-1 (13.2.4 colores, 10.7 paro de emergencia); NEMA MG 1
(9 puntas, factor de servicio); DIN 46228-4 (colores de punteras; Phoenix Contact, guía de punteras); Schneider Electric FAQ FA129583
(VA de llamada y de mantenimiento); Eaton ETR4 estrella-triángulo (pausa de 50 ms, 3–60 s); placa Nidec U10P2D (caso base).
Generar los módulos: python3 guiones_arr.py  → guion_a01.py … guion_a15.py (TIT + GUION, formato de reel_v2)."""
import pathlib

CIERRE = "Si te sirvió, suscríbete y sígueme."
R = {
    "a01": (("ASÍ FUNCIONA EL", "AUTOENCLAVAMIENTO"), {
        "gancho": "Presionas el botón verde, el motor arranca, sueltas el botón, y el motor sigue andando. El pulsador ya está abierto. "
                  "Entonces, ¿quién mantiene alimentada la bobina?",
        "p1": "El pulsador de arranque es un contacto normalmente abierto, con retorno por resorte: solo cierra mientras lo mantienes presionado. "
              "En el bloque de contacto son los bornes tres y cuatro; en el diagrama, trece catorce.",
        "p2": "En paralelo con él va el contacto auxiliar trece catorce del contactor. Cuando presionas, la corriente llega a la bobina, "
              "A uno A dos, y el contactor cierra todos sus contactos, también ese trece catorce.",
        "p3": "Ahora la corriente tiene dos caminos: el pulsador y el trece catorce. Sueltas el botón, el pulsador se abre, pero la bobina "
              "sigue alimentada por su propio contacto. Por eso se llama autoenclavamiento: el contactor se retiene solo.",
        "p4": "Para parar, el pulsador rojo es un contacto normalmente cerrado en serie. Al presionarlo corta la corriente, la bobina suelta, "
              "el trece catorce se abre y ya no hay retención, aunque sueltes el paro.",
        "p5": "Y hay una ventaja de seguridad: si se va la energía, el contactor suelta, y cuando regresa la energía el motor no arranca solo. "
              "Hay que volver a presionar marcha. El relé térmico también rompe la retención con su noventa y cinco noventa y seis.",
        "cierre": CIERRE}),
    "a02": (("¿BREAKER DE 80 A", "PARA UN MOTOR DE 26,5 A?"), {
        "gancho": "Un motor de diez caballos a doscientos ocho voltios, con veintiséis punto cinco amperios de placa, y le pongo un breaker "
                  "de ochenta amperios. ¿Está sobredimensionado? No, y te explico por qué.",
        "p1": "Al arrancar en directo, un motor pide de seis a ocho veces su corriente nominal durante unos segundos. Un breaker de treinta "
              "amperios curva C podría disparar en cada arranque.",
        "p2": "Por eso el Nec separa las dos protecciones. El breaker del circuito del motor protege contra cortocircuito y falla a tierra. "
              "La sobrecarga la protege otro aparato: el relé térmico.",
        "p3": "La tabla cuatrocientos treinta punto cincuenta y dos permite un breaker de tiempo inverso de hasta el doscientos cincuenta "
              "por ciento de la corriente de tabla. Para diez caballos a doscientos ocho voltios, la tabla cuatrocientos treinta punto "
              "doscientos cincuenta da treinta punto ocho amperios.",
        "p4": "Treinta punto ocho por dos punto cinco da setenta y siete amperios. Como no es un valor estándar, la excepción uno permite "
              "subir al siguiente: ochenta amperios.",
        "p5": "Y el cable no se calcula con el breaker: va al ciento veinticinco por ciento de treinta punto ocho, treinta y ocho punto cinco "
              "amperios, calibre ocho a setenta y cinco grados. El relé térmico, ajustado a veintiséis punto cinco amperios, cuida al motor "
              "y al cable de la sobrecarga.",
        "cierre": CIERRE}),
    "a03": (("ASÍ FUNCIONA EL", "RELÉ TÉRMICO"), {
        "gancho": "El relé térmico no mide la corriente con electrónica. La mide con calor: con una lámina de metal que se dobla. "
                  "¿Cómo dispara?",
        "p1": "Por dentro, cada fase pasa por un calefactor enrollado sobre una lámina bimetálica: dos metales soldados que se dilatan "
              "distinto. La corriente del motor calienta la lámina, y la lámina se curva.",
        "p2": "Las tres láminas empujan una regleta de disparo. Con la corriente normal, la curva no alcanza. Si el motor se sobrecarga, "
              "la lámina se calienta más, se curva más, y la regleta suelta un mecanismo de resorte.",
        "p3": "Ese mecanismo abre el contacto noventa y cinco noventa y seis, que está en serie con la bobina del contactor. El contactor "
              "suelta y el motor se detiene. Y cierra el noventa y siete noventa y ocho, para una luz de falla.",
        "p4": "Es clase diez: según la I E C sesenta mil novecientos cuarenta y siete cuatro uno, partiendo en frío dispara entre cuatro y "
              "diez segundos con siete punto dos veces la corriente ajustada. Deja pasar el arranque, pero no una sobrecarga sostenida.",
        "p5": "Y la mayoría de los modelos es sensible a la falta de fase: si se pierde una, las láminas se curvan desiguales y dispara antes. "
              "Por eso se ajusta a la corriente de placa, veintiséis punto cinco amperios en este motor, y no más.",
        "cierre": CIERRE}),
    "a04": (("EL CONTACTOR DE 32 A", "QUE NO AGUANTA 10 HP"), {
        "gancho": "Mi motor consume veintiséis punto cinco amperios y el contactor dice treinta y dos. Sobra, ¿no? Pues para un motor de diez "
                  "caballos a doscientos ocho voltios, se queda corto.",
        "p1": "La corriente de un contactor siempre va con su categoría de empleo, de la I E C sesenta mil novecientos cuarenta y siete cuatro "
              "uno. A C uno es para cargas resistivas, como hornos y calefacción. A C tres es para motores de jaula de ardilla: arrancar "
              "y desconectar con el motor en marcha.",
        "p2": "En A C tres el contacto cierra con la corriente de arranque, seis a ocho veces la nominal, y además abre con arco. Por eso el "
              "mismo aparato tiene una corriente A C tres menor que la A C uno.",
        "p3": "Para motores, el fabricante da además una tabla de caballos por tensión. En un catálogo típico, el contactor de treinta y dos "
              "amperios llega a siete punto cinco caballos a doscientos ocho voltios. El de treinta y ocho amperios, a diez caballos.",
        "p4": "La razón: a doscientos ocho voltios, la corriente de tabla de un motor de diez caballos es treinta punto ocho amperios, más que "
              "la de placa. El contactor se elige con la tabla de caballos o con la corriente A C tres, nunca con la corriente A C uno.",
        "p5": "Así que en el tablero va un contactor de treinta y ocho amperios en A C tres, con bobina de ciento veinte voltios, un contacto "
              "auxiliar normalmente abierto y uno cerrado.",
        "cierre": CIERRE}),
    "a05": (("ANTES DE ENERGIZAR:", "LA PRUEBA EN FRÍO"), {
        "gancho": "Terminaste de cablear el tablero. Antes de meter energía hay una prueba de dos minutos que te puede salvar el breaker, "
                  "el contactor, y el susto.",
        "p1": "Primero, verifica que no hay tensión: con el multímetro en voltios, entre fases y contra tierra, en la entrada. Cero. "
              "Ahora sí, sin energía, cierras el breaker principal.",
        "p2": "Pones el multímetro en continuidad y mides abajo del breaker, en sus salidas: entre dos y cuatro, entre cuatro y seis, y entre "
              "dos y seis. Con el contactor abierto no hay nada conectado entre fases: debe marcar O L, circuito abierto.",
        "p3": "Luego cada fase contra la tierra, el borne de P E. También O L. Si suena, hay un cable de fase tocando la caja o el riel, "
              "o un aislamiento dañado.",
        "p4": "Si suena entre dos fases, busca un puente mal puesto, un cable cruzado, o una puntera con hilos sueltos tocando el borne "
              "de al lado. Se corrige antes de energizar, no después del chispazo.",
        "p5": "El mando también se prueba en frío: en ohmios, entre el hilo tres y el neutro debe estar abierto. Al pulsar arranque marca la "
              "resistencia de la bobina, y al pulsar paro vuelve a abrir. Ahora sí, energizas.",
        "cierre": CIERRE}),
    "a06": (("¿POR QUÉ LA PINZA", "MARCA CERO?"), {
        "gancho": "Abrazas con la pinza la manguera del motor, el motor está trabajando, y la pantalla marca cero. ¿Está dañada la pinza? "
                  "No. La estás usando mal.",
        "p1": "La pinza no toca el cobre. Su mordaza es un núcleo magnético que rodea al conductor y mide el campo magnético que produce la "
              "corriente. Ese campo es proporcional a la corriente.",
        "p2": "En una manguera trifásica van las tres fases. En un sistema balanceado, en cada instante la suma de las tres corrientes es "
              "cero: lo que sale por una fase regresa por las otras dos.",
        "p3": "Si las tres pasan por la mordaza, sus campos se cancelan y la pinza mide esa suma: casi cero. Lo mismo pasa si abrazas la fase "
              "y el neutro de un circuito de ciento veinte voltios.",
        "p4": "Por eso se abre la caja de conexiones o se separan los conductores, y se abraza uno solo, T uno por ejemplo. Ahí sí marca la "
              "corriente real de esa fase.",
        "p5": "Mide las tres fases por separado: deben quedar parecidas y por debajo de la corriente de placa, veintiséis punto cinco "
              "amperios en este motor. Y esa suma tiene un uso: si abrazas solo las fases y no da cero, hay corriente que se va por tierra.",
        "cierre": CIERRE}),
    "a07": (("MOTOR DE 9 PUNTAS", "A 208 VOLTIOS"), {
        "gancho": "Abres la caja del motor y salen nueve cables, de T uno a T nueve. La placa dice doscientos ocho a doscientos treinta, y "
                  "cuatrocientos sesenta voltios. ¿Cómo lo conectas a doscientos ocho?",
        "p1": "Cada fase tiene dos bobinas. Las primeras van de T uno a T cuatro, de T dos a T cinco y de T tres a T seis. Las segundas "
              "salen por T siete, T ocho y T nueve, y su otro extremo ya viene unido por dentro, en una estrella.",
        "p2": "En baja tensión las dos bobinas de cada fase van en paralelo: L uno a T uno y T siete, L dos a T dos y T ocho, L tres a T tres "
              "y T nueve. Y T cuatro, T cinco y T seis se unen entre sí.",
        "p3": "Así quedan dos estrellas en paralelo. Cada bobina recibe la tensión de fase, unos ciento veinte voltios con doscientos ocho "
              "de línea, y la corriente se reparte entre las dos. Corriente de placa: veintiséis punto cinco amperios.",
        "p4": "En alta tensión, cuatrocientos sesenta voltios, van en serie: se unen T cuatro con T siete, T cinco con T ocho y T seis con "
              "T nueve, y la línea entra solo por T uno, T dos y T tres. Corriente de placa: doce amperios.",
        "p5": "Si lo dejas en la conexión de alta a doscientos ocho voltios, el motor arranca débil, se calienta y el térmico dispara. Y al revés, "
              "la conexión de baja a cuatrocientos sesenta lo quema. Antes de conectar, revisa la placa de conexiones del motor.",
        "cierre": CIERRE}),
    "a08": (("INVERSIÓN DE GIRO", "CON DOS CONTACTORES"), {
        "gancho": "Para invertir el giro de un motor trifásico basta con cruzar dos fases. Pero en una máquina no vas a cambiar cables cada vez. "
                  "Lo hacen dos contactores.",
        "p1": "En la potencia, los dos contactores toman la misma línea a la salida del breaker. Ka eme uno conecta en orden: L uno, L dos, "
              "L tres. Ka eme dos cruza dos fases: L tres entra donde iba L uno, y L uno donde iba L tres.",
        "p2": "Las salidas de los dos se unen y van a un solo relé térmico y al motor. Así el motor recibe la secuencia uno, dos, tres, o la "
              "tres, dos, uno, según qué contactor cierre.",
        "p3": "La fase del centro, L dos, pasa igual por los dos. Solo se intercambian las de los extremos, y con eso el campo magnético gira "
              "al revés, y el motor también.",
        "p4": "En el mando hay dos pulsadores de marcha, uno por sentido, cada uno con su autoenclavamiento, y un solo paro para los dos.",
        "p5": "Pero hay un peligro: si los dos contactores cierran al mismo tiempo, L uno y L tres quedan unidas a través de ellos. "
              "Cortocircuito entre fases. Por eso esta conexión siempre lleva enclavamiento.",
        "cierre": CIERRE}),
    "a09": (("EL CONTACTO NC QUE", "EVITA UN CORTOCIRCUITO"), {
        "gancho": "En una inversión de giro, si los dos contactores cierran juntos, hay un cortocircuito directo entre dos fases. Lo que lo "
                  "evita es un contacto auxiliar de unos pocos amperios.",
        "p1": "Enclavamiento eléctrico: el contacto normalmente cerrado de ka eme uno, el veintiuno veintidós, va en serie con la bobina de "
              "ka eme dos. Y el de ka eme dos, en serie con la bobina de ka eme uno.",
        "p2": "Si ka eme uno está cerrado, su contacto cerrado se abre, y la bobina de ka eme dos no puede recibir corriente aunque presiones "
              "el otro pulsador. Y al revés.",
        "p3": "Pero un contactor se puede pegar: un contacto soldado o una pieza trabada. Por eso se suma un enclavamiento mecánico, una pieza "
              "entre los dos contactores que impide que las dos armaduras cierren a la vez.",
        "p4": "Y hay un tercer nivel: pulsadores con doble contacto. Al presionar la marcha adelante, su contacto cerrado abre el camino de la "
              "marcha atrás.",
        "p5": "Con el eléctrico y el mecánico juntos, la inversión es segura. Y un consejo: antes de cambiar de sentido, deja que el motor se "
              "detenga, para no frenarlo de golpe con la corriente de arranque.",
        "cierre": CIERRE}),
    "a10": (("ESTRELLA-DELTA:", "¿CUÁNTO TIEMPO EN ESTRELLA?"), {
        "gancho": "En un arranque estrella delta, el temporizador decide cuándo pasar a triángulo. Si lo ajustas muy corto o muy largo, el "
                  "arranque deja de servir.",
        "p1": "Son tres contactores: el de línea, el de estrella y el de triángulo. Al arrancar cierran línea y estrella. Cada bobina del motor "
              "recibe la tensión de línea dividida entre raíz de tres, y la corriente de arranque baja a un tercio.",
        "p2": "El par también baja a un tercio. Por eso el motor arranca en estrella con poca carga, y debe llegar cerca de su velocidad "
              "nominal antes del cambio.",
        "p3": "El temporizador ka te uno cuenta desde el arranque. Al terminar, abre estrella y cierra triángulo. Si lo ajustas muy corto, el "
              "motor pasa a triángulo todavía lento y da un pico de corriente casi como un arranque directo.",
        "p4": "Si lo ajustas muy largo, el motor se queda en estrella con un tercio del par, y si la carga pide más, se calienta. Se ajusta "
              "midiendo el tiempo que tarda en llegar a velocidad, más un margen pequeño.",
        "p5": "Y entre estrella y triángulo hay una pausa de unos cincuenta milisegundos, que los temporizadores estrella triángulo ya traen. "
              "Sirve para que el contactor de estrella abra y se apague su arco antes de que cierre el de triángulo.",
        "cierre": CIERRE}),
    "a11": (("¿PARA QUÉ SIRVE", "LA PUNTERA?"), {
        "gancho": "En el tablero cada cable termina en un tubito de colores. Parece un detalle de lujo, pero sin él, el cable de varios hilos "
                  "se puede soltar del borne.",
        "p1": "El cable flexible es un manojo de hilos finos. Si lo metes pelado bajo el tornillo, al apretar los hilos se abren: unos quedan "
              "afuera, otros se cortan, y la presión no llega a todos.",
        "p2": "La puntera es un tubo de cobre estañado que se crimpa sobre los hilos con una pinza especial. Los hilos quedan compactados en "
              "una sola pieza, que el borne aprieta completa.",
        "p3": "El collar de plástico protege la entrada del aislamiento, y su color dice la sección. Con el código alemán D I N cuarenta y seis "
              "mil doscientos veintiocho: blanco, cero punto cinco milímetros cuadrados; gris, cero punto setenta y cinco; rojo, uno; "
              "negro, uno punto cinco; azul, dos punto cinco.",
        "p4": "El mando de catorce A W G, unos dos punto uno milímetros cuadrados, lleva la puntera de dos punto cinco, la azul. La potencia "
              "de ocho A W G, ocho punto cuatro milímetros cuadrados, lleva la de diez, que en ese código es roja.",
        "p5": "Y un consejo: la puntera debe tener el largo del borne, y se crimpa con la pinza del tamaño correcto, no con alicate. Una "
              "puntera mal crimpada se sale igual que un cable sin puntera.",
        "cierre": CIERRE}),
    "a12": (("¿POR QUÉ EL MANDO", "VA EN ROJO?"), {
        "gancho": "Abres un tablero bien hecho y los cables tienen colores: negros, rojos, azules. No es gusto del que lo armó. Lo recomienda "
                  "la norma de máquinas.",
        "p1": "La I E C sesenta mil doscientos cuatro uno recomienda un color por función. Negro: los circuitos de potencia, en alterna y "
              "en continua.",
        "p2": "Rojo: los circuitos de mando en corriente alterna, como el de ciento veinte voltios de este tablero. Azul: los de mando en "
              "corriente continua, por ejemplo los veinticuatro voltios de un P L C.",
        "p3": "Azul claro: el neutro. Y verde con amarillo: solo el conductor de protección, la tierra. Ese color no se usa para nada más.",
        "p4": "Y naranja: los circuitos que siguen con tensión aunque abras el seccionador del tablero, porque vienen de otra fuente. "
              "Así el electricista sabe que ahí hay peligro.",
        "p5": "Además, cada punta lleva un marcador con el número del hilo, el mismo del diagrama. Con colores y números, cualquiera da "
              "mantenimiento sin adivinar.",
        "cierre": CIERRE}),
    "a13": (("ASÍ FUNCIONA LA", "BOBINA DEL CONTACTOR"), {
        "gancho": "Un contactor de treinta y ocho amperios se mueve con una bobina que consume unos pocos voltamperios. ¿Cómo una corriente tan "
                  "pequeña mueve contactos tan grandes?",
        "p1": "Por dentro hay un núcleo fijo de hierro laminado, con forma de E, y la bobina de cobre alrededor, conectada a A uno y A dos. "
              "Enfrente está la armadura, otra E de hierro, unida a los contactos móviles y sostenida por un resorte.",
        "p2": "Al energizar la bobina, el núcleo se vuelve un electroimán y atrae a la armadura. Al moverse, la armadura cierra los contactos "
              "principales y cambia los auxiliares. Al quitar la tensión, el resorte la regresa.",
        "p3": "Al cerrar pasa algo interesante. Con el entrehierro abierto, la bobina tiene poca inductancia y pide una corriente de llamada "
              "alta. Cuando la armadura cierra, la inductancia sube y la corriente baja a la de mantenimiento, varias veces menor.",
        "p4": "En alterna, el flujo pasa por cero ciento veinte veces por segundo, y la armadura vibraría y zumbaría. Para evitarlo, el núcleo "
              "lleva una espira de sombra: un anillo de cobre que retrasa parte del flujo y mantiene la fuerza en el cruce por cero.",
        "p5": "Por eso la tensión de la bobina debe ser la del mando, ciento veinte voltios de alterna en este tablero. Si es más baja, no cierra "
              "bien y zumba; si es más alta, se calienta y se quema. Viene impresa en la bobina.",
        "cierre": CIERRE}),
    "a14": (("¿GUARDAMOTOR O", "BREAKER + TÉRMICO?"), {
        "gancho": "Para proteger un motor puedes poner un breaker y un relé térmico, o un solo aparato que hace las dos cosas: el guardamotor. "
                  "¿Cuál conviene?",
        "p1": "El guardamotor junta tres funciones: seccionamiento, con su manija de encendido y apagado; disparo magnético contra cortocircuito; "
              "y disparo térmico ajustable contra sobrecarga, con su dial en amperios.",
        "p2": "Con breaker más térmico, cada función va en su aparato: el breaker cuida el cortocircuito, y el térmico, montado bajo el "
              "contactor, la sobrecarga. Es lo que usamos en el tablero del motor de diez caballos.",
        "p3": "El guardamotor ahorra espacio y cableado, y muchos traen contactos auxiliares para avisar al mando que disparó. Además, el ajuste "
              "térmico y el magnético ya vienen coordinados para motores.",
        "p4": "Pero tiene un rango: cada modelo cubre una franja de corriente, por ejemplo de veintidós a treinta y dos amperios, y se elige "
              "con la corriente del motor. Y no reemplaza al contactor: para arrancar con pulsadores o un P L C, el contactor sigue haciendo falta.",
        "p5": "Ojo con la norma: en instalaciones con Nec, muchos guardamotores están listados solo como controlador manual y necesitan un "
              "breaker o fusibles antes. Solo los listados como tipo E pueden ir solos. Revisa la hoja del fabricante.",
        "cierre": CIERRE}),
    "a15": (("¿QUÉ SIGNIFICAN", "13-14 Y 21-22?"), {
        "gancho": "En el contactor dice trece, catorce, veintiuno, veintidós. No son números al azar: con solo leerlos sabes si el contacto es "
                  "abierto o cerrado.",
        "p1": "La regla viene de la norma europea E N cincuenta mil cinco y de la I E C sesenta mil novecientos cuarenta y siete. Cada contacto "
              "auxiliar tiene dos dígitos: el primero es el número de orden, y el segundo, la función.",
        "p2": "Si la función es uno dos, el contacto es normalmente cerrado: once doce, veintiuno veintidós. Si es tres cuatro, es normalmente "
              "abierto: trece catorce, cuarenta y tres cuarenta y cuatro.",
        "p3": "Cinco seis y siete ocho son de función especial, como los temporizados o los del relé térmico: noventa y cinco noventa y seis es "
              "cerrado y abre con la sobrecarga; noventa y siete noventa y ocho es abierto y cierra.",
        "p4": "Los contactos principales usan otra numeración: uno, tres y cinco son las entradas, L uno, L dos y L tres; dos, cuatro y seis, "
              "las salidas, T uno, T dos y T tres. Y la bobina es A uno A dos.",
        "p5": "En el diagrama, el número del borne va al lado de cada contacto. Por eso puedes cablear siguiendo el esquema sin ver el aparato: "
              "el trece catorce del diagrama es el trece catorce del contactor.",
        "cierre": CIERRE}),
}

if __name__ == "__main__":
    aq = pathlib.Path(__file__).parent
    for k, (tit, g) in R.items():
        (aq / f"guion_{k}.py").write_text(f'"""Reel {k.upper()} · serie arranques (fuentes en guiones_arr.py)."""\nTIT = {tit!r}\nGUION = {g!r}\n')
        print(k, sum(len(v) for v in g.values()))

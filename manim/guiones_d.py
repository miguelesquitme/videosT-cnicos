"""Guiones de los Shorts V19–V38 (9-nov-2026). Estándar: 1:30+, gancho → fundamento → dato real → consecuencia →
conclusión → cierre. Sin presentarse; números en palabras; cierre sin nombrar plataformas.

Fuentes verificadas:
 V19 tierra física: NEC 2020 250.53(A)(2) Excepción (electrodo de 25 Ω o menos), 250.4(A)(5) y 250.54 (la tierra
     NO es un camino efectivo de falla); 120 V / 25 Ω = 4,8 A (Python). 250.4(A)(1) (rayos y sobretensiones).
 V20 CA/CC: 60 Hz; V pico = 120 × √2 = 169,7 V; transformador solo con CA (inducción de Faraday); pérdidas I²R.
 V21 fotocelda: especificación de fotocontroles de Riverside Public Utilities según ANSI C136.10: encendido calibrado
     a 1,5 fc (× 10,764 = 16 lux), relación apagado/encendido ≤ 1,5, retardo de apagado 3–5 s, falla en "encendido".
 V22 toques: descarga electrostática (efecto triboeléctrico; se siente desde unos miles de voltios, energía muy
     pequeña) vs corriente de fuga de un aparato sin tierra (NEC 250.110/250.114; OSHA efectos de la corriente).
 V23 giro del motor: campo giratorio; invertir dos fases invierte la secuencia; n = 120 f / p (60 Hz, 4 polos = 1800 rpm).
 V24 efecto corona: el aire se ioniza cerca de ≈ 30 kV/cm (ley de Peek, nivel del mar); haces de conductores bajan
     el campo; la humedad lo aumenta.
 V25 fusible: elemento con estrechamientos, arena de sílice, I²t; NEC 240.6(A) valores normalizados; nunca puentear.
 V26 factor de potencia: P = √3·V·I·FP; corriente reactiva; capacitores de corrección.
 V27 sensor inductivo: oscilador + bobina, corrientes de Foucault; 3 hilos CC: café +, azul −, negro salida
     (IEC 60947-5-2); PNP entrega +, NPN entrega −; distancia menor en aluminio y cobre (según fabricante).
 V28 120 V en 240 V: P = V²/R; 1000 W a 120 V → R = 14,4 Ω → 4000 W y 16,7 A a 240 V (Python).
 V29 parpadeo: caída de tensión V = I·R; corriente de arranque del motor (5–8 × nominal; p. ej. 6,6× en la ficha
     Hyosung 5 hp); neutro flojo → luces que suben y bajan (peligro).
 V30 kWh: E = P·t; ejemplos calculados en Python.
 V31 variador: rectificador → bus de CC (≈ 1,35 × V de línea) → inversor IGBT con PWM; n = 120 f / p; leyes de
     afinidad: potencia ∝ velocidad³ (0,8³ = 0,51).
 V32 estrella-triángulo: 6 bornes U1 V1 W1 / U2 V2 W2 (IEC 60034-8); en estrella cada devanado recibe V/√3; arranque
     estrella-triángulo: corriente y par ≈ 1/3.
 V33 IP65: IEC 60529: 6 = hermético al polvo; 5 = chorros de agua (boquilla 6,3 mm, 12,5 L/min, a 3 m); 7 = inmersión
     a 1 m durante 30 min; X = sin ensayar.
 V34 paro de emergencia: ISO 13850 / IEC 60204-1: accionador rojo sobre fondo amarillo, enclavamiento mecánico, rearme
     deliberado, contactos de apertura directa (IEC 60947-5-5); rearmar NO debe arrancar la máquina.
 V35 LED que brilla apagado: acoplamiento capacitivo entre conductores paralelos, interruptor iluminado o que corta el
     neutro (NEC 404.2(B)); el driver acumula carga en su capacitor y destella.
 V36 agua pura: conductividad del agua destilada ≈ 1 µS/cm; agua de mar ≈ 50 000 µS/cm (City of Boulder / BASIN);
     conducen los iones disueltos.
 V37 pararrayos: NFPA 780 / IEC 62305: puntas captoras, bajantes, electrodos de tierra y uniones; esfera rodante de
     46 m (150 ft, NFPA 780); el pararrayos no atrae el rayo: lo intercepta y lo lleva a tierra.
 V38 PLC: ciclo de escaneo (leer entradas → ejecutar programa → escribir salidas); IEC 61131-3 (lenguajes LD, FBD, ST,
     SFC); escalera que imita los esquemas de relés.
"""

FIN = "Si te sirvió, suscríbete y sígueme."

G19 = {  # tierra física
    "gancho": "Tu casa tiene una varilla de cobre enterrada. Mucha gente cree que, si hay una falla, la corriente se va a la "
              "tierra y listo. Pero eso, por sí solo, no te protege. Te explico por qué.",
    "p1": "Imagina una lavadora con su carcasa metálica. Un cable de fase pierde el aislamiento y toca el metal. Ahora la "
          "carcasa tiene ciento veinte voltios, y quien la toque se convierte en el camino de la corriente.",
    "p2": "Si esa falla solo tuviera la tierra física para volver, haría falta pasar por la varilla. El Nec acepta un "
          "electrodo de veinticinco ohmios o menos. Ciento veinte voltios entre veinticinco ohmios: cuatro punto ocho "
          "amperios. Un breaker de veinte ni se entera, y la carcasa sigue energizada.",
    "p3": "Por eso el Nec dice que la tierra no es un camino efectivo para la corriente de falla. Lo que de verdad protege es "
          "el conductor de puesta a tierra de equipos, el cable verde, que regresa al tablero y se une al neutro en el "
          "tablero principal.",
    "p4": "Con ese camino de muy baja impedancia, la falla se vuelve un cortocircuito de cientos de amperios, y el breaker "
          "dispara en milisegundos. La carcasa queda sin tensión.",
    "p5": "Entonces, ¿para qué sirve la varilla? Para descargar rayos y sobretensiones y para estabilizar el voltaje respecto "
          "a la tierra. Necesitas las dos cosas: el electrodo y el cable verde hasta cada aparato.",
    "cierre": FIN,
}

G20 = {  # CA vs CC
    "gancho": "La batería del carro y el tomacorriente de tu casa dan electricidad, pero no es la misma. Una es corriente "
              "continua y la otra alterna. ¿Cuál es la diferencia y por qué a tu casa llega alterna?",
    "p1": "En la corriente continua, los electrones avanzan siempre en el mismo sentido y el voltaje es constante. Así "
          "funcionan las baterías, los paneles solares y casi todos los circuitos electrónicos.",
    "p2": "En la alterna, el voltaje sube, baja, cambia de polaridad y vuelve. En nuestra red lo hace sesenta veces por "
          "segundo: sesenta hercios. Y los ciento veinte voltios son un valor eficaz: el pico real llega a unos ciento "
          "setenta.",
    "p3": "¿Por qué se distribuye en alterna? Por el transformador. Solo funciona con alterna, porque necesita un campo "
          "magnético que cambia. Con él se sube el voltaje para transmitir y se baja para usarlo.",
    "p4": "Y subir el voltaje conviene: para la misma potencia, la corriente baja, y las pérdidas en los cables dependen del "
          "cuadrado de la corriente. Diez veces menos corriente, cien veces menos pérdidas.",
    "p5": "Por eso tu celular tiene un cargador: convierte la alterna del tomacorriente en continua de pocos voltios para la "
          "batería. Las dos conviven en tu casa todos los días.",
    "cierre": FIN,
}

G21 = {  # fotocelda
    "gancho": "Las luces de la calle se encienden solas al anochecer y se apagan al amanecer. No hay nadie con un "
              "interruptor. ¿Quién les dice cuándo? Una fotocelda.",
    "p1": "Arriba de la lámpara hay un pequeño domo. Adentro tiene un sensor de luz, una fotorresistencia o un fotodiodo, "
          "cuya resistencia o corriente cambia según la luz que recibe.",
    "p2": "Un circuito compara esa señal y maneja un relé que conecta la lámpara. Una especificación típica, basada en la "
          "norma Ansi C ciento treinta y seis punto diez, pide encender con uno punto cinco pie-candelas: unos dieciséis "
          "lux, la luz del atardecer.",
    "p3": "Para que no parpadee, apaga con un poco más de luz que la de encendido, máximo uno punto cinco veces más. Y tiene "
          "un retardo de tres a cinco segundos, para que los faros de un carro o un relámpago no la apaguen.",
    "p4": "Otro detalle: si la fotocelda se daña, falla en encendido. Es preferible una lámpara encendida de día que una "
          "calle a oscuras.",
    "p5": "Se conecta con una base de tres contactos que gira y traba. Si una lámpara se enciende y se apaga sola en la "
          "noche, revisa que su propia luz o un anuncio no le estén pegando a la fotocelda.",
    "cierre": FIN,
}

G22 = {  # toques al tocar metal
    "gancho": "¿Te da toques cuando tocas la manija de la puerta, el carro o la refrigeradora? No todos los toques son "
              "iguales. Uno es inofensivo y el otro puede matarte.",
    "p1": "El primero es la electricidad estática. Al caminar o rozar ropa, tu cuerpo gana o pierde electrones por efecto "
          "triboeléctrico. Al acercarte a un metal, la carga salta en una chispa.",
    "p2": "Esa chispa puede ser de miles de voltios, pero dura una fracción de microsegundo y tiene muy poca energía. Por "
          "eso solo da un susto. Pasa más en días secos, porque la humedad ayuda a que la carga se disipe.",
    "p3": "El segundo es muy distinto: un aparato con una fuga. Un cable dañado toca la carcasa de la refrigeradora o la "
          "lavadora, y sin conductor de tierra el metal queda energizado. Lo sientes como un hormigueo constante, no como "
          "una chispa.",
    "p4": "Ese hormigueo es corriente de ciento veinte voltios pasando por ti. Con las manos mojadas, unos pocos miliamperios "
          "más y ya no te puedes soltar.",
    "p5": "La regla: chispa de un instante, estática. Hormigueo que se repite al tocar un aparato, falla. Desconéctalo, no "
          "lo uses y revisa la tierra y el aislamiento con un electricista.",
    "cierre": FIN,
}

G23 = {  # giro del motor
    "gancho": "Conectas un motor trifásico y gira al revés. ¿La solución? Cambiar dos cables, cualquiera de los tres. "
              "¿Por qué funciona eso?",
    "p1": "Un motor trifásico tiene tres devanados, separados ciento veinte grados. Cada fase llega a su máximo en un momento "
          "distinto: primero la uno, luego la dos y luego la tres.",
    "p2": "Esa secuencia crea un campo magnético que gira dentro del motor, y el rotor lo persigue. A sesenta hercios, con "
          "cuatro polos, el campo gira a mil ochocientas revoluciones por minuto.",
    "p3": "Si intercambias dos fases, la secuencia cambia: ahora es uno, tres, dos. El campo gira al revés, y el rotor "
          "también.",
    "p4": "Si intercambias las tres en orden, la secuencia sigue igual y no pasa nada. Por eso son dos, y solo dos.",
    "p5": "Esto es crítico en bombas y compresores: algunos se dañan si giran al revés. Antes de acoplar la carga, da un "
          "pulso corto y revisa el sentido. Y en un inversor de giro, dos contactores hacen exactamente este cambio.",
    "cierre": FIN,
}

G24 = {  # efecto corona
    "gancho": "Si pasas debajo de una línea de alta tensión en una noche húmeda, puedes oír un chisporroteo. No es tu "
              "imaginación. Se llama efecto corona.",
    "p1": "Alrededor de un conductor con mucho voltaje hay un campo eléctrico intenso, sobre todo pegado a su superficie.",
    "p2": "Cuando ese campo supera la rigidez del aire, unos treinta kilovoltios por centímetro a nivel del mar, el aire "
          "cerca del cable se ioniza. Se forman pequeñas descargas que suenan y, en la oscuridad, dan un brillo azul.",
    "p3": "Con lluvia, neblina o humedad, las gotas en el cable crean puntas donde el campo es mayor, y el ruido aumenta.",
    "p4": "La corona es energía perdida y causa interferencia de radio. Por eso las líneas de muy alto voltaje usan varios "
          "conductores juntos por fase, llamados haces: así el campo en la superficie es menor.",
    "p5": "Que se escuche no significa que sea peligroso estar lejos, pero sí te recuerda que esa línea está energizada. "
          "Nunca acerques varillas, escaleras ni piscuchas.",
    "cierre": FIN,
}

G25 = {  # fusible
    "gancho": "Un fusible es un pedazo de metal que se derrite a propósito. Suena simple, pero está diseñado con mucha "
              "precisión. ¿Cómo funciona?",
    "p1": "Adentro tiene un elemento de plata o cobre con partes más angostas, llamadas cuellos. Ahí la resistencia es mayor, "
          "y con exceso de corriente se calientan primero.",
    "p2": "Con una sobrecarga se funden después de un tiempo. Con un cortocircuito, en milisegundos. Mientras más corriente, "
          "más rápido: el calor depende de la corriente al cuadrado por el tiempo.",
    "p3": "Al fundirse se forma un arco. En los fusibles industriales, el cuerpo está lleno de arena de sílice que absorbe el "
          "calor y apaga el arco.",
    "p4": "Comparado con un breaker, el fusible es simple, muy rápido y barato, pero se cambia cada vez que actúa.",
    "p5": "Y el error más peligroso: poner uno más grande, o un alambre en su lugar. El fusible protege al cable. Si lo "
          "puenteas, el próximo en fundirse puede ser el aislamiento dentro de la pared. Siempre reemplázalo por uno igual.",
    "cierre": FIN,
}

G26 = {  # factor de potencia
    "gancho": "Dos motores consumen la misma potencia útil, pero uno pide más corriente que el otro. La diferencia está en "
              "el factor de potencia.",
    "p1": "Un motor necesita corriente para hacer trabajo, la potencia activa, en kilovatios. Y también corriente para crear "
          "su campo magnético: la potencia reactiva. Esa va y viene sin hacer trabajo.",
    "p2": "Las dos forman un triángulo. La hipotenusa es la potencia aparente, en kilovoltamperios. El factor de potencia es "
          "activa entre aparente: qué tanto de lo que circula se aprovecha.",
    "p3": "En un motor trifásico, la potencia es raíz de tres por el voltaje por la corriente por el factor de potencia. Si "
          "el factor baja de cero punto noventa y cinco a cero punto setenta, la corriente sube un treinta y seis por "
          "ciento para la misma potencia.",
    "p4": "Más corriente significa cables más calientes, más pérdidas y transformadores más cargados. Por eso las empresas "
          "eléctricas pueden cobrar recargos a la industria con bajo factor de potencia.",
    "p5": "La solución son los capacitores: entregan la potencia reactiva cerca del motor, y la red ya no tiene que llevarla "
          "y traerla.",
    "cierre": FIN,
}

G27 = {  # sensor inductivo
    "gancho": "En las fábricas hay sensores que detectan una pieza de metal sin tocarla. ¿Cómo lo hacen? Son sensores "
              "inductivos.",
    "p1": "En la punta tienen una bobina alimentada por un oscilador. La bobina crea un campo magnético alterno justo "
          "delante de la cara del sensor.",
    "p2": "Cuando un metal entra en ese campo, se inducen en él corrientes de Foucault que le roban energía al oscilador. "
          "La oscilación baja, el circuito lo detecta y activa la salida.",
    "p3": "Solo detectan metales, y no todos a la misma distancia. La distancia nominal se mide con acero; con aluminio o "
          "cobre se detecta mucho más cerca, según el factor que indica el fabricante.",
    "p4": "Los de corriente continua suelen tener tres hilos. Según la I E C sesenta mil novecientos cuarenta y siete, parte "
          "cinco dos: café al positivo, azul al negativo y negro a la salida.",
    "p5": "Y aquí está la duda de siempre: un sensor P N P entrega positivo en su salida; uno N P N entrega negativo. Tiene "
          "que coincidir con la entrada de tu P L C, o no lo va a leer.",
    "cierre": FIN,
}

G28 = {  # 120 V en 240 V
    "gancho": "¿Qué pasa si conectas un aparato de ciento veinte voltios a doscientos cuarenta? No funciona el doble de "
              "bien. Recibe cuatro veces la potencia.",
    "p1": "Tomemos una resistencia de un calentador de mil vatios a ciento veinte voltios. Su resistencia es voltaje al "
          "cuadrado entre potencia: catorce punto cuatro ohmios.",
    "p2": "A doscientos cuarenta voltios, la misma resistencia recibe doscientos cuarenta al cuadrado entre catorce punto "
          "cuatro: cuatro mil vatios, y dieciséis punto siete amperios. El doble de voltaje, cuatro veces la potencia.",
    "p3": "El resultado: la resistencia se quema en segundos, y los aparatos electrónicos pueden destruirse en un instante.",
    "p4": "¿Y al revés? Un aparato de doscientos cuarenta conectado a ciento veinte recibe solo la cuarta parte: un "
          "calentador apenas calienta, y un motor puede no arrancar y sobrecalentarse.",
    "p5": "Antes de conectar, lee la etiqueta. Si dice cien a doscientos cuarenta voltios, funciona en los dos. Si dice un "
          "solo voltaje, respétalo.",
    "cierre": FIN,
}

G29 = {  # luces que parpadean
    "gancho": "Enciendes el microondas o arranca la refrigeradora y las luces bajan un instante. ¿Por qué pasa? ¿Y cuándo "
              "debe preocuparte?",
    "p1": "Los cables de tu casa, la acometida y el transformador tienen una pequeña resistencia. Cuando circula corriente, "
          "una parte del voltaje se queda en ellos: es la caída de tensión, voltaje igual a corriente por resistencia.",
    "p2": "Un motor, al arrancar, pide de cinco a ocho veces su corriente nominal durante un instante. Por ejemplo, un motor "
          "de cinco caballos puede pedir más de seis veces su corriente.",
    "p3": "Ese pico aumenta la caída de tensión en los conductores que compartes con las luces, y el voltaje baja por unos "
          "momentos. Cuando el motor acelera, la corriente baja y la luz vuelve.",
    "p4": "Un parpadeo leve al arrancar un motor es normal. Pero si las luces bajan mucho, o unas suben mientras otras bajan, "
          "puede ser un neutro flojo. Eso es peligroso: hay aparatos que reciben más voltaje del normal.",
    "p5": "Si notas eso, apaga los aparatos sensibles y llama a un electricista para revisar las conexiones del tablero y de "
          "la acometida.",
    "cierre": FIN,
}

G30 = {  # kWh
    "gancho": "Tu recibo de luz no cobra vatios. Cobra kilovatios hora. Y si entiendes la diferencia, puedes calcular cuánto "
              "te cuesta cada aparato.",
    "p1": "El vatio mide potencia: qué tan rápido usa energía un aparato. El kilovatio hora mide energía: potencia por "
          "tiempo. Mil vatios durante una hora es un kilovatio hora.",
    "p2": "Ejemplo: una plancha de mil doscientos vatios durante media hora gasta cero punto seis kilovatios hora. Un "
          "televisor de cien vatios, cinco horas al día durante treinta días: quince kilovatios hora al mes.",
    "p3": "Lo que más gasta no siempre es lo más potente, sino lo que pasa más tiempo encendido. Una refrigeradora trabaja "
          "todo el día, aunque su motor se encienda y se apague.",
    "p4": "Y las cargas que calientan, como la ducha o la plancha, son de las que más energía usan en poco tiempo.",
    "p5": "Para saber cuánto cuesta, multiplica los kilovatios hora por la tarifa de tu recibo. Con eso decides qué cambiar "
          "primero.",
    "cierre": FIN,
}

G31 = {  # variador de frecuencia
    "gancho": "Un motor de inducción gira casi siempre a la misma velocidad. Pero en muchas fábricas la cambian con un "
              "aparato: el variador de frecuencia. ¿Cómo lo hace?",
    "p1": "La velocidad del campo del motor es ciento veinte por la frecuencia entre el número de polos. Si cambias la "
          "frecuencia, cambias la velocidad. A treinta hercios, un motor de cuatro polos gira cerca de novecientas "
          "revoluciones.",
    "p2": "El variador hace tres pasos. Primero, un rectificador convierte la alterna en continua. Segundo, capacitores la "
          "filtran: es el bus de continua.",
    "p3": "Tercero, transistores I G B T conmutan miles de veces por segundo y arman una nueva alterna con pulsos de ancho "
          "variable, a la frecuencia que pidas. Además baja el voltaje junto con la frecuencia, para no saturar el motor.",
    "p4": "La gran ventaja está en bombas y ventiladores: la potencia baja con el cubo de la velocidad. Al ochenta por ciento "
          "de velocidad, consume cerca del cincuenta y uno por ciento de la potencia.",
    "p5": "Además arranca suave, sin el pico de corriente del arranque directo. Por eso cada vez más motores trabajan con "
          "variador.",
    "cierre": FIN,
}

G32 = {  # estrella y triángulo
    "gancho": "¿Por qué un motor trifásico tiene seis bornes, si solo llegan tres fases? Porque se puede conectar de dos "
              "formas: en estrella o en triángulo.",
    "p1": "Los seis bornes son los dos extremos de sus tres devanados: U uno, V uno y W uno, y U dos, V dos y W dos. Con "
          "puentes se decide cómo se unen.",
    "p2": "En estrella, los tres finales se unen en un punto. Cada devanado queda con el voltaje de línea dividido entre "
          "raíz de tres. En triángulo, cada devanado queda entre dos fases, con el voltaje completo.",
    "p3": "Por eso la placa dice dos voltajes, por ejemplo doscientos treinta y cuatrocientos. El menor es en triángulo y el "
          "mayor en estrella. Así el mismo motor sirve en dos redes.",
    "p4": "Y hay un truco: arrancar en estrella y pasar a triángulo. En estrella cada devanado recibe menos voltaje, y la "
          "corriente y el par de arranque bajan a cerca de un tercio.",
    "p5": "Un error común es conectar en triángulo un motor que debía ir en estrella. Recibe raíz de tres veces más voltaje "
          "y se quema. Revisa siempre la placa y los puentes.",
    "cierre": FIN,
}

G33 = {  # IP65
    "gancho": "En una lámpara, una caja o un sensor dice I P sesenta y cinco. No es un modelo. Es un código de la norma I E "
              "C sesenta mil quinientos veintinueve, y te dice dónde lo puedes instalar.",
    "p1": "La primera cifra es la protección contra sólidos. El seis significa hermético al polvo: no entra nada, ni "
          "siquiera en una cámara de polvo con vacío.",
    "p2": "La segunda es contra el agua. El cinco significa chorros de agua: en la prueba se lanzan doce punto cinco litros "
          "por minuto con una boquilla de seis punto tres milímetros desde tres metros.",
    "p3": "Un I P sesenta y siete aguanta inmersión a un metro durante treinta minutos. Pero ojo: soportar inmersión no "
          "siempre garantiza soportar chorros fuertes. Son pruebas distintas.",
    "p4": "Si ves una X, por ejemplo I P X cinco, significa que esa protección no se ensayó.",
    "p5": "Para exteriores con lluvia, busca al menos un I P sesenta y cinco. Y recuerda: al hacer las conexiones y pasar los "
          "cables, se debe mantener ese grado. Un mal empaque y el número ya no vale.",
    "cierre": FIN,
}

G34 = {  # paro de emergencia
    "gancho": "En toda máquina industrial hay un botón rojo con fondo amarillo. Parece un botón de paro cualquiera, pero no "
              "lo es. Tiene reglas muy estrictas.",
    "p1": "El paro de emergencia está normado por la Iso trece mil ochocientos cincuenta y la I E C sesenta y dos cero "
          "cuatro. Rojo sobre fondo amarillo, para encontrarlo en un segundo. Y con forma de hongo, para golpearlo con la "
          "palma.",
    "p2": "Al presionarlo se queda enclavado. No regresa solo. Para soltarlo hay que girarlo o jalarlo: una acción "
          "deliberada.",
    "p3": "Sus contactos son de apertura directa: el mismo empuje mecánico los separa, aunque estén soldados. No depende de "
          "un resorte.",
    "p4": "Y algo clave: soltar el hongo no debe arrancar la máquina. Solo permite que alguien la vuelva a arrancar con el "
          "botón de marcha.",
    "p5": "El paro de emergencia es una medida complementaria. No reemplaza las guardas ni el bloqueo para mantenimiento. "
          "Pero cuando algo sale mal, es lo primero que debes alcanzar.",
    "cierre": FIN,
}

G35 = {  # LED que brilla apagado
    "gancho": "Apagas la luz y el foco LED sigue brillando un poquito, o destella cada tantos segundos. No está poseído. "
              "Tiene explicación.",
    "p1": "Un foco LED tiene un pequeño circuito, el driver, con un capacitor. Necesita muy poca corriente para que el LED "
          "emita algo de luz.",
    "p2": "Primera causa: el interruptor corta el neutro en lugar de la fase. El foco queda conectado a la fase, y por "
          "acoplamiento hay una corriente diminuta. Además es peligroso: el portalámparas queda energizado. El Nec pide "
          "que el interruptor corte la fase.",
    "p3": "Segunda: cables largos que van paralelos. Entre ellos se forma un capacitor, y aunque el interruptor esté abierto, "
          "pasa una corriente muy pequeña.",
    "p4": "Tercera: interruptores con luz piloto o sensores que necesitan un poquito de corriente para funcionar, y la toman "
          "a través del foco.",
    "p5": "Con esa corriente, el capacitor del driver se carga y, al llegar a cierto voltaje, destella. Revisa primero que "
          "el interruptor corte la fase. Si es por los cables o el interruptor, existen cargas de compensación.",
    "cierre": FIN,
}

G36 = {  # agua pura
    "gancho": "Te han dicho que el agua conduce la electricidad. Pero el agua pura casi no conduce. Lo que conduce es lo que "
              "lleva disuelto.",
    "p1": "Para que haya corriente se necesitan cargas que se puedan mover. En un metal son electrones libres. En el agua "
          "son iones: átomos con carga, como los de la sal y los minerales.",
    "p2": "El agua destilada tiene muy pocos iones. Su conductividad ronda un microsiemens por centímetro. El agua de mar "
          "anda por los cincuenta mil: cincuenta mil veces más.",
    "p3": "El agua de la llave, la lluvia que corre por el suelo o el sudor tienen sales disueltas. Por eso, en la práctica, "
          "toda el agua que encontrarás conduce.",
    "p4": "Y tu piel mojada conduce mucho más que seca. La resistencia del cuerpo puede bajar de cien mil ohmios a unos mil, "
          "y la corriente sube cien veces con el mismo voltaje.",
    "p5": "Así que el dato es cierto en el laboratorio, pero no en tu casa. Nunca manipules aparatos eléctricos con las manos "
          "mojadas ni cerca del agua.",
    "cierre": FIN,
}

G37 = {  # pararrayos
    "gancho": "Un pararrayos no atrae los rayos. Tampoco los evita. Entonces, ¿qué hace exactamente?",
    "p1": "Un sistema de protección contra rayos tiene tres partes: puntas captoras en lo alto, conductores de bajada por "
          "fuera del edificio y electrodos enterrados. Todo bien unido.",
    "p2": "Cuando un rayo va a caer cerca, la punta le ofrece un punto de impacto. Así el rayo no golpea el techo, el "
          "concreto o una antena.",
    "p3": "Los bajantes llevan esa corriente, que puede ser de decenas de miles de amperios, hasta la tierra por un camino "
          "conocido y de baja impedancia, lejos de las personas y de los cables.",
    "p4": "Para decidir dónde poner las puntas, la N F P A setecientos ochenta usa el método de la esfera rodante: se imagina "
          "una esfera de cuarenta y seis metros rodando sobre el edificio. Donde la esfera toca, hace falta protección.",
    "p5": "Y no basta con la punta: también se unen las tuberías y la tierra eléctrica, y se ponen supresores de "
          "sobretensión en el tablero. Si no, el rayo puede entrar por los cables.",
    "cierre": FIN,
}

G38 = {  # PLC
    "gancho": "Antes, una máquina se controlaba con decenas de relés y cables. Hoy, con un aparato del tamaño de un libro: el "
              "P L C. ¿Qué es y cómo funciona?",
    "p1": "P L C significa controlador lógico programable. Es una computadora industrial hecha para el polvo, el calor y el "
          "ruido eléctrico de una fábrica.",
    "p2": "Tiene entradas, donde se conectan pulsadores, sensores y flotadores; y salidas, que manejan bobinas de "
          "contactores, luces y válvulas.",
    "p3": "Funciona en un ciclo que se repite en milisegundos: lee todas las entradas, ejecuta el programa y actualiza las "
          "salidas. Una y otra vez.",
    "p4": "El programa se escribe en lenguajes de la norma I E C sesenta y un mil ciento treinta y uno, parte tres. El más "
          "usado es el diagrama escalera, que se parece a un esquema de relés. Por ejemplo: si el flotador marca nivel bajo "
          "y no hay falla, enciende la bomba.",
    "p5": "La ventaja: para cambiar cómo trabaja la máquina, cambias el programa, no el cableado. Y es la puerta de entrada a "
          "la automatización industrial.",
    "cierre": FIN,
}

GUIONES_D = {
    "v19": ("¿Por qué es importante", "la TIERRA FÍSICA?", G19),
    "v20": ("¿Corriente ALTERNA", "o CONTINUA?", G20),
    "v21": ("¿Por qué las luces de la", "calle se ENCIENDEN SOLAS?", G21),
    "v22": ("¿Por qué me da TOQUES", "algo METÁLICO?", G22),
    "v23": ("¿Por qué el motor", "gira AL REVÉS?", G23),
    "v24": ("¿Por qué SUENAN los cables", "de alta tensión?", G24),
    "v25": ("¿Cómo funciona", "un FUSIBLE?", G25),
    "v26": ("¿Qué es el", "FACTOR DE POTENCIA?", G26),
    "v27": ("¿Cómo detecta METAL", "un sensor inductivo?", G27),
    "v28": ("¿Qué pasa si conectas", "120 V a 240 V?", G28),
    "v29": ("¿Por qué BAJAN las luces", "cuando algo arranca?", G29),
    "v30": ("¿Qué es un", "KILOVATIO HORA?", G30),
    "v31": ("¿Cómo funciona un", "VARIADOR de frecuencia?", G31),
    "v32": ("¿ESTRELLA o", "TRIÁNGULO?", G32),
    "v33": ("¿Qué significa", "IP65?", G33),
    "v34": ("¿Por qué el paro de", "EMERGENCIA es así?", G34),
    "v35": ("¿Por qué el LED", "BRILLA APAGADO?", G35),
    "v36": ("¿El agua pura", "CONDUCE?", G36),
    "v37": ("¿Cómo funciona un", "PARARRAYOS?", G37),
    "v38": ("¿Qué es un", "PLC?", G38),
}

if __name__ == "__main__":
    tot = 0
    for k, (_, _, g) in GUIONES_D.items():
        n = sum(len(v) for v in g.values())
        tot += n
        print(k, n, "chars ≈", round(n / 15.5), "s")
    print("total", tot)
    print(1 / 0.95 * 0.95 / 0.70, 0.95 / 0.70, 1200 * 0.5 / 1000, 100 * 5 * 30 / 1000, 120 * 30 / 2)


# ---- ampliación (p6) para que cada Short supere 1:30 con fundamento extra
_P6 = {
    "v19": "Un dato más: el cable verde debe llegar a cada tomacorriente y a cada carcasa metálica. Si tu tomacorriente tiene "
           "el agujero redondo pero la caja no tiene cable de tierra, ese agujero no está conectado a nada, y la protección "
           "es solo apariencia. Revísalo con un probador de tomacorrientes; cuesta poco y te dice en segundos si la tierra "
           "existe.",
    "v20": "Y un dato curioso: la alterna también tiene ventajas en los motores. Un motor de inducción, el más usado en la "
           "industria, funciona gracias a que el campo cambia. No necesita escobillas ni conmutador, por eso es tan simple "
           "y resistente. Aun así, hoy muchas líneas muy largas y los paneles solares usan continua, y la electrónica de "
           "potencia convierte de una a otra con muy buena eficiencia.",
    "v21": "La fotocelda también ahorra energía, porque la lámpara solo trabaja cuando hace falta. Y en tu casa puedes usar "
           "la misma idea: una fotocelda para la luz del garaje o del jardín. Se conecta en serie con la lámpara, con su "
           "cable de fase de entrada, su salida hacia la lámpara y su neutro. Respeta la potencia máxima que indica, sobre "
           "todo si la carga es de LED, porque su corriente de arranque puede ser alta.",
    "v22": "Para reducir la estática, toca primero el metal con una llave o con los nudillos: la chispa salta desde la llave "
           "y casi no la sientes. En casa ayuda un poco de humedad en el ambiente. Pero para el hormigueo de un aparato no "
           "hay truco: la única solución es reparar la falla y tener el conductor de tierra conectado hasta el tablero.",
    "v23": "En el motor, el rotor nunca alcanza del todo la velocidad del campo. Esa diferencia se llama deslizamiento, y es "
           "lo que permite que se induzca corriente en el rotor y aparezca el par. Por eso un motor de cuatro polos a "
           "sesenta hercios no gira a mil ochocientas exactas, sino a unas mil setecientas sesenta y cinco, como indica su "
           "placa. Con un medidor de secuencia de fases puedes saber el giro antes de conectar.",
    "v24": "En algunas subestaciones también se ve en los herrajes con puntas o bordes filosos. Por eso los equipos de alto "
           "voltaje usan anillos y piezas redondeadas, llamadas anillos anticorona, que reparten el campo. Y las cámaras de "
           "inspección ultravioleta detectan la corona de día, para encontrar aisladores sucios o dañados antes de que "
           "fallen.",
    "v25": "Los fusibles tienen tipos. Los de acción rápida protegen electrónica; los de acción retardada aguantan la "
           "corriente de arranque de un motor sin fundirse, pero siguen siendo rápidos ante un cortocircuito. En la "
           "industria verás letras como g G, para uso general, o a M, para acompañamiento de motores. Escoger el tipo "
           "correcto es tan importante como escoger los amperios.",
    "v26": "Veamos un ejemplo: un motor que necesita diez kilovatios a cuatrocientos ochenta voltios. Con factor de potencia "
           "cero punto noventa y cinco pide unos doce punto siete amperios. Con cero punto setenta, unos diecisiete punto "
           "dos. La misma máquina, el mismo trabajo, casi cinco amperios más por cada fase. Y los motores trabajando con "
           "poca carga tienen peor factor de potencia: un motor sobredimensionado también te cuesta.",
    "v27": "Otra cosa: estos sensores tienen una salida normalmente abierta o normalmente cerrada, y casi siempre un LED que "
           "indica cuándo detectan. Antes de culpar al programa, mira ese LED: si enciende cuando acercas el metal, el "
           "sensor funciona y el problema está en el cableado o en la entrada. También existen los capacitivos, que "
           "detectan líquidos y plásticos, pero esa es otra historia.",
    "v28": "Esto también pasa por error en los tableros con dos fases: un tomacorriente conectado entre dos fases en lugar "
           "de fase y neutro entrega doscientos cuarenta. Por eso los tomacorrientes de doscientos cuarenta voltios tienen "
           "otra forma de patas, según la configuración Nema, para que no puedas conectar un aparato de ciento veinte. No "
           "uses adaptadores para forzar una clavija.",
    "v29": "Una caída de tensión pequeña es inevitable, pero se diseña para que sea baja. Como recomendación, el Nec sugiere "
           "no pasar del tres por ciento en un circuito y del cinco por ciento en total, desde la acometida hasta el último "
           "aparato. Cuando un circuito es muy largo, se usa un calibre mayor. Así los motores arrancan mejor y las luces "
           "casi no se notan.",
    "v30": "Un truco: los aparatos en espera también suman. Un decodificador o una bocina que consumen cinco vatios todo el "
           "día, todo el mes, suman tres punto seis kilovatios hora. Poco a poco, varios aparatos así se notan. Y un "
           "medidor enchufable de energía te dice el consumo real de cualquier aparato en kilovatios hora, mejor que "
           "cualquier estimación.",
    "v31": "Pero el variador también tiene cuidados. Los pulsos rápidos pueden causar ruido eléctrico, así que se usa cable "
           "apantallado y una buena tierra. A muy baja velocidad, el ventilador del propio motor enfría poco. Y el variador "
           "se programa con los datos de la placa del motor: voltaje, corriente, frecuencia y velocidad, para que lo proteja "
           "bien.",
    "v32": "En la caja de bornes, los puentes se ponen así: para estrella, los puentes unen en una línea los tres bornes de "
           "arriba: W dos, U dos y V dos. Para triángulo, los tres puentes van en vertical, cada uno une un borne de arriba con el de abajo: W "
           "dos con U uno, U dos con V uno, y V dos con W uno. Casi todas las tapas de la caja de bornes traen el dibujo de las dos conexiones.",
    "v33": "Hay más ejemplos que verás seguido: un I P veinte es un aparato para interiores, que solo evita meter los dedos. "
           "Un I P cuarenta y cuatro ya resiste salpicaduras. Y en zonas de lavado con manguera a presión se usa I P sesenta "
           "y seis o más. Elige el grado por el lugar donde se instala, no por la marca ni por el precio.",
    "v34": "En el esquema, el paro de emergencia va en serie con todo el circuito de mando, y en máquinas grandes actúa sobre "
           "un relé de seguridad que vigila sus dos canales. Según la I E C sesenta y dos cero cuatro, la parada puede ser "
           "categoría cero, cortando la energía de inmediato, o categoría uno, frenando primero y luego cortando. Se prueba "
           "de forma periódica, no solo cuando hay un accidente.",
    "v35": "Para saber cuál es tu caso, apaga el interruptor y mide con un probador entre el portalámparas y la tierra. Si "
           "marca voltaje, el interruptor está en el neutro y hay que corregirlo. Si no, prueba con un foco de otra marca, "
           "porque algunos drivers son más sensibles. Y si el destello sigue, existen capacitores de compensación que se "
           "conectan en paralelo con el foco.",
    "v36": "Por eso el agua destilada se usa en algunos laboratorios y en baterías de plomo ácido: no contamina con minerales. "
           "Y por eso un rociador de agua no es un extintor para fuegos eléctricos: el agua común conduce. En la industria, "
           "la conductividad del agua se mide para controlar calderas y torres de enfriamiento, porque indica cuántos "
           "minerales lleva disueltos.",
    "v37": "Los rayos tienen corrientes que en promedio rondan los treinta mil amperios, y algunos superan los cien mil. Con "
           "esas corrientes, cualquier conexión floja se vuelve un punto caliente. Por eso los bajantes se fijan bien, se "
           "evitan curvas cerradas y se revisa el sistema cada cierto tiempo, sobre todo después de que cae un rayo.",
    "v38": "Un ejemplo real: un tanque con dos flotadores, uno de nivel bajo y otro de nivel alto. El P L C enciende la bomba "
           "cuando el nivel baja, la mantiene encendida con un enclavamiento en el programa y la apaga al llegar arriba. Y si "
           "el relé térmico dispara, la entrada de falla apaga todo y enciende una luz. Lo que antes eran cinco relés, hoy "
           "son unas pocas líneas de programa.",
}
for _k, (_a, _b, _g) in list(GUIONES_D.items()):
    _cierre = _g.pop("cierre")
    _g["p6"] = _P6[_k]
    _g["cierre"] = _cierre

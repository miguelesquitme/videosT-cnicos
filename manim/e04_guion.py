"""
E04 · CÓMO CONECTAR UN TOMACORRIENTE CON TIERRA (NEMA 5-15) (horizontal).
Verificado:
 - NEMA 5-15: 125 V, 15 A, con tierra; la ranura del neutro es más ancha que la de fase; la pata de tierra es más
   larga y conecta primero (Wikipedia, NEMA connector).
 - NEC 2020 200.10(B): en tomacorrientes y clavijas polarizadas, el terminal del neutro se identifica con metal
   blanco o plateado.
 - NEC 2020 406.4(A) y (B): en circuitos de 15 y 20 A, tomacorrientes con tierra, y su contacto de tierra conectado
   a la tierra de equipos.  · 250.146: puente de unión del tomacorriente a la caja metálica (salvo excepciones).
 - NEC 2020 240.4(D)(5): cobre 12 AWG → 20 A.  · Tabla 210.21(B)(3): circuito de 20 A con dos o más
   tomacorrientes → tomacorrientes de 15 o 20 A.  · 210.21(B)(1): uno solo en circuito individual → no menor que
   el circuito.  · 406.12: en viviendas, tomacorrientes a prueba de manipulación (TR).
 - NEC 2020 250.24(A)(5): el neutro no se conecta a la tierra de equipos después del equipo de acometida.
"""
GUION = {
    "intro": "Lo usas todos los días, pero ¿sabes qué significa cada agujero del "
             "tomacorriente? ¿Por qué uno es más grande que el otro? ¿Y para qué sirve el redondo? Hoy armamos un "
             "circuito de tomacorrientes con tierra, completo, del tablero a la placa, y te explico el porqué de cada "
             "conexión.",
    "nema": "Empecemos por el nombre. El tomacorriente más común en nuestras casas se llama NEMA cinco quince. El cinco "
            "indica que es de ciento veinticinco voltios y con tierra. El quince indica que es de quince amperios. Y "
            "una letra al final te dice si es el tomacorriente, con R, o la clavija del aparato, con P.",
    "agujeros": "Ahora, los agujeros. La ranura más pequeña es la fase. La ranura más grande es el neutro. Y el agujero "
                "redondo es la tierra. Por eso muchas clavijas tienen una pata más ancha: solo entra de una forma, y la "
                "fase siempre queda en su lugar. Y fíjate en la pata de tierra: es más larga, así que es la primera en "
                "conectarse y la última en desconectarse.",
    "terminales": "Por detrás, cada color de tornillo tiene su cable. Los tornillos de latón son para la fase. Los "
                  "plateados, para el neutro: así lo identifica el Nec dos mil veinte. Y el tornillo verde, para la "
                  "tierra. Entre cada par de tornillos hay una pestaña que los une, para que los dos tomacorrientes del "
                  "dúplex funcionen juntos.",
    "tierra_para": "¿Y para qué sirve la tierra? Imagina una lavadora o una refrigeradora con carcasa de metal. Si un cable interno se pela y toca el metal, sin tierra la carcasa queda energizada, esperando a que alguien la toque. Con tierra, esa falla tiene un camino directo al tablero, la corriente sube de golpe, y el breaker se dispara.",
    "polarizada": "Y la polaridad también importa. Acuérdate del video de la lámpara: el neutro debe llegar a la rosca del portalámparas. Una clavija polarizada asegura que, en una lámpara de mesa, la rosca quede del lado del neutro, siempre que el tomacorriente esté bien conectado.",
    "circuito": "Nuestro circuito será de veinte amperios, con cable calibre doce de cobre, que es el que corresponde a "
                "esa protección. ¿Y se pueden poner tomacorrientes de quince amperios en un circuito de veinte? Sí, "
                "cuando el circuito alimenta dos o más tomacorrientes. Pero si es un solo tomacorriente en un circuito "
                "exclusivo, ese tomacorriente debe ser de veinte amperios.",
    "veinte": "Por cierto, existe también el tomacorriente de veinte amperios, el NEMA cinco veinte. Se reconoce porque su ranura de neutro tiene forma de T, así acepta clavijas de quince y de veinte amperios. Pero una clavija de veinte amperios no entra en un tomacorriente de quince.",
    "vatios": "¿Y cuánto aguanta un tomacorriente de quince amperios? Con la fórmula de potencia, ciento veinte voltios por quince amperios dan mil ochocientos vatios. Ojo con las regletas: si conectas un hervidor y una plancha juntos, fácilmente te pasas.",
    "herramientas": "Y las herramientas: un desarmador plano y uno de estrella, un pelacables, una pinza, el multímetro, y un probador de voltaje. Y antes de empezar, como siempre: breaker apagado, y verificar que no haya tensión.",
    "seguridad": "Antes de tocar un solo cable: baja el breaker del circuito, y verifica con un probador que no haya tensión. Nunca supongas que algo está apagado. Compruébalo siempre.",
    "materiales": "Necesitas: un breaker de un polo de veinte amperios, tubo EMT de media pulgada con conectores y "
                  "abrazaderas, dos cajas rectangulares, dos tomacorrientes dúplex con tierra, sus placas, conectores de "
                  "empalme, y cable THHN calibre doce, de varios hilos: negro para la fase, blanco para el neutro, y "
                  "verde para la tierra.",
    "recorrido": "El recorrido: del tablero, un tubo llega a la primera caja. Y de la primera caja, otro tubo continúa a "
                 "la segunda. Así alimentamos los dos tomacorrientes con el mismo circuito.",
    "cableado": "Jalamos los cables. Del tablero a la primera caja van tres: negro, blanco y verde. Y de la primera caja "
                "a la segunda, otros tres, de los mismos colores. Deja por lo menos quince centímetros de cable libre en "
                "cada caja para poder trabajar con comodidad.",
    "tablero": "En el tablero: el negro va al breaker de veinte amperios, el blanco a la barra de neutros, y el verde a "
               "la barra de tierra. Aprieta cada tornillo con el torque que indica el fabricante.",
    "colas": "En la primera caja hay un buen truco: en lugar de usar el tomacorriente como puente, haz colas. Une los "
             "dos negros con un tramo corto de cable negro, y ese tramo va al tomacorriente. Lo mismo con los blancos y "
             "con los verdes. Así, si un tomacorriente falla o lo cambias, el siguiente sigue funcionando.",
    "conexion": "Ahora conectamos. Pelamos cada cable, torcemos los hilos para que no se abran, y formamos el gancho "
                "en el sentido de las agujas del reloj. El negro va al tornillo de latón. El blanco, al plateado. Y el "
                "verde, al tornillo verde.",
    "tierra_caja": "Y como la caja es metálica, también se une a la tierra: una cola verde va del empalme de tierras al "
                   "tornillo verde de la caja. Así, si una fase toca el metal, la falla tiene un camino directo de "
                   "regreso al tablero, y el breaker se dispara.",
    "segunda": "La segunda caja es más sencilla: es la última del circuito, así que los cables van directo al "
               "tomacorriente. Negro al latón, blanco al plateado, verde al verde, y una cola de tierra para la caja.",
    "tr": "Un detalle de seguridad: en viviendas, el Nec dos mil veinte pide tomacorrientes a prueba de manipulación, "
          "marcados con las letras T R. Por dentro tienen persianas que solo se abren cuando entran las dos patas a la "
          "vez, para que un niño no pueda meter un objeto por un solo agujero.",
    "placa": "Doblamos los cables con cuidado hacia el fondo de la caja, atornillamos el tomacorriente, y colocamos la "
             "placa. Ahora sí: subimos el breaker.",
    "prueba": "Y probamos con el multímetro en voltaje. Entre fase y neutro debe marcar cerca de ciento veinte voltios. "
              "Entre fase y tierra, también cerca de ciento veinte. Y entre neutro y tierra, prácticamente cero. Si eso "
              "se cumple, la polaridad y la tierra están bien.",
    "probador": "También puedes usar un probador de tomacorrientes, el que tiene tres lucecitas. Lo enchufas, y la combinación de luces encendidas te dice si todo está correcto, si falta la tierra, si falta el neutro, o si la fase y el neutro están invertidos. La tabla viene impresa en el mismo probador.",
    "dividido": "Un dato extra: si con unas pinzas quitas la pestaña de latón, cada mitad del tomacorriente queda independiente. Así puedes, por ejemplo, controlar una mitad con un interruptor de pared y dejar la otra siempre energizada. Rompe solo la pestaña de latón, la de la fase, y deja la plateada.",
    "caliente": "Y si algún día ves un tomacorriente caliente, decolorado, o con olor a quemado, baja el breaker y revísalo. Casi siempre es un tornillo flojo o un cable mal apretado.",
    "viejo": "¿Y si vas a cambiar un tomacorriente viejo, de dos agujeros, y en la caja no hay tierra? No pongas uno de tres agujeros así nada más: el redondo quedaría sin conectar. El Nec dos mil veinte da opciones para ese caso, como poner otro sin tierra, o uno con protección de falla a tierra marcado con la leyenda: sin tierra de equipos.",
    "repaso": "Repasemos. Del tablero sale el circuito de veinte amperios. En la primera caja, colas para la fase, el neutro y la tierra. En la segunda, conexión directa. Y en las dos cajas, la tierra también llega al metal de la caja.",
    "errores": "Tres errores muy comunes. Uno: invertir fase y neutro. El aparato funciona, pero partes que deberían "
               "estar sin tensión, como la rosca de una lámpara, quedan energizadas. Dos: dejar la tierra sin conectar. "
               "Todo parece funcionar, hasta que hay una falla. Y tres: hacer un puente entre neutro y tierra en el "
               "tomacorriente para engañar al probador. Eso está prohibido: el neutro y la tierra solo se unen en el "
               "tablero principal.",
    "cierre": "En resumen: la ranura pequeña es la fase y va al tornillo de latón, la grande es el neutro y va al "
              "plateado, y la redonda es la tierra, al tornillo verde y a la caja. Si te sirvió, suscríbete en YouTube y "
              "sígueme en Facebook. Nos vemos en el próximo video.",
}

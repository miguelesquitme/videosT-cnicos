"""
E03 · APAGADOR DE ESCALERA (3 vías), paso a paso (horizontal).
Verificado:
 - NEC 2020 404.2(A): los interruptores de 3 y 4 vías conmutan solo el conductor no puesto a tierra (fase);
   en tubería metálica, el cableado entre interruptores y salidas cumple 300.20(A) (todos los conductores del
   circuito en la misma tubería).  · NEC 2020 404.2(B): el interruptor no desconecta el neutro.
 - Leviton 5603-2 (instructivo): común = tornillo negro/oscuro; viajeros = tornillos de latón; tierra = verde.
 - NEC 2020 240.4(D)(3): cobre 14 AWG → 15 A.  · Cable THHN de 7 hilos (NEC Tabla 8, "stranding 7").
"""
GUION = {
    "intro": "Enciendes la luz al pie de la escalera, subes, y la apagas desde "
             "arriba. ¿Cómo puede un mismo foco obedecer a dos interruptores distintos? Hoy lo vas a entender, y lo vamos "
             "a armar completo, paso a paso: desde el tablero, con tubería, cajas, cable y conexiones reales, hasta "
             "encender el foco desde los dos lados.",
    "usos": "¿Dónde se usa? En escaleras, en pasillos largos, en habitaciones con dos puertas, y en garajes. En cualquier lugar donde entras por un lado y sales por el otro, y no quieres caminar a oscuras para apagar la luz.",
    "nombre": "¿Por qué se llama de tres vías? Porque tiene tres terminales de conexión, sin contar la tierra. En otros países le dicen conmutador o interruptor de escalera.",
    "idea": "Primero, la idea. Un interruptor sencillo es como una puerta: abre o cierra el paso de la corriente. "
            "El de tres vías es distinto: es un selector. Tiene un terminal común, y dos caminos posibles, que llamamos "
            "viajeros. El común siempre está conectado a uno de los dos viajeros. Nunca está simplemente apagado.",
    "anatomia": "Míralo de cerca. Tiene tres tornillos de conexión y uno verde. El tornillo de color oscuro es el "
                "común. Los dos tornillos de latón son los viajeros. Y el verde es la tierra. Fíjate también que la "
                "palanca no dice encendido ni apagado: en un tres vías, arriba o abajo depende del otro interruptor.",
    "esquema": "Ahora el esquema. La fase del tablero llega al común del primer interruptor. Del primer interruptor al "
               "segundo van los dos viajeros. Y del común del segundo interruptor sale el retorno hacia el foco. El "
               "neutro, en cambio, no pasa por ningún interruptor: va directo al foco.",
    "tabla": "Veamos las cuatro combinaciones. Si los dos comunes apuntan al mismo viajero, el camino está completo, y "
             "el foco enciende. Si apuntan a viajeros distintos, el camino se corta, y el foco se apaga. Por eso, "
             "cualquiera de los dos interruptores que muevas, siempre cambia el estado del foco.",
    "identificar": "¿Y si el interruptor no tiene el tornillo oscuro, o está tan sucio que no se distingue? Usa el multímetro en continuidad. El común es el único terminal que tiene continuidad con uno de los otros dos en una posición de la palanca, y con el otro en la posición contraria. Los dos viajeros nunca tienen continuidad entre sí.",
    "regla": "Y una regla importante del Nec dos mil veinte: los interruptores de tres vías solo deben conmutar la fase, "
             "nunca el neutro. Y cuando el cableado va en tubería metálica, todos los conductores del circuito, incluido "
             "el neutro, viajan por la misma tubería.",
    "seguridad": "Antes de tocar un solo cable: baja el breaker del circuito, y verifica con un probador que no haya tensión. Nunca supongas que algo está apagado. Compruébalo siempre.",
    "materiales": "Para armarlo necesitas: un breaker de un polo de quince amperios, tubo EMT de media pulgada con sus "
                  "conectores y abrazaderas, dos cajas rectangulares para los interruptores, una caja octagonal para el "
                  "foco, dos interruptores de tres vías, un portalámparas con foco LED, conectores de empalme, y cable "
                  "THHN calibre catorce, de varios hilos.",
    "colores": "Los colores: negro para la fase, blanco para el neutro y verde para la tierra. Para los viajeros "
               "usaremos rojo y amarillo, y para el retorno, azul. Para estos, el Nec no exige un color: solo que no "
               "sean blancos, grises ni verdes, que están reservados para el neutro y la tierra.",
    "recorrido": "Este es el recorrido. Del tablero, un tubo baja a la caja del primer interruptor, al pie de la "
                 "escalera. De ahí, otro tubo sube hasta la caja octagonal del techo, donde va el foco. Y de la caja "
                 "octagonal, un tercer tubo llega a la caja del segundo interruptor, arriba de la escalera.",
    "cableado": "Ahora jalamos los cables. Del tablero al primer interruptor van tres: negro, blanco y verde. Del primer "
                "interruptor a la caja del foco van los dos viajeros, el blanco que sigue hacia el foco, y el verde. Y de "
                "la caja del foco al segundo interruptor suben los dos viajeros, el retorno azul, y el verde.",
    "pelado": "Como usamos cable de varios hilos, hay un detalle: al pelarlo, tuerce los hilos con los dedos para que "
              "queden juntos, y forma el gancho en el sentido de las agujas del reloj. Así, al apretar el tornillo, "
              "ningún hilo se escapa.",
    "s1": "En el primer interruptor: el negro, la fase, va al tornillo oscuro, el común. El rojo y el amarillo van a "
          "los dos tornillos de latón. El blanco no se toca aquí: sigue de paso hacia la caja del foco. Y los verdes "
          "van al tornillo verde del interruptor y a la caja metálica.",
    "caja": "En la caja del foco se hacen los empalmes: rojo con rojo y amarillo con amarillo, para que los viajeros "
            "sigan hasta el segundo interruptor. El blanco va directo a la rosca del portalámparas. El azul, el retorno, "
            "va al contacto del centro. Y todos los verdes se unen, y se conectan a la caja.",
    "s2": "En el segundo interruptor: el azul, el retorno, va al tornillo oscuro, el común. El rojo y el amarillo van "
          "a los dos tornillos de latón. Aquí no importa cuál viajero va en cuál tornillo: lo importante es no "
          "confundir el común. Y el verde, al tornillo verde.",
    "tierra": "¿Por qué tanta tierra? Porque las cajas, los tubos y el yugo de los interruptores son de metal. Si un cable pelado toca el metal, la tierra lleva esa falla de regreso al tablero, y el breaker se dispara antes de que alguien toque la caja.",
    "continuidad": "Un truco de electricista: cuando jales los cables, marca los dos viajeros con un pedacito de cinta en cada extremo. Así, en cada caja sabes de inmediato cuáles son los viajeros y cuál es el retorno, aunque los colores se parezcan con poca luz.",
    "placa": "Con todo conectado, doblamos los cables con cuidado hacia el fondo de cada caja, atornillamos los interruptores, y ponemos las placas. Revisa que ningún pedazo de cobre pelado quede fuera del tornillo: si sobra, córtalo.",
    "led": "Y en el techo, el portalámparas con un foco LED. Consume mucho menos que uno incandescente y casi no calienta. Pero la regla del portalámparas no cambia: el neutro va a la rosca, y el retorno al contacto del centro.",
    "prueba": "Antes de energizar, revisa con calma: la fase entra al común del primero, el retorno sale del común del "
              "segundo, y el neutro llega al foco sin pasar por ningún interruptor. Ahora sí: subimos el breaker.",
    "encender": "Mira el camino de la corriente. La fase llega al común del primer interruptor, toma uno de los "
                "viajeros, llega al segundo interruptor, sale por su común hacia el foco, y regresa por el neutro. "
                "Movemos el de abajo: se apaga. Movemos el de arriba: se enciende otra vez. Funciona desde los dos lados.",
    "repaso": "Repasemos todo el circuito de un vistazo. Del tablero, la fase llega al común del primer interruptor. Los dos viajeros suben a la caja del foco, y siguen hasta el segundo interruptor. Del común del segundo, el retorno regresa al centro del portalámparas. Y el neutro y la tierra acompañan todo el recorrido, sin pasar por ningún interruptor.",
    "errores": "Tres errores muy comunes. Uno: conectar la fase en un tornillo de viajero en lugar del común. El foco "
               "solo funciona en algunas posiciones, y parece que el interruptor está malo. Dos: confundir el común en "
               "el segundo interruptor; por eso siempre busca el tornillo oscuro. Y tres: usar el neutro como viajero, "
               "o conmutar el neutro. Además de que no funciona bien, el portalámparas puede quedar energizado aunque "
               "el foco esté apagado.",
    "cuatro": "¿Y si necesitas controlar el foco desde tres lugares o más? Se agregan interruptores de cuatro vías entre los dos de tres vías. Cada uno de cuatro vías cruza los viajeros. Eso lo veremos en otro video.",
    "cierre": "En resumen: la fase al común del primero, los viajeros entre los dos, el retorno del común del segundo "
              "al centro del portalámparas, y el neutro directo al foco. Si te sirvió, suscríbete en YouTube y sígueme "
              "en Facebook, y compártelo con alguien que esté aprendiendo. Nos vemos en el próximo video.",
}

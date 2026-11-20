"""
E02 · CIRCUITO SIMPLE CON LÁMPARA, del tablero al foco (horizontal 1920x1080, YouTube).
Referencias (NEC = NFPA 70):
 200.6 neutro blanco/gris · 250.119 tierra verde o desnuda · IEC 60445 neutro azul
 240.4(D) 14 AWG Cu → máx. 15 A · 250.24 puente de unión principal solo en la acometida
 358.30 EMT: fijar a ≤ 3 ft (900 mm) de cada caja y cada ≤ 10 ft (3 m) · 300.14 ≥ 6 in (150 mm) de cable libre
 110.14(D) (2017) torque con herramienta calibrada · 110.14(B) empalmes con dispositivos identificados
 314.16 relleno de cajas: 14 AWG = 2.00 in³; caja octagonal 4 × 1½ = 15.5 in³
 410.90 neutro a la rosca del portalámparas · 404.2(B) el interruptor no desconecta el neutro
 250.4(A)(5) camino efectivo de falla a tierra · NFPA 70E verificar ausencia de tensión
"""
GUION = {
    "intro": "Hola, soy Miguel Esquit, electricista. Encender un foco parece lo más simple del mundo: subes el interruptor, y listo. Pero detrás de ese clic "
             "hay reglas que te pueden salvar la vida. Hoy vamos a armar un circuito completo, desde el tablero hasta "
             "la lámpara, con tubería, cajas y conexiones reales. Y al final vas a entender por qué el interruptor "
             "siempre corta la fase, y por qué el neutro va directo a la lámpara.",
    "plano": "Este es el recorrido. Del centro de carga sale un tubo hasta una caja octagonal en el techo, donde va "
             "la lámpara. De esa caja, otro tubo baja hasta una caja rectangular en la pared, donde va el interruptor. "
             "Vamos a seguir el Código Eléctrico Nacional de Estados Unidos, el Nec, edición dos mil veinte, también conocido "
             "como N F P A setenta.",
    "materiales": "Esto es lo que necesitas: un interruptor termomagnético de un polo y quince amperios. Tubo metálico "
                  "EMT de media pulgada, con sus conectores y abrazaderas. Una caja octagonal de cuatro pulgadas, una "
                  "caja rectangular de dos por cuatro, un interruptor sencillo, un portalámparas de porcelana, y cable "
                  "THHN calibre catorce, en cuatro colores.",
    "colores": "Y los colores no son decoración. Según el Nec, el neutro debe ser blanco o gris. La tierra de los "
               "equipos, verde, o desnuda. La fase puede ser de cualquier otro color; aquí usamos negro. Y el cable que "
               "regresa del interruptor a la lámpara, que llamamos retorno, lo haremos rojo. Ojo: en las normas "
               "internacionales I E C, el neutro es azul. Por eso, siempre averigua con qué norma estás trabajando.",
    "seguridad": "Antes de tocar nada: se apaga el interruptor principal, y se verifica con un probador que no haya "
                 "tensión. Nunca supongas que algo está apagado. Compruébalo.",
    "tablero": "Ahora, el tablero por dentro. Estas dos barras están energizadas: ahí se montan los interruptores "
               "termomagnéticos. Esta es la barra de neutros, y esta, la barra de tierra. En el tablero principal, y "
               "solo ahí, el neutro y la tierra se unen con un puente de unión. En cualquier otro tablero, van separados.",
    "breaker": "¿Y por qué quince amperios? Porque el Nec dice que el cable calibre catorce de cobre no puede "
               "protegerse con más de quince amperios. El breaker no protege al foco: protege al cable. Si lo cambias "
               "por uno más grande, el cable puede sobrecalentarse antes de que el breaker se dispare.",
    "tubo": "Siguiente paso: la tubería. El tubo EMT se une a cada caja con un conector y su contratuerca. Y el Nec pide "
            "fijarlo con abrazaderas a no más de noventa centímetros de cada caja, y después, como máximo, cada tres "
            "metros.",
    "cableado": "Con la tubería lista, se jalan los cables con una guía. Del tablero a la caja octagonal van tres: "
                "negro, blanco y verde. De la caja octagonal al interruptor, otros tres: el negro que baja, el rojo que "
                "regresa, y el verde. Y en cada caja se dejan por lo menos quince centímetros de cable libre, para poder "
                "trabajar.",
    "conex": "En el tablero, el negro va al breaker, el blanco a la barra de neutros, y el verde a la barra de tierra. "
             "Y aquí viene algo que muchos ignoran: cada tornillo tiene un torque indicado por el fabricante. Y el "
             "Nec pide usar un medio aprobado para lograr ese valor, como un torquímetro o un desarmador de torque. Un "
             "tornillo flojo se calienta, y uno demasiado apretado daña el cable.",
    "caja": "En la caja octagonal se hacen los empalmes. El negro que viene del tablero se une con el negro que baja al "
            "interruptor. El blanco va directo a la lámpara. El rojo que regresa del interruptor, también va a la "
            "lámpara. Y todos los verdes se unen, y se conectan a la caja metálica con su tornillo de tierra.",
    "tierra": "¿Y para qué el verde, si la lámpara funciona sin él? La tierra no está ahí para que funcione: está para "
              "protegerte. Si la fase se pela y toca la caja metálica, el verde le da a esa falla un camino de muy baja "
              "resistencia de regreso al tablero. La corriente se dispara, y el breaker abre el circuito.",
    "relleno": "¿Y caben tantos cables en una caja tan pequeña? El Nec tiene una cuenta para eso. Cada cable calibre "
               "catorce ocupa dos pulgadas cúbicas. Aquí entran cuatro conductores, y hasta cuatro verdes cuentan como "
               "uno solo: diez pulgadas cúbicas. Y aunque contáramos el portalámparas como dispositivo, llegaríamos a "
               "catorce. La caja octagonal de cuatro pulgadas tiene quince punto cinco. Sí cabe.",
    "interruptor": "En la caja del interruptor: el negro va a uno de los tornillos de latón, el rojo al otro, y el verde "
                   "al tornillo verde. Un truco de electricista: el cable se dobla en forma de gancho y se coloca en el "
                   "sentido de las agujas del reloj. Así, al apretar, el tornillo lo jala hacia adentro en lugar de "
                   "empujarlo hacia afuera.",
    "neutro_sw": "Un dato de electricista: el Nec dos mil veinte pide llevar también el neutro a la caja del "
                 "interruptor, en baños, pasillos y habitaciones, porque los interruptores inteligentes lo necesitan para "
                 "funcionar. Pero hay excepciones. Una de ellas es nuestro caso: si los cables llegan por tubería con espacio "
                 "suficiente, el neutro se puede agregar después.",
    "lampara": "Y llegamos a la lámpara. El portalámparas tiene dos partes metálicas: el contacto del centro, al fondo, "
               "y la rosca, que es la parte que puedes tocar al cambiar un foco. El Nec es clarísimo: el neutro, el "
               "blanco, va conectado a la rosca. Y el rojo, el que viene del interruptor, va al contacto del centro.",
    "rosca": "¿Por qué? Porque la rosca es lo más fácil de tocar. Si estuviera conectada a la fase, al cambiar el foco "
             "podrías tocar ciento veinte voltios con los dedos. Conectada al neutro, queda prácticamente a cero voltios.",
    "regla": "Y la regla de oro: el interruptor corta la fase, nunca el neutro. Mira la diferencia. Si cortas la fase, "
             "al apagar, la lámpara se queda sin tensión. Pero si cortaras el neutro, el foco se apaga igual, y sin "
             "embargo el portalámparas sigue con ciento veinte voltios, esperando a que alguien lo toque. Por eso el "
             "Nec prohíbe que un interruptor desconecte el conductor neutro.",
    "pruebas": "Antes de dar energía, un buen electricista prueba. Con los cables todavía sueltos en el tablero, pon el "
               "multímetro en continuidad. Sin foco, entre el negro y el blanco no debe sonar; si suena, hay un corto. "
               "Entre el negro y el verde, tampoco; si suena, hay una falla a tierra. Ahora enrosca el foco y sube el "
               "interruptor: entre el negro y el blanco debe marcar una resistencia baja, la del filamento. Bajas el "
               "interruptor, y vuelve a abrirse. Así sabes que todo está bien, antes de energizar.",
    "encender": "Todo conectado. Ponemos las tapas, subimos el principal y el breaker, y subimos el interruptor. Mira el "
                "camino de la corriente: sale por la fase del tablero, pasa por el breaker, baja al interruptor, "
                "regresa por el rojo, atraviesa el foco, y vuelve por el neutro blanco hasta la barra de neutros.",
    "errores": "Tres errores que se ven muchísimo. Uno: poner el interruptor en el neutro. La lámpara se apaga, pero el "
               "portalámparas sigue energizado. Dos: cambiar el breaker por uno más grande porque se dispara. El "
               "problema no se arregla, solo se esconde, y el cable se calienta. Y tres: empalmar solo torciendo los "
               "cables y poniendo cinta. El Nec pide usar dispositivos de empalme identificados para ese uso, como los "
               "conectores de resorte, o soldar el empalme.",
    "cierre": "En resumen: neutro blanco a la rosca, el interruptor corta la fase, breaker de quince amperios para "
              "calibre catorce, y tierra en todas las partes metálicas. Si te sirvió, guarda este video, compártelo con "
              "alguien que esté aprendiendo, y suscríbete. Y recuerda: si no estás calificado, llama a un electricista. Soy Miguel Esquit, y nos vemos en el próximo video.",
}

if __name__ == "__main__":
    from comun_e import audio, DIR, SUFIJO_VOZ
    tot = 0
    for k, t in GUION.items():
        w, d = audio(DIR / f"voz_e02_{SUFIJO_VOZ}", k, t)
        tot += d
        print(k, round(d, 1))
    print("total", round(tot, 1), "s ·", sum(len(t) for t in GUION.values()), "caracteres")

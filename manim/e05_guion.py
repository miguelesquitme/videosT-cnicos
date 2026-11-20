"""
E05 · LEY DE OHM CON COSAS DE TU CASA (horizontal).
Verificado:
 - Georg Simon Ohm publicó su ley en 1827 ("Die galvanische Kette, mathematisch bearbeitet").
 - Potencia P = V·I; aritmética comprobada en Python (ver comprobaciones al final).
 - NEC 2020 Capítulo 9, Tabla 8: cobre 12 AWG de 7 hilos sin recubrimiento = 6.50 ohm/km a 75 °C.
 - Las potencias de los aparatos son ejemplos ("revisa la etiqueta"), no datos de un modelo real.
"""
GUION = {
    "intro": "¿Por qué se dispara el breaker cuando conectas el hervidor y la "
             "plancha al mismo tiempo? ¿Por qué un foco LED gasta tan poquito? ¿Y por qué un cable largo se calienta? "
             "Todas las respuestas salen de una de las fórmulas más famosas de la electricidad: la ley de Ohm. Y hoy "
             "la vas a entender con cosas de tu casa.",
    "agua": "Imagina la electricidad como agua en una tubería. El voltaje es la presión que empuja el agua. La corriente "
            "es la cantidad de agua que pasa cada segundo. Y la resistencia es qué tan angosta es la tubería: mientras "
            "más angosta, más le cuesta pasar al agua.",
    "unidades": "Cada una tiene su unidad. El voltaje se mide en voltios, con la letra V. La corriente, en amperios, con "
                "la letra A. Y la resistencia, en ohmios, con la letra griega omega. En tu casa, el voltaje del "
                "tomacorriente es de unos ciento veinte voltios.",
    "ley": "En mil ochocientos veintisiete, el físico alemán Georg Simon Ohm publicó la relación entre estas tres "
           "magnitudes: el voltaje es igual a la corriente por la resistencia. V igual a I por R. Así de simple.",
    "triangulo": "Hay un truco para no olvidarla: el triángulo. Arriba va la V, y abajo la I y la R. Tapas la que "
                 "quieres encontrar, y lo que queda te dice la operación. ¿Quieres la corriente? Voltaje entre "
                 "resistencia. ¿Quieres la resistencia? Voltaje entre corriente. ¿Quieres el voltaje? Corriente por "
                 "resistencia.",
    "alterna": "Una aclaración honesta: en tu casa la corriente es alterna. Para aparatos que básicamente calientan, como un hervidor, una plancha o una ducha, la ley de Ohm funciona muy bien. En motores y equipos electrónicos el cálculo es más complejo, pero la idea es la misma.",
    "potencia": "Pero en las etiquetas de los aparatos casi nunca ves ohmios: ves vatios. Los vatios son la potencia, y "
                "tienen su propia fórmula, que trabaja junto con la de Ohm: la potencia es igual al voltaje por la "
                "corriente. P igual a V por I.",
    "led": "Primer ejemplo: un foco LED que dice nueve vatios. Si lo conectas a ciento veinte voltios, la corriente es "
           "nueve entre ciento veinte: cero punto cero setenta y cinco amperios. Apenas setenta y cinco miliamperios. "
           "Por eso puedes tener muchísimos focos LED en un mismo circuito.",
    "hervidor": "Segundo ejemplo: un hervidor de agua que en su etiqueta dice mil quinientos vatios. Mil quinientos "
                "entre ciento veinte: doce punto cinco amperios. Y si quieres su resistencia, aplicas Ohm: ciento "
                "veinte entre doce punto cinco, son nueve punto seis ohmios mientras está funcionando.",
    "plancha": "Tercer ejemplo: una plancha de mil doscientos vatios. Mil doscientos entre ciento veinte: diez amperios.",
    "comparacion": "Compáralo con un foco incandescente de sesenta vatios, de los de antes: sesenta entre ciento veinte, medio amperio. Casi siete veces más corriente que el LED de nueve vatios, que da una luz parecida. Por eso cambiar a LED se nota en el recibo.",
    "paralelo": "Ahora, la clave: en tu casa, los aparatos se conectan en paralelo. Cada uno recibe los mismos ciento "
                "veinte voltios, pero sus corrientes se suman en el cable y en el breaker. Si el hervidor y la plancha "
                "están en el mismo circuito, la corriente total es doce punto cinco más diez: veintidós punto cinco "
                "amperios.",
    "breaker": "Y si ese circuito tiene un breaker de veinte amperios, la corriente se pasa del límite, y el breaker se "
               "dispara. No está malo: está haciendo su trabajo, protegiendo al cable de calentarse de más. La solución "
               "no es poner un breaker más grande, sino repartir los aparatos en distintos circuitos.",
    "regleta": "Lo mismo pasa con las regletas y extensiones. Muchas son de quince amperios. Si conectas ahí el hervidor y la plancha, son veintidós punto cinco amperios en una regleta de quince. Se calienta, y es un riesgo de incendio. Siempre suma las corrientes antes de conectar.",
    "serie": "¿Y en serie? Cuando los aparatos van uno detrás de otro, por todos pasa la misma corriente, pero el voltaje se reparte. Por eso, en algunas series de luces navideñas antiguas, si un foquito se fundía, se apagaba toda la serie: se abría el único camino.",
    "microondas": "Otro ejemplo: un microondas que en su etiqueta dice que consume mil doscientos vatios. Mil doscientos entre ciento veinte: diez amperios. Igual que la plancha. Por eso en las cocinas suelen haber varios circuitos.",
    "focos": "Y una comparación curiosa: ¿cuántos focos LED de nueve vatios consumen lo mismo que esa plancha de diez amperios? Diez entre cero punto cero setenta y cinco: unos ciento treinta y tres focos.",
    "cable": "Y aquí viene algo que pocos saben: el cable también tiene resistencia. Según la tabla ocho del Nec, el cable "
             "de cobre calibre doce, de siete hilos, tiene seis punto cinco ohmios por kilómetro. Parece poco, pero "
             "suma.",
    "caida": "Imagina un tomacorriente a veinticinco metros del tablero. La corriente va y regresa, así que recorre "
             "cincuenta metros de cable. Eso da cero punto tres dos cinco ohmios. Si pasan quince amperios, por Ohm, "
             "en el cable se pierden casi cinco voltios. El aparato ya no recibe ciento veinte, sino unos ciento "
             "quince.",
    "calor": "Y esa energía no desaparece: se convierte en calor dentro del cable. Por eso, cuando un circuito es muy "
             "largo o lleva mucha corriente, se usa un cable más grueso: menos resistencia, menos pérdida, y menos "
             "calor.",
    "joule": "Y ese calor también se calcula. La potencia que se pierde en el cable es la corriente al cuadrado por la resistencia. Quince al cuadrado son doscientos veinticinco, por cero punto tres dos cinco ohmios: unos setenta y tres vatios de calor, repartidos a lo largo del cable. Como tener un foco viejo encendido, escondido en la pared.",
    "medir": "Todo esto lo puedes comprobar con un multímetro. En voltaje, mides los ciento veinte del tomacorriente. "
             "Con un amperímetro de gancho, abrazas un solo cable y mides la corriente del aparato. Y con el aparato "
             "desconectado, puedes medir resistencias. Ojo: la resistencia de un aparato apagado y frío no es la misma "
             "que cuando está funcionando.",
    "energia": "¿Y lo que te cobran en el recibo? No son vatios, son kilovatios hora: la potencia por el tiempo que la usas. Un hervidor de mil quinientos vatios encendido diez minutos usa un cuarto de kilovatio hora. Un foco LED de nueve vatios, encendido cinco horas diarias durante un mes, usa uno punto tres cinco kilovatios hora.",
    "seguridad": "Y un consejo de seguridad: nunca midas resistencia con el circuito energizado. Para medir ohmios, el aparato debe estar desconectado. Si mides en un circuito con voltaje, puedes dañar el multímetro, o lastimarte.",
    "reto": "Un reto para ti. Un ventilador que dice sesenta vatios, a ciento veinte voltios, ¿cuánta corriente "
            "consume? Te doy unos segundos. La respuesta: sesenta entre ciento veinte, medio amperio.",
    "ejercicio": "Último ejercicio. En un circuito de veinte amperios conectas una cafetera de novecientos vatios y una tostadora de ochocientos. ¿Se dispara el breaker? Novecientos entre ciento veinte son siete punto cinco amperios. Ochocientos entre ciento veinte, unos seis punto siete. En total, unos catorce punto dos amperios. Menos de veinte: el breaker aguanta.",
    "repaso": "Repasemos. El voltaje empuja, la corriente fluye, y la resistencia se opone. Corriente es igual a voltaje entre resistencia. Potencia es igual a voltaje por corriente. En paralelo, las corrientes se suman. Y en el cable, la resistencia se convierte en calor y en caída de voltaje.",
    "cierre": "En resumen: V igual a I por R, y P igual a V por I. Con esas dos fórmulas entiendes por qué se dispara un "
              "breaker, por qué el LED ahorra, y por qué los cables largos se calientan. Si te sirvió, suscríbete en "
              "YouTube y sígueme en Facebook. Nos vemos en el próximo video.",
}

if __name__ == "__main__":
    # comprobaciones de aritmética
    assert abs(9 / 120 - 0.075) < 1e-9
    assert abs(1500 / 120 - 12.5) < 1e-9 and abs(120 / 12.5 - 9.6) < 1e-9
    assert abs(1200 / 120 - 10) < 1e-9 and abs(12.5 + 10 - 22.5) < 1e-9
    r = 6.50 * 0.050
    assert abs(r - 0.325) < 1e-9 and abs(15 * r - 4.875) < 1e-9 and abs(60 / 120 - 0.5) < 1e-9
    print("aritmética OK", r, 15 * r, 120 - 15 * r)

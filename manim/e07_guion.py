"""E07 · H21 · ¿CÓMO FUNCIONA EL DISYUNTOR? · Selecciona el breaker correcto — horizontal, ~6 min.
Misma línea visual que e06b (portadillas, cinta, criterios, tablas de ejemplo), aparatos en 2D de frente, sin marcas.

Fuentes verificadas (9-nov-2026):
- IEC 60050 (IEV 441-14-20) interruptor automático: aparato mecánico de conexión capaz de establecer, soportar e
  interrumpir corrientes en condiciones normales y también establecer, soportar durante un tiempo especificado e
  interrumpir corrientes en condiciones anormales especificadas, como las de cortocircuito.
- IEC 60898-1 (vía ficha técnica ETI ETIMAT): disparo instantáneo B 3–5 In, C 5–10 In, D 10–20 In (t < 0,1 s);
  corriente convencional de no disparo 1,13 In (≥ 1 h) y de disparo 1,45 In (< 1 h); temperatura de referencia 30 °C;
  poder de corte asignado (p. ej. 6 kA, 10 kA), marcado en un rectángulo sin unidad ("6000").
- NEC 2020 (PDF del usuario): 110.9 (poder de interrupción ≥ corriente de falla disponible en los bornes);
  240.4 y 240.4(D) (12 AWG → 20 A, 10 AWG → 30 A); 240.4(G) y Tabla 240.4(G) (circuitos de motores: Art. 430);
  Tabla 240.6(A) (15, 20, 25, 30, 35, 40 A…); 422.13 (calentador de agua de almacenamiento ≤ 450 L: dispositivo y
  conductores ≥ 125 % de su potencia nominal); Tabla 430.250 (5 hp, 230 V, 3~ = 15,2 A); Tabla 430.52 (interruptor de
  tiempo inverso: 250 % de la corriente a plena carga); 430.52(C)(1) Excepción 1 (si no coincide con un valor
  normalizado, se permite el valor normalizado inmediato superior); Tabla 310.16 (12 AWG 25 A a 75 °C).
- Cálculos (Python): 4500/240 = 18,75 A; × 1,25 = 23,44 A → 25 A. 15,2 × 2,5 = 38 A → 40 A. 15,2 × 1,25 = 19 A.
"""

GUION = {
    "gancho": "Un breaker puede dejar pasar un poco más de su corriente durante más de una hora sin dispararse. Pero ante un "
              "cortocircuito de miles de amperios se abre en menos de una décima de segundo. ¿Cómo sabe la diferencia? En "
              "este video vas a ver cómo funciona el disyuntor por dentro y cómo seleccionar el correcto, con seis criterios "
              "y dos ejemplos reales.",
    # 1 · qué es
    "q_def": "Disyuntor, interruptor automático o breaker: es el mismo aparato. La norma I E C sesenta mil cincuenta lo "
             "define como un aparato mecánico de conexión capaz de establecer, soportar e interrumpir corrientes en "
             "condiciones normales, y también de interrumpir corrientes anormales, como las de cortocircuito.",
    "q_dif": "Ahí está la diferencia con el contactor del video anterior: el contactor solo maniobra en condiciones "
             "normales. Y a diferencia de un fusible, que se funde y hay que cambiarlo, el disyuntor se vuelve a cerrar con "
             "su palanca. Su trabajo principal es proteger al conductor.",
    # 2 · partes
    "p_intro": "Vamos a abrirlo. Estas son sus partes, y cada una tiene una función.",
    "p_palanca": "Arriba, la palanca y el mecanismo de disparo: una cerradura con resortes que mantiene cerrados los "
                 "contactos. Cuando algo la libera, los resortes los abren de golpe, aunque alguien esté sosteniendo la "
                 "palanca.",
    "p_contactos": "Los contactos: uno fijo y uno móvil, con pastillas de aleación de plata. Junto a ellos, la cámara "
                   "apagachispas, con plaquetas metálicas que dividen y enfrían el arco.",
    "p_termico": "El disparador térmico es una lámina bimetálica: dos metales soldados que se dilatan distinto con el "
                 "calor. La corriente la calienta y, si es demasiada, se curva y empuja la barra de disparo.",
    "p_magnetico": "El disparador magnético es una bobina con un émbolo. Con un cortocircuito, el campo es tan fuerte que "
                   "el émbolo golpea el mecanismo en milisegundos.",
    "p_simbolo": "En los esquemas, según la I E C sesenta y seis diecisiete, se dibuja como un contacto con una cruz, y con "
                 "sus disparadores de sobrecarga y de cortocircuito. Su identificación es Q.",
    # 3 · funcionamiento
    "f_sobrecarga": "Veamos una sobrecarga. Con un poco más de corriente de la nominal, el bimetal se calienta despacio. "
                    "Tarda minutos, o hasta una hora, en curvarse lo suficiente. Con más corriente, se calienta más rápido. "
                    "Por eso se llama protección de tiempo inverso: a más corriente, menos tiempo.",
    "f_corto": "Ahora un cortocircuito. La corriente sube a cientos o miles de amperios. La bobina dispara el émbolo, los "
               "contactos se separan, el arco salta a la cámara apagachispas y se apaga. Todo en menos de una décima de "
               "segundo.",
    "f_curva": "Todo esto se resume en la curva de disparo. Según la norma I E C sesenta mil ochocientos noventa y ocho, con "
               "uno punto trece veces su corriente nominal no debe disparar en una hora, y con uno punto cuarenta y cinco "
               "veces debe disparar antes de una hora. La parte magnética depende de la curva: la B dispara entre tres y "
               "cinco veces la nominal; la C, entre cinco y diez; y la D, entre diez y veinte.",
    # 4 · críticos
    "c_cable": "Primer punto crítico: el breaker protege al cable, no al aparato. Su corriente nunca debe ser mayor que la "
               "que soporta el conductor. Por eso el Nec limita el calibre doce a veinte amperios.",
    "c_poder": "Segundo: el poder de corte. Es la máxima corriente de cortocircuito que puede interrumpir sin destruirse. "
               "En los breakers I E C viene en un rectángulo, por ejemplo seis mil, o sea, seis kiloamperios. El Nec, en el "
               "artículo ciento diez punto nueve, exige que sea igual o mayor que la corriente de falla disponible.",
    "c_temp": "Y tercero: el bimetal siente el calor del ambiente. La curva está hecha a treinta grados. En un tablero muy "
              "caliente, dispara antes; por eso hay que ventilarlo y no amontonar breakers sin espacio.",
    # 5 · selección
    "s_intro": "Para seleccionar un disyuntor revisamos seis criterios.",
    "s1": "Criterio uno: la tensión y el tipo de corriente. La tensión nominal del breaker debe ser igual o mayor que la del "
          "circuito, y debe estar hecho para corriente alterna o continua, según el caso.",
    "s2": "Criterio dos: la corriente nominal. Debe ser igual o mayor que la corriente de la carga, pero igual o menor que la "
          "corriente que soporta el conductor.",
    "s3": "Criterio tres: el número de polos. Un polo para ciento veinte voltios, dos polos para doscientos cuarenta, y tres "
          "polos para un circuito trifásico.",
    "s4": "Criterio cuatro: la curva de disparo. La B, para cargas sin corriente de arranque y cables largos; la C, para el "
          "uso general, alumbrado y tomacorrientes; y la D, para motores y transformadores con arranques fuertes.",
    "s5": "Criterio cinco: el poder de corte, igual o mayor que la corriente de cortocircuito disponible en ese tablero.",
    "s6": "Criterio seis: el tipo de carga. Si es un motor, el Nec permite un breaker más grande, porque la sobrecarga la "
          "cuida el relé térmico, y el breaker solo protege contra cortocircuito.",
    # 6 · ejemplo 1
    "e1_datos": "Ejemplo uno: un calentador de agua de almacenamiento de cuatro mil quinientos vatios a doscientos cuarenta "
                "voltios.",
    "e1_pasos": "Criterio uno: doscientos cuarenta voltios alternos. Criterio dos: la corriente es cuatro mil quinientos "
                "entre doscientos cuarenta, dieciocho punto setenta y cinco amperios. El Nec, en el artículo cuatrocientos "
                "veintidós punto trece, pide el ciento veinticinco por ciento: veintitrés punto cuatro amperios. El valor "
                "normalizado siguiente es veinticinco amperios, con cable calibre diez.",
    "e1_resto": "Criterio tres: dos polos. Criterio cuatro: es una resistencia, sin arranque: curva C. Criterio cinco: "
                "poder de corte igual o mayor que la falla disponible, por ejemplo diez kiloamperios. Criterio seis: carga "
                "resistiva. Resultado: breaker de dos polos, veinticinco amperios.",
    # 7 · ejemplo 2
    "e2_datos": "Ejemplo dos: la bomba del video del contactor. Motor trifásico de jaula de cinco caballos, a doscientos "
                "treinta voltios.",
    "e2_pasos": "Criterio uno: doscientos treinta voltios alternos. Criterio dos: según la tabla cuatrocientos treinta "
                "punto doscientos cincuenta, su corriente a plena carga es de quince punto dos amperios. Criterio tres: "
                "tres polos. Criterio cuatro: es un motor con corriente de arranque alta: curva D.",
    "e2_resto": "Criterio cinco: poder de corte según el tablero. Y criterio seis, el clave: es un motor. La tabla "
                "cuatrocientos treinta punto cincuenta y dos permite hasta el doscientos cincuenta por ciento: treinta y "
                "ocho amperios. Como no es un valor normalizado, se permite el siguiente: cuarenta amperios. Ese breaker "
                "solo cuida el cortocircuito; la sobrecarga la cuida el relé térmico. Y ese es el tema del próximo video.",
    "cierre": "Ahora ya sabes cómo funciona un disyuntor y cómo seleccionarlo. Si te sirvió, suscríbete y sígueme. Nos vemos "
              "en el próximo video.",
}

SECCIONES = {
    "q_def": ("1", "¿QUÉ ES UN DISYUNTOR?"),
    "p_intro": ("2", "PARTES DEL DISYUNTOR"),
    "f_sobrecarga": ("3", "¿CÓMO FUNCIONA?"),
    "c_cable": ("4", "ASPECTOS CRÍTICOS"),
    "s_intro": ("5", "SELECCIONA EL DISYUNTOR"),
    "e1_datos": ("6", "EJEMPLO 1 · CALENTADOR DE AGUA"),
    "e2_datos": ("7", "EJEMPLO 2 · MOTOR DE 5 hp"),
}

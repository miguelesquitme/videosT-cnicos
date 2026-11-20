"""E08 · H22 · ¿CÓMO FUNCIONA EL RELÉ TÉRMICO? · Selecciona y ajusta el relé correcto — horizontal, ~6 min.

Fuentes verificadas (9-nov-2026):
- IEC 60947-4-1, clases de disparo (catálogo ABB, tabla según la norma): a 7,2 × Ir en frío: clase 10A 2–10 s,
  clase 10 4–10 s, clase 20 6–20 s, clase 30 9–30 s; a 1,05 × Ir no dispara; el relé de sobrecarga actúa por
  sobrecarga y también por pérdida de fase.
- Schneider TeSys LRD (catálogo): relés compensados, clase 10A, compensación −20…+60 °C, rearme manual o automático
  (sale de fábrica en manual, bajo tapa), botón Stop actúa el NC, Test actúa NC y NA. Rangos: LRD14 7–10 A,
  LRD16 9–13 A (D12–D38), LRD21 12–18 A (D18–D38), LRD22 16–24 A. LRD14L: 7–10 A, clase 20, para D09–D38.
- ABB TF42 (ficha): clase 10, compensación −25…+60 °C, 95-96 NC (disparo), 97-98 NA (señal), rearme manual o
  automático, sensible a pérdida de fase, TEST y STOP. Rangos: TF42-13 10–13 A, TF42-16 13–16 A, TF42-10 7,6–10 A.
  ABB EF19-18.9: relé electrónico, 5,7–18,9 A, clase seleccionable (10E, 20E…).
- NEC 2020: 430.6(A)(2) (la protección de sobrecarga se basa en la corriente de PLACA del motor); 430.32(A)(1)
  (relé de sobrecarga: máximo 125 % de la corriente de placa si FS ≥ 1,15 o calentamiento ≤ 40 °C; 115 % los demás).
- Motor ejemplo 1: Hyosung 5 hp, 4 polos, 230/460 V, 60 Hz: 13,1 A a 230 V; FS 1,25; rotor bloqueado 660 %.
- Motor ejemplo 2: WEG W22 00718ET3E213T, 7,5 hp, 230/460 V: 9,18 A a 460 V; FS 1,25; rotor bloqueado 7,1×.
- Cálculos: 13,1 × 1,25 = 16,4 A; 9,18 × 1,25 = 11,5 A.
"""

GUION = {
    "gancho": "El breaker de cuarenta amperios del video anterior protege a la bomba contra un cortocircuito. Pero si la bomba "
              "se atasca y el motor pide dieciocho amperios en lugar de trece, ese breaker ni se entera, y el motor se "
              "quema poco a poco. ¿Quién lo protege? El relé térmico. Vamos a ver cómo funciona y cómo seleccionarlo y "
              "ajustarlo, con seis criterios y dos ejemplos reales.",
    # 1 · qué es
    "q_def": "El relé térmico es un relé de protección contra sobrecarga para motores, normado en la I E C sesenta mil "
             "novecientos cuarenta y siete, parte cuatro uno. Una sobrecarga es una corriente un poco mayor que la "
             "nominal, que dura mucho tiempo: un rodamiento dañado, una bomba atascada o una fase que se pierde.",
    "q_como": "Un detalle importante: el relé térmico no corta la corriente del motor. Se monta debajo del contactor, y "
              "cuando detecta la sobrecarga abre su contacto noventa y cinco noventa y seis, que está en serie con la "
              "bobina. Quien abre el circuito de potencia es el contactor.",
    # 2 · partes
    "p_frente": "Por fuera tiene tres pines de cobre que entran en los bornes de salida del contactor, y abajo sus bornes "
                "dos, cuatro y seis, hacia el motor. Al frente, el dial para ajustar la corriente, el botón azul de rearme, "
                "el botón rojo de paro, el de prueba y la ventana que indica si disparó.",
    "p_contactos": "Tiene dos contactos auxiliares: el noventa y cinco noventa y seis, normalmente cerrado, que va en serie "
                   "con la bobina del contactor; y el noventa y siete noventa y ocho, normalmente abierto, para una luz o una "
                   "señal de falla.",
    "p_dentro": "Por dentro, cada fase pasa por un calefactor enrollado sobre una lámina bimetálica. Las tres láminas empujan "
                "una regleta doble, llamada diferencial, y un cuarto bimetal compensa la temperatura del ambiente.",
    "p_simbolo": "En los esquemas se dibujan por separado: el elemento térmico, en el circuito de potencia, y su contacto "
                 "noventa y cinco noventa y seis, en el de mando. Ambos llevan la misma identificación: F.",
    # 3 · funcionamiento
    "f_disparo": "Con la corriente nominal, los bimetales se calientan, pero no lo suficiente. Con una sobrecarga se curvan "
                 "más, empujan la regleta, el mecanismo dispara, se abre el noventa y cinco noventa y seis, la bobina se "
                 "queda sin tensión y el contactor detiene el motor.",
    "f_fase": "Si se pierde una fase, el motor sigue girando con dos y por ellas circula más corriente. Un bimetal se queda "
              "frío mientras los otros dos se curvan: la regleta diferencial detecta esa diferencia y dispara antes.",
    "f_clase": "¿Y cuánto tarda? Lo define la clase de disparo. Con siete punto dos veces la corriente ajustada, como al "
               "arrancar, la clase diez dispara entre cuatro y diez segundos; la veinte, entre seis y veinte; y la treinta, "
               "entre nueve y treinta. A uno punto cero cinco veces, no debe disparar.",
    # 4 · críticos
    "c_corto": "Primer punto crítico: el relé térmico no protege contra cortocircuito. Un bimetal tarda segundos y un "
               "cortocircuito destruye todo en milisegundos. Siempre va con un breaker o fusibles antes.",
    "c_placa": "Segundo: se ajusta con la corriente de la placa del motor, no con la de la tabla, como pide el artículo "
               "cuatrocientos treinta punto seis del Nec. Y según el cuatrocientos treinta punto treinta y dos, nunca más del "
               "ciento veinticinco por ciento, si el factor de servicio es uno punto quince o mayor.",
    "c_rearme": "Y tercero: el rearme. En automático, el motor puede arrancar solo al enfriarse el relé. Si eso es "
                "peligroso para alguien, usa el rearme manual, y antes de rearmar busca la causa.",
    # 5 · selección
    "s_intro": "Para seleccionar un relé térmico revisamos seis criterios.",
    "s1": "Criterio uno: el rango de ajuste. La corriente de placa del motor debe quedar dentro del rango, de preferencia "
          "hacia el centro, no en un extremo.",
    "s2": "Criterio dos: la clase de disparo. Clase diez para arranques normales, de pocos segundos. Clase veinte o treinta "
          "para cargas pesadas que tardan en acelerar, como ventiladores grandes, molinos o centrífugas.",
    "s3": "Criterio tres: que se monte en tu contactor. Cada fabricante indica con qué contactores encaja.",
    "s4": "Criterio cuatro: sensibilidad a la falta de fase y compensación de temperatura. Hoy la mayoría las trae, pero "
          "hay que confirmarlo.",
    "s5": "Criterio cinco: el rearme, manual o automático, según la seguridad de la máquina.",
    "s6": "Criterio seis: los contactos auxiliares. El noventa y cinco noventa y seis para la bobina, y el noventa y siete "
          "noventa y ocho para señalizar la falla.",
    # 6 · ejemplo 1
    "e1_datos": "Ejemplo uno: la bomba de nuestra serie. En la placa del motor dice: cinco caballos, doscientos treinta "
                "voltios, trece punto uno amperios y factor de servicio uno punto veinticinco.",
    "e1_pasos": "Criterio uno: trece punto uno amperios. Un relé de nueve a trece no alcanza. Sirve uno de doce a dieciocho, "
                "o uno de trece a dieciséis, según la marca. Se ajusta el dial en trece punto uno. El máximo permitido sería "
                "dieciséis punto cuatro.",
    "e1_resto": "Criterio dos: arranque directo normal: clase diez. Criterio tres: se monta en el contactor de dieciocho "
                "amperios. Criterio cuatro: con falta de fase y compensación. Criterio cinco: rearme manual. Y criterio "
                "seis: el noventa y cinco noventa y seis en serie con la bobina, y el noventa y siete noventa y ocho a una luz "
                "de falla.",
    # 7 · ejemplo 2
    "e2_datos": "Ejemplo dos: un ventilador grande. Su placa dice: siete punto cinco caballos, cuatrocientos sesenta "
                "voltios, nueve punto dieciocho amperios, factor de servicio uno punto veinticinco. Supongamos que por la "
                "inercia de las aspas tarda unos doce segundos en acelerar.",
    "e2_pasos": "Criterio uno: nueve punto dieciocho amperios: un relé de siete a diez amperios, ajustado en nueve punto "
                "dos. Criterio dos, el clave: un relé clase diez dispara antes de diez segundos a siete punto dos veces la "
                "corriente, y el arranque dura doce. Se dispararía en cada arranque.",
    "e2_resto": "Se necesita clase veinte: por ejemplo, un relé térmico de siete a diez amperios clase veinte, o uno "
                "electrónico con la clase seleccionable. Los demás criterios, igual que en el ejemplo uno.",
    "cierre": "Ahora ya sabes cómo funciona el relé térmico y cómo seleccionarlo y ajustarlo. Si te sirvió, suscríbete y "
              "sígueme. Nos vemos en el próximo video.",
}

SECCIONES = {
    "q_def": ("1", "¿QUÉ ES UN RELÉ TÉRMICO?"),
    "p_frente": ("2", "PARTES DEL RELÉ TÉRMICO"),
    "f_disparo": ("3", "¿CÓMO FUNCIONA?"),
    "c_corto": ("4", "ASPECTOS CRÍTICOS"),
    "s_intro": ("5", "SELECCIONA EL RELÉ TÉRMICO"),
    "e1_datos": ("6", "EJEMPLO 1 · BOMBA DE 5 hp"),
    "e2_datos": ("7", "EJEMPLO 2 · VENTILADOR DE 7,5 hp"),
}

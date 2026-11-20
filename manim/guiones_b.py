"""Guiones de los Shorts V12–V17 rehechos con el estándar nuevo (1:30–3:00, fundamento técnico, terminología correcta).
Reglas: sin presentarse, números en palabras, cierre "Si te sirvió, suscríbete y sígueme." sin nombrar plataformas.

Fuentes verificadas (1-nov-2026):
 V12  OSHA Construction eTool "Electrical Incidents" (tabla de NIOSH 1998 / Greenwald 1991, 60 Hz, mano-pie, 1 s):
      1 mA percepción; 5 mA choque leve, se puede soltar; 6–16 mA doloroso, pierde control muscular ("let-go");
      17–99 mA dolor extremo, paro respiratorio, no se puede soltar, muerte posible; 100–2000 mA fibrilación
      ventricular, muerte probable. Ejemplo OSHA: piel seca 100 000 Ω → 120 V / 100 000 Ω = 1 mA;
      piel mojada 1 000 Ω → 120 mA. LED 9 W / 120 V = 75 mA. NEC 2020 210.8 (GFCI en baños y cocinas).
 V13  NEC 2020 Cap. 9 Tabla 8: 12 AWG trenzado, cobre sin recubrir 6.50 Ω/km a 75 °C. 15 m de circuito = 30 m
      ida y vuelta → 0.195 Ω; 10 A → 19.5 W; 20 A → 78 W (P = I²R). Tabla 310.16: 12 AWG cobre 20/25/30 A
      (60/75/90 °C). Tabla 310.15(C)(1): 4–6 conductores 80 %; 7–9 70 %; 10–20 50 %.
 V14  AWG (Wikipedia, American wire gauge): el número viene de las pasadas de trefilado; 36 AWG = 0.005 in,
      0000 AWG = 0.46 in, 39 pasos (razón 92^(1/39) ≈ 1.123); área ×2 cada 3 calibres, diámetro ×2 cada 6.
      NEC Tabla 8: 14 = 2.08 mm², 12 = 3.31, 10 = 5.26, 8 = 8.37 (8.37/2.08 = 4.02). NEC 240.4(D): 14 → 15 A,
      12 → 20 A, 10 → 30 A. Por encima de 4/0 se usa kcmil (Tabla 8: 250, 300 ... kcmil).
 V15  NEC 2020 250.119 (tierra de equipos: desnudo, verde o verde con franjas amarillas; esos colores no se usan
      para otros conductores; 4 AWG y mayores se pueden identificar al instalar); 200.6 (neutro blanco o gris);
      250.4(A)(5) (camino efectivo de falla de baja impedancia que permita operar la protección).
      IEC 60445: PE verde-amarillo, N azul.
 V16  OSHA eTool Evacuation Plans, "Portable Fire Extinguishers": clases A, B, C, D, K; clase C = cableado,
      tableros, equipo eléctrico energizado; "Never use water to extinguish an electrical fire" (el agua conduce
      y puede electrocutar); CO2 para clases B y C; polvo químico ABC.
 V17  IEC 61010-1 (2.ª ed.), según FLIR "What do CAT ratings mean?": CAT II tomacorrientes y cargas enchufables;
      CAT III instalación del edificio (tableros, breakers, cableado); CAT IV origen de la instalación.
      Impulso: 600 V → CAT II 4000 V, CAT III 6000 V, CAT IV 8000 V; 1000 V → CAT II 6000 V, CAT III 8000 V.
"""

FIN = "Si te sirvió, suscríbete y sígueme."

G12 = {
    "gancho": "¿Qué es más peligroso: el voltaje o la corriente? Lo que daña tu cuerpo es la corriente que lo atraviesa. "
              "Y hace falta mucho menos de la que te imaginas.",
    "p1": "La corriente se mide en amperios, pero para el cuerpo humano la unidad que importa es el miliamperio: una "
          "milésima de amperio. Por ejemplo, una lámpara LED de nueve vatios, a ciento veinte voltios, consume unos "
          "setenta y cinco miliamperios.",
    "p2": "La agencia de seguridad laboral de Estados Unidos, Osha, publica estos efectos para un choque de sesenta "
          "hercios, de la mano al pie, durante un segundo. Con un miliamperio apenas sientes un cosquilleo. Con cinco, "
          "un choque leve, pero todavía te puedes soltar.",
    "p3": "Entre seis y dieciséis miliamperios, el choque duele y empiezas a perder el control de los músculos. "
          "La mano se queda agarrada al conductor: no te puedes soltar.",
    "p4": "Entre diecisiete y noventa y nueve, hay dolor extremo, contracciones fuertes, y la respiración se puede "
          "detener. Y desde cien miliamperios, el corazón puede entrar en fibrilación ventricular: late desordenado y "
          "deja de bombear. La muerte es probable.",
    "p5": "Fíjate: la corriente de esa lámpara LED ya está en la zona mortal. Entonces, ¿qué limita la corriente? La "
          "resistencia de tu cuerpo. Y aquí entra la ley de Ohm: corriente igual a voltaje entre resistencia.",
    "p6": "Osha lo ejemplifica así. Con la piel seca, unos cien mil ohmios: ciento veinte voltios entre cien mil da un "
          "miliamperio, apenas lo sientes. Con la piel mojada, la resistencia baja a unos mil ohmios: ciento veinte "
          "entre mil, ciento veinte miliamperios. Suficiente para la fibrilación.",
    "p7": "Por eso el agua y la electricidad son tan peligrosas, y por eso el Nec exige interruptores de falla a tierra "
          "en baños y cocinas: detectan una fuga de pocos miliamperios y cortan en una fracción de segundo.",
    "p8": "Así que no subestimes los ciento veinte voltios de tu casa. Lo que importa es cuánta corriente logra pasar por "
          "ti. Trabaja siempre sin tensión, y con las manos secas.",
    "cierre": FIN,
}

G13 = {
    "gancho": "Un cable que se calienta te está avisando algo. ¿De dónde sale ese calor, si el cobre es tan buen conductor?",
    "p1": "El cobre conduce muy bien, pero no es perfecto. El Nec, en su tabla ocho, da la resistencia de cada calibre: "
          "un cable doce de cobre tiene unos seis punto cinco ohmios por kilómetro. Es poco, pero no es cero.",
    "p2": "Cuando los electrones avanzan por el metal, chocan con los átomos y les transfieren energía. Los átomos vibran "
          "más, y esa vibración es calor. Es el efecto Joule.",
    "p3": "La fórmula es: potencia igual a corriente al cuadrado por resistencia. Lo importante es ese cuadrado. Si "
          "duplicas la corriente, el calor no se duplica: se multiplica por cuatro.",
    "p4": "Hagamos la cuenta. Un circuito de quince metros en cable doce son treinta metros de ida y vuelta: unos cero "
          "punto dos ohmios. Con diez amperios, se pierden unos veinte vatios en calor a lo largo del cable. Con veinte "
          "amperios, casi ochenta.",
    "p5": "Ese calor lo tiene que aguantar el aislamiento. Por eso el Nec, en la tabla tres diez punto dieciséis, da la "
          "corriente permitida según la temperatura del aislamiento: para el doce de cobre, veinte, veinticinco o "
          "treinta amperios, a sesenta, setenta y cinco o noventa grados.",
    "p6": "Y si metes muchos conductores en el mismo tubo, se calientan entre ellos y se enfrían peor. El Nec pide "
          "reducir: con cuatro a seis conductores que llevan corriente, al ochenta por ciento; de siete a nueve, al "
          "setenta.",
    "p7": "En casa, los puntos que más se calientan suelen ser las conexiones flojas: el área de contacto es pequeña, la "
          "resistencia sube, y ahí se concentra el calor. Por eso los tornillos se aprietan bien.",
    "p8": "Así que, si un cable o un tomacorriente está caliente, no lo ignores: hay demasiada corriente, un calibre "
          "pequeño o una mala conexión.",
    "cierre": FIN,
}

G14 = {
    "gancho": "Calibre catorce y calibre doce. El doce es más grueso. Número menor, cable más grueso. ¿No debería ser "
              "al revés?",
    "p1": "La explicación está en cómo se fabricaba el alambre. Se estiraba pasándolo por dados, agujeros cada vez más "
          "pequeños. Eso se llama trefilado. Y el número de calibre venía de cuántas pasadas llevaba: más pasadas, "
          "alambre más delgado, número más grande.",
    "p2": "Ese sistema es el calibre americano de alambres, A W G. Hoy se define con dos extremos: el treinta y seis "
          "mide cero punto cero cero cinco pulgadas, y el cuatro ceros, cero punto cuarenta y seis pulgadas. Entre los "
          "dos hay treinta y nueve pasos, y en cada paso el diámetro crece en la misma proporción.",
    "p3": "De ahí sale una regla muy útil: cada tres calibres, el área se duplica. Y cada seis calibres, el diámetro se "
          "duplica.",
    "p4": "Compruébalo con la tabla ocho del Nec. El catorce tiene dos punto cero ocho milímetros cuadrados. El doce, "
          "tres punto treinta y uno. El diez, cinco punto veintiséis. Y el ocho, ocho punto treinta y siete. Del "
          "catorce al ocho bajas seis calibres, y el área es cuatro veces mayor.",
    "p5": "Más área de cobre significa menos resistencia y menos calor. Por eso el calibre fija la protección máxima. "
          "Según el Nec, el catorce de cobre se protege con quince amperios; el doce, con veinte; y el diez, con "
          "treinta.",
    "p6": "Y cuando el cable es más grueso que el cuatro ceros, se usa otra unidad: los kcmil, miles de milésimas "
          "circulares. Ahí el número sí crece con el tamaño.",
    "p7": "Recuerda: en A W G, número menor, cable más grueso. Y nunca pongas un breaker más grande sin revisar el "
          "calibre del cable.",
    "cierre": FIN,
}

G15 = {
    "gancho": "Abres una caja y ves negro, blanco y verde. El verde no lleva corriente en condiciones normales. "
              "Entonces, ¿para qué está, y por qué tiene que ser verde?",
    "p1": "Ese conductor se llama conductor de puesta a tierra de equipos. Une todas las partes metálicas: cajas, "
          "carcasas de aparatos y la pata redonda del tomacorriente, y las lleva de regreso al tablero.",
    "p2": "Su trabajo empieza cuando algo falla. Si una fase toca la carcasa metálica de un aparato, la corriente "
          "encuentra por el verde un camino de muy baja resistencia. La corriente sube muchísimo, el breaker se "
          "dispara, y la carcasa deja de estar energizada.",
    "p3": "Sin ese conductor, la carcasa se queda con tensión, esperando a que alguien la toque. Y entonces el camino a "
          "tierra eres tú.",
    "p4": "Por eso el color está normado. El Nec, en la sección doscientos cincuenta punto ciento diecinueve, dice que "
          "la tierra de equipos puede ir desnuda, verde, o verde con franjas amarillas. Y prohíbe usar esos colores "
          "para cualquier otro conductor.",
    "p5": "El neutro, según la sección doscientos punto seis, va en blanco o gris. Para las fases, el Nec no fija un "
          "color único: lo común es negro y rojo. Así cualquier electricista sabe qué es cada cable sin adivinar.",
    "p6": "En la norma internacional I E C, que se usa en Europa, la tierra es verde con amarillo y el neutro es azul. "
          "Si trabajas con equipo importado, ojo con eso.",
    "p7": "Y una regla: nunca uses un cable verde como fase, ni marques un cable negro como tierra en calibres pequeños. "
          "Solo desde el calibre cuatro se permite identificarlo al instalarlo.",
    "cierre": FIN,
}

G16 = {
    "gancho": "Una extensión empieza a echar humo y llamas. Lo primero que piensas es echarle agua. Ese puede ser tu "
              "último error.",
    "p1": "Los fuegos se clasifican según lo que se quema. Clase A: madera, papel y tela. Clase B: líquidos inflamables, "
          "como gasolina o solventes. Clase C: equipo eléctrico energizado. Clase D: metales combustibles. Y clase K: "
          "aceites de cocina.",
    "p2": "En un fuego clase C el peligro no es solo el fuego: es la tensión. El agua común lleva sales y minerales, y "
          "conduce la electricidad. Si le echas un chorro, la corriente puede viajar por el agua hasta tus manos.",
    "p3": "Osha lo dice claro: nunca uses agua para apagar un fuego eléctrico. Primero hay que desenergizar.",
    "p4": "Así que lo primero es cortar la energía: baja el breaker de ese circuito, o el principal, si puedes llegar sin "
          "pasar junto al fuego. Sin tensión, el fuego deja de ser eléctrico y se vuelve un fuego común.",
    "p5": "Si todavía hay tensión, usa un extintor con un agente que no conduce: dióxido de carbono o polvo químico. "
          "Busca la letra C en la etiqueta. Los de polvo A B C sirven para las tres clases y son los más comunes en "
          "casas y negocios.",
    "p6": "El de dióxido de carbono desplaza el oxígeno y no deja residuo: es ideal para tableros y equipo electrónico. "
          "El de polvo químico interrumpe la reacción del fuego, pero deja un polvo que luego hay que limpiar.",
    "p7": "Y si el fuego es grande, o no se apaga en unos segundos, sal y llama a los bomberos. Tu vida vale más que "
          "cualquier aparato.",
    "cierre": FIN,
}

G17 = {
    "gancho": "Tu multímetro dice CAT tres, seiscientos voltios. Mucha gente cree que solo es el voltaje máximo. Pero ese "
              "CAT decide si el multímetro te protege, o te explota en la mano.",
    "p1": "CAT significa categoría de medición, y viene de la norma I E C sesenta y un mil diez. No habla de tu voltaje "
          "normal, sino de los transitorios: picos de tensión que duran microsegundos y llegan por rayos o por la "
          "conmutación de cargas grandes.",
    "p2": "Mientras más cerca estás de la acometida, más energía pueden traer esos picos, porque hay menos impedancia "
          "que los frene. Por eso la instalación se divide en categorías.",
    "p3": "CAT dos: lo que se conecta a un tomacorriente, como electrodomésticos y herramientas portátiles. CAT tres: la "
          "instalación fija del edificio, tableros, breakers y cableado. CAT cuatro: el origen de la instalación, la "
          "acometida, el medidor y las líneas exteriores.",
    "p4": "Según la norma, un multímetro CAT dos de seiscientos voltios debe soportar un impulso de cuatro mil voltios. "
          "Uno CAT tres de seiscientos, seis mil. Y uno CAT cuatro de seiscientos, ocho mil.",
    "p5": "Ojo con esta trampa: un CAT dos de mil voltios aguanta el mismo impulso que un CAT tres de seiscientos. Por eso "
          "no basta con ver el voltaje: hay que ver la categoría del lugar donde vas a medir.",
    "p6": "La regla: el multímetro debe tener una categoría igual o mayor que el lugar donde mides. Para un tablero, "
          "mínimo CAT tres. Para el medidor o la acometida, CAT cuatro.",
    "p7": "Y las puntas también cuentan. Si tus puntas son CAT dos, todo el equipo queda en CAT dos. La protección vale lo "
          "que vale su parte más débil.",
    "cierre": FIN,
}

GUIONES_B = {
    "v12b": ("¿Cuánta corriente", "puede MATARTE?", G12),
    "v13b": ("¿Por qué se", "CALIENTA un cable?", G13),
    "v14b": ("¿Por qué el 12 es", "MÁS GRUESO que el 14?", G14),
    "v15b": ("¿Por qué la tierra", "es VERDE?", G15),
    "v16b": ("¿AGUA en un", "fuego eléctrico?", G16),
    "v17b": ("¿Qué significa CAT III", "en tu multímetro?", G17),
}

if __name__ == "__main__":
    tot = 0
    for k, (_, _, g) in GUIONES_B.items():
        n = sum(len(v) for v in g.values())
        tot += n
        print(k, n, "chars ≈", round(n / 15.5), "s ≈", round(n * 0.4), "créditos")
    print("total", tot, "≈", round(tot * 0.4), "créditos")
    print(0.03 * 6.50, 10**2 * 0.195, 20**2 * 0.195, 8.37 / 2.08, 92 ** (1 / 39), 120 / 100000, 120 / 1000, 9 / 120)

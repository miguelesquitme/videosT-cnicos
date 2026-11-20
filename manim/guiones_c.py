"""Guiones de los Shorts V03–V10 rehechos con el estándar nuevo (1:30–3:00, fundamento técnico, terminología correcta).
Reglas: sin presentarse, números en palabras, cierre "Si te sirvió, suscríbete y sígueme." sin nombrar plataformas.

Fuentes verificadas (1-nov-2026):
 V03  FAA AC 70/7460-1L (Obstruction Marking and Lighting, 2016, según Snopes): esferas de al menos 36 in (91 cm) en
      cables largos que cruzan cañones, lagos o ríos; de 20 in (51 cm) en tramos cortos o cerca de pistas; colores
      naranja de aviación, blanco o amarillo, alternados; separación de unos 200 ft (≈ 61 m). Desviadores de aves:
      APLIC (Avian Power Line Interaction Committee).
 V04  Magnetostricción: el núcleo cambia de dimensión al magnetizarse, en cada medio ciclo → 2 × 60 = 120 Hz.
      Núcleo laminado para reducir corrientes parásitas (física de transformadores).
 V05  NEC 2020 200.10(B) (terminal del neutro identificado: blanco o plateado), 410.50 (el neutro va a la rosca del
      portalámparas), 404.2(B) (interruptores no deben desconectar el neutro). NEMA 5-15.
 V06  NEC 2020 250.124(A): conexiones separables (clavijas y tomacorrientes) deben ser de "primero conecta, último
      desconecta" (first-make, last-break) para el conductor de puesta a tierra de equipos. 406.10.
 V07  NEC 2020 250.110 (partes metálicas de equipos fijos que pueden energizarse se conectan a tierra),
      250.4(A)(5) (camino efectivo de falla de baja impedancia). Efectos de la corriente: OSHA/NIOSH.
 V08  NEC 2020 240.6(A) (valores normalizados 15, 20, 25, 30, 35, 40, 45, 50, 60 A…), 240.4(D) (14 → 15 A,
      12 → 20 A, 10 → 30 A), 210.20(A) (carga continua: dispositivo ≥ 125 % → la carga continua ≤ 80 %);
      Art. 100: carga continua = 3 horas o más. Breaker termomagnético: bimetal (sobrecarga) + bobina (cortocircuito).
 V09  NEC 2020 240.4 y 240.4(D); Tabla 310.16 (12 AWG cobre 20/25/30 A); P = I²R: (30/20)² = 2.25.
 V10  Rigidez dieléctrica del aire ≈ 3 kV/mm (≈ 3 MV/m, aire seco a nivel del mar); densidad Al 2.70 g/cm³ vs
      Cu 8.96 g/cm³; conductividad Al ≈ 61 % IACS; ACSR = aluminio con alma de acero. Aisladores de porcelana o
      polímero.
"""

FIN = "Si te sirvió, suscríbete y sígueme."

G03 = {
    "gancho": "¿Has visto esas bolas de colores colgadas en los cables de alta tensión? No son adornos, y tampoco son para "
              "los pájaros. Son para los pilotos.",
    "p1": "Desde el aire, un cable es casi invisible. Es muy delgado, no tiene luz propia, y contra el cielo o el paisaje "
          "se pierde. Un conductor de distribución mide apenas uno o dos centímetros de grueso. Para un helicóptero o una avioneta que "
          "vuela bajo, chocar con un cable es mortal.",
    "p2": "Por eso existen los marcadores esféricos. La guía de la Administración Federal de Aviación de Estados Unidos "
          "pide esferas de por lo menos noventa y un centímetros cuando el cable cruza un cañón, un lago o un río.",
    "p3": "En tramos más cortos, o cerca de la pista de un aeropuerto, se permiten de cincuenta y un centímetros. Y se "
          "colocan más o menos cada sesenta metros.",
    "p4": "¿Y los colores? Naranja de aviación, blanco y amarillo, alternados. Así siempre hay una bola que contrasta: "
          "contra el cielo, contra la montaña o contra el agua.",
    "p4b": "Además, la esfera se ve igual desde cualquier ángulo. No importa si el piloto se acerca de frente o de lado: "
           "siempre ve un círculo del mismo tamaño. Una placa plana, vista de canto, casi desaparecería.",
    "p5": "Para las aves hay otros dispositivos: espirales y placas que cuelgan del cable, más pequeños, para que lo vean "
          "a tiempo. Esos sí son para los pájaros. Así que, si ves esas bolas sobre un río, ya sabes: le avisan a un piloto "
          "que ahí cruza un cable.",
    "cierre": FIN,
}

G04 = {
    "gancho": "¿Te has parado cerca de un transformador y escuchas ese zumbido grave? No está fallando. Ese sonido tiene "
              "una explicación física.",
    "p0": "Su trabajo es bajar el voltaje de la línea de distribución a los ciento veinte y doscientos cuarenta voltios "
          "de tu casa, con dos bobinas montadas sobre el mismo núcleo.",
    "p1": "Ese núcleo está hecho de láminas de acero eléctrico. Cuando el acero se magnetiza, sus "
          "dominios magnéticos se alinean y el material cambia de tamaño un poquito. Ese efecto se llama magnetostricción.",
    "p2": "En nuestra red, la corriente alterna cambia de sentido sesenta veces por segundo. Pero el acero se estira en "
          "cada medio ciclo, sin importar el sentido. Por eso vibra el doble: ciento veinte veces por segundo.",
    "p3": "Esa vibración pasa al tanque y al aire, y la escuchas como un zumbido grave de ciento veinte hercios. En los "
          "países con red de cincuenta hercios, el zumbido es de cien.",
    "p4": "¿Y por qué el núcleo es de láminas y no de un bloque sólido? Para cortar las corrientes parásitas que se "
          "inducen en el acero: con láminas aisladas, se pierde mucho menos energía en calor.",
    "p4b": "El zumbido del núcleo depende sobre todo del voltaje, porque el voltaje fija cuánto se magnetiza el núcleo. "
           "Con mucha carga, las bobinas también vibran un poco y el sonido aumenta.",
    "p5": "Un zumbido parejo es normal. Pero si escuchas chasquidos, chispazos o ves aceite escurriendo, aléjate y "
          "repórtalo a la empresa eléctrica.",
    "cierre": FIN,
}

G05 = {
    "gancho": "Mira tu tomacorriente: una ranura es más grande que la otra. No es un error de fábrica. Es una medida de "
              "seguridad que se llama polaridad.",
    "p1": "La ranura corta es la fase, el conductor que lleva tensión. La ranura larga es el neutro, que regresa la "
          "corriente y está casi a cero voltios respecto a tierra. En tu instalación, el neutro y la tierra se unen en "
          "un solo punto: el tablero principal. El neutro lleva corriente, así que no es lo mismo que la tierra.",
    "p2": "La clavija polarizada tiene una pata más ancha, así que solo entra de una forma. El Nec, en la sección "
          "doscientos punto diez, pide identificar el terminal del neutro con un color blanco o plateado.",
    "p3": "¿Para qué sirve? Para que cada aparato reciba la fase por el lado correcto. En una lámpara, por ejemplo, el "
          "Nec pide que el neutro vaya a la rosca del portalámparas, la parte que podrías tocar al cambiar la lámpara.",
    "p4": "Y el interruptor de la lámpara corta la fase, nunca el neutro. Así, cuando está apagada, la rosca y el foco "
          "quedan sin tensión.",
    "p5": "Si alguien limara la pata ancha o invirtiera los cables, la rosca quedaría energizada aunque el interruptor "
          "esté apagado. Por eso nunca hay que forzar una clavija polarizada. Y si tienes duda, un probador de tomacorrientes "
          "te dice con sus luces si la fase y el neutro están invertidos.",
    "cierre": FIN,
}

G06 = {
    "gancho": "Toma una clavija de tres patas y mírala de lado. La pata redonda es más larga que las otras dos. No es "
              "casualidad: está diseñada así para protegerte.",
    "p1": "La pata redonda es la de tierra. Conecta las partes metálicas del aparato con el conductor de puesta a tierra "
          "de equipos, el cable verde que regresa al tablero. En el tomacorriente, ese contacto redondo va al tornillo verde.",
    "p2": "Como es más larga, cuando enchufas, la tierra toca primero. Cuando las patas de fase y neutro entran, el "
          "aparato ya está aterrizado.",
    "p3": "Y al desenchufar pasa al revés: la fase y el neutro se separan primero, y la tierra se suelta de último. El "
          "aparato nunca queda con tensión y sin tierra al mismo tiempo.",
    "p3b": "Si el aparato tiene una falla y la fase toca su carcasa, la tierra que ya está conectada lleva esa corriente "
           "al tablero, y el breaker se dispara. La carcasa no se queda esperando a que la toques.",
    "p4": "El Nec lo exige en la sección doscientos cincuenta punto ciento veinticuatro: en clavijas y tomacorrientes, la "
          "tierra debe conectar primero y desconectar de último.",
    "p5": "Por eso nunca le cortes la pata redonda a una clavija para que entre en un tomacorriente viejo. Le estarías "
          "quitando su protección. La solución correcta es instalar un tomacorriente con tierra.",
    "cierre": FIN,
}

G07 = {
    "gancho": "Te estás bañando, tocas la llave o la ducha, y sientes un toque. No es normal, y no lo debes ignorar.",
    "p1": "La ducha eléctrica calienta el agua con una resistencia, igual que una plancha. Esa resistencia va bañada en "
          "agua, separada solo por su aislamiento. En las posiciones más calientes consume más potencia y más "
          "corriente; por eso necesita un circuito exclusivo, con el calibre y el breaker que indique el fabricante.",
    "p2": "Con el tiempo, el sarro y el calor dañan ese aislamiento. Entonces parte de la corriente se escapa por el agua "
          "y por las partes metálicas. Si la ducha no tiene tierra, esa corriente busca otro camino: tu cuerpo.",
    "p3": "Y en el baño estás en el peor caso: piel mojada, pies mojados. Osha lo ejemplifica: con la piel mojada, ciento "
          "veinte voltios pueden hacer pasar ciento veinte miliamperios, suficiente para la fibrilación.",
    "p4": "Por eso el Nec, en la sección doscientos cincuenta punto ciento diez, pide conectar a tierra las partes "
          "metálicas de los equipos fijos. Con el cable verde conectado hasta el tablero, una falla hace que el breaker "
          "se dispare.",
    "p5": "Si tu ducha da toques, corta el breaker y no la uses. Revisa que tenga su conductor de tierra conectado, y "
          "cambia la resistencia si está dañada. Un interruptor de falla a tierra en ese circuito agrega otra "
          "capa de protección.",
    "cierre": FIN,
}

G08 = {
    "gancho": "Abres el tablero y cada breaker tiene un número: quince, veinte, treinta. ¿Qué significa? Pista: no protege "
              "al aparato. Protege al cable.",
    "p1": "Ese número es la corriente nominal en amperios. El Nec, en la sección doscientos cuarenta punto seis, da los "
          "valores normalizados: quince, veinte, veinticinco, treinta, y así hacia arriba.",
    "p2": "Adentro hay dos protecciones. Una térmica: una lámina bimetálica que se calienta y se dobla cuando hay "
          "sobrecarga, y dispara después de un tiempo. Y una magnética: una bobina que dispara al instante con un "
          "cortocircuito. Por eso, mientras mayor la sobrecarga, más rápido dispara: con un poco de exceso "
          "tarda minutos; con mucho, segundos.",
    "p3": "El número se elige según el cable. Según el Nec, el cobre catorce se protege con quince amperios, el doce con "
          "veinte, y el diez con treinta.",
    "p4": "Y ojo con las cargas continuas, las que funcionan tres horas o más. El Nec pide que el breaker sea de por lo "
          "menos ciento veinticinco por ciento de esa carga. En la práctica: un breaker de veinte amperios, hasta "
          "dieciséis amperios continuos.",
    "p5": "Así que el número no dice cuánto aguanta tu aparato: dice cuánta corriente puede llevar ese circuito sin "
          "poner en riesgo el cable. Y cuando se dispara, no está malo: está haciendo su trabajo.",
    "cierre": FIN,
}

G09 = {
    "gancho": "El breaker se dispara a cada rato. ¿La solución es poner uno más grande? No. Ese es uno de los errores más "
              "peligrosos en una instalación.",
    "p1": "El breaker no protege al aparato: protege al cable. El Nec, en la sección doscientos cuarenta punto cuatro, "
          "pide que cada conductor esté protegido según la corriente que soporta.",
    "p2": "Imagina un circuito en cable doce con su breaker de veinte. Si lo cambias por uno de treinta, ahora pueden "
          "pasar treinta amperios por un cable que la tabla tres diez punto dieciséis limita a veinticinco, aun con "
          "aislamiento de setenta y cinco grados.",
    "p3": "Y el calor crece con el cuadrado de la corriente. De veinte a treinta amperios, la corriente sube cincuenta por "
          "ciento, pero el calor en el cable sube dos punto veinticinco veces.",
    "p4": "El aislamiento se degrada, las conexiones se aflojan y se calientan más, y el breaker nunca se entera: para él, "
          "treinta amperios son normales. Así empiezan muchos incendios dentro de las paredes.",
    "p5": "Si el breaker se dispara seguido, te está avisando: hay demasiada carga en ese circuito. Por ejemplo, una plancha de mil doscientos vatios y una "
          "cafetera de mil ya suman más de dieciocho amperios. La solución es repartir "
          "las cargas o hacer un circuito nuevo, con el calibre correcto. Y si se dispara sin carga, "
          "puede haber un cortocircuito: que lo revise un electricista.",
    "cierre": FIN,
}

G10 = {
    "gancho": "Los cables de tu casa tienen forro. Pero los de las líneas de los postes van desnudos. ¿Por qué no los "
              "aíslan, si llevan miles de voltios?",
    "p1": "Porque el aislante es el aire. El aire seco soporta unos tres mil voltios por milímetro antes de romperse. Si "
          "los conductores van bien separados entre sí y del poste, el aire los aísla. En las líneas de transmisión, de mucho más voltaje, "
          "las distancias entre conductores son de metros.",
    "p2": "Lo que los sostiene son los aisladores, de porcelana o de polímero. Su forma con discos alarga el camino por la "
          "superficie, para que la lluvia y el polvo no formen un puente.",
    "p3": "Un forro para miles de voltios sería grueso y pesado, y además atraparía el calor. Desnudo, el cable se enfría "
          "con el aire y puede llevar más corriente.",
    "p4": "Por eso se usa aluminio con alma de acero. El aluminio pesa casi la tercera parte que el cobre, y conduce "
          "alrededor del sesenta por ciento. El acero le da la resistencia mecánica para claros largos.",
    "p5": "Ojo: existen cables con cubierta en zonas con árboles, pero esa cubierta no es un aislamiento completo. Trata "
          "cualquier línea aérea como energizada. Y nunca acerques escaleras, varillas ni piscuchas: si le "
          "acercas un camino conductor, el aire deja de protegerte.",
    "cierre": FIN,
}

# Ampliaciones (para llegar a 1:30 o más)
G06["p2"] += " Es la conexión de seguridad, lista antes de que llegue la energía."
G06["p5"] += " Y evita los adaptadores que dejan la tierra suelta."
G08["p1"] = G08["p1"].replace("Ese número es", "Ese número, impreso en la palanca, es")
G08["p3"] += " Si el breaker fuera más grande, el cable podría calentarse sin que el breaker reaccione."
G10["p2"] += " Y en tensiones más altas se usan más discos en cadena."
G10["p4"] += " Así cada poste soporta menos peso."
G05["p4"] += " Si el interruptor cortara el neutro, la lámpara se apagaría, pero seguiría con tensión adentro."
G07["p3"] += " Y el agua que corre ayuda a que la corriente encuentre camino."

GUIONES_C = {
    "v03c": ("¿Para qué son las", "BOLAS de colores?", G03),
    "v04c": ("¿Por qué ZUMBAN", "los transformadores?", G04),
    "v05c": ("¿Por qué una ranura", "es MÁS GRANDE?", G05),
    "v06c": ("¿Por qué la pata", "redonda es MÁS LARGA?", G06),
    "v07c": ("¿Por qué te da", "TOQUE la ducha?", G07),
    "v08c": ("¿Qué significa el", "número del BREAKER?", G08),
    "v09c": ("¿Por qué NO poner un", "breaker MÁS GRANDE?", G09),
    "v10c": ("¿Por qué los cables", "del poste NO tienen forro?", G10),
}

if __name__ == "__main__":
    tot = 0
    for k, (_, _, g) in GUIONES_C.items():
        n = sum(len(v) for v in g.values())
        tot += n
        print(k, n, "chars ≈", round(n / 15.5), "s ≈", round(n * 0.33), "créditos")
    print("total", tot, "≈", round(tot * 0.33))
    print((30 / 20) ** 2, 2.70 / 8.96, 20 / 1.25)

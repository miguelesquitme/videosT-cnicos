"""
Guiones de los Shorts verticales V03–V18 (canal @miguelesquit). Cada uno con su fundamento técnico.
Reglas: sin presentarse, cierre "Si te sirvió, suscríbete y sígueme." sin nombrar plataformas, números en palabras.

Fuentes verificadas:
 V03  FAA AC 70/7460-1L, 3.5.1 Spherical Markers: esferas de al menos 36 in (91 cm) en cruces de cañones, lagos y
      ríos; 20 in en líneas más cortas o cerca de pistas; colores naranja aviación, blanco o amarillo, alternados;
      separación de unos 200 ft (≈ 61 m).
 V04  Magnetostricción: el núcleo cambia de tamaño en cada medio ciclo → vibración al doble de la frecuencia
      de la red: 120 Hz en redes de 60 Hz (Guatemala usa 60 Hz).
 V05  NEC 2020 200.10(B): en tomacorrientes y clavijas polarizadas, el terminal del neutro se identifica (plateado);
      configuración NEMA 5-15: ranura del neutro más ancha.
 V06  NEMA 5-15: la pata de tierra es más larga: conecta primero y desconecta de último (ANSI/NEMA WD 6).
 V07  NEC 2020 250.110 (partes metálicas de equipos fijos que pueden energizarse → conductor de puesta a tierra
      de equipos) y 250.4(A)(5) (camino efectivo de falla a tierra que permita operar al dispositivo de protección).
 V08  NEC 2020 240.4(D)(3) y (5): cobre 14 AWG → 15 A; 12 AWG → 20 A.
 V09  NEC 2020 240.4 (los conductores se protegen según su ampacidad) y 240.4(D).
 V10  Conductores de distribución aéreos desnudos (ACSR): el aire separa e los aisladores sostienen; los conductores
      con forro existen pero son la excepción.
 V11  U.S. DOE Energy Saver, LED Lighting: los LED residenciales (sobre todo ENERGY STAR) usan al menos 75 % menos
      energía y duran hasta 25 veces más que los incandescentes.
 V12  OSHA (Construction eTool) / NIOSH 1998, choque de 60 Hz, mano-pie, 1 s: 1 mA percepción; 5 mA choque leve;
      6–16 mA doloroso, "no te puedes soltar"; 17–99 mA dolor extremo, paro respiratorio, muerte posible;
      100–2000 mA fibrilación ventricular, muerte probable.
 V13  Ley de Joule P = I²·R; NEC 2020 Tabla 310.16 (cobre 12 AWG: 20/25/30 A a 60/75/90 °C).
 V14  AWG: número mayor = conductor más delgado; NEC 2020 Cap. 9 Tabla 8: 14 AWG 2.08 mm², 12 AWG 3.31 mm²,
      10 AWG 5.26 mm², 8 AWG 8.37 mm² (≈ 4 × 14 AWG).
 V15  NEC 2020 250.119 (tierra: verde, verde con franjas amarillas o desnudo) y 200.6 (neutro: blanco o gris);
      IEC 60445 (tierra verde-amarillo, neutro azul).
 V16  NFPA 10: fuego clase C = equipo eléctrico energizado; se combate con agente no conductor (CO2, polvo químico).
 V17  IEC 61010-1 / 61010-2-030: CAT II cargas conectadas a tomacorrientes; CAT III instalación fija y tableros;
      CAT IV origen de la instalación (acometida, medidor).
 V18  NEC 2020 Tabla 430.7(B) (letras de código de rotor bloqueado, kVA por HP en la placa); corriente de arranque
      varias veces la nominal.
"""

SHORTS = {
    "v03": ("¿Para qué son las", "BOLAS de colores?", {
        "gancho": "¿Has visto esas bolas de colores colgadas en los cables de alta tensión? No son adornos.",
        "p1": "Son marcadores para los pilotos. Desde un avión o un helicóptero, un cable es casi invisible, sobre todo "
              "cuando cruza un río, un lago o un cañón.",
        "p2": "Según la guía de la Administración Federal de Aviación, en esos cruces largos las esferas deben medir "
              "por lo menos noventa y un centímetros. Cerca de un aeropuerto se permiten de cincuenta y un centímetros.",
        "p3": "Los colores son naranja, blanco y amarillo, y se alternan para que resalten contra el cielo o el paisaje. "
              "Y se colocan más o menos cada sesenta metros.",
        "p4": "Así que esas bolitas no están ahí para los pájaros: están para que un piloto no choque con un cable.",
        "p5": "Para las aves hay otros dispositivos: espirales y placas que cuelgan del cable, para que lo vean a tiempo y no choquen. Esos sí son para los pájaros.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v04": ("¿Por qué ZUMBAN", "los transformadores?", {
        "gancho": "¿Te has parado cerca de un transformador y escuchas ese zumbido? Tiene una explicación muy curiosa.",
        "p1": "El transformador tiene un núcleo de láminas de hierro. Cuando el hierro se magnetiza, cambia de tamaño un "
              "poquito. Se estira y se encoge. A eso se le llama magnetostricción.",
        "p2": "En nuestra red la corriente alterna cambia de sentido sesenta veces por segundo. Y el hierro se estira en "
              "cada medio ciclo, sin importar el sentido. Por eso vibra el doble: ciento veinte veces por segundo.",
        "p3": "Esa vibración mueve el aire, y eso es lo que escuchas: un zumbido grave, de ciento veinte hercios.",
        "p4": "Un zumbido parejo es normal. Pero si escuchas chasquidos o chispazos, aléjate y repórtalo a la empresa "
              "eléctrica.",
        "p5": "Y un dato más: en los países donde la red es de cincuenta hercios, el zumbido es de cien hercios. Un poquito más grave.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v05": ("¿Por qué un agujero", "es MÁS GRANDE?", {
        "gancho": "Mira tu tomacorriente: un agujero es más grande que el otro. No es un error de fábrica.",
        "p1": "La ranura pequeña es la fase, la que trae el voltaje. La ranura grande es el neutro. Y el agujero redondo "
              "es la tierra.",
        "p2": "Muchas clavijas tienen una pata más ancha. Así, solo entran de una forma, y la fase siempre llega al lugar "
              "correcto del aparato. A esto se le llama polaridad.",
        "p3": "¿Para qué sirve? En una lámpara, por ejemplo, la fase llega al interruptor y al centro del portalámparas, "
              "y la rosca queda del lado del neutro. Si tocas la rosca al cambiar el foco, es menos peligroso.",
        "p4": "Por eso el Nec pide que el terminal del neutro se identifique: es el tornillo plateado. La fase va al "
              "tornillo de latón.",
        "p5": "Ojo: si alguien conecta el tomacorriente al revés, la clavija polarizada ya no protege, y la rosca del foco queda con voltaje. Por eso conviene revisarlo con un probador.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v06": ("¿Por qué la pata", "redonda es MÁS LARGA?", {
        "gancho": "Toma una clavija de tres patas y mírala de lado. La pata redonda es más larga que las otras dos. ¿Por "
                  "qué?",
        "p1": "Esa pata es la tierra. Y está diseñada así a propósito: al enchufar, es la primera en hacer contacto.",
        "p2": "Así, antes de que llegue el voltaje al aparato, su carcasa de metal ya está conectada a tierra.",
        "p3": "Y al desconectar pasa lo contrario: la tierra es la última en soltarse. El aparato nunca queda con voltaje "
              "y sin tierra, ni siquiera por un instante.",
        "p4": "Por eso nunca le cortes la pata de tierra a una clavija para que entre en un tomacorriente viejo. Le "
              "quitas su protección.",
        "p5": "Y otro detalle: el agujero redondo debe estar conectado de verdad al cable verde. Un tomacorriente de tres agujeros sin tierra conectada engaña: parece seguro, pero no lo es.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v07": ("¿Por qué te da", "TOQUE la ducha?", {
        "gancho": "Te estás bañando, tocas la llave, y sientes un toque. ¿Qué está pasando?",
        "p1": "La ducha eléctrica calienta el agua con una resistencia. Si su aislamiento falla, el voltaje puede llegar "
              "al agua o a las partes de metal.",
        "p2": "Si la ducha no tiene tierra, esa falla no tiene a dónde ir. La corriente busca otro camino: tu cuerpo, "
              "mojado y descalzo.",
        "p3": "Con el cable de tierra conectado, la falla tiene un camino directo de regreso al tablero. La corriente sube "
              "de golpe, y el breaker se dispara.",
        "p4": "El Nec pide que las partes de metal de un equipo fijo como este se conecten a tierra. Si tu ducha da toques, "
              "baja el breaker y no la uses hasta revisarla.",
        "p5": "Y no basta con conectar el cable verde a la ducha: tiene que llegar hasta la barra de tierra del tablero. Si se queda suelto en la pared, no sirve de nada.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v08": ("¿Qué significa el", "15 o 20 del BREAKER?", {
        "gancho": "Abres el tablero y cada breaker tiene un número: quince, veinte, treinta. ¿Qué significa?",
        "p1": "Es la corriente máxima en amperios. Si por el circuito pasa más corriente durante un tiempo, el breaker se "
              "dispara.",
        "p2": "Pero lo importante es a quién protege: protege al cable. Cada calibre aguanta una corriente sin "
              "sobrecalentarse.",
        "p3": "Según el Nec, el cable de cobre calibre catorce va con un breaker de quince amperios, y el calibre doce con "
              "uno de veinte.",
        "p4": "Así que el número del breaker te dice qué cable debería tener ese circuito.",
        "p5": "Y una curiosidad: el breaker tiene dos partes. Una térmica, que se calienta poco a poco con una sobrecarga, y una magnética, que actúa al instante en un cortocircuito.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v09": ("¿Por qué NO poner un", "breaker MÁS GRANDE?", {
        "gancho": "El breaker se dispara a cada rato. ¿La solución es poner uno más grande? No. Y te explico por qué.",
        "p1": "El breaker está calculado para el cable. Un calibre catorce va con quince amperios, y un calibre doce con "
              "veinte.",
        "p2": "Si en un cable calibre catorce pones un breaker de treinta, puede pasar el doble de corriente sin que se "
              "dispare. Y como el calor crece con el cuadrado de la corriente, el cable se calienta cuatro veces más.",
        "p3": "El aislamiento se derrite, y el cable dentro de la pared se convierte en un riesgo de incendio.",
        "p4": "Si el breaker se dispara, está haciendo su trabajo. La solución es repartir las cargas, o hacer un circuito "
              "nuevo con el cable adecuado.",
        "p5": "Y si el breaker se dispara apenas lo subes, puede haber un corto. No lo fuerces: busca la falla primero.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v10": ("¿Por qué la alta tensión", "NO tiene forro?", {
        "gancho": "Los cables de tu casa tienen forro. Pero los de los postes van desnudos. ¿Por qué?",
        "p1": "Porque el aislante es el aire. Mientras los cables estén separados y lejos de la gente, el aire no deja "
              "pasar la corriente.",
        "p2": "Para que no toquen el poste, se sostienen con aisladores de porcelana o polímero. Son ellos los que separan "
              "el voltaje de la estructura.",
        "p3": "Forrar un cable de miles de voltios requiere un aislamiento grueso y pesado. Desnudo, es más liviano y "
              "se enfría mejor al aire. Existen cables con forro, pero en distribución son la excepción.",
        "p4": "Y ojo: ese forro tampoco te protegería. Nunca toques ni te acerques a un cable de alta tensión.",
        "p5": "Por eso la distancia es tu protección. Escaleras, varillas, piscuchas o andamios cerca de las líneas pueden ser mortales.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v11": ("Foco LED: ¿por qué", "gasta TAN POCO?", {
        "gancho": "Un foco LED alumbra lo mismo que uno de los de antes, pero gasta muchísimo menos. ¿Cómo lo logra?",
        "p1": "El foco de antes producía luz calentando un filamento hasta ponerlo al rojo blanco. La mayor parte de esa "
              "energía se iba en calor, no en luz.",
        "p2": "El LED es un semiconductor: produce luz directamente cuando pasa la corriente, y se calienta mucho menos.",
        "p3": "Según el Departamento de Energía de Estados Unidos, un LED residencial usa por lo menos setenta y cinco "
              "por ciento menos energía, y dura hasta veinticinco veces más.",
        "p4": "Por eso un LED de nueve vatios puede reemplazar a uno antiguo de sesenta. Se nota en el recibo.",
        "p5": "Y como se calienta mucho menos, también ayuda en lugares cerrados: menos calor dentro de la lámpara y del cuarto.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v12": ("¿Cuánta corriente", "puede MATARTE?", {
        "gancho": "No es el voltaje el que mata: es la corriente que pasa por tu cuerpo. ¿Y cuánta hace falta? Muy poca.",
        "p1": "Un miliamperio, es decir, una milésima de amperio, apenas se siente como un cosquilleo.",
        "p2": "Entre seis y dieciséis miliamperios, el choque duele y empiezas a perder el control de los músculos. Puede "
              "que no te puedas soltar.",
        "p3": "Entre diecisiete y noventa y nueve miliamperios, hay dolor extremo y puede haber paro respiratorio. Y desde "
              "cien miliamperios, el corazón puede entrar en fibrilación. Es probable la muerte.",
        "p4": "Para comparar: un foco LED de nueve vatios consume unos setenta y cinco miliamperios. Esos datos son de la "
              "agencia de seguridad laboral de Estados Unidos.",
        "p5": "¿Y el voltaje? Con más voltaje, más corriente logra atravesar la resistencia de tu cuerpo. Por eso ciento veinte voltios ya pueden ser mortales, sobre todo con la piel mojada.",
        "cierre": "Respeta siempre la electricidad. Si te sirvió, suscríbete y sígueme."}),
    "v13": ("¿Por qué se", "CALIENTA un cable?", {
        "gancho": "Toca un cable que lleva mucha corriente y vas a notar que está tibio. ¿De dónde sale ese calor?",
        "p1": "El cobre conduce muy bien, pero no es perfecto: tiene una pequeña resistencia. Y cuando la corriente pasa "
              "por una resistencia, parte de la energía se convierte en calor.",
        "p2": "Es la ley de Joule: el calor es igual a la corriente al cuadrado por la resistencia. Al cuadrado. Si la "
              "corriente se duplica, el calor se multiplica por cuatro.",
        "p3": "Por eso cada calibre tiene una corriente máxima. El Nec la da en su tabla tres diez punto dieciséis, según "
              "el calibre y la temperatura que soporta el aislamiento.",
        "p4": "Un cable caliente es una advertencia: la corriente es demasiada para ese calibre.",
        "p5": "Y además del calibre, importa cómo va el cable: muchos conductores juntos en un mismo tubo se enfrían peor, y el Nec pide reducir su corriente permitida.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v14": ("¿Por qué el 12 es", "MÁS GRUESO que el 14?", {
        "gancho": "Calibre doce y calibre catorce. ¿Cuál es más grueso? El doce. Y no es un error.",
        "p1": "En el sistema americano de calibres, el número va al revés: mientras más grande el número, más delgado es "
              "el cable.",
        "p2": "Viene de cómo se fabricaba el alambre: se estiraba pasándolo por dados, y el número indicaba cuántas "
              "pasadas llevaba. Más pasadas, más delgado.",
        "p3": "Los datos del Nec: el calibre catorce tiene dos punto cero ocho milímetros cuadrados de cobre. El doce, tres "
              "punto treinta y uno. El diez, cinco punto veintiséis. Y el ocho, ocho punto treinta y siete: cuatro veces "
              "el catorce.",
        "p4": "Así que cuando bajas el número, subes el cobre.",
        "p5": "Y para cables más gruesos que el calibre uno, se usan ceros: uno cero, dos ceros, tres ceros y cuatro ceros. Después de eso, se mide en kcmil.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v15": ("¿Por qué el cable de", "tierra es VERDE?", {
        "gancho": "Abres una caja y hay cables de colores. ¿El verde para qué es? ¿Y por qué no se usa cualquier color?",
        "p1": "Los colores son una forma de hablar sin palabras: le dicen al siguiente electricista qué hace cada cable.",
        "p2": "Según el Nec, la tierra de equipos es verde, verde con franjas amarillas, o desnuda. Y el neutro es blanco "
              "o gris. Ningún otro conductor puede usar esos colores.",
        "p3": "En Europa, con la norma I E C, cambia: la tierra es verde con amarillo, y el neutro es azul.",
        "p4": "Por eso, antes de trabajar, confirma qué norma se usó en esa instalación. Y nunca uses el verde como fase.",
        "p5": "Y la fase puede ser negra, roja, azul, o de otro color, siempre que no sea blanco, gris ni verde.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v16": ("¿AGUA en un", "fuego eléctrico?", {
        "gancho": "Un aparato conectado empieza a echar fuego. Lo primero que se te ocurre: agua. Error.",
        "p1": "El agua común conduce la electricidad. Si la tiras sobre un equipo energizado, la corriente puede viajar "
              "por el chorro hasta tu cuerpo.",
        "p2": "Primero, si es seguro, corta la energía: baja el breaker. Sin voltaje, el riesgo de choque desaparece.",
        "p3": "Y para fuego en equipos energizados, la norma de extintores clasifica el fuego como clase C. Se usa un "
              "agente que no conduce, como el dióxido de carbono o el polvo químico.",
        "p4": "Revisa la etiqueta de tu extintor: si dice C, sirve para fuego eléctrico.",
        "p5": "Y si el fuego es grande, o no puedes cortar la energía, sal y llama a los bomberos. Ningún aparato vale más que tu vida.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v17": ("¿Qué significa", "CAT III en tu multímetro?", {
        "gancho": "Tu multímetro dice CAT tres, seiscientos voltios. ¿Qué significa eso? Puede salvarte de un accidente.",
        "p1": "La categoría indica dónde puedes medir con seguridad. No se trata solo del voltaje normal, sino de los "
              "picos de voltaje que pueden aparecer en ese punto de la instalación.",
        "p2": "CAT dos es para aparatos conectados a un tomacorriente. CAT tres, para la instalación fija: tableros, "
              "circuitos y tomacorrientes. Y CAT cuatro, para el origen: la acometida y el medidor.",
        "p3": "Mientras más cerca de la acometida, más energía puede tener un pico. Por eso un multímetro sin categoría, o "
              "de una categoría baja, puede explotar en tus manos.",
        "p4": "Usa siempre un multímetro y unas puntas con la categoría y el voltaje del lugar donde vas a medir.",
        "p5": "Y fíjate en las puntas: también tienen categoría. Si el multímetro es CAT tres pero las puntas son CAT dos, el conjunto queda en CAT dos.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
    "v18": ("¿Por qué el motor", "jala MÁS al arrancar?", {
        "gancho": "Cuando arranca la bomba o el compresor, las luces bajan un instante. ¿Por qué?",
        "p1": "Un motor detenido se comporta casi como un corto: todavía no genera la fuerza contraelectromotriz que "
              "limita su corriente.",
        "p2": "Por eso, al arrancar, pide varias veces su corriente normal durante un instante. Cuando toma velocidad, la "
              "corriente baja a su valor de trabajo.",
        "p3": "La placa del motor lo indica con una letra de código. El Nec, en su tabla cuatro treinta punto siete B, "
              "dice cuántos kilovoltamperios por caballo de fuerza pide con el rotor bloqueado.",
        "p4": "Por eso la protección de un motor se calcula distinto que la de un foco: tiene que aguantar el arranque sin "
              "dispararse.",
        "p5": "En motores grandes, para reducir esa corriente se usan arrancadores: estrella triángulo, arrancadores suaves o variadores de frecuencia.",
        "cierre": "Si te sirvió, suscríbete y sígueme."}),
}

if __name__ == "__main__":
    import sys
    tot = 0
    for k, (_, _, g) in SHORTS.items():
        n = sum(len(t) for t in g.values())
        tot += n
        print(k, n)
    print("total", tot)

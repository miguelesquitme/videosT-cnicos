"""F01 · Así funciona una FOTOCELDA (fotocontrol de alumbrado, ANSI C136.10). Reel vertical v2 (23-nov), dibujo real pieza por pieza.
Fuentes: NSi Photocontrols catalog (serie 5200: 1,5 fc ±0,2; apagado/encendido 1,5:1; enciende al instante; apaga en 3–5 s;
falla encendido; cubierta de polipropileno UV con color por tensión; ventana de acrílico; patas de latón; CdS o silicio; relé de CD;
MOV 360 J; negro línea, rojo carga, blanco neutro). JL-205C (Ø84 × 66 mm; ventana al norte; girar a la derecha para trabar;
prueba con cinta negra, no con el dedo, ≈2 min). Intermatic K122 (receptáculo Ø65 mm fenólico, contactos de latón).
1,5 fc × 10,764 = 16,1 lux.
"""
TIT = ("ASÍ FUNCIONA UNA", "FOTOCELDA")
GUION = {
    "gancho": "Al caer la tarde, las lámparas de la calle se encienden solas, sin que nadie toque un interruptor. "
              "La responsable es esta pieza de tres patas que va encima de la lámpara: el fotocontrol, o fotocelda. Vamos a abrirla.",
    "p1": "Por fuera tiene tres partes. La cubierta, de polipropileno con protección ultravioleta; su color indica la tensión, "
          "y la gris es de ciento veinte voltios. La ventana, de acrílico transparente, que se instala viendo al norte, "
          "para que el sol no le pegue de frente. Y la base, con tres patas de latón y un empaque que sella contra el agua.",
    "p2": "Las tres patas forman un enchufe de giro: entra en el receptáculo y se gira a la derecha hasta trabar. "
          "Cada pata tiene su función. Línea, que trae la fase. Carga, que sale hacia la lámpara. Y neutro. "
          "En el receptáculo, el cable negro es la línea, el rojo la carga y el blanco el neutro.",
    "p3": "Ahora, por dentro. Detrás de la ventana está el sensor: en los modelos antiguos, una fotorresistencia de sulfuro de cadmio; "
          "en los electrónicos, un fototransistor de silicio. Una pequeña fuente alimenta un relé de corriente directa, "
          "que es el que conecta la lámpara. Y este disco azul es un varistor, que absorbe las sobretensiones de los rayos.",
    "p4": "De día, la luz llega al sensor y el relé se mantiene abierto: la lámpara está apagada. "
          "Al atardecer, cuando la luz baja a uno punto cinco pie candela, unos dieciséis lux, la bobina atrae el contacto, "
          "el relé cierra y la lámpara enciende al instante.",
    "p5": "En la mañana, para apagar necesita más luz: hasta uno punto cinco veces el nivel de encendido. "
          "Esa diferencia evita que parpadee con la luz cambiante. Y apagar le toma de tres a cinco segundos; "
          "así, los faros de un carro o un relámpago en la noche no la apagan.",
    "p6": "Si el fotocontrol se daña, falla encendido: la lámpara se queda prendida también de día. "
          "Por eso, una lámpara encendida a mediodía es la primera pista de un fotocontrol dañado.",
    "p7": "Dos consejos de campo. Si la lámpara se enciende y se apaga toda la noche, su propia luz o la de un rótulo le está pegando al sensor. "
          "Y para probarla de día, tapa la ventana con cinta negra, no con el dedo, porque el dedo deja pasar luz. "
          "Espera unos dos minutos y debe encender.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

"""V22 v2 · ¿Por qué me da TOQUES algo metálico? Estática vs fuga (reel vertical, dibujo real; 23-nov).
Fuentes (4+; ficha referencias/v22_fuentes.md): IEC 61000-4-2 (150 pF + 330 Ω; 8 kV contacto → 30 A pico, 0,8 ns,
16 A a 30 ns, 8 A a 60 ns); ESDA Fundamentals of ESD parte 1 (alfombra 35 000 V con 10–25 % HR; 1 500 V con 65–90 % HR);
InCompliance "Static electricity and people" (pocos notan < 1 000 V; casi todos se quejan > 3 000 V); OSHA (1 mA se siente;
6–16 mA no se puede soltar); NEC 2020 250.4(A)(5); worldstandards.eu (NEMA 5-15: pata de tierra Ø4,8 mm, 3,2 mm más larga).
Cálculos: E = ½·150 pF·(8 kV)² = 4,8 mJ; 120 V / 100 kΩ = 1,2 mA; 120 V / 1 kΩ = 120 mA.
"""
TIT = ("ASÍ FUNCIONA UN", "TOQUE AL TOCAR METAL")
GUION = {
    "gancho": "Tocas la manija de la puerta y te da un toque. Tocas la lavadora y también. Parecen iguales, "
              "pero uno es inofensivo y el otro puede matarte. Así se distinguen.",
    "p1": "El primero es electricidad estática. Al caminar sobre una alfombra en un día seco, tu cuerpo se puede cargar "
          "hasta treinta y cinco mil voltios. Con el aire húmedo, apenas mil quinientos. Al acercar el dedo al metal, "
          "la carga salta en una chispa.",
    "p2": "La norma I E C sesenta y un mil cuatro dos modela tu cuerpo como un capacitor de ciento cincuenta picofaradios. "
          "A ocho mil voltios, el pico llega a treinta amperios, pero en sesenta nanosegundos ya bajó a ocho, y se acaba. "
          "La energía es de unos cinco milijoules: un susto. Por debajo de mil voltios casi nadie la siente.",
    "p3": "El segundo es una fuga. Dentro de la lavadora, el cable de fase rozó con el borde del chasis y se peló. "
          "Si no hay conductor de tierra, todo el metal queda a ciento veinte voltios. No es una chispa: "
          "es un hormigueo que se repite cada vez que lo tocas.",
    "p4": "Y esa corriente no se acaba: va y viene sesenta veces por segundo mientras la toques. Con la piel seca, "
          "unos cien mil ohmios, pasa poco más de un miliamperio. Con la piel mojada, mil ohmios, ciento veinte miliamperios. "
          "Desde seis a dieciséis miliamperios ya no te puedes soltar.",
    "p5": "Para eso es la pata redonda de la clavija: es más larga, conecta primero y une el chasis a tierra. "
          "Con tierra, la falla regresa por el conductor verde, la corriente sube de golpe y el breaker se dispara. "
          "Nunca le cortes esa pata.",
    "p6": "Para comprobarlo, pon el multímetro en voltaje alterno y mide entre el chasis y la tierra del tomacorriente. "
          "Si marca ciento veinte voltios, desconecta el aparato y no lo uses. La regla: chispa de un instante, estática. "
          "Hormigueo que se repite, falla.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

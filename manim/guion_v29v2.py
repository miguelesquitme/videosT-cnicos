"""V29 v2 · ¿Por qué BAJAN las luces cuando algo arranca? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v29_fuentes.md): NEC 2020 T430.248 (½ hp 115 V: 9,8 A), T430.251(A) (½ hp 115 V: 58,8 A), 210.19(A) NI
(3 % / 5 %), Cap. 9 T8 (12 AWG trenzado 6,50 Ω/km); IDC Motor starting sags; Power Monitors "Identifying loose neutrals"
(119/121 → 105/135 V); EC&M "The case of the defective neutral".
Cálculos: R = 6,50 Ω/km × 0,060 km = 0,39 Ω; 9,8 A × 0,39 = 3,8 V; 58,8 A × 0,39 = 22,9 V → 97 V; 58,8 / 9,8 = 6,0."""
TIT = ("ASÍ BAJAN LAS LUCES", "AL ARRANCAR UN MOTOR")
GUION = {
    "gancho": "Arranca la bomba o el compresor de la refrigeradora, y las luces bajan por un instante. ¿Es normal o es una falla? "
              "Depende de cómo bajen.",
    "p1": "Un motor, al arrancar, pide mucha más corriente que trabajando. Según el N E C, un motor de medio caballo a ciento quince voltios "
          "consume nueve punto ocho amperios trabajando, y al arrancar hasta cincuenta y ocho punto ocho: seis veces más.",
    "p2": "Esa corriente pasa por los cables, y los cables tienen resistencia. Treinta metros de cable calibre doce, ida y vuelta, "
          "son cero punto treinta y nueve ohmios. Con nueve punto ocho amperios caen tres punto ocho voltios. "
          "Con cincuenta y ocho punto ocho caen veintitrés.",
    "p3": "Si las luces están en ese circuito, ven la caída: por un instante quedan en noventa y siete voltios, "
          "y vuelven a subir cuando el motor toma velocidad. Si es breve y leve, es normal.",
    "p4": "Para limitarlo, el N E C recomienda que la caída no pase del tres por ciento en un circuito, y del cinco en total. "
          "La solución: cable más grueso, o el motor en su propio circuito.",
    "p5": "Pero si unas luces bajan y otras suben al mismo tiempo, es otra cosa: un neutro flojo. "
          "Una línea puede caer a ciento cinco voltios mientras la otra sube a ciento treinta y cinco. Eso quema aparatos.",
    "p6": "Mide en el tablero, de cada fase a neutro. Si las dos lecturas se separan cuando conectas una carga, desenergiza y revisa el neutro. "
          "Y si el problema está en la acometida, llama a la distribuidora.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

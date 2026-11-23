"""V24 v2 · ¿Por qué SUENAN los cables de alta tensión? Efecto corona (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v24_fuentes.md): Nassau/Southwire ACSR Drake 26/7 (Ø 1,108 in = 28,14 mm; 7 de acero, 26 de aluminio);
MacLean Power MG523Z (ANSI 52-3, vidrio templado, Ø255 mm, paso 146 mm, bola y casquillo); EEPower "Understanding corona
discharge" (≈30 kV/cm aire seco, lluvia/neblina, 1–20 kHz, ozono, pérdidas < 1 %, haces, anillos anticorona, brillo azulado);
Wikipedia "Peek's law" (cables trenzados: factor 0,87–0,83)."""
TIT = ("ASÍ SUENA EL", "EFECTO CORONA")
GUION = {
    "gancho": "Si pasas debajo de una línea de alta tensión en una noche húmeda, puedes oír un chisporroteo. "
              "No es tu imaginación: es el aire alrededor del cable que se está rompiendo. Se llama efecto corona.",
    "p1": "Empecemos por el cable. Este es un A C S R Drake: siete hilos de acero al centro, que le dan la resistencia mecánica, "
          "y veintiséis hilos de aluminio alrededor, que llevan la corriente. Mide veintiocho milímetros de diámetro y no tiene forro.",
    "p2": "Con cientos de miles de voltios, el campo eléctrico es más fuerte justo en la superficie del conductor. "
          "Cuando pasa de unos treinta kilovoltios por centímetro, lo que aguanta el aire seco, el aire se ioniza: "
          "aparecen pequeñas descargas que suenan y, en la oscuridad, brillan en azul.",
    "p3": "Con lluvia o neblina, las gotas que cuelgan del cable forman puntas donde el campo se concentra, y el ruido aumenta. "
          "Además se forma ozono y se pierde energía, aunque en una línea bien diseñada es menos del uno por ciento.",
    "p4": "La solución es la geometría. En lugar de un solo cable por fase, se usan dos, tres o cuatro juntos, "
          "separados por espaciadores. Ese haz se comporta como un conductor más grueso, y el campo en la superficie baja.",
    "p5": "Lo mismo pasa en los herrajes. Cada disco de vidrio templado mide doscientos cincuenta y cinco milímetros, "
          "y se engancha con bola y casquillo cada ciento cuarenta y seis. Y abajo, ese aro de aluminio es el anillo anticorona: "
          "reparte el campo para que no se concentre en las puntas de los herrajes.",
    "p6": "Que se escuche no significa que puedas acercarte: te recuerda que la línea está energizada. "
          "Nunca acerques varillas, escaleras ni barriletes.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

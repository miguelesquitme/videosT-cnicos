"""V30 v2 · ¿Qué es un KILOVATIO HORA? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v30_fuentes.md): Landis+Gyr FOCUS AX (2S, 120/240 V, Clase 200, LCD 9 dígitos, ANSI C12.20); Measurement Canada
AE-1641 (LED de prueba infrarrojo, registros kWh); CPS Energy meter specifications; LBL Standby (5–10 %, ejemplo 5 W); U.S. DOE (5–10 %).
Cálculos: 1 kWh = 1000 W × 3600 s = 3,6 MJ; 1200 W × 0,5 h = 0,6 kWh; 100 W × 5 h × 30 = 15 kWh; 5 W × 720 h = 3,6 kWh."""
TIT = ("ASÍ SE MIDE UN", "KILOVATIO HORA")
GUION = {
    "gancho": "En el recibo de la luz no te cobran voltios ni amperios: te cobran kilovatios hora. ¿Qué es eso, "
              "y cómo calculas cuánto gasta cada aparato?",
    "p1": "El vatio es potencia: qué tan rápido se usa la energía. El kilovatio hora es energía: potencia por tiempo. "
          "Mil vatios funcionando una hora es un kilovatio hora: tres punto seis millones de joules.",
    "p2": "Y quien lo cuenta es el medidor. Este es un medidor digital de base, forma dos S, para ciento veinte y doscientos cuarenta voltios. "
          "Mide el voltaje y la corriente, los multiplica, y suma la energía en su registro de kilovatios hora. "
          "Por este led infrarrojo manda pulsos proporcionales a la energía, para verificarlo.",
    "p3": "Ahora la cuenta. Una plancha de mil doscientos vatios, media hora: cero punto seis kilovatios hora. "
          "Un televisor de cien vatios, cinco horas diarias durante treinta días: quince kilovatios hora al mes.",
    "p4": "Lo que produce calor es lo que más gasta: plancha, ducha, estufa, secadora. "
          "Los electrónicos gastan menos por hora, pero suman muchas horas.",
    "p5": "Y está el consumo en espera: aparatos apagados que siguen conectados. Uno de cinco vatios, todo el mes, "
          "son tres punto seis kilovatios hora. En una casa, la espera puede ser del cinco al diez por ciento de la energía.",
    "p6": "La fórmula para cualquier aparato: vatios por horas al día por días, entre mil. "
          "Multiplícalo por el precio del kilovatio hora de tu recibo, y sabrás cuánto te cuesta.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

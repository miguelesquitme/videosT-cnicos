"""V26 v2 · ¿Qué es el FACTOR DE POTENCIA? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v26_fuentes.md): Eaton PFC guide for the plant engineer; TDK FilterCap MKP B3236 (datasheet);
Schneider VarPlus Can; Fluke "Power factor formula". Cálculos (Python): I = P/(√3·V·FP): 10 kW, 480 V → 12,66 A (0,95) y
17,18 A (0,70) → +35,7 %; 100 kW / 125 kVA = 0,80."""
TIT = ("ASÍ FUNCIONA EL", "FACTOR DE POTENCIA")
GUION = {
    "gancho": "Dos motores hacen el mismo trabajo, pero uno pide treinta y seis por ciento más corriente que el otro. "
              "La diferencia se llama factor de potencia.",
    "p1": "Un motor necesita dos potencias. La activa, en kilovatios, es la que hace trabajo: mueve el eje. "
          "Y la reactiva, en kilovoltamperios reactivos, la que mantiene su campo magnético: va y viene entre la red y el motor sin hacer trabajo.",
    "p2": "Las dos forman un triángulo. La hipotenusa es la potencia aparente, en kilovoltamperios: lo que la red tiene que entregar. "
          "El factor de potencia es activa entre aparente. Cien kilovatios con ciento veinticinco kilovoltamperios dan cero punto ochenta.",
    "p3": "En trifásico, la corriente es la potencia entre raíz de tres, el voltaje y el factor de potencia. Diez kilovatios a cuatrocientos ochenta voltios: "
          "con cero punto noventa y cinco son doce punto siete amperios; con cero punto setenta, diecisiete punto dos. "
          "Treinta y seis por ciento más, para el mismo trabajo.",
    "p4": "Más corriente es más calor en cables y transformadores. Por eso las distribuidoras cobran recargos a la industria con bajo factor de potencia. "
          "La meta usual es cero punto noventa y cinco.",
    "p5": "La solución es un capacitor. Por dentro son bobinas de película de polipropileno metalizado, selladas en resina dentro de un bote de aluminio. "
          "Entrega la potencia reactiva junto al motor, y la red ya no tiene que llevarla y traerla.",
    "p6": "Dos detalles de seguridad. Trae resistencias de descarga: al desconectarlo debe bajar a menos de cincuenta voltios en un minuto. "
          "Y si falla, el bote se infla y un desconectador por sobrepresión lo saca del circuito. Si ves uno inflado, no lo toques: "
          "cámbialo desenergizado.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

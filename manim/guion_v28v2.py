"""V28 v2 · ¿Qué pasa si conectas 120 V a 240 V? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v28_fuentes.md): Tempco (tubular: Ni 80 / Cr 20, MgO compactado, pin frío); Watlow WATROD (Ø 6,6 / 8,0 / 10,9 mm;
vainas de acero); Leviton 5661 (NEMA 6-15R 250 V 15 A); worldstandards.eu y plug-socket museum (NEMA 5-15, 125 V);
Apple manual del adaptador USB-C (100–240 V~ 50–60 Hz). Cálculos: R = 120²/1000 = 14,4 Ω; I = 240/14,4 = 16,7 A; P = 240²/14,4 = 4000 W;
240 V nominal a 120 V → ¼ de la potencia."""
TIT = ("ASÍ SE QUEMA UN", "APARATO DE 120 V")
GUION = {
    "gancho": "Conectas un aparato de ciento veinte voltios en un tomacorriente de doscientos cuarenta. En segundos huele a quemado. "
              "¿Por qué tan rápido, si solo es el doble de voltaje?",
    "p1": "Veamos un aparato que calienta. Por dentro tiene una resistencia tubular: un alambre de níquel cromo en espiral, "
          "rodeado de óxido de magnesio compactado, dentro de un tubo de acero de ocho milímetros. El óxido aísla el alambre, "
          "pero deja pasar el calor.",
    "p2": "En su etiqueta dice: ciento veinte voltios, mil vatios. Con la ley de Ohm, su resistencia es el voltaje al cuadrado "
          "entre la potencia: catorce punto cuatro ohmios. Ese valor casi no cambia, aunque cambie el voltaje.",
    "p3": "A doscientos cuarenta voltios, la corriente se duplica: dieciséis punto siete amperios. Y la potencia es voltaje por corriente: "
          "cuatro mil vatios. Doble voltaje, cuatro veces la potencia. El alambre se pone amarillo, casi blanco, y se funde.",
    "p4": "Al revés pasa lo contrario: un calentador de doscientos cuarenta conectado a ciento veinte entrega solo la cuarta parte. "
          "No se quema, pero casi no calienta.",
    "p5": "Por eso los tomacorrientes tienen formas distintas. El cinco quince, de ciento veinticinco voltios, tiene las ranuras verticales. "
          "El seis quince, de doscientos cincuenta, las tiene horizontales, para que la clavija de un aparato de ciento veinte no entre. "
          "Nunca lo fuerces con un adaptador.",
    "p6": "Y antes de conectar, lee la etiqueta. Si dice cien a doscientos cuarenta voltios, como la mayoría de cargadores, sirve en ambos. "
          "Si dice solo ciento veinte, es solo ciento veinte.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

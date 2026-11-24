"""V32 v2 · ¿ESTRELLA o TRIÁNGULO? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v32_fuentes.md): IEC 60034-8 (marcado de bornes; vía Siemens); WEG manual de instalación; Bitzer "Star-delta start"
(⅓ de corriente y par; Δ a la tensión de red; seis puntas libres; 3 contactores; 75–80 % de la velocidad); Siemens SIRIUS estrella-triángulo
(⅓ de la corriente; relé a 0,58 × In). Cálculos: 400/√3 = 230,9 V; 1/√3 = 0,577."""
TIT = ("ASÍ SE CONECTA EN", "ESTRELLA O TRIÁNGULO")
GUION = {
    "gancho": "Abres la caja de bornes de un motor I E C y encuentras seis bornes y tres puentes. Según cómo los pongas, "
              "el mismo motor trabaja a doscientos treinta o a cuatrocientos voltios. Estrella o triángulo.",
    "p1": "Adentro hay tres bobinas, una por fase. Sus puntas llegan a la caja marcadas según la norma: arriba U uno, V uno y W uno, "
          "los inicios. Abajo W dos, U dos y V dos, los finales, corridos un lugar para que los puentes queden rectos.",
    "p2": "En estrella, los puentes van horizontales abajo y unen los tres finales en un punto común. Cada bobina queda entre una fase "
          "y ese punto, y recibe el voltaje de línea entre raíz de tres: con cuatrocientos voltios, cada bobina recibe doscientos treinta.",
    "p3": "En triángulo, los puentes van verticales: U uno con W dos, V uno con U dos y W uno con V dos. Cada bobina queda entre dos fases "
          "y recibe el voltaje de línea completo: doscientos treinta.",
    "p4": "Por eso la placa dice doscientos treinta en triángulo y cuatrocientos en estrella: las bobinas siempre ven doscientos treinta. "
          "Si lo conectas en triángulo a cuatrocientos, cada bobina recibe raíz de tres veces más, y el motor se quema.",
    "p5": "Y si el motor trabaja en triángulo a tu voltaje de red, puedes arrancarlo en estrella y pasarlo a triángulo. "
          "La corriente y el par de arranque bajan a un tercio. Cerca del ochenta por ciento de la velocidad, se cambia a triángulo.",
    "p6": "Para eso los seis bornes van libres, sin puentes, con tres contactores. Y el relé térmico se ajusta a cero punto cincuenta y ocho "
          "veces la corriente nominal, porque mide la corriente que pasa por las bobinas.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

"""V23 v2 · ¿Por qué el motor gira AL REVÉS? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v23_fuentes.md): Siemens "Motor rotation direction" (IEC 60034-8); WEG manual de instalación;
Fluke 9040 manual; Fluke "Don't run it backwards"; Britannica (construcción del motor de inducción); SEW (sentido de giro).
Cálculos: n = 120·f/p = 120·60/4 = 1800 rpm; placa Nidec U10P2D 1760 rpm → deslizamiento (1800−1760)/1800 = 2,2 %."""
TIT = ("ASÍ GIRA AL REVÉS", "UN MOTOR TRIFÁSICO")
GUION = {
    "gancho": "Conectas un motor trifásico, lo arrancas y gira al revés. La solución de campo es cambiar dos cables, "
              "cualquiera de los tres. Pero, ¿por qué funciona?",
    "p1": "Por dentro, el estator es un paquete de láminas de acero al silicio de medio milímetro, con ranuras. "
          "En las ranuras van tres bobinados de cobre, repartidos alrededor del núcleo, uno por fase. "
          "Y el rotor es una jaula: barras de aluminio unidas por dos anillos.",
    "p2": "Cada fase llega a su máximo en un momento distinto, separadas ciento veinte grados: primero L uno, "
          "luego L dos y luego L tres. Ese orden se llama secuencia de fases.",
    "p3": "Como los bobinados están repartidos y las corrientes llegan en orden, el campo magnético gira dentro del estator. "
          "A sesenta hercios, con cuatro polos, gira a mil ochocientas revoluciones por minuto. "
          "El rotor lo persigue un poco más lento: este motor gira a mil setecientas sesenta.",
    "p4": "Si intercambias dos fases, la secuencia queda uno, tres, dos, y el campo gira al revés. "
          "Si mueves las tres en orden, la secuencia no cambia. Por eso son dos, y solo dos.",
    "p5": "La norma I E C sesenta mil treinta y cuatro ocho lo deja claro: con L uno, L dos y L tres en U uno, V uno y W uno, "
          "el eje gira en sentido horario, visto desde el lado del eje.",
    "p6": "Y hay máquinas que no perdonan: un compresor de tornillo que gira al revés no bombea aceite y se destruye en segundos. "
          "Antes de acoplar, mide la secuencia con un indicador de rotación de fases, o arranca el motor sin carga y revisa el sentido.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

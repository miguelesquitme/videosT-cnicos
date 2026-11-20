"""Short V31b · ASÍ FUNCIONA UN VARIADOR DE FRECUENCIA (versión técnica, 1:30–3:30).

Fuentes verificadas (nov-2026):
- NEC 2020 430.122(A): conductores de alimentación del variador ≥ 125 % de la corriente nominal de ENTRADA del equipo
  de conversión (EC&M, "Stumped by the Code", Sec. 430.122(A)).
- Bus DC de un variador de 480 V ≈ 650–680 V DC (control.com, "DC Bus Fundamentals in Industrial Motor Drives").
  Rectificador de 6 pulsos: 1,35 × VLL ≈ 648 V con 480 V; con capacitores tiende al pico √2 × 480 ≈ 679 V.
- Precarga con resistencia y contactor/relé de bypass que cierra a un umbral de voltaje (control.com).
- Manuales de fabricantes: esperar el tiempo de la etiqueta de advertencia y medir el bus; el LED CHARGE se apaga
  debajo de ~50 V DC (manual de un fabricante, sección de seguridad).
- NEMA MG 1 Parte 31: motores para uso con inversor, aislamiento para pulsos de 1600 V pico (PG&E, "VFD Motor
  Insulation"); un motor de 460 V puede ver ~1200 V en bornes por onda reflejada.
- n_s = 120 f / p ; V/Hz constante: 460 V / 60 Hz = 7,67 V/Hz.
- Leyes de afinidad (bombas y ventiladores centrífugos): P ∝ n³ → 0,8³ = 0,512.
- IEC 61800-2 (sistemas de accionamiento de velocidad variable), IEC 61800-3 (EMC).
"""

TIT1 = "ASÍ FUNCIONA UN"
TIT2 = "VARIADOR DE FRECUENCIA"

GUION = {
    'gancho': 'Un motor de cuatro polos a sesenta hertz gira a unos mil setecientos cincuenta r p m, y no hay perilla que lo cambie. Para cambiar la velocidad hay que cambiar la frecuencia. Eso hace el variador. Veamos qué pasa adentro.',
    'ext': 'Por fuera: arriba, el teclado con pantalla, marcha, paro y potenciómetro. Abajo, la bornera de potencia: L uno, L dos y L tres de alimentación; U, V y W al motor; tierra, y los bornes del bus de directa y de la resistencia de frenado. Al lado, la bornera de control: entradas digitales, analógicas de cero a diez voltios y de cuatro a veinte miliamperios, y un relé de falla.',
    'bloques': 'Por dentro, el circuito de potencia tiene tres etapas: rectificador, bus de corriente directa e inversor.',
    'rect': 'Primero, el rectificador: un puente de seis diodos que convierte la trifásica en directa pulsante. Con cuatrocientos ochenta voltios de línea, el bus queda cerca de seiscientos cincuenta voltios de directa.',
    'precarga': 'Al energizar, los capacitores descargados se verían como un corto. Por eso entra una resistencia de precarga, y cuando el bus llega a su nivel, un relé la puentea.',
    'bus': 'El bus es un banco de capacitores electrolíticos que filtra el rizado y guarda energía; muchos equipos agregan un reactor de directa para bajar armónicos.',
    'seguridad': 'Ojo: esos capacitores quedan cargados aunque abras el interruptor. Respeta el tiempo de la etiqueta, espera que se apague el indicador de carga y mide entre más y menos con un multímetro categoría tres antes de meter mano.',
    'inversor': 'Ahora el corazón: el inversor. Seis I G B T en tres ramas, cada uno con su diodo de rueda libre. Los dos de una misma rama nunca conducen a la vez, porque cortocircuitarían el bus; por eso el control deja un tiempo muerto.',
    'pwm': 'Conmutan a la frecuencia portadora, entre dos y dieciséis kilohertz. Con modulación por ancho de pulso, el voltaje promedio dibuja una senoide, y la inductancia del motor deja la corriente casi senoidal.',
    'vhz': 'Si solo bajara la frecuencia, el motor se saturaría; por eso el variador baja también el voltaje. Un motor de cuatrocientos sesenta voltios y sesenta hertz trabaja a siete punto sesenta y siete voltios por hertz: a treinta hertz recibe unos doscientos treinta voltios y su sincronismo baja a novecientos r p m.',
    'rampa': 'Con arranque directo, el motor jala de seis a ocho veces su corriente nominal. Con variador arrancas en rampa, y la corriente queda limitada, típicamente al ciento cincuenta por ciento durante un minuto en servicio pesado.',
    'frenado': 'Al desacelerar una carga de mucha inercia, el motor regenera y el bus sube; si sube demasiado, falla por sobretensión. Para eso está el chopper de frenado, que descarga el exceso en una resistencia.',
    'campo': 'En campo, cuatro reglas. Conductores de alimentación al ciento veinticinco por ciento de la corriente de entrada, NEC cuatrocientos treinta punto ciento veintidós. Cable para variador apantallado, con la malla aterrizada en ambos extremos. Motor para inversor, NEMA eme ge uno parte treinta y uno. Y selecciona el variador por corriente de salida, no solo por caballos.',
    'dato': 'Y el dato que vende variadores: en una bomba centrífuga, la potencia va con el cubo de la velocidad. Al ochenta por ciento de velocidad consume más o menos la mitad.',
    'cierre': 'Si te sirvió, suscríbete y sígueme.',
}

TOTAL = sum(len(v) for v in GUION.values())

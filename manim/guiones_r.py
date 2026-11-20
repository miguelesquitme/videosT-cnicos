"""Reels técnicos de un solo concepto (19-nov-2026). Fuentes verificadas:
R1 inductivo: Turck "Operating Distance Considerations" (Sn, Sr 0,9–1,1 Sn, Su 0,81–1,21 Sn, Sa 0–0,81 Sn; blanco estándar
   acero dulce 1 mm, lado = diámetro de la cara o 3 Sn; factores: inox 0,60–1,00, latón 0,35–0,50, aluminio 0,35–0,50,
   cobre 0,25–0,45; histéresis < 15 % de Sr). IEC 60947-5-2. Baumer y Pepperl+Fuchs (principio: oscilador LC, ferrita, Foucault).
R2 capacitivo: Balluff "Basics capacitive sensors" (capacitor abierto en un oscilador RC; C = ε0·εr·F/S; pared ≤ 4 mm
   en sensores estándar; ajuste: girar a la izquierda hasta apagar, a la derecha hasta encender y 180° más; Sn con placa
   Fe 360 aterrizada de 1 mm). εr del agua ≈ 80, plásticos ≈ 2–4 (valores de tabla de constantes dieléctricas).
R3 óptico: ifm "Photoelectric sensors" (barrera: mayor alcance y margen de ganancia, ve a través de transparentes;
   retro polarizado: doble recorrido del haz, filtros polarizadores contra objetos brillantes; difuso: basta 2 % de la luz;
   supresión de fondo: triangulación, menos alcance).
R4 arranques: ZVEI "Start motors – conserve resources" (DOL 6–8 × In, IE3+ hasta 8–15 ×; Y-Δ par 1/3 y pico en la
   transición; arrancador suave: corriente máx. 300 % bombas/ventiladores/bandas, 350 % compresores, 400–450 % molinos).
   Par del motor de inducción ∝ V².
R5 relé: control.com "Contactors versus Relays" (relés < 10 A, sin cámaras apagachispas; contactores con cámaras y
   auxiliares); IEC 60947-5-1 (AC-15, DC-13); EN 50005 (contacto conmutado 11-12-14, bobina A1-A2).
"""

R = {
    "r1": ("ASÍ DETECTA METAL UN", "SENSOR INDUCTIVO", {
        "gancho": "Tienes un sensor inductivo de ocho milímetros. Con acero detecta a ocho. Con aluminio, a menos de cuatro. "
                  "¿Por qué? Te lo explico desde el principio físico.",
        "p1": "Adentro hay un oscilador conectado a una bobina con núcleo de ferrita, abierto hacia la cara del sensor. Esa "
              "bobina genera un campo magnético alterno de alta frecuencia que sale por el frente.",
        "p2": "Cuando entra un metal, el campo induce corrientes de Foucault en su superficie. Esas corrientes le roban "
              "energía al oscilador y la amplitud baja. Un comparador con histéresis detecta esa caída y conmuta la salida.",
        "p3": "Pero no todos los metales roban la misma energía. El acero dulce es la referencia: factor uno. El inoxidable "
              "queda entre cero punto seis y uno; el latón y el aluminio, entre cero punto treinta y cinco y cero punto "
              "cincuenta; el cobre, entre cero punto veinticinco y cero punto cuarenta y cinco.",
        "p4": "Y ojo con la ficha técnica: Sn es la distancia nominal, medida con una placa de acero de un milímetro. La "
              "distancia asegurada, Sa, es el ochenta y uno por ciento de Sn. Solo ahí garantiza la detección con "
              "tolerancias de fabricación, voltaje y temperatura.",
        "p4b": "Además, el blanco estándar es cuadrado, con lado igual al diámetro de la cara del sensor o a tres veces Sn, "
               "el que sea mayor. Si tu pieza es más pequeña que eso, la distancia de detección también baja.",
        "p5": "Regla de campo: multiplica Sn por cero punto ochenta y uno y por el factor del material. Sensor de ocho "
              "milímetros con aluminio, tomando cero punto cuatro: unos dos punto seis milímetros. Ahí montas el objetivo.",
        "cierre": "Si te sirvió, suscríbete y sígueme.",
    }),
    "r2": ("ASÍ DETECTA UN", "SENSOR CAPACITIVO", {
        "gancho": "Este sensor detecta el agua a través de la pared de un tanque de plástico, sin tocarla. No usa flotador. "
                  "Usa la constante dieléctrica.",
        "p1": "Su cara activa es un electrodo que forma un capacitor abierto con lo que tiene enfrente. Ese capacitor es "
              "parte de un oscilador R C. Mientras la capacitancia es baja, el oscilador no arranca.",
        "p2": "La capacitancia es épsilon cero, por épsilon r, por el área, entre la distancia. Si se acerca un material con "
              "épsilon r alto, la capacitancia sube, el oscilador arranca y la etapa de disparo conmuta la salida.",
        "p3": "Aquí está la clave: el agua tiene una constante dieléctrica de unos ochenta; los plásticos, de dos a cuatro. "
              "Por eso el sensor casi no ve la pared, pero sí el agua que está detrás. En un sensor estándar, la pared "
              "no debe pasar de cuatro milímetros.",
        "p3b": "La distancia nominal se mide con una placa metálica aterrizada; con otros materiales se corrige. Tomando el "
               "agua como referencia, el vidrio da entre cero punto cuatro y cero punto seis, y el PVC entre cero punto dos y "
               "casi cero punto cinco. Por eso un capacitivo ajustado para agua puede no ver un envase de vidrio vacío.",
        "p4": "Para ajustarlo, con el tanque lleno: gira el potenciómetro de sensibilidad a la izquierda hasta que la salida "
              "se apague, luego a la derecha hasta que encienda, y dale media vuelta más para compensar humedad y temperatura.",
        "p5": "Cuidado con dos cosas: si te pasas de sensibilidad, empieza a ver la pared o la espuma; y el producto pegado "
              "en la pared puede dejar la salida activada aunque el tanque esté vacío.",
        "cierre": "Si te sirvió, suscríbete y sígueme.",
    }),
    "r3": ("SENSOR ÓPTICO:", "¿CUÁL MODO USAR?", {
        "gancho": "Tres sensores ópticos, tres formas de ver. Elige mal y tu línea se para por una botella brillante.",
        "p1": "Barrera: emisor y receptor en carcasas separadas, uno frente al otro. Detecta cuando el objeto corta el haz. "
              "Tiene el mayor alcance y el mayor margen de ganancia, así que aguanta polvo y suciedad. Su contra: dos "
              "equipos que cablear y alinear, y puede ver a través de un objeto transparente.",
        "p2": "Retrorreflectivo: emisor y receptor en la misma carcasa, con un reflector prismático enfrente. El haz recorre "
              "el doble de camino. Con filtro polarizado distingue la luz del reflector del brillo de una lata o un empaque "
              "metalizado; sin filtro, ese brillo lo engaña.",
        "p3": "Difuso: no usa reflector; el mismo objeto devuelve la luz. Le basta un dos por ciento de la luz emitida para "
              "conmutar, por eso depende del color, el tamaño y el acabado: un objeto negro mate se detecta mucho más cerca "
              "que uno blanco.",
        "p4": "Si atrás hay una pared o una banda brillante, usa supresión de fondo: mide por triangulación y solo ve dentro "
              "de la distancia que ajustas, a cambio de menos alcance.",
        "p5": "Regla rápida: polvo y distancia, barrera. Un solo lado de la máquina y objetos brillantes, retro polarizado. "
              "Objetos cerca y sin espacio para reflector, difuso con supresión de fondo.",
        "p6": "Y antes de cablear, define la lógica: light on activa la salida cuando el receptor recibe luz; dark on, cuando "
              "deja de recibirla. En barrera y retro, para que la salida se active con el objeto presente, normalmente usas dark on.",
        "cierre": "Si te sirvió, suscríbete y sígueme.",
    }),
    "r4": ("ARRANQUE DE MOTORES:", "DIRECTO · ESTRELLA-DELTA · SUAVE", {
        "gancho": "Mismo motor, tres arranques y tres corrientes muy distintas. Esto es lo que ve la red en cada uno.",
        "p1": "Arranque directo: el contactor aplica el voltaje pleno. El motor jala de seis a ocho veces su corriente "
              "nominal, y uno de alta eficiencia puede pasar de ocho. El par de arranque es el máximo: acelera rápido, "
              "pero golpea la mecánica y provoca caída de tensión.",
        "p2": "Estrella-delta: arranca en estrella y cada devanado recibe el voltaje de línea entre raíz de tres. La "
              "corriente de línea y el par bajan a un tercio. Cerca de su velocidad, los contactores pasan a delta, y en "
              "esa transición hay un pico de corriente y un golpe de par. Necesitas un motor de seis puntas, conectado "
              "en delta a tu voltaje de línea.",
        "p3": "Arrancador suave: tiristores en antiparalelo recortan la onda y suben el voltaje en rampa. Como el par es "
              "proporcional al cuadrado del voltaje, el arranque es progresivo y sin golpes. Limitas la corriente según "
              "la carga, de tres a cuatro veces y media la nominal, y al terminar un contactor de bypass lo puentea.",
        "p3b": "Con números: un motor de diez caballos a cuatrocientos sesenta voltios tiene catorce amperios nominales. En "
               "directo puede pedir más de cien amperios; en estrella-delta, unos treinta y siete; con arrancador suave limitado "
               "a tres veces, cuarenta y dos.",
        "p4": "En resumen: directo, máximo par y máxima corriente. Estrella-delta, un tercio de corriente y un tercio de "
              "par, para cargas que arrancan en vacío. Suave, rampa ajustable para bombas, ventiladores y bandas. Y si "
              "necesitas variar la velocidad, eso ya es un variador.",
        "cierre": "Si te sirvió, suscríbete y sígueme.",
    }),
    "r5": ("¿QUÉ ES UN RELÉ?", "Y POR QUÉ NO ES UN CONTACTOR", {
        "gancho": "La salida de un PLC es de veinticuatro voltios y medio amperio. No puede mover una válvula de doscientos "
                  "treinta voltios. Para eso existe el relé.",
        "p1": "Un relé es un interruptor accionado por una bobina. Al energizar A uno y A dos, el electroimán atrae la "
              "armadura y mueve el contacto. En un relé de interfaz típico el contacto es conmutado: once es el común, "
              "doce el normalmente cerrado y catorce el normalmente abierto.",
        "p2": "Así el control queda aislado galvánicamente de la carga: veinticuatro voltios de directa en la bobina y "
              "doscientos treinta de alterna en el contacto. En la base vienen un LED y un diodo de rueda libre que se "
              "come el pico inductivo de la bobina al desenergizar.",
        "p3": "¿Y por qué no arrancar un motor con él? Porque sus contactos son de baja corriente, típicamente hasta unos "
              "diez amperios, y no tiene cámaras apagachispas. Se califica en categorías de control: AC quince y DC trece, "
              "según la IEC sesenta mil novecientos cuarenta y siete cinco uno. El contactor tiene polos de potencia en "
              "AC tres, cámaras de extinción y contactos auxiliares.",
        "p3b": "Un detalle de campo: si el módulo trae diodo, respeta la polaridad de la bobina, A uno positivo y A dos negativo. "
               "Si la inviertes, el diodo pone en corto la salida que lo alimenta.",
        "p4": "Regla de campo: el relé maneja señales y bobinas; el contactor maneja la potencia. El PLC activa el relé, el "
              "relé energiza la bobina del contactor y el contactor arranca el motor.",
        "cierre": "Si te sirvió, suscríbete y sígueme.",
    }),
}

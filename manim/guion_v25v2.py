"""V25 v2 · ¿Cómo funciona un FUSIBLE? (reel vertical, dibujo real; 23-nov).
Fuentes (referencias/v25_fuentes.md): Eaton Bussmann Fuseology (cuello restringido; varias secciones con falla; relleno que
forma fulgurita; < ¼ de ciclo; el fusible no debe exceder la capacidad del conductor); Ferraz Shawmut gG cilíndricos
(cerámica, casquillos plateados, arena; 10 × 38: Ø10,3 × 38); Mersen 10×38 gG (0,5–32 A, 400–690 V); AutomationDirect
(I²t); Electrokit (gG rango completo; aM solo cortocircuito, motores)."""
TIT = ("ASÍ FUNCIONA UN", "FUSIBLE POR DENTRO")
GUION = {
    "gancho": "Un fusible es un pedazo de metal que se derrite a propósito. Suena simple, pero por dentro está diseñado "
              "para abrir un cortocircuito en menos de un cuarto de ciclo. Vamos a abrir uno.",
    "p1": "Este es un fusible cilíndrico de diez por treinta y ocho milímetros, clase g G. Cuerpo de cerámica, "
          "y en los extremos dos casquillos plateados que hacen el contacto. Impreso: dieciséis amperios, quinientos voltios.",
    "p2": "Adentro hay una lámina metálica con partes más angostas, llamadas cuellos, y todo está lleno de arena. "
          "En los cuellos la sección es menor, la resistencia es mayor, y ahí se calienta primero.",
    "p3": "Con una sobrecarga, la lámina se calienta poco a poco, hasta que un cuello se funde y se abre. "
          "Puede tardar segundos o minutos: depende de la corriente al cuadrado por el tiempo, la I cuadrado t.",
    "p4": "Con un cortocircuito, varios cuellos se funden casi al mismo tiempo y se forman varios arcos. "
          "La arena absorbe el calor, se funde y forma un vidrio aislante llamado fulgurita, que obliga a la corriente a llegar a cero. "
          "Todo en menos de un cuarto de ciclo, antes de que la corriente llegue a su pico.",
    "p5": "La letra importa. g G protege contra sobrecarga y cortocircuito: es el de uso general, para cables. "
          "a M solo protege contra cortocircuito: se usa en motores, junto con un relé térmico.",
    "p6": "Y el error más peligroso: cambiarlo por uno más grande, o ponerle un alambre. El fusible protege al cable. "
          "Si lo puenteas, lo próximo en fundirse es el aislamiento dentro de la pared. Siempre reemplázalo por uno igual.",
    "cierre": "Si te sirvió, suscríbete y sígueme.",
}

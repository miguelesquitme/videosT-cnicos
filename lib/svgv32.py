"""V32 v2 · ¿ESTRELLA o TRIÁNGULO? Piezas reales.
Fuentes (referencias/v32_fuentes.md): IEC 60034-8 (marcado U1 V1 W1 / U2 V2 W2; vía Siemens "Motor rotation direction");
WEG manual de instalación (diagramas de conexión de 6 cables); Bitzer "Star-delta start" (corriente y par ≈ ⅓; el motor debe
poder trabajar en Δ a la tensión de red; seis puntas libres; 3 contactores; cambiar a Δ al 75–80 % de la velocidad);
Siemens SIRIUS combinaciones estrella-triángulo (corriente ⅓; relé ajustado a 0,58 × In; temporizador 1–20 s)."""
from svgv2 import pieza, sombra, T, R


def bobina(n1="U1", n2="U2"):
    """Bobina del estator: madeja de alambre esmaltado de cobre con su aislamiento y las dos puntas marcadas."""
    Wp, Hp = 420, 1000
    c, p = [], {}
    c.append(f'<path d="M210,40 V200" stroke="#151617" stroke-width="22"/><path d="M210,800 V960" stroke="#151617" stroke-width="22"/>')
    c.append(sombra(R(80, 200, 260, 600, "url(#gCobreH)"), "sCuerpo"))
    for y in range(206, 800, 14):
        c.append(f'<path d="M80,{y} Q210,{y + 10} 340,{y}" stroke="#8C4A1E" stroke-width="5" fill="none" opacity="0.8"/>')
    c.append(R(80, 200, 260, 30, "#E8DFC8") + R(80, 770, 260, 30, "#E8DFC8"))
    c.append(R(150, 10, 120, 50, "#FFFFFF") + T(210, 35, n1, 36, "#111", 900))
    c.append(R(150, 940, 120, 50, "#FFFFFF") + T(210, 965, n2, 36, "#111", 900))
    p["a"] = (210, 40)
    p["b"] = (210, 960)
    return pieza(Wp, Hp, 0.05, "".join(c), p)


def _caja(con):
    import svgref
    return svgref.caja_bornes("6", con, ancho_mm=110.0)


def _placa():
    import svgv28
    return svgv28.etiqueta(("Δ 230 V", "Y 400 V"), "MOTOR 3~ · IEC", 60.0)


CATALOGO = {"caja_d": lambda: _caja("delta"), "caja_y": lambda: _caja("estrella"), "caja_l": lambda: _caja("libre"),
            "bU": lambda: bobina("U1", "U2"), "bV": lambda: bobina("V1", "V2"), "bW": lambda: bobina("W1", "W2"), "placa": _placa}
GRUPOS = {14: ["caja_d", "caja_y", "caja_l"], 30: ["bU", "bV", "bW"], 12: ["placa"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

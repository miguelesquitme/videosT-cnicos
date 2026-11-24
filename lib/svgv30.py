"""V30 v2 · ¿Qué es un KILOVATIO HORA? Piezas reales.
Fuentes (referencias/v30_fuentes.md): Landis+Gyr FOCUS AX (forma 2S autocontenida, 120 / 240 V 60 Hz, Clase 200, LCD de 9 dígitos,
+kWh/−kWh/neto, ANSI C12.20 clase 0,5); aprobación Measurement Canada AE-1641 (LED de prueba infrarrojo a la derecha bajo el LCD,
pulsos proporcionales a la energía; registros kWh y kW); CPS Energy Meter Specifications; LBL Standby (espera 5–10 % del consumo
residencial; ejemplo 5 W); U.S. DOE (espera 5–10 %)."""
from svgv2 import pieza, sombra, T, R, logo, tornillo


def medidor(lectura="004215"):
    """Medidor de base (socket) forma 2S, vista de frente: base y aro de sello, tapa transparente, carátula con LCD,
    LED de prueba IR, placa de datos (CL200 · 240 V · 3 hilos · FM 2S) y ventana del sello."""
    Wp, Hp = 1000, 1060
    cx, cy = 500, 520
    c, p = [], {}
    # base de la caja y aro
    c.append(sombra(f'<circle cx="{cx}" cy="{cy}" r="480" fill="url(#gGalv)"/>', "sCuerpo"))
    c.append(f'<circle cx="{cx}" cy="{cy}" r="455" fill="none" stroke="#5E646B" stroke-width="10"/>')
    c.append(R(cx - 30, cy + 440, 60, 90, "url(#gAceroV)") + f'<circle cx="{cx}" cy="{cy + 500}" r="18" fill="#C62828"/>')  # sello
    # tapa transparente
    c.append(f'<circle cx="{cx}" cy="{cy}" r="420" fill="#DDE7EE" opacity="0.35"/>')
    # carátula
    c.append(f'<circle cx="{cx}" cy="{cy}" r="380" fill="#F4F5F2"/>')
    c.append(R(cx - 300, cy - 230, 600, 190, "#1B1F24"))
    c.append(R(cx - 285, cy - 215, 570, 160, "#A9B89A"))
    c.append(T(cx - 30, cy - 140, lectura, 108, "#1B1F24", 800, ls=4))
    c.append(T(cx + 250, cy - 70, "kWh", 34, "#1B1F24", 900))
    p["lcd"] = (cx, cy - 135)
    # LED IR de prueba (a la derecha bajo el LCD) y puerto óptico
    c.append(f'<circle cx="{cx + 200}" cy="{cy + 10}" r="20" fill="#5B1E2E"/>' + T(cx + 200, cy + 55, "TEST", 26, "#3A3F45", 800))
    c.append(f'<circle cx="{cx - 200}" cy="{cy + 20}" r="44" fill="#2A2D33"/><circle cx="{cx - 215}" cy="{cy + 20}" r="9" fill="#5B1E2E"/><circle cx="{cx - 185}" cy="{cy + 20}" r="9" fill="#111"/>')
    p["led"] = (cx + 200, cy + 10)
    # placa de datos
    c.append(R(cx - 260, cy + 110, 520, 170, "#E1E4E8"))
    filas = [("CL200", "240 V", "60 Hz"), ("3 HILOS", "FM 2S", "1Ø"), ("kWh", "ANSI C12.20", "")]
    for i, f in enumerate(filas):
        for j, t in enumerate(f):
            c.append(T(cx - 170 + j * 170, cy + 150 + i * 50, t, 30, "#1B1F24", 800))
    c.append(logo(cx - 45, cy + 300, 50))
    p["placa"] = (cx, cy + 195)
    # brillo de la tapa
    c.append(f'<path d="M{cx - 300},{cy - 280} C{cx - 200},{cy - 380} {cx},{cy - 410} {cx + 120},{cy - 400}" stroke="#FFFFFF" stroke-width="22" fill="none" opacity="0.5"/>')
    return pieza(Wp, Hp, 0.18, "".join(c), p)


def plancha():
    """Plancha de vapor vista de lado: suela de aluminio, depósito transparente, mango, perilla de temperatura y cordón;
    etiqueta 120 V~ 1200 W."""
    Wp, Hp = 1300, 700
    c, p = [], {}
    c.append(sombra('<path d="M60,560 C200,560 900,560 1180,520 L1240,600 H40 Z" fill="url(#gAluR)"/>', "sCuerpo"))
    c.append('<path d="M70,560 C300,420 700,300 1150,500 L1180,520 C900,560 200,560 70,560 Z" fill="#2A63B8"/>')
    c.append('<path d="M700,380 C850,250 1000,250 1100,330 L1150,500 C1000,380 850,370 700,380 Z" fill="#9FD3F2" opacity="0.7"/>')
    c.append(sombra('<path d="M300,420 C320,220 500,150 800,150 C950,150 1050,200 1080,300 L1000,320 C980,250 900,220 800,220 C560,220 420,280 390,400 Z" fill="#1E3F7A"/>'))
    c.append(f'<circle cx="560" cy="440" r="60" fill="url(#gAceroR)"/><rect x="555" y="390" width="10" height="40" fill="#1B1F24"/>')
    c.append('<path d="M60,520 C0,500 -10,420 40,400" stroke="#151515" stroke-width="22" fill="none"/>')
    c.append(R(760, 440, 260, 70, "#E6E8EA") + T(890, 475, "120 V~ 1200 W", 32, "#111", 900))
    p["etq"] = (890, 475)
    return pieza(Wp, Hp, 0.25, "".join(c), p)


def tele(encendida=True):
    """Televisor LED de pantalla plana con base, etiqueta 100 W."""
    Wp, Hp = 1400, 950
    c, p = [], {}
    c.append(sombra(R(0, 0, 1400, 800, "#111214"), "sCuerpo"))
    c.append(R(25, 25, 1350, 750, "#1F4A7A" if encendida else "#16181B"))
    if encendida:
        c.append('<path d="M25,500 C400,380 800,620 1375,420 V775 H25 Z" fill="#2F6FA8" opacity="0.8"/>')
    c.append(R(600, 800, 200, 80, "#2A2D33") + R(450, 880, 500, 40, "#2A2D33"))
    c.append(logo(660, 812, 40))
    c.append(R(1150, 700, 200, 60, "#E6E8EA") + T(1250, 730, "100 W", 34, "#111", 900))
    p["etq"] = (1250, 730)
    return pieza(Wp, Hp, 0.5, "".join(c), p)


def cargador():
    import svgv28
    return svgv28.cargador()


CATALOGO = {"medidor": lambda: medidor("004215"), "medidor2": lambda: medidor("004216"), "plancha": plancha,
            "tele": lambda: tele(True), "cargador": cargador}
GRUPOS = {6: ["medidor", "medidor2"], 3: ["plancha"], 2: ["tele"], 12: ["cargador"]}

if __name__ == "__main__":
    import sys
    from svgv2 import lote, hoja
    out = sys.argv[1]
    lote(CATALOGO, out, GRUPOS)
    print(hoja(out, out + "/_hoja.png"))

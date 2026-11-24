"""Diagrama de potencia H01 dibujado SÍMBOLO POR SÍMBOLO (vectores con trazo, no potrace) para editarlo en Canva.

Las medidas salen píxel a píxel de referencias/diagramas_h01/potencia_original.png (553 × 759); se dibuja en esas
coordenadas y un transform lo lleva al lugar que ocupa en el cuadro del video (1920 × 1080):
x_video = 1,25·x + 44,75 · y_video = 1,25·y + 95,75 (verificado con las cajas del volcado).
Los textos (bornes, designaciones, placa) NO se tocan: ya son texto editable en el volcado.

Uso:  python3 canva_diag.py entrada.svg salida.svg   (reemplaza el grupo VGroup_016 de potrace y une la cuadrícula)
"""
import re
import sys
import json

TR = "matrix(1.25,0,0,1.25,44.75,95.75)"
SW = 1.5            # grosor del trazo en px del original (≈ 1,6 px en el video)
NEG = "#000000"
FASES = (245, 275, 305)   # L3→1, L2→3, L1→5 (columnas de los polos)


def L(*pts):
    return "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)


def path(i, d, dash=False, fill="none", sw=SW):
    da = ' stroke-dasharray="3 3"' if dash else ""
    st = f' stroke="{NEG}" stroke-width="{sw}" stroke-linecap="butt" stroke-linejoin="miter"{da}' if sw else ""
    return f'<path id="{i}" d="{d}" fill="{fill}"{st}/>'


def circ(i, cx, cy, r, fill="none"):
    return f'<circle id="{i}" cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{NEG}" stroke-width="{SW}"/>'


def punto(i, cx, cy):
    return f'<circle id="{i}" cx="{cx}" cy="{cy}" r="2.6" fill="{NEG}"/>'


def grupo(i, *hijos):
    return f'<g id="{i}">' + "".join(hijos) + "</g>"


def tierra(i, x, y0):
    """Símbolo de tierra: tres rayas decrecientes (29 / 19 / 9 px) separadas 7 px, desde y0."""
    return path(i, L((x - 14.5, y0), (x + 14.5, y0)) + " " + L((x - 9.5, y0 + 7), (x + 9.5, y0 + 7)) + " " + L((x - 4.5, y0 + 14), (x + 4.5, y0 + 14)))


def diagrama():
    g = []
    # ---------------------------------------------------------------- -X0 barras de alimentación
    barras = []
    for nom, y in (("PE", 21), ("N", 51), ("L3", 81), ("L2", 111), ("L1", 141)):
        barras.append(grupo(f"X0_{nom}",
                            circ(f"X0_{nom}_borne_ent", 35, y, 4), circ(f"X0_{nom}_borne_sal", 95, y, 4),
                            path(f"X0_{nom}_puente", L((39, y), (91, y)), dash=False) if nom != "PE" else
                            path(f"X0_{nom}_puente", L((39, y), (52, y)) + " " + L((56, y), (91, y)), dash=False),
                            path(f"barra_{nom}", L((99, y), (514, y)), dash=(nom == "PE"))))
    g.append(grupo("sim_X0_barras", *barras))

    # ---------------------------------------------------------------- derivaciones de fase a -F2 (con su punto)
    der = []
    for nom, x, y in (("L3", 245, 81), ("L2", 275, 111), ("L1", 305, 141)):
        der.append(grupo(f"cond_{nom}_X0-F2", punto(f"pto_{nom}", x, y), path(f"lin_{nom}_X0-F2", L((x, y), (x, 246)))))
    g.append(grupo("conductores_X0-F2", *der))

    # ---------------------------------------------------------------- -F2 disyuntor 3P (polos 1-2 / 3-4 / 5-6)
    #   brazo móvil inclinado (230,246)→(245,275) + bloque de disparo girado + tope horizontal
    polos = []
    for k, x in enumerate(FASES):
        dx = x - 245
        tope = ((237, 247), (258, 272), (287, 297))[k]
        polos.append(grupo(f"F2_polo{k + 1}",
                           path(f"F2_p{k + 1}_brazo", L((230 + dx, 246), (245 + dx, 275))),
                           path(f"F2_p{k + 1}_tope", L((tope[0], 261), (tope[1], 261))),
                           f'<rect id="F2_p{k + 1}_disparo" x="{227 + dx}" y="{253.5}" width="9" height="9" fill="{NEG}" '
                           f'transform="rotate(-25 {231.5 + dx} 258)"/>'))
    g.append(grupo("sim_F2_disyuntor", *polos))

    g.append(grupo("conductores_F2-KM1", *[path(f"lin_F2-KM1_{k + 1}", L((x, 275), (x, 366))) for k, x in enumerate(FASES)]))

    # ---------------------------------------------------------------- -KM1 contactor (contactos principales NA)
    polos = []
    for k, x in enumerate(FASES):
        dx = x - 245
        tope = ((237, 247), (263, 272), (287, 297))[k]
        polos.append(grupo(f"KM1_polo{k + 1}",
                           path(f"KM1_p{k + 1}_brazo", L((230 + dx, 366), (245 + dx, 395))),
                           path(f"KM1_p{k + 1}_tope", L((tope[0], 381), (tope[1], 381)))))
    g.append(grupo("sim_KM1_contactor", *polos))

    g.append(grupo("conductores_KM1-F3", *[path(f"lin_KM1-F3_{k + 1}", L((x, 395), (x, 472))) for k, x in enumerate(FASES)]))

    # ---------------------------------------------------------------- -F3 relé térmico (caja + elemento por polo)
    elem = [path(f"F3_p{k + 1}_elemento", L((x, 471.5), (x, 478.5), (x + 15, 478.5), (x + 15, 494.5), (x, 494.5), (x, 501.5)))
            for k, x in enumerate(FASES)]
    g.append(grupo("sim_F3_rele_termico", path("F3_caja", L((238, 471.5), (327, 471.5), (327, 501.5), (238, 501.5)) + " Z"), *elem))

    g.append(grupo("conductores_F3-X1", *[path(f"lin_F3-X1_{k + 1}", L((x, 501.5), (x, 557))) for k, x in enumerate(FASES)]))

    # ---------------------------------------------------------------- -X1 bornes de salida al motor
    g.append(grupo("sim_X1_bornes", *[circ(f"X1_borne{k + 1}", x, 561, 4) for k, x in enumerate(FASES + (335,))]))

    # ---------------------------------------------------------------- -M1 motor trifásico + masa
    mot = [circ("M1_circulo", 275, 666, 44.5),
           path("M1_tilde", "M291,676 C294,671 297,670 300,673 C303,677 306,678 309,673"),
           path("M1_masa", L((323.5, 657.5), (323.5, 675)) + " " + L((326.5, 657.5), (326.5, 675)))]
    g.append(grupo("sim_M1_motor", *mot))
    g.append(grupo("conductores_X1-M1",
                   path("lin_X1-M1_T1", L((245, 565), (245, 632))),
                   path("lin_X1-M1_T2", L((275, 565), (275, 621.5))),
                   path("lin_X1-M1_T3", L((305, 565), (305, 633)))))

    # ---------------------------------------------------------------- PE (conductor de protección) y tierras
    g.append(grupo("cond_PE",
                   punto("pto_PE_1", 335, 21), punto("pto_PE_2", 440, 21),
                   path("lin_PE_barra-X1", L((335, 21), (335, 557)), dash=True),
                   path("lin_PE_X1-motor", L((335, 565), (335, 606)), dash=True),
                   path("lin_PE_motor", L((335, 606), (335, 666), (327, 666))),
                   punto("pto_PE_3", 335, 576),
                   path("lin_PE_a_tierra2", L((335, 576), (395, 576), (395, 588)), dash=True),
                   path("lin_PE_tierra2", L((395, 588), (395, 606))),
                   path("lin_PE_a_tierra1", L((440, 21), (440, 183)), dash=True),
                   path("lin_PE_tierra1", L((440, 183), (440, 201)))))
    g.append(grupo("sim_tierras", tierra("tierra_1", 440, 201), tierra("tierra_2", 395, 606)))
    return f'<g id="diagrama_potencia" transform="{TR}">' + "".join(g) + "</g>"


def una_cuadricula(svg):
    """Une las ~150 líneas de la cuadrícula del fondo (grupo VGroup_000) en un solo path."""
    m = re.search(r'<g id="VGroup_000">(.*?)</g>', svg, re.S)
    if not m:
        return svg
    ds = re.findall(r' d="([^"]*)"', m.group(1))
    attrs = re.search(r'<path [^>]*?(stroke="[^"]*" stroke-opacity="[^"]*" stroke-width="[^"]*")', m.group(1))
    st = attrs.group(1) if attrs else 'stroke="#C9CED6" stroke-width="1"'
    nuevo = f'<g id="cuadricula"><path id="cuadricula_fondo" d="{" ".join(ds)}" fill="none" {st}/></g>'
    return svg[:m.start()] + nuevo + svg[m.end():]


def aplicar(entrada, salida):
    s = open(entrada).read()
    m = re.search(r'<g id="VGroup_016">(.*?)</g>', s, re.S)
    cuerpo = m.group(1)
    # se quitan SOLO los paths de potrace del grupo; los textos se quedan
    textos = re.sub(r'<path [^>]*/>', "", cuerpo)
    s = s[:m.start()] + diagrama() + f'<g id="diagrama_potencia_textos">{textos}</g>' + s[m.end():]
    s = una_cuadricula(s)
    open(salida, "w").write(s)
    return salida


if __name__ == "__main__":
    aplicar(sys.argv[1], sys.argv[2])
    print(sys.argv[2])

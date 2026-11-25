"""Piezas del catálogo para las publicaciones (24-nov)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "lib"))
import svgref as G
from render_svg import render_lote, margen_de
DST = Path(__file__).resolve().parent / "eq"
lote = {
    "KM1": G.contactor("KM1"), "KM1on": G.contactor("KM1", on=True), "KM2": G.contactor("KM2"),
    "KM3": G.contactor("KM3"),
    "QB": G.disyuntor(n=1, In=16, curva="B", ref="F1", tension="230/400 VAC"),
    "QC": G.disyuntor(n=1, In=16, curva="C", ref="F2", tension="230/400 VAC"),
    "QD": G.disyuntor(n=1, In=16, curva="D", ref="F3", tension="230/400 VAC"),
    "QM1": G.guardamotor("QM1", (22, 32), 26.5, on=True),
    "F3": G.rele_termico("F3", (23, 32), 26.5), "F3tr": G.rele_termico("F3", (23, 32), 26.5, disparado=True),
    "KT1": G.temporizador("KT1", "SEC", tiempo=0.3, on=True),
    "S3": G.emergencia("S3"),
    "S1": G.pulsador("verde", "I", "S1", funcion="ARRANQUE"), "S0": G.pulsador("rojo", "O", "S0", funcion="PARO"),
    "H1": G.piloto("verde", "H1", encendido=True),
    "M1": G.motor("M1"),
    "CB9": G.caja_bornes("9", "bajo_y"),
    "PZ": G.pinza("26,4", "AC"), "PZ0": G.pinza("0,0", "AC"),
    "MM": G.multimetro("OL", "Ω", pos=5),
    "X0": G.bornera(("1", "2", "3", "4", "5"), {"4": "N", "5": "PE"}, "X0", paso_mm=10.2, pasos={"4": 5.2}, numeros=(1, 2, 3, 4, 5)),
}
render_lote([(n, v, margen_de(v[0])) for n, v in lote.items()], DST, px_mm=14)
print("ok", len(lote))

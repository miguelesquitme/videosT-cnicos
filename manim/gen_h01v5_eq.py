"""Equipos de H01 v5 (Correcciones del usuario 23-nov noche): bloques traseros y borneras rediseñados.
Copia el resto de h01v3_eq/ y rinde solo lo nuevo en h01v5_eq/."""
import shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
import svgref as G
from render_svg import render_lote, margen_de
SRC, DST = Path(__file__).parent / "h01v3_eq", Path(__file__).parent / "h01v5_eq"
DST.mkdir(exist_ok=True)
for f in SRC.iterdir():
    shutil.copy(f, DST / f.name)
lote = {
    "X0": G.bornera(("1", "2", "3", "4", "5"), {"4": "N", "5": "PE"}, "X0", paso_mm=10.2, pasos={"4": 5.2}, numeros=(1, 2, 3, 4, 5)),
    "X1": G.bornera(("1", "2", "3", "4"), {"4": "PE"}, "X1", paso_mm=10.2, numeros=(1, 2, 3, 4)),
    "S0b": G.bloque("1", "2", nc=True), "S1b": G.bloque("3", "4"),
    "H1b": G.bloque("X1", "X2", piloto=True), "H2b": G.bloque("X1", "X2", piloto=True),
    "H1bon": G.bloque("X1", "X2", piloto=True, estado="on_verde"), "H2bon": G.bloque("X1", "X2", piloto=True, estado="on_rojo"),
    "MMol": G.multimetro("OL", "Ω", pos=5), "MMol2": G.multimetro("OL", "Ω", pos=5),
}
render_lote([(n, v, margen_de(v[0])) for n, v in lote.items()], DST, px_mm=20)
print("ok", len(lote))

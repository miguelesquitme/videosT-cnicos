"""Piezas de los reels A01–A15 → arr_eq/ (copia de h01v5_eq + catálogo + svgarr)."""
import shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
import svgref as G, svgarr as A
from render_svg import render_lote, margen_de
SRC, DST = Path(__file__).parent / "h01v5_eq", Path(__file__).parent / "arr_eq"
DST.mkdir(exist_ok=True)
for f in SRC.iterdir():
    shutil.copy(f, DST / f.name)
lote = {
    "KM2": G.contactor("KM2"), "KM2on": G.contactor("KM2", on=True), "KM3": G.contactor("KM3"), "KM3on": G.contactor("KM3", on=True),
    "KT1": G.temporizador("KT1", "SEC", tiempo=0.3), "KT1on": G.temporizador("KT1", "SEC", tiempo=0.3, on=True),
    "QM1": G.guardamotor("QM1", (22, 32), 26.5), "QM1on": G.guardamotor("QM1", (22, 32), 26.5, on=True),
    "CBalto": G.caja_bornes("9", "alto"), "CBbajo": G.caja_bornes("9", "bajo_y"),
    "PZ0": G.pinza("0,0", "AC"), "PZ26": G.pinza("26,4", "AC"), "S3": G.emergencia("S3"),
    "MMv0": G.multimetro("0.0", "V~", pos=2), "MMol": G.multimetro("OL", "Ω", pos=5),
    "rc": A.rele_corte(False), "rc_tr": A.rele_corte(True),
    "bc": A.bobina_corte(False), "bc_on": A.bobina_corte(True),
    "pt_hilos": A.puntera("hilos"), "pt_azul": A.puntera("puntera", "#1E4FD8"), "pt_roja_p": A.puntera("puntera", "#D92D20", "#161616"),
    "pt_05": A.puntera("puntera", "#F4F4F2", "#161616", 60), "pt_075": A.puntera("puntera", "#9AA0A6", "#161616", 60),
    "pt_10": A.puntera("puntera", "#D92D20", "#161616", 60), "pt_15": A.puntera("puntera", "#1B1B1B", "#5A5A5A", 60),
    "pt_25": A.puntera("puntera", "#1E4FD8", "#161616", 60),
}
render_lote([(n, v, margen_de(v[0])) for n, v in lote.items()], DST, px_mm=16)
print("ok", len(lote))

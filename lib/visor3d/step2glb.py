"""STEP de fabricante → GLB con colores (pip install cascadio). Uso: python3 step2glb.py archivo.stp [salida.glb]"""
import sys, cascadio
src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + ".glb"
print(cascadio.step_to_glb(src, dst, tol_linear=0.02), dst)

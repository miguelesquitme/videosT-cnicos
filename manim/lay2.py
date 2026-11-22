"""Vista fija de revisión: equipos + todos los cables + diagramas (H01 v2)."""
from h01v2_lay import *
from h01v2_diag import diagrama_mando, diagrama_potencia
import os


class Lay2(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#000000"
        E = disposicion()
        placa = Rectangle(width=4.9, height=8.85, stroke_width=0).set_fill("#D9682F", 1).move_to([0.9, -0.05, 0])
        puerta = Rectangle(width=3.75, height=8.85, stroke_width=0).set_fill("#5B636D", 1).move_to([5.95, -0.05, 0])
        self.add(placa, puerta, *E.values())
        for _, hs, _ in hilos_mando(E):
            for pts, col, n, ta, tb, ka, kb in hs:
                self.add(Cable(pts, col, "mando", n, ta, tb, ka, kb))
        for kk, lst in hilos_potencia(E).items():
            for pts, col, n, ta, tb in lst:
                self.add(Cable(pts, col, "pot", n, ta, tb))
        H = (diagrama_mando if os.environ.get("D", "m") == "m" else diagrama_potencia)(alto=7.9, centro=(-4.55, -0.2))
        self.add(H.todo())
        z = os.environ.get("Z")
        if z:
            x, y, w = map(float, z.split(","))
            self.camera.frame.set(width=w).move_to([x, y, 0])

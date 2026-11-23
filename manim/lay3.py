"""Vista fija de revisión H01 v3: conexión didáctica + diagrama literal."""
import os
from h01v3_lay import *
from diag_lit import diagrama_mando, diagrama_potencia


class Lay3(MovingCameraScene):
    def construct(self):
        self.camera.background_color = FONDO
        self.add(rejilla())
        E = disposicion()
        self.add(riel_din(E), puerta_marco(E), *E.values())
        for _, cs, _ in hilos_mando(E):
            self.add(*cs)
        if os.environ.get("POT"):
            for lst in hilos_potencia(E).values():
                self.add(*lst)
        H = (diagrama_mando if os.environ.get("D", "m") == "m" else diagrama_potencia)(alto=7.9, centro=(-4.75, -0.25))
        self.add(H.todo())
        z = os.environ.get("Z")
        if z:
            x, y, w = map(float, z.split(","))
            self.camera.frame.set(width=w).move_to([x, y, 0])

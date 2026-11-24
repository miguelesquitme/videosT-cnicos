import os
os.environ.setdefault("TEMA", "gris")
from h01v3 import *
import h01v5_lay as L5
from diag_lit import diagrama_mando, diagrama_potencia

class Prueba(H01v3):
    def construct(self):
        E = L5.disposicion()
        modo = os.environ.get("MODO", "pot")
        if modo == "mando":
            H = diagrama_mando(alto=6.8, centro=(-4.75, -0.35))
        else:
            H = diagrama_potencia(alto=6.4, centro=(-4.7, -0.35))
        self.add(H.todo(), L5.riel_din(E), L5.puerta_marco(E))
        for n, e in E.items():
            if n in ("S0", "S1", "H1", "H2") and modo != "frente":
                continue
            self.add(e)
        if modo == "frente":
            return
        for _, c, _ in L5.hilos_mando(E):
            self.add(c)
        if modo == "pot":
            P = L5.hilos_potencia(E)
            for v in P.values():
                for c in v:
                    self.add(c)
            self.add(L5.red_entrada(E))
            mo = Eq3("M1", 0.0095)
            mo.img.move_to([5.2, -2.55, 0])
            self.add(mo, L5.manguera_tsj(E, mo))

"""Vuelca el cuadro de la sección 8 (conexión de potencia) de H01 v4 a SVG editable para Canva."""
import os
os.environ.setdefault("SOLO", "c_potencia")
from h01v3 import *  # noqa
from manim import FadeOut
from canva_dump import volcar


class Fin(Exception):
    pass


class DumpC8(H01v3):
    def voz(self, clave):
        self._clave = clave
        if clave == "p5":      # el cuadro del usuario (8:02): potencia completa, antes de la caja del motor
            self.volcar()
        return super().voz(clave)

    def volcar(self):
        if True:
            for c in self.cables:
                c.set_opacity(1)
            nombres = {id(v): k for k, v in self.E.items()}
            nombres[id(self.cables)] = "cables_mando"
            if hasattr(self, "cab_pot"):
                nombres[id(self.cab_pot)] = "cables_potencia"
            volcar(self, os.environ.get("SALIDA", "c8.svg"), nombres=nombres)
            raise Fin()

    def construct(self):
        try:
            super().construct()
        except Fin:
            pass

"""Miniatura / portada del video E06 · El contactor (1920x1080).
FORMATO=h manim -qh -s --disable_caching -o mini_e06 mini_e06.py MiniE06
"""
from comun_e import *
from miniaturas import fondo_azul, texto_gancho, sticker, logo_esq
from piezas_auto import riel_din, cable, C_POT
from piezas_auto2 import contactor_2d


class MiniE06b(MovingCameraScene):
    def construct(self):
        self.add(fondo_azul())
        x0 = 3.95
        glow = resplandor([x0, 0.0, 0], 3.4, "#2EC4DD", 14, 0.05)
        rl = riel_din(5.4, 1.9).move_to([x0, -0.2, 0])
        ct = contactor_2d(1.65, "18").move_to([x0, -0.2, 0])
        cs = VGroup(*[cable([ct.b[n].entrada.get_center(), ct.b[n].entrada.get_center() + UP * 3.0], C_POT, w=22, puntera=False) for n in ("1/L1", "3/L2", "5/L3")],
                    *[cable([ct.b[n].entrada.get_center(), ct.b[n].entrada.get_center() + DOWN * 3.0], C_POT, w=22, puntera=False) for n in ("2/T1", "4/T2", "6/T3")])
        self.add(glow, rl, cs, ct)
        txt = texto_gancho([("SELECCIONA EL", "#FFFFFF"), ("CONTACTOR", "#2EC4DD"), ("CORRECTO", "#FDB022")], 110)
        txt.scale_to_fit_width(7.6).move_to([-3.4, 1.35, 0])
        for sm in txt.family_members_with_points():
            sm.joint_type = LineJointType.ROUND
        def bloque_num(n, l1, l2, col):
            cu = RoundedRectangle(width=1.5, height=1.5, corner_radius=0.08, stroke_width=0).set_fill(col, 1)
            nn = T(n, 96, "#0B1C3D", "HEAVY").move_to(cu)
            tx_ = VGroup(T(l1, 40, "#0B1C3D", "HEAVY"), T(l2, 30, "#344054", "BOLD")).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            fondo = RoundedRectangle(width=tx_.width + 1.5 + 0.8, height=1.5, corner_radius=0.08, stroke_width=0).set_fill(WHITE, 1)
            fondo.align_to(cu, LEFT).align_to(cu, UP)
            tx_.next_to(cu, RIGHT, buff=0.32)
            return VGroup(fondo, cu, nn, tx_)
        sts = VGroup(bloque_num("7", "CRITERIOS", "de selección", "#FDB022"), bloque_num("2", "EJEMPLOS", "reales", "#16A34A")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        sts.next_to(txt, DOWN, buff=0.45).align_to(txt, LEFT)
        self.add(txt, sts)
        logo_esq(self, (6.95, -3.85))

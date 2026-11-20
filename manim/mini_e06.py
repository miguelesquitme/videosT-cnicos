"""Miniatura / portada del video E06 · El contactor (1920x1080).
FORMATO=h manim -qh -s --disable_caching -o mini_e06 mini_e06.py MiniE06
"""
from comun_e import *
from miniaturas import fondo_azul, texto_gancho, sticker, logo_esq
from piezas_auto import contactor_frente, riel_din, cable, cerrar_indicador, C_POT


class MiniE06(MovingCameraScene):
    def construct(self):
        self.add(fondo_azul())
        x0 = 3.95
        glow = resplandor([x0, 0.0, 0], 3.4, "#2EC4DD", 14, 0.05)
        rl = riel_din(5.4, 1.9).move_to([x0, -0.2, 0])
        ct = contactor_frente(1.95, "18").move_to([x0, -0.2, 0])
        cerrar_indicador(ct, True)
        cs = VGroup(*[cable([ct.b[n].entrada.get_center(), ct.b[n].entrada.get_center() + UP * 3.0], C_POT, w=22, puntera=False) for n in ("1/L1", "3/L2", "5/L3")],
                    *[cable([ct.b[n].entrada.get_center(), ct.b[n].entrada.get_center() + DOWN * 3.0], C_POT, w=22, puntera=False) for n in ("2/T1", "4/T2", "6/T3")])
        self.add(glow, rl, cs, ct)
        txt = texto_gancho([("EL MISMO", "#FFFFFF"), ("CONTACTOR", "#2EC4DD"), ("¿18 A o 32 A?", "#FDB022")], 110)
        txt.scale_to_fit_width(7.6).move_to([-3.4, 1.35, 0])
        for sm in txt.family_members_with_points():
            sm.joint_type = LineJointType.ROUND
        s1 = sticker("motor AC-3: 18 A", "#E5484D", size=40, ang=0.03)
        s2 = sticker("resistencias AC-1: 32 A", "#16A34A", size=40, ang=-0.03)
        sts = VGroup(s1, s2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(txt, DOWN, buff=0.45).align_to(txt, LEFT)
        self.add(txt, sts)
        logo_esq(self, (6.95, -3.85))

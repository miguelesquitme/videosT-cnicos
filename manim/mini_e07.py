"""Miniaturas H21 (disyuntor) y H22 (relé térmico), 1920x1080, sin marca."""
from comun_e import *
from miniaturas import fondo_azul, texto_gancho, logo_esq
from piezas_auto import riel_din, cable, C_POT
from piezas_auto2 import contactor_2d
from piezas_proteccion import breaker_din, breaker_on, rele_termico, ajustar_dial


def bloque_num(n, l1, l2, col):
    cu = RoundedRectangle(width=1.5, height=1.5, corner_radius=0.08, stroke_width=0).set_fill(col, 1)
    nn = T(n, 96, "#0B1C3D", "HEAVY").move_to(cu)
    tx_ = VGroup(T(l1, 40, "#0B1C3D", "HEAVY"), T(l2, 30, "#344054", "BOLD")).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    fondo = RoundedRectangle(width=tx_.width + 1.5 + 0.8, height=1.5, corner_radius=0.08, stroke_width=0).set_fill(WHITE, 1)
    fondo.align_to(cu, LEFT).align_to(cu, UP)
    tx_.next_to(cu, RIGHT, buff=0.32)
    return VGroup(fondo, cu, nn, tx_)


def textos(scene, lineas, n_crit):
    txt = texto_gancho(lineas, 110)
    txt.scale_to_fit_width(7.6).move_to([-3.4, 1.35, 0])
    for sm in txt.family_members_with_points():
        sm.joint_type = LineJointType.ROUND
    sts = VGroup(bloque_num(str(n_crit), "CRITERIOS", "de selección", "#FDB022"), bloque_num("2", "EJEMPLOS", "reales", "#16A34A")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    sts.next_to(txt, DOWN, buff=0.45).align_to(txt, LEFT)
    scene.add(txt, sts)
    logo_esq(scene, (6.95, -3.85))


class MiniE07(Scene):
    def construct(self):
        self.add(fondo_azul())
        x0 = 4.0
        self.add(resplandor([x0, 0.0, 0], 3.4, "#2EC4DD", 14, 0.05))
        rl = riel_din(5.4, 1.9).move_to([x0, -0.1, 0])
        bs = VGroup(breaker_on(breaker_din(1, 20, "C", s=1.05, tension="120/240 V~", ref="Q1")), breaker_on(breaker_din(2, 25, "C", s=1.05, tension="120/240 V~", ref="Q2"))).arrange(RIGHT, buff=0.0).move_to([x0, -0.1, 0])
        self.add(rl, bs)
        textos(self, [("SELECCIONA EL", "#FFFFFF"), ("DISYUNTOR", "#2EC4DD"), ("CORRECTO", "#FDB022")], 6)


class MiniE08(Scene):
    def construct(self):
        self.add(fondo_azul())
        x0 = 4.0
        self.add(resplandor([x0, 0.0, 0], 3.4, "#2EC4DD", 14, 0.05))
        r = rele_termico(1.7, (12, 18), "F2", "10A").move_to([x0, -0.2, 0])
        if r.height > 6.6:
            r.scale_to_fit_height(6.6)
        self.add(r)
        textos(self, [("AJUSTA EL", "#FFFFFF"), ("RELÉ TÉRMICO", "#2EC4DD"), ("CORRECTO", "#FDB022")], 6)

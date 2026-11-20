from piezas_auto import *
class Prueba(MovingCameraScene):
    def construct(self):
        fondo_degradado(self) if 'fondo_degradado' in globals() else None
        rl = riel_din(7, 1.0).move_to([-3.5, 0, 0])
        ct = contactor_frente(1.0).move_to([-4.5, 0.2, 0])
        self.add(rl, ct)
        for k, (n, lab) in enumerate((("1/L1", "L1"), ("3/L2", "L2"), ("5/L3", "L3"))):
            p = ct.b[n].tor.get_center()
            self.add(cable([p + UP*0.05, p + UP * 1.6, p + UP * 1.6 + RIGHT * 0.8, p + UP*2.6 + RIGHT*0.8], C_POT, etiqueta=lab))
        p = ct.b["A1"].tor.get_center()
        self.add(cable([p, p + RIGHT * 1.4, p + RIGHT*1.4 + UP*1.0], C_MANDO, w=7, etiqueta="A1"))
        # despiece
        parts = VGroup(camara_apaga(), VGroup(contacto_fijo(-1), contacto_fijo(1), puente_movil()), portacontactos(), armadura_T(),
                       resorte(), bobina(), nucleo_E(), base_contactor()).arrange(DOWN, buff=0.12).scale(0.55).move_to([0.6, 0, 0])
        self.add(parts)
        # símbolos
        s = VGroup(sim_bobina(), sim_contacto(True, contactor=True, n1="1", n2="2"), sim_contacto(True, n1="13", n2="14"),
                   sim_contacto(False, n1="21", n2="22"), sim_pulsador(True, ref="S2", n1="13", n2="14"), sim_pulsador(False, ref="S1", n1="11", n2="12"),
                   sim_termico_contacto(), sim_motor(), sim_termico_pot(), sim_contacto(True, interruptor=True, n1="1", n2="2")).arrange_in_grid(2, 5, buff=0.6).move_to([5.0, 0, 0]).scale(0.8)
        self.add(s)

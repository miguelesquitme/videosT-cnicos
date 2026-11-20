"""Base de los reels técnicos de un solo concepto (19-nov-2026): título fijo arriba en banda opaca, chip de sección,
zoom de calidad, corriente animada y cierre. Temas: blanco o negro (paletas de alto contraste)."""
from shorts_c import *  # noqa
import shorts_v
from piezas_auto2 import carta as _carta, etiqueta as _etiqueta

TEMAS = {
    "blanco": dict(fondo="#FFFFFF", banda="#FFFFFF", linea="#0057B8", t1="#101828", t2="#0057B8", txt="#101828", txt2="#475467",
                   chip_box="#101828", chip_txt="#FFFFFF", ac=["#0057B8", "#C2410C", "#047857", "#B42318", "#7C3AED"], ejes="#98A2B3",
                   grid="#EEF2F7"),
    "negro": dict(fondo="#000000", banda="#000000", linea="#00E5FF", t1="#FFFFFF", t2="#00E5FF", txt="#FFFFFF", txt2="#B8C0CC",
                  chip_box="#16181D", chip_txt="#FFFFFF", ac=["#00E5FF", "#FFB020", "#39FF88", "#FF4D6D", "#C084FC"], ejes="#5B6472",
                  grid="#0D0F14"),
}


class ReelTec(ShortC):
    TEMA = "blanco"
    CLAVE = ""
    TIT1 = ""
    TIT2 = ""

    def construct(self):
        th = self.th = TEMAS[self.TEMA]
        W, H = 9.2, 16.4
        self.add(Rectangle(width=W, height=H, stroke_width=0).set_fill(th["fondo"], 1).set_z_index(-100))
        rej = VGroup(*[Line([x, -8.2, 0], [x, 8.2, 0]) for x in np.arange(-4.5, 4.6, 0.5)],
                     *[Line([-4.6, y, 0], [4.6, y, 0]) for y in np.arange(-8, 8.1, 0.5)]).set_stroke(th["grid"], 1.2).set_z_index(-99)
        self.add(rej)
        banda = Rectangle(width=W, height=3.55, stroke_width=0).set_fill(th["banda"], 1).move_to([0, 6.3, 0])
        linea = Line([-4.6, 4.53, 0], [4.6, 4.53, 0]).set_stroke(th["linea"], 5)
        t1 = T(self.TIT1, 42, th["t1"], "HEAVY")
        t2 = T(self.TIT2, 64, th["t2"], "HEAVY")
        tt = VGroup(t1, t2).arrange(DOWN, buff=0.12).move_to([0, 5.55, 0])
        for m in tt:
            if m.width > 8.3:
                m.scale_to_fit_width(8.3)
        self.marco = VGroup(banda, linea, tt).set_z_index(50)
        self.add(self.marco)
        self.chip_act = None
        self.cuerpo()
        resto = DUR_MIN - self.renderer.time
        if resto > 0:
            self.wait(resto)

    # utilidades
    def ac(self, i):
        return self.th["ac"][i]

    def tx(self, texto, size=30, color=None, peso="BOLD"):
        return T(texto, size, color or self.th["txt"], peso)

    def card(self, titulo, lineas=(), color=None, w=7.8, size=28):
        m = _carta(titulo, lineas, color or self.ac(0), w, size)
        if self.TEMA == "blanco":
            sombra = m[0].copy().set_fill("#101828", 0.10).set_stroke(width=0).shift(RIGHT * 0.06 + DOWN * 0.06)
            borde = m[0].copy().set_fill(opacity=0).set_stroke("#D0D5DD", 1.5)
            m = VGroup(sombra, m, borde)
        return m.scale_to_fit_width(8.4) if m.width > 8.4 else m

    def tag(self, texto, color=None, size=28):
        m = _etiqueta(texto, color or self.ac(0), size)
        return m.scale_to_fit_width(8.4) if m.width > 8.4 else m

    def chip(self, num, texto, color=None):
        th = self.th
        color = color or self.ac(0)
        n = VGroup(Square(0.62, stroke_width=0).set_fill(color, 1), T(num, 30, "#FFFFFF" if self.TEMA == "blanco" else "#000000", "HEAVY"))
        t = T(texto, 30, th["chip_txt"], "HEAVY")
        caja = RoundedRectangle(width=t.width + 0.5, height=0.62, corner_radius=0.04, stroke_width=0).set_fill(th["chip_box"], 1)
        t.move_to(caja)
        g = VGroup(n, VGroup(caja, t)).arrange(RIGHT, buff=0).move_to([0, 4.0, 0]).align_to([-4.2, 0, 0], LEFT).set_z_index(49)
        anim = [FadeIn(g, shift=RIGHT * 0.3)]
        if self.chip_act is not None:
            anim.append(FadeOut(self.chip_act, shift=LEFT * 0.3))
        self.play(*anim, run_time=0.35)
        self.chip_act = g

    def quitar_chip(self):
        if self.chip_act is not None:
            self.play(FadeOut(self.chip_act), run_time=0.25)
            self.chip_act = None

    def zoom(self, mob, punto, factor, destino, rt=1.0):
        punto = np.array(punto, float)
        self.play(mob.animate.scale(factor, about_point=punto).shift(np.array(destino, float) - punto), run_time=rt, rate_func=smooth)

    def zoom_a(self, mob, sub, ancho, destino, rt=1.0, marco=True):
        f = ancho / sub.width
        if marco:
            r = SurroundingRectangle(sub, color=self.ac(0), buff=0.06, corner_radius=0.04, stroke_width=4)
            self.play(Create(r), run_time=0.3)
            mob.add(r)
        self.zoom(mob, sub.get_center(), f, destino, rt)
        if marco:
            self.play(FadeOut(r), run_time=0.2)
            mob.remove(r)

    def flujo(self, pts, color=None, vel=2.2, esc=1.4):
        c = corriente([np.array(p, float) for p in pts], vel=vel, escala=esc, color=color or self.ac(1))
        self.add(c)
        return c

    def ejes(self, x_len=7.6, y_len=2.6, xr=(0, 1, 0.25), yr=(-1.2, 1.2, 1), ticks=False, **kw):
        return Axes(x_range=list(xr), y_range=list(yr), x_length=x_len, y_length=y_len, tips=False,
                    axis_config={"color": self.th["ejes"], "stroke_width": 2.5, "include_ticks": ticks, **kw})

    def leyenda(self, texto, destino, desde, color=None, size=24, lado=RIGHT):
        """Etiqueta con línea guía hacia un punto."""
        t = self.tag(texto, color, size).move_to(desde)
        ln = Line(t.get_edge_center(-lado) if lado is not None else t.get_center(), destino).set_stroke(color or self.ac(0), 3)
        pt = Dot(destino, radius=0.06, color=color or self.ac(0))
        return VGroup(ln, pt, t)

"""Exporta el estado de una escena de Manim a SVG EDITABLE (para Canva): cada VMobject = un <path> con id,
cada Text = un <text> real (Inter), cada ImageMobject = un <image> PNG incrustado. Agrupa por equipo/cable/símbolo
cuando el objeto trae .nombre (o por el mobject de nivel superior). También guarda un JSON con el inventario de
elementos (id, tipo, caja en px, color, texto) que sirve de BASE para detectar qué cambió el usuario en Canva.

Uso:  from canva_dump import volcar ;  volcar(scene, "salida.svg")
"""
import base64
import io
import json
import numpy as np
from manim import VMobject, ImageMobject, Text, MarkupText, Paragraph, config, Group, VGroup, Mobject
from PIL import Image

PX = config.pixel_width / config.frame_width if config.pixel_width else 135.0


def _xy(p, W, H, fw, fh):
    return ((p[0] + fw / 2) * W / fw, (fh / 2 - p[1]) * H / fh)


def _hex(c):
    try:
        return c.to_hex()[:7]
    except Exception:
        return "#000000"


class Volcador:
    def __init__(self, W=1920, H=1080, fw=None, fh=None):
        self.W, self.H = W, H
        self.fw = fw or config.frame_width
        self.fh = fh or config.frame_height
        self.k = W / self.fw
        self.out, self.inv, self.n = [], [], 0

    def xy(self, p):
        return _xy(p, self.W, self.H, self.fw, self.fh)

    def nid(self, pref):
        self.n += 1
        return f"{pref}{self.n:04d}"

    # ---------------------------------------------------------------- piezas
    def texto(self, m, grupo):
        op = m.get_fill_opacity() if hasattr(m, "get_fill_opacity") else 1
        if op < 0.02:
            return
        em_px = (m.font_size / 48.0) * (0.485 / 0.727) * self.k
        x0, y0 = self.xy(m.get_corner(np.array([-1, 1, 0])))
        x1, y1 = self.xy(m.get_corner(np.array([1, -1, 0])))
        ang = 0.0
        txt = getattr(m, "original_text", None) or getattr(m, "text", "")
        txt = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        col = _hex(m.get_fill_color())
        peso = 800
        i = self.nid("T")
        w, h = x1 - x0, y1 - y0
        rot = len(txt.strip()) >= 2 and h > w * 1.15 and "\n" not in txt
        if rot:   # texto girado 90° (se lee de abajo hacia arriba)
            xb = x0 + 0.727 * em_px
            self.out.append(f'<text id="{i}" data-grupo="{grupo}" x="0" y="0" transform="translate({xb:.1f},{y1:.1f}) rotate(-90)" '
                            f'font-family="Inter" font-weight="{peso}" font-size="{em_px:.1f}" fill="{col}" fill-opacity="{op:.2f}" '
                            f'textLength="{h:.1f}" lengthAdjust="spacingAndGlyphs">{txt}</text>')
        else:
            yb = y0 + 0.727 * em_px
            self.out.append(f'<text id="{i}" data-grupo="{grupo}" x="{x0:.1f}" y="{yb:.1f}" font-family="Inter" font-weight="{peso}" '
                            f'font-size="{em_px:.1f}" fill="{col}" fill-opacity="{op:.2f}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{txt}</text>')
        self.inv.append({"id": i, "tipo": "texto", "grupo": grupo, "texto": txt, "caja": [round(x0), round(y0), round(x1), round(y1)], "color": col})

    def imagen(self, m, grupo):
        arr = m.get_pixel_array()
        if arr is None:
            return
        op = getattr(m, "opacity", 1) if not callable(getattr(m, "opacity", None)) else 1
        ul = self.xy(m.get_corner(np.array([-1, 1, 0])))
        dr = self.xy(m.get_corner(np.array([1, -1, 0])))
        im = Image.fromarray(np.asarray(arr).astype(np.uint8))
        b = io.BytesIO()
        im.save(b, "PNG", optimize=True)
        i = self.nid("I")
        self.out.append(f'<image id="{i}" data-grupo="{grupo}" x="{ul[0]:.1f}" y="{ul[1]:.1f}" width="{dr[0] - ul[0]:.1f}" '
                        f'height="{dr[1] - ul[1]:.1f}" preserveAspectRatio="none" '
                        f'href="data:image/png;base64,{base64.b64encode(b.getvalue()).decode()}"/>')
        self.inv.append({"id": i, "tipo": "imagen", "grupo": grupo, "caja": [round(ul[0]), round(ul[1]), round(dr[0]), round(dr[1])]})

    def trazo(self, m, grupo):
        pts = m.points
        if len(pts) < 2:
            return
        fo = float(m.get_fill_opacity())
        so = float(m.get_stroke_opacity())
        sw = float(m.get_stroke_width())
        if fo < 0.01 and (so < 0.01 or sw <= 0):
            return
        d = []
        for sp in m.get_subpaths():
            if len(sp) < 4:
                continue
            p0 = self.xy(sp[0])
            d.append(f"M{p0[0]:.1f},{p0[1]:.1f}")
            for j in range(0, len(sp) - 3, 4):
                a, b, c = self.xy(sp[j + 1]), self.xy(sp[j + 2]), self.xy(sp[j + 3])
                d.append(f"C{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}")
            if np.allclose(sp[0], sp[-1]):
                d.append("Z")
        if not d:
            return
        fill = f'fill="{_hex(m.get_fill_color())}" fill-opacity="{fo:.2f}"' if fo >= 0.01 else 'fill="none"'
        stroke = (f'stroke="{_hex(m.get_stroke_color())}" stroke-opacity="{so:.2f}" stroke-width="{sw * 0.01 * self.k:.2f}" '
                  f'stroke-linecap="round" stroke-linejoin="round"') if so >= 0.01 and sw > 0 else ""
        i = self.nid("P")
        self.out.append(f'<path id="{i}" data-grupo="{grupo}" d="{" ".join(d)}" {fill} {stroke} fill-rule="evenodd"/>')
        x0, y0 = self.xy(m.get_corner(np.array([-1, 1, 0])))
        x1, y1 = self.xy(m.get_corner(np.array([1, -1, 0])))
        self.inv.append({"id": i, "tipo": "trazo", "grupo": grupo, "caja": [round(x0), round(y0), round(x1), round(y1)],
                         "relleno": _hex(m.get_fill_color()) if fo >= 0.01 else None, "linea": _hex(m.get_stroke_color()) if sw > 0 and so > 0.01 else None})

    # ---------------------------------------------------------------- recorrido
    def recorrer(self, m, grupo):
        if isinstance(m, (Text, MarkupText)):
            self.texto(m, grupo)
            return
        if isinstance(m, Paragraph):
            for s in m.submobjects:
                self.recorrer(s, grupo)
            return
        if isinstance(m, ImageMobject):
            self.imagen(m, grupo)
            return
        if isinstance(m, VMobject) and len(m.points) > 0:
            self.trazo(m, grupo)
        for s in m.submobjects:
            self.recorrer(s, grupo)

    def escena(self, mobjects, fondo="#E4E7EB", nombres=None):
        nombres = nombres or {}
        self.out.append(f'<rect id="fondo" x="0" y="0" width="{self.W}" height="{self.H}" fill="{fondo}"/>')
        orden = sorted(enumerate(mobjects), key=lambda t: (getattr(t[1], "z_index", 0), t[0]))
        for k, (_, m) in enumerate(orden):
            g = nombres.get(id(m)) or getattr(m, "nombre", None) or f"{type(m).__name__}_{k:03d}"
            self.out.append(f'<g id="{g}">')
            self.recorrer(m, g)
            self.out.append("</g>")

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.W}" height="{self.H}" '
                f'viewBox="0 0 {self.W} {self.H}">' + "\n".join(self.out) + "</svg>")


def volcar(scene, ruta, fondo="#E4E7EB", nombres=None):
    v = Volcador()
    v.escena(scene.mobjects, fondo, nombres)
    open(ruta, "w").write(v.svg())
    json.dump(v.inv, open(str(ruta).replace(".svg", "_base.json"), "w"), ensure_ascii=False, indent=0)
    return ruta

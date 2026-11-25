"""Convierte un elemento QElectroTech (.elmt) a SVG (líneas, rect, elipse, círculo, arco, polígono, texto)."""
import sys, math, re, xml.etree.ElementTree as ET
def st(e):
    s = dict(kv.split(":", 1) for kv in (e.get("style") or "").split(";") if ":" in kv)
    col = {"black": "#111", "white": "#fff", "red": "#d00", "green": "#080", "blue": "#00c", "gray": "#888", "brun": "#8b4513", "yellow": "#e6c200", "cyan": "#0aa", "magenta": "#c0c", "lightgray": "#ccc", "orange": "#f80", "purple": "#808", "none": "none"}
    c = col.get(s.get("color", "black"), s.get("color", "#111"))
    fill = col.get(s.get("filling", "none"), "none") if not s.get("filling", "none").startswith("hor") else "none"
    w = {"none": 0.5, "thin": 0.5, "normal": 1, "hight": 2, "eleve": 3}.get(s.get("line-weight", "normal"), 1)
    dash = ' stroke-dasharray="3 2"' if s.get("line-style") in ("dashed", "dotted", "dashdotted") else ""
    return f'stroke="{c}" stroke-width="{w}" fill="{fill}"{dash}'
def conv(path, lang="es"):
    r = ET.parse(path).getroot()
    W, H = float(r.get("width")), float(r.get("height")); hx, hy = float(r.get("hotspot_x")), float(r.get("hotspot_y"))
    name = ""
    for n in r.iter("name"):
        if n.get("lang") in (lang, "en") and (not name or n.get("lang") == lang): name = n.text or ""
    out = []
    d = r.find("description")
    for e in (d if d is not None else []):
        t = e.tag
        if t == "line": out.append(f'<line x1="{e.get("x1")}" y1="{e.get("y1")}" x2="{e.get("x2")}" y2="{e.get("y2")}" {st(e)}/>')
        elif t == "rect": out.append(f'<rect x="{e.get("x")}" y="{e.get("y")}" width="{e.get("width")}" height="{e.get("height")}" rx="{e.get("rx", 0)}" {st(e)}/>')
        elif t == "ellipse":
            x, y, w, h = (float(e.get(k)) for k in ("x", "y", "width", "height"))
            out.append(f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" {st(e)}/>')
        elif t == "circle":
            x, y, dm = (float(e.get(k)) for k in ("x", "y", "diameter"))
            out.append(f'<circle cx="{x + dm / 2}" cy="{y + dm / 2}" r="{dm / 2}" {st(e)}/>')
        elif t == "arc":
            x, y, w, h = (float(e.get(k)) for k in ("x", "y", "width", "height")); a0, sw = float(e.get("start")), float(e.get("angle"))
            cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
            p = lambda a: (cx + rx * math.cos(math.radians(a)), cy - ry * math.sin(math.radians(a)))
            (x0, y0), (x1, y1) = p(a0), p(a0 + sw)
            out.append(f'<path d="M{x0:.2f},{y0:.2f} A{rx},{ry} 0 {1 if abs(sw) > 180 else 0} {0 if sw > 0 else 1} {x1:.2f},{y1:.2f}" {st(e)}/>')
        elif t == "polygon":
            pts, i = [], 1
            while e.get(f"x{i}") is not None: pts.append(f'{e.get(f"x{i}")},{e.get(f"y{i}")}'); i += 1
            tag = "polyline" if e.get("closed") == "false" else "polygon"
            out.append(f'<{tag} points="{" ".join(pts)}" {st(e)}/>')
        elif t == "text":
            sz = re.search(r",(\d+(?:\.\d+)?),", e.get("font") or "") ; sz = sz.group(1) if sz else e.get("size", "9")
            out.append(f'<text x="{e.get("x")}" y="{e.get("y")}" font-family="Arial" font-size="{sz}" fill="#111">{(e.get("text") or "").replace("&", "&amp;").replace("<", "&lt;")}</text>')
        elif t == "terminal":
            out.append(f'<circle cx="{e.get("x")}" cy="{e.get("y")}" r="1.6" fill="#d33"/>')
    return name, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-hx - 2} {-hy - 2} {W + 4} {H + 4}" width="{(W + 4) * 3}" height="{(H + 4) * 3}">{"".join(out)}</svg>'
if __name__ == "__main__":
    print(conv(sys.argv[1])[1])

"""Rasteriza los SVG de svgeq.py a PNG transparente de alta resolución con Chromium (Playwright).
Guarda también <nombre>.json con el tamaño en mm, el margen y los bornes (mm) para ubicarlos en Manim."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

PX_MM = 24  # resolución: 24 px por mm (un contactor de 45 mm = 1080 px de ancho)


def render_lote(lote, salida, px_mm=PX_MM):
    """lote: lista de (nombre, (svg, bornes, (W, H)), margen)."""
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(device_scale_factor=1)
        for nombre, (svg, bornes, (W, H)), margen in lote:
            wpx = int(round((W + 2 * margen) * px_mm))
            hpx = int(round((H + 2 * margen) * px_mm))
            import re
            svg2 = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', f'width="{wpx}" height="{hpx}"', svg, count=1)
            pag.set_viewport_size({"width": wpx, "height": hpx})
            pag.set_content(f'<html><body style="margin:0;background:transparent">{svg2}</body></html>')
            pag.wait_for_timeout(50)
            pag.screenshot(path=str(salida / f"{nombre}.png"), omit_background=True, clip={"x": 0, "y": 0, "width": wpx, "height": hpx})
            (salida / f"{nombre}.json").write_text(json.dumps({"W": W, "H": H, "margen": margen, "px_mm": px_mm, "bornes": bornes}))
        nav.close()


def margen_de(svg):
    import re
    m = re.search(r'viewBox="(-?[\d.]+)', svg)
    return -float(m.group(1))

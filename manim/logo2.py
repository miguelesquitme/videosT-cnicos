"""Logo ME. sin círculo (letras) y marcas de agua nuevas."""
from PIL import Image, ImageDraw, ImageFont
F = "/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf"
FI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"


def letras(alto=400, cM=(205, 235, 242), cE=(14, 155, 181)):
    f = ImageFont.truetype(F, alto)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    wM, wE, wP = (tmp.textlength(t, font=f) for t in ("M", "E", "."))
    W = int((wM + wE + wP) * 0.93) + 20
    im = Image.new("RGBA", (W, int(alto * 1.05)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = im.height / 2
    d.text((10, y), "M", font=f, fill=cM + (255,), anchor="lm")
    d.text((10 + wM * 0.93, y), "E", font=f, fill=cE + (255,), anchor="lm")
    d.text((10 + (wM + wE) * 0.93, y), ".", font=f, fill=cE + (255,), anchor="lm")
    return im.crop(im.getbbox())


letras().save("logo_letras.png")  # colores originales (para tarjetas)
# para marca de agua sobre fondo blanco, la M un poco más intensa para que se lea
L = letras(400, (120, 196, 216), (14, 155, 181))


def tag(txt, size, color=(14, 120, 145)):
    f = ImageFont.truetype(FI, size)
    l, t, r, b = f.getbbox(txt)
    im = Image.new("RGBA", (r - l + 16, b - t + 12), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((8 - l, 6 - t), txt, font=f, fill=color + (255,))
    return im


def con_opacidad(img, op):
    a = img.split()[3].point(lambda v: int(v * op))
    img.putalpha(a)
    return img


# vertical: logo + @ en vertical, más grande y más adentro, más transparente
img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
lg = L.resize((150, int(150 * L.height / L.width)), Image.LANCZOS)
tg = tag("@miguelesquit", 46).rotate(90, expand=True)
x0, y0 = 64, 600
img.paste(lg, (x0, y0), lg)
img.paste(tg, (x0 + (lg.width - tg.width) // 2, y0 + lg.height + 22), tg)
con_opacidad(img, 0.55).save("marca_v.png")
# horizontal: logo más grande sin círculo + @
img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
lg = L.resize((170, int(170 * L.height / L.width)), Image.LANCZOS)
tg = tag("@miguelesquit", 38)
x0 = 1920 - 60 - lg.width - 14 - tg.width
y0 = 1080 - 60 - lg.height
img.paste(lg, (x0, y0), lg)
img.paste(tg, (x0 + lg.width + 14, y0 + (lg.height - tg.height) // 2), tg)
con_opacidad(img, 0.8).save("marca_h.png")
print("ok")

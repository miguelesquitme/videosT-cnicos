"""Recrea el logo ME. en alta resolución y genera las marcas de agua (vertical y horizontal)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf"
import glob
F = (glob.glob("/usr/share/fonts/**/Montserrat-Black.*", recursive=True) + [F])[0]
FI = glob.glob("/usr/share/fonts/**/Inter*Bold*.*", recursive=True)
FI = [f for f in FI if f.endswith("Inter-SemiBold.otf") or f.endswith("Inter-SemiBold.ttf")] or FI


def logo(S=600):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([4, 4, S - 4, S - 4], fill=(255, 255, 255, 255), outline=(14, 155, 181, 255), width=max(2, S // 90))
    f = ImageFont.truetype(F, int(S * 0.42))
    wM = d.textlength("M", font=f); wE = d.textlength("E", font=f); wP = d.textlength(".", font=f)
    x0 = (S - (wM + wE + wP) * 0.93) / 2
    y = S * 0.5
    d.text((x0, y), "M", font=f, fill=(205, 235, 242, 255), anchor="lm")
    d.text((x0 + wM * 0.93, y), "E", font=f, fill=(14, 155, 181, 255), anchor="lm")
    d.text((x0 + (wM + wE) * 0.93, y), ".", font=f, fill=(14, 155, 181, 255), anchor="lm")
    return im


L = logo()
L.save("logo_me.png")


def marca(W, H, pos, tam_logo, tam_txt, vertical_txt=False, op=0.78):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lg = L.resize((tam_logo, tam_logo), Image.LANCZOS)
    f = ImageFont.truetype(FI[0], tam_txt)
    l, t, r, b = f.getbbox("@miguelesquit")
    tag = Image.new("RGBA", (r - l + 16, b - t + 12), (0, 0, 0, 0))
    ImageDraw.Draw(tag).text((8 - l, 6 - t), "@miguelesquit", font=f, fill=(14, 120, 145, 255))
    if vertical_txt:
        tag = tag.rotate(90, expand=True)
        x, y = pos
        img.paste(lg, (x, y), lg)
        img.paste(tag, (x + (tam_logo - tag.size[0]) // 2, y + tam_logo + 14), tag)
    else:
        x, y = pos
        img.paste(lg, (x, y), lg)
        img.paste(tag, (x + tam_logo + 12, y + (tam_logo - tag.size[1]) // 2), tag)
    a = img.split()[3].point(lambda v: int(v * op))
    img.putalpha(a)
    return img


marca(1080, 1920, (26, 560), 96, 40, vertical_txt=True).save("marca_v.png")
marca(1920, 1080, (1920 - 420, 1080 - 128), 84, 38).save("marca_h.png")
print("ok", F, FI[0])

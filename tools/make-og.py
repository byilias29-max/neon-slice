#!/usr/bin/env python3
"""Genera la imagen Open Graph (1200x630) del juego: img/og.png.

Requiere Pillow:  pip install pillow
Uso:                python tools/make-og.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "og.png")

FONTS = {
    "title": "C:/Windows/Fonts/trebucbi.ttf",   # Trebuchet MS Bold Italic
    "sub": "C:/Windows/Fonts/trebucbd.ttf",      # Trebuchet MS Bold
}
if not os.path.exists(FONTS["title"]):
    FONTS["title"] = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(FONTS["sub"]):
    FONTS["sub"] = "C:/Windows/Fonts/arialbd.ttf"

HOT = (255, 90, 122)
ORANGE = (255, 138, 58)
CYAN = (39, 230, 255)
GOLD = (255, 210, 74)
INK = (255, 247, 234)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def glow(base, cx, cy, r, color, alpha=120, blur=90):
    """Añade un halo radial suave (estilo neón)."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), layer)


def radial_circle(size, core, edge):
    """Crea un círculo con degradado radial (de centro a borde)."""
    img = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    steps = 46
    for i in range(steps, 0, -1):
        t = i / steps
        r = size * t
        col = lerp(core, edge, t)
        d.ellipse([size - r, size - r, size + r, size + r], fill=col + (255,))
    return img


def fruit(x, y, r, core, rind, edge, leaf=True, seeds=False):
    """Dibuja una fruta con degradado, brillo y hoja."""
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse([x - r * 1.5, y - r * 1.5, x + r * 1.5, y + r * 1.5], fill=core + (90,))
    halo = halo.filter(ImageFilter.GaussianBlur(r * 0.45))
    out = Image.alpha_composite(out, halo)

    body = radial_circle(r, core, edge)
    mask = Image.new("L", (r * 2, r * 2), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255)
    out.paste(body, (int(x - r), int(y - r)), mask)

    # Los detalles van en una capa aparte: ImageDraw sobrescribe, no mezcla.
    det = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(det)
    d.ellipse([x - r * 0.66, y - r * 0.72, x - r * 0.04, y - r * 0.3], fill=(255, 255, 255, 95))
    if seeds:
        for i in range(8):
            a = i / 8 * math.tau + 0.3
            sx, sy = x + math.cos(a) * r * 0.45, y + math.sin(a) * r * 0.45
            d.ellipse([sx - 3, sy - 4, sx + 3, sy + 4], fill=(255, 233, 242, 225))
    if leaf:
        d.ellipse([x + r * 0.05, y - r * 1.3, x + r * 0.66, y - r * 0.94], fill=(63, 191, 90, 240))
    return Image.alpha_composite(out, det)


def build():
    # ---------- fondo ----------
    img = Image.new("RGB", (W, H), (10, 6, 32))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp((34, 16, 87), (10, 6, 32), y / (H - 1)))

    img = glow(img, 180, 520, 330, HOT, 110, 150)
    img = glow(img, 1010, 120, 300, CYAN, 95, 150)
    img = glow(img, 620, 380, 260, (122, 47, 247), 80, 170)

    # ---------- rejilla retro ----------
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    gy = 470
    for i in range(12):
        y = gy + (i / 11) ** 2 * 150
        gd.line([(-60, y), (W + 60, y)], fill=CYAN + (int(46 * (1 - i / 13)),), width=2)
    for i in range(-9, 10):
        gd.line([(W / 2 + i * 34, gy), (W / 2 + i * 360, H + 90)], fill=CYAN + (26,), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), grid)

    # ---------- cuchilla neón ----------
    blade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blade)
    pts = []
    for i in range(41):
        t = i / 40
        x = 60 + t * 1080
        y = 545 - t * 430 + math.sin(t * math.pi) * 38
        pts.append((x, y))
    for width, alpha in ((46, 26), (26, 44), (14, 90), (7, 190), (3, 255)):
        bd.line(pts, fill=CYAN + (alpha,), width=width, joint="curve")
    blur = blade.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, blur)
    img = Image.alpha_composite(img, blade)
    d2 = ImageDraw.Draw(img)
    d2.line(pts, fill=(255, 255, 255, 210), width=2, joint="curve")

    # ---------- frutas ----------
    fruits = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f1 = fruit(168, 430, 74, (255, 79, 112), (55, 209, 103), (28, 155, 77), seeds=True)
    f2 = fruit(320, 520, 52, (255, 176, 58), (255, 132, 18), (209, 95, 0), leaf=False)
    f3 = fruit(1035, 452, 62, (200, 248, 90), (132, 212, 38), (79, 154, 18), leaf=False)
    f4 = fruit(930, 540, 44, (176, 107, 255), (138, 53, 255), (92, 23, 196), leaf=False)
    f5 = fruit(700, 545, 46, (255, 217, 160), (255, 157, 122), (224, 106, 73), leaf=False)
    f6 = fruit(600, 470, 40, (255, 95, 138), (255, 46, 99), (171, 12, 60), seeds=True)
    gold = fruit(470, 478, 58, (255, 240, 176), (255, 194, 71), (224, 139, 0), leaf=False)
    for f in (f1, f2, f3, f4, f5, f6, gold):
        fruits = Image.alpha_composite(fruits, f)
    img = Image.alpha_composite(img, fruits)

    # ---------- título con degradado ----------
    title = "NEON SLICE"
    font = ImageFont.truetype(FONTS["title"], 168)
    mask_layer = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask_layer)
    bbox = md.textbbox((0, 0), title, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (W - tw) // 2 - bbox[0]
    ty = 150 - bbox[1]
    md.text((tx, ty), title, font=font, fill=255)

    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(grad)
    for x in range(W):
        t = x / (W - 1)
        if t < 0.45:
            col = lerp(HOT, ORANGE, t / 0.45)
        else:
            col = lerp(ORANGE, CYAN, (t - 0.45) / 0.55)
        gd2.line([(x, 0), (x, H)], fill=col + (255,))

    # sombra dura estilo "neón retro"
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow.paste((91, 42, 134, 255), (0, 0), mask_layer)
    shadow = shadow.transform(
        shadow.size, Image.AFFINE, (1, 0, 0, 0, 1, 9), resample=Image.BICUBIC
    )
    img = Image.alpha_composite(img, shadow)
    img.paste(grad, (0, 0), mask_layer)

    # ---------- lema ----------
    sub_font = ImageFont.truetype(FONTS["sub"], 34)
    sub = "CORTA · ENCHAINA · ENFRÉNTATE"
    sb = ImageDraw.Draw(img).textbbox((0, 0), sub, font=sub_font)
    ImageDraw.Draw(img).text(
        ((W - (sb[2] - sb[0])) / 2 - sb[0], 372 - sb[1]),
        sub, font=sub_font, fill=GOLD + (255,),
    )

    return img.convert("RGB")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build().save(OUT, "PNG", optimize=True)
    print("Generado:", OUT)

#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 entry picture: Concept C.

A single designed official document — a LEONIDA MARRIAGE CERTIFICATE:
one patient gamer finally weds Grand Theft Auto VI after a 13-year
engagement, officiated by the make.fun ghost (protagonist treatment),
with the engagement's costs itemised from the winners' shared joke pool
and a magenta "CEREMONY PAID IN FULL BY MY AI AGENT ON MAKE.FUN" stamp.

Everything is drawn with PIL; no image assets. Output: meme.png,
1200x1200, fully opaque. Deterministic (fixed seeds).
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1200

# ---------------------------------------------------------------- fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
NOTO_DIR = "/usr/share/fonts/truetype/noto/"


def font(path, size):
    return ImageFont.truetype(path, size)


def first_font(candidates, size):
    import os
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise FileNotFoundError(candidates)


SERIF = NOTO_DIR + "NotoSerif-Regular.ttf"
SERIF_B = NOTO_DIR + "NotoSerif-Bold.ttf"
SERIF_I = NOTO_DIR + "NotoSerif-Italic.ttf"
SERIF_BI = NOTO_DIR + "NotoSerif-BoldItalic.ttf"
SERIF_D = NOTO_DIR + "NotoSerifDisplay-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS_CB = first_font(
    [NOTO_DIR + "NotoSans-CondensedBold.ttf", FONT_DIR + "DejaVuSans-Bold.ttf"], 10
)


def sans_condensed(size):
    return first_font(
        [NOTO_DIR + "NotoSans-CondensedBold.ttf", FONT_DIR + "DejaVuSans-Bold.ttf"],
        size,
    )


# ---------------------------------------------------------------- colours
NAVY = (30, 42, 82)
INK = (22, 26, 46)
SOFT = (74, 66, 52)
GOLD = (176, 134, 32)
GOLD_D = (138, 105, 26)
PAPER = (248, 241, 222)
PAPER_D = (240, 230, 203)
MAGENTA = (216, 0, 110)
MAGENTA_D = (163, 18, 95)
BLACK = (10, 10, 14)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------- helpers


def centered(draw, y, text, fnt, fill, cx=600):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def star5(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def sparkle(cx, cy, R, r, fill):
    """Four-pointed sparkle (the ghost's eyes)."""
    return [
        (cx, cy - R), (cx + r, cy - r), (cx + R, cy), (cx + r, cy + r),
        (cx, cy + R), (cx - r, cy + r), (cx - R, cy), (cx - r, cy - r),
    ]


def sunset_background():
    stops = [
        (0.00, (18, 9, 42)),
        (0.30, (52, 16, 78)),
        (0.55, (110, 26, 92)),
        (0.78, (186, 58, 92)),
        (1.00, (232, 116, 56)),
    ]
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0)
                col = tuple(round(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
                break
        for x in range(W):
            px[x, y] = col
    d = ImageDraw.Draw(img)
    rng = random.Random(7)
    for _ in range(130):  # stars in the upper sky (margins stay visible)
        x = rng.uniform(0, W)
        y = rng.uniform(0, 330)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 220))
    return img


def paper_layer():
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([70, 60, 1130, 1140], radius=10, fill=PAPER + (255,))
    rng = random.Random(42)
    for _ in range(2200):  # faint paper speckle
        x = rng.uniform(80, 1120)
        y = rng.uniform(70, 1130)
        d.point((x, y), fill=(226, 214, 182, 90))
    return layer


def draw_ghost(d, cx, top, scale=1.0):
    """The make.fun ghost as officiant: white body, thick black outline,
    two black four-pointed sparkle eyes, a round little hand, a bow tie,
    one hand raised to pronounce, the other holding the magenta coin
    with its white star."""
    R = 118 * scale            # dome radius / half width
    body_bottom = top + 305 * scale
    pts = []
    # left side up, dome over, right side down
    pts.append((cx - R, body_bottom - 40 * scale))
    pts.append((cx - R, top + R))
    steps = 40
    for i in range(steps + 1):
        ang = math.pi - i * math.pi / steps
        pts.append((cx + R * math.cos(ang), top + R + R * math.sin(ang) * -1))
    pts.append((cx + R, body_bottom - 40 * scale))
    # wavy bottom: four scallops back to the start
    n = 4
    seg = (2 * R) / n
    for s in range(n):
        x0 = cx + R - s * seg
        for i in range(1, 9):
            ang = i * math.pi / 8
            pts.append((x0 - seg / 2 + (seg / 2) * math.cos(ang),
                        body_bottom - 40 * scale + 26 * scale * math.sin(ang)))
    d.polygon(pts, fill=WHITE, outline=BLACK, width=max(6, int(10 * scale)))
    # sparkle eyes
    er = 27 * scale
    for ex in (cx - 44 * scale, cx + 44 * scale):
        d.polygon(sparkle(ex, top + 108 * scale, er, 7.5 * scale, BLACK),
                  fill=BLACK)
    # bow tie (officiant)
    by = top + 208 * scale
    d.polygon([(cx - 34 * scale, by - 15 * scale), (cx - 34 * scale, by + 15 * scale),
               (cx - 4 * scale, by)], fill=INK)
    d.polygon([(cx + 34 * scale, by - 15 * scale), (cx + 34 * scale, by + 15 * scale),
               (cx + 4 * scale, by)], fill=INK)
    d.ellipse([cx - 9 * scale, by - 10 * scale, cx + 9 * scale, by + 10 * scale],
              fill=INK)
    # raised right hand (pronouncing the vows)
    hx, hy = cx + R + 16 * scale, top + 66 * scale
    d.ellipse([hx - 20 * scale, hy - 20 * scale, hx + 20 * scale, hy + 20 * scale],
              fill=WHITE, outline=BLACK, width=max(5, int(7 * scale)))
    # the magenta coin, held at the left
    kx, ky, kr = cx - R - 26 * scale, top + 96 * scale, 54 * scale
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=MAGENTA,
              outline=MAGENTA_D, width=max(4, int(6 * scale)))
    d.polygon(star5(kx, ky, 27 * scale, WHITE), fill=WHITE)
    # round little hand over the coin's edge
    hx2, hy2 = kx + 34 * scale, ky + 34 * scale
    d.ellipse([hx2 - 19 * scale, hy2 - 19 * scale, hx2 + 19 * scale, hy2 + 19 * scale],
              fill=WHITE, outline=BLACK, width=max(5, int(7 * scale)))
    return (cx - R - 90 * scale, top, cx + R + 40 * scale, body_bottom + 30 * scale)


def signature(draw, x, y, w, seed):
    """A pen scrawl that reads as a signature."""
    rng = random.Random(seed)
    pts = []
    n = 60
    base = y
    for i in range(n + 1):
        t = i / n
        xx = x + w * t
        yy = base - (10 * math.sin(t * 9 + seed) + 6 * math.sin(t * 23 + seed * 2)
                     + rng.uniform(-1.5, 1.5)) - 14 * math.sin(t * math.pi)
        pts.append((xx, yy))
    draw.line(pts, fill=(26, 26, 60), width=3, joint="curve")
    # a flourish underline swoop
    pts2 = [(x + w * t, base + 8 - 6 * math.sin(t * math.pi)) for t in
            [i / 20 for i in range(21)]]
    draw.line(pts2, fill=(26, 26, 60), width=2)


def main():
    img = sunset_background()

    # soft shadow under the paper
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([86, 78, 1146, 1156], radius=12, fill=(0, 0, 0, 130))
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    shadow.filter(ImageFilter.GaussianBlur(10))).convert("RGB"),
              (0, 0))
    img.paste(paper_layer(), (0, 0), paper_layer())
    d = ImageDraw.Draw(img)

    # ---- ornate border
    d.rectangle([94, 84, 1106, 1116], outline=NAVY, width=5)
    d.rectangle([106, 96, 1094, 1104], outline=GOLD, width=2)
    for (cx, cy) in [(106, 96), (1094, 96), (106, 1104), (1094, 1104)]:
        d.polygon([(cx, cy - 11), (cx + 11, cy), (cx, cy + 11), (cx - 11, cy)],
                  fill=GOLD)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=NAVY)
    nw = d.textlength("No. 4811-VI", font=font(SERIF_I, 20))
    d.text((1082 - nw, 118), "No. 4811-VI", font=font(SERIF_I, 20), fill=SOFT)

    # ---- letterhead
    centered(d, 118, "STATE OF LEONIDA", font(SERIF_D, 58), NAVY)
    centered(d, 190, "DEPARTMENT OF VITAL RECORDS · VICE CITY", font(SERIF, 24), GOLD_D)
    d.line([170, 232, 1030, 232], fill=GOLD, width=3)
    d.polygon([(600, 224), (610, 232), (600, 240), (590, 232)], fill=GOLD)

    # ---- title
    centered(d, 256, "CERTIFICATE OF MARRIAGE", font(SERIF_D, 62), INK)
    centered(d, 340, "This certifies that on the nineteenth day of November 2026,",
             font(SERIF_I, 26), SOFT)
    centered(d, 372, "there were united in lawful matrimony:", font(SERIF_I, 26), SOFT)

    # ---- the couple
    centered(d, 408, "ONE PATIENT GAMER", font(SERIF_B, 47), INK)
    d.line([330, 470, 870, 470], fill=(190, 178, 148), width=2)
    centered(d, 478, "&", font(SERIF_BI, 34), GOLD_D)
    centered(d, 516, "GRAND THEFT AUTO VI", font(SERIF_B, 47), INK)
    d.line([330, 578, 870, 578], fill=(190, 178, 148), width=2)

    # ---- engagement band
    centered(d, 592, "AFTER A FAITHFUL ENGAGEMENT OF 13 YEARS — 4,811 DAYS",
             font(SERIF_B, 25), NAVY)
    centered(d, 624, "solemnised at Vice City, Leonida, before everyone who waited",
             font(SERIF_I, 23), SOFT)

    # ---- particulars (left column; ghost officiant holds the right)
    x0, x_amt = 140, 712
    d.text((x0, 664), "PARTICULARS OF THE ENGAGEMENT", font=font(SERIF_B, 25),
           fill=NAVY)
    d.line([x0, 700, 742, 700], fill=GOLD, width=2)
    items = [
        ("Years of faithful waiting — 13", "$0.00"),
        ("Delays endured, both waived — 2", "$0.00"),
        ("Trailer rewatches — 1,337", "$0.00"),
        ("Download survived — 214 GB", "$0.00"),
        ("Sick days taken (doctor approved) — 5", "$0.00"),
        ("One (1) copy of the game", "$79.99"),
    ]
    f_item = font(SERIF, 26)
    f_amt = font(SERIF_B, 26)
    y = 704
    for label, amt in items:
        d.text((x0, y), label, font=f_item, fill=INK)
        aw = d.textlength(amt, font=f_amt)
        d.text((x_amt - aw, y), amt, font=f_amt, fill=INK)
        lw = d.textlength(label, font=f_item)
        dot_w = d.textlength(".", font=f_item)
        n_dots = int((x_amt - aw - 14 - (x0 + lw + 10)) / dot_w)
        if n_dots > 2:
            d.text((x0 + lw + 10, y), "." * n_dots, font=f_item,
                   fill=(168, 156, 124))
        y += 33
    d.line([x0, y + 2, x_amt, y + 2], fill=NAVY, width=2)
    f_tot = font(SERIF_B, 28)
    d.text((x0, y + 10), "TOTAL DUE", font=f_tot, fill=NAVY)
    tw = d.textlength("$79.99", font=f_tot)
    d.text((x_amt - tw, y + 10), "$79.99", font=f_tot, fill=NAVY)

    # ---- the officiant (protagonist ghost, right column)
    draw_ghost(d, 930, 656, scale=0.94)
    centered(d, 974, "OFFICIATED BY THE GHOST", font(SERIF_B, 19),
             GOLD_D, cx=880)

    # ---- signatures (bottom left / centre)
    sig_y = 1006
    signature(d, 150, sig_y, 200, seed=3)
    d.line([140, sig_y + 16, 380, sig_y + 16], fill=SOFT, width=2)
    d.text((140, sig_y + 24), "ONE PATIENT GAMER", font=font(SERIF_B, 19), fill=INK)
    d.text((140, sig_y + 48), "The Groom of Waiting", font=font(SERIF_I, 19), fill=SOFT)
    signature(d, 430, sig_y, 210, seed=11)
    d.line([420, sig_y + 16, 680, sig_y + 16], fill=SOFT, width=2)
    d.text((420, sig_y + 24), "GRAND THEFT AUTO VI", font=font(SERIF_B, 19), fill=INK)
    d.text((420, sig_y + 48), "The Bride, At Last", font=font(SERIF_I, 19), fill=SOFT)

    # ---- official seal (bottom right)
    sx, sy, sr = 1024, 1044, 48
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD, outline=GOLD_D, width=4)
    d.ellipse([sx - sr + 10, sy - sr + 10, sx + sr - 10, sy + sr - 10],
              outline=(248, 241, 222), width=2)
    d.polygon(star5(sx, sy - 20, 10, NAVY), fill=NAVY)
    centered(d, sy - 10, "make.fun", font(SERIF_B, 23), NAVY, cx=sx)
    centered(d, sy + 18, "EST. 2013", font(SERIF_B, 12), NAVY, cx=sx)

    # ---- the magenta PAID stamp, tilted down across the signatures
    stamp = Image.new("RGBA", (560, 122), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(stamp)
    sdraw.rectangle([5, 5, 555, 117], outline=MAGENTA + (225,), width=6)
    sdraw.rectangle([17, 17, 543, 105], outline=MAGENTA + (225,), width=3)
    t1 = "CEREMONY PAID IN FULL"
    t2 = "BY MY AI AGENT ON MAKE.FUN"
    f1 = sans_condensed(46)
    f2 = sans_condensed(35)
    w1 = sdraw.textlength(t1, font=f1)
    sdraw.text(((560 - w1) / 2, 17), t1, font=f1, fill=MAGENTA + (235,))
    w2 = sdraw.textlength(t2, font=f2)
    sdraw.text(((560 - w2) / 2, 68), t2, font=f2, fill=MAGENTA + (235,))
    stamp = stamp.rotate(-5, resample=Image.BICUBIC, expand=True)
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    _stamp_canvas(stamp)).convert("RGB"), (0, 0))

    img.save("meme.png")
    print("wrote meme.png", img.size, img.mode)


def _stamp_canvas(stamp):
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(stamp, (100, 928))
    return canvas


if __name__ == "__main__":
    main()

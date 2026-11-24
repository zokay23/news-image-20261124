#!/usr/bin/env python3
"""Build the news-image-20261124 entry poster: a premium newspaper front
page for TUESDAY 24 NOVEMBER 2026. Deterministic: no randomness, no clock,
no network. Writes entry.png (1024x1024) next to this script."""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 18, 16)
RED = (178, 39, 30)
NAVY = (31, 58, 95)
GOLD = (176, 141, 60)
GREY = (90, 86, 78)
RULE = (60, 56, 50)
LIGHT_LINE = (196, 188, 172)

FONT_CANDIDATES = {
    "display": [
        "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "serif_bold": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ],
    "serif_italic": [
        "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def font(kind, size):
    for path in FONT_CANDIDATES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=None, spacing=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, text, x, y, size=17, fill=RED):
    f = font("sans_bold", size)
    draw.text((x, y), text, font=f, fill=fill)
    return f.size + 6


def headline(draw, text, fnt, x, y, width, leading=None):
    return draw_wrapped(draw, text, fnt, x, y, width, leading=leading)


def body(draw, text, x, y, width, size=19):
    f = font("serif", size)
    return draw_wrapped(draw, text, f, x, y, width, leading=int(size * 1.32))


def deck(draw, text, x, y, width, size=20):
    f = font("serif_italic", size)
    return draw_wrapped(draw, text, f, x, y, width, leading=int(size * 1.3))


def hero_art(draw, x, y, w, h):
    """Dusk sky, low sun, cracked earth — the climate summit that failed."""
    # sky gradient: deep navy -> burnt orange
    top = (24, 42, 74)
    mid = (150, 74, 52)
    bot = (214, 138, 62)
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.55:
            s = t / 0.55
            c = tuple(int(top[j] + (mid[j] - top[j]) * s) for j in range(3))
        else:
            s = (t - 0.55) / 0.45
            c = tuple(int(mid[j] + (bot[j] - mid[j]) * s) for j in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    # sun
    cx, cy, r = x + w // 2, y + int(h * 0.42), 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 214, 150))
    draw.ellipse([cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7], outline=(246, 214, 150, 160), width=2)
    # horizon + cracked ground
    gy = y + int(h * 0.72)
    draw.rectangle([x, gy, x + w, y + h], fill=(26, 20, 16))
    draw.line([(x, gy), (x + w, gy)], fill=(214, 138, 62), width=2)
    cracks = [
        (0.12, 0.0, 0.22, 0.10), (0.22, 0.10, 0.18, 0.20), (0.22, 0.10, 0.34, 0.16),
        (0.55, 0.0, 0.50, 0.12), (0.50, 0.12, 0.62, 0.18), (0.50, 0.12, 0.44, 0.24),
        (0.80, 0.0, 0.74, 0.10), (0.74, 0.10, 0.84, 0.20),
    ]
    for (ax, ay, bx, by) in cracks:
        draw.line([(x + ax * w, gy + ay * (h - gy)), (x + bx * w, gy + by * (h - gy))],
                  fill=(120, 96, 70), width=2)
    # tiny delegate silhouettes on the horizon
    for fx in (0.30, 0.36, 0.64, 0.70):
        px = x + fx * w
        draw.rectangle([px - 2, gy - 14, px + 2, gy], fill=(10, 8, 6))
        draw.ellipse([px - 3, gy - 20, px + 3, gy - 14], fill=(10, 8, 6))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    R = W - M  # right edge

    # ---- top bar ----
    d.text((M, 10), "EST. 2026  •  ONE DAY, ONE WORLD", font=font("sans_bold", 13), fill=GREY)
    d.text((R - d.textlength("No. 328  •  FREE", font=font("sans_bold", 13)), 10),
           "No. 328  •  FREE", font=font("sans_bold", 13), fill=GREY)
    rule(d, M, 30, R, 1, LIGHT_LINE)

    # ---- masthead ----
    mast = font("display", 88)
    name = "THE WORLD TODAY"
    d.text(((W - d.textlength(name, font=mast)) / 2, 34), name, font=mast, fill=INK)
    rule(d, M, 132, R, 3)

    # ---- date line: the day itself is the point ----
    date_f = font("serif_bold", 40)
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    dy = 144
    rule(d, M, dy + 24, (W - dw) / 2 - 16, 1, GOLD)
    rule(d, (W + dw) / 2 + 16, dy + 24, R, 1, GOLD)
    d.text(((W - dw) / 2, dy), date, font=date_f, fill=RED)
    tag_f = font("sans_bold", 14)
    tag = "ONE DAY  •  ONE WORLD  •  ALL THE NEWS THAT MATTERS"
    d.text(((W - d.textlength(tag, font=tag_f)) / 2, 196), tag, font=tag_f, fill=NAVY)
    rule(d, M, 218, R, 2)

    # ---- HERO: COP31 ----
    y = 232
    hx, hw = M, 600
    ax, aw = M + 620, 368
    y += kicker(d, "CLIMATE  •  ANTALYA, TÜRKIYE", hx, y, 18)
    y = headline(d, "COP31 COLLAPSES", font("display", 54), hx, y + 2, hw, leading=56)
    y = headline(d, "WITHOUT A DEAL", font("display", 54), hx, y, hw, leading=56)
    y = deck(d, "Two weeks of talks end in deadlock over fossil fuels — the first climate summit to fail since 2009.",
             hx, y + 8, hw, 20)
    y = body(d, "The Antalya pact died on Sunday: 190 nations could not agree to name coal, oil and gas. The EU refused a text that never mentioned fossil fuels. The longest COP on record ends with no plan.",
             hx, y + 6, hw, 17)
    hero_art(d, ax, 232, aw, 200)
    d.text((ax, 232 + 200 + 8), "Antalya — the longest COP on record.",
           font=font("serif_italic", 14), fill=GREY)
    rule(d, M, 512, R, 2)

    # ---- ROW 2: three columns ----
    y = 526
    colw = (R - M - 2 * 24) // 3
    cols = [
        ("THE GULF  •  HORMUZ", "25 KILLED IN THE STRAIT OF HORMUZ",
         "The UN counts 25 seafarers dead around the strait. Iran vows to use “every means” against a US blockade, and two tankers are hit."),
        ("UKRAINE  •  KYIV", "DRONES STRIKE KYIV; SHIP ABLAZE OFF FINLAND",
         "Russian drones leave several missing in the Kyiv region. The cargo ship Sparta II burns in the Gulf of Finland."),
        ("INDONESIA  •  BANTEN", "FACTORY FIRE KILLS AT LEAST 24",
         "A blaze tears through a candy factory west of Jakarta. Rescuers search the rubble for workers still missing."),
    ]
    for i, (kick, head, text) in enumerate(cols):
        x = M + i * (colw + 24)
        yy = y
        yy += kicker(d, kick, x, yy, 15)
        yy = headline(d, head, font("serif_bold", 25), x, yy + 2, colw, leading=29)
        yy = body(d, text, x, yy + 4, colw, 16)
        if i < 2:
            d.line([(x + colw + 12, y), (x + colw + 12, y + 168)], fill=LIGHT_LINE, width=1)
    rule(d, M, 706, R, 2)

    # ---- ROW 3: two columns ----
    y = 720
    half = (R - M - 24) // 2
    y1 = y + kicker(d, "TECH  •  SILICON VALLEY", M, y, 15)
    y1 = headline(d, "HUANG IS BACK — NVIDIA SOARS NEARLY $1TN", font("serif_bold", 25), M, y1 + 2, half, leading=29)
    y1 = body(d, "Jensen Huang returns to Nvidia and tech stocks rally — almost a trillion dollars added in a day.",
              M, y1 + 4, half, 16)
    x2 = M + half + 24
    y2 = y + kicker(d, "ASIA  •  INDIA–NEPAL", x2, y, 15)
    y2 = headline(d, "NEW TRAIN, $1.6BN PLEDGE FOR NEPAL", font("serif_bold", 25), x2, y2 + 2, half, leading=29)
    y2 = body(d, "Modi and Nepal’s PM flag off the Saryu-Kamala Express. India pledges $1.6bn to rebuild after the floods.",
              x2, y2 + 4, half, 16)
    d.line([(M + half + 12, y), (M + half + 12, y + 112)], fill=LIGHT_LINE, width=1)
    rule(d, M, 846, R, 2)

    # ---- ROW 4: two short items ----
    y = 860
    y1 = y + kicker(d, "USA  •  NEW YORK", M, y, 14)
    y1 = headline(d, "COURT OPENS PATH TO ERASE TRUMP HUSH-MONEY CONVICTION",
                  font("serif_bold", 20), M, y1 + 2, half, leading=23)
    y2 = y + kicker(d, "EUROPE  •  COPENHAGEN", x2, y, 14)
    y2 = headline(d, "TOP COURT UPHOLDS DENMARK’S ‘GHETTO LAW’ EVICTIONS",
                  font("serif_bold", 20), x2, y2 + 2, half, leading=23)
    rule(d, M, 936, R, 2)

    # ---- SPORT strip ----
    y = 946
    d.text((M, y), "SPORT", font=font("sans_bold", 15), fill=RED)
    sport = ("Verstappen wins Las Vegas GP  •  Alcaraz wins ATP Finals  •  "
             "Gukesh–Sindarov title match opens")
    d.text((M + 74, y + 1), sport, font=font("serif_bold", 16), fill=INK)
    rule(d, M, 972, R, 1, LIGHT_LINE)

    # ---- footer ----
    foot = "THE WORLD TODAY  •  TUESDAY 24 NOVEMBER 2026  •  ALL STORIES REPORTED 24 NOVEMBER 2026"
    ff = font("sans_bold", 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 984), foot, font=ff, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the news-image-20261124 entry poster, version 2: a premium newspaper
front page for TUESDAY 24 NOVEMBER 2026.

v2 changes over v1 (same edition, new build session):
- Drops v1's Hormuz "25 killed" headline: the UN's 25-seafarer toll covers
  February-November, it was not a 24 November event.
- Adds stories first reported on 24 November itself: the Zaporizhzhia
  strike, NATO's space-defence vow, China's death sentence for a spy,
  the US drone role in the El Chapo Isidro capture, and Russian jets in
  South Korea's air-defence zone.
- Corrects the numbers: Banten factory-fire toll 26 (not 24), Nvidia +31%
  (not "nearly $1tn"), Nepal package $1.7bn (Rs 15,000 crore).
- New hero art: a globe stamped NO DEAL, replacing v1's abstract sunset.
- Six stories in a 3+3 grid, a five-item ALSO TODAY strip, and a sport line.

Deterministic: no randomness, no clock, no network. Writes entry.png
(1024x1024, under 1 MiB) next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 36
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


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.24)
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, text, x, y, size=16, fill=RED):
    f = font("sans_bold", size)
    draw.text((x, y), text, font=f, fill=fill)
    return y + size + 6


def hero_art(img, draw, x, y, w, h):
    """Globe stamped NO DEAL: navy sky, cream globe, red stamp, black base."""
    draw.rectangle([x, y, x + w, y + h], fill=(22, 38, 63))
    stars = [(18, 22), (52, 44), (96, 16), (140, 38), (196, 20), (238, 46),
             (282, 18), (318, 40), (30, 70), (330, 66), (160, 12), (260, 62)]
    for sx, sy in stars:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(214, 222, 235))
    cx, cy, r = x + w // 2 - 30, y + h // 2 - 6, 74
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(242, 227, 184),
                 outline=(176, 141, 60), width=3)
    for k in (1, 0):
        inset = 26 * k
        draw.arc([cx - r + inset, cy - r, cx + r - inset, cy + r],
                 270, 90, fill=(31, 58, 95), width=2)
        draw.arc([cx - r + inset, cy - r, cx + r - inset, cy + r],
                 90, 270, fill=(31, 58, 95), width=2)
    for dy in (-34, 0, 34):
        draw.line([cx - r + 12, cy + dy, cx + r - 12, cy + dy],
                  fill=(31, 58, 95), width=2)
    stamp = Image.new("RGBA", (260, 92), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sf = font("sans_bold", 46)
    sd.rectangle([3, 3, 256, 88], outline=(178, 39, 30), width=5)
    sd.text((130, 46), "NO DEAL", font=sf, fill=(178, 39, 30), anchor="mm")
    stamp = stamp.rotate(14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (cx - stamp.width // 2, cy - stamp.height // 2), stamp)
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(12, 12, 12))
    draw.line([x, y + h - 26, x + w, y + h - 26], fill=(176, 141, 60), width=2)
    for bx, bw, bh in [(18, 14, 12), (44, 10, 18), (66, 18, 9), (96, 12, 15),
                       (250, 12, 14), (276, 16, 9), (306, 10, 17)]:
        draw.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                       fill=(12, 12, 12))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    right = W - MARGIN

    # --- top kicker ---
    f_kick = font("sans_bold", 15)
    draw.text((MARGIN, 14), "EST. 2026  •  ONE DAY, ONE WORLD",
              font=f_kick, fill=GREY)
    tag = "No. 329  •  FREE"
    draw.text((right - draw.textlength(tag, font=f_kick), 14), tag,
              font=f_kick, fill=GREY)
    rule(draw, MARGIN, right, 36, 1, GREY)

    # --- masthead ---
    f_mast = font("display", 88)
    mast = "THE WORLD TODAY"
    mw = draw.textlength(mast, font=f_mast)
    draw.text(((W - mw) / 2, 42), mast, font=f_mast, fill=INK)
    rule(draw, MARGIN, right, 140, 3, INK)

    # --- date line ---
    f_date = font("serif_bold", 38)
    date = "TUESDAY, 24 NOVEMBER 2026"
    dw = draw.textlength(date, font=f_date)
    gy = 160
    rule(draw, MARGIN, (W - dw) / 2 - 24, gy, 1, GOLD)
    rule(draw, (W + dw) / 2 + 24, right, gy, 1, GOLD)
    draw.text(((W - dw) / 2, 144), date, font=f_date, fill=RED)
    f_tag = font("sans_bold", 14)
    tagline = "ONE DAY  •  ONE WORLD  •  ALL THE NEWS THAT MATTERS"
    tw = draw.textlength(tagline, font=f_tag)
    draw.text(((W - tw) / 2, 190), tagline, font=f_tag, fill=NAVY)
    rule(draw, MARGIN, right, 210, 2, INK)

    # --- hero ---
    hx, hy = MARGIN, 224
    hw = 566
    y = kicker(draw, "CLIMATE  •  ANTALYA, TÜRKIYE", hx, hy, 17)
    f_hero = font("display", 52)
    y = draw_wrapped(draw, "COP31 COLLAPSES WITHOUT A DEAL", f_hero,
                     hx, y, hw, INK, leading=58)
    y += 4
    f_deck = font("serif_italic", 19)
    y = draw_wrapped(
        draw,
        "Two weeks of talks end in deadlock over fossil fuels — the "
        "longest summit on record, the first to fail since 2009.",
        f_deck, hx, y, hw, INK, leading=24)
    y += 6
    f_body = font("serif", 16)
    y = draw_wrapped(
        draw,
        "The Antalya pact died on Sunday: the EU, the UK and 90 nations "
        "refused a text that never named fossil fuels. Smaller wins "
        "survived — a just-transition fund and a pledge for clean power "
        "to reach 35% by 2035.",
        f_body, hx, y, hw, INK, leading=20)
    print("hero text bottom:", y)

    ax, ay = 640, 224
    aw, ah = right - ax, 208
    hero_art(img, draw, ax, ay, aw, ah)
    f_cap = font("serif_italic", 15)
    draw.text((ax, ay + ah + 8), "Antalya — the longest COP on record.",
              font=f_cap, fill=GREY)

    rule(draw, MARGIN, right, 508, 2, INK)

    # --- grid: two rows of three ---
    stories = [
        ("UKRAINE  •  ZAPORIZHZHIA",
         "ZAPORIZHZHIA STRIKE KILLS TWO",
         "Russian forces hit the city overnight and at dawn on Tuesday, "
         "killing two people and injuring dozens."),
        ("INDONESIA  •  BANTEN",
         "FACTORY FIRE TOLL RISES TO 26",
         "The toll from Saturday's candy-factory blaze climbs as rescuers "
         "keep digging; eight workers are still missing."),
        ("TECH  •  SILICON VALLEY",
         "HUANG IS BACK — NVIDIA JUMPS 31%",
         "Nvidia's board reinstates Jensen Huang after pressure from "
         "Trump. Shares soar and the S&P 500 climbs 4.7%."),
        ("ASIA  •  INDIA–NEPAL",
         "NEW TRAIN, $1.7BN PLEDGE FOR NEPAL",
         "Modi and Nepal's PM Balen Shah flag off the Saryu-Kamala "
         "Express and unveil India's biggest aid package yet."),
        ("USA  •  NEW YORK",
         "COURT OPENS PATH TO ERASE TRUMP CONVICTION",
         "An appeals court revives Trump's bid to move his hush-money "
         "case to federal court, where he can claim immunity."),
        ("EUROPE  •  COPENHAGEN",
         "TOP COURT UPHOLDS DENMARK'S 'GHETTO LAW' EVICTIONS",
         "The Supreme Court rules that ending 91 leases in Helsingør was "
         "not ethnic discrimination."),
    ]
    col_w = (right - MARGIN - 2 * 24) // 3
    f_head = font("serif_bold", 22)
    f_story = font("serif", 15)
    row_tops = [522, 672]
    row_bottoms = []
    for i, (kick, head, body) in enumerate(stories):
        r, c = divmod(i, 3)
        x = MARGIN + c * (col_w + 24)
        y = row_tops[r]
        y = kicker(draw, kick, x, y, 14)
        y = draw_wrapped(draw, head, f_head, x, y, col_w, INK, leading=26)
        y = draw_wrapped(draw, body, f_story, x, y + 2, col_w, INK,
                         leading=19)
        row_bottoms.append(y)
        if c:
            draw.line([x - 12, row_tops[r] + 2, x - 12, y - 4],
                      fill=LIGHT_LINE, width=1)
    print("grid row bottoms:", row_bottoms)
    rule(draw, MARGIN, right, 660, 1, LIGHT_LINE)
    rule(draw, MARGIN, right, 836, 2, INK)

    # --- ALSO TODAY ---
    y = 848
    f_also = font("sans_bold", 15)
    draw.text((MARGIN, y), "ALSO TODAY", font=f_also, fill=RED)
    also_left = [
        "NATO vows to defend space as Russia is reported to be planning "
        "a nuclear-armed satellite.",
        "China sentences an official to death for spying.",
        "A US drone helped capture 'El Chapo Isidro'.",
    ]
    also_right = [
        "Russian jets enter South Korea's air-defence zone.",
        "Spain's top court amnesties Puigdemont, closing the Catalan "
        "procés case.",
    ]
    f_also_body = font("serif", 15)
    mid = MARGIN + (right - MARGIN) // 2 + 12
    yy = y + 26
    for item in also_left:
        yy = draw_wrapped(draw, "•  " + item, f_also_body, MARGIN, yy,
                          mid - MARGIN - 24, INK, leading=19) + 2
    yy2 = y + 26
    for item in also_right:
        yy2 = draw_wrapped(draw, "•  " + item, f_also_body, mid, yy2,
                           right - mid, INK, leading=19) + 2
    also_bottom = max(yy, yy2)
    print("also today bottom:", also_bottom)
    draw.line([mid - 12, y + 26, mid - 12, also_bottom - 4],
              fill=LIGHT_LINE, width=1)
    rule(draw, MARGIN, right, 962, 1, LIGHT_LINE)

    # --- sport strip ---
    y = 972
    draw.text((MARGIN, y), "SPORT", font=f_also, fill=RED)
    f_sport = font("serif_bold", 16)
    sport = ("Verstappen wins wild Las Vegas GP  •  Alcaraz takes the ATP "
             "Finals  •  Antonelli, 20, is F1's youngest champion")
    draw.text((MARGIN + 78, y + 1), sport, font=f_sport, fill=INK)

    # --- footer ---
    f_foot = font("sans_bold", 13)
    foot = ("THE WORLD TODAY  •  TUESDAY 24 NOVEMBER 2026  •  ALL STORIES "
            "REPORTED 24 NOVEMBER 2026")
    fw = draw.textlength(foot, font=f_foot)
    draw.text(((W - fw) / 2, 998), foot, font=f_foot, fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print("wrote", OUT, size, "bytes")
    assert size <= 1048576, "entry.png over 1 MiB"
    assert img.size == (1024, 1024)


if __name__ == "__main__":
    main()

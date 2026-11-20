#!/usr/bin/env python3
"""Generate entry.png (v2): a newspaper front page summing up Thursday 19 November 2026.

Design: smaller masthead so the lead wins; the summit is shown as one editorial
illustration (a round table seen from above, three flag-coloured chairs, a
declaration sheet in the middle) instead of three flag panels; hierarchy 1 + 2 + 3
(one lead, two secondary stories, three short summaries); every headline carries
the development, not just the topic; a two-item ticker.

Deterministic: fixed strings, fixed geometry, no randomness, no network.
Saves JPEG data (quality 90) under the name entry.png, under 1 MiB, 1024x1024.
Run: python3 gen_image.py  (writes entry.png next to this file)
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 40
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (30, 58, 95)
GREY = (90, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit(draw, text, fnt, max_width):
    """wrap() that refuses to ship a truncated line: max 2 lines, or fail loudly."""
    lines = wrap(draw, text, fnt, max_width)
    assert len(lines) <= 2, f"text overflows 2 lines: {text!r} -> {lines}"
    return lines


def center(draw, y, text, fnt, fill=INK, width=W):
    draw.text(((width - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def star_points(cx, cy, r_outer, r_inner, rot=-90.0):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 36.0)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_tile(w, h, kind):
    """A chair tile (w x h) painted with one country's flag, rounded corners."""
    tile = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(tile)
    if kind == "us":
        stripe = h / 13.0
        for i in range(13):
            c = (179, 25, 66) if i % 2 == 0 else (255, 255, 255)
            d.rectangle([0, i * stripe, w, (i + 1) * stripe], fill=c)
        cw, ch = w * 0.4, stripe * 7
        d.rectangle([0, 0, cw, ch], fill=(60, 59, 110))
        for row in range(9):
            n = 6 if row % 2 == 0 else 5
            for col in range(n):
                cx = cw * (0.12 + 0.76 * col / 5.0) if n == 6 else cw * (0.20 + 0.76 * col / 4.0)
                cy = ch * (0.10 + 0.80 * row / 8.0)
                r = 2.6
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    elif kind == "cn":
        d.rectangle([0, 0, w, h], fill=(222, 41, 16))
        d.polygon(star_points(w * 0.16, h * 0.30, 10, 10 * 0.382), fill=(255, 222, 0))
        for sx, sy, sr in [(0.36, 0.14, 4), (0.44, 0.26, 4), (0.44, 0.42, 4), (0.36, 0.54, 4)]:
            d.polygon(star_points(w * sx, h * sy, sr, sr * 0.382, rot=-70), fill=(255, 222, 0))
    else:  # ru
        third = h / 3.0
        for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 43, 30)]):
            d.rectangle([0, i * third, w, (i + 1) * third], fill=c)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=12, fill=255)
    tile.putalpha(mask)
    return tile


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN  # 944

    # ---- masthead (smaller, so the lead wins) ----
    f_top = font(SANS_B, 18)
    d.text((MARGIN, 28), "THURSDAY, 19 NOVEMBER 2026", font=f_top, fill=INK)
    right = "WORLD EDITION"
    d.text((W - MARGIN - d.textlength(right, font=f_top), 28), right, font=f_top, fill=INK)
    f_mast = font(SERIF_B, 64)
    center(d, 46, "THE WORLD", f_mast)
    d.rectangle([MARGIN, 116, W - MARGIN, 119], fill=INK)
    d.rectangle([MARGIN, 122, W - MARGIN, 123], fill=INK)

    # ---- lead headline ----
    f_kick = font(SANS_B, 20)
    center(d, 132, "SHENZHEN SUMMIT  \u00b7  THE FIRST THREE-WAY MEETING", f_kick, fill=RED)
    f_head = font(SERIF_B, 66)
    center(d, 156, "TRUMP, XI AND PUTIN", f_head)
    center(d, 222, "MEET IN SHENZHEN", f_head)
    f_sub = font(SERIF_I, 24)
    center(d, 288, "First three-way summit ends with a declaration that nuclear", f_sub, fill=(60, 58, 52))
    center(d, 314, "war must never happen \u2014 but no arms-control talks agreed", f_sub, fill=(60, 58, 52))

    # ---- editorial illustration: round table from above ----
    cx, cy, rx, ry = 512, 434, 230, 66
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=NAVY, outline=(20, 38, 62), width=2)
    # declaration sheet on the table
    d.rounded_rectangle([437, 400, 587, 464], radius=4, fill=(255, 255, 255), outline=(200, 194, 178), width=1)
    for i, yy in enumerate((412, 424, 436, 448)):
        d.line([449, yy, 575 - (18 if i == 3 else 0), yy], fill=(150, 146, 136), width=2)
    d.ellipse([560, 446, 578, 464], fill=RED)
    # three flag chairs around the table
    chair_us = flag_tile(104, 48, "us")
    chair_cn = flag_tile(104, 48, "cn")
    chair_ru = flag_tile(104, 48, "ru")
    img.paste(chair_us, (460, 348), chair_us)
    img.paste(chair_cn, (300, 486), chair_cn)
    img.paste(chair_ru, (620, 486), chair_ru)
    d = ImageDraw.Draw(img)
    d.rectangle([MARGIN, 546, W - MARGIN, 547], fill=INK)

    # ---- two secondary stories ----
    secondaries = [
        ("WORLD COURT", "ICJ RULES MYANMAR COMMITTED GENOCIDE",
         "Rules 9\u20136 in a case brought by Gambia over the Rohingya: the state is responsible."),
        ("CLIMATE", "COP31 DRAFT DROPS FOSSIL FUEL LANGUAGE",
         "Antalya negotiators strip the phase-out pledge as finance talks stall."),
    ]
    col_w = (inner - 28) // 2
    gx, gy = MARGIN, 560
    f_skick = font(SANS_B, 17)
    f_shead = font(SERIF_B, 30)
    f_sbody = font(SANS, 21)
    for idx, (kicker, headline, body) in enumerate(secondaries):
        x = gx + idx * (col_w + 28)
        y = gy
        d.text((x, y), kicker, font=f_skick, fill=RED)
        lines = fit(d, headline, f_shead, col_w)
        yy = y + 22
        for ln in lines:
            d.text((x, yy), ln, font=f_shead, fill=INK)
            yy += 34
        blines = fit(d, body, f_sbody, col_w)
        yy = y + 22 + 2 * 34
        for ln in blines:
            d.text((x, yy), ln, font=f_sbody, fill=(40, 38, 34))
            yy += 25
        if idx == 0:
            d.line([x + col_w + 14, y + 2, x + col_w + 14, y + 132], fill=(200, 194, 178), width=1)

    # ---- three short summaries ----
    summaries = [
        ("MARKETS", "ANTHROPIC $81.3BN IPO DEBUTS",
         "Shares close $97.17, up 17% on Nasdaq debut."),
        ("UKRAINE", "3RD CRIMEA BRIDGE STRIKE IN A WEEK",
         "Rail traffic halted; EU plans a \u20ac45bn loan for 2027."),
        ("GAZA", "GAZA PEACE PLAN SCORES 4 OF 26",
         "Five aid groups rate the truce as residents start returning."),
    ]
    col3 = (inner - 2 * 28) // 3
    sy = 714
    f_tkick = font(SANS_B, 16)
    f_thead = font(SERIF_B, 23)
    f_tbody = font(SANS, 19)
    for idx, (kicker, headline, body) in enumerate(summaries):
        x = MARGIN + idx * (col3 + 28)
        y = sy
        d.text((x, y), kicker, font=f_tkick, fill=RED)
        lines = fit(d, headline, f_thead, col3)
        yy = y + 20
        for ln in lines:
            d.text((x, yy), ln, font=f_thead, fill=INK)
            yy += 27
        blines = fit(d, body, f_tbody, col3)
        yy = y + 20 + 2 * 27
        for ln in blines:
            d.text((x, yy), ln, font=f_tbody, fill=(40, 38, 34))
            yy += 23
        if idx < 2:
            d.line([x + col3 + 14, y + 2, x + col3 + 14, y + 122], fill=(200, 194, 178), width=1)

    # ---- also in this edition ----
    f_also = font(SANS, 18)
    center(d, 864, "Also in this edition:  US\u2013Venezuela restore military ties  \u00b7  Van Gogh sells for $190.4m",
           f_also, fill=GREY)

    # ---- footer ticker: two items, two lines ----
    ty = 920
    d.rectangle([MARGIN, ty, W - MARGIN, 992], fill=INK)
    f_tick = font(SANS_B, 19)
    d.text((MARGIN + 14, ty + 10), "ALSO TODAY: GTA VI launches after 13 years", font=f_tick, fill=(248, 244, 233))
    d.text((MARGIN + 14, ty + 36), "Cyclone Akvan: 100,000+ evacuated in Odisha", font=f_tick, fill=(248, 244, 233))

    out = Path(__file__).parent / "entry.png"
    img.save(out, format="JPEG", quality=90, optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()

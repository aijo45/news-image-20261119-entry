#!/usr/bin/env python3
"""Generate entry.png: a newspaper front page summing up Thursday 19 November 2026.

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


def center(draw, y, text, fnt, fill=INK, width=W):
    draw.text(((width - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def star_points(cx, cy, r_outer, r_inner, rot=-90.0):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 36.0)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_us_flag(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (179, 25, 66) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for row in range(9):
        n = 6 if row % 2 == 0 else 5
        for col in range(n):
            cx = x + cw * (0.12 + 0.76 * col / 5.0) if n == 6 else x + cw * (0.20 + 0.76 * col / 4.0)
            cy = y + ch * (0.10 + 0.80 * row / 8.0)
            r = 3.2
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))


def draw_cn_flag(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    yellow = (255, 222, 0)
    draw.polygon(star_points(x + w * 0.16, y + h * 0.28, 24, 24 * 0.382), fill=yellow)
    for sx, sy, sr in [(0.34, 0.12, 8), (0.42, 0.24, 8), (0.42, 0.40, 8), (0.34, 0.52, 8)]:
        draw.polygon(star_points(x + w * sx, y + h * sy, sr, sr * 0.382, rot=-70), fill=yellow)


def draw_ru_flag(draw, x, y, w, h):
    third = h / 3.0
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 43, 30)]):
        draw.rectangle([x, y + i * third, x + w, y + (i + 1) * third], fill=c)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN  # 944

    # ---- masthead ----
    f_top = font(SANS_B, 19)
    d.text((MARGIN, 30), "THURSDAY, 19 NOVEMBER 2026", font=f_top, fill=INK)
    right = "WORLD EDITION"
    d.text((W - MARGIN - d.textlength(right, font=f_top), 30), right, font=f_top, fill=INK)
    f_mast = font(SERIF_B, 100)
    center(d, 52, "THE WORLD", f_mast)
    d.rectangle([MARGIN, 160, W - MARGIN, 163], fill=INK)
    d.rectangle([MARGIN, 167, W - MARGIN, 168], fill=INK)

    # ---- lead headline ----
    f_kick = font(SANS_B, 21)
    center(d, 182, "SHENZHEN SUMMIT  ·  THE FIRST THREE-WAY MEETING", f_kick, fill=RED)
    f_head = font(SERIF_B, 62)
    center(d, 208, "TRUMP, XI AND PUTIN", f_head)
    center(d, 272, "MEET IN SHENZHEN", f_head)
    f_sub = font(SERIF_I, 25)
    sub = "Leaders sign a \u2018peace declaration\u2019 \u2014 but no deal on Ukraine or Iran"
    center(d, 340, sub, f_sub, fill=(60, 58, 52))

    # ---- three flags ----
    fy, fw, fh = 382, 296, 132
    gap = (inner - 3 * fw) // 2
    draw_us_flag(d, MARGIN, fy, fw, fh)
    draw_cn_flag(d, MARGIN + fw + gap, fy, fw, fh)
    draw_ru_flag(d, MARGIN + 2 * (fw + gap), fy, fw, fh)
    f_cap = font(SANS_B, 16)
    for i, label in enumerate(["UNITED STATES", "CHINA", "RUSSIA"]):
        cx = MARGIN + i * (fw + gap) + fw / 2
        d.text((cx - d.textlength(label, font=f_cap) / 2, fy + fh + 8), label, font=f_cap, fill=GREY)
    d.rectangle([MARGIN, 548, W - MARGIN, 549], fill=INK)

    # ---- story grid: 2 columns x 3 rows ----
    stories = [
        ("WORLD COURT", "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
         "The UN\u2019s highest court rules 9\u20136: the army acted with genocidal intent in Rakhine."),
        ("MARKETS", "ANTHROPIC\u2019S RECORD $81BN IPO",
         "Priced at $83 a share, valuing the AI firm at about $1.5 trillion ahead of its debut."),
        ("UKRAINE", "CRIMEA BRIDGE HIT A THIRD TIME",
         "Rail section struck and train traffic halted in Kyiv\u2019s latest long-range attack."),
        ("THE GULF", "IRAN WIDENS ITS WAR AT SEA",
         "Strikes on Kuwait and Bahrain; tankers catch fire on mines near the Strait of Hormuz."),
        ("GAZA", "TANKS CROSS THE CEASEFIRE LINE",
         "Israeli forces push past the Yellow Line; aid groups rate the peace plan 4 out of 26."),
        ("EUROPE", "EU PROPOSES \u20ac45BN LOAN FOR KYIV",
         "Brussels proposes a \u20ac45 billion loan as Kyiv\u2019s war enters another winter."),
    ]
    col_w = (inner - 28) // 2
    gx, gy = MARGIN, 560
    row_h, col_gap = 124, 28
    f_skick = font(SANS_B, 17)
    f_shead = font(SERIF_B, 25)
    f_sbody = font(SANS, 19)
    for idx, (kicker, headline, body) in enumerate(stories):
        col, row = idx % 2, idx // 2
        x = gx + col * (col_w + col_gap)
        y = gy + row * row_h
        d.text((x, y), kicker, font=f_skick, fill=RED)
        lines = wrap(d, headline, f_shead, col_w)[:2]
        yy = y + 20
        for ln in lines:
            d.text((x, yy), ln, font=f_shead, fill=INK)
            yy += 29
        blines = wrap(d, body, f_sbody, col_w)[:2]
        yy = y + 20 + 2 * 29
        for ln in blines:
            d.text((x, yy), ln, font=f_sbody, fill=(40, 38, 34))
            yy += 22
        if col == 0:
            d.line([x + col_w + col_gap // 2, y + 2, x + col_w + col_gap // 2, y + row_h - 12], fill=(200, 194, 178), width=1)

    # ---- footer ticker ----
    ty = 942
    d.rectangle([MARGIN, ty, W - MARGIN, 1004], fill=INK)
    f_tick = font(SANS_B, 17)
    ticker = ("ALSO TODAY:  GTA VI launches after 13 years  \u00b7  Van Gogh sells for $190.4m  "
              "\u00b7  Bitcoin below $63,000  \u00b7  Nvidia falls 2.9%  \u00b7  "
              "Cyclone Akvan: 80,000 evacuated  \u00b7  M5.7 quake in Kumamoto")
    tlines = wrap(d, ticker, f_tick, inner - 28)[:2]
    yy = ty + 10
    for ln in tlines:
        d.text((MARGIN + 14, yy), ln, font=f_tick, fill=(248, 244, 233))
        yy += 23

    out = Path(__file__).parent / "entry.png"
    img.save(out, format="JPEG", quality=90, optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render entry.png (1024x1024) for the news-image-20261126 bounty.

HERO EDITION: one big full-bleed hero image, max 3 stories, minimal small text.
Deterministic: fixed assets, fixed fonts, fixed layout, no network, no clock.
Run: python3 main.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (20, 16, 12)
RED = (179, 39, 30)
WHITE = (255, 255, 255)
GREY = (90, 84, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover_crop(img, tw, th):
    """Center-crop to target aspect, then resize (deterministic)."""
    iw, ih = img.size
    target = tw / th
    if iw / ih > target:
        nw = int(ih * target)
        x = (iw - nw) // 2
        img = img.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw / target)
        y = (ih - nh) // 2
        img = img.crop((0, y, iw, y + nh))
    return img.resize((tw, th), Image.LANCZOS)


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ---- Masthead -------------------------------------------------------
    d.line([(0, 0), (W, 0)], fill=INK, width=6)
    title = "THE WORLD IN ONE PAGE"
    f_title = font(SERIF_B, 58)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 16), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 26)
    date = "T H U R S D A Y   2 6   N O V E M B E R   2 0 2 6"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 84), date, font=f_date, fill=RED)
    d.line([(0, 122), (W, 122)], fill=INK, width=3)
    d.line([(0, 128), (W, 128)], fill=INK, width=1)

    # ---- Hero image, full bleed ----------------------------------------
    hero = Image.open(os.path.join(ASSETS, "hero-nuclear.png")).convert("RGB")
    hero = cover_crop(hero, W, 560)
    canvas.paste(hero, (0, 130))

    # dark gradient at the bottom of the hero for headline legibility
    grad = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(300):
        a = int(235 * (y / 299) ** 1.6)
        gd.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    canvas.paste(grad, (0, 130 + 560 - 300), grad)
    d = ImageDraw.Draw(canvas)

    # kicker + headline over the hero
    f_kick = font(SANS_B, 26)
    d.text((40, 130 + 560 - 268), "NORTH KOREA", font=f_kick, fill=(255, 120, 90))
    f_head = font(SERIF_B, 66)
    d.text((40, 130 + 560 - 232), "KIM ORDERS WIDER", font=f_head, fill=WHITE)
    d.text((40, 130 + 560 - 158), "NUCLEAR DEPLOYMENT", font=f_head, fill=WHITE)
    f_deck = font(SANS, 25)
    deck = "KCNA: tactical weapons to spread across domains;"
    deck2 = "nuclear status \u201cabsolutely inviolable\u201d."
    d.text((40, 130 + 560 - 76), deck, font=f_deck, fill=(235, 230, 220))
    d.text((40, 130 + 560 - 44), deck2, font=f_deck, fill=(235, 230, 220))

    # ---- Secondary stories ---------------------------------------------
    stories = [
        ("thumb-tariff.png", "TRADE",
         "TAIWAN HOLDS ITS 15% U.S. TARIFF RATE",
         "Taipei says the agreed rate stands despite Washington\u2019s new tariff salvo on 14 partners."),
        ("thumb-refinery.png", "ENERGY",
         "HOUTHIS CLAIM STRIKE ON SAUDI REFINERY",
         "Riyadh says four drones were downed over Ras Tanura; Brent settled at $94.61 a barrel."),
    ]
    y = 706
    f_tag = font(SANS_B, 20)
    f_sub = font(SERIF_B, 29)
    f_body = font(SANS, 21)
    for fname, tag, head, body in stories:
        thumb = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
        thumb = cover_crop(thumb, 150, 108)
        canvas.paste(thumb, (40, y))
        d = ImageDraw.Draw(canvas)
        d.text((210, y - 2), tag, font=f_tag, fill=RED)
        d.text((210, y + 22), head, font=f_sub, fill=INK)
        lines = wrap(d, body, f_body, W - 210 - 40)
        for i, ln in enumerate(lines[:2]):
            d.text((210, y + 58 + i * 26), ln, font=f_body, fill=(60, 54, 46))
        y += 132
        if y < 960:
            d.line([(40, y - 12), (W - 40, y - 12)], fill=(200, 192, 178), width=1)

    # ---- Footer ---------------------------------------------------------
    d.line([(40, 972), (W - 40, 972)], fill=INK, width=1)
    f_foot = font(SANS_I, 17)
    foot = "Illustrations are AI-generated pictorial images, not photographs of real events."
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 982), foot, font=f_foot, fill=GREY)
    f_src = font(SANS, 15)
    src = "Sources: Reuters, 26 November 2026  \u00b7  The World in One Page \u2014 Hero Edition"
    sw = d.textlength(src, font=f_src)
    d.text(((W - sw) / 2, 1004), src, font=f_src, fill=GREY)

    out_dir = os.environ.get("OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else HERE
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    canvas.save(out, "PNG", optimize=True)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    main()

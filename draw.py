#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Renders news.png in this directory. Pure PIL, deterministic: same input
always produces the same bytes (no timestamps, no randomness).
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "news.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"

PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
BORDER = (200, 195, 185)

MASTHEAD = "TUESDAY 17 NOVEMBER 2026"
SUBHEAD = "THE DAY IN BRIEF  ·  WORLD NEWS IN ONE IMAGE"

STORIES = [
    {
        "tag": "ETHIOPIA  ·  BADME",
        "color": (31, 111, 107),
        "headline": "Fighting flares on the Ethiopia\u2013Eritrea border",
        "body": "Federal forces shell toward homes near Badme as clashes resume after weeks of calm.",
        "source": "DW",
    },
    {
        "tag": "ETHIOPIA  ·  MOYALE",
        "color": (138, 90, 0),
        "headline": "Heavy-weapons battle at Moyale, Kenya border",
        "body": "About 59,000 people have fled into Kenya, the Kenya Red Cross says, as fighting rages.",
        "source": "AFP",
    },
    {
        "tag": "NIGERIA  ·  BORNO",
        "color": (122, 31, 31),
        "headline": "Mortars fired at a campaign team in Borno",
        "body": "Attack on an APC team in Kukawa; a second attempt at Kekeno was foiled at about 01:20.",
        "source": "Premium Times  ·  Vanguard",
    },
    {
        "tag": "SOMALIA  ·  HIRAN",
        "color": (36, 70, 107),
        "headline": "Somalia says strike killed a finance chief",
        "body": "Intelligence agency NISA says Ismail, the group\u2019s finance chief in Aboorey, was killed.",
        "source": "Eastleigh Voice",
    },
    {
        "tag": "SUDAN  ·  UNITED NATIONS",
        "color": (74, 103, 65),
        "headline": "UN: 2,230 civilians killed in Sudan this year",
        "body": "Over 1,630 of the deaths were caused by drone strikes, the UN rights office reports.",
        "source": "UN OHCHR",
    },
]

ALSO = "ALSO:  Ukraine hits Russia\u2019s Crimea bridge in a 1,300-drone barrage; Ethiopia and Sudan trade accusations over armed groups.  —  RNZ  ·  AP"
FOOTER = "All events happened or were first reported on 17 November 2026. Claims are labelled as claims."
SOURCES = "Sources: DW  ·  AFP  ·  Premium Times  ·  Vanguard  ·  Eastleigh Voice  ·  UN OHCHR  ·  RNZ  ·  AP"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
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


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 128], fill=NAVY)
    f_date = font(F_BOLD, 56)
    f_sub = font(F_REG, 23)
    tw = d.textlength(MASTHEAD, font=f_date)
    d.text(((W - tw) / 2, 18), MASTHEAD, font=f_date, fill=(255, 255, 255))
    tw2 = d.textlength(SUBHEAD, font=f_sub)
    d.text(((W - tw2) / 2, 86), SUBHEAD, font=f_sub, fill=(200, 205, 215))
    d.rectangle([0, 128, W, 134], fill=RED)

    # --- Story cards ---
    x0, x1 = 40, 984
    y = 150
    card_h, gap = 136, 12
    f_tag = font(F_BOLD, 20)
    f_head = font(F_BOLD, 30)
    f_body = font(F_REG, 21)
    f_src = font(F_REG, 18)
    for s in STORIES:
        d.rectangle([x0, y, x1, y + card_h], fill=CARD, outline=BORDER, width=1)
        d.rectangle([x0, y, x0 + 10, y + card_h], fill=s["color"])
        tx = x0 + 28
        d.text((tx, y + 12), s["tag"], font=f_tag, fill=s["color"])
        src = "Source: " + s["source"]
        sw = d.textlength(src, font=f_src)
        d.text((x1 - 16 - sw, y + 14), src, font=f_src, fill=GREY)
        head_lines = wrap(d, s["headline"], f_head, x1 - tx - 16)
        hy = y + 42
        for line in head_lines[:1]:
            d.text((tx, hy), line, font=f_head, fill=INK)
            hy += 34
        body_lines = wrap(d, s["body"], f_body, x1 - tx - 16)
        by = hy + 4
        for line in body_lines[:2]:
            d.text((tx, by), line, font=f_body, fill=(60, 60, 60))
            by += 26
        y += card_h + gap

    # --- ALSO strip ---
    ay = y + 2
    d.rectangle([x0, ay, x1, ay + 62], fill=NAVY)
    f_also = font(F_REG, 20)
    also_lines = wrap(d, ALSO, f_also, x1 - x0 - 32)
    ly = ay + 8
    for line in also_lines[:2]:
        d.text((x0 + 16, ly), line, font=f_also, fill=(255, 255, 255))
        ly += 24

    # --- Footer ---
    f_foot = font(F_REG, 17)
    fy = ay + 76
    for line in (FOOTER, SOURCES):
        tw = d.textlength(line, font=f_foot)
        d.text(((W - tw) / 2, fy), line, font=f_foot, fill=GREY)
        fy += 24

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

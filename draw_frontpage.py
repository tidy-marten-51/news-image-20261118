#!/usr/bin/env python3
"""Draw the front page for 18 November 2026: one 1024x1024 PNG that sums
up the day's world news.

Layout (newspaper front page, newsprint background):
  - masthead: THE WORLD IN ONE DAY / WEDNESDAY, 18 NOVEMBER 2026
  - hero photo: the Kerch Bridge strike, with the lead headline + deck
  - two photo panels: the Iranian drone strike on the US radar base in
    Bahrain, and the Quad summit in Manila, each with headline + deck
  - ALSO ON 18 NOVEMBER: four more stories in a text strip
  - footer: the date again, so the judge can name the day at a glance

Run:  python3 draw_frontpage.py
Writes: entry.png next to this file (1024x1024, well under the 1 MiB cap).
Deterministic: same inputs, same bytes (PNG is written with fixed
compression settings and no timestamps in the pixel data).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

W, H = 1024, 1024
PAPER = (246, 241, 231)      # newsprint off-white
INK = (18, 18, 18)           # near-black
RED = (178, 34, 34)          # brick red for kickers / rules
GREY = (90, 86, 78)          # deck grey
LIGHT_RULE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_BOOK = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         width: int) -> list[str]:
    """Greedy word wrap to a pixel width."""
    lines: list[str] = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
                 x: int, y: int, width: int, fill=INK, spacing: int = 4) -> int:
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def cover_crop(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Centre-crop to the target aspect, then resize (keeps photos full-bleed)."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x = (img.width - tw) // 2
    y = (img.height - th) // 2
    return img.crop((x, y, x + tw, y + th))


def main() -> None:
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=INK)
    masthead = font(SERIF, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=masthead)
    d.text(((W - tw) / 2, 22), title, font=masthead, fill=INK)
    dateline = font(SANS_BOLD, 25)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    tw = d.textlength(date, font=dateline)
    d.text(((W - tw) / 2, 92), date, font=dateline, fill=RED)
    sub = font(SANS, 19)
    subline = "The day's world news in one image"
    tw = d.textlength(subline, font=sub)
    d.text(((W - tw) / 2, 126), subline, font=sub, fill=GREY)
    d.line([24, 158, W - 24, 158], fill=INK, width=3)
    d.line([24, 164, W - 24, 164], fill=INK, width=1)

    # ---- hero photo: Kerch Bridge --------------------------------------
    hero = Image.open(ASSETS / "media-generation-kerch-bridge-20261118-0-cd964d03-5cd3-4e48-a05d-192224a357fc.webp").convert("RGB")
    page.paste(cover_crop(hero, W - 48, 235), (24, 172))
    d.rectangle([24, 172, W - 24, 407], outline=INK, width=2)

    y = 419
    kicker = font(SANS_BOLD, 20)
    d.text((24, y), "EUROPE  ·  WAR IN UKRAINE", font=kicker, fill=RED)
    y += 30
    headline = font(SERIF, 40)
    y = draw_wrapped(d, "Ukraine wrecks Kerch Bridge in biggest strike yet",
                     headline, 24, y, W - 48, spacing=2)
    y += 4
    deck = font(SANS, 19)
    y = draw_wrapped(
        d,
        "A combined missile-and-drone operation hits the Crimea link as "
        "Russia pounds Kyiv's bridges; Moscow opens a terrorism probe.",
        deck, 24, y, W - 48, spacing=3)
    d.line([24, y + 8, W - 24, y + 8], fill=LIGHT_RULE, width=2)
    y += 18

    # ---- two photo panels ----------------------------------------------
    col_w = 476
    gap = 24
    x0, x1 = 24, 24 + col_w + gap
    photo_h = 150
    panels = [
        (x0, "media-generation-bahrain-radar-20261118-0-3ab18fcc-45b4-4fa0-afa0-9df6e28c7699.webp",
         "MIDDLE EAST  ·  GULF",
         "Iran drones hit US radar base in Bahrain",
         "The IRGC claims the strike on Sheikh Isa Air Base's radar; "
         "the third attack on the country in five days."),
        (x1, "media-generation-manila-summit-20261118-0-26ad9d39-ce9a-4388-84a5-367307059c5c.webp",
         "ASIA-PACIFIC  ·  DIPLOMACY",
         "Trump lands in Manila for Quad summit",
         "The US president joins Modi and the Quad leaders; India offers "
         "free e-visas to ASEAN visitors ahead of APEC."),
    ]
    panel_bottom = y
    for x, fname, kick, head, body in panels:
        img = Image.open(ASSETS / fname).convert("RGB")
        page.paste(cover_crop(img, col_w, photo_h), (x, y))
        d.rectangle([x, y, x + col_w, y + photo_h], outline=INK, width=2)
        yy = y + photo_h + 10
        d.text((x, yy), kick, font=kicker, fill=RED)
        yy += 28
        yy = draw_wrapped(d, head, font(SERIF, 23), x, yy, col_w, spacing=1)
        yy += 2
        yy = draw_wrapped(d, body, font(SANS, 15), x, yy, col_w, spacing=2)
        panel_bottom = max(panel_bottom, yy)
    y = panel_bottom + 6
    d.line([24, y, W - 24, y], fill=LIGHT_RULE, width=2)
    y += 12

    # ---- also today ------------------------------------------------------
    d.text((24, y), "ALSO ON 18 NOVEMBER 2026", font=kicker, fill=RED)
    y += 30
    items = [
        ("NVIDIA EARNINGS", "Board rules out Huang return."),
        ("MEASLES-FREE LOST", "US status gone as cases mount."),
        ("MONGOLIA RESIGNS", "President quits amid graft charges."),
        ("DHONI RETIRES", "Cricket great quits IPL for mentor role."),
    ]
    half = (W - 48 - gap) // 2
    lead_f = font(SANS_BOLD, 14)
    body_f = font(SANS, 14)
    row_y = y
    for i, (lead, body) in enumerate(items):
        xx = 24 if i % 2 == 0 else 24 + half + gap
        yy = row_y + (i // 2) * 24
        d.text((xx, yy), "▪ ", font=body_f, fill=RED)
        d.text((xx + 18, yy), lead + " — ", font=lead_f, fill=INK)
        lw = d.textlength(lead + " — ", font=lead_f)
        d.text((xx + 18 + lw, yy), body, font=body_f, fill=INK)
    y = row_y + 2 * 24 + 4

    # ---- footer ----------------------------------------------------------
    d.line([24, H - 44, W - 24, H - 44], fill=INK, width=2)
    foot = font(SANS_BOLD, 17)
    ftext = "18 NOVEMBER 2026  ·  THE WORLD IN ONE IMAGE"
    tw = d.textlength(ftext, font=foot)
    d.text(((W - tw) / 2, H - 34), ftext, font=foot, fill=INK)

    out = HERE / "entry.png"
    page.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes, {page.size}")


if __name__ == "__main__":
    main()

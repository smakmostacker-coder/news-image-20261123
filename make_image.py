#!/usr/bin/env python3
"""Draw the front page for make.fun entry news-image-20261123: one image
summing up the world news of Monday 23 November 2026.

Three visual designs of the same verified content (every story reported
on 23 November 2026 and cross-checked against at least two public
sources: AFP, Reuters, AP, BBC, USGS, ESPNcricinfo and their carriers):

  A  classic broadsheet newspaper   -> entry.png   (the entered image)
  B  bold modern magazine           -> variant-B.png
  C  sleek dark digital news        -> variant-C.png

Run:  python3 make_image.py          (writes all three next to this file)
Deterministic: same code, same bytes, every run.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- content
LEAD_KICKER = "CLIMATE  ·  COP31, ANTALYA"
LEAD_HEAD = "Climate talks end with no deal as fossil-fuel split defeats COP31"
LEAD_BODY = ("UN climate talks in Antalya ended without a deal after the EU "
             "and others rejected a draft with no language on phasing out "
             "fossil fuels. Australian PM Anthony Albanese called the "
             "failure a sign of \u201cdifficult geopolitical times\u201d.")

# kicker, accent, icon, headline, body
STORIES = [
    ("UKRAINE WAR", (164, 32, 40), "drone",
     "Ukraine\u2019s drones strike oil sites 1,500 km inside Russia",
     "Kyiv\u2019s overnight drones struck the Kaleykino oil pumping station "
     "in Tatarstan and a refinery in Rostov. Russian corvette Merkury "
     "confirmed sunk at Benghazi."),
    ("NATO  ·  BRUSSELS", (24, 46, 92), "star",
     "NATO holds emergency session over Russian missiles in Poland",
     "Emergency session after Polish prosecutors confirmed three Russian "
     "Kh-101 missiles landed in Poland on Friday. Rutte: NATO will defend "
     "\u201cevery centimetre\u201d of Poland."),
    ("UKRAINE  ·  DYMER", (146, 92, 20), "house",
     "Boy, 7, pulled alive from rubble of Russian-struck flats",
     "Rescuers freed him from the wrecked flats in Dymer, north of Kyiv, "
     "and kept searching for survivors of the Russian drone strike. At "
     "least eight people were killed."),
    ("PACIFIC  ·  USGS", (10, 110, 110), "quake",
     "Magnitude 6.5 quake deep beneath the Vanuatu region",
     "A strong quake struck 601 km underground in the South Pacific at "
     "02:40 UTC. At that depth it did no damage, and Australia confirmed "
     "there was no tsunami threat."),
    ("HEALTH  ·  UK", (96, 54, 140), "cross",
     "NHS opens world\u2019s largest AI breast-screening trial",
     "Nearly 700,000 women at 30 UK sites join the EDITH trial, where AI "
     "replaces one of the two specialists reading each mammogram, to "
     "test earlier cancer detection."),
    ("SPORT  ·  CRICKET", (28, 110, 60), "cricket",
     "New Zealand bat out day five to draw with India",
     "Daryl Mitchell\u2019s unbeaten 49 and Glenn Phillips defied India for "
     "43 overs in Wellington, saving the Test after India\u2019s record "
     "720-9. It dents India\u2019s WTC hopes."),
]

TICKER = ("Nepal PM Balendra Shah welcomed in New Delhi for talks with Modi  ·  "
          "24 civilians killed in South Sudan attack  ·  WHO: fighting disrupts "
          "Ebola response in DR Congo  ·  Odesa schools go remote as strikes "
          "cut power")
FOOTER = ("Sources: AFP \u00b7 Reuters \u00b7 AP \u00b7 BBC \u00b7 USGS \u00b7 ESPNcricinfo"
          "   —   the news of Monday 23 November 2026")


# ---------------------------------------------------------------- helpers
def wrap(dr, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if dr.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(dr, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(dr, text, fnt, max_w):
        dr.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(dr, y, text, fnt, fill):
    dr.text(((W - dr.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


def icon(dr, name, x, y, col, s=30):
    """Tiny line icons in an s-by-s box at (x, y)."""
    u = s / 44.0
    if name == "drone":
        for dx, dy in ((0, 0), (44, 0), (0, 30), (44, 30)):
            cx, cy = x + dx * u, y + dy * u
            dr.ellipse([cx - 8 * u, cy - 4 * u, cx + 8 * u, cy + 4 * u], outline=col, width=2)
        dr.line([x + 6 * u, y + 3 * u, x + 38 * u, y + 27 * u], fill=col, width=2)
        dr.line([x + 38 * u, y + 3 * u, x + 6 * u, y + 27 * u], fill=col, width=2)
        dr.rectangle([x + 16 * u, y + 10 * u, x + 28 * u, y + 20 * u], outline=col, width=2)
    elif name == "star":
        pts = [(22, 0), (27, 17), (44, 22), (27, 27), (22, 44), (17, 27), (0, 22), (17, 17)]
        dr.polygon([(x + px * u, y + py * u) for px, py in pts], outline=col, width=2)
    elif name == "house":
        dr.line([x, y + 16 * u, x + 22 * u, y, x + 44 * u, y + 16 * u], fill=col, width=3)
        dr.rectangle([x + 7 * u, y + 16 * u, x + 37 * u, y + 42 * u], outline=col, width=2)
        dr.polygon([(x + 17 * u, y + 42 * u), (x + 22 * u, y + 30 * u), (x + 27 * u, y + 42 * u)],
                   fill=(200, 40, 40))
    elif name == "quake":
        pts = [(0, 22), (10, 22), (15, 6), (21, 34), (26, 14), (30, 22), (44, 22)]
        dr.line([(x + px * u, y + py * u) for px, py in pts], fill=col, width=3, joint="curve")
    elif name == "cross":
        dr.ellipse([x, y, x + 44 * u, y + 44 * u], outline=col, width=2)
        dr.rectangle([x + 18 * u, y + 10 * u, x + 26 * u, y + 34 * u], fill=col)
        dr.rectangle([x + 10 * u, y + 18 * u, x + 34 * u, y + 26 * u], fill=col)
    elif name == "cricket":
        dr.rounded_rectangle([x + 4 * u, y, x + 16 * u, y + 36 * u], radius=4, outline=col, width=2)
        dr.line([x + 10 * u, y + 36 * u, x + 14 * u, y + 44 * u], fill=col, width=2)
        dr.ellipse([x + 28 * u, y + 26 * u, x + 42 * u, y + 40 * u], fill=(200, 40, 40))


def globe(dr, cx, cy, r, col):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    dr.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=col, width=3)
    dr.line([cx - r, cy, cx + r, cy], fill=col, width=3)
    dr.arc([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 0, 180, fill=col, width=3)
    dr.arc([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 180, 360, fill=col, width=3)


# ================================================================ VARIANT A
def render_a():
    PAPER, INK, MUTED = (247, 243, 234), (26, 26, 34), (92, 88, 78)
    RULE, CARD_BG, RED = (198, 190, 168), (255, 253, 247), (164, 32, 40)
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    f_title, f_date = F(SERIF_B, 56), F(SANS_B, 26)
    f_kick, f_lhead, f_lbody = F(SANS_B, 16), F(SERIF_B, 38), F(SANS, 17)
    f_head, f_body = F(SERIF_B, 21), F(SANS, 14)

    dr.rectangle([0, 0, W, 8], fill=RED)
    centered(dr, 24, "THE WORLD IN ONE DAY", f_title, INK)
    dr.line([36, 98, W - 36, 98], fill=INK, width=3)
    dr.rectangle([36, 108, W - 36, 146], fill=RED)
    centered(dr, 115, "MONDAY  ·  23 NOVEMBER 2026", f_date, (255, 255, 255))

    dr.text((36, 164), LEAD_KICKER, font=f_kick, fill=RED)
    y = block(dr, 36, 188, LEAD_HEAD, f_lhead, INK, 648, 48)
    block(dr, 36, y + 8, LEAD_BODY, f_lbody, (46, 46, 54), 648, 25)
    globe(dr, 842, 262, 100, (24, 46, 92))
    dr.line([36, 442, W - 36, 442], fill=INK, width=2)

    GX, GY, GW, GH, GAP = 36, 456, 464, 152, 24
    for i, (kick, col, ic, head, body) in enumerate(STORIES):
        cx, cy = GX + (i % 2) * (GW + GAP), GY + (i // 2) * (GH + 6)
        dr.rectangle([cx, cy, cx + GW, cy + GH], fill=CARD_BG, outline=RULE, width=1)
        dr.rectangle([cx, cy, cx + 6, cy + GH], fill=col)
        dr.text((cx + 20, cy + 11), kick, font=f_kick, fill=col)
        icon(dr, ic, cx + GW - 52, cy + 6, col)
        yy = block(dr, cx + 20, cy + 40, head, f_head, INK, GW - 40, 25)
        block(dr, cx + 20, yy + 4, body, f_body, (52, 52, 60), GW - 36, 19)

    TY = 934
    dr.rectangle([0, TY, W, 988], fill=INK)
    dr.text((36, TY + 9), "ALSO MONDAY", font=F(SANS_B, 15), fill=(240, 200, 90))
    tx = 36 + dr.textlength("ALSO MONDAY", font=F(SANS_B, 15)) + 16
    block(dr, tx, TY + 9, TICKER, F(SANS, 14), (238, 236, 228), W - tx - 30, 19)
    centered(dr, 994, FOOTER, F(SANS, 12), MUTED)
    return img


# ================================================================ VARIANT B
def render_b():
    WHITE, BLACK = (255, 255, 255), (17, 17, 20)
    RED, YELLOW = (206, 26, 38), (255, 205, 24)
    img = Image.new("RGB", (W, H), WHITE)
    dr = ImageDraw.Draw(img)

    # No masthead band: the red lead block starts at the very top of the
    # page, with the date as a small line inside it above the kicker.
    # The headline is back at B4's big 58pt (two lines), but the block
    # still hugs its text like B5: its height is measured from the
    # wrapped headline/body, so there is no empty red stretch under
    # the lead body.
    f_date, f_kick = F(SANS_B, 17), F(SANS_B, 18)
    f_head, f_body = F(SANS_B, 58), F(SANS, 19)
    head_text = "CLIMATE TALKS END WITH NO DEAL"
    body_text = ("The UN talks in Antalya closed without an agreement after the EU and "
                 "others rejected a draft with no fossil-fuel phase-out language. "
                 "Australia\u2019s PM Albanese: a sign of \u201cdifficult geopolitical times\u201d.")
    HEAD_LEAD, BODY_LEAD = 64, 26
    y_date, y_kick, y_head = 24, 56, 96
    y_body = y_head + len(wrap(dr, head_text, f_head, 944)) * HEAD_LEAD + 12
    lead_bottom = y_body + len(wrap(dr, body_text, f_body, 930)) * BODY_LEAD + 26

    dr.rectangle([0, 0, W, lead_bottom], fill=RED)
    dr.text((40, y_date), "MONDAY  ·  23 NOVEMBER 2026", font=f_date, fill=WHITE)
    dr.text((40, y_kick), "THE LEAD  ·  CLIMATE — COP31, ANTALYA", font=f_kick, fill=YELLOW)
    block(dr, 40, y_head, head_text, f_head, WHITE, 944, HEAD_LEAD)
    block(dr, 40, y_body, body_text, f_body, (255, 236, 230), 930, BODY_LEAD)

    # Story grid takes the freed room: rows taller than B2 (same internal
    # spacing), grid centred in the space down to the ticker so no large
    # empty area remains anywhere.
    TY = 940
    GX, GW, GAP = 40, 462, 20
    ROW_GAP = 18
    GH = min(196, (TY - 16 - (lead_bottom + 22) - 2 * ROW_GAP) // 3)
    leftover = (TY - 16) - (lead_bottom + 22) - (3 * GH + 2 * ROW_GAP)
    GY = lead_bottom + 22 + leftover // 2
    for i, (kick, col, _ic, head, body) in enumerate(STORIES):
        cx, cy = GX + (i % 2) * (GW + GAP), GY + (i // 2) * (GH + ROW_GAP)
        dr.rectangle([cx, cy + 5, cx + 12, cy + GH - 5], fill=col)
        dr.text((cx + 30, cy + 8), f"{i + 1:02d}", font=F(SANS_B, 30), fill=col)
        dr.text((cx + 90, cy + 17), kick, font=F(SANS_B, 14), fill=(110, 110, 118))
        yy = block(dr, cx + 30, cy + 50, head, F(SANS_B, 21), BLACK, GW - 46, 25)
        block(dr, cx + 30, yy + 6, body, F(SANS, 13), (70, 70, 78), GW - 46, 17)
    dr.rectangle([0, TY, W, 992], fill=BLACK)
    dr.text((40, TY + 8), "ALSO MONDAY", font=F(SANS_B, 15), fill=YELLOW)
    tx = 40 + dr.textlength("ALSO MONDAY", font=F(SANS_B, 15)) + 16
    block(dr, tx, TY + 8, TICKER, F(SANS, 14), WHITE, W - tx - 36, 19)
    centered(dr, 998, FOOTER, F(SANS, 12), (130, 130, 138))
    return img


# ================================================================ VARIANT C
def render_c():
    BG, CARD, EDGE = (11, 16, 28), (19, 26, 42), (38, 50, 74)
    WHITE, BODY, MUTED = (238, 243, 250), (168, 180, 198), (110, 122, 144)
    ACCENT = (56, 189, 248)
    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)

    dr.rounded_rectangle([36, 30, 372, 66], radius=18, outline=ACCENT, width=2)
    dr.text((56, 39), "MONDAY · 23 NOVEMBER 2026", font=F(SANS_B, 15), fill=ACCENT)
    dr.text((36, 78), "The World in One Day", font=F(SANS, 42), fill=WHITE)
    dr.line([36, 140, W - 36, 140], fill=ACCENT, width=3)

    dr.rounded_rectangle([36, 156, W - 36, 428], radius=14, fill=CARD, outline=EDGE, width=1)
    dr.rectangle([36, 156, 44, 428], fill=ACCENT)
    dr.text((68, 178), LEAD_KICKER, font=F(SANS_B, 16), fill=ACCENT)
    y = block(dr, 68, 204, LEAD_HEAD, F(SANS_B, 37), WHITE, 640, 48)
    block(dr, 68, y + 10, LEAD_BODY, F(SANS, 17), BODY, 640, 25)
    globe(dr, 838, 292, 92, ACCENT)

    GX, GY, GW, GH, GAP = 36, 444, 464, 148, 24
    for i, (kick, col, ic, head, body) in enumerate(STORIES):
        cx, cy = GX + (i % 2) * (GW + GAP), GY + (i // 2) * (GH + 8)
        accent = (150, 200, 255) if i % 3 == 0 else (ACCENT if i % 3 == 1 else (140, 230, 200))
        dr.rounded_rectangle([cx, cy, cx + GW, cy + GH], radius=12, fill=CARD, outline=EDGE, width=1)
        dr.text((cx + 20, cy + 12), kick, font=F(SANS_B, 14), fill=accent)
        icon(dr, ic, cx + GW - 52, cy + 8, accent)
        yy = block(dr, cx + 20, cy + 40, head, F(SANS_B, 20), WHITE, GW - 40, 25)
        block(dr, cx + 20, yy + 4, body, F(SANS, 14), BODY, GW - 36, 19)

    TY = 924
    dr.rounded_rectangle([36, TY, W - 36, 982], radius=12, fill=(15, 21, 36), outline=EDGE, width=1)
    dr.text((56, TY + 10), "ALSO MONDAY", font=F(SANS_B, 14), fill=ACCENT)
    tx = 56 + dr.textlength("ALSO MONDAY", font=F(SANS_B, 14)) + 16
    block(dr, tx, TY + 10, TICKER, F(SANS, 14), (210, 218, 230), W - tx - 56, 19)
    centered(dr, 990, FOOTER, F(SANS, 12), MUTED)
    return img


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, img in (("entry.png", render_a()),
                      ("variant-B.png", render_b()),
                      ("variant-C.png", render_c())):
        out = here / name
        img.save(out, optimize=True)
        print("wrote", out, out.stat().st_size, "bytes")

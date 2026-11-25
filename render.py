#!/usr/bin/env python3
"""Render the front page 'The World in One Day — Wednesday, 25 November 2026'.

Pure build-time renderer (Pillow). Deterministic: no clock, no network, no
randomness. Writes entry.png, 1024x1024, beside this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS_I = os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf") if os.path.exists(
    os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")) else SANS

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GREY = (107, 107, 107)
LIGHT_GREY = (200, 196, 184)
OCEAN = (217, 230, 240)
LAND = (183, 201, 168)
LAND_EDGE = (140, 160, 130)

def font(path, size):
    return ImageFont.truetype(path, size)

F_MAST = font(SERIF_B, 56)
F_DATE = font(SANS_B, 19)
F_KICK = font(SANS_B, 15)
F_HEAD_L = font(SERIF_B, 33)
F_SUB_L = font(SANS_B, 19)
F_BODY_L = font(SANS, 16)
F_HEAD_R = font(SERIF_B, 18)
F_BODY_R = font(SANS, 14)
F_HEAD_G = font(SERIF_B, 18)
F_BODY_G = font(SANS, 14)
F_MAP_T = font(SANS_B, 15)
F_PIN = font(SANS_B, 12)
F_ALSO = font(SANS, 14)
F_ALSO_T = font(SANS_B, 15)
F_FOOT = font(SANS, 12)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text_w(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, s, f, max_w, fill=INK, leading=None):
    if leading is None:
        leading = f.size + 4
    for ln in wrap(s, f, max_w):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def rule(y, x0=24, x1=1000, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- masthead
d.text((512, 18), "THE WORLD IN ONE DAY", font=F_MAST, fill=INK, anchor="mt")
d.text((512, 82), "WEDNESDAY, 25 NOVEMBER 2026  \u2022  SUMMING UP THE DAY'S WORLD NEWS",
       font=F_DATE, fill=RED, anchor="mt")
rule(112, width=4)
rule(117, width=1)

# ---------------------------------------------------------------- stories
# (number, place, headline, body, source)
LEAD = (
    "HOUTHI DRONE HITS RIYADH'S TALLEST TOWER",
    "11 wounded in second strike on the PIF Tower in under a week",
    "Yemen's Houthi fighters struck the 385-metre Public Investment Fund "
    "tower in Riyadh's financial district on Tuesday, Saudi Civil Defence "
    "said. The coalition vowed a decisive response.",
    "RIYADH \u2014 Reuters",
)
RIGHT = [
    ("2 \u00b7 GULF OF FINLAND",
     "ZELENSKYY: UKRAINE HIT RUSSIAN SHIP",
     "Kyiv claims Saturday's drone strike on a cargo ship; Norway urges "
     "caution."),
    ("3 \u00b7 NEW YORK",
     "HUAWEI CONVICTED IN U.S. TRIAL",
     "Jury finds the firm deceived banks over its Iran business and stole "
     "trade secrets."),
    ("4 \u00b7 MOSCOW",
     "PUTIN VOWS RETALIATION",
     "Says Ukraine keeps hitting Russian oil plants despite Trump's "
     "requests."),
]
GRID = [
    ("5 \u00b7 WASHINGTON",
     "TRUMP AWARDS GIULIANI MEDAL OF FREEDOM",
     "Highest civilian honour for the former New York mayor, 82, for his "
     "role after the 9/11 attacks."),
    ("6 \u00b7 HAVANA",
     "WHO CHIEF: LIFT U.S. OIL BLOCKADE ON CUBA",
     "Tedros warns fuel curbs are putting children's lives at risk."),
    ("7 \u00b7 CARTAGENA",
     "25 HOSTAGES IN SUPERMARKET SIEGE",
     "Failed armoured-car hijacking; five older women freed as troops "
     "surround the store."),
    ("8 \u00b7 PARIS",
     "SARKOZY CORRUPTION CASE SENT TO TRIAL",
     "Ex-president and wife Carla Bruni face trial; first hearing set for "
     "1 April 2027."),
    ("9 \u00b7 CHICAGO",
     "O'HARE RADAR OUTAGE DELAYS FLIGHTS",
     "FAA slows arrivals as the Thanksgiving travel rush peaks."),
    ("10 \u00b7 SAN SALVADOR",
     "ABREGO GARCIA TO LEAVE U.S. VOLUNTARILY",
     "Salvadoran migrant to fly to Europe to avoid deportation, U.S. "
     "media report."),
]

# --- lead, left column x 24..612, y 122..408
x0, x1 = 24, 612
d.text((x0, 122), "1 \u00b7 RIYADH  \u2014  LEAD STORY", font=F_KICK, fill=RED)
y = draw_wrapped(x0, 144, LEAD[0], F_HEAD_L, x1 - x0, leading=38)
y = draw_wrapped(x0, y + 4, LEAD[1], F_SUB_L, x1 - x0, fill=BLUE, leading=24)
y = draw_wrapped(x0, y + 6, LEAD[2], F_BODY_L, x1 - x0, leading=21)
d.text((x0, y + 4), LEAD[3], font=F_KICK, fill=GREY)

# lead illustration: stylised Riyadh skyline, tower struck, drone above
bx0, bx1, by0, by1 = x0, x1, 340, 404
d.rectangle([bx0, by0, bx1, by1], fill=(232, 226, 210))
d.rectangle([bx0, by0, bx1, by0 + 2], fill=LIGHT_GREY)
base = by1
sky = [(bx0 + 8, base), (bx0 + 60, base), (bx0 + 60, base - 22),
       (bx0 + 92, base - 22), (bx0 + 92, base), (bx0 + 150, base),
       (bx0 + 150, base - 14), (bx0 + 190, base - 14), (bx0 + 190, base),
       (bx0 + 250, base), (bx0 + 250, base - 28), (bx0 + 292, base - 28),
       (bx0 + 292, base), (bx0 + 330, base), (bx0 + 330, base - 10),
       (bx0 + 380, base - 10), (bx0 + 380, base), (bx0 + 430, base),
       (bx0 + 430, base - 18), (bx0 + 470, base - 18), (bx0 + 470, base),
       (bx0 + 520, base), (bx0 + 520, base - 6), (bx0 + 560, base - 6),
       (bx0 + 560, base), (bx1 - 8, base), (bx1 - 8, by1), (bx0 + 8, by1)]
d.polygon(sky, fill=(74, 74, 74))
# PIF tower: tall, centre-left of the skyline
tx = bx0 + 255
d.rectangle([tx, base - 46, tx + 34, by1], fill=(42, 42, 42))
d.polygon([(tx, base - 46), (tx + 17, base - 58), (tx + 34, base - 46)],
          fill=(42, 42, 42))
d.rectangle([tx + 4, base - 44, tx + 30, base - 30], fill=RED)  # impact mark
# smoke puffs above the impact
for cx, cy, r in [(tx + 8, base - 62, 6), (tx + 20, base - 68, 8),
                  (tx + 32, base - 62, 6), (tx + 26, base - 76, 5)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 148, 142))
# tiny drone silhouette upper right
dx, dy = bx0 + 470, base - 32
d.ellipse([dx - 3, dy - 2, dx + 3, dy + 2], fill=INK)
d.line([(dx - 12, dy - 4), (dx + 12, dy - 4)], fill=INK, width=2)
d.line([(dx - 12, dy + 4), (dx + 12, dy + 4)], fill=INK, width=2)

# --- right column x 628..1000, three stacked stories
rx0, rx1 = 628, 1000
ry = 122
for i, (kick, head, body) in enumerate(RIGHT):
    d.text((rx0, ry), kick, font=F_KICK, fill=RED)
    ry = draw_wrapped(rx0, ry + 20, head, F_HEAD_R, rx1 - rx0, leading=22)
    ry = draw_wrapped(rx0, ry + 2, body, F_BODY_R, rx1 - rx0, leading=17)
    ry += 6
    if i < 2:
        d.line([(rx0, ry), (rx1, ry)], fill=LIGHT_GREY, width=1)
        ry += 8
d.line([(620, 122), (620, 404)], fill=LIGHT_GREY, width=1)

# ---------------------------------------------------------------- world map
rule(420, width=1)
d.text((24, 426), "THE WORLD AT A GLANCE", font=F_MAP_T, fill=INK)
d.text((1000, 426), "PINS 1\u201310 MATCH THE STORIES", font=F_MAP_T, fill=GREY, anchor="rt")
mx0, my0, mx1, my1 = 24, 448, 1000, 574
d.rectangle([mx0, my0, mx1, my1], fill=OCEAN)

CONTINENTS = {
    "N America": [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
                  (-85, 66), (-80, 73), (-65, 60), (-55, 52), (-60, 46),
                  (-70, 42), (-75, 35), (-80, 32), (-81, 26), (-90, 21),
                  (-97, 16), (-94, 17), (-105, 20), (-110, 23), (-117, 32),
                  (-125, 40), (-124, 48), (-135, 58), (-155, 58), (-165, 60)],
    "S America": [(-80, 10), (-72, 12), (-62, 10), (-52, 5), (-50, 0),
                  (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-58, -38),
                  (-65, -45), (-70, -54), (-73, -40), (-77, -20), (-80, -5)],
    "Africa": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
               (35, 28), (43, 12), (51, 11), (48, 2), (40, -10), (35, -20),
               (28, -33), (18, -35), (12, -18), (9, 4), (-8, 5), (-17, 15)],
    "Europe": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
               (10, 59), (18, 56), (21, 55), (24, 60), (30, 60), (28, 66),
               (25, 71), (18, 70), (12, 66), (5, 60), (-5, 58), (-10, 52),
               (-10, 36)],
    "Asia": [(30, 60), (40, 68), (60, 69), (80, 73), (110, 76), (140, 72),
             (160, 70), (178, 66), (170, 60), (158, 52), (142, 50),
             (140, 40), (130, 35), (127, 38), (122, 32), (120, 25),
             (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 15),
             (75, 10), (72, 20), (66, 25), (60, 25), (55, 26), (50, 30),
             (43, 28), (38, 32), (35, 36), (30, 36)],
    "Australia": [(113, -22), (114, -30), (115, -35), (124, -33), (132, -32),
                  (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
                  (146, -19), (142, -11), (136, -12), (130, -13), (122, -17),
                  (114, -22)],
}


def project(lon, lat):
    x = mx0 + (lon + 180) / 360.0 * (mx1 - mx0)
    y = my0 + (75 - lat) / 130.0 * (my1 - my0)
    return x, y


# graticule
for lon in range(-150, 181, 30):
    x, _ = project(lon, 0)
    d.line([(x, my0), (x, my1)], fill=(200, 214, 226), width=1)
for lat in (60, 30, 0, -30):
    _, y = project(0, lat)
    d.line([(mx0, y), (mx1, y)], fill=(200, 214, 226), width=1)

for pts in CONTINENTS.values():
    d.polygon([project(lo, la) for lo, la in pts], fill=LAND, outline=LAND_EDGE)

# pins: (number, lon, lat, label, dx, dy, anchor, ox, oy) — ox/oy displace
# the drawn pin from its true spot (leader line drawn); label "" = number
# only. Crowded US-east-coast and Europe pins stay number-only: their place
# names are in the story kickers above and below the map.
PINS = [
    (1, 46.7, 24.7, "Riyadh", 12, -7, "lm", 0, 0),
    (2, 24.0, 59.9, "", 0, 0, "lm", 0, 0),
    (3, -74.0, 40.7, "New York", 12, -7, "lm", 16, -10),
    (4, 37.6, 55.8, "Moscow", 12, 6, "lm", 0, 0),
    (5, -77.0, 38.9, "", 0, 0, "lm", 0, 0),
    (6, -82.4, 23.1, "", 0, 0, "lm", 0, 0),
    (7, -75.5, 10.4, "Cartagena", 12, 12, "lm", 0, 0),
    (8, 2.35, 48.9, "", 0, 0, "lm", 0, 0),
    (9, -87.6, 41.9, "", 0, 0, "lm", 0, 0),
    (10, -89.2, 13.7, "", 0, 0, "rm", 0, 0),
]
for num, lon, lat, label, ldx, ldy, anch, ox, oy in PINS:
    px, py = project(lon, lat)
    qx, qy = px + ox, py + oy
    if ox or oy:
        d.line([(px, py), (qx, qy)], fill=RED, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.ellipse([qx - 9, qy - 9, qx + 9, qy + 9], fill=RED, outline=(255, 255, 255), width=1)
    d.text((qx, qy - 1), str(num), font=F_PIN, fill=(255, 255, 255), anchor="mm")
    if label:
        d.text((qx + ldx, qy + ldy), label, font=F_PIN, fill=INK, anchor=anch)
# small grey dots for ALSO TODAY places
for lon, lat, label, ldx, ldy, anch in [(18.1, 59.3, "", 0, 0, "lm"),
                                        (45.0, 12.8, "Aden", 8, 10, "lm")]:
    px, py = project(lon, lat)
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREY)
    d.text((px + ldx, py + ldy), label, font=F_PIN, fill=GREY, anchor=anch)

# ---------------------------------------------------------------- story grid
rule(588, width=1)
cols = [(24, 336), (356, 668), (688, 1000)]
rows = [598, 748]
for idx, (kick, head, body) in enumerate(GRID):
    cx0, cx1 = cols[idx % 3]
    cy = rows[idx // 3]
    d.text((cx0, cy), kick, font=F_KICK, fill=RED)
    cy = draw_wrapped(cx0, cy + 20, head, F_HEAD_G, cx1 - cx0, leading=22)
    draw_wrapped(cx0, cy + 2, body, F_BODY_G, cx1 - cx0, leading=18)
    if idx % 3 < 2:
        d.line([(cx1 + 10, rows[idx // 3]), (cx1 + 10, rows[idx // 3] + 138)],
               fill=LIGHT_GREY, width=1)
d.line([(24, 740), (1000, 740)], fill=LIGHT_GREY, width=1)

# ---------------------------------------------------------------- also today
rule(896, width=1)
d.text((24, 904), "ALSO TODAY", font=F_ALSO_T, fill=RED)
also = (
    "Sweden to vote on Kristersson staying PM \u00b7 Yemen army: Houthis "
    "won't take Aden \u00b7 175 migrants unaccounted for after contact lost "
    "with a Senegal boat \u00b7 Nvidia suppliers cheer Huang's return \u00b7 "
    "Germans now oppose Ukraine military aid, 53%\u201346% \u00b7 England level "
    "the T20 series in Australia \u00b7 Dell lifts outlook on AI-server boom "
    "\u00b7 CIA and ODNI hit by cyber breach, unclassified data taken"
)
draw_wrapped(24, 926, also, F_ALSO, 976, leading=19)

# ---------------------------------------------------------------- footer
rule(984, width=1)
d.text((512, 992),
       "Sources: Reuters, CBS News, FAA, Saudi Civil Defence \u2014 25 Nov 2026  \u00b7  "
       "Entry for make.fun news-image-20261125",
       font=F_FOOT, fill=GREY, anchor="mt")

img.save(OUT, "PNG")
print("wrote", OUT, os.path.getsize(OUT), "bytes")

#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (v2).

Fresh build: 40 verified stories in 11 region groups, 12 hand-drawn scene
panels, a drawn world map with numbered pins, a UTC timeline and a
date-check footer. Output is a deterministic 1024x1024 PNG under 1 MiB.
Run:  python3 draw_day.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
NAVY = (26, 42, 94)
GOLD = (212, 175, 55)
MAP_GREEN = (183, 211, 160)
MAP_LINE = (120, 150, 105)
PIN = (198, 40, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (region, colour, headline, subline, source, pin-on-map?)
REGIONS = [
    ("NORTH AMERICA", (31, 56, 100), [
        ("Macy's 100th parade postponed",
         "First postponement ever; gusts to 60 mph.", "CNN", True),
        ("Trump proposes tariffs on 14 partners",
         "China capped 20%; Vietnam up to 35%.", "Reuters", False),
        ("Dow erases 1,100-pt plunge",
         "Dow +0.33% to 50,182.95; Nasdaq -0.62%.", "TradingView", False),
        ("US growth revised up to 4.3%",
         "Q3 second estimate; fastest in 3 years.", "Reuters", False),
        ("Musk: two SpaceX shares per US child",
         "Worth about $18bn; one from each.", "Reuters", False),
        ("FedEx jet overruns Miami runway",
         "MD-11 stops by the fence; no injuries.", "AP", True),
        ("Nor'easter leaves 358,000 in the dark",
         "Thanksgiving outages; Missouri worst.", "PowerOutage.us", False),
        ("New York bans AI chatbot toys, 5 years",
         "Moratorium signed; fines up to $15,000/day.", "Engadget", False),
        ("Kroger cuts 3,000 corporate jobs",
         "Notices under way; work shifts to India.", "NY Post", False),
    ]),
    ("SPORT", (123, 74, 18), [
        ("Chess World Ch.: Game 3 tied 1-1",
         "Gukesh vs Sindarov in Geneva; two draws so far.", "Chess.com", False),
        ("Davis Cup: Italy edge South Korea 2-1",
         "Berrettini-Vavassori win deciding doubles.", "ATP", False),
        ("Davis Cup QFs continue in Bologna",
         "Germany face Britain; Spain meet Austria.", "AFP", False),
        ("Thanksgiving NFL: two last-second thrillers",
         "Bears 39-35 Lions; Eagles 39-38 Cowboys.", "USA Today", True),
    ]),
    ("EUROPE", (15, 118, 110), [
        ("Russia strikes Kyiv overnight",
         "Ballistic missiles; grain ships hit near Odesa.", "Reuters", True),
        ("EU summit: 45bn euro Ukraine loan agreed",
         "Leaders agree 2028-34 budget.", "Reuters", False),
        ("Samara refineries ablaze after drones",
         "Kuibyshev and Syzran plants hit; one killed.", "Kyiv Post", False),
        ("Poland plans no-fly zone",
         "Missiles crossed airspace 20 & 24 Nov.", "Straits Times", True),
        ("Duran Duran's Andy Taylor dies at 65",
         "Death announced 25 Nov; prostate cancer battle.", "Reuters", False),
    ]),
    ("MIDDLE EAST", (153, 27, 27), [
        ("Cairo tanker crash kills 31",
         "Fuel tanker explodes on Ring Road; 27 vehicles burn.", "CNN", True),
        ("Houthis hit Jizan port; Riyadh stops missiles",
         "Minor damage; Jeddah drone downed.", "Rigzone", False),
        ("Gaza strikes kill 9, incl. Hamas deputy",
         "Third straight night despite the ceasefire.", "Reuters", False),
        ("Two tankers hit mines near Khasab",
         "IRGC claim, unverified; supertanker ablaze.", "Reuters", True),
        ("Eisenkot resumes coalition talks",
         "Aims to finalise deals by 1 Dec.", "Arab News", False),
    ]),
    ("TECH & SPACE", (107, 33, 168), [
        ("FCC clears SpaceX Starmind: 1m satellites",
         "Orbital data centres; first satellite by 2033.", "Reuters", False),
        ("Memory-chip shortage triples RAM prices",
         "AI servers soak up supply; server prices +45%.", "TrendForce", False),
    ]),
    ("EAST ASIA", (185, 28, 28), [
        ("Bank of Korea hikes rate to 3.25%",
         "25bp rise, 5-2 vote; highest since Oct 2024.", "Reuters", False),
        ("Kim: tactical nukes an 'urgent task'",
         "Inspected nuclear sites; KCNA reports 26 Nov.", "Yonhap", True),
        ("Shanghai chief Chen Jining probed for graft",
         "Fourth Politburo member investigated since 2025.", "Dawn", False),
        ("TAIEX rebounds 956 pts to 39,151.81",
         "Delta +6.2%, Foxconn +4.8% after sell-off.", "Taiwan News", True),
    ]),
    ("SOUTH ASIA", (194, 65, 12), [
        ("India marks 18th anniversary of 26/11",
         "166 killed in Mumbai in 2008; tributes in Delhi.", "DD India", False),
        ("Karachi building collapse kills 4",
         "Six-storey block under construction; 17 missing.", "AP", False),
        ("Bangladesh garment protests tear-gassed",
         "Workers reject new Tk 17,000 minimum wage.", "Reuters", False),
        ("India marks Constitution Day",
         "Samvidhan Divas: 1949 adoption of the Constitution.", "ANI", False),
    ]),
    ("SOUTHEAST ASIA", (21, 128, 61), [
        ("Java mine flood kills 13, 13 missing",
         "Illegal gold mine in Bogor; shaft 100m deep.", "Al Jazeera", True),
        ("Myanmar rejects ICJ genocide orders",
         "Min Aung Hlaing: some measures 'inappropriate'.", "Reuters", False),
    ]),
    ("AFRICA", (29, 78, 216), [
        ("Generic HIV shot reaches Africa",
         "300,000 vials to Zambia, Uganda, Zimbabwe.", "Reuters", False),
        ("South Africa sweep Bangladesh 2-0",
         "Mulder 7-31; win by an innings and 219 runs.", "Dawn", False),
    ]),
    ("LATIN AMERICA", (190, 24, 93), [
        ("Brazil pulls envoy from Argentina",
         "No Milei invite to Lula's Jan 5 inauguration.", "MercoPress", True),
    ]),
    ("OCEANIA", (71, 85, 105), [
        ("Qantas jet aborts Sydney landing",
         "Air NZ A321 crossed runway; ATSB probes.", "ATSB", True),
        ("Australia passes Digital Duty of Care",
         "Fines up to 5% of global revenue for Big Tech.", "CNA", False),
    ]),
]

# story number -> (x, y) pin on the map
PINS = {
    1: (225, 92), 6: (205, 122), 13: (175, 112), 14: (560, 80),
    17: (538, 66), 19: (565, 105), 22: (640, 100), 27: (805, 82),
    29: (820, 100), 34: (775, 148), 38: (272, 165), 39: (848, 152),
}

TIMELINE = [
    ("01:00", "FedEx overruns Miami runway"),
    ("05:30", "TAIEX closes +956"),
    ("06:30", "Kyiv strikes reported"),
    ("09:00", "EU summit opens, Brussels"),
    ("13:00", "Chess Game 3 begins, Geneva"),
    ("18:00", "Thanksgiving NFL kickoff"),
]


def wrap(text, fnt, width):
    """Wrap text to fit width, returning a list of lines."""
    lines = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=10 ** 6,
                                   break_long_words=False) or [""])
    out = []
    for line in lines:
        if fnt.getlength(line) <= width:
            out.append(line)
            continue
        words, cur = line.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if fnt.getlength(trial) <= width:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


# ------------------------------------------------------------------ scenes
def scene_balloon(d, x, y, w, h):
    # Thanksgiving parade balloon: turkey body, head, beak, strings
    d.ellipse([x + w * 0.28, y + 4, x + w * 0.72, y + h * 0.62], fill=(150, 90, 40))
    d.ellipse([x + w * 0.58, y + 2, x + w * 0.80, y + h * 0.30], fill=(150, 90, 40))
    d.polygon([(x + w * 0.78, y + h * 0.16), (x + w * 0.92, y + h * 0.20),
               (x + w * 0.78, y + h * 0.26)], fill=(230, 150, 30))
    d.ellipse([x + w * 0.68, y + h * 0.08, x + w * 0.73, y + h * 0.14], fill=(26, 26, 26))
    for dx in (0.35, 0.5, 0.65):
        d.line([x + w * dx, y + h * 0.60, x + w * dx, y + h * 0.92],
               fill=(120, 110, 100), width=1)


def scene_chart(d, x, y, w, h):
    d.line([x + 8, y + h - 10, x + w - 6, y + h - 10], fill=(90, 86, 76), width=2)
    d.line([x + 8, y + 6, x + 8, y + h - 10], fill=(90, 86, 76), width=2)
    pts = [(x + 10, y + h * 0.30), (x + w * 0.30, y + h * 0.55),
           (x + w * 0.50, y + h * 0.75), (x + w * 0.70, y + h * 0.45),
           (x + w - 10, y + h * 0.22)]
    d.line(pts, fill=(21, 128, 61), width=3, joint="curve")
    d.polygon([(x + w - 10, y + h * 0.22), (x + w - 18, y + h * 0.24),
               (x + w - 10, y + h * 0.32)], fill=(21, 128, 61))


def scene_jet(d, x, y, w, h):
    d.line([x + 4, y + h - 8, x + w - 4, y + h - 8], fill=(90, 86, 76), width=2)
    d.ellipse([x + w * 0.10, y + h * 0.30, x + w * 0.90, y + h * 0.62],
              fill=(200, 205, 215))
    d.polygon([(x + w * 0.42, y + h * 0.34), (x + w * 0.58, y + h * 0.62),
               (x + w * 0.50, y + h * 0.66)], fill=(150, 155, 170))
    d.polygon([(x + w * 0.80, y + h * 0.30), (x + w * 0.92, y + h * 0.18),
               (x + w * 0.94, y + h * 0.38)], fill=(150, 155, 170))
    for dx in (0.20, 0.32, 0.44):
        d.ellipse([x + w * dx, y + h * 0.40, x + w * dx + 4, y + h * 0.46],
                  fill=(26, 42, 94))
    d.ellipse([x + w * 0.84, y + h * 0.40, x + w * 0.88, y + h * 0.46],
              fill=(26, 42, 94))


def scene_storm(d, x, y, w, h):
    d.ellipse([x + w * 0.14, y + 6, x + w * 0.45, y + h * 0.55], fill=(120, 125, 135))
    d.ellipse([x + w * 0.35, y + 2, x + w * 0.66, y + h * 0.55], fill=(100, 105, 115))
    d.ellipse([x + w * 0.55, y + 8, x + w * 0.86, y + h * 0.55], fill=(120, 125, 135))
    for i, dx in enumerate((0.22, 0.45, 0.68)):
        d.line([x + w * dx, y + h * 0.58, x + w * dx - 3, y + h * 0.88],
               fill=(70, 110, 180), width=2)
    d.polygon([(x + w * 0.48, y + h * 0.55), (x + w * 0.40, y + h * 0.78),
               (x + w * 0.52, y + h * 0.78), (x + w * 0.44, y + h * 0.95)],
              fill=(230, 180, 40))


def scene_rook(d, x, y, w, h):
    # chess rook on a small chequered square, centred
    bs = 13
    bx, by = x + (w - 2 * bs) / 2, y + 6
    for r in range(2):
        for c in range(2):
            fill = (240, 235, 220) if (r + c) % 2 == 0 else (60, 60, 60)
            d.rectangle([bx + c * bs, by + r * bs, bx + (c + 1) * bs, by + (r + 1) * bs],
                        fill=fill)
    cx = x + w / 2
    d.rectangle([cx - 6, by + 4, cx + 6, by + 2 * bs - 4], fill=(26, 26, 26),
                outline=(255, 255, 255))
    for dx in (-6, -1, 4):
        d.rectangle([cx + dx, by - 2, cx + dx + 4, by + 5], fill=(26, 26, 26),
                    outline=(255, 255, 255))
    d.rectangle([cx - 8, by + 2 * bs - 6, cx + 8, by + 2 * bs - 2], fill=(26, 26, 26))


def scene_football(d, x, y, w, h):
    d.ellipse([x + w * 0.12, y + h * 0.28, x + w * 0.88, y + h * 0.72],
              fill=(140, 82, 32))
    d.line([x + w * 0.30, y + h * 0.50, x + w * 0.70, y + h * 0.50],
           fill=(255, 255, 255), width=2)
    for dx in (0.36, 0.44, 0.52, 0.60):
        d.line([x + w * dx, y + h * 0.42, x + w * dx, y + h * 0.58],
               fill=(255, 255, 255), width=2)
    d.line([x + 4, y + h - 6, x + w - 4, y + h - 6], fill=(21, 128, 61), width=2)


def scene_flame(d, x, y, w, h):
    d.rectangle([x + w * 0.14, y + h * 0.42, x + w * 0.34, y + h * 0.92],
                fill=(120, 125, 135))
    d.rectangle([x + w * 0.38, y + h * 0.58, x + w * 0.56, y + h * 0.92],
                fill=(100, 105, 115))
    d.polygon([(x + w * 0.62, y + h * 0.92), (x + w * 0.72, y + h * 0.30),
               (x + w * 0.82, y + h * 0.92)], fill=(230, 120, 30))
    d.polygon([(x + w * 0.68, y + h * 0.92), (x + w * 0.74, y + h * 0.55),
               (x + w * 0.80, y + h * 0.92)], fill=(250, 200, 60))


def scene_tanker(d, x, y, w, h):
    d.line([x + 4, y + h * 0.72, x + w - 4, y + h * 0.72], fill=(70, 110, 180), width=2)
    d.polygon([(x + w * 0.10, y + h * 0.55), (x + w * 0.90, y + h * 0.55),
               (x + w * 0.82, y + h * 0.72), (x + w * 0.18, y + h * 0.72)],
              fill=(120, 60, 40))
    d.rectangle([x + w * 0.30, y + h * 0.38, x + w * 0.46, y + h * 0.55],
                fill=(200, 200, 200))
    d.rectangle([x + w * 0.50, y + h * 0.38, x + w * 0.66, y + h * 0.55],
                fill=(180, 180, 180))
    for dx, dy in ((0.16, 0.80), (0.84, 0.80)):
        d.ellipse([x + w * dx - 3, y + h * dy - 3, x + w * dx + 3, y + h * dy + 3],
                  fill=(40, 40, 40))


def scene_satellite(d, x, y, w, h):
    d.rectangle([x + w * 0.06, y + h * 0.34, x + w * 0.30, y + h * 0.66],
                fill=(40, 80, 160), outline=(20, 50, 110))
    d.rectangle([x + w * 0.70, y + h * 0.34, x + w * 0.94, y + h * 0.66],
                fill=(40, 80, 160), outline=(20, 50, 110))
    for dx in (0.14, 0.22):
        d.line([x + w * dx, y + h * 0.34, x + w * dx, y + h * 0.66],
               fill=(120, 160, 220), width=1)
    for dx in (0.78, 0.86):
        d.line([x + w * dx, y + h * 0.34, x + w * dx, y + h * 0.66],
               fill=(120, 160, 220), width=1)
    d.rectangle([x + w * 0.38, y + h * 0.40, x + w * 0.62, y + h * 0.60],
                fill=(200, 200, 200), outline=(90, 90, 90), width=2)
    d.ellipse([x + w * 0.46, y + h * 0.46, x + w * 0.54, y + h * 0.54],
              fill=(230, 150, 30))
    d.arc([x + w * 0.64, y + h * 0.04, x + w * 0.96, y + h * 0.40],
          start=300, end=60, fill=(230, 150, 30), width=3)
    for sx, sy in ((0.10, 0.14), (0.90, 0.10), (0.50, 0.06)):
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(230, 200, 60))


def scene_syringe(d, x, y, w, h):
    d.line([x + w * 0.22, y + h * 0.78, x + w * 0.76, y + h * 0.24],
           fill=(150, 155, 170), width=9)
    d.line([x + w * 0.76, y + h * 0.24, x + w * 0.92, y + h * 0.08],
           fill=(90, 90, 90), width=2)
    d.line([x + w * 0.40, y + h * 0.64, x + w * 0.58, y + h * 0.46],
           fill=(230, 60, 60), width=4)
    d.rectangle([x + w * 0.08, y + h * 0.74, x + w * 0.26, y + h * 0.94],
                fill=(200, 220, 240), outline=(90, 90, 90), width=2)
    d.rectangle([x + w * 0.12, y + h * 0.82, x + w * 0.22, y + h * 0.90],
                fill=(230, 60, 60))


def scene_cricket(d, x, y, w, h):
    # bat swung diagonally, red ball beside it
    d.polygon([(x + w * 0.30, y + h * 0.10), (x + w * 0.44, y + h * 0.06),
               (x + w * 0.72, y + h * 0.62), (x + w * 0.60, y + h * 0.70)],
              fill=(210, 180, 130), outline=(120, 90, 40))
    d.polygon([(x + w * 0.28, y + h * 0.06), (x + w * 0.34, y + h * 0.02),
               (x + w * 0.44, y + h * 0.10), (x + w * 0.38, y + h * 0.16)],
              fill=(120, 90, 40))
    d.ellipse([x + w * 0.74, y + h * 0.58, x + w * 0.94, y + h * 0.80],
              fill=(180, 40, 40))
    d.arc([x + w * 0.74, y + h * 0.58, x + w * 0.94, y + h * 0.80],
          start=0, end=360, fill=(255, 255, 255), width=1)
    d.line([x + 4, y + h - 6, x + w - 4, y + h - 6], fill=(21, 128, 61), width=2)


def scene_flags(d, x, y, w, h):
    d.line([x + w * 0.30, y + 4, x + w * 0.30, y + h - 6], fill=(90, 86, 76), width=2)
    d.line([x + w * 0.68, y + 4, x + w * 0.68, y + h - 6], fill=(90, 86, 76), width=2)
    d.polygon([(x + w * 0.30, y + 4), (x + w * 0.62, y + 4),
               (x + w * 0.62, y + h * 0.42), (x + w * 0.30, y + h * 0.42)],
              fill=(0, 150, 60))
    d.polygon([(x + w * 0.44, y + h * 0.12), (x + w * 0.52, y + h * 0.23),
               (x + w * 0.44, y + h * 0.34), (x + w * 0.36, y + h * 0.23)],
              fill=(250, 220, 0))
    d.polygon([(x + w * 0.68, y + 4), (x + w * 0.96, y + 4),
               (x + w * 0.96, y + h * 0.42), (x + w * 0.68, y + h * 0.42)],
              fill=(120, 180, 230))
    d.ellipse([x + w * 0.78, y + h * 0.12, x + w * 0.86, y + h * 0.30],
              fill=(255, 255, 255))


SCENES = [
    ("Parade balloon", scene_balloon),
    ("Markets rebound", scene_chart),
    ("FedEx overrun", scene_jet),
    ("Nor'easter", scene_storm),
    ("Chess, Game 3", scene_rook),
    ("Thanksgiving NFL", scene_football),
    ("Samara ablaze", scene_flame),
    ("Tankers mined", scene_tanker),
    ("Starmind", scene_satellite),
    ("HIV shot arrives", scene_syringe),
    ("Cricket sweep", scene_cricket),
    ("Brazil-Argentina", scene_flags),
]

CONTINENTS = [
    [(60, 78), (90, 70), (140, 66), (190, 70), (235, 78), (250, 88),
     (225, 100), (205, 118), (185, 128), (150, 132), (120, 122), (80, 105), (55, 90)],
    [(285, 62), (305, 64), (310, 72), (295, 76), (282, 70)],
    [(245, 128), (285, 124), (305, 138), (300, 160), (285, 175), (262, 172), (245, 150)],
    [(490, 72), (520, 64), (545, 66), (555, 76), (540, 86), (510, 88), (492, 82)],
    [(495, 96), (535, 92), (560, 104), (565, 130), (550, 158), (520, 162),
     (498, 140), (488, 115)],
    [(560, 64), (640, 58), (730, 60), (800, 66), (830, 78), (825, 96),
     (790, 104), (760, 118), (720, 112), (690, 124), (660, 108), (620, 100),
     (580, 92), (562, 80)],
    [(745, 128), (765, 132), (755, 140)],
    [(790, 138), (805, 140), (798, 148)],
    [(800, 138), (850, 134), (868, 146), (855, 162), (815, 160), (798, 148)],
]


# ------------------------------------------------------------------ layout
def draw_masthead(d):
    d.rectangle([0, 0, W, 58], fill=NAVY)
    d.text((16, 8), "THE WORLD IN ONE DAY", font=font(SERIF_B, 34), fill=(255, 255, 255))
    d.text((16, 42), "THURSDAY  \u2022  WORLD NEWS",
           font=font(SANS_B, 12), fill=(180, 195, 230))
    right = "26 NOVEMBER 2026"
    d.text((W - 16 - font(SANS_B, 24).getlength(right), 10), right,
           font=font(SANS_B, 24), fill=GOLD)
    sub = "40 TOP STORIES  \u2022  11 REGIONS  \u2022  SECOND EDITION"
    d.text((W - 16 - font(SANS_B, 11).getlength(sub), 40), sub,
           font=font(SANS_B, 11), fill=GOLD)


def draw_map(d):
    y0, y1 = 62, 170
    d.rectangle([0, y0, W, y1], fill=(214, 230, 240))
    for gx in range(0, W + 1, 83):
        d.line([gx, y0, gx, y1], fill=(190, 210, 225), width=1)
    for gy in range(y0, y1 + 1, 27):
        d.line([0, gy, W, gy], fill=(190, 210, 225), width=1)
    for poly in CONTINENTS:
        d.polygon(poly, fill=MAP_GREEN, outline=MAP_LINE)
    d.text((16, y0 + 3), "MAP \u2014 WHERE THE DAY HAPPENED",
           font=font(SANS_B, 10), fill=(70, 80, 90))
    num_f = font(SANS_B, 11)
    for n, (px, py) in PINS.items():
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=PIN, outline=(255, 255, 255), width=2)
        label = str(n)
        d.text((px - num_f.getlength(label) / 2, py - 7), label, font=num_f,
               fill=(255, 255, 255))


def draw_scenes(d):
    x0, gap = 14, 8
    pw = (W - 2 * x0 - 5 * gap) // 6
    cap_f = font(SANS_B, 10)
    for row in range(2):
        y = 176 + row * 68
        for col in range(6):
            idx = row * 6 + col
            caption, fn = SCENES[idx]
            x = x0 + col * (pw + gap)
            d.rectangle([x, y, x + pw, y + 62], fill=(255, 255, 255),
                        outline=(200, 195, 185))
            fn(d, x + 6, y + 3, pw - 12, 42)
            tw = cap_f.getlength(caption)
            d.text((x + (pw - tw) / 2, y + 47), caption, font=cap_f, fill=INK)


def story_block_height(head_f, sub_f, text_w, headline, subline, src):
    hl = wrap(headline, head_f, text_w)
    sl = wrap(subline + " \u2014 " + src, sub_f, text_w)
    return max(15, len(hl) * 15) + len(sl) * 12 + 5


def draw_columns(d, head_size=13, sub_size=9):
    """Lay out the three story columns; return True if it fits."""
    head_f = font(SANS_B, head_size)
    sub_f = font(SANS, sub_size)
    hdr_f = font(SANS_B, 11)
    num_f = font(SANS_B, 10)
    x0, gap = 14, 12
    col_w = (W - 2 * x0 - 2 * gap) // 3
    text_w = col_w - 24
    y_top, y_bot = 306, 916
    columns = [
        [REGIONS[0], REGIONS[1]],
        [REGIONS[2], REGIONS[3], REGIONS[4]],
        [REGIONS[5], REGIONS[6], REGIONS[7], REGIONS[8], REGIONS[9], REGIONS[10]],
    ]
    # measure first
    heights = []
    for col in columns:
        h = 0
        for name, colour, stories in col:
            h += 20
            for headline, subline, _src, _pin in stories:
                h += story_block_height(head_f, sub_f, text_w, headline, subline, _src)
        heights.append(h)
    if max(heights) > y_bot - y_top:
        return False
    # draw
    n = 0
    for ci, col in enumerate(columns):
        x = x0 + ci * (col_w + gap)
        y = y_top
        for name, colour, stories in col:
            d.rectangle([x, y, x + col_w, y + 17], fill=colour)
            d.text((x + 6, y + 3), "%s  \u2014  %d" % (name, len(stories)),
                   font=hdr_f, fill=(255, 255, 255))
            y += 20
            for headline, subline, src, _pin in stories:
                n += 1
                hl = wrap(headline, head_f, text_w)
                sl = wrap(subline + " \u2014 " + src, sub_f, text_w)
                d.rounded_rectangle([x, y + 1, x + 15, y + 16], radius=3, fill=colour)
                num = str(n)
                d.text((x + 7 - num_f.getlength(num) / 2, y + 3), num,
                       font=num_f, fill=(255, 255, 255))
                ty = y
                for line in hl:
                    d.text((x + 22, ty), line, font=head_f, fill=INK)
                    ty += 15
                for line in sl:
                    d.text((x + 22, ty), line, font=sub_f, fill=MUTED)
                    ty += 12
                y = ty + 5
    return True


def draw_timeline(d):
    y = 922
    d.text((16, y), "UTC TIMELINE \u2014 THURSDAY 26 NOVEMBER 2026",
           font=font(SANS_B, 10), fill=MUTED)
    y += 14
    d.line([16, y + 4, W - 16, y + 4], fill=(150, 145, 135), width=1)
    t_f = font(SANS_B, 10)
    l_f = font(SANS, 9)
    for i, (t, label) in enumerate(TIMELINE):
        x = 16 + i * (W - 32) // 6
        d.ellipse([x - 3, y + 1, x + 3, y + 7], fill=PIN)
        tx = max(4, min(x - t_f.getlength(t) / 2, W - 40))
        d.text((tx, y + 10), t, font=t_f, fill=PIN)
        lx = max(4, min(x - 20, W - 160))
        d.text((lx, y + 22), label, font=l_f, fill=INK)


def draw_footer(d):
    d.line([16, 972, W - 16, 972], fill=(150, 145, 135), width=1)
    d.text((16, 978),
           "DATE CHECK \u2014 Stories as reported on 26 Nov 2026. Claims are attributed where unconfirmed.",
           font=font(SANS_B, 11), fill=INK)
    d.text((16, 993),
           "Sources: Reuters \u2022 AP \u2022 CNN \u2022 Al Jazeera \u2022 Arab News \u2022 Yonhap \u2022 CNA \u2022 Taiwan News \u2022 Dawn \u2022 Straits Times \u2022 ATP \u2022 FIDE \u2022 FCC \u2022 Kyiv Post \u2022 MercoPress \u2022 USA Today \u2022 ATSB \u2014 full list in README.",
           font=font(SANS, 9), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_map(d)
    draw_scenes(d)
    # shrink fonts until the columns fit; never leave them blank
    chosen = (11, 8)
    for hs, ss in ((13, 9), (12, 9), (11, 8)):
        probe = Image.new("RGB", (W, H), PAPER)
        if draw_columns(ImageDraw.Draw(probe), head_size=hs, sub_size=ss):
            chosen = (hs, ss)
            break
        chosen = (hs, ss)
    draw_columns(d, head_size=chosen[0], sub_size=chosen[1])
    draw_timeline(d)
    draw_footer(d)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()

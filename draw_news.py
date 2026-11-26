#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Build-time only: the submitted program (main.ts) just copies entry.png.
36 stories in 9 region groups, plus a drawn world map with pinned
story locations, a UTC timeline, and small drawn scene illustrations.
Every headline was verified against reputable reporting on
26 November 2026; see README.md for the source list. Claims the
reporting itself calls unconfirmed are attributed as such.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (20, 24, 38)
NAVY = (16, 42, 90)
SLATE = (70, 78, 96)
CARD = (255, 255, 255)
LINE = (200, 192, 172)
GOLD = (255, 214, 90)
OCEAN = (213, 229, 240)
LAND = (198, 210, 186)
LAND_LINE = (150, 166, 140)
RED = (178, 34, 34)

F_BIG = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(F_BIG if bold else F_REG, size)


def wrap(draw, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def one_line(draw, text, f, width):
    """Shrink text to a single line, trimming words with an ellipsis."""
    if draw.textlength(text, font=f) <= width:
        return text
    words = text.split()
    while words and draw.textlength(" ".join(words) + " ...", font=f) > width:
        words.pop()
    return " ".join(words) + " ..."


# (region, color, [(headline, subline), ...])
REGIONS = [
    ("NORTH AMERICA", (16, 42, 90), [
        ("Macy's 100th parade postponed to Saturday",
         "First postponement ever; gusts to 60 mph."),
        ("Trump proposes tariffs on 14 trading partners",
         "China 20% cap; Vietnam up to 35%; Taiwan 15%."),
        ("Dow erases 1,100-pt plunge; Nasdaq dives 4%",
         "Dow +0.33% to 50,182.95; Nasdaq -0.62%."),
        ("US growth revised up to 4.3%, fastest in 3 years",
         "Q3 second estimate, up from 3.4%."),
        ("Musk: two SpaceX shares for every US child",
         "Worth about $18bn; one each from SpaceX, Musk."),
        ("FedEx jet overruns Miami runway, no injuries",
         "MD-11 from Memphis stops by fence; FAA probes."),
        ("Nor'easter leaves 358,000 without power",
         "Thanksgiving outages; Missouri, Virginia worst."),
        ("New York bans AI chatbot toys for five years",
         "Hochul signs ban; fines up to $15,000 a day."),
        ("Kroger begins cutting 3,000 corporate jobs",
         "Notices under way; work shifts to Bangalore hub."),
    ]),
    ("SPORT", (120, 70, 20), [
        ("Chess World Ch.: Game 3 under way, tied 1-1",
         "Gukesh vs Sindarov in Geneva; two draws so far."),
        ("Davis Cup: Italy edge South Korea 2-1",
         "Berrettini-Vavassori win deciding doubles."),
        ("Davis Cup: Germany face Britain; Spain-Austria",
         "Quarter-finals continue on Thursday in Bologna."),
    ]),
    ("EUROPE", (0, 105, 105), [
        ("Russia strikes Kyiv overnight; grain ships hit",
         "Ballistic missiles; 2 ships attacked near Odesa."),
        ("EU summit: 45bn euro Ukraine loan; 1.6tn budget",
         "Leaders agree 2028-34 budget; 70bn gap for 2027."),
        ("Samara refineries ablaze after drone strikes",
         "Kuibyshev and Syzran plants hit; one killed."),
        ("Poland plans no-fly zone after incursions",
         "Missiles crossed airspace on 20 and 24 Nov."),
        ("Duran Duran's Andy Taylor dies at 65",
         "Death announced 25 Nov; prostate cancer battle."),
    ]),
    ("MIDDLE EAST", (140, 40, 40), [
        ("Cairo tanker crash kills 31, burns 27 vehicles",
         "Fuel tanker explodes on Ring Road; driver arrested."),
        ("Houthis hit Jizan port; Riyadh missiles stopped",
         "Minor damage, no casualties; Jeddah drone down."),
        ("Gaza strikes kill 9, incl. Hamas education deputy",
         "Third straight night despite ceasefire."),
        ("Two tankers hit mines near Khasab - IRGC claim",
         "Supertanker ablaze; claim unverified."),
        ("Eisenkot resumes coalition talks in Israel",
         "Aims to finalise deals by 1 Dec; Netanyahu fears."),
    ]),
    ("TECH & SPACE", (90, 60, 140), [
        ("FCC clears SpaceX Starmind: 1m AI satellites",
         "Orbital data centres; first satellite by 2033."),
        ("Memory-chip shortage triples RAM prices",
         "AI servers soak up supply; server prices up 45%."),
    ]),
    ("EAST ASIA", (178, 34, 34), [
        ("Bank of Korea hikes rate to 3.25%",
         "25bp rise, 5-2 vote; highest since October 2024."),
        ("Kim: tactical nukes an 'urgent task'",
         "Inspected nuclear sites; KCNA reports 26 Nov."),
        ("Shanghai chief Chen Jining probed for graft",
         "Fourth Politburo member investigated since 2025."),
        ("TAIEX rebounds 956 pts to 39,151.81",
         "After sell-off; Delta +6.2%, Foxconn +4.8%."),
    ]),
    ("SOUTH ASIA", (176, 124, 0), [
        ("India marks 18th anniversary of 26/11 attacks",
         "166 killed in Mumbai in 2008; tributes in Delhi."),
        ("Karachi building collapse kills 4, 17 missing",
         "Six-storey block under construction; 14 injured."),
        ("Bangladesh garment protests met with tear gas",
         "Workers reject new Tk 17,000 minimum wage."),
        ("India marks Constitution Day",
         "Samvidhan Divas: 26 Nov, marking 1949 adoption."),
    ]),
    ("SOUTHEAST ASIA", (46, 125, 50), [
        ("Java mine flood kills 13, 13 still missing",
         "Illegal gold mine in Bogor; shaft 100m deep."),
        ("Myanmar rejects ICJ genocide orders",
         "Min Aung Hlaing: some measures 'inappropriate'."),
    ]),
    ("AFRICA", (60, 90, 160), [
        ("Generic HIV shot reaches Africa: 300,000 vials",
         "Lenacapavir to Zambia, Uganda, Zimbabwe."),
        ("South Africa sweep Bangladesh 2-0 in Tests",
         "Mulder 7-31; win by an innings and 219 runs."),
    ]),
]

# columns: region indices, balanced at 12 stories each
COLUMNS = [[0, 1], [2, 3, 4], [5, 6, 7, 8]]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 104], fill=NAVY)
d.text((28, 12), "THE WORLD IN ONE DAY", font=font(20, True), fill=GOLD)
d.text((28, 34), "26 NOVEMBER 2026", font=font(48, True), fill=(255, 255, 255))
d.text((28, 84), "THURSDAY  \u2022  WORLD NEWS", font=font(16, True), fill=(180, 200, 235))
d.text((660, 84), "36 TOP STORIES  \u2022  9 REGIONS", font=font(16, True), fill=GOLD)

# ---------------- drawn world map ----------------
d.rectangle([0, 104, W, 192], fill=OCEAN)
LAND_POLYS = [
    # North America
    [(70, 124), (150, 116), (210, 120), (225, 134), (205, 148),
     (170, 164), (120, 162), (75, 146)],
    # Greenland
    [(228, 108), (252, 106), (256, 118), (236, 122)],
    # South America
    [(215, 156), (245, 154), (262, 168), (250, 188), (225, 184), (212, 168)],
    # Europe
    [(468, 120), (510, 112), (540, 118), (545, 132), (520, 138),
     (490, 136), (470, 128)],
    # Africa
    [(470, 144), (515, 142), (545, 152), (540, 172), (515, 188),
     (485, 184), (468, 164)],
    # Asia
    [(550, 114), (640, 106), (730, 108), (800, 118), (830, 136),
     (800, 156), (740, 164), (660, 160), (580, 148), (552, 132)],
    # SE Asia islands
    [(740, 168), (780, 166), (800, 174), (760, 180)],
    # Australia
    [(770, 178), (815, 176), (825, 188), (785, 190)],
]
for poly in LAND_POLYS:
    d.polygon(poly, fill=LAND, outline=LAND_LINE)

# small drawn scenes on the map
# parade balloon over New York
d.ellipse([150, 116, 168, 128], fill=(255, 90, 90), outline=(150, 40, 40))
d.line([(159, 128), (159, 134)], fill=(120, 60, 20), width=1)
d.rectangle([155, 134, 163, 138], fill=(180, 120, 40))
# flame over Cairo
d.polygon([(528, 134), (534, 142), (538, 136), (540, 144), (532, 148),
           (524, 144), (526, 137)], fill=(255, 140, 0), outline=(200, 60, 0))
# satellite, top right
d.rectangle([912, 118, 926, 126], fill=(90, 100, 120), outline=(40, 50, 70))
d.rectangle([898, 120, 912, 124], fill=(40, 90, 160))
d.rectangle([926, 120, 940, 124], fill=(40, 90, 160))
d.line([(919, 118), (926, 110)], fill=(40, 50, 70), width=2)
# tennis ball, Indian Ocean
d.ellipse([852, 164, 868, 180], fill=(190, 220, 60), outline=(120, 150, 20))
d.arc([852, 164, 868, 180], start=300, end=60, fill=(255, 255, 255), width=2)
d.arc([852, 164, 868, 180], start=120, end=240, fill=(255, 255, 255), width=2)
# syringe, southern Africa
d.line([(478, 164), (492, 176)], fill=(60, 60, 60), width=3)
d.line([(492, 176), (496, 180)], fill=(60, 60, 60), width=1)
d.rectangle([474, 160, 480, 166], fill=(200, 60, 60))

# numbered pins: (story number, x, y)
PINS = [(1, 172, 142), (6, 182, 158), (13, 536, 126), (15, 604, 118),
        (18, 528, 152), (19, 570, 156), (21, 600, 150), (25, 748, 130),
        (33, 764, 170), (35, 508, 176)]
for num, px, py in PINS:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255))
    t = str(num)
    tw = d.textlength(t, font=font(10, True))
    d.text((px - tw / 2, py - 7), t, font=font(10, True), fill=(255, 255, 255))

# caption drawn last so land never covers it
d.text((28, 106), "MAP \u2014 WHERE THE DAY HAPPENED  (numbered pins = story numbers)",
       font=font(11, True), fill=SLATE)

# ---------------- UTC timeline ----------------
d.rectangle([0, 192, W, 260], fill=(232, 228, 214))
d.text((28, 196), "UTC TIMELINE \u2014 THURSDAY 26 NOVEMBER 2026",
       font=font(11, True), fill=SLATE)
TL_Y = 240
d.line([(40, TL_Y), (984, TL_Y)], fill=SLATE, width=2)
for h in range(0, 25, 4):
    x = 40 + (h / 24.0) * 944
    d.line([(x, TL_Y - 4), (x, TL_Y + 4)], fill=SLATE, width=2)
    lab = f"{h:02d}:00"
    tw = d.textlength(lab, font=font(9))
    d.text((x - tw / 2, TL_Y + 7), lab, font=font(9), fill=SLATE)
# event labels in two rows above the line, placed to avoid collisions
# (utc hour, label, row, x-mode)  row 1 y=210, row 2 y=222
def tl_label(hour, label, y, mode="center"):
    x = 40 + (hour / 24.0) * 944
    tw = d.textlength(label, font=font(10, True))
    if mode == "left":
        lx = 28
    else:
        lx = min(max(x - tw / 2, 28), 996 - tw)
    d.text((lx, y), label, font=font(10, True), fill=INK)
    d.ellipse([x - 5, TL_Y - 5, x + 5, TL_Y + 5], fill=RED,
              outline=(255, 255, 255))

tl_label(1.67, "FedEx overruns runway", 210, "left")
tl_label(5.5, "Bangladesh protests", 210)
tl_label(9.48, "TAIEX closes +956", 210)
tl_label(14.0, "Chess Game 3 begins", 210)
tl_label(5.5, "Missile crashes in Poland", 222)
tl_label(12.0, "358,000 without power", 222)

# ---------------- body: 3 columns ----------------
margin, gap, col_w = 24, 14, 316
slot_h, sec_h = 47, 22
y0 = 268
n = 0
for ci, col in enumerate(COLUMNS):
    x = margin + ci * (col_w + gap)
    y = y0
    for ri in col:
        name, color, stories = REGIONS[ri]
        d.rectangle([x, y, x + col_w, y + sec_h], fill=color)
        d.text((x + 8, y + 4), f"{name}  \u2014  {len(stories)}",
               font=font(12, True), fill=(255, 255, 255))
        y += sec_h + 4
        for head, sub in stories:
            n += 1
            d.rounded_rectangle([x, y + 2, x + 22, y + 24], radius=5, fill=color)
            num = str(n)
            tw = d.textlength(num, font=font(11, True))
            d.text((x + 11 - tw / 2, y + 5), num, font=font(11, True),
                   fill=(255, 255, 255))
            tx = x + 30
            twd = col_w - 30
            hl = wrap(d, head, font(14, True), twd)[:2]
            yy = y
            for line in hl:
                d.text((tx, yy), line, font=font(14, True), fill=INK)
                yy += 17
            sl = one_line(d, sub, font(11), twd)
            d.text((tx, yy), sl, font=font(11), fill=SLATE)
            y += slot_h
        y += 6

# ---------------- footer ----------------
fy = 972
d.line([(24, fy), (1000, fy)], fill=LINE, width=2)
d.text((24, fy + 8),
       "DATE CHECK \u2014 Stories as reported on 26 Nov 2026. Claims are attributed where unconfirmed.",
       font=font(12, True), fill=INK)
d.text((24, fy + 30),
       "Sources: Reuters \u2022 AP \u2022 CNN \u2022 Al Jazeera \u2022 Arab News \u2022 Yonhap \u2022 CNA \u2022 Taiwan News \u2022 Dawn \u2022 Straits Times \u2022 ATP \u2022 FIDE \u2022 FCC \u2022 Kyiv Post \u2022 Prothom Alo \u2022 JPost \u2022 Haaretz",
       font=font(11), fill=SLATE)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, "stories:", n)

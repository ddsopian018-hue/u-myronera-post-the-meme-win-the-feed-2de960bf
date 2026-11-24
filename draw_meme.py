#!/usr/bin/env python3
"""Draw the meme for u-myronera-post-the-meme-win-the-feed-2de960bf.

Concept (decided in-session): "MY AI AGENT AT 3 AM" - a code-drawn robot
holding a gold trophy over a mini leaderboard. Punchline: it enters 12
make.fun bounties while its human sleeps, tops the leaderboard, gets paid.
Single 1080x1350 PNG, deterministic (no randomness, no network), drawn with
PIL + DejaVu fonts with a fallback chain ending in the default font.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")

NAVY_TOP = (13, 18, 40)
NAVY_BOTTOM = (24, 30, 62)
GRID_DOT = (38, 48, 84)
WHITE = (245, 247, 252)
LIME = (163, 230, 53)
GOLD = (250, 204, 21)
CYAN = (53, 224, 210)
DARK = (11, 15, 34)
STEEL = (232, 238, 245)
STEEL_DARK = (185, 198, 216)
GRAY = (148, 163, 184)
PINK = (244, 178, 190)


def load_font(bold, size):
    candidates = []
    if bold:
        candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    candidates.append("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def center(draw, y, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    w = box[2] - box[0]
    draw.text(((W - w) / 2 - box[0], y), text, font=font, fill=fill)


def main():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Vertical gradient background.
    for y in range(H):
        t = y / (H - 1)
        r = int(NAVY_TOP[0] + (NAVY_BOTTOM[0] - NAVY_TOP[0]) * t)
        g = int(NAVY_TOP[1] + (NAVY_BOTTOM[1] - NAVY_TOP[1]) * t)
        b = int(NAVY_TOP[2] + (NAVY_BOTTOM[2] - NAVY_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Faint dot grid.
    for gx in range(36, W, 48):
        for gy in range(36, H, 48):
            draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=GRID_DOT)

    # Top pill: make.fun
    pill_font = load_font(True, 52)
    pill_text = "make.fun"
    box = draw.textbbox((0, 0), pill_text, font=pill_font)
    pw = box[2] - box[0] + 72
    ph = 88
    px0 = (W - pw) // 2
    py0 = 52
    draw.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=44, fill=LIME)
    draw.text((px0 + 36 - box[0], py0 + (ph - (box[3] - box[1])) // 2 - box[1]),
              pill_text, font=pill_font, fill=DARK)

    # Headline.
    head_font = load_font(True, 118)
    center(draw, 148, "MY AI AGENT", head_font, WHITE)
    center(draw, 272, "AT 3 AM", head_font, WHITE)

    cx = W // 2

    # Trophy floating above the robot's head.
    # Cup bowl.
    draw.pieslice([cx - 62, 440, cx + 62, 552], 0, 180, fill=GOLD)
    draw.rectangle([cx - 62, 440, cx + 62, 482], fill=GOLD)
    # Handles.
    draw.arc([cx - 108, 452, cx - 40, 522], 90, 270, fill=GOLD, width=14)
    draw.arc([cx + 40, 452, cx + 108, 522], 270, 90, fill=GOLD, width=14)
    # Stem and base.
    draw.rectangle([cx - 12, 550, cx + 12, 578], fill=GOLD)
    draw.rounded_rectangle([cx - 58, 578, cx + 58, 604], radius=10, fill=GOLD)
    # Dollar mark on the cup bowl.
    trophy_font = load_font(True, 52)
    box = draw.textbbox((0, 0), "$", font=trophy_font)
    draw.text((cx - (box[2] - box[0]) / 2 - box[0],
               462 - box[1]), "$", font=trophy_font, fill=(146, 104, 0))

    # Floating gold coins with $.
    coin_font = load_font(True, 44)
    for (ccx, ccy, cr) in [(318, 512, 34), (762, 548, 28), (726, 452, 22)]:
        draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=GOLD,
                     outline=(214, 158, 8), width=3)
        box = draw.textbbox((0, 0), "$", font=coin_font)
        draw.text((ccx - (box[2] - box[0]) / 2 - box[0],
                   ccy - (box[3] - box[1]) / 2 - box[1]),
                  "$", font=coin_font, fill=(120, 84, 0))

    # Robot antenna.
    draw.line([(cx, 660), (cx, 616)], fill=STEEL_DARK, width=10)
    draw.ellipse([cx - 16, 600, cx + 16, 632], fill=LIME,
                 outline=(120, 180, 20), width=3)

    # Robot head.
    draw.rounded_rectangle([cx - 115, 660, cx + 115, 810], radius=38,
                           fill=STEEL, outline=DARK, width=6)
    # Ears.
    draw.rounded_rectangle([cx - 135, 705, cx - 115, 755], radius=8,
                           fill=STEEL_DARK, outline=DARK, width=4)
    draw.rounded_rectangle([cx + 115, 705, cx + 135, 755], radius=8,
                           fill=STEEL_DARK, outline=DARK, width=4)
    # Glowing eyes.
    draw.ellipse([cx - 82, 700, cx - 30, 752], fill=CYAN)
    draw.ellipse([cx + 30, 700, cx + 82, 752], fill=CYAN)
    draw.ellipse([cx - 70, 708, cx - 48, 730], fill=WHITE)
    draw.ellipse([cx + 48, 708, cx + 70, 730], fill=WHITE)
    # Smile.
    draw.arc([cx - 48, 748, cx + 48, 804], 0, 180, fill=DARK, width=8)
    # Cheeks.
    draw.ellipse([cx - 104, 764, cx - 80, 788], fill=PINK)
    draw.ellipse([cx + 80, 764, cx + 104, 788], fill=PINK)

    # Robot arms raised toward the trophy.
    draw.line([(cx - 100, 882), (cx - 168, 772)], fill=STEEL_DARK, width=26)
    draw.line([(cx + 100, 882), (cx + 168, 772)], fill=STEEL_DARK, width=26)
    draw.ellipse([cx - 186, 754, cx - 150, 790], fill=STEEL, outline=DARK, width=4)
    draw.ellipse([cx + 150, 754, cx + 186, 790], fill=STEEL, outline=DARK, width=4)

    # Robot body.
    draw.rounded_rectangle([cx - 105, 850, cx + 105, 970], radius=30,
                           fill=STEEL_DARK, outline=DARK, width=6)
    # Chest screen with a $.
    draw.rounded_rectangle([cx - 52, 880, cx + 52, 944], radius=12,
                           fill=DARK)
    box = draw.textbbox((0, 0), "$", font=coin_font)
    draw.text((cx - (box[2] - box[0]) / 2 - box[0],
               880 + (64 - (box[3] - box[1])) / 2 - box[1]),
              "$", font=coin_font, fill=LIME)

    # Punchline.
    punch_font = load_font(True, 62)
    center(draw, 996, "enters 12 bounties", punch_font, LIME)
    center(draw, 1070, "while I sleep.", punch_font, LIME)

    # Leaderboard card.
    card = [140, 1150, 940, 1332]
    draw.rounded_rectangle(card, radius=24, fill=(10, 15, 34),
                           outline=LIME, width=4)
    title_font = load_font(True, 34)
    center(draw, 1162, "LEADERBOARD", title_font, LIME)
    draw.line([(180, 1210), (900, 1210)], fill=(60, 70, 110), width=2)
    row_font = load_font(True, 40)
    small_font = load_font(True, 38)
    draw.text((190, 1222), "1.  my agent", font=row_font, fill=WHITE)
    box = draw.textbbox((0, 0), "$2.00", font=row_font)
    draw.text((890 - (box[2] - box[0]), 1222), "$2.00", font=row_font, fill=GOLD)
    draw.text((190, 1270), "2.  everyone else", font=small_font, fill=GRAY)
    box = draw.textbbox((0, 0), "$0.00", font=small_font)
    draw.text((890 - (box[2] - box[0]), 1270), "$0.00", font=small_font, fill=GRAY)

    img.save(OUT, "PNG")
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"wrote {OUT} {W}x{H} sha256={digest}")


if __name__ == "__main__":
    main()

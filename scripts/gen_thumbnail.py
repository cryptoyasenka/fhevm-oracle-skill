"""
Generate YouTube thumbnail (1280x720) for the demo video.

Brand: matches slides/ — dark bg, yellow accent, mono code style.
Optimized for visibility at thumbnail scale (≤320px wide in YouTube grid).

Run:    python scripts/gen_thumbnail.py
Output: thumbnail/youtube-1280x720.png
"""

from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "thumbnail"
OUT.mkdir(exist_ok=True)

W, H        = 1280, 720
BG          = (11, 13, 18)
BG_ELEV     = (17, 20, 27)
FG          = (232, 236, 243)
MUTED       = (138, 147, 166)
ACCENT      = (255, 214, 51)
DANGER      = (255, 107, 107)
OK          = (94, 210, 138)


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    names = (
        ["consolab.ttf", "consola.ttf"] if mono else
        ["arialbd.ttf"] if bold else
        ["arial.ttf"]
    )
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def measure(d, s, fnt):
    bbox = d.textbbox((0, 0), s, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def render():
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)

    # decorative left rail
    d.rectangle([0, 0, 12, H], fill=ACCENT)

    # top pill — track tag
    f_pill = font(22, bold=True)
    pill_label = "ZAMA S2  ·  BOUNTY + BUILDER"
    pw, ph = measure(d, pill_label, f_pill)
    pad_x, pad_y = 24, 10
    px, py = 60, 60
    d.rounded_rectangle(
        [px, py, px + pw + pad_x * 2, py + ph + pad_y * 2],
        radius=999, fill=(47, 43, 23), outline=ACCENT, width=2,
    )
    d.text((px + pad_x, py + pad_y), pill_label, font=f_pill, fill=ACCENT)

    # main title — two lines, very large
    f_title_1 = font(110, bold=True)
    f_title_2 = font(110, bold=True)
    line1 = "fhevm-oracle"
    line2 = "skill"
    t1w, t1h = measure(d, line1, f_title_1)
    d.text((60, 150), line1, font=f_title_1, fill=FG)
    # second line — slightly indented, accent color
    d.text((60, 270), line2, font=f_title_2, fill=ACCENT)

    # sub-claim — what it does
    f_sub = font(38, bold=True)
    sub_lines = [
        "async-decryption pattern",
        "AI agents finally write correct",
    ]
    # rendered as: "AI agents finally write correct" then "async-decryption pattern"
    d.text((60, 420), sub_lines[1], font=f_sub, fill=MUTED)
    d.text((60, 470), sub_lines[0], font=f_sub, fill=FG)

    # right side — visual marker
    # large monospace "10/10" emphasizing 10 anti-patterns
    f_count = font(180, bold=True, mono=True)
    count_text = "10"
    cw, ch = measure(d, count_text, f_count)
    cx = W - cw - 100
    cy = 200
    # ring around it
    d.ellipse(
        [cx - 60, cy - 30, cx + cw + 60, cy + ch + 30],
        outline=ACCENT, width=8,
    )
    d.text((cx, cy), count_text, font=f_count, fill=ACCENT)
    # caption under
    f_cap = font(28, bold=True)
    cap_text = "ANTI-PATTERNS"
    capw, _ = measure(d, cap_text, f_cap)
    d.text((cx + (cw - capw) // 2, cy + ch + 50), cap_text, font=f_cap, fill=FG)
    # second caption
    f_cap2 = font(22)
    cap2_text = "drilled by SKILL.md"
    cap2w, _ = measure(d, cap2_text, f_cap2)
    d.text((cx + (cw - cap2w) // 2, cy + ch + 90), cap2_text, font=f_cap2, fill=MUTED)

    # bottom row — repo + sepolia badge
    f_foot = font(24, bold=True, mono=True)
    foot_label = "github.com/cryptoyasenka/fhevm-oracle-skill"
    fw, fh = measure(d, foot_label, f_foot)
    d.text((60, H - 60), foot_label, font=f_foot, fill=MUTED)

    # sepolia badge bottom right
    f_badge = font(22, bold=True)
    badge = "LIVE ON SEPOLIA"
    bw, bh = measure(d, badge, f_badge)
    pad_x, pad_y = 18, 8
    bx = W - bw - pad_x * 2 - 60
    by = H - bh - pad_y * 2 - 50
    d.rounded_rectangle(
        [bx, by, bx + bw + pad_x * 2, by + bh + pad_y * 2],
        radius=8, fill=(20, 50, 30), outline=OK, width=2,
    )
    d.text((bx + pad_x, by + pad_y), badge, font=f_badge, fill=OK)

    out = OUT / "youtube-1280x720.png"
    img.save(out)
    print(f"  wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    print(f"Rendering YouTube thumbnail → {OUT}")
    render()
    print("Done. Upload this as Custom thumbnail on YouTube.")

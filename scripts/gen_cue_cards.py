"""
Generate teleprompter cue cards for the demo voice-over.

Each segment's voice-over text is rendered as a 1920x1080 PNG with large
readable text. Yana opens these on a second monitor (or phone) while
recording and reads them off — synchronizes with the on-screen action
in the recorded window.

Run:    python scripts/gen_cue_cards.py
Output: cue-cards/seg1-hook.png .. seg6-outro.png
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
OUT  = ROOT / "cue-cards"
OUT.mkdir(exist_ok=True)

W, H        = 1920, 1080
BG          = (11, 13, 18)
FG          = (232, 236, 243)
MUTED       = (138, 147, 166)
ACCENT      = (255, 214, 51)
DANGER      = (255, 107, 107)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["arialbd.ttf"] if bold else ["arial.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def measure(d, s, fnt):
    bbox = d.textbbox((0, 0), s, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def write(img: Image.Image, name: str):
    img.save(OUT / name)
    print(f"  wrote cue-cards/{name}")


# Each segment: (id, title, duration, [(line, accent_word_or_None), ...], hint)
# accent_word in line = render in ACCENT yellow + bold. Use None for plain.

SEGMENTS = [
    (
        "seg1-hook", "1 — HOOK", "22 sec",
        [
            ("F H E V M.", "F H E V M"),
            ("It keeps your data secret.", None),
            ("But to read a value,", None),
            ("you call the ORACLE.", "ORACLE"),
            ("AI agents make TEN MISTAKES here.", "TEN MISTAKES"),
            ("We built a skill file to fix that.", None),
            ("Plus a live contract on SEPOLIA.", "SEPOLIA"),
        ],
        "FHEVM = «ef eitch ee vee em» (по буквам)",
    ),
    (
        "seg2-problem", "2 — PROBLEM", "35 sec",
        [
            ("AI agents skip the SIGNATURE CHECK.", "SIGNATURE CHECK"),
            ("So FAKE DATA passes.", "FAKE DATA"),
            ("They save the value before the replay flag.", None),
            ("So one proof works TWICE.", "TWICE"),
            ("They use a sync call that does not exist.", None),
            ("They miss the time check by ONE SECOND.", "ONE SECOND"),
            ("The skill teaches all TEN TRAPS.", "TEN TRAPS"),
        ],
        "медленно, 84 wpm — у тебя ЗАПАС времени",
    ),
    (
        "seg3-contract", "3 — CONTRACT", "35 sec",
        [
            ("This is a-sink ri-VEEL vawlt.", "a-sink ri-VEEL vawlt"),
            ("The demo contract from the skill.", None),
            ("Look here.", None),
            ("The signature check runs FIRST.", "FIRST"),
            ("Only small input checks come before.", None),
            ("The replay flag goes up BEFORE the value.", "BEFORE"),
            ("So the same proof can not run twice.", None),
            ("The time check uses GREATER THAN, not equal.", "GREATER THAN"),
            ("Two hundred twenty lines. One file.", None),
        ],
        "мышкой: 152 → 155 → 106 → Ctrl+Shift+− 3×",
    ),
    (
        "seg4-tests", "4 — TESTS", "25 sec",
        [
            ("Four Hardhat tests run in mock mode.", None),
            ("They cover the same traps.", None),
            ("MISSING signature.", "MISSING"),
            ("REPLAY attack.", "REPLAY"),
            ("TIME off by one.", "TIME"),
            ("And the happy path.", None),
            ("A contract from the skill PASSES THEM ALL.", "PASSES THEM ALL"),
        ],
        "уже запустила `npx hardhat test`? Ждёшь 4 passing",
    ),
    (
        "seg5-demo", "5 — LIVE DEMO", "45 sec",
        [
            ("Now the live demo on SEPOLIA.", "SEPOLIA"),
            ("I lock the number SIXTY THREE.", "SIXTY THREE"),
            ("The S D K encrypts it.", "S D K"),
            ("I set a sixty second timer.", None),
            ("Lock. Sign. Done.", None),
            ("— (sixty seconds pass) —", None),
            ("I trigger the reveal.", None),
            ("Now I call fulfill.", None),
            ("The callback checks the signature.", None),
            ("Sets the replay flag. Writes the value.", None),
            ("SIXTY THREE.", "SIXTY THREE"),
            ("The number stayed secret until the timer.", None),
        ],
        "wait 60s = в CapCut ускоришь до 3 сек",
    ),
    (
        "seg6-outro", "6 — OUTRO", "18 sec",
        [
            ("Repo at GIT-hab dot com", "GIT-hab"),
            ("slash KRIP-to ya-SEN-ka", "KRIP-to ya-SEN-ka"),
            ("slash f h e v m oracle skill.", None),
            ("Skill file for the BOUNTY.", "BOUNTY"),
            ("Contract for the BUILDER track.", "BUILDER"),
            ("License B S D three clause clear.", "B S D"),
            ("Thanks Zama.", "Thanks Zama"),
        ],
        "финал — улыбнись в голос",
    ),
]


def render_segment(slug, title, duration, lines, hint):
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)

    f_title = font(48, bold=True)
    f_meta  = font(36)
    f_body  = font(58, bold=False)
    f_body_b = font(58, bold=True)
    f_hint  = font(30)

    # header
    text_left = 80
    d.text((text_left, 50), title, font=f_title, fill=ACCENT)
    duration_w, _ = measure(d, duration, f_meta)
    d.text((W - duration_w - 80, 60), duration, font=f_meta, fill=MUTED)
    # separator
    d.rectangle([text_left, 130, W - 80, 134], fill=ACCENT)

    # body: vertically distributed
    n = len(lines)
    body_top = 200
    body_bot = H - 130
    line_h = (body_bot - body_top) // max(n, 1)

    for i, (line, accent_word) in enumerate(lines):
        y = body_top + i * line_h + line_h // 2
        if accent_word and accent_word in line:
            # split into 3 parts: before / accent / after — render with separate fills
            before, _, rest = line.partition(accent_word)
            after = rest
            parts = [(before, FG, f_body), (accent_word, ACCENT, f_body_b), (after, FG, f_body)]
            total_w = sum(measure(d, p, fn)[0] for p, _, fn in parts)
            x = (W - total_w) // 2
            for p, fill, fn in parts:
                pw, ph = measure(d, p, fn)
                d.text((x, y - ph // 2), p, font=fn, fill=fill)
                x += pw
        else:
            lw, lh = measure(d, line, f_body)
            d.text(((W - lw) // 2, y - lh // 2), line, font=f_body, fill=FG)

    # footer hint
    if hint:
        hw, _ = measure(d, hint, f_hint)
        d.text(((W - hw) // 2, H - 70), hint, font=f_hint, fill=MUTED)

    write(img, f"{slug}.png")


if __name__ == "__main__":
    print(f"Rendering cue cards → {OUT}")
    for slug, title, dur, lines, hint in SEGMENTS:
        render_segment(slug, title, dur, lines, hint)
    print("Done. Open these on a second monitor while recording.")

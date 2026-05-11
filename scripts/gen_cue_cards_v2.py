"""
Generate v2 teleprompter cue cards for the 2:29 final cut.

Differences from gen_cue_cards.py:
- 6 cards instead of 7 (clip4 tests segment dropped from timeline)
- seg3 (contract) shortened from 35s to 29s; closer is "Four Hardhat tests pass"
  (compensates for the removed clip4 messaging)
- segments renumbered: original seg5a/5b → seg4/seg5; seg6 stays
- mouse-cue hints removed from seg3 (clip3-v2 is fully pre-rendered,
  no live VS Code navigation needed)

Run:    python scripts/gen_cue_cards_v2.py
Output: cue-cards/seg1-hook-v2.png .. seg6-outro-v2.png
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


SEGMENTS = [
    (
        "seg1-hook-v2", "1 — HOOK", "22 sec  ·  0:00–0:22",
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
        "seg2-problem-v2", "2 — PROBLEM", "35 sec  ·  0:22–0:57",
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
        "seg3-contract-v2", "3 — CONTRACT", "29 sec  ·  0:57–1:26",
        [
            ("This is a-sink ri-VEEL vawlt.", "a-sink ri-VEEL vawlt"),
            ("The demo contract from the skill.", None),
            ("The signature check runs FIRST.", "FIRST"),
            ("Only small input checks come before.", None),
            ("The replay flag goes up BEFORE the value.", "BEFORE"),
            ("So the same proof can not run twice.", None),
            ("The time check uses GREATER THAN, not equal.", "GREATER THAN"),
            ("FOUR HARDHAT TESTS PASS.", "FOUR HARDHAT TESTS PASS"),
        ],
        "clip3-v2 уже готов, мышкой ничего не делаешь — просто читай",
    ),
    (
        "seg4-demo-lock-v2", "4 — LIVE DEMO (lock)", "20 sec  ·  1:26–1:46",
        [
            ("Now the live demo on SEPOLIA.", "SEPOLIA"),
            ("I lock the number SIXTY THREE.", "SIXTY THREE"),
            ("The S D K encrypts it.", "S D K"),
            ("I set a sixty second timer.", None),
            ("Lock.", "Lock"),
            ("Sign.", "Sign"),
            ("Done.", "Done"),
        ],
        "после Done — открываешь cue card 5",
    ),
    (
        "seg5-demo-reveal-v2", "5 — LIVE DEMO (reveal)", "25 sec  ·  1:46–2:11",
        [
            ("Sixty seconds pass.", None),
            ("I trigger the reveal.", "trigger"),
            ("The callback checks the SIGNATURE first.", "SIGNATURE"),
            ("Then sets the REPLAY FLAG.", "REPLAY FLAG"),
            ("Then writes the value.", None),
            ("SIXTY THREE.", "SIXTY THREE"),
            ("The number stayed secret until the timer.", None),
        ],
        "финал демо — улыбка в голос",
    ),
    (
        "seg6-outro-v2", "6 — OUTRO", "18 sec  ·  2:11–2:29",
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

    text_left = 80
    d.text((text_left, 50), title, font=f_title, fill=ACCENT)
    duration_w, _ = measure(d, duration, f_meta)
    d.text((W - duration_w - 80, 60), duration, font=f_meta, fill=MUTED)
    d.rectangle([text_left, 130, W - 80, 134], fill=ACCENT)

    n = len(lines)
    body_top = 200
    body_bot = H - 130
    line_h = (body_bot - body_top) // max(n, 1)

    for i, (line, accent_word) in enumerate(lines):
        y = body_top + i * line_h + line_h // 2
        if accent_word and accent_word in line:
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

    if hint:
        hw, _ = measure(d, hint, f_hint)
        d.text(((W - hw) // 2, H - 70), hint, font=f_hint, fill=MUTED)

    write(img, f"{slug}.png")


if __name__ == "__main__":
    print(f"Rendering v2 cue cards → {OUT}")
    for slug, title, dur, lines, hint in SEGMENTS:
        render_segment(slug, title, dur, lines, hint)
    print("Done. Open these on a second monitor while recording.")

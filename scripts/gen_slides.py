"""
Generate 1920x1080 PNG slides for the demo video — drop into CapCut as image clips.

Run:    python scripts/gen_slides.py
Output: slides/01-title.png ... slides/07-callout-checksig.png ...

No external assets. Uses Pillow (already installed) + system Arial.
Brand colors mirror frontend/app/globals.css: bg #0b0d12, fg #e8ecf3, accent #ffd633.
"""

from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Windows + Python 3.14 default stdout = cp1251; force UTF-8 for arrows/checkmarks.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "slides"
OUT.mkdir(exist_ok=True)

# --- design tokens ----------------------------------------------------------

W, H        = 1920, 1080
BG          = (11, 13, 18)         # #0b0d12
BG_ELEV     = (17, 20, 27)         # #11141b
FG          = (232, 236, 243)      # #e8ecf3
MUTED       = (138, 147, 166)      # #8a93a6
ACCENT      = (255, 214, 51)       # #ffd633
ACCENT_DIM  = (255, 214, 51, 40)
DANGER      = (255, 107, 107)      # #ff6b6b
OK          = (94, 210, 138)       # #5ed28a
BORDER      = (28, 33, 44)         # #1c212c

def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        ["consolab.ttf", "consola.ttf"] if mono else
        ["arialbd.ttf", "arial.ttf"] if bold else
        ["arial.ttf"]
    )
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

def new_canvas(transparent: bool = False) -> Image.Image:
    if transparent:
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return Image.new("RGB", (W, H), BG)

def text(d: ImageDraw.ImageDraw, xy, s, *, fnt, fill=FG, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)

def measure(d: ImageDraw.ImageDraw, s, fnt):
    bbox = d.textbbox((0, 0), s, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def pill(d, x, y, label, *, fnt, fg=ACCENT, bg=(47, 43, 23), pad=(28, 12), radius=999):
    # bg pre-mixed at ~15% accent over BG so it works on plain RGB canvas.
    w, h = measure(d, label, fnt)
    box = [x, y, x + w + pad[0] * 2, y + h + pad[1] * 2]
    d.rounded_rectangle(box, radius=radius, fill=bg, outline=ACCENT, width=2)
    text(d, (x + pad[0], y + pad[1]), label, fnt=fnt, fill=fg)
    return box[2] - box[0], box[3] - box[1]

def card(d, x, y, w, h, *, fill=BG_ELEV, border=BORDER, radius=24):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, outline=border, width=2, fill=fill)

def write(img: Image.Image, name: str):
    img.save(OUT / name)
    print(f"  wrote slides/{name}")

# --- 01: title --------------------------------------------------------------

def slide_01_title():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    title  = "fhevm-oracle"
    sub    = "async-decryption skill for FHEVM agents"
    bottom = "Zama Developer Program — Mainnet S2 — Bounty + Builder Track"

    f_pill = font(28, bold=True)
    pill_label = "FHEVM · Sepolia testnet"
    pw, ph = measure(d, pill_label, f_pill)
    pill(d, (W - pw - 56) // 2, 220, pill_label, fnt=f_pill)

    f_title = font(190, bold=True)
    tw, th = measure(d, title, f_title)
    text(d, ((W - tw) // 2, 320), title, fnt=f_title, fill=FG)

    f_sub = font(56)
    sw, _ = measure(d, sub, f_sub)
    text(d, ((W - sw) // 2, 580), sub, fnt=f_sub, fill=MUTED)

    f_bot = font(32)
    bw, _ = measure(d, bottom, f_bot)
    text(d, ((W - bw) // 2, 880), bottom, fnt=f_bot, fill=MUTED)

    write(img, "01-title.png")

# --- 02: anti-patterns ------------------------------------------------------

def slide_02_anti_patterns():
    img = new_canvas()
    d = ImageDraw.Draw(img)

    f_h = font(72, bold=True)
    text(d, (120, 100), "5 ways agents botch async decrypt", fnt=f_h)

    items = [
        ("AP-001", "No checkSignatures → fake-decryption attack"),
        ("AP-002", "No replay guard → same proof submitted twice"),
        ("AP-003", "Handles[i] ↔ abi.decode tuple swapped"),
        ("AP-007", "Calling FHE.decrypt() — doesn't exist on mainnet"),
        ("AP-010", "block.timestamp >= revealAt — off by one"),
    ]
    f_tag  = font(36, bold=True, mono=True)
    f_text = font(40)
    y = 280
    for tag, body in items:
        d.rounded_rectangle([120, y, 360, y + 70], radius=14, fill=(50, 22, 26), outline=DANGER, width=2)
        text(d, (240, y + 35), tag, fnt=f_tag, fill=DANGER, anchor="mm")
        text(d, (400, y + 35), body, fnt=f_text, fill=FG, anchor="lm")
        y += 130

    f_foot = font(34)
    text(d, (120, 970), "The skill drills all ten as muscle memory.", fnt=f_foot, fill=MUTED)
    write(img, "02-anti-patterns.png")

# --- 03: safety checklist ---------------------------------------------------

def slide_03_safety():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    f_h = font(64, bold=True)
    text(d, (120, 100), "What an agent loaded with the skill writes", fnt=f_h)
    f_sub = font(34)
    text(d, (120, 190), "AsyncRevealVault.sol — every line below is a live commit.", fnt=f_sub, fill=MUTED)

    items = [
        ("✓", "checkSignatures(handles, cleartexts, proof) runs before any state write"),
        ("✓", "revealed = true consumed BEFORE any cleartext write"),
        ("✓", "handles[i] order matches abi.decode tuple position"),
        ("✓", "FHE.allowThis + FHE.allow(_, depositor) after lock()"),
        ("✓", "Strict > on revealAt — at-the-second is too early"),
        ("✓", "No external calls in fulfillReveal — replay/reentry by construction"),
    ]
    f_check = font(56, bold=True)
    f_text  = font(38)
    y = 320
    for mark, body in items:
        text(d, (140, y), mark, fnt=f_check, fill=OK)
        text(d, (220, y + 14), body, fnt=f_text, fill=FG)
        y += 90

    write(img, "03-safety.png")

# --- 04: tests --------------------------------------------------------------

def slide_04_tests():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    f_h = font(72, bold=True)
    text(d, (120, 100), "Mock-mode Hardhat tests — 4/4 pass", fnt=f_h)

    cases = [
        "rejects triggerReveal before revealAt   (AP-010)",
        "rejects fulfillReveal with no signatures (AP-001)",
        "rejects second fulfillReveal             (AP-002)",
        "decrypts amount + secret after revealAt  (canonical)",
    ]
    f_mono = font(38, mono=True)
    y = 320
    for c in cases:
        text(d, (180, y), "✓", fnt=font(48, bold=True), fill=OK)
        text(d, (260, y + 8), c, fnt=f_mono, fill=FG)
        y += 90
    f_foot = font(36)
    text(d, (120, 920), "A contract written from the skill passes them by construction.",
         fnt=f_foot, fill=MUTED)
    write(img, "04-tests.png")

# --- 05: live demo callout --------------------------------------------------

def slide_05_live():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    f_h = font(72, bold=True)
    text(d, (120, 120), "Live on Sepolia — try it yourself", fnt=f_h)

    items = [
        ("Frontend",  "fhevm-oracle-frontend.vercel.app"),
        ("Contract",  "0x256e8948057982D483C60F7c060E3253a4d6A49b"),
        ("Network",   "Sepolia testnet · chainId 11155111"),
        ("Repo",      "github.com/cryptoyasenka/fhevm-oracle-skill"),
    ]
    f_lab  = font(34, bold=True)
    f_val  = font(40, mono=True)
    y = 320
    for lab, val in items:
        text(d, (160, y),     lab, fnt=f_lab, fill=ACCENT)
        text(d, (160, y + 60), val, fnt=f_val, fill=FG)
        y += 160
    write(img, "05-live.png")

# --- 06: outro --------------------------------------------------------------

def slide_06_outro():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    f_h = font(96, bold=True)
    title = "Drop SKILL.md, ship correct FHEVM."
    tw, _ = measure(d, title, f_h)
    text(d, ((W - tw) // 2, 220), title, fnt=f_h, fill=FG)

    f_lines = font(40, mono=True)
    lines = [
        "github.com/cryptoyasenka/fhevm-oracle-skill",
        "",
        "AsyncRevealVault on Sepolia:",
        "0x256e8948057982D483C60F7c060E3253a4d6A49b",
        "",
        "License: BSD-3-Clause-Clear",
    ]
    y = 460
    for line in lines:
        if not line:
            y += 50; continue
        lw, _ = measure(d, line, f_lines)
        text(d, ((W - lw) // 2, y), line, fnt=f_lines, fill=ACCENT if "github" in line else FG)
        y += 60

    f_foot = font(34)
    foot = "Thanks Zama."
    fw, _ = measure(d, foot, f_foot)
    text(d, ((W - fw) // 2, 950), foot, fnt=f_foot, fill=MUTED)
    write(img, "06-outro.png")

# --- 07-09: highlight callouts (transparent overlay) ------------------------

def callout(name: str, label: str, body: str):
    img = new_canvas(transparent=True)
    d = ImageDraw.Draw(img)
    bw, bh = 900, 220
    bx, by = 60, 60  # top-left; user repositions in CapCut
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=24,
                        fill=(11, 13, 18, 235), outline=ACCENT, width=4)
    f_lab  = font(38, bold=True, mono=True)
    f_body = font(34)
    text(d, (bx + 36, by + 32), label, fnt=f_lab, fill=ACCENT)
    text(d, (bx + 36, by + 100), body, fnt=f_body, fill=FG)
    write(img, name)

def callouts():
    callout("07-callout-checksig.png", "AP-001",
            "checkSignatures runs before any state write")
    callout("08-callout-replay.png", "AP-002",
            "revealed = true BEFORE any cleartext write")
    callout("09-callout-finality.png", "AP-010",
            "Strict > on revealAt — at-the-second is too early")

# --- main -------------------------------------------------------------------

if __name__ == "__main__":
    print(f"Rendering slides → {OUT}")
    slide_01_title()
    slide_02_anti_patterns()
    slide_03_safety()
    slide_04_tests()
    slide_05_live()
    slide_06_outro()
    callouts()
    print("Done. Drop these PNGs into CapCut as image tracks.")

"""
Render segment 4 (TESTS) as a 25-second terminal-screencast MP4.

Replaces a screen-record of `npx hardhat test` running. Test names lifted
verbatim from test/AsyncRevealVault.ts:

  AP-010 finality      — rejects triggerReveal before revealAt
  canonical flow       — decrypts amount + secret after revealAt
  AP-002 replay        — rejects a second fulfillReveal
  AP-001 signature     — rejects fulfillReveal with no valid signatures

Timing matches segment 4 voice-over:
  0-3s    blank prompt
  3-6s    `npx hardhat test` typed + compile output
  6-9s    + AP-001 passes (matches "MISSING signature")
  9-12s   + AP-002 passes (matches "REPLAY attack")
  12-15s  + AP-010 passes (matches "TIME off by one")
  15-19s  + canonical passes ("happy path")
  19-25s  "4 passing (2s)" summary, large green

Run:    python scripts/gen_clip4_tests.py
Output: video-clips/clip4-tests-static.mp4
"""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "video-clips"
TMP_DIR = ROOT / "video-clips" / "_tmp_clip4"
OUT_DIR.mkdir(exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)

W, H = 1920, 1080

# Windows Terminal-ish palette
BG          = (12, 12, 12)
TITLEBAR    = (32, 32, 32)
FG          = (204, 204, 204)
PROMPT_USER = (94, 210, 138)
PROMPT_PATH = (95, 175, 222)
DIM         = (130, 130, 130)
OK          = (94, 210, 138)
YELLOW      = (255, 214, 51)
RED         = (255, 107, 107)
GRAY        = (107, 110, 116)
CURSOR      = (204, 204, 204)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["consolab.ttf", "consola.ttf"] if bold else ["consola.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def font_ui(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
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


# Pre-canned terminal session — what Yana would see line-by-line
PROMPT = ("PS C:\\Projects\\fhevm-oracle-skill> ", PROMPT_USER)
TYPED  = "npx hardhat test"

# Lines that appear progressively (each shot adds more)
COMPILE_BLOCK = [
    ("Compiled 4 Solidity files successfully (evm target: cancun).", DIM),
    ("", FG),
    ("  AsyncRevealVault", FG),
]

TEST_AP001 = (
    "    √ rejects fulfillReveal with no valid signatures (AP-001)",
    OK,
)
TEST_AP002 = (
    "    √ rejects a second fulfillReveal after a successful one (AP-002 replay)",
    OK,
)
TEST_AP010 = (
    "    √ rejects triggerReveal before revealAt (AP-010 finality)",
    OK,
)
TEST_CANON = (
    "    √ decrypts amount + secret after revealAt (canonical flow)",
    OK,
)

SUMMARY_BLOCK = [
    ("", FG),
    ("", FG),
    ("  4 passing (2s)", OK),
]


def draw_terminal_frame(
    *,
    lines: list[tuple[str, tuple[int, int, int]]],
    cursor_after_typed: bool = False,
    typed_text: str = "",
    show_prompt: bool = True,
    top_label: str = "",
    bottom_label: str = "",
    big_summary: bool = False,
) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Titlebar
    titlebar_h = 60
    d.rectangle([0, 0, W, titlebar_h], fill=TITLEBAR)
    f_title = font_ui(26, bold=False)
    d.text((30, 16), "PowerShell  —  fhevm-oracle-skill",
           font=f_title, fill=(204, 204, 204))
    for ix, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = W - 30 - ix * 30
        d.ellipse([cx - 8, 22, cx + 8, 38], fill=col)

    # Top label strip
    if top_label:
        d.rectangle([0, titlebar_h, W, titlebar_h + 50], fill=(17, 20, 27))
        f_label = font_ui(34, bold=True)
        lw, _ = measure(d, top_label, f_label)
        d.text(((W - lw) // 2, titlebar_h + 8), top_label, font=f_label, fill=YELLOW)
        body_top = titlebar_h + 80
    else:
        body_top = titlebar_h + 30

    # If big_summary, render giant centered text
    if big_summary:
        f_huge = font(180, bold=True)
        text = "4 passing"
        tw, th = measure(d, text, f_huge)
        x = (W - tw) // 2
        y = (H - th) // 2 - 60
        d.text((x, y), text, font=f_huge, fill=OK)
        # subtitle
        f_sub = font(48)
        subtitle = "(2s)"
        sw, _ = measure(d, subtitle, f_sub)
        d.text(((W - sw) // 2, y + th + 30), subtitle, font=f_sub, fill=DIM)
        # check ring
        ring_r = 80
        rx = (W - tw) // 2 - ring_r * 2
        ry = y + th // 2
        d.ellipse([rx - ring_r, ry - ring_r, rx + ring_r, ry + ring_r],
                  outline=OK, width=8)
        f_check = font(110, bold=True)
        check = "√"
        chw, chh = measure(d, check, f_check)
        d.text((rx - chw // 2, ry - chh // 2 - 8), check, font=f_check, fill=OK)
    else:
        # Render terminal lines
        f_term = font(26)
        f_prompt = font(26, bold=True)
        line_h = 38
        x_left = 60
        y = body_top

        if show_prompt:
            prompt_str, prompt_color = PROMPT
            d.text((x_left, y), prompt_str, font=f_prompt, fill=prompt_color)
            pw, _ = measure(d, prompt_str, f_prompt)
            if typed_text:
                d.text((x_left + pw, y), typed_text, font=f_term, fill=FG)
                tw, _ = measure(d, typed_text, f_term)
                if cursor_after_typed:
                    # blinking cursor (just draw)
                    d.rectangle(
                        [x_left + pw + tw + 4, y + 4,
                         x_left + pw + tw + 4 + 14, y + 32],
                        fill=CURSOR,
                    )
            elif cursor_after_typed:
                d.rectangle([x_left + pw + 2, y + 4, x_left + pw + 16, y + 32],
                            fill=CURSOR)
            y += line_h

        # output lines
        for line, color in lines:
            d.text((x_left, y), line, font=f_term, fill=color)
            y += line_h

        # final prompt (after summary, if applicable)

    # Bottom label
    if bottom_label:
        d.rectangle([0, H - 70, W, H], fill=(17, 20, 27))
        f_bl = font_ui(24)
        lw, _ = measure(d, bottom_label, f_bl)
        d.text(((W - lw) // 2, H - 52), bottom_label, font=f_bl, fill=FG)

    return img


SHOTS = [
    dict(
        name="shotA-prompt",
        lines=[],
        typed="",
        cursor=True,
        top="$ npx hardhat test  —  4 tests, mock mode",
        bottom="four mock-mode tests drilling the same traps",
        seconds=3,
    ),
    dict(
        name="shotB-compile",
        lines=COMPILE_BLOCK,
        typed=TYPED,
        cursor=False,
        top="$ npx hardhat test  —  4 tests, mock mode",
        bottom="compiling Solidity 0.8.27 — evm cancun",
        seconds=3,
    ),
    dict(
        name="shotC-ap001",
        lines=COMPILE_BLOCK + [TEST_AP001],
        typed=TYPED,
        cursor=False,
        top="AP-001  ·  MISSING signature  →  reverts",
        bottom="fulfill without proof is rejected",
        seconds=3,
    ),
    dict(
        name="shotD-ap002",
        lines=COMPILE_BLOCK + [TEST_AP001, TEST_AP002],
        typed=TYPED,
        cursor=False,
        top="AP-002  ·  REPLAY attack  →  reverts",
        bottom="second fulfill on the same vault is rejected",
        seconds=3,
    ),
    dict(
        name="shotE-ap010",
        lines=COMPILE_BLOCK + [TEST_AP001, TEST_AP002, TEST_AP010],
        typed=TYPED,
        cursor=False,
        top="AP-010  ·  TIME off by one  →  reverts",
        bottom="trigger at exactly revealAt is too early (strict >)",
        seconds=3,
    ),
    dict(
        name="shotF-canonical",
        lines=COMPILE_BLOCK + [TEST_AP001, TEST_AP002, TEST_AP010, TEST_CANON],
        typed=TYPED,
        cursor=False,
        top="canonical flow  ·  encrypt → trigger → fulfill  →  passes",
        bottom="happy path: amount + secret revealed in cleartext",
        seconds=4,
    ),
    dict(
        name="shotG-summary",
        lines=[],
        typed=TYPED,
        cursor=False,
        top="A contract from the skill passes them all",
        bottom="4 passing  ·  mock mode  ·  Hardhat",
        seconds=6,
        big_summary=True,
    ),
]


def render():
    print("Rendering segment 4 (TESTS) shots...")
    shot_mp4s: list[Path] = []
    for shot in SHOTS:
        png_path = TMP_DIR / f"{shot['name']}.png"
        img = draw_terminal_frame(
            lines=shot["lines"],
            cursor_after_typed=shot["cursor"],
            typed_text=shot["typed"],
            top_label=shot["top"],
            bottom_label=shot["bottom"],
            big_summary=shot.get("big_summary", False),
        )
        img.save(png_path)

        shot_mp4 = TMP_DIR / f"{shot['name']}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(png_path),
            "-t", str(shot["seconds"]),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-vf", "scale=1920:1080",
            "-preset", "fast",
            "-crf", "20",
            str(shot_mp4),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ffmpeg stderr for {shot['name']}:\n{result.stderr}")
            raise SystemExit(result.returncode)
        print(f"  shot {shot['name']:20s} -> {shot_mp4.name}  ({shot['seconds']}s)")
        shot_mp4s.append(shot_mp4)

    concat_file = TMP_DIR / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in shot_mp4s),
        encoding="utf-8",
    )

    out_mp4 = OUT_DIR / "clip4-tests-static.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(out_mp4),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg stderr:\n{result.stderr}")
        raise SystemExit(result.returncode)
    print(f"  wrote {out_mp4.relative_to(ROOT)}")


if __name__ == "__main__":
    render()
    print("\nDone. Drop video-clips/clip4-tests-static.mp4 into CapCut.")

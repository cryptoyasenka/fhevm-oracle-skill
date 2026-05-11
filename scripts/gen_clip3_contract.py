"""
Render segment 3 (CONTRACT) as a 35-second static-keyframe MP4.

Replaces a screen-record of VS Code highlighting key lines of AsyncRevealVault.sol.
Outputs a video that looks like a VS Code dark editor with synthetic highlights
on the three anti-pattern lines (158, 161, 111).

Timing (matches voice-over for segment 3):
    0-3s   shot A — fulfillReveal() declaration (line 138 area), no highlight
    3-12s  shot B — line 158 highlighted (checkSignatures FIRST)
    12-21s shot C — line 161 highlighted (revealed = true BEFORE)
    21-30s shot D — line 111 highlighted (strict > time check)
    30-35s shot E — zoomed out, three highlights visible on full file

Run:    python scripts/gen_clip3_contract.py
Output: video-clips/clip3-contract-static.mp4
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
SRC = ROOT / "contracts" / "AsyncRevealVault.sol"
OUT_DIR = ROOT / "video-clips"
TMP_DIR = ROOT / "video-clips" / "_tmp_clip3"
OUT_DIR.mkdir(exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)

W, H = 1920, 1080

# VS Code Dark+ palette
BG          = (30, 30, 30)
ACTIVE_LINE = (45, 45, 48)
GUTTER      = (133, 133, 133)
FG          = (212, 212, 212)
COMMENT     = (106, 153, 85)
KEYWORD     = (86, 156, 214)
TYPE        = (78, 201, 176)
FUNC_NAME   = (220, 220, 170)
STRING      = (206, 145, 120)
NUMBER      = (181, 206, 168)
HIGHLIGHT   = (255, 214, 51)    # accent yellow
ACCENT_BG   = (84, 64, 12)      # dark yellow translucent target
LABEL_BG    = (17, 20, 27)
DANGER      = (255, 107, 107)

KEYWORDS = {
    "function", "external", "internal", "public", "private", "view", "pure",
    "returns", "return", "if", "else", "revert", "emit", "storage", "memory",
    "calldata", "new", "import", "pragma", "contract", "struct", "mapping",
    "address", "bool", "true", "false", "constructor", "modifier", "require",
    "using", "for", "is", "this",
}
TYPES = {
    "uint256", "uint64", "uint32", "uint8", "int256", "bytes", "bytes32",
    "string", "euint64", "euint256", "externalEuint64", "externalEuint256",
    "FHE", "Vault", "ZamaEthereumConfig",
}


def font(size: int, bold: bool = False, mono: bool = True) -> ImageFont.FreeTypeFont:
    names = (
        ["consolab.ttf", "consola.ttf"] if mono and bold else
        ["consola.ttf"] if mono else
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


def tokenize_line(line: str):
    """Return list of (text, color) for one line of Solidity source."""
    # Detect comment start (handles `// ...` and `/// ...`)
    stripped = line
    out = []
    # Find // outside of strings — simple version: just split on first //
    if "//" in stripped:
        before, _, comment = stripped.partition("//")
        if before.strip():
            out.extend(_tokenize_code(before))
        out.append(("//" + comment, COMMENT))
        return out
    return _tokenize_code(stripped)


def _tokenize_code(text: str):
    """Tokenize non-comment code into (text, color) tuples."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        # whitespace
        if ch in " \t":
            j = i
            while j < n and text[j] in " \t":
                j += 1
            out.append((text[i:j], FG))
            i = j
            continue
        # string literal
        if ch == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 1
            j = min(j + 1, n)
            out.append((text[i:j], STRING))
            i = j
            continue
        # identifier / keyword
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            if word in KEYWORDS:
                color = KEYWORD
            elif word in TYPES:
                color = TYPE
            elif j < n and text[j] == "(":
                color = FUNC_NAME
            else:
                color = FG
            out.append((word, color))
            i = j
            continue
        # number
        if ch.isdigit():
            j = i
            while j < n and (text[j].isalnum() or text[j] == "."):
                j += 1
            out.append((text[i:j], NUMBER))
            i = j
            continue
        # punctuation / operator
        out.append((ch, FG))
        i += 1
    return out


def read_source() -> list[str]:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    return lines


def draw_code_frame(
    *,
    src_lines: list[str],
    center_line: int,
    highlight_lines: set[int],
    label_top: str,
    label_bottom: str,
    font_size: int = 28,
    visible_rows: int = 30,
    show_full_file: bool = False,
) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    if show_full_file:
        # Squish the entire file into the viewport
        return draw_full_file_frame(
            src_lines=src_lines, highlight_lines=highlight_lines,
            label_top=label_top, label_bottom=label_bottom,
        )

    f = font(font_size, mono=True)
    f_label = font(34, bold=True, mono=False)
    f_label_small = font(24, mono=False)

    line_h = font_size + 12
    gutter_w = 110
    code_left = gutter_w + 40
    code_top = 110
    code_bottom = H - 130
    visible_rows = (code_bottom - code_top) // line_h

    # Determine first visible line
    half = visible_rows // 2
    first_visible = max(1, center_line - half)
    last_visible = min(len(src_lines), first_visible + visible_rows - 1)
    if last_visible - first_visible + 1 < visible_rows:
        first_visible = max(1, last_visible - visible_rows + 1)

    # Title bar (filename)
    titlebar_h = 60
    d.rectangle([0, 0, W, titlebar_h], fill=(45, 45, 48))
    f_title = font(26, mono=False)
    title_text = "AsyncRevealVault.sol  —  fhevm-oracle-skill"
    d.text((30, 16), title_text, font=f_title, fill=(212, 212, 212))
    # red/yellow/green dots
    for ix, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = W - 30 - ix * 30
        d.ellipse([cx - 8, 22, cx + 8, 38], fill=col)

    # Label strip under titlebar (what to look at)
    d.rectangle([0, titlebar_h, W, titlebar_h + 50], fill=LABEL_BG)
    if label_top:
        lw, _ = measure(d, label_top, f_label)
        d.text(((W - lw) // 2, titlebar_h + 8), label_top, font=f_label, fill=HIGHLIGHT)

    # Draw lines
    for row, line_no in enumerate(range(first_visible, last_visible + 1)):
        y = code_top + row * line_h
        # Active highlight background
        if line_no in highlight_lines:
            d.rectangle([gutter_w, y - 2, W - 30, y + line_h - 2], fill=ACCENT_BG)

        # Gutter line number
        ln = str(line_no)
        lnw, lnh = measure(d, ln, f)
        d.text((gutter_w - lnw - 20, y), ln, font=f, fill=GUTTER)

        # Code line — tokenized
        if 1 <= line_no <= len(src_lines):
            tokens = tokenize_line(src_lines[line_no - 1])
            x = code_left
            for tok, color in tokens:
                tw, th = measure(d, tok, f)
                fg = HIGHLIGHT if line_no in highlight_lines else color
                d.text((x, y), tok, font=f, fill=fg)
                x += tw

    # Bottom label
    if label_bottom:
        d.rectangle([0, H - 80, W, H], fill=LABEL_BG)
        lw, _ = measure(d, label_bottom, f_label_small)
        d.text(((W - lw) // 2, H - 60), label_bottom, font=f_label_small, fill=FG)

    return img


def draw_full_file_frame(
    *,
    src_lines: list[str],
    highlight_lines: set[int],
    label_top: str,
    label_bottom: str,
) -> Image.Image:
    """Zoomed-out 'code map' frame: minimap-style bars per line + callout cards.

    Each line becomes a thin colored bar (no readable text). Bar width is
    proportional to non-whitespace content, color comes from the first token.
    The three highlighted lines get full-width yellow fill plus a labeled
    callout card on the right side pointing to them.
    """
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Titlebar (VS Code style)
    titlebar_h = 60
    d.rectangle([0, 0, W, titlebar_h], fill=(45, 45, 48))
    f_title = font(26, mono=False)
    d.text((30, 16), "AsyncRevealVault.sol  —  the whole file at a glance",
           font=f_title, fill=(212, 212, 212))
    for ix, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = W - 30 - ix * 30
        d.ellipse([cx - 8, 22, cx + 8, 38], fill=col)

    # Top label strip
    label_strip_h = 60
    d.rectangle([0, titlebar_h, W, titlebar_h + label_strip_h], fill=LABEL_BG)
    if label_top:
        f_label = font(34, bold=True, mono=False)
        lw, _ = measure(d, label_top, f_label)
        d.text(((W - lw) // 2, titlebar_h + 12), label_top, font=f_label, fill=HIGHLIGHT)

    # Layout: left = code map, right = callout cards
    map_top = titlebar_h + label_strip_h + 30
    map_bottom = H - 110
    map_left = 220
    map_right = 900
    map_h = map_bottom - map_top
    total_lines = len(src_lines)
    slot_h = map_h / total_lines  # ≈ 4.2px per line — bars only, no text

    # Gutter labels: every 20 lines, plus the highlights
    f_gutter = font(13, mono=True)
    gutter_marks = set(range(1, total_lines + 1, 20)) | highlight_lines | {total_lines}
    for i in gutter_marks:
        y = map_top + (i - 1) * slot_h
        col = HIGHLIGHT if i in highlight_lines else GUTTER
        text = str(i)
        tw, _ = measure(d, text, f_gutter)
        d.text((map_left - 12 - tw, y - 7), text, font=f_gutter, fill=col)

    # Vertical gutter divider
    d.line([(map_left - 6, map_top), (map_left - 6, map_bottom)],
           fill=(60, 60, 60), width=2)

    # Color by leading token kind
    def line_color(line: str):
        s = line.lstrip()
        if not s:
            return None
        if s.startswith("//") or s.startswith("/*") or s.startswith("*"):
            return COMMENT
        first = ""
        for ch in s:
            if ch.isalpha() or ch == "_":
                first += ch
            else:
                break
        if first in KEYWORDS:
            return KEYWORD
        if first in TYPES:
            return TYPE
        return FG

    # Bars
    map_width = map_right - map_left
    max_content = 80  # chars mapped to full width
    for i, line in enumerate(src_lines, start=1):
        y0 = map_top + (i - 1) * slot_h
        y1 = y0 + slot_h - 0.6  # tiny gap between bars

        if i in highlight_lines:
            # Full-width bright yellow highlight
            d.rectangle([map_left - 6, y0, map_right + 6, y1],
                        fill=HIGHLIGHT)
            continue

        c = line_color(line)
        if c is None:
            continue
        content_len = len(line.rstrip()) - (len(line) - len(line.lstrip()))
        # Dim the color so highlights pop
        dim = tuple(int(v * 0.55) for v in c)
        indent_chars = len(line) - len(line.lstrip())
        indent_px = min(indent_chars, 20) / 80 * map_width
        bar_w = min(content_len, max_content) / max_content * (map_width - indent_px)
        d.rectangle([map_left + indent_px, y0, map_left + indent_px + bar_w, y1],
                    fill=dim)

    # Right-side callout cards: explicit mapping by line number
    card_left = 1000
    card_right = W - 60
    card_w = card_right - card_left
    card_h = 130
    LINE_MAP = {
        111: ("AP-010", "Strict time check",
              "if (block.timestamp <= revealAt) revert\nstrict >, not >=  ·  exact-second is too early"),
        158: ("AP-001", "Signature check FIRST",
              "FHE.checkSignatures(handles, cleartext, proof)\nbefore state  ·  reverts forged callbacks"),
        161: ("AP-002", "Replay flag BEFORE value",
              "v.revealed = true  ·  v.amountClear = a\nsame proof can never run twice"),
    }
    cards = []
    for i in sorted(highlight_lines):
        tag, title, sub = LINE_MAP.get(
            i, (f"L{i}", "Highlighted line", "")
        )
        cards.append((i, tag, title, sub))

    # Stack cards vertically with anchors on the left
    total_card_h = len(cards) * card_h + (len(cards) - 1) * 30
    start_y = map_top + (map_h - total_card_h) / 2
    f_tag = font(22, bold=True, mono=False)
    f_card_title = font(28, bold=True, mono=False)
    f_card_sub = font(20, mono=True)
    f_badge = font(16, bold=True, mono=False)
    bh = measure(d, "L999", f_badge)[1]
    min_badge_gap = bh + 14  # vertical distance to prevent overlap

    # Compute non-overlapping badge Y positions: keep close ones nudged apart
    raw_badge_ys = [map_top + (ln - 0.5) * slot_h for ln, *_ in cards]
    badge_ys = list(raw_badge_ys)
    for k in range(1, len(badge_ys)):
        if badge_ys[k] - badge_ys[k - 1] < min_badge_gap:
            badge_ys[k] = badge_ys[k - 1] + min_badge_gap

    for idx, (line_no, tag, title, sub) in enumerate(cards):
        cy = start_y + idx * (card_h + 30)
        # Card background
        d.rectangle([card_left, cy, card_right, cy + card_h], fill=LABEL_BG)
        d.rectangle([card_left, cy, card_left + 6, cy + card_h], fill=HIGHLIGHT)
        # Tag
        d.text((card_left + 22, cy + 14), tag, font=f_tag, fill=HIGHLIGHT)
        # Title
        d.text((card_left + 22, cy + 44), title, font=f_card_title, fill=FG)
        # Sub (two-line code hint)
        for j, sub_line in enumerate(sub.split("\n")):
            d.text((card_left + 22, cy + 80 + j * 24),
                   sub_line, font=f_card_sub, fill=(200, 200, 200))
        # Connector: horizontal from bar -> elbow -> card edge
        bar_y = map_top + (line_no - 0.5) * slot_h
        card_y = cy + card_h / 2
        elbow_x = (map_right + card_left) / 2 + idx * 12  # stagger to avoid overlap
        d.line([(map_right + 6, bar_y), (elbow_x, bar_y)],
               fill=HIGHLIGHT, width=2)
        d.line([(elbow_x, bar_y), (elbow_x, card_y)],
               fill=HIGHLIGHT, width=2)
        d.line([(elbow_x, card_y), (card_left, card_y)],
               fill=HIGHLIGHT, width=2)
        # Line-number badge nudged to avoid stack overlap
        badge_text = f"L{line_no}"
        bw, _ = measure(d, badge_text, f_badge)
        bx = map_right + 14
        by = badge_ys[idx] - bh / 2 - 4
        # If we nudged this badge off its bar, draw a tiny leader to the real bar
        if abs(badge_ys[idx] - bar_y) > 2:
            d.line([(bx - 8, badge_ys[idx]), (map_right + 6, bar_y)],
                   fill=HIGHLIGHT, width=1)
        d.rectangle([bx - 6, by - 4, bx + bw + 6, by + bh + 4], fill=HIGHLIGHT)
        d.text((bx, by), badge_text, font=f_badge, fill=(20, 20, 20))

    # Bottom label
    if label_bottom:
        d.rectangle([0, H - 80, W, H], fill=LABEL_BG)
        f_label_small = font(24, mono=False)
        lw, _ = measure(d, label_bottom, f_label_small)
        d.text(((W - lw) // 2, H - 55), label_bottom, font=f_label_small, fill=FG)

    return img


# -----------------------------------------------------------------------------
# Shot list
# -----------------------------------------------------------------------------

SHOTS = [
    dict(
        name="shotA-fulfillreveal",
        center=143,
        highlight=set(),
        label_top="fulfillReveal()  —  the KMS-signed callback",
        label_bottom="three small input checks  ·  then signature  ·  then state",
        seconds=3,
    ),
    dict(
        name="shotB-checksig",
        center=156,
        highlight={158},
        label_top="AP-001  ·  signature check runs FIRST",
        label_bottom="without this anyone can submit fake cleartext  ·  line 158",
        seconds=9,
    ),
    dict(
        name="shotC-replayflag",
        center=159,
        highlight={161},
        label_top="AP-002  ·  replay flag set BEFORE the value",
        label_bottom="so the same proof cannot run twice  ·  line 161",
        seconds=9,
    ),
    dict(
        name="shotD-timecheck",
        center=109,
        highlight={111},
        label_top="AP-010  ·  strict >  not >=",
        label_bottom="at exactly revealAt is too early  ·  line 111",
        seconds=9,
    ),
    dict(
        name="shotE-full",
        center=100,
        highlight={111, 158, 161},
        label_top="220 lines  ·  one file  ·  all three traps fixed",
        label_bottom="reference implementation from SKILL.md",
        seconds=5,
        full=True,
    ),
]


def render():
    src_lines = read_source()
    print(f"Source: {SRC.name} ({len(src_lines)} lines)")

    # Stage 1: render each shot to its own MP4 with exact duration via -loop+-t
    shot_mp4s: list[Path] = []
    for shot in SHOTS:
        png_path = TMP_DIR / f"{shot['name']}.png"
        img = draw_code_frame(
            src_lines=src_lines,
            center_line=shot["center"],
            highlight_lines=shot["highlight"],
            label_top=shot["label_top"],
            label_bottom=shot["label_bottom"],
            show_full_file=shot.get("full", False),
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
        print(f"  shot {shot['name']:25s} -> {shot_mp4.name}  ({shot['seconds']}s)")
        shot_mp4s.append(shot_mp4)

    # Stage 2: concat MP4s with concat demuxer (lossless, all have identical codec/params)
    concat_file = TMP_DIR / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in shot_mp4s),
        encoding="utf-8",
    )

    out_mp4 = OUT_DIR / "clip3-contract-v2.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(out_mp4),
    ]
    print(f"\nffmpeg concat -> {out_mp4.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg stderr:\n{result.stderr}")
        raise SystemExit(result.returncode)
    print(f"  wrote {out_mp4.relative_to(ROOT)}")


if __name__ == "__main__":
    render()
    print("\nDone. Drop video-clips/clip3-contract-v2.mp4 into CapCut.")

"""
Render segments 5a (LOCK, 20s) and 5b (REVEAL, 25s) as static-keyframe MP4s.

Programmatic recreation of the live frontend (https://fhevm-oracle-frontend.vercel.app)
UI states — Yana could not screen-record. Brand matches frontend/app/globals.css:
  bg #0b0d12 · bg-elev #11141b · fg #e8ecf3 · muted #8a93a6
  border #1c212c · accent #ffd633 · ok #5ed28a · danger #ff6b6b

No fake MetaMask popup screenshots — just dapp UI state strings ("Awaiting wallet
signature…") so we don't co-opt a real product's trademark visuals.

Timings match VIDEO-VOICEOVER-SIMPLE.md segments 5a / 5b.

Run:    python scripts/gen_clip5_demo.py
Output: video-clips/clip5a-lock-static.mp4 (20s)
        video-clips/clip5b-reveal-static.mp4 (25s)
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
TMP_DIR = ROOT / "video-clips" / "_tmp_clip5"
OUT_DIR.mkdir(exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)

W, H = 1920, 1080

# frontend palette
BG          = (11, 13, 18)
BG_ELEV     = (17, 20, 27)
FG          = (232, 236, 243)
MUTED       = (138, 147, 166)
BORDER      = (28, 33, 44)
ACCENT      = (255, 214, 51)
ACCENT_DARK = (84, 64, 12)
DANGER      = (255, 107, 107)
OK          = (94, 210, 138)
OK_DARK     = (20, 50, 30)


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
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


def draw_topnav(d):
    """Navbar with brand + 'Live on Sepolia' pill + wallet pill."""
    nav_h = 80
    d.rectangle([0, 0, W, nav_h], fill=BG_ELEV)
    d.line([0, nav_h, W, nav_h], fill=BORDER, width=1)

    # brand
    f_brand = font(28, bold=True, mono=True)
    d.text((60, 24), "fhevm-oracle-skill", font=f_brand, fill=FG)

    # GitHub link (right of brand)
    f_link = font(20)
    d.text((430, 30), "github", font=f_link, fill=MUTED)
    d.text((520, 30), "docs", font=f_link, fill=MUTED)

    # wallet pill (right)
    f_pill = font(20, mono=True)
    wallet = "0x7A3F…58A9"
    pw, _ = measure(d, wallet, f_pill)
    pill_x = W - 60 - pw - 32
    d.rounded_rectangle(
        [pill_x, 22, pill_x + pw + 28, 56],
        radius=999, fill=BG, outline=BORDER, width=1,
    )
    # green dot
    d.ellipse([pill_x + 14, 35, pill_x + 22, 43], fill=OK)
    d.text((pill_x + 30, 30), wallet, font=f_pill, fill=FG)

    # sepolia pill (left of wallet)
    f_sep = font(18, bold=True)
    sepolia = "SEPOLIA"
    sw, _ = measure(d, sepolia, f_sep)
    sep_x = pill_x - sw - 60
    d.rounded_rectangle(
        [sep_x, 22, sep_x + sw + 28, 56],
        radius=999, fill=OK_DARK, outline=OK, width=2,
    )
    d.text((sep_x + 14, 30), sepolia, font=f_sep, fill=OK)


def draw_status_strip(d, top_label, accent_color=ACCENT):
    if not top_label:
        return
    strip_top = 80
    strip_h = 70
    d.rectangle([0, strip_top, W, strip_top + strip_h], fill=BG_ELEV)
    d.line([0, strip_top + strip_h, W, strip_top + strip_h], fill=BORDER, width=1)
    f_label = font(36, bold=True)
    lw, _ = measure(d, top_label, f_label)
    d.text(((W - lw) // 2, strip_top + 14), top_label,
           font=f_label, fill=accent_color)


def draw_bottom_caption(d, caption):
    if not caption:
        return
    d.rectangle([0, H - 80, W, H], fill=BG_ELEV)
    d.line([0, H - 80, W, H - 80], fill=BORDER, width=1)
    f = font(22)
    cw, _ = measure(d, caption, f)
    d.text(((W - cw) // 2, H - 56), caption, font=f, fill=MUTED)


def draw_card(d, x, y, w, h, *, fill=BG_ELEV, border=BORDER):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=fill, outline=border, width=1)


def draw_lock_form(
    d, *,
    amount: str = "",
    secret: str = "",
    seconds: str = "",
    status: str = "",
    status_color=ACCENT,
    button_label: str = "Lock encrypted value",
    button_state: str = "idle",     # idle, hover, busy
    tx_hash: str = "",
):
    card_w = 900
    card_x = (W - card_w) // 2
    card_y = 240
    card_h = 620
    draw_card(d, card_x, card_y, card_w, card_h)

    f_label = font(20)
    f_input_label = font(18)
    f_input = font(26, mono=True)
    f_button = font(28, bold=True)
    f_status = font(22, bold=True)
    f_hash = font(18, mono=True)

    pad = 50

    # title
    f_title = font(36, bold=True)
    d.text((card_x + pad, card_y + 30), "Lock encrypted value",
           font=f_title, fill=FG)
    d.text((card_x + pad, card_y + 80),
           "Encrypted via FHEVM client-SDK before submit — handle on-chain",
           font=f_input_label, fill=MUTED)

    # inputs
    inputs = [
        ("Amount (uint64)", amount, "e.g. 63"),
        ("Secret (uint256)", secret, "e.g. 123456789"),
        ("Lock duration (seconds)", seconds, "e.g. 60"),
    ]
    y = card_y + 150
    for label, value, placeholder in inputs:
        d.text((card_x + pad, y), label, font=f_input_label, fill=MUTED)
        ix, iy, iw, ih = card_x + pad, y + 30, card_w - pad * 2, 50
        focused = value != ""
        outline = ACCENT if focused else BORDER
        width = 2 if focused else 1
        d.rounded_rectangle([ix, iy, ix + iw, iy + ih],
                            radius=8, fill=BG, outline=outline, width=width)
        if value:
            d.text((ix + 16, iy + 12), value, font=f_input, fill=FG)
        else:
            d.text((ix + 16, iy + 12), placeholder, font=f_input, fill=(80, 86, 100))
        y += 100

    # status row
    if status:
        sy = y + 10
        if status_color is ACCENT:
            bg = ACCENT_DARK
        elif status_color is OK:
            bg = OK_DARK
        else:
            bg = (50, 20, 20)
        sw, _ = measure(d, status, f_status)
        d.rounded_rectangle([card_x + pad, sy, card_x + pad + sw + 40, sy + 44],
                            radius=8, fill=bg, outline=status_color, width=2)
        # leading dot
        d.ellipse([card_x + pad + 14, sy + 17, card_x + pad + 28, sy + 31], fill=status_color)
        d.text((card_x + pad + 36, sy + 9), status, font=f_status, fill=status_color)

    # button
    btn_y = card_y + card_h - 100
    btn_color = ACCENT if button_state == "idle" else (220, 184, 28)
    if button_state == "busy":
        btn_color = (90, 75, 20)
    d.rounded_rectangle([card_x + pad, btn_y, card_x + card_w - pad, btn_y + 60],
                        radius=10, fill=btn_color)
    bw, _ = measure(d, button_label, f_button)
    d.text((card_x + (card_w - bw) // 2, btn_y + 14),
           button_label, font=f_button,
           fill=(11, 13, 18))

    # tx hash strip below card (when set)
    if tx_hash:
        hy = card_y + card_h + 30
        d.text((card_x + pad, hy), "Sepolia tx", font=f_input_label, fill=MUTED)
        d.text((card_x + pad + 120, hy - 2), tx_hash, font=f_hash, fill=ACCENT)


def draw_vault_card(
    d, *,
    vault_id: int = 5,
    seconds_remaining: int | None = None,
    state_label: str = "",
    state_color=ACCENT,
    reveal_value: int | None = None,
    show_handles: bool = False,
    pipeline_step: str = "",  # "sig" "replay" "value" "done"
):
    card_w = 900
    card_x = (W - card_w) // 2
    card_y = 240
    card_h = 620
    draw_card(d, card_x, card_y, card_w, card_h)

    pad = 50

    # title
    f_title = font(34, bold=True)
    d.text((card_x + pad, card_y + 30), f"Vault #{vault_id}",
           font=f_title, fill=FG)
    f_sub = font(20)
    d.text((card_x + pad, card_y + 78),
           "amount + secret — locked, awaiting decryption proof",
           font=f_sub, fill=MUTED)

    # state pill
    if state_label:
        f_state = font(22, bold=True)
        sw, _ = measure(d, state_label, f_state)
        sx = card_x + card_w - sw - 96
        sy = card_y + 36
        bg = ACCENT_DARK if state_color is ACCENT else OK_DARK
        d.rounded_rectangle([sx, sy, sx + sw + 44, sy + 40],
                            radius=999, fill=bg, outline=state_color, width=2)
        d.ellipse([sx + 14, sy + 14, sx + 26, sy + 26], fill=state_color)
        d.text((sx + 34, sy + 7), state_label, font=f_state, fill=state_color)

    # countdown / timer area
    f_timer_label = font(20)
    if seconds_remaining is not None:
        d.text((card_x + pad, card_y + 160), "Time remaining",
               font=f_timer_label, fill=MUTED)
        f_timer = font(110, bold=True, mono=True)
        timer_text = f"{seconds_remaining:02d}s" if seconds_remaining >= 0 else "00s"
        d.text((card_x + pad, card_y + 190), timer_text, font=f_timer, fill=ACCENT)

    # reveal value (big)
    if reveal_value is not None:
        d.text((card_x + pad, card_y + 160), "Cleartext amount",
               font=f_timer_label, fill=MUTED)
        f_huge = font(220, bold=True, mono=True)
        text = str(reveal_value)
        d.text((card_x + pad, card_y + 200), text, font=f_huge, fill=ACCENT)
        # subtitle
        f_sub2 = font(22)
        d.text((card_x + pad, card_y + 460),
               "decrypted via KMS · signature verified · proof consumed",
               font=f_sub2, fill=MUTED)

    # handles block (during fulfillReveal animation)
    if show_handles:
        hy = card_y + 380
        f_mono_lbl = font(20, mono=True)
        f_mono = font(18, mono=True)
        d.text((card_x + pad, hy), "// handles[] — abi.decode tuple order",
               font=f_mono_lbl, fill=MUTED)
        d.text((card_x + pad, hy + 30),
               "handles[0] = FHE.toBytes32(v.amount);",
               font=f_mono, fill=FG)
        d.text((card_x + pad, hy + 56),
               "handles[1] = FHE.toBytes32(v.secret);",
               font=f_mono, fill=FG)
        d.text((card_x + pad, hy + 100),
               "FHE.checkSignatures(handles, cleartexts, proof);",
               font=f_mono, fill=ACCENT)

    # pipeline status (bottom)
    if pipeline_step:
        steps = [
            ("AP-001  sig verified",  pipeline_step in {"sig", "replay", "value", "done"}),
            ("AP-002  replay consumed", pipeline_step in {"replay", "value", "done"}),
            ("cleartext written",       pipeline_step in {"value", "done"}),
        ]
        sy = card_y + card_h - 130
        f_step = font(20, bold=True)
        for i, (label, active) in enumerate(steps):
            col = OK if active else (60, 65, 75)
            dot_color = OK if active else (60, 65, 75)
            d.ellipse([card_x + pad, sy + 4, card_x + pad + 18, sy + 22],
                      fill=dot_color)
            mark = "√" if active else "·"
            f_mark = font(18, bold=True)
            d.text((card_x + pad + 3, sy - 1), mark, font=f_mark, fill=BG)
            d.text((card_x + pad + 36, sy), label, font=f_step,
                   fill=OK if active else MUTED)
            sy += 36

    # trigger reveal button (when idle, time=0)
    if seconds_remaining == 0 and pipeline_step == "":
        btn_y = card_y + card_h - 100
        d.rounded_rectangle(
            [card_x + 50, btn_y, card_x + card_w - 50, btn_y + 60],
            radius=10, fill=ACCENT,
        )
        f_btn = font(28, bold=True)
        btn_label = "Trigger reveal  →  fulfillReveal()"
        bw, _ = measure(d, btn_label, f_btn)
        d.text((card_x + (card_w - bw) // 2, btn_y + 14),
               btn_label, font=f_btn, fill=BG)


# ============================================================================
# Shot definitions
# ============================================================================

def make_shot_5a(name: str, **kwargs):
    """5a shots — lock flow, frontend form view."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_topnav(d)
    draw_status_strip(d, kwargs.get("top", ""),
                      accent_color=kwargs.get("top_color", ACCENT))
    draw_lock_form(
        d,
        amount=kwargs.get("amount", ""),
        secret=kwargs.get("secret", ""),
        seconds=kwargs.get("seconds", ""),
        status=kwargs.get("status", ""),
        status_color=kwargs.get("status_color", ACCENT),
        button_label=kwargs.get("button_label", "Lock encrypted value"),
        button_state=kwargs.get("button_state", "idle"),
        tx_hash=kwargs.get("tx_hash", ""),
    )
    draw_bottom_caption(d, kwargs.get("bottom", ""))
    return img


def make_shot_5b(name: str, **kwargs):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_topnav(d)
    draw_status_strip(d, kwargs.get("top", ""),
                      accent_color=kwargs.get("top_color", ACCENT))
    draw_vault_card(
        d,
        vault_id=kwargs.get("vault_id", 5),
        seconds_remaining=kwargs.get("seconds_remaining"),
        state_label=kwargs.get("state_label", ""),
        state_color=kwargs.get("state_color", ACCENT),
        reveal_value=kwargs.get("reveal_value"),
        show_handles=kwargs.get("show_handles", False),
        pipeline_step=kwargs.get("pipeline_step", ""),
    )
    draw_bottom_caption(d, kwargs.get("bottom", ""))
    return img


SHOTS_5A = [
    dict(
        name="shotA-hero",
        seconds=3,
        top="Live on Sepolia  ·  AsyncRevealVault",
        bottom="0x256e8948057982D483C60F7c060E3253a4d6A49b",
    ),
    dict(
        name="shotB-typed-63",
        seconds=3,
        amount="63", secret="123456789", seconds_field="60",
        top="Encrypting cleartext  →  euint64 + euint256",
        bottom="63 stays secret  ·  only the encrypted handle goes on-chain",
    ),
    dict(
        name="shotC-encrypting",
        seconds=3,
        amount="63", secret="123456789", seconds_field="60",
        status="Encrypting via FHEVM SDK …",
        button_state="busy",
        top="Client-side encryption  ·  no plaintext leaves the browser",
        bottom="amount + secret  →  euint64 + euint256 ciphertexts",
    ),
    dict(
        name="shotD-signing",
        seconds=3,
        amount="63", secret="123456789", seconds_field="60",
        status="Awaiting wallet signature …",
        button_state="busy",
        top="Lock  ·  Sign  ·  submit lock(ciphertexts, 60)",
        bottom="60-second timer starts when the tx is mined",
    ),
    dict(
        name="shotE-pending",
        seconds=3,
        amount="63", secret="123456789", seconds_field="60",
        status="Tx pending in Sepolia mempool …",
        button_state="busy",
        tx_hash="0xbb66e334506b7f7dcfe68b3f33e30d76f5d778396556553ea0df042091209c70",
        top="One confirmation  ·  ~12 sec block time",
        bottom="vault id assigned on mine — countdown starts",
    ),
    dict(
        name="shotF-locked",
        seconds=5,
        amount="63", secret="123456789", seconds_field="60",
        status="Locked  ·  Vault #5  ·  unlocks in 60s",
        status_color=OK,
        button_state="busy",
        button_label="Vault locked",
        tx_hash="0xbb66e334506b7f7dcfe68b3f33e30d76f5d778396556553ea0df042091209c70",
        top="Done  ·  cleartext never left the browser",
        bottom="next: wait 60s, then trigger reveal",
    ),
]


SHOTS_5B = [
    dict(
        name="shotA-timer-zero",
        seconds=3,
        seconds_remaining=0,
        state_label="UNLOCKED",
        state_color=OK,
        top="60 seconds pass  ·  revealAt reached",
        bottom="Vault #5  ·  triggerReveal() now valid",
    ),
    dict(
        name="shotB-trigger",
        seconds=3,
        seconds_remaining=0,
        state_label="UNLOCKED",
        state_color=OK,
        top="triggerReveal()  ·  AP-009 idempotent",
        bottom="flags both ciphertexts for KMS public-decryption",
    ),
    dict(
        name="shotC-fulfill-called",
        seconds=3,
        state_label="FULFILLING",
        show_handles=True,
        top="fulfillReveal(vaultId, cleartexts, proof)",
        bottom="anyone can submit — only with a real KMS proof",
    ),
    dict(
        name="shotD-pipeline-sig",
        seconds=3,
        state_label="FULFILLING",
        pipeline_step="sig",
        top="AP-001  ·  FHE.checkSignatures runs FIRST",
        bottom="without it, anyone could submit fake cleartext",
    ),
    dict(
        name="shotE-pipeline-replay",
        seconds=3,
        state_label="FULFILLING",
        pipeline_step="replay",
        top="AP-002  ·  v.revealed = true  BEFORE the value",
        bottom="same proof cannot run twice",
    ),
    dict(
        name="shotF-pipeline-value",
        seconds=3,
        state_label="FULFILLING",
        pipeline_step="value",
        top="cleartext amount + secret written",
        bottom="abi.decode tuple order matches handles[] — AP-003",
    ),
    dict(
        name="shotG-reveal-63",
        seconds=7,
        state_label="REVEALED",
        state_color=OK,
        reveal_value=63,
        pipeline_step="done",
        top="63  ·  the number stayed secret until the timer",
        bottom="canonical async-decryption pattern  ·  from SKILL.md",
    ),
]


def render_clip(out_name: str, shots: list[dict], maker):
    print(f"\nRendering {out_name}…")
    shot_mp4s: list[Path] = []
    for shot in shots:
        png_path = TMP_DIR / f"{out_name}_{shot['name']}.png"
        # remap "seconds_field" key for 5a (keyword conflict with frame duration)
        kwargs = dict(shot)
        sec = kwargs.pop("seconds")
        name = kwargs.pop("name")
        if "seconds_field" in kwargs:
            kwargs["seconds"] = kwargs.pop("seconds_field")
        img = maker(name, **kwargs)
        img.save(png_path)

        shot_mp4 = TMP_DIR / f"{out_name}_{shot['name']}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(png_path),
            "-t", str(sec),
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
        print(f"  shot {shot['name']:25s} -> {shot_mp4.name}  ({sec}s)")
        shot_mp4s.append(shot_mp4)

    concat_file = TMP_DIR / f"{out_name}_concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in shot_mp4s),
        encoding="utf-8",
    )

    out_mp4 = OUT_DIR / f"{out_name}.mp4"
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
    render_clip("clip5a-lock-static", SHOTS_5A, make_shot_5a)
    render_clip("clip5b-reveal-static", SHOTS_5B, make_shot_5b)
    print("\nDone. Drop both into CapCut (5a then 5b, with a tiny crossfade between).")

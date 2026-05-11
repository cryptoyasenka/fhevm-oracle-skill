"""
Render clip5a (LOCK, 20s) and clip5b (REVEAL, 25s) using REAL app screenshots
from https://fhevm-oracle-frontend.vercel.app as backgrounds, with PIL overlays
for state-change animations.

v1 clips (clip5a-demo-static.mp4 / clip5b-reveal-static.mp4) stay untouched.

Run:    python scripts/gen_clip5_v2.py
Output: video-clips/clip5a-demo-v2.mp4
        video-clips/clip5b-reveal-v2.mp4
"""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SCREENS = ROOT / "app-screenshots"
OUT_DIR = ROOT / "video-clips"
TMP_DIR_A = ROOT / "video-clips" / "_tmp_clip5a_v2"
TMP_DIR_B = ROOT / "video-clips" / "_tmp_clip5b_v2"
OUT_DIR.mkdir(exist_ok=True)
TMP_DIR_A.mkdir(exist_ok=True)
TMP_DIR_B.mkdir(exist_ok=True)

W, H = 1920, 1080

# Frontend palette (frontend/app/globals.css)
BG          = (11, 13, 18)
BG_ELEV     = (17, 20, 27)
ACCENT      = (255, 214, 51)
OK          = (94, 210, 138)
MUTED       = (138, 147, 166)
FG          = (232, 232, 235)
DANGER      = (255, 107, 107)


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    names = (
        ["consolab.ttf"] if mono and bold else
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


def load_bg(name: str) -> Image.Image:
    img = Image.open(SCREENS / name).convert("RGB")
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    return img


def dim_bg(img: Image.Image, alpha: float = 0.45) -> Image.Image:
    """Darken background so overlays stand out."""
    overlay = Image.new("RGB", (W, H), BG)
    return Image.blend(img, overlay, alpha)


def rounded_rect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def overlay_card(
    bg: Image.Image,
    *,
    title: str,
    subtitle: str = "",
    body_lines: tuple = (),
    accent_text: str = "",
    pulse: bool = False,
    success: bool = False,
    width: int = 1200,
    height: int = 400,
) -> Image.Image:
    """Center a state-change card on the dimmed background."""
    img = dim_bg(bg, 0.55).copy()
    d = ImageDraw.Draw(img, "RGBA")
    x0 = (W - width) // 2
    y0 = (H - height) // 2
    x1, y1 = x0 + width, y0 + height

    # Card shadow (cheap glow)
    glow_color = (*OK, 60) if success else (*ACCENT, 60)
    for i in range(8, 0, -2):
        rounded_rect(d, (x0 - i, y0 - i, x1 + i, y1 + i),
                     radius=24, outline=glow_color, width=2)

    rounded_rect(d, (x0, y0, x1, y1), radius=24,
                 fill=BG_ELEV, outline=(60, 60, 70), width=2)

    # Left accent stripe
    stripe_color = OK if success else ACCENT
    rounded_rect(d, (x0, y0, x0 + 8, y1), radius=4, fill=stripe_color)

    cx = x0 + 50
    cy = y0 + 40

    f_title = font(50, bold=True)
    f_sub = font(28)
    f_body = font(26, mono=True)
    f_accent = font(72, bold=True)

    d.text((cx, cy), title, font=f_title, fill=FG)
    cy += 65

    if subtitle:
        d.text((cx, cy), subtitle, font=f_sub, fill=MUTED)
        cy += 50

    for line in body_lines:
        d.text((cx, cy), line, font=f_body, fill=stripe_color if pulse else FG)
        cy += 38

    if accent_text:
        tw, th = measure(d, accent_text, f_accent)
        d.text((x1 - tw - 50, y1 - th - 30), accent_text,
               font=f_accent, fill=stripe_color)

    return img


def overlay_form_panel(
    bg: Image.Image,
    *,
    amount: str = "",
    secret: str = "",
    seconds: str = "",
    highlight_field: str = "",
    button_text: str = "Connect wallet",
    button_state: str = "primary",  # primary | pending | success
) -> Image.Image:
    """Synthetic Lock-form overlay matching real frontend palette."""
    img = dim_bg(bg, 0.55).copy()
    d = ImageDraw.Draw(img, "RGBA")

    panel_w, panel_h = 1100, 720
    x0 = (W - panel_w) // 2
    y0 = (H - panel_h) // 2
    x1, y1 = x0 + panel_w, y0 + panel_h
    rounded_rect(d, (x0, y0, x1, y1), radius=24,
                 fill=BG_ELEV, outline=(60, 60, 70), width=2)

    f_title = font(40, bold=True)
    f_label = font(24)
    f_value = font(40, mono=True)
    d.text((x0 + 50, y0 + 30), "Lock a vault", font=f_title, fill=FG)
    d.text((x0 + 50, y0 + 80), "Sealed-bid auction · Sepolia", font=f_label, fill=MUTED)

    # Three form fields
    fields = [
        ("amount (uint64)", amount, "amount"),
        ("secret (32 bytes max)", secret, "secret"),
        ("reveal in (seconds)", seconds, "seconds"),
    ]
    fy = y0 + 150
    for label, value, key in fields:
        d.text((x0 + 50, fy), label, font=f_label, fill=MUTED)
        bx0 = x0 + 50
        by0 = fy + 38
        bx1 = x1 - 50
        by1 = by0 + 78
        is_active = (key == highlight_field)
        border = ACCENT if is_active else (60, 60, 70)
        rounded_rect(d, (bx0, by0, bx1, by1), radius=12,
                     fill=(20, 23, 30), outline=border, width=3 if is_active else 1)
        d.text((bx0 + 24, by0 + 18), value or "", font=f_value, fill=FG)
        fy = by1 + 28

    # CTA button
    by0 = y1 - 110
    by1 = y1 - 30
    bx0 = x0 + 50
    bx1 = x1 - 50
    if button_state == "primary":
        rounded_rect(d, (bx0, by0, bx1, by1), radius=14, fill=ACCENT)
        tx_color = (20, 20, 20)
    elif button_state == "pending":
        rounded_rect(d, (bx0, by0, bx1, by1), radius=14,
                     fill=(60, 56, 24), outline=ACCENT, width=2)
        tx_color = ACCENT
    else:  # success
        rounded_rect(d, (bx0, by0, bx1, by1), radius=14, fill=OK)
        tx_color = (20, 20, 20)
    f_btn = font(32, bold=True, mono=True)
    tw, th = measure(d, button_text, f_btn)
    d.text(((bx0 + bx1 - tw) // 2, (by0 + by1 - th) // 2 - 4),
           button_text, font=f_btn, fill=tx_color)

    return img


# =============================================================================
# clip5a — LOCK (20s)
# =============================================================================

def render_5a():
    bg_hero = load_bg("state-1-hero.png")
    bg_try = load_bg("state-3-try-it.png")

    shots = []

    # Shot 1 (3s): hero with caption "Live on Sepolia — open the app"
    img1 = bg_hero.copy()
    d = ImageDraw.Draw(img1, "RGBA")
    rounded_rect(d, (40, H - 130, 1100, H - 40), radius=18,
                 fill=(*BG_ELEV, 230), outline=ACCENT, width=2)
    f1 = font(40, bold=True)
    f2 = font(24)
    d.text((70, H - 115), "Live on Sepolia testnet", font=f1, fill=ACCENT)
    d.text((70, H - 65), "fhevm-oracle-frontend.vercel.app", font=f2, fill=FG)
    shots.append(("01-hero", img1, 3))

    # Shot 2 (3s): try-it real screenshot, role-play card highlighted by border
    img2 = bg_try.copy()
    d = ImageDraw.Draw(img2, "RGBA")
    rounded_rect(d, (40, H - 130, 1300, H - 40), radius=18,
                 fill=(*BG_ELEV, 230), outline=ACCENT, width=2)
    d.text((70, H - 115), "Try it — sealed-bid auction role-play",
           font=f1, fill=ACCENT)
    d.text((70, H - 65), "Set bid, secret, timer — encrypt in browser",
           font=f2, fill=FG)
    shots.append(("02-tryit", img2, 3))

    # Shot 3 (4s): form filled with 63 / 123456789 / 60
    img3 = overlay_form_panel(
        bg_try,
        amount="63", secret="123456789", seconds="60",
        highlight_field="amount",
        button_text="Encrypt + Lock on Sepolia",
        button_state="primary",
    )
    shots.append(("03-form-filled", img3, 4))

    # Shot 4 (3s): encrypting state
    img4 = overlay_card(
        bg_try,
        title="Encrypting in your browser",
        subtitle="Zama relayer SDK · TFHE WASM engine",
        body_lines=(
            "amount → euint64 ciphertext",
            "secret → bytes32 ciphertext",
            "binding input proof to wallet...",
        ),
        pulse=True,
    )
    shots.append(("04-encrypting", img4, 3))

    # Shot 5 (3s): awaiting signature
    img5 = overlay_card(
        bg_try,
        title="Awaiting wallet signature",
        subtitle="MetaMask · Sepolia · gas ~180k",
        body_lines=(
            "lock(externalEuint64 a, bytes proofA,",
            "     externalEuint64 s, bytes proofS,",
            "     uint64 revealAt = block.timestamp + 60)",
        ),
        pulse=True,
    )
    shots.append(("05-signing", img5, 3))

    # Shot 6 (4s): locked success
    img6 = overlay_card(
        bg_try,
        title="Vault #5 locked",
        subtitle="0xbb66...e0a4 · Etherscan",
        body_lines=(
            "revealAt = block.timestamp + 60s",
            "amount + secret = ciphertext on-chain",
            "contract itself can't read them",
        ),
        accent_text="LOCKED",
        success=True,
    )
    shots.append(("06-locked", img6, 4))

    render_clip(shots, TMP_DIR_A, OUT_DIR / "clip5a-demo-v2.mp4")


# =============================================================================
# clip5b — REVEAL (25s)
# =============================================================================

def render_5b():
    bg_try = load_bg("state-3-try-it.png")
    bg_how = load_bg("state-2-how-it-works.png")
    bg_bottom = load_bg("state-4-vaults-activity.png")

    shots = []

    # Shot 1 (3s): countdown 00:00
    img1 = overlay_card(
        bg_how,
        title="Timer expired",
        subtitle="block.timestamp > revealAt",
        body_lines=("60s elapsed · ready to trigger",),
        accent_text="00:00",
        pulse=True,
    )
    shots.append(("01-timer", img1, 3))

    # Shot 2 (4s): trigger reveal click
    img2 = overlay_card(
        bg_how,
        title="Trigger reveal",
        subtitle="anyone can call triggerReveal(id)",
        body_lines=(
            "FHE.requestDecryption(handles, callback)",
            "queues async decryption with KMS network",
        ),
        pulse=True,
    )
    shots.append(("02-trigger", img2, 4))

    # Shot 3 (5s): handles + checkSignatures
    img3 = overlay_card(
        bg_how,
        title="fulfillReveal callback",
        subtitle="KMS-signed cleartext arrives",
        body_lines=(
            "bytes32[] handles = [amountHandle, secretHandle];",
            "FHE.checkSignatures(handles, cleartext, proof);",
            "// AP-001: signatures BEFORE state",
        ),
        pulse=True,
    )
    shots.append(("03-handles", img3, 5))

    # Shot 4 (3s): AP-001 pass
    img4 = overlay_card(
        bg_how,
        title="AP-001  signatures verified",
        subtitle="threshold sigs from KMS validators",
        body_lines=(
            "no forged callback can reach state",
            "any non-quorum proof reverts here",
        ),
        accent_text="OK",
        success=True,
    )
    shots.append(("04-ap001", img4, 3))

    # Shot 5 (3s): AP-002 pass
    img5 = overlay_card(
        bg_how,
        title="AP-002  replay flag set BEFORE value",
        subtitle="v.revealed = true; v.amountClear = a;",
        body_lines=(
            "same proof can never run twice",
            "ordering matters: flag, then write",
        ),
        accent_text="OK",
        success=True,
    )
    shots.append(("05-ap002", img5, 3))

    # Shot 6 (4s): cleartext "63" reveal — big number
    img6 = bg_bottom.copy()
    img6 = dim_bg(img6, 0.7).copy()
    d = ImageDraw.Draw(img6, "RGBA")
    # Glow
    for i in range(20, 0, -2):
        rounded_rect(d, ((W // 2) - 250 - i, (H // 2) - 200 - i,
                         (W // 2) + 250 + i, (H // 2) + 200 + i),
                     radius=40, outline=(*ACCENT, 30), width=2)
    rounded_rect(d, ((W // 2) - 250, (H // 2) - 200,
                     (W // 2) + 250, (H // 2) + 200),
                 radius=40, fill=BG_ELEV, outline=ACCENT, width=3)
    f_big = font(220, bold=True, mono=True)
    f_caption = font(36)
    tw, th = measure(d, "63", f_big)
    d.text(((W - tw) // 2, (H // 2) - th // 2 - 30), "63", font=f_big, fill=ACCENT)
    cap = "cleartext amount  ·  on-chain"
    cw, _ = measure(d, cap, f_caption)
    d.text(((W - cw) // 2, (H // 2) + 110), cap, font=f_caption, fill=FG)
    shots.append(("06-cleartext-63", img6, 4))

    # Shot 7 (3s): stayed secret until the timer
    img7 = overlay_card(
        bg_bottom,
        title="Stayed secret until the timer",
        subtitle="bid, secret, timer · no off-chain trust",
        body_lines=(
            "vault.amountClear = 63",
            "vault.secretClear = 0x075bcd15...",
            "Activity log · Etherscan · all public now",
        ),
        success=True,
    )
    shots.append(("07-final", img7, 3))

    render_clip(shots, TMP_DIR_B, OUT_DIR / "clip5b-reveal-v2.mp4")


# =============================================================================
# Common render pipeline
# =============================================================================

def render_clip(shots, tmp_dir: Path, out_mp4: Path):
    shot_mp4s = []
    for name, img, seconds in shots:
        png = tmp_dir / f"{name}.png"
        img.save(png)
        mp4 = tmp_dir / f"{name}.mp4"
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(png),
            "-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-r", "30", "-vf", f"scale={W}:{H}", "-preset", "fast", "-crf", "20",
            str(mp4),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr); raise SystemExit(r.returncode)
        print(f"  {name:25s} -> {mp4.name} ({seconds}s)")
        shot_mp4s.append(mp4)

    concat = tmp_dir / "concat.txt"
    concat.write_text("\n".join(f"file '{p.as_posix()}'" for p in shot_mp4s),
                      encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
           "-i", str(concat), "-c", "copy", str(out_mp4)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr); raise SystemExit(r.returncode)
    print(f"  wrote {out_mp4.relative_to(ROOT)}\n")


if __name__ == "__main__":
    print("Rendering clip5a (LOCK) v2 ...")
    render_5a()
    print("Rendering clip5b (REVEAL) v2 ...")
    render_5b()
    print("Done.")

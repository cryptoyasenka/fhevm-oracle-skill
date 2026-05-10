"""
Render static-image MP4 clips for non-live segments of the demo video.

These are placeholders for the visual track only — Yana records her voice
separately in CapCut and lays it on top.

Segment 1 (hook),  22 sec, slides/01-title.png        -> clip1-hook-static.mp4
Segment 2 (problem option A), 35 sec, slides/02-anti-patterns.png -> clip2-problem-static.mp4
Segment 6 (outro), 18 sec, slides/06-outro.png        -> clip6-outro-static.mp4

Run:    python scripts/gen_static_clips.py
Output: video-clips/*.mp4 (1920x1080, H.264, 30 fps, silent)
"""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "slides"
OUT = ROOT / "video-clips"
OUT.mkdir(exist_ok=True)

CLIPS = [
    ("01-title.png",        "clip1-hook-static.mp4",     22),
    ("02-anti-patterns.png", "clip2-problem-static.mp4", 35),
    ("06-outro.png",        "clip6-outro-static.mp4",    18),
]


def render(src: Path, dst: Path, seconds: int):
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", str(src),
        "-t", str(seconds),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-vf", "scale=1920:1080",
        "-preset", "fast",
        "-crf", "20",
        "-y",
        str(dst),
    ]
    print(f"  rendering {dst.name} ({seconds}s)…")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg stderr:\n{result.stderr}")
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    print(f"Rendering static clips → {OUT}")
    for src_name, dst_name, secs in CLIPS:
        src = SLIDES / src_name
        if not src.exists():
            print(f"  SKIP {src_name} — not found")
            continue
        dst = OUT / dst_name
        render(src, dst, secs)
    print("Done. Drop these MP4s into CapCut as the visual track.")

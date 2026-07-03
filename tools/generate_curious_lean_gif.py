#!/usr/bin/env python3
"""Generate animated GIF preview from cleaned curious_lean 28-frame sequence."""

import os
from PIL import Image

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1")
OUTPUT_PATH = os.path.join(PROJECT, "assets", "characters", "cat", "production", "gif_previews", "curious_lean_candidate_v1.gif")

# FPS from art_preview.cfg
FPS = 4.0
FRAME_DURATION_MS = int(1000 / FPS)


def main():
    frames = []
    for i in range(1, 29):
        path = os.path.join(FRAMES_DIR, f"frame_{i:02d}.png")
        if not os.path.exists(path):
            print(f"Missing frame: {path}")
            continue
        img = Image.open(path).convert('RGBA')
        # Composite onto a neutral background for GIF (GIF doesn't support alpha)
        bg = Image.new('RGBA', img.size, (50, 50, 50, 255))
        bg.paste(img, (0, 0), img)
        frames.append(bg.convert('RGB'))
        print(f"  Loaded frame_{i:02d}.png ({img.width}x{img.height})")

    if not frames:
        print("No frames found!")
        return

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
    )
    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"\nGIF saved: {OUTPUT_PATH}")
    print(f"  {len(frames)} frames, {FPS} fps, {size_kb:.0f} KB")


if __name__ == "__main__":
    main()

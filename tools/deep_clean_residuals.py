#!/usr/bin/env python3
"""
Deep clean residual artifacts from curious_lean frames - v2.

Strategy:
1. Connected-component analysis to remove small disconnected fragments
2. Column-density scan to detect and remove thin vertical strips on left edge
   that are separate from the main cat body density peak
"""

import os
import sys
from PIL import Image, ImageDraw
from collections import deque

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1_base_raw")
CLEAN_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1_base")
OUTPUT_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1")
CONTACT_DIR = os.path.join(PROJECT, "outputs", "art_preview_debug", "curious_lean_cleanup")
GIF_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "gif_previews")

ALPHA_THRESHOLD = 10
TRIM_MARGIN = 8
PADDING = 24
DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]


def find_connected_components(img):
    """Find all connected components of non-transparent pixels."""
    pixels = img.load()
    w, h = img.size
    visited = set()
    components = []
    
    for y in range(h):
        for x in range(w):
            if (x, y) in visited or pixels[x, y][3] <= ALPHA_THRESHOLD:
                continue
            
            component = set()
            queue = deque([(x, y)])
            visited.add((x, y))
            x_min, y_min, x_max, y_max = x, y, x, y
            
            while queue:
                cx, cy = queue.popleft()
                component.add((cx, cy))
                x_min, y_min = min(x_min, cx), min(y_min, cy)
                x_max, y_max = max(x_max, cx), max(y_max, cy)
                
                for dx, dy in DIRS:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited and pixels[nx, ny][3] > ALPHA_THRESHOLD:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            
            components.append((component, (x_min, y_min, x_max, y_max), len(component)))
    
    components.sort(key=lambda c: c[2], reverse=True)
    return components


def remove_small_components(img, min_area_ratio=0.01):
    """Remove connected components that are too small relative to the largest."""
    components = find_connected_components(img)
    if not components:
        return img, 0
    
    largest_area = components[0][2]
    threshold = largest_area * min_area_ratio
    pixels = img.load()
    removed = 0
    
    for comp_pixels, bbox, area in components:
        if area < threshold:
            for x, y in comp_pixels:
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
            removed += 1
    
    return img, removed


def remove_left_edge_strip(img, strip_max_width=50):
    """Detect and remove a thin vertical strip on the left edge.
    
    Strategy: Scan columns from left to right. Find where the main cat body
    density peaks. Remove everything before that point if it's a thin strip.
    """
    pixels = img.load()
    w, h = img.size
    
    # Get per-column pixel density
    col_density = []
    for x in range(w):
        count = sum(1 for y in range(h) if pixels[x, y][3] > ALPHA_THRESHOLD)
        col_density.append(count)
    
    # Find the first column with significant content
    first_content = 0
    for x in range(w):
        if col_density[x] > 15:
            first_content = x
            break
    else:
        return 0
    
    # Find the main body density peak (highest density column in the image)
    max_density = max(col_density)
    peak_threshold = max_density * 0.3  # Main body has at least 30% of peak density
    
    # Find where the main body starts (first column reaching peak_threshold
    # after the initial content)
    main_body_start = first_content
    for x in range(first_content, w):
        if col_density[x] >= peak_threshold:
            main_body_start = x
            break
    
    # If the strip between first_content and main_body_start is thin enough,
    # it's a residual strip
    strip_width = main_body_start - first_content
    
    if 0 < strip_width <= strip_max_width:
        # Check if there's a density dip between the strip and main body
        strip_region = col_density[first_content:main_body_start]
        post_region = col_density[main_body_start:min(main_body_start + 20, w)]
        
        if strip_region and post_region:
            strip_avg = sum(strip_region) / len(strip_region)
            post_avg = sum(post_region) / len(post_region) if post_region else 0
            
            # The strip should have lower density than the main body
            if post_avg > strip_avg * 1.5 or strip_avg < 30:
                # Remove the strip by zeroing alpha
                for x in range(first_content, main_body_start):
                    for y in range(h):
                        r, g, b, a = pixels[x, y]
                        if a > ALPHA_THRESHOLD:
                            pixels[x, y] = (r, g, b, 0)
                return strip_width
    
    return 0


def find_main_body_bbox(img):
    """Find bounding box of the largest connected component."""
    components = find_connected_components(img)
    if not components:
        return None
    return components[0][1]


def clean_frame(img, frame_num):
    """Full cleanup pipeline for a single frame."""
    img = img.copy()
    
    # Step 1: Remove small disconnected components
    img, removed_cc = remove_small_components(img, min_area_ratio=0.01)
    if removed_cc > 0:
        print(f"  Frame {frame_num}: Removed {removed_cc} small component(s)")
    
    # Step 2: Remove left-edge vertical strip residual
    strip_w = remove_left_edge_strip(img, strip_max_width=50)
    if strip_w > 0:
        print(f"  Frame {frame_num}: Removed {strip_w}px left-edge strip")
    
    # Step 3: Find main body bbox
    bbox = find_main_body_bbox(img)
    if bbox is None:
        print(f"  Frame {frame_num}: WARNING - no content!")
        return img
    
    x_min, y_min, x_max, y_max = bbox
    w, h = img.size
    x_min = min(x_min + TRIM_MARGIN, w - 1)
    y_min = min(y_min + TRIM_MARGIN, h - 1)
    x_max = max(x_max - TRIM_MARGIN, 0)
    y_max = max(y_max - TRIM_MARGIN, 0)
    
    cropped = img.crop((x_min, y_min, x_max + 1, y_max + 1))
    print(f"  Frame {frame_num}: content={cropped.width}x{cropped.height}")
    return cropped


def normalize_frame_sizes(frames):
    """Normalize all frames to the same canvas size, centering content."""
    if not frames:
        return frames
    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    final_w = max_w + 2 * PADDING
    final_h = max_h + 2 * PADDING
    print(f"\nNormalizing to {final_w}x{final_h}")
    
    normalized = []
    for frame in frames:
        canvas = Image.new('RGBA', (final_w, final_h), (0, 0, 0, 0))
        paste_x = (final_w - frame.width) // 2
        paste_y = (final_h - frame.height) // 2
        canvas.paste(frame, (paste_x, paste_y), frame)
        normalized.append(canvas)
    return normalized


def generate_rhythm_sequence(base_frames, output_dir):
    """Generate 28-frame sequence from 6 base poses."""
    rhythm = [
        2, 2, 2, 3, 3, 3, 3,
        3, 2, 1, 1, 1,
        1, 1, 1, 1,
        1, 6, 5, 5, 5, 5,
        5, 6, 1, 1, 1,
        1,
    ]
    assert len(rhythm) == 28
    os.makedirs(output_dir, exist_ok=True)
    for i, base_idx in enumerate(rhythm):
        frame = base_frames[base_idx - 1]
        frame.save(os.path.join(output_dir, f"frame_{i+1:02d}.png"))
    print(f"  Generated 28 frames")


def create_gif(frames, output_path, fps=4.0):
    """Create animated GIF from frames."""
    duration_ms = int(1000 / fps)
    rgb_frames = []
    for f in frames:
        bg = Image.new('RGBA', f.size, (50, 50, 50, 255))
        bg.paste(f, (0, 0), f)
        rgb_frames.append(bg.convert('RGB'))
    rgb_frames[0].save(
        output_path, save_all=True, append_images=rgb_frames[1:],
        duration=duration_ms, loop=0, optimize=True,
    )
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  GIF: {len(rgb_frames)} frames, {fps} fps, {size_kb:.0f} KB")


def create_contact_sheet(frames, output_path, label=""):
    """Create a contact sheet showing all frames in a grid."""
    if not frames:
        return
    cols = 7
    rows = (len(frames) + cols - 1) // cols
    thumb_w = frames[0].width
    thumb_h = frames[0].height
    max_thumb = 200
    if thumb_w > max_thumb or thumb_h > max_thumb:
        scale = max_thumb / max(thumb_w, thumb_h)
        thumb_w = int(thumb_w * scale)
        thumb_h = int(thumb_h * scale)
    margin = 4
    sheet_w = cols * (thumb_w + margin) + margin
    sheet_h = rows * (thumb_h + margin) + margin + 30
    sheet = Image.new('RGBA', (sheet_w, sheet_h), (30, 30, 30, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, margin // 2), f"{label} ({len(frames)} frames)", fill=(200, 200, 200))
    y_offset = 30
    for i, frame in enumerate(frames):
        row, col = i // cols, i % cols
        thumb = frame.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
        x = margin + col * (thumb_w + margin)
        y = y_offset + row * (thumb_h + margin)
        draw.rectangle([x-1, y-1, x+thumb_w+1, y+thumb_h+1], outline=(80, 80, 80))
        sheet.paste(thumb, (x, y), thumb)
        draw.text((x, y + thumb_h + 1), f"#{i+1}", fill=(150, 150, 150))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sheet.save(output_path)
    print(f"  Contact sheet: {output_path}")


def main():
    print("=" * 60)
    print("Deep Clean Residuals v2 - Column Density + Connected Components")
    print("=" * 60)
    
    print("\n[1/6] Loading raw frames...")
    raw_frames = []
    for i in range(1, 7):
        path = os.path.join(RAW_DIR, f"frame_{i:02d}.png")
        img = Image.open(path).convert('RGBA')
        raw_frames.append(img)
        print(f"  Loaded frame_{i:02d}.png ({img.width}x{img.height})")
    
    print("\n[2/6] Before contact sheet...")
    create_contact_sheet(raw_frames,
                        os.path.join(CONTACT_DIR, "v4_before_contact.png"),
                        "Before (raw)")
    
    print("\n[3/6] Deep cleaning frames...")
    cleaned = []
    for i, frame in enumerate(raw_frames):
        print(f"\n  Processing frame_{i+1:02d}.png:")
        c = clean_frame(frame, i + 1)
        cleaned.append(c)
    
    print("\n[4/6] Normalizing frame sizes...")
    normalized = normalize_frame_sizes(cleaned)
    
    print("\n  Saving cleaned base frames...")
    os.makedirs(CLEAN_DIR, exist_ok=True)
    for i, frame in enumerate(normalized):
        frame.save(os.path.join(CLEAN_DIR, f"frame_{i+1:02d}.png"))
    
    print("\n  After contact sheet...")
    create_contact_sheet(normalized,
                        os.path.join(CONTACT_DIR, "v4_after_contact.png"),
                        "After (deep cleaned v2)")
    
    print("\n[5/6] Generating 28-frame sequence...")
    generate_rhythm_sequence(normalized, OUTPUT_DIR)
    
    print("\n[6/6] Generating animated GIF...")
    gif_frames = []
    for i in range(1, 29):
        gif_frames.append(Image.open(os.path.join(OUTPUT_DIR, f"frame_{i:02d}.png")).convert('RGBA'))
    create_gif(gif_frames, os.path.join(GIF_DIR, "curious_lean_candidate_v1.gif"))
    
    print("\n" + "=" * 60)
    print("DONE!")
    print(f"  Base frames: {CLEAN_DIR}")
    print(f"  28-frame sequence: {OUTPUT_DIR}")
    print(f"  GIF preview: {GIF_DIR}/curious_lean_candidate_v1.gif")
    print(f"  Contact sheets: {CONTACT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

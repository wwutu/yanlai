#!/usr/bin/env python3
"""
Extract curious_lean frames from raw base using connected-region detection.

Problem: The original 6 raw frames were cut from a sprite sheet using equal-width
columns, causing:
  1. Left-edge residual contamination (neighboring pose sliver)
  2. Right side of cat body slightly cropped/narrowed

Approach:
  1. For each raw frame, detect the cat's bounding box via connected non-transparent pixels
  2. Apply safety margins to avoid edge contamination
  3. Crop to the cat silhouette, then pad to a uniform canvas size
  4. Output clean, properly-framed base frames and regenerate 28-frame sequence
"""

import os
import sys
from PIL import Image, ImageDraw

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1_base_raw")
CLEAN_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1_base")
OUTPUT_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1")
CONTACT_DIR = os.path.join(PROJECT, "outputs", "art_preview_debug", "curious_lean_cleanup")

# Margin (pixels) to trim from each side after bounding-box detection.
# This helps exclude residual contamination at frame edges.
TRIM_MARGIN = 8

# Extra padding around the detected bounding box for the final canvas.
PADDING = 24

# Threshold for "non-transparent" pixel detection
ALPHA_THRESHOLD = 10


def find_content_bbox(img, threshold=ALPHA_THRESHOLD):
    """Find the bounding box of non-transparent content in a RGBA image.
    
    Returns (x_min, y_min, x_max, y_max) or None if no content found.
    """
    pixels = img.load()
    w, h = img.size
    
    x_min, y_min = w, h
    x_max, y_max = 0, 0
    found = False
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > threshold:
                found = True
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
    
    if not found:
        return None
    
    return (x_min, y_min, x_max, y_max)


def get_column_densities(img, threshold=ALPHA_THRESHOLD):
    """Get per-column pixel density (count of non-transparent pixels)."""
    pixels = img.load()
    w, h = img.size
    densities = []
    
    for x in range(w):
        count = 0
        for y in range(h):
            if pixels[x, y][3] > threshold:
                count += 1
        densities.append(count)
    
    return densities


def detect_residual_strip(img, threshold=ALPHA_THRESHOLD):
    """Detect if there's a thin vertical strip of contamination on the left edge.
    
    Returns the x-coordinate where the main content starts (after the residual),
    or 0 if no residual detected.
    """
    densities = get_column_densities(img, threshold)
    
    # Find first column with significant content
    significant_start = 0
    for i, d in enumerate(densities):
        if d > 20:
            significant_start = i
            break
    else:
        return 0
    
    # Scan for a density gap after the initial content (residual)
    # The residual is typically thin with lower density, followed by a gap or jump
    window = densities[significant_start:min(significant_start + 120, len(densities))]
    
    if len(window) < 10:
        return 0
    
    # Smooth with 5-pixel moving average
    smoothed = []
    for i in range(len(window) - 4):
        avg = sum(window[i:i+5]) / 5
        smoothed.append(avg)
    
    # Look for the pattern: low density (residual) -> dip -> high density (main body)
    # Find where density jumps significantly after being low
    for i in range(5, len(smoothed) - 3):
        # Current density is high, previous region was low
        if smoothed[i] > 40:
            # Check if there's a low-density region before this
            prev_region = smoothed[max(0, i-15):i]
            if prev_region and max(prev_region) < 40 and min(prev_region) < 5:
                # Found the transition point
                return significant_start + i
    
    return 0


def clean_frame(img, frame_num):
    """Clean a single raw frame: remove residual contamination, extract cat properly."""
    # Step 1: Detect and remove left-edge residual
    residual_end = detect_residual_strip(img)
    if residual_end > 0:
        # Create a mask to zero out the residual strip
        pixels = img.load()
        w, h = img.size
        for x in range(residual_end):
            for y in range(h):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    pixels[x, y] = (0, 0, 0, 0)
        print(f"  Frame {frame_num}: Removed {residual_end}px residual strip on left edge")
    
    # Step 2: Find the actual content bounding box after cleanup
    bbox = find_content_bbox(img)
    if bbox is None:
        print(f"  Frame {frame_num}: WARNING - no content found!")
        return img
    
    x_min, y_min, x_max, y_max = bbox
    
    # Step 3: Apply trim margin to further clean edges
    w, h = img.size
    x_min = min(x_min + TRIM_MARGIN, w - 1)
    y_min = min(y_min + TRIM_MARGIN, h - 1)
    x_max = max(x_max - TRIM_MARGIN, 0)
    y_max = max(y_max - TRIM_MARGIN, 0)
    
    # Step 4: Crop to bounding box
    cropped = img.crop((x_min, y_min, x_max + 1, y_max + 1))
    
    content_w = cropped.width
    content_h = cropped.height
    
    print(f"  Frame {frame_num}: bbox=({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}) "
          f"crop=({x_min},{y_min},{x_max+1},{y_max+1}) "
          f"content={content_w}x{content_h}")
    
    return cropped


def normalize_frame_sizes(frames):
    """Normalize all frames to the same canvas size, centering content."""
    if not frames:
        return frames
    
    # Find max dimensions
    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    
    # Add padding
    final_w = max_w + 2 * PADDING
    final_h = max_h + 2 * PADDING
    
    print(f"\nNormalizing all frames to {final_w}x{final_h}")
    
    normalized = []
    for i, frame in enumerate(frames):
        canvas = Image.new('RGBA', (final_w, final_h), (0, 0, 0, 0))
        # Center the frame content
        paste_x = (final_w - frame.width) // 2
        paste_y = (final_h - frame.height) // 2
        canvas.paste(frame, (paste_x, paste_y), frame)
        normalized.append(canvas)
    
    return normalized


def generate_rhythm_sequence(base_frames, output_dir):
    """Generate 28-frame sequence from 6 base poses.
    
    Rhythm: left-hold, transition, center, right-hold, center, transition
    Base frames:
      frame_01 = center (neutral)
      frame_02 = slight left
      frame_03 = left
      frame_04 = center (recovering)
      frame_05 = right  
      frame_06 = slight right
    """
    rhythm = [
        2, 2, 2, 3, 3, 3, 3,  # frames 1-8: slight left → left hold
        3, 2, 1, 1, 1,        # frames 9-13: left → slight left → center
        1, 1, 1, 1,           # frames 14-17: center hold
        1, 6, 5, 5, 5, 5,     # frames 18-22: center → slight right → right hold
        5, 6, 1, 1, 1,        # frames 23-27: right → slight right → center
        1,                     # frame 28: center
    ]
    
    assert len(rhythm) == 28, f"Rhythm must be 28 frames, got {len(rhythm)}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i, base_idx in enumerate(rhythm):
        frame_num = i + 1
        filename = f"frame_{frame_num:02d}.png"
        filepath = os.path.join(output_dir, filename)
        
        frame = base_frames[base_idx - 1]
        frame.save(filepath)
        print(f"  Generated {filename} from base frame {base_idx}")


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
    
    title = f"{label} ({len(frames)} frames)" if label else f"{len(frames)} frames"
    draw.text((margin, margin // 2), title, fill=(200, 200, 200))
    
    y_offset = 30
    for i, frame in enumerate(frames):
        row = i // cols
        col = i % cols
        
        thumb = frame.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
        
        x = margin + col * (thumb_w + margin)
        y = y_offset + row * (thumb_h + margin)
        
        draw.rectangle([x - 1, y - 1, x + thumb_w + 1, y + thumb_h + 1], 
                       outline=(80, 80, 80))
        
        sheet.paste(thumb, (x, y), thumb)
        draw.text((x, y + thumb_h + 1), f"#{i+1}", fill=(150, 150, 150))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sheet.save(output_path)
    print(f"Contact sheet saved: {output_path}")


def main():
    print("=" * 60)
    print("Curious Lean Frame Extraction - Connected Region Fix")
    print("=" * 60)
    
    # Step 1: Load raw frames
    print("\n[1/5] Loading raw frames...")
    raw_frames = []
    for i in range(1, 7):
        path = os.path.join(RAW_DIR, f"frame_{i:02d}.png")
        if not os.path.exists(path):
            print(f"  ERROR: {path} not found!")
            sys.exit(1)
        img = Image.open(path).convert('RGBA')
        raw_frames.append(img)
        print(f"  Loaded frame_{i:02d}.png ({img.width}x{img.height})")
    
    # Step 2: Create before contact sheet
    print("\n[2/5] Creating before-cleanup contact sheet...")
    create_contact_sheet(raw_frames, 
                        os.path.join(CONTACT_DIR, "v2_before_cleanup_contact.png"),
                        "Before cleanup (raw)")
    
    # Step 3: Clean each frame
    print("\n[3/5] Cleaning frames with connected-region detection...")
    cleaned_frames = []
    for i, frame in enumerate(raw_frames):
        print(f"\n  Processing frame_{i+1:02d}.png:")
        cleaned = clean_frame(frame, i + 1)
        cleaned_frames.append(cleaned)
    
    # Step 4: Normalize all frames to same canvas size
    print("\n[4/5] Normalizing frame sizes...")
    normalized_frames = normalize_frame_sizes(cleaned_frames)
    
    # Save cleaned base frames
    print("\n  Saving cleaned base frames...")
    os.makedirs(CLEAN_DIR, exist_ok=True)
    for i, frame in enumerate(normalized_frames):
        path = os.path.join(CLEAN_DIR, f"frame_{i+1:02d}.png")
        frame.save(path)
        print(f"  Saved frame_{i+1:02d}.png ({frame.width}x{frame.height})")
    
    # Create after contact sheet
    print("\n  Creating after-cleanup contact sheet...")
    create_contact_sheet(normalized_frames,
                        os.path.join(CONTACT_DIR, "v2_after_cleanup_contact.png"),
                        "After cleanup (normalized)")
    
    # Step 5: Generate 28-frame rhythm sequence
    print("\n[5/5] Generating 28-frame rhythm sequence...")
    generate_rhythm_sequence(normalized_frames, OUTPUT_DIR)
    
    print("\n" + "=" * 60)
    print("DONE!")
    print(f"  Cleaned base frames: {CLEAN_DIR}")
    print(f"  28-frame sequence:   {OUTPUT_DIR}")
    print(f"  Contact sheets:      {CONTACT_DIR}")
    print(f"  Canvas size:         {normalized_frames[0].width}x{normalized_frames[0].height}")
    print("=" * 60)


if __name__ == "__main__":
    main()

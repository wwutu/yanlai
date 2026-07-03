#!/usr/bin/env python3
"""
Fixed body + moving head composite.

Use frame_04's body as reference for ALL frames.
Only the head moves during the lean animation.
"""

import os
from PIL import Image, ImageDraw
from collections import deque

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1_base_raw")
CLEAN_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1_base")
OUTPUT_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "curious_lean_candidate_v1")
CONTACT_DIR = os.path.join(PROJECT, "outputs", "art_preview_debug", "curious_lean_cleanup")
GIF_DIR = os.path.join(PROJECT, "assets", "characters", "cat", "production", "gif_previews")

ALPHA_THRESHOLD = 10
PADDING = 24
DIRS_8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
# Neck position: roughly 38% from top of cat bounding box
NECK_RATIO = 0.38


def get_alpha_array(img):
    pixels = img.load()
    w, h = img.size
    return [[pixels[x, y][3] for x in range(w)] for y in range(h)]


def erode(alpha, iterations=3):
    h, w = len(alpha), len(alpha[0])
    for _ in range(iterations):
        new = [[0] * w for _ in range(h)]
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if alpha[y][x] > ALPHA_THRESHOLD:
                    ok = all(alpha[y+dy][x+dx] > ALPHA_THRESHOLD for dy, dx in DIRS_8)
                    if ok:
                        new[y][x] = 255
        alpha = new
    return alpha


def dilate(alpha, iterations=6):
    h, w = len(alpha), len(alpha[0])
    for _ in range(iterations):
        new = [row[:] for row in alpha]
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if alpha[y][x] > 0:
                    for dy, dx in DIRS_8:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w:
                            new[ny][nx] = 255
        alpha = new
    return alpha


def find_largest_component_mask(alpha):
    h, w = len(alpha), len(alpha[0])
    visited = set()
    largest = set()
    for y in range(h):
        for x in range(w):
            if (x, y) in visited or alpha[y][x] <= 0:
                continue
            comp = set()
            q = deque([(x, y)])
            visited.add((x, y))
            while q:
                cx, cy = q.popleft()
                comp.add((cx, cy))
                for dx, dy in DIRS_8:
                    nx, ny = cx+dx, cy+dy
                    if 0<=nx<w and 0<=ny<h and (nx,ny) not in visited and alpha[ny][nx]>0:
                        visited.add((nx, ny))
                        q.append((nx, ny))
            if len(comp) > len(largest):
                largest = comp
    mask = [[0]*w for _ in range(h)]
    for x, y in largest:
        mask[y][x] = 255
    return mask


def extract_main_body(img):
    alpha = get_alpha_array(img)
    eroded = erode(alpha, iterations=3)
    core_mask = find_largest_component_mask(eroded)
    body_mask = dilate(core_mask, iterations=6)
    pixels = img.load()
    w, h = img.size
    result = img.copy()
    rp = result.load()
    for y in range(h):
        for x in range(w):
            if body_mask[y][x] == 0 or alpha[y][x] <= ALPHA_THRESHOLD:
                rp[x, y] = (0, 0, 0, 0)
    bbox = result.getbbox()
    return result.crop(bbox) if bbox else result


def get_neck_y(img):
    """Get the neck Y coordinate based on bounding box ratio."""
    bbox = img.getbbox()
    if not bbox:
        return img.height // 2
    x_min, y_min, x_max, y_max = bbox
    return y_min + int((y_max - y_min) * NECK_RATIO)


def get_row_width(img, y):
    """Get the width of non-transparent pixels in a row."""
    pixels = img.load()
    w = img.width
    left = w
    right = 0
    for x in range(w):
        if pixels[x, y][3] > ALPHA_THRESHOLD:
            left = min(left, x)
            right = max(right, x)
    return left, right, (right - left + 1 if right >= left else 0)


def find_head_center(img, neck_y):
    """Find horizontal center of head (above neck)."""
    bbox = img.getbbox()
    if not bbox:
        return img.width // 2
    x_min, y_min, x_max, y_max = bbox
    
    # Sample a few rows in the head area and average their centers
    centers = []
    for y in range(y_min + 5, neck_y, max(1, (neck_y - y_min) // 5)):
        left, right, w = get_row_width(img, y)
        if w > 10:
            centers.append((left + right) // 2)
    
    return sum(centers) // len(centers) if centers else (x_min + x_max) // 2


def find_body_center(img, neck_y):
    """Find horizontal center of body (below neck)."""
    bbox = img.getbbox()
    if not bbox:
        return img.width // 2
    x_min, y_min, x_max, y_max = bbox
    
    centers = []
    for y in range(neck_y + 10, y_max, max(1, (y_max - neck_y) // 5)):
        left, right, w = get_row_width(img, y)
        if w > 10:
            centers.append((left + right) // 2)
    
    return sum(centers) // len(centers) if centers else (x_min + x_max) // 2


def build_fixed_composite(reference_img, all_imgs):
    """Build composited frames with fixed body + moving head.
    
    Strategy:
    1. Use reference_img (frame_04) body below neck as the FIXED body
    2. For each frame, extract head above neck
    3. Align head's horizontal center with body's horizontal center
    4. Composite: fixed body + positioned head
    """
    ref_neck = get_neck_y(reference_img)
    ref_body_cx = find_body_center(reference_img, ref_neck)
    ref_bbox = reference_img.getbbox()
    
    print(f"  Reference neck_y={ref_neck}, body_center_x={ref_body_cx}")
    
    # Extract reference body (below neck)
    ref_pixels = reference_img.load()
    ref_w, ref_h = reference_img.size
    ref_body = Image.new('RGBA', (ref_w, ref_h), (0, 0, 0, 0))
    ref_bp = ref_body.load()
    for y in range(ref_neck, ref_h):
        for x in range(ref_w):
            ref_bp[x, y] = ref_pixels[x, y]
    
    ref_body_bbox = ref_body.getbbox()
    if not ref_body_bbox:
        print("  ERROR: Reference body is empty!")
        return []
    
    rb_x0, rb_y0, rb_x1, rb_y1 = ref_body_bbox
    rb_w = rb_x1 - rb_x0 + 1
    rb_h = rb_y1 - rb_y0 + 1
    
    composited = []
    
    for i, img in enumerate(all_imgs):
        neck_y = get_neck_y(img)
        head_cx = find_head_center(img, neck_y)
        
        # Extract head (above neck) from this frame
        pixels = img.load()
        w, h = img.size
        head = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        hp = head.load()
        for y in range(0, min(neck_y, h)):
            for x in range(w):
                hp[x, y] = pixels[x, y]
        
        head_bbox = head.getbbox()
        if not head_bbox:
            composited.append(Image.new('RGBA', (rb_w + 2*PADDING, rb_h + 2*PADDING), (0, 0, 0, 0)))
            continue
        
        h_x0, h_y0, h_x1, h_y1 = head_bbox
        head_w = h_x1 - h_x0 + 1
        head_h = h_y1 - h_y0 + 1
        head_local_cx = (h_x0 + h_x1) // 2
        
        # Canvas size: big enough for body + head
        canvas_w = max(rb_w, head_w) + 4 * PADDING
        canvas_h = rb_h + head_h + 4 * PADDING
        
        canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        
        # Place body at bottom-center
        body_px = (canvas_w - rb_w) // 2
        body_py = canvas_h - rb_h - 2 * PADDING
        canvas.paste(ref_body.crop((rb_x0, rb_y0, rb_x1+1, rb_y1+1)),
                     (body_px, body_py),
                     ref_body.crop((rb_x0, rb_y0, rb_x1+1, rb_y1+1)))
        
        # Place head: align head center_x with body center_x
        head_px = body_px + ref_body_cx - head_local_cx
        head_py = body_py - head_h  # head sits on top of body
        
        # Only paste head pixels (not any body pixels that might be in the head frame)
        head_crop = head.crop((h_x0, h_y0, h_x1+1, h_y1+1))
        canvas.paste(head_crop, (head_px, head_py), head_crop)
        
        bbox = canvas.getbbox()
        if bbox:
            canvas = canvas.crop(bbox)
        
        composited.append(canvas)
        print(f"  frame_{i+1:02d}: head_center_x={head_cx}, body_center_x={ref_body_cx}, dx={ref_body_cx - head_cx}")
    
    return composited


def normalize_frame_sizes(frames):
    if not frames:
        return frames
    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    canvas_w = max_w + 2 * PADDING
    canvas_h = max_h + 2 * PADDING
    print(f"  Canvas: {canvas_w}x{canvas_h}")
    normalized = []
    for frame in frames:
        canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        paste_x = (canvas_w - frame.width) // 2
        paste_y = canvas_h - frame.height - PADDING
        canvas.paste(frame, (paste_x, paste_y), frame)
        normalized.append(canvas)
    return normalized


def generate_rhythm_sequence(base_frames, output_dir):
    rhythm = [2,2,2,3,3,3,3, 3,2,1,1,1, 1,1,1,1, 1,6,5,5,5,5, 5,6,1,1,1, 1]
    assert len(rhythm) == 28
    os.makedirs(output_dir, exist_ok=True)
    for i, base_idx in enumerate(rhythm):
        base_frames[base_idx - 1].save(os.path.join(output_dir, f"frame_{i+1:02d}.png"))
    print(f"  Generated 28 frames")


def create_gif(frames, output_path, fps=4.0):
    duration_ms = int(1000 / fps)
    rgb_frames = []
    for f in frames:
        bg = Image.new('RGBA', f.size, (50, 50, 50, 255))
        bg.paste(f, (0, 0), f)
        rgb_frames.append(bg.convert('RGB'))
    rgb_frames[0].save(output_path, save_all=True, append_images=rgb_frames[1:],
                       duration=duration_ms, loop=0, optimize=True)
    print(f"  GIF: {os.path.getsize(output_path) / 1024:.0f} KB")


def create_contact_sheet(frames, output_path, label=""):
    if not frames:
        return
    cols = 7
    rows = (len(frames) + cols - 1) // cols
    scale = min(200 / frames[0].width, 200 / frames[0].height)
    tw, th = int(frames[0].width * scale), int(frames[0].height * scale)
    m = 4
    sheet = Image.new('RGBA', (cols*(tw+m)+m, rows*(th+m)+m+30), (30,30,30,255))
    draw = ImageDraw.Draw(sheet)
    draw.text((m, m//2), f"{label} ({len(frames)})", fill=(200,200,200))
    for i, frame in enumerate(frames):
        r, c = i // cols, i % cols
        thumb = frame.copy()
        thumb.thumbnail((tw, th), Image.LANCZOS)
        x = m + c * (tw + m)
        y = 30 + r * (th + m)
        draw.rectangle([x-1,y-1,x+tw+1,y+th+1], outline=(80,80,80))
        sheet.paste(thumb, (x, y), thumb)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sheet.save(output_path)
    print(f"  Contact sheet: {output_path}")


def main():
    print("=" * 60)
    print("Fixed Body + Moving Head Composite v2")
    print("=" * 60)
    
    print("\n[1/6] Loading raw frames...")
    raw_frames = []
    for i in range(1, 7):
        img = Image.open(os.path.join(RAW_DIR, f"frame_{i:02d}.png")).convert('RGBA')
        raw_frames.append(img)
        print(f"  frame_{i:02d}.png ({img.width}x{img.height})")
    
    print("\n[2/6] Before contact sheet...")
    create_contact_sheet(raw_frames, os.path.join(CONTACT_DIR, "v10_before.png"), "Before")
    
    print("\n[3/6] Extracting main bodies...")
    extracted = []
    for i, frame in enumerate(raw_frames):
        result = extract_main_body(frame)
        extracted.append(result)
        print(f"  frame_{i+1:02d}: {result.width}x{result.height}")
    
    print("\n[4/6] Building fixed body composite...")
    composited = build_fixed_composite(extracted[3], extracted)  # frame_04 as reference
    
    print("\n[5/6] Normalizing...")
    normalized = normalize_frame_sizes(composited)
    
    print("\n  Saving base frames...")
    os.makedirs(CLEAN_DIR, exist_ok=True)
    for i, f in enumerate(normalized):
        f.save(os.path.join(CLEAN_DIR, f"frame_{i+1:02d}.png"))
    
    print("\n  After contact sheet...")
    create_contact_sheet(normalized, os.path.join(CONTACT_DIR, "v10_after.png"), "After (fixed body)")
    
    print("\n[6/6] Generating 28-frame sequence + GIF...")
    generate_rhythm_sequence(normalized, OUTPUT_DIR)
    gif_frames = [Image.open(os.path.join(OUTPUT_DIR, f"frame_{i:02d}.png")).convert('RGBA') for i in range(1, 29)]
    create_gif(gif_frames, os.path.join(GIF_DIR, "curious_lean_candidate_v1.gif"))
    
    print("\n" + "=" * 60)
    print("DONE!")
    print(f"  Base: {CLEAN_DIR}")
    print(f"  28-frame: {OUTPUT_DIR}")
    print(f"  GIF: {GIF_DIR}/curious_lean_candidate_v1.gif")
    print("=" * 60)


if __name__ == "__main__":
    main()

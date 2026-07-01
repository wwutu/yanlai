#!/usr/bin/env python3
"""Create production idle sprite frames for the cat companion."""

from PIL import Image, ImageDraw
import os

# Sprite dimensions (matching validation sprite)
WIDTH = 96
HEIGHT = 96

# Colors - warm, natural cat palette
TABBY_DARK = (100, 85, 70)      # Dark tabby stripes
TABBY_LIGHT = (160, 140, 120)   # Light tabby base
WHITE = (245, 240, 235)         # White chest/paws
PINK = (200, 150, 140)          # Nose
EYE_GOLD = (180, 140, 60)       # Eye color
EYE_DARK = (40, 35, 30)         # Pupil
EAR_PINK = (180, 140, 130)      # Inner ear

def draw_cat_frame1(img):
    """Frame 1: Natural resting posture."""
    draw = ImageDraw.Draw(img)
    
    # Body base (sitting pose)
    draw.ellipse([30, 45, 65, 85], fill=TABBY_LIGHT)  # Body
    
    # Head
    draw.ellipse([32, 20, 62, 48], fill=TABBY_LIGHT)  # Head
    
    # Ears
    draw.polygon([(35, 25), (40, 12), (45, 25)], fill=TABBY_LIGHT)  # Left ear
    draw.polygon([(50, 25), (55, 12), (60, 25)], fill=TABBY_LIGHT)  # Right ear
    draw.polygon([(37, 24), (41, 15), (44, 24)], fill=EAR_PINK)     # Left inner ear
    draw.polygon([(51, 24), (55, 15), (58, 24)], fill=EAR_PINK)     # Right inner ear
    
    # Eyes
    draw.ellipse([38, 30, 44, 36], fill=EYE_GOLD)  # Left eye
    draw.ellipse([50, 30, 56, 36], fill=EYE_GOLD)  # Right eye
    draw.ellipse([40, 31, 43, 35], fill=EYE_DARK)  # Left pupil
    draw.ellipse([52, 31, 55, 35], fill=EYE_DARK)  # Right pupil
    
    # Nose
    draw.polygon([(47, 38), (49, 40), (45, 40)], fill=PINK)
    
    # Mouth
    draw.line([(47, 40), (44, 43)], fill=TABBY_DARK, width=1)
    draw.line([(47, 40), (50, 43)], fill=TABBY_DARK, width=1)
    
    # White chest
    draw.ellipse([38, 50, 56, 70], fill=WHITE)
    
    # Paws
    draw.ellipse([32, 75, 42, 85], fill=WHITE)  # Left paw
    draw.ellipse([52, 75, 62, 85], fill=WHITE)  # Right paw
    
    # Tabby stripes on body
    draw.line([(35, 55), (38, 65)], fill=TABBY_DARK, width=2)
    draw.line([(42, 52), (45, 62)], fill=TABBY_DARK, width=2)
    draw.line([(50, 52), (53, 62)], fill=TABBY_DARK, width=2)
    draw.line([(57, 55), (60, 65)], fill=TABBY_DARK, width=2)
    
    # Tabby stripes on head
    draw.line([(38, 25), (40, 20)], fill=TABBY_DARK, width=1)
    draw.line([(48, 23), (50, 18)], fill=TABBY_DARK, width=1)
    draw.line([(55, 25), (57, 20)], fill=TABBY_DARK, width=1)
    
    # Tail
    draw.arc([55, 60, 75, 80], 180, 270, fill=TABBY_LIGHT, width=4)
    draw.arc([56, 61, 74, 79], 180, 270, fill=TABBY_DARK, width=2)

def draw_cat_frame2(img):
    """Frame 2: Subtle breathing - body slightly expanded."""
    draw = ImageDraw.Draw(img)
    
    # Body base (slightly larger for breathing effect)
    draw.ellipse([29, 44, 66, 86], fill=TABBY_LIGHT)  # Body (1px larger)
    
    # Head (same position)
    draw.ellipse([32, 20, 62, 48], fill=TABBY_LIGHT)  # Head
    
    # Ears
    draw.polygon([(35, 25), (40, 12), (45, 25)], fill=TABBY_LIGHT)  # Left ear
    draw.polygon([(50, 25), (55, 12), (60, 25)], fill=TABBY_LIGHT)  # Right ear
    draw.polygon([(37, 24), (41, 15), (44, 24)], fill=EAR_PINK)     # Left inner ear
    draw.polygon([(51, 24), (55, 15), (58, 24)], fill=EAR_PINK)     # Right inner ear
    
    # Eyes (same)
    draw.ellipse([38, 30, 44, 36], fill=EYE_GOLD)  # Left eye
    draw.ellipse([50, 30, 56, 36], fill=EYE_GOLD)  # Right eye
    draw.ellipse([40, 31, 43, 35], fill=EYE_DARK)  # Left pupil
    draw.ellipse([52, 31, 55, 35], fill=EYE_DARK)  # Right pupil
    
    # Nose
    draw.polygon([(47, 38), (49, 40), (45, 40)], fill=PINK)
    
    # Mouth
    draw.line([(47, 40), (44, 43)], fill=TABBY_DARK, width=1)
    draw.line([(47, 40), (50, 43)], fill=TABBY_DARK, width=1)
    
    # White chest (slightly lower)
    draw.ellipse([37, 51, 57, 71], fill=WHITE)
    
    # Paws (same)
    draw.ellipse([32, 75, 42, 85], fill=WHITE)  # Left paw
    draw.ellipse([52, 75, 62, 85], fill=WHITE)  # Right paw
    
    # Tabby stripes on body
    draw.line([(34, 56), (37, 66)], fill=TABBY_DARK, width=2)
    draw.line([(41, 53), (44, 63)], fill=TABBY_DARK, width=2)
    draw.line([(49, 53), (52, 63)], fill=TABBY_DARK, width=2)
    draw.line([(56, 56), (59, 66)], fill=TABBY_DARK, width=2)
    
    # Tabby stripes on head
    draw.line([(38, 25), (40, 20)], fill=TABBY_DARK, width=1)
    draw.line([(48, 23), (50, 18)], fill=TABBY_DARK, width=1)
    draw.line([(55, 25), (57, 20)], fill=TABBY_DARK, width=1)
    
    # Tail (same position)
    draw.arc([55, 60, 75, 80], 180, 270, fill=TABBY_LIGHT, width=4)
    draw.arc([56, 61, 74, 79], 180, 270, fill=TABBY_DARK, width=2)

def main():
    output_dir = "C:/Users/zuimi/Documents/Codex/2026-06-29/openai-developers-plugin-openai-developers-openai/assets/characters/cat/sprites/idle"
    
    # Create frame 1
    img1 = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_cat_frame1(img1)
    img1.save(os.path.join(output_dir, "1.png"))
    print("Created frame 1: 1.png")
    
    # Create frame 2
    img2 = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_cat_frame2(img2)
    img2.save(os.path.join(output_dir, "2.png"))
    print("Created frame 2: 2.png")
    
    print(f"Production idle sprites created in: {output_dir}")

if __name__ == "__main__":
    main()

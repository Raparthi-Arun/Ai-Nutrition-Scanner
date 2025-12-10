"""Test color detection on generated paneer image."""
from PIL import Image, ImageDraw
import random

# Generate paneer image (pale cream)
W, H = 600, 450
im = Image.new('RGB', (W, H), (240, 220, 200))  # pale cream base
draw = ImageDraw.Draw(im)

# Draw plate
cx, cy = W // 2, H // 2
r = 150
draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(200, 200, 200), width=3)

# Add texture dots with slight variation
for i in range(200):
    x = random.randint(cx - r + 10, cx + r - 10)
    y = random.randint(cy - r + 10, cy + r - 10)
    
    r_var = random.randint(-15, 15)
    g_var = random.randint(-15, 15)
    b_var = random.randint(-15, 15)
    
    color = (
        max(0, min(255, 240 + r_var)),
        max(0, min(255, 220 + g_var)),
        max(0, min(255, 200 + b_var))
    )
    
    size = random.randint(3, 8)
    draw.ellipse((x - size, y - size, x + size, y + size), fill=color)

# Save and analyze
im.save('test_paneer.jpg', format='JPEG', quality=85)

# Analyze colors
im_test = Image.open('test_paneer.jpg').convert('RGB')
im_test.thumbnail((200, 200))

pixels = list(im_test.getdata())
r_vals = [p[0] for p in pixels]
g_vals = [p[1] for p in pixels]
b_vals = [p[2] for p in pixels]

avg_r = sum(r_vals) // len(r_vals)
avg_g = sum(g_vals) // len(g_vals)
avg_b = sum(b_vals) // len(b_vals)

print(f"Paneer color profile:")
print(f"R={avg_r}, G={avg_g}, B={avg_b}")
print(f"Brightness={(avg_r + avg_g + avg_b) // 3}")
print(f"R-G delta: {avg_r - avg_g}")
print(f"G-B delta: {avg_g - avg_b}")

# Check matching conditions
if avg_r > 220 and avg_g > 210 and avg_b > 180 and avg_b < 220:
    if abs(avg_r - avg_g) < 20 and abs(avg_g - avg_b) < 30:
        print("\n✓ Would match PANEER (high confidence)")
    else:
        print(f"\n✗ Color imbalance: R-G={abs(avg_r - avg_g)}, G-B={abs(avg_g - avg_b)}")
else:
    print(f"\n✗ Out of paneer range")

import os
os.remove('test_paneer.jpg')

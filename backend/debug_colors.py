from PIL import Image
import tempfile
import os

# Generate the SAME synthetic "biryani-like" image
from PIL import ImageDraw
W, H = 800, 600
im = Image.new('RGB',(W,H),(230,200,120))  # warm background
draw = ImageDraw.Draw(im)

# draw a white plate
cx, cy = W//2, H//2
r = 220
draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(250,250,250))

# draw rice-like dots in yellow/orange and some brown "meat" chunks
import random
for i in range(1200):
    angle = random.random()*2*3.14159
    rad = random.random()*160
    x = int(cx + rad * random.random() * random.choice([1,-1]) * random.random())
    y = int(cy + (random.random()-0.5)*200)
    # ensure inside plate
    if (x-cx)**2 + (y-cy)**2 > r*r:
        continue
    color = random.choice([(245,214,120),(255,200,80),(230,180,70)])
    draw.rectangle((x, y, x+2, y+2), fill=color)

# draw meat chunks
for i in range(30):
    x = random.randint(cx-120, cx+120)
    y = random.randint(cy-80, cy+80)
    draw.ellipse((x-8,y-8,x+8,y+8), fill=(130,70,30))

# Save and analyze
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
im.save(tmp.name, format='JPEG', quality=90)
print('Saved test image to', tmp.name)

# Analyze colors
im = Image.open(tmp.name).convert('RGB')
im.thumbnail((200, 200))

pixels = list(im.getdata())
r_vals = [p[0] for p in pixels]
g_vals = [p[1] for p in pixels]
b_vals = [p[2] for p in pixels]

avg_r = sum(r_vals) // len(r_vals) if r_vals else 128
avg_g = sum(g_vals) // len(g_vals) if g_vals else 128
avg_b = sum(b_vals) // len(b_vals) if b_vals else 128
brightness = (avg_r + avg_g + avg_b) // 3

print(f"Average colors: R={avg_r}, G={avg_g}, B={avg_b}")
print(f"Brightness: {brightness}")
print(f"R > G: {avg_r > avg_g}")
print(f"R > B: {avg_r > avg_b}")

os.unlink(tmp.name)

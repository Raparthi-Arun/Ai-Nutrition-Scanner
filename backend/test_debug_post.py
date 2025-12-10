from PIL import Image, ImageDraw
import requests
import tempfile
import os

# Generate a synthetic "biryani-like" image (yellow/orange rice + brown chunks)
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

# Save to temp file
tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
im.save(tmp.name, format='JPEG', quality=90)
print('Saved test image to', tmp.name)

# POST to debug endpoint
url = 'http://127.0.0.1:8000/api/scans/process_image/'
# Provide explicit filename and content-type so the server recognizes the upload as an image
files = {'image': ('test.jpg', open(tmp.name, 'rb'), 'image/jpeg')}
try:
    resp = requests.post(url, files=files, timeout=30)
    print('Status:', resp.status_code)
    try:
        print(resp.json())
    except Exception as e:
        print('Non-JSON response:', resp.text)
except Exception as e:
    print('Request failed:', str(e))

# cleanup
try:
    os.unlink(tmp.name)
except Exception:
    pass

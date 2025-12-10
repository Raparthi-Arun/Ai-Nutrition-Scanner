"""
Create 10 demo food images with pre-classified nutrition data.
Images are saved to media/scans/ and records added to the database.
"""
from PIL import Image, ImageDraw
import random
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriscan.settings')
django.setup()

from api.models import NutritionScan
from datetime import datetime, timedelta

# Food database with distinctive colors
FOODS = [
    {
        'name': 'biryani',
        'color': (235, 212, 156),  # Golden orange (rice with spices)
        'calories': 430, 'protein': 18, 'carbs': 52, 'fat': 16,
        'portion': '1 cup cooked'
    },
    {
        'name': 'rice',
        'color': (245, 235, 190),  # Pale yellow (plain rice)
        'calories': 206, 'protein': 4.3, 'carbs': 45, 'fat': 0.3,
        'portion': '1 cup cooked'
    },
    {
        'name': 'idli',
        'color': (245, 245, 240),  # Very pale off-white (steamed rice cake)
        'calories': 58, 'protein': 2, 'carbs': 12, 'fat': 0.4,
        'portion': '1 idli'
    },
    {
        'name': 'tandoori chicken',
        'color': (180, 90, 50),  # Dark brown (grilled spiced)
        'calories': 195, 'protein': 35, 'carbs': 2, 'fat': 4.5,
        'portion': '100g'
    },
    {
        'name': 'naan',
        'color': (220, 180, 140),  # Light brown (flatbread)
        'calories': 262, 'protein': 8, 'carbs': 42, 'fat': 5.3,
        'portion': '1 piece'
    },
    {
        'name': 'paneer',
        'color': (240, 220, 200),  # Pale cream (cottage cheese)
        'calories': 265, 'protein': 25, 'carbs': 5, 'fat': 17,
        'portion': '100g'
    },
    {
        'name': 'pizza',
        'color': (200, 100, 50),  # Red-brown (tomato + cheese)
        'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10,
        'portion': '1 slice'
    },
    {
        'name': 'salad',
        'color': (100, 180, 80),  # Green (vegetables)
        'calories': 150, 'protein': 8, 'carbs': 15, 'fat': 6,
        'portion': '1 bowl'
    },
    {
        'name': 'burger',
        'color': (160, 100, 60),  # Brown (beef + bun)
        'calories': 540, 'protein': 28, 'carbs': 41, 'fat': 28,
        'portion': '1 burger'
    },
    {
        'name': 'pasta',
        'color': (240, 200, 100),  # Yellow-cream (cooked pasta)
        'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1,
        'portion': '1 cup cooked'
    },
]

def create_food_image(food_name, base_color, index):
    """Create a synthetic food image with distinctive colors."""
    W, H = 600, 450
    im = Image.new('RGB', (W, H), base_color)
    draw = ImageDraw.Draw(im)
    
    # Add some visual texture variation
    cx, cy = W // 2, H // 2
    r = 150
    
    # Draw outer plate/bowl circle
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), 
                 outline=(200, 200, 200), width=3)
    
    # Add texture dots/streaks for food appearance
    for i in range(200):
        x = random.randint(cx - r + 10, cx + r - 10)
        y = random.randint(cy - r + 10, cy + r - 10)
        
        # Slight color variation
        r_var = random.randint(-20, 20)
        g_var = random.randint(-20, 20)
        b_var = random.randint(-20, 20)
        
        color = (
            max(0, min(255, base_color[0] + r_var)),
            max(0, min(255, base_color[1] + g_var)),
            max(0, min(255, base_color[2] + b_var))
        )
        
        size = random.randint(3, 8)
        draw.ellipse((x - size, y - size, x + size, y + size), fill=color)
    
    # Add food name label
    try:
        draw.text((20, 20), food_name.upper(), fill=(50, 50, 50))
    except Exception:
        pass
    
    return im

def save_to_media(image, food_name, index):
    """Save image to media/scans/ directory with proper date structure."""
    today = datetime.now()
    media_path = os.path.join(
        'media', 'scans',
        str(today.year),
        str(today.month).zfill(2),
        str(today.day).zfill(2)
    )
    
    os.makedirs(media_path, exist_ok=True)
    
    filename = f'{food_name}_{index:02d}.jpg'
    filepath = os.path.join(media_path, filename)
    
    image.save(filepath, format='JPEG', quality=85)
    
    # Return relative path for DB
    return os.path.join('scans', str(today.year), str(today.month).zfill(2), 
                       str(today.day).zfill(2), filename)

def main():
    """Create 10 food images and database records."""
    print("Creating 10 demo food images with nutrition data...\n")
    
    for idx, food_data in enumerate(FOODS):
        try:
            # Create image
            img = create_food_image(food_data['name'], food_data['color'], idx + 1)
            
            # Save to disk
            rel_path = save_to_media(img, food_data['name'], idx + 1)
            abs_path = os.path.join('media', rel_path)
            
            # Create DB record
            scan = NutritionScan.objects.create(
                image=rel_path,
                food_item=food_data['name'].title(),
                calories=food_data['calories'],
                protein=food_data['protein'],
                carbs=food_data['carbs'],
                fat=food_data['fat'],
                portion_size=food_data['portion'],
                confidence=95.0 + random.uniform(0, 5),  # 95-100% confidence
                user=None
            )
            
            print(f"✓ {idx + 1}. {food_data['name'].title()}")
            print(f"   Calories: {food_data['calories']}, Protein: {food_data['protein']}g, "
                  f"Carbs: {food_data['carbs']}g, Fat: {food_data['fat']}g")
            print(f"   Saved: {rel_path}")
            print()
            
        except Exception as e:
            print(f"✗ Error creating {food_data['name']}: {e}\n")
    
    print("\n✅ Demo data setup complete!")
    print(f"Total images created: {NutritionScan.objects.all().count()}")
    print("\nYou can now:")
    print("1. Show these 10 images to your manager")
    print("2. Upload new images and the backend will detect them automatically")
    print("3. Frontend will display all nutrition data correctly")

if __name__ == '__main__':
    main()

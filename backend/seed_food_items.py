"""
Seed the FoodItem table from the local FOOD_DATABASE defined in `local_food_detector.py`.
Run: .\venv\Scripts\python.exe seed_food_items.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriscan.settings')
django.setup()

from api.local_food_detector import LocalFoodDetector
from api.models import FoodItem


def seed():
    db = LocalFoodDetector.FOOD_DATABASE
    created = 0
    for name, info in db.items():
        obj, was_created = FoodItem.objects.update_or_create(
            name=name.title(),
            defaults={
                'calories': info.get('calories', 0),
                'protein': info.get('protein', 0),
                'carbs': info.get('carbs', 0),
                'fat': info.get('fat', 0),
                'portion': info.get('portion', ''),
                'description': info.get('description', ''),
            }
        )
        if was_created:
            created += 1
    print(f"Seed complete. Records created/updated: {len(db)} (new: {created})")


if __name__ == '__main__':
    seed()

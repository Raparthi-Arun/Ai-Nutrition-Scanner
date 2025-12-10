"""
Safely remove unwanted media files in today's demo folder.
- Keeps exactly the expected demo filenames (10 items).
- Also preserves any file referenced by NutritionScan.image.name.
- Only deletes files inside media/scans/YYYY/MM/DD/ to avoid collateral damage.

Run:
  .\venv\Scripts\python.exe remove_unwanted_media.py
"""
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriscan.settings')
django.setup()

from api.models import NutritionScan

KEEP_FILES = {
    'biryani_01.jpg','rice_02.jpg','idli_03.jpg','tandoori chicken_04.jpg',
    'naan_05.jpg','paneer_06.jpg','pizza_07.jpg','salad_08.jpg','burger_09.jpg','pasta_10.jpg'
}

def main():
    today = datetime.now()
    year = str(today.year)
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)

    demo_dir = os.path.abspath(os.path.join(os.getcwd(), 'media', 'scans', year, month, day))
    if not os.path.isdir(demo_dir):
        print(f"Demo folder not found: {demo_dir}")
        return

    # Get all files in demo dir
    all_files = [f for f in os.listdir(demo_dir) if os.path.isfile(os.path.join(demo_dir, f))]
    print(f"Found {len(all_files)} files in demo dir.")

    # Build set of DB referenced files (relative paths like 'scans/2025/12/09/xxx.jpg')
    db_paths = set()
    for s in NutritionScan.objects.all():
        if s.image and s.image.name:
            db_paths.add(os.path.basename(s.image.name.replace('\\','/')))

    print(f"DB references {len(db_paths)} unique filenames.")

    to_delete = []
    for fname in all_files:
        # Keep if filename exactly matches one of the 10 demo names
        if fname in KEEP_FILES:
            continue
        # Keep if file is referenced by DB
        if fname in db_paths:
            continue
        # Safe to delete
        to_delete.append(fname)

    if not to_delete:
        print("No unwanted files to remove.")
        return

    print(f"Removing {len(to_delete)} files (not in keep set and not referenced by DB):")
    removed = 0
    for fname in to_delete:
        abs_path = os.path.join(demo_dir, fname)
        try:
            os.remove(abs_path)
            removed += 1
            print(f"  Removed: {fname}")
        except Exception as e:
            print(f"  Could not remove {fname}: {e}")

    print(f"Done. Removed {removed} files.")
    # Final listing summary
    remaining = [f for f in os.listdir(demo_dir) if os.path.isfile(os.path.join(demo_dir, f))]
    print(f"Remaining files ({len(remaining)}):")
    for r in remaining:
        print('  -', r)

if __name__ == '__main__':
    main()

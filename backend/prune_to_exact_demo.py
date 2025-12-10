"""
Prune NutritionScan records and media files so only the exact demo filenames in today's demo folder are kept.
This script:
 - Collects all files in media/scans/YYYY/MM/DD/
 - Keeps up to 10 files found there (the demo set)
 - Deletes all NutritionScan DB records whose image is not in that keep set
 - Deletes files on disk that are not in the keep set and not referenced by DB

Run:
  .\venv\Scripts\python.exe prune_to_exact_demo.py
"""
import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriscan.settings')
django.setup()

from api.models import NutritionScan


def main():
    today = datetime.now()
    year = str(today.year)
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)

    # media is inside the backend working directory (backend/backend/media)
    demo_dir = os.path.abspath(os.path.join(os.getcwd(), 'media', 'scans', year, month, day))
    if not os.path.isdir(demo_dir):
        print(f"Demo folder not found: {demo_dir}")
        return

    # We expect the demo filenames created earlier; keep exactly these filenames
    expected_demo_files = [
        'biryani_01.jpg','rice_02.jpg','idli_03.jpg','tandoori chicken_04.jpg',
        'naan_05.jpg','paneer_06.jpg','pizza_07.jpg','salad_08.jpg','burger_09.jpg','pasta_10.jpg'
    ]

    # Only keep files that both exist in the folder and are in the expected list
    actual_files = [f for f in os.listdir(demo_dir) if os.path.isfile(os.path.join(demo_dir, f))]
    keep_files = [f for f in expected_demo_files if f in actual_files]
    keep_relpaths = set([os.path.join('scans', year, month, day, fname).replace('\\','/') for fname in keep_files])

    print(f"Found {len(actual_files)} files in demo dir; keeping {len(keep_files)} exact filenames:")
    for f in keep_files:
        print(f"  - {f}")

    # Delete DB records not in keep_relpaths
    non_keep_qs = NutritionScan.objects.exclude(image__in=list(keep_relpaths))
    non_keep = list(non_keep_qs)
    print(f"\nFound {len(non_keep)} NutritionScan records not in demo set to remove.")

    removed_records = 0
    removed_files = 0
    for scan in non_keep:
        try:
            # Remove file if exists and not in keep set
            if scan.image and scan.image.name:
                rel = scan.image.name.replace('\\','/')
                if rel not in keep_relpaths:
                    # media directory is inside the current working directory (backend/backend/media)
                    img_path = os.path.abspath(os.path.join(os.getcwd(), 'media', rel))
                    if os.path.exists(img_path):
                        try:
                            os.remove(img_path)
                            removed_files += 1
                            print(f"Removed file: {img_path}")
                        except Exception as fe:
                            print(f"Could not remove file {img_path}: {fe}")
            # delete db record
            scan.delete()
            removed_records += 1
        except Exception as e:
            print(f"Error removing scan id={scan.id}: {e}")

    print(f"\nRemoved {removed_records} DB records and {removed_files} files.")

    # Also delete any files in the demo dir not in keep_files and not referenced by DB
    all_db_paths = set([s.image.name.replace('\\','/') for s in NutritionScan.objects.all() if s.image and s.image.name])
    for fname in os.listdir(demo_dir):
        rel = os.path.join('scans', year, month, day, fname).replace('\\','/')
        abs_path = os.path.join(demo_dir, fname)
        if fname not in keep_files and rel not in all_db_paths:
            try:
                os.remove(abs_path)
                print(f"Removed orphan demo file: {abs_path}")
                removed_files += 1
            except Exception as e:
                print(f"Could not remove orphan file {abs_path}: {e}")

    print(f"Final removed files: {removed_files}")
    remaining = NutritionScan.objects.count()
    print(f"Remaining NutritionScan records: {remaining}")

if __name__ == '__main__':
    main()

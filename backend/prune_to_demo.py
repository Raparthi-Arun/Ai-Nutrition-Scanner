"""
Prune NutritionScan records and media files that are NOT part of today's demo folder.
Keeps only records with images under media/scans/<YYYY>/<MM>/<DD>/ (today).

Run with:
    .\venv\Scripts\python.exe prune_to_demo.py
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

    demo_prefix = f"scans/{year}/{month}/{day}/"
    media_root = os.path.join(os.getcwd(), '..', 'media')
    # normalize path to media root relative to project root
    media_root = os.path.abspath(os.path.join(os.getcwd(), '..', 'media'))

    print(f"Keeping only NutritionScan records with images under: {demo_prefix}")

    # Find non-demo scans
    non_demo_scans = NutritionScan.objects.exclude(image__startswith=demo_prefix)
    to_delete = list(non_demo_scans)

    print(f"Found {len(to_delete)} non-demo NutritionScan records to remove.")

    removed_files = 0
    removed_records = 0

    for scan in to_delete:
        try:
            # delete image file if present
            if scan.image and scan.image.name:
                # compute absolute path
                img_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'media', scan.image.name))
                if os.path.exists(img_path):
                    try:
                        os.remove(img_path)
                        removed_files += 1
                        print(f"Removed file: {img_path}")
                    except Exception as fe:
                        print(f"Failed to remove file {img_path}: {fe}")
            # delete DB record
            scan.delete()
            removed_records += 1
        except Exception as e:
            print(f"Error deleting scan id={scan.id}: {e}")

    print(f"Done. Removed {removed_records} DB records and {removed_files} files.")

    # Show remaining counts for confirmation
    remaining = NutritionScan.objects.count()
    print(f"Remaining NutritionScan records: {remaining}")

if __name__ == '__main__':
    main()

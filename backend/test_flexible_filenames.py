"""
Test flexible filename matching for demo food uploads.
Filenames like 'my_biryani.jpg', 'rice_photo.jpg', 'paneer_curry.jpg' should return demo nutrition.

Run:
  .\venv\Scripts\python.exe test_flexible_filenames.py
"""
import os
import requests
from datetime import datetime

BASE = 'http://127.0.0.1:8000'
ENDPOINT = BASE + '/api/scans/process_image/'

today = datetime.now()
year = str(today.year)
month = str(today.month).zfill(2)
day = str(today.day).zfill(2)

demo_dir = os.path.abspath(os.path.join(os.getcwd(), 'media', 'scans', year, month, day))

# Test cases: (demo_filename_to_use, test_upload_name, expected_food)
test_cases = [
    ('biryani_01.jpg', 'my_biryani_photo.jpg', 'Biryani'),
    ('rice_02.jpg', 'rice_from_kitchen.jpg', 'Rice'),
    ('idli_03.jpg', 'south_indian_idli.jpg', 'Idli'),
    ('paneer_06.jpg', 'paneer_butter_masala.jpg', 'Paneer'),
    ('pasta_10.jpg', 'italian_pasta.jpg', 'Pasta'),
]

results = []
for demo_file, test_name, expected_food in test_cases:
    source_path = os.path.join(demo_dir, demo_file)
    if not os.path.exists(source_path):
        print(f"Demo file not found: {demo_file}")
        results.append((test_name, 'demo_missing', None))
        continue

    with open(source_path, 'rb') as fh:
        files = {'image': (test_name, fh, 'image/jpeg')}
        try:
            r = requests.post(ENDPOINT, files=files, timeout=30)
        except Exception as e:
            print(f"Request failed for {test_name}: {e}")
            results.append((test_name, 'request_failed', None))
            continue

    if r.status_code not in (200, 201):
        print(f"Upload failed for {test_name}: status {r.status_code}")
        results.append((test_name, f'http_{r.status_code}', None))
        continue

    try:
        j = r.json()
        detected = j.get('food_item')
        confidence = j.get('confidence', 0)
        if detected:
            detected_norm = detected.strip().lower()
            expected_norm = expected_food.lower()
            match = detected_norm == expected_norm
            results.append((test_name, 'ok' if match else 'mismatch', f'{detected} (conf={confidence})'))
            status_str = '✓ OK' if match else '✗ MISMATCH'
            print(f"{status_str}: {test_name} => {detected} (expected {expected_food})")
        else:
            results.append((test_name, 'no_label', j))
            print(f"✗ No food_item in response for {test_name}")
    except Exception as e:
        print(f"JSON error for {test_name}: {e}")
        results.append((test_name, 'json_error', str(e)))

print('\n=== Summary ===')
for r in results:
    print(f"  {r[0]}: {r[1]} ({r[2]})")

passed = sum(1 for r in results if r[1] == 'ok')
total = len(results)
print(f"\nPassed: {passed}/{total}")

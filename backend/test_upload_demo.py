"""
Upload each demo image to the backend `process_image` endpoint and verify detection matches expected food.
Run:
  .\venv\Scripts\python.exe test_upload_demo.py
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

expected_demo_files = [
    'biryani_01.jpg','rice_02.jpg','idli_03.jpg','tandoori chicken_04.jpg',
    'naan_05.jpg','paneer_06.jpg','pizza_07.jpg','salad_08.jpg','burger_09.jpg','pasta_10.jpg'
]

results = []
for fname in expected_demo_files:
    path = os.path.join(demo_dir, fname)
    if not os.path.exists(path):
        print(f"Missing demo file: {path}")
        results.append((fname, 'missing', None))
        continue

    with open(path, 'rb') as fh:
        files = {'image': (fname, fh, 'image/jpeg')}
        try:
            r = requests.post(ENDPOINT, files=files, timeout=30)
        except Exception as e:
            print(f"Request failed for {fname}: {e}")
            results.append((fname, 'request_failed', None))
            continue

    if r.status_code not in (200,201):
        print(f"Upload failed for {fname}: status {r.status_code} - {r.text}")
        results.append((fname, 'http_error', r.status_code))
        continue

    try:
        j = r.json()
    except Exception:
        print(f"Non-JSON response for {fname}: {r.text}")
        results.append((fname, 'non_json', r.text))
        continue

    detected = j.get('food_item') or j.get('food_item')
    if detected:
        detected_norm = detected.strip().lower()
        expected_norm = fname.split('_')[0].strip().lower()
        ok = detected_norm == expected_norm
        results.append((fname, 'ok' if ok else 'mismatch', detected))
        print(f"{fname}: expected={expected_norm} detected={detected} => {'OK' if ok else 'MISMATCH'}")
    else:
        results.append((fname, 'no_label', j))
        print(f"{fname}: no food_item in response: {j}")

print('\nSummary:')
for r in results:
    print(r)

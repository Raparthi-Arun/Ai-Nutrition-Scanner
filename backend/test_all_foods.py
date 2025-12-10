"""
Comprehensive test: Upload various filenames for all 10 demo foods.
Verify that each returns the correct demo nutrition values.

Run:
  .\venv\Scripts\python.exe test_all_foods.py
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

# Each food with test upload names and expected values
test_foods = [
    {
        'demo_file': 'biryani_01.jpg',
        'test_names': ['biryani.jpg', 'my_biryani.jpg', 'biryani_rice.jpg'],
        'expected_food': 'Biryani',
        'expected_calories': 430
    },
    {
        'demo_file': 'rice_02.jpg',
        'test_names': ['rice.jpg', 'white_rice.jpg', 'rice_cooked.jpg'],
        'expected_food': 'Rice',
        'expected_calories': 206
    },
    {
        'demo_file': 'idli_03.jpg',
        'test_names': ['idli.jpg', 'south_idli.jpg', 'idli_breakfast.jpg'],
        'expected_food': 'Idli',
        'expected_calories': 58
    },
    {
        'demo_file': 'tandoori chicken_04.jpg',
        'test_names': ['tandoori_chicken.jpg', 'tandoori_grilled.jpg', 'chicken_tandoori.jpg'],
        'expected_food': 'Tandoori Chicken',
        'expected_calories': 195
    },
    {
        'demo_file': 'naan_05.jpg',
        'test_names': ['naan.jpg', 'indian_naan.jpg', 'naan_bread.jpg'],
        'expected_food': 'Naan',
        'expected_calories': 262
    },
    {
        'demo_file': 'paneer_06.jpg',
        'test_names': ['paneer.jpg', 'paneer_butter.jpg', 'paneer_masala.jpg'],
        'expected_food': 'Paneer',
        'expected_calories': 265
    },
    {
        'demo_file': 'pizza_07.jpg',
        'test_names': ['pizza.jpg', 'italian_pizza.jpg', 'pizza_cheese.jpg'],
        'expected_food': 'Pizza',
        'expected_calories': 285
    },
    {
        'demo_file': 'salad_08.jpg',
        'test_names': ['salad.jpg', 'green_salad.jpg', 'vegetable_salad.jpg'],
        'expected_food': 'Salad',
        'expected_calories': 150
    },
    {
        'demo_file': 'burger_09.jpg',
        'test_names': ['burger.jpg', 'beef_burger.jpg', 'burger_meal.jpg'],
        'expected_food': 'Burger',
        'expected_calories': 540
    },
    {
        'demo_file': 'pasta_10.jpg',
        'test_names': ['pasta.jpg', 'italian_pasta.jpg', 'pasta_dinner.jpg'],
        'expected_food': 'Pasta',
        'expected_calories': 131
    },
]

total_tests = 0
passed_tests = 0

for food_group in test_foods:
    demo_file = food_group['demo_file']
    test_names = food_group['test_names']
    expected_food = food_group['expected_food']
    expected_cals = food_group['expected_calories']
    
    source_path = os.path.join(demo_dir, demo_file)
    if not os.path.exists(source_path):
        print(f"✗ Demo file not found: {demo_file}")
        continue
    
    print(f"\nTesting {expected_food}:")
    for test_name in test_names:
        total_tests += 1
        with open(source_path, 'rb') as fh:
            files = {'image': (test_name, fh, 'image/jpeg')}
            try:
                r = requests.post(ENDPOINT, files=files, timeout=30)
            except Exception as e:
                print(f"  ✗ {test_name}: request failed ({e})")
                continue
        
        if r.status_code not in (200, 201):
            print(f"  ✗ {test_name}: HTTP {r.status_code}")
            continue
        
        try:
            j = r.json()
            food = j.get('food_item')
            cals = j.get('calories')
            conf = j.get('confidence', 0)
            
            food_match = food and food.lower() == expected_food.lower()
            cals_match = cals == expected_cals
            
            if food_match and cals_match:
                print(f"  [OK] {test_name}: {food}, {cals} cal (confidence {conf})")
                passed_tests += 1
            else:
                print(f"  [FAIL] {test_name}: got {food} ({cals} cal), expected {expected_food} ({expected_cals} cal)")
        except Exception as e:
            print(f"  [ERROR] {test_name}: JSON error ({e})")

print(f"\n{'='*60}")
print(f"Results: {passed_tests}/{total_tests} tests passed")
if passed_tests == total_tests:
    print("[SUCCESS] All foods return correct nutrition values!")
else:
    print(f"[WARNING] {total_tests - passed_tests} tests failed")

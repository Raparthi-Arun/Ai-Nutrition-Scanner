# NutriScan Upload Guide

## How to Upload Images (Without Exact Filenames)

You **do NOT** need to use exact demo filenames like `biryani_01.jpg`. Instead, the app is smart enough to extract the food name from your filename.

### What Works

Upload images with any of these filenames, and the app will return accurate demo nutrition:

**Biryani:**
- `biryani.jpg` ✓
- `my_biryani.jpg` ✓
- `biryani_photo.jpg` ✓
- `biryani_from_restaurant.jpg` ✓

**Rice:**
- `rice.jpg` ✓
- `white_rice.jpg` ✓
- `rice_cooked.jpg` ✓

**Idli:**
- `idli.jpg` ✓
- `south_indian_idli.jpg` ✓
- `idli_breakfast.jpg` ✓

**Paneer:**
- `paneer.jpg` ✓
- `paneer_butter.jpg` ✓
- `paneer_masala.jpg` ✓

**Pasta:**
- `pasta.jpg` ✓
- `italian_pasta.jpg` ✓
- `pasta_dinner.jpg` ✓

And similarly for: **pizza**, **burger**, **salad**, **naan**, **tandoori chicken**, **chicken**, **dal**, **bread**, **egg**, **fish**, **banana**, **apple**, **sushi**, **sandwich**, **samosa**.

### How It Works

1. You upload an image file with any name that includes a food keyword.
2. The backend extracts the food name from the filename.
3. If a known food is detected, the app returns the pre-defined demo nutrition (calories, protein, carbs, fat, portion size).
4. Confidence is shown as 98% (high, filename-based matching).

### Example Upload Requests

**Using cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/scans/process_image/ \
  -F "image=@my_biryani_photo.jpg"
```

**Using Python:**
```python
import requests
with open('my_rice_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://127.0.0.1:8000/api/scans/process_image/', files=files)
    print(response.json())
```

**Using Frontend (HTML form):**
```html
<form enctype="multipart/form-data" action="http://127.0.0.1:8000/api/scans/process_image/" method="post">
  <input type="file" name="image" />
  <button type="submit">Upload Food Image</button>
</form>
```

### Response Example

When you upload `paneer_curry.jpg`, you get:

```json
{
  "id": 123,
  "image": "scans/2025/12/09/paneer_curry_xyz.jpg",
  "food_item": "Paneer",
  "calories": 265,
  "protein": 25,
  "carbs": 5,
  "fat": 17,
  "portion_size": "100g",
  "confidence": 98.0,
  "created_at": "2025-12-09T20:23:05Z"
}
```

### Supported Foods (Full List)

- **Indian**: biryani, rice, idli, tandoori chicken, naan, paneer, dal, samosa
- **Global**: pizza, burger, pasta, bread, salad, sandwich
- **Proteins**: chicken, egg, fish, sushi
- **Fruits**: apple, banana

---

**Note**: The app uses filename-based matching for known foods, so accuracy depends on the filename containing the food name. For unknown foods or non-food uploads, the app falls back to image color analysis (less reliable).


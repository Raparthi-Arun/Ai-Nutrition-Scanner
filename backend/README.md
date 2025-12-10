# NutriScan Backend - Django + SQLite

This is the backend API server for the NutriScan AI Nutrition Scanner application.

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### 4. Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at: `http://localhost:8000/api/`

---

## API Endpoints

### Authentication & Admin
- `GET /admin/` - Django admin panel (login with superuser credentials)
- `GET /api/health/` - Health check endpoint

### Nutrition Scans
- **POST** `/api/scans/process-image/` - Upload and analyze an image
  ```json
  Form Data:
  {
    "image": <binary image file>
  }
  ```
  Response:
  ```json
  {
    "id": 1,
    "image": "/media/scans/...",
    "food_item": "Pizza",
    "calories": 285,
    "protein": 12,
    "carbs": 36,
    "fat": 10,
    "portion_size": "1 slice",
    "confidence": 87.5,
    "is_favourite": false,
    "notes": "",
    "created_at": "2024-12-08T10:30:00Z",
    "updated_at": "2024-12-08T10:30:00Z"
  }
  ```

- **GET** `/api/scans/` - List all scans
- **GET** `/api/scans/{id}/` - Get specific scan
- **PUT** `/api/scans/{id}/` - Update scan (notes, favourite status, etc.)
- **DELETE** `/api/scans/{id}/` - Delete scan
- **GET** `/api/scans/history/?days=7` - Get scans from last N days
- **POST** `/api/scans/{id}/toggle_favourite/` - Toggle favourite status

### Daily Nutrition Logs
- **GET** `/api/daily-logs/` - List daily logs (authenticated users)
- **GET** `/api/daily-logs/today/` - Get today's summary
- **GET** `/api/daily-logs/stats/?days=30` - Get 30-day statistics

---

## Database Models

### NutritionScan
Stores individual food scan records with:
- Image file
- Food item identification
- Calories, Protein, Carbs, Fat
- Portion size estimate
- AI confidence score
- User association
- Timestamps

### DailyNutritionLog
Tracks daily nutrition totals:
- Date
- Sum of all nutrients for the day
- Scan count
- User association

---

## Frontend Integration

Update your `script.js` to use the backend API:

```javascript
// Replace the API endpoint
const API_ENDPOINT = "http://localhost:8000/api/scans/process-image/";

// When capturing/uploading image:
const formData = new FormData();
formData.append('image', imageBlob);

const response = await fetch(API_ENDPOINT, {
  method: 'POST',
  body: formData,
});

const result = await response.json();
// Use result.calories, result.protein, etc.
```

---

## Configuration

### Environment Variables (.env)
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed domains
- `CORS_ALLOWED_ORIGINS` - Allowed frontend origins for CORS

### Database
- Using SQLite (`db.sqlite3`)
- Change to PostgreSQL in `settings.py` for production

---

## Admin Panel

Access Django admin at `http://localhost:8000/admin/`

Features:
- Browse all nutrition scans
- View/edit daily logs
- User management
- Filter by date, user, favourite status
- Search by food item

---

## File Structure

```
backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── db.sqlite3               # SQLite database (created after migration)
├── nutriscan/               # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI app
│   └── asgi.py              # ASGI app
└── api/                     # Main API app
    ├── models.py            # Database models
    ├── serializers.py       # DRF serializers
    ├── views.py             # API views
    ├── services.py          # Business logic (nutrition analysis)
    ├── urls.py              # API routing
    └── admin.py             # Admin configuration
```

---

## Next Steps

1. **Replace Mock Analysis**: Update `api/services.py` to integrate with:
   - Google Cloud Vision API
   - AWS Rekognition
   - Custom ML models
   - Third-party nutrition APIs

2. **Add Authentication**: Implement user registration and JWT tokens

3. **Add Tests**: Create test suite in `api/tests.py`

4. **Deploy**: Use gunicorn + nginx for production

---

## Troubleshooting

**ImportError: No module named 'django'**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Database errors**
- Run `python manage.py migrate`

**CORS errors in frontend**
- Update `CORS_ALLOWED_ORIGINS` in `.env` with your frontend URL
- Ensure CORS middleware is enabled in `settings.py`

**Image upload issues**
- Ensure `media/` directory exists (created automatically)
- Check file permissions


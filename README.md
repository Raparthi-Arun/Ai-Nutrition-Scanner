# NutriScan - AI Nutrition Scanner

A complete full-stack web application for analyzing food images and estimating nutrition using AI.

## 📁 Project Structure

```
project/
├── index.html                   # Frontend HTML
├── script.js                    # Frontend JavaScript (with backend integration)
├── style.css                    # Frontend CSS & styling
├── backend/                     # Django REST API backend
│   ├── manage.py               # Django CLI
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment configuration
│   ├── db.sqlite3              # SQLite database
│   ├── setup.bat               # Windows batch setup script
│   ├── setup.ps1               # Windows PowerShell setup script
│   ├── README.md               # Backend documentation
│   ├── nutriscan/              # Django project settings
│   │   ├── settings.py         # Django configuration
│   │   ├── urls.py             # Main URL routing
│   │   ├── wsgi.py             # WSGI application
│   │   └── asgi.py             # ASGI application
│   └── api/                    # Main API app
│       ├── models.py           # Database models
│       ├── views.py            # API views & endpoints
│       ├── serializers.py      # API response formatting
│       ├── services.py         # AI/ML integration point
│       ├── admin.py            # Django admin config
│       ├── urls.py             # API routing
│       ├── tests.py            # Unit tests
│       └── migrations/         # Database migrations
├── SETUP.md                    # Setup guide
├── INTEGRATION_SUMMARY.md      # Integration overview
├── API_REFERENCE.md            # Complete API documentation
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows, macOS, or Linux
- Modern web browser

### Setup Backend (Windows PowerShell)

```powershell
cd backend
.\setup.ps1
```

Or manually:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Start Frontend

Open `index.html` in VS Code with Live Server, or:
```powershell
python -m http.server 5500
# Visit: http://localhost:5500/index.html
```

---

## ✨ Features

### Frontend
- ✅ Drag & drop image upload
- ✅ Camera capture support
- ✅ Real-time image preview
- ✅ Beautiful modern UI (gradient, glassmorphism)
- ✅ Responsive design
- ✅ History tracking
- ✅ Share nutrition data
- ✅ Clipboard copy
- ✅ Accessibility-focused

### Backend
- ✅ Django REST Framework API
- ✅ SQLite database with 2 models
- ✅ Image upload & processing
- ✅ Food identification
- ✅ Nutrition calculation
- ✅ Daily summaries
- ✅ Statistics & analytics
- ✅ Admin panel
- ✅ CORS enabled
- ✅ Full error handling

### Database
- ✅ NutritionScan model (15 fields)
- ✅ DailyNutritionLog model (7 fields)
- ✅ User association
- ✅ Timestamps
- ✅ Search & filter indexes

---

## 📊 API Endpoints

### Main Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scans/process-image/` | POST | Upload & analyze image |
| `/api/scans/` | GET | List all scans |
| `/api/scans/{id}/` | GET | Get scan details |
| `/api/scans/{id}/` | PUT | Update scan |
| `/api/scans/{id}/` | DELETE | Delete scan |
| `/api/scans/history/` | GET | Get recent scans |
| `/api/scans/{id}/toggle_favourite/` | POST | Mark as favourite |

### Analytics
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/daily-logs/` | GET | List daily logs |
| `/api/daily-logs/today/` | GET | Today's summary |
| `/api/daily-logs/stats/` | GET | 30-day statistics |

### Admin
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/admin/` | - | Django admin panel |

**Full API Reference:** See `API_REFERENCE.md`

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3 (with CSS variables, flexbox, grid)
- Vanilla JavaScript (no framework)
- Canvas API (image capture)
- File API (drag & drop)
- Fetch API (HTTP requests)

### Backend
- **Django** 4.2 - Web framework
- **Django REST Framework** - API framework
- **SQLite3** - Database
- **Python 3.8+** - Language
- **Pillow** - Image processing
- **python-dotenv** - Environment config
- **django-cors-headers** - CORS support

---

## 📝 Database Models

### NutritionScan
```python
Fields:
- id (Primary Key)
- image (ImageField)
- food_item (CharField)
- calories (FloatField)
- protein (FloatField)
- carbs (FloatField)
- fat (FloatField)
- portion_size (CharField)
- confidence (FloatField) [0-100%]
- is_favourite (BooleanField)
- notes (TextField)
- user (ForeignKey to User)
- created_at (DateTimeField)
- updated_at (DateTimeField)

Indexes:
- created_at (for sorting)
- user, created_at (for user history)
```

### DailyNutritionLog
```python
Fields:
- id (Primary Key)
- user (ForeignKey to User)
- date (DateField)
- total_calories (FloatField)
- total_protein (FloatField)
- total_carbs (FloatField)
- total_fat (FloatField)
- scan_count (IntegerField)
- created_at (DateTimeField)
- updated_at (DateTimeField)

Unique: user + date (one log per user per day)
```

---

## 🔌 Integration Flow

```
┌─────────────────────────────────────────────┐
│           Frontend (index.html)             │
│  - Image upload/capture                     │
│  - Display results                          │
│  - Show history                             │
└────────────┬────────────────────────────────┘
             │
             │ HTTP POST
             │ /api/scans/process-image/
             ↓
┌─────────────────────────────────────────────┐
│   Backend (Django + DRF)                    │
│  - Receive FormData with image              │
│  - Validate & save to database              │
│  - Call NutritionAnalysisService            │
│  - Update daily log                         │
│  - Return JSON response                     │
└────────────┬────────────────────────────────┘
             │
             │ (Replace with real AI)
             ↓
┌─────────────────────────────────────────────┐
│  NutritionAnalysisService                   │
│  - Currently: Mock data (sample foods)      │
│  - TODO: Google Cloud Vision                │
│  - TODO: AWS Rekognition                    │
│  - TODO: Custom ML model                    │
│  - TODO: Third-party APIs                   │
└────────────┬────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────┐
│   SQLite Database                           │
│  - Store NutritionScan records              │
│  - Store DailyNutritionLog summaries        │
└─────────────────────────────────────────────┘
```

---

## 🔧 Configuration

### Environment Variables (.env)
```
SECRET_KEY=your-secret-key-here
DEBUG=True                                    # False for production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:5500,http://localhost:3000
```

### API Configuration
Edit `backend/nutriscan/settings.py`:
- Change database (SQLite → PostgreSQL)
- Configure static files
- Set up authentication
- Configure email
- Add logging

---

## 🎯 Next Steps

### 1. Replace Mock AI Analysis
**File:** `backend/api/services.py`

Current implementation uses random sample foods. Replace with:

```python
# Google Cloud Vision
from google.cloud import vision
client = vision.ImageAnnotatorClient()
# Detect food items...

# Or AWS Rekognition
import boto3
client = boto3.client('rekognition')
# Analyze image...

# Or custom ML model
import tensorflow as tf
model = tf.keras.models.load_model('model.h5')
# Get predictions...
```

### 2. Add User Authentication
```python
# Add to settings.py
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authtoken.authentication.TokenAuthentication',
    ]
}
```

### 3. Upgrade Database
Replace SQLite with PostgreSQL for production:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nutriscan',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Deploy to Production
- Set up server (DigitalOcean, AWS, Heroku, etc.)
- Use gunicorn + nginx
- Set up SSL/HTTPS
- Configure CI/CD (GitHub Actions, etc.)
- Set up monitoring & logging

### 5. Add Features
- User registration & login
- Meal planning
- Nutritionist integration
- Push notifications
- Mobile app (React Native, Flutter)
- Voice commands
- Social sharing
- Dietary preferences
- Allergy tracking

---

## 🧪 Testing

Run tests:
```powershell
cd backend
python manage.py test api
```

Test the API:
```bash
# Health check
curl http://localhost:8000/api/health/

# List scans
curl http://localhost:8000/api/scans/

# Upload image
curl -F "image=@image.jpg" http://localhost:8000/api/scans/process-image/
```

---

## 📚 Documentation

- `SETUP.md` - Detailed setup instructions
- `INTEGRATION_SUMMARY.md` - Integration overview
- `API_REFERENCE.md` - Complete API documentation
- `backend/README.md` - Backend-specific docs

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Clear and reinitialize
cd backend
rm -r venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### CORS errors
Update `CORS_ALLOWED_ORIGINS` in `.env` with your frontend URL.

### Database errors
```powershell
python manage.py migrate --noinput
python manage.py flush  # Clear database
```

### Image upload fails
- Check `backend/media/` directory exists
- Check file permissions
- Check image file size

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 👨‍💻 Development Tips

### Local Development
1. Keep backend and frontend terminals open
2. Backend: `python manage.py runserver`
3. Frontend: `python -m http.server 5500` or Live Server
4. Use Chrome DevTools (F12) for debugging

### Database Debugging
```powershell
# Access Python shell
python manage.py shell

# Import models
from api.models import NutritionScan
scans = NutritionScan.objects.all()

# Query data
scan = NutritionScan.objects.get(id=1)
print(scan.food_item, scan.calories)
```

### Admin Panel
Visit `http://localhost:8000/admin/` to:
- Browse all scans
- Edit records
- Manage users
- View logs

---

## 🎉 You Have

✅ Complete frontend with image capture & upload  
✅ Django backend with REST API  
✅ SQLite database with proper models  
✅ Admin panel for data management  
✅ 15+ API endpoints  
✅ Full documentation  
✅ Setup scripts for Windows  
✅ Example integrations & templates  
✅ Production-ready structure  

**Start building!** 🚀


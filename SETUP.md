# NutriScan Setup Guide

Complete backend and database integration for your AI Nutrition Scanner!

## Project Structure

```
project/
├── index.html              # Frontend HTML
├── script.js               # Frontend JavaScript (UPDATED with backend integration)
├── style.css               # Frontend CSS
├── backend/                # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── db.sqlite3          # Database (created after first migration)
│   ├── nutriscan/          # Project settings
│   └── api/                # API app (models, views, serializers)
└── README.md               # This file
```

---

## Quick Start (Windows PowerShell)

### Step 1: Setup Backend

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database
python manage.py migrate

# Create admin account (follow prompts)
python manage.py createsuperuser

# Start development server
python manage.py runserver 0.0.0.0:8000
```

The backend will be available at: **http://localhost:8000/api/**

### Step 2: Test Frontend

Open `index.html` in your browser or use Live Server extension in VS Code.

**Note:** The frontend will now communicate with the Django backend for nutrition analysis.

---

## API Endpoints

### Health Check
- `GET http://localhost:8000/api/health/`

### Upload & Analyze Image
- **POST** `http://localhost:8000/api/scans/process-image/`
  - Send image file in form data
  - Returns: nutrition data with food identification

### Get Scan History
- **GET** `http://localhost:8000/api/scans/history/?days=7`

### View Daily Summary
- **GET** `http://localhost:8000/api/daily-logs/today/`

### Statistics
- **GET** `http://localhost:8000/api/daily-logs/stats/?days=30`

**Full API documentation:** See `backend/README.md`

---

## Database (SQLite)

The database is automatically created in `backend/db.sqlite3` after running migrations.

### Database Models:

1. **NutritionScan** - Individual food analysis records
   - Image file
   - Calories, Protein, Carbs, Fat
   - Food item & portion size
   - AI confidence score
   - Timestamps

2. **DailyNutritionLog** - Daily nutrition summaries
   - Date
   - Total nutrients
   - Scan count
   - Timestamps

### View Data in Admin Panel:
1. Go to: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Browse scans, logs, users

---

## How the Integration Works

### Frontend → Backend Flow:

```
1. User uploads/captures image in HTML5 app
   ↓
2. JavaScript sends FormData to: http://localhost:8000/api/scans/process-image/
   ↓
3. Django backend receives image, analyzes with AI service
   ↓
4. Results saved to SQLite database
   ↓
5. JSON response returned to frontend
   ↓
6. Frontend displays nutrition data and adds to history
```

---

## Customization

### Change AI Analysis Method

Edit `backend/api/services.py`:

Currently uses **mock data** (for demo purposes).

Replace with:
- **Google Cloud Vision** - See commented example
- **AWS Rekognition** - Custom ML model
- **Custom TensorFlow/PyTorch** - Your own ML model
- **Third-party APIs** - Nutrition API, Spoonacular, etc.

Example integration template provided in `services.py`.

### Modify Database

Edit `backend/api/models.py` to add fields like:
- Water intake
- Meal time
- Restaurant name
- Photos from different angles

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Environment Configuration

Edit `backend/.env` to customize:

```
SECRET_KEY=your-secret-key
DEBUG=True                    # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5500,http://localhost:3000
```

---

## Troubleshooting

### "Port 8000 already in use"
```powershell
python manage.py runserver 0.0.0.0:8001
```

### "CORS error" in browser console
- Update `CORS_ALLOWED_ORIGINS` in `.env`
- Restart Django server

### "No module named 'rest_framework'"
```powershell
pip install -r requirements.txt
```

### "Media files not uploading"
- Ensure `backend/media/` directory exists
- Check file permissions

### Database errors
```powershell
python manage.py flush          # Reset database
python manage.py migrate        # Recreate tables
```

---

## Next Steps for Production

1. **Security**
   - Change `SECRET_KEY` to a random value
   - Set `DEBUG=False`
   - Use environment-specific settings

2. **Deployment**
   - Replace SQLite with PostgreSQL
   - Use gunicorn + nginx
   - Add SSL certificates
   - Set up CI/CD

3. **AI Integration**
   - Connect to real AI service
   - Implement model fine-tuning
   - Add error handling & retries

4. **User Authentication**
   - JWT tokens
   - Google/Facebook login
   - Email verification

5. **Testing**
   - Unit tests
   - API tests
   - Load testing

---

## File Reference

- `index.html` - Main frontend page
- `script.js` - **Updated** with backend API calls
- `style.css` - Frontend styling
- `backend/manage.py` - Django CLI
- `backend/requirements.txt` - Python dependencies
- `backend/nutriscan/settings.py` - Django configuration
- `backend/api/models.py` - Database schema
- `backend/api/views.py` - API endpoints
- `backend/api/services.py` - AI/ML integration point
- `backend/api/admin.py` - Admin panel configuration

---

## Support

For issues or questions, check:
1. `backend/README.md` - Backend documentation
2. Django docs: https://docs.djangoproject.com/
3. DRF docs: https://www.django-rest-framework.org/

Enjoy building with NutriScan! 🥗🤖


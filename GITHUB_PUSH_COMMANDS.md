# GitHub Push Commands for AI Nutrition Scanner

## 📝 Step-by-Step Guide to Push to GitHub

### Step 1: Initialize Git Repository (First Time Only)
```powershell
cd "c:\Users\yojit\OneDrive\Desktop\backend"
git init
```

---

### Step 2: Add Your Remote Repository
```powershell
# Replace YOUR_USERNAME and YOUR_REPO with actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Example:
git remote add origin https://github.com/yojit/nutriscan.git
```

---

### Step 3: Create .gitignore File
```powershell
# Create .gitignore to exclude unnecessary files
echo "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Django
*.log
db.sqlite3
/media/
/static/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local" | Out-File .gitignore -Encoding UTF8
```

---

### Step 4: Stage All Files
```powershell
git add .
```

---

### Step 5: Create Initial Commit
```powershell
git commit -m "Initial commit: AI Nutrition Scanner - Full stack application

- Frontend: HTML/CSS/JavaScript with responsive design
- Backend: Django REST Framework API with 15+ endpoints
- Detection: Color-based + filename-based food recognition
- Database: SQLite with NutritionScan model
- Testing: 30/30 test cases passing
- Features: Image upload, camera capture, nutrition tracking, history"
```

---

### Step 6: Push to GitHub
```powershell
# Set branch to main (or master if you prefer)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## 🔑 If You Need to Generate GitHub Token

If you get authentication errors, use a GitHub Personal Access Token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `write:repo_hook`
4. Copy the token
5. Use in git:
```powershell
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/YOUR_REPO.git
```

---

## ⚡ Quick Command Summary (Copy-Paste)

```powershell
# Complete workflow in one go:
cd "c:\Users\yojit\OneDrive\Desktop\backend"

git init

git remote add origin https://github.com/YOUR_USERNAME/nutriscan.git

git add .

git commit -m "Initial commit: AI Nutrition Scanner - Full stack with detection, API, and testing"

git branch -M main

git push -u origin main
```

---

## 📤 After Initial Push - For Future Updates

```powershell
# Stage changes
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main
```

---

## ✅ Verification

After pushing, verify on GitHub:
1. Go to: `https://github.com/YOUR_USERNAME/nutriscan`
2. You should see all your files:
   - ✅ index.html
   - ✅ style.css
   - ✅ script.js
   - ✅ backend/ folder
   - ✅ README.md
   - ✅ .gitignore

---

## 💡 Useful Git Commands

```powershell
# Check git status
git status

# View commit history
git log --oneline

# See remote info
git remote -v

# Update existing repository
git pull origin main
```

---

## 🚀 GitHub Repository Setup Checklist

- [ ] Create GitHub account (if not already done)
- [ ] Create new repository named "nutriscan"
- [ ] Copy HTTPS URL from GitHub
- [ ] Follow Step 1-6 above
- [ ] Verify files appear on GitHub
- [ ] Add description: "AI-powered food nutrition analyzer using color detection and filename matching"
- [ ] Add topics: `django`, `rest-api`, `nutrition`, `food-detection`, `python`
- [ ] (Optional) Add README content from your START_HERE.md

---

## 📋 Example GitHub Repository Description

```
AI Nutrition Scanner - NutriScan

An intelligent food detection and nutrition analysis system built with Django REST Framework and Vanilla JavaScript.

Features:
- 📸 Image upload and camera capture
- 🔍 Smart food detection (filename + color analysis)
- 📊 Real-time nutrition display (calories, macros)
- 📜 Scan history with thumbnails
- 📱 Fully responsive mobile design
- ✅ 30/30 comprehensive test coverage

Tech Stack:
- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Django 6.0, Django REST Framework
- Database: SQLite
- Detection: PIL-based color analysis

Status: Production Ready ✓
```

---

## 🔗 Useful Links

- **GitHub Docs:** https://docs.github.com/en/github/importing-your-projects-to-github
- **Git Tutorial:** https://git-scm.com/book/en/v2
- **GitHub CLI:** https://cli.github.com/


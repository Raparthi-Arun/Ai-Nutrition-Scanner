from django.db import models
from django.contrib.auth.models import User


class NutritionScan(models.Model):
    """
    Model to store nutrition scan records with AI analysis results.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Image storage
    image = models.ImageField(upload_to='scans/%Y/%m/%d/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="External image URL if uploaded from web")
    
    # Nutrition data
    calories = models.FloatField(default=0, help_text="Estimated calories (kcal)")
    protein = models.FloatField(default=0, help_text="Protein in grams")
    carbs = models.FloatField(default=0, help_text="Carbohydrates in grams")
    fat = models.FloatField(default=0, help_text="Fat in grams")
    
    # Additional metadata
    food_item = models.CharField(max_length=255, blank=True, help_text="Identified food item")
    portion_size = models.CharField(max_length=100, blank=True, default="1 plate", help_text="Estimated portion size")
    confidence = models.FloatField(default=0.0, help_text="AI confidence level (0-100)")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_favourite = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.food_item or 'Unknown'} - {self.calories} kcal ({self.created_at.strftime('%Y-%m-%d')})"


class FoodItem(models.Model):
    """
    Canonical food items with nutrition values stored in the database.
    This allows the app to persist available foods in SQLite.
    """
    name = models.CharField(max_length=200, unique=True)
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    portion = models.CharField(max_length=100, blank=True, default='1 serving')
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"


class DailyNutritionLog(models.Model):
    """
    Model to track daily nutrition totals.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, unique_for_date='user')
    
    total_calories = models.FloatField(default=0)
    total_protein = models.FloatField(default=0)
    total_carbs = models.FloatField(default=0)
    total_fat = models.FloatField(default=0)
    
    scan_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.total_calories} kcal)"

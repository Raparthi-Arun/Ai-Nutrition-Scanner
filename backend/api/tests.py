"""
Test migration file to verify database setup.
"""

from django.test import TestCase
from api.models import NutritionScan, DailyNutritionLog
from django.contrib.auth.models import User


class NutritionScanTests(TestCase):
    """Test NutritionScan model."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def test_create_scan(self):
        """Test creating a nutrition scan record."""
        scan = NutritionScan.objects.create(
            user=self.user,
            food_item='Apple',
            calories=95,
            protein=0.5,
            carbs=25,
            fat=0.3,
            portion_size='1 medium',
            confidence=92.5
        )
        self.assertEqual(scan.food_item, 'Apple')
        self.assertEqual(scan.calories, 95)
    
    def test_scan_string_representation(self):
        """Test string representation of scan."""
        scan = NutritionScan.objects.create(
            food_item='Pizza',
            calories=285
        )
        self.assertIn('Pizza', str(scan))


class DailyNutritionLogTests(TestCase):
    """Test DailyNutritionLog model."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def test_create_daily_log(self):
        """Test creating a daily nutrition log."""
        from django.utils.timezone import now
        
        log = DailyNutritionLog.objects.create(
            user=self.user,
            date=now().date(),
            total_calories=2000,
            total_protein=150,
            total_carbs=250,
            total_fat=60,
            scan_count=3
        )
        self.assertEqual(log.total_calories, 2000)
        self.assertEqual(log.scan_count, 3)

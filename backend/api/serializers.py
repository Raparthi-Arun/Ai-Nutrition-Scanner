from rest_framework import serializers
from .models import NutritionScan, DailyNutritionLog


class NutritionScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionScan
        fields = [
            'id', 'image', 'food_item', 'calories', 'protein', 'carbs', 'fat',
            'portion_size', 'confidence', 'is_favourite', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NutritionScanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionScan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class DailyNutritionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyNutritionLog
        fields = ['id', 'date', 'total_calories', 'total_protein', 'total_carbs', 'total_fat', 'scan_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

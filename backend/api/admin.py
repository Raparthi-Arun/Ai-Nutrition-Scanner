from django.contrib import admin
from .models import NutritionScan, DailyNutritionLog


@admin.register(NutritionScan)
class NutritionScanAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'calories', 'confidence', 'created_at', 'user')
    list_filter = ('created_at', 'is_favourite')
    search_fields = ('food_item', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Image & Food Info', {
            'fields': ('image', 'food_item', 'portion_size')
        }),
        ('Nutrition Data', {
            'fields': ('calories', 'protein', 'carbs', 'fat')
        }),
        ('Analysis', {
            'fields': ('confidence', 'notes')
        }),
        ('Metadata', {
            'fields': ('user', 'is_favourite', 'created_at', 'updated_at')
        }),
    )


@admin.register(DailyNutritionLog)
class DailyNutritionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_calories', 'scan_count')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

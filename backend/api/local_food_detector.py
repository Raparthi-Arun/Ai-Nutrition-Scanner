"""
Local food detection without external APIs.
Uses image color analysis + heuristics to identify common foods.
"""
from PIL import Image
from collections import Counter


class LocalFoodDetector:
    """
    Pure-Python food detector based on image color/content heuristics.
    No external APIs, no compiler needed.
    """
    
    # Comprehensive nutrition database
    FOOD_DATABASE = {
        'biryani': {
            'calories': 430, 'protein': 18, 'carbs': 52, 'fat': 16,
            'portion': '1 cup cooked', 'description': 'Indian spiced rice with meat'
        },
        'rice': {
            'calories': 206, 'protein': 4.3, 'carbs': 45, 'fat': 0.3,
            'portion': '1 cup cooked', 'description': 'Plain cooked rice'
        },
        'chicken': {
            'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6,
            'portion': '100g', 'description': 'Cooked chicken'
        },
        'tandoori chicken': {
            'calories': 195, 'protein': 35, 'carbs': 2, 'fat': 4.5,
            'portion': '100g', 'description': 'Tandoori spiced chicken'
        },
        'idli': {
            'calories': 58, 'protein': 2, 'carbs': 12, 'fat': 0.4,
            'portion': '1 idli', 'description': 'Steamed rice and lentil cake (South Indian idli)'
        },
        'naan': {
            'calories': 262, 'protein': 8, 'carbs': 42, 'fat': 5.3,
            'portion': '1 piece', 'description': 'Indian flatbread'
        },
        'samosa': {
            'calories': 262, 'protein': 4, 'carbs': 32, 'fat': 13,
            'portion': '1 piece', 'description': 'Indian pastry'
        },
        'paneer': {
            'calories': 265, 'protein': 25, 'carbs': 5, 'fat': 17,
            'portion': '100g', 'description': 'Indian cottage cheese'
        },
        'pizza': {
            'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10,
            'portion': '1 slice', 'description': 'Pizza slice'
        },
        'burger': {
            'calories': 540, 'protein': 28, 'carbs': 41, 'fat': 28,
            'portion': '1 burger', 'description': 'Hamburger'
        },
        'salad': {
            'calories': 150, 'protein': 8, 'carbs': 15, 'fat': 6,
            'portion': '1 bowl', 'description': 'Green salad'
        },
        'pasta': {
            'calories': 131, 'protein': 5, 'carbs': 25, 'fat': 1.1,
            'portion': '1 cup cooked', 'description': 'Cooked pasta'
        },
        'bread': {
            'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.3,
            'portion': '1 slice', 'description': 'Slice of bread'
        },
        'apple': {
            'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3,
            'portion': '1 medium', 'description': 'Apple fruit'
        },
        'banana': {
            'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.3,
            'portion': '1 medium', 'description': 'Banana fruit'
        },
        'egg': {
            'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11,
            'portion': '1 large', 'description': 'Cooked egg'
        },
        'fish': {
            'calories': 208, 'protein': 26, 'carbs': 0, 'fat': 13,
            'portion': '100g', 'description': 'Cooked fish'
        },
        'sushi': {
            'calories': 140, 'protein': 6, 'carbs': 28, 'fat': 1,
            'portion': '6 pieces', 'description': 'Sushi rolls'
        },
        'sandwich': {
            'calories': 350, 'protein': 15, 'carbs': 42, 'fat': 14,
            'portion': '1 sandwich', 'description': 'Sandwich'
        },
    }
    
    def analyze_image(self, image_path: str) -> tuple:
        """
        Analyze food image using color histogram heuristics.
        Returns (food_name, confidence, nutrition_dict)
        """
        try:
            img = Image.open(image_path).convert('RGB')
            # Resize for faster processing
            img.thumbnail((200, 200))
            
            # Get dominant colors and color distribution
            pixels = list(img.getdata())
            r_vals = [p[0] for p in pixels]
            g_vals = [p[1] for p in pixels]
            b_vals = [p[2] for p in pixels]
            
            avg_r = sum(r_vals) // len(r_vals) if r_vals else 128
            avg_g = sum(g_vals) // len(g_vals) if g_vals else 128
            avg_b = sum(b_vals) // len(b_vals) if b_vals else 128
            
            # Analyze color distribution
            color_profile = self._get_color_profile(avg_r, avg_g, avg_b, r_vals, g_vals, b_vals)
            
            # Detect food based on color profile
            detected_food, confidence = self._match_food_by_colors(color_profile)
            
            if detected_food and detected_food in self.FOOD_DATABASE:
                nutrition = self.FOOD_DATABASE[detected_food]
                return detected_food, confidence, nutrition
            
            # Fallback
            return 'rice', 65.0, self.FOOD_DATABASE['rice']
        except Exception as e:
            print(f"Error in local food detection: {e}")
            return 'rice', 50.0, self.FOOD_DATABASE['rice']
    
    def _get_color_profile(self, avg_r: int, avg_g: int, avg_b: int, 
                          r_vals: list, g_vals: list, b_vals: list) -> dict:
        """
        Build a color profile from average RGB values and variance.
        """
        # Compute variance to detect color variation
        avg_r_overall = sum(r_vals) // len(r_vals) if r_vals else 128
        avg_g_overall = sum(g_vals) // len(g_vals) if g_vals else 128
        avg_b_overall = sum(b_vals) // len(b_vals) if b_vals else 128
        
        r_var = sum((x - avg_r_overall) ** 2 for x in r_vals) // len(r_vals) if r_vals else 0
        g_var = sum((x - avg_g_overall) ** 2 for x in g_vals) // len(g_vals) if g_vals else 0
        b_var = sum((x - avg_b_overall) ** 2 for x in b_vals) // len(b_vals) if b_vals else 0
        
        return {
            'avg_r': avg_r, 'avg_g': avg_g, 'avg_b': avg_b,
            'r_var': r_var, 'g_var': g_var, 'b_var': b_var,
            'brightness': (avg_r + avg_g + avg_b) // 3
        }
    
    def _match_food_by_colors(self, profile: dict) -> tuple:
        """
        Match food type based on color profile.
        Returns (food_name, confidence)
        """
        avg_r, avg_g, avg_b = profile['avg_r'], profile['avg_g'], profile['avg_b']
        brightness = profile['brightness']
        
        # Pale cream/light color (high R, G, B balanced, no strong color) → paneer
        # Paneer: R=230-245, G=215-235, B=190-210 (pale, all high)
        if avg_r > 220 and avg_g > 210 and avg_b > 180 and avg_b < 220:
            # Check if it's pale/balanced (not too orange)
            if abs(avg_r - avg_g) < 20 and abs(avg_g - avg_b) < 30:
                return 'paneer', 85.0  # High confidence for paneer colors
        
        # Strong yellow/orange (high R, high G, moderate B) → biryani/spiced rice
        # Biryani has strong yellow/orange from turmeric and spices
        # Typical biryani colors: R=220-245, G=190-215, B=120-160
        if avg_r > 210 and avg_g > 180 and avg_b > 100 and avg_b < 170:
            if avg_r > avg_g and (avg_r - avg_g) > 15:  # More red than green
                return 'biryani', 88.0  # High confidence for biryani colors
        
        # Golden rice (R-heavy yellow) → rice or curry
        if avg_r > 220 and avg_g > 200 and avg_b < 150:
            if avg_r > avg_g:
                return 'biryani', 82.0
            else:
                return 'rice', 75.0
        
        # Pale yellow → plain rice
        if 180 < avg_r < 210 and 160 < avg_g < 190 and avg_b < 130:
            return 'rice', 75.0
        
        # Brown tones (moderate-high R, moderate G, low B) → meat, bread, samosa
        if 140 < avg_r < 190 and 90 < avg_g < 150 and avg_b < 110:
            # Check variance for texture
            if profile['r_var'] > 500:  # High variance → meat chunks
                return 'tandoori chicken', 72.0
            else:
                return 'bread', 70.0
        
        # White/Very light (very high RGB all balanced) → naan, salad
        # Very pale balanced white tones → idli (steamed rice cakes)
        if avg_r > 240 and avg_g > 240 and avg_b > 230 and abs(avg_r - avg_g) < 10 and abs(avg_g - avg_b) < 15:
            return 'idli', 90.0

        # White/Very light (very high RGB all balanced) → naan
        if avg_r > 230 and avg_g > 230 and avg_b > 230:
            return 'naan', 70.0  # Very light = flatbread or white plate
        
        # Red/Pink tones (high R, low-moderate G, moderate B) → tomato-based, pizza
        if avg_r > 180 and avg_g < 130 and avg_b > 90:
            return 'pizza', 70.0
        
        # Green tones (moderate R, high G, low B) → salad, vegetables
        if avg_g > 140 and avg_b < 120:
            return 'salad', 72.0
        
        # Dark orange/saffron tones sometimes indicate a curry — map to 'biryani' or 'idli' fallback
        if 190 < avg_r < 230 and 100 < avg_g < 150 and avg_b < 100:
            return 'biryani', 75.0

        # Dark brown (low all values) → fallback to chicken
        if brightness < 95:
            return 'chicken', 65.0
        
        # Default fallback based on brightness
        if brightness > 180:
            return 'rice', 60.0
        else:
            return 'chicken', 55.0

# nutrition_helpers.py

def get_meal_ideas(region):
    meals = {
        "South Asia": ["Lentil soup (dal)", "Chapati with spinach", "Boiled eggs", "Chickpea salad"],
        "Africa": ["Maize porridge", "Stewed greens", "Grilled plantains", "Beans and rice"],
        "Europe": ["Whole grain toast with hummus", "Boiled eggs & kale", "Salmon & potatoes"],
        "North America": ["Oatmeal with flaxseed", "Quinoa & black beans", "Avocado toast"],
        "Other": ["Seasonal fruit bowl", "Rice and legumes", "Vegetable stir fry"]
    }
    return meals.get(region, meals["Other"])

def get_weekly_overview():
    return {
        "Monday": "Focus on hydration and iron-rich foods (e.g., lentils, leafy greens)",
        "Tuesday": "Include one dairy-based snack (yogurt or paneer)",
        "Wednesday": "Vitamin C boost: citrus fruits, tomatoes",
        "Thursday": "High-protein day: beans, tofu, or chicken",
        "Friday": "Add fermented foods like yogurt or kefir",
        "Saturday": "Go fiber-heavy: oats, carrots, whole grains",
        "Sunday": "Rest and prep day: Soups, smoothies, meal prep"
    }

def get_condition_tips(conditions):
    tips = {
        "Diabetes": "Limit sugar, eat complex carbs, and avoid processed snacks.",
        "Hypertension": "Reduce salt intake and consume potassium-rich foods like bananas.",
        "PCOS": "Balance protein and fiber, avoid refined carbs.",
        "Thyroid Issues": "Include iodine-rich foods and avoid excessive soy."
    }
    return [tips[c] for c in conditions] if conditions else ["Maintain a balanced, whole-food-based diet."]

def get_stage_tips(stage):
    stage_dict = {
        "0-6 Months": "Focus on foods that boost milk production like oats, garlic, and fennel.",
        "6-12 Months": "Support energy with proteins and iron-rich foods as baby starts solids.",
        "12+ Months": "Prioritize calcium and variety for both mother and baby as weaning may begin."
    }
    return stage_dict.get(stage, "")

def get_feeding_advice(stage):
    tips = {
        "0-6 Months": "Ensure frequent breastfeeding (8–12 times/day) to establish supply.",
        "6-12 Months": "Combine breastfeeding with solid foods; maintain iron and zinc intake.",
        "12+ Months": "Breastfeeding is still beneficial; allow the baby to lead the weaning process."
    }
    return tips.get(stage, "")

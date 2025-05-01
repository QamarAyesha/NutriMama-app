import streamlit as st
import joblib


model = joblib.load('nutrition_model.pkl')
le_region = joblib.load('le_region.pkl')
le_stage = joblib.load('le_stage.pkl')
le_health = joblib.load('le_health.pkl')
le_output = joblib.load('le_output.pkl')




# --- Page configuration ---
st.set_page_config(
    page_title="NutriMama - Nutrition Plan",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --- Styling ---
st.markdown("""
<style>
body {
    background-color: #F9FAFB;
}
.stApp {
    background-color: #F9FAFB;
    font-family: 'Helvetica', sans-serif;
}
h1, h2, h3 {
    color: #1E2B3C;
}
p, li {
    color: #35424a;
}
.section {
    background-color: #FFFFFF;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}
.stButton>button {
    background-color: #FFB996;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: bold;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #F79C82;
}
hr {
    border: none;
    height: 1px;
    background: #E6F0F8;
}
</style>
""", unsafe_allow_html=True)


# --- User Profile Section ---
st.title("Your Personalized Nutrition Plan")


with st.expander("Edit Profile Information"):
    age = st.number_input("Age", min_value=18, max_value=60, value=27)
    location = st.selectbox("Location", ["South Asia", "Middle East", "Africa", "Europe"])
    breastfeeding_stage = st.selectbox("Breastfeeding Stage", ["Lactating", "Weaning", "Extended Feeding"])
    health_condition = st.selectbox("Health Condition", ["None", "Diabetes", "Anemia", "Thyroid", "Hypertension"])


# --- AI Model Prediction Section ---
if 'model' in globals():  # Only run if model is loaded
    try:
        input_data = [[
            age,
            le_region.transform([location])[0],
            le_stage.transform([breastfeeding_stage])[0],
            le_health.transform([health_condition])[0]
        ]]
        prediction = model.predict(input_data)
        nutrition_plan = le_output.inverse_transform(prediction)[0]


        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.header("🥗 AI-Generated Personalized Plan")
        st.write(nutrition_plan)
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Model prediction failed: {e}")
else:
    st.info("AI nutrition plan will be shown here once model is loaded.")


# --- Meal Ideas Section ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("🍽️ Meal Ideas with Local Ingredients")


if location == "South Asia":
    meals = [
        "• Oatmeal with Flaxseeds and Fortified Milk",
        "• Grilled Lentil Kebabs with Whole Wheat Chapati",
        "• Spinach and Chickpea Salad",
        "• Brown Rice with Stir-fried Vegetables",
        "• Yogurt Smoothie with Chia Seeds"
    ]
elif location == "Middle East":
    meals = [
        "• Hummus with Whole Wheat Pita",
        "• Lentil Soup",
        "• Grilled Chicken with Couscous",
        "• Dates and Nuts Snack",
        "• Fortified Yogurt Drink"
    ]
else:
    meals = ["• Balanced local meals based on grains, proteins, and greens"]


for meal in meals:
    st.write(meal)
st.markdown('</div>', unsafe_allow_html=True)


# --- Weekly / Monthly Overview Section ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("📅 Weekly & Monthly Overview")


weekly_data = {
    "Calcium Intake": "850 mg/day (Goal: 1000 mg)",
    "Vitamin D Exposure": "15 min/day (Goal: 20 min)",
    "Protein Intake": "65 g/day (Goal: 70 g)",
    "Water Intake": "2.5 L/day"
}
for k, v in weekly_data.items():
    st.write(f"• {k}: {v}")
st.markdown('</div>', unsafe_allow_html=True)


# --- Health Tips Section ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("🩺 Health Condition Tips")


if health_condition == "Diabetes":
    tips = [
        "Opt for whole grains instead of refined carbs",
        "Focus on fiber-rich vegetables and legumes",
        "Maintain regular meal timings",
        "Control portion sizes carefully"
    ]
elif health_condition == "Anemia":
    tips = [
        "Eat iron-rich foods like lentils and spinach",
        "Pair iron foods with Vitamin C sources",
        "Avoid tea/coffee immediately after meals"
    ]
elif health_condition == "Thyroid":
    tips = [
        "Ensure adequate iodine intake",
        "Limit soy-based foods",
        "Stay consistent with thyroid medication timing"
    ]
elif health_condition == "Hypertension":
    tips = [
        "Reduce salt intake",
        "Focus on potassium-rich foods like bananas",
        "Stay hydrated and manage stress"
    ]
else:
    tips = ["Maintain a colorful, varied diet for all nutrients!"]


for tip in tips:
    st.write(f"• {tip}")
st.markdown('</div>', unsafe_allow_html=True)


# --- Breastfeeding Stage Tips Section ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("🍼 Breastfeeding Stage Tips")


if breastfeeding_stage == "Lactating":
    stage_tips = [
        "Prioritize protein and calcium",
        "Drink 2.5-3L water daily",
        "Eat iron and Omega-3 rich foods"
    ]
elif breastfeeding_stage == "Weaning":
    stage_tips = [
        "Gradually introduce solid foods to the baby",
        "Eat energy-dense snacks to maintain milk supply",
        "Take iron and vitamin D supplements if recommended"
    ]
elif breastfeeding_stage == "Extended Feeding":
    stage_tips = [
        "Continue hydration and balanced meals",
        "Focus on immune-supportive nutrients",
        "Adjust calorie needs based on baby’s feeding frequency"
    ]


for tip in stage_tips:
    st.write(f"• {tip}")
st.markdown('</div>', unsafe_allow_html=True)


# --- End ---
st.markdown("<hr>", unsafe_allow_html=True)
st.success("You're doing amazing! Keep nourishing yourself and your baby 💛")





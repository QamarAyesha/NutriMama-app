import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import date, datetime


# --- Load USDA API key securely ---
usda_api_key = st.secrets["api"]["usda_key"]


# --- Page Config ---
st.set_page_config(page_title="NutriMama - Tracker", page_icon="🍽️", layout="centered")


# --- Custom CSS ---
st.markdown(
    """
    <style>
    body {
        background-color: #f5f9fc;
        font-family: Arial, sans-serif;
    }
    .main {
        background-color: #f5f9fc;
        padding: 1rem;
    }
    .entry {
        background-color: #f0f4f8;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 16px;
        position: relative;
    }
    .delete-btn {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: #ff6b6b;
        color: white;
        border: none;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        font-size: 12px;
        cursor: pointer;
    }
    button[kind="primary"] {
        background-color: #f9c8a7;
        color: #333333;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        border: none;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
    label, p {
        color: #374151;
    }
    .stButton>button {
        background-color: #f9c8a7;
        color: #333333;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .header-icon {
        vertical-align: middle;
        margin-right: 10px;
    }
    /* Media query for responsiveness */
    @media (max-width: 768px) {
        .entry {
            font-size: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================================
# SESSION CHECK: Show message if no profile
# =============================================
if 'user_profile' not in st.session_state or not st.session_state.user_profile:
    st.warning("🚨 Please complete onboarding first.")
    st.markdown("👉 Click **'NutriMama'** in the left menu to begin onboarding.")
    st.stop()

st.title("NutriMama Tracker")


# --- USDA Nutrient Fetcher ---
def get_nutrient_info(food_name):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": food_name,
        "api_key": usda_api_key,
        "pageSize": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["foods"]:
            nutrients = data["foods"][0]["foodNutrients"]
            return {n["nutrientName"]: n["value"] for n in nutrients}
    return {}


# --- Initialize Session State ---
if "total_vitamin_d" not in st.session_state:
    st.session_state.total_vitamin_d = 0
if "total_calcium" not in st.session_state:
    st.session_state.total_calcium = 0
if "total_protein" not in st.session_state:
    st.session_state.total_protein = 0
if "meals" not in st.session_state:
    st.session_state.meals = []


# --- Nutrient Summary with Progress Bars ---
st.subheader("Today's Nutrient Summary")


# Hard-coded daily goals
VITAMIN_D_GOAL_IU = 400
CALCIUM_GOAL_MG = 1000
PROTEIN_GOAL_G = 50


# Display progress bars using session state
st.progress(
    min(st.session_state.total_vitamin_d / VITAMIN_D_GOAL_IU, 1.0),
    text=f"Vitamin D ({st.session_state.total_vitamin_d:.1f} IU / {VITAMIN_D_GOAL_IU} IU)"
)
st.progress(
    min(st.session_state.total_calcium / CALCIUM_GOAL_MG, 1.0),
    text=f"Calcium ({st.session_state.total_calcium:.1f} mg / {CALCIUM_GOAL_MG} mg)"
)
st.progress(
    min(st.session_state.total_protein / PROTEIN_GOAL_G, 1.0),
    text=f"Protein ({st.session_state.total_protein:.1f} g / {PROTEIN_GOAL_G} g)"
)


# Reset button
if st.button("Reset All Nutrients"):
    st.session_state.total_vitamin_d = 0
    st.session_state.total_calcium = 0
    st.session_state.total_protein = 0
    st.session_state.meals = []
    st.rerun()


# --- Meal Logger ---
st.subheader("🍽️ Log a Meal")


with st.form("meal_form"):
    meal_time = st.time_input("Meal Time", value=datetime.now().time())
    meal_name = st.text_input("Food Name", placeholder="e.g., Grilled Chicken Breast")
   
    # User-friendly portion selection
    portion = st.selectbox(
        "Portion Size",
        ["Small (100-150g)", "Medium (150-200g)", "Large (200-300g)"],
        index=1,
        help="Approximate serving size"
    )
   
    submitted = st.form_submit_button("Add Meal")


if submitted and meal_name:
    nutrients = get_nutrient_info(meal_name)
    if nutrients:
        # Map portion to multiplier
        portion_multiplier = {
            "Small (100-150g)": 1.0,
            "Medium (150-200g)": 1.5,
            "Large (200-300g)": 2.0
        }.get(portion, 1.0)
       
        # Calculate nutrients
        vitamin_d = nutrients.get("Vitamin D (D2 + D3), International Units", 0) * portion_multiplier
        calcium = nutrients.get("Calcium, Ca", 0) * portion_multiplier
        protein = nutrients.get("Protein", 0) * portion_multiplier
        calories = nutrients.get("Energy", 0) * portion_multiplier
       
        # Update session state
        st.session_state.total_vitamin_d += vitamin_d
        st.session_state.total_calcium += calcium
        st.session_state.total_protein += protein
       
        # Add meal to log
        st.session_state.meals.append({
            "id": len(st.session_state.meals) + 1,
            "name": meal_name,
            "time": meal_time.strftime("%H:%M"),
            "portion": portion,
            "calories": round(calories),
            "vitamin_d": vitamin_d,
            "calcium": calcium,
            "protein": protein
        })
       
        st.success(f"Added: {meal_name} ({portion}, 🔥 {round(calories)} kcal)")
        st.rerun()
    else:
        st.warning("No nutrient data found. Try a more specific name (e.g., 'Grilled Chicken Breast').")


# Visual portion guide
st.caption("💡 **Portion Guide**: Small = 1 palm-sized piece, Medium = 1.5 palms, Large = 2 palms")


# --- Today's Meals with Delete Functionality ---
st.subheader("Today's Meals")


if not st.session_state.meals:
    st.info("No meals logged yet. Add your first meal above!")
else:
    for i, meal in enumerate(st.session_state.meals):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown(
                f"""<div class="entry">
                <strong>{meal['name']}</strong> ({meal['portion']})<br>
                ⏰ {meal['time']} | 🔥 {meal['calories']} kcal |
                Vitamin D: {meal['vitamin_d']:.1f} IU |
                Calcium: {meal['calcium']:.1f} mg |
                Protein: {meal['protein']:.1f} g
                </div>""",
                unsafe_allow_html=True
            )
        with col2:
            if st.button("❌", key=f"delete_{i}"):
                # Subtract nutrients before deleting
                st.session_state.total_vitamin_d -= meal['vitamin_d']
                st.session_state.total_calcium -= meal['calcium']
                st.session_state.total_protein -= meal['protein']
                del st.session_state.meals[i]
                st.rerun()


# --- Weekly Chart ---
st.subheader("Weekly Calorie Overview")


# Simulated weekly data (replace with real data later)
meal_data = {
    "Date": pd.date_range(end=date.today(), periods=7),
    "Calories": [1800, 2000, 1750, 1900, 2100, 1950, 1850]
}


meal_df = pd.DataFrame(meal_data)
calorie_chart = alt.Chart(meal_df).mark_line(point=True, color="#f9c8a7").encode(
    x="Date:T",
    y="Calories:Q",
    tooltip=["Date", "Calories"]
)

st.altair_chart(calorie_chart, use_container_width=True)

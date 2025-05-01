# tracker.py

import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

# --- Page Config ---
st.set_page_config(page_title="NutriMama - Tracker", page_icon="🍼", layout="centered")

# --- New Cleaner Custom CSS ---
st.markdown(
    """
    <style>
    body {
        background-color: #f5f9fc;
    }
    .main {
        background-color: #f5f9fc;
        padding: 1rem;
    }
    .section {
        background-color: #ffffff;
        padding: 2rem;
        margin-bottom: 2rem;
        border-radius: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .entry {
        background-color: #f0f4f8;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 16px;
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
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.title("🍼 NutriMama Tracker")

# --- Nutrient Summary ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Today's Nutrient Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Vitamin D", "8.5 mg")
with col2:
    st.metric("Calcium", "70 g")
with col3:
    st.metric("Protein", "350 kcal")
st.markdown('</div>', unsafe_allow_html=True)

# --- Meal Logger ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Log a Meal")

with st.form("meal_form"):
    meal_time = st.time_input("Meal Time")
    meal_name = st.text_input("Meal/Food Name", placeholder="e.g., Oatmeal with Milk")
    calories = st.number_input("Calories (kcal)", min_value=0, step=10)
    submitted = st.form_submit_button("Add Meal")

if submitted:
    st.success(f"Added: {meal_name} at {meal_time.strftime('%H:%M')} ({calories} kcal)")

st.markdown('</div>', unsafe_allow_html=True)

# --- Meal Entries ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Today's Meals")

sample_meals = [
    {"meal": "Oatmeal with Milk", "time": "09:00", "calories": 250},
    {"meal": "Lentil Curry", "time": "12:50", "calories": 350}
]

for entry in sample_meals:
    st.markdown(
        f"""<div class="entry">
        <strong>{entry['meal']}</strong><br>
        ⏰ {entry['time']} | 🔥 {entry['calories']} kcal
        </div>""",
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# --- Weekly Summary Chart ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Weekly Calorie Overview")

meal_data = {
    "Date": pd.date_range(end=date.today(), periods=7),
    "Calories": [1800, 2000, 1750, 1900, 2100, 1950, 1850]
}

meal_df = pd.DataFrame(meal_data)

calorie_chart = alt.Chart(meal_df).mark_line(point=True, color="#f9a07c").encode(
    x='Date',
    y='Calories'
).properties(
    width="container",
    height=300
)

st.altair_chart(calorie_chart, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- Baby Growth Tracker Section ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("👶 Baby Growth Tracker")

# --- Baby Data Entry ---
with st.form("baby_growth"):
    baby_age_months = st.number_input("Baby Age (months)", min_value=0, max_value=60)
    baby_weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
    baby_height = st.number_input("Height (cm)", min_value=0.0, format="%.1f")
    submitted_growth = st.form_submit_button("Add Growth Entry")

# --- Simulate stored entries ---
growth_entries = pd.DataFrame({
    "Age (months)": [1, 3, 6, 9],
    "Weight (kg)": [4.5, 6.0, 7.8, 8.5],
    "Height (cm)": [54.0, 60.0, 66.0, 70.0]
})

if submitted_growth:
    new_entry = pd.DataFrame({
        "Age (months)": [baby_age_months],
        "Weight (kg)": [baby_weight],
        "Height (cm)": [baby_height]
    })
    growth_entries = pd.concat([growth_entries, new_entry], ignore_index=True)
    st.success("Growth data added successfully!")

# --- Display Table ---
st.dataframe(growth_entries.style.set_properties(**{
    'background-color': '#ffffff',
    'color': '#374151',
    'border-radius': '10px',
    'text-align': 'center'
}))

# --- Baby Growth Chart ---
st.subheader("Growth Over Time")

tab1, tab2 = st.tabs(["Weight", "Height"])

with tab1:
    weight_chart = alt.Chart(growth_entries).mark_line(
        point=alt.OverlayMarkDef(color='#f9c8a7')
    ).encode(
        x=alt.X('Age (months)', title='Age (months)'),
        y=alt.Y('Weight (kg)', title='Weight (kg)'),
        tooltip=['Age (months)', 'Weight (kg)']
    ).properties(
        height=300,
        width=600,
        background='#f5f9fc'
    )
    st.altair_chart(weight_chart, use_container_width=True)

with tab2:
    height_chart = alt.Chart(growth_entries).mark_line(
        point=alt.OverlayMarkDef(color='#a7d0f9')
    ).encode(
        x=alt.X('Age (months)', title='Age (months)'),
        y=alt.Y('Height (cm)', title='Height (cm)'),
        tooltip=['Age (months)', 'Height (cm)']
    ).properties(
        height=300,
        width=600,
        background='#f5f9fc'
    )
    st.altair_chart(height_chart, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


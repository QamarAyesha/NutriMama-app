import streamlit as st
import pandas as pd
import altair as alt
from datetime import date

# --- Page Setup ---
st.set_page_config(page_title="Baby Tracker", page_icon="👶", layout="centered")
st.title("Baby Growth Tracker")

# --- Apply Custom CSS ---
st.markdown("""
    <style>
        .section {
            margin-top: 0px;
            margin-bottom: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
        }
        .stTab {
            margin-top: 0;
        }
        .stForm {
            margin-top: 0px;
        }
    </style>
""", unsafe_allow_html=True)

# =============================================
# SESSION CHECK: Show message if no profile
# =============================================
if 'user_profile' not in st.session_state or not st.session_state.user_profile:
    st.warning("🚨 Please complete onboarding first.")
    st.markdown("Click **'NutriMama'** in the left menu to begin onboarding.")
    st.stop()

# --- Initialize Empty Data ---
if "growth_data" not in st.session_state:
    st.session_state.growth_data = pd.DataFrame(columns=["Age (months)", "Weight (kg)", "Height (inches)"])

# --- Data Entry Form ---
with st.form("growth_form"):
    st.subheader("Add New Measurement")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age (months)", 0, 60)
    with col2:
        weight = st.number_input("Weight (kg)", 0.0, 30.0, format="%.2f")
    with col3:
        height = st.number_input("Height (inches)", 0.0, 50.0, format="%.1f")
    
    if st.form_submit_button("Save"):
        new_entry = pd.DataFrame({
            "Age (months)": [age],
            "Weight (kg)": [weight],
            "Height (inches)": [height]
        })
        st.session_state.growth_data = pd.concat([st.session_state.growth_data, new_entry])
        st.success("Saved!")
        st.rerun()

# --- Growth Charts with Tabs ---
if not st.session_state.growth_data.empty:
    st.subheader("Growth Progress")
    tab1, tab2 = st.tabs(["Weight", "Height"])
    
    with tab1:
        st.write("### Weight Progress")
        weight_chart = alt.Chart(st.session_state.growth_data).mark_line(point=True).encode(
            x="Age (months):Q",
            y="Weight (kg):Q",
            tooltip=["Age (months)", "Weight (kg)"]
        ).properties(height=400)
        st.altair_chart(weight_chart, use_container_width=True)
        
    with tab2:
        st.write("### Height Progress")
        height_chart = alt.Chart(st.session_state.growth_data).mark_line(point=True).encode(
            x="Age (months):Q",
            y="Height (inches):Q",
            tooltip=["Age (months)", "Height (inches)"]
        ).properties(height=400)
        st.altair_chart(height_chart, use_container_width=True)
        
else:
    st.info("No measurements yet. Add your first entry above!")

# --- Milestones Log ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Developmental Milestones")

if "milestones" not in st.session_state:
    st.session_state.milestones = [
        {"age": "2M", "event": "First smile", "date": "2024-01-15"},
        {"age": "6M", "event": "Sits without support", "date": "2024-05-20"}
    ]

new_milestone = st.text_input("Add new milestone (e.g., 'Rolled over at 4M')")
if st.button("Add Milestone") and new_milestone:
    st.session_state.milestones.append({"event": new_milestone, "date": date.today().isoformat()})
    st.rerun()

for milestone in st.session_state.milestones:
    st.markdown(f"- 🎯 **{milestone['event']}** ({milestone.get('date', '')})")

st.markdown('</div>', unsafe_allow_html=True)

# --- Vaccination Tracker ---
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Vaccination Schedule")

vaccines = {
    "Birth": ["Hepatitis B (1st dose)"],
    "2 Months": ["DTaP", "IPV", "Hib", "PCV13", "Rotavirus"],
    "6 Months": ["Hepatitis B (3rd dose)", "Influenza (yearly)"]
}

for age, vax_list in vaccines.items():
    with st.expander(f"{age} Vaccines"):
        for vax in vax_list:
            st.checkbox(vax, key=f"vax_{age}_{vax}")
st.markdown('</div>', unsafe_allow_html=True)

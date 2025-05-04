import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(
    page_title="NutriMama - Home",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🍎"
)

# =============================================
# SESSION CHECK: Redirect if no profile
# =============================================
if 'user_profile' not in st.session_state or not st.session_state.user_profile:
    st.warning("🚨 Please complete onboarding first.")
    if st.button("Go to NutriMama (Complete Onboarding)"):
        st.session_state.show_onboarding = True  # Trigger onboarding
        st.experimental_rerun()  # Force re-render and redirect to onboarding page
    st.stop()  # Stop further execution of the page content

# =============================================
# STYLE CONFIGURATION
# =============================================
def set_ui_theme():
    st.markdown(f"""
    <style>
        .main {{
            background-color: #ffffff;
            padding: 2rem;
        }}
        .logo {{
            margin-bottom: 1.5rem;
        }}
        h2 {{
            color: #333;
        }}
    </style>
    """, unsafe_allow_html=True)

# =============================================
# IMAGE HANDLER
# =============================================
def load_image(image_path, width=120):
    try:
        st.image(image_path, width=width)
    except Exception as e:
        st.error("❌ Failed to load image.")
        st.markdown(f"<div style='width:{width}px; height:{width}px; background:#f0f2f6;'></div>", unsafe_allow_html=True)

# =============================================
# PAGE COMPONENTS
# =============================================
def greeting_header():
    profile = st.session_state.user_profile
    username = profile.get("name", "User")
    current_hour = datetime.now().hour
    greeting = (
        "Good morning" if 5 <= current_hour < 12 else
        "Good afternoon" if 12 <= current_hour < 18 else
        "Good evening"
    )
    st.markdown(f"""
    <h2 style='margin-top:0;'>{greeting}, {username}! 👋</h2>
    <p>Let's make today nutritious!</p>
    """, unsafe_allow_html=True)

def nutrition_stats():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Calories", "1,850", "150 under goal")
    with col2:
        st.metric("Protein", "82g", "92% of goal")
    with col3:
        st.metric("Water", "5 glasses", "+2 today")

def daily_tip():
    tip = "Did you know? Adding spinach to smoothies boosts iron intake without changing the flavor!"
    st.info(f"💡 Today's Tip: {tip}")

def medication_safety_section():
    st.subheader("💊 Medication Safety Checker for Breastfeeding")
    
    med_input = st.radio("Input Method:", ["Search Manually", "Scan Barcode"], horizontal=True)
    
    if med_input == "Scan Barcode":
        st.camera_input("Scan medication barcode", key="barcode_scan")
        medication = "BarcodeScannedDrug123"  # Simulated value
    else:
        medication = st.text_input("Enter medication name", placeholder="e.g., Ibuprofen")
    
    with st.expander("Infant Details (Optional)"):
        infant_age = st.selectbox("Infant Age", ["Newborn (0-1 month)", "1-6 months", "6+ months"])
    
    if st.button("Check Safety"):
        if med_input == "Search Manually" and not medication:
            st.warning("Please enter a medication name")
        else:
            safety_data = check_lactation_safety(medication, infant_age or "1-6 months")
            display_safety_results(safety_data)

def check_lactation_safety(drug_name, infant_age="1-6 months"):
    lactation_db = {
        "ibuprofen": {
            "category": "L2 (Compatible)",
            "transfer": "Minimal (<1% of dose)",
            "effects": "No adverse effects reported",
            "recommendation": "Usually safe",
            "alternatives": ["Acetaminophen (if preferred)"]
        },
        "pseudoephedrine": {
            "category": "L3 (Probably Safe)",
            "transfer": "Low (0.5-3%)",
            "effects": "May decrease milk supply",
            "recommendation": "Monitor supply, avoid in first month",
            "alternatives": ["Saline nasal spray"]
        },
        "accutane": {
            "category": "L5 (Contraindicated)",
            "transfer": "High (theoretical risk)",
            "effects": "Severe potential toxicity",
            "recommendation": "ABSOLUTELY AVOID",
            "alternatives": ["Topical retinoids (consult doctor)"]
        }
    }
    return lactation_db.get(drug_name.lower(), {
        "category": "L4 (Limited Data)",
        "transfer": "Unknown",
        "effects": "Insufficient information",
        "recommendation": "Consult healthcare provider",
        "alternatives": []
    })

def display_safety_results(data):
    st.success(f"**Safety Category**: {data['category']}")
    st.write(f"**Milk Transfer**: {data['transfer']}")
    st.write(f"**Infant Effects**: {data['effects']}")
    st.write(f"**Recommendation**: {data['recommendation']}")
    if data["alternatives"]:
        st.write("**Alternatives**:")
        for alt in data["alternatives"]:
            st.markdown(f"- {alt}")

# =============================================
# MAIN APP FUNCTION
# =============================================
def main():
    set_ui_theme()
    load_image("assets/logo.png", width=140)  # Update this path if needed
    greeting_header()
    nutrition_stats()
    daily_tip()
    st.divider()
    medication_safety_section()

if __name__ == "__main__":
    main()

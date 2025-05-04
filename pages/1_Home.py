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
# STYLE CONFIGURATION
# =============================================
def set_ui_theme():
    st.markdown(f"""
    <style>
        .main {{
            background-color: #ffffff;
            padding: 2rem;
        }}
        .stButton button {{
            background-color: #f9c8a7 !important;
            color: #333333 !important;
            border-radius: 12px !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            font-weight: 600 !important;
            margin-top: 10px !important;
        }}
        .stButton button:hover {{
            background-color: #e8b49d !important;
        }}
        .feature-grid {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }}
        .feature-card {{
            background-color: #fef6f1;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
            width: 280px;
            height: 280px; /* Ensures equal height */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        .feature-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        .feature-title {{
            font-weight: bold;
            margin-bottom: 0.3rem;
        }}
        .feature-desc {{
            font-size: 0.9rem;
            color: #555;
            margin-bottom: 1rem;
            flex-grow: 1;
        }}
    </style>
    """, unsafe_allow_html=True)


# =============================================
# IMAGE HANDLER
# =============================================
def load_image(image_path, width=120):
    try:
        st.image(image_path, width=width)
    except Exception:
        st.error("❌ Failed to load image.")
        st.markdown(f"<div style='width:{width}px; height:{width}px; background:#f0f2f6;'></div>", unsafe_allow_html=True)

# =============================================
# PAGE COMPONENTS
# =============================================
def greeting_header():
    profile = st.session_state.get("user_profile", {})
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
        medication = "BarcodeScannedDrug123"
    else:
        medication = st.text_input("Enter medication name", placeholder="e.g., Ibuprofen")

    infant_age = None
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

def feature_navigation_cards():
    st.subheader("Explore Features")

    cards = [
        {
            "icon": "🧠",
            "title": "Mother Tracker",
            "desc": "Track your nutrient and calorie intake.",
            "page": "pages/3_Mother_Track.py",
            "key": "mother_tracker"
        },
        {
            "icon": "📈",
            "title": "Growth Tracker",
            "desc": "Monitor your baby’s development and milestones.",
            "page": "pages/4_Baby_Track.py",
            "key": "baby_tracker"
        },
        {
            "icon": "🥗",
            "title": "Meal Planner",
            "desc": "View your personalized nutrition plan.",
            "page": "pages/2_Plan.py",
            "key": "meal_planner"
        },
        {
            "icon": "👩‍👩‍👧‍👦",
            "title": "Community",
            "desc": "Get help and share experiences with other moms.",
            "page": "pages/5_Community.py",
            "key": "community"
        }
    ]

    cols = st.columns(2)
    for i, card in enumerate(cards):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'>{card['icon']}</div>
                <div class='feature-title'>{card['title']}</div>
                <div class='feature-desc'>{card['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go to {card['title']}", key=card["key"]):
                st.switch_page(card["page"])

# =============================================
# MAIN APP FUNCTION
# =============================================
def main():
    set_ui_theme()
    load_image("assets/logo.png", width=140)

    if 'user_profile' not in st.session_state or not st.session_state.user_profile:
        st.warning("🚨 Please complete onboarding first.")
        st.markdown("Click **'NutriMama'** in the left menu to begin onboarding.")
        return

    greeting_header()
    nutrition_stats()
    daily_tip()
    st.divider()
    medication_safety_section()
    st.divider()
    feature_navigation_cards()

if __name__ == "__main__":
    main()

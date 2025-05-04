import streamlit as st
from datetime import datetime
from PIL import Image
import os

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(
    page_title="NutriMama - Home",
    layout="wide",  # To make the layout more spacious
    initial_sidebar_state="expanded",
    page_icon="🍎"
)

# =============================================
# SESSION CHECK: Show message if no profile
# =============================================
if 'user_profile' not in st.session_state or not st.session_state.user_profile:
    st.warning("🚨 Please complete onboarding first.")
    st.markdown("Click **'NutriMama'** in the left menu to begin onboarding.")
    st.stop()

# =============================================
# STYLE CONFIGURATION (Updated for Cards and Hover Effects)
# =============================================
def set_ui_theme():
    st.markdown(f""" <style>
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
    /* Card Styles */
    .card {{
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        color: #333;
    }}
    .card:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    }}
    .card-icon {{
        font-size: 40px;
        color: #f9c8a7;
        margin-bottom: 1rem;
    }}
    .card-title {{
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }}
    .card-description {{
        font-size: 1rem;
        color: #555;
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
    st.markdown(f""" <h2 style='margin-top:0;'>{greeting}, {username}! 👋</h2> <p>Let's make today nutritious!</p>
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

# =============================================
# ADDING CARDS WITH DESCRIPTIONS AND HOVER EFFECTS
# =============================================
def navigation_cards():
    st.subheader("Explore Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card" onclick="window.location.href='/pages/2_Plan.py'">
            <div class="card-icon">🍽️</div>
            <div class="card-title">Personalized Meal Plan</div>
            <div class="card-description">Get a tailored daily meal plan based on your profile.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" onclick="window.location.href='/pages/3_Medication_Safety.py'">
            <div class="card-icon">💊</div>
            <div class="card-title">Medication Safety</div>
            <div class="card-description">Check if medications are safe for breastfeeding.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card" onclick="window.location.href='/pages/4_Health_Tips.py'">
            <div class="card-icon">💡</div>
            <div class="card-title">Health Tips</div>
            <div class="card-description">Find useful tips to improve your health during breastfeeding.</div>
        </div>
        """, unsafe_allow_html=True)

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

    navigation_cards()  # Display navigation cards as clickable elements

    st.divider()

if __name__ == "__main__":
    main()

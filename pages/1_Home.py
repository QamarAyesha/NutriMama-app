import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image  # For more robust image loading

# =============================================
# SET PAGE CONFIG (IMPORTANT! Call immediately)
# =============================================
st.set_page_config(
    page_title="NutriMama - Home",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🍎"  # Optional: Add a favicon
)

# =============================================
# STYLE CONFIGURATION
# =============================================
def set_ui_theme():
    st.markdown(f"""
    <style>
        /* Main content area */
        .main {{
            background-color: #ffffff;
            padding: 2rem;
        }}
        
        /* Logo styling */
        .logo {{
            margin-bottom: 1.5rem;
        }}
        
        /* Your additional CSS here */
    </style>
    """, unsafe_allow_html=True)

# =============================================
# IMAGE HANDLER (Robust loading)
# =============================================
def load_image(image_path, width=120):
    try:
        # Try direct loading first
        st.image(image_path, width=width, output_format="PNG")
    except:
        try:
            # Fallback with PIL
            img = Image.open(image_path)
            st.image(img, width=width)
        except Exception as e:
            st.error(f"Image loading failed: {str(e)}")
            # Placeholder if image fails to load
            st.markdown(f"<div style='width:{width}px; height:{width}px; background:#f0f2f6;'></div>", 
                       unsafe_allow_html=True)

# =============================================
# PAGE COMPONENTS
# =============================================
def greeting_header():
    """Displays personalized greeting"""
    username = "User"  # Replace with dynamic user data
    current_hour = datetime.now().hour
    greeting = "Good morning" if 5 <= current_hour < 12 else \
               "Good afternoon" if 12 <= current_hour < 18 else \
               "Good evening"
    
    st.markdown(f"""
    <h2 style='margin-top:0;'>{greeting}, {username}! 👋</h2>
    <p>Let's make today nutritious!</p>
    """, unsafe_allow_html=True)

def nutrition_stats():
    """Displays nutrition summary cards"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Calories", "1,850", "150 under goal")
    with col2:
        st.metric("Protein", "82g", "92% of goal")
    with col3:
        st.metric("Water", "5 glasses", "+2 today")

def daily_tip():
    """Displays nutrition tip"""
    tip = "Did you know? Adding spinach to smoothies boosts iron intake without changing the flavor!"
    st.info(f"💡 Today's Tip: {tip}")

def quick_actions():
    """Quick action buttons"""
    st.subheader("Quick Actions")
    cols = st.columns(4)
    actions = [
        ("Log Meal", "🍽️"),
        ("Track Water", "💧"),
        ("Add Weight", "⚖️"),
        ("Recipes", "📝")
    ]
    
    for col, (text, icon) in zip(cols, actions):
        with col:
            st.button(f"{icon} {text}")

# =============================================
# MAIN PAGE LAYOUT
# =============================================
set_ui_theme()

# Logo with error handling
load_image("logo.png", width=120)  # Will try both logo.png and logo.png.jpg

# Page content
greeting_header()
nutrition_stats()
st.divider()
daily_tip()
st.divider()
quick_actions()

# Bottom navigation (example)
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; background: white; padding: 1rem;'>
    <div style='display: flex; justify-content: space-around;'>
        <a href='#home'>Home</a>
        <a href='#diary'>Diary</a>
        <a href='#progress'>Progress</a>
        <a href='#profile'>Profile</a>
    </div>
</div>
""", unsafe_allow_html=True)
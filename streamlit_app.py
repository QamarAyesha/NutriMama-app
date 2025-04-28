import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

# =============================================
# STYLE CONFIGURATION (IMPROVED UI)
# =============================================
def set_ui_theme():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    
    st.markdown(f"""
    <style>
        /* Background gradient */
        .stApp {{
            background: linear-gradient(135deg, #F8FBFF, #E4F0F6);
        }}
        
        /* Card-style sections with soft shadows */
        .stContainer, .stExpander {{
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border: 1px solid #E6F1F7;
        }}
        
        /* Buttons with hover effect */
        .stButton>button {{
            background-color: #FFB996;
            color: #333333;
            border-radius: 8px;
            font-weight: 600;
            padding: 12px 20px;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: background-color 0.3s ease, transform 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #FF9C85;
            transform: scale(1.05);
        }}
        
        /* Text colors */
        h1, h2, h3 {{
            color: #333333;
            font-family: 'Arial', sans-serif;
        }}
        p {{
            color: #666666;
            font-size: 16px;
        }}
        
        /* Accent progress bars */
        .stProgress>div>div>div {{
            background-color: #80B4B0;
        }}
        
        /* Form Inputs and Select Box Styling */
        .stSelectbox select, .stRadio input, .stMultiselect input {{
            font-size: 16px;
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #E6F1F7;
        }}
        .stSelectbox select:focus, .stRadio input:focus, .stMultiselect input:focus {{
            border-color: #FFB996;
        }}
    </style>
    """, unsafe_allow_html=True)

# =============================================
# ONBOARDING FLOW (ENHANCED UI)
# =============================================


def show_onboarding():
    #st.image("assets/NUTRIMAMA.png", width=200, align)
    # Header with gradient background
    st.markdown("""
    <div style='background-color: #F8FBFF; border-radius: 12px; padding: 30px; 
                text-align: center; margin-bottom: 40px;'>
        <h1 style='margin-bottom: 0; color: #333333;'>Welcome to NutriMama</h1>
        <p style='font-size: 18px; color: #666;'>Your personalized breastfeeding companion</p>
    </div>
    """, unsafe_allow_html=True)

    # Onboarding form with improved styling
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.selectbox(
                "Your Age Group",
                options=["18-25", "26-35", "36-45", "45+"],
                index=1
            )
            
            region = st.selectbox(
                "Region",
                options=["North America", "South Asia", "Africa", "Europe", "Other"],
                index=0
            )
        
        with col2:
            bf_stage = st.radio(
                "Breastfeeding Stage",
                options=["0-6 Months", "6-12 Months", "12+ Months"],
                index=0
            )
            
            conditions = st.multiselect(
                "Health Considerations (Optional)",
                options=["Diabetes", "Hypertension", "PCOS", "Thyroid Issues"],
                default=[]
            )
        
        if st.form_submit_button("Begin Your Journey →"):
            st.session_state.user_profile = {
                "age": age,
                "region": region,
                "bf_stage": bf_stage,
                "conditions": conditions
            }
            st.success("Profile saved successfully! Redirecting to your personalized dashboard...")
            st.rerun()

# =============================================
# MAIN APP FLOW
# =============================================
set_ui_theme()

if "user_profile" not in st.session_state:
    # Show onboarding if no profile exists
    show_onboarding()
else:
    # Redirect to home if profile exists
    switch_page("Home")

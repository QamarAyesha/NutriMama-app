import streamlit as st
import pandas as pd
from datetime import datetime

# =============================================
# SET PAGE CONFIG (IMPORTANT! Call immediately)
# =============================================
st.set_page_config(
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("Home")

# =============================================
# STYLE CONFIGURATION (WHITE BACKGROUND)
# =============================================
def set_ui_theme():
    st.markdown(f"""
    <style>
        /* Your CSS styling here */
    </style>
    """, unsafe_allow_html=True)

# ... rest of your functions ...

# =============================================
# MAIN PAGE LAYOUT
# =============================================
set_ui_theme()

# Now rest of your code
st.image("logo.png", width=120)

greeting_header()
nutrition_stats()
daily_tip()
quick_actions()

# Bottom nav bar
st.markdown(""" 
<!-- your HTML here --> 
""", unsafe_allow_html=True)

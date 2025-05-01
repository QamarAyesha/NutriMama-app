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

def medication_safety_section():
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("💊 Medication Safety Checker for Breastfeeding")
    
    # Input methods
    med_input = st.radio("Input Method:", ["Scan Barcode", "Search Manually"], horizontal=True)
    
    if med_input == "Scan Barcode":
        st.camera_input("Scan medication barcode", key="barcode_scan")
        medication = "BarcodeScannedDrug123"  # Replace with actual scan processing
    else:
        medication = st.text_input("Enter medication name", placeholder="e.g., Ibuprofen")
    
    # Breastfeeding-specific check
    with st.expander("Infant Details (Optional)"):
        infant_age = st.selectbox(
            "Infant Age", 
            ["Newborn (0-1 month)", "1-6 months", "6+ months"]
        )
    
    if st.button("Check Safety"):
        if (med_input == "Search Manually" and not medication):
            st.warning("Please enter a medication name")
        else:
            safety_data = check_lactation_safety(
                medication,
                infant_age if infant_age else "1-6 months"  # Default
            )
            display_safety_results(safety_data)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Lactation-Specific Safety Check ---
def check_lactation_safety(drug_name, infant_age="1-6 months"):
    """Lactation-focused safety check (replace with real API calls)"""
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

# --- Results Display ---
def display_safety_results(data):
    st.markdown("### Lactation Safety Assessment")
    
    # Category badge
    category = data["category"]
    if "L5" in category:
        st.error(f"🚨 **{category}** - CONTRAINDICATED")
    elif "L4" in category:
        st.warning(f"⚠️ **{category}** - Caution Required")
    elif "L3" in category:
        st.warning(f"🔸 **{category}** - Probably Safe")
    else:
        st.success(f"✅ **{category}** - Compatible")
    
    # Key facts
    st.markdown("#### Key Facts")
    st.write(f"- **Milk Transfer:** {data['transfer']}")
    st.write(f"- **Reported Effects:** {data['effects']}")
    
    # Recommendation
    st.markdown("#### Recommendation")
    st.write(data["recommendation"])
    
    # Alternatives (if any)
    if data["alternatives"]:
        st.markdown("#### Safer Alternatives")
        for alt in data["alternatives"]:
            st.write(f"- {alt}")

    # References
    st.caption("ℹ️ Data based on NIH LactMed Database and Hale's Medications & Mothers' Milk")

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
medication_safety_section() 
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
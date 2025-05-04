import streamlit as st
from datetime import datetime

# =======================
# INITIAL STATE
# =======================
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False

# =======================
# PAGE SETUP
# =======================
def set_ui_theme():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
        page_title="NutriMama",
        page_icon="🤱"
    )

    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #F8FBFF, #E4F0F6);
        }
        .stContainer, .stExpander {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border: 1px solid #E6F1F7;
        }
        .stButton>button {
            background-color: #FFB996;
            color: #333333;
            border-radius: 8px;
            font-weight: 600;
            padding: 12px 20px;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FF9C85;
            transform: scale(1.05);
        }
        h1, h2, h3 {
            color: #333333;
            font-family: 'Arial', sans-serif;
        }
        p {
            color: #666666;
            font-size: 16px;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            margin: 0 auto 20px auto;
        }
    </style>
    """, unsafe_allow_html=True)

# =======================
# ONBOARDING FORM
# =======================
def show_onboarding():
    st.markdown("""
    <div style='background-color: #F8FBFF; border-radius: 12px; padding: 30px; 
                text-align: center; margin-bottom: 40px;'>
        <h1 style='margin-bottom: 0; color: #333333;'>Welcome to NutriMama!</h1>
        <p style='font-size: 18px; color: #666;'>Your personalized breastfeeding companion</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("onboarding_form"):
        name = st.text_input("Your Name*", placeholder="Enter your first name")

        col1, col2 = st.columns(2)

        with col1:
            age = st.selectbox(
                "Your Age Group*",
                options=["18-25", "26-35", "36-45", "45+"],
                index=1
            )

            region = st.selectbox(
                "Region*",
                options=["North America", "South Asia", "Africa", "Europe", "Other"],
                index=0
            )

        with col2:
            bf_stage = st.radio(
                "Breastfeeding Stage*",
                options=["0-6 Months", "6-12 Months", "12+ Months"],
                index=0
            )

            conditions = st.multiselect(
                "Health Considerations (Optional)",
                options=["Diabetes", "Hypertension", "PCOS", "Thyroid Issues"],
                default=[]
            )

        submitted = st.form_submit_button("Begin Your Journey →")

    if submitted:
        if not all([name, age, region, bf_stage]):
            st.error("Please fill all required fields (*)")
        else:
            # Map the stage to model input
            stage_map = {
                "0-6 Months": "Lactation",
                "6-12 Months": "Weaning",
                "12+ Months": "Extended"
            }

            st.session_state.user_profile = {
                "name": name,
                "age": age,
                "region": region,
                "bf_stage": stage_map.get(bf_stage, "Lactation"),
                "conditions": conditions,
                "onboarded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            st.session_state.onboarding_complete = True

# =======================
# MAIN FLOW
# =======================
set_ui_theme()

# Show onboarding
if not st.session_state.user_profile:
    show_onboarding()

# After successful onboarding
elif st.session_state.onboarding_complete:
    st.success("✅ Profile saved successfully!")
    if st.button("OK → Go to Home"):
        st.session_state.onboarding_complete = False
        st.switch_page("pages/1_Home.py")

# Already onboarded users revisiting main page
else:
    st.write(f"👋 Welcome back, **{st.session_state.user_profile['name']}**!")
    st.write("You're ready to get your personalized meal plan.")
    if st.button("Go to Home"):
        st.switch_page("pages/1_Home.py")

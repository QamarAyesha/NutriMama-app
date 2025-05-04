import streamlit as st
from datetime import datetime
import os

# ================================================
# INITIALIZE SESSION STATE
# ================================================
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None

# ================================================
# STYLE CONFIGURATION (IMPROVED UI)
# ================================================
def set_ui_theme():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
        page_title="NutriMama",
        page_icon="🤱"
    )
    
    st.markdown(f"""
    <style>
        /* Background gradient */
        .stApp {{
            background: linear-gradient(135deg, #F8FBFF, #E4F0F6);
        }}
        
        /* Card-style sections */
        .stContainer, .stExpander {{
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border: 1px solid #E6F1F7;
        }}
        
        /* Buttons */
        .stButton>button {{
            background-color: #FFB996;
            color: #333333;
            border-radius: 8px;
            font-weight: 600;
            padding: 12px 20px;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #FF9C85;
            transform: scale(1.05);
        }}
        
        /* Typography */
        h1, h2, h3 {{
            color: #333333;
            font-family: 'Arial', sans-serif;
        }}
        p {{
            color: #666666;
            font-size: 16px;
        }}
    </style>
    """, unsafe_allow_html=True)

# ================================================
# ONBOARDING FLOW
# ================================================
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
            # Breastfeeding Stage as duration (0-6 months, 6-12 months, etc.)
            bf_duration = st.selectbox(
                "Breastfeeding Duration*",
                options=["0-6 Months", "6-12 Months", "12+ Months"],
                index=0
            )
            
            # Health considerations (optional)
            conditions = st.multiselect(
                "Health Considerations (Optional)",
                options=["Diabetes", "Hypertension", "PCOS", "Thyroid Issues"],
                default=[]
            )
        
        submitted = st.form_submit_button("Begin Your Journey →")
    
    if submitted:
        if not all([name, age, region, bf_duration]):
            st.error("Please fill all required fields (*)")
        else:
            # Mapping breastfeeding duration to stage for model
            bf_stage_mapping = {
                "0-6 Months": "Lactation",
                "6-12 Months": "Weaning",
                "12+ Months": "Extended"
            }
            bf_stage = bf_stage_mapping[bf_duration]
            
            # Save the user profile in session state
            st.session_state.user_profile = {
                "name": name,
                "age": age,
                "region": region,
                "bf_duration": bf_duration,  # We store duration in the profile
                "bf_stage": bf_stage,        # We store internal stage in the profile
                "conditions": conditions,
                "onboarded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("Profile saved successfully!")
            # Now, pass to the plan page with user profile data
            st.experimental_rerun()

# ================================================
# PLAN PAGE (Calling Model API)
# ================================================
def show_plan_page():
    if 'user_profile' not in st.session_state or st.session_state.user_profile is None:
        st.error("No user profile found. Please complete the onboarding process.")
        return

    # Display user profile data (allow user to edit if needed)
    user_profile = st.session_state.user_profile
    st.write(f"### User Profile:")
    name = st.text_input("Name", user_profile['name'])
    age = st.selectbox("Age Group", ["18-25", "26-35", "36-45", "45+"], index=["18-25", "26-35", "36-45", "45+"].index(user_profile['age']))
    region = st.selectbox("Region", ["North America", "South Asia", "Africa", "Europe", "Other"], index=["North America", "South Asia", "Africa", "Europe", "Other"].index(user_profile['region']))
    bf_duration = st.selectbox("Breastfeeding Duration", ["0-6 Months", "6-12 Months", "12+ Months"], index=["0-6 Months", "6-12 Months", "12+ Months"].index(user_profile['bf_duration']))
    conditions = st.multiselect("Health Considerations (Optional)", options=["Diabetes", "Hypertension", "PCOS", "Thyroid Issues"], default=user_profile['conditions'])

    # Update session state if changes are made
    if st.button("Update Profile"):
        # Map the breastfeeding duration to stage again (in case it was changed)
        bf_stage_mapping = {
            "0-6 Months": "Lactation",
            "6-12 Months": "Weaning",
            "12+ Months": "Extended"
        }
        bf_stage = bf_stage_mapping[bf_duration]
        
        st.session_state.user_profile = {
            "name": name,
            "age": age,
            "region": region,
            "bf_duration": bf_duration,
            "bf_stage": bf_stage,
            "conditions": conditions,
            "onboarded_at": user_profile["onboarded_at"]
        }
        st.success("Profile updated successfully!")

    # Call model API and display nutrition plan
    if st.button("Get Nutrition Plan"):
        # Example API call to your backend
        profile_data = {
            "age": age,
            "region": region,
            "stage": user_profile["bf_stage"],  # Use the internal stage (Lactation, Weaning, Extended)
            "conditions": conditions
        }
        
        # Call model API or backend here (Assuming you have an API endpoint for model prediction)
        # result = api_call_to_model(profile_data)
        
        # Display the result (Here we mock the response)
        mock_response = {
            "personalized_plan": "Balanced diet + hydration",
            "meal_ideas": ["Fruits, grains, milk", "Soup and veggies"],
            "tips": ["Ensure hydration", "Include local, seasonal foods"]
        }
        
        st.write(f"### Nutrition Plan: {mock_response['personalized_plan']}")
        st.write("#### Meal Ideas:")
        for meal in mock_response['meal_ideas']:
            st.write(f"- {meal}")
        st.write("#### Tips:")
        for tip in mock_response['tips']:
            st.write(f"- {tip}")

# ================================================
# MAIN APP FLOW
# ================================================
set_ui_theme()

if not st.session_state.user_profile:
    show_onboarding()
else:
    # Call the plan page
    show_plan_page()

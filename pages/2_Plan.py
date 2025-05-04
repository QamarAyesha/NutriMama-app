import streamlit as st
from gradio_client import Client
from datetime import datetime

# =============================================
# PAGE CONFIG & THEME
# =============================================
st.set_page_config(page_title="Meal Plan for Nursing Mothers", layout="wide", page_icon="🍽️")

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
    </style>
""", unsafe_allow_html=True)

st.title("🥗 Meal Plan Recommender for Nursing Mothers")
st.markdown("Get a personalized meal recommendation based on your **region**, **age**, and **health conditions**.")

# =============================================
# SESSION CHECK
# =============================================
if 'user_profile' not in st.session_state or not st.session_state.user_profile:
    st.warning("🚨 Please complete onboarding first.")
    st.markdown("👉 Click **'NutriMama'** in the left menu to begin onboarding.")
    st.stop()

# =============================================
# LOAD PROFILE
# =============================================
user_profile = st.session_state.user_profile

required_keys = ['age', 'region', 'bf_duration', 'bf_stage', 'conditions']
for key in required_keys:
    if key not in user_profile:
        st.error(f"⚠️ Missing key in user profile: `{key}`. Please redo onboarding.")
        st.markdown("👉 Click **'NutriMama'** in the left menu to begin onboarding.")
        st.stop()

# =============================================
# DISPLAY PROFILE
# =============================================
st.write("### 👤 Your Current Profile")
st.write(f"**Name:** {user_profile['name']}")
st.write(f"**Age Group:** {user_profile['age']}")
st.write(f"**Region:** {user_profile['region']}")
st.write(f"**Breastfeeding Duration:** {user_profile['bf_duration']} _(Stage: {user_profile['bf_stage']})_")
st.write(f"**Health Conditions:** {', '.join(user_profile['conditions']) if user_profile['conditions'] else 'None'}")

# =============================================
# EDIT PROFILE OPTION
# =============================================
# Edit Profile Option
edit_profile = st.button("✏️ Edit Profile")

if edit_profile:
    with st.expander("Update Your Profile Information", expanded=True):
        with st.form("update_profile_form"):
            st.subheader("🔄 Update Profile")

            # Define options and get selected values
            age_options = ["18-25", "26-35", "36-45", "45+"]
            region_options = ["North America", "South Asia", "Africa", "Europe", "Middle East", "Other"]
            bf_duration_options = ["0-6 Months", "6-12 Months", "12+ Months"]
            condition_options = ["Anemia", "Diabetes", "Thyroid", "PCOS", "Hypertension", "Obesity", "Cholesterol", "None"]

            # Profile Form Inputs (excluding name)
            age = st.selectbox("Age Group", age_options, index=age_options.index(user_profile["age"]))
            region = st.selectbox("Region", region_options, index=region_options.index(user_profile["region"]))
            bf_duration = st.selectbox("Breastfeeding Duration", bf_duration_options, index=bf_duration_options.index(user_profile["bf_duration"]))
            conditions = st.multiselect("Health Conditions (Optional)", options=condition_options, default=user_profile["conditions"])

            # Form submit button
            submitted = st.form_submit_button("✅ Update Profile")

            if submitted:
                if not all([age, region, bf_duration]):
                    st.error("⚠️ Please fill all required fields.")
                else:
                    # Map breastfeeding duration to stage for internal use
                    bf_stage_mapping = {
                        "0-6 Months": "Lactation",
                        "6-12 Months": "Weaning",
                        "12+ Months": "Extended"
                    }
                    bf_stage = bf_stage_mapping.get(bf_duration, "Lactation")

                    # Update session state with new profile data, keeping the name unchanged
                    st.session_state.user_profile = {
                        "name": user_profile["name"],  # Keep the original name unchanged
                        "age": age,
                        "region": region,
                        "bf_duration": bf_duration,
                        "bf_stage": bf_stage,
                        "conditions": conditions,
                        "onboarded_at": user_profile.get("onboarded_at", "")
                    }

                    st.success("✅ Profile updated successfully!")
                    st.rerun()  # 🚀 Trigger UI refresh

# =============================================
# GET MEAL PLAN
# =============================================
st.markdown("---")
if st.button("📥 Get Meal Plan"):
    profile = st.session_state.user_profile
    with st.spinner("Fetching your personalized meal plan..."):
        try:
            client = Client("ayeshaqamar/nutrition-api")

            health_input = ", ".join(profile["conditions"])

            result = client.predict(
                age=profile["age"],
                region=profile["region"],
                stage=profile["bf_stage"],
                health_condition=health_input,
                api_name="/predict"
            )

            st.success(f"🎯 Recommended Plan: **{result['plan']}**")

            if result.get("meal_ideas"):
                st.subheader("🍽️ Meal Ideas")
                for meal in result["meal_ideas"]:
                    st.markdown(f"- {meal}")

            if result.get("tips"):
                st.subheader("🧠 Tips")
                for tip in result["tips"]:
                    st.markdown(f"- {tip}")

        except Exception as e:
            st.error(f"⚠️ Error fetching meal plan: {e}")

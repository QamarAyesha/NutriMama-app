import streamlit as st
from gradio_client import Client
from datetime import datetime

# =============================================
# PAGE CONFIG & THEME
# =============================================
st.set_page_config(page_title="Meal Plan", layout="wide", page_icon="🍽️")

st.markdown(
    """
    <style>
    body {
        background-color: #f5f9fc;
        font-family: Arial, sans-serif;
    }
    .main {
        background-color: #f5f9fc;
        padding: 1rem;
    }
    .entry {
        background-color: #f0f4f8;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 16px;
        position: relative;
    }
    .delete-btn {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: #ff6b6b;
        color: white;
        border: none;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        font-size: 12px;
        cursor: pointer;
    }
    button[kind="primary"] {
        background-color: #f9c8a7;
        color: #333333;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        border: none;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
    label, p {
        color: #374151;
    }
    .stButton>button {
        background-color: #f9c8a7;
        color: #333333;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .header-icon {
        vertical-align: middle;
        margin-right: 10px;
    }
    /* Media query for responsiveness */
    @media (max-width: 768px) {
        .entry {
            font-size: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Meal Plan Recommender")
st.markdown("Get a personalized meal recommendation based on your **region**, **age**, and **health conditions**.")

# =============================================
# SESSION CHECK
# =============================================
if 'user_profile' not in st.session_state or not st.session_state.user_profile:
    st.warning("🚨 Please complete onboarding first.")
    st.markdown("Click **'NutriMama'** in the left menu to begin onboarding.")
    st.stop()

# =============================================
# LOAD PROFILE
# =============================================
user_profile = st.session_state.user_profile

required_keys = ['age', 'region', 'bf_duration', 'bf_stage', 'conditions']
for key in required_keys:
    if key not in user_profile:
        st.error(f"⚠️ Missing key in user profile: `{key}`. Please redo onboarding.")
        st.markdown("Click **'NutriMama'** in the left menu to begin onboarding.")
        st.stop()

# =============================================
# DISPLAY PROFILE
# =============================================
st.write("### Your Current Profile")
st.write(f"**Name:** {user_profile['name']}")
st.write(f"**Age Group:** {user_profile['age']}")
st.write(f"**Region:** {user_profile['region']}")
st.write(f"**Breastfeeding Duration:** {user_profile['bf_duration']} _(Stage: {user_profile['bf_stage']})_")
st.write(f"**Health Conditions:** {', '.join(user_profile['conditions']) if user_profile['conditions'] else 'None'}")

# =============================================
# EDIT PROFILE OPTION
# =============================================
edit_profile = st.button("Edit Profile")

if edit_profile:
    with st.expander("Update Your Profile Information", expanded=True):
        with st.form("update_profile_form"):
            st.subheader("Update Profile")

            # Define options
            age_options = ["18-25", "26-35", "36-45", "45+"]
            region_options = ["North America", "South Asia", "Africa", "Europe", "Middle East", "Other"]
            bf_duration_options = ["0-6 Months", "6-12 Months", "12+ Months"]
            condition_options = ["Anemia", "Diabetes", "Thyroid", "PCOS", "Hypertension", "Obesity", "Cholesterol", "None"]

            # Safe index helper
            def safe_index(options, value, default=0):
                try:
                    return options.index(value)
                except ValueError:
                    return default

            # Profile Form Inputs (excluding name)
            age = st.selectbox("Age Group", age_options, index=safe_index(age_options, user_profile["age"]))
            region = st.selectbox("Region", region_options, index=safe_index(region_options, user_profile["region"]))
            bf_duration = st.selectbox("Breastfeeding Duration", bf_duration_options, index=safe_index(bf_duration_options, user_profile["bf_duration"]))
            conditions = st.multiselect("Health Conditions (Optional)", options=condition_options, default=user_profile["conditions"])

            # Form submit button
            submitted = st.form_submit_button("Update Profile")

            if submitted:
                st.write("DEBUG: Form submitted")
                if not all([age, region, bf_duration]):
                    st.error("⚠️ Please fill all required fields.")
                else:
                    # Map breastfeeding duration to stage
                    bf_stage_mapping = {
                        "0-6 Months": "Lactation",
                        "6-12 Months": "Weaning",
                        "12+ Months": "Extended"
                    }
                    bf_stage = bf_stage_mapping.get(bf_duration, "Lactation")

                    # Debug before update
                    st.write("DEBUG: Before update", st.session_state.user_profile)

                    # Update session state
                    st.session_state.user_profile = {
                        "name": user_profile["name"],
                        "age": age,
                        "region": region,
                        "bf_duration": bf_duration,
                        "bf_stage": bf_stage,
                        "conditions": conditions,
                        "onboarded_at": user_profile.get("onboarded_at", "")
                    }

                    # Debug after update
                    st.write("DEBUG: After update", st.session_state.user_profile)
                    st.success("Profile updated successfully!")
                    # st.rerun()  # Comment out for testing

# =============================================
# GET MEAL PLAN
# =============================================
st.markdown("---")
if st.button("Get Meal Plan"):
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
                st.subheader("Tips")
                for tip in result["tips"]:
                    st.markdown(f"- {tip}")

        except Exception as e:
            st.error(f"⚠️ Error fetching meal plan: {e}")

import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="Meal Plan for Nursing Mothers", layout="centered")
st.title("Meal Plan Recommender for Nursing Mothers")
st.markdown("Get a personalized meal recommendation based on your region, age, and health.")

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

# Ensure required fields exist (handle older profiles or partial updates)
required_keys = ['age', 'region', 'bf_duration', 'bf_stage', 'conditions']
for key in required_keys:
    if key not in user_profile:
        st.error(f"⚠️ Missing key in user profile: `{key}`. Please redo onboarding.")
        st.markdown("👉 Click **'NutriMama'** in the left menu to begin onboarding.")
        st.stop()

# =============================================
# DISPLAY PROFILE SUMMARY
# =============================================
st.write("### Your Current Profile:")
st.write(f"Name: {user_profile['name']}")
st.write(f"Age Group: {user_profile['age']}")
st.write(f"Region: {user_profile['region']}")
st.write(f"Breastfeeding Duration: {user_profile['bf_duration']} (Internal Stage: {user_profile['bf_stage']})")
st.write(f"Health Conditions: {', '.join(user_profile['conditions']) if user_profile['conditions'] else 'None'}")

# =============================================
# EDIT PROFILE BUTTON & FORM (Hidden by Default)
# =============================================
# Button to toggle editing profile
edit_profile = st.button("Edit Profile")

if edit_profile:
    with st.expander("Update Your Profile Information", expanded=True):  # Expand form only when clicked
        # Form to update profile
        with st.form("update_profile_form"):
            st.subheader("Update Profile")

            age_options = ["18-25", "26-35", "36-45", "45+"]
            region_options = ["North America", "South Asia", "Africa", "Europe", "Other"]
            bf_duration_options = ["0-6 Months", "6-12 Months", "12+ Months"]
            condition_options = ["Diabetes", "Hypertension", "PCOS", "Thyroid Issues"]

            age = st.selectbox("Age Group", age_options, index=age_options.index(user_profile["age"]))
            region = st.selectbox("Region", region_options, index=region_options.index(user_profile["region"]))
            bf_duration = st.selectbox("Breastfeeding Duration", bf_duration_options, index=bf_duration_options.index(user_profile["bf_duration"]))
            conditions = st.multiselect("Health Conditions (Optional)", options=condition_options, default=user_profile["conditions"])

            submitted = st.form_submit_button("Update Profile")

            if submitted:
                # Map breastfeeding duration to breastfeeding stage
                bf_stage_mapping = {
                    "0-6 Months": "Lactation",
                    "6-12 Months": "Weaning",
                    "12+ Months": "Extended"
                }
                bf_stage = bf_stage_mapping.get(bf_duration, "Lactation")

                # Health Condition Mapping - Map invalid conditions to "None"
                valid_condition_mapping = {
                    "PCOS": "None",
                    "Hypertension": "Hypertension",
                    "Diabetes": "Diabetes",
                    "Thyroid Issues": "Thyroid",
                }

                # Map user's selected conditions to the valid conditions
                mapped_conditions = [valid_condition_mapping.get(cond, "None") for cond in conditions]

                # Update the user profile in session state
                st.session_state.user_profile = {
                    "name": user_profile["name"],
                    "age": age,
                    "region": region,
                    "bf_duration": bf_duration,
                    "bf_stage": bf_stage,
                    "conditions": mapped_conditions,
                    "onboarded_at": user_profile.get("onboarded_at", "")
                }
                st.success("✅ Profile updated successfully!")

# =============================================
# GET MEAL PLAN FROM API
# =============================================
if st.button("Get Meal Plan"):
    profile = st.session_state.user_profile
    with st.spinner("Fetching your personalized meal plan..."):
        try:
            client = Client("ayeshaqamar/nutrition-api")

            # Join the mapped health conditions into a string
            model_conditions_str = ", ".join(profile["conditions"])

            # Get the model prediction using the user profile data
            result = client.predict(
                age=profile["age"],
                region=profile["region"],
                stage=profile["bf_stage"],  # Use mapped bf_stage
                health_condition=model_conditions_str,  # Send the mapped health conditions
                api_name="/predict"
            )

            st.success(f"Recommended Plan: **{result['plan']}**")

            st.subheader("🍽️ Meal Ideas")
            for meal in result.get("meal_ideas", []):
                st.markdown(f"- {meal}")

            st.subheader("🧠 Tips")
            for tip in result.get("tips", []):
                st.markdown(f"- {tip}")

        except Exception as e:
            st.error(f"⚠️ Error fetching meal plan: {str(e)}")

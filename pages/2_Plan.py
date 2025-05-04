import streamlit as st
from gradio_client import Client
import os

st.set_page_config(page_title="Meal Plan for Nursing Mothers", layout="centered")
st.title("Meal Plan Recommender for Nursing Mothers")
st.markdown("Get a personalized meal recommendation based on your region, age, and health.")

# Load user profile from session state
if 'user_profile' not in st.session_state:
    st.error("No user profile found. Please complete the onboarding process.")
else:
    user_profile = st.session_state.user_profile

    # Pre-fill the form with user profile data, allowing the user to edit if desired
    st.write(f"### Your Current Profile:")

    # Display the profile
    st.write(f"Name: {user_profile['name']}")
    st.write(f"Age Group: {user_profile['age']}")
    st.write(f"Region: {user_profile['region']}")
    st.write(f"Breastfeeding Duration: {user_profile['bf_duration']} (Internal Stage: {user_profile['bf_stage']})")
    st.write(f"Health Conditions: {', '.join(user_profile['conditions']) if user_profile['conditions'] else 'None'}")
    
    # Allow the user to adjust any profile information before fetching the plan
    with st.form("update_profile_form"):
        st.subheader("Update Your Profile Information")

        # Age: The user can adjust if needed
        age = st.selectbox(
            "Age Group",
            ["18-25", "26-35", "36-45", "45+"],
            index=["18-25", "26-35", "36-45", "45+"].index(user_profile['age'])
        )

        # Region: The user can adjust if needed
        region = st.selectbox(
            "Region",
            ["North America", "South Asia", "Africa", "Europe", "Other"],
            index=["North America", "South Asia", "Africa", "Europe", "Other"].index(user_profile['region'])
        )

        # Breastfeeding Duration: The user can adjust if needed
        bf_duration = st.selectbox(
            "Breastfeeding Duration",
            ["0-6 Months", "6-12 Months", "12+ Months"],
            index=["0-6 Months", "6-12 Months", "12+ Months"].index(user_profile['bf_duration'])
        )

        # Health Conditions: The user can modify or add conditions
        conditions = st.multiselect(
            "Health Conditions (Optional)",
            options=["Diabetes", "Hypertension", "PCOS", "Thyroid Issues"],
            default=user_profile['conditions']
        )

        submitted = st.form_submit_button("Update Profile")

        if submitted:
            # Map the selected breastfeeding duration to the correct stage for the model
            bf_stage_mapping = {
                "0-6 Months": "Lactation",
                "6-12 Months": "Weaning",
                "12+ Months": "Extended"
            }
            bf_stage = bf_stage_mapping[bf_duration]

            # Update the session state with the new profile data
            st.session_state.user_profile = {
                "name": user_profile['name'],  # Keeping the name unchanged
                "age": age,
                "region": region,
                "bf_duration": bf_duration,
                "bf_stage": bf_stage,
                "conditions": conditions,
                "onboarded_at": user_profile["onboarded_at"]
            }
            st.success("Profile updated successfully!")

    # When user clicks "Get Meal Plan", send the data to the model
    if st.button("Get Meal Plan"):
        with st.spinner("Fetching your personalized meal plan..."):
            try:
                client = Client("ayeshaqamar/nutrition-api")
                
                # Get the model prediction using data from the profile
                result = client.predict(
                    age=user_profile['age'],  # Use the updated or current profile data
                    region=user_profile['region'],
                    stage=user_profile['bf_stage'],
                    health_condition=", ".join(user_profile['conditions']),
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
                st.error(f"⚠️ Error: {str(e)}")

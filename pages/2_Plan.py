import streamlit as st
from gradio_client import Client

# Set up page configuration
st.set_page_config(page_title="Meal Plan for Nursing Mothers", layout="centered")

st.title("Meal Plan Recommender for Nursing Mothers")
st.markdown("Get a personalized meal recommendation based on your region, age, and health.")

# ===== USER INPUTS =====
age = st.number_input("Enter your age", min_value=16, max_value=60, value=28)
region = st.selectbox("Select your region", ["South Asia", "Africa", "Europe", "Middle East"])
stage = st.selectbox("Breastfeeding stage", ["Lactation", "Weaning", "Extended"])
health_condition = st.selectbox("Health condition", ["None", "Anemia", "Diabetes", "Thyroid"])

# ===== SUBMIT BUTTON =====
if st.button("Get Meal Plan"):
    with st.spinner("Fetching your personalized meal plan..."):
        try:
            # Use Gradio Client to interact with the Hugging Face Space API
            client = Client("ayeshaqamar/nutrition-api")
            result = client.predict(
                age=age,
                region=region,
                stage=stage,
                health_condition=health_condition,
                api_name="/predict"
            )

            # Check the result and display the response
            if result:
                st.success(f"Recommended Plan: **{result[0]['plan']}**")

                st.subheader("🍽️ Meal Ideas")
                for meal in result[0].get("meal_ideas", []):
                    st.markdown(f"- {meal}")

                st.subheader("🧠 Tips")
                for tip in result[0].get("tips", []):
                    st.markdown(f"- {tip}")

        except Exception as e:
            # Fallback response for testing if API fails
            st.warning("⚠️ API request failed. Showing default fallback data for testing.")
            
            # Default fallback data
            fallback_data = {
                "plan": "General balanced diet (test fallback)",
                "meal_ideas": ["Rice + lentils", "Seasonal veggies", "Boiled eggs"],
                "tips": [
                    "⚠️ This is a fallback response (model not loaded).",
                    "Use this only for frontend testing.",
                    "Ensure you upload the trained model to enable real predictions."
                ]
            }

            st.success(f"Recommended Plan: **{fallback_data['plan']}**")
            st.subheader("🍽️ Meal Ideas")
            for meal in fallback_data["meal_ideas"]:
                st.markdown(f"- {meal}")

            st.subheader("🧠 Tips")
            for tip in fallback_data["tips"]:
                st.markdown(f"- {tip}")

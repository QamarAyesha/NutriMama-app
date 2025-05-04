import streamlit as st
import requests

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
            # Prepare input for Gradio API
            payload = {
                "data": [age, region, stage, health_condition]
            }

            response = requests.post(
                "https://ayeshaqamar-nutrition-api.hf.space/run/predict",
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                output = result["data"][0]  # Adjust this based on your return format

                st.success(f"Recommended Plan: **{output['plan']}**")

                st.subheader("🍽️ Meal Ideas")
                for meal in output.get("meal_ideas", []):
                    st.markdown(f"- {meal}")

                st.subheader("🧠 Tips")
                for tip in output.get("tips", []):
                    st.markdown(f"- {tip}")
            else:
                st.error(f"❌ API Error: {response.text}")

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

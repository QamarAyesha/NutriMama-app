import streamlit as st
import requests

st.set_page_config(page_title="Meal Plan for Nursing Mothers", layout="centered")

st.title("Meal Plan Recommender for Nursing Mothers")
st.markdown("Get a personalized meal recommendation based on your region, age, and health.")

# ===== USER INPUTS =====
age = st.number_input("Enter your age", min_value=16, max_value=60, value=28)
region = st.selectbox("Select your region", ["South Asia", "East Africa", "North America", "Middle East"])
stage = st.selectbox("Breastfeeding stage", ["0-6 months", "6-12 months", "12+ months"])
health_condition = st.selectbox("Health condition", ["Healthy", "Anemia", "Gestational Diabetes", "Hypertension"])

# ===== SUBMIT BUTTON =====
if st.button("Get Meal Plan"):
    with st.spinner("Fetching your personalized meal plan..."):
        try:
            # API URL
            api_url = "https://7f6c026f-5b31-4a3c-9df7-649d1b48cc16-00-wetiwke814ub.pike.replit.dev/predict"
            
            # Prepare input
            payload = {
                "age": age,
                "region": region,
                "breastfeeding_stage": stage,
                "health_condition": health_condition
            }

            # API Request
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Recommended Plan: **{data['plan']}**")

                st.subheader("🍽️ Meal Ideas")
                for meal in data["meal_ideas"]:
                    st.markdown(f"- {meal}")

                st.subheader("🧠 Tips")
                for tip in data["tips"]:
                    st.markdown(f"- {tip}")
            else:
                st.error("❌ Failed to get recommendation. Please try again.")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")





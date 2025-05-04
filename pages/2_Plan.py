import streamlit as st
from gradio_client import Client

# Setting up the page configuration
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
            # Initialize the Gradio client
            client = Client("ayeshaqamar/nutrition-api")
            
            # Make the prediction call
            result = client.predict(
                age=age,
                region=region,
                stage=stage,
                health_condition=health_condition,
                api_name="/predict"
            )
            
            # Display the result
            st.success(f"Recommended Plan: **{result['plan']}**")
            st.subheader("🍽️ Meal Ideas")
            for meal in result.get("meal_ideas", []):
                st.markdown(f"- {meal}")
            st.subheader("🧠 Tips")
            for tip in result.get("tips", []):
                st.markdown(f"- {tip}")
                
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

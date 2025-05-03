import streamlit as st
import requests
import os
from huggingface_hub import InferenceClient

# Set up the page configuration for Streamlit
st.set_page_config(page_title="Meal Plan for Nursing Mothers", layout="centered")

st.title("Meal Plan Recommender for Nursing Mothers")
st.markdown("Get a personalized meal recommendation based on your region, age, and health.")

# ===== USER INPUTS =====
age = st.number_input("Enter your age", min_value=16, max_value=60, value=28)
region = st.selectbox("Select your region", ["South Asia", "Africa", "Europe", "Middle East"])  # Match your model's regions
stage = st.selectbox("Breastfeeding stage", ["Lactation", "Weaning", "Extended"])  # Match your model's stages
health_condition = st.selectbox("Health condition", ["None", "Anemia", "Diabetes", "Thyroid"])  # Match your model's conditions

# ===== SUBMIT BUTTON =====
if st.button("Get Meal Plan"):
    with st.spinner("Fetching your personalized meal plan..."):
        try:
            # Initialize HF Inference Client with your Hugging Face token
            client = InferenceClient(token=os.getenv("HF_TOKEN"))  # Ensure you set your HF_TOKEN in the Streamlit secrets
            
            # Prepare input (match your model's expected format)
            inputs = {
                "age": age,
                "region": region,
                "breastfeeding_stage": stage,
                "health_condition": health_condition
            }
            
            # Make a prediction request to the Hugging Face model
            response = client.post(
                json=inputs,
                model="ayeshaqamar/nutrition-api"  # Replace with your actual model's repo name
            )
          
           st.write(response.status_code)  # To check if the response code is 200
           st.write(response.text)  # To check the error message if any
            
            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()
                
                st.success(f"Recommended Plan: **{data['personalized_plan']}**")
                
                st.subheader("🍽️ Meal Ideas")
                for meal in data.get("meal_ideas", ["No specific meals suggested"]):
                    st.markdown(f"- {meal}")
                    
                st.subheader("🧠 Tips")
                for tip in data.get("tips", [
                    "Stay hydrated",
                    "Consult a nutritionist"
                ]):
                    st.markdown(f"- {tip}")
                    
            else:
                st.error(f"❌ API Error: {response.text}")

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

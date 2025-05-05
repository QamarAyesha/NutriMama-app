# NutriMama

**NutriMama** is a personalized nutrition recommendation web app built for breastfeeding mothers. It uses user-provided information and a trained machine learning model to deliver stage-aware, health-sensitive meal plans.

---

## Features

- **Onboarding Form**: Collects age, region, breastfeeding stage, and health conditions.
- **ML-Powered Recommendations**: Suggests nutrition plans based on user input using a trained RandomForestClassifier.
- **User-Friendly UI**: Built with Streamlit for smooth interactions and clean design.
- **Personalization**: Plans vary with lactation stage, health conditions (e.g., Anemia, PCOS), and region.
- **Responsive & Accessible**: Mobile-friendly and easy to use.

---

## 🛠 Tech Stack

| Category              | Tools/Technologies |
|-----------------------|--------------------|
| **Language & Framework** | Python, Streamlit |
| **Data & APIs**          | USDA FoodData Central (future), Gradio, gradio_client |
| **Modeling & ML**        | scikit-learn, RandomForestClassifier, pandas, numpy |
| **Data Processing**      | LabelEncoder, MultiLabelBinarizer |
| **Frontend & Viz**       | Streamlit, HTML/CSS, Altair |
| **Storage**              | Streamlit Session State (current), Airtable/Firebase (future) |
| **Deployment**           | Hugging Face Spaces, Streamlit Cloud |

---

## How it Works

1. **User Onboards**: Fills out a simple form.
2. **Data Encoded**: Inputs are transformed using label encoders & binarizers.
3. **ML Inference**: Inputs passed to a trained model which returns a recommended diet.
4. **Results Displayed**: User sees a summary and can explore more.

---

## Machine Learning

- **Model**: RandomForestClassifier (100 trees)
- **Data**: 100 samples of simulated user profiles
- **Features**: Age, region, breastfeeding stage, health conditions
- **Output**: Nutrition plan label (e.g., "High iron diet + calcium")

Model training script is located in `train_model.py`. Artifacts saved in `/model`:
- Trained pipeline
- Label encoders and health binarizer
- Plan classes

---

## Future Plans

- [ ] Save user profiles to Airtable or Firebase
- [ ] Barcode scanning for food logging (Pillow)
- [ ] Interactive Chatbot AI for nutrition Q&A
- [ ] Convert to Progressive Web App (PWA) using Vercel

---

## Development Guide
### Setup

git clone https://github.com/yourusername/NutriMama.git
cd NutriMama
pip install -r requirements.txt

###  Run Locally

streamlit run NutriMama.py 

## Demo link to run this application
https://nutrimama-gjyfqwzn6re4kug3z7tgztutr.streamlit.app/


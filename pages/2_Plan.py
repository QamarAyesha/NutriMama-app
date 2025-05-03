from nutrition_model import get_plan
from nutrition_helpers import (
    get_meal_ideas, get_weekly_overview, get_condition_tips,
    get_stage_tips, get_feeding_advice
)

st.title("🍼 Your Personalized Nutrition Plan")

profile = st.session_state.get("user_profile")

if not profile:
    st.error("Please complete onboarding first.")
    st.stop()

age = profile["age"]
region = profile["region"]
stage = profile["bf_stage"]
conditions = profile["conditions"]

plan = get_plan(age, region, stage, conditions)

with st.container():
    st.header("🧠 Nutrition Plan")
    st.success(plan)

with st.container():
    st.header("🍽️ Meal Ideas with Local Ingredients")
    for meal in get_meal_ideas(region):
        st.markdown(f"- {meal}")

with st.container():
    st.header("📅 Weekly Meal Overview")
    week = get_weekly_overview()
    for day, rec in week.items():
        st.markdown(f"**{day}**: {rec}")

with st.container():
    st.header("🩺 Health Condition Tips")
    tips = get_condition_tips(conditions)
    for tip in tips:
        st.markdown(f"- {tip}")

with st.container():
    st.header("🧬 Stage-Specific Nutrition Tips")
    st.info(get_stage_tips(stage))

with st.container():
    st.header("🤱 Lactation, Weaning & Feeding Advice")
    st.info(get_feeding_advice(stage))






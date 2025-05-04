import streamlit as st

def community_page():
    # =============================================
    # SESSION CHECK: Ensure user_profile exists
    # =============================================
    if 'user_profile' not in st.session_state or not st.session_state.user_profile:
        st.warning("🚨 Please complete onboarding first.")
        st.markdown("Click **'NutriMama'** in the left menu to begin onboarding.")
        st.stop()

    # =============================================
    # Page-level CSS styling
    st.markdown("""
    <style>
        body {
            background-color: #f5f9fc;
            font-family: 'Arial', sans-serif;
        }
        .stButton button {
            background-color: #f9c8a7;
            color: #333333;
            border-radius: 12px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: 600;
            margin-top: 10px;
        }
        .stButton button:hover {
            background-color: #e8b49d;
        }

        .stTextInput, .stTextArea {
            background-color: #ffffff;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
        }
        .forum-post {
            background-color: #f0f4f8;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 12px;
        }
        .recipe-card {
            background-color: #f9f4f0;  /* pastel background */
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 12px;
            border-left: 4px solid #f9c8a7;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .section-title {
            margin: 1.5rem 0 1rem 0;
            color: #333333;
        }
        .header-text {
            text-align: left;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="header-text">
        <h1 style='color: #333333; margin: 0;'>NutriMama Community</h1>
        <p style='color: #666; margin: 0;'>Connect, Share, and Learn Together</p>
    </div>
    """, unsafe_allow_html=True)

   
    # Peer Forums Section
    st.markdown("""<div class="section-title"><h2 style="margin: 0;">Peer Forums</h2></div>""", unsafe_allow_html=True)
    st.write("Join discussions with your peers on various topics.")

    with st.form("forum_form"):
        forum_topic = st.text_input("Start a New Topic", placeholder="Enter a new forum topic...")
        submitted = st.form_submit_button("Create Topic")
        if submitted and forum_topic:
            st.success(f"Topic '{forum_topic}' created!")

    st.markdown("**Ongoing Discussions**")
    forum_posts = [
        {"title": "How to improve breastfeeding techniques?", "replies": 12},
        {"title": "Tips for managing PCOS during breastfeeding", "replies": 8},
        {"title": "Best nutrition for new mothers", "replies": 15}
    ]
    for post in forum_posts:
        st.markdown(f"""
        <div class="forum-post">
            <strong>{post['title']}</strong><br>
            <small>{post['replies']} replies</small>
        </div>
        """, unsafe_allow_html=True)

    # Recipe Sharing Section
    st.markdown("""<div class="section-title"><h2 style="margin: 0;">Recipe Sharing</h2></div>""", unsafe_allow_html=True)
    st.write("Share and explore breastfeeding-friendly recipes with the community.")

    with st.form("recipe_form"):
        col1, col2 = st.columns(2)
        with col1:
            recipe_name = st.text_input("Recipe Name", placeholder="Enter recipe name...")
        with col2:
            prep_time = st.selectbox("Prep Time", ["<15 min", "15-30 min", "30-60 min", ">60 min"])

        ingredients = st.text_area("Ingredients", placeholder="List ingredients (separate with commas)...")
        instructions = st.text_area("Instructions", placeholder="Describe the preparation steps...")

        submitted = st.form_submit_button("Share Recipe")
        if submitted:
            if recipe_name and ingredients and instructions:
                st.success(f"Recipe '{recipe_name}' shared!")
            else:
                st.warning("Please fill all fields")

    st.markdown("**Popular Recipes**")
    recipes = [
        {
            "name": "Lactation Smoothie",
            "prep": "<15 min",
            "ingredients": "Banana, Oats, Almond Milk, Flax Seeds, Brewer's Yeast",
            "instructions": "Blend all ingredients until smooth. Serve chilled."
        },
        {
            "name": "Protein Power Bowl",
            "prep": "15-30 min",
            "ingredients": "Quinoa, Chicken Breast, Avocado, Spinach, Olive Oil",
            "instructions": "Cook quinoa. Grill chicken. Combine all ingredients in bowl."
        }
    ]
    for recipe in recipes:
        st.markdown(f"""
        <div class="recipe-card">
            <h4>{recipe['name']} • {recipe['prep']}</h4>
            <p><strong>Ingredients:</strong> {recipe['ingredients']}</p>
            <p><strong>Instructions:</strong> {recipe['instructions']}</p>
        </div>
        """, unsafe_allow_html=True)

# Call the function to render the page
community_page()



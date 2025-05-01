import streamlit as st

# =============================================
# COMMUNITY TAB PAGE
# =============================================

def community_page():
    # Set background color
    st.markdown("""
    <style>
        body {
            background-color: #f5f9fc; /* Soft pastel blue background */
        }
        .stButton>button {
            background-color: #f9c8a7; /* Peach color button */
            color: #333333; /* Dark gray text */
            border-radius: 8px; /* Rounded corners */
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #e8b49d; /* Slightly darker peach on hover */
        }
        .stTextInput, .stTextArea {
            background-color: #ffffff; /* Pure white input fields */
            border-radius: 10px; /* Rounded corners for inputs */
            border: 1px solid #e0e0e0; /* Light border */
            padding: 10px;
            color: #333333;
        }
        .stTextInput>input, .stTextArea>textarea {
            border: none;
        }
        .stMarkdown {
            color: #333333; /* Dark gray text for all markdown */
        }
        .section-header {
            font-size: 1.75em;
            font-weight: bold;
            color: #333333;
            margin-bottom: 15px;
        }
        .section-content {
            background-color: #ffffff; /* White section background */
            padding: 20px;
            border-radius: 12px; /* Rounded corners for sections */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <h1 style='color: #333333;'>Community Tab</h1>
        <p style='color: #666;'>Connect, Share, and Learn Together</p>
    </div>
    """, unsafe_allow_html=True)

    # Peer Forums Section
    st.markdown('<div class="section-header">👥 Peer Forums</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)

    st.write("Join discussions with your peers on various topics.")
    
    # Forum Input Box
    forum_topic = st.text_input("Start a New Topic", placeholder="Enter a new forum topic...")
    if forum_topic:
        st.success(f"Your forum topic '{forum_topic}' has been created successfully!")

    st.write("Here are some ongoing discussions:")

    # Sample discussions (these could be dynamically loaded from a database)
    forum_posts = ["How to improve breastfeeding techniques?", "Tips for managing PCOS during breastfeeding", "Best nutrition for new mothers."]
    for post in forum_posts:
        st.write(f"- {post}")

    st.markdown('</div>', unsafe_allow_html=True)  # Close Peer Forums Section
    st.markdown("---")

    # Ask an Expert Section
    st.markdown('<div class="section-header">🧑‍🔬 Ask an Expert</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)

    st.write("Got a question? Ask an expert in the field!")
    
    # Ask Question Form
    expert_question = st.text_input("Ask a Question", placeholder="Ask an expert about breastfeeding, nutrition, etc...")
    if expert_question:
        st.success(f"Your question '{expert_question}' has been submitted to an expert!")

    st.write("Here are some recent questions asked by others:")

    # Sample expert questions (these could be dynamically loaded from a database)
    expert_questions = ["What foods should I avoid while breastfeeding?", "Is it safe to exercise during breastfeeding?", "How to handle lactose intolerance while breastfeeding?"]
    for question in expert_questions:
        st.write(f"- {question}")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close Ask an Expert Section
    st.markdown("---")
    
    # Recipe Sharing Section
    st.markdown('<div class="section-header">🍳 Recipe Sharing</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-content">', unsafe_allow_html=True)

    st.write("Share and explore breastfeeding-friendly recipes with the community.")
    
    # Recipe Input Box
    recipe_name = st.text_input("Recipe Name", placeholder="Enter recipe name...")
    recipe_ingredients = st.text_area("Ingredients", placeholder="List ingredients for the recipe...")
    recipe_instructions = st.text_area("Instructions", placeholder="Describe the recipe instructions...")
    
    if st.button("Share Recipe"):
        if recipe_name and recipe_ingredients and recipe_instructions:
            st.success(f"Recipe '{recipe_name}' has been shared successfully!")
        else:
            st.warning("Please fill in all the fields to share your recipe.")
    
    st.write("Here are some popular recipes shared by others:")

    # Sample recipes (these could be dynamically loaded from a database)
    recipes = [
        {"name": "Breastfeeding Smoothie", "ingredients": "Banana, Almond Milk, Spinach", "instructions": "Blend all ingredients until smooth."},
        {"name": "Protein-packed Salad", "ingredients": "Chicken, Kale, Avocado, Olive Oil", "instructions": "Toss all ingredients together."}
    ]
    
    for recipe in recipes:
        st.write(f"### {recipe['name']}")
        st.write(f"**Ingredients**: {recipe['ingredients']}")
        st.write(f"**Instructions**: {recipe['instructions']}")
        st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)  # Close Recipe Sharing Section

# Call the community page function in the main flow
if __name__ == "__main__":
    community_page()

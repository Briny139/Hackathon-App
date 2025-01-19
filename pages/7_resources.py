import streamlit as st

st.set_page_config(page_title="Resources", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .resource-card {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .category-header {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Resources")

# Resources for different categories
categories = {
    "Emergency Services": [
        {"name": "Local Emergency Number", "contact": "911"},
        {"name": "Police Non-Emergency", "contact": "555-0123"},
        {"name": "Crisis Hotline", "contact": "1-800-555-0199"}
    ],
    "Mental Health": [
        {"name": "Suicide Prevention Lifeline", "contact": "988"},
        {"name": "Mental Health Crisis Line", "contact": "1-800-555-0198"},
        {"name": "Counseling Services", "contact": "555-0124"}
    ],
    "Medical Services": [
        {"name": "Nearest Hospital", "contact": "555-0125"},
        {"name": "24/7 Nurse Line", "contact": "555-0126"},
        {"name": "Poison Control", "contact": "1-800-222-1222"}
    ]
}

# Display resources by category
for category, resources in categories.items():
    st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
    
    for resource in resources:
        with st.container():
            st.markdown('<div class="resource-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3,1])
            
            with col1:
                st.write(f"**{resource['name']}**")
                st.write(f"Contact: {resource['contact']}")
            
            with col2:
                st.button("Call", key=f"call_{resource['name']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Back Button
if st.button("← Back to Main"):
    st.switch_page("app.py") 
import streamlit as st

# Set page title and configure layout
st.set_page_config(page_title="Sign Up Page", layout="centered")

# Add custom CSS to style the form
st.markdown("""
    <style>
    .stTextInput > label {
        font-size: 20px;
        font-weight: bold;
        font-family: cursive;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #ccc;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Create a card-like container
with st.container():
    # Add some padding and a border
    st.markdown("""
        <div style="padding: 20px; 
                    border: 2px solid #f0f0f0; 
                    border-radius: 10px;
                    margin: 10px;">
        <h1 style="text-align: center; font-family: cursive;">Sign Up Page</h1>
    """, unsafe_allow_html=True)
    
    # Create the name input field
    name = st.text_input("Your Name:")
    
    # Add dots for visual effect
    st.markdown("...")
    
    st.markdown("</div>", unsafe_allow_html=True)

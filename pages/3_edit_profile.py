import streamlit as st

st.set_page_config(page_title="Edit Profile", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .profile-section {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .stButton > button {
        width: 150px;
        border-radius: 10px;
        height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Edit Profile")

# Profile Picture
with st.container():
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.subheader("Profile Picture")
    st.file_uploader("Upload profile picture", type=["jpg", "png"])
    st.markdown('</div>', unsafe_allow_html=True)

# Basic Information
with st.container():
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name")
        st.text_input("Email")
    with col2:
        st.text_input("Phone")
        st.text_input("Location")
    st.markdown('</div>', unsafe_allow_html=True)

# Skills and Certifications
with st.container():
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.subheader("Skills & Certifications")
    skills = st.multiselect("Select your skills", 
                           ["First Aid", "CPR", "Mental Health First Aid", "Crisis Intervention"])
    st.file_uploader("Upload certification documents", type=["pdf", "jpg", "png"], accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Save Button
if st.button("Save Changes"):
    st.success("Profile updated successfully!")
    st.switch_page("app.py")

# Back Button
if st.button("← Back to Main"):
    st.switch_page("app.py") 
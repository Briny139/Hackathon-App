import streamlit as st

st.set_page_config(page_title="Search Users", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .search-box {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .user-card {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Search Users")

# Search section
with st.container():
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    search_query = st.text_input("Search by name or skills")
    col1, col2 = st.columns(2)
    with col1:
        distance = st.slider("Distance (miles)", 0, 50, 10)
    with col2:
        skills = st.multiselect("Skills", ["First Aid", "CPR", "Mental Health", "Transport"])
    st.markdown('</div>', unsafe_allow_html=True)

# Sample users (in real app, these would come from a database)
users = [
    {"name": "Alice", "distance": "0.5 miles", "skills": ["First Aid", "CPR"]},
    {"name": "Bob", "distance": "1.2 miles", "skills": ["Mental Health"]},
    {"name": "Carol", "distance": "2.0 miles", "skills": ["Transport", "First Aid"]}
]

# Display users
for user in users:
    with st.container():
        st.markdown('<div class="user-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3,1])
        
        with col1:
            st.write(f"**{user['name']}**")
            st.write(f"Distance: {user['distance']}")
            st.write("Skills: " + ", ".join(user['skills']))
        
        with col2:
            st.button("View Profile", key=f"profile_{user['name']}")
            st.button("Message", key=f"message_{user['name']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Back Button
if st.button("← Back to Main"):
    st.switch_page("app.py") 
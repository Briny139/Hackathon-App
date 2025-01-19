import streamlit as st

st.set_page_config(page_title="Manage Requests", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .request-card {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .respond-button > button {
        background-color: #00cc00;
        color: white;
    }
    .details-button > button {
        background-color: #4a90e2;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Requests")

# Filter options
status_filter = st.selectbox("Filter by status", ["All", "Pending", "Active", "Completed"])

# Sample requests (in real app, these would come from a database)
requests = [
    {"name": "John", "type": "Medical", "time": "2h ago", "status": "Pending"},
    {"name": "Sarah", "type": "Transport", "time": "1h ago", "status": "Active"},
    {"name": "Mike", "type": "Emergency", "time": "30m ago", "status": "Pending"}
]

# Display requests
for request in requests:
    with st.container():
        st.markdown('<div class="request-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3,1])
        
        with col1:
            st.write(f"**{request['name']}** - {request['type']}")
            st.write(f"Time: {request['time']}")
            st.write(f"Status: {request['status']}")
        
        with col2:
            st.markdown('<div class="respond-button">', unsafe_allow_html=True)
            st.button("Respond", key=f"respond_{request['name']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="details-button">', unsafe_allow_html=True)
            st.button("See details", key=f"details_{request['name']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Back Button
if st.button("← Back to Main"):
    st.switch_page("app.py") 
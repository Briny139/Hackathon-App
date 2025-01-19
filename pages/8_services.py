import streamlit as st

st.set_page_config(page_title="Services", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .service-card {
        border: 2px solid #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .service-category {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .request-button > button {
        background-color: #4a90e2;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Available Services")

# Service categories
services = {
    "Transportation": [
        {"name": "Emergency Transport", "description": "24/7 emergency transportation service"},
        {"name": "Medical Appointments", "description": "Scheduled medical appointment transport"},
        {"name": "General Transport", "description": "Non-emergency transportation assistance"}
    ],
    "Home Assistance": [
        {"name": "Meal Delivery", "description": "Hot meal delivery service"},
        {"name": "Grocery Shopping", "description": "Grocery shopping and delivery"},
        {"name": "Home Care", "description": "Basic home care assistance"}
    ],
    "Medical Support": [
        {"name": "Medicine Pickup", "description": "Prescription pickup and delivery"},
        {"name": "Medical Equipment", "description": "Medical equipment delivery"},
        {"name": "Home Health", "description": "Basic home health services"}
    ]
}

# Display services by category
for category, service_list in services.items():
    st.markdown(f'<div class="service-category">{category}</div>', unsafe_allow_html=True)
    
    for service in service_list:
        with st.container():
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            col1, col2 = st.columns([3,1])
            
            with col1:
                st.write(f"**{service['name']}**")
                st.write(service['description'])
            
            with col2:
                st.markdown('<div class="request-button">', unsafe_allow_html=True)
                st.button("Request", key=f"request_{service['name']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# Back Button
if st.button("← Back to Main"):
    st.switch_page("app.py") 
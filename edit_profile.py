import streamlit as st
from database import DatabaseManager
from components import show_logo

def show_edit_profile():
    show_logo()
    
    st.title("Edit Profile Page")
    
    # Load user's current details from database
    user_details = DatabaseManager.get_user_details(st.session_state.user_data['user_id'])
    
    # Initialize session state for resources and services with user's current data
    if 'resources' not in st.session_state or st.session_state.get('profile_just_loaded', True):
        st.session_state.resources = user_details.get('resources', '').split(', ') if user_details.get('resources') else []
        st.session_state.services = user_details.get('services', '').split(', ') if user_details.get('services') else []
        st.session_state.profile_just_loaded = False
    
    # Name input with current user's name
    current_name = user_details.get('name', '')
    new_name = st.text_input("Name", value=current_name, key="name")
    
    # Resources section
    st.markdown("### Resources I Can Provide")
    
    # Display current resources with remove buttons
    for idx, resource in enumerate(st.session_state.resources):
        if resource:  # Only display non-empty resources
            col1, col2 = st.columns([4, 1])
            with col1:
                st.info(f"📦 {resource}")
            with col2:
                if st.button("❌", key=f"remove_resource_{idx}"):
                    st.session_state.resources.remove(resource)
                    st.rerun()
    
    # Add resource dropdown
    resource_options = [
        "Medical Supplies",
        "Food",
        "Water",
        "Shelter",
        "Transport",
        "Clothing",
        "First Aid",
        "Blankets",
        "Tools",
        "Generator"
    ]
    # Filter out already selected resources
    available_resources = [r for r in resource_options if r not in st.session_state.resources]
    
    if available_resources:
        col1, col2 = st.columns([4, 1])
        with col1:
            new_resource = st.selectbox(
                "Add a resource",
                ["Select a resource..."] + available_resources,
                key="resource_select"
            )
        with col2:
            if st.button("Add", key="add_resource"):
                if new_resource and new_resource != "Select a resource...":
                    st.session_state.resources.append(new_resource)
                    st.rerun()
    
    # Services section
    st.markdown("### Services I Can Offer")
    
    # Display current services with remove buttons
    for idx, service in enumerate(st.session_state.services):
        if service:  # Only display non-empty services
            col1, col2 = st.columns([4, 1])
            with col1:
                st.info(f"🤝 {service}")
            with col2:
                if st.button("❌", key=f"remove_service_{idx}"):
                    st.session_state.services.remove(service)
                    st.rerun()
    
    # Add service dropdown
    service_options = [
        "Medical Aid",
        "Food Distribution",
        "Transportation",
        "Housing",
        "Counseling",
        "Search & Rescue",
        "Child Care",
        "Elder Care",
        "Construction",
        "Translation"
    ]
    # Filter out already selected services
    available_services = [s for s in service_options if s not in st.session_state.services]
    
    if available_services:
        col1, col2 = st.columns([4, 1])
        with col1:
            new_service = st.selectbox(
                "Add a service",
                ["Select a service..."] + available_services,
                key="service_select"
            )
        with col2:
            if st.button("Add", key="add_service"):
                if new_service and new_service != "Select a service...":
                    st.session_state.services.append(new_service)
                    st.rerun()
    
    # Save changes button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Save Changes", type="primary", use_container_width=True):
        # Update user data in session state and database
        st.session_state.user_data['name'] = new_name
        st.session_state.user_data['resources'] = ', '.join(filter(None, st.session_state.resources))
        st.session_state.user_data['services'] = ', '.join(filter(None, st.session_state.services))
        
        # Save to database
        success = DatabaseManager.update_profile(
            st.session_state.user_data['user_id'],
            new_name,
            st.session_state.user_data['resources'],
            st.session_state.user_data['services']
        )
        
        if success:
            st.success("Profile updated successfully!")
            st.session_state.page = "main"
            st.rerun()
        else:
            st.error("Failed to update profile. Please try again.") 
import streamlit as st
import sqlite3
import pandas as pd
from components import show_logo

def show_search_users():
    show_logo()
    
    st.title("Search Users")
    
    # Initialize session state for filters if not exists
    if 'resource_filter' not in st.session_state:
        st.session_state.resource_filter = []
    if 'service_filter' not in st.session_state:
        st.session_state.service_filter = []
    if 'distance_filter' not in st.session_state:
        st.session_state.distance_filter = "All"
    
    # Search and filter section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("Search by name")
    
    with col2:
        st.write("Filter By:")
        show_filters = st.button("Show Filters")
    
    # Filter sidebar
    if show_filters:
        with st.sidebar:
            st.header("Filters")
            
            # Resource filter (multiple selection)
            st.subheader("Resources")
            resource_filter = st.multiselect(
                "Select Resources",
                options=["Medical Supplies", "Food", "Transport", "Shelter"],
                default=st.session_state.resource_filter,
                key="resource_multiselect"
            )
            st.session_state.resource_filter = resource_filter
            
            # Service filter (multiple selection)
            st.subheader("Services")
            service_filter = st.multiselect(
                "Select Services",
                options=["Medical Aid", "Food Distribution", "Transportation", "Housing"],
                default=st.session_state.service_filter,
                key="service_multiselect"
            )
            st.session_state.service_filter = service_filter
            
            # Distance filter
            st.subheader("Distance")
            distance_filter = st.selectbox(
                "Select Distance",
                options=["All", "Within 5km", "5-10km", "10-20km", "20km+"],
                index=["All", "Within 5km", "5-10km", "10-20km", "20km+"].index(st.session_state.distance_filter),
                key="distance_select"
            )
            st.session_state.distance_filter = distance_filter
    
    # Get users from database
    conn = sqlite3.connect('registration.db')
    query = """
        SELECT name, resources, services, 
               latitude, longitude
        FROM users
        WHERE 1=1
    """
    
    params = []
    if search_query:
        query += " AND name LIKE ?"
        params.append(f"%{search_query}%")
    
    # Apply resource filters
    if st.session_state.resource_filter:
        resource_conditions = []
        for resource in st.session_state.resource_filter:
            resource_conditions.append("resources LIKE ?")
            params.append(f"%{resource}%")
        query += f" AND ({' OR '.join(resource_conditions)})"
    
    # Apply service filters
    if st.session_state.service_filter:
        service_conditions = []
        for service in st.session_state.service_filter:
            service_conditions.append("services LIKE ?")
            params.append(f"%{service}%")
        query += f" AND ({' OR '.join(service_conditions)})"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    # Display results
    if not df.empty:
        for _, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write(f"**{row['name']}**")
                    if row['latitude'] and row['longitude']:
                        # Calculate distance (placeholder for now)
                        distance = "5km"  # This should be calculated based on user's location
                        st.write(f"Distance: {distance}")
                
                with col2:
                    resources = row['resources'].split(',') if row['resources'] else []
                    services = row['services'].split(',') if row['services'] else []
                    
                    # Display resources in orange
                    for resource in resources:
                        st.markdown(f"<span style='color: orange;'>[{resource.strip()}]</span>", unsafe_allow_html=True)
                    
                    # Display services in blue
                    for service in services:
                        st.markdown(f"<span style='color: blue;'>[{service.strip()}]</span>", unsafe_allow_html=True)
    else:
        st.info("No users found matching your criteria")


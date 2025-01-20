import streamlit as st
import sqlite3
import pandas as pd

def show_search_users():
    st.title("Search Users")
    
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
            
            # Resource filter
            st.subheader("Resource")
            resource_filter = st.selectbox(
                "Select Resource",
                options=["All", "Medical Supplies", "Food", "Transport", "Shelter"],
                key="resource_filter"
            )
            
            # Service filter
            st.subheader("Service")
            service_filter = st.selectbox(
                "Select Service",
                options=["All", "Medical Aid", "Food Distribution", "Transportation", "Housing"],
                key="service_filter"
            )
            
            # Distance filter
            st.subheader("Distance")
            distance_filter = st.selectbox(
                "Select Distance",
                options=["All", "Within 5km", "5-10km", "10-20km", "20km+"],
                key="distance_filter"
            )
    
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
    
    if show_filters:
        if resource_filter != "All":
            query += " AND resources LIKE ?"
            params.append(f"%{resource_filter}%")
        if service_filter != "All":
            query += " AND services LIKE ?"
            params.append(f"%{service_filter}%")
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    # Display results
    if not df.empty:
        for _, row in df.iterrows():
            with st.container():
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
                
                st.divider()
    else:
        st.info("No users found matching your criteria") 
import streamlit as st
import sqlite3
from datetime import datetime
import folium
from streamlit_folium import st_folium
import pandas as pd

def show_main_page():
    st.title("Main Page")
    
    # Top section - Map with markers
    show_map_section()
    
    # Bottom section - Navigation buttons in a 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Edit Profile", use_container_width=True):
            st.session_state.page = "edit_profile"
            st.rerun()
            
        if st.button("Distress Call", 
                    use_container_width=True,
                    type="primary"):  # Red button
            st.session_state.page = "distress"
            st.rerun()
    
    with col2:
        if st.button("Search Users", use_container_width=True):
            st.session_state.page = "search_users"
            st.rerun()
            
        if st.button("Manage Requests", 
                    use_container_width=True,
                    type="primary"):  # Red button
            st.session_state.page = "manage_requests"
            st.rerun()
    
    # Admin controls in expander at the bottom
    with st.expander("Admin Controls"):
        show_admin_controls()

def show_map_section():
    # Get all users with locations from database
    conn = sqlite3.connect('registration.db')
    df = pd.read_sql_query("""
        SELECT user_id, name, latitude, longitude, resources, services
        FROM users
        WHERE latitude IS NOT NULL
    """, conn)
    conn.close()
    
    # Set Qatar's coordinates
    qatar_center_lat = 25.3548
    qatar_center_lon = 51.1839
    
    # Define Qatar's bounds
    qatar_bounds = [
        [24.4539, 50.7571],  # Southwest corner
        [26.1821, 51.6366]   # Northeast corner
    ]
    
    # Create map with Qatar focus and restrictions
    m = folium.Map(
        location=[qatar_center_lat, qatar_center_lon],
        zoom_start=8,
        min_zoom=7,
        max_zoom=13,
        max_bounds=True,
        min_lat=qatar_bounds[0][0],
        max_lat=qatar_bounds[1][0],
        min_lon=qatar_bounds[0][1],
        max_lon=qatar_bounds[1][1]
    )
    
    # Get current user's ID from session state
    current_user_id = st.session_state.user_data.get('user_id')
    
    # Add markers for each user
    for idx, row in df.iterrows():
        # Check if this is the current user
        if row['user_id'] == current_user_id:
            # Current user (blue circle)
            color = 'blue'
        elif 'distress' in str(row['services']).lower():
            # Distress calls (red circles)
            color = 'red'
        else:
            # Regular members (black circles)
            color = 'black'
            
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            color=color,
            fill=True,
            popup=row['name'],
        ).add_to(m)
    
    # Display map
    st_folium(m, height=400, width=None)
    
    # Add map key/legend below the map
    st.write("**Map Key:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("⚫ Members")
    with col2:
        st.markdown("🔴 Distress Call")
    with col3:
        st.markdown("🔷 You")

def show_admin_controls():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start New Registration"):
            st.session_state.page = 1
            st.rerun()
    
    with col2:
        if st.button("View All Registrations"):
            test_database()
    
    with col3:
        if st.button("Delete All Records"):
            delete_all_records()

def show_all_registrations():
    st.header("All Registrations")
    
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY registration_date DESC")
    records = c.fetchall()
    conn.close()
    
    if records:
        st.write("### Registration List")
        for record in records:
            st.divider()
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("**Name:** " + str(record[1]))
                st.write("**Date:** " + str(record[7][:16]))
            with col2:
                st.write("**Resources:** " + str(record[2]))
                st.write("**Services:** " + str(record[3]))
                if record[4] and record[5]:
                    st.write("**Location:** " + str(record[4]) + ", " + str(record[5]))
                if record[6]:
                    st.write("**Address:** " + str(record[6]))
    else:
        st.info("No registrations found in database.")

def delete_all_records():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    st.success("All records deleted successfully!")
    st.rerun() 

def test_database():
    st.header("Database Test Results")
    
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    # Get all records
    c.execute("SELECT * FROM users ORDER BY registration_date DESC")
    records = c.fetchall()
    conn.close()
    
    if records:
        st.write("### All Registrations")
        for record in records:
            st.write("---")
            st.write(f"**Name:** {record[1]}")
            st.write(f"**Resources:** {record[2]}")
            st.write(f"**Services:** {record[3]}")
            st.write(f"**Registration Date:** {record[4]}")
    else:
        st.write("No registrations found in database.")
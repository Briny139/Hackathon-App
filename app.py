import streamlit as st
import sqlite3
from datetime import datetime
from main_page import show_main_page
import folium
from streamlit_folium import folium_static, st_folium
import requests
import streamlit.components.v1 as components
from manage_requests import show_manage_requests
from communication import show_communication_page
from database import DatabaseManager
from search_users import show_search_users
from distress_call import show_distress_call
from edit_profile import show_edit_profile
from signup_process import show_signup_page, show_resources_page, show_final_page
import uuid

# Initialize database
def init_db():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    
    # First, check if the location columns exist
    cursor = conn.execute('PRAGMA table_info(users)')
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'latitude' not in columns:
        # Add new columns if they don't exist
        c.execute('ALTER TABLE users ADD COLUMN latitude REAL')
        c.execute('ALTER TABLE users ADD COLUMN longitude REAL')
        c.execute('ALTER TABLE users ADD COLUMN address TEXT')
        conn.commit()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  resources TEXT,
                  services TEXT,
                  latitude REAL,
                  longitude REAL,
                  address TEXT,
                  registration_date TIMESTAMP)''')
    conn.commit()
    conn.close()

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "search_users" # Start with signup page (page 1)
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'registered' not in st.session_state:
    st.session_state.registered = False

def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = "search_users" # Changed from "main" to 1
    if 'db_initialized' not in st.session_state:
        st.session_state.db_initialized = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

def main():
    init_session_state()
    
    # Initialize database if not already done
    if not st.session_state.db_initialized:
        DatabaseManager.init_db()
        st.session_state.db_initialized = True
    
    # Check for and add sample requests if none exist
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    try:
        # First check if the requests table exists
        c.execute('''CREATE TABLE IF NOT EXISTS requests
                    (id TEXT PRIMARY KEY,
                     need TEXT,
                     requester_id TEXT,
                     requester_name TEXT,
                     time TIMESTAMP,
                     status TEXT DEFAULT 'active',
                     distance TEXT)''')
        conn.commit()
        
        # Check if there are any active requests
        c.execute("SELECT COUNT(*) FROM requests WHERE status = 'active'")
        count = c.fetchone()[0]
        
        if count == 0:
            print("No active requests found, adding samples...")
            # Add sample requests with realistic data
            sample_requests = [
                ("Medical Supplies", "Need urgent insulin supplies", "10km"),
                ("Food Aid", "Require baby formula and diapers", "3km"),
                ("Transport", "Need transportation to medical facility", "5km"),
                ("Shelter", "Temporary housing needed for family of 4", "7km"),
                ("Water", "Clean drinking water needed", "2km")
            ]
            
            for need, notes, distance in sample_requests:
                try:
                    DatabaseManager.create_request(
                        need=need,
                        requester_id=str(uuid.uuid4()),  # Generate random requester_id
                        requester_name=f"Sample User {uuid.uuid4().hex[:4]}",  # Generate random name
                        distance=distance
                    )
                    print(f"Added sample request: {need}")
                except Exception as e:
                    print(f"Error adding sample request {need}: {str(e)}")
            
            print("Finished adding sample requests")
            
        # Verify requests were added
        c.execute("SELECT COUNT(*) FROM requests WHERE status = 'active'")
        new_count = c.fetchone()[0]
        print(f"Total active requests in database: {new_count}")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
    
    # Page routing
    if isinstance(st.session_state.page, int):  # Registration flow
        if st.session_state.page == 1:
            show_signup_page()
        elif st.session_state.page == 2:
            show_resources_page()
        elif st.session_state.page == 3:
            show_final_page()
    else:  # Main navigation
        if st.session_state.page == "main":
            show_main_page()
        elif st.session_state.page == "search_users":
            show_search_users()
        elif st.session_state.page == "manage_requests":
            show_manage_requests()
        elif st.session_state.page == "communication":
            show_communication_page()
        elif st.session_state.page == "distress":
            show_distress_call()
        elif st.session_state.page == "edit_profile":
            show_edit_profile()

def save_registration():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users 
                 (name, resources, services, latitude, longitude, address, registration_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (st.session_state.user_data['name'],
               st.session_state.user_data['resources'],
               st.session_state.user_data['services'],
               st.session_state.user_data.get('latitude'),
               st.session_state.user_data.get('longitude'),
               st.session_state.user_data.get('address'),
               datetime.now()))
    conn.commit()
    conn.close()
    st.session_state.page = 'main'
    st.session_state.registered = True
    st.rerun()



if __name__ == "__main__":
    main()
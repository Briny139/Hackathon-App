import streamlit as st
import sqlite3
from datetime import datetime
from main_page import show_main_page
from manage_requests import show_manage_requests
from communication import show_communication_page
from database import DatabaseManager
from search_users import show_search_users
from distress_call import show_distress_call
from edit_profile import show_edit_profile
from signup_process import show_signup_page, show_resources_page, show_final_page

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


def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 1 # Changed from "main" to 1
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
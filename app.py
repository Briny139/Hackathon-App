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
from database import init_requests_db, create_request
from search_users import show_search_users

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
    st.session_state.page = 'main'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'registered' not in st.session_state:
    st.session_state.registered = False

def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = "main"

def main():
    init_session_state()
    init_requests_db()
    
    # Add some test data if the table is empty
    if st.session_state.page == "manage_requests":
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM requests")
        count = c.fetchone()[0]
        conn.close()
        
        if count == 0:
            # Add sample requests
            create_request("Medical Supplies", "user1", "John Doe", "5 km")
            create_request("Food Aid", "user2", "Jane Smith", "3 km")
            create_request("Transport", "user3", "Mike Johnson", "1 km")
    
    # Page routing
    if st.session_state.page == "main":
        show_main_page()
    elif st.session_state.page == "search_users":
        show_search_users()
    elif st.session_state.page == "manage_requests":
        show_manage_requests()
    elif st.session_state.page == "communication":
        show_communication_page()

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

def reset_registration():
    st.session_state.page = 1
    st.session_state.user_data = {}
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

def delete_all_records():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    st.rerun()

def get_address_from_coords(lat, lon):
    try:
        # Using Nominatim API (free, no API key required)
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={'User-Agent': 'myapp/1.0'})
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', '')
    except:
        return ""

def get_user_location():
    st.write("To get your accurate location, please allow location access if prompted by your browser.")
    
    # Add a button to request location
    if st.button("Share My Location"):
        components.html(
            """
            <script>
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    window.parent.postMessage({
                        type: "location",
                        latitude: lat,
                        longitude: lon
                    }, "*");
                },
                function(error) {
                    console.error("Error getting location:", error);
                }
            );
            </script>
            """,
            height=0,
        )
        
        # Initialize location_shared state if not exists
        if 'location_shared' not in st.session_state:
            st.session_state.location_shared = False
            
        # Set location_shared to True when button is clicked
        st.session_state.location_shared = True
        st.rerun()

def show_signup_page():
    st.header("Sign Up")
    name = st.text_input("Name:", key="name")
    
    # Initialize location_shared state if not exists
    if 'location_shared' not in st.session_state:
        st.session_state.location_shared = False
    
    # Get user's location automatically
    user_location = get_user_location()
    
    # If location was just shared, update address
    if st.session_state.location_shared:
        if 'latitude' in st.session_state and 'longitude' in st.session_state:
            new_address = get_address_from_coords(
                st.session_state.latitude,
                st.session_state.longitude
            )
            if new_address:
                st.session_state.address = new_address
                st.session_state.location_shared = False  # Reset the flag
                st.rerun()
    
    # Initialize map center with Qatar's coordinates as default
    qatar_center_lat = 25.3548
    qatar_center_lon = 51.1839
    
    # Define Qatar's bounds
    qatar_bounds = [
        [24.4539, 50.7571],  # Southwest corner
        [26.1821, 51.6366]   # Northeast corner
    ]
    
    # Initialize session state with Qatar's coordinates if not set
    if 'latitude' not in st.session_state:
        st.session_state.latitude = qatar_center_lat
    if 'longitude' not in st.session_state:
        st.session_state.longitude = qatar_center_lon
    
    # Get and store address in session state
    if 'address' not in st.session_state:
        st.session_state.address = ""
    
    # Pre-fill address with detected location
    address = st.text_input("Address:", 
                           value=st.session_state.address,
                           key="address")
    
    st.write("📍 **Location Selection:**")
    st.write("Your location has been automatically detected. You can adjust it by clicking anywhere on the map.")
    
    m = folium.Map(
        location=[st.session_state.latitude, st.session_state.longitude],
        zoom_start=8,
        min_zoom=7,
        max_zoom=13,
        max_bounds=True,
        min_lat=qatar_bounds[0][0],
        max_lat=qatar_bounds[1][0],
        min_lon=qatar_bounds[0][1],
        max_lon=qatar_bounds[1][1]
    )
    
    # Add marker for current selection
    folium.Marker(
        [st.session_state.latitude, st.session_state.longitude],
        popup="Selected Location",
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    # Display the map
    map_data = st_folium(m, height=400, width=700)
    
    # Handle location selection and update address
    if map_data["last_clicked"]:
        st.session_state.latitude = map_data["last_clicked"]["lat"]
        st.session_state.longitude = map_data["last_clicked"]["lng"]
        # Get address for the new coordinates
        st.session_state.address = get_address_from_coords(
            st.session_state.latitude,
            st.session_state.longitude
        )
        st.success("✅ Location selected: {}, {}".format(
            st.session_state.latitude,
            st.session_state.longitude
        ))
        st.rerun()
    
    # Show current coordinates
    st.info("📍 Current location: {}, {}".format(
        st.session_state.latitude,
        st.session_state.longitude
    ))
        
    if st.button("Next"):
        if name.strip() and address.strip():
            st.session_state.user_data.update({
                'name': name,
                'address': address,
                'latitude': st.session_state.latitude,
                'longitude': st.session_state.longitude
            })
            st.session_state.page += 1
            st.rerun()
        else:
            st.error("Please fill in all fields")

if __name__ == "__main__":
    main()

import streamlit as st
from database import DatabaseManager
import requests
import folium
from streamlit_folium import st_folium
import sqlite3
from datetime import datetime
import streamlit.components.v1 as components
import time


def check_stored_location():
    components.html(
        """
        <script>
        // Check for stored location
        const lat = localStorage.getItem('user_lat');
        const lon = localStorage.getItem('user_lon');
        if (lat && lon) {
            // Update Streamlit session state
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: {
                    latitude: parseFloat(lat),
                    longitude: parseFloat(lon)
                }
            }, '*');
        }
        </script>
        """,
        height=0
    )

def save_registration():
    user_id = DatabaseManager.save_registration(
        st.session_state.user_data['name'],
        st.session_state.user_data['resources'],
        st.session_state.user_data['services'],
        st.session_state.user_data.get('latitude'),
        st.session_state.user_data.get('longitude'),
        st.session_state.user_data.get('address')
    )
    
    if user_id:
        st.session_state.user_data['user_id'] = user_id  # Store user_id in session state
        st.session_state.page = 'main'
        st.session_state.registered = True
        st.rerun()
    else:
        st.error("Registration failed. Please try again.")

def reset_registration():
    st.session_state.page = 1
    st.session_state.user_data = {}
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
    st.write("Click below to get your location based on your IP address.")
    
    if st.button("Get My Location"):
        try:
            # Using ipapi.co (free tier, no API key needed)
            response = requests.get('https://ipapi.co/json/')
            if response.status_code == 200:
                data = response.json()
                
                # Update session state with location data
                st.session_state.latitude = float(data['latitude'])
                st.session_state.longitude = float(data['longitude'])
                
                # Update address if possible
                address_components = []
                if data.get('city'):
                    address_components.append(data['city'])
                if data.get('region'):
                    address_components.append(data['region'])
                if data.get('country_name'):
                    address_components.append(data['country_name'])
                
                if address_components:
                    st.session_state.address = ", ".join(address_components)
                
                st.success(f"Location found: ({st.session_state.latitude:.6f}, {st.session_state.longitude:.6f})")
                st.success(f"Address: {st.session_state.address}")
                st.rerun()
            else:
                st.error("Could not fetch location. Please try again later.")
        except Exception as e:
            st.error(f"Error getting location: {str(e)}")
    
    return st.session_state.get('latitude'), st.session_state.get('longitude')

def show_signup_page():
    check_stored_location()
    st.header("Sign Up")
    name = st.text_input("Name:", key="name")
    
    # Initialize location_shared state if not exists
    if 'location_shared' not in st.session_state:
        st.session_state.location_shared = False
    
    # Get user's location automatically
    user_location = get_user_location()
    
    # Initialize Qatar's coordinates
    qatar_center_lat = 25.3548
    qatar_center_lon = 51.1839
    qatar_bounds = [
        [24.4539, 50.7571],  # Southwest corner
        [26.1821, 51.6366]   # Northeast corner
    ]
    
    # Initialize coordinates and address in session state
    if 'latitude' not in st.session_state:
        st.session_state.latitude = qatar_center_lat
    if 'longitude' not in st.session_state:
        st.session_state.longitude = qatar_center_lon
    if 'address' not in st.session_state:
        st.session_state.address = ""
    
    st.write("📍 **Location Selection:**")
    st.write("Your location has been automatically detected. You can adjust it by clicking anywhere on the map.")
    
    # Create the map
    m = folium.Map(
        location=[st.session_state.latitude, st.session_state.longitude],  # Use current position
        zoom_start=8,
        min_zoom=7,
        max_zoom=13,
        max_bounds=True,
        min_lat=qatar_bounds[0][0],
        max_lat=qatar_bounds[1][0],
        min_lon=qatar_bounds[0][1],
        max_lon=qatar_bounds[1][1]
    )
    
    # Add marker at current position
    folium.Marker(
        [st.session_state.latitude, st.session_state.longitude],
        popup="Selected Location",
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    # Display the map and get the data
    map_data = st_folium(m, height=400, width=700)
    
    # Handle location selection and update address
    if map_data and map_data.get("last_clicked"):
        st.session_state.latitude = map_data["last_clicked"]["lat"]
        st.session_state.longitude = map_data["last_clicked"]["lng"]
        # Get address for the new coordinates
        new_address = get_address_from_coords(
            st.session_state.latitude,
            st.session_state.longitude
        )
        if new_address:
            st.session_state.address = new_address
            
        # Recreate the map with updated marker
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
        
        folium.Marker(
            [st.session_state.latitude, st.session_state.longitude],
            popup="Selected Location",
            icon=folium.Icon(color="red")
        ).add_to(m)
        
        st_folium(m, height=400, width=700)
    
    # Show current coordinates
    st.info("📍 Current location: {}, {}".format(
        st.session_state.latitude,
        st.session_state.longitude
    ))
    
    # Display address input after map interaction
    address = st.text_input("Address:", 
                           value=st.session_state.address,
                           key="address")
    
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

def show_resources_page():
    st.header("Resources and Services")
    
    # Resources selection
    st.subheader("What resources can you provide? (Optional)")
    resources = st.multiselect(
        "Select resources:",
        ["Medical Supplies", "Food", "Water", "Shelter", "Clothing", "Transport"],
        key="resources"
    )
    
    # Services selection
    st.subheader("What services can you offer? (Optional)")
    services = st.multiselect(
        "Select services:",
        ["Medical Aid", "Food Distribution", "Transportation", "Housing", "Counseling"],
        key="services"
    )
    
    if st.button("Next"):
        # Remove validation check and always proceed
        st.session_state.user_data.update({
            'resources': ','.join(resources),
            'services': ','.join(services)
        })
        st.session_state.page = 3  # Move to final page
        st.rerun()

def show_final_page():
    st.header("Review and Submit")
    
    st.write("Please review your information:")
    st.write("**Name:** ", st.session_state.user_data.get('name', ''))
    st.write("**Address:** ", st.session_state.user_data.get('address', ''))
    st.write("**Resources:** ", st.session_state.user_data.get('resources', ''))
    st.write("**Services:** ", st.session_state.user_data.get('services', ''))
    
    if st.button("Submit"):
        user_id = DatabaseManager.save_registration(
            st.session_state.user_data.get('name'),
            st.session_state.user_data.get('resources'),
            st.session_state.user_data.get('services'),
            st.session_state.user_data.get('latitude'),
            st.session_state.user_data.get('longitude'),
            st.session_state.user_data.get('address')
        )
        
        if user_id:
            st.session_state.user_data['user_id'] = user_id  # Store the user_id
            st.success("Registration successful!")
            st.session_state.page = "main"
            st.rerun()
        else:
            st.error("Registration failed. Please try again.")

# Add this function to handle the location callback
def handle_location_callback():
    components.html(
        """
        <script>
        window.addEventListener('message', function(e) {
            if (e.data.type === 'location_update') {
                const lat = e.data.latitude;
                const lon = e.data.longitude;
                if (lat && lon) {
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: {
                            latitude: lat,
                            longitude: lon
                        }
                    }, '*');
                }
            }
        });
        </script>
        """,
        height=0
    )
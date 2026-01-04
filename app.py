import streamlit as st
import folium
from streamlit_folium import st_folium
import google.generativeai as genai
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


# API Key Integration
# User needs to create a .streamlit/secrets.toml file with GEMINI_API_KEY = "YOUR_API_KEY"
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("Gemini API Key not found. Please set it in .streamlit/secrets.toml") # while hosting you need to set the API key in streamlit hosting interface
    st.stop()


def generate_itinerary(starting_location, destination, budget_min, budget_max, currency, start_date, end_date, interests):
    prompt = f"Create a personalized, budget-friendly travel itinerary for a student trip from {starting_location} to {destination} from {start_date} to {end_date}. The budget is between {budget_min} and {budget_max} {currency}. The student is interested in {', '.join(interests)}. Include cost-effective transportation, affordable accommodation, and student-friendly activities. The itinerary should be structured with daily plans, estimated costs for each activity/transportation/accommodation, and time allocations. Please present the output in a clear, visually appealing markdown format with headings for each day and bullet points for activities."
    
    model = genai.GenerativeModel('gemini-pro-latest')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating itinerary: {e}")
        return "Error: Could not generate itinerary."

st.set_page_config(page_title="AI-Powered Travel Planner", layout="wide")

def main():
    tab1, tab2 = st.tabs(["Plan Your Trip", "About"])

    with tab1:
        st.title("AI-Powered Travel Planner for Students")

        # Initialize session state for itinerary
        if 'itinerary' not in st.session_state:
            st.session_state.itinerary = None

        st.sidebar.header("Plan Your Trip")

        # Starting Location Input
        starting_location = st.sidebar.text_input("Starting Location", "", placeholder="Enter starting location")

        # Destination Input
        destination = st.sidebar.text_input("Destination", "", placeholder="Enter destination location")

        # Custom Budget Input
        budget_min = st.sidebar.text_input("Minimum Budget", value="500")
        budget_max = st.sidebar.text_input("Maximum Budget", value="2000")
        currency = st.sidebar.text_input("Currency", value="USD")

        # Travel Date Pickers
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        # Interest/Activity Preferences
        interests = st.sidebar.multiselect(
            "Interests/Activities",
            ["Sightseeing", "Adventure", "Food", "Culture", "Relaxation", "Nightlife", "Study-related"]
        )

        if st.sidebar.button("Generate Itinerary"):
            if not destination:
                st.sidebar.error("Please enter a destination.")
            else:
                with st.spinner("The system is working, please wait..."):
                    st.subheader(f"Generating itinerary for {destination}...")
                    itinerary = generate_itinerary(starting_location, destination, budget_min, budget_max, currency, start_date, end_date, interests)
                    st.session_state.itinerary = itinerary



        # Display a map
        st.subheader("Explore on Map")
        
        geolocator = Nominatim(user_agent="travel_planner_app")

        @st.cache_data(ttl=3600) # Cache for 1 hour
        def geocode_location(location_name, retries=3, timeout=10):
            try:
                for attempt in range(retries):
                    try:
                        return geolocator.geocode(location_name, timeout=timeout)
                    except (GeocoderTimedOut, GeocoderServiceError) as e:
                        if attempt < retries - 1:
                            continue
                        st.sidebar.warning(f"Could not geocode {location_name} after {retries} attempts: {e}")
                        return None
            except Exception as e:
                st.sidebar.error(f"An unexpected error occurred during geocoding {location_name}: {e}")
                return None

        # Geocode starting location and destination for map
        if starting_location:
            starting_loc_coords = geocode_location(starting_location)
        else:
            starting_loc_coords = None

        if destination:
            destination_loc_coords = geocode_location(destination)
        else:
            destination_loc_coords = None

        # Create map
        if starting_loc_coords or destination_loc_coords:
            if destination_loc_coords:
                map_center = [destination_loc_coords.latitude, destination_loc_coords.longitude]
            elif starting_loc_coords:
                map_center = [starting_loc_coords.latitude, starting_loc_coords.longitude]
            else:
                map_center = [0, 0] # Default center if neither is found

            m = folium.Map(location=map_center, zoom_start=10)

            if starting_loc_coords:
                folium.Marker(
                    [starting_loc_coords.latitude, starting_loc_coords.longitude],
                    tooltip=starting_location
                ).add_to(m)
            if destination_loc_coords:
                folium.Marker(
                    [destination_loc_coords.latitude, destination_loc_coords.longitude],
                    tooltip=destination,
                    icon=folium.Icon(color="red")
                ).add_to(m)

            if starting_loc_coords and destination_loc_coords:
                m.fit_bounds([[starting_loc_coords.latitude, starting_loc_coords.longitude],
                              [destination_loc_coords.latitude, destination_loc_coords.longitude]])

            st_folium(m, width=700, height=500)

            # Move itinerary display inside the map block
            if st.session_state.itinerary:
                st.markdown(st.session_state.itinerary)
        else:
            st.info("Enter a starting location or destination to see the map.")

    with tab2:
        st.header("About This App")
        st.write("This AI-powered travel planner helps students create personalized and budget-friendly itineraries.")
        st.write("Developed with Streamlit and Google Gemini.")

        st.subheader("Developer Bio")
        st.write("Passionate Computer Science student with a strong interest in building scalable, AI-driven solutions. Strong teamcollaborator with proven performance in hackathons and technical events. Interested in applying technical skills,creativity, and continuous learning to impactful projects.")
    
        with open("documents/resume.pdf", "rb") as file:
            btn = st.download_button(
                label="Download Resume",
                data=file,
                file_name="resume.pdf",
                mime="application/octet-stream"
            )
        
        st.write("Social Link:")
        st.markdown("**LinkedIN Profle link:** https://www.linkedin.com/in/puneethkumarms")
        st.markdown("**Github Profile link:** https://github.com/PuneethKumarMS")
        
        st.subheader("Contact Information")
        st.markdown("**Email:** [puneethkumarms21@gmail.com](mailto:puneethkumarms21@gmail.com)")
        

       
if __name__ == "__main__":
    main()

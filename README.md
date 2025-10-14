# AI-Powered Travel Planner for Students

## Project Overview
This project is an AI-powered travel planner designed to help students create personalized and budget-friendly itineraries. Users can input their starting location, destination, budget, travel dates, and interests, and the application will generate a detailed itinerary using the Gemini API.

## Features
- **Personalized Itineraries**: Generates customized travel plans based on user preferences.
- **Budget-Friendly**: Considers budget constraints for accommodation, transportation, and activities.
- **Interactive Map**: Displays starting and destination locations on a map using Folium.
- **Real-time Feedback**: Provides loading indicators and messages during geocoding and itinerary generation.
- **Customizable Budget**: Allows users to input a custom budget range and currency.

## Setup Instructions

### Prerequisites
- Python 3.8+
- `pip` (Python package installer)

### Installation
1. **Clone the repository (if applicable):**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-name>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You may need to create a `requirements.txt` file first if it doesn't exist, by running `pip freeze > requirements.txt`)*

### Gemini API Key Setup
1. **Obtain a Gemini API Key:**
   - Go to the [Google AI Studio](https://aistudio.google.com/app/apikey) and create an API key.

2. **Create `secrets.toml`:**
   - In the root directory of your project, create a folder named `.streamlit`.
   - Inside the `.streamlit` folder, create a file named `secrets.toml`.

3. **Add your API key to `secrets.toml`:**
   - Open `secrets.toml` and add the following line, replacing `"YOUR_API_KEY"` with your actual Gemini API key:
     ```toml
     GEMINI_API_KEY = "YOUR_API_KEY"
     ```

## How to Run
1. **Start the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Access the application:**
   - Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Usage
1. Enter your starting location, destination, budget range, travel dates, and interests in the sidebar.
2. Click the "Generate Itinerary" button.
3. The application will display a map with your starting and destination points, followed by a personalized travel itinerary.
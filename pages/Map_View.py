import streamlit as st
import pandas as pd
import requests
import json

# --- Page Title ---
st.title("🗺️ Map View + Weather Info")

# --- Load city coordinates ---
with open("city_coordinates.json") as f:
    city_coords = json.load(f)

# --- Dropdown to select city ---
selected_city = st.selectbox("Select a city to view weather", options=list(city_coords.keys()))

# --- Show city on map ---
location_df = pd.DataFrame([{
    'lat': city_coords[selected_city][0],
    'lon': city_coords[selected_city][1]
}])
st.map(location_df)

# --- Fetch weather data ---
st.subheader(f"🌤️ Current Weather in {selected_city}")
api_key = st.secrets["OPENWEATHERMAP_API_KEY"]  # Stored in .streamlit/secrets.toml
lat, lon = city_coords[selected_city]

try:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response["cod"] == 200:
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"].title()
        icon_code = response["weather"][0]["icon"]
        st.metric("🌡️ Temperature", f"{temp} °C")
        st.write("**Condition:**", desc)
        st.image(f"http://openweathermap.org/img/wn/{icon_code}@2x.png", width=100)
    else:
        st.error("❌ Failed to fetch weather data.")

except Exception as e:
    st.error(f"Error fetching weather data: {e}")


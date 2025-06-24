import streamlit as st
import requests
import json

# --- Load cities list (example: top 1000 cities) ---
with open("city_list.json") as f:
    city_list = json.load(f)

# --- Set page config ---
st.set_page_config(page_title="Home | Weather Analysis", page_icon="☆️", layout="wide")

# --- Style tweaks ---
st.markdown("""
    <style>
        .stMetric { text-align: center; }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            background-color: #262730;
            color: white;
            border: 1px solid #444;
        }
        .stButton>button:hover {
            background-color: #444;
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 Real-Time Weather Analysis")
st.markdown("##### Your all-in-one platform for global weather insights and air quality monitoring.")
st.image("https://cdn-icons-png.flaticon.com/512/869/869869.png", width=80)

st.divider()

st.subheader("🗭 Explore Features")

col1, col2, col3 ,col4 = st.columns(4)

with col1:
    st.metric("🌡️ Live Weather", "Live data for any city")
    st.link_button("Go to Live Weather", "/Live_Weather")

with col2:
    st.metric("📊 Forecast", "5-day weather prediction")
    st.link_button("View Forecast", "/Forecast")

with col3:
    st.metric("🌀 AQI", "Air Quality Index")
    st.link_button("Check AQI", "/AQI")

with col4:
    st.metric("💡 Smart Suggestions", "Get weather-based tips")
    st.link_button("Recommendations", "/Recommendations")

st.divider()

st.subheader("🔎 Quick Weather Snapshot")
query = st.text_input("🔍 Search for a city", placeholder="Start typing a city name...")
suggestions = [city for city in city_list if query.lower() in city.lower()] if query else []
selected_city = st.selectbox("📍 Select from matches", suggestions) if suggestions else None
if selected_city:
    st.session_state.selected_city = selected_city
    st.success(f"Fetching data for: {selected_city}")

    try:
        api_key = st.secrets["OPENWEATHERMAP_API_KEY"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response["cod"] == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"].title()
            icon_code = response["weather"][0]["icon"]
            st.success(f"🌤️ {selected_city.title()}: {temp}°C, {desc}")
            st.image(f"http://openweathermap.org/img/wn/{icon_code}@2x.png", width=80)
        else:
            st.error("City not found. Please check spelling.")
    except:
        st.error("❌ Error fetching weather data. Check your API key or connection.")

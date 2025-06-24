import streamlit as st
import requests
import json
from datetime import datetime

api_key = st.secrets["OPENWEATHERMAP_API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

with open("city_list.json") as f:
    city_list = json.load(f)

def get_weather(city):
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    r = requests.get(BASE_URL, params=params)
    if r.status_code == 200:
        data = r.json()
        return {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'datetime': datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

st.title("🌦️ Live Weather")
city = st.selectbox("Select a city", options=city_list)

if city:
    data = get_weather(city)
    if data:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image(f"http://openweathermap.org/img/wn/{data['icon']}@2x.png", width=100)
        with col2:
            st.subheader(f"📍 {data['city']}")
            st.markdown(f"**🕒 Updated:** {data['datetime']}")
            st.markdown(f"**☄ Condition:** {data['weather']}")
        with col3:
            st.metric("🌡️ Temperature", f"{data['temperature']} °C")
            st.metric("💧 Humidity", f"{data['humidity']} %")
    else:
        st.error("City not found or API error.")
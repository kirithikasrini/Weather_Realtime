import streamlit as st
import requests
import json

api_key = st.secrets["OPENWEATHERMAP_API_KEY"]

st.title("🤖 Smart Weather Tips")

with open("city_list.json") as f:
    city_list = json.load(f)
city = st.selectbox("Select a city", options=city_list)

if city:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            weather_main = data['weather'][0]['main']

            st.markdown(f"### 📍 {city}")
            st.metric("🌡 Temperature", f"{temp}°C")
            st.metric("☁️ Weather", weather_main)

            st.markdown("### 💡 Recommendations")

            if temp < 15:
                st.info("🧥 It's chilly. Wear a jacket!")
            elif temp > 35:
                st.warning("☀️ It's hot. Stay hydrated!")
            else:
                st.success("😊 The temperature is quite pleasant!")

            if 'Rain' in weather_main:
                st.error("🌧️ Rain expected! Carry an umbrella.")
            elif 'Snow' in weather_main:
                st.error("❄️ Snowy conditions! Wear warm clothes.")
            elif 'Clear' in weather_main:
                st.info("🌞 It's sunny. Sunglasses recommended!")
        else:
            st.error(f"⚠️ Error: {data.get('message', 'Unable to fetch weather data')}")
    except Exception as e:
        st.error(f"❌ Exception: {str(e)}")

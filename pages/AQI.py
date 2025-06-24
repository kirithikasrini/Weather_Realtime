
import streamlit as st
import requests
import json

st.set_page_config(page_title="Air Quality Index", layout="wide")
api_key = st.secrets["OPENWEATHERMAP_API_KEY"]

st.title("🌫️ Air Quality Index (AQI)")
with open("city_list.json") as f:
    city_list = json.load(f)
city = st.selectbox("Select a city", options=city_list)


if city:
    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_resp = requests.get(geo_url).json()

        if geo_resp and isinstance(geo_resp, list) and 'lat' in geo_resp[0] and 'lon' in geo_resp[0]:
            lat = geo_resp[0]['lat']
            lon = geo_resp[0]['lon']

            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            aqi_resp = requests.get(aqi_url).json()

            if "list" in aqi_resp and len(aqi_resp["list"]) > 0:
                aqi = aqi_resp["list"][0]["main"]["aqi"]
                aqi_mapping = {
                    1: "Good 😊",
                    2: "Fair 🙂",
                    3: "Moderate 😐",
                    4: "Poor 😷",
                    5: "Very Poor 🤢"
                }

                st.subheader(f"AQI in {city}: {aqi_mapping.get(aqi, 'Unknown')}")
                st.metric("AQI Level", aqi, delta=None)
            else:
                st.error("Could not fetch AQI data.")
        else:
            st.error("❌ Could not find coordinates for the entered city.")

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")

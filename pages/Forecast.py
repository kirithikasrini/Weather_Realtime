import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

api_key = st.secrets["OPENWEATHERMAP_API_KEY"]

st.title("📅 5-Day Forecast")
with open("city_list.json") as f:
    city_list = json.load(f)
city = st.selectbox("Select a city", options=city_list)

if city:
    city = "Chennai"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        forecast = []
        for entry in data['list']:
            forecast.append({
                'datetime': entry['dt_txt'],
                'temperature': entry['main']['temp'],
                'humidity': entry['main']['humidity']
            })
        df = pd.DataFrame(forecast)
        st.line_chart(df.set_index('datetime'))
    else:
        st.error("City not found or API error.")
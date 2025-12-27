import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Weather Forecast App",
    page_icon="🌦️",
    layout="centered"
)

# ---------- DARK MODE ----------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .card {
        background: rgba(0,0,0,0.45);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #74ebd5, #ACB6E5);
        color: black;
    }
    .card {
        background: rgba(255,255,255,0.6);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- COMMON CSS ----------
st.markdown("""
<style>
.card {
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-top: 20px;
    text-align: center;
}
.temp {
    font-size: 48px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center;'>🌦️ Weather Forecast App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>know your weather update in  Real-time</p>", unsafe_allow_html=True)

# ---------- API KEY ----------
import os
API_KEY = os.getenv("WEATHER_API_KEY")


# ---------- AUTO LOCATION ----------
auto_loc = st.checkbox("📍 Auto-detect my location")

if auto_loc:
    loc_data = requests.get("https://ipinfo.io/json").json()
    city = loc_data.get("city", "Hyderabad")
else:
    city = st.text_input("🌍 Enter city name", "Hyderabad")

# ---------- FETCH WEATHER ----------
if st.button("🔍 Get Weather"):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current = data["current"]
        forecast = data["forecast"]["forecastday"]

        # ---- CURRENT WEATHER ----
        st.markdown(f"""
        <div class="card">
            <h2>📍 {city}</h2>
            <img src="https:{current['condition']['icon']}" width="90">
            <div class="temp">{current['temp_c']}°C</div>
            <p>🌤️ {current['condition']['text']}</p>
            <p>💧 Humidity: {current['humidity']}%</p>
            <p>🌬️ Wind: {current['wind_kph']} km/h</p>
            <p style="font-size:14px;">🕒 Last updated: {current['last_updated']}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---- 3 DAY FORECAST ----
        st.subheader("📅 3-Day Forecast")

        cols = st.columns(3)
        for i, day in enumerate(forecast):
            date = datetime.strptime(day["date"], "%Y-%m-%d").strftime("%A")
            with cols[i]:
                st.markdown(f"""
                <div class="card">
                    <h4>{date}</h4>
                    <img src="https:{day['day']['condition']['icon']}" width="60">
                    <p>🌡️ {day['day']['avgtemp_c']} °C</p>
                    <p>{day['day']['condition']['text']}</p>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.error("❌ Unable to fetch weather data")

# ---------- FOOTER ----------
st.markdown("""
<p style="text-align:center; font-size:14px; opacity:0.8;">
Built with ❤️ using Python, Streamlit & WeatherAPI<br>
By Navya Bhargavi 🚀
</p>
""", unsafe_allow_html=True)

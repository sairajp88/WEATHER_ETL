import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='./config/.env')
API_KEY = os.getenv("OWM_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Single city fetch with Celsius units
def get_weather_by_city(city_name: str):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # 👈 This makes it return Celsius!
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for {city_name}: {e}")
        return None

# Fetch for multiple cities
def get_weather_for_cities(city_list):
    weather_data = []
    for city in city_list:
        data = get_weather_by_city(city)
        if data:
            weather_data.append(data)
    return weather_data

# Test Block
if __name__ == "__main__":
    cities = ["Mumbai", "Delhi", "London", "New York", "Tokyo"]
    data = get_weather_for_cities(cities)
    for d in data:
        print(f"{d['name']} => {d['main']['temp']}°C")

import pandas as pd
from datetime import datetime

def transform_weather_data(raw_data: list) -> pd.DataFrame:
    cleaned_data = []

    for item in raw_data:
        if not item or 'main' not in item:
            continue  # Skip if data is missing or malformed

        # Extract and transform key data
        cleaned = {
            "city": item.get("name"),
            "country": item.get("sys", {}).get("country"),
            "temperature_c": round(item["main"]["temp"], 2),
            "feels_like_c": round(item["main"]["feels_like"], 2),
            "humidity": item["main"].get("humidity"),
            "pressure": item["main"].get("pressure"),
            "wind_speed": item.get("wind", {}).get("speed"),
            "weather_main": item.get("weather", [{}])[0].get("main"),
            "weather_desc": item.get("weather", [{}])[0].get("description"),
            "cloud_coverage": item.get("clouds", {}).get("all"),
            "timestamp_utc": datetime.utcfromtimestamp(item.get("dt", 0))
        }

        cleaned_data.append(cleaned)

    df = pd.DataFrame(cleaned_data)
    return df

# 🔽 Test block
if __name__ == "__main__":
    from extract import get_weather_for_cities

    cities = ["Mumbai", "Delhi", "New York", "Tokyo", "London"]
    raw_data = get_weather_for_cities(cities)
    df = transform_weather_data(raw_data)
    print(df.head())

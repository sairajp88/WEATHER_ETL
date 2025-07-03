from etl.extract import get_weather_for_cities
from etl.transform import transform_weather_data
from etl.load import load_to_snowflake

def main():
    cities = ["Mumbai", "Delhi", "New York", "Tokyo", "London"]
    raw_data = get_weather_for_cities(cities)
    df = transform_weather_data(raw_data)
    load_to_snowflake(df)

if __name__ == "__main__":
    main()

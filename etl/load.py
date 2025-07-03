import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

# Load env vars
load_dotenv(dotenv_path="./config/.env")

# Snowflake credentials
DB_NAME = os.getenv("SNOWFLAKE_DATABASE")
SCHEMA_NAME = os.getenv("SNOWFLAKE_SCHEMA")
USER = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# Step 1: Simulated transformed weather data
# Replace this with your real transformed DataFrame later
df = pd.DataFrame([{
    "CITY": "Mumbai",
    "COUNTRY": "IN",
    "TEMPERATURE_C": 27.6,
    "FEELS_LIKE_C": 31.2,
    "HUMIDITY": 82,
    "PRESSURE": 1003,
    "WIND_SPEED": 9.6,
    "WEATHER_MAIN": "Clouds",
    "WEATHER_DESC": "overcast clouds",
    "CLOUD_COVERAGE": 100,
    "TIMESTAMP_UTC": pd.Timestamp.utcnow()
}])

# Step 2: Connect
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE
)

cursor = conn.cursor()
cursor.execute(f"USE DATABASE {DB_NAME}")
cursor.execute(f"USE SCHEMA {SCHEMA_NAME}")
print(f"✅ Connected to Snowflake: {DB_NAME}.{SCHEMA_NAME}")

# Step 3: Create table if not exists
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS WEATHER_DATA (
    CITY STRING,
    COUNTRY STRING,
    TEMPERATURE_C FLOAT,
    FEELS_LIKE_C FLOAT,
    HUMIDITY INTEGER,
    PRESSURE INTEGER,
    WIND_SPEED FLOAT,
    WEATHER_MAIN STRING,
    WEATHER_DESC STRING,
    CLOUD_COVERAGE INTEGER,
    TIMESTAMP_UTC TIMESTAMP
)
""")
print("✅ Table ready")

# Step 4: Insert data
for _, row in df.iterrows():
    values = (
        row["CITY"],
        row["COUNTRY"],
        row["TEMPERATURE_C"],
        row["FEELS_LIKE_C"],
        row["HUMIDITY"],
        row["PRESSURE"],
        row["WIND_SPEED"],
        row["WEATHER_MAIN"],
        row["WEATHER_DESC"],
        row["CLOUD_COVERAGE"],
        row["TIMESTAMP_UTC"].isoformat()  # 👈 Convert Timestamp to string
    )
    cursor.execute(f"""
        INSERT INTO WEATHER_DATA (
            CITY, COUNTRY, TEMPERATURE_C, FEELS_LIKE_C, HUMIDITY,
            PRESSURE, WIND_SPEED, WEATHER_MAIN, WEATHER_DESC,
            CLOUD_COVERAGE, TIMESTAMP_UTC
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)

print("✅ Weather data inserted into Snowflake")
cursor.close()
conn.close()

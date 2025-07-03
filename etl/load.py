import os
from dotenv import load_dotenv
import snowflake.connector

# Load env vars
load_dotenv(dotenv_path="./config/.env")

# Snowflake credentials
DB_NAME = os.getenv("SNOWFLAKE_DATABASE")
SCHEMA_NAME = os.getenv("SNOWFLAKE_SCHEMA")
USER = os.getenv("SNOWFLAKE_USER")
PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

def load_to_snowflake(df):
    # Step 1: Connect
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

    # Step 2: Create table if not exists
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

    # Step 3: Insert data
    for _, row in df.iterrows():
        values = (
            row["city"],
            row["country"],
            row["temperature_c"],
            row["feels_like_c"],
            row["humidity"],
            row["pressure"],
            row["wind_speed"],
            row["weather_main"],
            row["weather_desc"],
            row["cloud_coverage"],
            row["timestamp_utc"].isoformat()
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

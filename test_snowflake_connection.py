from dotenv import load_dotenv
import os
import snowflake.connector

load_dotenv(dotenv_path="./config/.env")

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    role=os.getenv("SNOWFLAKE_ROLE")
)

cursor = conn.cursor()
cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE(), CURRENT_SCHEMA();")
print(cursor.fetchone())

cursor.close()
conn.close()

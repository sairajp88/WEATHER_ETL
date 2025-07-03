Here's your updated and polished `README.md` with the developer credit included:

---

# 🌦️ Real-Time Weather ETL Dashboard

A full-stack data engineering project that extracts real-time weather data from the OpenWeatherMap API, processes and loads it into Snowflake using a Python ETL pipeline, and visualizes it with an interactive Streamlit dashboard.

### 🚀 [Live Dashboard ↗](https://weather-anly-etl.streamlit.app/)

![Weather Dashboard Screenshot](https://github.com/sairajp88/WEATHER_ETL/assets/412382a4-d0f1-4085-a014-7552a544c963)

---

## 📌 Features

* 🌍 Real-time weather extraction for multiple cities
* 🛠️ Modular Python ETL pipeline
* ❄️ Snowflake data warehouse integration
* 📊 Interactive Streamlit dashboard
* ⏱️ GitHub Actions for hourly automation
* 🔐 Secure secrets handling (env vars + Streamlit Cloud)

---

## 🧱 Project Structure

```bash
weather_etl_pipeline/
├── config/              # .env file for secrets (not committed)
├── etl/                 # ETL scripts (extract, transform, load, scheduler)
├── report/              # Streamlit dashboard
├── .github/workflows/   # GitHub Action for ETL automation
├── logs/                # ETL logs
├── main.py              # Entrypoint for running ETL locally
├── requirements.txt     # Python dependencies
```

---

## 🔁 ETL Pipeline Overview

* **Extract**: Weather data via OpenWeatherMap API
* **Transform**: Cleaned and structured into pandas DataFrame
* **Load**: Inserted into Snowflake table `WEATHER_DATA`
* **Automate**: Runs hourly via GitHub Actions

---

## 📊 Dashboard Highlights

* **Filter by city, weather condition, and date**
* **Visuals**:

  * Line charts: Temperature, Humidity, Wind Speed
  * Bar chart: Weather Conditions Breakdown
* **Built using**: Streamlit + SQLAlchemy + Snowflake

---

## ⚙️ Setup Instructions

### 🔹 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/sairajp88/WEATHER_ETL.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your secrets in config/.env
```

`.env` format:

```env
OWM_API_KEY=your_openweathermap_api_key
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account_id
SNOWFLAKE_DATABASE=WEATHER_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

```bash
# 4. Run the ETL
python main.py

# 5. Run the Streamlit Dashboard
streamlit run streamlit_app.py
```

---

## ☁️ Cloud Deployment

* **Streamlit Cloud**: Dashboard hosted at
  👉 [weather-anly-etl.streamlit.app](https://weather-anly-etl.streamlit.app/)
* **GitHub Actions**: Hourly ETL via `.github/workflows/hourly_etl.yml`

---

## 🔐 Security Practices

* `.env` is ignored in `.gitignore`
* Secrets are managed via:

  * Streamlit Cloud > Advanced Settings > Secrets
  * GitHub Secrets for Actions (optional)
* GitGuardian monitors secret leakage in repo

---

## 📬 Feedback & Contributions

Suggestions, issues, and forks are welcome!
If you find this useful, drop a ⭐ on the repo 🙌

---

## 👨‍💻 Developer

**Sairaj Patil**
🔗 [LinkedIn](https://www.linkedin.com/in/sairaj-patil-iy)
📧 [sairajpatil.dev@gmail.com](mailto:pixelpatil95@gmail.com)

---

Let me know if you'd like this saved as a downloadable `README.md` file or added to your GitHub repo directly.

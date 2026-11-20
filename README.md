# GenAI-Based Intelligent Electronic Equipment Monitoring and Troubleshooting Assistant

Simulated sensor readings (temperature, voltage, current) are stored in SQLite,
shown on a Streamlit dashboard, and interpreted by the Google Gemini API.

## Files
- sensor_data.csv - simulated readings (normal, overheating, undervoltage, overcurrent)
- api.py - Flask API that stores readings
- replay.py - sends the CSV rows to the API
- llm.py - Gemini diagnosis module
- dashboard.py - Streamlit dashboard

## Setup
pip install flask requests pandas streamlit google-genai
Set the environment variable GEMINI_API_KEY (never commit your key).

## Run
1. python api.py
2. python -m streamlit run dashboard.py
3. python replay.py
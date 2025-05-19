import sys
import os
import requests
import psycopg2
import pandas as pd
from datetime import datetime

# Ensure project root is in the path so config can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import OPENWEATHER_API_KEY, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        print(f"{city_name}: {temp}°C, {description}")
        save_to_db(city_name, temp, description)
        return {
            "City": city_name,
            "Temperature (°C)": temp,
            "Description": description,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        print(f"[{city}] Failed to fetch data:", response.status_code, response.text)
        return None

def fetch_weather_for_cities(city_list):
    records = []
    for city in city_list:
        result = fetch_weather(city)
        if result:
            records.append(result)

    if records:
        df = pd.DataFrame(records)
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(output_dir, exist_ok=True)
        file_name = f"weather_report_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        file_path = os.path.join(output_dir, file_name)
        df.to_excel(file_path, index=False)
        print(f"✅ Excel report saved: {file_path}")
    else:
        print("⚠️ No data collected to save.")

def save_to_db(city, temp, desc):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather.weather_reports (city, temperature, description)
            VALUES (%s, %s, %s)
        """, (city, temp, desc))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Saved {city} to DB.")
    except Exception as e:
        print(f"DB error while saving {city}:", e)


        conn.commit()
        cur.close()
        conn.close()
        print(f"Saved {city} to DB.")
    except Exception as e:
        print("DB error:", e)

# Run directly
if __name__ == "__main__":
    cities = [
        "Dallas",
        "New York",
        "London",
        "Tokyo",
        "Bangalore",
        "San Francisco",
        "Chicago",
        "Berlin",
        "Sydney",
        "Toronto",
        "Mumbai",
        "Cape Town"
    ]
    fetch_weather_for_cities(cities)

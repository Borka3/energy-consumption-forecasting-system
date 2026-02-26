import sqlite3
import os


DB_FILE = "power_forecast.db"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "Database", "database", DB_FILE)

def get_database_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH)



def add_holiday_record(year, day_of_week, holiday_date, holiday_name):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Holidays (year, day_of_week, holiday_date, holiday_name) VALUES (?, ?, ?, ?)",
        (year, day_of_week, holiday_date, holiday_name)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return


def add_consumption_record(timestamp, timezone, location, ptid_code, power_load):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO EnergyConsumption (timestamp, timezone, location, ptid_code, power_load) VALUES (?, ?, ?, ?, ?)",
        (timestamp, timezone, location, ptid_code, power_load)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return




def add_weather_record(location, measurement_time, temperature, feels_like, dew_point, humidity, 
                       precipitation, precip_probability, precip_type, snow_level, snow_depth, 
                       wind_gust, wind_speed, wind_direction, pressure, cloud_cover, visibility, 
                       solar_radiation, solar_energy, uv_index, severe_risk, conditions):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO WeatherConditions 
        (location, measurement_time, temperature, feels_like, dew_point, humidity, 
         precipitation, precip_probability, precip_type, snow_level, snow_depth, 
         wind_gust, wind_speed, wind_direction, pressure, cloud_cover, visibility, 
         solar_radiation, solar_energy, uv_index, severe_risk, conditions) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (location, measurement_time, temperature, feels_like, dew_point, humidity,
         precipitation, precip_probability, precip_type, snow_level, snow_depth,
         wind_gust, wind_speed, wind_direction, pressure, cloud_cover, visibility,
         solar_radiation, solar_energy, uv_index, severe_risk, conditions)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return



def save_forecast_result(forecast_time, predicted_load, location="UNKNOWN"):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        
        cursor.execute(
            "UPDATE LoadForecasts SET predicted_load = ? WHERE forecast_time = ? AND location = ?",
            (predicted_load, forecast_time, location)
        )

        
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO LoadForecasts (forecast_time, predicted_load, location) VALUES (?, ?, ?)",
                (forecast_time, predicted_load, location)
            )

        conn.commit()
        print(f"Forecast saved or updated for {forecast_time}, {location}")
    except Exception as e:
        print(f"Error saving forecast: {e}")
    finally:
        cursor.close()
        conn.close()
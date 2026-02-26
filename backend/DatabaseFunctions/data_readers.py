import sqlite3
import os


DB_FILE = "power_forecast.db"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
DB_PATH = os.path.join(BASE_DIR, "Database", "database", DB_FILE)

def get_database_connection():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB_PATH)



def fetch_all_holidays():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Holidays")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_all_consumption():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EnergyConsumption")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_all_weather_data():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM WeatherConditions")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_weather_by_date_range(start_date, end_date):
    conn = get_database_connection()
    cursor = conn.cursor()
    
    sql_query = """
    SELECT *
    FROM WeatherConditions 
    WHERE date(measurement_time) BETWEEN date(?) AND date(?)
    ORDER BY measurement_time
    """
    cursor.execute(sql_query, (start_date, end_date))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_weather_for_forecast(start_date, forecast_days):
    conn = get_database_connection()
    cursor = conn.cursor()
    
    sql_query = """
    SELECT *
    FROM WeatherConditions 
    WHERE date(measurement_time) >= date(?)
    ORDER BY measurement_time
    LIMIT ?
    """
    cursor.execute(sql_query, (start_date, forecast_days * 24))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetch_forecasts_by_period(start_date, end_date):
    conn = get_database_connection()
    cursor = conn.cursor()
    
    sql_query = """
    SELECT *
    FROM LoadForecasts 
    WHERE date(forecast_time) BETWEEN date(?) AND date(?)
    ORDER BY forecast_time
    """
    cursor.execute(sql_query, (start_date, end_date))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_all_regions():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT location FROM EnergyConsumption")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
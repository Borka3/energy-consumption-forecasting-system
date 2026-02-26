import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys


sys.path.append(str(Path(__file__).parent.parent))

from DatabaseFunctions.data_readers import (
    fetch_all_holidays, 
    fetch_all_consumption,
    fetch_weather_by_date_range,
    fetch_weather_for_forecast
)

SPECIAL_NUMBER = 666999



def preprocess_for_training(start_date, end_date, region="N.Y.C."):
    print("=" * 60)
    print("=" * 60)
    
    try:
        usholidays_list = fetch_all_holidays()
        print(f"Holidays: {len(usholidays_list)}")
        
        weatherdata_list = fetch_weather_by_date_range(start_date, end_date)
        print(f"Weather data for period: {len(weatherdata_list)}")
        
        dt_list = fetch_all_consumption()
        print(f"Total consumption of data in the database: {len(dt_list)}")
        
        
        print(f"FILTERING BY REGION '{region}'...")
        loaddata_list = []
        
        for i, load in enumerate(dt_list):
            load_date = load[1]  
            load_region = load[3]  
            
            if load_region != region:
                continue
            
            try:
                load_dt = datetime.strptime(load_date, '%m/%d/%Y %H:%M:%S')
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                
                if start_dt <= load_dt <= end_dt:
                    loaddata_list.append(load)
            except Exception as e:
                print(f"Parse error {load_date}: {e}")
                continue
        
        if len(loaddata_list) == 0:
            print(f"NO DATA FOR REGION'{region}'IN THE GIVEN PERIOD!")
            return pd.DataFrame()
        
        loaddata_list = sort_list_by_dates(loaddata_list)
        
        
        print(f"\n  MERGE WEATHER AND CONSUMPTION FOR REGION '{region}'...")
        hourly_consumption = {}
        
        for load in loaddata_list:
            load_date = load[1] 
            load_value = load[5]
            try:
                load_dt = datetime.strptime(load_date, '%m/%d/%Y %H:%M:%S')
                hour_key = load_dt.replace(minute=0, second=0, microsecond=0)
                if hour_key not in hourly_consumption:
                    hourly_consumption[hour_key] = []
                hourly_consumption[hour_key].append(load_value)
            except Exception:
                continue
        
        data_list = []
        matched_count = 0
        
        for j in range(len(weatherdata_list)):
            weather_date = weatherdata_list[j][2]  
            try:
                weather_date_clean = weather_date.replace('T', ' ')
                weather_dt = datetime.strptime(weather_date_clean, '%Y-%m-%d %H:%M:%S')
                
                if weather_dt in hourly_consumption:
                    hourly_loads = hourly_consumption[weather_dt]
                    avg_load = sum(hourly_loads) / len(hourly_loads) if hourly_loads else np.nan
                    
                    prev_hour_dt = weather_dt - timedelta(hours=1)
                    prev_day_dt = weather_dt - timedelta(days=1)
                    
                    load_prev_hour = np.nan
                    load_prev_day = np.nan
                    
                    if prev_hour_dt in hourly_consumption:
                        prev_hour_loads = hourly_consumption[prev_hour_dt]
                        load_prev_hour = sum(prev_hour_loads) / len(prev_hour_loads) if prev_hour_loads else np.nan
                    
                    if prev_day_dt in hourly_consumption:
                        prev_day_loads = hourly_consumption[prev_day_dt]
                        load_prev_day = sum(prev_day_loads) / len(prev_day_loads) if prev_day_loads else np.nan
                    
                    elem = [
                        weatherdata_list[j][3],   # temperature
                        weatherdata_list[j][5],   # dew_point
                        weatherdata_list[j][6],   # humidity
                        weatherdata_list[j][12],  # wind_gust
                        weatherdata_list[j][13],  # wind_speed
                        weatherdata_list[j][14],  # wind_direction
                        weatherdata_list[j][15],  # pressure
                        weatherdata_list[j][16],  # cloud_cover
                        weatherdata_list[j][3] if j == 0 else weatherdata_list[j-1][3],  # prev_temp
                        int(weather_date[5:7]),   # month
                        avg_load,                 # power_load (target)
                        load_prev_hour,           # prev hour load
                        load_prev_day,            # prev day load
                        weather_dt.weekday(),     # day_of_week
                        1 if weather_dt.weekday() >= 5 else 0,  # is_weekend
                        1 if check_for_holiday(load_date, usholidays_list) else 0  # is_holiday
                    ]
                    data_list.append(elem)
                    matched_count += 1
            except Exception as e:
                print(f"Error parsing weather_date '{weather_date}': {e}")
                continue
        
        print(f"Data merged successfully:{matched_count}")
        
        if len(data_list) == 0:
            print("NO JOINED DATA!")
            return pd.DataFrame()
        
        
        df = pd.DataFrame(data_list, columns=[
            "temperature", "dew_point", "humidity", "wind_gust", "wind_speed",
            "wind_direction", "pressure", "cloud_cover", "prev_temp", "month",
            "power_load", "prev_hour_load", "prev_day_load", "day_of_week",
            "is_weekend", "is_holiday"
        ])
        
        
        df["temperature"] = df["temperature"].mask((df["temperature"] > 100.0) | (df["temperature"] < 0.0), np.nan)
        df["dew_point"] = df["dew_point"].mask((df["dew_point"] > 78.0) | (df["dew_point"] < -17.0), np.nan)
        df["humidity"] = df["humidity"].mask((df["humidity"] > 100.0) | (df["humidity"] < 8.0), np.nan)
        df["wind_gust"] = df["wind_gust"].mask((df["wind_gust"] > 61.0) | (df["wind_gust"] < 16.0), np.nan)
        df["wind_speed"] = df["wind_speed"].mask((df["wind_speed"] > 33.0) | (df["wind_speed"] < 0.0), np.nan)
        df["wind_direction"] = df["wind_direction"].mask((df["wind_direction"] > 360.0) | (df["wind_direction"] < 0.0), np.nan)
        df["pressure"] = df["pressure"].mask((df["pressure"] > 1045) | (df["pressure"] < 975.0), np.nan)
        df["cloud_cover"] = df["cloud_cover"].mask((df["cloud_cover"] > 100.0) | (df["cloud_cover"] < 0.0), np.nan)
        
        
        df["power_load"].replace(SPECIAL_NUMBER, np.nan, inplace=True)
        
        
        return df
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


    

def preprocess_for_prediction(start_date, days, region="N.Y.C."):

    
    weatherdata_list = fetch_weather_for_forecast(start_date, days)
    print(f"Weather data for prediction: {len(weatherdata_list)}")

    
    train_end_dt = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(hours=1)
    df_train = preprocess_for_training("2018-01-01", train_end_dt.strftime("%Y-%m-%d"), region)
    last_known_hour_load = df_train["power_load"].iloc[-1] if not df_train.empty else -1
    last_known_day_load = df_train["power_load"].iloc[-24] if len(df_train) >= 24 else last_known_hour_load

    data_list = []
    
    for i in range(len(weatherdata_list)):
        weather_date = weatherdata_list[i][2]
        weather_date_clean = weather_date.replace('T', ' ')
        weather_dt = datetime.strptime(weather_date_clean, '%Y-%m-%d %H:%M:%S')

        # Lagged feature
        prev_day = weather_dt.replace(hour=0, minute=0, second=0) - pd.Timedelta(days=1)
        prev_day_temps = []
        for j in range(len(weatherdata_list)):
            wd = weatherdata_list[j][2].replace('T', ' ')
            wd_dt = datetime.strptime(wd, '%Y-%m-%d %H:%M:%S')
            if prev_day <= wd_dt < prev_day + pd.Timedelta(days=1):
                prev_day_temps.append(weatherdata_list[j][3])
        avg_temp_prev_day = sum(prev_day_temps) / len(prev_day_temps) if prev_day_temps else -1

       
        
        load_prev_hour = last_known_hour_load if i == 0 else data_list[-1][11]
        load_prev_day = last_known_day_load

        elem = [
            weatherdata_list[i][3],   # temperature
            weatherdata_list[i][5],   # dew_point
            weatherdata_list[i][6],   # humidity
            weatherdata_list[i][12],  # wind_gust
            weatherdata_list[i][13],  # wind_speed
            weatherdata_list[i][14],  # wind_direction
            weatherdata_list[i][15],  # pressure
            weatherdata_list[i][16],  # cloud_cover
            weatherdata_list[i][3] if i == 0 else weatherdata_list[i-1][3],  # prev_temp
            int(weather_date[5:7]) if len(weather_date) > 7 else 1,          # month
            -1,                          # dummy load 
            load_prev_hour,              # prev hour load
            load_prev_day,               # prev day load
            weather_dt.weekday(),        # day_of_week
            1 if weather_dt.weekday() >= 5 else 0,  # is_weekend
            1 if check_for_holiday(weather_date_clean, fetch_all_holidays()) else 0  # is_holiday
        ]

        data_list.append(elem)
    
    df = pd.DataFrame(data_list, columns=[
        "temperature","dew_point","humidity","wind_gust","wind_speed",
        "wind_direction","pressure","cloud_cover","prev_temp","month",
        "power_load","prev_hour_load","prev_day_load","day_of_week",
        "is_weekend","is_holiday"
    ])
    
   
    if not df.empty:
        df["temperature"] = df["temperature"].mask((df["temperature"] > 100.0) | (df["temperature"] < 0.0), np.nan)
        df["dew_point"] = df["dew_point"].mask((df["dew_point"] > 78.0) | (df["dew_point"] < -17.0), np.nan)
        df["humidity"] = df["humidity"].mask((df["humidity"] > 100.0) | (df["humidity"] < 8.0), np.nan)
        df["wind_gust"] = df["wind_gust"].mask((df["wind_gust"] > 61.0) | (df["wind_gust"] < 16.0), np.nan)
        df["wind_speed"] = df["wind_speed"].mask((df["wind_speed"] > 33.0) | (df["wind_speed"] < 0.0), np.nan)
        df["wind_direction"] = df["wind_direction"].mask((df["wind_direction"] > 360.0) | (df["wind_direction"] < 0.0), np.nan)
        df["pressure"] = df["pressure"].mask((df["pressure"] > 1045) | (df["pressure"] < 975.0), np.nan)
        df["cloud_cover"] = df["cloud_cover"].mask((df["cloud_cover"] > 100.0) | (df["cloud_cover"] < 0.0), np.nan)

       
        for col in df.columns:
            df[col] = df[col].interpolate(method='linear', limit_direction='both')
    
    return df

def sort_list_by_dates(my_list):
    
    date_format = '%m/%d/%Y %H:%M:%S'
    my_list.sort(key=lambda x: datetime.strptime(x[1], date_format))
    return my_list


def check_for_holiday(date, ush_list):
    for holiday in ush_list:
        holiday_date = holiday[3]  

        try:
            
            load_dt = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')

            
            holiday_dt = datetime.strptime(str(holiday_date).split()[0], '%Y-%m-%d')

            if (load_dt.year == holiday_dt.year and
                load_dt.month == holiday_dt.month and
                load_dt.day == holiday_dt.day):
                return True
        except Exception as e:
            
            continue

    return False


 

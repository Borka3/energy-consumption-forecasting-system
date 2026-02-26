import pandas as pd
import os
from pathlib import Path
import sys
from datetime import datetime, timedelta
import numpy as np


sys.path.append(str(Path(__file__).parent.parent))

from Services.HelperClasses.custom_preparer import CustomPreparer
from Services.HelperClasses.ann_regression import AnnRegression
from DatabaseFunctions.data_readers import fetch_weather_for_forecast
from DatabaseFunctions.data_writers import save_forecast_result
from Services import preprocessing_service



def find_model_for_location(location):
   
    model_files = find_model_files()
    
    if not model_files:
        return None
    
    location_lower = location.lower()
    
    
    for model_file in model_files:
        filename = os.path.basename(model_file).lower()
        if location_lower in filename and 'current_model' not in filename:
            print(f"Site specific model found {location}: {os.path.basename(model_file)}")
            print("DEBUG returning:", model_file)

            return model_file
    
   
    for model_file in model_files:
        filename = os.path.basename(model_file).lower()
        if location_lower in filename:
            print(f"Model found for location {location}: {os.path.basename(model_file)}")
            return model_file
    

    for model_file in model_files:
        if 'current_model' in os.path.basename(model_file).lower():
            print(f"There is no specific model for {location}, I use current_model")
            return model_file
    
    print(f"No current_model, I use the first one available")
    return model_files[0]

def find_model_files():

    possible_locations = [
        'Services/Models',
        'Models',
        os.path.join(os.path.dirname(__file__), 'Models'),
    ]
    
    model_files = []
    seen_names = set()
    
    for location in possible_locations:
        if os.path.exists(location):
            for file in os.listdir(location):
                if file.endswith('.keras') or file.endswith('.h5'):
                    full_path = os.path.abspath(os.path.join(location, file))
                    file_name = os.path.basename(file)
                    
         
                    if file_name not in seen_names:
                        seen_names.add(file_name)
                        model_files.append(full_path)
    
    return model_files

def forecast(start_date, days, location="N.Y.C.", model_path=None):

    location = "N.Y.C."

    if model_path is None:
        best_model_path = os.path.abspath("Services/Models/model_N.Y.C._2018_01_01_2021_05_01.keras")
        if os.path.exists(best_model_path):
            model_path = best_model_path
            print(f"I use the best model: {os.path.basename(model_path)}")
        else:
            
            model_path = find_model_for_location(location)
            print("Best model not found, I'm using fallback...")
            print("DEBUG model_path returned:", model_path)
            if not model_path:
                print(f"No model found for location: {location}")
                return []

    print(f"Model: {os.path.basename(model_path)}")

    if not os.path.exists(model_path):
        print(f"Model does not exist: {model_path}")
        return []


    try:
    
        weatherdata_list = fetch_weather_for_forecast(start_date, days)
        if not weatherdata_list:
            print("No weather data!")
            return []
        print(f"Found {len(weatherdata_list)} weather records")

        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        train_start_dt = start_dt - timedelta(days=365)  
        train_end_dt = start_dt                         

        train_start = train_start_dt.strftime("%Y-%m-%d")
        train_end = train_end_dt.strftime("%Y-%m-%d")

        df_train = preprocessing_service.preprocess_for_training(train_start, train_end, location)
        if df_train.empty:
            print(f"There is no training data for {location} in the period {train_start} to {train_end}")
            return []

       
        num_columns = df_train.shape[1]
        SHARE_FOR_TRAINING = 0
        preparer = CustomPreparer(df_train, num_columns, SHARE_FOR_TRAINING)
        preparer.fit_scalers_for_forecast(df_train) 

        
        df_prediction = preprocessing_service.preprocess_for_prediction(start_date, days, location)
        if df_prediction.empty:
            print("Prediction DataFrame is empty!")
            return []
        print(f"Preprocessed  {len(df_prediction)} rows")

        
        print("DEBUG df_prediction.head():\n", df_prediction.head())

        preparer.datasetOrig = df_prediction.values.astype('float32')
        testX, testY = preparer.prepare_for_predict()
        print(f"Data prepared: {testX.shape}")

    
        ann_regression = AnnRegression()
        print(f"Loading model...")
        testPredict = ann_regression.predict_with_model_from_path(testX, model_path)

        if not isinstance(testPredict, np.ndarray):
            testPredict = np.array(testPredict)
        print(f"Prediction done: {testPredict.shape}")

       
        print("DEBUG raw testPredict (scaled):", testPredict[:10])

        
        testPredict = preparer.inverse_transform_test_predict(testPredict)

        
        predictedloaddata_list = []
        min_length = min(len(weatherdata_list), len(testPredict))

        for i in range(min_length):
            if isinstance(testPredict, np.ndarray):
                if testPredict.ndim == 3:
                    prediction = float(testPredict[i, 0, 0])
                elif testPredict.ndim == 2:
                    prediction = float(testPredict[i, 0])
                else:
                    prediction = float(testPredict[i])
            else:
                if hasattr(testPredict[i], '__len__'):
                    prediction = float(testPredict[i][0])
                else:
                    prediction = float(testPredict[i])

            elem = [weatherdata_list[i][2], prediction]
            predictedloaddata_list.append(elem)

        print(f"Prepared {len(predictedloaddata_list)} forecast for location {location}")

        for timestamp, prediction in predictedloaddata_list:
            save_forecast_result(timestamp, prediction, location)

        
        predictedloaddata_dataframe = pd.DataFrame(predictedloaddata_list)
        df_export = predictedloaddata_dataframe.rename(
            columns={0: 'Datum i vreme', 1: 'Prognozirano opterecenje'}
        )
        df_export['Location'] = location
        csv_filename = f"prognoza_{location}_{start_date}_{days}dana.csv"
        df_export.to_csv(csv_filename, index=False)

        print(f" CSV saved: {csv_filename}")
        return predictedloaddata_list

    except Exception as e:
        print(f"Forecast error: {e}")
        import traceback
        traceback.print_exc()
        return []

def list_available_models():
    model_files = find_model_files()
    
    if not model_files:
        return []
    
    models = []
    for model_path in model_files:
        try:
            size_kb = os.path.getsize(model_path) / 1024
            models.append({
                'name': os.path.basename(model_path),
                'path': model_path,
                'size_kb': f"{size_kb:.1f} KB",
                'modified': datetime.fromtimestamp(os.path.getmtime(model_path)).strftime('%Y-%m-%d %H:%M'),
                'location': os.path.dirname(model_path)
            })
        except:
            continue
    
    return models




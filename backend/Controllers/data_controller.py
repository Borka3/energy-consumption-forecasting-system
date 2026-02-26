from flask import request
import pandas as pd
import io
from .base_controller import BaseController
from DatabaseFunctions.data_writers import (
    add_consumption_record, 
    add_weather_record,
    add_holiday_record
)

class DataController(BaseController):
    
    @staticmethod
    def handle_load_data():
        try:
            if not request.files:
                return DataController.error_response("No files uploaded", 400)
            

            files_dict = request.files.to_dict()
            
         
            if 'files[]' in files_dict:
                files = request.files.getlist('files[]')
            else:
               
                files = []
                seen_names = set()
                
                for key, file in files_dict.items():
                    if file and file.filename:
                        
                        if file.filename not in seen_names:
                            seen_names.add(file.filename)
                            files.append(file)
            
            if not files:
                return DataController.error_response("No CSV files found in the uploaded folder", 400)
            
            results = []
            total_records = 0
            processed_count = 0
            
            for file in files:
                if file.filename and file.filename.lower().endswith('.csv'):
                    try:
                       
                        content = file.read().decode('utf-8')
                        
                        
                        file.seek(0)
                        
                        df = pd.read_csv(io.StringIO(content))
                        
                   
                        records_added = 0
                        for i in range(df.shape[0]):
                            row = df.iloc[i]
                            
                           
                            timestamp = row.get('Time Stamp') or row.get('timestamp') or row.get('Timestamp') or ''
                            location = row.get('Name') or row.get('location') or row.get('Location') or 'Unknown'
                            ptid = int(row.get('PTID') or row.get('ptid') or 0)
                            load_value = float(row.get('Load') or row.get('load') or row.get('MW') or 0)
                            
                            add_consumption_record(
                                timestamp=str(timestamp),
                                timezone="EST",
                                location=str(location),
                                ptid_code=ptid,
                                power_load=load_value
                            )
                            records_added += 1
                        
                        total_records += records_added
                        processed_count += 1
                        results.append({
                            'filename': file.filename,
                            'rows_processed': records_added,
                            'status': 'success'
                        })
                        
                    except Exception as e:
                        results.append({
                            'filename': file.filename,
                            'error': str(e),
                            'status': 'failed'
                        })
                elif file.filename:
                   
                    results.append({
                        'filename': file.filename,
                        'error': 'Ignored - not a CSV file',
                        'status': 'skipped'
                    })
            
            return DataController.success_response({
                'total_records': total_records,
                'processed_files': processed_count,
                'skipped_files': len(files) - processed_count,
                'details': results
            }, f"Loaded {total_records} records from {processed_count} CSV files")
            
        except Exception as e:
            return DataController.handle_exception(e)
    
    @staticmethod
    def handle_weather_data():
        try:
            if not request.files:
                return DataController.error_response("No files uploaded", 400)
            
           
            files_dict = request.files.to_dict()
            
            if 'files[]' in files_dict:
                files = request.files.getlist('files[]')
            else:
                files = []
                seen_names = set()
                
                for key, file in files_dict.items():
                    if file and file.filename:
                        if file.filename not in seen_names:
                            seen_names.add(file.filename)
                            files.append(file)
            
            if not files:
                return DataController.error_response("No CSV files found in the uploaded folder", 400)
            
            results = []
            total_records = 0
            processed_count = 0
            
            for file in files:
                if file.filename and file.filename.lower().endswith('.csv'):
                    try:
                        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
                        records_added = 0
                        
                        for i in range(df.shape[0]):
                            row = df.iloc[i]
                            
                            add_weather_record(
                                location=str(row.get('name') or row.get('location') or 'Unknown'),
                                measurement_time=str(row.get('datetime') or row.get('timestamp') or ''),
                                temperature=float(row.get('temp') or row.get('temperature') or 0),
                                feels_like=float(row.get('feelslike') or row.get('feels_like') or 0),
                                dew_point=float(row.get('dew') or row.get('dewpoint') or 0),
                                humidity=float(row.get('humidity') or 0),
                                precipitation=float(row.get('precip') or row.get('precipitation') or 0),
                                precip_probability=float(row.get('precipprob') or row.get('precip_probability') or 0),
                                precip_type=str(row.get('preciptype') or row.get('precip_type') or ''),
                                snow_level=float(row.get('snow') or row.get('snow_level') or 0),
                                snow_depth=float(row.get('snowdepth') or row.get('snow_depth') or 0),
                                wind_gust=float(row.get('windgust') or row.get('wind_gust') or 0),
                                wind_speed=float(row.get('windspeed') or row.get('wind_speed') or 0),
                                wind_direction=float(row.get('winddir') or row.get('wind_direction') or 0),
                                pressure=float(row.get('sealevelpressure') or row.get('pressure') or 1013),
                                cloud_cover=float(row.get('cloudcover') or row.get('cloud_cover') or 0),
                                visibility=float(row.get('visibility') or 10),
                                solar_radiation=float(row.get('solarradiation') or row.get('solar_radiation') or 0),
                                solar_energy=float(row.get('solarenergy') or row.get('solar_energy') or 0),
                                uv_index=int(row.get('uvindex') or row.get('uv_index') or 0),
                                severe_risk=str(row.get('severerisk') or row.get('severe_risk') or ''),
                                conditions=str(row.get('conditions') or 'Clear')
                            )
                            records_added += 1
                        
                        total_records += records_added
                        processed_count += 1
                        results.append({
                            'filename': file.filename,
                            'rows_processed': records_added,
                            'status': 'success'
                        })
                        
                    except Exception as e:
                        results.append({
                            'filename': file.filename,
                            'error': str(e),
                            'status': 'failed'
                        })
                elif file.filename:
                    results.append({
                        'filename': file.filename,
                        'error': 'Ignored - not a CSV file',
                        'status': 'skipped'
                    })
            
            return DataController.success_response({
                'total_records': total_records,
                'processed_files': processed_count,
                'skipped_files': len(files) - processed_count,
                'details': results
            }, f"Weather data imported - {total_records} records from {processed_count} CSV files")
            
        except Exception as e:
            return DataController.handle_exception(e)
    
    @staticmethod
    def handle_holiday_data():
        try:
            if 'file' not in request.files:
                return DataController.error_response("No file uploaded", 400)
            
            file = request.files['file']
            
            if not file.filename.endswith(('.xls', '.xlsx')):
                return DataController.error_response("File must be Excel format (.xls, .xlsx)", 400)
            
            df = pd.read_excel(io.BytesIO(file.read()))
            records_added = 0
            
            for i in range(df.shape[0]):
                row = df.iloc[i]
                
                add_holiday_record(
                    year=int(row.get('year') or 0),
                    day_of_week=str(row.get('day') or row.get('day_of_week') or ''),
                    holiday_date=str(row.get('date') or row.get('holiday_date') or ''),
                    holiday_name=str(row.get('holiday_name') or row.get('holiday') or '')
                )
                records_added += 1
            
            return DataController.success_response({
                'filename': file.filename,
                'rows_processed': records_added
            }, "Holidays data uploaded successfully")
            
        except Exception as e:
            return DataController.handle_exception(e)
        


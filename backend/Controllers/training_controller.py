from flask import request
from .base_controller import BaseController
from Services import training_service
import os
from datetime import datetime

class TrainingController(BaseController):
    
    @staticmethod
    def handle_training():
        try:
            data = request.json
            print(f" Training request received: {data}")
            
           
            is_valid, error_message = TrainingController.validate_required_fields(
                data, ['startDate', 'endDate']
            )
            if not is_valid:
                return TrainingController.error_response(error_message, 400)
            
            start_date = data['startDate']
            end_date = data['endDate']
            region = "N.Y.C."
            hyperparams = data.get('hyperparams', training_service.get_default_hyperparams())
            
          
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                
                if start_dt > end_dt:
                    return TrainingController.error_response(
                        "The start date must be before the end date", 400
                    )
                
              
                days_diff = (end_dt - start_dt).days
                if days_diff > 1500:
                    return TrainingController.error_response(
                        "The training period cannot be longer than 1500 days", 400
                    )
                    
            except ValueError:
                return TrainingController.error_response(
                    "Invalid date format. Use it YYYY-MM-DD", 400
                )
            
            print(f" Starting training for region '{region}': {start_date} to {end_date}")
            
            
            result = training_service.train_model(start_date, end_date, hyperparams)
            
            if result.get('success'):
                return TrainingController.success_response({
                    'region': region,
                    'model_path': result.get('model_path'),
                    'metrics': result.get('metrics'),
                    'training_time': result.get('training_time'),
                    'data_info': result.get('data_info')
                }, result.get('message', "Training successfully completed!"))
            else:
                return TrainingController.error_response(
                    result.get('message', 'Training failed.'),
                    400
                )
                
        except Exception as e:
            print(f" Controller error: {e}")
            return TrainingController.handle_exception(e)
    
    
    
   
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Field '{field}' is mandatory"
        
        if 'startDate' in data and 'endDate' in data:
            try:
                start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
                end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
                
                if start_date > end_date:
                    return False, "The start date must be before the end date"
                    
            except ValueError:
                return False, "Invalid date format. Use it YYYY-MM-DD"
        
        return True, ""
    

    
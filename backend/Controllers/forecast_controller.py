from flask import request
from .base_controller import BaseController
from Services import forecast_service
from Services import training_service
from datetime import datetime

class ForecastController(BaseController):

    @staticmethod
    def handle_forecast():
        try:
            data = request.json
            
          
            is_valid, error_message = ForecastController.validate_required_fields(
                data, ['startDate', 'days']
            )
            if not is_valid:
                return ForecastController.error_response(error_message, 400)
            
            start_date = data['startDate']
            days = int(data['days'])
            location = "N.Y.C."
            
           
            if not (1 <= days <= 7):
                return ForecastController.error_response("Days must be between 1 and 7", 400)
            
          
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                return ForecastController.error_response("Invalid date format. Use YYYY-MM-DD", 400)
            
          
            results = forecast_service.forecast(start_date, days, location)
            
            if results:
                return ForecastController.success_response({
                    'forecasts_count': len(results),
                    'csv_file': f"prognoza_{location}_{start_date}_{days}dana.csv",
                    'location': location, 
                    'sample': results[:10],
                    'statistics': ForecastController._calculate_statistics(results)
                }, f"Forecast successful for location {location}!")
            else:
                return ForecastController.error_response(f"Forecast failed for location {location}", 500)
                
        except Exception as e:
            return ForecastController.handle_exception(e)
    
    @staticmethod
    def _calculate_statistics(results):
        if not results:
            return {}
        
        loads = [load for _, load in results]
        return {
            'min': min(loads),
            'max': max(loads),
            'avg': sum(loads) / len(loads),
            'total': sum(loads),
            'count': len(loads)
        }
    

    
from flask import request
from .base_controller import BaseController
from DatabaseFunctions.data_readers import fetch_forecasts_by_period
from datetime import datetime
import math
from collections import defaultdict


class ResultsController(BaseController):

    @staticmethod
    def get_forecast_results():
        try:
            data = request.json

            
            is_valid, error_message = ResultsController.validate_required_fields(
                data, ['startDate', 'endDate']
            )
            if not is_valid:
                return ResultsController.error_response(error_message, 400)

            start_date = data['startDate']
            end_date = data['endDate']

            
            forecasts = fetch_forecasts_by_period(start_date, end_date)

            if not forecasts:
                return ResultsController.error_response("No forecasts found for selected period", 404)

            
            formatted_forecasts = []
            for forecast in forecasts:
                formatted_forecasts.append({
                    'id': forecast[0],
                    'timestamp': forecast[1],
                    'predicted_load': float(forecast[2]),
                    'location': forecast[4],  
                    'created_at': forecast[3]
                })

            return ResultsController.success_response({
                'count': len(formatted_forecasts),
                'forecasts': formatted_forecasts,
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            }, "Forecast data retrieved successfully")

        except Exception as e:
            return ResultsController.handle_exception(e)

    
   
    

    
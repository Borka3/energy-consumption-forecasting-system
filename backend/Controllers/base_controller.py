from flask import jsonify
from datetime import datetime
import traceback

class BaseController:
    
    @staticmethod
    def success_response(data=None, message="Success", status_code=200):
        response = {
            'success': True,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        if data is not None:
            response['data'] = data
        return jsonify(response), status_code
    
    @staticmethod
    def error_response(message="Error", status_code=500, details=None):
        response = {
            'success': False,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        if details:
            response['details'] = str(details)
        return jsonify(response), status_code
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        if not data:
            return False, "Request data is required"
        
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        return True, None
    
    @staticmethod
    def handle_exception(e):
        error_details = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return BaseController.error_response(
            message="Internal server error",
            status_code=500,
            details=error_details
        )
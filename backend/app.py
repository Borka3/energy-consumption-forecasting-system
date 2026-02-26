from flask import Flask
from flask_cors import CORS
from Controllers.data_controller import DataController
from Controllers.training_controller import TrainingController
from Controllers.forecast_controller import ForecastController
from Controllers.results_controller import ResultsController


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) 

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return {
        "status": "healthy",
        "service": "Electric Consumption Forecast API",
        "version": "1.0.0"
    }, 200


@app.route('/api/data/load', methods=['POST'])
def load_data():
    return DataController.handle_load_data()

@app.route('/api/data/weather', methods=['POST'])
def weather_data():
    return DataController.handle_weather_data()

@app.route('/api/data/holidays', methods=['POST'])
def holidays_data():
    return DataController.handle_holiday_data()

@app.route('/api/training/train', methods=['POST'])
def train_model():
    return TrainingController.handle_training()

@app.route('/api/forecast/generate', methods=['POST'])
def generate_forecast():
    return ForecastController.handle_forecast()

@app.route('/api/results/forecasts', methods=['POST'])
def get_forecasts():
    return ResultsController.get_forecast_results()


@app.route('/api/test/connection', methods=['GET'])
def test_connection():
    return {"status": "connected", "database": "electric_consumption"}, 200

if __name__ == '__main__':
    print("=" * 60)
    print(" Electric Consumption Forecast API")
    print("=" * 60)
    print("\n Available endpoints:")
    print("  HEALTH:")
    print("    GET  /api/health")
    print("    GET  /api/test/connection")
    
    print("\n  DATA:")
    print("    POST /api/data/load      - Import load CSV")
    print("    POST /api/data/weather   - Import weather CSV")
    print("    POST /api/data/holidays  - Import holidays Excel")
    
    print("\n  TRAINING:")
    print("    POST /api/training/train   - Train model (NYC only)")
  
    print("\n  FORECAST:")
    print("    POST /api/forecast/generate - Generate forecast (NYC only)")
    
    print("\n  RESULTS:")
    print("    POST /api/results/forecasts  - Get forecast results")
 
    
    
    app.run(debug=True, host='0.0.0.0', port=5000)
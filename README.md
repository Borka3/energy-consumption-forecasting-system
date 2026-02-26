# energy-consumption-forecasting-system

# Short-Term Electricity Consumption Forecast ⚡

---

##  Project Overview
The goal of this project is to develop an application for **short-term electricity consumption forecasting** based on historical and weather data.  
The forecast is performed on an **hourly resolution**, for a period of **1 to 7 days**, using a **neural network (Dense layers)**.  

The application is built in a **multi-layer architecture**:
- **User Interface layer** – interactive UI for data import, training, and forecast visualization  
- **Controller layer** – handles communication between the UI and the service layer, processes user requests, and forwards them to the business logic  
- **Service layer** – training, forecasting, data selection, and business logic  
- **Database layer** – storing input data and forecast results  

---

##  Features
- **Data Import**  
  - Ability to select CSV files  
  - Data is stored in the database on an hourly level  

- **Interactive Training Interface**  
  - User can select hyperparameters (number of layers, neurons, epochs...)  
  - Training is triggered directly from the UI  

- **Model Training**  
  - Training is performed for a selected date range  
  - Trained models are saved to file  
  - Success message displayed in the UI  

- **Consumption Forecast**  
  - User selects a start date and number of days (up to 7)  
  - Forecast is generated on an hourly level  
  - Results are stored in the database and exported to CSV  

- **Forecast Visualization**  
  - Forecasted values can be displayed for a selected date range  

---

##  Technologies
- **Python** (TensorFlow/Keras, Pandas, NumPy, Scikit-learn)  
- **SQLite** database  
- **Flask / Streamlit** for the user interface  
- **Multi-layer architecture** (UI,controller layer, service layer, database)  

---

##  Model
- **Dense neural network**   
- **Loss function**: Mean Squared Error (MSE)  
- **Optimizer**: Adam  
- **Feature engineering**: lag variables (previous hour/day consumption), weather data, holidays  

---

##  How to Run
1. Clone the repository:
2. Run the backend:
   Navigate to the backend folder and start the server:
   ```
   cd backend
   python app.py
   ```
4. Run the frontend:
   Navigate to the frontend folder and start the application:
   ```
   cd frontend
   npm install
   npm start
   ```
   







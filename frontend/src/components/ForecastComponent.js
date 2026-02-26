import React, { useState, useEffect } from 'react';
import { beginForecast, beginForecastTwoRegions, getTrainingRegions } from '../services/ForecastService';
import '../components.css';

const ForecastComponent = () => {
    const [startDate, setStartDate] = useState('');
    const [days, setDays] = useState('');
    const [loading, setLoading] = useState(false);



    const handleSubmit = async () => {
        if (!startDate || !days) {
            alert("Pick a date and number of days!");
            return;
        }

        const daysNum = parseInt(days);
        if (daysNum < 1 || daysNum > 7) {
            alert("Days must be 1-7!");
            return;
        }

        setLoading(true);

        try {
            
            const response = await beginForecast(startDate, daysNum );
            
            alert(response.data.message || "Forecast generated!");
            setStartDate('');
            setDays('');
        } catch (error) {
            alert(error.response?.data?.message || "Error generating forecast");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="component-container">
            <h2 className="component-title"> Forecast</h2>

            <div className="form-group">
                <label>Start date:</label>
                <input 
                    type="date" 
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="form-input"
                />
            </div>

            <div className="form-group">
                <label>Days (1-7):</label>
                <input 
                    type="number" 
                    min="1"
                    max="7"
                    value={days}
                    onChange={(e) => setDays(e.target.value)}
                    className="form-input"
                    placeholder="Enter 1-7"
                />
            </div>

            <button 
                onClick={handleSubmit}
                disabled={loading}
                className="form-button forecast-button"
            >
                {loading ? "Generating..." : "BEGIN FORECAST"}
            </button>
        </div>
    );
};

export default ForecastComponent;